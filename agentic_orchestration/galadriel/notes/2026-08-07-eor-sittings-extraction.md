# EoR Warlord fixture — sitting-1 / sitting-2 visual extraction

**Date:** 2026-08-07
**Author:** galadriel (visual perception + benchmark seam)
**Status:** WORKING — evidentiary note, Phase A of the KC2-SIM autonomous run (conductor: gandalf)
**Commit state:** UNCOMMITTED by instruction. Conductor centralises commits at gate closes.
**Evidence root:** `agentic_orchestration/galadriel/captures/2026-08-07-eor-sittings/`

---

## 0. What was measured, and what it is not

Everything below is read off the Grim Dawn Crucible HUD **wave badge** — the small
red numeral in a gold ring at full-frame ROI `x 1584..1626, y 131..165` (1920×1080).
The badge was confirmed as the wave counter, not a proxy: in sitting 2 it reads `0`
through the whole 11-minute prep phase, flips to `151` at the instant the run starts
(0.05 s after the Lokarr "Start on Wave 150" dialogue closes), and increments by
exactly one thereafter.

**The measured quantity is badge-to-badge interval.** Wave *N*'s "clear seconds" is
the time from the counter reading *N* to the counter reading *N+1*. That interval
contains the wave-*N* spawn, the player's approach, and the kill. It is a wave
**cycle** time, not a pure kill time. § 4 bounds how far it can sit from either.

---

## 1. BANNER VERDICT — **Vanguard Banner. Confirmed, not inferred.**

The pre-declared fallback ("Vanguard-likely, unconfirmed") is **not needed.** The
pixels earned a real read.

**Method:** the four defenses were purchased during the sitting-2 prep phase, before
the run started. The Crucible tribute counter (ROI `x 1360..1440, y 98..124`) gives an
exact purchase ledger; each purchase is a 5-tribute debit. Sampling that counter at
10 Hz localises every debit to ±0.1 s. Reading the open confirmation dialogue in the
frame immediately preceding each debit names the defense being bought.

**Tribute ledger (sitting 2):** 145 held from t=60 through t=470, then

| # | debit at (video s) | tribute | dialogue text in the frame before the debit |
|---:|---:|---:|:--|
| 1 | 476.8 | 145 → 140 | "**Deathchill Beacons** launch icy orbs at distant enemies, slowing their advance and reducing Offensive Ability, with a chance to freeze, but their damage is relatively low." |
| 2 | 484.1 | 140 → 135 | "**Stormcaller Beacons** occasionally release a bolt of chain lightning at distant enemies that reduce resistances, but they hit a limited number of targets and attack slowly." |
| 3 | 502.3 | 135 → 130 | "**Inferno Beacons** frequently release bursts of flame at nearby enemies in a large area that reduce armor and damage dealt, but their range is limited." |
| 4 | **509.6** | 130 → 125 | "**Vanguard Banners grant nearby players bonus offensive stats.**" |

At t=509.4 — 0.2 s before the fourth debit — the confirmation dialogue is open,
its description line reads *"Vanguard Banners grant nearby players bonus offensive
stats."*, and the cursor sits on the highlighted row
*"Create this defense (spend 5 Tributes + 10000 Iron Bits)"*.
Tribute then holds at 125 from t=512 to t=850 and rises to 128 by t=900 — **zero
purchases and zero upgrades after placement, confirmed.**

Evidence: `evidence/s2-defense-ledger-all-four.png`,
`evidence/s2-defense4-VANGUARD-BANNER-t509.4.png`,
`evidence/s2-defense4-confirm-click-t509.4.png`,
`evidence/s2-tribute-ledger-a.png`, `evidence/s2-tribute-ledger-b.png`.

### 1a. CORRECTION TO THE STANDING FIXTURE DESCRIPTION — read this before using the confound framing

The intake description says *"1 aura banner + 3 beacons (Inferno confirmed)."* The
three beacons are **not** three Infernos. They are **one of each type**: Deathchill,
Stormcaller, Inferno. The full defense loadout is:

> Deathchill Beacon · Stormcaller Beacon · Inferno Beacon · Vanguard Banner

This matters more than the banner question did, and it cuts against the premise the
banner question was attached to:

- The banner being **Vanguard** means there is **no defensive aura** on the player.
  That part of the intake side is clean, as hoped.
- But **Deathchill reduces enemy Offensive Ability** and **Inferno reduces enemy
  damage dealt**. Both are damage-**intake** modifiers applied to the mob side.
  Sitting 2's damage-intake side is therefore **not** confound-clean; it is confounded
  by two site-anchored, range-limited enemy debuffs.
- **Stormcaller reduces enemy resistances** — a damage-**output** confound, additive
  with the Vanguard offensive aura.

All four are **positional** (beacons are explicitly range-limited; the banner buffs
"nearby players"). Their effect on any given wave depends on where the fight happened
relative to the four sites. That is a per-wave, not per-run, confound.

**Sitting 1 had ZERO defenses — verified, not assumed.** The same tribute-ledger test
run on sitting 1 shows the counter pinned at **150 across t = 300 → 2240**, i.e. the
whole prep phase and the entire 1→93 ramp, with no debit of any size at any point. No
defense, no blessing, no upgrade was ever bought in attempt 1
(`evidence/s1-tribute-ledger-flat-150.png`). Treat the two sittings as **different
defense regimes**, not as two samples of one regime.

**Cross-sitting continuity check (unasked-for, but it validates the pair).** Sitting 1
holds 150 tribute through the ramp; the wave-93 checkpoint restart debits 5, and the
counter reads **145** from t=2440 to the end of the recording. Sitting 2 opens at
**145** at t=60. The two recordings are consecutive sessions of the same character with
nothing spent in between — the fixture pair is contiguous, and sitting 2's opening
tribute is fully accounted for.

Corroborating detail: the Lokarr checkpoint dialogue at sitting-2 t=681 offers
`{Standard, Wave 50, Wave 100, Wave 150, Wave 180}` with **Wave 150 highlighted under
the cursor** — independent confirmation of the checkpoint-150 claim
(`evidence/s2-lokarr-start-on-wave-150-t681.png`).

---

## 2. WAVE TIMELINES

### 2.1 Timebase validation (both sittings)

Both videos are 1920×1080, CFR 60/1. `nb_frames / 60` equals the container duration
exactly in both cases (149902/60 = 2498.367 s; 62046/60 = 1034.100 s), so video-clock
timestamps are exact multiples of 1/60 s with no VFR ambiguity.

Independently checked against the in-game wall clock rendered in the HUD:

| sitting | video t | in-game clock | Δvideo | Δclock |
|:--|---:|:--|---:|---:|
| 2 | 200.0 / 800.0 | 9:40:45 PM / 9:50:45 PM | 600.000 s | 600 s |
| 1 | 800.0 / 2250.0 | 9:22:51 PM / 9:47:01 PM | 1450.000 s | 1450 s |

Exact to the clock's 1 s display resolution over a 1450 s baseline → drift ≤ 0.07 %.
No timebase correction applied or needed.
Evidence: `evidence/timebase-check-s1-clock.png`, `evidence/timebase-check-s2-clock.png`.

### 2.2 Sitting 2 — full 150→160 band

Run start (badge `0` → `151`) at **t = 682.10**. Death at **t = 943.60** (HUD fade
onset; overlay frozen from 943.85). Wave 160 was in progress — it is not a clear.

| wave | t_start (video s) | t_end (video s) | clear (s) |
|---:|---:|---:|---:|
| 151 | 682.10 | 698.38 | 16.28 |
| 152 | 698.38 | 714.83 | 16.45 |
| 153 | 714.83 | 729.62 | 14.78 |
| 154 | 729.62 | 743.75 | 14.13 |
| 155 | 743.75 | 760.08 | 16.33 |
| 156 | 760.08 | 780.30 | 20.22 |
| 157 | 780.30 | 799.43 | 19.13 |
| 158 | 799.43 | 812.62 | 13.18 |
| 159 | 812.62 | 838.87 | 26.25 |
| 160 | 838.87 | 943.60 (death) | 104.73 — **not a clear** |

