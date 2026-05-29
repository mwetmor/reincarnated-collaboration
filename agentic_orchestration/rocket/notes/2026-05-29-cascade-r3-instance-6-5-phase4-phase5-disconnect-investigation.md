# Findings Note — Cascade-R3 Instance 6 #5: Phase 4 → Phase 5 Disconnect Investigation

**Date:** 2026-05-29 (evening)
**Author:** rocket
**Authority:** Dispatch `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-cascade-resumption-3-instance-6-5-phase4-phase5-disconnect-investigation.md`
**Disc #42a framing-audit applied:** Yes — held open Amendment 7b vs. decorative-by-design until empirical chain complete
**Parallel companions:** jack-ryan (framing audit + Instance 6 canonical record), gamora (Phase 3 gate analysis)

---

## § 1 — passing_kits composition analysis

### 1.1 Total counts

| Population | Count | Gate |
|---|---|---|
| passing_kits (base kits, WR bracket pass) | 13 | Phase 3 WR bracket: season_emit=True in gauntlet |
| variant_passing_rows (variant WR pass) | 585 | Inherited from parent cell's WR bracket result |
| PM-1 input total | 598 | 13 + 585 |
| PM-1 unique member kit IDs | 208 | After clustering (13 base s2 + 195 unique variant) |

### 1.2 Per-BC-cell distribution of passing_kits (13 kits)

All 13 passing kits carry `sample_idx=2` (`_s2` character_id suffix). Zero passing kits carry `_s0` or `_s1`.

**BC axis distribution:**

| Axis | Values |
|---|---|
| bc_range | melee: 6, ranged: 6, mid: 1 |
| bc_tempo | medium: 6, high: 4, low: 3 |
| bc_amplitude | variable: 7, flat: 3, spiky: 3 |
| bc_attribute | wis: 5, int: 3, str: 3, dex: 2 |
| bc_proxy_density | none: 12, light: 1 |

5 cells produce no passing kit: `endgame_bc_melee_high_flat_int_none`, `endgame_bc_mid_high_flat_dex_none`, `endgame_bc_mid_low_spiky_int_none`, `endgame_bc_ranged_low_spiky_dex_none`, `endgame_bc_ranged_low_spiky_str_none`.

### 1.3 Per sample_idx pass rate

| sample_idx | WR bracket passing kits | Explanation |
|---|---|---|
| 0 (s0) | 0 / 18 cells | config_to_kit collision — s0 mapping overwritten by s1, then s2 |
| 1 (s1) | 0 / 18 cells | config_to_kit collision — s1 mapping overwritten by s2 |
| 2 (s2) | 13 / 18 cells | Last writer survives dict overwrite; s2 kits receive wr_bracket_pass=True |

**Root cause of _s2_ exclusivity:** `w5r2_gauntlet_sim_integration()` in `season_generation_pipeline.py:1424-1428` builds `config_to_kit` keyed on `legendary_id = f"{kit.bc_cell_id}_{chain_id}"` (NOT on `character_id`). For 3 samples sharing the same BC cell, all 3 samples emit the same set of `legendary_id` strings. The loop `config_to_kit[cfg["legendary_id"]] = kit` iterates s0 → s1 → s2 in order; s2 overwrites s1 which overwrote s0. When the gauntlet result maps `legendary_id → season_emit=True`, the lookup finds only the s2 KitCandidate. This is the source of ALL _s2_ exclusivity in PM-1 input and Phase 5 cluster membership.

### 1.4 Per substrate lineage distribution

| cultural_lineage_canonical | Count |
|---|---|
| fantasy_generic | 7 |
| east_asian | 3 |
| european | 2 |
| southeast_asian | 1 |

### 1.5 Per cohort_archetype distribution

| cohort_archetype | Count |
|---|---|
| balanced | 10 |
| dps_min_maxer | 3 |
| defensive | 0 |
| hybrid | 0 |

Note: defensive and hybrid cohorts absent from passing_kits. No cells with `bc_proxy_density=dense` are present in this run's 18 cells, so hybrid cohort is structurally absent.

### 1.6 Element distribution (passing_kits)

earth: 6, physical: 3, fire: 1, wind: 1, lightning: 1, water: 1. Three passing kits are hybrid (is_hybrid=True).

---

## § 2 — _s2_ hardcoding location + trace

### 2.1 Origin of _s2_ exclusivity

**Not a hardcoded filter.** There is no `_s2_` substring filter in Phase 5 input code (`wave5_season_orchestrator.py:825-836`). The _s2_ exclusivity is a structural consequence of `config_to_kit` dict collision in `w5r2_gauntlet_sim_integration()`.

