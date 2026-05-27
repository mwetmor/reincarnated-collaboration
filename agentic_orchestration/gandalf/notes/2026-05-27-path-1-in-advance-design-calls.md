# Path (1) — In-Advance Design Calls Record

> **STATUS:** CURRENT — gandalf-authored. Five deeper design surfaces that compose with Path (1) Phase 4 + Phase 5 + Phase 7 work; Matt pre-thinking encouraged before KR fires bundled math-note Matt-gate. Routes to Matt as a thinking-aid; KR surfaces these alongside the 8 math-note Matt-gate questions when ratification fires.

**Date:** 2026-05-27 evening
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above" + "confirm execute on all three"
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (Path 1 recognition record)
- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` (Discipline #46 candidate)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.1 (amendment-pass-record entry)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` (companion)

---

## 0. TL;DR

Five in-advance design calls worth pre-thinking before KR fires bundled math-note Matt-gate. NOT blocking — KR will surface these alongside the 8 math-note Matt-gate questions. Pre-thinking gives Matt time to mull deeper architectural surfaces.

| # | Design call | Stakes |
|---|---|---|
| **A** | Faction cardinality target per season | Composes with faction-pair-seasons thought; affects clustering algorithm choice + parameters |
| **B** | Archive persistence — per-season reset or persistent | Per-season simpler; persistent grows; Discipline #46 § 7 critical if persistent |
| **C** | Phase 4 archive capacity per BC cell | Per-cell algorithm cost + archive growth + eviction frequency |
| **D** | Faction-coalescence × Sketch F named-personage interaction | Cross-cluster named-personage allocation policy |
| **E** | Phase 4 reject handling — what happens to REJECTED kits | Discard / retain in reject pool / log for human review |

---

## 1. Design Call A — Faction cardinality target per season

### 1.1 The question

How many factions should Phase 5 multimodal clustering produce per Reincarnated v1 season?

### 1.2 Why it matters architecturally

Math Note PM-1 (Multimodal Clustering Algorithm) chooses between:
- **K-means** — requires K (cluster count) specified explicitly
- **DBSCAN** — derives cluster count from density parameters
- **Gaussian mixture** — requires K
- **Hierarchical agglomerative** — produces dendrogram; cluster count chosen via cut-height

Choice depends on whether faction cardinality is:
- **Specified** (designer/Matt-locked target) — K-means / Gaussian mixture work
- **Emergent** (substrate clustering decides) — DBSCAN works
- **Hybrid** — hierarchical lets us cut at multiple levels and pick the "best" cardinality per-season

### 1.3 Composition with prior thought experiments

**Matt 2026-05-27 earlier (Earth realm + Court of Forms session):**
> "If I'm successful at producing a seasonal roster of 50-100 forms, I can launch seasons which are faction pairs."

This implies **2 factions per season** (faction-pair seasons) as a deliberate seasonal target.

**Pattern:** **K=2 factions per season** (faction-pair structure) with possible variants (K=3 triangulated; K=4 dual-pair) per season-brief.

Or alternatively: emergent K via DBSCAN, with seasonal-brief BIAS toward 2-faction outcomes when substrate allows.

### 1.4 Options

| Option | Approach | Trade-off |
|---|---|---|
| **A1** | K=2 fixed; faction-pair structure per season | Cleanest narrative; lockstep with seasonal-brief; potentially forces clustering when substrate doesn't naturally bimodal |
| **A2** | K=2-4 emergent per season | DBSCAN allows clustering to vote; seasonal-brief can prefer K=2 but accept variant |
| **A3** | K=3-8 emergent with no upper bound | Maximum flexibility; risks faction-explosion (10+ thin factions) |
| **A4** | K-by-substrate-evidence-vote | Substrate density + diversity vote K per BC cell; complex |

**gandalf-recommend: A2 (K=2-4 emergent with bias).** Honors substrate-led discipline (DBSCAN votes) while preserving design intent (faction-pair preferred). Math Note PM-1 specifies DBSCAN parameters tuned for K=2-4 typical output.

### 1.5 Pre-think question for Matt

**Does v1 commit to faction-pair structure (K=2 always)? Or is K=2-4 emergent (with seasonal-brief preference for K=2) preferable?**

---

## 2. Design Call B — Archive persistence (per-season or cross-season)

### 2.1 The question

Does the Phase 4 kit archive persist across seasons, or reset per-season?

### 2.2 Per-season reset

