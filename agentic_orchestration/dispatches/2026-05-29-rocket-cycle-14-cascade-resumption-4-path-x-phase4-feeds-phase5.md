# Dispatch — 2026-05-29 — rocket — cascade-resumption-4 Path X (Phase 4 archive → Phase 5 PM-1 wire-up + season_001 re-fire)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-29 evening late ("Path X — fire cascade-resumption-4" verbatim + "yes, option (i)" Wave B scope confirmation)
**Authority document:** `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-4-path-x-phase4-feeds-phase5-authorization.md` (commit `3de3a40`)
**Estimated effort:** ~30-60min code work + ~50sec Phase 5+ re-fire LLM (~$0.37 LLM)
**Acceptance:** All § 6 acceptance criteria below verified; jack-ryan Gate-2 PASS; auto-commit per CLAUDE.md addendum
**Hive-state:** ENABLED (Matt 2026-05-23 decision-routing directive in force)

---

## Context

Cascade-resumption-3 CLOSED at A2-1 RE-FIRE-3 + Amendments 1-8 + 7a + Instance 6 #5 investigation (rocket + jack-ryan + gamora three-way parallel). Findings consolidated to gandalf, who elected Path X per Matt verbatim authorization.

**The architectural disconnect** (Instance 6 #5): Phase 4 Pareto-2 archive (34 kits; s0=18, s1=9, s2=7) and Phase 5 PM-1 input (598 / 208 unique _s2 kits via `passing_kits + variant_passing_rows`) are disjoint at ~80% kit_id join. Phase 5 LLM curation operates on Phase 3 _s2 output instead of the design-selected Pareto-2 substrate. Result: only 6 of 34 archive kits get faction labels; 19 of 22 shipped_worthy kits ship with `cluster_id=NULL`.

**Why Path X is the elected resolution** (per cascade-resumption-4 § 1):
1. **Designer-writes-substrate principle:** Phase 4 Pareto-2 IS the design-selected substrate; Phase 5 LLM curation should operate on it.
2. **Variants are loadout flavors, not faction-membership candidates.** Letting 585 variant rows dilute faction signal undermines substrate emergence.
3. **Phase 7 join coherence.** Path X gives 100% archive ∩ Phase 5 overlap — faction labels + Wave B names map 1:1 to shipped_worthy kits.

**PM-1 sparsity tier verified safe at n=34 by gamora** (`SPARSITY_TIER_GMM_BIC=24`; n=34>24; GMM_BIC sweep at k∈{3,4}; no degenerate fallback). 8-element coverage preserved per Amendment 7.

**Composition with rocket Instance 6 #5 investigation:** the `config_to_kit` collision (`season_generation_pipeline.py:1424-1428`) is NOT load-bearing for Path X — Phase 4 archive is constructed from all 54 base kits at Phase 2 (before the collision fires) and has the full mixed-sample distribution. The collision becomes a Cycle 15+ canonical-write target (deferred).

**No Phase 2-4 re-fire required** — `kit_archive.db` intact from A2-1 RE-FIRE-3 production run. Path X is a NARROW wire-up + Phase 5+ re-fire only.

---

## Required reading before starting

1. **Controlling authorization:** `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-4-path-x-phase4-feeds-phase5-authorization.md` (commit `3de3a40`) — READ ALL § 0-13; § 5 is the implementation spec
2. **Jack-ryan Instance 6 #5 framing-audit:** `agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md` (commit `eb14ec3`) — Q1-Q6 verdicts; informs the Path X election rationale
3. **Rocket Instance 6 #5 investigation (your own prior work):** `agentic_orchestration/rocket/notes/2026-05-29-cascade-r3-instance-6-5-phase4-phase5-disconnect-investigation.md` (commits `764e732` + `bb9a507`) — § 1 passing_kits composition + § 3 Phase 4 archive contents
4. **Designer-writes-substrate principle:** `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`
5. **Hive-mind decision-routing:** Matt 2026-05-23 directive (per `agentic_orchestration/AGENTS.md`) — seam-owners decide in-scope work; Matt is LAST-resort escalation
6. **CLAUDE.md commit + push discipline addendum** (meta-repo CLAUDE.md) — auto-commit work-products; push asks Matt

---

## Math-before-code

This is a CONFIGURATION CHANGE / wire-up — no new math. Existing PM-1 GMM_BIC algorithm operates on a smaller, design-selected input population. Per cascade-resumption-4 § 7 + jack-ryan Q5 ambiguity (CALIBRATION SCOPE), there is no math-hotspot consultation required.

**Sparsity tier mapping** (already locked):
- n=34 archive input → exceeds `SPARSITY_TIER_GMM_BIC=24` floor → GMM BIC-selected (k∈{3,4})
- Fallback (n < 8): PM-1 KMEANS_K2 floor breach → WARN + fall back to `passing_kits + variant_passing_rows` (existing behavior); surface to KR per § 9.2

---

## Cross-seam contract change? (Principle 6 gate)

Does this dispatch add, modify, rename, or remove any field on a telemetry schema table, fight_log dict key, loadout dict key, export packet structure, or any other inter-seam fixture dict?

**Answer: NO** — Path X changes the SOURCE of `surviving_kit_datas` (the PM-1 input variable) from `passing_kits + variant_passing_rows` to the Phase 4 archive's ACTIVE kits. The `_build_pm1_kit_data` function signature and PM-1 output schema are unchanged. Phase 7 cohesion-data lookup, Wave A faction-cluster JSON, Wave B kit_name dict, and all downstream export consumers see the same structural shape.

**Side effect on downstream consumers** (informational, not a contract change):
- Phase 7 `cluster_id` assignment coverage jumps from ~17.6% (6 of 34) to 100% (34 of 34) — this is the intended player-facing coherence improvement, not a schema change.
- Wave B `kit_count` changes from current 13 (s2 base only) to 34 (all archive kits) — same record shape, more records.

**Round-trip: not applicable — no cross-seam contract change in this dispatch.**

---

## Scope

- [ ] § 5.1 code change at `reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py:825-831` — replace PM-1 input construction
- [ ] Helper function `_load_phase4_archive_for_pm1(phase4_archive_path)` (or equivalent inline) — load ACTIVE kits from `kit_archive.db`; reuse Phase 7 query infrastructure (`QUERY_ACTIVE_KITS_IN_CELL` or equivalent from `simulation/spatial_gauntlet/phase4_db.py`)
- [ ] Build `_build_pm1_kit_data`-compatible records from archive rows (carry character_id, bc_cell_id, cultural_lineage_canonical, element, BC axes, sample_idx)
- [ ] Backward-compat fallback: if archive count < 8 (PM-1 KMEANS_K2 SPARSITY floor) → WARN log + fall back to `passing_kits + variant_passing_rows` original behavior + emit telemetry surface flag (KR routing trigger per § 9.2)
- [ ] Update log line at orchestrator:833 to `[PM-1][Path X] PM-1 input: %d Phase 4 archive kits (mixed-sample Pareto-2 winners)` per cascade-resumption-4 § 5.1 template
- [ ] § 5.4 tests (~5-10 new) — see § 6 acceptance criteria table for the assertions to encode
- [ ] Phase 5+ re-fire on season_001 ONLY (~50sec; ~$0.37 LLM); auto-commit
- [ ] Math note appended at `reincarnated-engine/src/reincarnated/simulation/notes/` documenting Path X election + PM-1 input source change + sparsity tier verification at n=34 (lightweight; ~30 lines)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `rocket/v1.0-cascade-r4-path-x-phase4-feeds-phase5-1`
- [ ] Auto-commit per CLAUDE.md addendum (code change + math note + tests + Phase 5+ re-fire artifacts each as their own commit)

---

## Acceptance criteria

### § 6.1 Behavioral verification (post-Phase-5-re-fire on season_001)

- [ ] **PM-1 input cardinality = 34** (or current-season archive size; ≥ 8 SPARSITY floor)
- [ ] **PM-1 sparsity branch = NONE** (gmm_bic_sweep) at n=34
- [ ] **GMM cluster count k ∈ {3, 4}** (BIC-selected; no degenerate k=3 fallback artifact)
- [ ] **Phase 5 cluster member sample distribution mixed s0/s1/s2** matching Phase 4 archive (s0=18, s1=9, s2=7)
- [ ] **Phase 5 cluster element distribution: all 8 elements present at primary mono layer** (preserves Amendment 7 acceptance)
- [ ] **Wave B `kit_count = 34`** (all archive kits named per Matt option (i))
- [ ] **Phase 7 `cluster_id` assignment coverage = 100% of archive kits** (vs current ~17.6%)

### § 6.2 Cost verification

- [ ] Per-season LLM cost actual ≤ $0.50 (target $0.37; surfaces if > $0.50 per § 9.2)
- [ ] 3-season projection ≤ $1.50 (target $1.10; <2% of $50 cap)

### § 6.3 Composition preservation

- [ ] Amendment 6 Sub-fix 1 (S7 deepcopy; 54 distinct substrate bindings at Phase 2) — UNCHANGED
- [ ] Amendment 6 Sub-fix 2 (Pareto-2 lineage partition; 34 archive winners) — NOW CONSUMED by Phase 5
- [ ] Amendment 6 Sub-fix 3 (S8 Bound 4 paired-joint-sampling) — UNCHANGED
- [ ] Amendment 7 (E4c element coverage; all 8 elements at primary mono) — NOW VISIBLE at Phase 5
- [ ] Amendment 7a (per-chain element wiring) — UNCHANGED
- [ ] Amendment 8 ($50 cap re-imposed; Matt-gate retired) — UNCHANGED

### Round-trip

- [ ] Round-trip: not applicable — no cross-seam contract change in this dispatch.

### Backward compat smoke

- [ ] Synthetic test: archive_count=4 (< 8 SPARSITY floor) → fallback path fires with WARN log + telemetry flag emitted; no exception
- [ ] Synthetic test: archive_count=34 (target) → Path X path fires; PM-1 receives 34 records

---

## Out of scope (explicit non-goals)

- **NO Phase 2-4 re-fire** — `kit_archive.db` intact from A2-1 RE-FIRE-3; do not re-execute upstream phases
- **NO `config_to_kit` collision fix** (Instance 6 #6 candidate) — deferred to Cycle 15+ canonical-write target per cascade-resumption-4 § 2 + § 8 item 3
- **NO seasons 002 + 003 production fire** — Track A fires post-Matt-confirmation-gate per § 9.1 step 6 (separate dispatch coordinated by KR)
- **NO Wave B scope reduction to shipped_worthy subset** — Matt elected option (i): all 34 archive kits named
- **NO new disciplines authoring** — Cycle 14 wave-close canonical-write target list (per cascade-resumption-4 § 8 items 1-12); jack-ryan owns the Disc #42a Q4 amendment
- **NO design re-deliberation** — Path X is locked per Matt verbatim authorization; if rocket discovers a NEW architectural surface (e.g., 7th Instance 6 surface), surface to KR per § 9.2 enumeration (do not unilaterally amend scope)

---

## Open questions for the agent to resolve

1. **Helper function placement** — author `_load_phase4_archive_for_pm1` inside `wave5_season_orchestrator.py` (consistent with `_init_kit_archive_db` precedent at line 355) OR delegate to `phase4_db.py` (closer to query DDL). Rocket design call; document choice in math note.

2. **Archive row → `KitCandidate`-shaped object** — `_build_pm1_kit_data` expects a kit object with `.character_id` attribute and substrate metadata. Archive DB row unpacking may need an adapter dataclass (similar to Phase 7's `Phase7SyntheticKit` at `phase7_bridge.py:203`) or can reuse `KitCandidate` if archive rows carry sufficient fields. Rocket design call; verify against `_build_pm1_kit_data` signature.

3. **Sample-distribution preservation** — confirm archive DB persists `sample_idx` (s0/s1/s2) per row. If absent, derive from `character_id` suffix. Document the source-of-truth choice in math note. Per gamora finding (hive-mind-state line 4779), archive carries s0/s1/s2 distinction independent of `wr_bracket_pass`.

4. **Math note scope** — keep narrow per cascade-resumption-4 § 7 ("no new math; configuration change only"). Document: (a) PM-1 input source change rationale, (b) sparsity tier verification at n=34 referencing gamora's check, (c) helper function location decision, (d) fallback condition + telemetry surface flag.

---

## KR routing triggers — surface to KR during/after execution

Per cascade-resumption-4 § 9.2 — surface to KR (DO NOT halt; KR coordinates Matt-surface):

- **PM-1 cardinality < 8 at Path X archive consumption** (SPARSITY floor breach) → fallback fires + surface
- **$50 soft cap approach or breach** (LLM cost actual > 75% of season target)
- **R48 violation** (oversized-file safety per Disc #49)
- **Gate-2 material-fail** (jack-ryan BLOCK on this dispatch's tag)
- **Wave B spec-gap surfaces** during the 34-kit naming run
- **Class-taxonomy unexpected surface**
- **New Instance 6 surface (#7 candidate)** — fresh framing-audit-relevant disconnect discovered during execution
- **Framing-audit catches load-bearing assumption refutation** during own work
- **Phase 5 LLM call exceeds 5min wall-clock** (Disc #19 resource conflict signal)

KR will batch all surfaces for Matt at the cascade-resumption-4 § 9.1 step 5 consolidation gate.

---

## Execution sequence

1. **Read all required-reading docs above**
2. **Authorization read-confirm:** verify cascade-resumption-4 § 5.1 + § 5.4 + § 6 against own understanding before writing code
3. **Implement § 5.1 code change** at `wave5_season_orchestrator.py:825-831` + helper function + backward-compat fallback
4. **Author math note** (~30 lines)
5. **Write § 5.4 tests** (~5-10 new); run pytest on relevant module
6. **Auto-commit** code + math note + tests (one commit; reference cascade-resumption-4 authorization in commit message)
7. **Fire Phase 5+ re-fire on season_001 only** — invoke orchestrator with smoke=False on existing `kit_archive.db` archive (NO Phase 2-4 re-fire); should complete in ~50sec
8. **Auto-commit** Phase 5+ re-fire artifacts (phase5_faction_clusters.json, wave_b_*.json, phase7_*.json updates)
9. **Append completion record to this dispatch file** (per dispatches/README.md format); auto-commit completion record
10. **Surface to KR (this dispatch file completion record):** PM-1 cardinality actual, GMM k selected, cost actual, Phase 7 cluster_id coverage actual, per-element distribution at primary mono, sample distribution in Phase 5 clusters

KR will then:
- Read completion record
- Route to jack-ryan for § 6 Gate-2 quick review
- Consolidate season_001 output + Phase 7 verdict + cost actual for Matt surface (cascade-resumption-4 § 9.1 step 5-6 confirmation gate)
- Upon Matt confirmation: fire Phase 2 parallel tracks (Track A seasons 002 + 003; Track B drax loadout + § 12 hero-image-task; Track C gandalf A/B sub-agent)

---

## References

- **Cascade-resumption-4 authorization** (controlling): `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-4-path-x-phase4-feeds-phase5-authorization.md` (commit `3de3a40`)
- **Cascade-resumption-3 CLOSED state:** `agentic_orchestration/cycle-14-hive-mind-state.md` (consolidation lines 4755-4842)
- **Jack-ryan Instance 6 #5 framing audit:** `agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md` (commit `eb14ec3`)
- **Rocket Instance 6 #5 investigation (own prior work):** `agentic_orchestration/rocket/notes/2026-05-29-cascade-r3-instance-6-5-phase4-phase5-disconnect-investigation.md` (commits `764e732` + `bb9a507`)
- **Gamora Instance 6 #5 investigation (Phase 7 join + 13/54 analysis):** `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-instance-6-5-phase3-mechanical-gate-13-54-analysis.md` (commit `76b1f15`)
- **Designer-writes-substrate principle:** `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`
- **Hive-mind decision routing:** Matt 2026-05-23 directive (per `agentic_orchestration/AGENTS.md`)
- **CLAUDE.md commit + push discipline addendum** (meta-repo `CLAUDE.md`)
- **PM-1 SPARSITY tier constants:** `reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` (search `SPARSITY_TIER_`)
- **Phase 7 query infrastructure (reuse pattern):** `reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py:526-700` + `simulation/spatial_gauntlet/phase4_db.py` (`QUERY_ACTIVE_KITS_IN_CELL`, `QUERY_DISTINCT_ACTIVE_CELLS`)

---

**KR sign-off:** Dispatch authored per Matt 2026-05-29 evening late "Path X — fire cascade-resumption-4" + "yes, option (i)" verbatim authorization, routed to rocket as the seam owner of `wave5_season_orchestrator.py` per AGENTS.md scope map. Auto-commits expected per CLAUDE.md addendum (rocket = seam owner of engine generation code; cascade-resumption-4 work program = authorized; no per-commit Matt re-ask).

---

## Completion record

**Completed by:** rocket
**Date:** 2026-05-29
**Engine commit:** `779b547` (code + math note + tests)
**Collaboration commit:** `30b30ff` (Phase 5+ re-fire artifacts)
**Tag:** `rocket/v1.0-cascade-r4-path-x-phase4-feeds-phase5-1`

### Acceptance criteria verification (§ 6)

1. **PM-1 cardinality actual:** 34 (s0=18 / s1=9 / s2=7 — exact match Phase 4 archive ACTIVE count)
2. **Sparsity tier:** NONE — n=34 >= SPARSITY_TIER_GMM_BIC=24; GMM BIC sweep at k∈{3,4}
3. **GMM cluster count k selected:** k=4 (BIC-selected)
4. **Per-element distribution (primary mono, 8 elements):** earth / fire / holy / lightning / physical / shadow / water / wind — all represented
5. **Faction cluster labels:**
   - Grounded Chain Strikers (13 kits)
   - Stormbreak Vanguard (11 kits)
   - Stormveil Ironclad Surge (9 kits)
   - Ashfield Siege Callers (1 kit)
6. **Wave B kit_count actual:** 34 (all 34 archive kits named per Matt option (i))
7. **Phase 7 cluster_id assignment coverage:** 34/34 = 100% (prior: 17.6% = 6/34)
8. **Phase 7 shipped_worthy:** 0 — C-2 compactness gate calibration gap (clusters at n=34 produce compactness ≈0.14; gate floor=0.40; calibrated for 598-kit population). **KR surface per dispatch §9.2.** Not a Path X wiring defect.
9. **LLM cost actual:** $0.36 (Wave A $0.02 + Wave B $0.34) — within $0.37 estimate
10. **Wall clock:** 42.5s
11. **Backward-compat fallback smoke:** PASS — archive_count < 8 path triggers WARN + falls back to `passing_kits + variant_passing_rows` + surfaces `pm1_path_x_fallback=True`
12. **Composition preservation:** Phase 2-4 pipeline untouched; `start_from_phase=5` fast-path verified; Phase 3 PM-1 result overridden at Phase 4.5 step (after Phase 4 completes)

### New surfaces for KR routing

- **Phase 7 C-2 compactness calibration gap:** P7_CLUSTER_COMPACTNESS_FLOOR=0.40 was calibrated for the 598-kit PM-1 population. At n=34, cluster compactness ≈0.14 → all kits fail C-2 gate → shipped_worthy=0. This is a separate calibration issue from Path X; needs KR assessment for Cycle 15. Route per dispatch §9.2.

### Deferred (out-of-scope for this dispatch)

- `config_to_kit` collision (`season_generation_pipeline.py:1424-1428`): last-writer-wins drops s0/s1 from `wr_bracket_pass=True`; deferred to Cycle 15+ per Instance 6 #5 investigation findings

### Artifacts produced

- `reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` — `ArchiveKitAdapter`, `_load_phase4_archive_for_pm1`, `_run_pm1_on_phase4_archive` helpers; Phase 4.5 block; `start_from_phase` parameter
- `reincarnated-engine/src/reincarnated/simulation/math/cascade-r4-path-x-pm1-input-source-change-2026-05-29.md` — math note (Discipline #1)
- `reincarnated-engine/tests/test_cascade_r4_path_x_pm1_input_source.py` — 14 tests across 5 groups
- `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` — re-fire output (k=4, 34 kits)
- `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_relationships.json` — re-fire output
- `agentic_orchestration/cycle-14-wave-5-season-001/phase7_season_summary.json` — re-fire output (shipped_worthy=0; 100% cluster coverage)
- `agentic_orchestration/cycle-14-wave-5-season-001/kit_archive.db` — unchanged archive (re-fire reads only)
