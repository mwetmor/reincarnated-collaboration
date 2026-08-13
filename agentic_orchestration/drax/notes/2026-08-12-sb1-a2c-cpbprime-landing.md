# SB-1 Cell A2c — THE CP-B′ CLOSING BUILD · FEET · ETCH · SMOKE · YELLOW LINE · A/B

**Cell ID:** `SB1-CELL-A2c` · **Date:** 2026-08-12 · **Author:** drax (presentation seam)
**Ledger:** `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — row **A2c-0** is the charter;
**R-CPB-8** (feet/knees) · **R-CPB-7** (the etch, five ratified properties) · **R-CPB-2 + R-CPB-5c**
(smoke, damage-truth to 3.000) · **R-CPB-5b** (below-noticing) · **R-CPB-9** (the A/B instrument)
GOVERN. **Base:** the A2b-r landing `drax/notes/2026-08-12-sb1-a2br-recovery-landing.md`.
**Godot repo:** `63c94ea` → `e036bf1`, **five commits, pushed as they landed (PL-7).**

**VERDICT: ITEMS 0 · 1 · 2 · 3 · 4 ALL LANDED. 0 HALTS. NO CLIP RENDERED, as ordered.**
**Motion smoke 39 → 54 checks, 0 FAIL. Porcelain 230 at open and 230 at close.**

---

## 0 · THE THING MATT HAS TO DECIDE, FIRST, BECAUSE THE CLIP WAITS ON IT

**WEAPON_SCALE 1.65 or 1.95. The A/B stills are on the desk. Measured, not estimated:**

| | tip sweep | etch ring | vs the 2.400 m dweller ring | hammer drawn |
|---|---|---|---|---|
| **A — 1.65** | **2.15627 m** | 2.15627 m | **+0.2437 m of clearance** | 1.6481 m (96 % of his height) |
| **B — 1.95** | **2.42830 m** | 2.42830 m | **−0.0283 m — the steel is PAST the rank** | 1.9478 m (taller than the man) |

⚑ **THIS CORRECTS THE PRICE A2b-r PUT ON 1.95.** A2b-r offered it as *"sweep 2.35 m, steel 0.05 m
from the standing rank."* Measured off the weapon's own vertices in the pose the scene draws, it is
**2.4283 m** — the steel goes **through** the ring, not up to it. The old number was a linear
extrapolation off a hands radius that does not scale (the hands stay at 0.6752 m at every weapon
scale; only the hammer grows).

**That is exactly the hazard R-CPB-9 named.** The dwellers show no reactions until the combat act
exists (R-A1-1: zero combat lines this run), so steel in visual **contact** with an unreacting body
reads as passing **through** it — a K-1-class lie at the visual layer. Both frames show it plainly:
at 1.65 the etch ring stays clear of the standing rank; at 1.95 it crosses two of them.

**Neither choice can put a kill outside the visuals** — the smoke carries damage-truth to the wire's
3.000 m at both scales (§ 3). The decision is composition and honesty, not law compliance.

---

## 1 · ITEM 0 — THE FEET AND THE KNEES (R-CPB-8) · commit `a908490`

> *"the feet need to be planted and the knees slightly bent (right now the character seems to be
> resting back on heels and the knees bending backwards (inwards) which reads as inhuman."*

### 1.1 Matt read two defects. There was one, and it was an axis.

A2b-r flexed each shin about **`side`** — the **swing's** lateral axis, not the leg's — by a
**negative** angle. At `SWING_YAW −54` that axis decomposes to `0.588 · body-left + 0.809 ·
body-forward`, so one `−26°` rotation is simultaneously:

| component | effect | Matt's words |
|---|---|---|
| −15.3° about **body-left** | the ankle swings **forward** of the knee | "bending backwards" |
| −21.0° about **body-forward** | the shin leaves the thigh's plane | "(inwards)" |

**Measured on the shipped A2b-r pose:** knee apex **−0.0413 m** (left) / **−0.0183 m** (right)
*behind* the hip-ankle line, with 0.0723 / 0.0290 m of sideways break. Both signs wrong, from one
axis that was never the knee's.

### 1.2 And the boots were never on the floor at all.

Flexing a knee with the pelvis held still does not lower a body — **it lifts the foot.** Measured:
left ankle **+0.031 m**, right ankle **+0.094 m** above rest height, toes pitched **+6.5°** and
**+22.8°** nose-up. That is the heel-rock, in numbers.

### 1.3 ⚑ WHY NOTHING CAUGHT IT — NOTE-23's family, seventh instance

`pose.ground_gap_m` was `body_aabb(b).position.y`, and **Godot's AABB for a skinned mesh is the bind
box: it cannot see a pose.** It read **−0.007967 m for the rest body and −0.007967 m for a body
standing on air**, identical to 1e-9 — and the motion smoke asserted on it. **A check that cannot
fail is not a check.** Retired to `bind_pose_aabb_gap_m`, kept visible with its own basis string so
it can be *seen* to be inert, and replaced by bone-based `measure_stance()`.

### 1.4 The construction, inverted

| | old | new |
|---|---|---|
| | turn the knee by a dial; wherever the boot lands is where it is | **plant the boot** at a measured floor point; **drop the pelvis** by bisection until the deeper knee carries `KNEE_BEND_DEG`; **solve** each leg to its own planted ankle (law of cosines, knee poled along that boot's own toes); **level** the foot at the ankle so pitch and roll end at exactly zero |

Feet-on-the-floor is a **constraint the solve satisfies**, not an outcome a dial happens to give.
The three leg constants keep their names and their meanings and stop rotating bones: `STANCE_SPLIT_DEG`
is now the leg's angle from vertical expressed as a **distance along the floor** (15° → each boot
0.2009 m along the swing line), `STANCE_SPREAD_DEG` is toe-out yaw, `KNEE_BEND_DEG` is the target
flexion at the deeper knee. **The pelvis drop is arithmetic, not taste**: a 15° split plants each
boot further from its hip than the leg is long, so *some* drop is compulsory before the solve can
reach at all. Bisected: **0.0528 m**. `_roll_bone` had one caller and is deleted rather than left
lying about.

### 1.5 Result, measured

| | left | right | bar |
|---|---|---|---|
| knee apex **forward** of the hip-ankle line | **+0.0741 m** | **+0.0834 m** | ≥ +0.010 |
| knee flexion off straight | 23.2° | 26.0° | — ("slightly bent") |
| sideways break, as a fraction of forward | \| | 0.01 | ≤ 0.35 |
| sole tilt / toe pitch | 0.000° | 0.000° | < 1.0° |
| ankle + toe height error | **1.2e-07 m** | | ≤ 0.004 |
| pelvis ground-print from the boots' midpoint | 0.0369 m | | < 0.06 |

The pelvis stays **on the spin axis** — a body offset from it would *orbit* rather than spin in
place, which is a different defect from the one being fixed. **Hammer-tip sweep unchanged at
2.15627 m**: the drop is purely vertical and a horizontal radius does not care.

### 1.6 The structural assert has teeth

Four new smoke rows, and the fourth **rebuilds the A2b-r leg construction on a second skeleton** and
requires it to *still* measure hyperextended (−0.0549 / −0.0219 m, boots 0.1634 m up, toes +6.54 /
+22.77°) **and** requires the retired AABB to read the same number on that broken body as on the rest
body. If the defect ever stops reproducing, the row **fails even though the shipped body is fine**.
A regression cannot pass silently in either direction.

---

## 2 · ITEM 1 — THE ETCH (R-CPB-7) · commit `655a949`

Five ratified properties, each now a place in the code rather than an adjective in a note:

| property | where it lives | what it measures |
|---|---|---|
| **CONTINUOUS** | `_etch_ribbon`, swept geometry | **13,824 triangles**, unbroken. No particles to miss. The look Matt called "too thin and sparse" was 260 GPUParticles quads. |
| **DENSE** | 3 crossed ribbon planes × 5 rows, × 2 shells | a solid rod of light from any camera angle |
| **PERSISTENT** | `ETCH_PERSIST_REVS = 1.0` | 360.0° of arc = **0.3600 s** at the shipped 0.36 s/rev. Declared in **revolutions**, so retuning the spin keeps it a re-inscribed ring instead of a fragment. The seconds figure is derived and reported, never authored. |
| **SHARP-EDGED** | `pow(1 − rim, 2.6)` core / `1.15` sheath | crisp spine, softness pushed **out** into the bloom |
| **HOT** | core **9.0 HDR** → 0.30 HDR, white → orange | plus a thresholded glow pass on the WorldEnvironment |

**HOT is an HDR claim, not a colour claim, and that is why the environment moved.** A white-hot core
painted at 1.0 tonemaps to plain white and blooms nothing. `glow_hdr_threshold = 1.0` means
everything already in the scene — floor, bodies, both directional lights, every debug ring — blooms
**nothing**; the only surfaces the pass can reach are the ones that deliberately went HDR. A
thresholded response to a ruling, not a soft-focus filter over the run.

### 2.1 Radius is weapon-truth, and the row that proves it re-measures at a second scale

`measure_contact_band` takes the weapon vertices within **0.99 of maximum reach** — the steel where
it touches R-CPB-2's invisible circular surface — and hands the etch its ring radius (2.15627 m), its
height (1.12617 m), its angular head (−54.8°) and its stroke thickness (contact half-extent 0.1249 m
× 0.22 = 0.02748 m core). **Nothing is typed.** The smoke asserts that the only honest way there is:
rebuild the same measurement at WEAPON_SCALE 1.95 and require every number to move — 2.42830 /
1.10916 / 0.03247. *A typed radius passes every other row in the block.*

### 2.2 GL-18 / FG-10 survive by construction, not by care

The stroke is **static geometry** parented to the spinning holder: built once, never rebuilt, no
history buffer, no delta accumulation, no time read anywhere in the layer. **There is nowhere for a
second clock to enter, because there is no per-tick code at all** — `apply_tick` touches exactly one
thing on this layer, `visible`, gated on the same wire bit as everything else. Asserted structurally:
zero banned time/random tokens in the player file's code lines, no `TIME` in the shader's **code**
lines (comments stripped — the first draft failed the file for its own "there is no TIME here"
comment), and the mesh identical across three `apply_tick` calls.

### 2.3 The split is retained and now has three members

R-CPB-3b's convention held through the promotion: **ETCH_*** the dominant continuous layer,
**TRAIL_*** the GPUParticles trail **demoted to ember garnish** (260 → 110, quad 0.16 → 0.11 —
garnish does not compete with the line, and embers leaving the circle are what stop a stroke of light
reading as a drawn ring), **SPARK_*** the contact bursts, unchanged. Three families, each still
touching only itself.

**One defect caught by looking:** the first draft had `decay_gamma` **above** 1, which holds the
stroke white-hot for half a revolution and gives an after-image no after-image quality. Below 1 the
energy drops fast off the steel and then crawls. Fixed at 0.55, and the comment now says which way
round it goes.

---

## 3 · ITEM 2 — THE SMOKE BED (R-CPB-2 + R-CPB-5c + R-CPB-5b) · commit `19155f2`

**Two halves, one read (GL-15).** The **bed** is a ground mesh that carries the extent and the edge;
the **haze** is the particle field that carries the cloud. Neither is a second damage source, neither
flashes/ticks/counts, and both are gated on the same single wire bit as the etch and the bursts.

### 3.1 Why the bed is a mesh and not more particles — and this is R-CPB-5b, not taste

A particle field has a **hard** emission boundary: uniform density out to the emission radius, then
nothing. Put that at 3.000 m and **you have drawn the kill boundary**, and a player who can see the
rigging deflates. A mesh carries a **profile**, so the falloff **straddles** the wire radius:

| | value |
|---|---|
| full density inside | **2.3400 m** |
| zero density outside | **3.6600 m** |
| **exactly half at** | **3.000 m** — the wire's own `radius_m` |

There is **no radius in that profile at which the eye can find an edge.** Baked into vertex colour
from the declared constants, so no shader can disagree with them.

### 3.2 The composition the two rulings asked for, as two numbers

The etch's edge is deliberately **sharp** at 2.15627 m (weapon-truth). The bed's edge is deliberately
**soft** across 3.000 m (damage-truth). **The 0.8437 m between them is the generosity margin —
visible, and unreadable as a margin.**

Bed alpha by radius: 2.400 (dwellers) **0.855** · 2.750 **0.663** · 2.812 (kill **median**) **0.609**
· 2.9999 (kill **max**) **0.430** · 3.000 (wire) **0.430** · 3.300 **0.157**. The PM-1 histogram puts
67.2 % of kills in [2.75, 3.00); **every one of them lands where this profile is still plainly dark**,
which closes the phantom-kill hazard R-CPB-2 named.

### 3.3 ⚑ TWO WRONG DRAFTS, BOTH CAUGHT BY LOOKING

1. **380 haze particles at 0.86 peak alpha SATURATED.** Twenty layers of opaque smoke is not twenty
   times as smoky — it is one flat grey plate, measurably darker than the floor and still reading as
   a painted decal. **Cloud is variance, and variance needs overlap that is not already opaque.**
   170 at 0.30.
2. **The bed sorted in front of half the haze.** Two transparent things sort by distance, and a
   3.7 m disc's sort origin is its **centre**, so from a low oblique the bed drew over the very layer
   it exists to sit under. Pinned with `render_priority = -8`.

**And the glow levels from item 1 were wrong**, which only showed once there was something dark to
wash out. Godot's glow levels are a **blur-radius ladder** and the default includes the wide ones; a
9.0-HDR ring through those pales the whole disc from a low camera. Levels 0–3 only, intensity
0.9 → 0.55.

**ADR-006 clean:** no acquisitions. The haze samples `smoke_05_a.png` from the in-tree Brackeys CC0
bundle, unchanged from A2b-r; the bed is native geometry with **no texture at all**.

---

## 4 · ITEM 3 — THE YELLOW LINE, DECLARED · commit `1df95db`

### ⚑ THE DECLARATION

**WHAT IT IS:** `ScatterBox` — the **16 m half-extent DECLARED BOX outline** drawn on the floor at
each of the six emitter anchors, in `COL_BOX = Color(0.92, 0.74, 0.28)`.

**SOURCE PATH:** `/Users/admin/Games/reincarnated-godot/scripts/kc2_arena.gd` — constant `COL_BOX`
at the colour table, drawn in `_build_emitters()` via `_box_outline("ScatterBox", h, 0.16, Y_BOX,
box_col)` where `h = baton.placement_extents_m`, i.e. `config.arena.placement_extents_m`.

**CLASSIFICATION:** **scene-native debug draw.** Not a leftover gizmo. Not a material artifact. Not
anybody's forgotten test object. It is GL-9's own mark — *the placement primitive is the wire's shape
word, BOX, never a disc* — doing exactly the job the statics cell built it for. At any oblique camera
the near edge of one of those squares crosses the frame as a single straight yellow line, which is
why it never read as a square.

**IS IT BATON-TRUTH?** Yes. And it is **still scaffolding**, and those are not in tension. A
*measurement mark* is not a scene element, and R-CPB-9 already ruled this exact class: *"the debug
rings are SCAFFOLDING — no drawn ring ships; the player's perceived edge is the etch and the standing
front rank; D3 WW and GD EoR never draw their radii."*

**DISPOSITION: REMOVED from anything Matt judges a look from**, via one switch that takes the whole
class with it — `Kc2Arena.build_marks`. Verification harnesses default **on** (a still whose job is
to show three radii needs the radii). **The clip harness defaults OFF.** *The reason the line reached
Matt's eye at all is that `kc2_cpb_clip.gd` had no way to say no.*

**Identified by falsification, not by eye**, and the falsification is now a smoke row rather than a
sentence in this note: marks ON → `{ScatterBox 6, SweepDisc 1, EngageRing 1, Crosser 2}`, marks OFF →
`{}`, and the line leaves the frame. Recognising an amber constant in a source file is a hypothesis;
removing it and watching the line go is a test.

---

## 5 · ITEM 4 — THE A/B PAIR + THE RESHOT STANCE · commit `e036bf1`

**One run, two builds, one solved tick.** The scene is rebuilt at the second scale inside the same
process, so *"same sim tick"* is a fact about the run rather than a claim about two of them.
**`WEAPON_SCALE` is never edited** — the harness drives the declared
`Kc2PlayerChannel.weapon_scale_override` and clears it at the end, so **there is no working-tree state
to revert** and 1.65 remains the shipped constant (verified at cell close: `const WEAPON_SCALE := 1.65`).

**The tick is SOLVED, not picked.** R-CPB-9 asks for a tick with the hammer head on the *camera side*
of its arc, and that is an equation: the head's body-space angle is measured off the contact band,
the holder's yaw is a pure function of the tick, the camera's azimuth is arithmetic on the clip's own
framing. Nearest solution to the 1600 anchor: **1602.0115**.

**Framing is the clip's own, pointed at rather than re-derived** — `kc2_cpb_clip.gd` shot `d-close`,
eye `station + (2.4, 3.0, 2.7)`, look `station + (0, 1.0, 0)`, fov 48: **a true oblique, never an
overhead.** Dwellers in frame. **DEBUG RINGS OFF** (item 3's switch). **FINAL VFX ON.**
`camera_ground_gate` **PASSES** on the pose.

### 5.1 ⚑ A TICK BUG INHERITED FROM A2b-r, FOUND BY FIXING SOMETHING ELSE

`get_viewport().get_texture().get_image()` returns the **last completed frame** — the one rendered
from the state at the end of the *previous* `_process`. A spin-up ramp that stops one frame short of
the target therefore photographs the world one frame short of it, however confidently the manifest
then prints the target. **A2b-r's four stills are at tick 1599.5918, not the 1600.0000 they declare**
— 0.408 ticks, 12.2° of spin. Harmless to what those frames showed, **wrong in their manifest**, and
fixed here: the ramp lands *on* the tick.

### 5.2 The third frame, and three wrong attempts before it

The stance reshot has **the aura hidden, and the hiding declared in its own manifest row.** It is a
**verification** frame — its job is the boots and the knees; the aura is judged in 01 and 02. Three
wrong attempts first, all NOTE-30's family (*a frame that answers nothing while looking like it
does*): shot from inside the haze at 1.02 m it came back as a man in a fog bank; with only the smoke
cleared, **the etch's far arc still crossed the boots**, because a ring 1.126 m up projects low from
a high eye; and the first gating attempt set `visible` at *aim* time, which `apply_tick` rewrites
from the wire bit before the shutter. Gating is now the **last word spoken before the pixels are
read**, and the ember garnish is on the list because it hangs off the **weapon** rather than off any
of the roots — hiding "the aura" and leaving a spark in frame is a manifest saying one thing and a
picture showing another.

### 5.3 Parallax, declared (R-CPB-9's law candidate)

These are **true obliques, not overheads** — but the etch is **elevated** geometry (ring height
1.1262 m) shot from an eye 3.0000 m up, so elevated geometry still projects onto the ground stretched
about the camera's nadir by **H/(H−h) = 1.6010**. **Nothing about the reach may be measured off these
frames:** every radial number in the manifest came off the weapon's vertices, and the frames are for
**judgement**, not for measurement.

---

## 6 · THE MEASURED BLOCK

| quantity | A (1.65) | B (1.95) |
|---|---|---|
| hammer-tip sweep | **2.15627331734273 m** | **2.42829778899833 m** |
| etch ring radius | 2.15627325627332 m | 2.42829784973244 m |
| etch ring height | 1.12616896629333 m | 1.10915725231171 m |
| etch core half-width | 0.0274785602092743 m | 0.0324746608734131 m |
| weapon drawn length | 1.64814162254333 m | 1.94780373573303 m |
| clearance to the 2.400 m dweller ring | **+0.243726682657265 m** | **−0.0282977889983287 m** |
| steel past the dweller ring | **false** | **true** |
| smoke radius (damage-truth) | 3.000 m | 3.000 m |

**Scale-invariant (anatomy and pose — identical in both builds):**

| quantity | value |
|---|---|
| hands radius | **0.675202071666718 m** |
| grip residual | **0.000470405822852626 m** (bar 0.010) |
| hand gap | 0.10000929236412 m |
| elbows (R / L) | 139.398374666308° / 159.189276750088° |
| sole plant max error | **1.19209289550781e-07 m** (bar 0.004) |
| knee apex forward, min | **+0.0740707069635391 m** (bar +0.010) |
| knee flexion (L / R) | 23.1749434253674° / 26.0000456072146° |
| pelvis drop | 0.0527754742797697 m |
| smoke bed: full → zero → half | 2.3400 m → 3.6600 m → 3.000 m |
| etch persistence | 1.0 rev = 360.0° = 0.3600 s |
| tick (all three frames) | **1602.01146648256** |
| baton digest | `d7ecd866ac45…` (MATCH, every run) |

---

## 7 · Per-item commit table (CL-2)

| hash | item | what |
|---|---|---|
| `a908490` | **0** | FEET + KNEES — one wrong axis causing both halves of Matt's defect; boots planted and legs solved; the bind-pose AABB instrument retired; 4 smoke rows incl. the defective-form reproduction |
| `655a949` | **1** | THE ETCH — five ratified properties built, HDR + thresholded glow, radius weapon-truth proved by re-measuring at a second scale; 5 smoke rows |
| `19155f2` | **2** | THE SMOKE BED — darkness to 3.000 with a straddling soft edge; two saturation/sorting defects found by looking; 4 smoke rows |
| `1df95db` | **3** | THE YELLOW LINE — identified by falsification as `ScatterBox`, switched off by class, clip harness defaults off; 1 smoke row |
| `e036bf1` | **4** | THE A/B — one run, two builds, one solved tick; the A2b-r one-frame tick error found and fixed; three stills + manifest |

**All five pushed as they landed (PL-7). Zero minutes of uncommitted work at any point.**

---

## 8 · Laws

**Zero combat lines (R-A1-1)** — asserted across the whole driven tree with the player, pose, etch,
smoke bed and bursts in it: **0 text/canvas nodes**, 1,804+ nodes walked; the no-combat guard on the
driver's stripped bytes still passes. No reactions, no damage numbers, no UI text added.
**GL-18 / FG-10** — one clock. The etch has **no per-tick code at all**; every VFX state is carried
by the holder's yaw, which is a pure function of the sim tick. Structurally asserted (banned-token
scan on code lines only, `TIME` scan on the shader's code lines only, mesh identity across three
`apply_tick` calls).
**GL-15** — one ongoing-damage read: bed + haze (2 nodes), etch core + sheath (2 nodes), 3 burst
emitters, all gated on the same single wire bit. No second damage source.
**GL-13 / GL-12** — the pinned rectangle is untouched; no absence filled. **GL-6** — the baton digest
recomputes to `d7ecd866ac45` (MATCH) on every run in this cell. **GL-17** — no assets copied.
**ADR-006** — **no acquisitions of any kind.** Textures used are the two in-tree Brackeys CC0 sheets,
unchanged from A2b-r. Everything new is native geometry or a shader authored here.
**D-14** — no factory-spine coupling; all renders classic.
**Containment** — godot porcelain **230 at open, 230 at close**. `addons/` untouched in both
directions. Meta-repo side: **one new untracked capture dir**,
`agentic_orchestration/galadriel/captures/2026-08-12-sb1-a2c-stills/` (class E, 3 PNG + MANIFEST).
**Engine repo** — untouched.

---

## 9 · Self-attack surfaces (ranked, veto-open)

1. **The glow pass is a change to the SHARED arena environment.** Threshold 1.0 means nothing already
   in the scene reaches it, but **every other cell's renders inherit it** — CP-A stills included. If
   the conductor wants it scoped to the CP-B′ cells only, it moves behind a flag in one line.
2. **`STANCE_SPLIT_DEG` changed meaning.** It kept its name and its number (15°, the leg's angle from
   vertical) but it now decides a **distance along the floor** rather than a bone rotation. Same
   quantity, different mechanism. Anyone reading the old comment would be misled; the new one says so.
3. **The knee flexion is no longer a free dial.** `KNEE_BEND_DEG` now targets the *deeper* knee and
   the shallower one comes out where the geometry puts it (23.2° vs 26.0°). That is physically right
   for a split stance and it does mean one of the two knees is not directly controllable.
4. **The etch's palette, energies and persistence are declared taste.** No wire carries a colour.
   White-hot → orange, 9.0 HDR head, one revolution of afterimage. One constant each.
5. **The smoke bed is a flat ground plane.** From a very low camera it foreshortens toward
   invisibility and the haze carries the whole read. The clip's `d-close` eye (3.0 m up) is well
   above that failure mode; a ground-level segment would not be.
6. **The pose is still ten declared opinions with NO WIRE BASIS.** R-CPB-8 changed *how* the legs are
   built, not that fact. The wire carries `circle_sweep.active` on 3,732 of 3,732 samples and says
   nothing whatever about limbs.
7. **No per-revolution oscillation.** Still a deliberate absence, and the etch strengthens the
   argument: a second clock would make the etch radius time-varying, and the ring's whole claim is
   that it sits at exactly the hammer's measured reach.
8. **Twenty unlicensed editor addons still stand in the tree** on A2b-r's judgment (§ 1.2 of that
   note). Untouched this cell in either direction, per the containment pin. The fork is still the
   conductor's / Matt's and the removal command is still one line in the A2b-r landing.
9. **The helmet is still Matt's tepid "ok."** Untouched; upgrade surface open.

---

## 10 · Stills

`agentic_orchestration/galadriel/captures/2026-08-12-sb1-a2c-stills/` — three 1920×1080 PNGs, **all
at tick 1602.0115**, plus `MANIFEST.json` (sha256, bytes, camera pose, FOV, weapon_scale, debug-mark
state and aura state **per frame**, plus the full measured block at both scales, the parallax
declaration and the camera-ground-gate verdict). **Class E, untracked, never committed.**
PL-5 fired before a frame existed: **31 G free on / (floor 8 G)**, captures **6.70 G of the 10 G
ceiling**. sha256 re-verified against the manifest on disk: **3 of 3 MATCH.**

| file | weapon scale | what it answers |
|---|---|---|
| `01-scale-A-1.65.png` | 1.65 | the shipped scale, final VFX, rings off — the etch ring stays clear of the standing rank |
| `02-scale-B-1.95.png` | 1.95 | the candidate, same tick, same camera — the etch ring crosses two unreacting bodies |
| `03-stance-full-body.png` | 1.65 | R-CPB-8: both soles planted flat, knees broken forward, weight over mid-foot. **Aura hidden, declared.** |

**NO CLIP RENDERED.** The single CP-B′ clip fires in a later cell, gated on Matt's A/B pick, per the
A2c-0 charter.

---

## NOTES (continuing from NOTE-34)

**NOTE-35 — When one rotation produces two defects, look for one wrong AXIS.** Matt reported knees
bending "backwards (inwards)" — two words, and they read as two problems. They were one `−26°`
rotation about an axis 36° away from the joint's own: the component along body-left was
hyperextension, the component along body-forward was the shin leaving the thigh's plane. **Decompose
the rotation onto the joint's real axes before adding a second dial to fix the second symptom.**

**NOTE-36 — An AABB over a SKINNED mesh is the BIND box and cannot see a pose.** `body_aabb()` read
−0.007967 m for a body at rest and −0.007967 m for a body whose right boot hung 0.094 m in the air,
identical to 1e-9. Any "is it on the floor / is it in frame / how tall is it" check built on a
skinned AABB is a clean negative. Measure bones.

**NOTE-37 — Prefer a CONSTRAINT to a DIAL wherever the truth is positional.** "Knees bent 26°" is a
dial and it let the boots leave the floor. "Boots planted here, pelvis drops until the knee reaches
26°" is a constraint and the boots cannot leave the floor, because leaving is not in the solution
space. The dial keeps its name and its number; only the mechanism changes.

**NOTE-38 — Declare persistence in the UNIT THE MOTION IS IN.** The etch's afterimage is `1.0
REVOLUTIONS`, not `0.36 s`. Retuning the spin rate then keeps a re-inscribed ring; a seconds constant
would silently become a fragment at a faster spin and an overlap at a slower one. The seconds figure
is derived and reported.

**NOTE-39 — CLOUD IS VARIANCE, and variance dies at high per-particle alpha.** 380 quads at 0.86
alpha is not twenty times smokier than 20 quads — it is one flat plate, because the first few
saturate and the rest are invisible. Density comes from overlap that is *not already opaque*. Fewer,
lighter, bigger.

**NOTE-40 — A large transparent MESH sorts by its CENTRE.** A 3.7 m disc and a particle field around
it are both transparent, and the disc's sort origin put it in front of half the field from a low
oblique. Anything that is the *floor* of a composite read needs an explicit negative
`render_priority`; leaving it to distance means the camera decides your layer order per frame.

**NOTE-41 — `get_texture().get_image()` returns the PREVIOUS frame.** Anything set in `_process`
immediately before the read — camera, visibility, tick — is not in the pixels you get. Every
per-frame decision has to be made at least one frame before the shutter. This cost three wrong stills
in this cell and left a one-frame tick error in the A2b-r manifest.

**NOTE-42 — A "no clock" scanner must strip COMMENTS.** The first version of the etch's GL-18 check
failed the shader because the shader's own comment says *"there is no TIME here"*. A scanner that
reads prose will eventually pass code because the prose looked right.

**NOTE-43 — To prove a radius is not hardcoded, RE-MEASURE IT AT A SECOND SCALE.** Every other
assertion about "derived, never typed" passes trivially when only one scale is ever built. Build the
thing twice at different sizes and require the number to move.

**NOTE-44 — Identify a mystery element by REMOVING it, not by recognising it.** Matching an amber
colour constant in a source file to a yellow line in a frame is a hypothesis. Building the scene with
that element suppressed, at the same tick from the same camera, and watching the line leave is a
test — and it costs one flag.

---

*Landed by drax, presentation seam, 2026-08-12. HALTED after item 4, as ordered. No clip rendered.*
