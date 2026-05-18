# Demo — Vercel Deployment Asset-Pipeline Options Paper

**Authority:** `2026-05-18-drax-plus-star-lord-vercel-deployment-asset-pipeline-options-paper.md` dispatch; invocation § 2.4 deliverable 14.
**Authors:** star-lord (§§ 2, 3 architectural perspective, 5; § 1 measurements; portions of § 4) + drax (§ 1 code-loading patterns, § 3 demo-code-touch complexity, portions of § 4)
**Date:** 2026-05-18
**Status:** STAR-LORD SECTIONS COMPLETE — drax to add § 1.3 (code-loading patterns detail), § 3 per-path code-touch complexity, and co-sign § 4 recommendation
**Decision authority:** Matt L3 on morning

---

## § 0 — TL;DR

The demo's committed binary assets (3.27 GiB) are 3× Vercel Pro's 1 GB static-upload hard limit. A straightforward "deploy the repo" approach is not viable on any Vercel tier without an asset strategy. Four viable paths exist; **Path 4 (vendor-asset subset)** is the recommended Phase-1 move: curate a deployable ~200-400 MB subset of game-critical sprites, deploy it to Vercel Pro, and gate Phase-2 asset expansion to a CDN decision. No URL refactor required for Phase 1.

**Hard constraint tonight:** No deployment commit. This is scoping only. Matt decides on morning.

---

## § 1 — Current state

### 1.1 — Disk inventory

**Demo `public/` directory — full disk inventory:**

| Subdirectory | On-disk size | Git-tracked? | Notes |
|---|---|---|---|
| `public/assets/` | 1.9 GB | Partially | See asset breakdown below |
| `public/audio/sfx/` | ~4.0 GB | Mostly NOT | 3.4 GB of audio packs gitignore'd per `.gitignore` comments |
| `public/audio/music/` | 34 MB | Likely yes | Per-season MP3s; not in `.gitignore` |
| `public/sprites/` | 173 MB | Partially | 3,142 files committed; one large PNG sequence excluded |
| `public/tilesets/` | 13 MB | NOT | License constraint — gitignore'd |
| `public/seasons/` | 6.2 MB | YES | 10 seasons (5 legacy + 5 vs2a); engine-generated JSON data |
| **Total on disk** | **6.1 GB** | — | |

**Public/assets breakdown (sorted by committed file count):**

| Directory | On-disk size | Committed files | Notes |
|---|---|---|---|
| `DireDungeon_Items_Loot/` | 539 MB | 138,032 | Loot animation frames — largest single contributor |
| `chierit/` | 59 MB | 4,211 | Mini-boss/boss sprites (vs2a) |
| `characters/` | 30 MB | 4,159 | Player + enemy character spritesheets |
| `CreativeKind/` | 57 MB | 1,164 | VFX packs |
| `pimen/` | 7.4 MB | 1,273 | Monster sprites |
| `craftpix_catalogue_large/` | 1.1 GB | **0** | NOT committed; local-dev-only catalogue |
| `Elementals_bundle/` | 44 MB | 10 | Elemental VFX (small subset committed) |
| `free_characters_and_vfx/` | 28 MB | **0** | NOT committed; referenced in code |
| `Deathbringer VFX/` | 4.7 MB | 126 | VFX pack |
| `monsters/` | 2.8 MB | 109 | Monster spritesheets |
| Others | ~30 MB | ~300 | Misc (potions, treasure, etc.) |

**Git repository metrics:**
```
Total committed files: 152,631
Git object size (loose):  3.27 GiB
Git pack size (compressed): 205 MiB
```

### 1.2 — What is gitignore'd (not available for Vercel deployment without separate pipeline)

Per `.gitignore`:
- All `public/audio/sfx/*` subdirectories (3.4 GB total; CC0 + commercial packs staged locally)
- `public/tilesets/` (13 MB; license constraint)
- `public/sprites/abilities/Super Pixel Effects Gigapack/PNG/` (large PNG frame sequences; spritesheet/ version is committed)
- `craftpix_catalogue_large/` and `free_characters_and_vfx/` (inferred — 0 files in git)

**Critical note:** Audio is gitignore'd but the demo loads it via `/audio/sfx-manifest.json` at runtime. The manifest file IS committed. If deployed without audio files, the manifest-lookup will silently fail per the audio system's fetch pattern — no crash, just no ambient/SFX audio. Music (`/audio/music/*.mp3`) may be committed (not in `.gitignore`); drax to confirm.

