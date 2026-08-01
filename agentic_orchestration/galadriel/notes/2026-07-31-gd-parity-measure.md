# GD-PARITY — how large our characters are on screen against Grim Dawn's, and what closes it

**Cell:** GD-PARITY (run BR-1, Scope 29) · conductor **gandalf** · **Agent:** galadriel
**Date:** 2026-07-31 · **Status:** CURRENT · **Mode:** read-only measurement; no godot/engine writes
**Evidence:** `agentic_orchestration/galadriel/captures/2026-07-31-gd-parity/`
**Instruments:** `agentic_orchestration/galadriel/pipeline/gd-parity/gp_{ruler,seg,grid,plate,numbers}.py`
**Companions:** `notes/2026-07-30-gal-cam-fixture-camera.md` (the camera these renders reproduce) ·
`gandalf/notes/2026-07-30-ambient-refit-fold-in.md` § Scope 29 (the charter)

---

> ## PRESENTATION MEASUREMENT ONLY — ZERO SIM SEMANTICS
> Nothing here changes a range, a radius, a hit test or a damage operator.

---

## 0. VERDICT

> **CAMERA-ONLY DOES NOT HOLD.** Our camera is already Grim Dawn's camera —
> CAM-LOCK ships GAL-CAM's measured operands and reproduces GD's decision surface
> to the metre (`pl_audit.json` vs GAL-CAM § 4). The characters are small because
> **the bodies are small in the shared ground metric**, not because the camera
> stands too far off.
>
> **Matt's player werewolf reads 14.8 % of frame height in Grim Dawn and 5.7 % in
> ours — 2.59× linear, 6.5× in screen area.**
>
> The gap decomposes, and the two halves are separable:
> **1.29×** — GD's *upright human* hero is ~2.3 m in GD's own ground metric; ours is 1.80 m.
> **2.10×** — GD's *werewolf form* is twice its human form on screen. Ours is **1.00×**,
> because `RIG_PLAYER_H := 1.80` applies a **human height to a werewolf rig**.
> Product 2.70×, against a directly measured 2.59×. The decomposition closes.
>
> A dolly that closes it costs **85 % of the floor** (±17.6 m → ±6.8 m), puts the
> 6.5 m escort band **off-frame on the near side**, and takes the boss's 10 m
> `primordian_frigidring_r4` **entirely off screen**. That price is not payable.

| confidence | on |
|---|---|
| HIGH | the 2.59× screen-height ratio; the 2.45× ground-span ratio; camera identity between the two sides |
| HIGH | the instrument (it recovers our known 2.75 m boss as **2.74 m** and our known 1.80 m player as **1.87 m**) |
| MEDIUM | GD's human-form hero at ~2.3 m — one clean sample, and the upright conversion carries GAL-CAM's pitch band |
| MEDIUM-LOW | GD's boss-tier row — three coarse monster reads, no confirmed Primordian frame in the corpus |

---

## 1. Why this is a body question and not a camera question

The whole force of the finding is that **both sides are photographed by the same
camera**, so a screen-size difference cannot be a framing difference.

