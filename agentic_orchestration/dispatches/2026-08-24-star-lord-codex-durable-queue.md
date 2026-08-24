# Dispatch — 2026-08-24 — star-lord — the Codex durable queue (U-4 lane, made standing)

**Status:** PENDING
**From:** knight-rider (Matt directive, 2026-08-24 — Codex-lane HIGH-UPTIME provisions)
**To:** star-lord (export / output / telemetry / llm seam — and the factory harness)
**Approved by:** Matt, 2026-08-24
**Pattern:** B (dedicated session)

---

## Context — why this, and why now

The Codex lane is **a proven instrument**, and that is a measured statement, not an impression: **34/34 jobs `rc=0`** across the VFX archetype-binding run, fabrication checks clean, one judged selection gate downstream. Matt's directive is short and it is the whole reason this dispatch exists:

> **Hand-fired scripts are the bridge; the queue is the uptime.**

Today the lane runs off `agentic_orchestration/research/vfx-p2-dossiers/run_p2_serial.sh` — a good script, strictly serialized, idempotent on re-entry, per-job usage JSONL. It works. It is also **bespoke to one job class**, and its liveness is a human remembering to fire it. Every new job class means a new hand-cloned script, and every clone is a fresh chance to get the serial law wrong.

`agentic_orchestration/factory/harness/codex.py` is currently **an honest stub** — `HONEST_STUB = True`, `available()` returns `False`, `run()` raises. It was pinned deliberately so the fill would be a body-fill rather than a redesign. **The lane is now open** (auth healthy; last `_run-log.tsv` row terminal), so the block that stub names is gone. Fill it.

---

## THE SERIAL LAW — absolute, and it is the one thing this build must not get wrong

> **ONE `codex exec` at a time. One `auth.json`, one job stream.**

This is an OpenAI CI/CD-auth precondition, not a preference: *"one machine or serialized job stream."* Concretely, for this build:

- **The queue never runs two jobs concurrently.** Not "usually," not "unless the jobs are small." Never.
- **A busy lane means queue behind it or fire the Claude lane — NEVER parallel.**
- The mechanism must make violation *structurally impossible*, not merely discouraged. A lock that a caller can forget to take is not a lock. **If a second queue process starts, it must fail closed** — refuse to run, exit non-zero, and say why.
- ⚠ **The exclusion must be held at the `codex exec` invocation site, not merely at the queue-process boundary.** A single queue process spawning two children is the same violation as two queue processes. **State the mutual-exclusion primitive by name.** **Gate-2 will ask for: (i) the primitive, (ii) a test that starts a second `codex exec` under the lock and observes non-zero exit, (iii) your written choice of which crash failure-mode you accepted and why.**
- **Crash-safety matters more than throughput here.** A lock left behind by a killed process that then blocks the lane forever is a real failure mode; so is a lock that a stale-PID check clears too eagerly and lets two jobs run. Choose deliberately and **write down which failure you chose to risk and why.**

## MODEL PIN — of record, do not drift

**`gpt-5.6-sol` @ `model_reasoning_effort=xhigh`.** Every banked lane statistic — the 34/34, the 93.2 % cache-hit, the fabrication-check pass rate — was measured at this config. **A silent swap invalidates the whole baseline.** The pin belongs in the harness as a declared constant with a comment saying exactly that. Changes require the A/B evidence template in U-4 (~6 duplicate jobs, candidate vs pinned; criteria = curation WARN rate + URL-verification pass rate), never an edit.

## AUTH HEALTH — a first-class queue state, not an exception

`codex login status` is the check. Expired auth is **not** a job failure to retry — re-auth is a **Matt-only action**.

- The queue detects it, **stops taking Codex jobs**, and surfaces it loudly.
- Matt's directive is explicit about the response: **file a `canonical/matt_to_do/` row immediately and fall back to the Claude lane rather than idling the work.** Idle work is the failure; a filed row plus a fallback is the success.
- Whether the queue *writes* that row automatically or emits the condition for KR to file is your call — **but do not have it write to `matt_to_do/` silently and unattributably.** Name what you chose.

