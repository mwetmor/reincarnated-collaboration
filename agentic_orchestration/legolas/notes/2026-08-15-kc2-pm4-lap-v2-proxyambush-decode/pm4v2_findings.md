# KC2-PM4 · LAP V-2 — THE `ProxyAmbush` DECODE · FINDINGS

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Authority:** `R-PM4-58 part 2`, on Matt's word (2026-08-15, Q-b, verbatim): ***"decode it."***
**Date:** 2026-08-15.

**Pre-registration:** `PREREGISTRATION.md`, sha256
`d3653ba634cd48a55bc3200674e889e06500749919b911f0095424beae7fe8e9`, **committed ALONE in commit
`32b63c70` before any instrument of this lap ran** (the `L-46` carry — priority is git-attested,
held on first use at Lap V and held again here).

**All twelve pinned inputs re-hashed at instrument start; zero mismatches; no HALT fired.**

---

## § 0 — THE HEADLINE TABLE

| # | finding | grade |
|---|---|---|
| **F-1** | **⚑ `spawnThreshold` COUNTS THE AMBUSH'S OWN *LIVING* PLACED BODIES — NOTHING ELSE.** The compare at `0x103545f9` reads `(m_placedIds.end − m_placedIds.begin) >> 2` against `[this+0x504]`, and the vector it measures is pruned every tick by a loop that erases any id whose `ObjectManager` lookup fails **or** whose `Monster` vtable slot `0x22c` — decoded as **`Character::IsAlive()`** — returns false. Not players, not kills, not distance, not a global count. | **DECODED** |
| **F-2** | **⚑ `ProxyAmbush` ADDS ZERO BODIES. IT IS A DEFERRAL WRAPPER AROUND AN ORDINARY PROXY POOL.** `PoolComplete` (`0x10354fb0`) takes the pool's resolved id vector at `pool+0xb0` — **the exact vector Lap V's `F-5` decoded** — moves it into a *pending* queue at `[this+0x4d0]`, and clears the pool. `min/maxGroupSize` never creates a body; it is the number of `PlaceNextObject` calls per burst. | **DECODED** |
| **F-3** | **⚑ IT IS ONE-SHOT PER WAVE, SO `spawnThreshold` AND THE 3.0 s TIMER ARE *INERT*.** `Proxy::RunProxy` early-returns unless `[this+0x4ac] == 0` (`0x10351d50`) and sets it to `6` on success (`0x10351fd4`). The queue is filled once and never refilled; the first burst releases `Uniform[30,30] = 30` ≫ the largest p05 pool (7), so it empties the queue and no second burst can ever occur. | **DECODED** |
| **F-4** | **⚑ `alertArea = 100.0` IS ARENA-COVERING — THE "AMBUSH" IS NOT A PROXIMITY GATE IN PRACTICE.** `IsAlert` builds a `Sphere{proxy's own coords, r = alertArea}` and asks `World::GetEntitiesInSphere`, filtering the result by RTTI against `?classInfo@Player@GAME@@`. Across all **20** arena maps: max spawn→patrol distance **77.52 m**, max spawn→spawn **85.58 m**, and **0 of 1,284** spawn×patrol pairs exceed 100 m. `IsAlert()` is true from the first evaluated tick wherever the player stands. | **DECODED** |
| **F-5** | **⚑ THE WHOLE MECHANISM REDUCES TO ONE NUMBER: `+4.000 s` OF ARRIVAL DELAY.** All 54 tier-16 wave proxies share `delayedRun = True`, `chanceToRun = 100.0`, `placementExtents = 8.0`. The seven ambushes differ **only** by the eight `ProxyAmbush` fields, and once `alertArea` is inert and the group/threshold pair is inert, what is left is `Uniform[minDelayTime, maxDelayTime] = [4000, 4000] ms`. | **DECODED** |
| **F-6** | **⚑ THE PER-WAVE p05 NUMBERS ARE UNCHANGED AND NOW *EXACT*.** 151→**4.5**, 152→**3.0**, 153→**4.5**, 156→**7.0**, 157→**3.0**, 158→**3.0**, 159→**1.0**; band total **26.000**. Lap V § 6.1 published these as a **FLOOR**; the decode says they are the **value**. **Lap V's § 4.1 band totals (decoded p06-OFF 172.083 / p06-ON 197.083) are hereby DECODE-COMPLETE, not floors.** | **DECODED** |
| **F-7** | **⚑ MY OWN BLIND DIRECTIONAL BET `H-8` IS REFUTED 0/7.** I pre-registered that the decoded p05 **ceiling would exceed** Lap V's floor on **all seven** declaring waves. It exceeds it on **none**: ceiling **equals** floor, seven times out of seven. Self-caught by pre-registration, reported at the top rather than buried. | **DEFECT-CLASS: PREDICTION REFUTED** |
| **F-8** | **AMBUSH BODIES PURSUE.** The Lua withholds `LinkPatrolPointGroup` from ambush proxies (`survivalevent.lua` L552–553), which removes a **patrol route**, not the pursuit AI. The `mov al,1; ret` stub Lap U found at `ShouldFindEnemy@…StatePatrol` (RVA `0x00009350`) is ICF-shared by **15** states including **`Idle`, `Move`, `Wander`, `Roam`, `Return`** — every state an unpatrolled monster can idle in scans for enemies and transitions to `Pursue`. | **DECODED** |
| **F-9** | **⚑ LAP V's `UNREACHED-V5` IS CLOSED AS A SIDE-EFFECT.** The element type of the emitted-body vector at `[ProxyPool + 0xb0]` is **`unsigned` — entity IDs**: `PlaceNextObject` reads `[edi]` as a dword and hands it to `ObjectManager::GetObject` (`0x103551c4`). | **DECODED** |
| **F-10** | **THE AMBUSH APPEARS TO GATE WAVE ADVANCE — but I did not reach the proof.** `GetPlacedObjects` (`0x10354dd0`) deliberately appends the **not-yet-spawned** pending ids as well as the live ones, which is the shape `AllKilled()` (the wave-advance test at `survivalevent.lua` L716) would consume. **The native body of the `AllKilled` Lua binding was NOT located** — `UNREACHED-V2-1`. Given `F-4` + `F-5` the ambush always fires ~4 s in, so this changes no number. | **INFERRED-WITH-EVIDENCE** |
| **F-11** | **NO FOURTH MECHANISM.** All **54** tier-16 wave-proxy records are `Proxy` (47) or `ProxyAmbush` (7). No `ProxyEndless`, no `SetPiece`, no fourth declared class in the band. `R-PM4-56 part 4` does **not** trip. | **DECODED (negative)** |

