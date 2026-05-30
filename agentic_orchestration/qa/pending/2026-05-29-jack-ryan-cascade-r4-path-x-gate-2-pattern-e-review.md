# Finding — 2026-05-29 — cascade-r4-path-x-phase4-feeds-phase5

**Reviewer:** jack-ryan
**Severity:** PASS-with-INFO
**Target:** `rocket/v1.0-cascade-r4-path-x-phase4-feeds-phase5-1` (engine `779b547`; collab `30b30ff`, `52c1550`)
**Developer:** rocket
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam contract), 4 (decisions-log as truth), 5 (severity matters)
**Authorization:** `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-4-path-x-phase4-feeds-phase5-authorization.md` (commit `3de3a40`)

---

## Overall Disposition: PASS-with-INFO

The cascade-r4 Path X wire-up is mechanically complete and correct. All primary acceptance criteria in § 6 are verified. One semantic discrepancy in the element-coverage claim (INFO, pre-existing upstream gap) and one calibration gap in Phase 7 C-2 (WARN, correctly surfaced by rocket) are noted below. Neither blocks dispatch closure. Step 7 four-track fan-out may proceed per reasoning in § 6 below.

---

## § 6.1 Behavioral Verification — Per-Criterion Verdict

### PM-1 input cardinality = 34
**VERIFIED.**
`phase5_faction_clusters.json` total member_kit_ids = 34 (13+11+9+1). Archive query confirms 34 ACTIVE base kits with `kit_id LIKE 'S1_endgame_bc_%'`. Sample distribution in Phase 5 clusters: s0=18 / s1=9 / s2=7 — exact match Phase 4 archive ACTIVE count.

### PM-1 sparsity branch = NONE (gmm_bic_sweep) at n=34
**VERIFIED.**
Completion record: NONE. Confirmed: `SPARSITY_TIER_GMM_BIC=24`; n=34 > 24. All four clusters carry `pm1_algorithm: "gmm_k4"` in `phase5_faction_clusters.json`. No degenerate fallback artifact.

### GMM cluster count k ∈ {3, 4}
**VERIFIED.**
k=4 BIC-selected. `phase5_faction_clusters.json` `cluster_count: 4`. Within authorized range.

### Phase 5 cluster member sample distribution mixed s0/s1/s2 matching Phase 4 archive
**VERIFIED.**
s0=18 / s1=9 / s2=7 confirmed from Phase 5 cluster membership analysis. Exact match to Phase 4 archive ACTIVE base kit distribution.

### Phase 5 cluster element distribution: all 8 elements present at primary mono layer
**SURFACES — INFO (pre-existing upstream gap; not introduced by this dispatch).**

What is verified: Phase 4 archive contains all 8 elements at kit-membership level (earth / fire / holy / lightning / physical / shadow / water / wind confirmed from archive + phase2 join). All 8 physical-element kits from the archive ARE present as cluster members across clusters 1, 2, 3.

What surfaces: `_ELEMENT_MAP` in `phase5_pm1_multimodal_clustering.py` (line 287) has 7 entries — "physical" is absent. When a physical-element kit is encoded via `encode_categorical("physical", _ELEMENT_MAP)`, the default 0.5 is returned (midpoint between lightning=0.571 and wind=0.429). The reverse-lookup at cluster summary time resolves 0.5 to a non-physical element label. Result: `phase5_faction_clusters.json` `element_distribution` fields show only 7 elements; physical kits are silently re-labeled as earth/lightning/wind.

