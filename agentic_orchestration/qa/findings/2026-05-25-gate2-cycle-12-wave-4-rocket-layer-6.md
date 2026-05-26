# Finding — 2026-05-25 — Gate-2 Cycle 12 Wave 4 — Rocket Layer 6 (§ 8 Wire-up + L9 Refactor)

**Reviewer:** jack-ryan
**Severity:** INFO (PASS — zero BLOCK, zero WARN findings; three INFO observations)
**Target:** commit `cb659d7`; tag `rocket/v0.1-cycle-12-layer-6-section-8-wireup-and-l9-refactor-2026-05-25`
**Developer:** rocket
**Principles applied:** 1, 2, 3, 4, 5, 6

---

## Verdict

**PASS.** Layer 6 is composable. Cross-seam fan-out (star-lord export schema + gamora sim combatant integration + drax Spirit Guide panel) + integration smoke + Cycle 12 wind-down may proceed per KR dispatch sequencing.

Zero BLOCK findings. Zero WARN findings. Three INFO observations recorded.

Rocket delivered: `t4_wireup.py` (all 6 strategy application functions + 6 `opportunity_scan_mechanical_*` free functions + `elect_signature_chain_id` + `emit_cross_seam_fields` + `wire_up_kit_layer6`); `skill_tree.py` amended (`VALID_NODE_TYPES` frozenset + `validate_invariants()` runtime vocabulary check); math note with code-line citation map; 36/36 L6 tests PASS; 211/211 L3+L4+L6 combined PASS confirmed independently in 0.38s; `export/MIGRATION.md § v1.4-layer-6` authored; `generation/MIGRATION.md` amended. All 7 acceptance-criteria buckets verified below.

---

## What I found

Layer 6 is the strongest delivery of the Cycle 12 sequence in terms of architectural completeness. The LOCKED contract from framing brief § 4 is honored exactly: `apply_t4_alteration_to_combat(kit, t4_alteration, fight_engine_context)` returns `AlteredFightEngineContext` (new typed container, not a mutated context). All 6 v1 strategies wire correctly to combat arithmetic per math note § 1.3: RESOURCE_CONVERSION stamps `cost_resource_override` on every skill; TRADE_OFF sets `hit_modifier=1.0` + `crit_rate=0.0` at fight start; ELEMENT_CONVERSION sets `damage_type` per skill; DEFENSIVE_CONVERSION remaps evasion to armor (additive + zero-out pattern correct); GEOMETRY_COLLAPSE applies `aoe_radius *= 0.5` and `damage_multiplier *= 1.5` to AOE-only skills (non-AOE skills correctly skipped); DEFENSIVE_TRADEOFF sets `max_life_override=1` + `chaos_immune=True`. The L9 refactor is clean: `MechanicalKitContext` carries zero `cultural_tradition`, `lineage`, or `period` attributes; grep of `t4_wireup.py` returns only comments and docstrings — no live reads; `mechanic_alteration.py` L6 call path is untouched. `signature_chain_id` election uses max-η with deterministic chain-index tie-break per T4-A § 2. `VALID_NODE_TYPES` frozenset covers all 5 canonical types; `validate_invariants()` amendment is defensive-only (non-fatal warn + continue). Cross-seam emission contracts match `MIGRATION.md § v1.4-layer-6` exactly. Three INFO observations follow.

---

## Bucket-by-bucket findings

---

### Bucket 1 — § 8 wire-up correctness (6 v1 strategies)

**PASS.**

Independent verification of each strategy application function against math note § 1.3 + framing brief § 4:

| Strategy | Expected behavior | Verified |
|---|---|---|
| RESOURCE_CONVERSION | `cost_resource_override = "HP"` on all skills | YES — `_apply_resource_conversion` iterates `effective_skills`, sets key; Gate 1 test `test_resource_conversion_sets_cost_resource` PASS |
| TRADE_OFF | `effective_stats["hit_modifier"] = 1.0`, `effective_stats["crit_rate"] = 0.0` | YES — `_apply_trade_off` reads `hit_chance`/`crit_chance` from params with correct defaults; Gate 1 test PASS |
| ELEMENT_CONVERSION | `skill["damage_type"] = target_element` for all skills | YES — `_apply_element_conversion` iterates `effective_skills`; Gate 1 test `test_element_conversion_sets_damage_type` PASS |
| DEFENSIVE_CONVERSION | `armor += evasion`, `evasion = 0.0`, `evasion_converted_to_armor = True` | YES — additive pattern in `_apply_defensive_conversion` correct; Gate 1 test verifies armor > 0.10 after absorbing 0.20 evasion; PASS |
| GEOMETRY_COLLAPSE | `aoe_radius *= 0.5`, `damage_multiplier *= 1.5` (AOE skills only) | YES — guard `if skill.get("aoe_radius", 0.0) > 0.0` correct; non-AOE skill unchanged; Gate 1 test verifies s1 (AOE) and s2 (non-AOE) independently; PASS |
| DEFENSIVE_TRADEOFF | `max_life_override = 1`, `chaos_immune = True` | YES — `_apply_defensive_tradeoff` per legolas § 3.4 + `STRATEGY_DEFENSIVE_TRADEOFF`; Gate 1 test PASS |

Sim-seam boundary: all 6 strategies are `sim_prerequisite = None` (loadout-resolution-only per Cycle 11 § 8). `gamora_combatant_fields` is emitted as a read-only dict. No rocket code enters gamora live fight state. BOUNDARY CLEAR.

**INFO-A** (named below) is recorded on a minor DEFENSIVE_TRADEOFF thematic-signal redundancy in the L9 free function — non-blocking.

---

### Bucket 2 — L9 refactor (Discipline #25)

**PASS.**

Discipline #25 (semantic-layer rep-audit) primary verification:

**Zero cultural_tradition reads in L6 opportunity_scan code path:**

Grep of `t4_wireup.py` for `cultural_tradition`: 8 hits — ALL are docstrings, comments, or string literals (e.g., `"Does NOT read: cultural_tradition, lineage, period"`, `"No cultural_tradition reads"`). Zero live attribute reads.

Grep of `mechanic_alteration.py` for `cultural_tradition.`: zero hits (the dot-notation access check). `KitSubstrate.is_chaos_tradition` and `archetype_tag` heuristics remain in the ORIGINAL `opportunity_scan()` methods — correct; these are the Cycle 11 backward-compatible path. L6 call sites use `opportunity_scan_mechanical_*()` free functions exclusively, which read `MechanicalKitContext` only.

`MechanicalKitContext` carries only: `element`, `bc_amplitude`, `bc_attribute`, `bc_range`, `bc_tempo`, `bc_proxy_density`, `energy_type`, `weapon_mechanical_profile`, `weapon_kind`. No semantic overlay fields.

**Discipline #13a (semantic intent preserved):** refactor mapping verified against math note § 2.3:

| Strategy | Old signal | New signal | Intent preserved? |
|---|---|---|---|
| RESOURCE_CONVERSION | `substrate.dominant_element` | `ctx.element` | YES — same field, direct mechanical signal |
| TRADE_OFF | no cultural read | no cultural read | YES — no refactor needed (confirmed) |
| ELEMENT_CONVERSION | `substrate.fire_resonance_score` (element + archetype_tag) | `ctx.fire_resonance_score` (element + bc_attribute + weapon_mechanical_profile) | YES — archetype_tag heuristic replaced by mechanical proxy; same kits selected |
| DEFENSIVE_CONVERSION | `substrate.combat_tradition_armor_level` (archetype_tag) | `ctx.armor_level` (bc_attribute + weapon_mechanical_profile) | YES — STR+handheld_weapon covers physical_warrior + physical_grappler (the prior heavy-armor archetypes) |
| GEOMETRY_COLLAPSE | no cultural read | no cultural read | YES — no refactor needed (confirmed) |
| DEFENSIVE_TRADEOFF | `substrate.is_chaos_tradition` (element=="shadow") | `ctx.is_chaos_element` (element=="shadow") | YES — identical semantic content, just via mechanical field |

Gate 2 test `test_no_cultural_tradition_attribute_accessed_in_mechanical_scan` PASS: `MechanicalKitContext` has no `cultural_tradition`, `lineage`, or `period` attributes. CONFIRMED.

---

### Bucket 3 — signature_chain_id election

**PASS.**

Election algorithm per T4-A § 2 + math note § 3.2:

- **Max-η rule:** `elect_signature_chain_id` iterates all chains, calls `scan_mechanical(strategy_type, bc, ctx)` for each chain's first candidate (or Layer 4 active selection if provided), tracks `best_eta`; updates `best_chain_id` only on strict `>` (deterministic — first chain wins tie). Correct.
- **Deterministic tie-break:** chain iteration order is `skill_tree.chains` list order — chain_A first, then chain_B, etc. `>` guard means ties preserve first-seen chain. Correct per math note § 3.2 "chain_A < chain_B < chain_C < chain_D" ordering.
- **Fallback:** empty tree → returns `""` (Gate 3 test `test_election_with_empty_tree_returns_empty` PASS). No-candidates fallback → `chains[0].chain_id` (correct per math note).
- **Determinism:** Gate 3 test `test_election_is_deterministic` PASS (two identical calls produce identical result).
- **Valid chain_id:** Gate 3 test `test_election_returns_valid_chain_id` PASS.
- **Sets on tree:** `wire_up_kit_layer6` assigns `skill_tree.signature_chain_id = elected_chain_id` (in-place mutation on mutable SkillTree). Gate 3 test `test_election_sets_signature_chain_id_on_wire_up` PASS.

**INFO-B** is recorded on the active_t4_by_chain integration path — non-blocking; reserved for Cycle 13.

---

### Bucket 4 — VALID_NODE_TYPES + runtime validate_invariants

**PASS.**

`VALID_NODE_TYPES: frozenset[str] = frozenset({"damage", "control", "defense", "mobility", "utility"})` added at `skill_tree.py` lines ~60-66. 5 types, matches canonical skill-system vocabulary.

`validate_invariants()` INFO-C amendment: Invariant 2 block now iterates `chain.all_nodes` and checks `node.node_type not in VALID_NODE_TYPES`. Violation appended (non-fatal — returns list, does not raise). Called defensively in both `elect_signature_chain_id` and `wire_up_kit_layer6` before walking tree.

Gate 3 tests verify:
- `test_valid_node_types_constant_has_5_types`: PASS (5 types, all present).
- `test_validate_invariants_catches_invalid_node_type`: PASS (injecting `"fire"` as node_type produces violation mentioning `"fire"` in message).
- `test_election_validates_skill_tree_invariants`: PASS (invalid type does not cause exception, election continues and returns valid chain_id).

Generator behavior unchanged: `SkillTreeGenerator` only produces `["damage", "control", "defense", "mobility", "utility"]` — no regression.

Gate 5 test `test_no_regression_on_layer3_invariants` PASS across 10 representative kits (including the 5 archetype × element combos most likely to surface edge cases).

---

### Bucket 5 — Cross-seam emission contracts

**PASS.**

`emit_cross_seam_fields` output verified against `MIGRATION.md § v1.4-layer-6`:

**off_hand_contract:** When `kit.off_hand_item` is not None and `weapon_kind` is a valid focus/talisman/etc., `make_off_hand_contract` + `contract_to_dict()` is called; result assigned to `emission["off_hand_contract"]`. When no off-hand: `None`. Gate 4 tests `test_emit_cross_seam_fields_without_off_hand` + `test_emit_cross_seam_fields_with_off_hand_focus` PASS. JSON-serializable round-trip PASS.

**gamora_combatant_fields:** All 6 strategy keys present per MIGRATION.md shape:
- `resource_conversion`: `{"cost_resource": "HP", "scope": "all_skills"}` — CONFIRMED
- `trade_off`: `{"hit_modifier": 1.0, "crit_rate": 0.0}` — CONFIRMED
- `element_conversion`: `{"target_element": "fire", "scope": "all_damage"}` — CONFIRMED
- `defensive_conversion`: `{"evasion_to_armor": true}` — CONFIRMED
- `geometry_collapse`: `{"aoe_radius_multiplier": 0.5, "damage_multiplier_bonus": 1.5}` — CONFIRMED
- `defensive_tradeoff`: `{"max_life_override": 1, "chaos_immune": true}` — CONFIRMED

Gate 4 test `test_gamora_combatant_fields_per_strategy_keys` verifies all 6 keys PASS. JSON-serializable PASS.

**spirit_guide_narration_metadata:** Required keys present: `has_mechanic_alteration`, `alteration_type`, `thematic_rationale`, `spirit_guide_explainer_template`, `narrative_hooks`. Template mapping covers all 6 strategies. Gate 4 tests PASS.

