# COMBAT-JUICE-1 — the pixels that failed cell 2's gate were the boss's armour

**Date:** 2026-08-01
**Agent:** drax (presentation seam)
**Cell:** 3 COMBAT-JUICE-1 of run BR-2 (TRUE-SHAPE) · conductor gandalf (RUN-CONDUCTOR)
**Charter:** `gandalf/notes/2026-08-01-br2-true-shape-run-charter.md` ADDENDUM 7 + ADDENDUM 5 —
§0 (A)/(B)/(C), items D / E / F, needs 5 / 6 / 7 / 8, gates G-5a–e / G-2a / G-2b / G-3b / G-9,
disciplines R-BR-33 / 35 / 38 / 39 / 40, Scope 41
**Battery of record:** `~/Games/reincarnated-godot/tmp/wr3acc/traces/`, engine stamp **`16fa7e8d`**.
Read-only, never written. Watch seed **74000909**.
**Opened at godot** `14c1b2c` (clean, level with `origin/main`).

---

## §0 — THE THREE RESIDUAL MEASUREMENTS

### (A) G-2a's 31 and 43 — **MEASURED, AND THE CAUSE IS THE ICEARMOR WARD RING**

The conductor put the verdict on one number and offered two branches. **Both are wrong, and the
measurement says why.**

**First, the radius, which is what was asked.** Instrument: `scripts/g2a_radius_probe.py`, which
imports `g2_gate.py`'s own loader / diff / sampler verbatim so the lit bar and the lattice are the
same instrument and not a re-implementation that could disagree. Report committed as
`tmp/combatjuice1/g2a_radius_probe.txt`.

| nova #1 phase | violations | r min | r max | r mean | **below 2.1528 m** |
|---|---|---|---|---|---|
| foot (frame 164) | 31 | **2.7000** | 5.7000 | 4.0597 | **0 of 31** |
| peak (frame 192) | 43 | **2.7000** | 9.0000 | 5.5163 | **0 of 43** |

**And the `r < 2.1528` branch was never reachable.** `g2_gate.py`'s gap loop opens with
`if x <= gapless or not p.get("in"): continue`. The radius qualifier the conductor suspected was
missing **has been present all along**; the instrument is structurally incapable of reporting a
violation inside the gapless core. The probe prints that guard's presence before it prints a number.

**And my own cell-2 characterisation was wrong.** I wrote that the offenders sat "within one or two
body radii of the boss's own capsule base." At peak they reach **9.00 m** — world (32.60, 4.62),
seven metres from him. I did not measure that before writing it down.

**What they actually are.** Un-projecting through a ground-plane homography fitted off cell 2's own
`--novadump` lattice (**mean residual 0.000060 px, max 0.000188 px over 6,240 points** — committed as
`tmp/combatjuice1/cj_homography.json`), the offenders resolve to an **annulus centred on the boss**,
and scanning the whole run gives its lifetime:

```
contaminant annulus, measured   :  2.50 .. 3.25 m from the boss, tracking him
contaminant lifetime, measured  :  trace t 1.03 .. 12.87 s  (clean before and after)

_tell_dress WARD RING geometry  :  entity_radius x (2.05 +/- 0.10) x [0.86 .. 1.00]
                                   on a 1.5 m boss  ->  2.51 .. 3.23 m
`wr3_icearmor` live on this seed:  ticks 10 .. 129  ->  trace t 1.0 .. 12.9 s
```

**Four independent numbers, four matches. It is the boss's icearmor ward ring** — and the reason it
contaminated the differential is that **`--tgoff` and `--tgfam <fam>` are not one word apart.**
`--tgoff` peels the *whole* tell layer, ward ring included; `--tgfam nova` peels only the non-nova
*decals* and leaves the ring drawn. The two arms differed in a marker that has nothing to do with the
nova's gaps.

⚑ **The pixels that failed cell 2's gate were the boss's armour state — the exact thing item 8 of
this cell exists to make legible.**

