# KC2-PM4 · LAP AA — FINDINGS · THE REFERENT'S SPAWN STRUCTURE

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Commissioned by:** `R-PM4-67 part 7` · **Date:** 2026-08-16
**Pre-registration:** `prereg.md`, sha256 `ff7c25a34b568d8b79d1ccbacbaaf4b8c3b7ee23c9de52cbcc6aa866394a5611`,
**committed ALONE in `ba368773` before the instrument existed.**
**Instrument:** `agentic_orchestration/research/scripts/pm4aa_spawn_structure_2026_08_16.py`.
**Determinism ×2:** the instrument ran twice end to end; **all seven emitted artifacts
byte-identical.** 16 pins asserted EXACT, 9 recorded; no HALT fired.
**Law 3 honoured:** no sim outcome, scorecard, occupancy number or I-25 artifact was opened while
this lap ran. Nothing here is a prescription.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

A Crucible wave does **not** have an arrival schedule on the spawn side. Every active spawn point
of a wave is dispensed inside **one Lua `for` loop, in one call**, and the base-`Proxy` release path
underneath it is **synchronous end to end** — `DelayedRun` (5 instructions, no timer) tail-jumps
`RunProxy`, which calls `SelectPoolLocations`, which calls `PoolComplete`, which ends in a **direct
call** to `PlaceObjects`, which walks the whole id vector in **one loop** handing each body to
`World::AddEntity`. There is **no timer, no queue, and no per-body deferral anywhere on that path**,
and a census of all **54** tier-16 wave-proxy records over **41** distinct field names finds **no
release-rate, batch-size, interval or stagger field of any kind** — the only timing-named fields in
the band are `delayedRun` (a boolean latch, not a duration) and the four `ProxyAmbush` timers that
Lap V-2 already reduced to a flat `+4.000 s` on spawn point 5. **The referent releases each wave as
one simultaneous event.** What it *does* have is two things the sim's spawn model does not: the
pack's bodies are scattered by a **navmesh-validated polar sample that is uniform in RADIUS, not in
area** (`θ = rand()·2π/32767`, `ρ = rand()/32767 × placementExtents`, so density falls as `1/ρ` and
the mean offset is `E/2 = 4.0 m`, not `2E/3 = 5.33 m`), and — the lap's real find — **every body
that acquires the player beyond `alertDistance = 6.0 m` is pushed into an `AlertBeforePursue`
animation state before it marches.** Crucible spawn points sit **29–39 m** from the attack ring, so
that gate is satisfied for essentially every body in the band. `UNREACHED-U3` is **CLOSED**: the
alert state is entered, by a decoded path, on a decoded condition. Its **duration is an animation
length and is UNREACHED.** ⚑ **The arrival spacing the run is hunting is not authored at the spawn
point. On the referent side it is created between spawn and march, per body.**

---

## 1 — VERDICT PER FORK

**Fork (d) is stated first and bounds every fork-(a) number, as `prereg.md § 1` required.**

| fork | verdict | one-line basis |
|---|---|---|
| **(d) ARENA** | **name DECODED · map identity UNREACHED, decoy set 10 → 3** | The referent's own HUD reads **`Crucible of the Dead`** on 89 sampled frames (`pm4n_fct_events.csv`, pinned) = `tagSurvivalArena_01` (`ED/resources/Text_EN.arc :: tags_uimain.txt`); exactly **3 of the 10** shipped arena maps carry that tag (`survivalworld_a/_b/_e`); the tag→map binding lives in `Grim Dawn.exe` `.text`, which ships a **`.bind` (Steam DRM)** section. Difficulty tier **`Gladiator`** attested on 91 frames from the same artifact. |
| **(a) WHERE** | **DECODED** | 6 authored spawn points per arena, 4–6 active per wave; within-pack scatter decoded to the instruction — `NavManager::FillPointSet` + a polar rejection sampler at `Engine.dll 0x100edf30`, `placementExtents = 8.0 m`, per-body clearance `0.25 m`, 100-attempt cap, random facing over `2π`. |
| **(b) WHEN** | **DECODED (negative)** | The full release chain disassembled; **zero timers**; 54/54 records carry no schedule field; per-wave batch composition imported by identity from Lap V. **Simultaneous release, one call, all points.** |
| **(c) BETWEEN** | **DECODED (mechanism + condition) · duration UNREACHED** | `DefaultEnemyFoundResponse` sets `"Pursue"`, then — if `d > gameengine.alertDistance = 6.0` **and** `15.0 > AngerManager::GetAngerDiff(enemy)` — calls `AddTemporaryState("AlertBeforePursue")`, whose `OnBegin` plays `AnimationSet_Type 0x21` at speed `1.0f`. |

---

## 2 — FORK (d) — ARENA IDENTITY, AND THE BOUND IT PUTS ON EVERYTHING ELSE

### 2.1 What the referent itself attests

`pm4n_fct_events.csv` (Lap N, pinned, sha256 `cf8ed218…24ce2`) is an OCR of the referent's own HUD.
Two strings recur across the fight window:

| string | frames | HUD position | meaning |
|---|---:|---|---|
| `Crucible of the Dead` | **89** | `(0.892, 0.971)` — top right | the **area name** |
| `Gladiator` | **91** | `(0.006, 0.974)` — top left | the **Crucible difficulty tier** |

### 2.2 The tag table, complete

`ED/resources/Text_EN.arc :: tags_uimain.txt` declares eleven entries. Published whole so that the
match is checkable rather than asserted:

| tag | value | | tag | value |
|---|---|---|---|---|
| `_01` | **Crucible of the Dead** | | `_06` | Crucible of the Legion |
| `_02` | Crucible of the Deeps | | `_07` | Crucible of the Bog |
| `_03` | Crucible of the Sands | | `_08` | Crucible of the Woods |
| `_04` | Crucible of the Grove | | `_09` | Crucible of the Stars |
| `_05` | Crucible of the Void | | `_10` | Crucible of the Crags |
| | | | `Random` | Random |

**`Crucible of the Dead` = `tagSurvivalArena_01`, uniquely.**

### 2.3 ⚑ The decoy set, ENUMERATED (`D-Z-1`)

Ten arena maps ship. Which ones carry `tagSurvivalArena_01`:

| map | arena tags carried | candidate for the referent? |
|---|---|:-:|
| `survivalworld_a.map` | `_01`, `_02` | **YES** |
| `survivalworld_b.map` | `_01` | **YES** |
| `survivalworld_e.map` | `_01`, `_02`, `_05` | **YES** |
| `survivalworld_c/d/f/g/h/i/j` | `_03` / `_04` / `_06` / `_07` / `_09` / `_10` / `_08` | no |

`Grim Dawn.exe` `.rdata` carries two ordered arrays: a **map list** of ten
(`a,b,c,d,e,f,g,**j,h,i**` — note `j` before `h`) and the **arena dropdown**
(`Random, _01, _03, _04, _05, _06, _07, _08, _09, _10` — **`_02` is absent from the dropdown**).
The two arrays are of different lengths and different orders, so **no positional
map↔tag correspondence can be read off them**, and I decline to invent one.

> **VERDICT.** The referent's arena is **named**, and its **file identity is UNREACHED**: three of
> ten maps survive. The selector that binds a chosen tag to a `.map` is in the exe's `.text`, and
> the exe ships a `.bind` (Steam DRM) section — re-confirming Lap S's block from my own seat.
> **This bounds every fork-(a) distance below.**

### 2.4 The bound, quantified rather than shrugged at

Geometry imported by identity from Lap U's repaired artifact and **resolved through the mod stack**
(`survivalmode3` wins — see `D-AA-4`), 6 spawn points per map:

| quantity | **candidate arenas only** (a/b/e, n=18) | all ten arenas (n=60) |
|---|---|---|
| spawn → patrol centroid, median | **33.863 m** (min 0.112, mean 29.195, max 38.774) | 35.595 m (0.325–48.070) |
| spawn → nearest patrol point, median | **16.104 m** (min 1.862, max 21.146) | 16.431 m |
| attack-ring max extent, median | **40.049 m** (33.176–48.488) | 45.707 m |
| `placementExtents` | **8.0 on every one** | 8.0 on every one |

**The unreached arena identity costs at most ≈ 5 m of median march distance**, and costs nothing at
all on `placementExtents`. That is the honest size of the hole.

---

## 3 — FORK (a) — WHERE

### 3.1 The three fields that shape a release, and only those

`Proxy::Load` (`Game.dll 0x10350f90`), operands printed, three-start convergence asserted:

| `.dbr` field | member | loader default | shipped value, all 54 tier-16 records |
|---|---|---|---|
| `placementExtents` (literal `0x10569268`) | `[this+0x410]` | `2.5f` (`0x40200000`) | **8.0** |
| `chanceToRun` (literal `0x1056925c`) | `[this+0x3e0]` | `0.0f` | **100.0** |
| `delayedRun` (literal `0x10569250`) | parks state latch `[this+0x4ac] = 1` | `false` | **True** |

### 3.2 ⚑ THE SCATTER LAW, DECODED TO THE INSTRUCTION

`Proxy::SelectPoolLocations` (`0x103526e0`) builds a float vector of **`0.25f` per body**
(`0x3e800000`, one push per id) and calls
`Engine.dll!NavManager::FillPointSet(out, origin, placementExtents, radii, false, true)`.
The `true` selects the sampler at **`Engine.dll 0x100edf30`**, which per body does:

```
for (attempt = 0; attempt < 100; ++attempt) {          ; cmp esi, 0x64
    theta = (float)rand() * 0.00019175345369149f;      ; 0x102e03dc  == 2*pi / 32767
    rho   = (float)rand() * 3.0518509447574615e-05f    ; 0x102e03c8  == 1 / 32767
                          * placementExtents;          ; xmm2, the caller's extents
    x = cosf(theta) * rho + origin.x;                   ; __libm_sse2_cosf
    z = sinf(theta) * rho + origin.z;                   ; __libm_sse2_sinf
    ...navmesh poly lookup, then a clearance test against the per-body 0.25f radius...
    if (accepted) { WorldVec3::Translate; WorldVec3::PutOnFloor; return true; }
}
return false;                                           ; 100 attempts, then give up
```

