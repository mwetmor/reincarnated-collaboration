# Research — Grim Dawn pack-density ranking (datamine-measured) — 2026-08-01

**Mode:** A (analytical / primary-source probe)
**Commissioner:** gandalf (RUN-CONDUCTOR, EoR-Warlord playtest prep)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Access:** READ-ONLY over `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (189 MB, 8 `.arz` archives)
**Adapter:** `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (`ArzArchive`)
**Reproducibility:** `agentic_orchestration/legolas/scratch/2026-08-01-density/` — `p0_orient.py` … `p17_agg.py`, plus emitted `campaign_rows.json`, `crucible_rows.json`, `sr_rulesets.json`
**Discipline:** R-BR-34 — every ranked claim below cites record path + field values.

---

## Summary

The densest monster placement in Grim Dawn is **not** in the hand-authored campaign; it is the **Shattered Realm shard floor**, and it is fully database-resident. `records/endlessdungeon/rulesets/dungeonset15.dbr` (`FileDescription = "Shard 33+"`) declares **29 common + 10 hero + 4 boss proxy placements per floor** and an engine-evaluated floor total of **142.5 (Normal) / 188.6 (Elite) / 209.4 (Ultimate)**. Second is the **Crucible**, where the densest single wave is **tier 14 / wave 06 at 30–42 monsters simultaneously across 5 spawn points** (`crucible_rows.json`). Third, and the densest *campaign* content, is the **Steps of Torment floor-5 wave-3 ambush at 24–25 concurrent**, tied on concurrency with Bastion of Chaos and Port Valbury trap rooms.

Two schema corrections against the commission's premises are load-bearing and reported as measured findings: (1) **`spawnMin`/`spawnMax` are pool fields, never `Proxy` fields** — 0 of 383 base `Class: Proxy` records carry them; (2) **per-room placement counts ARE recoverable for procedurally-generated content** (Shattered Realm), even though they are absent for the hand-authored campaign, because generator parameters must live in the database.

The folklore list scores about 50%. The locations folklore names as densest that the database can actually identify — Steps of Torment, Bastion of Chaos, Port Valbury — are confirmed as the campaign's top three. Cronley's Hideout, the Fleshworks, Ancient Grove, and Tomb of the Heretic are **UNPROBED**: they carry no named proxy records at all and are populated from generic area pools placed in level geometry we do not have.

---

## Top-line ranking table

| # | Locus | Measured density | Unit | Source record | DB-resident? |
|---|---|---|---|---|---|
| 1 | **Shattered Realm, Shard 33+** | **142.5 / 188.6 / 209.4** (Norm/Elite/Ult) per floor; 43 proxy placements | monsters per floor | `records/endlessdungeon/rulesets/dungeonset15.dbr` | **fully** |
| 2 | **Crucible tier 14 wave 06** | **30 min / 42 max**, E = 36.75 | simultaneous, one arena | `records/proxies/tier14waves/proxy_w06_p01a..p05a.dbr` | **fully** |
| 2b | Crucible tier 13 wave 06 | **35 min** / 36 max, E = 36.00 | simultaneous, one arena | `records/proxies/tier13waves/proxy_w06_p01a..p06a.dbr` | **fully** |
| 3 | **Steps of Torment, floor 5 wave 3** | `maxGroupSize = 25`, pool `spawnMin=spawnMax=24` | concurrent, sustained | `records/proxies/boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr` | partial (needs placement) |
| 3= | Bastion of Chaos, trap room wave 3 | `maxGroupSize = 25`, pool 19 + `championMax=1` @ 25% | concurrent, sustained | `records/proxies/boss&quest/proxy_aread_bastionofchaos_traproomwave3.dbr` | partial |
| 3= | Port Valbury, trap room wave 3 | `maxGroupSize = 25`, pool `spawnMax=10` | concurrent, sustained | `records/proxies/boss&quest/proxy_aread_portvalbury_traproomwave3.dbr` | partial |
| 4 | **Bastion of Chaos, endless gauntlet** | 13–14 concurrent, respawn at `spawnThreshold=4` every 0.75–1.0 s, pool `spawnMin=spawnMax=100` | unbounded throughput | `records/proxies/boss&quest/proxy_aread_bastionofchaos_gauntletendless.dbr` | partial |
| 5 | **Dermapteran Infestation (Act 3)** — densest single non-ambush pack in the game | `spawnMin=15 spawnMax=18`, `championChance=40 championMin=2 championMax=4` → **ceiling 22** | one pack | `records/proxies/boss&quest/questproxy_areac_dermapteraninfestation.dbr` | partial |

---

## Measured constraint — what this substrate cannot answer

**No level/world geometry is present.** Verified by `find` over the whole fetch: zero `.wrl`, zero `.map`, zero `.lvl`, no `Levels.arc`. The only `.arc` files in the fetch are `Text_EN.arc` (×5, localization strings). See `p0_orient.py` output.

Consequence: for the **hand-authored campaign**, the number of proxy *instances* placed in a given room is not recoverable. A `Proxy` record describes a pack *template*; how many copies of it a level designer stamped into Warden's Cellar is a fact about the `.lvl` file, not the `.arz`. **No per-room campaign aggregate is offered in this note, because the substrate cannot support one.**