---

## § 1 — TARGET (a), PART 1: THE FIELD → OFFSET MAP

`ProxyAmbush::Load` (`0x10354400`) calls `Proxy::Load` first (`0x1035440b`) — so **every base-proxy
field is loaded too** — then reads its own eight, in this order. `LoadTable` vtable slot `+0x24` is
`GetFloat(name, default)`; slot `+0x1c` is `GetInt(name, default)`. The float constant multiplied
into the four timers, at `0x105f5918`, is **`1000.0`** — seconds → milliseconds, truncated by
`cvttss2si`.

| `.dbr` field | member | loader call | store site | shipped value (all 7) | decoded units |
|---|---|---|---|---|---|
| `alertArea` | `[this+0x4e8]` | `GetFloat(name, 0.0f)` | `0x10354426` | `100.0` | world units (= metres) |
| `minSpawnTime` | `[this+0x4ec]` | `(int)(GetFloat×1000)` | `0x1035445f` | `3.0` → `3000` | ms |
| `maxSpawnTime` | `[this+0x4f0]` | `(int)(GetFloat×1000)` | `0x10354489` | `3.0` → `3000` | ms |
| `minDelayTime` | `[this+0x4f4]` | `(int)(GetFloat×1000)` | `0x103544b3` | `4.0` → `4000` | ms |
| `maxDelayTime` | `[this+0x4f8]` | `(int)(GetFloat×1000)` | `0x103544d7` | `4.0` → `4000` | ms |
| `minGroupSize` | `[this+0x4fc]` | `GetInt(name, 1)` | `0x103544e2` | `30` | count |
| `maxGroupSize` | `[this+0x500]` | `GetInt(name, 1)` | `0x103544f6` | `30` | count |
| `spawnThreshold` | `[this+0x504]` | `GetInt(name, **10000**)` | `0x1035450d` | `15` | count |

> The `spawnThreshold` **loader default is 10,000** — i.e. a `ProxyAmbush` that omits the field
> never suppresses a burst. That is the shipped intent of the field: a *ceiling*, not a trigger.

**Runtime members decoded alongside** (all ctor-zeroed at `0x1035421b`–`0x1035424d`):

| member | meaning | evidence |
|---|---|---|
| `[0x4a0]` | `m_totalObjects` — the pool's resolved size | `0x10354fe5` |
| `[0x4a4]` | placed counter, `++` per successful spawn | `0x103552ae` |
| `[0x4ac]` | **the `Proxy` run latch** | `0x10351d50` / `0x10351fd4` |
| `[0x4c8]` | `ProxyPool*` (monsters) | `0x10351f6c` (`+0xb0`), `0x10351fc9` |
| `[0x4cc]` | accessory/loot container — **not roster** | `0x10351f92`, vt `+0x1fc` = `AccessoryComplete` |
| `[0x4d0]`/`[0x4d4]` | **pending** ids, `vector<unsigned>` | `0x10354fc8` |
| `[0x4dc]`/`[0x4e0]` | pending `WorldCoords`, stride `0x34` | `0x10354feb` |
| `[0x508]`/`[0x50c]` | **placed AND still alive** ids | `0x103552a9` (push), `0x1035469b` (erase) |
| `[0x514]` | `m_spawnTimer` (ms) | `0x103545c4` |
| `[0x518]` | `m_delayTimer` (ms) | `0x103545a7` |
| `[0x51c]` | `m_armed` latch, set once, never cleared | `0x10354588` |
| `[0x51d]` | re-select-locations flag — **written only by `RestoreState`** | `0x10354d93` |

---

## § 2 — TARGET (a), PART 2: THE TRIGGER ARITHMETIC, DECODED

