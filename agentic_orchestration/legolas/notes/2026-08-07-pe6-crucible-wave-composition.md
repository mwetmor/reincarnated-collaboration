# PROBE P-E6 — Grim Dawn Crucible wave composition (Gladiator), datamined

**Date:** 2026-08-07
**Mode:** A (analytical / primary-source probe, READ-ONLY)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Conductor:** gandalf — KC2-SIM autonomous run, Phase A
**Purpose:** supply the opposition-composition substrate for the Crucible battle-sim's wave engine, calibrated against the EoR-Warlord fixture (sitting 1 = waves 1→93, death at 93; sitting 2 = checkpoint 150 → death at 160).
**Discipline:** R-BR-34 — every count below cites a record path; every name below resolves through a localization tag.
**Commit status:** UNCOMMITTED by instruction (conductor centralizes commits at gate closes).

---

> **CORRIGENDUM — § 2.8 `characterLifeModifier` indexing (conductor-landed at KC2 ledger L-58, 2026-08-08; source: legolas's own w152/w157 generator-join finding, join note § 3.1/R-2 — a self-correction, honored corrigenda-forward; the body below is left as written).** The Gladiator life array is **WAVE-indexed** — `balancingadjustment_survivalmode_enemies03`, 200 entries, read `arr[wave − 1]`, reproduced under u8 read 200/200 — not a flat difficulty constant. The `+168 %` quoted at four sites below is the array read at the wrong index. At the fixture band (waves 151–158) the array reads **≈ +308 % … +318 %**; at wave 160 it reads **+324 %** ⇒ ≈ **1.3 M effective HP per nemesis**, 1.58 × the 827 K derived below. The four superseded sites (pre-banner line refs): **:167** difficulty-table row `+168 %` · **:187** burst-and-bulk designer-intent paragraph · **:377** "roughly 827,000 effective HP per nemesis" · **:621** wave-160 death narrative (its eHP figure scales × 1.58; its composition reading and the don't-over-fit-to-Zantarin conclusion are unaffected). Downstream surfaces were ALREADY corrected at ledger L-17 and are CURRENT — sim spec :1243/:2876 (wave-indexed row `…304·306·314·324·326·344…`), ledger L-17 strike, engine `opposition.py:281` wave-indexed read + `:301` regression guard. No consumer carried the stale value forward; this note was the last stale surface, closed here.

---

## §0 — Headline

**The whole Crucible is database-resident and it fully decodes.** 925 spawn-point proxy records across 20 tiers × 10 waves × up to 6 spawn points, resolving through 632 distinct pools to 1,617 distinct monster records, with **zero unresolved pool references and zero non-conforming records**. Global waves 1–200 are covered end to end.

Four findings are load-bearing and none of them was in the prior substrate:

1. **The tier↔wave binding is proved, not assumed.** Global wave = `(tier − 1) × 10 + wave`. Proof is the checkpoint tag ladder — tier05→50, tier10→100, tier15→150, tier18→180 — not inference. The Crucible runs to **wave 200**, not 150 or 170.
2. **Crucible difficulty is a DB-resident pool axis nobody had read.** 29 of 925 spawn points carry `poolEpic*` / `poolLegendary*` overrides. `poolLegendary` = **Gladiator**. The 2026-08-01 density note read only `pool1..pool6` and therefore measured the **Aspirant** composition. The correction is bounded and I state its size below (24 waves of 200 differ; only wave 150 differs inside the two priority bands).
3. **Spawn point 05 is not a spawn point — it is a sustained-population ambush.** All 107 `ProxyAmbush` records in the Crucible are p05, and every p05 is a `ProxyAmbush`, with byte-identical parameters at all 107 sites. 107/107, no exceptions.
4. **Wave 160 is an all-champion nemesis wave with no trash at all** — three nemesis slots + one superboss + one hero, **5 bodies raw and at most 7 under full Gladiator modifier application** (§4.6). Zantarin, the Immortal sits in the p01 pool at exactly **1-in-10**, which independently corroborates the fixture save's `tagNemesis_OrderDeathsVigil01`.

**Werewolf flag count: 0 active, 1 latent, 49 adjacency.** No werewolf-family monster record appears anywhere in the Crucible composition. Details in §5.

**§2.10 reconciles this note against sibling Phase-A probes U-8 and U-9**, which opened the Crucible's Lua and Crate's template files. They close one of my gaps outright and correct one framing I would otherwise have shipped wrong — the fixture fought waves **151→160**, not 150→160.

---

## §1 — Substrate, method, provenance

### 1.1 Corpus (and a corrected path)

The commission named `~/Games/vendor/grim-dawn/`. **That tree cannot answer this commission** — it has no `survivalmode3/`, and `SurvivalMode3.arz` is the effective owner of every wave record in tiers 16–20, i.e. waves 151–200, i.e. wave 160. I used the Edition-II pinned tree instead, which is the corpus of record for every prior GD probe:

```
/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/
```

| Archive | sha256 (first 24) | records |
|---|---|---:|
| `database/database.arz` | `8cdeff128422c765278087b7` | 34,114 |
| `gdx1/database/GDX1.arz` | (per 2026-07-24 pin) | 18,447 |
| `gdx2/database/GDX2.arz` | — | 16,451 |
| `gdx3/database/GDX3.arz` | — | 24,178 |
| `mods/survivalmode/database/SurvivalMode.arz` | `e55b760f36ab80a6ad16fd34` | 3,147 |
| `survivalmode1/database/SurvivalMode1.arz` | `6df94d3be33e600c737634bc` | 1,004 |
| `survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6` | 811 |
| `survivalmode3/database/SurvivalMode3.arz` | `b4aa2d78675c4f05f92988e5` | 1,431 |

84,663 distinct record paths after overlay. Overlay order (later wins): `base → gdx1 → gdx2 → gdx3 → sm_mod → sm1 → sm2 → sm3`. Display names via `Text_EN.arc` ×4 → 20,394 localization tags.

**Version pin: 1.3.0.0.** The client is 1.3.0.5. See §5 for the confound status of that gap on this surface.

### 1.2 Instruments

- `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` — `ArzArchive` (TQIT/LZ4-block reader)
- `agentic_orchestration/research/scripts/gd_arc_reader_2026_07_26.py` — `ArcArchive` + `parse_tag_file` (ARC v3 localization)
- Probe scripts, reproducible: `agentic_orchestration/legolas/scratch/2026-08-07-pe6-crucible/s1_orient.py … s8_emit.py`

### 1.3 Emitted artifacts (uncommitted, scratch)

| File | Rows | Grain |
|---|---:|---|
| `pe6_crucible_waves.csv` | 200 | one row per global wave — counts, kind census, nemesis flag, all three difficulty views |
| `pe6_crucible_wave_pools.csv` | 1,998 | one row per (wave, spawn point, pool) — full roster names + record paths |
| `s4_waves_full.json` | 200 | the complete nested extraction (12.7 MB) |

---

## §2 — Q1: the wave-record structure

### 2.1 Naming and coverage

```
records/proxies/tier<NN>waves/proxy_w<WW>_p<PP>a.dbr
```

925 records. **100 % conformance — 0 non-conforming files under any `tier*waves/` folder.** `NN` = 01–20, `WW` = 01–10, `PP` = 01–06, suffix always `a`. Every tier has exactly 10 waves; per-wave spawn-point count ranges 2–6.

### 2.2 The tier → global-wave binding — MEASURED, not inferred

The 2026-08-01 note recorded the schedule as "not in the database — sequencing is game script." That is true of the *timing*, but the *numbering* is recoverable from the localization tags:

| Tag (archive) | Verbatim | Binds |
|---|---|---|
| `tagNotification_Checkpoint05` (`sm_mod`) | *"You can now resume the Crucible on Wave 50."* | tier 05 → wave 50 |
| `tagNotification_Checkpoint10` (`sm_mod`) | *"…on Wave 100."* | tier 10 → wave 100 |
| `tagNotification_Checkpoint15` (`sm2`) | *"…on Wave 150."* | tier 15 → wave 150 |
| `tagNotification_Checkpoint18` (`sm3`) | *"…on Wave 180."* | tier 18 → wave 180 |

Four independent anchors, all consistent with **global wave = (tier − 1)·10 + wave**. Corroborated a fifth time by `tagHUDWaveTier01 = "Current Wave"` — the UI field the game internally calls *WaveTier* displays the *wave*, which is why the fixture save's `survivalWaveTier` holds 170 rather than 17.

**Consequence: the Crucible is 200 waves.** 20 tiers × 10. Independently corroborated by archive lineage:

| Wave band | Tiers | Effective owner | Reading |
|---|---|---|---|
| 1–150 | 1–15 | `sm_mod` founded; `sm1`/`sm2`/`sm3` overlay | base Crucible DLC ("Complete the Crucible through Wave 150" — `achS001Desc`) |
| 151–170 | 16–17 | records created by `sm1`, **100 % overridden by `sm3`** | AoM-era extension, wholly rewritten in FoA |
| 171–200 | 18–20 | `sm3` only | FoA-new |

The fixture's 2022 baseline `survival-greatest-wave = 170` is exactly the pre-FoA ceiling. That is a clean external check on the whole binding.

### 2.3 Record classes and the three-hop resolution

```
proxy_wWW_pPPa.dbr   [Class: Proxy (818) | ProxyAmbush (107)]
   └─ pool{i} / poolEpic{i} / poolLegendary{i}     weighted ALTERNATIVES — engine picks ONE
        └─ proxypool record  [Class: "" , template proxypool.tpl]
             spawnMin, spawnMax, championChance, championMin, championMax
             name{j} / weight{j} / limit{j} / minPlayerLevel{j} / levelVarianceEquation{j}
             nameChampion{j} / weightChampion{j} / limitChampion{j}
             └─ records/creatures/enemies/**.dbr  [Class: Monster]
                  description → tag → Text_EN.arc → display name
```

632 distinct pools referenced; **0 unresolved**.

`Class: Proxy` field union (n=818): `pool1..pool6` + `weight1..6` (`pool1`/`weight1` on all 818; `pool6` on 34), `placementExtents` (8.0 on all 925), `scale` (2.0 on all 925), `mesh` (`proxybounty01.msh` on all 925), plus the difficulty-scoped families below.

`Class: ProxyAmbush` field union (n=107): the above minus `poolEpic*`/`poolLegendary*`, plus `minGroupSize`, `maxGroupSize`, `spawnThreshold`, `minSpawnTime`, `maxSpawnTime`, `minDelayTime`, `maxDelayTime`, `alertArea`.

### 2.4 FIRST-OF-KIND — the difficulty axis lives on the wave record

29 of 925 spawn-point proxies carry `poolEpic{i}` / `poolLegendary{i}` with matching `weightEpic{i}` / `weightLegendary{i}`.

**Binding: base pools = Aspirant (Normal) · `poolEpic` = Challenger (Elite) · `poolLegendary` = Gladiator (Ultimate).** Evidence for the binding, in descending strength:

1. `records/game/survivalinfo.dbr` names its three balance records `survivalAdjustmentNormal / …Elite / …Ultimate`, and the fixture save carries `SURVIVALMODE_NORMAL` / `SURVIVALMODE_CHALLENGER` / `SURVIVALMODE_GLADIATOR` — a three-rung ladder with GD's standard Normal/Elite/Ultimate internals.
2. Every override is a monotonic escalation. Tier02 w05 p01 (wave 15): base = `poolsbasic/aetherialreanimator_t1` (trash, 2–4); Epic and Legendary = `poolsboss/aetherial_reanimator_zanbrandt` (boss, 7–7). Tier01 w05 p01 (wave 5): base = two trash pools; Epic/Legendary = three `poolshero` pools at `championChance 100 %`.
3. GD's `Epic`/`Legendary` tokens are its standing internal names for Elite/Ultimate.

**Measured sub-finding: Challenger and Gladiator are identical.** Of the 29 override sites, 28 carry both `poolEpic` and `poolLegendary`, and in **28/28 the pool sets are identical**; one site carries `poolEpic` only. Only Aspirant differs. So the sim needs exactly two composition views, not three.

**Size of the correction to the 2026-08-01 density note.** Gladiator differs from Aspirant on **24 of 200 waves**: 4, 5, 7, 9, 10, 12, 15, 18, 25, 29, 30, 33, 35, 39, 40, 42, 45, 48, 50, 51, 55, 65, **120, 150**. Twenty-two of the twenty-four are at wave ≤ 65. Σ E[monsters] over all 200 waves is 3,266.3 Aspirant vs 3,207.4 Gladiator — near-identical totals; the override trades *count* for *quality* (wave 51: Aspirant 6–8 trash → Gladiator 0–3, all heroes). **Tier 13/14 density claims in the prior note are difficulty-invariant and stand unamended.**

