# Aware-Fighter BW-1 — Exposure-Map + Utility-Scoring Math Note

**Author:** gamora (seam owner, `simulation/`), 2026-07-22
**Discipline #1 (math-before-code):** this note lands BEFORE any decision-layer code. It fixes the
policy-seam signature, the utility-scoring algebra, the BLIND-≡-legacy proof obligation, the
exposure/influence-map reads, and the AWARE candidate-consideration algebra. Code follows.
**Governing spec:** `agentic_orchestration/gandalf/notes/2026-07-22-aware-fighter-build-charter.md`
(§1 architecture pinned, §2 deliverables). **Equivalence battery** is the wave's hard gate (§2.3).

---

## §0 — Empirical seam recon (Discipline #11; verified at HEAD `f738d44`, one commit past the
W3′ fire-stamp `a3671d4` — the intervening commit added ONLY a decisions-log entry, no
`simulation/` code, so HEAD ≡ stamp for the fight path; proven by the battery BEFORE-leg
cross-check against the recorded W3′ gate-output).

The charter cites `spatial_engine.py:1338` as the target-selection site. **Empirically that line is
NOT the player's target choice** — it is the point-geometry AOE *hit resolver* inside
`_compute_aoe_hits` (`geometry_type == "point"`: which single target a point-skill lands on). The
actual **player target-choice** seam is TWO sites, both `min(..., key=distance_to)`:

1. **Movement-target choice** — `_get_player_primary_target(player, alive_mobs, boss_focus)` at
   `spatial_engine.py:1517`, whose fallback (line 1543) is
   `min(alive_mobs, key=lambda m: player.distance_to(m))`. Called at:
   - `:3515` (fight-start heading init) and
   - `:3840` (per-tick navigation-target pick).
   Boss-focus (line 1540) returns the stored `_boss_focus_entity` reference regardless of distance
   when `win_condition` activates it — a mechanical property, NOT a utility term.
2. **Attack-target choice** — `nearest_target = min(targets, key=lambda t: entity.distance_to(t))`
   at `:1915`, inside `_select_skill_for_entity`, feeding skill selection at `:1995`
   (`_select_player_skill_v2`).

`_select_skill_for_entity` and `_get_player_primary_target` are BOTH called for the player AND for
mobs/allies. **Mob and ally target choice is OUT OF SCOPE (mob AI is excluded, charter §1.5).** The
policy seam is scoped to the PLAYER only; mob/ally paths remain byte-identical.

**Movement intent** — the "approach / hold" decision — lives at `:3832–3930`: nav-target point
defaults to `(nearest.x, nearest.y)` (line 3849) with two orthogonal overrides that are mechanical
properties, NOT utility terms:
- **escape override** (`win_condition == "escape_reached"`, line 3855) → nav target = exit point;
- **gather override** (`_player_gather_primitive` AND area skill AND not boss-focused, line 3863) →
  nav target = pack centroid. **Charter §3 pins `player_gather_primitive` OFF in both configs**, so
  this branch is inert in the battery.
Then the advance/hold decision (line 3912): `if d_to_target > min_attack_range and _e4_move_scale >
0.0: advance` else hold.

**Skill selection** (`_select_player_skill_v2`, `:2036`) is EXCLUDED (charter §2.1). Energy-type
branching untouched. The seam extracts target choice + movement intent ONLY.

---

## §1 — The policy seam (the load-bearing extraction)

### §1.1 What the seam decides
Exactly two player decisions (charter §1.1):
- **D_target**: which mob is the player's primary target (used by BOTH movement nav-target and
  attack-target — they select the SAME entity today via the same `min(distance_to)`).
- **D_move**: the movement intent given the chosen target — {advance toward nav-target-point, hold}.
  (Execution stays the existing steering: `heading_rad` toward nav point + capped step; charter §1.3
  "no pathfinding rewrite".)

### §1.2 Considerations are DATA, not code branches (charter §1.1, §1.4)
A **consideration** is a scored function of `(candidate_target, world_read)` producing a raw score in
a bounded range, combined by a **weight**. A **PolicyConfig** is an ordered list of
`(consideration_name, weight)` pairs. The decision code path is FIXED; swapping the config swaps
behavior. **No dual code paths. No legacy branch behind a flag** (charter §1.4 — THE ablation
property). The legacy hardcoded `min(distance_to)` is REPLACED by the seam running the BLIND config.

