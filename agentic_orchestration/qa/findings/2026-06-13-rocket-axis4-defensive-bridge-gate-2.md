# Finding — 2026-06-13 — rocket Axis-4 defensive-bridge allocator

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (G1/G2/G3/G4 all PASS; two INFO folded forward; cross-seam touch CLEARS Gate-2, no gamora pre-concurrence required)
**Target:** engine `fc6e47e` (7 files) + collab `90a906e` (cross-seam flag)
**Developer:** rocket
**Spec / acceptance authority:** `agentic_orchestration/gandalf/notes/2026-06-13-defensive-bridge-design-spec.md` (collab `864a107`), §7 gates G1–G4
**Principles applied:** Review #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #6 (cross-seam round-trip); ADR-002 (tiered approval), ADR-004 (cross-seam MIGRATION), ADR-006 (read-only review); Disciplines #1, #11, #18, #18.2, #19.1

## What I found

The four MEASURED gates were re-run from the live BC pipeline, not taken on faith, and all four hold on my independent reproduction.

**G1 — MEASURED Axis-4 distribution (load-bearing).** I ran `scripts/rocket_defensive_bridge_measure_2026_06_13.py` twice. Both runs produced **25/22/23/26** (tank/mitigator/dodger/glass), 91/96 match (95%), eHP ordering PRESERVED (tank mean 32.8 / median 8.76 > mitigator 3.33 > dodger 2.57 > glass 0.82). All four bins land inside the ±4 band on 24. The distribution is **real and byte-deterministic** across re-runs (fixed seeds 300–407, sequential fights). Orphan baseline `0/2/0/94` is documented in the math note §0 from gamora's live full-corpus harness. G1 PASS.

**G2 — ≥2 mechanisms, no HP-bloat.** Measured mechanism counts tank=4 / mitigator=5 / dodger=3 / glass=0. No non-glass bin reaches its centroid on HP-scale alone; the allocator's `mechanism_count` audit field and the harness both confirm it. G2 PASS.

**G3 — dodger independently reachable.** Checked SEPARATELY over the 24 dodger-predicted kits: mean `avoidance_rate` 0.596, min 0.348, max 0.778, **23/24 ≥ 0.40**. The wire drives dodge from defensive intent, not dex (unit test `test_w2_avoidance_independent_of_dex` confirms a dex-floor kit clears the gate). G3 PASS.

**G4 — 270 invariant + same-element flavor divergence.** I built the fire kit `s1010-rep-0000` (vitality stat = 69) as both tank and glass off one `PlayerClass`: tank max_hp 29060 / armor 2769, glass max_hp 8412 / armor 158 — **exactly rocket's claimed pair.** The vitality stat is 69 in both; the alteration field carries no stat key (`test_g4_alteration_field_never_writes_vitality` confirms the payload excludes vitality/strength/dex/int/wis). The `STAT_BUDGET=270` assertion is live at `stat_allocator.py:47` and the kit's stat sum is 270. HP scales on DERIVED HP downstream of the budget; the vitality stat is genuinely unwritten. G4 PASS.