This constraint does **not** bind the two loci that top the ranking. Crucible waves and Shattered Realm floors are both generated at runtime from database parameters, so their placement counts are in the `.arz` by necessity.

---

## Q1 — Campaign proxy density census

### Schema finding (measured absence, contradicts commission premise)

The commission specified reading `spawnMin`/`spawnMax` off each Proxy. **Those fields do not exist on `Class: Proxy`.**

```
Class=Proxy records (base): 383; carrying spawnMin/spawnMax: 0
```

Field-union by Class under `records/proxies/` in `database.arz` (`p2_pool.py`):

| Class | n | carries |
|---|---|---|
| `Proxy` | 383 | `pool1..pool6` + `weight1..6`, `placementExtents`, `time1`, `faction*` |
| `None` (template `proxypool.tpl`) | 657 | **`spawnMin` (614), `spawnMax` (614), `championChance` (567), `championMin` (574), `championMax` (567)**, `name1..12`/`weight`/`limit`, `nameChampion1..12`, `levelVarianceEquation*`, `minPlayerLevel*`, `proxyPoolEquation` |
| `ProxyAmbush` | 149 | `minGroupSize`, `maxGroupSize`, `spawnThreshold`, `minSpawnTime`, `maxSpawnTime`, `minDelayTime`, `maxDelayTime`, `alertArea` + pool refs |
| `SetPiecePool` / `SetPiece` / `SetPiecePart` | 120 / 106 / 2 | placement grouping, no spawn counts |

So density is a **two-hop resolution**: `Proxy.poolN` → pool record → `spawnMin`/`spawnMax`. The earlier `v4_density.py` printed `spawnMin=None spawnMax=None` for every proxy for this reason. All rankings below resolve the hop; **1,002 `Proxy` + 421 `ProxyAmbush` records resolved to at least one pool, with 0 unresolved pool references.**

Note that `Proxy.pool1..poolN` with `weightN` are **weighted alternatives** — the engine picks *one*. Therefore "ceiling" = `max` over pools of `spawnMax + championMax`, and `E[total]` = weight-normalized expectation including `championChance/100 × mean(championMin, championMax)`.

### Top 12 campaign `Proxy` records by ceiling

| ceiling | sMin | sMax | chMax | E[tot] | record |
|---|---|---|---|---|---|
| **22** | 15 | 18 | 4 | 17.70 | `boss&quest/questproxy_areac_dermapteraninfestation.dbr` |
| 14 | 10 | 12 | 2 | 13.00 | `boss&questgdx3/proxy_voidmarkedchest_01.dbr` |
| 14 | 10 | 14 | 0 | 12.00 | `areag/maggots_t.dbr` |
| 14 | 9 | 12 | 2 | 11.50 | `area001/undeadskeletongolem_t.dbr` |
| 13 | 7 | 10 | 3 | 10.00 | `boss&quest/proxy_twinfalls_skeleton_t.dbr` |
| 13 | 7 | 10 | 3 | 9.50 | `area001/faction_orderdeathsvigil_skeletons_t.dbr` |
| 13 | 7 | 10 | 3 | 9.50 | `area001/undeadskeletonsa_s2_n.dbr` |
| 13 | 7 | 10 | 3 | 9.50 | `areah/undead_skeletonsfrost_t.dbr` |
| 13 | 7 | 10 | 3 | 9.50 | `boss&quest/proxy_areab_stepsoftorment_floor5eventfiller.dbr` |
| 13 | 5 | 10 | 3 | 9.35 | `area001/witchgod_spider_t.dbr` |
| 13 | 6 | 10 | 3 | 9.25 | `area001/undead_ghosts+skeletons_t.dbr` |
| 13 | 6 | 10 | 3 | 9.00 | `area001/undead_ghouls_t.dbr` |

Distribution across all 1,002: ceiling **max 22, mean 5.88**; `E[total]` **median 4.50, mean 4.06**. The Dermapteran Infestation is a **3.7× outlier** over the median pack and 1.6× over the next-highest record — it is the single fattest authored pack in Grim Dawn.

Its pool (`boss&questpools/p_areac_dermapteraninfestation.dbr`) is worth quoting in full because the composition is unusual: `weight=1000, limit=2` on `dermapteran_infestedfieldsspawner.dbr` — a **spawner creature inside the pack**, so realized density exceeds the 22 ceiling by whatever the spawner emits. Champion roster is `weight=700` on `dermapteran_b02` plus five `_h0N` heroes at `minPlayerLevel=25`.

### Top 10 `ProxyAmbush` by concurrency

`ProxyAmbush` is the higher-density mechanic: it maintains a **live population** and refills when the survivor count drops to `spawnThreshold`.

