# QD-Engine Rebuild W0.4 — Rocket Seam Code-Side Audit

**Date:** 2026-05-21
**Author:** rocket
**Seam tag:** `rocket/v1.23-w0-4-code-side-audit-1`
**Dispatch:** `agentic_orchestration/dispatches/2026-05-21-rocket-plus-gamora-plus-star-lord-w0-4-specialist-code-audit.md`
**Authority:** AUTONOMOUS per Matt directive (hive activation 2026-05-21; gandalf attestation § 5)

---

## HIGH-Risk LC Verdicts

### LC-001 — Archetype template hardcoded dict

**Verdict: DRIFT-FROM-AUDIT (positive drift — already migrated)**

**Key files inspected:**
- `src/reincarnated/generation/b6_archetype_templates.py:290-305` (D3 composition at boot)
- `src/reincarnated/generation/archetype_composer.py:1-880` (D3 Path-a engine)

**Finding:** The jack-ryan Phase 1 audit documented LC-001 as a frozen 14-template hardcoded dict. This is **no longer accurate**. D3 Phase-1 P1 (tagged `gamora/v1.4-d3-path-a-impl-1`) replaced the hardcoded dict architecture with on-boot composition:

- `b6_archetype_templates.py:290-305` contains `_build_archetype_templates()` which calls `archetype_composer.compose_from_config()` at module import time
- `ARCHETYPE_TEMPLATES` is now populated at boot from `SubstrateIdentity × Role → ArchetypeTemplate` via `archetype_composer.py`
- Physical archetypes (`hunter`, `physical_warrior`, `physical_grappler`, `physical_skirmisher`, `rogue`) remain in `PHYSICAL_ARCHETYPE_TEMPLATES` (lines 117-235) — preserved as explicit hardcoded templates (physical is not in the canonical-7 rotating set; this is by design per the D3 math note § 2.3)
- `hybrid_mage` RETIRED 2026-05-18; commented-out template in `_HYBRID_ARCHETYPE_TEMPLATES` (lines 245-272)
- `HYBRID_FORBIDDEN_PAIRS` derived at boot from `substrate.forbidden_hybrid_with` (lines 315-329, D3 WP-11)

**W0.2 prerequisite structural inventory — current ARCHETYPE_TEMPLATES composition:**

The ArchetypeTemplate dataclass (`b6_archetype_templates.py:56-110`) has these fields per template:

| Field | Type | Description |
|---|---|---|
| `archetype_tag` | str | e.g. "fire_mage", "earth_controller" |
| `kit_min / kit_mode / kit_max` | int | triangular distribution for kit size |
| `aoe_share_min / aoe_share_max` | float | fraction of kit slots with AOE geometry |
| `dominant_share / secondary_share / tertiary_share` | float | element distribution fractions (sum to 1.0) |
| `chain_count_min / chain_count_max` | int | skill chain count range |
| `tier_depth` | int | 3 = generalist, 4 = specialist |
| `cross_chain_rule` | str | "STRICT" or "FLEXIBLE" |
| `required_roles` | list[tuple[str,int]] | guaranteed (role, min_count) pairs |
| `geometry_bias` | dict[str, float] | geometry weight multipliers (BIAS_PREFERRED=2.0, PENALIZED=0.1) |
| `energy_type` | str | "mana" / "rage" / "combo" / "focus" / "stamina-as-resource" |
| `skill_power_tier` | int | base magnitude = tier² |
| `special_constraints` | list[str] | symbolic constraint tags enforced by kit builder |

**D3 composition-driven fields (archetype_composer.py):**

Kit parameters are role-driven (`_KIT_SIZES`, `_AOE_SHARES`, `_CHAIN_COUNTS`, `_REQUIRED_ROLES`, `_BASE_ELEMENT_DISTRIBUTION` at lines 88-128). Geometry bias is composed as S_w(g) × R_w(g) product of substrate affinity × role preference, clamped to [0.05, 4.0] (lines 183-216). Stat allocation is substrate.scaling_attribute-primary × role.stat_emphasis-secondary (lines 260-350). Energy type and skill_power_tier derived from substrate identity (archetype_composer lines 353-450 area).

