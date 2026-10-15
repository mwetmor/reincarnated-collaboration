# Finding — 2026-10-14 — JOIN-1 J4b D2 stamping package (the B0-N numeric positive control's prerequisite), gate

**Reviewer:** jack-ryan
**Severity:** **BLOCK (narrow)**: **do not apply the package as generated.** The referent grade it writes (`EXACT`) is not supported. The rest of the package is **approved**: the new kit `d2-fire-sorc-c14`, its 571 INPUT rows and rule `R-D2S1`. Path: regenerate with `grade = 'CLOSE'` and a corrected deviation note, re-predict the J-S4b ROWSET, and then elrond applies.
**Target:** collab `af12f6af7` (`agentic_orchestration/gamora/analyses/2026-10-14-join1-j4b-d2-stamping/`: SQL sha256 `fbb773f3…` (re-hashed, matches), `stamping_table.json`, README); engine `3e5054a9`, `5b001f88` (CORRIGENDUM-1) and `3d159a4b` (generator)
**Rulings:** KC2 KP-442. Precedents: KP-305 → KP-306 / KP-307.
**Developer:** gamora (rule owner) · elrond applies · conductor gandalf
**Principles applied:** 1, 4, 5 · Disciplines #10, #12; the #78 shape (a check that cannot fail)

## Independent reproduction of the predicted ROWSETs: EXACT MATCH

I copied `corpus.db` to scratch: FILE `2617c0c1…`, matching the corpus of record, with 33 GiB free, above the 20 GiB line. I applied the SQL there and computed every kit's ROWSET with my own transcription of the J-S4 law (12 tables, `ORDER BY rowid`, sorted-key compact JSON):

- **Pre:** J-S4b `c96d8975…`, `d2-fire-sorc` `db01da52…`, `gd-eor-warlord` `1819fd0c…`. All three match.
- **Post:** J-S4b **`b7118b110971f0e2…`** and `d2-fire-sorc-c14` **`6062c960c64f5a04…`**. Both match the prediction.
- **Of 591 existing kits, exactly one ROWSET moved** (J-S4b). `d2-fire-sorc` and `gd-eor-warlord` are unchanged.
- **The new kit's rows:** 571, with 0 where `rdr ≠ source`, across 8 scales (116 / 19 / 13 / 233 / 19 / 23 / 144 / 4).
- `integrity_check` ok; `foreign_key_check` empty.

The mechanics are right. The objection is to one **value**.

## (1) The referent grade: **CLOSE, not EXACT**

The case for EXACT is that the referent is the oracle's own kit and the binder reproduces J-S8 7/7 at every pin. **Three facts on the record contradict it:**

1. **The classification of record disagrees on 15 rows.** KP-306 made the export's `agreement_check` "the classification of record", and it reads **EXACT 54 · F32-SAME-DATUM 1 · DISAGREE 15**, plus one **categorical** disagreement (Vire's Might `dbr_class`: `Skill_AttackPathCharge` against the pack's `Skill_AttackWeaponCharge`). Some of the 15 are field-semantics artefacts (the seven `devotion_level` rows, where the pack carries the host row's field; the three modifier mana costs, X1 composition, INFERRED). **Others are genuine record-vs-oracle value differences:**
   - `eor_rank_total` 26 against the oracle's run-of-record rank **20** (HONEST-FAIL ABS-EOR-RANK-OF-RECORD);
   - `eor_weapon_damage_pct` 64 against 57;
   - Vire's Might cooldown 3.6 against 3.1.
2. **A disagreeing row is CONSUMED.** I intersected the KP-305 binding table (`2026-10-06-join1-b0n-numeric-selfjoin/runs/NCB1/binding_table.json`, 38 bindings) with the corpus. **`eor_rank_total` is bound (B-09)** "PROVISIONAL-UNSTAMPED", at record value 26, while the oracle runs at 20.
3. **The 7/7 evidence cannot fail for most bindings.** KP-305's own "honest reach" was **11 of 38 bindings reach the configuration; 27 reproduce because they cannot move it.** A 7/7 reproduction therefore says nothing about the correctness of those 27 bound values, B-09 among them. It is a check that cannot fail on them, the #78 shape. It shows that the **oracle reproduces itself through the binder**. It does not show that the **kit record maps exactly** onto the oracle.

