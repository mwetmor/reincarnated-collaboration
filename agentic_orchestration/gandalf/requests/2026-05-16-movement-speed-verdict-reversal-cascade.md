# Gandalf request to knight-rider — movement-speed verdict reversal cascade (4 dispatches)

**From:** gandalf
**To:** knight-rider
**Date:** 2026-05-16 (Day 4 close)
**Authorized by:** Matt directly, 2026-05-16 Day 4 ("Please take all of the recommended actions" + prior "We need to wire the actual end game player value, end game monster value and end game player:monster movement speed ratio all into the sim and the final JSON packet")
**Type:** Cascade commission — four dispatches with priority sequencing for VS2a-gating end-game-anchored movement speed

**Source artifacts:**
- `canonical/story/movement-speed-baseline.md` § "VERDICT REVERSAL 2026-05-16 (Day 4 close)" — operational values
- `agentic_orchestration/gandalf/findings/2026-05-16-export-dto-stage-b-silent-drop.md` — Track A precondition
- `canonical/16-project-roadmap.md` § VS2a — framing change (end-game playtest anchor)

---

## Why this cascade exists

Matt's verdict reversal: VS2a ships end-game-anchored movement speed (Option B), not mid-game pre-implementation (Option A). Direct quote:
> *"We need to wire the actual end game player value, end game monster value and end game player:monster movement speed ratio all into the sim and the final JSON packet. No point playing a game which is not ran through the sim."*

This supersedes the Option-A lock from this morning. Four downstream dispatches needed; priority sequencing matters because Track 1 precondition-blocks Track 4.

**Operational values to land:**
- `PlayerClass.movement_speed` default: 8.0 m/s (was 5.75)
- `Monster.movement_speed` trash: 5.75 m/s (unchanged)
- `Monster.movement_speed` fast archetypes: 7.5 m/s (top of locked range; was 6.6 in current rocket smoke)
- AI_SPEED_MULTIPLIER: 0.719 (was 0.767)
- Fast-archetype:player ratio: 0.938 (was 0.880)
- Sim consumption (gamora Gate 3b): VS2a-gating (was post-VS2a tight follow)

---

## Track 1 — Star-lord Stage B export-DTO fix (CRITICAL precondition)

**Status:** Commission already filed at `agentic_orchestration/gandalf/requests/2026-05-16-star-lord-export-dto-stage-b-fix-and-r11b.md`.

**Re-prioritization under verdict reversal:** Previously HIGH; now **CRITICAL VS2a-GATING**. Reasoning: drax must consume engine-emitted MS from JSON (no longer hardcoding mid-game values). If Stage B drops the field at boundary, drax cannot consume; cascade fails. Sequence ahead of star-lord's full queue (Stage 2 cosmological vocab → V2.4 → V2 regen → Stage 3 cipher migration).

**Estimated effort:** 6-10h. Already scoped in source commission.

---

## Track 2 — Rocket schema-default-update + monster fast-archetype tuning

**Owner:** rocket
**Estimated effort:** 1 session (~2-3h)
**Status:** PENDING — knight-rider authoring

### Scope

1. **Update `PlayerClass.movement_speed` default** from `5.75` to `8.0` in `class_schema.py` (or equivalent). End-game gear-only value per Option B lock.