**Role × substrate matrix (from archetype_composer.py _TAG_ALIASES + composed archetypes):**

Composition roles: `burst_damage`, `area_damage`, `control` × 7 canonical substrates (fire/water/earth/wind/lightning/holy/shadow) = 21 pairs → 18 distinct tags after alias collapse (fire/water burst=area share same tag). Plus physical (5 templates) = 23 total. hybrid_mage RETIRED.

| Substrate | burst_damage tag | area_damage tag | control tag |
|---|---|---|---|
| fire | fire_mage | fire_mage (alias) | fire_controller |
| water | water_mage | water_mage (alias) | water_controller |
| earth | earth_burst | earth_caster | earth_controller |
| wind | wind_burst | wind_caster | wind_controller |
| lightning | lightning_mage | lightning_caster | lightning_controller |
| holy | holy_mage | holy_caster | holy_controller |
| shadow | shadow_mage | shadow_caster | shadow_controller |
| physical | hunter, physical_warrior, physical_grappler, physical_skirmisher, rogue (hardcoded) |

**BC-target implicit assumptions in composed templates:**
- All elemental substrates: `energy_type="mana"`, `skill_power_tier=50`
- Physical warrior/grappler: `energy_type="rage"`, `skill_power_tier=65` (~1.69× magnitude correction)
- Hunter/skirmisher/rogue: `energy_type="focus"/"combo"`, `skill_power_tier=58` (~1.35× magnitude correction)
- Experimental: `skill_power_tier=50` (no tier compensation)
- `ARCHETYPES_FORBIDDEN_CLOSE_RANGE` = {fire_mage, water_mage} (lines 343-347; earth_caster, wind_caster NOT in list — asymmetry per LC-013)

**W0.2 implications:** Under substrate-as-cohesion-only, archetype templates are the W0.2 removal target. The D3 Path-a composition (on-boot from SubstrateIdentity × Role) is already the intermediate architecture. W0.2 REMOVES the composed template structure entirely, replacing it with direct substrate-identity-driven kit generation. The five physical-substrate hardcoded templates are the most structurally resistant to W0.2 (they carry role-specific geometry biases not expressible via a substrate identity × role formula alone — `require_cleave`, `require_escape_mobility`, `require_2_mobility` etc.).

---

### LC-002 — Fire selection bias

**Verdict: VERIFIED (structural presupposition confirmed; ablation not yet run)**

**Key files inspected:**
- `src/reincarnated/element/selector.py` (full; 737 lines)
- `data/seasonal_elements/pool.json` (156 entries inspected)

**Finding:** Two structural surfaces identified as fire-selection-bias contributors:

**Surface 1 — D1 allow-list pool imbalance (lines 601-609, `_weighted_sample`):**
Allow-list entries receive 2× sampling weight. Allow-list counts: fire=20, earth=22, water=11, wind=7. Fire has nearly 3× more allow-list entries than wind. Under the `_deterministic_fallback()` path (lines 536-598), fire-slot candidates with 20 allow-list entries vs wind's 7 creates a structural 2× advantage for allow-list fire words. However, this affects only *which word* is selected per slot — selection is still one word per slot per season — not per-season fire frequency.

**Surface 2 — Element selection is per-slot (one fire per season guaranteed):**
Each season selects exactly one element per slot (fire, wind, water, earth). The 23.6% over-representation telemetry finding (B14.5 sidecar) is about SKILL element distribution within a season (dominant_share × kit_size × archetype count), not element slot selection frequency. The structural presupposition is in `ELEMENT_AFFINITY` at `b6_archetype_templates.py:36-46`:

```
"fire": ["wind", "earth"]   # fire pairs with wind and earth
"wind": ["fire", "water"]   # wind pairs back with fire
```

Fire's affinity pairing with wind and earth means fire-dominant archetypes pull wind and earth into their secondary/tertiary distributions, not water. Under the current 4-element rotation, fire archetypes are as frequent as any other elemental archetype (1:1 by season), but the cross-element contamination from ELEMENT_AFFINITY produces higher fire-flavor skill counts in seasons where fire is theme_element.

