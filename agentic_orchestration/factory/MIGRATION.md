# factory — cross-seam schema + surface migrations

Schema custody: **star-lord** (SOFTWARE FACTORY strategy § 8). This file is the
cross-seam contract for the factory's durable surfaces, per ADR-004. Any consumer that
reads `receipts.db` — the CLI `status` / `report` surfaces, a future Tier-1/2 UI,
jack-ryan's Gate-2 queries — reads this file first.

**As of 2026-08-24 this file also covers the VENDOR-LANE surfaces** (`_run-log.tsv`,
`telemetry.jsonl`, `jobs/*.job.json`) — the surfaces the U-1 flight recorder, the fleet
board, and knight-rider's session-start liveness check build against. See the
**codex-lane v0** and **vendor-lane v1** entries at the bottom.

> **If you read one thing in this file, read THE SAFE-TO-FIRE PREDICATE.** A vendor
> lane is safe to fire when its answer state is **`open` or `queue-pending`** —
> `factory.lane_status.SAFE_TO_FIRE_STATES`. Bind to that name. Do NOT re-derive it
> from *"last `_run-log.tsv` row terminal"*: that reading is leg 3 alone, it is
> pre-Amendment-A, and it reports **busy on backlog**, which wedges a lane holding a
> deliberately parked job. Full contract in **vendor-lane v1 § 1**.

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

---

## vendor-lane v1 — the cross-session busy check + the Grok lane (2026-08-24)

**Shipped:** 2026-08-24. **Author:** star-lord.
**Authority:** lane spec `gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md`, **ratified by jack-ryan 2026-08-24 with Amendments A–I** (`gandalf/requests/2026-08-24-jack-ryan-lane-spec-ratification.md`, both passes). Build items **D-1…D-8**.
**Blast radius:** additive at every durable surface. `receipts.db` untouched at v3. The `_run-log.tsv` column count is unchanged at 6. One BEHAVIOURAL change to an existing exit code is named in § 3 below and it is a **correction of a defect**, not a widening.

Consumers this file is written for: the U-1 flight recorder, drax's fleet board
(`flight/bin/flight_report`, `factory/ui/board.py`), knight-rider's dispatch router
(U-4 question 3 and the § 10.3 selection law), and any session asking *"may I fire at a
vendor lane?"*.

---

### 1. THE SAFE-TO-FIRE PREDICATE — pinned by state name (Amendment H)

> **A vendor lane is SAFE TO FIRE when its answer state is `open` or `queue-pending`.**

That is the whole predicate. It has one home in code —
`factory.lane_status.SAFE_TO_FIRE_STATES` — and it is pinned by equality in
`tests/test_vocabularies.py`.

**Bind to this. Do not re-derive it.** In particular, do **not** bind to *"last
`_run-log.tsv` row terminal"*, which is what U-4's question (3) said before Amendment
A. That reading is leg 3 alone and it reports **busy on backlog**: `ENQUEUED` is a
member of `BUSY_MARKERS`, so `RunLog.is_idle()` returns False whenever a job is
enqueued and undrained. Compose that with P-9 — *an ENQUEUED-but-not-drained job IS the
held state*, and a hold persists as long as its named condition takes to resolve — and
one deliberately held job renders the lane permanently unusable to every other job and
every other session. `is_idle()` is still exported and still correct about what it
measures; it is simply not the fire predicate and never was.

The three routing dispositions **partition** the answer vocabulary:

| Disposition | States | What a dispatcher does |
|---|---|---|
| **SAFE TO FIRE** | `open`, `queue-pending` | fire now |
| **OCCUPIED** | `busy-lock`, `busy-out-of-band`, `busy-unknown` | **enqueue** behind it — the lane exists and works |
| **CLOSED** | `auth-expired`, `cli-missing` | the lane cannot take the work at all |

§ 10.3's Claude branch is reachable only when **both vendor lanes are CLOSED** (or both
are OCCUPIED and the run is schedule-critical, under the R-A ledger note). *Occupied is
not closed*, and *`queue-pending` is not occupied* — those two sentences are Matt's
verbatim floor expressed in this vocabulary.

---

### 2. THE EXIT-CODE TABLE — pinned

