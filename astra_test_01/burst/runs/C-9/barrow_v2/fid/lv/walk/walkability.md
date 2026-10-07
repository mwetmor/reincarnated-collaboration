# Sea-cave route -- walkability (R-C9-188/189)

Against the art level's **colliders** (terrain HeightMapShape3D, the stair's nosing ramp, the cave hood, the bounds), by `barrow_full/godot/tools/bv2f/walk_check.gd`, driven by `fid/lv/tools/lv_walkability.py`.

**v1's character step height:** `scripts/knight.gd` is a CharacterBody3D capsule r 0.35 m, h 1.85 m, on plain `move_and_slide()` with 18 m/s2 gravity and no step-up code; floor_max_angle 45 deg (Godot's default, not set): an edge is mounted only while the contact normal is within that of up, so **step height = r (1 - cos 45 deg) = 0.103 m** (read off the running node).

| bar | measured | |
|---|---|---|
| continuous walk surface, cave -> clifftop (every 0.05 m) | 559 of 559 centreline samples walkable; 0 breaks | PASS |
| stair slope <= 35 deg | 33.48 deg (collider); treads 33.48 deg | PASS |
| shelf slope <= 10 deg | 0.00 deg | PASS |
| no riser above v1's step height (0.103 m) | max 0.033 m between samples 0.05 m apart (treads' visual riser 0.179 m is under the ramp) | PASS |
| stair clear width >= 5 m | min 5.25 m over 14 sections | PASS |
| shelf clear width >= 6 m | min 6.15 m over 6 sections | PASS |
| cave mouth clear height ~7 m | 7.00 m headroom; mouth 6.00 m wide | PASS |
| v1's knight driven from inside the cave to the clifftop | reached True in 17.6 s (1053 frames, 0 off the floor); ends at uv (-5.30, -8.59) z 0.00 | PASS |

**Verdict: PASS**

| segment | samples | walkable | max slope | max dz / 0.05 m | z range | min headroom |
|---|---|---|---|---|---|---|
| cave | 58 | 58 | 0.00 deg | 0.000 m | -5.00 .. -5.00 | 7.00 m |
| shelf | 224 | 224 | 0.00 deg | 0.013 m | -5.00 .. -5.00 | 7.00 m |
| stair | 151 | 151 | 33.48 deg | 0.033 m | -4.99 .. -0.03 | 15.00 m |
| landing | 75 | 75 | 0.00 deg | 0.000 m | -0.00 .. -0.00 | 15.00 m |
| clifftop | 51 | 51 | 0.00 deg | 0.000 m | -0.00 .. 0.00 | 15.00 m |

Sections (clear width = walkable run across, capped by the free run to the nearest collider at 0.4 m and 1.2 m):

| section | surface | free between colliders | clear | headroom |
|---|---|---|---|---|
| stair_00 | 5.50 | 5.60 | 5.50 | 15.00 |
| stair_01 | 5.45 | 5.60 | 5.45 | 15.00 |
| stair_02 | 5.35 | 5.53 | 5.35 | 15.00 |
| stair_03 | 5.35 | 5.49 | 5.35 | 15.00 |
| stair_04 | 5.35 | 5.54 | 5.35 | 15.00 |
| stair_05 | 5.40 | 5.57 | 5.40 | 15.00 |
| stair_06 | 5.40 | 5.51 | 5.40 | 15.00 |
| stair_07 | 5.35 | 5.45 | 5.35 | 15.00 |
| stair_08 | 5.35 | 5.39 | 5.35 | 15.00 |
| stair_09 | 5.25 | 5.35 | 5.25 | 15.00 |
| stair_10 | 5.30 | 5.45 | 5.30 | 15.00 |
| stair_11 | 5.40 | 5.50 | 5.40 | 15.00 |
| stair_12 | 5.35 | 5.44 | 5.35 | 15.00 |
| stair_13 | 5.35 | 5.39 | 5.35 | 15.00 |
| shelf_00 | 7.95 | 8.14 | 7.95 | 15.00 |
| shelf_01 | 7.85 | 8.06 | 7.85 | 15.00 |
| shelf_02 | 7.70 | 7.98 | 7.70 | 15.00 |
| shelf_03 | 6.25 | 6.44 | 6.25 | 15.00 |
| shelf_04 | 6.15 | 6.44 | 6.15 | 15.00 |
| shelf_05 | 6.20 | 6.44 | 6.20 | 7.00 |
| cave_mouth | 6.00 | 6.00 | 6.00 | 7.00 |

Stills: `route_topdown.png` (straight down, north up) and `route_play.png` (v1's play camera) -- the magenta line is the knight's DRIVEN track (a check overlay, not in the guide); him on the stair for scale.

Where it stands: sketch A draws the cave under the lip at u ~ -9 with the stair on its east; the 7 m mouth needs a brow 3 m over the clifftop, which there projects into the paint pilot's tiles (R-C9-189) -- so the stair TOP stays at sketch A's stair top (where the start's path ends) and the flight runs EAST down the face to the shelf and the cave (cave mouth u = 6.4)
