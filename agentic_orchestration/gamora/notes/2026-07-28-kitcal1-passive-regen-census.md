# KIT-CAL-1 — passive health-regen census (sim seam)

**Date:** 2026-07-28
**Author:** gamora (simulation seam)
**Cycle:** KIT-CAL-1, run KC1-2026-07-27, conductor gandalf
**Mode:** READ-ONLY census + estimate. No engine source touched. No implementation.
**Predecessor:** `2026-07-28-kitcal1-p6-oncrit-expressibility.md` (BQ-4 — the crit-proc HoT ruling)
**Door under discussion:** `gamora/v-bq3-calibration-door-1`

Matt's challenge: the fixture's measured "Life healed ~5,649" is survival the sim werewolf will not
have. This note establishes what the sim actually does about passive HP restoration, before anything
is proposed.

---

## Q1 — Does ANY per-tick passive health regeneration reach spatial HP today? **NO.**

Verdict: **absent at three independent layers.** The energy twin exists and is elaborate; the HP
twin was never built.

### 1.1 The comparison case: energy regen DOES tick, and it is the whole loop

`spatial_gauntlet/spatial_engine.py:5013-5057` — inside the per-tick `for e in all_entities` block
titled `--- Tick cooldowns and energy ---`:

- `:1084` — `energy_regen: float  # per second` is a declared `SpatialEntity` field.
- `:5022-5024` — E2 ramping: `_regen = e.energy_regen * (1.0 + e.ramp_per_s * elapsed)`.
- `:5030` — aura benefit round: `_regen *= (1.0 + get_buff_percent("buff_mana_regen"))`.
- `:5037-5056` — Wave-B RS reservation cap: `_regen_cap = rs_effective_regen_cap(...)`.
- `:5057` — **the write**: `e.energy = min(_regen_cap, e.energy + _regen * self._tick_size)`.
- `:5116-5127` — telemetry twin: `FightEvent(event_type="resource_recovered",
  recovery_source="passive_regen")`.

There is no `hp_regen` / `health_regen` / `life_regen` field on `SpatialEntity` (`:1058-1200` field
block) and no `e.hp = min(e.max_hp, e.hp + ...)` anywhere in the tick loop. The HP side is simply
absent from the same loop — not disabled, not gated, **not present**.

### 1.2 Every HP-increment site in the spatial engine (exhaustive)

`grep -nE "\.hp \+=|\.hp = min\(" spatial_engine.py` returns exactly two:

- `:4508` — `self.player.hp = min(self.player.max_hp, self.player.hp + heal)` where
  `heal = skill.get("damage_multiplier", 0.5) * 200.0`. This is **cast-gated**, not passive: it
  fires only when the selector picks a skill whose geometry is `"self"` or `"none"` (`:4506`).
- `:4659` — the mob twin, same shape, `* 100.0`.

Both are discrete action events consuming an action slot and a cooldown. Neither is a per-tick term.

### 1.3 The one native passive-regen mechanism that EXISTS — and why it cannot reach spatial HP

A passive HP-regen stat does exist upstream, and it is dead on arrival on this path. Three
independent breaks, any one of which is sufficient:

**Producer** — `generation/defensive_allocator.py:147,188` emits
`regen_per_sec = total_regen / duration_s` on the `defensive_objective` block.

**Kernel consumer** — `simulation/combatant.py:911-916`:
```
_regen_per_sec = float(_do.get("regen_per_sec", 0.0))
if _regen_per_sec > 0.0:
    _defensive_seed_effects.append(ActiveEffect(
        name="heal_over_time", params={"tick_heal": _regen_per_sec}, duration_remaining=9_999.0,
    ))
```
So the engine's native passive HP regen is *implemented as a heal_over_time ActiveEffect* — it is
the same mechanism I ruled on in BQ-4, not a distinct stat.

**BREAK 1 — the spatial player never gets the seed.** That code lives in the full
`build_combatant` / `from_player_class` path. The spatial player is built by
`spatial_resolver_adapter.combatant_projection_from_class_dict` (`:225-260`), which constructs
`CombatantState(...)` directly from `stat_distribution` and never touches `defensive_objective`. No
seed effect is ever appended. (Corroborating negative: `entity_from_class_dict` refuses a
`player_class` object when the calibration door is open — `spatial_engine.py:5590-5599` — the door
is projection-path-only by construction.)

**BREAK 2 — the heal arithmetic self-nulls on the projection.**
`spatial_resolver_adapter.py:233` sets `hp=1.0, max_hp=1.0  # scratch; spatial HP is authoritative`.
The tick site re-syncs *only hp*: `spatial_engine.py:5149` —
`e.combatant_state.hp = max(e.hp, 1.0)`. **`max_hp` is never re-synced.** So in
`effect_resolver.py:123` — `actual_heal = min(tick_heal, combatant.max_hp - combatant.hp)` — the
term is `1.0 - max(e.hp, 1.0) <= 0.0`. The heal is non-positive by construction.

