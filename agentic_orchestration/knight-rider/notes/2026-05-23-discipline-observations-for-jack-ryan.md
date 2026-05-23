# Discipline observations queued for jack-ryan ratification — 2026-05-23

**Author:** knight-rider
**For:** jack-ryan (Tier-A process steward; engineering-disciplines ratification authority)
**Trigger:** Three macOS kernel panics caused by the legolas Phase E-1 pipeline on Matt's 8 GiB M2 host today (03:11, 03:32, 11:09). Forensic at `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-kernel-panic-triage.md`. Two discipline gaps emerged that warrant promotion to formal candidacy.

---

## Observation 1 — Memory-headroom check at math-before-code stage for compute-heavy dispatches

### Evidence

Knight-rider's RERUN dispatch (`2026-05-23-legolas-phase-E-1-RERUN-corrected-pool.md`) had a five-section Math-before-code block covering: F2 weight statistics, k-selection projection, bootstrap stability, bis-disposition criteria. It **did not require legolas to declare expected peak memory and validate against host RAM.** The pipeline crashed Matt's machine three times in 8 hours; cumulative risk of filesystem damage from kernel panics on the same boot session is non-zero.

This is a knight-rider-side discipline gap — the dispatch-authoring template (and Discipline #1 math-before-code) does not contain a host-resource-bounds check.

### Candidate Discipline framing

> **Discipline (proposed) — Pre-fire resource-bounds projection.** For compute-heavy dispatches (PCA / clustering / simulation / batch generation), the math-before-code section must include:
>
> 1. A **peak-memory projection** itemized per pipeline step (matrix shapes × dtype size + library working-set estimate)
> 2. A **host-headroom check** verifying projected peak < 62.5% of available RAM (i.e., leaves headroom for OS + Claude + observation tools)
> 3. If projection ≥ 62.5% of host RAM, **STOP and surface to knight-rider** before fire — alternatives include subsample-then-assign, bounded-memory algorithm substitution, or cloud-VM execution
>
> Smoke tests do not measure memory scaling at full-data shapes; explicit math is required.

### Severity

WARN candidate. This is a knight-rider-authoring discipline gap; jack-ryan should ratify and Discipline-list update should fold it into ENGINEERING-DISCIPLINES.md as a numbered amendment to Discipline #1 (math-before-code) or as a new numbered discipline.

### Suggested integration

Either amend Discipline #1 to add the resource-bounds clause, or promote as a separate Discipline #21 with cross-reference to #1 and #2. My preference: amend #1 — the resource-bounds check IS math-before-code, not a separate concern.

---

## Observation 2 — Smoke-test scope expansion to include resource-scaling rehearsal

### Evidence

The legolas pipeline's `--mode smoke` (N=100 rows, LIMIT applied at load) executed cleanly and produced the expected deliverables. At smoke scale, the F2-row-duplication step produced ~150 expanded rows; HDBSCAN.fit consumed single-digit MB. **Smoke passed; the failure mode at full scale (N=48,430 → 71,003 expanded → multi-GB HDBSCAN working set) was invisible to smoke.**

Smoke as currently scoped (per Discipline #2) verifies plumbing correctness — "does the code path execute end-to-end" — but does not exercise the resource-scaling behavior that determines whether full-mode is even viable on the host.

### Candidate Discipline framing

> **Discipline #2 amendment (proposed) — Smoke must include resource-scaling rehearsal for compute-heavy pipelines.**
>
> Compute-heavy pipeline smoke runs must capture per-step peak memory at smoke scale and produce an explicit projection of full-scale peak memory derived from the smoke measurements (with documented per-row or per-feature scaling assumption). If the projected full-scale peak exceeds 50% of host RAM, smoke does NOT pass — full-mode fire is gated pending refactor / subsample / cloud-VM provisioning.
>
> This is in addition to the existing plumbing-correctness purpose of smoke; both checks must pass.

### Severity

WARN candidate. Same authoring lane as Observation 1 — these are paired gaps in the smoke-test definition (Discipline #2).

### Suggested integration

Amend Discipline #2 to add the resource-scaling clause. Jack-ryan: please ratify and integrate at next discipline-list update opportunity.

---

---

## Observation 3 — Identical-point duplication for sample-weight emulation is a substrate-led-violation footgun on density-based algorithms

### Source

Gandalf design-side ratification of Option A (`agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md` § 4). Surfaced during the substrate-led-discipline analysis of the dual-stage F2 application.

### Evidence

Row-duplication to emulate sample weighting takes a row with weight w and creates w identical points at distance 0 from each other. **For density-based algorithms (HDBSCAN, DBSCAN, OPTICS, density-mean-shift), k-NN distance to duplicated points is 0, which artificially boosts apparent density** at the duplicated location even when the actual neighborhood is sparse. This manufactures cluster structure that isn't substrate-led — it's pre-imposed by the duplication pattern.

This isn't a bug specific to legolas's Phase E-1 implementation; it's a category-level methodological hazard that arises whenever a library lacks native `sample_weight` and the workaround chosen is row duplication.

### Candidate Discipline framing

> **Discipline (proposed) — Density-based algorithms must use native sample_weight or weighted-distance variants; NEVER emulate via row duplication.** Density-based clustering (HDBSCAN, DBSCAN, OPTICS, density-mean-shift) and k-NN-based methods compute density from inter-point distances. Row duplication of weighted samples produces identical-point pairs at distance 0, which fabricates density unrelated to substrate structure. Future weighted-clustering dispatches must (a) verify the chosen algorithm exposes a native `sample_weight` parameter, OR (b) use a weighted-distance metric variant, OR (c) propose a different methodology entirely. Row duplication as a sample-weight workaround is FORBIDDEN for any algorithm that consumes pairwise distances.

### Severity

WARN candidate. Catches a class of substrate-led-discipline violations before they appear in future dispatches. Particularly relevant for any future P3-multimodal-clustering work or any Phase F+ analytical work that touches density-based methods.

### Suggested integration

Promote as a new numbered Discipline. Cross-reference with Discipline #18 (gandalf design-spec-as-math) and the substrate-led-discipline framing from `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`.

---

## Observation 4 — Math-notes must ground implementation claims in code line references

### Source

Knight-rider's GMM scope check during Option-A dispatch authoring (2026-05-23 ~12:00 EDT). See `dispatches/2026-05-23-legolas-phase-E-1-OPTION-A-single-stage-F2.md` § "GMM scope check — Option-A-compliant in implementation already (RESOLVED)".

### Evidence

The legolas Phase E-1 math note at line 725 stated: "F2 weights applied as sqrt(w_i) row-multiplication on TF-IDF before SVD; as sample_weight on StandardScaler mean/std; **as integer-duplication for HDBSCAN and GMM fit**."

**Actual implementation:**
- HDBSCAN: integer-duplication confirmed (script lines 388-407). Math-note claim correct.
- GMM: NO integer-duplication. Script line 510 calls `gmm.fit(projections_k)` directly on un-expanded projections.

The math note overstated GMM behavior. The dispatch authoring caught this only because gandalf's ratification flagged GMM as also-affected — a verbatim code read would have caught it earlier. **Math notes that overstate implementation create downstream doubt and risk dispatches authored on bad assumptions.**

### Candidate Discipline framing

> **Discipline (proposed) — Math-note implementation claims must cite code line references.** Any math-note claim of the form "X applied as Y at stage Z" must include a parenthetical code reference: `(script lines NN-MM)` or `(file.py:NNN)`. Reviewers (knight-rider at dispatch authoring; jack-ryan at Gate-1; gandalf at design-side review) verify the cited code matches the claim before accepting the math note as load-bearing for downstream dispatches. Unverified math-note claims are surfaced as findings, not as accepted facts.

### Severity

INFO candidate. Low-severity discipline-hygiene improvement; not a violation that broke anything in this cycle (the GMM-already-compliant finding was a strict improvement). Worth promoting because the pattern will recur on every analytical pipeline that has a separate math note from the implementation.

### Suggested integration

Either amend Discipline #1 (math-before-code) to add a code-citation clause, or promote as a separate dedicated Discipline. Jack-ryan's call.

---

## Observation 5 — Substrate-voting-is-binding (gandalf-flagged; Discipline #18 amendment candidate)

### Source

Gandalf 2026-05-23 ~12:00 EDT (during frame-revision resize after 4th kernel panic). Owned as a Pattern A-deep ratification-discipline failure on gandalf's part. Full narrative + verbatim gandalf statement in `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md` § 3.

### Evidence

The Phase E-1 fires this cycle produced two substrate-voting signals that were treated as **flags** rather than **gates**:

| Fire | Signal | Treatment | Outcome |
|---|---|---|---|
| Smoke 03:11 EDT | k=4 retained, 1-of-4 stable axes | Framed as sample-frame artifact; ratified re-fire at k=12 | Did not surface the methodology-frame question |
| RERUN partial 11:05 EDT | k=12 retained heuristically; 3-of-12 stable axes | Logged as Phase E-1-bis flag; ratified continuation to clustering at k=12 | Compute-remediation focus obscured the substrate-vote |
| OPTION-A 11:40 EDT | Same as above (bootstrap unchanged by Option A) | Same treatment | Host kernel-panicked at HDBSCAN.fit (4th panic) |
| Matt + gandalf 12:00 EDT resize | k_stable = 3 acknowledged as the substrate's verdict | Frame-revision cuts at k_stable | Phase E-1 frame realigned to substrate vote |

Gandalf verbatim: "The bootstrap-stability check IS the substrate voting. It voted k=3. I logged that vote as a flag and ratified a re-fire at k=12 anyway because compute-remediation was the visible problem."

### Candidate Discipline framing

> **Discipline #18 amendment (proposed) — Substrate-voting-is-binding at axis discovery.**
>
> When a substrate-driven measurement produces a value substantially below the methodology's chosen parameter, the chosen parameter must be cut to the substrate-driven value **before the next stage fires.** Substrate measurement is a **gate**, not a **flag.** A logged flag with continued execution at the original parameter is a substrate-led discipline violation regardless of compute-remediation framing.
>
> Specific application points:
> - Bootstrap-stability at axis discovery: if `k_stable < k_chosen` by factor 2+ (e.g., k_stable=3, k_chosen=12), cut to k_stable before clustering fires
> - Scree-kink at PCA: if kink position dominates the heuristic-chosen k by a wide margin, the heuristic loses
> - Silhouette at clustering: if score peaks at a smaller cluster count than the configured min, re-fire at the smaller count
>
> The compute-remediation question ("can we make k_chosen run?") is orthogonal to the methodology question ("does the substrate support k_chosen?"). When the answer to the methodology question is no, the compute-remediation question is moot.

### Severity

**WARN candidate, leaning BLOCK.** This discipline gap (treated by both gandalf at design-side ratification AND knight-rider at dispatch authoring) cost 4 kernel panics and a full cycle of compute remediation that was investigating the wrong problem. Promoting to BLOCK enforcement at Gate-1 would catch the next iteration of this pattern at the right time.

### Suggested integration

Amend Discipline #18 (gandalf design-spec-as-math) with the substrate-voting-is-binding clause; or promote as a separate Discipline cross-referenced with #18 and #1. Gandalf has committed to authoring an addendum to `gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` recording this failure. Jack-ryan's ratification + disciplines-doc integration follows.

---

## Observation 6 — Confident framing on partial evidence at the diagnosis layer (Discipline #19 candidate; jack-ryan Gate-1 Finding 6)

### Source

Frame-revision note § 9 (`agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md`), confirmed and operationalization-extended by jack-ryan Gate-1 Pattern-A-light review 2026-05-23 ~12:30 EDT on the frame-revision dispatch. Jack-ryan verdict: structurally distinct from Observations 1-4; warrants its own candidate.

### Evidence (three datapoints today)

| Diagnosis call | When | Confident framing | Cheapest refuting test (unrun at framing time) | Outcome |
|---|---|---|---|---|
| Smoke-frame artifact (knight-rider crash-triage handoff 03:25 EDT) | post-1st panic | "k=4, 1-of-4 stable IS sample-frame artifact of N=100 monoculture" | Run full-mode pipeline on real pool (~42 sec) | Full-mode partial-fire later refuted the framing; substrate signal was real |
| Option-A memory comfort (knight-rider kernel-panic-triage 11:15 EDT) | post-3rd panic | "Option A should comfortably fit in 8 GB" | Profile HDBSCAN at n=48K, d=12 via psutil RSS-check or equivalent before authoring the dispatch | 4th kernel panic at 11:43 EDT refuted the framing |
| (No third instance yet but the pattern is now established for ratification) | | | | |

Both calls were confident framings on partial evidence. Both cost a fire cycle to refute. Both could have been hedged at framing time with available cheaper tests.

### Candidate Discipline framing (jack-ryan operationalization clause folded)

> **Discipline #19 (proposed) — Forensic-conclusion discipline: assertions of cause require the cheapest refuting test to have been run.**
>
> When triaging a crash, failure, or unexpected result, an authored note (forensic, triage, diagnosis) that asserts a causal claim ("X caused the failure" / "X is the binding constraint" / "X is an artifact of Y") must document whether the **cheapest refuting test** for X has been run, and what its result was. If the cheapest refuting test is unrun, the claim must be framed as a **hypothesis** ("X may be the cause; the cheapest refuting test is Y") rather than a **conclusion** ("X is the cause").
>
> **Operationalization (jack-ryan Gate-1 fold-in):** "cheapest refuting test" must be named explicitly for the claim type:
>
> - **Memory hypotheses:** the cheapest refuting test is a peak-RSS measurement (via `psutil`, `mprof`, or equivalent) at the proposed scale before firing the dispatch
> - **Methodology hypotheses (e.g., "k=4 is sample-frame artifact"):** the cheapest refuting test is the next-tier-larger sample run with the same methodology (smoke → full; or subset → full-pool)
> - **Substrate hypotheses ("the pool is too small / wrong distribution"):** the cheapest refuting test is a simple SQL count / distribution query against the substrate
> - **Cross-seam contract hypotheses ("the consumer / producer is reading the wrong schema"):** the cheapest refuting test is a verbatim schema diff between producer and consumer ends
>
> Future authoring template: any forensic note must include a § "Cheapest refuting test status" subsection stating whether the test was run, with what result, before the causal claim is accepted as load-bearing for downstream dispatches.

### Severity

**WARN candidate, leaning BLOCK for Gate-1 enforcement.** The two-datapoint cost in this cycle is already non-trivial (one wasted dispatch + one fired-then-kernel-panicked dispatch). Promoting to Gate-1 BLOCK enforcement (any dispatch whose math-before-code or forensic anchor contains an un-tested causal claim is blocked pending the cheapest refuting test) would catch the next iteration of the pattern at framing time.

### Suggested integration

Promote as new Discipline #19. Cross-reference with Discipline #1 (math-before-code; the cheapest refuting test is part of the math-before-code stage when it is a methodology hypothesis), Discipline #2 (smoke test; the cheapest refuting test is what smoke is designed to do at the plumbing level), and Discipline #18 (substrate-voting-is-binding; substrate-voting IS one of the cheapest refuting tests when applicable). The Discipline #18 + #19 pair forms a coherent "trust the substrate's empirical signal, document the test, do not over-extend the methodology" framework.

---

## Pattern observation (not yet ratification-ready; surfaced for awareness)

Both gaps emerged from the same root: **the engineering disciplines do not adequately handle the host-resource-bounds dimension for numerical/computational dispatches.** The disciplines were authored against the engine's simulation cadence (Discipline #1 math-before-code originated in B14.5 balance-loop work where memory was never close to host limit). The substrate-side analytical pipelines (Phase D / Phase E) operate on data scales where memory IS the binding constraint — and the disciplines have not been updated to reflect that.

Worth a one-paragraph addition to the disciplines preamble: *"As of 2026-05-23, the engineering-disciplines list applies across engine-side and substrate-side work. Substrate-side work brings host-resource-bounds (RAM, disk, swap) into the math-before-code and smoke scopes; engine-side work historically operated below host limits and so these checks were implicit. Make them explicit now."*

This preamble note is jack-ryan's call; surfaced here for awareness.

---

**Signed:** knight-rider, 2026-05-23 post-kernel-panic triage. Queued for jack-ryan ratification at next Pattern-B critique-pair opportunity. Not blocking the OPTION-A re-fire dispatch — that dispatch already incorporates the spirit of Observation 1 via the pre-fire memory-projection requirement.