### 1.3 — Asset loading code patterns

*(drax section — to be completed)*

The demo loads assets via URL paths relative to the deploy root:
- Characters: `/assets/characters/{slug}/sheets/{animName}.png`
- Monsters: `/assets/monsters/{slug}/{sheet_path}`
- VFX packs: hard-coded paths like `/assets/free_characters_and_vfx/...`
- Loot: `/assets/DireDungeon_Items_Loot/...`
- Audio: `/audio/sfx-manifest.json` (manifest) + per-event file paths

All asset references are absolute path strings (no Vite `import` statements for binary assets). Switching to a CDN requires a base-URL substitution: either an environment variable (`VITE_ASSET_BASE_URL`) prepended to each path, or a find-replace across all loader files. Drax to estimate the code-touch surface for § 3 per-path complexity.

### 1.4 — `.gitignore` exclusion summary

- `.gitignore` explicitly documents 3.4 GB of gitignore'd audio packs
- Tilesets explicitly excluded (license)
- `craftpix_catalogue_large/` (1.1 GB local catalogue) not committed — local dev only
- Result: committed repo = ~3.27 GiB — still 3× Vercel Pro 1 GB hard limit

---

## § 2 — Vercel tier constraints (star-lord)

Source: `vercel.com/docs/limits` (fetched 2026-05-18) + `vercel.com/pricing` (fetched 2026-05-18).

### 2.1 — Hard deployment limit (the blocker)

| Tier | Static file upload limit | Monthly cost |
|---|---|---|
| Hobby | **100 MB** | Free |
| Pro | **1 GB** | $20/user/month |
| Enterprise | N/A (custom) | Custom |

**The demo at 3.27 GiB committed is above the Pro limit by 3.27×.** This is a hard platform limit, not a soft guideline. Deployments exceeding the limit fail at build/upload step. There is no "just pay more to get past 1 GB" — the 1 GB is an architectural limit, not a billing limit.

The loadout app at 2.3 MB dist output fits comfortably in the Hobby tier. The demo is architecturally different: it's a game runtime with large binary asset libraries.

### 2.2 — Vercel Blob Storage (Pro tier)

| Resource | Included (Pro) | Overage |
|---|---|---|
| Blob Storage | 5 GB/month | $0.023/GB |
| Blob Data Transfer | 100 GB/month | $0.05/GB |
| Blob Simple Ops | 100,000/month | $3.00/million |

Blob Storage is a first-party object store integrated into Vercel projects. Assets uploaded to Blob are served via Vercel's CDN with HTTP caching. The URL form is `https://<blob-store-id>.public.blob.vercel-storage.com/<path>`. **Code must reference Blob URLs, not `/public/assets/` paths.**

5 GB included storage on Pro fits the demo's 3.27 GB committed asset set. Data transfer at 100 GB/month included is adequate for development/preview traffic; heavy production traffic would exceed it.

### 2.3 — Fast Data Transfer (CDN bandwidth)

| Tier | Included | Overage |
|---|---|---|
| Hobby | 100 GB/month | — |
| Pro | 1 TB/month | $0.15/GB (regional pricing) |

For a game demo with limited concurrent users, 100 GB Hobby bandwidth is likely sufficient during development. 1 TB Pro is ample for any reasonable traffic volume at this stage.

### 2.4 — Build constraints

| Resource | Hobby | Pro |
|---|---|---|
| Build time | 45 min | 45 min |
| Disk size during build | 23 GB | 23–64 GB |
| Max files per deployment | 15,000 (source) | 15,000 (source) |
| Concurrent builds | 1 | 12 |

The 15,000 source file limit is separate from the static upload size limit. The demo has 152,631 committed files — **10× the file count limit.** A standard Vercel CI build from the git repo would fail on both file count AND size, even before the 1 GB size limit is reached.

**This makes the file count limit an additional hard blocker**, independent of the storage limit. Any deployment strategy must either:
- Ship only a curated subset of files well under 15,000
- Or use a pre-built artifact approach where Vercel only sees the compiled `dist/` output (not source)

The `dist/` output of a Vite build copies all `public/` files as-is. Even a pre-built approach passes through the 15,000 file limit on the output side.

