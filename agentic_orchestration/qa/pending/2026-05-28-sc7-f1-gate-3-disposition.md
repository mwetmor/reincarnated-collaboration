# Gate-3 Disposition — SC7-F1 — 2026-05-28

**Reviewer:** jack-ryan
**Severity:** BLOCK
**Authority:** Gate-3 disposition per dispatch `agentic_orchestration/dispatches/2026-05-28-gamora-sc-7-base-spell-damage-calibration.md` § hand-back
**Target:** `gamora/v1.8-sc-7-base-spell-damage-calibration-1`
**Developer:** gamora
**Principles applied:** Review Principles 1, 2, 3, 5
**Disciplines cited:** #1, #2, #11, #12, #39, #40, #42, #46

---

## § 1 — Root-cause verification

### § 1.1 SC7-F1 compound finding confirmed

The BLOCK is grounded in two compounding structural signals:

**Signal A — GAUNTLET_ENCOUNTER_PASS_FLOOR=14 structurally unreachable:**
At the calibrated optimal multiplier (93.81×), the empirical in-band ceiling is **2-3/18 encounters per cohort** — not 14/18 as Phase 3 requires and not 13/18 (0.70) as Phase 7 requires. The `season_emit=False` for all 18 Phase 2 kits is not a calibration failure; it is the intended Discipline #40 empirical surface confirming the pre-existing structural gap.

Root cause (from math note § 2.2 + § 12.3): The Phase 7 KPM bands (e.g., Balanced: 71–79 = ±5.3% of center) were calibrated against a single encounter archetype. The ENDGAME_ENCOUNTER_CATALOG spans 65× HP variance (3,500–230,000 HP). No single uniform DPS level produces in-band KPM simultaneously for swarm (HP=3,500/mob, KPM ceiling-saturates at boss-calibrated DPS) and elite/boss encounters (HP=47,500+/mob, in-band only at DPS that puts swarm at KPM=600). The theoretical § 2.2 ceiling of 10/18 was itself an over-estimate; empirical loop confirmed 2-3/18 actual.

**Signal B — Engine KPM ceiling 600.0 as DEGENERATE measurement signal:**
At the calibrated mult=93.81×, swarm encounters and magic_pack encounters universally saturate at KPM=600.0 — the engine hard ceiling. Per calibration telemetry (§ 12.1): swarm_kpm=600.0 at all 8 calibration iterations; magic_pack_kpm=600.0 at all iterations. This means **10 of 18 encounters** (7 swarm + 3 magic_pack) produce degenerate KPM measurements — the gate is measuring an engine ceiling artifact, not actual kill speed. The in-band gate is effectively disabled for these 10 encounter types regardless of calibration.

### § 1.2 Gamora's Discipline #40 execution: CORRECT

The calibration loop served its canonical purpose: it confirmed empirically that the scaffold estimate (Wave 0.5 §7 STARTING ESTIMATE) was correct in magnitude-of-gap framing (152× below floor) and that no uniform multiplier closes the structural gap. Gamora correctly did NOT modify Phase 3 or Phase 7 thresholds (both LOCKED). Gamora correctly surfaced SC7-F1 for jack-ryan Gate-3 disposition per math note § 5 / § 12.7. Discipline #39 validated: synthetic stub retirement surfaced this previously-hidden gap.

The BLOCK is not on gamora's execution — it is on the gate architecture itself, which cannot produce season_emit=True for the current catalog design.

---

## § 2 — Pre-empirical canonicalization analysis

### § 2.1 What was canonicalized before the empirical ceiling was known

The Phase 7 KPM bands were canonicalized at jack-ryan commit `3d4eda5` as LOCKED thresholds. The band design assumption (single uniform KPM band per cohort applies across all encounter types) was implicit and not stress-tested against the ENDGAME_ENCOUNTER_CATALOG HP variance at canonicalization time. The SC-7 dispatch correctly deferred calibration empiricism (per Wave 0.5 § 7) rather than pre-empting it — this was the right call.