`ProxyAmbush::UpdateSelf(int dt)` @ `0x10354520`, in full. `edi = this`, `esi = dt`.

```
Actor::UpdateSelf(dt)                                                    ; 0x10354530 (base, via IAT)
if (NavManager::Get()->IsNavDataLoaded(this->GetRegion())
    && !gEngine->IsNetworkClient())                                      ; 0x10354547 / 0x10354559
        this->Proxy::RunProxy();                                         ; 0x10354565  <- SERVER-SIDE ONLY

if (!this->m_armed) {                                                    ; 0x1035456a  cmp byte [edi+0x51c],0
    if (!this->IsAlert()) return;                                        ; 0x10354575 / 0x1035457c
    this->m_armed = true;                                                ; 0x10354588
    this->m_delayTimer = IGenerate(minDelayTime, maxDelayTime);          ; 0x103545a1 -> [edi+0x518]
    return;                                                              ; 0x103545b3  (no placement this tick)
}
if (this->m_delayTimer > 0) { this->m_delayTimer -= dt; return; }        ; 0x103545be -> 0x103546c7

this->m_spawnTimer -= dt;                                                ; 0x103545c4
if (this->m_pendingIds.empty()) return;                                  ; 0x103545d1..0x103545db
if (this->m_spawnTimer <= 0) {
    n_live = (m_placedIds.end - m_placedIds.begin) >> 2;                 ; 0x103545ea..0x103545f6
    if (n_live > this->spawnThreshold)          /* UNSIGNED `ja` */      ; 0x103545f9 / 0x103545ff
        this->m_spawnTimer = minSpawnTime;                               ; 0x1035464f  (suppress; retry later)
    else {
        n = IGenerate(minGroupSize, maxGroupSize);                       ; 0x1035461f
        for (i = 0; i < n; ++i) this->PlaceNextObject();                 ; 0x10354627..0x10354631
        this->m_spawnTimer = IGenerate(minSpawnTime, maxSpawnTime);      ; 0x1035464b
    }
}
/* every tick past the delay: prune the live set */                      ; 0x1035465b..0x103546bc
for (it = m_placedIds.begin; it != m_placedIds.end; ) {
    Object* o = ObjectManager::Get()->GetObject(*it);                    ; 0x10354672 / 0x1035467a
    if (o == nullptr || !o->vt[0x22c]())   /* Character::IsAlive() */    ; 0x10354681 / 0x1035468f
        erase(it);                        /* memmove + end -= 4 */       ; 0x103546a6 / 0x103546af
    else ++it;
}
```

**`F-1`, stated exactly.** *Threshold of what:* the count of entity IDs in `[this+0x508]`.
*Which ids:* only those this ambush itself spawned (`push_back` at `0x103552a9`), minus those the
prune loop has removed. *Why "living":* the prune predicate is the `Monster` vtable slot `0x22c`,
which resolves to **`?IsAlive@Character@GAME@@UBE_NXZ`** (`0x10047200`). *Measured where:* on the
proxy object itself, not the world. *Evaluated when:* **per tick**, inside `UpdateSelf(int)`, and
only after the delay has elapsed. *The predicate:* `place iff n_live <= spawnThreshold`, via an
**unsigned `ja`** on the negation — so with `spawnThreshold = 15` the burst is suppressed at 16+
living.

> **One-tick staleness, stated because it is true:** the count read at `0x103545ea` is the value
> left by the **previous** tick's prune, since the prune loop runs later in the same function.

**Vtable-base method note.** The `Monster` and `ProxyAmbush` vtable bases were established by the
empirical convention **slot `0x000` = `GetRTTIClassInfo`**, corroborated three ways: it puts
`UpdateSelf` at `0x168` for both classes; it makes `RunProxy`'s two 2-argument virtual calls
type-correct (`+0x1f8` = `PoolComplete(ProxyPool*, …)` fed a raw `[this+0x4c8]`, `+0x1fc` =
`AccessoryComplete(vector<unsigned>&, …)` fed `[this+0x4cc]+0x20`); and slot `+0x200` lands exactly
on `GetRTTIClassInfo@ProxyEndless`, i.e. the start of the next class's table. See `D-V2-1`.

---

## § 3 — TARGET (b): WHAT SPAWNS

**The chain, end to end:**

1. `Proxy::RunProxy` (`0x10351d30`) resolves the monster pool at `[this+0x4c8]`, calls
   `SelectPoolLocations(pool->[0xb0], this->[0x414], true)` (`0x10351f75`), then dispatches vtable
   `+0x1f8` (`0x10351fc9`) = **`ProxyAmbush::PoolComplete(pool, coords)`**.
2. `ProxyAmbush::PoolComplete` (`0x10354fb0`):
   `m_pendingIds = pool->[0xb0]` (`0x10354fc8`) · `m_totalObjects = size` (`0x10354fe5`) ·
   `m_pendingCoords = coords` (`0x10354feb`) · **`pool->[0xb0].end = pool->[0xb0].begin`**
   (`0x10354ff4`) — the pool's vector is emptied into the queue.
