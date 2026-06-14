# Research — Archetype Label-as-Input Vestigial Sweep — 2026-06-14

**Mode:** A (analytical audit)
**Commissioner:** gandalf
**Scope:** generation/, simulation/, export/, output/, telemetry/ (+ doc files)
**Lock reference:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`

---

## Summary Count

| Class | Live-Path | Deprecated-Resident | Total |
|---|---|---|---|
| VIOLATION | 9 | 7 | 16 |
| COMPLIANT-OUTPUT | 8 | — | 8 |
| STALE-DOC | 3 | — | 3 |

The live-path violation cluster is concentrated in three files: `class_generator.py`, `mechanic_alteration.py`, and `season_orchestrator.py`. The deprecated-resident cluster is fully in the deprecated-in-place modules (`archetype_composer.py`, `b6_archetype_templates.py`, `b6_kit_builder.py`, `legacy_archetype_shim.py`). The simulation layer has conditional label-keyed branching (VIOLATION) but no label-as-input stat/skill generation.

---

## LIVE-PATH VIOLATIONS (highest priority — reached by season_orchestrator → class_generator.generate)

### V-1 | class_generator.py:363-367 | `classify_archetype(dominant_element, [], energy_type, role_orientation)` | VIOLATION | LIVE-PATH

Symbol: `archetype` (string result of `classify_archetype`)
Why: This is the early-derivation call that produces the label BEFORE skill generation. The label is immediately consumed by V-2, V-3, V-4, V-5. Composing a BC-target directly and sampling from it would be the lock-compliant path; deriving the label first and using it to gate templates/stats/skills is the violation.

### V-2 | class_generator.py:371-372 | `ARCHETYPE_TEMPLATES.get(archetype)` | VIOLATION | LIVE-PATH

Symbol: `archetype` (the label from V-1), `ARCHETYPE_TEMPLATES`
Why: Label string used as lookup key into the archetype template registry. The template drives `skill_power_tier` (effective_power_tier passed to AbilityGrammar), `cross_chain_rule`, geometry bias — all generation parameters. Label is INPUT to generation, not output.

### V-3 | class_generator.py:373-377 | `self._b6_builder.build(archetype_tag, ...)` | VIOLATION | LIVE-PATH

Symbol: `archetype_tag` (= label from V-1)
Why: Label string passed as first argument to `B6KitBuilder.build()`, which dispatches to `ARCHETYPE_TEMPLATES.get(archetype_tag)` (V-7 below). This is the core label-gated skill composition: which skills are generated, in what proportions, with what geometry biases, is entirely determined by the label.

### V-4 | class_generator.py:383 | `allocate_stats(archetype, rng)` | VIOLATION | LIVE-PATH

Symbol: `archetype` (label from V-1)
Why: The label is passed to `stat_allocator.allocate_stats()`, which dispatches `ARCHETYPE_TEMPLATES.get(archetype_tag)` and returns archetype-keyed stat distributions. Stats (strength/dexterity/intelligence/wisdom/vitality split) are determined by the label. This is a direct label-to-stat-generation linkage.

### V-5 | class_generator.py:413-414 | `_ARCHETYPE_ACTION_REGISTER.get(archetype)` + `_ARCHETYPE_ROLE_FUNCTION.get(archetype)` | VIOLATION | LIVE-PATH

Symbol: `archetype` (label from V-1); dicts `_ARCHETYPE_ACTION_REGISTER`, `_ARCHETYPE_ROLE_FUNCTION`
Why: Label-keyed dicts that drive `embodiment_action_register` and `class_role_function` fields on the generated `PlayerClass`. These are form/behavior fields determined by the label rather than derived from BC-coordinate measurement.

### V-6 | class_generator.py:430-436 | `select_mechanic_alteration_from_kit_params(archetype_tag=archetype, ...)` | VIOLATION | LIVE-PATH

Symbol: `archetype` (label from V-1)
Why: Label passed to mechanic-alteration selection, which internally uses it as a direct key into `_geo_map` (932-958 in `mechanic_alteration.py`) to set `damage_geometry`, and into conditional branches for `damage_tempo` (975), `damage_amplitude` (982-987), and `defensive_profile` (994-1001). The label drives which T4 alteration strategy fires. Generation input, not output.

### V-7 | class_generator.py:533 | `if not weird and archetype_tag in ARCHETYPE_TEMPLATES` | VIOLATION | LIVE-PATH

Symbol: `archetype_tag` (label); `ARCHETYPE_TEMPLATES`
Why: Conditional branch on the label to decide whether to invoke the B6 structured builder or fall back to the standard/weird generator. The label gates which generation path is taken — a structural composition fork controlled by the label.

### V-8 | season_orchestrator.py:145-146 | `classify_archetype(...)` → `ARCHETYPES_FORBIDDEN_CLOSE_RANGE` | VIOLATION | LIVE-PATH

Symbol: `expected_archetype` (label); `ARCHETYPES_FORBIDDEN_CLOSE_RANGE`
Why: `_pick_range_profile()` pre-derives the label to gate whether `close` is a valid range option. The label drives a generation-input constraint (`range_profile`) that propagates into all downstream skill generation. This is label-as-generation-constraint.

### V-9 | mechanic_alteration.py:932-1001 | `_bc_view_from_generation_params(archetype_tag=...)` — `_geo_map`, tempo/amplitude/defensive conditionals | VIOLATION | LIVE-PATH

Symbol: `archetype_tag` (label); 24-entry `_geo_map` dict; inline `if archetype_tag in (...)` conditionals at lines 975, 982, 984, 994, 996
Why: The function is a v1 approximation that reverses the correct flow — instead of receiving a measured BC-target, it RECONSTRUCTS a synthetic BC-target by looking up the label in hardcoded tables. The label is the input; the BC-target is the derived output. This inverts the lock. Lock-compliant path: receive the actual composed BC-target from `compose_kit()` instead of rebuilding it from the label.

---

## DEPRECATED-RESIDENT VIOLATIONS (present in codebase, not reached by live path)

### V-D1 | archetype_composer.py | entire module | VIOLATION | DEPRECATED-RESIDENT

Module marked DEPRECATED W0.2 Phase 2 (2026-05-21); removal gate P5 W5.X. Exports `_derive_archetype_tag(substrate, role)`, `compose_from_config()`, `_TAG_ALIASES` — the D3 Path-a composition engine that derives labels from substrate×role pairs. Still imported by `archetype_classifier.py` (V-D2) and `b6_archetype_templates.py` (V-D3). The deprecation-in-place is correct per math note §9.3; documenting for completeness.

### V-D2 | archetype_classifier.py:14 + :84 | `from .archetype_composer import _derive_archetype_tag, _TAG_ALIASES` + `return _derive_archetype_tag(dominant_element, composition_role)` | VIOLATION | DEPRECATED-RESIDENT (proximate to live path)

Symbol: `_derive_archetype_tag`, `_TAG_ALIASES`
Why: `archetype_classifier.classify_archetype()` is the function called at V-1 (live-path). The classifier itself is not deprecated, but its implementation routes through the deprecated `archetype_composer._derive_archetype_tag()`. When Rocket's cutover lands, this module will be replaced or emptied.
NOTE: this is also a LIVE-PATH violation via V-1 — listed here because the underlying derivation logic resides in the deprecated module.

### V-D3 | b6_archetype_templates.py:316-346 | `_build_archetype_templates()` + `ARCHETYPE_TEMPLATES` population | VIOLATION | DEPRECATED-RESIDENT

Symbol: `ARCHETYPE_TEMPLATES` (the live dict); `_build_archetype_templates()`
Why: Module deprecated W0.2 Phase 2; `ARCHETYPE_TEMPLATES` is the label-keyed lookup table consumed by live-path violations V-2, V-4, V-7 and simulation violations V-S1–V-S4. Deprecated-in-place per §9.3. The dict at module level is still actively consumed by live path.

### V-D4 | b6_kit_builder.py:82-84 | `ARCHETYPE_TEMPLATES.get(archetype_tag)` | VIOLATION | DEPRECATED-RESIDENT (but reached by live path via V-3)

Symbol: `archetype_tag` (label); `ARCHETYPE_TEMPLATES`
Why: `B6KitBuilder.build()` takes `archetype_tag` as first argument and immediately does `ARCHETYPE_TEMPLATES.get(archetype_tag)`. If no template, raises ValueError. Template drives all kit-building: `required_roles`, `geometry_bias`, element distribution shares, `chain_count`, `tier_depth`. This is the structural label-to-generation path.

### V-D5 | legacy_archetype_shim.py | `ARCHETYPE_TAG_TO_BC_TARGET` + `ARCHETYPE_TAG_TO_ROLE` + `bc_target_for_archetype()` | VIOLATION | DEPRECATED-RESIDENT

Symbol: 24-row `ARCHETYPE_TAG_TO_BC_TARGET` dict; `ARCHETYPE_TAG_TO_ROLE`
Why: The shim translates label → BC-target as a backward-compatibility bridge. The translation direction (label → BC, not BC → label) is the violation. Per math note §5, the shim is temporary; removal at P5 W5.X. The shim itself is not on the live generation path (nothing in season_orchestrator calls `compose_for_archetype_tag()`), but it exists and normalizes the label-as-input mental model.

### V-D6 | stat_allocator.py:118-153 | `allocate_stats(archetype_tag)` → `ARCHETYPE_TEMPLATES.get(archetype_tag)` | VIOLATION | DEPRECATED-RESIDENT (but reached live via V-4)

Symbol: `archetype_tag` (label); local `ARCHETYPE_TEMPLATES` (backed by composition)
Why: `stat_allocator.py` builds its own `ARCHETYPE_TEMPLATES` from composition at import time; `allocate_stats(archetype_tag)` looks up stat profile by label. This is the stat-assignment-by-label violation. Reached live from `class_generator.py:383`.

### V-D7 | simulation/balance_loop.py:1886, 1948, 2030, 2183 | `ARCHETYPE_TEMPLATES.get(player_class.archetype_tag)` | VIOLATION | DEPRECATED-RESIDENT

Symbol: `player_class.archetype_tag` (label); `ARCHETYPE_TEMPLATES`
Why: Four balance-loop methods (`_lever_element_distribution_variants`, `_lever_element_swap`, `_lever_skill_swap`, `_lever_geometry_resample`) look up the archetype template by label to enforce `required_roles`, geometry_bias, and element distribution bounds during recomposition. These are generation-adjacent operations (they modify the kit during balance convergence) — and they gate on the label to determine valid modifications. Under the lock, the modifier loop should constrain to BC-target bounds, not archetype-template bounds.

---

## SIMULATION VIOLATIONS (label-keyed branching in fight/balance layer, not generation per se)

### V-S1 | simulation/ai_strategies.py:292 | `if combatant.archetype in _PLAYER_CONTROLLER_ARCHETYPES` | VIOLATION | LIVE-PATH

Symbol: `combatant.archetype` (= `player_class.archetype_tag`, the label); `_PLAYER_CONTROLLER_ARCHETYPES`
Why: The fight engine branches on the archetype label to decide whether to fire control skills before DPS sorting. This is a mechanical behavior gate driven by the label. Lock-compliant path would key on Axis 2B (control density bin) or the `role_orientation` field — not the label. Commission asks specifically about simulation consuming label as input; this qualifies.

### V-S2 | simulation/ai_strategies.py:331 | `get_priority_roles(combatant.archetype, ...)` → `ARCHETYPE_ROLE_PRIORITY` lookup | VIOLATION | LIVE-PATH

Symbol: `combatant.archetype` (label); `ARCHETYPE_ROLE_PRIORITY` (24+ entry dict)
Why: The AI rotation order (which skills fire in what sequence) is keyed entirely by the archetype label. Label drives tactical behavior identity. Under the lock, combat AI rotation should follow from the kit's measured BC bins (e.g., control-density → control-first), not from the label. This is a significant simulation-layer violation.

### V-S3 | simulation/balance_loop.py:1007, 1027 | `if player_class.archetype_tag != "experimental"` | VIOLATION | LIVE-PATH

Symbol: `player_class.archetype_tag` (specific label "experimental")
Why: The label string "experimental" is used to gate whether primary and secondary recompose loops run. A non-label equivalent would be the `experimental_constraint_relaxed` list or a boolean flag. Label as gating condition for generation-adjacent behavior.

### V-S4 | simulation/balance_loop.py:2637, 2695, 2972, 3417, 3564 | `compute_balance_gear_stats(player_class.archetype_tag, p)` | VIOLATION | LIVE-PATH

Symbol: `player_class.archetype_tag` (label); `_PHYSICAL_ARCHETYPES` set in `gear_catalog.py`
Why: `compute_balance_gear_stats()` keys on the label to decide whether to add elemental resistances (physical archetypes get a resistance bonus; others do not). This is a generation-adjacent balance parameter controlled by the label.

---

## COMPLIANT-OUTPUT HITS (label emitted as name-on-top — do NOT remove)

| File:Line | Symbol | Classification | Note |
|---|---|---|---|
| output/season_writer.py:388 | `"archetype_tag": player_class.archetype_tag` | COMPLIANT-OUTPUT | JSON export field; name-on-top only. Not consumed by generation. |
| output/season_writer.py:439 | `"archetype_tag": monster.archetype_tag` | COMPLIANT-OUTPUT | Monster export; same. |
| output/season_writer.py:505 | `class_dict.get("archetype_tag") == "experimental"` | COMPLIANT-OUTPUT (boundary) | Export validation: guards skill-tier check logic in writer; reads the exported label but doesn't drive generation. Marginal but acceptable — the writer is outside the generation+simulation seam. |
| export/season_exporter.py:715, 752, 807, 815 | `archetype_tag` field reads/column-list | COMPLIANT-OUTPUT | Export schema field; not consumed upstream. |
| telemetry/recorder.py:817, 850, 1228, 1260, 1295 | `archetype_tag` / `archetype_label` fields | COMPLIANT-OUTPUT | Telemetry write-only; no downstream consumption back into generation or simulation. |
| output/summary_formatter.py:22 | `player_class.archetype_tag` | COMPLIANT-OUTPUT | Display/summary only. |
| season_orchestrator.py:1365-1379 | `_ARCHETYPE_LABEL` + `_name_class_template()` | COMPLIANT-OUTPUT | Template naming fallback only — fires when LLM naming is unavailable; produces a display name string, not consumed by generation or sim. The label is read FROM the generated class (not fed into generation). |
| bc_target_composer.py:621-638 | `synthesize_archetype_label()` | COMPLIANT-OUTPUT | Label synthesized FROM the BC-target tuple as a display string. This is the lock-done-right example: BC-target → label, not label → BC-target. |

---

## STALE-DOC HITS

### SD-1 | bc_target_composer.py:871-876 | `ORCHESTRATOR_SEVERANCE_AUDIT` block, lines "the _generate_classes() → ClassGenerator path is the legacy path currently in use" + "SEVERANCE REQUIRED: Yes" | STALE-DOC

Why: Written 2026-05-21 as a W0.2 audit finding. Describes the label-as-input live path as the CURRENT architecture and frames the new composer as a "parallel path." This note normalizes the violation for any reader who reaches it. The orchestrator integration was slated for "Phase 3 wiring" — that work is now active (Rocket's cutover). The note should be updated to reflect the in-flight cutover status.

### SD-2 | generation/AGENT_STATE.md:2371-2375 | "Mechanism (confirmed working)" section | STALE-DOC

Content: Describes the four-step label-keyed pipeline (classify_archetype → ARCHETYPE_TEMPLATES.get → template.skill_power_tier → AbilityGrammar) as CONFIRMED WORKING and presents step 3 (label lookup) as legitimate. This text normalizes the violation and will misguide any agent reading AGENT_STATE for context on what the current architecture does. Written 2026-05-19 for B6 pre-work audit.

### SD-3 | generation/MIGRATION.md:2848-2857 | W0.2.2 Orchestrator Severance Audit finding | STALE-DOC

Content: "STATUS: CONFIRMED COMPLIANT (no emergency severance required)" with explanation that classify_archetype derivation inside ClassGenerator is "a downstream classification, not an upstream selection constraint." This framing is incorrect under the lock — classify_archetype fires before skills are generated and the label it produces drives ARCHETYPE_TEMPLATES.get() and allocate_stats(). The audit was correct for W0.2 scope (no severance before smoke), but the conclusion paragraph normalizes the violation as "compliant" without that qualification. Misguides post-cutover readers.

---

## Cross-Cutting Observation

The `vestigial_labels.py` module (Session 4 Item 8, 2026-06-12) is FULLY COMPLIANT. It reads MEASURED BC bins + structural properties AFTER generation to produce a UX label string. It does not participate in any generation branching. This is the implementation pattern the lock prescribes.

The `cycle14_wave5_emitter.py:derive_archetype_tag()` and `cycle13_normal_season_export.py:_derive_archetype_tag()` are COMPLIANT-OUTPUT in context: both are export utilities that derive a label string for JSON schema population from non-generation inputs (BC attribute fields or char_id strings). They do not gate generation.

---

## Source list

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/class_generator.py` (lines 363-414, 430-436, 533-535)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/archetype_classifier.py` (full)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/archetype_composer.py` (full — DEPRECATED)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` (lines 316-388)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/b6_kit_builder.py` (lines 68-100)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/legacy_archetype_shim.py` (full)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/stat_allocator.py` (lines 118-153)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (lines 905-1026, 1115-1159)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py` (lines 41, 144-146, 542, 1365-1379)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/gear_catalog.py` (lines 165-192)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_composer.py` (lines 621-638, 845-893)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` (lines 45-101, 292, 331)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (lines 1007, 1027, 1884-1886, 1946-1948, 2025-2030, 2176-2183, 2636, 2695, 2972, 3417, 3564)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py` (lines 109, 730)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/season_writer.py` (lines 388, 439, 505)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (lines 2846-2857)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (lines 2367-2375)
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
