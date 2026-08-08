# KC2-SIM — HALT-10 micro-probe: opposition eHP composition (Crucible wave 160, Gladiator)

**Agent:** legolas (UNKNOWN-RESEARCHER)
**Conductor:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, Phase B
**Commission:** targeted micro-probe **HALT-10** — proto HP → on-screen eHP composition chain
**Disposition:** **CLOSED for the nemesis class (residual ≤ 0.004 %) · PARTIAL for the p04 superboss (named gap, −4.13 %)**
**Commit:** NONE (charter § 4.7 — conductor commits at gate close)
**Scratch:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-08-kc2-ehp-composition/`
**External fetches:** ZERO. Everything below is corpus-resident.

---

## 0 — Corpus provenance (MANDATORY)

**Read tree:** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` — the Edition-II pin.

| Archive | md5 | bytes |
|---|---|---:|
| `database/database.arz` | `20d47784be5f93124636992f9e5562e2` | 58 338 379 |
| `gdx3/database/GDX3.arz` | `08365db74863744fea2cfc7254666f55` | 47 334 429 |
| `mods/survivalmode/database/SurvivalMode.arz` | `ac4ad3539196ccf26b6f8be6ab7d3a8b` | 7 052 806 |

All `.arz` reads went through the eight-archive overlay stack, **last-wins**:
`base → gdx1 → gdx2 → gdx3 → sm_mod → sm1 → sm2 → sm3`
(resolver: `scratch/2026-08-08-kc2-ehp-composition/t0_lib.py`; every table below carries its winning archive).

**One disclosed exception — `templates.arc`.** The Edition-II pin ships no `.arc` under `database/`. Template
citations come from the already-extracted Edition-I dump at
`scratch/2026-08-08-kc2-halt-bundle/tpl/` (808 `.tpl`, sourced from `/Users/admin/Games/vendor/grim-dawn/database/templates.arc`,
freshness-probed in the 2026-08-08 HALT-bundle note § 0 — 19/19 1.3.0.0-era field names PRESENT).
Template citations are graded **TPL-CITED (Edition-I archive, freshness-probed)**. **Every numeric value in this
note comes from the Edition-II `.arz`.**

---

## 1 — FINDINGS TABLE (one read for the conductor)

