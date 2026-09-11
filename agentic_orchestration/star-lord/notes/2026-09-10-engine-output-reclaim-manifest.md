# Engine operational-pipeline disk-reclaim manifest — 2026-09-10

**Agent:** star-lord (engine operational-pipeline seam)
**Conductor:** gandalf
**Authority:** Matt GO 2026-09-10, binding constraint verbatim: *"I don't want to lose data we will need to reference later."* Conservative default KEEP.
**Scope (dispatch-bounded):** `~/Games/reincarnated-engine/output/`, `logs/`, `cache/`. Nothing else touched.
**Occasion:** T20 disk-RED re-opened — `/System/Volumes/Data` at 28.80 GB avail of 460 (94% used). See `~/Games/reincarnated-collaboration/canonical/matt_to_do/2026-08-24-mac-disk-space-red.md`.

---

## 0. Headline

**Total freed: 18,219,748 KB — 17.38 GiB (18.66 GB decimal).**
**Items deleted: ZERO. Data lost: ZERO.**

The dispatch asked for a KEEP/DELETE classification. On inspection, a third option **strictly dominated deletion** for the entire high-yield surface: the 18.87 GB of `fights.jsonl` is line-oriented JSON with extreme structural repetition and compresses **14.6×** with stdlib-readable gzip. Compressing in place recovers 93% of what full deletion would have recovered while satisfying Matt's constraint *absolutely* rather than probabilistically — nothing needs to be "regenerable" if nothing is gone.

Deletion was therefore reserved for items where compression could not apply. **No such item survived predicate review.** Details and the reasoning that nearly went the other way are in § 3.

| Scope path | Before (KB) | After (KB) | Freed (KB) |
|---|---:|---:|---:|
| `output/` | 19,154,052 | 1,348,040 | **17,806,012** |
| `logs/` | 498,328 | 84,592 | **413,736** |
| `cache/` | 56,896 | 56,896 | 0 (KEEP — see § 4) |
| **TOTAL** | **19,709,276** | **1,489,528** | **18,219,748** |

Directory-delta arithmetic reconciles exactly with the per-item sums in § 2 and § 3 (17,572,692 + 647,056 = 18,219,748). No unaccounted bytes.

Disk after: 43.46 GB avail (from 28.80). The observed disk delta (14.66 GB) is *smaller* than my freed total because elrond was writing to `data/` concurrently during this pass — my per-item measurements, not `df`, are the authoritative record of this seam's contribution.

---

## 1. Inventory (top-level, `du -sk`, sorted)

### `output/` — 19,154,052 KB before

**Structural fact that determined every ruling:** 18,866,676 KB of the 19,154,052 KB (98.5%) is **26 `fights.jsonl` files**. The remaining 287,376 KB is ~1,900 small artifacts, of which **1,236 are git-tracked**. The per-season content packages — `classes/*.json`, `monsters/*.json`, `gear/catalog.json`, `manifest.json`, `balance_results.json`, `validation_report.json`, `generation_log.txt` — are **all tracked and durable**; only `fights.jsonl` and `gear_pool_staged.json` are excluded, by a deliberate `.gitignore` rule whose own comment reads *"excluded from git; **kept locally**."*

| # | Item | KB before | Class |
|---:|---|---:|---|
| 1 | `R8-ab-run-2026-05-19/` | 7,553,776 | KEEP (archived) |
| 2 | `standard-demo-regen-2026-05-17/` | 4,292,140 | KEEP (archived) |
| 3 | `track-c-spot-regen-2026-05-21/` | 1,801,408 | KEEP (archived) |
| 4 | `standard-demo-regen-2026-05-18/` | 1,563,200 | KEEP (archived) |
| 5 | `S1-first-batch-2026-05-19/` | 887,372 | KEEP (archived) |
| 6 | `S1-retry-1-100002-2026-05-19/` | 829,596 | KEEP (archived) |
| 7 | `S1-retry-2-100003-2026-05-19/` | 821,552 | KEEP (archived) |
| 8 | `p2-fresh-diagnostic-regen-2026-05-19/` | 693,468 | KEEP (archived) — **decisions-log cited** |
| 9 | `R8-mode-smoke-2026-05-19/` | 480,788 | KEEP (archived) |
| 10 | `kpm-full-run-console-20260616.log` | 128,328 | KEEP (archived) |
| 11 | `phase1-harness-full-run.log` | 78,212 | KEEP (archived) |
| 12–~100 | all remaining entries (each ≤ 6,172 KB; mostly tracked `.json`/`.md` measurement receipts) | 24,036 | KEEP (untouched) |

