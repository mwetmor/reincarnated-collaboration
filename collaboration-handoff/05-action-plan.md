# Action Plan — Concrete Steps

> **Note (added 2026-05-08, end of day):** This action plan describes the path we initially expected to take. The day's work deviated from it in shape, though the underlying intent — *deliberate decision-making, supported by evidence, before execution* — was preserved. Specifically:
>
> - **Step 1 (doc maintenance) was deferred** until after the architectural decision, on the reasoning that the maintenance pass should reference a clean decision rather than be done in the middle of one. Doc maintenance is now queued via `11-cli-doc-maintenance-prompt.md`.
> - **Step 2 (code investigation) and Step 3 (decomposition exercise)** were performed by a CLI session opened against the engine repo, using `07-cli-decomposition-prompt.md`. The output is `08-decomposition-report.md`.
> - **Steps 4–6 (reflection / son conversation / decision)** happened in this discussion folder, informed by the decomposition findings, the trial-room and class-scoping design captured in `06-trial-room-and-class-scoping.md`, and the geometry palette decisions in `../canonical/09-geometry-palette-discussion.md`. The decision landed and is captured in `10-decision-log-entry-dimensional-generation.md`.
> - **Steps 7+ (implementation)** are now structured as the four-phase dimensional generation rollout described in file 10, with summoner archetypes deferred to a separate Phase 5 effort.
>
> This file is preserved as a historical record of the original plan's shape; **it should not be treated as the current plan of record.** The current plan of record is the decision artifact at file 10 plus the doc-maintenance prompt at file 11.

## How to use this plan

This document breaks the work into discrete steps in the right order. Each step has a clear scope, expected output, and stopping point. Don't skip steps — they build on each other.

The first three steps are mechanical (doc maintenance, code investigation, design exercise). The fourth is reflective (consider options). The fifth is collaborative (talk with son). The sixth is decision. Steps after that depend on the decision.

Total time for steps 1-6 is probably one full day if done carefully. The decision (step 6) shouldn't be rushed. Steps 7+ are days/weeks depending on which option is chosen.

## Step 1 — Doc maintenance pass

**Goal:** Bring documentation in sync with what was built and discovered May 7-8.

**Approach:**

Open Claude Code (or your preferred Claude session) pointed at this folder. Give Claude this orientation:

> Today's work: documentation maintenance only. Read these files in order:
> 1. `collaboration-handoff/README.md`
> 2. `collaboration-handoff/01-context.md`
> 3. `collaboration-handoff/02-doc-maintenance-required.md`
>
> Then update each doc listed in 02-doc-maintenance-required.md in priority order. Don't invent content — capture what's already known from the context document. Match existing format and style. Stop and let me review before committing.
>
> Don't start architectural work in this session. Don't begin investigation of current code structure. Don't draft new priority test plans for things not in the maintenance list. Doc maintenance is the entire scope.

**Specific docs to update (per 02-doc-maintenance-required.md):**

1. `engine-repo/docs/evolution-plan.md` — acknowledge telemetry/anchor/element work
2. `engine-repo/test-plans/priority-01-known-issues.md` — current state of three sub-issues
3. `engine-repo/test-plans/priority-02-gear-status.md` — revise scope based on actual gear state
4. `engine-repo/test-plans/priority-11-monster-mana-economy.md` — new file documenting the bug
5. `design-repo/decisions/decisions-log.md` — add yesterday's architectural decisions
6. `design-repo/risks/risks.md` — add monster mana economy and balance variety findings
7. `design-repo/planning/current-phase.md` — actual Phase 0 progress
8. `engine-repo/notes/sessions/2026-05-07.md` and `2026-05-08.md` — session notes

**Expected output:**

8-10 updated or new markdown files across the engine and design repos. Updates should be factual reports of what was built and discovered, not interpretations or recommendations.

**Stopping point:**

When all docs are updated and reviewed. Don't move to step 2 until step 1 is complete and committed. Doc maintenance and code investigation are different cognitive modes; don't blend them.

**Estimated time:** 2-3 hours

**Pitfall to avoid:**

Letting doc maintenance expand into "while I'm in here, let me also..." Stay strictly in the maintenance scope. Architectural improvements come in later steps.

## Step 2 — Code investigation

**Goal:** Verify assumptions about the current engine state. The architectural proposal is built on assumptions that should be checked against actual code.

**Approach:**

Open Claude session and ask it to investigate (no code changes, just reading and reporting):

