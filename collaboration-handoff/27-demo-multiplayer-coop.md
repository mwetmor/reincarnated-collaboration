# Demo Multiplayer Co-op Architecture

**Captured:** 2026-05-10
**Scope:** add 2-player co-op (project owner + son) to the Pixi.js demo. Real-time shared session: both players in the same arena, fighting the same monsters and bosses, sharing damage credit and drops.
**Status (decided 2026-05-10):** **moved to demo1 Phase 7 stretch goals (optional, post-Phase-6).** Demo1 main scope (Phases 1-6) ships single-player. After Phase 6 family playtest, if multiplayer is still desired, this doc's architecture lands as Phase 7 Stretch A in file 24 (~2 weeks effort).

## Why this is its own document

Multiplayer is **architecturally different** from single-player demo1. Single-player Pixi.js is browser-only with all state in the client. Multiplayer requires:

- Server runtime (Node.js or similar)
- WebSocket or HTTP-poll connection between clients and server
- Shared game state on the server (authoritative)
- Client-server message protocol (action events from clients; state broadcasts from server)
- Player ID assignment + session lobby
- Latency masking / interpolation for smooth gameplay
- Decisions about loot attribution and damage credit

This isn't a small addition — it changes the deployment model (now requires hosting), the game-loop architecture (server-authoritative), and the gameplay rules (who gets what when).

It deserves its own doc + scope decision.

## Phasing — locked 2026-05-10

Multiplayer is **moved to demo1 Phase 7 stretch goals**. Phases 1-6 of demo1 ship single-player; multiplayer is added optionally as a post-Phase-6 stretch if/when desired.

This is similar to original "Path B" but consolidates the multiplayer effort with other stretch goals (per-season music) under a unified Phase 7 stretch section in file 24.

Original phasing options (now superseded):
- A: integrate into demo1 from start (rejected — too much scope)
- B: ship single-player first, layer multiplayer as demo1b (close to chosen path; consolidated under Phase 7 stretch)
- C: defer to demo3 entirely (rejected — too far in future for desired use case)

## Architecture for "super-simple server"

Design constraint: minimum-viable server that supports 2-player co-op without ambition for more (no leaderboards, no persistence, no server-side anti-cheat).

