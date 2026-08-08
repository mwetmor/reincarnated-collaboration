# PROBE U-9 — `spawnMinModifier` operator order on Crucible Gladiator

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-07 · **Mode:** A (analytical / primary-source probe), read-only
**Commissioned by:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, Phase A
**Corpus:** Edition-II `.arz` pin (2026-07-24, GD 1.3.0.0) **+ a newly-opened substrate lane** — see § 1
**Substrate read first:** `legolas/notes/2026-08-01-gd-pack-density-ranking.md`, `…/2026-08-04-gd-1305-patch-delta-probe.md`
**Reproducibility:** `legolas/scratch/2026-08-07-u9-spawnmin/` — `q1_findfields.py` … `q7_clamp.py`, plus extracted `tpl/` and `lua/`
**Grading key:** **DB-CITED** = read verbatim from the corpus · **DEV-DOC** = stated by Crate in published developer documentation · **DERIVED** = inference, operator stated · **UNRESOLVED**

---

## §0 — Headline

**The operator-order question is CLOSED on the axis that carries the money, and bounded to ±1.9 % on the axis that does not.**

`spawnMinModifier` is **multiplicative, expressed as a percentage in which 0 *or* 100 means "no change."** It is not additive, and it is not `+120 %`. On Gladiator the value is **120 → ×1.20**. This is not an inference: the field's semantics are declared in Crate's own template file, `database/templates/gameproxies.tpl`, which annotates `spawnMin`/`spawnMax`/`championMin`/`championMax` as **`"Additive"`** and `spawnMinModifier`/`spawnMaxModifier`/`championMinModifier`/`championMaxModifier` as **`"Percent (0 or 100) no change"`**. § 3.1.

Three further gates on the count model are likewise closed, two of them by Crate's published *Grim Dawn Modding Guide*:

1. **Player-count scaling does not exist in the count model.** The only hook where `numberOfPlayers` could enter is `proxyPoolEquation`, and **632 of 632** Crucible pools reference the identity record `proxypoolequation_01.dbr` (`poolValue * 1` on all four outputs). Crate: *"The default proxypoolequation_01.dbr is used for all Grim Dawn spawn pools."* Independently, `balancingadjustment_mp+difficulty_enemies01.dbr` is `Class = AttributePak` and carries **no spawn-count fields at all**. § 3.3.
2. **Champions ADD; they do not convert.** Crate: *"The distinction between the Regular and Champion Pools is solely for controlling their spawn counts… Spawn Min/Max: the number of monsters to spawn from the Regular Pool. Champion Min/Max: the number of monsters to spawn from the Champion Pool."* § 5.1.
3. **A per-pool exemption flag exists and the commission's model must carry it.** `ignoreGameBalance` — Crate: *"True/false check whether to use the difficulty modifiers that increase spawn count."* **74 of 632** Crucible pools set it, and they are exclusively boss pools. § 5.2.

**What remains open is small and I have measured how small.** Two sub-questions the database genuinely cannot settle — the intra-order of the additive term against the percentage, and the engine's clamp direction when `min' > max'` — move the *total monster count across the entire calibration window (waves 151–170)* by **5.5 monsters out of 292, or 1.9 %**. § 4.3.

**And one unbilled finding is four times larger than both residuals combined.** The Crucible's **6th spawn point is opt-in** — a player choice, not a constant. Verbatim from the Crucible's own Lua: `-- final spawn point is for bonus spawns, player chooses to enable this`. Across waves 151–170 it is worth **+8.4 %** monsters. If the sim hard-codes six spawn points it will over-count by more than four times the entire operator-order uncertainty. § 5.4.

---

## §1 — Why this closed: a substrate lane the corpus pin did not include

The Edition-II fetch contains `.arz` databases only. The **raw 2026-07-23 DepotDownloader fetch at `/Users/admin/Games/vendor/grim-dawn/`** contains two archives Edition-II omits, and both are decisive here:

| Archive | Size | What it holds | Prior status |
|---|---|---|---|
| `database/templates.arc` | 781 KB | **819 `.tpl` files** — Crate's own declaration of every DBR field's type, class and **`description`** | never opened |
| `mods/survivalmode/resources/Scripts.arc` | 73 KB | **24 plain-text Lua files** — the Crucible's wave sequencer, tier scripts, spawn call | declared UNRESOLVED |

Both are readable with the **existing** `gd_arc_reader_2026_07_26.py` (ARC v3, same LZ4 codec). No new tooling was required — only the recognition that the reader was pointed at `Text_EN.arc` alone.

**Join-safety of the raw fetch, verified before use (DB-CITED):**

| Archive | raw fetch | Edition-II | |
|---|---|---|---|
| `database/database.arz` | 58,338,379 B | 58,338,379 B | IDENTICAL |
| `mods/survivalmode/database/SurvivalMode.arz` | 7,052,806 B | 7,052,806 B | IDENTICAL |
| `survivalmode1/…/SurvivalMode1.arz` | 2,459,167 B | 2,459,167 B | IDENTICAL |
| `survivalmode2/…/SurvivalMode2.arz` | 2,351,568 B | 2,351,568 B | IDENTICAL |

