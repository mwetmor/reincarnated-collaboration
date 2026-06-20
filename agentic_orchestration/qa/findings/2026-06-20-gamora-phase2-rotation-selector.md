# Finding — 2026-06-20 — gamora-phase2-rotation-selector

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no BLOCK; no WARN)
**Target:** tag `gamora/v-rotation-selector-phase2-1` — engine `e2f3929`, collab `95df683`
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #3 (seed hygiene), #11 (empirical inspection), #12 (semantic-shift)
**Gates:** G3a (Phase-2 mana-default) — gandalf pre-reg; G3b — false-PASS guard (CRITICAL)

## What I found

Phase 2 ports the kernel `ai_strategies` build-vs-spend intent into the spatial player selector
(`_select_player_skill_v2`, `spatial_engine.py`), replacing the shortest-cooldown-first pick that
collapsed to T1. Verified first-hand on every Gate-2 item:

**Mechanism correctness (Discipline #11, verified in the diff, not the report).** The selector
branches on `energy_type` and the FULL branch set is present and faithful to the kernel template:
mana-default/steady/overflow → greedy-capstone (`_dps_score` = `dm/max(cd,0.5)`, mirroring
`ai_strategies._common:466-472`); rage → build-on-swarm/spend-on-anchor (`spend_threshold =
0.5*max_energy`, anchor = `nearest.max_hp >= 2*300`); combo/charges → accumulate-then-dump
(`energy>=3.0`, direct port of `:435-438`); charge-stack → build-and-hold (`>=0.8*max_energy`).
Recompose-first HELD — no new mechanic; every branch is a transcription of existing kernel intent.
The T1-collapse fix is the rotation, NOT a coercion-removal hack: `_dps_score` floors cd at 0.5 so
the cd-0.0 capstone is no longer coerced to 2.0, but the actual selection is DPS-ordered build-vs-spend,
not naive de-coercion (which the math-note §1 correctly shows would just flip to T4-spam). Confirmed.

**Empirical inspection (Principle 6 / Discipline #11, verified on disk).** Result JSON
`rotation-selector-phase2-G3a-smoke-20260620_160112.json`: `tier_dist_off = {1:100%}` →
`tier_dist_on = {1:53.9%, 4:46.1%}`, `t1_collapse_broken: true`. T2/T3=0% is the CORRECT
greedy-capstone DPS-ordering for mana-default — I verified the reasoning rather than accepting it:
DPS-score = dm/max(cd,0.5) gives T4=2.0/0.5=4.0 ≫ T1=0.8/2.0=0.4 > T2=1.0/4.0=0.25 > T3=1.3/8.0=0.16,
so when T4 is affordable it fires, and when the pool throttles below cost-40 the next-highest-DPS
*affordable* tier is T1 (not T2/T3, which have lower DPS-score from longer cd). The two-tier
T4-burst / T1-fill shape is the honest greedy-capstone for mana-default. The Phase-1 gate now BINDS:
casters sustain T4 (kpm_on 174-288); STR throttles to T1-fill (kpm_on 18.9) — burst→lull is visible
and quantitative.

**G3b false-PASS guard (CRITICAL) — HELD.** gamora did NOT claim G3b PASS. Verified three ways:
(1) result JSON `G3b_status` = "BUILT-but-UNMEASURED-pending-Phase-R … NOT a PASS";
(2) `criterion_above_t1_gt_50pct: false` (46.1% < 50%) is recorded honestly, not massaged to PASS;
(3) math-note §4/§10 explicitly states "I will NOT claim G3b PASS on the mana-default-only population
— that would be a false PASS." The rage branch is BUILT + smoke-exercised on a synthetic entity
(builder-on-swarm at empty pool; spender-on-anchor at full pool + anchor) and explicitly UNMEASURED
on the population. This is exactly the gandalf-mandated disposition. No BLOCK.

**Semantic-shift continuity (Discipline #12) — HELD.** Math-note §7 declares the boundary
("T1-only throughput" → "full-rotation throughput") and explicitly states it COMPOSES with the
Phase-1 resource-gate shift, routing both to the four-boundary continuity record. The flag comment
in `spatial_engine.py:169-region` repeats the declaration at the code site. Coherent.

**Measure-isolated / no production-gate regression — HELD.** Diff touches only the simulation seam
(spatial_engine.py + harness + math-note + AGENT_STATE.md). `kpm_bands()` appears in the harness as
an import + a single read (`bands = kpm_bands()`) for reporting — never mutated. No
`ENCOUNTER_COHORT_KPM_BAND` or production-gate write anywhere in the diff. `bands_untouched: true`
in the JSON, verified true. Band-staleness magnitude (magic_pack DPS ×42, elite_pack ×95) is
RECORDED-NOT-ACTED — flagged as Phase-5 ONE-refit input, correctly not acted on this phase.

**Seed hygiene (Discipline #3) — HELD.** `PHASE2_SEED_BASE = 8_500_000`, disjoint from all
known-used bases (820000/Phase-1 span topped 7,337,003; [700000,766703]; [619000,684303]; 1_600_000).
Production-disjoint stride layout documented; paired-seed V2 ON/OFF so the flag is the only lever.

**Smoke-gate (Principle 2) — HELD.** Ran `tests/test_spatial_gauntlet_scenarios.py` +
`tests/test_a4_recompose_energy_calibration_round_trip.py` first-hand: **36 passed** — matches the
commit's 36/36 claim exactly (27 spatial scenarios + 9 energy round-trip).

**Cross-seam (Principle 3 / 6, ADR-004) — round-trip not applicable, justified.** Rotation selection
is internal to the simulation seam; reads only fields already on the spatial entity; no telemetry
schema change; `damage_dealt`/`resource_spent` event SHAPE unchanged (only the tier mix differs).
No MIGRATION.md required. Justification present in math-note §8 — satisfies Principle 6 clause (ii).

## Rationale

All five Gate-2 focus items pass with first-hand evidence. The false-PASS guard (the one BLOCK-worthy
risk gandalf flagged) held cleanly and is the strongest part of the work: gamora measured exactly what
the mana-default population can measure (G3a T1-collapse break) and refused to claim the post-Phase-R
falsifiers (G3b). The asymmetric-STR-starvation finding is correctly framed as an **instrument
artifact, not a real STR weakness**: STR throttles because it is firing the WRONG economy
(mana-default, where its low int/wis yields a small pool that can't sustain cost-40 T4), not because
STR's kit is weak. Its real economy is rage (build-on-damage-dealt, no mana-pool dependency), which
arrives only at Phase R. Reading STR sufficiency from this number would itself be the contamination
the workstream exists to remove (brief §5 caution; G1-ruling). gamora flags it as pre-Phase-R
foreshadowing, which is the correct disposition. Recompose-first, semantic-shift, measure-isolation,
and seed hygiene all held per Disciplines #1/#12/#3 and brief §5.

## Action

- [x] Developer (gamora): none required — Phase 2 passes Gate-2. Proceed to Phase 3 (DoT) per the dep chain.
- [ ] Carry-forward to Phase-5 Gate-6 (jack-ryan): (a) the band-staleness magnitude (magic_pack ×42 /
      elite_pack ×95) is the largest instrument shift recorded so far and is the dominant ONE-refit
      input; (b) the four-boundary semantic-shift continuity record (Phase 1 resource-gate + Phase 2
      full-rotation now logged; Phase 3 DoT + Phase 4 mitigation still to come) — assemble at Phase 5.
- [ ] Carry-forward to Phase R / Phase 6: G3b (economy distinguishability + rage build-on-swarm/
      spend-on-anchor falsifier) re-arms once the doc-48 economies are in the population. The rage
      branch is BUILT; Phase R must verify it MATERIALIZES on a real rage entity, not just the synthetic.
- [ ] Matt: no decision needed at this gate. (Phase R scope + Phase-5 band approval remain Matt's per
      the G1-ruling; not triggered by this finding.)

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (`_select_player_skill_v2`, `_is_spender_skill`, `_dps_score`, `_spend_economy_pool`, the `skill_ready` build-spend affordability branch, the cast-site accrual hook)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/rotation_selector_phase2_harness_2026_06_20.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/rotation-selector-phase2-2026-06-20.md` (§1 T1-collapse proof, §2 branch map, §3 G3a pre-compute, §4/§10 G3a/G3b split, §6 wiring, §7 semantic-shift, §8 cross-seam)
- `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/rotation-selector-phase2-G3a-smoke-20260620_160112.json`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (§3 Phase-2 + GATE G3, §5)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-20-instrument-validity-G1-rocket-economy-prerequisite-RULING.md` (the G3a/G3b split)
- Smoke verified first-hand: `tests/test_spatial_gauntlet_scenarios.py` + `tests/test_a4_recompose_energy_calibration_round_trip.py` → 36 passed
