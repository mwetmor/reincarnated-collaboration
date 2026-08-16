# KC2-PM4 · LAP V — THE ROSTER DECODE · FINDINGS

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Authority:** `R-PM4-56 part 2` (ledger `L-47` / `R-PM4-56`), on Matt's Q58 word (2026-08-15,
verbatim): ***"fix the bonus spawn system and count-model holes now."*** **Date:** 2026-08-15.

**Pre-registration:** `PREREGISTRATION.md`, sha256
`48754f273073887a55ef8cad025fa79cc3f03db07a9dee4b76264f85773b1d07`, **committed ALONE in commit
`cfa2e01c` before any instrument of this lap ran** (the `L-46` carry — priority is git-attested).

---

## § 0 — THE HEADLINE TABLE

| # | finding | grade |
|---|---|---|
| **F-1** | **⚑ `bonusSpawnStatus` IS NOT A FIELD AND NOT A DIFFICULTY TERM — IT IS A ONE-SHOT, SERVER-SIDE, PLAYER-ELECTED BOOLEAN, AND ITS ONLY SETTER IS A QUEST EVENT.** `checkBonusStatus()` returns the file-local `bonusChest`, initialised `false`, set `true` exactly once by `gd.survival.rewards.bonusChest()`, cleared by `resetLootVariables()`. | **DECODED** |
| **F-2** | **The p06 gate is the ONLY p06 suppressor**, and in tier 16 **8 of 10 waves declare a p06 proxy** — including **wave 160**. Waves 154 and 159 declare none, so p06 is worth **exactly nothing** at 159 and 154 regardless of the flag. | **DECODED** |
| **F-3** | **⚑ THE COUNT MODEL RESOLVES AT `Game.dll sub_10357590`, AND EVERY LINE OF IT IS READABLE.** Regular count `n = lo + rand() % (spawnMax − lo + 1)` with `lo = min(max(spawnMin,0), spawnMax)` — **uniform inclusive, one draw per spawn point per wave, clamp-min-down real**. | **DECODED** |
| **F-4** | **⚑ THE OPERATOR ORDER IS `(base + additive) × modifier`, THE ROUNDING IS TRUNCATION, AND THE PER-WAVE ADJUSTMENT LANDS *OUTSIDE* THE MODIFIER.** `U9-1` is **closed**; the sim's branch A is right on the first two and wrong on the third — and the third is **exactly inert** over 151–160 (`spawnMinAdj = spawnMaxAdj = 0` at every wave in the band). | **DECODED** |
| **F-5** | **⚑ `championChance` IS APPLIED FIRST, AND CHAMPIONS CONSUME THE REGULAR BUDGET — THEY DO NOT ADD.** The champion limb emits into the same vector the regular draw then subtracts (`0x10357ca5`). **Crate's modding-guide "champions add, they never convert" is contradicted by the shipped code.** | **DECODED** |
| **F-6** | **F-5 IS EXACTLY INERT OVER WAVES 151–160.** Census of all 139 alternative-rows in the band: **zero** carry `championChance > 0` **and** a non-empty regular roster. The correction is real and it buys nothing here. **Reported because it is true, not because it moves a number.** | **DECODED (negative)** |
| **F-7** | **⚑ `EMPTY_ROSTER_DISPOSITION = NO_OP_ON_EMPTY` IS THE BRANCH THE GAME IMPLEMENTS.** The weighted picker returns FALSE on an empty/exhausted roster and the emission loop **breaks** (`0x10357cf7`, `0x10357dad`). **`CONJURE_FROM_TEMPLATE` is DECODED-WRONG and its +11 bodies do not exist.** The sim's incumbent branch is correct. | **DECODED** |
| **F-8** | **⚑ THE COUNT HAS A CAP NOBODY MODELLED: `limitN`.** The picker filters on `limit != 0` and **decrements it on every pick** (`0x1035841a` / `0x103584fc`). A unique-boss pool with `spawnMin = spawnMax = 1` and `limit1 = 1` is granted `+1` on Gladiator, asks for **2**, and can only deliver **1**. **25 alternative-rows in the band are capped this way; it costs −11.5 expected bodies against the incumbent.** | **DECODED** |
| **F-9** | **⚑ MY OWN U9 § 5.2 IS CONVICTED BY F-8.** "Doubled bosses on Gladiator is a real and intended behaviour" was **DERIVED, and it is wrong** for every `limit1 = 1` pool — which is every unique-boss pool in the band. Self-caught, FIT law. | **DEFECT `D-V-1`** |
| **F-10** | **⚑ THIRD MECHANISM — `ProxyAmbush` AT SPAWN POINT 5, `minGroupSize = maxGroupSize = 30`.** All seven tier-16 p05 proxies are class `ProxyAmbush`, not `Proxy`. **NOT DECODED, NOT PRICED — reported as a run-level HALT trigger per `R-PM4-56 part 4`.** It does **not** touch wave 160, 154 or 155 (no p05 declared). | **`F-3M-1` — HALT TRIGGER** |
| **F-11** | **THE GRADED PREDICTION.** Decoded, p06 **ON**: per-wave expected roster median **21.1875** vs the referent median 25 (**ratio 0.8475**); **7 of 10** waves can *envelope-reach* 19; **wave 160 = 7.0 exactly, 12 short of the referent floor of 19.** | **GRADED** |
| **F-12** | **⚑ THE DECODE IS NET-UNFAVOURABLE AGAINST THE INCUMBENT.** Decoded p06-ON totals **197.08** expected bodies over 151–160 against the incumbent p06-ON **208.58** — the roster fix **removes 11.5 bodies** with one hand while p06 adds 25 with the other. Against the run of record (incumbent p06-OFF, 183.58) the net is **+13.5 over ten waves**, not +36. | **GRADED** |

