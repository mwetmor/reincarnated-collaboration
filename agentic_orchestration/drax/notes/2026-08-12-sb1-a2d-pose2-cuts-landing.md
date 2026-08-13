# SB-1 Cell A2d — POSE ROUND 2 · THE CUT PATTERN · THE LAST BUILD BEFORE THE CLIP

**Cell ID:** `SB1-CELL-A2d` · **Date:** 2026-08-12/13 · **Author:** drax (presentation seam)
**Ledger:** `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — row **A2d-0** is the charter;
**R-CPB-11** (A feet · B elbows · C occlusion) · **R-CPB-12** (the cut pattern, five clauses) ·
**R-CPB-10** (scale 1.65) · **R-CPB-7** (five stroke properties) GOVERN.
**Base:** the A2c landing `drax/notes/2026-08-12-sb1-a2c-cpbprime-landing.md`.
**Godot repo:** `e036bf1` → `01f91aa`, **five commits, pushed as they landed (PL-7).**

**VERDICT: ITEMS 0 · 1 · 2 · 3 · 4 ALL LANDED. NO CLIP RENDERED, as ordered.**
**Motion smoke 54 → 63 checks, 0 FAIL. Porcelain 230 at open and 230 at close.**
**ONE BLOCKER BANKED, NOT IMPROVISED AROUND — § 0.**

---

## 0 · THE THING THE CONDUCTOR HAS TO ROUTE, FIRST

⚑ **R-CPB-5's RULED BAND AND R-CPB-11-C's OCCLUSION LAW ARE MUTUALLY EXCLUSIVE AT
WEAPON_SCALE 1.65.** Not a preference — arithmetic, off the weapon's own vertex rings.

A2c's 2.15627 m of sweep was bought by closing both fists around the hammer's **ornate talon
pommel** — a 0.0801 m-radius flange, 0.16 m across, sitting *inside* the right fist with the talons
through the fingers. `GRIP_FRAC = 0.09` put the hands on the decoration. The lowest station at
which both fists clear onto the plain rod is **0.20**, and at 1.65 that measures **1.9593 m**:
**0.1407 m below R-CPB-5's band floor of 2.10.** No pose closes that gap. Only the scale can.

| | grip on the pommel (A2c) | grip on the rod (A2d) |
|---|---|---|
| sweep | 2.15627 m | **1.95934 m** |
| inside the ruled band [2.10, 2.35] | yes | **no, by 0.1407 m** |
| clearance to the 2.400 m standing rank | +0.2437 | +0.4407 |
| outward-facing hand vertices in steel | **92, deepest 0.0655 m** | 2, deepest 0.00427 m |

**AND THE A/B MATT JUDGED WAS PRICED AGAINST THE DEFECTIVE GRIP.** With the grip corrected, the
arithmetic inverts — measured on a probe body, **NOT BUILT**:

> **the same corrected grip at WEAPON_SCALE 1.95 measures 2.3156 m — INSIDE the band AND still
> 0.0844 m clear of the standing rank.** That is the combination *neither* scale could offer while
> the fists were on the pommel: at 1.65 the reach fell short of the band, at 1.95 the steel went
> 0.0283 m *through* the rank. Correcting the grip resolves the tension R-CPB-9 was convened over.

**NOT BUILT, and I did not build it.** R-CPB-10 pins 1.65 and the A2d charter says *"Do not build
1.95 anything."* The collision is a **smoke row** (`R-CPB-5 vs R-CPB-11-C: the band is UNREACHABLE
at 1.65 with a legal grip`) so it cannot go stale in a comment: it PASSES while the incompatibility
is real and FAILS the moment anybody resolves it. **The call is the conductor's and Matt's.**

---

## 1 · ITEM 0 — THE FEET (R-CPB-11-A) · commit `17d10a4`

> *"the feet still sit back on the heels with toes pointing upwards… the angle of the feet needs to
> be flat so that the soles of the shoes/bottom of feet flatly pin to the floor tiles."*

### 1.1 The instrument gap, closed by LOOKING first

A2c measured sole tilt **0.000°** and plant error **1.2e-07 m**. I cropped still 03 before writing a
line of code: both boots are plainly raked, toe-up, resting on a heel edge. The eye was right.

**Root cause, off the asset:** this boot's **entire underside is one ramp** — a heel edge at
y = −0.0177 to a raised point at y = +0.0114 over 0.0868 m of boot: **18.13° NOSE-UP IN THE BIND
POSE.** Its ankle-to-toe **bone** line, meanwhile, is horizontal (`_plant_stance` refuses a rig
where it is not). So A2c's *"level the foot to its rest basis"* levelled the bone line to 0.000°
exactly as it claimed **and faithfully reproduced the mesh's rake.**

### 1.2 ⚑ TWO MORE DRAFTS OF THE NEW INSTRUMENT WERE ALSO BLIND

Both are kept in the source comments, because both looked right:

1. **"the sole is the bottom 22 mm of the boot at rest."** On a raked boot that selects the **heel
   pad alone** — 12 vertices spanning 2.8 mm — and a plane fitted through a heel pad is level by
   construction. **Scored 0.0000°** on the pose Matt called toes-up.
2. **"the sole is every triangle whose skinned normal faces the floor."** The textbook answer. On
   this asset it finds **four 2 cm facets under the ankle totalling 9.6 cm²**, because only 11 of
   the boot's triangles have all three corners majority-weighted to the foot and the real underside
   triangle wraps up the point with its normal 64° off vertical. Levelling *that* buried the boot
   **6 cm under the tiles** before the next measurement caught it.

**What measures it now is what the eye was using: THE UNDERSIDE PROFILE.** The skin is evaluated on
the CPU (`vertex' = Σ w_j · bone_pose(bind_j) · bind_pose_j · v`, off LOCAL poses — no frame, no
cache); the sole SET is decided **once at rest** and re-measured **by key** at every pose; the pitch
is the least-squares slope of the lowest surface across 10 stations, heel to toe. Positive is
toes up. It is a side-elevation silhouette, computed — the exact picture Matt was looking at.