| # | Finding | Grade |
|---|---|---|
| **1** | **The chain is FIVE links, not two.** `eHP = characterLife(bio, charLevel) × (1 + 5.80 + G/100 + own/100)`, where `charLevel` is itself a **two-stage** composition: proxy `levelVarianceEquation` → **per-monster-record `charLevel` equation**. | DB-CITED |
| **2** | **MISSING TERM A — the ordinary Ultimate pack.** `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` `[base]`, `characterLifeModifier = [50,50,50,50, 320,320,320,320, **580**,580,580,580]` (3 difficulties × 4 player-counts). Ultimate/1-player = index 8 = **+580 %**. Wired by `gameengine.monsterAttributePak` → this exact record. This is the "*before ordinary Ultimate difficulty scaling*" phrase from P-E6 line 377, now a number. | DB-CITED |
| **3** | **MISSING TERM B — the per-record `charLevel` equation.** `character.tpl`: *"Equation used to determine level if this character is placed in the world manually."* Four distinct forms on the wave-160 board: `charLevel*1` · `charLevel*1+2` · `charLevel*1+5` · **`(charLevel*1.1)+2`**. At spawn 106 these give charLevel **106 / 108 / 111 / 118.6**. Because `characterLife` is a `^1.5` power law, the `×1.1` form alone is **×1.172** on base HP. **This is what a shared-base model could not produce — 15/16 nemeses share `bio_boss_nemesis_01` but they do NOT share the `charLevel` equation.** | DB-CITED + TPL-CITED |
| **4** | **Combination is ADDITIVE, not multiplicative.** `M = 1 + 5.80 + 3.24 = 10.04`. Multiplicative `(1+5.80)(1+3.24) = 28.83` is **−61 % wrong**. | INFERRED-TESTED |
| **5** | **F1 and F2 CLOSE.** Two fingerprints, **two different bio curves**, one common multiplier: back-solved `M` = **10.019603** (F1) and **10.020158** (F2) — agreement to **0.006 %**. Under the wave-160 array cell (`G=324`) both land at **+0.204 % / +0.198 %**. | DB-CITED |
| **6** | **F2 is a UNIQUE identification: Kubacabra, the Endless Menace** (`nemesis_beast_01_p1`, p02). `bio_boss_nemesis3phase_01` is carried by exactly one record on the wave-160 board. **The captured board contained Kubacabra — a 1-in-5 p02 draw, now MEASURED.** | DB-CITED |
| **7** | **F1 is a ×1.1-group nemesis on `bio_boss_nemesis_01`, from p01 or p03** (p02 is spent on Kubacabra). Candidate set: Benn'Jahr · Curate Ignus · Shriek · Vinn Ozmald (p01) · Reaper of the Lost (p03). **Not Raddoth** — he carries `characterLifeModifier = +100` on his own record and lands at 4,102,036. | DB-CITED |
| **8** | **F3 = the p04 superboss slot, with a NAMED GAP.** Galakros @ charLevel 110 predicts **2,200,824** vs measured 2,295,755 → **−4.135 %**. The Steward @ 105 predicts 2,052,825 → −10.58 %. F3 demands charLevel **113.15** on the `(charLevel*33)^1.5+500` curve; the DB permits at most **110**. **Shortfall = 3.15 levels. No corpus term supplies the missing ×1.043.** | NAMED-ABSENT |
| **9** | **ONE-INDEX QUESTION.** The exactly-solved `M = 10.0196–10.0202` equals `1 + 5.80 + **3.22**` to 0.004 %. `3.22` is the Gladiator cell at **array index 158**; U-8's convention is `wave = index + 1`, so index 158 = wave 159. **The footage is definitively wave 160** (§ 4.4 proof). Reading: the engine indexes the survival adjustment by **completed** waves. Under U-8's convention the chain still closes at **+0.20 %**. | INFERRED-TESTED |
| **10** | **H2 — NAMED-ABSENT.** No hero/boss-rank HP multiplier exists. `gameengine.dbr` (366 fields) carries **zero** classification-keyed life field; its only classification-keyed entries are display colours and speed caps. `monster.tpl` declares a `SuperBoss` classification but **no HP consequence is attached to it anywhere in the corpus.** | NAMED-ABSENT |
| **11** | **H4 — NOT REQUIRED, and not applicable.** 110 mutator records; only `toughened` (+8/10/**12** `characterLifeMultModifier`) and `regenerating` (+4/5/6) touch monster life. **Zero Crucible proxy/pool/wave record references `records/game/mutators/` anywhere in the corpus.** And no mutator term is needed — F1/F2 close to 0.004 %/0.002 % without one. **Mutators are NOT a confound on wave-160 opposition eHP.** | DB-CITED |
| **12** | **TRAP — `armorbase05.characterLifeModifier` is DB-present and empirically EXCLUDED.** Every wave-160 monster runs `skillName3 = records/skills/nonplayerskills/passive/armorbaseNN.dbr` at `skillLevel3 = charLevel*1`; those passives carry a 200-cell `characterLifeModifier` reaching **+137 at index 118**. Including it breaks F1/F2 to +13.9 % / −9.6 % and forces charLevel ≈ 109 — **a level no wave-160 record can produce.** Excluding it lands both at ≤ 0.2 %. | INFERRED-TESTED (excluded) |
| **13** | **CORRECTION to P-E6 § 2.7 / § 4.1 — three errors.** (a) `lv8_boss+` is `min = max = (apl+4)+(apl/50)` — a **point, not a band**; P-E6 quoted `apl+3…apl+4+apl/50`. (b) Boss spawn level at apl=100 is **106**, not 104 — the `apl/50` term was dropped. (c) "**roughly 827,000 effective HP per nemesis**" is **~4.5× low**; the wave-160 nemesis eHP band is **3.18 M – 3.73 M** (4.10 M for Raddoth). | DB-CITED |
| **14** | **NEW LIVE OVERLAY DIVERGENCE (same class as P-E6 § 5.2's werewolf trap, but this one is ON the board).** `bio_boss_aetherial_colossusgalakros`: `gdx1 = ((charLevel*55)^1.53)+6000` vs `sm1 = ((charLevel*33)^1.5)+500`. Identical split on `bio_boss_tombguardian` (`gdx2` vs `sm2`). **Both are wave-160 p04 records.** A join that resolves them through the campaign stack returns a wildly different curve. | DB-CITED |
| **15** | **`ignoreGameBalance` does NOT gate the life modifier.** `proxypool.tpl` declares it `type="bool" default="0"` with **no description** (semantics NAMED-ABSENT). But it cannot gate the survival pack: the three nemesis pools carry `True`, and if that suppressed the +324 term F1 would miss by −32 %. `proxyPoolEquation` (present on **all six** wave-160 pools, not just p04) is `poolValue * 1` on all four spawn/champion fields — **spawn-count only, no HP.** | DB-CITED |

---

## 2 — THE CHAIN, stated for the sim

```
                  apl = averagePlayerLevel = 100          (fixture is L100)
  (1) spawn_level  = levelVarianceEquation(apl)           records/proxies/lv*.dbr           [base]
  (2) charLevel    = <per-record equation>(spawn_level)   monster record field `charLevel`  [overlay winner]
  (3) base_life    = characterLife(charLevel)             bio via characterAttributeEquations
  (4) M            = 1 + 5.80 + G/100 + own/100
  (5) eHP          = base_life * M
```

### (1) Level-variance proxies — DB-CITED, `records/proxies/…` `[base]`

| proxy | `minVarianceEquationNormal` | `maxVarianceEquationNormal` | at apl = 100 |
|---|---|---|---|
| `lv8_boss+.dbr` (p01/p02/p03, all nemeses) | `(averagePlayerLevel+4)+(averagePlayerLevel/50)` | *identical* | **106** (a point) |
| `lv7_uber hero.dbr` (p04 superbosses) | `(averagePlayerLevel+3)` | `(averagePlayerLevel+3)+(averagePlayerLevel/50)` | **103 – 105** |
| `lv6_hero.dbr` (p06 hero) | `(averagePlayerLevel+2)+(averagePlayerLevel/50)` | `(averagePlayerLevel+3)+(averagePlayerLevel/50)` | **104 – 105** |

**All 16 `lv*.dbr` records in the corpus carry ONLY `…Normal`.** `proxylevelvarianceequation.tpl` declares
`minVarianceEquationEpic/Legendary` and `maxVarianceEquationEpic/Legendary`, and **0 of 16 records populate them**
(TPL-CITED + DB-CITED). There is **no Elite/Ultimate level-variance branch**. This closes one H1 sub-question outright.

### (2) The per-record `charLevel` equation — the term the model was missing

`character.tpl` → `charLevel`, `type = "equation"`, description verbatim:
> *"Equation used to determine level if this character is placed in the world manually."*

| form | wave-160 records | charLevel at spawn 106 |
|---|---|---:|
| `(charLevel*1.1)+2` | Benn'Jahr · Curate Ignus · Shriek · Vinn Ozmald · **Raddoth** · Grava'Thul · Underking · Reaper of the Lost · Reaper of Rot · **Kubacabra** | **118.6** |
| `charLevel*1+5` | Archmage Aleksander (p03) · **Galakros** (p04, on spawn 103–105) | 111 / 108–110 |
| `charLevel*1+2` | Valdaran (p01) · *the five p06 heroes carry `(charLevel*1)+2`* | 108 / 106–107 |
| `charLevel*1` | Zantarin · Iron Maiden · Fabius · Moosilauke · **The Steward** (p04) | 106 / 103–105 |

### (3) `characterLife` — five curves on the wave-160 board

| bio | equation | winning archive | carried by |
|---|---|---|---|
| `bio_boss_nemesis_01` | `((charLevel*42)^1.5)+20000` | `sm_mod` | **16** wave-160 records |
| `bio_boss_nemesis3phase_01` | `((charLevel*36)^1.5)+16000` | `sm1` | Kubacabra P1 only |
| `bio_boss_aetherial_colossusgalakros` | `((charLevel*33)^1.5)+500` | **`sm1`** ⚠ see § 1 #14 | Galakros |
| `bio_boss_tombguardian` | `((charLevel*33)^1.5)+500` | **`sm2`** ⚠ | The Steward |
| `bio_hero_standard_01` | `((charLevel*11)^1.50)-20` | `sm_mod` | all five p06 heroes |

**Kubacabra is 3-phase with a different bio per phase** — the sim needs all three:
`bio_boss_nemesis3phase_02 = ((charLevel*19)^1.5)+9000` (P2, records `_p2a/_p2b`) and
`bio_boss_nemesis3phase_03 = ((charLevel*13)^1.5)+3000` (P3, records `_p3a…_p3d`).
At charLevel 118.6 and `M = 10.04` that is **P1 2,961,649 → P2 1,164,328 → P3 637,941**.

### (4) The multiplier `M` — two global sources, additive

| source | record | value | provenance |
|---|---|---:|---|
| ordinary **Ultimate** difficulty | `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` `characterLifeModifier[8]` | **+580** | `[base]`; wired by `gameengine.monsterAttributePak` |
| Crucible **Gladiator** wave cell | `records/game/balancingadjustment_survivalmode_enemies03.dbr` `characterLifeModifier[159]` | **+324** | `[sm_mod]` |
| per-record | monster `characterLifeModifier` | **+100 on Raddoth only** (0/None on all other 22) | overlay winner |
| **multiplayer** | same pack, `characterLifeMultModifier[8]` | **0** (solo) — `[0,90,180,270]` per difficulty by player count | `[base]` |

`characterLifeMultModifier` is the **only** multiplicative life term in the corpus adjustment layer, and at
solo Ultimate it is **zero**. That is the DB's own statement that solo life scaling is additive.

---

## 3 — CLOSURE

Exact arithmetic, `scratch/…/t19_final.py`, emitted to `t19_closure.csv`.

```
spawn (lv8_boss+, apl=100) = (100+4)+(100//50) = 106
nemesis charLevel          = 1.1*106 + 2       = 118.6
base_life  bio_boss_nemesis_01       @118.6 = 371,561.225
base_life  bio_boss_nemesis3phase_01 @118.6 = 294,984.956
base_life  bio_..colossusgalakros    @110   = 219,205.617
```

| Gladiator cell | `M` | fingerprint | measured | predicted | residual |
|---|---:|---|---:|---:|---:|
| **wave-160 (idx 159), G = 324** | 10.0400 | **F1** ×1.1 nemesis | 3,722,896 | 3,730,474.7 | **+0.2036 %** |
| | | **F2** Kubacabra | 2,955,796 | 2,961,649.0 | **+0.1980 %** |
| | | **F3** Galakros @110 | 2,295,755 | 2,200,824.4 | **−4.1350 %** |
| | | *F3′ The Steward @105* | 2,295,755 | 2,052,824.9 | −10.5817 % |
| **wave-159 (idx 158), G = 322** | 10.0200 | **F1** | 3,722,896 | 3,723,043.5 | **+0.0040 %** |
| | | **F2** | 2,955,796 | 2,955,749.3 | **−0.0016 %** |
| | | **F3** Galakros @110 | 2,295,755 | 2,196,440.3 | −4.3260 % |

**Back-solved exact multiplier:** F1 → `10.019603` · F2 → `10.020158`. Two independent fingerprints running
through **two different power-law curves with different coefficients (42 vs 36) and different constants
(20000 vs 16000)** agree on `M` to **0.006 %**. That agreement is the evidence; it cannot be fitted, because
`M` was not free per fingerprint.

**Stated envelope (declared before shopping, not after):** the chain is **CLOSED for the nemesis class within
±0.21 %** under the U-8 index convention, and within **±0.005 %** under the completed-waves reading. The
p04 superboss is **NOT closed**; its residual is **−4.14 %** and is reported as a gap, not fitted away.

---

## 4 — HYPOTHESIS VERDICTS

### 4.1 H1 — spawn-level re-evaluation — **CONFIRMED, and it is the larger of the two missing terms**

Not in the form the commission proposed (there is no Ultimate-specific level table — § 2 (1) proves the
`…Epic/Legendary` variance branches are unpopulated in all 16 records). The real mechanism is the **two-stage
level composition**: the proxy sets a spawn level, then the *monster record's own* `charLevel` equation
re-evaluates it. The 308,685 figure in P-E6 § 4.1 is `((104*42)^1.5)+20000` — i.e. it was quoted at charLevel
**104**, which is (a) two levels below the proxy's own output (106) because the `apl/50` term was dropped, and
(b) **14.6 levels** below where 10 of 16 nemeses actually land (118.6). Corrected nemesis base band:
**317,052 – 371,561**.

### 4.2 H2 — hero/boss rank multipliers — **NAMED-ABSENT**

`records/game/gameengine.dbr` `[base]`, all 366 fields read. Every classification-keyed field is cosmetic or
speed: `bossMonsterColor {^r}` · `heroMonsterColor {^o}` · `championMonsterColor {^y}` · `questMonsterColor {^p}` ·
`bossAttackSpeedCapMax/Min` · `bossRunSpeedCapMax/Min` · `bossSpellCastSpeedCapMax/Min` · `bossRange`.
**No `heroHealthModifier`, no boss-rank HP term, nothing keyed on `monsterClassification` that touches life.**
`monster.tpl` declares the picklist `Common;Champion;Hero;Boss;Quest;SuperBoss;` — the corpus attaches **no HP
consequence** to any of those values. Rank differentiation is carried entirely by *bio choice* + *`charLevel`
equation*.

### 4.3 H3 — per-record proto variation + class mix — **CONFIRMED on both halves**

- **Proto variation:** confirmed, and it is `charLevel`, not the bio. 15/16 nemeses do share
  `bio_boss_nemesis_01`; they split **10 / 1 / 1 / 4** across four `charLevel` forms. Plus one per-record
  `characterLifeModifier` (**Raddoth +100** — the only one on the board).
- **Class mix:** confirmed, and the fingerprint→record assignment is **F1 = nemesis (p01 or p03, ×1.1 group) ·
  F2 = Kubacabra (p02, unique) · F3 = p04 superboss (Galakros favoured over the Steward by 6.4 pp of residual)**.
- **Census reading, flagged for the conductor:** the board holds **five** bodies but the census reports **three**
  boss-class values. The hero slot (405,213) is an order of magnitude below the rest and presumably below the
  census threshold. The **third nemesis is unaccounted for**. Two readings, both DB-consistent: (i) the census
  reported top-3 only; or (ii) **both p01 and p03 rolled ×1.1-group records on `bio_boss_nemesis_01`, giving
  byte-identical HP that a distinct-value census would deduplicate** — P = 0.4 × 0.5 = **0.20** exactly.
  Worth one question to galadriel: *was the census top-N or all-distinct?* The answer changes the wave-160
  board reconstruction.

### 4.4 The wave-160 identity, proved (rules out "the footage was wave 159")

The `M`-solve lands on the **wave-159 array cell**, so the alternative "the footage was wave 159" had to be
killed on independent grounds. It is:

| wave | distinct bios on the whole board |
|---|---|
| **159** | 14 bios — `bio_boss_beetle_02` · `..chthonian_ekketzul` · `..chthonian_lunalvalgoth` · `..fleshhulk_01` · `..gryphonstone_01` · `..humanwendigo_darkwood` · `..jaggedwaste_manticore_01` · `..rok_wind_01` · `..statue_templeguardian_02` · `..stepsoftorment_golem_phase01` · `..themessenger` · `..wendigo_ancient` · `..witchgodguardian_temple` · `..yeti_rimehorn_01` |
| **160** | 5 bios — **`bio_boss_nemesis_01` (n=16)** · **`bio_boss_nemesis3phase_01` (n=1)** · `bio_boss_aetherial_colossusgalakros` · `bio_boss_tombguardian` · `bio_hero_standard_01` |

**Neither F1/F2 bio exists anywhere on the wave-159 board.** The footage is wave 160. Therefore the
index-158 result is a **statement about the engine's indexing rule**, not about which wave was filmed —
the engine appears to index the survival adjustment by *completed* waves (`wave N → cell N−2`, 0-based).
Graded INFERRED-TESTED: the database does not state the indexing rule, so this is an inference from a
0.004 % fit across two curves, not a citation.

### 4.5 H4 — mutator HP terms — **NOT REQUIRED, and out of scope for the Crucible**

Two independent grounds, either sufficient:

1. **Not needed.** F1 and F2 close to 0.004 % / 0.002 % with no mutator term. Any mutator multiplier would
   *break* an already-exact fit. The smallest available monster-life mutator is `toughened` at +8 %.
2. **Not wired.** 110 records under `records/game/mutators/`; **12** carry a non-zero life field
   (`toughened{,_e,_u}` `characterLifeMultModifier` 8/10/12 · `regenerating{,_e,_u}` 4/5/6 +
   `characterLifeRegenModifier` 25/35/40 · `leeching{,_e,_u}` `offensiveLifeLeechMin` 400/500/600 ·
   `player_vigorous{,_e,_u}` 12, player-side). A corpus-wide sweep of every proxy record found **zero**
   Crucible reference to `records/game/mutators/`; the only survival-tree "mutator" hits are FX and sound
   (`records/fx/general/playermutator_fx01.dbr` `[sm_mod]`, `records/sounds/spak_playermutator.dbr` `[sm_mod]`).

**Verdict: no declared confound. H4 does not bind.** The commission's stop-condition ("if a mutator multiplier
is required to close, say so and STOP") is not triggered.

---

## 5 — THE NAMED GAP (F3)

Everything below was **ruled out by reading, not by fitting**:

| candidate explanation | verdict |
|---|---|
| campaign-vs-survival bio overlay on Galakros/Steward | **ruled out** — the campaign curve `((cl*55)^1.53)+6000` requires charLevel ≈ 57 to hit the target; the survival curve is the overlay winner and is the one used |
| Elite/Ultimate level-variance branch on `lv7_uber hero` | **ruled out** — 0 of 16 `lv*.dbr` populate `…Epic/…Legendary` |
| absorb-shield inflating the on-screen bar | **ruled out** — neither p04 record carries a `Skill_BuffSelfShield`; Galakros has `galakros_enrage` (`Skill_PassiveOnLifeBuffSelf`), the Steward has no self-buff at all |
| phase records (as Kubacabra has) | **ruled out** — neither Galakros nor the Steward has a `_p2`/`_p3` sibling anywhere in the corpus |
| per-record `characterLifeModifier` | **ruled out** — 0.0 / None on both |
| `proxyPoolEquation` | **ruled out** — `poolValue * 1` on all four fields; present on **all six** wave-160 pools, not just p04 |
| mutators | **ruled out** (§ 4.5) |
| `armorbase05` passive | **ruled out** (§ 1 #12) — including it breaks F1/F2 and demands an impossible level |
| a different apl | **ruled out** — apl = 100 is *pinned* by F1/F2 landing at 118.6 = 1.1 × ((100+4)+(100//50)) + 2 |

**Statement of the gap, exactly:** at `M = 10.04`, F3 requires `base_life = 228,660.9`, i.e.
**charLevel 113.148** on the `(charLevel*33)^1.5+500` curve. The database permits Galakros at **108–110**.
**Shortfall: 3.15 levels, equivalently a missing ×1.0431 on the p04 superboss only.**

**Recommendation to the conductor:** carry the nemesis class as CLOSED and the p04 slot as a declared
±5 % uncertainty band, **or** ask galadriel to re-read the F3 fingerprint and confirm the census methodology
(top-N vs all-distinct, and whether the p04 body was visually Galakros or the Steward — they are
visually unmistakable: an aetherial colossus vs an animated statue). The DB cannot adjudicate further.

---

## 6 — SIM-READY OUTPUT

`scratch/2026-08-08-kc2-ehp-composition/t20_wave160_board_ehp.csv` — 60 rows: every wave-160 roster record ×
every DB-permitted spawn level × both Gladiator cells, with `bio`, `life_eq`, `charLevel_eq`, `proxy`,
`spawn_level`, `charLevel`, `own_lifemod`, `M`, `base_life`, `eHP`.

**The board, at `M = 10.04` (wave-160 cell) / `M = 10.02` (completed-waves reading):**

| pt | monster | bio | `charLevel` eq | cl | base | eHP@324 | eHP@322 |
|---|---|---|---|---:|---:|---:|---:|
| p01 | **Raddoth** *(+100 own)* | nemesis_01 | `(charLevel*1.1)+2` | 118.6 | 371,561 | **4,102,036** | 4,094,605 |
| p01 | Benn'Jahr · Curate Ignus · Shriek · Vinn | nemesis_01 | `(charLevel*1.1)+2` | 118.6 | 371,561 | **3,730,475** ← **F1** | 3,723,043 |
| p02 | Underking · Grava'Thul · Reaper of the Lost · Reaper of Rot | nemesis_01 | `(charLevel*1.1)+2` | 118.6 | 371,561 | 3,730,475 | 3,723,043 |
| p03 | Reaper of the Lost | nemesis_01 | `(charLevel*1.1)+2` | 118.6 | 371,561 | 3,730,475 | 3,723,043 |
| p03 | Archmage Aleksander | nemesis_01 | `charLevel*1+5` | 111 | 338,316 | 3,396,692 | 3,389,926 |
| p01 | Valdaran | nemesis_01 | `charLevel*1+2` | 108 | 325,499 | 3,268,008 | 3,261,498 |
| p01 | Zantarin · Iron Maiden · Fabius · Moosilauke | nemesis_01 | `charLevel*1` | 106 | 317,052 | 3,183,204 | 3,176,863 |
| p02 | **Kubacabra P1** | nemesis3phase_01 | `(charLevel*1.1)+2` | 118.6 | 294,985 | **2,961,649** ← **F2** | 2,955,749 |
| p02 | *Kubacabra P2* | nemesis3phase_02 | `(charLevel*1.1)+2` | 118.6 | 115,969 | 1,164,328 | 1,162,010 |
| p02 | *Kubacabra P3* | nemesis3phase_03 | `(charLevel*1.1)+2` | 118.6 | 63,540 | 637,941 | 636,671 |
| p04 | **Galakros** | colossusgalakros | `charLevel*1+5` | 108–110 | 213,268–219,206 | 2,141,212–**2,200,824** ← **F3 −4.1 %** | 2,196,440 |
| p04 | The Steward | tombguardian | `charLevel*1` | 103–105 | 198,665–204,465 | 1,994,596–2,052,825 | 2,048,736 |
| p06 | 5 wendigo-cannibal heroes | hero_standard_01 | `(charLevel*1)+2` | 106–107 | 39,795–40,360 | 399,543–405,213 | 404,406 |

**Total board eHP** (3 nemeses + 1 superboss + 1 hero, using the F1/F2/F3 assignment): **≈ 9.4 M**, versus the
≈ 4.1 M the old `308,685 × 4.24` model would have produced for the same five bodies. **The sim's opposition
health pool was understated by ~2.3×.**

---

## 7 — SCRIPTS

All under `scratch/2026-08-08-kc2-ehp-composition/`, all READ-ONLY:

| script | purpose |
|---|---|
| `t0_lib.py` | eight-archive overlay resolver (`owners` / `read` / `merged` / `find`) |
| `t1_roster_hp.py` | wave-160 pool → 23 distinct monster records |
| `t2_monster_fields.py` · `t3_chain.py` | full field dump; `charLevel` / bio / classification chain; level proxies |
| `t4_hunt_multipliers.py` · `t5_difficulty.py` | `records/game/*` inventory; the Ultimate + challenge + ultra packs |
| `t6_ratio_solve.py` · `t7_exact_solve.py` · `t8_enumerate.py` | multiplier-invariant ratio test; exact 2-unknown solve; exhaustive M-consistency enumeration |
| `t9_mods_and_mutators.py` | wave-cell verification; per-record modifiers; 110-mutator sweep |
| `t10_wave160_proxies.py` · `t14_p04_deep.py` | re-verified spawn-point proxies from source; p04 per-archive diff |
| `t12_phases.py` · `t13_kubacabra_phases.py` | phase/variant records; 727-bio inverse search for F3 |
| `t15_pooleq_and_tpl.py` | `proxyPoolEquation`; template annotations |
| `t16_skills_gear.py` · `t17_armorbase.py` | skill/item chain scan; the `armorbase*` passive layer |
| `t18_final_sweep.py` · `t19_final.py` | corpus-wide adjustment-record sweep; high-precision closure |

Emitted: `t11_predicted_ehp.csv` · `t19_closure.csv` · **`t20_wave160_board_ehp.csv`** (the sim input).

---

## 8 — WHAT THE CONDUCTOR SHOULD DO

1. **Replace the eHP model.** `308,685 × (1+3.24)` → the five-link chain in § 2. The old model was low by
   **2.3×–2.8×** per nemesis.
2. **Take the numbers from `t20_wave160_board_ehp.csv`**, not from this note's rounded table.
3. **Decide the index convention.** Both are defensible; the completed-waves reading fits 50× tighter.
   Whichever is chosen, the *same* rule must be applied to every other array in
   `balancingadjustment_survivalmode_enemies03` — including `offensiveTotalDamageModifier`, which HALT-9
   already corrected to +43 at wave 160 (that becomes **+41** under the completed-waves reading).
   **This is a cross-cutting consequence and it is the single most load-bearing open item here.**
4. **Carry the p04 gap as a declared ±5 % band**, or route one question to galadriel (§ 5).
5. **Log the two live overlay traps** (§ 1 #14) alongside P-E6 § 5.2's werewolf entry.
