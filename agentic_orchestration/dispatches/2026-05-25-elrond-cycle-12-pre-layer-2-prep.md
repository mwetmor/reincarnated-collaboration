# Dispatch — 2026-05-25 — elrond — Cycle 12 pre-Layer-2 prep (per-cell register breakdown + element_weapon_kind_coherence_matrix)

**From:** knight-rider
**To:** elrond (data steward — catalogue DB; pre-Layer-2 substrate analysis lead)
**Approved by:** KR autonomous in-scope decision per Cycle 12 scope-doc § 1 + § 6 (sub-agent invocation sequencing + acceptance-criterion application + pre-resolved known-unknowns); surfaced by legolas MC-1 surprise 1 + MC-2 flag 3 returns
**Estimated effort:** ~30-60 min combined (~15-30 min per-cell register breakdown + ~15-30 min coherence matrix from frequency distribution)
**Acceptance:** Two pre-Layer-2 substrate artifacts produced to inform rocket Layer 2 dispatch authoring + Layer 2 generator implementation: (1) per-cell register breakdown query result; (2) element_weapon_kind_coherence_matrix from Tier S/A frequency distribution in v1_scope

---

## Context

Legolas MC-1 + MC-2 Mode A methodology consults returned 2026-05-25 with hybrid recommendations (MC-1 = H3 deterministic per-cell-fired-once enumeration; MC-2 = hybrid filter-then-sample with soft coherence weighting). Both consults surfaced prerequisite substrate artifacts elrond should produce BEFORE rocket Layer 2 dispatch fires:

1. **MC-1 surprise 1** (level-of-analysis gap): composition policy v1 § 1 register-share targets (historical ~50-55%, fantasy ~30-35%) were designed for substrate CURATION, not kit GENERATION. Applying as per-cell generation weights may not produce matching kit register distributions because within each cell, eligible substrate may itself be register-skewed (martial STR/DEX cells are historical-heavy per § 11.2). Resolution: **per-cell register breakdown SQL query** against v1_scope, BEFORE Layer 2 dispatch finalizes cell-weight parameters.

2. **MC-2 flag 3** (required Layer 2 input artifact): the hybrid filter-then-sample heuristic scoring requires `element_weapon_kind_coherence_matrix` — a matrix of element × weapon_kind pair frequencies derived from Tier S/A row distribution in v1_scope, used as the soft coherence weight component (0.15 × element_weapon_kind_coherence). Without this matrix, the substrate-binding heuristic cannot fire per MC-2's recommended scoring function.

Both are short SQL-driven artifacts; elrond is the seam-owner per catalogue DB ownership.

This dispatch fires in parallel with: elrond SC-2 Option A re-fire + jack-ryan Gate-2 on drax Wave 3b + gandalf Pattern A-light on composition policy § 4 coverage gap.

These two artifacts are PREREQS for rocket Layer 2 dispatch authoring (alongside gandalf comp-policy § 4 confirmation + MC-1/MC-2 methodology recommendations + Gate-1 amendment integration). Until all four return, rocket L2 dispatch authoring waits.

---

## Required reading before starting

