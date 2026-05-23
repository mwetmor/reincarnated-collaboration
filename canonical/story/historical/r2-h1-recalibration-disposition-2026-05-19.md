# R2 H1 Recalibration Disposition — Spatial Sub-gauntlet Calibration Saturation under Corrected Instrument

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Date:** 2026-05-19
**Author:** gandalf (story-and-design steward)
**Authority:** AUTONOMOUS L2-equivalent per protocol § 4.0 (Matt directive 2026-05-19; pre-approval-batch authority).
**Predecessors (precedent chain):**
- `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` — encounter-recalibration-against-corrected-instrument precedent (R1 Blocker 3).
- `canonical/story/r2-h1-disposition-2026-05-19.md` — § 3.4 forward-flag (this disposition extends that flag) + § 4 sub-claim 4 (instrument-limited metrics have a clear re-test path).
- `reincarnated-engine/design/working-agreement/F1-geometry-type-schema-design-2026-05-19.md` — the instrument fix that this disposition reacts to.

**Trigger:** Gamora's R2-RT H1 re-test (51 × 3 × 30 under explicit `spatial_geometry_type` field; engine `output/R2-h1-revalidation-2026-05-19/`) returned **H1 FAIL via spatial calibration saturation** — a NEW finding distinct from the prior instrument-limitation reading. F1 correctly reclassified 18 additional circle-dominant classes (3 → 21 of 51). Circle skills now deal proper AOE damage in simulation. The DPS correction is large enough to produce **WR = 1.000 across all 51 classes in open_arena and chokepoint** at the existing spatial calibration (`PLAYER_ARMOR_FACTOR_VS_STANDARD = 0.85`, `SPATIAL_DAMAGE_SCALE = 8.0`). H1 variance = 0.000 because the measuring surface is degenerate.

---

## § 0 — TL;DR

**Chosen path: HYBRID (Option C) — partial damage-scale reduction + partial mob HP increase + explicit substrate-purpose framing.**

| Lever | Old (v0.13/v0.14/v0.2-RT) | New (post-disposition) | Magnitude |
|---|---|---|---|
| `SPATIAL_DAMAGE_SCALE` | 8.0 | **4.0** | -50% player damage multiplier |
| `MOB_HP_DIFFICULTY_MULTIPLIER` (NEW; open_arena + chokepoint swarm) | implicit 1.0 | **1.5** | +50% mob HP for standard-tier swarm in open_arena + chokepoint |
| `PLAYER_ARMOR_FACTOR_VS_STANDARD` | 0.85 | **0.85** (unchanged) | survivability surface preserved |
| Boss-with-adds scenario constants | (unchanged) | (unchanged) | not in scope; § 3.4 forward-flag continues |

**Rationale (one paragraph):** The R1 Blocker 3 precedent (gandalf 2026-05-19) is structurally identical to this finding — *encounter calibration set against an under-classified geometry instrument; when F1 corrected the instrument, the calibration over-rewarded the catalogue.* R1 split the recalibration across multiple knobs so no single lever did the heavy lifting (HP × 0.50 + armor × 0.55 + duration 180s). The same shape applies here: splitting the correction across `SPATIAL_DAMAGE_SCALE` (player-side) and a new `MOB_HP_DIFFICULTY_MULTIPLIER` (mob-side) preserves both the *spatial signal* (AOE geometry continues to matter; circle still outperforms point against multi-mob swarms) AND the *non-degenerate measurement surface* (WR distributes below 1.000 so variance can be measured at all). A pure damage-scale halving (Option A) would over-correct one side; a pure mob-HP increase (Option B) would leave the player-side calibration anomalously hot. The hybrid is genre-canonically clean and mirrors how D2's Hell `/players N` HP scaling and PoE's Map Tier difficulty both spread the difficulty knob across multiple dimensions rather than weaponizing a single multiplier.

**Tag firing:**
- `vs2a/v0.2-r2-h1-revalidated` — **REMAINS HELD** pending R2-RT v3 post-recalibration re-test.
- `vs2a/v0.3-r2-spatial-calibration-disposed` — **FIRES** on this disposition's commit (intermediate; this disposition is a stand-alone design surface). *Note: tag number adapts to current VS2a numbering; knight-rider re-numbers at commit time if v0.3 is already in use; the canonical name is `vs2a/v0.X-r2-spatial-calibration-disposed` and the namespace is per the VS2a scope-of-work tag-landscape.*
- `vs2a/v0.2-r2-h1-revalidated` fires AFTER R2-RT v3 passes under recalibrated constants per the validation gate in § 5.

**Sequencing:** Fires **alongside S1**, not before. S1 = catalogue kit-redesign regen; this = simulation-layer calibration. Different files. No concurrent edit. See § 4.

---

## § 1 — Decision criteria applied (what tipped me)

### § 1.1 — The R1 Blocker 3 precedent is load-bearing

