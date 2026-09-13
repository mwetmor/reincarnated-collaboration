# Cliffside greybox: checkpoint 1 (drax, 2026-09-13)

This is a greybox blockout of the cliffside path. It uses only primitives and flat colours: no painting, no generated images, no new art. It was built for R-C3-42 checkpoint 1 (plan: `gandalf/notes/2026-09-13-cliffside-scene-hitl-plan.md`), with gandalf's orthographic-canvas addendum added.

- **Scene:** `reincarnated-godot/scenes/cliffside_blockout.tscn` (commit `de4fe2c`, not pushed)
- **Build and render script:** `scripts/cliffside_blockout.gd`
- **Composite script:** `scripts/cliffside_blockout_composite.py`
- **Renderer:** Godot 4.6.3, Forward+/Metal, windowed run, SubViewport readback
- **Machine-readable numbers:** `blockout_meta.json` (camera, measurements, layout, bands, ortho canvas) and `composite_record.json` (sprite placement)

## Camera: GD `player_lock`, dolly k solved by measurement

The camera is a direct port of `wr2_playback.gd:_pl_build_lock`, using the constants from `kc2_cpb_clip.gd`:
- yaw 47°
- pitch 52.95354112560294° down
- vertical FOV 31.78610183061007° (KEEP_HEIGHT)
- anchor (0.50104, 0.55093)

At k = 1 the offset matches the `pl_audit.json` pin with a delta of 0.0 m. k scales only the offset vector.

**How k was solved.** A proxy-only mask pass was rendered: the 1.75 m capsule (r 0.30) at 4× supersampling (7680×4320), transparent background, MSAA. I read the capsule's silhouette height off that image and repeated `k ← k·h/target` until it matched. Precision is about ±0.25 px at 1080p, which is about ±0.2 % in k.

| Rung | k | Stand-off (m) | Camera height (m) | Measured silhouette (px @1080) | Still |
|---|---|---|---|---|---|
| 12.0 % | **0.562541** | 19.594 | 15.974 | 129.56 | `rung_plateau_12p0.png` |
| **12.5 %** | **0.541386** | **18.857** | **15.374** | **135.00** | `02_follow_plateau_k12p5.png` |
| 13.0 % | **0.521628** | 18.169 | 14.813 | 140.44 | `rung_plateau_13p0.png` |

- **Anchor check.** At all three follow positions the projected proxy ground point is exactly (962.0, 595.0) px.
- **Silhouette extent.** The silhouette spans y 472.75 to 607.75. Its bottom sits 12.75 px *below* the ground point, because the underside of the capsule's lower cap is visible from 53°.

## Layout (metres)

- **Path:** winding centreline, 46.4 m long, 6.1–8.9 m wide. On screen it runs from lower-left to upper-right.
- **Plateau:** at s = 20.9 m, about 14 m along × 12.5 m across. It pushes out toward the cliff.
- **Cliff:** a 1.2 m rock lip, then a sheer 40 m drop on the far (upper-left) side.
- **Near side:** a dark rock wall along s 3–12 and s 25–31, plus boulders.
- **Chasm:** s 33.4–43.4 m, 10.0 m across. It cuts all the way through the landmass.
- **Bridge:** 3 m wide, 6 planks. Plank index 3 (the 4th from the near end) is flagged `falls_out` and coloured magenta (metadata `falls_out=true`).

**Background depth bands** are all on render layer 16, separate from the foreground, so they can become parallax layers later:

| Band | Where | Colour |
|---|---|---|
| Valley floor | y = −40 m, parallel to the cliff, extends under the landmass, a few mounds | olive |
| Charred forest | 150–300 m out (screen-up beyond the cliff), y −158 → −273 m, burnt trunks | dark red-brown |
| Temple ruins | 380–430 m out, y −328 → −361 m, broken columns/walls (boxes) | pale ochre |
| Sky | camera-facing card 1500 m along the view axis; orange at top (toward the horizon) → violet at bottom | gradient |

