# CLI Session Prompt — Phase 1: Energy Type Axis

## How to use this file

This prompt is intended to be pasted into a fresh Claude Code session opened against `/Users/admin/Games/reincarnated-engine/`. It orients the session to **Phase 1 of the dimensional generation refactor** (per the architectural decision committed to `engine-repo/design/decisions/decisions-log.md`, drafted at `collaboration-handoff/10-decision-log-entry-dimensional-generation.md`).

Phase 1's budget is ~1 week of focused implementation work. That doesn't fit a single CLI session. The prompt is structured to:

1. Orient the session via a substantial reading list.
2. Gate the session to produce a detailed **implementation plan** (not code) as its first task.
3. After plan approval, execute the plan in **checkpointed steps**, each ≤ 1 day of work and independently reviewable.

This is a different shape from the prompts in `07-cli-decomposition-prompt.md` (read-only investigation) and `11-cli-doc-maintenance-prompt.md` (doc curation). Phase 1 modifies engine code, runs tests, and ships behavioral change. The "stop and ask before action" gate is therefore even more important — the cost of acting on a wrong assumption in implementation is higher than in research.

## The prompt

Copy everything between the dashed lines into a new Claude Code session opened at `/Users/admin/Games/reincarnated-engine/`.

---

I'm starting Phase 1 of the dimensional generation refactor for the reincarnated engine: **adding energy types as a generation input dimension and removing the structural assumption that all classes use mana.** This phase fixes the monster mana economy bug at its root.

**Phase 1 scope (and what it explicitly is NOT):**

This phase:
- Adds `energy_type` as a primary generation input dimension (rage / combo / focus / mana / stamina-as-resource).
- Removes `mana_cost_pct` from classes whose energy type isn't mana; introduces equivalents (rage cost, focus cost, combo build/spend, etc.).
- Updates the combat simulator to handle multiple energy types.
- Resolves the structural monster mana economy bug per `08-decomposition-report.md` Finding 2.

