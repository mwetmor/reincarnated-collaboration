# Discipline candidate — "A presentation run terminates in frames at the play camera"

**Proposed by:** gandalf (`CANON-STEWARD`), 2026-07-24
**Ratifier:** jack-ryan (per `canonical-doc-format.md` § 6.7 — gandalf proposes, jack-ryan ratifies)
**Target:** `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — next free number (#63 at time of writing)
**Origin:** self-diagnosed defect in a gandalf-authored charter. This is not a proposal about someone else's failure.

---

## The proposed rule

> **Any run, dispatch or wave whose SUBJECT is the presentation layer does not meet its exit
> predicate until it produces images rendered at the play camera.**
>
> Cells, matrices, JSON payloads, latency tables and prose are *instrumentation*. They may
> accompany the frames. They may not substitute for them.
>
> Corollaries:
> 1. **The play camera, not a model viewer.** An asset photographed in isolation answers a
>    different question than the same asset at the gameplay camera, and answers it wrongly.
> 2. **Judgeable by the human, unaided.** If Matt must read a table to know whether the run
>    succeeded, the run has not produced its deliverable.
> 3. **The harness is not optional scope.** If no capture harness exists, building one is
>    inside the run, not deferred out of it.

## Why — the evidence

**The failure.** The 2026-07-23 MCP bake-off (charter: `2026-07-23-mcp-bakeoff-run-charter.md`) ran
18 cells across 3 instruments and 6 probes. It produced PASS/FAIL cells, JSON payloads, a latency
table and a verdict recommendation. It produced **zero frames of what the player camera sees.**

Matt, 2026-07-24: *"I cannot interpret these results without anything to judge."*

That is a complete verdict on the run. The subject was the presentation layer; the deliverable was
not presentable.

**The aggravating detail.** Probe P1 was literally an *isolated-asset* capture probe — a model
viewer. Diablo III's team moved monster-silhouette review off the model viewer and onto the gameplay
camera precisely because a creature that reads beautifully at 3 m and eye level can be unreadable at
the ARPG camera. We rebuilt the rejected viewing condition and called it a probe.

**The aggravating detail that stings.** `reincarnated-godot/scripts/shoot_costume_variants.gd` —
drax, 2026-06-21 — is a variants→contact-sheet→human-eye-pick harness. It existed, it worked, and it
had been used a month before the bake-off. **The practice was not missing. The charter regressed
from it.** A discipline is warranted precisely because good practice already existed and a
well-formed charter still walked past it.

**The mechanism, named.** The bake-off charter's rubric law read: *"the owner's question is 'which
instrument serves our **proven** needs'"* — a backward-looking construction. *Proven* needs were
verification-era needs, so the probe set weighted observation over authoring 4:2, and observation
probes naturally terminate in measurements. **The frame requirement is the guard that makes an
instrumentation-shaped charter still deliver a judgeable artifact.**

## Relation to existing canon

This is the **run-level enforcement** of the A1 presentation law already ruled by Matt in
`canonical/current-to-end-state/current-to-end-state-game.md` PART A:

> *"Only author and judge what the player camera sees."*

A1 governs authoring. It was not read as governing *runs about* authoring, and the gap let a
presentation run ship without a presentable artifact. The proposed discipline closes exactly that
gap and adds nothing else.

## Scope boundary — what this does NOT say

- It does not require frames from runs whose subject is engine math, corpus extraction, telemetry or
  schema. Those have their own exit predicates.
- It does not forbid instrumentation. The bake-off's latency finding (114–180 ms/call → ~2.5 min of
  pure wire time per 1,000 nodes) was genuinely load-bearing and is the reason the wire will never
  carry assembly. Keep the tables. Add the pictures.
- It does not require *beautiful* frames. It requires *judgeable* ones. A frame showing a failure is
  a passing deliverable.

## Already in force downstream

KIT-REPLICA LAP-1 (`2026-07-24-kit-replica-lap1-run-charter.md` §6) was written under this rule
before it was proposed, in the charter's own words: *"No cell, JSON or prose substitutes for a
picture. A presentation run that produces no judgeable frame has not met its exit predicate."* Its
honorable fallback exists so that **every room ships a frame even when its method fails.** That is
the shape the discipline should produce.

---

**Signed:** gandalf, 2026-07-24. Proposed, not ratified. jack-ryan holds the pen on the canonical text.
