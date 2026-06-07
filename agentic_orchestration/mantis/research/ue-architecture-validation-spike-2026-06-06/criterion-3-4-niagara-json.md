# Criterion 3.4 — Niagara VFX Consumes Engine Ability-Spec JSON

**Verdict:** IN PROGRESS (Session 1 — schema understood; execution pending UE 5.7 verification)
**Date:** 2026-06-06 Session 1

---

## 1. Engine JSON schema analysis (from cycle-14 output)

The engine kit JSON available in `agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` encodes kit BC-axis signature in the kit_id:

```
S1_endgame_bc_{engagement}_{amplitude}_{variance}_{attribute}_{support}_s{slot}
```

| Field | Values observed | Niagara mapping |
|---|---|---|
| engagement | melee / ranged / mid | Emitter type (scatter/cone/area) |
| amplitude | high / medium / low | Spawn rate / particle size |
| variance | flat / spiky / variable | Burst pattern (steady / burst / pulse) |
| attribute | str / dex / int / wis | Element family (physical / agility / magical / wisdom) |

The `wave_b_identities.json` adds:
- `kit_name_canonical` — e.g., "Ember Sweeper of the Scorch Line"
- `kit_identity_narrative` — flavor description

**Gap for criterion 3.4:** need `element_primary` and `geometry_tag` fields which appear to live in the full engine Phase 2 substrate derivation, not in the wave_b_identities output. These fields exist in the engine's kit generation pipeline (per `canonical/skill-system-2026-05-24.md`: "skill composition pattern: element × geometry × tempo × amplitude × tier_coefficient"). The cycle-14 output JSON in the meta-repo doesn't expose per-kit `element_primary` directly — it's encoded in the kit_id attribute slot (`dex` = agility/physical family, `int` = magical family, etc.).

**Practical workaround for spike:** construct 3 test ability-spec JSON files that map the known kit_id BC axes to Niagara parameters. These are derived from the kit_id encoding, not raw-generated content.

---

## 2. Test ability specs for spike

Three ability specs derived from cycle-14 Season 1 kit_ids:

### Spec A — High-frequency melee burst (fire/lightning type)
```json
{
  "kit_id": "S1_endgame_bc_melee_high_flat_str_none_s0",
  "ability_name": "Broad-Blade Sweep",
  "geometry_tag": "arc_wide",
  "element_primary": "fire",
  "tempo": "fast",
  "amplitude": "high",
  "amplitude_variance": "flat",
  "range": "melee_close",
  "niagara_hints": {
    "emitter_type": "scatter_cone",
    "color_hue": [1.0, 0.3, 0.0],
    "spawn_rate": 80,
    "particle_size": 0.8,
    "reach_m": 1.5
  }
}
```

### Spec B — Control/freeze effect (ranged, ice type)
```json
{
  "kit_id": "S1_endgame_bc_ranged_low_spiky_int_none_s0",
  "ability_name": "Frost Lock",
  "geometry_tag": "point_target",
  "element_primary": "water",
  "tempo": "slow",
  "amplitude": "low",
  "amplitude_variance": "spiky",
  "range": "ranged_long",
  "niagara_hints": {
    "emitter_type": "point_impact",
    "color_hue": [0.0, 0.7, 1.0],
    "spawn_rate": 20,
    "particle_size": 1.2,
    "reach_m": 8.0
  }
}
```

### Spec C — Shadow teleport/movement (lightning type)
```json
{
  "kit_id": "S1_endgame_bc_mid_high_flat_dex_none_s0",
  "ability_name": "Phase Step",
  "geometry_tag": "self_displacement",
  "element_primary": "shadow",
  "tempo": "fast",
  "amplitude": "high",
  "amplitude_variance": "flat",
  "range": "mid_distance",
  "niagara_hints": {
    "emitter_type": "displacement_burst",
    "color_hue": [0.3, 0.0, 0.8],
    "spawn_rate": 60,
    "particle_size": 0.6,
    "reach_m": 4.0
  }
}
```

---

## 3. Test protocol

Per dispatch § 5 test pattern:

1. Place 3 test JSON files at `Content/Data/AbilitySpecs/` in UE project
2. Create Niagara system `NS_AbilityTest`:
   - Emitter configured with User Parameters: `EmitterType` (int), `ColorHue` (vec3), `SpawnRate` (float), `ParticleSize` (float), `Reach` (float)
   - Per-emitter type: scatter_cone / point_impact / displacement_burst (3 emitter variants, activated by EmitterType parameter)
3. Blueprint Actor `BP_NiagaraAbilityTest`:
   - On Begin Play: load JSON file → parse fields → call `SetNiagaraVariableFloat`/`Vector` on attached Niagara Component
   - 3 test instances, one per spec
4. Place in test map; run in Play-In-Editor; verify visual effect visible

**UE5 JSON loading APIs:**
- Native: `FFileHelper::LoadFileToString` + `FJsonSerializer::Deserialize` (C++ required for file loading)
- Blueprint-accessible: `JsonBlueprintUtilities` plugin (UE5.7, bundled) — exposes JSON parse nodes to Blueprint
- Recommended for spike: `JsonBlueprintUtilities` plugin (avoid C++ authoring for a spike that shouldn't generate production code per dispatch § 1.2)

---

## 4. Acceptance evaluation

After test runs:
- **PASS:** 3/3 abilities produce visible Niagara effect matching spec (correct color, shape, reach)
- **YELLOW:** 2/3 PASS + documented issue on 1
- **RED:** systemic JSON ingestion failure in Niagara

---

## 5. Execution gate

**Blocked by:** UE 5.7 smoke test result.
- If PASS: create test map, author Niagara system, run spec ingestion test
- If FAIL: resolve 5.7 migration issue first

**Estimated sessions:** 1-2 sessions to author + test.

---

*Criterion 3.4 status: IN PROGRESS — schema understood, test specs drafted, execution pending UE 5.7 project verification.*
