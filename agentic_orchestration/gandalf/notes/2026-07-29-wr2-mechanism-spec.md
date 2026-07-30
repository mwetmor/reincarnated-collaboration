# WR2 — Mechanism spec: B (combatant collision) + C (movement policy v2)

**Run:** WR2-ENCGEO-2026-07-29 · **Cell:** SPEC · **Author:** gandalf (`SPEC-AUTHOR`, named sub-agent)
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Builder:** gamora (Cells B, C) · **Date:** 2026-07-29
**Authority:** charter §1 (mechanism table), §2 rulings R-WR2-3 / R-WR2-4 / R-WR2-5, §3 gates S-1..S-6
**Class:** spec. No production code in this document. Seams execute.

**Substrate read:** `simulation/spatial_gauntlet/spatial_engine.py` (463 KB kernel),
`spatial_gauntlet/arena.py`, `spatial_gauntlet/policy/{seam,considerations,telegraph_response}.py`,
`gd_nova.py`, `gd_attack_speed.py`, and the WR1-ENV measured record
(`agentic_orchestration/gamora/notes/2026-07-29-wr1-envelope-spec.md`).

---

## §0 — Two corrections the code forced, before either mechanism

Both WR1-ENV findings are right in *consequence* and wrong in *mechanism*. The mechanism is what we
build against, so it gets fixed here first.

### §0.1 The sim DOES resolve combatant collision. Its setpoint is 80% of contact.

`_apply_soft_collision` (spatial_engine.py:2140) is called every tick at :5111. It pushes pairs apart
to a threshold of

```
threshold = SOFT_COLLISION_FRACTION * (a.entity_radius + b.entity_radius)     # :2154
SOFT_COLLISION_FRACTION = 0.8                                                 # :170
```

For player (0.5) + boss (1.5): `0.8 × 2.0 = 1.600`. **The measured 1.600 m flat, over 83,937 ticks,
is not the absence of collision — it is the collision's declared setpoint, reproduced to three
decimals.** The 0.400 m interpenetration is licensed by a constant, not omitted by an oversight.

The distributional shape confirms it. WR1-ENV measured `p5 = p25 = p50 = 1.600` exactly, with spread
only above (`p75 1.652`, `p95 1.986`). An exactly-flat mode is what a **one-sided** push produces:
the push is symmetric (`a += n·p; b -= n·p`, :2158-2161) and then *all* entities are re-clamped
(:2181-2182), so when the player is wall-pinned its half of the correction is annulled and only the
boss moves — landing separation exactly on `threshold`. The flat 1.600 mode and the 75% wall-pin
share are the same fact seen twice.

A second, competing collision law also exists: the boss hard-body block (:2165-2178) enforces only
`d ≥ ENTITY_RADIUS_BOSS = 1.5` — the boss's radius *alone*, not `rᵢ+rⱼ`. It is strictly weaker than
the 1.600 soft threshold and therefore never binds. Two collision laws, both wrong, one dead.
Mechanism B replaces both with one.

### §0.2 The player has NO contact-range movement policy. It is not kiting — it is being bulldozed.

WR1-ENV §HALT describes "a back-off/re-approach melee cadence whose net is a monotone straight-line
drift." **There is no back-off branch in the player's code.** The player's entire movement surface is
one `elif` (:5090):

```
elif d_to_target > min_attack_range and _e4_move_scale > 0.0:   # advance
```

with `min_attack_range = max(2.0, min(attack_ranges))` (:5011). The soft-collision equilibrium is
1.600 m; `1.600 > 2.0` is False; the predicate never fires again after contact. **From first contact
to death the player is motionless.** `MovementIntent.HOLD` (policy/seam.py:122) means, literally,
"stand still."

The drift is the boss's. `melee_aggressive` targets the player's position each tick (:2054); the
symmetric push-apart returns half of the closure; net pair-centroid translation ≈ ½·v_boss·Δt per
tick along the boss's approach bearing. The player is a puck pushed across a table. It never orbits
because a bulldozed puck has no reason to turn, and it stops at (0.5, 0.5) because that is where the
table ends. 179 of 180.

**This makes Mechanism C simpler and its risk different than the charter assumed.** We are not
replacing a policy with a better one; we are supplying a policy where a no-op currently sits.
Nothing has to be un-learned. But everything C does is *new* motion, so C moves outcomes hard, and
§3's S-3 is the gate that matters.

