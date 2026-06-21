# Dispatch — 2026-06-21 — star-lord — typed-threat telemetry (death-cause-with-element)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-06-21 — publish-go on the typed-resistance recal wave.
**Estimated effort:** ~0.5 wave. **Concurrent** with rocket/gamora — author the additive field + MIGRATION; the round-trip smoke needs gamora's live typed death channel, so coordinate the field shape with gamora before her calibration validation needs it.
**Acceptance:** an additive telemetry field makes the now-live TYPED death channel observable (death-cause-with-element / damage-by-type); existing consumers byte-identical; MIGRATION + round-trip smoke pass.

> **Parent MASTER (Gate-1 ENDORSE):** `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`. This pickup is the star-lord section extracted verbatim. Gate-1 finding: `qa/findings/2026-06-21-recal-wave-typed-resistance-MASTER-gate1.md`.

## Context

The recal wave restores a real player-death channel routed through the kernel resolver with TYPED damage (each signature boss does its element; the kit's per-element resist mediates). Today survival = 1.000 instrument-wide — invisible because nothing dies. To tune the typed band AND verify "matching matters," the death channel must be OBSERVABLE: which element killed the kit, and how much damage by type. Without it, gamora's "a matched kit eases" is unmeasurable.

## Required reading before starting
1. `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md` — **§8** (star-lord handoff), **§3** (why typed telemetry is needed to verify reward-for-matching).
2. `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md` — the 0a spike (the typed damage path the telemetry observes).

## NON-NEGOTIABLE GUARDS (carry verbatim)
- **Additive only** — no field renamed/removed; existing consumers byte-identical (keeps the offensive instrument's banked artifacts intact).
- **Content emission HELD until the two-axis joint close** — this telemetry supports the wave's validation; it does not unlock emission.

## Scope
- [ ] Additive telemetry capturing the now-live TYPED death channel: **death-cause WITH element** and/or **damage-by-type** — richer than the typeless version, NEEDED to tune the typed band and verify matching matters. Your call on exact shape at build (converge with gamora on what her band-validation reads).
- [ ] **Additive only** — see guard.
- [ ] MIGRATION.md (star-lord ↔ gamora boundary, ADR-004).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `star-lord/v-typed-threat-telemetry-N`

## Cross-seam contract change? (Principle 6 — YES, round-trip REQUIRED)
ADDS fight_log/telemetry fields. Round-trip smoke: a production-path fight that kills the player with a TYPED skill → assert death-cause-with-element + damage-by-type present and populated through the gamora→star-lord boundary into the season JSON.

## Out of scope (explicit non-goals)
- The `_DEFERRED_PROXY_BINS` lift / 25% proxy emission (Matt-reserved, separate).
- Any non-additive schema change.

## Open questions for you to resolve (and document)
- Exact additive field shape (death-cause-with-element vs damage-by-type vs both) — converge with gamora on what her typed-band validation needs to read.

## References
- Typed-resistance design-half: `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md`
- 0a resolver spike: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md`
- Coordinating MASTER: `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`
- Disciplines: #11 empirical inspection, #12 semantic-shift

---

## Completion record

**Completed:** 2026-06-21
**Tag:** `star-lord/v-typed-threat-telemetry-1` (engine commit `d04edcc`)
**Status:** ALL SCOPE ITEMS COMPLETE — round-trip smoke PASS; push HELD per ADR-006.

### What was delivered

**Additive field:** `player_death_element` (the exact field gamora produced in `SpatialFightResult`).
No damage-by-type field added — gamora's producer does not emit per-type damage breakdown, only the
killing-blow element. Per dispatch scope: "Your call on whether to also surface damage-by-type if the
producer exposes it — converge with what's actually available on `SpatialFightResult`; do not invent
producer fields gamora didn't emit." Producer confirmed: only `player_death_element` is available.

**Three-step consumer delivery (gamora MIGRATION v1.81):**

1. **DB column** — `telemetry/migrations.py _V2_19`: `player_death_element TEXT NULL` on
   `spatial_fight_results`. Pending Matt ADR-006 production-DB auth.

2. **Persist leg** — `telemetry/spatial_recorder.py _INSERT_SQL`: `player_death_element` added
   after `wr_1d_fight`. Read via `getattr(result, "player_death_element", None)` — brownfield-safe.

3. **Export packet** — `export/schemas.py`: `ExportTypedDeathTelemetry` (Pydantic BaseModel,
   fields: fight_id/class_id/scenario_id/player_death_element/player_survived) +
   `build_typed_death_telemetry(result)` factory (gamora→star-lord export boundary).

**MIGRATION.md:** `simulation/MIGRATION.md §v1.81` consumer delivery record appended;
`export/MIGRATION.md §v1.81` new entry authored.

### Round-trip smoke results (Discipline #11 empirical — all 3 mandatory cases)

| Case | player_death_element | DB | export player_survived | Result |
|---|---|---|---|---|
| Typed-element death | `"fire"` | `"fire"` | `False` | **PASS** |
| Armor death | `"armor"` | `"armor"` | `False` | **PASS** |
| Survival | `None` | `NULL` | `True` | **PASS** |

Full chain: `SpatialFightResult` → `_INSERT_SQL` → DB → `build_typed_death_telemetry(row_stub)` → `ExportTypedDeathTelemetry` — **PASS**

All 7 canonical typed elements (fire/water/earth/wind/lightning/holy/shadow) — **PASS**

### Test results
19 new tests / 59/59 total `round_trip_spatial_telemetry.py` PASS; 0 regressions (4752-test suite
baseline unchanged).

### Additive-only guard confirmed
No field renamed/removed. `_INSERT_SQL` positional ordering append-only. `validate()` unchanged.
All 20+2 pre-v2.19 fields round-trip identically in post-v2.19 DB. Existing consumers byte-identical.

### Open item for Matt (wave close)
`_V2_19` migration requires Matt ADR-006 authorization for production DB apply. Same standing gate
as v2.17/v2.18. Specced + ready; no DB write without explicit auth.
