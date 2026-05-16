# Architectural Proposal — Dimensional Combatant Generation

## Status

This is a proposal, not a decision. It emerged from conversation on the night of May 7-8, 2026 about resource systems for physical archetypes. The proposal extends naturally to address the monster mana economy bug architecturally rather than tactically.

This document captures the proposal in enough detail to evaluate seriously. The decision between this proposal and alternatives lives in `04-decision-options.md`.

## Core idea

Currently, the engine generates classes and monsters using archetype labels as primary inputs. A "physical_warrior" archetype gets a template that prescribes its abilities, stats, resource use, and so on. A "controller" monster archetype gets different prescriptions.

The proposal: replace archetype-driven generation with dimensional generation. The primary inputs become:

- **Energy type** (rage, combo, focus, mana, stamina-as-resource, or none-cooldown-only)
- **Range profile** (close, medium, long)
- **Armor weight** (light, medium, heavy)
- **Damage type** (physical, fire, wind, water, earth, or hybrid)
- **Possibly additional dimensions** (control-effect-heavy, healing-capable, mobility-focused, etc.)

Archetype labels become emergent descriptors applied at naming time, not generation inputs. A combatant generated with rage + close + heavy + physical might naturally be described as "warrior" but could equally be named something more specific to that exact combination.

## Why this matters for the reincarnated engine specifically

Several constraints unique to this engine favor dimensional generation:

**Body-swap mechanic.** Players cycle through generated classes via Trial defeats. Brief experiences with each class. Differentiation matters more than mastery. Energy type is one of the most immediate ways to communicate "you're a different combatant now" — a rage class plays fundamentally differently from a mana class within seconds of taking control.

**Generated content paradigm.** The engine generates classes and abilities; designers don't hand-craft them. Predefined archetypes constrain what generation can produce. Letting archetypes emerge from dimensional combinations lets generation actually generate, including novel combinations that don't fit existing labels.

**Cross-season gear smuggling.** Gear from prior seasons carries forward. A piece designed for one season's class might be equipped by a future season's class. If gear interacts with abstract dimensions ("ability cost reduction" works for any energy type) rather than archetype-specific stats, smuggling becomes more flexible.

**Naming and cohesion.** The naming pipeline benefits from concrete dimensional inputs. "Name a rage-using close-combat physical class" gives the LLM more material to work with than "name a warrior with fire flavor." Cohesion validation has sharper criteria.

**Trial bosses and monster identity.** If both classes and monsters emerge from the same dimensional space, the body-swap mechanic becomes mechanically coherent: defeating a focus-using long-range elemental controller lets you become that combatant — with all those properties, not a generic archetype label.

## Connection to monster mana economy bug

The bug discovered yesterday is that monster generation samples cooldowns and mana costs independently from mana pools, producing monsters that exhaust mana within seconds.

Tactical fix: validate sustainability at generation time. Reject ability/cost combinations that aren't sustainable.

Architectural fix via dimensional generation: monsters that emerge as rage-using don't have mana pools at all. Monsters that emerge as mana-using have mana pools designed coherently with their abilities (because mana is their defining mechanic, not a default). The bug exists because mana is being assigned by default to monsters that shouldn't have had it; dimensional generation only assigns mana to combatants whose identity is mana-based.

This is a deeper fix than tuning. It addresses why the bug is possible at all rather than catching its symptoms.

## Proposed dimensional axes (initial sketch)

These dimensions need design discussion before being final. Initial sketch:

**Energy type:**
- **Rage:** builds during combat (taking damage, dealing damage), spent on big abilities. Feels reactive, escalating.
- **Combo points:** built by certain "builder" abilities, spent by "spender" abilities. Feels rhythmic, deliberate.
- **Focus:** maintained over time, depletes during inactivity, replenished by aim/concentration actions. Feels methodical.
- **Mana:** large pool consumed by abilities, regenerates passively. Feels strategic, conservation-based.
- **Stamina-as-resource:** fast depletion, fast recovery between actions. Feels kinetic, paced.
- **None (cooldown-only):** no resource constraint, abilities limited by cooldowns alone. Feels mechanical, rotation-driven. (Probably worth avoiding except for specific cases.)

**Range profile:**
- **Close:** melee-range abilities dominant, may have one or two ranged tools
- **Medium:** mixed range, abilities work at medium distance
- **Long:** ranged abilities dominant, weak in close combat

**Armor weight:**
- **Heavy:** high armor, slow movement, melee tank pattern
- **Medium:** balanced defense and mobility
- **Light:** low armor, high mobility, glass-cannon pattern

**Damage type:**
- Physical, fire, wind, water, earth, or hybrid combinations
- Maps to existing canonical element system

**Possible additional dimensions** (worth discussing but not required initially):
- Control orientation (high/medium/low control effects)
- Healing capability (yes/no, self-only/group)
- Mobility (high/medium/low)
- DOT vs burst damage profile

## What dimensional generation looks like in practice

**Class generation flow:**

1. Generator picks dimensional combination based on season context (anchor, elements, season number)
2. Combination must satisfy validity rules (some combinations are forbidden — e.g., heavy armor + long range is awkward; mana + close-combat + heavy is unusual but possible as battle cleric)
3. Stats template derives from dimensional choices (heavy armor = high HP and armor, low mobility; light armor = lower HP, higher dodge)
4. Abilities generated to match dimensional profile (close-combat class gets melee abilities, rage class gets rage-building and rage-spending abilities)
5. Naming receives full dimensional context, produces evocative class name
6. Cohesion validation checks name fits the dimensional combination

**Monster generation flow:**

Same dimensional approach. Monsters get:

1. Tier (trash, standard, elite, boss) — affects HP, damage, ability count
2. Dimensional combination (some constraints by tier — bosses might have richer combinations)
3. Stats and abilities derived from dimensions and tier
4. Naming and flavor

The same dimensional generator produces both classes and monsters — they're both combatants, differing only in role (player-controlled vs. fought) and tier scaling.

**Body-swap implication:**

When a player defeats a Trial boss, they become that combatant. The dimensional combination of the boss becomes the dimensional combination of the new player class. This is mechanically coherent: you're not getting a generic archetype slot; you're inheriting the specific dimensional identity of who you defeated.

## What dimensional generation does NOT mean

This proposal isn't about removing all structure from generation. Several things stay:

- **Canonical role-slots** (fire/wind/water/earth/physical) remain — they're a separate dimension from energy type
- **Seasonal element substitution** (ember substitutes for fire in a season) remains
- **Anchor system** remains as season-level grounding
- **Naming pipeline** remains, just with richer input
- **Balance loop** remains, validating dimensional combinations against gauntlet
- **Constraints on which combinations are valid** still exist — generator avoids nonsensical combinations

The change is what flows into the generator and how the generator produces output. The pipeline structure stays.

## Estimated implementation cost

Honest estimate: 2-3 weeks of focused effort. Specifically:

**Refactoring class generation** (1 week): replacing archetype-driven generation with dimensional. Existing class templates serve as reference — verify each can be reproduced as a dimensional combination.

**Refactoring monster generation** (3-5 days): same pattern, simpler than classes (fewer ability slots).

**Updating simulator** (3-5 days): handle multiple energy types in resource model, validate combat across dimensional combinations.

**Updating naming pipeline** (1-2 days): receive dimensional context, generate names against richer input.

**Re-verification** (3-5 days): regenerate classes and monsters with new architecture, verify balance, verify naming quality, verify simulator behavior.

This is substantial work but bounded. Most of it is replacing existing logic rather than adding new logic.

## Risks and concerns

**Risk: Some combinations might be unplayable or boring.** Heavy armor + long range is awkward. Mana + close-combat + heavy is unusual. Generator needs constraints to avoid producing nonsensical combinations.

**Mitigation:** Validity rules on dimensional combinations. Some combinations forbidden, others marked as low-probability. Existing archetypes serve as reference for "combinations known to work."

**Risk: Existing 11 generated classes need recontextualizing.** Season_000042's classes were generated under archetype paradigm.

**Mitigation:** Decompose existing archetypes into dimensional descriptions. If they decompose cleanly, dimensional approach maps to existing thinking. If they don't, that's signal about whether the approach fits.

**Risk: More dimensions = more combinations = more validation surface.** Simulator validates more combinations than archetype-driven approach does.

**Mitigation:** Each dimension is concrete (specific energy mechanics, specific damage formulas). The validation problem is more dimensional but each dimension is well-defined.

**Risk: Implementation pulls focus from shipping Phase 0.** This is real architectural work that delays gear, batch generation, and other priorities.

**Mitigation:** This is the question for the decision (see 04-decision-options.md). The work is genuinely bigger than tactical fixes. Whether it's worth doing depends on project goals and timeline.

## Decomposition exercise

A useful exercise to validate the proposal: take each existing archetype and try to express it as a dimensional combination.

- physical_warrior = rage + close + heavy + physical
- earth_caster = mana + medium + medium + earth
- fire_mage = mana + long + light + fire
- water_priest = mana + medium + light + water + healing
- wind_hunter = focus + long + light + physical
- (etc., for all 11 archetypes)

If decompositions feel natural, the approach maps cleanly. If they feel forced, that's signal about fit.

This is a 30-minute exercise that grounds the abstract proposal in concrete current content. Worth doing before deciding.

## What this proposal opens up

If pursued, dimensional generation enables several future possibilities:

- **Novel archetypes emerging** that don't fit any predefined label — dimensional combinations the team didn't think of
- **Cross-class gear** that interacts with abstract dimensions, working across class types
- **Body-swap as identity inheritance** rather than archetype assignment
- **Monster variety that mirrors class variety** — same dimensional space, different role
- **Trial boss design that's mechanically meaningful** — boss's dimensional combination becomes the player's new class
- **Simpler simulator validation** — one dimensional model instead of many archetype-specific ones (eventually)

Some of these are immediate benefits; some are long-term enablers.

## What this proposal does NOT solve

Worth being clear about scope:

- It doesn't solve gear implementation (Priority 02 still requires its own work)
- It doesn't solve LLM cost or quality issues
- It doesn't replace the need for the anchor and element systems (those operate at season level, dimensional generation operates at combatant level)
- It doesn't make the engine "done" — it's foundation work that other priorities still build on top of

## Open questions for evaluation

These need answers before committing to the proposal:

1. How does this interact with seasonal elements? Does a class with "fire" damage still get the seasonal "ember" substitution? Probably yes, but worth confirming.

2. What's the right dimensional complexity? The sketch above has 4 dimensions; could be more, could be fewer. More dimensions = richer variety but harder validation.

3. Are there hard incompatibilities? Mana + heavy armor might be fine (battle cleric pattern); mana + light armor + close-combat physical damage doesn't make obvious sense — what does the generator do with awkward combinations?

4. How do we handle existing season_000042 classes? Do we backfill dimensional descriptions, regenerate them, or leave them as legacy?

5. Does this proposal need to land before Priority 02 (gear), or can gear be implemented against current archetype structure with dimensional thinking applied later?

The decision document (`04-decision-options.md`) addresses the high-level choice. These open questions affect implementation if the decision is to proceed.
