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

## Pattern observation (not yet ratification-ready; surfaced for awareness)

Both gaps emerged from the same root: **the engineering disciplines do not adequately handle the host-resource-bounds dimension for numerical/computational dispatches.** The disciplines were authored against the engine's simulation cadence (Discipline #1 math-before-code originated in B14.5 balance-loop work where memory was never close to host limit). The substrate-side analytical pipelines (Phase D / Phase E) operate on data scales where memory IS the binding constraint — and the disciplines have not been updated to reflect that.

Worth a one-paragraph addition to the disciplines preamble: *"As of 2026-05-23, the engineering-disciplines list applies across engine-side and substrate-side work. Substrate-side work brings host-resource-bounds (RAM, disk, swap) into the math-before-code and smoke scopes; engine-side work historically operated below host limits and so these checks were implicit. Make them explicit now."*

This preamble note is jack-ryan's call; surfaced here for awareness.

---

**Signed:** knight-rider, 2026-05-23 post-kernel-panic triage. Queued for jack-ryan ratification at next Pattern-B critique-pair opportunity. Not blocking the OPTION-A re-fire dispatch — that dispatch already incorporates the spirit of Observation 1 via the pre-fire memory-projection requirement.
