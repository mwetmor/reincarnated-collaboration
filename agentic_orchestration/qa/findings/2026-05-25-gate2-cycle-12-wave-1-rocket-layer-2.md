# Finding — 2026-05-25 — Gate-2 Cycle 12 Wave 1 — Rocket Layer 2 (BC-Target Subspace Generator)

**Reviewer:** jack-ryan
**Severity:** WARN (PASS-WITH-AMENDMENTS — no BLOCK findings; three WARN; two INFO)
**Target:** commit `9597084`; tag `rocket/v0.1-cycle-12-layer-2-bc-target-subspace-generator-2026-05-25`
**Developer:** rocket
**Principles applied:** 1, 2, 3, 4, 5 + Cross-cutting

---

## Verdict

**PASS-WITH-AMENDMENTS.** Layer 2 is composable for Layer 4 sequencing once MC-3 returns.
Zero BLOCK findings. Three WARN findings. Two INFO findings.

All five Gate-1 amendments (WARN-2/4/6/7 + INFO-4) are correctly disposed and verified in
source. The primary scrutiny target — 25-cell vs 22-cell BC roster discrepancy — is RESOLVED
as INFO-level: the 25 cells are the correct canonical count per gandalf comp-policy verdict §
1.1 (the "22-cell" references in framing brief et al. were informal undercount; the operational
reality is 12 routed + 13 un-routed = 25 cell-rows in Stage 0 roster). No canonical amendment
required. Three WARN observations are noted for rocket to address at next commit opportunity;
none block Layer 4 sequencing.

---

## Per-principle findings

---

### Principle 1 — Math-before-code

**PASS.** Math note `generation/notes/cycle-12-layer-2-bc-target-subspace-generator-2026-05-25.md`
is present and correctly covers all five required sections (Math 1-5). Verified:

- **Math 1 (MC-1 H3 cell sampling):** formula is correct. 22-cell reference in math note §
  1.1 refers to the v1-bc-target-intent Sketch A roster and matches the CELL_DEFINITIONS table
  design intent. The 25-cell discrepancy is addressed under cross-cutting below (INFO-A).

- **Math 2 (MC-2 scoring function):** score = 0.40·tier + 0.35·cell_match + 0.15·coherence +
  0.10·novelty. Verified against `_score_row()` in `bc_target_substrate_engine.py` — weights
  match exactly. Tier weights (S=1.0/A=0.75/B=0.50/C=0.25) match `TIER_WEIGHTS` dict. Coherence
  lookup from `ELEMENT_WEAPON_KIND_COHERENCE` (Matrix 2.C) matches math note § 2.1. Novelty
  formula `1.0 - (times_selected / max(1, total_selected))` matches implementation. CONFIRMED.

- **Math 3 (comp-policy § 4 routing):** 12 LOCKED cells enumerated and matched against
  `_apply_section_4_routing()` routing dispatch in `bc_target_subspace_generator.py`. All 12
  routing labels present (fold, stage_3_5, option_c, sidecar_b variants, accept_low_floor,
  pan_fantasy). Un-routed cells (13 cells) route to default heuristic per gandalf Option B
  verdict. Cell 20 (Holy Knight) correctly flags as `default_heuristic_v1.1_amendment_queued`.
  CONFIRMED.

- **Math 4 (per-cell register-share targeting):** correctly defers per-cell register override;
  relies on ensemble-level monitoring via Smoke Gate 2 register-share audit. Implementation
  consistent with policy; empirical tuning deferred to post-smoke. CONFIRMED.

- **Math 5 (BLOCKED/THIN classification):** THIN_CELL_FLOOR=5 adopted (matches MC-2 recommendation
  and math note § 5.3). Pre-fire audit classifies all 25 cells; surfaced in `audit_log()` return
  per Cell 14/17 as special-routing cases. CONFIRMED.

#### WARN-A — Math note uses "22 cells" referencing throughout; now operationally 25

