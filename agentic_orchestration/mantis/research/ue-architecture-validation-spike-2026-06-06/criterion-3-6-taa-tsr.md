# Criterion 3.6 — TAA/TSR Fast-Combat Readability

**Verdict:** BLOCKED (depends on criterion 3.2 character import)
**Date:** 2026-06-06 Session 1

---

## Blocking gate

Requires an imported humanoid Skeletal Mesh from criterion 3.2 to run motion tests. No independent blocker.

---

## Pre-work: UE 5.7 TSR baseline knowledge

### TSR vs TAA in UE 5.7

UE 5.7 ships Temporal Super Resolution (TSR) as the preferred anti-aliasing path for real-time rendering. Per canonical 38 D1: "TAA blur during fast combat — mitigated by TSR + motion-vector tuning + per-character motion-aware shader tweaks."

Key TSR properties for fast-combat readability:
- TSR accumulates temporal information at a secondary resolution pass, then upscales — fundamentally better ghost-rejection than TAA
- UE 5.7 TSR includes "TSR History ScreenPercentage" control; lower values trade temporal quality for less ghosting at extreme motion
- TSR works best with accurate motion vectors (skeletal mesh motion vectors are per-bone, not per-object, in UE5)
- For fast-combat (10-20 m/s movement + 200-400ms swing): motion vectors on skeletal mesh must be enabled per-mesh

### Known TAA failure modes for ARPG

- **Character-vs-background ghosting:** character moves fast over static environment → TAA samples from wrong temporal position → character appears to "smear" or leave a trail
- **Ability VFX bleed:** additive Niagara particles during dash get temporally accumulated → VFX region over-brightens
- **Edge aliasing on weapon swings:** thin weapon silhouette at high angular velocity → TAA sub-samples → edge flickers

TSR substantially mitigates the first two. The third requires per-mesh TSR coverage mask tuning or MSAA at weapon mesh level (unusual; rarely needed).

---

## Test protocol (ready to execute when 3.2 complete)

Per dispatch § 7:

### Scene setup
1. Test map: `Content/TestMaps/TAATest`
2. Character: Meshy-imported Skeletal Mesh from criterion 3.2 (or substituted with UE5 Mannequin if 3.2 is delayed — Mannequin is always available as fallback character)
3. Background: static environment with contrast textures (brick/stone floor + walls — provides clear reference for ghosting detection)

### Motion parameters (ARPG-typical per dispatch § 7)
- Character run speed: 10-15 m/s (horizontal movement)
- Attack swing: 200-400ms duration, full-arc (180°+)
- Dash: 4-6 m/s instantaneous displacement over 100ms
- Camera: third-person, 5m behind character, follows with 50ms input lag

### Measurement approach
- Capture via in-editor Movie Render Queue at 1080p, 60fps
- TAA frame: one pass with anti-aliasing mode = TAA
- TSR frame: same sequence with anti-aliasing mode = TSR (project settings change)
- Visual comparison: export 5 frames from each (peak motion moments) and compare side-by-side
- FPS profile: Unreal Insights (stat unit overlay in editor) to confirm 60fps floor not broken by TSR overhead

### Acceptance criteria
- **PASS:** TSR combat reads clearly at 60fps; no major blur compromise at PC native; TSR preferred over TAA for fast-motion scenarios
- **YELLOW:** TSR acceptable at PC; mobile-resolution projection (720p scalability) shows edge-case blur → note for WS5 mobile-polish
- **RED:** TSR blur compromises readability at PC even after basic settings tuning → escalate as UE 5.7 TSR configuration design call

---

## Fallback character note

If criterion 3.2 Meshy import is blocked when criterion 3.6 execution is needed, the UE5 Third Person Character Mannequin (bundled with UE starter content) provides an equivalent humanoid skeletal mesh for TAA/TSR testing. The Mannequin is always present in UE5 projects created from the Third Person template (or importable via the default content pack). This allows 3.6 to proceed in parallel with 3.2 if needed.

**NOTE:** using Mannequin for TAA/TSR test is valid for criterion 3.6 alone. The final criterion 3.6 verdict should still be re-verified with a Meshy-imported mesh when 3.2 completes, to confirm TSR handles the specific geometry/material characteristics of Meshy outputs (which may differ from Mannequin's clean quad-dominant mesh).

---

*Criterion 3.6 status: BLOCKED — can proceed with Mannequin fallback if 3.2 is delayed beyond ~2 sessions. Execution protocol documented.*