3. `ProxyAmbush::PlaceNextObject` (`0x103550c0`) pops **exactly one** id and one `WorldCoords`
   (`memmove` at `0x1035519b` / `0x103551b5`), and **early-exits without spawning if either queue
   is empty** (`0x10354138` / `0x1035513e`). Then:
   `GameEngine::FastSpawnEntity(entity, coords)` (`0x1035529a`) ·
   `m_placedIds.push_back(id)` (`0x103552a9`) · `++[this+0x4a4]` (`0x103552ae`).
   For entities passing the `Monster` RTTI test: `[entity+0x37bc] = this->GetObjectId()`
   (`0x1035522d`), `[entity+0x37d8] = m_totalObjects` (`0x1035526f`), and `Monster` vtable `+0x314`
   = **`Monster::EnableSpawnAnimation()`** (`0x10355289`).

**`pool + 0xb0` is the same vector Lap V's `F-5` located** and that the count-resolver
`Game.dll sub_10357590` fills. **Therefore, verbatim and without amendment:** the regular draw
`n = lo + rand() % (spawnMax − lo + 1)`, the champion-first ordering, the
`(base + additive) × modifier` operator order, `NO_OP_ON_EMPTY`, **and the `F-8` `limitN` capacity
cap all apply to the ambush's bodies exactly as they do to a plain proxy.** Lap V's
`pm4v_roster_arithmetic.csv` already priced the p05 rows through that model; nothing in this lap
moves any of those numbers.

**Compare the non-ambush baseline.** `Proxy::PoolComplete` (`0x10352580`) walks `pool->[0xb0]` and
does the same per-entity work **immediately**, in the same call. The ambush's override changes one
thing: *when*.

> **`H-4alt` is what the bytes say.** `min/maxGroupSize` is a **per-burst release count**, not a
> body count. I pre-registered the alternative precisely so that this outcome could not be spun,
> and I am reporting it with the emphasis I would have given the large answer.

---

## § 4 — TARGET (c): WHEN

**One-shot, per wave, with a 4.000 s delay.**

* **The latch.** `RunProxy` begins `cmp dword [this+0x4ac], 0 / jne → return` (`0x10351d50`) and
  ends `mov dword [this+0x4ac], 6` (`0x10351fd4`). The only writers anywhere in the `Proxy` family
  are: ctor → `0`, `Proxy::Load` → `1` when `delayedRun` (`0x10351144`), `Proxy::DelayedRun`
  `1 → 0` then tail-jump into `RunProxy` (`0x10351d10`), `RunProxy` → `5` on a `chanceToRun` fail
  (`0x10351e1e`) or `6` on success, `Proxy::Disable` → `2`, `Proxy::ResetSettings` → `0`.
* **`delayedRun = True` on all 54 tier-16 proxies**, so `Load` parks the state at `1` and the Lua's
  `:Run()` (`survivalevent.lua` L558) releases it via `DelayedRun`. `chanceToRun = 100.0` and the
  roll is `IGenerate`-free `FGenerate(0, 100.0)` compared with `jbe` — it can never fail.
* **Fresh proxy per wave.** `survivalevent.lua` L548 `Proxy.Create(...)` per spawn point per wave.
  The latch is therefore per-wave by construction; `ResetSettings` never has to be involved.

**The timeline of one declaring wave:**

| t | event | evidence |
|---|---|---|
| wave start | `Proxy.Create` → `Load` (state 1) → `:Run()` → `DelayedRun` → `RunProxy` → pool resolves → `PoolComplete` **queues** N bodies. **Zero bodies on the board.** | L548/L558, `0x10351d10` |
| first ticked frame | `IsAlert()` true (§ 5) → `m_armed = 1`, `m_delayTimer = Uniform[4000, 4000] = 4000 ms` | `0x10354588`, `0x103545a1` |
| + 4.000 s | delay elapses; `m_spawnTimer` is ctor-zero so it is already ≤ 0; queue non-empty; `n_live = 0 ≤ 15` → **burst of `Uniform[30,30] = 30` `PlaceNextObject` calls**, of which the first N spawn and the remaining `30 − N` are no-ops on an empty queue | `0x10354627` |
| thereafter | queue empty; `RunProxy` latched at 6 → **never refills**. `spawnThreshold` and the 3.0 s interval have nothing left to gate. | `0x10351d50` |

> **This is why `H-2` is refuted.** `PlaceNextObject` *does* place exactly one object per
> invocation — that half of the prediction held — but `UpdateSelf` calls it thirty times inside a
> single tick. The release is a **burst**, not a trickle, and the 3.0 s spawn timer never governs
> anything in this band.

---

## § 5 — TARGET (d): WHERE, AND WHAT `alertArea` ACTUALLY DOES

**`ProxyAmbush::IsAlert()` (`0x10355000`), decoded:**

```
float r = this->alertArea;                                     ; [esi+0x4e8]
WorldCoords wc = this->GetCoords();                            ; 0x1035504c  Entity::GetCoords
const Vec3& p  = wc.GetRegionPosition();                       ; 0x10355054  WorldVec3::GetRegionPosition
Sphere s = { p.x, p.y, p.z, r };                               ; 0x1035505d..0x10355075
Region* rg = this->GetRegion();                                ; 0x1035507a
World::GetEntitiesInSphere(scratch, rg, s, true, 2);           ; 0x10210482 -> IAT 0x104e5574
filter scratch by RTTI == ?classInfo@Player@GAME@@ (0x107ff5a0)
return !result.empty();                                        ; 0x10355090  cmp begin,end / setne
```