---

## § 1 — LIMB (a): `bonusSpawnStatus`, DECODED

### 1.1 `V-a1` — the function body, verbatim

`game/survival/rewards.lua`, shipped inside `survivalmode3/resources/Scripts.arc` (the
last-writer-wins overlay; `sm1` and `sm_mod` carry byte-different but semantically identical copies
at lines 926 and 879 respectively):

```lua
local bonusChest = false                                   -- L18, module scope

function gd.survival.rewards.checkBonusStatus()            -- L1003
	return bonusChest
end

function gd.survival.rewards.bonusChestTokenGlobalMP()     -- L1009
	bonusChest = true
end

function gd.survival.rewards.bonusChest()                  -- L1015
	if Server && not bonusChest then
		LuaGlobalEvent("bonusChestTokenGlobalMP")
		bonusChest = true
		local spawn  = Entity.Get(spawnPoint06FxId)
		local coords = spawn:GetCoords()
		local fx = Entity.Create("records/fx/ambient/fx_eldritchrift_medium01.dbr")
		if (fx != nil) then fx:NetworkEnable(); fx:SetCoords(coords) end
	end
end

function gd.survival.rewards.resetLootVariables()          -- L1067
	if Server then rewardUpgraded = false; bonusChest = false end
end
```

**Every input to the return value is named, and there is exactly one:** the module-local
`bonusChest`. **`V-a1` = DECODED.**

Three consequences the fold needs:

1. **It is one-shot and monotone within a run** (`if Server && not bonusChest`), so it cannot flip
   mid-band. Whatever it is at wave 151 it still is at wave 160.
2. **`gd.survival.rewards.bonusChest` is registered as a QUEST EVENT** — `game/questevents.lua`
   L85: `bonusChest = gd.survival.rewards.bonusChest,`. It is fired from the quest/dialogue system,
   not from the wave engine, not from difficulty, not from wave index.
3. **It has a visible signature.** Setting it creates `fx_eldritchrift_medium01` at
   `spawnPoint06FxId`. See § 6 `R-V-1`.

### 1.2 `V-a4` — the referent-side value: **`UNREACHED-S7` STAYS OPEN, AND IS RE-SCOPED**

The prereg fixed the rule: DECODED only if the flag turns out to be *forced*. It is not. The
shipped text says so in the game's own words —

> `achS007Desc = Complete the Crucible through Wave 150 on Gladiator Difficulty with the 6th Spawn
> Point active.`
> `tagTutorialTip64TextB = …any additional bonuses you activated **at the start**.`
> (`mods/survivalmode/resources/Text_EN.arc :: tags_survivalui.txt`)

**⚑ `bonusSpawnStatus` is a PLAYER ELECTION MADE AT THE START OF THE RUN.** No amount of record or
binary reading can tell me what Matt elected. **`UNREACHED-S7` therefore stays open on the referent
side and is re-scoped from a *records* question to a *fixture* question.** Both limbs are computed
and published below; **I do not pick one, and specifically I do not pick the one that grades
better** (`R-PM4-27 part 3`; the better-grading limb is p06 ON, and saying so out loud is the point).

### 1.3 `V-a2` — the gate, and that it is the only one

`game/events/survivalevent.lua`, verbatim (L392, L535, L539–540):

```lua
waveEvent.numSpawns = table.getn(entity)                       -- entity[1..6] -> 6
local bonusSpawnStatus = gd.survival.rewards.checkBonusStatus()
math.randomseed(Time.Now())
for id = 1, waveEvent.numSpawns do
	if (waveEvent.waves[id][waveEvent.waveIndex] != nil && (id < waveEvent.numSpawns || bonusSpawnStatus == true)) then
```

A sweep of the whole survival Lua returns **exactly this one gate**; the `else` branch marks the
point `proxyKilled` without spawning. **`V-a2` = DECODED.** Two riders:

* **`math.randomseed(Time.Now())` per wave is EXACTLY INERT in tier 16.** The Lua-side pick
  `random(1, totalProxies)` is over the declared proxy list, and **every tier-16 list has length
  ≤ 1** (measured: lengths ∈ {0, 1} over all 60 slots). There is no Lua-side roster randomness in
  the band at all.
* `Proxy.Create(…, …, true)` — the third argument defeats the engine's boss-spawn limit on **every**
  Crucible wave (u9 § 5.5, re-confirmed). Campaign boss-concurrency intuitions do not transfer.

### 1.4 `V-a3` — which waves declare a p06 proxy, and from which pools

From `survivalmode1/resources/Scripts.arc :: game/survival/tier16waves.lua`. Global wave
`w = 150 + tierWave`.

| global wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | **160** |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **p06 declared** | — | ✔ | ✔ | — | ✔ | ✔ | ✔ | ✔ | — | **✔** |
| p05 declared | ✔ | ✔ | ✔ | — | — | ✔ | ✔ | ✔ | ✔ | — |

