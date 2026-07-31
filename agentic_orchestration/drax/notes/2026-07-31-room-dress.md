# ROOM-DRESS — the rooms are old now, and the fight envelope was measured before a single stone was placed

> **Cell:** ROOM-DRESS (BR-1 BATON-RENDER §3 cell #6) — per-room disrepair + doorway dirt-bleed on the
> four-room crypt, under a hard fight-clearance law and under the EXISTING light.
> **Agent:** drax (presentation seam). **Conductor:** gandalf (`RUN-CONDUCTOR`). **Gates:** D-1 … D-4.
> **Date:** 2026-07-31.
> **Contract of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` (Scopes 1–23 + the five
> landings; **the five-item lighting brightness decision is OPEN at Matt's eye and this cell moved no
> lighting constant**) · `gandalf/notes/2026-07-31-baton-render-run-charter.md` (§3 cell 6, R-BR-6).
> **Substrate:** `kitcal_g5/wr2_battery_after/g5_m4cadence_nova_mitR2proxy_tg_dec_bsep_mv2_ntv2`
> (R-BR-6 re-pin), engine `f1ab3b09`, **opened READ-ONLY**; fixture seed **74000806** boss/arm A.
> **Inherited:** godot `30f83fc` LOCAL (ahead 14). **Shipped:** godot `78043af` LOCAL, ahead 15, **NOT pushed**.
> **Files touched:** `scripts/wr1_dressing.gd` (new) · `scripts/wr1_dress_envelope.gd` (new) ·
> `scripts/kit_replica_level.gd` (+3 accessors) · `scripts/wr1_level.gd` · `scripts/wr2_playback.gd`.

---

## §0 — The cell in six sentences

**The clearance law is a measurement, not a habit of leaving room:** the region the fight actually
sweeps was computed off the frozen traces as the union of capsules dragged along every alive actor's
own path — over the WHOLE tier battery, 60 boss traces and both policy arms, not just the fixture —
frozen into a 75 × 75 grid per room, and every one of the 534 placed props was tested against it with
its own AABB-measured footprint radius before it was allowed to exist. **The minimum distance from any
prop to the fight is 2.286 m** against the battery and **2.286 m against the fixture**, the same prop;
zero props are inside the envelope and zero are below the 2.00 m margin. **The 12 m telegraph ring got
its own clause and its own arithmetic**: a prop hides 0.7548 m of floor per metre of its own height
along the one ground bearing that points away from CAM-LOCK, so the test is a directional occlusion
capsule rather than a symmetric no-go band — 0 footprints and 0 occlusion strips enter the disc,
minimum 0.528 m. **No lighting constant moved and the measurements prove it**: LSTAT-2 is
byte-identical (`5d4fa240cb0ead2c…`, 0 px of 921,600), the cold pool footprint reads 1.000023× of its
clean value, and the beam's share of that footprint is 8.470 % in BOTH arms to three decimals.
**The four rooms are four different places by count AND by character** — 131 small pieces / 97 broad
flat drifts / 65 tall silhouettes / 172 on the boss stage, and 4.41 % / 8.41 % / 4.68 % / 14.03 % of
frame at the same pose. **⚑ AND THE FINDING THE CELL EXISTS TO REPORT: the dressing has almost no
tonal separation from the floor it sits on — prop-to-floor contrast is 1.0262× at the same pixels —**
so under today's faint shadow the dressing reads by silhouette and texture only; it is the direct
beneficiary of Matt's open shadow-depth item, and I did not touch a lighting constant to compensate.

---

## §1 — WHERE THE CLEARANCE LAW CAME FROM

### 1.1 The envelope is a swept path, not a bounding box

The player's bounding box on the fixture is x [17.62 … 35.50], y [4.03 … 28.63] and the boss's is
x [23.62 … 34.50], y [9.11 … 28.00]. Taken as a rectangle that is 22.5 × 24.6 m of a 36 × 36 m arena —
two thirds of the room forbidden for a fight that is really a pair of curves through it. So the
envelope is the **union of swept capsules**: each actor's own `entity_radius_m` (player 0.50 m, boss
1.50 m, escorts 0.50 m) dragged along its own tick-to-tick segment, unioned over every alive actor and
every trace.

| grid | traces | room floor clear at ≥ 2.0 m |
|---|---:|---:|
| `trash` | 30 | 76.2 % |
| `champion` | 30 | 85.0 % |
| `mixed_pack` | 30 | 71.3 % |
| **`boss`** | **60** (both arms) | **47.4 %** |

**The union is taken over the WHOLE battery, not over the fixture, and that is a deliberate cost.**
R-BR-4 lets the conductor pick any of the 30 seeds for the LAP-1 WATCH; a dressing laid out against
one seed would be a dressing that fails the moment the pick changes. The fixture is a subset of the
boss grid by construction, which is why the two minima in §2 are the same number.

### 1.2 It is frozen data, and the grid places while the continuous field grades

The level builder must not open a trace — it builds for every harness in the tree, most of which have
no trace at all. So `tmp/roomdress/measure/bake_mask.py` measures once, offline, at 0.10 m, then
min-pools to 0.50 m cells and writes `scripts/wr1_dress_envelope.gd`. **Storing the MINIMUM over each
cell is what makes the in-engine test conservative rather than approximate**: a disc covered by cells
whose stored minima are all ≥ M has true clearance ≥ M. A cell average would not have that property.

After the render, `tmp/roomdress/measure/verify.py` **re-grades every placed prop against the
CONTINUOUS path** — exact point-to-segment distance to every capsule of every trace at full precision.
The grid places; the continuous field is what the gate is scored on.

### 1.3 The telegraph ring, and why the test is directional

Censused rather than assumed (`measure/telegraph_census.json`): the leg contains **exactly ONE circle
telegraph**, fired 44 times across both arms, always the same event — origin (26.158596, 15.416323),
`radius_m` 12.0. Frozen into the same file.

**A prop hides the floor BEHIND it, never in front, and "behind" at a fixed camera is one fixed ground
bearing.** At CAM-LOCK (pitch 52.9535°, yaw 47°) a prop of height h hides `h / tan(pitch)` = **0.7548 h
metres** of floor along the bearing pointing away from the camera. The test is therefore that capsule
against the disc. The simpler alternative — ring + a symmetric 1.96 m band (the worst case for a 2.6 m
prop) — would have forbidden roughly a third of the boss room **for a 4 cm dirt patch that hides
nothing**, and it would have been forbidding it for a reason that is not true.

---

## §2 — GATES, tolerances named first, then the numbers

| gate | tolerance, named before the shipped render |
|---|---|
| **D-1a** envelope | **0 props inside the swept envelope**, and **min clearance ≥ 2.00 m** measured against the CONTINUOUS path. 2.00 m = one boss radius (1.50) + half a player (0.25) + slop, so the fight cannot brush a prop even on a frame the trace does not contain. |
| **D-1b** ring | **0 props whose footprint OR CAM-LOCK occlusion strip enters the 12.0 m disc**, min ≥ **0.50 m**. Lower than D-1a on purpose: the ring is DRAWN, not walked — this is a legibility constraint on a decal, not a traversal constraint on a body. |
| **D-2** distinguishability | four rooms differing on **both** axes that a viewer reads: prop COUNT and frame COVERAGE, no two rooms within 20 % of each other on the second; four-up plate delivered. |
| **D-3** no lighting drift | LSTAT-2 sha **unchanged**; staticity **0 px** of 921,600 on a dust-off arm; cold-pool footprint mean within **±1 %**; beam share of that footprint within **±0.5 pp** across the arms. |
| **D-4** performance | median frame render time at CAM-LOCK **≤ +25 %** vs the clean room, measured with the PNG capture off (the encode of a 720p frame costs more than the render, so a "frame time" with capture in it is a measurement of libpng). |

### D-1a — THE ENVELOPE · **PASS**

534 props placed, 225 rejected for envelope/fit, 15 more rejected for the ring; every rejection
**re-rolled, never nudged**.

| | |
|---|---:|
| margin demanded | **2.00 m** |
| **MIN clearance, prop → the whole tier battery** | **2.2857 m** |
| **MIN clearance, prop → the FIXTURE (74000806)** | **2.2857 m** (the same prop: `grave litter`, r 0.16 m, sim (20.13, 2.48)) |
| props INSIDE the envelope | **0** |
| props below the 2.00 m margin | **0** |

Per group of the population, continuous re-grade:

| | n | min | median | max |
|---|---:|---:|---:|---:|
| room 0 | 131 | 2.546 | 8.852 | 18.634 |
| room 1 | 97 | 2.533 | 10.416 | 22.331 |
| room 2 | 65 | 2.507 | 8.134 | 16.022 |
| **room 3 (the stage)** | **172** | **2.286** | 7.066 | 15.887 |
| doorway bleed, in-room half | 69 | 2.600 | 7.100 | 13.200 |

**Plate: `plates/PLATE_D1_clearance.png`** — four rooms, the swept envelope in red, envelope + 2 m in
yellow, and every single prop's footprint circle in green. It is the fastest read of this gate and it
is also the fastest read of what the law COSTS (see §5.1).

### D-1b — THE TELEGRAPH RING · **PASS**

| | |
|---|---:|
| boss-room props tested | 180 |
| props whose footprint enters the 12.0 m disc | **0** |
| props whose CAM-LOCK occlusion strip enters it | **0** |
| MIN clearance, occlusion strip counted as part of the prop | **0.5278 m** (`loose skulls`, r 0.23 m, h 0.36 m ⇒ reach 0.27 m) |
| occlusion reach per metre of prop height | 0.7548 m |

**⚑ THE FIRST BUILD FAILED THIS CLAUSE AND THE FAILURE IS WHY THE CLAUSE EXISTS AS CODE.** Before the
keep-out was written, **9 props lay inside the ring's floor disc** — all of them flat ground washes,
the worst 3.196 m inside it and 0.04 m tall. Nothing about them occludes anything, and the temptation
was to argue exactly that and move on. They were evicted instead, because TELL-DRESS T-3 measures the
rim against **the actual local floor at that pixel**, and a dirt patch under the ring changes that
denominator on a gate another cell already banked.

### D-2 — FOUR ROOMS, FOUR DRESSINGS · **PASS**

Measured at one pose per room (CAM-LOCK, lock target at each room's north-west quadrant), dressed
against clean, same frame, one variable:

| room | character | props | groups | mean h | max h | footprint area | **dressing px** | **% of frame** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **R0** trash · dark-fortress | the collapsed guardroom — MANY, SMALL | 131 | 8 | 0.26 m | 1.11 m | 388.8 m² | 82,296 | **4.41 %** |
| **R1** champion · dwarven-dungeon | the silted works — BROAD, FLAT | 97 | 7 | 0.18 m | 1.59 m | 713.0 m² | 156,713 | **8.41 %** |
| **R2** mixed_pack · dungeon-realms | the boneyard — FEW, TALL | 65 | 7 | **0.64 m** | **2.60 m** | 235.2 m² | 87,269 | **4.68 %** |
| **R3** boss · dark-fantasy | **the stage of the watch** — MOST, MOST VARIOUS | **172** | **11** | 0.45 m | 2.36 m | **869.6 m²** | **261,599** | **14.03 %** |

The two axes separate the two pairs that share a coverage figure: R0 and R2 are within 0.3 pp of each
other on frame coverage and are **not** confusable, because R0 carries **twice the pieces at 40 % of
the mean height** and R2 carries the only silhouettes in the level that reach 2.6 m. R0 additionally
owns the level's **only cobwebs** — polygon-dark-fortress is the only pack on disk that ships them,
which is exactly why they are R0's signature and not everyone's.

Per-room group manifests are in §3. **Plate: `plates/PLATE_D2_four_rooms.png`** (+ a gamma-lifted
inspection twin, because the crypt is genuinely dark and the claim has to be checkable by eye).

### D-3 — NO LIGHTING DRIFT · **PASS**, all four clauses

| clause | measurement |
|---|---|
| **LSTAT-2** | sha256 `5d4fa240cb0ead2c5cff9c288d686e22fce639f8713bc54cc6df6c99913b911d` — **byte-identical** to the value BEAM-CONE, SHADOW-UNIFY and TELL-DRESS banked. Pixel diff **0 of 921,600, max channel 0**. It is zero for a structural reason: the L7 stage builds `kit_replica_level.build_level()` directly, never the WR1 level, and `room_dress` defaults FALSE. |
| **staticity** | two separate process launches, dressing ON, dust + room-ambient peeled: **0 px of 921,600, max channel delta 0**. The 0-px bar TELL-DRESS/BEAM-FIX established is **unchanged**, and it survives because the dressing adds no `GPUParticles3D`, no tween and no animation — placement is a seeded `RandomNumberGenerator` off `LEVEL_SEED`, so the same room builds the same way every launch. |
| **cold floor pools** | footprint = blue-dominant bright pixels of the clean NOBEAM arm (66,344 px). Mean luma **91.5313 → 91.5334 = 1.000023×** (FULL) and **83.7784 → 83.7805 = 1.000025×** (NOBEAM). |
| **FULL / NOBEAM spot-check** | the beam mesh is genuinely present (peeling it moves **164,949 px**, mean \|Δ\| 2.51). Its share of the pool footprint is **8.470 % clean and 8.470 % dressed** — identical to three decimals. |

Declared delta, whole frame: mean luma **68.3538 → 68.3784 (+0.036 %)**. That is prop albedo replacing
floor albedo, not light — and it is *positive*, i.e. the dressing is very slightly brighter than the
stone it covers, which brings me to §5.2.

### D-4 — PERFORMANCE · **PASS**

Capture off, 150 rendered frames, CAM-LOCK, same lock target, same machine, back to back:

| | clean | dressed | Δ |
|---|---:|---:|---:|
| **median frame** | **7.918 ms** | **8.242 ms** | **+4.09 %** |
| p95 frame | 8.277 ms | 8.592 ms | +3.81 % |
| mean frame | 11.852 ms | 12.381 ms | +4.46 % |
| draw calls in frame | 323 | 543 | +68.1 % |
| primitives in frame | 85,498 | 278,465 | +226 % |
| objects in frame | 4,403 | 4,770 | +8.3 % |
| level build (one-off) | 3.83 s | 4.12 s | +7.6 % |

**+4.09 % against a named +25 % budget.** Worth saying why the draw-call figure is three times the
frame-time figure and is not alarming: 534 static opaque instances of small meshes are cheap next to
this scene's real costs (the shadow atlas, the volumetric fog, the beam meshes). The `max` column of
both arms is ~600 ms and is the first post-settle frame — shader compilation, identical in both.

---

## §3 — WHAT EACH ROOM IS MADE OF

Every path is relative to the room's own kit ROOT, so **a room can only be dressed out of the pack it
is built from** — the cross-pack borrow that would put a dark-fortress cobweb on a dark-fantasy atlas
is unreachable through `make_prop_public`. Materials resolve through the kit's own MaterialList via
the same `_apply_module_materials` the walls, pillars and torches take (the pillar-quilt resolver);
the dressing authors no second material policy.

| room | groups |
|---|---|
| **R0** | brick rubble 34 · floor litter 26 · snapped planks 16 · scattered bone 14 · rubble piles 12 · displaced flags 12 · **cobwebs 10** · chain heaps 7 |
| **R1** | pebble scatter 22 · silt wash 20 · dirt drifts 15 · rockfall 14 · gravel runs 12 · displaced flags 8 · goblin remains 6 |
| **R2** | bone shards 16 · boulders 11 · cracked slabs 10 · **toppled column drums 9** · **great ribs 8** · displaced flags 6 · ore spill 5 |
| **R3** | grave litter 34 · bone + skull piles 20 · burnt rubble 18 · dirt wash 18 · tombstones 16 · loose skulls 16 · displaced flags 16 · dirt ingress 12 · the fallen 9 · ruined wall stubs 7 · fallen beams 6 |
| **bleed** | 152 pieces across 6 thresholds; the 69 that lie INSIDE a room are in the census and clearance-tested, the corridor half needs no test |

**"Displaced flags" are the kit's own floor tile**, re-instanced tilted 6–10° and sunk 2–13 cm. It is
the cheapest honest cracked flagstone there is and it is guaranteed kit-correct in every room, because
it is literally the tile the floor is made of.

### 3.1 The doorway bleed — both kits cross, in both directions

A spill made of only the room's own kit stops AT the doorway, and the threshold is still a seam: a
clean edge between two clean floors. So each of the six thresholds is dressed **twice** — the room's
own debris runs OUT past the masonry line into the corridor, and the corridor's kit (which is the NEXT
room's kit, by `_build_corridor`'s own pre-existing rule) runs BACK IN past the same line — with each
one's density falling off quadratically on the far side. Where they overlap, two packs' floor litter is
interleaved. That is what "one continuous old place" looks like from a metre off the ground.

Keyframes at all six: `keyframes/RD_walk_thr_{R0E,R1W,R1E,R2W,R2E,R3W}.png`.

### 3.2 The near-wall composition rule, which is an occlusion rule wearing a taste hat

CAM-LOCK stands to the SOUTH-EAST; the south and east walls are the ones that dissolve so the room can
be seen into. Tall dressing there stands solid inside the dissolve and masks the fight. So those two
bands take **ground clutter only** (≤ 0.62 m within 5 m of the wall, and nothing at all within 1.15 m
of it), and every silhouette taller than a man is restricted to the north and west walls — the far side
of frame. The tombstones, wall stubs, fallen beams, column drums and great ribs all carry a `wallfar`
zone for exactly this reason.

---

## §4 — MY OWN FAILURES, in the order they happened

1. **The clearance test did not run at all on the first build, and nothing said so.**
   `const MASKS := { "boss": PackedStringArray([…]) }` is not a constant expression in GDScript, so the
   whole envelope script failed to compile, `disc_clearance` resolved to nothing, and 385 props were
   placed with the law absent. It printed `SCRIPT ERROR: … Nonexistent function 'disc_clearance'`
   **385 times** — caught by scanning the log, not by the frames, which looked entirely reasonable. The
   log scan is in the guard list for this exact reason (TELL-DRESS §6.4, same lesson, second time).
2. **A 12.23 m rib and a 19.8 m-wide dirt patch, inside a room whose wall course is 3.006 m.** The
   first build took each pack's authored scale as a statement about THIS world. It is a statement about
   the pack's world: `SM_Env_Bone_Rib_*` is a Hell-scale set piece and `SM_Gen_Env_Ground_Dirt_*` is
   terrain. Fixed by making every recipe name a size **in metres** and fitting the measured AABB to it.
   Fixed **again** an hour later when a ×1.30 jitter multiplied through the fit and carried a rib back
   to **3.15 m — taller than the masonry it stands against**; the jitter may now only ever shrink.
3. **Ten cobwebs vanished silently and the shortfall line named the symptom, not the cause.** The web
   sampler put them in the four wall corners, which is where a cobweb belongs and also where every
   torch fixture stands — `_sconce_positions()` seats them at ±(edge/2 − 0.85), i.e. **0.57 m** from the
   corner web spot, inside a 1.05 m keep-out. All ten were eaten before instantiation, so no warning
   path was ever reached. They now run the LENGTH of the north and west walls, and both silent-abandon
   branches now `push_warning` with a cause.
4. **The webs hung upward.** Seated by origin rather than by top, a 2.4 m sheet at a 2.8 m hook put
   2.4 m of web above a 3.006 m wall. Seated by top now.
5. **The first ring check FAILED and my instinct was to argue with it** (§ D-1b). Nine flat washes were
   inside the 12 m disc; every one of them was harmless; the clause still says what it says. Evicted.
6. **The first dressed frame at CAM-LOCK was nearly empty**, because I had put all dressing in wall
   bands and the camera holds ~35 m across about the player — the walls it would show are at or beyond
   the frame edge. That is what produced the `field` zone, and the zone is not a relaxation: the same
   clearance test runs on every candidate, and the field groups are all ground clutter.

---

## §5 — AT MATT'S EYE / ROUTED

### 5.1 ⚑ THE PRICE OF THE LAW, AND IT IS VISIBLE IN EVERY FRAME OF THE WATCH

At CAM-LOCK the camera is locked to the PLAYER, and the player is by definition inside the envelope.
So the dressing is at the frame's PERIPHERY in every frame of the watch, by construction, and the floor
under the fight is bare stone. That is the law working, not a shortfall — but it is the single biggest
compositional consequence of the cell and it should be seen before it is judged. It has exactly one
lever and the lever is a number: the margin, **2.00 m**, and the choice to build the grid from the
**whole 60-trace boss battery** rather than from the fixture alone. Dropping to the fixture alone would
free floor near where THAT fight does not go — at the cost of breaking the dressing the moment R-BR-4
picks a different seed for the watch.

### 5.2 ⚑ THE DRESSING HAS ALMOST NO TONAL SEPARATION FROM THE FLOOR — a FINDING, not a licence

Measured on the room-3 plate pose, at the 261,599 pixels the dressing occupies, against the floor those
**same pixels** showed when clean:

| | |
|---|---:|
| dressing-pixel luma, mean / median | 83.24 / 74.15 |
| the floor at those same pixels, mean / median | 81.11 / 73.74 |
| **prop / floor contrast** | **1.0262 ×** |
| dressing pixels under luma 12 (functionally invisible) | **0.77 %** |

The props are **lit** — only 0.77 % of them are functionally black. What they lack is tonal separation:
they read by silhouette and by texture, and almost not at all by brightness. **The cause is item (1) of
the standing five: `UNIFIED_KEY_ENERGY` is shipped at 1.00 (ρ ≈ 0.86–0.95, "uniform but faint"), so a
rubble pile casts almost no shadow of its own and reads as a pattern painted on the floor rather than
as an object standing on it.** If the shadow-depth ruling goes to 3.50, this dressing gains 534 new
cast shadows and separates by itself. **I did not touch a lighting constant to compensate, and the
dressing has not been pre-brightened to hide the coupling** — so whichever way that item is ruled, what
you see is what the ruling produces.

### 5.3 Smaller items

3. **R0 reads sparsest at the plate pose despite carrying the second-highest prop count** (131 props,
   4.41 % of frame) — its pieces are simply the smallest, which is its character. If the eye wants the
   guardroom denser it is four `count` integers in one table and no other change.
4. **The bleed spans a KIT BOUNDARY at every east threshold.** By `_build_corridor`'s own pre-existing
   rule the corridor wears the NEXT room's kit, so room *i*'s east threshold has the next pack's litter
   crossing back into it. I read that as the point of a bleed rather than as a defect; it is a taste
   call and taste calls in this run are veto-open.
5. **Nothing in the dressing is collidable.** `with_collision = false` is the watch's own setting and
   nothing here changes it — this is depiction, not a playable level. When the seam ever becomes
   playable, every prop needs a decision (static body vs walk-through), and the census is the list.
6. **534 props is not a per-room budget, it is one seed's outcome.** The whole layout re-rolls from
   `LEVEL_SEED` (74001000) and is reproducible from it; the counts in §3 are targets, and a group that
   cannot find clear floor reports its shortfall rather than relaxing the law. This build reported
   **zero shortfalls**.

---

## §6 — DELIVERABLES — `~/Games/reincarnated-godot/tmp/roomdress/` (87 MB after prune)

**M-EYE, MOTION FIRST. CAM-LOCK on every clip, camera identity AND the dressing ARM printed on every
frame** (the watch banner now carries a `DRESSING:` line beside `CAMERA:` and `BEAM:` — a before/after
pair whose halves are visually similar cannot be told apart later from the file alone, which is the
class of ambiguity that cost BEAM-FIX two clips).

1. **`clips/ROOMDRESS_before_after_watch_CAMLOCK.mp4`** — **WATCH THIS FIRST.** The real trace-driven
   watch, seed 74000806, clean masonry beside the dressed room, same 200 frames, same camera, one
   variable. The nova fires at frame 92 in both halves.
2. **`clips/ROOMDRESS_four_room_walk_CAMLOCK.mp4`** — 620 frames / 20.7 s, the CAM-LOCK lock target
   walked in a straight line from room 0's centre to room 3's centre (157.5 m), crossing all three
   corridors and all six thresholds. Only the camera's POSITION moves; its basis is never recomputed,
   exactly as `wr2_playback.gd::_pl_cam_update()` does it, so this is the watch's rig and not a
   lookalike of it.
3. **`plates/PLATE_D2_four_rooms.png`** (+ `…_gammalift.png`) — the four-up, one pose per room.
4. **`plates/PLATE_D1_clearance.png`** — the gate as a picture: four rooms, the measured envelope, the
   margin contour, and all 534 footprints.

**Keyframes:** `RD_watch_nova_burst_{clean,dressed}.png` · `RD_walk_thr_{R0E,R1W,R1E,R2W,R2E,R3W}.png`.
**Instruments:** `measure/envelope.py` · `measure/clearance.py` · `measure/bake_mask.py` ·
`measure/verify.py` · `measure/telegraph_census.json` · `measure/census_watch.json` ·
`measure/D1_verify.json` · `measure/D1_ring.json` · `measure/D2_rooms.json` ·
`measure/D3_lighting.json` · `l7/l7_roomdress.png` · `rd_probe.gd` / `.tscn` · `run_rd.sh` · `logs/`.

---

## §7 — GUARDS

| guard | result |
|---|---|
| collision check at cell start | clean, HEAD `30f83fc` as expected |
| declared authorised surface | `scripts/wr1_dressing.gd` + `wr1_dress_envelope.gd` (**new**), `kit_replica_level.gd`, `wr1_level.gd`, `wr2_playback.gd` — **5 files, nothing else in the tracked tree moved** |
| `project.godot` sha256 | `6bef17eb6dd5e44a…` — **NO DELTA** (TELL-DRESS's banked value) |
| `walltop_void_radial` / `walltop_occlude` shaders | `2710fc11…` / `d29a01be…` — unchanged |
| `sky_shaft` / `sky_dust` shaders | `535974e0…` / `599c4283…` — untouched; this cell draws stone and bone, not light |
| all `vfx/ambient/**` rollup | **`e049676b85c5c59f…`** — byte-identical to BEAM-CONE, SHADOW-UNIFY and TELL-DRESS |
| **lighting constants** | **ZERO edits.** No `Light3D`, no emissive material, no environment override, no particle system is authored by this cell. |
| prior cells' clips | beamcone / beamfix / rivalcast / shadowunify / telldress — **32 clips, all intact** |
| engine tree | **never opened for write**; traces read READ-ONLY |
| `SCRIPT ERROR` / `Parse Error` / `SHADER ERROR` scan on all 29 logs | **0** |
| LSTAT-2 | sha unchanged, **0 px** |
| staticity | **0 px of 921,600**, max channel 0 |
| disk | `tmp/roomdress` **87 MB** after prune; peak intermediates ~750 MB (the 620-frame walk), **well under the 2 GB ceiling**; every PNG sequence encoded then deleted |
| godot commit | **`78043af` LOCAL, ahead 15, NOT pushed** |

---

## §8 — ROUTING

**LAP-1 WATCH (BR-1 §3 cell #7) is unblocked.** The dressing is opt-in behind `--dress 1`, so the watch
can be cut with or without it and the arm is on the frame either way. The re-pinned substrate
(R-BR-6) and the fixture seed are the ones this cell measured against; if R-BR-4 selects a different
seed the dressing does not move, because the envelope grid already covers all 60 boss traces.

The five-item brightness decision remains open, item (2) of §5 above is now a **sixth** thing riding on
its first clause, and none of them block the watch.