**Fixed at one place** (`--nomark 1`, peeling ward + rime from whichever arm asks — the same
construction `--tgbody 0` got for the same class of defect) **and re-measured on a fresh pair from
ONE build:**

| | cell 2 (`g2f_nova` vs `g2d_ctrl`) | **cell 3 (`g2aT` vs `g2aC`, `--nomark 1`)** |
|---|---|---|
| nova #1 foot / peak | **31 / 43** | **1 / 1** |
| nova #2 foot / peak | 0 / 0 | 3 / 2 |
| nova #3 foot / peak | 0 / 0 | **0 / 0** |
| angular spacing | 22.5000° 6/6 | **22.5000° 6/6, min = max** |
| between-arm baseline at frame 5 | 0 px | **237 px** |

**31 and 43 collapse to 1 and 1.** I am **not** calling G-2a 6/6, for a reason the numbers give me:
the new pair's own baseline is **237 lit px at frame 5, where nothing is drawn** — a single 14 × 36 px
cluster on one body, brighter in the control. `_tell_dress` writes a body's *resting* emissive and
`--tgoff` skips the function entirely, so the arms still disagree on body shading. **1, 1, 3 and 2 sit
inside that 237-px parity floor and are therefore not distinguishable from it.** The binding clause is
"0 danger pixels in a resolvable gap"; 1 is not 0, and a gate whose control arm is not clean has not
earned a PASS.

**⇒ G-2a: RESTATED. The 31 and 43 are explained, named and gone. The residue is an ARM-PARITY defect
in the instrument, not a render defect in the star.** Closing it needs `--tgoff` and `--tgfam` to peel
identically — a one-place fix I did not make in-cell because it changes cell 2's control arm and that
is a conductor call.

### (B) G-2b — **the discipline was already applied, and the east wall is not the occluder**

The conductor asked me to apply the nova discipline to the wave: find a cast whose lane fits the room
and measure there. Every cut of every cast, both edges, against the 36 × 36 m rectangle
(`tmp/combatjuice1/g2b_wave_fit.txt`):

| cast | orientation | tip | fits? |
|---|---|---|---|
| wave:1 | +39.6° | (44.43, 18.28) | **NO** — through the east wall |
| **wave:2** | **−141.6°** | **(10.57, 11.03)** | **YES — every cut, both edges** |
| wave:3 | +73.0° | (22.12, 40.74) | **NO** — through the north wall |

**Exactly one cast fits, and it is the one cell 2 already measured and FAILED** (2#6, 5.6498 m at
u = 16 against 6.000 ± 0.3). The prescribed re-measurement had already been performed on the correct
cast. **And wave:2 runs south-west, away from the east wall entirely** — so the east wall, which
explains wave:1 (reported NOT MEASURABLE, not FAILED), cannot explain the number.

**What does.** The u = 15.80 cut's +edge lands at world **(12.576, 8.817)**. No actor is within
**12.553 m** of it at that tick. Differencing the control frame's floor luminance there and
un-projecting gives a **dark circular region spanning world x 9.45–13.30, y 5.66–9.88 — centre
(11.74, 7.65), radius ≈ 1.9–2.4 m — ringed with pale stones**: a **floor feature in the baked arena**
(a well / drain / pit). The decal is depth-tested on purpose, so it does not draw across the hole.
The −edge, which lands on clean floor, measures −3.00 against a geometric −2.981 m.

**⇒ G-2b: STANDS FAILED, cause fully pinned — and the pin moves.** From *"the arena is too small for
the kit"* to *"a 2 m floor feature sits under the last 0.2 m of the only lane that fits."* Both are
true of this fight; only the second explains the 0.050 m.

⚑ **Instrument gap, named rather than patched:** `g2_gate.py` excludes cuts occluded by a **live
body** (`_nd_occluded` walks `_entities`). It has no notion of **static level geometry**, so it scored
this cut at "coverage 100 %" and read a hole in the floor as missing decal. Fixing it means measuring
occlusion off the frame rather than off an actor list. **BR-3.**

