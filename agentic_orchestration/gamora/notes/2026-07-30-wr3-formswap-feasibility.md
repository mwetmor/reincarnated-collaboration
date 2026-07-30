# WR3-KITE-COMMIT — in-fight form-swap feasibility (R-WR3-8(c))

**Author:** gamora (simulation seam) · **Date:** 2026-07-30 · **Mode:** READ-ONLY reconnaissance.
**Commissioned by:** gandalf (RUN-CONDUCTOR), charter `2026-07-30-wr3-kite-commit-run-charter.md`
§2 R-WR3-8(c). **Engine HEAD at read:** `54536c30`.
**NO production code written. NO engine edits. NO runs executed.**

---

## VERDICT

> **ABSENT-CHEAP at the engine seam — ABSENT-STRUCTURAL at the fixture substrate.**
>
> No mechanism exists today for a fight actor to change its stat block, HP pool, or kit
> mid-fight. The *engine* seam is cheap: `SpatialEntity` is a plain mutable `@dataclass` and a
> swap verb is a **mid-fight rebind of two bodies** (option **b**), not a new intent type and not
> a precompute unbake. The *substrate* is the blocker, and it is not mine: **the fixture contains
> exactly one compiled kit** (`gd-werewolf-kitcal-1`, the TRANSFORMED form). There is no
> human-form kit to swap TO. Building the verb without that kit gives a swap between a form and
> itself.
>
> **Consequently R-WR3-8(c)'s conditional fires: form-swap stages as K2, not folded into K.**

**One correction the read forces, and it shrinks K2 rather than growing it:** R-WR3-4 already
established `werewolf1.dbr` carries no `characterLife`. The 759 → 1607 step in our battery is a
**GEAR step at the R2/R3 boundary** (`kitcal_g5_scenarios.py:57-66`) — a *between-session*
progression event, not a form event. So the honest K2 is a **kit/stat swap at CONSTANT pool**,
and question 3's HP-carry semantics **do not need to be answered for the referent**. They are
answered below anyway, because the engine's current representation is the thing that would trap a
future pool-changing form.

---

## §1 — Q1: does any mid-fight stat/pool/kit change mechanism exist? **NO.**

### 1.1 The stat block is bound ONCE, at fight start

There is exactly one player-entity construction site:
`spatial_gauntlet/spatial_engine.py:6990` `entity_from_class_dict(...)`, terminating in the single
`SpatialEntity(...)` literal at `:7290-7360`. `run_spatial_fight` calls it once (`:7758`). The
`class_dict` is **never re-read after that call** — grep-verified: no `class_dict` reference inside
`SpatialFightEngine` (`:3104`).

Bound-at-init, from that one call:

| field | site | folded-in at init |
|---|---|---|
| `max_hp`, `hp` | `spatial_engine.py:7098`, `:7308-7309` | `player_pool_from_class_dict` |
| `movement_speed` | `:7311` | `class_dict["movement_speed"]` |
| `skills` | `:7312` | raw list |
| `skill_geometries` | `:7313` (computed `:7102-7104`) | `_determine_geometry_type_with_source` per skill |
| `skill_energy_costs` | `:7316` (computed `:7106`) | Leg-B `cost_scale`/`cost_slope` folded |
| `energy_regen` | `:7319` (computed `:7281-7282`) | E2 `regen_magnitude` folded |
| resolver skills | `:7246` `build_resolver_skills(skills)` | kernel `_ResolverSkill` objects |

### 1.2 Both bodies take the pool, and only `hp` ever crosses back

The player exists as **two bodies** (R-KC1-20): the `SpatialEntity` and the kernel
`CombatantState`. Both take the same pool from the same call —
`spatial_resolver_adapter.py:173-197` (`player_pool_from_class_dict`), consumed at
`spatial_engine.py:7098` and at `spatial_resolver_adapter.py:286` (`hp=_pool, max_hp=_pool`).

The engine re-syncs **`hp` only**, at `spatial_engine.py:6602`:

```python
e.combatant_state.hp = max(e.hp, 1.0)   # re-sync scratch to live HP (parity :295)
```