Sizes are a weaker test than hashes and are reported as such, but they are consistent with the Edition-II cut record's own 11/11-identical-manifest finding. The raw fetch predates Edition-II by one day and lacks `gdx3`/`survivalmode3`; **every `.tpl` and `.lua` claim below is cross-checked against Edition-II `.arz` field presence**, so the version skew does not reach the findings.

> **Two prior-note gaps close as a side effect.** `2026-08-01-gd-pack-density-ranking.md` § "Knowledge gaps" recorded (2) *"Crucible tier → global wave number — the schedule is in game script, not data"* and § Q5 recorded that level geometry was absent. The schedule is now read directly (§ 2.4). And **`resources/Levels.arc` exists in the raw fetch** — the Q5 depot-pull recommendation is already satisfied on disk and should be re-costed rather than re-fetched. Not pursued here; out of commission scope.

---

## §2 — The records, verbatim

### 2.1 The difficulty scalar — `records/game/gameproxies.dbr`

There are **two** records at this path. Which one binds depends on whether you are in the campaign or the Crucible; the Crucible is a mod (`mods/survivalmode/`) and its copy overlays the base. **DB-CITED, complete, both records:**

```
[base]   records/game/gameproxies.dbr          (3 fields)
   spawnMax    = [0.0, 1.0, 1.0]
   championMax = [0.0, 2.0, 3.0]
   templateName = database/templates/gameproxies.tpl

[sm_mod] records/game/gameproxies.dbr          (6 fields)   <-- THE CRUCIBLE RECORD
   spawnMin         = [0.0, 0.0, 1.0]
   spawnMax         = [0.0, 1.0, 1.0]
   championMin      = [0.0, 0.0, 1.0]
   championMax      = [0.0, 1.0, 1.0]
   spawnMinModifier = [0.0, 112.0, 120.0]
   templateName     = database/templates/gameproxies.tpl
```

Array index is **`[Aspirant, Challenger, Gladiator]` = `[Normal, Epic/Elite, Ultimate]`** (§ 2.3 proves the binding). Neither `sm1`, `sm2` nor `sm3` carries a `gameproxies.dbr`, so the `sm_mod` record is the sole authority for all 200 Crucible waves.

**Two asymmetries, both load-bearing and both easy to miss:**

- **The Crucible record is materially different from the campaign record.** The campaign has no `spawnMin`, no `championMin`, and **no `spawnMinModifier` at all**. Any count intuition carried over from campaign datamining is wrong for the Crucible.
- **`spawnMaxModifier` is ABSENT from the record while PRESENT in the template.** Verified by explicit key check: `spawnMaxModifier`, `championMinModifier`, `championMaxModifier`, `difficultyModifier` and `championDifficultyModifier` are all declared in `gameproxies.tpl` and all **unset** in both records. Crate had the max-side percentage available and chose not to use it. **The max side is additive-only.** This is the answer to the commission's "companion max-side field if present": it exists in schema, it is unset in data.

A dev leftover at `sm_mod::records/game/copy of gameproxies.dbr` carries `championMax = [0, 2, 2]` against the live `[0, 1, 1]` — evidence the champion additive was tuned *down* late. Not authoritative; recorded so it is not mistaken for the live record.

### 2.2 The schema — `database/templates/gameproxies.tpl`, verbatim

This is the artifact that settles the question. Reproduced exactly:

```
Variable { name = "difficultyModifier"        class = "array" type = "real" description = "Percent (0 or 100) no change" }
Variable { name = "championDifficultyModifier" class = "array" type = "real" description = "Percent (0 or 100) no change" }
Variable { name = "spawnMin"                  class = "array" type = "real" description = "Additive" }
Variable { name = "spawnMax"                  class = "array" type = "real" description = "Additive" }
Variable { name = "spawnMinModifier"          class = "array" type = "real" description = "Percent (0 or 100) no change" }
Variable { name = "spawnMaxModifier"          class = "array" type = "real" description = "Percent (0 or 100) no change" }
Variable { name = "championMin"               class = "array" type = "real" description = "Additive" }
Variable { name = "championMax"               class = "array" type = "real" description = "Additive" }
Variable { name = "championMinModifier"       class = "array" type = "real" description = "Percent (0 or 100) no change" }
Variable { name = "championMaxModifier"       class = "array" type = "real" description = "Percent (0 or 100) no change" }
```

A sweep of **all 819 templates** (`q4_tplsweep.py`) confirms these ten strings are the *only* place in the shipped schema where either description appears against a spawn-count field, and that no other template redefines them.

### 2.3 The per-wave adjustment — and the Aspirant/Challenger/Gladiator binding

`records/game/survivalinfo.dbr` (sm_mod) names the three difficulty records explicitly. **DB-CITED:**

