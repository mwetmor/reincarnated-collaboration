# Phase E-1 Kernel-Panic Triage — 2026-05-23

**Author:** knight-rider
**Trigger:** Matt reported the legolas Phase E-1 pipeline crashed the Mac twice today (beachball → pink screen → instant restart). Asked for diagnosis.
**Verdict:** **Confirmed kernel panic from memory exhaustion. Deterministic failure on this hardware for this workload. DO NOT re-fire the RERUN dispatch as-is.**

---

## 1. Evidence

### Hardware
- **Mac:** M2 (Mac14,3), macOS 15.6.1
- **RAM: 8 GiB** (`hw.memsize = 8589934592`)
- **8 cores**

### Crash signature (all three panics today; identical mechanism)

| Panic file | Time | Compressor | Swapfiles | Watchdog |
|---|---|---|---|---|
| `panic-full-2026-05-23-031111` | 03:11:11 | 100% pages limit (BAD) | 10 | "no checkins from watchdogd in 91s" |
| `panic-full-2026-05-23-033214` | 03:32:14 | 100% pages limit (BAD) | 12 | "no checkins from watchdogd in 92s" |
| `panic-full-2026-05-23-110913` | 11:09:13 | 100% pages limit (BAD) | **15** | "no checkins from watchdogd in 90s" |

All three say `Compressor Info: 100% of compressed pages limit (BAD)`. This is macOS literally reporting: "memory compressor is saturated — every page that can be compressed has been compressed, and we still don't have enough." Default macOS swap starts with 2 swapfiles; 15 swapfiles means the kernel was opening new swap volumes at an unsustainable rate. The kernel was thrashing disk so hard that watchdogd (the high-priority daemon that proves the system is alive) couldn't get scheduled for 90+ seconds → the kernel panics for safety.

**This is not a software bug in the panic sense — it is memory pressure that exceeds the OS's ability to cope, and the OS protectively kills the machine rather than risk a hung state.**

### Pipeline run log — where it hung each time

The 11:09 panic followed this run-log sequence (the RE-FIRE attempt):

```
[11:05:02] === Phase E-1 Pipeline starting (mode=full) ===
[11:05:03] Loaded 48430 rows from v_category_sample
... [Deliverables 1 & 2 complete in ~42 seconds — TF-IDF, PCA, bootstrap]
[11:05:44] === DELIVERABLE 3: Clustering ===
[11:05:44] Running HDBSCAN (min_cluster_size=30)...
[11:05:44] Expanded matrix for HDBSCAN fit: (71003, 12)
<3 minutes 29 seconds of silence; panic at 11:09:13>
```

The 03:29 first-fire log shows the identical hang point:
```
[03:29:23] === DELIVERABLE 3: Clustering ===
[03:29:23] Running HDBSCAN (min_cluster_size=30)...
[03:29:23] Expanded matrix for HDBSCAN fit: (22065, 4)
<panic at 03:32:14, ~2 min 51 sec later>
```

**Both crashes hung inside `hdbscan.HDBSCAN.fit()` on the F2-row-duplicated expanded matrix.**

## 2. Root cause

In `scripts/phase_e1_pipeline.py`, `run_hdbscan()` (lines 388-431) applies F2 inverse-frequency weighting to HDBSCAN by **physically duplicating rows by their integer weight**:

```python
int_weights = np.round(weights).astype(int)
int_weights = np.clip(int_weights, 1, 20)  # cap duplication at 20x
expanded = []
for i, (row, w) in enumerate(zip(projections_k, int_weights)):
    for _ in range(w):
        expanded.append(row)
expanded = np.array(expanded)
clusterer = hdbscan.HDBSCAN(min_cluster_size=30, min_samples=5, ...)
clusterer.fit(expanded)
```

- Original (16,699 rows) → 22,065 rows after duplication (cap 20×). Bootstrapped resamples + PCA matrix + TF-IDF matrix all still resident → HDBSCAN.fit(22,065 × 4) blew past 8 GB on first try.
- Corrected (48,430 rows) → 71,003 rows after duplication. Same outcome, faster.

The expanded matrix itself is small (71,003 × 12 × 8 bytes = ~6.8 MB). The problem is **HDBSCAN's internal mutual-reachability-distance, MST, and condensed-tree construction**. For n ≈ 71,003 in 12-dim Euclidean, HDBSCAN's peak working memory runs into several GB even with the KD-tree path, and that's on top of the Python process's already-large residency (TF-IDF sparse matrix, LSA basis, PCA loadings, bootstrap intermediate axes, weights array).

**The pipeline is not pathologically broken — it would run fine on a 32-GB machine. It is fundamentally incompatible with 8 GB RAM for the current pool size.**

## 3. Why the smoke test didn't catch this

Smoke = N=100 rows → expanded ~150 rows → HDBSCAN peak memory in single-digit MB. The smoke test verified **plumbing correctness**, not **resource scaling**. This is a Discipline #2 (smoke-test discipline) blind spot: smoke tested "does the code path execute end-to-end" but did not measure peak-memory scaling against host RAM.

## 4. Substrate integrity check

Post-panic verification (2026-05-23 11:13):