| maxGrp | minGrp | thresh | pool sMax | chMax | respawn (s) | record |
|---|---|---|---|---|---|---|
| **25** | 24 | 3 | 24 | 0 | 0.25–0.5 | `boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr` |
| **25** | 24 | 3 | 19 | 1 | 0.25–0.5 | `boss&quest/proxy_aread_bastionofchaos_traproomwave3.dbr` |
| **25** | 24 | 3 | 10 | 1 | 0.25–0.5 | `boss&quest/proxy_aread_portvalbury_traproomwave3.dbr` |
| 21 | 20 | 3 | 20 | 0 | 0.25–0.5 | `boss&quest/proxy_areab_stepsoftorment_floor5wave2.dbr` |
| 21 | 20 | 3 | 16 | 0 | 0.25–0.5 | `boss&quest/proxy_aread_bastionofchaos_traproomwave2.dbr` |
| 18 | 17 | 3 | 17 | 0 | 0.25–0.5 | `boss&quest/proxy_areab_stepsoftorment_floor5wave1.dbr` |
| 16 | 16 | 0 | 15 | 1 | 0.5–1.5 | `boss&questgdx3/questproxy_waveevent_dranghoularena_wave02.dbr` |
| **14** | 13 | **4** | **100** | 0 | 0.75–1.0 | `boss&quest/proxy_aread_bastionofchaos_gauntletendless.dbr` |
| 12 | 6 | 3 | 15 | 1 | 1.0 | `boss&questgdx3/questproxy_waveevent_dranghoularena_wave03.dbr` |
| 12 | 5 | 3 | 11 | 1 | 0.25–0.5 | `boss&quest/proxy_aread_roverlegacy_wave3.dbr` |

Across all 421 ambushes: `maxGroupSize` **max 25, median 5**.

The **Bastion of Chaos endless gauntlet** deserves separate framing. Its concurrency cap (14) is modest, but the pool declares `spawnMin = spawnMax = 100` and the ambush refills whenever survivors fall to 4, every 0.75–1.0 s, with `maxDelayTime=16 / minDelayTime=14`. Roster is 6 Chthonic entries (`chthoniandevourer_a01` w=125; `chthonianfiend_a01/a02` w=100). **For total monsters processed per minute rather than monsters on screen, this is the campaign's densest room.**

### Aggregation by area token

| area token | n | nProxy | nAmb | max ceiling | max ambush grp | mean E | p90 E |
|---|---|---|---|---|---|---|---|
| `boss&quest:areab` (Act 2) | 22 | 11 | 11 | 13 | **25** | 3.02 | 6.25 |
| `boss&quest:aread` (Act 4) | 59 | 27 | 32 | 11 | **25** | 2.58 | 5.75 |
| `boss&quest:areac` (Act 3) | 30 | 21 | 9 | **22** | 12 | 2.38 | 6.00 |
| `area001` (shared campaign) | 302 | 239 | 63 | 14 | 7 | 5.27 | 7.55 |
| `areag` (FG / Act 7) | 162 | 117 | 45 | 14 | 5 | 5.09 | 7.62 |
| `areah` (FoA / Act 8) | 146 | 104 | 42 | 13 | 5 | 4.72 | 7.50 |
| `areae` (AoM / Act 5–6) | 90 | 72 | 18 | 12 | 5 | 5.41 | 8.00 |
| `boss&questgdx3` | 12 | 1 | 11 | 14 | 16 | 13.00 | 13.00 |
| `areavoid` | 31 | 15 | 16 | 10 | 5 | 5.00 | 5.88 |
| `monstertotem` (gdx2/3) | 26 | 0 | 26 | — | 8 | — | — |

Reading: **ambient/roaming density is highest in `areae` (AoM) and `area001`** (mean E 5.41 / 5.27, p90 8.00 / 7.55) — the expansion zones raised baseline trash density. But **peak** density is entirely in `boss&quest` set-piece rooms, which have *low* mean (2.4–3.0) because that tree is mostly single-boss proxies, and *maximal* extremes.

**Difficulty scalar (base `records/game/gameproxies.dbr`):** `spawnMax = [0, 1, 1]`, `championMax = [0, 2, 3]` — indexed Normal/Elite/Ultimate. Every ceiling above gains **+1 spawn and +3 champions on Ultimate**. The Dermapteran ceiling is therefore 22 on Normal and **26 on Ultimate**.

---

## Q2 — Crucible / Survival-mode waves

### Schema (first-of-kind documentation for this substrate)

Wave records live at `records/proxies/tier<NN>waves/proxy_w<WW>_p<PP>a.dbr`. **1,293 records across the 4 survival archives, 100% conformance to that pattern, 0 nonconforming** (`p4_wavenames.py`). Decoded: `NN` = tier 01–20, `WW` = wave 01–10, `PP` = spawn point 01–06.

Spawn points are corroborated by `records/scriptentities/spawnpoint02..06.dbr` and `spawnbeacon_01..05.dbr` in the same archive — **the Crucible arena has 6 fixed spawn positions**, and a wave activates a subset of them.

Resolution across the overlay stack (`sm_mod` → `sm1` → `sm2` → `sm3`, later wins): **925 spawn-point proxies, 200 distinct (tier, wave) pairs, 0 unresolved pool references.**

**Measured absence:** the tier→global-wave-number schedule is **not** in the database. `records/scriptentities/tier14spawnpoint01.dbr` carries `onAddToWorld = gd.survival.tier14Waves.spawnPoint01OnAddToWorld` — the sequencing is game script, not data. `records/game/survivalinfo.dbr` carries only sounds, FX, `difficultyTimes = [300, 600, 900]`, and the three balance-adjustment refs. Tier ordering below is therefore reported as tier index, **not** as an in-game wave number.

### Densest single wave in the game

**`tier14 / wave06` — 5 spawn points, 30 min / 42 max, E = 36.75.**