### 1.3 The fix is a CONSTRAINT (NOTE-37), and the ratified knees survive it

Five laps of **{plant the boot → bisect the pelvis drop → solve both legs → level the foot →
MEASURE THE MESH → correct pitch, roll and lift}**. The knee target is re-bisected **inside every
lap**, so Matt's *"the knees are perfect now"* is not spent on the feet.

One sign error on the way, caught by the measurement rather than by a frame: `(UP × fwd) × fwd` is
**−UP**, so rotating about `lat` by a *positive* angle takes the nose **down**. Both signs were
inverted in the first draft and drove the rake from +18.6° to **+61.9°**.

| | before (A2c) | after |
|---|---|---|
| underside pitch (L / R) | +18.57° / +18.57° | **+0.0018° / +0.0019°** |
| gap to the tiles | +0.0000 (heel only) | **±1e-05 m** |
| toe-minus-heel | +0.03150 m | **0.00000 m** |
| knee apex forward, min | +0.0741 m | **+0.0741 m** (unchanged) |
| knee flexion (L / R) | 23.17° / 26.00° | **23.17° / 26.01°** (unchanged) |

**AND THE BODY WAS 9.6 mm INSIDE THE FLOOR** — pre-existing, in every frame this scene has ever
rendered, and squarely inside the same ruling. The ground offset was `-body_aabb().position.y`, the
**bind box**, which reaches below the lowest sole vertex. It is off the **soles** now.

### 1.4 The retired instrument is kept visible — and the row REQUIRES IT TO DISAGREE

Same treatment A2c gave the bind-pose AABB: renamed `bone_*`, still reported. The new row does not
merely note the retirement, it **asserts the disagreement**: the bone-line read scores **18.14° on
the body that is flat** and scored **0.000° on the body that was not**. A check that agreed with its
replacement on both bodies would have proved nothing.

---

## 2 · ITEM 1 — THE ELBOWS (R-CPB-11-B) · commit `cab8b17`

> *"the arms are straight (or maybe bent inwards at the elbows) but there should be just a little
> bit of bend in the elbows of at least one arm (usually the right arm…)."*

### 2.1 NOTE-35 applied before any magnitude — and the axis WAS the whole defect

Measured on the A2c article, before touching anything:

| | flexion | apex | OUT | BACK | DOWN |
|---|---|---|---|---|---|
| RIGHT | **40.60°** | 0.1045 m | +0.0172 | −0.0025 | **+0.1031** |
| LEFT | 20.81° | 0.0544 m | **−0.0109** | +0.0145 | +0.0513 |

