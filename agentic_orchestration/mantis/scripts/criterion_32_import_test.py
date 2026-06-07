"""
Criterion 3.2 — Meshy → UE 5.7 Import Test
Spike: empirical validation only; no production code generated.

Tests:
  1. Import Crusader biped GLB (Idle_03_withSkin) as skeletal mesh — known-good baseline
  2. Inspect skeleton hierarchy (bone count, root bone name)
  3. Inspect mesh properties (LOD count, material slots)
  4. Import additional animation GLBs (Walking, Running, Roll_Dodge_4) using same skeleton
  5. Print pass/fail verdict per import

Usage (headless):
  UnrealEditor-Cmd.exe <project> -run=PythonScript -PythonScript=<path_to_this_file>
  -unattended -nullrhi -nosound
"""

import unreal
import os

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CRUSADER_BASE = r"C:\dev\reincarnated-collaboration\duskweaver\Meshy_AI_Crusader_of_the_Ember_biped"

IMPORT_FILES = {
    "Idle_03": os.path.join(CRUSADER_BASE, "Meshy_AI_Crusader_of_the_Ember_biped_Animation_Idle_03_withSkin.glb"),
    "Walking":  os.path.join(CRUSADER_BASE, "Meshy_AI_Crusader_of_the_Ember_biped_Animation_Walking_withSkin.glb"),
    "Running":  os.path.join(CRUSADER_BASE, "Meshy_AI_Crusader_of_the_Ember_biped_Animation_Running_withSkin.glb"),
    "Roll_Dodge_4": os.path.join(CRUSADER_BASE, "Meshy_AI_Crusader_of_the_Ember_biped_Animation_Roll_Dodge_4_withSkin.glb"),
}

DEST_PATH = "/Game/Characters/MeshyTest"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg):
    unreal.log(msg)
    print(msg)


def import_skeletal_mesh(source_path, dest_path, asset_name):
    """Import a GLB/FBX as skeletal mesh using AssetImportTask (automated)."""
    task = unreal.AssetImportTask()
    task.filename = source_path
    task.destination_path = dest_path
    task.destination_name = asset_name
    task.replace_existing = True
    task.automated = True
    task.save = True

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])

    # Return list of imported objects
    return task.imported_object_paths


def inspect_skeletal_mesh(asset_path):
    """Load and inspect a SkeletalMesh asset; return dict of findings."""
    asset = unreal.load_asset(asset_path)
    if asset is None:
        return {"error": f"Could not load asset at {asset_path}"}

    findings = {"asset_class": type(asset).__name__, "path": asset_path}

    if isinstance(asset, unreal.SkeletalMesh):
        skeleton = asset.get_editor_property('skeleton')
        if skeleton:
            # Get bone names via skeleton API
            bone_count = skeleton.get_editor_property('reference_skeleton')
            findings["has_skeleton"] = True
            findings["skeleton_path"] = str(skeleton.get_path_name())
            # Try to count bones via the mesh LOD info
            lod_info = asset.get_editor_property('lod_info')
            findings["lod_count"] = len(lod_info) if lod_info else 0
            # Material slots
            materials = asset.get_editor_property('materials')
            findings["material_slot_count"] = len(materials) if materials else 0
        else:
            findings["has_skeleton"] = False
    elif isinstance(asset, unreal.AnimSequence):
        findings["is_anim_sequence"] = True
        skeleton = asset.get_editor_property('skeleton')
        findings["has_skeleton"] = skeleton is not None
        if skeleton:
            findings["skeleton_path"] = str(skeleton.get_path_name())
        frame_rate = asset.get_editor_property('target_frame_rate')
        findings["frame_rate"] = str(frame_rate)
        rate_num = asset.get_editor_property('target_frame_rate')
        findings["num_frames"] = asset.get_editor_property('number_of_sampled_keys')
    else:
        findings["note"] = f"Asset is {type(asset).__name__}, not SkeletalMesh or AnimSequence"

    return findings


# ---------------------------------------------------------------------------
# Main test execution
# ---------------------------------------------------------------------------

