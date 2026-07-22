# Finding — 2026-07-22 — VDM-2 W3a-fix RE-GATE (apply-script guard remediation)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** PASS — BLOCK cleared
**Target:** commit `c5688c8b` — `agentic_orchestration/elrond/notes/2026-07-22-vdm2-w3b-apply.sh` (rewritten) + `…-w3a-fix-negative-path-evidence.md` (new)
**Developer:** elrond (data steward)
**Run:** `2026-07-22-vdm2-edition-next-lap` (gandalf RUN-CONDUCTOR) · desirable-run-pattern §5 safety-2 independent Gate-2
**Clears:** `agentic_orchestration/jack-ryan/reviews/2026-07-22-vdm2-w3a-migration-gate2.md` (the prior BLOCK)
**Principles applied:** Review Principle #2 (smoke-gate — prove the guard actually fires); Discipline #2 (smoke-test vs full-regen), #8 (schema validation at boundaries), #10 (empirical inspection over assumption — I re-ran the abort path myself rather than trusting the transcript); ADR-006 (read-only external systems — live db untouched, verified).

---

## Verdict: **PASS.** The single BLOCK-ing defect is remediated. The safety guard is now real control-flow, proven by my own execution of the abort path.

This was a fast, narrow re-review — remediation-verification only. I did NOT re-prove the additive schema, census, court fidelity 257/270, or additive-holds; those were cleared in the prior Gate-2 and DDL v1 + riders are byte-unchanged (git-confirmed: `git diff 30ac1eb5 c5688c8b` on both `…-ddl-v1.sql` and `…-riders.sql` is EMPTY; the only substantive change between the cleared package and the fix is the `.sh` rewrite + the new evidence note). I reviewed exactly the three items the remediation touches.

---

## What I found