- **Pro:** simpler engineering; archive size bounded by single season's generation pool (~50-100 raw kits); Discipline #46 § 7 per-cell bounding simpler
- **Pro:** Wave 5 production per season operates against fresh archive; no cross-season carryover
- **Pro:** seasonal theme coalescence intact (each season's faction-coalescence operates against own kit pool)
- **Con:** no cross-season learning — substrate doesn't accumulate Pareto-frontier knowledge across seasons
- **Con:** Court of Forms accumulation operates on individual kits (ascended Spirits); doesn't compose with persistent kit archive

### 2.3 Cross-season persistent

- **Pro:** Pareto frontier accumulates across seasons; archive becomes substrate-evidence record of "what mechanical forms have we shipped?"
- **Pro:** novel-vs-already-shipped detection — Mahalanobis duplicate detection prevents shipping the SAME kit-shape across seasons
- **Pro:** Composes with Court of Forms (Court collects Spirits; archive collects kit-shapes the Spirits embody)
- **Con:** archive grows unbounded; Discipline #46 § 7 per-cell bounding CRITICAL
- **Con:** eviction policy becomes load-bearing; cross-season eviction decisions affect substrate-evidence accumulation
- **Con:** "fresh emergence" each season is muted — Season N's kits compete against Season N-1, N-2, ... for archive slots

### 2.4 Hybrid options

- **B1** Per-season archive + persistent "Court archive" — current season's archive is per-season; ascended Spirits move into persistent Court archive for cross-season uniqueness checking
- **B2** Per-cell persistence varies — high-density cells (martial-heavy) per-season; low-density cells (caster-faith) persistent for accumulation

### 2.5 gandalf-recommend

**B1 (per-season archive + persistent Court archive).** Per-season is operationally cleaner; Court archive holds ascended Spirits and serves cross-season uniqueness AND composes with Earth Meta-Layer Court-of-Forms narrative.

### 2.6 Pre-think question for Matt

**Per-season reset (operational simplicity)? Cross-season persistent (substrate-evidence accumulation)? OR B1 hybrid (per-season archive + persistent Court archive)?**

---

## 3. Design Call C — Phase 4 archive capacity per BC cell

### 3.1 The question

How many kits per BC cell in the archive?

### 3.2 Why it matters

Per-cell capacity bounds:
- Per-cell algorithm cost (Pareto + Crowding + Mahalanobis are O(k²) per cell; k=10 → 100 ops; k=100 → 10,000 ops; k=1000 → 1M ops)
- Total archive size (capacity × ~68,040 cells × density of populated cells)
- Eviction frequency (low capacity → eviction every generation; high capacity → eviction rare)

### 3.3 Options

| Option | Capacity / cell | Total archive (if 1% cells populated) | Per-cell ops |
|---|---|---|---|
| **C1** | 10 | 6,800 kits | 100 ops |
| **C2** | 30 | 20,400 kits | 900 ops |
| **C3** | 100 | 68,040 kits | 10,000 ops |
| **C4** | 1000 | 680,400 kits | 1M ops (Discipline #46 § 7 critical) |

### 3.4 gandalf-recommend

**C2 (30 kits / cell)** for Cycle 14 v1. Per-cell algorithm cost ~900 ops (trivial); total archive bounded at ~20-30K kits across many seasons; Discipline #46 § 7 protects.

If empirical evidence shows 30/cell is too restrictive (forces eviction every generation), Cycle 15+ tuning to C3 (100/cell).

### 3.5 Pre-think question for Matt

**Default 30 kits per BC cell OK? Or different target?**

---

## 4. Design Call D — Faction-coalescence × Sketch F named-personage interaction

### 4.1 The question

Phase 5 produces:
- **Multimodal clustering** → faction labels (emergent per-season)
- **Sketch F named-personage allocation** → ~32% of forms get named-personage anchors (Lu Bu, Arthur, Beowulf, etc.)

How do these compose?

### 4.2 Composition options

| Option | Faction × Named-personage interaction |
|---|---|
| **D1** | **Faction-coupled named-personage** — each faction has a curated named-personage pool (Crimson Court members get Vampire / Imperial named anchors; Verdant Reach members get Druidic / Pastoral anchors). Faction membership LOCKS named-personage pool. |
| **D2** | **Faction-orthogonal named-personage** — Sketch F allocation is faction-independent; Lu Bu can appear in any faction; faction-narrative interprets the cross-faction named-personage |
| **D3** | **Cohesion-judge-determined** — Phase 5 cohesion-judge LLM decides per-kit whether to apply Sketch F allocation given faction context; high-faction-named-personage alignment → name; low alignment → engine-named-original per bi-modal pattern |

### 4.3 gandalf-recommend

**D3 (cohesion-judge-determined).** Honors substrate-led discipline (cohesion judge votes; not pre-coupled); allows flexibility (Lu Bu can appear in Crimson Court IF cohesion judge sees alignment); preserves Sketch F bi-modal pattern; composes with Wave 3 Phase 5 LLM scope.

### 4.4 Pre-think question for Matt

**Faction × named-personage interaction = D1 / D2 / D3?** D3 is gandalf-recommend; faction-coupled (D1) is more rigid; faction-orthogonal (D2) is most flexible but might lose narrative cohesion.

---

## 5. Design Call E — Phase 4 reject handling policy

### 5.1 The question

When Phase 4 math gates REJECT a kit (Pareto-dominated / duplicate / low-novelty / cell-at-capacity-evicted), what happens to the rejected kit?

### 5.2 Options

| Option | Rejected kit handling | Trade-off |
|---|---|---|
| **E1** | **Discarded entirely** — REJECT means delete | Cleanest; no leftover state; rejected kits are lost work |
| **E2** | **Retained in "reject pool"** — REJECTED kits logged for cross-season substrate-evidence | Preserves substrate-evidence; archive growth bounded by Discipline #46 § 7 only on ACCEPTED archive; reject pool is separate growing surface |
| **E3** | **Returned to Phase 2 with re-roll** — REJECT triggers re-generation at same BC cell with different seed | Preserves cell coverage; risks infinite-rejection loops |
| **E4** | **Returned to Phase 5 with re-coalesce** — REJECT (mechanical pass) triggers re-cohesion at Phase 5 | Specific to cohesion-fail; preserves kit but re-themes |
| **E5** | **Logged for human review** — REJECTED kits surface to gandalf for design-quality audit | Preserves designer override; risks substrate-led discipline erosion |

### 5.3 gandalf-recommend

**E1 (discarded) for Cycle 14 v1; E2 (reject pool) considered Cycle 15+.**

E1 operational simplicity. E5 (human review) violates substrate-led discipline if used for override; if used for telemetry only, fine but cost overhead.

Phase 7 2-layer joint-gate HELD verdict (per amended doc 39 § 5.7) is separate from Phase 4 REJECT — HELD means "passed Phase 4 + 5 but failed joint-gate composition"; HELD kits may return to specific phase per Path 1 record § 3.3. REJECT (Phase 4) is more terminal than HELD (Phase 7).

### 5.4 Pre-think question for Matt

**Cycle 14 v1 Phase 4 REJECT = discard (E1)?** OR retain in reject pool (E2)? OR something else?

---

## 6. How these compose with the 8 math-note Matt-gate decisions

When KR fires bundled math-note Matt-gate per kicker § 3.2, the 8 math-note design calls + these 5 in-advance design calls compose into a single bundled ratification:

**Phase 4 math-note decisions (per Path 1 record § 3.1):**
1. Pareto formulation
2. Crowding metric
3. Mahalanobis dimensional projection
4. KL reference distribution
5. Eviction policy

**Phase 5 math-note decisions (per Path 1 record § 3.2):**
6. Multimodal clustering algorithm (composes with Design Call A — faction cardinality)
7. Faction-label assignment policy (composes with Design Call D — named-personage interaction)

**Phase 7 calibration decision (per Path 1 record § 3.3):**
8. 2-layer joint-gate thresholds

**Plus these 5 in-advance design calls:**
- A: Faction cardinality target
- B: Archive persistence (per-season or cross-season)
- C: Phase 4 archive capacity per BC cell
- D: Faction-coalescence × Sketch F named-personage interaction
- E: Phase 4 reject handling policy

Total 13 design calls bundled at single Matt-gate. Sounds substantial but each is concise; gandalf-recommend exists for all 13; ratification is mostly review + confirm-or-amend per discipline.

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — in-advance design calls record for Matt pre-thinking before bundled math-note Matt-gate fires
**Authority:** Matt 2026-05-27 "confirm execute on all three"
**Composition:** with Path 1 recognition record + Discipline #46 candidate + failure-modes register; preserves no-class architectural commitment + substrate-led discipline at all design calls

**For:** Matt pre-thinking on 5 deeper design surfaces (A faction cardinality / B archive persistence / C archive capacity per cell / D faction-coalescence × Sketch F interaction / E Phase 4 reject handling) that compose with the 8 math-note design calls at bundled Matt-gate. KR surfaces these alongside math-note Matt-gate when ratification fires; pre-thinking gives Matt time to mull deeper architectural surfaces before ratification.

**Signed:** gandalf (story-and-design steward)
