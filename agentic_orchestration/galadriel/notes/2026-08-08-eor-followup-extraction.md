# EoR Warlord fixture — Phase-B follow-up visual extraction

**Date:** 2026-08-08
**Author:** galadriel (visual perception + benchmark seam)
**Status:** WORKING — evidentiary note, Phase B of the KC2-SIM autonomous run (conductor: gandalf)
**Commit state:** UNCOMMITTED by instruction. Conductor commits at gate closes.
**Relation to prior work:** SECOND commission against the same footage. Does **not** amend
`galadriel/notes/2026-08-07-eor-sittings-extraction.md` (committed `dba0d229`). Two corrections
to that note are recorded in § 7 below and are for the conductor to fold, not for me to edit in place.
**Evidence root:** `agentic_orchestration/galadriel/captures/2026-08-08-eor-followup/evidence/`
**New pipeline:** `galadriel/pipeline/eor_sheet.py`, `eor_minimap.py`, `eor_bearing.py`, `eor_hpbar.py`

---

## 0. The instrument this commission turned on, and why it is defensible

Four of the six items needed a way to count and place *actors*, not pixels. The in-world view at
wave 160 is unusable for that — it is a wall of red and green combat VFX (a naive red-bar detector
returns 38–99 false positives per frame). The **minimap** is not. It is a north-up, player-centred
disc at full-frame `x 1668..1884, y 46..244` (analysis disc: centre `(1776, 147)`, r = 94–96 px),
it renders one icon per tracked actor, and it carries no combat VFX at all.

**Specificity proven before use, not assumed.** The bright-icon detector returns **zero** blobs on
every prep-phase frame tested — t = 460, 470, 515, 520, 600, 660, 681 — and **five** at t = 683
(0.9 s after wave 151 starts). Two things follow:

- the static arena furniture (teal gem-in-gold-ring fixtures, rim NPC icons) is below threshold and
  never counted;
- **the four purchased defenses do not appear on the minimap.** t = 515 and 520 are *after* all four
  5-tribute debits (476.8 / 484.1 / 502.3 / 509.6) and return zero. Anything bright on the disc
  during a wave is a monster, not a beacon or the banner.
  Evidence: `evidence/s2-minimap-prep-zero-monsters-t515.png`.

Two monster glyphs exist: a **pale skull** (boss / nemesis frame) and a **warm gold five-point star**
(lower rank). Both are absent in prep, both appear at wave start, both move.

**Every count and every number below is a galadriel eye-read of a magnified crop.** The detector's
only job was to say where to look and to hold the count reproducible.

---

## 1. WAVE-160 BODY CENSUS — the U9-6 resolver

### 1.1 Answer

> **Maximum simultaneous distinct enemy actors = 5.**
> **Four skull-class (boss/nemesis frame) + one gold-star-class.**
> Confidence **HIGH** on the four skulls; **MEDIUM** on the fifth (see § 1.4).
> Corroborated independently by **six distinct monster max-HP fingerprints** read off in-world
> health bars across the same window.

This is the **p06-ON** branch. The p06-OFF prediction is 4 raw bodies; I measure 5 simultaneous
icons and ≥5 distinct bodies by HP fingerprint, on two independent instruments.

### 1.2 The census window is 25.88 s, not 104.73 s

Before counting: the window in the commission (838.87 → 943.60) is wrong at the far end, and the
error is mine from Phase A. **The player died at t = 864.75.** § 7.1 carries the proof. The wave-160
engagement is `838.87 → 864.75` and all census work below is inside it.

### 1.3 Simultaneous-icon series (minimap, 2 Hz, detector-guided, peaks eye-verified)