---

## §B — MECHANISM B: combatant body separation

> **R-WR2-3 (settled):** all combatant pairs — player↔mob AND mob↔mob. Dead bodies exempt (carcasses
> don't block; matches Grim Dawn). Deterministic order-stable relaxation. Arena clamp OUTERMOST.

### B-1 Predicate (the thing being built)

At tick close, for every ordered pair (i, j) of **living** combatants:

```
d(i,j) ≥ r_i + r_j − ε_touch
```

`ε_touch = 0.001 m` (1 mm). Gate S-1 allows 1 cm; the solver targets 1 mm so S-1 passes with an
order of magnitude of margin and a marginal FAIL is unambiguously a bug, not a tolerance argument.

**Radius source — unchanged, do not invent one.** `SpatialEntity.entity_radius`, populated at spawn
from the scenario's `SpawnSpec.entity_radius` (arena.py:180; `kitcal_g5_scenarios.py:691`:
`1.5 if a.tier == "boss" else 0.5`; player 0.5 at :709). B reads it and never writes it.
`ENTITY_RADIUS_BOSS`/`ENTITY_RADIUS_STANDARD` (:120-121) survive only as spawn-side defaults; B must
not consult them — a scenario that spawns a 0.9 m elite must separate at 0.9, not at a global.

### B-2 Solver: projected Gauss-Seidel, index-ordered, in-place

Per tick, after the navigation phase and before the nova crossing phase — **the existing call site at
:5111 is correct and does not move.** Replace the *body* of `_apply_soft_collision`; keep one call.

```
for sweep in 0 .. ITER_MAX-1:
    max_residual = 0
    for i in 0 .. n-1:                      # index order over `all_entities`
        for j in i+1 .. n-1:
            skip unless both alive
            n_hat, d  = separation normal + centre distance   (see B-5 for d ≈ 0)
            gap = (r_i + r_j) - d
            if gap <= ε_touch: continue
            w_i, w_j = split(i, j)           # see B-3
            move i by +n_hat · gap · w_i ; move j by −n_hat · gap · w_j
            clamp i ; clamp j                # arena.clamp_entity, INSIDE the sweep
            max_residual = max(max_residual, gap)
    if max_residual <= ε_touch: break
final: clamp all entities                    # outermost, unconditional
```

Three properties this shape buys, and each is load-bearing:

- **Clamp inside the sweep** is how the corner conflict resolves itself. A wall-pinned body absorbs
  none of its share; the residual survives into the next sweep and the *free* body takes it. Within
  two or three sweeps the free body has absorbed 100%. No special-case corner code, no "who wins"
  branch — the iteration is the answer. (This is exactly what the current one-sided push does
  accidentally at :2181; B does it on purpose and to convergence.)
- **`break` on a clean sweep** makes the common case (nobody overlapping) cost exactly one sweep —
  the same cost as today.
- **Gauss-Seidel, not Jacobi.** Corrections apply immediately, so a three-body pile converges in
  sweeps rather than oscillating. Determinism comes from the *ordering being fixed*, not from
  order-independence — the same trade every sequential-impulse solver in the industry makes (Box2D,
  and the reason Havok ships a "determinism" build mode that pins body order). Jacobi's
  order-independence is a real property we are declining; see determinism §D-2 for what we owe in
  exchange.

**`ITER_MAX = 8`.** Contact graphs here are ≤ ~12 bodies and sparse. If 8 sweeps do not converge, the
tick is genuinely over-constrained; see B-6.

> **⚠ ERRATUM (R-WR2-16, 2026-07-29, Cell B S-1 FAIL 321/450):** the pseudocode above does NOT
> implement the redistribution the first bullet below promises. With the player wall-pinned and
> area-weighted split, the clamped body's 0.90 share is annulled each pass and the gap decays as
> `0.90^m` — `0.9^8 = 0.43` of the overlap survives every tick (measured worst slack −0.252 m;
> the recurrence's fixed point reproduces the scenario's boss speed exactly). **The prose is the
> mechanism; the pseudocode was its defective transcription.** Corrected law: **clamp-aware
> shortfall transfer** — within the pass, measure each body's REALIZED post-clamp displacement;
> any annulled magnitude transfers to the pair partner in the same pass (same index order, same
> determinism contract). `ITER_MAX` stays 8 (raising it was and remains drift, §E). S-1 unchanged.

