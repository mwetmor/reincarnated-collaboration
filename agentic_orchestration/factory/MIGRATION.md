# factory — cross-seam schema + surface migrations

Schema custody: **star-lord** (SOFTWARE FACTORY strategy § 8). This file is the
cross-seam contract for the factory's durable surfaces, per ADR-004. Any consumer that
reads `receipts.db` — the CLI `status` / `report` surfaces, a future Tier-1/2 UI,
jack-ryan's Gate-2 queries — reads this file first.

**As of 2026-08-24 this file also covers the VENDOR-LANE surfaces** (`_run-log.tsv`,
`telemetry.jsonl`, `jobs/*.job.json`) — the surfaces the U-1 flight recorder, a future
board, and knight-rider's session-start liveness check will build against. See the
**codex-lane v0** entry at the bottom.

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

---

## codex-lane v0 — the vendor lane becomes a durable queue (U-4, 2026-08-24)

**Shipped:** 2026-08-24. **Author:** star-lord.
**Dispatch:** `agentic_orchestration/dispatches/2026-08-24-star-lord-codex-durable-queue.md`
**Blast radius:** one BEHAVIOURAL contract change (below), plus three NEW surfaces that
nothing consumed before. No existing consumer of `receipts.db` is affected; its schema
is unchanged at v3.

### 1. BEHAVIOURAL CONTRACT CHANGE — `codex.available()` flips `False → True`

This is the one item in this entry that changes what already-written code does, so it
is first.

`harness/codex.py` was an honest stub: `HONEST_STUB = True`, `available()` returned
`False` unconditionally, `run()` raised `NotImplementedError`. `workflow.py` reads
`available()` at LOAD and refuses any agentic phase naming a closed lane. **A workflow
declaring `harness: codex` used to be rejected at load, always. It is now ACCEPTED
whenever `codex login status` is healthy and the serial lane is free.**

What that means for the spine: the loader will now ROUTE work to a second vendor. Any
workflow that named `codex` as a placeholder — expecting the load-time refusal to keep
it from running — will now run. There is exactly one such workflow shipped
(`workflows/kc2-baton-mechanical.yaml`) and it does not name `codex`; a grep for
`harness: codex` across the repo returns nothing else. Named here anyway, because a
contract change whose blast radius is currently zero is still the change that bites when
the radius stops being zero.

`HONEST_STUB` and `BLOCKED_ON` are **DELETED**, not left beside the working body, and
`tests/test_no_stub_gates.py` now asserts they are absent. The stub carve-out in that
file (`flagged == [codex.py]`) became `flagged == []` — the same equality, one exemption
smaller.

**`available()` was NOT promoted onto the `HarnessAdapter` Protocol — an explicit
decision, not an oversight.** `base.HarnessAdapter` still declares only `name` and
`run`; `available()` remains duck-typed at `workflow.py:196`. Promoting it makes
`ClaudeCodeHarness` non-conforming to the protocol it is the reference implementation
for, and both repairs are worse than the status quo: give the Claude lane an
`available()` returning `True` (a green nobody measured, in a package whose loudest rule
forbids exactly that), or make it probe `claude` on every workflow load (a subprocess
per load to answer a question that lane has never needed asked). Duck-typing says the
true thing: a lane that can answer "am I open?" answers; a lane that cannot is not
asked.

**New optional adapter method: `unavailable_reason() -> str`.** `workflow.py` now asks
the ADAPTER for the reason a lane is closed and falls back to the module-level
`BLOCKED_ON` only if the adapter does not answer. This is additive — a harness
publishing only `BLOCKED_ON` keeps its exact message. It exists because `BLOCKED_ON` is
fixed at import time, which was adequate for one closed state ("Matt has not installed
it") and is not adequate for a live lane with three (`auth_expired`, `busy`,
`cli_missing`), which an operator must be able to tell apart: one needs Matt, one needs
a minute, one needs a PATH.

### 2. NEW SURFACE — `_run-log.tsv`, extended ADDITIVELY

