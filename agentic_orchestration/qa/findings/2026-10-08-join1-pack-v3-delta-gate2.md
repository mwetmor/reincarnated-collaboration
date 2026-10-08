# Finding — 2026-10-08 — JOIN-1 KP-381/382/383 `kc2-rulebook-pack-v3` delta Gate-2

**Reviewer:** jack-ryan (DEV-MODE delta Gate-2, before gamora's `PACK_PIN` → v3; conductor gandalf)
**Severity:** PASS-WITH-NOTES (INFO only)
**Target:** engine `c795a1c2` (prereg) · `e0cd5f74` (cut) · `c55fbce6` (MIGRATION + AGENT_STATE); collab `6404d775f` (evidence)
**Developer:** star-lord
**Source:** gamora step 2b (engine `7a8fc0f3` / `d7561387`; collab `910048891`; the other jack-ryan's GO at `b6cf4e94e`)
**Principles applied:** 1, 3, 5

## What I found

| Check | Result |
|---|---|
| **(a) Prereg before cut; digests** | Prereg committed 10:29:24 → receipt stamp `102954` → cut committed 10:30:10. The prereg is unchanged at HEAD. Pack `2713e4cd…` and manifest FILE `fc3537f0…` re-derive. `offense_da` `21f5ae86`/`a74e9622`, `offense_da_population` `a377e04e`/`cfa9cda6` and `meta` `612847bb`/`8210961a` equal § 3 to the full hex. The 7 carried members are byte-identical to v2. All files equal their `e0cd5f74` blobs |
| **(b) Rows** | All 199 v2 rows (196 + 3 CONST) are canonical-JSON identical in v3; 251 rows in total. `value_fields` are unchanged. The header differs only in `pack`, `format`, `read_rule`, `evidence_step2b` and `header_amendments_v3`. The 52 new pairs are exactly s2b's new set. **5 MEASURED:** `da` is bit-equal to the sealed CSV `DA` (FILE `5c55998d`) and to S2b-MEAS `table`; `pth` is bit-equal to `p_table`; level and classification are verbatim; `level_margin_levels` is bit-exact from `da_mod_pct_total`. **47 SOURCED:** `da`, `pth`, `pth_at_da_plus_e_l` and `level_margin_levels` are bit-equal to S2b-CLASS; `L`, `body_class` and the CERTAIN verdict match; `da_margin_after_e_l` is exact; the provenance string is exact. I recomputed all 52 `pth` values and 47 `pth(da+E_L)` values in my own child process on the sealed tree (`969fbd8d`, left clean afterwards): **all bit-equal, all CERTAIN** |
| **(c) Population** | **I re-derived it myself** in a child on the sealed tree. **B:** my own parse of the 25 census JSONs (shas equal `census_shas`, salt-invariant). **C:** my own depth-tracking BFS over `load_pet_contracts`. **A:** my own loop over `REFERENT_LINEUP` under the documented rule (pins always; unpinned non-excluded iff max-emit > pinned count). Result: **A 173 · B 62 · A∪B 209 · P 248 · C depth-1 34 · depth-2 5 · depth ≥ 3 none · capped 19**. P, B and depth-2 equal s2b's sets. The member: **248 rows**, one per `offense_da` pair. Every row's `population_parts`, `population_part` (B > A > C precedence: 62 / 147 / 39), `pet_depth` and `in_js8_path_196` equal my derivation (0 mismatches). `population_part` equals gamora's `source` on the 47. **The depth-2 label "unspawnable in the sealed sim" is on exactly the 5 depth-2 rows** and null on the other 243 |
| **(d) Loader** | The v1-re-cut `load_offense_da(JOIN)` returns **248**. The pinned v0 `load_operands(JOIN)` returns 35. Both refuse `ORACLE`, `PLAY`, `join`, `""` and `None` (10/10, which I exercised myself) |
| **(e) § 4.7 v4 at `e0cd5f74`** | Quiet HEAD (start = end), kc2 tree `7496a28a` at both ends, instrument pinned. Limb A is canonical-equal (`f04ef6d0`). Limb B shows 0 files changed or dirty. B' passes. Both ORACLE children's `opened` lists (631 and 720 entries) contain no rulebook-pack paths. **Valid** |
| **(f) G-10 miscount** | **Adequately handled.** The prereg says "tool + 12 pack files + receipt" (14). The pack has 11 files: the manifest plus 10 members, and I confirmed the manifest lists 10. So 13 is correct, and the commit holds exactly those 13, all adds. The evidence records it as `ok_against_prereg_literal: false` with the arithmetic, and the commit message says so too. Nothing hides behind the miscount, because the commit equals the derived set exactly. The prereg's own § 1 enumeration (7 carried + offense_da + population + meta) gives 10 members, so this is an arithmetic slip, not a scope change. All digest predictions were exact |
| Controls | Raw logs are committed. NC-V3-a, b, c and d all ran as predicted (b: 3 failures on `bl_bounty08|153`; `pth` did not move at +1 ulp, as reported) |

## Notes

**INFO-V3-1 · `class_rules_disagree`'s meaning text is stale.** It still reads "on this path: the 2 bossskills/pets/ records". The v3 member has **3** true rows; the new one is the C-pet `…/bossskills/pets/gabbalthunn_obsidianshard.dbr`. The value_fields were carried unchanged, which preserved the old count. **Cite:** Discipline #82. **Action (star-lord, next cut):** drop the count or restate it per population. Consumers must not read the count from the header.

**INFO-V3-2 · G-10 practice.** State the file count derived from the member list, not as a free number. **Cite:** Discipline #76.

**INFO-V3-3 · The population member has no sanctioned JOIN-only loader.** It is digest-protected through the manifest, but a reader opens it as raw JSON, so no refusal applies to it. `load_offense_da` and `load_operands` both refuse non-JOIN; this member is the only one with no refusing reader. **Action (gamora):** her closure-tally reader should open it only after the JOIN-only `load_offense_da` digest check, or star-lord adds `load_population(config="JOIN")` at the next cut. **Action (gamora):** her PACK_PIN commit also adds the v3 pack and `kc2_rulebook_pack_v3.py` to B' `forbidden_dirs`. B' currently lists v0–v2 only, and the zero opens for v3 rest on the `opened` scan.

**INFO-V3-4 · How independent my population check is.** B and C come from my own parse and BFS. A is my own implementation of the documented rule, but it uses the sealed `referent_lineup`, `wave_engine` and `roster` API. It is therefore an independent implementation, not an independent source.

**Carried:** INFO-5(b).

## Action
- [ ] star-lord: INFO-V3-1 and INFO-V3-2 at the next cut.
- [ ] gamora: INFO-V3-3 (open the population member only behind the JOIN-only digest check; add v3 to B').
- [ ] Matt: none. **gamora may move `PACK_PIN` to v3.**

## References
- Engine:
  - `src/reincarnated/export/math/2026-10-08-kc2-rulebook-pack-v3-prereg.md`
  - `src/reincarnated/export/kc2_rulebook_pack_v3.py`
  - `src/reincarnated/output/kc2-rulebook-pack-v3-20261008_102954/` + receipt
  - `src/reincarnated/simulation/scripts/gamora_join1_pj25_step2b_2026_10_08.py@d7561387`
- Collab:
  - `agentic_orchestration/star-lord/analyses/2026-10-08-join1-rulebook-pack-v3/`
  - `…/gamora/analyses/2026-10-08-join1-pj25-step2b/run-edition-IV/s2b_report.json@910048891`
- Census: `/Users/admin/Games/join3a-bulk-evidence/step2b-census-oracle/` (25 files, sha-pinned)
- Sealed: `969fbd8d`, `data/kc2/pm4o_oa_da.csv`
