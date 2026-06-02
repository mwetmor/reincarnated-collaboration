# IA-3 Phase 4 V2 Iteration Close — drax

**Date:** 2026-06-01
**Author:** drax
**Authority:** Matt 2026-06-01 strategic reset + LOCK F (MVP-discipline) + LOCK G (autonomous Vercel preview)
**Workstream tag:** `IA-3-drax-V2-iteration`

---

## Integration verdict: SUCCESS

Season_000043 (V2 brine-theme) data loads in both reincarnated-loadout and
reincarnated-demo via existing components. No new UI components created. V1
season_000042 preserved intact. All acceptance criteria met.

---

## 1. reincarnated-loadout

**Data-loading approach:** Same Vite `import.meta.glob` static imports as V1 (existing
`useSeasonData.ts` glob patterns). Added `data/season_000043/` directory:

- `data/season_000043/manifest.json`: adapted from engine manifest.json; `elements` stub
  (canonical-four mapped from cosmological_vocabulary slot_fills: ignition/suffusion/
  bulwark/displacement -> fire/water/earth/wind); `seasonal_elements` built from
  slot_fills with `impact -> physical`; `cosmological_vocabulary` preserved.
- `data/season_000043/classes/class_0001.json` through `class_0005.json`: 5 playable
  V2 classes copied directly (Saltfire Hermit / Brine-Soaked Warden / Salt-Crusted
  Tide Warden / Salt Flat Drifter / Evaporant Stormwright). class_0006-0011 excluded
  (same is_act_boss:null MVP mitigation as V1 — see Bug 1 below).
- `data/season_000043/gear_pool.json`: adapted from `gear_pool_staged.json`; `id` ->
  `gear_id` rename; `fit_energy_type` / `fit_range_profile` / `fit_role_orientation`
  extracted from `class_fit_profile` nested dict (V2 has real fit data; V1 used empty
  dicts because V1 gear also lacked flat fit_* fields at engine level — both V1 and V2
  engine gear use class_fit_profile; V2 adaptation extracts correctly).

**Zero code changes:** Existing `useSeasonData.ts` glob picks up new directory automatically.
season_000043 appears in `selectableSeasons` on Loadout and Sample pages alongside season_000042.

**Build:** `tsc -b && vite build` — CLEAN (0 TS errors; 1063 modules; +7 vs V1 1056).

**Commit:** `91dc05d` — `drax: IA-3 P4 — season_000043 V2 data-loading layer (reincarnated-loadout)`

---

## 2. reincarnated-demo

**Data-loading approach:** Same fetch-based loader as V1 (`src/data/loader.ts`).
Added `public/seasons/season_000043/`:

- `metadata.json`: adapted from engine manifest; same SeasonMetadata shape as V1;
  elements + seasonal_elements stub from slot_fills; brine theme.
- `classes.json`: merged array of 5 V2 playable classes; `is_act_boss: false` and
  `carried_gear: null` added additively; `balance_metadata.actual_winrate` and
  `converged` backfilled from `convergence_report.endgame_L50`.
- `monsters.json`: merged array of all 44 V2 monsters.
- `gear_pool.json`: adapted from `gear_pool_staged.json`; `id` -> `gear_id`; fit_*
  extracted from `class_fit_profile`.
- `gauntlet_recipe.json`: copied directly (format matches GauntletRecipe exactly).

**SEASON_IDS update:** `src/data/loader.ts` — added `'season_000043'` to `SEASON_IDS` array.

**Type extension (LOCK J § 1 additive):** NONE needed. All V2 geometry types (aura /
blink / chain_lightning / circle / dash_attack / ground_slam / ground_targeted_circle /
melee_strike / multi_projectile / self_buff / single_target / teleport / vortex_pull)
already present in `GeometryType` union from V1 P1 extension.

**Build:** `tsc --noEmit && vite build` — CLEAN (0 TS errors; 539 modules; +3 vs V1 536).

**Commit:** `803788c` — `drax: IA-3 P4 — season_000043 V2 data-loading layer (reincarnated-demo)`

---

## 3. V1-fix-deferral bug surface verification (§ 2.3)

### Bug 1 — Engine classes 0006-0011 emit `is_act_boss: null` not `true`

**V2 status: PERSISTS — same behavior.**

Verified: `season_000043/classes/class_0006.json` has `is_act_boss: null` and
`is_retired: null`. Engine sha is identical (cda99a5) for V1 and V2; no engine work
intervened. Mitigation applied at data-staging step (only class_0001-0005 staged).

TODO(drax): remove MVP class-staging workaround when engine ships is_act_boss correctly
on class_0006-0011.

### Bug 2 — `resolveElementDisplay` null-guard scope issue

**V2 status: PERSISTS — same engine behavior; same mitigation active.**

V2 engine manifest has `elements: null` (verified). Our adapted manifest provides
canonical-four elements stub so `resolveElementDisplay` does not hit the null path
at runtime. The underlying function still has no null-guard on `manifest.elements`
access. Bug persists in code; mitigation keeps it non-blocking.

TODO(drax): add null-guard to resolveElementDisplay for manifest.elements when engine
begins emitting elements:null consistently.

### Bug 3 — SeasonManifest type `elements` non-optional vs engine emits null

**V2 status: PERSISTS — same engine behavior; same mitigation active.**

`SeasonManifest.elements` is typed as `Record<string, ElementMapping>` (non-optional,
line 162 of `types.ts`). V2 engine manifest emits `elements: null`. Our adapted
manifest stubs the field so the build/runtime never sees null. Type mismatch between
engine output and loadout type definition persists; no TS error because the adapted
data is used, not the raw engine output.

