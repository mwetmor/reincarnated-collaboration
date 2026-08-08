# KC2-SIM — group-assignment micro-probe: the eHP chain, rebuilt and closed EXACTLY (8/8)

**Agent:** legolas (UNKNOWN-RESEARCHER)
**Conductor:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, Phase C → G-D
**Commission:** targeted micro-probe extending HALT-10 after galadriel's wave-160 board closure falsified the record→form map
**Extends / AMENDS:** `legolas/notes/2026-08-08-kc2-ehp-composition-probe.md` (HALT-10; adopted at ledger L-29)
**Consumes:** `galadriel/notes/2026-08-08-kc2-board-closure.md` §§ 1, 3, 4 (30 Hz census + nameplate levels)
**Disposition:** **CLOSED-DB-CITED for Q1 · Q2 · Q3 · Q4 · Q6 · PARTIAL for Q5** (mechanism cited, one +3 offset NAMED-ABSENT)
**Commit:** NONE (charter § 4.7 — conductor commits at gate close)
**Scratch:** `legolas/scratch/2026-08-08-kc2-ehp-composition/`
**Emission:** `legolas/scratch/2026-08-08-kc2-ehp-composition/t21_wave160_board_ehp_r2.csv` (39 rows, 33 cols)
**External fetches:** ZERO. Everything below is corpus-resident.

---

## 0 — Corpus provenance (re-verified against my own prior pin, byte-for-byte)

| Archive | md5 | bytes | vs HALT-10 pin |
|---|---|---:|---|
| `database/database.arz` | `20d47784be5f93124636992f9e5562e2` | 58,338,379 | **IDENTICAL** |
| `gdx3/database/GDX3.arz` | `08365db74863744fea2cfc7254666f55` | 47,334,429 | **IDENTICAL** |
| `mods/survivalmode/database/SurvivalMode.arz` | `ac4ad3539196ccf26b6f8be6ab7d3a8b` | 7,052,806 | **IDENTICAL** |

**`templates.arc` gap: unchanged and re-disclosed.** The Edition-II pin ships no `.arc` under `database/`;
template citations come from the Edition-I dump at `scratch/2026-08-08-kc2-halt-bundle/tpl/` and are graded
**TPL-CITED**. Every numeric value below is Edition-II `.arz`.

**NEW this pass — `resources/Text_EN.arc` IS Edition-II-native** (base + gdx1/2/3 + all four survival archives).
20,394 tag keys banked; every monster name in this note is DB-CITED from the pinned tree, not from memory.

---

## 1 — HEADLINE

**The chain closes EXACTLY — 8 bodies, 6 bio curves, 3 armorbase arrays, 3 levels, ZERO residual on every one.**

```
eHP = floor( characterLife(bio, L) × M )
M   = 1 + 5.80 + G/100 + armorbaseNN[L−1]/100
G   = balancingadjustment_survivalmode_enemies03.characterLifeModifier[159] = 324
L   = the monster's level — the SAME quantity the nameplate displays
```

| body (camera-named) | record | L | bio curve | armorbase | M | predicted | measured | resid |
|---|---|---:|---|---|---:|---:|---:|---:|
| Zantarin, the Immortal | `nemesis_orderdeathsvigil_01` | 109 | `((L*42)^1.5)+20000` | 05 → 125 | 11.29 | **3,722,896** | 3,722,896 | **0** |
| Archmage Aleksander | `nemesis_aetherialvanguard_01` | 109 | `((L*42)^1.5)+20000` | 05 → 125 | 11.29 | **3,722,896** | 3,722,896 | **0** |
| Kubacabra, the Endless Menace | `nemesis_beast_01_p1` | 109 | `((L*36)^1.5)+16000` | 05 → 125 | 11.29 | **2,955,796** | 2,955,796 | **0** |
| Galakros, the Mountain | `aetherialcolossus_galakros` | 106 | `((L*33)^1.5)+500` | 05 → 103 | 11.07 | **2,295,755** | 2,295,755 | **0** |
| Aetherial Bileeater | `aetherialbloater_b01_summon` | 112 | `((L*27)^1.33)+150` | 04 → 129 | 11.33 | **484,095** | 484,095 | **0** |
| Death Revenant | `..._01_revenantsummon` | 109 | `((L*11)^1.50)−20` | 05 → 125 | 11.29 | **468,504** | 468,504 | **0** |
| Aleksander's Shard | `aetherialvanguard_crystal` | 109 | `((L*4)^1.5)+100` | 04 → 125 | 11.29 | **103,912** | 103,912 | **0** |
| Skeletal Archer | `skeleton_a02_summon` | 109 | `((L*5.6)^1.28)+24` | 01 → 110 | 11.14 | **41,237** | 41,237 | **0** |

**This is not a fit.** Every term is DB-cited; the only levels used are galadriel's camera nameplate reads.
The falsification test (§ 7) scans **200 Gladiator cells × 81 integer levels = 16,200 candidate pairs per body**
and returns **exactly one** solution each — and it is the camera's. Zero free parameters, zero residual,
unique solution.

**Three of my HALT-10 links were wrong and are struck** (§ 8). The largest: I *excluded* the `armorbase`
passive as a "trap". It is a **required term**. My exclusion test was run at a level that was itself wrong.

---

## 2 — Q1 · POOL-SLOT ENUMERATION — **CLOSED-DB-CITED**

### 2.1 The wave-160 spawn points, re-derived from the wave record (not from the P-E6 emission)

