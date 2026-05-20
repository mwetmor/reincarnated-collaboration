# Pipeline Integration Notes — Initial Audit

**Date:** 2026-05-20
**Phase:** 1 — Reconnaissance
**Pipeline:** ChatGPT Image Gen → Meshy 3D Model → Mixamo Rig → VFX Mapped
**Sources:** Meshy.ai documentation, Adobe Mixamo FAQ, Unity forums, curtision.com pipeline guide, community resources

---

## Summary

The canonical Reincarnated pipeline is technically viable for humanoid characters. The steps chain cleanly and the tooling is well-documented. However, three constraint-propagation points create hard limits that affect design decisions:

1. **Humanoid-only constraint propagates from Mixamo backward through the entire chain.** Any non-humanoid monster generated via ChatGPT→Meshy hits a wall at Mixamo. Separate custom-rigging path required.

2. **Render pipeline lock (URP recommended) must be decided before VFX procurement.** Several high-quality VFX packs are Built-in only or URP-only. The decision affects what is purchasable and usable.

3. **VFX attachment requires no native Mixamo socket bones.** Unity Animation Rigging package is required for clean runtime VFX attachment to hand/weapon bones. This is a known workflow, but it adds one engineering step that must be built once.

---

## Stage 1: ChatGPT Image Gen

**Function:** Generate 2D reference images of characters, monsters, or effect concepts.

**Inputs:** Text prompt + optional seed image for consistency.

**Critical constraints:**
- Must produce consistent perspective (3/4 or front-facing) for Meshy to reconstruct correctly
- Character limbs must be visible and separated (T-pose preferred)
- Clean/transparent background reduces mesh contamination
- Style must be self-consistent within a batch (mixing photorealistic and cartoon in one session produces inconsistent outputs)

**Cost:** ~$0.02–0.05 per image at standard ChatGPT API rates. Effectively negligible per-character.

**Known failure modes:**
- Crossed arms, hidden limbs → Meshy reconstructs as merged/fused geometry → Mixamo rigging fails
- Complex backgrounds included in 3D mesh → background geometry corrupts model
- Style drift across sessions → visual inconsistency in final character roster

**Mitigation:** Develop a canonical ChatGPT prompt template per character archetype type. Establish style conventions in the prompt (e.g., "stylized fantasy warrior, T-pose, plain white background, front-facing, cel-shaded art style").

**Iteration speed:** ~30 seconds per image. Can batch-generate 20+ concepts in under 20 minutes.

---

## Stage 2: Meshy 3D Model

**Function:** Convert 2D image to 3D model with texture.

**Inputs:** Image (FBX preferred for Mixamo compatibility).

**Output:** Textured 3D mesh in FBX / OBJ / GLB / USDZ / STL / BLEND formats.

**Critical constraints:**
- Humanoid detection is automatic — Meshy auto-rigs if it detects head/torso/arm/leg structure
- Non-humanoid models produce a mesh but require external rigging
- Mesh topology quality varies; organic characters perform better than hard-surface
- `model_type: humanoid` outputs include a basic skeleton auto-rig from Meshy (100+ preset animations natively) before the Mixamo step

**Cost (as of 2025-2026):**
- Free: 100 credits/month, 10 downloads/month
- Pro: $20/month, 1000 credits/month
- Max: $60/month (studio tier)
- Credit cost: ~20 credits per Meshy 6 Preview generation
- At Pro tier: ~50 character generations per month

**Processing time:** ~30 seconds for generation; ~2-5 minutes including retopology optimization.

**Known failure modes:**
- Asymmetric character design → poor bone placement in rigging step
- High-poly mesh without retopology → Mixamo upload limit exceeded (Mixamo has a ~10k-50k poly recommended limit)
- Complex clothing/accessories → mesh merging artifacts at joints
- Low-contrast or poorly-lit reference image → surface reconstruction artifacts

**Mitigation:**
- Use Meshy's retopology tool (Pro feature) to optimize to game-ready poly count
- Ensure prompt produces high-contrast reference image
- Build in a "Meshy quality check" step before Mixamo upload

---

## Stage 3: Mixamo Rig

**Function:** Auto-rig humanoid mesh and provide animation library (~2500 animations).

**Inputs:** FBX or OBJ with humanoid topology.

**Output:** Rigged FBX with selected animation baked in.

**Critical constraints:**
- **Humanoid bipeds ONLY** — absolute hard constraint
- Character must be in T-pose or A-pose with feet pointing forward
- Origin at (0,0,0) required
- Character height does not matter (Mixamo normalizes scale)
- Manual joint placement required: user must click on character's chin, wrist, elbow, knee, and groin positions

**Cost:** Free for Adobe CC subscribers. Mixamo has been free since Adobe acquisition. No per-animation cost.