**Trace:**

1. `season_generation_pipeline.py:1424-1428` — `w5r2_gauntlet_sim_integration()` iterates `kit_candidates` in list order (s0, then s1, then s2 for each cell). `config_to_kit[legendary_id] = kit` assigns all three samples to the same T4 `legendary_id`. s2 is the last writer and survives.

2. `season_generation_pipeline.py:1478-1480` — `if kit_emit_map.get(legendary_id, False): kit.wr_bracket_pass = True` — this resolves only to the s2 KitCandidate, not s0/s1.

3. `wave5_season_orchestrator.py:813` — `variant_passing_rows = [vr for vr in variant_rows if vr.wr_bracket_pass]` — variants inherit their parent cell's WR result. Since s2 passed, all variants for that cell get `wr_bracket_pass=True`.

4. `wave5_season_orchestrator.py:825-831` — `passing_kits` (13 s2 base kits) + `variant_passing_rows` (585 variants) feed PM-1. No filter on suffix here. The _s2_ exclusivity in PM-1 members reflects the upstream collision, not a downstream filter.

5. `VariantKitRow.character_id` (`wave5_season_orchestrator.py:452`) — `f"{bc_cell_id}_s2_{strategy.lower()}_{invest_profile}"`. The `_s2_` in variant IDs comes from the Amendment 6 S2 naming convention in variant config construction — this is intentional spec (S2 = second sub-fix tier of variant enumeration, per cascade-r3 dispatch vocabulary).

### 2.2 Extension cost to include s0 + s1

**Technically addressable but not a Phase 5 disconnection fix.** The config_to_kit collision means s0/s1 kits never receive `wr_bracket_pass=True`. Even if the collision were fixed (by accumulating all samples into a set per `legendary_id` and marking all matching kits), the question becomes: should all 3 samples per cell enter PM-1/Phase 5?

Amendment 7 (element coverage) deliberately created 3 distinct samples per cell with distinct element draws. The 3 samples are content-distinct kits, not duplicates. The config_to_kit collision is architecturally unintended: s0/s1 kits with passing mechanical performance are silently dropped from PM-1 input.

Extension cost (if fix were scoped):
- Modify `w5r2_gauntlet_sim_integration()` to accumulate all samples per `legendary_id` in a set, then mark all of them `wr_bracket_pass=True` — ~5 lines
- PM-1 input would grow from 598 to potentially ~598 + (2 × 13 cells × passing_rate) — conservatively 624-650
- Phase 5 cluster membership would include s0/s1 kits where their cells passed the WR bracket
- This would resolve the config_to_kit collision (an additional instance of Instance 6 pattern?)
- Amendment estimate: ~1 hour code + smoke

**However:** this is a SEPARATE potential bug (config_to_kit collision), not the Phase 4 → Phase 5 disconnect under investigation.

---

## § 3 — Phase 4 Pareto-2 archive consumption analysis

### 3.1 kit_archive contents (empirical)

| Population | Count | kit_archive rows |
|---|---|---|
| Base kits (Phase 4 accepted) | 34 | s0=18, s1=9, s2=7 |
| Variant rows (Phase 4 accepted) | 0 | All 585 variants rejected: `inferior_duplicate` |
| **Total kit_archive ACTIVE rows** | **34** | **34** |

**Why all 585 variants rejected:** `inferior_duplicate` via MG-3 (Mahalanobis nearest-neighbor gate in `phase4_mg5_eviction.py:170-178`). Variant rows carry the same quality_vector as their parent base kit (q1-q5 mechanical quality unchanged; only T4 strategy + invest_profile overlay differ, which are not in the quality vector). MG-3 flags them as inferior duplicates of the already-accepted base kit.

**Implication:** The Amendment 6 Sub-fix 2 Pareto-2 partition (cultural_lineage_canonical as second partition key) correctly operates within (bc_cell_id × lineage) buckets for BASE KITS. For variant rows, the partition does not help them escape rejection: their quality vectors are identical to a base kit resident in the same partition bucket.

### 3.2 Downstream consumers of kit_archive