`records/proxies/tier16waves/proxy_w10_p{01,02,03,04,06}a.dbr` — **5 spawn points**, winner `[sm3]`.
(Tier 16 = waves 151–160; w10 = wave 160.) The proxies carry **no** `levelVarianceEquation` of their own —
they carry only `pool{i}` + `weight{i}`. This confirms the HALT-10 pool set exactly.

| spawn point | pool | weights |
|---|---|---|
| `proxy_w10_p01a` | `poolsboss/nemesis_all` | 100 |
| `proxy_w10_p02a` | `poolsbossgdx1/nemesis_all_noaetherialvanguard` | 100 |
| `proxy_w10_p03a` | `poolsbossgdx1/nemesis_wendigooraetherialvanguard` | 100 |
| `proxy_w10_p04a` | `poolsbossgdx1/aetherialcolossus_galakros` **·** `poolsbossgdx2/korvaaktombguardian` | 100 / 100 |
| `proxy_w10_p06a` | `poolsherogdx1/wendigocannibal_hero` | 100 |

### 2.2 Every pool slot → its ACTUAL record and DB-cited display name

Names resolved from `Text_EN.arc` (`tags_creatures.txt` / `tagsgdx{1,2,3}_creatures.txt`). All pools resolve
to `[sm3]` as overlay winner; all nemesis slots carry `levelVarianceEquation{i} = records/proxies/lv8_boss+.dbr`.

| slot | record | tag | **display name** | class | `charLevel` field | own `characterLifeModifier` |
|---|---|---|---|---|---|---:|
| p01.1 | `nemesis_aetherial_01` | `tagNemesis_Aetherial01` | **Valdaran, the Storm Scourge** | Boss | `charLevel*1+2` | 0 |
| p01.2 | `nemesis_chthonian_02` | `tagNemesis_Chthonian02` | **Benn'Jahr, the Colossal** | Boss | `(charLevel*1.1)+2` | 0 |
| p01.3 | `nemesis_orderdeathsvigil_01` | `tagNemesis_OrderDeathsVigil01` | **Zantarin, the Immortal** ← **on camera** | Boss | `charLevel*1` | 0 |
| p01.4 | `nemesis_outlaw_01` | `tagNemesis_Outlaw01` | **Fabius "the Unseen" Gonzar** | Boss | `charLevel*1` | 0 |
| p01.5 | `nemesis_undead_02b` | `tagNemesis_Undead02` | **Moosilauke, the Chillwind** | Boss | `(charLevel*1)` | — |
| p01.6 | `nemesis_kymon_02` | `tagNemesis_Kymon02` | **The Iron Maiden** | Boss | `charLevel*1` | 0 |
| p01.7 | `nemesis_undead_01` | `tagGDX3Nemesis_Undead02` | **Raddoth, Lord Hierophant** | Boss | `(charLevel*1.1)+2` | **100** |
| p01.8 | `nemesis_kymon_01` | `tagGDX3Nemesis_Zealot02` | **Curate Ignus** | Boss | `(charLevel*1.1)+2` | 0 |
| p01.9 | `nemesis_orderdeathsvigil_02` | `tagGDX3Nemesis_Necro02` | **Shriek** | Boss | `(charLevel*1.1)+2` | 0 |
| p01.10 | `nemesis_outlaw_02` | `tagGDX3Nemesis_Outlaw02` | **Vinn "the Giant" Ozmald** | Boss | `(charLevel*1.1)+2` | 0 |
| p02.1 | `nemesis_beast_01_p1` | `tagGDX1Nemesis_Beast01` | **Kubacabra, the Endless Menace** ← **on camera** | Boss | `(charLevel*1.1)+2` | 0 |
| p02.2 | `nemesis_chthonianvoidborn_01` | `tagGDX1Nemesis_Chthonian01` | **Grava'Thul, the Voiddrinker** | Boss | `(charLevel*1.1)+2` | 0 |
| p02.3 | `nemesis_wendigo_01` | `tagGDX1Nemesis_Wendigo01` | **Reaper of the Lost** | Boss | `(charLevel*1.1)+2` | 0 |
| p02.4 | `nemesis_beast_02` | `tagGDX3Nemesis_Beast02` | **The Underking** | Boss | `(charLevel*1.1)+2` | — |
| p02.5 | `nemesis_wendigo_02` | `tagGDX3Nemesis_Wendigo02` | **Reaper of Rot** | Boss | `(charLevel*1.1)+2` | 0 |
| p03.1 | `nemesis_aetherialvanguard_01` | `tagGDX1Nemesis_Aetherial01` | **Archmage Aleksander** ← **on camera** | Boss | `charLevel*1+5` | 0 |
| p03.2 | `nemesis_wendigo_01` | `tagGDX1Nemesis_Wendigo01` | Reaper of the Lost *(dup of p02.3)* | Boss | `(charLevel*1.1)+2` | 0 |
| p04a.1 | `aetherialcolossus_galakros` | `tagGDX1MiniBoss_Aetherial02` | **Galakros, the Mountain** ← **on camera** | Quest | `charLevel*1+5` | 0 |
| p04b.1 | `statue_korvaaktombguardian` | `tagGDX2Boss_TombGuardian_01` | **The Steward** | Quest | `charLevel*1` | — |
| p06.C1–C5 | `wendigocannibal_h01…h05` | `tagGDX{1,3}HeroWendigoCannibal_*` | **Ulda Emberclaw · Haldra the Bloodlust · Palros, Protector of the Pack · Allcadius the Unburied · Gaddo Evergrown** | Hero | `(charLevel*1)+2` | 0 |

