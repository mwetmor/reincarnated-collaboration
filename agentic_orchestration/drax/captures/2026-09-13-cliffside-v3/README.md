# Cliffside v3: continuous massif, padded canvas, chunk grid, scene data (drax, 2026-09-13)

This is v3 under R-C3-48. The problem it fixes: the v2 guides cut every camera-facing cliff face 7 m below its rim and left empty space beneath. That made hard straight bottom edges and opened a window through rock under the plateau, so it read as a bridge with no underside.

Nothing was painted or generated; everything comes from the Godot greybox.

**Sources**
- Scene: `reincarnated-godot/scripts/cliffside_blockout.gd --v3`
- Packaging: `scripts/cliffside_v3_package.py`
- Layout, camera and 100.6176 px/m scale are unchanged from v2.

## Geometry fix
- **Faces run to 20 m.** Every camera-facing cliff face continues down to 20 m below its rim; the masks and guides cut at 20 m. In the geometry the walls actually run the full 40 m drop.
- **Solid rock under the bay.** In v2 the space cut out in front of the plateau went all the way through the rock mass. v3 adds solid rock beneath it: the same outline without the cut-out, running from 20 m down to 40 m. The cut-out is now a 20 m-deep notch with a rock floor at the cut, not a slot you can see through.
- **Masks come from the nearest surface.** The mask and depth map record, for each pixel, the nearest surface the view hits. Nothing is hidden to expose rock behind it, so no window can open. Void appears only where the view meets no rock above the 20 m cut: beyond the far-side rim, and through the chasm below 20 m.

## Canvas: 5376×4096, same top-left origin as v2

| File | What it is |
|---|---|
| `07_ortho_canvas_shaded_v3.png` | Shaded greybox, orthographic, yaw 47° / pitch 52.954°, 100.6176 px/m. RGBA, alpha 0 where there is no terrain |
| `08_ortho_canvas_layer_id_v3.png` | Flat layer-ID colours |
| `ortho_canvas_v3_mask.png` | 8-bit: 255 wherever terrain exists down to the 20 m cut, 0 elsewhere |
| `ortho_canvas_v3_depth_mm.png` | **Depth below rim**, 16-bit (format below) |
| `work/ortho_canvas_v3_depth_rgba.png` | Raw Godot depth render (R = high byte, G = low byte, in mm; B = 255 where a surface was hit) |
| `work/blockout_meta_v3.json`, `work/scene_data_raw.json` | Raw numbers from the Godot run |

The canvas was rendered at full size, not padded afterwards: faces running to 20 m extend below v2's 3980-row edge, reaching row 4004 under the plateau tip.

v3 pixel coordinates equal v2's minus (0.41, 0.06) px. v2 centred a canvas whose width and height had been rounded up to whole pixels; v3 pins the top-left exactly. Plateau spawn: v2 (2286.03, 2407.38), v3 (2285.62, 2407.32).

### Depth map format
- **Encoding:** 16-bit greyscale PNG (uint16); each value is millimetres below the local rim.
  - `0` = walkable or top surface at rim level, including the tops of boulders and posts.
  - `1…20000` = cliff face, or the 20 m rock floor of the notch.
  - `65535` = not foreground. Read it together with the mask.
- **Rim height:** every rim in this level is at y = 0, so depth = max(0, −y).
- **Verified:** down the plateau tip face the value rises 16.4967 mm per row, which is exactly 1 m ÷ 60.6183 px.
- **Fade for assembly:** alpha = 1 for mm ≤ 8000; (20000 − mm) / 12000 for 8000 < mm ≤ 20000; 0 beyond.

