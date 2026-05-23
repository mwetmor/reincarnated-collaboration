# 29 — Reincarnated: Engine Architecture and Game Scope

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** Strategic anchor document. Adopted into project 2026-05-11 from a working draft. Captures concepts discussed; partial post-demo1 reconciliation applied. Sections marked TBD remain genuine open decisions.

**Last updated:** 2026-05-12 (adopted 2026-05-11; locks through 2026-05-12: 3-act lock, Earth meta-layer framing, progression-design Section 1-12 closures via file 32 + file 33, Stage restructure A1-A7 via file 16)

## How this doc relates to others

This is the **scope-and-architecture** anchor. Where this doc and downstream specs disagree:
- This doc wins on **scope** ("are we building X?")
- Downstream specs win on **implementation** ("how does X work?")
- Architectural disagreements get resolved deliberately, not by default

Companion docs:
- `16-project-roadmap.md` — tactical near-term operations; operationalizes this doc (Track A staging A1-A7 + interleaved playtests)
- `28-engine-arpg-rebalance-design.md` — post-demo1 engine queue; some Open Design Decisions below resolve via that doc
- `32-progression-design.md` — progression-system design (all 12 sections RESOLVED 2026-05-12; full design spec for Stage A7)
- `33-progression-skeleton.md` — progression skeleton (immutable + decided only; canonical reference for locked progression decisions)
- `../family-review/demo1-progress-tracker.md` — execution history of the demo1 validation phase

## Current state (2026-05-11)

**Demo1 v1.2 shipped.** Live at https://reincarnated-demo.vercel.app — playable on desktop AND mobile. Demo1 served as both Engine 1 validation AND minimum-viable Engine 2 prototype:

- **Engine 1 validation:** 5 generated seasons × 53 classes × ~200 gear items per season, all from runtime LLM-flavored mechanical generation
- **Engine 2 prototype:** linear 7-room gauntlet with packs, doors, breather states; LMB controls + WASD/mobile joystick; per-season visual theming + music; Diablo-style HUD; equipment-driven weapons + ability VFX

What demo1 proved:
- The JSON packet contract between Engine 1 outputs and a consumer works (the demo IS the consumer)
- Generated content is mechanically playable and varied enough to feel distinct per season/class
- Procedural fallback safety nets work at multiple visual layers
- Mobile + desktop deployment from a single Pixi.js codebase is feasible

What demo1 didn't validate (genuine Engine 2 territory):
- Town hub design
- Quest chains tied to act progression
- Procedural dungeon generation with thematic validation
- NPC dialogue + multi-NPC interaction
- Body-swap mechanic interaction with world state
- Cross-season meta-progression

What demo1 surfaced for engine work (tracked in file 28):
- 6+ demo-side overrides compensating for engine generator miscalibrations (combo cost, focus cost, swarm-tier monsters, etc.)
- Element naming quality issues (`milk`, `thrum` flavors land badly with LLM)
- Legendary gear abilities specced but not shipped in Priority 02 (now B5 + B15 in current naming; ships Stage A4)
- Per-skill geometry dimensions missing from JSON exports

## Design philosophy: shaped balance over numeric scaling

**Reincarnated's classes differ by COMPOSITION first, by NUMBERS last.** This is a deliberate design philosophy choice that emerged from demo1 validation and design conversation.

The original engine implementation leaned heavily on `damage_modifier` (a per-class scaling coefficient) to balance classes against the gauntlet at 50% win rate. Convergence ranges were wide (0.05× to 1.9× observed for hunters — a 38× spread). Two classes at modifiers 0.05× and 1.5× would have THE SAME mechanical kit shape and differ only in per-ability damage numbers. That's spreadsheet differentiation — what ARPGs often get critiqued for.

Reincarnated chooses a different path: **balance emerges from variety in DESIGN dimensions, not from numeric scaling.** Damage_modifier is the last-resort fine-tune in a tight range (target 0.85-1.15); the primary balance levers are:

