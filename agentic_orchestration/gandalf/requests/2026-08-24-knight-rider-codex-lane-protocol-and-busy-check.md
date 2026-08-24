# Request — 2026-08-24 — knight-rider → gandalf — Codex-lane protocol update + cross-session busy check

**Status:** derive from completion record below, not from this line (#73)
**From:** knight-rider
**To:** gandalf (ELICITOR / SPEC-AUTHOR mode — you author the spec; you do not build)
**Authority:** Matt directive 2026-08-24, verbatim: *"please pass a prompt so that I can start a gandalf session to update the protocol for the codex lane. We also need a check when a codex lane can be used to see (across all sessions) if any codex agent is currently in use."*

This file contains TWO things:

- **§ A** — the paste-ready session prompt for the gandalf Codex-lane session
- **§ B** — a separate explanation Matt asked be surfaced to that same session: a defect in `.claude/agents/knight-rider.md` that KR declined to self-edit

---

## ⚑ MID-FLIGHT AMENDMENT — 2026-08-24, AFTER THIS FILE WAS HANDED TO GANDALF

**READ THIS BEFORE § A. Roughly half of deliverable (B) shipped while you were reading the commission for it.**

star-lord's durable-queue build landed (`dbd5bf22`, `660dfd6a`, tag `star-lord/v1.0-codex-durable-queue-1`) at `agentic_orchestration/factory/lane.py`. **I tested it live rather than reading it** — three states, one process:

```
lock path: /Users/admin/.reincarnated/lane-locks/codex-7b80b031a89d.lock
free (nothing running)?   True
free while HELD?          False
free after release?       True
```

**`lane.lane_is_free()` is the cross-session busy check.** The lock file lives **outside every repo**, keyed to a hash of the resolved `CODEX_HOME` — so its subject is *the `auth.json` being serialised*, not a queue directory, not a working tree. It answers across sessions, repos, and worktrees.

**What this settles, by construction rather than by spec:**

- **G-1 (truth source)** — `fcntl.flock(LOCK_EX|LOCK_NB)`. The kernel holds it and drops it when the holder dies, **including on SIGKILL where no userspace cleanup runs.** State is *derived* from the kernel, never *asserted* by a file's contents. #73 satisfied structurally, which is the strongest form.
- **G-2 (which failure we choose)** — chosen, documented, and **both directions have a row**: a dead process's lock is refused the right to outlive it (no PID, no reaper, deliberately no `--force`); a *live orphaned* `codex exec` **does** hold the lane until it exits, because that process is genuinely using `auth.json`. star-lord rejected PID-file+reaper on the reasoning that its two failure modes are symmetric and both fatal.
- **G-3 (granularity)** — per-`CODEX_HOME`, i.e. **per-account**. And the *reason* I said was written down nowhere is now written down: an **OpenAI CI/CD-auth precondition — "one machine or serialized job stream"** — not a preference. Granularity follows the reason exactly as G-3 predicted it should.
- **G-4 (query vs acquire)** — `lane_is_free()` is explicitly **ADVISORY**: it acquires and immediately releases, and its own docstring names the TOCTOU — *"a PROBE, not a reservation… between its answer and any use of that answer the lane can change hands."* The guarantee is the lock held across `subprocess.run`, at exactly one call site.
- **G-5 (works with the queue down)** — yes. It is a library call against a lock file in `~/.reincarnated/`; no queue process need be running.

**What is STILL YOURS, and is now the whole job:**

- **G-6 — Matt's hand-run `codex` is INVISIBLE to this.** A raw `codex` in a terminal never enters `CodexHarness.run()`, so it takes no lock and `lane_is_free()` will cheerfully report **True** while Matt is mid-session. This is now the **single largest remaining hole**, and it cannot be closed inside agent tooling — it needs either a wrapper Matt actually uses, or an out-of-band liveness derivation (process scan), or an explicit accepted-risk ruling. **Rule on it.**
- **G-7 — what a machine-answerable Q3 `NO` means for the router.** Untouched by the build, and now *more* pressing: the check is cheap and reliable, so Q3 stops being a memory question and becomes a branch. Route-to-Claude versus queue-and-wait are two different routers, and **R-D** makes each recorded NO durable and countable.
- **G-8 — recorder versus read-model.** `Telemetry` now emits append-only JSONL from birth, so the events exist. Whether lane state is *emitted* by the check or *derived* by the recorder is undecided — and getting it backwards makes the busy check the second truth source **THE LAW** exists to prevent, in its most dangerous form: the one that gates firing, and therefore feels authoritative.
- **All of deliverable (A)** — the operating protocol. Entirely untouched by this build. Serial-law enforcement point, auth-health precondition, model pin, fault fallback, HELD-job release. Still living in a Matt directive and in my head.

**One more thing the build produced that belongs in your protocol.** star-lord's own defect record: **`codex login status` answers on stderr with empty stdout.** His `check_auth` read stdout and therefore reported the healthy lane **expired unconditionally** — the queue would never have drained a single job. He notes **no unit test could have found it, because his fakes shared the bug's premise**; the live run caught it on first invocation. The auth-health precondition in deliverable (A) must specify *which stream it reads*, and the protocol should say plainly that a fake sharing the bug's premise is not a test.

**Read `factory/lane.py` and `factory/MIGRATION.md` before specing.** Do not spec around what shipped, and do not take the paragraph above on my word — my numbers have had a bad run and **#19.1(b)** applies to me hardest.

---

## § A — SESSION PROMPT (paste this)

> You are gandalf, in **ELICITOR / SPEC-AUTHOR** mode. Run your session-start protocol first, then take this commission. **You author a spec; you do not build.** jack-ryan ratifies after you; star-lord builds after him.
>
> ### What you are producing
>
> **Two deliverables, one document** (`gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md` or a name you prefer):
>
> **(A) The Codex-lane operating protocol, updated.** § U-4 in `agentic_orchestration/workflow-upgrades.md` currently defines a *router* — the four-question gate (1) Context-portable? (2) Curatable? (3) Lane open? (4) Verifier slotted? — ratified-with-amendments by jack-ryan as **R-A…R-D**. What it does **not** define is the lane's *operating* protocol: the serial law's enforcement point, the auth-health precondition, the model pin, the fault fallback, what a HELD job is and how it is released. Those currently live in a Matt directive and in my head. Put them in the document.
>
> **(B) The cross-session busy check.** Any session, on any agent, must be able to answer *"is a Codex agent in use right now?"* before it fires one. Today no session can. Spec the mechanism — not the code.
>
> ### The incident that motivates this — it is live right now, not hypothetical
>
> The **2012-Blizzard crawl** is CLEARED by you and fenced at sealed-spec § 6.6. It is the one genuinely Codex-shaped job I have. I have **not fired it**, and the reason is not policy — it is that **star-lord is building the durable queue in a live session and may exercise `codex exec` during his own build**, and I have no way to find out. So the instrument sits cold while the work that needs it waits. Matt asked why the lane was left open; this is the answer, and it is the thing you are being asked to close.
>
> Note the shape carefully: **uptime is not utilization.** The lane was healthy, authenticated, and idle. Nothing was broken. The lane went unused because *nobody could safely prove it was free.*
>
> ### The hard fact that should anchor the spec
>
> The lane's only existing record is `agentic_orchestration/research/vfx-p2-dossiers/usage/_run-log.tsv`. I inspected it. **Every row is written at close** — the leading timestamp is the end time, with `start=`/`end=` inside the row. Therefore:
>
> **A job that is currently running has NO ROW AT ALL.**
>
> The lane's record structurally cannot answer "busy now." It answers "was busy." This is not an operator-discipline gap you can close with a rule — it is a gap in the artifact, and any busy check that reads this file as-is will report *idle* precisely when the lane is *hottest*. Please verify this yourself against the file rather than inheriting it from me (**#19.1(b)** — and my numbers have a bad week: two of three counts I handed gamora in a dispatch this run were wrong, one of them a future-tense sentence I read as a census).
>
> Also note: the file has **no curator column**, which **R-B** now requires at enqueue time. The record needs a schema change regardless of what you decide about liveness.
>
> ### Eight forks to grill — these are my guesses at the shape, not the shape
>
> - **G-1 — What is the truth source, and what happens when sources disagree?** A lockfile *asserts* busy. Process state *derives* it. **#73** was ratified today and says state is derived, never asserted. But deriving means scanning for live `codex exec` processes, which is host-local — and a lockfile survives across things a process scan cannot see. If they disagree, which wins? A wrong answer here builds the #73 defect into the fix for it.
> - **G-2 — Which failure do we choose?** Every lock has two failure modes and you cannot have neither. **False-busy** (holder crashed, lock never released, lane idles forever — today's outcome by other means) versus **false-idle** (check says free, two `codex exec` processes run, serial law broken). PID-liveness, TTL, and heartbeat each trade these differently. Name the choice as a choice; do not let the mechanism make it silently.
> - **G-3 — What is the singleton actually protecting?** Is the lane one global lock, or per-model, per-host, or per-account? The serial law was imposed for a reason — cost, rate-limit, or output-collision. **The reason determines the granularity**, and I do not think the reason is written down anywhere. If it is rate-limit, the lock is per-account and a second host does not help. If it is cost-visibility, it is per-account too. If it is output-collision, it is per-working-tree and two lanes are fine.
> - **G-4 — Who may ask versus who may take?** I need a read-only *"is it free?"* that does not acquire. A read that races an acquire is a classic TOCTOU. Does the spec need query and acquire to be the same operation (test-and-set), or is an advisory read good enough given a human-paced fleet?
> - **G-5 — What must work when the queue is DOWN?** star-lord's durable queue is being built right now. The obvious move is to make the queue own the lock. But **today's blocking situation is exactly "the queue does not exist yet"** — and a busy check that only works once the queue is up would not have unblocked the crawl. Decide whether the check is a queue feature or a substrate the queue also uses.
> - **G-6 — Does it see Matt?** Matt may run `codex` by hand in his own terminal, outside every agent session. Is that invisible to the check, and is that acceptable? If it must be visible, the mechanism can no longer live inside agent tooling.
> - **G-7 — What does a NO on Q3 mean?** Router question (3) is "Lane open?" and is answered from memory today. Once it is machine-answerable, a NO means either *route to Claude instead* or *queue and wait for the lane*. **Those are two different routers.** **R-D** requires a recorded NO to name its failing question — so a Q3 NO becomes a durable, countable record, which also makes "how often is the lane contended" measurable for the first time.
> - **G-8 — Recorder or read-model?** U-1's board will want to display lane state. **THE LAW** is that the board is a VIEW and never a second truth source. So: does the busy check *emit* an event that the recorder consumes, or does the recorder *derive* busy from the events it already has? Get this backwards and the busy check becomes the second truth source THE LAW exists to prevent — and it will be the authoritative-feeling one, because it is the one that gates firing.
>
> ### Sealed — do not reopen
>
> - **R-A…R-D** are jack-ryan's ratified amendments to U-4. Build on them; a change to them is a re-ratification, not a spec edit.
> - **The tier-2 VFX law is sealed.** Reopening is a **HALT to Matt**.
> - **You never build.** And the whirlwind clean-room quarantine holds — no quarantined artifact may reach a building agent through your document's reference list. I violated this myself at Gate-1 this run, through my own References section, which is how I know it is easy.
> - **Serial law itself is not up for debate** — its *enforcement point and granularity* are. jack-ryan already tightened the enforcement point to the `codex exec` invocation site (a single queue process spawning two children is the same violation as two queue processes).
>
> ### Required reading
>
> - `agentic_orchestration/workflow-upgrades.md` § U-4 (incl. R-A…R-D), § U-1 (THE LAW; the #73 build constraint at line 21), § U-3
> - `agentic_orchestration/dispatches/2026-08-24-star-lord-codex-durable-queue.md` — what is being built right now; your spec must not contradict it mid-flight
> - `agentic_orchestration/research/vfx-p2-dossiers/usage/_run-log.tsv` and `run_p2_serial.sh` — the lane as it actually exists
> - `engineering-disciplines.md` **#73**, **#19.1(b)**, **#62(a)** (all three ratified today), **#9**/**#10** (see § B below — the names lie)
>
> ### Routing after you
>
> jack-ryan ratifies → star-lord builds (composing with the durable queue, one data path) → I fire the 2012-Blizzard crawl the moment the check exists. The crawl brief carries verbatim: *"probe the media URL, not the page."* `3BnHvNZ_4YM` stays closed. Router **Q4** still needs its curator named — my candidate is galadriel verifies frames, you land. Rule on that too if you're willing; it is currently the only thing besides the busy check standing between the crawl and firing.
>
> ### Also please rule on § B below — Matt asked that it be surfaced here.

---

## § B — The role-file defect KR declined to self-edit

**Surfaced by Matt to this session.** KR started to edit this himself, stopped, and was told to write it up instead.

**File:** `.claude/agents/knight-rider.md`, line 68 — the startup-reading list in KR's own role definition.

**Current text:**

> `engineering-disciplines.md` — **the 12 disciplines** (especially #1 math-before-code, #2 smoke-test, **#11 attribution**, #12 semantic-shifting)

**Two defects, both surfaced by jack-ryan's ruling of 2026-08-24 (`9c79d78f`):**

1. **"#11 attribution" is wrong twice over.** Verified against the file: **#11** is *Empirical inspection over assumption* (line 182). **#10** is the one titled *Attribution clarity* (line 173) — and jack-ryan's ruling is that #10 means **experimental** attribution (*change one thing, measure one thing*), **not** authorship. So the role file points at the wrong number, for a concept that does not exist at either number. jack-ryan corrected this identical mis-citation *inside* `engineering-disciplines.md` in the same commit; KR's role file is a third copy of it, and it is the copy that shapes every KR session.

2. **"the 12 disciplines" is stale — there are 73+.** This is a header asserting state instead of deriving it, which is precisely **#73**, ratified hours ago. The role file is an instance of the defect its own reading list is supposed to teach.

**Why this is worth a ruling and not a quiet fix:** jack-ryan's ruling registered **source-provenance / authorship attribution as a candidate with no discipline home**, at two instances — the #19.1(b) escape hatch, and KR's 2026-08-24 glob-attribution defect (`git add agentic_orchestration/dispatches/2026-08-24-*.md` swept gamora's completion-record append into commit `81547a68` under KR's message). **This role-file line is arguably a third instance of the same absence**: KR reached for a number that felt like it meant authorship, and the reason it felt that way is that the concept has a name in the discipline stack but no rule behind it. If gandalf agrees it is a third instance, the candidate reaches jack-ryan's own stated bar of three.

**What KR proposed writing** (not written — held for this ruling): corrected numbers; an explicit note that authorship-provenance has no discipline home so KR stops reaching for #9/#10 when he means it; an instruction to derive the discipline count from the file rather than trust the line; and added pointers to **#62** (name every path; a glob is not safer than `-A`) and **#19.1(b)** — the two rules KR broke this session.

**Open question for gandalf:** who owns `.claude/agents/*.md`? It is not a seam file and it is not canonical. KR judged a unilateral edit to his own behavioral definition worth showing Matt first, which was right, but the ownership gap is real and will recur for every agent's role file. A companion gap is already logged: **`AGENTS.md` has no ownership entry for `agentic_orchestration/factory/`** (Gate-1 INFO, unrouted).

---

## References

- `agentic_orchestration/workflow-upgrades.md` § U-4, § U-1
- `engineering-disciplines.md` #73, #19.1(b), #62(a), #9, #10, #11 — commits `ef7cfc82`, `9c79d78f`
- `agentic_orchestration/gandalf/requests/2026-08-24-jack-ryan-u4-router-ratification.md`
- `agentic_orchestration/dispatches/2026-08-24-star-lord-codex-durable-queue.md`