The right elbow carried **forty degrees** — more than either ratified knee — and Matt read the arms
as straight, because **0.1031 of its 0.1045 m apex pointed straight DOWN**: along the arm's own
visual axis from an elevated camera, the one projection in which a bend disappears. And the left
pointed 0.0109 m **into the torso** — his *"or maybe bent inwards"*, in metres. One shared
skeleton-space `ELBOW_POLE = (0, −1, −0.35)` produced both. **No angle threshold could have caught
either. NO MAGNITUDE WAS ADDED**; the reach moved 0.6175 → 0.6172 m.

### 2.2 Two wrong drafts, both found by measuring

1. **A world-axis pole.** The LEFT arm reaches ACROSS the midline, so 0.64 of its own direction *is*
   the character's right — a pole asking for OUT +0.4774 projected into the apex plane as
   **OUT −0.1483**. An elbow cannot be given an "outward" that is parallel to the arm. The weights
   are now applied to the **perpendicular projections** of their own directions, renormalised first.
2. **BACK weighted above OUT.** Inside the apex plane, this pose's outward and backward come out at
   a dot product of **−0.9098 (right) / −0.9863 (left)**: they are **ONE AXIS IN TWO SIGNS**. BACK
   won and flipped **both** elbows inward. Matt's ruled clause is *"never inward"*, so OUT carries
   the weight (1.00 vs 0.35). **That dot product is now a smoke row, not a comment** — if a future
   pose makes the two independent, the row fails and the weights get revisited.

**After:** apex OUT **+0.07697 (right) / +0.03026 (left)**, both above the 0.006 m bar; flexion
40.38° / 20.10° at landing, 38.71° / 21.22° after item 2 moved the grip; right dominant. Grip
re-solved and intact: **residual 0.00155 m** (bar 0.010), fists 0.09998 m apart.

**Third row has teeth:** A2c's pole is rebuilt on a second skeleton through a declared override and
reproduces **+0.01719 / −0.01091 exactly**.

---

## 3 · ITEM 2 — THE OCCLUSION LAW (R-CPB-11-C) · commit `919983c`

**Geometry, not paint order.** These are opaque depth-tested meshes; `render_priority` would draw a
fist in *front* of steel it is physically inside — the lie made worse, not better.

### 3.1 The fists were gripping the POMMEL

Haft radius, ring by ring, in body space (the fists spanned −0.48 … −0.20):

```
-0.44  r 0.0596-0.0602      -0.40  r 0.0000-0.0161  (the pommel cap)
-0.38  r 0.0643-0.0825  (96 verts: the TALONS)
-0.36  r 0.0316            -0.32  r 0.0801   <- a 0.16 m FLANGE, inside the right fist
-0.28  r 0.0535            -0.22 .. +0.14  r 0.0459   <- the PLAIN ROD
```

### 3.2 ⚑ THE FIRST PREDICATE WAS UNPASSABLE, AND THAT MATTERS

*"Any hand vertex inside the weapon"* counted **197** — because **a fist closed on a handle HAS
flesh inside the steel by construction**: the inner walls of the fingers and the palm are what the
handle occupies, and they are invisible precisely because the hand is around them. A bar of zero on
that predicate condemns every grip on every handle. The predicate is now **`inside AND its own
skinned normal faces radially outward`** — the *visible* surface of the hand, buried. Both counts
are reported so the distinction can be checked rather than taken on my word.

### 3.3 Two fixes, both pose/transform, and the seat is FORCED not picked

- **`GRIP_FRAC` 0.09 → 0.20**, the lowest station where both fists clear onto the plain rod. Still
  the bottom fifth of a 1.6 m weapon; Matt's *"near the base"* holds.
- **A RADIAL SEAT, 90° / 0.10 m**, sliding the HAND off the haft's axis so it rides the surface
  instead of being inside it. **It costs no reach** — the solve puts the grip point on the reach
  line either way, so the weapon does not move, only the hand does.

**The bar is a DEPTH, not a count, and that is a ruling about this asset.** The haft is 0.0918 m
across at 1.65 and this hand's aperture is ~0.03 m: **no pose puts a hand outside a pole thicker
than its grip and still has it touch.** A seat of 0.11 m *does* reach zero buried vertices — and
lifts the fists 0.015 m clear of the steel, a man holding a hammer he is not touching, which is the
same class of lie one layer out. Solved sweep, 7 seats:

| seat | buried | deepest | contact gap | burial ok | contact ok | LAW |
|---|---|---|---|---|---|---|
| 0.06 | 24 | 0.01694 | −0.01564 | no | yes | no |
| 0.08 | 8 | 0.02018 | +0.01053 | no | no | no |
| 0.09 | 4 | 0.01238 | −0.00962 | no | yes | no |
| **0.10** | **2** | **0.00427** | **−0.01527** | **yes** | **yes** | **YES** |
| 0.11 | 0 | 0.00000 | +0.01543 | yes | **no** | no |
| 0.12 | 0 | 0.00000 | +0.01315 | yes | **no** | no |
| 0.14 | 0 | 0.00000 | +0.04221 | yes | **no** | no |

**Exactly one value satisfies both sides.** Also measured: opening the fingers buys *nothing*
(curl 1.00 → 0.00 leaves burial at 60/49) — it was never the fingers.

**After:** 0 + 2 buried of 384 + 380, **deepest 0.00427 m** (0.25 % of body height); contact gap
−0.01527 m; **arm-vs-arm clearance 0.00925 m** over 687 × 687 skinned vertices — clause (a) held
already and improved. Teeth row rebuilds A2c's grip and still measures **92 / 0.0655 m**.

**Honest residue, declared:** 2 vertices at 4.3 mm. Covered by still 02 as the charter allows.

---

## 4 · ITEM 3 — THE CUT PATTERN (R-CPB-12) · commit `a337d30`

| clause | built as | measured |
|---|---|---|
| **1 TRUNCATION** | `CUT_PERSIST_REVS` 1.0 → **0.45**, in REVOLUTIONS (NOTE-38) | 162.0° of arc = **0.1620 s**, derived; under the 0.3–0.5 s the eye resolves |
| **2 TWO CLASSES** | SWORD = A2c's ribbon, build kept. CLAW = 3–4 stacked thinner lines, staggered leading AND trailing edges, per-line width variety. Own `CLAW_*` family. | sword 8,544 tris / claw 20,448 over 12 library meshes |
| **3 ALTERNATION** | STRICT on the global stroke index — *the ruling alternates the CLASSES and randomises the INTERVALS*, not the reverse. 11 births/rev, bin-bounded jitter. | 37 cuts over 3 revs, 19/18; intervals **21.25–44.58°** about a 32.7 mean; **all 5** vertical levels across a 0.360 m band centred on the measured 1.10796 m |
| **4 PALETTE** | white-hot → orange → **RED**, three stops, `decay_gamma` 0.55 kept below 1, last 0.28 smoothstepped out | (1.00,0.97,0.90) → (1.00,0.42,0.06) → **(0.98,0.07,0.02)** |
| **5 DETERMINISM** | hashes of (CUT_SEED 20260813, revolution, slot). No `randi()` seeded or otherwise, no RNG object, no clock, no accumulation. | 5 assert paths, § 4.2 |

**THE RADIUS IS UNTOUCHED BY ALL OF IT.** The cadence changes **WHEN**, **WHERE ALONG** and **AT
WHAT HEIGHT**, never **HOW FAR OUT** — and the weapon-truth row still proves that by re-measuring at
a second scale.

### 4.1 ⚑ THE LAYER LEFT THE SPINNING HOLDER, AND THAT IS A CORRECTION

A2c parented the ring to the body, and **for a full circle that is exactly right**: a ring is
rotationally symmetric, so a rigidly-rotating age gradient is indistinguishable from marks being
burned in and left behind. **Discrete cuts break the equivalence** — a burn mark stays where the
steel touched. Rotate the pattern with the body and the same arrangement sweeps past forever, which
is a spinning wheel, not a cadence. The cuts are **world-fixed** and the head moves past them.

**Which spends A2c's strongest structural claim, necessarily.** *"This layer has no per-tick code at
all"* is gone: clause 5 names the **REVOLUTION INDEX** as an input, and static body-frame geometry
is 1-revolution periodic **by construction**. The falsification is now a row: the layout at *t* and
at *t* + one revolution must **DIFFER** — if it did not, the revolution index would not really be
in it.

### 4.2 Determinism, five ways

1. **Banned-token scan** on the player file's CODE lines (comments stripped — NOTE-42): 0 hits
   across `Time.`, `randf`, `randi`, `randomize`, `get_ticks_*`, `RandomNumberGenerator`.
2. **No `TIME`** in the shader's code lines.
3. **The whole driven pool** — mesh id, yaw, height, age, visibility, 24 slots — **IDENTICAL**
   across `apply_tick(1717) → apply_tick(2400) → apply_tick(1717)`.