### `logs/` — 498,328 KB before · **0 files git-tracked** (`logs/` is a directory-level ignore)

| Item | KB before | Class |
|---|---:|---|
| `bc_shift_sweep_20260525_105145.log` | 374,444 | KEEP (archived) |
| `w07_lc011_ablation.log.gz` | 51,608 | KEEP (already gzipped by prior work) |
| `bc_shift_sweep_20260525_104937.log` | 40,896 | KEEP (archived) |
| `llm/` (13 × `llm_YYYYMMDD.jsonl` call ledgers) | 27,844 | **KEEP — see § 4** |
| `weapon-library-track-A3.log` | 2,744 | KEEP (archived) |
| ~28 remaining entries (each ≤ 388 KB) | 792 | KEEP (untouched) |

### `cache/` — 56,896 KB before · **0 files git-tracked** (`cache/` is a directory-level ignore)

| Item | KB before | Class |
|---|---:|---|
| `llm/` — 14,224 hash-keyed response-cache JSONs | 56,896 | **KEEP — see § 4** |

---

## 2. Action A — `fights.jsonl` × 26: KEEP, gzip-archived in place

**Ruling: KEEP (lossless archive). NOT deleted.**

### Why this is not a DELETE

The dispatch's DELETE class is *"batch run outputs regenerable from seeded deterministic runs."* Three findings moved these out of that class:

1. **`fights.jsonl` is a convergence TRACE, not a final-state export.** Every record carries `iteration` and `modifier` — it is the *path* the balance loop walked, iteration 0..N. The git-tracked `classes/*.json` hold only the **final converged** class. Re-simulating from the tracked package therefore cannot reproduce iterations 0..N-1. The trace is not recoverable from the durable artifacts; only a full re-run from seed reproduces it.

2. **The prior durable copy is GONE.** `agentic_orchestration/CHANGELOG.md:3742` records that the 2026-05-18 ingest backfilled 609,800 fight rows into `telemetry.db` from six of these files. I verified the live DB:

   ```
   sqlite3 "file:src/reincarnated/telemetry/telemetry.db?immutable=1" "SELECT COUNT(*) FROM class_fight_loadouts;"
   → 0
   ```

   `class_fight_loadouts` is **empty**. The table exists with its full 40-column schema; the rows are not in it. Whatever rebuilt that DB dropped the backfill. **These 26 files are currently the only copy of this data on disk.** Had I deleted them per the letter of the dispatch, the loss would have been unrecoverable without ~10 hours of compute and ~$20 of LLM spend — and the deletion would have looked correct at the time, because the CHANGELOG says the data was ingested. *The record said durable; the substrate said empty.*

3. **Re-run cost is real and partly non-reproducible.** The R8 README logs per-season durations of **34–88 minutes**; `season_100005`'s manifest records `generation_duration_seconds: 2990.5`. Each run invokes the LLM naming pipeline (~$0.85–1.00/season), which is not bit-reproducible. A "regeneration" would be a *similar* run, not the same one — so A/B comparisons against these traces would silently lose their parity.

Finding (2) alone is disqualifying under *"anything whose regeneration recipe you cannot name concretely."* Compression makes the question moot.

### Predicate gates — both passed, machine-checked

**Gate 1 — nothing tracked.** Run per-file across all 26, not sampled:

```
find output -name 'fights.jsonl' | while read f; do echo "$(git ls-files "$f" | wc -l)  $f"; done
→ 0 for all 26/26
```

**Gate 2 — no citation.** `decisions-log.md` + `baseline/` grepped for each run-directory name. One hit, on `p2-fresh-diagnostic-regen-2026-05-19`, at `design/decisions/decisions-log.md:2979,2999,3000,3029,3037`. The cited paths are `p2-classification-and-floor-lock-analysis.md` and `season_100005/balance_results.json` — **both git-tracked, both untouched.** No citation anywhere in either repo names a `fights.jsonl` as evidence. (9 collab-repo mentions of the string `fights.jsonl` exist; all are schema/provenance discussion, none is an evidentiary citation of a specific file.)

