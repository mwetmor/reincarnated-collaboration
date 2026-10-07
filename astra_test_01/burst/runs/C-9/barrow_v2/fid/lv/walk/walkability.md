# Sea-cave route -- walkability (R-C9-188/189)

Against the art level's **colliders** (terrain HeightMapShape3D, the stair's nosing ramp, the cave hood, the bounds), by `barrow_full/godot/tools/bv2f/walk_check.gd`, driven by `fid/lv/tools/lv_walkability.py`.

**v1's character step height:** `scripts/knight.gd` is a CharacterBody3D capsule r 0.35 m, h 1.85 m, on plain `move_and_slide()` with 18 m/s2 gravity and no step-up code; floor_max_angle 45 deg (Godot's default, not set): an edge is mounted only while the contact normal is within that of up, so **step height = r (1 - cos 45 deg) = 0.103 m** (read off the running node).

| bar | measured | |
|---|---|---|
| continuous walk surface, cave -> clifftop (every 0.05 m) | 638 of 638 centreline samples walkable; 0 breaks | PASS |
| stair slope <= 35 deg | 33.34 deg (collider); treads 33.34 deg | PASS |
| shelf slope <= 10 deg | 5.09 deg | PASS |
| no riser above v1's step height (0.103 m) | max 0.033 m between samples 0.05 m apart (treads' visual riser 0.250 m is under the ramp) | PASS |
| stair clear width >= 5 m | min 5.40 m over 17 sections | PASS |
| shelf clear width >= 6 m | min 6.25 m over 9 sections | PASS |
| cave mouth clear height ~7 m | 7.40 m at the arch's lip (the first centreline sample under the roof); 4.85 m deeper in; the floor 4.67 m clear across 1 m inside | PASS |
| v1's knight driven from inside the cave to the clifftop | reached True in 21.0 s (1258 frames, 0 off the floor); ends at uv (7.33, -15.83) z 2.50 | PASS |

**Verdict: PASS**

| segment | samples | walkable | max slope | max dz / 0.05 m | z range | min headroom |
|---|---|---|---|---|---|---|
| cave | 60 | 60 | 0.00 deg | 0.000 m | -3.50 .. -3.50 | 4.85 m |
| shelf | 249 | 249 | 5.09 deg | 0.019 m | -3.53 .. -3.46 | 15.00 m |
| stair | 183 | 183 | 33.34 deg | 0.033 m | -3.48 .. 2.50 | 15.00 m |
| landing | 97 | 97 | 0.00 deg | 0.000 m | 2.50 .. 2.50 | 15.00 m |
| clifftop | 49 | 49 | 0.00 deg | 0.000 m | -3.50 .. 2.50 | 15.00 m |

Sections (clear width = walkable run across, capped by the free run to the nearest collider at 0.4 m and 1.2 m):

| section | surface | free between colliders | clear | headroom |
|---|---|---|---|---|
| stair_00 | 5.40 | 5.50 | 5.40 | 15.00 |
| stair_01 | 5.40 | 5.54 | 5.40 | 15.00 |
| stair_02 | 5.40 | 5.57 | 5.40 | 15.00 |
| stair_03 | 5.50 | 5.63 | 5.50 | 15.00 |
| stair_04 | 5.50 | 5.66 | 5.50 | 15.00 |
| stair_05 | 5.45 | 5.67 | 5.45 | 15.00 |
| stair_06 | 5.55 | 5.75 | 5.55 | 15.00 |
| stair_07 | 5.50 | 5.82 | 5.50 | 15.00 |
| stair_08 | 5.50 | 5.71 | 5.50 | 15.00 |
| stair_09 | 5.45 | 5.91 | 5.45 | 15.00 |
| stair_10 | 5.55 | 5.87 | 5.55 | 15.00 |
| stair_11 | 5.50 | 5.66 | 5.50 | 15.00 |
| stair_12 | 5.50 | 5.74 | 5.50 | 15.00 |
| stair_13 | 5.45 | 5.65 | 5.45 | 15.00 |
| stair_14 | 5.55 | 6.07 | 5.55 | 15.00 |
| stair_15 | 5.50 | 6.18 | 5.50 | 15.00 |
| stair_16 | 5.50 | 6.30 | 5.50 | 15.00 |
| shelf_00 | 6.90 | 7.86 | 6.90 | 15.00 |
| shelf_01 | 6.25 | 6.53 | 6.25 | 15.00 |
| shelf_02 | 7.25 | 7.81 | 7.25 | 15.00 |
| shelf_03 | 7.25 | 7.81 | 7.25 | 15.00 |
| shelf_04 | 7.00 | 6.97 | 6.97 | 15.00 |
| shelf_05 | 7.40 | 7.44 | 7.40 | 15.00 |
| shelf_06 | 7.70 | 8.68 | 7.70 | 15.00 |
| shelf_07 | 7.50 | 8.15 | 7.50 | 15.00 |
| shelf_08 | 7.40 | 8.36 | 7.40 | 15.00 |
| cave_mouth | 6.10 | 4.67 | 4.67 | 0.43 |

Stills: `route_topdown.png` (straight down, north up) and `route_play.png` (v1's play camera) -- the magenta line is the knight's DRIVEN track (a check overlay, not in the guide); him on the stair for scale.

Where it stands: cave W, stair E as sketch A draws them: the cave under the lip at u -9.5, the stair climbing east across the face to the clifftop at u 6.9