4. **Two fresh builds** (a second arena and a second player, from scratch, same process) produce a
   **byte-identical layout** at tick 1717.
5. **NOT one-revolution periodic** — the row that proves the revolution index is real.

⚑ **AND THE POOL CARRIED HISTORY IN ITS DARK SLOTS.** The first draft only *hid* unused nodes, so
each kept the mesh, yaw, height and age of whatever stroke last used it: the pool's full state
depended on **which ticks had been visited**, not on the current one. Invisible today, and exactly
the residue that becomes visible the first time another path reveals a slot. Caught by assert 3 —
which is why it compares the **whole** pool and not only the drawn ones. Every slot is written every
tick now, dark ones included.

### 4.3 Two tunings by eye, after the first build measured green

The first pattern (5 cuts/rev) measured perfectly and read **sparse** — two or three lonely arcs, not
a whirlwind. 11/rev, peak 6 alive. And the palette knee at 0.34 turned every stroke red within 16°
of the head; at **0.56** the white-hot head survives long enough to read as the leading edge.
Neither number is measurable against a ruling — both are declared taste, and the clip should decide
them.

### 4.4 Architecture

A **LIBRARY** of 12 meshes (2 classes × 6 seeded variants, 28,992 triangles, two surfaces each — 0
bloom sheath, 1 crisp core) built once and never rebuilt, drawn through a **POOL** of 24 nodes with
per-node materials. Peak 6 cuts alive, **0 pool collisions**. Per-tick work is transforms and one
uniform.

---

## 5 · ITEM 4 — THE STILLS · commit `01f91aa`

