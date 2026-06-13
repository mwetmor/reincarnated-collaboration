# Dispatch — Gamora: Proxy Kernel Handoff (Session 2)

**STATUS:** **FIRED 2026-06-12 — Session 2 § 3 RATIFIED by Matt (with three riders, applied to the spec).** All 5 items authorized. Item 4 UN-HELD (Q9 RULED — Matt-ratified, Session 1 batch: spend-all + passive per-stack bonus while held; ruling record `gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md` § 1 Q9); Item 4 still sequences AFTER Items 1+2 smoke per § 8 and remains kernel-change-protocol gated. (gandalf + Matt, 2026-06-12 Pattern B session; normalization pass applied 2026-06-12)

> **RATIFICATION RIDERS (Matt, 2026-06-12 — applied to Session 2 spec § 3):**
> 1. **`"summon"` struck** from ProxyThresholdEvent event types — proxies do NOT summon (proxies-of-proxies ruling, ruling record § 4); PROXY_FISSION death-split is the sole bounded exception
> 2. **Fission bounds are interface fields, kernel-enforced:** `fission_recursion_cap: int = 4` (max TOTAL fission entities) + `fission_expiry_s: float = 30.0` (sub-proxy lifetime) on ProxyDeathEvent
> 3. **Smoke-population composition (Items 1+2):** the smoke MUST include deliberately proxy-stacked kits (PROXY_SOVEREIGNTY + DUAL_PROXY-style compositions pushed hard) so the proxy-primary empirical gate (`gandalf/notes/2026-06-12-proxy-primary-architecture-recognition.md` § 5) has reachability evidence for `proxy_contribution_pct` ~0.5 — not just one-proxy bolt-on samples
>
> **DESIGN LATITUDE GRANT (Matt, 2026-06-12):** significant implementation-design latitude is granted wherever this dispatch or Session 2 § 3 marks gamora-owned judgment: § 3.3 supporting-type struct layout and field design; behavioral-tier dispatch architecture inside fight_engine; hook siting for death events, on-hit accumulation, and the Q9 passive held-bonus; fission cap/expiry enforcement mechanics; the Item 5 terrain boundary judgment; and perf tradeoffs at hot paths. **Latitude covers HOW, not WHAT:** locked BC axis vocabulary, the ratified interface shape (§ 3.2 fields + symmetric `proxies_a`/`proxies_b` kwargs), the brownfield guarantee (golden-master regression anchor), the riders above, and rocket-supplies/kernel-reads magnitude ownership are not negotiable. Where a latitude call would change design INTENT or a ratified surface, surface to gandalf before implementing — otherwise exercise judgment and record the call in the Gate-2 handoff.
**Authored by:** gandalf (Session 2 spec author; KR auto-commits per standing pattern)
**Target agent:** gamora
**Seam:** simulation/ (fight_engine, combatant, balance_loop, ProxyCombatant new module)
**Does NOT touch:** generation, output, telemetry/schema, demo, loadout

---

> **NORMALIZATION PASS (gandalf, 2026-06-12, Matt-authorized):** kernel premises in this dispatch were corrected against engine code (read-only verification; legibility verdict § 6): symmetric `simulate_fight` signature (§ 2); `_ENERGY_CONFIGS` actual 3-tuple shape + new-behavior scope (§ 4); terrain greenfield premise (§ 5). ~~Item 4 HOLDS on Q9~~ **Q9 RULED same-day (Session 1 ratification): Item 4 UN-HELD** — behavior spec amended per § 4 below. All items fire on Session 2 § 3 ratification (Item 4 post Items 1+2 smoke).

## 0. Context

Session 2 of the 5-session architecture cascade (gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md) is in DRAFT status — it locks on Matt's ratification (Session 2 § 3 interface ratification is the gate for this dispatch). This dispatch contains five action items for gamora. Items 1-2 (ProxyCombatant entity model + simulate_fight extension) are BLOCKING for all proxy-family T4 hypothesis tests. Item 3 (companion modifier vector) enables companion balance validation in parallel. Item 4 (charge-stack energy type) is a kernel-change-protocol item ON HOLD pending Q9. Item 5 (terrain-reactive geometry assessment) gates Session 3 scope.

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

**Proxy behavioral dispatch design note:** gamora designs the internal dispatch (the proxy action loop inside fight_engine) at implementation time. The interface spec defines what capabilities exist; gamora decides how fight_engine iterates over the proxy lists and dispatches per behavioral_tier and proxy_type. Minimal coupling to the main combatant loop is preferred: proxy actions are side-effects to the main a↔b loop, not structural modifications to it.

