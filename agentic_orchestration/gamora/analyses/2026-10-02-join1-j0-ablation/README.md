# JOIN-1 · J0: the ablation map, oracle side (v3.11, scripted pilot P-MOVE)

**NOT-A-GRADED-RUN. Print-only, and never a T-A artifact. Nothing tuned. No oracle behaviour change.**
gamora, 2026-10-02, Run JOIN-1 (charter v0.6 § 4.1 / § 5 J0; KC2 KP-229). Gate: jack-ryan Gate-2 on the classification and on the E-2 candidate. Neither may be quoted until that gate passes.

- Pre-registration (committed alone, before the harness existed): engine `0a3e0a0e`, `simulation/math/kc2-join1-j0-ablation-j1-selfjoin-prereg-2026-10-02.md` §§ 1–4
- Harness: engine `6227374a` + table amendment `1e4e00be` (see § Corrections), `simulation/scripts/gamora_join1_j0_ablation_map_2026_10_02.py`. It imports `gamora_kc2_play_v3p11_oracle_2026_10_02` unmodified.
- Per-family runs: `runs/<family>.json` (51 files, incl. CONTROL). Table: `ablation_table.json`. Launcher log: `run.log`.

## Control reproduces pass 4 (prereg § 1 gate: PASSED)
`CONTROL` (`V311-FULL`, arm M-POL-2, salts 0–19) gives **×1.0713**, with leg-A terminals at salts 2/10/15/18 (w160). This is pass 4's `pw_A` figure exactly.

Two cross-checks against pass-4 configurations computed by a different route also hold. `A-MUT` (the mutator keyword removed at the boundary) = **×0.9351** = pass-4 `LU`. `A-LINEUP` = **×2.1233** = pass-4 `MUT`. So the boundary-removal instrument and the oracle's own configuration switches agree to the fourth decimal.

## ⚑ Read this before the table: what "removed" means
A keyword removal restores `simulate_wave`'s **signature default**. For the v3.8–v3.11 folds, the default is **absent**. **For several base folds, the default selects the LEGACY pre-fold branch, not "no mechanism".** Examples:
- `A-SUSTAIN`: healing still lands, and more of it (heal 12.67 M vs 12.00 M).
- `A-DEF`: `defenses_enabled=False` takes the pre-defence path.

Those rows measure **"this fold vs its legacy branch"**, not "this mechanism vs nothing". The direction of a base-fold row is therefore not a sign of the mechanism's own effect. The rows affected are A-GMAG, A-MBOARD, A-DEFER, A-VOLLEY, A-SUSTAIN, A-SECOND, A-KITRES, A-DOTTL, A-CC, A-PETS-PLAYER, A-ALERT, A-PATROL, A-COUNTER, A-DEF and A-SEP. The pre-registered rule (§ 2) defined removal this way. The interpretation is named here, after the fact, so it is not buried (#12).

## The table (20 salts, paired; Δ against the control)

Columns: ratio = landed hp/s w151–159 / 1605.6 · dead = leg-A deaths of 20 (all in w160 unless marked) · legB = leg-B deaths per salt · wave_s = mean wave duration w151–159 · heal:in = Σheal/Σintake w151–159 · disc = bodies per tick in the disc · mov = the pilot's moving fraction.