`agentic_orchestration/galadriel/captures/2026-08-12-sb1-a2d-stills/` — three 1920×1080 PNGs at the
solved tick **1602.85833** (5 cuts alive), plus `MANIFEST.json`. **Class E, untracked, never
committed.** PL-5 fired before a frame existed: **30 G free on /** (floor 8), captures **6.71 G of
the 10 G ceiling**. sha256 re-verified on disk: **3 of 3 MATCH**.

| file | what it answers |
|---|---|
| `01-feet-side-elevation.png` | R-CPB-11-A. Eye 0.215 m off the tiles, broadside. Both soles flat on the stone. **Aura hidden, declared.** |
| `02-grip-closeup.png` | R-CPB-11-B + C. Both elbows bent and pointing outward, both fists on clean steel. **Aura hidden, declared.** |
| `03-cuts-beauty.png` | R-CPB-12 frozen. The clip's own `d-close` framing, FINAL VFX ON, rings OFF, 1.65. |

**The tick is SOLVED**, not browsed: one revolution walked at frame resolution, scored on {both
classes alive} × {camera-side} × {vertical spread}.

⚑ **A STILL CANNOT PHOTOGRAPH A CADENCE (NOTE-29)** and frame 03's own subject line says so.
Alternation, truncation and the interval scatter are **temporal**; the clip is their instrument.
What the frame shows is the frozen state: discrete cuts instead of one closed ring, both classes at
once, the vertical scatter, and the white-hot → orange → red ramp. **Set beside A2c's frame 01 the
difference is unmissable: one unbroken glowing circle, then a scatter of separate cuts.**

**Three wrong framings on frame 02**, all NOTE-30's family. At fov 30 from 1.5 m it held one fist and
**no elbow** — a close-up of the half of the question already answered. Widened, it came back as a
**dark wall**: `UP × outd` picks a side by an accident of which way the solved tick left the body
pointing, and at this one it put the eye **inside the torso**. The camera is now derived from the
right arm's **own** shoulder-to-wrist line, with the side chosen by measuring which of the two is
further from the spin axis.

**The scratch eye-harness is deleted**, as declared when it was created. `_a2d_eye.gd`,
`scenes/_a2d_eye.tscn`, `run_a2d_eye.sh` existed so each item could be **looked at before it was
committed** rather than all four at the end. They found the boot rake, the pommel grip and the
sparse first pattern. Gone at item 4.

---

## 6 · THE MEASURED BLOCK

| quantity | value |
|---|---|
| hammer-tip sweep | **1.95934157916458 m** |
| cut ring radius | 1.9593415046365 m |
| cut ring height (vertical band centre) | 1.10796304047108 m |
| clearance to the 2.400 m standing rank | +0.4407 m |
| **R-CPB-11-A** sole pitch (L / R) | **+0.00184994° / +0.00190708°** |
| sole gap to the tiles (L / R) | −1.196e-05 / +9.723e-06 m |
| boot's BIND-POSE rake (the defect) | **18.1252770368159°** |
| retired bone-line tilt on the fixed body | **18.136786°** (it disagrees, and must) |
| retired bone-line plant error | 0.06926823 m |
| **R-CPB-11-B** apex OUT min | **+0.0312074292451143 m** (bar 0.006) |
| elbow flexion (min / max) | 21.2157° / 38.7081°, right dominant |
| apex-plane out·back (R / L) | −0.9098 / −0.9863 (one axis, two signs) |
| **R-CPB-11-C** outward faces buried | **2** of 764 |
| deepest burial | **0.00426835949417822 m** (bar 0.006) |
| contact gap | −0.01527 m (bar +0.010) |
| arm-vs-arm clearance | 0.00925176004148318 m (bar 0.002) |
| **knees, RATIFIED and untouched** | apex +0.0740568935871124 m; flexion 23.1705° / 26.0085° |
| pelvis drop | 0.0662409998622024 m |
| grip residual | 0.00155283743515611 m (bar 0.010) |
| hand gap | 0.0999793410301208 m |
| **R-CPB-12** persistence | **0.45 rev = 162.0° = 0.1620 s** |
| cuts per revolution / pool / peak alive | 11 / 24 / 6 |
| mean interval / measured spread | 32.727° / 21.25–44.58° |
| cut arc band | 0.055–0.140 rev (19.8–50.4°) |
| vertical band / levels | 0.360 m / 5, all used |
| claw lines / gap / width / stagger | 3–4 / 0.040 m / 0.26–0.62 of core / 0.030 rev |
| seed | **20260813** |
| library / triangles | 12 meshes / 28,992 |
| palette | (1.00,0.97,0.90) → (1.00,0.42,0.06) → (0.98,0.07,0.02); knee 0.56; gamma 0.55; fade 0.28 |
| tick (all three stills) | **1602.85833333333** |
| baton digest | `d7ecd866ac45` (MATCH, every run) |

---

## 7 · Per-item commit table (CL-2)

| hash | item | what |
|---|---|---|
| `17d10a4` | **0** | FEET — the boot's underside is raked 18.13° in the BIND POSE; three instruments scored it flat before one agreed with the eye; constraint solve, knees preserved to three decimals; body re-grounded off its soles |
| `cab8b17` | **1** | ELBOWS — a bend is a DIRECTION; 40.6° of flexion reading as straight; per-arm chest-frame pole declared IN the apex plane; two wrong drafts measured, not argued |
| `919983c` | **2** | OCCLUSION — the fists were gripping the ornate talon pommel; predicate narrowed to visible burial; grip moved to the plain rod + a radial seat forced by a two-sided bar; **the blocker banked** |
| `a337d30` | **3** | CUT PATTERN — ring truncated to 0.45 rev, two classes strictly alternating at seeded intervals and heights, palette to RED, world-fixed, seeded-deterministic five ways; pool history residue found and closed |
| `01f91aa` | **4** | STILLS — three frames, one solved tick, manifest with sha256; scratch harness retired |

**All five pushed as they landed (PL-7). Zero minutes of uncommitted work at any point.**

---

## 8 · Laws

**Zero combat lines (R-A1-1)** — **5,123 nodes walked** with the player, pose, cuts, smoke and bursts
in the tree: **0 text/canvas nodes**. No reactions, no damage numbers, no UI text added.
**GL-18 / FG-10** — one clock. The cut layer's per-tick surface is hashes of integers derived from
the sim tick; asserted five ways including two fresh builds and a non-periodicity falsification.
Scene-sim determinism digest `35f1b889ab0ebf20` ×3.
**GL-15** — one ongoing-damage read: bed + haze (2), the cut pool (24), 3 burst emitters, all gated
on the same single wire bit. **The row's claim was restated rather than its number retuned** — a
count is not a read, and twelve cuts of one whirlwind are one read.
**GL-13 / GL-12** — the pinned rectangle untouched; no absence filled. **GL-6** — the baton digest
recomputes to `d7ecd866ac45` (MATCH) on every run in this cell. **GL-17** — no assets copied, no
mesh edited, no asset mutated; every fix is pose or transform.
**ADR-006** — **no acquisitions of any kind.** No new textures; the cuts are native geometry and a
shader authored here.
**D-14** — no factory-spine coupling; all renders classic.
**Containment** — godot porcelain **230 at open, 230 at close**. `addons/` untouched in both
directions (19 untracked entries, unchanged). Meta-repo: **one new untracked capture dir**,
`agentic_orchestration/galadriel/captures/2026-08-12-sb1-a2d-stills/` (class E, 3 PNG + MANIFEST,
3.6 MB). **Engine repo — untouched.**

---

## 9 · Self-attack surfaces (ranked, veto-open)

1. **§ 0's BLOCKER is the whole cell's biggest surface.** I chose the newer, more specific ruling
   (R-CPB-11-C) over the older band (R-CPB-5's [2.10, 2.35]) and banked the collision instead of
   halting. Defensible — R-CPB-5c already re-based the generosity reference from 2.400 to 3.000 m
   and ruled sparks weapon-truth, and A2c's own note calls the band *"derived against the WRONG
   number"* — but **it is a ruling I did not have the authority to retire, and I did not retire it:
   it is still measured, still printed, still failing its own bar in the evidence string.** If the
   conductor wants the band honoured instead, the grip goes back on the pommel and item 2 reverts.
2. **The scale arithmetic in § 0 is a genuine invitation to re-open R-CPB-10**, and I am the party
   who benefits from it being re-opened (it would restore the reach my fix cost). Measured on a
   probe, not built, and stated as arithmetic rather than as a recommendation — but the conductor
   should read it knowing whose finding it is.
3. **THE CUT PATTERN IS THE LARGEST BLOCK OF DECLARED TASTE IN THE SCENE.** Cadence (11/rev),
   persistence (0.45), arc band, vertical band, palette knee (0.56), claw geometry, decay and fade:
   **eleven constants and one seed, NO WIRE BASIS whatever.** Two of them (cadence, palette knee) I
   tuned **by eye after the build measured green**, which is exactly the kind of decision a still
   cannot settle. The clip should decide them.
4. **The cut layer now HAS per-tick code**, which A2c's etch did not. It is exact and asserted five
   ways, but *"no per-tick code at all"* was a stronger structural guarantee and it is gone. It had
   to go — clause 5 names the revolution index — but the trade is real.
5. **`OCCL_BURIAL_MAX_M = 0.006` is a bar I chose**, and it is the difference between "the law
   holds" and "the law holds except for two vertices". The two-sided criterion forces the seat once
   the bar exists; the bar itself is my judgment that 6 mm on a 1.7097 m body is below noticing.
6. **The boot's 18.13° rake is an ASSET fact corrected in the POSE.** Any future clip that plays a
   Synty animation on this body will show the rake again, because the animation carries its own
   foot rotations. The fix belongs to the authored pose, not to the rig.
7. **The occlusion law is enforced at ONE POSE.** R-CPB-11-C is a standing law for every rig this
   project ships; this scene draws one frozen pose, so nothing here proves it for a moving arm.
8. **The pose is now ELEVEN declared opinions with no wire basis** — R-CPB-11 changed three and
   added the elbow-apex weights. The wire carries `circle_sweep.active` on 3,732 of 3,732 samples
   and says nothing about limbs.
9. **`GRIP_FRAC = 0.20` is asserted on its OUTCOME, not derived from the haft profile.** The profile
   is in the source comment and the sweep table is in § 3.3, but a future asset swap would need the
   number re-solved by hand rather than re-derived by code.
10. **Twenty unlicensed editor addons still stand in the tree** on A2b-r's judgment. Untouched this
    cell in either direction, per the containment pin.
11. **The helmet is still Matt's tepid "ok."** Untouched; upgrade surface open.

---

## NOTES (continuing from NOTE-44)

**NOTE-45 — REPRODUCE BY EYE BEFORE YOU BUILD AN INSTRUMENT.** A2c's harness said the soles were
flat to 1.2e-07 m. A four-second crop of its own still showed both boots plainly toe-up. The crop
came first here and it is the only reason the third instrument was built instead of the second being
trusted. **When a measurement and an owner disagree, photograph the thing.**

**NOTE-46 — A BLIND INSTRUMENT CAN BE REPLACED BY A SECOND BLIND INSTRUMENT, AND A THIRD.** Three
definitions of "the sole" scored this pose flat: the ankle-to-toe BONE line, the lowest-22-mm vertex
band, and the down-facing skinned FACES. Each was defensible; each was measuring something other
than what renders. **The replacement is not automatically better than what it replaces — make it
disagree with the old one on a known-good and a known-bad article before you trust it.**

**NOTE-47 — RETIRE AN INSTRUMENT BY REQUIRING IT TO DISAGREE.** A row that says "the old check is
retired" is prose. A row that asserts *the old check reads 18.14° on the body the new one calls flat*
is a test, and it fails if the two ever quietly converge. Same shape as the defective-form
reproduction, pointed at the instrument instead of the article.

**NOTE-48 — A BEND IS A DIRECTION, NOT A SCALAR.** Forty degrees of elbow flexion read as a straight
arm because the apex pointed along the arm's own visual axis. Any joint check that asserts an ANGLE
will pass on an article whose joint is turned the wrong way. Assert the **displacement**, decomposed
onto axes a person can name.

**NOTE-49 — DECLARE A DIRECTION IN THE SPACE IT LIVES IN.** An elbow's apex lives in the plane
perpendicular to the arm; every component of a pole along the arm is discarded. Asking for "outward"
in world axes gave **−0.1483** of outward on an arm reaching across the body. Project the basis
directions into the constrained space FIRST, then weight them.

**NOTE-50 — WHEN TWO DESIRED DIRECTIONS ARE ANTIPARALLEL IN THE CONSTRAINED SPACE, MEASURE THE DOT
PRODUCT AND PUT IT IN A ROW.** "Back and outward" sounded like two independent adjustments and came
out at −0.99. The comment explaining why one weight dominates will go stale; the row will not.

**NOTE-51 — A PREDICATE THAT NO CORRECT ARTICLE CAN SATISFY IS NOT A LAW, IT IS A BUG IN THE LAW.**
"No hand vertex inside the weapon" is unsatisfiable for a fist on a handle — the handle occupies the
hole. Narrow the predicate to what an eye can actually see (outward-facing surfaces) and the law
becomes checkable. Report both counts so the narrowing is visible.

**NOTE-52 — MAKE A TOLERANCE TWO-SIDED WHEN THE ONE-SIDED VERSION HAS A DEGENERATE SOLUTION.**
"Zero buried vertices" is reachable — by lifting the hands off the weapon. The bar that forces the
right answer is {burial below noticing} AND {still in contact}, and exactly one value in the solved
sweep satisfies both. **A single-sided bar is an invitation to satisfy it the stupid way.**

**NOTE-53 — WHEN A FIX COLLIDES WITH AN OLDER RULING, BANK BOTH NUMBERS AND MAKE THE COLLISION A
ROW.** Correcting the grip put the reach 0.14 m below a ruled band. Silently retuning the band would
have hidden a decision; halting would have shipped nothing. The collision is now a passing test that
fails the day somebody resolves it, and the arithmetic for both sides is on the desk.

**NOTE-54 — STATIC BODY-FRAME GEOMETRY IS ONE-REVOLUTION PERIODIC BY CONSTRUCTION.** Any pattern
required to vary per revolution cannot be built that way, however much one wants to keep the "no
per-tick code" guarantee. The honest replacement is a pure function of the tick plus an assert that
the layout at *t* and *t + 1 rev* **differ** — without that row, "the revolution index is an input"
is unfalsifiable.

**NOTE-55 — A POOL'S HIDDEN SLOTS ARE STATE.** Hiding a node without rewriting it leaves the mesh,
transform and uniforms of whatever last used it, so the full state depends on which ticks were
visited. Invisible until something reveals the slot. **Compare the WHOLE pool in the determinism
assert, not just the drawn part** — that is what caught it.

**NOTE-56 — A SHADER UNIFORM'S DEFAULT CANNOT BE READ BACK OFF THE SHADER.** Declare palette
constants in the script, write them onto the material, and read them off the material. The
alternative is scanning the `.gdshader` as text, which is NOTE-42 all over again.

**NOTE-57 — A CAMERA DERIVED FROM THE STATION PICKS ITS SIDE BY ACCIDENT.** `UP × outward` put the
grip shot's eye inside the torso at the solved tick, because "outward" had rotated. Derive a
verification camera from **the anatomy it is verifying**, and choose the side by measuring which one
is further from the body.

---

*Landed by drax, presentation seam, 2026-08-13. HALTED after item 4, as ordered. NO CLIP RENDERED.*
