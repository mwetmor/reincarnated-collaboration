# Finding — 2026-06-15 — b6-deletion Prerequisite-A adversarial stress-run (Gate-2)

**Reviewer:** jack-ryan
**Severity:** PASS (no INFO/WARN/BLOCK)
**Target:** commit `a7d2d9f`, tag `rocket/v1.3-b6-deletion-prereq-A-stress-run` (engine repo, NOT pushed)
**Developer:** rocket
**Principles applied:** #1 (math-before-code), #2 (smoke-gate / smoke-vs-regen), #5 (severity matters); Disciplines #1, #1.2 (code-cited math), #2.1 (bounded sample), #8 (schema validation at boundaries), #10 (empirical inspection over assumption). ADR-002 (within-seam, but this gate licenses a cross-seam deletion → escalated to gandalf+Matt for fire-confirmation).

## Verdict

**PASS.** This is half of the both-pass tally that must clear before the legacy b6 `ARCHETYPE_TEMPLATES` deletion (Decision 2) may fire. gamora's Prerequisite B is the other half (running). A clears clean as a gate; a TIGHT-but-real PASS, with one zero-slack design caveat to carry forward (separated from the gate decision below).

## What I found

Verified at source, not from rocket's summary. Re-ran the harness — reproduces exactly (melee worst-cell median 11, min_geo_only 10, meets-floor 256/256, ALL PASS, ~0.8s). The three Gate-2 cruxes all hold:

1. **Amendment genuinely honored.** `overall_pass = worst_cell_pass and min_floor_pass and band_pass` (harness line 355), all three computed off the `melee_summary` only. The pooled global median IS computed (lines 358-360) but is excluded from `overall_pass` and labeled `pooled_global_median_NOT_the_gate` in the headline. The ranged/14-palette cells run in a structurally separate `_run_subset(melee_forced=False)` partition (line 335) whose summary never enters any PASS boolean. A 14-palette ranged cell therefore cannot dilute or rescue a melee-corner collapse — the exact Gate-1 amendment requirement. Every physical cell (incl. DEX/ranged) is run melee-FORCED (`geo_bin="single-target"`, `range_profile="close"` → 11-geometry palette, lines 201-203), so the headroom-1 corner is the central case on all 8 cells, not a tail.

2. **Tripwire LIVE, not asserted.** `min_floor_pass = melee_min_geo_only >= 10` (line 352). I exercised the actual pass-component logic with a forced sub-floor: holding worst_cell_median at 11 but dropping min_geo_only to 9 flips VERDICT 11→HONEST_FAIL. A single melee collapse to 9 cannot be masked by a passing median, and the ranged partition is not in the gate to rescue it. I also confirmed the composer reports the floor honestly: drawing kit_size=10 against an artificially-collapsed 9-geometry palette yields geometry_only_distinct=9 with `step3_fired=True` — the falsification sense fires exactly as designed.

3. **PASS real, not propped.** The worst corner is min_geo_only = exactly 10 (zero slack). This is a genuine native palette draw: at kit_size=10 on the 11-melee palette, `_draw_geometry_distinct_first` Phase-1 draws `min(10,11)=10` distinct geometries WITHOUT replacement (`step3_fired=False`, `reaches=0`) — confirmed by direct composer probe. Nothing props it to 10: triple-distinct (geometry, role, tier_band) equals geometry-only-distinct exactly (both {10:128, 11:36, 13:92}), so role/tier lifted ZERO sub-floor counts over the bar. No seed-selection or ranged-partition contribution enters the floor.

4. **step-3 honesty.** The kit_size=10 partition shows 0 step3 reaches (the falsification sense — floor met natively). All 72 melee reaches are in the kit_size=13 partition (kit_size 13 > 11-palette → 2 structural re-use skills per kit), correctly labeled the elrond pool-growth signal in `step3_firing.by_kit_size`. The two senses are partitioned, not conflated.

5. **Scope clean.** mechanic-pool path AST-verified disabled (`executable_references_in_envelope_composer: []`); palette invariant clean (melee 11 / ranged 14, no caster-geometry overlap); no production file touched (only the harness, the artifact, and `generation/AGENT_STATE.md` in the commit); no b6 deletion (proves the floor only).

## Rationale

The Gate-1 amendment was the single condition on this construction: the PASS must key on the headroom-1 melee subset's `worst_cell_median` + `min_geo_only`, NOT the pooled global median that could dilute a melee collapse once a 14-palette cell is present. Source verification confirms the gate is wired exactly that way and the honest-fail tripwire is executable, not narrated. Per Principle #5 and Discipline #10, I exercised the failure path rather than trusting the asserted PASS — both the gate logic flip and the composer floor-report behavior were empirically confirmed.

## Zero-slack / pool-growth caveat (design-judgment flag for gandalf+Matt — NOT a BLOCK criterion)

This is a TIGHT pass. The worst melee corner (`endgame_bc_melee_low_spiky_str_none`) sits at min_geo_only = exactly 10 — the headroom-1 corner has zero slack on the 11-geometry melee palette at kit_size 10. The envelope holds the floor under the adversarial pool, but melee headroom is exactly one geometry; any future grammar change that removes a single melee geometry from the reachable palette would drop this corner below the floor. rocket surfaced (did not design away) the 11-melee-palette 11→≥13 expansion as an elrond pool-growth refinement — the 72 structural re-use reaches at kit_size=13 are the signal that the melee palette is thin against the 13 ceiling.

Recommendation to carry to fire-confirmation: **"envelope holds the floor under stress, but melee headroom is exactly 1; melee-palette expansion (11→≥13) recommended before or concurrent with the deletion as a slack buffer."** This is a robustness note, not a gate failure — the floor IS met at 10. gandalf+Matt own whether the deletion fires now (floor proven) or waits on the palette expansion (slack restored).

## Action

- [x] jack-ryan: Gate-2 verified at source — amendment honored, tripwire live, PASS not propped. Finding committed.
- [ ] gandalf+Matt (fire-confirmation): note Prerequisite A clears as half the both-pass tally; weigh the zero-slack caveat when deciding deletion timing vs. melee-palette expansion. Decision 2 fires only when BOTH A and gamora's B pass.
- [ ] No developer action required on the stress-run itself (clean).

## References

- Harness: `~/Games/reincarnated-engine/scripts/weapon_as_identity_b6_prereq_A_adversarial_2026_06_15.py` (PASS logic lines 344-405; melee-forced subset lines 201-203; separate ranged partition line 335)
- Composer: `~/Games/reincarnated-engine/src/reincarnated/generation/weapon_envelope_composer.py` (`_draw_geometry_distinct_first` lines 192-240 — Phase-1 distinct-without-replacement = native floor)
- Artifact: `~/Games/reincarnated-engine/output/weapon-as-identity-b6-prereq-A-adversarial-20260615.json`
- Math-note: `~/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-15-b6-deletion-prereq-A-adversarial-pool-math-note.md` §§ 0, 3, 4
- Gate-1 finding: `agentic_orchestration/qa/findings/2026-06-15-gate1-rocket-b6-prereq-A-thin-pool-stress-run.md`