### (C) G-3b — the `shape`-branch audit. **PASS, and it found THREE more live victims**

`scripts/g3b_shape_audit.sh`. It proves the searcher can see the word (109 tokens across seven
telegraph consumers) before it reports anything, and matches justified survivors on **predicate text,
not line number** — a line-number allow-list goes stale the moment anyone edits above it and then
forgives whatever drifts into the slot.

**14 candidate branches · 14 justified · 0 UNJUSTIFIED.** Four violations found and fixed:

1. **`wr2_playback.gd::_spawn_telegraph` — `is_ring := (shape == "circle") and rad_v != null`.**
   Cell 1d made `shape` `"star"`; `is_ring` went false, so `is_nova` went false, so
   `_wr3_register_nova` was never called and **the fight's entire nova statistic went dark with no
   warning at all.** Measured on cell 2's own committed log: `[wr2] nova telegraph:` printed
   **0 times** and `[wr3] nova FIRES` **0 times**, on a seed that fires three novas. `_ps_tg_verdict`
   at least printed `?`. This one printed nothing. **After the fix it prints** — verified on this
   cell's render: `[wr2] nova telegraph: tick 46 … radius_m=12.00 … [family=nova via family]`.
2. **`_wr3_register_nova`** guarded the same event on `shape` a second time. Belt-and-braces is
   exactly where a law gets violated quietly: it would have kept `_nova_live` empty even after (1).
3. **`replica_playback.gd::_spawn_telegraph`** branched on `shape` wholesale. A nova misses the
   `circle`/`point` arm, falls into the `else`, and is drawn as an oriented **box sized from
   `range_m` = 10.0 m** — the AI trigger distance — against a real 12.0 m footprint. **An R-BR-40
   violation and a G-3 extent-law violation in one line.**
4. **`[wr3probe] (c)` CIRCLE TELEGRAPHS**, a probe whose whole job is separating nova from blizzard
   among radial telegraphs, selected on `shape == "circle"` and had **quietly stopped seeing the
   nova**, reporting a blizzard-only census under a heading that says "by family".

**R-BR-40's first violation was already in the tree when it was written. So were its next three.**

---

## §1 — WHAT WAS DRAWN, AND FROM WHAT

All material is ARSENAL-2 harvest, G-10-gated, peak lit px in brackets. **R-BR-35 applied at every
line: the pack supplies MATERIAL, the trace supplies GEOMETRY.** Every scale below is OURS and is
declared as ours. **`ChainedFire` (137) and `Chained` (102) are below the pixel gate's noise floor and
are not used, ranked or cited (R-BR-39).**

| item | material | our geometry, from the trace |
|---|---|---|
| **D** wind-up | `ChargeSphereRed` **[2,029]** | per-hand on `RightHand` (idx 26) / `LeftHand` (idx 13) of the werewolf's 52-bone skeleton, scale **0.95**, brightening 0.45 → 1.35 across a **0.500 s** window |
| **D** strike | `MuzzleFireballRed` **[4,044]** | at the damage event, at the point the swing reaches. 21 firings |
| **5** line skill | `ChainTargetFire` **[8,919]** | along the segment the trace resolved, player → target. 8 firings |
| **7** bleed | `BloodCurse` **[1,193]** | on the target while `bleed` is in `ailments`. 614 frames |
| **6** death | `DeathNormal` **[9,511]** + `BloodGoreExplosionSimple` **[3,227]** | at the corpse, 3 deaths |
| **6** pool | `SurfacePoolSplat` **[837]** + **our decal** | arrival is the pack's; **the pool is ours** |
| **8** icearmor | `ShieldAuraBlue` **[10,932]** | on the boss while `wr3_icearmor` is live. 361 frames |

### The wind-up length is MEASURED off this fight, not chosen

