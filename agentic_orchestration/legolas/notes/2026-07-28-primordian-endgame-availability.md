# Primordian at endgame — availability per mode, measured from the Edition-II corpus

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-07-28 · **Commissioner:** gandalf
**Matt's question:** *"How can I fight Primordian at end game crucible?"*
**Class:** evidentiary — measured extraction from primary source
**Mode:** read-only. No writes outside `legolas/notes/` + `legolas/scratch/`.
**Predecessor:** `legolas/notes/2026-07-28-kitcal1-primordian-proto.md` (identity, kit, loot — all
carried forward unchanged; this note adds *availability* and *difficulty scaling*)

**Grading key:** **M** = MEASURED (field read verbatim from `.arz`) · **D** = DERIVED (arithmetic
shown, operator named) · **U** = UNRESOLVED / boundary of this lane.

---

## 0. Headline — the answer, four lines

1. **Yes, Primordian is in the Crucible, and the corpus contains the Crucible.** The Edition-II
   fetch carries `mods/survivalmode/` (3,147 records) plus three Crucible DLC packs. **No
   supplementary fetch is needed.** **M.**
2. **Two Crucible spawn points, both measured:** `tier09 / wave 06` and `tier14 / wave 02` —
   under the corroborated wave indexing, **absolute waves ≈ 86 and ≈ 132**. Neither is overridden
   by any Crucible DLC pack, so both remain live for a full-DLC owner. **M** (refs) / **D** (absolute
   wave numbers). At wave 132 he is **paired with Viloth** in the same proxy.
3. **Shattered Realm: present in the data but almost certainly NOT reachable for Matt.** Primordian
   sits in `proxy_bossbaseeasy01` and `proxy_bossbasefull02` — the **base-game-content-scope** boss
   proxies. He appears in **zero** of the `proxy_bossall*` families (easy/medium/hard/veryhard, in
   both the gdx2 originals and the gdx3 overrides) — and `bossall*` is the family an
   expansion-owning account draws from. **M.** The base-vs-all *selection rule* lives in the world
   files, not the `.dbr` layer — that is this lane's boundary (§5, **U**).
4. **Campaign Ultimate is the big fight; Crucible is the *smaller* one.** The Crucible **overrides
   the boss life equation** to `((charLevel*25)^1.5)+100` against the campaign's
   `((charLevel*51)^1.53)+2400` — a **~3.7× smaller base pool** at level 108. Campaign-Ultimate
   Primordian is roughly **6–8× beefier than Crucible-Gladiator Primordian**, not weaker. **M** +
   **D**. This inverts the intuition embedded in Matt's question.

---

## 1. Record identity — exhaustive sweep (M)

Swept **all eight** `.arz` archives for `primordian` / `primorian` / `slith_wightmirecave01` /
`slithbossb02`, across both record paths **and** full string tables (catching field-value
references). Census, with provenance:

| archive | path | records | strings | sha256[:16] |
|---|---|---|---|---|
| base | `database/database.arz` | 34,114 | 82,688 | `8cdeff128422c765` |
| gdx1 | `gdx1/database/GDX1.arz` | 18,447 | 57,204 | `e28ab2515477ac80` |
| gdx2 | `gdx2/database/GDX2.arz` | 16,451 | 56,685 | `f6d5bd67602ce5af` |
| gdx3 | `gdx3/database/GDX3.arz` | 24,178 | 70,267 | `1661be5ef6db1f08` |
| **survivalmode (Crucible core)** | `mods/survivalmode/database/SurvivalMode.arz` | **3,147** | 13,773 | `e55b760f36ab80a6` |
| survivalmode1 | `survivalmode1/database/SurvivalMode1.arz` | 1,004 | 7,337 | `6df94d3be33e600c` |
| survivalmode2 | `survivalmode2/database/SurvivalMode2.arz` | 811 | 6,820 | `940e40344e9dde53` |
| survivalmode3 | `survivalmode3/database/SurvivalMode3.arz` | 1,431 | 11,099 | `b4aa2d78675c4f05` |

**Every hit, complete (M):**

