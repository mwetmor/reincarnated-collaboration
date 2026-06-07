# Criterion 3.2 — Meshy → UE 5.7 Import

**Verdict:** YELLOW — interactive import needed; Interchange/Slate headless constraint discovered
**Date:** 2026-06-06 Session 1 + 2026-06-07 Session 2
**Session 2 update:** Headless import attempted (2026-06-07); Interchange/Slate constraint found; interactive import path documented below.
**Criteria 3.1 status:** PASS ✅ — 3 meshes available at `meshy-3d-outputs/`
**Session 2 inputs available:**
- Crusader biped GLBs at `C:\dev\reincarnated-collaboration\duskweaver\Meshy_AI_Crusader_of_the_Ember_biped\` — 4 animations (Idle_03, Walking, Running, Roll_Dodge_4), all with skin + skeleton + animation baked in (~28MB each)
- Matt's spike-generated FBX: stated to be at `Content\Characters\MeshyTest\` but directory does NOT exist at session 2 start (pending Matt dropping files)

## Pipeline constraint identified (Session 2 — 2026-06-07)

**Empirical finding:** UE 5.7 Interchange framework requires Slate application (editor UI) for asset import operations. In headless mode (`-nullrhi -nosound`), Slate is not initialized. When `AssetImportTask` is called in headless Python, Interchange invokes the ContentBrowser + Slate for import dialogs, causing:

```
Assertion failed: CurrentApplication.IsValid()
[File: SlateApplication.h Line: 321]
```

Callstack: `PythonScriptPlugin → AssetTools.ImportAssetTasks → InterchangeEngine → ContentBrowser → Slate` → crash.

**Implication:**
- GLB/FBX import via `AssetImportTask` is NOT headless-compatible with UE 5.7's Interchange pipeline
- Interactive UE Editor session required for import verification
- This is NOT a product capability limitation — it is a headless-testing tooling constraint
- Production import workflow is always interactive anyway; this constraint does not block WS1+

**Alternative headless path (for future reference):**
- Interchange can be disabled via `Config/DefaultEditor.ini`: `[/Script/InterchangeCore.InterchangeProjectSettings] bInterchangeEnabled=False` — this reverts to old FBX importer which may be headless-safe for FBX format
- GLB format without Interchange: NOT supported (Interchange provides GLB/glTF support; disabling Interchange = no GLB import)

## Meshy image → 3D pipeline constraint (Matt, 2026-06-07)

**CRITICAL PRODUCTION PIPELINE NOTE** (Matt, 2026-06-07):

When passing images to Meshy for character generation (image-to-3D path):
- **Image MUST be in T-pose or A-pose** — character with arms extended horizontally or at 45°
- **No items in hands** — weapons, shields, tools must not appear in the reference image
- **No secondary entities** — pets, mounts, companions, environmental objects must not appear

This constraint applies to the IMAGE-TO-3D path. The text-to-3D path (used in criterion 3.1) does not have this constraint — Meshy generates T-pose automatically from text prompts.

**Impact on production pipeline:**
- Text-to-3D (criterion 3.1 path): no constraint; Meshy auto-generates T-pose
- Image-to-3D (future path for character appearance generation from substrate reference images): T-pose/A-pose images REQUIRED
- Museum weapon images (criterion 3.3 path): no T-pose constraint (weapons are static meshes; no skeleton needed)

**Documented for WS1 commission scoping:** production character pipeline must source or generate T-pose/A-pose reference images when image-to-3D is used for character body generation.

---

## Status

Criterion 3.1 is PASS — 3 meshes generated and evaluated. The remaining blocker is the **Meshy rigging step**, which requires the Meshy web app (not available via API).

**Empirical finding (Session 1):** Meshy text-to-3D preview API returns FBX with mesh + textures but ZERO skeleton entries. Verified: Kit A FBX downloaded and parsed — no bone/skeleton/deformer data present. The "Rig Character" feature exists only in the Meshy web app.

**What Matt needs to do (one-time manual step):**
1. Log into Meshy web app (meshy.ai)
2. Open tasks for Kit A, B, C (by task ID)
3. Click "Rig Character" on each → Meshy auto-detects humanoid skeleton
4. Export each with "Unreal Engine" preset → downloads FBX with Control Rig
5. Copy FBX files to `C:\dev\reincarnated-unreal\Reincarnated\Content\Characters\MeshyTest\` on PC
6. Mantis imports via UE Editor → completes criterion 3.2 evaluation

**Meshy task IDs for web app:**
| Kit | Task ID |
|---|---|
| Kit A — Ember Sweeper (fire/DEX) | `019ea025-fe66-71d2-b139-2687d74b5aa5` |
| Kit B — Tide Warden (holy/WIS) | `019ea026-074b-705d-ac86-6d5f2405e8ec` |
| Kit C — Duskweaver (shadow/INT) | `019ea026-100e-7339-bc41-c57937bba495` |

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

## Interactive import verification protocol (for Matt)

5-minute step to close criterion 3.2:
1. Open UE 5.7 Editor at `C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject`
2. In Content Browser: navigate to `Characters/MeshyTest/`
3. Drag-and-drop `Meshy_AI_Crusader_of_the_Ember_biped_Animation_Idle_03_withSkin.glb` from Explorer
4. In Interchange import dialog: select "Skeletal Mesh" → enable "Import Animations" → OK
5. Verify in Content Browser: SK_Crusader + Skeleton + AnimSequence assets created
6. Double-click Skeleton → confirm humanoid bone hierarchy (Pelvis, Spine, Arms, Legs)
7. Screenshot the Skeleton editor → add to this file
8. Mantis marks criterion 3.2 PASS when screenshot received

**Alternatively:** if Matt places the spike-generated FBX files at `Content\Characters\MeshyTest\`, same import protocol applies.

*Criterion 3.2 status: YELLOW — Interchange/Slate headless constraint found (empirical, 2026-06-07); interactive import is the correct production path; 5-minute interactive verification step needed to close to PASS.*