**Ordering:** the index order of `all_entities = [self.player] + self.mobs + self._positioned_allies`
(:4569), constructed once per fight. Dead entities are **skipped in place, never removed** — removal
reindexes and reindexing is a silent determinism break. Do not sort. Do not build a `set` of entities
(see §D-3: `SpatialEntity` is unhashable).

### B-3 The split — who gets moved

`split(i, j)` returns `(w_i, w_j)` with `w_i + w_j = 1`.

**Recommended (OQ-1, lean):** area-weighted, so the bigger body wins the shove.

```
w_i = r_j² / (r_i² + r_j²)          w_j = r_i² / (r_i² + r_j²)
```

Player (0.5) vs boss (1.5): the player takes 0.90 of the correction, the boss 0.10. Equal radii →
50/50, which reproduces today's mob↔mob behaviour exactly.

The genre agrees unanimously and it is worth naming why: in D2 you cannot shove Baal; in PoE
body-blocking is asymmetric by monster size and the whole "you can block a corridor with your own
body but not a Rare's" texture falls out of it; in Grim Dawn a Nemesis walks through your formation
and you walk around it. A boss you can push with your shoulder does not read as a boss. The 1.5 m
radius is already a *statement* about the Primordian's presence; a 50/50 split contradicts the
statement every tick.

> **⚠ Sequencing consequence — B ALONE MAKES S-2 WORSE. This is expected and must not be read as a
> regression at Cell B's Gate-2.** Under today's 50/50 split the bulldozer moves the pair centroid at
> ~½·v_boss; under 90/10 it moves at ~0.9·v_boss. B without C corners the player *faster*. **S-2 is a
> post-C gate.** Cell B's Gate-2 grades S-1 + S-4 + full regression only. (OQ-5.)

### B-4 Dead bodies exempt

Skip the pair if either party is `is_alive == False`. Today's soft loop already does this (:2151);
today's boss-hard block checks only `other.is_alive` and not the boss's (:2172) — a dead boss still
body-blocks. B deletes that block, which deletes the asymmetry.

Carcasses do not block. This is the GD rule and it is the right one for a reason worth stating: a
corpse that blocks converts every big pack-clear into a self-made maze, and the player's punishment
for winning is pathing. D2's corpses are walkable; PoE's are walkable; the one genre memory of
blocking corpses is early-access jank nobody kept.

### B-5 Degenerate + tie handling

- **Coincident bodies (`d < 1e-6`).** Today the guard `d > 0.0001` (:2156) *skips* the correction —
  perfectly-coincident bodies never separate, forever. B must not inherit that. Fallback normal, in
  priority order, all deterministic and RNG-free:
  1. `normalize(spawn_i − spawn_j)` if that is non-zero;
  2. else `(1.0, 0.0)`, with `i` (the lower index) taking `+`.
  Precedent in-file: the fear-flee path's coincident-position fallback is literally `(1.0, 0.0)`
  (:2005-2007, `_WAVED_EPS_FLEE_MIN`). Same law, second consumer.
- **Exact-tie residuals.** No tie-breaking is needed: pair order is total (i<j over fixed indices)
  and every correction is a single in-place add. Do not accumulate corrections in a list and sum them
  — summation order would become a hidden determinism dependency.

### B-6 Non-convergence: fail loud, never silent

If `ITER_MAX` sweeps end with `max_residual > ε_touch`, the arena clamp still fires last (the clamp
is *always* outermost — R-WR2-3), the residual overlap persists for that tick, and the engine
increments a per-fight counter:

```
collision_residual_ticks   : int     # ticks where the solver did not converge
collision_residual_max_m   : float   # worst residual overlap seen, metres
```

Both reported by the Cell-BAT battery. S-1 is then *falsifiable* rather than quietly violated, and if
it fails we know whether it failed by 1 mm or by half a metre. Expected value on this substrate: zero
and zero.

### B-7 Arming

**Mandatory: `body_separation_v2: bool = False`, default OFF.** `SOFT_COLLISION_FRACTION` is consumed
by every scenario in the repo; changing the law globally perturbs the entire banked balance corpus
and Gate-2's full-regression name-diff law fails on contact. Off, the surface is one `if` per tick and
the legacy path is byte-identical. This is the house pattern — `piloted_competence`, `_trace_decisions`,
the GD flags all live this way — and it is not optional here.