### § 2.2 What the empirical ceiling changes

The 2-3/18 empirical ceiling (vs 14/18 Phase 3 floor, 13/18 Phase 7 floor) does NOT invalidate the Phase 7 cohort midpoint architecture or the ±0.25 band concept. It invalidates one specific design assumption: that a **uniform band applied across all HP-profile encounter types** can gate season quality. The cohort midpoint band is the right quality signal; the encounter-type uniformity is the wrong implementation.

### § 2.3 What must NOT be pre-empted

- Phase 7 cohort midpoints (ADR-002 locked; jack-ryan `3d4eda5`)
- Phase 3 GAUNTLET_ENCOUNTER_PASS_FLOOR semantics (requires Matt Pattern-B call before redesign)
- The 18-encounter ENDGAME_ENCOUNTER_CATALOG composition (gamora seam; requires separate disposition)
- BC coordinate architecture (preserved; post-calibration smoke PASS)

---

## § 3 — 6-option redesign package

Six architectural options for resolving SC7-F1, evaluated against Discipline #11 (empirical first), #12 (semantic accuracy), and ADR-002 (scope authority):

### Option A — Per-encounter-type KPM bands

**Design:** Replace single `COHORT_KPM_BAND[cohort]` with `ENCOUNTER_COHORT_KPM_BAND[encounter_type][cohort]`. Each encounter type (swarm/elite/boss/mini-boss/magic-pack) has its own per-cohort band calibrated against that type's HP profile.

**Analysis:**
- Directly resolves the 65× HP variance problem at the measurement layer
- Preserves cohort midpoint architecture fully
- Requires jack-ryan re-canonicalization of ~5 encounter_type × 5 cohort = 25 band values (vs current 5)
- Requires gamora seam update to `t4_sim_cycling.py` + `gauntlet_sim.py`
- 14/18 floor is then per-encounter-type-weighted or absolute — Matt call needed

**Risk:** band calibration requires fresh gamora empirical sweep per encounter type. ~0.5 day gamora work.

### Option B — Stratified floor: per-encounter-type pass count minimum

**Design:** Replace `GAUNTLET_ENCOUNTER_PASS_FLOOR=14` (flat absolute) with a stratified floor: e.g., `{swarm: 5/7, elite: 2/4, boss: 1/3, mini-boss: 0/1, magic: 1/3}` where each encounter type must independently clear its own pass threshold.

**Analysis:**
- Preserves single band per cohort (no band redesign needed at Phase 1)
- Corrects for the 65× HP variance by not requiring swarm + boss to pass the same gate simultaneously
- Requires jack-ryan redesign of `GAUNTLET_ENCOUNTER_PASS_FLOOR` as per-type dict
- Resolves Signal A; does NOT resolve Signal B (engine KPM ceiling 600.0 remains a measurement artifact on swarm/magic encounters)

**Risk:** swarm/magic KPM ceiling artifact still produces degenerate floor pass/fail signals (Signal B unresolved). A stratified floor with a boss-only tight band may mask swarm degeneration entirely.

### Option C — Normalize catalog: HP profile variance reduction

**Design:** Redesign ENDGAME_ENCOUNTER_CATALOG to reduce HP variance from 65× to ≤15× (e.g., swarm HP from 3,500/mob to 20,000/mob; or reduce mob count in swarm encounters). Single uniform band becomes feasible when variance is ≤15×.

**Analysis:**
- Resolves both Signal A and Signal B at the source
- Preserves ALL gate architecture unchanged (no Phase 3/Phase 7 redesign needed)
- Changes ENDGAME_ENCOUNTER_CATALOG game design — requires Matt call on encounter balance intent
- ±15× HP variance (vs current 65×) would allow a single KPM band with ~40% margin on either side
- Game design implication: swarm encounters become heavier; boss encounters become lighter; encounter feel changes