`max_hp` is **never re-synced anywhere in the tree.** The adapter says so in its own comment
(`spatial_resolver_adapter.py:264-271`: *"`max_hp` is never re-synced"*). **This is the single
sharpest fact for K2**: a swap that writes `entity.max_hp` and forgets
`entity.combatant_state.max_hp` reproduces exactly the two-bodies-three-orders-apart defect
R-KC1-20 was ratified to close.

### 1.3 There IS a read-time modifier layer — it does not cover HP or kit

`combatant.py:486-492` `get_buff_percent(name)` sums `percent` over `ActiveEffect`s. Its entire
vocabulary is three keys (`spatial_engine.py:364-370`):

- `buff_damage` → `damage_resolver.py:969`, `spatial_engine.py:3052`, `:4440`
- `buff_mana_regen` → `combatant.py:537`, `spatial_engine.py:6483`
- `buff_speed` → `spatial_engine.py:3800`

There is **no `buff_max_hp`, no `buff_hp`, no kit-level rider.** `max_hp` is read **RAW** at every
consumer: `spatial_engine.py:2770, 3026, 4049, 4372, 5004, 5819, 5835, 5918, 6009, 6758, 6870`;
`effect_resolver.py:247`; and the four kernel clamps the adapter enumerates
(`damage_resolver.py:1259` lifesteal, `:1203` heal cap, `effect_resolver.py:124` HoT cap,
`:977`/`:141` execute + freeze-shatter fraction).

### 1.4 The only mid-fight HP-level rewrite in the tree is mob-side and unrelated

`spatial_engine.py:1957`, the R2 leash return: `entity.hp = entity.max_hp` (D3 territory-guard
reset, suppressible). It writes `hp`, never `max_hp`, and never fires for the player.

### 1.5 The closest existing "mid-fight state changes an effective stat" precedent

The E4 commitment state machine (`spatial_gauntlet/commitment_state_machine.py`;
`p.commit_state` at `spatial_engine.py:4043-4053`) is the pattern a swap verb would be tempted to
copy. **It is not a rebind.** It produces a per-tick scalar `_e4_move_scale` applied at the
*read site* (`spatial_engine.py:5488, 5695, 4753`), leaving `entity.movement_speed` untouched. It
changes no field on the entity except its own state variables. Nothing in the tree changes a
*stat*.

### 1.6 The intent system is movement-only

`policy/seam.py:27-51` — `MovementIntent` has four members: `ADVANCE`, `HOLD`, `EVADE` (M-3),
`REPOSITION` (WR2 Mechanism C). All four are *"move the body this way this tick"*. The classifier
(`policy/seam.py:151-179`) is a pure function of `(distance, min_attack_range, move_scale,
band_outer)` and returns nothing else. **A form-swap is not a movement decision and must not be
smuggled into this enum** — and the seam's own comments already warn that two prior extensions
made every external exhaustive match non-exhaustive (`policy/seam.py:34-36`, `:46-50`).

### 1.7 No form/stance/shapeshift concept exists anywhere in the seam

Tree-wide grep over `simulation/**/*.py` for `shapeshift|shape_shift|form_swap|form_switch|stance`
returns **zero** hits outside prose. The only occurrence of the *word* "transformed" in the whole
seam is the fixture docstring at `kitcal_g5_scenarios.py:183` — see §4.

---

## §2 — Q2: the smallest honest seam

**Classification: (b) mid-fight stat-block rebind.** Not (a) — a new intent type would put a
non-movement verb into a movement enum. Not (c) — the precomputes are shallow and re-derivable
from the same functions that built them; nothing is baked into an unreachable form.

### 2.1 The minimum honest write set

A swap verb must write **both bodies, atomically, in one function**, or it re-opens R-KC1-20:

| # | what | where it must be written |
|---|---|---|
| 1 | `entity.skills` | `SpatialEntity.skills` (`spatial_engine.py:1144`) |
| 2 | `entity.skill_geometries` + `.skill_geometry_sources` | re-run `_determine_geometry_type_with_source` (`:7102-7104`) |
| 3 | `entity.skill_energy_costs` | re-run `:7106` + Leg-B cost fold |
| 4 | `entity.skill_cooldowns` | **policy decision, not mechanical** — carry or reset (see §2.4) |
| 5 | kernel `combatant_state.skill_states` | re-run `build_resolver_skills` (`:7246`) |
| 6 | `entity.movement_speed` | `:7311` |
| 7 | `entity.max_hp` **and** `combatant_state.max_hp` | `:7309` + adapter `:286` |
| 8 | defence door fields (`armor`, resists, `crit_chance`, `block_chance`) | `combatant_projection_from_class_dict` (`spatial_resolver_adapter.py:199+`) |

The honest shape is a **`rebind_form(entity, class_dict, *, allow_calibration_overrides)` helper
that calls the SAME factory functions `entity_from_class_dict` already calls** — Discipline #24
single-expression, the same argument `player_pool_from_class_dict` exists to make. A swap that
open-codes any of rows 1–8 is a second expression, and the second expression is the defect.

### 2.2 Blast radius — invariants a swap BREAKS, named

These are Discipline #12 semantic shifts, not bug fixes. Each is a comment in the tree that
becomes **false** the moment a swap lands:

1. **`spatial_engine.py:4553-4556` — the nova telegraph escape law.** Verbatim: *"DERIVED AT CAST
   FROM THE CASTER'S TARGET'S KIT SPEED, which is what makes it deterministic and
   **per-fight-constant**."* A form that changes `movement_speed` makes it per-*segment*-constant.
   Rings already in the air keep their fuse (correct, and stated); rings cast after the swap get a
   different one. **This is the S-7 gate's own input** (`replica_frame_emitter.py:179-184`).
2. **`replica_frame_emitter.py:151-173` — the frame HEADER.** `max_hp`, `hp_provenance`, `skills`,
   and (on the Mechanism-D arm) `movement_speed_ms` are emitted **ONCE, at fight start**. The
   per-frame entity block (`:249-262`) carries `hp`, `commit_state`, `energy` — **not** `max_hp`,
   **not** `skills`. After a swap the header is a **lie about the second half of the fight**, and
   every pool-fraction grader joining on it silently divides by the wrong pool. **This is
   R-WR3-8(a)'s requirement** ("all pool-fraction gates computed against the CURRENT form's pool")
   landing as a **schema change**: a replica-frame contract amendment, MIGRATION.md owed, drax's
   Godot renderer and star-lord's consumers both downstream.
3. **`spatial_engine.py:4049` — E4 forced-break threshold** reads `p.max_hp` live. A pool change
   moves the sustained-pressure break point mid-fight.
4. **`spatial_engine.py:6758` — the timeout survival predicate** `hp_pct = hp / max_hp` against
   0.50. Same scalar, different denominator, post-swap.
5. **`spatial_engine.py:3026` — the O-d lifesteal headroom clamp** `max_hp - hp`. A pool-raising
   swap instantly creates leech headroom that was not earned.
6. **Execute / freeze-shatter fractions** (`damage_resolver.py:977`, `effect_resolver.py:141`) —
   woken by R-KC1-20, CORPUS-dormant only. A hand-authored harness dict is outside that corpus,
   and that caveat is already written down (`spatial_engine.py:7036-7039`).

### 2.3 Gates a swap mechanism touches