**BREAK 3 — the bridge only carries damage.** `spatial_engine.py:5150-5185`: the loop calls
`_dot = _tick_effects(...)` and bridges back with `e.hp -= _dot` (`:5185`). The `heal_over_time`
branch mutates `combatant.hp` (scratch, `effect_resolver.py:125`) and increments
`heals_received` / `bc_signals.hot_recovered` (`:126-129`) — and that scratch HP is overwritten by
the next tick's re-sync at `:5149`. **Nothing returns the heal.** This is the same finding as BQ-4,
now confirmed to cover the *passive* regen mechanism as well as the proc one.

Net: the mechanism exists in the kernel, is measured by `bc_measurement`, and is **structurally
unreachable from the spatial regime**. `scripts/gamora_step3_lived_calibration_sweep_2026_07_07.py:288`
is a standing artifact of the same gap — an H3 discriminator that probes
`("hp_regen", "health_regen", "regen_per_second", "regen")` on a boss `CombatantState` and finds
none of them.

---

## Q2 — Minimal gated build, if we wanted a pinned flat HP/s through the BQ-3 door

**ESTIMATE ONLY. Not implemented. Not proposed.**

Shape: one new `_calibration_overrides` sub-key, `hp_regen_per_s: float` (flat, per second, pinned;
no shape, no ramp, no buff interaction), consumed at one write site inside the existing tick loop.

### Files and sizes

| File | Change | Est. |
|---|---|---|
| `spatial_gauntlet/calibration_overrides.py` | add `"hp_regen_per_s"` to `ENTITY_OVERRIDE_FIELDS` (`:118`) + `_SCALAR_DOMAIN` entry `(0.0, None)` (`:132-141`) + docstring amendment | ~8 lines |
| `spatial_gauntlet/spatial_engine.py` | `SpatialEntity` field `hp_regen_per_s: float = 0.0` in the defaulted-keyword block (`~:1105`) | 1 line + comment |
| `spatial_gauntlet/spatial_engine.py` | consume in `entity_from_class_dict` alongside the `max_hp` override (`:5604-5605`) and pass to the constructor (`~:5800`) | ~4 lines |
| `spatial_gauntlet/spatial_engine.py` | the write, inside the existing `--- Tick cooldowns and energy ---` loop, immediately after `:5057`: `if e.hp_regen_per_s > 0.0: e.hp = min(e.max_hp, e.hp + e.hp_regen_per_s * self._tick_size)` | ~3 lines |
| `tests/test_bq3_calibration_override_door.py` | domain-rejection cases, L3 crash case, C4 byte-identity case, one tick-arithmetic case | ~60 lines |
| `simulation/math/<name>.md` | Discipline #1 note (must precede code) | new |
| `simulation/MIGRATION.md` | `calibration_override_fields` gains a member — star-lord's stamp consumer | ~15 lines |

**Total production-code delta: ~16 lines across 2 files.** The door already carries the six
containment layers; a new sub-key inherits all of them for free (L1 namespace, L2 keyword opt-in,
L3 crash-on-leak, L4 boundary asserts, L5 static test, L6 output stamp).

### Discipline #12 risk surface — three named items

1. **The C4 corner is byte-identical, the semantic is not.** `hp_regen_per_s = 0.0` makes the branch
   a no-op, so production is bit-preserved. But the invariant *"player HP is monotone non-increasing
   between cast events"* — true on every spatial path since the engine existed — is broken inside
   the door. That is the same class of shift BQ-3 already named for `max_hp` (door module docstring),
   and it must be named again, not inherited silently.
2. **It creates a passive-regen mechanism at the WRONG layer.** The engine's real passive regen is a
   `heal_over_time` ActiveEffect (`combatant.py:911-916`) that is broken by BREAK 2/BREAK 3 above.
   Adding a parallel entity-level HP/s term does not fix that; it *routes around* it. When the real
   defensive-mechanics wave lands and fixes the bridge, there will be two passive-regen paths with
   different arithmetic. This is precisely the "lazy substitute for the real mechanism" Matt's
   ratification amendment warned about. It is contained, but it is still a second path.
3. **It would be the first calibration override that ticks.** Every existing override is a
   *construction-time literal replacement*. A per-tick override is live state inside the run loop —
   a different containment posture (L4's boundary asserts still hold, but the blast radius of a
   mis-set value is now duration-scaled rather than one-shot). Also: the L6 stamp currently reports
   fields consumed at build; a tick-consumed field is honestly reported but the stamp's meaning
   widens.

---

