# Sea-cave route -- walkability (R-C9-188/189)

Against the art level's **colliders** (terrain HeightMapShape3D, the stair's nosing ramp, the cave hood, the bounds), by `barrow_full/godot/tools/bv2f/walk_check.gd`, driven by `fid/lv/tools/lv_walkability.py`.

**v1's character step height:** `scripts/knight.gd` is a CharacterBody3D capsule r 0.35 m, h 1.85 m, on plain `move_and_slide()` with 18 m/s2 gravity and no step-up code; floor_max_angle 45 deg (Godot's default, not set): an edge is mounted only while the contact normal is within that of up, so **step height = r (1 - cos 45 deg) = 0.103 m** (read off the running node).

| bar | measured | |
|---|---|---|
| continuous walk surface, cave -> clifftop (every 0.05 m) | 539 of 539 centreline samples walkable; 0 breaks | PASS |
| stair slope <= 35 deg | 33.34 deg (collider); treads 33.34 deg | PASS |
| iced landing (cut in the cove) slope <= 10 deg | 0.00 deg | PASS |
| no riser above v1's step height (0.103 m) | max 0.033 m between samples 0.05 m apart (treads' visual riser 0.250 m is under the ramp) | PASS |
| stair clear width >= 5 m | min 5.25 m over 17 sections | PASS |
| iced landing clear depth >= 5 m (cave mouth -> stair foot) | min 5.60 m over 5 sections | PASS |
| cave mouth clear height ~7 m | 7.18 m at the arch's lip (the first centreline sample under the roof); 5.13 m deeper in; the floor 5.35 m clear across 1 m inside | PASS |
| v1's knight driven from inside the cave to the clifftop | reached True in 18.1 s (1086 frames, 0 off the floor); ends at uv (8.12, -9.95) z 2.50 | PASS |

**Verdict: PASS**

| segment | samples | walkable | max slope | max dz / 0.05 m | z range | min headroom |
|---|---|---|---|---|---|---|
| cave | 61 | 61 | 0.00 deg | 0.000 m | -3.50 .. -3.50 | 5.13 m |
| shelf | 172 | 172 | 0.00 deg | 0.019 m | -3.50 .. -3.50 | 15.00 m |
| stair | 184 | 184 | 33.34 deg | 0.033 m | -3.48 .. 2.50 | 15.00 m |
| landing | 85 | 85 | 0.00 deg | 0.000 m | 2.50 .. 2.50 | 15.00 m |
| clifftop | 37 | 37 | 0.00 deg | 0.000 m | 2.50 .. 2.50 | 15.00 m |

Sections (clear width = walkable run across, capped by the free run to the nearest collider at 0.4 m and 1.2 m):

| section | surface | free between colliders | clear | headroom |
|---|---|---|---|---|
| stair_00 | 5.30 | 6.13 | 5.30 | 15.00 |
| stair_01 | 5.30 | 6.05 | 5.30 | 15.00 |
| stair_02 | 5.30 | 6.04 | 5.30 | 15.00 |
| stair_03 | 5.30 | 6.08 | 5.30 | 15.00 |
| stair_04 | 5.30 | 6.45 | 5.30 | 15.00 |
| stair_05 | 5.30 | 6.21 | 5.30 | 15.00 |
| stair_06 | 5.25 | 6.02 | 5.25 | 15.00 |
| stair_07 | 5.30 | 6.14 | 5.30 | 15.00 |
| stair_08 | 5.25 | 5.80 | 5.25 | 15.00 |
| stair_09 | 5.25 | 6.33 | 5.25 | 15.00 |
| stair_10 | 5.30 | 6.04 | 5.30 | 15.00 |
| stair_11 | 5.40 | 6.19 | 5.40 | 15.00 |
| stair_12 | 5.30 | 6.05 | 5.30 | 15.00 |
| stair_13 | 5.30 | 6.02 | 5.30 | 15.00 |
| stair_14 | 5.30 | 6.11 | 5.30 | 15.00 |
| stair_15 | 5.35 | 6.25 | 5.35 | 15.00 |
| stair_16 | 5.30 | 6.65 | 5.30 | 15.00 |
| shelf_00 | 5.60 | 6.42 | 5.60 | 4.04 |
| shelf_01 | 6.20 | 6.45 | 6.20 | 2.15 |
| shelf_02 | 6.00 | 6.03 | 6.00 | 1.33 |
| shelf_03 | 6.40 | 6.55 | 6.40 | 1.72 |
| shelf_04 | 6.05 | 6.54 | 6.05 | 4.75 |
| cave_mouth | 5.35 | 5.45 | 5.35 | 1.97 |

Stills: `route_topdown.png` (straight down, north up) and `route_play.png` (v1's play camera) -- the magenta line is the knight's DRIVEN track (a check overlay, not in the guide); him on the stair for scale.

Where it stands: cave W, stair E as sketch A draws them: the cave under the lip at u -9.5, the stair climbing east across the face to the clifftop at u 4.8
