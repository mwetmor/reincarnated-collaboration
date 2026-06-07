"""
Criterion 3.4 — JSON data pipeline standalone validation
No UE APIs required. Runs with UE bundled Python or any Python 3.x.

Validates:
  1. JSON files exist and parse correctly
  2. Required fields present
  3. geometry_tag → emitter_type mapping correct
  4. element_primary in valid set
  5. color_hue in [0.0, 1.0] per channel
  6. Numeric Niagara parameters in UE-safe ranges
"""

import json
import os
import sys

ABILITY_SPEC_DIR = r"C:\dev\reincarnated-unreal\Reincarnated\Content\Data\AbilitySpecs"

SPEC_FILES = [
    "ability_spec_A_broad_blade_sweep.json",
    "ability_spec_B_frost_lock.json",
    "ability_spec_C_phase_step.json",
]

VALID_EMITTER_TYPES = {"scatter_cone", "point_impact", "displacement_burst"}

VALID_GEOMETRY_TAGS = {
    "arc_wide": "scatter_cone",
    "point_target": "point_impact",
    "self_displacement": "displacement_burst",
}

VALID_ELEMENTS = {"fire", "water", "shadow", "earth", "lightning", "wind", "holy", "poison"}

NIAGARA_PARAM_BOUNDS = {
    "spawn_rate": (1, 500),
    "particle_size": (0.1, 20.0),
    "reach_m": (0.1, 50.0),
}

COLOR_BOUNDS = (0.0, 1.0)


def validate_color(color_hue):
    if not isinstance(color_hue, list) or len(color_hue) != 3:
        return False, "Expected list of 3"
    for i, ch in enumerate(color_hue):
        if not (COLOR_BOUNDS[0] <= ch <= COLOR_BOUNDS[1]):
            return False, f"Channel {i} value {ch} out of bounds"
    return True, "OK"


def validate_niagara_param(name, value):
    if name not in NIAGARA_PARAM_BOUNDS:
        return True, "no bound"
    lo, hi = NIAGARA_PARAM_BOUNDS[name]
    if lo <= value <= hi:
        return True, f"{value} in [{lo}, {hi}]"
    return False, f"{value} OUT OF BOUNDS [{lo}, {hi}]"


def validate_ability_spec(spec):
    issues = []
    passes = []

    required = ["kit_id", "ability_name", "geometry_tag", "element_primary",
                "tempo", "amplitude", "range", "niagara_hints"]
    for f in required:
        if f not in spec:
            issues.append(f"MISSING: {f}")
        else:
            passes.append(f"field OK: {f}")

    geo_tag = spec.get("geometry_tag")
    if geo_tag in VALID_GEOMETRY_TAGS:
        expected_emitter = VALID_GEOMETRY_TAGS[geo_tag]
        actual_emitter = spec.get("niagara_hints", {}).get("emitter_type")
        if actual_emitter == expected_emitter:
            passes.append(f"geo->emitter mapping correct: {geo_tag}->{actual_emitter}")
        else:
            issues.append(f"emitter mismatch: expected {expected_emitter}, got {actual_emitter}")
    else:
        issues.append(f"unknown geometry_tag: {geo_tag}")

    element = spec.get("element_primary")
    if element in VALID_ELEMENTS:
        passes.append(f"element_primary valid: {element}")
    else:
        issues.append(f"unknown element_primary: {element}")

    hints = spec.get("niagara_hints", {})

    color_ok, color_msg = validate_color(hints.get("color_hue", []))
    if color_ok:
        passes.append(f"color_hue valid: {hints.get('color_hue')}")
    else:
        issues.append(f"color_hue invalid: {color_msg}")

    for param in ["spawn_rate", "particle_size", "reach_m"]:
        val = hints.get(param)
        if val is None:
            issues.append(f"niagara_hints.{param} MISSING")
        else:
            ok, msg = validate_niagara_param(param, val)
            if ok:
                passes.append(f"{param}={val} ({msg})")
            else:
                issues.append(f"{param}: {msg}")

    emitter_type = hints.get("emitter_type")
    if emitter_type in VALID_EMITTER_TYPES:
        passes.append(f"emitter_type in library: {emitter_type}")
    else:
        issues.append(f"emitter_type '{emitter_type}' not in library")

    return passes, issues