**⚑ Wave 160 declares a p06 proxy and declares NO p05.** Its p06 pool is
`records/proxies/poolsherogdx1/wendigocannibal_hero.dbr` (a hero pool: `spawnMin = spawnMax = 0`,
`championChance = 100`, `championMin = championMax = 1`, five `nameChampion*` entries each
`limitChampion = 1`).

Full per-wave p06 pools are in `pm4v_bonusspawn.json`; the per-alternative arithmetic for all 139
alternative-rows in the band is in `pm4v_roster_arithmetic.csv`.

### 1.5 `V-a5` — what p06 is worth, decoded

| global wave | 152 | 153 | 155 | 156 | 157 | 158 | **160** | **band total** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **expected bodies added by p06** | 3.0 | 3.0 | 3.0 | 7.0 | 3.0 | 3.0 | **3.0** | **25.0** |

**⚑ gamora's `C-12` pricing of +25 bodies is EXACT to the decimal.** That number was reached from
the incumbent recipe and it survives the corrected one unchanged, because every p06 pool in the
band is a hero/bounty/devotion pool whose count comes through the champion limb, which the
corrections do not touch.

---

## § 2 — LIMB (b): THE COUNT-MODEL RESOLUTION, DECODED

### 2.1 The resolver, located

`ProxyPool`'s methods are **not exported**, so no symbol names them. Both functions were located by
their `int3`-delimited bounds inside `Game.dll` and identified by the `.rdata` field literals they
push. **Every address below is an RVA in `Game.dll`,
sha256 `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02`** (byte-identical to the
binary Lap U decoded `ViewDistance` from).

| function | bounds | role |
|---|---|---|
| `sub_10357330` | `0x00357330 … 0x0035758f` | **`ProxyPool::Load`** — reads every field off the record |
| **`sub_10357590`** | **`0x00357590 … 0x00357e2f`** | **the resolve-and-spawn function; the whole count model lives here** |
| `sub_103583d0` | `0x003583d0 …` | the **weighted picker** (level filter · `limit != 0` · weight sum · `dec limit`) |
| `sub_103585c0` | `0x003585c0 … 0x00358609` | the **forced-entry scan** (`limit > 0` **and** flag `[+0x28]`) |
| `sub_10358610` | `0x00358610 …` | **emit one body** → `push_back` into the pool's vector at `[this+0xb0]` |
| `0x104bfcf0` | — | MSVC float→int32, **truncation toward zero** |

**Field offsets on the `ProxyPool` object**, each established by the literal pushed immediately
before the store in `Load`:

| offset | field | literal VA |
|---|---|---|
| `+0x20` | `spawnMin` | `0x1056afa0` |
| `+0x24` | `spawnMax` | `0x1056af94` |
| `+0x28` | `championMin` | `0x1056af88` |
| `+0x2c` | `championMax` | `0x1056afec` |
| `+0x30` | `championChance` (float) | `0x1056afdc` |
| `+0x34` | `ignoreGameBalance` (byte) | `0x1056b074` |
| `+0x38 / +0x50 / +0x68 / +0x80` | the four `*Equation` strings | `0x1056b00c` / `0x1056aff8` / `0x1056b034` / `0x1056b020` |
| `+0x98` | regular selections, loaded from the `name%d` / `weight%d` / `limit%d` family | `0x10805338` |
| `+0xa4` | champion selections, from `nameChampion%d` / `weightChampion%d` / `limitChampion%d` | `0x10805cb8` |
| `+0xb0 / +0xb4` | **the emitted-body vector** (begin / end) | — |

### 2.2 `V-b1` + `V-b2` — the distribution, and where it is drawn

**Regular count draw, `0x10357c69`–`0x10357ca1`, read verbatim:**

```
10357c69  mov  edx, [edi+0x24]        ; spawnMax
10357c6c  xor  ecx, ecx
10357c6e  cmp  ecx, [edi+0x20]        ; 0 vs spawnMin
10357c74  sbb  ecx, ecx               ;  ecx = (spawnMin > 0) ? -1 : 0
10357c76  and  ecx, [edi+0x20]        ;  ecx = max(spawnMin, 0)
10357c79  cmp  ecx, edx
10357c7b  cmovb edx, ecx              ;  edx = lo = min(max(spawnMin,0), spawnMax)   <-- CLAMP-MIN-DOWN
10357c7e  sub  eax, edx               ;  eax = spawnMax - lo
10357c83  inc  eax                    ;  range
10357c84  mov  [edi+0x20], edx        ;  spawnMin is REWRITTEN to the clamped value
10357c8a  dec  eax ; cmp eax, 0x7ffd ; ja …    ; degenerate-range guard -> n = lo
10357c92  call [0x104e650c]           ;  the CRT rand()
10357c98  cdq
10357c99  idiv dword [ebp+8]          ;  edx = rand() % range
10357c9e  add  ecx, [ebp-0x14]        ;  n = lo + rand() % (spawnMax - lo + 1)
```

* **`V-b1` = DECODED — uniform inclusive on `[lo, spawnMax]`**, implemented as `lo + rand() % range`
  (so it carries the classic modulo bias; irrelevant at these range sizes but recorded, not assumed
  away).
