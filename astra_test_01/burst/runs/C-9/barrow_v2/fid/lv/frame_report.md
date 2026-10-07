# BV2F LV — Phase 0.2 frame fix (DEV-4, plan C6): report

**Lane:** LV (drax). **Spend:** $0, no images. **Files read but not edited:** `layout_v2.json`, `barrow_full.gd`, `barrow_heather.gd`, `barrow_v2_sw.gd`. Nothing was written to `barrow_full/godot` (R-C9-163).

## 1. The transform
```
world = R_y(+47°) · (x, z, y)        Godot: Basis(Vector3.UP, deg_to_rad(47)) * Vector3(x, z, y)
rot_y_world = rot_y_sim + 47°        (a model's Godot yaw turns with the site)
```
Sim +x (east) maps to v1's `u_hat` = (cos47, 0, −sin47), which is screen-right (`barrow_full.gd:76`). Sim +y (south) maps to −`v_hat`, which is screen-down. The camera, the heather card basis, the suns, the snow and the pen are unchanged.
- Python: `fid/lv/frame.py`
- GDScript twin: `fid/lv/godot/frame.gd`. The twin matches `frame.py` to 6.5e-7 m in world coordinates and 1e-4 px on screen. Godot's own `unproject_position` gives the same result.

## 2. Sign test (`fid/lv/test_frame.py` → `frame_proof/test_frame_output.{txt,json}`): ALL PASS
| Test | Result |
|---|---|
| T1: the analytic v1 camera basis equals the live basis recorded in `barrow_heather.gd:43-45` | max diff 2.4e-7 |
| T2: p02 is screen-UP of the start; p01 is screen-LEFT | p02 (958, −2546) px; p01 (−3462, 769) px |
| T2b: p04 is screen-RIGHT; p03 is screen-DOWN | PASS |
| T3: the v1 camera applied to R_y(+47)·sim equals the layout's own yaw-0 law (6 anchors + 81 grid points × 3 heights) | worst 1.8e-12 px. **The play camera sees exactly the frame layout_v2 was composed in.** |
| T4: negative controls are rejected (yaw −47: off by 12,480 px; yaw 0, the R-C9-159 case: off by 6,335 px, p02 lands up-right at 21.5°) | PASS |
| T5: round trip and model yaw | 3.6e-15 |

## 3. Play-camera render and overlay (`frame_proof/`)
- `render_fixed.png` is the fix. `render_r159.png` is the negative control (site unrotated).
- Both are rendered by Godot 4.6.3 through v1's camera law: orthographic, pitch 52.954°, yaw 47°.
- Both are unlit marker renders. They show the anchors with their 8 m discs, the floor, the coastline (the cliff lip, in red), the shore ice, the mere, the stream, the path, the stone circle, the mound and barrow door, the wreck and mast, the hall with its porch and great door, the gable, the cave mouth and the stair.
- Magenta arrows show `faces_deg`. The black arrow shows the stair's climb direction.
- `overlay_fixed.png` and `overlay_r159.png` put sketch A and the render side by side, with bearing rays drawn on both.
- Sketch anchors were measured by ellipse-fitting each patch outline (`sketch_anchors.py` → `sketch_anchor_px.json`). The patch centre is the anchor; the dots are the doors.

### I-2 mechanical decision (`overlay.py` → `bearings.json`)
Bearing = angle of the anchor from the start on screen, in degrees counter-clockwise from screen-right.

| Anchor | Sketch A | Fix (+47) | Δ | R-C9-159 (0) | Δ |
|---|---|---|---|---|---|
| p01 | 182.2 | 192.5 | +10.3 | 154.0 | −28.2 |
| p02 | 80.8 | 69.4 | −11.4 | 21.5 | −59.3 |
| p03 | 228.4 | 287.8 | **+59.4** | 231.3 | +2.9 |
| p04 | 357.0 | 350.1 | −6.9 | 306.6 | −50.4 |
| p05 | 146.3 | 150.6 | +4.3 | 99.7 | −46.6 |
| p06 | 338.1 | 325.4 | −12.7 | 272.8 | −65.4 |
| Cyclic order | p02 p05 p01 p03 p06 p04 | match | | match | |
| Similarity-fit rotation | | **−3.2°** | | +41.6° | |

