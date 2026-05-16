# Decision Options — Three Paths Forward

## What needs to be decided

Yesterday's investigation surfaced two related issues:

1. Monster mana economy bug producing 62% convergence failure rate
2. Physical archetypes likely have no resource system, only cooldowns

These can be addressed three ways with meaningfully different scope and outcomes. This document lays out the options honestly so the decision can be made deliberately.

The decision affects approximately the next 1-3 weeks of work and the architectural foundation for everything after.

## Option A — Tactical fixes only

**What it means:**

Treat both issues as bugs requiring patches, not architectural changes. Specifically:

- **Monster mana fix:** Add validation at monster generation time. Reject ability/mana_cost/cooldown combinations that aren't sustainable for ≥60 seconds at the monster's mana pool and regen rate. Regenerate combinations until valid.
- **Resource systems for physical archetypes:** Either leave as cooldown-only (current state) or add a simple stamina cost to physical abilities (similar to mana, just different label).
- **Physical warrior fix:** Merge as currently implemented (percentage armor + resistance gear stub).

**Implementation cost:** ~3-5 days

**What this gets you:**
- Monster mana bug resolved
- Physical warrior fix landed
- Engine produces consistent balance across seeds
- Can move to Priority 02 (gear) and beyond on schedule

**What this doesn't get you:**
- Physical archetypes still feel mechanically thinner than caster archetypes
- Naming pipeline still operates on archetype labels rather than richer dimensional context
- Body-swap mechanic continues to use archetype identity
- Future architectural refactor (if pursued) still needed and will be larger

**Best fit when:**
- Phase 0 timeline is constrained
- Project priority is shipping playable demo over architectural refinement
- Willing to accept "good enough" mechanical identity per class
- Comfortable with the possibility of larger refactor later

**Honest concern:**

This path does the immediate work but leaves the underlying design issues. They'll surface again later — likely when class quality measurement (Cluster 2) reveals that classes feel similar despite different elements, or when gear implementation runs into "what does this stat mean for different classes" questions.

## Option B — Moderate addition (energy types within current architecture)

**What it means:**

Add energy types as a class/monster attribute within the existing archetype framework. Each archetype gets an associated default energy type (warrior → rage, rogue → combo, archer → focus, casters → mana). Generation continues to use archetype as primary input but now also outputs an energy type that affects ability costs and naming.