* **`V-b2` = DECODED — one draw per POOL, and exactly one pool per spawn point per wave.**
  `Proxy::InitializePools` (`0x00351380`) calls `Proxy::SelectPool` (`0x00352130`) — the weighted
  pick over the proxy's `pool%d` / `weight%d` — and `Proxy::RunProxy` runs the one selected pool.
  The sim's `_weighted_pick` models this hop correctly.
* **The clamp-min-down that u9 § 6 marked "DERIVED (branch A)" is now DECODED**, and it is
  `cmovb` at `0x10357c7b`.

**`V-b5` — seeding: PARTLY DECODED, and I am not claiming more.** `sub_10357590` opens
(`0x103575c7`) with a **Park–Miller minimal-standard step**, `next = (seed × 16807) mod 2147483647`,
seeded from a GameEngine call at `[0x108080a4] + 0xc04`. That stream feeds the **level-variance**
argument passed to every emit, **not** the count draws — the count draws call the **CRT `rand()`**
through the import at `[0x104e650c]`. **Whether the CRT stream is seeded deterministically per
sitting is `UNREACHED-V4`.** Declared in the prereg as expected-unreached; landing as such.

### 2.3 `V-b3` — `championChance`, its order, and the conversion

```
1035796a  movss  xmm0, [edi+0x30]      ; championChance
10357972  comiss xmm0, xmm1(=0)
10357978  jbe    0x103579b0            ; <-- chance <= 0 SKIPS THE ROLL AND FALLS INTO THE DRAW
1035799e  (RandomFloat(0.0, 100.0))
103579a6  comiss xmm0, [edi+0x30]
103579aa  ja     0x10357c04            ; roll > chance -> jump to the REGULAR phase
10357a00  mov esi,[edi+0x2c] ; mov edx,[edi+0x28] ; sub esi,edx ; inc esi
10357a16  call [0x104e650c] ; cdq ; idiv esi ; add eax, championMin
                                       ; n_ch = cmin + rand() % (cmax - cmin + 1)
10357b12  (top-up: if emitted < championMin, emit the difference)
```

then, in the regular phase:

```
10357ca5  mov  eax, [edi+0xb4]
10357cab  sub  eax, [edi+0xb0]
10357cb1  sar  eax, 2                  ; bodies THIS POOL HAS ALREADY EMITTED
10357cb4  sub  ecx, eax                ; n_regulars = n - already_emitted
```

and `sub_10358610` — used by **both** limbs — appends to that same vector
(`0x10358786  lea ecx,[edi+0xb0]`).

> **⚑ `V-b3` = DECODED, AND IT INVERTS THE DOCUMENTED RULE. `championChance` gates the CHAMPION
> limb, which runs FIRST; the regular limb then fills the wave's budget *up to* `n`, minus whatever
> the champion limb already put on the board. Champions CONVERT. Crate's own modding guide says
> they add. The shipped code says they do not.**

Two riders, both stated because they cut against the interesting direction:

* **`championChance <= 0` does not block the champion limb — it bypasses the roll.** The limb still
  runs, still computes `n_ch`, and still tries to emit. It produces nothing only because such pools
  have no `nameChampion*` roster (§ 2.4) — a *census* fact, not a code fact.
* **F-6: over waves 151–160 the conversion is EXACTLY INERT.** Of 139 alternative-rows in the band,
  **0** carry `championChance > 0` **and** a non-empty regular roster, and **0** carry
  `championChance == 0` **and** a non-empty champion roster. The correction is real, it is
  load-bearing outside this band, and here it moves nothing. I report it because it is true.

### 2.4 `V-b4` — `EMPTY_ROSTER_DISPOSITION`: **`NO_OP_ON_EMPTY`, DECODED**

The prereg's anti-fit clause applies here and I invoke it explicitly: `CONJURE_FROM_TEMPLATE` is
the branch that grades better (+11 bodies, and it lands AC-10.4 inside T-2 where the incumbent is
outside). The evidence had to clear the same bar either way. It does:

```
10357cf0  call 0x103583d0        ; the weighted picker
10357cf5  test al, al
10357cf7  je   0x10357d30        ; picker returned FALSE -> BREAK OUT OF THE EMIT LOOP
…
10357da6  call 0x103583d0        ; the same test inside the spawnMin TOP-UP loop
10357dad  je   0x10357ddf        ; -> BREAK
```

and the picker itself (`0x1035840b`, `0x10358485`) returns `al = 0` whenever the candidate set is
empty. **A draw from an empty set yields nothing, the loop stops, and no body is invented.**
`CONJURE_FROM_TEMPLATE` and `PROMOTE_TO_CHAMPION_DRAW` are both **DECODED-ABSENT**. The sim's
incumbent branch was right, and **`C-13`'s +11 bodies do not exist.**

### 2.5 ⚑ `V-b6` OVERRUN — `U9-1` CLOSED, AND A CAP NOBODY HAD

The prereg parked the operator-order residual `U9-1` and said that if the disassembly answered it
for free it would be reported as a bonus finding, not a scope expansion. It did.

**The order, per field, `0x103576d5`–`0x103577a2` (spawn) and `0x10357833`–`0x10357904` (champion):**

```
v = (int)( (float)v + gameproxies.<field>[difficulty] )                  # ADDITIVE   (truncation)
if gameproxies.<field>Modifier[difficulty] > 0:
    v = (int)( (modifier * 0.01f) * (float)v )                           # MODIFIER   (truncation)
v += challengeAdjustment[wave].<field>Adj                                # PER-WAVE ADJ, OUTSIDE
if <field>Equation is non-empty:  v = Proxy::RunEquation(eq, v)          # 0x10353350
```

