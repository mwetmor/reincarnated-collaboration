# 2026-05-18 — drax-demo — R2 + Vercel hybrid deployment for VS2a mobile playtest

**Authority:** Matt L3 morning 2026-05-18 verbatim "fire drax on the R2 hybrid implementation. Accept #1."
**Type:** Pattern B; ~2-4 hours.
**Predecessor:** Drax v1.18.5 + v1.19 + v1.20 + v1.20.1 + v1.21 SHIPPED. Track A.2 D11.5 + mobile-render-validation in flight; this dispatch queues after Track A.2.
**Status:** 🟡 **QUEUED — fires after Track A.2 lands. Pattern B; matt-manual Cloudflare setup is prerequisite.**

---

## Why this matters

Demo deploy currently impossible on Vercel — build output is 6.1GB (1.1GB craftpix dungeon tileset + 4GB audio packs + remaining sprites + code bundle). Way over Vercel's free tier limits and the asset-pipeline issue blocks mobile playtest via deployed URL.

R2 hybrid splits the deployment:
- **Vercel**: hosts the demo code bundle (~10MB Pixi.js + game logic + HTML/CSS) — well within free tier
- **Cloudflare R2**: hosts vendor assets (~6GB sprites + audio) — $0.10-1/mo storage, FREE egress

Total cost: $0.10-1/mo. Time to ship: ~2-4h drax once Matt's Cloudflare prerequisites are in place.

This unblocks mobile playtest via a real deployed URL — Matt can hit the URL from his phone, share with playtesters, get real-device feedback that DevTools mobile emulation can't replicate.

---

## Matt-manual prerequisites (REQUIRED before drax starts)

Matt completes these before drax fires:

1. Cloudflare account (free signup at dash.cloudflare.com)
2. Enable R2 (requires card on file even if free tier)
3. Create bucket (e.g., `reincarnated-assets`)
4. Enable public access → save the `pub-XXXXX.r2.dev` URL
5. Generate API token (Object Read & Write scope) → save Access Key ID + Secret + S3 endpoint URL
6. CORS policy: `[{"AllowedOrigins": ["*"], "AllowedMethods": ["GET", "HEAD"], "AllowedHeaders": ["*"], "MaxAgeSeconds": 86400}]`

Matt provides drax with the public r2.dev URL + API credentials before drax fires. Credentials should NOT be committed to git — use `~/.r2-credentials.env` or 1Password.

---

## Required reading

1. **Cloudflare R2 docs:** https://developers.cloudflare.com/r2/ (S3-compatible API + URL structure)
2. **Existing Vite static asset handling:** `vite.config.ts` + `public/` structure
3. **Existing asset reference patterns:** grep for `/assets/` + `/audio/sfx/` + `/seasons/` across `src/`
4. **Demo .gitignore:** check what's currently excluded from git (kenney/ oga/ leohpaz/ etc. — those are already vendor-local-only)
5. **Pixi loader docs:** Pixi.js handles full-URL Texture sources natively (no special config needed)

---

## Scope — four implementation blocks

### Block 1 — Asset URL helper + path audit

Author `src/utils/assetPath.ts`:

```typescript
/**
 * Asset path resolver — routes to R2 in production, local public/ in dev.
 *
 * R2_BASE is the Cloudflare R2 public URL; baked in at build time via Vite env.
 * In dev mode (npm run dev), VITE_R2_BASE is unset → falls through to local /assets/ paths.
 * In prod mode (npm run build), VITE_R2_BASE is set → all asset paths route to R2.
 *
 * Examples:
 *   assetUrl('/assets/chierit/lightning-ronin/idle.png')
 *   → dev:  '/assets/chierit/lightning-ronin/idle.png' (Vite serves from public/)
 *   → prod: 'https://pub-abc123.r2.dev/assets/chierit/lightning-ronin/idle.png'
 *
 * Pixi.js Texture.from() + Howler.js accept full URLs natively — no extra config.
 */
const R2_BASE = import.meta.env.VITE_R2_BASE ?? '';

export function assetUrl(path: string): string {
  // Path normalization: ensure leading slash; strip any double slashes
  const normalized = ('/' + path).replace(/\/\/+/g, '/');
  return `${R2_BASE}${normalized}`;
}

// Convenience helpers for common asset roots (catches direct string-concat callers):
export const assetsUrl = (subpath: string) => assetUrl('/assets/' + subpath);
export const audioUrl  = (subpath: string) => assetUrl('/audio/' + subpath);
export const seasonsUrl = (subpath: string) => assetUrl('/seasons/' + subpath);
```

