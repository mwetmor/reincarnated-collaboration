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

(append on completion)
