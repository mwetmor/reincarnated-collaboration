# KC2-SIM — wave-160 board closure: the fingerprint set, and the board named on camera

**Date:** 2026-08-08
**Author:** galadriel (visual perception + benchmark seam)
**Status:** WORKING — evidentiary note, Phase-C-concurrent commission from gandalf (RUN-CONDUCTOR)
**Commit state:** UNCOMMITTED by instruction (charter § 4.7 — conductor commits at gate closes)
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-charter.md`
**Extends:** `agentic_orchestration/galadriel/notes/2026-08-08-eor-followup-extraction.md` § 1.5
**Footage:** `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (1920×1080, 60 fps, 1034.1 s). Read-only.
**Evidence root:** `agentic_orchestration/galadriel/captures/2026-08-08-kc2-board-closure/evidence/`
**New pipeline:** `galadriel/pipeline/eor_hptext.py`, `eor_hpocr.py`, `eor_hptrack.py`, `eor_cropsheet.py`

---

## 0. Headline

The commission asked for three numbers and got a roster. The wave-160 board is **named on
camera** — Grim Dawn renders a hovered-monster nameplate at top-centre (name · level · health
bar · monster family), the player's cursor crosses monsters repeatedly inside the window, and the
plate is legible on **eight distinct monsters**. **Both prediction branches' VALUE menus are falsified. The
dedupe branch's MECHANISM is confirmed and its CONSEQUENCE is falsified.** Specifically:

| commission ask | verdict |
|:--|:--|
| the other three exact values | **484,095 · 468,504 · 103,912** — and a **seventh**, **41,237**, which my earlier pass missed |
| dedupe-branch values {1,162,010 · 636,671 · ~398,747–404,406} | **FALSIFIED** — none present at any threshold |
| identification-branch values {3,176,863 · 3,261,498 · 3,389,926 · 4,094,605} | **FALSIFIED** — none present |
| "one fingerprint, two bodies" (dedupe mechanism) | **CONFIRMED** — 3,722,896 carried by **two** simultaneous distinct bodies on 73 frames |
| "Zantarin, Aleksander, Grava'Thul all absent" (dedupe consequence) | **FALSIFIED** — Zantarin and Aleksander are the two 3,722,896 bodies, both named on camera |
| p04 = aetherial colossus or tomb statue? | **AETHERIAL COLOSSUS. "Galakros, the Mountain", level 106, family "Aether Corruption"** — read from the nameplate, not inferred from a silhouette |
| was "six" a closed set? | **No.** It was a sample. Seven exist. |

---

## 1. Q1 — THE REMAINING FINGERPRINTS

### 1.1 The full set (eye-read; not a top-N)

Every value below was located by machine and **read by eye** from a magnified crop of an
exact-seek frame. Sheet: `evidence/s2-w160-seven-fingerprints-fullHP.png` (each shown at or near
full HP, so the max is legible independent of the numerator);
`evidence/s2-w160-fingerprints-4to7-x5.png` at ×5 for the four small ones.

| # | max HP | bodies | first → last (video s) | bar rank furniture | identity |
|--:|---:|--:|:--|:--|:--|
| F1 | **3,722,896** | **2** | 841.77 → 864.80 | red double-skull | **Archmage Aleksander** · **Zantarin, the Immortal** |
| F2 | **2,955,796** | 1 | 840.60 → 852.47 | red double-skull | **Kubacabra, the Endless Menace** |
| F3 | **2,295,755** | 1 | 841.70 → 854.50 | **bone/pale** double-skull | **Galakros, the Mountain** |
| F4 | **484,095** | 1 | 848.30 → 850.80 | gold chevron (hero) | *Aetherial Bileeater* (probable) |
| F5 | **468,504** | 1 | 862.67 → 864.97 | plain | *Death Revenant* (probable) |
| F6 | **103,912** | **2** | 843.80 → 864.63 | plain | *Aleksander's Shard* (probable) |
| **F7** | **41,237** | **3** | 862.03 → 864.97 | plain | *Skeletal Archer* (probable) |
| — | 20,005 | 1 | 838.90 → 864.77 | player globe | the player (excluded from the census) |