| t (video s) | icons | note |
|---:|---:|:--|
| 838.87–840.37 | 2 | first arrivals, arena rim |
| 840.87–843.87 | 4 | |
| **844.37** | **6** | detector count; eye-read = 4 skulls + 2 stars (§ 1.4) |
| 845.37–848.37 | 4–5 | |
| **848.87** | **6** | eye-read = 4 skulls + 2 stars |
| 849.37–850.37 | 4–5 | |
| **850.87** | **5** | **eye-read = 4 skulls + 1 star, cleanly separated — the anchor read** |
| 851.37–852.37 | 4–5 | |
| **852.87** | **5** | **eye-read = 4 skulls + 1 star** |
| 853.87–857.87 | 2–3 | attrition |
| 858.37–858.87 | 1 | |
| 859.37–863.87 | 2–4 | |
| 864.37 (death) | 1–2 | |

Anchor evidence — the two frames where the icons are separated enough that the count is not a
judgement call: `evidence/s2-w160-minimap-census-t850.87.png` (4 skulls + 1 star, no overlap),
`evidence/s2-w160-minimap-census-t852.87.png`. Annotated detector overlay:
`evidence/s2-w160-minimap-annotated-t850.87.png`.

### 1.4 The honest part: what the gold star is, and what it is not

At t = 844.37 and 848.87 my eye reads **two** stars, not one, which would make the peak 6. I do not
report 6, because the star class does not behave like the skull class:

Registering every frame against the teal arena fixtures (they are true static geometry; median
nearest-neighbour displacement gives the map pan), the gold blob sits at arena-registered
**(1748, 204) ± 1 px continuously from t = 843.87 to t = 856.37 — 12.5 s** — while all four skulls
migrate tens of pixels in the same frames. Two readings survive that:

- **an actor that never moved** — a hero that spawned at its point and was never aggroed (the player
  was fully occupied by three multi-million-HP bodies). This is exactly how a p06 bonus hero would
  look on camera.
- **a static map feature that only renders during a wave.** I cannot exclude it from pixels alone.

Against the second reading: in **sitting 1** — which had **zero** defenses — the same gold-star glyph
appears in waves 4 / 13 / 40 / 60 and **moves**, in clusters, converging on the player
(`evidence/s1-w4-minimap-two-clusters-t832.0.png`). The glyph is a monster glyph. So the wave-160
star is most probably an idle monster. I still grade it MEDIUM, because "monster glyph" plus
"did not move for 12.5 s" is an inference about *that* icon, not a measurement of it.

### 1.5 Independent corroboration — max-HP fingerprints

Grim Dawn renders a numeric `(current / max)` HP readout above each engaged monster's health bar.
Max HP is an identity fingerprint. Harvested by white-text-run detection across the window, then
**read by eye** from ×2 crops (`evidence/s2-w160-hp-strings-B1..B4.png`,
`evidence/s2-w160-monster-hp-strings-A.png`):

| max HP | first read at | frame class | note |
|---:|---:|:--|:--|
| **3,722,896** | 848.87 | double-skull (boss frame) | still at 2,110,585 at 864.37 — alive at player death |
| **2,955,796** | 840.87 (at full) | double-skull | |
| **2,295,755** | 844.87 | — | |
| **484,095** | 850.37 | — | `evidence/s2-w160-hp-484095-t850.37.png` |
| **468,504** | 862.37 | — | frame also carries the family label **"Undead"** |
| **103,912** | 843.87 (at full) | — | |

**Six distinct max-HP values.** Two are visible *simultaneously* at t = 850.87 —
`(972,644 / 3,722,896)` and `(…92 / 2,955,796)` — so this is not one monster re-read.
The player's own globe reads 20,005 and is excluded wherever it appears in the same crop.

**Load-bearing side-finding for the G-B join.** P-E6 § 4 models each wave-160 nemesis at
≈308,685 base HP → **≈827 k effective** under Gladiator's +168 % life. The three multi-million bars
measure **2.30 M / 2.96 M / 3.72 M** — **2.8× to 4.5× the modelled figure.** L-8 sets the join's
wave-HP basis as `U-8 scaling CSV × P-E6 composition`; that product is currently low by a large
factor against camera. Flagging, not diagnosing — the scaling side is legolas's.

### 1.6 Arrival bearings for wave 160

