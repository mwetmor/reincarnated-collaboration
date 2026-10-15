# JOIN-1 · J4b: the arms each registered NO VERDICT item needs (read-only; no runs, no figures) (gamora, 2026-10-15)

**For the conductor's authorisation decision** (KP-472).

**Common to every arm below, unless an item says otherwise:**
- the 25 J-S8 cells (5 arms × salts 0–4, manifest `f82807fb`);
- the **tapes of record** `j4b-tapes-4e6ed5b3` (the same seeds as the primary run);
- runtime `fb49080f`, runner `e98309c`, pack **v5.1**;
- her kit `d2-fire-sorc-c14`, L-22 `enemy-anchored`, r_HP **R1 40.54578785101241**, r_DMG **PRIMARY 78.58354893651813**;
- **L-21 `d2-world` on every kit** (ADDENDUM-13 § 3: the remaining registrations are "evaluated at the primary setting");
- rows 22 / 23 / 24 `d2` (KP-454).

"Changes" below means the only settings that differ from this.

**"Blind?"** asks whether today's primary result (her M-c ×1.517 over {159, 160}, 25 / 0; her survival 25 / 25; collab `aaa1f6a3f`) could inform the item's outcome. Every registration was fixed before the run and cannot be revised. The question is how much evidential value is left.

---

## 1 · NC-J4b-ANCHOR (anchored vs raw)
- **Registered:**
  - prereg (engine `32d3325c`) § 3 item 1;
  - ADDENDUM-1 § B (`2c5413335` fold, engine design);
  - ADDENDUM-A § H.
- **Prediction:** **M-c anchored > raw** and **M-a anchored ≥ raw.** Paired totals over the 25 cells, with an exact sign test.
- **Arm needed: her RAW arm.**
  - Changes: **L-22 `raw`**, so **r_HP = r_DMG = 1**. The enemy-operand conversions are **kept** (ADDENDUM-3 § 1: the AR quantile table, `physical_contact_table`, and the DA / CtH solve stay as bound).
  - The comparator is not needed: this compares her anchored primary run with her raw arm.
- **Blind?** **Half observed.** The anchored half is today's primary run. The raw half is unobserved. The direction is near-mechanical: raw damage is 1 / 40.5 and raw life is 1 / 78.6, so the prediction can fail only if the anchor wiring is broken. **Low contamination risk.**

## 2 · The r_DMG arms and their orderings
- **Registered:**
  - prereg § 3 table and item 2;
  - ADDENDUM-6 / 7 § 4 / 9;
  - ADDENDUM-A § H.
- **Predictions:**
  - **use-weighted ≤ primary on M-a and on T;**
  - **primary ≤ worst-case on T only;**
  - every other pair is un-ordered.
  - M-a against the Warlord stays UN-PREDICTED in every arm.
- **Arms needed:**
  - **(2a) WORST-CASE.** Changes: r_DMG **97.06456111531031** (pack `RB-A-anchor_r_dmg_worst`), so her life is **273,819** GD HP.
  - **(2b) USE-WEIGHTED.** Changes: r_DMG **46.97872899159665** (pack `RB-A-anchor_r_dmg_use`), so her life is **132,527** GD HP.
  - In both arms r_HP stays R1, and every r_DMG-scaled sheet quantity moves with the arm (life, heals, potion life, flat absorb).
  - The prereg also asks for these as **comparator sensitivities**, i.e. each arm printed against `JOIN[warlord]` with no direction.
- **⚑ Two things to rule before these are graded:**
  1. **"use-weighted ≤ primary on M-a" can no longer fail.** Today her primary survival is **25 / 25**, the ceiling, so any count satisfies it. **That limb is now uninformative.** It was registered blind; it is reported as **"satisfied at the ceiling, uninformative"**, not as evidence. "use-weighted ≤ primary on T" likewise cannot fail, because primary T = H on every cell. **Only "primary ≤ worst-case on T" can still fail**, if the worst-case arm dies where the primary did not.
  2. **H is not numerically fixed.** The prereg defines H as "each cell's own fixed tick budget, identical across arms", and the runs carry the oracle's per-wave cap `oracle_max_ticks` 4000. **A one-line ruling on H is needed** (for example, the cell's 10-wave window under the cap) before any T limb is graded.