**Stress-tests (my lane):**
1. **Disc #18 timing** — math note §5 documents the honest sequence: START seeds (1.8/0.45/0.40/0.25 tank) measured 22/19/26/29 on a first pass, then the sweep fired against THAT measured gap to reach 25/22/23/26. The narrative is internally consistent and the sweep moves are tied to named confusion leaks (mitigator→glass, mitigator→dodger, tank→mitigator). Timing claim is credible. **See INFO-1** for the one reproducibility gap.
2. **270-invariant** — confirmed empirically above (vitality unwritten; 270 assertion holds).
3. **Cross-seam touch** — the `defensive_objective` handler is the **10th** additive handler on the pre-existing `alteration_fields`/`af` chain in `from_player_class` (alongside `trade_off`, `resource_conversion`, `element_conversion`, `defensive_conversion`, `geometry_collapse`, `defensive_tradeoff` ×2, `direct_damage_amplification`, `trade_off_reversed_frenzy`). The `alteration_fields` param pre-existed (combatant.py:383, gamora's Cycle-12-Wave-5 `gamora_combatant_fields` seam). rocket added no signature change, raised it to KR rather than patching silently, and documented the dict contract in MIGRATION (ADR-004 satisfied).
4. **Brownfield invariant** — confirmed: no-af and empty-af construction are byte-identical (max_hp/armor/dodge/active_effects all equal; `_defensive_seed_effects` defaults `[]`).
5. **Scope containment** — 7 files, one new generation module + one guarded sim handler + test/math/MIGRATION/state/harness. No general allocator-wiring pass; the contained Axis-4 stat-objective bridge only.
6. **Regression** — `test_defensive_allocator.py` 13/13. `test_combat_simulator.py` 22/23; the one failure `test_different_seeds_vary` reproduces with `combatant.py` reverted to its parent (B11-balance threshold, pre-existing, NOT this change — I verified via parent-checkout). rocket's attribution is honest.

## Rationale

Per Review Principle #1, the math note (Discipline #1 anchor) cites the live measurement form and the spec survived contact with the code (spec-M → measured-ratio ~2× gain explained by the denominator-folded mitigation and low caster base armor). Per Principle #3 / ADR-004, the cross-seam edit is additive, guarded, byte-identical on the un-altered path, and carries a MIGRATION dict contract — the established `af` seam, not a new one. Per Discipline #11, every gate was inspected against measured output, not asserted state. Per Discipline #18.2, the extension consultation (the sweep) fired AFTER the baseline emitted its first measured distribution.

**On gamora concurrence (the explicit question):** the touch CLEARS Gate-2 as-landed and does NOT require gamora pre-concurrence to stand, because (a) it extends an established gen→sim contract with one in-pattern additive key, (b) the un-altered path is byte-identical, (c) the signature is unchanged, and (d) it is flagged + MIGRATION-documented. gamora retains re-siting authority (whether the handler stays in `from_player_class` or moves to a defensive-application helper) — that is a within-seam refactor she may exercise later without re-opening this gate, since the `alteration_fields["defensive_objective"]` dict contract is the stable interface and won't change shape on re-siting. **Recommend KR route the flag to gamora as INFO-for-awareness, not as a blocking sign-off.**

## INFO (folded forward — neither blocks)

- **INFO-1 (reproducibility of the sweep narrative, Disc #19.1):** the harness's `_SWEEP_SEEDS` is byte-identical to the now-default calibrated `_BIN_SEEDS`, so `--sweep` re-runs the SAME calibrated seeds twice — it cannot regenerate the claimed START (22/19/26/29) → swept (25/22/23/26) transition. The START seeds survive only in spec/math-note prose, not in any runnable artifact. The measured CALIBRATED distribution is fully reproducible (I confirmed 25/22/23/26 deterministically); only the *delta* is not independently re-runnable. The cheapest refuting test — re-introduce the §4 START seeds as a `_START_SEEDS` table the harness can pass via the existing `seed_override` hook — would make the Disc #18 timing claim self-verifying rather than prose-attested. Low priority; the end-state gate is what ships.
- **INFO-2 (overfit risk, unverified):** the calibration is fit to THIS 96-kit `kse_20260613_002` corpus (low caster base armor → ~2× spec-M→measured gain). Whether 25/22/23/26 generalizes to a different corpus/element spread is untested. The gates are inequalities (`≥5.0` tank, `<2.0` glass, `≥0.40` dodger) with deliberate above-gate centroids and wide margins (tank median 8.76 vs 5.0 gate; dodger mean 0.596 vs 0.40 gate), so modest corpus drift should hold — but a cheap refuting run on a second corpus would confirm generalization. Per the dispatch, overfit risk that is real-but-unverified is INFO, not BLOCK. Folded forward; gates re-engagement criterion = a second-corpus measured pass when one next exists.

## Action

- [x] jack-ryan: Gate-2 verdict PASS-WITH-INFO on G1–G4; finding committed.
- [ ] KR: route the combatant.py touch flag to gamora as **INFO-for-awareness** (not blocking sign-off); gamora retains within-seam re-siting authority over the handler placement.
- [ ] rocket (optional, non-blocking): add a `_START_SEEDS` table + harness wiring so the Disc #18 sweep delta is self-verifying (INFO-1). Empirical criterion: harness `--sweep` reproduces both 22/19/26/29 and 25/22/23/26 from one invocation.
- [ ] rocket/gamora (deferred, non-blocking): second-corpus measured pass to confirm calibration generalization (INFO-2). Empirical criterion: a non-`kse_20260613_002` corpus lands inside the ±4 band.

## References

- `~/Games/reincarnated-engine/src/reincarnated/generation/defensive_allocator.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py` (handler at lines 589–620; `af` chain)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/defensive-bridge-allocator-2026-06-13.md`
- `~/Games/reincarnated-engine/tests/test_defensive_allocator.py`
- `~/Games/reincarnated-engine/scripts/rocket_defensive_bridge_measure_2026_06_13.py`
- `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` ([2026-06-13] entry)
- `~/Games/reincarnated-engine/src/reincarnated/generation/stat_allocator.py:47` (STAT_BUDGET=270 assertion)
- `agentic_orchestration/rocket/notes/2026-06-13-defensive-bridge-combatant-touch-flag.md`
- `agentic_orchestration/gandalf/notes/2026-06-13-defensive-bridge-design-spec.md` (acceptance authority)
