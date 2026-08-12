# SB-1 Cell A2 (CP-B) — SKIRT · LOCOMOTION · PLAYER · IDLE · SUMMONS · THE CLIP

**Cell ID:** `SB1-CELL-A2` · **Date:** 2026-08-12 · **Author:** drax (presentation seam)
**Charter:** `gandalf/notes/2026-08-10-sb1-kc2-scene-run-charter.md` @ `9b3e7e2b` (+ retention rider)
**Ledger:** `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — **A1b-6 fires this cell**;
R-CPA-1/3/4 bind, R-A1-1 and R-A1-LAW bind, PL-5 binds item 6, PL-7 authorises the pushes.
**Godot repo:** `aec38e8` → `d5468b2`, **six commits, 16 paths**. **Meta repo:** `1da0b2fe`.

**VERDICT: ALL SIX ITEMS LANDED. 0 HALTS.**

---

## 1 · Per-item commit table (CL-2)

| hash | item | what |
|---|---|---|
| `4bf15b4` | **1** | the SKIRT — dress that outruns every camera, plus `clip_rect()` and `camera_ground_gate()` |
| `8c4b82a` | **2** | the LOCOMOTION driver — 344 bodies from 1,003 knots, and the facing law |
| `6f99130` | **4** | the IDLE line — 344 AnimationPlayers, three shared clips, per-leg clip choice |
| `1962b4c` | **3** | the PLAYER — pinned, spinning, channelling (R-CPA-4) |
| `a5eab4c` | **5** | SUMMONS — K-4 declared by name on an empty domain |
| `d5468b2` | **6** | the CP-B CLIP — three shots, 63.83 s, promoted on green |
| `1da0b2fe` | 6 (meta) | the FG-9 promotion leg, on the factory spine's own gates |

**Item order is 1 · 2 · 4 · 3 · 5 · 6, and that is deliberate:** item 3's player body needs the
same animation binding item 4 builds, and writing it twice to preserve a numbering would have put
two copies of the clip loader in the tree. Commit titles carry the brief's numbers.

**Containment.** Godot porcelain **233 = the L-0 pin exactly**. Engine porcelain **2,789 = the
FG-17 baseline**, before and after. Baton digest recomputes to `d7ecd866ac45…` after every harness
run and every render. No PNG or MP4 is committed. `captures/` **6.67 G → 6.69 G** of its 10 G
ceiling.

---

## 2 · Item 1 — the SKIRT (R-CPA-3: *"skirt for SB-1, walls at the authored level"*)

An 800 × 800 m dress plane, **1 cm under** the measured floor, centred on the measured footprint's
centre. Its half-extent (400 m) is a **presentation choice with NO WIRE BASIS** and says so in its
own report row, exactly like the nemesis height.

| claim | how it is asserted, rather than promised |
|---|---|
| it is **not** the GL-13 clip surface | `clip_rect()` reads the footprint and **cannot** read the skirt. Checked by IDENTITY against the floor (86.915 × 85.303 m — A1b's numbers, unmoved) **and by DIFFERENCE** against the skirt, so a clip rect that had quietly grown to 800 m fails |
| it is **not** geometry | 1,430 nodes walked: zero `CollisionObject3D` / `CollisionShape3D` / `CollisionPolygon3D` anywhere in the scene |
| the camera **never reaches its edge** | `camera_ground_gate(eye, look, fov, aspect, far)` — nine frustum rays intersected with the ground plane; each must land inside the skirt **or** beyond fog saturation. Per-frame callable; item 6 HALTs on a red |

**FL-3 on the gate itself, in both directions.** An at-horizon pose goes RED with the horizon
reason; a pose parked 900 m out looking straight down goes RED with the *outside-the-skirt* reason.
⚑ The second mutant's first draft went red for the **wrong reason** (horizon) — JR-A1a-4's lesson
arriving on my own gate — and the check now asserts that mutant's own string.

**What the frames caught, before this landed** (my own law: the frame is a verification instrument):

1. **`fog_density` is the density reached AT `fog_depth_end` in DEPTH mode, not a per-metre rate.**
   Carrying the exponential arm's 0.006 across ran the depth fog at **0.6 % strength**: the first
   probe frame came back a lit grey plain with a hard horizon line. At 1.0 the ground reaches
   background exactly.
2. **The fog colour is now the background colour, identically** — a different fog colour paints a
   bright band where ground meets sky. Measured on the probe frame at native resolution: the ground
   emerges from **rgb(16,15,18) — the background — as a smooth gradient with no discontinuity**.
3. Skirt albedo 0.105 → 0.038, because a lit 800 m plane is a lit 800 m plane.

---

## 3 · Item 2 — the LOCOMOTION driver

`apply_tick(tick_f)` is a **pure function of the tick**: no accumulator, no easing, no velocity
integrator. Ask it twice, get the same world.

| law | what the driver does, and the number that proves it |
|---|---|
| **GL-7** between-ticks | a 30 fps frame advances 0.408 ticks, so the position function is evaluated BETWEEN knots. Not a second function: at integer ticks it is **BIT-IDENTICAL** to `actor_position()` on **32,375 samples, max abs delta 0.0** |
| **GL-7** per leg | `leg_index_at()` → `leg_speed_ms(leg)`. Asserted at all three A1a bases (**12 @ 2 dp · 23 @ 4 dp · 282 @ 1e-6 m/s**) and on the driver's own output at **282/282** leg boundaries |
| **K-5** the drip | entry is each body's own `path[0].run_tick`; the driver does not know what a wave is. Worst wave **167 spreads 306 ticks = 24.98 s**; **14 of 20** waves drip. *A per-wave batch spawn would read 0 on all twenty* — the check names that counterfactual |
| **NOTE-1** dwells | **all 17**, not the named 12: position held across the whole span to 1e-5 m, sampled BETWEEN ticks, and the body reads idle |
| **GL-12** past the end | position UNDEFINED → body **HIDDEN**. Not held at its last knot (filling an absence), not dressed as a death (that is the combat act). 344/344 visible on the terminal tick, 344/344 gone half a tick later |
| **R-A1-1** | no combat presentation is REACHABLE from the driver — asserted on the file's own bytes with comments **and string literals** stripped |

### ⚑ THE FACING LAW — a defect report on my own A1b item 2

A sim **rotation** of θ is a Godot yaw of θ; a sim **heading** of θ is not, because these bodies are
**+Z-FORWARD**. That convention is measured in this repo and twice-evidenced (WR1-ROOMS A1, and
`mobcast_stride_probe.gd`'s sign correction where the cross product and seven independently
authored Synty clip labels agreed). A1b seeded all 344 with `rotation.y = spawn_heading_rad` —
**short by exactly π/2**: every body faced 90° off its own declared spawn convention. Invisible in a
statics cell; visible the moment anything walks. One function now
(`sim_dir_to_godot_yaw`), used by the seed AND the driver, asserted on 344/344 **and against the old
form** so a revert cannot pass.

### What the smoke caught in itself

* `leg_index_at` was **closed** `[start, end]`, so a body arriving at a dwell reported the *arrival*
  leg's speed on the dwell's first tick — **12 of 17 dwells began with one tick of walking**.
  Half-open now: the leg that is STARTING says what happens next.
* the seed check read `rotation.y` **after** the driver had walked the bodies and rewritten it, and
  reported a defect that was not there. *A measurement taken after the thing it measures has moved
  is not a measurement.*

---

## 4 · Item 4 — the IDLE line (NOTE-16, taken deliberately)

344 AnimationPlayers, **three `Animation` resources parsed once and shared**. Clip choice follows
the MEASURED per-leg speed (idle / walk / run), never an average over the body. A hidden body does
not animate (`active` follows visibility), so pre-entry bodies cost nothing and are not secretly
mid-stride when they appear. Clips harvested from the rigs that already use them: idle + walk are
`mob_rig`'s pair, run is `wr2_actor_rig`'s `CLIP_RUN`.

**Pre-entry bodies are HIDDEN until their own entry tick** — the choice the brief asked me to state.
GL-8 makes `path[0].run_tick` the first drawable tick, and a body standing on the board before the
wire says it is there would be inventing 25 s of presence for the ambush's last arrival.

**FOOT-SLIDE IS NAMED DEBT, NOT HIDDEN DEBT (GL-19).** Clips play at **authored rate**. The run's
measured leg speeds (**median 4.000 m/s over 642 moving legs, max 5.800**) outrun every locomotion
clip on disk, so fast bodies slide; time-scaling a walk cycle to 4 m/s invents a cadence the wire
does not carry. Declared in `Kc2Motion.report.foot_slide_debt`, with the instrument that would close
it named (`scripts/mobcast_stride_probe.gd` measures a clip's implied ground speed).

**The binding test found two defects in itself before it found none in the clips** — and this
matters because a retargeted clip that binds to nothing leaves the body in rest pose, which by eye
is exactly what an unbound body looks like:

1. it sampled *through* the hidden-bodies-do-not-animate optimisation, and an inactive
   AnimationPlayer ignores `seek`/`advance`;
2. it measured `get_bone_global_pose().origin` and read **0.0 on all three clips**. Skeleton3D
   refreshes its GLOBAL pose cache on its own processing step and a headless `--script` run never
   takes a frame — so the global cache sat at rest while the LOCAL pose the animation writes moved
   0.081 rad. **A gate whose reading depends on a step the harness never runs is measuring the
   harness** (NOTE-15's law, on a different instrument). Local pose now: idle 0.048 rad, walk 0.865,
   run 1.479 between phase 0 and 0.5.

---

## 5 · Item 3 — the PLAYER (R-CPA-4: *"the body performs the channel"*)

* **PINNED.** NOTE-13 re-measured every build: player x and y take **one distinct value each across
  3,732 samples**, radius one value = 3.000, `channel_active` **true on 3,732/3,732**. Measured
  translation of the body over 24 sampled ticks: **0.000000000 m**. CP-B's "player sweep" is a spin
  in place. If a future baton's track is not constant, the file declares the station UNDEFINED and
  places no body (GL-12).
* **THE SPIN IS A PURE FUNCTION OF SIM TIME.** Same tick twice → identical yaw.
* **THE SPIN RATE IS A PRESENTATION CHOICE WITH NO WIRE BASIS**, flagged like the nemesis height.
  The reference's per-tick 360° is the sim's **uniform-disc abstraction**, not a render rate: 12.25
  rev/s is 147°/frame at 30 fps and aliases into a body that appears to turn slowly *backwards*.
  **0.60 s per revolution = 20.00°/frame measured off the driver**, under the 45° direction-ambiguity
  bound (GL-16: judge at watch distance).
* **THE CHANNEL IS CONTINUOUS BECAUSE THE WIRE SAYS SO** — and it is driven per tick from
  `tracks.circle_sweep.active`, not from that sentence.
* **NO CONSUMER READS `heading_rad`** — asserted on the file's own code (comments and string
  literals stripped): zero occurrences.

**R-BR-17 harvested first** (charter § 10 lists it NOT-HARVESTED; CL-4 forbids restating from
recollection), including the exit-review amendment that the shell works by **occlusion**, not
additive bloom. Applied: the CORE silhouette is the measured **3.000 m** ribbon the arena already
draws at `config.kit.radius_m` — no pack ships a primitive that draws a MEASURED radius — and
Binbun's `magic_areas/basic_area` is the SHELL, scaled so its ground disc lands **on** the wire's
radius and stacked under the ribbon. GL-1: the pack supplies material, the trace supplies geometry.

**Two catches from measuring instead of assuming:**

* the FX scale is read from the **GroundGlow mesh by name**. Sizing from "the largest quad" would
  have used the flare particles' 3.4 m draw pass and drawn the ground disc at **3.64 m — 21 % wider
  than the channel the wire measures**. The flares still overspill to 3.643 m; that is bloom, not
  silhouette, and it is now a **declared number** (`shell_overspill_m`) rather than a frame
  discovery.
* **CL-10 on a precedent number, and it did not reproduce.** WR2 records this body at native rest
  **1.7097 m**; my own AABB path measures **1.628 m**. A measurement-path difference, not a
  different body — but shipping 1.628 would have put the protagonist **below every trash mob at
  1.70**. Drawn at the precedent's height (scale 1.0502), with both numbers and the delta in the
  report.

The A1b plinth is **removed**, not stacked under him: it stood in for the player when nothing stood
there, and a body on a plinth is a body lifted off the ground the wire measured.

---

## 6 · Item 5 — SUMMONS (K-4, literally)

`ABSENT-SUMMON-BODIES` / **DORMANT-EMPTY-DOMAIN**, declared by name with its count recomputed from
the actor table every build (a hard-coded "0 summons" would be a recollection wearing a
measurement's clothes, CL-4).

**0 of 344** actors carry no path. R-L53-2 declares summoned bodies OUT-OF-MODEL and the sim never
simulated one (PL-4), so the render-at-spawn half has nothing to act on. **The prohibition half is
live and STRUCTURAL:** `Kc2Baton` refuses the *load* on a pathless actor, and `apply_tick()` has no
branch that can move a body without a knot pair. When a baton finally lands summon bodies the loader
**stops** — the loud failure the fork wants, never a silent invented wander. The summon-CAPABLE
rostered kits are named in the declaration (Karroz ×2, Tempest Spawn ×2, The Steward ×2, Stone
Basilisk ×2), all fully pathed, none raising adds.

---

## 7 · Item 6 — the CP-B clip

**Class E — owner-eye. UNTRACKED, never committed.**
`agentic_orchestration/galadriel/captures/2026-08-12-sb1-cpb/`

| field | value |
|---|---|
| file | `cpb-motion-watch.mp4` |
| sha256 | `97378e50fe479444cfab8840d99bdabc7a033067480de67e86bbc6097285aaf3` |
| bytes | 17,610,978 |
| duration | **63.83 s** (expected trace 63.67 s) · 1920×1080 · h264 · 30 fps |
| time base | **1× real time** — the trace clock is inviolate (GL-18) |
| beside it | `MANIFEST.json` (sha256, framing sentence, per-shot camera poses **and camera-gate verdicts**, driver report, FG-9/FG-12 receipts, PL-5 before/after) + three shot sidecars |

> ### Framing sentence (charter § 6 — the sentence Matt reads before looking)
>
> **This is run E-s09-cp150 MOVING, and every motion in it is a measurement.** 344 bodies walk the
> 1,003 path knots the sim emitted, each entering on its own tick — the wave-167 ambush drips in over
> 306 ticks, 24.98 seconds, because that is what the wire says and a batched spawn would have been
> tidier and false. Bodies that stop are standing at knots the sim put two of in one place. The
> player never moves: he is pinned at the origin the whole run with the channel never once off, so
> his "sweep" is a spin in place inside a 3.000 m field that is the wire's own radius. **Nothing here
> strikes, dies or counts — combat is the next act. When a body vanishes, that is its path ending,
> not a death being shown.**

### The three shots, and why these windows

The windows were chosen **by measuring the baton**, and the measurement moved them twice.

* **CONCURRENCY.** The 344-body roster is a **SEQUENCE, not a crowd**: peak concurrency **31**
  (tick 1261); the busiest 30 s window averages **14.6**. My first draft framed ticks 1560–1930 wide
  and the dry run showed **two to five bodies on an 87 m floor**.
* **THE DWELLS ARE ENGAGE-RING WAITS, EXACTLY.** Every long dwell sits at **r = 2.400 m** from the
  player — `d_engage_m` to three decimals, on all of them. So the dwell shot became a station shot.

| # | shot | ticks | trace s | what it carries |
|---|---|---|---|---|
| A | `a-field` | 1131–1451 | 26.1 | 68 entries, mean 14.6 bodies, knots spanning the whole measured floor — **and the SKIRT** |
| B | `b-ring` | 1570–1700 | 10.6 | five long dwells (44–70 ticks): bodies walk in and **stop dead on the 2.4 m ring** while the player spins in his 3.0 m channel |
| C | `c-ambush` | 2920–3250 | 26.9 | wave 167's **306-tick / 24.98 s drip**, eight p05 two-knot straight walkers arriving on the station |

### Gates, in order, each able to stop the cell

* **PL-5 floor check before any frame**, in the harness AND in the shell: **6.67 G of 10 G, PASS**.
  Plus a **free-disk floor** (31.5 G free vs an 8 G floor) — a render that fills the volume loses the
  run just as thoroughly as one that breaches the ceiling.
* **The camera gate per shot, before any frame** — nine frustum rays (R-CPA-3). **PASS ×3**; the
  verdicts are in the manifest.
* **FG-9** — each shot encoded to a temp name, concatenated to a temp deliverable, ffprobe-verified,
  promoted **only on green**, then the promoted bytes **re-hashed against the pre-promotion digest**
  so the promotion is proven not to have changed them.
* **FG-12** — **1,915 PNG frames (3.04 G) pruned** immediately after each encode, each prune leaving
  a receipt line with its regeneration command. Frames were written to `/tmp`, outside `captures/`.

### The factory spine ran the legs it may run — and the line is declared (charter § 4)

`ffprobe_verifies` and `sha256_matches` are called **from `factory.gates`** by
`drax/tools/kc2_cpb_promote.py`: spine code adjudicating SB-1's media promotion, not a hand-rolled
ffprobe parse. **The render stayed classic on purpose, and this is a law-driven decline, not a
fault:** D-14 says a spine phase that imports or renders Godot churns 3,288 gitignored `.godot/`
lines — post-D-1 a visible write, therefore a breach, therefore an abort — and its closing sentence
on the charter routing Godot cells outside the spine is *"keep it that way."* **The spine did not
fault. G-FACT is unaffected by this cell.**

### ⚑ What the frames caught, again

The first preview of the channel came back with the Binbun aura scaled **uniformly** into a **5 m
yellow pillar** that occluded the player standing inside his own channel and swallowed the 3.0 m
ribbon that is the edge of record. Two fixes, both from the harvested law rather than taste:
**scale XZ only** (the wire measures a RADIUS, not a volume), and apply **R-BR-17's own
discriminator against the pack** — the two `UpwardGlow` cylinders are a **readable shape**, so they
do not go under a core beat. Light energy 0.55 → 0.35 for an aura 2.14× wider than the one that
number was measured on. Verified after the fix on extracted frames at native resolution, including a
four-frame strip at 0.5 s intervals showing the knight through front, side and back of one
revolution.

---

## 8 · Harness state (CL-3: reproduce the number from the artifact)

| harness | before this cell | after |
|---|---|---|
| loader smoke | 28 checks, 0 FAIL | **28, 0 FAIL** |
| placement smoke | 10/10 | **10/10** |
| falsification | 7 checks, 0 FAIL | **7, 0 FAIL** |
| differential vs the stub consumer | 22/22 EXACT | **22/22 EXACT, 0 DELTA** |
| arena smoke | 20 checks | **24, 0 FAIL** (+4 skirt) |
| **motion smoke** | — | **26 checks, 0 FAIL** (new) |

The whole A1a wall was re-run **after** the loader change (`actor_position_t`, `leg_index_at`, the
facing law), not merely the new file's.

**FG-10, and it names its layer.** Two identical passes plus a third with the scene deliberately
walked elsewhere first produce one digest over **40 ticks × 344 bodies**. Layer: **scene-sim**
(visibility + world position after the single presentation cast + leg index + clip state + yaw).
**NOT pixels** (the N3 term is open — charter § 10). **NOT skeletal pose.**

---

## 9 · NOTES (continuing from NOTE-16)

**NOTE-17 — the roster is a SEQUENCE, not a crowd, and the statics cell could not show that.**
Peak concurrency is **31 of 344** (tick 1261); the busiest 30 s window averages **14.6**. A1b's
still-set put all 344 bodies on the floor at once because a statics cell has no clock, and the
honest read of that frame is *"here is where every body of the run spawns"*, not *"here is the
army"*. Anything reasoning about crowd density, VFX budget or per-frame cost from the CP-A stills is
reasoning from a picture of the whole run at once. **Bears directly on the form-diversity commission
(R-CPA-2):** at ~15 bodies on camera the six-dress clone read is far weaker in motion than it is in
the parade still.

**NOTE-18 — every long dwell is an ENGAGE-RING wait, to three decimals.** All twelve ≥44-tick
dwells sit at **r = 2.400 m** from the player — `config.kit.d_engage_m` exactly. The five in shot B
stand at `(2.346, -0.506)`, `(0.153, 2.395)`, `(-2.376, 0.340)`, `(2.346, -0.505)`,
`(1.350, -1.984)`; radius 2.400 on every one. So the violet ring A1b drew as a static is **the thing
the bodies are standing on**, and the dwell is not a pause in walking — it is a body arriving at its
engagement distance and holding. The five Δtick=1 dwells are a different phenomenon (clipped arrival
steps) and are drawn identically because the wire does not distinguish them.

**NOTE-19 — two bodies dwell at the SAME point and interpenetrate, and nothing may push them
apart.** `w160_a003` and `w160_a004` both wait at `(2.346, -0.506)` — 0.001 m apart. The wire
carries `entity_radius_m` **null ×344** and `body_radius_role = NON-CAUSAL`, and `collision_model`
is **OPEN-PLANE**: there is no body radius to separate them with and no collision to do it. Visible
in shot B. **Adding a separation would be inventing geometry the sim did not have** — the sim's
bodies are points, and two points may coincide.

**NOTE-20 — `fog_density` means something different in DEPTH fog, and the default reading is
silently wrong.** In `FOG_MODE_EXPONENTIAL` it is a per-metre rate; in `FOG_MODE_DEPTH` it is the
density **reached at `fog_depth_end`**. Carrying 0.006 across ran the fog at 0.6 % and produced a
frame that looked like a lit car park. Any later cell switching fog modes re-measures rather than
carries. (FL-4's shape: a constant is pinned to the substrate it was measured on — here, to the
*mode* it was measured in.)

**NOTE-21 — a body's disappearance at its terminal tick is NOT a death, and the clip will read as
if it were.** 344/344 paths end and the body is hidden, because past `path[-1]` the position is
UNDEFINED (GL-12). Bodies therefore **pop out of existence** in the clip, most of them at the tick
they died on. This is the honest state of a cell with no combat presentation, it is in the framing
sentence, and **it is the single biggest thing the combat act changes**: the collapse (R-A1-1) goes
exactly where the pop is now.

**NOTE-22 — the A1b roster was seeded 90° off, and only motion could have found it.** Full account
in § 3. The general form for future cells: **the frame map for POSITIONS and the frame map for
FACINGS are different functions, and a statics cell exercises only the first.** Both now live in
`Kc2Baton` beside `sim_to_godot`, so a consumer cannot pick one up without the other.

**NOTE-23 — two instrument defects in one cell, both of the NOTE-15 class.** (i) The clip-binding
test sampled through the optimisation that disables the thing it measures; (ii) it read a pose cache
that only refreshes on a frame the headless harness never takes. Both read as **clean negatives** —
"0.0 m, nothing is bound" — which is the most dangerous failure shape an instrument has. *A gate
whose reading depends on machinery the harness never runs is measuring the harness.*

---

## 10 · Attack surfaces for the COMBAT act (post-CP-B)

Named so the gatekeeper and the conductor do not have to find them. Surfaces 1–9 of the A1b landing
still stand except where noted.

1. **The pop is where the collapse goes** (NOTE-21). 344 disappearances at terminal ticks are
   already timed exactly; the combat act replaces each with a death read. R-A1-1 rules what may
   *not* appear there: 332/344 killing blows carry `damage_applied == 0.0`, so a number would print
   "0" on 96.5 % of them.
2. **`strike()` exists, `charge()` does not, and K-1 is still enforced only structurally.** This
   cell added **no** anticipation timing and no wind-up driver. There remain **zero telegraph rows**
   in the event vocabulary to key one from; back-timing a wind-up from an impact fabricates timing
   grammar (GL-12).
3. **The motion driver reads NO event rows at all.** Combat presentation is the first consumer that
   will, and the FG-13 census (1,556 consumed + 344 binned = 1,900) is the list it must satisfy.
   The driver's token census (comments and string literals stripped) is the guard that this stayed
   true; the combat cell will have to *retire* that guard deliberately rather than quietly.
4. **`apply_tick()` is a pure function of the tick, and FG-10 depends on it.** Any combat state that
   accumulates across frames (hit-stop budgets, flinch timers, corpse decay) breaks the property
   that makes the determinism assertion exact. Budget it as a *function of tick*, or the digest gate
   goes soft.
5. **Foot-slide is unmeasured debt** (§ 4) and combat animation will make it worse: a strike clip on
   a body already sliding reads as a slide *with* a swing. `mobcast_stride_probe.gd` is the
   instrument.
6. **The channel FX has an undeclared damage temptation.** EoR damages continuously; the wire
   carries the damage rows. The FX today has **no** per-hit behaviour, and GL-15 says arriving
   damage and ongoing damage are two deliberately unequal channels — the persistent aura already
   carries the "ongoing" half, so combat must not add a second one there.
7. **The 3.0 m ribbon is the CORE and the flares overspill it to 3.643 m** (§ 5). Any hit-region
   presentation must key to the measured radius, not to the visible bloom.
8. **GL-13's clip surface is `clip_rect()`** — 86.915 × 85.303 m, centred at sim `(-1.819, 0.244)`,
   NOT the origin and NOT the skirt. Telegraph-class ground FX clip there; the function exists so no
   consumer has to know that.
9. **The camera gate is per-frame callable and CP-C will need it per-shot** (moving cameras
   included): `camera_ground_gate()` takes a pose, not a Camera3D, so a moving camera is a loop over
   poses.
10. **Two bodies at one point** (NOTE-19) — any per-body combat marker will draw twice at
    `(2.346, -0.506)`, and nothing may separate them.

---

## 11 · Where to attack this cell

(a) The **spin rate** (0.60 s/rev) is the largest presentation invention here after the skirt's
size: it satisfies a continuity bound, not a measurement. (b) The **skirt half-extent** is a round
number chosen to be "bigger than any camera" — the gate makes the claim testable but does not derive
the number. (c) The **shot windows** are three of many defensible choices; a different three would
tell a different true story, and the manifest carries the tick spans so the framing is auditable.
(d) The **player body pick** (WR2's knight) is register precedent for a body the wire says nothing
about, and its height now comes from another run's measurement rather than mine. (e) **The FX trim**
(hiding the pack's UpwardGlow columns) is my reading of R-BR-17's discriminator applied to an asset
the ruling never saw. (f) The clip is **63.83 s across three cuts** — "one short clip" is satisfied
in file count, and argued in duration.

---

## 12 · HALT

**CP-B is a Matt checkpoint (charter § 6): the run does not proceed past an unviewed checkpoint.**
Combat presentation is NOT started and no line of it exists in the tree. Both repos pushed per PL-7.

— drax, presentation seam, 2026-08-12. *Six items, six commits, zero halts. One π/2 defect found in
my own landed work, two instrument defects found in my own new gates, and a five-metre yellow pillar
found by looking at the frames.*
