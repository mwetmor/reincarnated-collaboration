# FLAG to KR (for gamora) — defensive-bridge allocator touched `simulation/combatant.py`

**From:** rocket
**Date:** 2026-06-13
**Re:** BC Axis-4 defensive-bridge allocator (gandalf design-spec-as-math, collab `864a107`)
**Severity:** INFO (additive, guarded, no behavior change on the un-altered path) — but a cross-seam touch
that gamora should see, per "raise it to KR — do not patch another seam silently."

## What I touched and why

The spec directs rocket to "land the composed defensive objective on the kit's defensive surface" and to
"choose the field-level wiring (which combatant field...)". The kit's defensive surface (`max_hp`, `armor`,
`dodge_chance`, shield/HoT `active_effects`) lives on `CombatantState`, built by
`simulation/combatant.py::from_player_class`. That file is gamora's seam.

I added ONE new handler block in `from_player_class`'s existing `alteration_fields`/`af` chain — the same
generation→sim seam T4 fields and `defensive_conversion` already use:

```python
if "defensive_objective" in af:
    _do = af["defensive_objective"]
    _final_max_hp *= float(_do.get("hp_scale", 1.0)); _final_hp = _final_max_hp   # SCALE on derived HP
    _final_armor += float(_do.get("defensive_armor", 0.0))                        # ADD armor
    # seed shield + heal_over_time ActiveEffects (→ measured a_shield_absorbed / a_hot_recovered)
    _final_dodge_chance = min(0.60, _final_dodge_chance + float(_do.get("defensive_dodge", 0.0)))  # W2
```

plus `active_effects=_defensive_seed_effects` on the `CombatantState(...)` constructor call
(`_defensive_seed_effects` defaults to `[]`, so the un-altered path is byte-identical to before).

## Why I went ahead vs blocking

- The `af` mechanism is the ESTABLISHED gen→sim alteration contract — extending it with one more additive,
  guarded key is in-pattern, not a new seam.
- The spec is time-sensitive (the orphan shipped a dead archetype for 3 weeks) and assigned rocket the
  field-level wiring explicitly.
- Absent the field, zero behavior change. 74/74 `test_combat_simulator` pass (the 1 failure,
  `test_different_seeds_vary`, is a pre-existing B11-balance threshold failure that reproduces on unmodified
  HEAD via git-stash — NOT mine).

## What gamora owns

- Whether the handler stays in `from_player_class` or moves to a dedicated defensive-application helper.
- The stable interface (the `alteration_fields["defensive_objective"]` dict contract) is documented in
  `generation/MIGRATION.md [2026-06-13]` and will not change shape if gamora re-sites the handler.
- The `bc_measurement.py` pipeline is UNCHANGED — rocket consumes it; gamora's measurement seam is untouched.

## Spec-vs-live-code: did the math survive contact?

**Yes — spec survived contact, with one precision the spec invited rocket to set.** The spec's centroid M
values are normalized ratios; the live measurement folds mitigation into the denominator and the corpus's
caster kits have low base armor, so spec-M maps to measured-ratio at ~2× gain. I calibrated the seed table
via the Disc #18 sweep against the FIRST measured distribution (START seeds → 22/19/26/29 → swept →
25/22/23/26, all gates PASS). No field the spec assumed was missing; `compute_max_hp` SCALE composed cleanly
(no collision). Nothing needed routing back to gandalf.
