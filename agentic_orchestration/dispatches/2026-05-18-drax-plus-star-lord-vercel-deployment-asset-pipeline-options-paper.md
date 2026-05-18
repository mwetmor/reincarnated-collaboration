# 2026-05-18 — drax + star-lord — Vercel demo deployment asset-pipeline options paper (scoping only; § 2.4)

**Authority:** Overnight sprint invocation `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` § 2.4 deliverable 14; pre-authorization matrix § 6 row 6.
**Type:** Pattern B; ~2-3 hours; **DRAX + STAR-LORD JOINT.**
**Status:** 🟢 **ACTIVE — parallelizable with all other tracks. SCOPING ONLY. No deployment commit tonight.**
**Tag intent:** none (canonical-story doc).

---

## Why this is scope-only tonight

Per invocation § 2.4 and pre-authorization matrix § 6 row 17: actual Vercel deployment for demo is a **HARD NO** tonight. Three structural blockers (6.1GB build output > Vercel free tier; mobile P0 touch zones — now closed; no deployment scout has done this) make this a Matt-L3-on-morning decision, not an overnight commit.

Tonight's deliverable is a **written options paper** that lets Matt decide on morning which path to take. Tomorrow's dispatch fires the chosen path; tonight's paper is the input to that decision.

---

## Required reading

1. The full invocation (above) — § 2.4
2. Demo build configuration: `~/Games/reincarnated-demo/vite.config.ts`, `~/Games/reincarnated-demo/package.json`, `~/Games/reincarnated-demo/.gitignore`
3. Asset directories: `~/Games/reincarnated-demo/public/` and `~/Games/reincarnated-demo/assets/` (or wherever vendor packs land) — size measurement per-subdirectory
4. Audio packs (kmontesdev 2GB + PixelLoops staged) — Matt's manual download set
5. CraftPix dungeon tilesets (~1.1GB)
6. Loadout app deployment as comparison (already-deployed Vercel; what tier; what asset profile)
7. Vercel pricing docs (publicly available)

---

## Deliverable

A new canonical-story doc at `canonical/story/demo-vercel-deployment-asset-pipeline-options-2026-05-18.md`. Co-authored by drax + star-lord; structurally drax owns the demo-side technical reality (asset paths, code touch-points for CDN URL refactors, build config), star-lord owns the back-end/data-pipeline architectural perspective.

### Required content

**§ 1 — Current state.** Inventory:
- Total build output size (run `npm run build` and measure dist size; or estimate from public/ + assets/ inventory)
- Per-subdirectory size breakdown (audio packs, sprite tileset vendor packs, character spritesheets, UI icons, etc.)
- `.gitignore` exclusion list (what's ignored today; why)
- Asset-loading code paths (where the demo references assets — file:// vs URL pattern)

**§ 2 — Vercel tier constraints.** Free, Pro, Enterprise tiers. Build-output limits; bandwidth pricing; blob-storage pricing. Source: Vercel public docs as of 2026-05-18.

**§ 3 — Strategy options.** At minimum the 5 paths invocation § 2.4 names:

1. **Vercel Pro + bandwidth budget.** Ship everything; Pro tier; monitor bandwidth.
2. **Vercel + external CDN for vendor assets.** Vercel hosts app code; vendor assets fetch from S3 / Cloudflare R2 / similar; asset-loading code refactored to use CDN URLs.
3. **Vercel Blob Storage.** Use Vercel's native blob storage for vendor assets; pricing TBD; tight integration.
4. **Vendor-asset subset for deployment.** Ship a curated subset (1-2 substrates, 1-2 biome tilesets) sized to fit free/Pro tier; full library remains local for development. Demo-link showcases curated subset.
5. **Self-hosted deployment elsewhere.** Netlify, Cloudflare Pages, GitHub Pages (static-only); other.

For each path:
- **Cost** (one-time + monthly + bandwidth-dependent)
- **Complexity** (code changes required; deployment-config changes; ongoing maintenance burden)
- **Time-to-first-deploy** (rough estimate from "Matt approves on morning" to "demo URL live")
- **Maintenance burden** (asset refresh cadence, CDN cache invalidation, etc.)
- **Tradeoffs** (what's gained, what's compromised)

**§ 4 — Recommendation.** Drax + star-lord pick a preferred path. State why. State the second-best alternative and why it's runner-up. Matt makes the L3 call on morning; this is your evidence-grounded recommendation.

**§ 5 — Vercel:deployment-expert consultation pre-stage.** Per invocation deliverable 15, knight-rider drafts a follow-on dispatch for the morning. This section describes what that dispatch would contain so knight-rider can pre-stage it. Do not author the dispatch yourselves; just describe its shape so knight-rider can draft.

---

## Methodology

1. **Measurements, not guesses.** Run `du -sh` per directory; check `package.json` for vendor pack sources; check `.gitignore` for what's excluded.
2. **Vercel docs are authoritative on pricing.** Cite the docs you read; do not estimate from memory.
3. **Cost includes time.** Implementation hours are a cost; ongoing maintenance hours are a cost. Bandwidth pricing is a cost. List them all.
4. **The recommendation is allowed to be opinionated.** "Path 4 (vendor subset) is the right Phase-1 move" is the right kind of recommendation. Hedging recommendations are not useful to Matt.

---

## Out of scope

- Any deployment commit or attempt tonight (HARD NO § 6 row 17)
- Loadout app deployment changes (loadout has stable deployment; do not touch its pipeline)
- Asset-pipeline implementation work (this is scoping; implementation lands after Matt L3)
- New asset curation (elrond's domain; orthogonal to deployment strategy)
- vercel:deployment-expert agent commission firing (pre-stage only; knight-rider drafts unfired dispatch)

## HARD NOs (per invocation § 6)

- No `git push --force`
- No actual Vercel deploy of demo
- No vendor acquisitions
- No CLAUDE.md or AGENTS.md modifications

## Completion handoff

1. Append completion record to this dispatch (both authors note completion)
2. Hive-log STATE entry (§ 14.1.1 PRE-SIGNAL discipline)
3. Options paper lands at `canonical/story/demo-vercel-deployment-asset-pipeline-options-2026-05-18.md`
4. Knight-rider drafts the unfired vercel:deployment-expert dispatch based on the paper's § 5
5. Matt reads on morning + L3-decides which path
6. Tomorrow's dispatch fires the chosen path

---

## Coordination note

This is a joint dispatch — both authors must contribute. Suggested split:
- **Drax-led:** §§ 1 (current state), 3 (per-path complexity from demo-code-touch perspective), portions of 4 (recommendation)
- **Star-lord-led:** §§ 2 (tier constraints), 3 (per-path architectural perspective on asset-pipeline patterns), 5 (consultation pre-stage shape), portions of 4 (recommendation)

Both authors agree on § 4 recommendation. If they disagree, surface as L2 to knight-rider in hive log; knight-rider routes or queues for morning Matt L3.

---

*Dispatched 2026-05-18 evening by knight-rider per overnight sprint invocation § 2.4 (drax + star-lord joint scoping). Single-night sprint cadence.*
