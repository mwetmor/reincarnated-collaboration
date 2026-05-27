# Dispatch — 2026-05-27 — star-lord — Cycle 13 Wave 4 Export Schema Update (Gates Gamora W4G.5)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-05-27 + Cycle 13 framing brief § 4.1 KR autonomous + gamora SC-7 FULL closure cross-seam flag (commit `6ebf6c8`) — "Star-lord export schema update needed BEFORE W4G.5 — route to KR for Wave 4 star-lord dispatch"
**Estimated effort:** 1-3 hrs export schema update + round-trip smoke
**Acceptance:** export schema updated to handle Wave 4 gamora sim cycling output fields (per SC-7 framework FULL § 9 closure); round-trip smoke per ADR-004; tagged commit; gamora W4G.5 unblocked

## Context

Gamora SC-7 methodology consultation FULL closure (commit `6ebf6c8`) flagged ONE cross-seam dependency requiring KR routing:

> **Cross-seam flag (1):** Star-lord export schema update needed before W4G.5 — route to KR for Wave 4 star-lord dispatch.

W4G.5 (per SC-7 sub-wave structure) = archive insertion + quality report. This requires export schema able to handle Wave 4 gamora sim cycling output fields. Star-lord seam owns export/output/telemetry/llm; export schema is star-lord canonical.

This dispatch fires the star-lord export schema update concurrently with gamora Wave 4 implementation (which will use stub-write pattern at W4G.5 if star-lord output not yet landed; integrates when landed). NON-BLOCKING on gamora W4G.0-W4G.4 sub-waves.

**Per gamora SC-7 FULL closure (commit `6ebf6c8`; output at `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` § 9):** review SC-7 § 9 for specific Wave 4 gamora output fields that need export schema support. Examples likely include:
- Per-fight outcome data with cohort × scope dimensions
- KPM median per cell × cohort × scope × progression node
- Quality report metadata (T4 regeneration rate; quarantine rate; sub-gate failure counts)
- Reference encounter integration outputs

Star-lord seam-owner determines specific schema spec per SC-7 § 9 + own canonical knowledge of existing export schema.

## Required reading before starting

1. `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` § 9 FULL Closure (SC-7 output; specific field requirements for Wave 4 gamora sim cycling)
2. `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-13-sc-7-methodology-consultation-full-execution.md` (gamora SC-7 completion record)
3. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended (D60+D62+D84+D85 sim methodology architecture context)
4. `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` amended (Wave 3 T4 scope-dimension; new T4CandidateV2 fields)
5. `agentic_orchestration/operating-procedures/star-lord.md` (operating procedure; export/output/telemetry/llm seam authority)
6. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1.2 + #11 + Principle 6)
7. Existing engine export code paths (your seam): `reincarnated-engine/src/reincarnated/export/` for current export schema
8. Engine telemetry: `reincarnated-engine/src/reincarnated/telemetry/` for sim-result telemetry capture

## Math-before-code (schema update; not algorithm)

NOT applicable — schema update only.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip required.** Star-lord export schema update IS a cross-seam contract change. Wave 4 gamora sim cycling implementation consumes export schema for sim-result writeout. Round-trip smoke required per ADR-004.

**Round-trip smoke:** sample Wave 4 sim-result data structure (per SC-7 § 9 specs) writes to export; round-trip verify field-presence + type-consistency + downstream loadable.

**MIGRATION.md required** per ADR-004 if schema field renamed / removed from existing export schema. Document new fields per Wave 4 scope.

## Scope

- [ ] Review SC-7 § 9 FULL Closure for specific Wave 4 gamora output field requirements
- [ ] Identify export schema gaps (new fields needed; renamed fields; deprecated fields)
- [ ] Implement export schema update per Wave 4 needs:
  - Sim-result writeout fields (per-fight outcome + cohort × scope dimensions)
  - KPM median writeout per stratification (cell × cohort × scope × progression node)
  - Quality report metadata (T4 regeneration rate; quarantine rate; sub-gate failure counts; degenerate-state-detection flags)
  - Reference encounter integration outputs (from SC-6 WU bundled; commit `ee15c96`)
- [ ] Backward compatibility — preserve existing export schema fields; ADD new; rename/remove only if SC-7 explicitly requires
- [ ] Round-trip smoke: sample Wave 4 data structure → export → load → verify field-presence + type-consistency
- [ ] MIGRATION.md per ADR-004 (document new fields)
- [ ] AGENT_STATE.md updated per session end

### Discipline compose-check

- [ ] #1.2 code-citation — cite existing export schema entry points (file + line)
- [ ] #11 empirical inspection — post-script empirical count assertions (Wave 4 fields added: N; existing fields preserved: M; verify empirically)
- [ ] **WARN-pattern PRESERVED status maintenance** — per Wave 3 Gate-2 milestone; post-script empirical count assertions 100% accurate target preserved
- [ ] Principle 6 round-trip — Wave 4 sample data round-trip smoke PASSes

## Acceptance criteria

- [ ] Export schema updated per SC-7 § 9 Wave 4 field requirements
- [ ] Backward compatibility preserved
- [ ] Round-trip smoke per Principle 6 PASSes
- [ ] MIGRATION.md updated per ADR-004
- [ ] Post-script empirical count assertions per WARN-pattern preservation
- [ ] Tagged commit per star-lord convention: `star-lord: Cycle 13 Wave 4 export schema update for gamora W4G.5 sim cycling outputs (per SC-7 FULL closure 6ebf6c8)`
- [ ] AGENT_STATE.md updated

