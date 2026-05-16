# CLI Session Prompt — Phase 3: Geometry Palette and Adjacency Mechanics

## How to use this file

This prompt is intended to be pasted into a fresh Claude Code session opened against `/Users/admin/Games/reincarnated-engine/`. It orients the session to **Phase 3 of the dimensional generation refactor** — adding 8 net-new geometry types (plus 2 marginal), building adjacency mechanics in the simulator, activating the `range_profile` axis, and unlocking physical × control as a coherent class identity. Phase 1 (energy type axis) and Phase 2 (role orientation axis) have both fully merged; this is the largest of the three implementation phases.

Phase 3's budget is ~1.5–2 weeks per the original plan, **realistically 2 weeks given the volume**. Same gate pattern as Phases 1 and 2:

1. Substantial reading list to orient.
2. Stop-and-ask gate to surface questions before any plan or code.
3. After plan approval, **checkpointed implementation** (each ≤ 1 day of work, independently reviewable).

Target branch: `work/priority-12-phase-3-geometry`. Same as Phase 1/2 pattern, the work merges via PR(s) after a session note and acceptance check.

## The prompt

Copy everything between the dashed lines into a new Claude Code session opened at `/Users/admin/Games/reincarnated-engine/`.

---

I'm starting Phase 3 of the dimensional generation refactor: **adding 8 net-new geometry types (plus 2 marginal) to the ability grammar, building adjacency mechanics in the simulator, and activating the `range_profile` axis as the third dimensional input.** This phase closes the structural gap that's been visible in production data since Phase 1: warriors use generic `projectile` geometry as melee fallback, hunters need 1.5–1.9× damage modifiers to converge because they're mechanically indistinguishable from mages with single_target abilities.

**Phase 3 scope (and what it explicitly is NOT):**

This phase:

- Adds the **8 net-new CORE geometry types** per the agreed palette in `../canonical/09-geometry-palette-discussion.md`: `melee_strike`, `melee_arc`, `ground_slam`, `ranged_physical`, `ground_targeted_circle`, `teleport`, `self_buff`, `totem`.
- Adds the **2 CORE-MARGINAL types** with generator restrictions: `aura` (paladin/druid sustained-radial only), `beam_channel` (channeled-magic mages only).
- Builds **adjacency mechanics** in the combat simulator: a numeric definition of "close range" so melee abilities have proper engagement geometry. This is the largest single sim addition.
- Activates the `range_profile` axis with values **`close` / `medium` / `long`**. *Note on framing:* `range_profile` values are close/medium/long; "melee" is a geometry type within the close-range bucket, not a `range_profile` value itself. Don't conflate them.
- **Expands the validity matrix:** physical × control becomes possible (wrestlers / grapplers / trappers using `melee_strike` + `ground_slam` + control effects). Physical × hybrid likewise becomes possible. Hunters get `ranged_physical` mechanics (pierce / multishot / ballistic) distinct from generic `projectile`.
- Updates the LLM naming pipeline to receive `range_profile` and richer geometry context (one-line addition matching the Phase 1/2 pattern).
- Verifies convergence across the new geometry-using archetypes empirically. **Strong expectation: hunter modifiers drop toward 0.5–1.0 from the current 1.5–1.9× range, validating the "hunters need ranged_physical to be mechanically meaningful" hypothesis.**

This phase does NOT:

- Add the dimensional diversity constraint (Phase 4).
- Implement summoner archetypes, multi-actor sim, or the STAGED geometry types (`summon_combatant`, `ally_target`, `ally_radius`) — Phase 5, deferred.
- Touch the spirit-swap mechanics layer (open questions in `06-trial-room-and-class-scoping.md` § 4–7).
- Fix the encounter-quality issue (gauntlet weakness / trial boss difficulty ceiling). That's Priority 13 territory, separately scoped.
- Address the name-collision pattern (Smoke-Spire Cantor finding from Phase 1 CP7). Still open, lower priority than the geometry work.
- Regenerate prior seasons. New geometry data activates with the next generated season after Phase 3 lands.

**Phase 3 validity matrix (the explicit revision from Phase 2):**

Phase 2's matrix was: elemental → mana energy + any role; physical → non-mana energy + damage-only role. Phase 3 expands the *physical-side* of the matrix:

| Dominant element | Energy types | Role orientations | Range profiles | Notes |
|---|---|---|---|---|
| fire / water / earth / wind | mana | damage / control / hybrid (support gated) | medium / long mostly; close possible for melee elementals (paladin-like) | element × non-mana combinations remain DEFERRED to Phase 4 / gear pathway |
| physical | rage / combo / focus / stamina | damage / control / hybrid | close / medium / long | physical × control unlocked by `melee_strike` / `ground_slam`; physical × hybrid unlocked by mixed-geometry combinations |

**Element × non-mana cross-combinations are still deferred** (a fire-themed rage warrior, etc.). Phase 4's diversity constraint and Priority 02's gear pathway provide alternative paths to elemental flavor on physical classes. Don't open that matrix in Phase 3.

**Required reading, in two phases. Phase 3 is the largest implementation phase by volume — orient thoroughly.**

**Phase A — Engine repo and design subdirectory orientation (your current working directory).**

Read whichever exist (skip and report missing):

1. `CLAUDE.md` (engine repo root, if present).
2. `README.md` (engine repo root, if present).
3. `design/CLAUDE.md` if present.
4. `design/decisions/decisions-log.md` — focus on the dimensional refactor entry; Phase 1 and Phase 2 outcomes will inform Phase 3 patterns.
5. `design/risks/risks.md` — focus on the dimensional refactor scope risk and any encounter-quality entries.
6. `design/planning/current-phase.md`.
7. `docs/evolution-plan.md`.
8. `docs/notes-protocols.md`.
9. `test-plans/priority-12-dimensional-refactor.md` — **Phase 3 sub-section is the focus**; this is your scope-of-work document.
10. `test-plans/priority-01-known-issues.md` — the percentage armor formula (K=3000) and elemental resistance stub from PR #2 carry forward into Phase 3's warrior generation rework. Don't undo them.
11. `test-plans/priority-02-gear-status.md` — gear is unblocked after Phase 2; Phase 3's geometry palette interacts with eventual gear design.
12. `notes/sessions/2026-05-08-phase1-energy-type.md` — Phase 1 session note.
13. `notes/sessions/` — any Phase 2 session notes; especially the controller sub-flavor taxonomy finding.
14. `notes/plans/phase-2-role-orientation.md` — Phase 2's plan structure as a template for Phase 3's plan.

Then read the engine code Phase 3 will modify — this is more substantial than prior phases since Phase 3 touches both generation and simulator:

15. `src/reincarnated/generation/role_constraints.py` — ability grammar, where the new geometry types must be registered. Largest single change.
16. `src/reincarnated/generation/class_generator.py` — primary generation entry point.
17. `src/reincarnated/generation/archetype_classifier.py` — emergent classification; will need extension for physical × control archetypes (wrestlers, grapplers, trappers).
18. `src/reincarnated/generation/stat_allocator.py` — stat templates for new physical archetypes.
19. **The combat simulator's effect / engagement / range handling.** Find and read whatever currently models distance, hit ranges, projectile travel, AOE shapes. Adjacency mechanics are net-new and need to slot into this layer cleanly.
20. The damage_resolver and any code dealing with effect application, especially for movement-based abilities (`teleport`, `dash_attack`-equivalents) and sustained effects (`aura`, `beam_channel`).
21. `src/reincarnated/llm/naming.py` — Phase 3 adds `range_profile` to naming context.
22. `src/reincarnated/telemetry/recorder.py` and `migrations.py` — migration 1.5 adds `range_profile` column to classes; possibly extends abilities table for new geometry-type validity.

Read more code as needed during orientation; the simulator's range/distance handling is the part most likely to surface architectural surprises — read it carefully.

**Phase B — Recent design discussion (in `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/`):**

23. `00-working-agreement.md` — meta-rules.
24. `06-trial-room-and-class-scoping.md` — design intent: spirit-swap, form library, class scoping. Phase 3 makes the trial-room mechanic mechanically richer because side-by-side bosses with different range profiles read very differently at the silhouette layer.
25. `08-decomposition-report.md` — empirical findings, especially Finding 3 (no melee geometry exists). Phase 3 closes that gap directly.
26. `../canonical/09-geometry-palette-discussion.md` — **the agreed geometry palette and consumability filter.** This is your design spec for the new types; reference its CORE / CORE-MARGINAL / DEFER classifications throughout.
27. `10-decision-log-entry-dimensional-generation.md` — original architectural decision draft.
28. `12-cli-phase-1-energy-type-prompt.md` — Phase 1's prompt.
29. `13-cli-phase-1-polish-prompt.md` — operational learnings, especially the `python3` requirement.
30. `14-cli-phase-2-role-orientation-prompt.md` — Phase 2's prompt structure as a template.

