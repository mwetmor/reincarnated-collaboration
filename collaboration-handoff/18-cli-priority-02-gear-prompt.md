# CLI Session Prompt — Priority 02: Gear Implementation

## How to use this file

This prompt is intended to be pasted into a fresh Claude Code session opened against `/Users/admin/Games/reincarnated-engine/`. It orients the session to **Priority 02 (gear implementation)**, with the design doc at `canonical/17-gear-and-spirit-guide-design.md` as the primary scope reference.

**This is the first non-phase priority** in the dimensional-refactor era. The dimensional refactor (Phases 1–3, with 4 and 5 deferred) provides the architectural foundation; gear is the first additive content layer built on top. Phase 3 PR (#7) was merged; main is at the latest dimensional-complete state.

Estimated budget: **2–3 weeks** (realistic, larger than the original 1–2 week test plan because gear's scope expanded to include the trait infrastructure shared with Priority 14). Same gate pattern as the phase prompts:

1. Substantial reading list to orient
2. Stop-and-ask gate to surface questions before any plan or code
3. After plan approval, **checkpointed implementation** (each ≤ 1 day, independently reviewable)

Target branch: `work/priority-02-gear`.

## The prompt

Copy everything between the dashed lines into a new Claude Code session opened at `/Users/admin/Games/reincarnated-engine/`.

---

I'm starting Priority 02: gear implementation. The dimensional refactor has merged through Phase 3 (Phase 4 and Phase 5 are deferred to medium-term per the project roadmap). Gear is the first additive content priority built on the dimensional architecture.

**This is more than "minimum viable gear."** The original test plan at `engine-repo/test-plans/priority-02-gear-status.md` is Phase 0 era and predates the dimensional refactor. The current design intent is captured in `/Users/admin/Games/reincarnated-collaboration/canonical/17-gear-and-spirit-guide-design.md` and **supersedes the test plan as the primary scope reference**. The test plan remains as historical context.

Gear implementation includes the **trait infrastructure shared with Priority 14 (Traits-and-Skills progression)**. Since gear is the immediate priority, this CLI session builds the trait system that Priority 14 will eventually inherit and exercise more fully. This is a meaningful scope expansion vs. the original test plan.

**Priority 02 scope:**

This priority:

- **Universal gear generation pipeline** — class-agnostic; tier gradient (common / uncommon / rare / epic / legendary); template-named for common/uncommon, LLM-named for rare+.
- **Deterministic gear properties** — `power_score` (universal magnitude) and `class_fit_profile` (5-axis vector matching dimensional generation: energy_type, range_profile, armor_weight, damage_type, role_orientation). Computed by engine from mechanical content; LLM does not propose fit weights.
- **Trait infrastructure** — shared with Priority 14. Schema, validation, combat-sim application, telemetry. Three trait categories: stat traits, ability traits, granted abilities. Provenance and stacking rules per the design doc.
- **Spirit Guide engine-layer API** — pure deterministic functions: `evaluate_gear_swap`, `evaluate_class_health`, `recommend_class_for_context`, `quick_simulate`. NOT a player-facing UI; that's far-future.
- **Convergence loop integration** — gear-aware convergence calibrated against scenario-appropriate average gear (NOT max gear). Per-(class, monster) win rates persisted as bare-class baseline.
- **LLM naming integration** — extends `TrackedLLMClient` with new purposes for rare+ gear naming. `visual_prompt` field for forward-compat with Meshy/Unity.
- **Combat simulator integration** — gear stats applied to combatant; ability modifiers applied per-ability; traits attached/detached on equip/unequip.

This priority does NOT:

- Build the Spirit Guide as a player-facing entity (UI, voice, fade, countdown — far-future post-UI/VFX).
- Implement vendor / economy / crafting / durability / set bonuses / trade — out of scope.
- Implement bad-luck-protection adaptive drops — explicit non-goal per design doc.
- Pre-compute all class × gear × monster combinations — combinatorially infeasible and unnecessary.
- Touch summoner archetypes (deferred to Phase 5, post-UI/VFX).
- Touch the spirit-swap mechanics layer (open questions deferred).
- Address the encounter-quality concern (Priority 13, separately scoped).

**Required reading, in two phases. This is a substantial priority — orient thoroughly.**

**Phase A — Engine repo orientation.**

Read whichever of these exist (skip and report missing):

1. `CLAUDE.md` (engine repo root) — operational orientation.
2. `README.md` (engine repo root) — purpose and structure.
3. `design/CLAUDE.md` if present.
4. `design/decisions/decisions-log.md` — read the dimensional refactor entry plus any subsequent decisions.
5. `design/risks/risks.md`.
6. `design/planning/current-phase.md`.
7. `docs/evolution-plan.md`.
8. `docs/notes-protocols.md`.
9. `test-plans/priority-02-gear-status.md` — **historical context only.** This Phase 0-era plan is superseded by the design doc at file 17. Read for current state of stubs (8 NULL gear rows; `gear_catalog.py` placeholder), but do not treat as scope-of-work.
10. `test-plans/priority-12-dimensional-refactor.md` — Phase 1–3 final status; Phase 4 + 5 deferred.
11. `notes/sessions/` — recent session notes (Phase 1 + Phase 2 + Phase 3 close-outs).

Then read the engine code that gear will integrate with (more substantial than prior phases since gear touches generation + simulator + LLM + telemetry simultaneously):

12. `src/reincarnated/generation/gear_catalog.py` — current stub. Will be replaced/extended.
13. `src/reincarnated/generation/class_generator.py` — generation pipeline; gear generation will integrate here.
14. `src/reincarnated/generation/role_constraints.py` — ability grammar (gear ability modifiers reference these).
15. `src/reincarnated/generation/season_orchestrator.py` — orchestrator (gear generation timing during season generation).
16. `src/reincarnated/llm/naming.py` — LLM naming pipeline; will be extended with gear naming.
17. `src/reincarnated/llm/tracked_client.py` — purpose enumeration; will gain new purposes for gear.
18. `src/reincarnated/telemetry/recorder.py` and `migrations.py` — schema; migration 1.6 will land for gear + traits.
19. **The combat simulator** — gear/trait application during fights. Find the effect resolver, combatant state, damage resolver. Gear stats need to be applied; ability modifiers need to take effect; traits need attach/detach lifecycle.
20. The convergence loop / balance loop code — gear-aware convergence needs to layer in.

Read more code as needed during orientation. The most consequential code paths are the ones gear's mechanical effects flow through (generation → combatant state → damage resolution → telemetry).

**Phase B — Recent design discussion (in `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/`):**

21. `00-working-agreement.md` — meta-rules.
22. `06-trial-room-and-class-scoping.md` — design intent for cross-class smuggling, form library, spirit-swap. Gear's `class_fit_profile` is the mechanism by which cross-class smuggling becomes mathematically meaningful.
23. `../canonical/09-geometry-palette-discussion.md` — geometry palette (gear's ability modifiers reference these geometry types).
24. `10-decision-log-entry-dimensional-generation.md` — original architectural decision.
25. **`../canonical/17-gear-and-spirit-guide-design.md` — THE PRIMARY SCOPE REFERENCE.** Read this carefully. It captures the unified Spirit-Guide-marginal-value architecture, the tier gradient, the trait provenance and stacking rules, the convergence-against-average-gear principle, and explicit out-of-scope items.
26. `../canonical/16-project-roadmap.md` — Priority 02 positioning + Priority 14 (the trait-system inheritor).
27. `12-cli-phase-1-energy-type-prompt.md`, `14-cli-phase-2-role-orientation-prompt.md`, `15-cli-phase-3-geometry-prompt.md` — prior CLI prompts as templates for plan structure and constraint conventions.

**Empirical findings from Phases 1–3 to incorporate into Priority 02 planning:**

- **Per-path AI pattern (refined Phase 2/3):** new behavior may need `_common()` and/or `_scripted()` updates depending on whether it conflicts with DPS-scoring or archetype-priority. Always check both paths when adding combat-sim behavior.
- **Hunter modifier post-Phase-3:** mean 1.055×, bimodal distribution. Gear is the next system that can address this — gear that fits hunter's identity strongly will have high marginal value for hunters, addressing the variance.
- **Controller sub-flavor pattern:** element × control produces 4 distinct identities (lockdown / attrition / disruption / debuff). Gear should respect this — element-themed gear may want to reinforce the per-element controller identity rather than be element-agnostic.
- **Phase 3 `at_melee_range` engagement model:** gear that interacts with melee should respect the engagement state. A weapon-effect that fires "on hit" needs to know whether the hit was a melee strike or a ranged projectile.
- **`python3` operational note:** engine doesn't have a `python` shim; CLI invocations must use `python3`.
- **The "flavor-distinct, math-equivalent" pattern (Phase 3 finding):** several geometry types are different LLM-naming labels backed by identical resolver math. Gear's affixes should follow the same pattern — distinct flavor at LLM/naming layer, possibly identical resolver math at mechanical layer.

**STOP after reading. Do not begin coding. Do not produce an implementation plan yet.**

Instead, respond with:

1. **A brief one-paragraph summary** confirming you've absorbed the context — in your own words.
2. **Questions, concerns, or open items.** Especially:
   - **Trait infrastructure architectural shape.** The design doc specifies attach/detach on equip/unequip, plus stacking rules. Surface your proposed implementation: does the engine have a "trait registry" per combatant? How are traits applied during fight resolution — at attack-time per-ability, or at fight-start as composed effects on the combatant state? Different choices have different performance and clarity trade-offs.
   - **Class_fit_profile computation.** Given gear's mechanical content (which stats it modifies, which abilities it enhances, which dimensional axes its effects target), surface your proposed deterministic algorithm for computing fit weights. Should be reproducible — same gear → same fit profile.
   - **Convergence loop integration.** Gear-aware convergence requires generating "scenario-appropriate average gear" on both player and monster sides during balance runs. What's the algorithm for "average gear" generation? A weighted random draw from each tier matching expected drop rates? Surface your proposal.
   - **Spirit Guide API surface.** The design doc sketches four functions; surface your proposed full signatures and any additional helper functions. These are pure deterministic functions; their tests should be deterministic too.
   - **`visual_prompt` field population.** Should the LLM be prompted explicitly for the visual description (a separate concern from the gear's name and flavor), or should the existing rare+ naming call also produce visual_prompt as part of one combined call? Surface your preference.
   - **Anything from the engine code that suggests architectural surprises.** Trait infrastructure intersects combatant state, ability application, and effect resolution — those are well-trodden code paths but introducing a per-combatant trait registry may surface unexpected coupling. Surface findings now.
3. **Clarifications you'd want me to confirm** — preferred branch name, specific tier-rate percentages (the design doc has ballpark estimates but not committed values), trait-validation rule specifics, anything else.

**Wait for explicit go-ahead** before producing the implementation plan.

**After go-ahead — first task is the implementation plan, not code.**

Produce a detailed plan as `notes/plans/priority-02-gear.md`. The plan should cover:

- **Schema changes:** migration 1.6 (gear table refinements, trait table, possibly per-(class, monster) win rate table). How existing data handles new schema.
- **Trait infrastructure:** schema, validation, attach/detach lifecycle, stacking rules per the design doc, combat-sim application.
- **Gear generation pipeline:** universal generation, tier gradient (common → legendary), template-naming for low tiers, LLM-naming for rare+ tiers.
- **Class_fit_profile computation:** deterministic algorithm, reproducibility, mechanical-content-to-fit-weights mapping.
- **Combat simulator integration:** gear stat application, ability modifier application, trait attach/detach during fight initialization.
- **Convergence loop integration:** average-gear distribution generation, per-(class, monster) win rate persistence.
- **LLM naming integration:** new purposes in tracked client (`name_gear_unique`, possibly `propose_gear_traits`); visual_prompt population.
- **Spirit Guide engine API:** function signatures, deterministic test approach.
- **Telemetry:** what gets recorded; how the existing recorder is extended.
- **Verification approach:** how to test gear's effects on balance, sample naming output, simulate gear-aware convergence.
- **Acceptance criteria.**
- **Implementation sequence with checkpoints** (likely 7–9 steps, each ≤ 1 day, each producing a working state).
- **Risks and unknowns** specific to gear implementation.

Stop after the plan. Let me review and approve before any code is written.

**After plan approval — implement step-by-step, stopping at each checkpoint.**

Same pattern as Phases 1/2/3: implement → test → commit → report (built / learned / surprised / next) → wait for go-ahead.

**Constraints — do not violate these:**

- **Priority 02 (gear) only.** Do not implement Priority 13 (encounter quality), Priority 14 (Traits-and-Skills progression — but DO build the trait infrastructure that Priority 14 will inherit), Phase 4 (diversity constraint), or Phase 5 (summoner).
- **Don't build the Spirit Guide as a player-facing entity.** Engine API only — pure functions. UI/voice/countdown is far-future.
- **Don't touch the spirit-swap mechanics layer** (open questions in `06`).
- **Don't pre-compute all class × gear × monster combinations.** Bounded slices only (per-(class, monster) bare-class win rate; gear power_score; class_fit_profile).
- **Don't make architectural decisions.** If something appears architectural during implementation, pause and surface it. Route back to the discussion folder if needed. The design doc covers the architectural decisions; in-flight decisions should be implementation-level only.
- **Calibrate gear-aware convergence against average gear, not max gear.** This is a load-bearing design call from the design doc. The convergence loop's gear distribution must reflect typical play, not optimal play.
- **No `--no-verify` on commits.** If a hook fails, fix the underlying issue.
- **Use `python3`** for any CLI invocations.

**Stopping condition for Priority 02 overall:**

Priority 02 is complete when:

1. Migration 1.6 lands; gear, traits, and per-(class, monster) win rate tables exist.
2. Universal gear generation produces gear across all five tiers with appropriate naming approach (template for common/uncommon, LLM for rare+).
3. Each gear instance has deterministic `power_score` and `class_fit_profile`; same gear → same values.
4. Trait infrastructure works end-to-end: traits attach on equip, detach on unequip, stack per the rules, get applied correctly in combat-sim resolution.
5. Spirit Guide engine API is implemented as deterministic functions with tests.
6. Gear-aware convergence runs against average-gear baselines; per-(class, monster) win rates persisted.
7. A test season generates with gear; LLM naming for rare+ produces qualitatively distinct gear names; sample names verifiable.
8. Acceptance criteria from the plan are explicitly checked.
9. Doc updates: `notes/sessions/2026-05-XX-priority-02-gear.md`; `test-plans/priority-02-gear-status.md` updated to ✓ Complete; relevant decisions log entries.

After Priority 02 lands, produce two artifacts for me:

- A summary suitable for a session note (built / learned / surprised / next).
- A one-paragraph **"ready for next priority"** handoff capturing the new project state. Specifically: what's now possible because gear exists; what assumptions Priority 13 (encounter quality) and Priority 14 (Traits-and-Skills) can now rely on; what surprised in implementation that future priorities should be aware of.

**Resumability:**

Priority 02 will likely span multiple CLI sessions (~2–3 weeks of work). Each resume re-reads: `notes/plans/priority-02-gear.md` for current checkpoint status, the most recent session note, and the design doc at `/Users/admin/Games/reincarnated-collaboration/canonical/17-gear-and-spirit-guide-design.md` for the architectural reference.

---

## Notes for the project owner

- **Priority 02 is the largest single non-phase priority by scope.** ~2–3 weeks realistic. Don't be surprised if the CLI's plan surfaces an 8th or 9th checkpoint — gear, trait infrastructure, Spirit Guide API, convergence loop integration, and LLM naming are all real chunks of work, and they all touch each other.
- **The trait infrastructure is the surprise expansion.** Original test plan said 1–2 weeks; with traits in scope, realistic is 2–3. Worth setting expectations accordingly.
- **The convergence-against-average-gear principle is load-bearing.** If the CLI's plan calibrates against optimal gear instead, push back hard. That undermines the "break the meta" structural property and produces brittle balance.
- **The Spirit Guide API is engine-layer only.** If the CLI starts proposing UI, voice, countdown, or anything player-facing, push back. That's far-future post-UI/VFX work; this priority is the analytical foundation only.
- **After Priority 02 lands, the natural next steps are Priority 13 (encounter quality, ~1 week) and Priority 14 (Traits-and-Skills, ~2 weeks).** Both will inherit infrastructure built during Priority 02 (per-(class, monster) win rates for Priority 13's encounter analytics; trait system for Priority 14's progression unlocks).
