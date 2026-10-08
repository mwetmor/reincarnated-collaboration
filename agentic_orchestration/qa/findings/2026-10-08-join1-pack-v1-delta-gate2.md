# Finding — 2026-10-08 — JOIN-1 KP-368 `kc2-rulebook-pack-v1` delta Gate-2

**Reviewer:** jack-ryan (DEV-MODE, delta Gate-2; Run JOIN-1, conductor gandalf; ledger KP-368 / KP-370)
**Severity:** PASS-WITH-NOTES (1 WARN, 5 INFO; no BLOCK)
**Target:** engine `334fa5e8` (prereg) · `d5793a12` (cut) · `2318cd4b` (MIGRATION + AGENT_STATE); collab `d4dbc182a` (gate evidence)
**Developer:** star-lord
**Principles applied:** 1 (math before code / prereg before cut), 3 (cross-seam impact), 5 (severity matters)

## What I found

I re-derived every load-bearing claim with my own script. I did not use the tool's checker, apart from its loaders, which I exercised directly.

| Claim | Independent result |
|---|---|
| pack `0b1feb31…`, manifest FILE `ae9fe7c3…` | **Re-derived exactly** from the member bytes under PACK_DIGEST_LAW |
| P-V1-3 member FILE / ROWSET (all 7) | **All equal.** `offense_da` `e1f2e0de…` / `24ae737d…` and `meta` `346fa0d0…` / `f7cf1066…` match to the full 64 hex |
| v0's five members byte-identical | **Yes**, against the v0 pack on disk **and** against the blobs at v0's cut commit `c5b72bbf`. v0 re-derives to `974ff092` |
| On-disk pack = committed blobs | **Yes**: all 8 pack files equal their `d5793a12` blobs |
| Census | 199 rows = 196 `OFFENSE-DA` + 3 `CONST`; 74 MEASURED / 122 SOURCED; CERTAIN 196/196 |
| Population | The 196 pairs equal the J-S8 path read **from the 25 `JOIN_*.json` blobs at collab `07d78e729`**. The SOURCED set equals `s2_apply.per_row`, read **from the blob at `1641e2dec`**, not from the working tree. MEASURED ∩ SOURCED = ∅ |
| MEASURED rows (74) | `da` bits equal the sealed CSV `DA` (FILE `5c55998d…c564`, re-hashed). `level` = `spawn_level`. Classification and threat tier are verbatim. Line pointer = CSV index + 2 |
| SOURCED rows (122) | `da`, `p` and `p_at_da_plus_e_l` bits equal `s2_apply`; `level` = `L`; the provenance string is exact; `level_margin_da` = `DA_STAR − (da + E_L)` exactly |
| p recomputation | I recomputed all 196 `p` values and 122 `p(da+E_L)` values in my own child process, using `PYTHONPATH` = sealed `969fbd8d` src, the sealed `threat.probability_to_hit` and `-P` with no bytecode. **All bit-equal**, with 0 failures. Path min p = 105.9822630137391, bit-equal to `s2_apply.path_min_p`. p(DA\*) = 100.0. The sealed tree is clean after the run, and its kc2 tree is `7496a28a` |
| Constants | `DA_STAR` and `E_L` are bit-equal to `s2_apply`; `PLAYER_OA` = 3259.0 |
| Prereg before cut | Prereg committed 08:39:57. Receipt stamp `084024` (08:40:24). Cut committed 08:40:43. The prereg is unchanged `334fa5e8`..HEAD. The tool refuses to cut without `KC2_RB1_PREREG_COMMIT` and on any prereg drift. The receipt records `334fa5e8` |
| Cut commit scope (G-10) | `git show --stat d5793a12` = exactly the tool, the 8 pack files and the receipt. MIGRATION's tool pin `4088f568…` matches the file |
| Loader refusals | I exercised both loaders myself. They refuse `ORACLE`, `PLAY`, `join`, `""` and `None` (10/10). JOIN loads 196 rows and 3 constants |
| No ORACLE/PLAY read path | 0 references to v1 in the engine's tracked tree outside the export seam's own files. 0 references in the sealed tree. 0 references in godot `kc2_runtime`, `kc2_play/src`, `main.tscn` and `project.godot`. Both ORACLE children's `opened` lists (631 and 720 entries) contain no v1 pack or v1 tool path. The only matching strings are the instrument's own graded-output writes into the collab evidence dir |
| Controls NC-V1-a…d | The recorded observations match the prereg § 4 predictions. NC-V1-a's row is CSV line 2, which is the first MEASURED row |

## Findings

**WARN-1 · `body_class` is labelled as a declared rule, but a second, different declared rule already ships under the same name.**
- **Labelling: yes.** The member's `value_fields` meaning says "DECLARED RULE … Not a GD monsterClassification", and so does prereg § 1.
- **Collision.** gamora's step-2 reporting rule (engine `6b35abb9`, `body_class()`; the basis of collab `afd83b8db` "summons (25 rows) class-uncalibrated") is a different taxonomy:
  - gamora's classes are summon / nemesis / boss_quest / bounty / hero / common, and her summon test is `_summon` **or `/pets/`**;
  - star-lord's rule uses the directory plus `+summon` on `_summon` only.