**Pass/fail (Phase 1 proxy smoke):**
- All 14 proxy types instantiate without error
- Minimal-tier types (no HP or position) survive a full fight with no fight_engine exceptions
- Mid-tier types (position + targeting) correctly target enemies in fight
- Full-tier types (skill rotation) execute at least 2 distinct skills in a standard fight
- Death events: at least one PROXY_FISSION test — proxy death spawns 2 sub-proxies at 60% ± 2% stats
- Bodyguard intercept: intercept event fires when player hit exceeds 20% max HP threshold
- `simulate_fight(combatant_a, combatant_b, proxies_a=None, proxies_b=None)` remains bit-identical to pre-extension baseline (golden-master self-verify: 0/60 delta)

**MIGRATION.md:** new section for ProxyCombatant entity model. Document:
- New files authored
- fight_engine.py modification sites (line references)
- simulate_fight signature extension (backward-compatible)
- FightResult additions (proxy telemetry fields)
- Vestigial-ontology charge: any new proxy interface surface must use substrate-truthful vocabulary (no new ontology-named fields; no new required kernel-schema fields that add legacy ontology vocabulary)

---

## 2. simulate_fight signature extension (BLOCKING — paired with Item 1)

**Current (verified at `simulation/fight_engine.py:107`):** the kernel is SYMMETRIC — `simulate_fight(combatant_a: Combatant, combatant_b: Combatant, ...)` with existing kwargs (max_duration, seed, spatial/gauntlet parameters). No player/enemy asymmetry exists at the kernel; roles are caller-side.

**Extended (symmetric, matching kernel convention):**
```python
def simulate_fight(
    combatant_a: Combatant,
    combatant_b: Combatant,
    *,
    proxies_a: list[ProxyCombatant] | None = None,
    proxies_b: list[ProxyCombatant] | None = None,
    # ... existing kwargs unchanged
) → FightResult:
```

Symmetry preserves the kernel's design invariant AND gives the validation seam enemy-side proxies (gauntlet bosses with adds) for free. The player-proxy use case passes `proxies_a` only.

**Constraint:** the `proxies_a=None, proxies_b=None` path must produce bit-identical output to the pre-extension baseline. This is the golden-master contract; verify via harness after extension.

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

**Application point:** Before the `simulate_fight` call in balance_loop, when a player kit has COMPANION_CONTRACT or MONSTER_PACT T4, adjust the player-side Combatant's parameters by the companion modifier vector stored in the companion kit's record.

**Six modifier types:**
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

## 4. Charge-stack energy type — _ENERGY_CONFIGS entry (kernel-change-protocol item — **UN-HELD: Q9 RULED 2026-06-12**)

**Q9 RULING (Matt-ratified 2026-06-12, Session 1 batch — ruling record § 1 Q9):** **spend-all PLUS a passive per-stack bonus while stacks are held.** The pure spend-all sawtooth (mean ≈0.25–0.5, high variance) never measures into the locked Axis 5 charge-stack bin (build-then-HOLD: mean ≥0.75, var <0.20); the passive held-bonus makes holding a real strategy. Rocket varies passive-vs-burst magnitudes per kit (rocket dispatch Item 10) so the optimal-rotation solver yields hold-optimal kits (→ charge-stack bin) AND spend-optimal kits (→ generator-spender bin). Zero lock amendment.

**Status:** This item is a KERNEL CHANGE per kernel-change-protocol (adding a new `energy_type` to `_ENERGY_CONFIGS`). It is GATED by: (a) ~~Q9 ruling~~ RESOLVED, (b) DEFENSIVE_TRADEOFF gate condition update (per vestigial-ontology register 2026-06-12: any `energy_type` addition requires `_ENERGY_CONFIGS` table edit + DEFENSIVE_TRADEOFF gate condition update), and (c) kernel-change-protocol § 3. Sequencing: fires AFTER Items 1+2 smoke (§ 8).

**Actual `_ENERGY_CONFIGS` shape (verified at `simulation/combatant.py:322`):** `dict[str, tuple[float, bool, float]]` — `(pool_max, start_full, regen_per_s)`. Current entries: rage `(100.0, False, 0.0)`, combo `(5.0, False, 0.0)`, focus `(100.0, True, -5.0)`, stamina-as-resource `(150.0, True, 20.0)`. The original draft's rich dict form (`regen_on_hit`, `decay_rate`, `skill_cost_model`) does NOT exist in the kernel — those are NEW kernel behaviors, not config values:

- **On-HIT accumulation is new.** The closest precedent is combo, which accumulates on primary-attack USE (`fight_engine.py:750`), not on hit-landing. Charge-stack's "+1 per enemy hit" requires a new accumulation hook at the hit-resolution site.
- **Spend-all cost model is new.** No existing energy type spends its full pool on a threshold skill; per-skill costs are the current model. The threshold-spend-all dispatch is a new mechanism.