**Ablation hypothesis (Discipline #13b):** The fire 23.6% vs 20% expected finding may be partially attributable to: (a) fire's element affinity pulling it into secondary slot of wind-dominated and earth-dominated kits more frequently than water does, since `ELEMENT_AFFINITY.wind = [fire, water]` creates fire as one of only two valid secondaries for wind-dominant kits; (b) archive-history artifact from early seasons where fire was more frequently the theme_element (Discipline #11.1 state-space conditioning: this would need to be conditioned by season count). Ablation: regenerate 10 seeds with fire allow-list weight halved and compare per-archetype skill-element distributions.

**Cross-seam contract:** Element selection output (`SeasonalElements.fire_slot.element_name`) is passed to class generator as `dominant_element` for fire-type classes. No direct cross-seam contract gap here — the bias is upstream of the export boundary.

---

### LC-006 — Canonical-four LLM exposure (rocket-side verification)

**Verdict: SUBSTANTIALLY-RESOLVED with one test-coverage gap noted**

**Key files inspected:**
- `src/reincarnated/element/selector.py:43-56` (`_get_valid_slots`)
- `src/reincarnated/element/selector.py:65-73` (`_SYSTEM_PROMPT`)
- `src/reincarnated/element/selector.py:386-458` (`_build_d1_rubric_questions`)
- `src/reincarnated/element/selector.py:612-674` (`_build_prompt`)
- `src/reincarnated/canonical/library_generator.py:77-111` (`_generate_entry`)
- `tests/test_no_canonical_four_in_llm_prompts.py:1-511`

**Finding per site:**

**selector.py:43-56 (`_get_valid_slots`):** Internal routing only. Canonical-four labels ("fire", "wind", "water", "earth") used as routing keys for slot identification. Not LLM-visible. VERIFIED COMPLIANT.

**selector.py:65-73 (`_SYSTEM_PROMPT`):** Uses grouping-layer labels (ignition/suffusion/bulwark/displacement) exclusively. Stage 3 note confirms canonical-four replaced. VERIFIED COMPLIANT. Test guard `TestElementSelectorSystemPrompt` at test file lines 408-429 covers this.

**selector.py:386-458 (`_build_d1_rubric_questions`):** Q7 (lines 442-448) contains `"fire / wind / water / earth"` as text in a rubric question asking whether a proposed word structurally implies one of the canonical labels. This is legitimate audit-flag use — the question IS the Discipline #14 leak-check tool. Q7 is audit-only (explicitly: "a Y answer does NOT reduce the score or block allow-list status"). VERIFIED COMPLIANT per W0.6 jack-ryan disposition.

**selector.py:612-674 (`_build_prompt` user prompt):** The output JSON example at lines 663-674 contains:
```
"fire_slot": {"element_id": "ember"},
"wind_slot": {"element_id": "gale"},
"water_slot": {"element_id": "tide"},
"earth_slot": {"element_id": "stone"}
```
These are internal routing keys that the LLM sees as the required output format. The slots themselves are framed as "ignition/suffusion/bulwark/displacement" throughout the prompt body (lines 638-642, 652-655). The `_format_pool()` function (lines 688-711) uses `_SLOT_TO_GROUPING` to display only grouping-layer labels. However, `fire_slot`/`wind_slot`/`water_slot`/`earth_slot` appear as OUTPUT KEY NAMES in the example — the LLM reads these as format keys, not as conceptual labels. These are technically visible to the LLM.

**Test coverage gap confirmed:** `tests/test_no_canonical_four_in_llm_prompts.py:19-22` explicitly states: "This test does NOT cover the element selector LLM call (selector.py) because that call's output JSON keys (fire_slot/wind_slot/etc.) are internal protocol keys, not player-visible." The test only checks `_SYSTEM_PROMPT` text. `_build_prompt()` user content with `fire_slot`/`wind_slot` example keys is NOT tested by the no-canonical-four guard.

**Assessment:** The output key exposure (`fire_slot` etc.) was documented in W0.6 jack-ryan disposition as: "The JSON output keys (fire_slot, wind_slot, water_slot, earth_slot) remain as internal protocol routing keys — they are NOT the slot labels the LLM reasons about." This is architecturally correct — the LLM uses these as format keys, not as conceptual framing. But the W0.6 action item stated: "Rocket W0.4 section should confirm test coverage extends to `selector.py` prompt construction path. If test currently only covers `naming.py`, add a coverage assertion for `_build_prompt()` output."

**Confirmed:** Test does NOT extend to `_build_prompt()` user prompt content. The `fire_slot` key exposure in example JSON is present at `selector.py:665-668`. The W0.6 action item to add a coverage assertion for `_build_prompt()` is NOT yet complete. This is not a phase-blocking issue (W0.6 classified as non-blocking for this specific item) but should be logged as a follow-on action.

**`canonical/library_generator.py:84`:** `"Element: {element}"` in `_generate_entry()` user prompt exposes canonical element name to LLM. This is the one-time canonical library setup script. Per W0.6 jack-ryan disposition: this is a structural non-issue (canonical layer generation, not per-season generation). VERIFIED per W0.6 disposition.

**LC-006 overall rocket-side verdict:** SUBSTANTIALLY-RESOLVED. Cipher migration is live at all per-season LLM prompt construction sites. Residual: (1) `_build_prompt()` `fire_slot`/`wind_slot` example keys visible to LLM (not per-season framing, architecturally acceptable per W0.6); (2) test coverage for `_build_prompt()` user prompt not yet added (W0.6 action item outstanding).

---

### LC-007 — Humanoid gear schema

**Verdict: VERIFIED (schema confirmed as humanoid-presupposing; migration not shipped)**

**Key files inspected:**
- `src/reincarnated/generation/gear_schema.py:1-311`
- `src/reincarnated/generation/gear_catalog.py:8-156`
- `src/reincarnated/generation/gear_generation.py:263-354`

**Confirmed humanoid-presupposing surfaces:**

`gear_schema.py:29-34` (`BaseItemType`): `slot` field with values "weapon" / "armor" / "accessory" / "off_hand"; `handedness` "1h"/"2h".

`gear_schema.py:131-177` (`GearInstance`): `slot`, `handedness` fields; `dominant_element`.

`gear_schema.py:198-216` (`Loadout`): `weapon`, `off_hand`, `armor`, `accessory` named fields; `_is_off_hand_active()` gated on `handedness == "1h"`.

`gear_catalog.py:12-42`: `BASE_ITEMS` list with sword, dagger, staff, wand, orb, bow, grimoire, greatsword, helmet, chest, robe, hood, ring, amulet, shield, off_hand_dagger, off_hand_sword, focus — medieval humanoid equipment.

**LC-007 disposition (DEFER to P4 W4.1) confirmed as appropriate:** The gear schema is the foundational humanoid-presupposing cluster. No migration shipped. Position C migration (slot-as-functional-mechanic + embodiment-as-narrative-skin) is locked in canonical docs but not yet implemented.

---

### LC-008 — STR/DEX/INT math-bearing labels

**Verdict: NEEDS-DOWNSTREAM-FIX (generation-side complement to star-lord finding)**

**Key files inspected:**
- `src/reincarnated/generation/gear_generation.py:263-354`
- `src/reincarnated/generation/gear_schema.py:151`

**Finding:** `_compute_stat_requirements()` at `gear_generation.py:263-286` uses short-form keys `"str"`, `"dex"` in the output dict:
```python
return {"str": stat_floors.heavy_floor}
return {"dex": stat_floors.ranged_floor}
return {"str": ..., "dex": ..., "_any": 1.0}
```
`can_equip()` at `gear_generation.py:289-315` builds a `stat_map` keyed by `"str"`, `"dex"`, `"int"`, `"wis"`, `"vit"` (lines 305-311). These are short-form abbreviations of STR/DEX/INT, not canonical humanoid labels, but they are the implementation tokens that map to `actor_stats.strength`, `.dexterity`, `.intelligence`.

The LC-008 canonical position is PRESERVE (math-bearing labels survive as abstract power dimensions; LLM-visible narrative reframes per-embodiment per Discipline #14). The `can_equip()` logic is math-bearing and form-agnostic at the engine level. The LLM exposure risk (star-lord's `naming.py:323` finding of `stats.as_dict()` in name_class prompt) is a star-lord-seam issue. Rocket-side generation does not expose `str`/`dex`/`int` strings directly to LLM at generation time.

**Cross-seam note:** Star-lord's `NEEDS-DOWNSTREAM-FIX` verdict at `naming.py:323` is the actionable site. Rocket-side: no additional fix required beyond the LLM-visibility gate that must be resolved in star-lord seam.

---

### LC-012 — Foundation validator

**Verdict: RESOLVED (confirmed; W0.3 work, no drift)**

Per AGENT_STATE.md W0.3 entry (2026-05-21): foundation validator updated from 4-rotating+1-physical to accept 1-7 rotating substrates from CANONICAL_SUBSTRATES. Engine commit `3e428ae`, tag `qd-rebuild/v0.3-foundation-validator-7-substrate`. Backward compat: existing 4-rotating+physical seasons validate unchanged. Confirmed no drift.

---

## § 2.8 W1.13 Current-State Findings

**Finding: Skill-tree-node infrastructure FULLY ABSENT from generation seam. W1.13 builds NEW infrastructure.**

**Files inspected:**
- `src/reincarnated/generation/b6_kit_builder.py` (893 lines, full)
- `src/reincarnated/generation/class_generator.py` (key sections)
- `src/reincarnated/generation/b6_archetype_templates.py` (full)

**Confirmed absent:** No `SkillTreeNode`, `TreeNode`, `skill_tree`, `node_subset`, `per_node_coefficients`, `bc_coordinate`, or any skill-tree-node structure exists in any of these files. Kit builder operates on `_SlotPlan` objects (tier/chain/role/element per skill) and `ArchetypeTemplate` objects. There is no concept of a skill tree node — only a flat kit list organized by tier and chain.

**What exists today:** `TIER_UNLOCK_REQUIREMENTS` dict at `b6_archetype_templates.py:386-390` (min ranks in Tier N-1 parent to unlock T2/T3/T4) and `TIER_SCALING_BANDS` at `b6_archetype_templates.py:378-384` are progression-adjacent, but these are kit composition parameters, not skill-tree-node objects.

**ArchiveEntry implications:** Per star-lord's W0.4 finding, a new `archive_entries` table is required for `archive_entries` (node_subset, per_node_coefficients, scalar_modifier, bc_coordinate, per_tier_WR, cohesion_theme, visual_identity). Rocket-side complement: the GENERATION of these fields also requires new infrastructure. Specifically:
- `node_subset` and `per_node_coefficients` must be produced by the generation seam when creating a kit for QD archive submission
- Currently the generation seam produces a flat `PlayerClass.skills` list — no subset-gating, no per-node coefficient fields
- W1.13 implementation on rocket side means: modifying the class generation output schema to produce `ArchiveEntry`-compatible kit descriptions with node_subset + per_node_coefficients fields

**Actionable for W1.13 design:** W1.13 is a NEW infrastructure workstream on both rocket and star-lord seams. No existing code to modify — additive new schema and generation logic.

---

## Alt A OQ-2 + OQ-3 Findings

### OQ-2 — chain_lightning boss multi-hop behavior

**Finding: chain_lightning uses geometric-series fan-out model; boss multi-hop is NOT separately supported**

**Key files:**
- `src/reincarnated/simulation/damage_resolver.py:72-337` (chain_lightning mechanics)
- `src/reincarnated/generation/b6_kit_builder.py:776-782` (constraint)
- `src/reincarnated/generation/geometry_derivation.py:182-184, 326-330` (assignment)

**Behavior summary:** `chain_lightning` is handled by the `_FANOUT_DECAY_GEOMETRIES` path at `damage_resolver.py:323-337`. The total damage multiplier is computed as a geometric series sum: `(1 - decay^(n+1)) / (1 - decay)` where `n` defaults to `_CHAIN_DEFAULT_N=3` (primary hit + 3 arcs) and `decay` defaults to `_CHAIN_DEFAULT_DECAY=0.7`. This produces a total multiplier of approximately 2.76× for default parameters.

**Boss multi-hop question:** The simulation is solo-only (LC-010 confirmed). In a 1v1 fight (player vs boss), chain_lightning hits the single boss target once (primary hit) then has no additional targets to chain to. The geometric-series model applies the FULL multiplier to the boss (all arcs resolve on the same target). This is the VS2a solo-sim approximation — all arc hits sum onto the single defender. There is no "bin-limited" multi-hop in the boss fight sense; the sim gives chain_lightning full geometric-series credit against a boss.

**Alt A OQ-2 verdict:** chain_lightning is NOT bin-limited against boss in the current solo sim. It receives full geometric-series multiplier regardless of target count. This is an approximation acceptable for VS2a but should be noted: in a real multi-target fight (post-P4), chain_lightning would NOT collect full multiplier on the boss because arcs would hop to nearby enemies. The solo-sim OVER-estimates chain_lightning's boss damage vs what a multi-target environment would produce. File:line: `damage_resolver.py:325-337`.

---

### OQ-3 — 5-skill kit generation anomaly

**Finding: No hard 5-skill minimum; kit sizes governed by template triangular distribution; minimum can go below 10 for templates with kit_min=10 only under rounding edge cases**

**Key files:**
- `src/reincarnated/generation/b6_kit_builder.py:129-135, 218-346`

**Kit size logic:** `_sample_kit_size()` at `b6_kit_builder.py:129-135` uses triangular distribution over `(kit_min, kit_mode, kit_max)`. Templates have minimums: elemental mage/caster/controller = kit_min=10 or 12; hunter/physical = kit_min=10; rogue = kit_min=12.

**5-skill anomaly surface:** The `_plan_tier_counts()` function at `b6_kit_builder.py:312-346` allocates kit_size across tiers using band constraints:
- Specialist (4-tier): T1: 3-5, T2: 3-5, T3: 2-4, T4: 1-3
- Generalist (3-tier): T1: 4-6, T2: 5-7, T3: 3-5

For a kit_size=10 specialist (min=10), the minimum sum is 3+3+2+1=9 — one less than 10. The "last tier gets remainder clamped to band" logic at line 342-346 could in theory produce a kit with T4 receiving fewer skills than the floor if remaining < lo. With kit_size=10 and `remaining` going to T4 = `10 - (T1+T2+T3) ≥ 10 - (5+5+4) = -4`, the floor-clamping at `max(lo, min(hi, remaining))` would clamp to `max(1, min(3, negative))` = 1. So minimum kit size in practice is constrained by the band minimums, not a hard 5-skill floor.

**Alt A OQ-3 verdict:** No hard 5-skill kit size in the code. The anomaly description ("5-skill kit generation anomaly") as a kit-construction edge case may refer to an observed output during Alt A spot-check regens, not a code constraint. The `_plan_tier_counts()` logic can in theory produce uneven distributions for very small kits, but the template kit_min=10 floor prevents generating kits below 10. If a 5-skill kit was observed, it would be from a corrupted template or a deliberate future change. File:line: `b6_kit_builder.py:312-346`.

---

## MEDIUM-Risk LCs — Rocket Seam Quick Verdicts

| LC | Constraint | Rocket Touch? | Status / Finding |
|---|---|---|---|
| LC-013 | Mage range constraint | YES | `b6_archetype_templates.py:343-347`: ARCHETYPES_FORBIDDEN_CLOSE_RANGE = {fire_mage, water_mage}. Confirmed: earth_caster and wind_caster NOT in list (acknowledged asymmetry per audit). VERIFIED. |
| LC-014 | D1 pool humanoid-fantasy bias | YES | `selector.py:404-456`: Q4 syllable-cap gate active; Q2 `{word}-bolt/{word}-armor` unamended. FORMALLY-DEFERRED per W0.6 disposition. No code change needed in W0.4. |
| LC-018 | Energy homogeneity | YES (gen) | Generation energy_type fields present in ArchetypeTemplate but all elemental archetypes use `energy_type="mana"`. Physical archetypes use rage/combo/focus. Structural homogeneity within elemental class confirmed. VERIFIED as DOCUMENTED. |
| LC-022 | Substrate-expansion archetype matrix gap | YES | RESOLVED — D3 composition now generates templates for lightning/holy/shadow at boot via archetype_composer.py. 11 new tags (lightning_mage/caster/controller, holy_mage/caster/controller, shadow_mage/caster/controller, earth_burst, wind_burst) all present in ARCHETYPE_TEMPLATES. LC-022 is DRIFT-FROM-AUDIT (positive drift). |
| LC-025 | Charge-stack/damage-taken-converts bins deferred | Partial | No charge-stack or CWDT-style skill generation found in ability_grammar.py or b6_kit_builder.py. HP-cost skill type not generated (confirms LC-030). VERIFIED as absent. |
| LC-026 | Mana bug — non-mana classes get mana | YES | `simulation/combatant.py:362-375`: energy_type branches on `_ENERGY_CONFIGS`; rage/combo/focus/stamina-as-resource all get their own pool config, NOT mana. Mana bug RESOLVED. DRIFT-FROM-AUDIT (positive drift). |
| LC-028 | Single-word rule | YES | `selector.py:658`: enforced in `_build_prompt()` rules block ("Names must be single words (hyphens OK; no spaces)"). W0.6 REVISE-CANONICAL-DOC action outstanding; no code change needed. VERIFIED. |
| LC-030 | HP-cost skill variety gap | YES | No `hp_cost` or `cost_type` field anywhere in generation seam (`ability_grammar.py`, `b6_kit_builder.py`, `class_generator.py`). HP-economy Axis 5 bin will be EMPTY in QD archive until generation extended. VERIFIED as ABSENT. |

---

## Cross-Seam Boundary Notes

**LC-001 archetype tag → telemetry:** Archetype tags (`fire_mage`, `earth_controller`, etc.) surface in telemetry via `CombatantState.archetype` (simulation seam). D3 composition produces 23 tags vs the original 13. Any telemetry queries that enumerate hardcoded archetype tags (e.g., gamora analysis scripts) need updating for new composed tags. No MIGRATION.md entry was filed for this; should be noted for gamora/star-lord awareness.

**LC-006 test coverage gap → star-lord:** The W0.6 action item for `_build_prompt()` test coverage is a rocket-seam addition to `tests/test_no_canonical_four_in_llm_prompts.py`. This file is in the engine repo (not star-lord's seam), but star-lord originally wrote the test. Rocket should own the addition since it covers rocket-seam code.

**LC-007 gear schema → drax:** Position C migration will require Loadout schema changes that surface in `reincarnated-loadout/` (drax seam). Per W0.6 disposition, MIGRATION.md + Discipline #15 UI decomposition required when dispatch fires.

**LC-022 positive drift → gamora:** D3 composition ships 11 new archetype tags (lightning/holy/shadow variants). Gamora's simulation must handle these archetypes. Per AGENT_STATE.md, season_100005 showed these archetypes generating and converging — confirms simulation handles them. No new cross-seam gap surfaced.

---

## New HIGH-Risk LC Discovery

**None.** No new HIGH-risk LCs discovered during inspection. No phase-halt triggered.

---

## Summary

| LC | Verdict | Primary File:Line |
|---|---|---|
| LC-001 | DRIFT-FROM-AUDIT (positive — D3 composition live) | `b6_archetype_templates.py:290-305`; `archetype_composer.py` |
| LC-002 | VERIFIED (structural presupposition confirmed; ablation pending) | `selector.py:601-609`; `b6_archetype_templates.py:36-46` |
| LC-006 | SUBSTANTIALLY-RESOLVED (test gap outstanding) | `selector.py:65-73, 663-674`; `library_generator.py:84` |
| LC-007 | VERIFIED (humanoid presupposition confirmed; deferred) | `gear_schema.py:29-34, 131-177, 198-216`; `gear_catalog.py:12-42` |
| LC-008 | NEEDS-DOWNSTREAM-FIX (star-lord `naming.py:323`; rocket side clean) | `gear_generation.py:263-315` |
| LC-012 | RESOLVED (W0.3; no drift) | `foundation/foundation.py:39-65` |
