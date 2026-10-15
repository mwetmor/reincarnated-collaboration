# JOIN-1 · J4b · THE GRADED MARGIN: the D2 Fire Sorceress vs `JOIN[warlord, gd-decoded @ 196]`, computed ONCE under PREREG-ADDENDUM-C (gamora, 2026-10-15)

> **Labels carried on every print:**
> - **COMPLETENESS PASSES UNDER A POST-HOC RULE** (jack-ryan `826520a1d`; Gate-2 `39433b107`);
> - **ADDENDUM-13 CORR-4 § 2 is FALSE AS PRE-STATED** (KP-463);
> - the read-ahead and FALSE-AS-PRE-STATED probe limbs are carried **by reference** (KP-456 / KP-459; jack-ryan Gate-2 § 6).

**Release and provenance:**
- **Release:** KP-471. Matt's windowed self-test at `fb49080f` is GREEN 85/85 (godot `773867b`); KP-312 conditions 1–5 are met.
- **The grain set of record is the gb-fix grains** (`/Users/admin/Games/join3c-bulk/gb-fix/arms/`), runner `e98309c`, runtime `fb49080f`, pack v5.1, the tapes of record `j4b-tapes-4e6ed5b3`, labelled.
  - The pin file sha256 is `1a17de52fc460fd0371472aea8d77ff3687b95d893b52d2b71acacb4d32fc333`, and **105 / 105 pins were verified**.
  - **G1–G7 are pinned here** (INFO-1) in `g1_g7_pins.json`: 70 files, sha256 `b77414ef55e40a6da1e60197387e154db13ba91064d4171a72b4bff32dc165d6`. All 70 also equal their `manifest-port.json` digests.
- **Grader:** `gamora_join4b_grade.py` at engine **`e7939e40`**, run in the dedicated worktree.
  - **One instrument fix was needed before any figure was read:** the comparator port GO declares `offered = null` on disc and summon rows, and `cell_metrics` raised a TypeError on it.
  - The fix was made fail-first (`de0233bb`, then `e7939e40`). It does not touch M-c, which reads `applied`.
- **Rule:** PREREG-ADDENDUM-C (engine `0c97b2ef`), applied as written. No re-run, no re-selection, no change of pairing. (The grader's label string reads "PREREG-ADDENDUM-B § 3" because C reuses B's rule and waves.)
- **The two senses of "offered"** (CORR-4): M-c reads `applied` only, and no `offered` is compared across the two emitters.

---

## THE VERDICT: the PRIMARY registration (flinch-on vs flinch-on): **TRUE**

**M-c (her) ≥ M-c (Warlord) over waves {159, 160}:**

| | Value |
|---|---|
| Pairs | **25** (both kits reached wave 159 in every cell; **0 dropped**) |
| Paired total, Σ over cells of per-cell M-c | **her 3,069,651.0 vs his 2,023,172.6** (×1.517) |
| Sign | **25 positive / 0 negative / 0 ties** |
| Exact two-sided sign test | **p = 5.96e-8** |
| Per-cell ratio, her / his | min **1.085**, median **1.548**, max **2.032** (`per_cell.json`) |

The prediction was "≥", and it would be FALSE only on a strict reversal. **There is no reversal, so it holds.**

## The gates (ADDENDUM-A § F as extended): all PASS
- **"Runs":** 25 / 25 cells, terminal, nothing raised. OBS-1 complete on both arms. drax's run: 0 refusals, 0 SCRIPT ERROR.
- **Comparator:**
  - engine leg 7 / 7 vs `4c30b0d64` (collab `0636752ba`);
  - port leg 7 / 7 (godot `53b8a7f`);
  - his flinch-off null path inert on the new runtime (jack-ryan Gate-2 § 7).
- **Engine row replay:** her 25 cells PASS on every class with 0 mismatches. His GH (173,430 rows) and GR replay with 0 mismatches. The replay inputs are byte-identical between `2ca2298` and gb-fix (only GB changed).
- **Effect gates (a) / (b) / (c):** 0 violations on both arms (gb-fix GB).
- **Dot conservation** (with `running_at_end`, ruling 2): 25 / 25 PASS.
- **Completeness: PASS UNDER THE POST-HOC RULE.** Precondition (P) passes on 50 / 50 cells, and all 63 orphans are TERMINAL. **The CORR-4 test remains FALSE AS PRE-STATED.**

## Every other registered item (ADDENDUM-A § H / prereg § 3)

