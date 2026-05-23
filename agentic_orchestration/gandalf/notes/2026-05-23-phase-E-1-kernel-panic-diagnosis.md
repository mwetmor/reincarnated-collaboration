# Phase E-1 Pipeline — Kernel Panic Diagnosis

> **STATUS:** CURRENT — incident report. Authored 2026-05-23 in response to Matt reporting the host machine kernel-panicked TWICE on `phase_e1_pipeline.py --mode full`. Forensic evidence shows THREE kernel panics today, all caused by the same script. **DO NOT re-fire this pipeline in its current form until remediation lands.**

**Author:** gandalf (story-and-design steward; acting incident-investigator at Matt's direct request)
**For:** Matt + next-session knight-rider + legolas (will receive a re-scoped dispatch)
**Trigger:** Matt direct invocation — "this task has twice now caused a failure of my mac computer, forcing the mouse wheel to spin as a rainbow colored beachball and the computer to instantaneously surface a pink screen and then restart"

---

## 1. Bottom line

**Root cause: out-of-memory kernel panic on an 8 GB Mac mini (Apple M2).** The `phase_e1_pipeline.py` script, on the full-mode HDBSCAN step, allocates more memory than the host can compress + swap fast enough; macOS watchdogd loses its 90-second check-in and the kernel panics.

This happened **three times today**, all from the same script:

| Panic timestamp | Run-log marker before panic | Substrate input | Expanded matrix at panic |
|---|---|---|---|
| 03:11:11 | (no log; first fire) | 16,699 rows (pre-Step-6.6) | ≈22k × 4 (inferred) |
| 03:32:14 | "Expanded matrix for HDBSCAN fit: (22065, 4)" | 16,699 rows | 22,065 × 4 |
| 11:09:13 | "Expanded matrix for HDBSCAN fit: (71003, 12)" | 48,430 rows (post-Step-6.6) | 71,003 × 12 |

Source: `/Library/Logs/DiagnosticReports/panic-full-2026-05-23-{031111,033214,110913}.0002.panic`. The 11:09 panic string: `panic(cpu 2 caller …): watchdog timeout: no checkins from watchdogd in 90 seconds … Compressor Info: 100% of compressed pages limit (BAD) and 37% of segments limit (OK) with 15 swapfiles`. **Compressor saturated at 100%, 15 swapfiles active** — textbook macOS OOM-kernel-panic signature.

## 2. Which line crashed the machine

`scripts/phase_e1_pipeline.py` line 416:

```python
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=min_cluster_size,
    min_samples=5,
    cluster_selection_epsilon=0.05,
    cluster_selection_method='eom',
    metric='euclidean'
)
clusterer.fit(expanded)   # ← panics here
```

The `expanded` matrix is constructed by **row-duplication** to fake sample weights (lines 398–404). For the 11:05 run that means **71,003 rows × 12 dimensions of float64**. The matrix itself is ~6.8 MB — small. The OOM is **inside HDBSCAN's fit**, not in the matrix construction.

HDBSCAN's `algorithm='best'` (default) and `cluster_selection_epsilon=0.05` together trigger build-paths that allocate large intermediate arrays (mutual-reachability graph, condensed tree, possibly a generic-algorithm fallback). On an 8 GB Mac with ~3–4 GB free after the IDE + browser + Claude + Python interpreter, this exceeds physical RAM, the compressor saturates, the SSD is thrashed across 15 swapfiles, kernel_task hangs in I/O, watchdog timeout fires → pink screen → restart.

## 3. Why the bis-loop never caught this

Three discipline failures compounded:

### 3.1 Crash-triage handoff misdiagnosed the first panic

`skill_handoff_2026-05-23-phase-E-1-crash-triage.md` (authored 03:25 EDT, between panic #1 and panic #2) framed the 03:11 event as: *"Machine reset at ~03:07 EDT mid-execution of legolas Phase E-1 dispatch"* — passive voice, treating the reset as an exogenous event. The actual sequence was: **the script caused the panic**. The triage missed this because:

- The smoke artifacts (k=4, 1-of-4 stable axes) were the visible evidence; they were correctly framed as sample-frame artifacts; but **the question "why did the machine reset?" was never asked**, only "what was the state at crash-time?"
- The continuation dispatch then instructed legolas to **re-fire the same script in full mode** with no memory-footprint pre-check. That re-fire produced panic #2.

**Discipline citation:** Discipline #1 (math-before-code) and Discipline-observation 4.2 from the EOD handoff ("forensic hypothesis vs forensic conclusion") both apply. The crash-triage drew a confident conclusion ("smoke completed; full never started") without asking *why* the machine reset. The cheapest refuting test — checking `/Library/Logs/DiagnosticReports/` for panic logs — was unrun.

### 3.2 No memory-footprint sanity check at math-hotspot routing

This is a P2 axis-discovery + clustering math hotspot. Per Discipline #18, methodology selection at named math hotspots requires legolas Mode A consultation before specialist execution. The methodology note (`phase-E-1-math-note.md`, committed `d738523`) specified HDBSCAN with `algorithm='best'` and `cluster_selection_epsilon=0.05` and row-duplication-for-weights — none of which were stress-tested against the host's 8 GB RAM ceiling before fire.

**Design-spec-as-math gandalf accountability:** my Pattern-A-deep design-fit verdict this morning (`gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md`) signed off on the re-fire without asking the memory question either. I share this discipline failure with knight-rider and legolas. The math-hotspot review checklist needs a hardware-resource line item.

### 3.3 Empirical evidence framed as substrate problem, not host problem

The bis-loop's whole framing — "is the substrate broken or is the methodology broken?" — implicitly assumed the script CAN run to completion on this host. When the smoke output looked weird, the team chased substrate (Step 6.6 category-promotion sweep). When full mode "didn't complete," the team assumed it was a machine reset and re-fired. Nobody asked: *can this script complete on this host at all?* The empirical evidence available — three panic logs sitting in `/Library/Logs/DiagnosticReports/` — was never consulted.

## 4. What NOT to do next

- **DO NOT re-fire `phase_e1_pipeline.py --mode full` on this host in its current form.** A fourth panic will occur. Each panic risks data loss (uncommitted in-flight DB transactions, editor state, IDE caches, browser session) and SSD wear.
- **DO NOT** assume "maybe it'll work this time" — three identical panics in 8 hours is not stochastic. It's deterministic OOM at the HDBSCAN step.
- **DO NOT** push back on this diagnosis by appealing to the smoke run's success. Smoke uses N=100 and `min_cluster_size=5`, which produces a tiny expanded matrix that fits trivially. Smoke does not exercise the OOM path.

## 5. Remediation tier-list

| Tier | Approach | Cost | Confidence it resolves OOM |
|---|---|---|---|
| **Tier 1 (recommended)** | Replace HDBSCAN row-duplication with a **bounded-memory clustering primitive**: e.g., `MiniBatchKMeans` (sklearn, native `sample_weight` support, streaming) for k-discovery, OR `hdbscan.HDBSCAN` with `algorithm='boruvka_kdtree'` explicit + `core_dist_n_jobs=1` (disable joblib parallelism) on the **non-expanded** matrix using sklearn-style sample_weight if available, OR `hdbscan` fit on the original (48,430 × 12) matrix without row-expansion + use sample_weight via a wrapper | Half-day rework + math-note amendment | HIGH — the matrix becomes 4× smaller and parallelism overhead drops |
| **Tier 2** | **Subsample the input** to ≤20,000 rows for HDBSCAN fit; assign the rest by nearest-centroid (already implemented at line 434 `assign_noise_to_nearest`). Run the bootstrap PCA + HDBSCAN on the subsample. F2 weights inform subsampling probability. | Quarter-day; preserves HDBSCAN | HIGH for memory; MEDIUM for representativeness (Phase D F1-bin coverage needs verification) |
| **Tier 3** | **Run on a different machine** — a cloud VM with ≥32 GB RAM, or a borrowed dev box. Pipeline runs cleanly; results rsync back. | Setup cost (one-time); recurring per-fire cost | HIGH — the script as written probably wants a 32 GB+ host |
| **Tier 4** | **Increase macOS swap** + `sudo sysctl` tuning to make the compressor more lenient. **NOT recommended** — risks SSD wear, doesn't address the 90-second watchdog, may still panic. | Low effort; high risk | LOW |
| Reserve | Algorithmic alternatives: `Birch`, `OPTICS` with `max_eps`, agglomerative with connectivity matrix. Each has tradeoffs vs HDBSCAN's noise-handling. | Day+ rework + methodology re-validation | Worth considering only if Tier 1 doesn't suffice |
| Reject | Re-firing the current script unchanged. Will panic again. |

**Gandalf-lean: Tier 1.** It addresses the root cause (HDBSCAN memory profile on this host) rather than working around it, and it keeps the work running on Matt's primary machine. Subsampling (Tier 2) is a reasonable fallback if Tier 1's algorithm doesn't preserve the cluster structure we need for Phase E-2 labeling.

## 6. Recommended next-step sequence

1. **Stop and acknowledge the discipline failure.** Authoring a knight-rider note that the crash-triage handoff misdiagnosed panic #1 closes the audit trail. Discipline observations 4.1 + 4.2 from the EOD handoff get a third sibling: "consult `/Library/Logs/DiagnosticReports/` before treating a 'machine reset' as exogenous."
2. **Author a Phase E-1 re-architecture math note.** Legolas authors; gandalf + jack-ryan critique-pair gate. Specify: bounded-memory algorithm; memory budget ≤4 GB peak; smoke + full runs on this host (M2 8 GB) as acceptance criteria.
3. **Add a Discipline-candidate amendment:** at math-hotspot routing (Discipline #18), the methodology selection MUST include a host-hardware feasibility assessment — peak RAM estimate, expected wall-clock, fallback algorithm if budget exceeds. This is the empirical-evidence criterion that gates re-fire.
4. **Then re-fire** on the corrected substrate (which is still good — Step 6.6 work was not wasted).

## 7. What I am NOT doing in this note

- **Not** authoring the replacement pipeline (that's legolas, in coordination with elrond on substrate access).
- **Not** writing a decision-log entry (jack-ryan owns that; my role here is to surface the design + discipline failure).
- **Not** retroactively blaming the bis-loop's substrate work — Step 6.6 was sound; the methodology-vs-substrate framing was reasonable in isolation. The failure was at a higher level: nobody asked "can the host run this?"

## 8. Empirical-evidence criteria for re-engagement

Per Discipline + my OP § 3.4 recognition-validate-commit cycle:

- **Recognition (this note):** captured.
- **Validate before re-fire:** the next pipeline version must demonstrate, on this host, a clean full-mode run that produces all Phase E-1 deliverables without triggering memory pressure (verifiable via `memory_pressure` polling during run). A successful dry-run on a 25%-subsample is necessary but not sufficient.
- **Commit:** Phase E-1 acceptance fires only when the re-architected pipeline lands clean output + no panic logs + jack-ryan Gate-2 ratification.

---

**Files referenced**

- Pipeline: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/scripts/phase_e1_pipeline.py`
- Run logs: same dir, `full-run-log-2026-05-23.txt` + `full-run-log-2026-05-23-rerun.txt`
- Panic reports: `/Library/Logs/DiagnosticReports/panic-full-2026-05-23-{031111,033214,110913}.0002.panic`
- Crash-triage handoff: `agentic_orchestration/skill_handoff_2026-05-23-phase-E-1-crash-triage.md`
- EOD handoff: `agentic_orchestration/skill_handoff_2026-05-23-eod.md`
- My prior design-fit verdict (which also missed the memory question): `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md`

**Signed:** gandalf

---

## 9. Addendum — 4th panic empirical confirmation + ratification-discipline failure + framing-audit gap

> **Status:** Addendum appended 2026-05-23 (late session, post-Cycle-9.10 frame-revision authoring). Records the 4th panic that empirically refuted Option-A's memory projection, the Pattern-A-deep ratification-discipline failure that allowed the re-fire to be authorized, and the framing-audit gap surfaced by Matt's diagnostic question. Closes the audit trail at the design-coherence-steward layer.

### 9.1 The 4th panic — empirical refutation of Option-A's memory projection

`panic-full-2026-05-23-114345.0002.panic` at 11:43:45 EDT. Same watchdog-timeout signature (92 seconds) as panics 1-3. Caused by `HDBSCAN.fit` on un-expanded (48,430 × 12) — ~3m 30s into clustering. The Option-A addendum's projected peak (~2.7-4.7 GB with mandatory `resource.setrlimit(RLIMIT_AS, 6 GiB)` defensive ceiling) **was empirically refuted**: the ceiling silently failed at `setrlimit` (`current limit exceeds maximum limit` warning at 11:39:32 in the run-log), so the safety net never engaged, and the un-expanded matrix at d=12 still exceeded 8 GiB.

D1 + D2 completed cleanly (PCA + bootstrap-stability finished at 11:40:15; outputs preserved on disk). Only D3 clustering hit the wall. Substrate untouched; APFS journaled cleanly through the 4th panic as through the prior three.

### 9.2 Pattern-A-deep ratification-discipline failure (mine)

My ratification at 11:26 EDT (`gandalf/notes/2026-05-23-phase-E-1-option-A-design-side-ratification.md`) had **two prior pieces of substrate-voting evidence in hand** when I signed off:

1. **03:11 run smoke output** — k=4, 1-of-4 stable axes. Visible in the bis-design-fit-verdict context.
2. **11:05 RERUN partial output** — k=12, 3-of-12 stable axes. Landed before the 11:09 panic; visible in the crash-triage handoff.

Both pieces of evidence said the same thing: **the substrate is voting against k=12 clustering dimensionality.** I logged this as a "Phase E-1-bis partial-acceptance flag" and ratified re-fire at k=12 anyway.

The correct response under substrate-led discipline (`canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` Patterns 4-5-6 retirements) would have been: **halt, escalate framing-review, propose refit at k=3 (or k=stable-axes) before any HDBSCAN re-fire is authorized.** The substrate-led discipline I authored canonical docs to enforce, I failed to apply to my own Pattern-A-deep ratification.

This is **Pattern-A-deep ratification-discipline failure**, named per knight-rider's frame-revision note. The failure is not that I missed the bootstrap-stability finding — I read it. The failure is that I treated it as a flag-to-log rather than as **substrate voting that the experiment frame was wrong**, which under the discipline I myself authored should have triggered halt + framing-review + refit.

### 9.3 Framing-audit gap surfaced by Matt's diagnostic question

The deeper structural gap: the team had dispatch-time framing review (Gate 1) and output-time process review (Gate 2). It did NOT have **execution-time framing review when empirical signals contradict the framing.** The bootstrap-stability finding landed at 11:40:15 in the run-log. HDBSCAN.fit started at 11:40:15 (same second). No checkpoint existed between "axis discovery surfaced 3-of-12 stable" and "clustering fires at k=12."

Matt's data-scientist diagnostic discipline — *what's causing this constraint, do I really need this element, was the framing off?* — did the work the team's discipline architecture should have done automatically. The team has alertness (Discipline #11 empirical-inspection) without an execution-time trigger-protocol; the structural slot for "halt-and-reframe when empirical signals contradict load-bearing methodology assumptions" did not exist as anyone's named responsibility.

### 9.4 Corrective actions landed in Cycle 9.10 (knight-rider + jack-ryan)

- **Discipline #18 amendment** (ratification-ready per Gate-1 Finding 4 INFO): substrate-voting-is-binding. When bootstrap-stability or equivalent substrate-voting evidence contradicts methodology-assumed dimensionality, the methodology re-cuts at the substrate's voted dimensionality before downstream stages fire.
- **Discipline #19 candidate** (Gate-1 Finding 6 WARN, jack-ryan operationalization folded): forensic-conclusion-discipline. Forensic claims must name the cheapest refuting test per claim type — memory: `psutil` RSS check; methodology: next-tier-larger sample run; substrate: SQL count; cross-seam: schema diff. Conclusions without named refutation tests are forensic hypotheses, not conclusions.
- **Frame-revision dispatch** at `dispatches/2026-05-23-legolas-phase-E-1-frame-revision-stratified-subsample-k3.md`: stratified-subsample at k=3 path. Acceptance gate verbatim: **≥50 clusters AND mean per-lineage purity ≥ 0.70** (per Gate-1 BLOCK Finding 2 ratification).
- **Frame-revision anchor note** at `knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md` (resize narrative + acceptance tree + 4-panic forensic table).
- **Carries dormant** pending fire outcome: 9.10-D substrate expansion fires if frame-revision surfaces coverage bottleneck (clusters < 50 OR purity < 0.70); 9.10-F cloud fire stays cancelled unless 9.10-D exhausted AND production-scale validation needed; 9.10-G Phase E-1.5 sensitivity sweep queued for robustness validation.

### 9.5 Owed: gandalf OP amendment (framing-audit checklist in Pattern A-deep)

Pattern A-deep ratification protocol gains an explicit framing-audit section. Three questions matched to Matt's diagnostic discipline:

1. What load-bearing framing assumption does this work depend on?
2. What evidence currently in hand (or surfaceable in current scope) could refute that assumption?
3. If refutation evidence exists or is plausible, is the right move to refine the framing rather than execute the work as-framed?

Landing as a separate artifact at `agentic_orchestration/operating-procedures/gandalf.md` + the installed skill at `.claude/skills/reincarnated-gandalf-operating-procedure/`. Non-blocking for the legolas frame-revision fire; lands before the next Pattern A-deep ratification.

### 9.6 Empirical-evidence criteria for re-engagement (updates § 8)

- **Recognition:** captured (this addendum + knight-rider's frame-revision note + jack-ryan's Discipline #18/#19 observation entries).
- **Validate:** Cycle 9.10 frame-revision dispatch fires on stratified-subsample k=3 path; acceptance gates measured verbatim (≥50 clusters AND mean per-lineage purity ≥ 0.70); native-vs-nearest-assigned split documented per MIGRATION.md per ADR-004 + Discipline #8.
- **Commit:** Phase E-1 acceptance fires on jack-ryan Gate-2 ratification of frame-revision output. If acceptance gates miss, the decision tree routes to 9.10-D (substrate expansion via targeted rare-lineage crawls) or 9.10-G (sensitivity sweep), **NOT to bigger HDBSCAN.** Cloud fire stays cancelled unless 9.10-D itself exhausts.

### 9.7 What this addendum does NOT do

- Does not amend §§ 1-8 of this note (they stand as authored — the record of what I knew at 11:17 EDT remains accurate at that moment).
- Does not author the discipline-candidate texts themselves (jack-ryan owns the canonical writes at `engineering-disciplines.md`).
- Does not author the gandalf OP amendment (separate artifact, owed, landing soon).
- Does not retroactively rewrite the Option-A ratification at `2026-05-23-phase-E-1-option-A-design-side-ratification.md`. That ratification stands as the record of what I thought at 11:26 EDT — including the discipline failure. This addendum stands as the record of what I now know was wrong with that thinking. The audit trail is preserved by keeping both intact.

---

**Signed (addendum):** gandalf
**Closes:** the audit trail on the kernel-panic incident at the design-coherence-steward layer. Cycle 9.10 frame-revision dispatch is cleared from design-side; design-side review of legolas Gate-2 output will run the framing-audit checklist per § 9.5.