| archive | record | rtype |
|---|---|---|
| base | `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` | `Monster` |
| base | `records/skills/nonplayerskills/bossskills/primordian_{arcticblast,flurry,frigidring,icearmor,passive,wave}.dbr` | skills (6) |
| gdx2 | `records/endlessdungeon/proxies/poolsboss/slith_primordian.dbr` | proxypool |
| **survivalmode** | **`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr`** | **`Monster` (override)** |
| **survivalmode** | **`records/proxies/poolsboss/slith_primordian.dbr`** | **proxypool** |

**gdx1 and gdx3 contain no Primordian data at all** — neither records nor string references. **M.**

> **Correction to the commission framing.** The commission calls Primordian "the Fangs of Asterkarn
> boss." He is not. His only creature record lives in the **base-game** `database.arz` at
> `boss&quest/slith_wightmirecave01.dbr` — the Wightmire Cave slith boss, Act 1 base content. gdx3
> (Fangs of Asterkarn) neither defines nor overrides him. Matt fought a base-game Act-1 boss while
> playing an all-DLC install. This matters for §3: his SR pool membership is *base-scope*, which is
> exactly what makes him unreachable there.

Display name bridge unchanged from the predecessor note: `description = tagSlithBossB02` →
**"Primordian, the Forgotten One"**; `FileDescription = "Primorian the Forgotten One"` (designer
typo in source, verbatim). `monsterClassification = Quest`. **M.**

---

## 2. Crucible — PRESENT, and Primordian is in it (M)

### 2a. Corpus coverage — the plain answer

**The Crucible IS in the corpus.** The commission anticipated it might be absent (Steam app 437830,
not among the fetched 219990 + 2699230). It is not absent: Crucible ships as a **mod**, and the
depot fetch pulled `mods/survivalmode/` along with three expansion packs (`survivalmode1/2/3`) and
their `Text_EN.arc` localisation archives. Nothing further needs fetching. **M.**

### 2b. The Crucible carries its own Primordian record

`mods/survivalmode/` **overrides** the monster record. Diff vs base — **33 differing fields of 968**
(**M**). The ones that matter:

| field | base (campaign) | survivalmode (Crucible) |
|---|---|---|
| `factions` | `faction_beast.dbr` | **`faction_aetherial.dbr`** |
| `distressCallGroup` / `Range` | `Slith` / 15.0 | **`Aetherial` / 50.0** |
| `dropItems` | True | **False** |
| `giveXP` | True | **False** |
| `onDie` | *(absent)* | **`gd.survival.rewards.bossKilled`** |
| `chanceToEquipMisc1/2/3` | 45 / 100 / 100 | **0 / 0 / 0** (all `lootMisc*` entries removed) |
| `skillName6` | `chillbane_blizzard` | **`passiveproperties_herodeflection`** |
| `skillName11` | *(absent)* | **`chillbane_blizzard`** (re-slotted, same `charLevel/4+1`) |
| `alertAnimChance` / `rallyAnimChance` | 100 / 100 | 0 / 0 |

**Unchanged across the override (M):** `charLevel = charLevel*1+3`, `minLevel/maxLevel = 1/250`,
`monsterClassification = Quest`, `experiencePoints = 800`, `controller = controller_boss_viloth`,
`characterAttributeEquations = bio_boss_standard_01`, all six `primordian_*` / boss skills, all
`defensive*` scalars, 8/8 attack/defence slots.

Two consequences worth stating plainly: **the Crucible Primordian drops nothing** (`dropItems =
False`, all equip-slots zeroed) — so the guaranteed Putrid Necklace from the campaign fight
(predecessor note §5) **does not exist in the Crucible**; rewards route through
`gd.survival.rewards.bossKilled` instead. And the `chanceToEquipMisc2 = 0` removal **eliminates the
stochastic ≈ +300-life gear term** that contaminated the campaign HP instrument — the Crucible
Primordian is a *cleaner* fixture than the campaign one. **M.**

### 2c. Where he spawns — full-corpus reverse-reference sweep (M)

Walked every record in every archive looking for field values citing the pool. Exhaustive result:

```
records/proxies/poolsboss/slith_primordian.dbr        [mods/survivalmode]
  spawnMin = spawnMax = 3 ; proxyPoolEquation = proxypoolequation_01
  name1 slith_wightmirecave01  alwaysSpawn1 True  limit1 1  levelVarianceEquation1 = lv7_uber hero
  name2 slitha_melee_b01       alwaysSpawn2 True  limit2 1  lv4_champion+
  name3 slitha_shaman_c01      alwaysSpawn3 True  limit3 1  lv4_champion+

REFERENCED BY — exactly two records, corpus-wide:
  records/proxies/tier09waves/proxy_w06_p02a.dbr   pool1 (weight1 100)          [proxytexture_orange]
  records/proxies/tier14waves/proxy_w02_p03a.dbr   pool2 (weight2 100)          [proxytexture_yellow]
                                                   pool1 = poolsboss/slith_viloth.dbr (weight1 100)
```

**The fixed trio carries over.** As in the campaign, Primordian never spawns alone — always with one
champion melee slith and one champion shaman slith (`alwaysSpawn`, `spawnMin = spawnMax = 3`). **M.**

**At tier14/w02 he is one of two equal-weight options** (`weight1 = weight2 = 100`) against
**Viloth** — so that spawn is a **50/50 coin-flip**, not a guarantee. **M.** The tier09/w06 proxy has
a single pool at weight 100 — **guaranteed** whenever that proxy fires. **M.**

### 2d. Tier → absolute wave (D, with strong corroboration)

`mods/survivalmode` defines **tier01…tier15**, each with exactly **10 waves** (`proxy_w01`…`proxy_w10`)
— **M**. The DLC packs extend the ladder: sm1 adds tier05–17, sm2 tier10–17, sm3 tier15–20. Union =
**tier01…tier20 = 200 waves**. **M.**

**The three Crucible balancing tables are arrays of exactly 200 entries** (§4). That the wave ladder
and the balance-array length agree at 200 is strong corroboration that **array index = absolute wave
number**, and therefore that tiers are sequential blocks of ten. Under that mapping:

| spawn record | tier | wave-in-tier | **absolute wave** |
|---|---|---|---|
| `tier09waves/proxy_w06_p02a.dbr` | 9 | 6 | **86** |
| `tier14waves/proxy_w02_p03a.dbr` | 14 | 2 | **132** |

**D** — the 10-per-tier block structure is measured; the *absolute* numbering is inferred from the
200/200 agreement. It is not read from a field that states it. Treat the wave numbers as ±1 tier
until someone confirms in-game.

### 2e. DLC-pack override check — Primordian survives (M)

A real reachability risk: the Crucible DLC packs *do* override tier records (sm1 touches tier09 and
tier14 directories). Checked directly. **None of `survivalmode1/2/3` overrides
`tier09waves/proxy_w06_p02a.dbr`, `tier14waves/proxy_w02_p03a.dbr`, `poolsboss/slith_primordian.dbr`,
or the monster record.** Neither do they reference Primordian anywhere. **Both spawn points remain
live on a full-DLC install.** **M.**

---

## 3. Shattered Realm — present in data, out of reach in practice

### 3a. The pool exists and is wired (M)

`gdx2 records/endlessdungeon/proxies/poolsboss/slith_primordian.dbr` — **field-for-field identical**
to the Crucible pool (same trio, same `lv7_uber hero` on Primordian, same limits and weights). **M.**

Referenced by **eight** SR boss proxies:
- `proxy_bossbaseeasy01_{01,02,03,04}` — as **pool33 of 35**, weight 100
- `proxy_bossbasefull02_{01,02,03,04}` — as **pool15 of 35**, weight 100

All 35 pools in both families carry `weight = 100`, so within a family Primordian is a **uniform
1-in-35** draw. **M.**

### 3b. …but only in the base-content families (M — this is the finding)

Membership swept across **every** SR boss-proxy family in gdx2 and gdx3:

| family (content scope) | variants | with Primordian |
|---|---|---|
| `proxy_bossbaseeasy01` | 4 | **4** |
| `proxy_bossbasefull02` | 4 | **4** |
| `proxy_bossbase{medium,hard}01`, `bossbasefull01` | 12 | 0 |
| `proxy_bossgdx1{easy,medium,hard,full}01` | 16 | 0 |
| `proxy_bossgdx2{easy,medium,hard,full}01` | 16 | 0 |
| `proxy_bossgdx3{easy,medium,hard,full}01` *(gdx3-added)* | 16 | 0 |
| **`proxy_bossall{easy,medium,hard,veryhard}01`** | **16** | **0** |
| `proxy_bossshatteredguardians*`, all `proxy_nemesis*` | 40+ | 0 |

gdx3 **overrides** the four `bossall*` families (growing them to 36/55/27/38 pools — folding in
Asterkarn bosses) and **adds** `bossgdx3*`. It does **not** override `bossbase*`, so the base
families keep gdx2's contents including Primordian. **M.**

**Reading:** the `base` / `gdx1` / `gdx2` / `gdx3` / `all` prefixes are content-ownership scopes. A
player who owns only the base game draws from `bossbase*`; a player who owns everything — Matt,
Edition II — draws from `bossall*`, which contains **no Primordian**. **This is why he has never
shown up in Matt's Shattered Realm runs, and why he will not.**

### 3c. The boundary — stated, not papered over (U)

I could not measure the selection rule. A full reverse-reference sweep of gdx2 and gdx3 found
**zero** `.dbr` records citing `proxy_bossbaseeasy01` or `proxy_bossbasefull02` by name. The
proxy-family → shard binding therefore lives in the **world/level layer** (`.lvl` inside the map
`.arc`s), which this lane does not parse. **U.**

So §3b's conclusion is: *membership* is measured and unambiguous; *selection* is inferred from the
naming scheme. Confidence high, but it is a scope-name inference, not a read field. Closing it
would require a `.lvl`/map-`.arc` parser — a new lane, roughly the cost of the original `.arz`
probe. My recommendation is **not** to build it for this question: the Crucible answer (§2) is fully
measured and is what Matt actually asked for.

---

## 4. Difficulty scaling — what an endgame re-fight actually looks like

### 4a. Campaign — the difficulty pak (M)

`records/game/balancingadjustment_mp+difficulty_enemies01.dbr` (`Class = AttributePak`). Arrays are
**12 entries = 3 difficulties × 4 player-counts**; single-player indices are **Normal 0, Elite 4,
Ultimate 8**. **M.**

| field | Normal 1P | Elite 1P | Ultimate 1P |
|---|---|---|---|
| `characterLifeModifier` | **+50** | **+320** | **+580** |
| `characterLifeMultModifier` | 0 | 0 | 0 |
| `offensiveTotalDamageModifier` | **−25** | **+25** | **+40** |
| `retaliationTotalDamageModifier` | −66 | −30 | **−15** |
| `characterOffensiveAbility` | 0 | +40 | +50 |
| `characterDefensiveAbility` | +35 | +60 | +75 |
| `characterAttackSpeedModifier` | −10 | 0 | 0 |
| `defensiveCold` / `defensiveFreeze` | 0 / 10 | 2 / 18 | 5 / 18 |

Note the **sign flip on `offensiveTotalDamageModifier`**: −25 on Normal, **+40 on Ultimate**. Across
the −25 → +40 swing plus the `armorbase05` rank climb (§4c), Primordian's damage regime changes
character completely, not just magnitude.

### 4b. Crucible — wave-indexed paks (M)

`records/game/survivalinfo.dbr` maps difficulty to table (**M**):

```
survivalAdjustmentNormal   -> balancingadjustment_survivalmode_enemies01.dbr   (Aspirant)
survivalAdjustmentElite    -> balancingadjustment_survivalmode_enemies02.dbr   (Challenger)
survivalAdjustmentUltimate -> balancingadjustment_survivalmode_enemies03.dbr   (Gladiator)
difficultyTimes            = [300, 600, 900]
```

Each is a **200-entry array indexed by wave**. Values at Primordian's two waves (**M**):

