# T9 handoff — plate, bridge slice, lit mode, numbers to beat
**PLATE.** `godot/plate/plate_v4.png`, 5376 × 4096 RGBA, 29.5 MB. Alpha is a real split, not decoration:
**39.75 % transparent (sky + chasm), 53.77 % opaque, 6.48 % partial.** A repaint must carry alpha back
unchanged or the backdrop starts occluding the sky.
**PINNED CONSTANTS.** Operative copy `godot/scripts/cliffside3d.gd:26-29` — `PPM = 100.617553710938`,
`CANVAS = (5376, 4096)`, `V4_UMIN = -23.2673988342285`, `V4_VMAX = 18.5067100524902`. They are *copies*:
originals at `cliffside_blockout.gd:85` (`PPM_ACCEPTED`, v1-measured off the plateau proxy, screen-x) and
`:105-106`; `gear.gd:26` holds a third copy of PPM. **Change one, change all three — nothing asserts they
agree.** Linear, because the camera is orthographic: `x_px = (dot(w,right) - V4_UMIN) * PPM`,
`y_px = (V4_VMAX - dot(w,up)) * PPM`. `cliffside3d.gd:750` inverts it. Pitch cos 0.602462407085.
**BRIDGE VIEW IN PLATE PX.** `tools/shot_t9.gd:16` aims **(3459.88, 1027.18)** zoom 1.0 → **x 2500–4420,
y 487–1567 = 1920 × 1080 plate px**. Not the play spawn / default aim **(2285.62, 2407.32)**
(`cliffside3d.gd:503`) — that is the *tree-path* frame (tree shot: aim (1896, 2640) zoom 1.5).
**THE 8 BRIDGE-SLICE PROPS.** Seven `bridge_*` plus `raven_perched`, which sits on bridge_post_3
(3681,657 vs the post's 3680,656) and belongs to the same silhouette. Sprites `godot/props/assets/<name>.png`,
declared in `godot/props/props.json`:
    bridge_obj_01_a (2588.4,1352.0) fade_when_behind | bridge_post_0 (3238.5,1428.0)
    bridge_obj_01_c (2829.1,1286.0)                  | bridge_post_1 (2996.0,1247.0)
    bridge_obj_02_a (3199.0,1486.0)                  | bridge_post_2 (3922.0, 836.0)
    raven_perched   (3681.0, 657.0) no collide       | bridge_post_3 (3680.0, 656.0)
`bridge_obj_01_a` is the only one of the eight flagged `fade_when_behind`.
**LIT MODE.** `cliffside3d.gd set_lit()` switches four things together, because any one alone answers
nothing: terrain takes a *shaded* projector and starts casting and receiving shadows; the sun stops being
masked to the character and lights everything (direction from `build_lights`, derived from the painting's
own key, so it does not move when the mode does); props swap `CliffWorld.card_material()` →
`card_material_lit()`; the character drops to true scale 1.0. Painted is the default, so everything Matt
has played is untouched. Both card materials are **alpha-scissor and never write ALPHA**: a shader writing
ALPHA without `depth_draw_always` / `depth_prepass_alpha` is classified TRANSPARENT, stops writing depth
and sorts per-object — what made every prop invisible once.
**NUMBERS TO BEAT** (`agentic_orchestration/drax/captures/2026-09-29-cliffside3d/t9_lit_world.json`).
Painted → lit: tree path mean luma 105.6 → 88.9, near-black 2.68 % → 6.87 %; **bridge 113.6 → 87.7,
near-black 1.70 % → 19.05 %**, with 16.21 % of the frame losing more than half its light.
**T9-1c (relief normals on the near wall) is parked with a NEGATIVE answer:** 10,324 of 37,810 vertices
moved, mean 0.445 m, and near-black went 19.04 % → 18.93 %. Shadows off changes nothing (15.27 % →
15.25 %); doubling the sun changes nothing (15.02 %). **With no sun and full ambient — the painted albedo
shown flat — 10.54 % is still near-black.** Over half the darkness is painted into the plate, so **1b (the
albedo repaint) is load-bearing and 1c cannot be judged until it lands.** Registration is exact because
displacement is along the view direction: the tree frame is pixel-identical (0 of 2,073,600), the bridge
frame differs 0.58 %, purely depth reordering at the chasm lip. Relief sits behind `--no-relief`. The wall
is also wrong at macro scale — an extruded vertical skirt where a cliff has faces at many orientations.
