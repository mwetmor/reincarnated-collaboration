# Gate-4 Disposition — 7th Scaffold-Drift Case — Cross-Class DPS Variance vs Single-Class-Calibrated KPM Band — 2026-05-28

**Reviewer:** jack-ryan
**Severity:** BLOCK (Pattern-B escalation — Matt design call required)
**Authority:** Gate-4 disposition per gamora Discipline #44 framing-refusal at Option F Phase 1 smoke (engine `80a4417`); Matt 2026-05-28 D7 ratification (scaffold-drift case #7+ Pattern-B routing anticipated)
**Target:** engine `80a4417` (Option F Phase 1 implementation, Discipline #44 framing-refusal invoked)
**Developer:** gamora
**Principles applied:** Review Principles 1, 2, 3, 5
**Disciplines cited:** #11, #18, #39, #40, #41, #42, #43, #44, #45

---

## § 0 — Framing Audit (Discipline #42)

### Q1 — Load-bearing framing assumptions of this Gate-4 task

1. Cross-class DPS variance is NOT subsumed by the SC7-F1 fix already delivered (stratified floor + ceiling bypass).
2. SC-7 calibrated BASE_SPELL_DAMAGE_L50 for ONE reference class — the 18 Phase 2 kits have class-specific DPS profiles that differ from the reference class.
3. The 3/18 season_emit result is the correct empirical signal, not a measurement artifact of the new stratified floor.
4. The 7th scaffold-drift case is architecturally distinct from SC7-F1 (encounter-HP-variance) and requires a separate disposition.

### Q2 — Refutation evidence sought (from telemetry + math notes)

- Smoke telemetry `option-f-phase-1-smoke-telemetry.json`: 85% T1 REJECT rate on 216 eligible encounter evaluations; 10/216 in-band (4.6%). This is DIRECT empirical evidence of cross-class DPS variance, not a measurement artifact.
- SC-7 math note § 12.3: empirical ceiling corrected to 2-3/18 in-band per cohort at the reference-class calibration. The calibration loop ran 8 iterations and converged at mult=93.81× — this is the authoritative measurement.
- Per-cohort KPM ranges in smoke telemetry `eligible_encounter_stats_by_cohort`: T2 KPM ranges 60.0–150.0 (DPS-min-maxer), 60.0–98.4 (Balanced), 60.0–70.6 (Defensive), 61.9–109.1 (Hybrid). The bands are {82-97, 71-79, 52-64, 64-82}. The actual KPM spreads SPAN multiple cohort bands — this is cross-class DPS variance, not a gate calibration issue.

### Q3 — Disposition decision

Q3=NO (do not refuse to execute Gate-4). The framing is sound: cross-class DPS variance IS a new architecturally distinct issue not subsumed by SC7-F1. The empirical evidence establishes the root cause. Proceeding with disposition.

---

## § 1 — Root-Cause Verification (Discipline #11)

### § 1.1 Empirical verification: cross-class DPS variance is the root cause

**Evidence from smoke telemetry (direct observation, not inference):**

Total eligible encounters: 216 (18 kits × 4 cohorts × 3 eligible encounter types/cohort — but not all kits have 3 eligible encounters per cohort; actual varies).

| Cohort | Eligible encounters | In-band | T1 rejected | T1 reject rate |
|---|---|---|---|---|
| DPS-min-maxer | 36 | 1 | 29 | 80.6% |
| Balanced | 72 | 2 | 61 | 84.7% |
| Defensive | 36 | 1 | 32 | 88.9% |
| Hybrid | 72 | 6 | 62 | 86.1% |
| **Total** | **216** | **10** | **184** | **85.2%** |

T1 REJECT threshold = kpm_delta > 0.30 (from `t4_sim_cycling.py` `TIER_1_REJECT_THRESHOLD`). 85% T1 reject means 85% of eligible encounter evaluations produce KPM more than 30% outside the cohort band.

**Per-kit emit breakdown:**
- `endgame_int_02_artillery_mage`: season_emit=True (Hybrid cohort, 3/4 eligible in-band)
- `endgame_wis_02_holy_knight`: season_emit=True (Hybrid cohort, 2/4 eligible in-band)
- `endgame_wis_03_ritual_mage`: season_emit=True (Balanced cohort, 2/4 eligible in-band)
- All other 15 kits: season_emit=False

**The three passing kits are INT/WIS caster-faith kits** — the kit types closest to the reference class used for SC-7 calibration (INT magical class). This is direct evidence that BASE_SPELL_DAMAGE_L50 was calibrated for one class archetype's DPS profile and the 18 Phase 2 kits span multiple DPS profiles (STR physical, DEX physical, INT magical, WIS faith).

**KPM range observed at boss encounters (T2 eligible encounters in-band + T2 KPM samples):**
- Balanced T2 KPM range: 60.0–98.4 (14% sample below band 71-79; 14% above band 71-79)
- DPS-min-maxer T2 range: 89.6–150.0 (exceeds band 82-97 at the upper end — over-performers)
- Hybrid T2 range: 61.9–109.1 (straddles Hybrid band 64-82)

The KPM spread at T2 (eligible boss encounters, not rejected) demonstrates that cross-class DPS variance drives the spread — different kit types produce genuinely different boss KPM, not measurement noise.

### § 1.2 Is this a new scaffold-drift case or an SC7-F1 amendment?

**Finding: This IS a new scaffold-drift case (7th) — it is NOT a SC7-F1 amendment.**

**Why it is NOT a SC7-F1 amendment:**
- SC7-F1 (6th case) identified the root cause as 65× HP variance making a single uniform KPM band unachievable. The fix was stratified floor — correct and delivered.
- SC7-F1 was calibrated at ONE reference class (INT/WIS magical kit at mult=93.81×). The calibration loop was Discipline #40-correct for its stated scope: find the multiplier that maximizes in-band count for the reference archetype.
- The new finding is that the 18 Phase 2 kits have class-specific DPS profiles (STR/DEX/INT/WIS × physical/magical damage paths) that produce KPM ranges outside the single-reference-class-calibrated band. This was NOT visible during SC-7 because the calibration loop operated at one reference class level by design.

**Discipline #40 diagnosis (case (c) — upstream architectural assumption retired by empirical evidence):**
The upstream assumption "calibrate BASE_SPELL_DAMAGE_L50 for one reference class and apply uniformly to all 18 Phase 2 kits" was a scaffold-with-pending-decision per Discipline #39/#40. The SC-7 math note § 3 Q-SC7-2 explicitly deferred per-tier tuning and § 12.3 acknowledged the calibration was run at the reference-class level. The cross-class DPS variance is the empirical surface of that deferred scaffold decision arriving at the gate.

**KR observation note (requested in task):** The single-reference-class-calibrated BASE_SPELL_DAMAGE_L50 IS itself a scaffold-with-pending-decision under Discipline #39 — it was calibrated for one class context (INT magical reference archetype) and applied uniformly to all 18 Phase 2 kits including STR/DEX physical kits. This is a proper Discipline #39 instance: "a stopgap that bypasses empirical-validation gates must be RETIRED at the cycle-close gate that introduced them." The cycle-close gate is now surfacing the required decision.

---

## § 2 — Compound Root-Cause Map

The 7th scaffold-drift case has two distinct components that compose at the Phase 3 gate:

**Layer 1 (Resolved — SC7-F1 / 6th case):** 65× HP variance across encounter types → single KPM band per cohort cannot gate all encounter types → FIXED by stratified floor (Option F Phase 1, engine `80a4417`). DELIVERED.

**Layer 2 (New — 7th case / this disposition):** Single-reference-class BASE_SPELL_DAMAGE_L50 calibration → STR/DEX physical kits produce fundamentally different boss KPM than the INT/WIS reference class → even at the calibrated multiplier (93.81×), most non-caster kits fall outside any cohort's KPM band at boss encounters → 85% T1 REJECT rate on eligible encounters.

These two layers are independent: fixing Layer 1 correctly (stratified floor) was necessary but not sufficient. Layer 2 requires a separate architectural decision about how KPM gate tolerance or KPM gate structure accommodates cross-class DPS variance.

---

## § 3 — 6-Option Analysis Package (Discipline #18 composition)

### Option A — Per-kit KPM bands (generalization of D2 per-encounter-type bands)

**Design:** Each of the 18 Phase 2 kit types receives its own KPM band calibrated against that kit's actual boss DPS profile. Effectively: `KIT_KPM_BAND[kit_id][cohort]` replacing the current `COHORT_KPM_BAND[cohort]`.

**Empirical grounding (Discipline #11):**
- The 3 passing kits (artillery_mage, holy_knight, ritual_mage) suggest INT/WIS caster kits sit in-band at mult=93.81×
- STR kits (heavy_barbarian: Balanced in-band at 71.1; light_fighter: sub-band at all cohorts) have different DPS profiles
- DEX kits: all 4 DEX kits season_emit=False; dagger_assassin and archer pass 0-2 non-eligible encounters but 0 eligible encounters

**Composition with SC7-F1 (D2 Cycle 15 per-encounter-type bands):**
Option A per-kit bands and D2 per-encounter-type bands are an OR-relationship at implementation level — they address different variance axes:
- D2 addresses HP-variance across encounter types (boss vs swarm at fixed class)
- Option A addresses DPS-variance across kit types (caster vs melee at fixed encounter type)
The two can compose as a 2-dimensional band space `BAND[encounter_type][kit_id][cohort]`. That is a ~18 kit × 5 encounter types × 4 cohorts = 360 band values — a significant calibration burden.

**Discipline #40 compliance:** per-kit calibration retires the single-reference-class scaffold. Each kit gets its own empirically-calibrated band. Clean closure.

**Risk:** per-kit band calibration requires 18 separate gamora calibration loops (one per kit type). ~1-2 day gamora effort. Composing with D2 Cycle 15 per-encounter-type bands defers a 360-value calibration surface to Cycle 15+. Cross-cycle scope concern.

**Effort:** ~1.5-2 days gamora + jack-ryan canonical.
**Cycle 14 close trajectory:** blocks Cycle 14 v1 close; this is Cycle 15+ scope unless a per-kit subset fires in Cycle 14.

---

### Option B — Wider band ±0.50 OR ±0.75

**Design:** Expand `COHORT_KPM_BAND` from current ±0.25 (kpm_delta ≤ 0.25 = in-band) to ±0.50 or ±0.75 to absorb cross-class DPS variance within the same single-band architecture.

**Empirical analysis (Discipline #11):**
The Balanced cohort band is currently 71-79 (±5.3% of center=75). T2 KPM observed range for Balanced: 60.0–98.4 (see eligible_encounter_stats_by_cohort). To include this range in-band:
- Band needed: 60-98 → kpm_delta ≤ (98-75)/75 = 0.31 → ±0.31 captures the observed T2 range
- At ±0.50: Balanced band = 38-112 → includes all observed T2 KPM

However, the T1 reject threshold (kpm_delta ≤ 0.30) is BELOW ±0.50. At ±0.50, the T1 stage would still reject some encounters, but the in-band gate is so wide that quality discrimination is reduced.

**Quality gate semantics (Discipline #12):**
At ±0.50, the band admits KPM=37.5–112.5 for Balanced center=75. A kit killing at 37.5 KPM is half the rate of a kit killing at 75 KPM. The gate becomes: "any kit that doesn't completely fail boss encounters." Quality discrimination is preserved at the extremes but lost at the center.

At ±0.75: Balanced band = 19-131. Admits KPM=19 (nearly no boss kill rate). Semantic accuracy (Discipline #12) is severely degraded.

**Risk:** Band widening absorbs cross-class DPS variance at the cost of gate quality authority. Discipline #12 violation risk at ±0.75. At ±0.50 the violation is borderline — defensible but semantically thin.

**Effort:** ~0.25 day gamora + jack-ryan re-canonicalization.
**Cycle 14 close trajectory:** could unblock Cycle 14 v1 close in Wave 5. Fastest unblock option. But quality gate becomes weak.

---

### Option C — Damage/HP% quality metric (replaces KPM as Phase 7 mechanical gate criterion)

**Design:** Replace KPM with `damage_fraction_per_fight = total_damage_dealt / encounter_total_HP`. This is class-agnostic: a melee kit and a caster kit delivering the same fraction of boss HP damage per fight score identically, regardless of kill speed.

**Empirical analysis (Discipline #11):**
- At the calibrated DPS level for INT/WIS reference class: boss KPM = 71-72 at mult=93.81×
- boss_with_adds HP (str_01): ~325,000. At KPM=71.1 with ~3 mobs × fight duration ~2.5min: total_damage ≈ 71.1 kills/min × 325,000/3 HP per kill × 2.5min ≈ 1,935,375 HP damage dealt vs 325,000 boss HP = 5.95× (fight completed: overkill via adds). The metric needs normalization per EXPECTED fight contribution.

**Playability gate semantics (doc 39 § 5.3):**
Damage/HP% is what the player perceives: "did my character meaningfully contribute to killing the boss?" A boss that a kit could never damage meaningfully is a playability violation. A kit that does 30% of boss HP damage but takes too long to kill it (KPM low) may still be a playable experience. The damage/HP% metric maps more directly to the player experience than KPM.

**Cross-class comparison:**
- STR heavy_barbarian at mult=93.81×: would deliver physical damage against boss (separate scaling path via BASE_PHYSICAL_DAMAGE_L50 from substrate — doc 47 § 4.2). The metric normalizes across damage types if `encounter_total_HP` is the common denominator.
- INT artillery_mage at mult=93.81×: magical damage already calibrated. Damage/HP% would be ~1.0+ (kills boss).

The metric IS class-agnostic IF physical and magical damage are separately calibrated to equivalent endgame boss HP proportion targets.

**Risk:** new metric requires new canonical definition (Discipline #1 math-before-code), legolas Mode A consultation (Discipline #18 — this is a math hotspot: new gate criterion), and gamora implementation. The metric itself may not be stable across all encounter types (multi-mob encounters scale differently from single-boss).

**Effort:** ~0.5 day legolas Mode A + ~0.75 day jack-ryan canonical + ~0.75 day gamora. Total ~2 days.
**Cycle 14 close trajectory:** cannot close Cycle 14 v1; this is Cycle 15 scope requiring Discipline #18 methodology lock before execution.

---

### Option D — Per-kit DPS normalization to reference class before applying KPM gate

**Design:** Before evaluating in-band, normalize each kit's observed KPM to a "reference-class-equivalent KPM" using a per-kit DPS normalization factor: `normalized_kpm[kit] = observed_kpm[kit] × (reference_dps / kit_dps)`. Then evaluate normalized_kpm against the current COHORT_KPM_BAND.

**Empirical analysis (Discipline #11):**
- The normalization factor requires knowing `kit_dps` at endgame — this is available from SC-7 telemetry (per-kit KPM at boss encounters is a proxy for DPS).
- Reference DPS = the calibrated INT/WIS caster DPS (boss_kpm ≈ 71-72 for reference class at mult=93.81×).
- For a STR heavy_barbarian (boss KPM observed ~ T1 REJECT level), normalization would require knowing the barbarian's actual boss KPM to compute the factor.

**Circular dependency problem:**
To normalize kit_dps, we need to know what KPM the kit actually produces at boss encounters — which requires running the fight simulation. But the simulation IS what we're gating. The normalization factor must be pre-computed from a separate reference run per kit, not derived from the same gate run being evaluated.

**Implementation path:** per-kit DPS baseline calibration loop (similar to SC-7 but per-kit) → produces per-kit normalization factors → store as `per_kit_dps_normalization_factor` in kit substrate or AGENT_STATE → apply in `w5g1_gauntlet_execution()` before in-band evaluation.

**Discipline #40 compliance:** per-kit normalization factors are themselves scaffold-with-pending-decision if derived from a partial calibration. Requires full per-kit calibration sweep to close the scaffold.

**Risk:** per-kit pre-calibration adds gamora execution cost before the gate can be applied. If STR/DEX kits use a different BASE_PHYSICAL_DAMAGE path (they do — doc 47 § 4.2 physical vs magical routes), the normalization must account for separate damage formula paths. Cross-damage-path normalization is architecturally complex.

**Effort:** ~1-1.5 days gamora (per-kit calibration sweep + normalization implementation) + jack-ryan canonical.
**Cycle 14 close trajectory:** ~partial — could fire as a Cycle 14 Wave 5 gamora item if per-kit sweep is fast (smoke discipline).

---

### Option E — Per-kit cohort midpoint median estimator (extend D2 per-cohort median to per-kit)

**Design:** The current Phase 7 median estimator (jack-ryan canonical `3d4eda5`) computes cohort midpoint as the median of all kits in a cohort. Option E computes a per-kit cohort midpoint using only that kit's historical boss KPM distribution across multiple seasons. The band then evaluates the kit against its own historical median, not the cross-kit cohort median.

**Empirical analysis (Discipline #11):**
- This requires multi-season historical data to compute a stable per-kit median. In Cycle 14 v1 with no prior season_emit, there is no historical KPM distribution to reference.
- Per-kit median would converge over time as seasons accumulate. As a Cycle 14 v1 unblock, it is a deferred option.

**Composition with D2 Cycle 15 per-encounter-type bands:**
Option E per-kit median and D2 per-encounter-type bands address different variance axes and can compose: `BAND[kit_id][encounter_type][cohort]`. But the data requirements (multi-season per-kit per-encounter-type KPM history) are substantial.

**Effort:** ~0.5 day design + jack-ryan canonical + gamora implementation. But requires multi-season baseline data that does not yet exist.
**Cycle 14 close trajectory:** cannot close Cycle 14 v1 (no prior season data); Cycle 15+ scope.

---

### Option F (jack-ryan judgment) — Staged Two-Track Resolution: Immediate Class-Archetype Bands (Track 1) + Per-kit Calibration Loops Deferred (Track 2)

**Design:**
**Track 1 (Cycle 14 v1 unblock, ~0.5-0.75 day):** Group the 18 Phase 2 kits into 4 damage-scaling archetypes per doc 47 § 3 (STR-physical, DEX-physical, INT-magical, WIS-faith) and calibrate one KPM band per archetype per cohort at the boss encounter level. This yields 4 archetypes × 4 cohorts = 16 band values (vs current 4 cohort bands). Each archetype band is calibrated empirically from the kit subsets that share the damage-scaling path (not per-individual-kit).

**Rationale for 4 archetypes:**
- The damage-scaling architecture (doc 47 § 3) already segments kits into STR-physical, DEX-physical, INT-magical, WIS-faith paths with distinct BASE_*_DAMAGE_L50 scaling
- Smoke telemetry confirms the segment signal: the 3 passing kits are all INT/WIS (caster paths); the 0-passing STR/DEX kits are physical paths
- Per doc 47 § 4.2: physical damage uses a DIFFERENT formula path from magical damage (substrate `base_physical_damage_l50` vs engine `BASE_SPELL_DAMAGE_L50`). A single KPM band across both paths is architecturally incoherent — the two paths have independent calibration constants.

**Track 2 (Cycle 15+, full per-kit calibration):** After Track 1 unblocks season_emit for Cycle 14, run per-kit calibration loops (Option A) to replace per-archetype bands with per-kit bands if the 4-archetype granularity proves insufficient. This defers the higher-resolution calibration to Cycle 15.

**Composition with SC7-F1 D2 (per-encounter-type bands, Cycle 15):**
Track 1 per-archetype bands compose with D2 per-encounter-type bands at Cycle 15 as a 2D band table: `BAND[damage_archetype][encounter_type][cohort]` = 4 × 5 × 4 = 80 values. This is the principled long-term architecture. Track 1 gets 16 values calibrated now; D2 + Track 2 expands to the full 80-value table at Cycle 15.

**Discipline #45 compliance note:** the 4 archetypes are NOT "classes" per the vocabulary lock. They are damage-scaling-path segments derived from doc 47's mechanical architecture (physical vs magical vs faith path). The segmentation is MECHANICAL (Discipline #13a-partition: permitted partition criteria include energy_type, geometry, damage-scaling path), not pre-authored taxonomy. This is per-archetype-shape in the doc 47 sense: STR-physical IS a mechanical substrate property, not a designer-authored class label.

**Effort:** Track 1: ~0.5 day gamora calibration sweep (4 archetype subsets × boss encounter KPM measurement) + ~0.25 day jack-ryan canonical. Track 2: ~1 day Cycle 15.
**Cycle 14 close trajectory:** PRESERVES Cycle 14 v1 close. Track 1 at 16 band values achievable in Wave 5. D9 close criteria (≥12/18 × 3 seasons) unblocked.

---

## § 4 — Per-Option Discipline Composition Audit (Disciplines #11, #18, #40, #41, #43, #44, #45)

| Option | #11 Empirical-first | #18 Methodology lock | #40 Scaffold closure | #41 No pre-authored taxonomy | #43 Wave-close quality | #44 Framing-refusal guard | #45 Vocabulary |
|---|---|---|---|---|---|---|---|
| A per-kit bands | PASS — requires empirical sweep per kit | PASS — calibration loop is defined; no hotspot | CLEAN — retires single-ref scaffold | PASS — mechanical per-kit, not class | Wave-close: verify 18 bands derived empirically | Gate on implementation quality | Per-kit = OK; not "per-class" |
| B wider band | PASS — band width is empirically analyzable | N/A — no methodology hotspot | PARTIAL — scaffold persists at wider margin | PASS | Wave-close: verify band-widening doesn't collapse gate authority | No framing risk | N/A |
| C damage/HP% | REQUIRES legolas Mode A first (Discipline #18) | BLOCK until methodology locked | Clean if derived properly | PASS | Not applicable until methodology locked | Gate on #18 absence | N/A |
| D per-kit normalization | PASS — requires per-kit calibration baseline | Moderate — normalization formula is a methodology choice | REQUIRES pre-kit baseline to close scaffold | PASS | Wave-close: verify normalization factors empirically derived | Watch for circular dependency | N/A |
| E per-kit median | Not applicable Cycle 14 (no prior data) | N/A | Cannot close Cycle 14 scaffold | PASS | N/A Cycle 14 | N/A | N/A |
| **F staged** | **PASS — Track 1 uses doc 47 archetype segments (empirically grounded)** | **PASS — 4-archetype calibration loops are not a hotspot** | **CLEAN — retires single-ref scaffold at archetype granularity** | **PASS — archetypes are doc 47 mechanical segments, not pre-authored classes** | **PASS — wave-close verifies 16 bands empirically calibrated** | **Low risk — calibration loops are well-defined** | **PASS — "damage archetype" = doc 47 scaling path, not vocabulary-locked term** |

---

## § 5 — Critical Architecture Questions (Discipline #42 surface findings)

### Q1: Is per-kit KPM variance substrate-emergent or calibration-artifact?

**Finding: BOTH, operating at different layers.**

- **Substrate-emergent component:** doc 47 § 3-4 establishes that STR-physical, DEX-physical, INT-magical, and WIS-faith kits have structurally distinct damage scaling paths. A STR barbarian's DPS derives from `base_physical_damage_l50` (substrate-carried per SC-6b backfill) via a different formula path than an INT mage's DPS from `BASE_SPELL_DAMAGE_L50` (engine-calibrated). This variance is architectural by design — different damage paths SHOULD produce different KPM at boss encounters.

- **Calibration-artifact component:** SC-7 calibrated BASE_SPELL_DAMAGE_L50 for one archetype (INT magical) and applied uniformly. The base_physical_damage_l50 substrate values are SC-6b-derived (SC-6b backfill at `3c95883`) with `family_baseline × amplitude_mean` formula (martial-heavy=177, ranged=91, caster=31) — these are substrate-level values, not calibrated against the same boss KPM target as BASE_SPELL_DAMAGE_L50. The two damage paths have INDEPENDENT calibration histories. No single KPM band can gate across independent calibrations.

**Implication:** Per-archetype bands (Option A/F) are the architecturally correct response to substrate-emergent variance. Wider bands (Option B) paper over the two-path calibration independence without resolving it.

### Q2: Does Option A per-kit bands compose with D2 Cycle 15 per-encounter-type bands?

**Finding: OR-relationship; both applicable; 2D composition is the long-term target.**

Option A per-kit bands and D2 per-encounter-type bands address orthogonal variance axes:
- Option A axis: DPS variance across kit types (STR vs INT vs WIS at fixed encounter type)
- D2 axis: HP-variance across encounter types (boss vs swarm at fixed kit type)

At Cycle 15, these compose as `BAND[kit_or_archetype][encounter_type][cohort]`. Option F Track 1 (per-archetype) reduces the per-kit axis to 4 archetypes, making the 2D composition manageable: 4 × 5 × 4 = 80 band values vs fully-per-kit 18 × 5 × 4 = 360 values.

The choice is NOT "Option A OR D2" — it is "Option A now, D2 at Cycle 15, both compose."

### Q3: Does Option C damage/HP% satisfy doc 39 § 5.3 playability gate semantics better than KPM?

**Finding: PARTIAL. Semantics are better; methodology complexity is higher; Cycle 15+ scope.**

Per the Gate-3 disposition (`044f4ea`) § 4 Q4: "Phase 7 cohort midpoint + ±0.25 band + gauntlet_pass_rate framework: YES, survives." The KPM architecture is sound; the calibration granularity is insufficient for cross-class variance. Option C replaces the metric entirely, which is architecturally cleaner but requires:
1. Legolas Mode A methodology consultation (Discipline #18 — methodology hotspot)
2. Multi-damage-path normalization for physical vs magical tracks
3. Jack-ryan canonical definition of `damage_fraction_per_fight` as a quality gate criterion

Option C has higher long-term quality semantics but CANNOT close Cycle 14 v1 and requires explicit Discipline #18 methodology lock before any implementation fires. Route to Cycle 15 alongside D2.

---

## § 6 — KR Observation Note: BASE_SPELL_DAMAGE_L50 as Scaffold-With-Pending-Decision (Discipline #39)

The single-reference-class BASE_SPELL_DAMAGE_L50 = {T1:28144, T2:42216, T3:60978, T4:112575} is explicitly a Discipline #39 scaffold-with-pending-decision:

1. **Origin:** SC-7 calibrated for ONE reference INT/WIS magical class. Math note § 12 records convergence at mult=93.81× against the reference archetype.
2. **Application scope:** Applied uniformly to ALL 18 Phase 2 kits including STR/DEX physical kits — kits that use a DIFFERENT damage formula path (doc 47 § 4.2 physical route via `base_physical_damage_l50`).
3. **Cross-path incoherence:** For STR/DEX physical kits, `BASE_SPELL_DAMAGE_L50` is irrelevant — their damage derives from the substrate `base_physical_damage_l50` path. Applying SC-7's calibrated `BASE_SPELL_DAMAGE_L50` to physical kits produces NO effect on their DPS. The physical kits' DPS is governed entirely by the SC-6b substrate values, which were NOT calibrated against the same boss KPM target.
4. **Discipline #39 trigger:** "stopgaps that bypass empirical-validation gates must be RETIRED at the cycle-close gate that introduced them." The SC-7 calibration scope-limited note acknowledged this: per-class calibration was deferred per § 3 Q-SC7-2 (Discipline #11 empirical-first: "don't add degrees of freedom until the data shows they are necessary"). The data now shows it is necessary: 85% T1 reject on eligible encounters, with 0/4 STR kits passing.

**Conclusion:** BASE_SPELL_DAMAGE_L50 applied uniformly across all damage paths is the Discipline #39 scaffold. The canonical decision now required: separate calibration per damage-scaling path (physical vs magical vs faith), or a path-agnostic metric (Option C), or per-archetype bands at the gate layer (Option F Track 1).

---

## § 7 — Effort and Cycle 14 Close Trajectory Impact

| Option | Effort | Who | Cycle 14 v1 impact | D9 close (≥12/18 × 3 seasons) |
|---|---|---|---|---|
| A per-kit bands | 1.5-2d gamora + jack-ryan | gamora + jack-ryan | BLOCK — too large for Wave 5 | Unblocked post-Option-A Cycle 15 |
| B wider band | 0.25d gamora + jack-ryan | gamora + jack-ryan | UNBLOCKS — fast | Unblocked; gate authority reduced |
| C damage/HP% | 2d total (legolas + jack-ryan + gamora) | gamora + legolas + jack-ryan | CANNOT CLOSE Cycle 14 | Unblocked Cycle 15+ |
| D per-kit normalization | 1-1.5d gamora | gamora + jack-ryan | PARTIAL — possible Wave 5 if fast | Unblocked if normalization converges |
| E per-kit median | Not applicable Cycle 14 | — | CANNOT CLOSE | Unblocked Cycle 16+ (multi-season) |
| **F staged** | **Track 1: ~0.75d; Track 2: ~1d Cycle 15** | **gamora + jack-ryan** | **UNBLOCKS Wave 5 (Track 1)** | **Unblocked at Wave 5** |

**Matt D7 anticipated this cascade:** Matt 2026-05-28 D7 ratified "if 3 attempts fail, likely scaffold-drift case #7+" and Pattern-B routing. The Cycle 14 close trajectory for any option must compose with D9 close criteria (≥12/18 × 3 seasons, per Matt D4).

**Option F Track 1 preserves season_001 Gate-2 PASS unblock timing** — Track 1 per-archetype calibration is Wave 5 scope. All other options except Option B are Cycle 15+ scope. Option B is the only comparable timing alternative but sacrifices gate quality.

**D13 P1-P9 parallel-fire composition:**
Track 1 (Option F) does not affect D13 P1-P9 parallel-fire seasons beyond unblocking season_emit. The per-archetype band calibration fires within gamora's simulation seam and does not require changes to rocket/star-lord/export seams. Option B similarly contained. Options A/C/D/E all require cross-seam coordination that would impact the parallel-fire timeline.

---

## § 8 — Recommendation

**RECOMMEND: Option F Staged (Track 1 per-archetype bands in Wave 5; Track 2 full per-kit Cycle 15).**

Rationale:
1. Track 1 directly addresses the architectural root cause (two independent damage calibration paths) via per-archetype segmentation that is grounded in doc 47's mechanical architecture — not an arbitrary grouping.
2. Track 1 closes the Discipline #39 scaffold (single-reference-class uniform calibration) at the granularity that empirical data supports (4 archetypes based on damage-scaling path, not 18 per-kit).
3. Track 1 preserves Cycle 14 v1 close and D9 close criteria unblocking.
4. Track 2 at Cycle 15 composes cleanly with D2 (per-encounter-type bands) into the principled 2D band architecture.
5. Option B is the minimal-effort alternative but semantically degrades the gate to a near-pass-always condition, which violates Discipline #12 (semantic accuracy).
6. Options C/E are architecturally superior in the long run but require Discipline #18 methodology lock and cannot close Cycle 14.

**If Matt prefers Option B (faster, simpler):** band widening to ±0.40 (not ±0.75) is the defensible bound. At ±0.40: Balanced band = 45-105. This admits KPM as low as 45 (below the 52-KPM Defensive band floor) but excludes complete non-performers. Document as Discipline #39 scaffold (BAND-WIDENING-PENDING-ARCHETYPE-CALIBRATION) with Cycle 15 retirement obligation.

---

## § 9 — Escalation Package for Matt (Pattern-B Design Call)

**Decision 1 — Approve Option F Track 1 per-archetype bands for Cycle 14 Wave 5?**
4 damage-scaling archetypes (STR-physical, DEX-physical, INT-magical, WIS-faith per doc 47 § 3) receive separate boss-KPM band calibration at the cohort level. 4 archetypes × 4 cohorts = 16 band values replacing current 4. Gamora empirical sweep per archetype group (~0.5d); jack-ryan canonical (~0.25d). Cycle 14 v1 close preserved.

**Decision 2 — Route Option B as alternative if D1 is too large for Wave 5?**
Band widening ±0.25 → ±0.40 (or ±0.50) as a temporary scaffold. Fast (~0.25d). Degrades gate quality. Requires explicit Discipline #39 SCAFFOLD tag with Cycle 15 retirement. If ratified, jack-ryan re-canonicalizes `3d4eda5` with the wider band + scaffold declaration.

**Decision 3 — Scope Track 2 + Option C/D for Cycle 15?**
After Cycle 14 v1 closes under Track 1 (or Option B), scope the Cycle 15 architectural close:
- Option C (damage/HP% metric): legolas Mode A methodology consultation first; then jack-ryan + gamora canonical + implementation
- Option A (per-kit full calibration): gamora calibration sweep per all 18 kit types; jack-ryan canonical 16-18 band values
- D2 (per-encounter-type bands): already scoped; composes with Track 1/Track 2 as 2D band table
Matt chooses between Option C and full per-kit Option A for the Cycle 15 architectural close.

---

## What I found

Option F Phase 1 (stratified floor + ceiling bypass, engine `80a4417`) is architecturally correct and is a complete resolution of the SC7-F1 6th scaffold-drift case. The Discipline #44 framing-refusal is correct: the implementation is right; the remaining acceptance gap (3/18 season_emit vs ≥12/18 required) is a new architectural issue not addressed by Phase 1. The 7th scaffold-drift case is the empirical surface of a deferred decision: SC-7 calibrated BASE_SPELL_DAMAGE_L50 for one reference class and applied uniformly to all 18 kits including physical-damage kits on a completely separate calibration path (doc 47 § 4.2). The 85% T1 reject rate on eligible encounters is the empirical consequence of that deferred decision arriving at the gate. The pass pattern (3 INT/WIS caster kits; 0 STR/DEX physical kits) directly confirms the root cause: cross-damage-path variance, not calibration magnitude.

---

## Rationale

- **Discipline #39** (no-synthetic-stub-as-permanent-fallback): SC-7 single-reference-class calibration IS the scaffold. The 18-kit Phase 2 smoke is the gate revealing the deferred decision.
- **Discipline #40** (scaffold-values-require-canonical-decision): BASE_SPELL_DAMAGE_L50 was flagged SCAFFOLD-WITH-PENDING-DECISION in SC-7 math note § 3 Q-SC7-2. The canonical decision is now required before Phase 3 can close.
- **Discipline #11** (empirical inspection): per-archetype calibration loops are the correct empirical-first approach. Widening the band without archetype-aware calibration is assumption-based design.
- **ADR-002** (tiered approval): per-archetype KPM bands are within gamora + jack-ryan seam authority (Matt D1 precedent for stratified floor). Matt Pattern-B call on which option to implement is required before dispatch fires.
- **Review Principle 3** (every BLOCK includes path forward): Option F Track 1 is the recommended path forward; Decision 1-3 above define the precise Matt call needed.

---

## Action

- [ ] **Matt:** Decision 1 — ratify Option F Track 1 (per-archetype boss KPM bands, 16 values) for Cycle 14 Wave 5
- [ ] **Matt:** Decision 2 — if Track 1 exceeds Wave 5 scope, ratify Option B (band widening to ±0.40) as scaffold with Cycle 15 retirement obligation
- [ ] **Matt:** Decision 3 — scope Track 2 + Option C or A for Cycle 15 architectural close
- [ ] **gamora (post-D1 or D2 ratification):** implement per-archetype bands OR band widening per Matt's choice
- [ ] **jack-ryan (post-D1 or D2 ratification):** re-canonicalize Phase 7 threshold doc at new commit with per-archetype band values OR wider band + scaffold declaration; update decisions-log with 7th scaffold-drift case entry
- [ ] **KR:** route Gate-4 disposition to Matt for D1+D2+D3 ratification; author implementation dispatch post-ratification per Option F Track 1 or Option B

---

## References

- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-phase-1-smoke-telemetry.json` — primary empirical evidence (85% T1 reject; 10/216 in-band; 3/18 season_emit)
- `agentic_orchestration/dispatches/2026-05-28-gamora-option-f-phase-1-stratified-floor.md` — completion record + Discipline #44 framing-refusal
- `reincarnated-engine/src/reincarnated/simulation/math/sc-7-base-spell-damage-calibration-2026-05-28.md` — SC-7 math note § 12 empirical results; § 3 Q-SC7-2 per-class calibration deferral
- `reincarnated-engine/src/reincarnated/simulation/math/option-f-phase-1-stratified-floor-math-2026-05-28.md` — Option F Phase 1 math authority
- `agentic_orchestration/qa/pending/2026-05-28-sc7-f1-gate-3-disposition.md` — 6th scaffold-drift case Gate-3 disposition (`044f4ea`)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — doc 47 damage-scaling paths (4 archetypes: STR-physical, DEX-physical, INT-magical, WIS-faith)
- `reincarnated-engine/design/decisions/decisions-log.md` — BASE_SPELL_DAMAGE_L50 scaffold decision history
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #11, #18, #39, #40, #42, #44 (all cited above)