- **Monster mana fix:** Combination of validation (Option A's tactical fix) AND archetype-appropriate energy assignment (warrior monsters use rage instead of mana, etc.). The bug becomes less common because mana is no longer the universal default.
- **Resource systems for physical archetypes:** Implemented per archetype with appropriate flavor (rage for warriors, combo for rogues, focus for archers).
- **Physical warrior fix:** Merge as currently implemented, then refactor warrior to use rage in subsequent work.

**Implementation cost:** ~1-2 weeks

**What this gets you:**
- Monster mana bug resolved more thoroughly than Option A
- Physical archetypes get distinct mechanical identities
- Naming pipeline can include energy type context
- Body-swap experience differentiates more meaningfully across classes
- Foundation for future dimensional refactor if pursued

**What this doesn't get you:**
- Archetypes remain primary generation inputs
- Combinations are constrained to archetype-blessed dimensions
- Novel combinations don't emerge — only what archetype templates allow
- Cross-season gear smuggling still complicated by archetype-specific gear stats

**Best fit when:**
- Want most of the practical benefits without full architectural refactor
- Project timeline allows 1-2 weeks of focused architecture work
- Willing to accept that future refactor (if needed) is still on the table
- Want concrete improvement to class feel without committing to full rebuild

**Honest concern:**

This is the "have your cake and eat it too" option, which often means the cake is smaller than it could be. You get partial benefits but pay partial costs. If full architectural refactor is the right answer eventually, this path means doing some of that work twice.

## Option C — Architectural refactor (dimensional generation)

**What it means:**

Refactor class and monster generation around dimensional composition as described in `03-architectural-proposal.md`. Energy type, range, armor weight, damage type become primary generation inputs. Archetype labels become emergent descriptors.

- **Monster mana fix:** Resolved architecturally — only mana-using monsters have mana pools, designed coherently with their abilities. Bug becomes structurally impossible.
- **Resource systems for physical archetypes:** Differentiated resources (rage, combo, focus, mana, stamina-as-resource) emerge naturally from dimensional generation.
- **Physical warrior fix:** Possibly subsumed by the architectural work. Or merged first to capture the formula improvement, then class generation rebuilt around dimensional approach.

**Implementation cost:** ~2-3 weeks

**What this gets you:**
- Monster mana bug resolved at root
- Distinct mechanical identities across all archetypes
- Naming and cohesion benefit significantly from richer context
- Body-swap mechanic becomes mechanically coherent (inherit dimensional identity)
- Cross-season gear smuggling becomes more flexible
- Novel archetypes can emerge from generation
- Foundation aligned with engine's actual constraints

**What this doesn't get you:**
- Phase 0 ships later
- Some uncertainty about how dimensional generation behaves in practice (new architecture has unknowns)
- Existing 11 generated classes need recontextualizing or regeneration
- Validation surface is more complex (more dimensions to verify)

**Best fit when:**
- Project timeline allows 2-3 weeks of architectural work
- Distinct class identity is high priority for design vision
- Body-swap mechanic is central to game's feel
- Comfortable with refactoring existing generated content
- Willing to invest in foundation that supports all future work

**Honest concern:**

This is genuinely substantial work. The estimate could be optimistic — architectural refactors often surface unexpected complexity. Three weeks could become four or five depending on what's discovered during implementation.

The flip side: this work, if done right, provides foundation that makes everything after it easier. Cluster 2 quality measurement, Priority 02 gear, Cluster 3 convergence work — all benefit from the architectural foundation.

## Comparison summary

| Dimension | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Time cost | 3-5 days | 1-2 weeks | 2-3 weeks |
| Monster mana bug | Patched | Mostly resolved | Architecturally resolved |
| Class identity | Same as today | Differentiated | Strongly differentiated |
| Naming benefit | None | Moderate | Strong |
| Body-swap experience | Unchanged | Improved | Significantly improved |
| Gear smuggling | Constrained | Constrained | Flexible |
| Future refactor needed | Likely | Possibly | No |
| Phase 0 timeline impact | Minimal | Moderate | Substantial |
| Risk of unexpected complexity | Low | Medium | Medium-high |
| Foundation quality for downstream priorities | Adequate | Better | Best |

## What to do with this comparison

These options have meaningfully different implications. The decision shouldn't be rushed. Specifically:

**Don't decide in the same session that you read this document.** Sleep on it. Talk with your son. Look at the engine code to verify assumptions about current state. Consider what matters most for the project.

**Do consider what you'd regret most.** If you choose Option A and later wish you'd chosen Option C, that's hindsight. If you choose Option C and Phase 0 takes a month longer than planned, that's accepted cost. Which trade-off feels more tolerable?

**Do have the conversation explicitly.** This is the kind of decision that benefits from being articulated to a collaborator. Even if your son's input doesn't change the decision, the act of explaining your reasoning forces clarity.

**Don't let Claude make this decision for you.** Claude can articulate the options, work through trade-offs, identify implications. But the decision is yours and your son's. The engine is your project. The right answer depends on what you want it to be.

## A modest opinion (take or leave)

If pressed for a recommendation, I'd lean Option B as the most defensible default for current circumstances. Reasons:

- Provides meaningful improvement to class feel and naming without full architectural commitment
- Resolves the immediate bug more thoroughly than Option A
- Preserves the option to pursue Option C later if benefits warrant it
- 1-2 weeks is real work but not engine-paralyzing

Option C is the right answer if class identity differentiation is foundational to the game's vision. If the body-swap mechanic is central and players experiencing many classes briefly need each to feel distinct, Option C delivers that more cleanly than Option B can.

Option A is the right answer if Phase 0 timeline is the dominant constraint and shipping working content matters more than architectural refinement. Reasonable choice if the project's priority is "playable demo soon" rather than "well-architected engine eventually."

But this is just one perspective. The decision belongs to you and your son. The honest answer to "which option is right" is "the one that matches your project priorities, which I don't fully know."

## Next step regardless of decision

Whatever decision is made, doc maintenance (per `02-doc-maintenance-required.md`) happens first. Yesterday's drift needs catching up before any new code or architectural work. That's not affected by the decision — it's prerequisite to all three options.

Once docs are current, the decision can be made and implementation can begin. The action plan in `05-action-plan.md` sequences this explicitly.
