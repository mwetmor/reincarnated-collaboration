# Dispatch — 2026-07-02 — drax — Godot bundle loader (D4)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-07-02 (one-realm §6.1; opens Wave 2, the Godot critical path)
**Estimated effort:** 2–4 days
**Acceptance:** engine-emitted content (D1's bundle) loads and is playable in `reincarnated-godot/` — a demo-realm kit/monster/gear set instantiated from the bundle, NOT hand-built Godot-side.
**Status:** GATED on D1 contract handshake. Fires when D1's bundle schema is handshaked. Gate-1 required before execution.

## Context

§6.1: "engine-emitted content playable in Godot. Hand-building kits Godot-side is FORBIDDEN: the engine is the product, and §20d is the condition under test." This dispatch is the **§20d test made concrete** — if the engine's bundle can't be loaded and played in Godot cheaply, we must know before promising 400 kits. It consumes D1's bundle. **Sequence the contract handshake with star-lord FIRST**: review D1's bundle schema note, agree the format (loader ergonomics govern), THEN build the loader.

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §6.1, §4 scope table, §0 (the loop this enacts)
- `canonical/current-to-end-state/current-to-end-state-game.md` (the playable-build tracker — your delta)
- D1 (`2026-07-02-star-lord-one-realm-emission-handjoin.md`) + its MIGRATION.md (the bundle schema — the contract you consume)
- `reincarnated-godot/` AGENT_STATE + scripts inventory (Synty POLYGON assets, Forward+/Metal, the enchanted-forest ravine level)

## Cross-seam contract change? (Principle 6 gate — YES, consumer side)

You are the **consumer** of D1's bundle-schema contract. The handshake is the gate: co-review the schema with star-lord before it locks.
- `Round-trip smoke: load D1's sample demo-realm bundle; instantiate every record type (kit/monster/gear); assert field-presence + playable instantiation. This IS the D1 round-trip's consumer boundary.`

## Scope

- [ ] Contract handshake with star-lord on D1's bundle schema (loader ergonomics inform the format) — BEFORE building
- [ ] Godot bundle loader: parse the bundle, instantiate kits + monsters + gear from records (NO hand-built kits)
- [ ] Per-floor element-rotation manifest consumed from the bundle
- [ ] Faction restyle consumed as presentation layer (III.7 — restyle only)
- [ ] Round-trip smoke (load sample bundle → instantiate → field-presence)
- [ ] Min-spec check per D10 (standing gate)
- [ ] `reincarnated-godot/` AGENT_STATE updated
- [ ] Tag: `drax/v-godot-bundle-loader-1`

## Acceptance criteria

- [ ] A demo-realm kit/monster/gear set loads from D1's bundle and is playable in Godot
- [ ] Zero hand-built kits Godot-side (§20d condition demonstrably held — content comes from the bundle)
- [ ] Round-trip smoke passes (consumer boundary of D1's contract)
- [ ] D10 min-spec check passes at this stage

## Out of scope (explicit non-goals)

- Verb realization (D5) — this dispatch loads/instantiates; verbs come next
- Floor authoring (D6), enemy AI (D7), UI (D8)
- Any re-emission or engine-side content authoring (that's the engine seam; you consume)

## Quality criterion

**Game-quality goal:** proves the engine-is-the-product thesis — playable content flows from the engine bundle, not from Godot hand-authoring. This is the honesty test behind the "400 kits" promise.

**Refutation conditions (surface if any apply):**
- The loader requires hand-massaging content Godot-side to make it playable (§20d failing — surface immediately)
- The bundle schema forces the loader into brittle special-casing (feed back to star-lord at handshake)
- Loading "works" but the content isn't actually playable (acceptance passing without advancing §20d)

## Open questions for the agent to resolve

- Loader architecture (resource-import pipeline vs. runtime JSON parse) — your call, document it
- How Synty POLYGON asset mapping keys off bundle records (archetype_tag → mesh set?)

## References

- one-realm-mvp-scope.md §6.1 · §20d (the condition under test) · D1 + MIGRATION.md
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md`