**Empirical findings from Phases 1+2 to incorporate into Phase 3 planning:**

- **The hunter empirical pattern (load-bearing for Phase 3):** every class in the production DB needing modifier > 1.5 is a hunter, across 3 seasons (200, 046, 093). Modifiers 1.656, 1.844, 1.938. Hunters are mechanically thin without `ranged_physical` geometry — they use generic projectile/single_target, identical to mages, with no damage advantage from their stat profile. **Phase 3's success criterion:** hunter modifiers drop toward 0.5–1.0× after `ranged_physical` lands. If they don't drop substantially, that's structurally informative and worth surfacing.
- **The controller sub-flavor taxonomy (Phase 2 CP5/CP6):** element × control produced 4 mechanically-distinct controller identities (lockdown / attrition / disruption / debuff per earth/water/wind/fire). **Expect similar emergent sub-flavors in Phase 3** as element × range_profile or role × geometry composes. Don't try to enumerate; let convergence behavior reveal the coherent combinations.
- **The per-path AI pattern (refined Phase 2 CP3):** new AI behavior may need to be applied to both `_common()` and `_scripted()` or only one — depends on whether it conflicts with DPS-scoring or with archetype-priority lookup. Always check both paths; don't always duplicate.
- **The balance floor at 0.05** carries forward from Phase 1 CP5. Whether it stays at 0.05 or tightens in Phase 3 is empirical — let CP-equivalent verification show the data.
- **The lifesteal ceiling is at 0.12** (Phase 2 CP5 tightening). Carries forward.
- **Phase 1's percentage armor formula (K=3000) and elemental resistance stub** carry forward.

**STOP after reading. Do not begin coding. Do not produce an implementation plan yet.**

Instead, respond with:

1. **A brief one-paragraph summary** confirming you've absorbed the context — in your own words.
2. **Questions, concerns, or open items.** Especially:
   - **Adjacency mechanics design.** What does "close range" mean numerically? Distance threshold? Engagement state (in-melee vs not)? Engagement range? Surface your proposed model. This is the most consequential design question inside Phase 3.
   - **Pierce / multishot / ballistic mechanics for `ranged_physical`.** Are these always-on properties or per-ability parameters? What does the simulator need to support?
   - **Sustained effect handling for `aura` and `beam_channel`.** Does the simulator currently have a "while-active" effect model, or does Phase 3 need to add one?
   - **Teleport / movement primitives.** Does the simulator have any movement model, or are abilities currently positional-stateless? Surface what already exists vs. what needs to be built.
   - **Generator restrictions for marginal types.** What signals an archetype's role profile "clearly demands" sustained effects (aura/beam_channel)? Likely tied to role_orientation, but propose explicit rules.
   - **Validity matrix expansion specifics.** The matrix above lists physical × control / hybrid as unlocked. Propose the specific archetype labels (e.g., `physical_grappler`, `physical_trapper`, `physical_skirmisher`) — same `[element]_[role]` pattern as Phase 2's controller labels, or a different pattern given physical-side variety?
   - **Anything from the simulator code that suggests architectural surprises.** Range/distance/engagement handling is the area most likely to surface "wait, the sim doesn't support this concept at all" findings. Surface them now rather than during implementation.
3. **Clarifications you'd want me to confirm** — preferred branch name, archetype label conventions for new physical-side classes, anything else.

**Wait for explicit go-ahead** before producing the implementation plan.

**After go-ahead — first task is the implementation plan, not code.**

Produce a detailed plan as `notes/plans/phase-3-geometry.md`. The plan should cover:

- **Schema changes:** migration 1.5 (`range_profile` column on classes; possibly extensions to abilities for geometry-type validity). How existing rows handle the new column.
- **Adjacency mechanics design:** the numeric / state model for close-range. Most consequential design call.
- **New geometry types — implementation per type:** for each of the 8 CORE + 2 marginal types, the simulator behavior, generator validity rules, and any new effect handling.
- **`range_profile` axis activation:** how the orchestrator picks range_profile per class, the validity matrix as specified above, naming pipeline integration.
- **Generator validity rules:** physical × control archetype labels, physical × hybrid handling, marginal type restrictions.
- **Combat sim updates:** range-based engagement, ballistic projectile mechanics, sustained-effect support, movement primitives.
- **Naming pipeline integration** (one-line addition per the Phase 1/2 precedent: `Range profile: <value>`).
- **Convergence verification approach:** test season generation with all new geometry types represented; expected outcomes; specific success criterion of hunter modifiers dropping toward 0.5–1.0.
- **Acceptance criteria.**
- **Implementation sequence with checkpoints** (likely 7–8 steps, each ≤ 1 day, each producing a working state).
- **Risks and unknowns** specific to Phase 3.

