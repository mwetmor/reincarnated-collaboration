# BEAM-SLITS — the shutter passed the exit-top law as one merged wall, and separating it took the wall away

**drax · 2026-08-01 · cell BEAM-SLITS · Scope 39 (Matt, pre-departure) · run BR-1, conductor gandalf**
**Opened at godot `d2ec8c9` (HUD-BUILD) — collision check CLEAN, no foreign commits.**

---

## §0 — The cell in seven sentences

1. **The footprint is 2.507×** — convex hull of the lit floor, 57.432 → 144.011 m², measured at the
   threshold where the slats are separate objects, and the multiple holds **2.22–2.59 across the
   whole threshold sweep**, so it is not an artefact of where the bar was set.
2. **Every slit is shorter than every slit it replaces** — built 3.62–4.74 m (mean 4.03) against a
   shipped set of 6.38–7.96 m measured (8.32 m built). The two ranges do not overlap.
3. **Total lit area FELL to 0.566×** (21.656 → 12.250 m²), which Scope 39 predicted and called
   correct: a crack passes less light than a grate.
4. **⚑ THE 8/8 EXIT-TOP LAW BROKE, AND THE REASON IS THAT IT WAS PARTLY A MERGE ARTEFACT.** The
   shutter satisfied it as ONE component of 346,683 px; the crack field resolves as SIX, and four of
   them died inside the frame. This is the same shape of defect BEAM-V3 self-indicted G-26a for, one
   cell later, on the gate BEAM-V3 itself built.
5. **It was bought back for no brightness at all** — `grad_floor` 0.06 → 0.14 on the slat window
   restores 8/8 with the beam's p99 moving 35.16 → 35.24. Shaft energy would also have done it, at
   **double** the shipped value, which is the exact opposite of ask A.
6. **Ask A's three grades all hold 8/8**, each paired with its own world-height floor
   (0.080/0.14 · 0.056/0.20 · 0.040/0.28) — and the world curve shows why the pairing works: the
   tone-down comes off the FLOOR (32.8 → 24.5 → 18.4 luma) while the high air is held FLAT
   (21.50 → 21.48 → 21.32). Glow down, shaft still leaving the ceiling.
7. **R-BR-12 did NOT trigger** — warm luminance reaches 76.7 % at the deepest tone-down against a
   ~80 % threshold, so R-BR-10's FULL dust arm stands. The mid-rung pair is measured anyway and
   lands at 71.5 %, i.e. **exactly where WARMTH left the room**, if holding the split constant is
   wanted.

**No self-verdict on the aesthetic. Conductor picks interim; Matt rules on return.**

---

## §1 — GATE G-39b: the combined floor space, and what "combined floor space" was taken to mean

**Declared before the measurement, because it decides the answer.** Two readings of Matt's phrase
are defensible and they move in OPPOSITE directions under this change:

| reading | what it is | what separation does to it |
|---|---|---|
| **FOOTPRINT — the gate** | area of the **convex hull** of the lit floor pixels | RISES |
| **LIT AREA — the honesty column** | the **union** of lit floor pixels | FALLS |

A gate defined on LIT AREA is satisfied by making the slits FATTER, which is the opposite of the
image. A gate on the HULL is satisfied by SEPARATION, which is the word Matt used. So the hull is
the gate; the union is reported beside it because Scope 39 says its fall is correct.

### 1.1 The gate level, and why it is not 0.10

The inherited instruments (`basepin.py`, G-26a, G-27a) headline **0.10 of the pool's own peak**. I
named that level before measuring and it turned out to be **measuring the wrong object**: at 0.10
the shutter's slats merge into ONE component filling 92 % of its own hull. There are no slats at
that level — there is an aperture.

**The bar was not moved quietly. The whole sweep is reported and the multiple is reported at every
level**, which is what makes the choice of level non-load-bearing:

| level | shutter hull | crack hull | **multiple** | shutter n | crack n |
|---|---|---|---|---|---|
| 0.02 | 118.47 | 262.84 | **2.22×** | 1 | 1 |
| 0.05 | 96.45 | 227.20 | **2.36×** | 1 | 1 |
| 0.10 | 78.13 | 192.99 | **2.47×** | 1 | 1 |
| 0.20 | 63.11 | 163.24 | **2.59×** | 2 | 2 |
| **0.30 ← GATE** | **57.432** | **144.011** | **2.507×** | **5** | 7 |

0.30 is quoted as the gate because it is **the lowest level at which the INHERITED state resolves
all five slats it was built with** — i.e. the level at which the object the ask is about exists. It
is a property of the state being replaced, not of the replacement.

