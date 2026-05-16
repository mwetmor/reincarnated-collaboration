# CLI Session Prompt — Decomposition Exercise

## How to use this file

This prompt is intended to be pasted into a fresh Claude Code session opened against the `reincarnated-engine` repo. It establishes context from the recent design discussion and tasks the session with the **decomposition exercise** described in `03-architectural-proposal.md` and `05-action-plan.md` step 3.

The exercise is read-only investigation. The session should produce a markdown report and stop — no code changes, no architectural work, no doc maintenance.

## The prompt

Copy everything between the dashed lines into a new Claude Code session opened at `/Users/admin/Games/reincarnated-engine/`.

---

I'm starting a focused investigation session. Before any action, you need to absorb context from a recent design discussion held in a separate folder, and from the proposal docs that frame the task.

**Required reading, in two phases. Read carefully — quality of orientation determines quality of the work that follows.**

**Phase A — Engine repo orientation (your current working directory).**

The session is opened in `/Users/admin/Games/reincarnated-engine/`. Ground yourself in the engine repo's own context first, before pulling in the recent design discussion. Read whichever of these exist (skip what doesn't, and report what you found vs. what was missing):

1. `CLAUDE.md` (engine repo root, if present) — operational orientation for this repo.
2. `README.md` (engine repo root, if present) — purpose and structure.
3. `docs/evolution-plan.md` — overall plan and phasing.
4. `test-plans/priority-01-known-issues.md` — most recent active priority work. **Note:** per `02-doc-maintenance-required.md`, this doc has not yet been updated to reflect what was discovered May 7–8; read with that in mind.
5. `test-plans/priority-02-gear-status.md` — adjacent priority that intersects with the architectural decision.
6. `notes/sessions/` — most recent session notes if any exist (may not yet — doc maintenance has not run).

Phase A is read-only orientation. Do not edit any of these files.

**Phase B — Recent design discussion (held in a separate workspace folder).**

Then read the collaboration-handoff folder, in this order:

7. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/00-working-agreement.md` — meta-rules. **Note:** those rules apply to *that* folder; in this engine-repo session you may read code freely, but you still must not write or modify code in this session.
8. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/01-context.md` — what was built and discovered May 7–8, 2026.
9. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/03-architectural-proposal.md` — the dimensional generation proposal, especially §"Decomposition exercise".
10. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/04-decision-options.md` — the A/B/C options this exercise informs.
11. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/06-trial-room-and-class-scoping.md` — most recent design context: spirit-swap and form-library framing, class-count scoping (5–6 playable + 3 act-boss), the trial-room mechanic, and several open questions.

**STOP after reading. Do not begin the decomposition exercise yet.**

Instead, respond with:

1. **A brief one-paragraph summary** confirming you've absorbed the context — in your own words, not a recap of the docs. Show that you've internalized the situation.

2. **Questions, concerns, or open items before starting decomposition.** The design docs explicitly contain open questions — see `06-trial-room-and-class-scoping.md` § "Open questions", especially items 4–7 about spirit-swap mechanics (earth-self as class vs. abstract anchor; duration model; form-shift cost; earth-self vulnerability), which are load-bearing for combat / sim scope. React to those if they affect the decomposition. Also surface anything else that seems unclear, contradictory, or potentially mistaken across the engine repo or the handoff docs — push back on framing if something doesn't add up. Don't just accept the docs.

3. **Anything you'd want verified or clarified** before proceeding — about my preferences, project constraints, the engine codebase, or assumptions you want me to confirm.

**Wait for an explicit go-ahead before starting the decomposition.** Do not interpret "thanks" or "I've read your summary" as permission. Wait for an unambiguous "go" or "proceed." If your questions in step 2 alter the shape of the decomposition exercise, we may revise the task before it starts.

**Task (begin only after explicit go-ahead from me):**

Perform the decomposition exercise on the existing season_000042 archetypes. Specifically:

1. **Locate the archetype data.** Likely in the engine repo's generation/ directory, archetype templates, or in the telemetry / research database (the `seasons` and `classes` tables per the schema noted in `01-context.md`). Report what you find and where.

2. **For each existing archetype** (there should be 11 in season_000042), express it as a dimensional combination using these axes:
   - **Energy type:** rage / combo / focus / mana / stamina-as-resource / none-cooldown-only
   - **Range profile:** close / medium / long
   - **Armor weight:** light / medium / heavy
   - **Damage type:** physical / fire / wind / water / earth / hybrid

3. **For each archetype, write down:**
   - Its proposed dimensional decomposition.
   - Whether the decomposition feels **natural** or **forced**.
   - Any aspects of the archetype that don't fit cleanly into these four dimensions (e.g., healing capability, control orientation, mobility).

4. **Aggregate findings:**
   - How many decompose naturally?
   - How many feel forced, and where does the friction come from?
   - Are there archetypal aspects that suggest one or more *additional* dimensions (e.g., "healing capability" as a fifth axis)?
   - Is there evidence for or against the dimensional generation approach overall?

5. **Produce a structured markdown report** at `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/08-decomposition-report.md` (note: that folder, per its working agreement, allows markdown notes — this is one). The report should be reviewable by me without needing to re-read source code.

**Constraints — do not violate these:**

- **Do not write or modify code.** No edits to engine source, no test scripts, no helper utilities. Read-only investigation only.
- **Do not propose architectural changes.** The decomposition exercise produces *evidence* for the architectural decision (A/B/C); the decision itself happens after, in a separate session, with the user.
- **Do not begin doc maintenance** as listed in `02-doc-maintenance-required.md`. That is separately scoped and not part of this session.
- **If something doesn't fit the dimensional axes, capture that as evidence** — don't force a tidy mapping. Forced fits make the exercise epistemically useless.
- **Do not regenerate or modify season_000042 data.** Treat it as legacy reference.

**Stopping condition:**

Stop when the decomposition report is written and reviewable. Report back to me with a one-paragraph summary of findings (most-natural, most-forced, anything surprising). Do not move to implementation, decision documentation, or further architectural work.

---

## Notes for the project owner

- The CLI session above will read from `reincarnated-collaboration/collaboration-handoff/` for context but write its findings *back* to that same folder (`08-decomposition-report.md`). This keeps all decision-supporting artifacts in one place.
- After the report exists, the next discussion session in this folder can read it alongside `03-architectural-proposal.md` and `04-decision-options.md` to make the formal A/B/C decision.
- If the engine repo's directory layout makes the archetype data hard to locate, the CLI session may ask you a question rather than guessing. That's expected and welcome.