## Chunk grid (`chunks/`, `chunks_v3.json`)
- **Grid:** 1536×1024 chunks stepping 1280 px across and 768 px down (256 px overlaps). Origins x ∈ {0, 1280, 2560, 3840}, y ∈ {0, 768, 1536, 2304, 3072}.
- **Files per chunk:** `chunk_<ix>_<iy>_guide.png` (non-foreground = pure #00ff00), `_mask.png`, `_depth.png` (16-bit, format above), `_id.png`.
- **Kept:** 17 of 20. Dropped: chunk_0_0, chunk_1_0 and chunk_0_1, all 0 % foreground.

**Paint order:** row by row, top to bottom, left to right. "After" lists the neighbours that must be painted first.

| # | Chunk | Origin | Foreground | After |
|---|---|---|---|---|
| 1 | chunk_2_0 | (2560, 0) | 36.3 % | — |
| 2 | chunk_3_0 | (3840, 0) | 76.5 % | 2_0 |
| 3 | chunk_1_1 | (1280, 768) | 25.8 % | — |
| 4 | chunk_2_1 | (2560, 768) | 79.9 % | 1_1, 2_0 |
| 5 | chunk_3_1 | (3840, 768) | 100 % | 2_1, 3_0 |
| 6 | chunk_0_2 | (0, 1536) | 10.5 % | — |
| 7 | chunk_1_2 | (1280, 1536) | 83.1 % | 0_2, 1_1 |
| 8 | chunk_2_2 | (2560, 1536) | 100 % | 1_2, 2_1 |
| 9 | chunk_3_2 | (3840, 1536) | 100 % | 2_2, 3_1 |
| 10 | chunk_0_3 | (0, 2304) | 74.9 % | 0_2 |
| 11 | chunk_1_3 | (1280, 2304) | 100 % | 0_3, 1_2 |
| 12 | chunk_2_3 | (2560, 2304) | 100 % | 1_3, 2_2 |
| 13 | chunk_3_3 | (3840, 2304) | 99.9 % | 2_3, 3_2 |
| 14 | chunk_0_4 | (0, 3072) | 100 % | 0_3 |
| 15 | chunk_1_4 | (1280, 3072) | 100 % | 0_4, 1_3 |
| 16 | chunk_2_4 | (2560, 3072) | 100 % | 1_4, 2_3 |
| 17 | chunk_3_4 | (3840, 3072) | 100 % | 2_4, 3_3 |

Diagonal neighbours above-left and above-right also share 256×256 corners. They are listed in `chunks_v3.json` and always come earlier in this order.

## Scene data (canvas px)

**`walkable.json`**
- **Walkable:** path_0, path_1 (after the chasm), the plateau, and bridge planks 0, 1, 2, 4 and 5. Plank 3 is in `walkable_flagged` with flag `falls_out`.
  - Polygons are ground-level outlines. The path and plateau polygons overlap where the path runs onto the plateau, so treat walkable as their union.
- **Blocked:** 6 rock footprints at ground level, 4 bridge posts, and 2 bridge rail strips.
  - The blockout has no rail mesh, only posts, so the rails are *implied*: 0.3 m strips along the deck edges.
- **Spawn:** feet on the plateau at **(2285.62, 2407.32)**. The analytic projection matches Godot's own projection to 0.01 px.
- **Bounds:** level [0, 0, 5376, 4096]; walkable bounding box [414.17, 383.17, 4249.43, 3390.22].

**`parallax.json`**
- **Camera rule:** view top-left = feet − (962, 595), clamped to [0, 3456] × [0, 3016].
- **Travel:** with the feet anywhere inside the walkable bounding box, the view ranges x 0–3287.43 and y 0–2795.22.
- **Layer size:** minimum layer size = view + factor × travel.

| Layer | Factor | Minimum size, walkable travel | Minimum size, full-canvas travel |
|---|---|---|---|
| sky | 0.12 | **2315 × 1416** | 2335 × 1442 |
| far_ruins | 0.25 | **2742 × 1779** | 2784 × 1834 |
| forest_valley | 0.45 | **3400 × 2338** | 3476 × 2438 |
| mist | 0.70 | **4222 × 3037** | 4340 × 3192 |

## Uncertain / worth a look
- **Most chunks are all ground:** the near-side landmass the path sits on is 30 m wide, so 11 of the 17 kept chunks are 99.9–100 % foreground. That is correct for the geometry. Narrowing it would be a layout change, which was not made.
- **Rock floor at the cut:** the rock floor of the notch sits exactly at 20 m, where the fade reaches alpha 0. It counts as terrain in the mask but disappears in the assembly.
- **Travel is an upper bound:** the travel figures use the walkable bounding box, which includes corners the feet cannot reach. The full-canvas column is the absolute upper bound.
- **Top surfaces of rocks and posts:** they are 0 depth because they are above the rim. Their tops are not walkable; they appear only as blocked ground footprints.
- **Face shading:** all camera-facing faces (plateau tip, walls of the notch, chasm far wall, landmass edges) are one flat dark grey, and all are `cliff_rock` in the ID images.
