# Evidence — 2026-07-22 — VDM-2 W3a fix: apply-script guard now fires (negative + positive path)

**Author:** elrond (data steward)
**Remediates:** jack-ryan Gate-2 BLOCK — `agentic_orchestration/jack-ryan/reviews/2026-07-22-vdm2-w3a-migration-gate2.md`
**Fixed artifact:** `agentic_orchestration/elrond/notes/2026-07-22-vdm2-w3b-apply.sh`
**Run:** `2026-07-22-vdm2-edition-next-lap` (gandalf RUN-CONDUCTOR)
**Live corpus.db:** UNTOUCHED throughout — md5 `50df15b776ad5b0da93fe90cdee1163d` at open AND close. All runs on throwaway copies (deleted after).

---

## The defect (jack-ryan's finding, accepted)

The 7 census asserts used `RAISE(ABORT,...)` inside bare top-level `SELECT CASE...END` inside the single-txn heredoc. SQLite permits `RAISE()` ONLY inside a trigger-program, so every assert failed at **parse** time and never evaluated its count. The `sqlite3` CLI (no `-bail`) skipped the parse error and proceeded to the v2.0-stamp `INSERT` + `COMMIT`, which succeeded. `set -euo pipefail` could not help — the `COMMIT` persists before bash sees the nonzero exit. Net: the db landed v2.0-stamped with **all asserts bypassed**; the headline safety contract ("assert failure → no stamp") was inoperative.

Reproduced (fresh scratch copy, exact idiom in isolation):
```
$ sqlite3 scratch.db "SELECT CASE WHEN (SELECT COUNT(*) FROM canon_corpus)=585 THEN 1 ELSE RAISE(ABORT,'x') END;"
Error: in prepare, RAISE() may only be used within a trigger-program   # exit 1
```

## The fix (jack-ryan Option B — bash-gated asserts + separate-call stamp)

**Chosen: bash control-flow (not a TEMP TRIGGER).** Rationale — it matches this script's existing bash-assert structure (steps 0/1/6b already gate with `[ ... ] || { exit 1; }`), and it makes "stamp last, only if every assert passed" a **real control-flow guarantee** rather than an in-SQL one SQLite silently skips.

Structural change (DDL v1 + riders SQL are **UNCHANGED** — Gate-2 proved them byte-perfect):

1. **[2-4] DDL v1 + riders run in ONE transaction and COMMIT** — with NO stamp. They *must* commit before the asserts because the 6 census columns (`corpus_class`/`court`/`original_element`/`atlas_coords`/`eras_normalized`) **do not exist until DDL v1 creates them** — a bash scalar query cannot read them otherwise. DDL+riders are idempotent + reversible (§4.3), the backup is taken first (step [1]), so a committed-but-unstamped db is exactly the "identifiable partial" the design wants; re-run is safe.
2. **[5] The 7 census asserts are now BASH control-flow** (17 individual gated checks — the 6 court sub-counts and the iron-law triple are each their own line). Each expected count is a `sqlite3` scalar into a shell var, gated by an `assert()` helper: `[ "$actual" = "$expected" ] || { echo "ASSERT FAIL ..."; exit 1; }` under `set -euo pipefail`.
3. **[6] The v2.0 stamp is a SEPARATE, LAST `sqlite3` invocation**, reached ONLY after all asserts pass. Because a failed assert `exit 1`s the script, the stamp line is **control-flow-unreachable** on any mismatch.

**Evidence harness note:** the shipped script's `DB` / `BACKUP` / `EXPECTED_PRE_MD5` now read `${VAR:-<production-default>}`, so the *unmodified* script can be driven against throwaway copies via env-override for these tests. Unset in production → live `corpus.db`. No other production behavior changes.

---

## Reproduction recipe (jack-ryan: re-run these yourself)