print("=" * 70)
print("CRITERION 3.4 — Ability-spec JSON data pipeline validation")
print("Standalone (no UE required) — validates JSON schema + Niagara bindings")
print("=" * 70)

all_results = []
overall_pass = True

for spec_file in SPEC_FILES:
    path = os.path.join(ABILITY_SPEC_DIR, spec_file)
    print(f"\n[SPEC] {spec_file}")

    if not os.path.exists(path):
        print(f"  ERROR: not found at {path}")
        all_results.append((spec_file, "RED", ["file_not_found"], []))
        overall_pass = False
        continue

    with open(path, "r", encoding="utf-8") as f:
        try:
            spec = json.load(f)
            print(f"  JSON parse OK — {len(spec)} keys")
        except json.JSONDecodeError as e:
            print(f"  JSON parse ERROR: {e}")
            all_results.append((spec_file, "RED", [str(e)], []))
            overall_pass = False
            continue

    print(f"  kit_id: {spec.get('kit_id')}")
    print(f"  ability_name: {spec.get('ability_name')}")
    print(f"  geometry_tag->emitter: {spec.get('geometry_tag')}->{spec.get('niagara_hints', {}).get('emitter_type')}")
    print(f"  element: {spec.get('element_primary')} | color: {spec.get('niagara_hints', {}).get('color_hue')}")
    print(f"  spawn_rate={spec.get('niagara_hints', {}).get('spawn_rate')} | size={spec.get('niagara_hints', {}).get('particle_size')} | reach={spec.get('niagara_hints', {}).get('reach_m')}m")

    passes, issues = validate_ability_spec(spec)
    for p in passes:
        print(f"  OK {p}")
    for i in issues:
        print(f"  XX {i}")

    if not issues:
        verdict = "PASS"
    elif len(issues) <= 1:
        verdict = "YELLOW"
        overall_pass = False
    else:
        verdict = "RED"
        overall_pass = False

    all_results.append((spec_file, verdict, issues, passes))
    print(f"  => {verdict}")

print("\n" + "=" * 70)
print("SUMMARY:")
pass_c = sum(1 for _, v, _, _ in all_results if v == "PASS")
yellow_c = sum(1 for _, v, _, _ in all_results if v == "YELLOW")
red_c = sum(1 for _, v, _, _ in all_results if v == "RED")

for fname, verdict, issues, passes in all_results:
    print(f"  {verdict:6s} - {fname} ({len(passes)} checks pass, {len(issues)} issues)")

print(f"\n  PASS={pass_c}  YELLOW={yellow_c}  RED={red_c}")

if red_c == 0 and yellow_c == 0:
    print("  DATA PIPELINE: PASS")
    print("  All 3 ability specs parse + validate correctly.")
    print("  Niagara parameter bindings are structurally sound:")
    print("  - geometry_tag->emitter_type mapping: complete")
    print("  - element_primary->color_hue: within [0.0, 1.0]")
    print("  - spawn_rate / particle_size / reach_m: within UE-safe ranges")
    print("  Next: author Niagara system NS_AbilityTest with User Parameters,")
    print("  wire to BP_NiagaraAbilityTest Blueprint, verify in PIE.")
    print("  CRITERION 3.4: PASS (data pipeline) / PENDING visual VFX in PIE")
elif red_c == 0:
    print("  DATA PIPELINE: YELLOW")
else:
    print("  DATA PIPELINE: RED")

print("=" * 70)
sys.exit(0 if overall_pass else 1)