and the whole game-balance block is skipped wholesale when `ignoreGameBalance` is set
(`0x103575f7  cmp byte [edi+0x34],0 ; jne 0x10357904`) — **but the equations still run for exempt
pools.**

* **`U9-1` = CLOSED. Branch A wins: the additive is INSIDE the modifier.** `n_min = ⌊(spawnMin + 1)
  × 1.20⌋` on Gladiator. u9's and the sim's shared assumption is decode-correct.
* **The rounding is TRUNCATION toward zero** (`0x104bfcf0`, the MSVC float→int32 helper), which
  equals `floor` on the non-negative counts the Crucible deals in. u9's `floor` is decode-correct.
* **⚑ NEW, and a correction to the sim: the per-wave `*Adj` term lands OUTSIDE the modifier**, not
  inside it. The sim computes `⌊(spawnMin + 1 + adj) × 1.20⌋`; the game computes
  `⌊(spawnMin + 1) × 1.20⌋ + adj`. **Exactly inert over 151–160** — measured:
  `spawnMinAdj = spawnMaxAdj = 0` at every wave in the band, and all three candidate
  `balancingadjustment_survivalmode_enemies0{1,2,3}` records agree cell-for-cell across the band
  (`spawnChampionMinAdj = spawnChampionMaxAdj = 1`), so **which record is selected is inert too**
  and I did not need to decode the selector (`UNREACHED-V2`).
* `spawnMaxModifier` and `championMin/MaxModifier` are **absent** from
  `records/game/gameproxies.dbr`, so those three multiplies are skipped. Only `spawnMinModifier`
  (`[0, 112, 120]`) ever fires. u9's "declared-but-unset" reading is decode-correct.
* Every pool in the band uses `records/proxies/proxypoolequation_01.dbr`, which is **the identity**
  (`spawnMinEquation = "poolValue * 1"`, and the same for the other three). Censused: **139/139
  alternative-rows.** The equation hop is inert in the band and is named, not assumed.

**⚑ AND THE CAP — `F-8`.** The weighted picker's eligibility test is `limit != 0`
(`0x1035841a`) and it **decrements the taken entry's limit** (`0x103584fc  dec dword [eax+0x24]`).
An entry with no `limit` field never reaches zero counting down from the loader's default and is
therefore unbounded; an entry with `limit1 = 1` can be handed out **once**.

That is decisive for one whole class of Crucible pool:

| | `records/proxies/poolsboss/manticore_matriarch.dbr` |
|---|---|
| record | `spawnMin = 1`, `spawnMax = 1`, `championChance = 0`, `limit1 = 1`, one `name1`, `ignoreGameBalance` **absent → False** |
| decoded bounds on Gladiator | `n_min = ⌊(1+1) × 1.20⌋ = 2`, `n_max = 1 + 1 = 2`, so `lo = 2`, `n = 2` |
| **what the roster can deliver** | **1** — the picker hands out `name1`, its limit goes to 0, the second call returns FALSE, the loop breaks, and the `spawnMin` top-up breaks on the same test |
| the sim | **2** |

**25 alternative-rows in the band sit in this class.** It is the entire decoded-vs-incumbent delta
(§ 4.2), and it is what makes Crate's own "doubled bosses on Gladiator" warning **not** apply to a
unique boss in the Crucible: the `+1` is granted, and the roster refuses to fill it.

---

## § 3 — LIMB (c): THE PREDICTION, PRE-REGISTERED, THEN GRADED

**Order of operations, as fixed in `PREREGISTRATION.md` § 5 and honoured:**
`pm4v_prediction.json` was written and hashed
(`450d52c9c5c430b528d1e2435760ff2ed45dec60c53a3b1981c20cc9701e275b`) and that hash recorded in
`pm4v_digests.json :: prediction_before_grade` **before** the grading instrument ran. The grading
instrument **re-hashes the prediction file and HALTs on any change** before computing a single
comparison. It did not HALT.

### 3.1 The prediction (decoded recipe, expectations and full envelopes)

| global wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | **160** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **p06 ON — E[roster]** | 26.500 | 20.000 | 26.500 | 11.000 | 19.333 | 22.875 | 22.375 | 36.000 | 5.500 | **7.000** |
| p06 ON — envelope | 24–29 | 20–20 | 26–27 | 11–11 | 19–21 | 21–24 | 18–24 | 30–45 | 5–7 | **7–7** |
| **p06 OFF — E[roster]** | 26.500 | 17.000 | 23.500 | 11.000 | 16.333 | 15.875 | 19.375 | 33.000 | 5.500 | **4.000** |
| p06 OFF — envelope | 24–29 | 17–17 | 23–24 | 11–11 | 16–18 | 14–17 | 15–21 | 27–42 | 5–7 | **4–4** |

### 3.2 The grade, against the referent's 19–36 / median 25 (a LOWER bound)

**Bound direction restated before the numbers, per prereg § 2 B-2: `roster ≥ living` always, so
every grade here is a NECESSARY-condition grade. Nothing below demonstrates sufficiency, and a
decode that lands at 19 has not "matched" a lower bound of 19.**

