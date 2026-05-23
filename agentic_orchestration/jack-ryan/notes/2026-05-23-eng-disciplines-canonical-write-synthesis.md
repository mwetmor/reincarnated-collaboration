# Synthesis note — Engineering-disciplines canonical write batch 2026-05-23

**Author:** jack-ryan
**Date:** 2026-05-23
**Scope:** Dispositions + rationale for gandalf 6-candidate + KR 7-observation consolidated batch
**Companion:** Engine commit `1fae3fa`; tag `jack-ryan/eng-disciplines-canonical-write-2026-05-23`

---

## 1. Numbering decisions

Gandalf proposed #20/#21 for no-sleep/timezone-agnosticism. KR Obs 3 (density-algorithm row-duplication prohibition) was assigned #20 instead. Rationale: the density-algorithm discipline is a substrate-side methodological discipline logically contiguous with the #18/#19 cluster (substrate-led methodology + forensic-conclusion discipline). Placing it at #20 keeps methodological disciplines together. No-sleep and timezone-agnosticism are behavioral-protocol disciplines and logically form a pair — they land at #21/#22 adjacent to each other as intended. Result:

| # | Discipline |
|---|---|
| #20 | Density-based algorithm row-duplication prohibition (KR Obs 3) |
| #21 | No sleep recommendations — CRITICAL (Gandalf #1) |
| #22 | Timezone-agnosticism — CRITICAL (Gandalf #2) |
| #23 | Framing-audit checklist (Gandalf #3) |
| #24 | Single-parameter sweep isolation (KR Obs 7) |
| #25 | Semantic-layer rep-audit (Gandalf #5, distinct from KR Obs 5) |

---

## 2. Overlap dispositions

### Gandalf #5 (semantic-layer rep-audit) + KR Obs 5 (substrate-voting-is-binding)

**Disposition: DISTINCT disciplines at different layers. NOT composed as one.**

KR Obs 5 addresses the **geometry layer**: when bootstrap-stability or another substrate-driven measurement votes a value substantially below the methodology's chosen parameter, the methodology parameter must be cut. The substrate vote is a gate, not a flag. This landed as #18.1 (amendment to Discipline #18, methodology-before-execution).

Gandalf #5 addresses the **semantic layer**: even after geometry-layer clustering succeeds (high purity score; stable k), the semantic interpretation assigned to the cluster's identity may not match the cluster's actual representative content. The Mode-A/B/C/D vocabulary taxonomy (Cluster 87 "S. American Indigenous Contemporary Shotgun" at 94.4% purity having top reps = Modern Argentine military firearms) shows that geometry purity does not guarantee semantic fidelity. This landed as #25 (new discipline).

These are different failure modes. Composing them would muddle the operational guidance: #18.1 tells you when to cut k before firing; #25 tells you to pull reps before inheriting semantic meaning. Both are needed; neither replaces the other.

### Gandalf #6 (cheapest-refuting-test-per-claim-type) + KR Obs 6 (forensic-conclusion discipline operationalization)

**Disposition: COMPOSED as #19.1 amendment to Discipline #19.**

Both proposals target the same gap in Discipline #19: the per-claim-type operationalization of "name the cheapest refuting test." KR Obs 6 supplies the operationalization directive and the two triggering instances (smoke-frame artifact framing; Option-A memory comfort framing). Gandalf #6 supplies the per-claim-type table (memory → psutil; methodology → next-tier sample; substrate → SQL count; cross-seam → schema diff; framing assumption → Pattern-A query; cluster semantic → rep-audit). These compose cleanly as #19.1 with the table as the authoritative lookup.

---

## 3. Amendment vs new-discipline decisions

### KR Obs 1 (memory-bounds projection) → #1.1 amendment to Discipline #1

KR's own preference; accepted. Memory-bounds projection IS math-before-code applied to compute-heavy dispatches. Amending #1 rather than creating a new discipline avoids fragmentation of the math-before-code conceptual cluster.

### KR Obs 2 (smoke resource-scaling rehearsal) → #2.1 amendment to Discipline #2

Same logic. Resource-scaling rehearsal IS smoke-test scope extended to compute-heavy pipelines. Amending #2.

### KR Obs 4 (math-note code-citation) → #1.2 amendment to Discipline #1

INFO severity candidate. Math-note code-citation is a within-discipline hygiene extension of math-before-code — the math note IS the discipline artifact; requiring code citations within it keeps it within the same discipline. Amending #1.2 rather than creating a new discipline at this severity.

### Gandalf #4 (methodology-consultation timing at extension hotspots) → #18.2 amendment to Discipline #18

Clearly an amendment — it refines a specific application rule within the methodology-before-execution discipline without changing its principle. Amending #18.2.

### Gandalf #5 (semantic-layer rep-audit) → new Discipline #25

New discipline. The semantic-layer failure mode is structurally distinct from methodology-before-execution (#18) and from substrate-voting-is-binding (#18.1). It addresses a different agent (any agent consuming cluster output as cultural-tradition substrate) at a different point in the workflow (semantic-inheritance decision, not axis discovery or methodology lock). New discipline required.

### KR Obs 3 (density-algorithm row-duplication) → new Discipline #20

New discipline. Row-duplication prohibition is not an extension of any existing discipline — it is a categorical algorithm-class constraint that applies regardless of whether math-before-code or methodology-before-execution gates are passed. New discipline.

### KR Obs 7 (single-parameter sweep isolation) → new Discipline #24

New discipline. Sweep isolation is an experimental-design discipline not captured under #1 (math-before-code), #18 (methodology-before-execution), or #19 (forensic-conclusion). It addresses the confound-by-design failure mode at the parameter-sweep planning layer. New discipline.

---

## 4. Rejected / deferred candidates

None. All 13 inputs (6 gandalf + 7 KR) were integrated, either as new disciplines or amendments. KR Obs 4 was INFO severity but included as #1.2 because the triggering instance was recent and the pattern will recur on every pipeline that maintains a separate math note from the implementation.

---

## 5. Future-batch carries

No new discipline candidates surfaced during this write that were out of scope. The existing Discipline #19 "Discipline #20+ candidates" note (JSON-summary-artifact; log-verbosity bounding; script wall-time estimates) remains queued for Matt's review — unchanged from prior text.

---

**Signed:** jack-ryan, 2026-05-23. Canonical write complete. Per-agent OP propagation cleared to fire.
