# Meshy Armor Capability — Research Findings
# Priority 1 (Mode A — Analytical)

**Date:** 2026-05-22
**Mode:** A (analytical)
**Commissioner:** gandalf (dispatch 2026-05-22-legolas-unity-asset-catalogue-armor-meshy.md)
**Sources consulted:** meshy.ai, docs.meshy.ai, help.meshy.ai, meshy.ai/tags/armor, meshy.ai/tags/helmets, meshy.ai/blog/unity-animation, YouTube/community pipeline guides

---

## Summary

Meshy can generate armor geometry across all major armor categories. Its text-to-3D engine makes no categorical distinction between props and characters — a chest plate, helmet, or gauntlet is simply a 3D object description. The model library (58K+ models) explicitly includes armor tags (armor, helmet, helmets, armour, breastplate, chestplate, gauntlet, pauldron). However, **the rigging API is character-body-only**: it operates on "standard humanoid (bipedal) assets" and has no explicit armor-as-separate-skinned-piece support. This creates a split that matters for implementation.

The practical finding: Meshy handles two distinct armor patterns, not one.

- **Pattern A — Baked armor (armor as part of the character mesh):** Meshy generates a "knight in plate armor" character where the armor IS the mesh surface. This character goes through the standard rigging pipeline, exits with bone weights, and imports into Unity as a Humanoid Animator. The armor deforms with the character because it is the character. This works fully and cleanly.

- **Pattern B — Separate armor piece (standalone armor prop for runtime equip):** Meshy generates a chest plate or helmet as a static mesh prop. The rigging API will not rig a standalone chest plate — it requires a humanoid body structure to run pose estimation. A standalone chest plate has no limb anatomy, so the API errors or produces nonsense. These pieces arrive as static meshes and require manual bone-weight painting (Blender) or rigid-attachment parenting to a bone anchor.

The design implication: if Reincarnated wants **armor as a visually separate equippable layer** (swap chest plates between characters at runtime), Meshy alone does not solve this — it requires the Blender skinning step or Asset Store pre-rigged armor packs. If armor is **baked into the character model per spirit/archetype**, Meshy handles it fully with no extra work.

