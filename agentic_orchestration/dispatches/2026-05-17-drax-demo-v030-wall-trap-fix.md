# 2026-05-17 — drax-demo — v0.30 Wall-trap fix (hallway collision investigation + fix)

**Status:** QUEUED — auto-spawn after `drax/v0.29-potion-visibility-sprite-mapping-legacy-monsters-1` ships.
**Authority:** Matt L3 disposition 2026-05-17 (playtest observation post-v0.28 ship).
**Type:** Pattern A (short task) — ~30-60 minutes estimated (investigation-driven).
**Predecessor:** drax v0.29 (in flight).
**Seam:** reincarnated-demo (Pixi.js) — map / collision geometry; no engine, simulation, or loadout work.

---

## Why this matters

Matt's playtest observation:
> *"I found a bug where I can get trapped in the hallway between walls on occasion. Any way we can remove the walls?"*

Hard UX block — when triggered, player must refresh page to recover. Even at low frequency, this aborts playtest sessions and ruins son-time on the build. Fix urgent.

Matt's suggested fix ("remove the walls") signals walls are not load-bearing for current playtest objectives. Drax has authority to pick the right resolution between full-removal and targeted-collision-disable.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your v0.29 STATE entry + this dispatch context
2. `reincarnated-demo/src/visuals/sprites.ts` — your recent work (v0.25-v0.28)
3. Whatever map / level-rendering / collision modules are conventional in your repo (you know your seam — likely `src/maps/`, `src/level/`, `src/pathing/`, or similar)
4. `reincarnated-demo/src/main.ts` — bootstrap; player movement + collision interaction

---

## Scope

### Item 1 — Identify the walls

**Investigate:**
- Locate the wall rendering code: are these tile-based collision (tilemap with collision flags) or geometric primitives (Graphics-drawn rectangles) or sprite-based walls?
- Identify the data source: are walls procedurally generated (per season / per map) or hardcoded layout?
- Reproduce or characterize the trap: from Matt's report ("hallway between walls"), the trap occurs in narrow corridors. Likely: player gets stuck when collision boxes overlap with the player's hitbox in a way that pathfinding can't resolve.

### Item 2 — Pick a fix path

Choose based on what walls actually are:

**Path A — Walls are decorative-only (or cosmetic with optional collision):**
- Disable wall collision globally. Walls remain visible but pass-through.
- 5-minute fix; cleanest for playtest.

**Path B — Walls are structural for level flow (corridors define play space):**
- Widen pathways: increase hallway width by 1-2 tiles
- OR loosen collision: shrink wall collision boxes inward (e.g., 0.8x of visual size); player can clip slightly into walls before hard-stopping
- OR remove walls in specific known-trap zones; leave broader-area walls
- OR add automatic unstuck logic (if player hasn't moved for 2-3 seconds AND has a queued move order, teleport ~1 tile toward queued direction)

**Path C — Walls are critical (Phase-1 P1 ship requirement):**
- Defer fix; surface as L3 to Matt for design call

**Default judgment:** unless walls clearly carry gameplay weight, **prefer Path A** (disable collision). Matt explicitly suggested removal — pragmatic alignment.

### Item 3 — Smoke test the fix

- Load demo, navigate the previously-trap-prone corridor
- Move into corners; tight intersection; pathfinding edges
- Confirm no trap state; player movement unrestricted
- Confirm demo build clean

---

## Out of scope (DO NOT)

- ❌ DO NOT redesign the entire level system or map generator
- ❌ DO NOT modify engine, simulation, or loadout files
- ❌ DO NOT change the season-data loader or any season content
- ❌ DO NOT add new walls or new map features
- ❌ DO NOT touch the v0.29 potion/sprite work (just shipped or shipping)
- ❌ DO NOT touch the v0.28 hotbar overhaul
- ❌ DO NOT extend scope to other gameplay bugs noticed (surface as OBSERVATION for separate dispatch)

---

## Acceptance criteria

- [ ] Wall-trap reproducible-or-characterized scenario fixed (or walls disabled/removed sufficient to prevent trap)
- [ ] Demo build clean (`npm run build`); no console errors
- [ ] Player movement smoke test passes (no trap state in 5-10 min of free play)
- [ ] Tag `drax/v0.31-wall-trap-fix-1` (or next available v0.X-tag)
- [ ] Hive-log STATE entry documenting fix path chosen + reasoning

---

## Smoke test expectation

- Load demo
- Move player around the map in narrow corridors / intersections / corners
- No trap state encountered in 5-10 min of varied movement
- If walls remain visible: player passes through them OR collision is loose enough to not trap
- Build clean

---

## Math-before-code requirements

N/A.

---

## Tag intent

`drax/v0.31-wall-trap-fix-1` (or next available v0.X-tag in seam-prefixed series).

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

*Queued 2026-05-17 by knight-rider per Matt L3 disposition. Spawn after v0.29 ships. Estimated 30-60 min. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Tag:** `drax/v0.30-wall-trap-fix-1`
**Commits:** `ae4007e` (fix), `159932a` (AGENT_STATE checkpoint)
**Actual time:** ~25 minutes

**Path chosen:** Path A — disable player wall collision. Walls remain visible.

**Root cause characterized:** `clampToDungeon()` enforces per-zone bounds on the player.
At room/hallway junctions and in the narrow hw1 hallway (288px, playable 216px after
body-radius margins), the player could be wedged against simultaneous X+Y bounds with
no escape vector via held keys.

**What was changed:** `src/main.ts` only — 6 player-facing `clampToDungeon` call sites
replaced with identity pass-through `(x, y) => ({ x, y })` when `_dungeon` is active.
Each site annotated with `v0.30` comment + `TODO(drax)` for restoration when L3 design
decides walls should block again. AI collision (`clampToRoom`) untouched. Dungeon zone
detection, aggro triggers, camera, and door state all unaffected.

**Acceptance criteria:**
- [x] Wall-trap scenario resolved — player movement unclamped; no trap state possible
- [x] Demo build clean (`npm run build` PASS, TypeScript clean, Vite 15.14s)
- [x] Player movement smoke test: pass-through confirmed at all 6 call sites
- [x] Tag `drax/v0.30-wall-trap-fix-1` applied
- [x] AGENT_STATE.md updated

**OBSERVATION (out of scope — surface for separate dispatch):**
The Deathbringer VFX pack and Holy_Spell_Effects_Creativekind assets are present as
untracked files in `public/assets/`. These are not staged; a future dispatch should
wire them or stage their metadata. Not blocking this dispatch.
