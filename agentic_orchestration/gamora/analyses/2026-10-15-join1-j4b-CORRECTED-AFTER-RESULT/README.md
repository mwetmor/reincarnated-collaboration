# JOIN-1 · J4b · THE PRIMARY RE-GRADED ONCE ON THE CORRECTED LANE (car2): CORRECTED-AFTER-RESULT (gamora, 2026-10-15)

> **Labels carried on every print** (also in `grade_report.json` → `labels` and in `per_cell.json`):
> 1. **CORRECTED-AFTER-RESULT.** This is printed beside the as-graded margin `aaa1f6a3f`, **which stays the result of record.** This figure goes to its own jack-ryan gate.
> 2. **NOT CONSERVATIVE: the corrections raise her offense** (KP-481 mana, KP-481 no-body Meteor / FB, KP-487 CARRY).
> 3. **COMPLETENESS PASSES UNDER A POST-HOC RULE** (jack-ryan `826520a1d`; Gate-2 `39433b107`).
> 4. **ADDENDUM-13 CORR-4 § 2 is FALSE AS PRE-STATED** (KP-463).
> 5. **Probe limbs:** the read-ahead and FALSE-AS-PRE-STATED limbs are carried by reference (KP-456 / KP-459).
> 6. **Meteor-delay semantics are RULED** (KP-476 / 481 / 487). On car2 the replay check is **present**: 8,688 action checks (A1–A6, M1–M4), 0 bad. The label "OPEN, replay check absent" belongs to `aaa1f6a3f` only.
> 7. **WARN-2: row 22 (control received) is FALSE AS PRE-STATED** (as graded).
> 8. **4 tie-frame Meteors resolved by the registered order; D2 melee order would fire them (favours her)** (KP-485). Recounted on car2: still **4** (M0 s0 205, M0 s3 166, W1 s1 311, W1 s4 254). A further 16 tie-frame interrupts are of other skills; they are printed, not split by delivery.
> 9. **KP-490:** her missiles in flight at a wave boundary are **DROPPED** at `_wave_check`, on parity with the oracle's A3. Mana stays spent and the Meteor delay carries. Counts are below.

## Inputs, verified first
- **Grain pins.** car2 is drax's corrected primary (godot `98aeae6`): `/Users/admin/Games/join3c-bulk/car2/primary`.
  - Pin file `reincarnated-godot/evidence/join1/j4b-hook/car-primary/grains_sha256.json`, sha256 `4bbea4a5e6bdb906eef36dd065cae909341518b94bba00d886a004afd3ae7c25`.
  - **75 / 75 files verified** on size and sha256. The bulk copy is byte-identical to the committed pin file.
- **Lane:** KP-481 / 482 + EXT1, lock form `<=`, KP-487 (a) and (b) CARRY. Settings were read back from every cell: r_DMG 78.58354893651813.
- **Rule:** PREREG-ADDENDUM-C (engine `0c97b2ef`), applied as written, ONCE. Nothing was re-selected or re-paired.
- **Grader:** `0ab979a7`, unchanged at engine `5f637abe`. H = 40,000.
- **r_DMG binding:** primary (`RB-A-anchor_r_dmg`, hex `4053a558dda37d80`), with **0 provenance mismatches**.
- **Comparator:** his gb-fix flinch-on grains (pins `1a17de52…`), unchanged. His per-cell M-c is identical to as-graded in **25 / 25** cells.

## Every gate on car2: PASS
| Gate | Result |
|---|---|
| Row replay (engine `5f637abe`, my run, primary binding) | **PASS 25 / 25 in every class.** tape 34,478 · packet 25,568 · mana 72,304 · cast 8,663 · potion 123 · struck 950 · rebase 225 · control 11 · dot 462 · locks 8,869 · gh 15,474 · gr 1,034 · action 8,688. **0 bad** (`replay_summary.json`) |
| Leech HP-chain identity (BLOCK-1 form) | **25 / 25**, worst relative residual 7.7e-17, **0 off-ledger falls**. HPCHAIN `hp_fall` agrees (`hpchain_identity.json`) |
| Runs / OBS-1 | 25 / 25 terminal, nothing raised. OBS-1 complete |
| Effect gates (a) / (b) / (c) / dying | 0 violations in every arm (`gates.json`) |
| Dot conservation (with `running_at_end`) | PASS in every arm |
| Completeness (POST-HOC) | PASS. Precondition (P) holds in every arm; 6 orphans, **all TERMINAL** |
| GO wave-tag mismatches | 0 |

## THE PRIMARY, side by side: M-c (her) ≥ M-c (Warlord) over waves {159, 160}
| | **As graded `aaa1f6a3f` (OF RECORD)** | **CORRECTED-AFTER-RESULT (car2)** |
|---|---|---|
| Pairs | 25, 0 dropped | **25, 0 dropped** |
| Her total | 3,069,651.0 | **3,097,858.8** |
| His total | 2,023,172.6 | **2,023,172.6** (unchanged) |
| Ratio of totals | ×1.517 | **×1.531** |
| Sign | 25 / 0 / 0 | **25 / 0 / 0** |
| Exact two-sided sign test | p = 5.96e-8 | **p = 5.96e-8** |
| Per-cell ratio, min / median / max | 1.085 / 1.548 / 2.032 | **1.085 / 1.556 / 2.145** |
| Verdict | TRUE | **TRUE** |

**Per-cell delta of her M-c, corrected minus as graded** (`per_cell.json`):
- **Net Σ +28,207.8 (+0.92 %).**
- Up in 9 cells, down in 7, unchanged in 9. The 9 unchanged cells had no correction reaching waves 159 / 160.
- Range **−22,402.8 (−14.7 %, W1-NULL|3) to +18,297.4 (+14.8 %, W1|3)**.
- **Reading, stated rather than hidden:** the corrections raise her offense by construction (label 2). The per-cell signs mix because a corrected cast changes the trajectory of everything after it. Only the net total and the sign test are graded. **No pair flips**: the closest pair is W1-NULL|2 at ×1.085, unchanged.

Un-predicted prints (never a verdict):
- **M-a:** 25 vs 18.
- **T:** 1,000,000 vs 749,609.
- **M-d:** her **6.34 M** (as graded 6.65 M) vs 17.91 M.
- **M-b:** 250 / 250.
- **Whole-cell M-c (INFO):** her 1,991,085 vs 942,824.

## KP-490: her missiles dropped at a wave boundary (`dropped_at_boundary.json`)
- **The grains carry no dropped-missile counter**, so these counts are DERIVED.
- **Meteors:** two derivations are printed side by side and are **not reconciled cell by cell.**
  - created − impacts: **312** over 25 cells, 11–15 per cell. This one also includes Meteors still in flight at the final wave's end.
  - Meteors whose action + 60 frames passes a non-final boundary: **289**.
- **Fire Ball and pyre drops: NOT DERIVABLE from the grains (NO VERDICT).** An emitted counter is owed if a per-cell figure is wanted.

*Graded once.* gamora, 2026-10-15. Engine grader `0ab979a7` at `5f637abe`. Grains: car2 (`4bbea4a5…`). `aaa1f6a3f` is the result of record.
