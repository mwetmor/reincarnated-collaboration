# Dispatch — Gamora: Proxy Kernel Handoff (Session 2)

**STATUS:** READY TO FIRE — fires immediately after Session 2 lock (gandalf + Matt, 2026-06-12 Pattern B session)
**Authored by:** gandalf (Session 2 spec author; KR auto-commits per standing pattern)
**Target agent:** gamora
**Seam:** simulation/ (fight_engine, combatant, balance_loop, ProxyCombatant new module)
**Does NOT touch:** generation, output, telemetry/schema, demo, loadout

---

## 0. Context

Session 2 of the 5-session architecture cascade (gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md) is now locked. This dispatch contains five action items for gamora. Items 1-2 (ProxyCombatant entity model + simulate_fight extension) are BLOCKING for all proxy-family T4 hypothesis tests. Item 3 (companion modifier vector) enables companion balance validation in parallel. Item 4 (charge-stack energy type) is a kernel-change-protocol item. Item 5 (terrain-reactive geometry assessment) gates Session 3 scope.

**No existing kernel path changes.** All items are additive. Golden-master oracle remains the regression anchor for all changes (`simulation/spatial_gauntlet/golden_master/spatial_golden_master_season_001010_2026_06_11.json`; 27/27 structural tests at SDS=0.6).

---

## 1. ProxyCombatant entity model (BLOCKING — new kernel module)

**Scope:** Implement `ProxyCombatant` as a new entity class in `simulation/`. NOT an extension of `Combatant`. Implements the interface spec at Session 2 spec § 3.

**Key decisions:**
- ProxyCombatant is a fight-participant alongside the player (NOT an opponent)
- 14 proxy types map to this single interface using optional feature groups
- Behavioral tier ("minimal" | "mid" | "full") controls which features are active per instance
- Minimal tier (Resource Conduit, Warcry/Buff Spirit): HP optional; no position; no targeting
- Mid tier (Totem/Turret, Volatile Emitter, Terrain Anchor, Trap/Mine, Volatile Emitter, Slot-Queue Emitter, Delayed Position Shadow, Charged Threshold Proxy, Fragile Escort): position + targeting; no skill rotation
- Full tier (Passive Fighter, Autonomous Caster, Golem/Construct, Bodyguard): independent skill rotation + cooldown tracking

**Deliverables:**
1. New file: `simulation/proxy_combatant.py` — ProxyCombatant class + supporting types (ProxySkill, ProxyZoneEffect, ProxyResourceGen, ProxyDeathEvent, ProxyThresholdEvent, ProxyAccumulationState, ProxyEnergyState)
2. New file: `simulation/entity_from_proxy_dict.py` (or add to `combatant.py`) — constructor: builds ProxyCombatant from kit proxy fields
3. fight_engine.py: proxy participant loop — at each fight tick, call proxy behavioral dispatch per proxy type and tier; proxies act after player, before enemy response
4. fight_engine.py: proxy death handling — remove from active list; fire death_event if present
5. fight_engine.py: Bodyguard intercept mechanic — intercept_threshold_pct check per player hit event

**Proxy behavioral dispatch design note:** gamora designs the internal dispatch (the proxy action loop inside fight_engine) at implementation time. The interface spec defines what capabilities exist; gamora decides how fight_engine iterates over player_proxies and dispatches per behavioral_tier and proxy_type. Minimal coupling to player's fight loop is preferred: proxy actions are side-effects to the main player↔enemy loop, not structural modifications to it.

**Pass/fail (Phase 1 proxy smoke):**
- All 14 proxy types instantiate without error
- Minimal-tier types (no HP or position) survive a full fight with no fight_engine exceptions
- Mid-tier types (position + targeting) correctly target enemies in fight
- Full-tier types (skill rotation) execute at least 2 distinct skills in a standard fight
- Death events: at least one PROXY_FISSION test — proxy death spawns 2 sub-proxies at 60% ± 2% stats
- Bodyguard intercept: intercept event fires when player hit exceeds 20% max HP threshold
- `simulate_fight(player, enemy, player_proxies=None)` remains bit-identical to pre-extension baseline (golden-master self-verify: 0/60 delta)

