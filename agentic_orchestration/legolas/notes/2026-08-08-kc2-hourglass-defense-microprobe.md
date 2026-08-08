# KC2-SIM Phase-B micro-probe — hourglass semantics · defense duration · mutator 5-vs-6 — 2026-08-08

**Probe:** Phase B micro-probe (KC2-SIM autonomous run) · **Conductor:** gandalf · **Agent:** legolas (UNKNOWN-RESEARCHER)
**Mode:** A (analytical / primary-source measurement) · **Access:** read-only throughout. Nothing committed.
**Scratch:** `agentic_orchestration/legolas/scratch/2026-08-08-hourglass/`

---

## CORPUS PROVENANCE (L-2 standing check)

**Tree read:** `~/Games/vendor/grim-dawn-edition-II-20260724/` — **verified as the Edition-II pin.**
Eight `.arz` archives, merged campaign-then-survival stack, **84,663 records**:

| archive | bytes | SHA-256 (first 16) |
|---|---:|---|
| `database/database.arz` | 58,338,379 | `8cdeff128422c765` |
| `gdx1/database/GDX1.arz` | 42,398,951 | `e28ab2515477ac80` |
| `gdx2/database/GDX2.arz` | 33,106,854 | `f6d5bd67602ce5af` |
| `gdx3/database/GDX3.arz` | 47,334,429 | `1661be5ef6db1f08` |
| `mods/survivalmode/database/SurvivalMode.arz` | 7,052,806 | `e55b760f36ab80a6` |
| `survivalmode1/database/SurvivalMode1.arz` | 2,459,167 | `6df94d3be33e600c` |
| `survivalmode2/database/SurvivalMode2.arz` | 2,351,568 | `940e40344e9dde53` |
| `survivalmode3/database/SurvivalMode3.arz` | 3,919,713 | `b4aa2d78675c4f05` |

**FoA/1.3.0.0 marker confirmed:** `tier18waves` 55 · `tier19waves` 56 · `tier20waves` 55 spawn-point
proxies present (absent from both pre-FoA cuts). This is the Edition-II tree, not Edition-I and not the
full-install depot.

**Second tree, named because part of the evidence comes from it:** the Crucible **Lua** is *not* in
Edition-II (Edition-II is a curated `.arz` + `Text_EN.arc` subset). The wave sequencer, bonus-timer and
mutator-ladder source were read from the banked extraction of `~/Games/vendor/grim-dawn/` (depot
2026-07-23, **pre-FoA**) at `legolas/scratch/2026-08-07-u8-tierwave/lua/` — U-8's **gap G1**, still open
and still named. Everything read from the `.arz`, the UI records and the tag tables in this note is
Edition-II. **See § 1.6: the camera itself now closes the currency question on the pre-FoA formula.**

---

## VERDICT BLOCK

| # | Question | Verdict |
|---|---|---|
| **1** | Hourglass field `x1490..1532, y105..120` | **(a) — the Crucible BONUS TIMER. CLOSED.** Formula-only prediction was **185.13 s at wave-151 start → 03:02 at t=685**; galadriel read **03:02**. Match to 0.2 s. The 01:31→01:34 refresh is **a hero kill (+4000 ms) net of ~1 s countdown = +3**, uniquely. |
| **2** | Do the four defenses carry a lifetime/expiry? | **NO. Permanent for the run. Hypothesis (b) FALSIFIED — the death-confound does not exist.** `lifeTime = 0` on all 15 defense DBRs; no skill anywhere spawns them (so no TTL vector); Crate's own comment: *"permanently saved into the world once spawned."* |
| **3** | Mutator count 6 (source) vs 5 (camera) | **Ladder confirmed 6 at full grain — "ladder misread" FALSIFIED. "Icon-less mutator" FALSIFIED** (27/27 packs carry a distinct bitmap). Data supports a **display-side cause**, and names two concrete mechanisms with measurements attached: the icon pane is authored **300 px wide** (5 icons of 48 px fit; 6 do not), and galadriel's 140 px-wide badge crop covers **only 47 % of that pane's width**. |