| point | min | max | E | pool options (weighted, engine picks one) |
|---|---|---|---|---|
| p01 | 6 | 9 | 7.50 | `poolsbasic/chthoniandevourer_t2` 8–9 · `poolsbasicgdx2/mummy_t2` 6–7 |
| p02 | 5 | 8 | 6.88 | `cultistchaos_t3` 7–8 · `necro_t3` 7–8 · `zealot_t3` 7–7 · `poolsbasicgdx1/humanwendigo_t3` 5–6 |
| p03 | 6 | 8 | 7.00 | `skeletonranged_t2` 7–8 · `poolsbasicgdx2/eldritcharmor_lightning_t2` 6–7 |
| p04 | 5 | 8 | 6.88 | (same 4-option set as p02) |
| p05 | 8 | 9 | 8.50 | `chthoniandevourer_t2` 8–9 |

All five pools have `championChance = 0` — **this wave is pure trash volume, no champions**, which makes it the cleanest high-count referent for a simulator.

### Top 10 waves

| tier | wave | pts | min | max | E | archives |
|---|---|---|---|---|---|---|
| **14** | **6** | 5 | 30 | **42** | **36.75** | sm_mod, sm1, sm2 |
| 12 | 1 | 6 | 33 | 40 | 36.50 | sm_mod, sm2 |
| 9 | 7 | 5 | 29 | 39 | 33.75 | sm_mod, sm1 |
| 10 | 1 | 5 | 27 | 39 | 33.00 | sm_mod |
| **13** | **6** | 6 | **35** | 36 | 36.00 | sm_mod, sm1 |
| 16 | 8 | 6 | 15 | 36 | 25.00 | sm3 |
| 8 | 6 | 6 | 29 | 35 | 32.25 | sm_mod |
| 6 | 6 | 6 | 29 | 35 | 32.00 | sm_mod, sm1 |
| 13 | 4 | 6 | 28 | 35 | 31.50 | sm_mod, sm1, sm2 |
| 3 | 4 | 6 | 30 | 33 | 32.00 | sm_mod |

**Simulator recommendation:** if the sim wants a *deterministic* dense room, prefer **tier 13 wave 06** — it has the highest guaranteed floor in the game (`min = 35`, spread over all 6 spawn points) with a tight 35–36 band, versus tier 14 wave 06's wider 30–42. If the sim wants the absolute ceiling, tier 14 wave 06.

### Per-tier totals (10 waves each)

| tier | Σ min | Σ max | Σ E | densest wave max |
|---|---|---|---|---|
| 1 | 141 | 172 | 155.2 | 21 |
| 2 | 161 | 188 | 176.3 | 27 |
| 3 | 188 | 237 | 212.0 | 33 |
| 4 | 161 | 186 | 178.1 | 27 |
| 5 | 143 | 179 | 164.9 | 28 |
| 6 | 161 | 185 | 177.0 | 35 |
| 7 | 160 | 196 | 181.1 | 32 |
| 8 | 154 | 203 | 183.2 | 35 |
| 9 | 138 | 174 | 160.3 | 39 |
| 10 | 140 | 199 | 175.9 | 39 |
| 11 | 143 | 199 | 174.4 | 32 |
| 12 | 168 | 232 | 207.0 | 40 |
| **13** | **193** | **237** | **217.7** | 36 |
| 14 | 132 | 201 | 177.5 | **42** |
| 15 | 127 | 216 | 181.5 | 31 |
| 16 | 99 | 163 | 137.6 | 36 |
| 17 | 85 | 124 | 108.6 | 21 |
| 18 | 82 | 120 | 106.8 | 20 |
| 19 | 74 | 105 | 95.8 | 18 |
| 20 | 78 | 103 | 95.5 | 18 |

**Tier 13 is the densest tier** (Σ E = 217.7). Note the **inversion above tier 15**: tiers 16–20 (the expansion-added bands, owned by `sm3`) drop to roughly half the count of tiers 12–15. Late Crucible trades *quantity* for *quality* — fewer, harder monsters. This is a designed density curve peaking around tiers 12–15, not a monotonic ramp, and it is a directly transferable finding for our own wave pacing.

**Difficulty scalar (`records/game/gameproxies.dbr`, SurvivalMode):** `spawnMax = [0,1,1]`, `championMin = [0,0,1]`, `championMax = [0,1,1]`, **`spawnMinModifier = [0, 112, 120]`**. On Ultimate the wave floor is multiplied by 1.20 and each pool gains +1 spawn: tier 14 wave 06 becomes roughly **36 min / 47 max**.

---

## Q2b — Shattered Realm (the actual answer, and an unexpected one)

`records/endlessdungeon/` sits **outside** `records/proxies/`, which is why the commission's search path would have missed it. It carries 2,209 records in GDX2 and 466 in GDX3, with classes `ProxyEndless` (238 / 123), `EndlessDungeonFloor` (110 / 17), and **`EndlessDungeonGenerator` (16 / 16)**.

`EndlessDungeonGenerator` **is the per-room placement census** — the exact data class the commission expected to be unrecoverable. It is present here precisely because Shattered Realm floors are generated at runtime, so their placement counts have to be data.

### All 16 rulesets ranked (identical in GDX2 and GDX3; 32 records total)

