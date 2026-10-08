# Sea-cave route -- walkability (R-C9-188/189)

Against the art level's **colliders** (terrain HeightMapShape3D, the stair's nosing ramp, the cave hood, the bounds), by `barrow_full/godot/tools/bv2f/walk_check.gd`, driven by `fid/lv/tools/lv_walkability.py`.

**v1's character step height:** `scripts/knight.gd` is a CharacterBody3D capsule r 0.35 m, h 1.85 m, on plain `move_and_slide()` with 18 m/s2 gravity and no step-up code; floor_max_angle 45 deg (Godot's default, not set): an edge is mounted only while the contact normal is within that of up, so **step height = r (1 - cos 45 deg) = 0.103 m** (read off the running node).

| bar | measured | |
|---|---|---|
| continuous walk surface, cave -> clifftop (every 0.05 m) | 477 of 477 centreline samples walkable; 0 breaks | PASS |
| stair slope <= 35 deg | 32.66 deg (collider); treads 32.66 deg | PASS |
| iced landing (in the cove) slope <= 10 deg | 0.00 deg | PASS |
| no riser above v1's step height (0.103 m) | max 0.032 m between samples 0.05 m apart (treads' visual riser 0.250 m is under the ramp) | PASS |
| stair clear width >= 5 m | min 5.15 m over 12 sections | PASS |
| iced landing clear width >= 5 m (cave mouth -> past the jamb -> stair foot) | min 5.25 m over 7 sections | PASS |
| cave mouth clear height ~7 m | 7.16 m at the arch's lip (the first centreline sample under the roof); 4.78 m deeper in; the floor 4.10 m clear across 1 m inside | PASS |
| v1's knight driven from inside the cave to the clifftop | reached True in 14.7 s (881 frames, 0 off the floor); ends at uv (10.65, -0.33) z 0.74 | PASS |

**Verdict: PASS**

| segment | samples | walkable | max slope | max dz / 0.05 m | z range | min headroom |
|---|---|---|---|---|---|---|
| cave | 40 | 40 | 0.00 deg | 0.000 m | -3.50 .. -3.50 | 4.78 m |
| shelf | 213 | 213 | 0.00 deg | 0.000 m | -3.50 .. -3.50 | 15.00 m |
| stair | 133 | 133 | 32.66 deg | 0.032 m | -3.50 .. 0.72 | 15.00 m |
| landing | 40 | 40 | 0.00 deg | 0.000 m | 0.75 .. 0.75 | 15.00 m |
| clifftop | 51 | 51 | 4.64 deg | 0.004 m | 0.71 .. 0.75 | 15.00 m |

Sections (clear width = walkable run across, capped by the free run to the nearest collider at 0.4 m and 1.2 m):

| section | surface | free between colliders | clear | headroom |
|---|---|---|---|---|
| stair_00 | 5.30 | 7.00 | 5.30 | 15.00 |
| stair_01 | 5.30 | 7.07 | 5.30 | 15.00 |
| stair_02 | 5.30 | 6.11 | 5.30 | 15.00 |
| stair_03 | 5.30 | 5.42 | 5.30 | 15.00 |
| stair_04 | 5.15 | 5.39 | 5.15 | 15.00 |
| stair_05 | 5.15 | 5.39 | 5.15 | 15.00 |
| stair_06 | 5.30 | 5.63 | 5.30 | 15.00 |
| stair_07 | 5.30 | 5.61 | 5.30 | 15.00 |
| stair_08 | 5.30 | 5.57 | 5.30 | 15.00 |
| stair_09 | 5.20 | 5.33 | 5.20 | 15.00 |
| stair_10 | 5.20 | 5.29 | 5.20 | 15.00 |
| stair_11 | 5.15 | 6.60 | 5.15 | 15.00 |
| shelf_00 | 5.35 | 5.77 | 5.35 | 1.21 |
| shelf_01 | 9.70 | 10.10 | 9.70 | 1.19 |
| shelf_02 | 5.25 | 5.77 | 5.25 | 15.00 |
| shelf_03 | 9.95 | 10.48 | 9.95 | 1.36 |
| shelf_04 | 7.55 | 8.68 | 7.55 | 15.00 |
| shelf_05 | 5.35 | 6.57 | 5.35 | 15.00 |
| shelf_06 | 5.50 | 6.55 | 5.50 | 15.00 |
| cave_mouth | 4.10 | 6.45 | 4.10 | 1.77 |

Stills: `route_topdown.png` (straight down, north up) and `route_play.png` (v1's play camera) -- the magenta line is the knight's DRIVEN track (a check overlay, not in the guide); him on the stair for scale.

Where it stands: R-C9-226: cave W, stair E as sketch A draws them -- the cave in the back wall of a 5.0 m sea-cut cove at u -4.3, the iced landing at its mouth, the stair cut from the cove's back-right corner climbing INLAND (up-screen) between rock columns to the clifftop at u 8.6