**Centre = the proxy's own world position. Radius = `alertArea` = 100.0. Filter = `Player`.**
`alertArea` is a **radius**, not an area: it is stored at `sphere+0x0c`, the fourth float of a
`{Vec3, float}`.

**Placement geometry is proxy-local, with no player read anywhere on the path.** The coordinates
are computed by `Proxy::SelectPoolLocations` inside `RunProxy` **before** `PoolComplete`
(`0x10351f75`) and stored in the pending coords vector. `PlaceNextObject` re-runs
`SelectPoolLocations` only when `[this+0x51d]` is set — and that flag is written by
**`RestoreState` alone** (`0x10354d93`), i.e. the save/load path. `placementExtents = 8.0` on all
54 tier-16 proxies, matching the `placement_extents_m = 8.0` Lap U already recorded. **`H-5` held.**

**⚑ And now the deflationary part.** Using Lap U's `pm4u_geometry_v3.csv` + `pm4u_map_placements_v3.csv`:

| quantity | value |
|---|---|
| arena maps examined | **20** (`survivalworld_a…j` × `survivalmode1/2/3`) |
| spawn-point × patrol-point pairs | **1,284** |
| pairs beyond `alertArea` = 100.0 | **0** |
| max spawn → patrol distance, any map | **77.52 m** (`survivalworld_j`) |
| max spawn → spawn distance, any map | **85.58 m** (`survivalworld_f`) |

**A 100 m sphere centred on any spawn point contains the entire arena footprint.** `IsAlert()` is
therefore **true on the first evaluated tick of every wave, wherever the player stands.** The
mechanism named "ambush" does not, on these maps, implement an ambush: it implements a fixed
four-second delay. **`H-3` held as mechanism and is inert as behaviour.**

---

## § 6 — TARGET (e): BEHAVIOUR AFTER SPAWN

**The Lua gate, verbatim** (`game/events/survivalevent.lua`, inside `SurvivalEvent_SpawnNext`):

```lua
-- set the spawns to patrol if a patrol point group was provided
if waveEvent.proxy[id]:IsAmbush() == false && waveEvent.patrolPoint != nil then   -- L552
    waveEvent.proxy[id]:LinkPatrolPointGroup(waveEvent.patrolPoint)               -- L553
end
```

What it withholds is a **patrol route**, not the pursuit AI. Lap U decoded the transition
`ShouldFindEnemy → EnemyFound → DefaultEnemyFoundResponse → SetState("Pursue")`. This lap shows the
`ShouldFindEnemy` implementation Lap U found at RVA `0x00009350` (`mov al,1; ret`) is **ICF-shared
by fifteen states**: `Attack`, `DefendLeader`, `DodgeAttack`, `FollowLeader`, **`Idle`**,
`JumpAttack`, **`Move`**, `Patrol`, `Pursue`, `RepositionForAttack`, **`Return`**, **`Roam`**,
`Trapped`, `WaitToAttack`, **`Wander`**. The states that return `xor al,al` are the incapacitated
ones only (`Confused`, `GettingUp`, `Immobile`, `KnockedDown`, `Panic`, `Paralyze`, `Sleep`,
`Stunned`, `TakeHit`).

**⇒ An unpatrolled ambush body idles in a scanning state, acquires, and pursues exactly as
Lap U's pursue-all decode describes. `H-6` HELD — confirmed, not refuted.**

**`F-10`, the wave-advance interaction, with its uncertainty stated.**
`survivalevent.lua` L716 advances the wave only when every live proxy reports `AllKilled()`.
`ProxyAmbush::GetPlacedObjects` (`0x10354dd0`) appends the live placed ids (loop at `0x10354df4`)
**and then**, when the pending coords vector is non-empty (`0x10354e62`), also appends the
**not-yet-spawned** pending ids (loop from `0x10354e90`). Overriding the accessor specifically to
report unspawned bodies as outstanding is the shape of a wave-advance guard — but **I did not
locate the native body of the `AllKilled` Lua binding** (`UNREACHED-V2-1`), so the link is
**INFERRED-WITH-EVIDENCE and is not claimed as decoded.** It moves no number: by `F-4` + `F-5` the
ambush fires ~4 s into every wave regardless.

---

## § 7 — TARGET (f): THE PER-WAVE CONTRIBUTION

### 7.1 The release law (the condition function `H-7` pre-committed me to emitting)

```
burst fires on a tick iff:
      m_armed                                   (∃ Player within alertArea of the proxy — F-4: always)
  AND m_delayTimer <= 0                         (after Uniform[minDelayTime, maxDelayTime])
  AND m_spawnTimer <= 0                         (Uniform[minSpawnTime, maxSpawnTime] between bursts)
  AND len(m_pendingIds) > 0                     (filled ONCE by PoolComplete; never refilled — F-3)
  AND n_live <= spawnThreshold                  (n_live = |placed ∧ Character::IsAlive()|)

n_released = min( UniformInclusive(minGroupSize, maxGroupSize), len(m_pendingIds) )
```

