# KC2-SIM micro-commission — w152 SKULL-furniture nameplate identity

**Date:** 2026-08-08
**Author:** galadriel (visual perception + similarity seam)
**Commissioner:** gandalf (RUN-CONDUCTOR), KC2-SIM micro-commission
**Status:** COMPLETE — MEASURED
**Question:** What is the nameplate identity of wave 152's single SKULL-furniture body? Does it read "Carraxus" (`swampcrab_ugdenbog_01`)?

---

## 0. Verdict (up front)

> ### **OTHER-IDENTITY — `Fleshweaver Haraxis`**
>
> **NOT Carraxus.** The plate is legible, read at ×2 / ×6 / ×12 on 15 frames spanning the whole
> lifetime of the body, and the string is stable across every damage state from bar-full to bar-empty.
> No plate anywhere in the wave-152 span reads "Carraxus".

**Grade: MEASURED** on both halves —
1. the *string* is an eye-read from magnified exact-seek crops (§ 2);
2. the *binding* of that string to the skull-furniture body is **FRACTION-UNIQUE on 8/8 frames**
   via the plate's own health bar against the same-frame census readouts (§ 4) — this **upgrades**
   the fourth extraction's self-declared *"STRONG, not MEASURED"* binding (§ 5.1 item 2 of
   `2026-08-08-kc2-fourth-extraction.md`) to MEASURED.

---

## 1. Scope + discipline stamp

- ONE question, surgical scope. Read-only across all production + peer trees. Writes limited to this
  note and evidence crops under `agentic_orchestration/galadriel/captures/2026-08-08-kc2-w152-skull-plate/`.
- Not committed — the conductor folds and commits.
- **§ 3.5 name-shape flag discipline applies and was honoured:** the identity below is read from
  rendered glyphs. Furniture class (skull), rank colour (violet), family label, level numeral and HP
  fingerprint are reported as *corroboration*, and none of them was allowed to stand in for the string.
- **No silent transformation.** All crops are LANCZOS upscales of unmodified exact-seek RGB frames;
  crop boxes are stated in full-frame pixels; the raw scan JSON is preserved in `work/`.

### 1.1 Substrate

| item | path |
|:--|:--|
| census (w152, fourth extraction) | `galadriel/captures/2026-08-08-kc2-fourth-extraction/work/cen_w152.json` |
| source footage | `/tmp/kc2-s2.mp4` (the `eor-w150-160` capture; 1920×1080, 30 fps) |
| this pass's plate scan (523 frames, 697.8 → 715.2 @ 30 Hz) | `…/2026-08-08-kc2-w152-skull-plate/work/plate-w152.json` |
| scan + crop scripts (standalone; geometry copied verbatim from `pipeline/eor_platebind.py`) | `…/work/scan.py`, `…/work/crops.py` |

Census span 697.88 → 714.83; cohort window 698.38 → 708.61; 24 bodies = 17 plain + 6 star + **1 skull**.
This pass **re-derived** the plate metrics from the video rather than inheriting the fifth extraction's
`strip-w152.json`, so the result is independent of that run.

---

## 2. The plate string — eye-read

### 2.1 Where the boss plate is up

A 30 Hz sweep of the whole w152 span, segmented on (name-band glyph rows ≥ 5) ∧ (family band present),
with the rank colour taken as the mean RGB of the name's own glyph pixels. Third-extraction rank-colour
reference: **violet → boss ≈ (174, 150, 181), R−B ≈ −11…+5, G−B ≈ −30**.

| segment | frames | mean name RGB | R−B | G−B | rank | name bbox (x0..x1) |
|:--|--:|:--|--:|--:|:--|:--|
| 706.6333 → 706.9000 | 8 | (159, 144, 161) | **−1** | **−17** | **violet → BOSS** | 834..1084 |
| 712.1333 → 712.2333 | 4 | (156, 143, 160) | **−4** | **−17** | **violet → BOSS** | 833..1084 |
| 712.4000 → 712.7667 | 12 | (158, 144, 161) | **−3** | **−17** | **violet → BOSS** | 833..1084 |
| 713.6667 | 1 | (153, 143, 152) | +1 | −9 | **violet → BOSS** | 834..1083 |