```
survivalAdjustmentNormal   = records/game/balancingadjustment_survivalmode_enemies01.dbr
survivalAdjustmentElite    = records/game/balancingadjustment_survivalmode_enemies02.dbr
survivalAdjustmentUltimate = records/game/balancingadjustment_survivalmode_enemies03.dbr
```

That is the binding: **Aspirant = Normal = index 0 = `…enemies01`; Challenger = Elite/Epic = index 1 = `…enemies02`; Gladiator = Ultimate = index 2 = `…enemies03`.** (Crate's own naming drifts across layers — `Elite` in the DBR field, `Game.Difficulty.Epic` in Lua, "Challenger" in UI text. All three denote index 1.)

These records use `database/templates/gameadjustment.tpl`, which declares a `"Spawns"` group of four **`int` arrays** — `spawnMinAdj`, `spawnMaxAdj`, `spawnChampionMinAdj`, `spawnChampionMaxAdj` — all with **empty descriptions**. Each array is **200 elements long**, matching the 200 Crucible waves exactly.

**Measured values (DB-CITED):**

| record | difficulty | `spawnMinAdj` | `spawnMaxAdj` | `spawnChampionMinAdj` | `spawnChampionMaxAdj` |
|---|---|---|---|---|---|
| `…enemies01` | Aspirant | **0 for all 200** | **0 for all 200** | 0 → 1 at idx 84 | 0 → 1 at idx 67 |
| `…enemies02` | Challenger | **0 for all 200** | **0 for all 200** | 0 → 1 at idx 67 | 0 → 1 at idx 51 |
| `…enemies03` | **Gladiator** | **0 for all 200** | **0 for all 200** | 0 → 1 at idx 67 | 0 → 1 at idx 51 |

**The per-wave adjustment contributes nothing to regular spawn counts on any difficulty.** It contributes **+1 champion floor and +1 champion ceiling** past the knees. Challenger and Gladiator are identical here; only Aspirant is softer.

*(Three `copy of …` and three `06-10-26 backup/…` variants exist with 150-element arrays and non-zero `spawnMaxAdj`. Dev leftovers, not referenced by `survivalinfo.dbr`. Recorded so a future crawl does not pick the wrong record.)*

### 2.4 The index of those arrays — and the tier→wave schedule

The Crucible's Lua names the indexing directly. **DB-CITED (Lua), `mods/survivalmode/resources/Scripts.arc :: game/events/survivalevent.lua` L505–510:**

```lua
-- Increment the Survival Mode Difficulty AttributePak rank. This happens every wave.
-- global monster stat modifier, stored in records/game/balancingadjustment_survivalmode_enemies01.dbr
if checkpointUsed then
    checkpointUsed = false
else
    Game.IncrementSurvivalDifficulty()
    -- Increment wave # on code end for score purposes
    Game.IncrementSurvivalWaveTier()
end
```

and at the checkpoints, `game/survival/eventcontrol.lua` sets rank and wave to the **same integer**:

```lua
Game.SetSurvivalWaveTier(51);  Game.SetSurvivalDifficulty(51)     -- wave 51
Game.SetSurvivalWaveTier(101); Game.SetSurvivalDifficulty(101)    -- wave 101
Game.SetSurvivalWaveTier(151); Game.SetSurvivalDifficulty(151)    -- wave 151  (sm1)
```

**The AttributePak rank IS the wave number**, incremented once per wave and pinned to the wave number at every checkpoint. The 200-element arrays are wave-indexed.

The tier→wave schedule — recorded as UNRESOLVED in the prior note — is a header comment in every tier script. **DB-CITED, complete:**

| tier | waves | | tier | waves | | tier | waves |
|---|---|---|---|---|---|---|---|
| 01 | 1–10 | | 08 | 71–80 | | 15 | 141–150 |
| 02 | 11–20 | | 09 | 81–90 | | 16 | **151–160** |
| 03 | 21–30 | | 10 | 91–100 | | 17 | **161–170** |
| 04 | 31–40 | | 11 | 101–110 | | 18 | 171–180 |
| 05 | 41–50 | | 12 | 111–120 | | 19 | 181–190 |
| 06 | 51–60 | | 13 | 121–130 | | 20 | 191–200 |
| 07 | 61–70 | | 14 | 131–140 | | | |

Tiers 1–17 are read verbatim from `-- Waves N through M for Survival Mode` comments (tiers 1–15 in `sm`, tiers 15–17 in `sm1`). **Tiers 18–20 are DERIVED**: `survivalmode2/resources/scripts.arc` is an empty container and the raw fetch has no `survivalmode3`, but tier ownership in the `.arz` (`sm3` alone owns tiers 18–20) plus the exact 200-element array length plus the unbroken ×10 pattern make the extension near-certain. Corroborated externally: the Grim Dawn wiki records 150 base waves and *"170 with the Ashes of Malmouth expansion"* — matching tier 17 = wave 170 precisely.

**Consequence for the calibration window:** waves 151–170 sit far past every adjustment knee (51, 67, 84). A **±1 ambiguity in whether the array is indexed by rank or rank−1 is irrelevant to this run** — every relevant value is deep in the saturated tail. Verified by direct read of indices 149–172 on `…enemies03`: `spawnChampionMinAdj` and `spawnChampionMaxAdj` are `1` throughout; `spawnMinAdj`/`spawnMaxAdj` are `0` throughout.

---

## §3 — The operator order

### 3.1 Additive vs multiplicative — **CLOSED**

**DB-CITED.** `spawnMinModifier` is a **percentage multiplier**, with **0 or 100 both meaning "no change."** On Gladiator, `120` means **×1.20**, *not* `+120` and *not* `×2.20`.

This refutes the only interpretation that would have materially broken the sim. Candidate C — reading the value as an additive-percent (`base × (1 + 120/100)` = ×2.20) — is **refuted by the template text**, which is explicit that 100 is the identity. The measured consequence of that refutation is large: on the densest calibration wave (158) candidate C would have produced roughly double the correct count.

The Aspirant value of `0` is *not* "zero monsters" — it is the second identity element the description names.

### 3.2 The intra-order — **UNRESOLVED, and bounded**

The template establishes *what each field is*. It does not establish the sequence in which the engine applies the additive term and the percentage. Two candidates survive:

| | formula (Gladiator: `add = +1`, `mod = 120`) |
|---|---|
| **A** add-then-multiply | `min' = trunc( (base_min + add) × mod/100 )` |
| **B** multiply-then-add | `min' = trunc( base_min × mod/100 ) + add` |

**Why the database cannot discriminate them.** The natural integrity constraint `min' ≤ max'` does not separate the candidates: applied across the 558 non-exempt Crucible pools, **A violates it 133 times and B violates it 121 times**. Both require the engine to clamp, so neither is excluded. (`q5_discriminate.py`.)

**Three things are nonetheless known about the residual, and they shrink it to near-nothing:**

1. **A and B are algebraically identical on Aspirant and Challenger.** `spawnMin = [0, 0, 1]` — the additive term is **zero** except on Gladiator, and `x + 0` commutes with any multiplication. The ambiguity exists on exactly one of the three difficulties.
2. **On Gladiator they differ only when `base_min ≡ 4 (mod 5)`**, and then by exactly 1. Measured: **39 of 558 pools (7.0 %) unclamped; 25 of 558 (4.5 %) after clamping.** The disagreeing pools are concentrated at base ranges 4–5, 4–6 and 9–11.
3. **Template group order weakly favours A.** `gameproxies.tpl` lists `spawnMin`, `spawnMax` *before* `spawnMinModifier`, `spawnMaxModifier`, and likewise `championMin/Max` before their modifiers. This is editor-layout order, not evaluation order, and is offered as **DERIVED, weak** — but it is the only DB-internal signal that exists, and it is the ordering a straightforward C++ implementation of that struct would produce.

**Recommendation: adopt A with truncation, and carry the residual as a declared ±1.9 % band (§ 4.3).**

### 3.3 Player-count scaling — **CLOSED: there is none**

The commission asks whether the modifier is applied before or after player-count scaling. **The question is void for the Crucible count model: player count never enters it.** Three independent legs:

1. **DB-CITED.** `proxypoolequation.tpl` exposes `numberOfPlayers` and `gameDifficulty` as equation variables — this is the one architectural hook where player count could reach a spawn count. **All 632 Crucible pools reference `records/proxies/proxypoolequation_01.dbr`**, whose complete content is:
   ```
   spawnMinEquation    = poolValue * 1
   spawnMaxEquation    = poolValue * 1
   championMinEquation = poolValue * 1
   championMaxEquation = poolValue * 1
   ```
   Identity on all four outputs. 632/632, zero exceptions.
2. **DEV-DOC.** Crate, *Grim Dawn Modding Guide*, "Spawn Pool": *"Proxy Pool Equation: Record reference for modifying the spawn min/max values. **The default proxypoolequation_01.dbr is used for all Grim Dawn spawn pools.**"*
3. **DB-CITED, measured absence.** `records/game/gameengine.dbr` names `playerAttributePak = records/game/balancingadjustment_mp+difficulty_players01.dbr`. That record and its sibling `balancingadjustment_mp+difficulty_enemies01.dbr` are `Class = AttributePak` / `attributepak.tpl` and carry **no `spawnMinAdj`/`spawnMaxAdj`/`spawnChampion*Adj` fields whatsoever**. Multiplayer scaling in Grim Dawn is a *stat* scalar (life, damage, resists), not a *count* scalar.

Our fixture is solo, so this would have been moot in practice; it is reported because it removes a term the sim might otherwise have carried speculatively.

### 3.4 Rounding — **UNRESOLVED, bounded**

`gameproxies.tpl` types the modifier arrays as `real`; `gameadjustment.tpl` types the adjustment arrays as `int`; `proxypool.tpl` types `spawnMin`/`spawnMax` as `int`. So a real-valued intermediate must be reduced to an integer, and the reduction is not declared anywhere in the shipped data.

`floor` (equivalently C truncation toward zero, since all quantities are non-negative) is the assumption carried below. Measured sensitivity across the 558 non-exempt pools: `floor` vs `round` changes A on **67 of 558 (12 %)** and always by 1; `ceil` is excluded on plausibility grounds — it produces 504/558 range violations, four times either alternative.

### 3.5 Clamp direction — **UNRESOLVED, and the larger of the two residuals**

Because every candidate produces `min' > max'` on tight pools, the engine must reconcile. Two branches: clamp the floor **down** to the ceiling (`min' := max'`) or raise the ceiling **up** to the floor (`max' := min'`).

**DERIVED, in favour of clamp-min-down:** Crate had `spawnMaxModifier` available in the same template, in the same group, with the same semantics — and deliberately left it unset while setting `spawnMinModifier`. The legible design intent is *"raise the guaranteed floor toward an unchanged ceiling"*, not *"raise the ceiling by a back door."* Under clamp-max-up, setting only the min-side modifier would silently do the max side's job, which would make the unset `spawnMaxModifier` field pointless.

Measured cost of being wrong: **+3 monsters across all 20 calibration waves** (295.0 vs 292.0 mid-range). § 4.3.

---

## §4 — The discrimination test

### 4.1 Worked examples — five concrete Crucible spawn pools

Gladiator, `add_min = +1`, `add_max = +1`, `mod = 120`, `spawnMinAdj = 0`. Cells are `floor / round / ceil` of `min'`.

| pool | base | IGB | **A** `(b+1)×1.2` | **B** `⌊1.2b⌋+1` | **C** `b×2.2 +1` *(refuted)* | `max'` |
|---|---|---|---|---|---|---|
| `poolsbasic/chthoniandevourer_t2` | 8–9 | 0 | 10/11/11 | 10/11/11 | 18/19/19 | **10** |
| `poolsbasic/skeletonranged_t2` | 7–8 | 0 | 9/10/10 | 9/9/10 | 16/16/17 | **9** |
| `poolsbasic/cultistchaos_t3` | 7–8 | 0 | 9/10/10 | 9/9/10 | 16/16/17 | **9** |
| `poolsbasic/aetherialabomination_t1` | 2–3 | 0 | 3/4/4 | 3/3/4 | 5/5/6 | **4** |
| `poolsbasic/aetherialabomination_t2` | 3–4 | 0 | 4/5/5 | 4/5/5 | 7/8/8 | **5** |

Reading: **A/floor and B/floor agree on four of five**; they part on `skeletonranged_t2` only after `round`. **C is grossly out of range on every row** — it exceeds `max'` by 6–9 monsters per pool, which is exactly why the template's "100 = no change" clause is the load-bearing sentence in this probe.

### 4.2 The design finding the test surfaced

Applying A/floor with clamp across all 558 non-exempt pools:

| | Aspirant | **Gladiator** |
|---|---|---|
| band-width histogram (`max'−min'`) | `{0: 381, 1: 156, 2: 21}` | `{0: 520, 1: 33, 2: 5}` |
| **deterministic pools (width 0)** | **381/558 = 68 %** | **520/558 = 93 %** |

**`spawnMinModifier` is a variance-suppression mechanism, not a volume mechanism.** Its effect is to drag the floor up against a ceiling that only moves by +1. On Gladiator **93 % of Crucible pools spawn a fixed count with no roll at all.** Two consequences worth carrying forward:

- **For the sim:** Gladiator wave counts are very nearly deterministic. The count model does not need a rich sampler; it needs the right constant.
- **For our own design (unbilled):** this is a clean, transferable idiom — *escalate difficulty by removing downside variance rather than by raising the cap.* The player experiences "always the bad case" instead of "sometimes a worse case."

### 4.3 The residual, measured on the calibration window

All four branches (order × clamp), Gladiator, solo, waves 151–170, 6th spawn point OFF:

| branch | Σ mid-range regular monsters, waves 151–170 |
|---|---|
| **A / clamp-min-down** *(recommended)* | **292.0** |
| A / clamp-max-up | 295.0 |
| B / clamp-min-down | 289.5 |
| B / clamp-max-up | 291.0 |
| *(expected champions, all branches)* | *63.0* |

**Maximum spread across every surviving interpretation: 5.5 monsters on 292 = 1.9 %.**

Per-wave, 12 of the 20 calibration waves are **identical under all four branches**; the largest single-wave divergence is 2 monsters (wave 161: 15–16 under A, 13–16 under B).

**Ruling for the conductor:** the residual is far inside any tolerance a monster-count calibration row would plausibly assert. **The count model does not need to be dropped to INFORMATIVE on account of U-9.** That disposition is yours; this is the evidence for it.

---

## §5 — Other count-affecting terms (commission Q4)

Five terms beyond `spawnMinModifier`. The sim will mis-count if it misses any of them.

### 5.1 Champions are additive, not conversions — **DEV-DOC**

The commission asks specifically whether champion/hero mechanics "convert rather than add." **They add.** Crate, *Grim Dawn Modding Guide*, "Spawn Pool":

> *"Spawn Pools are referenced by proxies to spawn a group of monsters. **The distinction between the Regular and Champion Pools is solely for controlling their spawn counts.** You can spawn a Champion monster from the Regular Pool. It makes no special distinction.*
> *· **Spawn Min/Max:** The number of monsters to spawn from the Regular Pool.*
> *· **Champion Min/Max:** The number of monsters to spawn from the Champion Pool.*
> *· **Champion Chance:** The chance of dispensing from the Champion Pool."*

Corroborated structurally in the data: `poolshero/chthoniandevourer_hero.dbr` has `spawnMin = spawnMax = 0`, `championChance = 100`, `championMin = championMax = 1`, and **`nameChampion1..7` with no `name1..N` roster at all**. It spawns exactly one hero and zero regulars — champions plainly are not drawn from the regular allotment.

**The champion-chance gate is safe to model as a hard gate.** Census over all 632 Crucible pools: **515** have `championChance = 0` **and no champion roster**; **117** have `championChance > 0` **and** a roster. **Zero pools** have a champion roster with `championChance = 0`. There is no case where a raised champion count could be realised on a pool that was not meant to have champions.

### 5.2 `ignoreGameBalance` — the per-pool exemption — **DEV-DOC + DB-CITED**

> Crate: *"**Ignore Game Balance:** True/false check whether to use the difficulty modifiers that increase spawn count. This is important for proxies that dispense a single entity, such as Aether Crystals, as otherwise several crystals could spawn on top of each other."*

**74 of 632** Crucible pools set it. The distribution is exact and clean:

| family | n | IGB=0 | IGB=1 |
|---|---|---|---|
| `poolsbasic` (+gdx1/gdx2) | 291 | **291** | 0 |
| `poolsbasicgdx3` | 25 | 24 | 1 |
| `poolshero` (all four) | 95 | **95** | 0 |
| `poolsboss` | 96 | 78 | 18 |
| `poolsbossgdx1` | 38 | 25 | 13 |
| `poolsbossgdx2` | 29 | 23 | 6 |
| **`poolsbossgdx3`** | 36 | **0** | **36** |
| `poolsdevotion` / `poolsbounty` (all) | 22 | 22 | 0 |

**Every exempt pool is a boss pool. No trash or hero pool is ever exempt.** Note the sharp policy change: all 36 Fangs-of-Asterkarn boss pools are exempt, while only 18 of 96 base-game boss pools are. **DERIVED:** the 78 non-exempt base-game boss pools, which are almost all `spawnMin = spawnMax = 1`, therefore resolve to `min' = max' = 2` on Gladiator — Crate's own Aether-Crystal warning says in so many words that this is what happens when the flag is off. Doubled bosses on Gladiator is a real and intended behaviour, not a modelling artefact.

### 5.3 Champion additives on Gladiator — a 3× hero multiplier

Composing § 2.1 and § 2.3 for waves 151–170:

```
championMin' = pool.championMin + gameproxies.championMin[2] + adj03.spawnChampionMinAdj[w]
             = 1              + 1                          + 1                        = 3
championMax' = 1              + 1                          + 1                        = 3
```

**Every hero placement in the calibration window spawns three heroes, not one.** `championMinModifier`/`championMaxModifier` are unset, so this term is purely additive and exact — no rounding, no clamp. Over waves 151–170 it accounts for an expected **63.0 champions** against 292 regulars, i.e. **~18 % of the wave population is champion-tier**, and two thirds of that is a difficulty additive rather than pool content.

### 5.4 The 6th spawn point is OPT-IN — the largest unmodelled term

**DB-CITED (Lua), `game/events/survivalevent.lua`.** Declaration at L375–377:

```lua
entity[5] = Entity.Get(survivalModeEventSpawnPoint05Id)
-- final spawn point is for bonus spawns, player chooses to enable this
entity[6] = Entity.Get(survivalModeEventSpawnPoint06Id)
```

and the gate in the spawn loop at L537–539:

```lua
-- Check if final bonus spawn should be used
local bonusSpawnStatus = gd.survival.rewards.checkBonusStatus()

for id = 1, waveEvent.numSpawns do
    if (waveEvent.waves[id][waveEvent.waveIndex] != nil && (id < waveEvent.numSpawns || bonusSpawnStatus == true)) then
```

Spawn point 6 (`id == numSpawns == 6`) fires **only** when `bonusSpawnStatus` is true. Corroborated by the achievement text in `mods/survivalmode/resources/Text_EN.arc :: tags_survivalui.txt`:

> `achS007Desc = Complete the Crucible through Wave 150 on Gladiator Difficulty with the 6th Spawn Point active.`

and by the token `SURVIVALMODE_GLADIATORBONUSSPAWNS` granted in `game/survival/rewards.lua`.

**Measured impact:** **13 of the 20** calibration waves declare a p06 proxy. Mid-range total across waves 151–170: **292.0 with p06 off → 316.5 with p06 on, +8.4 %.**

**This is 4.4× the entire operator-order + clamp uncertainty.** If the fixture's sitting did not have the 6th spawn point active and the sim assumes six points, the count model is wrong by four times more than the question this probe was commissioned to settle. **The fixture must record whether the 6th spawn point was active.** Flagged for the conductor as an input the sim needs and may not have.

### 5.5 The boss spawn limit is bypassed in the Crucible

Same file, L548, verbatim: `Proxy.Create(…, …, true) -- Proxy dbr, origin point, true for 'ignore boss spawn limit'`. An engine-side cap on concurrent bosses exists and the Crucible explicitly passes `true` to defeat it on **every** wave spawn. No count term for the sim, but it means campaign-derived boss-concurrency intuitions do not transfer to the Crucible.

---

## §6 — Recommended count model

Per spawn point, per wave, Gladiator, solo. `w` = global wave number; `pool` = the weighted-random pool the point resolved to.

```
if pool.ignoreGameBalance:                       # 74/632 Crucible pools, all boss pools
    n_min, n_max = pool.spawnMin, pool.spawnMax
    c_min, c_max = pool.championMin, pool.championMax
else:
    n_min = floor( (pool.spawnMin + 1 + adj03.spawnMinAdj[w]) * 120/100 )    # adj term == 0 for all w
    n_max =        pool.spawnMax + 1 + adj03.spawnMaxAdj[w]                  # adj term == 0 for all w
    if n_min > n_max: n_min = n_max                                          # clamp-min-down (DERIVED)
    c_min = pool.championMin + 1 + adj03.spawnChampionMinAdj[w]              # == +2 for w >= ~68
    c_max = pool.championMax + 1 + adj03.spawnChampionMaxAdj[w]              # == +2 for w >= ~52

regulars  = randint(n_min, n_max)                # deterministic for 93% of pools on Gladiator
champions = randint(c_min, c_max) if rand() < pool.championChance/100 else 0
```

Wave total = Σ over **active** spawn points. **Points 1–5 always; point 6 only if the player enabled bonus spawns.** No player-count term at any stage.

Per-wave envelopes for the calibration window (A / clamp-min-down, p06 OFF) are tabulated in full in `q7_clamp.py` output; the two extremes are wave 158 at 23–38 + 6 champions and wave 170 at 4–4 + 0.

---

## §7 — Residuals

| # | Item | Grade | Bound | What would close it |
|---|---|---|---|---|
| **U9-1** | Intra-order: `(base+add)×mod` vs `⌊base×mod⌋+add` | UNRESOLVED | 25/558 pools; **2.5 monsters over 20 waves (0.9 %)** | Observed in-game counts on a Gladiator pool with `base_min ≡ 4 (mod 5)`; or engine disassembly |
| **U9-2** | Clamp direction when `min' > max'` | UNRESOLVED (DERIVED toward min-down) | **3.0 monsters over 20 waves (1.0 %)** | Observed count on any width-0 pool, e.g. tier 17 wave 170 (4–4 base) |
| **U9-3** | Rounding mode (`floor` vs `round`) | UNRESOLVED | 67/558 pools, always ±1 | Same observation as U9-1 |
| **U9-4** | `adj[]` index is rank or rank−1 | UNRESOLVED | **Zero for this run** — waves 151–170 are past every knee | An observed champion-count change at wave 51 vs 52 |
| **U9-5** | Tiers 18–20 → waves 171–200 | DERIVED | Outside the calibration window | `survivalmode3/resources/Scripts.arc`; absent from the raw fetch |
| **U9-6** | Whether the fixture sitting had the **6th spawn point active** | **UNRESOLVED — conductor-side** | **+8.4 %, the largest single term** | Ask Matt; or read the `SURVIVALMODE_GLADIATORBONUSSPAWNS` token from the save |
| **U9-7** | Raw-fetch join-safety verified by **size**, not hash | DERIVED | — | `shasum` both trees; cheap, not run |
| **U9-8** | Whether hero pools' Gladiator `spawnMin +1` spawns a regular from an empty roster | UNRESOLVED | ≤1 monster per hero placement | Observation; hero pools have no `name1..N`, so 0 is the plausible engine behaviour and is what § 6 assumes |

**All three of U9-1/2/3 are the same class of question and would be closed by one observation:** a single screenshot-countable Gladiator wave containing a `base_min ≡ 4 (mod 5)` pool. If the conductor wants U-9 fully green rather than 98 % green, that is the cheapest possible experiment.

---

## §8 — Sources

**Primary — local corpus, read-only, no writes to any vendor tree**

| Source | Path |
|---|---|
| GD base database (1.3.0.0) | `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/database/database.arz` |
| Crucible base / AoM / FG / FoA overlays | `…/mods/survivalmode/database/SurvivalMode.arz`, `…/survivalmode{1,2,3}/database/SurvivalMode{1,2,3}.arz` |
| Expansion databases | `…/gdx{1,2,3}/database/GDX{1,2,3}.arz` |
| **Template archive (NEW LANE)** | `/Users/admin/Games/vendor/grim-dawn/database/templates.arc` — 819 `.tpl`, ARC v3 |
| **Crucible Lua (NEW LANE)** | `/Users/admin/Games/vendor/grim-dawn/mods/survivalmode/resources/Scripts.arc` — 24 files; `…/survivalmode1/resources/Scripts.arc` — 11 files |
| Crucible UI strings | `/Users/admin/Games/vendor/grim-dawn/mods/survivalmode/resources/Text_EN.arc :: tags_survivalui.txt` |
| `.arz` adapter | `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` |
| `.arc` reader | `agentic_orchestration/research/scripts/gd_arc_reader_2026_07_26.py` |

**Key records cited:** `records/game/gameproxies.dbr` (base + sm_mod) · `records/game/survivalinfo.dbr` · `records/game/balancingadjustment_survivalmode_enemies0{1,2,3}.dbr` · `records/game/balancingadjustment_mp+difficulty_{enemies,players}01.dbr` · `records/game/gameengine.dbr` · `records/proxies/proxypoolequation_01.dbr` · `records/proxies/tier{01..20}waves/proxy_w##_p##a.dbr` (925 records)
**Key templates cited:** `gameproxies.tpl` · `gameadjustment.tpl` · `proxypool.tpl` · `proxypoolequation.tpl` · `proxyambush.tpl`

**Primary — Crate Entertainment, published developer documentation**

| Source | URL | Retrieved |
|---|---|---|
| **Grim Dawn Modding Guide (PDF)** — Tutorial 05 "Spawning Monsters" / "Spawn Pool"; source of every DEV-DOC quote in § 3.3 and § 5 | https://www.grimdawn.com/downloads/Grim%20Dawn%20Modding%20Guide.pdf | 2026-08-07 |

**Secondary — community reference, used only for the tier-18–20 corroboration in § 2.4**

| Source | URL | Retrieved |
|---|---|---|
| Official Grim Dawn Wiki, *The Crucible* — 150 waves base, 170 with AoM; Aspirant/Challenger/Gladiator naming | https://grimdawn.fandom.com/wiki/The_Crucible | 2026-08-07 |

**Sought and did not yield** — Steam discussion 1768134097434867472 (spawn-rate modding; no mechanics stated) · Crate modding subforum threads 112181 / 112731 (multiplayer spawn scaling; no statement of operator order). **No external source states the intra-order or the clamp direction.** U9-1/2/3 are unresolved externally as well as internally, and are reported as such rather than filled with a plausible guess.

**Scripts, in execution order** — all under `agentic_orchestration/legolas/scratch/2026-08-07-u9-spawnmin/`:
`q1_findfields.py` (8-archive field sweep → `q1_hits.json`) · `q2_gameproxies.py` (verbatim record dumps) · `q3_templates.py` (**templates.arc crack** → `tpl/`) · `q4_tplsweep.py` (819-template description sweep) · `q5_discriminate.py` (**operator-order test** → `q5_violations.json`) · `q6_refine.py` (A-vs-B separation, IGB census, band-collapse) · `q7_clamp.py` (**four-branch residual bound + 6th-spawn-point term**)

---

## CLOSURE VERDICT

**CLOSED (operator order stated).**

`spawnMinModifier` is a **multiplicative percentage in which both 0 and 100 mean "no change"** — Gladiator's `120` is **×1.20** applied to the wave pool's base `spawnMin` together with the `Additive` `spawnMin` term of **+1**, with **no max-side percentage** (`spawnMaxModifier` is declared in the schema but left unset, so the ceiling moves by **+1 additive only**), and with **no player-count scaling anywhere in the chain** (the `proxyPoolEquation` hook is identity for 632/632 Crucible pools).

Residual: the *sequence* of the +1 against the ×1.20, the rounding mode, and the clamp direction remain undetermined by both the database and every external source consulted — but they are jointly bounded at **±1.9 % of total monster count across the entire waves-151–170 calibration window**, and are therefore not a basis for demoting monster-count-dependent calibration rows. The larger risk to the count model is not this question at all: it is the **opt-in 6th spawn point (+8.4 %)**, whose state in the fixture sitting is unrecorded (**U9-6**).

---

**Signed:** legolas, 2026-08-07. The commission asked whether the database could settle the semantics of `spawnMinModifier`. It could — but not from the `.arz`, which is where the question had been aimed. It settled from `templates.arc`, an archive sitting unopened in a fetch we already had, in which Crate annotates each field with what it means in plain English. The lesson worth carrying past this probe is that the corpus pin optimised for record *content* and dropped the two archives that carry record *semantics* and *sequencing* — the templates and the Lua. Opening them closed this question, closed the tier→wave schedule that a prior note had written off as script-resident and unrecoverable, and turned up a player-controlled spawn point worth four times the uncertainty I was sent to measure.