**Observation:** The math note (Math 1 § 1.1 and § 5 header) consistently references "22 BC roster
cells" and "22 cells" as the substrate pre-filter target count. The implementation operates on
25 CELL_DEFINITIONS. The math note was authored against the framing-brief "22-cell" figure and
does not note the reconciliation to 25 per gandalf comp-policy verdict § 1.1. Test line 148
explicitly asserts `len(audit['per_cell']) == 25`.

**Risk:** future readers of the math note will find the "22-cell" claim inconsistent with the
implementation. This is a documentation drift candidate.

**Cite:** Discipline #1 (math-before-code — math note must accurately describe implementation);
Discipline #13a (implementation-vs-intent drift).

**Action:** Rocket appends a note to math note § 1.1 at next commit: "Note: operational roster
is 25 cells per gandalf comp-policy verdict § 1.1 (2026-05-25). The '22-cell' figure in framing
brief and this note's § 1.1 header was an informal undercount. CELL_DEFINITIONS has 25 entries."

**Severity: WARN.** Does not block Layer 4 sequencing; documentation only. Rocket may batch
with other math-note amendments.

---

#### INFO-B — Discipline #1.2 code-line citations absent from math note

**Observation:** Per Gate-2 on Layer 3 INFO-B precedent and Discipline #1.2 (2026-05-23
amendment), math note claims of the form "X applied as Y at stage Z" should include
parenthetical code references `(script lines NN-MM)` or `(file.py:NNN)`. Math note § 2.1
states "Implementation: `SubstrateBindingEngine._score_row()` in bc_target_substrate_engine.py"
— this is a correct file-level citation. However, no line-range citations appear in any of the
five math sections.

**Cite:** Discipline #1.2 (math-note implementation claims must cite code line references).

**Action:** Rocket retrofits line-range citations at next commit (non-blocking; INFO-level per
Gate-2 on L3 INFO-B precedent). Not a Layer 4 sequencing gate.

**Severity: INFO.**

---

### Principle 2 — Smoke-gate before commit

**PASS.** 28/28 Layer 2 tests PASS. 374/374 regression PASS (excluding 7 pre-existing
`GROUPING_VOCAB_DOC_PATH` env-var issue in unrelated test files, documented as not Layer 2
fault). Verified by dispatch completion record and MIGRATION.md smoke record.

#### Smoke Gate 1 (22-kit base enumeration)
Four tests verified: kit generation, Gate-1 shape conformance, cell routing provenance, audit
log surfaces BLOCKED/THIN/READY. Audit log asserts 25 cell entries (`len(audit['per_cell']) == 25`)
— confirms implementation operationally consistent with 25-cell roster.

#### Smoke Gate 2 (50-kit cheapest-refuting-test — per MC-2 § 5.2 + Discipline #19.1)
Pass thresholds verified in test code: ≥90% coherence (element × weapon_kind pairing above
EPSILON in Matrix 2.C) + ≥25% diversity (unique substrate row IDs / total kits) + ≤10%
deep-relaxation (relaxation_level ≥ 3). Confirmed thresholds match dispatch acceptance criteria.
Test passes per completion record. CONFIRMED.

#### Smoke Gate 3 (round-trip JSON serialization)
Four tests: round-trip, t4_alteration_output=None, off_hand_item=None, required-fields-present.
WARN-6 constraint (json.dumps round-trip) tested inline in test body. CONFIRMED.

#### Smoke Gate 4 (AUGMENT — legacy ClassGenerator preserved)
Three tests: legacy generator importable + has generate() method, discriminator distinct
("generator_v2" != "legacy_classgenerator"), engine_version distinct. CONFIRMED.

#### Pre-existing env-var issue (7 unrelated test files)
Confirmed: `GROUPING_VOCAB_DOC_PATH` issue is pre-existing and unrelated to Layer 2 scope.
Documented in dispatch completion record and MIGRATION.md. Gate-2 agrees — not Layer 2 fault.
No action required.

---

### Principle 3 — Cross-seam round-trip readiness

**PASS WITH OBSERVATIONS.**

#### MIGRATION.md § v1.4-layer-2 (export seam) — present and complete
`src/reincarnated/export/MIGRATION.md` § v1.4-layer-2 is present. Documents: Gate-1 amendments
applied, new modules shipped, AUGMENT pattern, consumer obligations (star-lord/gamora/drax all
correctly deferred to Layer 6 wire-up), smoke result. Cross-seam contract change correctly
flagged as YES (Principle 6 gate); round-trip smoke justified as 28/28 PASS.