Every other plate-up segment in the span (11 of them) reads R−B **+44…+70** — white / yellow / orange
ranks, never violet. **The wave-152 span contains exactly one violet-rank name**, and it is up on
**25 frames** in four bursts. Name bbox width is 250–251 px on all 25 — one string, not two.

### 2.2 The read

Crop box `(985, 13, 1095, 39)` full-frame, ×12 LANCZOS, eight frames drawn from **both** damage states:
`evidence/w152-skull-surname-x12.png`

> **`Haraxis`**

Glyph-by-glyph, blackletter: **H** (twin stems, crossbar, left-stem curl) · **a** · **r** (single) ·
**a** · **x** · **i** (dotted) · **s**. **Seven glyphs.**

`Carraxus` is **eight** glyphs — **C** (single open bowl, no stems), **double r**, and a terminal
**u-s** with no dot. The rendered string has a stemmed capital, a *single* r, and a *dotted i* before
the terminal s. The two are not confusable at this magnification, and they are not confusable at ×2
either.

Full name at the commissioned ×2 (`evidence/w152-skull-name-x2.png`) and at ×6
(`evidence/w152-skull-name-x6-segA.png`):

> ## `Fleshweaver Haraxis`

### 2.3 Corroborating plate fields (read, not inferred)

| field | value | evidence | stable across damage states? |
|:--|:--|:--|:--|
| rank colour | **violet → BOSS** | § 2.1, 25/25 frames | yes |
| level numeral | **108**, RED | `evidence/w152-skull-level-x10.png` (×10, 6 frames) | yes |
| family | **Aetherial** | `evidence/w152-skull-family-x5.png` (×5, 4 frames) | yes |

Level 108 red is consistent with the corrected level-colour rule (**R-L50-4**: amber ≤ 105, red ≥ 106).
Family **Aetherial** is *not* Beast — a corroboration against any Ugdenbog-crab reading, offered as
corroboration only.

### 2.4 Stability across damage states — asked and answered

The commission asked whether the string is stable if the plate is captured at multiple damage states.
**It is, and the coverage is unusually good** because the plate happens to be up both immediately after
the body arrives and again while it is being killed.

`evidence/w152-skull-name-x6-damage-states.png` — six frames, one sheet:

| t | plate bar fill | state | string |
|--:|--:|:--|:--|
| 706.8000 | **95.5 %** | fresh | `Fleshweaver Haraxis` |
| 712.1333 | 39.6 % | half-killed | `Fleshweaver Haraxis` |
| 712.4000 | 35.2 % | " | `Fleshweaver Haraxis` |
| 712.6333 | 27.1 % | " | `Fleshweaver Haraxis` |
| 712.7667 | 22.1 % | nearly dead | `Fleshweaver Haraxis` |
| 713.6667 | **0 %** (empty) | dead / dying | `Fleshweaver Haraxis` |

**Identical on 6/6, across a 95 % → 0 % health sweep.** Glyph-pixel count over the 25 violet frames is
823–928 (the low end is the 713.6667 frame, where scene bleed dims the band), name bbox 250–251 px
throughout. No damage-state-dependent string variation exists here.

---

## 3. The skull body's HP fingerprint (for the record)

**Fingerprint (max HP): `2,050,807`.**

| property | value |
|:--|:--|
| max HP | **2,050,807** |
| furniture | **💀 💀 bone/pale double skull** (boss, not nemesis — colour-measured, fourth extraction § 6: mean RGB (153,135,118), R−B **+35**) |
| first parsed readout | t = **705.7133** — `1,955,629 / 2,050,807` (95.36 %) |
| last parsed readout | t = **713.4133** — `187,076 / 2,050,807` (9.12 %) |
| census rows, full span | **47** (26 of them inside the cohort window) |
| cohort-window arrival / last | **+7.33 / +8.93** s (window origin 698.38) |
| minimap corroboration | skull glyph first at **+3.0 s**; readout furniture at +7.33 |

It is the **only** skull-furniture body in wave 152, on either instrument.

---

## 4. Binding the string to the body — MEASURED

