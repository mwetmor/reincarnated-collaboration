# PRE-REGISTRATION — v3.10 oracle pass 3 (KP-219), committed ALONE before pass 3 runs (KP-209 law)

**Seat:** gamora (oracle owner) · **Conductor:** gandalf · **Written:** 2026-10-02
**Engine at writing:** `e02ad1ae` — derivation `50a78411` + `a5d21618`; math note `1f980860` (ALONE) + § 6.4 addendum
`f227d441` (ALONE); folds `388e86a7` (1 D8 persistence) · `1cf2030a` (2 slots/WaitToAttack/path failure + pets) ·
`16e1bf3d` (3 RFA trigger) · `dc913076` (4 crowd jostle, with D7) · `817d51ef` (5 P-MOVE); composition `e02ad1ae`. Pilot derivation output (collab, this folder)
`pilot_move_derivation_referent.json` sha `8c40d895…`.
**Labels:** KNOWN (a published value, checked as a replica) · SEEN (a value I saw before writing, disclosed) ·
PREDICTED (from the rules and the control alone).

## 0 · What ran before this file, and what I saw

- **Replicas (KNOWN), all exact against legolas's published per-salt arms** (results `e4c6133fc`): RJ-PERSIST salts
  0–2 `[2.2623, 2.1964, 2.1349]`; RJ-SLOT `[2.0621, 2.0995, 1.9757]`; RJ-RFA `[2.4656, 2.4147, 2.4902]`; RJ-FULL
  `[1.8836, 2.328, 2.1153]`; the control V39-FULL through the new composition `[2.5439, 2.3089]`; R-FULL via the
  composition `[1.8836, 2.328]`. Standing on salts 0–1 (control 0.573 step / 0.485 net; R-FULL 0.575 / 0.600) was
  printed with them; the 20-salt values of these arms are legolas's (KNOWN, below).
- **SEEN (disclosed): the control's pilot motion on V39-FULL salt 0** (an instrument on the published arm): moving
  0.756 of ticks (> 0.49 m/s), mean speed 3.28 m/s over all ticks, 4.31 while moving; legolas's control closing
  +0.795 (empty) / −1.249 (occupied) is published.
- **Crash-only, counters only:** slots+pets salt 0 (pet slot counters); V39-FULL / F5-MOVE / V310-FULL salt 0 through the
  composition (nothing raised; P-MOVE jump/advance counts; slot/WTA/RFA/crowd/whiff counts). P-MOVE on the BARE
  `simulate_wave` boards w151–160 (no oracle stack): positions and duty counters only (max 48.5 m; commanded moving
  0.73–0.93). The § 6.3 → § 6.4 repair came from that bare-board smoke (sane-bound wall at 80 m), disclosed in the
  math note addendum.
- **No ratio, death, wave duration, standing, closing or disc figure of F2-SLOT, F24-SLOT-CROWD, F5-MOVE, V310-NOMOVE,
  V310-FULL or F1-LAND has been computed, printed or read.**

## 1 · Referent and control (for reference)

**Referent (FOOTAGE):** ×1.0; no death; w152 16.3 s, w155 16.2 s; standing at 2.46–4.92 m 0.34 (Lap H-2); closing on
the nearest with the disc empty +0.92 (60 fps frames; +1.05 on the 83 ms grid), occupied +0.13 / +0.15; pilot moving
0.848 of 83 ms windows, mean speed 2.98 m/s.
**Control V39-FULL (KNOWN):** ×2.304; first deaths w152 ×15, w156 ×2, w154, w160 ×2; w152 33.9 s, w155 28.5 s; standing
step 0.575 / net 0.479; closing (empty) 0.795; disc 1.661.

## 2 · Predictions (PW-FOLDED, salts 0–19, seed-9 line-up; ratio = landed w151–159 / T / 1,605.6)

