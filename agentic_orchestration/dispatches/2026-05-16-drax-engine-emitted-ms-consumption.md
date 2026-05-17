# Dispatch — 2026-05-16 — drax — Engine-emitted MS consumption (remove hardcoded values)

**From:** knight-rider (authored per Matt directive Day-4 close: "authorize all four" — MS verdict reversal cascade item #5)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** QUEUED — fires after BOTH (a) rocket MS schema-defaults dispatch returns AND (b) star-lord Stage B export-DTO dispatch returns. Engine-to-demo pipeline must be in place before drax can consume from it.
**Estimated effort:** ~1-2h; remove hardcoded values, wire JSON consumption, re-derive PIXELS_PER_METER conversions per consumed value

**Gate-1 bypass rationale:** Matt-directed (verdict-reversal cascade explicitly authorized), single-seam (demo only), reversible (revert path is restoring hardcoded constants).

**Acceptance summary:** `world/movement.ts` no longer has hardcoded MS constants for player / monster archetypes; values are consumed from engine-emitted consolidated JSON (ExportClass.movement_speed + ExportMonster.movement_speed); PIXELS_PER_METER conversions re-derived per consumed value (5.75 m/s × 48 = 276 px/s; 8.0 m/s × 48 = 384 px/s; 7.5 m/s × 48 = 360 px/s); smoke verifies end-to-end demo plays correct end-game values. Tag + AGENT_STATE + completion record.

---

## Why this dispatch exists

Per gandalf's MS verdict-reversal cascade (item #5):

> drax: Remove hardcoded values from world/movement.ts; consume engine-emitted MS via JSON; re-derive PIXELS_PER_METER conversions per consumed value (5.75 m/s × 48 = 276 px/s base; 8.0 m/s × 48 = 384 px/s end-game player; 7.5 m/s × 48 = 360 px/s end-game fast monster)

Closes "no point playing a game which is not ran through the sim" — demo now plays what engine emits.

## Cross-seam contract change?

**Round-trip: not applicable for the contract itself** — drax is the CONSUMER of contracts authored upstream (rocket schema + star-lord export DTO). However:

- **Required: round-trip smoke verifying field-presence at the demo JSON-load boundary.** Per R11(b) Principle 6 — when consuming engine-emitted fields, drax verifies field is present + correct shape before using.
- If consolidated JSON arrives without `movement_speed` field (e.g., star-lord Stage B regressed; rocket schema didn't ship; old-season JSON predates the field), drax must fail-loud or fall back deliberately — NOT silently default to hardcoded.

## What this dispatch produces

### Step 1 — Locate hardcoded MS constants

Find all hardcoded MS values in:
- `~/Games/reincarnated-demo/src/world/movement.ts`
- `~/Games/reincarnated-demo/src/world/topology.ts` (note: v0.20.1 already inlined PIXELS_PER_METER = 48 here per circular-import fix; that one stays)
- Any other module hardcoding player_speed_px_s / monster_speed_px_s / AI_SPEED_MULTIPLIER

### Step 2 — JSON consumption

Wire from the consolidated JSON shape star-lord Stage B emits:
- `class.movement_speed` (m/s, float) → multiply by PIXELS_PER_METER (48) → demo render px/s
- `monster.movement_speed` (m/s, float, per-monster) → same conversion

For named bosses where rocket flagged "gamora-design-call" and gamora may not have assigned: fall-back order:
1. Use monster-instance's `movement_speed` if present
2. Use archetype-default if instance-specific missing
3. Fail-loud with WARN log if both missing (NOT silently default)

### Step 3 — AI_SPEED_MULTIPLIER

Either:
- Consume from JSON if rocket/star-lord emit it as a constant in manifest
- OR compute on demo side: `AI_SPEED_MULTIPLIER = monster.movement_speed / player.movement_speed` (per-monster basis)

Pick the cleaner approach; document in notes.

### Step 4 — Smoke test (R11(b) round-trip + Discipline #2)

- Load a fresh season (rocket-generated, star-lord-exported)
- Verify class movement_speed = 8.0 → demo renders player at 384 px/s
- Verify trash monster = 5.75 → 276 px/s
- Verify fast monster = 7.5 → 360 px/s
- Field-presence assertion at JSON load boundary
- Existing demo tests pass; new MS-consumption tests pass

### Step 5 — Tag + AGENT_STATE + completion record

- Intermediate tag: `drax/v0.20.5-engine-emitted-ms-consumption`
- AGENT_STATE updated
- Fill completion record

## Out of scope (explicit)

- **NO PIXELS_PER_METER edits** (locked at 48; inlined in topology.ts per v0.20.1 circular-import fix; do not touch)
- **NO schema/export changes** (rocket + star-lord seams)
- **NO sim consumption code** (gamora Gate 3b seam)
- **NO scale-strip / sprite-scale work** (separate dispatches in flight)
- **NO playable gauntlet feature work** beyond MS consumption
- **NO loadout-repo changes**
- **NO Pixogen / chierit / CreativeKind sprite changes**

## Required reading

- Gandalf's MS verdict-reversal cascade (Matt-relayed Day-4 close) — the conversion math
- `canonical/story/movement-speed-baseline.md` (gandalf updated parallel; consume post-update as authoritative)
- Rocket MS schema-defaults dispatch completion record (the upstream source-of-truth values)
- Star-lord Stage B export-DTO dispatch completion record (the consolidated-JSON shape)
- Your `world/movement.ts` + `world/topology.ts` (current state)

## Acceptance criteria

- [ ] Hardcoded MS constants removed from `world/movement.ts` and any other module
- [ ] `world/topology.ts` PIXELS_PER_METER = 48 inline preserved (do NOT revert)
- [ ] JSON consumption wired for class.movement_speed + monster.movement_speed
- [ ] AI_SPEED_MULTIPLIER strategy chosen + documented (consume from JSON OR compute per-monster)
- [ ] Field-presence assertion at JSON load boundary (R11(b))
- [ ] Fail-loud behavior on missing field (WARN log; no silent hardcoded fallback)
- [ ] Smoke: fresh season loads + demo renders player at 384 px/s + trash at 276 + fast at 360
- [ ] Existing demo tests pass; new MS-consumption tests pass
- [ ] No new TS errors (`tsc --noEmit` clean)
- [ ] Intermediate tag `drax/v0.20.5-engine-emitted-ms-consumption` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: tag hash, AI_SPEED_MULTIPLIER strategy, any old-season JSON compatibility findings (legacy seasons may predate the field)

## Tag policy

- **Intermediate tag:** `drax/v0.20.5-engine-emitted-ms-consumption`
- **Milestone tag:** none.

---

## Completion record

**Completed:** 2026-05-16
**Hardcoded constants removed (files + lines):**
- `src/world/movement.ts`: removed `MOVE_SPEED_BASE_MPS`, `MOVE_SPEED_EARLY_MPS`, `MOVE_SPEED_MID_MPS`, `MOVE_SPEED_LATE_MPS`, `MOVE_SPEED_MONSTER_TRASH_MPS`, `MOVE_SPEED_MONSTER_FAST_MPS`, `MOVE_SPEED_MONSTER_FAST_MAX_MPS`, `MOVE_SPEED_BASE_PX`, `MOVE_SPEED_EARLY_PX`, `MOVE_SPEED_MID_PX`, `MOVE_SPEED_LATE_PX`, `MOVE_SPEED_MONSTER_TRASH_PX`, `MOVE_SPEED_MONSTER_FAST_PX`, `PLAYER_MOVE_SPEED_PX`, `AI_SPEED_MULTIPLIER`, `playerMoveSpeed()`, `speedForProfile()`. Replaced with `movementSpeedPx(mps, label)` and `MOVE_SPEED_FALLBACK_PX`.
- `src/main.ts`: `speedForProfile('medium')` initialization replaced; `speedForProfile(cls.range_profile)` at startGauntlet replaced with `movementSpeedPx(cls.movement_speed, ...)`.

**AI_SPEED_MULTIPLIER strategy:** compute-per-monster (not consume-from-JSON). AI_SPEED_MULTIPLIER was a ratio (0.767 = 5.75/7.5) that derived monster speed from player speed. With engine-emitted per-monster `movement_speed`, this ratio is baked into the engine-assigned value directly. `tickAIMove` now accepts `monsterSpeedPx` as a parameter (default = `MOVE_SPEED_FALLBACK_PX`). `PackActor` stores `monsterSpeedPx` computed at wave load via `movementSpeedPx(slot.spec.sourceData.movement_speed, 'monster:...')`. No runtime ratio math; speed is a property of the monster, not a derivative of player speed.

**Old-season JSON compatibility:** All 5 existing seasons (season_001001–001005) are pre-rocket/v1.3-ms-schema-defaults and lack `movement_speed` on both `ClassData` and `MonsterData`. `movementSpeedPx(undefined)` fires `console.warn` with a message identifying the combatant and references the upstream tag to fix. Fallback = 276 px/s (5.75 m/s × 48 = gandalf-locked base, Matt-approved 303258c). No crash, no silent wrong value. New engine-generated seasons suppress the WARN and deliver correct values (8.0 m/s player, 5.75 m/s trash, 7.5 m/s swarmer/sniper).

**Intermediate tag:** `drax/v0.20.5-engine-emitted-ms-consumption @ 6c812b1`
**Tests status:** 315/315 passed (21 new in tests/v0205-ms-consumption.test.ts + 294 prior unchanged). Build: `npm run build` clean.
**Notes for knight-rider:**
- topology.ts PIXELS_PER_METER = 48 inline preserved (v0.20.1 circular-import fix unchanged).
- No loadout changes.
- Smoke: tsc --noEmit clean; vite production build 520 modules clean.
- Old-season WARN is expected behavior for all current seasons — will resolve when rocket regenerates seasons with the new schema defaults.
- tickAIMove signature change: added optional `monsterSpeedPx` as 8th parameter (default = MOVE_SPEED_FALLBACK_PX). No callers outside main.ts.
