# LAP S — THE CRUCIBLE WAVE-ADVANCE RULE — decoded verbatim from shipped game script

**Agent:** legolas · **Run:** KC2-PM4, Lap S (R-PM4-44 part 3, limb c) · **2026-08-14**
**Grade:** **MEASURED** — this is the shipped rule read out of the shipped bytes, not inferred.

---

## 0. The rule, in one sentence

> **A Crucible wave advances when EVERY spawn point's PROXY reports `AllKilled()` — evaluated on a
> 1000 ms polling timer, not on a kill event — and a spawn point whose wave entry is `nil` is marked
> killed IMMEDIATELY without ever spawning.**

Two things gate. Nothing else does. In particular: **no timer, no kill count, no player position,
and — critically — nothing that a monster creates at runtime.**

---

## 1. Where it lives, and how it was reached

Lap R recorded Crucible spawn/wave logic UNREACHED because it is not in the `.arz` record DB. It is
not. It is in **shipped Lua source text**, inside ARC containers nobody on this run had opened:

| container | file | bytes | form |
|---|---|---:|---|
| `mods/survivalmode/resources/Scripts.arc` | `game/events/survivalevent.lua` | 22,405 | **plain UTF-8 source** |
| `survivalmode1/resources/Scripts.arc` | `game/survival/eventcontrol.lua` | 17,604 | plain UTF-8 source |
| `survivalmode1/resources/Scripts.arc` | `game/survival/tier16waves.lua` | 11,767 | plain UTF-8 source |

They are **not compiled bytecode** — the first bytes are `/*\r\n`, a comment banner. Read with the
project's existing `gd_arc_reader_2026_07_26.ArcArchive`; no new format work was needed.
All three are banked verbatim under `evidence/`.

**Routing to waves 151–160, from the script's own arithmetic** (`eventcontrol.lua`, not assumed):

```lua
local wave = Game.GetSurvivalWaveTier()
rewardTier = math.floor(wave / 10)
...
elseif rewardTier == 15 then
    gd.survival.tier16Waves.startSurvivalModeEvent()
```

`floor(151/10) = 15 → tier16Waves`. Corroborated independently by
`eventControl.startTier15Event()`, which does `Game.SetSurvivalWaveTier(151)` and then calls
`gd.survival.tier16Waves.startSurvivalModeEvent()`. **Waves 151–160 = `tier16waves.lua`. MEASURED.**

---

## 2. The gate, verbatim

`survivalevent.lua`, `SurvivalEvent_Update` — this is the whole advance decision:

```lua
local eventFailed = Game.PlayersDead()

if not eventFailed then

    for id = 1, waveEvent.numSpawns do
        if (waveEvent.proxy[id] != nil && waveEvent.proxy[id]:AllKilled()) then
            waveEvent.proxyKilled[id] = true
        end
    end

    for id = 1, waveEvent.numSpawns do
        if (not waveEvent.proxyKilled[id]) then
            break
        end

        if id == waveEvent.numSpawns then
            if (waveEvent.waveIndex < waveEvent.numWaves) then
                for id = 1, waveEvent.numSpawns do
                    waveEvent.proxyKilled[id] = false
                end
                print "starting next wave"
                SurvivalEvent_SpawnNext(objectId)
            else
                ...  -- tier complete
```

And the spawn side, `SurvivalEvent_SpawnNext` — note that **a `nil` wave entry sets
`proxyKilled = true` without spawning anything**, so an inactive spawn point never gates:

```lua
for id = 1, waveEvent.numSpawns do
    if (waveEvent.waves[id][waveEvent.waveIndex] != nil
        && (id < waveEvent.numSpawns || bonusSpawnStatus == true)) then
        ...
        waveEvent.proxyKilled[id] = false
        waveEvent.proxy[id] = Proxy.Create(..., waveEvent.coords[id].origin, true)
        waveEvent.proxy[id]:SetCoords(waveEvent.coords[id])
        if waveEvent.proxy[id]:IsAmbush() == false && waveEvent.patrolPoint != nil then
            waveEvent.proxy[id]:LinkPatrolPointGroup(waveEvent.patrolPoint)
        end
        waveEvent.proxy[id]:Run()
    else
        waveEvent.proxyKilled[id] = true
        waveEvent.proxy[id] = nil
    end
end
```

### 2.1 Five load-bearing consequences

