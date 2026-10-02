# PRE-REGISTRATION — v3.11 oracle pass 4 (KP-225), committed ALONE before pass 4 runs (KP-209 law)

**Seat:** gamora (oracle owner) · **Conductor:** gandalf · **Written:** 2026-10-02
**Engine at writing:** math note ALONE `c2e1659c` · fold 1 (line-up) `29ef9e5c` · fold 2 (mutators) `8cf1cc8b` ·
composition script `3cfb2fda`.
**Labels:** KNOWN (a published value) · SEEN (a value I saw before writing, disclosed) · PREDICTED (from the rules,
the inputs and the control alone).

## 0 · What ran before this file, and what I saw

- **Unit tests** of both folds (`tests/test_kc2_v3p11_{lineup,mutators}.py`): constructed bodies and the bare
  `simulate_wave` w152/w153 board (no oracle stack). One bare-board w152 smoke printed landed totals and a 326 s
  timeout on the BARE board (no player offence; not an oracle figure).
- **Replica (KNOWN):** V310-FULL salt 0 through the edited engine and through the v3.11 script: ×1.7742, first death
  w152 at 42.286 s, exactly pass 3's published salt-0 values (the fold-off identity).
- **Crash-only smoke, V311-FULL salt 0 (SEEN, counters only, disclosed):** nothing raised; the line-up landed as
  pinned (board census w152/w155/w156); summon census per wave; mutator counters: flat rows 574 + 574, pct rows
  614 / 690, levels clamped 0, monster hits 994, leech heal 2.65 M HP (overheal 3.19 M), **Cruel active on 0.816 of
  player ticks**, resisted rows 578. The same smoke on V310-FULL printed its summon census.
- **No ratio, death, wave duration, time-into-w160 or per-wave intake figure of LU, MUT, V311-FULL or any
  attribution / sensitivity configuration has been computed, printed or read.**

## 1 · Referent and control (for reference)

**Referent (FOOTAGE):** ×1.0 (1,605.6 hp/s over w151–159); wave durations (Lap H-2) 151 15.6 · 152 16.3 · 153 14.9 ·
154 14.2 · 155 16.2 · 156 20.2 · 157 19.3 · 158 13.0 · 159 26.3 · 160 25.0 s. Per-wave intake (hp/s; legolas KP-211
lead 2): 151 1,220 · 152 766 · 153 1,394 · 154 2,692 · 155 1,018 · 156 1,648 · 157 2,167 · 158 288 · 159 2,318 ·
160 4,070.

