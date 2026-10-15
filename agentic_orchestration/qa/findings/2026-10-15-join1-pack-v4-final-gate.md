# Finding — 2026-10-15 — JOIN-1 J4b · packs gate: `kc2-rulebook-pack-v4` FINAL (`dee7cf58…`)

**Reviewer:** jack-ryan (DEV-MODE packs gate, BLOCK authority; before drax binds)
**Severity:** PASS-WITH-NOTES (0 BLOCK, 1 WARN, 6 INFO). **drax may bind `dee7cf58`.**
**Target:** engine `03502344` (prereg delta) · `bcc3ab03` (cut) · `e28bbbc8` / `9483bfe9` (MIGRATION); collab `737395a99` + `20a5736c1`
**Developer:** star-lord
**Principles applied:** 1, 3, 5

## Verified independently

| Check | Result |
|---|---|
| **Prereg before cut; digests** | Prereg committed 23:32:39 → receipt stamp `233315` → cut committed 23:33:34; the prereg is unchanged at HEAD. Pack `dee7cf58…` and manifest FILE `724dc54a…` re-derive. All 16 member FILE / ROWSET digests equal prereg § 3. Every file equals its `bcc3ab03` blob. Tool FILE `621aa8ae…` = the prereg's |
| **Carried members** | 14/16 byte-identical to re-cut `022a7068` (only `anchor_d2_gd` and `meta` differ); 9/10 v3 members byte-identical (only `meta`). The first cut `48c6d891` stays on disk |
| **KIT vs the verbatim C-14 inputs** | **Hard points:** gamora's stamping **v3** (collab `d2e28cbc6`) `profile.skills` rows (86) + its 24 `skillProgression` rows (FBolt +3, Inferno +19, Enchant +2) give exactly the pack's 13 `blvl` rows (FBolt 20 / Inferno 20 / Enchant 3 / FB, Met, FM 20 / the 1-pointers; Σ 110). **slvl** 46/46/46/46/46, Warmth 27, Enchant 29, FA/Static/Teleport 16 and **synergies** +560 / +200 / +60 equal legolas stage 6's `FINAL_charms_BO_BC_FA` section. **Sheet rows** (life 2821, mana 1032, block 11/3, DR 18, FCR/FHR/FBR frames 8/8/9, absorb 8, resists 75, clvl 99, vit/energy 535/97) are equal. **DATAMINED skill rows** (Fire Ball 668.5/721.5 @46, Meteor 3007/3117, pyre 2104/2184, FM 345, Warmth 342) equal gamora's `primary_rows.json` (FILE `0ade1f7f`, as pinned) |
| **ANCHOR rows** | `r_HP` = 243,295 / 6,000.5 = `40.54578785101241`, bit-equal. `r_DMG` 78.5835 / worst 97.0646 / use 46.9787 are bit-equal to legolas `r_dmg.json@a83290a69` `R1_alvl85_all` (see INFO-5). `coldeffect` −33 for champion-hero / boss / nemesis, trash frozen. The three `tables/*` FILE digests equal gamora's committed tables (collab `0cd2c3570`; emitter engine `833fee62`). `anchor_m_per_yd` = 1.2 JUDGED, with the printed sensitivities and the KP-441 pointer |
| **GD binder** | The pinned v0 `load_operands(JOIN)` returns **35** operands, encoding-equal to v3's. No v4 row is an OPERAND |
| **D2 rows JOIN-only** | `load_operands` and `load_layer` (kit, anchor, hooks) refuse `ORACLE`, `PLAY`, `join`, `""` and `None`: **20/20, run by me** |
| **§ 4.7 v4** | Attempt 1 is NO VERDICT: HEAD moved `bcc3ab03` → `5b001f88`, gamora's commit. It is kept and not quoted. **Attempt 2** ran in a dedicated worktree (`reincarnated-engine-v4final-s47`, HEAD fixed at `bcc3ab03`): pinned, A / B / B' pass, ORACLE BYTE-IDENTICAL. All engine reads came from that worktree (0 from the shared tree), and 0 pack paths appear in either ORACLE child's `opened` list. **Valid** |
| **Controls NC-V4F-a…f** | Raw logs match the prereg § 4 predictions: table-drift 1 difference; value-drift `RB-K-life_d2`; table-digest `RB-A-anchor_ar_eq_table`; yard-drift `RB-A-anchor_m_per_yd`; d `member_failures` on the contact table; e 10/10 refusals |