**One residual, stated plainly and pre-registered as a test, not smoothed over:** the formula cannot
produce `00:00` at t=900. Earliest possible zero-crossing in wave 160 is **t = 919.2**. See § 1.5.
This does not disturb verdicts 1 or 2.

---

## 1 — TASK 1: hourglass semantics

### 1.0 The formula, DB-CITED, quoted before any comparison

`survivalevent.lua :: SurvivalEvent_StartBonusTimer` (lines 452–484), with Crate's own comment:

```lua
local tier = gd.survival.eventControl.checkRewardTier()
-- if a checkpoint was used, override the tier, for MP purposes
if checkpointWave > 0 then tier = math.floor(checkpointWave / 10) end
local multiplier = Game.GetSurvivalMultiplier()
...
else                          -- Gladiator == Game.Difficulty.Ultimate
    defaultTimer = 80000
    tierBonus    = 12000
end
-- Default based on difficulty, adds time per reward tier, modified by current multiplier
local timer = (1 / ((multiplier + 1) ^ 0.49)) * (defaultTimer + (tier * tierBonus))
Game.SetSurvivalTimer(timer)                       -- SET, not accumulated
```

Called from **`SurvivalEvent_SpawnNext` line 521 — once per wave.** The only upward vector between
waves is `rewards.lua` lines 908–936, under the comment
`-- Increment the Bonus Timer when a Hero, Boss or Nemesis is killed`:

```lua
gd.survival.rewards.heroKilled()    -> Game.SurvivalTimerAdd(4000)
gd.survival.rewards.bossKilled()    -> Game.SurvivalTimerAdd(8000)
gd.survival.rewards.nemesisKilled() -> Game.SurvivalTimerAdd(12000)
```

