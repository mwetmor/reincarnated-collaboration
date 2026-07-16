# Game-code normalization — R0 (Refit Candidate 1 precondition)

**Date:** 2026-07-16T15:46:00.738089+00:00 · **Executor:** elrond · **Script:** `agentic_orchestration/research/scripts/corpus_gamecode_normalize_2026_07_16.py`
**DB:** corpus.db (gitignored; this log is the record). **Backup:** corpus.db.pre-gamecode-normalize-2026-07-16-backup

Normalizes long-form `canon_corpus.game` -> short codes so the table converges on one convention and the derivation's FRANCHISE_ROLLUP orphan check does not HALT. Idempotent; no cell_key / kit_id touched (frozen Edition-I fit unaffected).

## Migration provenance (the actual transformation applied — first run 2026-07-16T15:45Z)

The section below reflects the FINAL (converged) state after an idempotent re-run. The load-bearing transformation itself, applied on the first run, was:

| long form | short code | rows updated (full-table sweep) | short-code before -> after (active) |
|---|---|---|---|
| `lost-ark` | `la` | 62 | 0 -> 62 (fresh bucket) |
| `diablo-4` | `d4` | 1 | 41 -> 42 (merge) |
| `diablo-3` | `d3` | 1 | 44 -> 45 (merge) |
| `diablo-immortal` | `di` | 1 | 20 -> 21 (merge) |
| **total** | | **65** | |

`mcd` (already short-code) left untouched at 94 active rows. All long-form rows lived in the active set (full-table count == active count for each), so the sweep touched exactly the 65 active-set rows. Post-asserts (no long form survives table-wide; every active `game` is short-code; merge accounting balances) all PASSED on the first run before the schema-meta stamp. The re-run confirmed idempotency (0 rows updated).

## Before

Distinct `game` in ACTIVE set (628 rows): 21 codes.
Long-form present (full table):
- `lost-ark` -> `la`: 0 rows table-wide (0 in active set); target short code currently has 62 rows table-wide.
- `diablo-4` -> `d4`: 0 rows table-wide (0 in active set); target short code currently has 46 rows table-wide.
- `diablo-3` -> `d3`: 0 rows table-wide (0 in active set); target short code currently has 49 rows table-wide.
- `diablo-immortal` -> `di`: 0 rows table-wide (0 in active set); target short code currently has 24 rows table-wide.

No long-form rows present — table already normalized. **Idempotent no-op.**

## Apply (full-table sweep — all row_class, all negative)


**Total rows updated: 0.**

## Post-assert

- No long-form code survives table-wide. OK.
- Active-set distinct `game` codes (21): chronicon, d2, d3, d4, di, gd, hades1, hades2, hot, la, le, mcd, poe1, poe2, tl1, tl2, tli, tq, tq2, undecember, vs. All short-code. OK.

### Merge accounting (active set)

| short code | before (active) | folded-in (active) | after (active) |
|---|---|---|---|
| la (<- lost-ark) | 62 | 0 | 62 |
| d4 (<- diablo-4) | 42 | 0 | 42 |
| d3 (<- diablo-3) | 45 | 0 | 45 |
| di (<- diablo-immortal) | 21 | 0 | 21 |

- `mcd` (already short-code) untouched: 94 active rows (unchanged from 94). OK.

- Schema-meta marker `gamecode-normalize-2026-07-16` inserted.

## Result

Game-code convention converged. Active-set distinct codes: 21, all short-code. FRANCHISE_ROLLUP orphan check will now pass with `la`+`mcd` added at derivation time.
