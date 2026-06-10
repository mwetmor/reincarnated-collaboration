# Fable-5 Evaluation — Reshaped Around Design-Handoff Fidelity

**STATUS:** DESIGN NOTE — reshapes the Fable-5 Phase 2/3 commission plan per Matt 2026-06-10 reframing
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Supersedes (in part):** `2026-06-10-session-close-handoff-opus-4-8-resume.md` § 2.2 / § 2.3 commission shape — the *task candidates* survive; the *eval framing* changes
**Gated on:** Fable-5 Phase 1 Gate-1 PASS (jack-ryan adversarial review of `canonical/story/2026-06-10-engine-architecture-canonical-synthesis.md`, in flight)

---

## 0. The reframing (Matt 2026-06-10)

> "I think the real test will be how well a fable 5 agent can predict the necessary details as architectural design which another fable 5 agent will pick up and implement."

This is a sharper eval axis than the one the handoff plan was built on. The original plan tested **each model in isolation**:
- Phase 1 — can Fable-5-gandalf write a synthesis doc?
- Phase 2 — can Fable-5-rocket implement?
- Phase 3 — can Fable-5-gamora do sim-math?

Matt's version tests the **seam between two Fable-5 agents** — the *design handoff*. The question is no longer "is each agent individually competent" but:

> **Does a Fable-5-authored architectural spec carry enough predictive detail that a second Fable-5 agent can implement it cleanly, with zero clarification round-trips?**

This is the more valuable signal. A model that writes beautiful prose but under-specifies the load-bearing engineering decisions will *look* good in isolation and *fail* at the handoff. The handoff is where real multi-agent throughput lives or dies.

---

## 1. What is actually under test — the channel, not the endpoints

The artifact under test is the **spec itself as a communication channel.** Phase 1 (the synthesis doc) was a *recognition/backward-looking* artifact — it describes what already exists. A spec is *forward-looking* — it must anticipate what an implementer will need to decide and pre-decide it.

The synthesis doc proved Fable-5-gandalf can *read and reconcile* a complex canonical lineage. It did NOT prove Fable-5-gandalf can *author forward architecture with predictive completeness.* Those are different muscles. Phase 2 tests the second.

**Endpoints we are NOT primarily measuring:**
- Whether the implementation is correct (necessary but not sufficient — a correct implementation reached through five clarification round-trips is a *handoff failure* even if the code is right)
- Whether the author's prose is good

**The seam we ARE measuring:** the predicted-vs-needed gap.

---

## 2. The metric — clarification-gap

Define the handoff-fidelity score as the inverse of the **clarification-gap**: every decision the implementer had to make that the spec did not pre-decide.

| Gap class | What it counts | Severity |
|---|---|---|
| **G0 — Clean** | Implementer built directly from spec; zero questions | (ideal) |
| **G1 — Silent divergence** | Implementer had to make a load-bearing choice the spec didn't cover, and chose *without flagging* | HIGH — invisible drift; the dangerous one |
| **G2 — Flagged round-trip** | Implementer hit a gap, *recognized* it, and would have needed to ask | MEDIUM — honest but costs a cycle |
| **G3 — Ambiguity resolved by re-reading** | Spec contained the answer but buried/ambiguous; implementer found it on second read | LOW — fidelity present, legibility weak |
| **G4 — Over-specification** | Spec dictated detail that constrained the implementer wrongly or wastefully | LOW-MED — predictive *overreach* (the opposite failure) |

**Scoring protocol:** the Fable-5-rocket implementer is instructed to maintain a running **gap-log** — every point where it had to decide something the spec didn't pre-decide, classified G1–G4, *recorded at the moment of decision* (not reconstructed after). The gap-log IS the primary deliverable, alongside the implementation. A G0 run with an empty gap-log and correct output is the high-fidelity result.

**The honesty guard:** G1 (silent divergence) is the failure mode that an isolated-capability test cannot see. We surface it by requiring the implementer to log decisions *as it makes them*, then having gandalf (Opus 4.8) audit the implementation against the spec to catch G1 gaps the implementer didn't self-report. The delta between self-reported gaps and audited gaps is itself a signal — about the *implementer's* self-awareness, not the spec.

---

## 3. The protocol — leakage prevention

For the handoff to be the thing under test, the spec must be the **only channel.** No author-reasoning, no dialogue, no shared session context.

1. **Author phase (Fable-5-gandalf):** writes a self-contained forward spec for the bounded task. Math-first per Discipline #18 (design-spec-as-math): axis meanings, formula intent, data contracts, acceptance criteria, edge cases. Declares canonical-source-consultation at start.
2. **Air-gap:** the spec is committed as a standalone artifact. The implementer agent is launched **fresh** — it reads the spec + named canonical anchors + the codebase, and *nothing from the author's session.* No "ask gandalf" affordance during the run.
3. **Implementer phase (Fable-5-rocket):** builds from the spec; maintains the gap-log; produces implementation + gap-log + smoke-test.
4. **Audit phase (gandalf Opus 4.8):** audits implementation against spec; catches unreported G1 gaps; scores the handoff.

This is the *clean-room* version of the team's normal critique-pair handoff. In production we *want* the back-channel (it's cheaper to ask than to guess). But to *measure* spec fidelity we have to close the back-channel and see what the spec alone carries.

---

## 4. Reshaped Phase 2 — kit-to-star-sign assignment (the handoff probe)

Task survives from handoff § 2.2 Option α. It is an *excellent* handoff probe because it contains a **natural predictive trap** that separates a deep spec from a shallow one:

**The trap:** Branch A binds kits **1:1** to star-signs (Tal Rasha § 4.1; cosmograph-pivot § 10). A naive "nearest-centroid lookup" is a **many-to-one** map — multiple kits can independently pick the same nearest star-sign. The 1:1 constraint turns this into a **bipartite assignment problem** (linear-sum-assignment / Hungarian), not a per-kit nearest-neighbor.

This is precisely the kind of "necessary detail" Matt's reframing targets. The fidelity question becomes concrete and falsifiable:

> **Does the Fable-5-gandalf spec PREDICT that 1:1 binding makes this an assignment problem, and specify the formulation (cost matrix, global optimization, tie-breaking, the more-kits-than-signs / fewer-kits-than-signs cases)?**
> Or does it say "nearest-centroid" and leave the implementer to discover the trap?

- If the spec predicts it → high fidelity; the implementer builds `scipy.optimize.linear_sum_assignment` cleanly (G0).
- If the spec misses it → the implementer either silently builds the wrong (many-to-one) thing (G1 — the worst, and exactly what we want to catch) or recognizes the gap and round-trips (G2).

**Other predictive details the spec must carry (each a fidelity checkpoint):**
- Input data contract — kit JSON shape; star-sign canonical set (the N≥400 derived signs vs the 88 IAU constellations — *which*?); the feature/embedding space centroids live in
- Distance metric in that space (and why)
- Output schema — where the `star_sign` field lands in season-output
- Degenerate cases — empty centroid, kit with no valid features, count mismatch
- Substrate-led guard — Phase 1 hand-curated mappings (if any exist) are canonical anchors the algorithm must *respect*, not override (the substrate-led discipline probe from the original plan survives intact)

**Why this task over Option β/γ:** the 1:1-assignment trap gives us a single, sharp, binary fidelity signal that the other candidates lack. β (D1 scoring) and γ (B16 loot) are good tasks but have no comparably crisp predictive trap.

---

## 5. Phase 3 disposition — fold, don't run separately

Under the *isolation* framing, Phase 3 (gamora hunter-convergence audit) tested a third seam (sim-math). Under the *handoff* framing it's redundant *as a separate run* — it tests the same property (spec→implementation fidelity) in a different seam, at the cost of a whole extra cycle.

**Recommendation:** defer Phase 3 unless Phase 2 produces an *ambiguous* fidelity signal. If Phase 2 is decisively G0 or decisively G1-heavy, we have our answer about handoff fidelity and Phase 3 adds cost without resolving anything. If Phase 2 is *mixed* (e.g., G0 on the easy details, G1 on the assignment trap), then run Phase 3 (hunter audit) as a *second handoff probe in a different seam* to test whether the fidelity gap is task-specific or model-general.

This honors scope-control: one decisive probe before a second.

---

## 6. What the three-part eval memo now measures

The eval memo (handoff § 2.4) is reframed:

| Dimension | Old (isolation) | New (handoff) |
|---|---|---|
| **Primary** | Per-agent capability | **Handoff fidelity — clarification-gap score (G0–G4)** |
| Quality | Synthesis + impl + math each scored | Implementation correctness as *necessary floor*; fidelity as the headline |
| Discipline | Per-agent discipline adherence | Did the *spec* encode the disciplines such that the implementer inherited them without being told? (e.g., did substrate-led survive the handoff?) |
| Cost | Tokens vs Opus baseline | Tokens **+ round-trips saved/incurred** — a high-fidelity spec that costs more tokens up front but saves N round-trips is net-cheaper |
| Seam-fit | gandalf vs rocket vs gamora | **Author-seam vs implementer-seam** — is Fable-5 better at *writing* specs or *consuming* them? |

The cost reframing matters: a model that produces more verbose but more *predictive* specs may cost more per-spec but less per-delivered-feature. The round-trip is the expensive unit, not the token.

---

## 7. Discipline guards (carry into both commissions)

- **Recognition-validate-commit (OP § 3.4):** this note is the *recognition* of the reshaped eval; it commits nothing until Gate-1 PASSes and Matt approves the reshaped Phase 2. Empirical criterion to fire Phase 2 = Gate-1 PASS.
- **Math-first (Discipline #18):** the author spec is design-spec-as-math; the 1:1-assignment formulation is itself the math hotspot.
- **Substrate-led (OP § 3.1):** Phase 1 hand-curation is canonical anchor; the algorithm respects it.
- **Air-gap integrity:** the value of the result depends entirely on the implementer not having author back-channel. Launch fresh; spec is the only channel.
- **Self-contained-prompt discipline:** the implementer commission must be paste-ready and reference only committed artifacts (the spec + named canonical anchors), since it runs in a fresh session.

---

## 8. Sequencing

1. **[in flight]** Gate-1 — jack-ryan adversarial review of Phase 1 synthesis doc.
2. **[on Gate-1 PASS + Matt approval]** Author phase — Fable-5-gandalf writes the kit-to-star-sign forward spec (clean-room, math-first, 1:1-assignment trap NOT telegraphed in the commission — the commission says "spec the kit→star-sign assignment," it does NOT hand the author the trap; predicting the trap *is the test*).
3. Air-gap — commit spec as standalone artifact.
4. Implementer phase — Fable-5-rocket builds from spec alone; maintains gap-log.
5. Audit phase — gandalf Opus 4.8 audits; scores G0–G4; catches unreported G1.
6. Phase 3 fold decision (§ 5) — run hunter probe only if Phase 2 is ambiguous.
7. Eval memo (§ 6 reframed dimensions).

---

**End of design note.** The task is unchanged; the lens is sharper. We are measuring the *spec-as-channel*, and the 1:1-assignment trap gives us a single falsifiable fidelity probe at the center of it.