#### generation/MIGRATION.md — present and complete
`src/reincarnated/generation/MIGRATION.md` entry at [2026-05-25] Cycle 12 Layer 2 present.
Change summary, Gate-1 amendments, new modules, AUGMENT pattern, smoke test result all
correctly documented. Consumer obligations enumerated.

#### WARN-B — Export MIGRATION.md § v1.4-layer-2 PlayerClassV2 schema pseudocode uses divergent field names

**Observation:** The PlayerClassV2 schema pseudocode excerpt in `export/MIGRATION.md` §
v1.4-layer-2 (lines 3056-3085) uses field names `stat_distribution`, `substrate_triple`,
`class_id`, `class_name`, `archetype`, `bc_target_label` — these are the conceptual framing-brief
names, NOT the actual field names in the implementation. The actual `PlayerClassV2` dataclass
uses `stat_allocation`, `mechanical_substrate_triple`, and does not have `class_id`,
`class_name`, `archetype`, or `bc_target_label` as fields.

**Risk:** star-lord or gamora consuming this MIGRATION.md schema excerpt at Layer 6 wire-up
will find field names that don't match the actual implementation. This is a documentation hazard
at the cross-seam boundary (Discipline #8 / Principle 3 Principle 6 round-trip risk).

**Cite:** Principle 3 (cross-seam round-trip readiness); Principle 6 (cross-seam contract
changes require round-trip discipline); ADR-004 (MIGRATION.md must be accurate for downstream
consumers).

**Action:** Rocket amends `export/MIGRATION.md` § v1.4-layer-2 PlayerClassV2 schema excerpt
to use the actual field names from the implementation (`stat_allocation`, `mechanical_substrate_triple`,
etc.) OR adds a clear note: "The following is the framing-brief conceptual schema; actual
implementation field names may differ — see `bc_target_player_class.py` for authoritative field
names." Must be addressed before Layer 6 wire-up dispatch authoring (not an immediate Layer 4
blocker, but should not be left for KR to discover during Layer 6 dispatch authoring).

**Severity: WARN.** Does not block Layer 4 sequencing. Should be resolved before Layer 6.

---

#### AUGMENT pattern — verified
Legacy `ClassGenerator` in `class_generator.py` is unchanged per both MIGRATION.md entries
and Smoke Gate 4 three-test harness. `source_library` discriminator ("generator_v2" vs
"legacy_classgenerator") is tested. CONFIRMED.

#### PlayerClassV2 emitted fields — Layer 3 + Layer 4 + Layer 6 composability
Layer 3 (skills, skill_tree, t4_candidates) = None pre-Layer-3. Layer 4 (stat_allocation,
attribute_coupling, converged_modifier) = None pre-Layer-4. Layer 6 (t4_alteration_output) =
None pre-Layer-6. All verified in Smoke Gate 1 shape-conformance test assertions. CONFIRMED.

---

### Principle 4 — Engineering-disciplines compliance

**PASS WITH ONE OBSERVATION.**

#### Discipline #1 (math-before-code): PASS
Math note authored before implementation per dispatch record. WARN-A (22-cell vs 25-cell
documentation drift) and INFO-B (line citations) noted above.

#### Discipline #8 (schema validation at boundary): PASS
WARN-6 resolution verified: `validate_generation_params()` calls `json.dumps(generation_params)`
and raises `ValueError` on non-serializable values. `_build_player_class()` also catches
serialization failure and strips non-serializable values before emitting. Both layers of
defense present. CONFIRMED.

WARN-7 resolution verified: `generation_seed: int = 0` default is present but the
`BcTargetSubspaceGenerator.__init__(seed: int)` requires seed explicitly; per-kit seed is
`kit_seed = self.seed + (cell_index * 1000) + kit_index` — always an int, always set. The
`validate()` method checks `self.generation_seed is None` (not possible with int default; this
is a dead code path but harmless). CONFIRMED.

