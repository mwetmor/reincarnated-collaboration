# Dispatch — 2026-05-16 — star-lord — Telemetry schema v2.1: B10 V2 room-evaluation fields

**From:** knight-rider (authored per gamora's B10 V2 dispatch completion record cross-seam HIGH flag; Matt-approved 2026-05-16 Day 4)
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 (per knight-rider recommendation surfaced after gamora B10 V2 completion)
**Status:** PENDING — ACTIVE
**Estimated effort:** 1 session (~2-3 hours); straightforward schema-additive migration + recorder wiring + smoke test. No conceptual math required (Discipline #1 N/A); attribution clarity per gamora's MIGRATION.md is the load-bearing reference.
**Acceptance:** Six new telemetry fields land via migrations.py v2.1; recorder writes them when fight_log dicts carry the values; smoke test confirms end-to-end persistence; MIGRATION.md updated; next full regen capable of capturing B10 V2 room-evaluation metrics.

---

## Context — why this dispatch exists

Gamora's B10 V2 dispatch closed 2026-05-16 with intermediate tag `gamora/v1.3-b10-v2-sequential-room @ 9db2f5a` pushed to origin. Per gamora's MIGRATION.md §v1.4 (new file at `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`), the V2 sequential-room semantics introduce six new data points that the existing telemetry schema cannot capture:

**Three new fields on `class_fight_loadouts`** (per-fight rows; emitted from fight_engine):
- `encounter_index_within_room` (INTEGER) — which encounter in the room sequence the row represents (0..N-1; N=3 per V2 lock)
- `room_won` (INTEGER 0/1) — whether the class survived the entire room of N encounters (not just this individual encounter)
- `hp_fraction_at_encounter_start` (REAL) — HP fraction entering this encounter (1.0 for encounter 0 of a room; lower for subsequent encounters under V2 carryover)

**Three new fields on `class_balance_results`** (per-class convergence rows; emitted from balance_loop):
- `use_room_evaluation` (INTEGER 0/1) — whether the binary search used room-level WR semantic (V2) vs encounter-level (V1)
- `room_winrate` (REAL) — per-room non-pack WR achieved at convergence (the V2 binary-search target)
- `room_pack_winrate` (REAL) — per-room pack WR observed at the converged modifier (the AOE-differential metric the spec calls out)

**Why this dispatch is the critical-path item before the next full regen:**

A full regen at the current main HEAD (post B10.4 Option 2 + post rocket B6 pre-work + post gamora B10 V2) would write per-fight rows under V2 semantics — but the schema cannot persist the new V2 context. Without these fields:
- The compounded B14.5 V1 + B6 + V2 modifier compression observed in gamora's V2 smoke (mean |mod-1.0| = 0.3175) cannot be measured on a full season — only smoke
- Drax's `Damage × Time-to-Kill` viz pivot (queued separately) cannot consume per-room metrics
- B10 V2's AOE-differential goal (`room_pack_winrate ≈ 1.0` per gamora's V2 smoke) cannot be confirmed on a full regen
- Cross-seam attribution between B6 pre-work and B10 V2 (Discipline #13b territory) cannot be done without per-room data

## What this dispatch does

### Step 1 — Schema migration (v2.1)

Append a new migration to `reincarnated-engine/src/reincarnated/telemetry/migrations.py` (current version per the telemetry-tier1 dispatch was V2.0). New version: **v2.1** (or whichever version number is next per your seam's convention).

Add the six columns per the gamora MIGRATION.md §v1.4 specification:

**class_fight_loadouts:**
```sql
ALTER TABLE class_fight_loadouts ADD COLUMN encounter_index_within_room INTEGER;
ALTER TABLE class_fight_loadouts ADD COLUMN room_won INTEGER;
ALTER TABLE class_fight_loadouts ADD COLUMN hp_fraction_at_encounter_start REAL;
```

**class_balance_results:**
```sql
ALTER TABLE class_balance_results ADD COLUMN use_room_evaluation INTEGER;
ALTER TABLE class_balance_results ADD COLUMN room_winrate REAL;
ALTER TABLE class_balance_results ADD COLUMN room_pack_winrate REAL;
```

All six are NULL-permitting (consistent with the Tier-1 pattern — historical rows pre-migration carry NULL; fresh rows post-migration carry actual values).

### Step 2 — Recorder wiring

Update `reincarnated-engine/src/reincarnated/telemetry/recorder.py` (or whichever module owns the relevant `record_*` functions per your seam):

- `record_class_fight_loadouts` (or equivalent): accept the three new fields from the fight_log dict; write them in the INSERT when present.
- `record_class_balance_results` (or equivalent): accept the three new fields from balance_loop output; write them in the INSERT when present.

**Defensive nulls:** if a fight_log dict lacks the new fields (e.g., when called from a V1 code path that's still operative for some reason), write NULL — do NOT error. This preserves backward compatibility through any V1 code paths that may still exist.

### Step 3 — Smoke test

Per Discipline #2 (smoke-test discipline):

1. **Unit-level:** existing tests in `tests/test_telemetry.py` (or equivalent) pass.
2. **End-to-end:** run a small smoke season (5 classes, like gamora's V2 smoke) against the patched recorder. Query the resulting telemetry DB and verify:
   - All 6 new columns exist on the target tables
   - Fresh rows from the smoke have non-NULL values in all 6 (because the smoke uses V2 semantics; gamora's code emits the values)
   - Per-encounter rows show `encounter_index_within_room` cycling 0/1/2 (N=3) per gamora's room semantic
   - `hp_fraction_at_encounter_start` decreases monotonically within a room (carryover working) and resets to 1.0 at room boundary
   - `room_won` is consistent: all encounters within a room share the same value (survived-room vs died-in-room)
   - `use_room_evaluation = 1` for all V2 convergence rows
   - `room_winrate` ≈ 0.50 per the V2 binary-search target (from gamora's V2 math note §2)
   - `room_pack_winrate` ≈ 1.000 per the V2 smoke observation (AOE differential achieved)

### Step 4 — MIGRATION.md

Append the v2.1 entry to `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (or wherever the telemetry/export MIGRATION.md lives — your seam's convention). Cover:

- Six new fields with semantics
- Cross-reference to gamora's `simulation/MIGRATION.md` §v1.4 as the source-of-truth for field semantics
- Cross-reference to gamora's B10 V2 math note for the V2 convergence semantic
- Downstream consumer note for drax: when drax's `Damage × TTK` projection pivot lands, it should consume `room_won` + `hp_fraction_at_encounter_start` for room-level damage normalization

### Step 5 — AGENT_STATE + completion record

Update `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` (or telemetry/AGENT_STATE per your seam's convention):
- v2.1 telemetry schema migration shipped
- B10 V2 room-evaluation fields persisted
- Cross-seam flag CLOSED (gamora's HIGH flag from `simulation/MIGRATION.md` §v1.4)
- summary_formatter.py `convergence_winrate` display already FIXED at commit `6d108df` (this dispatch closes the related flag from gamora's V2 completion record that incorrectly listed it as still-open)

Fill in the completion record at the bottom of this dispatch.

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-telemetry-schema-v2.1` at the commit closing migration + recorder + tests pass.
- **Milestone tag:** none from this dispatch.
- Standard ADR-003 protocol: confirm with knight-rider before any milestone tag.

## Cross-seam considerations

- **Gamora:** READ-ONLY consumer of the new fields via `fight_log` dict construction in balance_loop / fight_engine. Gamora's MIGRATION.md §v1.4 is the source-of-truth for field semantics; star-lord implements the persistence side. If during implementation you find a field-semantic ambiguity, file a finding and route to gamora via knight-rider — do NOT modify gamora's seam.
- **Drax:** downstream consumer for the eventual `Damage × TTK` viz pivot. No coordination required during this dispatch; drax's pivot is a separate follow-on dispatch.
- **Rocket:** out of seam.
- **Knight-rider:** notify at completion. When this lands, the next full regen of `season_001005` (or a new season) becomes capable of capturing V2 room-evaluation metrics + B6 pre-work modifier compression on a full-class roster. That regen authorization is Matt-decision territory; not part of this dispatch.

## Out of scope (explicit)

- **Full regen of season_001005 (or any season).** This dispatch makes the schema capable of capturing the next regen's output; running the regen itself is a separate dispatch (Matt-authorization required).
- **Modification of gamora's seam** (balance_loop, fight_engine, fight_result). The fields you persist must already be present in the fight_log dict gamora emits; if a field is missing, file a finding for gamora.
- **Drax `Damage × TTK` projection pivot.** Downstream consumer dispatch; separate.
- **B6 pre-work isolation experiment.** Cross-component attribution between B6 and V2 is a separate Discipline #13b question; not commissioned here.
- **summary_formatter.py changes.** Already fixed at commit `6d108df`; this dispatch closes the cross-seam flag, not the code.
- **Engine_version, seasonal_element_name, convergence_wall_time_seconds.** Pre-existing flagged telemetry gaps per ADR-006 (Matt-approval required); separate.

## Required reading

- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` §v1.4 (gamora's source-of-truth for field semantics — your authoritative reference)
- `reincarnated-engine/src/reincarnated/simulation/math/b10-v2-sequential-room-convergence.md` (gamora's V2 math note — convergence semantic context)
- `agentic_orchestration/dispatches/2026-05-16-gamora-b10-v2-sequential-room.md` (gamora's V2 dispatch + completion record)
- `agentic_orchestration/dispatches/2026-05-14-star-lord-telemetry-tier1.md` (your own prior telemetry schema work — V2.0 pattern reference)
- `reincarnated-engine/src/reincarnated/telemetry/migrations.py` (your target for the v2.1 migration)
- `reincarnated-engine/src/reincarnated/telemetry/recorder.py` (your target for recorder wiring)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke-test), #11 (attribution), #12 (semantic-shifting — V2 IS a semantic shift)

## Acceptance criteria

- [ ] migrations.py v2.1 entry added; six new columns created (3 on each target table)
- [ ] Recorder wired to write the six fields when present in fight_log / balance result dicts
- [ ] Defensive nulls (no error if fields absent — backward compatibility)
- [ ] Existing telemetry tests pass
- [ ] Smoke season (5-class V2 smoke) end-to-end verified: 6 columns populated; semantics correct (encounter_index cycling, hp_fraction decreasing within room, room_won consistency, room_winrate ≈ 0.50, room_pack_winrate ≈ 1.000)
- [ ] MIGRATION.md v2.1 entry filed (cross-references gamora's MIGRATION.md §v1.4)
- [ ] Intermediate tag `star-lord/v1.3-telemetry-schema-v2.1` cut
- [ ] AGENT_STATE.md updated (includes summary_formatter.py flag closure note)
- [ ] Knight-rider notified with: tag hash, migration version, smoke-status, any cross-seam flags

---

## Completion record

(To be filled in by star-lord on completion)

**Completed:**
**Migration version:**
**Intermediate tag:**
**Smoke status:**
**MIGRATION.md entry:**
**Cross-seam flags:**
**Notes for knight-rider:**