The prior BLOCK was isolated: the 7 census asserts used `RAISE(ABORT,…)` inside bare top-level `SELECT CASE…END`, which SQLite permits only inside a trigger-program, so every assert failed at PARSE time, the CLI skipped them, and the v2.0 stamp landed regardless of the counts — the headline safety contract was inoperative. elrond rewrote the script to my own Option-B recommendation: the DDL v1 + riders commit first in one transaction (the census columns must exist before bash can read them back), then the checks run as **17 bash-gated asserts** (each expected count read via a `sqlite3` scalar into a shell var and compared by an `assert()` helper that does `[ "$actual" = "$expected" ] || { echo "ASSERT FAIL…"; exit 1; }` under `set -euo pipefail`), and the **v2.0 stamp is a separate, last `sqlite3` invocation** reached only after all 17 asserts pass. I verified all three review items — the control-flow structure (statically), the abort behavior (by re-running the negative path MYSELF, not trusting elrond's transcript), and the production-safe default path (by resolving the unset-override defaults in an isolated subshell). All three pass. The live corpus.db was untouched throughout (md5 `50df15b776ad5b0da93fe90cdee1163d`, stamp `v1.1-deprecation-source_urls`, zero v2.0 rows — verified at open and at close).

## Item-by-item evidence

### Item 1 — the bash-gate is REAL control-flow (static analysis) — PASS
- **No `RAISE` in executable SQL.** The only two `RAISE` occurrences in the file are in the header comment describing the prior defect (lines 13–14). The parse-skip escape hatch is gone.
- **No swallow-and-continue.** The only two `sqlite3 "$DB" <<SQL` heredocs are line 97 (DDL+riders) and line 168 (the stamp). There is NO `sqlite3 < asserts.sql` / `.read asserts` on the assert path — the 17 asserts (lines 130–158) are pure bash scalar substitutions `$(sqlite3 … "SELECT COUNT…")` fed to the `assert()` helper.
- **`set -euo pipefail` at line 50** (real code, not comment).
- **Ordering:** DDL+riders heredoc (L97) → 17 asserts (L130–158) → **stamp heredoc (L168)** last. The stamp is a distinct `sqlite3` invocation strictly after every assert.
- **`assert()` helper** (L117–127) hits `exit 1` on mismatch; under `set -e` that terminates the whole script before the stamp line. Structure confirms "stamp last, only if every assert passed" is a genuine control-flow guarantee.

### Item 2 — I RE-RAN the negative path myself (did NOT trust the transcript) — PASS
This is the load-bearing discipline: the first BLOCK existed precisely because a safety was self-asserted-as-working yet inoperative. I exercised the abort path on my own throwaway copies via the env-override harness, choosing my **own** victim row to stay independent of elrond's transcript.

- **POSITIVE path** (correct data): all 17 asserts printed real counts (267/299/19/0, court 90/54/44/42/27/13, 270/268/268, jsonnull 29, iron-law 585/574/19) — proving they evaluate live, not parse-skip — exit 0, stamp `v2.0`, exactly 1 v2.0 row.
- **NEGATIVE (a) — real data corruption** (my own pick: flipped `kit_id='d2-avenger'` `elem_raw` fire→cold, shifting `court.fire` 54→53; fed the corrupted-copy md5 as `EXPECTED_PRE_MD5` so the md5 preflight passes and the CENSUS guard is what's under test): the `court.fire` assert saw 53, echoed `ASSERT FAIL: court.fire expected 54 got 53`, **exit 1 BEFORE the stamp call**. Final stamp stayed `v1.1-deprecation-source_urls`; **zero v2.0 rows**. This is the exact failure mode that was inoperative in my first BLOCK, and it now aborts.
- **NEGATIVE (b) — wrong expectation** (my throwaway copy, `corpus_class.record` expected 268 vs true 267): aborts on the FIRST assert, exit 1, stamp `v1.1-*`, zero v2.0 rows.
- **REVERSIBILITY** (extra check, not requested): the aborted migrated-but-unstamped partial (md5 `1f6a7dcc…`) restored from its step-[1] backup to exactly the live md5 `50df15b776ad5b0da93fe90cdee1163d`, stamp back to `v1.1-*`. The "identifiable, reversible partial" claim holds byte-for-byte.
- **IDEMPOTENCE / re-run safety** (extra check): re-running the fixed script over a residual partial does NOT silently re-migrate — the step-[0] md5 preflight fires `FATAL: pre-apply md5 … != expected. corpus.db changed since W3a. ABORT`, and the step-[1] backup-clobber guard independently refuses if a backup already exists. Double-guarded against a botched re-run. Positive finding.

| Path | Input | Exit | Final stamp | v2.0 rows | My verdict |
|---|---|---|---|---|---|
| positive | correct data | 0 | `v2.0` | 1 | stamps clean |
| negative (a) real-row corruption | `court.fire` 54→53 (`d2-avenger`) | 1 | `v1.1-deprecation-source_urls` | 0 | aborts, NO stamp |
| negative (b) wrong expectation | `corpus_class.record` expect 268 | 1 | `v1.1-deprecation-source_urls` | 0 | aborts, NO stamp |

### Item 3 — env-override default path is production-safe — PASS
Resolved the L50–64 variable block in an isolated subshell with `DB`/`BACKUP`/`EXPECTED_PRE_MD5` UNSET (assignments only — no `sqlite3`, no `cp`, live db never touched):
- `DB` → the LIVE `…/curated/corpus.db` (PASS).
- `BACKUP` → live-adjacent dated backup `corpus.db.pre-vdm2-schema-2026-07-22-backup` (PASS); distinct from `DB` — no self-clobber (PASS).
- `EXPECTED_PRE_MD5` → the locked `50df15b776ad5b0da93fe90cdee1163d` (PASS).
- **Backup is unconditional and ordered:** step [1] `cp "$DB" "$BACKUP"` (L84) always runs before the DDL heredoc (L96) and verifies `BACKUP_MD5 == EXPECTED_PRE_MD5` before proceeding; the only preceding guard *aborts* on a pre-existing backup, it does not *skip* the cp. No `${VAR:-default}` silently points production at a throwaway or skips the backup.

## Rationale

Review Principle #2 (a guard that cannot fire is not a guard): the guard now fires — I watched it abort on both a real-data divergence and a wrong-expectation, with my own hands, on throwaway copies, and confirmed zero v2.0 rows landed each time. Discipline #8 (schema validation at boundaries): the boundary check now executes as bash control-flow rather than parse-skipped SQL. Discipline #10 (empirical inspection over assumption): I did not clear this on elrond's transcript — I re-ran the abort path independently, which is exactly the discipline whose absence caused the original defect to ship. ADR-006 honored: live corpus.db md5 unchanged at open and close, zero v2.0 rows in live, all scratch deleted.

## Action

- [x] **elrond:** remediation accepted. The apply script (`c5688c8b`) is cleared for W3b execution on the merits of the apply-script safety guard.
- [ ] **elrond (carry-forward WARN from prior Gate-2, still non-blocking):** the `verify_ledger` 597-vs-2068 row-count nit in the MIGRATION.md draft (`…-vdm2-migration-draft.md`) — reconcile or clarify what 597 counts before the MIGRATION.md is appended at W3b step [7]. Documentation-only; does not affect the apply. Not a re-gate blocker.
- [ ] **gandalf RUN-CONDUCTOR:** no decision needed. Mechanical BLOCK, mechanical fix, cleared within elrond's seam. W3b apply is unblocked from the Gate-2 side. (Actual W3b execution + push remains conductor-sequenced.)

## References
- `agentic_orchestration/elrond/notes/2026-07-22-vdm2-w3b-apply.sh` — the fix; reviewed static (L50–178) + executed end-to-end 3×.
- `agentic_orchestration/elrond/notes/2026-07-22-vdm2-w3a-fix-negative-path-evidence.md` — elrond's evidence; I re-ran its harness independently rather than trusting it.
- `agentic_orchestration/elrond/notes/2026-07-22-vdm2-ddl-v1.sql` · `…-riders.sql` — byte-unchanged from the cleared package (git-confirmed EMPTY diff `30ac1eb5`→`c5688c8b`); NOT re-proven.
- `agentic_orchestration/jack-ryan/reviews/2026-07-22-vdm2-w3a-migration-gate2.md` — the prior BLOCK, now cleared.
- Live target: `agentic_orchestration/research/curated/corpus.db` @ `v1.1-deprecation-source_urls` / md5 `50df15b776ad5b0da93fe90cdee1163d` — verified unchanged, zero v2.0 rows, at close.

**Verdict: PASS.** The one defect that held the W3a migration package is remediated and the fix is proven by independent execution of the abort path. Everything else was already cleared. corpus.db stays v1.1 (this was script review only). NO PUSH from me (conductor centralizes); committing this review artifact to my seam per the established pattern.
