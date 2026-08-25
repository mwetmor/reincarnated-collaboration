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

---

## ⚑ ADDENDUM, same day — a SECOND surface, five more instances, and it widens the candidate

Filed hours after the above, from gamora's comment-truth commit (`83f351ce`, `reincarnated-engine`), which I verified as comment-only at source (32 insertions, **zero** non-comment additions; 10 geometry multipliers byte-identical; X-1 smoke 18 GREEN / 0 RED).

**Her flag:** *"five in-tree refs to `damage_resolver.py:1491` (fear/taunt eviction) already point ~520 lines off — real site is 2014. Pre-existing, same defect class, outside this scope."*

**She is right that it is the same defect class, and that matters more than the five refs do.** The body of this filing framed the defect as *"headers go stale."* That framing is too narrow. The general shape is:

> **A POINTER THAT NO LONGER POINTS.** A `Status:` header, a `file:line` citation, a named hook, a doc census — each is a cheap reference to an expensive fact, and each **degrades silently** because nothing re-checks a pointer that is not being followed at the moment the referent moves.

The two surfaces now on the table:

| Surface | Instances | Failure mode when followed |
|---|---|---|
| Dispatch `Status:` headers | 3 (gamora, rocket, star-lord) | **under-claims** → a FALSE ALARM; work that appears undone. Effort goes into a gap that does not exist. |
| In-tree `file:line` citations | 5 (all → `damage_resolver.py:1491`, real site `:2014`) | **mis-points** → the reader lands 520 lines away, in unrelated code, and must decide whether the citation or their own reading is wrong. |

⚑ **And a third, already on the record from the same 24 hours:** `generation/MIGRATION.md:229`'s *"6 Wave-C kits"* is **future-tense prose that reads as a present-tense census** — gamora had to untangle a 6/18/21 population confusion caused by exactly that. So: three surfaces, nine instances, **five agents**, one week.

**What this does to my recommendation.** In the body above I preferred the **corollary** (*verify a load-bearing pointer against the referent, not the field*) over the primary clause, on the grounds that it asks one consumer for one check at the moment of most attention. **The addendum strengthens that preference rather than complicating it** — because the corollary generalizes across all three surfaces unchanged, while a primary clause would need a separate rule per surface ("update the header," "update the line number," "tense-mark the census"). One consumer-side discipline covers what three author-side disciplines would.

**Concrete cheap instrument, offered for your judgment, not asserted:** the `file:line` surface is the one that is **mechanically checkable** — a citation of the form `path.py:NNN` can be resolved and its neighbourhood matched against the citing text. The header surface is not (it requires a `git` call per dispatch). If any of this ships as tooling rather than as prose, the `file:line` half is where it pays.

**Routing for the five stale refs themselves:** gamora flagged rather than fixed, correctly — they were outside a comment-truth scope she was right to keep tight. They are hers to correct when she next opens that file; **I am not dispatching a session for five line numbers**, and recording that decision so their survival is a choice rather than a lapse.

---

## ⚑ SECOND ADDENDUM, same day — I dispatched a fix for a defect that had already been fixed, and I am the one who argued for the check that would have caught it

**This is the strongest evidence in the filing and it is against me.** Bank it accordingly.

**What happened.** I routed instance-3-of-the-third-surface — `generation/MIGRATION.md:229`'s *"6 Wave-C kits"* — to rocket as a live doc-truth defect, quoting gamora's finding. rocket's return, in his words:

> *"Premise partially refuted — the named line was already fixed."*

It was repaired at **`0a07c144`** (rocket, 2026-08-24 18:52) **and pushed** — roughly eighteen hours before I dispatched it. It now carries a bordered **"PROJECTED, NOT MEASURED"** box with the projected/measured split, the 6/18/21 disambiguation, and gamora's attribution. **The dispatch was written against a stale read, not against a stale doc.**

**Why this is not merely embarrassing — it is the exact shape under review.** gamora's carry note in `simulation/MIGRATION.md:640-642` is itself **a pointer that no longer points.** Her note was true when written. The referent moved. Nothing re-checked it. I then followed the pointer, found it plausible, and *acted on it without resolving it* — spending a specialist session on a repair that had already landed.

**And I had already written the rule against doing that, in this file, hours earlier:**

> *"a dispatch header is evidence, not proof. Where a header's state is load-bearing for a decision, verify against the tag / commit / origin, not against the field."*

**Load-bearing does not get narrower than "this dispatch exists because of it."** One `sed` at the cited line — the same call I ran twenty minutes later before dispatching elrond, having learned it the expensive way — would have shown the box.

**⚑ What this does to the recommendation: it moves the corollary from *preferable* to *the load-bearing clause*, and it widens its trigger.** My body text scoped the corollary to consumers of `Status:` headers. That scope is too narrow by exactly this case. The corrected form:

> **Before ACTING on a routed finding — dispatching it, gating on it, or citing it as a premise — resolve its pointer at source.** A carry note, a `→ agent` routing line, and a `Status:` header are all the same instrument: a cheap reference to an expensive fact, recorded by someone who could not know when the fact would move. **The one who acts is the one who must re-resolve, because they are the only party present at the moment it becomes load-bearing.**

The author-side clause could not have saved this one. gamora's note was correct at authorship; there is no edit she failed to make. **Only the consumer-side check was ever going to catch it** — which is the argument the body makes, now demonstrated rather than asserted.

**A refinement I did not previously see, and which I would not have believed without this case: a stale routing is worse than a stale header, because it is *actionable*.** A stale header produces a false alarm someone may notice and dismiss. A stale routing **produces a dispatch** — it converts the error into a specialist session, cross-repo commits, and a push, before anyone reads it critically.

**What it cost, and the honest ledger** — because a self-report that inflates its own harm is as useless as one that hides it:

- **Cost:** one rocket session (~2.4 min, 18 tool calls) on a premise that was 18 hours dead.
- ⚑ **Return, which was real:** the neighbourhood sweep I ordered — the part of the dispatch that was *not* premised on the stale pointer — **found a live instance at `:266`**, a bare *"the 9 Wave-C kit rosters"* reading as census. It is the same defect **inside the very document that adopts the anti-census convention six lines earlier at `:260`**. rocket's line: *"A convention its own document breaks in the next paragraph is not yet a convention."* Fixed at `9d4ee5d1`, pushed.
- **The lesson that survives both:** the dispatch paid for itself **through its sweep clause, not its premise.** *"Sweep for the class, not just the instance, and report the count including zero"* is a cheap clause that made a dead dispatch productive. **Where a routed finding might be stale, ordering the sweep alongside the fix converts a wasted session into a live one.** I intend to keep writing it, and I note that it worked here by accident rather than by design.

**One measurement banked in passing** (rocket, read-only over `corpus.db`, 574 kits / 1,224 kit-skills): effect-tags `orbit` / `placed_lane` / `walls_demand` fire **0 / 0 / 0** times — **neither Wave-C tagging rule has ever fired on real data**, while 21 skills carry `orbit` geometry by the mapping path. That is a separate finding, routed to the `AOE_GEOMETRIES` deferral (routing record item 4), and recorded here only so it is not lost in a completion summary.