| Item (as registered) | Result |
|---|---|
| **M-a vs the Warlord: UN-PREDICTED in every arm** | printed only: **her 25 / 25 survive; he survives 18 / 25** (flinch-on). Flinch-off baseline 17 / 25 |
| M-b, M-d: UN-PREDICTED | printed only: M-d Σ intake **her 6.65 M vs his 17.91 M** (her lower in 24 / 25 cells). M-b: G7 carries no `wave_end` tag, so "cleared" counts waves reached, **250 / 250 for both**. Printed, not interpreted |
| M-c (her) ≥ M-c (Warlord), whole cell (ADDENDUM-A § B) | **superseded** by B / C (wave-restricted). The whole-cell figure is printed as INFO: her 1,990,857 vs his 942,824 (25 / 0) |
| **NC-J4b-ANCHOR** (M-c anchored > raw; M-a anchored ≥ raw) | **NO VERDICT.** The `raw` arm is not in the released grain set (not run) |
| **Arm orderings** (use-weighted ≤ primary on M-a and T; primary ≤ worst-case on T) | **NO VERDICT.** The worst-case (×97.06) and use-weighted (×46.98) r_DMG arms were not run |
| **Offered damage per tick: R2 ≤ R1 ≤ non-ladder** | **NO VERDICT.** The R2 and non-ladder r_HP arms were not run |
| **The § 2 negative controls, per row, and fraction (b)** | **NO VERDICT.** The per-row NC runs are not in the released grain set. Reach counts are printed below |
| Fraction (a): 32 / 32 rows mapped | **NO VERDICT.** It is not measured from grains; it is a census / implementation property, outside this computation |
| **PREREG-ADDENDUM-B (off / off sensitivity pairing)** | **NO VERDICT.** Her flinch-off arm was not run |
| Asymmetry line (her flinch-on vs his flinch-off), printed, not registered | 25 pairs, her 3,069,651 vs his 2,119,294, 25 / 0, p = 5.96e-8. M-a: her 25 vs his 17 |
| His M-c **without summons** (CORR-1 sensitivity) | 25 pairs, his 2,022,944, 25 / 0. Unchanged |
| **Comparator sensitivities r_DMG ×97.06 (worst) and ×46.98 (use-weighted)** | **NO VERDICT** (not run) |
| The yard key, population R2 / R3 / R4, no-FA, the ES arm, champions frozen, Warmth 0, no-potion / no-refill, ECDF P, bleeding-contact, no-charm sheet (prereg § 4) | **not run.** Nothing is printed |

## KP-427, reported separately
- **WARN-1, the drain-exclusion bias:**
  - **Her side (16b, port):** `non_health_by_type` is **empty in 25 / 25 cells**, so there were **0 SlowManaLeach / ManaBurnDrain / Disruption landings on her**. That gives **B_hi = 0, B_eq = 0, and a lost-cast bound of 0** for her margin.
  - **His side:** the port's S16b counter shows 14 non-health routings over 11 cells; the type split is not exported on his profile.
  - **The engine-side 16a recorder (oracle run attributes) was never built,** so that sub-item is **NO VERDICT**.
  - **Bias on her margin: 0** (nothing landed on her).
- **WARN-2, REACHED-INSENSITIVE (named rows):**
  - **Row 22** (control received, predicted RI): **10 landings** across her 25 cells, so it was **reached**. RI does not hold. ACTIVE still needs its NC, which is NO VERDICT above.
  - **Row 9** (cast root): `move_refused_cast` **28,765**. Reached.
  - **Row 24**, the freeze → chill clause: tied to row 22, which was reached (control rows include Freeze → chill).
  - **Row 26**, the Resilient bleed clause: **RI by declaration.** `resilient_bleed_noop` fired 62 times, counted.
  - **Row 32** (flat absorb): Aether 94, Chaos 671 and Life 319 intake rows landed. Reached.
  - **Other reach counts** (her 25 cells):

    | Counter | Count | Counter | Count |
    |---|---|---|---|
    | casts | 8,673 | fb_explosions | 5,446 |
    | meteor_impacts | 1,423 | pyre_frames | 180,482 |
    | static_casts | 787 | blocks | 39 / 569 draws |
    | hitrec | 109 | potions | 130 |
    | FA freeze / chill | 204 / 126 | oculus procs | 5 / 43 draws |
    | thorns | 330 | L-21 flinch windows (GH) | 7,049 |

## Fidelity-cost table and the HOME margin
- The fidelity-cost table is prereg § 5, and it carries unchanged. Drains on her: 0.
- **The HOME margin is DEFERRED**, with the re-entry criterion as prereg § 5.

*Computed once.* gamora, 2026-10-15. Engine grader `e7939e40`; the grain set is gb-fix (`1a17de52…`) with G1–G7 pinned (`b77414ef…`).