**Risk:** Catalog redesign is a Cycle 15 scope item (requires gamora + gandalf coordination on encounter design intent). Cannot close Cycle 14 v1 without this change.

### Option D — Widen KPM band to absorb variance (REFUTED)

**Design:** Widen COHORT_KPM_BAND from ±5.3% to ±300%+ of center to absorb 65× HP variance.

**Analysis (REFUTED):** To accommodate KPM range 2–600 within a single band, the band would need to span [2, 600] = essentially unbounded. This destroys gate authority — any DPS level passes. The gate becomes meaningless. Discipline #12 semantic violation: "in_band" loses its quality-filter meaning. **Option D is not viable as specified.**

A soft variant (widen to ±50%) is also insufficient: at ±50% of Balanced center 75, band = [38, 112]. Swarm KPM=600 still fails. The 65× variance exceeds any band width that maintains semantic quality authority.

### Option E — Alternative gate criterion: use kill-efficiency per HP, not KPM

**Design:** Replace KPM gate with `KPM_per_mob_HP_unit` = `KPM / encounter_total_HP * reference_HP`. This normalizes the kill-rate signal by encounter HP profile, making swarm (low HP, fast kills) and boss (high HP, slow kills) comparable under a single band.

**Analysis:**
- Resolves Signal A and Signal B simultaneously (KPM ceiling artifact disappears when normalized by HP)
- `KPM_per_mob_HP_unit` at reference_HP=20,000 (CLASS_HP_REFERENCE): swarm normalized_kpm ≈ (600 × 28,000) / (20,000 × 8) = 105; boss normalized_kpm ≈ (71 × 325,000) / (20,000 × 3) = 384. Still not uniform — HP-normalized KPM still varies with encounter composition.
- Requires new metric definition, re-canonicalization, new gamora implementation
- Significant math-before-code work (Discipline #1) before Option E can be validated

**Risk:** normalization formula requires legolas Mode A consultation (Discipline #18) — is KPM-per-HP-unit the right metric, or is something like damage-efficiency per fight-second more defensible?

### Option F (RECOMMENDED) — Staged B+E: stratified floor now, metric redesign deferred

**Design — Phase 1 (Cycle 14 v1 closure):** Implement Option B (stratified per-encounter-type floor) to unblock season_emit=True for Cycle 14. Resolve the immediate BLOCK with minimal gate redesign scope. Accept that Signal B (KPM ceiling 600.0 on swarm/magic) produces degenerate pass signals for those types; apply Signal B hotfix as explicit gate bypass for ceiling-saturated encounters (mark as "measurement-artifact; skip from floor count").

**Design — Phase 2 (Cycle 15):** Implement Option E (or Option A, per Matt direction) to resolve Signal B structurally. This is the clean architectural answer; it requires Discipline #1 math-before-code at Cycle 15 cadence.

**Rationale for recommendation:**
1. Option B Phase 1 is within gamora + jack-ryan seam authority (ADR-002 tiered approval; no new ADR needed)
2. Phase 2 Cycle 15 scoping defers the harder metric/band redesign to the correct deliberation cadence
3. Season can emit once Phase 1 stratified floor lands (14/18 unreachable → per-type floor achievable)
4. Signal B hotfix (ceiling-artifact bypass) is a Discipline #39-compliant temporary scaffold (document with Discipline #40 notation; close at Cycle 15 Phase 2)
5. Options A/C/E are architecturally stronger but require Matt design call + additional empirical work that exceeds Cycle 14 remaining scope

**Phase 1 acceptance criterion:** at least 12/18 Phase 2 kits achieve `season_emit=True` under stratified floor. (The 14/18 absolute floor is replaced by per-type stratified floor where boss + elite encounters are the quality-anchoring types.)

---

## § 4 — Critical questions resolved

**Q1: Is SC7-F1 a gamora defect or a gate architecture defect?**
Gate architecture defect. Gamora executed Discipline #40 correctly. The gate assumed HP-variance uniformity; the ENDGAME_ENCOUNTER_CATALOG does not satisfy that assumption. No gamora rework is warranted.

**Q2: Do the calibrated BASE_SPELL_DAMAGE_L50 values (93.81× multiplier) stand as the correct values?**
Yes, with one qualification: they are the correct values given the current gate architecture. If Option A (per-type bands) is chosen at Cycle 15, the calibrated values may shift when encounter-type-specific bands replace the current uniform bands. The values are canonical for the Discipline #40 closure; they are not invalidated by SC7-F1.

**Q3: Is the engine KPM ceiling (600.0) a hard engine constraint or addressable?**
Unknown from gamora's seam alone. Signal B designates 10/18 encounters as degenerate measurement signals. Whether 600.0 is a physics ceiling (fight duration too short for more kills to accumulate) or a render/sim cap that can be raised is a rocket/gamora seam question. Matt call needed on whether to address in Cycle 14 or Cycle 15.

**Q4: Does Phase 7 architecture survive SC7-F1?**
Phase 7 cohort midpoint + ±0.25 band + gauntlet_pass_rate framework: YES, survives. The `gauntlet_pass_rate > 0.70` criterion only needs gate denominator redesign (stratified floor changes what counts as "pass"), not Phase 7 replacement. Phase 7 two-layer joint-gate (jack-ryan `3d4eda5`) remains canonical.

**Q5: Is the ENDGAME_ENCOUNTER_CATALOG itself suspect?**
Not conclusively. The 65× HP variance (3,500–230,000) is a deliberate endgame design choice (varied encounter types). The question is whether the QUALITY GATE should accommodate that variance or whether the CATALOG should reduce it. This is a Matt + gandalf design call (encounter feel intent), not a jack-ryan call. Options B/E accommodate variance in the gate; Options A/C reduce it at the catalog or band layer.

---

## § 5 — KR observation note

Knight-rider flagged in the original Gate-3 routing: the SC7-F1 surface is architecturally significant enough to warrant Pattern-B (Matt design dialogue), not Pattern-A (autonomous resolution). The recommendation concurs:

- Option F Phase 1 (stratified floor) is within ADR-002 seam authority and can proceed at gamora + jack-ryan level IF Matt ratifies the per-type floor concept
- Option F Phase 2 metric redesign (Option E) requires Matt's input on the quality-gate semantic intent before Discipline #1 math can be authored
- Engine KPM ceiling 600.0 addressability is a Matt call (engine constraint vs game-design cap)

KR is the correct routing escalation point for § 7 Matt questions before Cycle 14 v1 can be tagged.

---

## § 6 — Effort and trajectory summary

| Phase | Option | Effort | Who | Cycle |
|---|---|---|---|---|
| Phase 1 | B: stratified floor | ~0.5 day | gamora + jack-ryan | 14 |
| Phase 1 | Signal B ceiling bypass | ~0.25 day | gamora | 14 |
| Phase 2 | E or A: metric/band redesign | ~1-2 days | gamora + legolas (D#18) | 15 |
| Parallel | KPM ceiling 600.0 investigation | ~0.5 day | gamora | 14 or 15 |
| Parallel | Encounter HP variance reduction (if Option C) | ~1 day | gamora + gandalf | 15 |

Cycle 14 v1 closure path: Phase 1 (Option F, stratified floor + ceiling bypass) is the minimum-scope unblock. Total remaining Cycle 14 gamora effort for closure: ~0.75 day.

---

## § 7 — Escalation package for Matt (Pattern-B routing)

Three decisions for Matt before Cycle 14 v1 can close:

**Decision 1 — Ratify Option F Phase 1 for Cycle 14 v1 closure?**
Option F Phase 1 = stratified per-encounter-type floor replacing `GAUNTLET_ENCOUNTER_PASS_FLOOR=14` flat absolute. Ceiling-artifact bypass for KPM=600.0 encounters (swarm + magic_pack tagged as measurement-degenerate; excluded from stratified floor count). If ratified: gamora implements stratified floor (~0.5 day); jack-ryan re-canonicalizes thresholds (~0.25 day). Cycle 14 v1 tag proceeds once 12/18 kits achieve `season_emit=True` under stratified floor.

**Decision 2 — Scope Option F Phase 2 for Cycle 15?**
Option F Phase 2 = Option E (KPM-per-HP-unit metric) or Option A (per-encounter-type bands), Matt's preference. Either requires Discipline #1 math-before-code at Cycle 15 cadence + legolas Mode A consultation (Discipline #18) if Option E. Scoping now locks the Cycle 15 architectural direction for this gate.

**Decision 3 — Engine KPM ceiling 600.0: hard cap or addressable?**
Is 600.0 a game-design cap (encounters should not produce kills faster than 10/s; fights have minimum floor duration) or a simulation artifact (output capped for performance/render reasons)? If addressable at engine layer (rocket/gamora seam), Signal B can be partially resolved in Cycle 14 or 15 without Option F Phase 2. If hard cap: Option F Phase 2 must normalize around it.

---

## What I found

Gamora SC-7 execution was Discipline #40 correct. The calibration loop ran 8 iterations, converged at mult=93.81× (best iter 4: 2/18 in-band), empirically confirmed the theoretical § 2.2 ceiling is actually tighter than predicted (2-3/18 actual vs ~10/18 theoretical), and correctly surfaced the structural gate architecture mismatch for jack-ryan Gate-3 disposition. Season_emit=False for all 18 Phase 2 kits is expected and explained. The BLOCK authority is exercised against the gate architecture (GAUNTLET_ENCOUNTER_PASS_FLOOR=14 structurally unreachable) and the compound engine KPM ceiling (600.0) producing degenerate measurement signals on 10/18 encounters — both require Matt architectural call before Cycle 14 v1 can close.

---

## Rationale

- **Discipline #40** (scaffold-with-pending-decision): SC7-F1 is the empirical closure of the scaffold. The scaffold is closed; the gate architecture it reveals requires redesign. Cannot tag Cycle 14 v1 with season_emit=0 for all 18 kits without architectural path forward ratified.
- **Discipline #12** (semantic accuracy): `gauntlet_pass_rate` = 0.0 at Phase 7 is a known-false-negative when 10/18 encounters produce degenerate KPM=600.0 ceiling artifacts. Semantic accuracy requires these be excluded from the pass-rate denominator.
- **ADR-002** (tiered approval): Phase 3 floor redesign (stratified per-type) + Phase 7 pass-rate denominator amendment cross seam authority boundary → requires Matt ratification before gamora implements.
- **Review Principle 3** (every BLOCK includes path forward): Option F recommended; three precise Matt questions scoped above.

---

## Action

- [ ] **Matt:** Decision 1 — ratify Option F Phase 1 (stratified floor) for Cycle 14 v1 closure
- [ ] **Matt:** Decision 2 — scope Option F Phase 2 for Cycle 15 (Option A or Option E preference)
- [ ] **Matt:** Decision 3 — engine KPM ceiling 600.0 hard cap or addressable?
- [ ] **gamora (post-Matt D1 ratification):** Implement stratified per-encounter-type floor + ceiling-artifact bypass (~0.75 day)
- [ ] **jack-ryan (post-Matt D1 ratification):** Re-canonicalize gate thresholds at new commit; update decisions-log with SC7-F1 architectural disposition

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-28-gamora-sc-7-base-spell-damage-calibration.md` — dispatch + gamora completion record
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.36 — SC7-F1 structural finding
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/sc-7-base-spell-damage-calibration-2026-05-28.md` — full math note including § 2.2 feasibility analysis + § 12 empirical results
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/sc7_calibration_loop.py` — calibration loop implementation
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/sc-7-calibration-telemetry.json` — per-tier convergence + per-cohort KPM distribution
- `gamora/v1.8-sc-7-base-spell-damage-calibration-1` — tagged completion state