### 2.5 FIRST-OF-KIND — spawn point 05 is the ambush point

| Claim | Measurement |
|---|---|
| Every `ProxyAmbush` in the Crucible is at spawn point 05 | 107/107 |
| Every spawn point 05 in the Crucible is a `ProxyAmbush` | 107/107 |
| Parameters vary across the 107 sites | **no** — identical at every site |

```
minGroupSize = maxGroupSize = 30      spawnThreshold  = 15
minSpawnTime = maxSpawnTime  = 3.0 s  minDelayTime = maxDelayTime = 4.0 s
alertArea    = 100.0
```

Reading, with its uncertainty stated: p05 monsters arrive **on a 3-second drip after a 4-second delay**, not instantaneously with the other points. The `maxGroupSize = 30` concurrency cap never binds in the Crucible, because p05 pool budgets run 3–11 (well under 30) — cf. the Bastion-of-Chaos gauntlet, where `spawnMin = spawnMax = 100` against `maxGroupSize = 14` makes the cap the operative term. **Whether `maxGroupSize` caps concurrency independently of the pool budget is not determinable from the database alone** — flagged, not resolved. The safe sim model is: p05 emits its pool count, staggered on a 3 s cadence beginning at t+4 s.

### 2.6 Spawn point 06 is optional

`achS007Desc` verbatim: *"Complete the Crucible through Wave 150 on Gladiator Difficulty **with the 6th Spawn Point active**."* Corroborated by `records/scriptentities/spawnpoint06_fx.dbr → gd.survival.rewards.spawnPoint06FXOnAddToWorld` — spawn point 06 hangs off the *rewards* script namespace, not the wave namespace. **p06 is a player-elected difficulty toggle.** It is defined on 4–7 waves per decade throughout. A sim wanting the default run should be able to switch p06 off; wave 160's hero slot is p06, so this is not cosmetic.

### 2.7 Level model (inherited, re-verified)

All roster entries resolve `levelVarianceEquation` against `averagePlayerLevel`; nemesis and boss entries use `lv8_boss+` (`apl+3+apl/50 … apl+4+apl/50`), hero entries `lv6_hero`, trash `lv2_normal`/`lv3_strong`. **The Crucible carries no player-level gate on tier access.** `minPlayerLevel{j}` gates individual roster entries only; at L100 every gate is open.

### 2.8 Gladiator monster scalars — `balancingadjustment_survivalmode_enemies03.dbr`

This is the survival-specific layer applied on top of ordinary Ultimate scaling. 35 non-zero fields; values at array index 99 (level 100):

| Field | Aspirant | Challenger | **Gladiator** |
|---|---:|---:|---:|
| `characterLifeModifier` | +53 % | +120 % | **+168 %** |
| `characterOffensiveAbility` (flat) | +26 | +21 | **+26** |
| `characterOffensiveAbilityModifier` | +2.1 % | +2.1 % | +2.1 % |
| `characterDefensiveAbility` (flat) | +20 | +26 | **+33** |
| `characterDefensiveAbilityModifier` | +3 % | +3 % | +3 % |
| `offensiveTotalDamageModifier` | +20 % | +20 % | +20 % |
| `characterAttackSpeedModifier` / `…SpellCastSpeedModifier` | +5 % | +5 % | **+8 %** |
| `offensiveCritDamageModifier` | 0 | 0 | **+6 %** |
| `offensivePhysicalModifier` | 0 | 0 | **−15 %** |
| `offensiveSlow*Modifier` (bleed/cold/fire/life/lightning/phys/poison) | −30 % | −36 % | **−40 %** |
| `offensiveSlowDamageMultModifier` | −15 % | −30 % | **−40 %** |
| `characterPercentHealIncreaseModifier` | −43 % | −43 % | −43 % |
| `defensiveReflectModifier` | −70 % | −70 % | −70 % |
| `offensive{Freeze,Petrify,Sleep,Stun,Trap}Modifier` | −40 % | −40 % | −40 % |
| `characterLifeRegenModifier` / `…ManaRegenModifier` | +20 % | +20 % | +20 % |
| `retaliationTotalDamageModifier` | +24 % | +16 % | +22 % |
| `spawnChampionMinAdj` / `MaxAdj` | +1 | +1 | +1 |
| `defensivePercentCurrentLife` | 5 | 5 | 5 |
| `defensiveConvert` | 50 | 50 | 50 |

Two designer-intent readings worth carrying to the sim: Gladiator monsters take a **−15 % physical-damage cut and a −40 % DoT cut** while gaining +168 % life and +20 % total damage. The Crucible's Gladiator tuning is a **burst-and-bulk** regime, not a DoT-and-attrition regime.

### 2.9 Count scalars — `records/game/gameproxies.dbr` (survival override, `sm_mod`)

```
spawnMin  = [0, 0, 1]      spawnMax   = [0, 1, 1]
championMin = [0, 0, 1]    championMax = [0, 1, 1]
spawnMinModifier = [0, 112, 120]        # index Normal / Elite / Ultimate
```

I report raw pool counts as **MEASURED** and the adjusted counts as **INFERRED-GUARDED**, with the guard declared: the deltas are applied only to pools with `spawnMax ≥ 2`. Applying them to a 1-of-1 nemesis pool would put **two** nemeses on every nemesis spawn point at wave 160 (eight to ten nemeses in the wave), which the database cannot corroborate and play experience contradicts. The `spawnMinModifier` percentage semantics are inherited from the 2026-08-01 note and are themselves an inference. Both columns ship in `pe6_crucible_waves.csv` (`raw_*` and `glad_adj_*`); the sim should treat `raw_*` as ground and `glad_adj_*` as a modelled upper band.


### 2.10 CROSS-PROBE RECONCILIATION — U-8 and U-9 supersede two things above

My sibling Phase-A probes landed in parallel and both opened a substrate lane this probe did not (the Crucible's **Lua source** in `Scripts.arc`, and Crate's **template files** in `database/templates/`). Where they conflict with me, they win — they read declarations, I read data.

| This probe said | U-8 / U-9 measured | Status here |
|---|---|---|
| §2.4/2.9 — `spawnMinModifier` percentage semantics **inherited as inference** (G-3) | **U-9, DB-CITED:** `gameproxies.tpl` annotates `spawnMin/Max`, `championMin/Max` as `"Additive"` and `*Modifier` as `"Percent (0 or 100) no change"`. Gladiator `120` → **×1.20 multiplicative** | **G-3 CLOSED by U-9.** My `glad_adj_*` CSV columns use exactly this reading and are therefore correct on that axis |
| §2.9 — the `spawnMax ≥ 2` guard on 1-of-1 boss pools, declared as **my inference** | **U-9, DB-CITED:** the real mechanism is the pool field **`ignoreGameBalance`** — Crate: *"whether to use the difficulty modifiers that increase spawn count."* **74 of 635** Crucible pools set it, and they are almost exclusively boss pools (`poolsbossgdx3` 36, `poolsboss` 18, `poolsbossgdx1` 13, `poolsbossgdx2` 6, `poolsbasicgdx3` 1) | **My guard was the right instinct with the wrong operator.** See §4.6 — measured per-pool, not inferred |
| §2.6 — p06 is optional, argued from an achievement string + the `rewards` script namespace | **U-9, from the Crucible's own Lua, verbatim:** `-- final spawn point is for bonus spawns, player chooses to enable this`. Worth **+8.4 %** monsters across waves 151–170 | **Independently confirmed, and upgraded from inference to source** |
| §2.2 — the checkpoint tags bind tier 15 → wave 150 | **U-8, from the Lua sequencer:** the label names the checkpoint you are *credited* with; the counter is set to 151 and the increment skipped, so **"Start on Wave 150" spawns `tier16waves/proxy_w01_*` = wave 151**. Also `rewardTier ≠ tier` (at wave 151, content tier 16 / rewardTier 15) | **Tier↔wave arithmetic unchanged; the *entry point* is amended.** See §3.2 |
| §2.2 — the Crucible is 200 waves | **U-8, independently, by three-cut corpus differential:** 200, and `170` is the stale pre-FoA ceiling | **Agrees** |

Two of U-9's findings have no counterpart above and belong in the sim's count model: **player-count scaling does not exist** (632 of 632 Crucible pools reference the identity `proxypoolequation_01.dbr`), and **champions ADD rather than convert** (Crate: *"Spawn Min/Max: the number of monsters to spawn from the Regular Pool. Champion Min/Max: the number… from the Champion Pool."*). The second one validates the `smax + cmax` ceiling arithmetic used throughout §3.

---

## §3 — Q2: PRIORITY BANDS, full extraction

Notation: `p<N>` = spawn point; `t / H / B / D / Y` = trash / hero / boss / devotion-hero / bounty-hero pool; `/` separates **weighted alternatives at one spawn point** (the engine picks exactly one); `\*` marks the p05 ProxyAmbush; `(n)` or `(n-m)` = `spawnMin`–`spawnMax`; `1×h` = `championChance 100 %` with `spawnMin/Max = 0`, i.e. exactly one champion. `min–max` sums the per-point floor and ceiling across active points; the realized count lies between. Both tables below are machine-generated from `s4_waves_full.json`; full per-pool rosters with record paths are in `pe6_crucible_wave_pools.csv`.

### 3.1 Band A — waves 1–93 (sitting 1)

Σ raw E = **1,600.4 monsters** over 93 waves. Nemesis waves in band: **{90}** only.