**With the decoded shipped values `minGroupSize = maxGroupSize = 30`, `spawnThreshold = 15`,
`delay = 4000 ms`, `interval = 3000 ms`, and a one-shot queue whose largest resolution in the band
is 7, this condition function collapses to a constant.** The `n_live <= 15` clause and the 3.0 s
interval can only bite if the queue survives a burst; it cannot, because `30 > 7`. **I state the
collapse rather than hiding the function, and I state the function rather than hiding the collapse.**

### 7.2 The replacement table (supersedes Lap V § 6.1's exposure table)

| global wave | tier-16 wave | p05 proxy | alts | **E[bodies]** | envelope | Lap V § 6.1 "floor" | Δ | arrival |
|---|---|---|---:|---:|---|---:|---:|---|
| **151** | 1 | `proxy_w01_p05a` | 1 | **4.5** | 4 – 5 | 4.5 | **0.0** | wave start **+ 4.000 s** |
| **152** | 2 | `proxy_w02_p05a` | 1 | **3.0** | 3 – 3 | 3.0 | **0.0** | + 4.000 s |
| **153** | 3 | `proxy_w03_p05a` | 1 | **4.5** | 4 – 5 | 4.5 | **0.0** | + 4.000 s |
| **154** | 4 | — none declared — | – | **0** | – | – | – | – |
| **155** | 5 | — none declared — | – | **0** | – | – | – | – |
| **156** | 6 | `proxy_w06_p05a` | 3 | **7.0** | 7 – 7 | 7.0 | **0.0** | + 4.000 s |
| **157** | 7 | `proxy_w07_p05a` | 3 | **3.0** | 3 – 3 | 3.0 | **0.0** | + 4.000 s |
| **158** | 8 | `proxy_w08_p05a` | 2 | **3.0** | 3 – 3 | 3.0 | **0.0** | + 4.000 s |
| **159** | 9 | `proxy_w09_p05a` | 2 | **1.0** | 1 – 1 | 1.0 | **0.0** | + 4.000 s |
| **160** | 10 | — none declared — | – | **0** | – | – | – | – |
| | | | | **26.000** | | 26.000 | **0.000** | |

*(Each wave's alternatives all carry `pool_weight = 100.0` and identical `e_bodies`, so the
weighted pick is unambiguous. Envelopes and expectations are Lap V's decoded count model, carried
by citation, not re-derived.)*

**Nothing is conditional on runtime state.** The only decode-driven change to the roster picture is
**temporal**: the p05 contingent is absent for the first 4.000 s of each declaring wave and then
arrives all at once.

**Wave 160 — the wave the run's grade turns on — declares no p05 and is untouched by this lap, as
Lap V already stated.**

---

## § 8 — THE PRE-REGISTERED HYPOTHESES, GRADED HONESTLY

| id | prediction | grade | note |
|---|---|---|---|
| **`H-1`** | threshold counts the ambush's OWN live placed objects, not players/kills/distance | **HELD** | § 2. `Character::IsAlive` at `Monster` vt `+0x22c`. |
| **`H-1a`** | evaluated per tick inside `UpdateSelf(int)` | **HELD** | `0x103545f9`. |
| **`H-1b`** | "live < threshold ⇒ place" (strict/non-strict not pre-committed) | **HELD, exact form now stated** | `place iff live <= threshold`, unsigned `ja` on the negation. |
| **`H-2`** | one object per invocation ⇒ a **trickle** at 3.0 s | **REFUTED** | Per-invocation half held; the operative claim is wrong. It is a **burst of 30 in one tick**. |
| **`H-3`** | `alertArea` is a radius, read by `IsAlert`, arming the ambush; delay = arming → first placement | **HELD (mechanism) / INERT (behaviour)** | § 5. Exactly the predicted mechanism; 100 m covers the arena, so it never gates. |
| **`H-4`** | `min/maxGroupSize` bounds **placed bodies** | **REFUTED** | It is a per-burst **release count**. |
| **`H-4` (2nd half)** | same `ProxyPool` machinery ⇒ Lap V resolver + `F-8` `limitN` cap apply | **HELD** | § 3, `pool+0xb0`. |
| **`H-4alt`** | groupSize is not a body count; bodies still governed by the pool | **HELD** | The pre-registered alternative is the right one. |
| **`H-5`** | placement is proxy-local, not player-relative | **HELD** | § 5; the only player read in the class is `IsAlert`. |
| **`H-6`** | ambush bodies pursue per Lap U's decode | **HELD** | § 6; 15 scanning states share the `mov al,1` stub. |
| **`H-7`** | if `H-1` holds, emit a **condition function**, not a scalar | **HELD IN FORM** | Function emitted (§ 7.1) — and it collapses to a constant, which I did not anticipate. Both are reported. |
| **`H-8`** | decoded p05 **ceiling exceeds** Lap V's floor on **all seven** waves | **REFUTED 0/7** | Ceiling **equals** floor, seven for seven. See `F-7`. |

**Five held, one held-in-form-with-a-caveat-I-did-not-foresee, three refuted.** The refutations are
the informative ones: I expected a large hidden spawner and the bytes describe a four-second timer.

