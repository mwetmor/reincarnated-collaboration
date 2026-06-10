# Fable-5 Phase 2 — Author-Phase Commission (kit-to-star-sign assignment spec)

**STATUS:** COMMISSION — paste-ready opener for a fresh Fable-5-gandalf session (author phase of the design-handoff-fidelity test)
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Eval design:** `agentic_orchestration/gandalf/notes/2026-06-10-fable-5-handoff-fidelity-test-design.md`
**Protocol note (do NOT paste this section into the author session):** This is the AUTHOR phase. The author writes a forward implementation spec; a *separate* fresh Fable-5-rocket session (the implementer phase) later builds from that spec and nothing else (clean-room air-gap, eval design § 3). The commission below is written to be neutral — it asks for a complete implementation spec but **deliberately does NOT telegraph the 1:1-binding assignment-problem trap.** Whether the author reads the canonical Branch A binding, recognizes that 1:1 binding makes naive nearest-centroid wrong (it becomes a bipartite assignment problem), and specifies the correct formulation — *that recognition is the test.* If the commission names the trap, the test is void. Launch this as a fresh Fable-5 session (no shared context with this Opus 4.8 session).

---

## PASTE-READY OPENER (everything below the line)

---

You are gandalf, the story-and-design steward. Read your operating procedure skill (`reincarnated-gandalf-operating-procedure`) and execute the session-start protocol per OP § 1. Then take on the commission below.

**Mission: author a forward implementation spec for kit-to-star-sign assignment.**

The engine generates **kits** (the substrate-grounded gameplay loadouts). The game's creation-moment architecture binds kits to **star-signs** (the constellations of the cosmograph night-sky). We need a deterministic, offline-runnable procedure that assigns kits to star-signs, and we need it specified well enough that a *separate engineer who has never spoken to you* can implement it correctly from your spec alone — zero clarification questions. Your spec is the only thing they will receive.

**This is a design-spec-as-math handoff (Discipline #18).** Math and data contracts first; the spec must be precise enough to implement without judgment calls. Treat under-specification as the failure mode: every decision you leave to the implementer is a decision you got wrong.

### Required discipline (declare at the top of your spec)
1. **Canonical-source-consultation declaration** — before authoring, read the relevant source canonical docs in full (NOT ground-state oracle one-liners). At minimum, consult the Branch A kit↔star-sign binding architecture and the kit-to-star-sign MVP commission. Find the current sources via `canonical/00-ground-state.md` and the canonical/story creation-moment lineage; the elrond MVP commission is at `agentic_orchestration/legolas/` or `agentic_orchestration/elrond/` notes (search for `kit-to-star-sign`). Declare every doc you read in full at the top of the spec.
2. **Substrate-led** — any hand-curated mappings in the canonical sources are authoritative anchors your algorithm must *respect*, not override.
3. **Recognition-validate-commit** — flag any value you scaffold/placeholder explicitly; do not present a guess as a locked decision.

### Required spec contents (the implementer must be able to build from these alone)
- **Input data contracts** — exact shape of a kit record (which fields feed the assignment), the exact star-sign set being assigned to (name it precisely — there is more than one candidate set in the canon; pick the canonically-correct one and justify), and the feature/representation space the assignment operates in.
- **The algorithm** — stated as math, then as procedure. Distance/similarity metric and why. How the assignment is computed. Determinism guarantees. Tie-breaking rule.
- **Constraints** — any cardinality/binding constraints the canon imposes on the kit↔star-sign relationship, and how the algorithm satisfies them. (Read the binding architecture carefully; the relationship's cardinality dictates the algorithm class.)
- **Edge cases** — count mismatches between kits and star-signs (both directions), degenerate/empty features, kits with no valid representation.
- **Output schema** — exactly where and how the assignment result lands in the season-output JSON; field names and types.
- **Acceptance criteria** — a checklist an implementer can self-verify against, plus a smoke-test description.

### Output
Write the spec to a standalone file at `agentic_orchestration/gandalf/notes/2026-06-10-kit-to-star-sign-assignment-spec.md`, STATUS-stamped as a forward implementation spec (Fable-5 Phase 2 author phase). Commit it (auto-commit authorized per CLAUDE.md addendum). Do NOT implement anything — spec only. When done, report the spec path and a one-paragraph summary of the assignment approach you specified.
