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

- [ ] **Handshake = sign the schema (Gate-1 fold 2):** answer schema-note open questions 1–5 (packaging / inline-vs-refs / null-handling / ProxyDecl SCAFFOLD acceptance / FloorManifest granularity) at `src/reincarnated/export/math/2026-07-02-one-realm-bundle-schema-note.md`. Your numbered answers ARE the lock signal (a–e); loader ergonomics govern the format. Escalate the signed answers back to KR (KR then fires the star-lord lock-emit follow-on).
- [ ] **WAIT-for-lock guard (Gate-1 fold 1 — LOAD-BEARING):** do NOT build the loader against a real bundle file until (i) MIGRATION.md v1.83 `schema_status` reads LOCKED AND (ii) the emitted sample bundle contains ≥1 kit with a non-empty `proxies` payload (summoner mandate §3; D2's decls injected). You MAY build the loader against the LOCKED SCHEMA SHAPE (your own signed answers) in parallel; only the round-trip smoke waits on star-lord's emitted+proxies-populated file. Rationale: prevents building against a DRAFT schema or round-tripping a `proxies:[]` bundle that passes while the summon verb is untestable (Principle 6 + Discipline #8).
- [ ] Godot bundle loader: parse the bundle, instantiate kits + monsters + gear from records (NO hand-built kits)
- [ ] Per-floor element-rotation manifest consumed from the bundle
- [ ] Faction restyle consumed as presentation layer (III.7 — restyle only)
- [ ] Round-trip smoke (load sample bundle → instantiate → field-presence) — **and assert the SCAFFOLD boundary (Gate-1 fold 3):** the loader must NOT bake the four SCAFFOLD proxy magnitudes (base_hp / damage_multiplier / attack_interval_s / proxy_max_active) into anything presented as tuned — they are gamora-D3 calibration targets (schema note :162-165; Discipline #9)
- [ ] Min-spec check per D10 (standing gate)
- [ ] `reincarnated-godot/` AGENT_STATE updated
- [ ] Tag: `drax/v-godot-bundle-loader-1`

## Acceptance criteria

- [ ] A demo-realm kit/monster/gear set loads from D1's bundle and is playable in Godot — **playability predicate (Gate-1 fold 4, §20d honesty):** at least one loaded kit instantiates with a resolvable primary_attack skill (name + geometry + range_m present and non-degenerate), NOT merely a record that parses
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


---

## Park record — drax, 2026-07-02 (handshake SIGNED; loader BUILT vs locked shape; round-trip PARKED for star-lord lock-emit)

**Status: PARKED at a clean boundary. Handshake signed, D10 stood up alongside, loader built + proven against the locked SHAPE. The §20d round-trip against real content is BLOCKED on the star-lord lock-emit — the intended sequencing park point.**

### Scope completion
- [x] **Handshake = sign the schema (fold 2):** answered Q1–5 → SIGNED at `agentic_orchestration/drax/notes/2026-07-02-one-realm-bundle-schema-handshake-drax-SIGNED.md`. Lock signal (a–e) all CONFIRMED. Escalated to KR (KR fires the star-lord lock-emit). Two conditions (all-keys-present guarantee; non-empty proxies) + one ambiguity (gear 10-vs-11 slot) are the only pushbacks.
- [x] **WAIT-for-lock guard (fold 1) HONORED:** loader built against the LOCKED SHAPE (my signed answers); the round-trip against a real file does NOT run until MIGRATION.md v1.83 LOCKED AND ≥1 non-empty proxies. Enforced in-code (`bundle_roundtrip_smoke.gd` real-mode requires schema_status=LOCKED + non-empty proxies).
- [x] **Godot bundle loader:** `scripts/bundle_loader.gd` — parses + instantiates kits/monsters/gear from records. **ZERO hand-built kits** (§20d honored — pure consumer).
- [x] **Per-floor element-rotation manifest:** consumed (`get_floor_sequence()` / `dominant_element_for_floor()`).
- [x] **Faction restyle (III.7 — restyle only):** `build_faction_restyle_map()` + `apply_faction_restyle()` — presentation overlay only; refuses any faction field colliding with a fight-model field (proven: NEG3 → III.7 VIOLATION fires).
- [x] **Round-trip smoke + SCAFFOLD boundary (fold 3):** `bundle_roundtrip_smoke.gd` asserts the 4 SCAFFOLD magnitudes are flagged non-tuned (proven: a non-scaffold-flagged proxy → FAIL). Ran in `--shape-fixture` mode → SHAPE PASS.
- [x] **Min-spec check per D10 (standing gate):** D10 stood up this session; the D4 acceptance checkbox wires in when the real round-trip closes (Godot render scene exists to profile).
- [x] **AGENT_STATE updated.**
- [x] **Tag:** `drax/v-godot-bundle-loader-1`.

### Acceptance — status
- [~] **A demo-realm kit/monster/gear set loads + is playable (playability predicate, fold 4):** PROVEN against the locked SHAPE (2/2 fixture kits resolve a non-degenerate primary_attack: name+geometry+range_m). **NOT yet closed against REAL content** — awaits the LOCKED emit. The predicate CODE is proven to fire (NEG2 range_m=0 → §20d PLAYABILITY FAIL).
- [x] **Zero hand-built kits Godot-side:** held — the loader is a pure consumer; no kit authored Godot-side.
- [~] **Round-trip smoke passes:** SHAPE PASS now; REAL round-trip closes on the lock-emit.
- [~] **D10 min-spec check passes:** D10 harness green; the D4-scene min-spec run happens when the real content renders.

### What's owed (the clean unblock)
Star-lord: (1) resolve gear 10-vs-11 slot ambiguity; (2) re-run assembly `--locked` with D2's summoner decls injected (≥1 kit non-empty proxies — NOT `proxies:[]`); (3) emit `one_realm_demo_bundle.json` schema_status=LOCKED; (4) stamp MIGRATION.md v1.83 LOCKED. Then drax: `bundle_roundtrip_smoke.gd --bundle <emitted>` closes the §20d round-trip against real content.

### Refutation conditions — none triggered; all three GUARDED
- Loader requires hand-massaging content → NO (pure consumer; zero hand-built).
- Schema forces brittle special-casing → fed the two conditions + one ambiguity back at handshake (the pushback happened).
- Loading "works" but content not playable → the §20d playability predicate + non-empty-proxies guard exist precisely to catch this; both proven to fire on negatives.

**Signed:** drax, 2026-07-02. Handshake signed, loader built to the locked shape, round-trip parked for the lock-emit. Reported to KR: fire star-lord, then bring me back to close the round-trip.