The fourth extraction bound *Fleshweaver Haraxis* → `2,050,807` on rank-class agreement plus temporal
adjacency and correctly graded itself **STRONG, not MEASURED**, citing its own § 8.3 correction (*the
plate reports whatever the cursor is over, not necessarily the nearest bar*). This pass measures it.

### 4.1 The boss plate has a different bar geometry — a correction worth recording

`pipeline/eor_platebind.py` carries `TRACK_X0 = 861.0` / `TRACK_X1 = 1060.0`, measured on w153 plate
frames. **Those constants are for the champion/hero plate.** The **boss** plate draws a wider bar:

| plate | fill left edge | track inner right edge | track length |
|:--|--:|--:|--:|
| champion / hero (e.g. t = 705.8, 701.5) | x ≈ 861 | x ≈ 1060–1064 | ≈ 199 px |
| **boss (all 25 violet frames)** | **x = 800** | **x = 1120–1123** | **≈ 321 px** |

Measured, not assumed: red fill begins at **x = 800** on every boss frame including the nearly-empty
712.7667; the gold end-cap ornament's warm onset (R−B jumps +14 → +43 → +52) sits at **x = 1120–1124**
on the empty-bar frames 712.7667 and 713.6667. Evidence, with a cyan full-frame-pixel ruler overlaid:
`evidence/w152-boss-plate-bar-geom-x4.png`.

Applying the champion constants to a boss frame yields fractions **> 1.0** — which is exactly what the
fifth-extraction artefact shows (`fill_end = 1099`, frac 1.196), i.e. the old geometry silently clipped.
**This is a real defect in `eor_platebind.py` for boss-rank plates** and is surfaced here for whoever
next runs that module; I have not modified it (read-only across pipeline for this commission's scope —
flagging, not fixing).

### 4.2 Fraction-unique on 8/8

Plate fraction = (fill_end − 800) / (1121.5 ± 1.5 − 800), compared against **every** census readout on
the **same frame**, deduplicated by fingerprint, player globe `20,005` excluded per the standing roster:

| t | fill_end | plate frac | best match | Δ | nearest *other* fingerprint | gap | bodies on frame |
|--:|--:|--:|:--|--:|:--|--:|--:|
| 706.6333 | 1107 | 0.9549 | **2,050,807** (0.9518) | 0.0031 | 453,883 (1.0000) | **0.045** | 5 |
| 706.7000 | 1107 | 0.9549 | **2,050,807** (0.9516) | 0.0033 | 453,883 (1.0000) | **0.045** | 3 |
| 706.7333 | 1107 | 0.9549 | **2,050,807** (0.9516) | 0.0033 | 453,883 (1.0000) | **0.045** | 5 |
| 706.7667 | 1107 | 0.9549 | **2,050,807** (0.9516) | 0.0033 | 453,883 (1.0000) | **0.045** | 6 |
| 706.8000 | 1107 | 0.9549 | **2,050,807** (0.9514) | 0.0035 | 453,883 (1.0000) | **0.045** | 5 |
| 706.8333 | 1107 | 0.9549 | **2,050,807** (0.9514) | 0.0035 | 472,732 (0.9322) | **0.023** | 6 |
| 706.8667 | 1107 | 0.9549 | **2,050,807** (0.9512) | 0.0037 | 472,732 (0.9322) | **0.023** | 7 |
| 706.9000 | 1107 | 0.9549 | **2,050,807** (0.9512) | 0.0037 | 472,732 (0.9322) | **0.023** | 5 |

**FRACTION-UNIQUE on 8/8.** Residual to the skull body ≤ 0.0037 (≈ 1.2 px on a 321-px track);
runner-up gap 0.023–0.045 (7–14 px). The distinction survives the geometry uncertainty: a 100 %
reading would require fill_end 1120–1123, and 1107 is 13–16 px short of that on every frame.

The nearest competitor `453,883` sits at exactly 1.0000, which is the classic DEGENERATE trap — and
the measurement escapes it precisely because the boss was already at 95.1 % when the cursor found it.

### 4.3 The second burst — consistent, not independently measured