| ruleset | `FileDescription` | `proxies` | `heroProxies` | `bossProxies` | `floors` | floorTotal N | E | U |
|---|---|---|---|---|---|---|---|---|
| `dungeonset15` | **Shard 33+** | **29** | **10** | **4** | 3 | **142.5** | **188.6** | **209.4** |
| `dungeonset14` | Shard 25–32 | 29 | 9 | 4 | 3 | 138.5 | 182.6 | 201.9 |
| `dungeonset13` | Shard 24 | 29 | 8 | 4 | 3 | 134.5 | 176.6 | 194.4 |
| `dungeonset12` | Shard 19–23 | 29 | 8 | 4 | 3 | 134.5 | 176.6 | 194.4 |
| `dungeonset11` | Shard 18 | 29 | 8 | 4 | 3 | 134.5 | 176.6 | 194.4 |
| `dungeonset10` | Shard 17 | 29 | 7 | 4 | 3 | 130.5 | 170.6 | 186.9 |
| `dungeonset09` | Shard 13–16 | 28 | 7 | 3 | 3 | 127.0 | 166.2 | 182.3 |
| `dungeonset08` | Shard 12 | 28 | 7 | 3 | 3 | 127.0 | 166.2 | 182.3 |
| `dungeonset07` | Shard 9–11 | 28 | 6 | 3 | 3 | 123.0 | 160.2 | 174.8 |
| `dungeonset06` | Shard 8 | 27 | 6 | 3 | 3 | 119.5 | 155.8 | 170.2 |
| `dungeonset05` | Shard 6–7 | 27 | 6 | 3 | 3 | 119.5 | 155.8 | 170.2 |
| `dungeonset04` | Shard 5 | 27 | 5 | 2 | 3 | 115.5 | 149.8 | 162.7 |
| `dungeonset03` | Shard 4 | 27 | 5 | 2 | 3 | 115.5 | 149.8 | 162.7 |
| `dungeonset02` | Shard 2–3 | 26 | 4 | 2 | 3 | 108.0 | 139.4 | 150.6 |
| `dungeonset01` | Shard 1 | 26 | 3 | 1 | 3 | 104.0 | 133.4 | 143.1 |
| `dungeonset00` | TEST RULESET | 26 | 3 | 2 | 3 | 103.0 | 132.4 | 142.1 |

Floor-total equations, verbatim from `dungeonset15.dbr`:

```
floorTotalNormal   = 1.0 * (commonProxies * 3.5) + 1.0 * (heroProxies * 4) + 1
floorTotalElite    = 1.0 * (commonProxies * 4.4) + 1.0 * (heroProxies * 6) + 1
floorTotalUltimate = 1.0 * (commonProxies * 4.6) + 1.0 * (heroProxies * 7.5) + 1
```

**Two inferences, flagged as such:**

1. **`commonProxies` is not a literal field name.** The full field union for `EndlessDungeonGenerator` (`p14_verify.py`) contains `proxies`, `heroProxies`, `bossProxies`, `trapProxies`, `nemesisProxyWeights`, `shrineProxyWeights` — and **no `commonProxies`**. `heroProxies` binds by exact name; `proxies` is the only remaining common-proxy count field, so the binding `commonProxies := proxies` is near-certain but is an inference, not a read.
2. **Whether `floorTotal*` is a monster count or a floor kill-target is not determinable from the database alone.** An independent pool-derived estimate cross-checks it: SR `poolsbasic` (n=444) has mean `spawnMin` 5.17 / mean `spawnMax` 5.84 → ≈5.5 monsters per common placement. So Shard 33+ ≈ 29 × 5.5 ≈ **160 common** + 10 heroes (`poolshero`, n=80, all `spawnMin=spawnMax=0, championChance=100, championMax=1` → exactly 1 hero each) + 4 bosses (`poolsboss`, n=204, 177 of them `spawnMin=spawnMax=1`) ≈ **174 monsters/floor**. The engine's own equation brackets that (142.5 Normal → 209.4 Ultimate). **The two independent estimates agree to within ~20%, which is strong corroboration that `floorTotal` is a monster count.**

At 3 floors per shard, **a single Shard 33+ run is roughly 430–630 monsters.** Additional density riders on the same record: `championChance = 13`, `heroChance = 100`, `maxShrines = 2`, `shrineProxyWeights = [70, 25, 5]`, `viewDistanceOverride = 19.0`, `roamBehaviorOverride = NeverRoam`, `distressCallRangeOverride = 15.0`.

`viewDistanceOverride = 19.0` and `NeverRoam` are worth flagging for the Godot render: SR floors deliberately **compress the visible field and pin monsters in place**, so the ~174 monsters are experienced as a dense static carpet rather than a roaming swarm.

---

## Q3 — Level-band annotation

### Structural finding: Grim Dawn has no absolute monster levels

Every `levelVarianceEquation*` on every campaign pool resolves to one of 16 records under `records/proxies/lv*.dbr`, and **all 16 are expressed against `averagePlayerLevel`** (`p3_eq.py`):