WR2's battery runs with it ON. Everything else in the tree runs with it OFF.

---

## §C — MECHANISM C: movement policy v2 (player only)

> **R-WR2-4 (settled):** design to the FIXTURE. The acceptance shape is **orbit-and-reposition melee**
> (Matt's measured play), not ranged kiting. 5.617 stays retired. The preferred-range band derives
> from post-collision contact (≥ 2.0 m combined radii).

### C-0 Where it lives

The BW-1 architecture is *seam decides, engine executes*, and `policy/seam.py` is documented "NO RNG
is consumed here. NO engine state is mutated." Honour it:

- **`MovementIntent` gains `REPOSITION = "reposition"`** (policy/seam.py:27). Precedence, highest
  first: **EVADE ▸ REPOSITION ▸ ADVANCE ▸ HOLD.** `_m3_telegraph_response` already claims the tick by
  returning True (:4211) — that precedence is preserved verbatim. A pilot reading a nova is not
  simultaneously circling. (The enum's own §SS-M12b-4 note already warns that exhaustive matches
  outside the seam are non-exhaustive; add REPOSITION to that warning.)
- `movement_intent()` returns REPOSITION where it would today return HOLD, **iff** the policy is armed
  and the player is alive and `move_scale > 0`. Unarmed → HOLD, byte-identically.

  > **⚠ ERRATUM (SS-C-3, ratified §8.23, 2026-07-29):** post-R-WR2-17 this prose and §C-1's radial
  > rule name DIFFERENT sets — `band_outer` (2.70 vs boss) exceeds `min_attack_range` (2.00), so
  > `d ∈ (2.00, 2.70]` was ADVANCE and becomes REPOSITION. **§C-1 is the operative text**; this
  > clause's literal reading would leave the band measure-zero post-B. Known residual (Gate-2 Cell C
  > WARN-5, name-and-pin): vs standard-radius targets `band_outer` (1.70) < `min_attack_range`
  > (2.00) leaves a HOLD annulus `d ∈ (1.70, 2.00]` — 0.096% of armed ticks; its width moves with
  > TUNABLE `BAND_WIDTH`; any tuning lap touching band parameters must re-measure it.
- The **vector** is computed by a new pure helper in `policy/` — `reposition_vector(...)` — taking
  explicit arguments and returning `(dx, dy, new_orbit_sign)`. No RNG, no mutation, unit-testable in
  isolation. Orbit sign is *engine* state on the player entity, passed in and handed back.
- The engine's player-movement block (:5090) executes it through **the same multiplicative chain
  every other player motion uses** (documented at :5050):
  `step = v · Δt · _e4_move_scale · M(player)`, then `arena.clamp_entity`, then
  `total_displacement += hypot(post-clamp delta)`. A rooted (E4) or hard-CC'd (F8) player **does not
  orbit**. If C bypasses that chain, the control layer leaks and every root in the game is cosmetic.

Scope: **player only.** Mobs keep `_navigate_entity` untouched (R-WR2-4, and it keeps the Cell-C blast
radius one function wide).

### C-1 Preferred-range band — derived from contact, not declared

```
r_contact  = player.entity_radius + target.entity_radius      # 2.0 vs boss, 1.0 vs standard mob
band_inner = r_contact + BAND_PAD_INNER                       # default pad 0.10 m
band_outer = min(band_inner + BAND_WIDTH, min_attack_range)   # default width 0.60 m
```

`min_attack_range` is the existing `max(2.0, min(non-self skill range_m))` (:5011) — read, not
redefined. The band is **per-target and per-tick**, recomputed from the live target's radius; that is
what "per kit class" means operationally, because the kit's `range_m` set and the target's radius are
the only two inputs that vary. No new per-class table. No 5.617.

Radial rule: `d < band_inner` → push out; `d > band_outer` → that *is* ADVANCE, which already exists;
inside the band → radial term zero, tangential term owns the tick.

> **⚠ C-1 carries the run's sharpest risk. Read OQ-2 before building.** Against the boss,
> `r_contact = 2.0` and `min_attack_range = 2.0`, so `band_outer` collapses onto `band_inner` and the
> band degenerates. Worse: the skill-range test at :2336 is `nearest_dist <= range_m`, **centre-to-
> centre**, so once B holds separation at `2.0 + ε` a 2.0 m melee skill is **out of range on every
> tick**. Player DPS against the boss goes to zero and S-3 fails outright. This is not a tuning
> problem; it is a units problem, and it is OQ-2.

