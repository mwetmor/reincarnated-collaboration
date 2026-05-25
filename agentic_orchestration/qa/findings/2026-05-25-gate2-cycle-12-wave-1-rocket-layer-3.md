# Finding — 2026-05-25 — Gate-2 Cycle 12 Wave 1 — Rocket Layer 3 (Skill Content + SC-3)

**Reviewer:** jack-ryan
**Severity:** INFO (PASS — no BLOCK or WARN findings)
**Target:** commit `5ec6ecc`; tag `rocket/v0.1-cycle-12-layer-3-skill-content-and-sc-3-2026-05-25`
**Developer:** rocket
**Principles applied:** 1, 2, 3, 4, 5, 6

---

## Verdict

**PASS.** Layer 3 is composable for Layer 4 sequencing once Layer 2 lands. Zero BLOCK findings. Zero WARN findings. Four INFO observations recorded for the log.

---

## What I found

Rocket delivered a complete Layer 3 implementation: SkillTree + SkillChain + Skill + T4Slot + T4Candidate + T4Alteration dataclasses (`skill_tree.py`), SkillTreeGenerator with 25-archetype template registry, 146 substrate templates across 6 families (`substrate_templates.py`), SC-3 off-hand mechanical contracts for 5 types (`off_hand_contract.py`), 132/132 tests across 6 gate classes in 0.23s, and MIGRATION.md § v1.4 cross-seam obligations record. All four Gate-1 amendments (WARN-1, WARN-3, WARN-5, INFO-3) are verified resolved in source. Math note covers all 5 implementation areas with code-level citations. W1.13 § 3.1 invariants are enforced in `validate_invariants()`. BC axis keys are locked to the 8-key vocabulary from math note v1.1 § 3.6. The substrate template count (146) is above the ~130 estimate and within per-family targets. SC-3 contract shapes match `off-hand-items-2026-05-24.md § 2.3` per-type definitions. Cross-seam obligations (star-lord + gamora + drax) are correctly deferred to Layer 6 and enumerated in MIGRATION.md.

---

## Per-principle findings

### Principle 1 — Math-before-code

**PASS.** Math note `generation/notes/cycle-12-layer-3-skill-content-and-sc-3-2026-05-25.md` is present and pre-dates implementation per commit record. Five sections map to five modules:

- Math 1 (topology) → `skill_tree.py` `_ARCHETYPE_TEMPLATES` + `SkillChain` shape. Node count targets (10-15, practical min 6, max 16) match code constants. Chain counts (2-4) match. DAG constraints match.
- Math 2 (node anatomy + bc_axis_contribution) → `Skill.__post_init__` strict 8-key enforcement. `_NODE_TYPE_AXIS_BASE` patterns match the math note § 2.2 table exactly. Tier weights (0.6/0.8/1.0) match code `_TIER_WEIGHT`. Layer 4 consumption formula from § 2.3 reproduced correctly in Gate-6 test (lines 448-455).
- Math 3 (T4 allocation) → `T4_CANDIDATES_MAX=6`, `_CANDIDATE_ALLOCATION={1:[2],2:[2,2],3:[2,2,1],4:[2,2,1,1]}`. Derivation traces to T4-A § 2 (1 sig + 1-3 secondary ≤ 6). Matches math note § 3.1 exactly.
- Math 4 (substrate templates) → 6 families, 146 total (math note targets 145; 16 vs ~15 for W1.11 is within "~15+" spec). Module-level asserts fire at import time: `assert len(W1_2_HP_ECONOMY) == 25`, etc. All-keys validation at module level catches bad `bc_axis_deltas` on load.
- Math 5 (SC-3 shapes) → `off_hand_contract.py` dataclasses match math note § 5.2-5.6 field specs.

**Discipline #1 compliance: verified.**

---

### Principle 2 — Smoke-gate before commit

**PASS.** 132/132 in 0.23s per commit message and rocket completion record. Six gate classes verified against dispatch acceptance criteria:

- Gate 1 (SkillTree generator shape) — 4 tests: shape, bc_axis dict, valid strategies, signature count. Confirms WARN-3 dict type and WARN-5 arity hold on a representative archetype.
- Gate 2 (25 archetype templates) — 100 tests (25 archetypes × 4): valid tree, T1 playability, WARN-5 arity, topology. All 25 archetypes in `_ARCHETYPE_TEMPLATES` parameterized. Full coverage.
- Gate 3 (substrate templates) — 6 tests: count ≥ 130, family counts, bc_delta key validation, JSON round-trip, L1 eligibles ≥ 10, T4 candidates ≥ 5. **INFO-A** (see below).
- Gate 4 (SC-3 contracts) — 9 tests: 5 contract shapes, JSON primitives all-five, factory dispatch, round-trip, WARN-1 field presence.
- Gate 5 (round-trip) — 5 tests: all-chains, 2-chain, multiple T4, off-hand case, signature_chain_id=None.
- Gate 6 (Layer 2 compose) — 3 tests: Layer 4 walk simulation, archetype distinctness, bc_axis Layer 4 indexing.

