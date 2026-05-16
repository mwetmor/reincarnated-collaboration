# CLI Session Prompt — Documentation Maintenance

> **Note (added after use, 2026-05-08):** This prompt was used and the doc maintenance work completed (commits `e3e812d` for engine-repo updates and `973eb7f` for the design subdirectory). At time of writing, the design docs were assumed to live in a separate `design-repo`; they were subsequently moved to `engine-repo/design/` as a subdirectory. References to `design-repo/...` paths in the prompt body should be read as `engine-repo/design/...` if this prompt is reused as a template for future doc maintenance sessions. The prompt body is preserved as written for historical reference.

## How to use this file

This prompt is intended to be pasted into a fresh Claude Code session opened against the working repos (`reincarnated-engine` and the design repo). It establishes context from the recent design discussion and architectural decision, then tasks the session with the documentation maintenance described in `02-doc-maintenance-required.md` — *now informed by the architectural decision that has landed in `10-decision-log-entry-dimensional-generation.md`.*

This is doc-update work only. The session must not start architectural code work, must not modify generator behavior, and must not begin Phase 1 of the dimensional refactor.

## The prompt

Copy everything between the dashed lines into a new Claude Code session opened at `/Users/admin/Games/reincarnated-engine/` (with read access to the design repo as well — confirm path with the user if unclear).

---

I'm starting a focused documentation maintenance session. Before any action, you need to absorb context from a recent design discussion and from the architectural decision that has just landed.

**Required reading, in two phases. Read carefully — quality of orientation determines quality of the work that follows.**

**Phase A — Engine repo and design repo orientation (current working directory + design repo).**