## Rulings on star-lord's open notes

1. **Sheet pin `7c1ea68d` vs the live sheet.** **Values sound, no re-cut.** I flattened both: stage 6 (`a118544b`, collab `f97161330`) is a **strict superset** of stage 1. **0 existing leaves changed or removed**; it adds only the `FINAL_…` section. Every pack pointer into `7c1ea68d` therefore resolves to the same value in the live sheet, and the pinned bytes are retrievable as the blob at `0ac88e6ef`. *Owed:* the tool reads the pin from the blob (`git show 0ac88e6ef:…`) so that it re-runs, or the next cut re-pins to stage 6. Record which in MIGRATION.
2. **No KP-444 citation in the pack.** **Acceptable for this cut.** The `blvl` rows already derive from `profile.skills` + `skillProgression` (provenance "110 = 98 + 12 quest"), and the values equal KP-444 exactly, as I checked against stamping v3. The citation is carried by `9483bfe9` and `kp444_check.json`. *Owed:* a `meta` citation at the next cut.
3. **The B' list doesn't name v4.** Same class as my earlier INFO-2 / INFO-V2-2. The `opened` scan shows 0 opens. *Owed (gamora):* add the three v4 pack dirs and `kc2_rulebook_pack_v4{,_recut,_final}.py` at the next instrument touch.
4. **Prereg "15 of 16".** An erratum; the true count is 14 of 16. The predictions were exact, and the erratum is recorded in the evidence. **Closed.**
5. **INFO-V3-1.** Still owed; `offense_da` is carried byte-identical. Carry it to the next `offense_da` touch.

## Findings

**WARN-1 · `RB-K-kit_id` = `"d2-fire-sorc"`, with provenance "kits-export d2-fire-sorc.json".** KP-442 put the C-14 rows under the **new** `d2-fire-sorc-c14` and found (F4) that `d2-fire-sorc`'s stamped rows are D2R web values, not 1.13. This cut predates KP-442 by about a minute. No consumer reads this row today (grep of the engine `join2_rulebook` and godot `kc2_play/join`), and every KIT value points to C-14, C-13 or 1.13 sources, so nothing is wrong in substance. But the pack of record names the F4-tainted kit. **drax must not key on it. Fix it at the next cut.** **Cite:** #8, #71.

**INFO-1:** `kp444_check.json` labels the live sheet `a118544b` "stage 5". It is stage 6 (`f97161330`); stage 5 (`b4d5e2920`) has different bytes.

**INFO-2…INFO-6:** notes (1), (2), (3) and (5) above, plus INFO-5. `r_dmg.json` names 97.06 `r_DMG_primary`, while the pack's primary is mean÷mean 78.58 (ADDENDUM-6/-9; documented by `RB-A-anchor_r_dmg_arm_default`). Anyone reading legolas's file directly gets the opposite label.

## Action
- [ ] drax: bind `dee7cf58`. Do not key on `RB-K-kit_id` (WARN-1).
- [ ] star-lord, at the next cut: WARN-1 (`d2-fire-sorc-c14`); a KP-444 `meta` citation; re-pin to stage 6 or read the blob (note 1); INFO-V3-1; correct INFO-1.
- [ ] gamora: add v4 to B' (note 3).
- [ ] Matt: none.

## References
- Engine:
  - `src/reincarnated/export/kc2_rulebook_pack_v4_final.py`
  - `…/math/2026-10-15-kc2-rulebook-pack-v4-final-prereg-delta.md`
  - `src/reincarnated/output/kc2-rulebook-pack-v4-20261014_233315/` (+ re-cut `…_232246`, first `…_230813`, v3 `…-v3-20261008_102954`)
- Collab:
  - `star-lord/analyses/2026-10-15-join1-rulebook-pack-v4/final/`
  - legolas `…/2026-10-14-join1-c14-sorc-build-file/sorc_build_sheet.json` @ `0ac88e6ef` / `b4d5e2920` / `f97161330`
  - `…/2026-10-01-join1-j4b-d2-fire-sorc/primary_rows.json@4eda5de34`
  - `…/c13-enemy-anchor/r_dmg.json@a83290a69`
  - gamora `…/2026-10-14-join1-j4b-d2-stamping/stamping_table.json@d2e28cbc6`
  - `…/2026-10-14-join1-j4b-build/tables/`
- Ledger rows KP-436/437/439/441/442/443/444