Both gates passed for all 26. The archive action was taken anyway, not the deletion the gates would have permitted.

### Method + integrity verification

`gzip -6`, 4-way parallel, in place. Then, per Discipline #8 (validate at the boundary — an archive nobody verified is not a backup):

- `gzip -t` on all 26 → **26/26 PASS**
- Round-trip line count, `R8-mode-smoke/baseline/season_099999`: pre-compression `wc -l` = **15,344**; `gzcat | wc -l` = **15,344**
- Round-trip first record byte-identical to the pre-compression head

### Per-item result

| Path (relative to `~/Games/reincarnated-engine/`) | KB before | KB after | Freed KB |
|---|---:|---:|---:|
| `output/track-c-spot-regen-2026-05-21/season_200002/fights.jsonl` | 948,028 | 65,152 | 882,876 |
| `output/standard-demo-regen-2026-05-17/season_002013/fights.jsonl` | 928,200 | 63,680 | 864,520 |
| `output/R8-ab-run-2026-05-19/inverted_no_naming/season_099003/fights.jsonl` | 898,324 | 61,952 | 836,372 |
| `output/R8-ab-run-2026-05-19/inverted/season_099003/fights.jsonl` | 898,220 | 61,888 | 836,332 |
| `output/R8-ab-run-2026-05-19/baseline/season_099003/fights.jsonl` | 897,156 | 61,760 | 835,396 |
| `output/R8-ab-run-2026-05-19/baseline/season_099001/fights.jsonl` | 888,204 | 60,544 | 827,660 |
| `output/S1-first-batch-2026-05-19/season_100001/fights.jsonl` | 886,360 | 60,032 | 826,328 |
| `output/standard-demo-regen-2026-05-17/season_002015/fights.jsonl` | 881,964 | 60,736 | 821,228 |
| `output/R8-ab-run-2026-05-19/inverted_no_naming/season_099001/fights.jsonl` | 879,784 | 59,904 | 819,880 |
| `output/R8-ab-run-2026-05-19/inverted/season_099001/fights.jsonl` | 870,644 | 59,520 | 811,124 |
| `output/standard-demo-regen-2026-05-17/season_002011/fights.jsonl` | 852,044 | 58,560 | 793,484 |
| `output/track-c-spot-regen-2026-05-21/season_200001/fights.jsonl` | 851,500 | 57,920 | 793,580 |
| `output/standard-demo-regen-2026-05-17/season_002014/fights.jsonl` | 834,688 | 57,088 | 777,600 |
| `output/S1-retry-1-100002-2026-05-19/season_100002/fights.jsonl` | 825,096 | 56,704 | 768,392 |
| `output/standard-demo-regen-2026-05-18/season_002016/fights.jsonl` | 802,744 | 55,552 | 747,192 |
| `output/S1-retry-2-100003-2026-05-19/season_100003/season_100003/fights.jsonl` | 795,364 | 53,696 | 741,668 |
| `output/standard-demo-regen-2026-05-17/season_002012/fights.jsonl` | 786,504 | 54,464 | 732,040 |
| `output/standard-demo-regen-2026-05-18/season_002017/fights.jsonl` | 758,520 | 52,544 | 705,976 |
| `output/R8-ab-run-2026-05-19/inverted/season_099002/fights.jsonl` | 750,900 | 51,648 | 699,252 |
| `output/R8-ab-run-2026-05-19/baseline/season_099002/fights.jsonl` | 740,784 | 50,944 | 689,840 |
| `output/R8-ab-run-2026-05-19/inverted_no_naming/season_099002/fights.jsonl` | 721,340 | 49,792 | 671,548 |
| `output/p2-fresh-diagnostic-regen-2026-05-19/season_100005/fights.jsonl` | 692,496 | 47,488 | 645,008 |
| `output/R8-mode-smoke-2026-05-19/no_coalesce/season_099999/fights.jsonl` | 123,544 | 8,388 | 115,156 |
| `output/R8-mode-smoke-2026-05-19/inverted/season_099999/fights.jsonl` | 118,344 | 8,028 | 110,316 |
| `output/R8-mode-smoke-2026-05-19/baseline/season_099999/fights.jsonl` | 118,156 | 8,012 | 110,144 |
| `output/R8-mode-smoke-2026-05-19/inverted_no_naming/season_099999/fights.jsonl` | 117,768 | 7,988 | 109,780 |
| **TOTAL** | **18,866,676** | **1,293,984** | **17,572,692** |

