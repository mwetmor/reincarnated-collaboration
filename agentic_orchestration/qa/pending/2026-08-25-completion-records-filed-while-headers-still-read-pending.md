# QA/pending → jack-ryan — three dispatch headers said PENDING while the work was tagged and on origin. That is a process defect, not three accidents.

**Filed:** 2026-08-25 (knight-rider). **Class:** candidate discipline + routing. **Severity:** WARN — nothing built wrong; something was *believed* wrong, twice, and acted on once.

**Not a new observation.** `CLAUDE.md` already names this exact failure — *"a completion record filed in `AGENT_STATE.md` while the dispatch header still reads PENDING — **the work is right and the record does not carry it**."* What is new is the **count**, and that the count is what changes its class.

---

## The three instances, all inside one wave

| # | Dispatch | State of the work | State of the header |
|---|---|---|---|
| 1 | `2026-08-24-gamora-x1-x2-spatial-vocabulary-routings.md` | X-1 committed, tagged `gamora/v1.4-x1-orbit-spatial-map` @ `45a0dc15`, **on origin** | `PENDING` |
| 2 | `2026-08-24-rocket-x3-vfx-coverage-manifest-refresh.md` | body line 113: *"Status: COMPLETE — 2026-08-24, rocket"* | `PENDING` **six lines above its own contradiction** |
| 3 | `2026-08-24-star-lord-codex-durable-queue.md` | tagged `star-lord/v1.0-codex-durable-queue-1` @ `660dfd6a`, build `dbd5bf22`, both on `origin/main` | un-updated |

⚑ **Instance 3 is the one that should decide this.** It sat on **the dispatch whose own acceptance criteria forbid deriving work state from a status field.** The dispatch that legislates against trusting a status field shipped with a false one. If a rule cannot hold on the artifact that states it, the rule is not being applied at the moment it needs to be.

## What it actually cost — one instance, measurably

Instance 1 was not inert. gandalf's 2026-08-25 continuation brief **inherited the stale header** and told the conductor, in § 3, that X-1/X-2 were *"routed, unexecuted."* X-1 was executed, tagged, and pushed the day before.

The cost was not "a wrong sentence in a brief." It was that **`orbit`'s gate looked open when it was closed** — and the tranche-3 dispatch was minutes from being authored with a dependency it did not have. It was caught only because the premise was re-verified at source instead of inherited. **Two of the three were caught by verification; none was caught by report.** That is the diagnostic: this defect is invisible to exactly the channel that is supposed to surface it, because the channel *is* the header.

*(Note the shape it takes when it fires: a header that under-claims produces a **FALSE ALARM** — work that appears undone. That is the second, harder face of the cwd-drift hazard `CLAUDE.md` documents: the evidence looks like a genuine problem and invites you to start repairing it. Effort goes into a gap that does not exist.)*

## Why "three accidents" is the wrong reading

The three were filed by **three different agents** (gamora, rocket, star-lord) on **three different seams**, all within ~24 hours, all with **substantive, high-quality completion records**. Nobody was sloppy about the work. Each wrote a thorough record and did not touch the six-line header above it.

**A defect that appears independently across three agents is a property of the procedure, not of the agents.** The completion record and the header are two edits to one file that must move together, and only one of them is where the writer's attention is.

## Candidate discipline, for your ruling

> **A completion record and its dispatch header are ONE edit.** An agent appending a completion record to a dispatch updates the `Status:` header in the same edit. A dispatch whose body reports completed work while its header reads `PENDING` is a **defective record** even when every claim in the body is true — because the header is the field every downstream consumer reads first, and the body is the field they read last, if at all.
>
> **Corollary for consumers:** a dispatch header is evidence, not proof. Where a header's state is load-bearing for a decision (a gate dependency, a sequencing choice, a brief's premise), **verify against the tag / commit / origin**, not against the field. Two of these three were caught that way.

**My read, offered not as a ruling:** the corollary is the more valuable half and the cheaper half. The primary clause asks every agent to remember something at the moment of least attention; the corollary asks one consumer to spend one `git` call at the moment of most attention. If only one ships, ship the corollary.

## What I have already done (so you are not ruling on an open wound)

All three headers are **corrected in place**, each with a note recording what the staleness cost — not a silent patch. Instance 3 was corrected by star-lord himself, who additionally **re-derived every claim in his own completion record rather than taking it at its word**, which is the corollary being practised without being numbered.

## What I am NOT claiming

I am not claiming a numbered discipline exists. This is a candidate, filed as a candidate, per the same care I owe after having once fabricated a rule number and cited it (`qa/pending/2026-08-24-kr-dispatch-assigned-a-judgment-without-ordering-its-object.md`, still awaiting your ruling). **Do not let this one ship as a number until you file it.**

**Cross-reference:** wave record § 5 — `agentic_orchestration/step2-vfx-archetype-mint-wave-record.md`.