Then grep + refactor all hardcoded paths:

```bash
# Find all asset path usages
grep -rn "'/assets/\|\"/assets/\|'/audio/\|\"/audio/\|'/seasons/\|\"/seasons/" src/ --include='*.ts' --include='*.tsx' --include='*.js'
```

Replace direct string literals with `assetUrl()` / `assetsUrl()` / `audioUrl()` / `seasonsUrl()` helper calls. Most usages will be in:
- `src/visuals/dungeonTileset.ts` (PACK_298079 + PACK_125640 + PACK_169442 constants)
- `src/visuals/ambientPropsExtension.ts`
- `src/visuals/spriteVfx.ts` (Fantasy%20Spells category paths)
- `src/visuals/chierit*.ts` + monsters renderer
- `src/audio/audio.ts` (Howler.js load paths)
- `src/encounter/gauntlet.ts` (season JSON loads via fetch)
- `src/main.ts` (anywhere assets are referenced)

### Block 2 — Vite env var + build config

Add to `.env.example` (commit this; documents the env contract):
```
# Production R2 asset base URL (omit in dev)
# Example: VITE_R2_BASE=https://pub-abc123def456.r2.dev
VITE_R2_BASE=
```

Add to `.gitignore`:
```
.env.local
.env.production.local
```

Matt sets `VITE_R2_BASE` in Vercel's environment variables UI for the production deployment (Vercel dashboard → Project Settings → Environment Variables). Dev (`npm run dev`) leaves it unset; Vite picks up from `public/` locally.

Verify `vite.config.ts` includes proper `define`-time substitution; default config handles `import.meta.env.VITE_*` natively.

### Block 3 — Asset upload script (one-shot + idempotent re-upload)

Author `scripts/upload-assets-to-r2.sh`:

```bash
#!/usr/bin/env bash
# Upload public/assets/ + public/audio/ + public/seasons/ to Cloudflare R2.
#
# Prerequisites:
#   1. AWS CLI installed: brew install awscli
#   2. ~/.r2-credentials.env file with:
#        export AWS_ACCESS_KEY_ID="..."
#        export AWS_SECRET_ACCESS_KEY="..."
#        export R2_ENDPOINT="https://<account-id>.r2.cloudflarestorage.com"
#        export R2_BUCKET="reincarnated-assets"
#   3. Bucket already created with public access enabled
#
# Usage: ./scripts/upload-assets-to-r2.sh
#
# Idempotent: aws s3 sync only uploads changed/new files.

set -euo pipefail

# Load credentials
[[ -f ~/.r2-credentials.env ]] || { echo "Missing ~/.r2-credentials.env"; exit 1; }
source ~/.r2-credentials.env

echo "→ Uploading public/assets/ to R2..."
aws s3 sync public/assets/ "s3://${R2_BUCKET}/assets/" \
    --endpoint-url "${R2_ENDPOINT}" \
    --cache-control "public, max-age=31536000, immutable" \
    --delete  # remove R2 files that no longer exist locally

echo "→ Uploading public/audio/ to R2..."
aws s3 sync public/audio/ "s3://${R2_BUCKET}/audio/" \
    --endpoint-url "${R2_ENDPOINT}" \
    --cache-control "public, max-age=31536000, immutable" \
    --delete

echo "→ Uploading public/seasons/ to R2..."
aws s3 sync public/seasons/ "s3://${R2_BUCKET}/seasons/" \
    --endpoint-url "${R2_ENDPOINT}" \
    --cache-control "public, max-age=3600" \
    --delete  # season JSONs may update; shorter cache

echo "✓ R2 upload complete. Verify at https://<pub-url>.r2.dev/assets/..."
```

`chmod +x scripts/upload-assets-to-r2.sh`. Document in `README.md` under "Deployment" section.

### Block 4 — Vercel project setup + smoke test