**Processing time:** ~1-2 minutes for auto-rigging; manual joint placement adds ~3-5 minutes. Animation export per animation ~30 seconds.

**Known failure modes:**
- Poor topology at joints (elbow, knee, shoulder) → deformation artifacts in animation
- Missing body part definition (hidden elbows in costume) → incorrect bone placement
- Multiple separate mesh objects not joined → rigging produces invalid results
- Symmetry issues → bone placement on one side only

**Animation coverage gaps relevant to Reincarnated:**
- Spell casting: basic one-hand and two-hand cast available; channel and charge-up variants thin (~5-15 total)
- Dodge/roll: ~10-20 variants; shallow for ARPG differentiation
- No boss/monster animations (non-humanoid)

**Bone hierarchy (standard Mixamo):**
```
Hips → Spine → Spine1 → Spine2 → Neck → Head
                      → LeftShoulder → LeftArm → LeftForeArm → LeftHand
                      → RightShoulder → RightArm → RightForeArm → RightHand
       → LeftUpLeg → LeftLeg → LeftFoot → LeftToeBase
       → RightUpLeg → RightLeg → RightFoot → RightToeBase
```

No weapon socket bones. VFX attachment must be done in Unity.

---

## Stage 4: VFX Mapped

**Function:** Attach Unity VFX prefabs to Mixamo-rigged characters in Unity.

**Inputs:** Rigged FBX from Mixamo + VFX prefabs from Unity Asset Store packs.

**Output:** Playable character with visual skill effects.

**Critical constraints:**

### Render Pipeline Lock
Must decide before VFX procurement:
- **Built-in Render Pipeline:** Most compatible (all older packs). Not recommended for new projects.
- **URP (Universal Render Pipeline):** Recommended for mobile-first projects (Reincarnated). The majority of quality VFX packs support URP.
- **HDRP:** High-quality PC/console. Not needed for Reincarnated Phase 0 mobile-first target.

**Recommendation for Reincarnated:** Lock to URP. Filters out Built-in-only packs (e.g., SineVFX Aura and Ground Effects) but maximizes forward compatibility and mobile performance.

### VFX Attachment Convention
Mixamo provides no weapon socket bones. Convention for VFX attachment:

| VFX Type | Attachment Bone | Method |
|---|---|---|
| Cast effects (projectile/chain/single-target) | RightHand | Child GameObject parented to RightHand bone in Inspector |
| Dual-hand cast effects (large AOE) | Spine2 / Chest | Child GameObject parented to Spine2 |
| Aura / buff / defensive effects | Hips or Spine | Child GameObject centered on character |
| Ground-anchored AOE | No bone — world space | Instantiated at character's ground position, no parent |
| Totem effects | No bone — world space | Instantiated at placement location, no parent |

Unity Animation Rigging package enables dynamic switching of anchor bones at runtime (useful for skills that cast from left vs right hand, or involve both hands).

### VFX Scale
Mixamo standard humanoid in Unity = approximately 1.8 Unity units (1.8 meters) height. VFX prefabs should be tested against this reference scale. Most Unity Asset Store VFX packs are designed for standard Unity humanoid proportions — scale adjustments typically minor (0.8x–1.2x range).

### Element Tagging
Each VFX prefab must be tagged with its canonical element (fire/water/earth/wind/lightning/holy/shadow/physical/neutral) in a manifest file for the substrate-filtering layer. This manifest connects the engine's element selection to the VFX instantiation system.

**Cost:** VFX procurement from Unity Asset Store (see Track B survey). One-time per pack.

---

## Constraint Propagation Map

```
ChatGPT → Meshy → Mixamo → VFX
   │          │        │        │
   │          │        │        └── Render pipeline lock (URP) propagates back to procurement
   │          │        └── Humanoid-only propagates back to image generation brief
   │          └── T-pose, separated limbs propagates back to image generation prompt
   └── Style consistency constraint propagates forward to VFX style register choice
```

**The most load-bearing decision is the Humanoid constraint.** It determines:
1. What monster types are feasible in the pipeline
2. Whether a separate custom-rigging workflow is needed
3. The animation vocabulary available for monster skill expression

---

## Open Integration Questions for Phase 2

1. **Non-humanoid monster pipeline:** What is the current plan for non-humanoid enemy generation in the engine? Does `monster_generator.py` target humanoid forms exclusively? If not, the custom-rigging path needs scoping.

2. **VFX element manifest:** Does a VFX element manifest exist currently? If not, this needs to be designed as part of the QD-engine rebuild scope.

3. **Mixamo TOS for commercial release:** Formal review needed — the free tier's commercial use terms should be reviewed by Matt before proceeding. The informal community understanding is "permitted" but the TOS language should be confirmed.

4. **URP vs Built-in decision:** Confirm render pipeline for Reincarnated game deployment. This gates VFX procurement decisions.