- **Measured over the pack's 196 rows:** gamora's rule gives **25** SOURCED summons. Star-lord's `+summon` gives **23**. The two disagree on `bossskills/pets/loghorrean_void.dbr` and `…/pets/witchgodguardian_sentinel_crystal.dbr`.
- **Consequence.** The guard is named as a reader of `body_class`. If it labels "class uncalibrated" from the pack, it will not reproduce the rows gamora reported.
- **Cite:** Disciplines #8 and #71; ADR-004.
- **Not BLOCK**, because nothing consumes v1 until the `PACK_PIN` commit.
- **Action:** settle this during the field-name confirmation that is already owed. Either:
  - rename the field (e.g. `record_dir_class`) so it cannot be read as the INFO-S2a class; or
  - adopt one rule for both seams.

  Either way, re-cut v1 **before** the `PACK_PIN` move, as the prereg already provides.

**INFO-1 · The 'NO VERDICT' handling is sound. The reason recorded for it is incomplete.**
- **The verdict itself is sound:**
  - The verdict rule requires HEAD fixed AND limbs A, B and B'.
  - Run 1 was withheld, not quoted, and kept on record.
  - Run 2 at `47c5c94e` is valid evidence for the cut. `d5793a12` is an ancestor of `47c5c94e`, so the pack is present at that commit.
  - `d5793a12..47c5c94e` touches only `src/join2_rulebook/**`, three `scripts/**` files and tests. Limb B reports 0 import-closure files changed between the seal and HEAD.
  - The s47-v4 instrument diff is a control-only addition (`nc8k`) that is off the graded path.
- **What the record leaves out:**
  - Run 1 *also* had `instrument_pinned=false` and **B' FAIL**. gamora's uncommitted witness-hook and instrument edits were live in the working tree at the start of the run.
  - Both runs therefore used instrument blob `5fae93ac`, not the cut-time blob `3267badf`.
  - `v1_gate_evidence.json` `run_1.reason` names only "HEAD moved".
- **Cite:** Disciplines #75 and #81.
- **Action:** star-lord adds the B' and instrument-pin facts to the run-1 record at the next touch.

**INFO-2 · The B' witness does not guard v1.** `forbidden_dirs` in s47 v4 names the v0 pack and the v0 tool only. G-8's "0 pack opens" for v1 rests on the post-hoc scan of the `opened` lists, which I re-ran and which holds. The live witness would not turn RED on a v1 open. **Cite:** Discipline #75. **Action:** gamora adds the v1 pack dir and `export/kc2_rulebook_pack_v1.py` to `forbidden_dirs` in the `PACK_PIN` commit. The port needles are substrings, so they already cover v1.

**INFO-3 · The controls' raw outputs are not committed.** NC-V1-a…d exist only as one-line `observed` strings. Receipts for the dry-run controls are not in the evidence dir. **Cite:** Disciplines #7 and #80. **Action:** commit the control receipts next to the gate evidence.

**INFO-4 · P-V1-2/3 are pins measured by the dry run, not blind predictions.** This is the declared S1 discipline. What they add as evidence is the tool's determinism together with the prereg-before-cut ordering, which I verified. No action.

**INFO-5 · Two by-construction artefacts of the design, recorded here for consumers. Neither needs action unless the design changes.**
- **(a) Carried members still say v0.** The carried members self-identify as `"pack": "kc2-rulebook-pack-v0"` because they are byte-identical. Readers must take the pack's identity from `manifest.json` or `meta.json`.
- **(b) A late-gate failure in cut mode would still write a pack.** Cut mode writes the pack *before* G-3, G-4, G-7 and G-9 are evaluated. A failure at those gates would leave a FAIL-verdict pack on disk, not a HALT. "Nothing is written" holds for G-2 only. None of these gates fired.

## Action
- [ ] star-lord + gamora: WARN-1. Resolve `body_class` during the field-name confirmation; re-cut before `PACK_PIN` if the field is renamed or its rule changes.
- [ ] star-lord: INFO-1 (complete the run-1 reason), INFO-3 (commit the control receipts).
- [ ] gamora: INFO-2 (add v1 paths to the B' `forbidden_dirs` in the PACK_PIN commit).
- [ ] Matt: none. Nothing here is BLOCK or ESCALATE.

## References
- Engine:
  - `src/reincarnated/export/kc2_rulebook_pack_v1.py`
  - `src/reincarnated/export/math/2026-10-08-kc2-rulebook-pack-v1-prereg.md`
  - `src/reincarnated/output/kc2-rulebook-pack-v1-20261008_084024/`
  - `src/reincarnated/output/kc2-rulebook-pack-v1-cut-receipt-20261008_084024.json`
  - `src/reincarnated/export/MIGRATION.md`
  - `6b35abb9` (gamora's `body_class`)
- Sealed: `/Users/admin/Games/reincarnated-engine-join1-v311` (`969fbd8d`), `data/kc2/pm4o_oa_da.csv`
- Collab:
  - `agentic_orchestration/star-lord/analyses/2026-10-08-join1-rulebook-pack-v1/` (`v1_gate_evidence.json`, `s47v4/`, `s47v4-r2/`)
  - `…/gamora/analyses/2026-10-08-join1-pj25-step2/run-edition-IV/s2_apply.json@1641e2dec`
  - `…/2026-10-07-join1-j2-gate2-owed/dynamic/JOIN_*.json@07d78e729`
