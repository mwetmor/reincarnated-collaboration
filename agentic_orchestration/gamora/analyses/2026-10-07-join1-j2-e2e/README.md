# JOIN-1 · J2-E2e evidence: § 4.7 instrument v4 + per-pid witness v2 (E2b Gate-2 WARN-1, WARN-2)

gamora, 2026-10-07. This is a **separate instrument commit before E3**, not folded into E3. Conductor KP-323; finding collab `5312a8852`.

## Engine commits

| Commit | What it holds |
|---|---|
| `518579d1` (ALONE) | `gamora_join2_s47_v4_2026_10_07.py` · `join2_bprime_witness_hook_v2/sitecustomize.py` · `tests/test_join2_s47_v4_warn12.py` |
| `62b6e48e` (ALONE, a fix) | Limb B excludes exactly the instrument's own two files (see § 1) |

**Fail-first:** the test file run against v3 gave **13 failed, 2 passed**. The 2 that passed test witness v2 directly, not the script. Against v4: **15 passed**. The Limb B exclusion test failed on the committed `518579d1`; with the fix, the file gives **16 passed**.

## § 1 · v4's first run of record read NOT SHOWN (`s47v4/`, kept, not relabelled)

At `518579d1`, Limb A was equal (`f04ef6d0…`) and B′ passed, but **Limb B failed**: `files_changed_between_seal_and_HEAD = [join2_bprime_witness_hook_v2/sitecustomize.py]`.

**Cause.** The HEAD child loads the witness file *as a library*, for the shared fingerprint, after its audit hook is installed. So v2's closure rule, "no loaded or opened engine file changed since the seal", saw the instrument itself.

**This is attributed to a named instrument defect, not to an ORACLE change.** The fix in `62b6e48e` excludes exactly two paths, the v4 script and the witness v2 file, and records each with its sha256. Every other file is checked as before.

## § 2 · § 4.7 at `62b6e48e`: **ORACLE BYTE-IDENTICAL** (`s47v4-r2/`)

- **HEAD:** start = end = `62b6e48e`; the kc2 tree is `7496a28a` at both ends.
- **Limb A:** canonical `f04ef6d0…` on both sides.
- **Limb B:** passes. The only exclusion is `instrument_files_excluded = [witness v2 sitecustomize.py, sha256 f3c03b7e…]`.
- **Limb B′:** passes.
  - Path hits: 0 and 0.
  - Census equal: 44 function rows under the WARN-1 fingerprint, plus the 63 values.
  - Exact s47 tree: 2 of 2 children, `tree_ok`.
  - 0 witness hits. Each record's exit fingerprints equal the sealed census.
- **Limb C:** passes.

## § 3 · Controls at `62b6e48e` (`controls/`)

These are NON-GRADED-CONTROL, import-only runs. The predictions are in `CONTROL_PREDICTIONS`, committed at `518579d1` before any run of record.

| control | observed | matches prediction |
|---|---|---|
| nc8-0 | B′ GREEN | yes |
| nc8a | B′ RED: 3 path hits; census differs `['threat.mitigate']`; witness hits on the module path, the opened files and the fingerprint | yes |
| nc8b | B′ RED: 18 path hits (6 `join2_rulebook*` modules plus opened files); witness import-EVENT hits; census equal | yes |
| nc8c | B′ RED: witness env hit only | yes |
| nc8d | B′ RED: foreign `sitecustomize` hit; tree 1 of 2 (`tree_ok` false) | yes |
| nc8e | NO VERDICT (`62b6e48e` → `518579d1`) | yes |
| **nc8f** (re-homed `resolve_hit`) | B′ RED: census differs exactly `['threat.resolve_hit']`; witness fingerprint hit only; path GREEN | yes |
| **nc8g** (`probability_to_hit` 300.0 → 301.0) | B′ RED: census differs exactly `['threat.probability_to_hit']`; witness fingerprint hit only; path GREEN | yes |
| nc8-0-strip (now a predicted control, INFO-2) | B′ GREEN; stripped `['JOIN1_B0N_BINDINGS', 'JOIN2_PARENT_STRIP_CTL']` | yes |

The scratch dry runs at `518579d1`, before this commit, gave the same B′ results.

## Owed at E3 (finding § 4)

- The emitter-mode tree on the ORACLE-half re-emission: exactly 1 emitter pid plus 25 cells (50 under `--inertness`).
- Witness inertness: 7/7 ROWSETs equal to `f82807fb`, and `foreign_reads` = 0.
- The coverage negative control, with one cell's witness displaced.
- The JOIN-half records in the same schema.
- NC-J2-8 (a) and (b) re-run with the binder of record.
- The A-2 JSON with the real class names and a corrigendum line to ADDENDUM-E1 (INFO-1).
