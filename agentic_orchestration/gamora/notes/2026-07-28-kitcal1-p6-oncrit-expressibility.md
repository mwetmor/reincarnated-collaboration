# KIT-CAL-1 P-6 — can Wave-C express an ATTACKER-TARGETED consequence gated on on_crit?

**Date:** 2026-07-28
**Author:** gamora (simulation seam)
**Cycle:** KIT-CAL-1, run KC1-2026-07-27, conductor gandalf
**Mode:** READ-ONLY research check. No engine source touched, no commits to engine repo.

**Fixture:** Matt's measured Grim Dawn werewolf L13, Battle Surge rank 1 — *on critical hit, heal
SELF 8% max HP per second for 3 seconds, 6 second recharge.* Screenshot 281 (death-2 frame) reports
lifetime "Life healed: ~5649" over 5453s — the mechanism has a measured total waiting on it.

---

## VERDICT: NOT-EXPRESSIBLE → BQ-4

Two of three legs are missing; the third (attacker-target selection) is the one that already works.
Sibling of BQ-3 (calibration-override door, `gamora/v-bq3-calibration-door-1`) — file under the
future defensive-mechanics wave.

---

## Leg 1 — trigger vocabulary: is on_crit a Wave-C trigger? **NO (produced, then dropped)**

The token exists in the spec vocabulary and the crit event is emitted by the kernel resolver — but
nothing in the spatial sim ever logs it.

- `src/reincarnated/generation/resource_economy.py:126-134` — `PROC_TRIGGER_CONDITIONS` includes
  `"on-crit"` (Wave-B five). Spec-side the token is legal.
- `src/reincarnated/simulation/damage_resolver.py:1349` — `events.append("on_crit")` in
  `_apply_crit`. The event IS produced, per hit, underscore-named.
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:3589` — `_wave_c_log_event`
  docstring names on-crit as an intended event site. It is aspirational: no call site supplies it.
- Actual `_wave_c_log_event` call sites — `spatial_engine.py:4545` (`on-hit`), `:4549` (`on-kill`),
  `:4550` (`on-defender-death`), `:4725` (`on-block-successful`), `:4731` (`on-damage-taken`).
  **No on-crit.**
- The player→mob attack path routes through `_apply_skill_damage` (`spatial_engine.py:4533`), which
  never requests `return_events=True`. Only the **mob→player** path opts in
  (`spatial_engine.py:4711-4718`). So the crit list is built inside the resolver on the player's
  own attacks and discarded at the adapter boundary
  (`spatial_resolver_adapter.py:365-368` — `return_events=False` ⇒ float only).
- Naming bridge also absent: resolver emits `on_crit` (underscore); the Wave-C log/match vocabulary
  is hyphenated (`on-crit`). No normalizer exists.

## Leg 2 — target selector: can a consequence resolve to the ATTACKER? **YES — but no heal payload**

This is the leg that exists. Attacker-targeted resolution is already a working, shipped pattern.

- `spatial_engine.py:3759-3761` — `_wave_c_dispatch_consequence`, `resource-fill` branch writes
  `attacker.energy = min(attacker.max_energy, attacker.energy + _fill)`. The consequence resolves to
  the entity that *scored* the event, not the victim. Precedent is unambiguous.
- `spatial_engine.py:3782-3787` — `_wave_c_dispatch_bt` does the same onto the BLOCKER.

What is missing is the payload, not the selector:

- `resource_economy.py:166-173` — `CONSEQUENCE_TYPES` = {`apply-mark`, `consume-mark`, `linked-cast`,
  `resource-fill`, `ailment-overwrite`, `burst-damage`}. **No heal / HP-restore member.**
  `resource-fill` fills `max_energy`; there is no `max_hp` analogue.
- Structural second problem: the mark-consume dispatch requires a live MARK on a DEFENDER
  (`spatial_engine.py:3616-3634`). Battle Surge carries no mark. The mark-free
  trigger→consequence path exists for exactly **one** hard-coded event —
  `spatial_engine.py:3646-3651` gates on `_event == "on-block-successful"`. There is no generic
  `proc_trigger_condition == <event> → dispatch consequence` branch.

## Leg 3 — duration + recharge: 3s tick + 6s ICD? **NO on both halves**

- **3s HoT — machinery exists, but its output never reaches spatial HP.**
  `effect_resolver.py:121-130` implements a real `heal_over_time` ActiveEffect (per-tick
  `tick_heal`, `DOT_TICK_INTERVAL` granularity, `duration_remaining` decay, `hot_recovered`
  BC signal). Constructible in principle.
  **The bridge is one-directional.** `spatial_engine.py:5143-5152` calls `tick_effects` on every
  entity, but `:5163` re-syncs `combatant_state.hp` to the live spatial HP as *scratch*, and `:5186`
  applies **only** the returned DoT float: `e.hp -= _dot`. The HoT's `combatant.hp += actual_heal`
  lands on that scratch state and is thrown away next tick. In the spatial regime, HoT recovery
  does not exist. Any encoding of Battle Surge would heal zero.
- **6s internal cooldown — no primitive.** There is no per-proc ICD anywhere in the consequence
  path. The nearest machinery is the Wave-B RC charge-cycle refill,
  `spatial_engine.py:5108-5114` (`cycle_recharge_accum` / `cycle_recharge_seconds`), which is a
  resource-charge timer bound to skill availability and is not reachable from any consequence
  dispatch. Repurposing it would be a semantic overload, not a wiring job.

---

## Why not EXPRESSIBLE-WITH-GLUE

Each remaining piece crosses a line that glue does not cross:

1. **Logging on-crit** requires threading `return_events=True` through `_apply_skill_damage`
   (`spatial_engine.py:2458+`) — a hot-path signature change on the player attack path — plus a
   `on_crit`→`on-crit` normalizer, plus a mark-free generic trigger→consequence branch to replace
   the hard-coded block-only gate.
2. **A heal consequence_type** is a `CONSEQUENCE_TYPES` vocabulary extension in
   `generation/resource_economy.py` — **rocket's seam**, cross-seam per ADR-002, plus an emission
   surface for the two magnitudes (per-second fraction, duration).
3. **The HoT→spatial-HP bridge is a Discipline #12 semantic shift**, not a bug fix: it changes the
   HP trajectory of *every* entity in the spatial regime that carries a sustain effect, including
   the seeded `regen_per_sec` HoT at `combatant.py:911-915`. It must be framed, math-noted, and
   A/B'd against a full regen — not slipped in under a fixture.

## What BQ-4 owes (scope sketch, for the defensive-mechanics wave)

- Math note: HoT→spatial-HP bridge semantics (double-count guard vs. the existing DoT float bridge;
  overkill/overheal clamp; attribution channel — heal is not negative damage).
- Generic `proc_trigger_condition → consequence` dispatch, replacing the block-only special case.
- Per-proc ICD primitive (`consequence_icd_seconds`) — distinct from RC charge-cycle.
- `CONSEQUENCE_TYPES` extension request to rocket: a self-heal-over-time member carrying
  (fraction-of-max-HP-per-second, duration-seconds).
- Fixture check target: the ~5649 lifetime "Life healed" figure over 5453s is the acceptance
  observable once all four land.

**Related:** BQ-3 (`simulation/spatial_gauntlet/calibration_overrides.py`, math note
`simulation/math/bq3-calibration-override-door-2026-07-28.md`). Both BQ items exist because the
KIT-CAL-1 fixture reaches for real player-side defensive/sustain mechanisms the engine has not
built yet. Neither should be worked around inside the calibration door.
