# Research: what GD actually does at the Crucible's ambush point (p05)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf (KC2-PLAY, pack cut v3.8 held on this) · **Date:** 2026-10-01
**Posture:** read-only throughout. Pack, oracle and port untouched. § 6 is an in-process wrap of gamora's harness, NOT-A-GRADED-RUN.
**Labels:** **DATAMINED** = read out of GD's shipped bytes (Ed-IV `.arz`, Ed-IV `Game.dll`, Ed-I Lua, Ed-III `.anm` headers). **FOOTAGE** = from the referent recording or plate reads taken from it. **SIM** = measured on our oracle. **INFERRED** = my reasoning, kept apart from the record.
**Binary of record:** `~/Games/vendor/grim-dawn-edition-IV-20260929/Game.dll`, sha256 `e75925d1…8126` (32-bit, 25,100 exports). Lap V-2 decoded an earlier build (`4876d6bd…`). I re-checked that `ProxyAmbush::UpdateSelf` in Ed IV has the same member offsets and control flow (`evidence/`).

---

## Summary

1. **The p05 spawn is not a chance roll, and it is not a dormant or proximity ambush.** Every declared wave (151, 152, 153, 156, 157, 158 and 159) spawns its p05 group with certainty. The group is the full pool roll (Lap V counts, 26.0 bodies over the band), released all at once at +4.000 s. `chanceToRun = 100`, each wave has one proxy option, the Lua has no roll, and `alertArea = 100 m` covers the whole arena. GD *does* have a true dormant ambush (`ControllerMonsterHidden`, which waits until a player is within `appearDistance` and then dissolves in), but **0 of the 466 tier-16 roster records use it.** *(DATAMINED)* Matt's "a handful of spawn chances" is not supported for p05.
2. **What GD does differently from our oracle is the emergence.** A ProxyAmbush body is spawned with `Monster::EnableSpawnAnimation()`. A plain ring `Proxy` never makes that call. Three things follow:
   - **AI layer.** The body sits in `ControllerMonsterStateStartup`, where `ShouldFindEnemy` is FALSE, `OnUpdate` is empty and `EnemyFound` and `Attacked` do nothing, while it plays its record's *spawn* clip. On the clip's `"End"` event it moves to `Idle`. Only then does it scan, acquire and pursue.
   - **Action layer.** The body runs `SpawnAction` (type 19). Attack, Move and Evade requests are **PENDING**, Stun, Knockdown and TakeHit are **REJECTED**, and Die is **REPLACE**.
   - **No protection.** Nothing writes invincible or targetable, and the radius-damage target filter admits the body. **It can be hit and killed by area damage while emerging.**

   *(DATAMINED)*
3. **Emergence lasts as long as the record's spawn clip:** plant 1.500 s, golem 3.567 s, imp hero 1.533 s, hypporaven hero 1.667 s, wight hero 2.467 or 2.833 s, wraith hero 0.867 s, Ekketzul 3.500 s, Korvaak messenger 1.4 or 1.867 s, aetherial corruption 2.45 or **4.9 s**. The clips show creatures coming out of the ground: the corruptions use the zombie crawl-out clip and the golem plays `golemswamp_phase01_appearance`. Two pairs are given as bounds because the anim-table speed composition is UNDECODED (the same open hop as D-1's `RESID-D1-1`). *(DATAMINED clip lengths; the speed composition is UNKNOWN)*
4. **The wave-151 and wave-153 p05 "Carnivorous Plant" is a stationary turret.** `controller_livingplant.dbr` is a `ControllerStationaryMonster`, the only one in the tier-16 roster. Its Pursue state issues `SetState("Attack"|"Idle")` and never moves, and Move, Return, Flee, FollowLeader and DefendLeader are all bound to one state that only does `SetState("Idle")`. Its walk and run clips are the combat-idle clip, and `disallowRotation = True`. The oracle and pack treat it as an ordinary walker. *(DATAMINED; one generic `MoveTo` inside the shared template `UseSkill` is UNREACHED)*
5. **Footage.** The video share is unreachable this session, so frames at +4–5 s are **UNKNOWN**. Existing plate reads do name p05 bodies on all four waves checked:
   - 151 and 153: Carnivorous Plant and Ugdenbog Golem;
   - 152: Vanallius the Voracious, an aetherial-corruption hero;
   - 157: Phigillius Stormbile, an imp hero.

   None is read earlier than +7.07 s into its wave, which is 3.07 s after release. *(FOOTAGE + DATAMINED identity)* So GD spawns them, and Matt's cursor was on them.
