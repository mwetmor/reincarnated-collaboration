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

### Known gap, stated rather than closed — CLOSED in v3

`permission_mode` records what the **harness reported**. It does not record the host's
`~/.claude/settings.json` `defaultMode`, which on this host is `bypassPermissions` and
was H1's root cause. Reading that at run start and recording it on `sessions` is queued
(jack-ryan's H6 amendment) and is **not** in v2.

*Closed by v2 → v3 below. The paragraph stays because a gap that was open for a version
is part of what a v2 row means, and a reader querying v2 rows needs to know it.*

---

## v2 → v3 — the limits of the measurement become part of the measurement (Gate-2 H6)

**Shipped:** round sixteen, 2026-08-11. **Author:** star-lord.
**Blast radius:** additive. Every v1/v2 query returns identical results against a v3 DB.

### What changed

Four columns added to `sessions`, all nullable, no defaults:

| column | type | meaning |
|---|---|---|
| `host_permission_mode` | TEXT | `permissions.defaultMode` as `~/.claude/settings.json` states it |
| `host_permission_source` | TEXT | the sentence naming *which file* that came from and *which layers were not resolved* |
| `measured_trees` | TEXT | JSON array of the trees the run **declared** it would fingerprint (`wf.repos`), written at session open |
| `measurement_limit` | TEXT | the sentence bounding what a green containment verdict means |

New module `factory/host.py` — `read_host_permission_mode()` and
`describe_measurement_limit()`. `Receipts.start_session` gains three optional
parameters (`host`, `measured_trees`, `measurement_limit`); existing call sites that
omit them write NULLs and are unaffected.

### Why — the receipt recorded the fence and omitted the ground

Two facts are true of every run and neither one is visible from inside a phase:

1. **The wall stands on ground the factory does not set.** H1's root cause was
   `~/.claude/settings.json` setting `permissions.defaultMode` to `bypassPermissions`
   — outside the tree, outside the workflow. J1 then measured that `--allowedTools`
   does **not** restrict in headless `default` mode, so the argv is not evidence of the
   grant either. v2 recorded what the harness reported about itself. Nothing recorded
   what the host had already decided before the harness started.
2. **The wall only ever looked at `wf.repos`.** A phase with unrestricted `Bash`
   reaches the whole filesystem. "0 breaches" is a claim about a bounded region, and
   before v3 the boundary appeared nowhere on the receipt.

Neither is a defect in the wall. Both are defects in what the receipt *claims* the wall
established — the recurring shape of this whole review series, arriving one level up: a
narrower answer wearing the wide answer's clothes.

### NULL semantics — read this before writing a query

- `host_permission_mode IS NULL` — the mode was **not stated or not readable**. The
  `host_permission_source` sentence distinguishes the four cases (`UNREAD`,
  `UNPARSEABLE`, `UNSTATED`, and — on a pre-v3 row — both columns NULL, meaning the run
  never looked).
- `host_permission_mode` is **never** filled with Claude Code's own fallback,
  `"default"`. That value would be correct on every host that has not changed the
  setting and unfalsifiable on the ones that have. It is `usage.py`'s zero-filled-token
  defect moved from cost to containment, and it is refused by
  `test_H6_an_UNSTATED_host_default_is_NULL_not_the_fallback`.
- A consumer that writes `COALESCE(host_permission_mode, 'default')` has converted "we
  did not measure" into "the host was ordinary."
- `measured_trees = '[]'` — the run declared **no** tree, so there is no containment
  evidence on it at all. `IS NULL` — the run did not record its scope. Different facts.
- `measured_trees` is the **declared** scope, not a post-hoc list of what got
  fingerprinted. It is written at session open, before the first phase runs. On any run
  that reaches a phase the two coincide; on a run that aborts earlier they diverge, and
  the column still tells you what was *in scope* — which is the question a reader of an
  aborted receipt is actually asking. The v3 shipping note called this "the trees
  actually fingerprinted", which was H6's own defect committed inside H6's fix: a name
  answering a question about the measurement while the value answers a question about
  the declaration. Corrected in round seventeen (Gate-2 JR-1); **the stored values did
  not change and no migration is required** — only the claim made about them.

Rows migrated from v1/v2 carry NULL in all four columns and are **not backfilled**. The
host default for a run that predates this measurement was never measured and must read
as unmeasured forever.

### What this column set does NOT resolve

`host_permission_mode` is **one layer**. Claude Code resolves enterprise policy, CLI
flags, environment, project `.claude/settings.json`, `.claude/settings.local.json`, and
the user file. This reads the last of those. That limit is written into every
`host_permission_source` value rather than into this document alone, so a query that
returns the mode cannot separate it from its caveat.

(Measured on this host: `~/.claude/settings.json` states `bypassPermissions`; the
meta-repo's `.claude/settings.local.json` has an `allow` list and no `defaultMode`; the
meta-repo has no `.claude/settings.json`. So the layers do stack here, and reading one
of them is a partial measurement — named, not papered over.)

### The surface renders it on the GREEN path

`report.render_run_report` emits a `## What was measured — and what was not` section on
**every** run, not inside `if breaches:`. Green is where the over-claim happens: "0
breaches" invites the reading "nothing was written". A caveat that only prints when
something went wrong is a caveat no reader of a green report ever sees. Asserted by
`test_H6_the_caveat_is_rendered_on_a_run_with_NO_breaches`, whose premise assertion
requires the breach section to be absent so the row cannot pass on the other mechanism.

### How the migration runs

Automatically, on `Receipts.__init__`, via `_MIGRATIONS[1]`. Additive `ALTER TABLE`
only. A pre-existing v2 row survives with NULLs — asserted by
`test_H6_a_v2_database_is_MIGRATED_to_v3_and_its_rows_survive` against a hand-built v2
fixture (built by hand rather than by dropping columns from the current schema: a
fixture assembled by mutating today's code cannot represent a DB written months ago).

**Nothing is needed from any consumer.** No coordination window; v1 and v2 queries keep
working.

### Verification

Thirteen rows in `tests/test_host.py`, each run against its own mutation with the first
killer recorded. The four load-bearing ones:

- `test_H6_an_UNSTATED_host_default_is_NULL_not_the_fallback` — kills the zero-fill.
- `test_H6_the_PRODUCTION_default_path_resolves_through_the_users_home` — the ROUTE
  row. Every other host row passes an explicit path, so all of them would stay green if
  the no-argument default pointed somewhere that does not exist. This one moves
  `Path.home()` and watches the real default follow, which is only possible because
  `default_settings_path()` resolves at call time rather than at import.
- `test_H6_a_RUN_records_the_host_default_it_ran_under` — the WIRING row, written
  because J5's first mutation pass found the column-writing correct and the call site
  absent.
- `test_H6_the_caveat_is_rendered_on_a_run_with_NO_breaches` — the green path.