*(This verifies U-8 § 4.4's `+4 / +8 / +12 s` claim at its exact call site. It was correct.)*

Two further zeroing paths, both outside the window in question: `Game.SetSurvivalTimer(0)` at tier
completion (line 748, `-- Pause Bonus Timer`) and `Game.ResetSurvivalTimer()` on event failure
(line 779, fires at death).

### 1.1 PRE-REGISTERED PREDICTION — stated from the formula alone

Fixture inputs: Gladiator; M1 checkpoint start; `Game.SetSurvivalWaveTier(151)` and
`checkpointActivated(151)` both fire before the event starts, so `checkRewardTier() = ⌊151/10⌋ = 15`
**and** the checkpoint override `⌊151/10⌋ = 15` — the two paths agree, no ambiguity.

```
base   = defaultTimer + tier × tierBonus = 80 000 + 15 × 12 000 = 260 000 ms
T(m)   = 260 000 / (m+1)^0.49
T(1)   = 260 000 / 2^0.49 = 260 000 / 1.404432 = 185 124 ms = 185.12 s = 03:05
```

1. **Initial value = 185.12 s (03:05)**, counting down in real time from the run start.
2. **Hard SET at every wave start**, not accumulation — the value *falls* wave over wave as the
   multiplier climbs, and any unspent remainder is discarded.
3. **Mid-wave upward steps only in {+4, +8, +12} s**, on hero / boss / nemesis kills.
4. **Floors at zero and stays there** until the next `SpawnNext`.
5. Predicted display at galadriel's sample t = 685 (run start 682.10 → 2.90 s elapsed):
   **185.12 − 2.90 = 182.22 s = `03:02`.**

### 1.2 CHECK — and the reading is a three-way lock, not a one-way fit

| galadriel | predicted from formula | Δ |
|---|---|---|
| `03:02` at t = 685 | `03:02` (182.22 s) | **≤ 0.2 s — inside one 1 Hz display tick** |

The value is diagnostic, not merely compatible. Every neighbouring cell of the parameter grid misses:

| perturbation | predicted display at t=685 | |
|---|---|---|
| multiplier m = 0 | `04:17` | ✘ |
| **m = 1, tier 15, Gladiator** | **`03:02`** | **✔** |
| m = 2 | `02:28` | ✘ |
| m = 3 | `02:08` | ✘ |
| tier 14 (i.e. wave 149) | `02:53` | ✘ |
| tier 16 (i.e. a wave-160 start) | `03:10` | ✘ |
| Challenger difficulty | `02:47` | ✘ |
| Aspirant difficulty | `02:37` | ✘ |

So one HUD frame independently re-confirms **three** things the run already held on other evidence:
**Gladiator**, **rewardTier = 15 at the first fought wave** (hence U-8's `first_wave_fought = label + 1`,
since a wave-150 first-fought would still read tier 15 but a *tier-16* base would read 03:10), and
**the multiplier starts at 1, not 0.**

### 1.3 The upward refresh — resolved to the exact event class

The timer is SET, never added-to, at a wave boundary; a wave clear therefore produces a **jump to a new
full value**, not a nudge. A `+3 s` nudge can only be a mid-wave `SurvivalTimerAdd` net of countdown:

```
Δdisplay = bonus − Δt_real ,   with Δt_real ≈ 1.0 s between the two samples
```

| kill class | bonus | predicted Δdisplay over a 1.0 s gap |
|---|---:|---:|
| **hero** | **+4 s** | **+3** ✔ observed |
| boss | +8 s | +7 |
| nemesis | +12 s | +11 |

**`01:31 → 01:34` across t=797–798 is a hero kill.** Uniquely — the three classes are 4 s apart and the
observed step is exact. It lands 1.4–2.4 s before wave 157's clear at 799.43, exactly where a wave's
last dangerous kill sits. This is a second, independent confirmation of hypothesis (a) using a
*different term of the same formula*.

### 1.4 Hypotheses (b) and (c) — falsified on the HUD inventory alone, before § 2 even runs

`tags_survivalui.txt` is the Crucible's own UI string file. It defines **exactly five** HUD readouts,
and no others:

| tag | text | rollover |
|---|---|---|
| `tagHUDWaveTier01` | Current Wave | *"The Wave of Monsters you are currently fighting."* |
| **`tagHUDTimer01`** | **Bonus Timer** | *"If you defeat a Crucible Wave before this timer expires, the Score Multiplier will increase."* |
| `tagHUDMultiplier01` | Score Multiplier | *"…based on how many consecutive Bonus Timers you beat. If you fail to beat the Bonus Timer, the Multiplier resets."* |
| `tagHUDScore01` | Score | |
| `tagHUDTribute01` | Tributes | |

Corroborated by the pane record itself, `records/ui/survivalpane/survivalpane_table.dbr` [sm_mod],
35 fields — one and only one timer element (`survivalTimer` + `survivalTimerGlow` +
`survivalTimerRollover`), and **two sounds that only a failing countdown needs**:

```
timerTenSecondsSound = records/sounds/spak_bonustimer10sleft.dbr
timerFailedSound     = records/sounds/spak_bonustimerfailed.dbr
```

**⇒ (c) is falsified for both named candidates.** There is no mutator timer (mutators are rolled once
per tier at `SurvivalEvent_Start` line 435 and carry no duration — § 3), and there is no checkpoint
timer anywhere in the survival Lua, the survival UI records, or the survival tag tables. The in-game
clock is `hudClockText`, a 12-hour wall clock (galadriel read it as `9:40:45 PM` for her timebase check)
— it cannot read `00:00` and is not mm:ss.

**Geometry, as corroboration** (both panes are top-right anchored; at the videos' native 1920×1080):

| pane | record | extent | offset (R/T) | ⇒ box |
|---|---|---|---|---|
| survival pane | `survivalpane_table.dbr` [sm_mod] | 378 × 128 | 10 / 40 | x **[1532, 1910]**, y **[40, 168]** |
| mutator icon row | `infoiconpane_table.dbr` [base, gdx2] | 300 × 50 | 90 / 135 | x **[1530, 1830]**, y **[135, 185]** |

galadriel's hourglass box `x 1490..1532, y 105..120` is **vertically inside the survival pane's band**
and **outside the icon row's**, and its right edge coincides with the pane's left edge to the pixel.
The ~42 px horizontal offset is a *reconciliation item* (text justification / UI scale / alignment
convention), **not** a challenge to the verdict — the arithmetic in § 1.2 and § 1.3 carries that on its
own. Flagging it so nobody re-derives it as a discrepancy.

### 1.5 THE ONE RESIDUAL — pre-registered as a falsifiable test

The wave-160 timer is SET at t = 838.87 (galadriel § 2.2). Death at 943.60, 104.73 s later. The run
cleared waves 151–159 = 9 consecutive beaten timers, so with a +1-per-beaten-timer ladder the multiplier
is at most **10** at wave 160 (the pane ships bitmaps `survivalpane_multiplier01…10`, so 10 reads as the
display ceiling). Kill bonuses inside wave 160 can only push the zero-crossing **later**.

| m at wave 160 | T(m) | zero-crossing | display at t = 900 |
|---:|---:|---:|---:|
| 6 | 100.20 s | 939.07 | 00:39 |
| 8 | 88.59 s | 927.46 | 00:27 |
| 9 | 84.13 s | 923.00 | 00:23 |
| **10 (ceiling)** | **80.30 s** | **919.17** | **00:19** |

**Prediction: the field is NON-ZERO at t = 900 — between `00:19` and `00:47` — and reaches `00:00`
no earlier than t = 919.2.** If galadriel's fuller series confirms a literal `00:00` at t = 900, then
either the multiplier is uncapped internally and far above 10 (≈20 would be needed), or the 1.3.x
client changed the formula relative to the pre-FoA Lua (gap G1). **Neither outcome resurrects
hypothesis (b)** — § 2 kills that independently, at the record level.

Cross-check on the one mid-wave sample, reported honestly as *consistent-with-slack, not a lock*:
at t=797, wave 157 (start 780.30, 16.70 s elapsed), `m = 7` predicts 93.86 − 16.70 = 77.2 s, so the
observed `01:31` (91 s) implies ≈ +13.8 s of accrued hero kills — ~3 heroes, plausible for a Gladiator
tier-16 wave. `m = 5` predicts 91.4 s with *zero* accrued bonus, also a clean fit. **A single mid-wave
sample cannot separate them.**

### 1.6 The clean measurement to hand back — the timer is a multiplier read-out

Because the timer is **SET** at `SpawnNext`, the frame immediately after each badge flip shows
**exactly `T(m)`, with no kill-bonus contamination**. That inverts:

```
m = (260 000 / T_ms) ^ (1/0.49) − 1
```

So one sample per wave boundary measures the multiplier ladder to the integer. Predicted values under
the +1-per-clear assumption, against galadriel's own boundary times:

| wave | t_start | assumed m | predicted display at t_start |
|---:|---:|---:|---:|
| 151 | 682.10 | 1 | `03:05` |
| 152 | 698.38 | 2 | `02:31` |
| 153 | 714.83 | 3 | `02:11` |
| 154 | 729.62 | 4 | `01:58` |
| 155 | 743.75 | 5 | `01:48` |
| 156 | 760.08 | 6 | `01:40` |
| 157 | 780.30 | 7 | `01:33` |
| 158 | 799.43 | 8 | `01:28` |
| 159 | 812.62 | 9 | `01:24` |
| 160 | 838.87 | 10 | `01:20` |

Ten pre-registered numbers. If they land, the multiplier ladder is closed and § 1.5's residual resolves
with them; if they don't, the deviation *is* the measurement of how the real ladder differs.

**Bonus closure, unasked-for: this is what re-validates the pre-FoA Lua for the 1.3.0.5 client.** U-8's
gap G1 says the Crucible source on disk predates FoA. The `03:02` hit and the `+3` hit are two
independent confirmations, taken *from the fixture's own 1.3.0.5 client*, that
`StartBonusTimer` and `SurvivalTimerAdd` are **unchanged**. G1 narrows accordingly.

---

## 2 — TASK 2: defense-duration narrow read (G-6 carve-out) — **NO EXPIRY. Hypothesis (b) is dead.**

Scope held: the four fixture defenses only. Blessings untouched, per charter.

**Fixture loadout → records** (camera-verified purchase ledger, galadriel § 1; type mapping from
`defenses.lua` line 22, `-- 0 = No Spawn, 1 = Defense Banner, 2 = Offense Banner, 3 = Fire Turret,
4 = Ice Turret, 5 = Lightning Turret, 6 = Wall`):

| defense | record | `lifeTime` |
|---|---|---:|
| Deathchill Beacon | `records/creatures/defenses/turret_ice.dbr` [sm_mod] | **0** |
| Stormcaller Beacon | `records/creatures/defenses/turret_lightning.dbr` [sm_mod] | **0** |
| Inferno Beacon | `records/creatures/defenses/turret_fire.dbr` [sm_mod] | **0** |
| Vanguard Banner | `records/creatures/defenses/banner_offense.dbr` [sm_mod] | **0** |

**Five independent lines, all agreeing:**

1. **`lifeTime = 0` on all fifteen** defense DBRs (5 types × 3 upgrade tiers), not just the four.
2. **The field is live, so 0 is a real "no expiry", not an absent feature.** Scanned all 5,311
   `records/creatures/` records: 3,099 carry `lifeTime`; **exactly 2 are non-zero** — a 5 s
   `mummyskeleton_a01` and a 1 s `zombie_a01_doa`, both scripted corpse props. The engine honours the
   field; the defenses set it to zero.
3. **There is no TTL vector at all, because no *skill* spawns a defense.** Grim Dawn expresses summon
   lifetimes as `spawnObjectsTimeToLive` on the spawning skill. I swept all 84,663 records for
   references to `creatures/defenses/`: **124 hits, every one an asset path** (mesh / texture / anim) or
   the `characterAttributeEquations` bio record — **zero `spawnObjects*` entries.** The only spawn path
   is `Entity.Create(...)` in `defenses.lua`, which takes no lifetime argument.
4. **Crate says so, four times, in a repeated developer comment** — once per defense point:
   `-- Defense Points spawn monster entities, which are permanently saved into the world once spawned`,
   and at the module head, `-- Once spawned, a defense cannot be replaced and its associated NPC is
   despawned`.
5. **The only destruction path is run reset.** `gd.survival.defenses.resetVariables()` (line 577) is the
   single place a defense entity is `:Destroy()`ed, and it is called from exactly one site —
   `eventcontrol.lua` line 621, at run reset. **Not on a timer, not per wave, not per tier.**

**The durations that DO exist are per-cast effect windows, and all are ≤ 10 s** — two orders of
magnitude off the observed countdown's scale, and periodic rather than terminal:

| skill | class | `skillActiveDuration` | cooldown |
|---|---|---:|---:|
| `banneroffense_frenzy_buff` | SkillBuff_Passive | 5–8 s | 15 s |
| `turretlightning_stormcaller` | Skill_BuffAttackRadiusLightning | 8 s | 15 s |
| `turretfire_firestorm` | Skill_BuffAttackRadiusDrop | 5 s | — |
| `turretice_chillingsurge_buff` | SkillBuff_Debuf | 4 s | — |
| `banneroffense_aura_buff` | SkillBuff_Passive | **none** (toggled radius aura) | — |

Note also that **three of the four defenses grant the player nothing to expire**: the Beacons' skill
lists are attack skills plus self-passives (`passiveproperties_defense`, `armorbase03`,
`turretice_icebolt` …). Only the Vanguard Banner touches the player, and its aura is
`Skill_BuffRadiusToggled` — on/off by proximity, with no duration field at all.

> **Ruling: the four defenses were live from placement (t ≈ 476.8–509.6, prep phase) until the death at
> t = 943.60. They cannot have expired ~45 s before the wave-160 death. The first-order confound
> galadriel flagged does not exist.** Her § 2.2 hazard is discharged.
>
> The *positional* confound she raised in § 1a is untouched by this and still stands — Deathchill's
> −OA, Inferno's −damage-dealt and Stormcaller's −resistance are permanent but **range-limited**, so
> they remain a per-wave confound that depends on where each fight happened. Permanence makes them
> *more* consistently present, not less confounding.

---

## 3 — TASK 3: mutator list and the 5-vs-6

### 3.1 The ladder, re-read at full grain — **6 is correct. "Ladder misread" is FALSIFIED.**

`survivalevent.lua :: SurvivalEvent_SelectMutators` (lines 325–360), verbatim ladder:
`≥17 → 7 · ≥15 → 6 · ≥13 → 5 · ≥11 → 4 · ≥9 → 3 · ≥6 → 2 · ≥3 → 1 · else 0`.

At the fixture's wave-151 checkpoint start **both** inputs give 15 — `checkRewardTier()` reads
`Game.GetSurvivalWaveTier() = 151 → ⌊151/10⌋ = 15`, and the checkpoint override reads
`⌊checkpointWave/10⌋ = ⌊151/10⌋ = 15`. They **agree**; there is no divergence to exploit.
`SelectMutators()` is called from **exactly one site**, `SurvivalEvent_Start` line 435 — i.e. **once per
tier**, under the comment `-- Select Mutator(s) for the set of rounds`. So **6 for the whole 151–160
band**, not 6-then-something-else.

**Composition, DB-CITED and load-bearing for the count question** (`MutatorRandomizer`, lines 243–249):
`mutatorCount ≥ 6 → playerMutatorCount = 2`, remainder monster. **The six are 2 player + 4 monster.**

**Off-by-one found in passing, reported because it changes the pool the sim should sample from.** Both
selection loops guard with `if rand < total…` where `rand = random(1, total)`:

```lua
local rand = random(1, totalMutatorsPlayer)     -- 1..10
if rand < totalMutatorsPlayer then              -- 1..9 only
```

⇒ **`mutatorpak_player_10` (Voidmarked) and `mutatorpak_monster_17` (Vengeful) can never be selected.**
The effective pool is **9 player + 16 monster = 25**, not 27. The `while` loop still reaches the target
size, so this does **not** reduce the count — but a sim sampling the full 27 would be wrong.

### 3.2 The pool at rewardTier 15/16 on Gladiator — all 27 packs

The pool is **not** tier- or difficulty-filtered; difficulty selects the *magnitude* variant
(`normalMutator` / `eliteMutator` / `ultimateMutator` → Gladiator = `ultimateMutator`). Same 25
selectable entries at every tier ≥ 3; only the **count** changes.

**Monster mutators** (`affectsPlayers = false`):

| # | name | effect | icon |
|---:|---|---|---|
| 01 | Aetherwarped | Monsters deal additional Aether damage. | `mutatoricon_monster01_aetherwarped.tex` |
| 02 | Berserking | Attack faster and deal additional Bleeding damage. | `…monster02_berserking.tex` |
| 03 | Brawling | Additional Physical damage. | `…monster03_brawling.tex` |
| 04 | Brutal | Additional Pierce damage. | `…monster04_brutal.tex` |
| 05 | Corrupted | Additional Chaos damage. | `…monster05_corrupted.tex` |
| 06 | Crippling | Monster attacks Slow opponents. | `…monster06_crippling.tex` |
| 07 | Cruel | Monster attacks cripple opponents' Damage. | `…monster07_cruel.tex` |
| 08 | Ignited | Infused with Fire; additional Burn damage. | `…monster08_ignited.tex` |
| 09 | Leeching | Leech health back with every attack. | `…monster09_leeching.tex` |
| 10 | Poisonous | Additional Poison damage. | `…monster10_poisonous.tex` |
| 11 | Reckless | Increased Attack Speed. | `…monster11_reckless.tex` |
| 12 | Regenerating | Increased Health, highly enhanced Health Regeneration. | `…monster12_regenerating.tex` |
| 13 | Swift | Increased Speed. | `…monster13_swift.tex` |
| 14 | Time-Warped | Greatly reduced Spell Cooldowns, increased Casting Speed. | `…monster14_timewarped.tex` |
| 15 | Toughened | Greatly increased Health. | `…monster15_toughened.tex` |
| 16 | Unstoppable | Cannot be Slowed. | `…monster16_unstoppable.tex` |
| 17 | Vengeful | Increased Damage, greatly increased Retaliation. | `…monster17_vengful.tex` — **unreachable, § 3.1** |

**Player mutators** (`affectsPlayers = true`) — **two of the fixture's six are from this list**:

| # | name | effect | icon |
|---:|---|---|---|
| 01 | Accelerated | Player Cooldowns are reduced. | `mutatoricon_player01_accelerated.tex` |
| 02 | Aethermarked | More Resistant to Aether. | `…player02_aethermarked.tex` |
| 03 | Armored | Increased Armor. | `…player03_armored.tex` |
| 04 | Ascended | Deal increased Damage. | `…player04_ascended.tex` |
| 05 | Blessed | More Resistant to All damage. | `…player05_blessed.tex` |
| 06 | Mighty | Critical Strikes are extra lethal. | `…player06_mighty.tex` |
| 07 | Resilient | More Resistant to Poison and Bleeding. | `…player07_resilient.tex` |
| 08 | Sprinting | Move faster. | `…player08_sprinting.tex` |
| 09 | Vigorous | Increased Health. | `…player09_vigorous.tex` |
| 10 | Voidmarked | More Resistant to Chaos. | `…player10_voidmarked.tex` — **unreachable, § 3.1** |

**Sim note, unsolicited:** four of the six are hostile and two are *helpful to the player*. A sim that
models Crucible mutators as a pure difficulty tax will over-punish by exactly the 2-player-mutator term.

### 3.3 The reconciliation — what the data supports

| candidate | verdict | basis |
|---|---|---|
| **ladder misread** | **FALSIFIED** | § 3.1 — re-read at full grain; both tier inputs give 15; ladder gives 6; one call site |
| **one mutator icon-less** | **FALSIFIED** | **27/27** packs carry a distinct, non-empty `bitmapName` under `ui/hud/mutatoricon_*.tex`. No duplicates, no blanks. |
| **UI row caps at 5** | **SUPPORTED, with a named uncertainty** | see below |
| **row clips off-crop** | **SUPPORTED, with a measured mechanism** | see below |

**The pane is authored 300 px wide.** `records/ui/infoiconpane/infoiconpane_table.dbr` [base, gdx2 —
**no survival override**; both `hud_mastertable` and `hud_orbmastertable`, which *are* sm3-overridden,
still point at it]:

```
defaultIconBitmap    = ui/infoiconpane/generic_mutatoricon.tex     <- this is the mutator row
iconSpacing          = 6
windowDefaultExtentX = 300      windowDefaultExtentY = 50
windowDefaultX       = 90       windowDefaultY       = 135
windowScreenAlignmentX = Right  windowScreenAlignmentY = Top
```

There is **no `maxIcons` field** — all 9 fields are listed above — so any cap is *extent-driven*:

| icon width | 5 icons need | 6 icons need | fits in 300 px |
|---:|---:|---:|---|
| 40 px | 216 | 270 | 6 |
| 44 px | 244 | 294 | 6 |
| **48 px** | **264** | **318** | **5 only** |
| 50 px | 274 | 330 | 5 only |

`windowDefaultExtentY = 50` bounds the icon height at ≤ 50, and GD HUD icons are square — so 48 px is
the natural read, and at 48 px **the pane holds exactly five and overflows at six.** **Uncertainty
named:** the `.tex` dimensions are **not in Edition-II** (no UI resource archive in the cut), so 48 px
is inferred from the pane height, not measured. This is the leading hypothesis, not a closure.

**And the crop can produce it by itself.** At 1920 px the row spans **x [1530, 1830]**. galadriel's
badge ROI is `crop=140:50:1550:125` → **x 1550..1690**, i.e. **140 of the row's 300 px = 47 %**, missing
the leftmost icon's start and everything past 1690. Any icon count taken from a crop of that geometry
undercounts systematically.

**Recommended read, which converts a count into an identification and settles it either way:** re-crop
**x 1510..1850, y 125..195** (row box plus margin) at a timestamp **≥ 5 s after** run start —
`notifyPluralMutators` fires at selection and the row may still be animating in at t=684, 1.9 s after
t=682.10. Then match each icon against the 27 filenames in § 3.2. The outcome is decisive:
**{2 player + 4 monster} = 6** ⇒ the earlier count was crop-limited; **5 identified with the 6th absent
at the pane's right edge** ⇒ extent-driven overflow, and § 3.2's 48 px inference is confirmed.

---

## 4 — Gaps, stated plainly

| # | Gap | Impact |
|---|---|---|
| **G1** (inherited, U-8) | `SurvivalMode3`'s Lua is not on disk; the timer formula and mutator ladder are read from the **pre-FoA** cut. | **Reduced by this probe.** Two independent camera hits (§ 1.2, § 1.3) taken on the fixture's own 1.3.0.5 client confirm `StartBonusTimer` and `SurvivalTimerAdd` are unchanged. |
| **G5** (new) | Mutator icon `.tex` pixel dimensions are absent from Edition-II (no UI resource archive). | The 5-vs-6 geometric argument (§ 3.3) rests on a 48 px inference. One re-crop closes it. |
| **G6** (new) | The multiplier's increment rule and its true internal ceiling are engine-side; the UI ships bitmaps for x1…x10 only. | Bounds § 1.5's residual. § 1.6's ten pre-registered numbers measure it directly. |

**No gap touches the § 2 verdict** — the defense records are Edition-II, read directly, at full grain.

---

## 5 — Grade summary

| # | Target | Verdict | Provenance |
|---|---|---|---|
| 1 | Hourglass = Bonus Timer | **CLOSED — (a)** | **DB-CITED** (`StartBonusTimer` + `SurvivalTimerAdd` + `tagHUDTimer01` + `survivalpane_table`) **× CAMERA-CONFIRMED** twice, both pre-registered |
| 1b | (b) defense/blessing duration readout | **FALSIFIED** | **DB-CITED** — the Crucible UI file defines five readouts and one timer |
| 1c | (c) mutator / checkpoint timer | **FALSIFIED** | **DB-CITED** — no such timer exists in the survival Lua, UI records or tags |
| 2 | Defense lifetime / expiry | **CLOSED — none; permanent for the run** | **DB-CITED** ×5 independent (`lifeTime=0` ×15 · live-field control scan 5,311 records · zero `spawnObjects` refs in 84,663 · Crate's ×4 repeated comment · single `resetVariables` destroy path) |
| 3 | Mutator pool + effects at tier 15/16 Gladiator | **CLOSED — 27 packs listed; 25 selectable** | **DB-CITED** (`mutatorpak_*` + tag resolution) |
| 3b | Count = 6, composition 2 player + 4 monster | **CLOSED** | **DB-CITED** (`SelectMutators` + `MutatorRandomizer`, single call site) |
| 3c | The 5-vs-6 discrepancy | **NARROWED to display-side; two mechanisms measured** | ladder + icon-less both FALSIFIED; pane extent 300 px and crop coverage 47 % both quantified |

---

**Signed:** legolas, 2026-08-08. The hourglass predicted itself: 185.12 seconds from Crate's own
constant, minus the 2.9 seconds the camera had been running — `03:02`, which is what the frame says.
The second hit is better than the first, because a `+3` step on a screen has no business matching a
`+4000` in a Lua file unless the two are the same object. And the defenses never had a clock on them at
all — Crate wrote *"permanently saved into the world"* four times, once per site, and meant it.
