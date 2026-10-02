# PRE-REGISTRATION — v3.9 oracle pass 2 (KP-212), committed ALONE before pass 2 runs (KP-209 law)

**Seat:** gamora (oracle owner) · **Conductor:** gandalf · **Written:** 2026-10-02
**Engine at writing:** `9be13ef1` (math note `f16f2202` ALONE; folds `ca3cb890` · `7a84fc57` · `8e0cca0c` · `cac2a07b` ·
`c3df8b5b`; composition script `9be13ef1`; pilot derivation `8fd95dc9`, output collab `3b7647beb`).
**Labels:** KNOWN (a published replica value, not a prediction) · SEEN (a value I saw before writing, disclosed) ·
PREDICTED (from the rules alone).

## 0 · What ran before this file, and what I saw

- **Replicas (KNOWN), salts 0–2 only, per salt, all exact against legolas's published arms:**
  SP `[1.864, 2.0919, 1.8021]`; C11B `[2.3527, 2.5976, 2.3043]`; C11B-B `[2.332, 2.5748, 2.2801]`; AIMOVE
  `[2.0728, 2.1774, 1.4912]`; AIFULL `[1.7635, 1.7728, 1.5603]`; V38-FULL `[2.3801, 2.3386, 2.1895]`. Their 20-salt
  values are legolas's (`results_table.json`) and are stated below as KNOWN.
- **SEEN (disclosed): salt 0 only, during fold-3 smoke, the ratios were printed before I suppressed them:** 3b
  (DoT divisor) `2.3801` = the control (population 0); 3a (acquisition grid) `2.3635`; 3c (`initial`) `2.3396`.
  No other pass-2 configuration's ratio, death wave, landed or duration has been read.
- **Crash-only (counters only):** F5-HUNT and V39-FULL salt 0 ran, nothing raised; 1,014 / 1,921 drift ticks;
  V39-FULL 534 swings paused, 7,030 choices, 11,634 standing steps, 18,240 pursuing steps.

## 1 · The rules being tested (summarised; the math note is the authority)