```
lv1_weak            min/max = (averagePlayerLevel-1)
lv2_normal          min = (averagePlayerLevel-1)              max = (averagePlayerLevel)
lv3_strong          min = (averagePlayerLevel)                max = (averagePlayerLevel)+(averagePlayerLevel/75)
lv4_champion        min = (averagePlayerLevel+1)              max = (averagePlayerLevel+1)+(averagePlayerLevel/75)
lv5_elitechampion   min = (averagePlayerLevel+2)              max = (averagePlayerLevel+1)+(averagePlayerLevel/50)
lv6_hero            min = (averagePlayerLevel+2)+(apl/50)     max = (averagePlayerLevel+3)+(averagePlayerLevel/50)
lv7_uber hero       min = (averagePlayerLevel+3)              max = (averagePlayerLevel+3)+(averagePlayerLevel/50)
lv8_boss            min = (averagePlayerLevel+3)+(apl/50)     max = (averagePlayerLevel+4)+(averagePlayerLevel/50)
```

Usage across 1,657 pools: `lv3_strong` 2,011 · `lv4_champion` 1,510 · `lv2_normal` 1,366 · `lv5_elitechampion` 600 · `lv7_uber hero` 391 · `lv8_boss` 212.

**Consequence for the playtest: content is never level-locked. A level-20 EoR Warlord entering any zone meets monsters at levels 19–24.** The gate is campaign progression and survivability, not a level requirement — so "reachable at L15–25" is a question about *where the character has walked*, not about a database field.

### What `minPlayerLevel` actually gates

`minPlayerLevel<i>` gates **individual roster entries**, not spawn counts. Histogram over campaign pools:

```
2:5  3:21  4:10  5:17  6:8  7:20  8:21  9:7  10:50  11:7  12:47  13:2  14:70
15:337  16:21  18:15  20:17  22:3  24:18  25:33  28:1  29:1  30:48  31:1
35:317  40:18  45:223  50:29  55:130  65:72  70:76  75:9
```

Three large cliffs: **15** (337 entries), **35** (317), **45** (223). A level-20 character has crossed the L15 cliff and not the L35 one — so it sees the mid-tier `_b0N` variants but none of the `_c0N` elite variants.

Crucible pools show the same structure (`p15_q3.py`), with cliffs at 8 (100), 12 (111), **15 (179)**, 20 (132), **25 (216)**, 30 (63), 35 (69). Concretely, in the densest wave's pools:

- `poolsbasic/skeletonranged_t2` — `skeleton_a02_archer` ungated; `skeleton_b01_archer` and `skeleton_b04_warlock` at `minPL=15`; `skeleton_c01/c02/c03` at `minPL=25`.
- `poolsbasic/cultistchaos_t3` — `_a02` ungated; `_b01` at 10, `_b02` at 12, `_b03` at 16; `_c01/_c02` at **25**.
- `poolsbasic/chthoniandevourer_t2` — `_a01` ungated; `_b01/_b02` at 12.

**At level 20 the count is unchanged and the roster is truncated at the `_c` tier.** Spawn counts live on the pool, which carries no level gate at all — so a L20 character in Crucible tier 14 wave 06 still faces 30–42 monsters, just composed entirely of `_a` and `_b` variants.

### Band table for the top entries

| ceiling / maxGrp | band (campaign progression) | record |
|---|---|---|
| 22 | Act 3 (~L32–40) | `boss&quest/questproxy_areac_dermapteraninfestation.dbr` |
| **25** | **Act 2 (~L24–32)** | `boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr` |
| 25 | Act 4 (~L40–50) | `boss&quest/proxy_aread_bastionofchaos_traproomwave3.dbr` |
| 25 | Act 4 (~L40–50) | `boss&quest/proxy_aread_portvalbury_traproomwave3.dbr` |
| 21 | Act 2 (~L24–32) | `boss&quest/proxy_areab_stepsoftorment_floor5wave2.dbr` |
| 18 | Act 2 (~L24–32) | `boss&quest/proxy_areab_stepsoftorment_floor5wave1.dbr` |
| 14 | Act 4 (~L40–50) | `boss&quest/proxy_aread_bastionofchaos_gauntletendless.dbr` |
| **14** | **Act 1 / shared, L1+** | `area001/undeadskeletongolem_t.dbr` |
| **13** | **Act 1 / shared, L1+** | `area001/faction_orderdeathsvigil_skeletons_t.dbr`, `undeadskeletonsa_s2_n`, `undead_ghosts+skeletons_t`, `undead_ghouls_t`, `beasts_prawn_t`, `beastswastes_random`, `groblec+d_always` |
| 13 | Act 1, L1+ | `boss&quest/proxy_twinfalls_skeleton_t.dbr` |
| 12 | Act 1 (rift wave events) | `questproxy_waveevent_burrwitchrift_wave01.dbr`, `proxy_wightmireriftgate_wave1.dbr` |

Act-band assignment is derived from the `_area[a-h]_` infix in `boss&quest` record names (`p13_bands.py`: areab 22, areac 30, aread 60, areae 33, areaf 21, areag 62, areah 60 records) mapped to Grim Dawn's published act order. **The act→level mapping itself is genre knowledge, not measured** — flagged accordingly.

### Verdict for the EoR Warlord playtest

**Reachable-at-L20 density winner: `records/proxies/boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr` — 24–25 concurrent, sustained.** Steps of Torment is an optional Act 2 dungeon whose entrance is reachable in the L15–25 window; floor 5 sits at the deep end of it. It is the only 25-concurrent room in the game that a L20-ish character can physically stand in.

