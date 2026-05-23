# Geometry Palette — Discussion and Decisions

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

## Status

Discussed and decided in working session 2026-05-08, building on findings from `../collaboration-handoff/08-decomposition-report.md` (which surfaced the missing-melee-geometry gap) and the design intent in `../collaboration-handoff/06-trial-room-and-class-scoping.md`. Captured here as the geometry palette that the dimensional generation pipeline (Option C in `../collaboration-handoff/04-decision-options.md`) should produce against. Not yet a formal `decisions-log` entry; will be promoted alongside the architectural decision.

## Why this exists

Two facts force a comprehensive geometry palette decision *now*, not incrementally:

1. **Generation is emergent (not template-driven).** Per `../collaboration-handoff/08-decomposition-report.md` Finding 1, the engine's class generator takes element as input and derives archetype labels post-hoc. There is no archetype template to "demand" a geometry type. The generator picks from whatever is available in the ability grammar. **Whatever is not in the palette cannot appear in any generated output.** Waiting "until an archetype demands it" is incoherent under this generation model.

2. **The decomposition exposed concrete gaps.** Both physical warriors in season_000042 use `projectile` geometry on their primary attack — because the grammar has no melee option. This is the same shape of gap that any other unrepresented mechanical concept would produce: forced, wrong-fit fallbacks rather than absent classes. Building the missing geometry is part of making dimensional generation honest.

The palette must therefore be sized to span the design space we want emergent archetypes to live in.

## The consumability filter

Geometry types are consumed by two downstream pipelines beyond the engine's own simulator:

- **Text-LLM consumer** — generates ability descriptions, naming prompts, single-frame "hero shot" descriptions. Struggles with motion-defining and temporally-extended effects (a "warrior spins" is hard to render as a still description).
- **VFX consumer** — Claude connectors that generate Three.js (now) and Unity (later) code for visual effects. Three.js handles particles, meshes, projectiles, AOE indicators, beams, basic animation. Struggles with: complex character animation (wants pre-rigged Mixamo assets), AI behavior trees, sustained interactive effects, multi-stage state machines.

A geometry type's **consumability score** is the worse of the two — both consumers must be able to deliver, or the type is excluded regardless of mechanical merit. The scale used below: 5 = trivially consumable; 4 = easy with minor effort; 3 = moderate, possible with care; 2 = strains one or both consumers significantly; 1 = unviable for current tooling.

This filter does substantive pruning. About a third of candidates that would otherwise be CORE drop to DECIDE or DEFER once cost-of-rendering and cost-of-describing are taken into account.

## Decision table