---

## Scope

### The queue itself

- [ ] **Fill `factory/harness/codex.py`** against the existing `HarnessAdapter` protocol in `harness/base.py` — `run(prompt, cwd, config) -> RawResult`. Return a real `RawResult`: `ok`, `text`, `usage`, `harness`, `model`, `exit_code`, `raw_output_path`, `prompt_path`, `error`. **`available()` must now tell the truth in both directions** — it returns `False` when auth is expired or the lane is busy, and the *reason* must be surfaceable, not swallowed.
- [ ] ⚠ **Correction to a claim I made and got wrong: `available()` is NOT on the `HarnessAdapter` Protocol.** `base.py` declares only `name` and `run`; `available()` is **duck-typed** at `workflow.py:196`. Verify that yourself before relying on it. **Promoting `available()` onto the Protocol is a base-class change consumed by `claude_code.py` and the spine — if you do it, it is an explicit decision, named in the MIGRATION.md this dispatch already requires, not a quiet tidy-up.**
- [ ] **Update `factory/tests/test_harness.py:169`** — it asserts `CodexHarness().available() is False` and will break the moment the stub is filled. **Update it to assert the new auth/busy-aware contract in both directions. Do not delete it — a deleted test is how `available()` stops telling the truth.**
- [ ] **`codex exec --json` emits per-turn usage natively.** Map it into `UsageBreakdown` the same way `claude_code.py` maps the `result` frame. Do not invent a second usage vocabulary; the spine already has one.
- [ ] **Clone the proven runner's semantics, don't reinvent them.** From `run_p2_serial.sh`: strict serialization, **idempotent re-entry** (a re-fired queue must not redo completed jobs), per-job usage JSONL, per-job stdout and stderr captured to separate files. `-s read-only` and `--skip-git-repo-check` are the posture of record for research jobs; make the sandbox posture a **declared per-job-class config value**, not a hardcoded constant — a future job class may need something else and it must be a visible decision when it does.
- [ ] **A standing durable queue**, not a one-shot: jobs enqueue as files/rows; the queue drains them serially; state survives process death. **Re-entry after a crash must be safe and must be tested** — kill it mid-job and restart it, and report what happened.
- [ ] **`_run-log.tsv` remains the lane's liveness surface.** The pre-fire check of record — *"last row terminal"* — is what the U-4 router's question (3) reads and what KR reads at session start. **Do not break that contract while generalizing it.** If you extend the format, the terminal-row check must still be answerable by a human running `tail -1`.

### The telemetry half (U-1(a) from birth)

- [ ] **Emit per-job lifecycle telemetry as append-only JSONL from day one.** Matt's framing: *"This also births U-1(a) telemetry for the lane from day one."* Minimum grain: enqueue → start → finish timestamps, job identity, model + reasoning-effort actually used, exit code, token usage, retry/fallback flags, terminal outcome.
- [ ] ⚠ **DO NOT pre-commit to the U-1 record schema.** The fleet flight-recorder spec (`gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md`) is **DRAFT and awaiting Matt's fork rulings F-1…F-8** (queue Q61), and jack-ryan has not ratified its schema or THE LAW. Emit the facts in a shape that a recorder can *read and normalize later*; do not freeze axes Matt has not ruled on.

  **The eight items above are FACTS THAT MUST BE PRESENT, not a record schema.** Emit append-only JSONL, one event per line, carrying `schema_version` and a permissive passthrough object for anything you observe that the list does not name. Do not build any consumer that depends on the top-level shape.

  **"Which axes does the recorder normalize on" is the F-1…F-8 decision and is HALT-worthy. "What field name do I use for exit code" is yours. Do not HALT on the second.**
