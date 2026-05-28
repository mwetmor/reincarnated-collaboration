# Dispatch — 2026-05-27 — gamora — Phase 7 IMPLEMENTATION (kit_archive → gauntlet_sim.py bridge + 2-layer gate runtime + verdict emission)

**From:** knight-rider
**To:** gamora (combat sim integration owner; simulation seam)
**Approved by:** Matt 2026-05-27 verbatim ratification per gamora Pattern A-light F-10 finding: "Phase 7 IMPLEMENTATION dispatch authored + queued (gamora primary; combat sim integration owner; scope per Q4 — kit_archive ACCEPTED iteration + gauntlet_sim.py encounter sweep + cohort KPM measurement per Phase 7 spec thresholds + 2-layer gate runtime + Phase 7 verdict emission to ExportFactionCluster/kit_archive)"
**Estimated effort:** ~1-2 weeks gamora impl
**Acceptance:** Phase 7 IMPLEMENTATION bridge + runtime + verdict emission landed per Phase 7 spec (gandalf `0cf4e3d`) + canonical thresholds (jack-ryan `3d4eda5`); kit_archive ACCEPTED → gauntlet_sim.py iteration; cohort KPM measurement; 2-layer gate verdict emission; MIGRATION.md for gauntlet_pass_rate column addition; smoke-test pre-Wave-5

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** close the F-10 spatial-gauntlet integration gap before Wave 5 production season fires. Phase 7 spec + canonical thresholds exist but the BRIDGE from Phase 4 mechanical archive ACCEPTED → gauntlet_sim.py encounter sweep → cohort KPM measurement → 2-layer verdict emission does NOT exist. Without this bridge, Wave 5 cannot execute. Composes "Engine first. Game second. Phase third." — Phase 7 verdict gate is the engine-layer firewall protecting downstream player-facing quality.