| # | config | ratio | first deaths (20 salts) | w152 s | w155 s | standing step / net (2.46–4.92 m) | closing (empty) |
|---|---|---|---|---|---|---|---|
| P1 | **F1-PERSIST** (= RJ-PERSIST; pets untouched) | **KNOWN ×2.281** (−1.0 %) | KNOWN 152×15, 156×2, 160, 2 survive | KNOWN 35.4 | KNOWN 30.5 | KNOWN 0.586 / 0.488 | KNOWN 0.936 |
| P2 | **F2-SLOT** (pets in slots) | **DOWN vs control 10–22 %: ×1.80–2.07** (central 1.93; vs R-SLOT −8…+3 %) | w152 on 7–14; ≥ 3 survive | 35–47 | 24–32 | 0.51–0.57 / 0.43–0.50 | 0.85–1.15 |
| P3 | **F3-RFA** (= RJ-RFA) | **KNOWN ×2.381** (+3.4 %) | KNOWN 152×15, 160×4, 154 | KNOWN 33.9 | KNOWN 22.8 | KNOWN 0.573 / 0.472 | KNOWN 0.714 |
| P4 | **F24-SLOT-CROWD** | **DOWN vs control 4–20 %: ×1.85–2.21** (central 2.0) | w152 on 6–14; ≥ 2 survive | 38–56 | 20–31 | 0.53–0.61 / 0.52–0.68 | 0.95–1.30 |
| P5 | **F5-MOVE** (pilot alone) | **UP 0–15 %: ×2.30–2.65** (central 2.45) | w152 on ≥ 14 | 22–34 | 18–28 | 0.50–0.61 / 0.42–0.56 | 0.85–1.20 |
| P6 | **V310-NOMOVE** (folds 1–4) | **×2.00–2.25** (central 2.12; vs R-FULL ×2.168, pets −8…+4 %) | w152 6–13, w160 3–9, 1–7 survive | 44–62 | 18–26 | 0.54–0.60 / 0.55–0.65 | 0.85–1.15 |
| **P7** | **V310-FULL** (all five) | **×2.05–2.45** (central 2.25) | **w152 on 6–15; w160 on 2–9; 0–6 survive** | **33–55** | **17–26** | **0.50–0.60 / 0.50–0.65** | **0.85–1.20** |
| P8 | F1-LAND (sensitivity) | within ±2 % of F1-PERSIST | as F1 | as F1 ± 2 s | as F1 ± 2 s | as F1 ± 0.01 | — |

Further predictions on V310-FULL:

| # | quantity | prediction | basis |
|---|---|---|---|
| P9 | standing vs the referent | still ABOVE 0.34 on the step instrument by **+0.16…+0.26**; on the net instrument by +0.16…+0.31 | §6.1: the control's pilot already moves about as much and as fast as the referent, so P-MOVE changes DIRECTION more than duty; the decoded AI moved standing by −0.005 (legolas); neither should close a 0.23 gap |
| P10 | pilot realised (start-of-tick to start-of-tick) | moving fraction **0.74–0.88**; mean speed **2.3–3.1 m/s** (control 0.756 / 3.28; referent 0.848 / 2.98 on the 83 ms grid) | P-MOVE replays the referent's windows; the player's body clip and HOLD ticks pull it down |
| P11 | closing with the disc OCCUPIED | **−0.40…+0.40 m/s** (control −1.25; referent +0.15) | the replay carries the referent's occupied E[v cos δ] 0.15; the clip and nearest-switching add noise |
| P12 | disc occupancy w151–159 (bodies/tick) | **UP vs control (1.661) to 1.8–2.8** | the pilot no longer backs off when the disc is occupied |
| P13 | w152 and w155 vs the referent | both still LONGER than 16.3 / 16.2 s | the decoded AI lengthens w152 (slots, jams); the pilot does not kill faster than the referent |

**Graded arms (5 × salts 0–4, V310-FULL):**

| # | prediction |
|---|---|
| G1 | the five arms' ratios lie within ±10 % of each other |
| G2 | terminals include a w152 first death in ≥ 3 of the 5 arms |

## 3 · Pass / fail

- Each row is HIT or MISS against its interval (a multi-part row is HIT only if every part is); central values are
  not graded. KNOWN rows are replica checks (exact, or the replica failed).
- **No configuration is adopted or rejected on its ratio.** Folds 1–4 are decoded (legolas, DATAMINED); fold 5 is
  the referent's own motion. The referent is the test of the rules, not a target.
- Misses are reported with the mechanism that produced them, not re-predicted.
