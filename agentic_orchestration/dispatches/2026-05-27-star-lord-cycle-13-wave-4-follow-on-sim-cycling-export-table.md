# Dispatch — 2026-05-27 — star-lord — Cycle 13 Wave 4 Follow-On (Sim Cycling Export Table + Sentinel + Ingest Stub)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-05-27 + gamora Wave 4 Track B completion record (commit `c956a4b`) + MIGRATION.md § v1.29 flag + jack-ryan Wave 4 BUNDLED Gate-2 PASS verdict (commit `888ffca`) next-action sequence routing
**Estimated effort:** 30-60 min small follow-on (sentinel + sim cycling export table + ingest stub)
**Acceptance:** sentinel file at `export/wave4_schema_landed.sentinel` + T4 sim cycling export table added + ingest stub for `simulation/output/wave4_sim_results_*.json`; tagged commit; round-trip smoke; MIGRATION.md updated

## Context

Gamora Wave 4 Track B sim cycling implementation (commit `10a6193`) flagged star-lord follow-on at MIGRATION.md § v1.29:

> **Star-lord follow-on (MIGRATION.md § v1.29):** create `export/wave4_schema_landed.sentinel` + add T4 sim cycling export table + ingest `simulation/output/wave4_sim_results_*.json` — gates on star-lord agent completing concurrent dispatch.

Star-lord prior Wave 4 export schema dispatch (commit `8dbb808`) added `ExportAlterationOutput` 5 scope fields + `ExportSimCyclingQualityReport` model. This follow-on adds the sentinel + sim-result-specific export table + ingest stub for actual W4G sim cycling JSON outputs.

Jack-ryan Wave 4 Gate-2 (commit `888ffca`) PASS confirmed Wave 4 architecture; this follow-on is the small post-Gate-2 cleanup landing the gamora-flagged routing requirement.

## Required reading before starting

1. `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-13-wave-4-sim-cycling-implementation-w4g.md` (Track B completion record; § v1.29 flag context)
2. `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.29 (gamora-flagged follow-on details)
3. `reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` (W4G primary; output format reference)
4. `reincarnated-engine/src/reincarnated/export/` (your prior Wave 4 schema work commit `8dbb808`; export module)
5. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-4-gate-2-track-b-gamora.md` (Wave 4 Track B Gate-2 PASS)
6. `agentic_orchestration/operating-procedures/star-lord.md`
7. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1.2 + #11 + Principle 6)

## Math-before-code (small schema follow-on; no algorithm)

NOT applicable.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip required.** New T4 sim cycling export table + ingest stub IS cross-seam contract addition. Backward compatible (additive); MIGRATION.md per ADR-004.

**Round-trip smoke:** sample W4G sim-result JSON → ingest stub → export table → re-load → verify field-presence + type-consistency.

## Scope

- [ ] Create sentinel file at `reincarnated-engine/src/reincarnated/export/wave4_schema_landed.sentinel` (per gamora MIGRATION.md § v1.29 flag)
- [ ] Add T4 sim cycling export table per gamora `T4SimRecord` schema (see `simulation/t4_sim_cycling.py`)
- [ ] Add ingest stub function for `simulation/output/wave4_sim_results_*.json` glob pattern
- [ ] Backward compatibility: NO breaking changes to existing export schema (commit `8dbb808` Wave 4 schema preserved)
- [ ] Round-trip smoke per Principle 6: sample sim-result JSON → ingest → export → re-load
- [ ] MIGRATION.md update with § v1.7 (or appropriate version) follow-on entry per ADR-004
- [ ] AGENT_STATE.md updated per session end

### Discipline compose-check

- [ ] **#1.2 code-citation** — cite gamora `T4SimRecord` schema location (file + line)
- [ ] **#11 empirical inspection** — post-script empirical count assertions (sim cycling export table fields added: N; sentinel file presence: 1; existing schema preserved); 100% accurate per WARN-pattern MAINTAINED status
- [ ] **Principle 6 round-trip** — sample sim-result round-trip PASSes

## Acceptance criteria

- [ ] Sentinel file created
- [ ] T4 sim cycling export table added
- [ ] Ingest stub for `wave4_sim_results_*.json` glob
- [ ] Backward compat preserved
- [ ] Round-trip smoke PASSes
- [ ] MIGRATION.md updated per ADR-004
- [ ] Post-script empirical count assertions per WARN-pattern MAINTAINED
- [ ] Tagged commit: `star-lord: Cycle 13 Wave 4 follow-on — sim cycling export table + sentinel + ingest stub (per gamora MIGRATION.md § v1.29 + jack-ryan Gate-2 PASS 888ffca)`

## Out of scope

- Telemetry DB v2.16 migration (per ADR-006; separate Matt-explicit)
- Other Wave 5+ work
- Modifying gamora simulation code
- Modifying canonical docs
- decisions-log entries

## References

- `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-13-wave-4-sim-cycling-implementation-w4g.md`
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.29
- `reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py`
- `reincarnated-engine/src/reincarnated/export/` (your seam; prior commit `8dbb808`)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-4-gate-2-track-b-gamora.md`
- `agentic_orchestration/operating-procedures/star-lord.md`

---

**Cycle:** 13
**Wave:** 4 follow-on (post-Gate-2 cleanup)
**Gates:** Wave 4 fully cleaned-up; supports downstream Wave 5 + Cycle 14+ telemetry-ingest workflows
**Priority:** P2 — small follow-on; non-blocking on Wave 5 dispatch authoring