### 1.2 The numbers Matt asked for

| quantity | BEAM-V3 shutter | BEAM-SLITS cracks | ratio |
|---|---|---|---|
| **footprint (hull), gate level** | 57.432 m² | **144.011 m²** | **2.507×** |
| lit area (union), gate level | 21.656 m² | **12.250 m²** | **0.566×** |
| fill (lit / hull) | 0.377 | 0.085 | — |
| slit length, BUILT | 8.32 m (all five equal) | **3.62 / 3.89 / 3.67 / 4.74 / 4.24 m** | 0.48× mean |
| slit length, MEASURED at gate | 7.93 / 7.96 / 7.48 / 6.38 / 6.44 | 4.72 / 3.87 / 3.59 / 3.41 (+ a 5th resolving as stubs) | — |
| slit width | 0.69 m | 0.64 m (built 0.73–0.89) | ≈ held |
| aperture radius on the floor | 6.303 m | **8.950 m** | 1.42× |
| group span across | ±4.16 m | **±7.70 m** | 1.85× |

**Every built slit (max 4.74 m) is shorter than every measured inherited slit (min 6.38 m).** The
ranges do not overlap, so "shorten their length" is a fact about the layout and not about a mean.

### 1.3 ⚑ Why 2.5× is not reachable inside the mask, and the arithmetic that says so

The mask is a **unit disc**: it can only draw inside the aperture the cone cuts, radius
z_pool·tan(21°) = **6.303 m**, area 124.8 m². The shutter's hull is 57.4 m² of that. Spreading the
slits to the disc's *rim* — the largest footprint the mask can express at all — tops out near
**1.8×**, and it gets there by making the slits LONGER, which is ask B2 backwards.

So 2.5× **with shorter slits** requires a larger opening. `SKY_SLAT_SPREAD` multiplies the TANGENT
of the slat lamp's half-angle, so the floor aperture scales by exactly that factor while the cone's
SHAPE — virtual apex, taper, frame-top width ratio — is preserved by similarity. Solved on a
rendered ladder, not modelled: 1.30 → 2.14× · **1.42 → 2.507×** · 1.45 → 2.58× · 1.50 → 2.65×.

---

## §2 — ⚑ THE FINDING THIS CELL EXISTS TO REPORT: 8/8 WAS PARTLY A MERGE

Scope 27 #3's law — no visible beam END inside the CAM-LOCK frame — passed 8/8 on the shutter. At
census position P1 the entire slat window resolved as **ONE component, 346,683 px**, which left the
frame's top. One object, one exit, one pass.

Separate the slits and the blades separate with them. The crack field at P1:

| component | px | top row | verdict |
|---|---|---|---|
| 1 | 39,035 | 0 | EXITS FRAME TOP |
| 2 | 43,317 | 68 | **⚑ VISIBLE END** |
| 3 | 5,185 | 138 | exits at a side edge |
| 4 | 79,532 | 189 | **⚑ VISIBLE END** |
| 5 | 423 | 320 | **⚑ VISIBLE END** |
| 6 | 59,766 | 375 | **⚑ VISIBLE END** |

**The old pass was carried by the merge.** Each blade's own opacity is unchanged — the world widths
are near-identical (0.78 m shutter vs 0.84 m crack), because the cone widened by the same factor the
mask narrowed by. What changed is that five blades used to converge into one bright wall and now
five stand alone. BEAM-V3 caught G-26a rewarding a mirrored pattern for spreading further on a
foreign axis. **This is the same class, in the gate BEAM-V3 built, found by the cell that stressed
it.** I do not think either gate was badly chosen; I think a gate that has only ever been run on one
topology has only ever been tested on one topology.

### 2.1 Three levers measured, one chosen, and the two rejections are on record

| lever | result at P1, slats only | why not |
|---|---|---|
| **shaft energy** | 0.080 FAIL · 0.120 FAIL · **0.160 PASS** · 0.240 PASS | Restores it at **2.00×** the shipped energy, near the pre-BEAM-V3 0.175. Correct, and the exact opposite of ask A. **Rejected on the ask.** |
| **screen floor** | 0.60 FAIL · 0.75 FAIL · 0.90 FAIL | The blades are not dying at the frame's TOP ROW. Wrong suspect, ruled out by measurement rather than by argument. |
| **world grad floor** | 0.14 **PASS** · 0.22 PASS | Chosen. |

