# hive-mind-scope-discipline — per-cycle scope-of-autonomy enumeration

> **STATUS:** CURRENT (load-bearing as of 2026-05-25) — refinement of hive-mind entry protocol per Matt directive resolving recurring knight-rider over-asking behavioral bug
>
> **Authored:** 2026-05-25
> **Author:** gandalf (story-and-design steward; protocol-author lineage)
> **Authority:** Matt 2026-05-25 — "Maybe it is best to draft a hive mind document each time with hive mind scope for that sprint?"
> **Pattern:** per-cycle scope-doc authored at cycle-open; ratified by Matt; consumed by knight-rider as authority-of-record for the cycle

---

## 0. What this discipline IS and IS NOT

**IS:** the operational discipline that every Matt-authorized hive-mind cycle (and every multi-stage non-hive-mind sprint that involves knight-rider orchestration) opens with an explicit **scope-doc** enumerating what knight-rider can autonomously decide + execute + commit + push for that cycle. The scope-doc is **authoritative for the cycle** — knight-rider treats it as the ground-truth answer to "is this in my scope?"

**IS NOT:** the substantive cycle protocol (each cycle authors its own protocol/state doc at cycle entry, e.g. `agentic_orchestration/cycle-<N>-hive-mind-state.md`). NOT a substitute for ADR-002 tiered approval (architectural commitments still escalate per ADR-002 regardless of scope-doc). NOT a replacement for hive-mind decision-routing § 4 (seam-owner-first routing still applies; scope-doc just removes inference ambiguity about WHICH decisions are KR's to route vs Matt's to make).

---

## 1. Why this discipline exists — root cause diagnostic

### 1.1 The behavioral bug

Recurring pattern observed 2026-05-24 / 2026-05-25 in knight-rider operation:

| Failure mode | Example |
|---|---|
| KR pauses on in-scope decisions | "Awaiting your direction on (1)+(2)+(3) before firing" where (1) and (2) are clearly in-scope orchestration calls |
| KR pauses on routine commits | "Awaiting your 'commit + push' go" for work-products of authorized cycle work |
| KR pauses on sequencing | "Confirm sequence to proceed" for items in seam-owner scope per hive-mind decision-routing |

### 1.2 Root cause — scope-inference ambiguity collapses to ask-safety

Current state: knight-rider must INFER her scope-of-autonomy for each cycle from:
- The cycle's opening dispatch language
- The hive-mind-protocol.md § 4 verbatim Matt directive (decision-routing)
- The CLAUDE.md commit/push addendum (2026-05-25)
- ADR-002 tiered approval table
- The substantive cycle protocol doc
- Precedent from prior cycles

This inference surface is large. When inference is ambiguous, knight-rider correctly applies safety-default = ask. **Ask-safety is being preferred over forward-motion.** The behavioral pattern is rational given the inputs; the inputs need to change.

### 1.3 The architectural fix

Move scope from **inferred** to **enumerated.** Each cycle opens with a scope-doc that affirmatively lists what's in-scope. Ambiguity defaults to in-scope, not to ask-safety. Knight-rider reads the scope-doc once at cycle-open, consults it when in doubt, and fires forward without re-asking unless an item is explicitly listed out-of-scope or unenumerated.

### 1.4 What the bug is NOT