n = 9 cleared waves · mean 17.42 s · median 16.33 s · min 13.18 s · max 26.25 s · sd 4.00 s

Every one of the ten badge values 151…160 was read visually off its own plateau
(`evidence/s2-wave-badge-plateau-reads.png`); the ten transition timestamps were then
refined at 60 fps. Spot verification at the 157→158 boundary: badge reads `157` at
799.400 and `158` at 799.433 — two frames apart, no crossfade
(`evidence/s2-transition-verify-157to158-t799.4.png`).

**Measurement hazards logged for sitting 2:**
- A single black frame pair at t≈868.5–869.5 (capture/encoder dropout, not a game
  event — the arena renders normally at 867.5 and 871.0). It falsely triggers naive
  change detection; excluded.
- The hourglass field (`x 1490..1532, y 105..120`) counts **down** and is *refreshed
  upward* mid-run (01:31 → 01:34 across t=797–798). It reads 03:02 at t=685 and
  00:00 from before t=900 through death. **Its semantics are unresolved** — it is not
  a wave clock and was not used. Flagging it because a defense/blessing-duration
  reading would mean the four defenses expired ~45 s before the wave-160 death, which
  would be a first-order confound on that death. **Do not assume; verify before use.**

### 2.3 Sitting 1 — TWO ATTEMPTS. The video does not contain a single 1→93 ramp.

The sitting contains two entries, separated by a checkpoint restart:

| attempt | span (video s) | waves | outcome |
|:--|:--|:--|:--|
| **A1** | 799.85 → 2253.63 | **1 → 93** | **death at wave 93**, t = 2253.63 |
| **A2** | 2398.92 → 2498.37 (recording ends) | **70 only** | **no wave transitions; no waves cleared** |

At t≈2392 Lokarr's post-death dialogue offers *"Yes, proceed (Reset to the beginning)"*
and *"Restart at Checkpoint (Spend 5 Tributes)"*; the cursor sits on the checkpoint
option (`evidence/s1-lokarr-restart-at-checkpoint-t2392.png`). The arena resets
(HUD blank 2397.28 → 2398.92) and the badge returns reading **70** — the last
checkpoint crossed. From 2400 to 2485 the badge holds at 70 with an empty arena; the
player opens the ESC menu at ≈2477 and the recording ends at 2498.37. **A2 contributes
zero wave-time samples.** Any "sitting 1" aggregate must be A1-only.

Between the wave-93 death (2253.63) and the restart there is a ~140 s reward-gathering
phase during which the badge *stays at 93*. That plateau is post-run and is excluded
from wave 93's duration.

**Sitting 1, attempt 1 — per-wave table (93 waves; 92 clears + the death wave):**