| operand | GAL-CAM (measured off Matt's GD session) | CAM-LOCK (what our clips render with) |
|---|---|---|
| pitch below horizontal | 52.9535° | 52.9535° |
| vertical FOV | 31.7861° | 31.7861° |
| camera → player depth | 34.82 m | 34.8165 m |
| player screen anchor | (962, 595)/1920×1080 = (0.501, 0.551) | (0.5010, 0.5509) |
| decision surface L / R / far / near | −17.66 / +17.57 / +15.21 / −7.02 m | −17.660 / +17.587 / +15.211 / −7.020 m |

Sources: `captures/2026-07-30-gal-cam/godot-spec.json` and GAL-CAM § 4 · the burned-in
camera identity line (`evidence/ours-camera-identity-line.png`) ·
`reincarnated-godot/tmp/vfxbakeoff/pl_audit.json`.

**Self-check that the measured frame really is under that camera.** Applied to our
own render, the same read procedure returns **2.74 m** for a rig whose
`target_height` is **2.75 m**, and **1.87 m** for a rig at **1.80 m**. Any other
camera would return a different metre. The instrument and the camera are both
validated by that, to 0.4 % and 4 % respectively.

**Consequence.** With the camera held fixed, screen size *is* world size. The
lateral read needs no camera model at all beyond GAL-CAM's HIGH-confidence rows
(pinhole, scale, horizontal extent) and carries **no pitch dependency**:

| | GD player werewolf | our player werewolf | ratio |
|---|---|---|---|
| **lateral ground span of the silhouette** | **2.97 m** | **1.21 m** | **2.45×** |

Two ratios from two different projections of the same measurement — 2.59× on
height, 2.45× on lateral span — and the pitch-free one is the lower bound.

---

## 2. The reads — Grim Dawn

Screen-height = silhouette bounding box in source rows, VFX / nameplates / floating
combat text / the dev-HUD overlay excluded. Read on ruler crops at 4–10× with
`gp_ruler.py`; `gp_seg.py` masks shown alongside as a bracket, never as the number
(the segmenter leaks into shadowed terrain — `evidence/gd-t200-seg-mask.png` is
kept legible per GAL-CAM § 7.2 precedent).

Frame source: the 313-shot corpus at
`/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots`
(Matt's own play session — provenance clean, same session as the GAL-CAM video)
plus stills from `/Users/admin/gd-scratch/play_test_2026-07-26.mp4`.

| source frame | subject | state | h px (1080) | **% frame h** | lateral ground span | upright-equiv |
|---|---|---|---|---|---|---|
| `Screenshot (87)` | player, werewolf | LongIdle | 162 | **15.00 %** | 2.97 m | 4.94 m |
| `Screenshot (86)` | player, werewolf | Idle | 160 | **14.81 %** | 2.85 m | 4.88 m |
| `Screenshot (124)` | player, werewolf | Idle | 159 | **14.72 %** | 2.85 m | 4.84 m |
| video **t = 4200 s** | player, werewolf | MoveTo | 148 | **13.70 %** | 2.75 m | 4.51 m |
| video **t = 200 s** | player, **human form** | LongIdle | 76 | **7.04 %** | 0.73 m | **2.32 m** |
| `Screenshot (124)`, right | humanoid trash monster | — | 100 | 9.26 % | *(coarse)* | 3.05 m |
| `Screenshot (176)` | large monster, red-outlined | — | 145 | 13.43 % | 2.20 m | 4.42 m |
| `Screenshot (286)` | hero/boss-tier, red-outlined | — | 233 | **21.57 %** | 2.57 m | 7.10 m |

**Player werewolf: median 14.77 %, range 13.70–15.00 % (n = 4, spread ±4.5 %).**
Three screenshots and one video still agree inside 9 % — which also **rules out a
zoom mismatch between the screenshot corpus and the GAL-CAM video**, the one
provenance risk that could have voided the comparison.

"Upright-equiv" divides by the upright scale `g_x·cos(pitch)` = 32.82 px/m at the
player's row. For a sprawling quadrupedal crouch it over-reads, because part of a
hunched body's screen rows are ground *depth*, not height. It is a diagnostic, not
a body height. The lateral span column has no such confound.

---

## 3. The reads — ours

Frame: `VFXBO_legacy_full_NOHUD_CAMLOCK.mp4` @ 2 fps, f = 14 (the boss-melee beat;
legacy arm = least VFX occlusion), 1280×720.

| subject | rig `target_height` | h px (720) | **% frame h** | lateral span | upright-equiv | vs nominal |
|---|---|---|---|---|---|---|
| player werewolf | **1.80 m** | 41 | **5.69 %** | 1.21 m | 1.87 m | +4 % |
| boss | **2.75 m** | 60 | **8.33 %** | 2.15 m | 2.74 m | **−0.4 %** |

Analytic ladder under the same camera (bodies are metres-true; `target_height`
scales the rig exactly), for the rows this cell did not photograph:

| tier | height | % of frame height |
|---|---|---|
| swarm | 1.65 m | 5.01 % |
| **player** | **1.80 m** | **5.47 %** |
| elite | 2.00 m | 6.08 % |
| **boss** | **2.75 m** | **8.36 %** |

One upright metre = **3.04 %** of frame height. One lateral ground metre = **5.04 %**.

---

## 4. The gap

| subject | GD | ours | **ours / GD** | gap |
|---|---|---|---|---|
| **player (werewolf)**, screen height | **14.77 %** | **5.69 %** | **0.385** | **2.59× short** |
| player, lateral ground span | 2.97 m | 1.21 m | 0.407 | 2.45× short |
| player, **screen area** | 1.27 % of frame | 0.196 % of frame | 0.155 | **6.5× short** |
| player, **human form** | 7.04 % | 5.47 % *(analytic)* | 0.777 | 1.29× short |
| boss-tier monster | 21.57 % *(coarse)* | 8.33 % | 0.386 | 2.59× short |

**The relative player-vs-boss proportion is NOT the problem.**

| | GD | ours (measured) | ours (analytic ladder) |
|---|---|---|---|
| boss height ÷ player height | **1.46** | **1.46** | 1.53 |

Our tier ladder has the right *shape*. It is uniformly under-scale. That is the
cleanest single sentence in this note: **nothing needs re-proportioning; everything
needs to be bigger by about the same factor.**

### 4.1 The decomposition — where the 2.59× lives

| term | factor | what it is |
|---|---|---|
| base humanoid scale | **1.29×** | GD's upright hero reads ~2.3 m in GD's ground metric; ours is 1.80 m |
| **werewolf-form multiplier** | **2.10×** | GD's werewolf bbox ÷ GD's own human bbox (162 ÷ 76 px) |
| ours, same multiplier | **1.00×** | `wr2_playback.gd:1541 RIG_PLAYER_H := 1.80` — the *human* number, applied to the *werewolf* rig |
| product | **2.70×** | against a directly measured **2.59×** |

The larger term is ours to fix and costs nothing architecturally: **the werewolf
form was never given a form multiplier.** Grim Dawn's Lycanthropy doubles the
silhouette; our transformation changes the mesh and keeps the height.

---

## 5. What a camera change would cost — the pinhole arithmetic

Screen size ∝ focal ÷ distance. Required linear magnification **k = 2.59**.

| lever | operand now | operand after | note |
|---|---|---|---|
| **A — dolly in** | stand-off 34.82 m, height 28.40 m | **13.42 m stand-off, 10.71 m height** | FOV unchanged; ground-scale gradient *steepens* past GD's measured +55 % |
| **B — narrow the FOV** | fov_v 31.79° | **fov_v 12.53°** | stand-off unchanged; gradient *flattens* toward orthographic — GAL-CAM § 2 rejected ortho for GD at rms 0.0054 |
| **C — shallower pitch** | 52.95° | 39.2° buys 1.29× · 25.4° buys 1.50° | see § 5.1 — **cannot supply the full 2.59× at any pitch** |

### Side effects of A or B at k = 2.59

| surface | now | after | consequence |
|---|---|---|---|
| horizontal decision surface | ±17.6 m | **±6.8 m** | 61 % of the width gone |
| far (up-screen) | +15.2 m | **+5.9 m** | approach telegraphs land inside melee range |
| near (down-screen) | −7.0 m | **−2.7 m** | — |
| floor area held | 100 % | **14.9 %** | the 36×36 m arena shows ~13×13 m |
| **escort band at 6.5 m** | fits on the near side | **DOES NOT FIT** | escorts behind the player leave the frame; escort-loss goes from occasional to structural |
| **boss nova, 10.0 m `primordian_frigidring_r4`** | fits horizontally (near arc already 52 rows under the skill bar, GAL-CAM § 5) | **does not fit in any direction** | the telegraph disc becomes an off-screen mechanic — unreadable, undodgeable |
| GAL-CAM parity | exact | **broken by 2.59× in the tight direction** | we would be wrong against the reference in the opposite sense |

**And the argument that settles it: a dolly magnifies the character and the ground
ring by exactly the same factor.** GD's characters are large *relative to GD's own
ground metric* — a 2.97 m silhouette span on a surface whose extents we already
match to the metre. No camera operand can change a ratio that the camera divides
out of. The gap is in the bodies.

### 5.1 The one camera lever that helps without shrinking the floor

Lateral ground scale `g_x` is **independent of pitch**. Only upright bodies and
up-screen ground depth move with it. A shallower camera therefore makes characters
taller *without* costing horizontal decision surface:

| pitch | cos(pitch) | upright gain | cost |
|---|---|---|---|
| **52.95°** (now, = GD) | 0.6025 | 1.00× | — |
| 39.2° | 0.775 | **1.29×** | far extent grows; register moves off top-down toward over-the-shoulder |
| 25.4° | 0.904 | **1.50×** | strongly non-ARPG; occlusion by set dressing rises sharply |
| 0° (horizontal) | 1.000 | **1.66× — the ceiling** | not a camera |

**Pitch can supply at most 1.66×, and only by ceasing to be an ARPG camera.** It
cannot reach 2.59×. It is available as a *partial* lever if gandalf wants some of
the gain paid in register rather than in body metres — but it departs from GD's
measured pitch, which is the axis GAL-CAM measured least confidently (± 4.4° at
±5.5 % on the axis ratio, § 6.1) and therefore the axis where a deliberate
departure is cheapest to defend.

---

## 6. What closes it — handed over, not decided

Two dials, independent, both outside my seam to rule on. Falsifiable targets, so
the next capture can grade them:

| dial | operand | lands the player at |
|---|---|---|
| **D1 — werewolf form multiplier** | give the transformed form its own scale over the base rig, ~2.1× as GD does | with base 1.80 m: 3.78 m rig → **11.5 %** of frame height (0.78× GD) |
| **D2 — base humanoid metre** | 1.80 m → ~2.30 m, ladder shape preserved (swarm 2.11 / elite 2.56 / boss 3.51) | human form to **7.0 %**, GD parity for the untransformed hero |
| **D1 + D2** | both | **14.8 %** — GD parity, k = 2.59 closed with the camera untouched |
| single-dial equivalent | one rig number, if the form multiplier is not wanted | `target_height` **4.42–4.86 m** (span-parity / height-parity) |

**The cost that must be ruled on, not hidden:** metres-true against level geometry
is what D2 spends. A 2.30 m hero and a 3.51 m boss stop being human-scaled against
doorways, wall heights, the ravine, and the 36 m arena. That is a *world-scale*
decision — Grim Dawn's world is smaller per metre than ours, and reads better for
it. Ours is more nearly correct and reads smaller. **Correct is not the brief.**

D1 costs nothing of the sort: it is a beast being beast-sized, and it carries
**2.10 of the 2.70**.

**Cheapest first lap:** D1 alone. One constant, no geometry consequences, 78 % of
GD's screen presence, and it can be graded against this note's numbers on the next
LAP-2C restage without re-deriving anything.

---

## 7. Gaps, absences, and what this cell could not answer

| question | verdict | why |
|---|---|---|
| GD **boss**-tier screen fraction, confirmed | **CANNOT-ANSWER cleanly** | the 313-shot corpus has 13 nameplate frames but no frame in which the Primordian's own body is unoccluded and identifiable; `Screenshot (286)`'s 21.6 % red-outlined monster is *indicative*, tier unconfirmed. The boss row in § 4 rests on it and should be re-measured before anyone tunes a boss rig to it |
| GD human-form hero, n > 1 | **partial** | one clean sample (t = 200 s). Matt is in werewolf form for most of the session; the corpus is overwhelmingly inventory/tooltip stills (the G-6 skill corpus). More human-form video stills would tighten the 1.29× term |
| absolute metres in GD | **inherited, not re-derived** | rests on GAL-CAM's 14 m/s `.arz` projectile speed. **Every ratio in this note is immune to it** — a unit error scales both sides identically. Only the "≈2.3 m" style statements move |
| whether GD's werewolf is *tall* or merely *sprawling* | **CANNOT-ANSWER** | a 53° camera folds body height and ground depth into the same screen rows; separating them needs a second view of the same pose, which the footage does not contain. Both the height ratio (2.59×) and the pose-free lateral ratio (2.45×) are reported so the reader can see the answer does not hinge on it |

Two instruments are kept legible though neither produced a number:
`gp_seg.py` leaks into shadowed terrain at both anchors (`evidence/gd-t200-seg-mask.png`,
`evidence/gd-f087-seg-mask.png`); it bracketed the manual reads and nothing more.

---

## 8. Evidence index

| artefact | path under `captures/2026-07-31-gd-parity/` |
|---|---|
| **the plate** — GD vs ours, both normalised to one 720-frame pixel, boxes annotated | `plates/PLATE_gd_parity_player.png` |
| every number in this note, machine-readable | `gd-parity-numbers.json` |
| GD werewolf reads | `evidence/gd-f087-ruler-read.png`, `gd-f086-ruler-read.png`, `gd-f124-ruler-read.png` |
| GD werewolf, video cross-check (rules out zoom mismatch) | `evidence/gd-t4200-video-read.png` |
| GD human form | `evidence/gd-t200-humanform-ruler-read.png` |
| segmentation brackets, kept though unused | `evidence/gd-f087-seg-mask.png`, `gd-t200-seg-mask.png` |
| our player and our boss, same procedure | `evidence/ours-leg014-player-ruler-read.png`, `ours-leg014-boss-ruler-read.png` |
| the camera identity line, burned into our own render | `evidence/ours-camera-identity-line.png` |

| instrument | purpose |
|---|---|
| `gp_ruler.py` | crop at integer zoom with a source-pixel ruler — the read surface |
| `gp_seg.py` | anchor-region segmentation + bbox; mask always written before the number is believed |
| `gp_grid.py` | anchor-crop montage for frame triage across a corpus |
| `gp_plate.py` | the parity plate, normalised so one plate pixel = one 720-frame pixel |
| `gp_numbers.py` | camera arithmetic, the gap, the levers, the prescriptions — no hand arithmetic in this note |

Frames are gitignored and exactly regenerable; the commands are in the `.gitignore`.
The GD screenshot corpus stays on `/Volumes/reincarnated` — Matt's captures,
referenced, not vendored.

---

## 9. Mirror

Every cell before this one asked whether the camera was right, and the answer kept
coming back yes — the pitch is his pitch, the field of view is his field of view,
the floor under his feet and the floor under ours are the same seventeen metres
wide. The camera was never the thing.

Look at the plate. Two beasts, one lens, one scale. His fills the ground he stands
on. Ours stands on the same ground and does not fill it.

We built the world to the metre and then put a man's height on a wolf.