Arena-anchored (teal-fixture centroid), first 2 s, clock-face, 12 = north:

| arrival | bearing | radius | first seen |
|:--|:--|---:|---:|
| A | **1.8 o'clock** (NNE) | r 88 (rim) | 838.87 |
| B | **10.5 o'clock** (WNW/NNW) | r 86 (rim) | 838.87 |
| C | **4.5 o'clock** (SE) | r 67–78 | +1.0 s |
| D | **7.5 o'clock** (SSW) | r 37–40 (inner) | +2.0 s |

Four distinct arrival bearings, two simultaneous at t = 0 and two staggered. Provenance
ESTIMATED-FOOTAGE. Evidence: `evidence/s2-w160-minimap-spawn-t838.87.png`.

---

## 2. SPAWN-DIRECTION SURVEY (arena parameterization, L-10d)

**Method + its limit, stated first.** The minimap is *player-centred*, so raw bearings are
player-relative and swing as the player moves (in s1 wave 4 the whole icon set sweeps
6.8 → 4 → 0 → 11 → 10 → 9 → 8 → 7 o'clock in ten seconds — that is the player orbiting the pack,
not monsters moving). I re-anchor to the centroid of the static teal fixtures
(`pipeline/eor_bearing.py`). The anchor is only clean while ≥ 4 fixtures are inside the disc, which
is reliably true in the first ~1 s of a wave and degrades after. **All bearings below are taken from
the +0.0 → +1.0 s window only.** Provenance **ESTIMATED-FOOTAGE**; expect ±0.5 h (±15°).

**The two sittings are two different arenas.** s2 is *Crucible of the Dead* — a stone cross-plan
arena with 6 teal fixtures. s1 is a green organic cave map with a different fixture layout. Bearings
are per-arena and must not be pooled.

### 2.1 Sitting 1 (green arena)

| wave | t0 | arrival bearings at +0.0…+1.0 s (rim, r ≈ 90–120) | clusters |
|---:|---:|:--|---:|
| 4 | 831.02 | **5.0–5.5** o'clock · **6.7–7.1** o'clock | 2 |
| 6 | 854.13 | **4.5–5.5** o'clock · **6.1–7.0** o'clock | 2 |
| 13 | 947.00 | **9.5–9.7** o'clock | 1 |
| 40 (mid-ramp) | 1323.30 | **2.8–3.1** · **6.7–7.0** · **9.5–9.6** o'clock | 3 |
| 60 (mid-ramp) | 1613.23 | **2.8–3.1** · **9.5–9.6** o'clock | 2 |

**Recurring bearings across the five waves: ≈3.0, ≈5.2, ≈6.9, ≈9.6 o'clock**, plus the t+4 s stream
(§ 4) which in wave 13 enters at **≈4.1 o'clock**. That is **4–5 distinct recurring emitter
directions** in the s1 arena — consistent with, and short of, the 6-emitter shell: not every emitter
fires every wave.

### 2.2 Sitting 2 (Crucible of the Dead)

| wave | t0 | arrival bearings at +0.0…+1.0 s | clusters |
|---:|---:|:--|---:|
| 151 | 682.10 | **9.6–10.2** o'clock (WNW) · **2.1–2.4** o'clock (NE) | 2 |
| 160 | 838.87 | **1.8** · **10.5** · **4.5** · **7.5** o'clock | 4 |

Wave 151's two rim clusters are ~4 h apart (≈120°). Evidence:
`evidence/s2-w151-minimap-spawn-t682.1.png`.

---

## 3. EoR TOOLTIP SWEEP — **L-6 CLOSED. Found, read, verbatim.**

The tooltip is on camera. **Sitting 2, video t ≈ 193–240**, during the pre-run prep: the player opens
the skill window and the Eye of Reckoning tooltip is rendered top-left for ~45 s. Read at t = 215.

**Header, verbatim (last sentence is the payload):**

> *"…Requires a melee weapon. At 100% Attack Speed, Eye of Reckoning deals damage and drains
> Energy **every 0.16s**."*