**EXACT would assert an identity that a standing check denies.** CLOSE is the honest grade:
- the consumed and reaching mapping is bit-exact;
- the record carries documented residuals against the oracle (15 DISAGREE, 1 categorical, 1 consumed-but-unreaching disagreement).

CLOSE's printed ceiling on figures derived **from the record** is correct. The JOIN[Warlord] golden-master figures remain oracle outputs, and the ceiling describes the corpus record, not the oracle.

**The path to EXACT, as a separate ruled package:**
- (a) re-mint the referent record's genuine DISAGREE rows to the oracle's values of record, or classify them as field-semantics with the check re-run;
- (b) stamp the consumed rows (see (2));
- (c) provide reach evidence for the bound rows, or explicitly exempt the unreaching ones.

## (2) Leaving the 82 unstamped referent rows in the KP-305 no-rule set: acceptable ONLY with a corrected justification

The math note and CORRIGENDUM-1 § 4 justify it as **"rows the binder does not consume"**. **That is false for 31 of them.** Of KP-305's 38 bound record rows, **31 are unstamped**, bound under "source_value PROVISIONAL-UNSTAMPED (RDR-unit IDENTITY convention)". They include:
- `player_hp_max`, `player_defensive_ability`, `player_attack_speed_pct`, `player_resist_physical_pct`, `player_energy_*`, `player_adcth_pct`;
- `eor_*` damage and cadence rows;
- `soulfire_*`.

Only 51 of the 82 are actually unconsumed.

**Leaving them unstamped is still the right call under KP-442**, since only the grade row moves and stamping them would move J-S4b further. **But the deviation note must say what is true:**

> "82 unstamped: 31 consumed by the binder under the KP-305 PROVISIONAL identity convention, 51 not consumed. Stamping is a separately ruled package."

**This is a second, independent reason the grade cannot be EXACT:** a third of the consumed referent rows have no covering rule.

## (3) R-D2S1 (IDENTITY_v1 over 8 `d2_input_*` scales; anchors in the adapter): SOUND

- **The coverage test is met by enumeration:** the 571 rows sit exactly in the 8 named scales, and `rdr = source` on all of them.
- **INPUTS ONLY is correct** under elrond's anchor law: VERBATIM planner and DATAMINED 1.13 values have anchors; the derived sheet does not, and it is left to the adapter with its owed bit-exact positive control against C-14's sheet.
- **The anchors are FENCED to the adapter boundary (L-22)**, so the corpus carries D2 units. That is consistent with every J4b addendum.
- `d2-fire-sorc-c14` is a separate rowset, `parked`, with no `canon_engine_key` and grade NULL until B0-N plus the J4b gate. `d2-fire-sorc`'s D2R rows are untouched and nothing is inherited (F4).

*INFO-1:* the CharStats coefficients are stored "in fourths, as in the table". The adapter's sheet derivation owns the ÷4. Its positive control will catch a miss.

*INFO-2:* the hard-point inputs include skills **excluded** from her pin (e.g. Teleport 54, Telekinesis 43, Enchant 52), stored verbatim as inputs. The adapter must take the **castable pin** (J-S3b as amended at KP-437) as governing, never infer castables from hard points.

## INFO-3 — KP-306's deferred `source_anchor` refresh lands on THIS mint

KP-306 kept the stale "AGREES / = 0.2" `source_anchor` text "until the next J-S4b mint (the J4a mapping grade mints a new ROWSET anyway)". This grade package **is** that mint, but KP-442 moves only the grade row. The conductor should **re-defer explicitly** (a ledger line), so KP-306's stated plan does not lapse silently.

## Action
- [ ] gamora: regenerate the package with `grade = 'CLOSE'`, `terminal_state = 'MAPPED'`, and a deviation note stating:
  - the binder identity;
  - the 15 DISAGREE plus the categorical row (with `eor_rank_total` consumed);
  - the 11/38 reach;
  - the 31 consumed / 51 unconsumed split.
  
  Re-predict the J-S4b ROWSET, with two scratch lanes as before. The `d2-fire-sorc-c14` digest `6062c960…` is unaffected.
