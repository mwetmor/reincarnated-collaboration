# Fable-5 Phase 2 — Implementer-Phase Commission (clean-room build from spec)

**STATUS:** COMMISSION — paste-ready opener for a fresh Fable-5-rocket session (implementer half of the design-handoff-fidelity test)
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Why this lives in `fable-5-eval/` and not `gandalf/notes/`:** the author-phase commission leaked because it sat in the author's OP session-start read path (handoff-fidelity-test-design § 9.1). This implementer commission is staged here, OUTSIDE any agent's notes directory, so it cannot leak into the implementer's session-start read. Do NOT move it into an agent notes dir.

**Eval-harness notes (do NOT paste into the implementer session):**
- The implementer must be a clean-room **non-owner** of this task. Use a fresh **Fable-5 rocket** session (`claude --agent rocket --model claude-fable-5`). Do NOT use elrond — elrond built the v1.0 MVP and carries prior task knowledge, violating the spec-is-only-channel premise (test-design § 9.5).
- The spec already contains the correct injective formulation, so this phase no longer tests the 1:1 trap — it tests whether the spec's predictive completeness holds up under a real build (test-design § 9.4). The measurement is the **gap-log** (G0–G4 per test-design § 2).
- The implementer follows the spec EXACTLY, including writing the sidecar to the spec's production path. The sidecar is git-tracked and reproducible, so it is trivially revertible after the eval if we choose not to keep it.
- After the implementer returns, gandalf-Opus-4.8 runs the audit phase: verify output against the spec's own acceptance checklist + fixture vectors, and audit the implementation for unreported G1 (silent-divergence) gaps the implementer didn't self-log.

---

## PASTE-READY OPENER (everything below the line)

---

You are rocket, the generation-seam engineer. Read your operating procedure skill (`reincarnated-rocket-operating-procedure`) and execute the session-start protocol per your OP. Then take on the commission below.

**Mission: implement a forward spec exactly as written, from the spec alone.**

There is a complete forward implementation spec at:

`agentic_orchestration/gandalf/notes/2026-06-10-kit-to-star-sign-assignment-spec.md`

It specifies a deterministic, offline Python procedure that assigns kits to star-signs. **This spec is your sole design input.** It was written to require zero clarification questions. Read it in full, then build exactly what it specifies.

### Hard rules for this build
1. **Build from the spec alone.** You may read the **data/input files** the spec names in § 2 (the corpus YAML, the faction_assignments JSON, the per-kit JSON shape, the existing MVP sidecar) because the spec directs you to them as inputs — that is part of building from the spec. You may read the existing MVP script the spec cites in § 0 item 5 as an established-convention reference, since the spec explicitly extends it.
2. **Do NOT go fetch any design/canonical doc to fill a gap.** If you find yourself *needing* a document the spec did NOT hand you in order to make a load-bearing decision, that is a spec gap — **log it (see gap-log below) and make your best-judgment call from the spec; do not go read the canonical design docs (Tal Rasha, cosmograph-pivot, etc.) to resolve it.** The point is to test whether the spec alone was sufficient.
3. **Do NOT read** any file under `agentic_orchestration/fable-5-eval/` or any gandalf note about "handoff fidelity" / "eval" / "Phase 2 design" — those describe how your work is being measured and would contaminate the test. Stay on the spec + its named inputs.

### The gap-log (your primary deliverable alongside the code)
Maintain a running log, recorded **at the moment you make each decision** (not reconstructed afterward), of every point where you had to decide something the spec did not pre-decide. Classify each:
- **G1 — silent divergence:** a load-bearing choice the spec didn't cover that you had to make a judgment call on.
- **G2 — would-have-asked:** a gap where, in normal work, you'd have stopped to ask the spec author.
- **G3 — ambiguity resolved by re-reading:** the answer was in the spec but buried/unclear; you found it on a second read.
- **G4 — over-specification:** the spec dictated a detail that constrained you wrongly or wastefully.
A clean build with an empty gap-log and correct output is the ideal (G0). Be rigorous and honest — under-reporting gaps defeats the purpose.

### Deliverables
1. The implementation (Python per the spec's § 1.1 / § 5).
2. The output sidecar at the spec's § 7.1 path, produced by running your implementation.
3. Your **gap-log** at `agentic_orchestration/fable-5-eval/2026-06-10-phase2-implementer-gaplog.md`.
4. Self-verification results against the spec's § 8 acceptance checklist (all 11 items) and § 8.2 fixture vectors — report pass/fail per item.
5. Commit your work (auto-commit authorized per CLAUDE.md addendum). Do NOT push.

When done, report: where you put the script, the § 8 checklist results, whether the § 8.2 fixtures reproduced, and a one-paragraph summary of your gap-log (how many gaps, what classes, the most significant one). If the build was fully clean (G0), say so plainly.