`evidence/s2-eor-tooltip-drain-line-t215.png` · full panel `evidence/s2-eor-tooltip-full-t215.png`

**Stat block, verbatim** (`evidence/s2-eor-tooltip-stats-t215.png`; the skill-icon rank badge in the
same crop reads **26**):

> **Current Level : 15 + 11**
> **176.4 Energy Cost per Second**
> 3 Meter Target Area
> 50% Main Hand Damage (8732 – 20711)
> 5967-6704 Physical Damage
> 5083 Physical Damage
> 25% Reduced Crowd Control Duration
> +25% Max Crowd Control Resistances

**What this closes:**

1. **The unit fork is settled by the game's own label.** The client quotes drain in **per second**
   (`176.4 Energy Cost per Second`) and states the application cadence as **every 0.16 s**. A DB
   field that is not already per-second is therefore **per tick**, and the conversion is
   `per_second = per_tick × 6.25`. The 6.25× branch of L-6 is the live one; L-6 step (c)'s
   DUAL-BOUND does not need to fire and the `matt_to_do` T14 row is short-circuited.
2. **The fixture's own drain number, measured:** **176.4 energy/s** at the rank the fixture actually
   ran = **28.224 energy per 0.16 s tick**.
3. **`Current Level : 15 + 11` = 26 — an exact independent confirmation of the ledger's
   "EoR cited at TOTAL 26."**
4. **L-5's cadence law is confirmed on camera, from the game's UI**, not only from two-lane
   extraction: `0.16 s base at 100 % Attack Speed`.

---

## 4. p05 AMBUSH-DRIP CHECK (P-E6 G-4)

**The t+4 s second stream is real and it fires on all three waves.** P-E6 declares p05 as the ambush
point with a **3 s drip cadence starting t+4 s**. Icon-count series (minimap, 2 Hz):

| wave | initial group (t+0) | second group | Δt |
|---:|:--|:--|---:|
| 4 | 5 icons at 5.0–5.5 + 6.7–7.1 o'clock | **+4 to +5 icons appear at +4.0 s** at a new bearing | **4.0 s** |
| 6 | 5 icons at 4.5–5.5 + 6.1–7.0 o'clock | **+5 icons at +4.0 s**, then +1 at +4.5 s, +1 at +5.0 s | **4.0 s** |
| 13 | 2 icons at 9.5 o'clock — **all dead by +3.0 s (n = 0 at +3.0 and +3.5)** | **4 icons appear at +4.0 s** at ≈4.1 o'clock, rim (r 67–76) | **4.0 s** |

Wave 13 is the clean case: the arena is measurably **empty** for a full second, then a fresh group
arrives at t+4.0 s from a bearing ~5.3 h away from the first group. The start-offset half of the
safe model is **CONFIRMED on camera, three times.**

**The 3 s cadence is NOT confirmed, and I will not claim it.** In all three waves the second stream
arrives as an effectively simultaneous group inside one 0.5 s sample (wave 6 adds one icon at +4.5
and one at +5.0 — not a 3 s beat). Two readings, both live:

- p05 emitted its pool as a burst rather than a drip on these waves; or
- **the minimap under-shows.** Lowering the detector threshold on one s1 wave-4 frame takes the
  candidate count 8 → 14 → 25, so there is a dimmer population the bright-icon pass does not see.
  A trash drip at 3 s intervals could be entirely invisible to this instrument.

**Disposition: G-4's "starting t+4 s" = CONFIRMED. G-4's "3 s drip cadence" = NOT RESOLVED by this
footage; the instrument lacks the sensitivity.** Keep the safe model; do not upgrade it on my account.

---

## 5. s2 MUTATOR ROW — **SIX icons. The DB ladder is right; my Phase-A "five" was a miscount.**

