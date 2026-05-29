# Gamora Analysis Note — Cascade-R3 Instance 6 #5: Phase 7 Join Logic + 13/54 Mechanical Gate + Sample Distribution

**Date:** 2026-05-29 (evening late)
**Author:** gamora (engine simulation seam)
**Authority:** Dispatch `2026-05-29-gamora-cycle-14-cascade-resumption-3-instance-6-5-phase3-mechanical-gate-13-54-analysis.md` + gandalf URGENT REDIRECT directive (commit `e466c26`)
**Companion investigations:** rocket (CLOSED `764e732`) + jack-ryan (CLOSED `eb14ec3`)
**Disciplines applied:** #11 (empirical inspection), #18 (math hotspot consultation), #41 (substrate-led), #42a (framing-audit Q1-Q6), #45 (vocabulary lock)

---

## § 1 — Phase 7 Join Logic + `shipped_worthy=22` Computation (PRIMARY REDIRECT QUESTION)

### 1.1 Empirical verification

Phase 7 evaluates the 34 ACTIVE `kit_archive` rows (Phase 4 Pareto-2 output). It produces verdicts per kit per cohort assignment. The `season_summary.json` reports `kits_evaluated=34, kits_shipped_worthy=22, kits_held_mechanical=12`.

**How `shipped_worthy=22` is computed:**