**Why the far bands sit so low.** At this pitch and FOV the top edge of the frame looks 37° below the horizon, so the horizon is never in frame. A band "300 m out" is only visible if it is also about 250 m *below* the path. I set each band's height so its edges fall at chosen view-down angles from the plateau camera (forest 45.5°→42°, ruins 40.6°→39.9°). With this camera, "beyond" means "below".

**Lighting.** Directional light comes from screen upper-left, with shadows and ambient 0.45. A depth haze toward the sunset colour starts 40 m from the camera, so it touches only the background bands. It is off in the ID passes and on the ortho canvas.

## Images

| File | What it is |
|---|---|
| `01_follow_start_k12p5.png` | Follow camera at 12.5 %, proxy at path start |
| `02_follow_plateau_k12p5.png` | Same, proxy at the plateau vista point |
| `03_follow_bridge_approach_k12p5.png` | Same, proxy 2.5 m before the chasm edge |
| `rung_plateau_12p0.png`, `rung_plateau_13p0.png` | Plateau at the 12.0 % and 13.0 % rungs |
| `04_overview_x3.png` | Offset ×3 (k 1.6242, stand-off 56.57 m, height 46.12 m), same angles, centred on the path's bounding box; all three proxies |
| `05_layer_id_plateau_k12p5.png` | Unlit, one flat colour per class, plateau position. Legend in `blockout_meta.json` → `layer_id` |
| `06_far_layers_only_plateau_k12p5.png` | Background bands only, from the plateau follow camera (valley, forest, ruins, sky) |
| `07_ortho_canvas_shaded.png` | **Ortho level canvas**, foreground only, shaded, transparent background. 4977×3980 px |
| `08_ortho_canvas_layer_id.png` | Same canvas, flat layer-ID colours |
| `09_compare_plateau_perspective_vs_ortho.png` | Perspective plate, ortho crop, and an ID-edge overlay at the plateau (see below) |
| `10/11/12_composite_*_k12p5.png` | Keeper idle_S_00 on the clean plate at each follow position. The plateau also has walk_E_03 beside it |
| `13_sheet_plateau_vs_LE05_D206.png` | Plateau composite beside LE-05 and D2-06 at equal display height (720 px), labelled |
| `work/plate_*_k12p5.png` | Clean plates: the same follow render with the proxy hidden. These are the base for the composites |

## Orthographic level canvas (addendum)

- **Projection.** Same basis as `player_lock` (yaw 47°, pitch 52.954°), orthographic, foreground layer only (path, landmass top and cliff, rocks, plateau, bridge). No background bands, no proxies.
- **Scale.** I measured **100.6176 px/m** along screen-x at the plateau proxy ground point in the 12.5 % follow render, and set the ortho size to match: 39.556 m of view height over 3980 px. On the canvas that gives:
  - screen-x: 100.62 px per ground metre
  - screen-y: 80.31 px per ground metre of depth (×sin pitch)
  - screen-y: 60.62 px per vertical metre (×cos pitch)
- **Tiles.** The canvas is a single image; it stayed under the viewport size limit, so no tiles were needed.
- **Proxy ground points in canvas px:**
  - start (974.9, 2938.9)
  - plateau (2098.1, 1925.2)
  - bridge_approach (2942.6, 1465.4)
- **Bounds.** The canvas covers path, lip and a 7 m near-side rock band over s −4…50.4. The landmass continues past the canvas edges, and the chasm wall runs down its right side.
- **Capsule size.** In ortho the 1.75 m capsule measures **130.0 px**, against 135.0 px in perspective at the same px/m.

### Perspective vs ortho at the plateau (`09_…`)

Both images are aligned so the plateau ground point sits at (962, 595). They agree only near that point, and differ more toward the top and bottom of the frame.

**Measured through the perspective camera at column 962:**