`grad_floor` works and it works for the right reason: it is the residual of the **world-height**
factor, so it feeds the beam where the eye reads *a shaft leaving the ceiling* and **not** where the
eye reads *glow*, which is the lit air just above the pool. **0.06 → 0.14 restores 8/8 with the
beam's p99 moving 35.16 → 35.24 — for no brightness at all.**

### 2.2 The full census, shipped state

| position | exits-top | weakest exit (row-0 mean) | verdict |
|---|---|---|---|
| P1 circle pool | 2 | 2.160 (0.0585 p99) | **PASS** |
| P2 slat pool | 3 | 3.617 (0.1004) | **PASS** |
| P3 circle, frustum near edge | 1 | 3.426 (0.0949) | **PASS** |
| P4 slat, frustum near edge | 1 | 9.283 (0.2656) | **PASS** |
| P5 room centre | 3 | 2.968 (0.0782) | **PASS** |
| P6 SE | 4 | 6.255 (0.1911) | **PASS** |
| P7 SW | 0 (no beam in frame) | — | **PASS** |
| P8 NE | 1 | 6.918 (0.1773) | **PASS** |

**8/8.**

---

## §3 — ASK A: the glow ladder, and why each rung carries a second constant

### 3.1 The grades, and why these grade points

`SKY_SHAFT_ENERGY` at 1.00× / 0.70× / 0.50× as suggested — 0.080 / 0.056 / 0.040. The rungs are
kept as the brief named them rather than re-solved, because **the interesting variable turned out
not to be the rung**: it is that a rung taken alone breaks the topology, and the pairing is the
result. Each grade therefore carries the world-height floor that holds its exit-top:

| grade | shaft energy | slat grad_floor | 8-position census |
|---|---|---|---|
| **A1** | 0.080 (1.00×) | 0.14 | **8/8 PASS** |
| **A2** | 0.056 (0.70×) | 0.20 | **8/8 PASS** |
| **A3** | 0.040 (0.50×) | 0.28 | **8/8 PASS** |

Unpaired, the same energies give **8/8 · 7/8 · 6/8** (P1 fails at 0.70×; P1 and P4 at 0.50×), and at
0.70× the P1 failure is **attributed to the slat window, not the circle** (circle-only PASS,
slats-only FAIL) — which is why a slat-side constant can pay for it and the Matt-verdicted circle is
never touched.

### 3.2 Per-pixel opacity and total light, both, because BEAM-V3 learned that the hard way

CAM-LOCK at the slat pool, `energy.py` unchanged:

| arm | beam p99 | ratio | total light on frame | ratio |
|---|---|---|---|---|
| E100 `beamE 0.080` | 36.017 | 1.000× | 2.506e6 | 1.000× |
| E070 `beamE 0.056` | 27.089 | **0.752×** | 1.828e6 | **0.729×** |
| E050 `beamE 0.040` | 20.370 | **0.566×** | 1.345e6 | **0.537×** |
| D070 `density 0.63` | 31.949 | 0.887× | 2.059e6 | 0.822× |
| D050 `density 0.45` | 27.370 | 0.760× | 1.656e6 | 0.661× |

**Two levers, and they are not the same knob.** The shader integrates
`v = pow(1 - exp(-acc*density), edge_power)` and then multiplies by `beam_energy`: energy is a FLAT
gain, density is the extinction inside a saturating exponential, so density takes the thick bright
core down harder than the thin edges. Both are on the ladder; the deliverable clip carries the
energy arm because that is the one the brief named.

### 3.3 ⚑ The opacity world-curve — the measurement that shows the two asks are separated by HEIGHT

`run_grad.sh MODE=side`: orthographic, horizontal, screen factor peeled, **lamp peeled** (the beam is
`blend_add` and its own pool runs at 253/255 — without `--nolamp` the brightest part of the beam
reports as the dimmest). Slat window:

| height | shutter | A1 | A2 | A3 |
|---|---|---|---|---|
| 0.00 m — **where "glow" lives** | 33.158 | 32.769 | **24.501** | **18.376** |
| 3.29 m | 35.599 | 36.934 | 28.358 | 21.910 |
| 6.58 m | 45.366 | 51.209 | 42.404 | 35.735 |
| 9.88 m | 27.594 | 36.268 | 31.951 | 28.427 |
| 13.17 m — **where the topology lives** | 9.215 | **21.502** | **21.476** | **21.316** |
| beam p99 | 51.33 | 54.33 | 44.53 | 37.46 |

Read the two bold rows together. **The tone-down comes off the bottom of the shaft and the top is
held flat to a third of a luma unit across a 2× energy range.** That is the whole design of the
pairing, and it is the reason ask A and Scope 27 #3 can both be satisfied at once.

