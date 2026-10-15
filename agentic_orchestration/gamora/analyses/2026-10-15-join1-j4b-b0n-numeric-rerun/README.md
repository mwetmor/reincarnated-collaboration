# JOIN-1 · J4b · the B0-N NUMERIC re-run: **PASS** on all three criteria

**Prereg:** engine `301e35c1`. **Instruments:**
- `gamora_join1_b0n_selfjoin_2026_10_06.py` (KP-305), UNMODIFIED;
- `gamora_join4b_b0n_d2_bind_2026_10_14.py`, engine `396b5757`;
- the § 4.7 v4 instrument, with pack v4 added to the B′ forbidden dirs, engine `a04a572a`.

**Where:** the dedicated worktree `reincarnated-engine-j4b-cert`. GD steps ran at `a04a572a`; the D2 bind and § 4.7 at `396b5757`. Heavy steps went through the courtesy wrapper.

**Pins:**
- corpus.db FILE `c7012de3134a1e64…`;
- J-S4b ROWSET `59099b7d…`, grade **CLOSE / MAPPED**;
- `d2-fire-sorc-c14` ROWSET `bbc2db89…`;
- pack v4 FINAL `dee7cf58…`. Its `RB-K-kit_id` row is NOT keyed on (packs gate WARN-1).

**Not a graded run.** The oracle ran from the sealed worktree `969fbd8d` (kc2 tree OID `7496a28a`) through the J-S8 emitter, unmodified, in dry run. `corpus.db` was read only: the harness worked on a scratch copy, and the D2 bind opened it `mode=ro`. Nothing was written.

| Criterion | Result | Evidence |
|---|---|---|
| **P1 · GD reproduces J-S8 7/7 at the new pin** | **PASS: 7/7 ROWSETs equal `f82807fb`, 25/25 cells complete**. The executes set TA-X-07/20/29/30 all reproduce | `R2-J4b/compare.json`, `run_manifest.json`, `grain_files_sha256.txt` (the grains, 44 MB, stay in the scratchpad) |
| P1b · the bound values equal KP-305 R2's | **HOLDS**: `bindings.json` minus its corpus path and tag is identical to `2026-10-06-join1-b0n-numeric-selfjoin/runs/R2/bindings.json`. The grade change reaches no binding | `R2-J4b/bindings.json` |
| **P2 · the D2 rows bind under the new grade** | **PASS** (detail below) | `d2_bind.json` |
| **P3 · no binding moves the GD configuration** | **PASS**: (a) P1 is 7/7; (b) every compared D2 operand is in layer `KIT:d2-fire-sorc` (53 of 53), with 0 in `LAW` / `WORLD` / `KIT:warlord`; (c) the GD bind path (the harness, `join1_b0n_hook`, the J-S8 emitter) never imports `join2_rulebook`, and the run's artifacts carry no reference to it | `d2_bind.json` (`layers_of_compared`); `R2-J4b/` |
| **§ 4.7 v4** (B′ now forbids the 3 pack v4 dirs and 3 v4 tools) | **ORACLE BYTE-IDENTICAL**: "HEAD fixed; A and B and B' pass" | `s47v4/`, `s47v4.stdout.txt` |

**P2 in detail:**
- **Inputs:** 597 / 597 rows read, all with rule `R-D2S1`, and 0 rows have `rdr ≠ source`. The transcribed Skills.txt constants equal the bound corpus rows (0 mismatches).
- **53 / 53 derivable pack v4 operands are EQUAL:**
  - every `sheet.*` operand: life 2,821, mana 1,032, Defence 3,017 / 3,267, block 11 / 3, resists 75 ×4, DR 18, absorb 8, FCR / FHR / FBR frames 8 / 8 / 9, clvl 99;
  - all 13 `blvl.*`, including Fire Bolt 20, Inferno 20 and Enchant 3 (KP-444);
  - all 10 `slvl.*` in the pack, including 46 / 46 / 29;
  - Fire Ball (raw 668.5–721.5, synergy +560 %, mana 27.5, missile);
  - Meteor (raw 3,007–3,117, synergy +200 %, radius, 60 / 30 frames);
  - the burning ground (bitrate 2,104–2,184, synergy +60 %, 705 frames, DamageRate 41);
  - Static Field; Frozen Armor (+105 %, 7,500 frames, freeze 75 → 18 / 12 / 9);
  - the buffs (BO 16 +80 % 180 s, BC 16 155 s, mana 7 / 11);
  - thorns 10; mana after kill 5; regen bonus 25; Warmth 342 %; Fire Mastery 345 %; item mastery 0; ManaRegen 120; double-fill stats 535 / 97.
- **Unequal: 0.**
- **20 pack operands are NOT-DERIVED by design**, each with its reason: belt and potion rows (C-13), policy rows (rotation, Static rule, on_struck order, belt policy), lever settings, the row-25 map, identity rows, and `kit_id` (WARN-1).
- **Derived but absent from the pack:** `slvl.blaze`, `slvl.fire_wall`, `slvl.telekinesis`. They are prerequisites and are never cast.

**The stale label, stated:** the KP-305 harness prints `APPROX-CEILING: J-S4b mapping grade NULL (owed at J4a)`. **That string is the instrument's historical text.** The grade of record is **CLOSE** (KP-443), and every figure here carries the CLOSE grade. The harness was not edited, so it remains the KP-305 instrument byte for byte.

**B0-N (base note § 8 (1)) is DISCHARGED numerically:** P1 7/7, P2 53 / 53 equal, P3 holds.