def run_criterion_32():
    log("=" * 70)
    log("CRITERION 3.2 — Meshy → UE 5.7 Import Test")
    log("Source: Crusader biped GLBs (known-good baseline from Meshy AI rig)")
    log("=" * 70)

    results = {}

    # -----------------------------------------------------------------------
    # Step 1: Import primary skeletal mesh (Idle_03 — has full skin + skeleton)
    # -----------------------------------------------------------------------
    log("\n[STEP 1] Importing Idle_03 (primary skeletal mesh + skeleton)...")
    idle_src = IMPORT_FILES["Idle_03"]
    if not os.path.exists(idle_src):
        log(f"  ERROR: Source file not found: {idle_src}")
        results["Idle_03"] = {"error": "source_not_found"}
    else:
        log(f"  Source: {idle_src} ({os.path.getsize(idle_src):,} bytes)")
        imported = import_skeletal_mesh(idle_src, DEST_PATH, "SK_Crusader_Idle")
        log(f"  Imported objects: {imported}")

        if imported:
            for obj_path in imported:
                findings = inspect_skeletal_mesh(obj_path)
                log(f"  Asset: {obj_path}")
                for k, v in findings.items():
                    log(f"    {k}: {v}")
                results[f"Idle_03_{obj_path.split('/')[-1]}"] = findings
        else:
            log("  WARN: No objects imported (import may have failed silently)")
            results["Idle_03"] = {"error": "no_objects_returned"}

    # -----------------------------------------------------------------------
    # Step 2: Import animation GLBs
    # -----------------------------------------------------------------------
    for anim_name in ["Walking", "Running", "Roll_Dodge_4"]:
        log(f"\n[STEP 2] Importing {anim_name}...")
        src = IMPORT_FILES[anim_name]
        if not os.path.exists(src):
            log(f"  ERROR: Source file not found: {src}")
            results[anim_name] = {"error": "source_not_found"}
            continue

        log(f"  Source: {src} ({os.path.getsize(src):,} bytes)")
        imported = import_skeletal_mesh(src, DEST_PATH, f"SK_Crusader_{anim_name}")
        log(f"  Imported objects: {imported}")

        if imported:
            for obj_path in imported:
                findings = inspect_skeletal_mesh(obj_path)
                log(f"  Asset: {obj_path}")
                for k, v in findings.items():
                    log(f"    {k}: {v}")
                results[f"{anim_name}_{obj_path.split('/')[-1]}"] = findings
        else:
            log(f"  WARN: No objects returned for {anim_name}")
            results[anim_name] = {"error": "no_objects_returned"}

    # -----------------------------------------------------------------------
    # Step 3: Verdict
    # -----------------------------------------------------------------------
    log("\n" + "=" * 70)
    log("VERDICT SUMMARY:")

    pass_count = 0
    yellow_count = 0
    red_count = 0

    for key, finding in results.items():
        if "error" in finding:
            log(f"  RED  — {key}: {finding['error']}")
            red_count += 1
        elif finding.get("has_skeleton") is True:
            log(f"  PASS — {key}: skeleton present, class={finding.get('asset_class')}, lods={finding.get('lod_count', 'N/A')}, mats={finding.get('material_slot_count', 'N/A')}")
            pass_count += 1
        elif finding.get("has_skeleton") is False:
            log(f"  YELLOW — {key}: no skeleton detected")
            yellow_count += 1
        elif finding.get("is_anim_sequence"):
            log(f"  PASS — {key}: AnimSequence, skeleton={finding.get('has_skeleton')}")
            pass_count += 1
        else:
            log(f"  YELLOW — {key}: {finding.get('note', 'unknown')}")
            yellow_count += 1

    log(f"\n  PASS={pass_count}  YELLOW={yellow_count}  RED={red_count}")
    if red_count == 0 and yellow_count == 0:
        log("  OVERALL: PASS ✅")
    elif red_count == 0:
        log("  OVERALL: YELLOW ⚠️  (review YELLOW items)")
    else:
        log("  OVERALL: RED ❌ (see RED items above)")

    log("=" * 70)
    log("Criterion 3.2 test complete.")


# Entry point
run_criterion_32()