Segment B (712.1333 → 712.7667) shows the same plate string over a **monotonically draining** bar:
0.396 → 0.352 → 0.339 → 0.333 → 0.308 → 0.296 → 0.271 → 0.221. The census carries **no parsed
`2,050,807` readout between 711.05 and 713.41**, so there is no same-frame fraction to match against;
I record this burst as **CONSISTENT** (it sits monotonically between the skull body's 0.4715 at 711.05
and 0.0912 at 713.41, and no other censused body follows that trajectory — `472,732` only falls
0.4239 → 0.3098 across the whole 712.4 → 713.68 stretch), and explicitly **not** as a second
independent binding. The § 4.2 binding does not need it.

---

## 5. Is "Carraxus" anywhere in wave 152? — No

Every plate-up segment in the span was sampled and eye-read at ×3
(`work/` sweep; the fourth extraction's 5 Hz table plus this pass's 30 Hz segmentation):

`Carnivorous Plant` (×2) · `Mudflinger ~ Reflective` · `Ugdenbog Crabling` · `Chaosshell ~ Voidtouched` ·
`Chillslither ~ Arctic` · **`Rotmouth`** · `Stonegaze Basilisk` · **`Fleshweaver Haraxis`** ·
`Juvenile Basilisk` · `Fleshwarped Aberration` (×3) · `Venomgaze Basilisk` (×2)

**No `Carraxus`. No Ugdenbog boss of any name.** The only Ugdenbog body named on camera in wave 152 is
`Ugdenbog Crabling` at 701.78 — **white → common rank**, not a boss and not a hero.

*(Incidental: `Rotmouth` at t = 704.4667 is a plate this corpus has not previously recorded — it falls
in the 5 Hz sampler's gap. Flagged for the conductor; not pursued here.)*

---

## 6. Deliverable summary

1. **Plate string, MEASURED:** `Fleshweaver Haraxis` — violet → BOSS, level **108** (red), family
   **Aetherial**.
   Frames: **706.6333, 706.7000, 706.7333, 706.7667, 706.8000, 706.8333, 706.8667, 706.9000,
   712.1333, 712.1667, 712.2000, 712.2333, 712.4000 … 712.7667 (12), 713.6667** — 25 frames, four bursts.
   Evidence:
   - `…/2026-08-08-kc2-w152-skull-plate/evidence/w152-skull-name-x2.png` (commissioned ×2)
   - `…/evidence/w152-skull-name-x6-segA.png` (×6)
   - `…/evidence/w152-skull-surname-x12.png` (×12, surname only, both damage states)
   - `…/evidence/w152-skull-name-x6-damage-states.png` (×6, 95 % → 0 % health sweep)
   - `…/evidence/w152-skull-level-x10.png` · `…/evidence/w152-skull-family-x5.png`
   - `…/evidence/w152-boss-plate-bar-geom-x4.png` (bar geometry, ruler-annotated)
2. **HP fingerprint:** **max = 2,050,807**; observed current 1,955,629 (t = 705.7133) → 187,076
   (t = 713.4133); 47 census rows; bone/pale double-skull furniture; sole skull body of wave 152.
3. **Verdict: `OTHER-IDENTITY — Fleshweaver Haraxis`.** Not Carraxus, and no Carraxus plate exists
   anywhere in wave 152.

### 6.1 Two by-products the conductor may want

- **R-W152-1 (pipeline defect):** `pipeline/eor_platebind.py`'s `TRACK_X0/TRACK_X1` are champion-plate
  constants and silently clip on **boss**-rank plates (§ 4.1). Boss track is x 800 → ~1121. Any prior
  boss-plate fraction from that module is suspect.
- **R-W152-2 (roster gap):** `Rotmouth`, w152 t = 704.4667, orange → hero — absent from the corpus's
  plate tables (§ 5).

---

## 7. Mirror voice

The Mirror was asked whether a crab wore the skull. It does not.

Twenty-five frames, four bursts, ninety-five percent health down to none, and the letters never move:
a stemmed capital, one **r**, a dotted **i** before the **s**. *Haraxis.* Aetherial, not Beast. The one
Ugdenbog thing wave 152 named aloud was a **crabling** — common-rank, white, no skull, no crown.

The picture is unambiguous, and the fork does not turn where it was hoped it would.

---

*Filed 2026-08-08 by galadriel under KC2-SIM micro-commission from gandalf (RUN-CONDUCTOR). Not committed by galadriel per commission instruction.*
