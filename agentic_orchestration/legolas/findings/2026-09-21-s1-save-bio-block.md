# Research — S-1: the save's bio block — field mapping, true values, blast radius — 2026-09-21

**Mode:** A (analytical / primary-source probe)
**Commission:** **S-1**, issued under *The Commission Rule* (`gandalf/notes/2026-09-21-the-commission-rule.md`), Run KC2-PLAY
**Commissioner / conductor:** gandalf (RUN-CONDUCTOR)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Access:** read-only throughout. No save, game file, pack, oracle or vendor tree was modified. No network fetch was made for S-1 (§ 8).

---

## HEADLINE

⚑ **THE MAPPING IS CORRECT. The field order is right, the offsets are right, and there is no v8 drift in this block. The character genuinely stored `physique 74 / cunning 858 / spirit 74`.**

**And the domain argument that motivated the commission is wrong on its own terms, from the client's own text:**

> `tagCharAttributeDescription01` — *"A cunning intellect improves your combat technique, increasing **physical**, pierce, bleed and internal trauma damage. Cunning also increases your … chances of landing melee and ranged attacks, and critically hitting enemies."*

**Cunning is Grim Dawn's PHYSICAL-damage attribute**, first-named in the client's own list, and the sole attribute source of Offensive Ability (`tagCharStatsOADescription`). For a **physical** two-handed Eye-of-Reckoning Warlord, dumping attribute points into Cunning is not eccentric — it is the attribute that scales the build's damage and its hit/crit chance. Physique was never the binding constraint on his gear: ⚑ **his two mastery bars and his devotion tree supply 890 Physique before a single attribute point is spent** — 1013 with the base 50 and gear's 73 — against a computed weapon requirement of ≈474.

**But S-1 was worth issuing anyway, because the probe surfaced three material errors — none of them in the mapping.**

1. ⚑ **C-1 § 5.1 double-counted the base 50.** The bio's `74` is **already** `50 + 3 × 8`; C-1 added the base again.
2. ⚑ **C-1 § 5.1 omitted the two mastery bars and the devotion tree**, which together contribute **+349 Intelligence** (194 + 155). Corrected total Spirit is **536 flat (568 after the +6 % modifier)**, not 237. ⚑ **The residual C-1 reported as 28.75 /s is roughly a third of that once the term is corrected** (§ 5.2).
3. ⚑ **C-1 § 5.3's base-energy term `250 + 16 × 99 levels = 1834` is wrong.** `manaIncrement = 16` is charged **per attribute point spent in Spirit**, not per level. Verified exactly on nine independent saves at levels 1, 13 and 100. The character's stored base energy is **298**.

⚑ **And one methodological finding with reach beyond this commission: expansion archives OVERRIDE base, and first-hit archive ordering silently reads a STUB.** `_classtraining_class09.dbr` (the Oathkeeper mastery bar) is a **32-rank placeholder in `database.arz`** and the **live 100-rank record in `GDX2.arz`**. Read first-hit, it reports `+64 STR / +56 INT / +256 energy`; read correctly, `+250 / +125 / +650`. § 6.

**Blast radius in CODE: zero.** No constant in `simulation/kc2/`, no value in the v3.x pack, and nothing in the Godot runtime derives from this block (§ 7, measured). The three errors are confined to C-1's § 5 prose ledger — a *narrative* correction, not a re-derivation of the pack.

---

## 0 · Surfaces — what was searched, what was reachable, what was not