---

## § 9 — DEFECT TABLE

| id | defect | disposition |
|---|---|---|
| **`D-V2-1`** | **Method defect in the Lap S PE reader (`pm4s_pe_2026_08_14.py`).** Its export dictionary maps the `??_7X@GAME@@6B@` and `??_7X@GAME@@6BObject@1@@` vtable data symbols onto colliding RVAs, so **vtable bases read from the export table are unreliable** (it reported the `Proxy` and `ProxyAmbush` primary vtables at the same address). Self-caught when slot `+0x1fc` resolved to a five-parameter method being invoked with two arguments. | **REPORTED, NOT REPAIRED.** Corrected in-lap by the empirical slot-0 convention, corroborated three ways (§ 2). The reader is left byte-identical because Laps S/T/U/V were computed with it and **none of them read a vtable** — repairing it now would perturb a frozen instrument for no gain (NOTE-9). Route to the conductor if any future lap needs vtable reads from that reader. |
| — | **No arithmetic defect was found this lap.** Lap V's p05 numbers reproduce exactly. | — |

**A correction, not a defect.** Lap V § 6.1 published the p05 numbers as *"a FLOOR, not an
estimate, until `F-3M-1` is ruled"*, and § 7.2 forbade treating them as decode-complete. That was
the correct posture under the then-standing HALT rule and it is not an error. **It is now
retired:** the numbers are exact. Anything downstream still treating 4.5 / 3.0 / 4.5 / 7.0 / 3.0 /
3.0 / 1.0 as lower bounds should stop.

---

## § 10 — UNREACHED CENSUS (honest; nothing here is estimated)

| id | what | status |
|---|---|---|
| **`UNREACHED-V2-1`** | **the native body of the `AllKilled` Lua binding.** The binding strings live in `Grim Dawn.exe` (`AllKilled` @ `0x66b75c`, `IsAmbush` @ `0x66b784`, `LinkPatrolPointGroup` @ `0x66b76c`) but **no dword reference to any of them exists in any of the three shipped modules**, so the binding table's construction was not reached. `F-10` is therefore **INFERRED-WITH-EVIDENCE**, not decoded. Moves no number. |
| **`UNREACHED-V2-2`** | **the engine tick rate / the `dt` units of `UpdateSelf(int)`.** The timers are unambiguously **milliseconds** (`Load` multiplies seconds by `1000.0` and truncates), so the 4.000 s is wall time; but the number of ticks between `Run()` and the arming tick is **≥ 1** and not decoded. The arrival offset is therefore `4.000 s + O(1 tick)`. |
| **`UNREACHED-V2-3`** | **whether `Proxy::ResetSettings` (which zeroes the run latch) is ever invoked in the Crucible.** Not needed: the Lua creates a fresh proxy per wave (L548), so the latch is per-wave regardless of the answer. Named, not claimed. |
| **`UNREACHED-V2-4`** | **the placement geometry *inside* the 8 m disc** — `Proxy::SelectPoolLocations`' internals (navmesh sampling, spacing, collision rejection). Only the disc radius (`placementExtents = 8.0`) and the fact that it is proxy-local are decoded. |
| **`UNREACHED-V2-5`** | **the `true, 2` trailing arguments to `World::GetEntitiesInSphere`** (a `bool` and an `EntityListType`). They may pre-filter the query. The **downstream** `Player` RTTI filter is decoded, so `IsAlert`'s semantics are safe either way, but the pre-filter is not read. |
| **`UNREACHED-V2-6`** | **which of the 20 arena maps the referent's tier-16 block used.** Not needed: the `F-4` verdict (`alertArea` covers the footprint) holds on **all 20**, so no map choice can change it. |
| **`UNREACHED-S7`** | **the referent-side `bonusSpawnStatus` election.** Untouched by this lap — it is Lap W's (the `R-V-1` video route). Carried, not re-opened. |

**Closed by this lap:** Lap V's **`UNREACHED-V5`** — the element type of `[ProxyPool + 0xb0]` is
`unsigned` (entity IDs). See `F-9`.

---

## § 11 — HAND-OFF, SHAPED FOR I-22 (gamora), WITH DO-NOTs

### 11.1 What to fold

1. **The p05 roster numbers do not change. At all.** 151→4.5, 152→3.0, 153→4.5, 156→7.0, 157→3.0,
   158→3.0, 159→1.0; band p05 total **26.000**. Lap V's § 4.1 band totals — decoded p06-OFF
   **172.083**, decoded p06-ON **197.083** — are now **DECODE-COMPLETE**, and Lap V § 7.2's
   "DO NOT treat § 3's numbers for waves 151/152/153/156/157/158/159 as decode-complete" is
   **RESCINDED by this lap**.
2. **The one thing to add is temporal.** On the seven declaring waves the p05 contingent is
   **absent for the first 4.000 s** and then arrives **all at once** at the p05 point, inside the
   same 8 m placement disc as any other proxy. If the sim models arrival timing (Lap T), that is a
   one-line offset on one spawn point.
3. **Ambush bodies carry no patrol-point group but do pursue** (§ 6). If the sim models patrol
   routing, p05 bodies skip it and head for the player from spawn.