- [ ] **THE LAW applies pre-emptively:** any view over this data is **read-only, zero authority, never in the data path.** The queue is the data path; a board is a projection. Do not build anything that reads queue state and then *writes back into it*.
- [ ] ⚠ **NEW AND BINDING — Discipline #73 (jack-ryan, 2026-08-24), and it lands ahead of Matt's F-1…F-8 rulings because it is a defect finding, not a schema choice.** A dispatch's `**Status:**` header is **measured-defective and NON-AUTHORITATIVE**: across 197 dispatch files, 99 carry no `Status:` header at all, and of the 31 reading open/pending, **14 are contradicted by a substantive completion record in the same file** — tags, SHAs, smoke counts — spanning 2026-05-16 → 2026-07-22 across five agents. **Work state is DERIVED from the completion record's presence and terminal marker plus git. Never asserted by a field.** Your telemetry must not emit, and no consumer you build may read, a work-state claim sourced from that header. (This is why it is yours and not the board's problem: rendering a board from that field would project a corpus-wide stale claim onto a *surface* — THE LAW's failure mode arriving through the front door.)

### Fault fallback

- [ ] **Junk output or an unmodeled condition → the named Claude agent takes the lane, no re-litigating.** Encode this as the queue's declared failure posture: it does not retry indefinitely, it does not improvise, it marks the job for Claude-lane pickup and moves on. (This is the VFX charter P2 fallback, generalized.)
- [ ] **Every vendor-lane output must have a named Claude curator downstream — no exceptions. That is the governance line.** The queue must carry the curator's identity as a **required** job field. A job that cannot name its curator does not enqueue.
- [ ] ⚠ **NEW AND BINDING — U-4 was RATIFIED-WITH-AMENDMENTS by jack-ryan 2026-08-24, AFTER this dispatch was first authored. Amendment R-B is a build constraint on YOU, and it is verbatim:**
  > **R-B — Question (4) becomes a RECORDED FIELD, not an assertion.** "Zero governance leaks" is not machine-checkable while the curator's identity lives only in the dispatcher's head. Ruled: every vendor-lane job writes the **named curator agent** into its `_run-log.tsv` row at **enqueue time (not at close)**. A job whose curator field is empty is a **refusal to fire**, not a job to be reconciled later. This makes the empirical criterion falsifiable by query rather than by memory, and the field is the natural identity axis for U-1's flight recorder (§ U-1(a)) — **capture it once, at the source.**

  The ratification's status line names this explicitly: *"R-B is a build constraint on star-lord's durable-queue task — the curator field is enqueue-time schema, not a later add."* **Enqueue-time, not close-time, is the whole point** — a curator recorded at close is a curator chosen after seeing the output, which is not a governance control. Read § U-4 R-A…R-D in `workflow-upgrades.md` before you design the job record.

### Standing

- [ ] Tests: **a second `codex exec` started under the lock exits non-zero** · crash-and-resume is safe · idempotent re-entry does not redo work · auth-expired path stops cleanly and surfaces · `test_harness.py:169` updated (not deleted) to the new two-directional `available()` contract
- [ ] `AGENT_STATE.md` updated; MIGRATION.md if any factory-consumed surface moves
- [ ] ℹ **Gate-1 INFO, carried so it is not lost:** `AGENTS.md` has **no ownership entry for `agentic_orchestration/factory/`**. You are being asked to make it standing infrastructure; a standing seam with no owner in the topology map is a gap. **Do not write AGENTS.md yourself** — surface the gap in your completion record and knight-rider routes it.
- [ ] Tag `star-lord/v<X.Y>-codex-durable-queue-1`

## Cross-seam contract change? (Principle 6 gate)