6. **Lethality.**
   - **Emergence alone** moves the graded ratio −1.5 % to −2.3 % (×3.243 → ×3.19 / ×3.17) and first-10-s pressure −7 % to −10 %.
   - **Emergence plus the stationary plant** gives first-10-s pressure ×3.32 → **×2.89–3.06**. With waves 151 and 153 excluded it gives ×3.06 → **×2.96–2.98**.
   - The headline ratio for the plant arms (×2.29–2.75) is an **artefact.** The oracle's pilot does not go and kill a stationary straggler, so wave 153 stretches from 15 s to 39–104 s, which dilutes HP/s. Matt cleared 153 in 15 s.
   - **Not the ×3.** *(SIM)*

---

## Q1: The `ProxyAmbush` records and their templates *(DATAMINED)*

**The seven tier-16 p05 proxies** (`records/proxies/tier16waves/proxy_w0{1,2,3,6,7,8,9}_p05a.dbr`) resolve last-wins to `survivalmode3`, and their values are identical across Ed II and Ed IV (prior lap). Field by field:

| field | value (all 7) | what it does (decode) | in practice |
|---|---|---|---|
| `Class` / template | `ProxyAmbush` / `proxyambush.tpl` (includes `proxy.tpl`) | deferral wrapper around a normal proxy pool | — |
| `chanceToRun` | 100.0 | `RunProxy` rolls `FGenerate(0,100) <= chance` | **never fails** |
| `delayedRun` | True | parks the proxy until Lua `:Run()` | released on the wave flip |
| `alertArea` | 100.0 m | `IsAlert`: is any `Player` within a 100 m sphere of the proxy? | **always true.** 0 of 1,284 spawn×patrol pairs on 20 maps exceed 100 m |
| `minDelayTime` / `maxDelayTime` | 4.0 / 4.0 s | delay from arming to first release | **+4.000 s (+ ≥1 tick)** |
| `minGroupSize` / `maxGroupSize` | 30 / 30 | `PlaceNextObject` calls per burst, not a body count | the whole queue (≤ 7) releases in one tick |
| `spawnThreshold` | 15 | suppresses a burst while > 15 of its own bodies are alive; loader default 10,000 | inert, because the queue is filled once |
| `minSpawnTime` / `maxSpawnTime` | 3.0 / 3.0 s | interval between bursts | inert |
| `placementExtents` | 8.0 m | proxy-local scatter disc | same as every proxy |
| `pool1..3` / `weight1..3` | see table | equal weights, picked per proxy run | — |

