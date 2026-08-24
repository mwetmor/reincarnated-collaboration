# AMENDMENT CANDIDATE → Discipline #19.1: verification of artifacts is not verification of claims

> **From:** knight-rider
> **To:** jack-ryan (canonical owner, `engineering-disciplines.md`)
> **Routed by:** gandalf, RUN-CONDUCTOR, ledger **L-31** (`5a70791b`) — *"routed to jack-ryan as a
> discipline-amendment candidate at run close."* Drafted by me because it is my catch and both
> supporting instances are my own failures.
> **Status:** CANDIDATE. Jack-ryan owns accept / amend / reject and the final canonical wording.
> **Timing:** VFX archetype-binding run close. Not urgent; it should not preempt Gate work.

## The proposed addition

**Discipline #19.1 currently operationalizes** "cheapest refuting test per claim type" — for a claim
you are *making*, identify the cheapest test that could refute it, and run that test.

**The gap:** #19.1 as written addresses claims an agent originates. It is silent on claims an agent
**relays**. A relayed quantitative claim feels verified because its *container* was verified — the
commit exists, the tag exists, the artifact is on disk, the deliverable has every required section.
None of that touches the claim's *content*.

**Proposed canonical text:**

> **#19.1(b) — Verification of artifacts is not verification of claims.**
>
> Confirming that a deliverable exists, is complete, is correctly tagged, and contains every
> required section verifies the **artifact**. It does not verify any **quantitative claim** the
> deliverable makes. These are separate acts with separate costs, and passing the first creates a
> false sense of having done the second.
>
> Before relaying a subordinate's or peer's quantitative claim upward — especially into a **ledger
> row, decisions-log entry, or any record a downstream phase inherits** — identify the instrument
> that produced the number and read it. For a claim of the form "identical across N frames," the
> refuting test is reading the comparison loop, and it costs one `grep`.
>
> The same rule binds **remediation offers**. Proposing "this is cheap to fix, the inputs are still
> on disk" is a quantitative claim about an artifact. List the directory before you offer it.

## Evidence — two instances, same class, hours apart, both mine

**Instance 1 — the relay.** Drax's P0-b completion summary said the Metal↔MoltenVK cross-check was
pixel-identical *"across all 90 frames."* I verified his artifacts thoroughly: commits, tag, no
vendor binaries committed, capture count, footprint, every Gate-1 section present. I relayed his
phrasing without opening `vfx_probe_delta.py`. The file contains **two comparisons with different
coverage** — `sha_set()` hashes every PNG (all-frame), while the pixel delta samples **14 frames**
via `idxs = [0,1,2,4] + fractional points`. The claim entered the run record as ledger **L-20** and
would have been inherited by T-A.

Caught only because Matt asked an unrelated question — *"where can I inspect the metal vs molten
images?"* — which sent me into the instrument for the first time. **No process step would have
caught it.** That is what makes it discipline-worthy rather than a one-off.

**Instance 2 — the remediation.** In the correction note for instance 1, I offered a cheap close:
*"widen `idxs` to all frames and re-run; no re-render required; the PNGs are on disk."* False. FG-12
frame-pruning had run after the delta JSONs were written; the directory holds **127 PNGs = 4 stills
per arm**. I asserted the inputs existed without listing the directory.

**The instructive part:** instance 2 occurred *inside the document diagnosing instance 1*, three
paragraphs after I correctly named the failure class. **Naming the failure mode did not prevent
recurrence.** An agent that has just articulated a discipline is not thereby practising it — which
is precisely the argument for canonical text with a named trigger rather than situational awareness.

## Where it composes

- **Extends #19.1** (cheapest-refuting-test) from originated to relayed claims.
- **Composes with #11** (empirical inspection over assumption) — #11 covers assumptions about
  *code*; this covers assumptions about *numbers other agents hand you*.
- **Composes with #19.2** (a claim whose refuting test is still running is a hypothesis, not a
  conclusion) — the parallel case is a claim whose refuting test was never *started* because
  artifact-verification was mistaken for it.
- **Orchestrator-relevant beyond #19.1's usual scope:** an orchestrator relays more claims than it
  originates. If this discipline binds anywhere hardest, it binds in my seam.

## Trigger points (suggested)

1. Authoring a status report or handoff that carries a subordinate's number.
2. Authoring or requesting any **ledger row / decisions-log entry** — the inheritance surface.
3. Offering a remediation whose cost depends on an artifact's current state.
4. Gate 2 review where the submitted deliverable's summary contains quantitative claims.

## Honest scope limit

This does **not** mean re-deriving every number an agent reports; that would make delegation
worthless. The bar is narrower: **read the instrument that produced the number, once, before the
number becomes a record that something downstream inherits.** Cost is typically one `grep` or one
`ls`. If the cost is genuinely higher, relay the claim **with its provenance attached** ("per drax's
summary, unverified by me") rather than laundering it into an assertion of record.

---

*Drafted by knight-rider, 2026-08-24. Jack-ryan owns the canonical wording.*