**16 distinct nemesis records** (Reaper of the Lost appears in both p02 and p03). **15 of 16 carry
`bio_boss_nemesis_01`**; Kubacabra alone carries `bio_boss_nemesis3phase_01`.

### 2.3 The commission's direct question — variant records for Zantarin and Aleksander?

**NO. NAMED-ABSENT, with the search enumerated.**

- Corpus-wide path search for `zantarin` returns **16 records — all skills and item-pet bonuses, zero creature
  records.** GD keys nemesis creature records by *faction*, never by proper name. Zantarin is
  `nemesis_orderdeathsvigil_01` and there is exactly one of it in the live tree.
- `aleksander` and `kubacabra` return **0 paths** for the same reason.
- No `_02` / Crucible-specific / overlay-added variant of either record exists. Zantarin's owner chain is
  `base → gdx1 → gdx2 → sm_mod` (winner `sm_mod`); Aleksander's is `gdx1 → gdx2 → sm1` (winner `sm1`). Both
  winners carry `charLevel` values (`charLevel*1` and `charLevel*1+5`) that are **NOT** the ×1.1 form.

**So the ×1.1 group cannot be reached by any record substitution — and it does not need to be. The record
`charLevel` equation is not in the chain at all** (§ 3.1). Zantarin, Aleksander and Kubacabra carry three
*different* `charLevel` equations and all three run at level **109**.

### 2.4 The dedupe fact, now explained by citation

galadriel measured exactly two simultaneous bodies at 3,722,896 across 73 frames. Under the corrected chain
**all 15 `bio_boss_nemesis_01` nemeses have byte-identical eHP at wave 160 — 3,722,896 to the unit.** A
fingerprint collision between any two non-Kubacabra nemesis draws is therefore **certain, not a 0.20 coincidence**
(my HALT-10 § 4.3 estimate is struck). The board drew Zantarin (p01) + Kubacabra (p02, the one exception) +
Aleksander (p03) — the only 3-draw pattern that yields exactly two colliding nemesis fingerprints and one
distinct one, which is precisely what the camera saw.

---

## 3 — Q2 · THE EXACT CARRIER FOR 3,722,896 — **CLOSED-DB-CITED**

### 3.1 First: the record `charLevel` equation is NOT a chain link. The template says so.

`character.tpl` → `charLevel`, `type = "equation"`, description **verbatim**:

> *"Equation used to determine level if this character is placed in the world **manually**."*

Crucible bodies are **not** placed manually. They are proxy-spawned:
`game__events__survivalevent.lua` L548, verbatim —
`waveEvent.proxy[id] = Proxy.Create(waveEvent.waves[id][waveEvent.waveIndex][randomizer], waveEvent.coords[id].origin, true)`
— **three arguments, no level.** The level therefore comes from the proxy pool's `levelVarianceEquation`
and nothing else. My HALT-10 "stage 2" was reading a field that the template scopes out of this path.

**Independent confirmation from the data:** three nemeses with three different `charLevel` equations
(`*1`, `*1+5`, `*1.1+2`) all run at **109**.

### 3.2 The 118.6 result was a degeneracy artifact — and here is the audit that shows it

HALT-10's headline evidence was that `bio_boss_nemesis_01` and `bio_boss_nemesis3phase_01` back-solve the same
`M` to 0.006%. **That agreement is nearly automatic.** The two curves are near-proportional
(coefficients 42/36, constants 20000/16000 — and `20000/16000 = 1.250` sits close to `(42/36)^1.5 = 1.2601`),
so their ratio is almost level-independent:

| L | 106 | 109 | 118.6 | 130 | 150 |
|---|---|---|---|---|---|
| `nem/kub` ratio | 1.2594993 | 1.2595241 | 1.2595938 | 1.2596612 | 1.2597509 |

The whole range L ∈ [106, 150] spans **0.018%** of ratio. Any L in that band finds an `M` that "agrees"
across the two curves; the DB then offers a 200-cell Gladiator menu dense enough that *some* cell will look
like a hit. **That is the trap I fell into.** Struck as evidence.

**What the ratio-solve actually returns when run properly:** bisecting
`nem(L)/kub(L) = 3,722,896 / 2,955,796` gives **L\* = 108.9894** — i.e. **109**, the camera's number — and at
exactly L = 109 the two-curve `M` spread is **0.0000%** (11.289998 vs 11.289999), the minimum over the entire scan.

### 3.3 The missing term: `armorbaseNN.characterLifeModifier`

Every wave-160 monster runs an `armorbase` passive at `skillLevel = charLevel*1`, and those records carry a
200-cell `characterLifeModifier`. **Array index = skill level − 1** (1-based skill level → 0-based array),
determined from two independent bodies and then confirmed by six more:

| record | idx 105 | idx 108 | idx 111 | carried by |
|---|---:|---:|---:|---|
| `armorbase01` | 88 | **110** | 114 | Skeletal Archer (Common) |
| `armorbase04` | 103 | **125** | **129** | Aleksander's Shard, Aetherial Bileeater |
| `armorbase05` | **103** | **125** | 129 | all nemeses, Galakros, Death Revenant |

`armorbase01`/`02` are one array; `03`/`04`/`05` are another. All `[base]`, no overlay.

The three "deviating" bodies in the joint solve are explained to the cent by this term alone:

| | L | armorbase | `M` | Δ vs nemesis |
|---|---:|---:|---:|---:|
| nemeses / Death Revenant / Shard | 109 | 125 | 11.29 | — |
| **Galakros** | 106 | 103 | **11.07** | −0.22 = −22/100 ✓ |
| **Skeletal Archer** | 109 | 110 (`armorbase01`) | **11.14** | −0.15 = −15/100 ✓ |
| **Aetherial Bileeater** | 112 | 129 | **11.33** | +0.04 = +4/100 ✓ |

### 3.4 The per-record `characterLifeModifier` is NOT applied — falsified on camera

`aetherialbloater_b01_summon` carries `characterLifeModifier = 50.0`. Including it as `+0.50` on `M`
gives **505,458 vs a measured 484,095 = +4.41%**. Excluding it gives **484,095 = EXACT**.

**Consequence: Raddoth's `+100` is not applied either.** My HALT-10 row "Raddoth = 4,102,036" is struck;
Raddoth's eHP at wave 160 is **3,722,896**, identical to every other `bio_boss_nemesis_01` nemesis.
*(Single-witness rule — Bileeater is the only body on the filmed board that carries a non-zero own modifier
and was measured. Graded DB-CITED-FALSIFIED, and flagged as resting on one witness.)*

### 3.5 The rounding step the commission predicted: **`floor`**

`base × M` lands on `3722896.5636` · `2955796.2481` · `2295755.6626` · `484095.4871` · `468504.1634` ·
`103912.5647` · `41237.9089`. **`floor` succeeds on all eight bodies; `round` misses four of the seven
distinct values (five of the eight bodies) — Zantarin, Aleksander, Galakros, Shard, Archer.**

The −147 residual the commission asked me to chase (`3,723,043` vs `3,722,896`) does not exist under the
corrected chain, and it was never a truncation artifact: it was the ~4-parts-in-100,000 leftover of the two
~12% errors in § 9.1 failing to cancel *perfectly*. Under the corrected chain the residual is exactly **0**.

### 3.6 The Gladiator array index is INVERTED relative to the § 10.7 law

