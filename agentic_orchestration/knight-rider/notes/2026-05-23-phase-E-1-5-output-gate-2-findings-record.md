# Phase E-1.5 Output Gate-2 Findings Record — 2026-05-23

**Author:** knight-rider
**For:** durable record of jack-ryan DEV-MODE Gate-2 review on legolas Phase E-1.5 sensitivity sweep (commit `ef9707c`, tag `legolas/phase-E-1-5-sensitivity-sweep-2026-05-23` local)
**Reviewer:** jack-ryan (Pattern-A-light, ~30 min)
**Verdict:** **Gate-2 ratification CONDITIONAL PASS** — Phase E-1.5 acceptance recorded; 2 named conditions for knight-rider to fold (Discipline #20 candidate; cluster-116 relabel surface to gandalf); 9.11-D dispatch NOT blocked

---

## 1. Acceptance summary (legolas reported; jack-ryan verified)

| mcs | Clusters | Purity | F6 | Noise | RSS |
|---|---|---|---|---|---|
| 10 | 125 | 0.9444 | 0 | 427 | 1.12 GiB |
| 15 | 103 | 0.9412 | 0 | 550 | 1.12 GiB |
| 20 | 85 | 0.9287 | 0 | 559 | 1.11 GiB |
| 30 | 65 | 0.9177 | 0 | 922 | 1.14 GiB |

All 4 at ACCEPTANCE tier. DB writes OFF verified by jack-ryan live SQLite query (`clusters=125`, `cluster_membership=48,430`, `id=3 → cluster_id=116` Phase-E-2-DB state intact).

## 2. Findings (verbatim from jack-ryan return)

### Finding 1 — Math-before-code compliance (Discipline #1) [INFO]

Math-note mtime 14:03; pipeline code mtime 14:05. Two-minute delta; math-note on disk before code changes. Single-commit delivery means intra-session order not verifiable beyond mtimes, but artifact + pipeline in same commit (ef9707c) + math-note header explicitly asserts "PRE-FIRE." Discipline #1 compliant on available evidence.

### Finding 2 — DB-write-OFF compliance [INFO — independently verified]

Live SQLite query confirmed: `clusters=125`, `cluster_membership=48,430`, `id=3 → cluster_id=116` "European Uncurated-Period Spear Family" — exactly the Phase E-2-DB canonical state. No clobber.

### Finding 3 — Cheapest-refuting-test application (Discipline #19) [INFO]

Every hypothesis in math-note §4 has a named cheapest test and a documented result in comparison report §7 hypothesis-verdict table. The one REFUTED hypothesis (subsample composition stability) has its refuting test documented (compare subsample_per_lineage dict across 4 runs; arctic: 27 → 56 rows). Full compliance.

### Finding 4 — Acceptance-gate compliance [INFO]

All ten dispatch acceptance-gate checkboxes verified in completion summary. Per-variant artifacts present on disk. Every gate passes.

### Finding 5 — Comparison report format compliance (dispatch §E) [INFO]

All required elements present: per-variant summary table; cross-variant trends; hypothesis verdicts; recommendation framed as data not commitment (explicitly "gandalf decides"); form-bundling vs prefix-bundling verdict; cross-cutting observations for follow-on dispatches.

### Finding 6 — Subsample-composition-REFUTED finding [WARN]

The finding is ratification-ready as stated. Floor=mcs×2 is a design artifact coupling two swept parameters; prescribed fix (fixed floor passed as `--subsample_floor <int>` independent of mcs) is correct and specific.

**Should surface as new Discipline candidate** (not merely a "sweep design improvement") because it is a methodology-correctness constraint — any future sensitivity sweep that varies a parameter feeding the subsample floor is confounded by design.

**Recommendation:** knight-rider queues this as **Discipline #20 candidate** — *"single-parameter sweep isolation: the subsample composition must not vary when only the clustering parameter is under test."*

Not blocking here because the confound is mild for dominant lineages and the direction of findings is unchanged (the STRONGER arctic null result at mcs=30 actually strengthens the conclusion). But should not remain as footnote-only observation.

### Finding 7 — 9.13-A anomaly framing [WARN]

Three-layer diagnosis largely correct:
- (a) clustering placed PMD mines into European/unknown cluster correctly per substrate metrics — confirmed by top-rep stability across all 4 mcs variants
- (b) gandalf labeled the cluster "Spear Family" as a labeling artifact — completion summary notes the provisional description was "european unknown mixed weapons" before canonical override
- (c) joint outcome is the anomaly

**Framing stops short of recommending a corrective action.** Completion summary says "noted for elrond's 9.11-D review" but the corrective path is ambiguous: is this (i) relabel cluster 116 to something accurate like "European Uncurated-Period Mixed Weapons" in production DB, or (ii) wait for 9.11-D substrate cleanup and potentially re-cluster?

**Lower-cost path:** label is wrong NOW in production DB and does not require re-clustering to fix. Targeted gandalf relabel of cluster 116 fixes it without waiting for 9.11-D.

**Recommendation:** knight-rider surface this distinction to gandalf explicitly — "label is wrong" (fixable now) vs "substrate is wrong" (requires 9.11-D). Not a BLOCK because production-DB state is not being consumed by a player-facing system under active development.

### Finding 8 — Sub-carry status updates [INFO]

- 9.10-G: CLOSED — Phase E-1.5 complete
- 9.10-G.1: CLOSED — psutil 7.2.2 + RSS-guard active

Findings that should surface as new queued items or escalations:
- **New Discipline #20 candidate** (per Finding 6)
- **Cluster 116 label fix** — gandalf targeted relabel (per Finding 7); lower-cost than waiting for 9.11-D
- **Cluster 62 sub-clustering** — design option surfaced to gandalf if weapon-form granularity within fantasy_named_template becomes a priority (comparison report §9.3 handles as data not commitment)
- **F6 floor prescription** — dispatch-authoring guidance for future sweeps using mcs > 10 (comparison report §9.4; should fold into dispatch template or engineering disciplines)

---

## 3. Synthesis for knight-rider follow-on actions

| Finding | Required follow-on |
|---|---|
| F6 (Discipline #20 candidate) | Author Observation 7 in `knight-rider/notes/2026-05-23-discipline-observations-for-jack-ryan.md`; queue for jack-ryan ratification |
| F7 (cluster-116 relabel) | Author surface note for gandalf at `agentic_orchestration/gandalf/open-threads/` (or equivalent); routes to gandalf for next-session decision (relabel OR defer to 9.11-D) |
| F8 sub-bullets (Cluster 62 sub-clustering; F6 floor prescription) | Captured as data in legolas comparison report § 9; no separate artifact needed; gandalf design call can consume |
| Sub-carry closures | CHANGELOG Cycle 9.13 entry: 9.10-G + 9.10-G.1 CLOSED |

---

## 4. Empirical reinforcements landed this cycle

The sensitivity sweep's findings reinforce several earlier decisions empirically:

1. **k=3 substrate-voting decision (Cycle 9.10 frame-revision)** — all 4 mcs variants at acceptance-tier purity and cluster-count thresholds. The k=3 lock is robust to mcs variation.
2. **Gandalf coarse-spine acceptance (Cycle 9.11 Gate-2 condition 3)** — form-bundling distribution stable through mcs=20; coarse-spine canonical labeling decision empirically backed.
3. **9.11-D → 9.11-E corrective path (gandalf 9.11-G meta-record recommendation)** — Mode-B dominance of rare-lineage clusters confirmed; mcs is empirically the wrong parameter to vary; substrate-tagging-discipline work is the right path. Not just observation; now empirically grounded.
4. **9.13-A PMD landmines anomaly** — mcs-invariant; structural placement is correct per substrate metrics; the label is the artifact, not the clustering. Reframes 9.13-A from "diagnostic feed for 9.11-D" to "label-fix-now OR substrate-fix-later" two-path decision (per Finding 7).

---

**Signed:** knight-rider, post-Gate-2-CONDITIONAL-PASS synthesis 2026-05-23 ~14:35 EDT. Phase E-1.5 acceptance recorded; 2 named conditions to fold; 9.11-D NOT blocked.