Read whichever of these exist (skip what doesn't, and report what you found vs. what was missing):

1. `CLAUDE.md` (engine repo root, if present) — operational orientation for this repo.
2. `README.md` (engine repo root, if present) — purpose and structure.
3. `docs/evolution-plan.md` — current phasing as documented (will be updated).
4. `test-plans/priority-01-known-issues.md` — current state (will be updated).
5. `test-plans/priority-02-gear-status.md` — current state (will be updated).
6. `notes/sessions/` — any existing session notes.
7. Any other priority test plans that exist.
8. `design-repo/decisions/decisions-log.md` — current decisions log (will receive a new entry).
9. `design-repo/risks/risks.md` — current risks register (will receive new entries).
10. `design-repo/planning/current-phase.md` — current phase document (will be updated).
11. `design-repo/CLAUDE.md` if present — design repo orientation.

This is read-only orientation in Phase A. Do not edit yet.

**Phase B — Recent design discussion and architectural decision (collaboration-handoff folder).**

Then read the collaboration-handoff folder, in this order:

12. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/00-working-agreement.md` — meta-rules. **Note:** those rules apply to *that* folder; in this engine-repo / design-repo session you may write to those repos to perform the doc maintenance — that is the point of this session. You still must not start architectural code work outside the doc updates.
13. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/01-context.md` — what was built and discovered May 7–8, 2026.
14. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/02-doc-maintenance-required.md` — the original doc maintenance scope. **Note:** several items in this list are now informed by the architectural decision (file 10), which post-dates this scope document.
15. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/06-trial-room-and-class-scoping.md` — design intent: spirit-swap, form library, trial room, class scoping (5–6 playable + 3 act-boss).
16. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/08-decomposition-report.md` — empirical findings from decomposing season_000042 archetypes.
17. `/Users/admin/Games/reincarnated-collaboration/canonical/09-geometry-palette-discussion.md` — agreed geometry palette (16 active types + staged summoner types).
18. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/10-decision-log-entry-dimensional-generation.md` — **the architectural decision that has landed.** This is load-bearing context; the doc updates should reflect it.

**STOP after reading. Do not begin any doc edits yet.**

Instead, respond with:

1. **A brief one-paragraph summary** confirming you've absorbed the context — in your own words, not a recap of the docs.
2. **Questions, concerns, or open items.** Specifically: (a) any places where `02-doc-maintenance-required.md` and the architectural decision (file 10) conflict in their guidance, and how you'd reconcile; (b) any docs in your reading that are themselves stale enough to need rework beyond what `02` specifies; (c) anything that seems unclear, contradictory, or worth verifying before editing.
3. **Anything you'd want me to confirm** before editing — e.g., the exact format of existing decisions-log entries (so the new entry matches), preferred location for new test plans, whether new Phase 1–4 priority test plans should be one umbrella file or four.

**Wait for an explicit go-ahead before starting edits.** Do not interpret "thanks" or "I've read your summary" as permission. Wait for an unambiguous "go" or "proceed."

**Task (begin only after explicit go-ahead from me):**

Update or create the documents listed below, in priority order. Match each doc's existing format and style. **Stop after each doc (or each small batch) and let me review before moving to the next.** Doc maintenance is not a single landing; it's a sequence of reviewable updates.

**High priority — must update:**

1. **`engine-repo/docs/evolution-plan.md`** — acknowledge May 7–8 foundation work (telemetry, anchor system, element system) and the architectural decision to adopt dimensional generation refactor (Option C, staged). Reflect that Phase 0's remaining work is now structured as Phases 1–4 of the dimensional refactor.

2. **`engine-repo/test-plans/priority-01-known-issues.md`** — current state of three sub-issues:
   - Issue A (physical warrior): investigation complete; fix on `work/priority-01-physical-warrior` branch; **decision: merge as-is to capture the formula improvement, then Phase 3 of the dimensional refactor reworks warrior generation structurally.**
   - Issue B (fire mage scaling): subsumed by Phase 1 (monster mana economy is structural per Finding 2 of `08-decomposition-report.md`).
   - Issue C (naming repetition): likely resolved by anchor + element variety system; verification pending.

3. **`engine-repo/test-plans/priority-02-gear-status.md`** — revised scope: gear table is essentially placeholder; full implementation is a 1–2 week effort; **now blocked on Phase 2 of the dimensional refactor** (rather than the broader "resource architecture decision" framing in the original doc).

4. **NEW: `engine-repo/test-plans/priority-11-monster-mana-economy.md`** — document the structural mana bug per `08-decomposition-report.md` Finding 2. Mark it as **subsumed by Phase 1 of the dimensional refactor**, not as a separate priority needing its own fix.

5. **`design-repo/decisions/decisions-log.md`** — append two sets of entries:
   - The May 7–8 architectural decisions listed in `02-doc-maintenance-required.md` § High Priority item 5 (NullRecorder pattern, two-database situation, database as source of truth for anchor/element history, single-word rule for element names, auto-accept LLM element proposals, percentage armor formula with K=3000, manifest version bumps).
   - The dimensional generation refactor decision drafted in `collaboration-handoff/10-decision-log-entry-dimensional-generation.md`. Reformat to match the log's existing entry style if needed.

6. **`design-repo/risks/risks.md`** — add entries per `02-doc-maintenance-required.md` § High Priority item 6, with one update: the "Class resource architecture undecided" risk has been resolved by the architectural decision and should be marked as such. Add a new risk: "Dimensional generation refactor scope estimate uncertainty (4–6 weeks budget; could extend if Phase 3 melee/adjacency mechanics are harder than estimated)."

**Medium priority:**

7. **`design-repo/planning/current-phase.md`** — reflect actual Phase 0 progress (telemetry, anchor, element foundations built) and the dimensional refactor staging (Phases 1–4 of the dimensional refactor as the remainder of Phase 0).

8. **`engine-repo/notes/sessions/2026-05-07.md` and `2026-05-08.md`** — create or update session notes for both days. Per the notes protocol, capture: what was built, what was learned, what surprised, what's next. Keep honest — including the late-night discovery flow that extended scope.

**New (created today, post-decision):**

9. **`engine-repo/test-plans/priority-XX-dimensional-refactor.md`** (or `priority-12-` if the next number) — umbrella priority for the dimensional refactor with sub-sections for Phases 1–4. Cross-reference `collaboration-handoff/10-decision-log-entry-dimensional-generation.md` for full context. Each phase sub-section should describe scope, estimate, acceptance criteria, and dependencies. Confirm filename and number with me before creating.

**Constraints — do not violate these:**

- **No code changes** to the engine itself. Doc updates only.
- **No work on Phase 1+** of the dimensional refactor in this session. The decision has been made; implementation is a separate effort.
- **Match each doc's existing format and style.** Don't impose new conventions.
- **Don't invent content.** All updates should be derivable from the source materials in the reading list. Where a fact is unclear, ask rather than guess.
- **Stop and let me review** after each doc (or each small batch). Don't push through the whole list without checkpoints.

**Stopping condition:**

The session's work is complete when all the doc updates above are done, reviewed by me, and committed (or at least staged for commit) in their respective repos. Then report a summary of what changed and any items deferred.

---

## Notes for the project owner

- This session's scope is intentionally large (8–10 docs to touch). Expect 2–4 hours of work depending on review pace. The "stop after each doc" pattern keeps it manageable.
- The decisions-log entry in file 10 is a *draft* — the doc maintenance session may reformat to match the log's existing entry style. The substance should be preserved.
- After doc maintenance, the next CLI session would be Phase 1 implementation of the dimensional refactor. That's a different prompt and a different scope; not part of doc maintenance.
- If during the read-and-questions gate the CLI session surfaces something that meaningfully changes the architectural decision, *pause* and bring it back to this discussion folder before letting the doc maintenance proceed. Doc maintenance shouldn't lock in a decision that needs revisiting.