### 2.5 — Tier summary for demo deployment

| Constraint | Hobby | Pro | Demo current |
|---|---|---|---|
| Static upload size | 100 MB | 1 GB | 3.27 GB committed |
| Max source files | 15,000 | 15,000 | 152,631 committed |
| Bandwidth/month | 100 GB | 1 TB | Low (dev traffic) |
| Monthly cost | Free | $20/user | — |
| Blob storage | 1 GB | 5 GB | — |

**Conclusion:** No standard Vercel deployment path works without asset reduction. The blockers are file count + size, not bandwidth.

---

## § 3 — Strategy options

### Path 1 — Vercel Pro + bandwidth budget ("ship everything")

**Description:** Deploy the full demo repo to Vercel Pro, paying for whatever bandwidth is consumed.

**Cost:**
- $20/month (Pro tier base)
- Bandwidth: ~$0.15/GB overage after 1 TB (negligible at low traffic)
- Storage: N/A — this path assumes assets fit in deployment

**Complexity (star-lord architecture view):** BLOCKED. The demo exceeds both the 1 GB static upload limit AND the 15,000 file limit. Path 1 is not viable on Vercel regardless of tier. There is no Pro-tier option that raises the static upload limit beyond 1 GB (Enterprise is custom but not documented to raise this specifically). This path would require Enterprise negotiation plus likely a build workaround.

**Complexity (drax code-touch):** *(to be added)*

**Time-to-first-deploy:** Blocked — cannot ship.
**Maintenance burden:** N/A.
**Tradeoffs:** Hard no. Do not pursue.

---

### Path 2 — Vercel + external CDN for vendor assets (S3 or Cloudflare R2)

**Description:** Vercel hosts the app code, JS/CSS bundles, and small committed assets (seasons JSON, critical-path sprites). Vendor binary packs (DireDungeon loot, chierit, CreativeKind, characters, etc.) served from an external CDN. Asset-loading code refactored to use CDN base URL.

**Cost (star-lord architecture view):**
- Vercel Pro: $20/month (app code + data transfer)
- Cloudflare R2: $0.015/GB/month storage + free egress. 3 GB = $0.045/month. Negligible.
- AWS S3 alternative: $0.023/GB/month + $0.09/GB egress. 3 GB stored = $0.07/month + bandwidth costs per request. Cloudflare R2 wins on egress cost.
- **One-time upload cost:** ~$0.045 (R2) or $0.07 (S3) for initial 3 GB upload. Round-trip operational cost is < $1/month for low traffic.
- Total ongoing: ~$21/month (Vercel Pro + R2 negligible).

**Complexity (star-lord architecture view):**
- New external accounts (Cloudflare R2 or AWS S3): ~30-60 min setup
- Upload 3.27 GB of assets to CDN: 1-2 hours (depends on connection speed)
- Code change: introduce `VITE_ASSET_BASE_URL` env var; prefix all asset paths. Estimate: touch ~10-15 source files.
- Vercel deploy of app-only subset: < 1 hour once CDN is populated
- Ongoing: CDN invalidation when assets change (minor operational burden)

**Complexity (drax code-touch):** *(to be added — estimate touch surface for asset base URL refactor)*

**Time-to-first-deploy:** 4-8 hours from Matt approval (account setup + asset upload + code refactor + deploy)
**Maintenance burden:** Low. Asset refreshes require CDN re-upload + cache invalidation. CDN is durable; no per-deploy re-upload.
**Tradeoffs:** Two-vendor complexity. Cloudflare R2 free egress is a clear winner over S3 for game assets.

---

### Path 3 — Vercel Blob Storage

**Description:** Upload vendor assets to Vercel Blob (first-party object store). App code in Vercel deployment. Asset URLs become `https://<blob-id>.public.blob.vercel-storage.com/...`. Code refactored to use Blob URLs.

**Cost:**
- Vercel Pro: $20/month (includes 5 GB Blob storage — covers demo assets)
- Blob Data Transfer: 100 GB/month included; $0.05/GB overage
- Overage risk: 3 GB assets × 30-40 requests per user per session = high bandwidth at scale, low at dev traffic. At < 100 users/day: well within included 100 GB.

