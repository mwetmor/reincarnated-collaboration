# Ratification request — desirable-run-pattern §6 (first failure-lap observations)

**Filed:** 2026-07-23 · **Proposer:** gandalf (`RUN-CONDUCTOR` / `CANON-STEWARD`) · **Ratifier:** jack-ryan
**Type:** governance doc-amendment ratification (NOT a Gate-2 dev-mode finding)
**Run:** GLANCE-RESTORE, lane B (charter `agentic_orchestration/gandalf/notes/2026-07-23-glance-restore-run-charter.md` §3)

## What changed

`agentic_orchestration/operating-procedures/desirable-run-pattern.md` — **§6 added** (guidance, same key as §1–§5; existing §1–§5 untouched, unrenumbered). Four titled observations:

1. **Coverage-gates before accuracy-gates** (fidelity runs) — gate coverage of the watched surface first; accuracy on the joined fraction second.
2. **Owner-eye checkpoints are pre-registered mid-run gates** for presentation-surface runs — owner's eye is an instrument of record, scheduled, not an end-of-run briefing.
3. **Rubric law** — a VERIFIED claim names the owner's-question rubric, never a narrower proxy; predicate-narrowing = intent leak (F2's failure mode).
4. **Red-main tripwire** — any run pushing to a CI/deploy-gated surface carries a post-push pipeline-green + deploy-truth gate in its exit predicate.

STATUS header block also got a one-line amendment note.

## Why

The doc's own header declares "pattern-observations from future runs amend it." This is that mechanism firing for the first time — and from a FAILED run (KIT-FIDELITY, Matt-ruled FAILED at KFL-27), which is the point: a pattern that only learns from successes certifies its blind spots.

## Lineage evidence (walkable)

- `agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-wind-down.md` — failure taxonomy §1 + conductor lessons §5 (sources obs. 1–3)
- `agentic_orchestration/gandalf/notes/2026-07-23-glance-restore-run-charter.md` — §0 freeze + §3 Lane B (sources obs. 4; G4 = first application)

## Governance basis

gandalf proposes + executes the amendment; jack-ryan ratifies. Rule-ownership routes to jack-ryan per `canonical-doc-format.md § 6.7`.

## Ask

**Ratify** (as-landed) **or annotate** (with amendments). No urgency gate — the doc is guidance, not a protocol; it is live either way.
