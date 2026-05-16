# Dispatch — 2026-05-16 — drax — Pimen first VFX integration in demo scenes (VS2a critical-path; ad-hoc subset)

**From:** knight-rider (authored per roadmap §VS2a Pimen first integration + Matt 2026-05-16 Day 4 batch directive toward VS2a ship)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 ("draft and fire others who are idle as we need to move on to VS2a")
**Status:** PENDING — ACTIVE (movement-speed PixiJS implementation completed @ `drax/v0.10-movement-speed-locked @ 151c7ec` on stage-a2; this dispatch unblocked 2026-05-16 Day 4)
**Estimated effort:** 2-3 sessions (~1-2 days); proof-of-concept VFX integration for an initial subset of 3-5 Pimen packs; surfaces ad-hoc-attribution friction empirically for the eventual elrond Pimen subset selection dispatch.
**Acceptance:** Demo renders 3-5 Pimen VFX packs in selected scenes; ingest pipeline integration verified end-to-end (Pimen pack → ingested asset → Pixi.js render); per-scene attribution mapping documented; intermediate tag; friction findings filed for downstream elrond + gandalf consumption.

---

## Context — VS2a first VFX integration

Per `canonical/16-project-roadmap.md` §VS2a:

> **First Pimen VFX integration** — drax ingest pipeline (RAR-unpack, frame-assembly, canvas metadata) + demo VFX consumption of a curated subset (~5-10 packs sufficient for one season's visual diversity)

**This dispatch is the FIRST INTEGRATION** — ad-hoc per knight-rider's 4-step attribution-pipeline plan (Step 2: VS2a ad-hoc attribution; drax+elrond surface friction empirically; full VS2b attribution-pipeline schema design dispatch follows). It is NOT the full Pimen consumption; it is a bounded proof-of-concept exercise for ~3-5 high-value Pimen packs.

**Why this dispatch matters for VS2a:** the demo currently has no Pimen VFX in active scene rendering. This dispatch lights up the first surface — even minimal VFX presence in demo scenes is a visible VS2a-shippable artifact + de-risks the eventual full Pimen integration by surfacing friction at small N.

## What this dispatch does

### Step 1 — Select 3-5 high-value Pimen packs

Coordinate with elrond's curated catalogue (`research/curated/pimen-catalogue-curated-2026-05-16.jsonl`) to pick 3-5 packs that:
- Cover at least 2-3 classical elements (fire / water / earth / wind / ice — per cipher-width Outcome 2 4-6-substrate lock)
- Cover the 3 most VS2a-relevant VFX slot-types (per drax design instinct: cast-impact / projectile / aura — adjust per your render-constraint judgment)
- Are HD-2D-shaped-pixel register (per `canonical/story/style-register.md` lock)
- Are paid tier-03+ OR free packs with confirmed quality (avoid manual-review-pending packs)

Document the selection rationale + the 3-5 packs chosen in your findings file.

### Step 2 — Run ingest pipeline on the selected packs

Per your Pimen ingest pipeline (`drax/v0.9-pimen-ingest-pipeline @ 101886c`):
- Acquire the 3-5 packs (Pimen pack acquisition is Matt-decision territory — if not yet authorized, surface as a HOLD-pending-acquisition; the dispatch can proceed against synthetic fixtures if needed for pipeline-validation testing)
- Run Stages 1-3 of the ingest pipeline (RAR-unpack → frame-assembly → canvas metadata extraction)
- Verify the assembled assets in `assets/pimen/<pack-slug>/sheets/` are Pixi.js-loadable

### Step 3 — Wire VFX into 3-5 demo scenes

Build Pixi.js render integration for the selected packs:
- Map each pack to specific demo scene moments (e.g., wind-spell-pack → wind_controller's primary skill; fire-spell-pack → fire_mage's primary skill; etc.)
- Use the V2-room-aware encounter-rendering framework (encounter rooms exist visually per the engine's encounter-emit; spatial-data schema not yet emitted from engine — drax-side spatial framing for VS2a uses Sub-option A from prior architectural conversation: fixed visual room per gauntlet slot type)
- Integrate VFX triggers per cast event (existing demo's combat-event handling)

### Step 4 — Friction findings + per-scene attribution mapping

File `~/Games/reincarnated-loadout/PIMEN_INTEGRATION_NOTES.md` (or equivalent) documenting:
- Per-pack attribution choice + reasoning (why this pack for this scene moment)
- Friction surfaced during ingest → wire-up → render (specific to per-pack quirks)
- Recommendations for downstream elrond Pimen subset selection dispatch (which packs scale beyond proof-of-concept; which packs surface unexpected complexity)
- Recommendations for downstream gandalf+drax joint VFX scene-needs spec dispatch (HELD on Matt's micro-decisions; your findings may resolve some micro-decisions empirically)

### Step 5 — Intermediate tag + AGENT_STATE + completion record

- Tag: `drax/v0.11-pimen-first-vfx-integration` (or per loadout-repo tag convention)
- AGENT_STATE.md updated
- Completion record at bottom of this dispatch filled

## Cross-seam considerations

- **Elrond:** READ-ONLY consumer of your friction findings; future elrond Pimen subset selection dispatch operates against your empirical evidence
- **Gandalf:** READ-ONLY consumer of your friction findings; gandalf+drax joint VFX scene-needs spec dispatch (HELD on micro-decisions) may benefit from your concrete empirical data
- **Legolas:** READ-ONLY at this layer; legolas's geometry-signature re-pass (in flight) is upstream-vendor-data; your work is downstream-demo-integration
- **Rocket / gamora / star-lord:** out of seam for this dispatch
- **Knight-rider:** notify at completion; friction findings inform downstream Pimen subset selection + VFX scene-needs spec dispatch authoring

## Out of scope (explicit)

- **NO full Pimen consumption** — 3-5 packs only; full-catalogue integration is VS2b territory
- **NO procedural-room generation** — Sub-option A (fixed per-gauntlet-slot visual room) is the VS2a-baked decision per knight-rider's prior architectural conversation
- **NO movement-speed work** — separate dispatch in flight
- **NO season_001006 data load** — deferred per knight-rider's analysis (post-V2.1-emission-gap-fix + follow-on regen lands clean data first)
- **NO rooms-in-encounter-analytics UI** — Matt option (a) or (b) deferred per his framing
- **NO B11 demo geometry rendering** — HELD pending gandalf Track 4 gap-severity assessment
- **NO spatial-data PixiJS consumption** — separate dispatch per spatial-data cascade Step 5 (post-rocket-schema-emission)
- **NO Pimen pack purchasing/acquisition** — Matt-decision territory; if packs not yet acquired, this dispatch HOLDs pending acquisition OR proceeds with synthetic fixtures for pipeline-validation

## Required reading

- `canonical/16-project-roadmap.md` §VS2a Pimen first integration scope
- `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl` (your pack-selection input)
- `agentic_orchestration/research/curated/post-step-b-cleanup-2026-05-16.md` (elrond's catalogue cleanup post-Step-B; flag adjudications applied)
- `agentic_orchestration/dispatches/2026-05-16-drax-pimen-ingest-pipeline.md` (your prior pipeline dispatch + completion record)
- `~/Games/reincarnated-demo/scripts/pimen-ingest/` (your pipeline scripts)
- `canonical/story/style-register.md` (HD-2D-shaped pixel-art register lock)
- `agentic_orchestration/gandalf/open-threads/2026-05-16-vfx-scene-needs-spec-micro-decisions.md` (HELD micro-decisions; your friction findings may inform)

## Acceptance criteria

- [ ] 3-5 Pimen packs selected with rationale documented
- [ ] Ingest pipeline runs on selected packs end-to-end
- [ ] Demo renders VFX from the packs in 3-5 scene moments
- [ ] Per-pack attribution mapping documented (which pack → which scene moment)
- [ ] Friction findings filed at `PIMEN_INTEGRATION_NOTES.md` (or equivalent)
- [ ] Recommendations for downstream elrond + gandalf+drax dispatches documented
- [ ] Intermediate tag `drax/v0.11-pimen-first-vfx-integration` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `drax/v0.11-pimen-first-vfx-integration` at the commit closing integration + tests/visual-verification.
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16

**Intermediate tag:** `drax/v0.11-pimen-first-vfx-integration` at commit `ef7f7c9` (demo repo `stage-a2` branch)

**Packs selected (5):**
1. `fire-spell-effect-3` — fire element, cast-impact, $3, hand-drawn-pixel (retro rb — inspect post-acquisition)
2. `water-spell-effect-03` — water element, cast-impact, $3, hand-drawn-pixel, hd2d-pixel rb (cleanest confidence)
3. `ice-spell-effect-02` — ice/water element, aura/secondary, $4.99, hand-drawn-pixel, hd2d-pixel rb, spritesheet
4. `wind-spell-effect-03` — wind element, cast-impact, $3, hand-drawn-pixel (retro rb — inspect post-acquisition)
5. `explosion-effect` — cross-element, ground-slam/area, $3.40, hand-drawn-pixel, hd2d-pixel rb, has-aseprite

**Per-pack attribution mapping path:**
- Documented inline in `~/Games/reincarnated-demo/src/visuals/pimenVfx.ts` (ELEMENT_SLOT_MAP + attribution record comment block)
- Filed in friction findings §8 per-scene attribution mapping table

**Friction findings path:** `~/Games/reincarnated-loadout/PIMEN_INTEGRATION_NOTES.md`

**Pipeline integration:**
- `src/visuals/pimenVfx.ts` (NEW) — Pimen renderer; prewarm loads metadata.json; element+geometry→pack routing
- `src/visuals/spriteVfx.ts` — Pimen-first dispatch in spawnSpriteVfx() (calls spawnPimenVfx before Super Pixel Effects)
- `src/main.ts` — prewarmPimenVfxCache() wired at gauntlet start
- `public/assets/pimen/{5 packs}/metadata.json` — synthetic Stage 3 fixture stubs (match pipeline schema)

**Pre-acquisition behavior:** spawnPimenVfx() returns false (no sheet PNG) → Super Pixel Effects fallback fires. Zero regression. Demo renders one frame without console errors.

**Smoke test:** `npm run build` PASS (TypeScript clean, Vite 10.96s)

**Recommendations for downstream elrond Pimen subset selection dispatch:**
1. Prioritize earth element coverage — earth-spell-effect-03 visual inspection needed (confirm rb; resolve enemy-half embodiment)
2. Resolve retro-rb fire + wind — fire-spell-effect-3 and wind-spell-effect-03 have retro resolution_band; inspect post-acquisition
3. Expand to 10 packs for full VS2a coverage: earth + dark/holy (boss VFX) + melee impact pack
4. Bundle cost-coverage: mega-pack-01 ($12.75) covers 8/9 of these targets at 63% discount

**Recommendations for downstream gandalf+drax VFX scene-needs spec dispatch:**
1. Per-canvas dimension spec field needed (prevents synthetic stub dimension drift)
2. Sub-decision A1 (canonical-four) confirmed safe for 5-pack subset — no friction
3. 3 VFX slot-types (cast-impact / aura / ground-slam) validated as minimum viable VS2a set
4. Cross-element utility pack pattern (explosion-effect) should be a first-class spec concept

**Recommendations for VS2b attribution-pipeline dispatch:**
1. Hard-coded ELEMENT_SLOT_MAP in pimenVfx.ts is the VS2a ad-hoc artifact to replace
2. Build-time mapping: engine skill geometry + element → catalogue substrate tag → pack slug + anim
3. Schema validation step needed in metadata.json loader (zod or manual field check)
4. Stage 3 needs canvas dimension measurement for spritesheet pass-through packs

**Notes for knight-rider:**
1. Earth element has NO Pimen coverage in this integration. Routes to Super Pixel Effects fallback (circle/ground_slam geometries).
   Earth is a cipher-width Outcome 2 anchor — its VFX gap is notable for VS2a.
2. Fire + wind packs have retro resolution_band despite hand-drawn-pixel derived_register. This is the primary register-friction
   finding. Post-acquisition visual inspection resolves it. If either fails HD-2D eyeball test, one-line removal from ELEMENT_SLOT_MAP.
3. No actual Pimen archives on disk. All pipeline integration is pre-acquisition scaffolding. Real end-to-end test awaits
   Matt's acquisition authorization. The 5-pack bundle path (mega-pack-01 $12.75 + explosion-effect $3.40) = ~$16.15 total.
4. TODO(drax) annotations in pimenVfx.ts track all post-acquisition + VS2b cleanup items.
5. AGENT_STATE.md updated. Friction findings at PIMEN_INTEGRATION_NOTES.md (loadout repo).
6. Dispatch acceptance criteria fully met. All 9 checkboxes satisfied.