| grade | p06 ON | p06 OFF |
|---|---|---|
| **G-1** waves whose envelope max reaches 19 | **7 / 10** (151, 152, 153, 155, 156, 157, 158) | **4 / 10** (151, 153, 157, 158) |
| **G-2** median E[roster] vs referent median 25 | **21.1875** — ratio **0.8475**, difference **−3.8125** | 16.6667 — ratio 0.6667, difference −8.3333 |
| **G-3** wave 160 vs referent floor 19 | **7.000 [7, 7] — short by 12.0** | 4.000 [4, 4] — short by 15.0 |
| **G-4** band total E[bodies] | **197.083** | 172.083 |

### 3.3 The pre-registered priors, graded honestly — **three hold, one fails**

| prior | stated before the decode | outcome |
|---|---|---|
| **PRIOR-1** median E[roster] ∈ [20, 26] | — | **HOLDS** (21.1875) |
| **PRIOR-2** ≥ 3 of 10 waves expected below 19 | — | **HOLDS, exactly at the edge** (3 of 10: 154, 159, 160) |
| **PRIOR-3** wave 160 expected below 19 | point guess 8–12 | **HOLDS on the claim, FAILS on the point guess** — the answer is **7.0**, below my own lower bound. I under-predicted how much the `limit` cap would bite. |
| **PRIOR-4** G-1 returns k ≤ 7 | — | **HOLDS, exactly at the edge** (k = 7) |

**The failed point guess is the informative one.** I priced wave 160 at 8–12 from gamora's
branch arithmetic; the decode returns 7 because `F-8`'s `limit` cap removes a body from p04 that
neither model had. **A prior that lands inside its own interval every time is decoration.**

---

## § 4 — THE COMPARATOR: DECODED vs INCUMBENT vs THE RUN OF RECORD

### 4.1 Per wave (expectations under each recipe, over the identical records)

| wave | decoded ON | decoded OFF | incumbent ON | incumbent OFF | Δ(dec−inc) | as-run roll |
|---|---:|---:|---:|---:|---:|---:|
| 151 | 26.500 | 26.500 | 26.500 | 26.500 | 0.000 | 28 |
| 152 | 20.000 | 17.000 | 20.750 | 17.750 | −0.750 | 18 |
| 153 | 26.500 | 23.500 | 26.500 | 23.500 | 0.000 | 24 |
| 154 | 11.000 | 11.000 | 12.000 | 12.000 | −1.000 | 13 |
| 155 | 19.333 | 16.333 | 21.333 | 18.333 | −2.000 | 18 |
| 156 | 22.875 | 15.875 | 24.875 | 17.875 | −2.000 | 19 |
| 157 | 22.375 | 19.375 | 23.375 | 20.375 | −1.000 | 21 |
| 158 | 36.000 | 33.000 | 36.000 | 33.000 | 0.000 | 33 |
| 159 | 5.500 | 5.500 | 9.250 | 9.250 | **−3.750** | 9 |
| **160** | **7.000** | **4.000** | **8.000** | **5.000** | **−1.000** | **5** |
| **total** | **197.083** | **172.083** | **208.583** | **183.583** | **−11.500** | **188** |

### 4.2 What the amendment actually buys, in one line

> **p06 ON is worth +25.000 expected bodies. The count-model correction is worth −11.500. Against
> the run of record (incumbent, p06 OFF, expectation 183.583) the corrected recipe with p06 ON lands
> at 197.083 — a net +13.500 bodies over TEN waves, i.e. +1.35 per wave.**

And the whole −11.500 is one mechanism: **`F-8`'s `limit` cap on unique-boss pools**, which
subtracts exactly 1.0 from each of 25 capped alternative-rows, weight-averaged. `F-5`'s champion
conversion contributes **0.000** in the band (`F-6`), and `F-7` removes gamora's `C-13` branch
outright rather than folding it.

**⚑ The honest headline for the conductor: the roster amendment is smaller than it was priced, and
half of the reason is that one of the two priced branches is decode-wrong in the direction that
loses bodies.**

---

## § 5 — DEFECT TABLE

| id | defect | seam | disposition |
|---|---|---|---|
| **`D-V-1`** | **My own `2026-08-07-u9-spawnmin-operator-order.md` § 5.2 states, as DERIVED: *"Doubled bosses on Gladiator is a real and intended behaviour, not a modelling artefact."* `F-8` convicts it.** The doubling is granted by the additive and then **refused by `limit1 = 1`** on every unique-boss pool. The u9 claim is wrong for the entire class it was written about. | legolas (mine) | **SELF-CAUGHT, reported, not silently repaired.** u9's § 5.2 and § 6 count model are superseded by § 2 of this file. NOTE-9: I do not edit the u9 note; supersession is recorded here and in the hand-off. |
| **`D-V-2`** | The sim's `count_bounds` places the per-wave `*Adj` term **inside** the `spawnMinModifier` multiply; the game places it **outside** (§ 2.5). | gamora | **Exactly inert over 151–160** (`spawnMinAdj = spawnMaxAdj = 0` at every band wave). Fix for correctness, not for counts. |
| **`D-V-3`** | The sim models the champion limb as an **additive** hard gate; the game runs it **first** and subtracts its output from the regular budget, and bypasses the gate entirely when `championChance <= 0` (§ 2.3). | gamora | **Exactly inert over 151–160** (`F-6`, censused). Fix for correctness. **Do not fold it as a count change and do not price it.** |
| **`D-V-4`** | Neither the sim nor `pe6_crucible_wave_pools_v2.csv` carries `limitN` / `limitChampionN`, so the capacity cap of `F-8` cannot be expressed by the incumbent schema at all. | gamora + the pe6 sidecar | **LIVE, −11.500 bodies over the band.** The sidecar needs two new columns; see § 7. |