- **Blind?** The M-a and "use-weighted ≤ primary on T" limbs are **decided by today's ceiling**. The worst-case T limb is still blind in substance.

## 3 · The r_HP arms (the offered-damage ordering)
- **Registered:** ADDENDUM-A § C, which replaced the prereg § 3 item 6 M-c ordering.
- **Prediction:** **offered damage per tick: R2 ≤ R1 ≤ non-ladder** (RAW sense, her arms only, CORR-4 § 1; paired totals). M-c under each arm is printed, un-ordered.
- **Arms needed:**
  - **(3a) R2.** Changes: r_HP **29.152836858187047** (Chaos Sanctum; ADDENDUM-4 § 1.1).
  - **(3b) NON-LADDER.** Changes: r_HP ≈ **54.06** (= R1 / 0.75, the D2 non-ladder HP columns). **⚑ Its exact value is owed from C-13's classic-column re-run (legolas) before this arm can be run** (ADDENDUM-4 § 1.1: "owed if this arm is run").
  - R1 is the primary run.
- **Blind?** **Yes.** Her offered per tick at R1 was **not** computed or read in today's computation, which printed `applied` only. The ordering is mechanical (offered scales with r_HP by construction), so this is a row-identity check of the anchor.

## 4 · Her FLINCH-OFF arm (PREREG-ADDENDUM-B's off / off pairing)
- **Registered:**
  - PREREG-ADDENDUM-B (engine `a4d77ae2`) § 3;
  - ADDENDUM-13 § 2 (it stands as the sensitivity pairing).
- **Prediction:** **M-c (her) ≥ M-c (Warlord) over waves {159, 160}.** Paired where both kits reached wave 159; exact sign test; FALSE only on a strict reversal; fewer than 6 pairs gives NO VERDICT.
- **Arm needed: her arm with L-21 `gd` (NONE).** Nothing else changes.
  - **The comparator already exists:** his flinch-off arm is the engine leg (collab `0636752ba`, 7 / 7 vs `4c30b0d64`; port leg godot `53b8a7f`).
- **Blind?** **No, not in substance.** Flinch acts on monsters' attacks on her, not on her damage, so today's flinch-on margin (×1.517, 25 / 0, min ×1.085) strongly predicts the off / off outcome.
  - It was registered blind and is graded as registered.
  - **Its evidential value is now low**, and the print says so.

## 5 · Fractions (a) / (b) and the per-row negative controls
- **Registered:** prereg § 2 (the table) and ADDENDUM-A § H ("the § 2 negative controls, per row").
- **Predictions:**
  - **(a) 32 / 32** rows mapped (31 / 32 if row 18 is ruled unmappable);
  - **(b) 22 ACTIVE + 1 REACHED-INSENSITIVE (row 22) / 23.** ACTIVE requires a non-zero reach count **and** the row's NC passing.
- **(a) needs no arm.** It is a census / implementation determination: elrond's census § 13, the site table and the forms. It is a documentary check for elrond / jack-ryan.
- **(b): which NC needs which arm.** The "row identity" NCs are computable on the existing primary grains, with no new arm. The engine row replay already covers rows 8, 10, 15, 20, 26 (partly), 28 (per packet), 31 and 32.