**Runner-up, zero progression risk: Crucible tier 14 wave 06 (30–42).** The database carries **no player-level gate on Crucible tier access** — tier selection is script-driven and level-agnostic, so a L20 character is mechanically permitted into tier 14. Survival is the only barrier, which is exactly the variable a playtest wants to measure.

**Safest ambient pick: `area001/undeadskeletongolem_t.dbr` (ceiling 14, 9–12 + 2 champions)** — an `area001` shared pool with `minPL = 0` on every roster entry, so it presents identically at L20 and L80.

---

## Q4 — Named-location hypotheses: tested, not trusted

Method: token match over all 82,131 campaign records, then over the 1,423 resolved proxy rows. Folklore claim on the left, measurement on the right.

| Folklore claim | Verdict | Measured |
|---|---|---|
| **Steps of Torment (Act 2)** | ✅ **CONFIRMED — #1 campaign** | 13 proxy records. `proxy_areab_stepsoftorment_floor5wave3` = `maxGroupSize 25`, pool `spawnMin=spawnMax=24` of pure skeletons (`skeleton_a01` w=100, `a02_archer` w=100 limit=8, `b04_warlock` limit=2, `b01_archer` limit=1, `b03_priest` limit=1). Waves 1/2/3 = 18/21/25. Best non-ambush: `floor5eventfiller` ceiling 13. |
| **Bastion of Chaos (Act 4)** | ✅ **CONFIRMED — tied #1** | 15 proxy records (80 total). `traproomwave3` = `maxGroupSize 25`, pool 19 + `championChance 25% championMax 1` over 12 named `waveevent_boc_*` heroes. Plus the endless gauntlet (pool `spawnMax=100`). |
| **Port Valbury (Act 4)** | ✅ **CONFIRMED — tied #1 on concurrency, thinner pools** | 19 proxy records. `traproomwave3` = `maxGroupSize 25` but pool only `spawnMax 10` — same ambush frame, half the pool. Folklore overrates it relative to SoT/BoC. |
| **Shattered Realm (GDX2)** | ✅ **CONFIRMED — #1 overall, by 5×** | Not under `records/proxies/` at all; 2,209 records under `records/endlessdungeon/`. See Q2b. |
| **Warden's Cellar / Burrwitch (Act 1)** | ⚠️ **PARTIAL** | 'warden' → 104 records, but all creature/controller/boss records (`boss&quest/warden01.dbr`, `controller_boss_warden`); the only proxy hit is `questproxy_areah_blacklodge_warden` (unrelated, FoA). 'burrwitch' → 7 proxy records, best is `questproxy_waveevent_burrwitchrift_wave01` at `maxGroupSize 12`. **Warden's Cellar itself has no named proxy** — it is populated from generic `area001` pools placed in level geometry. Its density is a placement fact, not a database fact. |
| **Cronley's Hideout (Act 2)** | ❌ **UNPROBED** | 32 records match 'cronley' — all NPC (`npc_dariuscronley_01`), loot (`breakable_cronleysecret_a01`), lore (`loreobject_cronley_random01`), and the `anm_dariuscronley` animation. **Zero proxy or pool records.** Hideout is filled from generic Act-2 pools; density not database-resolvable. |
| **The Fleshworks (Malmouth / GDX1)** | ❌ **UNPROBED** | **0 records match 'fleshwork' anywhere in 82,131 records.** The location name is not a database token at all. (`malmouth` → 43 proxy records; best is `questproxy_waveevent_malmouthdocks_wave01`, `maxGroupSize 12`.) |
| **Ancient Grove (GDX1)** | ❌ **UNPROBED for density** | 151 records match, but they are boss skills (`ancientgrove/slathsarr_*`) and SR boss pools (`poolsbossgdx1/ancientgrove_basilisk|manticore|swampgolem`). Only **one** proxy record: `proxy_areae_ancientgrove_trappedchest_01`, ceiling 1. Grove trash is generic `areae` pools. |
| **Tomb of the Heretic (GDX2)** | ❌ **UNPROBED for density** | 42 records match 'heretic' — creatures (`humanoutlaw_heretic_c01`), a blockade NPC, barrier FX, and `d01_bosschest_tombofheretic_boss01`. **Zero proxy or pool records.** |
| *(unsolicited)* **Dermapteran Infestation (Act 3)** | 🆕 **NEW — folklore misses it** | Ceiling 22, the highest single-pack value in the game, 1.6× the runner-up. Folklore does not list it. |

### The pattern behind the misses

The folklore locations that the database *can* identify are exactly the ones built on **`ProxyAmbush` wave events and trap rooms** — Steps of Torment, Bastion of Chaos, Port Valbury, and the rift wave-events at Burrwitch/Wightmire/Malmouth. Those got bespoke named proxy records because they are scripted set pieces.

The locations that come back UNPROBED — Cronley's Hideout, the Fleshworks, Ancient Grove, Tomb of the Heretic — are **hand-placed dungeons filled from generic area pools**. Their perceived density is a function of how many generic proxies the level designer stamped into a confined space, which is precisely the fact that lives in the missing `.lvl` files.

This is a clean, useful split rather than a gap: **scripted-density locations are fully measurable from the `.arz`; placement-density locations are not measurable at all without level geometry.** Folklore does not distinguish the two, and conflates "felt dense" across both mechanisms.