The proven runner (`research/vfx-p2-dossiers/run_p2_serial.sh`) wrote four
tab-separated columns. **Those four columns are unmoved.** Two are appended:

| col | field | example | new? |
|---|---|---|---|
| 1 | `ts_utc` | `2026-08-24T14:03:40Z` | no |
| 2 | `job_id` | `30-ma_video_companion` | no |
| 3 | **`marker`** | `rc=0` · `SKIP-EXISTS` · `ENQUEUED` · `START` · `FALLBACK-CLAUDE` · `AUTH-BLOCKED` · `ENQUEUE-REFUSED` | no (vocabulary widened) |
| 4 | `detail` | free-form `k=v k=v` | no |
| 5 | **`curator=<agent>`** | `curator=elrond` | **YES** |
| 6 | `event=<enqueue\|start\|finish>` | `event=enqueue` | **YES** |

**THE LIVENESS CONTRACT IS PRESERVED AND IS THE POINT.** The pre-fire check of record —
*"last row terminal"*, which the U-4 router's question (3) reads and which knight-rider
reads at session start — is still `tail -1`, and still column 3:

```sh
tail -1 usage/_run-log.tsv | cut -f3        # rc=0  -> lane idle
tail -1 usage/_run-log.tsv | cut -f5        # curator=elrond
```

Asserted by `test_the_terminal_check_is_answerable_by_TAIL_MINUS_1_AND_CUT`, which runs
that exact shell pipeline rather than simulating it.

**Reading rules a consumer must not get wrong:**

- **Four-column rows are legal and must stay readable.** Every row the proven 30-job
  VFX run wrote has four columns. `RunLog.curator_of` returns `None` for them, meaning
  **UNKNOWN**, and a governance-leak query must not read that as "empty". The pre-R-B
  corpus has no curator field; it does not have an empty one.
- **`ENQUEUED` and `START` are NON-terminal.** A log ending in `ENQUEUED` means the
  lane is idle but has pending work; ending in `START` means a job was launched and no
  finish row followed it — a crash, or a job still running. Both correctly read as *do
  not fire*.
- **An unrecognised marker is NON-terminal**, and `RunLog.append` now REFUSES to write
  one. Column 3 is a closed vocabulary in both directions.
- `rc=<N>` is matched by PREFIX, any exit code, exactly as the proven runner wrote it.

### 3. NEW SURFACE — `telemetry.jsonl` (U-1(a) emission, schema DELIBERATELY NOT frozen)

Append-only JSONL, one event per line. `schema_version` is
`reincarnated.lane.telemetry/0.1`.

> **DO NOT BUILD A CONSUMER THAT DEPENDS ON THE TOP-LEVEL SHAPE.** The U-1 fleet
> flight-recorder record schema is Matt's F-1…F-8 rulings and jack-ryan has not
> ratified its axes. This emission exists so the FACTS are on disk and findable when
> the recorder is specified; it does not pre-empt the axes. Every record carries a
> permissive `passthrough` object for exactly that reason: a normaliser must have
> somewhere to have found the fact it needs.

Events: `enqueue` · `start` · `attempt_failed` · `finish` · `lane_blocked`.
Facts present across the lifecycle: enqueue/start/finish timestamps (`ts_utc` +
`ts_epoch`), `job_id`, `curator`, `lane`, `model`, `reasoning_effort`, `exit_code`,
`usage` (a `UsageBreakdown` dict), `attempt`, `fallback`, `outcome`, `error`.

**Absent is absent.** A fact the queue does not know is OMITTED, never zero-filled —
the `start` event carries no `model`, because the queue does not know which model the
harness will pin and a guess beside the finish event's measured value is worse than a
gap.