| family | class | ratio | Δratio | dead | Δdead | legB | wave_s | heal:in | disc | mov |
|---|---|---|---|---|---|---|---|---|---|---|
| **CONTROL** | | **1.0713** | | **4** | | 0.20 | 39.38 | 0.9845 | 1.114 | 0.826 |
| A-LINEUP ⚑substitution | LOAD-BEARING | 2.1233 | +1.0520 | 20 (151–160) | +16 | 2.60 | 41.70 | 0.9277 | 1.674 | 0.843 |
| A-MUT | LOAD-BEARING | 0.9351 | −0.1362 | 2 | −2 | 0.10 | 38.74 | 0.9868 | 1.023 | 0.825 |
| A-MUT-BC | LOAD-BEARING | 0.9327 | −0.1386 | 2 | −2 | 0.10 | 39.13 | 0.9871 | 1.116 | 0.826 |
| A-MUT-LEECH | INCIDENTAL | 1.0841 | +0.0128 | 4 | 0 | 0.20 | 39.00 | 0.9826 | 1.091 | 0.822 |
| A-MUT-CRUEL | INCIDENTAL | 1.0265 | −0.0448 | 3 | −1 | 0.15 | 38.83 | 0.9807 | 1.041 | 0.827 |
| A-MUT-RA | LOAD-BEARING | 1.1730 | +0.1017 | 4 | 0 | 0.20 | 39.48 | 0.9810 | 1.122 | 0.824 |
| A-ENG | LOAD-BEARING | 1.2406 | +0.1693 | 11 | +7 | 0.55 | **23.14** | 0.9849 | 1.493 | 0.836 |
| A-ENG-REPOS | LOAD-BEARING | 1.1649 | +0.0936 | 3 | −1 | 0.15 | 40.28 | 0.9611 | 1.012 | 0.826 |
| A-ENG-PERSIST | INCIDENTAL | 1.1134 | +0.0421 | 5 | +1 | 0.25 | 39.77 | 0.9831 | 1.151 | 0.824 |
| A-ENG-RFA | LOAD-BEARING (c: wave +11.8 %) | 1.0676 | −0.0037 | 5 | +1 | 0.25 | 44.01 | 0.9775 | 1.011 | 0.824 |
| A-ENG-PETS | LOAD-BEARING | 1.1630 | +0.0917 | 6 | +2 | 0.30 | 39.41 | 0.9876 | 1.141 | 0.822 |
| A-ENG-SLOTS | LOAD-BEARING | 1.1882 | +0.1169 | 2 | −2 | 0.10 | 36.36 | 0.9756 | 1.101 | 0.823 |
| A-ENG-CROWD | INCIDENTAL | 1.0333 | −0.0380 | 5 | +1 | 0.25 | 37.17 | 0.9818 | 1.106 | 0.822 |
| A-PILOT ⚑pilot sensitivity | LOAD-BEARING | 0.9683 | −0.1030 | 7 | +3 | 0.35 | 45.43 | 0.9872 | 0.937 | **0.737** |
| A-SP (swing pause) | LOAD-BEARING (b: deaths +7) | 1.1070 | +0.0357 | 11 | +7 | 0.55 | 39.62 | 0.9817 | 1.093 | 0.824 |
| A-C11B | LOAD-BEARING | 1.0156 | −0.0557 | 2 | −2 | 0.10 | 39.34 | 0.9862 | 1.111 | 0.823 |
| A-INIT | INCIDENTAL | 1.0255 | −0.0458 | 5 | +1 | 0.25 | 39.87 | 0.9794 | 1.123 | 0.825 |
| A-EM-LAT | INCIDENTAL | 1.0812 | +0.0099 | 5 | +1 | 0.25 | 39.38 | 0.9849 | 1.126 | 0.826 |
| A-COMP-DOT | **INERT** | 1.0713 | 0 | 4 | 0 | 0.20 | 39.38 | 0.9845 | 1.114 | 0.826 |
| A-FR (fire range) | LOAD-BEARING | 1.0180 | −0.0533 | 3 | −1 | 0.15 | 33.01 | 0.9591 | 1.248 | 0.824 |
| A-FR-BANDAURA | NOT-ABLATABLE-ALONE | — | | | | | | | | |
| A-EM (emergence) | INCIDENTAL | 1.1284 | +0.0571 | 4 | 0 | 0.20 | 37.71 | 0.9866 | 1.124 | 0.823 |
| A-STAT | INCIDENTAL | 1.1292 | +0.0579 | 7 | +3 | 0.35 | 36.27 | 0.9786 | 1.231 | 0.824 |
| **A-COMP (composition)** | LOAD-BEARING | **1.5651** | **+0.4938** | 12 | +8 | 0.65 | 37.45 | 0.9497 | 1.153 | 0.825 |
| A-C11A (all C-11a) | INCIDENTAL | 1.0610 | −0.0103 | 3 | −1 | 0.15 | 39.41 | 0.9843 | 1.118 | 0.827 |
| A-C1 (retaliation gate) | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |
| A-C2 (auras/grants) | INCIDENTAL | 1.0610 | −0.0103 | 3 | −1 | 0.15 | 39.41 | 0.9843 | 1.118 | 0.827 |
| A-C4 (duration divisors) | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |
| A-POOL (pool lift) | LOAD-BEARING | 0.9071 | −0.1642 | 3 | −1 | 0.15 | 31.56 | 0.9961 | 1.443 | 0.841 |
| A-WINNER (winner surface) | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |
| **A-GMAG** (global magnitude) | LOAD-BEARING | **0.5381** | **−0.5332** | 0 | −4 | 0.00 | 38.69 | 0.9825 | 1.081 | 0.825 |
| A-MBOARD (measured board) | LOAD-BEARING | 0.7080 | −0.3633 | 3 | −1 | 0.15 | 38.84 | 0.9720 | 1.128 | 0.826 |
| A-DEFER | INCIDENTAL | 1.0497 | −0.0216 | 5 | +1 | 0.25 | 39.80 | 0.9855 | 1.110 | 0.825 |
| A-VOLLEY | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |
| A-SUSTAIN ⚑legacy branch | LOAD-BEARING (b: deaths −4) | 1.1125 | +0.0412 | 0 | −4 | 0.00 | 39.74 | 0.9912 | 1.111 | 0.826 |
| A-SECOND | INCIDENTAL | 1.0714 | +0.0001 | 4 | 0 | 0.20 | 39.24 | 0.9810 | 1.139 | 0.823 |
| A-KITRES | INCIDENTAL | 1.0834 | +0.0121 | 3 | −1 | 0.15 | 39.50 | 0.9799 | 1.105 | 0.825 |
| A-DOTTL | INCIDENTAL | 1.1185 | +0.0472 | 1 | −3 | 0.05 | 39.09 | 0.9791 | 1.125 | 0.824 |
| A-CC | INCIDENTAL | 1.0579 | −0.0134 | 4 | 0 | 0.20 | 40.29 | 0.9845 | 1.103 | 0.827 |
| A-PETS-PLAYER (player summons) | INCIDENTAL | 1.0655 | −0.0058 | 4 | 0 | 0.20 | 39.22 | 0.9830 | 1.097 | 0.825 |
| A-ALERT | INCIDENTAL | 1.1004 | +0.0291 | 4 | 0 | 0.20 | 39.75 | 0.9812 | 1.092 | 0.827 |
| A-MECH | NOT-ABLATABLE-ALONE | — | | | | | | | | |
| A-PATROL | LOAD-BEARING | 1.1566 | +0.0853 | 1 | −3 | 0.05 | 35.59 | 0.9843 | 1.197 | 0.828 |
| A-COUNTER (counterplay) | LOAD-BEARING | 1.2558 | +0.1845 | 8 | +4 | 0.40 | 40.08 | 0.9401 | 1.105 | 0.823 |
| A-DEF ⚑legacy branch | INCIDENTAL | 1.1137 | +0.0424 | 2 | −2 | 0.10 | 40.49 | 0.9826 | 1.129 | 0.828 |
| **A-SEP** (body separation) | LOAD-BEARING | **1.5163** | **+0.4450** | 11 | +7 | 0.55 | **56.88** | 0.9951 | 1.253 | 0.821 |
| A-CHAN (M-POL-2-NULL) | INCIDENTAL | 1.0768 | +0.0055 | 3 | −1 | 0.15 | 39.41 | 0.9833 | 1.061 | 0.839 |
| A-SEAT (M0) | INCIDENTAL | 1.0768 | +0.0055 | 3 | −1 | (identical to A-CHAN) | | | | |
| ARENA-W1 (an addition) | INCIDENTAL | 1.0528 | −0.0185 | 3 | −1 | 0.15 | 40.14 | 0.9841 | 1.075 | 0.820 |
| ARENA-W1-NULL | **INERT** | 1.0713 | 0 | 4 | 0 | | | | | |