| Dimension | What varies | Tracked as |
|---|---|---|
| **Kit composition** | Element distribution, geometry mix, AOE coverage, role coverage per class | File 28 B6 |
| **Gear variance gate** | Pass/fail check at 50th/75th/95th/99th percentile gear; reject pathological scaling | File 28 B7 |
| **Trait pool** | 5-10 traits per class with varied acquisition floors (1, 12, 25, 38) and per-trait power curves; all reach similar power at character level 50 | File 28 B9a |
| **Skill point distribution** | 120-point endgame budget (2/level + 20 from quests/bosses); variable 10-15 skill kit per archetype; per-skill cap 15 (allows ~8 maxable skills out of kit, forcing specialization); per-skill scaling coefficient engine-determined; optimal distribution is the "meta build"; player can diverge | File 28 B9b |
| **Build reset mechanism** | Strict during play: free reset only under specific triggers (struggling → Spirit Guide guided reset; body swap; end-game; refused body swap → guided reset). Paid endgame reset: post-completion players can pay commodities to reset and replay. | File 28 B9c |
| **damage_modifier** | Fine-tune lever ONLY after design-space dimensions exhausted | (existing) |

**Endgame-baseline framing:** the engine balances against character level 50 (endgame) with all available traits at max rank and full skill point distribution. When the progression system ships (Stage A7 per file 16; B14 multi-band sim handles per-band balance), the engine emits per-band optimal distributions (early/mid/late at L17/L33/L50) — Spirit Guide consumes these for cross-phase build coaching.

**Genre-anchored gauntlet (B10 + B11 — added 2026-05-11; B11 scope expanded 2026-05-11 evening):** the shaped-balance dimensions only converge cleanly IF the gauntlet itself matches ARPG genre conventions. Per Diablo / PoE genre research, this means: ~80-100 mobs/min clear target, ~70% trash composition, 10-12 room acts, boss fights remain 1v1 cinematic encounters. Heavy-AOE archetypes (controllers 60-75% AOE, hybrid mages 65-80%) require the expanded geometry palette (7 → 16 active-discrete-AOE; 16 → 25 total palette) to avoid kit-variety crunch — 3 un-defer (whirlwind / dash_attack / leap_strike) plus 6 new (chain_lightning / ricochet_bounce / vortex_pull / ring / multi_projectile / fork). **Architectural pattern adopted:** further AOE-shape variety is expressed as PARAMETERS on existing geometries (piercing line via `collision_mode`; cardinal/star/diagonal patterns via `multi_projectile.angle_distribution`; crescent via `melee_arc.sweep_shape`; proximity damage falloff on all radial geometries) rather than as new geometry types — keeps palette bounded, naming pipeline unchanged, VFX surface contained. B6 (kit composition) + B10 (gauntlet) + B11 (geometry expansion) + B7 (gear variance gate) must ship as one coordinated sprint — landing in isolation creates architectural mismatch.

**Player-facing outcome:** same class plays meaningfully differently between characters based on (a) which traits unlocked at the player's story state, (b) how the player distributes skill points, (c) gear acquired. This is genre-correct ARPG depth (PoE skill tree, D2 build variety, D3 Paragon) and protects against the "every class is the same except for damage numbers" critique.

**Note:** the philosophy is articulated here; the engine work to fully realize it (B6, B7, B9) is post-demo1-ship engine queue work tracked in file 28. Demo1 v1.2 currently ships against the original numeric-scaling balance approach plus demo-side overrides; the shaped-balance philosophy ships when Track A engine maturation completes.

## Game vision

Reincarnated is a Diablo-style action RPG with two distinctive design pillars:

**Body-swap mechanic.** Players inhabit different generated characters over the course of play. Defeating Trial bosses offers the option to "swap into" the defeated combatant's body, transforming the player's class identity while preserving world progress. **This is the meta-progression mechanism**, not a separate feature — body-swap, gear smuggling, and accumulated knowledge form a coherent meta-layer (see Cross-season meta-progression below).

**Procedurally generated content with mechanical balance.** Each season produces novel classes, abilities, monsters, gear, and trials. Content is LLM-contextualized for flavor and thematic coherence, while simulation validates mechanical balance.

These pillars distinguish Reincarnated from existing ARPGs. Other procedural ARPGs (Megabonk, Rangers In The South) lack runtime LLM generation. Other LLM-driven games (AI Roguelite) lack mechanical simulation balance. Reincarnated occupies the intersection.

## Scope: what Reincarnated IS

**A Diablo-style ARPG.** Familiar structure: hub + sequential acts with dungeons between, final boss ending the game.

**Hub between runs/acts** — see "Open: town hub vs run hub" below; this is a real scope decision.

**Bounded act structure.** **3 acts per game (LOCKED 2026-05-11)** with per-act level bands A1: L1-17, A2: L18-33, A3: L34-50. 1 Trial body-swap opportunity per act. Quest completion in current act unlocks the next. See file 32 § Section 10 / file 33 § "Act structure."

