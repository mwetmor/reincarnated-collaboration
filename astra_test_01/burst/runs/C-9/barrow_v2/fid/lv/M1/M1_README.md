# M1 cover (`M1_cover.jpg`, one phone screen): three asks

1. **Which layout?** Recommended: **v7c**.
   - v7c passes check (a): all six openings are visible.
   - v7c separates the fallen gable again as its own ruin. This reverses the merged hall Matt saw after R-C9-148.
   - v7b is **comparison only**: it fails check (a).
2. **The burnt hall: open sides?** Recommended: **keep the ruin closed-sided except the one declared great door**, so there are no false entrances.
3. **The walk:** Recommended: the **.command on the Mac now**. A packaged .app can come later.

P6′ result: _PENDING (PH re-measure on `fid/lv/placed_fit_v7c.json`)_.

---

# M1 packet: barrow_v2 layout v7c (RECOMMENDED), with v7b for comparison (BV2F lane LV, Phase 1, R-C9-177)

- `M1_stills_A.jpg` — stills 01–04 of v7c at v1's play camera and zoom, each framed on its hero object with him on the disc edge for scale, beside sketch A (not to scale): the start, the wreck, the barrow door, the sea cave.
- `M1_stills_B.jpg` — stills 06, 08, 09 and 10: the mere, then the p01, p02 and p03 discs, each with its deliverer, beside sketch A.
- `M1_stills_C.jpg` — stills 12 and 14: the p05 disc, and the cave top with the stair, beside sketch A.
- `M1_stills_hall_gable_v7c_v7b.jpg` — the hall and gable views (stills 05, 07, 11, 13): v7c on the left, v7b in the middle, sketch A on the right.
- `M1_map_v7c.jpg` — labelled top-down map of v7c, north up. Gold circles: the 8 m spawn discs. Magenta: the deliverer openings. Black line: the walkable edge.
- `M1_guide_v7c.jpg` — the class-tinted guide of v7c, with its class map below it.
- `M1_divergence.jpg` — anchor bearings against sketch A, plus one line each on the hall and the gable.
- `Walk barrow_v2 v7c.command` — the walkable greybox, with v1's controls, camera and rig. Double-click to run. Set `BV2F_VARIANT=v7b` to walk v7b instead.

**v7c compared with v7b:**
- **Hall:** in v7c the hall stands on the floor's north-east edge. It runs upper-left to lower-right, as in sketch A, and its great door faces south-west, toward the camera and onto p04, which it serves by its exit lane.
- **Gable:** the fallen gable is its own collapsed ruin on p06's ray. It uses BVP's ruin build at one uniform scale, 8 m.
- **Sea cave:** the cave-cliff rock that hid the cave mouth is trimmed, so the mouth is the cliff face itself. The rocks in front of it are cleared. The stair is unchanged (R-C9-148).
- **Validator:** R1–R13 pass 66/66 on both v7b and v7c.
- **Why the hall still differs from sketch A:** the sealed anchor data puts p06 screen-lower-left of p04, the opposite of the sketch. So no hall can serve p04 and also end on p06's ray (R-C9-174). In v7c the gable stands alone.

**Check (a): visible projected area of each opening at the play camera**

The figures come from frozen v1 tools: capture_ids (run through godot_run.sh) renders the openings with everything else in front of them, and again with nothing else, at v1's camera and zoom. "% of frontal" is the visible projected area as a share of the opening's own size.

- The door openings (barrow door, great door, sea cave) are measured as vertical surfaces.
- The open hull, the ruin's heap and the mere's ice are measured as horizontal surfaces.

v7c — **PASS**:

| Opening (anchor) | Probe | Faces camera | Visible m² | % of unoccluded | Frontal m² | % of frontal | |
|---|---|---|---|---|---|---|---|
| barrow_door (p02) | vertical | yes | 22.36 | 100.0 | 38.8 | 57.7 | PASS |
| hall_great_door (p04) | vertical | yes | 6.35 | 99.2 | 21.6 | 29.4 | PASS |
| sea_cave_mouth (p03) | vertical | yes | 21.55 | 54.8 | 65.3 | 33.0 | PASS |
| fallen_gable_breach (p06) | horizontal | yes | 10.98 | 86.0 | 16.0 | 68.6 | PASS |
| wreck_rail (p01) | horizontal | yes | 10.70 | 70.8 | 18.9 | 56.5 | PASS |
| mere_ice (p05) | polygon | yes | 373.61 | 99.9 | 468.7 | 79.7 | PASS |

v7b — **FAIL**. The great door faces away from the camera, and the cave mouth is 96 % hidden behind the cave-cliff rock:

| Opening (anchor) | Probe | Faces camera | Visible m² | % of unoccluded | Frontal m² | % of frontal | |
|---|---|---|---|---|---|---|---|
| barrow_door (p02) | vertical | yes | 22.36 | 100.0 | 38.8 | 57.7 | PASS |
| hall_great_door (p04) | vertical | **NO** | 0.00 | 0.0 | 21.6 | 0.0 | **FAIL** |
| sea_cave_mouth (p03) | vertical | yes | 1.47 | 3.7 | 65.3 | 2.2 | PASS |
| fallen_gable_breach (p06) | horizontal | yes | 14.94 | 85.5 | 21.9 | 68.2 | PASS |
| wreck_rail (p01) | horizontal | yes | 10.70 | 70.8 | 18.9 | 56.5 | PASS |
| mere_ice (p05) | polygon | yes | 373.61 | 99.9 | 468.7 | 79.7 | PASS |

**Anchor bearings against sketch A:** p01 +10.3°, p02 −11.4°, p03 +59.4° (registered divergence #1, R-C9-165), p04 −6.9°, p05 +4.3°, p06 −12.7°.

**R-C9-178 fixes (v7c re-rendered; validator 66/66; check (a) still 6/6):**
- **Braziers:** no model was ever built. A primitive stand-in (stand + bowl) of the slot's size now shows them.
- **Standing stones and grave markers:** they had been placed at z 0 on slopes up to 4.2 m, so terrain buried them. Both are now seated on the terrain; the stones show (22k ID px).
  - The grave markers stay small: they are 0.55 m tall, and 2 of the 7 lie inside the barrow-front model's footprint.
- **Cliff faces:** they stood inside the terrain's own rock face, centred on the lip and 6 m deep. Each is moved out by half its depth plus 0.5 m, and they now render (1.0M px).
- **Outcrops 3, 6, 7, 9, 12 and 13:** dropped from v7c because their centres lie outside the paint envelope (reasons in `layout_v7c.json` → `v7c_r178`).
- **Check (a) numbers:**
  - My probe figures stand. The probe is the opening's own plane at its mouth: the hall door is **6.35 m²**.
  - PH's 8.22 m² measured the dark curtain, a 0.3 m-thick box 1.6 m inside the door. Its top and side faces add projected area.
  - One rule now decides "faces camera" in both files (`lv_openings.faces_camera`, imported by the check):
    - The wreck rail's frame faces away (`frame_faces_camera: false`).
    - Check (a) measures the wreck's open hull, which is open to the sky (`check_a_faces_camera: true`).