R1 Blocker 3 disposition (filed 2026-05-19 by gandalf under autonomous L2-equivalent authority) addressed the same structural pattern: *gauntlet test fixture calibrated against an under-classified instrument; instrument correction (kills-only semantic fix) made the test fixture over-hostile; recalibration spread across multiple knobs.* That disposition's framing is **the canonical pattern for "instrument-corrected; test fixture follows."** This disposition follows that pattern exactly, only the direction is inverted: R1 Blocker 3 made boss reachable (knobs that REDUCE difficulty); this disposition makes the open_arena ceiling honest (knobs that INCREASE difficulty so WRs distribute below 1.000).

R1 Blocker 3 § 2.1 ("three modest knobs; no single lever does the heavy lifting") is the explicit precedent for the hybrid here. R1 used HP × 0.50 + armor × 0.55 + duration 180s; this uses `SPATIAL_DAMAGE_SCALE × 0.50` + `MOB_HP_DIFFICULTY_MULTIPLIER × 1.5`. Same shape; same authority surface; same precedent.

### § 1.2 — This is NOT a category-of-completion reframe

I considered (and rejected) the framing "preserve v0.14 + v0.2 as instrument-corrected; calibration follow-on routed to S1 territory or VS2b." Three reasons it does not fit:

1. **The original v0.14 disposition ALREADY used the category-of-completion frame** to surface the instrument-limitation finding. v0.14's sub-claim 4 explicitly committed: "INSTRUMENT-LIMITED METRICS HAVE A CLEAR RE-TEST PATH — VS2a `geometry_type` field re-enables H1 re-test under original variance ≥ 0.10 threshold." That re-test path is now MET (F1 shipped; instrument is correct). The remaining task IS the re-test itself, under the original 0.10 threshold. Reframing the re-test as a second category-of-completion would silently retire the original threshold a second time — that is the precise move R1 disposition-3 § 7.3 ("why not hold the tag pending kit redesign") and v0.14 disposition § 2.2 ("why not Option B — hold v0.14 strictly until VS2a") both warned against repeating.
2. **The finding is a magnitude question, not a kind question.** The substrate-identity of the spatial sub-gauntlet is unchanged: it still measures geometry-aware WR; circle still > point against swarms; chokepoint still favors cone/line; boss-with-adds still inherits R1-style boss difficulty. The CALIBRATION CONSTANTS are out-of-tune for the AOE-correct cohort — that is a numeric recalibration, not a substrate-identity revision. Substrate-identity declarations from v0.13/v0.14 stand untouched.
3. **Routing to S1 territory would conflate two seams.** S1 (kit-redesign regen) is a catalogue-side workstream (rocket + gandalf consultation). Spatial calibration is a sim-instrument-side workstream (gamora; same surface as R1 Blocker 3's `balance_loop.py` constants). Mixing them confuses ownership boundaries the engine-rebuild protocol § 2.3 already named.

### § 1.3 — The R2 substrate's purpose is NOT reframed

I considered (and rejected) the framing "R2's spatial substrate is a geometric-differentiation surface, not a pass/fail balance gate." That framing has appeal — it would let H1 be a *diagnostic* rather than a *target*. But it conflicts with the original R2 hypothesis (gap-solutions-and-tests.md § 3): "WR variance by geometry-type within same role increases from ~0.05 to ~0.15+" is explicitly a measurable PASS/FAIL claim, and v0.14 preserved the 0.10 threshold as the post-VS2a re-test target. Retroactively converting the substrate to a diagnostic-only role would walk back two commitments at once (v0.14's preservation; the original gap-solutions claim). The recalibration is cleaner — we honor both the substrate's diagnostic value AND the original measurement claim.

### § 1.4 — The spatial signal must be PRESERVED through recalibration

The most important design constraint: whatever recalibration lands MUST preserve the geometric signal that the original R2 hypothesis predicted and that the v0.14 disposition cited as PROVEN (28pp underlying delta point vs cone/circle under heuristic). The hybrid is designed precisely around this: a 50% damage reduction alone would bring all classes down proportionally (signal preserved) but the 1D scalar damage modifier (already at floor 0.05–0.83 for many classes) would create a different floor-saturation artifact — *all classes converging at low-WR floor* — same degeneracy, opposite ceiling. Adding a mob-HP increase preserves more of the player-damage dynamic range and lets AOE geometry differentiation surface in the WR distribution. Genre canon backs this (D2 Champion+Unique packs combine higher HP with armor scaling; PoE Map Bosses combine elemental resistance with HP scaling) — the difficulty knob is spread across multiple dimensions for a reason.

### § 1.5 — Discipline #12 framing

This recalibration is a **third semantic shift** in the R-series workstream, distinct from R1's two:

- **R1 Disposition 1 semantic shift:** what "win" means for boss/mini-boss tiers (kills-only vs HP%-at-timeout).
- **R1 Disposition 3 semantic shift:** what the gauntlet's test fixture calibration represents (genre-mid-tier endgame vs anomalously-hostile-beyond-genre-norms).
- **R2 Recalibration semantic shift (this disposition):** what the spatial sub-gauntlet's calibration represents under CORRECTED geometry classification (re-honored player AOE potential with rebalanced mob durability, so the measurement surface is non-degenerate AND the genre-canonical difficulty intent is preserved).

All three shifts are intentional and named. Commit message for the recalibration MUST cite Discipline #12 and reference this disposition document.

---

## § 2 — Implementation shape

### § 2.1 — Constants (gamora implements in `spatial_engine.py` constants block + `arena.py`)

| Constant | File | Old | New | Effect |
|---|---|---|---|---|
| `SPATIAL_DAMAGE_SCALE` | `spatial_engine.py` line 125 | 8.0 | **4.0** | Player damage multiplier in spatial fights halved. The 1D balance modifier (~0.08 floor to ~0.83 ceiling) now scales by 4.0 → spatial-effective range 0.32–3.32. Circle-AOE skills hitting 4–8 mobs simultaneously still produce strong DPS; the multiplier headroom drops by half. |
| `MOB_HP_DIFFICULTY_MULTIPLIER` (NEW) | `arena.py` constants block (top of file) | implicit 1.0 | **1.5** | Standard-tier swarm mobs in `open_arena` and `chokepoint_corridor` scenarios receive 1.5× HP at gauntlet construction time. Applied at the mob-instance level (Pydantic `model_copy` pattern, mirroring R1 Blocker 3's `BOSS_HP_DIFFICULTY_MULTIPLIER` application site). Boss tier in `boss_with_adds` scenario UNCHANGED — boss recalibration is § 3.4 forward-flagged territory. |

**Application boundary:**

- `MOB_HP_DIFFICULTY_MULTIPLIER` applies to mob spawns where `is_boss=False` AND `threat_tier in ("swarm", "magic", "elite")`. Bosses (`is_boss=True` or `threat_tier == "boss"`) and elites in boss-tier scenarios are out of scope.
- The constant lives in `arena.py` rather than `spatial_engine.py` to keep mob-fixture knobs grouped with scenario definitions; damage-scale knobs stay in `spatial_engine.py` with the damage-mitigation constants. Both files already contain calibration-block comments; this disposition extends the existing pattern.

**Math validation (post-recalibration, expected behavior):**

At a class with damage_modifier 0.5 (mid-band; ~middle of the converged 0.05–0.83 distribution under the 1D R1 calibration):

- Old `SPATIAL_DAMAGE_SCALE = 8.0`: spatial-effective modifier = 0.5 × 8.0 = 4.0. Player DPS per swarm mob ≈ ~400/s (per arena.py comment line 107–110). 8 mobs at 2019 HP each = 16,152 total HP. Time-to-clear ≈ 8 × (2019 / 400 / hits_per_skill_cycle). With circle AOE hitting 4 mobs per cast, time-to-clear ≈ 20s. With point single-target, time-to-clear ≈ 40s.
- New `SPATIAL_DAMAGE_SCALE = 4.0` + `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5`: spatial-effective modifier = 0.5 × 4.0 = 2.0. Mob HP = 2019 × 1.5 = 3028.5. Player DPS per mob ≈ 200/s (half of old). Total mob HP = 24,228. Time-to-clear ≈ 121s (circle AOE 4-hit) → **straddles 120s timeout**, distributing WR across (0.4, 0.9) range depending on RNG burst alignment + geometry hit-count variance.
- Point single-target time-to-clear under new constants ≈ 242s → WR collapses to 0.0–0.2 range. **The point/circle delta becomes load-bearing again** because the AOE multiplier is now decisive for surviving the 120s budget.

This is exactly the surface H1 was designed to measure. Variance across geometry-type means at this calibration should land in the 0.10–0.25 range under the 41/4/55 true partition (21 circle / 2 line / 28 point). The 0.10 threshold becomes genuinely reachable.

### § 2.2 — Why these specific magnitudes (genre-canonical envelope)

**`SPATIAL_DAMAGE_SCALE` 8.0 → 4.0:** The original 8.0 was chosen (per arena.py line 107–110) to scale the 1D-calibrated modifier (single-mob context) for spatial fights (3–8 mobs). With heuristic 43/3/4 geometry distribution, this produced player DPS ~400/s per skill — calibrated for the THEN-believed-prevalent single-target classes (43 of 51). Under the corrected 41% circle distribution, those classes are doing 4–8× the work per cast (AOE hits everyone in radius). **Halving the multiplier is the cleanest correction toward the true-distribution-honoring calibration**; it does not overshoot toward the opposite ceiling.

**`MOB_HP_DIFFICULTY_MULTIPLIER` 1.0 → 1.5:** The 50% mob HP increase is conservative compared to R1 Blocker 3's parallel knob (BOSS_HP_DIFFICULTY_MULTIPLIER 0.80 → 0.50 = 38% reduction in the inverse direction). Swarm mobs at 2019 HP × 1.5 = 3028 HP is still well within genre-canonical swarm durability (D2 Hell-difficulty swarms scale 30–80% × base; PoE white-pack monsters in T16 maps scale ~2× from baseline; D3 Torment XVI swarms scale 3–10×). The 1.5 multiplier is at the conservative end — calibrated to land H1 in the measurable variance zone, not to push the spatial substrate into a harsher genre niche.

**Why not a third knob (e.g., armor scaling on standard mobs)?** Standard mobs in spatial sub-gauntlet are not yet armor-mitigated against player damage; the `armor_factor` on the player-side is the only mitigation surface. Adding armor scaling on standard mobs would be a NEW mechanism, not a recalibration — out of scope for a disposition. R1 Blocker 3 added a new constant (`BOSS_ARMOR_DIFFICULTY_MULTIPLIER`) for the boss tier; doing the analogous swarm-armor mechanism here is reasonable VS2b territory if the two-knob recalibration in this disposition proves insufficient.

### § 2.3 — Code-change specification (for gamora)

| Change | File | Site | Note |
|---|---|---|---|
| Update `SPATIAL_DAMAGE_SCALE` | `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` | line 125 | 8.0 → **4.0**. Update the docstring comment block above (lines 106–114) with new math walkthrough: "modifier from ~0.08 to ~0.83 → spatial-effective 0.32–3.32; player DPS ~200/s per skill against 1.5× HP swarm; clears 8-mob swarm in ~120s with AOE geometry advantage." |
| Add `MOB_HP_DIFFICULTY_MULTIPLIER` | `src/reincarnated/simulation/spatial_gauntlet/arena.py` | new constants block (top of file, after imports) | `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5`. Include docstring citing this disposition + the R1 Blocker 3 precedent. |
| Apply HP multiplier at mob spawn construction | `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` OR wherever mob-instance HP is set from scenario `SpawnSpec` | mob-instantiation site (gamora identifies during implementation) | Apply only when `is_boss=False` AND `threat_tier in ("swarm", "magic", "elite")` AND the scenario is `open_arena` or `chokepoint_corridor`. Boss tier in `boss_with_adds` scenario gets HP=base (unchanged). Pydantic `model_copy` if mob model is immutable. |
| Update WARNING log for ceiling saturation | `spatial_engine.py` post-fight result emission | wherever fight result is computed | If post-recalibration any scenario still produces WR ≥ 0.95 for ≥ 80% of classes in smoke, log WARNING citing the calibrated constants. Pattern P7 fail-loud discipline; surfaces second-pass tightening need. |
| Math note authoring | `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md` (NEW) | new doc | Math note authored by gamora alongside implementation, cites this disposition; captures the spatial DPS / mob HP / time-to-clear walkthrough for circle vs point vs line geometry at sample modifier values. Discipline #1 (math-before-code). |
| MIGRATION.md entry | `src/reincarnated/simulation/MIGRATION.md` | append new entry after R1-related entries | Document the two new constants, the application boundary, the precedent disposition cited. ADR-004 compliance. |

### § 2.4 — Smoke-test before full re-run (Discipline #17)

Before the 51-class full R2-RT v3 re-run, gamora executes a **5-class smoke** under the recalibrated constants:

- Sample 5 classes spanning the geometry partition (per gamora's audit data): 2 circle-dominant (e.g., class_0020 fire_controller 10-circle-skill; class_0006 holy_controller 4-circle), 2 point-dominant (e.g., class_0019 physical_warrior, class_0035 hunter), 1 line-dominant (class_0016 lightning_mage or class_0059 lightning_mage).
- Run open_arena + chokepoint (boss_with_adds excluded; § 3.4 forward-flagged separately).
- Smoke pass criteria:
  - At least 2 of 5 classes produce 0.10 ≤ WR ≤ 0.90 in open_arena (non-degenerate variance surface confirmed)
  - The 2 circle-dominant classes show higher WR than the 2 point-dominant classes in open_arena (signal direction preserved)
  - The 1 line-dominant class shows higher chokepoint-vs-arena delta than the others (H3 mechanism preserved)
- If smoke FAILS: gamora has L1 authority on second-pass calibration tightening (per R1 Blocker 3 § 10.1 precedent — incremental knob adjustment within the disposition's framework). Options in preference order: (1) `SPATIAL_DAMAGE_SCALE` 4.0 → 3.0; (2) `MOB_HP_DIFFICULTY_MULTIPLIER` 1.5 → 2.0; (3) combination. Do NOT escalate back to gandalf for incremental tightening within this framework.
- If smoke PASSES: proceed to full 51-class R2-RT v3.

---

## § 3 — Substrate-identity continuity (no kind-of-thing revision)

The substrate-identity declarations from v0.13 and v0.14 stand unchanged:

- The R2 spatial sub-gauntlet remains a 2D position-and-geometry-aware fight simulator (Arena + ChokeZone + SpawnSpec; per `arena.py`)
- Three scenarios remain (open_arena 50×50, chokepoint_corridor 10×50 with bottleneck at y=[23,27], boss_with_adds 30×30 with 1 boss + 2 flanking adds)
- Win conditions remain (all_mobs_killed for open_arena and chokepoint; boss_killed for boss_with_adds)
- Geometry resolution remains (3-path resolver: explicit `spatial_geometry_type` → rich `geometry_type` translation → legacy heuristic with WARNING)
- Telemetry surface remains (`spatial_fight_results` table; 20 fields per fight; Pattern P7 enforced at write boundary)
- H2 PASS evidence from v0.14 (74.5% boss-vs-arena delta detection under heuristic) and v0.2 RT (100% qualification under corrected instrument) remains valid in its directional reading (boss is harder than swarm scenarios; magnitude rebalances under recalibration but direction is preserved)
- H3 PASS evidence from v0.14 (cone/line favoring chokepoint at +0.130 gap) remains valid in its directional reading (chokepoint geometry favors line/cone over circle/point); H3 was instrument-confounded under v0.2 RT (ceiling saturation), and the recalibration's expected effect is restoring the measurable surface

This disposition is a **calibration recalibration**, not a substrate redesign. The "kind of thing" R2 is remains exactly what v0.13/v0.14 committed.

### § 3.4 — Spatial boss recalibration — forward-flag CONTINUES (unchanged)

The R2 H1 disposition § 3.4 forward-flagged spatial boss calibration as orthogonal-finding territory for VS2a/VS2b. That forward-flag continues to apply, unchanged, in this recalibration disposition:

- `boss_with_adds` scenario continues to produce WR = 0.000 across all 51 classes (consistent with R1 Blocker 3's catalogue-kit-broken-at-boss-tier finding)
- This disposition does NOT modify `PLAYER_ARMOR_FACTOR_VS_BOSS`, boss HP, boss armor, or boss-tier max_duration
- The recalibration here applies ONLY to open_arena and chokepoint_corridor scenarios (standard-tier mobs); boss-tier remains in its v0.13/v0.14 calibration
- Post-S1 (kit-redesign-regen lands), if spatial boss WR remains 0.000 despite repaired kits, a spatial-specific boss recalibration follows in VS2b — that is a separate disposition, not in this scope

The reason for this split is the same as R1 Blocker 3's reason: standard-tier recalibration responds to instrument-correction (F1 fixed the AOE classification problem affecting swarms); boss-tier recalibration would respond to a different finding (kit-composition gap at boss difficulty, which is S1's territory). Mixing them would conflate two recalibration causes.

---

## § 4 — Sequencing

### § 4.1 — Read

**This disposition fires alongside S1, not before, not after.** The two surfaces are independent:

- **S1** (rocket + gandalf consultation; `2026-05-19-rocket-plus-gandalf-vs2a-S1-kit-redesign-sprint.md`) regenerates the 51-class catalogue with kit-redesign criteria. Catalogue-side workstream. Touches `generation/` + season JSONs. Does NOT touch `simulation/spatial_gauntlet/`.
- **This R2 recalibration** (gamora; this disposition) modifies sim-instrument constants in `simulation/spatial_gauntlet/spatial_engine.py` + `simulation/spatial_gauntlet/arena.py`. Does NOT touch `generation/` or season JSONs.

No file overlap. No concurrent-edit risk. Different seam ownership. Different dispatch headers. The two workstreams can fire in any order or in parallel.

### § 4.2 — Per knight-rider sequencing decision

Knight-rider's existing R2-RT v3 routing (the next sprint after this disposition lands) can:

- Fire **before** S1 ships — under the existing 5-shipped-season catalogue (which already has F1's explicit `spatial_geometry_type` field; 0% heuristic_fallback per gamora's audit). The R2-RT v3 measures the recalibrated H1 against the F1-corrected instrument on the existing catalogue. This is sufficient to close the H1 variance ≥ 0.10 threshold under the original criterion.
- OR fire **after** S1 ships — against the regenerated kit-redesigned catalogue. This produces a measurement that also reflects kit-redesign quality but couples two findings (recalibration + kit redesign) in one re-test cycle.

**Gandalf recommendation:** R2-RT v3 fires **on the existing 5-season catalogue, BEFORE S1 ships.** Reasoning: (a) the catalogue's geometry partition is already correct under F1 backfill; (b) coupling R2-RT v3 to S1 conflates two recalibration causes and makes the H1 ≥ 0.10 evidence hard to attribute; (c) the recalibration is a self-contained sim-instrument fix worth ratifying in isolation, on the catalogue baseline that v0.13/v0.14/v0.2-RT all measured against. **L1 gamora autonomy on this sequencing once the constants land** — gamora can choose existing-catalogue-first or wait-for-S1 based on operational ordering; this disposition does not require one or the other.

If R2-RT v3 fires before S1 and PASSES H1 ≥ 0.10: tag `vs2a/v0.2-r2-h1-revalidated` FIRES under the original threshold (the v0.14 disposition § 3.2 re-test gate is fulfilled).

If R2-RT v3 fires after S1: tag `vs2a/v0.2-r2-h1-revalidated` fires after S1 + post-S1 re-test PASSES. Either path closes the gate; the disposition does not pre-bias the path.

### § 4.3 — Dispatch routing for gamora

Knight-rider drafts a follow-on dispatch:
- `agentic_orchestration/dispatches/2026-05-19-gamora-vs2a-R2-recalibration-impl.md`
- Scope: implement the two constants per § 2.3 + 5-class smoke + (if smoke PASS) full 51-class R2-RT v3 + tag-fire on H1 PASS.
- Authority: AUTONOMOUS L1 gamora per protocol § 4.0; L1 second-pass tightening within disposition framework.

---

## § 5 — Validation gate (R2-RT v3 post-recalibration)

### § 5.1 — Tests

Re-run **all three** hypothesis tests under the recalibrated constants (identical to R2 production sprint methodology):

- **H1 — Geometry-type WR divergence:** variance ≥ 0.10 across the three geometry-type means (circle / line / point). **Threshold preserved from original criterion** (v0.14 § 3.2; this disposition's stated re-test target).
- **H2 — Boss-with-adds detection sanity:** ≥ 30% of classes show ≥ 10pp WR delta between open_arena and boss_with_adds. **Threshold preserved.** Expected to continue PASSING (boss tier untouched; standard-tier WR distribution becomes non-degenerate so the delta becomes meaningfully measurable rather than 1.000-vs-0.000 degenerate).
- **H3 — Chokepoint testability sanity:** chokepoint-vs-arena WR delta gap ≥ 0.05 between cone/line classes and circle/point classes. **Threshold preserved.** Expected to PASS again (geometry mechanism restored once WR distribution is non-degenerate).

### § 5.2 — True-partition check

Re-confirm the F1 geometry partition (41.2% circle / 3.9% line / 54.9% point) is unchanged under the recalibrated run. The recalibration does not modify the catalogue; the partition should be identical to gamora's R2-RT (v0.2) audit. If the partition shifts, surface as anomaly.

### § 5.3 — WP-R2-A-1 closure

WP-R2-A-1 (name-heuristic mis-classification tracking) is currently PARTIALLY CLOSED per gamora's R2-RT audit (heuristic_fallback = 0% MET; H1 measurement BLOCKED by saturation). After R2-RT v3 PASS under recalibrated constants and original H1 threshold, **WP-R2-A-1 fully CLOSES.**

### § 5.4 — Pass / fail criteria

- **R2-RT v3 PASS** = all three of (H1 variance ≥ 0.10 PASS) + (H2 PASS preserved) + (H3 gap ≥ 0.05 PASS preserved). Tag `vs2a/v0.2-r2-h1-revalidated` FIRES. WP-R2-A-1 CLOSES. v0.14's § 3.2 re-test gate fulfilled.
- **R2-RT v3 PARTIAL** = H1 PASS but H2 or H3 regress. Surface as anomaly via REQUEST to gandalf; do NOT auto-fire tag. Anomaly disposition follows precedent of R8 sub-cases.
- **R2-RT v3 FAIL** = H1 < 0.10 under recalibrated constants. This is a third-finding case; gandalf re-disposition required. **Forecast: extremely unlikely.** The 28pp underlying delta in v0.14 (point 0.721 vs cone/circle 1.000) was instrument-limited by sample imbalance; under corrected 21-circle distribution + non-saturated calibration, variance should land in the 0.10–0.25 range. If H1 still fails, the deeper finding would be that the *catalogue's geometric diversity is too low* (currently 41/4/55 — 2 line classes is anomalously few) which would route to S1 first-batch class selection refinement (rocket + gandalf consultation territory).

---

## § 6 — Risk + watchpoints

### § 6.1 — WP-R2-A-1 status updates

| State | Marker |
|---|---|
| Pre-disposition | PARTIALLY CLOSED (heuristic_fallback=0%; H1 blocked by saturation) |
| Post-disposition + recalibration impl + R2-RT v3 PASS | FULLY CLOSED |
| Post-disposition + recalibration impl + R2-RT v3 FAIL | Watchpoint REOPENS under new framing (catalogue diversity binding constraint); gandalf re-disposition |

### § 6.2 — New watchpoint (this disposition surfaces)

**WP-R2-A-2 (spatial calibration drift under post-disposition partition changes):**
- **Owner:** gamora
- **Condition:** Whenever the catalogue geometry partition shifts materially from the post-F1 41.2/3.9/54.9 distribution (e.g., post-S1 kit-redesign regen may shift it; future regenerations may shift it again), the spatial sub-gauntlet H1 measurement may need to be re-validated to confirm the recalibrated constants still produce a non-degenerate WR distribution.
- **Threshold:** if any catalogue partition shifts circle-pct or line-pct by ≥ 10pp, re-run a 5-class smoke (post-shift) to confirm WR variance is still in (0.10, 0.30) range. If smoke shows saturation either direction, surface to gandalf for second-pass disposition.
- **Risk:** MEDIUM — depends on S1 kit-redesign shape. If S1 deliberately rebalances kit geometry distribution (e.g., toward more 1-circle / 1-line / 1-cone / 1-point classes), partition drift may be intentional, in which case the recalibration constants need a calibration cycle of their own.
- **Resolution mechanism:** smoke-test re-run; constants re-tuned within disposition framework (L1 gamora) OR new gandalf disposition (L2-equivalent) if constant retuning fails to produce non-degenerate variance.

### § 6.3 — Calibration drift watchpoint (cross-cutting)

The pattern of "test-fixture calibration tuned against an instrument that later got corrected" has now occurred TWICE in the R-series (R1 Blocker 3 and this R2 recalibration). The drift-audit (`canonical/story/drift-audit.md`) currently does NOT name this pattern as a cross-cutting drift instance. **This disposition surfaces a candidate drift-audit addition:**

**Drift-16 candidate — "Calibration-against-instrument: test-fixture constants tuned against under-classified instruments that subsequent schema work corrects."**

Pattern shape:
- An instrument (heuristic classifier, schema gap, or other approximation) under-counts or mis-classifies a salient population
- Test-fixture calibration (HP / damage / armor / duration multipliers) is tuned against the under-counted population's effective DPS / TTK
- Schema work corrects the instrument (e.g., F1 added explicit `spatial_geometry_type`; semantic-fix added kills-only boss measurement)
- The corrected instrument reveals the test-fixture calibration is now out-of-tune in a predictable direction (over-rewarding the correctly-counted-now population, OR over-punishing it)
- Disposition: spread the recalibration across multiple knobs (R1 Blocker 3 pattern); preserve original threshold; re-test under corrected instrument

**Recommendation:** drift-audit § 16 entry added in a follow-on commit (not this disposition; not blocking). Knight-rider routes to gandalf as a near-term canonical-doc task. The pattern is now established (twice in 24 hours); naming it canonically prevents future recurrence from being treated as a novel finding.

### § 6.4 — Cross-seam risk

- **rocket + S1:** Independent surfaces; no concurrent-edit risk (catalogue regen vs sim constants).
- **star-lord + telemetry:** No schema changes; existing `spatial_fight_results` table captures recalibrated measurements transparently.
- **jack-ryan + Gate-1:** Gate-1 review on the recalibration impl commit must confirm:
  - Math note (R2-recalibration-math-2026-05-19.md) authored alongside implementation (Discipline #1)
  - MIGRATION.md entry concurrent (ADR-004)
  - Discipline #12 cited in commit message
  - 5-class smoke results in output dir; smoke pass criteria met before full 51-class run
  - Pattern P7 ceiling-saturation WARNING preserved (if recalibration overshoots, fail-loud surfaces it)
  - Constants are NAMED (no inline literals)

---

## § 7 — Cross-references

### § 7.1 — Precedent dispositions

- **R1 Blocker 3** (`reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md`) — encounter recalibration against corrected instrument; same structural pattern; this disposition follows the same multi-knob hybrid shape.
- **R2 H1** (`canonical/story/r2-h1-disposition-2026-05-19.md`) — § 3.2 re-test gate; § 3.4 forward-flag; § 4 sub-claim 4 (instrument-limited metrics have clear re-test path); this disposition extends § 3.4's reasoning to the standard-tier calibration.
- **R8 Sub-case 3** (`canonical/story/r8-disposition-2026-05-19.md`) — partial-commit precedent (for any case where part of the workstream tags fire and part is held); informs the held-vs-fired tag distinction in § 0.

### § 7.2 — Schema + impl dependencies

- **F1** (`reincarnated-engine/design/working-agreement/F1-geometry-type-schema-design-2026-05-19.md`) — the instrument fix this disposition reacts to; F1 acceptance complete is the prerequisite for this disposition's relevance.
- **F2** (`canonical/story/vs2a-kit-redesign-approach-decision-2026-05-19.md` or equivalent) — kit-redesign approach decision; S1 dispatch follows F2.

### § 7.3 — Doc amendments this disposition triggers

- `canonical/story/r2-h1-disposition-2026-05-19.md` — § 3.4 forward-flag UPDATED to reference this disposition (standard-tier calibration disposed here; boss-tier calibration continues to be forward-flagged).
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 3 — Disposition 2026-05-19 subsection AMENDED to reference this recalibration disposition.
- `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` — WP-R2-A-1 status update; WP-R2-A-2 (NEW) added.
- `canonical/story/drift-audit.md` — Drift-16 candidate surfaced; § 6.3 above. Not authored in this disposition; follow-on routing.

### § 7.4 — Tag landscape (VS2a)

Per `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § "Tag landscape":

| Tag | Trigger | Status |
|---|---|---|
| `vs2a/v0.1-geometry-type-schema-shipped` | F1 lands | FIRED |
| `vs2a/v0.2-r2-h1-revalidated` | R2 re-test passes under explicit field | **HELD pending R2-RT v3 post-recalibration** |
| `vs2a/v0.X-r2-spatial-calibration-disposed` (NEW; knight-rider numbers) | this disposition's commit | **FIRES on this disposition's commit** |
| All others | per existing VS2a roadmap | unchanged |

---

## § 8 — Operating envelope of post-recalibration v0.2

For consumers of the engine after `vs2a/v0.2-r2-h1-revalidated` fires under recalibrated constants:

**What the tag claims:**
- Spatial sub-gauntlet operates under recalibrated constants (`SPATIAL_DAMAGE_SCALE = 4.0`; `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` for standard-tier mobs in open_arena + chokepoint)
- H1 variance ≥ 0.10 PASS under original criterion + explicit `spatial_geometry_type` instrument
- H2 boss-vs-arena delta detection PASS (preserved)
- H3 chokepoint testability gap ≥ 0.05 PASS (preserved)
- WP-R2-A-1 fully CLOSED
- WP-R2-A-2 (post-disposition partition-shift drift) ACTIVE-MONITORING

**What the tag does NOT claim:**
- That spatial boss combat is calibrated for player kills (boss-with-adds WR continues at 0.000 across all 51 classes; spatial boss recalibration remains § 3.4-forward-flagged territory; consistent with R1 Blocker 3's catalogue-kit-broken-at-boss-tier finding)
- That the catalogue's geometric diversity is balanced (41/4/55 partition is the F1-corrected truth; 2 line classes is anomalously few; this is a S1 catalogue-side observation, not an R2 calibration issue)
- That post-S1 kit-redesign-regen will preserve the current partition (post-S1 partition may shift; WP-R2-A-2 monitors for this)

---

## § 9 — Provenance

Authored 2026-05-19 by gandalf under autonomous L2-equivalent authority (Matt directive 2026-05-19; protocol § 4.0; pre-approval-batch authority).

**Inputs synthesized:**
- `reincarnated-engine/output/R2-h1-revalidation-2026-05-19/R2-test1.md` — H1 FAIL result + calibration saturation analysis
- `reincarnated-engine/output/R2-h1-revalidation-2026-05-19/summary.md` — full revalidation summary + finding
- `reincarnated-engine/output/R2-h1-revalidation-2026-05-19/geometry_audit.md` — true partition audit (41.2% circle / 3.9% line / 54.9% point)
- `agentic_orchestration/hive-mind/engine-rebuild-log.md` tail — gamora's R2-RT STATE + REQUEST entries; S1 baseline R1 sprint v3 STATE
- `canonical/story/r2-h1-disposition-2026-05-19.md` § 3.2 + § 3.4 + § 4 (precedent + re-test gate + forward-flag continuity)
- `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` (encounter recalibration precedent; multi-knob hybrid shape; Discipline #12 framing precedent)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (current calibration constants; lines 116–125 + lines 90–115 docstring math walkthroughs)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (scenario definitions; mob spawn shape)
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 3 (R2 hypothesis specification)
- `agentic_orchestration/dispatches/2026-05-19-gamora-vs2a-R2-H1-revalidation.md` (gamora's dispatch + completion record)
- `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` (WP-R2-A-1 current state)
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` (VS2a tag landscape)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 autonomous-operation authority

**Genre-canon references (compounding R1 Blocker 3's citations):**
- D2 Hell-difficulty Champion+Unique pack HP scaling + `/players N` formula (swarm-tier durability genre baseline)
- PoE Map Tier scaling (T16 white-pack monsters ~2× baseline HP; multi-dimensional difficulty knob spread)
- D3 Torment XVI swarm scaling (3–10× baseline HP for elite-density swarms; difficulty-knob-on-multiple-dimensions pattern)
- Last Epoch Empowered Monolith scaling (~30–50% HP scaling combined with damage scaling for endgame swarm tiers)

*Filed 2026-05-19 by gandalf. The instrument is correct now — F1 fixed the heuristic blindness; circle is finally circle. The calibration was tuned against the wrong silhouette of the catalogue; it now needs the right silhouette's calibration. Two knobs, modest magnitudes, the genre's envelope honored on both sides. The original threshold is preserved as a threshold — neither retired nor lowered — only made measurable for the first time. Mithrandir signs.*