**Refutation conditions** (gamora surfaces if any apply):
- kit_archive ACCEPTED set iteration creates per-cell bounding issues (Discipline #46 § 7 stress under realistic load)
- gauntlet_sim.py encounter sweep semantics incompatible with kit_archive kit schema (kit-shape mismatch between Phase 4 archive output + gauntlet_sim consumer expectations)
- Cohort midpoint median estimator (per jack-ryan Seam 2 `3d4eda5`) requires more substrate than first-Wave-5-season can provide at n=15-20 per-cohort
- HELD verdict 2-retry-per-kit + 1-retry-per-cluster state machine (per gandalf Seam 1 `0cf4e3d`) hits race condition under iterative Position B Wave 5 attempts
- gauntlet_pass_rate column addition to kit_archive requires cross-seam coordination with star-lord ExportFactionCluster/kit_archive schema integration

## Context

**Authority chain:**
- Matt 2026-05-27 F-10 routing ratification (verbatim above)
- Phase 7 spec at `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` (gandalf Seam 1 `0cf4e3d`)
- Phase 7 canonical thresholds at `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` (jack-ryan Seam 2 `3d4eda5`)
- Phase 4 mechanical archive at engine `749d5aa` (gamora Dispatch 3A; kit_archive + reject_pool tables; ACCEPTED signal semantics)
- Phase 5 ExportFactionCluster at engine `bf7f659` (star-lord; phase7_gate_status enum + placeholder semantics + regeneration_fired field)
- Position B Wave 5 amendment (single iterative generation + audit-gate; up to 3 retries; cohort midpoint median estimator robust to ±0.25 band)
- F-10 spatial-gauntlet integration gap registered post gamora Pattern A-light response

**Critical gap (gamora Pattern A-light finding):**
- `spatial_gauntlet/` is R2 2D spatial combat substrate (research; NOT production)
- `gauntlet_sim.py` is the 1D scalar-distance gauntlet executor (production)
- They run CONCURRENTLY; one does NOT replace the other
- **kit_archive does NOT natively feed gauntlet_sim.py** — bridge module required at this dispatch

## Required reading

**Phase 7 dispatch chain:**
- `agentic_orchestration/dispatches/2026-05-27-phase-7-2-layer-joint-gate.md` (Seam 1+2 completion records)
- `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` (gandalf composition spec)
- `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` (jack-ryan canonical thresholds)

**Bridge surfaces:**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/phase4_db.py` (kit_archive DDL + ACCEPTED signal)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/phase4_pipeline.py` (Phase 4 archive integration)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (1D scalar-distance production gauntlet executor; bridge consumer)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` ExportFactionCluster (phase7_gate_status + regeneration_fired fields)

**Cross-cutting:**
- `agentic_orchestration/dispatches/2026-05-27-wave-5-production-season-dispatch.md` § Dependencies (Wave 5 gates on this dispatch landing)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-register.md` § F-10 (added 2026-05-27 per gamora Pattern A-light)
- Engineering-disciplines.md § Discipline #1 / #11 / #18 / #42 / #43 / #44 / #45 / #46

## Discipline #46 compliance (DB-touching dispatch; § 3.1 mandatory)

- [ ] Bridge query: iterate kit_archive WHERE archive_status='ACCEPTED' — per-cell streaming (Discipline #46 § 7 LOAD-BEARING; NO unbounded fetchall over full archive)
- [ ] gauntlet_pass_rate column addition: REAL type per jack-ryan `3d4eda5`; **MIGRATION.md per ADR-004 MANDATORY**
- [ ] EXPLAIN QUERY PLAN at all new query paths (bridge iteration + gauntlet_sim consumer queries + verdict emission writes)
- [ ] No cartesian joins between kit_archive + ExportFactionCluster

## Discipline #42 framing-audit

- **Q1:** (1) Phase 7 spec + canonical thresholds are impl-ready (Seam 1+2 complete); (2) kit_archive ACCEPTED iteration semantics fit gauntlet_sim.py encounter sweep input format; (3) cohort midpoint median estimator works with first-Wave-5-season substrate (n=15-20 per-cohort sufficient)
- **Q2:** verify gauntlet_sim.py input format vs kit_archive kit schema; verify per-cohort substrate count at first-Wave-5-season; verify HELD verdict 2-retry-per-kit + 1-retry-per-cluster state machine fits iterative Position B model
- **Q3:** if kit schema mismatch OR cohort substrate insufficient OR retry semantics conflict, invoke #44 framing-refusal + surface back to KR

## Scope

### Part 1 — gauntlet_pass_rate column addition (~0.5 day)

- [ ] ALTER TABLE kit_archive ADD COLUMN gauntlet_pass_rate REAL
- [ ] **MIGRATION.md per ADR-004** authored (cross-seam coordination with star-lord since ExportFactionCluster/kit_archive may be downstream consumer)
- [ ] EXPLAIN QUERY PLAN on the post-migration table
- [ ] Backfill strategy for any pre-existing kit_archive rows (NULL acceptable until Wave 5 fires)

### Part 2 — kit_archive ACCEPTED → gauntlet_sim.py bridge module (~3-5 days)

- [ ] Create bridge module at `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py` (or your judgment on venue)
- [ ] Iterate kit_archive WHERE archive_status='ACCEPTED' streamed per-cell per Discipline #46 § 7
- [ ] For each ACCEPTED kit: invoke gauntlet_sim.py encounter sweep against kit's cohort (5 cohorts: Damage / Defensive / Control / Support / Hybrid per gandalf spec § 1.3 priority-ordered classifier)
- [ ] Compute gauntlet_pass_rate per kit (encounter sweep results aggregated)
- [ ] Write gauntlet_pass_rate back to kit_archive row
- [ ] Per-seed determinism preserved

### Part 3 — Cohort KPM measurement (~2-3 days)

> **AMENDED 2026-05-27 per Matt D-2B pre-ratification:** NO historical-telemetry prior (avoids synthetic_mode-bypass contamination per Discipline #39); first-Wave-5-attempt empirical KPM distribution IS the calibration source; midpoints recalibrate per Position B retry attempt until first PASS commits; STATIC after first PASS commits (NOT after attempt 1 regardless of audit outcome).

- [ ] Per-cohort gauntlet_pass_rate distribution capture
- [ ] Cohort midpoint median estimator per jack-ryan `3d4eda5` (median per cohort; bootstrap stability ±0.05-0.08 CI at n=15)
- [ ] **D-2B NO PRIOR:** first-Wave-5-attempt produces empirical KPM distribution → midpoints computed from that distribution (NO Cycle 13 telemetry; NO D11+D12 historical prior)
- [ ] **Position B composition:** cohort midpoints RECALIBRATE per retry attempt (if attempt 1 audit FAILs → recalibrate midpoints on attempt 2 distribution; if attempt 2 audit FAILs → recalibrate on attempt 3 distribution); ONCE FIRST PASS COMMITS → midpoints LOCK STATIC for rest of Cycle 14
- [ ] Cycle 15+ auto-tune per Matt pre-ratification #1 STATIC mutability (production-season evidence-driven)

### Part 4 — 2-layer gate runtime (~3-4 days)

- [ ] **Mechanical pass** evaluation: gauntlet_pass_rate >70% within ±25% of cohort midpoint per cohort + Phase 4 archive_status='ACCEPTED'
- [ ] **Cohesion pass** evaluation: consume Phase 5 ExportFactionCluster cohesion fields (cluster_compactness + cosine_similarity_max + diversity_flag + phase7_gate_status + regeneration_fired + downstream ai_tell_compliance_score from F-C Wave 3 Seam 2) per gandalf spec § 2 + jack-ryan canonical `3d4eda5`; cohesion-judge confidence ≥0.75 (jack-ryan canonical lock) + ai_tell_compliance_score ≥0.70 (forward-compat for Wave 3 F-C)
- [ ] **HELD verdict** state machine: 2-retry-per-kit (C-1 cohesion fail) + 1-retry-per-cluster (C-2/C-3 cluster-level fails) + no-retry-for-mechanical-fail (Phase 4 already rejected)
- [ ] **D-1 RESET BETWEEN ATTEMPTS:** per-kit HELD retry budgets RESET to fresh budget at start of EACH Wave 5 generation attempt (Position B retry attempts are independent calibration cycles; a kit that hit 2 retries on attempt 1 starts fresh on attempt 2)
- [ ] NO silent re-roll loops; every retry logs to Discipline #43 audit input (across all attempts; audit log accumulates per Wave 5 cycle)

### Part 5 — Phase 7 verdict emission (~2-3 days)

- [ ] Phase7KitVerdictLog DDL per jack-ryan canonical `3d4eda5` (per-cell bounding compliant)
- [ ] Phase7ClusterAggregateLog DDL per jack-ryan canonical `3d4eda5`
- [ ] Verdict emission to ExportFactionCluster.phase7_gate_status (canonical / placeholder) + kit_archive row updates
- [ ] Discipline #43 design-quality audit input: HELD verdict log structure per jack-ryan canonical specification

### Part 6 — Smoke-test + Position B composition (~1-2 days)

- [ ] Smoke-test Phase 7 IMPL against historical telemetry (D11+D12 era) before first-Wave-5-season fires
- [ ] Verify Position B audit-gate WAIT semantics: Phase 7 verdict feeds INTO Discipline #43 + Gate-2 audit BEFORE canonical commit
- [ ] Verify STATIC midpoints prevent gaming across iterative attempts
- [ ] Composition with Position B retry semantics (audit feedback → recalibrate Phase 7 thresholds at next attempt — but STATIC midpoints LOCK first-Wave-5-season; thresholds themselves DON'T re-tune)

### Risks + Watch Items (per failure-modes register § 5)

- F-5 joint-gate threshold drift watch
- F-10 spatial-gauntlet integration gap (closes with this dispatch)
- D-5 joint-gate theological drift (per Discipline #11 at faith-holy cohesion evaluation)
- F-1 math methodology drift watch (cohort midpoint median estimator under different substrate distributions)

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- [ ] All tests PASS (existing + new Phase 7 bridge + verdict emission)
- [ ] Tag at completion: `gamora/v1.7-phase-7-implementation-1`
- [ ] MIGRATION.md per ADR-004 for gauntlet_pass_rate column addition
- [ ] Append completion record to this dispatch with: bridge module location + EXPLAIN QUERY PLAN captures + smoke-test pre-Wave-5 results + Discipline #41/#42/#44/#45/#46 verifications
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria

- [ ] gauntlet_pass_rate column added + MIGRATION.md
- [ ] Bridge module operates kit_archive ACCEPTED → gauntlet_sim.py encounter sweep
- [ ] Cohort KPM measurement implemented per jack-ryan median canonical
- [ ] 2-layer gate runtime operational (mechanical + cohesion + HELD state machine)
- [ ] Phase 7 verdict emission to ExportFactionCluster + kit_archive
- [ ] Discipline #43 audit log structure implemented
- [ ] Smoke-test against historical telemetry PASS
- [ ] Position B composition verified
- [ ] Discipline #46 § 7 per-cell bounding integrity preserved
- [ ] Discipline #45 vocabulary lock CLEAN (no class/role/archetype non-exempt vocab)
- [ ] Tag cut + AGENT_STATE.md updated + MIGRATION.md
- [ ] Completion record + commit + push

## Out of scope

- Do NOT touch Phase 4 impl (gamora Dispatch 3A complete)
- Do NOT touch Phase 5 cohesion-judge LLM (gandalf+star-lord Wave 3 seams)
- Do NOT touch Wave 1.5 Stage 3 (rocket complete)
- Do NOT touch THEMATIC_REGISTRY (gandalf complete)
- Do NOT touch A/B comparison protocol (gandalf separate dispatch at Wave 5 close)
- Do NOT enter Wave 5 production-season execution (separate dispatch fires post this lands)
- Do NOT modify Phase 7 spec or canonical thresholds (gandalf Seam 1 / jack-ryan Seam 2 sealed)

## Open questions for gamora

- **Q-P7-IMPL-1:** Bridge module venue — `simulation/phase7_bridge.py` vs `simulation/spatial_gauntlet/phase7_bridge.py` vs other? Your judgment per existing simulation/ structure
- **Q-P7-IMPL-2:** gauntlet_sim.py kit input format — does kit_archive row structure feed directly OR does it need transformation? Compose with rocket's Wave 1.5 Stage 3 kit output format if relevant
- **Q-P7-IMPL-3:** Backfill semantics for pre-existing kit_archive rows (NULL gauntlet_pass_rate acceptable until Wave 5 fires; verify no downstream consumers panic on NULL)
- **Q-P7-IMPL-4:** Discipline #45 vocabulary check — any new module names / DDL columns / public API terms need grep audit at impl close

## References

- Matt 2026-05-27 F-10 routing ratification
- Gamora Pattern A-light Q1-Q5 finding (architecture clarification)
- Gandalf Phase 7 Seam 1 spec (`0cf4e3d`)
- Jack-ryan Phase 7 Seam 2 canonical thresholds (`3d4eda5`)
- Gamora Dispatch 3A Phase 4 (`749d5aa`; kit_archive ACCEPTED signal)
- Star-lord Dispatch 3B Seam 3 (`bf7f659`; ExportFactionCluster fields)
- Wave 5 dispatch (`2026-05-27-wave-5-production-season-dispatch.md`; this dispatch gates Wave 5)
- Engineering-disciplines.md § Discipline #1 / #11 / #18 / #42 / #43 / #44 / #45 / #46

---

## Completion record

(append on completion)