**MIGRATION.md:** new section for ProxyCombatant entity model. Document:
- New files authored
- fight_engine.py modification sites (line references)
- simulate_fight signature extension (backward-compatible)
- FightResult additions (proxy telemetry fields)
- Vestigial-ontology charge: any new proxy interface surface must use substrate-truthful vocabulary (no new ontology-named fields; no new required kernel-schema fields that add legacy ontology vocabulary)

---

## 2. simulate_fight signature extension (BLOCKING — paired with Item 1)

**Current:** `simulate_fight(player: Combatant, enemy: Combatant) → FightResult`

**Extended:**
```python
def simulate_fight(
    player: Combatant,
    enemy: Combatant,
    player_proxies: list[ProxyCombatant] | None = None,
) → FightResult:
```

**Constraint:** `player_proxies=None` path must produce bit-identical output to the pre-extension baseline. This is the golden-master contract; verify via harness after extension.

**FightResult additions (additive; no existing field removal):**
```python
proxy_damage_contributed: float = 0.0          # total proxy-attributable damage
proxy_damage_by_type: dict[str, float] = {}    # keyed by proxy_type string
proxy_death_events: list[str] = []             # proxy_id values that died
proxy_resource_generated: float = 0.0          # from Resource Conduit type
```

star-lord telemetry: FightResult additions are internal-to-seam as long as proxy fields are not surfaced in star-lord's export schema. Surface to export in a separate dispatch (not this handoff).

---

## 3. Companion modifier vector application (NO kernel change — balance_loop caller side)

**Scope:** Implement companion modifier vector application in `simulation/balance_loop.py` at the companion pairing stage. This is a CALLER-SIDE change to balance_loop — no kernel modification.

**Application point:** Before `simulate_fight(player, enemy)` call, when a player kit has COMPANION_CONTRACT or MONSTER_PACT T4, adjust the player Combatant's parameters by the companion modifier vector stored in the companion kit's record.

**Five modifier types:**
| Modifier | Applied as | NPC cap | Monster cap |
|---|---|---|---|
| `damage_amp` | Multiplicative on player damage output | 1.15 | 1.10 |
| `cc_duration_mult` | Multiplicative on player CC duration | 1.25 | 1.35 |
| `survivability_mod` | Additive to effective HP/damage reduction | 0.10 | 0.0 |
| `resource_gen_mod` | Additive to resource generation rate | 0.10 | 0.05 |
| `aoe_radius_mod` | Additive to AoE skill radius | 0.15 | 0.10 |
| `enemy_cc_mult` | Multiplicative to enemy CC duration received (monster-exclusive) | 1.0 | 1.25 |

**Cap enforcement:** gamora adds a pre-application cap-check; if any modifier exceeds its type cap (e.g., rocket sets damage_amp=1.20 due to archetype mapping), clamp to cap and flag in telemetry.

**Validation protocol in balance_loop:** after companion modifier application, verify player WR delta vs no-companion baseline ≤ 0.10. If exceeded: log a WARN in telemetry output; do NOT silently pass.

**MIGRATION.md:** document modifier application site in balance_loop.py (line reference); confirm no new kernel file edits.

---

## 4. Charge-stack energy type — _ENERGY_CONFIGS entry (kernel-change-protocol item)

**Status:** This item is a KERNEL CHANGE per kernel-change-protocol (adding a new `energy_type` to `_ENERGY_CONFIGS`). It is GATED by: (a) DEFENSIVE_TRADEOFF gate condition update (per vestigial-ontology register 2026-06-12: any `energy_type` addition requires `_ENERGY_CONFIGS` table edit + DEFENSIVE_TRADEOFF gate condition update), and (b) kernel-change-protocol § 3.

**Behavior spec for charge-stack energy type:**
- Pool maximum: 10 stacks (maps to `actor.mana` pool maximum = 10)
- Starting value: 0 stacks
- Accumulation: +1 per enemy hit (on any player or proxy hit landing on an enemy); no passive regen; no decay
- Skill cost model: charged threshold skills SPEND all stacks on activation (spend-all); other skills cost 0 stacks (resource use is threshold-gated, not per-skill)
- Overflow: accumulation caps at 10; hits at cap do not add stacks

**_ENERGY_CONFIGS entry (gamora authors the exact dict form per combatant.py pattern):**
```python
"charge-stack": {
    "max": 10,
    "start": 0,
    "regen_on_hit": 1.0,      # per enemy hit
    "regen_per_tick": 0.0,
    "decay_rate": 0.0,
    "skill_cost_model": "threshold_spend_all",  # threshold skills spend all stacks; others cost 0
}
```

