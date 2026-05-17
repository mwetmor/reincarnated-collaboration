# Dispatch — 2026-05-16 — star-lord — Spatial-data telemetry persistence (v2.3 schema; per spatial-data cascade Step 4)

**From:** knight-rider (authored per spatial-data-jsonschema decisions-log entry committed `303258c` Step 4 of 6-step implementation cascade)
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 ("draft and fire others who are idle as we need to move on to VS2a")
**Status:** PENDING — ACTIVE
**Estimated effort:** ~2-3h per gandalf's commission Step 4 estimate; parallel-compatible with rocket spatial-data schema-additive emission (Step 2)
**Acceptance:** Telemetry schema v2.3 migration adds spatial-resolution telemetry columns; recorder wired to write fields when present in fight_log dicts; defensive nulls (consistent with v2.0 → v2.1 → v2.2 → v2.3 pattern); smoke test verifies persistence; MIGRATION.md v2.3 entry; intermediate tag.

---

## Context — Step 4 of spatial-data cascade

Per the 2026-05-16 spatial-data-jsonschema decisions-log entry (committed `303258c`) 6-step implementation cascade:

> Step 4: Star-lord telemetry persistence — ~2-3h; parallel-compatible with Step 2

This dispatch is **parallel-compatible with rocket's spatial-data schema-additive emission (Step 2)** — your work adds telemetry persistence for spatial-resolution outcomes. Rocket's Step 2 + gamora's Step 3 (Stage A2 sim consumption; LOAD-BEARING per Matt directive) eventually produce per-fight spatial-resolution data that this dispatch's telemetry captures.

**Important context:** the spatial-data schema is locked but rocket Step 2 hasn't fired yet (queued behind rocket's current dispatch chain). For your work:
- The schema fields exist in code (when rocket Step 2 lands)
- The recorder needs columns to persist them
- Defensive nulls handle the pre-rocket-Step-2 state (recorder accepts None for spatial fields; writes NULL)

## What this dispatch does (v2.3 telemetry migration)

Following the pattern from your v2.1 + v2.2 schema work (per `dispatches/2026-05-16-star-lord-telemetry-schema-b10-v2-fields.md` + `2026-05-16-star-lord-telemetry-observed-ms-emission.md`):

### Step 1 — Schema addition (v2.3 telemetry migration)

Append a new migration entry to `reincarnated-engine/src/reincarnated/telemetry/migrations.py` (v2.3):

**class_fight_loadouts** (per-fight spatial-resolution outcomes):

```sql
ALTER TABLE class_fight_loadouts ADD COLUMN encounter_floor_width_m REAL;
ALTER TABLE class_fight_loadouts ADD COLUMN encounter_floor_height_m REAL;
ALTER TABLE class_fight_loadouts ADD COLUMN encounter_kind TEXT;
ALTER TABLE class_fight_loadouts ADD COLUMN intended_combat_range_band TEXT;
ALTER TABLE class_fight_loadouts ADD COLUMN spatial_complexity_tier TEXT;
ALTER TABLE class_fight_loadouts ADD COLUMN player_spawn_x_m REAL;
ALTER TABLE class_fight_loadouts ADD COLUMN player_spawn_y_m REAL;
ALTER TABLE class_fight_loadouts ADD COLUMN movement_profile TEXT;
```

All NULL-permitting (consistent with v2.x pattern; historical rows pre-migration carry NULL; fresh rows post-migration carry actual values).

**Field semantics:**
- `encounter_floor_width_m`, `encounter_floor_height_m` — per-encounter floor dimensions (meters); per gandalf's per-encounter-kind dimension library (32.7×14m trash / 28×28m elite / 40×24m boss / 50×30m act-boss)
- `encounter_kind` — string enum: `"trash" | "elite" | "boss" | "act_boss"` etc.
- `intended_combat_range_band` — string enum: `"close" | "mid" | "far" | "mixed"`
- `spatial_complexity_tier` — string enum: `"open_arena" | "obstacle_arena" | "corridor"` per gandalf's spatial-data jsonschema doc
- `player_spawn_x_m`, `player_spawn_y_m` — player spawn coordinates (meters; per-encounter floor-center origin)
- `movement_profile` — string enum from initial 6: `"walking" | "running" | "crawling" | "floating" | "flying" | "teleporting"`