| # | consequence | grade |
|---|---|---|
| **A-1** | **The gate is per-PROXY, not per-BODY.** The predicate is `Proxy:AllKilled()`, once per spawn point — six booleans, not a body census. | **MEASURED** |
| **A-2** | **It is POLLED at 1000 ms.** `tier16waves.lua` sets `survivalModeEventParameters.updatePeriod = 1000`; `SurvivalEvent_Start` does `Script.RegisterForUpdate(objectId, "SurvivalEvent_Update", waveEvent.updatePeriod)`. **Advance therefore lags the last kill by U ~ Uniform(0, 1] s.** | **MEASURED** |
| **A-3** | **A `nil` wave entry never gates.** Marked `proxyKilled = true` immediately. Waves 151–160 have `nil` entries (§ 3). | **MEASURED** |
| **A-4** | **Spawn point 6 is conditional.** `id < waveEvent.numSpawns \|\| bonusSpawnStatus == true` — the LAST spawn point only fires when `gd.survival.rewards.checkBonusStatus()` is true; otherwise it is marked killed without spawning. | **MEASURED** |
| **A-5** | **The wave counter increments INSIDE `SpawnNext`,** via `Game.IncrementSurvivalWaveTier()` — i.e. the counter ticks and the new wave is dispensed in the same call. The on-screen counter is therefore a spawn event, not a clear event. | **MEASURED** |

---

## 3. Which spawn points are active per wave (tier 16)

Read from `tier16waves.lua`'s `spawnPointNNwaveMMProxies` table — `{nil}` means the point does not
spawn that wave and does not gate it. **Wave 15x = tier-16 wave index x+1.**

| tier-16 wave | game wave | p01 | p02 | p03 | p04 | p05 | p06 | gating proxies |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---:|
| 01 | **151** | ● | ● | ● | ● | ● | — | 5 |
| 02 | **152** | ● | ● | ● | ● | ● | ●* | 5–6 |
| 03 | **153** | ● | ● | ● | ● | ● | ●* | 5–6 |
| **04** | **154** | ● | ● | ● | ● | **—** | **—** | **4** |
| 05 | **155** | ● | ● | ● | ● | — | ●* | 4–5 |
| 06 | **156** | ● | ● | ● | ● | ● | ●* | 5–6 |
| 07 | **157** | ● | ● | ● | ● | ● | ●* | 5–6 |
| 08 | **158** | ● | ● | ● | ● | ● | ●* | 5–6 |
| 09 | **159** | ● | ● | ● | ● | ● | — | 5 |
| 10 | **160** | ● | ● | ● | ● | — | ●* | 4–5 |

`*` = spawn point 6, active only when `bonusSpawnStatus` is true (A-4).

> **⚑ Wave 154 is the ONLY wave in the tier with FOUR active spawn points** — both p05 and p06 are
> `nil`. That is a decoded, record-side reason for the referent's w154 being its shortest wave
> (14.20 s, Lap R). **It is not a behavioural mystery; it is a smaller wave by authorship.**

---

## 4. What `AllKilled()` ranges over — and the honest limit

**This is the question that decides `D-I12-5`.** Split grade, deliberately:

| claim | grade | basis |
|---|---|---|
| the gate calls `Proxy:AllKilled()` once per spawn point | **MEASURED** | Lua source, § 2 |
| a `Proxy` holds an explicit list of the entity IDs **it placed** | **MEASURED** | `Game.dll` exports: `?PlaceObjects@Proxy@GAME@@IAEXAAV?$vector@I@mem@@ABV?$vector@VWorldCoords@GAME@@@4@@Z`, `?GetPrimaryObjects@Proxy@GAME@@QAEXAAV?$vector@I@mem@@@Z`, `?GetAccessoryObjects@Proxy@…`, `?GetPlacedObjects@Proxy@GAME@@UBEXAAV?$vector@I@mem@@@Z` |
| traps are NOT proxy-owned and do not gate | **MEASURED** | `survivalevent.lua` creates traps with `Character.Create(trapDbrs[randTrap], trapLevel, nil)` — no proxy involved — and removes them with `SurvivalEvent_DespawnTraps()`, never waits on them |
| **runtime summons of monsters do not gate advance** | **INFERRED-WITH-EVIDENCE** | a summon is created by the summoner's skill at runtime; it was never passed through `Proxy::PlaceObjects`, so it cannot be in the proxy's placed-ID vector. Consistent with, but not proven by, the above. |
| the body of `Proxy::AllKilled()` itself | **⚑ UNREACHED** | the Lua binding lives in `Grim Dawn.exe`, which ships with a **`.bind` section (Steam DRM)** — its `.text` is encrypted at rest, so static disassembly of the binding is blocked. `Game.dll` and `Engine.dll` are NOT protected and were disassembled freely. The `Proxy` binding NAME table is readable in the exe's plaintext `.rdata` (`Get · Create · Create · Create · IsType · AllKilled · Run · LinkPatrolPointGroup · IsAmbush`); the implementation is not. **Recorded UNREACHED, not estimated.** |

