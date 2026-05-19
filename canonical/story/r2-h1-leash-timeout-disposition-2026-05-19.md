# R2 H1 Leash + Timeout Disposition — Third-Finding Structural Substrate Re-disposition

**Date:** 2026-05-19
**Author:** gandalf (story-and-design steward)
**Authority:** AUTONOMOUS L2-equivalent per protocol § 4.0 (Matt directive 2026-05-19; pre-approval-batch authority).
**Predecessor chain (three findings deep):**
1. `canonical/story/r2-h1-disposition-2026-05-19.md` — **Finding 1** (engine-rebuild v0.14): variance metric instrument-limited under name-heuristic 43/3/4; category-of-completion frame + F1 forward routing.
2. `canonical/story/r2-h1-recalibration-disposition-2026-05-19.md` — **Finding 2** (R2-RT v1 under explicit field): calibration over-rewards corrected-AOE cohort; HYBRID Option C two-knob recalibration; `vs2a/v0.13-r2-spatial-calibration-disposed` fired.
3. **Finding 3 (this disposition)**: post-recalibration smoke FAIL via mob leash mechanic + timeout-semantic interaction; structural substrate re-disposition required.

**Trigger:** gamora's R2 recalibration impl + 5-class smoke (`output/R2-recalibration-smoke-2026-05-19/smoke_report.md`; math note § 9 `design/working-agreement/R2-recalibration-math-2026-05-19.md`) — HYBRID Option C constants applied (SPATIAL_DAMAGE_SCALE=4.0; MOB_HP_DIFFICULTY_MULTIPLIER=1.5; L1 second-pass MOB_DAMAGE_SCALE=0.40 added); 4/5 classes still WR=1.000. Empirical trace: 11 mob hits in 120s vs expected ~686; player HP 98.8% at fight end. **Root cause: `leash_distance_m = 18m` (monster JSON default) vs spawn-to-player distance 20-32m → mobs never reach player.** This is scenario engagement geometry, not calibration.

---

## § 0 — TL;DR

**Chosen path: γ — Hybrid B + C disposition on engagement geometry, with explicit S1 regenerated catalogue as the gold-standard H1 ≥ 0.10 threshold validation bed.**

| Lever | Old | New | Magnitude |
|---|---|---|---|
| **Mob leash override** (NEW per-scenario field) | implicit JSON default 18m | **35m** for swarm spawns in `open_arena` + `chokepoint_corridor` | Preserves "approach across open arena" semantic; mobs pursue full 50m arena |
| **Timeout win condition** for `open_arena` + `chokepoint_corridor` | HP > 50% → win | **kills_only** (any mob alive at 120s → loss) | Semantic alignment with H1 intent (kill efficiency by geometry) |
| Player spawn y in `open_arena` | y=40 | y=40 (unchanged) | "Approach" scenario semantic preserved |
| Player spawn y in `chokepoint_corridor` | y=40 | y=40 (unchanged) | Bottleneck-approach semantic preserved |
| `boss_with_adds` win condition / spawns | unchanged | unchanged | § 3.4 forward-flag continues |

**Meta-pattern reading (three findings deep):** Each finding fixed one scaffolding layer of the spatial sub-gauntlet's test fixture; each fix unmasked the next layer down. Finding 1 was the *classifier* layer (name-heuristic). Finding 2 was the *calibration* layer (SPATIAL_DAMAGE_SCALE + MOB_HP). Finding 3 is the *engagement-geometry* layer (leash distance + timeout outcome). These three layers were each individually plausible at their authoring time but were jointly calibrated against each other's implicit assumptions; when any single layer is corrected, the next layer's scaffolding-implicit assumption becomes the binding constraint. **This is NOT a fourth instance of "calibration-against-instrument" (Drift-16 candidate); it is a NEW pattern: "scaffolding-coupled measurement degeneracy" (Drift-17 candidate) — when an instrument's correctness depends on multiple coupled scaffolding decisions, each implicit-calibrated against the others, fixing any one unmasks the next.**

**Tag firing:**
- `vs2a/v0.14-r2-leash-timeout-disposed` — **FIRES** on this disposition's commit (3rd-pass milestone).
- `vs2a/v0.2-r2-h1-revalidated` — **REPLACED** by `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` (diagnostic confirmation only) + `vs2a/v0.4-r2-h1-validated-on-S1-catalogue` (gold-standard threshold validation). See § 4 + § 5 for the two-stage validation gate.

**Sequencing:** Engagement-geometry fix fires NOW (gamora L1 implementation). R2-RT v3 fires on existing catalogue as **diagnostic confirmation** (engagement geometry is sound; signal direction preserved; partial H1 evidence). **Gold-standard H1 ≥ 0.10 threshold validation lives on the S1 regenerated catalogue.** S1 is in flight (rocket regen + gamora R1-sprint validation gate); S1 first-batch validation just completed (gamora R1 sprint v3 partition; baseline confirmed).

---

## § 1 — Decision criteria applied (what tipped me)

### § 1.1 — Pattern recognition: this is the third onion layer, not a recurrence