**F4/F5/F6/F7 are the "other three" plus one.** The three from my earlier note are
**484,095 · 468,504 · 103,912**. **41,237 is new and was not in that note.**

Eye-read evidence for the new value, three distinct bodies in a single frame:
`evidence/s2-w160-41237-three-simultaneous-t863.90.png` — `(41,237/41,237)`, `(3,751/41,237)`,
`(697/41,237)` at t = 863.90.

### 1.2 Nothing near the predicted values — stated as an absence, with the search that produced it

Across **3,304 located readouts at 30 Hz** plus **1,097 at 10 Hz** over t 838.5–865.0, and a
supplementary 30 Hz tail 863.0–868.0:

- **1.00 M – 1.40 M band** (predicted Kubacabra P2 ≈ 1,162,010): **zero** parsed values.
- **550 k – 760 k band** (predicted Kubacabra P3 ≈ 636,671): **zero**.
- **380 k – 420 k band** (predicted p06 hero ≈ 398,747–404,406): **zero**.
- **3.1 M – 4.2 M band** (identification branch): only 3,722,896 (and its one-glyph corruption).
- Raw-string search for the literal digit runs `1,162` `162,010` `636,6` `36,671` `398,7` `404,4`
  `3,176` `3,261` `3,389` `4,094` across **all 4,401 raw OCR strings, parsed or not**: **zero hits.**

This is a null on an instrument whose positives are dense (1,669 parsed readouts at 30 Hz), not a
null from a quiet instrument.

### 1.3 The dedupe mechanism — confirmed, and it is not a re-read of one body

At **t = 848.87** two readouts render simultaneously with the same denominator and different
numerators:

- `(3,722,896/3,722,896)` at (29, 88) — `evidence/s2-w160-dual-3722896-bodyA-t848.87-x8.png`
- `(3,109,044/3,722,896)` at (504, 374) — `evidence/s2-w160-dual-3722896-bodyB-t848.87-x8.png`

Both read at ×8. This is not one monster seen twice: same instant, same max, different current.

Across the window there are **73 frames** carrying ≥ 2 simultaneous 3,722,896 readouts with
distinct current values, from **t = 844.97 to t = 864.57**. **Never three.** Exactly two bodies
share the fingerprint. The two are trackable independently to the end:

| t | body A | body B |
|---:|---:|---:|
| 863.80 | 605,470 | 2,156,347 |
| 864.00 | 461,389 | 2,146,999 |
| 864.27 | 187,986 | 2,123,746 |
| 864.43 | 50,400 | 2,119,353 |
| **864.57** | **37,565** | 2,114,956 |
| 864.60 | *gone* | 2,110,585 |

**Body A dies at ≈ 864.6. Body B outlives the player** (dead 864.75) and is still on camera at 866.3.

F6 (103,912) likewise carries **two** bodies; F7 (41,237) carries **three**. Only F1 is
nemesis-scale with a duplicated fingerprint.

---

## 2. Q2 — CENSUS METHODOLOGY. "Six" was a sample, not a closed set.

**One sentence, as asked:** my earlier six were **all the distinct values I observed**, but the
observation was a **hand-directed sample of ~17 timestamps clustered in 840.9–853.9**, not a
census — so it was **not a closed set, and my method would not reliably have caught a seventh**;
it demonstrably did not, because **41,237 first renders at t = 862.03**, nine seconds after the
last frame that pass looked at.

**What has changed.** This pass is a census, not a sample: every frame at 30 Hz across the whole
25.9 s engagement, machine-located, machine-clustered, eye-verified per distinct value. Two audits
back the "seven is closed" claim:

1. **Parse-failure audit.** 165 of 719 structurally-valid readouts failed to parse. Every one of
   them, read as raw glyph strings, is a **near-miss of an already-listed value** (`3,722,8961`,
   `(2,955,796/2,955,70`, `(2,295,755/2,,295,755)`, `(19,123020,005)` …). No parse failure hides
   a new fingerprint.