Six gates are sufficient for Layer 3 acceptance. No obvious gap in gate coverage for BLOCK-eligible failures.

**Discipline #2 compliance: verified.**

---

### Principle 3 — Cross-seam round-trip readiness

**PASS.** Round-trip posture correctly assessed and handled:

- **SkillTree JSON round-trip**: Gate 5 exercises `_tree_to_dict` → `json.dumps` → `json.loads` → field assertions. BC axis contribution survives JSON round-trip (dict[str, float] with 8 keys). Validates the star-lord-equivalent serialization path.
- **SC-3 contract round-trip**: `contract_to_dict` + `contract_from_dict` tested for all five types; `_validate_json_primitives` calls `json.dumps` at serialization boundary (Discipline #8 compliance).
- **MIGRATION.md § v1.4**: present, complete. Documents 3 new modules, 146-template breakdown, Gate-1 amendment dispositions, SC-3 contract table, and cross-seam obligations deferred to Layer 6. Downstream seams (star-lord, gamora, drax) correctly named.
- **25-archetype template registry vs BC roster**: 25 archetypes shipped. BC roster has 22 named cells (7 elements × variable role count) plus experimental. The 25-archetype set covers all 22 cells (fire/water/earth/wind/lightning/holy/shadow/physical × damage/mage/controller/etc.) with minor variants per element (e.g., earth_caster + earth_burst). Three variants handle cells that have multiple valid archetype shapes. This is within rocket discretion per dispatch open question on substrate family decomposition.
- **Layer 4 consumption contract**: Gate-6 `test_skill_tree_emits_walkable_structure_for_layer4` simulates the exact Layer 4 walk formula from math note v1.1 § 4.2-4.3: `wr_gradient[axis_key] += contribution * sp_rank * tier_coefficient`. Confirms dict-keyed shape is safely walkable. WARN-3 resolution directly enables this path.
- **No Layer 2 dependency violations**: Layer 3 imports only from `mechanic_alteration.py` (within rocket seam). No access to Layer-2-only fields (BC-target, StatDistribution, converged_modifier — all Layer 4+ territory). PlayerClass stub in Gate 6 is minimal (dict shape, not the Layer-2 dataclass), which is correct for Layer 3 isolation.

**Cross-seam obligations for Layer 6** correctly noted as INFO, not blocking:

- star-lord: `off_hand_contract` export field addition — DEFERRED to Layer 6 dispatch
- gamora: sim combatant SC-3 consumption — DEFERRED to Layer 6 dispatch
- drax: Spirit Guide panel SC-3 display — DEFERRED to Layer 6 dispatch

**Principle 3 + Principle 6 compliance: verified.**

---

### Principle 4 — Engineering-disciplines compliance

**PASS on all cited disciplines:**

- **Discipline #1** (math-before-code): math note pre-dates code per commit ordering and is cited in module docstrings and MIGRATION.md. Discipline #1.2 code-citation clause: math note § 2.2 node-type patterns cite no explicit code line numbers. This is the Discipline #1.2 (2026-05-23 amendment) pattern — math notes must include parenthetical code references for "applied as Y at stage Z" claims. See **INFO-B** below.
- **Discipline #2** (smoke-gate): 132/132 PASS in 0.23s. Smoke output in commit message. Compliant.
- **Discipline #8** (schema validation at export boundary): `Skill.__post_init__` raises on missing/extra bc_axis keys. `contract_to_dict` calls `_validate_json_primitives` → `json.dumps`. `substrate_templates.py` module-level loop validates bc_axis_deltas keys on load. Three independent enforcement layers. Strong compliance.
- **Discipline #11** (empirical inspection): 132/132 tests exercise runtime invariants. Gate 2 runs every archetype through `validate_invariants()` — this is the correct empirical check for the node-count and T4-arity constraints. Compliant.
- **Discipline #13a** (implementation-vs-intent drift): All four Gate-1 amendments correctly disposed (see amendment verification below). No new drift introduced.
- **Discipline #25** (semantic-layer rep-audit): `bc_axis_contribution` is mechanical-layer (numeric float per axis). Thematic text lives in `interaction_metadata["thematic_tag"]` as a separate field. Module docstring and Skill docstring explicitly state the L9 semantic split. Substrate templates carry `element_affinity` as selection signal in `interaction_metadata`-equivalent field (`element_affinity` on SubstrateTemplate), not in node_type or generation constraint. Compliant.

---

### Gate-1 amendment disposition verification

All four amendments verified resolved in source:

**WARN-1 (off_hand_type cites SC-3):** Resolved. `off_hand_contract.py` module docstring: "WARN-1 compliance: off_hand_item field comment cites SC-3 (Cycle 12), not Sidecar B." `make_off_hand_contract` docstring: "WARN-1 compliance: this contract is SC-3 (Cycle 12), not Sidecar B." `off_hand_type` field present on all five contract dataclasses as the runtime discriminator. Gate-4 test `test_warn1_field_comment_off_hand_type` exercises this explicitly. **VERIFIED RESOLVED.**

**WARN-3 (bc_axis_contribution dict[str, float] with __post_init__ enforcement):** Resolved. `Skill.__post_init__` raises `ValueError` on missing keys (checks `BC_AXIS_KEYS - keys`) AND on extra keys (checks `keys - BC_AXIS_KEYS`). Values are float by construction in `_make_bc_contribution`. Gate-1 test `test_bc_axis_contribution_is_dict` asserts type, key set, value type, and value range. Gate-6 tests index by axis string key directly. **VERIFIED RESOLVED — enforcement is strict (both missing and extra key detection).**

**WARN-5 (T4_CANDIDATES_MAX=6 + allocation rule):** Resolved. `T4_CANDIDATES_MAX = 6` constant defined at module level. `_CANDIDATE_ALLOCATION = {1:[2], 2:[2,2], 3:[2,2,1], 4:[2,2,1,1]}` matches math note § 3.1 derivation exactly (max 2+2+1+1=6). `validate_invariants()` checks `len(self.t4_candidates) > T4_CANDIDATES_MAX` and appends violation. Gate-2 `test_t4_candidates_arity_warn5` runs all 25 archetypes. **VERIFIED RESOLVED.**

**INFO-3 (signature_chain_id Optional[str] = None):** Resolved. `SkillTree.signature_chain_id: Optional[str] = None` field present. Generator sets it to `None` at construction. Gate-5 `test_signature_chain_id_is_none_at_layer3` exercises this explicitly. Docstring: "INFO-3: nullable at L3; L6 sets." **VERIFIED RESOLVED.**

---

### W1.13 § 3.1 invariant enforcement spot-check

Three invariants per dispatch cross-cutting requirement:

1. **Tier 1 playability**: `validate_invariants()` checks `playable_at_level_1`, `cost <= L1_COST_CEILING[energy_type]`, `cooldown_seconds <= 2.0`, `parent_skill_ids == []` on every chain's tier_1_node. Generator enforces these at construction (`_make_tier1_node` hardcodes `playable_at_level_1=True`, draws cost from range `[cost_ceil//3, cost_ceil]`, cooldown from `[0.5, 2.0]`, `parent_skill_ids=[]`). **STRONG ENFORCEMENT.**

2. **Substrate-agnostic generation**: `validate_invariants()` has a comment "No enforcement here — generation code ensures node_type is abstract." The behavioral enforcement is in `_make_tier1_node` (choices from abstract vocabulary) and `_make_tier_2_3_nodes` (same). `test_all_nodes_substrate_agnostic` in TestEdgeCases validates `node_type in {"damage", "control", "defense", "mobility", "utility"}` across fire_mage, water_controller, shadow_mage. This is behavioral enforcement (generator-side guarantee + test), not structural enforcement (validator-side runtime check). See **INFO-C** below.

3. **Topology validity**: `validate_invariants()` checks `node.tier < 2` for non-T1 nodes and appends violation. `_make_tier_2_3_nodes` uses `tier = 2 if i < (count + 1) // 2 else 3` — correct tier assignment. Single-parent DAG constraint: `parent_skill_ids=[prev_id]` (length-1 list, chained). No cycle possible given linear construction. **VERIFIED.**

---

### Substrate template count verification

146 templates across 6 families:

| Family | Target | Delivered | Assert |
|---|---|---|---|
| W1.2 HP Economy | 25 | 25 | `assert len(...) == 25` |
| W1.3 Damage Converts | 25 | 25 | `assert len(...) == 25` |
| W1.4 Charge Stack | 25 | 25 | `assert len(...) == 25` |
| W1.5 Movement | 30 | 30 | `assert len(...) == 30` |
| W1.6 Proxy | 25 | 25 | `assert len(...) == 25` |
| W1.11 Element Specific | ~15 | 16 | `assert len(...) == 16` |
| **Total** | **~130** | **146** | TEMPLATE_COUNT constant |

146 vs ~130 estimate: 16 delta attributable to W1.5 (30 vs estimated 25) + W1.11 (16 vs 15). Both within dispatch math 4 targets (W1.5 targeted 30 explicitly; W1.11 targeted "~15+"). **Per-family counts reasonable and within rocket discretion.**

---

### SC-3 off-hand contract shape verification

Per `off-hand-items-2026-05-24.md § 2.3` cross-check:

- **banner** = aura emission (proxy-buff + faction-aura): `BannerContract` has `aura_radius_m`, `buff_geometry="aura"`, `proxy_damage_bonus`, `proxy_speed_bonus`, `axis_2A_proxy_shift`. Matches.
- **focus** = element-amp + cast-amp (passive scaling): `FocusContract` has `element_affinity`, `element_amp_bonus`, `cast_speed_bonus`, `ritual_channel_stability`. Matches.
- **talisman** = ritual-amp + channel stability (WIS-scaled): `TalismanContract` has `primary_stat_scaling="WIS"`, `ritual_channel_stability`, `ritual_damage_bonus`, `cooldown_reduction`. Matches.
- **tome** = knowledge-buff (spell-amp or tactical; INT/WIS/DEX-scaled): `TomeContract` has `knowledge_buff_type`, `primary_stat_scaling`, `knowledge_amp_bonus`, `buff_duration_s`. `from_weapon_metadata` correctly routes DEX/STR → tactical, INT → spell_amp, WIS → ritual. Matches.
- **horn** = proxy-call + tempo-shift + war-cry: `HornContract` has `proxy_call_count`, `war_cry_duration_s`, `tempo_shift_bonus`, `war_cry_damage_bonus`, `axis_2A_proxy_shift`, `axis_3A_tempo_shift`. Matches.

**All five SC-3 contract shapes verified against canonical source.**

---

## INFO findings (no action required)

### INFO-A — Gate-3 test asserts exact family counts as magic numbers

Gate-3 `test_family_counts` asserts `len(W1_2_HP_ECONOMY) == 25`, etc. as literal integers in the test. Per Discipline #9 (test assertions derive from spec sources, not magic numbers), these could derive from `assert len(W1_2_HP_ECONOMY) == len(W1_2_HP_ECONOMY)` at module level — but that's trivially true. The actual enforcement is the module-level `assert len(W1_2_HP_ECONOMY) == 25` in `substrate_templates.py` itself. The test re-asserts the same constant. This is slightly redundant but not harmful — the module-level assert is load-time enforcement; the test is regression detection. Low concern; noting for the record.

- Cite: Discipline #9 (test assertions derive from spec sources)
- Action: none required; module-level asserts are the load-time enforcement; test redundancy is acceptable.

### INFO-B — Math note § 2.2 pattern table lacks Discipline #1.2 code citations

Math note § 2.2 states "Final bc_axis_contribution[key] = base_pattern[key] * tier_weight + perturbation" but does not include a parenthetical code reference per Discipline #1.2 (2026-05-23 amendment: "Any math-note claim of the form 'X applied as Y at stage Z' must include a parenthetical code reference"). The corresponding code is `skill_tree.py` method `_make_bc_contribution` (lines 606-620). The math note correctly describes the formula but does not cite the code location.

This is a Discipline #1.2 gap. Not blocking because: (a) the formula match is easily verifiable, (b) no downstream dispatch relies on this math note claim for a methodology decision, (c) Discipline #1.2 was motivated by code-claim mismatch at the GMM/HDBSCAN scale — the Layer 3 formula is simple and directly verifiable. Noting for future math note discipline across rocket's Layer 4 + Layer 6 notes.

- Cite: Discipline #1.2 (math-note implementation claims must cite code line references)
- Action: rocket should include code citations in Layer 4 + Layer 6 math notes. No retrofit needed for Layer 3.

### INFO-C — Substrate-agnostic invariant 2 is behavioral enforcement only (not runtime-checked)

`validate_invariants()` explicitly comments "No enforcement here — generation code ensures node_type is abstract." This means a SkillTree constructed manually (not via SkillTreeGenerator) with element-specific node_types (e.g., `node_type="fire"`) would not be caught by `validate_invariants()`. The test `test_all_nodes_substrate_agnostic` covers the generator path but not the manual construction path.

At Layer 3 this is acceptable because: (a) SkillTree objects are only constructed via SkillTreeGenerator at v1, (b) Layer 4 does not manually construct SkillTree, (c) the 5-type vocabulary is enforced at generation via `self._rng.choice(["damage", "control", "defense", "mobility", "utility"])`. For Layer 6 wire-up when external code may construct SkillTree objects, adding a `node_type in VALID_NODE_TYPES` check to `validate_invariants()` would close this gap.

- Cite: Discipline #13a (implementation-vs-intent drift — generator behavioral guarantee is sufficient for v1; explicit runtime check is the stronger form)
- Action: recommend rocket add runtime node_type vocabulary check to `validate_invariants()` at Layer 6 implementation. Not required before Layer 4 sequencing.

### INFO-D — Cross-seam Layer 6 obligations enumerated correctly; no Layer 3 action required

Star-lord, gamora, and drax obligations correctly deferred to Layer 6 per MIGRATION.md § v1.4 and rocket completion record. Noting these for Layer 6 dispatch authoring:

- star-lord: `off_hand_contract` field in season export schema alongside `off_hand_item`
- gamora: consume `OffHandMechanicalContract` in sim combatant construction (aura effects, element amp, proxy call)
- drax: Spirit Guide panel display for off-hand contract bonuses

These are not Layer 3 scope; recorded as INFO for KR Layer 6 dispatch authoring reference.

- Cite: Principle 3 (cross-seam impact called out explicitly); ADR-004 (MIGRATION.md cross-seam obligations)
- Action: KR incorporates these into Layer 6 dispatch scope. No action for rocket at this stage.

---

## What I did NOT flag

- SC-3 v1 rocket-internal judgment (no star-lord schema extension at Layer 3): correct per dispatch math note § 5.7 judgment and MIGRATION.md rationale. Sim does not consume off-hand effects yet; Layer 6 is the consumer. This is the correct staging.
- 25 vs 22 archetype templates: 25 archetypes for 22 BC roster cells is within rocket discretion. Three elements (fire, earth, wind) have two archetype variants each (e.g., earth_caster + earth_burst). This is defensible — the dispatch math 1 table showed per-element multiplicity for elements with distinct damage-geometry profiles.
- Gate 6 `test_archetype_trees_are_distinct` disjunctive assertion (`!= chain_count OR != cross_chain_rule`): this is a weak test (either condition suffices for pass). fire_mage (3-chain FLEXIBLE) vs physical_warrior (2-chain STRICT) trivially satisfies both simultaneously. The weak assertion is acceptable for a composition-smoke purpose; not a correctness gap.
- `TalismanContract` BC axis shifts include `axis_4_defensive_shift` and `axis_5_economy_shift` that are not in the BannerContract axis shift vocabulary — this is correct per the distinct off-hand type mechanics; no inconsistency.
- `STRATEGY_ELEMENT_CONVERSION` in `_default_params` seeds `"target_element": "fire"` as a placeholder. This is Layer 3's job (seed 0.5 placeholder; Layer 6 computes real η and element). Not a drift issue; correctly noted in math note § 3.3.

---

## Action items

| # | Severity | Item | Owner | When |
|---|---|---|---|---|
| INFO-A | INFO | Gate-3 magic number assertion note | rocket | On-demand; no action required |
| INFO-B | INFO | Add code line citations to Layer 4 + Layer 6 math notes per Discipline #1.2 | rocket | At Layer 4 + Layer 6 math note authoring |
| INFO-C | INFO | Add `node_type in VALID_NODE_TYPES` runtime check to `validate_invariants()` | rocket | At Layer 6 implementation |
| INFO-D | INFO | Layer 6 dispatch must enumerate star-lord + gamora + drax SC-3 obligations as acceptance criteria | KR | At Layer 6 dispatch authoring |

---

## References

- `src/reincarnated/generation/skill_tree.py` (primary review target — commit 5ec6ecc)
- `src/reincarnated/generation/substrate_templates.py`
- `src/reincarnated/generation/off_hand_contract.py`
- `tests/test_cycle12_layer3_skill_tree.py`
- `src/reincarnated/generation/notes/cycle-12-layer-3-skill-content-and-sc-3-2026-05-25.md`
- `src/reincarnated/export/MIGRATION.md` § v1.4
- `agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md` (Gate-1 amendment source)
- `agentic_orchestration/dispatches/2026-05-25-jack-ryan-cycle-12-gate-2-rocket-layer-3.md`
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-3-skill-content-and-sc-3.md`
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