| field | diff | w1 | w50 | **w86** | **w132** | w150 | w200 |
|---|---|---|---|---|---|---|---|
| `characterLifeModifier` | Normal | 6 | 36 | **46** | **76** | 108 | 438 |
| | Elite | 70 | 80 | **104** | **174** | 218 | 612 |
| | **Ultimate** | 95 | 110 | **145** | **240** | 304 | **990** |
| `offensiveTotalDamageModifier` | all three | 5 | 10 | **18** | **32** | 42 | 130 |
| `characterOffensiveAbility` | Ultimate | 0 | 10 | **21** | **39** | 48 | 83 |
| `characterDefensiveAbility` | Ultimate | 0 | 12 | **26** | **49** | 60 | 95 |
| `characterAttackSpeedModifier` | Ultimate | 0 | 4 | **6** | **10** | 11 | 13 |
| `retaliationTotalDamageModifier` | Ultimate | 0 | 3 | **+14** | **+50** | 74 | 110 |

`characterLifeMultModifier` is **absent** from all three Crucible tables (**M**) — no multiplicative
life term in the Crucible, unlike the campaign pak where it exists but is 0 at 1P.

Note `offensiveTotalDamageModifier` is **identical across all three Crucible difficulties** — Crucible
difficulty buys enemy *survivability*, *accuracy* and *retaliation*, **not raw damage**. **M.**

### 4c. The Crucible rewrites the boss life equation — the load-bearing find (M)

`mods/survivalmode` **overrides `bio_boss_standard_01.dbr`**. Exactly **one** substantive field
differs (11 fields compared):

```
characterLife    base     = ((charLevel*51)^1.53)+2400
                 crucible = ((charLevel*25)^1.5)+100
```

Everything else — `characterMana`, str/dex/int, OA/DA, both regen equations — is **identical**. **M.**
At charLevel 108 that is **531,723 vs 140,396** base life: the Crucible boss starts from a pool
**~3.8× smaller**. The wave modifiers never make that back (§4d).

`survivalmode` does **not** override `lv6_hero`, `lv7_uber hero`, `armorbase05`,
`damagebase_physical04`, or `primordian_icearmor` — all inherit base. **M.**

**Level-scaled skill arrays at endgame ranks (M, `armorbase05`, 200-entry, rank = `charLevel*1`):**

