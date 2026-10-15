# JOIN-1 · J4b · B0-N prerequisite: the D2 stamping package, **v3** (for jack-ryan's narrow delta, then elrond's apply)

**Author:** gamora (normalization-rule owner). **Read-only on `corpus.db`.** Scratch copies only.

**Math notes:**
- engine `3e5054a9`: `join1-j4b-d2-stamping-2026-10-14.md`;
- engine `5b001f88`: CORRIGENDUM-1 (KP-442).

**Generator:** `simulation/scripts/gamora_join4b_d2_stamping_2026_10_14.py`. **v3 at engine `ce810948`** (v2 `2f70b989`, v1 `3d159a4b`).

**Input of record:**
- `corpus.db` FILE `2617c0c101d8d924cb327e50137b1b3a61b1a8cbd81a24632d2ebe3469eaa26b`.
- ROWSETs: J-S4b `c96d8975…`; `d2-fire-sorc` `db01da52…`; `gd-eor-warlord` `1819fd0c…`.
- The generator HALTs on any drift.

**Version history** (each superseding the last for the apply):

| Version | Collab commit | Change |
|---|---|---|
| v1 | `af12f6af7` | first package; 571 rows |
| v2 | `591ebde87` | + DATAMINED `d_prop_randclassskill_val1 = 3`: Hellfire Torch's planner stat holds the CLASS, not the bonus |
| **v3** | **this commit** | see below |

**What v3 changes:**
- **(a) KP-443 (jack-ryan's BLOCK on EXACT, collab `bb83a9eeb` + `f658a08b0`):** the referent grade is **CLOSE**. The deviation note is corrected:
  - 15 DISAGREE rows plus one categorical in KP-306's `agreement_check`, including a **consumed** one: `eor_rank_total` is 26 on the record vs 20 in the oracle (binding B-09);
  - only **11 of 38** bindings reach the configuration;
  - of the 82 unstamped rows, **31 ARE bound** under KP-305's provisional identity convention and **51 are unconsumed**.
- **(b) KP-444 (the planner's `skillProgression` IS SPENT):** the 24 VERBATIM progression entries (Fire Bolt +3, Inferno +19, Enchant +2) and `skillPos = 24` enter as input rows.
  - The adapter therefore derives final hard points **Fire Bolt 20 / Inferno 20 / Enchant 3** from the inputs, for 110 hard points in total.
  - With all-skills, class and tree skills plus Battle Command, that is **slvl 46 / 46 / 29**, and synergies Fire Ball **+560 %**, Meteor **+200 %**, burning ground **+60 %**.

| File | What |
|---|---|
| `corpus_j4b_d2_stamping_2026_10_14.sql` | ONE transaction, with guards. sha256 **`f9985251f76c0c099be48e4ca28d7192d56339e4ca1a1adff20857b7f690114a`** |
| `stamping_table.json` | every row with its anchor; the input digests; the two scratch applies |

## What the SQL does
1. **J-S4b:** `kit_mapping.grade = 'CLOSE'`, `terminal_state = 'MAPPED'`, plus (a)'s note. That is **one row**; `kit_numeric` is untouched.
2. **`R-D2S1`:** IDENTITY_v1 over 8 `d2_input_*` scales. The JOIN anchors are applied at the adapter boundary, never in the corpus.
3. **The new kit `d2-fire-sorc-c14`:**
   - a `canon_corpus` row (parked);
   - `kit_mapping` (grade NULL, owed);
   - 3 citations;
   - **597 INPUT rows**, all with `rdr = source`.

Rows by scale:

| Scale | Rows |
|---|---|
| level and quests | 19 |
| stat points | 4 |
| hard points (profile.skills 13 + progression 24 + skillPos 1) | 38 |
| item stats | 233 |
| CharStats | 19 |
| bases, runes and the Properties row | 117 |
| skill parameters | 144 |
| missile parameters | 23 |
| **Total** | **597** |

## Predicted post-apply ROWSETs (two independent scratch applies, A == B; integrity ok; 0 FK violations)

| Kit | Before | **After (predicted, v3)** |
|---|---|---|
| **J-S4b `gd-eor-warlord-referent`** | `c96d8975ca4d5e0511174c2ba5d6560329b1e049749e49137f7f45ab592ad0e9` | **`59099b7d779f44b5d56076058a0539af97b9497dd2e298868b8020c4fe598ac7`** (moved only by the grade row) |
| **`d2-fire-sorc-c14`** (new) | — | **`bbc2db8943086e85bf2504ccd4f4ed77fbcd87d9c84e692cdb2bf26a069db87b`** |
| `d2-fire-sorc` | `db01da52…` | `db01da528164eeec5935b0d0d1836f94ec748ebbd11118e2cf2360f7a26ed618` (unchanged, guarded) |
| `gd-eor-warlord` | `1819fd0c…` | `1819fd0c1e277469ff81016ae5e32cafa46ba4944e30d12f35d1ec2bf108c7cc` (unchanged) |

**Guards held on both scratch copies:**
- the OTHER-kits `kit_numeric` count and sums are the same before and after (562 / 110620.681632653 / 70298.0983204098);
- 597 rows inserted, 0 with `rdr ≠ source`;
- the referent's grade is `CLOSE` / `MAPPED`.

## The adapter's sheet from these 597 inputs (`join2_rulebook/d2/sheet.py`)
- life 2,821; mana 1,032;
- Defence 1,472 → FA (+105 %) 3,017 / 3,267;
- block 11 / 3;
- resists 75, uncapped 90 / 125 / 125 / 125;
- FCR 105 → 8 frames; FHR 60 → 8; FBR → 9;
- DR 18; magic absorb 8;
- BO 16 (+80 %), BC 16, FA 16;
- **slvl:** Fire Ball / Meteor / Fire Mastery / **Fire Bolt / Inferno 46**, **Enchant 29**, Warmth 27, Static / FA / Teleport 16.

The positive control and its fail-first test are engine commits.