The `phase7_kit_verdict_log` contains 109 records for `season_id='cycle-14-wave-5-season-001'`, `evaluation_attempt=0`. This is because each kit is evaluated against its per-cohort `cohort_midpoint` (derived from this run's gauntlet pass-rate distribution). Multiple verdict records per kit are possible (Phase 7 evaluates each kit once per `evaluate_kit_verdict` call; the 109 count reflects multi-run accumulation across retries and legacy rows in the DB). The `season_summary.json` count (22) is the count of **distinct ACTIVE kit_archive kit_ids with at least one `SHIPPED-WORTHY` verdict** in this season.

Cross-reference: `JOIN kit_archive ON verdict_log WHERE archive_status='ACTIVE' AND verdict='SHIPPED-WORTHY'` returns **22 unique kit_ids**. This matches exactly.

### 1.2 Cohesion pass for sparse Phase 5 members

The 22 shipped kits have the following cluster_id distribution:

| cluster_id | count | cohesion_score present |
|---|---|---|
| NULL | 19 | 0 (all None) |
| 1 | 1 | None |
| 4 | 2 | 0.85, 0.78 (Wave B populated) |

**Key mechanism — `evaluate_cohesion_pass()` in `phase7_verdict.py` lines 199-200:**

```python
# If cohesion_score is None: skip cohesion evaluation → cohesion pass assumed
# (faction_visibility=invisible; no Phase 5 output produced).
if cohesion_input.kit_level_cohesion_score is not None:
    if cohesion_input.kit_level_cohesion_score < P7_KIT_COHESION_SCORE_FLOOR:
        return False, "C1"
```

When `kit_level_cohesion_score is None` (kit not in Wave B results), the C-1 check is **skipped**. Cohesion_pass defaults to True for the per-kit gate.

Similarly for `cluster_compactness`:
- If `cluster_compactness is None` (kit not in any Phase 5 cluster), C-2 check is skipped.
- If `diversity_flag is None`, C-3 check is skipped.

**Operational result:** Kits with `cluster_id=NULL` have `cohesion_score=None`, `cluster_compactness=None`, and `diversity_flag=None`. All three cohesion conditions skip → `cohesion_pass=True` by implicit default.

### 1.3 Cluster_cohesion dict construction

The `cluster_cohesion` dict is built from `clusters_dicts` (Phase 5 PM-1 output). For each cluster, it stores `{member_kit_ids: [...], compactness, diversity_flag, phase7_gate_status, regeneration_fired}`. Phase 7 bridge looks up each kit_id against `member_kit_ids` lists — if the kit_id does not appear in any cluster's `member_kit_ids`, `cluster_id=None` and all cluster-level cohesion fields remain None.

The 19 kits with `cluster_id=NULL` are s0/s1 kits (plus one s2 kit `_ranged_low_spiky_str_none_s2`) that do NOT appear in any Phase 5 cluster's `member_kit_ids`. Phase 5 PM-1 operated on 598 input members (all `_s2` suffix), so s0/s1 kits from the Phase 4 archive are absent from all clusters. They receive implicit `cohesion_pass=True`.

### 1.4 Interpretation A vs B resolution

**VERDICT: Interpretation A — parallel-by-design, with implicit cohesion default.**

The Phase 7 code path confirms: Phase 4 archive feeds Phase 7 mechanical gate (kit_archive.db); Phase 5 PM-1 feeds Phase 7 cohesion gate (cluster membership lookup). These are PARALLEL inputs to Phase 7, not a sequential chain. Phase 7 does not REQUIRE both gates strictly — it requires mechanical_pass AND cohesion_pass, but cohesion_pass defaults to True when Phase 5 cohesion data is absent for a kit.

**Specific finding:** 19 of 22 shipped kits received `cohesion_pass=True` via implicit None-skip (not via explicit Phase 5 cluster membership). Only 3 of 22 shipped kits appear in Phase 5 clusters. This means 86% of shipped kits have no explicit faction assignment, receiving a pass-through on the cohesion gate.

**Interpretation B refutation:** The code comment at `wave5_season_orchestrator.py:1820-1824` explicitly anticipates "variants inherit base kit cohesion_data... variant kit_ids not present in wave_b_results → Phase 7 uses None → cohesion skipped." The None-skip is a documented design pattern for the Cycle 14 v1 `faction_visibility=invisible` state.

**Secondary finding — cohesion_pass=1 for kits with cluster_id=NULL in the verdict log:** This is correct behavior, not a defect. The `evaluate_cohesion_pass()` function returns `(True, None)` when all three fields (cohesion_score, cluster_compactness, diversity_flag) are None. This is the intended placeholder-mode pass-through per `phase7_verdict.py` docstring.

---

## § 2 — 13/54 Base Pass Rate Root Cause Analysis

### 2.1 Structural decomposition

**Total base kits:** 54 (18 BC cells × 3 substrate samples s0/s1/s2 per Amendment 6/7)

**Pass breakdown:**
- **13/54 base kits have `wr_bracket_pass=True`** (all s2-suffixed)
- **41/54 base kits have `wr_bracket_pass=False`**

The 41 failures decompose into two distinct causes:

**Cause A — config_to_kit collision (rocket finding confirmed):** For 13 passing BC cells, only the s2 sample receives `wr_bracket_pass=True`. The s0 and s1 samples for those cells receive `wr_bracket_pass=False` due to `w5r2_gauntlet_sim_integration()` dict-overwrite at `season_generation_pipeline.py:1424-1428`. This accounts for **13 × 2 = 26 kits** with `wr_bracket_pass=False`.

**Cause B — t4_candidates=0 for 5 failing BC cells:** The other 5 BC cells (`endgame_bc_melee_high_flat_int_none`, `endgame_bc_mid_high_flat_dex_none`, `endgame_bc_mid_low_spiky_int_none`, `endgame_bc_ranged_low_spiky_dex_none`, `endgame_bc_ranged_low_spiky_str_none`) have `t4_candidates_count=0` for their s2 kit. With no T4 candidates, no `legendary_id` strings are generated, and no `kit_result` records are produced in Phase 3 gauntlet. These 5 cells are absent from `phase3_gauntlet_results.json:kit_results` (13 unique cells, not 18). Their `wr_bracket_pass` remains False for all 3 samples. This accounts for **5 × 3 = 15 kits** with `wr_bracket_pass=False`.

**Summary:**
| Cause | Affected kits | `wr_bracket_pass=False` |
|---|---|---|
| config_to_kit collision (s0+s1 overwritten) | 13 cells × 2 samples | 26 kits |
| t4_candidates=0 (no T4 chains for cell) | 5 cells × 3 samples | 15 kits |
| Passing (s2 of 13 passing cells) | 13 cells × 1 sample | 13 pass |
| **Total** | **54 kits** | **41 fail / 13 pass** |

### 2.2 Verdict on 13/54 root cause

**Verdict category (per dispatch § 0): (A) + (B) combined**

- **(A) Expected behavior per Amendment 6 Sub-fix 1 `cell_any_pass` inheritance logic** — The 13/54 is consistent with Amendment 6 Sub-fix 1 design: cell_any_pass=True for the 13 cells, False for the 5 t4-empty cells. This is expected architecture given the constraint.
- **(B) Phase 3 mechanical gate calibration tighter than expected** — DOES NOT APPLY. The 13/54 is not caused by gate calibration. All 13 cells that produced valid T4 kits (s2 specifically) passed the gauntlet: `phase3_gauntlet_results.json` shows `season_emit=True` for 65 of 66 kit_results (the single fail is `endgame_bc_melee_medium_variable_str_none_t4_chain_1`). The mechanical gate is NOT over-tight; the rate-limiter is the config_to_kit collision and the t4-empty cells.
- **(C) Substrate-distinct systematic failure** — DOES NOT APPLY as primary cause. The 5 failing cells span multiple substrates/elements. The failure is structural (t4_candidates=0) not substrate-driven.

### 2.3 Per-cell BC axis distribution of 13 passing kits (s2 only)

| bc_range | bc_tempo | bc_amplitude | bc_attribute | Passing cells |
|---|---|---|---|---|
| melee | high | flat | dex | 1 |
| melee | high | flat | str | 1 |
| melee | high | variable | wis | 1 |
| melee | low | spiky | str | 1 |
| melee | medium | variable | str | 1 |
| melee | medium | variable | wis | 1 |
| mid | medium | variable | wis | 1 |
| ranged | high | flat | dex | 1 |
| ranged | low | spiky | int | 1 |
| ranged | low | spiky | wis | 1 |
| ranged | medium | variable | int (light) | 1 |
| ranged | medium | variable | int | 1 |
| ranged | medium | variable | wis | 1 |

5 absent cells (t4_candidates=0): `endgame_bc_melee_high_flat_int_none`, `endgame_bc_mid_high_flat_dex_none`, `endgame_bc_mid_low_spiky_int_none`, `endgame_bc_ranged_low_spiky_dex_none`, `endgame_bc_ranged_low_spiky_str_none`.

No substrate-systematic pattern in the 5 absent cells: they span int/dex/str attributes and melee/mid/ranged ranges.

---

## § 3 — Sample Distribution in passing_kits + Phase 4 Archive Comparison

### 3.1 Passing_kits (Phase 3 WR-bracket output)

- Total passing_kits: **13** (all s2 suffix)
- Total variant_passing_rows: **585** (13 cells × 45 variants each; cell_any_pass=True inherited from s2)
- PM-1 input: 13 + 585 = **598**

### 3.2 Phase 4 archive distribution vs config_to_kit collision

Phase 4 Pareto-2 operates on ALL 54 base kits (not just the 13 WR-passing s2 kits). The Pareto-2 partition uses (bc_cell_id, cultural_lineage_canonical) as partition key. It accepts the highest-quality non-dominated kits per partition.

**Archive composition: s0=18, s1=9, s2=7 (total 34)**

This is NOT contradicted by the rocket config_to_kit collision finding. The Pareto-2 gate is independent of `wr_bracket_pass`:
- **s0=18:** For 18 BC cells, the s0 kit was Pareto-accepted (highest quality vector in its partition bucket). s0 kits have `wr_bracket_pass=False` due to config_to_kit collision, but Pareto-2 operates on quality_vectors (q1-q5), not WR bracket status.
- **s1=9:** For 9 BC cells, the s1 kit was the Pareto-winner in its lineage partition.
- **s2=7:** For 7 BC cells, the s2 kit was the Pareto-winner. Note: 13 cells had s2 WR-passing, but only 7 s2 kits won the Pareto-2 competition (others were dominated by s0 or s1 on quality dimensions).

**Reconciliation with config_to_kit collision:** The collision only affects `wr_bracket_pass` propagation. Phase 4 Pareto-2 uses quality_vectors (q1-q5, derived from gauntlet metric performance), which are computed independently from the `wr_bracket_pass` mechanism. The quality_vectors were derived at neutral 0.5 for most kits (based on `phase3_quality_vectors.json` values), so the Pareto-2 selection reflects proximity-to-optimal across the population, not WR bracket status. This is why s0=18 and s1=9 entered Phase 4 archive despite having `wr_bracket_pass=False`.

**Variants all rejected from Phase 4:** 585 variants → 0 accepted. Per rocket finding: MG-3 (Mahalanobis nearest-neighbor gate) flags all variants as `inferior_duplicate` because variant quality_vectors are identical to their parent base kit (T4 strategy + invest_profile overlays don't enter the q1-q5 vector). This is expected behavior per Amendment 6 Sub-fix 2 design.

### 3.3 cell_any_pass inheritance verification (Amendment 6 Sub-fix 1)

The `_build_variant_kit_rows()` function at `wave5_season_orchestrator.py:536-544` builds `cell_any_pass` as:
```
cell_any_pass[cell] = True if any base kit has wr_bracket_pass=True for that cell
```

For 5 failing cells (t4_candidates=0): all 3 samples have `wr_bracket_pass=False` → `cell_any_pass[cell]=False` → 0 variants for those 5 cells enter `variant_passing_rows`.

For 13 passing cells: s2 has `wr_bracket_pass=True` → `cell_any_pass[cell]=True` → all 45 variants per cell inherit `wr_bracket_pass=True`.

**Verification: 585 = 13 cells × 45 variants per cell. Confirmed correct per phase4_archive_insertion.json.**

**Amendment 6 Sub-fix 1 cell_any_pass is functioning per spec.** Variants from the 5 failing cells are correctly excluded.

---

## § 4 — Path X PM-1 Sparsity Verification at n=34

### 4.1 PM-1 sparsity branch constants (phase5_pm1_multimodal_clustering.py)

```python
SPARSITY_TIER_GMM_BIC: int = 24      # n >= 24: GMM k∈{3,4} BIC-selected
SPARSITY_TIER_GMM_K3:  int = 20      # 20 <= n < 24: GMM k=3 fixed
SPARSITY_TIER_KMEANS_K3: int = 12    # 12 <= n < 20: k-means k=3 fallback
SPARSITY_TIER_KMEANS_K2: int = 8     # 8  <= n < 12: k-means k=2 degraded
```

### 4.2 Path X input: n=34

If Phase 5 PM-1 input = Phase 4 archive output (34 kits), then n=34 >= SPARSITY_TIER_GMM_BIC (24).

**Result: GMM BIC sweep at k∈{3,4} applies.** No degenerate fallback triggered. The degenerate k-means fallback requires n < 20. At n=34, GMM_BIC is the selected algorithm.

### 4.3 Expected cluster count at n=34

Current: n=598, k=4 (GMM_BIC_selected). At n=34, the BIC sweep selects k based on data geometry. The 34 Phase 4 archive kits span all 8 elements (per rocket Amendment 7 smoke verification at commit `8d5be1b`) and 5 cultural lineages. With a smaller, quality-selected population, the cluster count may drop from k=4 to k=3 (the BIC sweep evaluates k=3 and k=4; at n=34, fewer distinct clusters may be statistically supported).

**Assessment:** k=3 or k=4 both viable at n=34 via GMM_BIC. No degenerate fallback. The sparsity_flag will be `none` (not `SEASON_SPARSE`). This is the same sparsity tier as the current n=598 run.

**Downside of Path X (confirmed):** The variant-population substrate for cluster boundary inference is lost. Current n=598 (13 base s2 + 585 variants) provides richer coverage of investment-profile and strategy diversity. n=34 (34 quality-selected mixed-sample kits) provides more coverage of substrate diversity (s0/s1/s2 elements), but less T4-strategy coverage. The clusters at n=34 may be more element-homogeneous and less strategy-diverse than current n=598 clusters.

### 4.4 PM-1 sparsity verdict for Path X

| Metric | Current (n=598) | Path X (n=34) |
|---|---|---|
| n vs GMM_BIC threshold (24) | 598 >> 24: PASS | 34 > 24: PASS |
| Algorithm | GMM_BIC_selected (k=4) | GMM_BIC_selected (k=3 or k=4) |
| Degenerate fallback | Not triggered | Not triggered |
| Sparsity flag | none | none |
| Cluster count projection | k=4 (actual) | k=3 or k=4 (BIC-determined) |

**Path X is viable at n=34.** No sparsity degradation at the algorithm-selection layer.

---

## § 5 — Recommendations for Gandalf Path X/Y/Z Decision

### 5.1 Interpretation A confirmed: parallel-by-design with implicit cohesion default

Phase 7 ships kits with `cluster_id=NULL` via the implicit cohesion-pass-through (None-skip in `evaluate_cohesion_pass()`). The 22 shipped kits break down as:
- **19 kits: cohesion_pass=True via implicit None-skip** (cluster_id=NULL; no Phase 5 membership; cohesion check skipped)
- **3 kits: cohesion_pass=True via explicit Phase 5 membership** (cluster_id=1 or 4; 2 of these have Wave B cohesion scores)

This is Interpretation A: Phase 4 → Phase 7 and Phase 5 → Phase 7 are parallel, meeting at Phase 7. The current architecture works, but the cohesion gate is operating mostly in placeholder mode (86% of shipped kits have no faction assignment or cohesion score).

### 5.2 Path recommendations

**Path X (Phase 5 PM-1 input = Phase 4 archive output, n=34):**
- VIABLE at algorithm level (GMM_BIC, no degenerate fallback)
- Strongest architectural coherence: 100% Phase 4 ∩ Phase 5 overlap; all shipped kits from Phase 7 would have faction membership
- 8-element coverage preserved (per rocket Amendment 7 verification)
- Cluster count may drop k=4 → k=3; acceptable per BIC selection
- Implementation cost: ~1-2hr rocket (per gandalf estimate confirmed)
- **RECOMMENDED if the design intent is faction assignment for all shipped kits**

**Path Y (extend variants to s0/s1/s2 samples):**
- Requires fixing config_to_kit collision first (rocket Instance 6 #6 candidate)
- PM-1 input grows ~50% (598 → ~750 estimated)
- Does not unify Phase 4 → Phase 5 conceptually; parallel architecture persists
- Higher LLM cost for Wave B
- **Deferred recommendation: address config_to_kit collision as standalone fix first**

**Path Z (variants enter Phase 4 via Pareto-2 insertion):**
- Currently `variant_accepted_count=0` due to MG-3 identical-quality-vector rejection
- Requires new variant accept/reject criterion; non-trivial spec change
- **Not recommended for Cycle 14 v1**

### 5.3 config_to_kit collision (rocket Instance 6 #6 surface)

The config_to_kit collision is a SEPARATE issue from the Phase 4 → Phase 5 disconnect. The collision means s0/s1 kits are invisible to WR-bracket evaluation. Fix cost is low (~45-90min per rocket estimate), but the design question must be resolved first: "Should all 3 substrate samples per WR-bracket-passing BC cell enter PM-1?" This is a gandalf/matt design call, not a code-level fix.

### 5.4 The 13/54 pass rate is not a calibration concern

The 13/54 base pass rate is structurally determined by:
1. config_to_kit collision (only s2 can pass per cell)
2. t4_candidates=0 for 5 BC cells (structural absence of T4 chains)

Neither is a calibration issue. The Phase 3 WR bracket gate itself is well-calibrated: 65/66 chain-level gauntlet runs produce `season_emit=True`. The effective base kit pass rate at the character_id level would be ~13/18 (~72%) if the config_to_kit collision were fixed (only the 5 t4-empty cells would remain failing).

---

## § 6 — Surface-to-KR Findings

### 6.1 No new Phase 3 gate calibration concerns

The Phase 3 mechanical gate is functioning correctly per the gamora `496814b` fix. The 13/54 rate is a structural consequence of config_to_kit collision + t4_candidates=0 cells, not gate miscalibration.

### 6.2 Cohesion gate operating in implicit pass-through mode

**Surface condition:** 19 of 22 shipped kits have `cohesion_pass=True` via None-skip (cluster_id=NULL, cohesion_score=None, compactness=None). These kits ship without any verified faction membership or cohesion judge evaluation.

This is documented Cycle 14 v1 behavior (`faction_visibility=invisible` placeholder mode per `phase7_verdict.py` docstring). NOT a bug. However, it means the cohesion gate is largely non-operative for this production run. If Path X is adopted, all 34 Phase 4 kits would have faction assignment, and the cohesion gate would operate at full binding strength for future runs.

### 6.3 Summary for gandalf Path decision

| Question | Finding |
|---|---|
| shipped_worthy=22 computation | Distinct ACTIVE kit_ids with SHIPPED-WORTHY verdict; 19/22 via implicit cohesion pass-through |
| Interpretation A vs B | **A confirmed: parallel-by-design with implicit cohesion default** |
| 13/54 root cause | config_to_kit collision (26/41 fails) + t4_candidates=0 (15/41 fails) |
| Phase 4 archive s0=18/s1=9/s2=7 consistent with collision? | YES: Pareto-2 is independent of WR bracket; s0 kits dominate quality-wise |
| Path X PM-1 sparsity at n=34 | GMM_BIC viable; no degenerate fallback; k=3 or k=4 BIC-selected |
| Amendment 6 Sub-fix 1 cell_any_pass functioning | CONFIRMED: 585 variants = 13 cells × 45; 5 t4-empty cells correctly excluded |

---

**Analysis note authored by:** gamora, 2026-05-29 evening late
**Collab commit:** (see dispatch completion record)
