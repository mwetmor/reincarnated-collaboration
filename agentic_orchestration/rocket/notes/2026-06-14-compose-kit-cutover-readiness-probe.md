# Act 1 — `compose_kit` cutover-readiness probe (read-only)

**Author:** rocket (generation seam)
**Date:** 2026-06-14
**Task:** Wire live path `season_orchestrator → class_generator.generate` to
`bc_target_composer.compose_kit()`, retiring `classify_archetype → ARCHETYPE_TEMPLATES →
b6_builder.build(label)`; archetype label becomes `synthesize_archetype_label()` (post-composition).
**Verdict: NO-GO for an immediate re-point.** Act 2 as scoped ("re-point the entry + the 5
label-consumption sites") is not a re-point — it is a multi-unit workstream with a missing adapter,
a substrate-binding design hole, an unrun calibration gate, and a cross-seam schema dependency.
This note is the readiness probe; **no code was changed.**

## 1. compose_kit production-readiness — PARTIAL (unit-clean, integration-blocked)

`compose_kit()` (`bc_target_composer.py:676`) is implemented, unit-tested
(`tests/test_w02_bc_target_composer.py`), and returns `ComposedKit | None | DeferredEvaluation`
correctly. BUT it is consumed today **only by tests + `legacy_archetype_shim.py`** — never by the
live `class_generator`/`season_orchestrator` path (grep confirms zero live references).

**Blocking gap — output type mismatch (the adapter does not exist):**
- `ComposedKit.selected_mechanics: list[PoolMechanic]` (`bc_target_composer.py:658`).
  `PoolMechanic` (`:125`) is a flat descriptor: `mechanic_id, geometry_type, effective_range_tiles,
  cost_type, cd_seconds, cc_tags, is_proxy/is_movement, skill_power_tier_base, axis hints`.
- `PlayerClass.skills` requires `Skill` (`skill_schema.py:6`) — a rich model: `abilities:
  list[Ability]` (full objects the **simulator** consumes), `effects, geometry, timing, triggers,
  canonical_element, effect_category, color_value, power_tier, scaling_attribute, tier/chain_id/
  chain_position/parent_skill_ids/scaling_coefficient, canonical_pair_ref, name, flavor_text`.
- **No `PoolMechanic → Skill` converter exists anywhere** (grep empty). The live path builds `Skill`s
  via `AbilityGrammar.generate(role, element, power_tier) → SkillComposition.compose([ability])`
  (`class_generator.py:574-582`, b6 builder). The math note (`w0-2-archetype-removal-...md`) does
  **not** specify this adapter (grep for adapter/to_player_class/Layer-3 = empty). Building it is
  net-new code requiring a Disc#1 math note.

## 2. BC-target upstream source — SHIM-STAGED (contradicts the acceptance)

The orchestrator does **not** emit BC-targets. `_generate_classes` (`season_orchestrator.py:1539-1544`)
picks `(element, energy_type, role_orientation, range_profile)` and calls `class_gen.generate(...)`.
The **only** existing route to a `BcTarget` is:
`(element,energy,role) → classify_archetype → archetype_tag → bc_target_for_archetype` (shim,
`legacy_archetype_shim.py:54-136`). **So the live BC-target source is the legacy label** — which
directly conflicts with the acceptance criterion *"zero label-as-input in the live path."* You cannot
get a BcTarget today without first computing the legacy archetype label. Satisfying "zero
label-as-input" requires EITHER (a) the orchestrator emitting BC-targets directly (the separate
`bc_target_cell_sampler`/`bc_target_subspace_generator` Cycle-12 family — a *different* pipeline that
emits `PlayerClassV2` with `skills=None` pre-Layer-3, also not skill-populated), OR (b) a net-new
`(element,energy,role) → BcTarget` mapping that bypasses the label. Both are design+code, not a re-point.

## 3. ComposedKit → PlayerClass adapter surface — DOES NOT EXIST

Beyond the skill-type gap (§1), re-pointing breaks **all 5 label-consumption sites** in
`class_generator.generate`, because `synthesize_archetype_label()` emits a coordinate string
(`"ranged-slow/large-AOE/damage-pure/glass/overflow_damage_mana"`) that none of the legacy keyed maps
recognise:
1. `ARCHETYPE_TEMPLATES.get(archetype)` → `effective_power_tier` + `cross_chain_rule` (`:371,381`) — KeyError-equivalent (None).
2. `_generate_skills(archetype_tag=archetype)` → B6 build (`:373-377`) — the path being retired; replaced by compose_kit, needs the §1 adapter.
3. `allocate_stats(archetype, rng)` (`:383`) — keyed by legacy label; needs (role, bc_target)-keyed allocation. **No such allocator exists.**
4. `_ARCHETYPE_ACTION_REGISTER` / `_ARCHETYPE_ROLE_FUNCTION` (`:413-414`) — embodiment fields keyed by legacy label.
5. `select_mechanic_alteration_from_kit_params(archetype_tag=...)` (`:430`) — **partially ready**: `mechanic_alteration.py:224` already has a `BcTargetView`; entry still keys on `archetype_tag` + `dominant_element`.

**Substrate hole:** compose_kit is substrate-AGNOSTIC (no element input, by design — substrate assigned
at Phase-5 cohesion-judge, which is **unbuilt**). The live `PlayerClass`/simulator need
`dominant_element` + per-skill `canonical_element`. Re-binding element at the adapter is the deferred
Phase-5 work, or a transitional binding must be designed — **a gandalf design call.**

## 4. W0.2 deferred obligations A3 / A4 — BOTH STILL OPEN

- **A3 (shim calibration pass/fail, math note §5 / :590):** "if >20% of shim-path kits land >1 bin from
  BC-target default on any axis, recalibrate before P5." Requires Phase-3/4 simulation. **Never run.**
  Gate for W0.2.6 MIGRATION.md.
- **A4 (v2.15 co-migration, math note §8.4 / :775):** single `ALTER TABLE` adding `archetype_label`
  (rocket spec) **+** `recompose_energy_calibration_applied` (gamora) on `class_fight_loadouts`.
  **star-lord authors** (schema owner); rocket+gamora provide specs. **Cross-seam, open.** Gates W0.2.6.

## 5. Recommended sequencing (math-before-code; gated)

Act 2 should NOT fire as a same-session re-point. Proposed staged path for KR routing:
1. **Math note (rocket):** `ComposedKit → PlayerClass` adapter + transitional substrate-binding
   (PoolMechanic→Skill via grammar/composition; element re-bind point). Disc#1.
2. **gandalf design review:** substrate-binding at generation vs deferred Phase-5; and the
   "zero-label BC-target source" decision (§2 option a vs b).
3. **Cross-seam (KR → star-lord + gamora):** close A4 (v2.15 archetype_label co-migration) before any
   live `archetype_label` emission.
4. **A3 calibration run** (needs gamora sim) before P5 progression.
5. **Then** cutover + the water_mage-coordinate clean-compose acceptance, under Gate-2 (jack-ryan) +
   gandalf review.

**water_mage note:** at the *compose_kit* level the water_mage coordinate
`("ranged-slow","large-AOE","solo","damage-pure","medium","variable","glass","overflow")` already
composes clean (no `no_heal_skill` constraint contradiction — that B6 constraint concept doesn't exist
in compose_kit). The earlier water_mage 1/29 B6 sub-band fallback is a *legacy-path* artifact that the
cutover would dissolve — but only once §1–§3 above are built.