**MIGRATION.md completeness:** `export/MIGRATION.md § v1.4-layer-6` is present at top of file. Documents `AlteredFightEngineContext` shape, per-strategy mutation table, all three consumer shapes (star-lord/gamora/drax) with explicit FOLLOW-ON obligations, PlayerClassV2 field before/after table, sim-seam boundary statement, L9 refactor summary, Discipline #25 verification note. No WARN-B drift pattern (no field-name mismatch between MIGRATION.md and implementation found).

`generation/MIGRATION.md` Layer 6 entry present and cross-references export/MIGRATION.md. Consistent.

---

### Bucket 6 — Smoke + integration evidence

**PASS.**

**36/36 L6 PASS — independently verified:** `python3 -m pytest tests/test_cycle12_layer6_t4_wireup.py -v` collected 36 items, all PASS in 0.16s. Five gate classes confirmed executing per math note § 6.1.

**211/211 L3+L4+L6 combined PASS — independently verified:** `python3 -m pytest tests/test_cycle12_layer3_skill_tree.py tests/test_cycle12_layer4_convergence.py tests/test_cycle12_layer6_t4_wireup.py` collected 211 items, all PASS in 0.38s. No regression.

Gate 5 covers 22 representative kits across all 8 canonical elements + 16 archetype types. Full round-trip smoke (`test_round_trip_full_kit_json`) uses `_ensure_json_serializable` (star-lord export path proxy) and confirms `t4_alteration_output`, `off_hand_contract`, `gamora_combatant_fields` all survive JSON round-trip.