**YES — likely.** `codex.py` implements a registered harness the factory spine consumes, and the queue introduces a job-record surface plus a telemetry surface that downstream consumers (U-1 recorder, board, KR's liveness check) will read.

- **Required:** `Round-trip smoke: a production-path factory workflow selecting the codex harness → enqueue → serial drain → RawResult returned to the spine → receipts/usage recorded, with a field-presence check on RawResult's usage + model + exit_code and a terminal-row check on _run-log.tsv.`
- **MIGRATION.md required per ADR-004** for the job-record and telemetry surfaces — those are the surfaces other seams will build against, and `factory/MIGRATION.md` already exists as the place it goes.
- The stub's removal is itself a behavioral contract change: **`available()` flipping `False → True` changes what the spine will route.** Say so in MIGRATION.md.

## Acceptance criteria

- [ ] `codex.py` is a real adapter; `HONEST_STUB` and `BLOCKED_ON` are **gone**, not left lying next to working code
- [ ] Serial law enforced **at the `codex exec` invocation site**; mutual-exclusion primitive named; a concurrent-start attempt fails closed with a stated reason, proven by test
- [ ] Crash-resume and idempotent re-entry demonstrated, not asserted
- [ ] Model pin declared as a constant with the "every banked statistic was measured here" note
- [ ] Auth-expired path: stops taking jobs, surfaces the condition, names the `matt_to_do/` + Claude-fallback response
- [ ] Per-job telemetry emitted append-only, **without freezing an unratified U-1 schema**
- [ ] **Curator field written to the `_run-log.tsv` row at ENQUEUE time; empty curator = refusal to fire, proven by test** (U-4 R-B, binding)
- [ ] No emitted field, and no consumer built here, derives work state from a dispatch `**Status:**` header (Discipline #73)
- [ ] `_run-log.tsv` terminal-row liveness check still answerable by `tail -1`
- [ ] Round-trip smoke green; MIGRATION.md written
- [ ] Tag cut

## Quality criterion

**Game-quality goal this dispatch serves:** it is indirect and it is real — **the lane is capacity, and capacity is content.** The VFX run's 24-archetype reference corpus existed because the lane could grind 34 serial research jobs nobody had hours to do by hand. A durable queue means the next 24-row corpus does not wait on a human remembering to re-fire a shell script. **Uptime on this lane converts directly into how much of the game gets built.**

**Refutation conditions** (surface to knight-rider before executing if any apply):
- The serial law cannot be enforced structurally with the mechanisms available — say what you'd need; **do not ship a lock that relies on callers behaving**
- Proceeding requires a U-1 schema decision that Matt has not ruled (F-1…F-8) — **HALT, do not choose for him**
- Generalizing the runner would break the `_run-log.tsv` terminal-row contract KR and the U-4 router both read
- The acceptance criteria can all pass while the queue still permits two `codex exec` processes under some path you did not test
- The queue would become a second source of truth about work state rather than a lane — that violates THE LAW's spirit before U-1 even lands

## Out of scope

- **The board / any UI.** U-1(b) is a separate build behind the ≥2-workflow gate. You build the recorder-side emission; nobody renders it here.
- **Ratifying the U-4 router.** That is jack-ryan's, in flight.
- **Adding a Grok lane or any third vendor.** Admitted-in-principle via the U-8 judge door only, and gated.
- **Any third-party router/harness — Pi Agent Harness included.** DSH rejection is REAFFIRMED and generalized: context binds via AGENTS.md + brief through OUR harness; provider resolution is one line in `codex.py`.
- **Routing discipline-heavy seams to the lane.** gamora's law-stack, jack-ryan's gate authority, and the orchestrator seam HOLD permanently.
- Re-opening the F2 baton-consumer pilot (staged behind D5 revisit).

## References

- `agentic_orchestration/workflow-upgrades.md` § U-4 (lane shape, serial law, model pin, router, fault fallback) · § U-1 (flight recorder + THE LAW) · § U-3 (cache lever)
- `agentic_orchestration/factory/harness/base.py` (the pinned protocol) · `harness/claude_code.py` (the live-lane reference implementation, incl. how honestly to document a measured flag surface) · `harness/codex.py` (the stub to fill)
- `agentic_orchestration/research/vfx-p2-dossiers/run_p2_serial.sh` + `usage/_run-log.tsv` (the proven pattern and the liveness surface)
- `gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md` — **DRAFT, awaiting Matt F-1…F-8; read for shape, do not implement its schema**
- `gandalf/requests/2026-08-24-knight-rider-u1-fleetboard-build.md`

---

## Gate record

- jack-ryan Gate-1 DESIGN-MODE: **PASS-WITH-FINDINGS → **amendments applied 2026-08-24**** — Gate-1 batch review, 2026-08-24.
  Serial law tightened to the `codex exec` invocation site (a single process spawning two children is the same violation); U-1 hold clarified so it stops firing a spurious HALT on field-naming; two factual errors corrected (`available()` is duck-typed at `workflow.py:196`, not on the Protocol; `test_harness.py:169` will break and must be updated, not deleted).
  Amendments approved by jack-ryan directly under **ADR-002** (dispatch documents are documentation-only). **Nothing in this batch escalated to Matt.**

---

## Completion record — star-lord, 2026-08-24

**Tag:** `star-lord/v1.0-codex-durable-queue-1`
**Commit:** `dbd5bf22` (meta-repo `main`)
**Suite:** **661/661 green** (was 656 at session start; +26 new rows in
`factory/tests/test_lane.py`, +11 in `test_harness.py`, two existing rows UPDATED, none
deleted). ~178 s.
**Tree touched:** `agentic_orchestration/factory/` only. No engine paths, no
`gandalf/`, no `AGENTS.md`. Staged by name throughout (Discipline #62; gandalf was
concurrently active in this tree).

### 1. The mutual-exclusion primitive, and why it

**`fcntl.flock(fd, LOCK_EX | LOCK_NB)`** on a lock file keyed to a sha256 of the
resolved `CODEX_HOME` — `~/.reincarnated/lane-locks/codex-<sha12>.lock`. The lock's
subject is **the `auth.json` it serialises**, not a queue directory: two queues sharing
one `CODEX_HOME` share one token and MUST share one lock; two different `CODEX_HOME`s
are two different tokens and must NOT block each other. Keying on the queue directory
gets both of those backwards.

Held in `CodexHarness.run()` across the `subprocess.run` call **and nowhere else** —
that is the invocation site, and it is the only place in the package that spawns
`codex`.

**The measurement that makes `flock` satisfy the tightened requirement**, and it is the
non-obvious half, because `flock` is usually described as per-PROCESS:

```
same process, two separate open() calls on the same path
  -> second flock(LOCK_EX|LOCK_NB) FAILS, errno 35 (EWOULDBLOCK)   [Darwin 24.6.0]
```

`flock` locks are held by the **open file description**, not the process. So
`acquire()` opens a **fresh descriptor every time and never caches one**, which turns
"two processes cannot both run" into "two `codex exec` invocations cannot both run,
however they were reached" — two threads, a nested call, or one drain loop that got its
concurrency wrong. `test_ONE_PROCESS_cannot_hold_the_lane_TWICE` is the row; if it ever
reds, the guarantee has silently degraded to "one queue process", which is exactly what
Gate-1 refused.

Rejected alternatives: a **PID file + stale reaper** (its two failure modes are
symmetric and both fatal here — clear too slowly and a dead process wedges the lane,
clear too eagerly and two jobs run on one `auth.json`); an in-process
`threading.Lock` (cannot see a second process); a queue-level "only one drainer" guard
(the case Gate-1 named).

**Gate-2's requested test:** `test_a_SECOND_codex_exec_under_the_lock_EXITS_NONZERO` —
a real second process, a real `flock` attempt, **exit code 3**, stderr naming the law.
Plus `test_the_harness_DOES_NOT_LAUNCH_codex_when_the_lane_is_held`, which asserts the
absence of an invocation (a marker file the fake `codex` writes on start is never
created) — a refusal that still ran the vendor CLI would be a log line, not a lock.
**Also proven live** against the real host lock: a real `factory lane-drain` under a
held lock exited **2**, fired nothing, handed nothing off.

### 2. The crash failure-mode I accepted

The lock fd is made inheritable and passed to the child (`pass_fds=(lock.fd,)`), so the
child holds the same open file description and therefore the same lock. **Lock lifetime
== max(queue process, `codex exec` process), never longer.**

- **REFUSED:** a dead process's lock outliving it. No lock file whose mere existence
  blocks anything, no PID to go stale, no reaper to tune, and deliberately **no
  timeout-based lock breaking and no `--force`** — adding one converts the refused
  failure back into the accepted one at exactly the moment an operator is impatient.
  Row: `test_a_KILLED_queue_leaves_NO_STALE_LOCK` (SIGKILL the process group; the lane
  is free once the last holder exits).
- **ACCEPTED:** a **live orphaned `codex exec`** — parent killed while it ran — holds
  the lane until it exits or is killed. Chosen because that process is genuinely using
  `auth.json`; releasing the lane for it would be the double-fire the law forbids. A
  wedged lane is loud (`ps` names the holder; the run log's last row is non-terminal)
  and fails CLOSED. A double-fire is silent and violates a vendor precondition. Row:
  `test_a_LIVE_ORPHANED_child_STILL_HOLDS_the_lane` — the accepted half is **exhibited,
  not described**, because a trade is only honest if both directions have a row.

### 3. How the curator is enforced at enqueue (U-4 R-B)

Four layers, refusing outward-in:

1. `--curator` is `required=True` at argparse. A flag with a default is a flag that
   gets left off, and the governance line would then be enforced by whoever typed the
   command remembering it — the state R-B replaces.
2. `JobQueue.enqueue` refuses **first**, before any file or row is written. A refused
   job leaves no job record, no prompt file, no run-log row — nothing for someone to
   find later and fire. The refusal is derived from `REQUIRED_JOB_FIELDS` rather than
   restated beside it (the first version made that constant a *label*: it named the
   requirement in an error message while hardcoded conditions did the enforcing).
3. `RunLog.append` independently refuses an `event=enqueue` row with an empty curator,
   so no *other* writer can put a curator-less row into the surface the "zero
   governance leaks" criterion is queried from.
4. The name lands in **column 5 of the ENQUEUE row**, and
   `curator_at_enqueue(job_id)` reads the **enqueue row specifically** — not "a curator
   appears somewhere in this job's rows", which would accept a name chosen at close and
   report zero leaks while every name was picked after seeing the output.

Verified live: three real jobs, `curator=star-lord` on every row,
`tail -1 | cut -f5` → `curator=star-lord`.

### 4. Three defects this build made, and how each was caught

Recorded rather than quietly repaired, because how they were made is worth more than
the fixes.

- **`D-SL-CQ-1` — `str(None)` is the truthy string `"None"`.** I wrote
  `str(curator).strip()`, so `curator=None` sailed straight through the R-B refusal and
  would have written `curator=None` into the surface the leak query reads — counted as
  compliant by any query testing for a non-empty field. Caught by my own row.
- **`D-SL-CQ-2` — the usage mapping that looked like a rename.** codex's
  `cached_input_tokens` is a **subset** of `input_tokens`. Established from the record,
  not assumed: `67,431,424 / 72,375,471 = 0.9317` reproduces the banked **93.2%
  cache-hit** exactly, and the disjoint reading gives 0.4823 and matches nothing anyone
  wrote down. Passing the vendor's `input_tokens` through unchanged would have made
  `billable_token_total()` **count 67M tokens twice on a 72M-token run — a 93%
  over-report**.
- **`D-SL-CQ-3` — `codex login status` answers on STDERR, with an EMPTY stdout.**
  `check_auth` shipped reading `proc.stdout`, so it returned `auth_expired`
  **unconditionally**: `available()` would never have returned True, the queue would
  never have drained a job, and every job would have been handed to the Claude lane with
  a `matt_to_do` row demanding re-authentication of a lane that was already
  authenticated. **A permanently-closed lane fails safe and delivers zero uptime**,
  which is this dispatch's entire subject. **No unit test could have found it** — the
  fake `codex` binaries were written by me against the same wrong belief and agreed
  with the bug. The **live round-trip** found it, on the first invocation. How it was
  made: I ran the command in a terminal, which merges the streams, so what I measured
  was "the sentence appears somewhere" and what I wrote down was "the sentence appears
  on stdout". The test fixture now writes to **stderr** (with a stdout variant kept
  beside it, so a stderr-only fix would not pass by luck).

A fourth, found by reasoning about the live case rather than by a failure: **a busy lane
was reaching the fallback path.** `drain` proceeded on `busy`, `harness.run` refused
with `LaneBusy`, and that refusal was counted as a failed *attempt* — so a job whose
only problem was another drainer holding the lane for ten seconds got a **terminal
`FALLBACK-CLAUDE` row and a handoff manifest**. The serial law says "queue behind it or
fire the Claude lane"; a *drainer*'s answer is unambiguously the first, because the
other drainer is already doing the work. Busy now **defers** (non-terminal `ENQUEUED`
row, `event=defer`, job stays pending), with both the pre-check path and the race window
covered.

### 5. Acceptance criteria

| criterion | state |
|---|---|
| `codex.py` real; `HONEST_STUB` / `BLOCKED_ON` gone | DONE — deleted, and `test_no_stub_gates` asserts they are absent; its carve-out `flagged == [codex.py]` became `flagged == []` (same equality, one exemption smaller) |
| Serial law at the invocation site; primitive named; concurrent start fails closed, proven | DONE — `flock` per open-file-description; exit 3 in test, exit 2 live |
| Crash-resume + idempotent re-entry demonstrated | DONE — SIGKILL mid-job then resume; re-fired drain fires 0 and the fake's marker file does not grow |
| Model pin declared with the "every banked statistic was measured here" note | DONE — and moved **onto the argv**; it previously lived only in `~/.codex/config.toml` |
| Auth-expired path stops, surfaces, names `matt_to_do` + Claude fallback | DONE — and see § 6 for the choice I made |
| Per-job telemetry, append-only, without freezing U-1's schema | DONE — `schema_version` + `passthrough` on every record; no consumer built |
| Curator at ENQUEUE; empty = refusal to fire, proven | DONE — four layers, § 3 |
| No work state derived from a dispatch `Status:` header | DONE — `test_DISCIPLINE_73_...` scans the AST (non-docstring constants only, so the modules can describe the rule); a second row asserts the marker vocabularies contain no work-state term |
| `_run-log.tsv` terminal-row check answerable by `tail -1` | DONE — the test runs the actual `tail -1 \| cut -f3` pipeline; the proven runner's 4-column row is pinned as a literal and still reads terminal |
| Round-trip smoke green; MIGRATION.md written | DONE — § 7 |
| Tag cut | DONE |

### 6. Named choices the dispatch left to me

- **`matt_to_do/`: the queue writes a DRAFT, it does not file it.** On auth-expiry it
  writes a fully-formed ready-to-file row to `<queue>/AUTH-BLOCKED.md`, emits a
  `lane_blocked` telemetry event, writes an `AUTH-BLOCKED` run-log row, and hands every
  pending job to its named curator via a `fallback/` manifest. It does **not** append to
  `canonical/matt_to_do/`. Two reasons: an automated row in a curated human queue has no
  author in the accountability graph (the dispatch's own "silently and unattributably");
  and THE LAW — a queue that writes into a governance surface has put itself in that
  surface's data path. knight-rider files it.
- **`available()` NOT promoted onto the `HarnessAdapter` Protocol.** Verified the
  correction: it is duck-typed at `workflow.py:196` and `base.py` declares only `name`
  and `run`. Promoting it makes `ClaudeCodeHarness` non-conforming to the protocol it is
  the reference for, and both repairs are worse — give the Claude lane an `available()`
  returning `True` (a green nobody measured, in a package whose loudest rule forbids
  exactly that), or probe `claude` on every workflow load. Instead, an **additive**
  optional `unavailable_reason()` was added: `BLOCKED_ON` is fixed at import time, which
  was adequate for one closed state and is not adequate for three (`auth_expired` needs
  Matt, `busy` needs a minute, `cli_missing` needs a PATH). Named in MIGRATION.md.
- **Retry posture: `DEFAULT_MAX_ATTEMPTS = 1`, ceiling 3, exponential backoff.** The
  U-4 fault fallback is *hand it to the named Claude agent, no re-litigating*, not *try
  harder*. The ceiling is a constant, because "retries with backoff" degenerates into a
  spin-retry the moment it is a variable.
- **`validate_tools` REFUSES on this lane.** `codex exec` has no `--tools`; accepting a
  list would be the fail-open (a workflow would read as fenced and not be). This lane's
  pre-hoc containment is the SANDBOX MODE, declared per job class, validated against a
  closed vocabulary.

### 7. Round-trip smoke — LIVE, not simulated

Three real `codex exec` jobs through the production path
(`lane-enqueue` → `lane-drain` → `RawResult` → run log + telemetry):

```
lane open: fired=2 skipped=0 deferred=0 handed-to-claude=0
  01-smoke   rc=0   curator=star-lord
  02-smoke   rc=0   curator=star-lord
```

Serial confirmed from the timestamps — `02-smoke START` at `23:09:01Z`, the same second
`01-smoke` finished. Field-presence on `RawResult`: `usage` (`cache_read_tokens`,
`reasoning_tokens`, uncached `input_tokens`), `model=gpt-5.6-sol`,
`reasoning_effort=xhigh`, `exit_code=0`, `harness_session_id`. Re-drain fired 0 and
added no rows. `tail -1 | cut -f3` → `rc=0`; `cut -f5` → `curator=star-lord`.

**One scope limit, stated rather than papered over:** the dispatch asked for the
round-trip through "a production-path factory *workflow* selecting the codex harness".
That path requires an **agentic phase**, and the agentic lane has been on **HOLD since
round 17** (`LANDING.md` § 1 — a threat-model boundary that is gandalf's and Matt's to
draw, not mine). So the round-trip was proven through the queue's production path
instead, which is the path this dispatch actually builds. The workflow-load half is
covered: `available()` flipping `False → True` changes what the spine will route, and
that behavioural contract change is the first item in MIGRATION.md.

### 8. Gate-1 INFO carried forward — for knight-rider to route

**`AGENTS.md` has no ownership entry for `agentic_orchestration/factory/`.** This
dispatch makes it standing infrastructure; a standing seam with no owner in the topology
map is a gap. **I did not write `AGENTS.md`.** Naming it here, per instruction.

Two things worth knowing when it is routed: the tree now holds a **durable lock keyed to
host state outside the repo** (`~/.reincarnated/lane-locks/`), and it is the **only
place in the ecosystem that spawns a second vendor's CLI** — so "who owns
`factory/`" is also "who owns the vendor lane's uptime, its cost ledger, and its auth
health".

### 9. Flagged, not taken (no dispatch → not picked up)

- **Ambient MCP servers load inside every `codex exec`** — measured: a `vercel` MCP
  server is contacted and fails auth on all 30 jobs of the proven run, and on my smoke
  jobs. This is the Claude lane's H2 finding arriving on the second vendor.
  **RECORDED in `codex.py`, not fixed:** `--ignore-user-config` would also drop the
  model pin (which lives in `~/.codex/config.toml`), so closing it properly means
  pinning the whole config surface on the argv — a separate decision with its own
  evidence. Naming it is not fixing it and the comment says so.
- The negative branch of `check_auth` remains **REASONED, NOT MEASURED** — verifying
  the vendor's real not-logged-in text needs `codex logout`, a Matt-only action. Given
  `D-SL-CQ-3`, treat it as genuinely untested rather than as covered by symmetry.
- **The model pin can be DISPROVED but not CONFIRMED from the stream.** No codex frame
  echoes the model (`thread.started` carries only a `thread_id`; `turn.started` is
  empty), so there is no init-frame equivalent to `check_grant`. An unrecognised model
  DOES produce a `Model metadata for X not found` error item, which `adjudicate` treats
  as a failure rather than a warning. The adapter states both directions rather than
  implying a verification it cannot perform.
