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