| Consumer | File | What it reads | Reads s0/s1 kits? |
|---|---|---|---|
| Phase 7 bridge | `simulation/phase7_bridge.py` | ALL ACTIVE rows per bc_cell_id | Yes — 34 rows including s0=18, s1=9, s2=7 |
| Phase 7 DB queries | `simulation/phase7_db.py` | `WHERE archive_status='ACTIVE'` | Yes |
| Phase 4 MG gates (in-run) | `simulation/spatial_gauntlet/phase4_pipeline.py` | Per-cell residents during insertion | Yes (incremental) |
| phase7_kit_verdict_log | kit_archive.db | Written per evaluation | 89 substrate-led rows (multi-run) |
| Export pipeline (drax) | None — no direct kit_archive DB reads | Via orchestrator result dicts only | N/A |

**Phase 7 evaluates all 34 Phase 4 accepted kits.** Phase 7 result: `kits_evaluated=34`, `shipped_worthy=22` (64.7% acceptance rate), `held_mechanical=12`. The s0/s1 kits from Phase 4 are fully consumed by Phase 7 and contribute to the shipped-worthy count.

### 3.3 Phase 4 Pareto-2 vs Phase 5 relationship

The Phase 4 Pareto-2 archive and Phase 5 PM-1 input are **DESIGNED TO OPERATE ON DIFFERENT POPULATIONS**:

- **Phase 4 Pareto-2 population:** ALL 54 base kits (s0 + s1 + s2) + 585 variant rows. Gate: mechanical quality Pareto dominance per (bc_cell_id × lineage) partition. Output: kit_archive (34 rows).
- **Phase 5 PM-1 population:** 13 WR-bracket-passing base kits + 585 variant_passing_rows. Gate: WR bracket (season_emit in gauntlet). Output: PM-1 cluster members (208 unique).

These are two architecturally independent gates. Phase 4 is a Pareto-quality gate across ALL samples. Phase 5 is a WR-bracket (combat viability) gate on the last-surviving sample per cell.

The overlap is 6 kits: Phase 4 accepted s2 kits that are also in PM-1. The 28 Phase 4 accepted s0/s1 kits are absent from PM-1 — not because of a disconnect but because s0/s1 received `wr_bracket_pass=False` via config_to_kit collision.

**Phase 4 Pareto-2 archive is consumed by Phase 7.** Phase 7 evaluates mechanical viability against Phase 5 cohesion context. This is the intended Phase 4 → Phase 7 bridge, not Phase 4 → Phase 5.

---

## § 4 — Verdict: Amendment 7b spec proposal OR decorative-by-design confirmation

### Verdict: Phase 4 Pareto-2 → Phase 5 bypass is ARCHITECTURAL (NOT decorative-by-design; NOT Amendment 7b candidate)

**Rationale:**

The Gandhi finding ("Amendment 6 Sub-fix 2 Pareto-2 work is DECORATIVE for player-facing output") is empirically grounded but the framing requires clarification:

1. **Phase 4 Pareto-2 archive IS consumed downstream** — by Phase 7, which evaluates all 34 accepted kits for shipped-worthiness. 22 kits ship from Phase 7 output. Phase 4 Pareto-2 is NOT dead-code.

2. **Phase 5 bypassing Phase 4 archive is INTENDED ARCHITECTURE.** Phase 5 operates on PM-1 cluster members (WR-bracket-passing population). Phase 4 populates kit_archive for Phase 7 consumption. These are parallel downstream branches from the same Phase 3 gauntlet run, not a sequential chain.

3. **The player-facing output observation is correct in a narrow sense:** Phase 5 faction clustering (names, relationships, LLM labels) is built from PM-1 members, which are entirely _s2 base kits + s2-style variants. The 28 s0/s1 Phase 4 accepted kits do NOT appear in faction cluster membership. However, they DO appear in the Phase 7 shipped-worthy result (22 kits). Whether player-facing faction assignment is complete requires checking Phase 7 → export wiring, which is outside this scope.

4. **The true architectural issue is the config_to_kit collision** — not Phase 4 → Phase 5 bypass. `w5r2_gauntlet_sim_integration()` silently drops s0/s1 kits from WR bracket consideration by overwriting the config_to_kit dict. This means:
   - 28 Phase 4 Pareto-accepted kits (s0/s1) are excluded from Phase 5 faction clustering
   - These kits may ship from Phase 7 without faction assignment
   - Amendment 7 (3 distinct elements per cell) makes this more consequential: s0/s1/s2 may have distinct elements, but only s2 enters PM-1

5. **Is Amendment 7b warranted?** The answer depends on whether the 28 s0/s1 Phase 4 kits SHOULD have faction cluster membership for player-facing output. If they ship from Phase 7 without faction assignment, that is a gap. However, this is a DESIGN QUESTION (gandalf/matt scope), not a code defect with an obvious fix. The config_to_kit collision fix is scoped separately.