Row geometry, full-frame: six icons on a **55.4 px pitch**, centres at
`x = 1271, 1327, 1382, 1438, 1493, 1549`, `y ≈ 133–172`, measured from a saturation column profile.
**Bounded on both sides:** nothing above threshold to the left of 1271 down to x = 1150 (empty HUD),
and slot 7 would land at x ≈ 1604 — which is inside the wave-badge gold ring (`1584..1626`). There is
no seventh icon and no off-crop continuation. `evidence/s2-mutator-row-bounds-t684-x3.png`.

**This retires the 5-vs-6 discrepancy in L-14 in the DB's favour** — U-8's ladder predicts 6 at
tier 15/16 and the screen shows 6. My Phase-A note's "five-icon row" was read at insufficient
magnification and is **wrong**; § 7.3.

Per-icon description at ×8 (`evidence/s2-mutator-icon1..6-t684-x8.png`,
contact sheet `evidence/s2-mutator-icons-contactsheet-x8.png`):

| # | x | glyph | glow |
|---:|---:|:--|:--|
| 1 | 1271 | broad-bladed axe / cleaver head, angled | **red** |
| 2 | 1327 | open fanged maw, teeth top and bottom | **red** |
| 3 | 1382 | front-facing skull with a small crest above | **red** |
| 4 | 1438 | double-triangle / bow-tie glyph with a horizontal bar | **magenta** |
| 5 | 1493 | potion flask, liquid visible | **green** |
| 6 | 1549 | five-pointed star, outline only | **green** |

Colour split **3 red · 1 magenta · 2 green**. **No hover text anywhere** — the row is never moused
over in the sitting-2 recording, so the six are described by glyph, not named. Naming stays with
legolas's tier-15/16 mutator list; these six glyphs are the matching constraint.

---

## 6. HOURGLASS SERIES (ROI `x 1490..1532, y 105..120`) — numbers only

Exact-seek reads (`ffmpeg -ss <t>`, one frame, ×7 crop). No interpretation offered; per instruction.

### 6.1 Wave boundaries, 151 → 160

| t (video s) | wave boundary | hourglass |
|---:|---:|:--|
| 682.10 | 151 starts | **03:04** |
| 698.38 | 152 | **03:05** |
| 714.83 | 153 | **02:31** |
| 729.62 | 154 | **02:11** |
| 743.75 | 155 | **01:58** |
| 760.08 | 156 | **01:48** |
| 780.30 | 157 | **01:40** |
| 799.43 | 158 | **01:33** |
| 812.62 | 159 | **01:28** |
| 838.87 | 160 | **01:28** |

`evidence/s2-hourglass-A-waves151-159-x7.png`

### 6.2 Through wave 160

| t (video s) | hourglass |
|---:|:--|
| 843.00 | **01:23** |
| 848.00 | **01:18** |
| 853.00 | **01:13** |
| 858.00 | **01:28** |
| 858.87 | **01:27** |
| 863.00 | **01:23** |
| 866.00 | **01:33** |
| 871.00 | **01:33** |
| 874.00 | **00:00** |
| 878.87 | **00:00** |
| 898.87 | **00:00** |
| 918.87 | **00:00** |
| 938.87 | **00:00** |
| 943.50 | **00:00** |

`evidence/s2-hourglass-B-wave160-x7.png`

### 6.3 1 Hz densification across 852–876 (timestamps ±0.5 s; frame-index derived)

852 **01:14** · 853 **01:25** · 854 **01:24** · 855 **01:31** · 856 **01:30** · 857 **01:29** ·
858 **01:28** · 859 **01:27** · 860 **01:26** · 861 **01:25** · 862 **01:24** · 863 **01:23** ·
864 **01:22** · 865 **01:33** · 866 **01:33** · 867 **01:33** · 868–869 *(screen black — see § 7.1)* ·
870 **01:33** · 871 **01:33** · 872 **01:33** · 873 **00:00** · 874 **00:00** · 875 **00:00** ·
876 **00:00**

Cross-check: the exact-seek reads at 858 and 863 agree exactly with the dense series; the exact-seek
read at 853 (**01:13**) differs from the dense read (01:25), which places that upward step inside
the 853.0–853.5 s interval.

