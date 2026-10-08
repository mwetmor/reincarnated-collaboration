# JOIN-1: P-J2-5 guard rulebook `cf1a3ef9` (PACK_PIN → pack v1 RE-CUT + `OffenseHitUndecided`), evidence

**gamora, 2026-10-08.** These runs follow KP-375. The rulebook worktree was at `cf1a3ef9` for every run here. The instruments are the B′ `forbidden_dirs` + witness `FORBIDDEN_DIRS` list and NC-J2-2 retirement, as of engine `cc875bb9`.

## Runs

| Dir / file | What | Result |
|---|---|---|
| `pj29.json` | P-J2-9 operand bit-equality | **30/30 bit-equal**, NC-E5-1..4 true |
| `golden-master-run1-check-defect/` | J-S8 golden master, run 1 | **Emission was correct, but the instrument check was defective.** The instrument hard-coded tracked count 8 (pack v1 re-cut has 10). Its pid identity also included `engine_root_head`, which broke when HEAD moved mid-run. `pass: false`, `head_fixed: false`. **Kept as evidence, not as a verdict.** Fixed at engine `cc875bb9`. |
| `golden-master/` | J-S8 golden master re-run at `cc875bb9`, profile `gd` | **7/7 FILE-equal** (G1..G7), 25 cells, HEAD fixed, instrument pinned, no foreign reads. `JOIN-PROVENANCE.rulebook_commit = cf1a3ef9…` |
| `s47-nc8m/`, `s47-nc8m.stdout.json` | NON-GRADED-CONTROL nc8m: a v1 re-cut path made readable to the sealed child | **B′ RED as predicted** (`bprime_pass: false`; no § 4.7 verdict, by design) |
| `s47v4/`, `s47v4.stdout.txt` | § 4.7 v4 at quiet HEAD `cc875bb9` | **ORACLE BYTE-IDENTICAL** (HEAD fixed; A, B and B′ pass) |

**Guard minimums by source (INFO-R1)**, read from the GM records:
- MEASURED: PTH 105.98 at `springscrab_h01|152`;
- SOURCED: PTH 106.18 at `mindthief|155`.

Every path pair is ≥ 100, so the guard refused nothing on the J-S8 path. There were **0 JOIN-stream draws** and the J3-INTAKE-ROLL tripwire was 0.

**Bulk:** `emission/` and `records/` for both GM runs were moved to `/Users/admin/Games/join*-bulk-evidence/`. The `bulk_manifest.json` in each dir records the move.

**Superseded for PACK_PIN by `5f7d62fd` (pack v2, KP-378).** See `../2026-10-08-join1-pinv2/`.