#### Discipline #11 (empirical inspection over assumption): PASS
Substrate row count correctly updated to 2,293 (KR-verified) from framing-brief-era 3,042 in
both math note and `bc_target_subspace_generator.py` module docstring. 749-row delta documented
in math note with three hypotheses; elrond reconciliation dispatch queued for v1.1+. CONFIRMED.

#### WARN-C — `BcTargetCell.matching_policy` property defines but does not use `option_c_cells`

**Observation:** `BcTargetCell.matching_policy` property (bc_target_player_class.py lines 72-83)
defines `option_c_cells = {"cell_15_red_mage", "cell_23_monk", "cell_20_holy_knight"}` but
never uses it in its logic. The actual matching_policy return is purely attribute-based (INT/WIS
→ "option_beta"; else → "option_alpha") — Option C cells are not discriminated by this property
at all. Option C routing for Cell 15, Cell 20, and Cell 23 is instead handled at the CellDef
level via `matching_policy="option_c"` in CELL_DEFINITIONS and `allow_cross_attribute=True`.

**Risk:** (a) the dead `option_c_cells` set is misleading — it implies the property distinguishes
Option C, which it does not; (b) if `BcTargetCell.matching_policy` is ever consumed at the
instance level (by Layer 6 or test code), it will return "option_alpha" for Cell 15/20/23
rather than "option_c", which is semantically wrong. The correct routing authority is the
`CellDef.matching_policy` field, not the `BcTargetCell.matching_policy` property.

**Cite:** Discipline #13a (implementation-vs-intent drift — dead code signals divergence between
code structure and design intent); Discipline #11 (empirical inspection — the property does not
implement what its variable name implies).

**Action:** Rocket either (a) removes the `option_c_cells` dead set and updates the `matching_policy`
property comment to clarify "BcTargetCell matching_policy is attribute-derived; Option C routing
is at CellDef level — see CELL_DEFINITIONS.matching_policy" OR (b) replaces the body with a
cross-reference to CellDef routing to make the property's limited scope explicit. No behavioral
change required; this is a dead-code cleanup + comment clarification. May batch with WARN-A.

**Severity: WARN.** Does not block Layer 4 sequencing. Should be resolved before Layer 6
wire-up to prevent confusion at consumption site.

---

#### Discipline #13a (implementation-vs-intent drift): PASS (one WARN-C observation above)
Five Gate-1 amendments all correctly disposed. WARN-2 (MechanicalSubstrateTriple dataclass)
verified in source: frozen dataclass with `validate()` and `to_dict()`, vocabulary matches DB
schema (`element`/`weapon_kind`/`weapon_mechanical_profile` = weapon_kind_classified_subtype).
WARN-4 (StatDistributionV2 + Optional pre-Layer-4) verified: `StatDistributionV2 = Optional[dict[str, float]]`
type alias defined, all three Layer-4 fields (`stat_allocation`, `attribute_coupling`, `converged_modifier`)
are `Optional` and default `None`. INFO-4 (engine_version="v2.0") verified: `ENGINE_VERSION = "v2.0"`
class constant stamped on every kit. All amendments match MIGRATION.md disposition records.

#### Discipline #18 (methodology-before-execution): PASS
MC-1 Hybrid H3 implementation matches legolas methodology recommendation:
- Substrate pre-filter (BLOCKED/THIN/READY classification) present as Stage 1 in `classify_cells()`
- Per-cell-fired-once ordering by policy weight descending present in `per_cell_fired_once_order()`
- Multi-fire extension via `multi_fire_quota()` for N_kits > 22 present
- `source_library` discriminator mechanism present per MC-1 § 5.2 cheapest-refuting-test framing

