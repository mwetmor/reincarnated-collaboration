# Dispatch — 2026-05-25 — star-lord — Cycle 12 Wave 5 off_hand_contract export schema extension

**From:** knight-rider
**To:** star-lord (engine operational-pipeline seam — export/output/telemetry/llm)
**Approved by:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q1 Option γ includes cross-seam wiring per Gate-2-on-L3 INFO-D) + skip-confirmation re-auth 2026-05-25 + KR autonomously orchestrates per scope-doc § 1
**Estimated effort:** ~30-60 min star-lord (synthetic-agent throughput)
**Acceptance:** Class JSON export schema extended for `off_hand_contract` field per rocket L6 emission shape (MIGRATION.md § v1.4-layer-6); round-trip smoke (rocket emit → star-lord serialize → JSON → deserialize) PASS; no regression on existing 79/79 Cycle 11 schema extensions round-trip

---

## Context

Cycle 12 Wave 5 cross-seam follow-on fan-out. Rocket Layer 6 ✅ COMPLETE + Gate-2 ✅ PASS — emission contracts authored per MIGRATION.md § v1.4-layer-6. Three cross-seam consumers now fire in parallel to integrate L6 outputs:

- **star-lord (this dispatch)**: extend class JSON export schema for off_hand_contract field
- **gamora**: sim combatant integration (required for gauntlet sim to use new engine)
- **drax**: Spirit Guide panel update (enhancement)

Per Gate-2 on L6 verdict (PASS): cross-seam emission shapes verified match MIGRATION.md exactly; consumer-side code is FOLLOW-ON to Layer 6. This dispatch is the star-lord consumer side.

---

## Required reading before starting

- **`~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`** § v1.4-layer-6 — **PRIMARY load-bearing** — documents off_hand_contract emission shape rocket emits
- `~/Games/reincarnated-engine/src/reincarnated/generation/off_hand_contract.py` (Layer 3 OffHandContract dataclass — banner/focus/talisman/tome/horn types + factory + round-trip)
- `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py` `emit_cross_seam_fields()` (Layer 6 emission function — verify shape star-lord consumes)
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-6-section-8-wireup-and-l9-refactor.md` Bucket 5 (cross-seam SC-3 emission contracts)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-4-rocket-layer-6.md` Bucket 5 (cross-seam emission verification PASS)
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 (PlayerClass.off_hand_item field shape)
- `canonical/story/off-hand-items-2026-05-24.md` § 2.3 (off-hand mechanical contract semantics)
- `~/Games/reincarnated-engine/src/reincarnated/export/` (star-lord seam state; Cycle 11 schema extensions context at commit dcfa846 + MIGRATION.md § v1.3)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #2 + #8 + #11 + ADR-004)

---

## Math-before-code (per Discipline #1)

No new math — schema extension consuming existing L6 emission shape. Math note OPTIONAL for this small dispatch (rocket judgment); if authored, document at `~/Games/reincarnated-engine/src/reincarnated/export/notes/cycle-12-wave-5-off-hand-contract-export-schema-2026-05-25.md` (or star-lord naming).

---

## Scope (star-lord schema extension)

- [ ] Inspect MIGRATION.md § v1.4-layer-6 for off_hand_contract emission shape
- [ ] Inspect rocket `emit_cross_seam_fields()` at `t4_wireup.py` for actual emission keys + values
- [ ] Extend class JSON export schema with off_hand_contract field
  - Type: dict (OffHandContract serialized form) OR null (for kits without off-hand)
  - Subfields per OffHandContract dataclass: type + buff_geometry + aura_tempo + etc. per Layer 3 SC-3 design
- [ ] Update class_balance_results / class_fight_loadouts / season_writer.py serialization paths as needed
- [ ] Round-trip smoke: representative PlayerClassV2 with off_hand_contract → star-lord JSON serialize → deserialize → field-presence + shape check
- [ ] Round-trip smoke null-case: PlayerClassV2 without off_hand_contract → serializes as null → consumer null-safe
- [ ] No regression on Cycle 11 Wave 1 schema extensions round-trip (79/79 PASS baseline)
- [ ] MIGRATION.md export-seam update: extend existing MIGRATION.md with § v1.5-cycle-12-wave-5-off-hand-contract-export entry (or star-lord naming) documenting consumer-side schema extension for downstream (loadout drax) awareness
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `star-lord/cycle-12-wave-5-off-hand-contract-export-2026-05-25`

---

## Out of scope

- Layer 6 emission contract changes (LOCKED per MIGRATION.md § v1.4-layer-6; consume as-is)
- Off-hand mechanical contract design changes (Layer 3 SC-3 LOCKED)
- Drax loadout consumer code (separate cross-seam dispatch)
- Gamora sim consumer code (separate cross-seam dispatch)
- Architectural amendments (escalate via KR per scope-doc § 5 if needed)
- v1.1+ schema items

---

## Acceptance criteria

- [ ] off_hand_contract field present in class JSON export
- [ ] Round-trip smoke PASS (populated + null cases)
- [ ] No regression on existing 79/79 Cycle 11 Wave 1 round-trip
- [ ] MIGRATION.md export-seam updated per ADR-004
- [ ] AGENT_STATE.md updated
- [ ] Tag: `star-lord/cycle-12-wave-5-off-hand-contract-export-2026-05-25`
- [ ] Auto-commit + auto-push per star-lord seam authorization (CLAUDE.md addendum + Cycle 12 push-per-wave LIVE)

---

## Cross-seam impact

Round-trip: REQUIRED per Principle 6 — star-lord emits class JSON consumed by drax loadout app. If round-trip surfaces shape issue with rocket L6 emission, flag to KR for cross-seam coordination per scope-doc § 5.

---

## References

- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4-layer-6
- `~/Games/reincarnated-engine/src/reincarnated/generation/off_hand_contract.py`
- `~/Games/reincarnated-engine/src/reincarnated/generation/t4_wireup.py`
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-6-section-8-wireup-and-l9-refactor.md`
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-4-rocket-layer-6.md`
- `canonical/story/off-hand-items-2026-05-24.md` § 2.3
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification + skip-confirmation re-auth + KR autonomously orchestrates per scope-doc § 1
**Status:** FIRE — Wave 5 parallel-fire with gamora + drax cross-seam consumers; no specialist contention

**Matt-touch sequence:** star-lord completes → KR captures in state file → integration smoke + jack-ryan Gate-2 on full new engine fires when all 3 cross-seam consumers land
