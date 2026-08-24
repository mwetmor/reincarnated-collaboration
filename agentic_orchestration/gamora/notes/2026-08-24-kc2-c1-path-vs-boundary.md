# KC2 MODEL-COMPLETION RUN — C-1 · path-vs-boundary check

**Date:** 2026-08-24
**Author:** gamora (simulation seam)
**Status:** CURRENT — findings of record for Wave 1 cell C-1
**Authority:** gandalf RUN-CONDUCTOR, charter `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` § Wave 1, cell C-1
**Mode:** READ-ONLY analysis. No sim code changed. No checkpoint written. No AGENT_STATE write. Analysis script lived in `/tmp/kc2c1/` and is not part of the engine tree.

---

## 0 · VERDICT

> **APPROACHES — at `path[0]`, on every salt, by exact structural bound. Does NOT cross.**
>
> **No actor path point, player or monster, lies outside the rectangle under either anchoring.** The player is **19.86 m** (anchor A) / **21.68 m** (anchor B) clear of the nearest edge at its worst and never exceeds **22.22 m** from the arena centroid.
>
> **The monsters' closest approach is made at tick 0, at spawn, not in motion** — **3.05 m** (A) / **1.79 m** (B), i.e. **inside one sweep radius (`config.kit.radius_m` = 3.000 m)** of the boundary. Post-spawn, once bodies start walking, the minimum relaxes to 3.35 m (A) / 1.97 m (B) and thereafter monotonically inward: 86 of 97 actors never exceed their own spawn radius at any tick.
>
> **PROVABLY-INERT is NOT earnable from this record**, for three independent reasons stated in § 4: (a) 4 of 5 salts carry no coordinates at all; (b) the rectangle is not a decode — it is a *self-derived hull of a sibling run's own paths plus a 3.0 m margin*, so the test has almost no falsifying power; (c) an analytic reachability route to crossing exists through the `DRIVE_TO_PACK` pass-through lock and is not closed by any invariant in the code.

The conductor makes the "approaches" judgment call. The measurements are below. My read, offered as a read and not as the finding: **the headline is not the distance table — it is caveat C-1.a. The boundary this cell was asked to test paths against is not the arena's boundary. It is a bounding box drawn around the paths.**

---

## 1 · Provenance and the anchoring convention — VERIFIED, not assumed

### 1.1 Checkpoint identity

