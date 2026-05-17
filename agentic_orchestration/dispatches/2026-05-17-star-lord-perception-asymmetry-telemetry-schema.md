# 2026-05-17 — star-lord — Perception asymmetry telemetry schema (dual hit-counts)

**Authority:** Gandalf L3 § 8 binding decision per Matt L3 standing delegation 2026-05-17.
**Type:** Pattern A (short task) — ~0.5 day.
**Predecessor:** gandalf v1.5 asymmetric perceived AOE radius briefing.
**Parallel-safe with:** rocket v1.9 perception_asymmetry module dispatch (different scope; both can run simultaneously).

---

## Why this matters

Per gandalf § 5: the perception asymmetry's effect on KPM is **measurable** via telemetry. Engine emits `aoe_hit_count` per AOE cast; gamora's narrow-slice work adds the asymmetry consumption (escape AI uses apparent_radius; damage at true_radius). The KPM gauntlet validation test wants to see how many "spillover" hits occur — monsters that escaped the apparent radius but caught damage at true_radius.

This dispatch extends the telemetry schema to carry dual hit-counts per AOE cast.

---

## Required reading (in order)

1. `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` — full briefing; § 5 KPM gauntlet validation hook
2. Your prior telemetry work — `reincarnated-engine/src/reincarnated/export/` (telemetry schema + emit logic)
3. `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — your prior §v2/§v3 entries
4. `reincarnated-engine/src/reincarnated/simulation/fight_engine.py` (read-only; gamora's seam; just understand where AOE-cast events fire to know where dual hit-count emission lands)

---

## Scope

### Item 1 — Schema extension

Per gandalf § 4 telemetry obligation, the AOE-cast event needs two optional fields:

- `true_radius_hit_count: int | None` — monsters damaged at true_radius (the actual damage-effective radius)
- `apparent_radius_hit_count: int | None` — monsters that would have been damaged if damage resolved at apparent_radius (informational; perception-aware audit)

For player AOEs: `apparent < true`, so `apparent_radius_hit_count <= true_radius_hit_count`. The delta is "spillover" — monsters that "barely escaped" visually but still took damage.

For enemy AOEs: `apparent > true`, so `apparent_radius_hit_count >= true_radius_hit_count`. The delta is "buffer" — monsters that appeared to be in danger but were safe.

### Item 2 — Emit logic (lightweight; gamora consumes)

You don't fire the emit yourself (that's gamora's seam — she'll wire the dual-count emission inside her narrow-slice reactive-escape dispatch as a downstream consumer of this schema). Your job is to:

- Define the schema fields
- Document the cross-seam contract (gamora emits; you define the channel)
- Add validation: if either field is present, both should be; never one-of-pair

### Item 3 — Telemetry export updates

If the existing telemetry export pipeline serializes events to disk / DB / JSON:
- Ensure the new optional fields are correctly serialized when present
- Backward-compatible: events without these fields continue to load cleanly
- Discipline #12 semantic shift documentation: events post-this-dispatch may carry dual hit-counts where pre-this-dispatch events do not

### Item 4 — MIGRATION.md update

Author `export/MIGRATION.md` §v3.x entry:
- New optional schema fields
- Consumer obligations (gamora emits; D14 calibration consumes; demo doesn't consume directly)
- Discipline #11 attribution: telemetry events should include `engine_version` or `engine_git_sha` so dual-hit-count presence vs absence is interpretable

### Item 5 — Hive log + tag

- STATE entry
- HANDOFF → gamora (you've defined the schema; she emits when narrow-slice ships)
- Tag `star-lord/v1.4-perception-asymmetry-telemetry-schema-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT modify fight_engine.py (gamora's seam; consumes your schema)
- ❌ DO NOT modify demo or loadout code
- ❌ DO NOT change existing telemetry events (additive change only)
- ❌ DO NOT extend scope to other telemetry additions; surface as OBSERVATION

---

## Acceptance criteria

- [ ] Schema fields defined (true_radius_hit_count, apparent_radius_hit_count)
- [ ] Validation rule: both-present-or-both-absent
- [ ] Serialization handles both
- [ ] Backward-compatible (old events load cleanly)
- [ ] Unit tests for serialization + validation
- [ ] `export/MIGRATION.md` updated
- [ ] Hive-log STATE + HANDOFF → gamora
- [ ] Tag `star-lord/v1.4-perception-asymmetry-telemetry-schema-1`

---

## Smoke test expectation

- Schema definition imports cleanly
- Test event with both fields serializes + deserializes correctly
- Test event with neither field serializes + deserializes correctly
- Test event with only one field fails validation (fail-loud)

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). Apply cross-repo race-condition discipline.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 standing delegation + gandalf § 8 binding. Estimated 0.5 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Completed by:** star-lord
**Engine commit:** `0fce61a` (feat(telemetry): V2.5 perception-asymmetry AOE-cast event schema)
**Tag:** `star-lord/v1.4-perception-asymmetry-telemetry-schema-1` @ `0fce61a`
**Tests:** 38/38 pass (`tests/test_telemetry_v25_aoe_cast.py`). 147 prior telemetry tests: all pass. 0 regressions.

### Acceptance criteria — all met

- [x] Schema fields defined (`true_radius_hit_count`, `apparent_radius_hit_count`) — `aoe_cast_event.py`
- [x] Validation rule: both-present-or-both-absent — `AoeCastEvent.validate()` raises `ValueError` fail-loud
- [x] Serialization handles both — `to_db_row()` / `from_db_row()` round-trips in 4 test scenarios
- [x] Backward-compatible — old events (NULL hit-counts) load cleanly; both-absent state handled gracefully
- [x] Unit tests for serialization + validation — 38 tests across 4 classes
- [x] `export/MIGRATION.md` updated — §V2.5 entry with consumer obligations + KPM acceptance SQL
- [x] Hive-log STATE + HANDOFF → gamora — appended to `hive-mind/phase-1-p1-log.md`
- [x] Tag `star-lord/v1.4-perception-asymmetry-telemetry-schema-1` — cut

### Files modified

| File | Change |
|---|---|
| `src/reincarnated/telemetry/aoe_cast_event.py` | NEW — AoeCastEvent dataclass |
| `src/reincarnated/telemetry/migrations.py` | _V2_5 migration + MIGRATIONS entry |
| `src/reincarnated/telemetry/recorder.py` | SCHEMA_VERSION 2.4→2.5; record_aoe_cast_event(); NullRecorder stub |
| `tests/test_telemetry_v25_aoe_cast.py` | NEW — 38 tests |
| `tests/test_telemetry_v24.py` | equality pin → >= 2.4 range check (forward-compat) |
| `src/reincarnated/export/MIGRATION.md` | §V2.5 entry |
| `src/reincarnated/export/AGENT_STATE.md` | Session entry + header updated |

### Cross-seam handoffs dispatched

- **Gamora:** HANDOFF posted in hive log — emission wiring contract established. Requires rocket v1.9 (`foundation/perception_asymmetry.py`) to land first.
- **D14 calibration:** KPM gauntlet acceptance SQL in MIGRATION.md §V2.5 (player spillover ratio 5-15%; enemy buffer ratio 10-25%).

### Open observation (surfaced per dispatch "surface as OBSERVATION" rule)

The `record_event` generic stub on `TelemetryRecorder` (line 642) remains a no-op. Now that `record_aoe_cast_event` exists as a typed method, future event types should follow the same pattern (typed method, not generic stub). The generic stub can be retired when all planned event types have typed methods. Flag to knight-rider for future dispatch if needed.
