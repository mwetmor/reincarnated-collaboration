# Recognition — the one-pilot-policy contract (fit-direction law at the AI layer)

**Author:** gandalf, 2026-07-07 (Pattern-B review of Matt's external AI-architecture conversation).
**Status:** RECOGNITION RECORD — no build fires on this; it becomes a spec doc when the Godot combat layer (post-Q7, D6/D7 territory) is scoped. Filed so it's waiting when that work approaches.

## The recognition

The certification instrument measures kits **under a pilot policy**. KPM / WR / TTK are policy-conditional numbers: the same kit piloted by a smarter or dumber controller certifies differently. Today's policy is the deterministic scripted rotation (player kits: Phase-2 energy_type-branched build-vs-spend selector, `spatial_engine.py:1335`, math note `rotation-selector-phase2-2026-06-20.md`; monsters: `skill_rotation_priority` role-ordered rotation, `spatial_engine.py:1190`) — deterministic by design, which is CORRECT for a fitness instrument.

**The trap:** treating ship-game NPC AI as free to differ from sim AI ("the shipped game can use a richer AI than the sim"). If the shipped pilot differs materially from the certifying pilot, the bars stop predicting shipped balance — **the same defect as room dims diverging between sim and Godot, one layer up.** The one-spatial-contract law has a sibling:

> **One-pilot-policy contract:** the combat pilot policy is authored ONCE (deterministic, seeded) and consumed by BOTH the sim gauntlet and the Godot combat layer. Human-feel differences (reaction delay, aim/score noise, option masking, the Q1 controller-keyed perception edge) are expressed as **registered degradations of the same policy** — never as a second policy. Matt's Q1 perception-asymmetry ruling (symmetric sim + piloted-layer controller-keyed edge) is already this shape; this generalizes it.

**Planned-re-derivation corollary:** when the ship pilot upgrades (e.g., rotation → utility scorer over kit axes), the SIM adopts the same scorer and bars re-derive on it — a registered re-derivation event (same class as the Axis-5 structural-cost trigger), not drift.

## Architecture verdicts from the review (for the future spec)

- **Utility scorer over kit axes = the core pilot** for kit-combatants. Scaling argument is decisive and understated at population-scale emission (hundreds per cell × 18 cells × loot states): per-kit authored trees are impossible; one scorer reading the kit's OWN generation axes (role orientation, resource model, range band) pilots any kit, including post-launch emissions. The rotation selector's ability-metadata plumbing is where the scorer slots.
- **NPC kits must telegraph build identity** (grimoire-claimed souls / mirror-match opponents): scorer WEIGHTS derive deterministically from the kit's generation axes — a summoner summons early, a burst caster cycles to its nova. No runtime LLM in combat decisions (D7 lookup-not-generation, combat edition).
- **Steering/flocking = movement layer under decisions**, mapped to the ratified families (F1 swarm, F2 dispersed packs, F4 lane pressure). **Pack spacing is a BALANCE parameter, not cosmetics:** separation radii set AOE value; sim spawn distributions and Godot flocked distributions must cohere or sim AOE% stops predicting game AOE%. The spatial contract should eventually carry pack-spacing parameters (separation radius, cohesion distance) beside room dims.
- **BT for authored boss phases + utility within phase** — composes with F3 timed add-waves + §23.1 Structure-2. Authored beats at marquee moments = the D7 AI-tell discipline in another costume.
- **GOAP: NOT in the stack — cut entirely, not "reserved for bosses."** F.E.A.R.'s planner shone in cover-topology tactical shooting. The ARPG boss contract is *learn my pattern* (telegraph-and-punish; every Diablo boss; PoE Maven/Sirus are authored scripts). Emergent planning fights legibility, breaks the telegraph-dodge layer-handoff assumption (readable telegraphs), and breaks sim determinism. No tier earns its cost.
- **Tier map (cheapest tool that suffices):** trash = FSM-grade rotation + flocking · packs = same + pack cohesion/shared aggro · elites = utility + pack roles · NPC kits = utility with archetype priors from axes · bosses = BT phases + utility within phase. Readability for everything the player farms; "smart" reserved for mirror-match identity expression.

**Sequencing guard:** none of this is now-work. The scripted rotation is adequate for Step 3 and the current campaign. This note un-parks when the Godot combat layer is scoped.

**Signed:** gandalf, 2026-07-07. *One ruler for the rooms, one ruler for the hands that fight in them.*