Stop after the plan. Let me review and approve before any code is written.

**After plan approval — implement step-by-step, stopping at each checkpoint.**

Same pattern as Phase 1/2: implement → test → commit → report (built / learned / surprised / next) → wait for go-ahead.

**Constraints — do not violate these:**

- **Phase 3 only.** No Phase 4 (diversity constraint), Phase 5 (summoner), or Priority 13 (encounter quality) work.
- **Don't open the element × non-mana validity matrix.** That decision was made in Phase 1 (deferred) and reaffirmed in Phase 2 (still deferred). Phase 4 + gear pathway handle elemental flavor on physical classes via different mechanisms.
- **Don't regenerate prior seasons.** New geometry data activates with the next generated season after Phase 3 lands.
- **The percentage armor formula (K=3000) and elemental resistance stub** carry forward.
- **Don't make architectural decisions.** If Phase 3 surfaces something architectural — especially around the simulator's range/engagement/movement model — pause and surface it. Route back to the discussion folder if needed.
- **Don't address the encounter-quality concern** (Priority 13). It's separately scoped.
- **Don't address the name-collision pattern.** Separately scoped.
- **No `--no-verify` on commits.** If a hook fails, fix the underlying issue.
- **Use `python3`** for any CLI invocations (engine doesn't have a `python` shim — operational learning from Phase 1 polish).

**Stopping condition for Phase 3 overall:**

Phase 3 is complete when:

1. All 8 CORE geometry types are registered in the ability grammar and produce coherent abilities when sampled.
2. The 2 CORE-MARGINAL types (aura, beam_channel) are registered with generator restrictions enforced.
3. Adjacency mechanics work in the simulator — melee abilities engage at close range; non-close abilities don't.
4. `range_profile` is a generation input with `close` / `medium` / `long` values.
5. Physical × control validity matrix expansion: at least one new physical-side archetype label is generated (e.g., `physical_grappler` or whatever convention you chose), and it converges.
6. Hunter modifier drops toward 0.5–1.0× from the current 1.5–1.9× range (the load-bearing empirical success criterion).
7. A test season generated with diverse geometry types converges (≥80% rate).
8. Naming pipeline picks up `range_profile` and produces qualitatively different names per range (a close-range warrior names differently from a long-range archer).
9. Doc updates: `notes/sessions/2026-05-XX-phase3-geometry.md`; `test-plans/priority-12-dimensional-refactor.md` Phase 3 sub-section status updated to ✓ Complete.

After Phase 3 lands, produce two artifacts for me:

- A Phase 3 summary suitable for a session note (built / learned / surprised / next).
- A one-paragraph **"ready for Phase 4"** handoff capturing the new project state.

**Resumability:**

Phase 3 will likely span multiple CLI sessions given the volume. Each resume starts by re-reading: `notes/plans/phase-3-geometry.md` for current checkpoint status, the most recent session note, and `priority-12-dimensional-refactor.md`.

---

## Notes for the project owner

- **Phase 3 is the largest of the three implementation phases by code volume.** Realistic ~2 weeks; budget against the upper end. Don't be surprised if the CLI's plan surfaces the need for an 8th or 9th checkpoint — the geometry palette + simulator work is genuinely large.
- **The adjacency mechanics design is the most consequential call inside Phase 3.** Push back during the questions gate if the CLI's proposal feels off. Distance-threshold vs. engagement-state vs. engagement-range are meaningfully different design choices that will affect how melee combat *feels*.
- **Hunter modifier dropping toward 0.5–1.0 is the load-bearing empirical success criterion.** If it doesn't drop, something else is off — surface and we'll diagnose together rather than letting it become an in-flight tuning fight.
- **Expect emergent sub-flavors per geometry × role.** Phase 2 surprised us with 4 distinct controller identities per element. Phase 3 will likely produce similar sub-flavors per range_profile × role × element. Plan for them rather than be surprised.
- After Phase 3 lands, Phase 4 (dimensional diversity constraint) is the smaller follow-up that completes the Option C architectural decision. Phase 5 (summoner) is "much later." Priority 13 (encounter quality) and the name-collision fix are candidates for between-phase polish work.