**Procedurally generated dungeons between acts.** Each act has dungeon content unique to its theme. Validation approach: see "Open: dungeon validation method" below.

**LLM-generated content across all major systems:** classes, monsters, trial bosses, gear, quests, NPCs, world history, dungeon theming.

**Mechanical simulation validation.** Combat math, balance loops, and convergence verification ensure generated content is mechanically sound, not just narratively coherent.

**Persistent meta-progression across seasons.** Body-swap + cross-season gear smuggling + accumulated knowledge are the three components. (Possibly meta-currency; TBD.)

## Scope: what Reincarnated is NOT

These exclusions matter as much as the inclusions. They protect against scope creep.

**Not an open world.** No procedural overworld, no exploration outside designated content.

**Not a live-service game.** Each game has a defined end (final boss). Seasons are content rotation between games, not ongoing service.

**Not multiplayer (Phase 0 seasonal play).** Seasonal journey is single-player only. **The eventual Earth meta-layer envisions multiplayer events** (PVP / PVE guild events in the rift) — out of scope for current development but part of the long-term vision. See `../collaboration-handoff/34-earth-meta-layer.md` for the full meta-layer design.

**Not AAA-scope content.** Tier 1-2 progression systems (XP, levels, skills, gear, basic crafting if any) are in scope; deep systems like complex economies, guild systems, social features are out.

**Not generating hubs procedurally.** Whatever the hub form (town or run-hub), its layout is hand-designed. Procedural generation applies to dungeons only.

**Not narrative-driven combat.** Combat resolves through mechanical simulation. LLM contextualizes flavor (names, descriptions, narrative around combat) but doesn't decide combat outcomes through plausibility judgments.

