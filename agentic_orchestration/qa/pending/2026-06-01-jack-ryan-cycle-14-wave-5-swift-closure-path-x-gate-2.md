# Finding — 2026-06-01 — Cycle 14 Wave 5 Swift-Closure Path X Gate-2

**Reviewer:** jack-ryan
**Severity:** PASS-with-INFO
**Target:** engine commits `779b547` (cascade-r4 Path X impl) + `15735d0` (empirical verification + 12 tests + MIGRATION + AGENT_STATE)
**Developer:** rocket
**Principles applied:** Principle 6 (cross-seam contract), Disc #11 (empirical inspection), Disc #1.2 (math-note code citation), Disc #42a (framing-audit)

---

## Disposition: PASS-with-INFO

All three empirical-criterion gates verified by direct code inspection (Disc #11 — not assumed).
Recognition-record § 4.2 structural-integrity preservation honored. MIGRATION.md adequate.
Test coverage matches gate claims. Two INFO items recorded below; neither is blocking.

---

## Gate Verification (Disc #11 — empirical, not assumed)

### Gate (i) — Code-level

**VERIFIED.**

- `_run_pm1_on_phase4_archive()` at lines 639-708 of `src/reincarnated/simulation/wave5_season_orchestrator.py`: when `phase4_accepted_kits` is non-empty (the n=34 live case), `surviving_kit_datas` is built exclusively from `phase4_accepted_kits` via `_build_pm1_kit_data`. The `passing_kits + variant_passing_rows` path is the fallback branch guarded by `if phase4_accepted_kits:` / `else:`.
- Phase 3 PM-1 at lines 1093-1114: `surviving_kit_datas = base_kit_datas + variant_kit_datas` (old assignment). The comment at line 1094 explicitly states: "In cascade-resumption-4 Path X, the orchestrator will override this pm1_result AFTER Phase 4 completes." This is a preserved-for-telemetry pass; it does NOT feed Phase 5.
- `run_wave5_season_001` Phase 4.5 block: lines ~2622-2664. `_load_phase4_archive_for_pm1` + `_run_pm1_on_phase4_archive` called after Phase 4 COMMIT SIGNAL. Phase 3 pm1_result is overridden.
- `run_season_production` Phase 4.5 block: lines ~3048-3079. Identical pattern — `_load_phase4_archive_for_pm1` + `_run_pm1_on_phase4_archive` called post-Phase 4 COMPLETE. Symmetric with `run_wave5_season_001`.

Both orchestrator entry points confirmed. Override is structural, not comment-only.

### Gate (ii) — Smoke (n=34; k=4; sparsity=none; fallback=False)

**VERIFIED.**

- `test_pm1_surviving_kit_datas_count_equals_34` asserts `len(surviving_kit_datas) == 34` by constructing kit_datas from `_load_phase4_archive_for_pm1` output against the gamora-enumerated 34-kit fixture.
- `test_run_pm1_on_phase4_archive_returns_clusters_at_n34` asserts `k_observed in {2, 3, 4}` and `fallback_ref[0] == False`. The assertion message documents observed k as required by dispatch gate (ii).
- `test_pm1_no_fallback_fires_at_n34` asserts `fallback_ref[0] == False` on the 34-kit input.
- rocket AGENT_STATE.md records k=4 (gmm_k4; BIC-selected; sparsity=none) as the retroactive backfill result for season_001. Test accepts k in {2,3,4}; empirical result was k=4.

### Gate (iii) — BC-axis 8-element coverage

**VERIFIED.**

- `test_eight_element_coverage_preserved_post_path_x` asserts `elements_present == EXPECTED_8_ELEMENTS` against the gamora-enumerated 34-kit fixture with the exact element map (earth=6, fire=6, holy=4, lightning=3, physical=8, shadow=1, water=1, wind=5, total=34).
- `test_element_distribution_not_s2_only` asserts `not all(a.substrate_sample_idx == 2 for a in adapters)` and `s0_count > 0`, confirming the pre-Path-X bug (s0=0, s1=0, s2=208) is not reproduced.
- Cross-check: `GAMORA_34_KIT_IDS` in the test file (50 lines, 34 entries) was inspected against gamora's archive-stable signal (commit `16ce0bf`). The two sets are identical — confirmed by grep count (34 S1_endgame entries in both artifacts).

---

## Recognition-Record § 4.2 Structural-Integrity Preservation

**VERIFIED.**

Recognition record § 4.2 (line 147) names: "the gauntlet structural sieve remains valid; the Pareto-2 reduction methodology remains valid; only the metric-axis validity is in question."

Path X makes this true empirically:
- Phase 5 PM-1 now consumes the Phase 4 Pareto-2 archive (the 34 Pareto-2 winners), not a disjoint 208-member variant population.
- Phase 4 archive ∩ Phase 5 population is now 100% (was 6/34 = 18% pre-Path-X).
- The cohesion judge output now describes the wave-5 Pareto-2 archive identity, which is what § 4.2 structural-integrity presumes.
- PROVISIONAL marker applies at the metric-axis layer only (per recognition § 4.2 + gandalf verdict § 1). Path X is the structural fix that allows the PROVISIONAL marker discipline to operate in its intended scope — it is not itself a PROVISIONAL artifact.

---

## MIGRATION.md Adequacy (Principle 6 — Cross-Seam Contract)

**VERIFIED — ADEQUATE.**

MIGRATION.md entry at `src/reincarnated/generation/MIGRATION.md` [2026-06-01]:

- (a) What changed: documented. "Phase 5 PM-1 input source reads Phase 4 Pareto-2 archive winners (34 mixed-sample kits) rather than `passing_kits + variant_passing_rows`." Semantic change described precisely; schema field additions: none (correctly stated).
- (b) When it took effect: documented. "Implemented in cascade-resumption-4 (engine commit `779b547`, 2026-05-29); confirmed correct in swift-closure commit `15735d0`, 2026-06-01."
- (c) What downstream consumers must know: documented. Three named consumers: star-lord Phase 5 cohesion judge, gamora Phase 7 cohesion gate, rocket Cycle 15+ pattern library Phase A. Each gets a specific note on the semantic change they observe (cluster identity, Phase 7 kit_id join coherence, pattern library substrate identity).
- Before/after boundary table included. Backward-compatibility contract (fallback behavior) documented.

Note: MIGRATION.md entry is in the `generation` seam rather than the `simulation` seam. The core implementation code is in `simulation/wave5_season_orchestrator.py`. The generation seam owns Phase 5 PM-1 clustering logic (`phase5_pm1_multimodal_clustering.py`), so the generation MIGRATION.md is the correct location per the semantic change's downstream impact. The simulation MIGRATION.md at v1.63 cross-references Path X wire-up as preserved. No gap.

---

## Test Coverage Adequacy

**12 tests confirmed. 12/12 names inspected directly.**

Enumerated names from rocket completion note, with dispatch gate mapping:

| Test name | Gate | Present |
|---|---|---|
| `test_path_x_active_when_archive_populated` | Gate (i) | YES — line 572 |
| `test_kit_id_set_exact_match_gamora_enumeration` | Gate (i) | YES — line 230 |
| `test_run_pm1_on_phase4_archive_returns_clusters_at_n34` | Gate (ii) | YES — line 295 |
| `test_pm1_surviving_kit_datas_count_equals_34` | Gate (ii) | YES — line 329 |
| `test_pm1_no_fallback_fires_at_n34` | Gate (ii) | YES — line 350 |
| `test_eight_element_coverage_preserved_post_path_x` | Gate (iii) | YES — line 387 |
| `test_element_distribution_not_s2_only` | Gate (iii) | YES — line 410 |

Five unenumerated tests (directly inspected):

| Test name | Scope | Gate coverage |
|---|---|---|
| `test_no_variant_row_in_kit_id_set` | Purity check: all kit_ids start with `S1_endgame_bc_` | Gate (i) extension |
| `test_mixed_sample_distribution_matches_gamora_enumeration` | s0=18, s1=9, s2=7 distribution exact match | Gate (i) extension |
| `test_run_phase5_cohesion_judge_accepts_path_x_pm1_result_in_smoke` | Backward-compat: smoke=True entry point does not raise | Backward-compat |
| `test_faction_clusters_input_plumbing_from_path_x_pm1_result` | Wave A / F-C / Wave B reachability: `pm1_result_to_faction_clusters_input` | Backward-compat |
| `test_fallback_fires_when_archive_empty` | Fallback: `phase4_accepted_kits=[]` sets `fallback_ref[0]=True` | Fallback contract |

All 12 test names match the gates they claim to cover. The five unenumerated tests add purity, distribution, backward-compat, and fallback coverage that the seven gate-named tests do not redundantly supply. No coverage gap found.

Disc #1.2 note: math note cited in docstring at line 31 (`simulation/math/cascade-r4-path-x-pm1-input-source-change-2026-05-29.md`) and in `_run_pm1_on_phase4_archive` docstring at line 663. Reference is to the simulation seam math notes directory. Not inspected (out of scope — code change already verified empirically per Gate (i)); citation exists and is structurally correct.

---

## INFO Items

### INFO 1 — k=4 held; gandalf caveat 1 did not materialize; benign downstream

Gandalf 2026-05-29 caveat 1 predicted "k may drop to 2 or 3" at n=34. Empirical result: k=4 (GMM BIC selected k=4; sparsity=none). Caveat was appropriately stated as EXPECTED/ACCEPTABLE; it did not predict k=4 as disallowed.

Downstream implication for star-lord Phase 5 cohesion judge: k=4 is the current cluster count. The cohesion judge fires against 4 clusters, which is the same cluster count as the pre-Path-X run (which was k=4 over 208 `_s2`-only members). Star-lord should be aware that k=4 is consistent but now over the correct population (34 Pareto-2 archive kits rather than 208 variant members). No re-design of the cohesion judge methodology is needed; the PROVISIONAL marker applies at the metric-axis layer, not the cluster-count layer.

Cite: Disc #11 (empirical over assumed); gandalf verdict § 2 Q3 (k drop expected, k=4 observed — within accepted range).

### INFO 2 — shadow=1, water=1 sparse; downstream cohesion-judge flag

Of the 8 elements in the 34-kit archive: shadow=1, water=1. These are single-kit elements. Each is assigned to exactly one kit in the gamora-enumerated set.

Downstream cohesion-judge implication: PM-1 cluster boundaries at k=4 will likely not isolate shadow or water as cluster-defining axes — they will fall into mixed clusters. The cohesion judge output (cluster labels, Wave B names) will be dominated by the higher-cardinality elements (physical=8, earth=6, fire=6, wind=5). This is informative for star-lord's cohesion judge interpretation: shadow and water archetype distinctiveness may be underrepresented in cluster taxonomy. Not a Path X regression (this is the Phase 4 archive composition); flagging for star-lord awareness.

No Cycle 15+ Path Y/Z action required before wave-close. This is a composition fact, not a structural defect.

Cite: dispatch § 2.1 Gate (iii) sparse-element surface instruction; gandalf 2026-06-01 verdict § 2 Q3 (8-element coverage smoke as regression check, not composition constraint).

---

## Disc #42a Q5 Adjudication — Line-Reference-Staleness Pattern

**Adjudication: DISCIPLINE-CANDIDATE — INFO.**

The stale line reference `wave5_season_orchestrator.py:825-836` propagated through four artifacts:
1. gandalf 2026-05-29 surface note (original correct reference at time of authoring)
2. star-lord pre-fire surface (commit `6593626`) — cited verbatim from gandalf surface
3. gandalf 2026-06-01 verdict (commits `05c1300` + `900c0bc`) — § 2 Q3 cited `825-836` as the check location
4. KR Path X dispatch authoring (commit `05374f8`) — gate (i) description cited `825-836`

rocket's empirical inspection caught the staleness: the actual Path X implementation is at Phase 4.5 (lines ~2622ff in `run_wave5_season_001`), not lines 825-836. Lines 1093-1114 (the Phase 3 PM-1 that lines 825-836 likely correspond to in an earlier file version) still exist but are the preserved-for-telemetry pass that Path X overrides. The reference was not wrong about WHERE the old assignment was; it was stale about WHERE Path X operates.

Orchestration outcome: clean (Gate (c) PASS via empirical state). rocket's Disc #11 empirical inspection was the correct and sufficient termination.

**Is this a discipline-candidate pattern?**

Yes. The pattern is: a line-reference in a design-intent document is cited verbatim into downstream dispatches and verdicts without re-verification at authoring time. The reference is load-bearing (it is the check criterion for Gate (i) code-level verification). When the code is restructured, the reference becomes stale while the downstream chain continues to treat it as precise.

This composes with Disc #42a Q5 (calibration-scope-match) but is better named as a distinct authoring-time discipline: **line-reference claims in cross-artifact citations require re-verification at the point of re-citation, not inheritance of the originating author's inspection.**

**Proposed framing for Disc #42a Q5 extension or new discipline candidate:**

> When a line-reference claim from a prior design surface is incorporated verbatim into a dispatch, verdict, or finding authored at a later point (post-code-restructure), the authoring agent must re-verify the line reference against the current codebase before citing it as a gate criterion. Verbal descriptions of behavior (e.g., "surviving_kit_datas reads Phase 4 archive") do not require re-verification at the same frequency as precise line references, because verbal descriptions remain true across refactoring while line references may not.

This is a candidate for: (a) a sub-clause under Disc #42a as Q5 operationalization, OR (b) a new Disc #42b "line-reference re-verification at re-citation." The choice between these is a jack-ryan canonical-write decision at wave-close. Surfacing here as INFO for KR and Matt visibility; the discipline candidate does not block this Gate-2.

Cite: Disc #42a (framing-audit); dispatch § 2.5; Disc #11 (rocket's empirical inspection was the correct termination — discipline to strengthen the upstream authoring chain, not the verification chain).

---

## Canonical-Write Candidates (informative, out of scope this dispatch)

Already queued per dispatch § 5:
- **Disc #41** substrate-led at validation-metric layer (recognition § 3.1 amendment candidate) — queued for jack-ryan canonical-write post wave-close
- **Disc #42a Q5 / #42b** line-reference-staleness at re-citation — surfaced above; queued for wave-close canonical-write

No new candidates identified this review.

---

## Action

- [x] All three empirical-criterion gates: VERIFIED by direct code inspection
- [x] Recognition-record § 4.2 structural-integrity preservation: VERIFIED
- [x] Principle 6 cross-seam impact + MIGRATION.md adequacy: VERIFIED
- [x] Test coverage: 12/12 names present; gate mapping confirmed; 5 unenumerated directly inspected
- [x] Disc #42a Q5 adjudicated: DISCIPLINE-CANDIDATE INFO — no block
- [ ] KR: re-invoke star-lord Phase 5 cohesion judge dispatch with Gate (c) PASS confirmation
- [ ] KR / star-lord: carry INFO 2 (shadow=1, water=1 sparse) into cohesion judge context
- [ ] jack-ryan wave-close canonical-write: Disc #41 substrate-led amendment + Disc #42a Q5 / #42b line-reference discipline candidate

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` — lines 639-708 (`_run_pm1_on_phase4_archive`), 1093-1114 (Phase 3 PM-1), ~2622-2664 (`run_wave5_season_001` Phase 4.5), ~3048-3079 (`run_season_production` Phase 4.5)
- `/Users/admin/Games/reincarnated-engine/tests/test_wave5_swift_closure_path_x_phase4_feeds_phase5.py` — all 12 test methods inspected
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` — [2026-06-01] entry lines 8-86
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/rocket/notes/2026-06-01-wave-5-swift-closure-path-x-complete.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-01-gate-c-recognition-record-intent-verdict.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-29-phase-4-phase-5-disjoint-population-bug-surface.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-06-01-wave-5-swift-closure-archive-snapshot-stable.md`
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md` § 4.2