### Stack
- **Server:** Node.js with Express (HTTP) + `ws` (WebSocket) library
- **Hosting (development):** `localhost:3000` (you and son connect via local network — same WiFi)
- **Hosting (later):** any static-friendly hosting that supports Node (Render, Fly, Railway) OR self-host on a Mac/Raspberry Pi at home
- **State storage:** in-memory only (server holds the active session; nothing persists across server restarts; that's fine for co-op demo)
- **Protocol:** WebSocket binary or JSON messages; no message-queue middleware needed

### Game state model
- Server holds:
  - Active session (one per server instance — single-room model is fine for 2-player demo)
  - Each player's: class data (loaded from JSON exports; same as single-player), HP, resources, status effects, equipped gear, inventory
  - Current encounter state: which wave, which opponents alive, opponent HP/state
  - Drop pool: items dropped but not yet picked up
- Each client renders a snapshot of relevant state; no client-side game state (or minimal — interpolation only)

### Client-server protocol
- **Client → server messages:**
  - `JOIN` (with player name + chosen class)
  - `READY` (signal to start encounter)
  - `ABILITY_USE` (ability ID + target)
  - `POTION_USE` (potion type)
  - `EQUIP` (gear instance ID + slot)
  - `PICKUP` (drop instance ID)
- **Server → client broadcasts:**
  - `STATE` (full game state snapshot, ~10-30 Hz)
  - `EVENT` (combat events: damage dealt, status applied, drop spawned, etc.)
  - `TRANSITION` (wave change, victory, defeat)

### Co-op rules to settle

These are gameplay-design questions, not implementation:

1. **Damage attribution.** When player A's ability hits a monster, does player A get "credit" for damage? Both? For demo1b purposes, probably "both — shared encounter, shared progress."
2. **Drop attribution.** When a boss drops gear, who gets it?
   - Option: shared loot — whoever picks up first gets it
   - Option: per-player loot — server splits drops; each player gets their own claim
   - Option: turn-based pickup — each player gets dibs on alternating drops
   - Recommended: **shared loot** for simplicity; whoever picks up first gets the item. Family playing co-op will work it out socially.
3. **Death and revival.** If one player dies, do they wait for the other to finish, or revive?
   - Option: revive at next wave (player respawns when wave ends, sits out current wave)
   - Option: encounter fails when either player dies (high-stakes co-op)
   - Recommended: **revive at next wave** — keeps both players engaged.
4. **Scaling.** Are monsters tougher in 2-player? In single-player demo1, monsters are calibrated for one player. Two players makes encounters easier.
   - Option: keep monsters the same (encounters become easier in co-op, that's fine)
   - Option: scale monster HP × 1.5-2x per additional player
   - Recommended: **for demo1b, keep monsters the same.** Easier co-op is fine; it's a demo. Scaling is post-MVP.

### Sync challenges (latency masking)

For local-network play (same WiFi), latency is <10ms — feels instant. Acceptable for demo1b.

For internet play (you on one network, son on another remote network — e.g., him at college someday), latency could be 50-200ms. Needs:
- Client-side prediction for own actions (player presses ability → sees animation immediately; server confirms shortly after)
- Interpolation for other player's movement/actions
- Reconciliation if server state differs from client prediction

For demo1b: **assume local-network co-op only.** Internet-quality multiplayer is post-demo polish.

## Implementation phasing for demo1b (if Path B chosen)

Six steps, ~2 weeks total:

1. **Server scaffolding** (~2 days): Node.js + Express + ws; server holds in-memory session; basic JOIN/READY/STATE protocol
2. **Authoritative game loop** (~3-4 days): refactor client's game loop to be a render-of-server-state; all combat resolution moves server-side
3. **Action message handling** (~2 days): client sends ABILITY_USE, server processes (damage formula runs on server); state updates broadcast
4. **Co-op gameplay rules** (~2 days): drop attribution, revival, multi-player encounter logic
5. **UI for co-op** (~1-2 days): show partner's HP/resources, partner's name + class, partner's status effects
6. **Local network deployment + family playtest** (~1-2 days): set up server on a Mac at home, both players connect from same WiFi; iterate on feel

Each step is ~half-CP-equivalent of the single-player demo1's pacing.

## Architecture implications for demo1 (single-player) phase

If Path B is chosen, demo1 single-player work should be **structured to make demo1b refactor easy.** Specifically:

- Keep combat resolution functions **pure** (no rendering side effects in the resolver itself). This makes moving them server-side trivial in demo1b.
- Encapsulate game-state mutation in a **single state-update path**. The client-side game loop should look like: "consume input events → update state → render state." This separation is exactly what server-authoritative needs.
- Avoid putting game state in Pixi.js scene objects directly. Keep state in plain TS objects; sync to Pixi rendering each frame. This makes the state serializable for network transmission later.

These are good hygiene patterns regardless. They make demo1b's refactor a 1-2 week effort instead of a multi-week rewrite.

## Cost considerations

- Server hosting: $0 if local-only / self-hosted; ~$5-20/month for cloud hosting if you want internet co-op later
- Bandwidth: trivial (game state messages are small)
- Server compute: trivial (one Node.js process handles 2 players easily)

No LLM costs for multiplayer.

## What's NOT in scope for multiplayer

- **More than 2 players** (no scaling beyond co-op for demo1b/demo3)
- **Persistent player accounts / progression** (each session is fresh)
- **Anti-cheat / authoritative server validation beyond basic sanity checks** (demo, not commercial; trust both players)
- **PvP** (fight each other) — completely out of scope
- **Voice chat / text chat** (Discord is the family's tool)
- **Spectator mode** (no third players watching)

## Cross-references

- File 22 / file 24: demo1 / demo2 implementation context
- File 25: visual content R&D — adds partner-rendering visuals when multiplayer lands
- File 26: audio R&D — adds partner-action SFX (subtle audio cues for "your partner just used an ability") when multiplayer lands
- File 16 (roadmap): timeline placement once Path A/B/C is decided

## Status

- [ ] **Path A/B/C decision** (project owner)
- [ ] If Path B: demo1 single-player ships first
- [ ] demo1b architecture (after demo1 ships): server scaffolding → state refactor → co-op rules → playtest
- [ ] Family co-op playtest #1 (first time you and son play together)
- [ ] Iterate on co-op feel (revival, scaling, drop attribution)
