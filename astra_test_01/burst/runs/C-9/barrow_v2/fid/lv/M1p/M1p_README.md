# M1′ packet: barrow_v2 ART blockout (Matt R-C9-185; charter v1.0 § 15)

**Cover (`M1p_cover.jpg`, one phone screen): three asks, one recommendation each**
1. **Approve the composition for paint?** Recommended: yes, and start the paint pilot on the home ground. The site is 66 × 51 m, painted as 25 canvases (v1: 53 × 41 m, 16).
2. **Burnt hall: closed sides except the great door, or an open-sided ruin?** Recommended: closed sides except the great door, so there are no false doorways.
3. **How to walk it?** Recommended: the `.command` launcher on the Mac now; a packaged .app later.

Geometry check P6′: PASS — present, in place, true proportions (PH 51d955677).

**Files**
- `M1p_cover.jpg` — the cover.
- `M1p_stills_A/B/C.jpg` — 12 play-camera stills at v1's camera and zoom, each framed on its hero(es) and placed beside sketch A's matching area.
- `M1p_map.jpg` — labelled top-down map of the 66 × 51 m window.
- `M1p_guide.jpg` — the class-tinted guide with its class map.
- `Walk barrow_v2 art.command` — the walk; double-click on the Mac.

**What it is**
- Sketch A, taken literally: its pixels are used as a map at 24 px/m, the scale at which sketch A's own wreck comes out at the kit wreck's true 13 m.
- Authored in v1's camera-aligned (u, v) frame, the way v1's layout was. There is no site rotation (DEV-4 retired).
- Kit-v3 heroes at one uniform scale each: wreck 1.0, barrow front 0.45, hall 0.571 (18.5 m, sketch A's length). The fallen gable is its own ruin at 8 m.
- v1 stones; cliffs and crags from the earlier model builds, re-scaled uniformly. Palisade, logs and stair treads are procedural at true size.
- Layout of record: `fid/lv/art/layout_bv2art.json`. Kit inventory and footprint: `fid/lv/art/kit_inventory.json`. Frame: `fid/lv/art/frame_grid.bv2art.json`.

**Phase 1′ DONE items**
- **Measured footprint:** the window is 66.2 × 51.0 m. Placed geometry spans 65.9 m in u and 58.2 m in v; the v figure includes the cliff faces down to the sea.
- **Declared openings:** `fid/lv/guide_art/declared_openings.json`. A `char` class (the gable ruin) and an `ash` class (the hall yard) are in the class map.
- **Scale:** per-instance scale and anisotropy in `fid/lv/placed_fit_bv2art.json`. Maximum anisotropy is 1.0001; procedural pieces are N/A.
- **Hero coverage:** all 7 heroes PASS. Each is visible in at least one still with at least one other hero, measured from the ID render of the stills.

| Hero | Visible in (stills) | With a neighbour hero in | |
|---|---|---|---|
| wreck | 02, 03, 06 | 02, 03, 06 | PASS |
| cave_stair | 07, 08 | 07 | PASS |
| barrow_door | 04, 05 | 04, 05 | PASS |
| mere | 02, 03, 04, 05, 06, 12 | 02, 03, 04, 05, 06, 12 | PASS |
| ring | 01, 07, 12 | 07, 12 | PASS |
| hall_door | 09, 10, 11 | 09, 10, 11 | PASS |
| gable | 09, 10, 11 | 09, 10, 11 | PASS |

**Check (a), INFO only:** entrances visible from the play camera.

| Opening (anchor) | Probe | Faces camera | Visible m² | % of unoccluded | Frontal m² | % of frontal | |
|---|---|---|---|---|---|---|---|
| wreck_hull (W) | h_rect | yes | 12.33 | 81.6 | 18.9 | 65.1 | PASS |
| barrow_door (N) | v | yes | 4.70 | 100.0 | 7.8 | 60.0 | PASS |
| hall_great_door (E) | v | yes | 3.22 | 100.0 | 7.0 | 45.6 | PASS |
| gable_breach (SE) | h_rect | yes | 10.86 | 85.0 | 16.0 | 67.9 | PASS |
| sea_cave_mouth (SW) | v | yes | 4.00 | 42.0 | 15.8 | 25.2 | PASS |
| mere_ice (NW) | poly | yes | 119.78 | 91.5 | 164.0 | 73.0 | PASS |

**R-C9-186 presence fix:** crag #2 and driftwood log #3 moved onto the beach shingle. They had sunk below sea level when the shore was moved east. Slope stone #4 moved down the barrow slope, inside the paint envelope. Guide/ID re-rendered; hero coverage 7/7; check (a) 6/6 (INFO).
