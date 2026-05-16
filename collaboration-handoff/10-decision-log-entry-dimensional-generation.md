# Decisions-Log Entry — Dimensional Generation Refactor

## Purpose of this file

This file was a **drafted entry** that has since been added to `engine-repo/design/decisions/decisions-log.md` (commit `973eb7f`, 2026-05-08), reformatted to match the log's existing conventions during the doc maintenance pass. Preserved here as the original drafting artifact for historical reference; the canonical decision now lives in the design subdirectory of the engine repo.

---

## Dimensional generation refactor adopted (Option C, staged) — 2026-05-08

**What was decided:**

Adopt Option C from `collaboration-handoff/04-decision-options.md`: refactor class and monster generation around dimensional composition, replacing element-as-only-generation-input with five generation dimensions. Staged delivery in roughly four phases over an estimated 4–6 weeks (budget against the upper end).

Specific components:

1. **Five dimensional axes** as primary generation inputs:
   - `energy_type` (rage / combo / focus / mana / stamina-as-resource)
   - `range_profile` (close / medium / long)
   - `armor_weight` (light / medium / heavy)
   - `damage_type` (physical / fire / wind / water / earth / hybrid)
   - `role_orientation` (damage / sustain / control / hybrid)

   Element was already an input in the pre-existing pipeline (per `08-decomposition-report.md` Finding 1); archetype labels remain emergent classifications.

2. **Geometry palette of 16 active types** per `canonical/09-geometry-palette-discussion.md`: current 6 + 8 net-new (`melee_strike`, `melee_arc`, `ground_slam`, `ranged_physical`, `ground_targeted_circle`, `teleport`, `self_buff`, `totem`) + 2 marginal (`aura`, `beam_channel`, generator-restricted to archetypes that demand sustained effects).

3. **Class structure per season:** 5–6 playable + 3 act-boss (1 undertuned below the 40% balance threshold, 2 over-tuned at ~55% and ~60%). Per `collaboration-handoff/06-trial-room-and-class-scoping.md`.

4. **Existing season_000042 treated as legacy reference.** Not regenerated. New structure activates with next generated season.

5. **Summoner archetypes deferred to Phase 2** (separate, "much later" effort): multi-actor simulator support, minion AI, and activation of `summon_combatant` / `ally_target` / `ally_radius` in the active palette. Confirmed wanted by collaborator (son); explicitly scheduled as later work, not part of initial rollout.

6. **Sixth axis (control type: lock vs. displace) deferred** unless Phase 2 of dimensional rollout reveals friction that `role_orientation` cannot absorb as sub-dimensional flavor.

**Staged delivery:**

| Phase | Scope | Estimate | Unlocks |
|-------|-------|----------|---------|
| 1 | Energy type axis: rage/focus/etc. mechanics in combat; `energy_type` as generation input; remove default mana from non-mana classes | ~1 week | Structural fix to monster mana economy bug |
| 2 | Role orientation axis: 5th dimension; generator validity rules across damage / sustain / control / hybrid | ~1 week | Healer / controller distinct from caster; supports trial-room differentiation |
| 3 | Geometry palette expansion: 8 net-new + 2 marginal types; adjacency mechanics for melee; `range_profile` becomes meaningful | ~1.5–2 weeks | Warriors get real melee; full dimensional expressivity |
| 4 | Dimensional diversity constraint: generator enforces no two classes per season share full dimensional profile | ~few days | Trial-room mechanic mechanically viable |

**Why:**

Spirit-swap differentiation (player cycling through collected forms via the trial-room mechanic) is confirmed load-bearing for design intent; class identity must read instantly under cycling, not develop over hours of play. Side-by-side selection in the trial room with no class names forces the player to evaluate via mechanical / visual identity — which is exactly what dimensional axes provide.

The trial-room mechanic is *mechanically incompatible* with current generation: season_000042 produces two of each archetype with identical dimensional profiles, leaving the player to choose between visible duplicates. This is a hard incompatibility, not a soft preference.

The monster mana economy bug is structural rather than a sampling issue (per `08-decomposition-report.md` Finding 2): physical warriors are assigned `mana_cost_pct` of 14–30% by a pipeline that has no concept of non-mana classes, then given stat distributions (int=5, wis=7) that produce essentially no mana pool. Tactical patches address symptoms; only dimensional generation removes the structural assumption that every class has mana.

Investigation revealed the engine is already partially dimensional — element is a first-class generation input, and `archetype_classifier.py` derives archetype labels post-hoc. Option C is therefore not "rebuild from scratch" but "extend a partial design."

Options A and B were considered and rejected:

- **Option A (tactical fixes)** cannot deliver the trial-room mechanic and band-aids the structural bug rather than addressing why it is possible.
- **Option B (energy types within current architecture)** had a confused framing — there are no archetype templates to add energy types into, since archetypes are emergent labels. B reduces in practice to "C with fewer axes," leaving warriors broken (no melee geometry) and dimensional duplicates intact.

**Implications for priorities:**

- `work/priority-01-physical-warrior` branch: merge as-is to capture the percentage-armor formula (K=3000) and convergence wins, *before* Phase 3 reworks warrior generation structurally. The formula improvement is independent of the dimensional refactor and should not be lost.
- Priority 02 (gear): unblocked after Phase 2 (resource architecture decided + role orientation in place).
- Priority 11 (monster mana economy): subsumed by Phase 1.
- Priority 12 (resource architecture): essentially is Phase 1.
- New priority test plans needed for Phases 1–4 of the dimensional refactor (or one umbrella plan with phase sub-sections).

**Conditions to revisit:**

- If Phase 3's melee geometry / adjacency mechanics run more than ~1 week longer than estimated, revisit whether Phase 4 (diversity constraint) ships before melee is polished, or accept warriors-as-`projectile` for one more season.
- If a sixth axis (control type) is clearly needed during Phase 2 implementation, expand scope rather than fight it.
- If summoner Phase 2 work later proves > 2 weeks of additional scope, revisit whether summoner archetypes ship at all or are dropped from the design.

**Open questions not blocking this decision:**

- Spirit-swap mechanics layer (per `06-trial-room-and-class-scoping.md` § "Open questions" 4–7): earth-self as class vs. abstract anchor; duration model; form-shift cost; earth-self vulnerability. These affect simulator scope when form-cycling becomes implementable, but Phases 1–4 do not depend on them.
- Trial dungeon structure and visual rendering pipeline (Mixamo-Unity skins or equivalent): far-future work.

**Cross-references:**

- `collaboration-handoff/03-architectural-proposal.md` — original dimensional generation proposal.
- `collaboration-handoff/04-decision-options.md` — A/B/C options analyzed.
- `collaboration-handoff/06-trial-room-and-class-scoping.md` — design intent: spirit-swap, form library, class scoping, trial-room mechanic.
- `collaboration-handoff/08-decomposition-report.md` — empirical evidence from decomposing season_000042 archetypes.
- `canonical/09-geometry-palette-discussion.md` — geometry palette decisions and consumability filter.