| Check | Status |
|---|---|
| `v_category_sample` row count | **48,430** ✓ (unchanged from elrond's Phase-D-bis post-correction state) |
| `clusters` table | empty (expected — never populated; full-mode crashed before DB writes) |
| `cluster_membership` table | empty (expected) |
| On-disk artifacts under `phase-E-pattern-6-2026-05-23/` | Intact; `phase-E-1-axis-discovery.md` etc. were partially written by the crashed run but the substrate DB is unaffected. |
| File system corruption | None observed. macOS panics from this mechanism flush before halting; APFS is journal-protected. |

**The corrected substrate is safe. No re-do of elrond's Phase-D-bis work is needed.** The lethal step is exclusively in legolas's Deliverable 3 (HDBSCAN row-duplication clustering).

## 5. Remediation options

### Option A — Drop the F2 row-duplication; cluster on un-expanded projections **[RECOMMENDED]**

The F2 weighting is already applied at the **PCA stage** via sqrt-weighted row scaling (lines 209-225, mathematically correct weighted PCA). The PCA projections already encode the rare-lineage-amplification effect in the projected coordinates. Re-applying F2 weighting at the **clustering stage** via row duplication is over-engineering and is what blows the memory budget.

Edit `run_hdbscan` to call `clusterer.fit(projections_k)` directly on the 48,430 × 12 matrix (no expansion). Memory drops by ~1.5× from the duplication elimination, AND the underlying matrix is half-again smaller. Should comfortably fit in 8 GB.

Cost: ~30 minutes of legolas time (one method change + a math note addendum justifying that PCA-stage F2 weighting suffices). Methodology-clean: no F2 weights need refitting. Acceptance criteria unchanged. F5 PCA-primary lock holds.

**Caveat:** with cap=20× duplication, the maximum F2 amplification factor applied at clustering was 20. Without duplication, the only F2 effect at clustering is via the PCA projections — implicit, not explicit. Whether this is methodologically OK depends on whether gandalf's Pattern-6 design framework intended F2 amplification at **both** PCA and clustering stages, or only at PCA.

Recommend: legolas writes a one-page math note re-justifying single-stage F2 application before fire, with one-line gandalf consult if needed.

### Option B — Subsample-then-assign

Random sample (F2-weighted, without replacement) ~10,000 rows → HDBSCAN → produce labels for the sample. For remaining 38,430 rows: assign to nearest-cluster centroid in projection space.

Cost: ~1 hour legolas time. Methodology-rigorous: justifiable as "tractability adaptation under host constraint." Cluster boundaries identical to Option A in expectation; slightly more noise points possible.

Worth doing if Option A turns out to have methodology pushback.

### Option C — Run elsewhere

Provision a cloud VM (AWS EC2 c7g.xlarge with 8 GB, no help; c7g.2xlarge with 16 GB ~$0.30/hr) or use a 32+ GB Mac. One-shot fire, copy artifacts back, then DB write locally (DB writes themselves are tiny).

Cost: ~$1 in cloud spend; ~1-2 hours setup. Methodology UNCHANGED. Cleanest path if Matt wants to preserve the current pipeline bytes-for-bytes.

Caveat: ADR-006 (read-only external state by default) — running on a cloud VM is not a violation in spirit (local DB stays local; only compute moves) but should be acknowledged.

### Option D — Cap duplication at 1× (no duplication) without changing F2 design intent

Same effect as Option A but framed as "operational constraint" rather than "methodology re-evaluation." Set `int_weights = np.clip(int_weights, 1, 1)` at line 396, document the cap as a memory-constraint adaptation.

Equivalent outcome to Option A. Less methodologically honest about what changed. I do not recommend; either commit to single-stage F2 (Option A) or commit to cloud (Option C).

### My recommendation

**Option A.** Cleanest math; cheapest in time; runs on the existing 8 GB Mac; methodology defensible. Pre-fire one-line gandalf consult to confirm single-stage F2 application is design-intent-compatible.

## 6. Discipline observations (durable record)

Two findings warrant promotion to formal engineering-disciplines candidacy via jack-ryan:

### 6.1 Memory-headroom check at math-before-code stage for compute-heavy dispatches

Knight-rider's RERUN dispatch's math-before-code section (§ 1–5) covered F2 weight statistics, k-selection projection, bootstrap stability, bis-disposition criteria — but **did not require legolas to declare expected peak memory and validate against host RAM**. Three kernel panics is the cost of that omission.

Candidate Discipline: *"For compute-heavy dispatches (PCA, clustering, simulation), the math-before-code section must include a peak-memory projection and a host-headroom check. Smoke tests do not measure memory scaling; explicit math is required."*

### 6.2 Smoke-test scope expansion to include resource scaling

Discipline #2 currently treats smoke as "does the pipeline plumbing work end-to-end on a tiny dataset." This was not sufficient to surface the HDBSCAN row-duplication memory-explosion failure. A smoke at N=100 with cap=20× duplication produces ~150 rows — completely silent on the failure mode that triggers at N=48,430 → 71,003 rows.

Candidate Discipline amendment: *"Smoke tests for compute-heavy pipelines must include a resource-scaling rehearsal — at minimum, a peak-memory estimate at full-scale derived from the smoke run's per-row memory cost. If the projection exceeds 50% of host RAM, do not fire; refactor first."*

## 7. Recommended next action

1. **SUPERSEDE the RERUN dispatch.** Author a thin Option-A revision dispatch that:
   - Acknowledges the kernel-panic forensic
   - Instructs legolas to edit `run_hdbscan` per Option A (drop row duplication; cluster on `projections_k` directly)
   - Requires a one-page math-note addendum justifying single-stage F2 application
   - Requires a pre-fire memory projection: estimate peak Python residency from the Deliverable 1 & 2 measurements (TF-IDF matrix size + PCA basis size + bootstrap intermediate + clustering working set) and verify projected peak < 5 GiB before fire
   - Same acceptance criteria; same tag
2. **Optional pre-fire gandalf one-line consult** to confirm single-stage F2 application is compatible with Pattern-6 design intent (cleaning-policy § 5 didn't specify which stage gets the weighting).
3. **Halt further attempts on the current dispatch.** Do not let legolas re-fire RERUN as-is on this machine. The next crash is guaranteed; cumulative risk of filesystem damage compounds.

---

**Signed:** knight-rider, post-triage 2026-05-23 ~11:15 EDT