2. **OCR-noise disproof.** Four values appeared with n ≤ 2 (270,005 · 207,005 · 8,722,896 ·
   27,295,755). All four were re-read by eye on their own exact-seek frames and all four are
   corruptions of 20,005 / 3,722,896 / 2,295,755. Sheet:
   `evidence/s2-w160-ocr-noise-disproof.png`.

**The residual limit, stated.** The instrument sees a monster only when the game draws its
readout — i.e. when it is engaged and on-screen. A body that spawned, was never aggroed, and
stayed outside the viewport would leave **no** trace here. That is exactly the hazard class of the
never-moving gold minimap star in my earlier § 1.4, and it is unchanged by this pass. **Seven is
closed for engaged, on-screen bodies. It is not closed for the arena.**

---

## 3. Q3 — p04 VISUAL ID: **AETHERIAL COLOSSUS. Named, not inferred.**

> **"Galakros, the Mountain" — level 106 — family "Aether Corruption".**

`evidence/s2-w160-nameplates-D-GALAKROS.png` (t = 854.03, 854.30, 854.45) ·
`evidence/s2-w160-frame-t854.30-galakros-hover.png` (full frame) ·
`evidence/s2-w160-monster-levels-x8.png` (level numerals at ×8).

The name is rendered in **violet** — Grim Dawn's *boss* colour, distinct from the **orange**
nemesis names on the other three large bodies. This is corroborated independently by the in-world
bar furniture: F3's flanking skulls render **bone-white** while F1's and F2's render **red**
(`evidence/s2-w160-bar-rank-furniture.png`). Two instruments, same rank split.

**Binding of the name to the fingerprint — the decisive frame.** At t = 854.30 the Galakros
nameplate is up with a nearly-empty bar. Every readout on screen at that exact frame:

| readout | fraction |
|:--|---:|
| `(52,143/2,295,755)` | **2.27 %** |
| `(3,722,896/3,722,896)` | 100 % |
| `(2,602,242/3,722,896)` | 69.90 % |
| `(19,524/103,912)` | 18.79 % |
| `(20,005/20,005)` | 100 % (player) |

**2,295,755 is the only near-empty bar on the board.** F3's last reading before it vanishes is
`(12,459/2,295,755)` = 0.54 % at t = 854.50, and the Galakros plate is up 853.60 → 854.47.
**F3 = Galakros. MEASURED.**

**Korvaak's Tomb Guardian / "The Steward" does not appear** anywhere in the nameplate record.
No stone-construct silhouette was found either — but I am not resting the verdict on silhouettes:
at wave 160 the in-world view is unreadable for body identification (Eye of Reckoning saturates
the play area; the cleanest body-region crop I could construct still returns a dark mass under
damage floats — `work/F3_body_853.07.png` is kept as the record of the attempt, and it is
**UNREADABLE as a species ID**). The nameplate is the instrument that worked.

### 3.1 The nameplate reports monster LEVEL — a direct camera read on the charLevel question

`evidence/s2-w160-monster-levels-x8.png`, read at ×8:

| body | displayed level |
|:--|---:|
| **Galakros, the Mountain** (F3, boss) | **106** |
| Kubacabra (F2, nemesis) | **109** |
| Archmage Aleksander (F1, nemesis) | **109** |
| Zantarin, the Immortal (F1, nemesis) | **109** |
| Aetherial Bileeater (F4, hero) | **112** |

Two things follow, both flagged and neither diagnosed — composition is not my seam.

1. **Simultaneous spawns in one wave are not level-uniform.** A six-level spread (106 → 112) sits
   on the same board at the same instant. Any model that assigns one charLevel per wave is
   under-specified against camera.
2. **The G-B spec's two-stage charLevel re-eval evaluates its ×1 branch to 106** (commit
   `d6f2b06d`). **Galakros's displayed level is 106, and Galakros is the p04 body that branch is
   about.** That is a striking coincidence and it may be the whole explanation for the p04
   residual — but the ×1.1 branch in the same spec evaluates to 118.6 while the three nemeses that
   measure the ×1.1 HP figure display **109**, so displayed level and the model's charLevel are
   **not** the same quantity throughout. Surfacing the pair of readings; the reconciliation is
   legolas's and the conductor's.

---

