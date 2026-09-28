# Humanoid animation: the common thread behind the rig's defects, and the pipeline that removes it (verdict)

> **STATUS:** CURRENT verdict for Matt's decision (Run C-9, ledger R-C9-51). Author gandalf (DRIFT-CRITIC on the rig; ARCHITECT on the pipeline), 2026-09-28.
> **Matt, verbatim:** *"When looking at the AB test on the large monitor … 1) the feet are flat footed. 2) There is no coordination between the leg movement and the hips/body. 3) The left hand moves towards the poleaxe but does not grip onto it or even lock onto it … 4) There are visible breaks and lines between puppetted pieces … 5) There is a strange line that seems to tie the left hand to the chest/shoulder. … ultra think about what the common thread/issue is … and let me know if it would be possible to use a systematic approach … (or if another approach to 2D animation would be needed entirely; factor in that we also need modular gear/armor/weapons eventually). The goal … make the puppeted approach (or any 2D animation approach) the same as the video result … so we can make this into a humanoid pipeline."*

## 1 · The common thread: we are animating a PICTURE of the knight, not the knight

The rig is built by cutting ONE painted still into rigid pieces and rotating them in the picture plane. A painted still bakes in four things that belong to its single pose, and each of Matt's five defects is one of them showing through:

| Baked into the one still | What it breaks when the pose changes | Matt's items |
|---|---|---|
| **Occlusion:** what was hidden was never painted | holes and gaps where a part swings away (the hip, fixed by painting the under-layer RP-E) | 4 (neck and gorget, forearm and upper arm, under the tabard) |
| **Contours:** ink outlines drawn where one part overlapped another | the outline stays on the part underneath when the top part moves: a stray line | 5 (most likely the far arm's own contour, or a sliver of the haft, left on the chest piece; to be verified on a frame), part of 4 |
| **Projection:** the foreshortening of that one view | a real motion that turns a part TOWARD or AWAY from the camera (foot pitch, pelvis rotation, torso counter-rotation, the shoulder coming forward) changes the SILHOUETTE, and a rigid cut-out can only rotate the old silhouette flat in the plane | 1 (the roll is there, about 18° at heel strike and 29° at toe-off, but a one-piece sabaton with no toe break, rotated in the plane, still reads as a flat foot), 2 |
| **Structure:** nothing says what the pieces ARE | no skeleton semantics: nothing says "the pollaxe is a rigid body held at two grip points", so the far hand and the haft are two unrelated animations | 3 |

The **video works** because it redraws the whole body every frame: occlusion, contours, foreshortening and secondary motion are re-solved each time. That is also why it costs what it costs and drifts between clips.

**So: can the puppet be made the same as the video? No, not as a cut-out of a single still.**
- Items 3, 4 and 5 are fixable systematically inside the cut-out method: grip constraints, painted overlap under-layers at every joint (the RP-E method generalised), and outline-free under-layers.
- Items 1 and 2 are the method's ceiling. Out-of-plane motion needs NEW DRAWINGS per pose (swap sprites) or a body that can be re-projected.
- Cut-out animation is excellent in SIDE-view games with limited turning (the classic painted-puppet games). Our 8-direction, three-quarter camera is its hardest case, and every direction needs its own complete part set.

## 2 · The requirement that decides it: modular gear

- **Video:** every gear combination is new clips for every direction and every action. Combinatorial, and it fails the requirement outright.
- **Cut-out from stills:** every gear piece needs painted part sheets for every joint, in every direction, with its own overlaps and contours. Possible, but the effort multiplies with the gear count, and the ceiling in § 1 remains.
- **A 3D BODY rendered to 2D** (the Diablo 2 / Dead Cells / Infinity-engine family; `matt_notes_handoff_docs/claude-mobile-notes-2D-asset-pipeline` § 1 names it): gear pieces are separate meshes on ONE shared humanoid skeleton. Every clip and every direction comes for free for every piece, and pieces render as layers. **This is the only one of the three whose gear cost is additive rather than multiplicative.**

## 3 · Recommendation: give the pipeline a BODY, and keep the painter's hand on it

**A 3D proxy of the humanoid is the single source of truth for skeleton, occlusion, foreshortening and grip sockets. Every 2D frame is RENDERED from it at the game camera. The PAINT comes from our approved stills, not from a shader's idea of paint.**

1. **Body:** a humanoid mesh with a STANDARD humanoid skeleton, so every clip retargets to every humanoid, which is what makes it a pipeline. It is fitted to the knight's silhouette in the eight approved turnaround views, either kit-bashed on a base humanoid in Blender (installed on the Mac) or generated from the turnaround by an image-to-3D model (an external service: Matt's call).
2. **Paint:** PROJECT the approved stills onto the mesh from their own camera directions. There are eight views, so almost every surface is covered by at least one real painted pixel, and what one view hid another view shows. That is the under-layer problem solved once, for all joints, by geometry instead of a burst per joint.
   - The painted OUTLINES are removed from the projected texture (they are view-specific, § 1 row 2).
   - The dark FFT ink line (card LINE, R-C9-9) is drawn by an outline pass at render time, so the contour is always the CURRENT silhouette's.
   - Astra touches up any stretched or unseen patch once, on the texture, never per frame.
