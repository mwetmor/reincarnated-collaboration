# Finding — 2026-10-08 — JOIN-1 KP-373/375/376/377 `kc2-rulebook-pack-v2` delta Gate-2

**Reviewer:** jack-ryan (DEV-MODE delta Gate-2, before gamora's `PACK_PIN` → v2; conductor gandalf)
**Severity:** PASS-WITH-NOTES (INFO only)
**Target:** engine `d1da424e` (prereg) · `02bff63f` (cut) · `0469d403` (MIGRATION + AGENT_STATE); collab `91a010b6d` (evidence)
**Developer:** star-lord
**Base:** v1 re-cut `0c11ef63` (my gate: `dbc109ff3`)
**Principles applied:** 1, 3, 5

## What I found

I checked everything myself against the committed blobs.

| Focus | Result |
|---|---|
| **(a) Prereg before cut; digests** | Prereg committed 09:11:13 → receipt stamp `091157` → cut committed 09:12:13. The prereg is unchanged at HEAD, and the receipt cites `d1da424e`. Pack `95e9c600…` and manifest FILE `c4760fde…` re-derive. FILE / ROWSET for `laws_crit` `233ba69d`/`9c6bf345`, `kit_warlord_crit` `d28b411d`/`9be79723`, `offense_da` `6660c7d8`/`769c4744` and `meta` `8bcdaa69`/`77f2f706` all equal § 3. All 11 pack files equal their `02bff63f` blobs. G-10 = exactly the tool + 10 pack files + receipt |
| **(b) The four operands + bracket** | The OPERAND names are exactly crit.py `GD_DECODED_ROWS` at `5655123c` (`gd_decoded()` reads exactly these 4 from `ops._values`). Values and grades: `pth_roll_span_floor` = 100.0 (`4059…`) DECODED, which matches AMENDMENT-2's table. `crit_damage_pct_eor` = **69.0**, printed beside 57.0, JUDGED. `crit_damage_pct_soulfire` = **57.0**, printed beside 69.0, JUDGED. Those two match AMENDMENT-3 at `84cc0633` lines 24–25 verbatim; corrigendum `c850a0e7` adds only 10 lines. `crit_model_player_stream_gd_decoded` = `"pth-coupled"` DECODED, and that string is in crit.py `MODELS`. **The bracket** is class `BRACKET`, which the pinned v0 `load_operands` skips (non-OPERAND), so the JOIN load returns 35 = 31 + 4. No code reads `crit_bracket_player_stream`. `bracket_sealed_d100()` is called only in `tests/test_join3a_crit.py`, and never from the pack row |
| **(c) NC-V2-a** | See INFO-V2-1. **The fix was control-only, and no digest or prediction shifted** |
| **(d) `offense_da.json`** | The `rows` lists are identical (ROWSET `769c4744`). The header differs only in `pack`, `format`, `header_amendments_v2` and **one** `value_fields` entry (`level_margin_levels.meaning`, now INFORMATIONAL on MEASURED, with both minima named). Field order is unchanged. **INFO-R1 closed** |
| **(e) § 4.7 v4 at `02bff63f`** | Quiet HEAD: start = end = `02bff63f`, and the kc2 tree is `7496a28a` at both ends. Instrument pinned. Limb A is canonical-equal (`f04ef6d0` both sides). Limb B shows 0 files changed or dirty. B' passes. Both ORACLE children's `opened` lists (631 and 720 entries) contain no rulebook-pack paths. **Valid**; first-run valid, so no NO VERDICT this time |
| **(f) Corrigendum** | **Correct.** The carried v0 row `RB-DL-crit_damage_pct` has `design_basis` "the sheet's crit damage %", but its value 12.0 is v3.11 IC7-K-0163, which is sealed `fixture.py:219` `CRIT_DAMAGE_PCT = Cited(12.0, "spec §1.3 — Warborn Visor offensiveCritDamageModifier")`. It is a `DESIGN-LISTED-POINTER` with `operand_set_member: false`, so no loader returns it. It is recorded in v2 `meta.corrigenda` rather than in place, which is right for a member carried byte-identical. Self-found and disclosed in the prereg before the cut |

## Notes

**INFO-V2-1 · NC-V2-a run 1: what was fixed, and whether the disclosure is adequate.**
- **The fix was control-only.** Two pieces of evidence show it:
  - **The traceback.** Run 1's traceback puts the failing `assert r["operand"] == "crit_damage_pct_eor"` at line 356 of the pre-fix tool, inside the `if control == "value-ulp":` block, with `main` at line 474. The committed tool has the operand-selecting line at 355 and `main` at 473. That fits a 2-line → 1-line change (`rows[0]` + assert → select by operand) confined to that block.
  - **The output.** NC-V2-c/d ran against dry pack `v2dry3` (09:10:24), which was built by the **pre-fix** tool before the prereg commit. Its manifest FILE `c4760fde` and pack digest `95e9c600` are **identical to the cut's**.
- **No digest or prediction shifted.** The graded path's output is byte-identical before and after the fix, and NC-V2-b (pre-fix) and NC-V2-a r2 (post-fix) both count 26 checks.
- **The pre-fix harness failed safe.** Its assert refused to perturb the wrong (BRACKET) row and wrote nothing.
- **The disclosure is adequate.** r1 is kept raw, marked `as_predicted: false` and explained, and the receipt carries the fixed tool's sha.
- **Remaining gaps (Discipline #75):**
  - The hunk itself is not in the record.
  - The tool was edited *after* the prereg commit. That is permitted, because the prereg pins outputs rather than the tool FILE.
- **Action (star-lord, at the next evidence touch):**
  - paste the hunk into `v2_gate_evidence.json`;
  - delete the stale comment `# rows are id-sorted` on the selecting line.

  For future preregs, either pin the dry-run tool FILE or state that control-only edits after the prereg are permitted, with the hunk recorded.

**INFO-V2-2 · B' does not yet forbid v2.** `forbidden_dirs` now carries both v1 pack dirs and both v1 tools (gamora `9dbe2f34`), so **INFO-2 is closed for v1**. It does not carry the v2 pack dir or `kc2_rulebook_pack_v2.py`. The zero opens for v2 rest on the `opened`-list scan, which I re-checked. **Action (gamora):** add both in the `PACK_PIN` → v2 commit, as prereg § 5 already plans.

**INFO-V2-3 · For the record (no pack defect): the sealed oracle's `CRIT_DAMAGE_PCT` is the Visor term alone (12.0).** It is neither the sheet 57 nor the composed 69. The corrigendum establishes this. The J3a / JOIN comparisons should cite it as the referent's crit-damage operand, not as "the sheet's". The gd-decoded rows (57 / 69) are a JOIN-side change against that referent. **Action (gamora):** confirm that J3a's referent-vs-JOIN reports state this.

**INFO-V2-4 · Cosmetic.** The NC-V2-d refusal messages name the reused loaders' packs (v0 and v1), not v2. star-lord already noted this. No action needed.

**Carried:** INFO-5(b) (late gates run after the write). Declared in the prereg.

## Action
- [ ] star-lord: INFO-V2-1 (record the hunk; remove the stale comment; adopt a tool-pin policy for future preregs).
- [ ] gamora: INFO-V2-2 (add the v2 pack and tool to B' in the PACK_PIN commit); INFO-V2-3 (state the referent's operand in her reports).
- [ ] Matt: none. **gamora may move `PACK_PIN` to v2.**

## References
- Engine:
  - `src/reincarnated/export/math/2026-10-08-kc2-rulebook-pack-v2-prereg.md`
  - `src/reincarnated/export/kc2_rulebook_pack_v2.py` (FILE `bf3db920…`)
  - `src/reincarnated/output/kc2-rulebook-pack-v2-20261008_091157/` + receipt
  - `src/join2_rulebook/crit.py@5655123c`
  - AMENDMENT-2 `@1200ee19`, AMENDMENT-3 `@84cc0633` / `c850a0e7`
  - v3.11 `input_closure.json` IC7-K-0163
  - sealed `fixture.py:219`
- Collab: `agentic_orchestration/star-lord/analyses/2026-10-08-join1-rulebook-pack-v2/` (`v2_gate_evidence.json`, `controls/*.raw.log`, `s47v4/`)