| wave | t/w | class | min–max | E | Gladiator composition |
|---:|:---|:---|:---|---:|:---|
| 1 | 1/1 | trash | 15–15 | 15.0 | **p1** t:zombies_t1(5) / t:bonerat_t1(5) · **p2** t:zombies_t1(5) / t:bonerat_t1(5) · **p6** t:zombies_t1(5) / t:bonerat_t1(5) |
| 2 | 1/2 | trash | 8–10 | 9.0 | **p2** t:groble_a_t1(4) / t:prawn_t1(5) · **p3** t:groble_a_t1(4) / t:prawn_t1(5) |
| 3 | 1/3 | trash | 16–20 | 18.0 | **p1** t:gazer_t1(4-5) · **p3** t:gazer_t1(4-5) · **p4** t:cultistmelee_t1(4-5) · **p6** t:gazer_t1(4-5) |
| 4 | 1/4 | trash | 13–18 | 14.7 | **p3** t:aetherialhorror_t1(4) / t:aetherialwisps_t1(6) / t:thornedhorror_t1(4) · **p4** t:aetherialhorror_t1(4) / t:aetherialwisps_t1(6) / t:thornedhorror_t1(4) · **p5**\* t:prawn_t1(5) / t:spiderambush_t1(5) / t:zombiespoison_t1(6) |
| 5 | 1/5 | hero+trash | 9–10 | 10.0 | **p1** H:boar_hero(1×h) / H:raptor_hero(1×h) / H:rifthound_hero(1×h) · **p2** t:zombiesmutants_t1(3) · **p3** t:zombiesfire_t1(6) |
| 6 | 1/6 | trash | 19–20 | 19.8 | **p3** t:zombiesice_t2(7) · **p4** t:zombiesfire_t2(7) · **p5**\* t:ghost_t1(5-6) / t:skeletonranged_t1(6) |
| 7 | 1/7 | hero+trash | 11–15 | 13.5 | **p1** H:bonerat_hero(1×h) / H:dranghoul_hero(1×h) / H:harvestman_hero(1×h) · **p2** t:dermapteran_t1(5-6) / t:harpy_t1(3-4) · **p3** t:skeletonwarlocks_t2(5) · **p6** t:skeletonwarlocks_t1(3) |
| 8 | 1/8 | trash | 8–14 | 9.6 | **p1** t:chthoniandevourer_t1(5-6) · **p4** t:chthoniandreadguard_t1(3) / t:chthonianfiend_t2(7-8) / t:chthonianleech_t1(3) |
| 9 | 1/9 | trash | 10–17 | 13.8 | **p1** t:golem_t1(2-3) / t:troll_t1(2) · **p3** t:waspgiant_t1(6-7) / t:rifthound_t1(4-6) · **p4** t:waspgiant_t1(6-7) / t:rifthound_t1(4-6) |
| 10 | 1/10 | boss+trash | 14–16 | 15.5 | **p1** B:chthonian_trappedandalone(1) / B:golem_floodedpassage(1) · **p2** H:aetherialreanimator_hero(1×h) / H:chthoniandevourer_hero(1×h) / H:groble_hero(1×h) · **p4** t:skeletonranged_t2(7-8) · **p6** t:skeletonranged_t1(6) |
| 11 | 2/1 | trash | 22–27 | 25.0 | **p1** t:raptor_t2(6) · **p2** t:spiderdeeps_t1(4-5) · **p3** t:trollhalf_t1(5-6) / t:outlawmelee_t1(4-6) · **p4** t:trollhalf_t1(5-6) / t:outlawmelee_t1(4-6) · **p6** t:raptor_t1(4) |
| 12 | 2/2 | hero+trash | 9–13 | 11.5 | **p1** H:necro_hero(1×h) / H:zealot_hero(1×h) · **p2** t:blacklegion_t2(6-7) · **p3** t:outlawaether_t1(3-5) |
| 13 | 2/3 | hero+trash | 14–15 | 15.0 | **p1** H:zombies_hero(1×h) · **p5**\* t:spiderambush_t3(9) · **p6** t:spider_t1(5) |
| 14 | 2/4 | trash | 19–19 | 19.0 | **p3** t:cultistvitality_t2(6) · **p4** t:trollhalf_cave_t2(6) · **p5**\* t:zombiesaether_t2(7) |
| 15 | 2/5 | boss+trash | 17–18 | 18.0 | **p1** B:aetherial_reanimator_zanbrandt(7) · **p2** H:chthoniandreadguard_hero(1×h) / H:chthonianminion_hero(1×h) · **p3** B:aetherial_reanimator_gethrand(7) · **p6** t:chthoniandreadguard_t1(3) |
| 16 | 2/6 | trash | 16–22 | 18.5 | **p1** t:humanpossessed_t2(6) · **p2** t:groble_e_t1(4-6) / t:groble_d_t1(4-6) · **p3** t:groble_a_t1(4) / t:groble_b_t1(4-6) · **p4** t:aetherialreanimator_t1(2-4) |
| 17 | 2/7 | trash | 19–21 | 20.5 | **p1** t:ghost_t1(5-6) / t:skeleton_t1(6) · **p2** t:yeti_t1(3) · **p3** t:ghost_t1(5-6) / t:skeleton_t1(6) · **p4** t:yeti_t1(3) · **p5**\* t:skeletonrevenant_t1(3) |
| 18 | 2/8 | boss+trash | 17–21 | 19.3 | **p1** B:aetherial_mutant_devilscrossing(1) / B:aetherial_mutant_burrwitch01(2) / B:ghost_oligarch01(1) · **p2** H:vulture_hero(1×h) / H:prawn_hero(1×h) / H:outlawhero_hero(1×h) · **p3** t:chthoniandevourer_t2(8-9) · **p6** t:chthoniandevourer_t2(8-9) |
| 19 | 2/9 | hero+trash | 15–16 | 16.0 | **p1** H:trollhalf_hero(1×h) / H:mosquito_hero(1×h) · **p2** t:cultistfire_t2(6) · **p3** t:skeletonwarlocks_t1(3) · **p4** t:gazer_t2(6) |
| 20 | 2/10 | boss+trash | 11–14 | 12.2 | **p1** B:outlaw_balthazar(4-5) · **p3** B:outlaw_moneybags(4-5) · **p6** t:chthonianminion_t1(3-4) / t:chthoniandreadguard_t1(3) |
| 21 | 3/1 | hero+trash | 15–20 | 16.8 | **p1** t:ghoul_t2(6) / t:skeleton_t2(7-8) · **p2** H:ghoul_hero(1×h) / H:zombies_hero(1×h) / H:slith_hero(1×h) · **p4** t:ghoul_t2(6) / t:skeleton_t2(7-8) · **p5**\* t:prawndeeps_t1(3) |
| 22 | 3/2 | trash | 21–23 | 22.0 | **p3** t:outlawaether_t2(6) · **p4** t:outlawaether_t2(6) · **p5**\* t:harpyambush_t3(6-7) · **p6** t:harpy_t1(3-4) |
| 23 | 3/3 | boss+trash | 16–19 | 17.5 | **p1** B:dermapteran_vizier01(1) / B:dermapteran_vizier02(1) / B:dermapteran_vizier03(1) · **p2** t:chthonianleech_t1(3) / t:chthonianfiend_t1(6) · **p3** t:cultistfire_t2(6) / t:cultistpoison_t2(6) · **p4** t:cultistfire_t2(6) / t:cultistpoison_t2(6) |
| 24 | 3/4 | hero+trash | 30–33 | 32.0 | **p1** t:waspgiant_t2(7) · **p2** t:spider_t1(5) · **p3** t:prawn_t2(7) · **p4** t:groble_a_t2(6-7) / t:groble_b_t2(6-7) / t:groble_c_t2(6-7) · **p5**\* t:chthoniandevourer_t1(5-6) · **p6** H:groble_hero(1×h) |
| 25 | 3/5 | boss+trash | 13–22 | 18.0 | **p1** B:rifthound_bonehunter(1) · **p2** D:devotion_heroes×6 · **p3** t:rifthound_t2(6) / t:dermapteran_t2(10) · **p4** t:rifthound_t2(6) / t:dermapteran_t2(10) |
| 26 | 3/6 | trash | 28–30 | 29.0 | **p1** t:skeleton_t1(6) · **p2** t:harpy_t2(5-6) · **p3** t:zombies_t1(5) · **p4** t:ghoul_t2(6) · **p5**\* t:ghost_t2(6-7) |
| 27 | 3/7 | hero+trash | 12–19 | 14.5 | **p1** t:skeletonrevenant_t1(3) / t:outlawaether_t1(3-5) · **p2** H:harpy_hero(1×h) / H:yeti_hero(1×h) · **p3** t:golem_t2(3-5) / t:fleshhulk_t2(3) · **p4** t:skeletonrevenant_t1(3) / t:outlawaether_t1(3-5) · **p6** t:skeletonrevenant_t1(3) |
| 28 | 3/8 | trash | 20–27 | 23.2 | **p1** t:slith_a_t2(6) · **p2** t:spider_t1(5) / t:waspgiant_t1(6-7) · **p3** t:boar_t2(6-7) / t:boarfrost_t2(4-6) · **p4** t:spider_t1(5) / t:waspgiant_t1(6-7) |
| 29 | 3/9 | hero+trash | 8–13 | 11.0 | **p1** H:necro_hero(1×h) / H:zealot_hero(1×h) · **p2** H:outlawhero_hero(1×h) · **p5**\* t:skeleton_t3(8) / t:chthoniandevourer_t3(9-11) |
| 30 | 3/10 | boss+trash | 20–23 | 21.5 | **p1** B:chthonian_bolvar(5) · **p2** B:chthonian_zaria(1) · **p5**\* t:chthoniandevourer_t3(9-11) · **p6** t:chthoniandevourer_t1(5-6) |
| 31 | 4/1 | hero+trash | 15–18 | 17.2 | **p2** Y:bounty_heroes01(1×h) / Y:bounty_heroes02(1×h) / Y:bounty_heroes03(1×h) · **p3** t:dranghoul_t2(4) · **p4** t:aetherialhorror_t2(5-6) / t:zombiessoldiers_t2(6) · **p6** t:groble_b_t2(6-7) |
| 32 | 4/2 | trash | 21–27 | 23.8 | **p1** t:aetherialabomination_t1(2-3) · **p2** t:aetherialhorror_t2(5-6) / t:zombiesmutants_t2(6) · **p3** t:aetherialhorror_t2(5-6) / t:zombiesmutants_t2(6) · **p4** t:blacklegion_t1(4-6) / t:necro_t1(4) / t:zealot_t1(4) · **p5**\* t:zombiespoison_t1(6) / t:prawn_t1(5) |
| 33 | 4/3 | hero+trash | 7–10 | 10.0 | **p1** H:chthonianleech_hero(1×h) / H:chthoniandefiler_hero(1×h) · **p3** Y:bounty_heroes01(1×h) / Y:bounty_heroes02(1×h) / Y:bounty_heroes03(1×h) · **p4** H:humanpossessed_hero(1×h) / H:outlawhero_hero(1×h) · **p6** t:zombies_t2(7) |
| 34 | 4/4 | hero+trash | 21–25 | 23.5 | **p3** t:boarfrost_t3(5-6) · **p4** t:bonerat_t3(8-9) · **p5**\* t:chthoniandevourer_t2(8-9) · **p6** H:zombies_hero(1×h) |
| 35 | 4/5 | boss+trash | 15–17 | 17.0 | **p1** B:aetherial_warden(1) · **p2** D:devotion_heroes×6 · **p3** t:vulture_t2(6) · **p4** t:mosquito_t2(8) · **p5**\* H:prawn_hero(1×h) / H:chthoniandevourer_hero(1×h) |
| 36 | 4/6 | trash | 23–25 | 24.5 | **p1** t:manticore_t2(6) / t:manticoreaether_t2(5-6) · **p2** t:yeti_t1(3) / t:zombiesmutants_t1(3) · **p3** t:manticore_t2(6) / t:manticoreaether_t2(5-6) · **p4** t:yeti_t1(3) / t:zombiesmutants_t1(3) · **p5**\* t:spiderdeepsambush_t2(7) |
| 37 | 4/7 | boss+trash | 16–17 | 16.5 | **p1** B:chthonian_leech_necropolis(1) · **p2** B:chthonian_leech_void(1) · **p3** t:aetherialreanimator_t2(4-5) · **p4** t:ghoul_t2(6) · **p6** t:ghoul_t1(4) |
| 38 | 4/8 | trash | 8–9 | 8.5 | **p1** t:trollswamp_t1(2) · **p2** t:fleshhulk_t1(2) · **p3** t:golem_t1(2-3) · **p4** t:skeletalgolem_t1(2) |
| 39 | 4/9 | hero+trash | 7–10 | 10.0 | **p1** D:devotion_heroes×6 · **p2** H:cultist_hero(1×h) · **p3** H:humanpossessed_hero(1×h) · **p5**\* t:prawn_t2(7) |
| 40 | 4/10 | boss+trash | 12–13 | 13.0 | **p1** B:slith_elena(1) / B:dranghoul_bloodfeast(1) · **p2** D:devotion_heroes×6 · **p3** B:aetherial_harrath_nozombies(5) · **p6** t:slith_a_t2(6) |
| 41 | 5/1 | trash | 11–15 | 12.5 | **p3** t:aetherialabomination_t2(3-4) · **p4** t:chthoniandevourer_t3(9-11) / t:waspgiant_t3(8) |
| 42 | 5/2 | boss+trash | 7–13 | 11.0 | **p1** Y:bounty_heroes01(1×h) / Y:bounty_heroes02(1×h) / Y:bounty_heroes03(1×h) · **p2** t:yeti_t2(6) / t:golem_t2(3-5) · **p3** B:skeletalgolem_ilgorr(1) / B:swampgolem_bargoll(1) · **p6** t:trollswamp_t2(4) / t:swampgolem_t2(3-5) |
| 43 | 5/3 | hero+trash | 26–28 | 27.5 | **p1** t:blacklegion_t2(6-7) · **p2** t:outlawrange_t2(6) · **p3** t:troll_t1(2) · **p4** t:outlawrange_t2(6) · **p5**\* t:zombiessoldiers_t2(6) · **p6** H:humanpossessed_hero(1×h) |
| 44 | 5/4 | trash | 18–20 | 18.7 | **p1** t:zombiesice_t2(7) · **p2** t:skeletonwarlocks_t2(5) · **p3** t:boar_t1(3-4) / t:manticore_t1(3) / t:wendigo_t1(3-4) · **p4** t:boar_t1(3-4) / t:manticore_t1(3) / t:wendigo_t1(3-4) |
| 45 | 5/5 | boss+trash | 10–15 | 13.0 | **p1** B:chthonian_karroz(1) · **p2** t:trollhalf_t2(6) / t:trollswamp_t2(4) · **p3** B:dranghoul_gutworm(1) · **p4** t:trollhalf_t2(6) / t:trollswamp_t2(4) · **p6** H:trollhalf_hero(1×h) |
| 46 | 5/6 | hero+trash | 6–8 | 8.0 | **p1** H:aetherialreanimator_hero(1×h) · **p4** H:aetherialreanimator_hero(1×h) · **p5**\* t:chthonianvoid_ambush_t2(6) |
| 47 | 5/7 | trash | 16–18 | 17.0 | **p1** t:prawndeeps_t2(5) / t:raptor_t2(6) · **p2** t:prawndeeps_t2(5) / t:raptor_t2(6) · **p4** t:skeletalgolem_t1(2) · **p6** t:raptor_t1(4) |
| 48 | 5/8 | boss+trash | 6–8 | 8.0 | **p1** B:necro_captain(1) / B:zealot_captain(1) / B:manticore_matriarch(1) · **p2** H:dranghoul_hero(1×h) / H:dermapteran_hero(1×h) / H:golem_hero(1×h) · **p3** H:harpy_hero(1×h) / H:skeleton_hero(1×h) / H:trollhalf_hero(1×h) · **p4** t:trollhalfcorrupted_t2(5) |
| 49 | 5/9 | trash | 20–20 | 20.0 | **p3** t:zombiesmutants_t2(6) · **p4** t:cultistchaos_t2(6) / t:cultistvitality_t2(6) · **p5**\* t:chthoniandreadguard_t2(5) · **p6** t:zombiesmutants_t1(3) |
| 50 | 5/10 | boss+trash | 18–21 | 20.0 | **p1** B:ghost_alkamos(1) · **p2** B:chthonian_salazar(2) · **p3** t:aetherialabomination_t2(3-4) / t:yeti_t2(6) / t:yetiswamp_t2(5-6) · **p4** t:zombies_t1(5) · **p6** t:zombies_t2(7) |
| 51 | 6/1 | hero-only | 0–3 | 3.0 | **p1** H:ghoul_hero(1×h) / H:zombies_hero(1×h) · **p2** Y:bounty_heroes×5 · **p3** H:golem_hero(1×h) / H:troll_hero(1×h) / H:yeti_hero(1×h) |
| 52 | 6/2 | hero+trash | 23–26 | 25.5 | **p1** t:chthonian_t2(6) · **p2** t:outlawrange_t2(6) / t:humanwendigo_t2(5-6) · **p3** t:trollhalf_cave_t2(6) / t:aetherialbloater_t2(5-6) · **p5**\* t:spiderdeepsambush_t2(7) · **p6** H:spider_hero(1×h) |
| 53 | 6/3 | trash | 10–11 | 10.5 | **p3** t:skeletonrevenant_t3(6) / t:trollswamp_t3(6) · **p4** t:aetherialreanimator_t2(4-5) / t:aetherialfleshshaper_t2(4-5) |
| 54 | 6/4 | boss+trash | 18–20 | 19.0 | **p1** t:rifthound_t2(6) / t:raptor_t2(6) · **p2** t:ghost_t1(5-6) · **p3** B:yeti_asterkarnmountains(1) / B:aetherial_fleshhulk_quarry(1) / B:swampcrab_carraxus(1) · **p6** t:ghost_t2(6-7) |
| 55 | 6/5 | boss+trash | 10–11 | 11.0 | **p1** t:zombies_t3(8) · **p2** B:skeleton_zarthuzellan(1) · **p3** D:devotion_heroes×6 · **p4** B:skeleton_rolderathis(1) |
| 56 | 6/6 | trash | 29–35 | 32.0 | **p1** t:skeletalgolem_t2(4) · **p2** t:cultistfire_t1(5) · **p3** t:cultistvitality_t1(5) · **p4** t:cultistpoison_t1(5) · **p5**\* t:ghost_t2(6-7) / t:skeleton_t2(7-8) / t:witchgod_raptor_t2(6) / t:aetherialimp_t2(5-7) · **p6** t:ghost_t2(6-7) / t:skeleton_t2(7-8) / t:witchgod_raptor_t2(6) / t:aetherialimp_t2(5-7) |
| 57 | 6/7 | hero+trash | 24–25 | 25.0 | **p1** t:gazer_t2(6) · **p2** t:gazer_t2(6) · **p3** Y:bounty_heroes01(1×h) / Y:bounty_heroes02(1×h) / Y:bounty_heroes03(1×h) · **p4** t:gazer_t2(6) · **p6** t:gazer_t2(6) |
| 58 | 6/8 | trash | 13–14 | 13.5 | **p2** t:outlawmelee_t3(7) / t:outlawrange_t3(7) · **p4** t:manticoreaether_t3(6-7) |
| 59 | 6/9 | boss+trash | 16–21 | 19.5 | **p1** D:devotion_heroes×6 · **p2** B:bonerat_ratden01(6) · **p3** t:chthonianvoid_t2(6) / t:chthonian_t2(6) / t:chthonianservitor_t2(4-5) · **p4** t:prawn_t2(7) / t:bonerat_t2(7-8) / t:wendigocannibal_t2(6-7) |
| 60 | 6/10 | boss+trash | 5–7 | 6.5 | **p1** B:necro_malkadar(1) · **p2** D:devotion_heroes×6 · **p3** B:zealot_archon(1) · **p6** t:chthonian_t1(3-4) |
| 61 | 7/1 | boss+trash | 13–13 | 13.0 | **p1** B:chthonian_bloodlord(1) / B:chthonian_devourerashenwastes(1) · **p3** t:outlawaether_t2(6) / t:humanpossessed_t2(6) · **p4** t:outlawaether_t2(6) / t:humanpossessed_t2(6) |
| 62 | 7/2 | hero+trash | 26–32 | 28.5 | **p1** t:mosquito_t1(6-7) / t:waspgiant_t1(6-7) · **p2** t:spider_t1(5) / t:prawn_t1(5) / t:swampcrab_t1(5-6) · **p3** t:aetherialreanimator_t3(5-6) · **p4** t:spider_t1(5) / t:prawn_t1(5) / t:swampcrab_t1(5-6) · **p5**\* t:spider_t1(5) / t:prawn_t1(5) / t:swampcrab_t1(5-6) · **p6** H:slith_hero(1×h) |
| 63 | 7/3 | boss+trash | 13–14 | 14.0 | **p1** t:outlawrange_t2(6) · **p2** t:outlawaether_t2(6) · **p3** B:chthonian_bloodlord(1) · **p4** H:cultist_hero(1×h) / H:skeleton_hero(1×h) / H:swampcrab_hero(1×h) / H:ghostcrab_hero(1×h) |
| 64 | 7/4 | hero+trash | 20–27 | 22.8 | **p1** t:zealot_t1(4) / t:outlawmelee_t1(4-6) · **p2** t:trollhalfcorrupted_t3(6) / t:trollhalf_t3(7-8) · **p3** t:slith_b_t2(6) / t:slith_c_t2(6) · **p4** t:zealot_t1(4) / t:outlawmelee_t1(4-6) · **p6** H:zealot_hero(1×h) |
| 65 | 7/5 | **boss-only** | 2–4 | 4.0 | **p1** B:chthonian_sharzhul(1) · **p2** B:ghoul_gollus(1) · **p3** H:chthoniandreadguard_hero(1×h) / H:chthoniandefiler_hero(1×h) · **p4** H:groble_hero(1×h) / H:trollhalf_hero(1×h) |
| 66 | 7/6 | hero+trash | 13–20 | 17.2 | **p1** H:harpy_hero(1×h) / H:dermapteran_hero(1×h) / H:bonerat_hero(1×h) / H:basilisk_hero(1×h) · **p2** t:witchgod_bonerat_t3(7) / t:witchgod_prawn_t3(7) / t:ghostcrab_t3(6-7) · **p3** t:harpy_t1(3-4) / t:witchgod_rifthound_t1(4-6) / t:humanascendant_t1(4-5) · **p4** t:dermapteran_t1(5-6) / t:witchgod_spider_t1(4-6) / t:humanascendant_t1(4-5) |
| 67 | 7/7 | hero+trash | 21–27 | 24.5 | **p1** D:devotion_heroes×6 · **p2** t:thornedhorror_t2(6) / t:dranghoul_t2(4) · **p3** t:groble_b_t2(6-7) / t:groble_c_t2(6-7) · **p4** t:thornedhorror_t2(6) / t:dranghoul_t2(4) · **p5**\* t:zombiesice_t2(7) / t:zombiespoison_t2(7) |
| 68 | 7/8 | trash | 17–17 | 17.0 | **p3** t:chthoniandreadguard_t3(6) / t:chthonianleech_t3(6) · **p4** t:chthoniandreadguard_t3(6) / t:chthonianleech_t3(6) · **p6** t:chthonianleech_t2(5) |
| 69 | 7/9 | boss+trash | 18–18 | 18.0 | **p1** t:zombiesmutants_t2(6) / t:outlawaether_t2(6) · **p2** t:skeletonwarlocks_t2(5) · **p3** t:zombiesmutants_t2(6) / t:outlawaether_t2(6) · **p4** B:ghostcrab_mine(1) / B:aetherialcolossus_galakros(1) |
| 70 | 7/10 | hero+trash | 18–24 | 22.2 | **p1** t:boarfrost_t3(5-6) / t:chthonianleech_t3(6) / t:chthonianservitor_t3(4-5) · **p2** t:skeletalgolem_t2(4) · **p3** t:chthonianminion_t3(6-7) · **p4** t:boarfrost_t3(5-6) / t:chthonianleech_t3(6) / t:chthonianservitor_t3(4-5) · **p6** Y:bounty_heroes×5 |
| 71 | 8/1 | trash | 20–22 | 20.5 | **p1** t:troll_t1(2) / t:trollswamp_t1(2) · **p2** t:boar_t2(6-7) / t:thornedhorror_t2(6) · **p3** t:troll_t3(6) / t:trollswamp_t3(6) · **p4** t:boar_t2(6-7) / t:thornedhorror_t2(6) |
| 72 | 8/2 | boss+trash | 9–13 | 11.5 | **p1** B:dermapteran_queen(1) · **p2** B:ghost_oligarch01(1) / B:ghost_oligarch02(1) / B:ghost_oligarch03(1) · **p3** t:dermapteran_t2(10) / t:waspgiant_t2(7) · **p6** D:devotion_heroes×6 |
| 73 | 8/3 | trash | 16–20 | 18.2 | **p3** t:zombies_t2(7) / t:groble_a_t2(6-7) · **p4** t:ghoul_t3(7-8) · **p5**\* t:chthoniandreadguard_t2(5) / t:fleshhulk_t2(3) |
| 74 | 8/4 | hero+trash | 17–22 | 19.8 | **p3** t:raptor_t3(8) · **p4** t:mosquito_t3(9) / t:dermapteran_t3(12-13) · **p5**\* H:chthoniandreadguard_hero(1×h) / H:fleshhulk_hero(1×h) / H:aetherialcolossus_hero(1×h) |
| 75 | 8/5 | boss+trash | 12–19 | 16.2 | **p1** B:ghost_baronwradlith(1) / B:ghost_maninneed(1) / B:aetherialfleshshaper_hinissius(1) · **p2** D:devotion_heroes×6 · **p3** D:devotion_heroes×6 · **p4** t:blacklegion_t2(6-7) / t:outlawrange_t2(6) · **p5**\* t:ghost_t2(6-7) / t:skeleton_t2(7-8) / t:chthoniandevourer_t2(8-9) / t:aetherialcorruption_poison_t2(5-6) |
| 76 | 8/6 | hero+trash | 29–35 | 32.2 | **p1** t:cultistpoison_t2(6) / t:zombiespoison_t2(7) · **p2** t:cultistvitality_t2(6) / t:trollhalf_cave_t2(6) · **p3** t:cultistchaos_t3(7-8) / t:skeletonwarlocks_t3(6) · **p4** t:gazer_t2(6) / t:groble_b_t2(6-7) · **p5**\* t:vultureambush_t2(6) / t:harpyambush_t2(5-6) · **p6** H:zombies_hero(1×h) |
| 77 | 8/7 | hero+trash | 4–9 | 8.0 | **p1** H:trollhalfcorrupted_hero(1×h) / H:trollswamp_hero(1×h) · **p2** D:devotion_heroes×6 · **p3** Y:bounty_heroes01(1×h) / Y:bounty_heroes02(1×h) / Y:bounty_heroes03(1×h) · **p4** t:fleshhulk_t3(4) / t:troll_t3(6) |
| 78 | 8/8 | trash | 17–28 | 23.2 | **p3** t:chthoniandevourer_t2(8-9) / t:chthonianfiend_t2(7-8) / t:chthonianrylok_t2(4-5) · **p4** t:chthoniandevourer_t2(8-9) / t:chthonianfiend_t2(7-8) / t:chthonianrylok_t2(4-5) · **p5**\* t:skeletalgolem_t3(6) · **p6** t:chthonianminion_t1(3-4) |
| 79 | 8/9 | boss+trash | 9–11 | 10.5 | **p1** H:cultist_hero(1×h) / H:necro_hero(1×h) / H:zealot_hero(1×h) · **p2** B:outlaw_pitmaster(1) / B:aetherial_theoutcast01(1) / B:humanascendant_terrnox(1) / B:humanascendant_valaxteria(1) · **p3** t:aetherialabomination_t2(3-4) · **p4** t:chthoniandefiler_t2(5) |
| 80 | 8/10 | boss+trash | 21–24 | 23.0 | **p1** B:chthonian_unraveler(1) / B:outlaw_darius(1) · **p2** t:skeleton_t3(8) / t:slith_a_t3(7) · **p3** B:skeleton_deathrevenant(1) · **p4** t:dermapteran_t3(12-13) · **p6** H:ghost_hero(1×h) |
| 81 | 9/1 | hero+trash | 14–15 | 15.0 | **p3** t:witchgod_raptor_t3(7) / t:witchgod_rifthound_t3(7) · **p4** t:witchgod_prawn_t3(7) / t:witchgod_spider_t3(7) · **p6** H:raptor_hero(1×h) |
| 82 | 9/2 | hero+trash | 7–11 | 10.5 | **p1** H:waspgiant_hero(1×h) / H:vulture_hero(1×h) / H:mosquito_hero(1×h) · **p2** D:devotion_heroes×6 · **p5**\* t:ghost_t3(7-8) · **p6** Y:bounty_heroes01(1×h) / Y:bounty_heroes02(1×h) / Y:bounty_heroes03(1×h) |
| 83 | 9/3 | trash | 8–12 | 10.5 | **p1** t:chthoniandefiler_t3(6) / t:aetherialabomination_t3(4-5) · **p4** t:chthoniandefiler_t3(6) / t:aetherialabomination_t3(4-5) |
| 84 | 9/4 | boss+trash | 19–23 | 20.3 | **p1** B:witchgod_bysmielguardian(1) / B:witchgod_dreegguardian(1) / B:witchgod_solaelguardian(1) · **p2** t:chthonianvoid_t2(6) / t:skeleton_t2(7-8) / t:aetherialcorruption_t2(6-7) · **p3** t:witchgod_hellhound_t2(6) / t:witchgod_bonerat_t2(6) / t:witchgod_raptor_t2(6) · **p4** t:chthonianvoid_t2(6) / t:skeleton_t2(7-8) / t:aetherialcorruption_t2(6-7) |
| 85 | 9/5 | hero+trash | 24–26 | 26.0 | **p1** D:devotion_heroes×6 · **p2** t:trollhalf_t2(6) / t:trollhalf_cave_t2(6) · **p3** t:zombiessoldiers_t3(7) / t:outlawmelee_t3(7) · **p4** t:troll_t3(6) / t:trollswamp_t3(6) · **p5**\* t:skeletonrevenant_t2(5) · **p6** H:chthonian_hero(1×h) |
| 86 | 9/6 | boss+trash | 16–19 | 18.0 | **p1** B:slith_viloth(1) · **p2** B:slith_primordian(3) · **p3** t:slith_a_t3(7) / t:slith_c_t3(7) · **p4** t:golem_t3(5-7) · **p6** H:golem_hero(1×h) |
| 87 | 9/7 | boss+trash | 29–39 | 33.8 | **p1** t:spider_t2(8-9) / t:dermapteran_t2(10) · **p2** t:chthonianfiend_t2(7-8) / t:chthonianleech_t2(5) · **p3** B:troll_smugglerpass(4) / B:chthonian_outcasttarget(1) / B:chthonianservitor_lunalvalgoth(1) · **p4** t:spider_t2(8-9) / t:dermapteran_t2(10) · **p5**\* t:spiderdeeps_t2(7) |
| 88 | 9/8 | hero+trash | 17–24 | 21.2 | **p1** H:yeti_hero(1×h) / H:dermapteran_hero(1×h) / H:yetiswamp_hero(1×h) · **p2** H:humanpossessed_hero(1×h) / H:ghoul_hero(1×h) / H:wendigocannibal_hero(1×h) · **p3** t:chthonianminion_t3(6-7) · **p4** t:boar_t2(6-7) / t:dranghoul_t2(4) · **p6** t:chthonianfiend_t2(7-8) |
| 89 | 9/9 | **boss-only** | 3–3 | 3.0 | **p1** B:skeleton_kilrian(1) / B:wendigo_namadea(1) · **p2** B:aetherial_commander(1) / B:chthonianrylok_gabalthunn(1) · **p3** B:troll_swampking(1) / B:swampgolem_bargoll(1) |
| 90 | 9/10 | **NEMESIS** | 1–2 | 2.0 | **p3** B:nemesis_chthonian(1) · **p6** H:prawn_hero(1×h) / H:aetherialimp_hero(1×h) / H:wendigocannibal_hero(1×h) |
| 91 | 10/1 | trash | 27–39 | 33.0 | **p1** t:chthoniandevourer_t2(8-9) / t:harpy_t2(5-6) · **p2** t:gazer_t2(6) · **p3** t:chthoniandevourer_t2(8-9) / t:harpy_t2(5-6) · **p4** t:gazer_t2(6) · **p5**\* t:chthoniandevourer_t2(8-9) / t:harpy_t2(5-6) |
| 92 | 10/2 | boss+trash | 25–32 | 28.4 | **p1** B:dermapteran_vizier01(1) / B:dermapteran_vizier02(1) / B:beetle_maggot(1) · **p2** B:dermapteran_vizier03(1) · **p3** t:zombiesaether_t2(7) / t:humanpossessed_t2(6) / t:humankorvaak_t2(5-6) · **p4** t:yeti_t3(7) · **p5**\* t:skeletonranged_t2(7-8) / t:vultureambush_t2(6) · **p6** t:skeletonranged_t2(7-8) / t:aetherialbloater_t2(5-6) |
| 93 | 10/3 | hero+trash | 7–10 | 9.8 | **p3** H:spider_hero(1×h) / H:bonerat_hero(1×h) / H:groble_hero(1×h) / H:beetle_hero(1×h) · **p4** Y:bounty_heroes×5 · **p5**\* t:ghost_t3(7-8) / t:spiderdeepsambush_t3(8) |