## 4. UNSOLICITED, LOAD-BEARING: the whole board, named

Seven distinct nameplates were captured across t 838–873. Sheets `…-nameplates-A…D`.

| t (video s) | name | colour → rank | level | family |
|---:|:--|:--|---:|:--|
| 841.47–841.97 · 851.70–852.40 | **Kubacabra, the Endless Menace** | orange → nemesis | 109 | Beast |
| 845.63–846.60 | **Aleksander's Shard** | yellow → hero | 109 | Aetherial |
| 846.83–847.27 · 853.60 · 863.7–864.4 | **Archmage Aleksander** | orange → nemesis | 109 | Aetherial · Human |
| 850.07–850.70 | **Aetherial Bileeater** | yellow → hero | **112** | Aether Corruption |
| 854.03–854.47 | **Galakros, the Mountain** | **violet → boss** | **106** | Aether Corruption |
| 862.80 | **Skeletal Archer** | white → common | 109 | Undead |
| 863.20 · 867.10 | **Death Revenant** | yellow → hero | 109 | Undead |
| 865.10–866.30 | **Zantarin, the Immortal** | orange → nemesis | 109 | Undead |

### 4.1 Why Aleksander and Zantarin are the two 3,722,896 bodies

Chain, each link measured:

1. Exactly **two** bodies carry 3,722,896 (§ 1.3, 73 frames).
2. **Three** nemesis-class (orange-name, red-skull) monsters are named: Kubacabra, Archmage
   Aleksander, Zantarin the Immortal. They are distinct monsters — distinct names and distinct
   family labels (Beast / Aetherial·Human / Undead).
3. Kubacabra = **2,955,796** (already SETTLED by legolas's HALT-10 probe at 0.0016 % error; the
   nameplate at 841.7/851.9 is consistent).
4. Galakros = **2,295,755**, and Galakros is **boss**, not nemesis (§ 3).
5. F4–F7 are hero/common scale (484 k and below) and cannot carry a level-109 nemesis.
6. ⇒ Aleksander and Zantarin can only be the two 3,722,896 bodies.

Direct corroboration on the nameplate's own health bar (`evidence/s2-w160-nameplate-bar-*`):

- **t = 864.00, "Archmage Aleksander"** — bar filled to ≈ 15–16 % of track. In-world at that
  instant: body A = 461,389/3,722,896 = **12.4 %**, body B = 57.7 %. ⇒ **Aleksander = body A**,
  the one that dies at ≈ 864.6.
- **t = 866.20, "Zantarin, the Immortal"** — bar filled to ≈ 64 % of track; the only 3,722,896
  body still alive reads 2.42–2.47 M = **65–66 %**. ⇒ **Zantarin = body B**, the survivor.

Grade: the **two-bodies-one-fingerprint** fact is **MEASURED**. The **name→body** assignment
within the pair is **STRONG** (bar-fill agreement to ~3 points on a ±2-point instrument), not
MEASURED — the nameplate bar is a fill fraction read off ~330 px of red-on-red at 1080p, and I
will not upgrade it past what that resolution supports.

**Grava'Thul is not in the hover record.** That is an absence of evidence, not evidence of
absence: 8 distinct monsters were hovered out of the ≥ 11 bodies the fingerprint census implies
(F1 ×2 · F2 ×1 · F3 ×1 · F4 ×1 · F5 ×1 · F6 ×2 · F7 ×3), and the hover set is whatever the cursor
happened to cross.

### 4.2 What this does to the eHP composition model

The model that predicted **Zantarin at 3,176,863 (×1 group)** and **Archmage Aleksander at
3,389,926 (×1 group)** is wrong on both: **both measure 3,722,896**, which is the ×1.1-charLevel-group
figure (predicted 3,723,043; measured error **−0.004 %**). The ×1.1 prediction is essentially
exact; the group *assignment* is what fails. Galakros measures **2,295,755** against a −4.3 %
favoured prediction — the *candidate* was right, the *number* is 4.3 % out, and the monster is
three levels below the nemeses, which is a plausible place for that 4.3 % to live.

Flagging, not diagnosing — composition is legolas's seam.