---

## Q5 — What a `Levels.arc` depot pull would add

A follow-up Steam depot fetch would need the level-geometry archives that the current Edition-II pull omits: **`resources/Levels.arc`** for the base campaign, plus the per-expansion **`gdx1/resources/Levels.arc`**, **`gdx2/resources/Levels.arc`**, and **`gdx3/resources/Levels.arc`**. The current fetch's `resources/` directories contain only `Text_EN.arc` (470 KB base, ~190–240 KB per expansion). The internal path convention is confirmed by `EndlessDungeonFloor.regions`, which reads e.g. `levels/endlessdungeon/boss/boss_necropolis_a01.lvl` — so `.lvl` region files, referenced by name from the `.arz` we already hold, are the join target. Acquiring them would convert every campaign row in this note from a *pack template* into a *per-room instance count*: how many copies of `undeadskeletongolem_t` sit inside Warden's Cellar, how many proxies the Fleshworks carries per corridor, and whether Cronley's Hideout beats Steps of Torment once placement is counted. It would also let us measure room *volume*, giving monsters-per-square-metre rather than monsters-per-pack — the metric the Godot render actually needs for camera framing. Cost is the main unknown: `Levels.arc` is the largest archive class in a Grim Dawn install and the pull would likely be several GB against the current 189 MB, so this should be queued as a `matt_to_do` row with an explicit size check before fetch, and an `ARC` reader extension (`gd_arc_reader_2026_07_26.py` currently targets `Text_EN.arc` string tables only, not `.lvl` binary regions).

---

## Knowledge gaps not resolved

1. **Per-room campaign placement counts** — blocked on `Levels.arc` (Q5). No workaround exists in this substrate.
2. **Crucible tier → global wave number** — the schedule is in game script (`gd.survival.tier14Waves.*`), not data. Tier indices in this note are not in-game wave numbers.
3. **`floorTotal*` exact semantics** — monster count vs. floor kill-target not resolvable from data alone; the pool-derived cross-check (≈174 vs. 142.5–209.4) supports "monster count" but does not prove it.
4. **`commonProxies` binding** — inferred to `proxies` by elimination, not read.
5. **Act → player-level mapping** — genre knowledge, not measured; the database has no absolute levels (Q3).
6. **`proxyPoolEquation`** — all 545 campaign pools reference `proxypoolequation_01.dbr`, which is identity (`poolValue * 1` on all four of `spawnMin/Max`, `championMin/Max`). Measured as a no-op in this dataset; it exists as a hook only.
7. **`monstertotem` (gdx2/gdx3, 241 + 280 records)** — Nemesis/shrine totem events, `Class: MonsterShrine` + `ProxyAmbush`, max `maxGroupSize` 8. Probed shallowly; not a top-density candidate, so not pursued.

---

## Source list

All sources are local, read-only, and vendor-datamined. No network access was used.

| Source | Path | Records |
|---|---|---|
| GD base database | `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/database/database.arz` | 34,114 (1,417 proxies) |
| Ashes of Malmouth | `…/gdx1/database/GDX1.arz` | 18,447 (740 proxies) |
| Forgotten Gods | `…/gdx2/database/GDX2.arz` | 16,451 (944 proxies; 2,209 endlessdungeon) |
| Fangs of Asterkarn | `…/gdx3/database/GDX3.arz` | 24,178 (1,277 proxies; 466 endlessdungeon) |
| Crucible base | `…/mods/survivalmode/database/SurvivalMode.arz` | 3,147 (1,099 proxies; 653 wave records) |
| Crucible AoM overlay | `…/survivalmode1/database/SurvivalMode1.arz` | 1,004 (218 wave records) |
| Crucible FG overlay | `…/survivalmode2/database/SurvivalMode2.arz` | 811 (120 wave records) |
| Crucible FoA overlay | `…/survivalmode3/database/SurvivalMode3.arz` | 1,431 (302 wave records) |
| Adapter | `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` | — |
| Prior art (superseded on the `spawnMin` premise) | `agentic_orchestration/legolas/scratch/2026-07-30-wr3-veteran/v4_density.py` | — |

**Scripts, in execution order** — all under `agentic_orchestration/legolas/scratch/2026-08-01-density/`:

`p0_orient.py` (archive census) · `p1_schema.py` (Class histograms, field unions) · `p2_pool.py` (**spawnMin/Max location finding**) · `p3_eq.py` (`proxyPoolEquation`, `levelVarianceEquation`) · `p4_wavenames.py` (wave naming, 0 nonconforming) · `p5_census.py` (**campaign master census** → `campaign_rows.json`) · `p6_ambush.py` (top-ambush full dumps) · `p7_crucible.py` (**Crucible census** → `crucible_rows.json`) · `p8_gamemap.py` (wave-schedule search) · `p9_survivalinfo.py` (difficulty scalars, spawn entities) · `p10_named.py` (**endlessdungeon discovery**) · `p11_sr.py` (SR schema) · `p12_srrank.py` (**SR ruleset ranking** → `sr_rulesets.json`) · `p13_bands.py` (level bands, folklore ledger) · `p14_verify.py` (SR semantics verification) · `p15_q3.py` (Crucible level gating) · `p16_tokens.py` (widened token search) · `p17_agg.py` (area-token aggregation)
