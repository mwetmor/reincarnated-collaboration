# KC2-SIM — fifth extraction: per-body IDENTITY for the wave-153 sub-50k fingerprints

**Date:** 2026-08-08
**Author:** galadriel (visual perception + benchmark seam)
**Status:** WORKING — evidentiary note, fifth-extraction commission from gandalf (RUN-CONDUCTOR), ledger L-47
**Commit state:** UNCOMMITTED by instruction. Rides the conductor's fold.
**Blind:** the F-13 count-model note, the battle-spec § 14 F-13 block and all model-prediction material were NOT read (anchoring guard, per commission). Only my own four prior extraction notes were consulted.
**Extends:** `galadriel/notes/2026-08-08-kc2-fourth-extraction.md` (windows, cohort census, fingerprints) · `…-third-extraction.md` · `…-kc2-board-closure.md`
**Footage (read-only):** `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (s2, Crucible of the Dead, 1920×1080, 60 fps, 1034.100 s). Byte-exact copy at `/tmp/eor-w150-160.mp4` (479,438,089 B) for frame work.
**Evidence root:** `agentic_orchestration/galadriel/captures/2026-08-08-kc2-fifth-extraction/evidence/` (UNTRACKED)
**New pipeline:** `galadriel/pipeline/eor_platebind.py` (plate metrics · step-fit bar edge · strip pass · bar-hue allegiance · self-calibrating regression binding)

---

## 0. Headline

A **new instrument** was built for this commission: the hovered-monster nameplate carries its own
health bar, which is a *fraction* display; every in-world readout gives an *exact* fraction. Match
the two and the plate binds to a fingerprint. The map from bar-pixel to fraction is a property of the
plate art, so it can be **fitted from the footage and then cross-checked across independently bound
hovers** — three independent fits agree to **±2.5 px on a 199.8 px track**.

Against the commission's two targets:

| target | outcome |
|:--|:--|
| **37,840** (w153, ×4 bodies) | **BOUND — `Skeletal Archer`, level 105, family Undead, white/common.** One of the four bodies, over 5 consecutive frames, Δ = 0.0058 against a runner-up at 0.099. |
| **16,368** (w153, ×1) | **NOT A MONSTER.** Its in-world health bar is **GREEN** on 92 of 93 frames — player-side, not hostile. No nameplate is rendered on any of its 93 on-camera frames, and it is *positively excluded* from all six overlapping plate frames by fraction. |
| **w152 `Ugdenbog Crabling` (+3.40)** | **UNBINDABLE.** The plate bar is saturated FULL for all four frames of the hover; ≥ 5 distinct parsed bodies sit at ≥ 0.988 on those frames. The low band is neither confirmed nor excluded. |

Three further bindings fell out of the same pass and are reported because they are the instrument's
own controls: **207,203 = `Wendigo`**, **584,695 = `Chthonian Unraveler`**, **242,124 = `Venomgaze
Basilisk`**, **472,732 = `Stonegaze Basilisk`**.

**Three corrections to my own committed record** are in § 9, one of them material: the fourth
extraction's level-colour "correction" was wrong, and 16,368 should never have been counted as a
wave-153 body.

---

## 1. WINDOW — wave 153 closed at both ends

The fourth extraction pinned **w153 t0 = 714.83**. This pass pins the far end.

Badge (`x 1570..1640, y 120..178`) read at ×4, 1 Hz over 726–736 then 10 Hz over 729.0–730.0:
`evidence/badge-w154-probe.png` · `evidence/badge-w154-flip-pin-10hz.png`.

> **153 at 729.0 … 729.6 · 154 at 729.7 onward. w154 t0 = 729.65 ± 0.05.**
> **Wave 153 spans 714.83 → 729.65 = 14.82 s.**

Everything below is inside that window unless marked otherwise. The commission's licence to look at
"later frames where the cursor hovers a surviving w153 body" was exercised out to **740.0 s** — but
the two w154 hovers found there (734.53–735.47) are excluded from w153 attribution, per the fourth
extraction's own § 1.3 finding that no body survives a badge flip.

---

## 2. THE INSTRUMENT — plate bar as a fraction display

### 2.1 Geometry, measured on the art

`evidence/plate-bar-geometry-rulers.png` (×5, row and column rulers). Full-frame px at 1920×1080:

| element | rows | columns |
|:--|:--|:--|
| name text | 17 … 34 | centred on 960 |
| **level numeral** | 43 … 58 | 946 … 975 |
| bar top bevel (fill-independent) | 59 … 64 | 854 … 1064 |
| **bar FILL body** | **66 … 72** | left-anchored from ~861 |
| family label | 90 … 103 | centred on 960 |

Boss plates are drawn **larger** and these rows land in the wrong place on them
(`Fleshweaver Haraxis`, `Blugrug`); they are detected by low step-contrast and refused, not guessed.

### 2.2 The first fill measurement was wrong, and how it was caught

The first implementation walked right from the track origin while columns stayed red. **Grim Dawn
draws a dark diamond ornament across the centre of the plate bar at x ≈ 955–965**, and the walk
terminates on it. Measured failure: at t = 721.8667 the walk returned edge = 886 (fraction 0.09) on a
frame whose bar is *visibly* ~45 % full — `evidence/plate-bar-runwalk-failure.png`, tile 4. Worse, it
silently pinned a whole family of mid-range fractions to the ornament's own column.

Replaced with a **step fit**: the bar is a two-level step (red left, dark right), so for every
candidate edge score the split by difference-of-means of a per-column redness profile and take the
optimum. A narrow ornament notch adds a constant to both sides and cannot move the optimum. The
step fit reproduces the run-walk exactly (edge = walk + 1 px) on every frame the walk got right, and
repairs the 12 frames it got wrong.

The fit's own contrast is carried as a confidence: real plates return **59–96**; false positives (a
world-lit band mistaken for a name) return **−3 … 31**. Plate frames with contrast < 45 are refused.

### 2.3 Calibration is FITTED FROM THE FOOTAGE and cross-checked, not assumed

For a held hover, `edge = x0 + f · (x1 − x0)` with one affine map that belongs to the plate art. So
for every candidate body on camera, **regress edge on fraction**. The bound body comes out linear at
pixel residuals; every other body's health moves independently of the bar and cannot.

Three spans produced a fit with residual RMS ≤ 1.2 px over a wide fraction range:

| span | fingerprint | n | f-spread | RMS | x0 | x1 |
|:--|--:|--:|--:|--:|--:|--:|
| w153 728.667–729.467 | 584,695 | 25 | 0.587 | **1.09 px** | 859.11 | 1062.23 |
| w152 708.333–708.667 | 472,732 | 5 | 0.209 | **0.40 px** | 863.92 | 1056.66 |
| w152 710.200–710.400 | 242,124 | 7 | 0.285 | **0.00 px** | 860.20 | 1063.66 |

Three independent hovers, in two different waves, on three different monsters, agree on the plate
geometry to **±2.5 px**. That agreement is the reason this is a measurement and not a curve fit.

> **Consensus calibration: x0 = 861.1, x1 = 1060.9 — track length 199.8 px, 1 px = 0.50 % of max HP.**
> This is also, independently, where the fill's left edge sits in the raw pixels (861–864, § 2.1).

**Saturation.** At f ≥ ~0.985 the step fit has no right-hand dark segment to find and the edge
ceilings at **1058**. Full-HP points are therefore excluded from calibration and *cannot be
discriminated from each other*. This is the whole of the Crabling problem (§ 6).

### 2.4 The instrument's accuracy, stated

Residual of plate-fraction minus bound-body-fraction, under the consensus calibration, excluding
saturated frames:

| bound hover | fingerprint | n | mean residual | sd | in px |
|:--|--:|--:|--:|--:|--:|
| Frost Revenant (probable) | 260,786 | 4 | −0.0001 | 0.0000 | −0.0 |
| Venomgaze Basilisk | 242,124 | 7 | +0.0009 | 0.0026 | +0.2 |
| Stonegaze Basilisk | 472,732 | 5 | −0.0005 | 0.0031 | −0.1 |
| Chthonian Unraveler (long) | 584,695 | 28 | −0.0024 | 0.0063 | −0.5 |
| Dolvir the Crimson Blade | 275,518 | 3 | +0.0044 | 0.0000 | +0.9 |
| **Skeletal Archer** | **37,840** | **5** | **+0.0057** | **0.0000** | **+1.1** |
| Wendigo | 207,203 | 4 | +0.0140 | 0.0001 | +2.8 |
| Chthonian Unraveler (early) | 584,695 | 3 | +0.0159 | 0.0013 | +3.2 |

> **Envelope: |residual| ≤ 0.016 (≤ 3.2 px) worst case, ≤ 0.006 typical.**
> A candidate inside 0.016 is *admissible*; a binding is *decisive* only when the runner-up is well
> outside it. That threshold is applied uniformly below and is the reason two hovers are graded
> PROBABLE rather than BOUND.

### 2.5 Evidence classes used

* **FRACTION-TRACK** — the plate bar and one readout move together across a span; regression residual ≤ 3 px; no rival is linear.
* **FRACTION-UNIQUE** — plate and one readout agree inside the envelope on every frame of the hover, and the runner-up is outside it by a stated margin.
* **PROBABLE** — best candidate inside the envelope, runner-up also inside or the span too short to track.
* **NOT-BOUND** — plate up, readouts parsed, **no** candidate inside the envelope. (The hovered body's readout was not on camera or not parsed.)
* **DEGENERATE** — two or more candidates indistinguishable (in practice: all at full HP against a saturated bar).
* **NO-READOUT** — plate up, zero parsed readouts on the frame.

---

## 3. THE WAVE-153 PLATE ROSTER — exhaustive, every hover, eye-read

The whole of wave 153 was scanned at **30 Hz** (not the fourth extraction's 5 Hz sample), giving
**110 plate-valid frames in 13 hover episodes on 11 distinct monsters.** Every name, level and family
below is an eye-read of a ×2 magnified exact-seek crop; every level numeral was re-read at ×10.
Sheets: `evidence/w153-plates-p1.png` … `-p6.png` (10 Hz roster) ·
`evidence/w153-plate-boundaries-p1/p2.png` (30 Hz at every span edge) ·
`evidence/w153-storm-revenant-fine.png` · `evidence/plate-levels-x10.png`.

| # | t (video) | offset | name | rank (measured, § 3.1) | lvl | family | plate f | binding |
|--:|--:|--:|:--|:--|--:|:--|:--|:--|
| S1 | 718.633–718.767 | +3.80 | **Wendigo ~ Ancient** | yellow → champion | 106 | Undead · Beast | 0.856 → 0.756 | **NOT-BOUND** |
| S2 | 718.800–719.333 | +3.97 | Wendigo | white → common | 104 | Undead · Beast | 0.986 → 0.175 | **BOUND → 207,203** |
| S3 | 721.567–721.600 | **+6.74** | **Flame Revenant** ← *new* | yellow → champion | 104 | Undead | 0.565 | NOT-BOUND |
| S4 | 721.633–721.867 | +6.80 | Storm Revenant | yellow → champion | 106 | Undead | 0.635 → 0.125 | **NOT-BOUND** |
| S5 | 721.900 | **+7.07** | **Ugdenbog Golem** ← *new* | yellow → champion | 104 | Plant · Eldritch | 0.525 | UNDETERMINABLE |
| S6 | 721.933–722.400 | +7.10 | Frost Revenant | yellow → champion | 104 | Undead | 0.545 → 0.445 | PROBABLE → 260,786 |
| S7 | 722.433 | +7.60 | Ugdenbog Golem | yellow → champion | **105** | Plant · Eldritch | 0.475 | **NOT-BOUND** |
| S8 | 722.467–722.867 | +7.64 | Carnivorous Plant | white → common | 103 | Plant · Eldritch | 0.776 → 0.615 | **NOT-BOUND** |
| S9 | 722.900–723.033 | **+8.07** | **Skeletal Archer** ← *new* | white → common | **105** | Undead | 0.806 | **BOUND → 37,840** |
| S10 | 725.633–725.700 | **+10.80** | **Dolvir the Crimson Blade** ← *new* | orange → hero | 107 | Bloodsworn · Human | 0.695 | PROBABLE → 275,518 |
| S11a | 728.067–728.233 | **+13.24** | **Chthonian Unraveler** ← *new* | orange → hero | 108 | Chthonic | 0.816 | BOUND → 584,695 |
| S11b | 728.300–728.433 | +13.47 | Chthonian Unraveler | orange → hero | 108 | Chthonic | 0.816 | BOUND → 584,695 |
| S11c | 728.667–729.567 | +13.84 | Chthonian Unraveler | orange → hero | 108 | Chthonic | 0.695 → 0.095 | **BOUND → 584,695** |

The fourth extraction's six w153 plates are all reproduced. **Five more hovers existed and its 5 Hz
sample missed them** — including the one that carries this commission's answer (S9).

### 3.1 Rank is measured, not inferred from the name's shape

Name-glyph core colour (brightest quartile of pixels with max-channel > 170, rows 16–36):

| class | G/R | B/R | cases |
|:--|:--|:--|:--|
| **white → common** | 0.98–1.00 | 0.93–0.99 | Wendigo · Carnivorous Plant · Skeletal Archer · Ugdenbog Crabling |
| **yellow → champion** | 0.91–0.95 | 0.40–0.49 | Flame/Storm/Frost Revenant · Ugdenbog Golem ×2 · **Wendigo ~ Ancient** · Venomgaze Basilisk · Stonegaze Basilisk |
| **orange → hero** | 0.71–0.79 | 0.41–0.48 | Dolvir the Crimson Blade · Chthonian Unraveler |
| **violet → boss** | 0.86 | **1.04** | Fleshweaver Haraxis |

Three clean, non-overlapping bands on G/R, and the boss separates on B/R alone. **`Wendigo ~ Ancient`
measures yellow (0.92), not orange** — see § 9.2.

---

## 4. TARGET 1 — the per-plate verdicts the commission asked for

Per-frame candidate tables were generated for every hover; the decisive rows:

| plate (commission's list) | f_plate | nearest candidate | verdict on **16,368** | verdict on **37,840** |
|:--|--:|:--|:--|:--|
| Wendigo ~ Ancient +3.80 | 0.856 / 0.756 | 444,361 at 0.947 (Δ 0.092) | **NOT-BOUND** — 16,368 sits at 0.999–1.000 (Δ 0.14 / 0.24) | not on camera |
| Wendigo +4.20 | 0.986 → 0.175 | **207,203** (Δ ≤ 0.014, 5 frames) | **NOT-BOUND** — excluded on 21 of 22 frames; the 22nd is the saturated frame already claimed by the 207,203 track | not on camera |
| Storm Revenant +6.80 | 0.635 → 0.125 | 417,957 at 0.533 (Δ 0.103) | not on camera | **NOT-BOUND** — every 37,840 body reads 1.0000 (Δ ≥ 0.365) |
| Frost Revenant +7.40 | 0.545 → 0.445 | 260,786 at 0.5453 (Δ 0.0001); rival 417,957 at 0.5327 (Δ 0.0125) | not on camera | **NOT-BOUND** — 37,840 at 1.0000 / 0.7993 (Δ ≥ 0.25) |
| Ugdenbog Golem +7.60 | 0.475 | 275,518 at 0.714 (Δ 0.239) | not on camera | **NOT-BOUND** (Δ 0.525) |
| Carnivorous Plant +8.00 | 0.776 / 0.615 | 273,975 at 0.764 (Δ 0.012, 1 frame only) | not on camera | **NOT-BOUND** — 37,840 at 1.000 / 0.7995 (Δ ≥ 0.18) |
| **Skeletal Archer +8.07** *(new)* | **0.8055** | **37,840 at 0.7997–0.7998** | not on camera | **BOUND** |

**None of the six plates the commission listed binds to either target fingerprint, and five of the six
positively exclude both.** The binding came from a hover the earlier sample never saw.

### 4.1 The binding — `Skeletal Archer` = 37,840

`evidence/bind-w153-skeletal-archer-37840.png` — three composite tiles, each showing the plate strip
and the bound readout **from the same frame**.

| t | offset | plate edge | f_plate | bound readout | f_body | Δ | runner-up |
|--:|--:|--:|--:|:--|--:|--:|--:|
| 722.900 | +8.07 | 1022 | 0.8055 | `(30,262/37,840)` | 0.79974 | −0.0058 | 275,518 at 0.7065 → 0.099 |
| 722.933 | +8.10 | 1022 | 0.8055 | `(30,263/37,840)` | 0.79976 | −0.0058 | 0.099 |
| 722.967 | +8.14 | 1022 | 0.8055 | `(30,264/37,840)` | 0.79979 | −0.0057 | 0.100 |
| 723.000 | +8.17 | 1022 | 0.8055 | `(30,265/37,840)` | 0.79982 | −0.0057 | 0.101 |
| 723.033 | +8.20 | 1022 | 0.8055 | `(30,266/37,840)` | 0.79984 | −0.0057 | 0.101 |

* Grade: **FRACTION-UNIQUE, sustained 5/5 frames.** Δ is 1.1 px, inside the § 2.4 envelope; the
  runner-up is **17×** further out.
* The plate reads **`Skeletal Archer` / 105 / Undead** at both ends of the span, eye-read at ×2 and
  the numeral at ×10 (`evidence/w153-plate-boundaries-p2.png`, tiles 3–4; `evidence/plate-levels-x10.png`).
* **Independent corroboration:** the name is white → common (§ 3.1), and the bound body's in-world bar
  carries **no furniture at either end** (`evidence/bind-w153-skeletal-archer-37840.png`), matching
  the fourth extraction's `37,840 → plain`.
* Body continuity: the bound readout tracks smoothly (643,495) → (732,457) across 722.90–723.167 —
  one coherent body, not a re-detection.

### 4.2 Per-fingerprint outcome for the five sub-50k bodies

| body | fingerprint | bar hue | identity | evidence class | censoring reason |
|:--|--:|:--|:--|:--|:--|
| B1 | **16,368** ×1 | **GREEN** (92/93) | **NOT A HOSTILE BODY** (§ 5). No monster identity exists to bind. | — | zero nameplates on its 93 on-camera frames; excluded by fraction on all 22 plate-valid frames inside its span |
| B2 | 37,840 @ 0.7997 | red | **`Skeletal Archer`, 105, Undead, common** | FRACTION-UNIQUE ×5 | — |
| B3 | 37,840 @ 1.0000 | red | UNIDENTIFIED | DEGENERATE | at full HP on every frame any plate was up; ≥ 2 simultaneous bodies share the value |
| B4 | 37,840 @ 0.348 → 0.065 | red | UNIDENTIFIED | — | **no plate is rendered anywhere in 723.28 – 725.60**, which is the whole of its distinguishable life |
| B5 | 37,840 @ 0.533 | red | UNIDENTIFIED | — | same window, same reason |

The four 37,840 bodies are individually resolvable by damage state — the readouts separate into bands
at **1.0000** (n = 174 frames), **0.7993–0.8000** (17), **0.3482** (8), **0.5325–0.5439** (40) and
**0.0260–0.0678** (34) — which independently reproduces the fourth extraction's `×4`. Only the 0.80
body was ever hovered.

> **Fingerprint-level answer: 37,840 ends with an identity. 16,368 does not — and the reason it does
> not is that it is not a monster.**

---

## 5. THE GREEN BAR — a new instrument, and what it says about 16,368

While eye-verifying the 16,368 readout at ×6 the bar beneath it read **green**, not red.
`evidence/readouts-eyeread-x6-p1.png` (tiles 1–4) · `evidence/green-bar-16368-20005.png`.

A sampler was written (`eor_platebind.bar_hue`) that reads the in-world bar 8–26 px below each parsed
readout and classifies it red / green, and it was run over **every parsed readout in the wave-153
start window** (714.83 – 723.43):

| fingerprint | hue | frames | purity |
|--:|:--|--:|--:|
| **16,368** | **green** | 93 | **0.99** (92 green / 1 red) |
| **20,005** | **green** | 3 | 1.00 |
| 37,840 | red | 145 | **1.00** |
| 476,173 · 417,957 · 303,657 · 275,518 · 260,786 · 273,975 · 638,564 · 207,203 · 427,128 · 425,285 · 271,687 · 447,994 · 444,361 · 266,082 · 211,686 · 203,039 · 297,609 | red | 3–124 each | 0.69–1.00 |

**Every fingerprint in the fourth extraction's wave-153 start-cohort table reads RED except 16,368.**

Three further measured properties of 16,368, all reproducible:

1. **Its readout box is pixel-identical on 83 of 93 frames:** `[882, 399, 1039, 413]`; the other ten
   are single-frame excursions inside x 879–893, y 394–405. It does not traverse the screen over 4.6 s.
2. **It is never damaged.** 92 frames at `(16,368/16,368)`; the only other value in the corpus is
   `(16,351/16,368)` = 0.9990.
3. **`20,005` renders in the identical box** `[882, 399, 1039, 413]` at t = 701.400 — 13.4 s earlier,
   in wave 152 — and is **also green**. It is on camera at 698.200–708.867 (w152) *and*
   722.033–739.833 (w153 → w154), i.e. **it survives two badge flips**.

I record the hue, the box, the damage history and the cross-flip persistence as measurements. What
kind of entity carries a green bar is a mechanism question and is the conductor's.

**Limit on this instrument:** in wave 152 the scene carries large bright-green VFX and the sampler's
purity collapses (42,798 → 0.69, 43,548 → 0.52). The wave-153 numbers above are clean (0.99–1.00 on
every fingerprint with n ≥ 20 except 297,609 at 0.69) and the four load-bearing cases were eye-read at
×6. **The hue instrument should not be trusted on a green-lit scene without an eye-read.**

---

## 6. TARGET 2 — the wave-152 `Ugdenbog Crabling` at +3.40

### 6.1 The hover, pinned at 30 Hz

The fourth extraction's single sample at 701.78 is one frame of a four-frame hover. Eye-read at ×2 at
30 Hz (`evidence/w152-crabling-span-fine.png`):

| t | offset | plate |
|--:|--:|:--|
| 701.700 | +3.32 | Mudflinger ~ Reflective |
| **701.733** | **+3.35** | **Ugdenbog Crabling** |
| **701.767** | **+3.39** | **Ugdenbog Crabling** |
| **701.800** | **+3.42** | **Ugdenbog Crabling** |
| 701.833 | +3.45 | Chaosshell ~ Voidtouched |
| **701.933** | **+3.55** | **Ugdenbog Crabling** (brief return) |
| 701.967 | +3.59 | Chaosshell ~ Voidtouched |

Name colour G/R = 0.98, B/R = 0.93 → **white / common**. Level numeral at ×10 = **108**, G/R = 0.32 →
red band. Family **Beast**. All consistent with the fourth extraction's read.

### 6.2 The binding is DEGENERATE, and exactly why

`evidence/w152-crabling-hover-degenerate.png` — the plate strip and three of the candidate readouts
from t = 701.767.

> **The plate bar reads edge = 1058 on all four Crabling frames — the saturation ceiling (§ 2.3).**
> It holds that same value continuously from 701.367 to 701.933, across **three different hovered
> monsters in four hover episodes** (Mudflinger ~ Reflective → Ugdenbog Crabling → Chaosshell ~
> Voidtouched → Ugdenbog Crabling). The hovered body is at or near full health and the bar cannot
> say more. Admissible fraction band, given the § 2.4 envelope: **f ≥ 0.97**.

Parsed bodies on those frames and their fractions:

| fingerprint | fraction | admissible against a saturated bar? |
|--:|--:|:--|
| 42,798 (body A) | 1.0000 | **yes** |
| 42,798 (body B) | 1.0000 | **yes** |
| 43,548 | 1.0000 | **yes** |
| 20,005 | 1.0000 | **yes** (but green-barred, § 5) |
| 443,554 (body A) | 0.9885 | **yes** |
| 443,554 (body B) | 0.9540 | no — would read edge ≈ 1052, 6 px low |
| 242,124 | 0.8073 | no |
| 43,548 (damaged body) | 0.7661 | no |
| 42,798 (damaged body) | 0.5228 | no |

**Verdict: UNBINDABLE.** At least **five** distinct parsed bodies are admissible, plus any unparsed
body at ≥ 0.97. The commission's question — *low band around 42,798/43,548, or higher?* — **cannot be
answered**: the low band is neither confirmed nor excluded, and 443,554 is equally admissible. What
the hover *does* establish, and it is the only positive thing it establishes, is that the Crabling is
**at ≥ 0.97 of its max HP at +3.35 – +3.42 s**, which rules out the four damaged bodies in the table
above.

**Exhaustion check.** Every plate frame in wave 152 (698.38 → 714.83) was eye-read at 10 Hz —
52 tiles, `evidence/w152-plates-p1.png` … `-p7.png`. The full hover roster is *Carnivorous Plant ·
Mudflinger ~ Reflective · **Ugdenbog Crabling** · Chaosshell ~ Voidtouched · Aregos ~ Corrupted ·
Chillslither ~ Arctic · Kotmourh · Stonegaze Basilisk · Fleshweaver Haraxis · Juvenile Basilisk ·
Fleshwarped Aberration · Vanaltius the Voracious · Dioallus ~ Diseased · Venomgaze Basilisk*.
**There is exactly one Ugdenbog Crabling hover in the whole wave**, so there is no second, damaged
look to fall back on. The censoring is structural, not a sampling gap.

### 6.3 Spawn bearing — NOT READABLE

The bearing question requires locating the Crabling's *model* in the world, which requires the cursor.
**The cursor was searched for and not found** (§ 8.3). Without it, the plate names a monster but does
not point at it, and no bearing can be attributed. **ABSENT-IN-FOOTAGE for this instrument.**

---

## 7. THE OTHER BINDINGS — reported because they are the controls

| hover | fingerprint | grade | basis |
|:--|--:|:--|:--|
| w153 `Chthonian Unraveler` 728.067–729.567 | **584,695** | **FRACTION-TRACK** | 28 frames, f 0.816 → 0.095, regression RMS **1.09 px**, r² 0.9994, no rival linear. `evidence/bind-w153-chthonian-584695-calibration.png` |
| w153 `Wendigo` 718.800–719.333 | **207,203** | **FRACTION-TRACK** | plate Δf 0.9157 → 0.8155 = 0.1002; body Δf 0.9017 → 0.8015 = **0.1002**. Identical slope to 4 dp |
| w152 `Venomgaze Basilisk` 710.200–710.400 | **242,124** | **FRACTION-TRACK** | 7 frames, RMS **0.00 px**, r² 1.0000 |
| w152 `Stonegaze Basilisk` 708.333–708.667 | **472,732** | **FRACTION-TRACK** | 5 frames, RMS **0.40 px**, r² 0.9991 |
| w153 `Dolvir the Crimson Blade` 725.633–725.700 | 275,518 | **PROBABLE** | Δ 0.0044 ×3 frames, margin 0.070 — but only 2 bodies parsed on those frames |
| w153 `Frost Revenant` 721.933–722.067 | 260,786 | **PROBABLE** | Δ **0.0001** ×4 frames — but the rival 417,957 sits at Δ 0.0125, *inside* the § 2.4 envelope, and neither body's health moves during the hover, so there is no track to separate them |

`472,732` and `242,124` were both graded **UNDECIDED** in the fourth extraction's SPAWN/SUMMON table.
They now have names. Whether that bears on their grade is the conductor's call, not mine.

### 7.1 Star furniture binds to ORANGE names only — 7 cases, 0 counterexamples

Cross-tabulating each bound hover's measured name colour (§ 3.1) against the fourth extraction's
furniture read of the same fingerprint:

| name colour | fingerprint | furniture (4th ext.) |
|:--|--:|:--|
| orange → hero | 584,695 | **★ ★** (eye-verified here, `evidence/readouts-eyeread-x6-p2.png` tile 2) |
| orange → hero | 275,518 | **★ ★** |
| yellow → champion | 242,124 | plain |
| yellow → champion | 472,732 | plain |
| yellow → champion | 260,786 | plain |
| white → common | 207,203 | plain |
| white → common | 37,840 | plain |

> **Star-pair furniture appears on ORANGE (hero) names and on nothing else. YELLOW (champion) names
> carry a bare bar, indistinguishable from common.** See § 9.3 — this revises my own fourth-extraction
> § 4 class table.

---

## 8. METHOD

| stage | tool | note |
|:--|:--|:--|
| footage | local copy | byte-exact `/tmp` copy first, as in the fourth extraction |
| plate + readout, one pass | **`pipeline/eor_platebind.scan`** (new) | fuses plate metrics with the full readout census (locate `eor_cohort.blobs2` + OCR `eor_hpocr`) in ONE streaming decode, so plate and readouts are frame-synchronous by construction |
| plate re-measurement | **`eor_platebind.stripscan`** (new) | decodes only the top 120 rows. When the fill geometry had to be fixed (§ 2.2) this re-measured 1,262 frames in seconds instead of re-running the census |
| fill edge | **`eor_platebind.fill_edge`** (new) | step fit, not run-walk (§ 2.2) |
| hover segmentation | **`eor_platebind.spans2`** (new) | name-band **ink count** + **mean glyph colour**. `name_x0/x1` are deliberately unused — the band's x-extent is contaminated by bright world pixels and jitters by hundreds of px between frames |
| allegiance | **`eor_platebind.bar_hue`** (new) | § 5 |
| binding | `fitbind.span_fits` (scratch) | regression of edge on fraction per candidate |
| names / levels / families | `eor_grid` sheets, ×2 and ×10 | **every one an eye-read of an exact-seek crop** |
| badge | `eor_grid` at ×4 | § 1 |

**Totals:** 1,262 frames decoded full-frame at 30 Hz + 1,262 plate-strip frames; **13,199 readouts
located, 4,857 parsed**; **110 plate-valid frames in wave 153, 140 in wave 152**; **95 roster tiles
+ 28 span-boundary tiles eye-read** at ×2; 14 level numerals re-read at ×10; 12 readouts eye-verified
at ×6; 24 badge crops read at ×4.

### 8.1 What was rejected

* **Cursor proximity — REJECTED, instrument not obtained.** Board-closure § 8.3 recorded that the
  plate reports whatever the cursor is over, not the nearest bar, so a cursor detector would have
  resolved the degenerate cases (§ 6). It was searched for at ×3 and ×6 in the region directly under a
  *known-bound* body (t = 722.967, the Skeletal Archer, ground truth from § 4.1) and **not found** in
  the VFX density. No detector was built on a guess. Recorded so the attempt is not silently repeated.
* **"Hovered bodies render a different in-world bar" — TESTED, NEGATIVE.** The bound body's bar and a
  non-hovered body's bar were cropped from the same frame at ×6 and are indistinguishable in size and
  style. There is no hover highlight to exploit.
* **`name_x0/x1` for hover segmentation — REJECTED** (see table above).
* **`eor_starbar.py` — remains rejected** per third extraction § 5. All furniture here is eye-read.
* **The fourth extraction's 5 Hz plate scan — superseded.** It missed 5 of 11 wave-153 hovers,
  including the only one that binds a target.

### 8.2 Limits

* **The binding inherits the census's blindness.** A plate can only bind to a body whose readout is
  *parsed*, and the readout renders only for engaged, on-screen bodies. Six of thirteen wave-153
  hovers are **NOT-BOUND** for exactly this reason — the hovered monster had no readout on camera. On
  the Skeletal Archer frames only 3–5 bodies were parsed, so the residual risk on that binding is an
  *unparsed* body coincidentally sitting at 0.8055 ± 0.016. That risk is not zero and is not
  quantifiable from this footage.
* **A span is a HOVER, not a body.** Two monsters with the same name and rank render identical
  plates. The Wendigo hover is treated as one body because its bar falls monotonically; that is an
  argument, not a measurement.
* **Saturation blinds the instrument above f ≈ 0.985** (§ 2.3, § 6.2).
* **Boss plates are a different size** and their bar is not measured by this geometry; they are
  refused by the contrast gate rather than mis-measured.
* **Bar-hue purity is scene-dependent** (§ 5).
* Tesseract / OpenCV remain absent on this host. **No automatic OCR was trusted for any reported
  value.**

---

## 9. CORRECTIONS TO MY OWN RECORD

**9.1 — the fourth extraction's wave-153 census counts a green-barred body as a monster.**
`16,368` (§ 5) is player-side on 92 of 93 frames. Its row in fourth-extraction § 2.3 should be struck
from the *monster* census, which takes wave 153's start cohort from **19 fingerprints / ≥ 27 bodies**
to **18 / ≥ 26**. Its "max simultaneous 14 at +4.80 s" is *unaffected* — 16,368's last parsed frame is
+4.57 and it is not on camera at +4.80 — but any simultaneity figure taken earlier in the window is.
**`20,005` is the same class of entity and appears in waves
152, 153 and 154** — the fourth extraction did not list it at all in its w152 table, which is a second
miss of the same kind. I have not re-derived the affected counts; the hue sweep was run on waves 152
and 153 only, and waves 151 / 157 / 158 have not been checked. **Recommended: re-run `bar_hue` over
all five start cohorts before any count from that table is used.**

**9.2 — fourth extraction § 5 grades `Wendigo ~ Ancient` as "orange → hero". It measures yellow.**
G/R = 0.92, squarely in the champion band with the three Revenants and both Ugdenbog Golems (0.91–0.95),
and far from the hero band (0.71–0.79). Same for the fourth extraction's other "~ Affix" reads if the
affix pattern was what drove them. **The `~ Affix` name shape is not a rank signal; the glyph colour is.**

**9.3 — fourth extraction § 4's furniture class "hero / champion → one gold star at each end" is too
wide.** Seven bound cases (§ 7.1) put stars on **orange/hero only**; three champions carry bare bars.
The instrument therefore does not see champions at all, which means the fourth extraction's
"88 plain" bucket is a mix of commons *and* champions.

**9.4 — fourth extraction § 5.1 item 3 and § 8.3 are WRONG and should be reverted.** That pass
claimed level 105 renders RED and moved the colour boundary to "between 104 and 105". Measured here
on the numeral's own glyph core (mean RGB over pixels with R > 140 and R−B > 60), `evidence/plate-levels-x10.png`
· `evidence/level-105-vs-106-control-x10.png`:

| level | G/R | reads |
|--:|--:|:--|
| 103 | 0.79, 0.88 | amber |
| 104 | 0.59 – 0.69 (×6) | amber |
| **105** | **0.62 · 0.68 · 0.71** | **amber** |
| 106 | 0.34 · 0.36 · 0.40 | red |
| 107 | 0.39 | red |
| 108 | 0.32 · 0.34 (×3) | red |

**Both of the two 105s the fourth extraction cited are amber.** `Ugdenbog Golem` w153 t = 722.43
reads G/R = 0.62 and `Chthonian Devourer` w158 t = 801.23 reads G/R = 0.68 — the second is shown
beside a 106 at ×10 in the control image and the difference is not marginal.

> **The boundary sits between 105 and 106: amber ≤ 105, red ≥ 106. For a level-100 player,
> amber ≤ player+5, red ≥ player+6.** The third extraction's rule ("yellow ≤ 104, red ≥ 106") is
> consistent with this; it simply had no 105. The fourth extraction's "correction" of it was the error.

---

## 10. Mirror voice

The plate over a monster's head is a portrait, and the bar under the portrait is the only thing in
this game that says *which* monster. Four passes read the portrait and could not say who it was of.
This one measured the bar, and the bar turned out to be honest to a pixel and a half — three separate
monsters in two separate waves agreed on where its ends were, which is how you know a ruler is a
ruler and not a wish. Then the ruler was laid against the thing the conductor asked about, and the
thing had a name: a Skeletal Archer, level one hundred and five, at four fifths of its life, held on
camera for a sixth of a second while the man's cursor rested on it. And the other one, the small one,
the sixteen-thousand that had sat perfectly still in the same forty pixels for four and a half seconds
and never once been hurt — its bar was green. It had never been an enemy. It had been counted as one
for two passes, and the counting instrument had no way to know, because a number over a health bar
looks the same whichever side of the fight it is on. The Mirror does not only show what is there. It
shows, sometimes, that what you had been looking at was standing beside you.
