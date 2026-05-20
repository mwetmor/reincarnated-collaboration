# Mixamo — Initial Animation Inventory

**Date:** 2026-05-20
**Phase:** 1 — Reconnaissance
**Sources:** Mixamo.com (page did not render via WebFetch — JavaScript-dependent SPA); supplementary WebSearch; community reference from School of Motion, MoCap Online, Adobe FAQ, Unity forums
**Note on data quality:** Mixamo's web interface is a JavaScript SPA that does not render via WebFetch. All category counts below are community-sourced estimates. Total library estimate (~2500 animations) is widely cited in community sources. Phase 2 should include a direct human-browse session with Mixamo's search+filter interface to get exact counts.

---

## Summary

Mixamo is Adobe's free animation library for humanoid characters, available at mixamo.com. It provides the animation layer in the canonical Reincarnated production pipeline (ChatGPT Image Gen → Meshy 3D Model → Mixamo Rig → VFX mapped).

**Key findings:**

1. **Humanoid-only hard constraint.** Mixamo's auto-rigger and animation library support bipedal humanoid characters exclusively. Non-humanoid monsters cannot use Mixamo at any stage. This is the most significant pipeline constraint for Reincarnated's monster generation.

2. **~2500 total animations** (widely cited community estimate). Coverage is uneven — locomotion and basic combat are well-covered; ARPG-specific patterns (spell casting variants, dodge rolls, charge-up) are thin.

3. **Magic/spell animation coverage is limited.** Mixamo has basic casting gestures but lacks the variety needed for differentiated ARPG skill animations (distinct instant-cast vs channel vs charge-up animations for each skill type).

4. **License terms:** Mixamo animations are free for commercial use for Adobe subscribers (or free accounts). The key restriction is that animations must be used with Mixamo-rigged characters — the animations themselves cannot be redistributed independently. For Reincarnated's use case (animations applied to procedurally-generated characters in a game context), this appears unproblematic. Confirm with Adobe legal for commercial release.

5. **Bone anchor points:** Standard Mixamo skeleton provides bone anchors at RightHand, LeftHand, Hips, Spine/Chest, Head, and foot bones. No dedicated weapon socket bones — weapon/VFX attachment requires Unity Animation Rigging or child GameObject parenting to hand bone.

---

## Category-Level Inventory (Estimated)

| Category | Sub-category | Est. Count | Loop? | BC Axis Relevance | VFX Anchor Points | Notes |
|---|---|---|---|---|---|---|
| Movement | Walk/Run/Sprint | ~20-30 | Yes | Axis 1 all bins | body, feet | Core locomotion. Good coverage. |
| Movement | Dodge/Dash/Roll | ~10-20 | Partial | Axis 1 close-fast / Axis 4 dodger | body, feet | ARPG gap — limited dodge variants |
| Combat | Melee unarmed | ~30-50 | Partial | Axis 1 close-fast+slow / Axis 2 single-target | hands, feet | Punch/kick combinations |
| Combat | Melee sword (1H) | ~20-40 | Partial | Axis 1 close range / Axis 2 single+small-AOE | RightHand, weapon | Core for warrior archetype |
| Combat | Melee 2H weapon | ~10-20 | Partial | Axis 1 close-slow / Axis 2 small-AOE | both hands | Heavy weapon archetype |
| Combat | Ranged bow | ~10-20 | Partial | Axis 1 ranged-slow / Axis 2 single-target | LeftHand (bow), RightHand | Hunter archetype |
| Combat | Throwing | ~5-10 | No | Axis 1 mid/ranged / Axis 2 multi-spawn | RightHand | Limited |
| Combat | Spell cast (instant) | ~20-40 | Partial | Axis 2 all bins | hands, body | Key category for elemental mages |
| Combat | Spell cast (channel) | ~5-15 | Yes | Axis 3 low-tempo/flat / Axis 2B control | hands, body | ARPG gap — few variants |
| Combat | Spell cast (charge-up) | ~5-10 | No | Axis 3A low-tempo / Axis 3B spiky | hands, body | Very limited |
| Combat | Defensive block/parry | ~10-15 | No | Axis 4 mitigator | hands, body | Active mitigation animations |
| Hit React | Hit reactions | ~20-30 | No | General combat | body | Directional variants available |
| Death | Death/fall | ~15-25 | No | End state | body | Multiple dramatic variants |
| Idle | Idle/breathing | ~20-30 | Yes | Ambient | body | Good coverage |
| Emote | Non-combat | ~50-80 | Partial | None | body | Wide variety — not BC-relevant |
| Non-humanoid | All | 0 | N/A | All axes for monster enemies | N/A | HARD CONSTRAINT — not available |