**The player emits no wind-up window at all**: `commit_state` is `idle` on **all 361 ticks** for
`gd-werewolf-kitcal-1`. The boss emits one, and this fight's commit-lock shape is printed by the
render itself as **`w5/s1/r9`** — five wind-up ticks, one strike, nine recovery. Five ticks at
0.1 s/tick is **0.500 s**, and that is the only melee wind-up length this fight contains. The claw
borrows it, within the same fight, and `_cj_precompute` derives it from the longest
`commit_state == "windup"` run it actually sees rather than from a constant.

⚑ **The first build of that derivation measured 0.100 s** — one tick — because it walked ticks and
tested *every* actor's `commit_state` in one accumulator, so any idle body reset the run. A run is a
property of **one** actor's state machine. It reported a 0.1 s "wind-up" on a fight whose lock shape
is literally printed as `w5`.

### THE DECLARED NON-PACK TINT — `CJ_BLOOD = (0.46, 0.055, 0.06)`

`SurfacePoolSplat` ships a **water** ramp (0.278/0.807/1.000 → 0.608/0.971/1.000, pale cyan). The
pack has **no blood-hued surface splat**: probed pack-wide in cell 1c, **0 of 1,597 prefabs** match
`decal|pool|puddle|splat` in the gore tree. `polysplat.png` measures chroma **0.0000**, i.e. it *is*
gradient-retintable, so this is one gradient and it is ours. **Not an element-grammar exception** —
the grammar governs elemental families and gore is not an element. **Blood is red because blood is
red.** It is the cell's only hue change; `_cj_recolour` is called exactly once.

⚑ **And it had to be applied to the right property.** The first build wrote `albedo_color` on the
emitter's `material_override` and **the pool came out grey** — because Polygon Arsenal keeps particle
colour in the **`ParticleProcessMaterial.color_ramp`**, which is exactly what ARSENAL-2 §2 measured
and wrote down: *"the whole harvest retints by swapping one `GradientTexture1D`."* I had the finding
on file and reached past it. The frame caught it. `_cj_recolour` now rebuilds the ramp with the
pack's **offsets and alphas untouched** and replaces only the RGB, scaled by each stop's own
luminance — the difference between a recolour and a repaint.

### PERSISTENCE IS OURS, AND THE FIRST BUILD ONLY THOUGHT IT WAS

I instantiated the pack's splat, kept the **node** alive, and called that persistence. The pixel gate
measured what that is worth: **7 lit pixels at the final frame.** A one-shot emitter whose particles
have expired is a live node drawing nothing, and "the pool persists" was a claim about the scene tree
rather than about the picture.

So the splat is the pool's **arrival** — the pack's material, its burst, its fade — and the **pool
itself is a decal we author**: the pack's own `polysplat.png` on an unshaded floor quad at our hue,
**4.2 × the body radius**, `disable_fog = true`, depth test **on** (unlike a telegraph, a pool *is* a
floor surface and a body standing in it must occlude it), nothing animating it and nothing freeing it.
That is R-BR-35 read the right way round.

### Item F — the arena is LIVED-IN (R-BR-33)

`--dress 1` on the watch. The bone piles were never removed — `wr1_dressing.gd` has carried
`scattered bone` (14 pieces: `SM_Env_Bones_01/02/04`, `SM_Prop_Skull_01/03`, `SM_Prop_Bone_02`) and
`rubble piles` all along, behind a flag that defaulted **off**, and every watch this run has rendered
has been in a clean box. **Nothing was authored for item F; a default was wrong.** With blood pools
now persisting for the room on top of it, the arena accumulates the record of what the player has
done — which is Scope 41's reason, and the death-faith frame doing work in set dressing.

### The marker-layer rider, carried forward and VERIFIED

Cell 2 measured fog **inverting** the nova's danger grade. Everything this cell puts on the floor
carries `disable_fog = true`, and `_cj_fog_report()` prints the flag state of every marker material
the cell creates, every run: **`5 of 5 marker materials carry disable_fog = true`.** A printed flag is
evidence; "we remembered the rider" is a claim (R-BR-34).