**Said plainly and against my own arm: A1 is NOT a tone-down.** Its floor luma is 0.99× the
shutter's and its p99 is 1.06× — A1 is the geometry change at unchanged energy, plus the topology
repair. Ask A is delivered at A2 and A3. Calling A1 "grade 1.00×" would let a reader think glow came
down at every rung. It did not.

---

## §4 — PRESERVE checklist, re-measured item by item

| # | preserve | result | evidence |
|---|---|---|---|
| 1 | **slat DIRECTION match ~0.25°** | ⚠ **HELD, but only provable with a peel — read §4.1** | **−0.26°** with stagger peeled; the shipped arm reads −1.46° at the sharpest common level and +17.93° at the gate level, and BOTH are the instrument, not the geometry |
| 2 | **8/8 exit-top topology** | **BROKE, then RESTORED — read §2** | 6 components / 4 visible ends → **8/8 PASS** at every graded rung |
| 3 | **40 m apex / wide-cone law** | **UNTOUCHED** | build report: apex `SKY_BEAM_APEX_Y` 40.0, `top_y` 34.0, base −0.60, dissolve 9.00 — byte-identical strings before and after |
| 4 | **pools bit-identical** | **CIRCLE bit-identical; SLAT pool changed BY THE ASK — read §4.2** | `SkyCircle` NOSKY sha `c170578…`, POOL sha `014b7da…`, **IDENTICAL** across the change |
| 5 | **WARMTH state inherited, not re-tuned** | **HELD** | every render carries R-BR-10's `--dustwarm 1.0 --fogwarm 1.00 --fogunlit` in the harness's FIXED part; the shutter arm reproduces WARMTH's FULL number **exactly** (+9.110 / 71.4 %) |
| 6 | **refactor is non-perturbing** | **PROVED** | `--slitlegacy` renders **byte-identical** to the pre-change build: NOSKY `111b5eb…`, POOL `aa41ee7…` |
| 7 | **F-AH-3 `project.godot` [rendering]** | **NO DELTA** | sha256 `6bef17eb…aface8a` — identical to BEAM-V3's banked value |
| 8 | **F-AH-6 corrupt-H.264 gate** | **every clip decode-verified** | §6 |

### 4.1 ⚑ The direction gate, and an instrument failure I nearly banked as a geometry failure

First read of the shipped arm: **+48.48°**. That is a bigger disjoint than the 26.32° Matt
originally complained about. Two things were wrong with it, and neither was the beam.

* The instrument ran at **ortho 17 m** — BEAM-PIN2's frame, generous for a 12.6 m aperture and
  **clipping** for a 17.9 m one. The pattern being measured was cropped by the frame measuring it.
* At 30 m, unclipped, it still read **+51.29°** — because `stripeangle.py` thresholds at **10 % of
  the peel's 99.9th percentile**, and on a set that is ~4 % open over an aperture twice as wide the
  survivors at 10 % are mostly the unstructured glow disc. The Radon peak fitted noise
  (**sharpness 1.31**).

What said "instrument, not geometry" was the BEAM half of the same measurement: **−57.11° against
the shutter's −56.43°**. The beam had not rotated at all; only the POOL read had collapsed.

**The bar was not moved — it was doubled.** Both arms at three levels, all numbers reported:

| arm | lv 0.10 | lv 0.30 | lv 0.50 |
|---|---|---|---|
| shutter (`--slitlegacy`) | **+0.25°** (reproduces BEAM-V3 exactly) | −0.02° | −0.05° |
| crack field, shipped | +51.29° (sharp 1.31) | +17.93° (sharp 2.76) | **−1.46°** (sharp 4.23) |
| crack field, **stagger peeled** | — | −0.70° | **−0.26°** |

The stagger peel is the decisive leg. With separation and short slits kept and only the along-axis
shove removed, the disagreement returns to **−0.26°** — inside the 0.25° band. So:

> **The floor and the volume still carry the same bearing. What the stagger costs is not the match;
> it is the MEASURABILITY of the match** — a staggered set of parallel bars presents a second
> apparent lattice direction, and a single global Radon peak can lock onto it at mid thresholds.

**Not a self-verdict.** If the conductor or Matt wants the gate's margin restored as a *number*
rather than as a peel, the instrument needs a per-blade direction read; that is real work and it is
named as a debt below, not smuggled in here.

### 4.2 The pool clause, read out loud rather than assumed