| Row | Ground screen-x px/m | Ground-depth screen-y px/m | Vertical px/m |
|---|---|---|---|
| 0 (top) | 77.3 | 48.4 | 64.2 |
| 595 (anchor) | 100.6 | 82.1 | 58.3 |
| 1079 (bottom) | 119.6 | 116.0 | 44.9 |
| **ortho, everywhere** | **100.6** | **80.3** | **60.6** |

- **Top to bottom.** In perspective, ground detail at the top of the frame is drawn at 0.77× and at the bottom at 1.19×. Depth foreshortening varies 2.4× from top to bottom. In ortho it is constant.
- **How much ground each frame shows.** The perspective frame shows 9.4 m of ground above the anchor and 4.9 m below. A same-size ortho window shows 7.4 m above and 6.0 m below.
- **In the edge overlay.** The cliff lip and the near rocks spread apart toward the top and bottom edges by tens of pixels. Tall things lean outward from the frame centre in perspective and stay parallel in ortho.

**What this means for the painted scene.** A painting made over the ortho canvas will always match itself as the camera moves. It will not show the perspective render's "wider at the bottom" look. The perspective renders remain the look check.

## Composites

**Sprite placement.**
- **Idle frame:** `idle_S_00.png`, cropped to its alpha ≥ 128 bounding box (92×240 px), scaled ×0.5625 to 52×135 px (the capsule's measured silhouette height). Its feet (bottom-centre of the box) sit on the projected ground point (962, 595).
- **Walk frame:** `walk_E_03.png`, at the same ×0.5625 scale (70×134 px). Both cells share the 512 canvas at the same scale, so I kept one factor rather than stretching each frame to 135. Its feet are on a ground point 1.4 m to screen-right: (1102.9, 595).
- **Shadows:** none on the proxy or the sprites.

**Placement choices that change the read:**
1. With the feet on the ground point, the sprite's head is 12.75 px higher than the capsule top, because the capsule silhouette extends below the ground point.
2. There is no contact shadow.

## What did not work, or needs your eye

- **The sheer drop hides its own face.** The cliff is on the side away from the camera, so from 53° you cannot see a far-side cliff face. The drop reads only through the valley and haze. The face shows only where the edge turns toward the camera: the plateau's lower-left flank, the chasm far wall, and the canvas left edge. To show the drop like LE-05 does, the painting needs a cheat (a visible lip or strata), or the layout needs edges that face the camera.
- **The background is only a small corner of the frame.** At 12.5 % the upper-left corner beyond the cliff is roughly a quarter of the frame at the plateau, and less at the start. The four bands squeeze into about 10° of view angle.
- **Godot crashed once on exit (signal 11)** after all files were written, on the first run only. The later runs exited cleanly, and no output was affected.
- **The perspective ID pass has soft edges** from MSAA (colours blend at class boundaries). Classes can be recovered by nearest colour.

## v2: plateau re-route (R-C3-44)

Matt accepted the 12.5 % rung. I then rebuilt the vista plateau as a promontory that juts toward the camera, so its 40 m face is visible below the rim. To give it empty space in front, the near-side landmass is cut back to a rim over s = 6.9–29.9 m. The run is `cliffside_blockout.gd --v2`. It reuses the accepted k = 0.541386 and the 100.6176 px/m scale as constants rather than solving them again. All v1 files above are unchanged.

| File | What it is |
|---|---|
| `02_follow_plateau_v2_k12p5.png` | Follow camera on the plateau spawn point. Anchor (962.0, 595.0); capsule still measures 135.0 px |
| `07_ortho_canvas_shaded_v2.png`, `08_ortho_canvas_layer_id_v2.png` | Ortho foreground canvas, 4977×3980 px (same size and origin as v1) |
| `work/ortho_canvas_v2_fgmask_cut7m.png` | Foreground mask: fragments below −7 m are dropped, anti-aliasing off. This is the source of the chunk masks |
| `blockout_meta_v2.json` | v2 numbers plus key points in canvas px (rim and 7 m cut corners, spawn point, path centres) |

The chunk guides built from this canvas are in `../2026-09-13-cliffside-chunks/`.