**Behavior spec for charge-stack energy type (LOCKED per Q9 ruling 2026-06-12):**
- Pool maximum: 10 stacks → tuple form `(10.0, False, 0.0)` plus the new behaviors below implemented as code, not config
- Starting value: 0 stacks
- Accumulation: +1 per enemy hit (on any player or proxy hit landing on an enemy); no passive regen; no decay
- Skill cost model: charged threshold skills SPEND all stacks on activation (spend-all); other skills cost 0 stacks
- **Passive held-bonus (Q9 ruling — third new kernel behavior):** while stacks are held, the combatant gains a passive per-stack bonus (e.g., +X% damage per stack; magnitude is kit data from rocket, not kernel constant). Implemented as a damage-resolution modifier reading current stack count. Rocket supplies `per_stack_passive_bonus` and threshold-burst magnitudes per kit (rocket dispatch Item 10); the kernel reads, never chooses
- Overflow: accumulation caps at 10; hits at cap do not add stacks

**Scope honesty:** this item is larger than a one-row table edit. Gamora sizes the accumulation hook + spend dispatch as part of the kernel-change-protocol checklist; if the new hooks touch hit-resolution hot paths, surface the perf implication in the Gate-2 handoff.

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

**Corrected premise (normalization pass, code-verified):** terrain-reactivity is **GREENFIELD**. The spatial gauntlet does NOT implement terrain-reactive damage mechanics — the only terrain-adjacent mechanic anywhere in the sim is `ChokeZone` in `spatial_gauntlet/arena.py:104`, which clamps MOVEMENT only (zero damage/element/CC interaction). The original draft's "already implements terrain-reactive geometry" claim is retracted.

**Assessment questions:**
1. Is `ChokeZone`'s zone-position infrastructure (position-in-zone testing) reusable as the substrate for terrain ZONES with damage/CC semantics, or is a separate terrain-zone model cleaner?
2. Is terrain-reactivity (damage boost on matching terrain / CC extension in terrain / positional modifier by terrain type) implementable as a **caller-side parameter** (`terrain_type` kwarg per Session 3 § 3.2) with skill-tag checks at damage resolution, or does it require a new fight_engine branching path?
3. Does the current fight_engine have ANY concept of "terrain type" or "zone type" that damage modifiers can reference? (Expected answer per code inspection: no.) What is the minimum kernel surface to add terrain-type as a fight parameter?

**Assessment output:** gamora authors a 1-page assessment note at `gamora/notes/2026-06-12-terrain-reactive-geometry-assessment.md` covering the three questions above. Session 3 spec uses this assessment to decide whether terrain-reactive geometry is caller-side only (preferred) or a kernel-change-protocol item.

**This assessment does NOT require Session 3 to have fired.** Gamora can assess the boundary from current code state immediately.

---

## 6. Sequencing and session context

| Item | Priority | Blocking? | Session dependency |
|---|---|---|---|
| 1. ProxyCombatant entity model | BLOCKING | Yes — all proxy-family T4 hypothesis tests | Session 2 lock |
| 2. simulate_fight extension | BLOCKING | Yes — paired with Item 1 | Session 2 lock |
| 3. Companion modifier vector | HIGH | No — can parallel with Items 1+2 | Session 2 lock |
| 4. Charge-stack energy type | **UN-HELD (Q9 ruled 2026-06-12)** | Via protocol only | Items 1+2 smoke + kernel-change-protocol gate |
| 5. Terrain-reactive assessment | LOW | No — informs Session 3 only | Session 2 lock; assess before Session 3 |

Items 1+2 are the immediate priority. Item 3 can start in parallel. Item 4 is UN-HELD (Q9 ruled 2026-06-12) and fires post Items 1+2 smoke, with explicit kernel-change-protocol gate. Item 5 is low-urgency but should land before Session 3 fires. **Note (Session 1 ratification):** the Items 1+2 smoke population additionally services the proxy-primary empirical gate — `proxy_contribution_pct` ~0.5 reachability check per `gandalf/notes/2026-06-12-proxy-primary-architecture-recognition.md` § 5; include the metric in smoke telemetry output.