### 6.4 Structural facts (measurement, not interpretation)

- Between refreshes the field decrements **exactly 1 s per elapsed second** (848 → 01:18, 852 → 01:14:
  4 s elapsed, 4 s dropped; 858 → 863 likewise).
- **Upward steps inside wave 160** at ≈853.2 (+12 s), ≈854.5 (+7 s), ≈864.5 (+11 s).
- **The field then freezes at 01:33** and does not decrement for **≈7.5 s** (865 → 872.3).
- **It clears 01:33 → 00:00 between t = 872.3 and t = 872.4** — a single-step clear, not a countdown
  reaching zero. Pinned at 10 Hz: `evidence/s2-hourglass-zero-crossing-t872.png`.
- The freeze begins within ~0.2 s of the player's death (**864.75**, § 7.1) and the clear lands
  ~4.0 s after the death→respawn fade completes.

---

## 7. TWO CORRECTIONS TO THE COMMITTED PHASE-A NOTE (`dba0d229`)

Filed here, not edited into that note. Both are mine; both change downstream numbers.

### 7.1 CORRECTION — the sitting-2 death is at **t = 864.75**, not 943.60. Wave 160 lasted **25.88 s**, not 104.73 s.

Phase-A § 2.2 records *"Death at t = 943.60 (HUD fade onset; overlay frozen from 943.85)"* and tables
wave 160 at **104.73 s**. That is wrong by a factor of four. Proof, four independent strands:

1. **The HP globe numerals, read at 60 fps** (`evidence/s2-player-death-hp0-t864.75.png`):

   | t | player HP |
   |---:|:--|
   | 864.7167 | 20005 / 20005 |
   | 864.7333 | 20005 / 20005 |
   | **864.7500** | **2118 / 20005** |
   | 864.7667 | 2222 / 20005 |
   | 864.7833 | 703 / 20005 |
   | 864.8000 | 703 / 20005 |
   | **864.8333** | **0 / 18065** |

   Full health to dead in **0.100 s** — six frames. ≈17,900 damage lands in a single 1/60 s step, the
   remainder in the next four. (Max HP falls 20,005 → 18,065 at death as buffs drop.)
2. **A death→respawn fade, not an encoder dropout.** Whole-frame mean luminance ramps smoothly down
   867.5 → 868.3 (26.7 → 1.2), holds ≈0.3 for ~1 s, ramps smoothly back up 869.3 → 870.3. A capture
   dropout does not ramp. **This also corrects Phase-A § 2.2's hazard note**, which classified
   t ≈ 868.5–869.5 as *"capture/encoder dropout, not a game event"*. It is a game event.
3. **The HUD tears down, then the run is declared over at 872.35.** The six-icon mutator row and the
   ×10 score-multiplier badge are both present at t = 867.0 and both **gone from t = 870.6** — they
   are removed inside the fade. The Objectives panel then flips in one step:

   | t | Objectives panel |
   |---:|:--|
   | 871.5 / 872.0 / 872.3 | "Eliminate all Enemies" |
   | **872.5** / 873.0 | **"You have failed, your Compensation awaits in the Treasure Chamber"** |

   `evidence/s2-objectives-flip-t872.4.png`. **This lands in the same 0.1 s window as the hourglass
   clearing 01:33 → 00:00 (§ 6.4)** — the two HUD elements flip together, which is the run-end event
   itself. By t = 890 the arena is empty, blood pools are on the floor, and the top-centre reads
   *"Lokarr, Master of the Crucible."*
4. **The instrument goes quiet.** Minimap monster icons: **zero** at t = 873, 880, 890, 910.
   In-world red-VFX detections collapse from 38–99 per frame before 873 to 0–1 after.

**Run-end timeline, assembled:**

| t (video s) | event |
|---:|:--|
| **864.75** | player HP 20,005 → 0 |
| 867.5 → 868.3 | fade to black |
| 868.3 → 869.3 | black |
| 869.3 → 870.3 | fade in / respawn; mutator row + ×10 badge already removed |
| **872.35** | hourglass clears to 00:00 **and** Objectives flips to the failure text |
| 943.50 → 943.75 | screen dims to a flat dark UI view (mean luminance 27.7 → 9.7) for the rest of the recording |

