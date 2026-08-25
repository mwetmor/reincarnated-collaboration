# Vendor lane queue roots

**Owner:** star-lord (factory-harness seam)
**Authority:** lane spec `gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md`, ratified by jack-ryan 2026-08-24 (Amendments A–I binding) · `workflow-upgrades.md` § U-4

Two vendor lanes live here, one directory each. A lane is an **instrument operated by
a named agent**, never a seat: every job names the Claude curator who owns its output
downstream, at enqueue time, or it does not fire.

| Lane | Queue root | Credential | Serial rule |
|---|---|---|---|
| `codex` | `lanes/codex/` | `~/.codex/auth.json` | **LAW** — a verified OpenAI CI/CD-auth precondition (one machine or a serialized job stream) |
| `grok` | `lanes/grok/` | `~/.grok/auth.json` | **POLICY** — no equivalent xAI precondition has been verified; serialised by our choice |

The distinction in the last column is load-bearing. Do not defend the Grok policy as
if it were the Codex law: loosening it requires named evidence and an amendment, and
that is only possible while everyone can still find what it rests on.

The two lanes are **independent**. A busy Codex lane does not close the Grok lane;
running both at once is legal and intended. (The Codex lane's historical run-log also
lives at `research/vfx-p2-dossiers/usage/_run-log.tsv` — the proven runner's 30
four-column rows — and the busy check reads it too.)

---

## Before you fire anything: check the lane

```
cd agentic_orchestration && python3 -m factory lane
```

```
codex  open               lane free on all three legs; auth healthy
grok   queue-pending      lane FREE; 1 job(s) enqueued and not yet drained …
SELECT   : codex   [§ 10.3 deterministic order: codex -> grok]
```

Useful forms:

| Command | Answers |
|---|---|
| `factory lane` | both lanes + which one the selection law picks |
| `factory lane --lane grok` | one lane, exit code = that lane's state |
| `factory lane --safe-to-fire` | one bit: `0` = fire, `1` = do not |
| `factory lane --json` | the same answer for a machine, with every leg's raw reading |
| `factory lane --shell-fallback` | prints the degraded recipe below |

**The check acquires nothing and writes nothing.** No row, no telemetry event, no
surviving file touch. It is safe to run from any session at any time, including while
a drain is in flight, and a "free" answer is **never a reservation** — the only
reservation is the lock, held across the vendor invocation at the single call site.

### The answer states, and what each one means for you

| State | Exit | What to do |
|---|---|---|
| `open` | 0 | fire |
| `queue-pending` | 10 | **fire** — a backlog is not occupancy; a drain will take the lane |
| `busy-lock` | 20 | enqueue behind it |
| `busy-out-of-band` | 21 | enqueue; something the lock never saw is running (the PID is named) |
| `busy-unknown` | 22 | enqueue; a leg was unreachable and ambiguity never reads open |
| `auth-expired` | 30 | lane CLOSED — Matt-only re-auth; work falls back to the named curator |
| `cli-missing` | 31 | lane CLOSED |

