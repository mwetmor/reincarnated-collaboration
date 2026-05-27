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