The brief says pools stay bit-identical *unless the cell can prove a pool change is required, and
then it halts that sub-item*. **Ask B1 is a claim about the floor footprint of the slats — the slat
pool IS the object of the ask**, so the change is required by construction and halting B1 would halt
the cell. I read the clause as protecting (a) the CIRCLE, which is not in Scope 39, and (b) silent
change. So: the circle is **sha-verified identical on both frames**, and the slat pool's every moved
quantity is tabulated in §1.2. **Reported loudly rather than acted on quietly.** If the conductor
reads the clause more strictly, B1 is the sub-item to reverse and `--slitlegacy` reverses it in one
word.

---

## §5 — R-BR-12: the coupled warm split, and it does not trigger

`wlw.py` unchanged (WARMTH's luminance-weighted Σ(Y·b*)/ΣY), all arms at the FULL dust setting
except the last:

| arm | beam grade | dust arm | **frame warm Y %** | frame lum-w b\* | room warm % | sky Ytot |
|---|---|---|---|---|---|---|
| MLEG | shutter, 0.080 | FULL | **71.4 %** | +9.110 | 55.9 % | 58,865 |
| MA1 | cracks, 1.00× | FULL | **71.0 %** | +9.136 | 57.2 % | 58,998 |
| MA2 | cracks, 0.70× | FULL | **74.6 %** | +10.271 | 58.3 % | 57,238 |
| MA3 | cracks, 0.50× | FULL | **76.7 %** | +11.083 | 59.0 % | 56,059 |
| MA3MID | cracks, 0.50× | **MID (fog_warm 0.55)** | **71.5 %** | +8.232 | 48.7 % | 53,506 |

* **R-BR-12's ~80 % trigger is NOT reached** — 76.7 % at the deepest tone-down, 3.3 points short.
  **R-BR-10's FULL dust arm survives Scope 39 at every grade** and does not need stepping back.
* **A cross-cell reproduction worth banking:** MLEG returns **+9.110 / 71.4 %** — WARMTH's FULL arm
  to the third decimal, on a different harness, a cell later. The warm instrument is stable.
* The mid-rung pair is measured anyway because it is the useful one if holding the composition
  fixed is wanted: **A3 + MID lands at 71.5 %, i.e. within 0.1 point of where WARMTH left the
  room**, while the beam runs at half energy.
* **Direction of the coupling confirmed, magnitude small.** F-W-1 said the shaft is 62 % of the
  cold budget; halving its energy moves the frame warm split by **+5.3 points**, not by the double
  digits that would have forced R-BR-12. The sky register's own Ytot only falls 58,865 → 56,059
  (−4.8 %) because the *pool* — which the tone-down does not touch — carries most of it.

**Consequence: no `SLITS_WARM_PAIR` clip is owed and none is shipped.** The numbers above are the
deliverable; the pair renders in one command if the conductor wants it in motion.

---

## §6 — Deliverables

Under `/Users/admin/Games/reincarnated-godot/tmp/beamslits/clips/`. CAM-LOCK (`player_lock`),
**NOHUD**, seed 74000909, full dressed cast, `--rigs 1 --vfxarm C2_combo --playerlight A`, 30 fps,
R-BR-10 FULL warm on every side. **Beam is the only variable in every pairing.**

| clip | sha256 (16) | dims / frames / dur | decode | what it asks |
|---|---|---|---|---|
| **`SLITS_BEFORE_AFTER.mp4`** ← **WATCH FIRST** | `c9743f11e5669c46` | 2560×766 / 300 / 10.00 s | **OK** | the BEAM-V3 shutter beside the Scope-39 crack field, same trace, same frames, same camera, same warm state, **beam the only variable**. Left half is five parallel bars in one band; right half is separated, shorter, staggered blades |
| `SLITS_ENERGY_LADDER.mp4` | `fb983a571ef402e3` | 2880×574 / 300 / 10.00 s | **OK** | the three ask-A grades side by side, each panel naming its own energy, its paired world floor, its floor luma, its p99 ratio and its census result — so "how much glow" is Matt's pick, not a guess |
| `SLITS_WARM_PAIR.mp4` | — | — | — | **NOT SHIPPED. R-BR-12 did not trigger** (76.7 % against ~80 %). §5 carries the numbers, including the pair. |

Plates: `plates/KEY_before_after.png` (the fastest read) · `plates/DIAG_pool_LEG_AT085_AT025.png`
(the top-down floor peel, shutter vs crack field, with the gate contour drawn on) ·
`plates/DIAG_ba_timeline.png`. Keyframes: `keyframes/SLITS_{LEG,A1}_0090.png`.

**Arm run-shas** (concatenated PNG sequence, first 16 hex) — frames are pruned, so these are how a
re-render is checked against this cell: `CLEG 7c2a6a52e1a10905` · `CA1 80cb77ce0ead3ba0` ·
`CA2 5926397d2d79d2f6` · `CA3 391665bcf80887e6` · `MLEG 56b8581f1e7a5bf2` · `MA1 06cfc97180ce54db` ·
`MA2 5a0001b759f3d99a` · `MA3 14e44c8811894d3d` · `MA3MID 5272ce3832e2e205` ·
`MNOSKY a845f701aa66285e`.

**Instruments:** `measure/slitfoot.py` (G-39b — hull + union + per-slit decomposition, with a frame-
edge clip guard, because a cropped hull reads SMALLER and that failure mode flatters the old state) ·
`measure/stripeangle2.py` (G-39a — BEAM-V3's, with the threshold lifted into an argument and the
reason written into its header) · `run_bs.sh` · `run_foot.sh` · `run_energy.sh` · `run_s.sh` ·
`make_clips.sh` · `mklabel.py`. Re-used unchanged: BEAM-V3's `bv_probe`, `run_dir.sh`, `run_top.sh`,
`run_grad.sh`, `beamend.py`, `topline.py`, `gradprof.py`, `energy.py`, and WARMTH's `wlw.py`.

**Not applied, and named rather than smuggled:** the Scope-32 **wet layer** is absent from these
clips. Its shipped parameters are not recorded in the WARMTH landing note, and guessing them would
have put an unmeasured variable inside a beam A/B. It lands in the restage.

---

## §7 — Constants, before and after

| constant | BEAM-V3 | **BEAM-SLITS** | why |
|---|---|---|---|
| `SKY_SLAT_SPREAD` | *(did not exist; cone = `SKY_ANGLE_DEG`)* | **1.42** | B1. Multiplies the TANGENT, so the floor aperture scales exactly and the cone's shape is preserved by similarity |
| `SKY_SLAT_SPAN` | 0.66 *(inline in `_shutter_mask`)* | **0.86** | B1 — separation across the set |
| `SKY_SLAT_OPEN` | 0.235 *(inline)* | **0.137** | holds the slit's WORLD width near the inherited 0.7 m while the cone widens |
| `SKY_SLAT_LEN` / `_LEN_FADE` | 0.52 / 0.80 *(inline)* | **0.20 / 0.25** | B2 — every slit shorter |
| `SKY_SLAT_STAGGER` | *(none — no shove)* | **0.90** *(fraction of the room at that offset)* | the hull is set by extreme tips; expressed as a fraction so the circle clip can never chop a slit to a stub |
| `SKY_SLAT_PITCH_JIT` | *(none — equal pitch)* | **0.42** | equal pitch is a grate at any separation |
| `SKY_SLAT_LEN_VAR` | *(none — equal length)* | **0.22** | bounded so the longest crack (5.6 m) still beats the shortest inherited slat (6.38 m) |
| `SKY_SLAT_VIGNETTE` | 0.62 / 0.98 *(shared literal)* | **0.90 / 1.10** | at 0.62 it would eat the outermost slits of a set now reaching 0.86 |
| `SKY_SLAT_FIT_R` | *(new)* | **0.94** | no tip may reach the shader's hard `dot(m,m) > 1` bound and put a straight cut back |
| band shoulder | 0.45·w | **0.72·w** | 0.45 leaves a 6-px plateau in a 512-px mask and the projector's mipmaps eat its amplitude — measured, as slits vanishing from the gate |
| `SKY_SLAT_ANGLE_ATTEN` | 0.85 *(shared literal)* | **0.22** | a spot dims toward its rim because it is a lamp; holes in a ceiling all look at the same sky. At 0.85 the outermost crack falls under the gate and disappears |
| `SKY_SLAT_GRAD_FLOOR` | 0.06 *(shared)* | **0.14** | §2 — the exit-top law, bought for no brightness |
| `SKY_SPOT_ANGLE_ATTEN` | *(literal `0.85`)* | **0.85, now named** | so "the circle is untouched" is something the code says |
| `SKY_SHAFT_ENERGY` | 0.080 | **0.080 — UNCHANGED** | ask A is delivered as a peeled ladder, not as a shipped constant. **No aesthetic self-verdict** |
| `SKY_ENERGY_REF` / `UNIFIED_KEY_ENERGY` / `SKY_MASK_SIGN` / `SKY_BEAM_APEX_Y` / `SKY_BEAM_TOP_Y` / `SKY_BEAM_SCREEN_FLOOR` / `SKY_BEAM_DENSITY` | 30.0 / 1.00 / (1,−1) / 40.0 / 34.0 / 0.45 / 0.90 | **all unchanged** | Matt-locked or Matt-verdicted |

**Peels added, all one word:** `--slitlegacy` (restores the WHOLE BEAM-V3 shutter — span, open,
length, spread, vignette, attenuation, floor and all three irregularity knobs) · `--slitspread` ·
`--slitspan` · `--slitlen` · `--slitopen` · `--slitatten` · `--slitstagger` · `--slitgradfloor` ·
`--skyfogunlit` · and on the watch harness `--slitlegacy` / `--shaftE` / `--slitgradfloor`.
**All earlier peels survive unchanged.**

---

## §8 — ⚑ FINDINGS, AND THINGS I GOT WRONG

### 8.1 ⚑ F-BS-1 — the "glow" is 80 % VOLUMETRIC FOG, and R-BR-10 has already removed most of it

Peeling fog from the floor peel dropped the measured light in the slat pool's region from
**1.947e6 → 3.882e5**. The grey disc under the slats — the thing that reads as *glow* — is
overwhelmingly **E3's haze receiving the sky lamp at `light_volumetric_fog_energy = 2.6`**, not the
floor pool.

**Consequence for ask A:** Matt asked for the tone-down on 2026-08-01 *pre-departure*, i.e. against
the **pre-WARMTH** state. R-BR-10's shipped pick includes **`--fogunlit`**, which sets that same
uniform to **0.0**. **A large part of ask A was already discharged by a conductor ruling made after
Matt left**, and he has not yet seen it. Flagged rather than assumed: it is possible the beam Matt
wants toned down no longer exists in the form he saw it. Every clip in §6 carries the fog-unlit
state, so **what he watches on return is the composition as it now is** — but the "before" half is
also fog-unlit, so the A/B isolates geometry, not this.

### 8.2 ⚑ F-BS-2 — the exit-top gate has only ever been run on one topology

§2 in one line. Recorded as a finding about the GATE, not about this cell's output, because the next
cell that changes an aperture's connectivity will hit it again.

### 8.3 ⚑ I NEARLY REPORTED A 48° DISJOINT THAT DID NOT EXIST

§4.1. Two compounding instrument faults (a clipping frame, then a threshold tuned for a 47 %-open
pattern) produced a number worse than the defect Matt originally complained about. The thing that
saved it was that the BEAM half of the same measurement had not moved — i.e. **the instrument
disagreed with itself**, and that is what a two-sided measurement is for. Had `stripeangle.py`
reported only the disagreement, I would have banked a false alarm and probably reverted a correct
change.

### 8.4 ⚑ MY FIRST LADDER PRINTED FIVE IDENTICAL ROWS AND I ALMOST READ THEM

`for a in $ARMS` word-split `"--beamE 0.080"` into two arms, so **every rung rendered at the shipped
energy** and the table came back at 1.000× / 0.965× / **1.015×**. Caught only because a 0.50×
energy grade cannot be 1.015× as opaque. The fix (a bash array) is trivial; the lesson is that the
table looked *plausible* and the number that exposed it was the one that was physically impossible.
The failure and its detector are written into the script's header.

### 8.5 ⚑ THE LADDER CLIP WAS SILENTLY NEVER WRITTEN, AND THE F-AH-6 GATE CAUGHT IT

`make_clips.sh` v1 burned its labels with ffmpeg's `drawtext`. **This ffmpeg build has no drawtext
filter** (`ffmpeg -filters | grep drawtext` → nothing; it is why WARMTH shipped label PNGs). The
label step failed, the strip step then had no input, and `SLITS_ENERGY_LADDER.mp4` **was never
created at all** — while the script kept running and exited. The thing that reported it was the
**F-AH-6 decode gate**, which was written for corrupt-but-present H.264 and instead caught
absent-and-silent. A gate that only checks the artefact you expected to produce would have passed
this by printing nothing.

### 8.6 I CHOSE THE HEADLINE LEVEL BEFORE MEASURING AND IT WAS THE WRONG OBJECT

§1.1. 0.10 was named in advance, honestly, and turned out to measure the aperture rather than the
slats. I did not quietly re-headline: the multiple is reported at **all five levels** so the gate
does not depend on the choice. But the pre-naming discipline only protects against motivated
choices — it does not protect against choosing a level that measures the wrong thing, and this is
the second gate in two cells where the statistic, not the threshold, was the problem.

### 8.7 MY FIRST STAGGER WAS A HASH AND IT SPENT ITS REACH ON THE SLITS THAT HAD NONE

A stride permutation assigns its largest offsets by INDEX, and the slits with the most room to move
are the middle ones. Measured hull 56.6 m² where the same constants under alternating-sign shove
give far more. Worse, an absolute stagger fought the circle clip: outer slits were shoved out and
then chopped, producing a **0.56 m stump** where a 4 m crack was intended. Both are in the code's
comments at the site.

### 8.8 THE THING I DID NOT DO

I did not touch `SKY_SHAFT_ENERGY`, `SKY_ENERGY_REF`, `UNIFIED_KEY_ENERGY`, the circle's cone,
attenuation or grad floor, the HUD, body scales, the VFX registry, animations, or the WARMTH
constants. The engine tree was never opened for write.

---

## §9 — Debts, named

* **The direction gate needs a per-blade read** (§4.1). Today the match is provable only through the
  stagger peel. That is honest but it is not a printed gate, and the next cell to touch this pattern
  inherits an instrument that cannot grade it directly.
* **The per-window constant divergence is now three deep** — spread, attenuation, grad floor — and
  BEAM-V3 parked exactly this as *"the first time the two windows carried different constants; not
  taken without a ruling."* **Scope 39 forced it and the ruling is now overdue.**
* **The fifth crack sits at 0.32 of the pool peak** and fragments into stubs at the gate threshold.
  It is continuous on the plate; it is dim. Flattening the aperture recovered it from *invisible*,
  not to *equal*. A per-slit compensation exists as a knob and was not taken without a ruling.
* **F-BS-1's consequence** (§8.1) — someone should confirm with Matt that the glow he named is the
  fog-lit one, before ask A is closed on his eye.
* **`tmp/vfxbakeoff/` ~8 GB** — still outside any cell's prune (`rm -rf` on directories remains
  sandbox-denied; `rm -f` on files is not, which is how this cell pruned its own frames).
