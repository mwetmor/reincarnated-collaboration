# G1-A — GD 40-state coverage audit against the battle sim

**Agent:** gamora (simulation seam)
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-gamora-gd-40-state-coverage-audit.md`
**Type:** ANALYSIS / AUDIT — read-only. No production code changed, no engine file edited.
**Date:** 2026-07-25
**Sim revision audited:** `spatial_engine.py` @ 6022 lines (mtime 2026-07-23 01:14), `damage_resolver.py`
(2026-07-23 05:53), `combatant.py` (2026-07-17), `effect_resolver.py` (2026-07-17),
`commitment_state_machine.py` (2026-07-11), `arena.py` (2026-07-22). Working tree at commit `57f1b52d`.

---

## SUMMARY (≤10 lines)

```
CORRECTED HEADLINE COUNTS — 40 states, all classified:
    MODELLED        4   (Attack, Move, Return, Dead)
    PARTIAL         9   (Idle, Pursue, RepositionForAttack, Flee, Sleeping,
                         Immobile, Stunned, TakeHit, GettingUp)
    ABSENT         21
    PROPOSED-OUT    6   (QuestWalk/Move/UseSkill/PlayAnimation, Emote, Patrol)

MOST CONSEQUENTIAL DIVERGENCE from gandalf's provisional triage:
  The hard-CC block — Stunned / Immobile / Paralyze / Trapped / KnockedDown — was triaged
  "plausibly modelled / status-equivalent." It is NOT. EMPIRICALLY VERIFIED (probe, § 6): a mob
  carrying live stun + freeze + root + 90% chill selects its skill and moves its FULL per-tick
  distance. The action-lock exists (combatant.py:459) but sits on a code path with ZERO production
  callers. Fully-modelled count falls 12 → 4. Offsetting upgrade: `Return` (triaged absent) is
  MODELLED and TSF6 already measured it +0.15% parameter-faithful.