**Queued behind Items 1–5 (Session 1 catalog expansion, ratified 2026-06-12 — NOT in this dispatch's scope; sized here for visibility):** the four new T4 strategies (ruling record § 2) carry five kernel-side mechanic contracts that will arrive as a follow-on dispatch after this one completes: (a) `on_kill` corpse-burst hook with recursion cap 3 (GEOMETRY_PROPAGATION cascade); (b) overkill-surplus + threshold-hit splash resolution (GEOMETRY_PROPAGATION overkill); (c) vengeance-pool accumulation on the existing `on_take_damage` hook + next-skill discharge (RETRIBUTION_ENGINE — shares SACRIFICE_ASCENDANCY's hook site); (d) damage-continuity / DoT-stack-count state tracking (PERSISTENCE_ENGINE); (e) unhit-window Phase-stack accumulation + stack-consuming hit negation + avoidance-event telemetry (PHASE_MOMENTUM; the avoidance-event log also services the ratified Test 3 dodger criterion). Do not start these now; flagged so Items 1+2 architecture choices don't paint these into a corner.

Sessions 3 and 4 run in parallel with gamora's kernel extension. Gamora does not wait for Sessions 3+4 to complete before beginning Items 1-3.

---

## 7. Gate-2 handoff structure

After Items 1+2 implementation and smoke:

**Gate-2 handoff note** at `gamora/notes/2026-06-12-proxy-kernel-handoff-gate-2.md`:
- ProxyCombatant entity model summary (new files, fight_engine modification sites)
- simulate_fight extension: golden-master self-verify output (0/delta expected on `proxies_a=None, proxies_b=None`)
- Proxy smoke results: per-tier type instantiation + basic fight pass/fail
- Companion modifier vector application: cap-check output + WR delta measurement
- Vestigial-ontology charge compliance (new surface names substrate-truthful; no new required kernel-schema ontology fields)
- MIGRATION.md version bump

---

**Author:** gandalf, 2026-06-12. Matt-authorized gamora kernel handoff; Session 2 cascade. Gamora: fire when you next engage.

---

## Completion record

**Completed by:** gamora, 2026-06-12. All five items delivered + empirically validated.

| Item | Status | Gate evidence |
|---|---|---|
| 1. ProxyCombatant entity model | ✓ complete | proxy smoke 16/16; 14/14 type instantiation; fail-loud on unknown type; PROXY_FISSION lineage cap 4; bodyguard intercept threshold-gated |
| 2. simulate_fight extension | ✓ complete | golden-master self-verify **0/60** on `proxies_a=None, proxies_b=None` (bit-identical brownfield); FightResult additions additive default-neutral; owner-DPS damage basis (Disc #11 correction, contribution re-measured 0.556 ≥ 0.45 gate) |
| 3. Companion modifier vector (caller-side) | ✓ complete | companion smoke 15/15; NO kernel edit; golden-master 0/60; NPC/monster cap columns; cc via deepcopy-isolated control-duration scaling; WR-delta guard |
| 4. Charge-stack energy type (kernel-change-protocol) | ✓ complete | charge-stack smoke 8/8 (passive ratio EXACTLY 1.5, burst EXACTLY 6.0); golden-master 0/60 (§6.6 dead-code-for-mana-corpus confirmed); semantic-ordering note (Disc #12) |
| 5. Terrain-reactive assessment | ✓ delivered | 1-page note; greenfield confirmed; Session-3 recommendation = caller-side `terrain_type` kwarg |

**Brownfield guarantee held at EVERY gate** — golden-master 0/60 after Items 1+2, after Item 4, after Item 3. Three smoke harnesses green. No star-lord schema change (proxy FightResult fields internal-to-seam; export surfacing deferred to a separate dispatch).

**Engine commits:** `3102363` (Items 1+2), `dae0349` (Item 4), `e00cb6d` (Item 3), `d2ea435` (MIGRATION v1.66 + AGENT_STATE checkpoint).
**Collab commit:** `2dc8efd` (Gate-2 handoff + terrain assessment notes).
**Artifacts:** math note `simulation/math/proxy-kernel-extension-2026-06-12.md` (§0–§11, code-line citations); MIGRATION.md v1.66; Gate-2 handoff `gamora/notes/2026-06-12-proxy-kernel-handoff-gate-2.md` (7 design-latitude calls recorded); terrain assessment `gamora/notes/2026-06-12-terrain-reactive-geometry-assessment.md`.
**Routes to jack-ryan:** decisions-log entry for charge-stack semantic ordering (Disc #12) + new `energy_type` value; Gate-2 review of the three smokes + golden-master evidence against the ratified §3 interface + three riders; confirm the latitude calls sit within Matt-granted HOW-latitude.
**No tag** — milestone tag pending jack-ryan Gate-2.
**Follow-ons queued behind Gate-2:** live COMPANION_CONTRACT/MONSTER_PACT pairing wiring (rocket emits companion records); Session-3 terrain_type caller kwarg; proxy export-surfacing dispatch (star-lord); T4/proxy-magnitude reachability measurement (rocket).