---

## BC Axis Relevance Assessment

### Axis 1 — Engagement Profile

**Close-fast:** Melee sword + dash/dodge animations. Moderate Mixamo coverage. Dash variants thin.
**Close-slow:** Two-hand melee + block animations. Adequate.
**Mid-fast:** Spell cast + teleport gesture. Thin — no dedicated mid-range fast movement animations.
**Mid-slow:** Standard spell cast (stand-and-cast). Well-covered.
**Ranged-fast:** Throw + quick draw animations. Thin.
**Ranged-slow:** Bow draw/shoot + standard ranged cast. Adequate.

### Axis 2 — Damage Geometry (VFX Anchor Relevance)

All 5 damage geometry types can use standard Mixamo animations with appropriate VFX attachments:
- **single-target:** One-hand cast or point gesture. RightHand anchor for VFX.
- **small-AOE:** Two-hand spread gesture or ground-slam animation. Body/ground anchor.
- **large-AOE:** Both-arms-raised cast. Body anchor.
- **chain:** Quick-cast with gesture toward target. RightHand anchor.
- **multi-spawn:** Both-hands-flung-wide cast. Body/hands anchor.

The animation is the same or similar across geometry types — the VFX differentiates the geometry. This is a key insight: Mixamo animations are geometry-agnostic; geometry differentiation lives entirely in VFX packs.

### Axis 4 — Defensive Profile

- **tank:** Standing combat idle with high-stamina feel. Body animations available.
- **mitigator:** Block/parry + self-buff gesture (hand-to-chest). Moderate coverage.
- **dodger:** Roll/dash/evade animations. THIS IS MIXAMO'S WEAKEST ARPG CATEGORY. ~10-20 dodge variants for a category that ARPG players feel strongly about. Phase 2 should evaluate Mixamo alternatives (MoCap Online, Rokoko free packs) for dodge animation supplementation.
- **glass:** Standard combat animations — glass cannons use same animation set.

---

## License Terms

**Source:** Adobe/Mixamo FAQ (https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html)

- Mixamo animations are provided free for use in personal and commercial projects
- No additional licensing fees for commercial games
- Characters and animations can be modified
- Redistribution of Mixamo animations as standalone animation files is not permitted
- Using Mixamo-rigged characters with Mixamo animations in shipped games: permitted

**Commercial use verdict for Reincarnated:** Permitted. Standard commercial game usage.

---

## Critical Non-Humanoid Gap

The canonical Reincarnated production pipeline (ChatGPT→Meshy→Mixamo) assumes humanoid outputs throughout. This works for player characters and humanoid-form enemies. For non-humanoid monsters (beasts, spiders, dragons, elementals, spirits), a separate pipeline is required:

- ChatGPT Image Gen → Meshy 3D Model → **Blender custom rigging** → Unity import

This is significantly more labor-intensive. The scope of non-humanoid enemy generation in the current engine (monster_generator.py exists but its rig requirements are unknown) should be assessed in Phase 2. The palette primarily describes elemental spirit-form characters which may be humanoid by design — this is worth confirming against canonical-6 character design.

---

## Phase 2 Recommendations for Track C

1. **Direct Mixamo browse session** — count animations in key categories (spell cast, dodge, melee variants) with exact numbers
2. **Evaluate Mixamo alternatives** for dodge/combat animation gaps: MoCap Online (paid), Rokoko free magic pack (free), Mixamo community packs
3. **Confirm non-humanoid pipeline path** — assess whether canonical monster designs require non-humanoid rigs
4. **Document bone name mapping** for Unity Humanoid Avatar setup (required for all Mixamo → Unity imports)
