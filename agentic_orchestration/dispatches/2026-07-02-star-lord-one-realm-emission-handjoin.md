# Dispatch — 2026-07-02 — star-lord — one-realm emission hand-join (D1)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-07-02 (one-realm §5.1; the first of the two bounded engine asks)
**Estimated effort:** 1–2 days
**Acceptance:** a single Godot-consumable bundle for the demo realm (kits + monsters + gear + flavortext) exists, validates, and its schema is contract-handshaked with drax (D4).
**Status:** READY — first fire (concurrent with D2; consumes D2's decls). Gate-1 required before execution.

## Context

One Realm is the denominator (`canonical/reap-die-rise-game/one-realm-mvp-scope.md`, Matt-ratified 2026-07-02). §5.1 pulls a bounded **one-realm emission hand-join**: a single Godot-consumable bundle joining the two content tracks (generation + simulation-validated) for the demo realm. This is **explicitly NOT the II.2 unified emission driver** — that stays launch-track. It is a hand-join of what the demo realm needs: the ~8–10 curated kits (incl. ≥1 summoner), the demo monster set, gear, and flavortext, packaged so Godot can load and play it. The engine is the product; §20d ("if ~10 kits can't become 10 distinct verbs cheaply, we must know before promising 400") is the condition this bundle puts under test.

This bundle is the **root dependency of the entire Godot critical path** (§6). drax's bundle loader (D4) consumes it. The bundle **schema** is therefore a cross-seam contract: define it with drax before finalizing.

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §0–§6 (the denominator; §5.1 is your ask, §3 the roster shape, §4 the scope table)
- `current-to-end-state-engine.md` II.3 (emission gap — your bullet is the "+1 MVP-CRITICAL bounded one-realm hand-join"; the (a)–(d) general plumbing stays launch)
- Your own AGENT_STATE + the existing emitters: `cycle14_unified_bundle_emitters.py` (:363-373 monster bundle fields — the banked bundle-field surface), season_writer output shape
- `agentic_orchestration/gamora/notes/2026-07-02-sim-two-state-inspection.md` §Q3 (which demo-load-bearing capabilities are LIVE — element rotation, arena shells, kit power)
- D2 (`2026-07-02-rocket-demo-summoner-proxy-decls.md`) — the summoner kits' `proxies` payloads are an input to your bundle

## Math-before-code

Not a math dispatch. But **write a short bundle-schema note first** (`export/math/` or a schema doc) defining the bundle record shape BEFORE emitting — this is the artifact drax reviews at the contract handshake. Enumerate: kit record (stats/skills/proxies/element/archetype_tag/role_orientation/flavortext), monster record, gear record, per-floor element-rotation manifest, faction-restyle fields (presentation-side, III.7 invariant — faction is a restyle, not a stat change).

## Cross-seam contract change? (Principle 6 gate — YES)

This dispatch **defines a new cross-seam contract**: the Godot-consumable bundle schema (star-lord producer → drax/Godot consumer). **MIGRATION.md REQUIRED** documenting the bundle schema. Acceptance MUST include a round-trip:
- `Round-trip smoke: emit the demo-realm bundle from the production emission path; load-validate every record type against the schema; hand the schema + a sample bundle to drax (D4) for the contract handshake before the schema is locked.`

## Scope

- [ ] Bundle-schema note (the contract artifact for drax handshake)
- [ ] One-realm emission hand-join: emit a single bundle for the demo realm — kits (incl. summoner kits with D2's `proxies` payloads) + monsters + gear + flavortext
- [ ] Per-floor element-rotation manifest in the bundle (engine-supported today — one-realm §4)
- [ ] Faction fields present as **presentation-restyle** (III.7 invariant protected — faction does not change damage_scaling/affinity/resistance)
- [ ] Weapon descriptors: nice-not-critical — include if cheap, do not block the bundle on them
- [ ] Round-trip smoke + schema handshake with drax
- [ ] MIGRATION.md (bundle schema, star-lord↔drax boundary)
- [ ] AGENT_STATE.md updated
- [ ] Tag: `star-lord/v-one-realm-bundle-handjoin-1`

## Acceptance criteria

- [ ] A demo-realm bundle emits from the production path and validates against the schema note
- [ ] Summoner kits in the bundle carry D2's real `proxies` payloads (not `[]`)
- [ ] Faction is a restyle layer; III.7 invariant demonstrably held (no stat mutation)
- [ ] Round-trip smoke: emit demo-realm bundle → load-validate all record types → schema handshaked with drax (D4) before lock
- [ ] MIGRATION.md written (bundle schema contract)

## Out of scope (explicit non-goals)

- The II.2 unified emission driver (launch-track — this is a hand-join, not the driver)
- The (a)–(d) general emission plumbing in II.3 (launch-scope)
- Weapon-descriptor completeness (nice-not-critical)
- The 100-kit launch roster (III.4)
- Any `_DEFERRED_PROXY_BINS` lift or 25% proxy emission (launch-track; the summoner content in this bundle is hand-authored via D2, not generation-emitted)

## Quality criterion

**Game-quality goal:** the demo proves the engine is the product — engine-emitted content, not Godot-hand-built content, is what plays (§20d, the condition under test). A clean bundle contract is what makes "no meta / every hero unique / 400 kits" a promise the demo can make honestly.

**Refutation conditions (surface if any apply):**
- The bundle schema pre-commits to a content-shape Matt/gandalf has not ratified
- The hand-join drifts toward re-implementing the II.2 unified driver (scope creep)
- Faction fields leak into stat-affecting territory (III.7 violation)
- The bundle can validate without actually being Godot-loadable (acceptance passes without advancing §20d)

## Open questions for the agent to resolve (document your calls)

- Bundle packaging format (single JSON manifest + asset refs? per-record files?) — decide with drax at the handshake; drax's loader ergonomics govern
- Whether flavortext ships inline per-record or as a side table
- Minimal viable monster/gear record for the demo realm (curate to the demo's needs, not the full generator surface)

## References

- one-realm-mvp-scope.md §5.1 · §4 scope table · §3 roster
- current-to-end-state-engine.md II.3 (MVP-CRITICAL bullet), IV.2 MVP-lens
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md`