*(`\*` = ProxyAmbush spawn point. `D:devotion_heroes×6` / `Y:bounty_heroes×N` collapse the per-record devotion- and bounty-hero pool families, each of which is a weighted alternative yielding exactly one champion.)*

**Reading of the sitting-1 death.** Wave 93 is *not* a density wave (E = 9.75, second-lowest in its decade). It is a **hero-saturation wave**: four hero pools plus five bounty-hero pools plus one ambush point — nine of its ≤10 bodies are champion-tier. It follows immediately after wave 91 (up to 39 monsters) and wave 92 (up to 32 monsters plus four bosses), i.e. the fixture died on the third wave of a decade that opens with the two densest waves in the band and then flips to an all-champion composition. Wave 90 — three waves earlier — is the **first nemesis wave in the entire Crucible** (Benn'Jahr, the Colossal, solo).

**Band-A landmarks worth carrying to the sim:** wave 87 is the band's density peak (29–39, E 33.8); waves 56 / 76 / 91 sit at 29–39; waves 51, 65, 89, 90 collapse to 0–4 bodies of pure champion/boss content; wave 89 is the band's only pure boss wave (exactly 3 bosses, no trash); wave 90 opens the nemesis era.

### 3.2 Band B — waves 150–160 (sitting 2)

Σ raw E = **155.5 monsters** over 11 waves. Nemesis waves in band: **{150, 154, 160}**.

**Entry-point correction (U-8).** The commission frames sitting 2 as "checkpoint 150 → death at 160." U-8 read the Crucible's Lua sequencer and found the checkpoint label names the wave you are *credited* with, not the wave you fight: selecting "Start on Wave 150" sets the counter to 151 and skips the increment, so the first wave actually spawned is `tier16waves/proxy_w01_*` = **wave 151**. **The fixture therefore fought waves 151→160 — ten waves, not eleven — and never saw wave 150.** I retain wave 150 in the table below because it is the band's heaviest nemesis wave and the sim will want it, but it should be excluded from any sitting-2 reconstruction. Excluding it: **Σ raw E = 137.6 over 10 waves, nemesis waves {154, 160}**.

| wave | t/w | class | min–max | E | Gladiator composition |
|---:|:---|:---|:---|---:|:---|
| 150 | 15/10 | **NEMESIS** | 13–20 | 17.9 | **p1** B:nemesis_all_nooutlaw(1) · **p2** B:nemesis_all(1) · **p3** B:nemesis_all_nokymon(1) · **p4** t:necro_t3(7-8) / t:cultistvitality_t3(7-8) / t:zealot_t3(7) / t:humanwendigo_t3(5-6) · **p5**\* t:zombies_t3(8) / t:chthonian_t3(7) / t:chthonianvoid_ambush_t3(7-8) / t:wraith_t3(5-6) · **p6** D:devotion_heroes×6 |
| 151 | 16/1 | hero+trash | 13–22 | 18.5 | **p1** t:wraith_t3(5-6) / t:ghost_t3(7-8) · **p2** H:wraith_hero(1×h) / H:wendigo_hero(1×h) · **p3** H:swampgolem_hero(1×h) · **p4** t:wraith_t3(5-6) / t:ghost_t3(7-8) · **p5**\* t:livingplant_t3(3-4) |
| 152 | 16/2 | boss+trash | 6–11 | 10.5 | **p1** H:swampcrab_hero(1×h) / H:ghostcrab_hero(1×h) / H:springscrab_hero(1×h) · **p2** H:basilisk_hero(1×h) / H:thornedhorrorfrost_hero(1×h) · **p3** t:basilisk_t3(5-6) / t:thornedhorrorfrost_t3(5-6) · **p4** B:swampcrab_carraxus(1) / B:aetherialfleshshaper_hinissius(1) / B:aetherialfleshshaper_haraxis(1) / B:fleshweaverkrieg(1) · **p5**\* H:aetherialcorruption_hero(1×h) · **p6** D:devotion_heroes×6 |
| 153 | 16/3 | hero+trash | 12–18 | 16.8 | **p1** t:wendigo_t3(4-5) · **p2** Y:bounty_heroes×5 · **p3** t:skeletonrevenant_t3(6) / t:giant_t3(5-6) · **p4** Y:bounty_heroes×6 · **p5**\* t:livingplant_t3(3-4) · **p6** H:chthoniandreadguard_hero(1×h) / H:giant_hero(1×h) |
| 154 | 16/4 | **NEMESIS** | 9–10 | 9.5 | **p1** B:chthonian_bloodlord(1) / B:fatherkymon(1) · **p2** B:chthonianrylok_gabalthunn(1) / B:chthoniantyrant_grulthunn(1) · **p3** B:nemesis_beast(1) / B:nemesis_eldritch(1) / B:nemesis_kurn(1) · **p4** t:chthonianwretch_t3(6-7) / t:wendigocannibal_t3(6-7) / t:eldritcharmor_fire_t3(6-7) |
| 155 | 16/5 | boss+trash | 12–17 | 14.3 | **p1** B:aetherialcorruption_intro(1) · **p2** B:humanascendant_mindthief(1) / B:eldritcharmor_mindreaper(1) · **p3** t:aetherialimp_t3(5-7) / t:aetherialcorruption_poison_t3(5-6) / t:eldritchwraith_t3(5-6) · **p4** t:aetherialimp_t3(5-7) / t:aetherialcorruption_poison_t3(5-6) / t:eldritchwraith_t3(5-6) · **p6** Y:bounty_heroes×5 |
| 156 | 16/6 | boss+trash | 16–21 | 18.6 | **p1** B:witch_janaxia(1) · **p2** B:basilisk_witchritual(1) / B:direwolf_frozenwastes(1) · **p3** B:witch_larria(1) / B:kurnchthonic_shaman(1) · **p4** t:aetherialbloater_t3(5-6) / t:swampgolem_t3(3-5) / t:statue_t3(3-4) / t:chthonianherald_t3(5-6) · **p5**\* t:aetherialcorruption_fire_t3(5-6) / t:aetherialcorruption_ice_t3(5-6) / t:aetherialcorruption_lightning_t3(5-6) · **p6** t:humanwendigo_t3(5-6) |
| 157 | 16/7 | boss+trash | 7–16 | 13.9 | **p1** B:wendigocannibal_packla(1) / B:ghoul_nercropolis(1) / B:aetherialbloater_malmouthdocks(1) · **p2** D:devotion_heroes×6 · **p3** t:chthonianrylok_t3(4-5) / t:chthonianservitor_t3(4-5) / t:chthonianleech_t3(6) / t:gargoyle_t3(3-4) · **p4** t:swampgolem_t3(3-5) / t:aetherialbloater_t3(5-6) / t:skeletalgolem_t3(6) / t:yetidire_t3(5-6) · **p5**\* H:aetherialimp_hero(1×h) / H:aetherialcorruption_hero(1×h) / H:wight_hero(1×h) · **p6** H:aetherialcolossus_hero(1×h) |
| 158 | 16/8 | hero+trash | 15–36 | 25.0 | **p1** t:chthoniandevourer_t3(9-11) / t:swampcrab_t3(6-7) / t:sandlizard_t3(5-6) · **p2** D:devotion_heroes×6 · **p3** t:chthoniandevourer_t3(9-11) / t:swampcrab_t3(6-7) / t:sandlizard_volcanic_t3(5-6) · **p4** t:chthoniandevourer_t3(9-11) / t:swampcrab_t3(6-7) / t:sandlizard_eldritch_t3(5-6) · **p5**\* H:wraith_hero(1×h) / H:hypporaven_hero(1×h) · **p6** H:aetherialfleshshaper_hero(1×h) / H:dranghoul_hero(1×h) |
| 159 | 16/9 | **boss-only** | 5–7 | 5.5 | **p1** B:chthonianservitor_lunalvalgoth(1) / B:manticore_matriarch(1) · **p2** B:skeletalgolem_ilgorr(1) / B:aetherial_fleshhulk_quarry(1) / B:gryphonstone(3) / B:rok_wind(1) · **p3** B:witchgod_sentinel(1) · **p4** B:wendigo_namadea(1) / B:humanwendigo_gloomwald(1) / B:beetle_maggot(1) / B:yeti_rimehorn(1) · **p5**\* B:chthonianrylok_ekketzul(1) / B:korvaakmessenger(1) |
| 160 | 16/10 | **NEMESIS** | 4–5 | 5.0 | **p1** B:nemesis_all(1) · **p2** B:nemesis_all_noaetherialvanguard(1) · **p3** B:nemesis_wendigooraetherialvanguard(1) · **p4** B:aetherialcolossus_galakros(1) / B:korvaaktombguardian(1) · **p6** H:wendigocannibal_hero(1×h) |

**Note on wave 150 (not fought by the fixture — see the entry-point correction above).** It is the only wave in either priority band where the Gladiator view differs from Aspirant, and the difference is at **p02**, which on Gladiator/Challenger swaps to the unrestricted `nemesis_all` pool. Result: wave 150 puts **three independent nemesis rolls** on the board (p01, p02, p03) plus 15–16 trash plus a devotion hero. That makes wave 150 — the checkpoint the fixture started from — **the heaviest nemesis wave below 170**.

---

## §4 — Q3: wave 160, the kill wave

`records/proxies/tier16waves/proxy_w10_p{01,02,03,04,06}a.dbr`, all `Class: Proxy`, all owned by `sm3`, none carrying a Legendary override (so Aspirant = Challenger = Gladiator here: **the composition is difficulty-invariant**).

**Five spawn points. Zero trash pools. Three nemesis slots + one superboss + one hero. Realized count = 5 raw (see §4.6 for the modifier-adjusted band).**

| point | pool | picks | roster (weight) |
|---|---|---|---|
| **p01** | `records/proxies/poolsboss/nemesis_all.dbr` `[sm3]` `spawn 1-1` | 1 of 10, uniform | Valdaran, the Storm Scourge · Benn'Jahr, the Colossal · **Zantarin, the Immortal** · Fabius "the Unseen" Gonzar · Moosilauke, the Chillwind · The Iron Maiden · Raddoth, Lord Hierophant · Curate Ignus · Shriek · Vinn "the Giant" Ozmald — **each w = 100, limit = 1, `lv8_boss+`** |
| **p02** | `poolsbossgdx1/nemesis_all_noaetherialvanguard.dbr` `spawn 1-1` | 1 of 5, uniform | Kubacabra, the Endless Menace · Grava'Thul, the Voiddrinker · Reaper of the Lost · The Underking · Reaper of Rot |
| **p03** | `poolsbossgdx1/nemesis_wendigooraetherialvanguard.dbr` `spawn 1-1` | 1 of 2, 50/50 | Archmage Aleksander · Reaper of the Lost |
| **p04** | `poolsbossgdx1/aetherialcolossus_galakros.dbr` (w=100) **/** `poolsbossgdx2/korvaaktombguardian.dbr` (w=100) | 1 of 2 pools, 50/50 | Galakros, the Mountain · The Steward — both `lv7_uber hero` |
| **p06** | `poolsherogdx1/wendigocannibal_hero.dbr` `champChance 100 %` | 1 of 5, uniform | Ulda Emberclaw · Haldra the Bloodlust · Palros ~ Defender · Allcadius the Unburied ~ Reflective · Gaddo Evergrown ~ Bramble |

There is no p05, so **no ambush drip**: all five arrive together.

### 4.1 Statlines of the wave-160 roster (base, before survival adjustment)

`characterAttributeEquations` evaluated at charLevel 104 (= L100 player under `lv8_boss+`).

| Monster | bio | base HP @ L104 | base OA | base DA | skills |
|---|---|---:|---:|---:|---:|
| all 16 nemeses except Kubacabra | `bio_boss_nemesis_01` | **308,685** | 849 | 715 | 10–15 |
| Kubacabra, the Endless Menace | `bio_boss_nemesis3phase_01` | 245,089 | 849 | 715 | 14 |
| Galakros, the Mountain | `bio_boss_aetherial_colossusgalakros` | 201,558 | 911 | 778 | 13 |
| The Steward | `bio_boss_tombguardian` | 201,558 | 828 | 705 | 12 |

Applying §2.8's Gladiator `characterLifeModifier = +168 %` gives roughly **827,000 effective HP per nemesis**, before ordinary Ultimate difficulty scaling. Four of those at once, plus a hero, with **zero trash to interrupt or leech from**.

### 4.2 Zantarin — the measured killer, and the exact mechanism

The fixture save banked `greatest-monster-killed[2].last-monster-hitBy = tagNemesis_OrderDeathsVigil01`. That tag resolves to **`records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01.dbr` = "Zantarin, the Immortal"**, and that record is in the wave-160 p01 pool at **p = 0.100** exactly.

Zantarin's kit (14 skills, `records/skills/nonplayerskills/bossskills/nemesis/`, damage arrays 60 ranks — array-max quoted; **rank binding at wave 160 is UNRESOLVED**, see §7):

| Skill | Payload |
|---|---|
| `zantarin_curse1` → `_curse1_buff` | **"Curse of Frailty"** (`tagClass03SkillName06A`). 10 m radius, 6 s, `pointBlank`. **`defensiveLife = −30`, `defensivePoison = −30`, `defensivePhysical = −12`, `characterRunSpeedModifier = −75`, `characterSpellCastSpeedModifier = −75`** |
| `zantarin_vitalitynovabarrage` | `offensiveLifeMin` up to **2,888**, `skillCooldownTime = 2.0 s` |
| `zantarin_undeathmissiles` | `offensiveLifeMin` up to **2,645** |
| `zantarin_vitalityburst` | `offensiveLife` **1,486–1,797** |
| `zantarin_deathaura` | `offensiveLifeMin` up to **561/tick**, `skillTargetRadius = 12.0` |
| `zantarin_passiveproperties` | `defensiveLife = 60` (60 % vitality res), `defensiveSlowLifeLeach = 500`, `offensiveCritDamageModifier = +74 %`, **`retaliationSlowLifeMin = 113` with `retaliationSlowAttackSpeedGlobal = True` and `retaliationSlowRunSpeedGlobal = True`** |
| `zantarin_summonrevenant`, `_boneshield`, `_reactivesummonskeletalarcher`, `_reactiveundeathmissile` | summons + on-hit reactives |

**The mechanism is coherent and complete.** Curse of Frailty strips 30 points of vitality resistance and cuts movement 75 %, inside a 10 m radius, while the 12 m death aura ticks and a 2-second-cooldown vitality nova barrage lands for up to ~2,888 pre-mitigation. A player pinned at −75 % run speed cannot leave either radius. Additionally, **Zantarin's passive retaliates against every incoming hit with a global attack-speed and run-speed slow** — which is a targeted anti-pattern for a *channelled melee spin* like Eye of Reckoning, whose entire damage model is hits-per-second in contact range.

### 4.3 The other credible killers in the same wave

Ranked by threat to a physical/internal-trauma melee Warlord specifically:

1. **Grava'Thul, the Voiddrinker** (p02, p = 0.20). `chthonian02_nullification` → **"Nullified" — `tagEnemySkillNullification01Desc` verbatim: *"Your auras and buffs have been temporarily nullified."*** 3 s duration, plus `offensiveManaBurnDrainMin`. An EoR Warlord's survivability is almost entirely buff-stack (Presence of Virtue, Divine Mandate, Field Command, Overguard-class layers, plus the fixture's measured devotion procs Turtle Shell / Arcane Barrier). Nullification deletes that stack for 3 s. Paired with `chthonian02_homingchaos` at up to **6,729 chaos** — the single largest per-hit number in the wave-160 roster — and `chthonian02_auraofoppression` (−15 % attack speed, −15 % cast speed, `notDispelable`). **This is the wave's most build-specific killer.**
2. **Archmage Aleksander** (p03, p = 0.50). `aetherialvanguard_aethermeteor` up to **4,893 aether**, 3 m radius, plus two Panetti's-Replicating-Missile nova skills and a self-teleport. Aether is the classic Warlord resistance hole.
3. **Valdaran, the Storm Scourge** (p01, p = 0.10). `valdaran_lightningorbnova` up to **4,766 lightning**, `valdaran_lightningbolt` up to 3,666, plus `teleportswap` — he can move the player *into* the other three bosses.
4. **The Underking** (p02, p = 0.20). `beast2_toxiccadence` up to **3,286 physical + 1,957 poison over 12 s**, charge-up 6 s. Highest raw physical hit in the wave.
5. **Benn'Jahr, the Colossal** (p01, p = 0.10). `bennjahr_chaosstomp` up to 2,155 chaos, 9 m radius, plus `obsidianprison` (a hard lockdown) and `summoncluster`.
6. **The Iron Maiden** (p01, p = 0.10). `ironmaiden_ringofiron` up to **2,350 pierce + 714 bleed/5 s**, 4 m radius, 20 s cooldown, **`notDispelable = True`** — and she runs a full player Soldier kit (Cadence, Blade Arc, Blitz, Overguard, Menhir's Will, Markovian's, Zolhan's), i.e. she out-Warlords the Warlord.

### 4.4 A cross-check that does NOT close — flagged

The same save field group records `last-monster-hit = tagEnemySkeletonC04 = "Death Revenant"`. **No record carrying that tag is spawnable at wave 160.** Death Revenant is reachable in band B only at **wave 153** (`poolsbasic/skeletonrevenant_t3` p03 at p = 0.20; `poolsbounty/bounty_heroes03 → odv_bounty13` p02/p04) and **wave 155** (`bounty_heroes03` p06). Wave 160's entire population is 16 nemeses + Galakros/The Steward + 5 wendigo-cannibal heroes; none is a skeleton.

Therefore **the two "last monster" fields cannot both date from wave 160.** Either `last-monster-hit` is stale from wave 153/155 while `last-monster-hitBy` is current (which is what the save-parse note assumed and what the DB permits), or the two fields update on different cadences and the Zantarin reading is itself carried from wave 150 (where Zantarin's appearance probability is 0.311 across three independent nemesis points). **Reported, not resolved.** It does not overturn the Zantarin verdict — Zantarin *is* in the wave-160 pool — but it means the identification rests on a 1-in-10 prior plus a save field of unverified freshness, and the sim should not treat "Zantarin killed the fixture at 160" as certain.

Worth noting as a coincidence and not more: `odv_bounty13` — the bounty-hero record that also displays as "Death Revenant" — is an **Order of Death's Vigil** record, the same faction as Zantarin.

### 4.5 Where Zantarin can appear at all

15 of 200 waves. P(present) computed as 1 − Π(1 − 1/|roster|) across that wave's independent nemesis points:

| wave | 110 | 120 | 125 | 130 | 140 | **150** | **160** | 165 | 170 | 185 | 186 | 190 | 191 | 193 | 196 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P | .100 | .125 | .100 | **.500** | .100 | **.311** | **.100** | .100 | .234 | .111 | .125 | .319 | .125 | .125 | .100 |

Wave 130 is the standout: `poolsboss/nemesis_necro` has a 2-name roster, so Zantarin is a coin flip there.


### 4.6 How many bodies wave 160 actually puts on the board — measured, with the residual named

Applying U-9's `ignoreGameBalance` finding to wave 160 specifically:

| point | pool | `ignoreGameBalance` | takes the Gladiator spawn-count modifiers? |
|---|---|---|---|
| p01 | `poolsboss/nemesis_all` | **True** | **no — exempt** |
| p02 | `poolsbossgdx1/nemesis_all_noaetherialvanguard` | **True** | **no — exempt** |
| p03 | `poolsbossgdx1/nemesis_wendigooraetherialvanguard` | **True** | **no — exempt** |
| p04 | `poolsbossgdx1/aetherialcolossus_galakros` · `poolsbossgdx2/korvaaktombguardian` | *field absent* | **yes** |
| p06 | `poolsherogdx1/wendigocannibal_hero` | **False** (explicit) | **yes** |

So **the three nemesis slots are exempt by an explicit flag** — my §2.9 guard reached the right answer on those three by the wrong route. But **p04 and p06 are not exempt**, which means the Gladiator additive terms (`spawnMax +1`, `championMin/Max +1`) do apply there. Under full modifier application wave 160 becomes **3 nemeses + 2 superbosses + 2 heroes = 7 bodies**, not 5.

I do **not** assert 7. Whether a `spawnMin = spawnMax = 1` boss pool with no exemption flag actually doubles is precisely the residual U-9 bounded (operator order + clamp direction, ±1.9 % across waves 151–170), and it is U-9's model to settle, not this probe's. **The defensible statement is: wave 160 presents 5 bodies raw and at most 7 under full modifier application; all three nemesis slots are exactly one each regardless.** The sim should take the count from U-9's model and the *composition* from this note.

Exemption rate across the sitting-2 band, measured: wave 150 3/17 · 151 0/8 · 152 1/18 · 153 0/17 · **154 5/10** · 155 0/14 · 156 2/13 · 157 0/21 · 158 0/19 · **159 4/13** · **160 3/6**. The exemption concentrates exactly where it should — on the boss and nemesis waves.

---

## §5 — Q5: the werewolf confound — FLAG COUNT

**Scope of the sweep:** all 200 waves × all spawn points × all three difficulty views → 1,617 distinct monster records; token-matched on both record path and localization display name.

### 5.1 ACTIVE flags: **ZERO**

| token | occurrences in the Crucible composition |
|---|---:|
| `werewolf` | **0** |
| `wereraven` | **0** |
| `wereform` | **0** |
| `lycan` | **0** |
| `shifter` | **0** |

**No werewolf-family monster record appears anywhere in the Crucible, at any wave, at any difficulty.** The wave-composition surface is *unaffected* by the 1.3.0.0 → 1.3.0.5 werewolf drift documented in the patch-delta probe (2026-08-04 §2.4, C-2/C-3). The declared confound does not bind here.

Corpus-wide, only **three** werewolf-family records exist outside player-FX/PC trees:

| Record | Effective owner | Referenced by any proxy pool? |
|---|---|---|
| `records/creatures/enemies/boss&quest/werewolf_edgeofsanity_01.dbr` — **"Kovcha"** (`tagGDX3NPC_AREAH_40`), `monsterClassification = Quest` | `gdx3` | **0 referrers, corpus-wide** |
| `records/creatures/enemies/faction/npc_werewolf_allied.dbr` | `gdx3` | 0 |
| `records/creatures/enemies/bios/bio_boss_werewolf_01.dbr` | **`sm3`** (also carried by `gdx3`) | referenced only by the two above |

### 5.2 LATENT flag: **ONE** — and it is a real overlay divergence

`records/creatures/enemies/bios/bio_boss_werewolf_01.dbr` is carried by **both** `GDX3.arz` and `SurvivalMode3.arz`. The survival copy wins the overlay, and the two copies **differ in exactly one of ten fields**:

```
characterLife    gdx3 = ((charLevel*44)^1.53)+6000
                 sm3  = ((charLevel*30)^1.5)+500
```

At charLevel 100 that is ≈ **382,000 HP (campaign)** versus ≈ **164,800 HP (survival copy)** — the survival copy is about **43 %** of the campaign statline. Because nothing in the Crucible composition references it, the divergence is **inert**: it changes no wave, no count, no sim input. But it is a live trap for any future join that resolves `bio_boss_werewolf_01` through the survival overlay stack — it will silently return the low-HP curve. **Logged so a later probe does not rediscover it as a contradiction.**

### 5.3 ADJACENCY flags: **49 records** that a naive token search would surface and that are NOT werewolves

| family | distinct records | waves touched | in wave 160? |
|---|---:|---:|---|
| `wendigo*` (Wendigo, Ugdenbog Cannibal, Reaper of the Lost / Reaper of Rot) | **38** | 45 | **yes** — `nemesis_wendigo_01/02` at p02 and p03; `wendigocannibal_h01–h05` at p06 |
| `hypporaven*` (Hypporaven, Evernight) — nearest name-neighbour to "wereraven" | 8 | 9 | no (waves 147–149, 158, 172, 176, 182, 189, 198) |
| `direwolf*` (Siff Icehowl) | 1 | 3 (156, 189, 197) | no |
| `zombieberserker*` ("Walking Dead", "Corpsefiend") | 2 | 14 | no |

**These are name collisions, not the confound.** They are listed so downstream agents do not re-flag them, and so nobody mistakes the wave-160 wendigo content (which is substantial) for werewolf content.

### 5.4 Verdict on the confound for this probe

The 1.3.0.4 werewolf hitbox change and the 1.3.0.1/1.3.0.4 low-level boss-HP passes touch the **player's** wereform and the **levels 1–35** boss band. The Crucible wave composition is neither. **Wave composition at 1.3.0.0 is a safe join surface for the sim.** The pinning caveat that remains live is the patch-delta probe's C-3 line about *"Crucible wave-200 spawns"* — that is tier 20, wave 10, outside both priority bands, and I did not attempt to re-verify it against 1.3.0.5.

---

## §6 — Q4 + Q6: coarse bands and arena geometry

### 6.1 Coarse decade table, Gladiator view, all 200 waves

| decade | Σmin | Σmax | ΣE | wave classes | families entering this decade |
|:---|---:|---:|---:|:---|:---|
| 1–10 | 123 | 155 | 138.8 | trash×7, hero+trash×2, boss+trash×1 | **35** — zombies, bonerat, groble_a, prawn, cultistmelee, gazer, aetherialhorror, aetherialwisps, thornedhorror, spiderambush … |
| 11–20 | 159 | 186 | 175.1 | trash×4, hero+trash×3, boss+trash×3 | **30** — spiderdeeps, trollhalf, outlawmelee, necro, zealot, blacklegion, outlawaether, spider, cultistvitality … |
| 21–30 | 183 | 229 | 205.5 | hero+trash×4, trash×3, boss+trash×3 | **21** — ghoul, slith, prawndeeps, harpyambush, cultistpoison, dermapteran_vizier01–03, rifthound_bonehunter … |
| 31–40 | 145 | 171 | 164.1 | hero+trash×4, trash×3, boss+trash×3 | **18** — **bounty_heroes01–03**, zombiessoldiers, aetherialabomination, chthoniandefiler, aetherial_warden, manticore … |
| 41–50 | 138 | 166 | 155.7 | trash×4, boss+trash×4, hero+trash×2 | **16** — skeletalgolem_ilgorr, swampgolem_bargoll, **wendigo**, dranghoul_gutworm, chthonian_karroz, necro_captain … |
| 51–60 | 148 | 173 | 165.5 | boss+trash×4, trash×3, hero+trash×2, hero-only×1 | **16** — humanwendigo, chthonian, aetherialbloater, aetherialfleshshaper, swampcrab_carraxus, witchgod_raptor … |
| 61–70 | 161 | 196 | 181.1 | hero+trash×5, boss+trash×3, boss-only×1, trash×1 | **16** — chthonian_bloodlord, swampcrab, ghostcrab, slith_b/c, **chthonian_sharzhul**, ghoul_gollus, humanascendant … |
| 71–80 | 154 | 203 | 183.2 | boss+trash×4, trash×3, hero+trash×3 | **17** — dermapteran_queen, ghost_oligarch02/03, aetherialcolossus, ghost_baronwradlith, chthonianrylok … |
| 81–90 | 138 | 174 | 160.3 | hero+trash×4, boss+trash×3, trash×1, boss-only×1, **NEMESIS×1** | **16** — **witchgod_{bysmiel,dreeg,solael}guardian**, slith_primordian, slith_viloth, lunal'valgoth … |
| 91–100 | 140 | 199 | 175.9 | boss+trash×5, hero+trash×3, trash×1, **NEMESIS×1** | **23** — beetle_maggot, humankorvaak, chthonian_obsidianthrone, fleshweaverkrieg, mummy_osyr, wraith … |
| 101–110 | 143 | 199 | 174.4 | hero+trash×4, boss+trash×4, boss-only×1, **NEMESIS×1** | **27** — prawn_ikrix, gryphon_temple, scorpion, aetherial_amalgamation, lizard_desert, skeletalgolem_arkoviancoliseum … |
| 111–120 | 169 | 232 | **207.0** | boss+trash×4, hero+trash×3, **NEMESIS×2**, trash×1 | **26** — korvaakascendant, skeletalgolem_uroboruukguardian, humanwendigo_gloomwald, eldritchhound_*, statue … |
| 121–130 | 193 | 237 | **217.7** | boss+trash×5, hero+trash×3, **NEMESIS×2** | **9** — aetherialfleshshaper_haraxis, gryphonstone, human_dravis, **nemesis_necro**, **nemesis_zealot**, aetherial_loxmere … |
| 131–140 | 132 | 201 | 177.5 | boss+trash×5, hero+trash×1, hero-only×1, trash×1, boss-only×1, **NEMESIS×1** | **4** — livingplant, eldritcharmor_lightning, aetherial_theoutcast03, **fatherkymon** |
| 141–150 | 128 | 216 | 181.5 | boss+trash×5, hero+trash×3, boss-only×1, **NEMESIS×1** | **24** — humanascended, humankurn, witchgod, wight_iceboundpassage, springscrab, yeti_chthonic … |
| 151–160 | 99 | 163 | 137.6 | boss+trash×4, hero+trash×3, **NEMESIS×2**, boss-only×1 | **22** — thornedhorrorfrost, giant, **nemesis_beast**, **nemesis_eldritch**, **nemesis_kurn**, direwolf_frozenwastes … |
| 161–170 | 85 | 124 | 108.6 | boss+trash×5, **NEMESIS×3**, hero+trash×1, boss-only×1 | **21** — **nemesis_aetherialvanguard**, avian, rhino, wendigo_{handarroth,ollivioth,yuvolloth}, kurnchthonic_chieftain … |
| 171–180 | 82 | 120 | 106.8 | **NEMESIS×5**, boss+trash×5 | **18** — rok, beastroguelike_manticore, human_korvaak, **celestial{armor,statue,gryphon,lizard,hound}**, tombheretic_morgoneth … |
| 181–190 | 74 | 105 | 95.8 | **NEMESIS×7**, boss+trash×3 | **12** — **nemesis_wendigo**, rokvoid, scorv, icedefiler, factoryguardians, celestialmonstrosity … |
| 191–200 | 78 | 103 | 95.5 | **NEMESIS×8**, boss+trash×2 | **3** — nemesis_all_nonecro, groblefrost, **dread** |

**The design curve, stated plainly.** Trash volume peaks at decade 121–130 (ΣE 217.7) and then falls by more than half to 95.5 by 191–200, while the nemesis-wave count rises monotonically from 0 (waves 1–89) to 8 of 10 (waves 191–200). The Crucible does not get denser; it gets **harder per body**. The inflection is wave ~150: everything before it is a volume test, everything after it is a boss-gauntlet.

**Nemesis entry ladder (34 nemesis waves total):**
- **wave 90** — first ever (Benn'Jahr, solo)
- 100 (Valdaran), 110 (`nemesis_all`), 115, 120, 125, 130, 140, 150 — roughly every 10th
- **154** — first multi-nemesis-*family* roll (`nemesis_beast` / `_eldritch` / `_kurn` on one point)
- **160** — first wave with **three** independent nemesis points
- 161, 165, **170** (six nemesis pools across four points — the biggest in the game)
- 171, 175, 176, 179, 180, 181, 185, 186, 187, 188, 189, 190, 191, 192, 193, 195, 196, 198, 199, 200

**Roster additions by tier band:** `nemesis_all` grows from 8 members (base game) to 10 (with outlaws) to 16 (with `nemesis_beast`, `_chthonianvoidborn`, `_wendigo_01/02`, `_aetherialvanguard`) plus FoA's `_eldritch` (Kaisan, Ixall) and `_kurn` (Nyarlathon) families entering at wave 154 and `nemesis_wendigo` as a named pool at 181.

### 6.2 Spawn-point occupancy by decade

| decade | p01 | p02 | p03 | p04 | p05\* | p06 |
|:---|---:|---:|---:|---:|---:|---:|
| 1–10 | 7/10 | 5/10 | 7/10 | 6/10 | 2/10 | 4/10 |
| 41–50 | 8/10 | 7/10 | 8/10 | 9/10 | 3/10 | 6/10 |
| 91–100 | 8/10 | 7/10 | 9/10 | 8/10 | 6/10 | 6/10 |
| 141–150 | 10/10 | 10/10 | 10/10 | 10/10 | 8/10 | 7/10 |
| 151–160 | 10/10 | 10/10 | 10/10 | 10/10 | 7/10 | 7/10 |
| 181–190 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 6/10 |
| 191–200 | 10/10 | 10/10 | 10/10 | 10/10 | 9/10 | 6/10 |

Full 20-row table in `s7_out.txt`. Points 1–4 saturate from wave ~111 onward; p05 (the ambush) saturates only above wave 180; p06 hovers at 4–7/10 throughout because it is the optional point.

### 6.3 Q6 — arena geometry: **PARTIALLY DB-resident, and the answer is mostly NO**

**What IS in the database:**

| Fact | Value | Source |
|---|---|---|
| Scatter radius around a spawn point | **`placementExtents = 8.0`** — identical on all 925 wave proxies | wave proxy records |
| Proxy marker scale / mesh | `scale = 2.0`, `mesh = creatures/enemies/proxybounty01.msh` — identical on all 925 | wave proxy records |
| Number and identity of spawn points | 6, named `spawnpoint02..06` + per-tier `tier<NN>spawnpoint01` (20 records) | `records/scriptentities/` |
| Other arena fixtures | 5 spawn beacons, 7 defense points + 7 defense-point NPCs, 8 trap points, 5 reward chests, 2 bonus chests, 1 event NPC, 1 merchant NPC, 1 `playerspawnpoint` (`sm3`) | `records/scriptentities/` |
| Ambush alert radius | `alertArea = 100.0` on all 107 p05 records | ProxyAmbush records |
| Aggro / view distance override | **absent** — no `viewDistanceOverride` / `roamBehaviorOverride` / `distressCallRangeOverride` in the survival archives (unlike Shattered Realm's `dungeonset*` rulesets, which carry all three) | measured absence |

**What is NOT:** the **world coordinates** of any of those fixtures. Every `tier<NN>spawnpoint01.dbr` is `Class: ScriptEntity` carrying only `onAddToWorld = gd.survival.tier<NN>Waves.spawnPoint01OnAddToWorld`, `onRemoveFromWorld`, `editorMesh`, `editorScale`, `pathing = False`. No position field exists on any survival record — a field-name sweep across all four survival archives for `position|worldpos|coord|spawnloc|location|levelname|mapname|worldmap` returns only UI-bitmap offsets and two boss-skill `spawnLocations` count arrays (Kaisan's phase-1/phase-2 lightning-strike patterns, values 5–9).

**Root cause, confirmed by file census:** the Edition-II fetch contains **0 `.wrl`, 0 `.map`, 0 `.lvl`, 0 `.msh`** files. Level geometry ships in `Levels.arc`, which is not in the fetch. This reproduces the 2026-08-01 finding on the campaign side.

**Recommendation for the sim's arena shell.** The DB gives you: 6 fixed emitters, each scattering its pack over an 8.0-unit radius, one of which (p05) is optional-drip and one of which (p06) is player-toggled, with a 100-unit ambush alert radius, and the player entering at a single `playerspawnpoint`. It does not give you the polygon those emitters sit in. **Model the arena as a shell with 6 parameterised emitter positions and treat the positions as a free parameter**, or measure them from a screen capture — do not go looking for them in the `.arz`.

---

## §7 — Named gaps (what this probe did not close)

| # | Gap | Consequence | Suggested next move |
|---|---|---|---|
| **G-1** | **Wave-timing and inter-wave cadence are script-resident, not data.** `records/game/survivalinfo.dbr` carries only `difficultyTimes = [300, 600, 900]` and sound refs; the wave→wave sequencing sits in `gd.survival.tier<NN>Waves.*` Lua | The sim can compose each wave but has no DB-grounded duration, bonus-timer, or inter-wave gap | `difficultyTimes` is a plausible 5/10/15-minute score-multiplier ladder but the binding is unread. Screen capture, or `Game.dll` string search |
| **G-2** | **Boss/nemesis skill RANK at a given wave is unresolved.** Skill damage arrays are 60 ranks; I quoted array maxima | Every damage figure in §4 is a **ceiling**, not the wave-160 value | Ranks likely bind to monster level via a `skillLevel` field on the Monster record or via `levelVarianceEquation`; needs a dedicated rank-binding probe (same class of question as the grimtools 60-vs-26 contradiction) |
| ~~**G-3**~~ | ~~`spawnMinModifier` semantics inherited, not verified~~ | — | **CLOSED by U-9** (`gameproxies.tpl`: `"Percent (0 or 100) no change"` → ×1.20 on Gladiator). Residual operator-order/clamp uncertainty is U-9's, bounded to ±1.9 % across waves 151–170 |
| **G-4** | **`ProxyAmbush.maxGroupSize` vs pool budget interaction** (§2.5) | p05's realized concurrency could be 30 rather than its pool count on any wave | Counted screen capture on a p05 wave (waves 4, 6, 13 are early and cheap to reach) |
| **G-5** | **The wave-160 save cross-check does not close** (§4.4) — Death Revenant is not spawnable at 160 | "Zantarin killed the fixture" is a 1-in-10 prior plus a save field of unverified freshness | Determine the write cadence of `last-monster-hit` vs `last-monster-hitBy` in the `.gdc` block; or accept as unresolved |
| **G-6** | **Celestial Blessings / Defenses / Tributes are not modelled here.** `records/skills/powerups` (12), `records/creatures/defenses` (21), `records/skills/defenses` (28) exist and are unextracted | The fixture measured `survival-defense-built +4` and `powerups-activated +0` during the sittings — the defenses were live, the blessings were not | A follow-on probe; the records are small and fully DB-resident |
| **G-7** | **4 dangling roster references.** `poolshero/bonerat_hero → hero/scavenger_h075.dbr` (waves 7, 66, 93) and `poolsbossgdx3/wight_hags → boss&quest/wight_scarfelldepths_01/02/03.dbr` (waves 177, 195) point at records absent from all 8 archives — 9 occurrences, 5 waves | ≤4 roster slots of ~7,000 resolve to nothing; the wight_hags pool is a wave-177/195 boss slot, so 1-in-N boss odds there are slightly off | Almost certainly cut content or a `Levels.arc`-side record; low value, but the wight_hags case sits in a boss pool and should be re-checked if waves 171–200 ever become priority |
| **G-8** | **Version skew is unmeasured on this surface.** Everything above is 1.3.0.0; the client is 1.3.0.5 | Low risk (§5.4), but not zero — 1.3.0.4's patch notes were not re-read for Crucible wave changes | Re-read the 157189 thread for `Crucible`/`Nemesis`/`wave` lines, or cut an Edition-III `.arz` at 1.3.0.5 |

---

## §8 — Source list

**Primary (datamined, this probe):**
- `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` — 8 `.arz` + 4 `Text_EN.arc`, sha256s in §1.1. Accessed 2026-08-07, read-only.
- Record paths cited inline throughout.

**Primary (localization, verbatim tags quoted):** `tagNotification_Checkpoint05/10/15/18`, `tagHUDWaveTier01`, `achS001Desc`, `achS007Desc`, `tagClass03SkillName06A`, `tagEnemySkillNullification01Desc`, `tagEnemySkeletonC04`, `tagNemesis_OrderDeathsVigil01`, `tagGDX3NPC_AREAH_40`.

**Sibling Phase-A probes (landed in parallel; reconciled in §2.10):**
- `agentic_orchestration/legolas/notes/2026-08-07-u8-tier-wave-map.md` — tier→wave map from the Crucible Lua sequencer; 200-wave ceiling; the checkpoint-150-starts-at-151 correction.
- `agentic_orchestration/legolas/notes/2026-08-07-u9-spawnmin-operator-order.md` — `spawnMinModifier` semantics from `gameproxies.tpl`; `ignoreGameBalance`; no player-count scaling; champions add; p06 opt-in from Lua.

**Prior probes (substrate, read at start):**
- `agentic_orchestration/legolas/notes/2026-08-01-gd-pack-density-ranking.md` — extraction pattern, tier-wave record naming, `gameproxies` scalars, `levelVarianceEquation` model. **Amended by this probe on two points: the difficulty axis (§2.4) and p05's ambush nature (§2.5).**
- `agentic_orchestration/legolas/notes/2026-08-04-gd-1305-patch-delta-probe.md` — werewolf confound C-2/C-3.
- `agentic_orchestration/legolas/notes/2026-08-04-gd-crucible-checkpoint-edit-probe.md` — checkpoint token ladder, `survivalWaveTier = 170`.
- `agentic_orchestration/legolas/notes/2026-08-05-eorwarlguts-save-parse.md` — `last-monster-hitBy = tagNemesis_OrderDeathsVigil01`, wave-160 death, TIER18 = wave 180.
- `agentic_orchestration/legolas/notes/2026-07-26-gd-displayname-bridge.md` — the tag → record bridge used for every name above.

**Instruments:** `research/scripts/gd_arz_adapter_2026_07_24.py`, `research/scripts/gd_arc_reader_2026_07_26.py`.

**Reproducibility:** `agentic_orchestration/legolas/scratch/2026-08-07-pe6-crucible/` — `s1_orient.py`, `s2_schema.py`, `s3_owner_difficulty.py`, `s4_extract.py`, `s5_w160.py`, `s6_werewolf_and_scalars.py`, `s7_bands.py`, `s8_emit.py`; outputs `s4_waves_full.json`, `pe6_crucible_waves.csv`, `pe6_crucible_wave_pools.csv`, `band_a.md`, `s1..s8_out.txt`.

---

## §9 — CLOSURE VERDICT

**PARTIAL (named gaps G-1 … G-8).**

Composition is **CLOSED**: all 200 waves, all 925 spawn points, all 632 pools, all 1,617 monster records, all three difficulty views, zero unresolved references, both priority bands extracted at full grain with per-pool rosters and record paths. Wave-160 is closed to the record level. Structure (§2), bands (§3), wave 160 (§4), werewolf flag (§5), coarse bands and geometry (§6) all answered.

What is **not** closed is everything *temporal* and everything *rank-scaled*: wave duration and inter-wave cadence are Lua, not data (**G-1** — and U-8 has now opened that lane, so this is closable); boss-skill rank binding is unread, so every damage figure in §4 is a ceiling rather than a value (**G-2**, the largest remaining hole); `ProxyAmbush.maxGroupSize` vs pool-budget interaction (**G-4**); the fixture's own save cross-check does not resolve cleanly (**G-5**); Celestial Blessings and Defenses are unextracted (**G-6**); four dangling roster references (**G-7**); 1.3.0.5 skew unmeasured on this surface (**G-8**). **G-3 closed in-session against sibling probe U-9**, and §2.10 reconciles both U-8 and U-9 against this note — including one correction I would otherwise have shipped wrong: the fixture fought waves **151→160**, not 150→160. These are named holes in an otherwise complete table, which is the pre-declared shape of a valid Phase-A return.

**What plausibly killed the fixture at 160.** Wave 160 is the first wave in the Crucible to put *three independent nemesis rolls plus a superboss plus a hero on the board simultaneously with zero trash* — five champion-tier bodies, each nemesis carrying roughly 827,000 effective HP under Gladiator's +168 % life modifier, arriving together with no ambush drip and nothing to leech from or interrupt against. The save names Zantarin, the Immortal, and Zantarin is measurably in that wave's p01 pool at exactly 1-in-10; his kit is a precise counter to a channelled melee Warlord — Curse of Frailty strips 30 points of vitality resistance and cuts run speed 75 % inside a 10 m radius while a 12 m death aura ticks and a 2-second-cooldown vitality nova barrage lands, and his passive retaliates against *every incoming hit* with a global attack-speed and run-speed slow, which is exactly the wrong thing to happen to a build whose damage is hits-per-second in contact range. But the honest reading is that Zantarin is one of several sufficient causes rather than the demonstrated one: Grava'Thul (p = 0.20 at p02) carries Nullification, which deletes the entire buff-and-devotion stack the fixture's 20K effective pool is built on, for 3 seconds, alongside the largest per-hit number in the wave (up to 6,729 chaos); Archmage Aleksander sits at p = 0.50 on p03 with a 4,893-aether meteor into a classic Warlord resistance hole; and the wave-160 Death Revenant contradiction (§4.4) means the save's Zantarin field cannot be dated to wave 160 with certainty. **The sim should model wave 160 as an all-champion, no-trash burst wave of 5 bodies raw (≤7 under full modifier application, §4.6), with three of the five slots guaranteed to be exactly one nemesis each — and should not over-fit to Zantarin specifically.**

**Werewolf flag count: 0 ACTIVE · 1 LATENT · 49 ADJACENCY.** Zero werewolf-family monster records appear anywhere in the Crucible composition, so the declared 1.3.0.0-vs-1.3.0.5 werewolf confound **does not bind this surface**. The one latent flag is `bio_boss_werewolf_01.dbr`, carried by both `GDX3.arz` and `SurvivalMode3.arz` with divergent `characterLife` equations (survival copy ≈ 43 % of campaign HP at L100) and referenced by no proxy pool anywhere in the game. The 49 adjacency flags are wendigo (38), hypporaven (8), direwolf (1) and zombieberserker (2) records that a naive token sweep would falsely surface — listed so they are not re-flagged downstream.