This phase does NOT:
- Add the role orientation axis (that's Phase 2).
- Expand the geometry palette or build melee mechanics (that's Phase 3).
- Add the dimensional diversity constraint (that's Phase 4).
- Implement summoner archetypes or multi-actor sim (that's Phase 5, deferred).
- Touch the spirit-swap mechanics layer — duration model, earth-self handling, form-shift cost, etc. (open questions in `collaboration-handoff/06-trial-room-and-class-scoping.md` § "Open questions" 4–7; deferred).
- Regenerate `season_000042` (legacy reference per file 06; new structure activates with next generated season).

**Validity matrix for Phase 1:**

- Elemental classes (fire / water / earth / wind `dominant_element`) → `energy_type = mana`.
- Physical classes (`dominant_element = physical`) → `energy_type` sampled from `[rage, combo, focus, stamina-as-resource]`.

Cross-combinations (e.g., a fire-themed rage warrior, a wind-themed focus archer, an earth-themed defender) are **deferred to Phase 2, not architecturally foreclosed**. The Phase 1 simplification keeps the validity matrix bounded so implementation focus stays on the energy-type mechanics themselves; it does not ban element × non-mana combinations as a design choice. The plan you produce should explicitly frame this matrix as a *Phase 1 simplification, not a permanent constraint*, so future readers don't interpret it as a foreclosure.

Two complementary pathways exist for elemental flavor on physical classes, to be sorted out during Phase 2 planning (out of scope for Phase 1):

- **Native dimensional pathway** — generator produces classes with elemental `dominant_element` + non-mana `energy_type` directly. Captures cases where the elemental theme is mechanically baked into the class identity (e.g., a fire-fury warrior whose rage abilities deal fire damage at the ability level).
- **Gear pathway** — the gear system (Priority 02, unblocked after Phase 2) layers elemental damage / flavor on top of any base class. Captures the standard ARPG convention (Diablo 2 Amazon's cold/lightning bow skills, Path of Exile elemental conversion via gear).

These are not mutually exclusive. Phase 2 will decide which archetypes use which pathway. Phase 1's simpler matrix doesn't lock in either choice.

**Required reading, in two phases. Read carefully — Phase 1 sets patterns Phases 2–4 will follow, so quality of orientation matters.**

**Phase A — Engine repo and design subdirectory orientation (your current working directory).**

Read whichever exist (skip and report missing):

1. `CLAUDE.md` (engine repo root) — operational orientation.
2. `README.md` (engine repo root) — purpose and structure.
3. `design/CLAUDE.md` (if present) — design-side orientation.
4. `design/decisions/decisions-log.md` — focus on the **2026-05-08 dimensional refactor entry** (the canonical version of file 10).
5. `design/risks/risks.md` — especially monster mana economy (Materialized) and dimensional refactor scope uncertainty.
6. `design/planning/current-phase.md` — current project phasing.
7. `docs/evolution-plan.md` — overall plan.
8. `docs/notes-protocols.md` — note format you'll use for session notes.
9. `test-plans/priority-12-dimensional-refactor.md` — **Phase 1 sub-section is the focus**; this is your scope-of-work document.
10. `test-plans/priority-01-known-issues.md` — warrior fix context (the percentage armor formula and resistance stub from PR #2 carry forward into Phase 3; do not undo them).
11. `test-plans/priority-11-monster-mana-economy.md` — the bug this phase resolves at root; preserved as supporting context.
12. `notes/sessions/2026-05-07.md` and `notes/sessions/2026-05-08.md` — recent session context.

Then read the engine code you'll be modifying:

13. `src/reincarnated/generation/class_generator.py` — primary generation entry point.
14. `src/reincarnated/generation/archetype_classifier.py` — emergent archetype classification logic.
15. `src/reincarnated/generation/role_constraints.py` — ability grammar.
16. `src/reincarnated/generation/stat_allocator.py` — stat templates per archetype.
17. The combat simulator's resource handling — find and read whatever file(s) currently model mana costs and pool / regen.
18. The telemetry recorder's `_insert_classes` method — schema relevant to new fields.

You may need to read more code to understand the simulator's resource model. Cast as wide as needed during orientation; report what you find.

**Phase B — Recent design discussion (in `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/`):**

19. `00-working-agreement.md` — meta-rules. **Note:** those rules apply to the discussion folder; in this engine-repo session you may write code, run tests, and commit (that is the point of this session). The discipline that does carry over: scope discipline. Don't expand into Phases 2–4.
20. `06-trial-room-and-class-scoping.md` — design intent: spirit-swap, form library, class scoping. The form-library framing matters because energy type is one of the most immediate ways class identity reads on form-shift.
21. `08-decomposition-report.md` — empirical findings. Focus on Findings 1–3 (engine partially dimensional, mana bug structural, no melee geometry) and the per-archetype decompositions for physical warriors (`class_0005`, `class_0010`).
22. `../canonical/09-geometry-palette-discussion.md` — light read. Geometry is mostly Phase 3, but Phase 1 may touch the abilities table schema in adjacent ways.
23. `10-decision-log-entry-dimensional-generation.md` — the original draft; canonical version is in `design/decisions/decisions-log.md`. Useful for the cross-references and the "what was rejected" section.

**STOP after reading. Do not begin coding. Do not produce an implementation plan yet.**

Instead, respond with:

1. **A brief one-paragraph summary** confirming you've absorbed the context — in your own words, not a recap.
2. **Questions, concerns, or open items.** Especially: (a) places where the engine code as-it-is looks like it will surprise the implementation (the design assumes things the code doesn't do); (b) assumptions in the design docs that don't match what the code actually contains; (c) anything you want me to clarify about scope, naming convention, testing patterns, or the structure of the energy types themselves (rage build/spend mechanics, focus depletion, combo points, etc.).
3. **Anything you'd want me to verify or confirm** — about preferences, generator validity rules (which energy + element combinations are valid?), naming pipeline integration scope (does Phase 1 update naming? minimal? full?), telemetry schema additions, or migration handling.

**Wait for explicit go-ahead before producing the implementation plan.** Do not interpret "thanks" as permission. Wait for an unambiguous "go" or "proceed."

**After go-ahead — first task is the implementation plan, not code.**

Produce a detailed, reviewable implementation plan as a markdown file at `notes/plans/phase-1-energy-type-axis.md`. The plan should cover:

- **Schema changes:** new fields in the `classes` table (`energy_type`, possibly `energy_pool_max`, `energy_regen_rate`), new columns in the `abilities` table (e.g., `energy_cost_pct` replacing or supplementing `mana_cost_pct`), and the migration that introduces them. How are existing season_000042 rows handled (NULL? backfill heuristic?).
- **Energy type mechanics:** how each of rage, combo, focus, mana, and stamina-as-resource works in combat — build mechanism, spend mechanism, decay/regen, pool size, interaction with abilities. Mana stays as-is; the others are net-new.
- **Code changes by file:** for each file you'll modify, what shape the change takes. Include `class_generator.py` (energy_type as input), `archetype_classifier.py` (now also conditioned on energy_type), `stat_allocator.py` (stat templates may differ by energy type), `role_constraints.py` (ability grammar may need energy-typed cost fields), the combat sim resource model, the telemetry recorder.
- **Generator validity rules:** the matrix of valid energy + element combinations. Some are obvious (rage + physical melee; mana + casters; focus + ranged physical). Some are debatable (could rage exist on a fire-themed class?). Propose a starting matrix and flag the debatable cells.
- **Naming pipeline integration:** does Phase 1 add energy_type to naming context, or is that deferred to a later phase? (My lean: minimal addition — the naming prompt should know energy_type so a "rage-using fire class" doesn't get named like a "mana-using fire mage." But if that requires substantial naming-pipeline work, defer to a sub-task and surface the trade-off.)
- **Combat sim verification:** how you'll verify each energy type produces sustainable, balanced combat. Reuse existing convergence test methodology if possible.
- **Test fixtures:** what classes you'll generate to verify each energy type works (e.g., a rage warrior, a combo rogue, a focus archer, an existing-style mana caster). How you'll measure convergence.
- **Implementation sequence with checkpoints:** break the work into 4–6 steps, each ≤ 1 day, each producing a working state that compiles and runs. Each checkpoint is a natural review point. Examples (suggestive, not prescriptive):
  - Checkpoint 1: schema migration + `energy_type` plumbed through generator inputs (no behavior change yet).
  - Checkpoint 2: rage mechanics in combat sim (mana stays as-is; rage now works).
  - Checkpoint 3: combo and focus mechanics.
  - Checkpoint 4: stamina-as-resource and validity matrix wired into generator.
  - Checkpoint 5: test season generated, convergence verified, mana economy bug confirmed resolved.
  - Checkpoint 6: doc updates (priority-12 status, session note, possibly evolution-plan adjustments).
- **Risks and unknowns** specific to Phase 1, beyond the architectural-level risks already in the register.

Stop after the plan. Let me review and push back / approve before any code is written.

**After plan approval — implement step-by-step, stopping at each checkpoint.**

For each checkpoint:
- Implement the planned work for that checkpoint.
- Run existing tests; verify they still pass (or, if they need updating, explain why and what changed).
- Run new tests / verification specific to the checkpoint.
- Report back to me: what was done, what was learned, what surprised, what's next. Stop and wait for go-ahead before the next checkpoint.

Each checkpoint should be commit-worthy. Commit messages reference the priority test plan and decisions log entry as appropriate.

**Constraints — do not violate these:**

- **Phase 1 only.** Do not implement role orientation, geometry expansion, diversity constraints, or summoner work.
- **Don't regenerate season_000042.** Legacy reference; new structure activates with next generated season.
- **The percentage armor formula (K=3000) and elemental resistance stub from PR #2 carry forward.** Don't undo them.
- **Don't make architectural decisions.** The dimensional generation refactor is decided. If you discover something during implementation that *appears* to require an architectural decision, **pause and surface it** — don't decide unilaterally. The discussion folder at `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/` is where architectural decisions live; ping me, and we'll route there if needed.
- **Don't expand into the spirit-swap mechanics layer.** Questions 4–7 in `collaboration-handoff/06-trial-room-and-class-scoping.md` are deferred.
- **The `base_mana` / `base_stamina` telemetry write gap** (per `project_engine_state_findings.md`) — fix it if your work naturally touches that code path. If not, leave it for a separate small effort. Don't expand scope to chase it.
- **No `--no-verify` on commits.** If a hook fails, fix the underlying issue.

**Stopping condition for Phase 1 overall:**

Phase 1 is complete when:

1. `energy_type` is a generation input dimension used by the class generator.
2. Mana costs are no longer assigned to non-mana classes; rage / combo / focus / stamina cost equivalents work.
3. Rage, combo, focus, and stamina-as-resource mechanics work in the combat simulator.
4. A test season is generated with diverse energy types and converges (≥80% convergence rate, comparable to existing single-energy seasons).
5. The structural monster mana economy bug is no longer reproducible (re-run the seeds in `08-decomposition-report.md` Finding 2 and confirm physical warriors no longer have unsustainable mana cost / mana pool mismatches because they no longer have mana costs at all).
6. Doc updates: `notes/sessions/2026-05-XX.md` for the days the work spans; `test-plans/priority-12-dimensional-refactor.md` Phase 1 sub-section status updated to ✓ Complete; any other docs touched as the work warrants.

After Phase 1 lands, produce two artifacts for me:
- A Phase 1 summary suitable for a session note (built / learned / surprised / next, per `docs/notes-protocols.md`).
- A one-paragraph **"ready for Phase 2"** handoff capturing the new project state — what's now possible, what assumptions Phase 2 can rely on, what surprised in Phase 1 that Phase 2 should be aware of.

**Resumability:**

If the work spans multiple CLI sessions (likely — Phase 1 is ~1 week of effort), each resume starts by re-reading: `notes/plans/phase-1-energy-type-axis.md` for the plan and current checkpoint status, the most recent session note, and `priority-12-dimensional-refactor.md` for current Phase 1 status. Then continue from the last completed checkpoint.

---

## Notes for the project owner

- This prompt is the longest and most consequential of the CLI prompts in this folder. It commits the project to a week of implementation work and sets patterns Phases 2–4 will follow. The orientation reading list is intentionally substantial — orienting cheaply now reduces the cost of misaligned implementation later.
- The **plan-before-code gate** is the most important constraint. Don't let the CLI session skip it, even if it seems eager to start coding. The plan is the artifact you can review and push back on; once code is written, push-back is more expensive.
- **Surfacing scope creep is part of the deal.** If during implementation the CLI session hits something that suggests the architectural decision needs revisiting, that's not a problem — that's the CLI doing its job correctly. Route those discoveries back to this discussion folder, don't let them become unilateral architectural decisions in the engine repo.
- After Phase 1 lands, draft Phase 2 prompt (role orientation axis) here in this discussion folder. Same shape, different scope. Don't pre-draft Phase 2 now — Phase 1's outcomes may shape what Phase 2 needs to look like.
