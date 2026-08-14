# SB-1 Cell A2g-r — THE LOOK DISTANCE · THE BOOM LANDED, THE GATE WENT RED, NOTHING PROMOTED

**Cell ID:** `SB1-CELL-A2g-r` · **Date:** 2026-08-13 · **Author:** drax (presentation seam)
**Ledger:** `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — **R-CPB-17** (Matt's distance ruling)
GOVERNS; **A2gr-0** is the charter; **R-CPB-16** (the lens), **R-CPB-15** (the rate) and
**CLK-1-1 / CLK-1-2** (the clock) are the inherited state.
**Base:** `drax/notes/2026-08-13-sb1-a2g-canon-landing.md` (the cell this revises) and
`drax/notes/2026-08-13-sb1-clk1-clock-landing.md` (the clock, untouched).
**Godot repo:** `03436f8` → `4646dd2` → `9e6068d`, **two commits, pushed as they landed (PL-7).**
**Collab repo:** `97092e6d` (the promote tool) + this note.

---

## ⚑ VERDICT

**THE BOOM IS LANDED AND VERIFIED — 72.857142857142857 m, READ FROM THE RIG, PIN DELTA ZERO, AND THE
FRAME IT PRODUCES HITS EVERY PRE-REGISTERED NUMBER INCLUDING THE ONE THAT MATTERS: THE MAN IS BACK AT
12.99 % OF FRAME HEIGHT. AND THE CLIP IS NOT PROMOTED, BECAUSE FG-10 WENT RED ON ONE LEG OF FIVE.**

⚑ **THE ONE THING THE CONDUCTOR NEEDS FIRST: THE RED LEG IS NOT THE BOOM'S FAULT, AND I CAN PROVE THE
NEGATIVE RATHER THAN ASSERT IT.** The two demoted-diagnostic legs came back at
`0253761a43b374b9…` and `504b6d8b4c0929ff…` — **CLK-1's digests and A2g's digests, character for
character, in a third cell at a third commit.** The host is deterministic, the session's load is
exonerated by its own bit-perfect legs, and nothing outside `_canon_pose` moved a pixel. What is red
is **one cell of the matrix**: canon frame · undulating · window 1570 · full span. Its two
neighbours — the same frame stationary at full span, and the same frame undulating at window 1660 —
are **bit-perfect across four passes**.

| item | commit | what |
|---|---|---|
| **1** | `4646dd2` | **THE BOOM** — the struck law, the rig read, the pin, and NOTE-80's wiring fix |
| **1b** | `9e6068d` | the boom's own print was printing its **format string** (NOTE-81) |
| **2** | `97092e6d` | the promote tool re-pointed at the ruling — **PREPARED, NEVER RUN** |
| **3** | *(this note)* | evidence. **NO MP4. NO MANIFEST. Nothing promoted. FG-9's deliverable path never entered.** |

**HALTED ON A RED GATE, per the charter's own instruction.** The honourable fallback is the charter
working.

---

## 0 · THE GATES THAT RAN BEFORE ANYTHING WAS TOUCHED

**GL-6 FIRST.** Baton `kc2-baton-v1-E-s09-cp150-20260809_052836.json` recomputed from bytes =
`d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa`, **1,065,632 B — MATCH**, before a
line was read. Re-asserted by the arena's own gate (`digest d7ecd866ac45 (MATCH)`) on every one of
the 21 process launches this cell made.

**PL-5 BEFORE FRAMES.** Captures **6.751 G of 10 G**, disk free 24.3 G — checked in the shell AND
again inside the Godot harness before a single frame was built. At close: **6.751 G, delta under
1 MB** (the evidence text files; no MP4 exists to have grown it).

**CONTAINMENT AT OPEN.** godot **229 untracked**, one dirty tracked file
(`tmp/br2watch/measure/census.json`, 2026-08-02) — **not mine, not touched.** Identical at close.

---

## 1 · ITEM 1 — THE BOOM · commits `4646dd2` + `9e6068d`

### 1.1 ⚑ THE RIG READ, PRINTED (GL-17 reference-governs)

The charter required the number be READ, not chosen, and that a material difference from the
expectation HALT rather than be absorbed. It is read from two files, neither of which this cell may
edit:

| source | line | value |
|---|---|---|
| `scripts/wr1_level_rig.gd` | **:28-29** | `ROOM_DIST := 34.0 * (WR1LevelS.ROOM_EDGE / 17.5)` |
| `scripts/wr1_level.gd` | **:87** | `const ROOM_EDGE := 37.5` |

```
34.0 × (37.5 / 17.5)  =  34.0 × 15/7  =  510/7  =  72.857142857142857 m
```

| | |
|---|---|
| **REALIZED WEREWOLF-SHOT DISTANCE** | **72.857142857142857 m** (exactly 510/7) |
| charter expectation | ≈ 72.857 m |
| **delta** | **+0.000142857 m — 0.14 millimetres** |
| verdict | **MATCH. Nothing to route up; no choice was made.** |

**Printed live by the scene that renders**, verbatim from the run log:

```
[cpb] ⚑ CANON CAMERA (R-CPB-16 lens + R-CPB-17 boom): yaw 47.0 / pitch -50.0 / fov 24.0,
FIXED BOOM 72.857142857 m (rig read 34.0 x (37.5 / 17.5) = 72.857142857,
pin delta 0.000000000000, MATCH); aim = station + 1.0 m; GL-13 rectangle 86.915 x 85.303 m
READ FOR REPORTING ONLY — no room dimension enters this pose (R-CPB-17)
```

### 1.2 THE CONSTANT IS A LITERAL, AND THAT IS THE ARGUMENT

`const CANON_BOOM_M := 72.857142857142857`, pinned in `kc2_cpb_clip.gd` with the R-CPB-17 citation
block above it. **A literal is the only form of this number that no room dimension can reach.** A
live `preload` of wr1's `ROOM_EDGE` would have been prettier and would have quietly re-introduced
exactly what the ruling struck: if wr1's room ever changes size, **this camera must not move.**

The cost of a literal is that it can be mistyped, so `_canon_pose` **recomputes the rig read from two
named provenance constants and compares** — `boom_pin_matches_rig_read: true`, delta `0.0` — and the
verdict travels to the sidecar and the claim ledger instead of living in a comment.

### 1.3 THE STRUCK LAW, AND WHERE IT STAYS

`DIST = 34.0 × (EDGE / 17.5)` is **struck from the presentation canon** per R-CPB-17(a) and left
**untouched in `wr1_level_rig.gd`**. That file is wr1's; the law is legitimate where it lives, as a
judge instrument for *"does this room fit the frame."* **This shot simply stops calling it.**

⚑ **ROOM-INVARIANCE IS EXPRESSED AS AN ABSENCE, AND THE ABSENCE IS AUDITABLE.** In `_canon_pose`,
`sx` and `sz` are read on the first two lines, recorded as the GL-13 scale reference, **and never
appear in a pose term again.** Every term is (station, angles, boom); the aim is the whirlwind
station + 1.0 m, so neither term reads a room. The promote tool's ledger checks this by recomputing
the eye with the footprint absent from the arithmetic — **room-invariance as a measurement, not a
claim.** (That row is written and, per § 2, never executed.)

⚑ **A2g's ONE DECLARED JUDGEMENT IS DISSOLVED, NOT RESOLVED.** `maxf` vs `minf` on a non-square
rectangle was worth 1.9 % of distance and was parked veto-open at A2g-2(3). With the boom fixed there
is no edge to choose: the judgement stops existing. **A2g-r carries zero camera judgements — every
term is a ruling or a read.**

### 1.4 ⚑ TWO WIRING DEFECTS FOUND BY READING THE WIRING, BOTH FIXED, NEITHER A PIXEL

**NOTE-80 — NOTE-76's HOLE WAS STILL OPEN ONE LEVEL DOWN.** NOTE-76 named the *concat* temp after the
cell. The **parts** it concatenates were still `$TMP/tmp-$SEG-$SHOT.mp4` in a shared directory —
and **A2g's two parts were sitting in exactly those names when this cell opened** (`tmp-A-stationary-
canon.mp4` 1.7 MB, `tmp-B-undulating-canon.mp4` 2.3 MB, both 2026-08-13 21:52–21:54). The harness did
not check `ffmpeg`'s exit status. **A quietly-failed encode would have appended the previous cell's
part to the concat, and the promote tool's `part_facts()` would have read its durations and frame
counts to build this clip's timeline — every gate green, the wrong parts.** Parts are now cell-scoped
and swept at open, the encoder's exit status is read, and the concat temp is removed before it is
rewritten. The claim ledger carries a freshness row.

**NOTE-81 — THE BOOM'S OWN PRINT WAS PRINTING ITS FORMAT STRING.** GDScript's `sprintf` has **no
`%e`**, and an unknown conversion does not raise — it hands back the format string. The pin-delta
fragment used `%.3e`, so the render log carried the literal `FIXED BOOM %.9f m (rig read %.1f x …`
**sitting between two neighbouring fragments of the same print that had substituted correctly.** A
half-substituted line does not look like a broken line. This was GL-17's *"print the read"*
requirement failing quietly. The sweep found a second `%e` in the mismatch `push_error` — the failure
path, where a format string instead of a number would have been worse. Both are `%.12f` now. **No
pixel, pose or sidecar value was ever wrong: `canon_derivation` carries floats, never formatted
strings. What was wrong was the human-readable evidence of them.**

### 1.5 EVERYTHING ELSE — VERIFIED AT HEAD, LISTED AS THE CHARTER ASKED

| article | value at HEAD | file:line |
|---|---|---|
| yaw / pitch / fov | **47.0 / −50.0 / 24.0** | `kc2_cpb_clip.gd:236-238` |
| aim convention | station + **1.0 m** | `kc2_cpb_clip.gd:241` |
| `CUT_PER_REV` | **17** | `kc2_player_channel.gd:276` |
| `CUT_DENSITY_TARGET` | **11.0** | `:283` |
| `WEAPON_SCALE` | **1.95** | `:125` |
| `GRIP_FRAC` / `GRIP_SEAT_M` | **0.20 / 0.10** | `:972` / `:981` |
| `CUT_PERSIST_REVS` | **0.45** | `:229` |
| `CUT_SEED` | **20260813** | `:230` |
| epoch bands | **5..13 / 0.10..0.40** | `:360-361` / `:394-395` |
| `player_rev_period_s` | **0.36** | `:150` |
| `PAL_*` ramp + knee | HEAD/MID/TAIL, **KNEE_AT 0.56, GAMMA 0.55** | `:464-468` |
| `FX_SEED` pinning | **20260813** + SMOKE 11 / TRAIL 23 / SPARK 37 | `:421-424` |
| `PREROLL_FRAMES` | **60**, tick-frozen | `kc2_cpb_clip.gd:70` |
| per-tick `seek_phase` | **present** | `kc2_motion.gd:299` → `kc2_body_anim.gd:182` |

Clip grammar unchanged: A stationary → 18-frame dip at the ENCODE → B undulating, ticks 1570–1700
both segments, 1:1 trace time, 1920×1080 @ 30 fps h264 yuv420p. **CLK-1 is untouched and not
regressed** — legs 2–5 of the matrix are the artifact-level proof.

---

## 2 · ITEM 3 — THE GATES. ⚑ FG-10 IS RED, AND THE MATRIX LOCALISES IT TO ONE CELL

### 2.1 THE FIVE-LEG MATRIX, FULL SPAN ON THE PROMOTED PAIRS PER CLK-1-2(4)

`PROBE_PASSES=4` · 4 × (320+320+46+46+46) = **3,112 rendered probe frames** across 20 launches.

| # | leg | span | states | disagreeing frames | digests |
|---|---|---|---|---|---|
| **1** | **canon / undulating** (t0 1570) | **FULL 320** | ⚑ **3** | ⚑ **ALL 320 (0…319)** | `14c83369…` · `981ba9dd…` · `f651b328…` · `f651b328…` |
| 2 | canon / **stationary** (t0 1570) | **FULL 320** | **1** | none | `95220575d1345ba3…` ×4 |
| 3 | canon / undulating, **t0 1660** | 46 | **1** | none | `982352531827455a…` ×4 |
| 4 | **d-close** / undulating *(demoted)* | 46 | **1** | none | ⚑ `0253761a43b374b9…` ×4 |
| 5 | **b-ring** / undulating *(demoted)* | 46 | **1** | none | ⚑ `504b6d8b4c0929ff…` ×4 |

Harness exit **12**. `FG-10 HALT — at least one leg of the matrix did not reproduce. Nothing
promoted.` No segment was rendered, no concat was made, **`/tmp/kc2_cpb/tmp-a2gr-lookdist-cadence-ab.
mp4` does not exist**, and the deliverable directory holds evidence text only.

### 2.2 ⚑ THE CONTROL LEGS ARE THE FINDING, AND THEY ARE A PROVEN NEGATIVE

Legs 4 and 5 render the **demoted diagnostics at poses this cell did not touch**. Their digests are
**CLK-1's** and **A2g's**, character for character — now reproduced in a **third cell at a third
commit**:

| digest | CLK-1 (`6eff089`) | A2g (`03436f8`) | **A2g-r (`9e6068d`)** |
|---|---|---|---|
| d-close / undulating | `0253761a43b374b9…` | `0253761a43b374b9…` | ⚑ **`0253761a43b374b9…`** |
| b-ring / undulating | `504b6d8b4c0929ff…` | `504b6d8b4c0929ff…` | ⚑ **`504b6d8b4c0929ff…`** |

Three conclusions, each carried by that arithmetic rather than by argument:

1. **THE HOST IS DETERMINISTIC.** Nine hundred and twenty probe frames reproduced bit-exactly in this
   session.
2. **THE BOOM MOVED NO PIXEL OUTSIDE `_canon_pose`.** Same proof A2g used, one cell later.
3. ⚑ **LOAD IS EXONERATED BY THE RUN'S OWN LEGS — AND I HAD REASON TO SUSPECT IT.** I ran light
   concurrent work (file edits, `py_compile`, greps) during leg 1's first two passes, and CLK-1's
   surface 1 names load as the one untested confound. But **leg 2 is a 320-frame full-span leg that
   came back bit-perfect four times under the same conditions**, and legs 3–5 likewise. **The
   confound I introduced is measured out by the run's own controls rather than argued away.**

### 2.3 WHAT IS ACTUALLY RED, STATED AS THE MATRIX STATES IT

The failing combination is **canon frame · undulating · window 1570**. Its neighbours each change one
term and go green:

* leg 2 changes the **cadence** (stationary, same window, same full span) → **1 state**
* leg 3 changes the **window** (1660, same cadence, same frame) → **1 state**

⚑ **AND THE SPAN LENGTH IS NOT THE DISCRIMINATOR, WHICH IS WORTH SAYING BECAUSE IT IS THE INTUITIVE
READ AND IT IS WRONG.** *Every* frame disagrees, **including frame 0** — so a 45-frame probe of
window 1570 would have caught this too. Leg 3 is green because it probes a **different window**, not
because it is short.

⚑ **THE FAILURE IS CONVERGING, NOT RANDOM.** Passes 1 and 2 are each unique; **passes 3 and 4 are
identical to each other.** Four passes, states A · B · C · C. That is the shape of a first-use cost
settling, not of a coin flip — and it is the same *family* of signature CLK-1 convicted (a one-time
renderer transient it named, GL-12, as *asynchronous shader-pipeline specialisation* **without
proving it**). A camera at a new position brings new geometry and material combinations into view.

⚑ **I AM NAMING THAT AND NOT CLAIMING IT (GL-12).** What is **measured** is § 2.2 and § 2.3: the
localisation, the convergence pattern, and the three exonerations. What is **not established** is the
mechanism, and establishing it is a diagnostic cell's job, not a render cell's. **A2gr-0 says HALT
after promote and bank the evidence if a gate goes red. I did not go looking for the mechanism, and I
did not re-run the gate to see whether it would come up green** — that is precisely the N=2 coin flip
A2e was promoted on (NOTE-67), and a clip promoted off a warm second run is a clip whose
reproducibility claim is false.

### 2.4 THE OTHER GATES, ALL RUN

**R-A1-1** — re-walked at HEAD with the new boom in the tree: **5,123 nodes, 0 text/canvas nodes.**
Motion smoke **71 checks, 0 FAIL.**

**FG-12** — **5 prune receipts, 6.74 G of probe intermediates reclaimed**, each with its regenerate
command, banked at `…/a2gr-fg12-prune-receipts.txt`.

**FG-9** — never entered. The temp name was cell-specific (`tmp-a2gr-lookdist-cadence-ab.mp4`,
verified ABSENT at open per NOTE-76's own discipline — checked, not assumed) and no bytes were ever
written to it.

---

## 3 · THE MEASURED BLOCK vs THE PRE-REGISTERED EXPECTATIONS

⚑ **THESE ARE REAL MEASUREMENTS AND THEY ARE NOT THE PROMOTED CLIP'S.** They come from a **3-frame
preflight render** taken before the matrix, through the same `unproject_position` instrument on the
same pose, at the same first tick (1570). The optics are a property of the **pose**, which is
deterministic — the camera gate, the derivation and the projection all ran identically on every one
of the 21 launches. **They are labelled as preflight rather than presented as a promoted artifact's
numbers, because no artifact was promoted.** Sidecar banked at
`…/evidence/a2gr-preflight-sidecar-shot-B-undulating-canon.json`.

| pre-registered (A2gr-0) | expected | **MEASURED** | verdict |
|---|---|---|---|
| subject screen height, tick 1570 | ≈ 12.96 % | **12.990 %** | ⚑ **HIT** |
| …in pixels of 1080 | ≈ 140.0 px | **140.30 px** | HIT |
| cut ring major axis | ≈ 153 px (vs A2g's 66) | **153.62 px** | HIT |
| **px/m across view at aim plane** | ≈ 34.9 | **34.8696** | ⚑ **HIT** |
| frame spans horizontally | ≈ 55 m | **55.062 m** | HIT |
| GL-13 corners outside frame | **4 of 4** | **4 of 4** | HIT — **reported as FACT** |
| ring ellipse minor/major | ≈ 0.7659 ± measurement | **0.765694** | HIT (−0.021 % vs A2g) |
| density, undulating mean | 11.371 (camera-independent) | **11.371** | HIT |
| density, stationary mean | 16.999 | **16.999** | HIT |
| thick/thin | 3.20 / 1.12 | **3.20 / 1.12** | HIT |

**Every pre-registered expectation lands. The subject is back in the Grim Dawn register.**

### 3.1 ⚑ ONE APPARENT MISS THAT WAS TWO QUANTITIES WEARING ONE NAME

The charter pre-registered **px/m ≈ 34.9**, derived as A2g's `15.0446 × 2.3177`. The subject block's
`px_per_metre_at_station` measured **22.18**, which looks like a 36 % miss. It is not a miss — the
sidecar carries **two different px-per-metre quantities**:

| quantity | A2g | × 2.3177 | **A2gr MEASURED** |
|---|---|---|---|
| **across-view** at the aim plane (a horizontal metre) | 15.0446 | 34.8694 | **34.8696** ⚑ the charter's number |
| **vertical** at the station (a metre of standing man) | 9.6268 | 22.3124 | **22.1805** |

Their ratio is **0.63610** against **cos(depression 49.956°) = 0.64338** — a vertical metre
foreshortens under a depressed camera, and the residual is the perspective the orthographic cosine
does not carry. **Both numbers are right, both were pre-registered by one name, and reporting either
alone would have been reporting a miss or a hit that was neither.** (NOTE-82; the NOTE-79 family —
ship the grammar of the quantity, not just its value.)

### 3.2 THE ELLIPSE — THE ROW BUILT TO PROVE THE ANGLE DID NOT MOVE

| | measured | predicted `sin(depression)` | error | depression |
|---|---|---|---|---|
| A2g @ 168.863 m | 0.765857 | 0.765830 | **+0.0035 %** | 49.9809° |
| **A2gr @ 72.857 m** | **0.765694** | 0.765548 | **+0.0191 %** | 49.9557° |
| d-close @ ~4.3 m | 0.530515 | 0.467890 | +13.38 % | — |

The measured ratio moves by **−0.021 %** while the boom moves by **−57 %**. ⚑ **That is the row
doing its job: the ellipse is a function of the ANGLE, so pulling the eye in along its own axis must
leave it alone — and it does.** The small residual is real and explained: the ring sits 1.0875 m up
and the aim at 1.000 m, so a **fixed** 0.0875 m offset subtends a larger angle at a shorter boom, and
the depression itself drops 0.025°. The prediction error grows 5.5× because perspective is 2.3×
nearer — **which is exactly why every reported figure is the measurement and the prediction rides
beside it.**

### 3.3 THE ANCESTRY — ONE DECLARED DELTA vs A2g

| | A2g | **A2g-r** | moved? |
|---|---|---|---|
| yaw / pitch / fov | 47 / −50 / 24 | 47 / −50 / 24 | — |
| aim (`look_at`) | (0, 1, 0) | (0, 1, 0) | — |
| **distance** | **168.863429 m** | ⚑ **72.857142857 m** | ⚑ **R-CPB-17** |
| eye | (79.384, 130.357, 74.026) | (34.251, 56.812, 31.939) | *consequence of the boom* |
| rate / clock / scale / grip / palette / epochs / seed / window / baton | — | — | — |

**Matt's ruling, verbatim, is the whole of the delta:**

> *"oh wow, the camera angle and zoom should have nothing to do with room size. nothing at all.. that
> is ludicrous."*

**Whose word moved what**, as the charter requires the manifest to say — the rate is **his lever**
(R-CPB-15), the clock is **the run's own fix** (CLK-1), the lens **angles are his canon** (R-CPB-16),
the boom is **his ruling** (R-CPB-17). That block is written into the promote tool and, per § 2, has
never been emitted.

### 3.4 ARTIFACTS

| file | what | class |
|---|---|---|
| `…/2026-08-13-sb1-a2gr-lookdist/a2gr-fg10-probe.txt` | the five-leg matrix, all digests | E, untracked |
| `…/a2gr-fg12-prune-receipts.txt` | 5 receipts, 6.74 G reclaimed, regenerate commands | E, untracked |
| `…/evidence/a2gr-harness-run.log` | the full harness run to the HALT | E, untracked |
| `…/evidence/a2gr-preflight-sidecar-…json` | the preflight sidecar behind § 3 | E, untracked |
| **`a2gr-lookdist-cadence-ab.mp4`** | ⚑ **DOES NOT EXIST** | — |
| **`MANIFEST.json`** | ⚑ **DOES NOT EXIST** | — |

---

## 4 · LAWS

**GL-6** — recomputed from bytes before anything was touched: `d7ecd866ac45…`, 1,065,632 B — **MATCH**
(§ 0); re-asserted by the arena's gate on all 21 launches.

**GL-12 — THREE ABSENCES DECLARED, NONE FILLED.** (i) The red leg's **mechanism is NOT established** —
the convergence signature is *consistent with* a first-use renderer cost, and I have named that
without proving it (§ 2.3). (ii) Inherited unclosed: the particle phase is still process-clocked, no
seek API. (iii) The promote tool's new ledger rows are **written and unexercised**, and the manifest
they would have produced **does not exist rather than existing with unverified numbers**.

**GL-13** — the pinned rectangle was **READ and never moved**: 86.915 × 85.303 m. ⚑ **And at A2g-r it
is no longer an input to anything** — R-CPB-17 struck the derivation that consumed it, so it is read
purely to be reported.

**GL-15** — one ongoing-damage read, unchanged: bed + haze, the 24-node cut pool, 3 burst emitters,
one wire bit. Smoke row PASS.

**GL-17 / ADR-006** — **no acquisitions of any kind.** The wr1 rig and level were **READ and CITED**,
never copied and never edited; the struck law stands untouched in wr1's own file. § 1.1 is the read,
printed.

**GL-18** — one clock, CLK-1's, **untouched and verified at HEAD**: `PREROLL_FRAMES 60`, per-tick
`seek_phase`, tick from the frame index. ⚑ **The artifact-level determinism claim is WITHDRAWN for
the canon/undulating/1570 frame** and stands, by measurement, for the other four legs.

**R-A1-1** — re-walked at HEAD: **5,123 nodes, 0 text/canvas nodes.** The dip is an encode filter and
no encode ran.

**D-14** — everything ran **classic**, off the factory spine. The only spine code in this cell is the
two post-hoc artifact gates inside the promote tool, and **the promote tool refused at its first
check.**

**PL-5** — floor-checked before frames in two places (**6.751 G of 10 G**, disk 24.3 G) and at close
(**6.751 G**, delta < 1 MB).

**FG-9** — **never entered**; the cell-named temp was verified absent at open and no bytes were
written to it. **FG-10** — five legs, promoted pairs at full span, **RED on one, HALT honoured.**
**FG-12** — 5 receipts, 6.74 G reclaimed.

**CL-2 / PL-7** — three commits, one per item (item 1 carries a declared follow-on for NOTE-81 as a
**new commit, never an amend**); the two godot commits pushed as they landed. ⚑ **One CL-2 note,
declared:** item 1 spans two files — `kc2_cpb_clip.gd` (the boom) and `run_kc2_cpb_clip.sh` (the cell
name and NOTE-80) — because a cell rename that is not atomic with the change it renames for is itself
the hazard NOTE-76 describes. CL-2 is commit-per-ITEM and this is one item.

**Containment** — godot **229 untracked at open and 229 at close**; `tmp/br2watch/measure/census.json`
**not mine and not touched**. ⚑ **No temporary working-tree operations were performed** — nothing to
declare under NOTE-69.

---

## 5 · SELF-ATTACK SURFACES (ranked, veto-open)

1. ⚑ **THE BINDING FRAME IS STILL NOT RENDERED, AND THAT IS THE COST OF THIS CELL.** R-CPB-17(d)
   routes density feel, palette knee, cadence read and the CLK-1 FX-draw question to A2g-r. **They
   are all still open.** The boom is proven and the frame it produces is measured, but Matt has
   nothing new to watch. I judged that a clip whose 320 frames are three different clips cannot
   carry a binding ratification — but the run wanted a watch and did not get one, and that is a real
   cost, not a technicality.
2. ⚑ **THE MECHANISM IS UNDIAGNOSED AND I STOPPED ON PURPOSE.** I have the localisation (§ 2.3) and
   a convergence pattern, and I did not spend a bisect on it. A diagnostic cell would want: the same
   leg at 45 frames on window **1570** (separating window from span for certain), a run with a
   **cleared shader cache** versus a warm one, and a pixel-signature read like CLK-1's ±1-channel
   histogram. **That is a CLK-2 charter and it is the conductor's to write.** My defence for stopping
   is the charter's own words; my attack on myself is that I was one cheap leg away from splitting
   the last ambiguity and I did not take it.
3. ⚑ **I RAN CONCURRENT WORK DURING LEG 1's FIRST TWO PASSES.** File edits and `py_compile` — light,
   but CLK-1's surface 1 names load as the one untested confound and I walked into it. **The run's
   own controls measure it out** (leg 2 is 320 frames, four bit-perfect passes, same conditions), so
   the conclusion survives. It survives by luck of experimental design rather than by my discipline,
   and a cleaner cell would have rendered on an idle machine.
4. ⚑ **§ 3's OPTICS COME FROM A PREFLIGHT, NOT FROM PROMOTED FRAMES.** The pose is deterministic and
   the instrument is the same one, and I labelled it rather than quietly presenting preflight numbers
   as an artifact's. But **a measurement taken from a render nobody promoted is weaker evidence than
   one taken from the bytes Matt watches**, and the subject figure in particular (12.990 %) will want
   re-measuring on the promoted clip when there is one.
5. **THE PROMOTE TOOL'S NEW ROWS HAVE NEVER EXECUTED.** Four new ledger rows about the boom, the
   room-invariance recomputation, the corner fact, the vs-A2g field-for-field proof and NOTE-80's
   freshness check are **written and unrun**. This is A2f's surface 8 returning in a smaller shape.
   The only thing proven is that the file imports and refuses correctly.
6. **I COMMITTED A TOOL FOR A PROMOTE THAT DID NOT HAPPEN.** My reason is coherence — the harness's
   `PARTS_DIR` is committed in godot, and leaving the reader uncommitted would put the two repos in
   disagreement at HEAD about where a part lives. It is still a commit of unexercised code.
7. ⚑ **NOTE-80 IS A DEFECT I FOUND IN MY OWN PREDECESSOR'S FIX, AND I ONLY FOUND IT BECAUSE I WENT
   LOOKING.** A2g closed the shared-concat hole and declared the class dead. It was not dead; it was
   one level down, and A2g's own parts were the loaded gun. **A fix that names a class should be
   checked against the whole class, and NOTE-76 was written as though naming the instance had killed
   it.**
8. **NOTE-81 MEANS MY GL-17 EVIDENCE WAS BRIEFLY A FORMAT STRING.** The required print was emitting
   placeholders, between two fragments that worked. Caught by reading the output; it would not have
   been caught by any gate in the stack, because no gate reads the render log.
9. **THE RED LEG'S THREE STATES WERE NOT KEPT AS PIXELS.** FG-12 pruned the probe frames, as it
   always does, so the difference between states A, B and C exists now only as three digests. A
   diagnostic cell will have to re-render to see it. **Cheap to say now, expensive to have wanted
   later** — a gate that fails could reasonably keep one frame from each distinct state.
10. **THE BOOM IS PROVEN AGAINST THE RIG AND NOT AGAINST MATT'S EYE.** 72.857142857 m is the rig's
    realized number to 0.14 mm and the subject lands at 12.99 %, which is the register R-CPB-17
    names. Whether *this* frame reads like Grim Dawn in motion is still an eye-call nobody has made.
11. **ONE-MACHINE DETERMINISM, INHERITED.** Legs 2–5 prove this host reproduces. Nothing here says
    another host would.
12. **Twenty unlicensed editor addons still stand in the tree; the helmet is still a tepid "ok."**
    Both untouched.

---

## NOTES (continuing from NOTE-79)

**NOTE-80 — A FIX THAT NAMES A CLASS MUST BE CHECKED AGAINST THE WHOLE CLASS, BECAUSE THE INSTANCE
YOU FIXED IS THE ONE YOU WERE LOOKING AT.** NOTE-76 killed the shared *concat* temp and said the
whole class of failure disappears. It did not: the *parts* were still shared, the encoder's exit
status was unread, and the previous cell's parts were sitting in exactly the names the next cell
would write. **The second instance was harder to see precisely because the first had been fixed and
declared closed.** When you name a class of defect, enumerate its members before you write the
sentence that says the class is dead.

**NOTE-81 — AN UNSUPPORTED FORMAT CONVERSION DOES NOT RAISE, IT RETURNS THE FORMAT STRING — AND A
HALF-SUBSTITUTED LINE DOES NOT LOOK BROKEN.** GDScript's `sprintf` has no `%e`. The fragment using it
printed its own placeholders **between two fragments of the same `print` that had substituted
correctly**, so the line read as prose with a technical-looking middle. This is NOTE-79's family
seen from the writing side rather than the parsing side: **the alphabet of a format string is not the
grammar of the language that consumes it.** And the deeper habit: **no gate in this stack reads the
render log, so evidence that lives only in a print is evidence only if a human looks at it.** I
looked because I was checking a number, not because anything made me.

**NOTE-82 — TWO QUANTITIES WEARING ONE NAME WILL PRODUCE A MISS OR A HIT AND BOTH WILL BE WRONG.**
A2gr-0 pre-registered "px/m ≈ 34.9". The sidecar carries `px_per_metre_across_view_at_aim` (34.87 —
the pre-registered one) and `px_per_metre_at_station` (22.18 — a *vertical* metre, foreshortened by
`cos(depression)`). Reading the second against the expectation gives a 36 % miss; reading the first
gives a hit to four decimals. **A pre-registration is only falsifiable if it names the quantity
precisely enough that only one measurement can answer it** — and when it does not, the honest move is
to report both with their geometry, not to pick the one that scores better.

**NOTE-83 — A CONTROL LEG THAT REPRODUCES A DIGEST FROM ANOTHER CELL IS THE CHEAPEST PROOF OF
INNOCENCE THERE IS, AND IT IS ONLY AVAILABLE IF SOMEBODY LEFT IT IN THE MATRIX.** R-CPB-16(d) demoted
b-ring and d-close to diagnostics; A2g kept them in the FG-10 matrix as regression legs, at
45 frames, and A2g's own surface 5 filed that as a declared trade — *"a regression in a diagnostic's
frame 200 would pass."* **Those two legs are what turned a red gate from a crisis into a
localisation.** They exonerated the host, the load and every line of this cell's change in one table,
because their digests had been on record since CLK-1. **Keep the legs whose value is that they never
change.**

---

*Landed by drax, presentation seam, 2026-08-13. The boom is Matt's ruling, read from the rig to
0.14 mm, and the man is back at 13 % of frame height. The gate went red on one leg of five and the
clip was not promoted. HALTED on the red gate — evidence banked, mechanism routed up.*