- NOT knight-rider lacking authority (the authority exists per hive-mind decision-routing § 4)
- NOT knight-rider missing the CLAUDE.md commit addendum (she reads it on session-open)
- NOT Matt being unclear in cycle-opening dispatches (the dispatches are clear about WORK; they're under-specified about AUTHORITY)
- IS the absence of an affirmative scope-enumeration artifact per cycle

---

## 2. When to author a scope-doc

### 2.1 Mandatory

- **Every hive-mind cycle open** (per hive-mind-protocol.md § 2.2 entry protocol — scope-doc authoring becomes step 1.5, between protocol authoring and Gate-1 review)
- **Every multi-stage non-hive-mind sprint** that involves knight-rider orchestration across 3+ dispatches or 2+ days
- **Every cycle reset / re-scope** that materially changes what KR can autonomously fire

### 2.2 Optional

- Single-dispatch routine work (no scope-doc needed; the dispatch IS the scope)
- Direct Matt → specialist Pattern B dialogues that bypass knight-rider entirely
- Ad-hoc one-shot critique invocations

### 2.3 Retroactive

A cycle already in flight without a scope-doc can have one authored mid-cycle. Treat as cycle-reset for the unfired portion. Cycle 10 (in flight 2026-05-24/25) is the founding retroactive example — see `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md`.

---

## 3. Who authors the scope-doc

**Default pattern:** gandalf drafts → Matt ratifies in <2 min.

**Rationale:**
- Gandalf reads the cycle's opening dispatch + canonical state as part of session-start (per gandalf OP § 1)
- Cycle-shape is already in gandalf's context at cycle-open
- Matt's load stays minimal (read + ratify)
- Gandalf is the protocol-author per hive-mind-protocol.md § 12 + § 14 maintenance authority

**Alternative patterns** (use when default doesn't fit):
- **Matt authors directly** when cycle opens in a Matt-Pattern-B session and the scope-doc is faster to author than to commission
- **Knight-rider self-authors as cycle-opening artifact, Matt ratifies** when KR has the clearest read on operational scope (KR is the consumer of the scope-doc; self-authoring removes one indirection)

**Ratification:** Matt's ratification is the authority-of-record. Until ratified, the draft scope-doc has no force. Ratification can be verbal in-session or written ("ratified" / "approve" / "fire as-is").

---

## 4. Template

Scope-doc lives at `agentic_orchestration/cycles/cycle-<N>-hive-mind-scope.md`. Structure:

```markdown
# cycle-<N>-hive-mind-scope

> **STATUS:** RATIFIED <YYYY-MM-DD> — Matt ratification
> **Cycle:** <N>
> **Cycle subject:** <one-line description>
> **Canonical protocol doc:** <path or "none — non-hive-mind sprint">
> **Effective:** <YYYY-MM-DD> through <cycle-final-tag>

## 1. In-scope autonomous decisions (knight-rider fires without re-asking)

- <decision class 1>
- <decision class 2>
- ...

## 2. In-scope autonomous executions

- <execution class 1>
- <execution class 2>
- ...

## 3. In-scope autonomous commits

- <commit class 1>
- <commit class 2>
- ...

## 4. Push posture for this cycle

One of:
- `push-per-wave` (auto-push after each wave completion)
- `push-at-cycle-close` (auto-push at cycle close)
- `push-ask` (default — ask before push)
- `push-per-commit` (auto-push after each commit — use sparingly)

## 5. Out-of-scope — MUST escalate to Matt

- <escalation class 1>
- <escalation class 2>
- ...

## 6. Pre-resolved known-unknowns

- If <X> happens during cycle → <do Y>
- If <Z> happens during cycle → <ask Matt>
- ...

## 7. Cross-cycle escalation triggers (rare)

- <condition that ends scope-doc applicability and triggers re-scoping>

## 8. Sign-off

**Drafted by:** <gandalf | matt | knight-rider>
**Ratified by:** Matt <YYYY-MM-DD>
**Authority basis:** <cycle protocol doc § / Matt directive verbatim / ADR ref>
```

### 4.1 Template principles

- **Affirmative enumeration over inference.** List what's in-scope explicitly. Ambiguity = in-scope by default, not ask-safety.
- **Specific over abstract.** "Fire Stage-3 execution dispatches; commit dispatch artifacts" beats "routine orchestration."
- **Pre-resolve foreseeable ambiguity.** § 6 catches the cases that would otherwise become ask-pauses.
- **Brief.** A scope-doc that takes >5 minutes to read defeats its purpose. Target: 1-2 pages.

---

## 5. How knight-rider consumes the scope-doc

### 5.1 Session-start protocol (refinement of KR OP § 1)

When knight-rider opens a session for an active cycle:

1. Standard session-start reads per KR OP § 1
2. **Read the cycle scope-doc** at `agentic_orchestration/cycles/cycle-<N>-hive-mind-scope.md` — treat as authority-of-record
3. **Cross-check scope-doc against current cycle state** — if cycle has materially evolved beyond scope-doc, flag for Matt re-scoping BEFORE firing

### 5.2 In-flight decision protocol

When a decision surfaces during cycle execution:

1. **Check scope-doc § 1-3** — is this in enumerated autonomous scope? If YES → fire (apply hive-mind decision-routing § 4 to choose seam-owner-vs-self).
2. **Check scope-doc § 5** — is this in enumerated out-of-scope? If YES → escalate to Matt.
3. **Check scope-doc § 6** — is this a pre-resolved known-unknown? If YES → apply pre-resolved guidance.
4. **If unenumerated** — default to in-scope and fire forward; flag the gap to gandalf for next-cycle scope-doc refinement. Ambiguity does NOT default to ask.

### 5.3 Anti-pattern — "but the scope-doc didn't say I could"

The scope-doc enumerates affirmative scope + explicit out-of-scope. Items NOT mentioned default to in-scope (per § 5.2 step 4). Knight-rider does NOT treat scope-doc as exhaustive whitelist. The scope-doc removes ambiguity for KNOWN cases; unknown cases follow hive-mind decision-routing § 4 (seam-owner-first) + forward-motion bias.

---

## 6. Composition with existing protocols

### 6.1 Composes with hive-mind-protocol.md § 2 (entry protocol)

Entry-protocol step 1.5 (NEW) — scope-doc authored + ratified BEFORE step 2 (jack-ryan Gate-1 review). Scope-doc and Gate-1 review can run in parallel if both authored same session.

### 6.2 Composes with CLAUDE.md "Team commit + push discipline" addendum (2026-05-25)

The CLAUDE.md addendum establishes default per-agent auto-commit patterns. The cycle scope-doc REFINES the default for that cycle — typically expanding (e.g., push-per-wave instead of default push-ask) but can also constrain (e.g., "no commits during W3 because we're in mid-experiment state").

### 6.3 Composes with hive-mind decision-routing § 4 (seam-routing)

Scope-doc does NOT override seam-routing. Within scope-doc autonomous scope, KR still routes seam-touching decisions to seam-owning sub-agents first. Scope-doc just removes the meta-question "is this even in my scope to route?"

### 6.4 Composes with ADR-002 tiered approval

Scope-doc CANNOT grant authority that exceeds ADR-002 tier-2 or tier-3 thresholds. If a decision surfaces during cycle that exceeds tier, KR escalates per ADR-002 regardless of scope-doc enumeration. Scope-doc is operational, not constitutional.

### 6.5 Composes with gandalf OP § 2 (Pattern A / Pattern B dialogue)

Gandalf's scope-doc authoring is a Pattern-B output for Matt (sustained dialogue → ratified artifact). Falls under existing gandalf authoring discipline; no new mode required.

---

## 7. Maintenance + amendment

- **Cycle-scope-doc amendments** within an active cycle require Matt ratification (same authority bar as original ratification)
- **This discipline doc amendments** follow gandalf OP § 4 + hive-mind-protocol.md § 12 — gandalf authors; jack-ryan reviews process-side; Matt ratifies material amendments
- **Discipline retirement** would require Matt directive; until then, scope-doc authoring is mandatory per § 2.1

---

## 8. Cross-references

### Companion docs
- `agentic_orchestration/operating-procedures/hive-mind-protocol.md` — universal hive-mind work-mode skill (this discipline composes on top)
- `agentic_orchestration/operating-procedures/knight-rider.md` § 3.5 — KR commit/push discipline (this discipline supplies the per-cycle authority surface)
- `CLAUDE.md` § "Team commit + push discipline" — team-level commit/push addendum (this discipline refines per-cycle)
- `agentic_orchestration/cycles/` — scope-doc artifact directory

### Authority basis
- Matt 2026-05-25 verbatim: "Maybe it is best to draft a hive mind document each time with hive mind scope for that sprint?"
- Matt 2026-05-23 verbatim hive-mind decision-routing directive (in hive-mind-protocol.md § 4)
- ADR-002 tiered approval (in `agentic_orchestration/GOVERNANCE.md`)

### Founding example
- `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md` — retroactive Cycle 10 scope-doc (the first canonical instance of this pattern)

---

## 9. Sign-off

**Author:** gandalf (story-and-design steward; protocol-author lineage)
**Authority:** Matt 2026-05-25 directive
**Status:** CURRENT — load-bearing for all knight-rider-orchestrated cycles starting Cycle 10 retroactively + Cycle 11+ prospectively
**Maintenance:** gandalf authors + maintains; jack-ryan reviews process-side; Matt ratifies amendments
