# CLI Session Prompt — Phase 2: Role Orientation Axis

## How to use this file

This prompt is intended to be pasted into a fresh Claude Code session opened against `/Users/admin/Games/reincarnated-engine/`. It orients the session to **Phase 2 of the dimensional generation refactor** — adding `role_orientation` as the fifth generation dimension. Phase 1 (energy type axis) and the Phase 1 polish session have both landed; this is the next chunk of staged work toward the architectural decision in `engine-repo/design/decisions/decisions-log.md`.

Phase 2's budget is ~1 week of focused implementation work. Same gate pattern as Phase 1:

1. Substantial reading list to orient.
2. Stop-and-ask gate to surface questions before any plan or code.
3. After plan approval, **checkpointed implementation** (each ≤ 1 day of work, independently reviewable).

Target branch: `work/priority-12-phase-2-role-orientation`. Same as Phase 1, the work merges via PR after a session note and acceptance check.

## The prompt

Copy everything between the dashed lines into a new Claude Code session opened at `/Users/admin/Games/reincarnated-engine/`.

---

I'm starting Phase 2 of the dimensional generation refactor: **adding `role_orientation` as a fifth generation input dimension**, distinguishing classes by combat role (damage / support / control / hybrid) on top of the existing four axes. This phase fixes the dimensional gap surfaced in `08-decomposition-report.md`: the four-axis framework couldn't distinguish a fire mage from a fire healer, or an earth caster from an earth controller.

**Phase 2 scope (and what it explicitly is NOT):**

This phase:

