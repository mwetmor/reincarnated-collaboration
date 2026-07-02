# Dispatch — 2026-07-02 — rocket — demo summoner proxy decls (D2)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-07-02 (one-realm §5.2; the second of the two bounded engine asks)
**Estimated effort:** 0.5–1 day
**Acceptance:** 2–3 demo summoner kits carry real, hand-authored `proxies` payloads in the `proxy_vocabulary_bridge` vocabulary — replacing the `[]` every kit emits today — WITHOUT lifting `_DEFERRED_PROXY_BINS` (no generation un-gate, no emission-share trigger).
**Status:** READY — first fire (concurrent with D1; your output feeds D1's bundle). Gate-1 required before execution.

## Context

One Realm is Necromancer-themed; §3's summoner mandate is load-bearing — "a death-cult demo where nothing can be raised breaks the fantasy promise in minute one." The roster carries ≥1 summoner in the starting pool (ideally 1 summoner lieutenant too). Summoner kits are **hand-tuned, playtest-validated demo content** — only the *general* certification instrument stays launch-track (III.1b).

Today `proxy_vocabulary_bridge.py` emits `"proxies": []` on every kit (`:22-23`), because content-emit is gated (`_DEFERRED_PROXY_BINS = {proxy-light, proxy-heavy}`, `bc_target_composer.py:97,318`). The FIGHT mechanism is BUILT (W1+W2, 2026-06-22) — the sim runs a summoner end-to-end today given a kit with real `proxies`. What's missing for the demo is **hand-authored decls** on the 2–3 demo summoner kits. §5.2 rules hand-authored decls acceptable at demo scope. This is the demo's second engine ask, and it **feeds D1** — star-lord's bundle needs the summoner kits to carry these real payloads.

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §3 (summoner mandate), §5.2 (your ask), §4 (scope table)
- `current-to-end-state-engine.md` III.1b (the MVP-SPLIT block — demo = hand-authored decls; the emit un-gate stays launch)
- `agentic_orchestration/gamora/notes/2026-07-02-sim-two-state-inspection.md` §Q1 (the built proxy-combat path the decls feed) + §Q2 (the four scaffold fight-magnitudes — these are gamora's to calibrate, NOT yours to set)
- `generation/proxy_vocabulary_bridge.py` — the vocabulary + the 14-type proxy_type map, tier, geometry, range, targeting; the `proxies:[]` emit site (`:22-23`); the scaffold constants (`:68,77,232,255` — leave as SCAFFOLD, gamora calibrates)
- The proxy spec `simulation/math/spatial-proxy-combat-spec-*.md` (decl field surface)

## Math-before-code

Not new math. **Document the decl-authoring rationale**: for each of the 2–3 summoner kits, why this `proxy_type` (from the 14-type map) / tier / geometry / range / targeting — tie each to the kit's thematic identity (necromancer raise vs. a caster's conjure). This is a content-shape note, not a magnitude derivation. **Do NOT set the four fight magnitudes** (`damage_multiplier`, `base_hp`/`PROXY_REFERENCE_HP`, `proxy_max_active`/`PROXY_TIER_MAX_ACTIVE`, `attack_interval_s`) — those stay SCAFFOLD; gamora calibrates them if/when D3 is ratified.

## Cross-seam contract change? (Principle 6 gate)

**NO new cross-seam contract.** The `proxies` field already exists on `PlayerClassV2.to_dict()` (rocket-owned surface; W2 round-tripped the 6 spawner fields to gamora). You are populating an existing field on hand-picked kits, not changing the schema. Your output flows into D1's bundle via the existing surface.
- `Round-trip: not applicable — no cross-seam contract change; the proxies surface already exists and was round-tripped at W2. The decls flow to D1 via the existing PlayerClassV2 surface.`

## Scope

- [ ] Pick the 2–3 demo summoner kits (coordinate roster with gandalf/§3: ≥1 starting-pool summoner; ideally 1 summoner lieutenant — the necromancer-raising-adds Structure-1 boss is thematically perfect)
- [ ] Hand-author real `proxies` payloads for each (proxy_type / tier / geometry / range / targeting in the bridge vocabulary)
- [ ] Content-shape note (per-kit decl rationale, thematic tie)
- [ ] Verify the kits now emit non-empty `proxies` (smoke: `to_dict()` shows real payloads)
- [ ] Confirm `_DEFERRED_PROXY_BINS` stays DOWN (no generation un-gate) and the four fight-magnitudes stay SCAFFOLD (gamora's lane)
- [ ] AGENT_STATE.md updated
- [ ] Tag: `rocket/v-demo-summoner-proxy-decls-1`

## Acceptance criteria

- [ ] 2–3 demo summoner kits emit real `proxies` payloads (not `[]`)
- [ ] `_DEFERRED_PROXY_BINS` unchanged (no bin lift); no 25% emission-share trigger; no generation path un-gated
- [ ] The four scaffold fight-magnitudes untouched (still tagged SCAFFOLD — gamora calibrates)
- [ ] Round-trip: not applicable (see Principle 6 above)

## Out of scope (explicit non-goals)

- Lifting `_DEFERRED_PROXY_BINS` / the generation proxy path (launch-track III.1b)
- The 25% proxy emission share (launch-track)
- Setting/calibrating the four fight magnitudes (gamora's lane — D3 if ratified)
- Support-role bin un-gate (rides III.1b, launch)
- Any kit beyond the 2–3 demo summoners

## Quality criterion

**Game-quality goal:** the death-cult fantasy is intact from minute one — the player can raise something. The summoner reads as a *summoner* (thematically legible proxy identities), not a stat block with an add-count.

**Refutation conditions (surface if any apply):**
- A chosen proxy_type contradicts the kit's necromancer/caster identity (§3 fantasy)
- The decls quietly require a fight-magnitude change (that's gamora's D3, not yours — flag it)
- Authoring these decls pressures the `_DEFERRED_PROXY_BINS` gate (it must stay down)
- The roster pick conflicts with gandalf's §3 Goldilocks / lieutenant curation

## Open questions for the agent to resolve (document your calls)

- Exactly which 2–3 kits (confirm against gandalf's §3 roster curation before finalizing)
- Whether the summoner lieutenant reuses the near-existing enemy-side `boss_with_adds` shell as its raise-adds fantasy (§3 notes this is thematically perfect + near-existing tech)

## References

- one-realm-mvp-scope.md §3 (summoner mandate), §5.2
- current-to-end-state-engine.md III.1b (MVP-SPLIT)
- gamora sim two-state inspection §Q1/§Q2
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md`