## Q3 — The zero-code alternative: fold sustain into pinned `max_hp`

`max_hp' = 1600 + r × T̂`, using the door's existing `max_hp` key. Zero code.

### Precedent: the engine already does exactly this, on purpose

`bc_measurement.py:205` —
```
ehp = f.max_hp + f.shield_buffer_est + f.regen_per_sec_est * ENCOUNTER_DURATION_TARGET
```
This is the **static-estimate basis** for Axis-4 eHP: `regen_per_sec_est × 30s` folded into a flat
pool. And `:199-203` show the engine's own opinion of it — when measured `shield_absorbed` and
`hot_recovered` are available for *every* fight, the basis flips to `"measured"` and the estimate is
discarded. The fold-in is the engine's acknowledged **fallback**, not its preferred reading.

### Where the fold-in distorts

Four distortions, in descending severity for this fixture:

1. **Burst ordering (the one that matters here).** EHP is a bank available at t=0; regen is a bank
   that fills over T. A nova landing at t=3s meets `1600 + r×T̂` under fold-in but only
   `1600 + r×3` under a tick. The player survives a spike they should die to. In this engine that
   is not a rounding difference — it is the *outcome bit*: mob→player damage runs through the typed-
   resistance death channel per hit (`spatial_engine.py:4711-4731`), each hit checking the flip
   independently. Sixteen projectiles resolving in one tick against a pool inflated by the *whole
   fight's* worth of healing is a categorically different survival test.
2. **Overkill absorption.** Fold-in HP absorbs overkill; regen does not heal a corpse. Any damage
   past 0 is wasted under a tick and fully banked under EHP.
3. **Duration feedback.** `T̂` must be *estimated in advance*, but survival changes T. Live longer →
   more real regen → but `T̂` was pinned. The estimate is circular and biased low if the fixture
   comparison is being run *because* survival is in question.
4. **Clear-time contamination.** A larger `max_hp` moves `hp_pct` (`spatial_engine.py:5296`), which
   feeds HP-threshold skill gating (`:4650` region, the LC guard). Pinning `max_hp` changes *when
   defensive skills fire*, not just how long the player lives. A regen tick does not touch that
   ratio's denominator.

### VERDICT

**EHP fold-in is NOT acceptable as the survival model for THIS opposition profile.**

The fixture boss is a 16-projectile cold nova ring plus an 8-second blizzard field — the damage is
concentrated in discrete, high-amplitude packets against a channel that tests death per hit. That is
the maximally adversarial case for the burst-vs-sustain distortion, and distortion (1) is not a
magnitude error, it is an outcome-flip error. A fold-in lap would report "survived" for a build the
tick model kills, and there is no post-hoc correction that recovers the true answer from that run.

**Narrow acceptance, stated precisely:** fold-in is acceptable if and only if the calibration lap's
question is *scalar* — total damage-taken, DPS-in, time-to-first-threshold — and the run is read
with the lethality bit explicitly discarded. It is not acceptable if the lap's question is
survival, clear-time, or TTK.

**Recommendation to the conductor:** if the lap needs the survival bit, do not fold. The honest
options are (a) run the lap without sustain and report the *un*-sustained result as a lower bound
(zero code, zero distortion, honestly labelled), or (b) take the Q2 build with its three named
Discipline-#12 risks accepted in writing. Option (a) requires nothing and lies about nothing.

---

## Reference — file:line index

| Claim | Evidence |
|---|---|
| energy regen ticks | `spatial_engine.py:5057` |
| energy_regen is a declared field | `spatial_engine.py:1084` |
| no HP twin in the tick loop | `spatial_engine.py:5013-5057` (absence) |
| only two HP-increment sites, both cast-gated | `spatial_engine.py:4508`, `:4659` |
| native passive regen is a HoT ActiveEffect | `combatant.py:911-916` |
| producer of `regen_per_sec` | `generation/defensive_allocator.py:147,188` |
| projection never seeds it (BREAK 1) | `spatial_resolver_adapter.py:225-260` |
| scratch `max_hp=1.0`, never re-synced (BREAK 2) | `spatial_resolver_adapter.py:233`, `spatial_engine.py:5149` |
| heal lands on scratch, only DoT bridges (BREAK 3) | `effect_resolver.py:121-129`, `spatial_engine.py:5150-5185` |
| standing artifact of the gap | `scripts/gamora_step3_lived_calibration_sweep_2026_07_07.py:288` |
| EHP fold-in precedent + its demotion to fallback | `bc_measurement.py:199-205` |
| door: entity-side override fields | `calibration_overrides.py:118` |
| door: `max_hp` applied verbatim | `spatial_engine.py:5604-5605` |
| door: projection-path-only by construction | `spatial_engine.py:5590-5599` |
