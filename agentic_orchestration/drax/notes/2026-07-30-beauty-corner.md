# BEAUTY-CORNER — the room answers light now, and two of my own rules died to the measurement

> **Cell:** BEAUTY-CORNER (E1 player-light bake-off · E2 armour-grade shadows · E3 shadow-haze fog ·
> E4 per-room skylight). **Agent:** drax (presentation seam). **Conductor:** gandalf
> (LR/presentation session). **Date:** 2026-07-30.
> **Contract of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` — Scope 6 (decomposition)
> · Scope 7 (Matt's rulings: bake-off / shadows / fog) · Scope 8 (fold-directive + hand-off manifest)
> · Scope 9 (skylight) · all landing blocks.
> **Inherited:** godot `ec9acbc` LOCAL (ahead 5). **Shipped:** godot `5b05947` LOCAL (ahead 6, NOT
> pushed). Prior cells this session: AMB-REFIT · AMB-RISE · CAM-LOCK · AMB-HUE · WALL-FIX+NUM-POP.

---

## §0 — What this cell says in three sentences

The room now carries a carried light, cast shadows, a bounded haze and a per-room skylight, and every
one of the four peels off with one boolean. **Two rules I wrote myself were killed by measurement
before they shipped** — the corner-only shadow subset (which measured *zero* shadow at the room
centre) and the global fog volume (which leaked 404,439 pixels into the void) — and both rejected
rules are on record in the source with their numbers. **The armour-silhouette standard cannot be
discharged in the WR3 watch at all, because the combatants in it are capsules**, so it is answered on
a probe that stands a rigged armoured figure in the same room under the same constants.

---

## §1 — E1: the player-light BAKE-OFF (Matt ordered the A/B)

### 1.1 The two arms, stated as what differs

| | static centre | carried light | E2/E3/E4 |
|---|---|---|---|
| **ARM B** (baseline, and the shipped default until Matt rules) | `pool_energy_scale = 1.0` — **exactly as PC-LIGHT left it, zero changes** | none | ON |
| **ARM A** | dimmed to **45%** | warm `OmniLight3D`, energy 5.2, range 9.0 m, atten 1.35, chest height 1.55 m, **shadow-casting** | ON |

The dim is **part of the arm, not a second knob**. Matt ruled "layers on top" (GD does both), not
"replaces" — so 0.0 was wrong; but at 1.0 the centre stays the brightest thing everywhere the player
is not, and the A/B stops being a test of the carried light. 0.45 is the value at which the carried
light is the brightest thing *near the player* while the room's middle is still a room.

### 1.2 Same-frame following — and it costs nothing

The brief asked for the light to follow the interpolated position "same-frame like the camera lock".
The camera needs an explicit late update because it is a **sibling** of the proxy. The light does not:
it is a **child of the player's body node**, so it inherits the interpolated transform in the same
assignment that places the proxy. There is no second code path that could drift, and no frame on which
the light can be a tick behind its body. Parenting *is* the guarantee.

### 1.3 The arms characterised as numbers, not adjectives

Mean floor luma in annuli around the player's measured screen anchor, averaged over frames 60/90/120/150
of the hit-dense window, `player_lock`:

| annulus | ARM A | ARM B | A − B |
|---|---|---|---|
| 0–80 px (≈ the player's own 2 m) | 98.39 | 78.09 | **+20.31 (+26.0%)** |
| 80–180 px | 79.45 | 74.63 | +4.82 |
| 180–300 px | 59.23 | 61.09 | −1.86 |
| 300–520 px | 32.36 | 35.53 | −3.17 |
| **near/far gradient** | **3.040** | **2.198** | **+38.3% steeper** |

**Arm A moves 26% more light onto the player and takes ~9% off the far field; the gradient centred on
the player is 38% steeper.** That is the lantern grammar as arithmetic. Room-wide, arm A is *darker*
than arm B (43.877 vs 46.865 lit-mean, §5) — the dim is real and it is the trade Matt is judging.

**Warmth (1.00, 0.66, 0.34)** is conductor-leaned and veto-open — slightly less orange than the
sconces' (1.00, 0.62, 0.30) so a viewer can tell the carried light from a torch. The cool variant is
one constant (`PLIGHT_COLOR_COOL`, present and unused).

### 1.4 ⚑ THE FLOOR MATERIAL — this cell's ONE authorised surface change

**BEFORE → AFTER, exactly:** `roughness 0.900 → 0.640` on **floor tiles only**. `specular` and
`metallic` **unchanged**. Albedo, texture, cull mode, and the texture file itself **untouched and
hash-verified** (`Floor_Tiles_01.png` `e28e6bcc…` start = end). Walls, pillars, toppers, torches and
the WALL-FIX brick band all still take `_apply_single_tex` at 0.9.

It is a **separate material cache key** (`mat_sheen:<rough>:<path>`), and that is load-bearing: the
wall takes the same function, and on every ATLAS kit (dungeon-realms, dwarven-dungeon)
`tex_floor == tex_wall`, so a shared key would have handed the sheen to the walls — silently, and only
on some kits.

**The value was solved on a ladder, and the ladder said something I did not expect.** Sheen isolated as
a diff against the 0.90 baseline at the `player_lock` camera:

| roughness | lift mean | lift max | **pixels lifted** | strong-lobe px |
|---|---|---|---|---|
| 0.75 | 5.00 | 25.1 | 41,632 | 119 |
| **0.64 (SHIPPED)** | 7.99 | 29.2 | **63,321 ← maximum** | 7,150 |
| 0.50 | 14.08 | 63.6 | 56,304 | 18,455 |
| 0.35 | 25.21 | 141.9 | **29,980 ← collapse** | 14,188 |

**The lit AREA peaks at 0.64 and then falls as the lobe tightens.** Below it the energy concentrates
into a small hot disc — which is exactly the plastic signature, arrived at by measurement rather than
by squinting. *A sheen is area; a plastic highlight is peak.* 0.64 is the area maximum.

`specular` is deliberately NOT raised: it scales F0, i.e. it is a claim that this floor is polished.
Concentrating the existing energy is the honest edit; adding energy is not.

---

## §2 — E2: shadows, and the subset rule I got wrong

### 2.1 ⚑ MY OWN RULE DIED TO ITS OWN CONTROL

The brief: *"If all twelve torches casting produces noisy overlap, choose a casting subset and declare
the judgment."* I wrote the subset first — four corner fixtures cast, eight wall-midpoint fills do not
— with a plausible paragraph about eight overlapping half-strength silhouettes smearing into an
unreadable blur. **Then I measured it, and shipped the opposite.**

| figure standing | 4 casters (corners) | 12 casters (all) |
|---|---|---|
| **beside a corner torch** | depth 32.6% (p95 53.4%) | depth 34.8% (p95 59.3%) |
| **at the ROOM CENTRE** | **0 shadowed pixels** | 15,103 px, depth 56.6% |

Two findings, both fatal to the subset:

1. **The overlap never happens.** At `omni_attenuation = 1.55` a lamp 2.4 m away outweighs one 11.9 m
   away by ~85×. Inverse-square with a 1.55 exponent does not make democratic light. One dominant
   silhouette in *both* arms — no fan, no smear, no second edge. The arithmetic I should have done
   first.
2. **Corner-to-centre in a 37.5 m room is 25.31 m; the scaled sconce range is 18.21 m.** The four
   corner fixtures **do not reach the middle of the room**. A corners-only rule gives a body standing
   where the fight actually happens *no cast shadow at all* — and I would have shipped that on a
   reasoned-sounding paragraph.

**Generalisable corollary, named because it will recur:** a light that ILLUMINATES but does not OCCLUDE
is fill that ERASES shadows. That is why adding casters made the corner case *deeper* (32.6% → 34.8%)
rather than shallower. The subset switch (`shadow_caster_mode`) is **kept, not deleted** — it is the
instrument that produced these numbers.

### 2.2 Resolution — spent freely, and aimed

An omni shadow is a **cubemap**: six faces from one atlas tile. Godot's default (4096 atlas, quadrant
subdiv 1/2/4/8) yields ~128 px per cube face across a full 90° field; a 0.25 m Synty pauldron seen from
5 m is 2.9° of that field = **~4 texels**. The old renders were not badly biased, they were
**unresolved**.

Shipped: **8192 atlas, 32-bit, quadrant subdivisions (1, 4, 16, 64)** on the root viewport. Quadrant 0
is one 4096 tile → **~2048 px per cube face**; the same pauldron now spans **~66 texels — 16× linear**.
Godot assigns quadrant 0 by screen-space importance, so under `player_lock` it goes to the torch the
player is passing — precisely the lamp Matt's sentence is about.

### 2.3 Bias and blur — the two-sided failure, swept

| bias | main silhouette area | perimeter | P²/A (edge detail) | acne blobs | acne px |
|---|---|---|---|---|---|
| 0.004 | 102,277 | 3,588 | 125.87 | 353 | 1,873 |
| 0.012 | 102,254 | 3,589 | 125.97 | 293 | 1,260 |
| **0.028 (SHIPPED)** | 102,222 | 3,590 | **126.08** | **173** | **828** |
| 0.060 | 102,098 | 3,606 | 127.36 | 88 | 688 |
| 0.120 | 101,925 | 3,635 | 129.64 | 79 | 661 |

0.028 removes **56% of the acne for 0.05% of silhouette area and 0.17% of the edge-detail ratio**.
Above it the acne return diminishes while the boundary starts getting ragged (perimeter climbing on a
shrinking area is raggedness, not detail). `shadow_normal_bias` is held **LOW at 1.0** (vs the 2.0
default) on purpose: normal-bias pushes samples along the surface normal and is precisely the knob
that eats fine edges — the acne budget is spent on depth bias, which does not.

`shadow_blur` **0.35** (Godot default 1.0). Godot's default is authored to hide low-resolution
stair-stepping — a defect-concealer, and at this atlas there is no defect left to conceal. Measured
silhouette-edge gradient: 8.498 at blur 1.0 → 9.329 at blur 0.0 (**+9.8%**). Declared honestly: blur
is **not** the dominant softness term (see §2.5); it is worth ~10% and it is free.

### 2.4 What does NOT cast, and why each was named rather than left

- **The centre pool.** A 32 m-reach lamp at the room centre would throw every body's shadow radially
  outward — a second contradictory direction from a fixture that does not exist. Fills do not cast.
- **The instrument overlays** (facing nub, footprint ring, identity stalk, HP bar). Not cosmetic: the
  player's stalk is a **9 m column**, and under a corner torch it would have laid a **fifteen-metre
  black bar** across the floor. Godot defaults every `MeshInstance3D` to casting, so this had to be
  switched off explicitly.
- **Every particle system** — torch flame, embers, and the five ambient layers. A billboard rendered
  into a shadow map is an opaque card that swings to face the camera; on the flames that is a black
  rectangle under every torch, cast by a light 0.36 m from the emitter. Handled in `_fx_sys()` for
  builder-made systems and by walking the instanced `room_ambient.tscn` for the scene-made ones (the
  Matt-verdicted ambient **resource** is untouched — rise, hue and alpha ramps byte-identical).

### 2.5 ⚑ CONTACT ANCHORING: SSAO, and the call declared

**Call: SSAO** (radius 0.65 m, intensity 1.1, power 1.6, light_affect 0.15). The alternative — lean on
the cast shadow alone — fails at exactly the case the rider names: a body in a region no torch reaches
casts **nothing**, and floats. SSAO is view-space and lamp-independent, so it darkens the floor-to-body
crease whether or not a lamp is present. Radius is **smaller than every proxy in the roster** (player
r = 0.5, boss r = 1.5) deliberately: a large radius reads as dirt in the room's corners, a small one
reads as *contact*.

That call is now vindicated by §2.1's second finding: at the room centre the only caster is the
skylight, so SSAO is frequently the *only* thing anchoring a body to the floor.

---

## §3 — E2's acceptance standard: the armour silhouette

### 3.1 ⚑ THE WATCH SCENE CANNOT ANSWER MATT'S SENTENCE — and not because of the shadows

`wr2_playback.gd::_build_entities()` renders every combatant as a **CAPSULE**, deliberately, and its
own comment says why: *"this roster has no rig in this project, and a mis-bound rig would be a lie of a
more expensive kind than a capsule."* **A capsule has no armour. It casts a capsule.** No shadow
setting makes a pauldron appear in the shadow of a body that has no pauldron.

So the standard is met or missed on the **shadow rig**, and it must be judged on geometry that has
armour. `tmp/beauty/armor_probe.gd` builds **the same room** through **the same class** with **the same
booleans and the same constants**, and stands `SK_Chr_King_Male_01` (the one armoured humanoid in this
project with a proven load path — `king_rig.gd`) beside a corner sconce, posed from the retargeted
base-locomotion WALK clip at a stride phase where the limbs separate. When a rigged roster lands the
watch inherits the rig unchanged and this probe becomes redundant.

### 3.2 The verdict-readiness statement — what reads and what does not

**Reads in the cast silhouette** (plate `PLATE_E2_armor_silhouette.png`): separated legs with the greave
taper, the notched skirt/tasset hem, the sword arm clear of the torso, the head-and-shoulder mass —
countable armour features against a capsule's zero, on a floor where the same figure previously cast
nothing at all.

**Does not read:** the pauldron/crown end of the silhouette at a corner torch. ⚑ **And the reason is
measured geometry, not the rig.** A point lamp at `SCONCE_H = 2.30 m` casting a 1.85 m figure projects
the crown to `d·h/(h − h_fig) = 5.11×` its distance — a **9.9 m smear** from a 2.4 m stand-off. The
far end of that silhouette is stretched fivefold along its length; that is what a low torch does to a
tall thing, in any renderer.

**Control that isolates it:** the same figure, same rig, same constants, standing in the **skylight
pool** — lamp at 15 m, projection ratio **1.14×** instead of 5.11× — casts a compact silhouette that
holds the whole figure. Same rig, an eighth of the stretch, and the detail is there.
(`tmp/beauty/probe/POOL_ARMOR_0001.png`.)

**So the honest verdict-readiness is:** the rig resolves the detail Matt asked for; the room's fixture
height limits how much of it survives the projection at a wall torch. Levers if Matt wants more, each
one constant: raise `SCONCE_H`, or accept the skylight as the detail-carrying caster. **Matt rules at
the plate.**

---

## §4 — E3: the haze, and the VOID-1 rider that failed twice before it passed

### 4.1 "Nearly imperceptible, grows in the shadows" resolves to two different settings

- *Nearly imperceptible* is **DENSITY**. Optical depth across the whole 37.5 m floor is a fraction of a
  stop — that is what "you should have to look for it" is as a number.
- *Grows in the shadows* is **NOT AUTHORED**. It falls out of the frozen `TONE_MAPPER_FILMIC` (the same
  tonemap that turned AMB-HUE's first purple pink): a fixed additive in-scatter term is a large
  relative lift against near-black and a negligible one against a torch-lit wall, because filmic
  compresses the top. Authoring a per-region density would have been the wrong instrument for a
  behaviour tonemapping gives free. Measured: **p05 1.43 → 2.35 (the dark lifts 64%), p95 82.80 → 97.79
  (the bright lifts 18%)**.

**Albedo purple-leaning** (0.620, 0.600, 0.720), judged at the eye against the accepted AMB-HUE spine —
a neutral haze read as a separate, colder system sitting *next to* the ambient rather than as the same
room's air. Held **desaturated** rather than at the ambient's 0.86: fog multiplies over every surface
including the brick WALL-FIX just landed, and a saturated volume tints masonry.

### 4.2 ⚑ VOID-1 FAILED, AND THE FIX WAS STRUCTURAL BOTH TIMES

**Failure 1 — the global volume. 404,439 leaked pixels** (mean +4.82, max +28.8). The first build put
density on the **Environment**, a froxel volume filling the whole camera frustum. The walls stop at
3.17 m with no ceiling, so torchlight rises over them and scatters outside the room. **No density is
low enough to fix that** — it is CEILING-1's class of defect in a volume: turning the density down
turns the leak and the fog down in lockstep, because they are the same number.

**Fix:** global density → **0**; the fog becomes a **`FogVolume` BOX seated on the room** (interior
footprint, floor to the wall course). A leak is then not small, it is *geometrically impossible* —
exactly the argument E4's lineage guard makes about the skylight.

**Failure 2 — the box was taller than the walls.** `FOG_BOX_TOP = 4.60` (chosen so the shaft would read
for longer) put the top 1.6 m of the box **above the wall line**, where an elevated camera sees it
against the void: **11,215 px rim**. With glow disabled the rim only fell to 8,322 — so **74% of it was
fog, not post-process**, and I could not write it off as the known glow bleed. Box top → `WALL_H`
exactly: **4,343 px**.

**Failure 3 — froxel resolution.** The residual 4,343 px was a **1.56 px-mean rim** hugging the room
silhouette: a froxel that straddles the wall edge puts room-fog on void pixels, and its bleed width is
one froxel by definition. `environment_set_volumetric_fog_volume_size(128, 96)` (Godot default 64³):

| froxel grid | in-room mean lift | LEAK |
|---|---|---|
| 64³ (default) | +12.57 | 4,343 px |
| **128×96 (SHIPPED)** | +10.66 | **0 px** |
| 256×128 | +10.01 | 0 px |

⚑ **ONE VARIABLE AT A TIME, THE SECOND TIME.** My first attempt moved `fog_length` 96 → 56 in the same
edit and the fog collapsed to mean +1.70. That was the **length** (the volume ended before the room's
far side), not the resolution. Separated, re-measured, length restored, density given back on the
bounded quantity (0.055 → 0.065) because a box density cannot leak and froxel bleed can.

### 4.3 ⚑ THE INSTRUMENT ITSELF WAS WRONG, AND THAT IS REPORTED TOO

The inherited `tmp/ambrise/void_leak.py` derives its void mask from **luma** — *"the void is where the
stage renders black."* Exact for the 17.5 m L7 stage (a small lit box on a black surround) and for a
localised element. **Wrong for fog in a 37.5 m room**: the floor has large genuinely-dark regions
between torches, they are black, the luma mask calls them void, and fog — whose whole purpose is to
lift dark pixels — registers as a "leak" made mostly of floor plainly inside the room.

I ran it, got LEAK, and **did not report it as a fog defect**, because a measurement whose mask is
wrong is not evidence of anything. New instrument: `tmp/beauty/void_geo.py` + `wr2_playback.gd`'s
`--voidmask 1`, which paints **every mesh flat unshaded white and hides the UI** — the frame is then
white exactly where geometry is and black exactly where it is not, independent of lighting, of the
unshaded void-dissolve shaders, and of what any element does to brightness.

### 4.4 VOID-1 VERDICT — the zero is earned by two controls

| state | LEAK |
|---|---|
| **SHIPPED (E3 fog + E4 skylight)** | **0 px — CONTAINED** |
| E3 fog alone | **0 px — CONTAINED** |
| E4 skylight alone | **0 px — CONTAINED** |
| CONTROL A: same density on the **unbounded global volume** | **343,833 px LEAK** (mean +3.50, max +20.7) |
| CONTROL B: bounded box, top raised 3.01 → 12.0 m | **30,310 px LEAK** (mean +15.87, max +40.9) |

Declared honestly: with the fog bounded, **density is no longer the leak axis** — the geometry is. So
the ×20-density control (which the brief's phrasing anticipated) does **not** trip, and saying so is
part of the reading. The two controls that *do* trip are on the axis that can actually fail.

---

## §5 — E4: the per-room skylight

### 5.1 The lineage guard, first, because it is the point

⚑ **This is not the deleted false sun.** CEILING-1 was an unbounded `DirectionalLight3D`, and PC-LIGHT
proved it could not be repaired by dimming (2.0 → 4.81× contrast, 0.22 → 4.19× — *worse* —, 0.0 →
28.52×). All three of its defect properties are **structurally** inverted here:

- **BOUNDED** — a `SpotLight3D` with finite `spot_range` and a finite cone; contribution outside the
  cone is exactly zero, not small. It cannot put a floor under the room.
- **MOTIVATED** — it is an *opening*. The projector mask is the aperture's shape, which is why the floor
  receives a **pattern**: a patterned pool states "there is a hole up there"; an even pool states
  "there is a lamp up there".
- **LOCALISED** — measured, not asserted: skylight-alone moves the room's lit mean by **+0.000
  (0.0%)**, touching **3,696 px** at up to +68 luma. ~2% of the floor. The other 98% is lit by fire
  exactly as before.

No `DirectionalLight3D` is added, re-enabled or touched.

### 5.2 Seed convention

Motif, azimuth, pool position, intensity and mask rotation are **all draws from one RNG seeded on
`hash("skylight:<level_seed>:<room_index>")`, in a fixed order** — so determinism is by construction,
not by four hashes agreeing.

⚑ **`level_seed` is deliberately NOT the fight seed** (`wr1_level.gd::LEVEL_SEED = 74001000`). Keying it
off the trace seed would change a room's **architecture** because a different fight was being watched.
A room's ceiling does not depend on who is fighting in it.

Shipped roll:

| room | motif | azimuth | pool (local) | energy |
|---|---|---|---|---|
| 0 trash | cracked-seam | 117.4° | (−5.03, −0.64) | 26.08 |
| 1 champion | cracked-seam | 161.7° | (−3.81, −1.96) | 21.37 |
| 2 mixed_pack | window-lattice | 20.9° | (2.24, −2.77) | 21.11 |
| **3 boss (the watch's room)** | **oculus-ring** | 180.3° | (−1.51, 2.70) | 20.69 |

⚑ **Declared:** rooms 0 and 1 share a motif. With three motifs and four rooms a repeat is guaranteed by
pigeonhole — **uniqueness lives in the operand tuple, not in the motif alone** (their azimuth, pool and
energy all differ). If Matt wants four distinct motifs, that is a fourth mask function, not a seed change.

### 5.3 Masks, energy, temperature

Three motifs **authored procedurally, LOCAL ONLY — no fetch was made and no texture file was added**:
a 3×4 mullioned **window-lattice**, an **oculus** (disc + structural ring + six spokes), and a
**cracked seam** built as a signed distance to a piecewise-linear spine with breathing width and two
branches (noise would read as dirt on a lens; a crack has to read as structure). All three carry a soft
outer vignette that kills the cone's own hard rim — without it the pattern cuts off at a perfect circle
and reads as a lamp with a gobo.

**Energy solved on a ladder**, against the room floor's own p99 (73.5 luma): ×1 → pool peak 95,
×3 → 117, ×6 → 124. **The ×6 rung buys +8 peak while tripling the lit area** — past ×3 the energy stops
making a pool brighter and starts making the room brighter, which is the false-sun direction. ×3 is the
last rung that is still a pool.

**COLD PALE (0.620, 0.740, 1.000)** — conductor lean, veto-open, one constant. It completes the
three-temperature grammar (warm torches / warm carried light / cool ambient / cold world-above), and
mechanically it is why the shaft *separates* from twelve orange sconces instead of dissolving into them.

⚑ **Accepted consequence of E3's containment:** the shaft is visible only for the ~3.0 m of its length
inside the fog box. Above the wall line it goes invisible — which is *correct*, not merely tolerated: a
visible shaft above the wall line **is** the leak, drawn on purpose. The D3 read (light arriving from
architecture you never render) works better when the beam enters frame than when it is traced to source.

---

## §6 — LSTAT-2: the authorised delta, measured and declared, not smoothed

**Guard first — the FROZEN L7 STAGE IS UNTOUCHED, and that is measured.** One edit in this cell was
unconditional (particles no longer cast). The L7 stage re-rendered at the R-6 camera, applied vs
reverted: **0 of 921,600 px, max channel diff 0, byte-identical PNG `398421737359c331…`** — the *same
hash* the WALL-FIX cell recorded. Mean luma 23.317067 both sides, Δ **+0.000000**. The no-cast edit is a
measured no-op there (alpha materials do not enter Godot's shadow pass) and a guard everywhere else.

**The authorised delta** — boss room, `arena_full` (the grading camera of record), lit pixels inside the
geometric room mask, against BASE = `--beauty off` (the state WALL-FIX left):

| state | room mean | p05 | p95 | contrast | Δ mean | px moved |
|---|---|---|---|---|---|---|
| BASE (`--beauty off`) | 34.649 | 1.43 | 82.80 | 58.100 | — | 0 |
| E1 arm A alone (light + sheen) | 32.555 | 1.43 | 77.55 | 54.414 | **−2.095 (−6.0%)** | 200,391 |
| E2 shadows + SSAO alone | 34.172 | 1.43 | 81.91 | 57.476 | **−0.477 (−1.4%)** | 25,232 |
| E3 fog alone | 46.056 | 2.35 | 97.79 | 41.558 | **+11.407 (+32.9%)** | 317,079 |
| E4 skylight alone | 34.649 | 1.43 | 82.78 | 58.082 | **+0.000 (0.0%)** | 3,696 |
| ALL ON, arm B | 46.865 | 1.64 | 98.71 | **60.273** | **+12.216 (+35.3%)** | 308,562 |
| ALL ON, arm A | 43.877 | 1.64 | 92.50 | 56.479 | **+9.228 (+26.6%)** | 302,218 |

Read, not smoothed:
- **E3 is the whole delta.** +32.9% on its own; the other three are ≤ 6% and two of them are *negative*.
- **Fog costs contrast (58.1 → 41.6) and the shadows give it back.** All-on arm B lands at **60.273 —
  higher than BASE**. The four elements are not independent in what they do to the histogram, and the
  combination is better-conditioned than fog alone. That is a real result and it argues for the stack
  as a stack.
- **Arm A is the darker arm room-wide** (43.877 vs 46.865) and the brighter arm on the player (§1.3).
  That is the bake-off, in one line.

---

## §7 — Guards

| guard | result |
|---|---|
| collision check at cell start (`git status`) | **clean** — no foreign uncommitted tracked work |
| `project.godot` sha256 start = end | `6bef17eb…ace8a` — **NO DELTA** |
| kit shaders `walltop_void_radial` / `walltop_occlude` | `2710fc11…` / `d29a01be…` — **unchanged** |
| all 16 `vfx/ambient/pp/*.tres` | **byte-identical start to end** (the Matt-accepted rise + hue) |
| kit textures `Floor_Tiles_01.png` / `Brick_Small_01.png` | `e28e6bcc…` / `5692f885…` — **unchanged** |
| **declared authorised surface** | floor **material** roughness `0.900 → 0.640`, floor tiles only, separate cache key (§1.4) |
| ref mp4 `tmp/wr2/wr3_after_pre_boss_B_74000802.mp4` | `910063d1…` — **intact** |
| frozen L7 stage | **0/921,600 px, byte-identical PNG** (§6) |
| traces | **READ-ONLY** — opened for read only; zero fight/trace semantics moved |
| engine tree | **zero writes by this cell** — never opened. (Foreign modifications are present there from another session; recorded, not claimed.) |
| protected dirs (ten) | `tmp/vmur*` `tmp/l7race` `tmp/ambfit` `tmp/ambrise` `tmp/ambhue` `tmp/camlock` `tmp/wr1` `tmp/pclight` → **0 files**. See the one exception below. |
| godot commit | **LOCAL, ahead 6, NOT pushed** |

⚑ **ONE PROTECTED-DIR WRITE, DECLARED RATHER THAN DISCOVERED.** `tmp/wr2/pl_audit.json` was rewritten at
19:30 by an early check render (the `player_lock` framing audit writes beside its own `--outdir`, and one
malformed early invocation resolved that to `tmp/wr2`). The file is **untracked scratch**; the CAM-LOCK
cell's shipped copy **`tmp/camlock/pl_audit.json` is intact and untouched** (18:14, and `tmp/camlock` shows
0 files newer than the cell-start marker), so no evidence was lost. Every subsequent render wrote to
`tmp/beauty/pl_audit.json`. Recorded because a guard that only reports the zeros is not a guard.

---

## §8 — Deliverables (M-EYE) — `~/Games/reincarnated-godot/tmp/beauty/`

Seed 74000802, `wr3_after` / pre / boss / B, the hit-dense opening window, 170 frames @ 30 fps,
carrying the refit + risen + purple ambient, the brick wall band and the anime damage numbers.

**THE MATT-FACING COMPARISON, FIRST:**
1. **`clips/BAKEOFF_armB_left_armA_right.mp4`** — the E1 A/B pair. Same segment, same camera
   (`player_lock`), arm B left, arm A right. **This is the one Matt asked for.**
2. `clips/BEAUTY_armA_playerlock.mp4` · `clips/BEAUTY_armB_playerlock.mp4` — each arm alone, clean.

**THE INTEGRATED PREVIEW:**
3. `clips/BEAUTY_BEFORE_top_AFTER_bottom.mp4` — the WALL-FIX state above, the full stack (arm A) below,
   same frames. *Not the hand-off watch* — that renders after Matt's verdicts, carrying everything accepted.

**PER-ELEMENT PLATES:**
4. **`plates/PLATE_E2_armor_silhouette.png` — REQUIRED, and the one to read against Matt's sentence.**
   Shadows off / shadows on / zoom on the near half of the silhouette.
5. `plates/PLATE_E1_bakeoff_A_vs_B.png` — the two arms, one frame, with the annulus numbers.
6. `plates/PLATE_E1_floor_sheen_ladder.png` — 0.90 / 0.64 / 0.35, the area-maximum argument.
7. `plates/PLATE_E3_haze_in_shadow.png` — fog off vs on, with the p05/p95 lift.
8. `plates/PLATE_E4_skylight_two_rooms.png` — boss-room oculus and room-2 window-lattice: **per-room
   uniqueness from the same code and two integers.**
9. `plates/PLATE_VOID1_contained_vs_controls.png` — the zero beside the two controls that trip.

**MEASUREMENT ARTEFACTS:** `void/*.json` (nine VOID-1 readings) · `lstat_ladder.{txt,json}` ·
`l7/l7_{BEFORE,AFTER}.png` (the byte-identical pair) · `probe/` (armour + skylight probe frames) ·
`logs/`.

---

## §9 — Reproducibility

- `scripts/kit_replica_level.gd` — `_apply_beauty_fog` / `_build_fog_volume` / `_apply_beauty_contact` /
  `_arm_shadow_omni` / `_arm_shadow_spot` / `_sconce_casts` / `_build_skylight` / `_skylight_mask` /
  `_apply_floor_sheen_tex`
- `scripts/wr1_level.gd` — pass-throughs + `LEVEL_SEED` + `_no_cast_recursive`
- `scripts/wr2_playback.gd` — `_beauty_shadow_atlas` / `_attach_player_light` / `_paint_void_mask`
- `tmp/beauty/armor_probe.gd` + `.tscn` + `run_armor_probe.sh` — the E2 acceptance instrument
- `tmp/beauty/void_geo.py` — VOID-1 with a geometric mask
- `tmp/beauty/lstat_rig.gd` + `.tscn` — the frozen-L7 guard, at the R-6 camera
- Renders: `OUTBASE=tmp/beauty CAM=player_lock FRAMES=170 EXTRA="--playerlight A" bash scripts/run_wr2_playback.sh wr3_after pre boss B 74000802 BEAUTY_armA`
- Peel any element: `--no-shadows` · `--no-fog` · `--no-skylight` · `--no-sheen` · `--playerlight B` ·
  or `--beauty off` for the whole family.

---

## §10 — At Matt's eye

1. **THE BAKE-OFF.** Arm A carries +26% light on the player and a 38% steeper gradient, at the cost of
   ~9% of the far field and a room that is overall darker. Arm B is the room you already accepted.
   One word either way; the loser costs one constant to remove.
2. **THE ARMOUR SILHOUETTE (§3).** What reads: legs, greaves, tassets, arm. What does not: pauldrons at
   a wall torch, because a 2.30 m lamp stretches a 1.85 m figure 5.11×. **And the watch's own
   combatants are capsules** — this is answered on a probe until a rigged roster lands.
3. **The fog's 32.9%** — it is the whole LSTAT-2 delta and it is authorised by design. If it reads as
   too much, `FOG_VOLUME_DENSITY` is one constant; the containment does not move with it.
4. **Skylight temperature and motif repeat** (§5.2/5.3) — cold pale is a lean, veto-open; rooms 0 and 1
   sharing `cracked-seam` is pigeonhole, and a fourth motif is a function, not a seed.
5. **The south wall — STILL FLAGGED, and now with its reason.** My skylight work did not touch it, so
   per the brief it stays flagged. The reason it is not cheap: `walltop_void_radial.gdshader` is
   `render_mode unshaded` **by design** — its own header says *"UNSHADED so the gradient is fully
   controllable (lighting can't lift the outer black)."* Making it shaded so it receives this cell's
   shadows would let torchlight lift the void-black the dissolve exists to guarantee. It is a design
   conflict, not a patch.

*I wrote a shadow rule and a fog volume that both sounded right, and the room disagreed with both.
The room is the one holding the light, so the room wins.*