I considered framing this finding as another instance of "calibration-against-instrument" (Drift-16 candidate, surfaced in Finding 2's disposition). It is structurally similar in surface shape — a measurement instrument was over-tuned against an earlier scaffolding choice, and correcting the upstream layer unmasked downstream brittleness. But the **causal mechanism** differs:

- **Drift-16 pattern** (R1 Blocker 3 + R2 recalibration): test-fixture multiplier constants tuned against an under-classified instrument; instrument schema work corrects the instrument; multiplier constants now over- or under-reward; recalibration via multi-knob hybrid.
- **Drift-17 pattern (this finding)**: test-fixture has MULTIPLE coupled scaffolding decisions (timeout semantic, leash mechanic, spawn geometry, win condition) each implicit-calibrated against the others' assumptions; correcting the calibration layer reveals that the engagement-geometry layer's scaffolding (HP>50% timeout win path) was masking floor-dm class behavior across the whole calibration history.

The key difference: **Drift-16 is about a single multiplier knob fighting against a corrected schema; Drift-17 is about multiple scaffolding decisions in a measurement instrument that were never individually load-tested because the calibration layer above them was always wrong-in-the-other-direction.** Naming both is needed. Both will be filed in drift-audit.

### § 1.2 — Why Path γ (Hybrid B + C with S1 as gold-standard bed), not Path α (Option D iteration) or Path β (defer entirely)

I considered three paths honestly:

**Path α — Implement gamora's Option D (A+C); iterate; risk a fourth finding.** This is the "keep peeling the onion" path. Cost: 0.5-1 day to implement + ~2-3 hours smoke + ~30 min full 51-class re-run. Risk: a *fourth* finding emerges. The empirical evidence for this risk is real — Findings 1 and 2 each surfaced a finding that the prior disposition would have called "extremely unlikely" under its own forecasting framework. The forecasting framework is undercalibrated for an instrument this many scaffolding layers deep.

The strongest argument *for* α: the engagement-geometry bug is a *real* substrate-level issue that would corrupt R2-RT v3 measurements on ANY catalogue (existing OR S1-regenerated). It needs to be fixed regardless of which catalogue we test on. **Fixing it is not optional.**

**Path β — Category-of-completion reframe: defer the original H1 ≥ 0.10 threshold re-test entirely to S1 regenerated catalogue; capture the three findings as the substantive disposition.** This is the move v0.14 § 2.2 explicitly warned against — silently retiring the original threshold by perpetually deferring its measurement.

The strongest argument *for* β: S1 IS the next catalogue. R2-RT v3 on the existing 5-shipped-season catalogue measures a *frozen artifact* about to be replaced. WP-R2-A-2 already commits to re-validation after S1 partition shift. Why measure twice?

The argument *against* pure β: it leaves the engagement-geometry bug unfixed, which would corrupt the S1 measurement too. And it does precisely what v0.14 warned against — perpetual deferral by re-framing.

**Path γ — Fix the engagement geometry AND explicitly separate two validation surfaces.** This is the path I'm choosing. It honors both arguments:
- The engagement-geometry fix is **necessary substrate repair**, not iterative recalibration. The leash + timeout interaction is a real bug. Fixing it is fixing the *test instrument*, not chasing the *test outcome*. (This is the architectural surgery v0.14 § 2.2 *did not* warn against.)
- The H1 ≥ 0.10 threshold validation has TWO surfaces under path γ:
  - **Surface 1 (R2-RT v3 on existing catalogue):** diagnostic confirmation that the engagement-geometry fix produces non-degenerate WR distribution; signal direction preserved; partial H1 evidence. NOT the gold-standard threshold validation.
  - **Surface 2 (R2-RT v4 on S1 catalogue):** gold-standard H1 ≥ 0.10 threshold validation on the regenerated catalogue's spatial run. This is the *cleaner test bed* because (a) the catalogue's geometry partition will be R8-inversion-driven rather than legacy-baseline-driven; (b) kit-broken classes will be largely replaced with R8-inverted-functional classes; (c) the signal will be measured against the catalogue the project is actually shipping.

This is **not** a category-of-completion reframe. The original threshold remains the validation target. What changes is the catalogue on which it is measured — and that change is *required anyway* per WP-R2-A-2's commitment to re-validate after partition shift. The disposition makes the two-stage validation explicit so that:
- Surface 1's outcome (whatever it is) does NOT silently fire `vs2a/v0.2-r2-h1-revalidated`. That tag is REPLACED.
- Surface 2's outcome IS the canonical H1 ≥ 0.10 threshold validation.
- Both surfaces inherit the engagement-geometry fix; neither inherits a perpetual-deferral framing.

### § 1.3 — Why Option B (leash override) + Option C (kills-only timeout), NOT Option A (spawn-shift) + C

Among gamora's four surfaced options, I rejected Option A (move player spawn y=40→y=25) and chose Option B (per-scenario leash override 18→35m) instead. Design reasoning:

**Option A is a scenario-redesign, not a substrate repair.** The `open_arena` scenario is named after — and designed around — the spatial dynamic of "8 swarm mobs approaching from south across 50m of open space." This is a genre-canonical signal: D2 Bloody Foothills, PoE Twilight Strand, Last Epoch Imperial Era open zones, Grim Dawn Wightmire — all use *approach-across-open-space* as the foundational ARPG combat semantic. The 20-32m initial gap is the scenario's *meaning*. Compressing the player spawn to y=25 (5-17m initial gap) reduces the scenario to a "starting engaged" composition, indistinguishable in spatial-dynamic terms from the chokepoint scenario. Two of three scenarios collapse to similar spatial profiles. The H3 chokepoint-vs-arena delta signal is degraded.

**Option B preserves the approach-across-open-space semantic.** Mobs still spawn 20-32m from player. They still approach. They just *continue* approaching past the previous 18m leash boundary. The spatial-dynamic semantic of the scenario is unchanged; only the engagement-mechanic constraint (which was implicit-default, never scenario-tuned) is loosened. Per-scenario leash override is also the *correct architectural seam* — the monster JSON default is a per-monster-archetype property, not a per-scenario property; the spatial sub-gauntlet's scenarios are the right surface to set scenario-aware leash behavior.

**Option C is the cleanest semantic alignment.** The "HP > 50% timeout win" path was scaffolding behavior from earlier development when calibration was less precise; it served as a *safety valve* against runaway calibration. Under HYBRID Option C calibration, that safety valve is now actively corrupting the signal:
- A floor-dm class (dm=0.05) cannot kill swarm mobs in 120s under any plausible calibration; in genre-canonical terms, this is a class that *should lose this fight.* The HP>50% timeout-win path lets it win anyway via "didn't die in 120s."
- H1's intent is "geometry-aware kill efficiency by class." A floor-dm class winning by survival is not a geometry-aware-kill-efficiency signal; it is a survival-via-mob-engagement-failure artifact.
- Kills-only timeout aligns the open_arena and chokepoint_corridor scenarios with what H1 was designed to measure.

**Why both B + C, not B alone or C alone?**

B alone (35m leash, HP>50% timeout still): mobs reach player; mob DPS damages player; player at floor dm may still survive 120s with HP > 50% via the recalibrated mob HP being so high that mobs can't be killed AND the recalibrated player armor being preserved (0.85 reduces damage substantially). Floor-dm class still wins on survival. Signal still degraded.

C alone (HP>50% removed, 18m leash retained): mobs still oscillate; player still takes ~11 hits in 120s; player HP is still ~98.8% at 120s; under kills-only semantic, player has not killed all mobs → LOSS. But mob HP-pool calibration was tuned assuming mobs could be engaged; with leash bypass, *no* class can kill all 8 mobs in 120s, and the entire scenario collapses to WR=0 across all classes. Different degeneracy mode, same fail outcome.

**Both B + C are needed.** B repairs the engagement-geometry; C aligns the win-condition semantic; together they produce the non-degenerate WR surface that H1 was designed to measure.

### § 1.4 — Substrate-identity continuity (third-finding-deep)

The substrate-identity declarations from v0.13/v0.14/v0.2-RT/v0.13-r2-spatial-calibration stand UNCHANGED. The R2 spatial sub-gauntlet remains:
- A 2D position-and-geometry-aware fight simulator
- Three scenarios (open_arena 50×50, chokepoint_corridor 10×50, boss_with_adds 30×30)
- Geometry resolution remains (3-path resolver, F1-corrected)
- Telemetry surface remains (`spatial_fight_results` table, 20 fields)
- H2 and H3 directional readings remain preserved (boss harder than swarm; chokepoint favors line/cone)

What changes:
- **Engagement-geometry layer**: per-scenario leash override (NEW field on SpawnSpec or scenario), kills-only timeout for open_arena + chokepoint (semantic shift on win condition).
- **Validation surfaces**: two-stage validation (existing-catalogue diagnostic + S1-catalogue gold-standard).

This is the third semantic shift in the R2 series (after F1 instrument correction and HYBRID Option C calibration). Discipline #12 citation required in implementation commit.

### § 1.5 — Discipline #12 framing (cumulative)

The R-series semantic-shift cadence:
- **R1 Disposition 1**: what "win" means for boss/mini-boss tier (kills-only vs HP%).
- **R1 Disposition 3**: what the gauntlet's calibration represents (genre-mid-tier vs anomalously-hostile).
- **R2 v0.14 disposition**: what the variance metric's PASS criterion represents under heuristic instrument (category-of-completion).
- **R2 recalibration**: what the spatial sub-gauntlet calibration represents under corrected instrument (re-honored AOE potential + restored mob durability).
- **R2 leash + timeout (this disposition)**: what the open_arena + chokepoint scenarios MEASURE (geometry-aware kill efficiency, not timeout survival; full-arena engagement, not leash-bypass artifact).

Five semantic shifts in the R-series across two days. Each was load-bearing. **Cumulative cadence is itself signal that the R-series workstream sits at the intersection of more scaffolding decisions than is typical for a single workstream.** This is captured in the Drift-17 entry below.

---

## § 2 — Implementation shape

### § 2.1 — Constants + per-scenario fields (gamora implements)

| Change | File | Site | Note |
|---|---|---|---|
| Add per-scenario leash override on SpawnSpec OR ArenaScenario | `simulation/spatial_gauntlet/arena.py` | SpawnSpec or ArenaScenario class | Add optional field `leash_distance_override_m: float \| None`. When set, overrides the monster JSON `leash_distance_m` default during fight construction. SCENARIO_OPEN_ARENA + SCENARIO_CHOKEPOINT set this to **35.0** for swarm spawns; SCENARIO_BOSS_WITH_ADDS leaves it None (boss + adds keep their JSON defaults). |
| Apply leash override in `run_spatial_fight()` | `simulation/spatial_gauntlet/spatial_engine.py` | mob-entity construction site | When constructing mob entity from SpawnSpec + monster JSON, prefer `spawn.leash_distance_override_m` if set; else use monster JSON `leash_distance_m`. Documented in docstring + math note § 10 (NEW). |
| Switch win condition outcome semantic for `open_arena` + `chokepoint_corridor` | `simulation/spatial_gauntlet/spatial_engine.py` | timeout-outcome resolution site | Current behavior: if `all_mobs_killed` win condition AND timeout reached AND player HP > 50%, fight result = WON (player). New behavior: if `all_mobs_killed` win condition AND timeout reached AND any mob alive, fight result = LOST (player). HP>50% timeout-survival path REMOVED for these two scenarios. Boss_with_adds win condition `boss_killed` retains its existing semantic. |
| Update WARNING log for floor-saturation | `spatial_engine.py` | post-fight result emission | Pattern P7 fail-loud discipline: if post-fix any scenario produces WR ≤ 0.05 for ≥ 80% of classes in smoke, log WARNING citing the engagement-geometry constants — surfaces second-pass tightening need symmetric to the existing ceiling-saturation WARNING. |
| Math note authoring (extension) | `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md` § 10 (NEW) | extend existing math note | Document the engagement-geometry fix walkthrough: leash 35m enables full-arena pursuit; kills-only timeout removes survival-win path; expected WR distribution at sample dm × geometry-type values. Discipline #1. |
| MIGRATION.md entry | `simulation/MIGRATION.md` | append after R1-recalibration + R2-recalibration entries | Document the two engagement-geometry changes (leash override field; timeout semantic change for two scenarios), application boundary (boss_with_adds untouched), precedent disposition cited. ADR-004 compliance. |

### § 2.2 — Why these specific magnitudes

**Leash override 18m → 35m for open_arena + chokepoint:** The 50×50 open arena has 50m of N-S travel; the chokepoint corridor has 50m of N-S travel. A 35m leash distance is sufficient for mobs to pursue from y=8 (mob spawn) to y=43 (5m short of player at y=40 in open_arena) — they reach engagement range across the full arena. The leash boundary remains a *mechanic* (mobs won't pursue infinitely; if player kites to extreme range they de-aggro), but the boundary is set to match the scenario's spatial scale rather than the monster JSON default that was authored for an unspecified-scale demo combat. Boss-with-adds untouched (30×30 arena; boss and adds keep their JSON-default leash; spatial composition there is about flanking, not pursuit-distance).

**Kills-only timeout for open_arena + chokepoint:** This restores the *test-instrument semantic* that H1 was designed against. The HP>50% timeout-survival path was scaffolding from earlier development; the disposition removes it. Boss_with_adds keeps its boss-killed win condition (untouched; § 3.4 forward-flag).

**Why not adjust mob count or arena size?** Those are scenario-design changes that would shift what each scenario *means*. The leash + timeout fix is a *substrate repair* — it restores the scenario's measurement-instrument fidelity to the spatial-dynamic semantic the scenario already commits to.

### § 2.3 — Smoke-test before full re-run (Discipline #17)

Before R2-RT v3 (existing catalogue) or R2-RT v4 (S1 catalogue), gamora executes a **5-class smoke** under the engagement-geometry fix:

- Same 5-class sample as the prior recalibration smoke (class_0016 line; class_0020 + class_0006 circle; class_0019 + class_0035 point).
- Run open_arena + chokepoint (boss_with_adds excluded; § 3.4 forward-flag).
- Smoke PASS criteria (same as recalibration smoke):
  - At least 2 of 5 classes produce 0.10 ≤ WR ≤ 0.90 in open_arena (non-degenerate variance surface confirmed)
  - The 2 circle-dominant classes show higher WR than the 2 point-dominant classes (signal direction preserved)
  - The line-dominant class shows higher chokepoint-vs-arena delta than the other classes (H3 mechanism preserved)
- L1 gamora authority on second-pass tightening within disposition framework (per R1 Blocker 3 § 10.1 precedent):
  - If WR floor-saturates (≥ 80% at WR ≤ 0.05): reduce MOB_HP_DIFFICULTY_MULTIPLIER 1.5 → 1.25 OR reduce MOB_DAMAGE_SCALE 0.40 → 0.30
  - If WR ceiling-saturates (≥ 80% at WR ≥ 0.95): keep prior recalibration tightening framework
  - Do NOT escalate to gandalf for incremental tightening within this framework
- **Escalation trigger:** if a FOURTH structural finding emerges (a substrate issue beyond calibration constants — like leash + timeout was), gamora escalates STATE + REQUEST to gandalf. Pre-commit: I do not expect a fourth substrate finding under this fix. The engagement-geometry layer is the layer the smoke trace empirically identified; there is no deeper layer that the recalibration's exposure has not already named.

---

## § 3 — Substrate-identity continuity (no kind-of-thing revision)

The substrate-identity declarations from v0.13/v0.14/v0.2-RT/v0.13-r2-spatial-calibration stand UNCHANGED. The R2 spatial sub-gauntlet remains:

- A 2D position-and-geometry-aware fight simulator (Arena + ChokeZone + SpawnSpec)
- Three scenarios (open_arena 50×50; chokepoint 10×50 with bottleneck; boss_with_adds 30×30)
- Geometry resolution remains (3-path resolver; F1-corrected explicit field; 0% heuristic_fallback)
- Telemetry surface remains (`spatial_fight_results` table; 20 fields)
- H2 directional reading remains valid (boss harder than swarm; boss-tier untouched)
- H3 directional reading remains valid (chokepoint favors line/cone via spatial geometry; the engagement-geometry fix RESTORES the measurable surface)

The engagement-geometry fix is a **scenario substrate-mechanic repair**, not a substrate redesign. The "kind of thing" R2 is remains exactly what v0.13/v0.14 committed.

### § 3.4 — Spatial boss recalibration — forward-flag CONTINUES (unchanged)

The R2 H1 disposition § 3.4 forward-flagged spatial boss calibration; the recalibration disposition § 3.4 continued the flag. This disposition continues the same:

- `boss_with_adds` scenario continues to produce WR = 0.000 across all 51 classes (catalogue-kit-broken-at-boss-tier finding; cross-references R1 Blocker 3 catalogue-kit finding)
- This disposition does NOT modify boss HP, boss armor, boss leash, boss timeout outcome, or PLAYER_ARMOR_FACTOR_VS_BOSS
- The engagement-geometry fix applies ONLY to open_arena + chokepoint_corridor (standard-tier swarm spawns)
- Post-S1 (kit-redesign-regen lands), if spatial boss WR remains 0.000 despite repaired kits, a spatial-specific boss recalibration follows in VS2b — that is a separate disposition, not in this scope

---

## § 4 — Sequencing

### § 4.1 — Engagement-geometry fix fires NOW

Independent of S1 sequencing. The fix is a substrate-instrument repair; it is *required* for any future R2-RT measurement to be sound regardless of which catalogue is being measured.

- Gamora implements per § 2.1 (single-day effort).
- 5-class smoke confirms non-degenerate WR surface.
- Knight-rider sequences R2-RT v3 (existing-catalogue diagnostic) after smoke PASS.

### § 4.2 — Two-stage validation gate

**Stage 1 — R2-RT v3 on existing 5-shipped-season catalogue (diagnostic confirmation):**
- Run full 51-class × 3 scenarios × 30 fights under the engagement-geometry fix.
- Measure H1 variance, H2 boss-delta detection, H3 chokepoint-vs-arena gap.
- **Stage 1 outcome semantics:**
  - **H1 ≥ 0.10:** the existing-catalogue's geometry partition (41.2% circle / 3.9% line / 54.9% point) is sufficient to measure variance ≥ 0.10 under the engagement-geometry fix. This is *partial* H1 evidence — strong directional confirmation, but on a catalogue that's about to be replaced by S1.
  - **H1 < 0.10:** the existing-catalogue's geometric diversity is too low for variance to reach threshold even under corrected substrate. This is a *catalogue-diversity finding* (2 line classes is anomalously few; the 41/4/55 partition is on the small-N edge for variance). NOT a substrate failure; surfaces as routing-to-S1 prediction (S1's R8-inversion regen is likely to shift geometry distribution toward more balanced partition; that shift becomes the test).
  - In EITHER case, Stage 1 outcome is *diagnostic only*. It does NOT fire `vs2a/v0.2-r2-h1-revalidated` (that tag is REPLACED — see § 5).

**Stage 2 — R2-RT v4 on S1 regenerated catalogue (gold-standard threshold validation):**
- After S1 first-batch validation gate PASSES (gamora's R1 sprint partition baseline confirmed; rocket S1 regen completes for one season; gandalf cohesion-judges; gamora R1-sprints; PASS criteria met) and S1 completes the 4 remaining seasons.
- Re-run R2-RT under the engagement-geometry fix + recalibrated constants + R8-inversion-regenerated catalogue.
- **Stage 2 outcome semantics:**
  - **H1 ≥ 0.10:** gold-standard threshold validated. Fire `vs2a/v0.4-r2-h1-validated-on-S1-catalogue`. Original threshold preserved end-to-end across three findings.
  - **H1 < 0.10 on S1 catalogue:** this would be a FOURTH-finding case requiring gandalf re-disposition. Forecast: **medium-low** probability. S1 first-batch baseline (gamora R1 sprint v3) shows the existing catalogue is 0/51 boss kills and 4/51 mini-boss kills; the R8-inversion has empirically shown 20% boss_kr ≥ 0.10 vs 0% in shipped (R8 A/B 3-season). The geometry partition under R8-inversion may shift in either direction (more balanced or less); the rocket-pre-work parameterization audit confirms tier assignment works against any emergent shape. If H1 fails on S1 catalogue, the deeper finding is *catalogue geometric diversity is the binding constraint, full-stop* — which routes to a generation-side disposition (rocket + gandalf) on per-class geometry-type targeting in the R8-inversion pipeline.

### § 4.3 — Does S1 regen pre-empt this disposition?

**No.** Two reasons:
- The engagement-geometry fix is required regardless of which catalogue is measured. Without the fix, R2-RT v4 on S1 catalogue would have the same leash + timeout bug. The fix is *substrate repair*, independent of catalogue.
- Stage 1 (existing-catalogue diagnostic) is a low-cost validation that the substrate fix produces a non-degenerate surface. ~30 min full 51-class run (post-smoke). It surfaces engagement-geometry-fix correctness *without* coupling to S1 timeline.

However, **knight-rider has discretion on Stage 1 timing.** If Stage 1 would compete with S1 for sequencing attention, knight-rider may defer Stage 1 to after S1 first-batch lands (so Stage 1 + Stage 2 fire in close sequence on the new catalogue). The disposition does not pre-bias this — gamora and knight-rider sequence per operational ordering.

### § 4.4 — Dispatch closure routing

Gamora's existing R2 recalibration impl dispatch (`agentic_orchestration/dispatches/2026-05-19-gamora-vs2a-R2-recalibration-impl.md`) is CLOSED by this disposition (completion record appended; route opened by gamora's REQUEST entry now satisfied). Knight-rider drafts follow-on dispatch:
- `agentic_orchestration/dispatches/2026-05-19-gamora-vs2a-R2-leash-timeout-impl.md`
- Scope: implement engagement-geometry fix per § 2.1 + 5-class smoke + Stage 1 R2-RT v3 (existing catalogue) + tag-fire on diagnostic confirmation
- Authority: AUTONOMOUS L1 gamora within disposition framework

---

## § 5 — Validation gate

### § 5.1 — Tests (Stage 1 + Stage 2)

Both stages re-run all three hypothesis tests (identical to R2 production sprint methodology):

- **H1 — Geometry-type WR divergence:** variance ≥ 0.10 across three geometry-type means. **Threshold preserved (third disposition in a row that does not retire the threshold).**
- **H2 — Boss-with-adds detection sanity:** ≥ 30% of classes show ≥ 10pp WR delta between open_arena and boss_with_adds. Expected PASS preserved (standard-tier WR distribution non-degenerate; boss WR remains 0 → delta is meaningfully measurable).
- **H3 — Chokepoint testability sanity:** chokepoint-vs-arena WR delta gap ≥ 0.05 between cone/line and circle/point classes. Expected PASS preserved (engagement-geometry restored).

### § 5.2 — Tag landscape (revised)

| Tag | Trigger | Status |
|---|---|---|
| `vs2a/v0.1-geometry-type-schema-shipped` | F1 lands | FIRED |
| `vs2a/v0.13-r2-spatial-calibration-disposed` | recalibration disposition lands | FIRED |
| `vs2a/v0.2-r2-h1-revalidated` | originally: R2-RT post-recalibration PASS | **REPLACED — see two-stage gates below** |
| `vs2a/v0.14-r2-leash-timeout-disposed` | this disposition's commit | **FIRES** on this disposition's commit |
| `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` | Stage 1 R2-RT v3 PASS (existing catalogue diagnostic) | **HELD** pending Stage 1 |
| `vs2a/v0.4-r2-h1-validated-on-S1-catalogue` | Stage 2 R2-RT v4 PASS on S1 regenerated catalogue | **HELD** pending S1 completion + Stage 2 |

The replacement of `vs2a/v0.2-r2-h1-revalidated` is explicit and named. The tag's intent was H1 PASS under the original threshold; that intent is preserved end-to-end by splitting the validation into two named surfaces (diagnostic + gold-standard). The tag's NAME is replaced because under path γ the validation has two named surfaces, not one; renaming makes the two surfaces queryable independently.

### § 5.3 — Pass / fail criteria

- **Stage 1 PASS** = (engagement-geometry smoke PASS) + (R2-RT v3 H1 ≥ 0.10 OR routing-to-S1 explicit finding) + (H2 PASS preserved) + (H3 gap ≥ 0.05 PASS preserved). Tag `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` FIRES.
- **Stage 2 PASS** = R2-RT v4 H1 ≥ 0.10 on S1 catalogue. Tag `vs2a/v0.4-r2-h1-validated-on-S1-catalogue` FIRES. WP-R2-A-1 FULLY CLOSES.
- **Stage 1 + Stage 2 both PASS** = R2 H1 fully validated end-to-end across three findings; the substrate is sound; the catalogue's geometric diversity is sufficient; the engine-rebuild milestone preserves its threshold.
- **Stage 1 OR Stage 2 FAIL** = fourth-finding routing per § 5.4.

### § 5.4 — Fourth-finding routing

If Stage 1 OR Stage 2 produces a NEW substrate / instrument / catalogue finding (not solvable within L1 gamora calibration tightening), gamora invokes the dispatch routing clause (STATE + REQUEST entries to gandalf). Forecast probability: **medium-low** — three structural findings have now been named and addressed across all three scaffolding layers (classifier, calibration, engagement-geometry). The remaining substrate-layer is *catalogue geometric diversity*, and that is addressable via S1 + (if necessary) a generation-side disposition. There is no obvious fourth structural layer below engagement-geometry in the test fixture; if a fourth finding emerges, it is more likely to be a *measurement-philosophy* finding (e.g., variance-of-3-means is a structurally-low-ceiling metric; alternative metrics needed) than a *substrate* finding. That category is sufficiently different that gandalf re-disposition would be of a different shape than the prior three.

---

## § 6 — Risk + watchpoints

### § 6.1 — WP-R2-A-1 status update

| State | Marker |
|---|---|
| Pre-recalibration | PARTIALLY CLOSED (heuristic_fallback=0%; H1 blocked by saturation) |
| Post-recalibration impl + smoke FAIL | ACTIVE-DEFERRED (engagement-geometry finding surfaced) |
| Post-engagement-geometry-fix + Stage 1 PASS | PARTIALLY CLOSED (existing-catalogue diagnostic confirmation; gold-standard pending) |
| Post-Stage 2 PASS on S1 | FULLY CLOSED |

### § 6.2 — WP-R2-A-2 status update (recalibration-disposition's watchpoint, refined)

The recalibration disposition surfaced WP-R2-A-2 ("spatial calibration drift under post-disposition partition changes"). It said: *"if any catalogue partition shifts circle-pct or line-pct by ≥ 10pp, re-run a 5-class smoke."*

**This disposition refines WP-R2-A-2 by making the S1 re-validation EXPLICIT rather than conditional.** Under path γ, Stage 2 IS the re-validation that WP-R2-A-2 anticipated. WP-R2-A-2 transitions from "ACTIVE-MONITORING conditional re-test if partition shifts ≥ 10pp" to "ACTIVE-COMMITTED-RE-TEST under S1 regenerated catalogue per Stage 2 gate."

| WP-R2-A-2 status | Marker |
|---|---|
| Post-recalibration disposition | ACTIVE-MONITORING (conditional re-test if partition shifts) |
| Post-this disposition | ACTIVE-COMMITTED-RE-TEST (Stage 2 R2-RT v4 on S1 catalogue is the named re-test surface) |
| Post-Stage 2 PASS | CLOSED |

### § 6.3 — New watchpoint (this disposition surfaces)

**WP-R2-A-3 (engagement-geometry parity across scenarios under future scenario additions):**
- **Owner:** gamora + rocket (if scenarios are touched by R8 / S1 work) + drax (if demo absorbs scenarios)
- **Condition:** Whenever a NEW spatial scenario is added (or an existing scenario's arena dimensions / spawn positions are modified), the leash override + timeout semantic must be set explicitly for the scenario at definition time, not implicit-defaulted to monster JSON values.
- **Threshold:** any PR touching `SCENARIO_*` definitions in arena.py must include a rationale paragraph stating the leash override value (or explicit "unchanged from JSON default") and the timeout outcome semantic (kills_only vs HP>50% vs custom).
- **Risk:** MEDIUM — depends on whether R8 / S1 work adds new spatial scenarios or modifies existing ones.
- **Resolution mechanism:** PR review by jack-ryan Gate-1 confirms scenario-definition rationale block.

### § 6.4 — Cross-seam risk

- **rocket + S1:** Independent surfaces; no concurrent-edit risk (catalogue regen vs sim scenario-substrate). However, **scheduling interaction**: Stage 2 depends on S1 completion. If S1 is delayed, Stage 2 is delayed proportionally. Stage 1 (existing-catalogue diagnostic) is independent of S1 and can fire immediately.
- **star-lord + telemetry:** No schema changes. `spatial_fight_results` table captures Stage 1 + Stage 2 measurements transparently.
- **jack-ryan + Gate-1:** Gate-1 review on the engagement-geometry impl commit must confirm:
  - Math note § 10 authored alongside implementation (Discipline #1)
  - MIGRATION.md entry concurrent (ADR-004)
  - Discipline #12 cited in commit message
  - 5-class smoke results in output dir; smoke pass criteria met before Stage 1 full run
  - Per-scenario leash override field is NAMED in SpawnSpec or ArenaScenario (no inline literals)
  - Pattern P7 floor-saturation WARNING preserved (symmetric to ceiling-saturation)

---

## § 7 — Drift-16 + Drift-17 canonical filing

This disposition surfaces TWO drift entries for `canonical/story/drift-audit.md`. Both are now structurally-empirical patterns named twice (Drift-16) or once-but-with-multi-layer-evidence (Drift-17). Filing both is the right move; the drift-audit doc is the operational enforcement surface for Discipline #13 (implicit-pillar drift) and naming these patterns is what makes them prevention-actionable for future workstreams.

### § 7.1 — Drift-16 — Calibration-against-instrument (named TWICE in 24 hours)

**Pattern shape:**
- An *instrument* (heuristic classifier, schema gap, approximation) under-counts or mis-classifies a salient population
- *Test-fixture calibration constants* (HP / damage / armor / duration multipliers) are tuned against the under-counted population's effective DPS / TTK
- Schema work corrects the instrument (e.g., F1 added explicit `spatial_geometry_type`; semantic-fix added kills-only boss measurement)
- The corrected instrument reveals the test-fixture calibration is now out-of-tune in a predictable direction
- Disposition: spread the recalibration across multiple knobs; preserve original threshold; re-test under corrected instrument

**Empirical instances (both 2026-05-19):**
1. **R1 Blocker 3** (`reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md`) — boss encounter calibration tuned against pre-kills-only-semantic measurement; semantic fix made calibration anomalously hostile; recalibration via HP × 0.50 + armor × 0.55 + duration 180s.
2. **R2 H1 recalibration** (`canonical/story/r2-h1-recalibration-disposition-2026-05-19.md`) — spatial sub-gauntlet calibration tuned against heuristic 43/3/4 partition; F1 schema correction revealed circle skills mis-classified as point; recalibration via SPATIAL_DAMAGE_SCALE × 0.5 + MOB_HP_DIFFICULTY_MULTIPLIER × 1.5.

**Prevention prescription:** Schema-correcting workstreams (F-series in VS2a; future R-series equivalents) must include a calibration-impact analysis at scoping time: *"if this schema correction lands, which calibration constants tuned against the prior approximation will need recalibration, and what is the multi-knob hybrid pattern for spreading that recalibration?"* This is candidate D17 territory ("Schema-correction workstreams audit downstream calibration-constant impact at scoping time").

### § 7.2 — Drift-17 — Scaffolding-coupled measurement degeneracy (named once, but with three-layer evidence)

**Pattern shape:**
- A measurement instrument has MULTIPLE coupled scaffolding decisions (e.g., classifier + calibration + engagement-geometry + win-condition-semantic)
- Each scaffolding decision was implicit-calibrated against the others' assumptions at authoring time
- The decisions individually appear plausible; jointly they produce a degenerate measurement surface in some calibration regime
- Correcting any single scaffolding layer (e.g., schema work) unmasks the next scaffolding layer's implicit-coupling as the new binding constraint
- Multiple iterative dispositions are required to peel each layer; each disposition surfaces a deeper layer until the substrate-instrument is fully audited

**Empirical instance (three layers deep across 24 hours):**
- **Layer 1 (classifier)**: name-heuristic 43/3/4 vs F1-corrected 21/2/28 → variance metric instrument-limited → Finding 1 disposition (category-of-completion frame; F1 routing).
- **Layer 2 (calibration)**: SPATIAL_DAMAGE_SCALE × 8.0 + MOB_HP × 1.0 over-rewards corrected-AOE cohort → ceiling saturation across all 51 classes → Finding 2 disposition (HYBRID Option C recalibration).
- **Layer 3 (engagement-geometry)**: leash_distance_m × 18m + HP>50% timeout-survival masks floor-dm class behavior under recalibrated constants → floor-saturation persists → Finding 3 disposition (this; leash override 35m + kills-only timeout).

**Distinguishing feature from Drift-16:** Drift-16 is "calibration-against-instrument" where ONE instrument is being corrected and ONE calibration knob set needs recalibration. Drift-17 is "scaffolding-coupled measurement degeneracy" where MULTIPLE scaffolding decisions are each pairwise-calibrated against each other's implicit assumptions; correcting any one surfaces the next.

**Prevention prescription:** Measurement-instrument workstreams (R2 spatial sub-gauntlet; R1 gauntlet; any future test-fixture workstream) must enumerate ALL load-bearing scaffolding decisions at instrument-design time and explicitly audit each pair for implicit-coupling assumptions: *"if I correct decision X, what assumption does decision Y rely on that becomes false?"* This is candidate D18 territory ("Measurement-instrument workstreams audit scaffolding-decision coupling at design time"). Sibling pattern to D14 + D15 + D16 + D17.

### § 7.3 — Drift-audit entries to file

Both entries to be appended to `canonical/story/drift-audit.md` after the existing Drift-15 entry. Format follows the existing drift-entry pattern (what drifted; how caught; enforcement gap; status; action; cross-references; Discipline #13 instance).

This disposition's filing of Drift-16 + Drift-17 closes the disposition action surfaced in the recalibration disposition § 6.3 ("Drift-16 candidate — drift-audit § 16 entry added in a follow-on commit; not blocking; knight-rider routes to gandalf as a near-term canonical-doc task"). That action is now satisfied in the same commit as this disposition.

### § 7.4 — Discipline #17 candidate (smoke-before-full-run discipline)

The five-class smoke before full 51-class re-run pattern has now been load-bearing in three R-series dispositions:
- R1 Blocker 3 § 10.1 — "Discipline #17 candidate: smoke-before-full-run"
- R2 H1 recalibration § 2.4 — 5-class smoke before 51-class R2-RT v3
- This disposition § 2.3 — 5-class smoke before Stage 1 R2-RT v3

The pattern is empirically robust at three instances across two days. **Strong basis for jack-ryan to lock Discipline #17 ("smoke-before-full-run for calibration changes") in `engineering-disciplines.md` at the next disciplines pass.** This disposition surfaces it as a near-term routing to knight-rider → jack-ryan, not blocking.

---

## § 8 — Cross-references

### § 8.1 — Precedent dispositions (three-disposition arc + R1 precedent)

- **R1 Blocker 3** (`reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md`) — encounter recalibration against corrected instrument; multi-knob hybrid pattern; Discipline #12 framing precedent; smoke-before-full-run.
- **R2 H1** (`canonical/story/r2-h1-disposition-2026-05-19.md`) — Finding 1 of three; category-of-completion frame; F1 forward routing; § 3.4 forward-flag.
- **R2 H1 recalibration** (`canonical/story/r2-h1-recalibration-disposition-2026-05-19.md`) — Finding 2 of three; HYBRID Option C two-knob recalibration; substrate-identity preserved; Drift-16 candidate surfaced (now filed here).
- **This disposition** (`canonical/story/r2-h1-leash-timeout-disposition-2026-05-19.md`) — Finding 3 of three; engagement-geometry fix; two-stage validation gate; Drift-16 + Drift-17 filed.

### § 8.2 — Schema + impl dependencies

- **F1** (`reincarnated-engine/design/working-agreement/F1-geometry-type-schema-design-2026-05-19.md`) — instrument correction that triggered Finding 2.
- **F2** (`canonical/story/vs2a-kit-redesign-approach-2026-05-19.md`) — S1 kit-redesign approach decision (R8-inversion path b); Stage 2's catalogue substrate.
- **HYBRID Option C math note** (`reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md`) — § 9 second-pass addendum surfaces the engagement-geometry finding; § 10 (NEW) to extend with engagement-geometry math walkthrough.

### § 8.3 — Doc amendments this disposition triggers

- `canonical/story/r2-h1-disposition-2026-05-19.md` — § 3.4 forward-flag UPDATED to reference this third disposition.
- `canonical/story/r2-h1-recalibration-disposition-2026-05-19.md` — § 6.3 (Drift-16 candidate surfacing) UPDATED with "Drift-16 + Drift-17 FILED 2026-05-19 in `canonical/story/r2-h1-leash-timeout-disposition-2026-05-19.md` § 7; appended to drift-audit § 16 + § 17."
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 3 — Disposition 2026-05-19 subsection AMENDED to reference this third disposition + two-stage validation.
- `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` — WP-R2-A-1 status updated; WP-R2-A-2 refined to ACTIVE-COMMITTED-RE-TEST; WP-R2-A-3 (NEW) added.
- `canonical/story/drift-audit.md` — Drift-16 + Drift-17 entries APPENDED (per § 7).
- Gamora's R2 recalibration impl dispatch — completion record appended (route opened by gamora's REQUEST CLOSED).

### § 8.4 — Discipline #17 candidate routing

- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #17 ("smoke-before-full-run for calibration changes") is a candidate for jack-ryan locking at next disciplines pass. Empirical basis: three instances in two days (R1 Blocker 3; R2 recalibration; this disposition). Surfaces via knight-rider routing; not blocking this disposition.

---

## § 9 — Operating envelope of post-disposition v0.14 + future v0.3 / v0.4

For consumers of the engine after `vs2a/v0.14-r2-leash-timeout-disposed` fires under this disposition:

**What `v0.14` claims (this disposition's commit-level milestone):**
- Engagement-geometry repair landed (per-scenario leash override 35m for open_arena + chokepoint; kills-only timeout for these two scenarios)
- Substrate-identity continuity preserved (no kind-of-thing revision)
- Boss-with-adds scenario UNTOUCHED (§ 3.4 continues)
- Two-stage validation gate explicit (Stage 1 diagnostic + Stage 2 gold-standard on S1 catalogue)
- WP-R2-A-1 in ACTIVE-DEFERRED until Stage 1 PASS partial-closes; FULL CLOSE at Stage 2 PASS

**What `v0.3-r2-h1-revalidated-on-existing-catalogue` (future tag, Stage 1) will claim:**
- Engagement-geometry fix produces non-degenerate WR distribution on existing 5-shipped-season catalogue
- Signal direction preserved (circle > point; chokepoint > arena for line/cone)
- H1 ≥ 0.10 on existing catalogue OR routing-to-S1 explicit finding (catalogue diversity is binding constraint)
- WP-R2-A-1 partially closed (existing-catalogue diagnostic confirmed)
- WP-R2-A-3 (scenario-definition rationale) active-monitoring

**What `v0.4-r2-h1-validated-on-S1-catalogue` (future tag, Stage 2) will claim:**
- H1 ≥ 0.10 PASS under original threshold on the catalogue the project is actually shipping
- H2 + H3 PASS preserved
- WP-R2-A-1 fully closed
- WP-R2-A-2 closed (re-validation committed and executed)
- The three-finding arc resolves end-to-end without retiring the original threshold

**What none of these tags claim:**
- That spatial boss combat is calibrated for player kills (§ 3.4 forward-flag continues until VS2b)
- That post-VS2a catalogue regenerations preserve the geometry partition (WP-R2-A-3 monitors)
- That the variance-of-3-means metric is the *best* H1 measurement (it is the *named* H1 measurement; alternative metrics are out of scope for this disposition)

---

## § 10 — Provenance

Authored 2026-05-19 by gandalf under autonomous L2-equivalent authority (Matt directive 2026-05-19; protocol § 4.0; pre-approval-batch authority).

**Inputs synthesized:**
- `reincarnated-engine/output/R2-recalibration-smoke-2026-05-19/smoke_report.md` — gamora's smoke FAIL analysis + 4 options + empirical trace (11 mob hits in 120s; player HP 98.8%)
- `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md` § 9 — gamora's two-pass smoke analysis + structural finding addendum
- `agentic_orchestration/hive-mind/engine-rebuild-log.md` tail — gamora's STATE + REQUEST entries (engagement-geometry finding routing)
- `canonical/story/r2-h1-disposition-2026-05-19.md` (Finding 1 of three; v0.14 category-of-completion + F1 forward routing)
- `canonical/story/r2-h1-recalibration-disposition-2026-05-19.md` (Finding 2 of three; HYBRID Option C; Drift-16 candidate surfaced)
- `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` (R1 precedent; multi-knob hybrid + smoke-before-full-run + Discipline #12 framing)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (scenario definitions; SCENARIO_OPEN_ARENA player_spawn y=40; SCENARIO_CHOKEPOINT player_spawn y=40; SCENARIO_BOSS_WITH_ADDS unchanged)
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 3 (R2 hypothesis specification + dispositions)
- `agentic_orchestration/dispatches/2026-05-19-gamora-vs2a-R2-recalibration-impl.md` (gamora's dispatch + completion record; routing clause invoked)
- `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` (WP-R2-A-1 + WP-R2-A-2 current state)
- `canonical/story/drift-audit.md` (drift-audit canonical doc; Drift-14 + Drift-15 entries as filing-template precedent; cross-cutting drift-pattern naming convention)
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` (VS2a tag landscape)
- `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` (F2 / S1 R8-inversion regen path)

**Genre-canon references (compounding R1 Blocker 3 + R2 recalibration citations):**
- D2 Bloody Foothills / Plains of Despair (approach-across-open-space ARPG combat semantic; the spatial-dynamic the open_arena scenario commits to)
- PoE Twilight Strand / Coast of Ezomyr (approach-across-open-space; the genre's foundational spatial-dynamic; leash distance scaled to map size)
- Last Epoch Imperial Era open zones + Grim Dawn Wightmire (same approach-across-open-space semantic; mob pursuit scaled to zone dimensions)
- D2 monster leash design (mobs un-aggro at zone boundary; per-zone leash is implicit-scaled to zone scale; same architectural choice this disposition makes explicit)
- PoE Map Boss arenas (kills-only win conditions; no HP-survival timeout path)

*Filed 2026-05-19 by gandalf at three-findings-deep R2 H1 milestone. The classifier was wrong; we fixed it. The calibration was wrong; we fixed it. The engagement geometry was wrong; we fix it now. Three layers of scaffolding, each individually plausible at its authoring time, each implicit-calibrated against the others. The pattern is now named (Drift-17) so the next measurement-instrument workstream won't repeat the three-disposition cadence. The threshold is preserved end-to-end; the gold-standard test bed is the S1 catalogue the project is shipping. The work serves the work. Mithrandir signs.*