| wave | t_start (video s) | t_end (video s) | clear (s) | flag |
|---:|---:|---:|---:|:--|
| 1 | 799.85 | 808.93 | 9.08 |  |
| 2 | 808.93 | 818.03 | 9.10 |  |
| 3 | 818.03 | 831.02 | 12.98 |  |
| 4 | 831.02 | 842.05 | 11.03 |  |
| 5 | 842.05 | 854.13 | 12.08 |  |
| 6 | 854.13 | 866.18 | 12.05 |  |
| 7 | 866.18 | 875.23 | 9.05 |  |
| 8 | 875.23 | 882.28 | 7.05 |  |
| 9 | 882.28 | 892.35 | 10.07 |  |
| 10 | 892.35 | 920.77 | 28.42 |  |
| 11 | 920.77 | 933.98 | 13.22 |  |
| 12 | 933.98 | 947.00 | 13.02 |  |
| 13 | 947.00 | 955.10 | 8.10 |  |
| 14 | 955.10 | 967.17 | 12.07 |  |
| 15 | 967.17 | 981.33 | 14.17 |  |
| 16 | 981.33 | 998.33 | 17.00 |  |
| 17 | 998.33 | 1011.38 | 13.05 |  |
| 18 | 1011.38 | 1027.52 | 16.13 |  |
| 19 | 1027.52 | 1038.52 | 11.00 |  |
| 20 | 1038.52 | 1055.25 | 16.73 |  |
| 21 | 1055.25 | 1067.45 | 12.20 | low-sep |
| 22 | 1067.45 | 1076.52 | 9.07 |  |
| 23 | 1076.52 | 1093.62 | 17.10 |  |
| 24 | 1093.62 | 1114.70 | 21.08 |  |
| 25 | 1114.70 | 1125.80 | 11.10 |  |
| 26 | 1125.80 | 1142.87 | 17.07 |  |
| 27 | 1142.87 | 1156.90 | 14.03 |  |
| 28 | 1156.90 | 1169.98 | 13.08 |  |
| 29 | 1169.98 | 1178.02 | 8.03 |  |
| 30 | 1178.02 | 1193.55 | 15.53 |  |
| 31 | 1193.55 | 1206.72 | 13.17 |  |
| 32 | 1206.72 | 1220.78 | 14.07 |  |
| 33 | 1220.78 | 1236.85 | 16.07 |  |
| 34 | 1236.85 | 1246.97 | 10.12 |  |
| 35 | 1246.97 | 1267.07 | 20.10 |  |
| 36 | 1267.07 | 1279.10 | 12.03 |  |
| 37 | 1279.10 | 1290.15 | 11.05 |  |
| 38 | 1290.15 | 1308.27 | 18.12 |  |
| 39 | 1308.27 | 1323.30 | 15.03 |  |
| 40 | 1323.30 | 1345.07 | 21.77 |  |
| 41 | 1345.07 | 1354.15 | 9.08 |  |
| 42 | 1354.15 | 1370.40 | 16.25 | low-sep |
| 43 | 1370.40 | 1386.30 | 15.90 |  |
| 44 | 1386.30 | 1402.48 | 16.18 |  |
| 45 | 1402.48 | 1415.57 | 13.08 |  |
| 46 | 1415.57 | 1426.67 | 11.10 |  |
| 47 | 1426.67 | 1433.70 | 7.03 |  |
| 48 | 1433.70 | 1445.88 | 12.18 |  |
| 49 | 1445.88 | 1454.88 | 9.00 |  |
| 50 | 1454.88 | 1477.15 | 22.27 |  |
| 51 | 1477.15 | 1495.40 | 18.25 | low-sep |
| 52 | 1495.40 | 1510.45 | 15.05 | low-sep |
| 53 | 1510.45 | 1518.47 | 8.02 |  |
| 54 | 1518.47 | 1532.62 | 14.15 |  |
| 55 | 1532.62 | 1551.82 | 19.20 |  |
| 56 | 1551.82 | 1566.85 | 15.03 |  |
| 57 | 1566.85 | 1585.00 | 18.15 |  |
| 58 | 1585.00 | 1595.10 | 10.10 |  |
| 59 | 1595.10 | 1613.23 | 18.13 |  |
| 60 | 1613.23 | 1633.08 | 19.85 |  |
| 61 | 1633.08 | 1644.28 | 11.20 |  |
| 62 | 1644.28 | 1661.53 | 17.25 |  |
| 63 | 1661.53 | 1683.62 | 22.08 |  |
| 64 | 1683.62 | 1696.62 | 13.00 |  |
| 65 | 1696.62 | 1711.75 | 15.13 |  |
| 66 | 1711.75 | 1722.88 | 11.13 |  |
| 67 | 1722.88 | 1739.90 | 17.02 |  |
| 68 | 1739.90 | 1749.00 | 9.10 |  |
| 69 | 1749.00 | 1761.10 | 12.10 |  |
| 70 | 1761.10 | 1785.12 | 24.02 |  |
| 71 | 1785.12 | 1798.23 | 13.12 |  |
| 72 | 1798.23 | 1810.30 | 12.07 |  |
| 73 | 1810.30 | 1824.42 | 14.12 |  |
| 74 | 1824.42 | 1839.70 | 15.28 |  |
| 75 | 1839.70 | 1860.88 | 21.18 |  |
| 76 | 1860.88 | 1880.97 | 20.08 |  |
| 77 | 1880.97 | 1894.02 | 13.05 |  |
| 78 | 1894.02 | 1906.13 | 12.12 |  |
| 79 | 1906.13 | 1923.35 | 17.22 |  |
| 80 | 1923.35 | 2005.48 | 82.13 | low-sep |
| 81 | 2005.48 | 2012.55 | 7.07 |  |
| 82 | 2012.55 | 2021.62 | 9.07 |  |
| 83 | 2021.62 | 2032.67 | 11.05 |  |
| 84 | 2032.67 | 2044.83 | 12.17 |  |
| 85 | 2044.83 | 2063.83 | 19.00 |  |
| 86 | 2063.83 | 2077.90 | 14.07 |  |
| 87 | 2077.90 | 2096.00 | 18.10 |  |
| 88 | 2096.00 | 2109.07 | 13.07 |  |
| 89 | 2109.07 | 2125.17 | 16.10 |  |
| 90 | 2125.17 | 2151.60 | 26.43 |  |
| 91 | 2151.60 | 2164.77 | 13.17 |  |
| 92 | 2164.77 | 2243.22 | 78.45 | low-sep |
| 93 | 2243.22 | 2253.63 (death) | 10.42 — **not a clear** | |