3. **Motion:** real walk and run clips, retargeted to the skeleton (mocap-class libraries or hand keys). Hips, torso counter-rotation, bob and heel-toe are in the clip. The **Keeper cadence** (walk 0.5797 s and run 0.5517 s per stride) and the IK foot plant carry over unchanged from today's work. The Grok clips stay as the REFERENCE the result is judged against.
4. **Grip:** the pollaxe is its own mesh, parented to the main hand, with a grip socket for the far hand. It cannot drift, by construction.
5. **Gear:** helm, tabard, pollaxe and cuisses as separate skinned meshes, each rendered as its own sprite layer per frame and per direction. The manifest's material, sockets, layers and wound_shader fields (mobile notes § 53) map onto this directly.
6. **Output:** the SAME sprite sheets the game already plays (12 walk frames, 8 run frames, idle, eight directions), so the Godot scene, the cadence and the A/B route do not change.

**The risk, named:**
- The projected paint may read slightly more "rendered" than a hand-painted frame, especially where the pose is far from the painted views (a knee at full bend).
- The shader outline must match the painter's line weight.
- Both are VISIBLE in the first spike, which is why the spike comes before any commitment.

## 4 · What happens to today's work

- **Nothing is wasted:** the cadence, IK plant, stride census and probes carry over; so do the eight approved stills (they become the texture sources) and the RP-E under-layers (projection sources for the hidden armour).
- The cut-out rig stays in the A/B route as the comparison it now is.
- **If Matt wants the cut-out pushed further meanwhile,** the systematic cut-out fixes are cheap and bounded: the grip constraint (3), outline-free under-layers per joint (4, 5), and a split heel/toe sabaton (1). They will improve it; they will not remove the ceiling in § 1.

## 5 · The spike (proposed; Matt gate before it fires)

One direction (E), walk and run, one knight, ending in the same A/B comparison Matt already uses (Grok · cut-out rig · 3D-projected):
1. Body plus skeleton, fitted to the E, NE, SE and N views.
2. Projection texture from the eight stills, outlines stripped, ink outline pass.
3. The walk and run clips at Keeper cadence.
4. Render to the game's sprite sheet format and drop it into the scene behind a third G-toggle state.
5. **The gear proof:** swap the pollaxe for a second weapon mesh and the helm for a second helm, with no repaint.

**Matt gates:**
- **M-a** the fitted body (silhouette overlay on the stills);
- **M-b** the first rendered frames next to the Grok frames;
- **M-c** walking it in the scene.

*— gandalf, 2026-09-28.*