1. Add `vercel.json` to demo repo (mirror loadout's pattern):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite"
}
```

2. Add to `.vercelignore`:
```
public/assets/
public/audio/
public/seasons/
node_modules/
src/
scripts/
*.md
```

This excludes the heavy asset dirs from the Vercel build — they're served from R2 instead. The `public/` files that REMAIN (e.g., `icon-192.png`, `manifest.json`, `index.html` favicon refs) stay on Vercel.

3. Matt links demo repo to a new Vercel project (one-time):
```bash
cd ~/Games/reincarnated-demo
npx vercel  # interactive: log in, create new project, link to GitHub
# OR Vercel dashboard → Import Project → GitHub → reincarnated-demo
```

4. Matt sets `VITE_R2_BASE` env var in Vercel dashboard (Production scope)

5. Drax smoke test sequence:
   - Run `scripts/upload-assets-to-r2.sh` first (uploads 6GB; may take 20-60 min depending on connection)
   - Verify a sample asset loads in browser: `https://<pub-url>.r2.dev/assets/chierit/lightning-ronin/idle.png` should return PNG
   - Local prod build: `VITE_R2_BASE=https://<pub-url>.r2.dev npm run build && npm run preview` — verify assets load from R2 not 404
   - Push to main → Vercel auto-deploys → hit Vercel URL → verify game playable + assets load
   - Hit Vercel URL from phone → verify mobile playable (touch zones from v1.20 + portrait canvas from v1.21 already in place)

---

## Acceptance criteria

- [ ] Matt completes Cloudflare prerequisites (R2 bucket + public URL + API token + CORS + ~/.r2-credentials.env)
- [ ] Block 1: `src/utils/assetPath.ts` authored; all hardcoded `/assets/` `/audio/` `/seasons/` paths refactored to use helpers
- [ ] Block 2: `.env.example` documents `VITE_R2_BASE`; `.gitignore` excludes `.env.local`
- [ ] Block 3: `scripts/upload-assets-to-r2.sh` authored + executable; documented in README
- [ ] Block 4: `vercel.json` + `.vercelignore` added; Matt links Vercel project + sets env var; smoke test passes end-to-end
- [ ] Local `npm run dev` still works unchanged (env var unset → falls through to local `/assets/`)
- [ ] `npm run build` clean
- [ ] Push triggers Vercel deploy; deployed URL loads game + assets from R2; mobile playable
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.22-r2-hybrid-deployment-1`

(Note: tag conflicts with existing #187 v1.22 portrait camera zoom. Bump this to `v1.23-r2-hybrid-deployment-1` OR ship v1.22 camera zoom first; let drax sequence.)

---

## Out of scope (DO NOT)

- ❌ Trimming vendor assets to a curated subset — that's the long-term post-VS2a cleanup; not this dispatch
- ❌ Setting up a custom domain for R2 — `pub-XXXXX.r2.dev` is fine for VS2a playtest; custom domain is polish-phase
- ❌ Implementing asset versioning / cache busting — `immutable` cache header is sufficient for now; revisit if asset updates need cache invalidation
- ❌ Self-hosting / alternative CDNs — Matt accepted Path 1 (R2 hybrid); other paths out of scope
- ❌ Auditing which assets are actually used at runtime — separate post-VS2a task
- ❌ Modifying the demo gameplay code (other than asset path refactors)
- ❌ Push tag (ADR-006)

---

## Coordination

- **Predecessor:** Drax Track A.2 D11.5 + mobile-render-validation in flight; this dispatch fires after those land
- **Concurrent (parallel-safe):** Drax v1.18 loadout bundle (different repo); rocket re-seed 002017 (different repo); galadriel Track C captures (different repo); star-lord Path A fights.jsonl ingest (different repo)
- **Triggers downstream:**
  - Mobile playtest unlock via real deployed URL (not just local-WiFi-from-phone)
  - VS2a sign-off path opens (one of the remaining critical-path items)
  - Vercel options paper (drax + star-lord) can document this decision retroactively
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Notes on the in-flight options paper

There's a `2026-05-18-drax-plus-star-lord-vercel-deployment-asset-pipeline-options-paper.md` dispatch in queue that was scoped to author a full options-comparison paper. Matt L3 morning verbatim "Accept #1. Fire Drax on R2 hybrid" pre-emptively chose the path. The options paper can now be repurposed as:

- Retrospective documentation of the decision rationale
- OR canceled in favor of just this implementation dispatch

Drax + star-lord decide whether to author the retrospective paper or fold it into this dispatch's completion record. Knight-rider's strong recommendation: fold into completion record; full options paper isn't load-bearing once decision is locked.

---

*Dispatched 2026-05-18 morning by knight-rider per Matt L3 verbatim "Accept #1. Fire Drax on R2 hybrid." ~2-4h drax. Matt-manual Cloudflare prereqs upstream. Pattern B; appends completion record + smoke evidence + R2 storage cost first-week data point when done.*

---

## Completion record

*(drax appends here when done)*