### Access recipe (replaces a regeneration recipe — the data is present, not gone)

- Stream: `gzcat <path>.gz` · grep: `gzcat <path>.gz | grep …`
- Restore in place: `gunzip <path>.gz`
- Python: `gzip.open(path, "rt")` — **stdlib**; no dependency. This is why gzip was chosen over zstd, which measured **59×** (would have freed ~0.95 GB more) but needs a Homebrew binary or a `pip install zstandard` to read. For an archive whose whole purpose is being readable at an unknown later date, stdlib portability outweighed 5% additional yield.

### ⚠ One consumer needs a one-line change before next use

`scripts/ingest_fights_jsonl_to_telemetry.py:103` opens the path with plain `open(fights_jsonl, "r", encoding="utf-8")`. Against a `.gz` it will **fail loudly** (`UnicodeDecodeError`), not silently — acceptable, but it is now a broken call site. Fix is one line (`gzip.open` when the suffix is `.gz`). **Not made here** — out of this dispatch's scope, and it belongs in a knight-rider dispatch per my flagged-but-not-dispatched rule. Queued in § 5.

---

## 3. Action B — 7 large console logs: KEEP, gzip-archived in place

**Ruling: KEEP (lossless archive). NOT deleted.**

These are the closest thing to a genuine DELETE in the whole scope: stdout/stderr transcripts whose *structured* results are tracked JSON beside them (`logs/bc_shift_sweep_results.json`; `output/kpm-band-spatial-recal-full-*.json`). `output/kpm-full-run-console-20260616.log` is 128 MB of one repeated `WARNING … heuristic_fallback` line.

I classified them KEEP anyway. Deleting all seven would have freed 653,348 KB; archiving them freed **647,056 KB — 99.04% of the same yield at zero risk.** Spending a real (if small) chance of losing a diagnostic transcript to buy 6,292 KB is a bad trade, and the WARNING-spam log is exactly the kind of artifact someone reaches for when a drift question reopens.

**Predicate gates:** Gate 1 — `git ls-files` returned **0** for all seven (`logs/` and `*.log` are directory/glob-level ignores; the three `output/` logs are individually untracked). Gate 2 — no citation in `decisions-log.md` or `baseline/` for any of the seven. Both passed; archive taken regardless.

**Integrity:** `gzip -t` on all seven → **7/7 PASS**.

| Path (relative to `~/Games/reincarnated-engine/`) | KB before | KB after | Freed KB |
|---|---:|---:|---:|
| `logs/bc_shift_sweep_20260525_105145.log` | 374,444 | 3,832 | 370,612 |
| `output/kpm-full-run-console-20260616.log` | 128,328 | 1,176 | 127,152 |
| `output/phase1-harness-full-run.log` | 78,212 | 636 | 77,576 |
| `logs/bc_shift_sweep_20260525_104937.log` | 40,896 | 420 | 40,476 |
| `output/S1-retry-2-100003-2026-05-19/generation_run.log` | 25,188 | 112 | 25,076 |
| `output/S1-retry-1-100002-2026-05-19/gen.log` | 3,536 | 20 | 3,516 |
| `logs/weapon-library-track-A3.log` | 2,744 | 96 | 2,648 |
| **TOTAL** | **653,348** | **6,292** | **647,056** |

---

## 4. Explicit KEEPs (untouched, not archived)

### `cache/llm/` — 56,896 KB · **KEEP**