### §1.3 Target-choice scoring algebra (utility aggregation)
For each alive candidate mob `c`, the total utility:

    U(c) = Σ_i  w_i · s_i(c, world)

where `s_i ∈ [0, 1]` is consideration `i`'s normalized score (higher = more desirable target) and
`w_i` is its weight. The chosen target is:

    D_target = argmax_c U(c)

**Tie-break (LOAD-BEARING for bit-equality):** the legacy `min(alive_mobs, key=distance_to)` returns
the FIRST element achieving the minimum under Python's `min` stability (first-in-iteration wins
ties). To reproduce this EXACTLY, argmax must resolve ties by **first-in-iteration order over
`alive_mobs`** — i.e. `max(candidates, key=lambda c: U(c))` where `alive_mobs` iteration order is
preserved and Python `max` keeps the FIRST maximum. See §2 for the exact BLIND reduction.

### §1.4 The BLIND consideration set = {distance} (charter §1.4, §2.2)
The single BLIND consideration is `distance`, defined so that argmax U reproduces argmin distance:

    s_distance(c) = -distance(player, c)          # closer ⇒ higher score

with weight `w_distance = 1.0`. Then:

    argmax_c [ 1.0 · (-distance(player, c)) ] = argmin_c distance(player, c)

**Bit-equality obligation (§1.4.1):** `max(alive_mobs, key=lambda c: -player.distance_to(c))` must
select the SAME entity as `min(alive_mobs, key=lambda c: player.distance_to(c))` on every fight tick.
This holds iff the tie-break resolves identically. Python's `min` and `max` both return the FIRST
extremal element for ties. BUT: `min(key=d)` first-min and `max(key=-d)` first-max over the SAME
iteration order select the SAME element **only when the extremum is unique**. On a TIE (two mobs at
identical distance), `min(key=d)` returns the first mob with the min distance; `max(key=-d)` returns
the first mob with the max of `-d` = min `d` = the SAME first mob. **They agree on ties.** Proof:
both scan left-to-right; `min` replaces current-best only on strictly-smaller `d`; `max` replaces
only on strictly-larger `-d` = strictly-smaller `d`. Identical replacement predicate ⇒ identical
selection. **∴ BLIND ≡ legacy at the entity-selection level, tick-for-tick, provably.** The battery
(§4) verifies this empirically on 256 fights with a per-decision trace — the proof is necessary but
the empirical check is the gate (Discipline #11).

**Float-identity caveat (§1.4.2):** `-distance` negation introduces no rounding for the COMPARISON
(negation of an IEEE-754 double is exact). The comparison `-d1 > -d2 ⟺ d1 < d2` is exact for
finite doubles. No epsilon. No tolerance band (charter §2.3 forbids them).

### §1.5 Movement-intent under BLIND (bit-equality)
BLIND movement intent must reproduce `:3849–3930` exactly:
- nav-target-point = chosen-target position `(D_target.x, D_target.y)` (escape/gather overrides stay
  as mechanical pre-checks OUTSIDE the utility layer — they are win_condition / flag driven, not
  consideration-scored; gather is pinned OFF; escape fires only on `escape_reached` scenarios, which
  are NOT in the W3′ 32-cell frame — all cells are `all_mobs_killed`).
- advance/hold: `d_to_target > min_attack_range and _e4_move_scale > 0.0` → advance (unchanged
  arithmetic). The seam RETURNS the intent; the existing code EXECUTES the step (heading + capped
  displacement + clamp + `total_displacement` accrual) byte-identically.

**Design decision (§1.5.1):** the seam is a THIN target-selector + intent-classifier. The escape and
gather overrides remain in the engine loop as pre-utility mechanical gates (they answer "is the
nav-target the exit / the pack centroid instead of a mob?" — a win-condition/flag question, not a
"which mob is most desirable?" question). Folding them into considerations would change their
semantics (Discipline #12) and is NOT required by the charter (charter §2.1 scopes the seam to
target choice + movement intent; the overrides are neither). They are preserved AS-IS. This keeps the
BLIND path byte-identical and the AWARE path free to reason about mob desirability without disturbing
win-condition mechanics.

---

## §2 — BLIND reduction (the exact code the seam runs for {distance})

Given `alive_mobs` (iteration-order-preserved), `player`, `boss_focus`:

    def choose_target_BLIND(player, alive_mobs, boss_focus):
        if boss_focus is not None and boss_focus in alive_mobs:
            return boss_focus                      # mechanical: unchanged (:1540)
        # utility layer with a single {distance} consideration, w=1.0:
        return max(alive_mobs, key=lambda c: -player.distance_to(c))   # ≡ argmin distance (§1.4)

This replaces BOTH `_get_player_primary_target`'s fallback AND `_select_skill_for_entity`'s
`nearest_target` FOR THE PLAYER. The boss-focus limb stays a mechanical pre-check. For mobs/allies,
the legacy `min(distance_to)` (and the taunt-weighted variant `_taunt_weighted_distance`) is
UNTOUCHED — those calls do not route through the player seam.

**Equivalence at both call sites:** at `:1915`, `_select_skill_for_entity` uses `nearest_target` for
(a) `nearest_dist` range-gating and (b) passing to `_select_player_skill_v2`. Under BLIND, the chosen
target IS the nearest (§1.4), so `nearest_dist` and the skill-selection input are identical. The
seam supplies the player's chosen target; the monster/ally branch keeps its own `min`.

---

## §3 — Exposure / influence map (charter §1.2, §2.2)

A **lightweight geometry read** computed from readable mob state per the charter's substrate:
`(x, y, threat_tier, archetype_tag, preferred_behavior)`. **No mob-AI change** (charter §1.5) — this
is a READ over the existing mob list. Per-decision computation is acceptable (charter §1.2); cost
budget ≤ small integer factor of the ~17 ms/fight baseline (charter §1.2, §2.2).

### §3.1 Readable substrate — EMPIRICAL runtime correction (Discipline #11)
The charter §1.2 lists the substrate as `(x, y, threat_tier, archetype_tag, preferred_behavior)`.
**Empirically (verified §0), `threat_tier` and `archetype_tag` are SpawnSpec (spawn-time) fields,
NOT runtime `SpatialEntity` attributes.** The seam reads RUNTIME entities. The runtime read-surface
that IS present on `SpatialEntity` (verified via dataclass introspection):
- `m.x, m.y` — position. PRESENT.
- `m.max_hp` — the runtime THREAT-MAGNITUDE proxy. In the W3′ roster, tier is encoded in HP
  (swarm/magic = 150; elite/boss = 2500 — `build_neutral_mob_dicts`). So `max_hp` is a faithful
  runtime stand-in for `threat_tier` with NO spawn-time plumbing. PRESENT.
- `m.preferred_behavior` — {melee_aggressive/ranged_kite/cast_at_range/stationary_caster/hit_and_run}.
  PRESENT. Serves the `archetype_tag`/behavior role (ranged-vs-melee threat projection).
- `m.aggro_radius_m` — the mob's engagement range (a threat-reach read). PRESENT.
- derived: `player.distance_to(m)`, bearing `atan2(m.y-py, m.x-px)`.

**Decision (§3.1.1):** use the RUNTIME surface (`max_hp` + `preferred_behavior` + `aggro_radius_m`)
as the threat-weight substrate — a within-seam READ of existing runtime state, NO mob-AI change, NO
entity-construction change (charter §1.5). This is the faithful realization of the charter's
"lightweight geometry read from readable mob state" given the empirical runtime surface. If prereg
later wants literal `threat_tier` on the entity, that is a separate additive plumbing task (out of
BW-1 scope); the `max_hp`-proxy is behaviorally equivalent on the gate roster.

### §3.2 Threat weight per mob (the influence scalar)
Each mob contributes an **influence weight** `θ(m)` scaling its geometric contribution to the map.
Magnitude-monotone (bigger HP pool = more threatening), behavior-modulated:

    θ(m) = hp_weight(m.max_hp) · behavior_factor(m.preferred_behavior)

    hp_weight(hp):  a monotone read of the runtime threat-magnitude proxy. Structural default:
                    hp_weight = 1.0 + max(0.0, (m.max_hp - SWARM_HP) / (BOSS_HP - SWARM_HP)) · (K-1)
                    with SWARM_HP=150, BOSS_HP=2500, K=6 → swarm/magic ⇒ ~1.0, boss/elite ⇒ ~6.0.
                    (Reproduces the intended tier_weight swarm→1.0 … boss→6.0 from the runtime HP.)
    behavior_factor: 1.0 for all behaviors at PROPOSAL (ranged_kite/cast_at_range/stationary_caster
                    project threat at distance; melee_aggressive/hit_and_run project on contact —
                    the distinction is CONSUMED by the per-consideration ranged/melee gating in §3.3,
                    not double-counted here). NOTE: hp_weight params + behavior_factor are set at
                    PROPOSAL — the GATE set + weights are pinned at prereg (charter §2.2), NOT here.
                    I propose the COMPUTABLE reads; the conductor+Matt pin which fire and at what weight.

The map is NOT consumed by BLIND (BLIND = {distance} only). It is the substrate the AWARE candidate
considerations (§3.3) read. It is computed ONLY when the active PolicyConfig contains ≥1 consideration
that reads it (lazy — zero cost on the BLIND path, preserving bit-equality AND the ~17 ms baseline).

### §3.3 AWARE candidate considerations (I PROPOSE; prereg PINS — charter §2.2)
Each is a normalized `s_i(c, world) ∈ [0, 1]`, computable from §3.1 with no mob-AI change. These are
CANDIDATES; the GATE set is pinned at prereg by conductor+Matt (charter §2.2). Proposed computable
list (mapping to the charter's candidate families: exposure/incoming-threat density, crossfire/arc
overlap, cluster density, lane/corridor pressure, escape-gradient):

1. **exposure_incoming_threat_density(c)** — the incoming-threat pressure the player is under while
   engaging `c`. Sum of `θ(m)` over mobs within radius `R_threat` of the PLAYER, kernel-weighted by
   proximity: `E = Σ_{m≠c} θ(m) · K(dist(player, m))` with `K(d) = max(0, 1 - d/R_threat)`. Score:
   `s = 1 - normalize(E)` (LOWER incoming density ⇒ MORE desirable — pick targets that don't deepen
   exposure). Charter family: *exposure / incoming-threat density*.

2. **cluster_density(c)** — how many mobs cluster near `c` (AOE-value proxy: killing into a dense
   cluster is efficient). `C = Σ_{m} θ(m) · K(dist(c, m))` over mobs within `R_cluster` of `c`
   (includes c). Score: `s = normalize(C)` (HIGHER cluster ⇒ MORE desirable). Charter family:
   *cluster density*. NOTE: this is target-desirability geometry, NOT the gather MOVEMENT primitive
   (which is pinned OFF and lives outside the seam) — it scores which mob to FIGHT, not where to
   walk. Discipline #12 flag: distinct semantics from `player_gather_primitive`.

3. **crossfire_overlap(c)** — degree to which engaging `c` places the player in the arc/line between
   multiple ranged threats (crossfire). For ranged mobs (`preferred_behavior ∈ {ranged_kite,
   cast_at_range, stationary_caster}`), count pairs whose bearings-to-player straddle the
   player→c axis within an arc tolerance. Score: `s = 1 - normalize(overlap)` (avoid crossfire).
   Charter family: *crossfire / arc overlap*.

4. **lane_pressure(c)** — corridor/lane congestion along the player→c approach axis: sum of `θ(m)`
   for mobs within a lane half-width `L_w` of the segment player→c. Score: `s = 1 -
   normalize(pressure)` (prefer targets on clearer approach lanes). Charter family: *lane/corridor
   pressure*.

5. **escape_gradient(c)** — alignment of engaging `c` with the direction of LOWEST threat density
   (the escape axis). Compute the threat-density gradient ∇E at the player (finite-difference of the
   §3.2 field over the 4 cardinal probes); score `c` by cosine-alignment of (player→c) with the
   NEGATIVE gradient (toward safety). Score: `s = normalize(cos_align)`. Charter family:
   *escape-gradient*.

**Normalization (§3.3.1):** `normalize(x)` is min-max over the candidate set for the current
decision (per-tick, per-decision), mapping to [0,1]; a degenerate all-equal set maps to 0.5
(neutral). This keeps every `s_i` bounded and weight-comparable. Normalization is LOCAL to the
decision (no cross-fight state) — deterministic, no RNG, no memory.

### §3.4 Cost model (charter §1.2, §2.2 — ≤ small integer factor of ~17 ms)
- BLIND: O(N) per target decision (one `distance_to` scan), map NOT computed → cost ≈ legacy
  (bit-identical work). Baseline preserved exactly.
- AWARE (all 5 candidates, worst case): the map + considerations are O(N²) in the worst kernel
  (each candidate sums over N mobs). N ≤ 40 in the W3′ frame ⇒ ≤ 1600 kernel evals per DECISION.
  Decisions fire on player-action ticks + nav ticks, not every micro-step. Budget target: keep
  AWARE per-fight within ≤ ~3–4× the ~17 ms baseline (small integer factor). If a pinned gate set
  exceeds this, that is a prereg-time tuning input (fewer considerations / cheaper kernels / cached
  map per tick), NOT a BW-1 blocker — the battery gates BLIND, not AWARE (charter §2.3). The map is
  computed AT MOST once per decision and MAY be cached per-tick if the pinned set proves hot
  (charter §1.2 "per-tick only if cheap").

**AWARE is NOT gated by the battery** (charter §2.3: the battery proves BLIND ≡ legacy). AWARE
correctness is a prereg/ablation concern (charter §4). BW-1 SHIPS the computable candidate machinery
+ the BLIND-equivalence proof; the GATE consideration set is pinned later.

**§3.4.1 — EMPIRICAL cost measurement (Discipline #11; replaces the §3.4 prediction).** Measured on
a 40-mob 44×44 arena (worst-case N, matching the gate roster), 120s cap, 5-fight mean:
- BLIND: **37.4 ms/fight** (map never built — zero-cost path; baseline preserved bit-for-bit).
- AWARE, ALL 5 candidates (worst-case stress ceiling): **204.6 ms/fight → 5.47× BLIND.**
- AWARE, LEAN {distance + 1 geometry read} (representative of a plausible pinned gate): **54.4 ms
  → 1.46× BLIND** (well within the small-integer-factor budget).
The all-5 stress ceiling EXCEEDS the ~3-4× target — reported honestly, NOT hidden. It is a
prereg-tuning input, NOT a BW-1 blocker (the battery gates BLIND, not AWARE; the gate set won't be
all 5). The dominant cost is the per-candidate O(N²) kernel, not map construction; cheaper mitigations
available to prereg if a rich gate set is pinned: (a) cache the ExposureMap per-tick (charter §1.2),
(b) precompute the θ-weighted density field once per decision and have all considerations read it,
(c) prune to the pinned subset. The LEAN measurement confirms the machinery is viable within budget
for a lean-to-moderate gate set. (Note: the 37.4 ms BLIND here > the charter's cited ~17 ms because
this is a full 40-mob/120s-cap fight, a heavier cell than the ~17 ms reference; the RATIO is the
budget-relevant quantity, and BLIND's ratio to itself is 1.00× — byte-identical, zero added cost.)

---

## §4 — Equivalence battery (charter §2.3 — THE HARD GATE)

### §4.1 Sequencing (charter §2.3 — critical)
(a) **BEFORE any refactor:** rerun the W3′ 256-fight set at HEAD via the LEGACY path; record per
fight the metric triple `(mobs_killed, total_aoe_hits, player_damage_total)` AND a per-decision
trace `(tick, chosen_target_id, movement_intent)`. Cross-check the metric triples against the
recorded W3′ `gate-output.json` (`baseline_fight_records` + `encounter_fight_records`). **If they
DON'T match ⇒ STOP (HEAD drift), report.** (Expectation: they match, since HEAD ≡ stamp for the
fight path — §0.)
(b) **AFTER the refactor:** rerun the same 256 via the policy seam in BLIND config.
(c) **Standard:** bit-equal metric triples per fight AND decision-trace equality. **ANY mismatch =
red-flag STOP + report** — including RNG-stream divergence with provably identical decisions (report
as its OWN class; the conductor rules on the substitute standard). No tolerance bands.

### §4.2 The 256 fights (charter §2.3; reuse the W3′ cell/seed/composition/parity logic)
32 cells × {matched-baseline, encounter} × 4 seeds {20260722, 20260723, 20260724, 20260725}.
Reproduce EXACTLY by importing the W3′ runner's selection→formation→scenario→fight machinery
(`round_robin_draft`, `courts_swap`, `assign_formation`, `make_encounter_scenario`,
`make_matched_baseline_scenario`, `build_neutral_mob_dicts`, `run_one_fight`). Same
`track_proxy_population=False`, `apply_mob_hp_difficulty_multiplier=False`, `damage_modifier=1.0`,
`player_gather_primitive=False` (default). corpus.db md5 `d091881d` READ-ONLY.

### §4.3 Decision-trace mechanism
A per-fight trace hook records, on each player DECISION tick, `(tick_counter, chosen_target_id,
movement_intent ∈ {advance, hold})`. In the BEFORE-leg the legacy code emits it; in the AFTER-leg the
seam emits it. Trace equality = identical (tick, target_id, intent) sequence per fight. Because the
seam is pure-functional over `(player, alive_mobs, boss_focus)` and BLIND ≡ legacy at entity
selection (§1.4), the traces MUST match if the refactor is faithful. The trace is the mechanism that
catches a divergence the metric triple might mask (e.g. a tie-break flip that happens not to change
the kill count on a given seed). **The trace instrument itself must be byte-neutral** — gated off in
production runs; enabled only for the battery. It reads state, never mutates RNG/HP/position.

### §4.4 RNG-stream divergence class (charter §2.3)
If metric triples AND decision traces are identical but the RNG stream diverges (provably identical
decisions, different random draw sequence), that is REPORTED AS ITS OWN CLASS — not a pass, not a
silent fail. The conductor rules on the substitute standard. (Not expected: the seam consumes no RNG;
it is a deterministic argmax over distances. But the charter requires the class be reportable.)

---

## §5 — Damage-intake metric (charter §2.4)

Add player damage-TAKEN to `SpatialFightResult` — precedent: 1D damage-taken accumulation
(`combatant.damage_taken`, `effect_resolver.py:109`, `damage_resolver.py:530`) and the spatial
`player_damage_total = self.player.delivered_damage_dealt` producer pattern (`spatial_engine.py:4883`).

### §5.1 Definition — enemy-inflicted damage only
`player_damage_taken` = cumulative damage the player TOOK FROM ENEMIES over the fight. Scalar per
fight, no time series (charter §2.4). Accumulation sites (verified §0):
- **`:4272`** `self.player.hp -= dmg` — the main mob-attack-on-player site (typed + flat routes).
  This is the enemy-damage-received channel (already emits a `damage_received` FightEvent with
  `damage_taken=dmg` at `:4310`). **INCLUDE.**
- **`:3763`** `self.player.hp -= coverage_dmg` — aura/coverage-pressure damage from mobs.
  Enemy-inflicted. **INCLUDE.**
- **`:4102`** `self.player.hp = max(0.0, self.player.hp - _hp_cost)` — SELF-inflicted LC HP-cost
  payment (the player's own skill cost). **EXCLUDE** — not enemy damage; matches the 1D
  `damage_taken` semantics (received-from-opponent), and folding self-costs in would conflate a
  cost-economy signal with a defensive-exposure signal (Discipline #12).

### §5.2 Implementation — one accumulator, mirror the delivered_damage_dealt pattern
Add `SpatialEntity.damage_taken: float = 0.0` (per-fight accumulator, in the telemetry-accumulator
block ~`:1213`). Increment by `dmg` at `:4272` and by `coverage_dmg` at `:3763`. Read into the
result at construction (`:4842`) as `player_damage_taken=self.player.damage_taken`, exactly mirroring
`player_damage_total=self.player.delivered_damage_dealt`.

### §5.3 Schema additivity (brownfield-safe; NOT a telemetry-schema change)
`SpatialFightResult.player_damage_taken: float = 0.0` — additive field, default 0.0, NOT a required
field (`validate()` does not enforce), INTERNAL-to-seam (the SQLite positional `_INSERT_SQL` does NOT
persist it — same status as `player_damage_total` / `total_displacement`). **No DB migration, no
telemetry-schema change** (charter §3: "no telemetry schema changes beyond the intake field" — and
this field, like its precedents, is a result-dataclass field the writer does not persist positionally,
so it is within-seam and requires no star-lord schema work). The batch runner wiring (charter §2.4):
`run_spatial_fight` already returns the `SpatialFightResult` list in its aggregate dict
(`fight_results`); the field rides that surface with zero runner-signature change.

### §5.4 Bit-equality preservation
The accumulator increment reads `dmg` / `coverage_dmg` AFTER they are computed and applied to
`player.hp` — it adds NO branch before RNG, NO HP mutation, NO position change. The metric-triple
bit-equality of the battery (§4) is UNAFFECTED (the triple is mobs_killed/aoe_hits/damage_dealt —
none read damage_taken). Adding the field is orthogonal to the seam refactor and to the battery
standard.

---

## §6 — Semantic-shift declarations (Discipline #12)

1. **Target selection is REPLACED, not branched.** The legacy hardcoded `min(distance_to)` player
   path is DELETED and replaced by the utility seam running BLIND (charter §1.4 — no legacy branch).
   This is a semantic re-expression: "nearest-first" becomes "argmax of a single {distance}
   consideration". Behavior is PROVEN identical (§1.4 + battery §4). Framed here, not buried.
2. **`cluster_density` consideration ≠ `player_gather_primitive`.** Both touch "mob clustering" but
   have DISTINCT semantics: cluster_density scores which mob to TARGET; gather scores where to WALK.
   Gather is pinned OFF and lives outside the seam. Called out to prevent conflation at prereg.
3. **`player_damage_taken` excludes self-inflicted HP costs** (§5.1). It is enemy-received damage,
   matching the 1D precedent. A future consumer wanting total-HP-lost (incl. self-costs) would need a
   separate field — this one is the defensive-exposure signal, deliberately scoped.

---

## §7 — Out-of-scope guardrails (charter §1.5, §3)

- Mob AI: UNTOUCHED. Mob/ally `min(distance_to)` and `_taunt_weighted_distance` do not route through
  the player seam.
- Formation builders / `arena.py`: UNTOUCHED (homogeneous COMMON-4 stands for lap 1).
- Skill selection (`_select_player_skill_v2`): UNTOUCHED (charter §2.1). Red-flag STOP if seam
  extraction proves impossible without touching it — do NOT widen scope.
- `corpus.db`: READ-ONLY, md5-checked.
- Telemetry schema: only the one intake field, and it is a within-seam result-dataclass field (§5.3).
- `player_gather_primitive`: OFF both configs (charter §3).

## §8 — Build order (code follows this note)
1. Add `SpatialEntity.damage_taken` accumulator + increments + `SpatialFightResult.player_damage_taken`
   + construction wiring (§5) — orthogonal, lowest risk, does not touch the seam.
2. Author the policy-seam module (`policy/` under spatial_gauntlet): PolicyConfig, considerations
   (distance for BLIND; the 5 AWARE candidates), exposure map, `choose_target` + `movement_intent`.
3. Wire the seam into `_get_player_primary_target` (player limb) + `_select_skill_for_entity` (player
   `nearest_target`) + the movement block, BLIND by default. Legacy player `min` DELETED.
4. Decision-trace hook (byte-neutral, gated off in production).
5. BEFORE-leg battery (legacy record) + cross-check vs recorded W3′ gate-output. Smoke slice first
   (Discipline #2): 2 pairs × 1 seed before the full 256.
6. AFTER-leg battery (BLIND) + bit-equality + trace equality. Any mismatch → STOP + report.
7. Unit tests (seam/scoring/map/metric) + battery packaged as a repeatable artifact.
8. Build report.