| G source | value | 8-body result |
|---|---:|---|
| `characterLifeModifier[158]` (§ 10.7 law: fighting 160 reads row 159) | 322 | **0/8 exact — all −0.177%** |
| `characterLifeModifier[159]` (the cell **labeled 160** under U-8's `wave = index+1`) | **324** | **8/8 EXACT** |

**Fighting wave *w* reads 0-based index *w*−1 — the cell LABELED *w*.** The "completed-waves" reading I
recommended at HALT-10 § 8.3, and which the spec adopted (§ 6.2b: *"the sim consumes the `glad_cell = 322`
rows"*), is **falsified**. **This is cross-cutting**: every 200-cell array in
`balancingadjustment_survivalmode_enemies03` is indexed the same way, so
`offensiveTotalDamageModifier` at wave 160 is **+43** (index 159), not +41.

---

## 4 — Q3 · HERO AUDIT — **CLOSED-DB-CITED, and the premise was wrong**

**None of the four small fingerprints is a p06 hero. All four are SUMMONS**, and the DB predicts their
camera multiplicities.

| fingerprint | bodies on camera | summoner + skill | `spawnObjects` | `petBurstSpawn` / `petLimit` |
|---:|---:|---|---|---|
| **41,237** | **3** | Zantarin `skill13 zantarin_reactivesummonskeletalarcher` (`Skill_SpawnPetMonster`) | `faction/skeleton_a02_summon.dbr` → `tagEnemySkeletonA02` = **"Skeletal Archer"** | 2 / 12 |
| **468,504** | 1 | Zantarin `skill6 zantarin_summonrevenant` | `nemesis_orderdeathsvigil_01_revenantsummon.dbr` → `tagEnemySkeletonC04` = **"Death Revenant"** | 1 / 3 |
| **103,912** | **2** | Aleksander `skill9 aetherialvanguard_summonshard` | `aetherialvanguard_crystal.dbr` → `tagGDX1Nemesis_Aetherial01_Crystal` = **"Aleksander's Shard"** | **2** / 6 |
| **484,095** | 1 | Galakros `skill12 galakros_summonbloater_secondary` (`Skill_TargetedSpawnPet`) | `aetherialbloater_b01_summon.dbr` → `tagGDX1EnemyAetherialBloater_B01` = **"Aetherial Bileeater"** | 1 / 3 |

Every one of these was re-verified under **winner-only** overlay semantics (§ 6), so the wiring is the
engine's, not an artifact of a field merge. The exact-carrier arithmetic is § 1's table — all four EXACT.

**Two honest caveats.**

1. **`aetherialbloater_b01.dbr` (non-summon) also exists** in `[gdx1, gdx3, sm1]` with *identical* bio,
   `charLevel`, classification, `armorbase` and own-modifier. The eHP conclusion is invariant to which of the
   two the camera saw; the *provenance* claim ("Galakros's pet") rests on the summon wiring plus the fact
   that no wave-160 pool spawns a bloater.
2. **`galakros_summonbloater_secondary` has a second output**, `aetherialbloater_c01_summon`
   ("Aetherial Regurgitator", `((L*31)^1.33)+150`, weight 30 at skill rank ≥17 vs 70 for b01). At L=112 it
   predicts **581,396**. Not seen on camera; carried in the CSV as an uncorroborated prediction.

**Corollary — the p06 hero band is also corrected.** The wendigo-cannibal heroes are `bio_hero_standard_01`
at L 107–108 → **450,012 – 460,431**, not the 398,747–405,213 I quoted at HALT-10. No p06 body was ever
engaged on camera (galadriel § 2's declared residual limit covers it).

---

## 5 — Q4 · KUBACABRA PHASE WIRING — **CLOSED-DB-CITED. The Crucible's Kubacabra is SINGLE-PHASE.**

The phase chain is not an HP-bar refill. It is a **death-spawn**:

- `[gdx1] nemesis_beast_01_p1.dbr` carries
  `poolToSpawnOnDeath = records/proxies/poolsdeathspawngdx1/dp_nemesisbeastp01.dbr` and
  `chanceToSpawnOnDeath = 100.0` and `waitForCallbackToSpawn = False`.
- That pool (`spawnondeathpool.tpl`, `spawnMin = spawnMax = 2`, `alwaysSpawn1/2 = True`) spawns
  `nemesis_beast_01_p2a` **and** `_p2b` — "Kubacabra, the Enduring".
- A corpus-wide reference sweep finds **exactly one** referrer of that pool: the `gdx1` P1 record.

**And the survival overlay deletes it.** `[sm1]`'s `nemesis_beast_01_p1.dbr` has **994 fields** to gdx1's
**995**, and the three it drops are `chanceToSpawnOnDeath`, `poolToSpawnOnDeath`, `mapNuggetType`. Because
`.arz` overlay is **whole-record replacement** (§ 6), the sm1 record simply has no death-spawn wiring.

This is a *pattern*, not an accident: Zantarin's `[sm_mod]` record likewise drops `skillName15`/`skillLevel15`
(`chestnemesis_01`, the nemesis loot chest) and all `lootMisc*` entries; Galakros's `[sm1]` record drops ten
`lootMisc*` fields. **The Crucible strips campaign-only mechanics — loot chests, map nuggets, and phase chains.**

**Camera agreement is total** (galadriel § 5): the bar runs to 9.1% and vanishes, the kill counter steps, the
denominator never moves, and zero hits for `1,162` / `636,6` across all 4,401 raw OCR strings.

**Sim disposition — CONFIRMED as the conductor proposed, and now DB-CITED rather than declared:** single body,
eHP **2,955,796**, no P2/P3. The HALT-10 instruction *"Kubacabra is 3-phase … the sim needs all three"*
(and spec § 6.2b's restatement) is **struck**. The P2/P3 rows survive in the CSV marked
`phase-UNWIRED-in-crucible` with their campaign values, so a future campaign-side consumer is not left
without them — but they must **not** be summed into a Crucible board.

---

## 6 — METHODOLOGICAL CORRIGENDUM: `.arz` overlay is WHOLE-RECORD REPLACEMENT

HALT-10 § 0 said reads went through the eight-archive stack "last-wins", and implemented that as a
**field-level merge**. That is the wrong engine model.

**Measured:** every archive ships a *complete* record.

| record | per-archive field counts |
|---|---|
| `nemesis_beast_01_p1` | gdx1 **995** → sm1 **994** (drops 3, adds 2) |
| `nemesis_orderdeathsvigil_01` | base 1004 → gdx1 1003 → gdx2 1006 → sm_mod **999** (drops 8) |
| `aetherialcolossus_galakros` | gdx1 998 → sm1 **991** (drops 10) |

A field merge **resurrects fields a later archive deliberately deleted** — which is exactly how Kubacabra's
phase chain would have survived into a Crucible model that has no such thing.

**Blast radius, checked and bounded:** across the eight measured bodies, winner-only and field-merge differ on
**exactly one field** — Kubacabra's `poolToSpawnOnDeath`. Every `characterAttributeEquations`, `charLevel`,
`characterLifeModifier`, `skillName2/3` and `skillLevel2/3` is identical. **All numeric conclusions in HALT-10
and in this note stand under the corrected model.** Everything in this note was re-run winner-only.

---

## 7 — FALSIFICATION TEST (the reason this is citation, not fitting)

Charter § 4.2 forbids tuning a value to a measured target. The test below is exact-match enumeration over a
DB-defined finite space, run *after* the model was fixed, with nothing free.

**Test A — per-body level uniqueness.** Hold `M = 10.04 + armorbase[L−1]/100` and scan **every integer
L ∈ [80, 160]**. Ask: which L produce `floor(base × M)` *exactly equal* to the measured integer?

| body | camera L | exact-matching L in [80,160] |
|---|---:|---|
| Zantarin · Aleksander | 109 | **[109]** |
| Kubacabra P1 | 109 | **[109]** |
| Galakros | 106 | **[106]** |
| Aetherial Bileeater | 112 | **[112]** |
| Death Revenant | 109 | **[109]** |
| Aleksander's Shard | 109 | **[109]** |
| Skeletal Archer | 109 | **[109]** |

**8/8 unique, 8/8 equal to the camera's independent nameplate read.**

**Test B — joint (G, L) uniqueness.** Free `G` across **all 200 Gladiator cells** *and* L across [80,160]
— 16,200 candidate pairs:

- Zantarin: **1** exact solution — `(index 159, G = 324, L = 109)`
- Galakros: **1** exact solution — `(index 159, G = 324, L = 106)`

The array index and the level are *jointly* pinned by the arithmetic, and they agree with the camera and with
U-8's labeling convention. Two instruments, one answer.

---

## 8 — Q5 · WHAT FEEDS THE DISPLAYED LEVEL — **PARTIAL**

### 8.1 CLOSED: displayed level **is** the HP-equation level

The commission asked whether the nameplate might be showing spawn-level or `levelRequirement` rather than the
HP-equation input, which would "dissolve an apparent contradiction." **It dissolves it in the stronger
direction: they are the same quantity.** Substituting the nameplate numbers into `characterLife` yields
exact integer agreement on 8/8 bodies with unique solutions (§ 7). There is no contradiction left to dissolve —
the 118.6 that created it was mine, and it is struck.

`levelRequirement` is absent from all four large-body records. The DB field that produces the level is the
proxy pool's `levelVarianceEquation{i}` → `records/proxies/lv*.dbr` → `min/maxVarianceEquationNormal`.

### 8.2 NAMED-ABSENT: a uniform **+3** offset between the proxy band and the measured level

| proxy | equation | band at apl = 100 | **measured** | offset |
|---|---|---|---:|---:|
| `lv8_boss+` (all nemeses) | min = max = `(apl+4)+(apl/50)` | **106** (a point) | **109** | **+3** |
| `lv7_uber hero` (p04) | min `(apl+3)`, max `(apl+3)+(apl/50)` | **103 – 105** | **106** | **+3 on the min** |
| `lv6_hero` (p06) | min `(apl+2)+(apl/50)`, max `(apl+3)+(apl/50)` | 104 – 105 | *(not engaged)* | assumed +3 |

Two proxies, two independent camera bodies, the same **+3**.

**Two observationally-equivalent readings, not discriminable from a single wave:**
(a) a +3 offset applied to the variance band; (b) `averagePlayerLevel` evaluating to **103** rather than 100
— at apl = 103, `lv8_boss+` = 107 + 2 = **109** and `lv7_uber hero` = **106 – 108** (Galakros at band min).
Both reproduce both measurements exactly. **A second wave with a nameplate read would separate them** —
under (a) the offset is constant, under (b) it is not necessarily.

**The search that produced the absence** (so a later probe does not redo it):

- **32** level-variance records corpus-wide; **0** carried by *any* survivalmode archive; **0** populate
  `min/maxVarianceEquationEpic|Legendary`; **0** reference `gameDifficulty` (which
  `proxylevelvarianceequation.tpl` *does* declare as an available equation variable — "Proxy (0 to n)").
- `proxypool.tpl`: no level-offset field. Only `levelVarianceEquation{i}` and the `min/maxPlayerLevel{i}` gates.
- `balancingadjustment_survivalmode_enemies03.dbr` — all **627** fields read: **no level field of any kind.**
- `gameengine.dbr` — `owners = ['base']` only; `monsterAttributePak` → the Ultimate pack; no level term.
- The survival Lua sets no monster level. `Game.GetAveragePlayerLevel()` appears three times: trap level,
  defense level, XP penalty. `Proxy.Create(dbr, origin, true)` takes no level argument.
- `records/creatures/pc/playerlevels.dbr` `maxPlayerLevel = 100` `[gdx2]` — the cap is 100, and the fixture
  is a Level 100 Warlord (ceremony § D), so apl = 103 cannot come from the character sheet.

**Verdict: the +3 is MEASURED and its DB source is NAMED-ABSENT.** I am not inventing a mechanism for it.
For the sim it is a stated input, not a derived one.

### 8.3 Summon levels: MEASURED per body, general rule NAMED-ABSENT

Zantarin's two pets and Aleksander's shard all run at **their summoner's level (109)**; Galakros's bloater runs
at **112 = summoner + 6**. No summon skill on the board carries a `petLevel` field (only `petLimit`,
`petBurstSpawn`, `skillMaxLevel`, `spawnObjectWeights`). The pets' own `charLevel` equations do not reproduce
any of the four measurements from any plausible input. **One suggestive coincidence, recorded and NOT claimed:**
the Bileeater's `charLevel` equation `(charLevel*1.1)+2` evaluated at `averagePlayerLevel = 100` gives
**exactly 112** — but the same construction fails on all three other summons, so it is a coincidence until a
second bloater measurement says otherwise.

---

## 9 — Q6 · THE CORRECTED CSV

**`legolas/scratch/2026-08-08-kc2-ehp-composition/t21_wave160_board_ehp_r2.csv`** — 39 rows × 33 columns,
winner-only overlay semantics throughout.

Columns: `body · name_tag · record · winner_archive · pool_slot · spawn_source · monster_class · proxy ·
proxy_lv_min/max · level_offset_vs_proxy · charLevel · charLevel_grade · bio_record · bio_archive ·
life_equation · armorbase_record · armorbase_skill_level_eq · armorbase_index · armorbase_pct · ultimate_pct ·
gladiator_index · gladiator_pct · own_characterLifeModifier · own_applied · M · base_life · eHP ·
**measured · residual_abs · residual_pct · verdict** · note`.

Row classes: **8 `EXACT`** (camera-corroborated, `residual_abs = 0`) · **28 `PREDICTION-uncorroborated`**
(un-drawn pool alternatives + the p06 heroes + the Regurgitator, so gamora can model any draw) ·
**3 `phase-UNWIRED-in-crucible`** (Kubacabra P2/P3, provenance-only, must not be summed).

`charLevel_grade` distinguishes `MEASURED-CAMERA` from `DERIVED (proxy band + 3; the +3 is MEASURED,
DB-source NAMED-ABSENT)` on every row, so the § 8.2 uncertainty travels with the data instead of living
only in this note.

**Engaged-board instantaneous eHP at wave 160**, at the camera's own multiplicities (Zantarin + Aleksander +
Kubacabra + Galakros + Bileeater + Death Revenant + Shard ×2 + Skeletal Archer ×3):

> **13,981,477**

Comparable HALT-10 figures, using its own `t20` record→form assignment at the 322 cell:

| | HALT-10 | corrected | Δ |
|---|---:|---:|---:|
| four large bodies (Zantarin · Aleksander · Kubacabra · Galakros) | 11,718,978 | **12,697,343** | **+8.35%** |
| summon layer | *not modelled* | **1,284,134** | — |
| board (HALT-10 counts a p06 hero it never had; I count the summons it did) | 12,123,384 | **13,981,477** | **+15.3%** |

### 9.1 Why HALT-10 looked closed to 0.004% — the two errors cancelled, and the p04 gap was the residue

This is the most useful diagnostic in the probe, so it is stated explicitly:

| | base-life change | `M` change | **net** |
|---|---:|---:|---:|
| **nemesis class** (118.6 → 109, 10.02 → 11.29) | **−11.25%** | **+12.67%** | **−0.0039%** |
| **Galakros** (110 → 106, 10.02 → 11.07) | −5.39% | +12.67% | **+4.52%** |

HALT-10's celebrated **±0.004%** nemesis closure was **two errors of ~12% each, in opposite directions,
cancelling**. The cancellation is not a coincidence of luck so much as of construction: the wrong level came
from a `×1.1` equation and the missing term was an array that grows with level, so over-leveling the monster
bought back most of what dropping `armorbase` cost.

And **the p04 "named gap" was the one place the cancellation failed.** Galakros's level error was smaller
(110 vs 106, not 118.6 vs 109) because its record equation was `charLevel*1+5` rather than `(charLevel*1.1)+2`,
so it under-compensated by **4.5%** — which is HALT-10's **−4.14% / −4.33%** residual to within rounding.
The gap I reported as an unexplained property of the superboss was in fact my own missing term, made visible
on the single body whose level error did not happen to hide it. **A residual that survives on one body but not
on others is a term, not a mystery** — I named it as a mystery, and it was a term.

> **Non-additivity warning for gamora.** Summons *respawn*: `petLimit` 3 / 6 / 12 with
> `spawnObjectsTimeToLive` 30–75 s. Total eHP *destroyed* over a wave is strictly greater than the
> instantaneous board eHP above. The number to feed a TTK model is a **flow**, not a stock. The CSV gives
> per-body eHP and per-skill limits; it does not model the flow, and this probe does not claim one.

---

## 10 — CORRIGENDA TO MY OWN HALT-10 NOTE (conductor: restate in the ledger; I amend my note)

Ordered by blast radius.

| # | HALT-10 location | Correction | Grade |
|---|---|---|---|
| **C-1** | § 1 #12 · § 4.5 · § 5 | **`armorbase05.characterLifeModifier` was WRONGLY EXCLUDED. It is a REQUIRED term.** My exclusion test ran at charLevel 118.6, which is itself wrong; at 109 the term is exactly what closes the chain. | REVERSED |
| **C-2** | § 1 #3 · § 2 (2) · § 3 | **The per-record `charLevel` equation is NOT in the chain.** `character.tpl` scopes it to *manual placement*; Crucible bodies are `Proxy.Create` spawns. **charLevel 118.6 is struck; the level is 109 / 106 / 112.** | STRUCK |
| **C-3** | § 1 #5 · § 3 | **The "0.006% two-curve agreement" is NOT evidence.** The two curves are near-proportional; their ratio varies 0.018% over L ∈ [106,150]. Struck as evidence. Correct ratio-solve returns L\* = 108.99. | STRUCK |
| **C-4** | § 1 #9 · § 3 · § 8.3 | **Array index INVERTED.** `G = characterLifeModifier[159] = 324` (the cell labeled 160), not 322. 8/8 exact vs 0/8. **Cross-cutting: `offensiveTotalDamageModifier` at wave 160 is +43, not +41.** Spec § 6.2b's *"the sim consumes the `glad_cell = 322` rows"* must flip. | REVERSED |
| **C-5** | § 1 #4 · § 2 (4) | **`M` is missing a term and carries one it should not.** Correct: `M = 1 + 5.80 + G/100 + armorbase[L−1]/100`. The per-record `own/100` is **falsified** (Bileeater +50 → +4.41%). **Raddoth's +100 does not apply; "Raddoth = 4,102,036" is struck → 3,722,896.** | REVERSED |
| **C-6** | § 1 #8 · § 3 · § 5 (entire section) | **The p04 NAMED GAP is CLOSED.** Galakros @ 106, M = 11.07 → 2,295,755 EXACT. The −4.14% gap and the "3.15 missing levels" are dissolved. **Spec § 12 T-8's declared ±5% p04 band is retired.** | CLOSED |
| **C-7** | § 5 | **The p04 identification was never HP-decidable.** Galakros and the Steward share `((L*33)^1.5)+500`; at equal level their eHP is *identical*. My "Galakros favoured by 6.4 pp of residual" was an artifact of giving them different level bands via the now-struck record-equation link. **The camera nameplate is the only discriminator, and galadriel supplied it.** | STRUCK |
| **C-8** | § 2 (3) · § 6 | **Kubacabra is SINGLE-PHASE in the Crucible.** `sm1` omits `poolToSpawnOnDeath` + `chanceToSpawnOnDeath`. *"The sim needs all three"* is struck. | REVERSED |
| **C-9** | § 0 | **Overlay model wrong.** `.arz` overlay is whole-record replacement, not field merge. All numeric conclusions survive (one field differs across the eight bodies), but the method must change. | METHOD |
| **C-10** | § 6 board table | **The p06 hero band was low.** `bio_hero_standard_01` at L 107–108 → **450,012 – 460,431**, not 398,747–405,213. And no camera fingerprint is a p06 hero — 484,095 / 468,504 / 103,912 / 41,237 are **summons** (a body class HALT-10 did not model at all). | REVISED |
| **C-11** | § 4.3 | **The dedupe probability was wrong.** Not P = 0.20 from "both rolled ×1.1 records". **All 15 `bio_boss_nemesis_01` nemeses have identical eHP**, so a collision between any two non-Kubacabra draws is certain. | REVISED |
| **C-12** | § 1 #13(c) | *"the wave-160 nemesis eHP band is 3.18 M – 3.73 M (4.10 M for Raddoth)"* → **it is a POINT: 3,722,896 for all 15 `bio_boss_nemesis_01` nemeses, plus 2,955,796 for Kubacabra.** | REVISED |
| **C-13** | § 1 #7 | *"Not Raddoth — he carries +100 and lands at 4,102,036"* — the exclusion argument is void (C-5). Immaterial to the outcome: the camera named the bodies. | STRUCK |

**Unchanged and re-confirmed:** § 1 #2 (Ultimate pack `+580`, wired via `gameengine.monsterAttributePak`) ·
§ 1 #10 (H2 — no `monsterClassification`-keyed HP term; note that rank *is* differentiated indirectly, by
which `armorbaseNN` a record runs) · § 1 #11 / § 4.5 (mutators not wired, not needed — the closure is exact
without one) · § 1 #14 (the `colossusgalakros` / `tombguardian` live overlay traps) · § 1 #15
(`ignoreGameBalance`, `proxyPoolEquation` = spawn-count only) · § 2 (1) (no Epic/Legendary variance branch —
re-swept, 0 of 32 corpus-wide) · § 4.4 (the footage is wave 160).

---

## 11 — SCRIPTS (all READ-ONLY, `scratch/2026-08-08-kc2-ehp-composition/`)

| script | purpose |
|---|---|
| `t21_variants.py` | corpus-wide name-token hunt (Zantarin / Aleksander / Galakros variant records) |
| `t22_pools_full.py` | full wave-160 pool-slot → record enumeration |
| `t23_tags.py` | `Text_EN.arc` tag bank (20,394 keys) → DB-cited display names |
| `t24_summons.py` · `t25_bios.py` | summoner skill chains; summon records + bios |
| `t26_solve.py` | **sensitivity audit that falsified HALT-10's ratio evidence** |
| `t27_M.py` · `t28_M2.py` | every `characterLife*` modifier in `records/game/` |
| `t29_joint.py` | joint M-solve across all seven fingerprints |
| `t30_armorbase.py` · `t31_exact.py` | per-body passive arrays; **the 8/8 exact closure** |
| `t32_levels.py` · `t35_w10.py` · `t37_pooleq.py` · `t44_sweep.py` | level machinery: proxies, wave-160 spawn points, pool equation, corpus sweep |
| `t33/t34/t36/t38` | wave-record location; survival level-field sweep; player-level cap; Gladiator pack dump |
| `t39_unique.py` | **falsification / uniqueness test (16,200-pair scan)** |
| `t40_kuba.py` · `t41_deathspawn.py` | Kubacabra phase records; death-spawn pool and its single referrer |
| `t42_overlay.py` · `t43_winneronly.py` · `t46_winnerskills.py` | overlay-semantics proof; winner-only re-verification |
| `t45_petlevel.py` | summon-level rule hunt (NAMED-ABSENT) |
| `t47_emit.py` | **CSV emitter → `t21_wave160_board_ehp_r2.csv`** |

---

## 12 — WHAT THE CONDUCTOR SHOULD DO

1. **Replace § 6.2b of the battle spec wholesale.** The five-link chain becomes four links, one of which
   (`armorbase`) the old text explicitly excluded. New AC-6.5: the chain must reproduce **eight** measured
   fingerprints at **±0 (exact integer)**, not two at ±0.05%.
2. **Flip the array-lookup application for `balancingadjustment_survivalmode_enemies03` to index *w*−1
   (the cell labeled *w*).** Then re-derive every other consumer of that record — `offensiveTotalDamageModifier`
   at wave 160 is **+43**. This is the single most load-bearing consequence and it reverses HALT-10's own
   recommendation.
3. **Retire the p04 ±5% band (§ 12 T-8).** It is closed exactly.
4. **Strike the Kubacabra 3-phase requirement** from § 6.2b and from gamora's mechanism build.
5. **Carry the +3 level offset as a declared sim input** with the § 8.2 NAMED-ABSENT stated, and consider a
   one-question follow-up to galadriel: *a nameplate level read at any other Crucible wave* would separate
   reading (a) from reading (b) and would either DB-close or permanently name the gap.
6. **Note for gamora:** consume `t21_wave160_board_ehp_r2.csv`; the summon layer is new and its
   respawn dynamics make board eHP a flow, not a stock (§ 9).

---

## 13 — Scout's note

The map I drew last pass had every road on it and the compass upside down. The bearing that fixed it was not
in the database at all — it was four small numerals painted on a scroll at the top of the screen, which
galadriel read at ×8 while the arena burned. *Level 109.* I had the creature, the curve and the multiplier and
I had put them together at a level no monster on that board ever stood at. Eight bodies, six curves, three
passives, and when the right level went in they all landed on the integer at once — no residual, no band, no
apology. That is what a closed chain sounds like: nothing.