| rank | `characterLifeModifier` | `offensiveTotalDamageModifier` | `defensiveProtection` (armor) |
|---|---|---|---|
| 13 *(Matt's fight)* | **−71** | **−78** | 76 |
| 17 | −71 | −74 | 105 |
| 100 | +57 | +25 | 1,607 |
| 105 | +94 | +25 | 1,728 |
| **108** | **+121** | **+25** | **1,805** |

This is the single largest scaling term and it is **wildly non-linear**: `characterLifeModifier`
swings **−71 % → +121 %** between rank 13 and 108, and armor climbs **76 → 1,805 (23.8×)**. The
predecessor note's §7.1 warning — that a few ranks of `armorbase05` move output enormously — applies
with far more force at endgame than it did at level 12.

`damagebase_physical04` (base attack, 210-entry, rank = charLevel): **101–128 @ r13 → 863–1,120 @
r108** — a **~8.6× raw base-attack climb** before any pak. **M.**

### 4d. Composed picture (D — bracketed, operator still HELD)

Per the predecessor note §7.2, the HP composition operator is **UNRESOLVED**: additive
(`life × (1 + Σmods/100)`) and multiplicative (`life × Π(1 + mod/100)`) both fit the single measured
campaign data point within ~1–2 %. I therefore report **both brackets** rather than pick one. All
figures at **player level 100, 1P**.

**Campaign** — `lv6_hero` gives spawn `(aPL+2)+(aPL/50)` … `(aPL+3)+(aPL/50)` = **104–105**, and
`charLevel = spawn+3` = **107–108**. Base life `((108*51)^1.53)+2400 = 531,723`.

| difficulty | `armorbase05` | pak | **life [additive]** | **life [multiplicative]** | net TDM | base atk |
|---|---|---|---|---|---|---|
| Normal | +121 % | +50 % | 1,440,969 | 1,762,662 | +24 % | 863–1,120 |
| Elite | +121 % | +320 % | 2,876,621 | 4,935,452 | +74 % | 863–1,120 |
| **Ultimate** | **+121 %** | **+580 %** | **4,259,101** | **7,990,732** | **+89 %** | **863–1,120** |

**Crucible** — `lv7_uber hero` gives spawn `(aPL+3)` … `(aPL+3)+(aPL/50)` = **103–105**, charLevel
**106–108**. Crucible base life at cl 108 = **140,396**.

| wave | difficulty | `armorbase05` | wave pak | **life [additive]** | **life [mult]** | wave TDM |
|---|---|---|---|---|---|---|
| ~86 | Aspirant | +121 % | +46 % | 374,858 | 453,002 | +18 % |
| ~86 | **Gladiator** | +121 % | +145 % | **513,850** | **760,175** | +18 % |
| ~132 | Aspirant | +121 % | +76 % | 416,976 | 546,085 | +32 % |
| ~132 | **Gladiator** | +121 % | **+240 %** | **647,226** | **1,054,936** | +32 % |

**Against Matt's measured fight.** The save's `greatestMonsterKilledLifeAndMana = 15,822` (campaign,
Normal, charLevel 13-or-17 unresolved). Endgame multiples:

- **Campaign Ultimate @ L100: ≈ 270×–505× the level-12 fight.**
- **Crucible Gladiator wave 132 @ L100: ≈ 41×–67×.**
- **Crucible Gladiator wave 86 @ L100: ≈ 32×–48×.**

**So the ranking is: campaign-Ultimate ≫ Crucible-Gladiator-w132 > Crucible-Gladiator-w86.** The
Crucible Primordian is roughly **6–8× less durable** than the campaign-Ultimate one, entirely
because of the `bio` life-equation swap in §4c. If the design question behind Matt's ask is *"where
do I get the hardest version of this fight?"*, the answer is **campaign Ultimate, not the Crucible.**

**All damage-side numbers remain under the §14.10 clamp hold** (predecessor §7.1). The `netTDM`
column is the additive sum `armorbase05 + damage_totaladjuster + pak`, reported raw; it must not be
composed into output damage until the champion/hero/boss clamp is measured. Note that at endgame the
sum is **positive** (+24 % to +89 %), well clear of the deep-negative band (−91 % to −95 %) that made
the level-12 figures so clamp-sensitive — so an endgame Primordian is, ironically, a **less
sensitive** damage fixture than the one Matt actually fought.

---

## 5. Availability verdict, by mode

| mode | Primordian re-fightable? | evidence grade | notes |
|---|---|---|---|
| **Campaign — Normal/Elite/Ultimate** | **YES** | **M** | Wightmire Cave, unchanged spawn chain (`proxy_wightmire_slitha01` → `p_wightmire_slitha01`, `lv6_hero`). `minLevel/maxLevel = 1/250`; no difficulty gate on the record. Full loot incl. the guaranteed necklace. |
| **Crucible — tier09 / wave ~86** | **YES, guaranteed on that spawn** | **M** | single pool at weight 100. |
| **Crucible — tier14 / wave ~132** | **YES, 50/50 vs Viloth** | **M** | two pools, equal weight 100. |
| **Crucible — all three difficulties** | **YES** (Aspirant/Challenger/Gladiator) | **M** | via `survivalinfo.dbr`; no DLC pack removes him. |
| **Shattered Realm** | **NO, in practice** | **M** membership / **U** selection | in `bossbase*` only; **zero** presence in the `bossall*` families an all-DLC account draws from. |
| **Nemesis / SR Guardians** | **NO** | **M** | absent from all 40+ nemesis and shattered-guardian proxies. |

**Practical answer to Matt's question:** *fight him in the Crucible at wave ~86 (tier 9, guaranteed)
or wave ~132 (tier 14, coin-flip against Viloth), on any of the three Crucible difficulties. He drops
nothing there — rewards come from the Crucible's own wave-reward system. If what you want is the
**hardest** Primordian, it is campaign Ultimate, which is 6–8× more durable than the Crucible
version.*

---

## 6. Records used (exact paths)

**Sweep + census:** all 8 `.arz` archives listed in §1.

**Creature:** `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` (base **and**
`mods/survivalmode` override) · `records/creatures/enemies/bios/bio_boss_standard_01.dbr` (base
**and** survivalmode override) · `records/creatures/enemies/{slitha_melee_b01, slitha_shaman_c01}.dbr`

**Crucible:** `mods/survivalmode/…/records/proxies/poolsboss/slith_primordian.dbr` ·
`records/proxies/tier09waves/proxy_w06_p02a.dbr` · `records/proxies/tier14waves/proxy_w02_p03a.dbr` ·
`records/proxies/poolsboss/slith_viloth.dbr` · `records/game/survivalinfo.dbr` ·
`records/game/balancingadjustment_survivalmode_enemies0{1,2,3}.dbr`

**Shattered Realm:** `gdx2 records/endlessdungeon/proxies/poolsboss/slith_primordian.dbr` ·
`gdx2 records/endlessdungeon/proxies/proxy_boss/proxy_bossbaseeasy01_{01..04}.dbr` ·
`gdx2 …/proxy_bossbasefull02_{01..04}.dbr` · full family sweep over 44 proxy families in gdx2 + 63
records in gdx3.

**Scaling:** `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` ·
`records/skills/nonplayerskills/passive/{armorbase05, damagebase_physical04, damage_totaladjuster,
resists_heroboss, passiveproperties_herodeflection}.dbr` ·
`records/proxies/{lv6_hero, lv7_uber hero, lv4_champion+, proxypoolequation_01}.dbr`

**Provenance.** Corpus root `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`; archive
SHA-256 prefixes in the §1 table (computed this session). Tooling:
`research/scripts/gd_arz_adapter_2026_07_24.py` (`ArzArchive`), driven by probes
`p1_sweep.py` … `p8_endgame.py` in `legolas/scratch/2026-07-28-primordian/`. Read-only throughout;
nothing written to the vendor tree.

---

## 7. Confidence and what is held

### High confidence (MEASURED)
Corpus coverage of the Crucible. Exhaustive record identity (§1) — path **and** string-table sweep
across all 8 archives, so the "no gdx1/gdx3 Primordian" claim is a true negative, not a miss. The
Crucible monster override and its 33-field diff. Both Crucible spawn references (exhaustive
reverse-reference walk over every record in every archive). The DLC-pack non-override check. SR pool
membership and the `bossall*` exclusion. All balancing-table values. The `bio` life-equation swap.

### DERIVED (arithmetic shown)
The tier → absolute-wave mapping (§2d) — block structure is M, absolute numbering is inferred from
the 200-wave / 200-entry agreement. Every composed life figure in §4d, reported as a **bracket**
across the two candidate operators, never as a single number.

### HELD / UNRESOLVED
1. **HP composition operator** — still held from the predecessor note §7.2. §4d brackets it. The
   Crucible Primordian (`chanceToEquipMisc* = 0`, no gear noise) is a **materially better closure
   fixture** than the campaign one; this is a new and cheap option for that open question.
2. **Champion/hero/boss damage clamp** — held per §14.10. Damage columns in §4 are raw.
3. **SR base-vs-all selection rule** (§3c) — lives in the world/`.lvl` layer this lane does not
   parse. **U.** The §3b conclusion rests on scope-name inference.
4. **Campaign region level bands.** Whether Wightmire Cave's `averagePlayerLevel` on Ultimate
   actually reaches ~100 is set in the world layer, not the `.dbr` layer. The creature imposes no
   clamp (`minLevel/maxLevel = 1/250`, **M**) and `lv6_hero` is purely `averagePlayerLevel`-driven
   (**M**), so §4d's L100 figures are an **upper** reading. If GD caps Act-1 monster level on
   Ultimate, campaign-Ultimate Primordian is weaker than tabled — but the §0.4 ranking against the
   Crucible would need a cap below ~charLevel 78 to invert, which is a large cap.
5. **Which level the save's `13` denotes** (charLevel vs spawn) — unchanged from predecessor §7.3,
   and it propagates into the "270×–505×" multiple in §4d.

---

*Downstream: gandalf (commissioner) — §0 and §5 are the answer to Matt; §1's framing correction
(Primordian is base-game, not Asterkarn) is charter-level; §4c's Crucible life-equation swap inverts
the difficulty intuition and may bear on KIT-CAL-1 fixture selection; §7.1 offers a cleaner HP-closure
fixture than the campaign fight. No canonical doc amended by this note.*