---

## § 6 — UNREACHED CENSUS (honest per limb; nothing here is estimated)

| id | what | status |
|---|---|---|
| **`UNREACHED-S7`** | **the referent-side value of `bonusSpawnStatus` in Matt's sitting** | **STILL OPEN — and now correctly classified.** § 1.2 decodes it as a **player election at run start**, so it is a *fixture* fact, unreachable from records or binary. **Both limbs published; neither adopted by me.** |
| **`R-V-1`** | *a route, not a finding.* Setting the flag creates `records/fx/ambient/fx_eldritchrift_medium01.dbr` at `spawnPoint06FxId` — **a persistent visible rift at spawn point 6** — and grants the token `SURVIVALMODE_GLADIATORBONUSSPAWNS`. **If the referent footage ever shows spawn point 6's location, `UNREACHED-S7` is closeable from the video.** I did **not** open the footage (out of this lap's limb set). Routed to the conductor. |
| **`UNREACHED-V1`** | **which quest/dialogue node fires the `bonusChest` quest event.** The binding exists (`game/questevents.lua` L85) but the `.qst` that raises it is not in any shipped `.arz` or `.arc` in the vendor tree. Named, not claimed. |
| **`UNREACHED-V2`** | **which `balancingadjustment_survivalmode_enemies0{1,2,3}` record the engine selects**, and what `[GameEngine + 0x28b50]` indexes it with. **Measured inert:** all three agree cell-for-cell across 151–160. Decoded far enough to be safe, not far enough to be claimed. |
| **`UNREACHED-V3`** | **the loader's default value for an absent `limit` field.** `INFERRED-WITH-EVIDENCE` that it is a value the `!= 0` test never rejects (otherwise trash pools with unlimited `name1`/`name2` could spawn nothing, which contradicts the shipped game). Not read out of `sub_10357e90`. |
| **`UNREACHED-V4`** | **whether the CRT `rand()` stream behind the count draws is seeded deterministically per sitting.** Pre-registered as expected-unreached (`V-b5`); landing as such. The Park–Miller stream at `0x103575c7` is a *different* stream and feeds level variance, not counts. |
| **`UNREACHED-V5`** | **the element type of the emitted-body vector at `[this+0xb0]`.** The *structural* claim of `F-5` does not depend on it — both limbs `push_back` into that container and the regular draw subtracts its size — but the element type is not decoded and I am not implying it is. |
| **`F-3M-1`** | **the `ProxyAmbush` mechanism at spawn point 5** — see § 6.1. **NOT DECODED BY RULE.** |

### 6.1 ⚑ `F-3M-1` — THE THIRD MECHANISM, NAMED AND NOT TOUCHED

`R-PM4-56 part 4` makes a third roster-relevant mechanism a **run-level HALT trigger**. One
surfaced. Per the rule I did **not** decode it and did **not** price it. What I have, and nothing
more:

* **All seven tier-16 spawn-point-5 proxies are `Class = ProxyAmbush`**, template
  `database/templates/proxyambush.tpl` — **not** `Proxy` / `proxy.tpl`:
  `proxy_w{01,02,03,06,07,08,09}_p05a.dbr`.
* Every one of them carries, identically: **`minGroupSize = 30`, `maxGroupSize = 30`,
  `spawnThreshold = 15`, `minSpawnTime = maxSpawnTime = 3.0`,
  `minDelayTime = maxDelayTime = 4.0`, `alertArea = 100.0`**.
* `ProxyAmbush` has its own `UpdateSelf` (`0x00354520`), its own `PoolComplete` (`0x00354fb0`), and
  its own `RunProxy` call site (`0x00354565`). The Crucible Lua already treats it specially —
  `if waveEvent.proxy[id]:IsAmbush() == false && … then LinkPatrolPointGroup(…)`.
* **A `minGroupSize` of 30 with a `spawnThreshold` of 15 and a 3-second spawn timer does not read
  like a one-shot pool draw.** I am not going to say what it reads like. It is unmodelled by the
  sim, unmodelled by `pe6_crucible_wave_pools_v2.csv`, and unmodelled by the numbers in this file.

**Exposure, so the conductor can rule with a number in hand.** My § 3 prediction treats p05 as a
plain proxy. The p05 contribution it assumes is:

| wave | 151 | 152 | 153 | 156 | 157 | 158 | 159 |
|---|---:|---:|---:|---:|---:|---:|---:|
| p05 E[bodies] as modelled here | 4.5 | 3.0 | 4.5 | 7.0 | 3.0 | 3.0 | 1.0 |

> **⚑ For those seven waves my prediction is a FLOOR, not an estimate, until `F-3M-1` is ruled.
> Waves 154, 155 and 160 declare no p05 at all, so `G-3` — the wave-160 grade, the one the run
> actually turns on — is CLEAN of this mechanism.**

---

## § 7 — HAND-OFF, SHAPED FOR I-22 (gamora), WITH DO-NOTs

### 7.1 What to fold