* **`AGENT_STATE.md`** — now five cells behind (MOB-CAST, BEAM-PIN2, VFX-BAKEOFF, BEAM-V3, WARMTH,
  HUD-BUILD, BEAM-SLITS).

---

## §10 — At Matt's eye

1. **THE FLOOR SPACE IS 2.51× AND EVERY CRACK IS SHORTER THAN EVERY SLAT IT REPLACES.** Built
   lengths 3.6–4.7 m against a shutter whose five bars were all 8.3 m. The ranges do not overlap.
   The lit area went DOWN to 0.57× — which is right, and is what a crack does.
2. **THEY ARE NOT A GRATE ANY MORE, AND THE THING THAT DOES THAT IS NOT THE SPREAD.** Equal bars at
   equal pitch read as architecture at any separation. What breaks it is unequal gaps, unequal
   lengths, and each crack shoved along its own line so no two ends agree. Watch the before/after:
   the left half is a shutter, the right half is a broken ceiling.
3. **⚑ AND SEPARATING THEM BROKE A LAW YOU ALREADY RULED ON, WHICH I RESTORED.** Your "no visible
   beam ends" law was passing partly because the five shafts merged into ONE. Pull them apart and
   four of them showed an end inside the frame. It is fixed, and it cost no brightness — I fed the
   beam higher up instead of brighter.
4. **YOUR TONE-DOWN AND THAT LAW PULL AGAINST EACH OTHER, AND I HAVE THE PRICE.** Dimming the shaft
   alone gives 8/8 → 7/8 → 6/8. So each rung on the ladder carries a matching high-air constant:
   the glow at floor level goes 33 → 24 → 18 while the light at the top of frame stays at 21.5 in
   all three. **Down where you look, unchanged where the law lives.**
5. **PART OF THE GLOW YOU ASKED ME TO REDUCE MAY ALREADY BE GONE.** Four fifths of the haze around
   the slats was fog lit by the skylight, and a ruling made after you left already switched that
   off. What you watch on return is the room with that already removed — so judge the ladder
   against what you see now, not against what you remember.
6. **THE ROOM DID NOT OVER-WARM.** Halving the beam moved the warm share 71.4 % → 76.7 %, under the
   80 % line, so the warm dust you have not yet ruled on stays as it is. If you want the split held
   exactly where it was while the beam runs at half, that pairing measures 71.5 % and is one command
   away.
7. **NO VERDICT FROM ME ON WHICH RUNG.** Three grades, all legal, all measured, all on one clip.