The per-row reasons (which of the rule's clauses a–e fired, and SE_paired) are in `ablation_table.json` → `rows[].why`.

**Counts (50 rows plus the control):** 21 LOAD-BEARING (one is the pilot) · 25 INCIDENTAL, of which 5 are INERT · 2 NOT-ABLATABLE-ALONE · 2 arena arms (W1 INCIDENTAL; W1-NULL INERT) reported for completeness.

## What it says for the kit↔world boundary (descriptive)
- **The world's magnitude chain dominates.** The order of effect is global magnitude (−0.53), composition (+0.49), separation (+0.45), measured board (−0.36), engagement (+0.17), counterplay (+0.18), pool lift (−0.16) and mutators (−0.14). Each moves the ratio more than every kit-side fold combined.
- **The kit-internal folds are INCIDENTAL on this board:** player summons (−0.006), kit residual (+0.012), secondary streams (+0.000), DoT timeline, CC on the player and alert. This is the measured basis for treating them as INTERNAL rather than load-bearing boundary terms.
- **Swing pause moves deaths, not the mean.** Δratio is only +0.036, but leg-A deaths go 4 → 11: a w160 burst effect.
- **The C-11a layer reduces to C2 alone** (auras/grants, −0.010). C1 and C4 are byte-inert on v3.11, and so are the winner surface, the volley fold, the composition DoT divisor and the disarmed arena fold. They are carried, but they do nothing on this path (#86).
- **The line-up row is a substitution.** Removing the referent's line-up returns the seed-9 board (×2.12, 20/20 dead from w151). It measures the line-up's choice, not an absence.

## E-2 checklist: CANDIDATE (ungated; may not be quoted before jack-ryan's Gate-2)
These are the GD-native mechanisms classed LOAD-BEARING on this board:
1. the global-magnitude fold, with its C-11b attribute limb;
2. the measured board (PTH / crit reading);
3. GD composition (the additive own-term law);
4. body separation (contact response);
5. GD engagement: slots, pets in slots, RFA (by wave duration), and the v3.9 base;
6. fire range (reach);
7. swing pause (by deaths);
8. counterplay;
9. patrol;
10. pool lift;
11. the Crucible mutators (Brutal/Corrupted, Resilient/Ascended);
12. the line-up (as content, not mechanism).

Not GD-native, so excluded from E-2: the pilot (A-PILOT) and player sustain's legacy-branch row.

## Corrections, observations and findings
- **OBS-1 (instrument silence in the base harness).** `A-MECH` refused at wave 151 with `ActorStateUnclassifiable` ("the mech block is absent…", A-3), which the oracle raises loudly as designed. Yet `c11.run_arm`'s `raised` field read **None**, with 0 rows. The J0 table caught it only because the ratio came back None. The harness amendment classifies a no-row cell as NOT-ABLATABLE-ALONE. The base harness's silence is a **finding against `gamora_kc2_c11_lethality_decomposition_2026_09_29.run_arm`** (my seam; recorded, not fixed in this wave, because that script is part of the oracle-of-record composition).
- **OBS-2.** `A-FR-BANDAURA` is refused by `InitialSelfCastFold` (it needs the aura rows of fire range). The band/aura limb cannot be removed while the initial self-cast is on: a dependency, recorded.
- **OBS-3.** `A-CHAN` and `A-SEAT` are byte-identical on v3.11, so the seat's only effect on this path is the channel policy.
- **Correction (harness).** After the runs, `classify()`/`table()` gained the no-row branch above (OBS-1). No run was repeated, and no threshold or rule changed.

## Halt check
No ORACLE behaviour change: no file under `simulation/kc2/` and no oracle-of-record script was edited, and every removal is a harness-level keyword or constructor change, restored in `finally`. Nothing tuned. Disk was 26 GiB free (`df -h`) at the run, above the 20 GiB line. **Nothing halts to Matt from J0.**