- `canonical/00-ground-state.md` § 1
- **`agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md`** § "Surprise 1" (level-of-analysis gap — primary source for per-cell register breakdown ask)
- **`agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md`** § "Flag 3" (element_weapon_kind_coherence_matrix specification + scoring function context)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1 (register-share targets) + § 11.2 (cell-level register skew)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes; 22-cell BC roster context)
- v1_scope substrate (per Cycle 10 wind-down): `elrond/v0.0-cycle-10-stage-3-phase-2-v1-scope-2026-05-25` tag → 3,042 rows; per-cell coverage report at elrond Phase 3 artifact
- v1_scope substrate DB: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` table `weapon_knowledge_entries` (confirmed per SC-2 Phase 1 enumeration finding)
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 (PlayerClass contract context; mechanical_substrate_triple consumes these artifacts at Layer 2 runtime)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #11 empirical inspection + #25 semantic-layer rep-audit + ADR-004 MIGRATION.md cross-seam

---

## Math-before-code (per Discipline #1)

No code — SQL queries against existing catalogue DB. Math layer is purely descriptive statistics:

**Artifact 1 — per-cell register breakdown:**
- For each of the 22 BC roster cells, count v1_scope=1 rows by register (historical / fantasy / military_modern / mythological)
- Output shape: table with columns (bc_target_cell_id, register, row_count) or matrix [cell_id × register → count]
- Derived field: per-cell register-share percentages (count / cell-total)
- Purpose: informs Layer 2 cell-weight parameter selection (composition-policy-weighted sampling needs to know within-cell register skew before parameter setting)

**Artifact 2 — element_weapon_kind_coherence_matrix:**
- For Tier S + Tier A rows in v1_scope (high-quality substrate), count rows by (element × weapon_kind) pair
- Output shape: matrix [element × weapon_kind → count], or normalized [element × weapon_kind → frequency]
- Coherence score per pair: normalized to [0, 1] per MC-2's scoring function (0.15 × coherence weight); MC-2 spec recommends frequency-as-coherence-proxy (high frequency = high coherence)
- Purpose: informs Layer 2 substrate-binding heuristic per MC-2 hybrid filter-then-sample scoring function
- Per L9: this matrix is mechanical-layer (element + weapon_kind are mechanical substrate dimensions, not semantic overlay)

---

## Scope (elrond pre-Layer-2 prep)

### Artifact 1 — per-cell register breakdown

- Query catalogue DB (`weapon_knowledge_entries`) for v1_scope=1 rows
- Aggregate by (bc_target_cell_id, register); count rows per group
- Compute per-cell register-share percentages (per-register count / per-cell total)
- Surface zero-coverage cells (cells with zero v1_scope rows in any register — useful context for MC-1 surprise 2 BLOCKED cells 14, 15, 17, 23)
- Capture artifact at `agentic_orchestration/elrond/cycle-12-pre-layer-2/per-cell-register-breakdown-2026-05-25.md` (markdown table format; or CSV at sibling path if elrond prefers)

### Artifact 2 — element_weapon_kind_coherence_matrix

- Query catalogue DB for Tier S + Tier A rows in v1_scope
- Aggregate by (element, weapon_kind); count rows per pair
- Compute normalized frequency per (element, weapon_kind) pair (count / total Tier-S+A v1_scope rows)
- Format as matrix (markdown table with elements as rows + weapon_kinds as columns, or vice versa per elrond layout judgment)
- Capture artifact at `agentic_orchestration/elrond/cycle-12-pre-layer-2/element-weapon-kind-coherence-matrix-2026-05-25.md`
- Include brief note on canonical Vincere element enum (8 core elements per ground-state) + weapon_kind enum (per existing catalogue schema) so consumer (rocket Layer 2) knows expected vocabulary

### Common (both artifacts)

- Per Discipline #11: direct-inspect rows before aggregating; show ≥3 sample rows from raw query in completion record
- Per Discipline #25 semantic-layer rep-audit: confirm both artifacts use MECHANICAL substrate fields only per L9 (element + weapon_kind + register/tier are mechanical; cultural_tradition / lineage / period are explicitly excluded from these artifacts)
- MIGRATION.md NOT required — both artifacts are read-side products; no schema change; downstream rocket Layer 2 consumer will read these as input

---

## Out of scope

- Schema changes (read-only against existing v1_scope substrate)
- Modifications to v1_scope (the curated substrate stays fixed per Cycle 10 wind-down)
- Inclusion of semantic-overlay fields (cultural_tradition / lineage / period) in either artifact — per L9, these are NOT in the BDI math model and NOT in MC-2's scoring function
- Per-cell substrate-binding execution (Layer 2 runtime concern; rocket implements per MC-2 recommendation against these artifacts)
- Composition policy v1 § 4 coverage gap confirmation (separate gandalf Pattern A-light dispatch — fires in parallel with this)
- Cells 14/15/17/23 BLOCKED-status fix (per MC-1 surprise 2, Layer 2 dispatch consumes composition policy § 4.1 routing table for these cells; not in this dispatch's scope)
- SC-2 subtype classification (separate dispatch — fires in parallel)
- SC-1 substrate-tagging cleanup (separate dispatch — likely in-flight or just-completed)

---

## Acceptance criteria

- [ ] Artifact 1 (per-cell register breakdown) authored at `agentic_orchestration/elrond/cycle-12-pre-layer-2/per-cell-register-breakdown-2026-05-25.md`
- [ ] Artifact 2 (element_weapon_kind_coherence_matrix) authored at `agentic_orchestration/elrond/cycle-12-pre-layer-2/element-weapon-kind-coherence-matrix-2026-05-25.md`
- [ ] Each artifact includes SQL query used + raw sample rows (≥3) + aggregated output + brief consumer note (what Layer 2 should expect)
- [ ] Per Discipline #11 empirical inspection: direct-inspected rows BEFORE aggregating
- [ ] Per Discipline #25 semantic-layer rep-audit: both artifacts use mechanical substrate fields only per L9
- [ ] Auto-commit + auto-push per elrond seam authorization (CLAUDE.md addendum)
- [ ] Tag: `elrond/cycle-12-pre-layer-2-prep-2026-05-25`

---

## Open questions for the agent to resolve

- Exact cell roster — confirmed 22-cell BC roster per qd-engine-bc-axes-lock; if catalogue schema column for cell-id differs from canonical, elrond clarifies in artifact
- Element enum vocabulary — 8 core elements per ground-state; if substrate has rows with element values outside the 8 (e.g., "physical", "neutral"), elrond surfaces in artifact note (may indicate v1_scope gap or substrate-tagging inconsistency)
- Whether to include Tier B rows in coherence matrix — MC-2 spec says "Tier S/A frequency distribution"; elrond may surface Tier B as a separate matrix column for completeness if it informs the question (elrond judgment; default Tier S+A only)
- Whether per-cell register breakdown should include v1_scope=0 rows as a "context" column — default per dispatch is v1_scope=1 only; elrond may surface v1_scope=0 totals as side-note for completeness

---

## Cross-seam impact

Round-trip: not applicable — read-only SQL queries against existing substrate; no schema changes; no fixture-dict shape changes. Both artifacts are markdown files consumed by KR + rocket Layer 2 dispatch authoring; no MIGRATION.md required.

---

## References

- `agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md` (MC-1 surprise 1 source)
- `agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md` (MC-2 flag 3 source)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1 + § 11.2
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #11 + #25

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** KR autonomous in-scope decision per Cycle 12 scope-doc § 1 (sub-agent invocation sequencing) + § 6 (pre-resolved known-unknowns — legolas MC-1+MC-2 returns naturally surface elrond prereq artifacts); routed seam-owner per hive-mind decision-routing § 4.3
**Status:** FIRE — pre-Layer-2 prep; fires in parallel with jack-ryan Gate-2 on drax Wave 3b + elrond SC-2 Option A re-fire + gandalf Pattern A-light on comp-policy § 4 coverage gap

**Matt-touch sequence:** elrond completes both artifacts → KR captures in state file → KR integrates into rocket L2 dispatch authoring alongside MC-1/MC-2 methodology + Gate-1 amendments + gandalf comp-policy confirmation → rocket L2 dispatch fires

---

## COMPLETION RECORD — 2026-05-25 elrond pre-Layer-2 prep

**Status:** COMPLETE
**Executor:** elrond
**Tag:** `elrond/cycle-12-pre-layer-2-prep-2026-05-25`

### Artifacts produced

| # | Artifact | Path |
|---|---|---|
| 1 | per-cell register breakdown | `agentic_orchestration/elrond/cycle-12-pre-layer-2/per-cell-register-breakdown-2026-05-25.md` |
| 2 | element_weapon_kind_coherence_matrix | `agentic_orchestration/elrond/cycle-12-pre-layer-2/element-weapon-kind-coherence-matrix-2026-05-25.md` |

### Row counts surfaced

- **v1_scope total:** 2,293 rows (NOT 3,042 quoted in dispatch — see Artifact 1 § 6.1 for substrate-bookkeeping gap)
- **v1_scope × tier:** S=539 / A=675 / B=1,056 / C=23
- **v1_scope × register (aggregate):** historical=1,202 (52.4%) / fantasy=1,022 (44.6%) / military_modern=32 (1.4%) / mythological=37 (1.6%)
- **v1_scope × mechanical_cell:** 18 named cells + `untyped` (466 rows) + `__null_trace__` Stage 3.5 gap-fill (42 rows) + `int_other` orphan (1 row) = 21 distinct cell-labels (intent doc lists 22 cells; 4 intent-doc cells have zero direct cell-id coverage and route per § 4.1)
- **Element-typed (S+A+B keyword-inference):** fire=13 / water=22 / earth=67 / wind=8 / lightning=5 / holy=25 / shadow=82 / physical=~2,058 (96.2% of total — element column does NOT exist; inference is keyword-based)

### Empirical inspection evidence (Discipline #11)

Artifact 1 § 5: 12 random rows sampled across mechanical_cell × register; spot-check validates correct cell+register assignment (e.g., `Smallsword` → `dex_dagger_assassin` historical S-tier; `pyromantic_ember_staff` → `__null_trace__` fantasy A-tier).

Artifact 2 § 4: 13 sample rows across 7 elements; spot-check validates word-boundary refined keyword-matching correctly excludes prior false-positives (e.g., `Centrefire revolver` not matched to fire; `Pair of Sword-Grip Ornaments` not matched to wind via "air").

### Consumer notes for rocket Layer 2

**Artifact 1 (per-cell register):**
- **DO NOT** apply composition policy § 1 aggregate register-share targets (historical 50-55% / fantasy 30-35%) as per-cell generation weights — per-cell registers are bimodal.
- Five cells have ≥85% single-register dominance; `dex_twin_blade_fencer_thin` is 100% fantasy.
- Cell-pair sharing per composition policy § 4.2 is visible in the data (substrate honors the 4-tuple-shared pools).
- 4 intent-doc cells (11 Red Mage, 17 Channeling Cleric, 22 Monk, 24 Artillery Mage) have ZERO direct cell-id coverage → MC-1 surprise 2 BLOCKED-cell routing per § 4.1 applies.

**Artifact 2 (element × weapon_kind coherence):**
- Use Matrix 2.C (row-normalized within element) as the lookup form for MC-2's `w_coherence × element_weapon_kind_coherence_score`.
- Substrate has weak DIRECT element signal — 96.2% of S+A+B rows default to `physical` (no element keyword). Per MC-2 § 6.1, `physical` IS the universal base element; this is expected.
- Wind (8 rows) and lightning (5 rows) are critically thin across all weapon_kinds — thin-cell-fallback cascade will fire routinely for wind/lightning kits per MC-2 § 5.2.
- Per MC-2 § 6.1, do NOT hard-zero matrix cells; apply epsilon (~0.01) for zero (element, weapon_kind) pairs.

### Substrate gaps surfaced for KR

1. **v1_scope row-count discrepancy** (dispatch 3,042 vs. actual 2,293 — see Artifact 1 § 6.1). May reflect sibling elrond SC-1 / SC-2 in-flight UPDATEs or pre-Stage-4 staleness in dispatch ref.
2. **No `element` column on `weapon_knowledge_entries` or populated on `weapons.dominant_element_affinities`.** Inference is keyword-based on `canonical_name`. v1.1+ schema evolution candidate.
3. **`tome` / `focus` weapon_kinds defined in CHECK constraint but zero-populated** — caster kits requesting these weapon_kinds substrate-bind from `category` rows.
4. **2 intent-doc cells (Monk, Red Mage) have zero substrate coverage and zero routing in composition policy § 4.1** — Layer 2 should escalate to gandalf if these archetypes are in rocket L2 dispatch scope.

### Per Discipline #25 L9 semantic-layer rep-audit

Both artifacts confirmed: use mechanical fields only (mechanical_cell, register_canonical, element, weapon_kind, quality_tier). No cultural_tradition / lineage / period / proxy_density fields included per MC-2 § 1 + composition policy § 3.

### Per ADR-004 cross-seam coordination

NO MIGRATION.md required. Both artifacts are read-side products consumed by rocket Layer 2 dispatch authoring. No schema changes. No engine telemetry writes. No fixture-dict shape changes.

### Concurrency hygiene

- READ-ONLY queries against `weapon_knowledge_entries` (no UPDATE / no schema change)
- No contention observed with sibling SC-1 / SC-2 elrond instances (which do UPDATEs against `cultural_lineage_canonical` / `historical_period_canonical` / `weapon_kind_classified_subtype` columns — disjoint from this dispatch's read columns)
- PRAGMA busy_timeout=30000ms was not invoked (no write contention occurred); SELECT queries completed in <1s each