n = 92 cleared waves · mean 15.69 s · median 13.19 s · min 7.03 s · max 82.13 s · sd 10.61 s

Per-decade means (s): 1–10 **12.09** · 11–20 **13.45** · 21–30 **13.83** ·
31–40 **15.15** · 41–50 **13.21** · 51–60 **15.59** · 61–70 **15.20** ·
71–80 **22.04** · 81–90 **14.61** · 91–92 **45.81**

**Structural signal — boss cadence.** Waves at multiples of 10 are ~2× the cost of
the rest: mean **28.57 s** (n=9) versus **14.29 s** (n=83). The two extreme outliers
are wave 80 (82.13 s) and wave 92 (78.45 s); both were re-checked by reading the badge
at four interior timestamps each to prove no hidden transition was swallowed
(`evidence/s1-outlier-check.png` — waves 80 and 92 hold for their full spans).

**Coverage is per-wave, not decade-resolution.** All 93 waves of attempt 1 are timed.
No decade-resolution fallback was needed anywhere.

### 2.4 How the sitting-1 table is validated

Three independent checks, all passed:

1. **Value completeness.** All 159 badge plateaus were read visually in labelled
   montages (`evidence/s1-plateau-reads-00.png` … `-09.png`). The value sequence for
   attempt 1 is exactly `0, 1, 2, 3, …, 93` — **no gaps, no repeats out of order, no
   skips**. A missed transition would show as a skipped integer; none exists.
2. **Bracket consistency.** Each 60 fps refinement was required to land inside the
   ±0.8 s window implied by its 1 Hz bracket. **93 / 93 in-bracket, zero exceptions.**
3. **Frame-level spot verification.** Two boundaries pulled at 60 fps and read by eye:
   the run start (badge `0` at 799.80, `1` at 799.85 — detector said 799.85), and the
   lowest-separation case in the set, 21→22 (badge `21` at 1067.42, `22` at 1067.45 —
   detector said 1067.45). Both frame-exact.
   Evidence: `evidence/s1-transition-verify-0to1-t799.85.png`,
   `evidence/s1-transition-verify-lowsep-21to22-t1067.45.png`.