**I-2 = FAIL, on p03 alone. The cyclic order matches; the other five anchors are within 12.7°.**
- No frame yaw can pass I-2. Sweeping the yaw from 0° to 90° gives:
  - with p03 excluded, the best yaw is 48.5° (max 11.6°); +47° gives 12.7°;
  - with all six anchors, the best is 34.3° max error at yaw 26.5°, which would break every other anchor.
- The cause is in the data, not the frame. p03 comes from the pack, verified by R1: (8.23, 32.06), which is south and slightly **east** of the start. Sketch A draws the p03 patch south-**west** of the start, above the cave.
- **The conductor must rule on this.**

## 4. Features whose orientation disagrees with sketch A (fix frame)
These are all layout-vs-sketch differences. T3 shows the play view now equals layout_v2's own frame.

**Agree:** barrow door (faces screen-down); mere (up-left of the start, covering p05); coastline (sea to the west and south, with shore ice in the west); cave mouth (faces screen-down, in the south face).

**Disagree:**
1. **Hall, great door and gable.**
   - Sketch: the hall runs from upper-left to lower-right, the great door's wall faces down-left toward the camera, and the gable is down-right of p04.
   - Layout: the hall runs from upper-right to lower-left (axis 222.99°), the great door faces **up-left** (`faces_deg` 312.99, NW), and the gable is at the hall's lower-left end.
   - This is about 90° off.
2. **Wreck.** The sketch hull is diagonal, bow to the upper-left. The layout hull is nearly vertical on screen (`faces` 78°). The R-C9-162(b) rebuild may resolve this.
3. **Stair.** The sketch flight climbs screen-up from the cave to the p03 patch. The layout flight runs screen-right along the face (axis 78°). This is what R-C9-148 ruled ("its run angles across the face").
4. **p03 position**, as in § 3.
5. **Stream.** The sketch shows the frozen channel upper-left. The layout stream comes off the barrow's west flank. This follows R-C9-145 (sketch B's stream) and is not a defect.

## 5. M0(a) lagoon and spit removal — Phase 1 touch list (not done)
**There is no lagoon or spit entry in `layout_v2.json`.** It has `sea.z_m` −7.5 and `shore_ice` at z −0.4, the wreck sits at z −0.45, and `terrain_h.f32` has no −1.3 shelf.

The −1.3 m lagoon and its spit were introduced by the R-C9-159 section build. They live in:
- `tools/v2sw_prep.py:87` (`lagoon {z −1.30, spit_a, spit_dir}`)
- `tools/section_sw_build.py:55-68, 175-182, 245-247, 334-343, 399-403, 475, 510, 573, 707-709`
- `tools/section_sw_paintcfg.py:32-33, 59`
- `godot/scripts/section_sw.gd:255-269`
- `barrow_full/godot/scripts/barrow_v2_sw.gd:36, 180-186, 810`
- `barrow_full/godot/data/barrow_v2_sw/{level,section}.json`

In Phase 1, the layout_v2 work is to **state** "one sea level". The entries that work touches:
- `sea`
- `shore_ice` (make the wreck "beached in shore ice" explicit)
- `features.wreck_hull` and `features.wreck_mast` (z, footprint)
- `models.wreck` (rebuilt per M0(b))
- `land` (the west edge, if the spit's corner is re-cut)
- `sculpt.heightfield` (re-run `sculpt_v2.py`; its sha changes)

Validator rules it touches:
- **R5**: blockers outside the floor; heightfield exactly 0 on the floor.
- **R10**: p01 wreck outside the edge and within 3.0 m of it.
- **R12**: the wreck-rail lane, at least 4.0 m.
- R1–R4 are unaffected.
- **R9** ("zero yaw") stays true: the layout's camera block is the *sim* camera, and the +47° now lives only in sim→world. Its text should say so in Phase 1.

## 6. For the conductor
1. Rule on I-2 = FAIL on p03 (pack data vs sketch A). Options:
   - accept the frame on the five-anchor result plus the −3.2° fit;
   - record p03 as a sketch-vs-oracle divergence;
   - or rule some other way.
2. The hall's orientation is about 90° off sketch A (§ 4.1). Phase 1 should decide whether layout_v2 turns the hall or whether this stands.
