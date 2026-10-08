# Finding — 2026-10-08 — JOIN-1 KP-371/372/374 `kc2-rulebook-pack-v1` RE-CUT, narrow delta Gate-2

**Reviewer:** jack-ryan (DEV-MODE, narrow delta Gate-2; conductor gandalf)
**Severity:** PASS-WITH-NOTES (INFO only; no WARN, no BLOCK)
**Target:** engine `115cc1b1` (prereg delta) · `375f9632` (re-cut) · `06d00fb6` (MIGRATION + AGENT_STATE); collab `61f73c29b` (evidence)
**Developer:** star-lord
**Delta to:** `11157a905` (gate on `0b1feb31`)
**Principles applied:** 1, 3, 5

## What I found

I checked everything with my own script against the committed blobs, not against the tool's checker.

| Check | Result |
|---|---|
| Prereg delta before the cut | Delta committed 08:56:19 → receipt stamp `085655` → cut committed 08:57:15. The delta and the first prereg `334fa5e8` are unchanged at HEAD. The first cut's tool `4088f568` is not edited. The receipt cites `115cc1b1` |
| Digests | Pack `0c11ef63…` and manifest `65992b1f…` re-derived. `offense_da` `0d3396b2…` / `769c4744…` and `meta` `f7427c37…` / `36c2bd87…` equal P-R-1…3 to the full hex. The tool is FILE `f0181034…`. Every pack file equals its `375f9632` blob. G-10 = exactly the 10 named paths |
| Renames are pure | Row ids and order are identical to `0b1feb31`. Under the rename map (`p→pth`, `p_at_da_plus_e_l→pth_at_da_plus_e_l`, `level_margin_da→da_margin_after_e_l`, `body_class→record_dir_class`), **every** old value is encoding-identical (bits and repr) on all 199 rows: **0 differences**. The three CONST rows are identical. The only additions per row are exactly `{s2_body_class, class_rules_disagree, level_margin_levels}` |
| Everything else | The five carried members are byte-identical to `0b1feb31`, and therefore to v0. The only pointer changes are the declared ones: MEASURED rows add `da_mod_pct_total` to `columns` plus `mod_pct`, and SOURCED rows gain a 3rd pointer to `s2_classes@afd83b8db` (FILE `d16521fc…`, which I re-hashed from the blob). `meta` adds only `supersedes_cut` and `crit_source_prohibition`. The census is unchanged. The receipt is PASS, with G-2 at 1,213 checks and 0 failures |
| WARN-1 (`body_class`) | **Closed.** `body_class` is absent from `value_fields`, and `meta` mentions it only as RETIRED. Both rules are labelled DECLARED and "NOT GD's monsterClassification", and gamora's rule cites `6b35abb9`. `s2_body_class` equals her class on 122/122 SOURCED rows. Her rule, which I transcribed independently, reproduces `measured_class_counts_74` exactly on the 74 MEASURED rows. `class_rules_disagree` = XOR(summon), and is true on **exactly 2 rows**: `bossskills/pets/loghorrean_void|154` and `witchgodguardian_sentinel_crystal|159` |
| `level_margin_levels` | Bit-exact against `(DA_STAR − da) / (12·(1 + mod/100.0))` on **all 196 rows**. SOURCED `mod` is `s2_classes.mod_pct`, and the result is bit-equal to her `level_margin` on 122/122. MEASURED `mod` is the sealed CSV's `da_mod_pct_total` (FILE `5c55998d`) |
| The minima he reports | SOURCED min 17.626229370123742 (`boss&quest/humanascendant_mindthief_01|155`). Summon min (her 25) **21.082147881009732** (`swampcrab_c01_summon|152`). Whole-path min **17.552981214343053**, on MEASURED `hero/springscrab_h01|152`, tied with `springscrab_h04|152` per the prereg delta. All confirmed |
| G-8 (§ 4.7 v4) | Run 1 at `375f9632` is NO VERDICT: HEAD moved to `5655123c`. It is kept on record and not quoted. Run 2 at `5655123c`: HEAD fixed, instrument pinned, A / B / B' pass, ORACLE BYTE-IDENTICAL. `375f9632` is an ancestor of `5655123c`. The diff between them is `src/join2_rulebook/**` plus one test, which is outside the oracle import closure (limb B reports 0 files changed since the seal). The two ORACLE children's `opened` lists (631 and 720 entries) contain 0 rulebook-pack paths. **Valid** |
| INFO-1 | **Closed.** The run-1 record now carries `instrument_pinned: false` and `limb_Bprime_pass: false`, and the original reason is preserved as `reason_as_first_recorded` |
| INFO-3 | **Closed.** Raw logs are committed for NC-V1R-a/b/c-d and for the first cut's NC-V1-a/b. The first cut's NC-V1-c/d were never captured, and that is stated; acceptable. NC-V1R-b names one row on all 4 failures, including `level_margin_levels`, as predicted |
| Consumers | No reference to the re-cut pack or its tool anywhere in `simulation/**`, `join2_rulebook/**`, godot `kc2_runtime` or `kc2_play/src`. Nothing is pinned to it yet |