1. **`P06_BONUS_SPAWNS` becomes a two-limb PARAMETER, not a constant, and NEITHER limb is
   adopted by me.** `UNREACHED-S7` is a fixture fact (§ 1.2). Run both limbs; publish both. The
   code default is already `True` while the operative limb is `False` — that disagreement is now a
   conductor call with a decoded reason behind it.
2. **p06 is worth `+25.000` expected bodies over the band, at waves 152, 153, 155, 156, 157, 158,
   160 only** (§ 1.5). Waves 151, 154, 159 gain nothing.
3. **`EMPTY_ROSTER_DISPOSITION` stays `NO_OP_ON_EMPTY`. Delete the `+11` from the ledger.**
   `CONJURE_FROM_TEMPLATE` is DECODED-ABSENT (§ 2.4). `empty_roster_plus_one` should become a
   parameter that is documented as *decode-refuted*, not merely *not fitted*.
4. **Add `limitN` / `limitChampionN` capacity to the count model (`D-V-4`).** This is the only
   decoded change that moves a number in the band: **−11.500** bodies. Capacity semantics: sum the
   per-entry limits over level-eligible entries; an entry with no limit field is unbounded; the
   emit loop **stops** when capacity is exhausted, including inside the `spawnMin` top-up.
5. **Correct `D-V-2` (adj outside the modifier) and `D-V-3` (champion conversion + gate bypass) for
   correctness.** Both are measured **exactly inert** over 151–160.
6. **Expected band totals to reproduce:** decoded p06-OFF **172.083**, decoded p06-ON **197.083**.
   Per-wave expectations in § 4.1 and machine-readable in `pm4v_prediction.json`.

### 7.2 DO-NOT (the § 8 pattern, carried from Lap U)

* **DO NOT fold `F-3M-1`.** The `ProxyAmbush` at p05 is a **HALT trigger**, not a lap deliverable.
  Folding a 30-body group-size term because it would help is precisely the move the run's laws
  exist to prevent.
* **DO NOT treat § 3's numbers for waves 151, 152, 153, 156, 157, 158, 159 as decode-complete.**
  They carry the unmodelled p05 term (§ 6.1). Waves 154, 155, 160 are clean.
* **DO NOT adopt a `bonusSpawnStatus` limb on the grounds that it grades better.** It is a fixture
  fact; the only legitimate resolutions are a Matt answer or the `R-V-1` video route.
* **DO NOT price `F-5`/`D-V-3` as a count change.** It is exactly inert in the band (`F-6`), and
  quoting it as a count movement would put a real mechanism behind a false number.
* **DO NOT read `roster ≥ 19` as "the referent band is reached."** 19–36 is a count of **living**
  bodies and it is a **LOWER** bound. Roster is a ceiling. Even at G-1 = 7/10, the concurrency
  functional has to survive the player's kill throughput, which is gamora's seam and not measured
  here.
* **DO NOT re-derive `⌊(spawnMin + 1) × 1.20⌋`.** It is decoded (§ 2.5), it is branch A, and it is
  the same value the sim already computes.
* **DO NOT carry u9 § 5.2's doubled-boss claim into anything.** It is `D-V-1`, and it is wrong.

---

## § 8 — DIGESTS (full 64 hex throughout, `R-PM4-55 part 2`)

### 8.1 Outputs of this lap

| artefact | sha256 |
|---|---|
| `PREREGISTRATION.md` (committed alone, `cfa2e01c`) | `48754f273073887a55ef8cad025fa79cc3f03db07a9dee4b76264f85773b1d07` |
| `pm4v_prediction.json` (**hashed before the grade**) | `450d52c9c5c430b528d1e2435760ff2ed45dec60c53a3b1981c20cc9701e275b` |
| `pm4v_grade.json` | `405bcb712d2a81bd8230f5e68d710045c80ea05cfecea25922e007a0ce85c332` |
| `pm4v_roster_arithmetic.csv` (139 alternative-rows) | `991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c` |
| `pm4v_bonusspawn.json` | `7c8d0b732d947c60c1a9344f3130482513195486f20ff49f6173ecd33fb84aa4` |
| `pm4v_countmodel.json` | `2c55a87e105e416004e4d9552812ab288e3e37d1528d7fd01ef3a9629894de7d` |
| `pm4v_digests.json` | *(covers all of the above; recomputed at commit)* |

### 8.2 Inputs, pinned and verified at instrument start (HALT on mismatch; none fired)

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

Both binary digests are **byte-identical to Lap U's pinned values**, so `F-3`–`F-8` were decoded
out of the same bytes that decided `U-T-1`.

### 8.3 Instruments

| instrument | role |
|---|---|
| `agentic_orchestration/research/scripts/pm4v_roster_2026_08_15.py` | I-V1/2/3 — Lua decode, record census, decoded recipe, **prediction emitted and hashed** |
| `agentic_orchestration/research/scripts/pm4v_grade_2026_08_15.py` | I-V4 — incumbent comparator + **the grade, gated on re-hashing the prediction** |
| `…/gd_arz_adapter_2026_07_24.py`, `…/gd_arc_reader_2026_07_26.py`, `…/pm4s_pe_2026_08_14.py` | carried readers, unmodified (NOTE-9) |

*Lap V closed by legolas (UNKNOWN-RESEARCHER), 2026-08-15. Read-only throughout; nothing outside
this notes directory and `research/scripts/` was written.*