| Surface | Status | Detail |
|---|---|---|
| **The save** | ✅ **9 distinct saves**, the control set | sha256 prefixes `b8e6f5` (referent, canonical fixture), `9e6fe9`, `c8738d`, `514a06`, `2ba5a4`, `ced728`, `f55b42`, `0d95d9`, `0be3a9`. Levels 1, 13 and 100; five masteries; two fresh characters. § 1.3 |
| **Game on disk — DBRs / ARZ** | ✅ **LIVE** | `/Users/admin/depots/` — 8 archives: 34,114 (base) + 18,447 (GDX1) + 16,451 (GDX2) + 24,178 (GDX3) + 3,147 + 1,004 + 811 + 1,431 (SurvivalMode). Record counts **match the 2026-07-23 probe exactly** — parser validated, not assumed. |
| **Localization** | ✅ | 7 × `Text_EN.arc`, **20,394 tags** (matches C-1's count) |
| **Game on disk — binary** | ❌ **UNAVAILABLE** | No PE binary on this host (unchanged from C-1). Not needed for S-1: the mapping closed from DBRs alone. |
| **Quest data** | ❌ **NOT ON DISK** | The depot ships `database/*.arz` and `resources/Text_EN.arc` only. No `Quests.arc`, no level archives. Bears on § 3.3 (the attribute-point budget) and is graded there. |
| **Build guide / web** | ⚪ **NOT FETCHED** | S-1 did not require it. The mapping question is answerable from primary sources only, and a guide could not settle a byte layout. **No robots.txt claim is made for S-1 because no fetch was attempted.** C-2 (separate file) carries its own robots record. |

**Reproduction tooling** (scratch, read-only): `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-09-21-s1-bio/`
- `arz.py` — TQIT `.arz` reader, all 8 archives, **with expansion-override precedence** (§ 6)
- `gdcg7.py` — copied unmodified from `legolas/scratch/2026-07-28-gdc-parse-g7/gdc_parse.py`
- `arcread.py` — copied unmodified from `research/scripts/gd_arc_reader_2026_07_26.py`
- `probe1_bio_raw.py` — raw 32-bit word dump of the bio block, both interpretations, every sample
- ⚑ `verify_bio.py` — **the control.** Tests the mapping against a closed form built entirely from the DBRs, over all samples, H1 vs H2
- `ledger.py` — full attribute ledger (bio + skills + devotions + gear)
- `tags.py`, `scan.py` — localization and full-database field scans

---

## 1 · Q1 — THE MAPPING

### 1.1 The block does not drift, and there is no room for it to

Raw dump of `character_bio` (block id 2) across **all nine distinct saves**:

| property | value | across |
|---|---|---|
| block version | **8** | 9 / 9 saves |
| payload length | **48 bytes** | 9 / 9 saves |
| words consumed by `version + 6 × int32 + 5 × float32` | **48 bytes** | exact |
| **trailing bytes** | **0** | 9 / 9 saves |
| end-of-block sentinel | **OK** | 9 / 9 saves |

⚑ **The block is fully consumed with zero residue on every sample, including saves whose NEIGHBOURING blocks drifted hard** — `inventory` reads version **11** against the 1.1.9.1 reference's 4, and `character_stash` **11** against 6. The bio block sat still while the blocks either side of it moved. That is the structural answer to *"has the format drifted?"*: **there is no unaccounted byte in which a drift could hide.**

Header-vintage discriminator, recorded because it separates the sample set: the post-header byte reads **7** on current-format saves and **1** or **3** on older ones. `gdc_file` version is **8** on all nine.

### 1.2 The layout, confirmed

```
block 2 "character_bio", version 8, 48 bytes:
   +0x00  uint32   level
   +0x04  uint32   experience
   +0x08  uint32   attributePointsUnspent
   +0x0c  uint32   skillPointsUnspent
   +0x10  uint32   devotionPointsUnspent
   +0x14  uint32   totalDevotionUnlocked
   +0x18  float32  physique        <-- CONFIRMED
   +0x1c  float32  cunning         <-- CONFIRMED
   +0x20  float32  spirit          <-- CONFIRMED
   +0x24  float32  health          <-- CONFIRMED (base, attribute-derived)
   +0x28  float32  energy          <-- CONFIRMED (base, attribute-derived)
```

This is the order both of our parsers already use (`research/scripts/gd_gdc_parse.py` and `legolas/scratch/2026-07-28-gdc-parse-g7/gdc_parse.py`). ⚑ **They inherited it from one common ancestor — the AaronHutchinson 1.1.9.1 reference — so their agreement was never independent evidence.** S-1 supplies the independent evidence.

### 1.3 ⚑ THE CONTROL — a closed form from the DBRs, tested on every sample

From `records/creatures/pc/playerlevels.dbr` and `records/creatures/pc/malepc01.dbr`, **read, not assumed**:

| field | value | archives agreeing |
|---|---|---|
| `characterStrength` / `Dexterity` / `Intelligence` (base PC) | **50.0** each | base, GDX1, GDX2, GDX3 |
| `characterLife` / `characterMana` (base PC) | **250.0** each | base, GDX1, GDX2, GDX3 |
| `strengthIncrement` / `dexterityIncrement` / `intelligenceIncrement` | **8** | base, GDX1, GDX2 |
| `lifeIncrement` (per Physique point) | **20** | base, GDX1, GDX2 |
| `lifeIncrementDexterity` (per Cunning point) | **8** | base, GDX1, GDX2 |
| `lifeIncrementIntelligence` (per Spirit point) | **12** | base, GDX1, GDX2 |
| `manaIncrement` (per Spirit point) | **16** | base, GDX1, GDX2 |
| `characterModifierPoints` (attribute points per level) | **1** | base, GDX1, GDX2 |

Corroborated verbatim by the client: `tagTutorialTip16TextC` — *"Each attribute point increases the attribute by 8."*

That yields two identities with **no free parameter**:

```
points_X  = (stored_X - 50) / 8
energy    = 250 + 16 x points_SPIRIT
health    = 250 + 20 x points_PHYSIQUE + 8 x points_CUNNING + k x points_SPIRIT
```

**H1** = the parser's order. **H2** = physique and cunning swapped (the hypothesis the commission asked me to test — it is the one that would make the referent a 858-Physique character).

| character | lvl | stored (P, C, S, HP, EN) | H1 energy | H1 health | **H2 health** |
|---|---|---|---|---|---|
| **EoRWarlGuts** (referent, `b8e6f5` / `9e6fe9`) | 100 | 74, 858, 74, **1154**, 298 | EXACT | **EXACT** (k=12) | ❌ predicts **2330** |
| EoRWarlGuts (older snapshots, ×3) | 100 | 74, 858, 74, **1142**, 298 | EXACT | **EXACT** (k=8) | ❌ predicts 2330 |
| Fresh Character 01 | 13 | 122, 74, 50, **454**, 250 | EXACT | **EXACT** | ❌ predicts 382 |
| Hellwrathh | 100 | 402, 394, 178, **1602**, 506 | EXACT | **EXACT** (k=8) | ❌ predicts 1654 |
| Ward The Soldier | 100 | 370, 402, 210, **1050**, 570 | EXACT | see § 1.4 | ❌ |
| DawnGuard / custom / AAANoQuestsTest | 1 | 50, 50, 50, 250, 250 | EXACT | EXACT | (cannot discriminate) |

⚑ **H1 reproduces the stored health to the unit on every discriminating sample. H2 fails on every one of them, and on the referent it is wrong by a factor of two.** The energy identity is EXACT on all nine saves under both hypotheses — it does not discriminate P from C, but it **pins the spirit slot absolutely**, and that is the slot C-1 depends on.

**Two things make this a finding rather than a fit:** the constants come from the shipped database and were not solved for, and the mapping was tested on characters of three different levels and five different masteries, including two fresh level-1 saves whose every attribute reads exactly the PC record's `50`.

### 1.4 The one exception, named and not smoothed

**Ward The Soldier** (`ced728`) does not close under either `k`. It closes **exactly** as `250 + 20 × 40 = 1050`, i.e. under a ruleset in which **only Physique contributes health**. Its `character_info` block is version **4** against the reference's 5 and its post-header byte is **1** — it is an old-format save from an older game version.

⚑ **The outlier still votes for H1.** The physique-only reading uses slot `[6] = 370 → 1050` exactly; under H2 it would use `[7] = 402 → 1130`, and misses. **The sample that breaks the formula does not break the mapping.**

A second, smaller version signal, reported and not reconciled: the referent's three **older** snapshots store health **1142** and the two current ones **1154**, on byte-identical attributes. `1154 − 1142 = 12 = 4 × points_SPIRIT`, which is exactly the delta between `lifeIncrementIntelligence = 8` and `= 12`. The clean single-constant reading is that the constant changed between those two save vintages and the game recomputed base health on load. **Hellwrathh closes at `k = 8` and the current referent at `k = 12`, consistent with that.** I have no second source for a patch that changed it; recorded as an observation, graded **CONSISTENT-NOT-SOURCED**.

---

## 2 · Q2 — the corrected values, with provenance

### 2.1 The stored (base) attributes — UNCHANGED, now verified

| field | value | what it means | grade |
|---|---|---|---|
| `physique` | **74.0** | `50` base + `3` attribute points × 8 | `SAVE-DECODED` + `DB-VERIFIED` (§ 1.3) |
| `cunning` | **858.0** | `50` base + `101` attribute points × 8 | same |
| `spirit` | **74.0** | `50` base + `3` attribute points × 8 | same |
| `health` | **1154.0** | `250 + 20·3 + 8·101 + 12·3` — reproduces exactly | same |
| `energy` | **298.0** | `250 + 16·3` — reproduces exactly | same |

⚑ **What "stored" EXCLUDES, and this is the load-bearing clarification:** the bio block holds **base + attribute-point allocation ONLY**. Mastery bars, devotions, gear, augments and components are **not in it**. They are applied at runtime on top. Any ledger that treats the bio value as the character's attribute will understate it badly — which is precisely what happened in C-1 § 5.

### 2.2 The TOTAL attributes — the numbers a ledger actually wants

Summed from the save's own allocation, every row resolved to its record at its allocated rank, **with expansion-override precedence applied** (§ 6):

| source | Physique | Cunning | **Spirit** | Energy |
|---|---|---|---|---|
| bio block (base + 107 attribute points) | 74 | 858 | **74** | 298 |
| Soldier mastery bar @ rank 46 (`_classtraining_class01.dbr`, `database.arz`) | +230 | +161 | **+69** | +460 |
| ⚑ Oathkeeper mastery bar @ rank 50 (`_classtraining_class09.dbr`, **`GDX2.arz`**) | +250 | +125 | **+125** | +650 |
| devotion tree (55 points) | +410 | +230 | **+155** | +1200 |
| gear + affixes + components + augments | +73 | +55 | **+113** | +220 |
| **flat total** | **1037** | **1429** | **536** | **2828** |
| `…Modifier` (%) | +28 % | +6 % | **+6 %** | +4 % |
| **after modifier** | **1327** | **1515** | **568** | **2941** |

**Gear's `characterIntelligence` +113 decomposes as:** `a007b_ch_att_all_10` suffix +55 · `b_ar007_ar_f` prefix +38 · `compb_sealannihilation` +20. ⚑ **C-1's 113 was right. What was missing around it was everything else.**

⚑ **The energy-pool row is reported as a SWEEP, not as an audited ledger, and it does NOT close against the pack's `ENERGY_MAX = 2576 (MEASURED)`.** 2941 flat-after-modifier is **365 over**. The pack's own `MO_ENERGY_RESERVATION = 982.0` is a separate, downstream subtraction (`2576 − 982 = 1594`, the observed ceiling), so the gap is not the reservation. My sweep walks buff chains breadth-first and may credit a rank or a record the runtime does not; **I am not asserting a corrected 2576, and nothing downstream should take 2941 as a value.** The attribute columns, by contrast, are itemised per record above and each row is individually checkable.

---

## 3 · Q4 — is this genuinely his allocation? YES, and here is why the build reads that way

The commission said: *"an unusual build is not an impossible one, and I would rather be told I was wrong about the game."* So, plainly: **you were wrong about the game, on two specific points, and the evidence is the client's own strings and the shipped equations.**

### 3.1 Cunning is the physical-damage attribute

| tag | text (verbatim) |
|---|---|
| `tagCharAttributeDescription01` | *"A **cunning** intellect improves your combat technique, increasing **physical**, pierce, bleed and internal trauma damage. Cunning also increases your capacity for pain, your chances of landing melee and ranged attacks, and critically hitting enemies."* |
| `tagCharStatsPhysicalPercentDmgInfo` | *"The percent bonus to all **Physical** Damage … not including the bonus from **Cunning**."* |
| `tagCharStatsOADescription` | *"**Offensive Ability** … is affected by skills, items, and **Cunning**."* |
| `tagCharAttributeDescription02` | *"**Physical conditioning** gives you the strength to fight in **heavier gear** … Physique also greatly increases your capacity for pain, your ability to regenerate your wounds and the ability to avoid being critically hit."* |
| `tagCharStatsDADescription` | *"**Defensive Ability** … is affected by skills, items, and **Physique**."* |

**Eye of Reckoning on this character is a physical two-hander.** Its damage scales with % Physical (Cunning) and its ability to land and crit scales with Offensive Ability (Cunning). Physique buys equip-gating, health and DA — all of which this character already has in surplus from elsewhere (§ 3.2). **101 of 107 points into Cunning is the allocation the client's own attribute copy recommends for this build.**

### 3.2 Physique was never the constraint — the mastery bars pay for the gear

Equipped weapon: `records/items/gearweapons/melee2h/d107_blunt2h.dbr` (`GDX1.arz`, `WeaponMelee_Mace2h`, `itemClassification = Legendary`, `itemLevel = 84`, `attributeScalePercent = 80.0`, item skill `gutsplosion`).

Its attribute requirement is **not stored as a literal** — `strengthRequirement = 0` on the record. It is computed from `itemCostName = records/game/itemcostformulas_legend.dbr`:

```
melee2hStrengthEquation (GDX1) =
  0.965*(2.79*(itemLevel*6.55)^1.205 - 1.8*(itemLevel*5.84)^1.2785 + ((itemLevel^1.5)*0.0125-1)*-5 + 18)

itemLevel 84  ->  591.9   x attributeScalePercent 80 %  ->  ~473.5 Physique required
```

The character carries **1037 flat / 1327 modified Physique**, decomposed: **50** base · **24** from his 3 attribute points · **480** from the two mastery bars · **410** from the devotion tree · **73** from gear. ⚑ **1013 of it — everything but the attribute points — is there with ZERO points in Physique, against a ≈474 requirement. He could have equipped this weapon twice over without spending one.** That is the mechanical fact gandalf's argument did not have: in Grim Dawn a level-100 dual-mastery character is gear-eligible on mastery-bar attributes alone, which frees the entire attribute budget for the damage stat.

*(The same equation file gives `chestStrengthEquation` ≈ 662 at itemLevel 94 before each piece's own `attributeScalePercent`; I did not compute per-piece scale factors because the weapon case already settles the question and doing so would add arithmetic without adding evidence.)*

### 3.3 The point budget: 107 points at level 100 — plausible, and consistent across three characters

`characterModifierPoints = 1` per level, so levelling alone yields **99** points (verified on Fresh Character 01: level 13, exactly 12 points allocated, `attributePointsUnspent = 0`). The referent has **107**.

⚑ **The 8-point excess is normal, not anomalous.** The two other independent level-100 saves in the control set carry **104** (Ward The Soldier: 40/44/20) and **103** (Hellwrathh: 44/43/16). All three exceed 99 by 4–8. The client confirms the mechanism exists — `tagActionGiveAttributePoint` / `tagActionGiveAttributePoints` are quest-reward action strings — but **the quest data is not in the depot** (only `database/*.arz` and `Text_EN.arc` ship), so I cannot enumerate which quests grant them or what the ceiling is.

**Grade: `searched-SOURCE-UNLOCATED`.** Searched the ARZ archives (all 8) and the localization corpus (20,394 tags); the reward table is not on this host. What *is* established: the mechanism exists, and 107 sits at the top of a 103–107 band observed across three unrelated level-100 characters.

### 3.4 A conflict in the client's own text, reported and not reconciled

| source | claim |
|---|---|
| `playerlevels.dbr` — `strengthIncrement`/`dexterityIncrement`/`intelligenceIncrement` | **8** per point |
| `tagTutorialTip15TextB` / `tagTutorialTip16TextC` | *"…by **8** per point"* / *"increases the attribute by **8**"* |
| ⚑ `tagCharAttributeIncrement01/02/03` | *"Each point increases Cunning / Physique / Spirit by **10**."* |

Three sources say 8, one says 10. **The saves settle it empirically — every attribute on every one of nine saves is `50 + 8n` for integer `n`, with no exceptions** — so the `…Increment0N` tags are stale strings. Recorded because the next reader of those tags deserves to know they are wrong, not because the question is open.

⚑ **A trap worth naming:** those three tags are indexed **01 = Cunning, 02 = Physique, 03 = Spirit** — an internal ordering that is *not* the save's storage order and *not* the character sheet's display order. Anyone deriving a field order from tag indices would land exactly on H2, the refuted hypothesis.

---

## 4 · Q3 — THE BLAST RADIUS

### 4.1 In CODE and in the PACK: measured, and it is ZERO

| target | method | result |
|---|---|---|
| `reincarnated-engine/src/reincarnated/simulation/kc2/**.py` | grep for `physique` / `cunning` / player `spirit` / `attribute` / `character_bio` / `player.gdc` | ⚑ **no hit.** The only `bio` in the package is MONSTER `bio_record` (a creature DBR path, unrelated). The only `spirit` hits are `fighting_spirit` and `spirit_guide`. |
| `fixture.py` `Cited(...)` constants (the pack's citation surface) | full enumeration | **no player attribute constant exists.** `MO_PLAYER_HP_MAX = 20005.0` is `MEASURED` from the sheet/orb, not derived from the bio's 1154. `ENERGY_MAX = 2576.0` is `MEASURED` from the globe, not derived from the bio's 298. |
| `reincarnated-godot` (`*.gd`, `*.json`) | same grep | **no hit** |
| `global_magnitude.py` attribute scaling `(dex/245)+1` / `(int/215)+1` | read | operates on **the board's bodies** (169 records / 344 actors), from `pm4m_body_chain.csv`. **The player is not in that population.** |

⚑ **Nothing the runtime computes moves.** This is the good half of the answer and it bounds the damage: S-1 is a **correction**, not a re-derivation, and it is nothing like the baton-versus-pool roster-basis event.

### 4.2 In C-1's narrative ledger: three corrections, one of which is large

**(a) C-1 § 5.1 — the double-count.**

> *"total Spirit = 237 (base 50 + save-bio 74 + gear `characterIntelligence` 113)"*

The bio's **74 already contains the base 50**. Proven by the three level-1 saves, which read `50 / 50 / 50` against `malepc01.dbr`'s `characterStrength = characterDexterity = characterIntelligence = 50.0`, and by the exact `50 + 8n` structure of every attribute on every sample.

**(b) C-1 § 5.1 — the omission, which is the big one.**

The ledger counted **bio + gear** and stopped. It omitted the **two mastery bars (+194 Intelligence)** and the **devotion tree (+155 Intelligence)**. Corrected:

| | C-1 | **S-1 corrected** |
|---|---|---|
| Spirit, flat | 237 | **536** |
| Spirit, after `characterIntelligenceModifier` +6 % | — | **568** |

Re-running C-1 § 5.1's own arithmetic with **536** substituted for 237, and **changing nothing else**:

```
spirit flat      = 0.01   x 536      =   5.36     (C-1:  2.37)
spirit percent   = 0.26 % x 536      =  139.4 %   (C-1: 61.62 %)

total = base_L100 + 5.36 + 19.7 x (1 + 0.63 + 1.394)
      = base_L100 + 5.36 + 59.53
      = base_L100 + 64.89

MEASURED total (ceremony §D #511)     = 75.37 /s
RESIDUAL                              = 10.48 /s      (C-1 reported 28.75 /s)
```

⚑ **The residual falls from 28.75 /s to ~10.5 /s on the single correction of one input.** With **568** (modifier applied) it falls further, to ~**6.5 /s**. I am **not** choosing between 536 and 568 — whether Grim Dawn's `characterIntelligenceModifier` multiplies the attribute before the regen formula consumes it is not established from any source I hold, and picking the one that closes better is exactly the fit Law 3 forbids. **Both are reported; neither is preferred.**

⚑ **And C-1's gear-and-skill flat term (19.7) and percent term (63 %) are themselves now suspect in the same direction** — my sweep finds `characterManaRegen` 30.3 flat and `characterManaRegenModifier` 118 % across the same allocation. I am **not** substituting those: my sweep is broad where C-1's enumeration was audited row-by-row, and a crude instrument must not overturn a careful one. **What I am asserting is the Spirit number, because it is itemised per record in § 2.2 and each row is individually checkable.** The regen flat/percent terms are flagged for a re-audit, not corrected here.

**(c) ⚑ C-1 § 5.2's stated REASON for refusing the 690 back-solve is factually wrong in both clauses.**

> *"~690 Spirit is not a number a physical two-hander Warlord carries. His base is 50, his gear contributes 113, and **his build dumps attribute points into Physique, not Spirit**."*

- **The build dumps 101 of 107 attribute points into CUNNING.** Physique and Spirit receive 3 points each.
- **Gear is not the only non-bio source.** Mastery bars and devotions contribute more Intelligence than gear does.

⚑ **The refusal was still CORRECT and should stand — but for a different reason than the one given.** The right reason is simply that back-solving a value from the equation it is supposed to explain is circular, regardless of whether the answer looks plausible. The reason C-1 actually gave was a domain claim about the build, and the domain claim was wrong. **This is the sharper lesson than the arithmetic: the refusal was right, the justification was a guess, and a right answer defended by a wrong reason will be overturned by the first person who checks the reason.** The corrected Spirit (536–568) is now within striking distance of 690, which makes the guard *more* necessary, not less.

**(d) C-1 § 5.3 — the base-energy term is wrong by 1536.**

> *"base: `characterMana` 250 + `manaIncrement` 16 × 99 levels = 1834"*

`manaIncrement = 16` is charged **per attribute point spent in Spirit**, not per level. Levelling grants **no energy at all** in this block. Verified exactly, no exceptions, on nine saves:

| character | spirit points | predicted `250 + 16n` | **stored** |
|---|---|---|---|
| EoRWarlGuts | 3 | 298 | **298** ✓ |
| Ward The Soldier | 20 | 570 | **570** ✓ |
| Hellwrathh | 16 | 506 | **506** ✓ |
| Fresh Character 01 (lvl 13) | 0 | 250 | **250** ✓ |
| three level-1 saves | 0 | 250 | **250** ✓ |

The character's stored base energy is **298**, not 1834. ⚑ **Containment: the pack does NOT consume C-1's 1834** — `fixture.py` carries `ENERGY_MAX = Cited(2576.0, …, "MEASURED")`. The error lives in the prose and dies there.

### 4.3 In the PARSERS: no change required

Both `research/scripts/gd_gdc_parse.py` and the g7 scratch parser are **correct as written**. The canonical one's field naming (`physique_stored_float`, …) already avoids claiming these are displayed attributes, which turns out to have been the right instinct. **What should be added is a comment, not a fix:** *"stored = base 50 + 8 per allocated attribute point; mastery bars, devotions and gear are NOT in this block."* That sentence is what C-1 needed and did not have.

---

## 5 · ⚑ THE METHODOLOGICAL FINDING — archive precedence, and a stub that reads clean

`arz` helpers that resolve a record by scanning archives in enumeration order and returning the **first** hit are wrong for any record an expansion overrides. The exemplar is not hypothetical — it is in this commission's own critical path:

| record | `database.arz` | **`GDX2.arz`** |
|---|---|---|
| `records/skills/playerclass09/_classtraining_class09.dbr` | **32-rank STUB** — rank 50 is **out of range**; last value `+64 STR / +56 INT / +256 mana` | **live 100-rank record** — rank 50 = **+250 STR / +125 DEX / +125 INT / +650 mana** |

Oathkeeper did not exist before *Forgotten Gods*; the base archive carries a leftover placeholder under the live record's exact path. ⚑ **A first-hit reader returns the stub, silently, with no error** — and a naive `[rank-1]` index against a 32-entry array either throws (visible) or, with a `min()` clamp, **returns the wrong value cleanly** (invisible). My first ledger run did exactly that and understated the referent's Spirit by 69 and his energy by 394.

**Fourth instance of the shape this run keeps meeting: an instrument that returns cleanly after it stopped answering the question.** The check ran; the check did not pass.

**Correct precedence** (implemented in `scratch/2026-09-21-s1-bio/arz.py`): `database.arz < GDX1.arz < GDX2.arz < GDX3.arz`, **last wins**; SurvivalMode archives layer above that only when the Crucible mod database is in play, and are opt-in rather than default.

**Exposure, stated honestly:** I have **not** audited which prior extractions used first-hit ordering. `research/scripts/gd_arz_adapter_2026_07_24.py` reads a single named archive and is not exposed. `legolas/scratch/2026-08-07-pe1-eor/arzgrep.py` iterates a fixed base→GDX3 list and reports every hit, so it surfaces duplicates rather than hiding them. ⚑ **Any tool that takes the FIRST of several hits on a record that exists in more than one archive is exposed, and that class has not been enumerated.** Routed to elrond as a curation question; recorded here so it is not discovered a third time.

---

## 6 · What did NOT close

| question | state |
|---|---|
| Where the 8 excess attribute points come from | ⚑ **`searched-SOURCE-UNLOCATED`** — quest data absent from the depot; mechanism confirmed by client tags; 107 within a 103–107 band across three level-100 saves |
| Whether `lifeIncrementIntelligence` changed 8 → 12 between the referent's two save vintages | **CONSISTENT-NOT-SOURCED** — the arithmetic closes exactly under that reading on 5 of 5 relevant samples; no patch note held |
| Whether `characterIntelligenceModifier` (+6 %) multiplies Spirit *before* the regen formula consumes it | **UNRESOLVED.** 536 vs 568. Both reported; not chosen. The formula lives in `Game.dll`, still unmounted |
| Whether the corrected pool ledger reproduces `ENERGY_MAX = 2576` | ⚑ **NO — sweep overshoots to 2941.** Reported as a sweep, not asserted. C-1's 2054 was built on a wrong base term; mine is built on an unaudited walk. **Neither is a ledger. This wants a dedicated audit, not a third estimate** |
| Whether C-1's regen flat (19.7) and percent (63 %) terms are complete | **FLAGGED, NOT CORRECTED** — my sweep finds 30.3 / 118 % over the same allocation. A broad instrument must not overturn an audited one; routed back as a re-audit request |

---

## 7 · Source list

**Primary — game files on disk** (`/Users/admin/depots/`, read-only, 8 `.arz` + 7 `Text_EN.arc`, accessed 2026-09-21)
- `records/creatures/pc/playerlevels.dbr` — base, GDX1, GDX2
- `records/creatures/pc/malepc01.dbr`, `femalepc01.dbr` — base, GDX1, GDX2, GDX3
- `records/skills/playerclass01/_classtraining_class01.dbr` — base
- `records/skills/playerclass09/_classtraining_class09.dbr` — ⚑ base (stub) **and** GDX2 (live)
- `records/items/gearweapons/melee2h/d107_blunt2h.dbr` — GDX1
- `records/game/itemcostformulas_legend.dbr` — base, GDX1
- 55 devotion records, 27 class-skill records, 12 equipped items + affix chains — enumerated in `ledger.py` output
- `tags_ui.txt`, `tags_tutorial.txt` (`Text_EN.arc`, base) — `tagCharAttributeDescription01/02/03`, `tagCharAttributeIncrement01/02/03`, `tagCharStatsOADescription`, `tagCharStatsDADescription`, `tagCharStatsPhysicalPercentDmgInfo`, `tagTutorialTip15TextB`, `tagTutorialTip16TextC`, `tagActionGiveAttributePoint(s)`

**Primary — saves** (read-only; 9 distinct sha256, listed § 0)

**Internal**
- `legolas/findings/2026-09-21-c1-off-channel-energy-recovery.md` §§ 5.1–5.3, 10
- `research/scripts/gd_gdc_parse.py`; `legolas/scratch/2026-07-28-gdc-parse-g7/gdc_parse.py`
- `reincarnated-engine/src/reincarnated/simulation/kc2/fixture.py`, `global_magnitude.py`, `micro_oracles.py`
- `gandalf/notes/2026-09-21-the-commission-rule.md`

**Not consulted:** no web source. S-1 required none and none is cited.

---

**Filed by:** legolas (UNKNOWN-RESEARCHER), 2026-09-21. Read-only throughout.
