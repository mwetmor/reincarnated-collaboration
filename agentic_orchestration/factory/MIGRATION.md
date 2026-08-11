# factory/receipts.db — schema migrations

Schema custody: **star-lord** (SOFTWARE FACTORY strategy § 8). This file is the
cross-seam contract for the factory's receipts DB, per ADR-004. Any consumer that reads
`receipts.db` — the CLI `status` / `report` surfaces, a future Tier-1/2 UI, jack-ryan's
Gate-2 queries — reads this file first.

**Standing rule:** the DB is *evidence*. Migrations are **additive only**. `ADD COLUMN`
cannot destroy a row. Anything that rewrites or drops is not a migration this module
performs unattended; it is a Matt-authorized operation per ADR-006.

---

## v1 → v2 — the grant becomes durable (Gate-2 J5 / J5b)

**Shipped:** round fifteen, 2026-08-11. **Author:** star-lord.
**Blast radius:** additive. Every v1 query returns identical results against a v2 DB.

### What changed

Five columns added to `agent_sessions`, all nullable, no defaults:

| column | type | meaning |
|---|---|---|
| `permission_mode` | TEXT | `permissionMode` as the harness reported it in its init frame |
| `granted_tools` | TEXT | JSON array of the tools the harness reported it was granted |
| `denial_count` | INTEGER | number of entries in `permission_denials` |
| `num_turns` | INTEGER | turns the harness reported |
| `stop_reason` | TEXT | stop reason the harness reported |

`Receipts.record_agent_session` gains an optional `extra` parameter (the harness's
`RawResult.extra`). Existing call sites that omit it write NULLs and are unaffected.

### Why — and why it is not cosmetic

`check_grant` adjudicated `permission_mode` and `granted_tools` and then **dropped
them**. On a FAILING phase the verdict survives in `phases.error`. On a PASSING phase —
the majority, and the ones a later reader trusts — nothing durable recorded what the
fence had been. The receipt could say the phase succeeded and could not say what it was
allowed to do while succeeding.

This is load-bearing because of **J1**: `--allowedTools` does **not** restrict in
headless `default` mode (measured twice — jack-ryan, then independently by star-lord).
The argv is therefore not evidence of the grant. The harness's init frame is the only
place the real answer appears, and `agent_sessions` is now the only place it is kept.

### NULL semantics — read this before writing a query

Absent is absent (`usage.py`'s opening law, applied to containment evidence):

- `granted_tools IS NULL` — the harness reported **no tool set**. Unknown.
- `granted_tools = '[]'` — the harness reported an **empty tool set**. Known, and known
  to be empty. `check_grant` turns on exactly this distinction.
- `denial_count IS NULL` — no denials were **reported**. It does **not** mean zero
  denials occurred.
- `denial_count = 0` — denials were reported, and there were none.

A consumer that writes `COALESCE(denial_count, 0)` has converted "we do not know" into
"it was clean" and has broken the contract this column exists to keep.

Rows migrated from v1 carry NULL in all five columns. They are **not backfilled**: the
grant for those sessions was never measured and must read as unmeasured.

### How the migration runs

Automatically, on `Receipts.__init__`, via `_MIGRATIONS`. Additive `ALTER TABLE` only.
A pre-existing row survives with NULLs — asserted by
`test_J5b_an_OLD_database_is_MIGRATED_not_merely_RESTAMPED`.

**Nothing is needed from any consumer.** No coordination window; v1 queries keep working.

### The version stamp now means something (J5b)

Before this round the stamp was written from the code's own constant, unconditionally,
**after** `executescript`. So opening a v1 DB with v2 code left the v1 table shape in
place (`CREATE TABLE IF NOT EXISTS` cannot add a column) and then relabelled it `2`.

The module docstring claimed the stamp existed "so a Tier-2 consumer can refuse an
unknown version rather than guess at it." A stamp its own writer overwrites on every
open can never disagree, so it could never refuse. Measured before it was fixed: a probe
opened a v1 DB with `SCHEMA_VERSION = 2` and a new column, and got stamp `2` with the
column absent.

Order is now **read → migrate-or-refuse → stamp**:

- **older DB** → migrated forward, then stamped.
- **newer DB** (`found > SCHEMA_VERSION`) → `SchemaVersionError`, and the DB is **not**
  restamped. Reading evidence with the wrong column expectations yields confident wrong
  answers, which is worse than an error. Restamping on refusal would destroy the very
  fact that caused the refusal, so the second attempt would succeed and be wrong.
- **unparseable stamp** → `SchemaVersionError`.

Consumers should expect `SchemaVersionError` from `Receipts(...)` and surface it rather
than catching it.

### Verification

Five rows, each run against its own mutation with the first killer recorded:
`test_J5_a_PASSING_agent_session_records_what_it_was_GRANTED`,
`test_J5_a_MISSING_grant_is_stored_as_NULL_not_as_an_empty_list`,
`test_J5b_an_OLD_database_is_MIGRATED_not_merely_RESTAMPED`,
`test_J5b_a_NEWER_database_is_REFUSED_rather_than_guessed_at`,
`test_J5_the_runner_CARRIES_the_grant_to_the_ledger`.

The last of those was added because the first mutation pass found the column-writing
correct and the **wiring** absent: deleting `result.extra` from the runner's call site
left the suite green. Four rows certified that `record_agent_session` stores a grant
handed to it, and none certified that anything ever hands it one. That is the WIRING
axis, landing on a finding about wiring.

### Known gap, stated rather than closed

`permission_mode` records what the **harness reported**. It does not record the host's
`~/.claude/settings.json` `defaultMode`, which on this host is `bypassPermissions` and
was H1's root cause. Reading that at run start and recording it on `sessions` is queued
(jack-ryan's H6 amendment) and is **not** in v2.
