# SKY-2 + WALLTOP-2 + CRIT-RED — the beam is geometry, the band was the brickwork, and the trace could tell all along

> **Cell:** SKY-2 (circle up / shutter slats / beam law / parallax) · WALLTOP-2 (one uniform band) ·
> CRIT-RED (red crit numerals). **Agent:** drax (presentation seam).
> **Conductor:** gandalf (RUN-CONDUCTOR, LR/presentation session). **Date:** 2026-07-30.
> **Contract of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` — Scope 9 (per-room
> skylight intent) · Scope 11 (SKY-2 directives + parallax honesty clause) · Scope 12 (Arm A ruled) ·
> Scope 13 (unified shadow grammar — NOT implemented here, and nothing built here fights it) ·
> Scope 14 (this cell's charter, Matt's verbatim rulings) · the INTEGRATE-PREP and BEAUTY-CORNER
> landing blocks.
> **Inherited:** godot `ec40cdc` LOCAL (ahead 7). **Shipped:** godot LOCAL (ahead 8, NOT pushed).

---

## §0 — What this cell says in five sentences

The beam is **mesh geometry, not fog**, and that was decided by measuring the froxel volume rather
than by preferring a technique — the fog has no silhouette in it to be crisp, and its 90 % temporal
reprojection is a smear generator for a pattern whose whole brief is that it moves. The walltop's
three bands were **not tone and not lighting**: every screen-space pass was ablated and moved
*exactly zero* cap pixels, and the bands turned out to be `Brick_Small_01`'s own mortar coursing,
sampled across 40 % of one tile at a world-locked phase. **The trace CAN distinguish crits** — the
field is there on 100 % of damage events, and this watch has exactly one, at t = 36.300 s, now
rendering red. Three of my own constructions died to their own renders and are on record with their
numbers: a single-surface beam sample that cut the circle in half, a path normalisation that blew
the beam to a white cloud, and a coupling instrument that was measuring the distance between two
different skylights. **The one thing I could not deliver is routed rather than hidden:** the
circle-beam is 6.93 m wide and 3.01 m tall, and no constant available to me makes that a column.

---

## §1 — PART 1: SKY-2

### 1.1 "Top half" is a screen statement about a world object, so it was measured

The watch's cameras share one bearing (`CAM_YAW_DEG = 47°`; `arena`, `arena_full` and `player_lock`
are byte-identical on it per the CAM-LOCK landing), so the ground direction pointing UP the screen is
`(-sin yaw, -cos yaw)`. The probe projects the four half-edge midpoints through the **actual
Camera3D** and reports which lands highest:

```
half-edge -X (west) -> screen y 376.4   <- TOP OF ROOM
ground screen-up unit XZ = (-0.7314, -0.6820)
check: -sin(47), -cos(47) = (-0.7314, -0.6820)
```

Agreement to four decimals — and then the complaint itself corroborates the axis: **the pre-SKY-2
pool sat at (−1.51, 2.70), which projects onto that axis at −0.737, i.e. in the BOTTOM half**, exactly
where Matt said the circle sits today. The bearing is handed down from `wr2_playback.gd::CAM_YAW_DEG`
rather than re-declared in the level, so a camera that ever stops sharing it breaks one line instead
of drifting silently across two files.

**Shipped layout, all four rooms** (screen-up dot: positive = top half, negative = bottom half):

| room | motif | circle pool | dot | slats | slat pool | dot |
|---|---|---|---|---|---|---|
| 0 trash | cracked-seam | (−6.06, −5.33) | **+8.07** | 5 | (5.01, 2.90) | **−5.65** |
| 1 champion | cracked-seam | (−5.85, −4.35) | **+7.24** | 4 | (5.10, 2.34) | **−5.33** |
| 2 mixed_pack | window-lattice | (−6.40, −1.47) | **+5.68** | 5 | (3.37, 7.00) | **−7.24** |
| **3 boss (the watch's room)** | **oculus-ring** | **(−3.30, −5.12)** | **+5.91** | **5** | **(1.90, 6.73)** | **−5.98** |

Per-room seeding **stands** (Scope 9): the original six draws keep their order and their meaning and
the slat draws are *appended*, because re-ordering them would have silently re-rolled every room's
motif. Rooms 0/1 still share `cracked-seam` — **the pigeonhole flag carries exactly as declared**.

### 1.2 ⚑ FOG vs MESH — decided by measurement, and the fog lost on its own numbers

The brief allowed E3's bounded-FogVolume machinery or a mesh, and required the choice be measured.
The froxel volume was measured first, in the room, at shipped settings:

- **Above the wall line it contributes exactly nothing** — E3's own VOID-1 fix capped the fog box at
  `WALL_H` because a taller volume glows into the void (three iterations bought that cap). Fine.
- **Within that height it is not a shaft at all.** Fog-on minus fog-off at the shaft camera is a
  room-wide **plateau**: peak/mean 1.8–3.2 spread across half the frame width, elevated in 9 of 16
  bins. There is no silhouette in it to be crisp.
- **The froxel grid is 128 wide across the viewport**, so any density boundary is quantised to
  ~12.5 px at 1600 px before Godot's own filter — and `volumetric_fog_temporal_reprojection_amount
  = 0.9` then blends 90 % of the previous frame, which is a smear generator for a pattern whose
  brief is that it *moves*.

The shipped mesh beam measures a **10–90 % edge of 4–7 px on a 13 px core**. A froxel shaft cannot
reach that: one froxel is already 12.5 px. **E3's fog is untouched** — it is still the room's haze.

### 1.3 The beam law, and the two bounds that make "cannot diffuse outwards" structural

`scripts/sky_shaft.gdshader`. The shader reconstructs the spot's own projective mask coordinate from
the lamp transform the `SpotLight3D` is actually using, then **ray-marches** the view ray through the
cone (32 steps, screen-hash jittered) accumulating the mask.

1. `continue` when `dot(m,m) > 1` — outside the cone a sample does not exist. Not small: absent.
2. **the integral IS the chord** — near the silhouette fewer samples fall inside, so the beam reaches
   zero *at its own boundary by arithmetic*. No separate fudge term.

Brightness is `1 - exp(-acc·density)` — Beer–Lambert, so it saturates smoothly instead of clipping,
and is still linear in `acc` near the edge, which is what preserves the crisp boundary.
The apex fades **along the axis only** (never radially) so the beam does not terminate in a hard disc
hanging in mid-air — the room has no ceiling mesh, and `apex_fade` is what turns a cut into an
arrival.

**Dust** (`sky_dust.gdshader`) runs the *identical* cone+mask test against the *same* uniforms and
`discard`s outside it — so "dust lives ONLY inside the shaft" is structural, and a mote in a slit's
shadow is impossible too, because the mask carves the dust exactly as it carves the beam.
"Lit directionally along the beam axis" is a **Henyey–Greenstein forward-scatter term** on the angle
between the view ray and the beam axis — computed, not faked, and the same anisotropy grammar E3's
fog already runs. Particles are explicitly set non-casting (the BEAUTY-CORNER §2.4 billboard defect).

### 1.4 ⚑ APEX-FOOT COUPLING — verified, after three instruments failed

Coupling is structural (beam and pool are the same cone, same mask), but that only holds if my
reconstruction of the projector coordinate agrees with Godot's. **Three attempts to settle it inside
the room all failed for one reason, and it is worth naming: the room contains TWO skylight patterns,
and "the brightest blob" was not guaranteed to be the same pattern in the pool image as in the beam
image. The instrument was measuring the distance between two different skylights and reporting it as
an error.** A leaning volume viewed from overhead is also a scaled, shifted *smear* of its pool, so a
weak correlation proves nothing either way — measured, and it did not settle it.

`tmp/sky2/mask_cal.gd` removes everything: one floor, one lamp, one mask, vertical, orthographic
top-down, no room, no second pattern, no tonemap, no glow.

| convention | beam px | bbox | **IoU vs POOL** |
|---|---|---|---|
| **`mask_sign (1,1)` — SHIPPED** | 26,244 | x[470..631] y[470..631] | **0.963** |
| mirrored in u | 26,244 | x[268..429] y[470..631] | 0.000 |
| mirrored in v | 26,244 | x[470..631] y[268..429] | 0.000 |
| rotated 180° | 26,244 | x[268..429] y[268..429] | 0.000 |

(POOL bbox x[470..628] y[470..628].) The shipped convention puts the beam's footprint **on its own
pool**; every alternative lands it in a different quadrant. ⚑ The beam is measured with an *absolute*
floor, not a fraction of its own max, because where it lands on the pool the 8-bit sum **clips** — a
relative threshold under-reports exactly the case that is correct.

⚑ **A real Godot gotcha found on the way, recorded because it is a trap:** a spot with a
`light_projector` and `shadow_enabled = false` renders **no light at all** — 0 lit pixels with the
projector set against 329,492 with it cleared. The shipped skylight only works because
`_arm_shadow_spot()` happens to switch shadows on. **A future `--no-shadows` peel would silently
delete the pools, not just the shadows** — and under Scope 13's SHADOW-UNIFY, which retires spot
shadow-casting, this is a live hazard for the next cell. Flagged, not fixed here (Scope 13 owns it).

### 1.5 Parallax — shaft and pool move as ONE BODY, verified geometrically

Node chain: `slide` (translation) → `tilt` (rotation about the beam's **foot**) → { lamp, shaft mesh,
dust }. There is no code path that moves one and not the other; the driver writes only those two
transforms. The observer is the player's own interpolated position, read in the same assignment the
proxy is drawn at (the CAM-LOCK/E1 same-frame discipline).

Observer (0,0) → (16,16) m, i.e. |rel| 22.63 m, `SKY_PARALLAX_SLIDE 0.030` ⇒ predicted 0.679 m:

| pattern | pool foot before | pool foot after | displacement |
|---|---|---|---|
| circle | (−3.3045, −5.1225) | (−2.8245, −4.6426) | **(+0.4800, +0.4800)** |
| slats | (1.8979, 6.7307) | (2.3778, 7.2107) | **(+0.4800, +0.4800)** |

Both patterns move by **exactly the slide**, to four decimals, and the beam's foot *is* that point.

⚑ **An image-space estimator disagreed and was wrong, and I am reporting it rather than quoting only
the number that suited me.** Intensity-weighted centroids put the pool's shift at 0.13 m against the
beam's 0.39–0.62 m, which looks like a 0.27–0.50 m decoupling. It is not: the tilt rotates the lamp
about the foot, which changes the pool's *incidence* and therefore redistributes brightness inside a
large smooth blob without moving it. The centroid was tracking a brightness distribution, not a
position. The geometric measurement is authoritative and the coupling is exact.

**Declared stylisation (Scope 11 clause carries, veto-open):** a real opening in a real ceiling does
not slide its pool across the floor when you walk. One constant per axis (`0.030` slide, `0.085°/m`
lean, clamped 2.6°), labelled a stylisation rather than dressed up as physics.

### 1.6 ⚑ THE HONEST FAILURE — the circle-beam is a slab, and it is routed to Matt

All from shipped constants (lamp 15.0 m and energy 22.8 are **Matt-LOCKED and untouched**; the
ceiling plane is the room's own wall course because the room has no ceiling mesh):

| | width | height | **aspect (h/w)** |
|---|---|---|---|
| **CIRCLE beam** | 6.93 m | 3.01 m | **0.43 — a slab** |
| **SLAT beam** | 0.78 m | 3.01 m | **3.84 — a column** |

**The slats deliver the D4-cathedral / GD light-well read; the circle cannot, and no constant I own
fixes it.** The three levers all cost something that is not mine to spend: lowering the lamp changes
irradiance 14× at fixed energy (an energy re-tune, forbidden); narrowing the cone shrinks a pool Matt
has already seen and liked; raising the apex above the wall line puts deliberate light in the void and
retires a containment guarantee that cost E3 three failures. **Fork for Matt:** (A) accept the wide
low circle-beam as a large oculus honestly rendered — *conductor-visible default, and what ships*;
(B) narrow the circle's aperture so it reads as a column, accepting a smaller pool; (C) let beams rise
above the wall line, accepting light in the void.

⚑ **Tilt raised 14° → 24°, with its cost measured not hidden:** the lean the eye actually gets over
the visible shaft goes 0.75 m → **1.34 m** (visually vertical → visually diagonal, which is the
ruling). The cost is that lamp-to-pool distance grows by `1/cos(tilt)`, so pool irradiance falls
**×0.886**. That is a consequence of a *ruled geometry change*, not a re-tune of the locked energy.

### 1.7 Two of my own constructions died to their own renders

**(a) Single-surface sampling.** The first beam sampled once per pixel at the proxy's far surface,
weighted by an analytic chord, and I wrote in the shader header that its error would be "a smooth
interior gradient, not an edge artefact". The isolated beam render said otherwise: **the circle-beam
was cut clean in half by a razor-straight vertical line and two of the five slat-beams did not render
at all** — the volume was terminating on a line belonging to the *proxy*, not to the beam. An edge
artefact, on the one property Matt ruled on. Replaced by the ray march.

**(b) Divide-and-clamp normalisation.** Normalising accumulated path by a reference length and
clamping means any ray longer than the reference saturates to white. The beam is up to 7 m *wide* and
3 m tall, so a low camera looks *along* its width and every such ray clipped: the first low-camera
render was a featureless white cloud, **2.80 % of all pixels saturated**. Replaced by Beer–Lambert.

**(c) A shader that did not compile, caught by the picture before the log.** Godot 4.6 removed the
`DEPTH_TEXTURE` built-in; the shader failed to compile and Godot fell back to a default material —
which is `blend_mix`, so the proxy cylinder rendered as a **dark opaque ellipse stamped over the
floor**. The render caught it as **148,960 pixels measured DARKER than the no-beam control, which an
additive volume can never be**; the log then named it. Fixed with `hint_depth_texture`, plus a guard
on the reverse-Z far plane, because an unguarded reconstruction divides by ~0 and **NaN silently
defeats every `<=` test below it**.

### 1.8 Beam energy — solved on a ladder against PATTERN SURVIVAL

The failure an energy causes is a *blown* beam with the aperture's structure cooked out, so the metric
is standard deviation inside the circle-beam's box (structure) beside saturated-pixel count:

| `SKY_SHAFT_ENERGY` | region mean | **std (structure)** | saturated px |
|---|---|---|---|
| 0.55 | 81.20 | 41.59 | 14 |
| **0.72 — SHIPPED** | 85.21 | **47.42** | 25 |
| 0.85 | 87.82 | 51.18 | 23 |

Structure *rises* with energy and saturation stays negligible, so **this ladder does not bound the
value from above** — said plainly rather than dressed up as a solve. 0.72 is the middle rung that
reads as "clearly lit" without pressing the low-camera case that `density` bounds.

⚑ **No per-slat energy scaling ships, and that is a measurement not an omission:** the shutter mask is
a *multiplier* on the same lamp, so where a slit is open the slat delivers the same peak irradiance
the circle does. "Same energy family" is satisfied by construction at 1.0; a scale factor would have
been an invented dimming. The knob exists if his eye wants one.

### 1.9 VOID-1

| state | in-room px moved | **LEAK** |
|---|---|---|
| **SHIPPED (beam + dust)** | 61,622 (17.11 % of room) | **0 px — CONTAINED** |
| CONTROL: beam apex raised 3.006 → 11.0 m | 65,301 | 0 px — **did NOT trip** |
| CONTROL: E3 density back on the unbounded global volume | 329,091 | **484,326 px LEAK** |

⚑ **The apex control CANNOT trip, and the reason is the mechanism itself:** the beam is bounded by a
cone that *converges toward the lamp*, so raising the apex makes the beam **narrower**, not wider —
at y = 11 m its radius is 1.68 m, deep inside the room. Reported as a control that cannot discriminate
rather than quoted as a passing test. The zero is earned by the second control, which proves the
instrument detects light in the void **in this exact frame at this exact camera** today.

---

## §2 — PART 2: WALLTOP-2

### 2.1 ⚑ The diagnosis overturns the brief's hypothesis, and it overturns it with zeros

The brief suspected the warm inner-lip bounce and/or a paint seam, and asked whether a screen-space
pass (SSAO?) was painting the unshaded cap. **Ablated, and the answer is nothing at all:**

| ablation | cap pixels changed |
|---|---|
| shadows + SSAO OFF | **0 — bit-identical** |
| fog OFF | **0 — bit-identical** |
| skylight OFF | **0 — bit-identical** |

`render_mode unshaded` behaving exactly as its header promises. **No screen-space pass touches this
surface**, so the "shadow band" is not a shadow and never was. The bands are PAINT — specifically the
**stone texture's own mortar coursing**:

- the cap is 0.45 m deep and samples `stone_tex` on a world-XZ UV at a 1.125 m period, so it traverses
  exactly **0.400 of ONE TILE** across its whole width, at whatever phase the world position lands on;
- `Brick_Small_01.png` swings **3.73×** in row-mean luminance over the worst 40 %-of-a-tile window;
- the rendered cap swings **4.07×** (L 57.04 bright vs 14.00 dark).

The texture's own contrast, arriving on the cap as a stripe. A "uniform band" is *impossible* while
the cap carries a third of a brick course stretched across its entire width. (INTEGRATE-PREP flagged
this constant and declined it as a masonry change on a just-accepted wall — correct then; it is now
the ruling's own subject.)

### 2.2 Shipped, and what each constant carries

| constant | before → after | why |
|---|---|---|
| `walltop_stone_flatten` | 0.0 → **1.0** | the band mismatch itself; flattens to the reference brick's own measured mean — **the same constant `_build_walltop_cap_mat` already hands atlas-only kits as their solid fallback**, so a flattened tiling cap and an atlas cap now land on the same value for free |
| `walltop_bounce_level` | 0.075 → **0.0** | the warm inner-lip strip, RULED OFF. Term retained at 0.0 — a ruling is not a deletion |
| `split_frac` | 0.50 → **0.50 + feather = 0.64** | at split 0.50 the ramp was *centred* on the midpoint and 14 % of the lit band was already fading — that is the "intermediate gradation". Now the ENTIRE inner half is uniform and the dissolve owns the outer half |
| `walltop_sky_level` | 0.62 → **0.685** | solved on a ladder (below) |

**`sky_level` solved against a measured referent, not raised until it looked right.** Target = the
luminance of the strip Matt called "totally daylight-bright" (**L 57.04**), so the band whose
*brightness* he endorsed becomes the whole band:

| `sky_level` | uniform-band mean L |
|---|---|
| 0.68 | 56.80 |
| 0.73 | 58.98 |
| 0.78 | 61.06 |

43.6 L per unit ⇒ **0.685 → 57.02 predicted; 56.89 measured.** Within 0.26 % of target.

### 2.3 Result, and the guarantee

| | uniform-portion L | **contrast** |
|---|---|---|
| BEFORE | min 13.86 max 57.04 mean 25.52 | **4.12×** |
| **AFTER** | min 55.84 max 57.54 mean 56.89 | **1.03×** |

**One band, spread 1.71 L = 3.00 % of its mean, then the void dissolve.**

⚑ **The dissolve guarantee is structural AND measured.** Everything moves the tint or the *start* of
the ramp; `black_point` is still 0.0 and the ramp still completes strictly inside the cap
(`0.64 + 0.14 = 0.78 < 1.0`), so `v_t ∈ [0.78, 1.0]` is `stone × 0.0` — exactly zero, arithmetic.
Measured with **glow disabled**: the 14 px immediately outboard of any pixel the paint moves —
22,400 samples — **0 px above 1/255, max channel 1.0**. With glow on the same band reads ≤5/255,
and that belongs to the post-process stage, not to this shader (the INTEGRATE-PREP glow lesson,
re-applied rather than re-learned).

---

## §3 — PART 3: CRIT-RED

### 3.1 ⚑ DISCOVER FIRST — and the trace CAN tell

`crit` (bool) and `crit_multiplier` are present on **100 %** of `damage` events. Censused, not assumed:

| battery | crits / damage events | traces with ≥1 | multipliers |
|---|---|---|---|
| WR3 after (165 traces) | **145 / 10,581 = 1.37 %** | 83 | all exactly 1.5 |
| WR2 after (450 traces) | 524 / 40,512 = 1.29 % | 248 | all exactly 1.5 |
| **THE WATCH TRACE** (wr3_after / pre / boss / B / 74000802) | **1 / 69** | — | 1.5 |

The watch's single crit is at **tick 363, t = 36.300 s** — a player cone hit on the boss for 299.94.
**It fires, it renders, and the run log says so:**

```
[wr2] CRIT-RED t=36.300  source=gd-werewolf-kitcal-1 -> target=boss&…  delivered=299.94  x1.5
[wr2] CRIT-RED: 1 crit of 30 damage events painted red (3.33%); `crit` key absent on 0 events
```

⚑ **A census printed on EVERY run**, so "no red numbers appeared" is never ambiguous between *the
fight had no crits* (data) and *the colour path never ran* (defect); a trace with no `crit` key raises
a warning naming the count. Absence is data; a silent zero is not.

⚑ **An inherited claim now measured rather than trusted.** The baton §3(6) comment asserts mob crits
are a structural zero. The census agrees exactly: player-dealt **145/9,157 = 1.58 %**, mob-dealt
**0/1,424 = 0.00 %**. Consequence stated plainly: **red can only ever appear on a DEALT number.** A
red received number would be a bug, not a rare event — and the code push-warns if one ever appears.

### 3.2 Colour, and its one weak edge declared

`COL_CRIT = (1.00, 0.12, 0.10)`. Separation from every colour a floater already uses:

- vs **chaos** (0.72,0.45,0.95) — *this fight's element*: hue 285° vs 2°. Unmistakable.
- vs **fire** (1.00,0.45,0.20): hue 19° vs 2°, far less saturated in red.
- vs **COL_RECEIVED** (1.00,0.42,0.38): hue 4° vs 2° — ⚑ **nearly the same hue.**

Separation from received salmon is **not** carried by hue. It is carried by saturation (0.88 vs 0.62)
and — load-bearing — by two structural cues that cannot coincide with a crit: a received number
carries the leading diamond and renders at `NUM_EM_FRAC_RECV`. A crit never does, and by the census
above never can. Declared here rather than left for someone to trip over.

**The pop is NOT touched.** The brief allowed a stronger crit pop "if free". It is not free:
`NUM_POP_PEAK` is a Matt-ACCEPTED envelope, and a second louder envelope would put a second variable
into a change he ruled as a *colour* change. Bangers stays at **font_size 135 / outline 27**.

---

## §4 — Guards

| guard | result |
|---|---|
| collision check at cell start (`git status`) | **clean** — tracked tree empty |
| `project.godot` sha256 start = end | `6bef17eb…` — **NO DELTA** |
| `walltop_void_radial` / `walltop_occlude` shaders | `2710fc11…` / `d29a01be…` — **unchanged** |
| all `vfx/ambient/pp/*.tres` (Matt-accepted rise + hue) | rollup `4c6a43b3…` — **byte-identical start to end** |
| kit textures (4, incl. both atlas kits) | **unchanged**, all four |
| Bangers font + OFL | `4160a731…` / `630dd5a3…` — **unchanged** |
| ref mp4 `tmp/wr2/wr3_after_pre_boss_B_74000802.mp4` | `910063d1…` — **intact** |
| traces | **READ-ONLY** — opened for census only; zero fight/trace semantics moved |
| engine tree | **never written** |
| protected dirs | no prior cell's deliverables written; this cell writes only `tmp/sky2/` |
| godot commit | **LOCAL, ahead 8, NOT pushed** |
| **declared authorised surfaces** | `scripts/sky_shaft.gdshader` (new) · `scripts/sky_dust.gdshader` (new) · `scripts/walltop_void.gdshader` · `scripts/kit_replica_level.gd` · `scripts/wr1_level.gd` · `scripts/wr2_playback.gd` · `scripts/run_wr2_playback.sh` (log filter) |

### 4.1 ⚑ LSTAT-2 — authorised delta, declared not smoothed

| | value |
|---|---|
| L7 stage sha | `5f92aa91…` → **`5d4fa240…`** |
| px changed | **116,583** of 921,600, max channel delta 55 |
| mean luma | 22.898919 → **23.349629** (**+0.450710**) |

Entirely WALLTOP-2 (the L7 stage carries wall caps; the beauty flags that gate the skylight default
off there). Same class as INTEGRATE-PREP's authorised −0.418 — and note the datum is now back within
0.03 of its pre-INTEGRATE-PREP value (23.317 → 22.899 → 23.350), because the dark band that cell
created is the band this ruling removes. Peelable with `walltop_daylight = false`.

---

## §5 — Deliverables — `~/Games/reincarnated-godot/tmp/sky2/`

**M-EYE, MOTION FIRST:**

1. **`clips/SKY2_room_judge_motion.mp4`** — the room with the full SKY-2 pattern in motion at the
   grading camera: circle in the top half, five slat-blades in the bottom, the player crossing them.
   **The one to watch for layout + beam crispness + parallax.**
2. **`clips/SKY2_playerlock_crossing_beams.mp4`** — the same segment at the game camera, where the
   player actually walks through the beams.
3. **`clips/CRITRED_t36.3.mp4`** — the crit window, red numeral in Bangers.
4. **`clips/WTSWEEP.mp4`** — the cap swept along its length (one still cannot show a band is uniform
   *for the length of the wall*).

**PLATES:**

5. **`plates/PLATE_walltop2_before_after.png`** — three bands (contrast 4.12×) above, one band
   (1.03×) below. **Fastest read in the cell.**
6. **`plates/PLATE_crit_red_vs_normal.png`** — the non-crit chaos numeral beside the crit numeral,
   same font, same size, colour the only variable.
7. `measure/beam_only3.png` — the beam ISOLATED (full minus pools): the oculus's ring and spokes and
   five discrete slat-blades, each carrying dust.
8. `measure/cal_overlay.png` / `measure/thin_overlay.png` — the coupling calibration.

**INSTRUMENTS + ARTEFACTS:** `sky2_probe.gd`/`.tscn`/`run_sky2_probe.sh` (iteration harness, five
cameras incl. the top-down coupling and cap-census poses) · `mask_cal.gd`/`.tscn` (the isolated
projector calibration) · `coupling.py` · `lstat_rig.gd` · `measure/void_*.json` · `l7/` · `logs/`.

**PEELS:** `--no-skylight` (whole family) · `--no-parallax` · `--skyceil <m>` (VOID-1 control) ·
`sky_beam` / `sky_dust` (level flags) · `walltop_daylight = false` (whole walltop ruling) ·
`walltop_stone_flatten = 0.0` / `walltop_bounce_level` (per-constant) · `COL_CRIT` (one constant).

---

## §6 — At Matt's eye

1. **THE CIRCLE-BEAM ASPECT FORK (§1.6).** Slats read as columns (aspect 3.84); the circle is a slab
   (0.43) and no constant I own fixes it, because the room has no ceiling above 3.006 m and the lamp
   height is welded to the locked energy. (A) accept — *ships today*; (B) narrow the aperture, smaller
   pool; (C) beams above the wall line, light in the void.
2. **THE WALLTOP.** One uniform band at L 56.89 against the L 57.04 strip you called daylight-bright;
   contrast 4.12× → 1.03×. The dissolve is bit-exact and now measured with glow off.
3. **THE CRIT.** Exactly one in this fight, at t = 36.300 s. If crits should read *louder* as well as
   redder, the pop is one constant — deliberately not moved, because you ruled a colour.
4. **PARALLAX IS A DECLARED STYLISATION** (Scope 11 clause), one constant per axis, veto-open.
5. **⚑ FLAGGED TO SHADOW-UNIFY (Scope 13), not fixed here:** a spot with a projector and
   `shadow_enabled = false` renders **zero light**. That cell retires spot shadow-casting — if it
   switches the skylight's shadow off without care, **the pools vanish with the shadows.**

---

*I built a beam that was correct in its geometry and wrong in its sampling, and the picture told me
before the arithmetic did. Then I built three instruments to prove the beam landed on its pool, and
all three were measuring two skylights at once. The one that finally answered had a floor, a lamp and
nothing else in the room — which is what I should have built first.*
