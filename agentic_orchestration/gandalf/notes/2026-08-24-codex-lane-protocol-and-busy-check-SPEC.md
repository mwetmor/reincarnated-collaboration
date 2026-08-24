# Codex-lane operating protocol + cross-session busy check — SPEC

> **STATUS:** SPEC — awaiting jack-ryan ratification (routing: gandalf authors → jack-ryan ratifies → star-lord builds the § 7 delta, composing with the in-flight durable-queue build, one data path → KR fires the 2012-Blizzard crawl).
> **Author:** gandalf (SPEC-AUTHOR; ELICITOR posture carried for the one Matt-fork the evidence cannot resolve — § 8 / queue Q62).
> **Commission:** `gandalf/requests/2026-08-24-knight-rider-codex-lane-protocol-and-busy-check.md` (Matt directive 2026-08-24 verbatim: *"update the protocol for the codex lane. We also need a check when a codex lane can be used to see (across all sessions) if any codex agent is currently in use."*)
> **This document specs; it does not build.** No production code was written in its authoring.

---

## 0 · Framing-audit (Discipline #42) + the hard fact, verified

**Q1 — load-bearing assumptions, enumerated and checked:**

1. *"The run-log structurally cannot answer busy-now."* **VERIFIED MYSELF (#19.1(b)), not inherited:** all 30 rows of `research/vfx-p2-dossiers/usage/_run-log.tsv` are written at close — the leading timestamp is the END time, `start=`/`end=` ride inside the row. A running job has NO ROW. The record answers "was busy," never "is busy." Also confirmed: **no curator column** (columns are end-ts · job-id · rc · detail-blob), so R-B requires a schema change regardless of liveness.
2. *"No session can answer busy-now."* **PARTIALLY REFUTED by the in-flight build** — and the spec must say so honestly rather than design in a vacuum. star-lord's uncommitted working tree (`factory/lane.py`, `factory/jobqueue.py`, `factory/harness/codex.py`, read in full 2026-08-24) already carries: a measured `flock(LOCK_EX|LOCK_NB)` mutual exclusion held at the `codex exec` invocation site with an inheritable fd (`pass_fds`), an advisory `lane_is_free()` probe, an `availability()` that answers auth-then-busy with surfaceable reasons, and a generalized run-log with `ENQUEUED`/`START` busy markers — i.e., queue-fired jobs WILL have a busy row. **What survives of the gap, and it is exactly the motivating incident:** a `codex exec` fired OUTSIDE the lock — star-lord hand-exercising the CLI in a live session, a legacy hand-fired script, Matt in his own terminal — takes no lock and writes no row. No leg of the in-flight build can see it. **VERIFIED:** no process-scan surface exists anywhere in `factory/` (grep for pgrep/psutil: zero hits).
3. *"The spec must not contradict the mid-flight build."* Honored structurally: § 2–§ 3 RATIFY the in-flight mechanism as protocol-of-record (so jack-ryan reviews one coherent thing), § 7 names only the DELTA.

**Q2/Q3:** no contradiction with seam authority; no framing refusal. The spec's center of gravity shifts from *"design a busy check"* to *"ratify the built mechanism + close the one leg it structurally cannot have."*

**The incident's true name (carried from KR, endorsed):** *uptime is not utilization.* The lane was healthy, authenticated, idle — and unusable, because nobody could prove it free. A lane held by vibes is the failure mode this document abolishes.

---

## 1 · What the busy check IS — one sentence

> **"Is a Codex agent in use right now?" is a DERIVATION over three independent state surfaces — the kernel lock, the process table, and the run-log — unioned fail-closed (any-busy-wins), readable by any session on this host without acquiring anything and without writing anything.**

Everything in § 3 unpacks that sentence. It is #73 applied to liveness: state is derived, never asserted — and it survives the queue not existing (§ G-5).

---

## 2 · The Codex-lane operating protocol (consolidated — this is deliverable A)

What § U-4 defines is a *router*. This section is the lane's *operating law*, consolidated out of the Matt directive, the star-lord dispatch, and the in-flight build's measured choices, so it stops living in one agent's head.

**P-1 — THE SERIAL LAW (verbatim, unchanged):** ONE `codex exec` at a time. One `auth.json`, one job stream. OpenAI CI/CD-auth precondition ("one machine or serialized job stream"), not a preference.

**P-2 — Enforcement point and primitive, NAMED:** the single `codex exec` call site in `CodexHarness.run()`. Primitive: `fcntl.flock(fd, LOCK_EX | LOCK_NB)` on a file keyed to the resolved `CODEX_HOME`, fd made inheritable and passed to the child (`pass_fds`) so lock lifetime = `max(queue, codex exec)` — a killed queue cannot leave a running child on an unlocked lane, and a dead process cannot leave a stale lock (the kernel releases on last-holder exit, including SIGKILL). Same-process double-acquisition FAILS (measured: errno 35 across two `open()`s — flock binds to the open file description, not the PID). **No timeout-based lock breaking, no `--force`, ever** — a break flag converts the refused failure mode into the forbidden one at exactly the moment an operator is impatient.

**P-3 — Granularity, and the reason WRITTEN DOWN (closes G-3):** the lock is **per-`auth.json`** (per resolved `CODEX_HOME`). The serial law's source is a per-CREDENTIAL vendor precondition; rate-limit and cost-visibility are likewise per-account. Output-collision is per-working-tree and is handled by the queue's job-record/output-path discipline, not by this lock. Consequences, both directions: two queue directories sharing one `CODEX_HOME` share one lane; a second authenticated subscription (second `CODEX_HOME`) is a second lane and is LEGALLY parallel — the law was never "one codex process per host," it is "one job stream per credential."

**P-4 — Auth health is a first-class lane state:** `codex login status` is the check of record (measured: rc=0, "Logged in using ChatGPT"). Expired auth is NOT a job failure and is never retried — re-auth is a **Matt-only action**. The queue stops taking Codex jobs, writes a ready-to-file row at `<root>/AUTH-BLOCKED.md` (it does NOT write into `canonical/matt_to_do/` itself — an automated append to a curated human queue is an authorless row in the accountability graph; **KR files it**), and hands every pending job to its named curator's Claude lane via a terminal `FALLBACK-CLAUDE` manifest. Idle work is the failure; a filed row plus a fallback is the success.

**P-5 — Model pin:** `gpt-5.6-sol` @ `model_reasoning_effort=xhigh`, declared as constants, said ON THE ARGV (never left to ambient `~/.codex/config.toml`). Every banked lane statistic was measured at this config. Drift is mechanically refused unless the config names its A/B evidence note (`model_ab_note`; template: ~6 duplicate jobs, candidate vs pin; criteria = curation WARN rate + URL-verification pass rate).

**P-6 — Sandbox is the fence:** this lane has no tool allowlist (`codex exec` exposes none); its pre-hoc containment is the sandbox mode, a CLOSED vocabulary (`read-only` / `workspace-write` / `danger-full-access`), declared per job class in the job record, never defaulted by typo. `read-only` is the posture of record for research jobs.

**P-7 — Fault posture:** one attempt by default (ceiling 3, bounded backoff, never a spin). Junk or an unmodeled condition → the job hands to its **named curator's Claude lane** via a `fallback/` manifest and a terminal `FALLBACK-CLAUDE` row — no re-litigating, and a post-re-auth drain never picks a handed-off job back up (ownership moves once).

**P-8 — Curator law (U-4 R-B, verbatim force):** every vendor-lane job writes its **named Claude curator** into the run-log row at ENQUEUE time. An empty curator is a **refusal to fire** — raised before any file or row exists. A curator recorded at close is an endorsement, not a control. There is no override toward the vendor lane over a missing curator (R-A: the override runs Claude-ward only).

**P-9 — What a HELD job is, and how it is released (closes the KR head-state gap):**

> **A HELD job is a job the router has cleared (all-YES, or Q3-NO-enqueue) whose drain is deliberately withheld, with the holding condition NAMED in a durable row.** Mechanically, once the queue exists: **ENQUEUED-but-not-yet-drained IS the held state** — the queue drains on invocation, not as a daemon, so holding is the absence of a drain call, and the enqueue row (with its curator and its `detail` naming the hold) is the durable record. **Release = a drain invocation, made when the named condition resolves** — and the releaser cites the condition in the drain's ledger note. Pre-queue holds (the 2012-Blizzard crawl today) live as dispatch/ledger rows carrying the same named condition. **A hold with an UNNAMED condition is the incident of record** — the crawl sat cold not because anything was decided but because nothing was checkable. Named-condition holds are governance; unnamed holds are drift.

**P-10 — Hand-fire retirement:** when the durable queue lands, `run_p2_serial.sh` RETIRES as an active instrument (kept in-tree as the proven-pattern lineage reference). From that point, a `codex exec` reached other than through the harness lock is a **protocol violation** — with exactly one standing exception: **Matt's personal terminal use**, which the check sees (§ 3 leg 2) but does not govern. Bridge window before the queue lands: any hand-fire REQUIRES the § 3 check first, and should take `SerialLaneLock` (already on disk) around the invocation.

**P-11 — #73 compliance:** no lane surface reads, derives from, or re-emits a dispatch `**Status:**` header. Work state is derived from completion records + git; LANE state is derived from the § 3 surfaces. The lane is a lane, never a second truth source about work.

---

## 3 · The cross-session busy check (deliverable B) — three legs, unioned fail-closed

**The contract:** any session, any agent, this host, answers *"is a Codex agent in use right now?"* in one command, read-only, without acquiring the lane and without writing anything.

| Leg | Surface | What it sees | What it CANNOT see |
|---|---|---|---|
| **1 — kernel lock probe** | `lane_is_free()` — acquire `LOCK_NB`, release immediately | every lock-taking invocation (all queue/harness fires), with zero staleness by construction (kernel drops on holder death) | a `codex exec` that never took the lock |
| **2 — process scan** *(the § 7 delta — does not exist yet)* | process table (`pgrep -f`-class scan for `codex exec`) | **out-of-band invocations**: hand-fired scripts, an agent exercising the CLI in a live session, Matt's terminal | anything on another machine |
| **3 — run-log last row** | `RunLog.is_idle()` — last row terminal? | queue backlog (`ENQUEUED`) and any in-flight queue job (`START` with no finish row); unrecognized markers read NON-terminal (fail-closed) | hand-fires that never wrote a row (which is why leg 3 alone — today's record — reports idle precisely when the lane is hottest) |

**The union rule: busy if ANY leg says busy.** There is no seniority ordering and no tie to break — see G-1's dissolution below. Each leg covers a blind spot of the others; a busy answer from any is a fact.

**Answer states (the check reports WHICH, never a bare bool):** `open` · `busy-lock` (holder visible via `ps`) · `busy-out-of-band` (a `codex exec` the lock never saw — name the PID) · `queue-pending` (lane free, ENQUEUED backlog exists — a *different* answer than busy: the next drain will take the lane) · `auth-expired` (closed on a Matt-only action) · `cli-missing`. Plus one advisory: `interactive-codex-present` (§ 8, Q62).

**Read-only, structurally (closes G-8):** the check derives from state surfaces and **emits nothing** — no telemetry event, no row, no lockfile touch that survives the probe. A probe that writes converts a question into a side effect and walks the checker into the data path, which is THE LAW's failure mode arriving through the *instrument*. Flow is one-directional: state surfaces → (busy check reads · queue telemetry records) → U-1 recorder derives history → board renders. **Liveness-NOW is never answered from telemetry or from the board** — those are record and view; the state surfaces are the truth the check derives from.

**Delivery shape:** a `factory` CLI subcommand (the CLI + `_cmd_status` scaffold already exist) with a pinned contract — distinct exit codes per state (star-lord picks the numbers, pins them in MIGRATION.md; `0` = open is the only pin this spec imposes), one-line human reason on stdout, `--json` for machine consumers. The exact invocation is documented at the queue root so "how do I check" is never folklore. A pure-shell degraded fallback (the pgrep pattern + `tail -1` of the run-log) is documented beside it for sessions without the Python environment.

---

## 4 · The eight forks, ruled

**G-1 — Truth source; who wins on disagreement? → THE DICHOTOMY DISSOLVES ON INSPECTION.** "A lockfile asserts; process state derives" presumes a lockfile whose *existence* is the claim. The built primitive is not that: the file's content is never read or trusted, and the lock IS kernel state bound to a live open file description — released on holder death including SIGKILL, unable to survive its process, unable to be stale. **flock is already derived state in #73's sense.** So there is no assert-vs-derive conflict to adjudicate: all three legs derive, from different surfaces with different blind spots, and disagreement is not contradiction — it is coverage. Union fail-closed (§ 3). The #73 defect cannot be built into this fix because nothing in it asserts.

**G-2 — Which failure do we choose? → FALSE-BUSY, chosen as a choice, three times over, consistently.** (a) The lock leg: star-lord's measured design already accepts a live orphaned `codex exec` wedging the lane — correctly, because that process is genuinely spending the credential; releasing around it is the double-fire. Wedge is loud (`ps` names the holder) and fails closed. (b) The process-scan leg: a false argv match delays a fire, loudly and diagnosably; a missed match silently violates a vendor auth precondition. (c) The run-log leg: an unrecognized marker reads non-terminal. **Every leg errs toward "do not fire."** The cost of false-busy is minutes of an operator's attention; the cost of false-idle is two job streams on one credential. Named, chosen, closed.

**G-3 — What is the singleton protecting? → PER-CREDENTIAL, reason now written down.** See P-3. The lock keying already built (resolved `CODEX_HOME`) is CONFIRMED as the correct granularity. One consequence the union rule must carry: leg 2 cannot cheaply attribute a raw out-of-band `codex exec` to a specific `CODEX_HOME`, so **an unattributable out-of-band process counts busy against ALL lanes on this host** — the false-busy direction, per G-2.

**G-4 — Ask vs take? → SEPARATE, and safe because the read is never the guarantee.** The advisory read gates *dispatch decisions*; the test-and-set (`LOCK_NB` at the single invocation site) gates *execution*. The TOCTOU race exists and is harmless: the loser receives `LaneBusy`, fails closed, and queues — no interleaving of the race can reach a vendor-precondition violation. For a human-paced fleet this is sufficient, and unifying query+acquire would force every "is it free?" question to momentarily TAKE the lane, making the question itself contend with the work. **Protocol law (elevating the in-flight docstring): no session may treat a "free" answer as a reservation.** The only reservation is the lock, held across the `codex exec` call, at the one call site.

**G-5 — What works when the queue is DOWN? → THE CHECK IS SUBSTRATE; the queue is a consumer.** Legs 1 and 2 require zero queue state (the lock primitive lives in `lane.py` below the queue; the process table is the OS's). Leg 3 degrades gracefully: absent log = no queue claim, not an error. A busy check that only worked once the queue was up would not have unblocked the crawl — this one answers on a bare host. The queue USES the same substrate (its `availability()` calls the same probe) — one mechanism, no fork of truth.

**G-6 — Does it see Matt? → YES for `codex exec` (leg 2 is FOR that); two residuals named.** (a) Interactive `codex` TUI sessions spend the same credential but are not automated job streams — the vendor precondition names job streams. Lean: **advisory-visible, non-blocking** (`interactive-codex-present`). This is the one genuine Matt-fork in the commission — it is about Matt's own working habit, and only Matt can rule whether his interactive presence should gate the fleet's lane. **→ Q62** (§ 8). (b) Codex on another machine is invisible and ACCEPTED: the fleet is single-host by charter (PC team retired 2026-06-30), and `auth.json` is host-resident. If a second host ever authenticates this credential, this section re-opens by name.

**G-7 — What does a NO on router Q3 mean? → ENQUEUE IS THE DEFAULT ROUTER; Claude-ward is the R-A exception.** With a durable queue, the two routers KR named collapse into one with a governed exception: a Q3 NO **enqueues** (curator named per R-B — the queue IS "queue and wait for the lane"), and routes to Claude **only** under the R-A directional override (schedule-critical, ledger note, Claude-ward only — never the reverse). **R-D compliance without a schema change:** a Q3-NO enqueue writes `router=Q3-NO` into the enqueue row's free-form detail column; a Q3-NO Claude-override writes the ledger note R-A already requires. Lane contention becomes countable for the first time: `grep -c "router=Q3-NO" _run-log.tsv`.

**G-8 — Recorder or read-model? → NEITHER; the check is a third thing: a read-only derivation that emits nothing.** Ruled in § 3. The recorder derives busy-HISTORY from the telemetry the queue already emits (enqueue/start/finish); the board renders the recorder; the check reads the state surfaces directly. Three roles, one direction of flow, zero second truth sources. Getting this backwards — a check that emits events others trust, or a board consulted for liveness — is refused by construction: the check writes nothing, and liveness-now is defined as unanswerable from telemetry.

---

## 5 · Router Q4 for the 2012-Blizzard crawl — curator RULED, release path named

**Curator = `galadriel`.** KR's candidate ("galadriel verifies frames, gandalf lands") is CONFIRMED, and it is exactly the R-B + sealed-spec § 6.6 composition, not a compromise between them: the crawl's outputs are codecs, resolutions, frame counts, decodability, mtimes — machine-verifiable in galadriel's instrument stack, which is what a curator DOES. **Landing is not a curator function:** per § 6.6, findings return to the conductor and land only on a fresh conductor ruling — the fence (no displacement, no promotion, no re-score; evidence-tier upgrades only) is untouched by this ruling. The R-B field reads `curator=galadriel`; the § 6.6 landing authority stays where the seal put it.

**Release path (P-9 applied):** the crawl is a HELD job whose holding condition is now fully named — *(1) busy check exists (the § 7 delta, or the § 3 documented shell bridge), (2) curator named (ruled above)*. On (1) resolving, KR enqueues with `curator=galadriel` and drains — **the crawl is the natural first production drain of the durable queue.** The brief carries verbatim: *"probe the media URL, not the containing page."* `3BnHvNZ_4YM` stays closed; a crawler that wanders into it is out of scope.

---

## 6 · § B rulings — the KR role-file defect, ownership, and the third instance

**6.1 — Fix the line; the fix is ratifiable now.** `.claude/agents/knight-rider.md:68` is wrong twice (verified against the discipline file: #11 = *Empirical inspection over assumption*; #10 = *Attribution clarity* = **experimental** attribution per jack-ryan `9c79d78f` — the concept KR reached for exists at neither number) and stale once ("the 12 disciplines" — a header asserting state, the #73 defect inside the reading list that teaches #73). Replacement text of record:

> `engineering-disciplines.md` — the disciplines (**derive the count from the file — #73**; especially #1 math-before-code, #2 smoke-test, **#11 empirical-inspection-over-assumption**, #12 semantic-shifting, **#62(a) name every path — a glob is not safer than `-A`**, **#19.1(b) inherited claims get the cheapest refuting test**). Note: **authorship-provenance has NO discipline home** — #10 is *experimental* attribution (change one thing, measure one thing), not authorship; stop reaching for #9/#10 when you mean who-wrote-this.

**6.2 — Third-instance question: YES, it counts — with its character stated precisely.** Instances 1–2 (the #19.1(b) escape hatch; the `81547a68` glob-attribution sweep) are *events* the absent rule failed to prevent. The role-file line is a different kind of evidence: not a violation but a **symptom** — a concept-name floating in the vocabulary with no rule anchoring it, mis-pinning itself onto neighboring numbers in the very document that shapes every KR session. A name with no referent generating citation drift is exactly what "no discipline home" predicts. Three instances reached → **jack-ryan's own stated bar is met; the source-provenance/authorship discipline candidate is his to draft** (his seam; this spec routes, it does not write his rule).

**6.3 — Who owns `.claude/agents/*.md`? → GOVERNANCE surfaces, two-tier rule (recommendation to Matt; operable as protocol immediately).** Role files are neither seam files nor canon — they are behavioral charters, and the recurring gap KR names is real for all eleven of them.

- **Tier 1 — charter substance** (scope, authority, persona, behavioral disciplines): **Matt-gated.** Any agent proposes; Matt rules. (Standing precedent: every role-tag in gandalf's own file is stamped "Matt-approved" with a date.)
- **Tier 2 — factual-reference hygiene** (wrong discipline numbers, stale counts, dead paths): **proposer ≠ sole-ratifier-on-self.** The subject agent writes the defect up (as KR correctly did — his decline-to-self-edit is CONFIRMED as the right instinct; it is the same conflict seam as gandalf's CANON-STEWARD → jack-ryan ratifier switch), a second party ratifies (jack-ryan wherever the reference is a discipline citation), and then the subject agent or KR executes the edit.
- **Stewardship attribution:** each agent is **steward-of-record for its own file's accuracy** — obliged to surface defects, never entitled to be its own ratifier.

Under this rule the 6.1 fix is a Tier-2 edit: jack-ryan ratifies the corrected citations (he authored `9c79d78f`, so ratification is a re-read), KR executes.

**6.4 — The companion gap:** `AGENTS.md` has no ownership row for `agentic_orchestration/factory/`. **Recommendation: star-lord owns `factory/`** — he built the spine, the harness contract, and now the lane + queue; the durable-queue dispatch already addresses him as the factory-harness seam. KR writes the topology row; Matt nods (topology is his surface). A standing seam with no owner is how the NEXT "whose is this?" incident happens.

---

## 7 · The build delta (star-lord, after jack-ryan ratifies) — additive to the in-flight build

The in-flight build is RATIFIED-AS-PROTOCOL by § 2–§ 4 (nothing in it moves). The delta is five items, all additive:

- **D-1 — the process-scan leg** (`lane.py`-adjacent): scan the process table for `codex exec` command lines (macOS: `pgrep -f`-class). Any hit while the flock probe reads free → `busy-out-of-band`, PID named. Unattributable hits count against all lanes on this host (G-3). Interactive `codex` (non-`exec`) processes → `interactive-codex-present`, advisory pending Q62.
- **D-2 — the `factory` CLI lane subcommand**: the § 3 contract — per-state exit codes (pinned in MIGRATION.md; `0` = open), one-line reason, `--json`. Invocation documented at the queue root; shell degraded fallback documented beside it.
- **D-3 — the Q3-NO router token**: `router=Q3-NO` in the enqueue row detail column (documentation + call-site convention; no schema change).
- **D-4 — `run_p2_serial.sh` retirement note** (P-10): header comment marking it lineage-not-instrument once the queue drains its first job; queue-root README says what replaced it.
- **D-5 — tests**: the check answers correctly in the named states (idle / lock-held / out-of-band exec, faked by a stub process / auth-expired via the injectable probe / queue-pending); **and the check writes nothing** — assert no file under the queue root changes and no telemetry event is emitted by a status call. That last test is THE LAW, made mechanical.

**Acceptance addition to the standing dispatch:** the 2012-Blizzard crawl enqueues with `curator=galadriel` and drains as the queue's first production workload; its run-log rows show `event=enqueue` carrying the curator BEFORE the `START` row exists.

---

## 8 · The Matt-fork (queued as Q62) — the only fork evidence cannot resolve

**Does Matt's own interactive vendor-CLI presence (`codex` TUI — and per § 9.3, `grok` TUI, one vendor-generic ruling) BLOCK that vendor's lane, or report advisory-only?** Lean: **advisory-only** — the vendor precondition names automated job streams; interactive use is ordinary plan usage; and a fleet lane that idles whenever Matt opens a chat window converts his presence into downtime. But the credential is genuinely shared, and only Matt can rule on the visibility of his own working habit. One-word shapes: **"advise as leaned"** / **"block"**. (Second-machine residual: accepted invisible, single-host fleet; re-opens by name if a second host ever authenticates.)

---

## 9 · The Grok lane, bundled (Matt-directed live probe, 2026-08-24 — same session)

**9.1 — Capability probe: DONE, and it is the U-4 first step, executed.** U-4 admits Grok in-principle via the U-8 judge door only, and names its first step: *"headless-CLI capability probe."* Matt directed the probe run directly this session (superseding the routed-as-Codex-job path for the probe itself). Measured facts, all first-hand:

| Fact | Measured value |
|---|---|
| Instrument | `~/.grok/bin/grok` v1.0.5 (`5115b46bc909`, stable) — installed, **not on PATH**; own home `~/.grok/` |
| Credential | `~/.grok/auth.json`, keyed `https://auth.x.ai::<uuid>` — logged in via **grok.com subscription** (verified: `grok models` prints "You are logged in with grok.com") |
| Models | `grok-4.6` (default; headless resolves to `grok-4.6-build`) · `grok-4.5` |
| Headless one-shot | `grok -p "<prompt>" --output-format json` → returned the demanded line verbatim (`PROBE-OK grok-lane 2026-08-24.`), `stopReason=end_turn`, **~4.3 s wall** |
| Telemetry envelope | JSON with `text` / `stopReason` / `sessionId` / `requestId` / `num_turns` / full `usage` (incl. `cache_read_input_tokens`, `reasoning_tokens`) / per-model `modelUsage` with **`costUSD`** (probe: $0.00286) — **native U-1 flight-recorder feed, richer than Codex's** (Codex surfaces usage; Grok surfaces usage AND dollar cost per call) |
| Streaming | `--output-format streaming-json` (NDJSON, ACP session updates) — the `codex exec --json` analog |
| Control surface | `--model` · `--reasoning-effort` · `--max-turns` · `--permission-mode` (default/acceptEdits/auto/dontAsk/bypassPermissions/plan) · `--allow`/`--deny` rules · `--disable-web-search` · `--json-schema` (structured output) |
| **Concurrency door (named)** | `grok agent leader` + `--leader` — a shared-leader mode that **multiplexes multiple clients onto one backend** via `~/.grok/leader.sock`. Also `agent stdio` / `agent headless` (WebSocket relay) multi-turn modes. |

**9.2 — Admission scope: the U-4 seal is RESPECTED, not widened.** Grok remains admitted **via the U-8 judge door only** — pilot = one From/To judge batch, three-way verdict comparison, galadriel primary. Bundling the lane LAW now is not opening a general research lane; it is ensuring that when the judge pilot fires, the lane is governed from birth instead of retrofitted after its first incident (the Codex lane's own history: rules consolidated out of "a Matt directive and KR's head" only after a cold-lane incident). Widening beyond the judge door is a re-ratification of U-4, not a spec edit.

**9.3 — Lane law generalizes: P-1…P-11 become PER-LANE law, parameterized by credential home.** The protocol was written against Codex but its logic is per-credential (P-3), and it transfers. The Grok instance values:

- **Serial law (P-1, with the reason honestly stated):** Codex's serial law cites a *verified vendor precondition*. **No equivalent xAI statement has been verified** — so the Grok lane is **serial-per-credential BY CHOICE, not by vendor law**: G-2's FALSE-BUSY ruling applied at the policy level. One `grok -p`/`grok agent` job stream per `~/.grok` credential until vendor-constraint evidence licenses otherwise; loosening requires the evidence named, in this spec, by amendment. (Cost-visibility and rate-limit remain per-account regardless — the P-3 granularity reasoning holds even where the CI/CD precondition doesn't.)
- **Enforcement (P-2):** same primitive — `SerialLaneLock` keyed to the resolved **Grok home** (`~/.grok` / `GROK_HOME`-equivalent), flock at the single invocation site in a `GrokHarness` sibling. **Leader mode is FORBIDDEN in lane invocations** (`--no-leader` said on the argv): a shared backend multiplexing clients is a concurrency door around the serial lock. A live `leader.sock` process found by leg 2 reads **busy-out-of-band** (FALSE-BUSY, per G-2).
- **Cross-vendor parallelism (P-3 consequence, stated):** the Codex lane busy does NOT close the Grok lane, and vice versa — different credentials, different vendors; the law was never "one vendor process per host." Parallel Codex+Grok is LEGAL. Unattributable out-of-band processes count against all lanes *of that CLI's vendor* on this host.
- **Auth health (P-4):** check of record = `grok models` (cheap, exercises real auth, measured rc=0). Expired auth: same discipline verbatim — Matt-only re-auth, `AUTH-BLOCKED.md` row for KR to file, pending jobs FALLBACK-CLAUDE to their named curators.
- **Model pin (P-5, honest about what is banked):** provisional pin `grok-4.6`, said on the argv. **Reasoning-effort is UNPINNED — no banked statistics exist at any config.** The U-8 judge pilot's first batch IS the banking measurement; it runs one declared config and that config becomes the pin, A/B discipline applying from then on. (Posture-2 logic — "a shallow second opinion launders confidence" — leans the pilot toward the highest available effort; the pilot declares it.)
- **Fence (P-6, translated to Grok's vocabulary):** no sandbox-mode triad here; the fence is `--permission-mode` + `--allow`/`--deny` + `--disable-web-search`. **Posture of record for judge jobs:** single-turn `-p`, artifacts inlined in the brief or cwd-scoped reads only, `--disable-web-search` unless the job class names web access, never `bypassPermissions`/`dontAsk` — declared per job class in the job record, never defaulted.
- **Fault posture (P-7), curator law (P-8), HELD definition (P-9), #73 compliance (P-11):** VERBATIM — no lane-specific variation. Judge-door admission means the curator field is galadriel-primary by construction, and R-C provenance applies doubly: a Grok verdict inside a galadriel judgment is named inline as Grok-sourced.
- **Hand-fire (P-10):** same rule from birth — this lane gets NO hand-fire era at all; its first fire is already post-protocol. Today's probe is the lineage exception, recorded here.
- **Busy check (§ 3, per-lane):** the three legs generalize — leg 1 probes the per-lane lock; leg 2's scan pattern covers `grok -p` / `grok agent` / `leader.sock` argv shapes; leg 3 reads the Grok lane's own run-log (same 6-column format, own file beside its outputs). The CLI subcommand grows a lane selector (`--lane codex|grok|all`; `all` is the default and answers fail-closed across lanes). Interactive `grok` TUI → the same advisory state, **which generalizes Q62 to vendor-generic**: "interactive vendor-CLI presence: advise or block" is ONE ruling covering both lanes (§ 8 updated framing; the queue row carries it).

**9.4 — Build delta additions (star-lord, same gate — additive to D-1…D-5):**

- **D-6 — `GrokHarness`** sibling in `factory/harness/` — pin constants (`grok-4.6`, `--no-leader`, argv-said), `availability()` via `grok models`, `SerialLaneLock` keyed to the Grok home, `pass_fds` lifetime discipline identical. **Gated behind U-8 judge-pilot authorization** — no build fires before the pilot is ruled live (a harness with no admitted workload is speculative code).
- **D-7 — busy-check lane selector**: leg-2 patterns for both vendors (incl. `leader.sock`), per-lane answer states, `--lane` flag, `all` default.
- **D-8 — per-lane run-log**: Grok lane's `_run-log.tsv` born WITH curator column and enqueue-time rows — it never has a rows-at-close era.
- **D-5 extension**: the writes-nothing test and state tests run per-lane.

---

## Sign-off

**gandalf**, 2026-08-24 — SPEC-AUTHOR (ELICITOR posture at § 8; § 9 added same day on Matt's directed Grok probe). Anchors: commission `gandalf/requests/2026-08-24-knight-rider-codex-lane-protocol-and-busy-check.md` · `workflow-upgrades.md` § U-4 (R-A…R-D; Grok-via-U-8-door clause) + § U-1 (THE LAW, #73 build constraint) · star-lord dispatch `dispatches/2026-08-24-star-lord-codex-durable-queue.md` + in-flight `factory/lane.py` / `factory/jobqueue.py` / `factory/harness/codex.py` (read in full) · `run_p2_serial.sh` + `_run-log.tsv` (verified directly) · **live Grok probe 2026-08-24 (`~/.grok/bin/grok` v1.0.5, measured first-hand: auth, models, headless JSON envelope, cost telemetry)** · engineering-disciplines #73, #19.1(b), #62(a), #9/#10/#11 · sealed VFX spec § 6.6 (fence untouched).
**Routing:** jack-ryan ratifies (§ 2–§ 6 + § 9, esp. the 6.1 Tier-2 fix, the 6.2 third-instance finding which reaches his stated bar, and § 9.3's serial-by-choice framing for a vendor with no verified precondition) → star-lord builds § 7 (D-1…D-5 now; D-6…D-8 behind the U-8 pilot gate) → KR enqueues the crawl per § 5.