**DEFENSIVE_TRADEOFF gate update (required per register):** after adding charge-stack to `_ENERGY_CONFIGS`, update the DEFENSIVE_TRADEOFF eligibility gate: `energy_type == "mana"` check must explicitly list all energy_types that are NOT mana (charge-stack is a non-mana type; kit with charge-stack is NOT eligible for DEFENSIVE_TRADEOFF). This prevents the gate from silently including new types.

**Vestigial-ontology check (per register discipline):** "charge-stack" is a behavioral-descriptor value name (physical question: "how does this kit's resource accumulate?") — NOT an ontological vocabulary addition. Q2 = PHYSICAL. PASS. No register update required for this value addition.

**Gate-2 requirement for this item:** gamora must include charge-stack implementation in a Gate-2 handoff with:
- _ENERGY_CONFIGS entry authored
- DEFENSIVE_TRADEOFF gate condition updated
- Golden-master delta after charge-stack entry addition (should be zero: no existing Season 001010 kits have charge-stack energy_type)
- Kernel-change-protocol § 3 checklist completed

---

## 5. Terrain-reactive geometry — boundary assessment request

**Status:** This is a GAMORA ASSESSMENT REQUEST, not an implementation item. Session 3 will specify terrain-reactive geometry behavior fully. Before Session 3 fires, gamora inspects fight_engine to determine:

**Assessment questions:**
1. The spatial gauntlet already implements terrain-reactive geometry (via `spatial_gauntlet/`, post-Phase-3-repoint). Is the terrain-reactive geometry path accessible at the fight_engine level, or is it exclusively in the spatial call path?
2. Is terrain-reactive geometry (damage boost in terrain zone / CC extension in terrain / positional modifier by terrain type) implementable as a **caller-side geometry parameter** on Combatant skills, or does it require a new fight_engine branching path?
3. Does the current fight_engine `run_fight` function have a concept of "terrain type" or "zone type" that modifiers can reference? If not, what is the minimum kernel surface to add terrain-type as a fight parameter?

**Assessment output:** gamora authors a 1-page assessment note at `gamora/notes/2026-06-12-terrain-reactive-geometry-assessment.md` covering the three questions above. Session 3 spec uses this assessment to decide whether terrain-reactive geometry is caller-side only (preferred) or a kernel-change-protocol item.

**This assessment does NOT require Session 3 to have fired.** Gamora can assess the boundary from current code state immediately.

---

## 6. Sequencing and session context

| Item | Priority | Blocking? | Session dependency |
|---|---|---|---|
| 1. ProxyCombatant entity model | BLOCKING | Yes — all proxy-family T4 hypothesis tests | Session 2 lock |
| 2. simulate_fight extension | BLOCKING | Yes — paired with Item 1 | Session 2 lock |
| 3. Companion modifier vector | HIGH | No — can parallel with Items 1+2 | Session 2 lock |
| 4. Charge-stack energy type | MEDIUM | Via protocol only | Session 2 lock; kernel-change-protocol gate |
| 5. Terrain-reactive assessment | LOW | No — informs Session 3 only | Session 2 lock; assess before Session 3 |

Items 1+2 are the immediate priority. Item 3 can start in parallel. Item 4 fires after Items 1+2 smoke; requires explicit kernel-change-protocol gate. Item 5 is low-urgency but should land before Session 3 fires.

Sessions 3 and 4 run in parallel with gamora's kernel extension. Gamora does not wait for Sessions 3+4 to complete before beginning Items 1-3.

---

## 7. Gate-2 handoff structure

After Items 1+2 implementation and smoke:

**Gate-2 handoff note** at `gamora/notes/2026-06-12-proxy-kernel-handoff-gate-2.md`:
- ProxyCombatant entity model summary (new files, fight_engine modification sites)
- simulate_fight extension: golden-master self-verify output (0/delta expected on `player_proxies=None`)
- Proxy smoke results: per-tier type instantiation + basic fight pass/fail
- Companion modifier vector application: cap-check output + WR delta measurement
- Vestigial-ontology charge compliance (new surface names substrate-truthful; no new required kernel-schema ontology fields)
- MIGRATION.md version bump

---

**Author:** gandalf, 2026-06-12. Matt-authorized gamora kernel handoff; Session 2 cascade. Gamora: fire when you next engage.