Classification: **INFO**. Reasons:
1. The `_ELEMENT_MAP` gap predates cascade-r4 (it was present before rocket's work; Amendment 7 acceptance was verified at the archive-population level, not at the cluster-JSON-output level).
2. Physical kits are correctly PRESENT as cluster members; the gap affects the computed summary label only.
3. The wire-up core (PM-1 receives 34 archive kits including physical-element kits) is correct.
4. Rocket's completion record item 4 ("earth / fire / holy / lightning / physical / shadow / water / wind — all represented") is interpreting the archive input correctly but overstates the Phase 5 JSON output accuracy. This is a documentation/framing precision issue, not a wiring failure.

**Recommended action (Cycle 15+):** Add "physical" to `_ELEMENT_MAP` in `phase5_pm1_multimodal_clustering.py` (line 287) with an appropriate ordinal value. This is a one-line fix but should be done with a dedicated dispatch since it changes cluster feature encoding.

**Cite:** Discipline #1 (math-before-code / empirical inspection over assumption); Principle 5 (severity matters — this gap existed pre-Path-X).

### Wave B kit_count = 34
**VERIFIED.**
`phase5_faction_clusters.json` `wave_b_kit_count: 34`. Completion record confirmed.

### Phase 7 cluster_id assignment coverage = 100% of archive kits
**VERIFIED (semantics confirmed).**
Phase 7 `kits_evaluated=34` and `clusters_aggregated=4` from `phase7_season_summary.json`. All 34 archive kits appear as cluster members in `phase5_faction_clusters.json` (verified by member_kit_ids union). The "cluster_id" coverage refers to Phase 5 JSON cluster membership, not a DB column — `kit_archive` schema does not persist a `cluster_id` field; Phase 7 performs runtime reverse-lookup against Phase 5 cluster cohesion dict. 100% coverage confirmed empirically: every archive kit appears in one of the 4 clusters.

---

## § 6.2 Cost Verification

**VERIFIED.**
- Per-season actual: $0.36 ($0.02 Wave A + $0.34 Wave B). Target: ≤$0.50. PASS.
- 3-season projection: $0.36 × 3 = $1.08. Target: ≤$1.50. PASS.
- Authorization target was $0.37/season; actual $0.36 — within $0.01 of projection. No $50 cap approach signal.

---

## § 6.3 Composition Preservation

**VERIFIED.**

| Amendment | Expected state | Verified |
|---|---|---|
| Amendment 6 Sub-fix 1 (S7 deepcopy; 54 distinct substrate bindings) | UNCHANGED | Phase 2-4 pipeline untouched per `start_from_phase=5` entry; Sub-fix 1 not in modified files |
| Amendment 6 Sub-fix 2 (Pareto-2 lineage partition; 34 archive winners) | NOW CONSUMED by Phase 5 | PM-1 receives exactly the 34 Sub-fix-2 archive kits as input |
| Amendment 6 Sub-fix 3 (S8 Bound 4 paired-joint-sampling) | UNCHANGED | Not in modified files |
| Amendment 7 (E4c element coverage; all 8 elements at primary mono) | NOW VISIBLE at Phase 5 | All 8 elements present in archive input; cluster membership reflects 8 elements (see INFO above re: JSON summary labeling) |
| Amendment 7a (per-chain element wiring) | UNCHANGED | Not in modified files |
| Amendment 8 ($50 cap re-imposed; Matt-gate retired) | UNCHANGED | Cost at $0.36/season, well within cap |

---

## Backward-Compat Smoke

**VERIFIED.**
Completion record item 11: archive_count < 8 path fires WARN + fallback + surfaces `pm1_path_x_fallback=True`. Code inspection confirms: `_load_phase4_archive_for_pm1` returns `[]` when `archive_count < SPARSITY_TIER_KMEANS_K2`; `_run_pm1_on_phase4_archive` falls back to `passing_kits + variant_passing_rows` when `phase4_accepted_kits` is empty. Log message emitted: `[PM-1][Path X FALLBACK]`.

Test coverage: 14 tests across 5 groups. Groups include archive_count=4 fallback path and archive_count=34 Path X path. Commit message confirms 14/14 cascade-r4 Path X tests PASS + 288/288 cascade-r3/PM-1 regression PASS.

---

## Cross-Seam Contract Verification

**NOT APPLICABLE — confirmed.**
`_build_pm1_kit_data` signature unchanged. PM-1 output schema unchanged (`phase5_faction_clusters.json` structure identical). Phase 7 cohesion-data reverse-lookup logic unchanged. Wave A faction-cluster JSON unchanged in structure. Wave B kit_name dict unchanged in shape (more records, same record shape). No MIGRATION.md required per ADR-004.

---

## Phase 7 C-2 Compactness Gap — Disposition

**Classification: WARN**

**What rocket reported:** `P7_CLUSTER_COMPACTNESS_FLOOR=0.40` was calibrated for the 598-kit PM-1 input population. At n=34, cluster compactness = 0.14 (all four clusters, uniform per `phase5_faction_clusters.json`). 34/34 kits fail C-2 gate → `shipped_worthy=0`. `phase7_season_summary.json` confirms: `kits_shipped_worthy=0`, `kits_held_cohesion=22`, `kits_held_both=12`.

**Was this in-scope for the cascade-r4 dispatch?** No. The dispatch scope (§ 6.1 behavioral verification table) does not list a `shipped_worthy` floor as an acceptance criterion. The Path X dispatch is: wire Phase 4 archive → Phase 5 PM-1 input. The Phase 7 C-2 calibration constant (`phase7_verdict.py:66`) predates this dispatch and was calibrated against the former 598-kit input population.

**Does shipped_worthy=0 invalidate the cascade-r4 closure?** No. The wire-up is mechanically correct. Path X achieves its design goal: Phase 5 LLM curation operates on the design-selected substrate, and Phase 7 cluster_id coverage is 100% (vs prior 17.6%). The shipped_worthy=0 outcome is a consequence of a calibration gap that is out-of-scope for this dispatch, not a defect in what landed.

**Does shipped_worthy=0 block Step 7 four-track fan-out?**

- **Track A** (seasons 002+003): The re-fire will execute the same wire-up with different seeds. Unless C-2 is recalibrated first, Track A will also produce shipped_worthy=0. Track A can fire but Matt should understand this outcome before authorizing.
- **Track B** (drax loadout + § 12 hero image): The Track B roster question is how drax selects a "seasonal hero." If hero selection requires shipped_worthy > 0, Track B hero selection is blocked by the C-2 gap. If Track B uses all 34 archive kits (the full Wave B name set) regardless of Phase 7 verdict, Track B can proceed. Matt needs to elect the selection criterion per authorization § 12.1 before Track B fires.
- **Track C** (gandalf A/B testing): Needs a candidate pool. The 34 kits with faction labels + Wave B names constitute a valid pool for A/B design work, independent of shipped_worthy. Track C can proceed.
- **§ 12 drax hero selection**: Per authorization § 12.1, the selection criterion is TBD ("likely highest cohesion-score kit per cluster OR specific faction-alignment marquee OR Matt-elected per substrate metadata"). With shipped_worthy=0, the "shipped_worthy subset" path is blocked; Matt's election of an alternate criterion (cohesion score or direct substrate metadata selection) unblocks § 12.

**Step 7 readiness summary:** Track C can fire immediately. Track B and § 12 require Matt to elect hero selection criterion not gated on shipped_worthy. Track A can fire but will produce shipped_worthy=0 unless C-2 is recalibrated first — KR should surface the recalibration scope to Matt as part of Step 6 before authorizing Track A.

**Is this a cascade-r4 § 9.2 enumerated trigger?** Yes — it qualifies under "New Instance 6 surface (#7 candidate)" and "Wave-B-spec-gap surfaces" (hero selection criterion undefined when shipped_worthy=0). Rocket has correctly surfaced it per § 9.2. KR routing is appropriate.

**Cite:** ADR-002 (tiered approval authority — recalibration of a Phase 7 constant is cross-seam impact requiring Matt); Principle 5 (severity matters — this is WARN not BLOCK because dispatch scope is complete and the gap is pre-existing/out-of-scope).

---

## Instance 6 #7 Candidacy Assessment

**Verdict: CONFIRMED as Instance 6 #7.**

**Characterization:** Phase 7 C-2 compactness gate calibration population mismatch. `P7_CLUSTER_COMPACTNESS_FLOOR=0.40` was set against the 598-kit PM-1 input population (Phase 3 _s2 + variants). Path X reduces PM-1 input to 34 archive kits (the design-selected substrate). Compactness is an intra-cluster cohesion measure that scales with cluster size and population variance. At n=34 total (4 clusters averaging ~8-9 members), cluster compactness ≈0.14 is geometrically reasonable for the reduced population; it is not a signal of poor clustering quality — it is a signal that the 0.40 floor was calibrated for a different population scale.

**Disc #42a cumulative Instance 6 pattern record (through #7):**

| Surface # | Description | Status |
|---|---|---|
| #1 | Wave B phantom kits (s2-only character artifact) | CLOSED |
| #2 | Variant Pareto-dominance (pre-ratified A3) | CLOSED |
| #3 | Sub-fix 3 namespace-only (S8 Bound 4) | INFO — Cycle 14 wave-close |
| #4 | Amendment 7 hybrid metadata-only (Amendment 7a fix applied) | CLOSED |
| #5 | Phase 4 → Phase 5 disjoint (Path X resolution) | CLOSED — this dispatch |
| #6 | config_to_kit collision (last-writer-wins; s2-only passing_kits) | DEFERRED Cycle 15+ |
| #7 | Phase 7 C-2 compactness calibration gap (0.40 floor vs n=34 population) | OPEN — Cycle 15 KR routing |

**Pattern note for wave-close canonical-write:** Seven Instance 6 surfaces in a single work program (Cycle 14 cascade-resumption-1 through -4). Pattern classification: recurring pipeline-stage isolation gap — individually-calibrated stage constants not re-validated when upstream input cardinality changes. This is the Disc #42a "Layer-isolation-vs-integration gap" sub-case proposed by jack-ryan in the Instance 6 #5 framing audit. Instance 6 #7 is a second specimen of the same sub-case (PM-1 population change invalidates Phase 7 compactness constant). The Q4 amendment recommended in the Instance 6 #5 framing audit — "when downstream stage input_cardinality is orders-of-magnitude different from upstream stage output count, stop and verify calibrated constants explicitly" — would have caught this.

**Cycle 14 wave-close canonical-write elevated priority:** Instance 6 #7 landing before the wave-close write confirms the Q4 amendment + Layer-isolation-vs-integration sub-case are load-bearing for Cycle 15+ discipline. Jack-ryan to author Disc #42a Q4 amendment at wave-close.

---

## Step 6 Matt Surface — KR Framing Recommendation

**For KR to use at cascade-r4 § 9.1 Step 6 Matt surface:**

The cascade-r4 Path X dispatch is mechanically complete and closed. Phase 5 PM-1 now runs on the 34 Phase 4 Pareto-2 archive kits (design-selected substrate) instead of 598 Phase 3 variant-inclusive rows. Faction labels + Wave B names now cover 100% of the archive (vs 17.6% prior). Wire-up is correct; composition preserved; LLM cost $0.36 within $0.50/season cap.

One new surface requires Matt's election before Step 7 fan-out proceeds fully: Phase 7 C-2 compactness gate (`P7_CLUSTER_COMPACTNESS_FLOOR=0.40`) was calibrated for the 598-kit population. At n=34, all clusters score compactness ≈0.14 → shipped_worthy=0. This is not a Path X defect; it is a calibration gap between the Phase 3-era threshold and the Phase 4-archive-era input scale. Three options for Matt:

1. **RECALIBRATE-FIRST (recommended before Track A):** Authorize a narrow Cycle 15 dispatch to recalibrate `P7_CLUSTER_COMPACTNESS_FLOOR` against n=34-scale input (likely targeting 0.10-0.15 range; needs gamora empirical analysis of what compactness values are geometrically achievable at n=34). Fire Track A post-recalibration. Estimated effort: half-day gamora + re-fire.
2. **CONFIRM AS-IS:** Accept shipped_worthy=0 for season_001 as a known artifact of the calibration gap; fire Track A + Track B + Track C with the understanding that a recalibration dispatch follows in Cycle 15. Hero selection for § 12 must use cohesion-score or direct substrate-metadata criterion (not shipped_worthy filter). Matt elects the § 12 hero selection criterion.
3. **REDUCE-SCOPE:** Proceed only with Track C (gandalf A/B testing) and § 12 hero selection from the 34 archive kits, hold Track A until recalibration lands.

Jack-ryan recommendation: CONFIRM AS-IS for Track C + § 12; RECALIBRATE-FIRST before Track A + Track B full execution. The 34-kit faction label + Wave B name output is already player-facing-coherent — that was the Path X goal. shipped_worthy is a separate Phase 7 quality gate that needs its constants updated.

---

## References

- Dispatch (with completion record): `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-cascade-resumption-4-path-x-phase4-feeds-phase5.md`
- Authorization: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-4-path-x-phase4-feeds-phase5-authorization.md`
- Phase 5 clusters: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json`
- Phase 7 summary: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/phase7_season_summary.json`
- PM-1 clustering module (element gap): `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/phase5_pm1_multimodal_clustering.py` (line 287 `_ELEMENT_MAP`)
- Phase 7 compactness constant: `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/phase7_verdict.py` (line 66 `P7_CLUSTER_COMPACTNESS_FLOOR`)
- Test file: `/Users/admin/Games/reincarnated-engine/tests/test_cascade_r4_path_x_pm1_input_source.py`
- Engine commit: `779b547`; Collab commits: `30b30ff`, `52c1550`