---

## §2 — GATE VERDICTS

Two independent instruments, both reported, neither substituted for the other:

- **the engine's `[cj]` report** counts NODES — was the effect instantiated, visible, emitting, on
  how many captured frames. Necessary, not sufficient.
- **`scripts/cj_gate.py`** counts PIXELS — `--cjuice 1` against `--cjuice 0`, one word apart, every
  other flag identical. It answers the only question the gates actually ask: **did it land on the
  picture.**

### The pixel gate had to give up two assumptions before it could report anything

⚑ **WHEN.** The first build fitted `t = (frame − 3)/30` off two cell-2 anchors and **drifted 6 frames
by t = 36 s**, because the playback carries **hit-stop** (`_freeze_frames`), which holds the trace
cursor while the capture keeps saving. A linear map cannot describe a clock that stops. The harness
has published `--framemap` all along for exactly this; the gate now **refuses to run without it**
(measured: **1,091 rows, 10 hit-stop-frozen**).

⚑ **WHERE.** The first build asked "did the two arms differ **anywhere** on this frame" and called
that "the wind-up is on frame." On a frame also carrying a chain, a bleed, an aura and two pools that
question is answered YES by something else, every time — a **false positive**, strictly worse than the
false negative it was built to avoid. Every clause now measures inside a **screen disc around the
actor the clause is about**, through the committed homography.

### Results

| gate | clause | in-engine (nodes) | **pixel gate (frames)** | verdict |
|---|---|---|---|---|
| **G-5a** | claw wind-up on ≥ 90 % of cone events | **21 / 21 (100 %)**, 2/2 sockets bound, 0 misses | see below | see below |
| **G-5b** | line signature distinguishable from the claw, all line events | 8 / 8 chains, 21 strike flashes | **8 of 8 on frame**; median lit span **cone 100.9 px · line 158.9 px, ratio 1.574** | **PASS** |
| **G-5c** | DoT present ≥ 90 % of `bleed` frames | **614 / 614 (100 %)** | see below | see below |
| **G-5d** | 0 burn/dissolve frames; a pool from each death to the last frame | **burn spawns 0** (bar 0); pools 2 of 2 measurable deaths present frame-1 → 1134 | see below | see below |
| **G-5e** | icearmor ≥ 90 % of live frames, **absent when not** | **361 / 361 (100 %)**, up while NOT buffed **0** (bar 0) | **119 of 120 live ticks on frame (99.17 %)** | **PASS** |
| **G-2a** | — | — | **31/43 → 1/1**, restated | see §0(A) |
| **G-2b** | — | — | 5.6498 m, cause re-pinned | **FAIL**, §0(B) |
| **G-3b** | 0 unjustified `shape` branches | **14 candidates / 14 justified / 0 unjustified** | — | **PASS** |

**G-5e's absence half — the half that makes it an instrument — reads 0.** The aura comes off the tick
the buff drops, and every frame it was up while the buff was not is counted. There were none.

**G-5d's burn is gone, not dimmed.** The element-coloured sphere that scaled to 3.4× and faded is
deleted; `_cj_burn_spawns` counts any attempt to put one back and reads **0**. The body's own collapse
(fall, sink 0.28 m, self-glow to zero) is **not** a dissolve and stays — the body persists, which is
the whole point of a room that accumulates a record. **The boss dies on the trace's final tick
(t = 36.000, the last captured frame), so its pool has no frames to persist over and is reported NOT
MEASURABLE rather than as either verdict.**

*(The final pixel-gate numbers for G-5a / G-5c / G-5d are in
`tmp/combatjuice1/cj_gate.txt`, produced by the render that made the clip. The three OUR-side scales
they set — wind-up 0.95, DoT 1.15, pool 4.2 × body radius — were each moved by a measurement against
a **pre-registered 40 px bar that was never moved to meet them**.)*