**Pools behind each wave** (bodies per Lap V's decoded count model, carried and unchanged):

| wave | pool(s) | bodies | gating found |
|---|---|---|---|
| 151, 153 | `livingplant_t3`: Carnivorous Plant (w 100, `limit1 = 4`) + Ugdenbog Golem (w 50); `spawnMin/Max 3/4` → decoded 4–5 | 4.5 | none |
| 152 | `aetherialcorruption_hero`: 1 of 5 heroes, `championChance 100` | 3.0 | none |
| 156 | one of `aetherialcorruption_{fire,ice,lightning}_t3`, `spawnMin/Max 5/6` | 7.0 | none |
| 157 | imp hero / corruption hero / wight hero | 3.0 | none |
| 158 | wraith hero / hypporaven hero | 3.0 | none |
| 159 | Ekketzul, or the Korvaak messenger | 1.0 | Korvaak pool: `maxPlayerLevel1 = 70` (`_02`), `minPlayerLevel2 = 70` (`_02b`), `ignoreGameBalance` |

No proxy or pool carries a difficulty-indexed field. Level comes from each entry's `levelVarianceEquation` (`lv3_strong`, `lv4_champion+`, `lv6_hero`, `lv7_uber hero`) and `proxypoolequation_01`.

**Ring points for comparison.** For example `proxy_w01_p01a.dbr` is `Class = Proxy`, `proxy.tpl`, `chanceToRun 100`, `delayedRun True`, `placementExtents 8.0`, with pools and weights. It has none of the eight ambush fields, it spawns at t = 0, and it **does not call `EnableSpawnAnimation`**: `Proxy::PoolComplete` and `Proxy::PlaceObjects` contain no `vt+0x318` call, while `ProxyAmbush::PlaceNextObject` makes one immediately before `FastSpawnEntity` (Ed IV `0x10356da9` → `0x10356dba`). 363 of the 435 ring-only records *own* a spawn clip, but the proxy path never plays it.

**Monster-side "ambush" fields are not used here.** `monster.tpl` has an *Ambush Parameters* group, `ambushDissolveTime` ("length of dissolve. 0=off") and `ambushDissolveTexture`. Its only reader in `Game.dll` is `ControllerMonsterStateHidden::OnUpdate` (`0x100fe17a`), the state of `ControllerMonsterHidden`. That is GD's real ambush:
- the monster sits in `LongIdle`;
- `OnUpdate` looks for the closest foe within `appearDistance` (default 5.0 m);
- it then plays the appear clip and calls `GraphicsMeshInstance::BeginUnDissolve`;
- on `"End"` it moves to `SetState("Pursue")`.

Ekketzul carries `ambushDissolveTime = 2`, but his controller is a plain `ControllerMonster`, so the field is inert for him. All other p05 records have 0. Census: `tier16_roster_controller_and_spawn_summary.json` (`ControllerMonster` 465, `ControllerStationaryMonster` 1, `ControllerMonsterHidden` **0**).

## Q2: The survival-mode wave logic *(DATAMINED, Ed-I `Scripts.arc` extract)*

- `tier16waves.lua` L19 says *"Possible Proxies for each wave and spawn point… Randomly selected."* Each p05 entry lists **one** proxy, and 154, 155 and 160 are `{nil}`.
- `survivalevent.lua` `SurvivalEvent_SpawnNext`: for each spawn id, if `waves[id][waveIndex] != nil` and (`id < numSpawns` or `bonusSpawnStatus`), it picks `random(1, totalProxies)` (always 1 here), then calls `Proxy.Create`, `SetCoords` and `:Run()`. `numSpawns` is the count of registered spawn entities (6), so **p05 (id 5) is unconditional**. Only p06 is gated by the bonus status.
- Ambush proxies are skipped for `LinkPatrolPointGroup`, so they get no patrol route.
- **Per wave:** p05 spawns on every declaring wave, with certainty, with the bodies rolled once per proxy run by the pool (count model per Lap V). Nothing is conditional on runtime state. The proxy queues the bodies on the flip, and no body exists until +4.000 s.

## Q3: The ambush AI state, the emergence, and targetability *(DATAMINED unless marked)*

**The chain, Ed-IV RVAs** (excerpts in `evidence/edIV_gamedll_decode_excerpts.txt`):

1. **`Monster::EnableSpawnAnimation`** (`0x2dded0`): sets `Character+0x1c64 = 1` **and** `ControllerMonster+0x4da = 1` (`SetPlayStartupAnim`).
2. **`ControllerMonsterStateStartup::OnBegin`** (`0xfe730`):
   - if `CanPlayStartupAnim` is false, it calls `SetState("Idle")` at once. This is the ring body's path.
   - otherwise, unless one anim-set predicate (`[animset+0x58]` vt `+0x3c`, unnamed) is true, it calls `ControllerAI::PlayAnimation(type 0x13 = Spawn, speed 1.0, no loop)` and stays in Startup.
3. **While in Startup:**
   - `OnUpdate` = `ret 4`.
   - `ShouldFindEnemy` and `ShouldFindClosestEnemy` resolve to the FALSE stub (vtable slots `+0x10` and `+0x14` are `0x1000c390`, against `0x10009350` TRUE in `Idle` and `Patrol`).
   - `EnemyFound` and `Attacked` are no-ops.
   - `RequestAttack` and `RequestMove` only forward to the default response.
4. **`HandleEvent`** (`0xfea60`): on `"End"` it calls `SetState("Idle")`, then `UseInitialSkillIfSet`. `Idle` scans (TRUE stub), so `EnemyFound` → `Pursue`, or `AlertBeforePursue` per D-1's six-limb gate.
5. **Action layer.** `ControllerBaseCharacter::CharacterHandlerUpdate` (`0xea480`) runs a `SpawnAction` if `JustSpawnedWithAnimation()` is true, otherwise an `IdleAction`. `JustSpawnedWithAnimation` (`0x53570`) is `flag && Entity::numUpdates < 30`, where `+0x12c` is `Entity::SetNumUpdates` / `++` in `Entity::Update`. `SpawnAction` (type `0x13` = 19) plays clip type 19 and finishes on its animation callback. RESID-D1-2's matrix, with the current action = 19:

   | requested | Attack 8 | MoveTo 4 / Walk 5 | Evade 24 | Stun 9 / Knockdown 10 / TakeHit 11 | **Die 15** |
   |---|---|---|---|---|---|
   | regime | PENDING | PENDING | PENDING | REJECT | **REPLACE** |

   If a `PlayAnimationAction` (18) is current instead, `Spawn` replaces it (`grid[19][18] = 0`). Which of the two installs first is UNREACHED, but either way the spawn clip plays.
6. **No protection write.** In Character code the invincible byte (`+0x1844`) is written only by `Load`, `SetInvincible` and its config command. Those are reached from quest commands and `ControllerAI::SetInvincible`, and no spawn path calls them. The targetable byte (`+0x182e`) is written only by `Load` and `SetTargetableConfigCmd` (from `ControllerCombat::HandleEvent`). `ControllerMonsterStateStartup::OnEnd` only *restores* DB defaults (show if hidden; clear invincible if not invincible in the DB; set targetable if targetable in the DB). That serves script-hidden monsters and does nothing to our records.
7. **Area damage reaches it.** `GameEngine::GetTargetsInRadius` / `GetAllTargetsInRadius` → `FilterInvalidTargets` (`0x26a810`) drop an entity only if it has not done its initial update, is not alive, `IsHiding()` (invisible, or `hiddenFromCombat`, or lifeState 0) or is not a foe. A spawning p05 body is alive, visible, `hiddenFromCombat = 0` on 31/31 records, and lifeState stays 2 (lifeState is only set to 3, 4 or 5 on die, dead or respawn). **So radius skills (EoR or Whirlwind) damage it, and Die REPLACE lets it die mid-clip.**

**Reconciling Matt's observation** (relayed by gandalf: *no name, no health bar, cannot be targeted or selected while spawning*) **with the above:**
- **Both can be true, on different layers.** Nameplates, health bars and cursor picking are UI. The UI lives in `Grim Dawn.exe`: neither DLL contains a UI class or the string `UIWorldActorDescription` (0 hits in both), and the exe is not on this machine (its `.text` is also Steam-DRM-bound, per Lap AA). The UI side is therefore **UNREACHED**.
- **INFERRED, with evidence:** `Character::GetSpawnAnimationEnabled` and `JustSpawnedWithAnimation` are *exported*, and their only Game.dll consumers are the action handler, replication and NPC startup. That fits an exe-side UI consumer.
- **The simulation layer (Game.dll) is decoded.** The emerging body is **damageable by area effects, killable, unable to act, and immune to flinch, stun and knockdown actions.**
- `hiddenFromCombat` ("Hide from UI and Combat") is the field GD uses when it wants both. It is **not** set on these records, which is consistent with "UI-hidden, combat-live".

**Can it attack before emergence completes?** No. The controller makes no attack decisions in Startup, and an Attack action would be PENDING behind `SpawnAction`. **Invulnerable or untargetable in the simulation?** No. **How long?** The clip length (Q-table below), plus at least one AI tick (UNKNOWN) before `Idle` acquires.

**Spawn-clip lengths** = `(frames − 1) / 30` from the shipped `.anm` headers (`anm_index.json`, Ed-III extract). The table is `p05_roster_spawn_controller_census.csv`:

| record (name) | clip | s @ speed 1.0 | anim-table speed | emergence D |
|---|---|---:|---:|---|
| livingplant_a01 (Carnivorous Plant) | carnivorousplant01a_p2_spawn_b01 | 1.500 | 1.0 | **1.500** |
| swampgolem_a01 (Ugdenbog Golem) | golemswamp_phase01_appearance_a01 | 3.567 | 1.0 | **3.567** |
| aetherialcorruption_b0x / _h0x | aetherialcorruption_spawn_a01 (unarmed), zombie01_unarmed_spawn_a01 | 4.900 | 2.0 (unarmed) | **2.45 – 4.90** |
| aetherialimp_h0x | aetherialimp_spawn_a01 | 1.533 | 1.0 | 1.533 |
| wight_h0x | wight02a_spawn_01a / wight01a_spawn_01a (2h) | 2.467 / 2.833 | 1.0 | 2.467 – 2.833 |
| wraith_h0x | wraith_spawn_a01 | 0.867 | 1.0 | 0.867 |
| hypporaven_h0x | gryphon01a_spawn_b01 | 1.667 | 1.0 | 1.667 |
| chthonianrylok_ekketzul | chthonianrylok_spawn_c01_fire | 3.500 | 1.0 | 3.500 |
| korvaakmessenger_02 / 02b | chthonianrylok_roar_a01 | 1.400 | 0.75 | 1.40 – 1.867 |

## Q4: Footage check

- **Direct frame check at +4.0–5.0 s on 151, 152, 153 and 157: UNKNOWN.** The referent (`eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`, sha `4c60960d…`) lives on the Pi share. `/Volumes/reincarnated` is unmounted, and `ssh reincarnated-pi.local` times out at the banner (the T22 symptom). No local frame bank covers those windows; the local stills are HUD crops.
- **What existing plate reads say** (`footage_p05_plate_reads.csv`; galadriel's hover nameplate reads, with p05 identity DATAMINED from pool seating). Time after release uses galadriel's onsets:

  | wave | name | p05 identity | time after release |
  |---|---|---|---:|
  | 151 | Carnivorous Plant | plant | 6.10 s, 8.70 s |
  | 152 | Vanallius the Voracious | `aetherialcorruption_h02` | 7.42 s |
  | 153 | Ugdenbog Golem | golem | 3.07 s, 3.60 s |
  | 153 | Carnivorous Plant | plant | 3.64 s |
  | 157 | Phigillius Stormbile | `aetherialimp_h01` | 4.93 s |

- **So:**
  - (a) GD spawned the p05 group on every wave checked. *(FOOTAGE)*
  - (b) These bodies were hovered by Matt's cursor, which means they were selectable once emerged.
  - (c) **No p05 plate appears before +3.07 s after release.** That fits "no plate while emerging" for every row except the golem's 3.07 s against a 3.567 s clip, which is inside the ±1 s onset uncertainty. It is *not* proof, because hover timing is the player's.
- **What would settle it:** mount the share, extract 30 fps frames over onset + [3.5, 9.0] s on 151, 152, 153 and 157, and look for:
  - the crawl-out or sprout animations near p05;
  - whether a hover during them shows a plate;
  - whether EoR damage numbers land on an emerging body.

## Q5: How the oracle models p05 today, and the delta *(SIM / code, read-only)*

| item | oracle (`simulation/kc2/`) | GD | delta |
|---|---|---|---|
| certainty / waves | p05 on 151, 152, 153, 156, 157, 158, 159 from `pools_for(...).is_ambush` (`run.py:1184-1188`) | same | none |
| count | pool roll, Lap V model (band 26.0) | same | none |
| release | `ambush_burst=True` (`roster.py:282`) → all at `P05_FIRST_ARRIVAL_S = 4.0` (`wave_engine.py:543, 685-688`) | +4.000 s + ≥ 1 tick, burst | none (tick slop) |
| position | stalagmite label (−6.82, 2.18) | true p05, 10.10 m (prior lap) | known, −0.6 % |
| before release | body does not exist until `spawn_t_s` (`run.py` live set `spawn_t_s <= t`) | nothing on the board | none. **The port differs**: it shows grey "ARRIVING" bodies from t = 0 that cannot be hit (`kc2p_card.gd:52`, `kc2rt_fight.gd:5900`) |
| emergence | **none.** On the board at 4.0 s it pursues and attacks at once (first p05 hit at 4.0 s on 152 and 156 in the control) | Startup + SpawnAction for D s: no move, no attack, no acquisition, **damageable** | **missing** |
| "spawn protection" | none in the oracle. The port's 4.0 s "cannot be hit" hold is a runtime construct | **no protection** at any point; during D it is hittable but inert | the port protects bodies GD would not; the oracle omits the inert window |
| AI state after spawn | no state machine; pursue at once (alert fold off) | Idle → acquire → Pursue / AlertBeforePursue | acquisition latency UNKNOWN |
| Carnivorous Plant | walker: `characterRunSpeed 1.0`; pack serves `MaxPursuitDistance 125` (measured 35, `monster_kinematics.json` known override); no `ControllerStationary` handling anywhere (grep: 0 hits) | stationary turret: bite short range, venomous seed medium range (2.5–22 m), never moves | **missing** |
| CC during spawn | CC not actuated anyway | Stun, Knockdown and TakeHit REJECT during SpawnAction | n/a |

## Q6: Lethality counterfactual *(SIM, NOT-A-GRADED-RUN)*

**Tool:** `tools/ambush_counterfactual.py`, wrapping `run_arm("PW-FOLDED")`, salts 0–19. The control reproduces exactly (×3.243 at 20 salts, ×3.17 at 0–4). The wraps:
- **HOLD** keeps a p05 body unmoving (`Mover.step` with dt = 0) and gives it no attack opportunity for D s, while it stays hittable.
- **PLANT** pins `livingplant_a01` for its whole life.
- **ABSENT** is a bound and not GD: it delays the body's existence by D.
- The A-3 mechanism guard needs a named halt code for an unmoved body, so held steps are labelled hold-code 17 (telemetry only).

| arm | graded ×ref (151–159) | first-10-s ×ref | ×ref excl. 151/153 | wave-153 mean duration | mean death wave |
|---|---:|---:|---:|---:|---:|
| PACK (control) | **3.243** | **3.318** | **3.062** | 15.4 s | 154.3 |
| HOLD-SHORT | 3.194 (−1.5 %) | 3.074 (−7.4 %) | 2.900 | 14.4 s | 154.2 |
| HOLD-LONG | 3.169 (−2.3 %) | 2.994 (−9.8 %) | 2.874 | 14.8 s | 154.3 |
| PLANT | 2.290 ⚠ | 3.409 | 3.115 | **79.2 s** | 154.9 |
| GD-SHORT (hold + plant) | 2.502 ⚠ | 3.064 | 2.958 | 53.0 s | 153.6 |
| **GD-LONG (hold + plant)** | 2.746 ⚠ | **2.894 (−12.8 %)** | **2.979 (−2.7 %)** | 39.1 s | 153.7 |
| GD-LONG at true p05 (TRUE-A) | 1.951 ⚠ | 2.843 | 3.098 | 104.0 s | 154.4 |
| ABSENT-LONG (bound, not GD) | 3.224 | 3.066 | 3.017 | 15.1 s | 155.0 |

⚠ **Do not read the graded ratio for the plant arms.** The landed totals barely move. The ratio falls because wave 153 runs 39–104 s instead of 15 s: once the plants cannot walk to the player, **the oracle's pilot does not go and kill them**, and the wave cannot advance until they die. The referent cleared 153 in 15 s. The duration-robust columns are the reading.

**Verdict (INFERRED from the table):**
- Modelling GD's real ambush (an inert-but-hittable emergence plus a stationary plant) **lowers early pressure by roughly 8–13 % and the steady rate by roughly 3 %**.
- The death wave does not move outside noise.
- **It does not close the ×3.**
- It does expose a **new oracle gap: no pilot behaviour for killing a stationary body.**

**Not modelled, UNKNOWN:**
- the AI acquisition latency after Startup → Idle;
- whether damage *auras* run during the clip;
- the anim-speed composition (bounded by the SHORT and LONG arms);
- AlertBeforePursue (off in PW-FOLDED);
- the arena identity among a, b and e.

---

## What pack v3.8 must encode (each with its source)

1. **Keep:** p05 is certain on 151, 152, 153, 156, 157, 158 and 159, with Lap V counts and a burst at +4.000 s. **No dormant, proximity or chance gate.** Sources: § Q1 and § Q2; Lap V-2 F-3 to F-5; `ControllerMonsterHidden` 0/466.
2. **New: an emergence window per record** (Q3 table, D_short and D_long). During it the body:
   - is on the board, hittable and killable;
   - **does not move, attack or acquire**;
   - is immune to the flinch, stun and knockdown *actions*.

   After it: Idle → acquire → pursue, with the acquisition latency declared UNKNOWN. Sources: `Monster::EnableSpawnAnimation`, `ControllerMonsterStateStartup::{OnBegin, HandleEvent}`, `CharacterHandlerUpdate`, and the RESID-D1-2 matrix row 19. Applies to **ProxyAmbush bodies only**; ring bodies keep zero emergence (`Proxy::PoolComplete` / `PlaceObjects` make no `vt+0x318` call).
3. **New: Carnivorous Plant (`livingplant_a01`) is stationary.** Movement is 0 and it keeps its ranged and melee slots. Correct the served `MaxPursuitDistance` to the measured 35. Source: `controller_livingplant.dbr` (`ControllerStationaryMonster`) and the stationary Pursue and null-state decode.
4. **Presentation rule, port only (not simulation):** no nameplate, no health bar and no cursor-selectability while emerging. Source: Matt's testimony; UNREACHED in the binaries (the exe). Remove the port's 0–4 s visible-but-unhittable "ARRIVING" hold. GD shows nothing for 0–4 s and then an emerging body that *can* be hit.
5. **Declare:** the speed-composition hop (corruption 2.45 or 4.9 s; messenger 1.4 or 1.867 s); the acquisition latency; aura behaviour during the clip.
6. **Carry from the prior lap:** the p05 position re-vendor (true p05 is 10.10 m from the centroid, not the stalagmite label).
7. **Route to gamora:** the pilot needs a stationary-target clearing behaviour, or a plant-faithful pack will stall wave 153.

## Knowledge gaps not resolved

| # | gap | what settles it |
|---|---|---|
| G-1 | Footage at +4–5 s (emergence visible? plate suppressed?) | mount the Pi share; 30 fps extraction over onset + [3.5, 9] s on 151, 152, 153 and 157 |
| G-2 | UI suppression mechanism (nameplate, health bar, pick) | a non-DRM `Grim Dawn.exe` or a live probe; out of reach in the DLLs |
| G-3 | Anim-speed composition (record or anim-table speed × the 1.0f passed) | the unexported per-slot anim class `vt+0x4` (same hop as RESID-D1-1) |
| G-4 | Startup predicate `[animset+0x58]` vt `+0x3c` (when the clip is skipped) | name that anim-set class; this is the first slice of the enemy-AI decode run |
| G-5 | Acquisition latency after Idle | the AI update loop (Lap U `UNREACHED-U1`) |
| G-6 | The generic `MoveTo` in the stationary template's `UseSkill` (`0x1012a6da`) | its guard condition |

## Files

| file | what |
|---|---|
| `p05_roster_spawn_controller_census.csv` | 31 p05 records: names, controller class, startVisible, hiddenFromCombat, ambush dissolve, spawn clips, D |
| `tier16_roster_controller_and_spawn_summary.json` | whole-roster controller-class census (466) |
| `footage_p05_plate_reads.csv` | p05-identifiable plate reads with times after release |
| `ambush_counterfactual_PW-FOLDED_salts0-19.json` | the eight arms, salts 0–19 and the 0–4 subsets, with per-wave detail |
| `evidence/edIV_gamedll_decode_excerpts.txt` | disassembly of every function cited above, with binary sha256 |
| `tools/` | `ambush_counterfactual.py`, `dump_decode_evidence.py`, `pe4_edition_IV.py`, `tier16_monster_spawn_census.py` |

## Source list (accessed 2026-10-01)

- **Vendor:**
  - `~/Games/vendor/grim-dawn-edition-IV-20260929/` (`Game.dll` `e75925d1…`, `Engine.dll` `f18e8658…`, 8 `.arz`)
  - `~/Games/vendor/grim-dawn-edition-II-20260724/` (`Text_EN.arc` × 3, for display names)
- **Lua:** `legolas/scratch/2026-08-07-u8-tierwave/lua/{sm1/game/survival/tier16waves.lua, smmod/game/events/survivalevent.lua}`
- **Templates:** `legolas/scratch/2026-08-08-kc2-halt-bundle/tpl/{proxyambush, monster, characterenemy, controllermonsterhidden, controllerstationarymonster}.tpl`
- **Prior findings:**
  - `legolas/notes/2026-08-15-kc2-pm4-lap-v2-proxyambush-decode/pm4v2_findings.md`
  - `…/2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv`
  - `…/2026-08-25-kc2-mc-lap-resid-d1-2/findings.md` + `engine data/kc2/resid_d1_2_action_permission_matrix.json`
  - `…/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json`
  - `legolas/findings/2026-09-29-gd-enemy-ai-own-files-inventory.md`
  - `legolas/research/2026-10-01-crucible-spawn-p05/`
  - `legolas/research/2026-10-01-kc2-enemy-range-audit/` (collab `2eb2ca138`)
- **Footage reads:** `galadriel/notes/2026-08-08-kc2-{third,fourth,fifth-extraction-w153-identity,barhue-cohort-correction,crabling-rotmouth-touch}.md`; `engine data/kc2/pm3_measured_reference_truth.csv`
- **Engine (read-only):**
  - `simulation/kc2/{run,wave_engine,roster,locomotion,threat,reengagement,action_permission}.py`
  - `simulation/scripts/gamora_kc2_play_c11a_fold_pricing_2026_09_30.py`, `gamora_kc2_c11_lethality_decomposition_2026_09_29.py`
  - pack `output/kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247/model/monster_kinematics.json`
- **Port (read-only):** `reincarnated-godot/kc2_play/src/{kc2p_card,kc2p_ground}.gd`, `kc2_runtime/sim/kc2rt_fight.gd`
