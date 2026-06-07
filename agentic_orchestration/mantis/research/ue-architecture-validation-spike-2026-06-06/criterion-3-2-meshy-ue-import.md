# Criterion 3.2 — Meshy → UE 5.7 Import

**Verdict:** BLOCKED (depends on criterion 3.1 mesh output)
**Date:** 2026-06-06 Session 1

---

## Blocking gate

Depends on criterion 3.1 producing 3 Meshy .FBX/.GLB mesh outputs. No independent blocker beyond that.

---

## Pre-work: UE 5.7 import pipeline confirmed

UE 5.7 is installed on this PC. FBX import pipeline is native UE functionality with no changes from 5.5→5.7 that affect humanoid skeletal mesh import.

### Control Rig import path (per canonical/story/asset-pipeline-meshy-swap-2026-05-22.md)

The Meshy 6 export path for Unreal:
1. In Meshy: Export → Unreal Engine format → Control Rig preset
2. Output: `.fbx` file with skeleton hierarchy named to UE conventions + Control Rig asset
3. UE import: Content Browser → Import → FBX → Skeletal Mesh → enable "Import Mesh" + "Import Animations" + "Create Physics Asset"

### Import test protocol (ready to execute when 3.1 complete)

Per dispatch § 3:
1. Import 3 FBX files into `Content/Characters/MeshyTest/` in UE project
2. For each mesh, verify:
   - Skeleton hierarchy intact (open Skeleton editor → confirm humanoid bone hierarchy: Root → Pelvis → Spine → Arms → Legs → Head)
   - Control Rig auto-generates or imports cleanly (check for Control Rig Blueprint asset in Content Browser)
   - Mesh + skeleton compose into Skeletal Mesh asset (single asset with assigned skeleton)
   - Drop into test scene → assign animation Blueprint → verify idle animation plays
3. Run headless smoke test:
   ```
   "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
   "C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject"
   -unattended -nullrhi -nosound
   -ExecCmds="LoadMap /Game/TestMaps/MeshyImportTest; quit"
   ```

### Known risk: UE 5.7 skeleton auto-retargeting

UE 5.7 introduced improvements to IK Retargeter auto-generation. If Meshy's bone naming doesn't exactly match UE5 Mannequin conventions, the import may succeed but the Control Rig auto-generation step may require manual bone mapping. This is the most likely YELLOW scenario.

**Mitigation if bone-naming mismatch:** use the UE5 IK Retargeter to manually map Meshy skeleton to Mannequin_UE5 reference skeleton. Documented process, ~30-60 min per kit. Not a RED condition.

### Legolas character customization research composition

Per `2026-06-02-unreal-character-customization-research`:
- CC5 (Reallusion Character Creator 5) is the recommended character foundation with MetaHuman-compatible skeleton
- For the spike, we're testing Meshy → UE 5.7 direct path (no CC5 intermediary)
- If Meshy → UE 5.7 path hits a RED condition, CC5 is the named fallback (per dispatch § 3 "Compose with legolas research")

---

## Alternative paths if 3.2 RED

Per dispatch § 3 cross-reference to legolas character customization research:
1. **CC5 + Mutable:** character modeled in CC5, exported via Auto Setup plugin → UE 5.7; Mutable provides runtime customization. This is the production-quality fallback if Meshy → UE 5.7 doesn't produce animatable characters.
2. **Synty Sidekick:** low-poly fantasy characters with UE Mannequin-compatible skeleton. Dramatically lower visual fidelity but guaranteed UE compatibility.

The Meshy → UE 5.7 path is preferred (as tested in this criterion) because it's substrate-driven (character appearance derives from substrate identity → Meshy prompt → mesh). CC5 requires manual art authoring per character at production scale.

---

*Criterion 3.2 status: BLOCKED (awaiting 3.1 mesh output) — import pipeline ready; execution protocol documented.*