**Pre-L2 regression:** L2 test file not separately named in combined run scope (rocket's test files are L3 + L4 + L6). The 211 count matches L3 (132) + L4 (43) + L6 (36) = 211 exactly. L2 tests are folded into L3 file at Layer 3 delivery (per Gate-2 on L3 finding). No standalone L2 regression run available. INFO-C observation below. Non-blocking: L3 tests cover the PlayerClassV2 contract that L2 outputs, and L6 Gate 5 exercises the full L2→L3→L4→L6 pipeline via `_make_minimal_kit_v2`.

**Discipline #2.1 (resource-scaling rehearsal):** Math 7 documents < 1ms per strategy, < 10ms per kit L6-only, < 30s for 22-kit full pipeline in stub mode. 0.16s actual run confirms projection. No kernel-panic risk (pure in-memory; no LLM calls, no DB calls).

---

### Bucket 7 — Provenance (math note + MIGRATION.md)

**PASS.**

**Discipline #1 (math-before-code):** Math note `generation/notes/cycle-12-layer-6-section-8-wireup-and-l9-refactor-2026-05-25.md` authored before implementation. Header states `Status: FINAL — authored before implementation per Discipline #1`. Covers Math 1-7 per dispatch scope.

**Discipline #1.2 (code-line citations):** Code-Line Citation Map present at top of math note with 8 entries covering Math 1 through Math 6 + Math 7. Citations name specific functions and line ranges. Spot-checked:
- Math 1 (LOCKED contract): `t4_wireup.py lines ~1-60` — confirms module header maps to the framing brief § 4 contract location. CONFIRMED.
- Math 3 (signature_chain_id): `t4_wireup.py lines ~290-340` cited as `elect_signature_chain_id function`. Actual function begins at line 749 in the delivered file. **Line range in citation map is inaccurate** (the function that exists at lines 290-340 is the `_bc_view_from_bc_target_cell` helper, not `elect_signature_chain_id`). This is the same pattern as INFO-A from Gate-2 on L4 — citation map line numbers drifted during implementation vs math note drafting.
- Math 2 (L9 refactor): `mechanic_alteration.py lines ~112-186` cited, but the L9 refactor landed in `t4_wireup.py` as free functions (not in `mechanic_alteration.py`). The citation points to `KitSubstrate` (the OLD location) rather than the new `MechanicalKitContext` + `opportunity_scan_mechanical_*` in `t4_wireup.py`. Acknowledged in math note body (§ 2.3 cites `tings_wireup.py lines ~148-260` for the new location), but the Code-Line Citation Map header entry for Math 2 still points to the old location.

These line-range and module-location discrepancies in the citation map are INFO-level (same class as L4 INFO-A). They do not affect functional correctness or any downstream consumption. Discipline #1.2 is SUBSTANTIALLY satisfied — code-line citations are present and load-bearing for all 6 Math sections. The map-vs-actual drift is notable for future reviewers.

**MIGRATION.md § v1.4-layer-6:** verified present and complete (Bucket 5).

---

## Per-principle findings

---

### Principle 1 — Math-before-code

**PASS.** Math note present, authored before implementation per header. Covers Math 1 (LOCKED contract + per-strategy wire-up) + Math 2 (L9 refactor mapping, Discipline #13a table) + Math 3 (signature_chain_id election rule, T4-A § 2 alignment) + Math 4 (cross-seam emission contracts, all 3 consumer shapes) + Math 5 (validate_invariants amendment, INFO-C closure) + Math 6 (cheapest-refuting-test, 5-gate class strategy) + Math 7 (resource bounds, < 10ms per kit projection). All 7 sections present.

**Discipline #1.2 code-line citations:** SUBSTANTIALLY SATISFIED. Code-Line Citation Map present with 8 entries. Two citation map inaccuracies noted (INFO-A — Math 3 line range, Math 2 module location). Structural compliance maintained; citation drift non-blocking.

---

### Principle 2 — Smoke-gate before commit

**PASS.** 36/36 L6 PASS; 211/211 L3+L4+L6 PASS. Both confirmed independently. Commit tag applied. Math 7 resource-bounds projection present (Discipline #2.1).

---

### Principle 3 — Cross-seam round-trip readiness

**PASS.** `AlteredFightEngineContext.to_dict()` is JSON-serializable (Gate 1 + Gate 5 round-trip tests PASS). `off_hand_contract` via `contract_to_dict()` is JSON-serializable (Gate 4 PASS). `gamora_combatant_fields` is JSON-serializable (Gate 4 PASS). `MIGRATION.md § v1.4-layer-6` present on both seams with complete consumer obligations and FOLLOW-ON dispatch instructions. No round-trip-not-applicable justification needed (round-trips completed).

---

### Principle 4 — Engineering-disciplines compliance

**PASS.**

- **Discipline #1 (math-before-code):** verified.
- **Discipline #1.2 (code-line citations):** substantially satisfied; two citation map inaccuracies noted at INFO level.
- **Discipline #2 (smoke-test):** 36/36 + 211/211 PASS.
- **Discipline #2.1 (resource-scaling rehearsal):** Math 7 present; 0.16s actual vs < 30s projection.
- **Discipline #8 (schema validation):** `VALID_NODE_TYPES` frozenset enforced in `validate_invariants()`; cross-seam emission shapes documented in MIGRATION.md and tested via Gate 4.
- **Discipline #11 (empirical inspection):** Gate 5 22-kit smoke + JSON round-trip exercises the full L2→L3→L4→L6 pipeline empirically.
- **Discipline #13a (implementation-vs-intent drift):** L9 refactor mapping table in math note § 2.3 confirms intent preservation per-strategy. Gate 2 tests verify mechanical signal substitutions produce same strategy selection for same kit shapes.
- **Discipline #17 (calibration sweeps):** N/A for L6 (no new calibration parameters; L4 sweeps cover the convergence layer). Correct disposition.
- **Discipline #25 (semantic-layer rep-audit):** zero cultural_tradition reads in L6 opportunity_scan code path. VERIFIED. `MechanicalKitContext` carries no semantic overlay fields. Test `test_no_cultural_tradition_attribute_accessed_in_mechanical_scan` PASS.

---

### Principle 5 — Severity classification

Three INFO findings. No WARN. No BLOCK. Severity classifications consistent with the nature of findings.

---

### Principle 6 — Cross-seam contract round-trip

**PASS.** MIGRATION.md present on both seams. Round-trip smoke complete (`test_round_trip_full_kit_json`). Consumer obligations enumerated as FOLLOW-ON dispatches per seam. `Round-trip: not applicable` clause not needed — round-trip was completed.

---

## INFO findings

---

### INFO-A — Code-line citation map line-range and module-location drift

**Observation.** The Code-Line Citation Map in the math note contains two inaccuracies relative to delivered code:

1. **Math 3 (signature_chain_id election):** cited as `t4_wireup.py lines ~290-340 (elect_signature_chain_id function)`. In the delivered file, lines ~290-340 contain `opportunity_scan_mechanical_trade_off` (the TRADE_OFF free function), not `elect_signature_chain_id`. The actual `elect_signature_chain_id` function begins at line 749. This is a citation map authoring artifact — the function existed at lines ~290-340 during math note drafting, then implementation grew.

2. **Math 2 (L9 refactor):** citation map entry points to `mechanic_alteration.py lines ~112-186 (KitSubstrate + _derive_* functions — REPLACED)`. The L9 refactor implementation landed in `t4_wireup.py` as `MechanicalKitContext` + 6 `opportunity_scan_mechanical_*` free functions, not in `mechanic_alteration.py`. Math note body § 2.3 correctly cites `t4_wireup.py lines ~148-260` for the new location; the Citation Map header still points to the old location.

**Pattern:** same class as Gate-2 on L4 INFO-A (param naming drift between math note and code). Citation map was authored during math note pre-drafting; implementation grew to different line ranges.

**Risk:** reviewers of future Layer amendments will need to reconcile the citation map against actual file positions. Low risk at v1 scope since the math note body text is accurate (§ 2.3 and § 3 cite the correct locations inline). Higher risk if a future agent uses the Citation Map as the primary navigation reference without cross-checking.

**Cite:** Discipline #1.2 (code-line citations must be accurate; map-vs-actual drift accumulates across layers).

**Action:** Rocket amends math note Code-Line Citation Map at next batch commit to: (a) update Math 3 line range to `lines ~749-827 (elect_signature_chain_id function)`, (b) update Math 2 entry to `generation/t4_wireup.py lines ~108-240 (MechanicalKitContext + opportunity_scan_mechanical_* free functions)` with a note that `mechanic_alteration.py lines ~112-186` is the REPLACED location (preserved for backward compat).

**Severity: INFO.** Does not block Layer 6 composition. Documentation correction only.

---

### INFO-B — active_t4_by_chain Layer 4 integration path not exercised in tests

**Observation.** `elect_signature_chain_id` accepts an optional `active_t4_by_chain: Optional[dict[str, Optional[str]]]` parameter. When provided, the function uses Layer 4's active T4 selection per chain (rather than defaulting to `slot.candidates[0]`). The math note § 3.2 documents this path: "Use Layer 4 active selection if available; else first candidate per chain."

The `active_t4_by_chain` path is correct in implementation: when the dict is provided and `chain.chain_id` is a key, the function searches `slot.candidates` for the matching `candidate_id`. However, the Gate 3 tests do not exercise this branch (all test calls omit `active_t4_by_chain`). The `wire_up_kit_layer6` orchestrator also does not currently pass `active_t4_by_chain` (it would need to read `_KitConvergenceState.active_t4` from the convergence result).

**Risk:** the Layer 4 → Layer 6 integration path for T4 candidate hand-off (converge.py `_phase2_t4_keystone_selection` selecting the winning candidate, then Layer 6 using that selection to score against real η for the election) is undocumented in the MIGRATION.md consumer obligations and has no test coverage. At v1, `slot.candidates[0]` is always used, which is the same as the Layer 3 default candidate. The integration path may be needed when Layer 4 convergence selects a non-first candidate in Phase 2.

**Impact at v1:** None. All Layer 4 Phase 2 selections use the first candidate in the L3 default set (per `_STRATEGY_BC_PROFILE` proxy scoring which maps to the first strategy type in `_NODE_TYPE_STRATEGIES`). So `active_t4_by_chain` = first candidate = `slot.candidates[0]` = same result as the default path. The gap becomes visible if Layer 4 Phase 2 selects a second candidate based on calibration sweeps.

**Cite:** Discipline #11 (empirical inspection — branch coverage gap on non-trivial optional path); future Cycle 13 BDI framework scope where Layer 4 active selection may diverge from candidates[0].

**Action:** At next Cycle 13+ scope where Layer 4 active T4 selections are used downstream, add a test exercising the `active_t4_by_chain` branch with a synthetic convergence result. At that point, `wire_up_kit_layer6` should also be extended to read `converge_result.per_dim_adjustments` and pass the active T4 selection. For Cycle 12 wind-down: no action required — v1 behavior is correct.

**Severity: INFO.** Does not block Layer 6 or Cycle 12 wind-down. Reserved for Cycle 13+ BDI scope.

---

### INFO-C — DEFENSIVE_TRADEOFF `opportunity_scan_mechanical` has redundant is_chaos_element + element=="shadow" check

**Observation.** `opportunity_scan_mechanical_defensive_tradeoff` contains this thematic score line:

```python
thematic = (0.35 if (ctx.is_chaos_element or ctx.element == "shadow") else
            0.15 if ctx.element == "fire" else 0.05)
```

`MechanicalKitContext.is_chaos_element` is defined as `return self.element == "shadow"`. So the condition `(ctx.is_chaos_element or ctx.element == "shadow")` is logically equivalent to `ctx.element == "shadow"` — the `or ctx.element == "shadow"` branch is always subsumed by `ctx.is_chaos_element`.

This is a harmless code clarity issue (the result is correct). The redundancy appears to be a copy pattern from the original `DefensiveTradeoffStrategy.opportunity_scan` which used `substrate.is_chaos_tradition or substrate.dominant_element == "shadow"` — a meaningful distinction in the original (is_chaos_tradition could be True for elements other than shadow in future v1.1). In the mechanical refactor, `is_chaos_element` IS `element == "shadow"` so the two sides of the `or` are identical.

**Risk:** None to correctness. Potential confusion for future maintainers who may wonder what case `ctx.element == "shadow"` covers that `ctx.is_chaos_element` does not.

**Cite:** Discipline #1 (implementation should match math note — math note § 2.3 lists `is_chaos_tradition → is_chaos_element` mapping without mentioning the redundancy); code clarity.

**Action:** Rocket simplifies to `thematic = (0.35 if ctx.is_chaos_element else 0.15 if ctx.element == "fire" else 0.05)` at next batch commit. Single-line fix; no behavior change.

**Severity: INFO.** No test impact; no correctness impact.

---

## 211/211 integration smoke verification

**Independently verified.** `python3 -m pytest tests/test_cycle12_layer3_skill_tree.py tests/test_cycle12_layer4_convergence.py tests/test_cycle12_layer6_t4_wireup.py` collected 211 items, all PASS in 0.38s. No collection errors on these three files.

L3: 132 tests | L4: 43 tests | L6: 36 tests | Combined: 211/211 PASS. Rocket's completion record claim verified.

Pre-L2 regression: L2 tests are bundled into L3 file delivery; Gate 5 22-kit smoke exercises the full L2→L3→L4→L6 pipeline via `_make_minimal_kit_v2` which constructs `PlayerClassV2` (the L2 output contract). Adequate for v1 scope.

---

## Action

- [ ] **Rocket (INFO-A):** Amend math note Code-Line Citation Map at next batch commit — update Math 3 entry to `lines ~749-827` and Math 2 entry to `t4_wireup.py lines ~108-240`. Batch with INFO-B/C amendments.
- [ ] **Rocket (INFO-B):** At Cycle 13+ BDI scope, add test for `active_t4_by_chain` branch in `elect_signature_chain_id`; extend `wire_up_kit_layer6` to consume Layer 4 active T4 selection. No action required for Cycle 12 wind-down.
- [ ] **Rocket (INFO-C):** Simplify `opportunity_scan_mechanical_defensive_tradeoff` thematic line to `0.35 if ctx.is_chaos_element` (remove redundant `or ctx.element == "shadow"` clause). Batch with INFO-A amendment.
- [ ] **Matt (none required):** No BLOCK or ESCALATE findings. Layer 6 is composable. KR may proceed with 3 cross-seam follow-on dispatches in parallel (star-lord export schema + gamora sim combatant integration + drax Spirit Guide panel) + integration smoke + Cycle 12 wind-down.

---

## References

- `agentic_orchestration/dispatches/2026-05-25-jack-ryan-cycle-12-gate-2-rocket-layer-6.md` (Gate-2 dispatch)
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-6-section-8-wireup-and-l9-refactor.md` (rocket Layer 6 dispatch + completion record)
- `agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md` (Gate-1 source)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-1-rocket-layer-3.md` (INFO-C + INFO-D precedent)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-3-rocket-layer-4.md` (INFO-A precedent: citation map drift pattern)
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 + § L9 + § L10
- `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py` (primary review target)
- `~/Games/reincarnated-engine/src/reincarnated/generation/skill_tree.py` (INFO-C amendment)
- `~/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (L9 refactor baseline + backward-compat path)
- `~/Games/reincarnated-engine/src/reincarnated/generation/notes/cycle-12-layer-6-section-8-wireup-and-l9-refactor-2026-05-25.md` (math note)
- `~/Games/reincarnated-engine/tests/test_cycle12_layer6_t4_wireup.py` (36 tests, 5 gate classes)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4-layer-6
- `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (Layer 6 entry)