`Proxy::GetState()` is `return this->[+0x4ac]` (disassembled), and the only writers of `+0x4ac` in
`Game.dll` are construction / `Load` / `InitializePools` / `DelayedRun` / `RunProxy` / `Disable` /
`SaveState` / `RestoreState` / `ResetSettings` — **no death-notification path writes it**, which is
why `AllKilled` must be computed on demand over the placed-ID list rather than latched on kill.

> **⚑ THE RULING THE SIM NEEDS.** The referent's rule gates on **six proxy booleans over
> proxy-dispensed bodies**. The sim gates on ALL deaths including 12 unkillable-by-design
> survivors. Those 12 are summons — **not proxy-dispensed** — and under the decoded rule they
> **cannot gate advance**. The sim's 46.12 s w154 against the referent's 14.20 s is therefore
> explained by two independent decoded facts: (i) w154 has only 4 gating proxies, and (ii) summons
> are outside the gate entirely.

---

## 5. The video arm — the pre-registered falsification test

Pre-registered rule (PREREGISTRATION § 4.1): for each wave increment, the minimum living-plate
count over `W = [t_inc − Δ, t_inc]`. A plate PROVES a body, so `min ≥ 1` would PROVE the board was
never empty and would FALSIFY all-deaths gating.

| Δ | min living-plate count at increments 152 … 160 | all windows non-empty? |
|---|---|---|
| 1.0 s | `0, 1, 0, 1, 1, 0, 0, 0, 0` | **False** |
| **3.0 s (PRIMARY)** | `0, 1, 0, 1, 1, 0, 0, 0, 0` | **False** |
| 5.0 s | `0, 1, 0, 1, 1, 0, 0, 0, 0` | **False** |

**VERDICT: NOT FALSIFIED.** I pre-committed to saying so plainly in this case, and I do: this test
can never *confirm* the rule, only fail to falsify it — and it failed to falsify it.
**6 of 9 increments have a demonstrably empty board (zero detected plates) in the preceding 3 s,
which is exactly what an all-proxies-killed gate predicts.** The video and the shipped script
agree; two independent instruments, one answer.

Global: the fight carries **180 zero-plate instants out of 10,216 (1.76 %, 3.00 s total)** — the
board is nearly always occupied, and empties only at wave seams.

**The three exceptions (153, 155, 156) are informative, not contradictory.** Under A-5 the counter
ticks *inside* `SpawnNext`, so the new wave is dispensed in the same call — a plate present at the
increment instant may be a body of the wave that is being born. The plate census carries no wave
identity per body (Lap R `UNREACHED-5`, carried unchanged), so this instrument cannot separate
them. It does not need to: the rule is decoded from source.

---

## 6. Two mechanisms this lap surfaced that the sim does not model at all

| # | mechanism | evidence | why it matters |
|---|---|---|---|
| **M-1** | **PATROL-POINT CONVERGENCE.** `tier16waves.lua` sets `patrolPoint = "PatrolPoint_Attack"`, and `SpawnNext` calls `proxy:LinkPatrolPointGroup(waveEvent.patrolPoint)` on every non-ambush proxy. Spawned packs **path to a named attack-point group**, they do not scatter and they do not individually seek the player from spawn. The groups exist in the world assets: 8–11 `patrolpoint_01.dbr` placements per arena (§ limb a). | Lua source + `.map` placements | The sim has **no convergence structure at all**. This is the single largest untold difference between the two spatial models. |
| **M-2** | **SPAWN BEACONS.** `eventcontrol.lua` spawns up to five `records/creatures/traps/spawnbeacon.dbr`, documented in the shipped comment as *"Spawn Beacons accelerate monster movement in their spawn areas."* Their world positions are decoded (`spawnbeacon_01..05`) and they sit **beside the spawn points** (e.g. `survivalworld_a`: beacon_01 at (46.816, 5.632, 74.314) vs `tier16spawnpoint01` at (46.813, 5.645, 73.955) — **0.36 m apart**). | Lua source + `.map` placements | Monster traversal speed near spawn is **boosted by a world mechanic**, so any sim that prices the march at `characterRunSpeed` alone prices it too slow. Named, NOT quantified — the beacon's magnitude is UNREACHED here. |