```bash
LIVE=~/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db
SCRIPT=~/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes/2026-07-22-vdm2-w3b-apply.sh
S=~/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes/.vdm2-fix-scratch   # throwaway

# ---- POSITIVE: correct data -> v2.0 stamp ----
mkdir -p "$S"; cp "$LIVE" "$S/pos.db"; rm -f "$S/pos.db.backup"
DB="$S/pos.db" BACKUP="$S/pos.db.backup" EXPECTED_PRE_MD5=50df15b776ad5b0da93fe90cdee1163d bash "$SCRIPT"
sqlite3 "$S/pos.db" "SELECT version FROM corpus_schema_meta ORDER BY rowid DESC LIMIT 1;"   # -> v2.0

# ---- NEGATIVE (a): corrupt ONE real input row -> abort, NO stamp ----
cp "$LIVE" "$S/neg.db"; rm -f "$S/neg.db.backup"
V=$(sqlite3 "$S/neg.db" "SELECT kit_id FROM canon_corpus WHERE corpus_bucket IN ('poe1','d2','gd','poe2','le') AND elem_raw='fire' LIMIT 1;")
sqlite3 "$S/neg.db" "UPDATE canon_corpus SET elem_raw='cold' WHERE kit_id='$V';"   # court.fire 54->53
NEG_MD5=$(md5 -q "$S/neg.db")
DB="$S/neg.db" BACKUP="$S/neg.db.backup" EXPECTED_PRE_MD5="$NEG_MD5" bash "$SCRIPT"   # exits 1
sqlite3 "$S/neg.db" "SELECT COUNT(*) FROM corpus_schema_meta WHERE version='v2.0';"   # -> 0

# ---- NEGATIVE (b): deliberately-wrong EXPECTED count (jack-ryan's 268 example) ----
cp "$LIVE" "$S/negb.db"; rm -f "$S/negb.db.backup"; cp "$SCRIPT" "$S/negb-apply.sh"
sed -i '' 's/assert "corpus_class.record" 267/assert "corpus_class.record" 268/' "$S/negb-apply.sh"
DB="$S/negb.db" BACKUP="$S/negb.db.backup" EXPECTED_PRE_MD5=50df15b776ad5b0da93fe90cdee1163d bash "$S/negb-apply.sh"  # exits 1
sqlite3 "$S/negb.db" "SELECT COUNT(*) FROM corpus_schema_meta WHERE version='v2.0';"   # -> 0
rm -f "$S/negb-apply.sh" "$S"/*.db "$S"/*.backup   # cleanup
```

---

## TRANSCRIPT A — POSITIVE PATH (correct data → v2.0 stamped)

```
# pre-run: scratch md5 + stamp
scratch md5   = 50df15b776ad5b0da93fe90cdee1163d
pre-run stamp = v1.1-deprecation-source_urls
# --- run actual apply script (env-overridden DB/BACKUP) ---
### VDM-2 W3b APPLY — 2026-07-22T06:16:12Z
## [0] preflight guards
  stamp OK (v1.1-deprecation-source_urls); md5 OK (50df15b776ad5b0da93fe90cdee1163d)
## [1] backup + md5
  backup -> .../.vdm2-fix-scratch/pos.db.backup (md5 50df15b776ad5b0da93fe90cdee1163d)
## [2-4] DDL v1 + riders (single txn; NO v2.0 stamp yet)
  DDL+riders committed (db migrated, still UNSTAMPED v1.1-*)
## [5] census asserts (bash-gated; mismatch -> exit 1 BEFORE stamp)
  ok   corpus_class.record = 267
  ok   corpus_class.annex = 299
  ok   corpus_class.system = 19
  ok   corpus_class.NULL = 0
  ok   court.physical = 90
  ok   court.fire = 54
  ok   court.chaos-poison = 44
  ok   court.lightning = 42
  ok   court.cold = 27
  ok   court.NULL = 13
  ok   original_element.record = 270
  ok   atlas_coords.record = 268
  ok   eras_normalized.record = 268
  ok   t4_doors.jsonnull = 29
  ok   iron-law.canon_corpus = 585
  ok   iron-law.kit_master = 574
  ok   iron-law.is_system = 19
  ALL 17 census asserts passed.
## [6] v2.0 stamp (separate call; reached only after all asserts passed)
  v2.0 stamp written.
## [6b] stamp verified: v2.0
## [7] MIGRATION.md — append the W3a draft entry to .../curated/MIGRATION.md (per ADR-004)
## [8] compendium regen from kit_master (smoke: kit_master assembles post-DDL)
### W3b APPLY COMPLETE. corpus.db @ v2.0. Backup at .../.vdm2-fix-scratch/pos.db.backup.
### Reversibility: cp ".../pos.db.backup" ".../pos.db" restores exact pre-VDM-2 state.
# --- end script ---
EXIT CODE      = 0   (0 = success)
post-run stamp = v2.0
v2.0 rows      = 1
```

**Result: PASS.** All 17 census asserts evaluate for real (proving the guard is now live, not parse-skipped), exit 0, stamp `v2.0`.

---

## TRANSCRIPT B — NEGATIVE PATH (a): corrupt ONE real input row → ABORT, NO stamp

This is the stronger negative: a **real data divergence** (not a hardcoded-wrong expectation). One record-bucket row's `elem_raw` is flipped `fire`→`cold`, which genuinely shifts the court census (`court.fire` 54→53). This is exactly the "future rider drift / subtly-changed corpus.db" failure the gate exists to catch.

