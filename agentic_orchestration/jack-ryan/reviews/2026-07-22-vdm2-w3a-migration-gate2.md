# Finding — 2026-07-22 — VDM-2 W3a migration package (corpus.db v1.1-verified → v2.0)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** BLOCK
**Target:** commit `30ac1eb5` — `agentic_orchestration/elrond/notes/2026-07-22-vdm2-*` (5 artifacts)
**Developer:** elrond (data steward)
**Run:** `2026-07-22-vdm2-edition-next-lap` (gandalf RUN-CONDUCTOR) · desirable-run-pattern §5 safety-2 independent Gate-2
**Principles applied:** Review Principle #2 (smoke-gate / prove the guard fires), #4 (decisions-log/ruling as truth — asserts are the mechanical enforcement of V-11..V-20 counts); Discipline #2 (smoke-test vs full-regen), Discipline #8 (schema validation at boundaries), Discipline #10 (empirical inspection over assumption); ADR-004 (MIGRATION.md handoff); ADR-006 (read-only external systems — honored, live db untouched).

---

## Verdict: **BLOCK** — one defect, one file (`2026-07-22-vdm2-w3b-apply.sh`), clean remediation.

The **DDL v1 and the data riders are byte-perfect** and every technical-integrity claim in the package verified exactly on a throwaway dry-run (evidence below). The BLOCK is isolated to the **apply script's census-assert idiom**, which silently voids the package's own headline safety guarantee ("any assert failure → ROLLBACK; the v2.0 stamp only lands if every assert passed"). That guarantee is **inoperative as written**. Because the apply script is manifest item #3 and Gate-2 scope clause #4 is explicitly "apply-script safety," this is in-scope and blocking.

---

## What I found

**The 7 census asserts at step [5] use `RAISE(ABORT,...)` inside bare top-level `SELECT CASE ... END` statements. SQLite permits `RAISE()` ONLY within a trigger-program.** Every assert therefore fails at *parse* time — it never evaluates the count. Under the sqlite3 CLI's default (no `-bail`) heredoc behavior, a parse error on one statement prints to stderr and the CLI **continues to the next statement**. Result on the throwaway apply-script run: all 7 asserts emitted `Parse error near line N: RAISE() may only be used within a trigger-program`, were skipped, and the script proceeded to the **v2.0 stamp INSERT + COMMIT** — which succeeded. The DB landed **stamped `v2.0`, corpus_class written to 585 rows, kit_master 574, integrity ok** — i.e. it *looks* like a clean success. `set -euo pipefail` does not save it: sqlite3 returns exit 1, but the `COMMIT` has **already persisted** inside the heredoc before the CLI exits, so by the time bash sees the nonzero code and dies, the mutation + stamp are permanent. The step-[6b] post-stamp guard reads `v2.0` and would pass.

Net blast radius: **the abort-on-mismatch protection does not exist at runtime.** The migration will complete and self-stamp v2.0 *regardless of whether the riders produced correct counts.* Today the counts happen to be correct (I re-derived all of them independently — see below), so the *data* would be fine; but the *safety property the package sells as its commitment-boundary* is absent. A future rider drift, or an application against a subtly-changed corpus.db, would stamp v2.0 over wrong data with no abort. That is precisely the failure this pre-registered gate exists to prevent.

Reproduced 3×: (a) the real apply script pointed at an isolated scratch copy; (b) the identical heredoc block hand-fed to sqlite3; (c) a minimal `set -euo pipefail` wrapper around `BEGIN; SELECT CASE...RAISE; INSERT v2.0; COMMIT;`. All three land v2.0 with the asserts bypassed. Root cause isolated: `sqlite3 db "SELECT CASE WHEN (SELECT COUNT(*)...)=585 THEN 1 ELSE RAISE(ABORT,'x') END;"` → `Error: in prepare, RAISE() may only be used within a trigger-program`.

## Rationale

Review Principle #2 (smoke-gate): a guard that cannot fire is not a guard. The package's §8 and the apply-script header both assert "assert failure → ROLLBACK; v2.0 stamp only reached if every assert passed" — this is the *stated* safety contract of the commitment boundary, and it is factually false as coded. Discipline #8 (schema validation at boundaries) requires the boundary check to *execute*; a parse-error-skipped check validates nothing. Discipline #10 (empirical inspection over assumption): the package's §9 validation evidence ran DDL+riders on a throwaway and checked counts *by eye*, but never ran the *apply script itself* end-to-end — which is why the RAISE idiom shipped. Running the actual script is what surfaced this.

## Action