**Control V310-FULL (KNOWN, pass 3, salts 0–19):** ×1.847; first deaths w152 ×9, w154 ×8, w160 ×2, w156 ×1, none
survive; w152 40.9 s, w155 19.9 s, w160 17.0 s (17/20 die in w160, leg A or B). **Own-wave intake ratio** (oracle
landed/s ÷ referent per-wave hp/s, from pass 3's per-wave ratios): 151 ×2.18 · **152 ×4.74** · 153 ×1.00 ·
154 ×1.95 · 155 ×1.83 · **156 ×2.30** · 157 ×0.45 · **158 ×4.66** · 159 ×1.79 · 160 ×1.42.

## 2 · Predictions (PW-FOLDED, salts 0–19)

**Ratio** = landed w151–159 / T / 1,605.6. **First deaths** = the leg-A terminal histogram over 20 salts. **Time into
w160** = per salt, the first death inside w160 (leg A or B) if any; reported as the count dying in w160 and the mean
time of that death.

| # | config | ratio | first deaths (20 salts) | w152 s | w155 s | w160: n die / mean t of the death |
|---|---|---|---|---|---|---|
| P1 | **LU** (line-up alone) | **×1.15–1.65** (central 1.40; seed-9 → re-drawn was ×0.71 in KP-211, and the referent's draw removes exactly the spike bodies) | **w152 ≤ 3**; w154 ≤ 8; ≥ 8 first deaths at w156 or later (incl. none); 0–8 with no death | 22–45 | 14–28 | 8–20 / 5–25 s |
| P2 | **MUT** (mutators alone, seed 9) | **×1.88–2.15** (central 1.98: Brutal/Corrupted raise intake, Resilient lowers the poison/bleed share; Leeching/Cruel act through duration) | w152 8–16; none survive | 40–55 | 19–27 | 14–20 / 3–17 s |
| **P3** | **V311-FULL** (both) | **×1.20–1.85** (central 1.50; = LU × 1.02–1.15) | **w152 ≤ 5**; ≥ 6 first deaths at w156 or later (incl. none); 0–6 with no death | 25–50 | 15–30 | 10–20 / 4–22 s |

**Per-wave own-wave intake ratio (vs the referent's per-wave hp/s):**

| wave | control (KNOWN) | P4 · LU | P5 · MUT (× control) | P6 · V311-FULL (× LU) |
|---|---|---|---|---|
| 151 | 2.18 | 1.0–2.0 | 0.95–1.20 | 0.95–1.25 |
| **152** | **4.74** | **1.5–3.5** (the spike falls ≥ 25 %) | 0.95–1.20 | 0.95–1.25 |
| 153 | 1.00 | 0.7–1.6 | 0.95–1.20 | 0.95–1.25 |
| 154 | 1.95 | 1.2–2.2 | 0.95–1.20 | 0.95–1.25 |
| 155 | 1.83 | 1.2–2.2 | 0.95–1.20 | 0.95–1.25 |
| **156** | **2.30** | **1.0–2.0** | 0.95–1.20 | 0.95–1.25 |
| 157 | 0.45 | 0.3–1.0 | 0.95–1.20 | 0.95–1.25 |
| **158** | **4.66** | **1.2–3.0** (the spike falls ≥ 35 %) | 0.95–1.20 | 0.95–1.25 |
| 159 | 1.79 | 1.0–2.2 | 0.95–1.20 | 0.95–1.25 |
| 160 | 1.42 | 0.9–2.0 | 0.95–1.20 | 0.95–1.25 |

A per-wave row is HIT if the wave's value is in its interval; P4–P6 are graded as "n of 10 waves HIT" and each
passes at ≥ 7/10.

**Direction predictions (attribution / sensitivity, on the referent board):**

| # | prediction |
|---|---|
| P7 | LU-BC ratio > LU ratio (flat + 50 % pierce/chaos only add intake) |
| P8 | LU-RA ratio < LU ratio (Resilient only removes poison/bleed intake; Ascended's additive +0.26 % is negligible) |
| P9 | LU-LEECH and LU-CRUEL: mean w151–159 wave duration > LU's (both slow the kill) |
| P10 | V311-ASCX ratio within ±3 % of V311-FULL, and its mean w151–159 duration ≤ V311-FULL's |
| P11 | LU-UNK ratio within ±6 % of LU (two extra boss bodies on two waves) |
| P12 | The summon check: the oracle produces fewer than all 17 referent summon identities (at least one identity the referent shows has no summon mechanic in the oracle — SEEN in the smoke as zero w151/w152/w153 summons on the referent board; disclosed above) |

**Graded arms (5 × salts 0–4, V311-FULL):**

| # | prediction |
|---|---|
| G1 | the five arms' ratios lie within ±10 % of each other |
| G2 | at most 5 of the 25 graded cells first die in w152 |

## 3 · Pass / fail

- Each row is HIT or MISS against its interval (a multi-part row is HIT only if every part is); central values are
  not graded; P12 is disclosed as informed by the smoke and graded but flagged.
- **No configuration is adopted or rejected on its ratio.** Fold 1 is the referent's own board (FOOTAGE+DATAMINED);
  fold 2 is DATAMINED. The referent is the test of the rules, not a target. Misses are reported with the mechanism
  that produced them, not re-predicted.
