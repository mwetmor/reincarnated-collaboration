# Finding — 2026-10-15 — JOIN-1 J4b · packs gate: `kc2-rulebook-pack-v5` (`c403ca5d…`)

**Reviewer:** jack-ryan (DEV-MODE packs gate, BLOCK authority)
**Severity:** PASS-WITH-NOTES (0 BLOCK, 1 WARN, 5 INFO), gated **as cut**. The carried contact-table defect is WARN-1.
**Target:** engine `5c03c3c7` (prereg) · `a1016c9a` (delta) · `d3f71b97` (cut) · `886dfcbf` (MIGRATION); collab `bacf73940`
**Developer:** star-lord
**Names:** gamora ADDENDUM-13 CORR-2 § 5 (engine `c99ac644`)
**Principles applied:** 1, 3, 5

## Verified independently

| Check | Result |
|---|---|
| **Prereg before cut; digests** | Prereg 02:32:56 → delta 08:17:51 → receipt stamp `081830` → cut 08:18:46; both docs are unchanged at HEAD. Pack `c403ca5d…` and manifest FILE `cb4bba48…` re-derive. All 17 members' FILE / ROWSET digests equal delta § 3. Every file equals its `d3f71b97` blob. Tool FILE `24315c73…` = the delta's. G-10 is 20 files |
| **Carried members** | v3's 9 and `tables/*` are byte-identical to v4. Changed: `anchor_d2_gd`, `hooks_j4b`, `kit_d2_fire_sorc`, `meta`; new: `world_l21` |
| **G-5b (my own diff)** | Over all **107** v4 rows (73 KIT + 24 ANCHOR + 10 HOOK), the decoded value and grade are identical except the two declared exemptions: `kit_id`, and `oculus_teleport_on_struck`, whose `stream` string moved to `oculus:d2-fire-sorc-c14`. That is 105 compared and 0 diffs, matching his G-5b. No v4 row is missing. The fields that differ on carried rows are only `scope`, the sheet `points_to` (stage 6 `a118544b`) and the declared `potion_class_factors` note |
| **`kit_id` fix (my v4 WARN-1)** | **Closed.** The value is `d2-fire-sorc-c14`, DECLARED-INVENTED, pointing to KP-442 (`f4793ea7c`) and to my WARN-1. The layer and scope strings follow it; the member path is kept |
| **WORLD `world_l21.json` + `RB-HOOK-L-21`** | All 8 `RB-W-l21_*` rows equal CORR-2 § 5 row for row: `_qualifying` (full dict compared), `_divisors` [16,8,4], `_divisor_sensitivity_2h`, `_polarity_50` "odd_gets", `_rule_75`, `_softhit` [19,128], `_length_frames` 8, `_attack_on_gethit` "reset", with the grades as stated. `RB-HOOK-L-21 monster_hit_recovery`: values {gd, d2-world}, default d2-world, JUDGED, LAW layer |
| **New KIT rows** | **Stream ids:** `RB-K-stream_ids` equals the `d2/streams.py@c99ac644` form (`KIT_ID = "d2-fire-sorc-c14"`, the 7 ids, LAW string) + `gethit:warlord`. **Stamina:** `stamina_max` 1179 (= ⌊603·1.8⌋ + 94; no-BO 697) and `stamina_drain_256` 24 (= max(1, 2·20·1·60//100)) equal stage 8 (`c14_stage7.json`, FILE `30f4a511` @ `cb7b01319`). **Pyre offsets:** all 18 (dx, dy) equal stage 7 element by element, and CORR-2 § 5. **`velocity_walk_run`** {726, 1026, 21, [121,171]} equals stage 7 `movement`. **`res_uncapped`** {fire 90, cold 125, light 125, poison 125} equals the sheet (key `light` verbatim per § 5; see INFO-1) |
| **GD binder** | The pinned v0 `load_operands(JOIN)` returns **35**, encoding-equal to v3 |
| **JOIN-only** | `load_operands` plus `load_layer` on KIT / WORLD / ANCHOR / HOOK refuse all 5 non-JOIN configs: **25/25, run by me**. JOIN reads `l21_length_frames` 8, `stamina_max` 1179 and `kit_id` `d2-fire-sorc-c14` |
| **§ 4.7 v4** | Run in the dedicated worktree, HEAD fixed at `d3f71b97`; pinned; A canonical-equal (`f04ef6d0`); B 0 changed; B' pass; **ORACLE BYTE-IDENTICAL**. 0 pack paths in either ORACLE child's `opened` list. The sealed child's only worktree reads are the witness `sitecustomize`. B' now lists the v4 dirs and tools (see INFO-3) |
| **Controls NC-V5-a…i** | The raw logs match delta § 4: the self-test reports 1 diff; value / table-digest / yard / offset / stamina each give 1 failure on the named row; stage7-digest HALTs at the pin; d `member_failures`; e 15/15 |

## Findings

**WARN-1 · KNOWN DEFECT carried byte-identical from v4.** `tables/physical_contact_table.json` (FILE `34496817`, gamora's emission at `833fee62`) has **no `defaultweaponattack.dbr` slot**, and that produces a "runs" FAIL on 10/25 cells.
- **v5 is faithful to its source.** The table equals gamora's committed digest. It is the **source** that is defective.
- **Ruling:**
  - drax may bind v5 for development and for the rows this gate certifies;
  - **no graded J4b / B0-N result that runs through the contact table may be quoted on v5.** v5.1 is required for those.
- **Self-finding:** my v4 gate (`84cafd696`) certified this table by digest identity to gamora's emission only, not by slot coverage. The defect therefore also lives in v4 FINAL `dee7cf58`, and the same restriction applies to anything bound to v4.

**v5.1 CAN be a narrow delta**, provided all of these hold, each pre-stated in a v5.1 prereg delta:
- (a) the two AR tables are byte-identical to v5;
- (b) the contact-table row diff is exactly the added `defaultweaponattack.dbr` slot rows, enumerated, with every other slot row identical;
- (c) `anchor_d2_gd` changes only in `RB-A-physical_contact_table`'s value FILE, and in the three table rows' gamora-`manifest.json` pointer FILE where her manifest moves;
- (d) every other member is byte-identical to v5, and `meta` changes only in supersedes, inputs and notes;
- (e) G-5b is extended to all v5 rows, with only those rows differing;
- (f) fail-first: the 10/25 "runs" FAIL is reproduced on v5 and GREEN on v5.1;
- (g) § 4.7 is re-run in the dedicated worktree; the GD binder is 35; controls a–i are carried, plus one new contact-slot control.

**INFO-1 · Two spellings in one member.** `res_uncapped` uses `light` (verbatim, matching engine `d2/sheet.py` `RES`), while `sheet.res.lightning` uses `lightning`. Record the alias in `meta` or unify at the next cut, so that a key join cannot silently miss.

**INFO-2 · Unnamed scope change.** Prereg § 2.4 predicted `anchor_d2_gd` and `hooks_j4b` byte-identical. The delta names the new hook row and the table-pointer commits, but not the `scope` string change ("pack …-v4" → "-v5") on every carried ANCHOR and HOOK row. G-5b permits it. Name it next time.

**INFO-3 · B' lacks v5.** B' now carries the v4 dirs and tools but not the v5 pack dir or `kc2_rulebook_pack_v5.py` (owed by gamora). The opened scan shows 0 opens.

**INFO-4 · INFO-V3-1 still owed** (`offense_da` carried).

**INFO-5 · v4's INFO-1 erratum** (the "stage 5" label) is recorded in v5 `meta.sheet_pin`. Closed.

## Action
- [ ] drax: bind v5 for development; quote no contact-table-dependent graded result until v5.1 (WARN-1).
- [ ] gamora: re-emit `physical_contact_table` with the `defaultweaponattack.dbr` slot; add v5 to B' (INFO-3).
- [ ] star-lord: v5.1 as a narrow delta under (a)–(g); INFO-1, INFO-2, INFO-4 at the next cut.
- [ ] Matt: none.

## References
- Engine:
  - `src/reincarnated/export/kc2_rulebook_pack_v5.py`
  - `…/math/2026-10-15-kc2-rulebook-pack-v5-prereg.md`, `…-prereg-delta.md`
  - `src/reincarnated/output/kc2-rulebook-pack-v5-20261015_081830/` (vs v4 `…_233315`, v3)
  - `src/join2_rulebook/d2/streams.py@c99ac644`, `d2/sheet.py@c99ac644`
  - ADDENDUM-13 CORR-2 (`c99ac644`)
- Collab:
  - `star-lord/analyses/2026-10-15-join1-rulebook-pack-v5/`
  - legolas `c14_stage7.json@cb7b01319`, `sorc_build_sheet.json@f97161330`
  - my v4 gate `84cafd696`