## Out of scope (explicit non-goals)

- Gamora Wave 4 sim cycling implementation (separate gamora dispatch; firing in parallel)
- Rocket Wave 4 spec-driven gear gen (separate)
- Phase 5 cohesion coalescence LLM seam work (Cycle 14)
- Loadout app changes (drax seam; Wave 4+ planning)
- Telemetry DB migration v2.16 ALTER TABLE (separate; per ADR-006)
- Modifying canonical docs (cross-seam gandalf authority)
- Modifying simulation code (gamora seam)
- decisions-log entries

## Open questions for the agent to resolve

- Field-naming convention for new Wave 4 fields: follow existing export schema convention OR define new namespace for Wave 4 sim cycling outputs; your seam-owner call
- Backward-compat verification depth: spot-check existing exports OR full re-test; recommend spot-check per session length constraints
- Telemetry DB v2.16 migration: separate dispatch per ADR-006 (Matt-explicit); does NOT fire this dispatch; flag if SC-7 implies it

## References

- `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` § 9 (SC-7 FULL closure source)
- `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-13-sc-7-methodology-consultation-full-execution.md` (gamora dispatch)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8
- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` (Wave 3 scope-dimension fields)
- `agentic_orchestration/operating-procedures/star-lord.md`
- Engine export/telemetry code (your seam)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1.2 + #11 + Principle 6)

---

**Cycle:** 13
**Wave:** 4 export schema update (gates gamora W4G.5)
**Gates:** gamora W4G.5 archive insertion + quality report
**Priority:** P1 — concurrent with gamora Wave 4 implementation; gates final W4G.5 sub-wave

---

## Completion record

**Completed:** 2026-05-27
**Author:** star-lord
**Commit:** `8dbb808` — `feat(star-lord): Cycle 13 Wave 4 export schema update for gamora W4G.5 sim cycling outputs (per SC-7 FULL closure 6ebf6c8)`

### Schema fields added: 6 (ExportAlterationOutput +5 scope; ExportSimCyclingQualityReport NEW)

**ExportAlterationOutput** — 5 additive nullable scope-dimension fields (code-cite: `t4_category_schema.py:379-384` + `T4CandidateV2.to_dict()` lines 458-462):
- `t4_scope` (str|None) — T4Scope enum value; Stage B vocabulary guard added
- `scope_downscale_factor` (float|None) — 1/sqrt(class_chain_count) for CHARACTER_WIDE B/C
- `scope_prior_weight` (float|None) — cohort prior from COHORT_SCOPE_PRIORS selection
- `scope_weighted_score` (float|None) — net_synergy_score × (1 + prior_weight)
- `scope_projection_data` (dict|None) — per-cohort scores + I1 all-negative flag

**ExportSimCyclingQualityReport** — NEW model (21 fields; 14 required + 7 optional). Written to `exports/<season_id>/sim_cycling_quality_report.json` at W4G.5 by `write_sim_cycling_quality_report()`. Loaded by `load_sim_cycling_quality_report()`.

### Backward compatibility: PRESERVED

All 5 scope fields default `None`. Pre-Wave-3 class JSON omitting scope keys reads back with all 5 as `None` — no Pattern P7 WARN. Prior export round-trip baseline: 82/82 PASS (42 Cycle 12 Wave 5 + 40 Cycle 11). No existing schema fields renamed or removed.

### Round-trip smoke (Principle 6): 36/36 PASS (new) + 82/82 PASS (prior) = 118/118 total PASS

Groups: (A) scope field pass-through (5) + (B) backward compat (5) + (C) model_dump() round-trip (4) + (D) Stage B validator type guards (6) + (E) ExportSimCyclingQualityReport write/load (11) + (F) empirical count assertions (5).

Test file: `tests/test_cycle13_wave4_export_schema_round_trip.py` (36 tests)

### MIGRATION.md: UPDATED — § v1.6-cycle-13-wave-4-scope-dimension-export prepended

`/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`

### Gamora W4G.5 gate status: UNBLOCKED

Gamora Wave 4 implementation can integrate at W4G.5 using `write_sim_cycling_quality_report()` + `load_sim_cycling_quality_report()` from `reincarnated.export`. The `ExportSimCyclingQualityReport` model is importable from `reincarnated.export`.

### Discipline compose-check

- [x] #1.2 code-citation — cited `t4_category_schema.py:379-384`, `T4CandidateV2.to_dict()` lines 458-462, `t4_scope_selector.py:285-299`, `t4_scope_selector.py:317-338` throughout
- [x] #11 empirical inspection — post-script empirical count assertions 100% accurate (ExportAlterationOutput field count = 14; ENDGAME_ENCOUNTER_CATALOG count = 18); WARN-pattern PRESERVED
- [x] Principle 6 round-trip — Wave 4 sample data round-trip smoke 36/36 PASS; prior baseline 82/82 PASS

### Open flags for KR routing

- Telemetry DB v2.16 migration: out of scope per dispatch; gamora's t4_alteration_type column (commit `7cfff770`) is already in prod. No new migration required for this export schema update.
- Drax quality badge display: `t4_regeneration_rate` + `quarantine_rate` + `archive_insertion_count` from `sim_cycling_quality_report.json` — separate drax Wave 4+ dispatch when gamora W4G.5 first cycle produces data.
- D25 cross-season learning: `kpm_medians_per_cell` + `cohort_scope_distribution_observed` fields are Cycle 14 retrospective inputs — routing note for knight-rider.