- [ ] **elrond (BLOCK — remediation required before W3b):** Replace the `RAISE(ABORT,...)`-in-SELECT assert idiom with one that actually aborts the transaction on mismatch. Two clean options, either acceptable:
  - **Option A (pure-SQL, minimal):** keep the single-txn heredoc but make each assert a statement SQLite *will* abort on. E.g. force a constraint violation / divide-by-zero, or use a temp trigger. Simplest robust pure-SQL form is a guard that raises via an invalid operation, e.g.:
    `SELECT CASE WHEN (<count>)=<expected> THEN 1 ELSE (SELECT 1 FROM (SELECT 1) WHERE 1/(0) ) END;` is fragile — **prefer** creating a `TEMP TRIGGER` or using `sqlite3 -bail` + a query that errors. The cleanest: add `.parameter`-free `SELECT RAISE` wrapped in a real trigger is overkill. **Recommended pure-SQL:** run each assert as `SELECT CASE WHEN <cond> THEN 1 ELSE (SELECT throw FROM (SELECT NULL AS throw) WHERE throw IS NOT NULL) END;` — no. These are all brittle.
  - **Option B (recommended — script-side assert, robust + legible):** run the DDL+riders in the txn *without* the RAISE lines; **COMMIT nothing yet** by keeping the census checks as `sqlite3` queries evaluated in bash *after* the DDL/riders but *before* the stamp, each compared with `[ "$X" = "<expected>" ] || { echo "ASSERT FAIL ..."; exit 1; }` under `set -e`; and only issue the `INSERT v2.0 ... ; ` stamp in a *separate* `sqlite3` call reached only if every bash assert passed. This makes "stamp LAST, only if asserts pass" a real control-flow guarantee (bash exits before the stamp on any mismatch), not an in-SQL one that SQLite silently skips. Trade-off: DDL/riders and stamp are then in *two* transactions — acceptable here because (i) DDL+riders are idempotent and reversible per §4.3, (ii) the backup is taken first, (iii) an un-stamped partial is exactly the "identifiable partial" the design wants; re-running is safe.
  - Whichever path: **re-run the full apply script end-to-end against a throwaway copy and confirm two things by observation — (1) on correct data it reaches and lands the v2.0 stamp; (2) deliberately break one expected count (e.g. temporarily set the corpus_class expected to 268) and confirm the script ABORTS with NO v2.0 stamp and the txn rolled back.** Ship the negative-path evidence in the re-submission. That negative test is the acceptance criterion for clearing this BLOCK.
- [ ] **elrond (WARN, fix advisable, non-blocking):** MIGRATION.md draft §"9 additive columns" says `verify_ledger` "§7 … mechanics verdicts ALREADY EXIST, **597 rows**", and package MIGRATION.md line references 2068. Live `verify_ledger` is **2068 rows** (I counted). The 597 figure is stale/mislabeled — reconcile the number or clarify what 597 counts (perhaps `run_tag='vdm1' mechanics'` subset) before the MIGRATION.md is appended. Documentation-only; does not affect the apply.
- [ ] **Matt / gandalf RUN-CONDUCTOR:** No decision needed — this is a mechanical BLOCK with a mechanical fix, within elrond's seam to remediate. No conductor design ruling is in question. Re-review is a fast turn once the negative-path evidence lands.

---

## Dry-run evidence — everything EXCEPT the assert idiom PASSES

Method: `cp` live corpus.db → scratch; ran DDL v1 + riders in one txn (`PRAGMA foreign_keys=ON; BEGIN; .read DDL; .read RIDERS; COMMIT`), exit 0; then separately ran the *actual* apply script against an isolated scratch dir. All scratch deleted; **live corpus.db md5 = `50df15b776ad5b0da93fe90cdee1163d` UNCHANGED at close** (verified). Live terminal stamp is `v1.1-deprecation-source_urls` (apply-script preflight accepts it — OK).

**Additive-only guarantee — PROVEN (Gate-2 clause 1):**
- Table inventory 21 → **33** (21 + 12 new); views unchanged at 4. All 12 new tables present.
- All 9 additive columns present (canon_corpus +6, mechanic_gap_docket +3, verify_ledger +3).
- **Pre-existing columns on all 3 altered tables: name+type byte-identical pre/post — zero dropped, renamed, or type-changed** (`comm -23` diff empty for each).
- **Existing-table row counts UNCHANGED:** canon_corpus 585/585, canon_engine_key 585/585, kit_mapping 574/574, mechanic_gap_docket 19/19, verify_ledger 2068/2068, kit_dossier 3444/3444, kit_citations 1287/1287, mint_ledger 12/12.
- **CHECK-safety (the pre-registered check) VERIFIED:** `diff` of `verify_ledger` table SQL pre/post shows the ONLY change is 3 appended nullable columns; the existing `claim_family` and `verdict` CHECK clauses are byte-identical — **no rebuild, no VDM-1 data touched.** A-1 (`range_band 'self'`) and A-4 (`arg_type 'real'`) CHECKs land only on the v1-NEW tables `skill_geometry_band` / `door_arg_schema`. Confirmed empirically: `self` ACCEPTED + `BOGUS` REJECTED; `real` ACCEPTED + `BOGUSTYPE` REJECTED.