> I need to investigate the current engine state to verify some assumptions before making architectural decisions. Please answer these questions by reading the engine code:
>
> 1. How do classes and monsters currently get generated? Are they generated by parallel systems or shared logic?
>    - Check: `src/reincarnated/generation/` directory structure
>    - Check: any shared abstractions between class and monster generation
>
> 2. What resource systems currently exist? Is the assumption correct that physical archetypes have only cooldowns (no mana, stamina, or other resource)?
>    - Check: ability cost handling in damage_resolver and combatant
>    - Check: stat templates for physical_warrior vs casters
>    - Check: whether stamina is actually used in combat (or only for sprinting/dodging as designed)
>
> 3. How are archetypes currently represented in code? Are they templates, enums, or something else?
>    - Check: archetype-related files in generation/
>    - Check: how naming pipeline receives archetype information
>
> 4. What does the gear table actually contain? Is the database state (8 NULL rows) consistent with code expectations or vestigial?
>    - Check: gear_catalog.py and any gear generation code
>    - Check: whether gear is referenced anywhere by class generation
>
> Report findings in a structured format. Don't propose changes. This is investigation only.

**Expected output:**

A report (probably 1-2 pages) confirming or correcting the assumptions in `03-architectural-proposal.md`. May reveal:

- Class and monster generation share more code than expected (good for architectural changes)
- Or they're fully parallel (means more refactoring work)
- Resource system assumptions might be wrong (maybe stamina IS used; maybe physical abilities DO have mana)
- Archetype representation might be more flexible than expected (easier to refactor) or hardcoded (harder)

**Stopping point:**

When investigation report is complete. Don't propose changes based on findings — those come later. Just understand current state.

**Estimated time:** 1-2 hours

**Pitfall to avoid:**

Letting Claude propose changes during investigation. The goal is understanding, not action.

## Step 3 — Decomposition exercise

**Goal:** Validate the dimensional generation proposal by attempting to express existing archetypes as dimensional combinations.

**Approach:**

This can be done with Claude or solo. Take each existing archetype from season_000042's classes and try to express it as a dimensional combination using the axes proposed in `03-architectural-proposal.md`:

- Energy type (rage/combo/focus/mana/stamina/none)
- Range profile (close/medium/long)
- Armor weight (light/medium/heavy)
- Damage type (physical/fire/wind/water/earth)

For each existing archetype, write down:

- Its proposed dimensional decomposition
- Whether the decomposition feels natural or forced
- Any aspects of the archetype that don't fit cleanly

Example (sketched):

```
physical_warrior:
  rage + close + heavy + physical
  Feels: natural
  Issues: none

earth_caster:
  mana + medium + medium + earth
  Feels: natural
  Issues: none

water_priest:
  mana + medium + light + water
  Feels: forced — also has healing capability not captured by dimensions above
  Issues: healing might need to be a separate dimension

fire_mage:
  mana + long + light + fire
  Feels: natural
  Issues: none
```

Continue through all archetypes from season_000042.

**Expected output:**

A document (maybe 1 page) with each archetype decomposed and notes on fit. This document is direct evidence for or against the dimensional proposal.

**Stopping point:**

When all 11 archetypes are decomposed. Look at the pattern: do most fit naturally (proposal is sound), or do many feel forced (proposal needs rethinking)?

**Estimated time:** 30-45 minutes

**Pitfall to avoid:**

Forcing archetypes to fit the proposed dimensions. If something feels forced, capture that as evidence — don't pretend it's clean.

## Step 4 — Reflection time

**Goal:** Consider the three options with current information.

**Approach:**

Walk away from the computer. Take a break. Maybe an hour or two. Think about:

- What you actually learned in steps 1-3
- Which option (A, B, or C from `04-decision-options.md`) feels right given what you now know
- What concerns you most about each option
- What you'd want to ask your son about

This isn't busywork. It's the cognitive transition from "gathering information" to "forming opinion." Forming opinion while still gathering information produces rushed decisions.

**Expected output:**

You return with a clearer sense of which option you're leaning toward and why. Could be different from what you expected at the start of the day. That's fine — that's the point of taking the time.

**Stopping point:**

When you have a working hypothesis about which option is right, even if it's tentative.

**Estimated time:** 1-2 hours of break time, processing in the background

**Pitfall to avoid:**

Skipping this step because it doesn't produce visible output. Reflection is real work.

## Step 5 — Conversation with son

**Goal:** Discuss the decision with your collaborator before committing.

**Approach:**

Walk your son through:

- What was built yesterday (briefly — he may already know)
- What was discovered (monster mana bug, the dimensional thinking)
- The three options with their trade-offs
- Your tentative leaning and why

Listen for:

- His reaction to the dimensional generation idea
- His intuition about class identity vs shipping speed trade-off
- Any constraints you might be missing
- His sense of how much time the project should spend on architecture

This conversation might confirm your leaning, change it, or surface a fourth option you haven't considered. All are valuable outcomes.

**Expected output:**

Shared understanding of the decision and an agreed direction. Could be the same direction you walked in with, could be different.

**Stopping point:**

When you and your son have made a decision together (or agreed to defer the decision to a specific time after more thinking).

**Estimated time:** 30-60 minutes of conversation

**Pitfall to avoid:**

Making the decision without your son. He's a collaborator on the project, and architectural decisions affect his work too. Even if he defers to you, the act of explaining the choice is valuable.

## Step 6 — Decision

**Goal:** Commit to one of the three options.

**Approach:**

Document the decision explicitly. Add to `design-repo/decisions/decisions-log.md`:

- **What was decided** (Option A, B, or C — and any specific scope adjustments)
- **Why** (the reasoning, including what was considered and rejected)
- **What it implies for upcoming priorities** (timeline, sequencing)
- **What conditions might cause us to revisit** (e.g., "if implementation reveals X, reconsider")
- **Date of decision** (May 8, 2026)

This isn't bureaucracy. It's the artifact that future-you and future-Claude reference when making downstream decisions. "Why are we doing this dimensional refactor?" should have a clear answer in the decisions log.

**Expected output:**

A decisions log entry capturing the choice. Approximately 200-400 words.

**Stopping point:**

When the entry is written and committed.

**Estimated time:** 30 minutes

**Pitfall to avoid:**

Vague decisions ("let's go with option B-ish, with some elements of C"). Be specific. If the decision is genuinely a hybrid, name what's included from each option.

## Steps 7+ — Implementation (depends on decision)

The remaining steps depend on which option was chosen. This document doesn't sequence them in detail because they're substantial enough to warrant their own planning sessions. But the high-level structure:

### If Option A (tactical fixes):

7. Implement monster mana sustainability validation
8. Decide on physical archetype resource situation (cooldown-only or simple addition)
9. Verify warrior fix across multiple seeds with functional monsters
10. Merge work/priority-01-physical-warrior to main
11. Move to Priority 02 (gear)

Estimated 3-5 days total.

### If Option B (energy types within archetypes):

7. Design energy type assignment per archetype
8. Implement energy type as class/monster attribute
9. Refactor ability cost handling per energy type
10. Update naming pipeline to receive energy type context
11. Implement monster mana fix combined with energy types
12. Verify across multiple seeds and classes
13. Merge work to main
14. Move to Priority 02 (gear)

Estimated 1-2 weeks total.

### If Option C (dimensional refactor):

7. Design dimensional axes in detail (which dimensions, what values)
8. Refactor class generation around dimensional inputs
9. Refactor monster generation in parallel
10. Update simulator for multiple energy types
11. Update naming pipeline for dimensional context
12. Verify dimensional combinations produce sensible combatants
13. Verify balance with new architecture
14. Address season_000042 backfill question
15. Merge to main
16. Move to Priority 02 (gear) with dimensional design from start

Estimated 2-3 weeks total.

Each implementation path needs its own session-level planning when reached. Don't try to plan all of it now.

## Honest pacing assessment

This entire plan (steps 1-6, ending with a deliberate decision) is one full day of work if pursued continuously. Probably more like two days at sustainable pace.

Steps 7+ add days or weeks depending on the decision.

This is normal for architectural work. The decision deserves the time. Rushing it produces patches; taking time produces foundation.

If the steps feel like a lot, remember: they're sequential and each is bounded. Doing the first step well makes the second step easier. The plan is structured so you're never trying to do everything at once.

## Where to keep this folder

Per the original request, this folder lives somewhere accessible to Claude Code on this Mac. Suggested locations:

- `/Users/admin/Games/reincarnated-engine/collaboration-handoff/` (in the engine repo, not committed — gitignored)
- `/Users/admin/reincarnated-collaboration/` (separate folder outside repo)
- Wherever else you find convenient

The location doesn't matter mechanically — what matters is that Claude Code can read these files when pointed at the folder.

You may want to add a note in the engine repo's README pointing at the collaboration folder so future-you doesn't forget where it is.

## Final note

This plan is structured to support deliberate decision-making, not to maximize speed. The goal isn't to finish the dimensional generation refactor (or whatever option you choose) by end of week. The goal is to make a decision you'll still endorse a month from now.

If the plan feels slow, that's intentional. Architectural decisions made under time pressure often get revisited within months. Decisions made deliberately tend to last.

Take the time it deserves.
