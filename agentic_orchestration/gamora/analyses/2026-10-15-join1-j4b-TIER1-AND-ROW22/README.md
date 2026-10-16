# JOIN-1 · J4b · TIER-1 ARMS AND ROW 22, graded ONCE against their REGISTERED predictions (gamora, 2026-10-15)

> **Labels carried on every print** (also in each JSON's `labels`):
> 1. **Primary of reference: the CORRECTED car2** (collab `e349130fb`), because these arms ran on the corrected lane. **The as-graded `aaa1f6a3f` stays the result of record.**
> 2. **NOT CONSERVATIVE:** the corrected lane raises her offense (KP-481 mana, KP-481 no-body Meteor / FB, KP-487 CARRY).
> 3. **COMPLETENESS PASSES UNDER A POST-HOC RULE** (jack-ryan `826520a1d`).
> 4. **CORR-4 FALSE AS PRE-STATED** (KP-463).
> 5. **Probe limbs carried by reference** (KP-456 / KP-459).
> 6. **Meteor-delay semantics RULED** (KP-476 / 481 / 487). The replay check is present on every arm.
> 7. **KP-490:** her in-flight missiles are dropped at a wave boundary.
> 8. **KP-473:** "use-weighted ≤ primary" on M-a and T is **SATISFIED AT THE CEILING, UNINFORMATIVE**. ADDENDUM-B off / off is **LOW EVIDENTIAL VALUE: informed by the flinch-on margin.**

## Inputs, verified first
- **Pins: every file verified on size and sha256.** In each case the committed pin file equals the bulk copy.

  | Arm | godot | Pin file sha256 | Files |
  |---|---|---|---|
  | use-weighted | `cd7d653` | `829fd0ac…` | 75 / 75 |
  | worst-case | `775e29d` | `d520d521…` | 75 / 75 (pins only; see below) |
  | raw | `874d88a` | `71bddef4…` | 75 / 75 |
  | flinch-off | `fba409f` | `38b2b3d6…` | 50 / 50 |
  | row 22 | `63af677` / `6efdbae` / `055f706` | `18730c80…` | 55 / 55 |

  ⚑ **The relay transposed two hashes.** By drax's own commit subjects, worst-case is `775e29d` and raw is `874d88a`.
- **My row replay** (engine `5f637abe`), with each arm bound to its own r_DMG row by hex:
  - use-weighted: `RB-A-anchor_r_dmg_use`, `40477d46fdd946ff`;
  - raw: `--anchor raw`, r_HP = r_DMG = 1.0;
  - flinch-off: primary, `4053a558dda37d80`.
  - **Result: PASS 25 / 25 in every class on every arm, 0 bad, 0 provenance mismatches.**
- **Leech HP-chain identity:** 25 / 25 on each arm, 0 off-ledger falls. Worst relative residual: use-weighted 6.7e-17, raw 2.3e-16, flinch-off 6.3e-17.
- **Gates:**
  - runs and OBS-1: 25 / 25 on each arm;
  - dot conservation: PASS on every arm;
  - effect gates: 0 violations on use-weighted and raw;
  - completeness (POST-HOC): PASS, with (P) holding; use-weighted has 3 orphans, all TERMINAL;
  - **flinch-off:** effect gates and completeness are **VACUOUS by construction** (L-21 off: no GH / GHR / GB; TIER2 (i)).
- **Grader functions:** `gamora_join4b_grade.py` `0ab979a7`, H = 40,000, applied as registered. No pairing or selection was changed.

## THE TABLE: registered prediction → result
| Item (registration) | Registered prediction | Result |
|---|---|---|
| **NC-J4b-ANCHOR, M-c** (prereg § 3 item 1; whole-cell M-c = Σ applied / Σ ticks) | anchored **>** raw | **TRUE.** car2 1,991,085 vs raw 311,691 (×6.39). 25 / 0, p = 5.96e-8 |
| **NC-J4b-ANCHOR, M-a** | anchored **≥** raw | **TRUE.** 25 vs **0** (raw dies in every cell, with life 2,821 at r_DMG 1) |
| (INFO) NC-ANCHOR on waves 159 / 160 | not registered | not formable: **raw reaches wave 159 in 0 cells** |
| **use-weighted ≤ primary, M-a** (item 2) | ≤ | **TRUE: SATISFIED AT THE CEILING, UNINFORMATIVE.** 25 vs 25 (the primary is at 25 / 25) |
| **use-weighted ≤ primary, T** (H = 40,000) | ≤ | **TRUE: SATISFIED AT THE CEILING, UNINFORMATIVE.** 1,000,000 vs 1,000,000 (the primary is at 25 × H) |
| use-weighted vs the Warlord, M-a / T | **UN-PREDICTED** | printed only: **M-a 25 vs 18**; **T 1,000,000 vs 749,609**. (M-c over 159 / 160, printed only: 3,038,999 vs 2,023,173, 25 pairs) |
| **primary ≤ worst-case, T** (H = 40,000) | ≤ | **PENDING, not graded.** The worst-case M0 arm is being re-emitted as a disclosed precaution. It will be graded once after the confirmation lands |
| **PREREG-ADDENDUM-B off / off:** M-c (her flinch-off) ≥ M-c (his flinch-off), waves {159, 160} | ≥ | **TRUE: LOW EVIDENTIAL VALUE.** 25 pairs, 0 dropped. 2,917,589 vs 2,119,294 (×1.377). **24 / 1**, p = 1.55e-6. Per-cell ratio 0.979 / 1.425 / 1.802; the one reversal is M-POL-2\|3 (115,909 vs 118,361). M-a printed only: 25 vs 17 |
| **Row 16 negative control** (L-21 off; "row identity on gated actions and motion") | NC passes; ACTIVE iff reach > 0 | **PASS → row 16 ACTIVE.** See the detail below |
| **Row 22, R0** (explicit d2-strict == today) | byte-identical | **TRUE.** My own check: all 7 G grains, GO, GH, GHR, GR, GC, GM, GB, GO-BODIES, HPCHAIN and J4B-ROWS of M0 / 0 equal car2 M0 / 0 |
| **Row 22, R1** (d2-strict, 8 forced families) | row identity vs the engine form | **TRUE.** My check: 9 rows (8 forced + 1 natural), each `(outcome, frames)` == `receivers.control_outcome(.., d2-strict)`, 0 bad |
| **Row 22, R2** (d2-nearest) | row identity | **TRUE**: 8 rows == the engine form, 0 bad. **slow25 EFFECT: NO VERDICT** (SLOW25 RECEIVER ABSENT; outcome recorded, effect unapplied; J4a list) |
| **Row 22, R3** (gd) | the sealed fold receives the landings | **TRUE, EVIDENCED BY SEALED COUNTERS** (drax `verdict.json`: `n_applications` +1 at each of ticks 100–107; Stun and Freeze resisted to zero, the other six inserted). 0 lane control rows (my check). The counters are not in the grain set, so this rests on drax's instrument |
| **Row 22, R4** (fail-first registry deletion) | RED | **TRUE (RED):** `raised_reason: j4b_kit_refused: ControlFamilyUnmapped: Sleep (tick 104)` (R4 provenance). laws sha `797625db…` is the same before and after |
| **Row 22, the zero-exposure count on J-S8** (car2, 25 cells) | printed | **11 natural landings, all Stun, in 10 cells.** Freeze, Immobilize, Knockdown, Petrify, Sleep, TakeHit and Trap: 0 |
| **Row 22 status** (prereg § 2: "predicted RI (named)") | RI | **ACTIVE.** Reach 11 > 0 and the forced-landing NC passes on every graded limb (gd by sealed counters; d2-nearest slow25 NO VERDICT, named). The RI prediction was already **FALSE AS PRE-STATED** (reached); this settles the row as **ACTIVE** |
| **Fraction (b)** | 22 ACTIVE + 1 RI (row 22) / 23 | **FALSE AS PRE-STATED.** The one named RI row (22) is ACTIVE, so the RI slot is empty. **The full count stays open:** each other BOUNDARY row needs its own NC to be counted ACTIVE, and several are NO VERDICT on the existing grains (rows 11–14 body NCs, 19, 21, 23, 24, 29, 30 destinations; NO-ARM-ITEMS § 2). **Demonstrated so far:** ACTIVE with NC passing: rows 8, 10, 15, 16, 17, 20, 22, 25 (non-magic), 26, 28, 31. PARTIAL: 9, 32 |

## Row 16 detail
- **Reach, on the car2 primary:** 7,712 GH decisions, of which **7,085 opened flinch windows**; `l21.n_reanchor` totals 1,034.
- **Off-control, on the flinch-off arm:**
  - L-21 off: no GH, GHR or GB grain, and no `l21` block in any cell's provenance (25 / 25);
  - **0 reanchors** and 0 GetHit draws;
  - the replay PASSes every class;
  - the effect gates have no windows to check.
- **Limit, stated:** "row identity on gated actions and motion" is evidenced here as *nothing is gated when the lever is off*. A byte comparison against a sealed no-lever reference is not in the grain set.

## Not graded here
- **primary ≤ worst-case on T:** waits for the worst-case M0 confirmation. It will be graded once, at H = 40,000.
- The offered ordering R2 ≤ R1 ≤ non-ladder (the tier-2 R2 / non-ladder arms).

*Graded once.* gamora, 2026-10-15. Engine `5f637abe` (replay `90e12d52`, grader `0ab979a7`).