### C-2 Tangential (orbit) term

```
n̂ = unit(player − target)          t̂ = (−n̂.y, n̂.x) · s          s ∈ {+1, −1}
v_tan = ORBIT_SPEED_FRAC · movement_speed          # default 0.60
```

60% of run speed, not 100%: a fighter circling a boss at a full sprint reads as panic. D2's
Barbarian-vs-Duriel dance, which is the closest ancestor of the shape Matt actually played, is a
sidestep cadence at well under travel speed.

**Sign persistence and flip — deterministic, state-driven, ZERO RNG draws (OQ-4, lean).** `s` persists
on the player entity and flips when **any** of:

1. **Wall rule (the load-bearing one).** The tangent's dot product with the aggregate wall-repulsion
   normal (C-3) is negative — i.e. the orbit is driving the player *into* the boundary band. Flip, and
   the orbit runs *along* the wall and away from the corner instead of into it.
2. **Dwell.** `ORBIT_FLIP_PERIOD_S` (default 4.0 s) elapsed since the last flip.
3. **Target change.** The chosen nav-target identity changed.

Debounced by `ORBIT_FLIP_DEBOUNCE_S` (default 0.8 s) so rule 1 cannot chatter against a wall.

**Specify the cadence in SECONDS, convert to ticks at read time.** `self._tick_size` is 0.1 s
full-fidelity but `REDUCED_TICK_SIZE = 0.5` exists (:119) and the navigation phase already carries a
warning about exactly this (:4888). A flip period expressed in ticks silently becomes a different
policy at reduced tick rate.

Why state-driven over a random flip: a flip that answers the wall *reads as intention* on the replay
Matt is going to watch — the fighter turns because it ran out of room, which is what a player does. A
random flip reads as indecision, which is the D3-era "monster wanders" complaint, and it costs an RNG
stream we would then have to defend at S-4. Zero draws is also zero risk to the before/after diff.

### C-3 Wall repulsion

Per wall face (4 of them), distance from the player's *body surface* to the face:

```
dist_W = player.x − r          dist_E = (arena.width_m − r) − player.x        (y analogous)
p_k    = max(0, WALL_BAND_M − dist_k)                       # penetration into the band
w_k    = (p_k / WALL_BAND_M)²                               # quadratic ease-in
u_wall = Σ_k w_k · inward_normal_k     (normalized if |u_wall| > 1)
v_wall = WALL_PUSH_FRAC · movement_speed                    # default 0.50
```

`WALL_BAND_M` default **3.0 m**.

**Quadratic, not linear, and not inverse-distance.** Quadratic is zero in both value *and slope* at
the band edge, so the player does not visibly bounce off an invisible field — the steering eases in.
Linear has a slope discontinuity you can see in a replay; inverse-distance diverges at the wall and
turns into a teleport at the exact moment the solver is already fighting the clamp.

**The corner falls out for free.** At (0.5, 0.5) two faces contribute, the sum points diagonally
inward, and the player leaves along the diagonal. No corner special case. The SW-corner pin is
answered by a term that never mentions corners.

### C-4 Composition and cap

```
v = v_tan·t̂ + v_wall·û_wall + v_rad·n̂
if |v| > movement_speed: v = unit(v) · movement_speed
step = v · Δt · _e4_move_scale · M(player)        # M = 0 | σ·(1−δ), F8/E4 chain, C-0
position += step ; arena.clamp_entity(...) ; total_displacement += realized
```

### C-5 Heading is NOT the movement bearing

**`heading_rad` keeps facing the target.** The engine already sets it toward the nav target at :5000
and the `line`/`cone` hit kernels are heading-dependent (:906). If REPOSITION overwrites heading with
the orbit tangent, **every line and cone skill fires sideways past the boss** and the player's damage
evaporates for reasons no one will attribute to a movement change. This is the single easiest way to
fail S-3 while believing the mechanism works. Strafe, do not turn.

### C-6 REPOSITION does NOT suppress the attack

Unlike EVADE — which deliberately costs uptime and sets `_m3_evaded_this_tick` (:4295, spec §9.4,
H-M3-c) — orbiting is free. The player attacks while strafing. (OQ-3, lean.)

