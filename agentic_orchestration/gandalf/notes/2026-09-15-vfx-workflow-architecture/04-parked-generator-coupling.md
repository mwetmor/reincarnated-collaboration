# Parked — generator coupling removed from the VFX architecture (v1 → v2)

> **STATUS:** PARKED — gandalf, 2026-09-15. Matt's correction (verbatim): *"Bad move bringing the serial content pipeline and generator into this session. Constraining our VFX production pipeline around a content generator we haven't ran in months before we even know if we can develop a VFX workflow at all is illogical."* Everything below was in `03-architecture.md` v1 and **constrains nothing** now. Kept so the findings are not lost; re-opened only if and when a proven VFX workflow is asked to consume generator output.

**Own-goal on record:** the coupling entered through my probe brief (*"coverage of the ~411-kit corpus"*, the engine geometry palette as the grammar index) — a framing-audit Q1 failure: I assumed the generator was the VFX system's customer before the VFX system existed. Legolas answered the question asked; Astra built the resolution layer the question implied.

## What was removed from the proposal

1. **`VfxSkillSpec` as a resolution layer over emitted data** (two emission schemas — `kit_space/kits/*.json` with `geometry_type` but prose effects and no `effect_category`; `seasons/*/classes/*.json` with `effect_category` + structured effects but no geometry; 603 null geometries; `roll`/`persistent_zone`/`projectile` values outside `VALID_GEOMETRY_TYPES`). → v2 Contract I is six hand-authored specs from the source games.
2. **Eleven grammar families indexed by the engine's 26-type palette** and the coverage curves (6 families → 88 % emitted / 53 % reference; 10 → 99.5 %). → v2 needs four grammars for six skills; the corpus taxonomy stays a naming reference only.
3. **Cross-seam findings** (below) — real, but not this workstream's.
4. **A sixth "shadow" treatment** proposed because it exists in the emitted corpus. → five treatments, the ones the six skills use.
5. **Coverage-denominator fork (V10 v1)** and the "melee sweep + displacement fixture before calling it complete" requirement.

## Cross-seam findings held here (route to KR only when Matt asks)

- Nine engine geometries never emitted — `melee_strike, melee_arc, ground_slam, dash_attack, whirlwind, leap_strike, aura, orbit, placed_lane` (31 % of the reference corpus) — the emitted corpus is projectile-and-field shaped (Legolas probe 1 § 1.2).
- 87 emitted skills carry `roll` / `persistent_zone` / `projectile` with no validator alias.
- `kit_space` skills carry no typed radius / range / count / duration; 603 null geometries.
- Two emission schemas, neither a complete presentation spec.
- Last Epoch: 37 corpus kits, zero banded rows; `mortar_arc` has zero archetype members and no engine geometry.

— gandalf, 2026-09-15
