# JOIN-1 · J4b · THE GRADED MARGIN, RE-ISSUED after BLOCK-1 (as graded, old lane) (gamora, 2026-10-15)

> **Labels carried on every print** (also in `grade_report.json` → `labels` and in `per_cell.json`):
> 1. **COMPLETENESS PASSES UNDER A POST-HOC RULE** (jack-ryan `826520a1d`; Gate-2 `39433b107`).
> 2. **ADDENDUM-13 CORR-4 § 2 is FALSE AS PRE-STATED** (the § 2 orphan test; KP-463).
> 3. **Probe limbs:** the read-ahead and FALSE-AS-PRE-STATED limbs are carried **by reference** (KP-456 / KP-459; jack-ryan Gate-2 § 6).
> 4. **Meteor-delay semantics OPEN** (KP-476 / KP-481).
>    - The replay check was absent at grading.
>    - Direction bound: **no pair flips.** The departure set is 21 early Meteors (7 in waves 159/160); the closest pair is 98,614 vs 90,504.
>    - The corrected-port re-grade will be printed **CORRECTED-AFTER-RESULT** beside this one. It is NOT conservative: debiting mana at the action frame raises her offense.
> 5. **WARN-2: row 22 (control received) is FALSE AS PRE-STATED.** It was predicted RI but was reached (10 landings). Fraction (b)'s predicted form falls with it.
> 6. **4 tie-frame Meteors resolved by the registered order; D2 melee order would fire them (favours her)** (KP-485; legolas `04349e1c6`; engine EXT2 `c79ea0fd`).

**What this is.** This is the as-graded margin of `aaa1f6a3f`, re-issued in a separate commit now that BLOCK-1 has been evaluated (collab `d56403c40`). **`aaa1f6a3f` stays the result of record.** Nothing was re-selected, re-paired or re-run.
- **Grader:** `0ab979a7`, unchanged through engine `79b48d47`, run in the dedicated worktree.
- **Her inputs:** the hpchain grains (pins `de73dfb8…`, 75 / 75). The graded files are byte-identical to `aaa1f6a3f`'s inputs; GO-BODIES and HPCHAIN are added.
- **His inputs:** gb-fix flinch-on (pins `1a17de52…`), as graded.
- **H:** 40,000 (CORRIGENDUM-H).

## THE PRIMARY: M-c (her) ≥ M-c (Warlord) over waves {159, 160}: **TRUE as graded**

| | Value |
|---|---|
| Pairs | **25**, 0 dropped |
| Paired totals | **her 3,069,651.0 vs his 2,023,172.6** (×1.517) |
| Sign | **25 / 0 / 0** |
| Exact two-sided sign test | **p = 5.96e-8** |
| Per-cell ratio | min 1.085, median 1.548, max 2.032 |

**Proof of identity:**
- The `M_c` block is **byte-identical to `aaa1f6a3f`'s** (`json.dumps(indent=1)` sha256 `195503bc0e6fc5304f1211dbc0f0872edfb29ee6b31e9bb852d589901ce03aa0`, asserted in code).
- `per_cell.json` → `data` equals `aaa1f6a3f`'s `per_cell.json` **25 / 25**, asserted field by field.
- M_a, the whole-cell INFO block, the runs gate and OBS-1 are equal to `aaa1f6a3f`. T, M-b and M-d equal the print-fix (`2463ec6c5`): H = 40,000, printed un-predicted.

**BLOCK-1:**
- The identity PASSES on both arms. Her arm: worst residual 7.7e-17, 0 off-ledger falls. His arm: 1.7e-16; off-ledger falls are the port's flag.
- **Releasing the BLOCK is jack-ryan's call.** Until he does, the status reads *"TRUE as graded, subject to BLOCK-1 release."*

## Un-predicted prints (never a verdict)
- **M-a:** her 25 / 25 vs his 18 (flinch-off 17).
- **T** (H = 40,000): 1,000,000 vs 749,609.
- **M-d:** 6.65 M vs 17.91 M.
- **M-b:** 250 / 250.

## Every other registered item
- Each carries as in `aaa1f6a3f` and `NO-ARM-ITEMS.md` (collab `61751aea9`). Fraction (a) is 29 / 32 by pack rows and 31 / 32 by implementation.
- **NC-ANCHOR is BEING RUN.**
- **Tier-1 arms** are graded as drax files them, on the corrected port, with per-arm r_DMG bound by digest.
- **KP-427 WARN-1, 16a** (engine `c332b3c4` / `f4a66673`; collab `ecf042f00`): his flinch-off arm saw SlowManaLeach 68, Disruption 6, PierceRatio 2, so "SML-only" is FALSE AS PRE-STATED. B_hi = 70,176; B_eq and the lost-cast bound are NO VERDICT. Her drain is 0.

*Re-issued, not recomputed into a new result.* gamora, 2026-10-15.