| gate | touched? | why |
|---|---|---|
| **S-1** (breadth / hits-per-press; `kitcal_g5_harness.py:193, 383, 667`) | **YES** | breadth is per-press, and a swap changes which skills exist. `assert_s1_control_pins` (`:963-1035`) walks the compiled kit and pins geometry to `single_target` under the control — it walks **one** kit. A two-kit fight makes the pin under-determined. |
| **S-2** (weapon-DoT lift; `kitcal_g5_scenarios.py:168`, harness `:281, 1448`) | **YES** | the poison rider is compiled onto `claws`. If the human form lacks claws, the S-2 lever is form-conditional. |
| **S-7** (telegraph escapability; `wr2_cell_bat_2026_07_29.py:32-35, 169-427`) | **YES, hardest** | clause 1 grades `(radius_m - d_onset) / wind_up_s <= NOVA_ESCAPE_FRAC * player_move_speed`, joining `movement_speed_ms` **from the header**. Per §2.2(1)+(2) that join key is per-fight today and would become per-segment. **S-7 does not regress silently — it grades against a stale number.** |
| `assert_static_pins` (`kitcal_g5_harness.py:1236`) | **YES** | pre-fight pins over a scenario set built from ONE `class_dict`. |
| `KIT_VARIANT_AXES` (`kitcal_g5_harness.py:1055`) | **YES** | `(pool) × (dot) × (s1_control)` = 8 variants. There is **no form axis**; the manifest (`freeze_shatter_manifest`, `:1129-1223`) enumerates exactly those 8. |
| `fixture_class_dict` pool guard (`kitcal_g5_scenarios.py:187-191`) | **YES** | raises unless `max_hp ∈ {759.0, 1607.0}`. A swap targeting any third pool is refused by design. |
| BQ-3 containment L1–L6 (`calibration_overrides.py`) | **YES** | `ENTITY_OVERRIDE_FIELDS` (`:140`) = `{max_hp, lifesteal_percent}`. A second pool would need a second door value, or the swap reads a second `class_dict` through the same validated door. The latter is correct; it needs **no new door**. |

### 2.4 The four decisions K2 owes BEFORE code (Discipline #1)

None of these are engine facts. All four must be ruled and written to
`simulation/math/<name>.md` before implementation:

1. **Swap trigger** — what makes the policy swap? (Referent: the player pressed a button on a
   cooldown, at will.)
2. **Swap cost / lockout** — duration, resource, animation lock. If zero, the policy swaps every
   tick and the mechanism is a free stat-max.
3. **Cooldown carry across swap** (row 4 above) — carry, reset, or per-form independent tracks.
   A reset is an exploit; a carry across disjoint skill sets is undefined.
4. **HP carry semantics** — §3. **Moot for the referent** (constant pool), load-bearing the moment
   any form changes the pool.

---

## §3 — Q3: HP-pool semantics on swap. **UNDEFINED today. The engine permits all three.**

`hp` and `max_hp` are two **independent plain floats** on a mutable dataclass
(`spatial_engine.py:1138-1139`, `@dataclass` at `:1119` — not frozen, no `eq=False`). Nothing in
the tree couples them. So a 759 → 1600 swap does whatever the writer writes:

| option | expression | consequence at 400/759 → pool 1600 |
|---|---|---|
| **flat carry** | `max_hp = 1600` only | 400/1600 = 25%. The player is **more fragile** by every fraction gate immediately after swapping *up*. Perverse. |
| **proportional carry** | `hp *= 1600/759` | 843/1600, 52.7% preserved. Preserves *felt* health. Manufactures **443 HP of free healing** in a fixture whose whole A/B design exists because the sim werewolf has **no** in-fight healing (`kitcal_g5_scenarios.py:180-182`, harness `:117`: *"THE A/B ARMS EXIST BECAUSE OF THIS ABSENCE"*). Would silently discharge BQ-4. |
| **full heal** | `hp = max_hp` | The `:1957` leash precedent. Nakedly the strongest; nobody would ratify it. |

**There is no default and no fallback.** Whichever is written IS the semantics, and the writer's
choice is a balance decision, not an implementation detail — which is exactly why R-WR3-8(c) was
routed before the spec freeze.

**Two additional constraints the representation imposes:**

- The domain guard `calibration_overrides.py:161, 226-232` requires `max_hp > 0` strictly (it
  divides at `spatial_engine.py:6758`). A swap must not transit through 0.
- **Both bodies or neither** (§1.2). `hp` re-syncs at `:6602`; `max_hp` does not. Writing only the
  spatial body leaves the kernel's four clamps evaluating against the pre-swap pool for the rest
  of the fight — a *defined answer to the wrong question*, which is the exact phrasing R-KC1-20
  used for the defect it closed (`spatial_resolver_adapter.py:268-271`).

---

## §4 — The static version: how the two legs get their pools today

`kitcal_g5_scenarios.py`:

- `:65-66` — two module constants, both `[MEASURED]`:
  `POOL_R2B = 759.0` (W-c window, canonical) · `POOL_R3 = 1607.0` (R3 comparison arm, G-8-corrected).