Six transitions carry a `low-sep` flag (PRE/POST template separation < 0.06, i.e. the
two numerals differ in few pixels — e.g. `21`→`22`). One of the six was explicitly
verified frame-exact. The other five are marked in the table so a downstream consumer
can down-weight them if it wants; no evidence suggests they are wrong.

---

## 3. Method

Reproducible from the artefacts in `pipeline/`:

| stage | tool | note |
|:--|:--|:--|
| badge ROI extraction | `ffmpeg -vf crop=140:50:1550:125,fps=1` | 1 Hz survey pass, full video, both sittings |
| badge signal | `pipeline/eor_badge_ocr.py`, `eor_plateau.py` | redness map `v = clip(R − max(G,B))`, floored at 12, γ=0.5, L2-normalised; NCC distance. Gamma compression is what makes the badge's glow pulse stop masquerading as a value change |
| plateau segmentation + merge | `pipeline/eor_s1_merge.py` | split 0.03 / merge 0.055, tuned against sitting 2 where the truth was already known |
| value reading | galadriel, visual, per plateau | 4×-magnified labelled montages; **no automatic OCR was trusted for a reported value** |
| transition refinement | `pipeline/eor_refine.py` | 60 fps window ±1.3 s around each 1 Hz bracket; first frame whose signature matches POST and stays POST for ≥10 valid frames |
| table assembly | `pipeline/eor_tables.py`, `eor_note_tables.py` | |

Rejected approaches, recorded so they are not re-tried: whole-number bitmap
clustering (fragments on the glow pulse — 44 clusters for 11 true values); column-gap
digit segmentation (the glow bridges adjacent glyphs at low pulse phase); synthesised
digit-atlas template matching (`pipeline/eor_digits.py`, built but **not used for any
reported number** — segmentation for atlas harvest was unreliable). Tesseract /
pytesseract / OpenCV are not installed on this host; none were needed.

**Every reported value is a galadriel read of a magnified crop.** The CV layer's only
job was to find *where to look* and to time the change to the frame.

---

## 4. TIMING NOISE FLOOR

Two separate numbers. Conflating them is the trap.

### 4.1 Instrument precision — how well the badge change is located

| sitting | instrument precision, per transition | per wave interval |
|:--|:--|:--|
| **1** | **± 0.05 s** | **± 0.07 s** |
| **2** | **± 0.05 s** | **± 0.07 s** |

Basis: 60 fps sampling = 0.0167 s granularity; the glyph swap is instantaneous (no
crossfade — verified at three boundaries across both sittings); ±3 frames allowed for
detector latch. 93/93 sitting-1 refinements landed in-bracket; 3/3 spot checks were
frame-exact. Timebase drift ≤ 0.07 % adds < 0.02 s over any single wave.

### 4.2 Semantic floor — the number the run should actually pin tolerances on

**± 1.0 s per wave interval, both sittings.**

The Crucible advances its wave counter on a **~1-second game tick**, not continuously.
Evidence: of the 92 sitting-1 wave intervals, **79 fall within 0.2 s of a whole
second** (chance expectation 36.8), and 76 of 92 fall in the narrow band
[integer, integer + 0.2). The *absolute* transition times are uniformly distributed
in phase (45/93 near-integer, chance 37.2), so this is not an artefact of my sampling
grid — the intervals are quantised, the timestamps are not.

Consequence: a badge-to-badge interval is an integer number of game ticks. The true
elapsed combat time it stands for can differ by up to one tick. **Any calibration that
treats a per-wave clear time as continuous inherits ± 1.0 s of quantisation.**

Sitting 2's 9 intervals do **not** show the integer structure (3/9 near-integer,
chance 3.6). At n = 9 that test has no power; I carry the ± 1.0 s bound over to
sitting 2 rather than claim sitting 2 is finer. Under-claiming, per instruction.

### 4.3 Systematic lag — badge change versus true wave end