`rand()` is the C runtime's (`api-ms-win-crt-utility-l1-1-0.dll!rand`, `RAND_MAX = 32767`); both
constants are the **exact** float32 of `2π/32767` and `1/32767`.

> **⚑ THE CONSEQUENCE, AND IT IS NOT COSMETIC.** The radius is drawn **uniform in ρ**, not uniform
> in area. Density therefore falls as `1/ρ`: with `placementExtents = 8.0` the **mean offset from
> the spawn point is `E/2 = 4.000 m` and the median is `4.000 m`**, where an area-uniform disc of
> the same radius would give a mean of `2E/3 = 5.333 m`. **A quarter of every pack is placed within
> 2.0 m of its spawn point.** A pack is centre-heavy, not evenly spread.

Two further structural facts on the same call path:

* **Facing is randomised per body** over `2π` (`0x40c90fdb = 6.2831855f`, `SelectPoolLocations`) —
  bodies do not spawn oriented toward the player.
* **Placement is nav-mesh constrained and can FAIL.** After 100 rejected attempts the sampler
  returns false. What `FillPointSet` does with a failure is **UNREACHED-AA-2** (below).

### 3.3 The point set itself

6 authored spawn points per arena on every complete map (Lap T's repaired census, imported); 4–6
active per wave (Lap S's table, unchanged); `placementExtents = 8.0` on all 54 tier-16 proxies.

---

## 4 — FORK (b) — WHEN

### 4.1 The release chain, end to end, with no timer in it

| step | site | what it does | timer |
|---|---|---|:-:|
| Lua `SurvivalEvent_SpawnNext` | `survivalevent.lua` **L539** | `for id = 1, waveEvent.numSpawns do` — **one loop over all six points** | — |
| | **L548** | `Proxy.Create(...)` per active point | — |
| | **L553** | `LinkPatrolPointGroup("PatrolPoint_Attack")` on every non-ambush proxy | — |
| | **L558** | `proxy:Run()` — **inside the same loop iteration** | — |
| `Proxy::DelayedRun` | `0x10351d10` | **12 instructions**: `if (state==1) { state=0; TAIL-JMP RunProxy; }` | **NONE** |
| `Proxy::RunProxy` | `0x10351d30` | one-shot latch; `chanceToRun` roll; `SelectPoolLocations` ×2; virtual `PoolComplete` (`vtbl+0x1fc`); latch → 6 | **NONE** |
| `Proxy::PoolComplete` | `0x10352580` | per-body proxy-parent stamping, then a **direct `call 0x10352af0`** | **NONE** |
| `Proxy::PlaceObjects` | `0x10352af0` | **one loop** over (ids × coords): `AddUniqueIdToEntity`, then `Engine.dll!World::AddEntity(entity, coords, true)` | **NONE** |

**Contrast, imported by identity:** `ProxyAmbush::PoolComplete` moves the same id vector into a
*pending* queue (`[this+0x4d0]`) and releases it after `Uniform[4000,4000] ms` (Lap V-2 `F-2`/`F-5`).
**The base `Proxy` does not queue** — the instrument asserted the absence (`queues_pending = False`).

### 4.2 The latch, enumerated — why "the Lua's `:Run()` reaches `DelayedRun`" is decoded, not assumed

The Lua↔native binding body is behind the exe's DRM. It does not need to be read. All 29 `imm32`
writes to `[reg+0x4ac]` in `Game.dll` are enumerated in `pm4aa_spawn_structure.json`; restricted to
the `Proxy` family they are: ctor → 0, `Load` → **1**, `InitializePools` → 3/4, **`DelayedRun` → 0**,
`RunProxy` → 5 or 6, `Disable` → 2, `ResetSettings` → 0. **`Proxy::DelayedRun` is the only exit from
state 1 in the module**, and `Proxy::UpdateSelf` only runs a proxy whose latch is already 0. A proxy
parked at 1 by `delayedRun = True` therefore cannot start by any other route.
*(The raw 29-row scan also captures unrelated classes that happen to have a member at `+0x4ac` —
published rather than filtered away, so the restriction is visible.)*

### 4.3 The field census — P-AA-1 as a census, not an impression

54 tier-16 wave-proxy records (**47 `Proxy` + 7 `ProxyAmbush`**), whole-record replacement across
the four-archive mod stack, **41** distinct field names. Fields whose *name* contains any of
`delay / time / interval / rate / period / stagger / cooldown / duration / wait / tick / batch /
burst / frequency`:

```
delayedRun · maxDelayTime · maxSpawnTime · minDelayTime · minSpawnTime
```

`delayedRun` is a **boolean latch**, not a duration. The other four exist **only on the seven
`ProxyAmbush` records** and are the `+4.000 s` Lap V-2 decoded. **There is no other schedule field
in the band.**

### 4.4 Per-wave batch composition (imported by identity, Lap V `pm4v_roster_arithmetic.csv`)

Expected bodies per active spawn point; **each cell is released in ONE batch, at one instant.**

| wave | active points | E[bodies] per point | wave total |
|---|---|---|---:|
| 151 | 1,2,3,4,5 | 16.0 · 6.0 · 3.0 · 16.0 · 4.5 | **45.5** |
| 152 | 1–6 | 9.0 · 6.0 · 14.0 · 4.0 · 3.0 · 18.0 | 54.0 |
| 153 | 1–6 | 6.0 · 15.0 · 14.0 · 18.0 · 4.5 · 6.0 | 63.5 |
| **154** | **1,2,3,4** | 2.0 · 2.0 · 3.0 · 24.0 | **31.0** |
| 155 | 1,2,3,4,6 | 1.0 · 2.0 · 21.5 · 21.5 · 15.0 | 61.0 |
| 156 | 1–6 | 1.0 · 2.0 · 2.0 · 23.5 · 21.0 · 7.0 | 56.5 |
| 157 | 1–6 | 3.0 · 18.0 · 23.5 · 26.0 · 9.0 · 3.0 | 82.5 |
| **158** | 1–6 | 27.0 · 18.0 · 27.0 · 27.0 · 6.0 · 6.0 | **111.0** |
| 159 | 1,2,3,4,5 | 2.0 · 6.0 · 1.0 · 4.0 · 2.0 | 15.0 |
| 160 | 1,2,3,4,6 | 1.0 · 1.0 · 1.0 · 2.0 · 3.0 | 8.0 |

*(p06 rows are `bonusSpawnStatus`-conditional per Lap S `A-4`; the referent's value is Lap V's
still-open `UNREACHED-S7` and is not decided here.)*

### 4.5 ⚑ Wave 150 is not in this table, and the commission's band spans two authored tables

`eventcontrol.lua` routes on `rewardTier = floor(wave/10)`; `15 → tier16Waves`. But
`SurvivalEvent_Start` dispenses **immediately** (`survivalevent.lua` **L438**) and
`SurvivalEvent_SpawnNext` increments the counter **inside itself** (**L513**) *before* dispensing.
So at counter 150 the tier-16 event starts, the counter ticks to 151, and **waveIndex 1 is
dispensed**. The bodies fought on the board labelled **150 were dispensed by the previous tier's
table.** `tier16waves.lua` covers **151–160**. The commission's "150–160" therefore spans two
authored tables, and only the second is decoded here.

---

## 5 — FORK (c) — BETWEEN SPAWN AND ENGAGE

### 5.1 What a body is at the instant of placement

`Proxy::PlaceObjects` hands each body to `World::AddEntity(entity, coords, true)` and
`Proxy::PoolComplete` stamps it, per body, with `[+0x37bc]` proxy-parent id, `[+0x37c0]`
proxy-parent name and `[+0x37d8]` sibling count (all three asserted present). Every non-ambush
proxy has already been given `PatrolPoint_Attack` (L553). **Acquisition is immediate**: Lap U's
pinned decode gives `ViewDistance = 80.0` on **169/169** of the rolled tier-16 roster, and the
arena's own worst case is far inside that.

### 5.2 ⚑ THE ALERT GATE — `UNREACHED-U3` CLOSED, AND IT WAS ALMOST CLOSED THE WRONG WAY

`ControllerMonsterState::DefaultEnemyFoundResponse` (`Game.dll 0x1010a360`) does **two** things,
not one. Lap U decoded the first. The second is this:

```
+0x039  SetState("Pursue")                                  ; literal 0x1052d5d4   (Lap U)
...
+0x333  d = sqrtf(dx*dx + dy*dy + dz*dz)                     ; sqrtss
+0x35f  if (d <= gGameEngine->[+0xc80]) goto skip            ; comiss / jbe
+0x375  a = AngerManager::GetAngerDiff(enemyId)
+0x385  if (15.0f <= a) goto skip                            ; 0x105f58ac / comiss / jbe
+0x38b  AddTemporaryState("AlertBeforePursue", stateData)    ; literal 0x1052d5fc
+0x418  if (rand()%100 < monster[+0x3240] && this[+0x28c]) { this[+0x28c]=0; PlayNetSound(...) }
```

**The distance operand is a shipped `.dbr` field.** `[GameEngine+0xc80]` has **exactly one writer**
(`GameEngine::LoadFromDatabase +0x186`) and **exactly one reader** (this gate). Its field literal is
`0x1054d7c0 = "alertDistance"`, loaded in the loader immediately after `"meleeTargetDistance"` into
`[+0xc7c]` — *the neighbouring member Lap Z decoded.* Constructor default `2.0f`, never used.

**The `gameengine` substring decoy set, ENUMERATED (7 records, `D-Z-1`):**

| record | `alertDistance` |
|---|---:|
| **`records/game/gameengine.dbr`** ← the shipped one, exact path | **6.0** |
| `records/ingameui/gameengine.dbr` | **5.0** ⚑ a real decoy, different value |
| `records/sandbox/arthur/archive/gameengine {01-23-15, 02-01-16, 09-09-15, 10-31, 7-31}.dbr` | 6.0 ×5 |

**Independent validation that the right record was read:** the same record's
`meleeTargetDistance` reads back **`2.4000000953674316`** — bit-for-bit Lap Z's published operand,
from a different instrument on a different question.

**The state itself.** `ControllerMonsterStateAlertBeforePursue::OnBegin` (`0x10109410`) is a single
call: `ControllerAI::PlayAnimation(AnimationSet_Type 0x21, <Name>, 1.0f, false, 0)`. `OnEnd`
(`0x10007f40`) is a **bare `ret`** (ICF-folded no-op). `OnUpdate` (`0x10109430`) reads the target's
coords and faces it; **no locomotion-named call appears** in its first `0x120` bytes.

> **⚑ THE FINDING.** Crucible spawn points sit **29–39 m** from the attack ring (§ 2.4).
> `alertDistance = 6.0 m`. **The distance limb of the gate is satisfied for essentially every body
> in the band.** Every such body is pushed into an animation state before it marches, and that state
> is **entered per body, on acquisition** — not per pack, not per wave. **This is the only
> per-body, spawn-adjacent delay the referent has, and no lap in this run had it.**

**What is NOT claimed.** The **duration** is an animation length (`UNREACHED-AA-3`). Whether the
body is *immobile* during it is **DECLARED, not DECODED**: `OnUpdate` issues no locomotion call, but
I did not decode whether the controller's outer update moves the body regardless — that outer loop
is the same virtual-dispatch driver Lap U left as `UNREACHED-U1`. The **anger limb**
(`15.0 > GetAngerDiff`) is decoded as arithmetic and **NOT** decoded as to when it holds
(`NAMED-AA-1`).

---

## 6 — ⚑ DO-NOT BLOCK (binding on every downstream fold)

1. **DO NOT** fold a spawn-side stagger, batch schedule, or per-point release delay for the
   referent. There is none. §§ 4.1–4.3 are a decoded **negative**, and the run has now spent one
   lap establishing it — do not re-open it as an assumption.
2. **DO NOT** model the pack scatter as a uniform disc. It is **uniform in radius** (`1/ρ` density,
   mean `E/2`), navmesh-validated, with a 100-attempt failure mode. An area-uniform disc of the same
   radius over-disperses the mean by **33 %** (`5.333` vs `4.000` m at `E = 8.0`).
3. **DO NOT** treat `alertDistance = 6.0` as a delay *magnitude*. It is the **gate**, not the
   duration. The duration is `UNREACHED-AA-3`. Any fold that needs a number must commission the
   animation-length decode, not estimate one.
4. **DO NOT** claim the alert state immobilises the body. § 5.2 states plainly what is decoded
   (`OnUpdate` issues no locomotion call) and what is not (whether the outer update moves it anyway).
   Those are different claims — this is the `D-I24D-1` class.
5. **DO NOT** cite any fork-(a) distance without the arena caveat. Arena identity is **UNREACHED at
   3 of 10 candidates**; § 2.4 publishes the candidate-restricted bound and the all-arena bound, and
   the candidate-restricted one is the one to use.
6. **DO NOT** use the enumerated decoy sets as sources. The six non-shipped `gameengine` records
   (one of which carries `alertDistance = 5.0`), the seven other arena maps, and the 29-row raw
   `+0x4ac` scan are published so that they are **visibly excluded**, not so they are available.
7. **DO NOT** read § 4.4's composition table as a roster. Those are **expectations** over Lap V's
   decoded count model; the per-wave draw is stochastic and `bonusSpawnStatus` (p06) is still
   `UNREACHED-S7`.
8. **All prior DO-NOT blocks are carried unchanged** — Lap V § 7.2, Lap V-2 § 11.2, Lap W § 7.2,
   Lap X § 12.2, Lap Y § 11.6, **Lap Z § 5 (all seven)**. In particular Lap Z DO-NOT 4: `NAMED-Z-1`
   (box-vs-sphere) is not propagated by this lap either.

---

## 7 — DEFECT TABLE (all mine · all self-caught · all repaired BEFORE any claim rested on them)

| id | defect | disposition |
|---|---|---|
| **`D-AA-1`** | ⚑ **THE BIG ONE.** My first-pass scan for `.text` references to the `"AlertBeforePursue"` literal took **one** address (`0x1052c33c`), found its single reference in `RegisterTemporaryStates`, and was about to report a **MEASURED-NEGATIVE — "registered and never entered"**, the `characterRunSpeedJitter` pattern. The literal has **TWO standalone copies** in `.rdata`. The second (`0x1052d5fc`) **is referenced — from inside `DefaultEnemyFoundResponse`.** The state IS entered. | **CAUGHT BEFORE ANY CLAIM**, by the `D-Z-1` enumeration guard I armed in `prereg.md § 5` — the instrument classifies **all 11** raw occurrences by NUL-delimitation, isolates the standalone copies, and scans **every** one. Repaired by **strengthening**: the guard now lives in the artifact. ⚑ **Lesson: a decoy set of LITERAL ADDRESSES is enumerated exactly as a decoy set of record paths is — and a false negative is the most expensive kind, because it reads as a clean finding.** |
| **`D-AA-2`** | My `PoolComplete` per-body-stamping predicate matched `"mov dword ptr [ebx + 0x37bc], eax"` — a spacing the disassembler does not emit — so it silently returned `False` for all three stamps. | **CAUGHT** by internal contradiction: I had read those exact instructions during declared reconnaissance. Repaired to match on the operand `[ebx + 0x37bc]` and armed with a **HALT** if any stamp is absent, so the predicate can no longer fail quietly. The `D-Z-2` class — *a silent negative in a string predicate does not crash, it lies.* |
| **`D-AA-3`** | My Lua line lookup took the **first** textual match of `for id = 1, waveEvent.numSpawns do` and reported **L397** — a loop inside `SurvivalEvent_Start` that gathers coordinates — as the dispensing loop. The dispensing loop is **L539**. | **CAUGHT BEFORE ANY CLAIM.** Repaired by anchoring on `SurvivalEvent_SpawnNext`'s own definition line and by **publishing the full hit set** (`[539, 715, 723, 730]`) in the log. The `D-Z-1` class applied to text: *the first match is not the right match.* |
| **`D-AA-4`** | I pooled Lap U's geometry rows and reported `n = 12` spawn points per arena. Lap U's artifact carries **two archive copies of every map** (a lower mod layer and `survivalmode3`); the true count is 6. Worse: on **`survivalworld_a` — one of fork (d)'s three candidates — the two copies DISAGREE.** | **CAUGHT** by the arithmetic not making sense against Lap T's published census of 6 per arena. Repaired by resolving the mod stack (`survivalmode3` is the highest layer and ships all ten maps), asserting `60 == 10 × 6` with a HALT, and **publishing the one disagreeing map by name**. Pooling would have silently averaged two different `survivalworld_a`s. |

---

## 8 — COLLATERAL: NAMED, NOT DECODED (`R-PM4-56 part 4`)

| id | finding | status |
|---|---|---|
| **`NAMED-AA-1`** | **The alert gate has a second limb the run has never seen: `AngerManager::GetAngerDiff(enemy)` compared against `15.0f`.** An anger subsystem exists (`ControllerMonster::AngerUpdate`, `AngerManager` at `controller+0x2b8`) and participates in whether a body alerts before pursuing. Its dynamics are **not decoded**; a body whose anger-diff is ≥ 15.0 skips the alert entirely. | **NAMED** |
| **`NAMED-AA-2`** | **`SurvivalEvent_SelectMutators()` runs once per wave** (`survivalevent.lua` L435, inside `SurvivalEvent_Start`). A Crucible **mutator** system exists and no lap in this run has touched it. Named because it is on the wave-dispensing path; **not decoded**, and not an argument for anything. | **NAMED** |
| **`NAMED-AA-3`** | **Spawn placement can FAIL.** The navmesh sampler gives up after **100** rejected attempts. On a crowded or geometrically awkward spawn disc some bodies may be placed by a fallback path or not at all. Real, on the decoded path, **magnitude unknown**. | **NAMED** |
| **`NAMED-AA-4`** | **Body facing at spawn is uniformly random over 2π** (`SelectPoolLocations`, `0x40c90fdb`). The sim has no spawn-facing concept. A real structural difference; **not decoded** as to whether it costs a turn before the march. | **NAMED** |
| **`UNREACHED-AA-1`** | The Lua↔native `Proxy:Run()` binding body is inside `Grim Dawn.exe`, which ships a `.bind` (Steam DRM) section with encrypted `.text`. Not read. It does not disturb § 4.2, whose conclusion rests on an **enumeration of the latch's writers**, not on reading the binding. | **UNREACHED — named** |
| **`UNREACHED-AA-2`** | What `NavManager::FillPointSet` does with a **failed** point (sampler returned false after 100 tries) — skip the body, place it at the origin, or abort the pack — was not followed to a conclusion. | **UNREACHED — named** |
| **`UNREACHED-AA-3`** | ⚑ **THE DURATION OF `AlertBeforePursue`.** `OnBegin` plays `AnimationSet_Type 0x21` at speed `1.0f`; `OnEnd` is a no-op; the exit is event-driven via `HandleEvent(const Name&)`. The length lives in an animation asset (`.anm`), which this lap did not commission and which is a different corpus from the record DB. **This is the single most load-bearing number the lap did not reach**, and it is not estimated. | **UNREACHED — named** |
| **`UNREACHED-AA-4`** | Whether the body is **immobile** during the alert state. `OnUpdate` issues no locomotion call, but the outer virtual-dispatch update driver is Lap U's `UNREACHED-U1` and was not reconstructed (`D-V2-1` forbids the vtable read). | **UNREACHED — named** |
| **`UNREACHED-AA-5`** | Which of `survivalworld_a / _b / _e` the referent's session loaded (§ 2.3). Blocked by the exe's DRM. Reachable, in principle, by a visual match of the referent capture against each map's rendered terrain — a capability this lap does not have. | **UNREACHED — named, bounded in § 2.4** |

---

## 9 — PRE-REGISTERED PREDICTIONS, GRADED

Wording is unchanged from `prereg.md § 4`, whether the bet held or failed.

| id | bet | result | evidence |
|---|---|---|---|
| `P-AA-1` | only `delayedRun` / `chanceToRun` / `placementExtents` shape a release; no base-`Proxy` delay, interval, batch or rate field | **PASS** | § 4.3 — 41 field names, 5 timing-named, 4 of them ambush-only |
| `P-AA-2` | `PlaceObjects` places the whole vector in one call | **PASS** | § 4.1 |
| `P-AA-3` | no authored stagger between spawn points | **PASS** | § 4.1 — one Lua loop, synchronous chain |
| `P-AA-4` | independent random offset per body bounded by `placementExtents`, not a formation. **Sub-bet: a SQUARE/BOX region** | **PASS on the law · ⚑ SUB-BET FAILED** | § 3.2 — it is **polar**, and worse for my bet, **radius-uniform**, which is neither a box nor an area-uniform disc |
| `P-AA-5` | `delayedRun` defers by at most one tick and carries no duration | **PASS** | § 4.1 — 12 instructions, tail-jump, no timer |
| `P-AA-6` | the ambush `4.000 s` is the only spawn-side timer in the band | **PASS** | § 4.3 |
| `P-AA-7` | pessimistic: arena identity lands UNREACHED, "nor which difficulty tier" | ⚑ **FAILED IN BOTH HALVES, in opposite directions** | the **tier is attested** (`Gladiator`, 91 frames), and the arena is **named** and narrowed 10 → 3 rather than left open; only the map file is UNREACHED (§ 2) |
| `P-AA-8` | pessimistic: `UNREACHED-U3` will not close | ⚑ **FAILED** | § 5.2 — it closed, on a decoded condition, and it took a defect (`D-AA-1`) to nearly close it the wrong way |
| `P-AA-9` | composition is stochastic; no point dispenses in more than one batch | **PASS** | § 4.1 + § 4.4 |
| `P-AA-10` | the load-bearing bet: arrival ORDER is generated by march geometry and body speed, not by a spawn schedule | ⚑ **PASS ON THE SPAWN SIDE, AND MY FRAMING WAS WRONG** | release is simultaneous (§ 4), so no spawn schedule exists — but § 5.2 finds a **per-body, spawn-adjacent alert delay** I did not anticipate. "Not a spawn schedule" was right; "therefore only march geometry and speed" was **not**, and I record that the prediction was too narrow |
| `P-AA-11` | wave 150 is not dispensed by `tier16waves.lua` | **PASS** | § 4.5 |
| `P-AA-12` | `placementExtents` decodes as a metric scatter bound | **PASS** | § 3.1–3.2 |

**Three failures, and all three are informative.** Two pessimistic bets were beaten by the evidence
(good — registering them is what makes that visible). `P-AA-10`'s framing failure is the one that
matters: I bet the negative correctly and drew the wrong positive from it.

---

## 10 — METHOD, AND WHAT WAS NOT DONE

* **Determinism ×2** — instrument ran twice end to end; **all seven artifacts byte-identical**.
* **Pins** — 16 asserted EXACT against prior laps' published digests, 9 recorded; **no HALT**.
* **Guards armed and exercised:** `D-Z-1` decoy enumeration (**fired**, `D-AA-1`); `D-Z-3`
  three-start disassembly convergence on five load-bearing sites (`[ebx+0x410]`,
  `[edi+0x4ac]=6`, `PlaceObjects` call, `[eax+0xc80]`, `[ebx+0x37bc]`) — no disagreement;
  HALT-on-absence predicates on the stamping test and the mod-stack row count (**fired**, `D-AA-4`);
  strict, non-resyncing readers throughout.
* **Import by identity (`R-PM4-67 part 2`)** — every prior-lap number (Lap N's OCR, Lap U's geometry
  and pursue decode, Lap V's composition, Lap V-2's ambush law, Lap Z's operand) was read from the
  pinned artifact at instrument time. **No number was restated from commission text or from prose.**
* **`D-V2-1` honoured** — no vtable reconstruction; every virtual call I could not resolve statically
  is an UNREACHED in § 8, not a guess.
* **Not done, deliberately:** no simulation; no sim artifact opened; no I-25 artifact opened; no
  scorecard consulted; no fold; no prescription; no designation by grade; no animation-asset decode;
  no visual match against the referent capture; **read-only on every external source; no push.**

---

## 11 — ARTIFACT DIGESTS (full 64-hex sha256)

### 11.1 Emitted by this lap

| artifact | sha256 |
|---|---|
| `prereg.md` | `ff7c25a34b568d8b79d1ccbacbaaf4b8c3b7ee23c9de52cbcc6aa866394a5611` |
| `pm4aa_arena_identity.json` | `e31aa504eeb8c7716ea7725b9a5b998c68f157b82852e9026e6e850b542950d4` |
| `pm4aa_placement_law.json` | `55506b697f1df1e09afdc1aabc04bc537d6d8531544642ce83c3c014b23d6ad9` |
| `pm4aa_release_chain.csv` | `d4794a8097a636d29a5d59ac13df920bd15ebaf181e46de433780a1ef28da4a3` |
| `pm4aa_proxy_fields.csv` | `018fd0c36736bb1b1a8b7972298a7a524820bdf4356a97af7088252758306a18` |
| `pm4aa_spawn_structure.json` | `69b698966839622f15c6c78a9fdcf6724d9f60bd2a51dad29ac54e82bc87470b` |
| `pm4aa_digests.json` | `8b4e310d45db1a364f216315c7703f6169c1b7d42e0cfd9ed72d494f4c68dc87` |
| `decode.log` | `b13b7d32206d8fda8495eb3b3294093e6c22cffb9c4933500312a31237581ac7` |
| `research/scripts/pm4aa_spawn_structure_2026_08_16.py` | `bd10c2fa96f3dea2681f582bea000bf8ccdecaa75c5ac7a792bb178ea700569c` |

### 11.2 Every artifact consulted (verified at instrument start)

`ED` = `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808` ·
`GD` = `/Users/admin/Games/vendor/grim-dawn` ·
`NOTES` = `agentic_orchestration/legolas/notes`

| artifact | sha256 |
|---|---|
| `ED/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `ED/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `ED/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `ED/mods/survivalmode/resources/Maps.arc` | `5377259861ad5c17a6009ae045ebc94612faca9a65bc14904b193b9c6d4fa708` |
| `ED/mods/survivalmode/resources/Scripts.arc` | `47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009` |
| `ED/resources/Text_EN.arc` | `1105b1eef70c83914a00d0516ea6db3a25ed06fad8ec91757481e66879d58a27` |
| `ED/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `ED/survivalmode1/resources/Maps.arc` | `2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237` |
| `ED/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `ED/survivalmode2/resources/Maps.arc` | `cef96030be9bdc9be64bf187389aeccec6552ba1cfde30d1c63d716d2f6dbaec` |
| `ED/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `ED/survivalmode3/resources/Maps.arc` | `94e20abadfce0f92d5187ab20bb8a9510fca9163e2b5b67b038cb55953f34911` |
| `GD/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `GD/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |
| `GD/Grim Dawn.exe` | `1a71e188ea3d7f83bec296e22acecf7cac71686c9c0c117d0eb03c9d7ada1ff4` |
| `NOTES/…lap-n-crit-and-collision/pm4n_fct_events.csv` | `cf8ed21815339bd62813237c73363e06db86b1758a725ff32567212ed0424ce2` |
| `NOTES/…lap-s-arena-advance/evidence/eventcontrol.lua` | `cd2bf304d89555d3471e6b449e7e2d170350fc6dfe97726f43ab9b395224a2be` |
| `NOTES/…lap-s-arena-advance/evidence/survivalevent.lua` | `8f1a434fd10b92fb0e3a9fc6293a2bfedca307f697243ec9f102e81f01a588fb` |
| `NOTES/…lap-s-arena-advance/evidence/tier16waves.lua` | `208abadefcb213d8227b61127a97a9e5fb4d5b4011150f713a81d4ecba8fd5d3` |
| `NOTES/…lap-u-ramp-decode/pm4u_geometry_v3.csv` | `5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2` |
| `NOTES/…lap-u-ramp-decode/pm4u_pursue_decode.json` | `6efd193aaa88158154beda71a723dbc70feda5f963ad470437137af92f98d733` |
| `NOTES/…lap-v-roster-decode/pm4v_roster_arithmetic.csv` | `991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c` |
| `NOTES/…lap-v2-proxyambush-decode/pm4v2_ambush.json` | `cb3f7f571c5bf25849814627b02d2c936465cd38393c95342bfb4baf99e8d010` |
| `NOTES/…lap-z-ring-operand/pm4z_findings.md` | `283cf38b25b9c2ad9444fed9e8f1c972b82f80fd0ccfc6258f389b77dd75ee26` |
| `research/scripts/gd_arz_adapter_2026_07_24.py` (carried, unchanged) | `040bd078a73f81ed7b839820fcfc15af1e74beba81a930fc147f1080bb317266` |
| `research/scripts/gd_arc_reader_2026_07_26.py` (carried, unchanged) | `a5def5a669270f6362f96dfcb932d0ba8a77b689919086675b97b95fa16f7597` |

---

*Returned by legolas (UNKNOWN-RESEARCHER), 2026-08-16, RUN KC2-PM4 Lap AA.
Prereg committed ALONE as `ba368773` before any instrument ran; this file, the six emitted
artifacts and the instrument follow in a second commit.*