**Note:** these fields capture the SPATIAL CONTEXT of each fight (where it happened); they do NOT capture full per-tick spatial state (that would be a separate higher-resolution telemetry table; out of scope here).

### Step 2 — Recorder wiring

Update `recorder.py` (or whichever module owns `record_class_fight_loadouts`):

- Accept the 8 new spatial fields from the fight_log dict; write in the INSERT when present
- **Defensive nulls:** if a fight_log dict lacks the fields (pre-rocket-Step-2 + pre-gamora-Step-3 paths), write NULL — do NOT error
- **Source field:** rocket's spatial-data schema emission (post-Step-2) populates these; until then, NULL

### Step 3 — Smoke test

Per Discipline #2:
- Existing tests in `tests/test_telemetry.py` pass
- New unit test for v2.3 migration + recorder wiring
- Pre-rocket-Step-2 defensive-null smoke: 5-class smoke season with NO spatial-data fields in fight_log → recorder writes NULL for all 8 fields; no errors
- Post-rocket-Step-2 emulation smoke: synthetic fight_log dicts WITH spatial-data fields → recorder persists; verify field values match input

### Step 4 — MIGRATION.md v2.3 entry

Append to `reincarnated-engine/src/reincarnated/export/MIGRATION.md`:

- v2.3 entry with 8 new spatial-data fields + semantics
- Cross-references to spatial-data-jsonschema decisions-log entry (`303258c`) + gandalf's `canonical/story/spatial-data-jsonschema.md`
- Cross-references to rocket Step 2 (spatial-data schema-additive emission; not yet authored — will be) + gamora Step 3 (Stage A2 sim consumption; LOAD-BEARING per Matt directive)
- Downstream consumer notes for drax (Step 5 PixiJS demo consumption; consumes spatial-data fields for per-encounter rendering)

### Step 5 — Intermediate tag + AGENT_STATE + completion record

- Tag: `star-lord/v1.3-telemetry-schema-v2.3-spatial-data`
- AGENT_STATE.md updated
- Completion record at bottom of this dispatch filled

## Cross-seam considerations

- **Rocket:** READ-ONLY upstream (rocket spatial-data schema-additive emission per cascade Step 2 — separate future dispatch; supplies the fields at generation time)
- **Gamora:** READ-ONLY future consumer (Stage A2 sim consumption per cascade Step 3 — LOAD-BEARING per Matt directive; gamora's Stage A2 work emits per-fight spatial-resolution data that your recorder persists)
- **Drax:** READ-ONLY downstream (Step 5 PixiJS demo consumption; consumes spatial-data fields for per-encounter rendering decisions)
- **Knight-rider:** notify at completion; telemetry v2.3 available for downstream consumers; v2.3 DB migration to live data/telemetry.db requires separate Matt ADR-006 authorization (same pattern as v2.1 + v2.2)

## Out of scope (explicit)

- **NO rocket-side schema emission** — separate cascade Step 2 dispatch
- **NO gamora-side sim consumption** — separate cascade Step 3 dispatch
- **NO drax-side rendering** — separate cascade Step 5 dispatch
- **NO production DB migration** — Matt ADR-006 authorization required separately
- **NO per-tick spatial state telemetry** — higher-resolution; out of scope (this dispatch captures per-fight spatial context, not per-tick)
- **NO existing v2.x migration re-architecture** — append v2.3 entry following the pattern

## Required reading

- 2026-05-16 spatial-data-jsonschema decisions-log entry (committed `303258c`) — Step 4 of 6-step cascade is your scope
- `canonical/story/spatial-data-jsonschema.md` (gandalf source-of-truth for schema fields + semantics)
- Your own prior v2.1 + v2.2 dispatches (pattern reference)
- `reincarnated-engine/src/reincarnated/telemetry/migrations.py` + `recorder.py` (target files; v2.1 + v2.2 entries are pattern reference)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke-test); #11 (attribution); #12 (semantic-shifting: spatial-data fields become populated post-rocket-Step-2 + post-gamora-Stage-A2; semantic shift)

