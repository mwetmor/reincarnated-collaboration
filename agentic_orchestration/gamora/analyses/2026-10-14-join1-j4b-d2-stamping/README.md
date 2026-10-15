# JOIN-1 · J4b · B0-N prerequisite: the D2 stamping package (for elrond to apply after jack-ryan's gate)

**Author:** gamora (normalization-rule owner). **Read-only on `corpus.db`.** Scratch copies only.

**Math notes:**
- engine `3e5054a9`: `join1-j4b-d2-stamping-2026-10-14.md`;
- engine `5b001f88`: **CORRIGENDUM-1**, folding conductor KP-442.

**Generator:** `simulation/scripts/gamora_join4b_d2_stamping_2026_10_14.py`, **v2 at engine `2f70b989`** (v1 was `3d159a4b`).

> ⚑ **v2 SUPERSEDES the v1 package (collab `af12f6af7`) for the apply.**
> - **The one difference:** v2 adds a DATAMINED row, `d_prop_randclassskill_val1 = 3` (Properties.txt).
> - **Why:** Hellfire Torch's planner stat `item_addclassskills#3#x: 1` stores the rolled CLASS, not the bonus. The +3 class skills is Properties.txt `val1` (legolas C-14 § 2). The sheet derivation could not reach her slvl without it.
> - **Effect:** 571 → **572** rows; `d2-fire-sorc-c14` ROWSET `6062c960…` → **`d21dee9b…`**; the SQL sha256 is now `4ba86689…`.
> - **Unchanged:** J-S4b (`b7118b11…`) and the two guarded kits.

**Input of record:**
- `corpus.db` FILE `2617c0c101d8d924cb327e50137b1b3a61b1a8cbd81a24632d2ebe3469eaa26b` (elrond: no drift).
- ROWSETs: J-S4b `c96d8975…`; `d2-fire-sorc` `db01da52…`; `gd-eor-warlord` `1819fd0c…`.
- **The generator HALTs if any of them drifts.**

| File | What |
|---|---|
| `corpus_j4b_d2_stamping_2026_10_14.sql` | ONE transaction, with guards before and after. sha256 `4ba866897f06bd76a38999dc27b50851c4f6489a6e259279bd25a96d765f29e8` (v2) |
| `stamping_table.json` | every `kit_numeric` row with its anchor; the input digests; the two scratch applies |

## What the SQL does
1. **J-S4b `gd-eor-warlord-referent`:** sets `kit_mapping.grade = 'EXACT'` and `terminal_state = 'MAPPED'`, plus a deviation note giving the grounds. That is **one row**.
   - `kit_numeric` is untouched; the **82 unstamped rows stay unstamped** (the KP-305 no-rule set). This was proposed by the rule owner.
   - **The grade value is the gate's to confirm** (alternative: `CLOSE`).
2. **`normalization_rule` `R-D2S1`:** IDENTITY_v1, `source_scale = 'd2_input'`, covering 8 `d2_input_*` scales.
   - **FENCED:** the JOIN anchors (r_HP, r_DMG, the yard key) are applied at the adapter boundary, never in the corpus.
3. **The NEW kit `d2-fire-sorc-c14`** (KP-442):
   - a `canon_corpus` row (`source 'c14-build-file'`, **parked**, no canon_engine_key);
   - `kit_mapping` (grade **NULL**, owed after the B0-N re-run and the J4b gate);
   - 3 `kit_citations` (the Maxroll planner and guide, `authored`; the 1.13 data mirror, `dataset`);
   - **572 `kit_numeric` INPUT rows** (v2), all stamped R-D2S1 with `rdr = source`:
     - VERBATIM planner values (`build_file_standard_verbatim.json`, sha256 `ee5b8b22…`): level 99, stat points, hard points, quests, and every numeric stat, defence, socket and rune of every item worn or carried. The mercenary is excluded.
     - DATAMINED 1.13 values (the J-S7 pins): CharStats Sorceress, the item bases, the Gems mods of the socketed runes, the Skills parameters of 10 skills, and the Missiles parameters of fireball / meteorcenter / meteorfire.
   - **The derived sheet is NOT stored** (S3).

Rows by scale:

| Scale | Rows |
|---|---|
| level and quests | 19 |
| stat points | 4 |
| hard points | 13 |
| item stats | 233 |
| CharStats | 19 |
| bases, runes, and the Properties row (v2) | 117 |
| skill parameters | 144 |
| missile parameters | 23 |
| **Total** | **572** |

## Predicted post-apply ROWSETs (two independent scratch applies, A == B; integrity ok; 0 FK violations)

| Kit | Before | **After (predicted)** |
|---|---|---|
| **J-S4b `gd-eor-warlord-referent`** | `c96d8975ca4d5e0511174c2ba5d6560329b1e049749e49137f7f45ab592ad0e9` | **`b7118b110971f0e2269ef16ac4ca5f435ee12a896a51bad51ebfda106c4ee41f`** (moved only by the grade row) |
| **`d2-fire-sorc-c14`** (new) | — | **`d21dee9b6ddfb71283374fc6de88e80d630fe3ce4a7b885ccee00c797a492db9`** (v2; v1 was `6062c960…`) |
| `d2-fire-sorc` | `db01da52…` | `db01da528164eeec5935b0d0d1836f94ec748ebbd11118e2cf2360f7a26ed618` (**unchanged**, guarded) |
| `gd-eor-warlord` | `1819fd0c…` | `1819fd0c1e277469ff81016ae5e32cafa46ba4944e30d12f35d1ec2bf108c7cc` (**unchanged**) |

**Guards held on both scratch copies:**
- OTHER-kits `kit_numeric`: 562 rows, Σsource 110620.681632653, Σrdr 70298.0983204098, the same before and after;
- 572 rows inserted, 0 with `rdr ≠ source`;
- the referent's grade is `EXACT` / `MAPPED`.

## Owed next (this seat)
**The adapter's sheet derivation**, with its positive control:
- **What it derives:** life, mana, Defence, block, resists, frames, slvl, and the BO / FA percentages.
- **The control:** derived from these 572 inputs, it must reproduce legolas's C-14 sheet (`sorc_build_sheet.json` `charms_BO` plus stage 3) bit-exactly.
- **Order:** fail-first, then code. It runs before the B0-N numeric re-run, in the dedicated worktree.