### Summary verdict

| Investigation area | Finding |
|---|---|
| Phase 4 → Phase 5 bypass | Architectural — two parallel downstream branches; NOT a bug |
| Phase 4 Pareto-2 consumed? | YES — by Phase 7 (22 kits shipped) |
| Phase 4 decorative? | No. Pareto-2 archive is the Phase 7 input population |
| _s2_ hardcoding | No filter hardcoding — structural consequence of config_to_kit collision |
| config_to_kit collision | Unintended — silences s0/s1 WR bracket evaluation; separate issue from Phase 4→5 bypass |
| Amendment 7b needed? | Scope-conditional — only if 28 s0/s1 Phase 7 kits lacking faction assignment is a player-facing gap; DESIGN QUESTION for gandalf/matt |

---

## § 5 — If Amendment 7b: scope estimate

**Not recommended as Amendment 7b per current evidence.** The Phase 4 → Phase 5 bypass is architectural. However, the config_to_kit collision IS a candidate for a focused fix:

**config_to_kit collision fix (tentative Amendment 7c or standalone):**

| Change | File | Lines |
|---|---|---|
| Accumulate all samples per legendary_id in a set | `generation/season_generation_pipeline.py:w5r2_gauntlet_sim_integration()` | ~8 lines |
| Mark all accumulated kits `wr_bracket_pass=True` after emit_map lookup | Same function | ~5 lines |
| Update math note | `generation/notes/` | ~20 lines |
| Smoke test | `smoke=True` re-fire | ~2 min |
| Full test suite check | `pytest` | ~5 min |

**Effort estimate:** ~45-90 min total. Low risk — the MG-1/2/3/4/5 gates in Phase 4 are unaffected. PM-1 input would grow by ~26 additional base kits (2 more samples per 13 passing cells), reaching ~624 PM-1 input. Phase 5 faction clusters would include s0/s1 content-distinct kits with different elements. This would reduce the "only s2 survives" artifact.

**However:** This fix should be PRECEDED by a design question to gandalf/matt: should all 3 samples per WR-bracket-passing cell enter PM-1 / Phase 5? The Amendment 7 3-sample design was explicitly to produce distinct-element kits per cell. The config_to_kit collision effectively erases that diversity from Phase 5 consideration.

---

## § 6 — Surface-to-KR findings

### § 6.1 — New surface: config_to_kit collision (potential Instance 6 #6)

`w5r2_gauntlet_sim_integration()` in `season_generation_pipeline.py:1424-1428` overwrites `config_to_kit` on each iteration of the 3-sample loop. This silently drops s0/s1 kits from WR bracket consideration across all 18 cells.

This meets Disc #42a framing-audit pattern: a pre-imposed structural constraint (config_to_kit overwrite) that shapes all downstream WR bracket, PM-1, Phase 5 outputs invisibly. Whether this is intentional spec (only one representative per cell in gauntlet) or an accidental collision depends on Amendment 7 3-sample intent.

**Surface condition triggered:** Discovery of additional Instance 6 surface (dispatch § 5, row 1). Surfacing to KR for gandalf design-context analysis.

### § 6.2 — Phase 7 faction assignment gap (corollary)

22 kits shipped from Phase 7. 13 of those were in PM-1 (s2 base kits); up to 9-10 additional are s0/s1 kits that entered kit_archive via Phase 4 Pareto but never received faction cluster assignment. Whether these kits have cluster_id assignment in Phase 7 cohesion_data lookup is unknown (cohesion_data only has 13 entries from Wave B). This is a corollary finding — not a new Instance 6 surface by itself, but a data quality gap worth flagging for export/drax downstream.

---

## § 7 — Acceptance criteria self-check

| Criterion | Status |
|---|---|
| § 2.1 passing_kits composition (per-cell, per-sample_idx, per-lineage, per-cohort) | COMPLETE |
| § 2.2 _s2_ hardcoding location + trace | COMPLETE — no hardcoded filter; structural collision |
| § 2.3 Phase 4 Pareto-2 consumption analysis | COMPLETE — consumed by Phase 7; not dead-code |
| § 2.4 Verdict explicit | COMPLETE — architectural bypass; not decorative-by-design; no Amendment 7b |
| KR consumption-ready | COMPLETE |
| Surface-to-KR conditions triggered | YES — § 6.1 config_to_kit collision |

---

**Findings authored by:** rocket, 2026-05-29 evening late
**Collab commit:** (appended post-commit)