| fold | rule |
|---|---|
| 1 swing pause | next swing at max(animation, U{min..max} ms), rerolled per swing (DATAMINED A) |
| 2 C-11b | dex and int × 1.10 (B) × 1.010 (A, declared mean) |
| 3 decodes | p05 acquisition on the 200 ms scan grid; SlowChaos/SlowAether int/200; `initial` = one self-cast (non-aura removed, gr3 aura → toggled aura; roster only) |
| 4 engagement | pursue to the CHOSEN skill's GD reach, stand in Attack, re-choose after each skill; specials → Normal → Default; 2.4 m halt retired for roster; pets keep the old rule |
| 5 pilot P-HUNT | while the 3.0 m disc is empty: player + K-MILL anchor close on the NEAREST live body at 0.919 m/s (the referent's measured closing); re-read every tick; nothing added while the disc is occupied |

## 2 · Predictions (PW-FOLDED salts 0–19, fixed seed-9 line-up; ratio = landed w151–159 / T / 1,605.6)

**Control, for reference (KNOWN):** V38-FULL ×2.390; first death in w160 on 20/20, 4.3–9.0 s in; wave means
13.4–24.9 s (w152 17.6 s, w155 13.4 s); standing fraction 2.46–4.92 m ≈ 0.08.

| # | configuration | quantity | prediction | basis |
|---|---|---|---|---|
| Q1 | F1-SP | ratio | **KNOWN ×2.015** (−16 %); 7/20 die in w160, 13 survive it | legolas SP |
| Q2 | F2-C11B | ratio | **KNOWN ×2.602** (+9 %); 16/20 first die in w160, 3 in 156, 1 in 151 | legolas C11B |
| Q3 | F3-DEC | ratio | **×2.30–2.40** (DOWN 0–4 %); first death in w160 on ≥ 15/20 | 3b population 0; 3a delays ~0.1 s on 26 p05 bodies; 3c removes ~0.2 % of landed and turns 15 slots into non-consuming auras (opposing); SEEN salt 0 −0.7 % / −1.7 % |
| Q4 | F4-ENG | ratio | **KNOWN ×1.790**; first death w152 on 18/20 (2 in w156) | legolas AIMOVE |
| Q5 | F5-HUNT | ratio | **UP 0 to +7 %: ×2.39–2.56**; first death still w160 on ≥ 15/20; w160 time-in 3–9 s | under the 2.4 m walk-in the disc is empty mostly early in a wave; closing sooner raises exposure and shortens the empty stretches (T down) |
| Q6 | F1+F4 | ratio | **KNOWN ×1.603**; w152 on 19/20 | legolas AIFULL |
| Q7 | V39-NOHUNT | ratio | **×1.72–1.92** | ≈ legolas ALLDEC ×1.827 (AIFULL + DOTDIV + C11B-B) × A ≈ ×1.01 × F3 ≈ ×0.98 |
| Q8 | V39-NOHUNT | first death / w152 | **the w152 stall persists:** first death in w152 on ≥ 15/20; w152 mean duration 35–48 s | the pilot is target-blind; casters stand off |
| **Q9** | **V39-FULL** | **ratio** | **×1.80–2.20 (central ×1.95): UP 0–20 % on V39-NOHUNT** | the pilot ends stalls (low-intake time leaves T) and refills the disc (more heal, but also the stood-off casters' intake continues while he walks) |
| **Q10** | **V39-FULL** | **the w152 stall** | **NOT fully resolved:** w152 mean duration **25–40 s** (against the referent's 16.3 s and AIFULL's 42.5 s); first death in w152 on **5–15 of 20** salts (fewer than Q8) | 0.919 m/s closes ~10 m of stand-off in ~11 s; the drive pull adds a few metres of tether slack; the mill keeps milling |
| **Q11** | **V39-FULL** | **time into w160** | of the salts that reach w160: **≥ 50 % first die in w160, 6–15 s in** (v3.8 4.3–9.0; the referent 29 s) | the pause and stand-off lower intake (later death), C-11b raises it; the w160 heal gap (empty disc, legolas lead 3) narrows only by the drift |
| Q12 | V39-FULL | w155 duration | **25–70 s** (AIFULL 92.9 s; referent 16.2 s) | same mechanism as Q10 |
| Q13 | V39-FULL vs V39-NOHUNT | leech-disc occupancy (bodies/tick, w151–159) | **UP by ≥ 1.3×** | the pilot's only action is to refill the disc |
| Q14 | F4-ENG, F1+F4, V39-NOHUNT, V39-FULL | standing fraction 2.46–4.92 m | **0.45–0.65 on all four**, overshooting the referent's 0.34; V38-FULL / F1 / F2 / F3 / F5 stay ≤ 0.15 | GD's stand-in-Attack; no RepositionForAttack, no contact jostle in the oracle (legolas P8) |
| Q15 | V39-FULL | pilot realised closing (empty disc) | **0.9–2.5 m/s** (≥ the drift; the drive pull adds); V39-NOHUNT (observer only) **0.2–1.5 m/s**; referent 0.919 | the instrument measures the whole pipeline (drive + drift + mill + cadence) |
| Q16 | V39-FULL vs V39-NOHUNT | disc-empty fraction of ticks | **DOWN**; V39-FULL still **≥ 0.25** (referent 0.14 of plate frames) | as Q13 |

**Graded arms (5 × salts 0–4, V39-FULL):**

| # | prediction |
|---|---|
| G1 | the five arms' ratios lie within ±10 % of each other (v3.8: ×2.315–2.334) |
| G2 | terminals mix w152 and w160 first deaths; at least one w152 first death in ≥ 3 of the 5 arms |

## 3 · Pass / fail

- Each prediction is graded HIT or MISS against its stated interval; KNOWN rows are checked as replicas (exact, or
  the replica failed).
- **No configuration is adopted or rejected on its ratio.** The folds are decoded (1–4) or derived from the
  referent's movement before any run (5); the referent is the test of the rules, not a target.
- Misses are reported with the mechanism that produced them, not re-predicted.
