# T10 handoff — the Frost King's Barrow: assets, tiles, ground, placement

Everything below is in `reincarnated-collaboration/astra_test_01/burst/runs/C-9/`. Scale bar
throughout: the barbarian at **1.85 m** = 157 px in concept **variant a**, so **K = 140.86 px/m**.
Camera is the game's own: pitch **52.9536°**, azimuth **47.00°**, orthographic.

## Assets — `cliffside3d/godot/models/barrow/*.glb`, manifest `godot/data/barrow_assets.json`
Nine Tripo builds (reduced 1.42–1.49M → 24k tris, ~45 MB → ~0.9 MB each) plus three others.

| glb | true size | yaw | plate IoU |
|---|---|---|---|
| `stone_tall` | 2.71 m h | 60° | 0.831 |
| `stone_mid` | 2.71 m h | 60° | 0.794 |
| `stone_short` | 1.24 m h | 345° | 0.796 |
| `lintel` | 2.28 m **across** | 135° | 0.707 |
| `post` | 2.04 m h | 30° | 0.881 |
| `rock_large` | 1.84 m h | 60° | 0.858 |
| `rock_small` | 0.54 m h | 135° | 0.658 |
| `birch` | 3.36 m h, **width forced 1.38 m** | 315° | 0.361 |
| `juniper` | 1.15 m h | 60° | 0.599 |
| `heather` | 0.81 m h × 1.03 m | any | procedural, 272 faces |
| `birch_proc` | 3.36 m h | — | procedural, **rejected**, see below |
| `raven` | 0.28 m h | — | T9 reuse |

**Scale rule, and it is not optional.** Every model is squat by `cos(pitch) = 0.602` because
its sheet was drawn from a plate cropped out of a 52.95° painting. Apply a **Y stretch of
1/0.602 = 1.660 BEFORE normalising to the target size** (`pitch_correct: true` in the
manifest). Verified here on the **lintel**, a beam whose length is across the screen and so
not foreshortened while its height is: raw length:height 3.17 → **1.91** after the stretch,
against the painting's **1.93**. (T9 verified the same correction on the rail post at
0.242 m vs the blockout's 0.220.)

**Yaw rule:** measured, not assumed — each model rendered through the cliff camera every 15°
and matched by silhouette against its identity plate. Apply `yaw_deg` as a Y rotation.
**Size unrotated, placement after the turn**: Godot's AABB is world-axis-aligned, so a
square post turned 45° reports a box √2 too wide.

## Tiles — `cliffside3d/godot/textures/barrow/*.png`, 1024², report `seam_finish.json`
`snow.png` → splat 0 · `path.png` → 1 · `rock.png` → 2 · `heather.png` → 3 · `ice.png` → 4.
`bark.png` is not a ground tile: it is the trunk wrap for `birch_proc` (repeat vertically).
Seam ratios after repair: snow 1.18, rock 0.99, bark 0.81, path 1.20, heather 1.43, ice 1.48.

## Ground — two, **authored is the default**
- **`godot/data/height_a_authored.png` + `.json`** ← use this. 300×300 @ 0.05 m, 15×15 m,
  relief 2.37 m, median slope 3.1°, nothing over 70°.
- `godot/data/height_a_marigold.png` + `.json` — depth-derived, keep as a toggle for Matt.
  Relief 4.00 m, median 18.8°, p90 48.0°, **1.71× calibration spread**, and its barrow crown
  reads *below* the surrounding ground.
- Reader: **`godot/scripts/barrow_heightfield.gd`** (`class_name BarrowHeightfield`) — a
  drop-in for `BarrowStandIn`: same `height_at` / `normal_at` / `build_terrain` /
  `place_on_ground`, same `TERRAIN_BIT` / `EXTENT` / `CELL`. Anchors the barrow to (0, −4)
  from each grid's own `mound.centre_xz`.
- Splat: `godot/data/splat_ids_a_marigold.png`, same grid, ids 0–4 as above.

## Placement — `godot/data/barrow_scene_a.json`, 70 instances
Emitted for **both** frames; use the `height_a_authored` list. Position formula, written into
the file: `scene = (world − grid_origin) + scene_offset`. The two grids' origins differ by
(0.45, 0.36) m, so a list used against the wrong ground puts every prop half a metre off its
own footprint. `stone_scale` (currently 1.0) is Matt's one-number lever: 1.37 makes the
stones twice his height.

## Generators
`38_heather_procedural.py` (Blender, `-- out.glb heather.png seed`) — real stems, not alpha
cards: a card has no silhouette the depth-and-normal edge pass can find.
`35_birch_procedural.py` — same shape, kept for reference.

## Known faults
1. **The procedural birch lost and I expected it to win.** Silhouette IoU against the
   concept's own birch: Tripo **0.361**, procedural **0.184**. Tripo is used. My prediction
   that a reconstructor would fail on thin twigs was right about the twigs and wrong about
   the result — the Tripo build inherits the painted sheet's overall mass, and mass is what
   a silhouette measures.
2. **The birch is the weakest asset at 0.361**, less than half the next worst. If one asset
   gets a second sheet, it is that one.
3. **Both birch builds came out ~2.35 m across** (Tripo 2.39, procedural 2.33) against the
   concept's measured 1.38 m, so the error is in neither builder. Handled by a forced width
   in the manifest — a non-uniform squash, defensible on a tree, stated rather than hidden.
4. **Heather stands in for two things.** The concept has heather *and* juniper; the 19
   clumps classified as heather take the procedural tussock. If the difference reads at the
   play camera it needs its own sheet.
5. **Only 11 birches**, filtered from a 30-component union of five prompts against the one
   confirmed birch. SAM2's 68 automatic proposals contained none.
6. **`tools/shot_barrow_t10.gd` is unverified.** Its two known faults are fixed (the
   tree-independent `_aabb`, the silent null on a missing manifest) but it has not been run
   to completion since. Per gandalf, the integrator shoots the stills with the stack on;
   this tool is a fallback, not the path.
7. **Terrain winding was backwards and is fixed** (`[k, k+n+2, k+n+1, k, k+1, k+n+2]`).
   Caught by the render-stack drax. My first check read face normals, found all +Y, and
   concluded "correct" — asserting the convention instead of testing it. Rendering both
   orders: the old one covers **0** of 25,600 sampled pixels, the new one 70.9%.