Post-immediate-arc: star-lord/knight-rider should decide whether engine should emit
canonical-four elements or loadout should make `elements` optional (nullable).

---

## 4. fights.jsonl explicit exclusion

**fights.jsonl (47.8MB) — EXCLUDED.**

Per dispatch § 2.1 INFO and jack-ryan Gate-1 INFO item: `fights.jsonl` was not staged
in either reincarnated-loadout or reincarnated-demo data directories. Same as V1 P1
precedent (P1 close § 6 deferred at 41.8MB). V2 is 47.8MB. Exclusion is intentional:
the file is raw fight telemetry; the loadout has no current component to consume it;
the demo has no fight replay mechanism. If a future analytics ask surfaces fight-level
data, a sample-stream approach would be needed rather than bundling the full JSONL.

---

## 5. V1 vs V2 observations (brief)

**Thematic register shift:** V1 (forge) = industrial/metallurgical/arena-combat;
V2 (brine) = post-oceanic/salt-flat/climate-elegiac. Both substantively LLM-coalesced.

**Anchor narrative:** V2 anchor "The Salt Flats After the Sea" (water_places) vs V1
"The Bronze Bull Pit" (coliseums_and_arenas). V2 description "where the ocean used
to be; salt crust over an absence" is tonally quieter — absence and remnant vs
spectacle and violence.

**Class names (V1 vs V2):**
- V1: Pit-Flame Warden / Slag-Fist Ironclad / Quench-Mancer / Bellows Runner / Hammerfall Tyrant
- V2: Saltfire Hermit / Brine-Soaked Warden / Salt-Crusted Tide Warden / Salt Flat Drifter / Evaporant Stormwright

V2 names lean toward solitude and elemental erosion vs V1 forge-violence register.
Both visually distinguishable in the Loadout season selector.

**Validation parity:** Both V1 and V2 hit 49.33% trial defeat rate (vs 50% target);
0 convergence failures. Engine pipeline reproducible.

**Gear fit data:** V2 gear_pool has real `fit_energy_type` / `fit_range_profile` /
`fit_role_orientation` values (extracted from `class_fit_profile`), whereas V1 was
staged with empty dicts `{}`. This is a V2 data quality improvement — same GearPoolEntry
type, richer fit data. Worth noting for post-arc GearGrid rendering.

**Geometry types:** No new types in V2 vs V1. All 13 types already in union.

---

## 6. Auto-commit + deploy record

### reincarnated-loadout
- **Commit:** `91dc05d` — 7 files, 26105 insertions
- **Pushed:** `main -> origin/main` (75417f8..91dc05d)
- **Vercel preview URL:** https://reincarnated-loadout-3rll3kdbf-matthew-wetmore-s-projects.vercel.app
- **Vercel inspect:** https://vercel.com/matthew-wetmore-s-projects/reincarnated-loadout/E36ttKNRLBbHBDwzCbaWUGpypCWC
- **Vercel deploy state:** READY
- **Build:** 1063 modules; 0 TS errors; 3.02s build time

### reincarnated-demo
- **Commit:** `803788c` — 6 files, 30816 insertions
- **Pushed:** `main -> origin/main` (0e511c4..803788c)
- (Demo has no Vercel deploy; public/ fetch-based loader; season selector updated)

---

## 7. Notable observations for post-immediate-arc Pattern B

1. **Gear fit data improvement (V2):** V2 gear has real class_fit_profile values vs
   V1 empty dicts. The GearGrid component (loadout) could surface fit scores in
   post-arc Pattern B — the data is now richer without engine changes needed.

2. **cosmological_vocabulary.json pair rationales:** V2 `cosmological_vocabulary.json`
   has three pair rationales (pair_thermal_rationale / pair_position_rationale /
   pair_luminance_rationale) that the `CosmologyPairBlock` component already handles.
   Wiring V2 cosmological vocabulary to the existing Pitch page CosmologyPairBlock is
   a 1-file data load + existing component — a clean first Pattern B task.

3. **Both seasons now selectable:** Season selector in Loadout and Sample pages shows
   both season_000042 (The Bronze Bull Pit) and season_000043 (The Salt Flats After the
   Sea). V1 vs V2 side-by-side comparison is now possible in the preview deploy. This
   is the expected outcome for multi-season pattern validation.

4. **fights.jsonl V2 (47.8MB):** Larger than V1 (41.8MB). If fight replay or per-fight
   analytics is a Pattern B ask, a streaming/sampling approach is needed — not bundling.

5. **Bug 1 (is_act_boss) root cause:** Engine emits `is_act_boss: null` on ALL classes
   including playable ones; it is not emitted as `true` on gauntlet-opponent classes.
   The demo's `getPlayableClasses` filter uses `!c.is_act_boss` which correctly passes
   when `null` (since `!null === true`). The loadout class selector only needs the 5
   staged classes. But the field is not semantically useful as emitted. Pattern B raise
   to star-lord/rocket for engine fix or schema clarification.

---

## 8. Routing back to KR

IA-3 P4 V2 iteration SUCCESS. Season_000043 loads in both reincarnated-loadout (Vercel
preview READY) and reincarnated-demo (build clean; season selector updated). V1
season_000042 preserved. No new UI components. Three V1-fix-deferral bugs persist
in engine (not blocking; mitigated at data-staging). fights.jsonl excluded explicitly.

**IA-3 P4 SUCCESS — IA-3 CLOSED — proceed to strategic re-engagement Pattern B with Matt.**