4. **`minGroupSize = 30` and `spawnThreshold = 15` are DECODED-INERT in this band. Do not model
   them.** Model them only if a future lane has a p05 pool resolving **> 30** bodies, in which case
   § 7.1's condition function is the law to implement.
5. **Lap V's `F-8` `limitN` cap, `NO_OP_ON_EMPTY`, the operator order and the champion-first
   ordering all apply unchanged to ambush bodies** — the ambush consumes the identical pool
   resolution (§ 3).

### 11.2 DO-NOT

* **DO NOT add bodies for the ambush. It adds exactly zero.** The single most likely misreading of
  `minGroupSize = 30` is "thirty extra monsters." The bytes say it is a release-batch size against
  a queue that never holds more than seven.
* **DO NOT model `spawnThreshold` as a difficulty term or a refill mechanic.** It is a burst
  suppressor on a queue that is filled once (`F-3`), and its loader default is 10,000 — the field
  is a ceiling by design.
* **DO NOT model `alertArea` as a "the player must walk over there" gate.** Decoded arena-covering
  on all 20 maps (`F-4`). Modelling it as a positional trigger would invent a mechanic the game
  does not have.
* **DO NOT fold `F-10` (wave-advance gating) as a hard mechanism.** It is INFERRED-WITH-EVIDENCE
  (`UNREACHED-V2-1`) and, because the ambush auto-fires at ~4 s, it changes nothing. Folding it as
  decoded would put a real inference behind a false confidence.
* **DO NOT re-open waves 154, 155, 160.** They declare no p05. **Wave 160 remains clean of this
  mechanism**, exactly as Lap V said.
* **DO NOT read the `+4.000 s` as exact-to-the-tick.** It is `4.000 s + O(1 tick)`
  (`UNREACHED-V2-2`). Quote the 4.000 s; carry the tick as slop.
* **DO NOT quote `H-8` as if it had been a neutral observation.** It was my blind directional bet
  and it lost 0/7 (`F-7`). If a downstream doc cites this lap's per-wave table, it should cite it
  as *unchanged from Lap V*, not as *newly discovered*.

---

## § 12 — DIGESTS (full 64 hex throughout, `R-PM4-55 part 2`)

### 12.1 Outputs of this lap

| artefact | sha256 |
|---|---|
| `PREREGISTRATION.md` (committed alone, `32b63c70`) | `d3653ba634cd48a55bc3200674e889e06500749919b911f0095424beae7fe8e9` |
| `pm4v2_ambush.json` | `cb3f7f571c5bf25849814627b02d2c936465cd38393c95342bfb4baf99e8d010` |
| `pm4v2_contribution.json` | `9c3b3db20ac8ce2b0f3a3b31adb6161b68990518fcc20ec25f8c306c95a8ac05` |
| `pm4v2_disasm.txt` | `ec787caab014d5e14b5499b618653c82acfbc0b081e4849b24d9cac855626fe4` |
| `pm4v2_findings.md` | *(this file — digest reported in the return message and in `pm4v2_digests.json`)* |
| `pm4v2_digests.json` | *(covers all of the above; recomputed at commit)* |

### 12.2 Inputs, pinned in `PREREGISTRATION.md § 1` and verified at instrument start (HALT on mismatch; none fired)

| input | sha256 |
|---|---|
| `edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `edition-III/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `edition-III/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `edition-III/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `edition-III/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `edition-III/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `edition-III/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `edition-III/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `edition-III/mods/survivalmode/resources/Scripts.arc` | `47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009` |
| `edition-III/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |
| `lap-v/pm4v_findings.md` | `5450e1567fe58337827c20719ec477ee56a40351cbd7c49ab823d0896ca1b895` |
| `lap-v/pm4v_roster_arithmetic.csv` | `991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c` |
| `lap-v/pm4v_prediction.json` | `450d52c9c5c430b528d1e2435760ff2ed45dec60c53a3b1981c20cc9701e275b` |
| `lap-u/pm4u_geometry_v3.csv` | `5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2` |
| `lap-u/pm4u_pursue_decode.json` | `6efd193aaa88158154beda71a723dbc70feda5f963ad470437137af92f98d733` |

Both binary digests are **byte-identical to Laps U and V's pinned values**, so `F-1`–`F-9` were
decoded out of the same bytes that decided `U-T-1` and Lap V's `F-3`–`F-8`.

### 12.3 Instruments

| instrument | sha256 | role |
|---|---|---|
| `research/scripts/pm4v2_ambush_2026_08_15.py` | `b2cbf68a000227b058ed7957a6aa6a2279b7c2c8d23980b9cb592555cf8e4370` | I-V2-1…4 — pin verification, binary decode, record census, geometry, contribution |
| `…/pm4s_pe_2026_08_14.py`, `…/gd_arz_adapter_2026_07_24.py`, `…/gd_arc_reader_2026_07_26.py` | *unchanged* | carried readers, **byte-identical** (NOTE-9; see `D-V2-1`) |

*Lap V-2 closed by legolas (UNKNOWN-RESEARCHER), 2026-08-15. Read-only throughout; nothing outside
this notes directory and `research/scripts/` was written.*