| # | Type | Status | Consumability | Limiting factor | Damage radius | Notes |
|---|------|--------|---------------|-----------------|---------------|-------|
| 1 | `single_target` | CORE (current) | 5 | — | single_target | instant generic hit |
| 2 | `projectile` | CORE (current) | 5 | — | single_target | magical bolt |
| 3 | `cone` | CORE (current) | 5 | — | AOE | frontal fan |
| 4 | `circle` | CORE (current) | 5 | — | AOE | radial around caster |
| 5 | `line` | CORE (current) | 5 | — | AOE | one-shot line |
| 6 | `persistent_zone` | CORE (current) | 4 | — | AOE | placed, persists |
| 7 | `melee_strike` | CORE (NEW) | 5 | — | single_target | close-range single hit; requires adjacency |
| 8 | `melee_arc` | CORE (NEW) | 5 | — | AOE | close-range frontal sweep; requires adjacency |
| 9 | `ground_slam` | CORE (NEW) | 4 | — | AOE | close-range AOE around caster; requires adjacency |
| 10 | `ranged_physical` | CORE (NEW) | 5 | — | single_target | ballistic (bow/crossbow/sling/throwing); pierce/multishot capable; distinct from `projectile` in trajectory and accuracy mechanics |
| 11 | `ground_targeted_circle` | CORE (NEW) | 4 | — | AOE | placed AOE at cursor location; absorbs `delayed_strike` via optional delay parameter |
| 12 | `teleport` | CORE (NEW) | 4 | — | other | instant relocation; absorbs `dash_movement` (aesthetic difference only) |
| 13 | `self_buff` | CORE (NEW) | 5 | — | other | applies to caster only; absorbs solo-case `ward/shield_zone` |
| 14 | `totem` | CORE (NEW) | 4 | — | AOE | placed entity that pulses effects from a fixed location; no AI, no movement; simpler than full summon |
| 15 | `aura` | CORE-MARGINAL (NEW) | 3 | VFX (particle-on-moving-rig) | AOE | sustained radial AOE that ticks while active, follows caster; generator restricts to archetypes that clearly demand sustained effects (paladin / druid) |
| 16 | `beam_channel` | CORE-MARGINAL (NEW) | 3 | VFX (sustained interactive render) | AOE | sustained line held while channeling; generator restricts to channeled-magic archetypes (lightning-mage, ray-of-frost mage) |
| 17 | `summon_combatant` | STAGED (NEW) | 1 | both (AI entity, multi-actor sim) | other | in palette as design intent; generator excludes until multi-actor sim + minion AI exist (Phase 2 work) |
| 18 | `ally_target` | STAGED (NEW) | 4 | depends on summon (no other allies in solo play) | single_target | activates when summoner archetypes are enabled |
| 19 | `ally_radius` | STAGED (NEW) | 4 | depends on summon | AOE | activates when summoner archetypes are enabled |
| 20 | `delayed_strike` | COLLAPSED | — | — | — | merged into `ground_targeted_circle` with optional delay parameter |
| 21 | `dash_movement` | COLLAPSED | — | — | — | merged into `teleport` |
| 22 | `ward/shield_zone` | COLLAPSED | — | — | — | merged into `self_buff` for the solo case; revisit if multi-actor allies are admitted |
| 23 | `dash_attack` | DEFER | 2 | text (motion-defines hit area) | — | express as movement-animation + `melee_strike` at runtime; not a distinct geometry |
| 24 | `leap_strike` | DEFER | 3 | VFX (vertical motion + landing) | — | express as `ground_slam` + travel animation |
| 25 | `whirlwind` | DEFER | 1 | both (motion-defining) | — | express as movement + `ground_slam` if needed |
| 26 | `trap` | DEFER | 2 | both (multi-stage state machine) | — | revisit if rogue/ranger archetypes concretely demand it |
| 27 | `counter` | DEFER | 2 | both (reactive trigger system) | — | express as buff + conditional reflect in existing grammar at lower fidelity |
| 28 | `wall_construct` | DEFER | 2 | both (pathfinding, environmental) | — | game-engine work, not VFX work; revisit only if a defensive archetype clearly demands it |

## Damage-radius diversity

The generator picks geometry types to satisfy role profiles (primary_attack, burst_damage, area_damage, damage_over_time, defensive, utility). Diversity within each radius category is what lets emergent archetypes feel mechanically distinct.

| Category | CORE only | + CORE-MARGINAL | + STAGED |
|----------|-----------|------------------|----------|
| **single_target** | 4 | 4 | 5 |
| **AOE** | 8 | 10 | 11 |
| **other** | 2 | 2 | 3 |
| **total active** | **14** | **16** | **19** |

**Read of the balance:**

- **Single-target (4 types active):** instant generic, magical projectile, close physical, ranged ballistic. Enough variety to cover primary_attack across all archetypes. No need to add more.
- **AOE (10 types active including marginal):** the bulk of the palette, mirroring ARPG reality. Variety covers caster-centered (`circle`, `ground_slam`, `aura`), placed (`persistent_zone`, `ground_targeted_circle`, `totem`), frontal (`cone`, `melee_arc`), and linear (`line`, `beam_channel`). Each radius/positioning combination is represented.
- **Other (2 types active):** intentionally small. Most utility is expressible as effect-on-`self_buff` or position-via-`teleport`. Grows only if summoner is enabled.

This balance gives the generator enough expressivity to produce diverse archetype profiles without the simulator carrying every conceivable type.

## Decisions explained

### Summoner is STAGED, not DEFERRED

The summoner question is the highest-leverage call in this palette. Reasoning for the staged decision:

- **Conceptual fit is real.** Procedural monster generation already exists. A summoned minion is conceptually a smaller AI-controlled combatant — exactly what the dimensional generator could produce as an output. The generation infrastructure is reusable.
- **Multi-actor sim is real expansion.** The simulator currently models 1v1 (player + monster gauntlet). Summoning means N+1 vs M actors per fight: pairing logic for damage resolution, combat pacing with multiple allies, target prioritization on both sides. Real work, but not impossibly hard.
- **Solo-gameplay constraint.** The pre-existing constraint (`../collaboration-handoff/06-trial-room-and-class-scoping.md` § "Mechanic framing") rejects "ARPG real-time control of multiple actors as confounding." A summoner with AI-controlled minions doesn't violate the *control* clause (you cast, the minion fights autonomously). Whether it violates the *party* clause is a design call. ARPG convention treats summoner pets as abilities, not party members (Diablo necromancer, PoE zombies); leaning toward admitting summoner with caveats: AI-only, transient, low cap (≤3 simultaneous).
- **Renderability cost is real.** A second actor needs rigging, animation, AI, pathfinding. Three.js can handle a single autonomous entity but it's significant work; Unity later eases this somewhat.

The staged approach respects all three constraints simultaneously: emergent generation needs the palette comprehensive (so summoner geometry is in the design); the renderability constraint says we shouldn't ship summoner classes until consumers can express them (so they're excluded from active generation); the architectural decision's immediate scope doesn't expand (so the C estimate doesn't inflate). Summoner geometry activates as a Phase 2 capability when multi-actor sim and minion AI exist.

The summoner question should be ratified by the project owner and son before this is final. The staging is a conservative path that keeps the option open without blocking immediate work.

### Marginal types (`aura`, `beam_channel`) stay in but are generator-restricted

Both have consumability 3 — Three.js can render basic versions, Unity polish later. They're worth keeping because each provides a unique class-identity expression that no other type covers:

- `aura` — sustained-radial expression for paladin/druid identity. No other geometry expresses "ongoing presence around the caster."
- `beam_channel` — channeled-magic identity for lightning-mage / ray-of-frost archetypes. No other geometry expresses "sustained directional power."

Generator validity rules should restrict their assignment to archetypes whose role profile clearly demands sustained effects, not include them as default options. This concentrates rendering cost on classes where the marginal type's identity *is* the archetype, rather than spreading it thin across many classes.

### Collapses preserve expressivity at lower cost

Three types collapsed because they were aesthetic or parameter-level distinctions, not new mechanical primitives:

- `delayed_strike` → `ground_targeted_circle` with a delay parameter. Same hitbox, same VFX, timing flag.
- `dash_movement` → `teleport`. Mechanically identical (instant relocation); aesthetic difference is in the VFX layer.
- `ward/shield_zone` → `self_buff` (solo case). Without allies, ward is just a self-buff with a visual radius. Revisit if multi-actor allies are admitted.

### Deferred types: each excluded for stated reason, none excluded by inertia

- `dash_attack` — motion-defines the hit area; LLM has to describe a path; VFX renders trajectory plus hits along it. Express as movement-animation + `melee_strike` at runtime instead.
- `leap_strike` — vertical motion plus landing AOE. Distinct from dash but expressible as `ground_slam` + travel animation.
- `whirlwind` — fails both filters. The ability *is* the motion. Express as movement + `ground_slam` if needed.
- `trap` — multi-stage state machine (place → wait → trigger). Hard for both consumers. Revisit if rogue/ranger demand it concretely.
- `counter` — reactive trigger system. Expressible as buff + conditional reflect at lower fidelity in existing grammar.
- `wall_construct` — environmental object affecting pathfinding. Game-engine work, not VFX work.

Each deferred type can be revisited. None are categorically off the table; they're queued behind concrete archetype demand and consumer capability.

## Implications for the architectural decision (Option C)

Under Option C from `../collaboration-handoff/04-decision-options.md`, the immediate generator palette is **16 types** (CORE 14 + CORE-MARGINAL 2). That's an addition of **8 net-new geometry types** to the engine's current 6, plus parameter extensions to `ground_targeted_circle` and `persistent_zone`.

**Consequential additions for sim work:**

- Three melee variants (`melee_strike`, `melee_arc`, `ground_slam`) all require defining **adjacency mechanics** in the simulator. This is the largest sim addition. Probably 3–5 days, consistent with the prior estimate in `project_engine_state_findings.md`.
- `aura` and `beam_channel` need **sustained-effect support** in the simulator (effect that persists while channeling / while active). Moderate work.
- `ranged_physical` needs **ballistic trajectory** distinct from generic projectile — pierce, multishot, accuracy. Some sim work but conceptually similar to existing projectile.
- `teleport` needs movement primitives in the sim that may not currently exist as ability outputs.
- `totem` needs placed-entity-with-effect-pulse — close to `persistent_zone` but with an entity model attached.

**STAGED types add Phase 2 scope but don't inflate the immediate C estimate.** Multi-actor sim and minion AI are deferred until summoner archetypes are actually being shipped.

The geometry palette work is therefore a meaningful but bounded chunk of Option C's scope — well-defined now, with each type's cost identifiable rather than emerging mid-implementation.

## Open questions

1. **Summoner ratification.** Owner + son to confirm: are AI-controlled, transient, low-cap minions admissible under the "solo gameplay" framing? Default to staged-include unless explicitly rejected.
2. **Adjacency mechanics in the sim.** What exactly does "close range" mean numerically? A specific distance threshold? Engagement-state-based (in melee combat = adjacent)? This is a sim design call that should be made when building melee.
3. **Pierce/multishot for `ranged_physical`.** Are these always-on properties, or per-ability parameters? Likely per-ability (some ranger abilities pierce, some don't).
4. **Generator restriction rules for `aura` and `beam_channel`.** What signals an archetype's role profile "clearly demands" sustained effects? Probably tied to role-orientation axis (sustain / control archetypes) once that fifth axis exists.
5. **Trajectory/projectile mechanics in Three.js.** What level of physical simulation can the Three.js Claude connector reliably produce — instant straight-line, ballistic arc, homing? This affects how `ranged_physical` is differentiated from generic `projectile` in practice.

## Cross-references

- `../collaboration-handoff/03-architectural-proposal.md` — dimensional generation proposal; geometry palette feeds the "range profile" axis.
- `../collaboration-handoff/04-decision-options.md` — A/B/C options; this palette is part of Option C's immediate scope.
- `../collaboration-handoff/06-trial-room-and-class-scoping.md` — design intent including the solo-gameplay constraint that shapes the summoner decision.
- `../collaboration-handoff/08-decomposition-report.md` — surfaced the missing-melee-geometry gap that motivated this discussion.
- `28-engine-arpg-rebalance-design.md` § B11 — palette expansion (2026-05-11) that supersedes parts of the decision below.

---

## Revision 2026-05-11 — Palette expansion (B11)

**Status:** Decision conversation 2026-05-11 (post-demo1-ship). Supersedes parts of the 2026-05-08 decision below. Driving forces: (1) revised AOE coverage targets per genre research (file 28 § B6: controllers 60-75% AOE, hybrid_mage 65-80%) cannot fit cleanly in the 7-active-discrete-AOE palette without forced repeats; (2) the consumability constraints that drove three "DEFER" decisions in 2026-05-08 have been retired by demo1's actual delivery (Phase 6 positional combat, Phase 8.2 weapon animations, Phase 12 Super Pixel Effects pack).

*[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. The AOE-share design discussion above (controllers 60-75%, hybrid_mage 65-80%) is pre-canonical-6 context — hybrid_mage no longer exists in the canonical roster. AOE coverage targets for the canonical-6 roster are governed by the B6/B11 palette decisions for substrate-coherent archetypes. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for context.]*

**Full rationale and implementation plan: `28-engine-arpg-rebalance-design.md` § B11.** This section captures the palette decisions only.

### Updates to the 2026-05-08 decision table

| # | Type | Old status | New status | Reason |
|---|---|---|---|---|
| 23 | `dash_attack` | DEFER | **CORE (NEW per B11)** | Demo1 Phase 6 movement architecture retires the motion-defining consumer block |
| 24 | `leap_strike` | DEFER | **CORE (NEW per B11)** | Same — landing-AOE pairs with `ground_slam` math, movement infrastructure exists |
| 25 | `whirlwind` | DEFER | **CORE (NEW per B11)** | Same — rotating-AOE-while-moving expressible via Phase 12 VFX pack |
| 26 | `trap` | DEFER | DEFER (unchanged) | State-machine complexity still exceeds value at current sim depth |
| 27 | `counter` | DEFER | DEFER (unchanged) | Reactive trigger system — same |
| 28 | `wall_construct` | DEFER | DEFER (unchanged) | Needs terrain/path mechanics not yet in sim; Phase 5+ territory |

### New geometries added (2026-05-11)

| # | Type | Status | Damage radius | Notes |
|---|---|---|---|---|
| 29 | `chain_lightning` | **CORE (NEW per B11)** | AOE | Projectile hits primary then arcs to N nearby targets (PoE Chain support meta). Requires multi-target dispatch (file 28 § C1) for full expression; demo-side splash can approximate. |
| 30 | `ricochet_bounce` | **CORE (NEW per B11)** | AOE | Projectile bounces target-to-target. Shares multi-target dispatch with `chain_lightning`. |
| 31 | `fork` | **CORE (NEW per B11)** | AOE | Projectile splits into N projectiles on impact (PoE Fork support). Mechanically distinct from chain (jumps) and ricochet (bounces). |
| 32 | `vortex_pull` | **CORE (NEW per B11)** | AOE | Pulls enemies to a point + applies AOE. Controllers benefit; combines positional displacement with AOE. |
| 33 | `ring` | **CORE (NEW per B11)** | AOE | Donut-shaped AOE — outer radius minus inner radius. Caster-centered (Shock-Nova archetype) or ground-targeted. Currently expressible only as `circle` with awkward LLM hand-waving; real geometry unlocks the archetype properly. |
| 34 | `multi_projectile` | **CORE (NEW per B11)** | AOE | Radial burst — N projectiles fired simultaneously at distributed angles from caster. Hunter/skirmisher AOE answer (PoE Multishot / Tornado Shot meta). |

### Parameter expansions on existing geometries (cross-cutting; not new types)

Four AOE-shape variants that would otherwise become new geometry types are instead expressed as **per-skill parameters** on existing geometries. This keeps palette type count bounded while expanding expressivity.

| Parameter | On geometry | Values | What it expresses |
|---|---|---|---|
| `collision_mode` | `line` | `stop_on_first` \| `pierce_all` | Piercing line — PoE Lightning Arrow, Diablo Bone Spear |
| `angle_distribution` | `multi_projectile` | `spread` \| `cardinal` \| `diagonal` \| `star` | Cross/plus, X/diagonal, asterisk patterns |
| `sweep_shape` | `melee_arc` | `pie` \| `crescent` \| `wide_arc` | Curved-band sweep variant; `wide_arc` expresses the wide horizontal cleave (see collapse entry for `melee_cleave` in Revision 2026-05-16) |
| `damage_falloff` | all radial geometries (`circle`, `ground_slam`, `ground_targeted_circle`, `ring`, `vortex_pull`, `aura`) | `uniform` \| `linear` \| `exponential` | Proximity damage — clean "positioning matters" lever |

### Revised damage-radius diversity table

| Category | After 2026-05-08 (CORE + MARGINAL) | After 2026-05-11 (B11) |
|----------|------------------------------------|------------------------|
| **single_target** | 4 | 4 (unchanged) |
| **AOE — active discrete** | 7 | **16** (+9: whirlwind, dash_attack, leap_strike, chain_lightning, ricochet_bounce, fork, vortex_pull, ring, multi_projectile) |
| **AOE — passive/persistent** | 3 | 3 (unchanged) |
| **other** | 2 | 2 (unchanged) |
| **total active** | **16** | **25** |

The 16-active-discrete-AOE count gives heavy-AOE archetypes comfortable kit-variety headroom (controllers' 8-10 AOE slots draw from 16 geometries, no forced repeats). The B6 "no same-geometry duplication unless intentional spam+spender pair" rule holds without crunching kit shapes.

**Note (2026-05-16):** The 25-type count above reflects rocket's actual emit pool at B11 (`ability_grammar.py` @ `ec31682`). 4 additional vocabulary types (projectile_homing, aura_directional, melee_cleave, iframe_dash) existed as canonical-09 vocabulary entries but were never implemented in the generator — vocabulary-vs-implementation drift. These 4 were vocabulary-collapsed via the Track 4 decision (Revision 2026-05-16 below); the 25 count was already correct for the emit pool.

### Explicitly skipped (2026-05-11 geometry-options review)

The geometry-options review surveyed FFXIV/PoE/D4 source material and surfaced shapes that fall outside scope. Captured here so they don't get re-discussed:

- **Compound geometries** (cone+circle, etc.) — express as multi-effect skills; generator picks dual effects with different geometries on the same skill rather than a new geometry type
- **`spiral`** — niche in genre, VFX-heavy; benefit-to-cost low
- **`checkerboard`** — FFXIV boss-only in source data; doesn't fit ARPG player palette
- **Pac-Man / open-circle** — almost exclusively enemy attack pattern in genre
- **Tethered AOE** — solo game; no allies to tether to (relevant only when summoner ships, and even then is mostly enemy-mechanic shaped)
- **Stack mark / Spread mark** — MMO/raid mechanics requiring multiple players; not applicable to solo game

### Second-wave park list (post-B11 geometry extension; B12 letter now reserved for movement speed)

Items worth adding eventually but NOT in B11 scope:

| Item | Park reason | Revisit trigger |
|---|---|---|
| `trail` (damage on path) | Distinct from whirlwind (where you WERE, not where you ARE); needs persistent ground tracking | After B11; pair with persistent_zone refactor |
| `persistent_ring_animated` | Temporal-dimension ring (expanding/contracting); telegraphed player abilities | Ship after `ring` (B11) lands; share geometry math |
| `rotating_zone` (clock-hand sweep) | Channeled-zone variant; rotates around fixed anchor, not caster | Express as channeled `persistent_zone` variant for now |
| **Telegraphed enemy AOE + asymmetric indicator scaling** | Genre game-feel: player AOE indicator slightly SMALLER than hitbox (edge catches feel generous); enemy indicator slightly LARGER (dodges feel narrow). Engine produces hitbox as source of truth; demo renderer scales indicator (~0.92× player, ~1.08× enemy). Nests cleanly with `damage_falloff` (concentric rings give a soft edge naturally). | Requires telegraphed enemy AOE to ship first (B10-adjacent VFX polish) |

### Implications for sim work (revised vs 2026-05-08 estimate)

The 2026-05-08 decision sized the geometry-palette work as a meaningful but bounded chunk of Option C's scope. B11 adds **~3-4 weeks** on top of that for the 9 new geometries + parameter expansions + generator updates + LLM naming context + demo VFX integration. See file 28 § B11 for the cost breakdown.

**B11 ships coordinated with B6 + B10 + B7** — they are architecturally co-dependent (file 29 strategic-anchor note). Landing in isolation creates mismatch: B6's AOE shares without B10's density push convergence back toward single-target; B6+B10 without B11 crunches heavy-AOE archetypes; B7's variance check needs the restructured gauntlet (B10) to test against.

---

## Revision 2026-05-11 (B13 extension) — Active defensive mobility geometries

**Status:** Locked 2026-05-11 evening via file 32 Section 12.5 closures. Adds 5 NEW defensive mobility geometries to the palette beyond the B11 expansion. Brings total active palette from **25 (post-B11) → 30 active types**. Active-discrete-AOE count from 16 → 21.

### Driving rationale

B11 added motion-AOE geometries that are OFFENSIVE (whirlwind, dash_attack, leap_strike — damage while moving). The DEFENSIVE/PURE-MOBILITY category was still missing from the generator pool. Without it, the procedural class generator cannot emit "dodge-tank" / "kiting-mage" / "berserker-skirmisher" style archetypes that genre players recognize. Per Section 12.5 (file 32), Reincarnated adopts the **Last Epoch per-class movement model** (NOT D4 universal Evade) — mobility emerges from the generator pool, archetype-appropriate.

### Five new defensive mobility geometries

| # | Geometry | Damage | Mechanics |
|---|---|---|---|
| 35 | `roll` | No | Short evasion dash; ~0.4s i-frames during animation; short CD |
| 36 | `defensive_dash` | No | Directional dash; no i-frames; reposition utility |
| 37 | `strafe_mode` | No | Toggle/sustained; movement becomes sideways while channeling main ability |
| 38 | `blink` | No | Short-range instant teleport; ~0.1-0.2s functional i-frame during animation |
| 39 | `dodge_stance` | Buff | Time-limited buff: +X% statistical evasion for duration; layers on top of `DODGE_CHANCE_CAP = 0.60` |

### Engine sim metadata (added per B13 scope)

- `cast_time` per skill (windup before damage applies — enables telegraphs)
- `damage_resolution_time` per skill (when hitbox resolves)
- `i_frame_window` per evasion skill (start_offset + duration during which player is untargetable)
- Demo respects these fields for telegraphs + i-frame resolution

### Demo rendering additions

- Telegraph rendering during cast_time (enemy AOE shows ground indicator before damage applies)
- **Asymmetric indicator scaling:** player AOE indicator ~0.92× hitbox (generous edges feel); enemy AOE indicator ~1.08× hitbox (dodges feel narrow)
- I-frame respect in hitbox resolution

### Updated damage-radius diversity table (post-B11 + B13)

| Category | After 2026-05-08 (CORE + MARGINAL) | After 2026-05-11 (B11) | After 2026-05-11 (B11+B13) | After 2026-05-16 (collapse) |
|----------|------------------------------------|------------------------|----------------------------|-----------------------------|
| **single_target** | 4 | 4 | 4 | 4 |
| **AOE — active discrete** | 7 | 16 | **16** (+ defensive mobility, but those are mostly "other" radius type) | **16** (-0 from collapse; no AOE types collapsed) |
| **AOE — passive/persistent** | 3 | 3 | 3 | 3 |
| **other** (defensive mobility, self_buff, teleport) | 2 | 2 | **7** (+ roll, defensive_dash, strafe_mode, blink, dodge_stance) | **7** (-0 from collapse; no "other" types collapsed) |
| **vocabulary entries removed** | — | — | — | **-4** (projectile_homing, aura_directional, melee_cleave, iframe_dash → collapsed to parameters) |
| **total active** | **16** | **25** | **30** | **26** |

The 5 new defensive mobility geometries fit the "other" category since they prioritize positional displacement / time-limited buff over damage application.

### Cross-references

- file 28 § B13 — full implementation scope
- file 32 § Section 12.5 — design discussion + reference notes
- file 33 § "Active evasion + mobility abilities (B13)" — locked decisions
- engine `design/decisions/decisions-log.md` — 2026-05-11 B13 entry (landed with Tier 1 batch commit)

---

## Revision 2026-05-16 — Vocabulary collapse (Track 4)

**Status:** Matt-approved 2026-05-16. Decisions-log entry "Geometry type collapses confirmed" committed at `67946d0`. Authored by gandalf Track 4 assessment; rocket dispatch closes the canonical-09 record. Brings total active palette from **30 (post-B13) → 26 active types**. No B11 or B13 scope is lost.

**Background:** gandalf's geometry-VFX-coverage investigation (commissioned 2026-05-16; see `story/geometry-vfx-coverage-assessment.md`) found that 4 of canonical-09's listed geometry types were vocabulary-vs-implementation drift: none of the 4 appeared in rocket's actual `ability_grammar.py` emit pool. The generator had already implemented the correct collapsed form. This is an Engineering Discipline #13a (implementation-vs-intent drift) remediation — the vocabulary drifted ahead of implementation and the collapse corrects the canonical record.

### Four collapsed geometry types

| Removed type | Collapses to | Behavioral flag / parameter |
|---|---|---|
| `projectile_homing` | `projectile_straight` | + `homing: bool` behavioral flag (sim-side trajectory tracking; no VFX distinction from straight projectile) |
| `aura_directional` | `cone` | + `persistent: true` + `damage_falloff: uniform` (parameter expansions already documented in B11 § "Parameter expansions") |
| `melee_cleave` | `melee_arc` | + `sweep_shape: wide_arc` (added to the `sweep_shape` parameter values in B11 § "Parameter expansions") |
| `iframe_dash` | `dash_attack` / `defensive_dash` | + `i_frame_window` metadata (already documented in B13 § "Engine sim metadata"; applies per-skill, not per-geometry) |

All four capabilities remain expressible. The collapse removes redundant vocabulary entries that duplicated parameter-level distinctions as if they were separate geometry primitives.

### Rationale per type

**`projectile_homing`:** No VFX distinction between homing and straight projectile — vendor sidecars show both render identically as projectile_straight VFX. The homing property is a sim behavioral flag (target-tracking trajectory update), not an asset class. D2 Magic Missile and PoE Vaal Spectral Throw both render as projectile_straight VFX with engine-controlled trajectory updates.

**`aura_directional`:** Every vendor's "directional aura" animation classified into `cone` / `nova_wave` / `beam_channel` during legolas's geometry-signature pass. The visual register of a sustained directional emission IS a cone; the distinction from a transient cone is the persistence parameter. Canonical-09 already documented `damage_falloff` and persistence on radial geometries; the aura_directional entry was redundant.

**`melee_cleave`:** Every vendor's "cleave" animation classified as `melee_arc`. The wide-horizontal-sweep variant is a parameter value (`sweep_shape: wide_arc`), not a distinct geometry. PoE Cleave and D4 cleave variants both render via melee_arc VFX with wider sweep angles. Canonical-09 already established the architectural principle that "AOE-shape variety is expressed as PARAMETERS on existing geometries rather than as new geometry types" — this collapse applies that principle.

**`iframe_dash`:** B13 already documented `i_frame_window` as a per-evasion-skill metadata field, not a per-geometry property. Visual register of iframe_dash is identical to dash_attack / defensive_dash (rapid character translation + motion-blur or trail VFX); the i-frame distinction is a sim-state. D4's universal Evade and D2's Whirlwind-dash render identically; i-frame distinction is mechanical.

### B13-deferred geometry types (NOT collapsed — distinct vendor class)

Three defensive-mobility geometry types listed in the B13 extension are **deferred to B13 post-VS2a**, not collapsed. They are character-animation primitives requiring a distinct vendor class (character rigs / animation cycles) rather than the VFX-pack vendor class that covers all other geometry types:

| Type | Status | Reason |
|---|---|---|
| `roll` | B13-deferred (character-animation primitive) | Pure character-animation; no VFX-pack vendor covers roll/dodge cycles; B13 character-animation vendor sweep commissioned |
| `parry_active` | B13-deferred (character-animation primitive) | Shield-flash + parry deflect is character-track, not VFX-track; deferred alongside roll |
| `block_active` | B13-deferred (character-animation primitive) | Same — requires character rig with block animation cycle |

These three are NOT in the B11 emit pool and are NOT ship-blocking for VS2a / B11. They activate when the B13 character-animation vendor sweep lands and B13 generator integration ships (~6-8 weeks post-B11 per `canonical/16-project-roadmap.md` § B13).

### VS2a B11 GREEN list — 11 of 13 elements

Per gandalf Track 4 assessment § 4.2, the following elements are cleared for B11 demo integration after the vocabulary collapses and composite-render strategies are applied:

**GREEN (cleared for VS2a B11):** fire / water / earth / wind / ice / thunder / holy / dark / poison / kinetic / status — 11 elements

**Not GREEN for VS2a:**
- `acid` — deprioritized (Pimen single-point-of-failure for all covered cells; not in canonical-four element pool; remains available as LLM-vocab flavor but not a class-defining element until secondary vendor lands)
- `void` — deferred pending Pixogen license verification; drops from VS2a element pool if license fails

### Cross-references

- `story/geometry-vfx-coverage-assessment.md` — gandalf Track 4 assessment; primary source-of-truth for collapse rationale, per-gap severity table, composite strategies, and GREEN list derivation
- engine `design/decisions/decisions-log.md` — decisions entry "Geometry type collapses confirmed — 4 canonical-09 types collapsed to behavioral flags; B13 animation primitives deferred; VS2a B11 GREEN list locked" (committed `67946d0`, 2026-05-16 Tier 1 batch)
- `agentic_orchestration/dispatches/2026-05-16-gamora-b11-sim-side-geometry-resolution.md` — gamora B11 sim dispatch; in-flight; implements `sweep_shape: wide_arc` on `melee_arc` and `i_frame_window` skill metadata
- Engineering Discipline #13a — implementation-vs-intent drift; this collapse is a #13a remediation