**Complexity (star-lord architecture view):**
- Use `vercel blob upload` CLI or `@vercel/blob` SDK to upload assets. Documented, first-party tooling.
- Code change: same `VITE_ASSET_BASE_URL` approach as Path 2. Same touch surface.
- Advantage: single-vendor. No separate CDN account. The `vercel:deployment-expert` agent covers this end-to-end.
- Disadvantage: Blob Storage URLs are not the same as the current path structure. Assets must be uploaded with same relative structure to keep paths consistent.
- Upload time: same as Path 2 (network-bound, not tool-bound).

**Complexity (drax code-touch):** *(to be added)*

**Time-to-first-deploy:** 3-6 hours from Matt approval (Blob upload + code refactor + deploy)
**Maintenance burden:** Low. Vercel CLI handles re-uploads. Integrated into Pro billing.
**Tradeoffs:** Single-vendor simplicity. Slightly more expensive at scale than R2 ($0.05/GB vs R2 free egress). Fully integrated into Vercel dashboard. Recommended over R2 unless egress cost becomes material (it won't at this stage).

---

### Path 4 — Vendor-asset subset for deployment ("curated demo subset")

**Description:** Identify the minimum game-functional asset subset (~200-400 MB), deploy only that subset to Vercel (fits within Pro 1 GB limit and well under 15,000 file count). Full library stays local for development. Demo URL showcases a curated subset; DireDungeon loot, large catalogues, and non-essential VFX gracefully absent or shimmed.

**Cost:**
- Vercel Pro: $20/month
- No external CDN
- No code refactor (paths unchanged)
- One-time effort: identify subset, add `.vercelignore` entries

**Complexity (star-lord architecture view):**
- The 138,032-file DireDungeon_Items_Loot/ accounts for 90% of the file count blocker. Excluding it from deployment (`.vercelignore` or `.gitignore` update) immediately solves the file count problem.
- DireDungeon handles loot drop animations. If excluded, loot drops either show fallback sprite or are suppressed. Drax to confirm whether this degrades critical demo flow.
- After excluding DireDungeon: remaining committed assets ≈ 152K - 138K = ~14K files. Just under the 15,000 limit.
- Committed asset size after DireDungeon exclusion: ~3.27 GB - ~539 MB = ~2.73 GB. Still over 1 GB limit.
- After further exclusion of chierit (59 MB, 4,211 files), characters raw-frame directories (leaving only spritesheets), other large VFX packs: a targeted subset of ~400-600 MB, ~8,000-10,000 files is achievable.
- This is a **file selection problem**, not an architecture problem. Drax knows which assets are critical for the vs2a demo vs optional. The subset is likely: seasons/*.json, core character spritesheets, pimen/used-subset, monsters/used-subset, critical VFX.

**Complexity (drax code-touch):** *(minimal — paths unchanged; `.vercelignore` addition only)*

**Time-to-first-deploy:** ~2-4 hours from Matt approval (asset audit + .vercelignore + first deploy attempt)
**Maintenance burden:** Low. New asset packs added to demo must be evaluated against the deployment budget. The constraint is visible and deliberate.
**Tradeoffs:** Demo shows a subset, not the full library. For a pitch demo or player link, the critical-path content is more important than completeness. Phase-2 expands to full library via Path 2 or 3 once the demo URL is established and the CDN path is worth the investment.

---

### Path 5 — Self-hosted elsewhere (Netlify, Cloudflare Pages, GitHub Pages)

**Description:** Deploy demo to an alternative static host.

**Complexity (star-lord architecture view):**
- GitHub Pages: Free. Size limit: 1 GB per repository. Same file count concerns.
- Netlify Free: 100 GB bandwidth, 300 min/month build time. Deployment size limit: not officially documented, but similar to Vercel (~500 MB practical limit). Would face same asset-pipeline problem.
- Cloudflare Pages: Free tier. Same file count concern (20,000 files/deploy limit on free tier). **This is actually slightly better than Vercel on file count.** $20/month Pro tier = 20,000 file limit; same blocker.
- The root problem (too many binary assets) exists on every platform. The asset pipeline architecture choice (Path 2/3/4) must still be made; only the deployment host changes.
- Given the loadout app is already on Vercel Pro, adding the demo to the same Vercel team is the simplest operational path. Path 5 adds platform complexity without solving the core problem.

**Tradeoffs:** Does not solve the asset problem; adds operational complexity of a second hosting platform. Not recommended as a standalone path.

---

## § 4 — Recommendation

### 4.1 — star-lord recommendation

**Phase 1: Path 4 (vendor-asset subset).** This is the right move for tonight/tomorrow.

Reason: The goal of Phase 1 is **a working demo URL**. Not a full-library deployment. Not CDN architecture. A URL that Matt or a future viewer can click and see the game run. Path 4 achieves this in 2-4 hours without new accounts, code refactors, or architecture decisions. The constraint is deliberate and visible — `.vercelignore` says exactly what was excluded and why.

The DireDungeon_Items_Loot/ exclusion alone removes 138,032 files. What remains (if the loot system gracefully degrades) likely fits within the 1 GB + 15,000 file limits with careful selection. Drax is best positioned to confirm what's critical-path for the demo — that confirmation is the key gate before the deployment runs.

**Phase 2: Path 3 (Vercel Blob).** Once the demo URL is live and Path 4 is validated, the Phase-2 asset expansion is the blob migration. Single-vendor. Tooled by `vercel:deployment-expert`. The code touch (base URL env var) is a clean refactor with known scope. R2 (Path 2) is equally valid as a Phase-2 option but adds an external account; Blob's integrated billing and Vercel-native tooling is the cleaner path unless egress costs become material.

**Do NOT pursue Path 1** (no viable path on Vercel). Path 5 (other host) adds complexity without solving the root problem.

### 4.2 — drax recommendation

*(to be added — drax confirms which assets are critical-path for vs2a demo; co-signs or amends the Path 4 recommendation)*

---

## § 5 — Vercel deployment-expert consultation pre-stage (star-lord)

This section describes the shape of the dispatch that knight-rider should draft (unfired tonight) for `vercel:deployment-expert` once Matt approves a path.

**If Matt approves Path 4 (subset):**
```
Dispatch type: vercel:deployment-expert consultation
Scope: Deploy reincarnated-demo to Vercel Pro as static site.
Context: Demo is a Pixi.js game; Vite build; public/ contains large binary assets
  that exceed Vercel's 1 GB / 15K file limits. A curated subset has been selected
  per .vercelignore entries. Need guidance on:
  1. Correct .vercelignore or .gitignore approach to exclude binary asset directories
     from Vercel's deployment file collection (vercel CLI deploy --prebuilt approach
     vs standard push approach)
  2. Whether 'vercel build' on the project repo (source mode) vs 'vercel deploy --prebuilt'
     (pre-built dist/ mode) is the right approach given binary asset volumes
  3. Vercel project creation and linkage steps for reincarnated-demo (separate from
     reincarnated-loadout which is already linked at prj_by2dUTmjoi532x14l6IWSgOIKGVg)
  4. .vercel/project.json setup for new demo project
  Reference: options paper at canonical/story/demo-vercel-deployment-asset-pipeline-options-2026-05-18.md
```

**If Matt approves Path 3 (Vercel Blob):**
```
Dispatch type: vercel:deployment-expert consultation
Scope: Migrate reincarnated-demo vendor assets to Vercel Blob; deploy app code only.
Context: Demo has ~3.27 GB of committed binary assets (game sprites). Strategy:
  upload vendor asset directories to Vercel Blob; update asset loading code to use
  Blob URLs via VITE_ASSET_BASE_URL env var; deploy app code separately.
Need guidance on:
  1. vercel blob upload bulk workflow for existing directory structure (~138K files in
     DireDungeon_Items_Loot/ alone)
  2. Maintaining URL path structure in Blob (so path substitution is simple)
  3. Cache-control headers for game sprite assets (long TTL; versioned by asset update)
  4. Env var wiring: VITE_ASSET_BASE_URL in vercel.json for production/preview/dev
  5. vercel:deployment-expert cost estimate for Pro Blob at ~3 GB stored + ~50 GB/month
     transfer (dev traffic)
  Reference: options paper at canonical/story/demo-vercel-deployment-asset-pipeline-options-2026-05-18.md
```

**Either path:** knight-rider should pre-stage one dispatch tonight (unfired); Matt selects which fires on morning.

---

*Authored 2026-05-18 overnight sprint. Star-lord sections complete (§§ 1.1-1.2, 1.4, 2, 3 architectural perspective, 4.1, 5). Drax sections pending (§§ 1.3, 3 code-touch complexity, 4.2). Hard no: no deployment commit tonight. Options paper only.*
