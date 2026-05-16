# Documentation Maintenance Required

## Why this comes first

Before any new architectural work happens, documentation drift from yesterday's sessions must be addressed. This is not optional housekeeping — it's how the project's knowledge maintenance protocol works. Without these updates, future sessions (and your son) will be operating on stale information.

The drift is substantial enough that catching up takes a focused session before any new code or design work. Treat this as the first work of the day.

## What to update, in priority order

### High priority — must update before any new work

**1. `engine-repo/docs/evolution-plan.md`**

Currently doesn't acknowledge that telemetry, anchor, and element systems were built. These are foundational additions that came before Cluster 1 priority work. The plan should reflect:

- Telemetry foundation as infrastructure layer
- Anchor system as content variety system
- Element system as content variety system
- Sequence shift: foundation work happened in parallel with Priority 01 investigation

Suggested update: add a section before Cluster 1 describing "Foundation work completed May 7-8, 2026" with brief description of each system and its role.

**2. `engine-repo/test-plans/priority-01-known-issues.md`**

The original priority anticipated three issues: physical warrior, fire mage scaling, naming repetition. Update to reflect current state of each:

- **Issue A (physical warrior):** Investigation complete. Two root causes identified (flat armor formula, missing elemental resistance). Fix proposed: percentage armor formula with K=3000, plus resistance gear stub. Status: committed to work branch but unmerged pending decision on whether to address as-is or fold into broader Priority 11/12 work.

- **Issue B (fire mage scaling):** Investigation revealed this is likely the same monster mana economy bug, not a separate issue. Fire mage failures at the simulator's M=0.20 floor occur because mana-starved monsters provide no real combat pressure. Status: subsumed by Priority 11 (monster mana economy).

- **Issue C (naming repetition):** Hypothesis is that this auto-resolves with anchor/element variety system removing static fire-themed seasons. Empirical verification needed via diversity query after running 2-3 LLM seasons. Status: likely resolved, verification pending.

**3. `engine-repo/test-plans/priority-02-gear-status.md`**

Original test plan had three paths (implemented/partial/not implemented). Database investigation showed actual state is closer to "not implemented" — gear table has 8 rows, all with names matching slot types ("Sword", "Helmet"), all stats and affixes NULL. Update scope to reflect:

- Gear is essentially placeholder slot registration, not actual gear instance generation
- Implementation work scope is larger than original test plan anticipated
- Priority is blocked on resource architecture decision (Priority 12 proposal)
- Realistic scope: 1-2 weeks of focused work for full gear implementation

**4. New file: `engine-repo/test-plans/priority-11-monster-mana-economy.md`**

Create new priority test plan documenting the monster mana economy bug. Use existing priority test plans as format reference. Should include:

- **Background:** Discovery context (during Priority 01 investigation)
- **Mechanism:** Independent cooldown/mana_cost sampling without sustainability check
- **Symptom:** 62% convergence failure rate across 8 test seeds
- **Affected priorities:** All class balance verification, Priority 04 (class quality), Priority 09 (trial accessibility), Priority 10 (cross-season variety)
- **Approach options:** Tactical fix (validate sustainability at generation time) vs architectural fix (dimensional generation that doesn't assign mana to non-mana combatants)
- **Acceptance criteria:** Monster rotations sustainable for ≥60 seconds at generated mana pool/regen, OR architectural change that removes the issue entirely

**5. `design-repo/decisions/decisions-log.md`**

Add entries for yesterday's architectural decisions:

- **NullRecorder pattern adopted** (May 7) — telemetry recorder uses Protocol-based interface with NullRecorder for telemetry-disabled paths. Eliminates None checks throughout orchestrator code.

- **Two-database situation** (May 7) — research.db (existing) and telemetry.db (new) coexist. Future consolidation deferred. Document the fork explicitly so it's not confusing later.

- **Database as source of truth for anchor/element history** (May 7) — no parallel history.json files. Selectors query telemetry database directly.

- **Single-word rule for element names** (May 7) — compounds reserved for ability naming. 13 compounds removed from element pool during cleanup.

- **Auto-accept LLM element proposals for Phase 0** (May 7) — manual review deferred. Tracked in element_proposals table.

- **Percentage armor formula with K=3000** (May 8) — replaces flat armor subtraction. K is tuning constant in formula `reduction = armor / (armor + K)`. Physical archetypes get stub resistance (9% per element) until proper gear lands in Priority 02.

- **Manifest version bumps** (May 7-8) — 1.0 → 1.1 (anchor) → 1.2 (anchor + elements). Consumers reading version can branch loader logic.

**6. `design-repo/risks/risks.md`**

Add entries for:

- **Monster mana economy bug** affecting balance verification across all classes until addressed
- **Balance-vs-variety tension** revealed by anchor/element rotation — gauntlets vary across seasons, balance modifiers calibrated against one season's gauntlet may not transfer to others
- **Class resource architecture undecided** — physical archetypes likely have no resource constraint, affecting class feel and balancing
- **Documentation drift risk** — sessions producing fast architectural changes outpace documentation discipline; need explicit catch-up sessions

### Medium priority — update during the doc maintenance session

**7. `design-repo/planning/current-phase.md`**

Update to reflect actual Phase 0 progress:

- Telemetry foundation built (originally not in plan)
- Variety systems built (anchor, element)
- Combat math improvements identified and partially implemented
- Open priorities revised based on yesterday's discoveries

**8. `engine-repo/notes/sessions/2026-05-07.md` and `2026-05-08.md`**

Create or update session notes for both days. Include:

- What was built
- What was learned
- What surprised you (the most valuable retrospective question)
- What's next

Per the notes protocol, these capture context that doesn't fit elsewhere. Keep them honest — including the late-night discoveries that extended scope beyond plan.

### Lower priority — capture but don't block on

**9. `design-repo/CLAUDE.md`**

May need update if working agreement evolved. Probably fine as-is.

**10. Test plan for Priority 12 (resource architecture)**

If decision is made to pursue resource architecture work, this needs its own test plan. Don't create yet — wait for the decision (see 04-decision-options.md).

## How to do this maintenance with Claude

The doc maintenance session should be focused and bounded:

> Today's session: documentation maintenance only. No code changes, no architectural work. The goal is to bring docs in sync with what was built and discovered May 7-8, 2026.
>
> Required reading (in this order):
> 1. `collaboration-handoff/01-context.md` (the context document)
> 2. Existing files at `engine-repo/docs/evolution-plan.md`, the priority test plans, decisions log, risks register, current phase
> 3. The 02-doc-maintenance-required.md file (which lists what to update)
>
> Tasks for this session:
> 1. Update each doc listed in priority order
> 2. Don't invent content — capture what's already known from the context document
> 3. Match existing format and style of each doc
> 4. Stop and let me review before committing
>
> Don't start architectural work in this session. Doc maintenance is its own bounded scope.

This pattern keeps the session focused. After this session ends, decisions about the architectural options (see 04-decision-options.md) can happen with clean documentation underneath.

## Estimated time

The doc maintenance session is probably 2-3 hours of work for someone familiar with the project. Less if Claude does most of the drafting and you review. More if discoveries during the maintenance session reveal additional drift.

This is more than a quick check-in. It's substantive work because the drift is substantial. Don't try to skip past it.

## After doc maintenance

With docs current, you can then:

1. Read the architectural proposal (03-architectural-proposal.md) with fresh context
2. Consider the three options (04-decision-options.md) deliberately
3. Talk through with your son if appropriate
4. Make a decision and plan implementation

The action plan in 05-action-plan.md sequences these steps explicitly.
