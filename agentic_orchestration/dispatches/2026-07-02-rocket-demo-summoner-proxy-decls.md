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

---

## Completion record — rocket, 2026-07-02

**Status:** DONE. Tag `rocket/v-demo-summoner-proxy-decls-1`. Smoke **53/53 ALL-PASS**. Auto-committed (authorized cycle work per CLAUDE.md); NOT pushed (Matt-gated).

**What shipped (2 additive files + 1 smoke; ZERO edits to the gate or the four SCAFFOLD magnitudes):**
- `reincarnated-engine/src/reincarnated/generation/demo_summoner_kits.py` — 3 hand-authored demo summoner summon-skill payloads (`DEMO_SUMMONER_SPECS`) + `demo_summoner_proxies(kit_id)` / `all_demo_summoner_proxies()` helpers that run each through the EXISTING `proxy_vocabulary_bridge.build_proxies_surface`. Payloads carry ONLY the rocket-owned identity inputs (`proxy_geometry`/`proxy_acquisition`/`effect_category`/`proxy_count`/`proxy_duration_s`/`proxy_spawn_cadence_s`); magnitude inputs left None → bridge fills SCAFFOLD.
- `reincarnated-engine/src/reincarnated/generation/math/demo-summoner-proxy-decls-content-shape-2026-07-02.md` — the Discipline #1 content-shape note (per-kit rationale; roster pick; scaffold-vs-final ownership; all four refutation-condition checks answered).
- `reincarnated-engine/src/reincarnated/generation/notes/demo_summoner_proxy_decls_smoke_2026_07_02.py` — the 53-check smoke.

**The 3 demo summoners (roster rationale documented; §3 mandate satisfied):**
| Kit (working id) | §3 slot | proxy_type / tier | geometry → range / targeting | fantasy |
|---|---|---|---|---|
| `demo_bone_acolyte` | **starting-pool summoner** (§3 floor — "raise something in minute one") | golem_construct / full | melee_strike → 1.5 m / taunt | line of raised skeletons (count 2, permanent-until-death) |
| `demo_crypt_lieutenant` | **summoner lieutenant** (§3 ideal — the Structure-1 raising-adds boss, becomable) | golem_construct / full | ground_slam → 1.5 m / taunt | one heavy bound bone-guard (count 1, slower cadence) |
| `demo_gravecaller` | flex caster-summoner (the §20d 2nd summon-verb) | autonomous_caster / full | projectile → 10.0 m / nearest | spectral archer from the backline (count 1, 30s fade) |

**Scope + acceptance (all met):**
- [x] 2–3 demo summoner kits emit real, non-empty `proxies` (3 shipped; each 1 decl, JSON-serializable, round-trips through the real sim consumer `entity_from_proxy_dict`).
- [x] `_DEFERRED_PROXY_BINS` UNCHANGED — zero diff on `bc_target_composer.py`; no generation un-gate; no 25% emission-share trigger.
- [x] The four scaffold fight-magnitudes UNTOUCHED — zero diff on `proxy_vocabulary_bridge.py`; smoke asserts each decl carries the scaffold defaults (`damage_multiplier=1.0`, `base_hp=REFERENCE×tier_factor`, `proxy_max_active=tier-default`, `attack_interval_s=DEFAULT`). gamora's lane (D3).
- [x] Round-trip: N/A — no cross-seam schema change; `proxies` already exists on `PlayerClassV2.to_dict()` (W2 round-tripped). Decls flow to D1 via the existing surface.
- [x] Content-shape note written; AGENT_STATE updated; tagged.

**§71 open question — RESOLVED YES:** the summoner lieutenant reuses the `boss_with_adds` raise-adds fantasy at the FANTASY level; mechanically the player-side uses the W1/W2 ally-proxy path (not an enemy-shell re-skin). Two shells, one fantasy — no cross-seam build here.

**One flag for gandalf (§3 curation, NOT a blocker):** the three kit ids are *working* ids. The decl payloads are keyed to FANTASY, not to a fixed roster slot — they travel onto whatever kit ids gandalf's final §3 Goldilocks/lieutenant curation assigns. Please confirm S1/S2/S3 map onto the final roster (starting-pool summoner + lieutenant satisfy the mandate floor+ideal; S3 is the flex — drop it if the curation prefers 2). No conflict detected with §3 as written.

**Refutation conditions — none triggered:** (1) no proxy_type contradicts the necromancer/caster identity (golem_construct = raise-a-body, autonomous_caster = conjure-a-spectre; no engineer/alchemist types); (2) the decls consume scaffold magnitudes as-is — no quiet magnitude change required; (3) no pressure on `_DEFERRED_PROXY_BINS` (hand-authoring bypasses generation); (4) no roster conflict with gandalf's §3 (flagged the id-mapping for confirmation).

**Signed:** rocket (generation seam), 2026-07-02.