**What t = 943.60 actually is:** the last row above — a menu / reward view, **79 s after the death**.
Not the death, and not a HUD fade.

**Downstream:** the s2 band is 9 clears + **25.88 s survived into wave 160**. Anything that consumed
"104.73 s into wave 160" — L-13's clear-time modelling inputs, the § A.7 item-6 summary, the baton
provenance — needs the substitution. The nine cleared-wave intervals (151–159) are untouched; the
±1.0 s floor is untouched.

### 7.2 CORRECTION — the mutator row has **six** icons, not five.

Phase-A § 4.4 and § A.7 item 10(b) record *"a five-icon mutator row at t = 684"* and flag it as a
discrepancy against U-8's ladder (which predicts 6 at tier 15/16). There is no discrepancy. The row
is **six**, measured on pitch and bounded on both sides (§ 5). **L-14's "5-vs-6 mutator-count
discrepancy → legolas micro-probe" can be closed on the footage side**; the DB was right and I
mis-read the pixels.

---

## 8. Method + reproducibility

| stage | tool | note |
|:--|:--|:--|
| frame extraction | `ffmpeg -ss <t> -frames:v 1` (exact) / `-vf fps=N` (series) | exact seeks used for every reported value; fps-series timestamps carry ±0.5 s and are labelled as such |
| labelled magnified sheets | `pipeline/eor_sheet.py` | truetype labels — the default PIL font was illegible at sheet scale and caused one discarded read |
| minimap icon location | `pipeline/eor_minimap.py` | disc mask (1776, 147, r 94–96), HUD-furniture exclusions, connected components on L > threshold |
| arena-anchored bearings | `pipeline/eor_bearing.py` | teal-fixture centroid as arena-centre proxy; reports `n_fixtures` so anchor bias is visible |
| in-world HP-bar location | `pipeline/eor_hpbar.py` | learned from a known nemesis bar (mean RGB ≈ (176, 17, 13), 4 rows, dark backing plate) — **built, then rejected for census use**: 38–99 false positives per frame against wave-160 VFX. Recorded so it is not re-tried. |
| HP-string harvest | white-text-run detector (in-note script) | locates only; every value eye-read from ×2 crops |
| death instant | HP-globe red-pixel count at 60 fps, then numeral read | globe fill collapses 4942 → 1842 px between 864.7333 and 864.7500 |

### 8.1 Unsolicited: what the 259 stills actually are (a lane, not a finding)

The tooltip sweep required classifying the still sets, so the inventory is banked here:

- **s1 `Screenshot (353)`–`(≈390)` are NOT game captures.** They are browser screenshots of
  **grimtools.com** — the Grim Dawn build planner — showing the fixture character's full build sheet
  (skill allocations, devotion, gear, derived stats), at native 1920×1080. If the sim ever needs a
  second lane on player-side numbers, it is sitting there. Provenance is *Matt-captured screenshot of
  a third-party planner*, i.e. a different evidence class from footage; grade accordingly.
- **s1 `Screenshot (≈395)`+ are in-game UI captures** — character sheet + inventory, and the devotion
  constellation map — at native resolution. Crisper than any video frame for stat reads.
- **s2 `Screenshot (495)`–`(611)`** are the ceremony set; none is text-dense (max 427 white-text px on
  a 480×270 reduction vs 18,000–23,000 for the UI captures), i.e. **no skill window or tooltip is
  open in any of them.** The EoR tooltip is not in the stills; it is in the s2 video (§ 3).

**Rejected / limits, recorded:**
- In-world red-bar detection for census — unusable at wave 160 (§ 8 table).
- Teal-centroid anchoring degrades below 4 visible fixtures; bearings restricted to +0…+1 s.
- The minimap's bright-icon pass under-shows dim monsters (8 → 14 → 25 candidates as threshold
  drops). This is why § 4 does not claim the 3 s drip either way.