Genre and gate agree. Every ARPG in the lineage lets you attack from a strafe; and a REPOSITION that
suppressed attacks would zero DPS across the whole contact phase and fail S-3 by construction. EVADE
costs uptime because a dodge *is* a trade; a sidestep is not.

### C-7 Arming

**`movement_policy_v2: bool = False`, default OFF**, same law and same reasons as B-7. **Two flags,
not one** (OQ-8) — Cell B's Gate-2 must be able to prove B in isolation, and the S-3 tuning lap, if it
fires, needs to move C without touching B.

---

## §D — Determinism analysis (S-4: byte-reproducible at fixed seed, twice)

### D-1 New stochastic elements: **none**, under the recommended design

B is fully deterministic (pure geometry). C as specified consumes **zero RNG draws** — the flip is
state-triggered (C-2). No stream position shifts anywhere; the before/after diff at S-6 is therefore
uncontaminated by draw-position drift, which is the failure mode WARN-1 raised against M-12b's
angular offset and which M-4 pre-empted.

**If the conductor overrules OQ-4 and wants a random flip**, it MUST land on a dedicated sub-stream,
per the two standing precedents (`gd_nova.py:254` `nova_substream`, `gd_attack_speed.py:198`
`swing_pause_substream`):

```
ORBIT_STREAM_SALT = 0x4F_52_42_49_54_5F        # b"ORBIT_"
orbit_substream(fight_seed) -> np.random.default_rng(np.random.PCG64(fight_seed ^ ORBIT_STREAM_SALT))
```

Constructed unconditionally (construction consumes nothing) and **drawn from only when armed**, so an
unarmed battery takes no draw at all and every downstream consumer keeps its position. Drawn from
`self._rng` or `self._resolver_rng` instead, it shifts every damage roll downstream of the first flip
and destroys comparability with the WR1 baseline on every tier.

### D-2 Order-dependence in B — the price of Gauss-Seidel

Gauss-Seidel is order-dependent by construction. Determinism holds **iff** the entity ordering is
stable, and that is now a standing invariant, not an implementation detail:

- Order is the index order of `all_entities` (:4569), constructed once per fight.
- **Never sort.** **Never filter-and-reindex** (dead entities are skipped, not removed). **Never
  iterate a `set` or a `dict` keyed on entities.**
- The ordering also introduces a *bias*: the player is index 0 and resolves against every mob first,
  so in a pack it accumulates more correction than any single mob. This is deterministic, and it is
  arguably correct (the player is the one body everything else is converging on), but it should be
  named in the Cell-B math note rather than discovered later.
- Gate-2 ask: a test that runs the solver on a shuffled copy of the entity list and asserts the
  results **differ** — proving the order is load-bearing and therefore that the invariant above is a
  real requirement and not a comment.

### D-3 ⚑ THE RISKIEST HAZARD — `SpatialEntity` is a plain `@dataclass`, so `in` is value-equality

`@dataclass class SpatialEntity` (spatial_engine.py:1096-1097) — no `eq=False`, no `frozen=True`.
Three consequences, all live:

1. **`__eq__` is field-by-field value comparison.** The existing boss-hard block does
   `others = [e for e in entities if e not in bosses]` (:2166). That is not an identity test. It is
   an O(n · fields) value comparison per entity, per tick, and it is semantically wrong the moment two
   entities carry equal field values.
2. **`__hash__` is `None`.** Dataclasses with `eq=True` and no `frozen=True` are **unhashable**.
   `set(entities)` and `{entity: ...}` raise `TypeError`. Any B implementation reaching for a set of
   resolved pairs must use **index tuples `(i, j)`**, never entity objects.
3. **The NaN trap, and this is why it heads the list.** IEEE-754 NaN is not equal to itself, so a
   dataclass carrying a single NaN field is **not equal to itself**. `e not in bosses` would then be
   True for a boss *against its own entry* — the boss would be resolved as both a boss and an "other,"
   double-correcting its position, and it would do so **only on the fights where some float went
   NaN**. Seed-dependent, silent, and it would present as a determinism failure with no local cause.

   > **⚠ ERRATUM (Cell B, 2026-07-29):** this mechanism does NOT reproduce — CPython's
   > `list.__contains__` tests `x is e or x == e`, so an entity always matches its OWN entry by
   > identity before equality runs; NaN cannot make a body miss itself. The consequence stands
   > corrected: the LIVE hazard is item 1 (value-equality false positives between two DISTINCT
   > entities carrying equal fields). The grep sweep and the index-only law are unchanged — and
   > were executed by Cell B (66 compares, 2 entity hits converted, re-sweep clean).