```
# CORRUPTION: kit_id='poe1-incinerate' elem_raw 'fire' -> 'cold' (shifts court.fire 54->53)
corrupted-copy md5 = c28393c153084e6f9a811e35524e2f1c   (fed as EXPECTED_PRE_MD5 so the md5 preflight passes and the CENSUS guard is what is under test)
pre-run stamp      = v1.1-deprecation-source_urls
# --- run actual apply script against the CORRUPTED scratch ---
### VDM-2 W3b APPLY — 2026-07-22T06:16:12Z
## [0] preflight guards
  stamp OK (v1.1-deprecation-source_urls); md5 OK (c28393c153084e6f9a811e35524e2f1c)
## [1] backup + md5
  backup -> .../.vdm2-fix-scratch/neg.db.backup (md5 c28393c153084e6f9a811e35524e2f1c)
## [2-4] DDL v1 + riders (single txn; NO v2.0 stamp yet)
  DDL+riders committed (db migrated, still UNSTAMPED v1.1-*)
## [5] census asserts (bash-gated; mismatch -> exit 1 BEFORE stamp)
  ok   corpus_class.record = 267
  ok   corpus_class.annex = 299
  ok   corpus_class.system = 19
  ok   corpus_class.NULL = 0
  ok   court.physical = 90
ASSERT FAIL: court.fire expected 54 got 53
  -> aborting BEFORE v2.0 stamp. db is migrated-but-UNSTAMPED (still v1.1-deprecation-source_urls).
  -> reverse the partial: cp ".../neg.db.backup" ".../neg.db"
# --- end script ---
EXIT CODE      = 1   (nonzero = aborted as required)
post-run stamp = v1.1-deprecation-source_urls   (MUST still be v1.1-* — NO v2.0)
v2.0 rows      = 0   (MUST be 0)
```

**Result: PASS (guard fired).** The `court.fire` assert saw 53, echoed `ASSERT FAIL`, exit 1 — **before** the stamp call. Final stamp remains `v1.1-deprecation-source_urls`; **zero v2.0 rows**. The migrated-but-unstamped partial is the intended reversible state (reverse via the step-[1] backup).

---

## TRANSCRIPT C — NEGATIVE PATH (b): jack-ryan's exact 268 example → ABORT, NO stamp

A throwaway copy of the script with the `corpus_class.record` expectation set to 268 (true value 267). Aborts on the **first** assert — court/etc. are never even queried. The shipped script is unchanged (keeps 267); this copy was deleted after the run.

```
# THROWAWAY SCRIPT COPY with corpus_class.record expected DELIBERATELY WRONG (268 vs true 267):
assert "corpus_class.record" 268 "$(sqlite3 "$DB" "SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='record';")"
scratch md5   = 50df15b776ad5b0da93fe90cdee1163d
pre-run stamp = v1.1-deprecation-source_urls
# --- run the wrong-expectation script against a clean scratch db ---
### VDM-2 W3b APPLY — 2026-07-22T06:16:28Z
## [0] preflight guards
  stamp OK (v1.1-deprecation-source_urls); md5 OK (50df15b776ad5b0da93fe90cdee1163d)
## [1] backup + md5
  backup -> .../.vdm2-fix-scratch/negb.db.backup (md5 50df15b776ad5b0da93fe90cdee1163d)
## [2-4] DDL v1 + riders (single txn; NO v2.0 stamp yet)
  DDL+riders committed (db migrated, still UNSTAMPED v1.1-*)
## [5] census asserts (bash-gated; mismatch -> exit 1 BEFORE stamp)
ASSERT FAIL: corpus_class.record expected 268 got 267
  -> aborting BEFORE v2.0 stamp. db is migrated-but-UNSTAMPED (still v1.1-deprecation-source_urls).
  -> reverse the partial: cp ".../negb.db.backup" ".../negb.db"
# --- end script ---
EXIT CODE      = 1   (nonzero = aborted as required)
post-run stamp = v1.1-deprecation-source_urls   (MUST still be v1.1-* — NO v2.0)
v2.0 rows      = 0   (MUST be 0)
```

**Result: PASS (guard fired).** Exit 1 on the first mismatch; final stamp `v1.1-deprecation-source_urls`; **zero v2.0 rows**.

---

## Summary

| Path | Input | Exit | Final stamp | v2.0 rows | Verdict |
|---|---|---|---|---|---|
| A positive | correct data | **0** | `v2.0` | 1 | stamps clean |
| B negative (real-row corruption) | `court.fire` 54→53 | **1** | `v1.1-deprecation-source_urls` | **0** | aborts, NO stamp |
| C negative (wrong expectation) | `corpus_class.record` expected 268 | **1** | `v1.1-deprecation-source_urls` | **0** | aborts, NO stamp |

**The safety contract is now operative:** the v2.0 stamp lands if and only if every census assert passes. On any mismatch the script exits before the stamp call is reached; the db keeps its pre-stamp version and the DDL+riders partial is reversible via the step-[1] backup.

**Live corpus.db md5 = `50df15b776ad5b0da93fe90cdee1163d` — verified unchanged at close.** All scratch dbs/backups deleted.