Plus one advisory, `interactive-<vendor>-present`, which is **never blocking** (Q62,
Matt-ruled: *"I'm not worried about TUI. I'll simply check the fleet-board before ever
engaging with the codex or grok TUI."*). A drain that fires while the advisory is
active writes the advisory token into its ledger note.

**Bind to the predicate, not to a leg.** *"Is it safe to fire?"* is
`factory.lane_status.SAFE_TO_FIRE_STATES` = `{open, queue-pending}` — pinned in
`factory/MIGRATION.md` and by literal in `factory/tests/test_vocabularies.py`. Do not
re-derive it from *"last run-log row terminal"*: that reading is leg 3 alone, it is
pre-Amendment-A, and it reports **busy on backlog**, which wedges a lane holding a
deliberately parked job.

---

## Firing a job

```
python3 -m factory lane-enqueue lanes/codex <job-id> <prompt-file> \
    --curator galadriel --job-class research --sandbox read-only
python3 -m factory lane-drain lanes/codex
```

For the Grok lane, name the lane and its own fence (it has no sandbox triad):

```
python3 -m factory lane-enqueue lanes/grok <job-id> <prompt-file> \
    --lane grok --curator galadriel --sandbox n/a
python3 -m factory lane-drain lanes/grok --lane grok
```

`--curator` is **required and has no override** (U-4 R-B). An unnamed curator is a
refusal to fire, raised before any file or row exists. A curator recorded at close is
an endorsement, not a control.

`--router Q3-NO` records that the four-question router cleared the job but answered NO
to question (3) — the lane was occupied, so the job queued. That makes lane contention
countable for the first time:

```
grep -c "router=Q3-NO" lanes/*/_run-log.tsv
```

`lane-drain` is idempotent and crash-safe. The correct response to *"did that finish?"*
is to run it again.

---

## The degraded fallback (no python available)

Strictly weaker than `factory lane` — it **cannot see leg 1, the kernel lock** — and it
says so. Use it only where the Python environment is unreachable.

```sh
# leg 2 — occupancy (the only leg that sees an out-of-band invocation)
ps -axo pid=,args= | grep -E '^(?:\S*/)?codex\b.*\bexec\b'
ps -axo pid=,args= | grep -E '^(?:\S*/)?grok\b.*(?:\s-p\b|\bagent\b)|leader\.sock'

# leg 3 — the last marker, per run-log
tail -1 lanes/codex/_run-log.tsv | cut -f3
tail -1 lanes/grok/_run-log.tsv  | cut -f3
tail -1 ../research/vfx-p2-dossiers/usage/_run-log.tsv | cut -f3

# auth
codex login status          # answer is on STDERR
~/.grok/bin/grok models     # NOT on PATH; resolve explicitly
```

Reading leg 3: `rc=<N>` · `SKIP-EXISTS` · `FALLBACK-CLAUDE` · `AUTH-BLOCKED` ·
`ENQUEUE-REFUSED` are terminal (nothing executing). `START` means executing.
**`ENQUEUED` means queue-pending, which is safe to fire — not busy.** Anything else is
a marker nobody enumerated and reads non-terminal, fail-closed.

`factory lane --shell-fallback` prints this recipe from the same source the real check
uses, so the two cannot drift into different instructions.

---

## The run-log format (6 columns, additive)

```
1 ts_utc    2 job_id    3 marker    4 detail    5 curator=    6 event=
```

Columns 1–4 are the proven runner's, byte-for-byte in the same positions, so every
`tail -1 | cut -f3` habit keeps working. Columns 5–6 are U-4 R-B's curator and the
lifecycle event. Rows written by `run_p2_serial.sh` have four columns and are read
without complaint — a missing curator there means *unknown*, not *empty*.

The **Grok** log is born with all six columns and with enqueue-time rows: that lane has
no rows-at-close era, because P-10 applies to it from birth and it has no hand-fire era
at all.

---

## `AUTH-BLOCKED.md`

If a drain finds the credential unhealthy it writes a ready-to-file row to
`<queue root>/AUTH-BLOCKED.md` and hands every pending job to its named curator's
Claude lane. **The queue does not file it — knight-rider does.** An automated append to
a curated human queue produces a row with no author in the accountability graph, and
re-authentication is a Matt-only action either way. Idle work is the failure; a filed
row plus a fallback is the success.

---

## The OTHER axis: `lanes/agents/_custody.tsv` — who is mid-flight in a SEAM?

The lock above serialises **vendor invocations**. It does not serialise **agents**. On
the day the busy check shipped, two dispatchers sent a star-lord sub-agent at the same
build twenty-eight minutes apart, and neither could see the other; the lane lock did its
job perfectly and was never the problem.

Seam custody is that question one level up (lane spec § 11, ratified with Amendments K
and L). The ledger lives at `lanes/agents/_custody.tsv` — 6 columns, append-only:
`ts · seam · holder · event · intent · detail`.

### Before you dispatch a sub-agent into a named seam

```
cd agentic_orchestration && python3 -m factory custody check --seam star-lord
```

```
star-lord    held            holder=gandalf-session-85515  — PID 85515 is alive. …
```

| State | Exit | What you do |
|---|---|---|
| `free` | **0** | claim it, then spawn |
| `held` | **20** | **DO NOT SPAWN.** Coordinate with the holder, wait, or escalate |
| `stale` | **21** | holder is dead. **Not free** — clear it with `override --note …` |
| `custody-unknown` | **22** | a leg could not be read. Treated as occupied, fail-closed |

**`[ $? -lt 20 ]` is the whole predicate** — bind to the band, not to the vocabulary.
`--safe-to-spawn` collapses it to one bit; `--json` gives a machine the same answer with
both legs' raw readings. `check` writes nothing and **does not create the ledger** if it
is absent, so it is safe from any session at any time.

### The three write verbs

```
python3 -m factory custody claim    --seam star-lord --holder <your-session-id> \
                                    --intent "what the sub-agent will do" \
                                    --release-on "the condition that ends this claim"
python3 -m factory custody release  --seam star-lord --holder <session> --evidence <commit-or-record>
python3 -m factory custody override --seam star-lord --holder <session> --note "why the stale claim is cleared"
```

* **`--release-on` is REQUIRED.** Every CLAIM names the condition whose satisfaction
  produces the RELEASE (Amendment L). A claim whose end cannot be stated is a claim that
  should not be written — an unbounded live claim is indistinguishable from owning the
  seam, and custody is dispatch exclusivity, never seam ownership.
* **One row per seam.** A run-scoped conductor charter claims its seams one row at a
  time; wildcards and comma-lists are refused, so a partial release stays expressible.
* **`claim` is atomic.** Check-and-append happens under an `flock` on the ledger itself,
  so two dispatchers racing cannot both win — and the loser is told **who** holds it.
* **`release` cites its evidence** — the completion record or commit the claim rested on.
  The `holder` column names the **session that must be alive**, not the agent, so the
  dispatcher normally writes the RELEASE; a release by a different session is recorded
  (`claimed_by=`), not refused.
* **There is no TTL and there never will be.** A stale claim clears only by an explicit
  `override` with a note. A TTL is a timeout-based lock break wearing a different word,
  and the case it gets wrong is a holder who is alive and mid-flight.

### The routing rule (fleet law, § 11.3)

> **Before dispatching a sub-agent into a named seam, check seam custody. Occupied seam
> → DO NOT SPAWN.** Claim before spawn; release on completion; override only over a dead
> holder, with a note. Standing down is the honourable path and it gets a ledger row,
> not a shrug.

Full contract, exit codes and the design reasoning: `factory/MIGRATION.md` § custody v0.
