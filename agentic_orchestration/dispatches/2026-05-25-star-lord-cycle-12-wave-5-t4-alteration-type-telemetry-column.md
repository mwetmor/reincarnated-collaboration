# Dispatch — 2026-05-25 — star-lord — Cycle 12 Wave 5 t4_alteration_type telemetry column (gamora follow-on)

**From:** knight-rider
**To:** star-lord (engine operational-pipeline seam — export/output/telemetry/llm)
**Approved by:** KR autonomous in-scope decision per Cycle 12 scope-doc § 1 (cross-seam follow-on per gamora MIGRATION.md § v1.28) + skip-confirmation re-auth 2026-05-25
**Estimated effort:** ~10-15 min star-lord (small additive schema change)
**Acceptance:** `t4_alteration_type` column (TEXT NULL) added to `class_fight_loadouts` telemetry table; backward-compat for pre-Wave-5 rows (NULL); no regression on existing telemetry round-trip

---

## Context

Gamora cycle-12 Wave 5 sim combatant integration ✅ COMPLETE (commit `e421800`; tag `gamora/cycle-12-wave-5-sim-combatant-integration-2026-05-25`). Per `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.28, gamora added `t4_alteration_type` to fight_log key vocabulary; star-lord follow-on is to surface this in `class_fight_loadouts` telemetry table so downstream T4 post-mortem analysis can filter/group by alteration type.

This is a small additive schema change — backward-compat for pre-Wave-5 rows (NULL).

---

## Required reading before starting

- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.28 (gamora cross-seam obligation source)
- `~/Games/reincarnated-engine/src/reincarnated/telemetry/` (star-lord seam state; class_fight_loadouts table schema)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.5-cycle-12-wave-5-off-hand-contract-export (star-lord prior amendment context)
- `agentic_orchestration/dispatches/2026-05-25-gamora-cycle-12-wave-5-sim-combatant-integration.md` (gamora completion record — context for column)
- ADR-004 MIGRATION.md cross-seam requirement

---

## Math-before-code (per Discipline #1)

No new math. Additive schema column.

---

## Scope (star-lord telemetry column extension)

- [ ] Add `t4_alteration_type` column (TEXT NULL) to `class_fight_loadouts` table per gamora MIGRATION.md § v1.28
- [ ] Update telemetry write path: when sim emits fight_log with `t4_alteration_type` (per gamora gauntlet integration), star-lord stamps the column on insert
- [ ] Backward-compat: pre-Wave-5 fight_log records (without t4_alteration_type) → NULL column value
- [ ] Round-trip smoke: 1 fight_log with t4_alteration_type populated → telemetry insert → SELECT round-trip → column present + value correct
- [ ] Round-trip smoke null-case: 1 fight_log without t4_alteration_type → insert → NULL column
- [ ] No regression on existing telemetry round-trip tests
- [ ] MIGRATION.md export-seam update: extend with new entry documenting telemetry schema change for downstream T4 post-mortem queries
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `star-lord/cycle-12-wave-5-t4-alteration-type-telemetry-column-2026-05-25`

---

## Out of scope

- Other Cycle 12 schema changes (separate dispatches; already landed for class JSON export — this is telemetry-side only)
- Alteration emission contract changes (LOCKED at rocket L6)
- Performance benchmarking
- v1.1+ items

---

## Acceptance criteria

- [ ] `t4_alteration_type` column present in `class_fight_loadouts` schema
- [ ] Telemetry write path populates column from fight_log when present
- [ ] Backward-compat NULL handling verified
- [ ] Round-trip smoke (populated + null) PASS
- [ ] No regression on existing telemetry tests
- [ ] MIGRATION.md updated per ADR-004
- [ ] AGENT_STATE.md updated
- [ ] Tag: `star-lord/cycle-12-wave-5-t4-alteration-type-telemetry-column-2026-05-25`
- [ ] Auto-commit + auto-push per star-lord seam authorization (CLAUDE.md addendum + Cycle 12 push-per-wave LIVE)

---

## Cross-seam impact

Round-trip: REQUIRED per Principle 6 — telemetry round-trip + downstream consumers (T4 post-mortem analysis queries). MIGRATION.md update documents the column for downstream awareness.

---

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.28 (gamora source)
- `agentic_orchestration/dispatches/2026-05-25-gamora-cycle-12-wave-5-sim-combatant-integration.md`
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.5
- ADR-004

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** KR autonomous in-scope decision per Cycle 12 scope-doc § 1 (cross-seam follow-on per gamora MIGRATION.md § v1.28) + skip-confirmation re-auth 2026-05-25
**Status:** FIRE — small follow-on amendment; fires in parallel with jack-ryan Gate-2 on full new engine

**Matt-touch sequence:** star-lord completes → KR captures in state file → on Gate-2 on full new engine PASS → KR drafts + auto-closes Cycle 12 wind-down per skip-confirmation re-auth → T4 post-mortem readiness milestone