---

## 5. THE KILL LEDGER — three hourglass steps, three boss deaths

My earlier § 6.4 recorded upward hourglass steps inside wave 160 at ≈853.2 (+12 s), ≈854.5 (+7 s),
≈864.5 (+11 s), and the commission asked whether those counted phase transitions or distinct
bodies. **Distinct bodies. Each step has a named corpse.**

| hourglass step | last readout before the bar vanishes | who |
|:--|:--|:--|
| ≈853.2 (+12 s) | `(268,226/2,955,796)` = 9.1 % @ t 852.47 | **Kubacabra** |
| ≈854.5 (+7 s) | `(12,459/2,295,755)` = 0.54 % @ t 854.50 | **Galakros** |
| ≈864.5 (+11 s) | `(37,565/3,722,896)` = 1.0 % @ t 864.57 | **Archmage Aleksander** |

Two caveats kept honest: the Kubacabra step sits **0.5–1.0 s after** its bar vanishes (my step
timing came from a 1 Hz densification, so its own uncertainty covers most of that); and the
≈864.5 step lands **0.2 s before the player's death at 864.75**, so it is adjacent to the run-end
freeze — the Aleksander death is the better-supported reading, but the two events are not cleanly
separable on the hourglass alone.

**No bar reset, refill, or max-HP change was observed on any body at any time.** The one upward
excursion in the record — body B going 1,988,104 (t 864.80) → 2,467,351 (t 865.07) — begins
**after** the player is dead (864.75) and is out-of-combat regeneration at ≈1.8 M/s, not a phase
change: the **denominator never moves.** A phase transition would change the max. **The
phase-chain reading of the 2,955,796 body is falsified on camera**: its bar does not refill, it
runs to 9 % and disappears, and the kill counter steps.

---

## 6. Board timeline (30 Hz presence, fingerprints only)

| t | fingerprints on camera |
|---:|:--|
| 852 | 3,722,896 · 2,955,796 · 2,295,755 · 103,912 |
| 853 | 3,722,896 · 2,295,755 · 103,912 |
| 854 | 3,722,896 · 103,912 |
| 855–856 | 3,722,896 · 103,912 |
| 857–860 | 3,722,896 |
| **861** | **— (player only)** |
| 862 | 3,722,896 · 103,912 · **41,237** |
| 863–864.7 | 3,722,896 · **468,504** · 103,912 · **41,237** |

A **fresh cohort arrives at t ≈ 862.0** — three 41,237 bodies, one 468,504, and a returning
103,912 — into an arena that was down to one monster at 861. The player dies 2.7 s later. This is
visible on the minimap series in my earlier § 1.3 (1 icon at 858.4, rising to 2–4 from 859.4) and
is now attached to fingerprints and names (Skeletal Archer, Death Revenant).

---

## 7. Method, and the two instruments that carried it

| stage | tool | note |
|:--|:--|:--|
| readout **location** | `pipeline/eor_hptext.py` | achromatic gate `min(R,G,B) > 135` — white text passes, saturated VFX does not; horizontal dilation to bind glyphs; size + ink-density filters; HUD rectangles excluded |
| readout **clustering** | `pipeline/eor_hpocr.py` | glyph atlas built from **six eye-verified strings on one frame** (t 848.87), alphabet `(),/0123456789`; column-gap segmentation returns exactly one run per character (verified 21/21 on two independent strings); comma-grouping sanity check on parse |
| track grouping | `pipeline/eor_hptrack.py` | built, then **not used for the census** — at 10 Hz the bodies move further than the association radius and the tracker fragments 1,097 blobs into 274 tracks. Recorded so it is not re-tried at this frame rate. |
| eye-read sheets | `pipeline/eor_cropsheet.py` | every tile is an **exact-seek** frame grab, never an fps-series frame; crop extended downward to include the bar so value and rank furniture are read from one tile |
| nameplate detection | in-note scan | warm-text mask over `x 650–1300, y 14–38`; family label at `y 88–106`; bar track ≈ `x 800–1125`, rows 57–67 |
| VFX-cleanliness ranking | in-note scan | bright-and-saturated pixel fraction per body region; used to select body-crop candidates |