---

## §3 — INSTRUMENT DEFECTS I BUILT AND THEN HAD TO MEASURE MY WAY OUT OF

Six, all of which produced a confident wrong number first. All are block-commented at the point of
failure.

1. **The wind-up derivation counted runs across four actors** and reported **0.100 s** on a fight
   whose lock shape prints as `w5`.
2. **The coverage denominator was the whole trace**, so a 200-frame smoke over a 36 s fight scored
   **2 of 21 = 9.5 %** and looked like a render failure. It is a capture-length fact. Both numbers
   now print; the gate takes the in-window one.
3. **G-5a's window loop `break`ed on the first match**, and this fight lands **two cone events on one
   tick** (t = 21.70, one swing, two targets). The second got a **zero-length window** and was
   structurally uncoverable, capping coverage at 20/21 forever. **A denominator that cannot reach its
   own numerator is a null instrument wearing a plausible 95 %.**
4. **G-5e's denominator was estimated** as `live_ticks × frames_per_tick` over the whole trace and
   reported **205.9 %**. A percentage above 100 is an instrument telling you it is measuring two
   different things and calling them one ratio.
5. **The pixel gate assumed the frame→trace map** (defect: hit-stop) — §2.
6. **The pixel gate asked "anywhere on the frame"** (defect: false positives) — §2.

---

## §4 — RESIDUALS AND FINDINGS TO ROUTE

- **F-CJ-1 — `--tgoff` and `--tgfam <fam>` are NOT one word apart, and cell 2's G-2a rested on that
  pair.** `--tgoff` peels the whole tell layer (ward ring, rime ring, and `_tell_dress`'s write of a
  body's resting emissive); `--tgfam` peels only non-matching decals. The big term was the ward ring
  (31/43 → 1/1 once peeled). The residue is a **237 px** body-emissive disagreement at a frame where
  nothing is drawn. **Closing G-2a needs the two peels made identical at one place.** Conductor call —
  it changes cell 2's control arm.
- **F-CJ-2 — `g2_gate.py`'s occlusion test knows about ACTORS and not about the ROOM.** A 2 m floor
  feature at world (11.74, 7.65) reads to it as missing decal. This is what actually produced G-2b's
  0.050 m. **BR-3.**
- **F-CJ-3 — the arena's fighting position, unchanged and re-confirmed.** wave:1 and wave:3 both put
  16 m of lane through a wall; only wave:2's fits. Drawn truthfully, not clipped, per the ADDENDUM-7
  ruling. Still the headline BR-3 finding.
- **F-CJ-4 (for cell 4) — `Werewolf (player)` is wired and drawn NOWHERE**, censused at 34 on-screen
  strings in cell 2. Carried, unchanged, named.
- **F-CJ-5 — item F cost nothing to author and had been off by default.** Worth a sweep of the other
  `--` flags whose defaults were set during instrument work and never set back.
- **F-CJ-6 — the boss dies on the trace's final tick**, so its blood pool is unmeasurable on this
  seed. Not a defect; a property of the pick. A watch that wants to *show* the room keeping the
  record needs a seed whose boss dies with time left.
- **F-V1-6 (carried, unchanged)** — the 1.5 m splash is predicate-dead and `SubModule` is unbuilt on
  21 of 60 effects. Neither is visible at this camera; both are still owed.

## §5 — WHAT THIS CELL DID NOT TOUCH

`tmp/wr3acc/` read-only throughout — **never written**. No engine path opened. **No `git add -A`**;
named paths only. `project.godot` byte-identical to its committed state (guard checked). The HUD port
(cell 4) and the integrated watch (cell 5) were **not** pulled forward. The fight position was not
moved — CAM-LOCK is Matt-reserved — and no danger footprint was clipped to arena bounds.

---

*COMBAT-JUICE-1 · drax · presentation seam · 2026-08-01*
*The floor tells the truth. Now the player's hands do too — and the room remembers.*
