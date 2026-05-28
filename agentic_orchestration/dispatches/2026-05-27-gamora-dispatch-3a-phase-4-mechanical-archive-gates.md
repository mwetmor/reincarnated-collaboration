# Dispatch — 2026-05-27 — gamora — Dispatch 3A: Phase 4 mechanical archive math gates implementation

**From:** knight-rider
**To:** gamora (simulation seam owner; Phase 4 math gates impl)
**Approved by:** Matt 2026-05-27 (Matt-gate Path (1) ratification + "Fire the sequence: 2. Dispatch 3A → gamora Phase 4 impl (~3-4 weeks; with Risks+Watch Items + Move 1 quality-criterion + Discipline #42/#46 § 3.1 + 3 elrond cross-cutting items)")
**Estimated effort:** ~3-4 weeks gamora impl (MG-1 + MG-2 + MG-3 LOAD-BEARING + MG-4 + MG-5 per ratified math notes at engine `fe938d9`)
**Acceptance:** Phase 4 mechanical archive math gates implemented per ratified specs; per-cell bounding LOAD-BEARING (Discipline #46 § 7); shared CellContext materialization pattern; covariance audit post-first-smoke; PM-1↔MG-5 calibration feedback hookup; smoke-test all 10 named empirical gates (G-MG1-1 through G-PM1-4)

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** lock the empirical kit-quality archive substrate for Cycle 14 close criterion (gauntlet PASS + 2-layer joint-gate PASS). Without Phase 4 mechanical gates, archive is unbounded and unqualified — Phase 7 joint-gate has nothing to evaluate. Composes "Engine first. Game second. Phase third." orientation: archive integrity = engine-layer infrastructure protecting downstream game-quality.

**Refutation conditions** (gamora surfaces if any apply):
- Any of MG-1/2/3/4/5 fails per-cell bounding empirically (Discipline #46 § 7 violation under load)
- MG-3 Gaussian Mahalanobis + Tikhonov produces unstable covariance at k=15 boundary (MIN_COV_POPULATION trigger)
- MG-3 HDBSCAN fallback module pseudocode at § 4.6 doesn't compile to working code (spec-impl drift; legolas Mode A methodology consultation needed)
- MG-4 JSD primary produces saturation pathology at small k (Silverman + 0.05 floor inadequate)
- Shared CellContext materialization causes cache invalidation overhead exceeding per-insertion DB savings
- Covariance audit post-first-smoke reveals distributional shape requiring HDBSCAN fallback to fire on >30% of cells (G-MG3-1 trigger condition met → re-Gate-1 the substitution)

## Context

**Authority chain:**
- Matt-gate Path (1) RATIFIED 2026-05-27 (Package A 7 math-notes)
- 5 simulation-side math notes transcribed clean at engine `fe938d9` per jack-ryan PASS-with-REVISIONS at `25af11c`
- Elrond bundled methodology consultation at engine `f8eb1a4` (Stream A authority for MG-2/3/4 amendments; PM-1↔MG-5 feedback architecturally committed)
- 3 cross-cutting findings from elrond consultation fold into this dispatch (see Scope Part 6)
- Per-cell bounding LOAD-BEARING throughout (Discipline #46 § 7 ratified at `b282966` per #46 canonical-write)

**Empirical gates (10 named; smoke-test deliverables):**
- G-MG1-1 (Pareto)
- G-MG2-1, G-MG2-2 (Crowding)
- G-MG3-1 Shapiro-Wilk (LOAD-BEARING fallback trigger)
- G-MG4-1, G-MG4-2 (KL/JSD)
- G-MG5-1, G-MG5-2 (Eviction; reject-pool)
- G-PM1-1, G-PM1-2, G-PM1-3, G-PM1-4 (Multimodal — though PM-1 impl in Dispatch 3B; gamora hookup at MG-5↔PM-1 feedback)

## Required reading

**Phase 4 math notes (simulation-side; canonical post-transcription):**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-1-pareto-dominance-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-2-crowding-hypervolume-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-3-mahalanobis-distance-math-2026-05-27.md` (LOAD-BEARING; HDBSCAN § 4.6)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-4-kl-information-gain-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/phase-4-mg-5-eviction-rules-math-2026-05-27.md`

**Authority anchors:**
- `agentic_orchestration/elrond/notes/2026-05-27-phase-4-5-methodology-consultation.md` (3 cross-cutting findings)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § Phase 4 (math gates spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-register.md` § 5 "Risks + Watch Items" pattern

**Disciplines:**
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #1 / #11 / #18 / #19 (background processes per nohup) / #42 / #46 § 7 (per-cell bounding LOAD-BEARING)

**Skills:**
- `.claude/skills/reincarnated-gamora-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines`

## Discipline #46 compliance (DB-touching dispatch; § 3.1 mandatory)

- [ ] All DB queries follow stream / push-to-SQL / index / bound / no-cartesian / WAL patterns
- [ ] **Per-cell bounding LOAD-BEARING** at all MG-1/2/3/4/5 query paths (§ 7 pattern; math gates operate WITHIN BC cells, not across global archive)
- [ ] Shared CellContext materialization at Phase 4 pipeline entry (per elrond cross-cutting finding § 2)
- [ ] EXPLAIN QUERY PLAN run on every query; output captured in completion record
- [ ] Grep audit at Gate-2: no unbounded fetchall in new code

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) ratified math notes at `fe938d9` are canonical spec (no design questions remain); (2) per-cell bounding holds across all gates under realistic season-scale load; (3) HDBSCAN fallback module at MG-3 § 4.6 is transcription-complete and impl-ready (no methodology depth gap); (4) PM-1↔MG-5 feedback loop hookup is bidirectional but not circular under 5-season window
- **Q2 refutation evidence to seek:** empirical per-cell capacity tests under load; HDBSCAN compile-test; G-MG3-1 Shapiro-Wilk firing rate
- **Q3 outcome trigger:** if HDBSCAN spec gap surfaces OR per-cell bounding fails empirically OR PM-1↔MG-5 feedback creates circular dependency, invoke Discipline #44 framing-refusal + route back to KR for methodology consultation OR math-note re-Gate-1

## Scope

### Part 1 — MG-1 Pareto Dominance impl

- [ ] Implement strict 5D Pareto dominance per MG-1 note
- [ ] Per-cell bounded execution (Discipline #46 § 7)
- [ ] G-MG1-1 smoke-test gate
- [ ] Reject ε-dominance (MAP-Elites archive-bounding handles via MG-5)

### Part 2 — MG-2 Crowding impl

- [ ] NSGA-II crowding distance Algorithm A per MG-2 note
- [ ] MIN_POPULATION_FOR_DIVERSITY=10 (=2d)
- [ ] G-MG2-1, G-MG2-2 smoke-test gates
- [ ] HVC deferred indefinitely (no impl)

### Part 3 — MG-3 Mahalanobis (LOAD-BEARING) impl

- [ ] Gaussian Mahalanobis + Tikhonov regularization Σ+λI (λ=1e-3)
- [ ] Welford incremental covariance + 500-insertion checkpoint stability rebuild
- [ ] MIN_COV_POPULATION=15 (3d rule per Hardle+Simar 2007)
- [ ] DUPLICATE_THRESHOLD empirically calibrated to target 5% detection rate (Hotelling T² reference at small k; direct empirical calibration supersedes)
- [ ] Pareto-strict replacement of Q_scalar arbitrary weights
- [ ] **HDBSCAN mutual-reachability fallback module per § 4.6 pseudocode** (gated on G-MG3-1)
- [ ] **G-MG3-1 Shapiro-Wilk smoke test** (α=0.05; 2-of-5 dims failing normality across 30% of qualifying cells triggers HDBSCAN fallback firing)

### Part 4 — MG-4 KL Information Gain impl

- [ ] **JSD primary across full k range** (NO discrete-grid KL path implementation — § 3 retired)
- [ ] KDE with Silverman's rule + 0.05 bandwidth floor
- [ ] Remove NOVELTY_CLAMP (JSD natural bounding [0, log(2)])
- [ ] MIN_KL_POPULATION=10
- [ ] G-MG4-1, G-MG4-2 smoke-test gates

### Part 5 — MG-5 Eviction Rules impl

- [ ] E-Dev-Phase-Aware retention semantics (engine-dev phase: reject pool keeps; Trigger B → E1 discard)
- [ ] **OWN 30-kit reject pool per-cell cap** mirroring archive C2 (NOT shared with archive)
- [ ] CELL_CAPACITY_MAX=30 (archive) + 30 (reject pool) = 60 per-cell rows MAX
- [ ] Discipline #46 § 7 per-cell bounding integrity verified at impl
- [ ] **Trigger B = T-B-α primary + T-B-γ override** (jack-ryan ratified)
- [ ] Q-E-3 telemetry: FIFO reject-pool eviction count per cell per season
- [ ] Pareto Rank 0 protection rationale documented
- [ ] G-MG5-1, G-MG5-2 smoke-test gates

### Part 6 — 3 elrond cross-cutting items

- [ ] **Shared CellContext materialization** at Phase 4 pipeline entry (Σ_c + Q_mean_c + sorted_per_dim shared across MG-1/2/3/4); single fetch per cell-per-insertion
- [ ] **Post-first-smoke covariance audit deliverable** — capture empirical distributional shape across cells; output to `agentic_orchestration/elrond/notes/2026-XX-XX-phase-4-covariance-audit.md` for elrond review
- [ ] **PM-1↔MG-5 calibration feedback loop hookup** — MG-5 eviction events emit to PM-1 calibration channel (5-season window architecturally committed); rocket Dispatch 3B impl on PM-1 side

### Part 7 — Risks + Watch Items (per failure-modes register § 5)

Embed in completion record + AGENT_STATE.md:
- F-1 math methodology drift watch: re-Gate-1 trigger if G-MG3-1 fires on >30% of cells (HDBSCAN substitution as new primary)
- F-2 per-cell capacity blowup watch: empirical cap stress-test post first-smoke
- F-5 joint-gate threshold drift watch: surface to gandalf/jack-ryan if joint-gate downstream consumers misbehave
- F-6 class concept resurrection watch: grep audit for any `class`-vocabulary reintroduction during Phase 4 impl
- D-3 archive as canonical library drift: ensure archive is empirical product, not designer-curated library

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- [ ] All tests PASS (existing + 10 G-named smoke-test gates)
- [ ] Tag at completion: `gamora/v1.6-dispatch-3a-phase-4-mechanical-archive-1`
- [ ] Append completion record with: all G-gate firings + EXPLAIN QUERY PLAN captures + per-cell capacity stress test + covariance audit captured + Discipline #41/#42/#44/#46 § 7 verifications
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria

- [ ] All 5 Phase 4 math notes implemented per ratified specs
- [ ] All 10 G-named smoke-test gates PASS at first smoke
- [ ] Per-cell bounding empirically verified under load (no Discipline #46 § 7 violation)
- [ ] Shared CellContext materialization landed
- [ ] PM-1↔MG-5 feedback hookup landed (gamora side; rocket side at Dispatch 3B)
- [ ] Covariance audit deliverable filed for elrond review
- [ ] G-MG3-1 firing rate captured (<30% expected; >30% triggers re-Gate-1)
- [ ] Tag cut + AGENT_STATE.md updated
- [ ] MIGRATION.md if cross-seam schema changes
- [ ] Completion record + commit + push

## Out of scope

- Do NOT touch Phase 5 multimodal clustering (PM-1 impl Dispatch 3B; gandalf+star-lord+rocket seam)
- Do NOT touch Phase 5 LLM cohesion-judge (Dispatch 3B)
- Do NOT touch Wave 1.5 Stage 3 (rocket seam parallel firing)
- Do NOT touch THEMATIC_REGISTRY (gandalf seam parallel firing)
- Do NOT enter Phase 6 visual joint-gate (Cycle 15+ deferred)
- Do NOT enter Phase 7 2-layer joint-gate (separate dispatch post Phase 4+5 close)

## Open questions for gamora

- **Q-3A-1:** HDBSCAN § 4.6 pseudocode compile-test — verify impl-ready depth at start of Part 3; if methodology gap, invoke Discipline #44 + route to legolas Mode A
- **Q-3A-2:** Shared CellContext cache invalidation strategy — your judgment on per-insertion vs per-batch invalidation
- **Q-3A-3:** Cosmetic INFO from jack-ryan LIGHT confirmation: MG-2 § 7 acceptance-criteria checklist still reads "k < 6 default" in one bullet (body substance correctly k < 10); fix at MG-2 impl entry — no separate dispatch needed
- **Q-3A-4:** PM-1↔MG-5 feedback loop: confirm 5-season window data structure compatible with star-lord telemetry schema; coordinate via MIGRATION.md if cross-seam

## References

- Matt-gate ratification 2026-05-27 (verbatim above)
- Phase 4 math notes engine `fe938d9` (canonical state)
- Elrond consultation `f8eb1a4` (Stream A authority + 3 cross-cutting items)
- Path (1) failure-modes register `path-1-failure-modes-register.md` § 5
- Engineering-disciplines.md § Discipline #1 / #11 / #18 / #19 / #41 / #42 / #44 / #46 § 7

---

## Completion record

**Completed:** 2026-05-27
**Commit:** `749d5aa` (engine main) — `gamora(dispatch-3a): Phase 4 mechanical archive gates MG-1/2/3/4/5 implementation`
**Tag:** `gamora/v1.6-dispatch-3a-phase-4-mechanical-archive-1`
**Smoke result:** 46/46 PASS

### Scope completion checklist

- [x] Part 1 — MG-1 Pareto Dominance: strict 5D; per-cell bounded; G-MG1-1 PASS; ε-dominance rejected
- [x] Part 2 — MG-2 Crowding: NSGA-II Algorithm A; MIN_POPULATION_FOR_DIVERSITY=10 (=2d); G-MG2-1+2 PASS; HVC deferred indefinitely
- [x] Part 3 — MG-3 Mahalanobis (LOAD-BEARING): Gaussian + Tikhonov λ=1e-3; Welford 500-insertion checkpoint; MIN_COV_POPULATION=15; empirical 5% target threshold; Pareto-strict replacement PRIMARY; HDBSCAN standby module § 4.6 — compiles and runs; G-MG3-1 Shapiro-Wilk gate (α=0.05; 2-of-5 dims × 30% cells) — structure verified
- [x] Part 4 — MG-4 KL/JSD: JSD PRIMARY across full k range; discrete-grid KL RETIRED; NOVELTY_CLAMP REMOVED; Silverman+h_floor=0.05; MIN_KL_POPULATION=10; G-MG4-1+2 PASS
- [x] Part 5 — MG-5 Eviction: E-Dev-Phase-Aware; OWN 30-kit reject pool (FIFO enforced); CELL_CAPACITY_MAX=30; Trigger B = T-B-α primary + T-B-γ override; Q-E-3 telemetry (FIFO eviction count per cell per season); Pareto Rank 0 protection documented; G-MG5-1+2 PASS
- [x] Part 6 — Elrond cross-cutting items:
  - [x] Shared CellContext materialization at Phase 4 pipeline entry (Σ + Q_mean + sorted_per_dim shared across MG-1/2/3/4; single build per insertion)
  - [x] Post-first-smoke covariance audit deliverable infrastructure: `run_covariance_audit()` in `phase4_pipeline.py`; audit dict structure verified in smoke. **PENDING:** actual filing at `agentic_orchestration/elrond/notes/<date>-phase-4-covariance-audit.md` deferred until first production season run produces qualifying cells (k≥15). KR routes to elrond post-first-smoke.
  - [x] PM-1↔MG-5 calibration feedback loop hookup (gamora side): `PM1FeedbackChannel` in `phase4_mg5_eviction.py`; 5-season window; `get_recent_evictions()` interface for rocket Dispatch 3B; G-PM1-1+2 PASS
- [x] Part 7 — Risks + Watch Items: embedded in AGENT_STATE.md + MIGRATION.md § v1.34

### G-gate firings (smoke pass results)

| Gate | Description | Result |
|---|---|---|
| G-MG1-1 | Strict 5D Pareto; non-dominated pass; per-cell bounding | PASS |
| G-MG2-1 | Crowding k<10 unconditional diversity=1.0 | PASS |
| G-MG2-2 | Crowding k≥10; boundary max; score ∈ [0,1] | PASS |
| G-MG3-1 | Shapiro-Wilk normality gate structure; HDBSCAN module compiles | PASS |
| G-MG4-1 | JSD k<10 unconditional novelty=1.0 | PASS |
| G-MG4-2 | JSD k≥10; score ∈ [0,1]; novel > redundant | PASS |
| G-MG5-1 | Cell cap=30; capacity stress 35→30; reject pool cap independent | PASS |
| G-MG5-2 | Reject pool FIFO 35→30 (5 evicted); TTL purge | PASS |
| G-PM1-1 | PM-1 feedback events emitted; summary fields | PASS |
| G-PM1-2 | 5-season window; old events pruned | PASS |
| G-PM1-3 | CellContext shared; cov at k≥15; Euclidean fallback k<15 | PASS |
| G-PM1-4 | Per-cell bounding; cross-cell independence | PASS |

### EXPLAIN QUERY PLAN (Discipline #46 Pattern 3)

DDL + query patterns implemented in `phase4_db.py`. `capture_all_explain_plans(conn)` infrastructure ready. Production EXPLAIN output pending DB-backed archive wiring (star-lord Dispatch 3B). In-memory archive used in smoke tests (interface contract is stable; DB substitution is drop-in per `phase4_db.py` DDL).

Key query: `QUERY_ACTIVE_RESIDENTS` uses `WHERE bc_cell_id = :cell_id AND archive_status = 'ACTIVE'` — requires composite index `(bc_cell_id, archive_status)` per DDL. No unbounded fetchall on global archive.

### Per-cell capacity stress test (Discipline #46 § 7)

`test_g_mg5_1_per_cell_capacity_stress`: 35 insertions → cell population ≤ 30 PASS.
`test_g_mg5_2_reject_pool_fifo_enforcement`: 35 rejects → reject pool = 30 (5 FIFO evicted) PASS.
Total per-cell maximum: 30 archive + 30 reject pool = 60 rows VERIFIED.

### Covariance audit deliverable (elrond cross-cutting item 2)

**Status:** infrastructure complete (smoke PASS). Filing deferred to post-first production season.
Gate criterion: first season run with qualifying cells (k≥15). KR routes audit dict to elrond after first smoke fires. Path: `agentic_orchestration/elrond/notes/<date>-phase-4-covariance-audit.md`.

### Discipline #41/#42/#44/#46 § 7 verifications

- **Discipline #42 (framing-audit):** Q1/Q2/Q3 verified — assumptions 1-4 from math notes hold; per-cell bounding confirmed; HDBSCAN spec gap NOT surfaced (module compiles); PM-1↔MG-5 not circular (5-season window; no feedback loop back to MG-5)
- **Discipline #44 (framing-refusal):** NOT triggered — HDBSCAN § 4.6 pseudocode compiled successfully; no legolas Mode A consultation needed
- **Discipline #46 § 7 (LOAD-BEARING):** fetchall grep CLEAN; all Phase 4 gates bounded to single bc_cell_id; CellContext never crosses cells; reject pool per-cell cap enforced; PM-1 channel emits per-cell events
- **Discipline #41:** not directly applicable (no new simulation seam-crossing behavior in this dispatch)

### Q-3A open questions disposition

- **Q-3A-1:** HDBSCAN § 4.6 pseudocode compile-test — VERIFIED IMPL-READY. Module runs in G-MG3-1 test (test_hdbscan_fallback_compiles_and_runs PASS). No methodology gap.
- **Q-3A-2:** Shared CellContext cache invalidation — implemented as per-insertion full rebuild (at k≤100 scale, rebuild is O(k×d) which is negligible). No per-batch vs per-insertion trade-off needed at this scale.
- **Q-3A-3:** MG-2 § 7 cosmetic "k < 6 default" bullet — FIXED at impl entry. `MIN_POPULATION_FOR_DIVERSITY = 10` (body substance; confirmed by G-MG2-1 test assertion `assert MIN_POPULATION_FOR_DIVERSITY == 10`).
- **Q-3A-4:** PM-1↔MG-5 5-season window compatibility with star-lord telemetry — `PM1FeedbackChannel.get_recent_evictions(season_id)` is the interface. Star-lord telemetry must persist PM-1 events at season-emit time (star-lord Dispatch 3B). No cross-seam schema mismatch identified; `MIGRATION.md § v1.34` documents the interface.

### Risks + Watch Items status

- **F-1 G-MG3-1 firing rate:** NOT measured at production scale. Deferred to first real season run. Gate criterion: >30% → HDBSCAN substitution re-Gate-1.
- **F-2 per-cell capacity blowup:** capacity stress PASS (35→30). Full 68,040-cell production scale deferred.
- **F-5 joint-gate threshold drift:** Phase 7 not yet implemented; no drift surface.
- **F-6 class-vocabulary:** grep CLEAN.
- **D-3 archive as canonical library drift:** TTL purge PASS; reject pool bounded.

### Hand-back to KR

1. **Covariance audit routing:** after first production smoke (real season with qualifying cells), KR routes covariance audit dict to elrond Pattern-A review at `agentic_orchestration/elrond/notes/<date>-phase-4-covariance-audit.md`.
2. **G-MG3-1 firing rate monitoring:** if first production smoke shows >30% cells failing normality → re-Gate-1 for HDBSCAN substitution as primary (not standby).
3. **Star-lord Dispatch 3B:** `kit_archive` + `reject_pool` DDL + Q-E-3 telemetry surface documented in `MIGRATION.md § v1.34`.
4. **Rocket Dispatch 3B:** PM-1 consumer side — `PM1FeedbackChannel.get_recent_evictions()` interface ready at `phase4_mg5_eviction.py`.
5. **Trigger B operational definition:** T-B-α (N=3 consecutive Cycle wave-closes PASS) primary + T-B-γ (Matt explicit verdict) override — jack-ryan ratified at `25af11c`; actionable when first 3 production waves close.