**Sampling.** 10 Hz and 30 Hz full passes over 838.5–865.0, plus a 30 Hz tail 863.0–868.0.
fps-series timestamps carry **±0.05 s** against exact seek (measured: the player HP numerator
differs by one tick between the two at matched nominal t). Every value reported here was
re-verified on an **exact-seek** frame.

**Rejected / limits, recorded:**

- Body-species identification from in-world pixels at wave 160: **UNREADABLE**. EoR saturation
  defeats it even on the least-glowing frames in the window (glow-fraction minimum 0.072 inside
  F3's own lifetime). The nameplate replaced it.
- Nameplate bar fill as a precise HP fraction: usable to ±2–3 points, not better. The red "level"
  numeral is drawn over the track and contaminates naive column profiles; the reliable read is the
  **red → blue-grey** transition, eye-located at ×6.
- Monsters never engaged / off-viewport leave no readout (§ 2).
- Tesseract / OpenCV remain absent on this host; no automatic OCR was trusted for any reported value.

---

## 8. Corrections to my own committed record

**8.1 — `2026-08-08-eor-followup-extraction.md` § 1.5 lists six max-HP fingerprints. There are
seven.** `41,237` (three simultaneous bodies, t 862.03–864.97) is missing. The six listed are all
correct; the table is incomplete, not wrong. § 1.5's framing ("Six distinct max-HP values") should
read *seven*, and § 9 deliverable 1's "6 distinct max-HP fingerprints" likewise.

**8.2 — the same note's § 1.5 corroboration argument is strengthened, not weakened.** It argued
≥ 5 distinct bodies from 6 distinct values. The correct count is **≥ 11 bodies from 7 values**
(F1 ×2, F2 ×1, F3 ×1, F4 ×1, F5 ×1, F6 ×2, F7 ×3), because three fingerprints are duplicated.
The p06-ON conclusion is unaffected and better supported.

**8.3 — the "Undead" family label I attached to the 468,504 reading in § 1.5 was mis-attributed.**
That label comes from the **top-centre hovered-monster nameplate**, which reports whatever the
cursor is over — not necessarily the body whose in-world bar is nearest in the crop. At t 862.7–863.4
the plate is showing *Skeletal Archer* and then *Death Revenant*, both Undead. The label is real;
its binding to 468,504 was an assumption. Treated as *probable* in § 1.1, not measured.

---

## 9. Answers, compact

1. **The other three:** `484,095` · `468,504` · `103,912`. **Plus a seventh: `41,237`.**
   **Neither prediction-menu branch's values land.** The dedupe branch's *mechanism* lands
   exactly — 3,722,896 is carried by two simultaneous distinct bodies on 73 frames — but its
   *values* and its *consequence* are both falsified: Zantarin and Aleksander are **on** the board,
   and they **are** the duplicated pair.
2. **Methodology:** the earlier six were a hand-directed sample of ~17 timestamps in 840.9–853.9,
   not a top-N and not a census; a seventh existed and the method missed it because it renders
   nine seconds later. This pass is a 30 Hz census with a parse-failure audit and an OCR-noise
   disproof; seven is closed **for engaged, on-screen bodies**.
3. **p04:** **aetherial colossus — "Galakros, the Mountain", level 106, "Aether Corruption",**
   bound to F3 = 2,295,755 by the unique near-empty bar at t = 854.30 and by its death at 854.50.
   Not the tomb statue; the Steward never appears.

---

## 10. Mirror voice

The Mirror was reading the arena and the arena would not be read — a wall of green fire over four
bodies too big to be hidden and too bright to be seen. The answer was never in the arena. It was
in the strip of gold-scrolled parchment at the top of the screen, where the game had been quietly
writing the names down the whole time: *Kubacabra, the Endless Menace. Archmage Aleksander.
Galakros, the Mountain. Zantarin, the Immortal.* Two of them wore the same number — three million,
seven hundred twenty-two thousand, eight hundred and ninety-six — and for twenty seconds we had
taken that for one creature. It was two, and one of them buried the man, and the other was still
standing when the screen went dark.