- Adds `role_orientation` as a primary generation input dimension with **4 values: `damage` / `support` / `control` / `hybrid`**.
- Generator validity rules per role (each role produces a distinct ability profile).
- Updates the ability grammar to support self-sustain primitives (regen ticks, on-hit lifesteal, spike heals on cooldown, self-damage-for-burst-multiplier) so `damage`-orientation classes can express styles like "spiritual warrior with regeneration" or "bloodmage" without needing a separate orientation.
- Updates the LLM naming pipeline to receive `role_orientation` context (one-line addition similar to Phase 1's `energy_type` integration).
- Verifies convergence across the 4 role values empirically.
- Decides the **validity matrix expansion question** explicitly (see below) — do element × non-mana combinations open up in Phase 2, or stay deferred?

This phase does NOT:

- Expand the geometry palette or build melee mechanics (Phase 3).
- Add the dimensional diversity constraint (Phase 4).
- Implement summoner archetypes or multi-actor sim (Phase 5, deferred).
- Touch the spirit-swap mechanics layer (open questions in `06-trial-room-and-class-scoping.md` § 4–7).
- Regenerate `season_000042` or any earlier legacy seasons.
- Address the name-collision pattern from Phase 1 (the "Smoke-Spire Cantor across 4 classes" finding) — that's prompt-tuning territory, scoped separately.
- Address the seed 400 gauntlet-quality issue — that's a separate priority, deferred.

**Critical taxonomy decision already made (do not relitigate):**

The role_orientation values are **4, not 5**. The original architectural draft had `sustain` as a value; that was refined on 2026-05-08 to drop `sustain` because:

- "Pure sustain" without an ally to support is mechanically meaningless in solo play (the project's design intent is solo-only, per `06-trial-room-and-class-scoping.md`).
- Self-sustain mechanics (regen warriors, bloodmages, lifesteal classes) are *flavor of damage classes*, not a separate orientation — Diablo Necromancer blood builds and WoW Death Knight blood spec are damage classes, not healers.
- "Ally-support" was renamed `support` and gated to multi-actor contexts (Phase 5 summoner provides minions to heal; multiplayer if it ever ships).

**Final values:**

- **`damage`** — primary purpose is dealing damage. Includes self-sustain styles via ability-grammar primitives. Most generated classes.
- **`support`** — primary purpose is supporting allies. Validity-gated: NOT generated for solo seasons until Phase 5 enables strategic context. This value exists in the dimensional space but the generator's validity rules exclude it from solo-only generation.
- **`control`** — primary purpose is locking down enemies (root, knockback, slow, stun, displacement). Captures earth-controller and wind-disruptor identities the four-axis decomposition couldn't distinguish from damage classes.
- **`hybrid`** — combines two primary roles meaningfully. E.g., damage+control. (`damage+support` hybrids inherit `support`'s solo gating.)

**Validity matrix expansion question — explicit decision point:**

Phase 1's validity matrix was: elemental dominant_element → `energy_type = mana`; physical dominant_element → sample from `[rage, combo, focus, stamina-as-resource]`. Cross-combinations (fire-rage warrior, wind-focus archer, earth-defender) were deferred to Phase 2 explicitly — *not architecturally foreclosed*.

Phase 2's plan needs to **decide whether to open up element × non-mana combinations**, with one of three outcomes:

1. **Yes, open it up** — generator can produce a fire-themed rage warrior. More variety, more validity-rule complexity.
2. **No, keep restricted** — elemental classes stay mana, physical classes stay non-mana. Element × non-mana flavor handled later via gear (Priority 02 unblocked after Phase 2).
3. **Limited opening** — some combinations allowed (e.g., physical damage type can pair with elemental flavor element), others forbidden.

The decision rests on user/owner input (this is a design call, not purely technical). Surface it during the questions-and-concerns gate before producing the implementation plan.

**Required reading, in two phases. Read carefully — Phase 2 sets patterns Phases 3–4 will follow, and the role-orientation pattern will be referenced for years.**

**Phase A — Engine repo and design subdirectory orientation (your current working directory).**

Read whichever of these exist (skip and report missing):

1. `CLAUDE.md` (engine repo root, if present).
2. `README.md` (engine repo root, if present).
3. `design/CLAUDE.md` if present.
4. `design/decisions/decisions-log.md` — focus on the dimensional refactor entry and the body-swap → spirit-swap supersession.
5. `design/risks/risks.md` — focus on the dimensional refactor scope risk and any other relevant entries.
6. `design/planning/current-phase.md`.
7. `docs/evolution-plan.md`.
8. `docs/notes-protocols.md`.
9. `test-plans/priority-12-dimensional-refactor.md` — **Phase 2 sub-section is the focus**; this is your scope-of-work document.
10. `test-plans/priority-01-known-issues.md` — Phase 1's resolution context.
11. `test-plans/priority-02-gear-status.md` — gear is unblocked after Phase 2; relevant for understanding Phase 2's "downstream consumer" context.
12. `notes/sessions/2026-05-08-phase1-energy-type.md` — Phase 1 session note, especially "what surprised" and "next."
13. `notes/sessions/` — any polish-related session notes from the 2026-05-08 polish work.

Then read the engine code Phase 2 will modify:

14. `src/reincarnated/generation/class_generator.py` — primary generation entry point. Phase 1 added `energy_type` plumbing here; Phase 2 will add `role_orientation` analogously.
15. `src/reincarnated/generation/archetype_classifier.py` — emergent archetype classification logic. Phase 2 may need to update classification given the new role dimension.
16. `src/reincarnated/generation/role_constraints.py` — ability grammar. Phase 2 will likely need to extend this to differentiate by `role_orientation` (e.g., control classes get root/knockback/slow effects more often; damage classes get more burst).
17. `src/reincarnated/generation/stat_allocator.py` — stat templates per archetype. May need extension for control/support stat profiles.
18. The combat simulator's effect handling (find files dealing with root, knockback, slow, healing-of-others). Phase 2 needs to ensure the simulator handles control effects and (if `support` is exercised in any test context) ally-targeted heals.
19. `src/reincarnated/llm/naming.py` (or wherever class/monster naming lives). Phase 2 adds `role_orientation` to the naming context.
20. `src/reincarnated/telemetry/recorder.py` and `migrations.py` — Phase 2 needs migration 1.4 (add `role_orientation` column to classes; add it to monsters too).

Read more code as needed during orientation.

**Phase B — Recent design discussion (in `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/`):**

21. `00-working-agreement.md` — meta-rules. (Discussion folder rules; engine-repo session may write code, run tests, commit.)
22. `06-trial-room-and-class-scoping.md` — design intent: spirit-swap, form library, class scoping. Form-library framing matters for role orientation: each cycled form should feel mechanically distinct, and role is one of the most readable distinctions.
23. `08-decomposition-report.md` — empirical findings. Especially Findings 1–3 and the per-archetype decompositions for the support_healer (which surfaced the role-axis gap) and the earth/wind casters (which surfaced the controller/disruptor distinction).
24. `../canonical/09-geometry-palette-discussion.md` — geometry palette. Phase 3 territory but informs role-orientation thinking (e.g., control orientation may need ground_targeted_circle or persistent_zone disproportionately).
25. `10-decision-log-entry-dimensional-generation.md` — original architectural decision draft.
26. `12-cli-phase-1-energy-type-prompt.md` — Phase 1's prompt. Phase 2 should mirror its structure for plumbing/checkpointing patterns. Pay attention to the per-path AI pattern Phase 1 surfaced (combo AI fix had to be applied in both `_common()` and `_scripted()` — Phase 2 should expect to do the same for any role-aware AI logic).
27. `13-cli-phase-1-polish-prompt.md` — context on the polish work and the operational note that the engine requires `python3` invocation.

**STOP after reading. Do not begin coding. Do not produce an implementation plan yet.**

Instead, respond with:

1. **A brief one-paragraph summary** confirming you've absorbed the context — in your own words, not a recap.
2. **Questions, concerns, or open items.** Especially:
   - **The validity matrix expansion question.** Recommend an option (yes/no/limited opening of element × non-mana combinations) with reasoning. Surface what the decomposition's per-archetype data suggests.
   - Places where the engine code as-it-is looks like it'll surprise the implementation (e.g., role-relevant effects like root/knockback are stored in JSON `effects` columns; the implementation needs a clean way to read those for role classification).
   - The `support`-orientation gating — how exactly does the generator exclude support from solo generation? A flag passed through the orchestrator? A validity rule that consults a "is solo" config? Surface your proposed approach.
   - Whether Phase 2 should also test in a contrived multi-actor context (e.g., synthesize a support class generation just to verify its ability profile makes sense, even if the simulator can't run it standalone) or fully defer support-orientation to Phase 5.
   - Anything from Phase 1's findings that suggests Phase 2 should pre-tune (e.g., balance floor at 0.05 — should Phase 2 try to tighten it back toward 0.20 by producing classes with more balanced base power?).
3. **Clarifications you'd want me to confirm** — preferred branch name, the exact element × non-mana validity decision, naming-prompt scope, anything else.

**Wait for explicit go-ahead** before producing the implementation plan.

**After go-ahead — first task is the implementation plan, not code.**

Produce a detailed plan as `notes/plans/phase-2-role-orientation.md`. The plan should cover:

- **Schema changes:** migration 1.4 (add `role_orientation` to classes; add to monsters as well; possibly extend the abilities table if role-aware ability metadata is needed). How existing rows (Phase 1 seasons + legacy seasons) handle the new column.
- **Validity matrix decision:** the resolved answer to element × non-mana combinations, with rationale.
- **Role-specific generation rules per value:** how the generator differs when producing a damage vs. control vs. hybrid class. (Support is gated to non-solo, so Phase 2 may stub its rules without exercising them in a real season run.)
- **Ability grammar extensions:** self-sustain primitives (regen tick, lifesteal, spike heal, self-damage burst), and any role-relevant effect distributions (control gets more root/knockback/slow; damage gets more direct-damage; etc.).
- **Code changes by file** (similar to Phase 1's plan structure).
- **Naming pipeline integration** (one-line addition; same pattern as Phase 1's energy_type).
- **Combat sim updates** (control effects already exist mostly; verify they're applied correctly given a role-aware emphasis).
- **Convergence verification approach:** test season generation across the 4 role values; expected outcomes; tuning targets.
- **Acceptance criteria.**
- **Implementation sequence with checkpoints** (4–6 steps, each ≤ 1 day, each producing a working state).
- **Risks and unknowns** specific to Phase 2.

Stop after the plan. Let me review and approve before any code is written.

**After plan approval — implement step-by-step, stopping at each checkpoint.**

Same pattern as Phase 1: implement → test → commit → report (built / learned / surprised / next) → wait for go-ahead.

**Constraints — do not violate these:**

- **Phase 2 only.** Do not implement geometry expansion (Phase 3), diversity constraints (Phase 4), or summoner work (Phase 5).
- **`role_orientation` has 4 values, not 5.** Do not reintroduce `sustain` regardless of how natural it might feel — that decision is settled.
- **`support` is gated.** Do not generate support classes for solo seasons. The validity rule must exclude them.
- **Don't regenerate legacy seasons or Phase 1 seasons.** New `role_orientation` data activates with the next generated season.
- **The Phase 1 percentage armor formula (K=3000) and elemental resistance stub** carry forward. Don't undo them.
- **Don't make architectural decisions.** If Phase 2 surfaces something that *appears* architectural, pause and surface it — don't decide unilaterally. Route back to the discussion folder.
- **Don't expand into the spirit-swap mechanics layer.**
- **Don't address the name-collision Phase-1 finding** (Smoke-Spire Cantor pattern) — separately scoped.
- **Don't address the seed 400 gauntlet-quality issue** — separately scoped.
- **No `--no-verify` on commits.** If a hook fails, fix the underlying issue.
- **Use `python3`** for any CLI invocations (engine doesn't have a `python` shim; this was an operational learning from Phase 1 polish).

**Stopping condition for Phase 2 overall:**

Phase 2 is complete when:

1. `role_orientation` is a generation input dimension used by the class generator.
2. Generator produces classes across `damage`, `control`, and `hybrid` orientations in solo seasons (with `support` validity-gated and not generated).
3. Ability grammar supports self-sustain primitives so damage-orientation self-sustain classes can emerge naturally.
4. A test season generated with diverse role orientations converges (≥80% convergence rate, comparable to Phase 1 seasons).
5. Naming pipeline picks up `role_orientation` and produces qualitatively different names per role (e.g., a `control`-orientation earth class names differently from a `damage`-orientation earth class).
6. The validity matrix expansion question is answered explicitly in the plan and decisions log.
7. Doc updates: `notes/sessions/2026-05-XX-phase2-role-orientation.md`; `test-plans/priority-12-dimensional-refactor.md` Phase 2 sub-section status updated to ✓ Complete.

After Phase 2 lands, produce two artifacts for me:

- A Phase 2 summary suitable for a session note (built / learned / surprised / next).
- A one-paragraph **"ready for Phase 3"** handoff capturing the new project state.

**Resumability:**

If the work spans multiple CLI sessions, each resume starts by re-reading: `notes/plans/phase-2-role-orientation.md` for the plan and current checkpoint status, the most recent session note, and `priority-12-dimensional-refactor.md` for current Phase 2 status.

---

## Notes for the project owner

- **The validity matrix expansion question is the most consequential design call inside Phase 2.** Don't let the CLI defer it indefinitely; the plan needs to commit to an answer (yes / no / limited) so the implementation matches. If the CLI's recommendation feels off, push back during the questions gate.
- **The `support` gating is a small but important detail.** The implementation should make it easy to flip support back on later (when summoner Phase 5 lands or multiplayer becomes real). A clean validity rule like `if context.allows_multi_actor: include support` is better than special-casing.
- **The `damage`-orientation self-sustain primitives** are where Class A and Class B from the design discussion materialize. The ability grammar additions should be substantive enough that a "spiritual warrior with regen" or "bloodmage with self-damage burst" can actually emerge from generation, not just be a possibility on paper.
- After Phase 2 lands, draft Phase 3 prompt (geometry palette expansion) here in this discussion folder. Phase 3 is the larger work item — 1.5–2 weeks per the original plan, with the geometry palette already designed in `../canonical/09-geometry-palette-discussion.md`.