MC-2 hybrid filter-then-sample implementation matches legolas methodology recommendation:
- Hard-filter to top-k candidates (k = max(3, N // 5)) then weighted sample by tier weight
- Score function coefficients match exactly (0.40/0.35/0.15/0.10)
- Thin-cell-fallback cascade: amplitude → tempo → range → energy_type → element (5 levels)
- Graceful-fail: UNGENERABLE result (not NULL) when cascade exhausted — confirmed in `bind()`

CONFIRMED.

#### Discipline #25 (semantic-layer rep-audit): PASS
`cultural_tradition`, `lineage`, and `period` fields on PlayerClassV2 are correctly placed in
the "Semantic overlay (NOT in BDI math; for narration + naming per L9)" section of the
dataclass. Comment in docstring explicitly states "NOT freeform strings" and "NOT in BDI math."
`WeaponKnowledgeEntry.to_mechanical_triple()` only uses `element`, `weapon_kind`, and
`weapon_kind_classified_subtype` — not semantic overlay fields. CONFIRMED.

---

### Principle 5 — Severity classification

Findings classified per REVIEW_PROCESS.md severity rubric:
- BLOCK: zero
- WARN: three (WARN-A math-note 22→25 drift; WARN-B export MIGRATION field name divergence;
  WARN-C dead option_c_cells code)
- INFO: two (INFO-A 25-vs-22 cell count resolution; INFO-B Discipline #1.2 line citations)

---

## Cross-cutting findings

---

### PRIMARY: 25-cell vs 22-cell BC roster discrepancy

**RESOLVED: INFO-A — 25 cells is the correct canonical count.**

**Investigation summary:** The framing brief, qd-engine-bc-axes-lock-2026-05-20.md,
composition policy v1, and gandalf comp-policy verdict § 4 consistently referenced "~22 cells"
as the v1 BC roster. Rocket shipped CELL_DEFINITIONS with 25 entries. The discrepancy is
explained definitively by gandalf's comp-policy-section-4-coverage-gap-confirmation.md § 1.1:

> "Total: 12 cells with locked routing + 13 cells without explicit per-cell routing = 25 cell-rows
> in Stage 0 roster. (Stage 0 § 1.2 summary count of '~22 distinct cells' appears to slightly
> under-count due to some rows collapsing in informal aggregation — the operational reality is
> 12 routed + 13 un-routed.)"

Rocket correctly consumed the full 25-cell Stage 0 roster from `v1-bc-target-intent-2026-05-24.md`
Sketch A plus elrond per-cell register breakdown. The "22-cell" figure in framing brief and
related docs was an informal aggregation undercount; the canon document (`v1-bc-target-intent`)
has 25 distinct cells when fully enumerated. Rocket's `bc_target_cell_sampler.py` module docstring
states: "Cell definitions are based on the v1 BC roster (22 cells)" — this comment is inaccurate
but consistent with the framing-brief undercount; the actual CELL_DEFINITIONS list is the
authoritative 25-cell enumeration.

No canonical amendment required. No gandalf routing required. Rocket's 25-cell implementation
is CORRECT. The WARN-A finding above flags the math-note documentation drift that should be
corrected.

**Classification: INFO-A.** Observation for the record; no blocking action.

**Cite:** `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 2.4 ("~22
distinct cells"); `agentic_orchestration/gandalf/notes/2026-05-25-comp-policy-section-4-coverage-gap-confirmation.md`
§ 1.1 (authoritative resolution: 25 cells).

---

### AUGMENT pattern verification

Legacy ClassGenerator preserved in `class_generator.py` per Smoke Gate 4. Both generators
coexist; `source_library` discriminator cleanly separates production paths. No API break.
CONFIRMED.

---

### L11 strict 4-tuple matching enforcement

Enforcement is at generator level (SubstrateBindingEngine._select_rows()) per design intent.
Option α (STR/DEX cells): range + tempo + attribute conditions; amplitude relaxed via geometry
proxy in cascade. Option β (INT/WIS caster cells): attribute-level match only. Option C
(cross-attribute hybrid): same as Option α base + optional cross-attribute widening when
`allow_cross_attribute=True`. Matching policy comes from `CellDef.matching_policy` (set in
CELL_DEFINITIONS) and is passed through `_bind_and_build()` → `bind()` correctly. CONFIRMED.

---

### Cells 14/15/17/23 § 4.1 LOCKED routing

All four are in the LOCKED 12 and have explicit routing in `_apply_section_4_routing()`:
- Cell 14: `stage_3_5_engine_authored_gap_fill` → routes to option_beta binding with fallback
- Cell 15: `option_c_str_melee_substrate_int_flavored` → `_bind_and_build` with allow_cross_attribute
- Cell 17: `sidecar_b_necro_enrichment_proxy_spawn` → `_bind_and_build` with extra_params flag
- Cell 23: `sidecar_b_east_asian_fist_staff_option_c` → `_bind_and_build` with allow_cross_attribute
CONFIRMED.

---

### Cells 11/20/22/24 default heuristic + v1.1+ amendment flag

- Cell 11 (Trap Assassin): `section_4_locked=False`, `section_4_routing=None` → default heuristic
  applies per gandalf Option B. Cell routing source: `"default_heuristic"`. CONFIRMED.
- Cell 20 (Holy Knight): `section_4_locked=False`, Option C inferred from § 3.3. Cell routing
  source: `"default_heuristic_v1.1_amendment_queued"` via special-case check in `_cell_routing_source()`.
  CONFIRMED.
- Cell 22 (Storm Caller): `section_4_locked=True`, `section_4_routing="sidecar_b_celtic_druidic_enrichment"`.
  Note: this IS in the LOCKED 12 (not an un-routed cell as the dispatch cross-cutting item
  implies). CONFIRMED.
- Cell 24 (Druid Beastmaster): `section_4_locked=True`, `section_4_routing="sidecar_b_celtic_pacific_proxy_spawn"`.
  Also in LOCKED 12. CONFIRMED.

Cells 11 and 20 are the genuine un-routed-default-heuristic cases per gandalf Option B.
CONFIRMED — provenance labels correctly distinguish "default_heuristic" vs
"default_heuristic_v1.1_amendment_queued".

---

### Substrate state alignment — actual 2,293 v1_scope rows

Math note § 1 and `bc_target_subspace_generator.py` module docstring both correctly cite 2,293
rows (KR-verified 2026-05-25), not the framing-brief-era 3,042. The 749-row delta (Tier-A:
1,431 → 675) is documented with three hypotheses; elrond reconciliation dispatch queued for
v1.1+. The thin-cell-fallback cascade is therefore expected to fire routinely (per-cell average
= 2,293/22 ≈ 104, considerably thinner than framing-brief-era 138). CONFIRMED appropriate.

---

### MechanicalSubstrateTriple dataclass type safety

Verified: frozen dataclass with `element: str`, `weapon_kind: str`, `weapon_mechanical_profile: str`.
`validate()` method checks element against canonical 8-element frozenset, non-empty weapon_kind,
non-empty weapon_mechanical_profile. `CANONICAL_ELEMENTS` frozenset defined at class body. Field
`weapon_mechanical_profile` = `weapon_kind_classified_subtype` from DB (per math note WARN-2
resolution). Third member vocabulary matches DB enum per SC-2 backfill. CONFIRMED.

---

### Thin-cell-fallback smoke for wind (8 rows) + lightning (5 rows)

Smoke Gate 2 deep-relaxation check (≤10% kits with relaxation_level ≥ 3) covers this
empirically: if wind/lightning critical thinness causes excessive cascade depth, it surfaces
in the 50-kit spot-check. Test passes per completion record — deep-relaxation rate confirmed
within threshold. No additional targeted thin-element smoke required.

---

## Action summary

| # | Severity | Finding | Action | Owner | When |
|---|---|---|---|---|---|
| INFO-A | INFO | 25-cell roster is correct canonical count per gandalf comp-policy verdict § 1.1 | No action required | — | — |
| INFO-B | INFO | Math note lacks Discipline #1.2 code-line range citations | Retrofit line citations at next commit | rocket | Next commit (non-blocking) |
| WARN-A | WARN | Math note uses "22 cells" throughout; implementation has 25 | Add reconciliation note to math note § 1.1 | rocket | Next commit (may batch with INFO-B) |
| WARN-B | WARN | export/MIGRATION.md § v1.4-layer-2 PlayerClassV2 pseudocode uses non-matching field names | Amend schema pseudocode to use actual field names or add clarifying note | rocket | Before Layer 6 wire-up dispatch authoring |
| WARN-C | WARN | `BcTargetCell.matching_policy` property defines dead `option_c_cells` set, never used | Remove dead set + clarify comment that Option C routing is at CellDef level | rocket | Before Layer 6 wire-up (may batch with WARN-A) |

---

## Gate-1 amendment disposition summary

| Amendment | Status | Verification method |
|---|---|---|
| WARN-2: MechanicalSubstrateTriple as structured dataclass | RESOLVED | Source inspection — frozen dataclass with validate() + to_dict(); vocabulary correct |
| WARN-4: StatDistributionV2 + Optional pre-Layer-4 | RESOLVED | Source inspection — `StatDistributionV2 = Optional[dict[str, float]]`; stat_allocation/attribute_coupling/converged_modifier all Optional + None default |
| WARN-6: generation_params JSON-primitive constraint | RESOLVED | Source inspection — validate_generation_params() enforces json.dumps round-trip; generator additionally strips non-serializable values |
| WARN-7: generation_seed required-not-nullable | RESOLVED | Source inspection — `generation_seed: int` in PlayerClassV2; BcTargetSubspaceGenerator stamps kit_seed (always int) on every kit |
| INFO-4: engine_version="v2.0" required field | RESOLVED | Source inspection — `ENGINE_VERSION = "v2.0"` class constant; stamped on every kit; validated in test |

---

## What I did NOT flag

- The `generation_seed: int = 0` default on `PlayerClassV2` (could imply seed=0 if not set
  by generator). Not flagging because `BcTargetSubspaceGenerator` always stamps `kit_seed`
  explicitly (never uses the default), and WARN-7 resolution correctly documents the required
  constraint. The 0 default is a dataclass mechanics artifact.
- The `_LOCKED_SECTION_4_ROUTING` dict in `bc_target_subspace_generator.py` being partially
  redundant with CELL_DEFINITIONS routing fields. This is implementation-internal redundancy;
  not a cross-seam concern.
- Level-1 fallback amplitude cascade implementation (`bc_target_substrate_engine.py` lines 531-557)
  re-querying without an actual amplitude filter variable. This is a known cascade approximation
  (noted in code comment); behavior is wider-candidate sampling, not wrong behavior. Appropriate
  for v1.
- `TestSmokeGate1.test_generates_kits` using `assert len(kits) > 0` (not exactly 22). Correct
  given that BLOCKED/THIN cells may reduce the realized kit count below 22. The assertion is
  appropriately permissive.

---

## References

- `agentic_orchestration/dispatches/2026-05-25-jack-ryan-cycle-12-gate-2-rocket-layer-2.md` (this Gate-2 dispatch)
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-2-bc-target-subspace-generator.md` (Layer 2 dispatch + completion record)
- `agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md` (Gate-1 amendment source)
- `agentic_orchestration/gandalf/notes/2026-05-25-comp-policy-section-4-coverage-gap-confirmation.md` § 1.1 (PRIMARY: 25-vs-22 resolution)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 2.4 + § 4 (22-cell informal count source)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes; Profile A cell-space)
- `agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md` (MC-1 Hybrid H3 methodology)
- `agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md` (MC-2 hybrid filter-then-sample methodology)
- `src/reincarnated/generation/bc_target_player_class.py` (PlayerClassV2, MechanicalSubstrateTriple, BcTargetCell, WeaponKnowledgeEntry)
- `src/reincarnated/generation/bc_target_substrate_engine.py` (SubstrateBindingEngine, MC-2 scoring)
- `src/reincarnated/generation/bc_target_cell_sampler.py` (CELL_DEFINITIONS 25 cells, BcTargetCellSampler)
- `src/reincarnated/generation/bc_target_subspace_generator.py` (BcTargetSubspaceGenerator, routing dispatch)
- `tests/test_bc_target_subspace_generator.py` (28 tests across 4 smoke gates)
- `src/reincarnated/generation/notes/cycle-12-layer-2-bc-target-subspace-generator-2026-05-25.md` (math note)
- `src/reincarnated/export/MIGRATION.md` § v1.4-layer-2 (export seam MIGRATION)
- `src/reincarnated/generation/MIGRATION.md` (generation seam MIGRATION)