Mechanism B deletes the block that contains this, which removes the instance. It does not remove the
trap. **Gate-2 ask:** grep the spatial seam for `in <list-of-entities>` / `not in <list-of-entities>`
and convert every hit to identity (`any(e is b for b in ...)`) or to index membership. New code in B
and C must use indices exclusively.

### D-4 Floating-point discipline

Every correction is a single in-place add against a Python float. Do **not** accumulate per-entity
corrections into a list and sum at the end — the summation order becomes a hidden determinism
dependency and it will survive every test that runs the entities in construction order. No numpy in
the separation loop; the current code is pure-Python floats and B stays pure-Python floats.

### D-5 Bounded, non-time-based fallback

`ITER_MAX` is a fixed integer. The convergence loop must **never** terminate on elapsed wall-clock,
iteration-count-derived-from-load, or anything else that varies between two runs of the same seed.

### D-6 Tick-size dependence

`ORBIT_FLIP_PERIOD_S` / `ORBIT_FLIP_DEBOUNCE_S` are seconds, converted at read time via
`self._tick_size`. At `REDUCED_TICK_SIZE = 0.5` the derived tick counts must round **deterministically**
— specify `max(1, int(round(period_s / tick_size)))`, one rounding rule, stated once.

### D-7 `total_displacement` semantics shift (report, do not gate)

W-D Axis-1 mobility accrues realized post-clamp motion at :5101 and :4291. C adds a third accrual
site and, more importantly, **an orbiting player accrues an order of magnitude more displacement than
a motionless one.** Any consumer thresholding on `total_displacement` changes meaning under the flag.
This belongs in the S-6 before/after diff table as a named line item, not as a surprise.

---

## §E — Tunable parameter table

**S-3's pre-authorized tuning lap may move the TUNABLE rows only. Mechanisms are frozen.**

| Parameter | Default | Mech | Tunable in the S-3 lap? |
|---|---|---|---|
| `ORBIT_SPEED_FRAC` | 0.60 | C | **YES** |
| `WALL_BAND_M` | 3.0 m | C | **YES** |
| `WALL_PUSH_FRAC` | 0.50 | C | **YES** |
| `BAND_PAD_INNER` | 0.10 m | C | **YES** |
| `BAND_WIDTH` | 0.60 m | C | **YES** |
| `ORBIT_FLIP_PERIOD_S` | 4.0 s | C | **YES** |
| `ORBIT_FLIP_DEBOUNCE_S` | 0.8 s | C | **YES** |
| `RADIAL_SPEED_FRAC` | 0.50 | C | **YES** |
| separation predicate `d ≥ rᵢ+rⱼ` | — | B | **NO** — the mechanism |
| split law (area-weighted) | r² | B | **NO** — a ruling (OQ-1), not a dial |
| solver type + iteration order | GS, index | B | **NO** — determinism contract |
| dead-exempt | on | B | **NO** — R-WR2-3 |
| clamp-outermost | on | B | **NO** — R-WR2-3 |
| `ε_touch` | 0.001 m | B | **NO** — correctness, and it sets S-1's margin |
| `ITER_MAX` | 8 | B | **NO** — raising it to pass S-1 is drift, not tuning |
| heading-faces-target | on | C | **NO** — C-5; a dial here is a damage bug |
| REPOSITION does not suppress attack | on | C | **NO** — C-6 |
| flip trigger set (wall / dwell / target) | — | C | **NO** — the mechanism; the *periods* are the dials |
| both flags' defaults (OFF) | False | B, C | **NO** |
| radius source (`entity_radius`) | — | B | **NO** — B never writes radii |

The wall between the two halves is the one that matters: **feel is tunable; geometry, precedence, and
determinism are not.** A lap that reaches for `ITER_MAX` or `ε_touch` to make S-1 green has stopped
tuning and started moving the goalposts, and the run's pre-registration exists to catch exactly that.

---

## §F — Open questions for the conductor

Eight. Ranked by weight. Each carries my lean; none is ruled here.

