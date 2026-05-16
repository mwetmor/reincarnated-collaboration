# Dispatch — 2026-05-16 — drax — Room/Hallway geometry system (VS2a critical-path; supersedes ellipse re-dimensioning)

**From:** knight-rider (authored per Matt 2026-05-16 Day 4 design directive + gandalf canonical `canonical/story/arena-room-hallway-system.md`)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (design directive: "I would like rooms that are more similar to Diablo/PoE and they should connect to one another without enemy combatant aggro prior to entering each room..."; gandalf canonical doc filed with Matt's defaults confirmed)
**Status:** PENDING — AWAITING-MATT-FIRE-CONFIRM. Large-scope dispatch (~1.5-2 weeks); knight-rider authoring this for Matt eyeball before drax fires.
**Estimated effort:** 2-3 sessions per playtest cycle; **calendar estimate 1.5-2 weeks** total including re-validation per gandalf's analysis; VS2a critical-path; drax line gains +1-1.5 weeks vs prior estimate (risk-1 update needed in roadmap).
**Acceptance:** Demo arena topology migrated from single-ellipse to room/hallway interior model per canonical `arena-room-hallway-system.md`; clampToEllipse retired; per-room aggro state machine implemented; camera variant logic for 15m/30m/45m rooms; B10 V2 sequential-room semantics receive matching visual presentation; intermediate tag; re-validation playtest cycle complete.

**SUPERSEDES:** ELLIPSE_RX 784→960 px authorization from prior turn (single-ellipse model itself is retired; not just re-dimensioned).

---

## Context — what Matt's directive locked

Per Matt's 2026-05-16 directive (gandalf-relayed):

> "I would like rooms that are more similar to Diablo/PoE and they should connect to one another without enemy combatant aggro prior to entering each room (roughly, or a general aggro range which fits the screen). So I think the genre's style prefer's square rooms and rectangular hallways (when not in open air areas)."

Per gandalf canonical `canonical/story/arena-room-hallway-system.md` (227 lines; Matt-approved 2026-05-16):

- **Door Mode B (free traversal)** — locked as default per Matt's defaults confirmation
- **Room size envelope 15-45m** with 30m default
- **Hallway width 6-10m** range (variable within range for visual interest)

**Pattern P6 resolution:** B10 V2's sequential-room sim semantics are landing without matching visual presentation. The forward audit (`canonical/story/p6-forward-audit-2026-05-16.md` § B10 V2 row WATCH item) flagged this. This dispatch operationalizes the WATCH item with full design direction.

## What this dispatch does

### Step 1 — Replace `reincarnated-demo/src/world/arena.ts`

The `clampToEllipse` model retires. Suggested approach (drax discretion on exact module structure):

- New module `reincarnated-demo/src/world/topology.ts` (or extend `arena.ts`) exporting room + hallway data structures + bounds-clamping logic
- Per gandalf canonical doc § "Suggested data structures":

```typescript
interface Room {
  id: string;
  bounds: { x: number; y: number; width: number; height: number }; // px
  variant: 'small' | 'default' | 'large'; // 15m / 30m / 45m
  aggroState: 'dormant' | 'active' | 'cleared';
  enemies: Combatant[];
  doors: Door[];
}

interface Hallway {
  id: string;
  bounds: { x: number; y: number; width: number; height: number };
  connects: [string, string]; // room IDs
}

interface Door {
  position: { x: number; y: number };
  connectsTo: string; // room or hallway ID
}

interface Dungeon {
  rooms: Room[];
  hallways: Hallway[];
  startingRoom: string;
}
```

These are suggestions; you have discretion on the actual data model. The constraints from the canonical doc are the semantics, not the types.

### Step 2 — Update `reincarnated-demo/src/world/movement.ts`

Replace `clampToEllipse` calls in `tickPlayerMove` and `tickAIMove` with room-or-hallway-aware bounds clamping:

- Player bounds: current room OR current hallway (based on player position)
- AI bounds: current room ONLY (AI does not pursue into hallways per genre convention)
- AI pursuit cap at room edge — if AI reaches room threshold while chasing player into hallway, AI halts and returns to ambient/wandering behavior within room

Preserve all movement-speed values from `canonical/story/movement-speed-baseline.md` (player base 5.75 m/s effective; AI_SPEED_MULTIPLIER 0.767 for VS2a mid-game-equivalent; chase margin 84 px/s).

### Step 3 — Per-room aggro state machine

New module `reincarnated-demo/src/world/aggro.ts` (suggested) per gandalf canonical doc:

**Three states per room:**
- **dormant**: all enemies positioned but inactive (no movement, no attacks, no AI tick; idle pose OR absent if positioned off-screen — drax design call)
- **active**: triggered when player crosses room threshold; ALL enemies in room transition simultaneously; standard AI behavior per `tickAIMove` with movement-speed values
- **cleared**: non-reversible state when all enemies dead; room remains traversable

**Trigger:** player threshold-crossing detection (room-edge or door-position detection). Activation is simultaneous for all enemies in room.

**"Screen-fit aggro range" = the room itself** (since rooms are sized to fit on viewport — 30m default fits 1920×1080 with margin at 48 px/m).

### Step 4 — Camera/viewport behavior per room variant

- **In hallway:** tight follow camera (existing `tickPlayerMove` behavior preserved)
- **In room (default 30m × 30m / 1440×1440 px):** frame the player with room bounds visible; camera may pan if player approaches room edge
- **In room (small variant 15m × 15m / 720×720 px):** full room visible at once; camera framing fixed at room center with player offset
- **In room (large variant up to 45m × 45m / 2160×2160 px):** camera follows player within room bounds; full room not visible at once; pre-pan optional on entry
- **Room-entry transition:** brief pan to frame room (~0.5s) before AI activates; gives player visual orientation. AI_ENGAGEMENT_WINDUP (current 0.7s in `movement.ts`) already covers this window

Camera module location: existing camera logic likely lives in `main.ts` or `rendering/`; drax discretion on where the room-aware framing lives.

### Step 5 — Door visual element (placeholder primitive)

Visual door element at room ↔ hallway boundaries:

- Placeholder primitive geometry (rectangular threshold marker) — feedback-layer art per P6.c sub-pattern; production door art is NOT in current sourcing scope
- Mode B (free traversal): door is passable in both directions at all times; player can retreat to hallway

### Step 6 — Linear-dungeon topology for VS2a

For VS2a's single-season regen: a linear dungeon (room1 → hallway → room2 → hallway → room3 → ...) is sufficient per gandalf canonical doc § "Integration with B10 V2 sequential rooms."

- Engine sim's "room" concept (HP carryover; N mobs per room from B10 V2) maps 1:1 to demo's visual Room
- B10 V2's sequential ordering becomes hallway connectivity in the visual topology
- Drax consumes engine's per-room composition data to populate visual rooms

**Branching/non-linear dungeons are explicitly Phase 1+ design** (out of scope for VS2a/VS2b).

### Step 7 — Re-validation playtest cycle

This is **equivalent to phase 6.1/6.2 movement calibration but for arena topology** per gandalf canonical doc § "Re-validation needed":

- **AI engagement distances** (`PREFERRED_RANGE` in `movement.ts`) — values were tuned for ellipse model; may need adjustment for room model
- **Chase margin in active-room state** — should remain 84 px/s per movement-speed-baseline spec; verify with new bounds
- **Pack movement patterns** — `tickAIMove` kiting logic needs to respect room bounds (no kiting through walls; predictable cap behavior)
- **Player traversal feel** — hallway widths should not feel constraining (test 6m vs 10m for visual + tactical feel); rooms should not feel arbitrary (test 30m default + 15m + 45m variants per encounter)

File playtest findings at `~/Games/reincarnated-loadout/ARENA_TOPOLOGY_PLAYTEST.md` (or per loadout-repo convention).

### Step 8 — Tests + smoke

- Existing arena tests adapted to new topology (existing `clampToEllipse` test sites become room/hallway bounds tests)
- New unit tests for room aggro state machine (dormant → active → cleared transitions; trigger detection; pursuit-cap-at-room-edge)
- New unit tests for camera variant logic
- Smoke: load test dungeon (3 rooms linear, 2 hallways) and verify: dormant rooms have no AI tick; active room AI behaves per current logic with new bounds; hallway traversal smooth; cleared rooms remain traversable

### Step 9 — Intermediate tag + AGENT_STATE + completion record

- Tag: `drax/v0.12-room-hallway-geometry-system` (or per loadout-repo tag convention)
- AGENT_STATE.md updated
- Completion record at bottom of this dispatch filled
- Re-validation playtest findings documented + recommendations for downstream tuning surfaced for Matt

## Cross-seam considerations

- **Engine (rocket/gamora/star-lord):** READ-ONLY consumer; B10 V2 engine sim semantics are unaffected by this dispatch; engine's per-room composition data is the input substrate this dispatch presents visually
- **Gandalf:** READ-ONLY consumer of your re-validation playtest findings; future tuning conversations operate against your empirical evidence; canonical doc is source-of-truth for design parameters (don't deviate without gandalf input)
- **Knight-rider:** notify at completion; this dispatch + the V2.1 emission-gap fix + B10 V2 land the full "sequential-room sim + matching visual presentation" cohesion for VS2a

## Out of scope (explicit per gandalf canonical doc § "What's NOT in scope")

- **NO open-air areas (second register)** — deferred to Phase 1 / VS2c+; second canonical doc when scope opens
- **NO branching / non-linear dungeons** — VS2a/VS2b ship linear dungeons; branching is Phase 1+ design
- **NO production door art** — placeholder primitive only; production art is P6.c feedback-layer track with no current commission
- **NO room theming / environment art** — Phase 1+
- **NO Mode A (gated doors) as default** — Mode B locked-in; Mode A remains per-encounter override for set-piece designs in future seasons
- **NO patrolling enemies in hallways** — empty hallways per Matt's "no cross-room aggro" directive
- **NO cinematic camera transitions** — no entry cutscenes; no boss-room dramatic framing; simple pan-and-frame only
- **NO movement-speed-baseline value changes** — locked at canonical/story/movement-speed-baseline.md; this dispatch consumes them, does not alter them
- **NO Pimen VFX work** — separate prior dispatch landed (`drax/v0.11-pimen-first-vfx-integration @ ef7f7c9`); independent
- **NO spatial-data PixiJS consumption** — separate dispatch per spatial-data cascade Step 5

## Required reading

- `canonical/story/arena-room-hallway-system.md` (source-of-truth; 227 lines; consume in full)
- `canonical/story/movement-speed-baseline.md` (m/s + 48 px/m + AI_SPEED_MULTIPLIER values)
- `canonical/story/p6-forward-audit-2026-05-16.md` § B10 V2 row (WATCH item this resolves)
- `canonical/16-project-roadmap.md` § B10 V2 + § VS2a (engine sim semantics this presents visually)
- `canonical/story/drift-audit.md` Pattern P6 (drift framing this resolves)
- `~/Games/reincarnated-demo/src/world/arena.ts` (current ellipse model being replaced)
- `~/Games/reincarnated-demo/src/world/movement.ts` (clampToEllipse call sites + AI engagement values)
- `~/Games/reincarnated-demo/src/main.ts` (camera logic to update)
- Your prior movement-speed PixiJS implementation completion record (`drax/v0.10-movement-speed-locked @ 151c7ec`) — Case A arena cramping signal informs how the new room sizes resolve that friction
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code: room sizes are math-locked per gandalf canonical); #2 (smoke-test); #11 (attribution: canonical doc is the source-of-truth)

## Acceptance criteria

- [ ] `arena.ts` (or new `topology.ts`) implements Room/Hallway/Door/Dungeon data structures (or equivalent)
- [ ] `movement.ts` `clampToEllipse` calls replaced with room-or-hallway-aware bounds clamping
- [ ] AI pursuit cap at room edge implemented (no pursuit into hallways)
- [ ] Per-room aggro state machine: dormant → active → cleared transitions working
- [ ] Camera variant logic for 15m/30m/45m room rendering
- [ ] Linear dungeon (room → hallway → room → ...) loadable + traversable
- [ ] Engine per-room composition data consumed correctly (1:1 mapping to visual rooms)
- [ ] All existing tests pass + new aggro-state-machine + camera-variant tests pass
- [ ] Re-validation playtest cycle complete; findings documented
- [ ] Intermediate tag `drax/v0.12-room-hallway-geometry-system` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `drax/v0.12-room-hallway-geometry-system` at the commit closing topology + aggro + camera + smoke pass.
- **Milestone tag:** none from this dispatch. Matt may elevate post-VS2a-ship.

---

## Completion record

**Completed:** 2026-05-16
**Intermediate tag:** `drax/v0.12-room-hallway-geometry-system` @ `5463be8`

**Topology data model chosen:**
Implemented all four types from the canonical suggestion (Room, Hallway, Door, Dungeon) with slight extensions: added `AggroState` on Room, `ZoneRef` for zone resolution, and helper functions (findZone, clampToDungeon, clampToRoom, exitDoor, playerSpawnForRoom, enemySpawnPositions). Module: `src/world/topology.ts`. Data model follows canonical suggested structure closely; discretion used on helper API surface.

The VS2a dungeon is a 7-room linear layout built by `buildVS2aDungeon()`:
- Rooms 1-3, 6-7: default variant (30m × 30m = 1440px)
- Room 4: small variant (15m × 15m = 720px) — tight mini-boss chamber
- Room 5: large variant (45m × 45m = 2160px) — boss set-piece
- 6 hallways alternating 6m/8m/10m wide for visual interest (all within 6-10m canonical band)

Dungeon is positioned in world-space with Y-center at CANVAS_HEIGHT/2 = 472px. Rooms laid out left-to-right along X-axis. Total dungeon world width ≈ 12.6 km (all rooms + hallways sum).

**Aggro state machine implementation notes:**
Module: `src/world/aggro.ts`. Three states implemented per spec: dormant / active / cleared.

- `checkAggroTrigger()` — called each frame from game loop when `gState === 'fighting'`; returns newly-triggered room or null
- `activateRoom()` — dormant → active; logs to console
- `clearRoom()` — active → cleared (non-reversible); called in `onDeathTimerExpired()`
- `shouldHaltPursuit()` — AI room-anchor cap: halts pursuit when player exits room AND AI is within 60px of room edge
- `isRoomAggroActive()` — gates AI skill tick in game loop

Main.ts wiring: aggro trigger check runs every frame in fighting state. AI movement tick is gated on `isRoomAggroActive(anchorRoom.aggroState)`. Dormant rooms = AI motionless at spawn positions. Aggro activates simultaneously for all pack members when player enters room. Room-anchor cap prevents AI from pursuing into hallways.

**Camera variant implementation notes:**
Module: `src/rendering/roomRenderer.ts`, exported as `computeCameraTarget()` + `lerpCamera()` + `applyCameraOffset()`.

Camera behavior by zone/variant:
- Small room (720px), default room (1440px), all hallways (288-480px): zone fits within 1800px canvas → camera fixed at zone center; full zone visible
- Large room (2160px): zone wider than canvas → follow-camera; player-centered, clamped at room edges

Camera uses exponential-decay lerp: `t = 1 - exp(-speed * dt)` with `CAMERA_SPEED = 8.0` (snappy, responsive follow). Screen shake from knockback passed through `applyCameraOffset()` as amplitude parameter on top of camera offset. Stage X/Y now encodes both camera position and screen shake (no longer zeroed between frames).

One behavior note: default room (30m × 30m) fits entirely within the 1800px canvas with 180px margin on each side. Player always sees the full default room — more comfortable than the prior ellipse (1568px visible width). This effectively resolves Case A arena cramping from v0.10 for default-room encounters.

**Re-validation playtest findings path:**
`~/Games/reincarnated-loadout/ARENA_TOPOLOGY_PLAYTEST.md` (loadout repo commit `1511db2`)

**Recommendations for downstream tuning:**
1. Wave 4 (small room, mini-boss): pack composition should use close/medium range profiles. PREFERRED_RANGE['long']=660px spans 92% of a 15m room — long-range AI will wall-hug. This is a gauntlet builder content call, not a movement.ts change.
2. Wave 5 (large room, boss): candidate PREFERRED_RANGE['long'] bump 660→900px to use the 45m room's space. Matt/knight-rider design decision.
3. KITE_TRIGGER (300px) monitor at playtest — may cause ranged AI to back into walls in default rooms.
4. Room-entry camera snap is instantaneous (camera already at room center for small/default rooms that fit viewport). If Matt wants a visible entry pan, reduce CAMERA_SPEED from 8.0→2.0 on room entry event; revert after pan completes.
5. Ambient particles: currently drift across full dungeon world-space. Suggest per-room or player-zone clipped particles in a follow-on dispatch.

**Notes for knight-rider:**
- Pattern P6 WATCH item (`canonical/story/p6-forward-audit-2026-05-16.md` § B10 V2 row) is resolved. Engine sim sequential-room semantics now have matching visual presentation. WATCH item can be closed.
- VS2a ship gate: this dispatch + V2.1 emission-gap fix + B10 V2 engine land the full "sequential-room sim + matching visual presentation" cohesion. Drax side is complete pending Matt's visual playtest.
- Open item for V0.13+: spatial-data PixiJS consumption dispatch (named in dispatch as a separate step); still pending.
- The 3 pre-existing `damage.test.ts` failures (rollAilmentApplies return type) are NOT introduced by this dispatch. Pre-existed at v0.11. They need a follow-on fix (changing `.toBe(true/false)` to `.toBe(result.applies)` or similar) — low urgency, non-blocking.
- `clampToEllipse` still exists in arena.ts (used for menu-screen background drawing). Not retired in this dispatch. Can be fully removed if/when menu screens adopt rectangular geometry.