## Notes

**INFO-R1 · On MEASURED rows, `level_margin_levels` is informational, but the field's meaning does not say so.** The value_fields text reads "the levels of level-rule error that would flip the verdict". MEASURED rows carry no level-rule error, as prereg delta § 1 itself states. The whole-path minimum, 17.553, sits on MEASURED rows. A consumer that takes `min()` over the member would therefore report a MEASURED figure under a frame that does not apply to it. **Cite:** Discipline #82 (a figure carries the population it ranges over). **Action:**
- gamora's guard takes this minimum by `source == "SOURCED"`, or reports it with its source.
- star-lord adds "MEASURED: informational" to the field meaning at the next cut. No re-cut is needed for this alone.

**INFO-R2 · The summon minimum is 21.0821, not ≥ 21.1.** "≥ 21.1" is true only after rounding to one decimal. collab `afd83b8db`'s "margin >= 21.1 levels" is false at exact precision. star-lord recorded this correctly. **Action:** gamora corrects her wording to "≥ 21.08" (or "21.1 at 1 d.p.") at her next record touch. **Cite:** Discipline #11.

**INFO-2 (from `11157a905`) · Still open; gamora's.** The B' `forbidden_dirs` in both re-cut runs still list only the v0 pack and tool. The v1 pack paths (both cuts) and the v1 tools should be added in her `PACK_PIN` commit.

**INFO-5(b) · Carried and declared in the prereg delta.** Cut mode still writes the pack before G-3, G-4, G-7 and G-9 are evaluated. No action.

## Action
- [ ] gamora:
  - INFO-R1: take the margin minimum by source in the guard and its reports;
  - INFO-R2: correct the wording in her record;
  - INFO-2: add the v1 paths to `forbidden_dirs` in the `PACK_PIN` commit.
- [ ] star-lord: INFO-R1, add "MEASURED: informational" to the field meaning at the next cut.
- [ ] Matt: none.

## References
- Engine:
  - `src/reincarnated/export/math/2026-10-08-kc2-rulebook-pack-v1-recut-prereg-delta.md`
  - `src/reincarnated/export/kc2_rulebook_pack_v1_recut.py`
  - `src/reincarnated/output/kc2-rulebook-pack-v1-20261008_085655/`
  - `…/kc2-rulebook-pack-v1-cut-receipt-20261008_085655.json`
  - `…/kc2-rulebook-pack-v1-20261008_084024/` (superseded cut, used for the comparison)
- Collab:
  - `agentic_orchestration/star-lord/analyses/2026-10-08-join1-rulebook-pack-v1/recut/`
  - `…/v1_gate_evidence.json`
  - `…/gamora/analyses/2026-10-08-join1-pj25-step2/run-edition-IV/s2_classes.json@afd83b8db`
- Sealed: `data/kc2/pm4o_oa_da.csv` @ `969fbd8d`