**Discipline #73 is enforced mechanically here, not by convention.** No lane module
reads a dispatch `**Status:**` header, emits a work-state claim, or references
`dispatches/` in executable code, and
`test_DISCIPLINE_73_no_lane_module_reads_a_dispatch_Status_header` proves it over the
AST (non-docstring string constants only, so the modules can DESCRIBE the rule without
tripping the scan). The marker vocabularies are separately asserted to contain no
work-state term (`SEALED`, `COMPLETE`, `PENDING`, …), because a board rendering lane
data must not be able to project a work-state claim through it.

### 4. NEW SURFACE — `jobs/<id>.job.json`

`schema_version` `reincarnated.lane.job/0.1`. Written atomically (tmp + `os.replace`).
Fields: `job_id`, `curator`, `job_class`, `prompt_path`, `output_path`, `sandbox`,
`skip_git_repo_check`, `web_search`, `ephemeral`, `min_output_bytes`, `max_attempts`,
`timeout_s`, `enqueued_at`, `enqueued_by`, `schema_version`, `extra`.

**U-4 R-B is SCHEMA here, not convention.** `curator` is a required field, refused at
enqueue when empty, and written into the `_run-log.tsv` row **at enqueue time**. A job
that cannot name its curator does not enqueue, and nothing is written when the refusal
fires — no job record, no prompt file, no run-log row. Enqueue-time is the whole point:
a curator recorded at close is one chosen after seeing the output, which is an
endorsement rather than a control. `JobQueue.curator_at_enqueue(job_id)` reads the
ENQUEUE row specifically, so R-B's empirical criterion ("zero governance leaks") is
falsifiable by query rather than by memory.

### 5. `UsageBreakdown.from_codex_turn_completed` — read this before summing anything

`cached_input_tokens` **is a subset of** `input_tokens` in the codex frame, not a
sibling of it. Established from the record, not assumed: the VFX run totals
`input 72,375,471` / `cached 67,431,424`, and `cached / input = 0.9317` reproduces the
banked **93.2 % cache-hit** statistic exactly; the disjoint reading gives 0.4823, which
matches nothing anyone recorded.

So the mapping stores `input_tokens = input - cached` (the UNCACHED share) and
`cache_read_tokens = cached`. Passing the vendor's `input_tokens` through unchanged
would have made `billable_token_total()` count 67 M tokens twice on a 72 M-token run —
a **93 % over-report produced by a mapping that looked like a rename.** Any consumer
recomputing a cache-hit rate from these fields wants
`cache_read / (input + cache_read)`, not `cache_read / input`.

`dollars` is NULL on this lane with a stated `absent_reason`: codex emits no cost
figure at all (unlike the Claude lane's list-price imputation), so a row printed from
this breakdown carries `[INCOMPLETE: ...]` rather than looking whole.

### 6. Model pin

`MODEL_PIN = "gpt-5.6-sol"` @ `MODEL_REASONING_EFFORT_PIN = "xhigh"`, passed **on the
argv**. It previously lived only in `~/.codex/config.toml` — ambient host state no file
in this repository controls. Changing it requires the U-4 A/B evidence template, and
`build_argv` enforces that: a config naming a different model is refused unless it also
names `model_ab_note`.

The pin can be DISPROVED but not CONFIRMED from the stream, and the adapter says so
rather than implying otherwise: no codex frame echoes the model, but an unrecognised
model produces a `Model metadata for X not found` error item, which `adjudicate` treats
as a FAILURE rather than a warning.

### 7. New CLI surface

```
factory lane-status  <queue-dir>          # auth + serial lane + last-row, exit 0 = fire
factory lane-enqueue <queue-dir> <job-id> <prompt-file> --curator <agent> [...]
factory lane-drain   <queue-dir> [--limit N]
```

`--curator` is `required=True` at the argparse layer as well as at the queue layer: a
flag with a default is a flag that gets left off, and the governance line would then be
enforced by whoever typed the command remembering it.

### Nothing is needed from any consumer

There is no coordination window. `receipts.db` is untouched at v3. The `_run-log.tsv`
extension is additive and every pre-existing reader keeps working. The one thing a
consumer MUST do before building on the telemetry stream is read § 3 above and not
freeze the shape.