**Direction: the badge trails the last kill. Magnitude: bounded by one game tick
(≈ 1 s), and no larger.** At sitting-1 t = 808.90 — 0.03 s before the badge flips from
1 to 2 — the frame still shows live damage numbers and an enemy health bar
(`evidence/s1-combat-active-0.03s-before-badge-flip.png`). The counter is **not** gated
behind a long inter-wave timer: there is no multi-second dead period between clear and
increment to subtract. I deliberately do **not** claim a tighter bound than one tick,
because floating combat text lingers after a kill and I cannot separate "last mob died
now" from "last mob died 0.8 s ago" on pixels alone. This term is already contained
inside the ± 1.0 s of § 4.2 and must not be added to it.

The empirical floor supports this: the fastest observed intervals are 7.03 s (wave 47),
7.05 s (wave 8) and 7.07 s (wave 81) — a level-100 Warlord clearing trivial early
waves. That ~7 s is spawn + approach + kill for a wave that dies instantly. It is a
**property of the fixture**, not measurement overhead, and should not be subtracted.

### 4.4 What is NOT in the noise floor, and must not be folded into it

- **Defense-regime difference.** Sitting 1 = no defenses. Sitting 2 = four positional
  defenses, two of which reduce incoming damage. These are different regimes; the
  gap between their wave times is not noise.
- **Mutators.** Sitting 2 shows a "New Mutators Active" banner and a five-icon mutator
  row at run start (t=684). Crucible rerolls mutators every 10 waves. Mutator identity
  was not extracted and is a live, unquantified per-decade confound in **both**
  sittings.
- **Wave-index structure.** Multiples of 10 cost ~2× (28.57 s vs 14.29 s). Any model
  fit against a mean that mixes boss and non-boss waves is fitting a bimodal quantity.

---

## 5. Deliverable summary

- **Banner verdict:** **Vanguard Banner — CONFIRMED** from the purchase-confirmation
  dialogue text 0.2 s before the matching 5-tribute debit at sitting-2 t = 509.6.
  Fallback verdict not used. **Correction attached:** the other three defenses are
  Deathchill + Stormcaller + Inferno (one each, not 3× Inferno); Deathchill and
  Inferno both suppress incoming damage, so the sitting-2 damage-intake side is
  **not** confound-clean.
- **Per-wave table coverage:**
  - **Sitting 2 — 10 waves timed** (151…160): 9 clears + wave 160 death-in-progress.
    Full band, per-wave resolution, no gaps.
  - **Sitting 1 — 93 waves timed** (attempt 1, waves 1…93): 92 clears + wave 93
    death-in-progress. Per-wave resolution throughout; **no decade-resolution fallback
    used anywhere.** A second attempt (checkpoint restart at wave 70, t = 2398.92)
    contributes **0** timed waves.
  - **Total: 103 waves timed, 101 clears.**
- **Noise floor:**
  - **Sitting 1: ± 1.0 s** per wave interval (instrument-only ± 0.05 s)
  - **Sitting 2: ± 1.0 s** per wave interval (instrument-only ± 0.05 s)
  - Dominated by the Crucible's ~1 s wave-advance tick, demonstrated at
    p ≪ 0.001 on 92 sitting-1 intervals. The badge-vs-last-kill lag is same-signed and
    contained within that same tick — do not add the two.
  - **Pin tolerances on ± 1.0 s, not ± 0.05 s.** The instrument is far finer than the
    thing it is pointed at.

---

## 6. Mirror voice

The badge is a small red numeral in a gold ring, and for ninety-three waves it tells
the truth without being asked. What it will not tell you is what the ring costs. That
sits one screen earlier, in a dialogue the player scrolled past in two tenths of a
second — four descriptions, four debits, and the word *Vanguard* holding still just
long enough to be read. The fixture was never one ramp; it was a ramp, a death, and a
second entry that never began. The Mirror shows what is, and what is is two attempts,
four unlike defenses, and a counter that only moves once a second.