`factory lane` exits per state. `0` = `open` is the only value the spec imposed; the
rest are chosen here and pinned so no consumer discovers them by experiment.

| Exit | State | Band |
|---|---|---|
| `0` | `open` | fire |
| `10` | `queue-pending` | fire |
| `20` | `busy-lock` | occupied |
| `21` | `busy-out-of-band` | occupied |
| `22` | `busy-unknown` | occupied |
| `30` | `auth-expired` | closed |
| `31` | `cli-missing` | closed |
| `2` | argparse usage error | — (argparse's own convention, not ours) |

**The band is part of the contract:** every fire-safe state is `< 20`; every occupied
or closed state is `>= 20`. A shell caller may rely on `[ $? -lt 20 ]`. An unknown
state exits `22`, never `0`.

`--safe-to-fire` collapses the answer to one bit — `0` = fire, `1` = do not — for
callers whose only question is *"may I fire?"*. Amendment A required `open` and
`queue-pending` to be **separately identifiable by exit code** while the spec required
`0` = safe-to-fire; those pull in opposite directions, and the resolution is two
questions rather than one collapsed answer.

For `--lane all` (the default) the exit code is the **worst lane's** code under the
fail-closed precedence, so a caller reading only the exit code is never told "open"
while a lane is occupied. `--safe-to-fire` at that scope answers the **selection law's**
question instead: is there *any* vendor lane I may fire? The per-lane answers are always
on stdout and in `--json`.

---

### 3. BEHAVIOURAL CHANGE — `factory lane-status`'s exit code

**Before:** `return 0 if (state.ok and queue.runlog.is_idle()) else 1` — exit `1` ("do
not fire") for a lane on which nothing was executing, whenever any job sat enqueued.

**Now:** the command returns the busy check's per-state exit code (§ 2), computed from
the same named predicate every other consumer uses.

**Consumer impact:** a caller that tested `rc == 0` still gets *"open, nothing
queued"*. A caller that tested `rc != 0` as *"do not fire"* now correctly gets a
fire-safe `10` on backlog. If you consume this command from a script, move to
`factory lane --safe-to-fire`, which is the surface built for that question. Two new
flags: `--lane codex|grok` and the printed `CHECK :` line carrying the composite.

---

### 4. NEW MODULE — `factory/lane_status.py` (D-1, D-2, D-7)

Three legs, unioned fail-closed over **execution occupancy only**:

| Leg | Surface | Sees | Blind to |
|---|---|---|---|
| 1 | kernel `flock` probe | every lock-taking invocation, zero staleness | an invocation that never took the lock |
| 2 | `ps -axo pid=,args=` | **out-of-band invocations** — hand-fires, a live agent session, Matt's terminal | another machine |
| 3 | run-log last row per job | in-flight `START`-without-finish; backlog | hand-fires that wrote no row |

Public surface a consumer may bind to: `lane_status()`, `all_lane_status()`,
`select_lane()`, `safe_to_fire()`, `exit_code_for()`, `scan_process_table()`,
`SAFE_TO_FIRE_STATES` / `CLOSED_STATES` / `OCCUPIED_STATES` / `EXIT_CODES` /
`VENDOR_ORDER` / `LANES`.

**THE LAW — this module writes nothing.** No row, no telemetry event, no surviving
file touch. Two consequences are structural rather than aspirational: it never imports
`RunLog` or `Telemetry` (asserted over the AST), and leg 1 is only probed when the lock
file **already exists**, because `lane_is_free()` opens with `O_CREAT` and asking
blindly would make a read-only status call create a file that outlives it.

**Blast radius is PER-VENDOR (Amendment B).** An unattributable out-of-band process
counts busy against every lane of *that vendor* and never crosses vendors. Leg 2's
attribution failure is *which credential home*, not *which vendor* — the vendor is
legible from the argv that matched. Two tests hold this in both directions.

**One declared extension to the spec's six answer states:** `busy-unknown`, for a leg
that was UNREACHABLE when no reachable leg reported occupancy. The § 3 vocabulary
assumes all three legs answer; reporting `open` on a lane whose lock we could not read
would be false-open, the one direction G-2 ruled against. The spelling is taken from
drax's fleet-board card deliberately — one question must not have two vocabularies.

**Note for drax:** `flight/bin/flight_report` currently carries `PROBE_MODE =
"degraded — D-2 CLI pending"` and reimplements the three legs. The CLI now exists.
Rendering `factory lane --json` (or importing `factory.lane_status`) would make the
card a view of the check's own derivation rather than a second implementation of it —
which is what Q62's instrument caveat asks for. The vocabularies already agree,
including `busy-unknown` and the `STATE_PRECEDENCE` ordering. No coordination window;
the current card keeps working.

---

### 5. NEW LANE — `grok` (D-6)

Registered as `grok` in `factory.harness`. `available_harnesses()` now returns
**three** names; a consumer asserting a set of two will fail (one test in this repo
did, and was renamed rather than relaxed).

| Fact | Value |
|---|---|
| Binary | `~/.grok/bin/grok` — **NOT on PATH**, resolved explicitly |
| Binary override | `$REINCARNATED_GROK_BIN` |
| Credential home | `~/.grok`, override `$GROK_HOME` |
| Model pin | `grok-4.6`, argv-said (`-m`) |
| Effort pin | `xhigh`, argv-said (`--reasoning-effort`), from job one (Amendment D) |
| **Resolved** model | `grok-4.6-build` — captured per call from `modelUsage` (Amendment C) |
| Invocation of record | `grok -p "<prompt>" --output-format json --no-leader --permission-mode default --disable-web-search` |
| Auth check of record | `grok models` → rc=0 + a "logged in" line |
| Lock | `SerialLaneLock` keyed to `~/.grok`, `pass_fds` lifetime discipline identical to Codex |
| Fence | `--permission-mode` (from `{default, acceptEdits, auto, plan}`) + `--disable-web-search`; `bypassPermissions` and `dontAsk` refused BY NAME |
| Prompt transport | argv (`-p`), with a declared ceiling of 256 KB and `--prompt-file` named as the door past it |

**The pin is DECLARED, not BANKED.** Zero lane statistics exist at any Grok config; the
first 10 production jobs are the banking window (Amendment I), and every row carries
curator + resolved model id + declared effort + per-call `cost_usd`. *(This sentence
was false when first written — the effort was on the argv and in the telemetry but not
on the row. Gate-2 finding **G2-1**; the field was added rather than the claim struck,
see § 7. And every one of those rows carries the per-job input floor of § 10.1 inside
its token and cost figures — read the window against it, not against zero.)*

**Amendment E is a hard preflight.** `--no-leader` is accepted by the CLI but is
**absent from `grok --help`** (documented only under `grok agent`). The harness asserts
the flag parses — `grok --no-leader --version`, rc check plus the absence of the
`unexpected argument` sentence, no model call, no cost — and **refuses to fire** on
failure. A version bump could remove the flag with no help-diff to signal it, and the
failure would be silent re-entry through the concurrency door the lock exists to close.

**Serial-by-CHOICE, not by law.** The Codex serial rule is a verified vendor
precondition. No equivalent xAI statement has been verified, so the Grok lane is
serialised as *our policy*. Same primitive, two kinds of rule; a reader who cannot tell
them apart will defend the policy as if it were the law.

**Cross-vendor parallel is LEGAL.** Different credentials, different locks, different
lock filenames (`codex-<digest>.lock` / `grok-<digest>.lock`). A busy Codex lane does
not close the Grok lane.

---

### 6. Per-lane run-log locations (D-8)

| Lane | Path | Format |
|---|---|---|
| `codex` | `agentic_orchestration/lanes/codex/_run-log.tsv` | 6-column |
| `codex` (historical) | `agentic_orchestration/research/vfx-p2-dossiers/usage/_run-log.tsv` | 4-column, written at close; read without complaint |
| `grok` | `agentic_orchestration/lanes/grok/_run-log.tsv` | 6-column **from its first row** |

The Grok log is **born with the curator column and with enqueue-time rows** — that lane
never has a rows-at-close era, because P-10 applies to it from birth and it has no
hand-fire era at all. Both paths are declared in `lane_status.LANES` and
`lane_status.CODEX_RUNLOGS`; leg 3 reads them, and an absent file is *"no queue claim"*
rather than an error.

Queue-root documentation: `agentic_orchestration/lanes/README.md` (the check
invocation, the state table, and the pure-shell degraded fallback).

---

### 7. Run-log DETAIL column — new tokens (D-3, C, D, I). No schema change.

Column 4 is free-form `k=v`, and it gains four conventions. The column COUNT is
unchanged at 6 and every existing reader is unaffected.

| Token | Row | Meaning |
|---|---|---|
| `router=Q3-NO` | enqueue | the four-question router cleared the job but answered NO to (3) *lane open?* — so it queued. Makes lane contention countable: `grep -c "router=Q3-NO"` |
| `resolved_model=<id>` | finish | Amendment C — the model the vendor actually billed, not the declared pin |
| `effort=<level>` | finish | Amendment D — the DECLARED reasoning effort the invocation asked for. **Added at Gate-2 (finding G2-1)**; see below |
| `cost_usd=<n>` | finish | Amendment I — per-call cost where the vendor reports one; **absent when it does not**, never zero-filled |

**`effort=` — why it exists, and what its absence means (G2-1).** Amendment D reads
*"the pilot declares its effort value explicitly on the argv **and records it in the
run-log row**."* Through `dddd232d` it was honoured on the argv (`--reasoning-effort
xhigh`) and in `telemetry.jsonl` (`reasoning_effort`) but **not on the row** — while
§ 5 of this document asserted that every row carried it. jack-ryan ruled the gap WARN
and named the choice: carry the field, or strike the claim. **The field is carried**,
because the surface Amendment I names for the banking window is the run-log, and a cost
column read beside a resolved model but *not* beside its effort level attributes an
effort change to the model (#10 — change one thing, measure one thing).

The value is read from the harness result's `extra`, not from the module's pin
constant, so a job that overrides the pin records **what it asked for** rather than
what the constant says. **Absent is absent**, exactly as for `cost_usd=`: a harness
that reports no effort writes no token, and no default is substituted. A banked row
stating an effort level nobody measured is worse than one stating none, because the gap
is detectable and the default is not — that is G2-1's own defect rebuilt on the other
side, and `test_grok_harness.py::test_G2_1_a_harness_that_reports_NO_EFFORT_gets_no_FABRICATED_one`
holds the line.

The Codex fence still reads `sandbox=<mode>`; the Grok fence reads
`permission_mode=<mode> web_search=on|off`. A Grok job declaring a `sandbox:` value is
**refused** — accepting it would let a job record read as fenced while the invocation
was not.

---

### 8. `AUTH-BLOCKED.md` is now vendor-generic

Same filename (knight-rider's filing habit and the `lane-status` check both look for it
by name), but the content names **which lane** and **which state**: heading
`# <lane> lane BLOCKED`, and the re-login command is the right one per vendor. A Grok
block no longer reads as a Codex one. Still not filed by the queue — knight-rider files
it.

---

### 9. Signature change — `lane.default_lock_path`

```python
default_lock_path(home=None, vendor="codex") -> Path
```

The first parameter was `codex_home`; it is now `home`, and `vendor` is new with a
backward-compatible default. **`default_lock_path()` with no arguments returns exactly
the path it always did**, which matters because `flight/bin/flight_report` calls it
that way and a rename would have pointed that view at a lock nobody takes. Callers
passing the old keyword `codex_home=` by name must switch to `home=`; no caller in this
repo did.

The vendor is part of the FILENAME, not merely of the digest, so
`ls ~/.reincarnated/lane-locks/` names the holder without resolving a sha256. An
undeclared vendor **raises** rather than defaulting a credential home.

---

### 10. `UsageBreakdown.from_grok_envelope` — and the containment question, settled

The Grok envelope is the **Anthropic wire shape**, not Codex's:
`cache_read_input_tokens` / `cache_creation_input_tokens` / `total_cost_usd` /
`modelUsage` / `num_turns`. Cache tokens are therefore **siblings** of `input_tokens`,
not a subset of them — the opposite of the Codex mapping, where passing input through
unchanged would double-count the cache.

This is settled by **the vendor's own arithmetic**, not by inference. The live smoke job
of 2026-08-24 reported `input 28,170 · cache_read 2,432 · cache_creation 0 · output 43`
and `total_tokens 30,645`, and `28170 + 2432 + 0 + 43 = 30,645` exactly. The subset
reading would have given 28,213, which matches nothing the vendor reported.
`billable_token_total()` reproduces `total_tokens` exactly on this lane.

`total_cost_usd` is recorded with `dollars_source = "harness_reported_imputed"`: the
credential is a **grok.com subscription**, so the figure is a list-price imputation and
no downstream report may present it as money billed. Reasoning tokens remain a **share
of output**, never a fifth addend.

#### 10.1 · `GROK_CLI_INPUT_FLOOR_TOKENS` — a NAMED MEASURED QUANTITY (Gate-2 finding G2-2)

> **`GROK_CLI_INPUT_FLOOR_TOKENS = 28_170`** — the fixed, CLI-injected input context
> billed on **every** Grok-lane job, independent of the prompt.
> **Measurement of record:** job `smoke-grok-lane-2026-08-24`, `lanes/grok/_run-log.tsv`
> + `lanes/grok/telemetry.jsonl` — a **one-line prompt** that reported
> `input 28,170 · cache_read 2,432 · cache_creation 0 · output 43`, `total 30,645`,
> `total_cost_usd 0.00983`. Declared in code at
> `factory/harness/grok.py::GROK_CLI_INPUT_FLOOR_TOKENS` so a consumer binds to the
> number rather than re-typing it.

The arithmetic above settles what the fields *mean*. This settles what the measurement
*costs*, which is a different question and the one Amendment I's banking window turns on.
**28,170 input tokens on a one-line prompt is not the prompt** — it is a fixed context the
CLI injects on every call, and it is therefore a **per-job floor** rather than per-job
model spend.

**The rule this imposes on the Amendment-I window (BINDING, per discipline #10 — change
one thing, measure one thing).** The window compares Grok's first ten *production* jobs
against Codex's banked baseline. Every one of those ten rows carries this floor inside its
`tokens=` and `cost_usd=` figures. So:

1. **Attribute the floor as FIXED OVERHEAD, never as per-job model spend.** The per-job
   marginal figure is `tokens − 28,170 − cache_read`, and a comparison against Codex that
   skips this subtraction is measuring *the CLI's context injection* while reporting *the
   model's cost*.
2. **`$0.00983` for 43 output tokens is the number that will mislead.** Read alone it says
   this lane is expensive; read beside the floor it says ~99.9 % of that call was fixed
   overhead. Anyone meeting the figure without the floor beside it draws the wrong
   conclusion, and the whole point of recording it here is that they cannot.
3. **A cost anomaly is measured against the floor, not against zero.** Star-lord's standing
   >2× rule applies to the marginal component; a job whose *total* is 2× the floor may be
   entirely ordinary.

**What this quantity is NOT (stated so the number is not over-trusted).** It is **n = 1**.
It was measured once, on one prompt shape, at one CLI version (`~/.grok/bin/grok` v1.0.5)
and one model pin (`grok-4.6` → resolved `grok-4.6-build`). The prompt's own tokens are
*inside* the 28,170, so the figure is an **upper bound on the fixed component**, not an
exact split — with a one-line prompt the difference is small but it is not zero. Nothing
here establishes that the floor is constant across prompt sizes, efforts, or CLI versions;
the ten banking jobs are the first evidence that could, and a floor that moves is itself a
finding worth the row. **A CLI version bump invalidates this measurement and requires a
re-probe** — which is exactly the reason it is written down with its provenance instead of
carried as a remembered number.

---

### 11. What a consumer must do

**Nothing is breaking.** No coordination window; `receipts.db` is at v3, untouched.

Two things a consumer **should** do:

1. **Bind to the predicate**, not to a leg (§ 1). If you currently ask *"is the last
   run-log row terminal?"*, you are asking a pre-Amendment-A question that reports busy
   on backlog.
2. **Do not freeze the telemetry shape.** `telemetry.jsonl` carries
   `schema_version` and a `passthrough` object on every record precisely so that a
   recorder can normalise later against U-1 axes that are Matt's F-1…F-8 to rule and
   are not ours to fix.