2. **Update `Monster.movement_speed` defaults** per Option B:
   - Trash tier: stays `5.75` (unchanged; monsters don't get gear MS scaling)
   - Fast archetypes: bump to `7.5` (top of locked range; end-game fast monsters at parity with old mid-game player baseline)
   - Named bosses: gamora design-call per locked-values table (no schema-default change)

3. **Update `_monster_to_dict` in `season_writer.py:292-314`** to include `movement_speed` (the Stage A gap surfaced in finding `2026-05-16-export-dto-stage-b-silent-drop.md` Track B). This was already scoped in the Stage B finding commission; folding into this Track 2 dispatch for coordination.

4. **Smoke verify:** regen smoke season; confirm player classes emit `movement_speed=8.0`; trash monsters `5.75`; fast archetypes `7.5`.

5. **MIGRATION.md entry** documenting the Option-B value updates + Stage-A monster-emit gap close.

6. **Intermediate tag:** `rocket/v1.x-movement-speed-option-b-defaults`.

### Required reading

- `canonical/story/movement-speed-baseline.md` § "VERDICT REVERSAL" (operational values)
- `agentic_orchestration/gandalf/findings/2026-05-16-export-dto-stage-b-silent-drop.md` (`_monster_to_dict` gap context)

---

## Track 3 — Gamora Gate 3b sim consumption (VS2a-gating)

**Owner:** gamora
**Estimated effort:** ~1.5-2 weeks gamora per movement-speed-baseline.md § "Simulation consumer (gamora scope)"
**Status:** PENDING — knight-rider authoring; **VS2a-gating per verdict reversal**

### Scope

1. **Sim consumes `Monster.movement_speed` + `PlayerClass.movement_speed`** rather than implicit defaults. Kiting modeling extended to include positional state; chase-margin math active.

2. **3-band distance state** (close / medium / long) per range-profile + monster-aggression-state.

3. **AI_SPEED_MULTIPLIER 0.719 consumed in sim** as the trash-to-player ratio; fast-archetype ratio 0.938 also modeled.

4. **Convergence-loop integration** — balance loop sees MS as variable affecting kiting effectiveness, time-to-contact, AOE-evasion-window. Per-class convergence may shift modestly; expected and acceptable.

5. **Smoke + regen:** fresh season generated with sim-MS-aware balance loop; convergence_report shows non-zero MS-related state on per-class telemetry.

6. **Decisions-log:** gamora reports any meaningful modifier-range shift attributable to MS-consumption; if material, knight-rider drafts amendment to the B10.4 Option 2 calibration epoch entry.

### Required reading

- `canonical/story/movement-speed-baseline.md` § "Reconciliation with the AI speed multiplier" (background on multiplier semantics)
- `canonical/story/engine-balance-stewardship.md` § Gate 3 Recommendation 3b (the original framing)
- gamora's existing AGENT_STATE.md flag for Stage A2 movement-speed sim extension

### Cross-seam coordination

- **Track 2 (rocket schema defaults) ships first** — gamora needs the new 8.0/7.5 default values present in PlayerClass/Monster instances
- **Track 1 (Stage B export-DTO fix) coordinates** — gamora reads from internal engine model directly, so does NOT depend on Track 1; but cross-validation against export packet (Discipline #11 attribution check) recommended

---

## Track 4 — Drax demo MS consumption from engine JSON

**Owner:** drax
**Estimated effort:** ~1-2 sessions (~3-5h)
**Status:** PENDING — depends on Track 1 + Track 2 landing
**Precondition:** Stage B export-DTO fix (Track 1) MUST land first; engine-emitted `movement_speed` must reach consolidated `classes.json` + `monsters.json` via fixed ExportClass + ExportMonster DTOs

### Scope

1. **Remove hardcoded values** from `reincarnated-demo/src/world/movement.ts`:
   - Player base 5.75; early 6.0; mid 7.5; late 8.0 — remove from constants
   - Monster trash 5.75; fast archetypes 6.6 — remove from constants
   - PLAYER_MOVE_SPEED_PX / AI_SPEED_MULTIPLIER — derive from JSON, not hardcoded

2. **Consume engine-emitted MS via JSON:**
   - Read `class.movement_speed` from `classes.json` per-class
   - Read `monster.movement_speed` from `monsters.json` per-monster
   - Apply `PIXELS_PER_METER = 48` conversion (constant; drax-side)
   - Derive AI_SPEED_MULTIPLIER per-encounter from monster vs player MS (not a global constant any more; per-monster ratio computed at runtime)

3. **Verify rendered behavior matches sim:** after rocket Track 2 ships + Stage B fix, regen a fresh season, confirm:
   - Player rendered at 8.0 m/s × 48 = 384 px/s
   - Monster trash rendered at 5.75 m/s × 48 = 276 px/s
   - Fast-archetype monsters at 7.5 m/s × 48 = 360 px/s
   - Per-encounter chase margin matches sim expectations

4. **Arena re-dimensioning check:** drax flagged Case A arena-tightness at 7.5 m/s player. At 8.0 m/s player (Option B), tightness compounds. Confirm whether ELLIPSE_RX needs further adjustment (currently authorized at 960 px per drax v0.10 follow-on flag); recommend per playtest feel.

5. **Intermediate tag:** `drax/v0.x-movement-speed-engine-consumption`.

### Required reading

- `canonical/story/movement-speed-baseline.md` § "VERDICT REVERSAL" (operational values)
- `canonical/story/movement-speed-baseline.md` § "Demo consumer (drax scope)" (PIXELS_PER_METER convention)

---

## Track 5 — Knight-rider decisions-log supersession entry

**Owner:** knight-rider authoring; jack-ryan Gate 1; Matt approval
**Estimated effort:** ~1-2h knight-rider draft + Gate 1 review + commit
**Status:** PENDING — sequenced after Track 2 + Track 3 ship (so entry reflects landed state, not pending-commitment)

### Scope

1. **Draft decisions-log entry** at `reincarnated-engine/design/decisions/decisions-log.md`:
   - **Title:** "2026-05-16: Movement-speed baseline rebased to end-game anchor (Option B) — Option A SUPERSEDED; sim consumption (Gate 3b) becomes VS2a-gating"
   - **Decision:** lock end-game-anchored values per `movement-speed-baseline.md` § "VERDICT REVERSAL" table; supersede earlier-same-day Option A entry
   - **Rationale:** Option A papered over schema-emit-without-consumer drift; Option B closes drift by forcing sim consumption + actual end-game values; playtest signal now reflects sim-validated state, not mid-game approximation
   - **Implications named:** VS2a is end-game playtest, not progression-curve playtest; early-game-feel deferred to Playtest Cycle 1; gear MS still B12 full audit Stage A2; AI_SPEED_MULTIPLIER rebased from 0.767 to 0.719
   - **Cross-reference:** `canonical/story/movement-speed-baseline.md` § "VERDICT REVERSAL"; this cascade commission

2. **Jack-ryan Gate 1** per CHANGELOG dispatch rubric (strategy doc producing decisions-log entries; INVOKE Gate 1)

3. **Matt approves; knight-rider commits**

### Cross-seam coordination

- Drafted after Tracks 2 + 3 land (decisions-log captures landed state)
- Track 1 + Track 4 may still be in flight when entry commits — that's fine; the cascade is sim-side + generation-side committed; demo-side is consumer

---

## Sequencing summary

```
PRIORITY ORDER:

Track 1 (Stage B export-DTO fix; star-lord)  ─┬─► Track 4 (drax demo JSON consumption)
                                              │
Track 2 (rocket schema defaults; rocket)  ────┼─► Track 4
                                              │
Track 3 (gamora Gate 3b sim consumption) ─────┘   Track 5 (knight-rider decisions-log entry)
                                                  ↑
                                                  └── after Tracks 2 + 3 land
```

**Critical path:** Track 1 (Stage B fix) blocks Track 4; otherwise tracks parallelize.

**VS2a-gating items:** Track 1, Track 2, Track 3, Track 4. All must close before VS2a ships.

**Total estimated cascade effort:** ~3-4 weeks across seams (largest item is gamora Track 3 at ~1.5-2 weeks).

---

## What this commission unblocks

- VS2a end-game-anchored playtest validation
- Sim-and-demo agreement on movement values (no drift between balance-tuned state and player-experienced state)
- Forward-compat for B12 full audit (Stage A2) — gear MS scaling builds on the engine-emitted MS foundation
- Closes Drift-9 ("Q2 movement empirically unknown") per `canonical/story/drift-audit.md`
- Operationalizes Gate 3 Recommendation 3b per `canonical/story/engine-balance-stewardship.md`

---

— gandalf, 2026-05-16 (Day 4 close)