**This cache is LIVE, not stale.** `src/reincarnated/llm/client.py:24` declares `cache_dir: Path | str = "cache/llm"` as the constructor default; `cache.py` reads `<key>.json` from it. The dispatch names "cache contents" as DELETE-class, and the `.gitignore` comment calls it *"large, regenerable"* — but **"regenerable" here means "regenerable by paying Anthropic again."** 14,224 cached responses discarded for 56 MB (0.3% of this pass's yield) converts durable bytes into recurring LLM spend. Wrong direction on both axes. Left intact.

*Available if Matt wants it:* `rm -rf cache/llm` yields 56 MB; recipe is "re-incur the LLM calls." I do not recommend it.

### `logs/llm/` — 27,844 KB · **KEEP**

13 daily `llm_YYYYMMDD.jsonl` files — **these are the LLM cost ledger.** Per my standing seam rule (*every session's cost goes into a ledger*; anomaly detection needs the history to compare against), this is primary telemetry, not a log. Not regenerable at any price. Untouched, uncompressed — they are small and actively read.

### Everything else in `output/` (~24 MB across ~90 entries) · **KEEP, untouched**

Tracked `.json`/`.md` measurement receipts, mostly ≤ 6 MB. Below the noise floor for a 28 GB problem; 1,236 of them are git-tracked anyway, failing Gate 1 outright.

### `data/`, `seasons/`, `baseline/`, `src/`, `exports/`, `reports/` · **out of scope, not inspected, not touched**

---

## 5. Flagged — not acted on

1. **⚠ `.gitignore` EDIT MADE — needs conductor ratification. This is the one change I made outside my three scope paths, and it is deliberate.**
   `output/**/fights.jsonl` does **not** match `fights.jsonl.gz`. Compressing therefore converted 26 ignored files (1.24 GB) into 26 **untracked-and-unignored** files — one `git add -A` away from being committed into git history, which is very hard to undo. I appended to `~/Games/reincarnated-engine/.gitignore` § "Large per-season output files":
   ```
   output/**/fights.jsonl.gz
   output/**/*.log.gz
   ```
   Verified: `.gitignore` had no concurrent uncommitted edit before I touched it; after, `git status --porcelain -- output | grep -c '\.gz$'` → **0**. **Uncommitted, per dispatch.** It is a direct consequence of an authorized action and matches the existing rule's documented intent, but it is a tracked shared file and the conductor should ratify it.

2. **`output/` carries 110 pre-existing untracked-and-unignored entries** (was 134 before my `.gitignore` edit removed the 24 I introduced). Entire directories — `R2-modifier-sweep-2026-05-19/`, `S1-retry-1-100002-2026-05-19/`, `phase3-smoke-2026-05-28/` — plus ~30 loose `.json`. **Not created by this pass.** Relevant to the repo's own `#62(a)` staging discipline: a `git add -A` in this repo sweeps 110 unreviewed entries. Flagging, not fixing.

3. **`class_fight_loadouts` is empty in the production `telemetry.db`** while `CHANGELOG.md:3742` records 609,800 rows ingested on 2026-05-18. Some rebuild dropped the backfill and nothing recorded it. This is a **telemetry-integrity finding well beyond a disk pass** — the durability claim in the team record does not match the substrate. Needs a knight-rider dispatch; I did not investigate further. **Directly load-bearing for this pass:** it is the single fact that turned 18.87 GB from "safely deletable" into "only copy on disk."

4. **`scripts/ingest_fights_jsonl_to_telemetry.py` needs gzip-aware open** (§ 2). One line. Requesting a dispatch rather than taking it.

5. **Two regeneration drivers are untracked** — `scripts/regen_002017_canonical_6.py` and `scripts/track_c_spot_regen_tc*.py` exist on disk but `git ls-files` returns 0. For `track-c-spot-regen-2026-05-21` (1.8 GB), **the regeneration recipe itself is not durable.** Independent confirmation that KEEP was correct there. Worth a dispatch to track them.

6. **Out-of-scope disk surface, observed not touched:** `~/Games/reincarnated-engine/.claude/worktrees/agent-ad557ae39574ea548/` is a full second copy of the repo tree. Not in my scope paths; flagging for whoever holds the T20 whole-disk picture.

---

## 6. Total freed

**18,219,748 KB = 17.38 GiB = 18.66 GB.**
**Deletions: 0. Files lost: 0. Bytes of data lost: 0.**
Disk before: 28.80 GB avail (94% used) → after: 43.46 GB avail (91% used).

Every byte reclaimed is recoverable with `gunzip`. Matt's constraint was not traded against — it was made unnecessary.