- `:57-59` — the provenance, verbatim: *"The 759 -> 1600 gear step lands at the **R2/R3
  boundary**, AFTER W-c"*. **This is a gear-progression event between sessions, not a form event.**
- `:151-160` — `fixture_class_dict(max_hp=..., ...)`, the single kit builder.
- `:187-191` — hard guard: `max_hp` must be `POOL_R2B` or `POOL_R3`; anything else raises.
- `:316-323` — the pool lands in `class_dict["_calibration_overrides"]["max_hp"]`, VERBATIM, with
  no `max(floor, override)`.
- Then `resolve_calibration_overrides` (`calibration_overrides.py:273-330`) validates it, and
  `player_pool_from_class_dict` (`spatial_resolver_adapter.py:173-197`) hands the same float to
  both bodies.

`kitcal_g5_harness.py:1055` — `KIT_VARIANT_AXES = ((POOL_R2B, POOL_R3), (False, True), (False, True))`.
Pool × weapon-DoT × S-1 control. **Eight variants. No form axis.**

**So the two legs are two SEPARATE FIGHTS with two separate `class_dict`s.** They are not two
states of one fight, and nothing in the harness can express "the same fight, later".

### The structural blocker, stated plainly

The fixture carries **one** compiled kit: `KIT_ID = "gd-werewolf-kitcal-1"`
(`kitcal_g5_scenarios.py:69`), `archetype_tag = "berserker_werewolf"` (`:302`), two skills
(`claws`, `charge`, `:313`). That is the **transformed** form. The docstring is explicit that the
human-form content was **deliberately excluded** — `:183`, verbatim:

> Onslaught (set-0, **CANNOT FIRE while transformed** -- kit-spec §1.3, five independent lines).

That line is the proof the form axis has real content consequences (at minimum one skill the
werewolf cannot use) **and** the proof that the human-form kit does not exist in the fixture. A
swap verb built today would swap `gd-werewolf-kitcal-1` for `gd-werewolf-kitcal-1`.

**The owed input is a compiled human-form kit** — a kit-spec/legolas extraction, not an engine
build. Until it lands, K2 can be *specified* but cannot be *validated*.

---

## §5 — Recommendation to the conductor (advisory; the ruling is gandalf's)

1. **Stage K2 separately from K**, per R-WR3-8(c)'s conditional. The engine work is small; the
   *substrate* and the *four decisions* (§2.4) are not, and folding them into K would put an
   unspecified verb inside the mechanism whose gates stage 1 is pre-registering.
2. **R-WR3-8(a) is separable and worth doing FIRST, independent of the verb.** "Pool-fraction
   gates compute against the CURRENT form's pool, never a fixed 759" is *today* satisfiable by
   moving the pool onto the per-frame block instead of the header (§2.2(2)) — a replica-frame
   schema amendment that makes every existing grader form-aware **before** any form exists. It is
   also the thing S-7 needs regardless.
3. **Reconsider whether the referent demands the pool half at all.** Per R-WR3-4 + §4, the
   referent's form-swap changed **kit and stats, not pool**. If K2 is scoped to a constant-pool
   kit/stat swap, §3 evaporates entirely and the mechanism is materially smaller.
4. **Route the human-form kit request to legolas** (kit-spec extraction) before K2's math note.
   Math-before-code cannot be satisfied without knowing what the other form *is*.

---

## §6 — Method + limits (Discipline #11, #10)

- **Read-only.** No files under `reincarnated-engine/` modified. No sim executed. No telemetry
  touched.
- **Evidence:** direct source reads + tree-wide greps over `simulation/**/*.py` at `54536c30`.
  Line numbers are as-of that commit and will drift.
- **Negative claims** (§1.3, §1.7, §1.1 "class_dict never re-read") rest on greps, which are
  exhaustive over the seam I own but not over `foundation/` (rocket) or `export/` (star-lord).
  I claim absence **within `simulation/`**.
- **Not assessed:** whether generation emits any form/transform primitive (rocket's seam — if K2
  needs one, per my scope that routes to knight-rider, not a patch by me).
- **Estimates deliberately withheld.** No hour/day figure is given: the §2.4 decisions dominate
  the cost and none are mine to make.