**Census re-derivation — every claim EXACT (independently re-derived, not trusting the asserts):**
- corpus_class: **record 267 · annex 299 · system 19 · NULL 0** (sum 585). ✓
- court (record bucket): **physical 90 · fire 54 · chaos-poison 44 · lightning 42 · cold 27 · NULL 13** → 257/270 courted. ✓
- original_element 270 · atlas_coords 268 · eras_normalized 268 (record). ✓
- iron-law: canon_corpus 585 · kit_master 574 · is_system 19. ✓

**Court mapping correctness (Gate-2 clause 3, V-15 implementation) — VERIFIED per-token:** grouped post-court by raw `elem_raw`: fire→fire(54), cold→cold(27), lightning(38)+aether(4)→lightning(42), physical(85)+physical?(1)+pierce(2)+bleed(2)→physical(90), chaos(22)+poison(4)+acid(3)+necrotic(5)+vitality(6)+void(3)+void?(1)→chaos-poison(44), and magic(4)/n-a(5)/mixed(1)/physical-chaos(1)/shadow?(1)/shadow-blood?(1)→NULL(13). The `?`-suffix base rule and the flagged `pierce`/`bleed`→physical extension both resolve exactly as documented; no token silently mis-mapped. **I accept the `pierce`/`bleed`→physical rider extension** — both are physical-family sub-tokens in every record-game taxonomy, within Q38 k=5, documented not silent. (Court taxonomy MERIT is conductor-ruled V-15/V-20, out of my scope; I reviewed *implementation fidelity* only, which is correct.)

**A-7 preserve-NULL (Gate-2 clause 3, the corrected-to-29 assert) — VERIFIED:** `t4_doors` JSON-null count **PRE 29 = POST 29** (unchanged), record-game subset 8, empty-array `[]` count 16/16 untouched. The rider provably performs **no** write to `t4_doors` and does not coerce/strip NULL. The pilot-§7-to-29 count correction is right.

**A-2 / A-3 seeds — VERIFIED:** door_registry 6; door_arg_schema 3 (`trigger_condition`::enum, `parallel_triggers`::int, `cadence_scale`::real); motion_signature_registry 7 incl. `fan_spread` present.

**Integrity — clean on DDL+riders scratch:** `PRAGMA integrity_check` = ok; `PRAGMA foreign_key_check` = 0 rows. (The buggy apply-script scratch also landed integrity ok — the defect is a *bypassed guard*, not corruption; the data it writes is correct.)

**Reversibility / apply-sequence (Gate-2 clause 4) — PARTIAL:** backup-first + md5-record-first ✓; `PRAGMA foreign_keys=ON` before side-car inserts ✓; raws never dropped ✓; new dockets default `status='open'` ✓ (distinct from 19 matt-ratified). **v2.0-stamp-LAST-only-if-asserts-pass = FAILS** (the BLOCK above): the stamp lands even though the asserts never run.

**ADR-004 conformance (Gate-2 clause 5) — PASS (aside from the WARN):** MIGRATION.md draft documents what changes, the additive guarantee, reversibility, per-game era vocabularies, and all 5 named downstream deps (normalization_rule → gamora/star-lord; exact_json → legolas Mode-B; W5 elem_raw→court re-derivation; capstone → W4; accepted_downgrade owner-identity → W4). This is a research-DB migration; MIGRATION.md is the durable record; no engine decisions-log entry required (per brief).

**VDM-1 survival (Gate-2 clause 6) — PASS:** kit_master returns 574; v_canon_corpus_rekeyed 585, v_combat_kits 518, v_corpus_substrate 509 all assemble intact post-apply.

---

## References
- `agentic_orchestration/elrond/notes/2026-07-22-vdm2-w3b-apply.sh` — **the BLOCK is here** (step [5] assert idiom, lines ~78-107).
- `agentic_orchestration/elrond/notes/2026-07-22-vdm2-ddl-v1.sql` — reviewed, byte-perfect.
- `agentic_orchestration/elrond/notes/2026-07-22-vdm2-riders.sql` — reviewed, byte-perfect; census exact.
- `agentic_orchestration/elrond/notes/2026-07-22-vdm2-w3a-migration-package.md` — the reviewable overview.
- `agentic_orchestration/elrond/notes/2026-07-22-vdm2-migration-draft.md` — ADR-004 draft (WARN: verify_ledger 597-vs-2068 row-count nit).
- Live target: `agentic_orchestration/research/curated/corpus.db` @ `v1.1-deprecation-source_urls` / md5 `50df15b776ad5b0da93fe90cdee1163d` (unchanged; untouched).

**Verdict: BLOCK.** Fix the apply-script assert idiom so it actually aborts, prove the negative path (deliberately-wrong count → no stamp + rollback) on a throwaway, re-submit. Everything else is cleared. NO PUSH (conductor centralizes).