**Confidence:** HIGH for the core finding (API documentation is explicit). MEDIUM for the baked-armor deformation quality claim (no direct empirical test by this agent; based on Meshy's stated auto-rigging behavior and general knowledge of mesh skinning). LOW for edge cases involving complex cloth armor (cloaks, robes) — these have physics-simulation requirements that go beyond rigging.

---

## 1.2.1 — Can Meshy Generate Armor Meshes?

**Yes, fully.** Evidence:

1. **Text-to-3D:** Meshy's text-to-3D accepts any natural-language description. Prompts like "medieval plate chest armor, T-pose, fantasy style, plain background" work by the same mechanism as any character or prop. The help center example ("Humanoid Male wearing a motorcycle helmet and biker outfit, T-Pose") demonstrates wearable/clothing generation is within scope.

2. **Model library tags:** The Meshy library has tagged categories for armor, helmet, helmets, armour, breastplate, chestplate, gauntlet, headgear. The /tags/armor page shows 30+ models spanning standalone pieces (pauldrons, chest plates, iron wyrm masks) and full armored characters.

3. **Style coverage:** The library includes realistic, low-poly, stylized, and voxel registers. Fantasy-medieval, sci-fi, and creature-inspired armor aesthetics are all represented in community model examples.

4. **Format output:** FBX, GLB, OBJ, USDZ, BLEND — all compatible with Unity.

**Per-category assessment:**

| Armor category | Meshy can generate? | Notes |
|---|---|---|
| Chest plate | Yes | Multiple community examples in library; text-to-3D confirmed |
| Helmet | Yes | Dedicated /tags/helmet and /tags/helmets library; 30+ examples |
| Gauntlets | Yes | Tagged in armor library; text-to-3D generates |
| Pauldrons / shoulder armor | Yes | Explicitly tagged in armor library ("Standalone Single pauldron" example found) |
| Greaves / boots | Yes | No explicit dedicated tag but covered under armor/equipment description |
| Cloak / cape | Yes (with caveats) | Generates geometry; cloth physics simulation NOT handled by Meshy |
| Full robe | Yes (with caveats) | Same caveat as cloak — static mesh, no cloth sim |

---

## 1.2.2 — Is the Output Skinnable to a Humanoid Skeleton?

**Conditionally yes.** The answer depends on which of two patterns is used.

### Pattern A: Baked armor (armor integrated into character mesh)

**Fully skinnable.** When Meshy generates a character model that includes armor as part of its mesh surface (a "knight in plate armor"), the entire mesh — body geometry, armor geometry, and all — is submitted to the rigging API as a single humanoid model. Meshy's rigging API:

- Detects body structure (head, torso, arms, legs — the armor forms part of these surfaces)
- Places skeleton automatically (100-joint humanoid rig, sub-30 second processing)
- Calculates bone weights across the entire mesh including armor surfaces
- Exports in FBX with humanoid rig that maps to Unity's Humanoid Avatar when Rig tab is set to "Humanoid" in Unity import settings

The chest plate deforms because it is topologically continuous with the chest mesh. Shoulder pauldrons deform with the shoulder bones. Gauntlet geometry deforms with the hand and forearm bones. This is the clean path.

**Known limitation:** Thin hard-surface elements (sharp edges on plate armor) may show visible deformation artifacts at joints (shoulder rotation, elbow flex) because mesh skinning assumes organic deformation. This is a general rigging problem, not a Meshy-specific failure — it affects any tool. Mitigation: use retopology (Meshy's Remesh API) to get clean quad topology before rigging, which reduces deformation artifacts.

### Pattern B: Standalone armor piece (separate mesh)

**Not skinnable via Meshy's rigging API.** The API documentation states: "currently only works well with standard humanoid (bipedal) assets with clearly defined limbs and body structure." A standalone chest plate has no bipedal anatomy — pose estimation fails. A standalone helmet has no torso/limb context — it exits as a static mesh.

**Rigid attachment is viable for several categories:**

| Armor category | Rigid attachment viable? | Anchor bone | Notes |
|---|---|---|---|
| Helmet | Yes | Head bone | Parented to Head bone; no deformation needed for rigid helm |
| Pauldrons | Yes (mostly) | LeftShoulder / RightShoulder | Rigid pauldron rotates with shoulder bone; visible gap at extreme rotations |
| Gauntlets | Yes (mostly) | LeftHand / RightHand | Rigid gauntlet follows hand; finger articulation not possible |
| Greaves / boots | Yes | LeftFoot / RightFoot | Works for full-boot designs that don't flex |
| Chest plate | Partial | Spine / Spine2 | Rigid chest attached to spine bone; visible mesh interpenetration during extreme bends |
| Cloak / cape | No | Spine (root) | Cloak needs cloth simulation (Unity's built-in Cloth component or Obi Cloth) to not look rigid |
| Full robe | No | Hips (root) | Same — static mesh robe = cloth that doesn't move with the character realistically |

### Bone hierarchy produced by Meshy

Meshy's auto-rig produces a humanoid skeleton that maps to Unity's Humanoid Avatar when the FBX Rig tab is set to "Humanoid" in the Unity import inspector. The documentation does not explicitly list the bone hierarchy produced, but the Unity integration guide instructs setting Animation Type to "Humanoid" — this confirms Meshy produces a Unity-compatible humanoid rig. The standard Mixamo bone hierarchy (Hips → Spine → Spine2 → Neck → Head → LeftShoulder → LeftArm → LeftForeArm → LeftHand → [fingers], RightShoulder → ..., LeftUpLeg → LeftLeg → LeftFoot, RightUpLeg → ...) is the Unity Humanoid Avatar standard. Meshy's exported skeletons follow this convention per community reports.

---

## 1.2.3 — Alternate Paths When Meshy Can't Fully Cover Armor

| Scenario | Alternate path | Cost/effort |
|---|---|---|
| Runtime armor swapping (equip/unequip separate pieces) | Asset Store pre-rigged armor packs (Infinity PBR Armor Pack 1 @ $50; Polytope Studio Modular Armors @ $49.99) — these provide Skinned Mesh Renderer components already weighted to Unity Humanoid Avatar bones | One-time asset purchase; no rigging work |
| Cloak / cape cloth simulation | Unity built-in Cloth component (free) or Obi Cloth ($55 on Asset Store) applied to generated cloak mesh; requires manual setup per cloth asset | Low-medium engineering effort; one-time per cloak variant |
| Full robe cloth sim | Same as cloak path above; or bake robe into character and accept limited cloth movement | Same |
| Hard-surface armor deformation quality (elbow/shoulder artifacts) | Blender post-processing: import FBX from Meshy, manually adjust bone weights at problem joints using weight painting tools, re-export | 30-90 minutes per character for experienced Blender user; one-time per archetype family |
| Armor as separate piece with full skinning | Blender manual skinning: import character + armor piece, merge or bind armor to character's armature, paint weights to transfer from body to armor | 1-3 hours per armor piece; practical for 5-15 canonical armor pieces, not scalable for hundreds |

---

## Confidence Read — Summary

**Does Meshy + Unity cover the dominant armor case cleanly?**

YES for the baked-armor pattern. A character generated by Meshy wearing armor exits as a fully rigged Humanoid Avatar. The armor deforms with the rig. This is clean for 3D character profiles where each spirit/archetype has its own visual model (baked-in armor varies per spirit).

NO for the runtime-equip-swap pattern. Separate skinned armor pieces require either Asset Store pre-rigged packs or manual Blender skinning. The Meshy rigging API does not handle standalone armor.

**Does armor require a substantively different pipeline than weapons?**

YES in one dimension. Weapons are held props attached to the Hand bone — static mesh, no deformation, rigid attachment works perfectly. Armor on body surfaces deforms — the rigid-attachment approach works for helmets, pauldrons, gauntlets, and boots but fails for chest pieces and cloth items. If the project wants equippable armor swapping, a different sourcing path is needed for body armor (chest + robe/cloak) vs. rigid extremity armor (helmet, gauntlets, boots, pauldrons).

---

## Source List

- Meshy rigging and animation API: https://docs.meshy.ai/en/api/rigging-and-animation (accessed 2026-05-22)
- Meshy rigging API constraints: https://docs.meshy.ai/en/api/rigging (accessed 2026-05-22)
- Meshy armor tag library: https://www.meshy.ai/tags/armor (accessed 2026-05-22)
- Meshy helmet tag library: https://www.meshy.ai/tags/helmets (accessed 2026-05-22)
- Meshy Unity animation guide: https://www.meshy.ai/blog/unity-animation (accessed 2026-05-22)
- Meshy animation generator feature: https://www.meshy.ai/features/ai-animation-generator (accessed 2026-05-22)
- Meshy text-to-3D help docs: https://help.meshy.ai/en/articles/9996858-how-to-use-the-text-to-3d-feature (accessed 2026-05-22)
- 3DFY AI on Meshy rigging alternatives: https://3dfy.ai/meshy-ai-alternatives-export-rigged-models/ (accessed 2026-05-22)
