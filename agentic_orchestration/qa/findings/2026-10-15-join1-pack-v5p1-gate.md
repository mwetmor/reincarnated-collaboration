# Finding — 2026-10-15 — JOIN-1 J4b · packs gate: `kc2-rulebook-pack-v5.1` (`8079f8ef…`), the narrow delta on v5

**Reviewer:** jack-ryan (DEV-MODE packs gate, BLOCK authority)
**Severity:** PASS-WITH-NOTES, **CONDITIONAL ON (f)** (0 BLOCK, 0 WARN, 3 INFO)
**Target:** engine `0b78936c` (prereg) · `48d49953` (delta) · `fa65d30b` (cut) · `6869aef9` (MIGRATION); collab `0848914ff` (evidence), `cc466d4be` (gamora's table)
**Developer:** star-lord; gamora (table)
**Basis:** my v5 gate `7d21565c9`, conditions (a)–(g)
**Principles applied:** 1, 3, 5

## Verified independently

| Condition | Result |
|---|---|
| **Order; digests** | Prereg 13:41:37 → delta 13:49:22 → receipt stamp `134952` → cut 13:50:12; both docs are unchanged at HEAD. Pack `8079f8ef…` and manifest FILE `6be53dfa…` re-derive. The changed members' FILE / ROWSET equal delta § 3: contact `81dba57f` / `b3889ea5`, anchor `26da4dcd` / `43477944`, meta `0b54ea2f` / `762a8223`. Every file equals its `fa65d30b` blob |
| **(a) AR tables** | Byte-identical to v5 (`8144c234`, `75cf28ec`), and equal to gamora's new manifest `outputs_sha256` (manifest FILE `b8d121de`, `engine_head` `d52dd775`, `head_fixed`; kc2 tree at `d52dd775` = seal `7496a28a`). **Met** |
| **(b) Contact-table diff** | My own diff of v5's table against v5.1's: **2,187 → 2,526: 339 added, 0 removed, 0 changed.** Every added key's skill basename is `defaultweaponattack.dbr`, and every value is `[true, "swing"]`. The added set equals gamora's `added_keys.json` (339) exactly. Counts change only slots (+339) and contact (800 → 1,139); `pierce_only` / `bleeding_only` and the other top-level keys are unchanged. The table bytes equal gamora's committed blob at `cc466d4be`. **Met** |
| **(c) `anchor_d2_gd`** | Field-by-field over all 24 rows: **only `RB-A-physical_contact_table` differs**, in `value`, `provenance` and `points_to` (new table, her manifest, `added_keys.json`, EMITTER `a8cda203`, ENGINE-FORM `d2/anchor.py@d52dd775`; both commits exist). The AR rows are fully unchanged, which is stricter than (c). No top-level change. **Met** |
| **(d) Everything else byte-identical** | **14/17 members byte-identical to v5.** `meta` changed keys = {`pack`, `format`, `supersedes`, `inputs`, `v5_1`}. `pack` and `format` were named in the prereg as the unavoidable identity fields; accepted. **Met** |
| **(e) G-5b** | My own decode through the loaders, v5 against v5.1, over all **122** rows (KIT 79, WORLD 8, ANCHOR 24, HOOK 11): the identical id set, and the only value/grade diff is `physical_contact_table`. **Met** |
| **(g) Re-runs** | GD binder **35**, encoding-equal to v3. Refusals **25/25** (my own run). JOIN reads the contact FILE `81dba57f…`. § 4.7 v4 is **ORACLE BYTE-IDENTICAL** in a dedicated worktree (`reincarnated-engine-v51-s47`) with HEAD fixed at `fa65d30b`: pinned, A `f04ef6d0`, B 0 changed, B' pass, 0 pack paths opened. The controls are as predicted: slot (338 ≠ 339, the `added_keys` mismatch), slot-b (`n_changed` 1), ar (HALT at (a)), anchor (HALT at (c) with the extra provenance field), d (verify exit 1), e (25/25). **Met** |
| **(f) Port fail-first (drax)** | **NOT YET RUN.** It is the condition on this verdict |

## Verdict

**PASS-WITH-NOTES, conditional on (f).**
- v5.1 **succeeds v5 as the pack of record for binding now.**
- It becomes **quotable for graded contact-table-dependent results** only once drax's (f) shows **10/25 "runs" FAIL on v5 `c403ca5d` → GREEN on v5.1 on the same 25 cells**, with no other cell changing verdict.
- **If (f) is RED, or any other cell moves, HALT to the conductor.** That would mean the table fix is not the whole cause, or that it moves something else. A re-gate follows in that case.
- When (f) lands GREEN, a one-line delta note citing drax's commit closes this.

## Findings

**INFO-1 · B' still does not list v5 / v5.1** (pack dirs and tools); owed by gamora, carried from v5 INFO-3. The opened scan shows 0 opens.

**INFO-2 · Two stale `pack` strings, both declared.** The v5 loader's refusal text names "kc2-rulebook-pack-v5" on v5.1. Row `scope` strings stay "…-v5…" by declared design (prereg § 0; `meta.v5_1.scope_strings`). Pack identity lives in the manifest and `meta.pack`. Consumers must not read it from either string.

**INFO-3 · Carried to the next full cut:** INFO-V3-1 (`offense_da`) and the `light` / `lightning` unification. The alias is recorded in `meta.v5_1.key_aliases`.

## Action
- [ ] drax: run (f) on fb49080f after the ORACLE chain, and report the commit. Any non-predicted cell HALTs.
- [ ] star-lord: a one-line note citing (f) when it is GREEN.
- [ ] gamora: INFO-1.
- [ ] Matt: none.

## References
- Engine:
  - `src/reincarnated/export/kc2_rulebook_pack_v5p1.py`
  - `…/math/2026-10-15-kc2-rulebook-pack-v5p1-prereg.md`, `…-prereg-delta.md`
  - `src/reincarnated/output/kc2-rulebook-pack-v5.1-20261015_134952/` (vs v5 `…-v5-20261015_081830`)
  - `a8cda203`, `d52dd775`
- Collab:
  - `star-lord/analyses/2026-10-15-join1-rulebook-pack-v5p1/`
  - `gamora/analyses/2026-10-15-join1-j4b-contact-table-v51/@cc466d4be`
  - my v5 gate `7d21565c9`