```

---

## 1. Method + scope

**What "the battle sim" is.** Every production caller routes to `run_spatial_fight`
(`spatial_engine.py:5676`) — verified: 20 modules import it (`balance_loop`, `gauntlet_sim`,
`t4_sim_cycling`, `kit_compiler`, all harnesses). The abstract 1v1 kernel path
(`ai_strategies.choose_action` → `combatant.available_skills` → `combatant.can_use_skill`) has
**no production caller anywhere in the repo** — repo-wide grep across `src/` and `tests/` returns
only `tests/test_d4_ai_strategies_consumer.py:351`, which injects a mock. Its logic was PORTED into
the spatial selector (`spatial_engine.py:2094` documents the port). This distinction is load-bearing
for six of the forty rows below.

**Classification rule applied** (dispatch § 3): MODELLED requires entry trigger + exit trigger +
parameter binding at a named file:line. A name that exists but drives no transition is not MODELLED.

**Evidence classes used.** `VERIFIED(file:line)` = read the code. `PROBE` = executed read-only
in-memory probe, § 6. `ABSENCE(<terms>)` = exhaustive grep over
`reincarnated-engine/src/reincarnated/` excluding `__pycache__`, terms listed. `INFERENCE` = labelled
explicitly; there are three in this document and they are tagged inline.

---

## 2. The 40-row matrix

| # | GD state | Class | Sim construct (file:line) or absence evidence | Notes |
|---|---|---|---|---|
| 1 | `Idle` | **PARTIAL** | Hold branches: `spatial_engine.py:1769-1779` (stationary_caster/proximity_trigger), `:1796-1808` (ranged_kite hold + re-face), `:1815-1818` (cast_at_range hold), `:1692-1700` (serial pre-activation hold) | Combat-idle (in-range, on-cooldown, holding) EXISTS. Non-combat idle does NOT: without an onset gate (row 4) a mob is never "idle because unaware." Missing half = the unaggroed idle. |
| 2 | `Startup` | **ABSENT** | `spatial_engine.py:1144` `action_available_at: float = 0.0`; `entity_from_monster_dict:5543-5670` constructs the mob live with no init state. ABSENCE(`startup`, `spawn_delay`, `start_delay` — only hit is `ContinuousSpawn.start_delay_s` at `:3652`, a spawner schedule, not a per-monster state) | Mobs are born attacking. Low consequence: GD's Startup is likely a one-frame init too — but that is INFERENCE about GD, not a sim finding. |
| 3 | `Attack` | **MODELLED** | Entry: mob action phase `spatial_engine.py:4336-4353`; selection `_select_skill_for_entity:1931`; cooldown gate `:1969` + `:4352`; range gate `:2011-2014`; resolution `:4374-4553`; exit: cooldown stamp `:4553-4555` | Greedy: first ready skill in rotation-priority order that is in range. No target-commitment, no attack-token. |
| 4 | `Pursue` | **PARTIAL** | Pursuit exists: `spatial_engine.py:1784-1833` (five behavior branches) + move block `:1836-1854`. Onset gate does NOT: `aggro_radius_m` (`:1124`) is stored (`:5587`, `:5659`) and never gate-read in `_navigate_entity` or the action phase | Confirms TSF6 § 3 row 1. Pursuit is from tick 0 at any distance. The only live proximity gate is the R3a serial-activation latch (`:1691-1700`), opt-in per scenario. Missing half = perception/onset. |
| 5 | `RepositionForAttack` | **PARTIAL** | Range-keeping: `spatial_engine.py:1787-1808` (ranged_kite backs off to `preferred_range_m`), `:1810-1818` (cast_at_range approach/hold), `:1820-1830` (hit_and_run at 0.7× preferred) | These are STATELESS per-tick range rules re-evaluated every tick, not a state. Missing: attack-intent binding (reposition *because* I want to attack), blocked-shot / LOS recovery, reposition-then-fire sequencing. There is no LOS test anywhere in the engine — ABSENCE(`line_of_sight`, `LOS`, `raycast` in `spatial_gauntlet/`). |
| 6 | `JumpAttack` | **ABSENT** | `leap_strike` → `"point"` geometry (`spatial_engine.py:777`); `dash_attack`/`defensive_dash`/`blink`/`teleport` → `"none"` (`:780-783`). Exhaustive enumeration of position-mutation sites: `:1678-1679` (nav), `:1759-1760` (fear-flee), `:1852-1853` (nav move), `:1879-1880` + `:1897-1898` (collision push), `:4120-4122` (player move). **No skill drives displacement.** | A leap/dash skill resolves as a nearest-target point hit or a self-cast heal (`:4219-4222`, `:4371-4373`) with zero motion. |
| 7 | `Roam` | **ABSENT** | ABSENCE(`roam`) — 1 hit package-wide, `spatial_engine.py:2990`, an unrelated comment ("the player roams freely after planting") | |
| 8 | `Flee` | **PARTIAL** | Wave-D fear-flee: `spatial_engine.py:1727-1763`. Entry = `fear` ActiveEffect present AND no `taunt`; velocity-away vector at `movement_speed × flee_speed_multiplier ∈ [0.5,1.5]`; composes with curse:decrepify `:1755-1757`. PROBE-confirmed live | Three gaps: (a) no HP-threshold flee — nothing keys on `fleeDistance` or `hp_pct`; (b) no exit trigger other than effect expiry; (c) **a fleeing mob still attacks** — the mob action phase (`:4337-4353`) gates only on `is_leashing`, serial activation, and cooldown. PROBE: feared mob returned skill index 0 while moving −0.6 m away. |
| 9 | `WanderPause` | **ABSENT** | ABSENCE(`wander`, `pause`, `idle_timer`) — all `wander` hits are the unrelated "Wanderer architecture" clustering concept (`phase7_db.py:83`, `phase7_verdict.py:69`) | |
| 10 | `Wander` | **ABSENT** | as row 9. Confirms TSF6 § 3 row 6 | |
| 11 | `Dying` | **ABSENT** | Death is instantaneous: `spatial_engine.py:2309-2312`, `:2338-2341`, `:2927`, `:3502`, `:3954`, `:4506-4508` — every site is `hp <= 0 → hp = 0.0; is_alive = False` in one statement. ABSENCE(`death_anim`, `dying`, `corpse` — only hit is a comment on the A4 kill-token economy at `:2583`) | No death interval, no death-throes window, no interruptible death, no corpse. |
| 12 | `Return` | **MODELLED** | Entry: `spatial_engine.py:1706` (`dist_from_spawn > leash_distance_m` → `is_leashing = True`). Behavior: `:1656-1681` full-speed return to `spawn_pos`. Exit: `d <= 0.5` → `is_leashing = False` (`:1674`), then re-aggro. Parameter binding: `leash_distance_m` (`:1125`), HP-convention branch `:1669-1674` | **Upgrade vs triage** (gandalf placed `Return` in the ~18 not-modelled). TSF6 § 2 measured leash fire at 120.17 m vs K·`MaxPursuitDistance` = 120.0 → **+0.15%**. Distance-keyed only; no `PursuitTime` component. |
| 13 | `FollowLeader` | **ABSENT** | ABSENCE(`leader`, `follow_leader`, `pack_leader`) — every `leader` hit is in `arena.py` and is **spawn-composition text only**: `:491-498` ("leader" + "3 minions tight around the leader"), `:1158`, `:757`. Zero runtime link from a minion entity to a leader entity; `SpatialEntity` carries no leader/pack field (`:909-1246`) | Packs exist as a SPAWN TOPOLOGY (tight clusters). They are not a behavioral hierarchy. |
| 14 | `Dead` | **MODELLED** | `SpatialEntity.is_alive` (`spatial_engine.py:1142`); per-tick alive filter feeding every phase; death event `replica_frame_emitter.py:342 deaths_from_diff` | Terminal, absorbing, no resurrection path in the mob loop. |
| 15 | `NavigateObstacle` | **ABSENT** | `Arena` is an open rectangle with boundary clamp (`arena.py:123-153`). `ChokeZone` (`arena.py:104-120`) clamps x within a y-band and its own docstring says *"models the bottleneck without full pathfinding."* No obstacle set, no navmesh, no re-path, no stuck-detection. ABSENCE(`obstacle`, `navmesh`, `pathfind`, `astar`, `waypoint`) | Loose item L1 in the family rollup. |
| 16 | `DefendLeader` | **ABSENT** | as row 13 | |
| 17 | `Charge` | **ABSENT** | `charge_then_melee` appears at `spatial_engine.py:1784` — and is an **exact alias of `melee_aggressive`** in the same conditional: `if behavior == "melee_aggressive" or behavior == "charge_then_melee":`. Same in the pilot-floor mirror (`commitment_state_machine.py:155`) | **Name collision worth flagging:** in `ai_strategies.py:296` "charge" means *burst-damage-then-melee priority*, i.e. a rotation ordering — NOT a gap-close dash. Nothing in the engine produces a charge displacement (see row 6 enumeration). |
| 18 | `Move` | **MODELLED** | `spatial_engine.py:1836-1854` (target-delta → `movement_speed × dt` step → heading update) + arena clamp `:1857` + soft-collision resolve `:1860-1902` | Parameter binding: `movement_speed`; live modifier: curse:decrepify only (`:1846-1850`). |
| 19 | `Panic` | **ABSENT** | ABSENCE(`panic`) — 0 hits package-wide | |
| 20 | `DodgeAttack` | **ABSENT** | `dodge_chance` is a per-hit probabilistic avoidance roll: `damage_resolver.py:1029` `did_hit(accuracy, defender.dodge_chance, rng.random())`. It consumes RNG, produces an `on_dodge` event (`:1030`), and moves nothing | The sim has "dodge" as a stat, not as a **movement reaction to a specific incoming attack**. Physical-damage only (`:1078`: elemental hits have no dodge gate). This is a *semantic* mismatch, not a naming coincidence — do not count it as coverage. |
| 21 | `Confused` | **ABSENT** | ABSENCE(`confus`) — 3 hits, all the English word in docstrings (`gauntlet_modes.py:27` "Callers cannot confuse the two modes") | |
| 22 | `Paralyze` | **ABSENT** | ABSENCE(`paraly`) — 0 hits package-wide. Not in the ailment registry (see row 26) | |
| 23 | `Trapped` | **ABSENT** | ABSENCE(`trapped`) — 0 hits; `trap` hits are all "smuggling-trap-clean" / "trapped in a local minimum" prose | |
| 24 | `Immobile` | **PARTIAL** | `root` IS in the live ailment registry (`damage_resolver.py:62` → `{bleed, blind, burn, chill, consecrate, curse, drain, execute, fear, freeze, knockback, poison, root, shock, stun, sunder}`); `CombatantState.is_rooted` at `combatant.py:395`. **Zero consumers**: repo-wide grep for `is_rooted` returns only its own definition | PROBE: a mob with a live `root` effect moved the full 0.5 m in a 0.1 s tick. The only movement modifier with a live consumer is curse:decrepify (`spatial_engine.py:1846-1850`) — and `_compute_curse_decrepify_movement_reduction`'s own docstring says *"NOT additive with chill/root"*, i.e. chill/root were expected to have their own consumers. They do not. `slow_factor` (`combatant.py:418`, chill) is likewise unconsumed — PROBE: 90% chill, full-speed movement. Missing half = the effect. Application is complete. |
| 25 | `KnockedDown` | **ABSENT** | `knockback` is a registry NAME with zero code consumers — repo-wide grep for `knockback` returns exactly one hit, `damage_resolver.py:41`, a comment describing the pre-registry hardcoded frozenset | No displacement (row 6), no downed state, no getup. |
| 26 | `Stunned` | **PARTIAL** | Application side is COMPLETE: `stun` ActiveEffect; diminishing-returns immunity stamp `effect_resolver.py:158-164`; boss resist tier `damage_resolver.py:1645-1651`; re-application block `damage_resolver.py:1604-1607`; `is_stunned` `combatant.py:408`; action-lock `combatant.py:459` (`if self.is_frozen or self.is_stunned: return False`) | **The action-lock is on a dead path.** `can_use_skill` ← `available_skills` ← `ai_strategies._common/_scripted/_random` ← `choose_action` — and `choose_action` has no production caller (§ 1). The live selector `_select_skill_for_entity` (`spatial_engine.py:1931-2051`) never consults `combatant_state.active_effects`; the mob action phase (`:4337-4353`) gates on `is_leashing` / serial activation / `action_available_at` only. PROBE: stunned mob returned skill index 0. Same verdict for `freeze` (`combatant.py:403`) and `silence` (`:399`). Missing half = the lock. |
| 27 | `Scared` | **ABSENT** | ABSENCE(`scared`) — 0 hits package-wide | |
| 28 | `Sleeping` | **PARTIAL** | R3a D2 serial-activation gate: `spatial_engine.py:1691-1700` — a mob with `serial_activation_radius_m` set HOLDS at spawn (faces target, does not pursue) and does not attack (`:4344-4351`), until the player crosses the radius, then LATCHES `is_activated=True` permanently | **Family reassignment vs triage** (gandalf put `Sleeping` in the non-combat bucket). Dormant-until-proximity is exactly what this gate does, and it is a real combat mechanism. Missing halves: no wake-on-damage, no wake-on-noise, no re-sleep, and it is opt-in per scenario (`serial_engagement=True`, `:5710`) rather than a per-monster property. |
| 29 | `WaitToAttack` | **ABSENT** | No attack-token, slot, or queue system. ABSENCE(`attack_slot`, `melee_slot`, `attack_token`, `wait_to_attack`, `engagement_slot`). Selector is greedy first-ready-in-rotation-priority (`spatial_engine.py:2016-2021`); every mob in range attacks every cooldown | The only crowd-spacing primitive is post-hoc boid push-apart (`:1860-1902`) plus the boss hard-collision body (`:1884-1898`). Neither is an attack-turn discipline. |
| 30 | `Patrol` | **PROPOSED-OUT** | ABSENCE(`patrol`) — 0 hits. No path/waypoint concept in `arena.py` (`SpawnSpec` `:160` carries a single x/y) | Marked, not ruled (dispatch § 3). Note: GD's `Patrol Points` string sits *outside* Table 3's upper boundary per the research doc's boundary section — a level-design construct. Scope is Matt's. |
| 31 | `QuestWalk` | **PROPOSED-OUT** | ABSENCE(`quest`) — 0 hits in `simulation/` or `spirit_guide/` | |
| 32 | `QuestMove` | **PROPOSED-OUT** | as row 31 | |
| 33 | `QuestUseSkill` | **PROPOSED-OUT** | as row 31 | |
| 34 | `QuestPlayAnimation` | **PROPOSED-OUT** | as row 31 | |
| 35 | `TakeHit` | **PARTIAL** | Player-side ONLY: channel forced-break — `spatial_engine.py:3184-3190` calls `csm.forced_break_triggered` (`commitment_state_machine.py:243-247`: Σ incoming over trailing window W ≥ Y% max-HP → break, ramp reset, lockout). Damage ring fed at `spatial_engine.py:4491-4505` | This IS a damage-driven interrupt with entry, exit, and parameter binding — but (a) it applies only to CHANNELS, (b) wind-up is explicitly *"un-interruptible at v1"* (`:3115`), and (c) `p = self.player` (`:3098`) — **mobs have no hit reaction at all**. Missing half = the mob actor. |
| 36 | `GettingUp` | **PARTIAL** | Player-side ONLY: `commit_lockout_until` (`spatial_engine.py:1220`), set on forced break (`:3188`), read as the re-initiate gate (`:3103`), duration from the emitted `forced_break_lockout_s` | A real post-interrupt recovery window, correctly shaped. Player-only, and reachable only via the channel break path. No downed→getup cycle (there is no downed state — row 25). |
| 37 | `UseSkillOnPoint` | **ABSENT** | All AoE is ATTACKER-ORIGIN: `_compute_circle_hits:1293` (`attacker.distance_to(t) <= radius`), `_compute_cone_hits:1297-1317` (attacker pos + attacker heading), `_compute_line_hits:1333-1347` (segment from attacker along heading), `point:1363-1368` (nearest target). The rich geometry `ground_targeted_circle` **collapses to attacker-centered `circle`** at `spatial_engine.py:759` and `kit_compiler.py:53` | The vocabulary exists at generation and is discarded at resolution. Nearest analogue: `_channel_fixed_hits` (`:1408`) tests a FROZEN footprint — but the origin is the caster's own position at channel start (`:3218-3219`), not a chosen point, and it is player-only. |
| 38 | `UseSkillOnAlly` | **ABSENT** (mob-side) | Mob `self`/`none` skills **self-heal only**: `spatial_engine.py:4371-4373` `heal = ...; mob.hp = min(mob.max_hp, mob.hp + heal)`. Mob attack targets are `_enemies_of(mob, ...)` (`:4362-4365`) — a mob can never select an ally as a skill target | Player-side has ally-benefiting auras (`_aura_beneficiaries_in_radius:366`) but those are radius-gated self-centered auras, not an ally-targeted cast. **Monster support behaviour does not exist.** Loose item L2. |
| 39 | `Emote` | **PROPOSED-OUT** | ABSENCE(`emote`) — every hit is a substring of "demote"/"demoted" (`ai_strategies.py:197`, `arena.py:412`) | Cosmetic. |
| 40 | `AlertBeforePursue` | **ABSENT** | Mob-side: no pre-commitment state anywhere in `_navigate_entity` (`:1631-1857`) or the mob action phase (`:4336-4362`). The telegraph that exists is **metadata minted AT fire-time and DOWNSTREAM of damage application** — `_mint_telegraph_spec:1425`, called at `:4527-4551` with `fire_time_s=elapsed`, under a comment block that states *"ADDITIVE METADATA ONLY (§7.2): this is DOWNSTREAM of the HP/damage/cooldown updates above — it does NOT read into them and adds NO avoidance branch"* (`:4528-4530`) | **The engine documents its own inertness.** `TELEGRAPH_WIND_UP_DEFAULTS_S` (`:197-203`) carries per-shape lead times (circle 1.2 s / cone 0.8 / line 0.6 / point 0.5) under the comment at `:195`: *"INERT in the sim (§7.2): consumed ONLY by Godot's dodge window (dispatch 5); moves no sim outcome."* Consumers: `spatial_telemetry.py:151` (schema field) and `replica_frame_emitter.py:376` (export). Zero sim consumers. The player-side wind-up FSM (`:3114-3177`) is a pre-ATTACK beat, not pre-PURSUE, and is `p = self.player`. |

---

## 3. Per-family rollup

gandalf's 7-family clustering covers **17 of the 40 states**. The audit adds two families the
clustering missed and one no-design-work-needed bucket, which accounts for the other 23.

| # | Family | States | MOD | PART | ABS | Verdict |
|---|---|---|---|---|---|---|
| F1 | aggro onset | `Pursue`, `AlertBeforePursue`, **`Sleeping`** (reassigned in) | 0 | 2 | 1 | Pursuit motion exists; **perception does not**. `aggro_radius_m` is a dead field. The one live proximity gate (serial activation) is opt-in and latching. |
| F2 | telegraph / pre-commitment | `AlertBeforePursue` | 0 | 0 | 1 | **Machinery exists on the wrong actor.** A wind-up FSM with cast_time, projection, move-cancel and un-interruptibility is fully built — for the PLAYER (`:3093-3300`). Mob telegraph is export metadata, self-documented INERT. |
| F3 | leash + return | `Return` | **1** | 0 | 0 | **The one green family.** TSF6 +0.15%. Distance-keyed only; the `PursuitTime` OR-branch is still absent. |
| F4 | idle loop | `Roam`, `Wander`, `WanderPause`, **`Idle`**, (`Patrol` → PROPOSED-OUT) | 0 | 1 | 3 | Un-aggroed mobs do not exist as a category, so there is nothing for an idle loop to run in. F4 is downstream of F1. |
| F5 | distress + pack | `FollowLeader`, `DefendLeader` | 0 | 0 | 2 | Packs are spawn geometry only. No leader reference on `SpatialEntity`; no distress broadcast (TSF6 § 3 row 7). |
| F6 | combat spacing | `RepositionForAttack`, `WaitToAttack`, `DodgeAttack`, `JumpAttack`, `Charge` | 0 | 1 | 4 | Range-keeping exists as a stateless rule; turn-taking, gap-close, evasive movement, and attack-intent binding do not. `Charge` and `DodgeAttack` both have same-named sim constructs that mean **different things** — do not count either. |
| F7 | fear granularity | `Flee`, `Panic`, `Scared` | 0 | 1 | 2 | One flee mechanism (fear-marker), three GD states. No HP-trigger. **A fleeing mob still attacks.** |
| **F8** | **hard-CC / status lock** *(NEW — triage had no family for these)* | `Stunned`, `Immobile`, `Paralyze`, `Trapped`, `KnockedDown`, `Confused` | 0 | 2 | 4 | **The largest verified gap, and the one the triage got backwards.** Application-side is mature (registry, DR, boss tiers, refresh rules). Consumption-side does not exist in the live loop. |
| **F9** | **hit reaction + recovery** *(NEW)* | `TakeHit`, `GettingUp`, `Dying` | 0 | 2 | 1 | Interrupt + lockout are built, player-only, channel-only. Mobs never react to being hit. Death is a single statement. |
| — | lifecycle (no design work implied) | `Idle`†, `Startup`, `Attack`, `Move`, `Dead` | **3** | 1† | 1 | `Attack`/`Move`/`Dead` are genuinely modelled. †`Idle` is counted in F4. |
| L1 | loose — pathing recovery | `NavigateObstacle` | 0 | 0 | 1 | Arena has no obstacles to navigate; ChokeZone is an axis clamp by design. |
| L2 | loose — monster support | `UseSkillOnPoint`, `UseSkillOnAlly` | 0 | 0 | 2 | Ground-targeting is discarded at the geometry resolver; ally-targeting is structurally impossible for mobs (`_enemies_of` filter). |
| — | PROPOSED-OUT | `QuestWalk/Move/UseSkill/PlayAnimation`, `Emote`, `Patrol` | — | — | — | Marked, not ruled. Scope is Matt's (G1-B). |

---

## 4. Expanded gap register (5 KPIs → 9 families + 2 loose)

Supersedes and extends `agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md` § 3.
Original KPI rows are preserved as cross-references in the "TSF6 row" column; their measured
verdicts stand unchanged (nothing in this audit contradicts a TSF6 measurement).

| ID | Family | TSF6 row (cross-ref) | GD parameter/state binding | Sim mechanism home | Status | Named delta |
|---|---|---|---|---|---|---|
| **F1** | aggro onset | KPI 1 *(aggro radii)* + KPI 4 *(pursuit time)* | `ViewDistance` 15.0, `InnerViewDistance` 4.0, `PursuitTime` 10000 ms; states `Pursue`, `AlertBeforePursue`, `Sleeping` | `aggro_radius_m` `:1124` (DEAD for onset); R3a serial latch `:1691-1700` (opt-in, one-way) | **BLOCKED-MECHANISM** | Per-tick `dist ≤ aggro_radius_m` onset check with inner/outer zoning; a de-aggro path; a `time_since_aggro > PursuitTime` alternate leash trigger (GD ORs distance ∨ time). |
| **F2** | telegraph / pre-commitment | KPI 2 *(anger rates)* — **reframed** | `SightAngerRate` 3.0 / `InnerSightAngerRate` 12.0 (4× ratio); state `AlertBeforePursue` (RTTI-confirmed `HandleEvent` override) | Player-side commitment FSM `:3093-3300` + `commitment_state_machine.py`; mob-side telegraph is export-only `:1425`, `:197-203` INERT | **BLOCKED-MECHANISM — but cheapest of the nine** | An `anger` scalar accruing at zone-dependent rate to a threshold, and a mob-side `committing` state. **This is a symmetrization, not a green-field build**: the wind-up state machine (entry, cast_time window, resolve-at-completion, cancel, un-interruptibility) already exists and is unit-tested; it is bound to `self.player`. |
| **F3** | leash + return | KPI 3 *(pursuit distance)* | `MaxPursuitDistance` 75.0; state `Return` | `leash_distance_m` `:1125` → `:1706` → `:1656-1681` | **EXISTS + PARAMETER-FAITHFUL** | None for distance. Time-leash rides F1. |
| **F4** | idle loop | KPI 6 *(wander)* | `WanderDistance` 4.0, `RoamDistance`, `MinRoamDistance`, `MaxTimeBeforeRoam`; states `Roam`, `Wander`, `WanderPause`, `Idle` | none | **BLOCKED-MECHANISM (downstream of F1)** | A pre-aggro idle loop with spawn-anchored roam target + dwell timer. Cannot be observed until F1 gives mobs an unaggroed state to be in. |
| **F5** | distress + pack | KPI 7 *(distress-call)* | `distressCallRange` 16.0, `DistressResponseGroup`, `ChanceToRespondToDistressCall` 75; states `FollowLeader`, `DefendLeader` | none — pack = spawn clustering only (`arena.py:491-498`) | **BLOCKED-MECHANISM** | A leader reference on `SpatialEntity`; a formation-offset nav target; a threat-relay broadcast on aggro/damage. **Note:** the spawn topology already exists, so the data half of pack hierarchy is free. |
| **F6** | combat spacing | *(NEW — not in TSF6)* | states `RepositionForAttack`, `WaitToAttack`, `DodgeAttack`, `JumpAttack`, `Charge` | `preferred_range_m` branches `:1787-1830`; boid push-apart `:1860-1902` | **BLOCKED-MECHANISM** | (a) attack-token/slot budget so surplus mobs hold; (b) skill-driven displacement — currently NO skill moves any entity; (c) attack-intent-bound repositioning. Item (b) is a prerequisite for `JumpAttack` AND `Charge` AND any knockback (F8). |
| **F7** | fear granularity | KPI 5 *(flee)* | `fleeDistance` 16.0, `FleeBehavior`; states `Flee`, `Panic`, `Scared` | Wave-D fear-flee `:1727-1763` | **PARTIAL** | An HP-threshold flee trigger keyed on `fleeDistance`; graded fear tiers; **an action-suppression half — a fleeing mob currently still attacks.** |
| **F8** | **hard-CC / status lock** | *(NEW — not in TSF6, and inverted vs the provisional triage)* | states `Stunned`, `Immobile`, `Paralyze`, `Trapped`, `KnockedDown`, `Confused` | Registry + DR + boss tiers all live (`damage_resolver.py:1604-1651`, `effect_resolver.py:158-164`); `is_stunned`/`is_frozen`/`is_rooted`/`slow_factor` (`combatant.py:395-424`) have **zero live consumers** | **BLOCKED-CONSUMER** *(new status class: the mechanism is built and unwired — distinct from BLOCKED-MECHANISM)* | Read `combatant_state.active_effects` at TWO sites: `_select_skill_for_entity:1931` (action lock) and `_navigate_entity:1836` (movement lock + `slow_factor` composition). Estimated surface: two gates, both alongside gates that already exist for fear/decrepify. **This is the highest coverage-per-line item in the register.** |
| **F9** | **hit reaction + recovery** | *(NEW)* | states `TakeHit`, `GettingUp`, `Dying` | Player channel forced-break `:3184-3190`; `commit_lockout_until` `:1220/:3103/:3188`; death is one statement | **BLOCKED-MECHANISM (mob actor)** | Mob-side hit reaction; wind-up interruptibility (currently v1-locked OFF by design, `:3115`); a death interval if `Dying` is wanted. |
| **L1** | pathing recovery | *(NEW)* | state `NavigateObstacle` | `ChokeZone` x-clamp `arena.py:104-120` ("without full pathfinding") | **BLOCKED-MECHANISM** | Obstacle set + a stuck-detect/re-path state. **Lowest priority — the arenas have nothing to path around; this is arguably a level-design prerequisite, not a sim gap.** |
| **L2** | monster support | *(NEW)* | states `UseSkillOnPoint`, `UseSkillOnAlly` | Ground-targeting collapsed at `:759`; mob targets are `_enemies_of` only `:4362` | **BLOCKED-MECHANISM** | (a) A placement point on the skill packet so `ground_targeted_circle` survives resolution — the generation-side vocabulary already exists and is being discarded; (b) an ally-target branch in the mob action phase. |

**Register summary (11 rows):** 1 EXISTS+PARAMETER-FAITHFUL (F3), 1 PARTIAL (F7), 1 BLOCKED-CONSUMER
(F8), 8 BLOCKED-MECHANISM. Every absence remains EXPECTED given the sim's charter (bounded balance
fights, not open-field AI) — with **one exception that is not expected and should be treated as a
finding rather than a scope statement: F8.** Hard CC is squarely inside the balance charter, the
application half was built deliberately across Wave-C/Wave-D, and the consumption half was never
wired to the live engine.

---

## 5. What the provisional triage missed

Five items, in descending consequence.

**(a) The hard-CC inversion.** The triage's "plausibly modelled / status-equivalent (~12)" bucket
contained `Stunned`, `Immobile`, `Paralyze`, `Trapped`, `KnockedDown`. Verified: `Paralyze` and
`Trapped` do not exist at all; `KnockedDown` is a registry name with zero consumers; `Stunned` and
`Immobile` have complete application machinery whose action/movement lock sits on a code path with
no production caller. Verified by execution (§ 6), not by reading. This single correction accounts
for 5 of the 8 downgrades and is why the modelled count falls 12 → 4.

**(b) `Return` was in the wrong bucket, and it is the sim's best result.** The triage listed
`Return` among the ~18 combat behaviours we appear NOT to model. It is fully modelled AND is the
only GD parameter TSF6 measured as faithful (+0.15%). Worth correcting because it is the existence
proof that the leash family is done — the constraint ladder can stand on it.

**(c) The telegraph is a symmetrization problem, not a build problem.** The hand-off treats
`AlertBeforePursue` as absent (correct) and implicitly as green-field (not correct). A complete
pre-commitment FSM — timed window, target projection over the window, competence-gated initiation,
mid-flight cancel, explicit un-interruptibility ruling, per-tick service — exists at
`spatial_engine.py:3093-3300` + `commitment_state_machine.py`. It is bound to `self.player` at four
sites. That materially changes the cost estimate for F2, which the hand-off § 2.3 ladder prices as a
rung.

**(d) `Sleeping` is a combat state and it has a partial sim home.** The triage placed it in
"non-combat / quest / cosmetic (~7)." Dormant-until-proximity is what the R3a D2 serial-activation
gate does (`:1691-1700`) — hold at spawn, do not pursue, do not attack, latch on player proximity.
Reassigned into F1. This also means the non-combat bucket is 6, not 7.

**(e) Two same-name-different-meaning traps that would inflate any future coverage count.**
`charge_then_melee` is an alias of `melee_aggressive` (`:1784`) and in `ai_strategies.py:296`
"charge" denotes a burst-damage rotation, not a gap-close. `dodge_chance` is a probabilistic
hit-avoidance roll (`damage_resolver.py:1029`), not an evasive movement reaction. Both would read as
coverage to a name-matching audit. Neither is.

**Two structural observations the family clustering did not have room for:**

- **No skill in the engine moves any entity.** Enumerated exhaustively at row 6. This is a single
  shared prerequisite under `JumpAttack`, `Charge`, `KnockedDown`, and any future knockback/pull.
  It is one capability, not four.
- **The 7-family clustering covers 17 of 40 states.** Adding F8 and F9 brings coverage to 26; the
  remaining 14 are the 6 PROPOSED-OUT plus the 8-state lifecycle bucket that needs no design work.
  Stating this so the family list is not mistaken for an exhaustive partition.

---

## 6. The probe (empirical inspection, Discipline #11)

Run to avoid banking § 5(a) as inference. Read-only, in-memory, no engine file touched, nothing
written to the engine repo. Script: `/tmp/gamora_cc_probe.py` (transient; reproduce from this spec).

Construction: one `melee_aggressive` mob (`movement_speed` 5.0, one `point` skill, `range_m` 20.0,
cooldown 1.0, cooldown counter at 0.0, `leash_distance_m` 1000.0 so leash cannot confound) at
(10,10); one player at (15,10). Per arm, a `CombatantState` carrying the named live `ActiveEffect`s
(`duration_remaining` 5.0) is attached as `mob.combatant_state`. Each arm calls
`_select_skill_for_entity(mob, [player], elapsed=1.0)` and then `_navigate_entity(mob, player, arena,
dt=0.1)`, measuring displacement.

| Arm | `is_stunned` | `is_frozen` | `is_rooted` | `slow_factor` | action → | displacement / 0.1 s |
|---|---|---|---|---|---|---|
| clean (control) | F | F | F | 1.00 | **0** | **0.5000 m** |
| stun | **T** | F | F | 1.00 | **0** | **0.5000 m** |
| freeze | F | **T** | F | 1.00 | **0** | **0.5000 m** |
| root | F | F | **T** | 1.00 | **0** | **0.5000 m** |
| chill+root+stun+freeze | **T** | **T** | **T** | **0.10** | **0** | **0.5000 m** |

Expected under GD semantics: action `None`, displacement 0.0000 for every non-clean arm.

**Positive controls** (proving the probe discriminates, i.e. the null result above is a real absence
and not a broken rig):

| Arm | action → | result |
|---|---|---|
| `fear` (flee_speed_multiplier 1.2) | **0** | dx = **−0.6000** m (away from player at x=15) — flee fires |
| `curse:decrepify` (magnitude 0.40) | — | displacement **0.3000** m vs 0.5000 baseline = exactly ×0.60 — reduction fires |

Both controls behave as the code says they should. The two live consumers work; the four inert ones
do not exist on the live path. The `fear` arm additionally confirms row 8's third gap: **the fleeing
mob still selected skill index 0.**

---

## 7. Provenance ledger

**VERIFIED (read the code, file:line cited in the matrix):** rows 1–40 sim-side constructs; the
dead-path finding in § 1; the telegraph inertness at `:195` and `:4528-4530` (the engine's own
comments, quoted verbatim).

**PROBE (executed):** rows 8, 24, 26 behavioural claims; § 6 table.

**ABSENCE (exhaustive grep over `reincarnated-engine/src/reincarnated/`, `__pycache__` excluded):**
rows 2, 6, 7, 9, 10, 11, 13, 15, 16, 19, 21, 22, 23, 25, 27, 29, 30–34, 39. Search terms are named
in each row's evidence cell.

**CITED FROM PRIOR RUN (not re-measured here):** the +0.15% leash figure, the `PursuitTime` and
distress-call absences — `agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md` §§ 2–3.
The code those measurements ran against is unchanged (`spatial_engine.py` mtime 2026-07-23 01:14,
predating the 2026-07-24 run).

**INFERENCE — three, labelled:**
1. Row 2: that GD's `Startup` is also a low-consequence one-frame init. INFERENCE about GD's
   behaviour; the research doc does not establish it, and no disassembly was done.
2. § 4 F2/F8: the effort characterisations ("symmetrization, not green-field"; "highest
   coverage-per-line"). INFERENCE from reading the code shape. Not a measurement, not a Gate-1
   design ruling, and explicitly not a scope proposal.
3. Row 20: that GD's `DodgeAttack` is an evasive movement reaction rather than an avoidance roll.
   INFERENCE from the state name's position in the state table (it sits among movement states) —
   the research doc did not disassemble it. If GD's `DodgeAttack` turns out to be a roll, row 20
   should be re-classified PARTIAL.

**Not established here — carried forward, not silently closed:** whether GD's own `Sleeping`,
`Patrol`, and the four `Quest*` states are in-scope (G1-B, Matt's ruling); the transition conditions
for `AlertBeforePursue` (the research doc's own open item #1 — anger threshold and exit event remain
undetermined, so F2's parameter binding cannot be specified from what we have); and whether the sim's
kernel abstract path is *intended* to be dead or is an un-retired legacy surface — that is a
seam-ownership question, not an audit finding, and it is raised here rather than acted on.

---

**Signed:** gamora, 2026-07-25. Findings only — no production code changed, no engine file edited,
no telemetry written.