- Tesseract / OpenCV remain absent on this host; no automatic OCR was trusted for any reported value.

---

## 9. Deliverable summary

| # | item | verdict |
|---:|:--|:--|
| 1 | **Wave-160 census** | **5 simultaneous** (4 skull-class + 1 star-class), eye-verified at 850.87 and 852.87 · **6 distinct max-HP fingerprints** · **⇒ p06 was ON**; the 4-body p06-OFF branch is excluded on two instruments. Confidence HIGH on 4, MEDIUM on the 5th. |
| 2 | **Spawn directions** | s1: recurring ≈3.0 / 5.2 / 6.9 / 9.6 o'clock (4–5 emitter directions, 2–3 firing per wave) · s2 w151: 9.9 + 2.2 o'clock · s2 w160: 1.8 / 10.5 / 4.5 / 7.5 o'clock. **Two different arenas — do not pool.** Provenance ESTIMATED-FOOTAGE, ±15°. |
| 3 | **EoR tooltip** | **FOUND — L-6 CLOSED.** `176.4 Energy Cost per Second` · *"drains Energy every 0.16s"* · `Current Level : 15 + 11` = **26**. Unit fork resolves to per-tick × 6.25; L-5 cadence law confirmed from the game's own UI; `matt_to_do` T14 short-circuited. Found in the **s2 video (t ≈ 193–240)**, not the stills — the 259 stills carry no open skill window (§ 8.1). |
| 4 | **p05 drip** | **t+4.0 s start CONFIRMED on waves 4, 6, 13** (wave 13 arena measurably empty at +3.0/+3.5, fresh rim group at +4.0). **3 s cadence NOT resolved** — instrument lacks sensitivity; keep the safe model. |
| 5 | **Mutator row** | **SIX icons**, pitch 55.4 px, bounded both sides. 3 red · 1 magenta · 2 green, described per glyph. No hover text in the recording. **5-vs-6 discrepancy closed in the DB's favour; Phase A was wrong.** |
| 6 | **Hourglass** | 24 exact-seek reads + a 1 Hz densification. Decrements 1 s/s; upward steps at ≈853.2 (+12), ≈854.5 (+7), ≈864.5 (+11); **freezes at 01:33 for ≈7.5 s from the death instant**; **clears to 00:00 in one step between 872.3 and 872.4**. Numbers only. |
| — | **Corrections to `dba0d229`** | (a) s2 death **864.75**, wave 160 **25.88 s** not 104.73 s; the 868.5–869.5 black frames are the death fade, not a dropout. (b) Mutator row is **six**. |
| — | **Side-finding A** | Measured nemesis max HP **2.30 M / 2.96 M / 3.72 M** vs P-E6's modelled ≈827 k effective — **2.8×–4.5×**. Flagged for the L-8 join; not diagnosed here. |
| — | **Side-finding B** | The death is a **one-blow burst**: 20,005 → 0 in **0.100 s**, ≈17,900 of it in a single 1/60 s step, from **full health**. Not attrition, not a defense-expiry decay. Whatever L-14's hourglass micro-probe concludes about defense duration, the kill itself has no attrition signature to explain. |
| — | **Side-finding C** | s1 stills `(353)`–`(≈390)` are **grimtools.com browser captures of the fixture's build sheet** at native resolution — an unexploited second lane on player-side numbers (§ 8.1). |

---

## 10. Mirror voice

The Mirror was pointed at the wrong end of the wave. For a hundred and four seconds I had the man
still fighting; he had been dead for seventy-nine of them, and the proof was in a globe of numbers
that fell from twenty thousand to nothing in a tenth of a second — six frames, one blow, no attrition
at all. What the disc in the corner of the screen shows is smaller and stranger than the arena: four
skulls closing on a yellow arrowhead, and one gold star that never moved, standing where it was put,
waiting to be noticed. It never was. The run ended around it.