**OQ-1 — the split law.** Area-weighted (r²) vs symmetric 50/50 for the correction share.
**Lean: area-weighted.** Genre-unanimous (D2 Baal, PoE size-asymmetric body-blocking, GD Nemesis), and
it degenerates to 50/50 for equal radii so mob↔mob is unchanged. Cost: it makes the pre-C bulldozer
faster (see B-3's sequencing warning).

**OQ-2 — attack range: centre-to-centre or surface-to-surface? THE S-3 RISK.** The skill-range test at
:2336 is `nearest_dist <= range_m`, centre-to-centre. Once B holds separation at `r_contact + ε`, a
2.0 m melee skill vs a 1.5 m-radius boss is **permanently out of range** — player boss DPS → 0, S-3
fails outright, and the pre-authorized tuning lap gets spent on a units bug that no C parameter can
reach. Three readings:
 (a) keep centre-to-centre, raise the `min_attack_range` floor above `r_contact` — a reach change on
 the damage side, arguably outside the charter's B+C scope;
 (b) **measure range surface-to-surface: `effective_range = range_m + target.entity_radius`** — the D2 /
 GD / PoE convention (a bigger monster is easier to reach because its body is nearer), one term,
 gated to the same flag, and it makes bosses feel appropriately huge as a side effect;
 (c) do nothing and accept the player attacking at exactly the contact boundary.
**Lean: (b), flag-gated.** But it moves damage-side outcomes, so it is the conductor's call and not
mine. **If (c) is ruled, expect S-3 FAIL and budget the lap for it.**

**OQ-3 — does REPOSITION suppress the tick's attack, as EVADE does?** **Lean: NO** (C-6). EVADE costs
uptime because a dodge is a trade; a sidestep is not, and a suppressing REPOSITION zeroes contact-phase
DPS and fails S-3 by construction.

**OQ-4 — flip trigger: state-driven or RNG sub-stream?** **Lean: state-driven, zero draws** (C-2). A
wall-answering flip reads as intention; a random flip reads as indecision, and it costs a stream we
would have to defend at S-4. If overruled, D-1 specifies the sub-stream exactly.

**OQ-5 — is S-2 gated at Cell B's Gate-2?** **Lean: NO — S-2 is post-C only.** B alone provably
worsens the corner pin (B-3). Cell B grades S-1 + S-4 + full regression. Confirm before Cell B lands
so a *correct* B is not read as a regression.

**OQ-6 — does the split law apply to mob↔mob too, or only to pairs involving the player?**
**Lean: one law everywhere.** Equal radii make it moot for trash-on-trash; it bites only boss↔add,
where "the boss shoves its own adds aside" is the right read and a second law would be a third physics.

**OQ-7 — does the boss get wall-awareness?** **Lean: NO, out of scope** (R-WR2-4 says player). Noted
because it is the residual risk: a boss that presses a wall-pinned player is no longer *able* to
interpenetrate under B, but nothing stops it re-pinning the player against a wall it is itself pressed
against. C-3's wall-repulsion is the only thing preventing that. **If S-2 fails after C, this is the
first suspect and `WALL_PUSH_FRAC` / `WALL_BAND_M` are the lap's first two dials.**

**OQ-8 — one flag or two?** **Lean: two** (`body_separation_v2`, `movement_policy_v2`). Cell B's
Gate-2 must prove B in isolation, and the tuning lap must move C without disturbing B.

---

## §G — What Cell B and Cell C each owe at Gate-2

**Cell B:** S-1 computed over all 450 fights (`min pairwise separation ≥ rᵢ+rⱼ − 1 cm`, every tick) ·
S-4 twice at fixed seed · `collision_residual_*` counters reported (expect 0, 0) · **full regression
byte-identical with the flag OFF** (the name-diff law; adjacent-suites-green is not the criterion) ·
the shuffled-order test of D-2 · a math note carrying the D-2 ordering invariant and the D-3 grep
sweep. **Not** S-2.

**Cell C:** S-2 (wall-contact share ≤ 5% of player-alive ticks per tier; final-10 s share ≤ 20%) ·
S-3 (no-evasion player still killable at the death-2 band; win still reachable on `pre`; `post` still
won) · S-4 · flag-OFF regression byte-identical · a trajectory reconstruction on
`boss__B__seed74000802` — **the same trace WR1-ENV used to establish drift-not-orbit** — showing the
path now turns. That reconstruction is the cheapest honest answer to "is the fight worth watching,"
and it is available before the render is.

---

*Spec closes. Rulings §2 untouched; eight forks routed up. — gandalf, `SPEC-AUTHOR`*