## Acceptance criteria

- [ ] migrations.py v2.3 entry added; 8 new columns on class_fight_loadouts
- [ ] Recorder wired to write 8 fields with defensive null handling
- [ ] Existing telemetry tests pass; new v2.3 unit test passes
- [ ] Pre-rocket-Step-2 defensive-null smoke verifies NULL writes (no errors)
- [ ] Post-rocket-Step-2 emulation smoke verifies field persistence
- [ ] MIGRATION.md v2.3 entry filed (cross-references spatial-data entry + gandalf source-of-truth + rocket Step 2 + gamora Step 3)
- [ ] Intermediate tag `star-lord/v1.3-telemetry-schema-v2.3-spatial-data` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-telemetry-schema-v2.3-spatial-data` at the commit closing migration + recorder + tests pass.
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16
**Migration version (v2.3):** Registered in `MIGRATIONS` list at position 13 (after v2.2); `_V2_3` migration string with 8 ALTER TABLE statements
**Intermediate tag:** `star-lord/v1.3-telemetry-schema-v2.3-spatial-data` at commit `0149bfa`
**Smoke status:** PASSED — 25/25 new tests in `tests/test_telemetry_v23.py`; 62/62 prior telemetry tests pass; full suite clean
**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — v2.3 entry appended

**Acceptance criteria check:**
- [x] migrations.py v2.3 entry added; 8 new columns on class_fight_loadouts
- [x] Recorder wired to write 8 fields with defensive null handling (`entry.get(field)` → NULL)
- [x] Existing telemetry tests pass (62/62); new v2.3 unit tests pass (25/25)
- [x] Pre-rocket-Step-2 defensive-null smoke: 5 classes × 3 fights → all 15 rows, all 8 columns IS NULL, no errors
- [x] Post-rocket-Step-2 emulation smoke: synthetic fight_log dicts WITH spatial fields → all 15 rows, all 8 columns 100% non-null, values match input exactly
- [x] MIGRATION.md v2.3 entry filed with cross-references to `303258c`, gandalf source-of-truth, rocket Step 2, gamora Step 3, drax Step 5
- [x] Intermediate tag `star-lord/v1.3-telemetry-schema-v2.3-spatial-data` cut
- [x] AGENT_STATE.md updated
- [x] Knight-rider notified at completion (this record)

**Notes for knight-rider:**

1. **V2.3 DB migration requires Matt ADR-006 authorization** — same pattern as V2.1 + V2.2. Schema is in `migrations.py` and applies on the next `apply_schema_migrations()` call. Live `data/telemetry.db` remains at its current version until authorized.

2. **Recorder is ready for rocket Step 2** — no recorder changes required when rocket's cascade Step 2 lands. The fight_log dict key contract is established (`encounter_floor_width_m`, `encounter_floor_height_m`, `encounter_kind`, `intended_combat_range_band`, `spatial_complexity_tier`, `player_spawn_x_m`, `player_spawn_y_m`, `movement_profile`). Rocket emits them; recorder picks them up automatically.

3. **Discipline #9 fix bundled in** — `test_telemetry_v22.py`'s `test_schema_version_is_22` hardcoded equality pin (`== "2.2"`) was updated to a `>= 2.2` range check (following the V2.1 test's pattern). Pre-existing fragility; fixing it now prevents future migration additions from breaking the prior test. No functional change to recorder or schema.

4. **Gamora Step 3 is the load-bearing step** — until gamora Stage A2 ships, all 8 columns carry NULL in fresh rows. The telemetry infrastructure is ready; the population signal comes when gamora's spatial-aware sim lands.
