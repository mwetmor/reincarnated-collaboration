# SHADOW-UNIFY — one author, and a gate whose two clauses pull against each other

> **Cell:** SHADOW-UNIFY (BR-1 BATON-RENDER §3 cell #4) — the full lighting cosmology:
> one shadow author on the one-sun vector, torches/lamps/carried light non-casting, the
> centre light retired, the pools-vanish landmine reconciled, the silhouette fix, the
> fog-unlit A/B, and the boss-beam crossing captured.
> **Agent:** drax (presentation seam). **Conductor:** gandalf (`RUN-CONDUCTOR`). **Gate:** G-3.
> **Date:** 2026-07-31.
> **Contract of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` — **Scope 13**
> (unified shadow grammar) · **Scopes 15/16/16-b** (centre light RETIRED, D1-esque carried light)
> · **Scope 19** (one sky direction + fog-unlit comparison) · **Scope 20** (camera, staticity,
> one sun) · the **BEAM-FIX / BEAM-CONE / RIVAL-CAST** landings.
> **Acceptance source:** `galadriel/notes/2026-07-30-shadow-cal.md` §3.
> Charter: `gandalf/notes/2026-07-31-baton-render-run-charter.md` (G-3).
> **Inherited:** godot `b80d7d9` LOCAL (ahead 12). **Shipped:** godot LOCAL (ahead 13, **NOT pushed**).

---

## §0 — The cell in six sentences

**The cosmology lands and its census is exact: ONE DirectionalLight3D authors every combatant
shadow, aimed by the same expression the beam patterns are graded against, so shadow azimuth and
shaft lean are one vector with a printed deviation of 0.000000° — and the scene contains ZERO
non-directional shadow authors out of 71 lights.** **The pools-vanish landmine is real, was fired
on purpose, and is now a number**: `shadow_enabled = false` on the sky projector spots costs the
floor pool **56.3 % of its p99** (55.36 → 24.18 on a frozen footprint), while the shipped
reconciliation — shadow machinery alive at `shadow_opacity = 0` — leaves the pool at **1.028× the
inherited state**. **The silhouette fix is measured on the question that actually matters** ("is the
hero brighter than the pool he stands in?"): the inherited torso lamp returns **1.016×** — a shape
with no separation, exactly RIVAL-CAST's silhouette — and moving the lamp out of the body returns
**1.540×**; the carrier fill was built, measured at **+0.6 %**, and NOT shipped. **⚑ G-3's headline
clause PASSES at 9.6 % against ~10 % and the margin is honest rather than comfortable, because the
gate's two halves are arithmetically opposed**: ρ = 1 − (the author's share of the local floor), so
deepening the shadow toward SHADOW-CAL's ~0.50 necessarily widens the bright-vs-dim disagreement —
the ladder crosses 10 % between key energy 1.0 and 1.4, and **holding ρ ≈ 0.50 at ≤10 % agreement
would require a room whose bright:dim floor ratio is ≤ 1.11, where ours measures 1.47.** **The
inherited state FAILS the same gate at 10.2 %, and fails it far worse on the shadow's own shape —
its shadow AREA swings 92 px to 43,935 px between two tiles of one room (478×), because a different
lamp authors it in each place.** **Five of my own instrument failures are written down, one of them
a NULL control that came back with 20,757 differing pixels and a shadow set whose bounding box was
the entire frame.**

---

## §1 — GATE G-3, clause by clause

**Tolerances named before the measurements:** (a) bright-tile ρ and dim-tile ρ agree within **10 %**
(SHADOW-CAL §3's own suggested check, verbatim); (b) **zero** non-directional shadow authors;
(c) floor pools within **±10 %** of the BEAM-CONE state on p99 **and** on footprint total.

### 1.1 ONE AUTHOR — the census, from the built scene rather than from the source

```
[kit_replica] SHADOW CENSUS (UNIFIED): 71 Light3D in scene
  | DIRECTIONAL authors 1 ["Key (DirectionalLight3D, E=1.000, op=1.00)"]
  | NON-DIRECTIONAL authors 0 []
  | shadow-machinery-alive-at-opacity-0 8 ["Lamp (SpotLight3D, E=34.320, op=0.00)", ... ]
```

It is a **tree walk, not a promise**: `KRL.print_shadow_census()` enumerates every `Light3D` in the
built four-room level and reads its shipped properties back off the node. A grep of the source
proves what the source says; this proves what the scene *is*. The eight `op=0.00` spots are the
pools-vanish reconciliation (§1.3) and are reported **separately** rather than folded into the zero.

**The re-aim is a basis assignment, not a pair of Euler angles.** `Key.transform` is built from
`sun_travel_dir()` — byte-identical expression to the `want_ax` that `_sky_pool_axis_report()`
grades every beam pattern against. Printed every build:

```
travel (-0.277394, -0.913545, +0.297468) | sun az 137.000° el 66.000°
| ONE-SUN deviation from beam axis 0.000000°
```

Scope 19's law ("the sky has ONE direction in this world") is therefore not a convention somebody
has to remember — the shadow azimuth cannot be edited apart from the shaft lean.

**⚑ AND THE SHADOW LENGTH IS A CONSEQUENCE, NOT A KNOB — SAID OUT LOUD SO NOBODY LATER READS
SCOPE 13's "~1.1–1.2×" AS IF THIS CELL HIT IT.** At elevation 66° a body of height *h* lays a ground
shadow of *h*/tan 66° = **0.445 h** — player **0.801 m**, boss **1.224 m**. Scope 13's 1.1–1.2×
figure is our own E2 *projection-stretch* number, a different quantity; SHADOW-CAL §3(4) explicitly
returned CANNOT-ANSWER on a referent length ratio and told this cell **not** to tune the angle to
one. The angle belongs to the sun; the shadow follows it.

### 1.2 ρ — the instrument, and the numbers

**The peel.** Render the identical frame three times, differing only in whether the bodies enter the
shadow map:

| arm | what differs |
|---|---|
| `CAST` | as shipped |
| `NOCAST` | bodies' meshes `cast_shadow = OFF` — same lighting, same pixels, no shadow |
| `GHOST` | bodies' meshes hidden, all lights (including the carried one) unchanged — the body mask |

```
S    = { px : luma(NOCAST) − luma(CAST) > 2 }  \  body
ρ    = mean(luma_CAST[S]) / mean(luma_NOCAST[S])
```

The denominator is not an annulus standing in for the floor: it is **the same pixels with the
shadow removed.** That is the exact definition of a multiplicative shadow's ratio with nothing
estimated and no human read — the thing SHADOW-CAL had to buy at one human segmentation per sample.
**Every ladder carries a NULL control** (identical inputs, a second process launch) and every one of
them returns **0 px differing of 921,600** after the FX peel (§5.2).

**SHIPPED — unified, one author at E = 1.00, five floor tiles, CAM-LOCK 1280×720:**

| tile | local floor | shadow | **ρ** | ρ (umbra) | absolute contrast | shadow px |
|---|---:|---:|---:|---:|---:|---:|
| T1 torch wall | 122.66 | 114.55 | 0.9339 | 0.9210 | 8.11 | 2,162 |
| T2 torch corner | 104.15 | 94.25 | 0.9049 | 0.8743 | 9.90 | 1,974 |
| **T3 circle pool (BRIGHTEST)** | **130.97** | 124.37 | **0.9496** | 0.9437 | 6.60 | 2,126 |
| **T4 mid-room (DIMMEST)** | **89.01** | 76.75 | **0.8623** | 0.7890 | 12.26 | 1,897 |
| T5 open floor | 98.06 | 87.69 | 0.8942 | 0.8581 | 10.38 | 1,965 |

**ρ spread bright-vs-dim = 9.6 % → PASS** against the ~10 % tolerance. Umbra spread 17.9 %
(reported, not graded — see below).

**INHERITED (godot `b80d7d9`), the same five tiles, the same instrument:**

| | ρ span | spread | ρ_umbra span | umbra spread | shadow px span |
|---|---|---:|---|---:|---|
| **inherited** | 0.8701–0.9632 | **10.2 % FAIL** | 0.6406–0.9774 | **41.6 %** | **92 … 43,935 (478×)** |
| **shipped** | 0.8623–0.9496 | **9.6 % PASS** | 0.7890–0.9437 | 17.9 % | 1,897 … 2,162 (1.14×) |

**⚑ THE AREA COLUMN IS THE STRONGEST NUMBER IN THIS CELL AND IT IS NOT THE GRADED ONE.** Under the
inherited grammar the *same body* casts a 92-pixel nothing at the room's middle and a 43,935-pixel
smear beside a torch — a **478× swing between two tiles of one room**, because a different lamp is
authoring it in each place (E2's 5.11× torch projection stretch, doing exactly what E2 measured it
would). Under one author the area varies by **1.14×** across all five tiles. That is what "same
shadow, every room" buys, and it is visible in the right-hand column of the ρ plate without any
number attached.

**Umbra vs whole shadow, both computed, the graded one named.** `S` is the whole cast shadow
*including its penumbra*, so its mean is diluted by a soft fringe no eye reads as "the shadow";
galadriel's referent number came off a hand-segmented dark blob, i.e. an umbra. Both are in the
JSON. **The gate is graded on the whole-shadow mean — the conservative one, the one closest to 1.0 —**
so that the two cannot be silently swapped for whichever passes.

### 1.3 ⚑ THE POOLS-VANISH LANDMINE, FIRED ON PURPOSE

Method: BEAM-CONE's own peel, unchanged, bodies absent from every arm (the carried omni would sit on
top of the thing being measured), footprint **frozen on the reference arm** (249,792 px):

```
pool = NOBEAM (sky lamps on, beam MESH off) − NOSKY (skylight off entirely)
```

| arm | pool p99 | vs inherited | pool total | vs inherited | verdict |
|---|---:|---:|---:|---:|---|
| **LEGACY `b80d7d9`** (reference) | 55.364 | 1.000× | 4,271,268 | 1.000× | — |
| **SPOT mode 1 — `shadow_opacity = 0`** | **56.901** | **1.028×** | **4,422,061** | **1.035×** | **SHIPPED, PASS** |
| SPOT mode 0 — `shadow_enabled = false` | 24.176 | **0.437×** | 2,832,588 | 0.663× | **FAIL, −56.3 % p99** |

**The hazard is real and it is now a number.** Killing the spot's shadow does not extinguish the
lamp — it flattens it: p50 barely moves (12.60 → 11.16) while **p99 collapses 55.4 → 24.2**. The
*pattern* goes, which is the part of a projected church-window pool that is the pool. Mode 1 keeps
the shadow machinery alive and authors exactly zero darkening, which is why the census can report
**0 non-directional authors** and the floor can keep its pools in the same build. The +2.8 % is
explainable rather than mysterious: under the legacy arm the spot was also shadowing *the room's own
geometry* into its pool, and that self-darkening is what mode 1 removes.

### 1.4 **G-3 VERDICT: PASS on all three clauses** — 9.6 % ≤ ~10 %; 0 non-directional authors of 71
lights; pools 1.028× p99 / 1.035× total, inside the ±10 % named tolerance.

---

## §2 — ⚑ THE FINDING THE GATE WAS HIDING: its two clauses are arithmetically opposed

This is the most useful thing the cell produced and it is not a pass/fail.

A shadow authored by a single light removes exactly that light's contribution, so

```
ρ(x) = 1 − K / F(x)        K = the author's contribution;  F(x) = local floor luminance
```

ρ is a **constant fraction only where F is constant.** Let r = F_bright / F_dim and let *s* = the
author's share on the dim tile. Then the bright-vs-dim disagreement is

```
(ρ_b − ρ_d) / mean  =  s(r−1)/r  /  (1 − s(1 + 1/r)/2)
```

**Measured in this room, r = 130.97 / 89.01 = 1.471.** Solving the inequality at 10 %:

- the deepest legal shadow at r = 1.471 is **ρ_dim ≈ 0.75** — deeper than that and the gate fails;
- reaching **ρ ≈ 0.50** while holding 10 % requires **r ≤ 1.11**, i.e. a room whose brightest floor
  tile is within 11 % of its dimmest.

A crypt with twelve torches and projected skylight pools is not an r = 1.11 room and is not supposed
to be. **The empirical ladder agrees with the algebra and crosses the line exactly where it says:**

| one author's energy | ρ span | **spread** | absolute contrast | frame mean luma |
|---:|---|---:|---|---|
| 0.06 *(PC-LIGHT's cold-rim value)* | 0.938–0.957 | 2.0 % | 2.4–2.8 | 35–52 |
| 0.62 | 0.899–0.966 | 7.2 % | 4.3–8.4 | 42–63 |
| **1.00 — SHIPPED** | **0.862–0.950** | **9.6 % PASS** | **6.6–12.3** | **45–69** |
| 1.40 | 0.831–0.935 | **11.7 % FAIL** | 8.8–16.0 | 48–75 |
| 3.50 | 0.751–0.878 | 15.7 % FAIL | 18.1–29.1 | 59–100 |
| 3.50 + torches × 0.30 | 0.747–0.875 | 15.8 % FAIL | 18.5–29.3 | 50–91 |
| 6.00 + torches × 0.30 | 0.726–0.841 | 14.7 % FAIL | 25.7–37.1 | 60–113 |

**1.00 is shipped because it is the DEEPEST RUNG THAT PASSES, and for no other reason.** The failing
rung above it is in the table beside it.

**⚑ AND THE OBVIOUS FIX WAS TRIED AND DOES NOT WORK, WHICH IS WHY IT IS IN THE TABLE.** "Dim the
torches so the one author is a bigger share" is the coherent D1 move and it buys **nothing** for the
gate (15.7 % → 15.8 %), because the largest source of floor inhomogeneity in this room is not the
torches — it is the **cold sky pool**, which is bright, non-casting, and therefore fills the shadow
that falls inside it. T3 is the highest-ρ tile in every single arm of every ladder.

**⚑ THE ACCEPTANCE NUMBER ITSELF DESERVES A FLAG, AND IT IS NOT A CRITICISM OF SHADOW-CAL.**
Its ρ = 0.482 / 0.565 pair comes from **two different zones of the referent** — Wightmire, outdoor
overcast, floor 81.9; and a torch-lit cavern, floor 38.1 (SHADOW-CAL §2). Each of those rooms is
internally dominated by its own key light, i.e. each is close to an r ≈ 1 room. The gate then
re-used that **between-scene** pair as a **within-room** check between a torch-lit tile and an open
tile — a strictly harder test, and one the referent has never been shown to pass. **Routed to the
conductor as a spec question, not as an excuse:** if what Matt wants is a shadow at half the local
floor, the lever is the ROOM's floor uniformity, not the shadow.

**And the referent's own shadow is faint too.** SHADOW-CAL §0, verbatim: the character shadow "is
not visible without a luma stretch". At the shipped rung our absolute contrast is 6.6–12.3 luma
against the referent's measured 16.6–42.4 — shallower, but the same *kind* of object, and the rung
that matches the referent's absolute band (E = 3.5, 18.1–29.1 luma) is one constant away and named.

---

## §3 — The silhouette fix (routed here from RIVAL-CAST §8.2)

**The diagnosis was already measured and it was never texture** — the werewolf atlas means
(106.4, 104.8, 102.9). The cause is one number: the carried omni sat at `(0, 1.55, 0)`, **inside the
torso**. An omni inside a mesh lights that mesh's interior faces; every camera-facing surface has its
normal pointing away from the only light meant to define it, so the hero renders as a hole in his own
pool.

**The metric is the D1 requirement, stated as a ratio:** the player's on-screen mean luma divided by
the **local floor ring** (55–130 px around his own projected CAM-LOCK anchor) — "is the hero brighter
than the pool he stands in?" Body pixels come from the `NOCAST − GHOST` peel, so the mask is measured
rather than drawn.

| arm | player mean | local pool | **hero / own pool** | player vs dark-floor baseline | px darker than the dark floor |
|---|---:|---:|---:|---:|---:|
| **inherited, lamp in the torso** | 104.01 | 102.39 | **1.016×** | 2.00× | 0.0 % |
| inherited + offset | 129.16 | 102.85 | 1.256× | 2.49× | 0.0 % |
| unified, lamp in the torso | 85.57 | 76.75 | 1.115× | 1.29× | 11.9 % |
| **unified + offset — SHIPPED** | **119.46** | 77.59 | **1.540×** | **1.80×** | **2.9 %** |
| unified + offset + carrier fill | 120.27 | 77.60 | 1.550× | 1.82× | 2.9 % |

**SHIPPED: `CARRY_OUT = 0.72 m` camera-side, `CARRY_H = 1.42 m` (shoulder, not sternum).** The
inherited **1.016×** is the silhouette RIVAL-CAST saw, in one number: the hero is the same luminance
as the floor he stands on, so he is a shape with no separation. The fix takes him to **1.540×** and
cuts the fraction of his own pixels that are darker than the room's dark floor by **4.1×**
(11.9 % → 2.9 %).

**⚑ THE CARRIER FILL IS BUILT, MEASURED AND REJECTED ON ITS OWN NUMBER.** It moved the ratio 1.540 →
1.550, i.e. **+0.6 %**. A second light that moves the thing it exists to move by 0.6 % is a light
nobody should have to reason about in a later cell. The arm survives as `su_probe.gd --carry fill`
so the rejection is re-runnable.

**The offset is WORLD-camera-side and that is a declared cheat with a reason.** A lantern in a hand
is body-local and turns with the carrier, so the requirement ("never the darkest thing in the room")
would fail at half of all headings. This game's camera bearing is FIXED at CAM-LOCK yaw 47°, so a
camera-side offset is heading-invariant by construction. Written into the source above the constant
rather than left to be discovered.

**The boss.** Cold-emissive, unchanged from RIVAL-CAST (`SKY_COLOR` × 0.50, read from the level).
On-screen mean **114.30 = 1.73× the dark-floor baseline**, p90 **170.66** — it reads by the crystal.
**Declared honestly: 36.6 % of the boss's pixels are darker than the room's dark floor**, because
the golem's non-crystal half is genuinely unlit; the body is read by its bright half against its own
dark half, which is the pack's design intent and is what the 49.11 % emissive coverage buys.
**⚑ AND THE TEMPERATURE SEPARATION IS ERODED BY THIS CELL, WHICH IS AT MATT'S EYE (§6.2).**

---

## §4 — The declared deltas (LSTAT-2, and the ones LSTAT-2 cannot see)

**LSTAT-2 — NO DELTA.** L7 stage sha256 `5d4fa240cb0ead2c…` → **`5d4fa240cb0ead2c…`** — the same sha
BEAM-FIX and BEAM-CONE banked. **0 px changed of 921,600**, max channel delta **0**, mean luma
23.349629 → 23.349629 (**+0.000000**). It is zero because `unified_cosmology` defaults **false** and
every pre-existing caller therefore builds the room it always did — **and that limit is stated rather
than allowed to make the zero look bigger than it is.**

**The deltas I INTEND, with numbers, measured on the same floor band at the same camera:**

| state | floor luma | floor B − R | attribution |
|---|---:|---:|---|
| inherited `b80d7d9` | 67.62 | **−44.84 (WARM)** | centre light ON, torches casting |
| unified, one author OFF | 44.51 | −13.29 | **Scope 16 alone: −34.2 % floor luma** |
| unified, author 0.62 | 61.24 | +9.70 | |
| **unified, author 1.00 — SHIPPED** | **69.16** | **+17.11 (COLD)** | |

**Read as one sentence: the cell trades the retired warm centre light for a cold one-sun key of
almost exactly the same floor brightness — the room's LEVEL is held to +2.3 %, and its TEMPERATURE is
inverted.** The level-holding is a genuine property (Matt's accepted brightness survives); the
inversion is a genuine cost and is at his eye. It is also on-grammar: after Scope 16 the warm belongs
only where a torch burns or a living body walks, and the sky is cold.

**Staticity — the 0-px bar BEAM-FIX set, re-run because this cell ADDS a light.** Fixed CAM-LOCK
camera, synthetic observer handed to the level at (0,0) → (16,16) = 22.6 m, bodies and particles
peeled:

| | px differing of 921,600 | max channel delta |
|---|---:|---:|
| **MOVED** | **0** | **0** |
| NULL (identical inputs, two launches) | **0** | **0** |

**Pool-axis / one-sun, carried forward and re-verified on every render:** pool-axis error ≤ 0.000004 m,
one-sun deviation **0.000000°** on all 8 patterns, in all four rooms.

---

## §5 — ⚑ FIVE OF MY OWN INSTRUMENT FAILURES, AND HOW EACH WAS CAUGHT

### 5.1 zsh does not word-split, and three peels silently did not happen

The peel flags were held in a shell variable and passed unquoted — `$PEEL` — inside a **zsh** loop.
zsh does not word-split unquoted parameters, so `--nodust --noambient --nofx` arrived as **one
unrecognised argument** and every peel was a no-op while the log looked correct. Caught because the
probe prints a line per peel and the line was absent; fixed by moving every ladder into a **bash**
script with real arrays. The ladder script says so in its header.

### 5.2 ⚑ THE NULL CONTROL FAILED, AND THE ρ CENSUS HAD BEEN READING DUST AS SHADOW

Two launches with byte-identical inputs came back with **20,757 differing pixels and a max delta of
59.8 luma.** `GPUParticles3D` is unseeded in this tree — BEAM-CONE §5.1 already measured two launches
of one mote statistic differing by 0.081 — so *every* two-render peel was contaminated. The
give-away was in the census itself: **the shadow set's bounding box was the whole frame**
(x 0…1173, y 19…719). Turning off sky dust and the room ambient was not enough; the **twelve torch
flame/ember systems per room** are the same class of object. `--nofx` now hides **120 particle
systems**, and every ladder since re-runs the null control and prints it: **0 px, max 0.0000.**

### 5.3 A shadow-quality sweep that proved nothing, because its own numbers were a mote

Before the FX peel, a normal-bias × blur sweep returned `deepest_px_D = 38.34` in **all four arms** —
a suspiciously identical value that was a single dust mote, not a shadow. It "proved" bias and blur
did not matter. After the peel the real answer appeared: the **umbra occludes ~70 % of the author's
own contribution** and the shallow ρ is a **lighting** fact, not an instrument one. The first bias
guess was wrong for a real reason and it is now in the source: Godot scales a *directional*
`shadow_normal_bias` by the **cascade's world size**, so a value copied from the positional-light
family (1.0–1.2, correct for a 5 m sconce) becomes a metre-scale offset across a 70 m cascade.
Shipped at **0.05 / blur 0.25 / bias 0.02**.

### 5.4 The readability body-mask included the body's own shadow

`|CAST − GHOST|` is the body **plus its cast shadow**, because the ghost arm has no shadow either.
The "body" mask swelled from 657 px to **1,246 px** and quietly folded a patch of dark floor into the
hero's own luma. The mask must be taken between two arms that **both** lack the shadow —
`|NOCAST − GHOST|`. Fixed, and the reason is written above the line.

### 5.5 `--resolution 1920x1080` is not 1920×1080, and it is not the CAM-LOCK camera

On this host the window is clamped by the menu bar and the viewport comes back **1920×971** — aspect
1.977, while the CAM-LOCK derivation carries `PL_ASPECT = 16/9` as a constant. The first two ρ
ladders were therefore measured at a camera that is **not** the published lock. Every measurement in
this note is re-run at **1280×720**, which returns exactly 1280×720. Fewer pixels, correct camera; a
measurement at the wrong camera is precisely the defect Scope 20 ruling 1 exists to prevent.

**One more, smaller:** a single-frame shot came back with an **empty banner**, because a `Label`'s
text set during the same `_process` that captures the viewport has not laid out yet. Caught by
looking at the frame instead of at the "frames: 1" line — BEAM-CONE §6.2's lesson, arriving again.

---

## §6 — Fog-unlit A/B (Scope 19), and the boss-beam crossing (captured, NOT ruled)

### 6.1 FOG-UNLIT — the verdict-shape, so Matt knows what he is choosing between

Mechanism is one property on the SKY lamps only (`light_volumetric_fog_energy = 0`); the warm torch
fog-lighting is untouched, exactly as the directive words it. Measured FX-peeled at the circle pool:

| | value |
|---|---|
| frame mean luma | 67.569 → 66.581 (**−1.46 %**) |
| pixels changed at all | 190,138 of 921,600 (20.6 %) |
| pixels darkened > 2 luma | 143,780 (15.6 %), p99 drop 9.30, max drop **15.16** |
| **upper third (the air / shaft volume)** | **mean drop +0.000, max 0.93** |
| middle third | mean drop +1.624, max 15.16 |
| lower third (the floor) | mean drop +1.341, max 15.16 |

**⚑ THE A/B IS A SMALL CHANGE AND IT IS SMALL FOR A STRUCTURAL REASON WORTH STATING: since SKY-2 the
beam is a MESH, not fog.** The sky lamps' fog contribution is only the **soft ground-level haze
around the pools** — the shafts themselves are geometry and do not move (max 0.93 luma in the upper
third of the frame). So this is a *"crisper pool skirt vs slightly hazier pool skirt"* decision, not
a *"beams on/off"* decision. Delivered as the A/B segment; the verdict is Matt's.

### 6.2 THE BOSS CROSSING A BEAM BASE — captured, and the gap law NOT TOUCHED

Per the routed fork: `SKY_BEAM_BASE_Y` is **unchanged at 2.40 m** and nothing in this cell moves the
gap terminus. The deliverable clips are staged so the crossing is unambiguous — the boss walks
(−2.0, −9.5) → (−6.06, −5.33), ending **on** the room-3 circle pool, so its top 0.35 m passes through
the beam-base plane in motion, twice per clip pair, at the game camera. Keyframes
`SU_after_mid.png` / `SU_after_end.png` hold the moment as stills.

---

## §7 — Constants, before and after

| constant | inherited | **SHADOW-UNIFY** | why |
|---|---|---|---|
| `unified_cosmology` | — | **flag, default FALSE** | LSTAT-2 stays able to detect things (§4) |
| `Key` aim | Euler (−62, −28, 0) | **basis from `sun_travel_dir()`** | Scope 19; deviation 0.000000° |
| `Key.light_energy` | 0.06 | **`UNIFIED_KEY_ENERGY` = 1.00** | deepest rung passing G-3 (§2) |
| `Key.light_color` | (0.55, 0.66, 0.95) | **(0.58, 0.68, 0.95)** | cold; warm is reserved for fire |
| `Key` shadow | default | **PSSM 4-split, 70 m, blur 0.25, nbias 0.05, bias 0.02** | §5.3 |
| 12 sconces per room | cast (E2 all-twelve) | **`shadow_enabled = false`** | Scope 13 cl. 2; retires the 5.11× smear |
| 8 sky projector spots | cast | **`shadow_enabled = true`, `shadow_opacity = 0`** | §1.3 landmine |
| `InteriorPool` (centre light) | built, dimmed 0.45 on arm A | **NOT BUILT** | Scope 16, Matt |
| carried omni | casting, at (0, 1.55, 0) | **non-casting, +0.72 m camera-side at 1.42 m** | Scope 13 cl. 3 + §3 |
| `CarrierFill` | — | **built, measured, NOT shipped** | +0.6 % (§3) |
| `sky_fog_lit` | — | **flag, default true** | Scope 19 A/B |
| `SKY_BEAM_BASE_Y` / gap law | 2.40 | **unchanged** | routed fork is CAPTURE, not rule |
| `SKY_ENERGY_REF` / `SKY_SHAFT_ENERGY` | 30.0 / 0.19 | **unchanged** | BEAM-CONE's, not this cell's |

---

## §8 — Deliverables — `~/Games/reincarnated-godot/tmp/shadowunify/`

**M-EYE, MOTION FIRST. Every clip at the CAM-LOCK rig, camera identity AND lighting identity printed
on every frame. 240 frames / 8 s / 1280×720 / 30 fps per arm.**

1. **`clips/SHADOWUNIFY_before_after_watch_CAMLOCK.mp4`** — **THE ONE TO WATCH.** The BEAM-CONE state
   beside the unified cosmology, the SAME walk at the SAME frames at the SAME camera, one variable.
   Left banner: *"BEFORE — godot b80d7d9: 12 torch omnis + sky spots + carried omni ALL CAST · centre
   light ON"*; right: *"SHADOW-UNIFY (AFTER) — one author E=1.00 · ρ 0.86–0.95 · pools 1.028× ·
   centre light RETIRED"*.
2. **`clips/SHADOWUNIFY_fight_walk_CAMLOCK.mp4`** — **the fight-adjacent motion clip, four laws in
   one take:** the werewolf walks a torch pass-by (local floor rises ~1.4× across the walk — contrast
   magnification, emergent, unscripted), the boss walks a beam base and crosses it, both bodies stay
   readable, and the shadows stay one direction the whole way.
3. **`clips/SHADOWUNIFY_fog_unlit_AB_CAMLOCK.mp4`** — the Scope-19 A/B, same walk, same frames.
4. **`plates/PLATE_shadow_rho_G3.png`** — the ρ plate: five tiles, the shipped frame beside **the
   shadow itself** (the `NOCAST − CAST` peel at gain ×6) and every tile's numbers, with the inherited
   state's ρ and shadow-pixel count under each.

**KEYFRAMES:** `keyframes/{SU_after,SU_before,SU_fogun}_{mid,end}.png`.
**INSTRUMENTS:** `scripts/su_probe.gd` + `scenes/su_probe.tscn` + `scripts/run_su.sh` ·
`tmp/shadowunify/measure/{rho,pools,readability,plate_rho}.py` ·
`measure/{run_rho_ladder,run_quality,run_pools,run_read}.sh` · `render_deliverables.sh` ·
banked JSON: `rho_{P062,E10,E14,E35,D30E35,D30E60,LEGACY}.json`, `pools_survival.json`,
`read_{SHIP,LEG}_{torso,offset,fill}.json` · `l7/l7_shadowunify.png` · `logs/`.

**PEELS (added, one word each):** `--legacycosmos` (wr2) / `--legacy` (probe) restores the whole
inherited cosmology · `--fogunlit` the Scope-19 arm · `--spotmode 0` re-fires the pools-vanish
landmine · `--keyE` the author's energy · `--nokeycast` the author without its shadow ·
`--sconceS` the torch-dim fork · `--carry torso|offset|fill` the three carried-light arms ·
`--nobodycast` / `--ghost` / `--nofx` the measurement peels · `--obs` the staticity observer.
All earlier peels survive unchanged.

---

## §9 — Guards

| guard | result |
|---|---|
| collision check at cell start (`git status`, tracked) | **clean**, HEAD `b80d7d9` as expected |
| `project.godot` sha256 | `6bef17eb…` — **NO DELTA** (a headless run had stripped a default-valued `[rendering]` block; restored at cell start and re-verified at cell end) |
| `sky_shaft.gdshader` / `sky_dust.gdshader` | **NOT TOUCHED** — this cell moves lights, not the beam |
| `walltop_void_radial` / `walltop_occlude` shaders | `2710fc11…` / `d29a01be…` — unchanged |
| all `vfx/ambient/**` | rollup **`e049676b…`** — byte-identical to BEAM-CONE's banked value |
| prior cells' clips / plates | `tmp/beamcone` ×4 clips, `tmp/beamfix` ×5 clips, `tmp/rivalcast` ×1 — **intact** |
| traces / engine tree | **never opened for write** |
| declared authorised surfaces | `scripts/kit_replica_level.gd` · `scripts/wr1_level.gd` · `scripts/wr2_playback.gd` (modified) + `scripts/su_probe.gd` · `scripts/run_su.sh` · `scenes/su_probe.tscn` (new) — **6 files** |
| staged-file guard (BEAM-CONE's lesson: the guard is a list) | 3 `M ` + 3 `A `, 6 expected; no `.uid`, no `__pycache__`, no unrelated probes |
| watch smoke (the port, not just the probe) | `wr2_playback.tscn` builds + renders, prints the SHADOW-UNIFY line and the carried-light line, **no SCRIPT ERROR / Parse Error** |
| godot commit | **LOCAL, ahead 13, NOT pushed** |
| disk | `tmp/shadowunify/` = **83 MB** after prune (peak intermediates ~460 MB, well under the 2 GB ceiling); every PNG sequence encoded then deleted in the same command; 60 measurement frames kept as the ρ/pool evidence |

**Open, honestly:** (a) the ρ plate's crops are framed on the boss, so the player's own shadow is the
smaller of the two blobs in the right-hand column rather than the headline one; (b) the deliverable
clips carry dust and ambient ON (they are the real render), so the two arms of the before/after are
not bit-identical outside the lighting — the *measurements* are all FX-peeled, the *clips* are not,
and that is the right way round but it is worth knowing; (c) rig-quality of the golem at close range
is still unjudged (RIVAL-CAST's own open item, unchanged).

---

## §10 — At Matt's eye

1. **⚑ THE SHADOW IS FAINT, AND THAT IS THE GATE'S OWN DOING.** ρ lands at **0.86–0.95**, not
   SHADOW-CAL's ~0.50. The arithmetic is in §2 and it is not a tuning shortfall: **ρ = 1 − (the one
   author's share of the local floor)**, so a deeper shadow *necessarily* disagrees more between a
   torch-lit tile and an open one. Reaching 0.50 at the gate's 10 % needs a room whose bright:dim
   floor ratio is ≤ 1.11; **ours is 1.47.** The rung that matches the referent's *absolute* contrast
   band (18–29 luma vs its measured 16.6–42.4) is **`UNIFIED_KEY_ENERGY` 1.00 → 3.50**, one constant,
   and it costs the gate (spread 15.7 %) and raises the room (frame mean 45–69 → 59–100). **Your
   call, in motion.**
2. **⚑ THE ROOM IS THE SAME BRIGHTNESS AND THE OPPOSITE TEMPERATURE.** Floor luma 67.62 → **69.16**
   (+2.3 %, i.e. your accepted level survives); floor blue-minus-red **−44.84 → +17.11** — warm to
   cold. Scope 16 (centre light retired, your ruling) does most of it: it alone takes the floor to
   44.51 luma and −13.29. If the crypt now reads too cold, the levers in order of bluntness are:
   restore the centre light (`center_light_retired = false`, one word), lower the author
   (`UNIFIED_KEY_ENERGY`), or warm the sconces back up.
3. **THE HERO IS NO LONGER THE DARKEST THING IN THE ROOM, AND HERE IS THE NUMBER.** Hero luma ÷ the
   pool he stands in: **1.016× → 1.540×**. The lamp left his chest and moved 0.72 m toward the lens
   at shoulder height. **The fill light you might have expected is measured and NOT shipped** — it
   bought 0.6 %.
4. **THE POOLS-VANISH LANDMINE IS REAL AND IS NOW DISARMED WITH A NUMBER.** The obvious way to stop
   the sky lamps casting costs the floor pool **56 % of its p99**. The shipped way costs **nothing**
   (1.028×) and still leaves **zero** non-directional shadow authors in a 71-light scene.
5. **THE BOSS CROSSES A BEAM BASE IN EVERY DELIVERABLE CLIP AND I DID NOT TOUCH THE GAP LAW.** Judge
   the 2.75 m body passing through the 2.40 m terminus in motion; if cold-on-cold reads as intended,
   nothing moves and the pools stay where BEAM-CONE left them.
6. **THE FOG-UNLIT A/B IS A SMALLER DECISION THAN IT SOUNDS.** Because the beam has been a MESH since
   SKY-2, un-lighting the fog changes the **haze skirt around the pools** and **nothing above 2 m**
   (max 0.93 luma in the top third of the frame). −1.46 % frame mean. It is a pool-edge decision.

---

## §11 — Routing

**SHADOW-UNIFY lands. TELL-DRESS (BR-1 §3 cell #5) is next.** It inherits a scene with exactly one
shadow author, so telegraph decals can be authored against a known light direction rather than
against twelve; and it inherits **one packaged brightness decision still open at Matt's eye** —
pools at 62 % (BEAM-CONE), the boss crossing the 2.40 m terminus (RIVAL-CAST), the shadow at ρ 0.93
and the floor gone cold (this cell). All four are the same conversation and all four are now
rendered, in motion, with numbers.