| item | value |
|---|---|
| file | `reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` |
| sha256 recomputed | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` |
| brief's pin | `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` |
| **match** | ✅ **BYTE-IDENTICAL. D5 law honoured: read only, parent and sibling untouched.** |

`identity.run_id = E-s09-cp150-mech`, `identity.sibling_of = E-s09-cp150`. `parent_immutability.frozen_pre = 20/20`, `frozen_post = 20/20`.

### 1.2 The sim's coordinate frame — READ, not assumed

`locomotion.py:300–309`, the `CitedArenaGeometry` docstring, declares the frame verbatim:

> ⚑ REFERENCE FRAME IS THE `PatrolPoint_Attack` CENTROID, NOT `playerspawnpoint` (§ 10.6 motion hook). […]
> ⚑ PLANE CONVENTION, DECLARED: the level's (x, z) horizontal pair maps to the sim's (x, y); `y_level` is the VERTICAL axis and is not modelled (open-plane, M-10 unchanged).

So **sim `(0, 0)` is the `PatrolPoint_Attack` centroid**, and `emitter_xy()` subtracts `centroid_xz` to produce every position in that frame. This is the same origin `player_drive.py` measures `PLAYER_SANE_BOUND_M` against (`math.hypot(px, py)`, `_finish()`).

The arena of record for the s2 band (waves 151–160, content tier 16) is `sm1/survivalworld_a.map`, per `locomotion.ARENA_SELECTION['s2']`. Centroid `(81.26, 64.361)` in level coordinates.

### 1.3 Where the rectangle comes from — and it is NOT a decode

The brief calls it "the decoded real arena." **It is not decoded.** Traced to source, `drax/notes/2026-08-12-sb1-a1b-statics-landing.md:62`:

> floor footprint | **86.915 × 85.303 m**, one `PlaneMesh` | the MEASURED occupied region (80.915 × 79.303 m over 5,085 positions: every knot, every spawn, the player track, the sweep track, all six anchors) grown by **one sweep radius, 3.000 m = `config.kit.radius_m`**, read from the wire

and the anchoring, `…:299–301`:

> **The floor footprint is GL-13's clip surface** and it is 86.915 × 85.303 m, centred at sim `(-1.819, 0.244)` — **not** at the origin. Telegraph FX clipping must use the measured rectangle, not a symmetric assumption about the arena centre.

Arithmetic checks: 80.915 + 2(3.000) = 86.915 ✅ · 79.303 + 2(3.000) = 85.303 ✅.

The rectangle is therefore **the AABB of the PARENT baton's own occupancy, inflated by one sweep radius.** The real arena extent is `UNREACHED-S8` — the `.lvl` has never been opened. `run.py:3566–3569` says so in the code itself:

> ⚑ IT COUNTS AND IT DOES NOT RAISE. Adding a raise on the board would convert a NAMED model gap (`D-PDEF-2` — monster containment is unmodellable without decoded arena walls, `UNREACHED-S8`) into an artificial terminal.

And legolas `pm4s_findings.md` § 3.3 retracted its own bound-direction claim (`D-S-1`), grading the video-derived hull **INDICATIVE**, and closed with: *"The video measures the fight's footprint; the world assets measure the arena. They are different quantities and this lap keeps them apart."*

### 1.4 Anchoring — BOTH interpretations computed

Because the anchoring is exactly the thing the brief told me not to assume, both are carried through every table.

| id | interpretation | rectangle (sim frame) |
|---|---|---|
| **A** | drax's measured centre `(-1.819, 0.244)` — the GL-13 clip surface as built | x ∈ [−45.2765, +41.6385], y ∈ [−42.4075, +42.8955] |
| **B** | naive origin-centred `(0, 0)` — the "symmetric assumption" drax explicitly warns against | x ∈ [−43.4575, +43.4575], y ∈ [−42.6515, +42.6515] |

**B is the harsher test on the −x side** (the p01 emitter side) and is the one that produces every worst number in this note. Neither produces a crossing.

---

## 2 · What the frozen record actually contains — the coverage gap, stated first

| salt | player path length (m) | coordinates in the frozen artifact? |
|---|---:|---|
| salt0 | 529.843 | ✅ **YES** — `salt0_player_track` (5 waves, 917 samples) + `salt0_knots` (97 actors, 10,036 knots) |
| salt1 | 664.429 | ❌ NO |
| salt2 | 196.330 | ❌ NO |
| salt3 | 39.276 | ❌ NO |
| salt4 | 109.774 | ❌ NO |

Salts 1–4 carry `player_path_length_m`, `n_distinct_player_positions`, `exit_partition`, `re_entries`, `state_census`, `lag_census_per_wave` — **and no positions.** The findings of record (`kc2-mech-wave-findings-20260816_162815.json`, `legs.L1.*`) carry no positions either; a scan for `max_abs_offset`, `sane_bound`, `offset_m`, `max_body_offset` returns **0 hits**.

**I did not re-execute the sim to fill this gap.** The remit is read-only, and re-running to obtain salts 1–4 would produce fresh artifacts whose relation to the frozen sibling is exactly the thing D5 exists to protect. Instead § 3.3 substitutes an **exact, salt-independent** bound for the spawn population, which covers all five salts by construction, and § 4.b states plainly what remains unmeasured.

---

## 3 · The measurements

### 3.1 Min-distance table — salt0, the deliverable

Distance is signed perpendicular distance to the **nearest** of the four edges; positive = inside.

| anchor | actor class | n points | **MIN dist to nearest edge** | points OUTSIDE | **max excursion from rect centre** | worst point (x, y) |
|---|---|---:|---:|---:|---:|---|
| **A** `(-1.819, 0.244)` | player | 917 | **19.8647 m** | **0** | 24.0490 m | (21.774, −4.418) |
| **A** | monsters (aggregate) | 10,036 | **3.0526 m** | **0** | 41.7788 m | (38.586, 5.071) |
| **A** | monsters, POST-spawn only | 9,939 | 3.3526 m | 0 | — | — |
| **B** `(0, 0)` | player | 917 | **21.6837 m** | **0** | 22.2174 m | (21.774, −4.418) |
| **B** | monsters (aggregate) | 10,036 | **1.7913 m** | **0** | 43.5882 m | (−41.666, 12.801) |
| **B** | monsters, POST-spawn only | 9,939 | 1.9661 m | 0 | — | — |

Raw occupancy AABB of the whole salt0 board (monsters + player): x ∈ [−41.6662, 38.5859] (span 80.2521), y ∈ [−36.4264, 38.8483] (span 75.2746), centred at (−1.5402, 1.2110).
Player-only AABB: x ∈ [−13.3714, 21.7738], y ∈ [−11.8020, 15.3300], max |r| from origin **22.2174 m**.
Monster-only max |r| from origin **43.5882 m** — and that point *is* a spawn.

### 3.2 The mechanism: the extremum is the spawn, and motion is inward

The monster minimum and the spawn minimum are **the same number to all four decimals** under both anchorings (3.0526 / 1.7913). The closest any monster ever gets to the boundary is the instant it appears.

| statistic | value |
|---|---|
| actors whose path max |r| exceeds their own spawn |r| | **11 / 97** |
| largest such outward excursion | +9.162 m (`w151_a027`, spawn |r| 1.962 → path max |r| 11.124) |
| all 11 outward-movers | inner-emitter (p05, |r| ≈ 7 m) bodies; **max |r| reached by any of them = 11.12 m** — 30+ m clear of every edge |
| paths straight, no bend | 0 / 97 (`paths_with_a_bend` = 97) |
| `clip` knots / `unclip` knots | 172 / 0 |

The outward movers are all interior bodies drifting out from the p05 ambush point toward the patrol ring. **No body that spawns near the perimeter moves further out.** That is `F-6` from legolas's Lap S showing up in the sim's own knots: *movement policy of spawned packs = converge on `PatrolPoint_Attack` group, NOT per-body player-seek.*

### 3.3 Spawn → boundary, and the salt-independent bound covering all five salts

Spawn positions are not free. They are drawn as `POLAR_UNIFORM_RHO` scatter of radius `spawn_structure.PLACEMENT_EXTENTS_M = 8.0 m` about **fixed** emitter placements read from the cited arena. The salt selects the draw inside the disc; it cannot move the disc. So the worst-case spawn over **all salts, all seeds, forever** is the worst point of each disc.

Emitters for the s2 band, `sm1/survivalworld_a.map`, centroid frame, tier 16:

| emitter | centre (x, y) | \|r\| | **worst-case dist to edge over the WHOLE 8.0 m disc, anchor A** | **anchor B** |
|---|---|---:|---:|---:|
| p01 (tier16) | (−34.447, 9.594) | 35.758 | +2.8295 m | **+1.0105 m** ← global worst |
| p02 | (9.343, −31.463) | 32.821 | +2.9445 m | +3.1885 m |
| p03 | (8.125, 32.368) | 33.372 | **+2.5275 m** | +2.2835 m |
| p04 | (30.905, 7.147) | 31.721 | +2.7335 m | +4.5525 m |
| p05 | (−6.821, 2.175) | 7.159 | +30.4555 m | +28.6365 m |
| p06 — **RULED OFF** (`D-W1` rider / `L-37(b)` / `F-10`) | (31.215, 6.805) | 31.948 | **+2.4235 m** | +4.2425 m |

> **⚑ EXACT, SALT-INDEPENDENT RESULT.** Every spawn on every salt lies inside the rectangle under both anchorings, with worst-case clearance **+2.4235 m** (anchor A, counting the ruled-off p06) / **+2.5275 m** (anchor A, p06 off) / **+1.0105 m** (anchor B). **No spawn can cross. And no spawn can be more than one sweep radius clear of the wall on the p01/p03/p04/p06 sides.**

Measured salt0 spawn distribution, anchor A:

| emitter | n | min dist to edge | median |
|---|---:|---:|---:|
| p01 | 20 | 3.6103 m | 11.7855 m |
| p02 | 11 | 5.9811 m | 11.5457 m |
| p03 | 26 | 4.0472 m | 11.7135 m |
| p04 | 28 | **3.0526 m** | 10.2725 m |
| p05 | 12 | 32.5570 m | 38.4261 m |

Five closest salt0 spawns, anchor A: `w155_a010` p04 (38.586, 5.071) 3.0526 m · `w154_a000` p01 (−41.666, 12.801) 3.6103 m · `w151_a005` p01 (−41.251, 8.579) 4.0254 m · `w151_a012` p03 (9.434, 38.848) 4.0472 m · `w153_a013` p03 (10.018, 38.288) 4.6078 m.

Proximity histogram (anchor A / anchor B):

| within … of edge | spawns (/97) | all monster knots (/10,036) | post-spawn knots (/9,939) |
|---|---|---|---|
| 3 m | 0 / 2 | 0 / 13 | 0 / 11 |
| 5 m | 5 / 7 | 27 / 54 | 22 / 47 |
| 10 m | 33 / 30 | 411 / 418 | 378 / 388 |
| 15 m | 75 / 76 | 1,643 / 1,596 | 1,568 / 1,520 |

The audit's *"worst spawn→player ≲ 76 m"* is consistent and is a *player-relative* number: with the player living at |r| ≤ 22.22 m and spawns out at |r| ≤ 43.76 m, near-antipodal spawn/player pairs reach ~66 m; the 76 m figure sits inside the reachable envelope and implies nothing about the boundary.

### 3.4 The player: why 22 m and not 43 m

The player's containment is not luck, and it is not an invariant either — it is the patrol-node geometry.

| quantity | value |
|---|---|
| max \|r\| of any `PatrolPoint_Attack` node (11 nodes) | **24.522 m** |
| salt0 measured player max \|r\| | **22.2174 m** |
| `PLAYER_SANE_BOUND_M` (raises) | 80.0 m |
| `PASS_THROUGH_LOCK_M` = `EOR_RADIUS_M` | 3.0 m |
| salt1 max player→target lag across waves 151–156 | 12.00 – 17.74 m (`lag_census_per_wave`) |

Packs converge on the node set; `DRIVE_TO_PACK` drives to the pack, so the player lives in the node region. The measured 22.22 m sits neatly under the 24.52 m outer node. **This is a mechanism, and it is the reason I am willing to extend the player verdict to salts 1–4 as a strong expectation — but it is an expectation, not a measurement.**

---

## 4 · Why PROVABLY-INERT is not earnable — three caveats, named

### C-1.a — ⚑ THE ANCHORING/PROVENANCE CAVEAT (the load-bearing one)

**The rectangle is not a decode of the arena. It is a bounding box drawn around a sibling run's own paths, plus 3.0 m.**

Consequence: this check is **very close to tautological**. The 3.0526 m measured minimum under anchor A is 3.000 m of *construction margin* plus 0.0526 m of signal. The only reason there is any slack at all is that the mech sibling's occupancy (x-span 80.2521 m) happens to be marginally tighter than the parent's (80.915 m) — i.e. the slack measures the *difference between two runs*, not a distance to a wall.

**A test whose boundary is defined as a superset of the thing being tested cannot fail.** The finding under the finding is: *there is no decoded boundary to test against.* `D-PDEF-2` is open, `UNREACHED-S8` stands, the `.lvl` is unopened, and `run.py` already declares monster containment an honest model gap rather than dressing it as a difficulty signal.

### C-1.b — the coverage caveat

4 of the 5 requested cells carry no coordinates (§ 2). The spawn population is covered for all five salts by the exact bound in § 3.3. The **player and monster path populations for salts 1–4 are UNMEASURED.** The only hard invariant that touches them is `PLAYER_SANE_BOUND_M = 80.0 m`, which is **1.84×** the rectangle's half-extent — it constrains nothing about containment. `player_drive.py:88–92` says as much in its own comment: *"80 m sits well above 45.06 + 3.0 + one step and well below 125 — so a firing bound means the POLICY ran away, not that the bound was tight."*

### C-1.c — the reachability caveat: crossing is not closed by any invariant

Two live routes out of the rectangle exist in the current code. Neither fired on salt0. Neither is prevented.

1. **The pass-through lock.** `DRIVE_TO_PACK` carries the player up to `PASS_THROUGH_LOCK_M = 3.0 m` past a target centroid before homing resumes. A pack reduced to one body sitting at the far lip of the p01 disc has centroid |r| = 43.758 m; the lock would carry the player to |r| ≈ 46.76 m — **outside under both anchorings** (anchor A p01-side edge x = −45.2765 vs a reachable x ≈ −45.45; anchor B, outside by ~2.0 m). Not observed — salt0's player topped out at 22.22 m because packs converge inward before dying — but nothing in the code forbids it.

2. **The neighbouring record already contains the counterexample.** `run.py:3568–3570`, verbatim:

   > on 6 of 8 I-19 arms the BOARD left the 45.06 m envelope (14–71 bodies per arm WALKED there) while `PLAYER_SANE_BOUND_M` watched only the player, and `D-I19-7`'s wave-154 terminal MISATTRIBUTED as a result.

   Different limb and different wave — but the same board and the same locomotion. **The sim demonstrably can put dozens of bodies past 80 m from the centroid, i.e. ~1.8× outside this rectangle.** The `D-PDEF-3` census counts it and deliberately does not raise, precisely because there are no decoded walls to contain against.

---

## 5 · What C-1 hands to the conductor

| # | statement | grade |
|---|---|---|
| 1 | No salt0 actor path point, player or monster, lies outside the rectangle under either anchoring. | **MEASURED** |
| 2 | salt0 player: min 19.86 m (A) / 21.68 m (B) clear; max |r| 22.22 m — ~half the half-extent. | **MEASURED** |
| 3 | salt0 monsters: min 3.05 m (A) / 1.79 m (B), **attained at `path[0]`**; post-spawn min 3.35 m / 1.97 m. | **MEASURED** |
| 4 | Every spawn on **every** salt is inside, worst-case clearance 2.42 m (A) / 1.01 m (B) — i.e. **within one sweep radius of the wall on four of five emitter sides**. | **EXACT, SALT-INDEPENDENT** |
| 5 | Motion is inward: 86/97 actors never exceed their spawn radius; the 11 that do are inner bodies capping at |r| = 11.12 m. | **MEASURED** |
| 6 | The player stays in the patrol-node region (max node |r| = 24.522 m) because packs converge there. | **MECHANISM, measured on 1 salt** |
| 7 | Player and monster paths on salts 1–4. | **UNMEASURED — not in the frozen record** |
| 8 | The rectangle is a self-derived occupancy hull + 3.0 m, not a decoded wall; `D-PDEF-2` / `UNREACHED-S8` open. | **PROVENANCE FACT** |
| 9 | The pass-through lock admits an unprevented route to |r| ≈ 46.76 m; the I-19 arms already put 14–71 bodies past 80 m. | **CODE-READ + RECORD-READ** |

**Facet (h) input, stated as measurement rather than as a recommendation:** nothing in the record shows a path crossing this rectangle, and the player is nowhere near it. What the record shows instead is that **bodies enter the world within one sweep radius of where the wall would be**, on every salt, by construction — and that the sim has no wall to enter *through*. Whether that makes B-7 walls-in-sim non-negotiable turns on rows 4, 8 and 9, not on row 1.

---

## 6 · Method

- All arithmetic in `/tmp/kc2c1/{c1,c2,c3}.py` (throwaway, outside the engine tree, not committed).
- Checkpoint read via `json.load`; sha256 recomputed from bytes before use.
- Emitter geometry obtained by importing `reincarnated.simulation.kc2.locomotion` / `.spawn_structure` read-only and calling `load_arena_geometry('survivalworld_a.map', 'sm1')`. No module was modified.
- Distance metric: signed perpendicular distance to the nearest of four axis-aligned edges. "Excursion" is Euclidean distance from the rectangle's own centre (so it differs between anchors A and B for the same point set — both reported).
- Disciplines: **#11 empirical inspection over assumption** (the anchoring was traced to `drax/notes/2026-08-12-sb1-a1b-statics-landing.md:62,299` and the frame to `locomotion.py:300–309` rather than assumed); **#4 right tool** (an exact structural bound replaced an unavailable measurement for salts 1–4 rather than a re-run); **#10 attribution** (the rectangle's derived provenance is stated before its numbers are used). No Discipline #1 math note is owed — no balance constant, formula, threshold or gate logic was changed.
- No MIGRATION.md owed: no schema touched, no field added or renamed, no telemetry write.
