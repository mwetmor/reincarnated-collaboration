# Sea-cave route -- walkability (R-C9-188/189)

Against the art level's **colliders** (terrain HeightMapShape3D, the stair's nosing ramp, the cave hood, the bounds), by `barrow_full/godot/tools/bv2f/walk_check.gd`, driven by `fid/lv/tools/lv_walkability.py`.

**v1's character step height:** `scripts/knight.gd` is a CharacterBody3D capsule r 0.35 m, h 1.85 m, on plain `move_and_slide()` with 18 m/s2 gravity and no step-up code; floor_max_angle 45 deg (Godot's default, not set): an edge is mounted only while the contact normal is within that of up, so **step height = r (1 - cos 45 deg) = 0.103 m** (read off the running node).

| bar | measured | |
|---|---|---|
| continuous walk surface, cave -> clifftop (every 0.05 m) | 404 of 404 centreline samples walkable; 0 breaks | PASS |
| stair slope <= 35 deg | 32.66 deg (collider); treads 32.66 deg | PASS |
| iced landing (in the cove) slope <= 10 deg | 0.00 deg | PASS |
| no riser above v1's step height (0.103 m) | max 0.032 m between samples 0.05 m apart (treads' visual riser 0.250 m is under the ramp) | PASS |
| stair clear width >= 5 m | min 5.15 m over 12 sections | PASS |
| iced landing clear width >= 5 m (cave mouth -> past the jamb -> stair foot) | min 5.60 m over 7 sections | PASS |
| cave mouth clear height ~7 m | 7.10 m at the arch's lip (the first centreline sample under the roof); 4.74 m deeper in; the floor 8.35 m clear across 1 m inside | PASS |
| v1's knight driven from inside the cave to the clifftop | reached True in 12.7 s (761 frames, 0 off the floor); ends at uv (9.30, -2.54) z 0.74 | PASS |

**Verdict: PASS**

| segment | samples | walkable | max slope | max dz / 0.05 m | z range | min headroom |
|---|---|---|---|---|---|---|
| cave | 40 | 40 | 0.00 deg | 0.000 m | -3.50 .. -3.50 | 4.74 m |
| shelf | 140 | 140 | 0.00 deg | 0.000 m | -3.50 .. -3.50 | 7.13 m |
| stair | 136 | 136 | 32.66 deg | 0.032 m | -3.50 .. 0.75 | 15.00 m |
| landing | 37 | 37 | 0.00 deg | 0.000 m | 0.75 .. 0.75 | 15.00 m |
| clifftop | 51 | 51 | 4.24 deg | 0.004 m | 0.72 .. 0.75 | 15.00 m |

Sections (clear width = walkable run across, capped by the free run to the nearest collider at 0.4 m and 1.2 m):

| section | surface | free between colliders | clear | headroom |
|---|---|---|---|---|
| stair_00 | 5.20 | 5.45 | 5.20 | 15.00 |
| stair_01 | 5.15 | 5.43 | 5.15 | 15.00 |
| stair_02 | 5.20 | 5.35 | 5.20 | 3.94 |
| stair_03 | 5.15 | 5.22 | 5.15 | 15.00 |
| stair_04 | 5.15 | 5.23 | 5.15 | 15.00 |
| stair_05 | 5.20 | 5.53 | 5.20 | 15.00 |
| stair_06 | 5.15 | 5.28 | 5.15 | 15.00 |
| stair_07 | 5.30 | 5.85 | 5.30 | 15.00 |
| stair_08 | 5.30 | 5.64 | 5.30 | 15.00 |
| stair_09 | 5.25 | 5.62 | 5.25 | 15.00 |
| stair_10 | 5.20 | 5.61 | 5.20 | 15.00 |
| stair_11 | 5.35 | 6.60 | 5.35 | 15.00 |
| shelf_00 | 6.50 | 7.53 | 6.50 | 15.00 |
| shelf_01 | 6.70 | 7.77 | 6.70 | 15.00 |
| shelf_02 | 5.65 | 6.14 | 5.65 | 1.62 |
| shelf_03 | 6.25 | 6.50 | 6.25 | 2.85 |
| shelf_04 | 6.25 | 7.33 | 6.25 | 15.00 |
| shelf_05 | 6.55 | 7.57 | 6.55 | 15.00 |
| shelf_06 | 5.60 | 6.55 | 5.60 | 15.00 |
| cave_mouth | 8.35 | 9.87 | 8.35 | 2.40 |

Stills: `route_topdown.png` (straight down, north up) and `route_play.png` (v1's play camera) -- the magenta line is the knight's DRIVEN track (a check overlay, not in the guide); him on the stair for scale.

Where it stands: R-C9-228: cave W, stair E as sketch A draws them -- no cove: the cave an arch worn into the face at the waterline (u -2.0), facing the camera; the stair in a natural gully of the cliff beside it, climbing INLAND (up-screen) between rock columns to the clifftop at u 7.2; a small iced ledge where its foot meets the mouth