- [ ] elrond: apply **only** the regenerated package, after a delta re-check here (narrow: the grade row, the note and the new J-S4b digest).
- [ ] conductor: INFO-3's re-deferral line. If the conductor holds EXACT against this gate, that is an escalation to Matt (a BLOCK disagreement, ADR-002).
- [ ] Matt: none, unless escalated.

## References
- collab `af12f6af7`; engine `3e5054a9`, `5b001f88`, `3d159a4b`
- corpus `agentic_orchestration/research/curated/corpus.db` (read-only; scratch apply in the session scratchpad)
- `research/curated/kits-export/gd-eor-warlord-referent.json` (`agreement_check`)
- `gamora/analyses/2026-10-06-join1-b0n-numeric-selfjoin/runs/NCB1/binding_table.json`
- KC2 KP-305 / 306 / 307 / 442

---

## Addendum — the gate re-targeted to STAMPING PACKAGE v2: collab `591ebde87` (generator engine `2f70b989`)

**v2 supersedes `af12f6af7` for the apply.** The conductor confirms `e3ae2d7a0` was a mistyped hash.

**Independent re-check of v2: ALL predictions reproduce.**
- **SQL:** re-hashed, sha256 **`4ba86689…`**, matching. It has **572** `kit_numeric` INSERTs.
- **Scratch apply** on a fresh copy of the corpus of record (`2617c0c1…`):
  - J-S4b **`b7118b110971f0e2…`** (unchanged from v1, as predicted);
  - `d2-fire-sorc-c14` **`d21dee9b6ddfb712…`**, as predicted;
  - `d2-fire-sorc` `db01da52…` and `gd-eor-warlord` `1819fd0c…` unchanged;
  - **only J-S4b moved among the 591 existing kits**;
  - 572 rows with 0 where `rdr ≠ source`; integrity ok; FK clean.
- **The added row is correct.** `d_prop_randclassskill_val1 = 3` matches `Properties.txt` in the datamine mirror: code `randclassskill`, `val1 = 3`, `func1 = 36`, `stat1 = item_addclassskills`. The Hellfire Torch planner field carries the **rolled class**, and the +3 magnitude is the property's own `val1`. Storing it as its own DATAMINED input row is right under the anchor law.
  - *INFO-4:* it is filed under scale `d2_input_base_item`, but it is a Properties parameter, not an item base. It is still covered by R-D2S1's enumeration, so this is a label nuance only. A future `d2_input_property` scale would read more precisely; that would be a rule-text amendment, not a blocker.
- **gamora's hard-point finding: CONFIRMED on the inputs.** The rows store the verbatim planner values: Fire Bolt (36) **17**, Inferno (41) **1**, Enchant (52) **1**. legolas's sheet hard-coded 20 / 20 / 3. **The verbatim INPUTS govern, so v2 is correct.**
  - ⚑ **Consequence for the owed positive control:** the adapter's sheet derivation must reproduce legolas's sheet bit-exactly. **Until legolas re-issues it at 17 / 1 / 1, that control is expected RED on Fire Bolt / Inferno synergy and slvl terms.** Run it against the corrected sheet only, and record the re-issue's hash as the reference. A control against the uncorrected sheet would fail for a reason that is not the adapter's.

**The verdict is unchanged: BLOCK (narrow).** v2 still writes **`grade = 'EXACT'`** for the referent. Every ground in § (1) and § (2) above is untouched by v2. Regenerate **v3** with:
- `grade = 'CLOSE'`;
- the corrected deviation note (15 DISAGREE plus the categorical row, `eor_rank_total` consumed, 11/38 reach, 31 consumed / 51 unconsumed unstamped);
- the re-predicted J-S4b ROWSET.

`d2-fire-sorc-c14`'s **`d21dee9b…`**, the 572 rows and R-D2S1 are **approved as in v2**. elrond applies v3 after a narrow delta here.
