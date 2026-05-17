# Dispatch — 2026-05-16 — gamora — V2.1 per-fight field emission gap fix (post-regen-recovery cross-seam flag #1)

**From:** knight-rider (authored per star-lord regen recovery cross-seam flag — surfaced 2026-05-16 Day 4)
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4 explicit "author 2 gamora dispatches" directive
**Status:** PENDING — ACTIVE
**Estimated effort:** 1-2 sessions (~2-4 hours); bounded code-fix work — identify the V2 room runner's fight_log dict construction; add the 3 missing fields; verify smoke; intermediate tag.
**Acceptance:** V2 room runner emits all 3 v2.1 per-fight fields (`encounter_index_within_room`, `room_won`, `hp_fraction_at_encounter_start`) in fight_log dicts that get persisted to `class_fight_loadouts`. Smoke season verifies field population end-to-end (currently all 204,800 rows for season_001006 have NULL on these fields; post-fix smoke produces non-NULL). Intermediate tag; cross-seam coordination with star-lord NOT needed (star-lord's v2.1 schema + recorder are correctly wired per smoke; the gap is purely on the emission side).

---

## Context — what star-lord discovered

Per star-lord's regen recovery findings file (`agentic_orchestration/qa/findings/2026-05-16-star-lord-full-regen-post-b6-v2.md`):

> V2.1 per-fight fields (`encounter_index_within_room`, `room_won`, `hp_fraction_at_encounter_start`): **ALL NULL across all 204,800 rows** of season_001006 — this is a gamora-seam fight_log emission gap (recorder is correctly wired; smoke confirmed; the live regen's room runner did not emit these fields in fight_log dicts).

**The asymmetry:**
- Star-lord v2.1 schema (commit `92fe8f7`): SHIPPED ✓ — columns exist on `class_fight_loadouts`
- Star-lord v2.1 recorder: SHIPPED ✓ — writes the fields when present in fight_log dicts
- Star-lord v2.1 smoke test: PASSED ✓ — synthetic fight_log dicts with the fields persist correctly
- **Gamora V2 room runner: GAP** — production fight_log dicts emitted by the V2 sequential-room execution path don't include the 3 new fields

The gap is **purely in gamora's seam.** Star-lord's v2.1 + v2.2 work both confirmed via smoke; the production-path emission needs the wire-up.

## What this dispatch does

### Step 1 — Locate the V2 room runner's fight_log dict construction

Per gamora's B10 V2 implementation (intermediate tag `gamora/v1.3-b10-v2-sequential-room @ 9db2f5a`), the V2 sequential-room execution path lives in `src/reincarnated/simulation/balance_loop.py` + `src/reincarnated/simulation/fight_engine.py` + `src/reincarnated/simulation/fight_result.py`. The fight_log dict is constructed at the point where balance_loop / fight_engine emits per-fight records that get passed to the telemetry recorder.

Find the construction site(s); document the file:line where fight_log dicts are built for the V2 room execution path.

### Step 2 — Add the 3 missing fields to fight_log dict construction

For each per-encounter fight record emitted within a V2 room:

1. **`encounter_index_within_room: int`** — which encounter in the room sequence (0, 1, 2 for N=3). Source: the room runner knows the index as it iterates encounters.
2. **`room_won: bool`** (persisted as INTEGER 0/1) — did the class survive the entire room (all N encounters with HP > 0)? Source: known at room-end; back-fill the field on each encounter within the room when the room completes.
3. **`hp_fraction_at_encounter_start: float`** — HP fraction the class enters this encounter with (1.0 for encounter_0; lower for subsequent encounters under V2 HP-carryover). Source: known at encounter-start.

Wire these into the existing fight_log dict construction; star-lord's recorder already accepts the fields (per v2.1 smoke).

### Step 3 — Smoke verification

Per Discipline #2:

- Run a small smoke season (5-class V2; matches gamora's prior V2 smoke pattern)
- Query telemetry DB post-smoke:
  - `SELECT COUNT(*) FROM class_fight_loadouts WHERE season_id = '<smoke_season>' AND encounter_index_within_room IS NOT NULL;` → expected: 100% of fresh rows
  - Same for `room_won` and `hp_fraction_at_encounter_start`
  - Confirm `encounter_index_within_room` cycles [0, 1, 2] (N=3)
  - Confirm `hp_fraction_at_encounter_start` = 1.0 for encounter_0 rows; decreases monotonically within a room
  - Confirm `room_won` consistent within each (monster, iteration, fight_index) room group

### Step 4 — Tag + AGENT_STATE + completion record

- **Intermediate tag:** `gamora/v1.3-b10-v2-emission-gap-fix` at the commit closing the wire-up + smoke pass.
- AGENT_STATE.md updated
- Completion record filled at bottom of this dispatch

## Cross-seam considerations

- **Star-lord:** READ-ONLY (no star-lord changes needed). The v2.1 + v2.2 telemetry schema + recorder are correctly wired per smoke; your fix is the missing emission side. Star-lord may want to know when the fix lands so they can verify (informational only).
- **Knight-rider:** notify at completion; the fix unblocks the eventual follow-on regen (which would populate v2.1 fields on full-class roster + recover class_0011's fight rows per star-lord's 10-vs-11 triage recommendation).
- **Rocket:** out of seam.
- **Drax:** READ-ONLY downstream — Damage×TTK projection switch will benefit from populated v2.1 fields once the follow-on regen lands.

## Out of scope (explicit)

- **NO regen.** This dispatch is the code-fix only. Follow-on regen lands separately (Matt-decision per ADR-006).
- **NO star-lord-side changes.** Recorder + schema are correctly wired.
- **NO V2 mechanics re-design.** The room-runner logic stays unchanged; only the fight_log dict construction adds 3 fields.
- **NO V2.2 emission** (`observed_movement_speed`). That's the upcoming gamora Stage A2 work consuming rocket's movement_speed schema; separate dispatch chain.
- **NO wind_controller modifier 3.51 investigation.** Separate gamora dispatch (`agentic_orchestration/dispatches/2026-05-16-gamora-wind-controller-modifier-investigation.md`).

## Required reading

- `agentic_orchestration/qa/findings/2026-05-16-star-lord-full-regen-post-b6-v2.md` (star-lord's regen recovery findings — the empirical basis for this fix)
- `agentic_orchestration/dispatches/2026-05-16-gamora-b10-v2-sequential-room.md` (your own B10 V2 dispatch + completion record — the V2 mechanics you'll wire fields into)
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` §v1.4 (your own V2 source-of-truth for field semantics)
- `reincarnated-engine/src/reincarnated/simulation/math/b10-v2-sequential-room-convergence.md` (your own V2 math note)
- `agentic_orchestration/dispatches/2026-05-16-star-lord-telemetry-schema-b10-v2-fields.md` (star-lord's v2.1 dispatch — the recorder/schema source-of-truth)
- `reincarnated-engine/src/reincarnated/telemetry/recorder.py` (star-lord's seam; read-only reference; understand the consumer pattern)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke-test), #11 (attribution: cite star-lord's findings file as the empirical basis), #12 (semantic-shifting: the 3 fields become populated post-fix; a semantic shift relative to all prior regens)

## Acceptance criteria

- [ ] V2 room runner's fight_log dict construction located + documented (file:line)
- [ ] 3 new fields wired into fight_log dict: `encounter_index_within_room` (cycles 0..N-1); `room_won` (back-filled at room-end; consistent within room); `hp_fraction_at_encounter_start` (1.0 for encounter_0; decreases within room)
- [ ] Smoke season verifies 100% field population on fresh rows
- [ ] Cycle-validation: encounter_index_within_room cycles [0, 1, 2] for N=3
- [ ] Monotonic-validation: hp_fraction_at_encounter_start decreases within a room
- [ ] Consistency-validation: room_won shared across all encounters in a room group
- [ ] Intermediate tag `gamora/v1.3-b10-v2-emission-gap-fix` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `gamora/v1.3-b10-v2-emission-gap-fix` at the commit closing wire-up + smoke pass.
- **Milestone tag:** none from this dispatch. Standard ADR-003 protocol.

---

## Completion record

**Completed:** 2026-05-16 by gamora (claude-sonnet-4-6)
**Construction site (file:line):**
  - Primary binary-search V2 branch: `balance_loop.py` ~line 509 (`"loadout_json": None` → `"{}"`)
  - Rejection gate re-run V2 branch: `balance_loop.py` ~line 626 (same change)
  - Both sites are in the `if self._use_room_evaluation:` branch of `balance_class()`
**Intermediate tag:** `gamora/v1.3-b10-v2-emission-gap-fix` at commit `df717a8`
**Smoke verification summary:**
  - 5-class V2 smoke (in-memory DB, 10 fights/matchup, 10 max_iterations)
  - DB rows written: 1114 (was 0 before fix)
  - encounter_index_within_room: 1114/1114 non-null (100%)
  - room_won: 1114/1114 non-null (100%)
  - hp_fraction_at_encounter_start: 1114/1114 non-null (100%)
  - Cycle validation: encounter_index values = [0, 1, 2] ✓
  - HP validation: encounter_0 always at 1.0 HP (430 rooms) ✓
  - HP range: all values in [0, 1] ✓
  - room_won consistency: 0 violations across all room groups ✓
  - Monotonic note: hp_fraction CAN increase between encounters due to potion carryover — correct V2 behavior, dispatch's "strictly decreasing" criterion is overly strict in presence of potions
  - Full test suite: 1384 tests pass (0 regressions)
**Root cause finding (Discipline #12):**
  - The actual gap was NOT a missing field in fight_log dict construction (the 3 fields were correctly wired at `balance_loop.py` lines 493-497 and 610-614 since the V2 dispatch)
  - The gap was: `"loadout_json": None` caused recorder's `loadout_json is None → continue` guard (recorder.py line 477) to silently drop all V2 rows
  - Star-lord v2.1 smoke (test_telemetry_v21.py) masked this by injecting synthetic entries with `loadout_json` set (lines 605-606, explicit comment in test code)
  - Fix: emit `"{}"` (empty JSON string) instead of `None` — passes the guard; means "no gear sampled"
  - MIGRATION.md §v1.4 updated + §v1.5 added documenting the semantic correction
**Notes for knight-rider:**
  - Cross-seam impact: star-lord recorder.py is UNCHANGED. The `loadout_json is None` guard is correctly V1 behavior; V2 now correctly bypasses it. No star-lord follow-on needed.
  - This fix unblocks the next full regen: season_001006 fight rows (or any fresh regen) will now produce non-NULL values for all 3 V2.1 per-fight fields
  - The star-lord v2.1 smoke's synthetic-entry workaround (test_telemetry_v21.py lines 605-606) remains correct as a unit test; it was probing recorder field-writing in isolation, which was correct. The gap was the integration path.
  - Regen sequencing: the emission fix is now in main. Matt authorization per ADR-006 needed for the next regen run that would populate season data with correct V2.1 fields.