**Not an engine for arbitrary games.** Reincarnated produces Diablo-style ARPGs specifically. Generalization to other genres is a hypothetical future project, not a current goal. (The two-engine architecture is generic-enough to be adapted later if someone wanted to; that's a "could," not a "should.")

## Architecture: two engines

The project splits into two engines with a defined contract between them.

### Engine 1: Content Generation Engine

**Purpose:** Generate fully balanced mechanical content for one season of play.

**Responsibilities:** class generation, ability generation with mechanical balance, monster generation across tiers and archetypes, trial boss generation with phase mechanics, gear generation, skill/paragon tree structure, item systems (gems/runes/consumables — exact scope TBD), seasonal theming, mechanical validation through simulation.

**Inputs:** seed, configuration, optionally prior seasons' content for cross-season variety/continuity.

**Outputs:** JSON packet, telemetry data, validation reports.

**Key principle:** mechanical correctness gates output. Generated content must converge in balance simulations. Narrative coherence is a property of the output but mechanical validation is the gate.

### Engine 2: World Generation Engine

**Purpose:** Consume Engine 1 packets and produce playable game worlds.

**Responsibilities:** hub definition (NPCs, vendor inventories, quest giver state), act structure, quest generation, dungeon generation (procedural maps + LLM theming + validation), NPC personality and dialogue, seasonal world history, cross-season historical context, multi-NPC interaction systems.

**Inputs:** one or more Engine 1 packets, configuration, player save state.

**Outputs:** playable game world definition, quest definitions, dungeon maps, NPC dialogue trees, narrative content.

**Key principle:** world coherence and player experience gate output. Generated worlds must feel internally consistent and present meaningful content.

### The contract between engines

A well-defined JSON packet schema makes the two-engine architecture work. The packet should:
- Be versioned (Engine 2 must handle multiple packet versions gracefully)
- Carry all mechanical content Engine 2 needs to construct the world
- Carry sufficient narrative context (seasonal anchor, elemental theming, flavor text) for Engine 2 to make coherent thematic choices
- Be human-readable enough that the contract is debuggable

The current `/exports/season_NNN/*.json` from Engine 1 is the ad-hoc draft of this packet. Formalization (schema version, completeness audit, Engine 2 backward-compat) happens when Engine 2 prototyping begins in earnest.

## Engine 1 status (post-demo1)

As of demo1 v1.2 ship (2026-05-11), Engine 1 is **functionally complete for demo-scale generation** but has known gaps documented in `28-engine-arpg-rebalance-design.md`:

**Working systems (demo1-validated):**
- Telemetry foundation + LLM call tracking
- Anchor system (130-entry place library with deterministic selection)
- Seasonal element system (147-entry pool with LLM substitution)
- Class generation with 19 archetype tags (mage variants + warrior + skirmisher + brute + monster archetypes)
- Monster generation across 5 tiers (trash/standard/elite/mini-boss/boss + act-boss)
- Combat math with percentage armor formula
- Balance loop with multi-energy-type convergence
- Resource systems: mana, rage, combo, focus, stamina-as-resource (all working with caveats below)
- Gear generation with fit_for_class scoring
- 5 fully-clean seasons in production (seeds 1001-1005)

**Known engine issues (file 28 Category A — bug fixes, ~3-5 hrs):**
- Combo skill cost generator emits costs incompatible with pool size (12/24 combo skills uncastable without demo override)
- Focus skill cost generator same shape (skills emit 7.9-35.3 costs against +10 restore)
- Per-skill geometry dimensions (range, half-angle, area_radius) missing from JSON
- `damage_formula.md` has 10 documented errors against actual code
- Shield magnitude flat at 1000 with no WIS/damage_modifier scaling

**Known balance gaps (file 28 Category B):**
- WIS-on-heal multiplier may be too gentle for stat investment to feel worthwhile
- Per-skill ailment chance scaling (currently flat 0.35 across all skill costs)
- AOE budget rebalancing for ARPG genre feel
- Swarm-tier monster generation (currently demo overrides trash stats client-side)
- Legendary gear abilities — Priority 02 spec'd auras/granted-abilities but never shipped (now B5 + B15 in current naming; ships Stage A4)

**Known content quality items (file 28 Category D):**
- Seasonal element naming quality (`milk`, `thrum` flavors land badly)
- Skill-name collision deduplication (~40% collision rate per season)
- Anchor selector duplicate detection
- One unnamed class observed in season 1002

**Dimensional generation refactor:** Done in spirit — energy type, role orientation, range profile, armor weight, and damage type are all functional axes in current Engine 1 output. The "dimensional generation" pivot from Phase 2 succeeded.

## Engine 2 status (not started)

Engine 2 proper has not been started. Demo1 served as a minimum-viable Engine 2 prototype with a much simpler "level structure" (linear 7-room gauntlet with hand-designed visual themes) than the eventual town+acts+dungeons.

Several pieces need design before Engine 2 implementation begins. **See Open Design Decisions below.**

## Cross-season meta-progression — Earth Self is the meta-layer spine

**Reincarnated Phase 0 (current development) = the SEASONAL JOURNEY portion of a larger eventual game.** The full game vision has an Earth meta-layer that is the persistent home for the player's identity across seasons.

### The Earth Self framing (added 2026-05-11)

- **Earth Self** = the player's persistent identity living on Earth (the meta-layer hub; not in current development)
- **Seasonal journey = descent.** Earth Self body-swaps into a seasonal spirit form for a time-bound journey — this is the current Reincarnated ARPG scope
- **Ascension = return.** Goal of seasonal journey: ascend the most meaningful life back to Earth as a Spirit form
- **Form library = accumulated ascended spirits** on Earth Self — a "truly novel gacha-style accumulation of uniquely LLM-generated ascended spirits"
- **Earth-layer events (eventual feature, not Phase 0):** PVP, PVE guild events, usually in **the rift** (liminal space between Earth and Seasonal realms), defending against monsters "not of either Earth or the Seasonal realm" (third-faction enemies)
- **Earth gameplay loop:** TBD — possibly MOBA, Pokemon Battles, Arena Style, or combinations. Distinct from the seasonal ARPG.

**Full vision: see `../collaboration-handoff/34-earth-meta-layer.md`** (separate design doc).

### Body-swap mechanics within a season

Body-swap, gear smuggling, and accumulated knowledge are not three separate features. **They're one mechanism viewed from three angles:**

- **Body-swap** is the moment of transformation — defeat a Trial boss, choose to inhabit them, retain world state but transform class identity. Per file 32 Section 11 closures (2026-05-11): Trial body-swap and Death body-swap both shrink the in-season class pool by 1; doppelganger-path (Trial refuse) preserves current class
- **Gear smuggling** is what items survive the transformation (in-game) AND what items survive across games (cross-season)
- **Knowledge** is what the player learns: about content shapes, build patterns, anchor archetypes, season conventions

### Design questions for the meta-layer

Phase 0 scope (seasonal journey only):
- ✅ Locked 2026-05-11: in-season body-swap mechanics (Trial path, doppelganger path, death path) — file 32 § 11
- ✅ Locked 2026-05-11: form library accumulation rule (≤1 ascension per season) — file 32 § 11
- TBD: Cross-game gear smuggling mechanics; probably limited capacity, scaling concerns
- TBD: Meta-currency (possibly include; needs scoping)
- TBD: Persistent world history (Engine 2 consuming multiple seasons' packets to weave cross-season references)

Earth meta-layer scope (post-Phase 0):
- TBD: Earth gameplay loop (MOBA / Pokemon-style / Arena / combination)
- TBD: Rift event structure (PVP and PVE; instance vs persistent; matchmaking; etc.)
- TBD: Third-faction enemies for rift events
- TBD: Guild/social systems

These design questions deserve focused docs when Engine 2 work begins (seasonal meta-progression) and post-Phase-0 (Earth meta-layer). Phase 0 doesn't need to resolve them, but the Earth meta-layer framing is now load-bearing for understanding Reincarnated's eventual scope.

## Phase planning (revised — parallel tracks, not waterfall)

The original framing of sequential Phases 0-4 doesn't reflect how the project actually develops. Engine 1, Engine 2 prototyping, and demo work iterate together. **Revised tracks:**

### Track A — Engine 1 maturation (in-flight, ongoing)

Current focus when project resumes. Closes the file 28 queue:
- Bug fixes (A1/A1b/A2/A4) — absorbed into Stage A2 (ARPG sprint) per file 16 restructure 2026-05-12; fixed as side-effects of B6/B11 generator work since Stage A2 regenerates all seasons anyway. Stage A1 retains only A3 doc audit + D1 design session + D3/D4 small items (~5-8 hrs)
- Category B balance tuning (~3-7 hrs) — WIS heal, ailment chance, AOE budget, swarm tier; B5 (legendary abilities) is heavier
- Category D content quality (~5-10 hrs) — element naming design session, skill name dedup, anchor dedup
- Category C (architectural) — multi-target dispatch, knockback consumer, convergence reshape; only if needed

After each engine category ships: demo override cleanup pass + season regeneration. Demo1 baseline improves with each round.

### Track B — Engine 2 prototyping (intermittent, demo-driven)

Demo1 served as Track B prototype phase 1. Future Track B work:
- Town/hub prototype (after "town vs run-hub" decision lands)
- Quest chain prototype (single-act first)
- Dungeon generation prototype with thematic validation (CV vs feature-tagged decision lands here)
- Body-swap interaction prototype
- Multi-NPC dialogue prototype

Each prototype validates one slice of Engine 2 before commitment. May reuse the demo1 codebase or fork a demo2 build.

### Track C — Engine 2 build (future)

After enough Track B prototyping validates the approach: full Engine 2 development. Town, acts, quests, dungeons, NPCs built to shippable quality. Timing depends on Track B outcomes.

### Track D — Integration and ship

Combine Engine 1 + Engine 2 into a playable game. Final polish. Iterate on player experience. Ship Reincarnated v1.0 (the full game, not the demo).

### Beyond ship

Iterate on shipped game. Add features. Consider open-source release of engines if they prove robust and useful.

Timeline estimates are deliberately not included. Father-son development cadence makes timeline prediction unreliable. The tracks are not strictly sequential; some interleave naturally.

## Open design decisions

These decisions are pending and should be made deliberately. Decisions previously listed but resolved by demo1 work have been removed.

### 🔴 High-impact, blocks Engine 2 commitment

**Hub form: Diablo-style town vs Hades-style run-hub.**
- Diablo-style: hand-designed town with 3-5 vendors, quest giver, NPCs, persistent across games. Higher narrative depth; higher build cost.
- Hades-style: minimal between-run hub with essential interactions (gear swap, NPC chats, run start). Lower build cost; matches indie scope better.
- The original draft assumed Diablo-style without examination. Both work; the decision affects scope substantially. **Recommend: prototype both via Track B before committing.**

**Dungeon validation method: CV-based vs feature-tagged.**
- CV-based: LLM target image → procedural dungeon → CV similarity score → ship/regenerate. Technically novel; potentially expensive (LLM + image gen + CV per dungeon); uncertain whether scoring produces useful signal.
- Feature-tagged: LLM describes features ("ruined cathedral with overgrown vines and broken statues"); procedural generator places matching elements; deterministic verification. Cheaper, more reliable; less novel.
- **Recommend: prototype both early (Track B); commit only after data.** This is one of the highest-risk items in the entire proposal.

**Final act count: 3 acts** *(LOCKED 2026-05-11)*
- 3 acts per game; per-act level bands ≈ 17 levels each (A1: 1-17, A2: 18-33, A3: 34-50)
- 1 Trial body-swap per act = 3 Trial body-swap opportunities per season
- Aligns with one-week-season + body-swap-as-meta-progression spine
- Decision locked via file 32 § Section 11 closures
- See `33-progression-skeleton.md` for canonical reference

### 🟡 Medium-impact, designable at any time

**Progression systems scope.** Which of the following are in scope:
- Skill trees per class (✓ partially — engine generates skill ability sets)
- Paragon-style endgame progression (TBD)
- Gem/rune systems (TBD)
- Crafting (TBD)
- Multiple difficulty tiers (TBD)
- Set bonuses (TBD)

**Number of hub vendors and their specializations** (only relevant if Diablo-style hub is chosen).

**Cross-season meta-progression depth.** Specific mechanics for gear smuggling capacity, meta-currency, accumulated-knowledge effects.

### 🟢 Low-impact, resolve when convenient

**Item type breadth:** weapons + armor + accessories are confirmed; gems/runes/consumables are TBD.

**Body-swap visual transition design.** Important for game feel but not blocking architecture.

## Reference points

**Influenced by Diablo 2/3:** hub structure, act progression, ARPG combat feel, gear-driven character power, run-based replayability.

**Influenced by AI Roguelite:** LLM-generated content concept. But Reincarnated mechanically validates content where AI Roguelite uses LLM for combat resolution itself.

**Influenced by roguelikes:** procedural content, meta-progression across runs, body-swap as restart-with-continuity.

**Influenced by Hades:** between-run hub model, "death is progress" framing — relevant to body-swap design.

**Not influenced by Path of Exile:** PoE's depth in passive trees, gem socketing, currency economy is out of scope. Reincarnated is intentionally simpler.

**Not influenced by MMO ARPGs (Lost Ark, Last Epoch online):** no multiplayer, no live service, no constant content updates required.

The right reference rhythm: something like Hades or Returnal (run-based with meta-progression), with Diablo's structural conventions, and novel content generation underneath.

## Risks and unknowns

**LLM content quality variance.** Generated content might be coherent on average but produce occasional jarring outputs. Demo1 surfaced specific cases (`milk` water, `thrum` wind) — cohesion validation helps but isn't perfect.

**LLM cost per game.** Each generated season costs API calls (~$0.87/season for demo1). Each play through could generate more (NPC dialogue, possibly). Cost-per-game might be uncomfortable for free distribution.

**🔴 CV-based dungeon validation may not work.** Highest-risk item in the proposal. Prototype early; have feature-tagged fallback ready.

**Body-swap mechanic might not feel as good as it sounds.** Players might find swapping disorienting rather than empowering. Playtesting will reveal this; design may need adjustment.

**Generated content might feel samey across seasons.** Variety systems are designed to prevent this but only playtesting verifies. Demo1's 5-season playtest gave some signal but limited.

**Two-engine architecture might reveal contract problems.** Demo1 effectively shipped against an ad-hoc packet schema. Engine 2 prototyping will reveal whether the packet is well-shaped or needs structural changes.

**Solo development pace might not sustain through full project.** Multi-year solo projects often fail to ship. Demo1 took ~3 weeks; full Engine 2 with hub + 3 acts + quests + dungeons + NPCs is potentially many months. Track A alone is ~28-40 working weeks (per file 16). Pacing and motivation are real factors.

## What this document is and isn't

**This is:** scope statement, architectural overview, and project anchor. Living documentation that should be updated as decisions land.

**This is not:** a finished spec. Implementation details belong in downstream docs. Decisions marked TBD are real open questions.

**When this doc and downstream specs disagree:** this doc wins on scope; downstream specs win on implementation; architectural disagreements get resolved deliberately.

## How to use this document

When you (or your son, or future contributors) need to make a design or architectural decision, ask:

- Is this within the scope defined here?
- Does it align with the two-engine split?
- Does it match the current Track focus (A engine, B prototyping, C build, D ship)?
- Does it require updating one of the Open Design Decisions?

When the answer to any of these is unclear, that's a signal that this document needs updating before the decision is made.