| Row | NC as registered | New arm(s) needed |
|---|---|---|
| 8 cadence, 10 no hit roll, 15 family, 20 intake law, 31 thorns, 32 absorb (+ G-ABS-DOT) | row identity | **none** (primary grains plus the row replay) |
| 9 cast root | row identity (`move_refused_cast` 28,765) | none |
| **11–14** Fire Ball, Meteor, burning ground, splash | one NC per body: **body off**, so her Σ damage dealt falls (paired) | **4 arms:** L-14 off; L-19 off; L-20 off; splash footprint off |
| **16** L-21 | row identity on gated action and motion | **none for row identity** (the effect gates already cover it). If an off-arm NC is wanted, it is the **same arm as § 4** |
| 17 interruptible casts | row identity | none |
| **19** block | NC-ROW19: **`gd` (block 0.0) vs `d2`**; draws == eligible hits | **1 arm:** L-23 `gd-flat-block-value` (0.0) |
| **21** potions | NC-ROW21: `d2-belt` ≥ **`gd`** and ≥ **no-potion**, on survival and casts / s | **2 arms:** L-S7 `gd`; no-potion |
| **22** control received | **forced-landing unit control** (8 families × 3 settings, row identity, a fail-first registry deletion) plus the zero-exposure count | **an off-board fixture, not an arena arm.** drax's KP-440 forced-landing control (godot `ba7a7c4`) may already discharge it; jack-ryan to confirm. **Note:** row 22 was reached (10 landings), so the RI prediction does not hold, and ACTIVE needs this NC |
| **23** DoTs received | per-application row identity; per-application intake **d2 ≤ gd** (sign test) | **1 arm:** `dot_receiver_law gd` |
| **24** chill | row identity on chilled ticks; displacement ≤ | **1 arm** if a `gd` comparison is wanted (chill `gd`). Otherwise row identity on the primary grains |
| **25** family map | a fail-first entry deletion (a unit test); row identity; per-hit intake ≥ the referent map | **1 arm:** her sheet on the **referent `RESIST_PCT` map** (ADDENDUM-4 § 5). The deletion is a unit test, not an arm |
| **28** Static | row identity per packet; **`off` gives zero packets** | **1 arm:** L-07 `off` (or the `static_wanted` rule off) |
| **29** FA freeze / chill | a forced landing per tier per cold resist; 0 triggers from ranged or spell slots | **an off-board fixture** (forced landing), plus the trigger-class count on the primary grains |
| **30** Oculus | exact binomial proc rate; destinations in the square and walkable; draw count | **none** (primary grains: 5 procs / 43 draws) |

- **Blind?** The NC directions compare the kit against its own ablations, and they are mechanical (a body removed means less damage). Today's primary result does not inform them, except that **row 22's RI prediction is already resolved as "reached"**, a result disclosed in the graded print.

## 6 · The engine-side 16a recorder (WARN-1, the drain-exclusion bias)
- **Registered:** prereg § 4 item 12 (KP-427 WARN-1).
- **Prediction:** the static pre-count predicts **SlowManaLeach-only exposure** (ADDENDUM-4 § 6), with the bias bounded by `B_hi`, `B_eq` and the Disruption lost-cast bound.
- **What it needs:** **no new arm.**
  - **His flinch-off arm is engine-emittable.** An additive sidecar extension (the CORR-1 sidecar pattern) would read the oracle's own `run.non_health_rows` and `run.non_health_by_type` (`run.py:4452–4457`) per (cell, wave), over the same 25 cells.
  - **His flinch-on arm** would need drax's S16b per-type split. Today the port records 14 routings with no type.
  - **Her side is already measured: 0 landings on 25 / 25 cells** (16b), so **the bias on her margin is 0** whatever 16a shows.
- **Blind?** **Yes.** His drain exposure is independent of her outcome.

---

**Summary, by the cost of discharging each item:**
- **No new arena arm:**
  - fraction (a), documentary;
  - the row-identity NCs (on the existing grains);
  - row 30;
  - row 22 and row 29 via off-board fixtures (row 22 possibly already run);
  - the 16a recorder (an engine sidecar on his flinch-off arm).
- **One arena arm each:**
  - her RAW (NC-ANCHOR);
  - WORST-CASE r_DMG;
  - USE-WEIGHTED r_DMG;
  - R2;
  - NON-LADDER (blocked on the C-13 value);
  - her FLINCH-OFF (ADDENDUM-B; also the row 16 off-NC);
  - L-23 `gd`; L-S7 `gd`; no-potion; DoT `gd`; chill `gd`; the referent RESIST map; Static `off`;
  - the four body-off arms (rows 11–14).

*Read-only list. No run and no figure.* gamora, 2026-10-15.
