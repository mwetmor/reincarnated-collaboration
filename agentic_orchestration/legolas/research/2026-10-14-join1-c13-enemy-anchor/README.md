# Research: JOIN-1 C-13 enemy anchor (D2 home endgame ↔ GD waves 151–160), 2026-10-14

**Mode:** A (analytical; primary-source probe) · **Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf, JOIN-1 conductor
**Rulings this serves:** KP-420 (enemy-anchored join, both directions), with scope added by KP-421 (block and hit law), KP-423 (potions) and KP-426 (universal player laws).
**Law:** LoD 1.13 expansion, Hell, players 1, single-player/ladder tables. The data is `fabd/diablo2 @ 45112569`, the J-S7 tables, with their digests re-verified by the generator. Code is from D2MOO `5596f5cb6c52` (a 1.10f reconstruction).
**GD side:** the frozen KC2 oracle, read through its own loaders. Nothing under `reincarnated-engine` was written; `git status` on `simulation/kc2` and `data/kc2` is clean.
**Division of labour:** gamora writes the conversion forms. This packet supplies the data, the pairings and the flags.

## Files

| File | What |
|---|---|
| `d2_enemy_quantities.json` | The D2 population under 4 rules, with per-monster rows and distributions (normal, champion, unique), plus bosses and superuniques |
| `gd_enemy_quantities.json` · `gd_notes.md` | GD w151–160: per (record, wave) cell; REF and BOARD populations; equal-weight and body-weighted |
| `ratio_table.json` | GD/D2 ratios pair by pair, GD role split, hit chance under each game's own law, yard→metre anchors |
| `sorc_defense_sheet.json` | The Sorceress's D2 defensive sheet at clvl 90: two stat profiles, with and without quest bonuses |
| `potions.json` · `potions_notes.md` | Census row 21: D2 potion laws, plus the oracle's Warlord potion, row for row |
| `universal_player_laws.json` · `universal_player_laws_notes.md` | KP-426 universal player laws (see § 9) |
| `scripts/` | `d2_enemy_anchor.py`, `gd_enemy_quantities.py`, `sorc_sheet_and_ratios.py`, `potions_extract.py`, `universal_player_laws.py`. All read-only and all re-runnable |
| `verification_*.log` | Re-run outputs. The D2 and GD JSONs were regenerated **byte-identical** (sha256 `f31a5fab…` and `bf4d7cc3…`) |
| `captures/` | D2MOO sources, plus Basin and Arreat pages, all sha256-listed. Potions and universal-law captures are in sub-folders |

Grades: **DATAMINED** (read from game data) · **MODEL-VERIFIED** (D2MOO code structure plus at least one community source, with tables reproduced) · **INFERRED** · **UNKNOWN**.

---

## Headline

| Pair (GD / D2) | D2 anchor (R1, normal) | GD (BOARD trash, body-weighted) | **Ratio, median [IQR-ratio]** | Grade |
|---|---|---|---|---|
| **HP** | 6,000 [4,829–8,346] | 243k [168k–409k] | **×40.5** [34.8–49.0] | both DATAMINED; ratio INFERRED |
| HP, champion ↔ champion-hero | 11,745 | 448k | ×38.1 | as above |
| **Damage per hit** (pre-mitigation) | 93 [84–129] (melee/attack columns only ⚑) | 8.06k folded [6.86k–9.59k] (779 raw) | **×86.6 folded** (p25/p25 ×82.1, p75/p75 ×74.5) / ×8.4 raw | flagged ⚑ |
| AR ↔ OA (raw numbers) | 4,089 | 2,416 | ×0.59 | **⚑ MISLEADING. Use hit chance (§ 4.2)** |
| Defense ↔ DA (raw numbers) | 1,816 | 2,204 | ×1.21 | **⚑ MISLEADING. Use hit chance** |
| Armour | none on D2 monsters | 915 (70 % absorption) | — | **⚑ NOT A RATIO** |
| Fire resist | median 33, IQR 0–57.5, **12/70 immune** | median 0, p75 25, max 80, **0 immune** | difference, not ratio | **⚑ mechanic** |
| Attack interval | **UNKNOWN** (frame data not in the tables) | swing 0.93 s [0.60–1.10] | — | **⚑ gap** |
| **Enemy hit chance on the kit** | 74 % [71–77] (normal melee vs the Sorceress); champion ≥ 81 % | 86.8 % [83–92] (monster vs the Warlord) | — | each in its own law |

**The asymmetry:** GD's enemies are about **×40 more durable** but about **×87 harder-hitting** than the D2 anchor population, both measured against the same D2 baseline. Two consequences follow.
- One joint scale factor cannot preserve both of a kit's hits-to-kill and its hits-to-die.
- That is exactly why KP-420 anchors each direction separately: gamora's forms need one key for offence and one for defence.

The damage ratio is **biased high**: 55 of the 70 R1 types also carry monster *skills* whose damage this packet does not compute (§ 3.3).

---

## 1. The D2 anchor population (Q1)

### 1.1 The rule, and the alternatives

| Rule | Definition | Areas | Distinct types |
|---|---|---|---|
| **R1 (proposed)** | **Every Hell area at the game's maximum area level, alvl 85** (`Levels.txt MonLvl3Ex == 85`) | 16 (15 populated): Pit 1/2, Mausoleum, Maggot Lair 3, Ancient Tunnels, Sewers 2 (A3), Forgotten Temple, Ruined Fane, Disused Reliquary, River of Flame, **Chaos Sanctum**, **WSK 1–3**, **Throne**, Worldstone Chamber | 70 |
| R2 | Chaos Sanctum only (Id 108) | 1 | 3 trash types + Diablo + 3 seal superuniques |
| R3 | Worldstone Keep 1–3 + Throne (Ids 128–131) | 4 | 36 + Baal |
| R4 | Every Hell area at alvl ≥ 81 | 66 | 327 |

**Why R1 is a rule and not a taste.** alvl 85 is the data's own ceiling: no `Levels.txt` row is higher. It is also the only band where every monster level and treasure class tops out. Both of the C-12 home-frontier candidates already sit there (Chaos Sanctum and Throne, `c12b_home_frontier.md`). R1 is an envelope over every "endgame farm", not a single pick from among them.

**What each alternative moves** (trash HP ratio / damage ratio):

| Rule | HP ratio | Damage ratio | Effect |
|---|---|---|---|
| R1 | ×40.5 | ×86.6 | — |
| R2 | ×29.2 | ×86.6 | Venom Lords and Oblivion Knights are tanky, so the HP ratio falls about 28 %. **Fire: Venom Lord ResFi 130 (immune), Oblivion Knight 60** |
| R3 | ×40.5 | ×74.7 | Same HP as R1, hits a little harder |
| R4 | ×41.4 | ×81.4 | Within 2 % of R1 on HP; immune share similar (64/327 fire) |

**R1 is robust to R3 and R4. R2 is the outlier** because it has only 3 types. Boss pairing: R2 (Diablo plus seals, median D2 22.6k) gives ×87.7 against GD boss/nemesis 1.98M. R3 (Baal 493.7k) gives ×4.0. A one-boss anchor is not a distribution.

### 1.2 Population mechanics
- **Spawn list:** Nightmare and Hell use the `nmon1..25` columns (D2MOO `LevelsTbls.cpp` loads the separate `wNightmareHellMonsters` list). DATAMINED + MODEL-VERIFIED.
- **Weighting:** both are reported. *equal* = one vote per distinct (MonStats Id, alvl). *slot* = weighted by `nmon` slot occurrences across the rule's areas. They differ by under 5 % on every median.
- **players 1:** `MONSTER_GetHpBonus(1) = 0`, so no life bonus. Damage gains +1/16 per extra player in NM/Hell (Basin MonLvl), which is also 0 here.

### 1.3 Gaps in the population
- **Baal's five wave bosses** (Colenzo, Achmel, Bartuc, Ventar, Lister) are **not** rows in `SuperUniques.txt` and are not boss-flagged MonStats rows in 1.13. Their spawn is hard-coded, so they are UNRESOLVED and not in R3. Baal's minions (`baalminion1–3`, Level(H) 92) are identifiable but are not placed in R3.
- **Superunique level** is taken as alvl + 3 (by analogy with uniques, from Basin). INFERRED.

---

## 2. D2 scaling laws (all MODEL-VERIFIED unless marked)

| Law | Statement | Sources |
|---|---|---|
| L1 monster level | Hell expansion: non-boss, non-NoRatio monsters take the area level `MonLvl3Ex`. Boss and NoRatio monsters take `MonStats Level(H)` | D2MOO `Monster.cpp` L197–201; `LevelsTbls.cpp` `GetMonsterLevelInArea` |
| L2 stat scaling | stat = MonStats(H) × `MonLvl[mlvl]` **`L-` column** (H) / 100, integer. NoRatio rows take the raw value | D2MOO `MonsterTbls.cpp` `DATATBLS_CalculateMonsterStatsByLevel` (offset 3 selects the `L-` columns); Basin MonLvl. **The generator asserts MonLvl at levels 85 and 88 against Basin's tables** (L-AC 1651, L-TH 3408, L-HP 6182, L-DM 96 at 85) |
| ⚑ L2b which column set | `L-` = **single-player and ladder**. Non-ladder Battle.net uses the classic columns, which give lower Hell life and defence: **HP ×0.75, AC ×0.85 at level 85** (4637/6182, 1403/1651). Attack rating and damage are the same in all versions | Basin MonLvl ("higher in Hell Ladder and single-player"); D2MOO `nGameType` offset. **This packet uses SP/ladder.** The other set is a one-factor sensitivity |
| L3 champion (Hell) | life +100 % (on base-level life); mlvl +2 for the attack-rating and damage lookup; damage +66 %, AR +49 % (100 and 75 × ChampionDamageBonus 66 / 100) | `MonUMod.txt` constants rows 6, 10, 11; `DifficultyLevels`; D2MOO `UMod2` / `UMod16`; Basin Champion (200 % life in Hell, level +2) |
| L3 unique and minion (Hell) | unique life +100 %, minion life +50 %; level +3. A unique with Extra Strong gets damage +99 % and AR +66 % | `MonUMod` rows 3, 9, 13, 15; D2MOO `UMod2` / `UMod5`; Basin Unique (Hell: 200 % / 150 %; level +3) |
| L4 resists | MonStats `Res*(H)` set as-is. Monsters get **no** Hell penalty; the −100 is the player's | D2MOO `Monster.cpp` (STAT_*RESIST from `nResistances[..][nDifficulty]`); DifficultyLevels `ResistPenalty` |

---

## 3. D2 enemy quantities, R1 at Hell (Q2)

Per-monster rows are in `d2_enemy_quantities.json → rules.R1_alvl85_all.rows`. Each row carries HP min/max, defence, every attack slot (min/max damage and AR), elemental adds with % chance and mode, resists, `aidel`, velocity and run, the skill list, ToBlock, Drain(H) and MonStats2 size and melee range.

| Quantity | Normal (median [IQR], range) | Champion | Unique |
|---|---|---|---|
| HP (mid of min/max) | **6,000** [4,829–8,346], 1,854–27,819 | 11,745 [9,504–16,691] | 11,745 [9,504–16,691] |
| Defence | 1,816 [1,568–1,981] | (same AC; champions get no AC change) | — |
| Damage per attack, best slot (physical mid + expected elemental) | **93** [84–129], 3–598 | 160 [143–220] | 98 [89–136]; 196 with Extra Strong |
| Attack rating, best slot | 4,089 [3,578–5,282] | 6,228 [5,450–8,176] | — |
| `aidel(H)` (AI think delay, frames) | 13 [13–13] | — | — |

**Resists (normal, 70 types), median [IQR], immune ≥ 100:**

| Family | Median [IQR] | Immune |
|---|---|---|
| Physical | 34 [25–50] | 3 |
| Magic | 0 [0–17.5] | 4 |
| **Fire** | **33 [0–57.5]** | **12** |
| Lightning | 33 [16–75] | 17 |
| Cold | 33 [0–69] | 16 |
| Poison | 50 [16–104] | 19 |

**Grades and limits:**
1. **HP, defence, AR, damage and resists are DATAMINED** through MODEL-VERIFIED laws. The expected elemental add (chance × mid) is INFERRED.
2. **Attack and cast RATE is UNKNOWN.** Attack frame counts live in AnimData.d2, which is not in the txt tables. `aidel` is AI think delay, a proxy only. Route: extract AnimData from the 1.13 MPQ, or Basin's per-monster frame tables.
3. **⚑ Monster skill damage is NOT computed.** 55 of 70 R1 types carry `Skill1–8` (for example Venom Lord `MegademonInferno`, Oblivion Knight `DoomKnightMissile` and Bone Spirit, Storm Caster `FingerMageSpider`). The skills are listed per row; their damage needs each skill's Skills.txt monster calculation. **So D2 "damage per hit" here is the melee/attack-column magnitude, and the damage ratio is an upper bound.**

## 4. GD enemy quantities (Q3)

See `gd_notes.md` for full provenance, which oracle functions feed each field, the two populations and the gaps. Headline, body-weighted median [p25–p75]:

| Quantity | BOARD all roles | BOARD trash | BOARD champion-hero | BOARD boss+nemesis | REF all |
|---|---|---|---|---|---|
| HP (oracle LO limb) | 409k [173k–570k] | 243k [168k–409k] | 448k [444k–569k] | 1.98M | 275k [202k–448k] |
| Damage, basic hit, folded | 8.06k [5.84k–10.0k] | 8.06k | 13.5k | 1.75k (physical clamp zeroes some bosses) | 4.4k |
| Damage, max slot, folded | 19.3k [12.1k–25.5k] | 16.3k | 22.6k | 24.5k | 9.8k |
| OA | 2,480 [2,357–2,648] | 2,416 | 2,657 | 2,664 | 2,176 |
| DA | 2,337 [2,186–2,514] | 2,204 | 2,554 | 2,538 | 2,151 |
| Armour (70 % absorption on every cell) | 933 [612–1,308] | 915 | 1,308 | 1,751 | 915 |
| Swing period | 0.93 s [0.60–1.10] | 0.93 | 1.1 | 0.9 | 1.05 |

- **Fire resist:** median 0, p75 25, range −20 to 80; **no cell is ≥ 100** in REF or BOARD.
- **⚑ CONFLICT to carry:** jack-ryan's J4b Gate-1 (INFO-9) reports board `res_fire` spanning **−25…500, with 5 immune (record, wave) pairs** in a **248-pair** population (`trap_lightningspike_hero_a01`, `loghorrean_void`, `beast_bloodpool`). That population is wider than BOARD's 95 cells; those records are trap or auxiliary bodies outside this packet's two populations. **Both statements can be true.** The ratio uses BOARD/REF, and a fire-immune census must use jack-ryan's wider set.

---

## 5. Ratio table and flags (Q4)

Full numbers are in `ratio_table.json → ratios_gd_over_d2` for each rule. Pairing: **GD role ↔ D2 rank** (trash ↔ normal, champion-hero ↔ champion, boss ↔ boss/superunique).

| # | Pair | Ratio (R1) | Label | Flag |
|---|---|---|---|---|
| P1 | HP ↔ HP | ×40.5 [34.8–49.0]; champion ×38.1 | INFERRED (ratio of two DATAMINED distributions) | Use the **LO HP limb** on GD (the oracle's own). L2b moves D2 HP ×0.75 if non-ladder columns are used |
| P2 | Damage per hit ↔ damage per attack | ×86.6 folded / ×8.4 raw | INFERRED | ⚑ (a) D2 omits monster **skill** damage, so the ratio is an upper bound. ⚑ (b) GD "folded" applies the oracle's attribute multiplier (≈4.3–4.8) and was **not** reconciled with `config_of_record.json` (gd_notes gap 4). GD raw (×8.4) is *not* the GD in-game hit; folded is. ⚑ (c) Both are **pre-mitigation** magnitudes |
| P3 | AR ↔ OA | ×0.59 (raw) | ⚑ **MISLEADING** | D2: `CtH = clamp(200·AR/(AR+DEF)·alvl/(alvl+dlvl), 5, 95)`, with an explicit level term. GD: the PTH equation in OA and DA, with crit tiers above 70/90 and floor 55, and no level term. **Map through hit probability** (§ 5.2), not a ratio |
| P4 | Defense ↔ DA | ×1.21 (raw) | ⚑ **MISLEADING** | Same as P3 |
| P5 | (none) ↔ armour | — | ⚑ **NOT A RATIO** | D2 monsters have no armour. Their physical mitigation is `ResDm` (%), and immunity sits at ≥ 100. GD has flat armour (915) with 70 % absorption, plus `res_physical`. Map D2 `ResDm` ↔ GD `res_physical` (both %); GD armour has no D2 counterpart on the monster side |
| P6 | resist ↔ resist | dimensionless; per-family distributions side by side | DATAMINED | ⚑ **Mechanics, not magnitudes:** D2 immunity at ≥ 100 can't be pierced by items. D2's Hell −100 is a *player-side* penalty (it belongs to the defensive sheet). GD has no immunes on BOARD/REF |
| P7 | attack rate ↔ swing period | — | D2 UNKNOWN | ⚑ gap (AnimData) |
| P8 | rank multipliers | champion ×2 life, +66 % damage, +49 % AR (Hell) | MODEL-VERIFIED | GD has no rank multiplier at this grain (heroes are separate records) |

### 5.2 Hit chance expressed in each game's own law (the replacement for P3 and P4)

**D2, monster on the Sorceress** (mlvl 85, clvl 90; her defence mid 1,203–1,280, § 6):
- Normal monsters hit **74 % [71–77]** (min 63, max 86).
- Champions hit **≥ 81 %**. That is a lower bound: AR here is the +49 % only, not re-looked-up at mlvl +2.
- **Then block:** 75 % in the MAXBLOCK profile, 3 % in NODEX.

**GD, monster on the Warlord:** `m2p_p_hit_pct` **86.8 % [83.2–91.6]**, range 77.1–100 (BOARD, body-weighted, `pm4o_oa_da.csv`).

**Kit on enemy:** her Fire Ball and Meteor make **no hit roll** (Missiles `ToHit` empty; J4b H07). The Warlord's PTH against this board is 103.5–124.9, so he never misses (D-L5 packet). **Both kits are effectively certain to hit**, so P3 matters only on the intake side.

---

## 6. The Sorceress's defensive sheet (Q5), clvl 90, LoD 1.13 (`sorc_defense_sheet.json`)

**Gear:** the kit record resolved in the 1.13 tables (J4b § 3): Eschuta's Temper, Spirit Monarch, Chains of Honor, Harlequin Crest (Flickering Flame has no 1.13 row), Magefist, Arachnid Mesh, Mara's Kaleidoscope.

**The record pins no attributes and no Chains of Honor base**, so the sheet is given for two INFERRED stat profiles. In both, Strength goes to the Monarch requirement (156) net of the +27 Strength on items, and the remainder goes to Vitality. 460 points assumes the three Lam Esen quests (445 without).

| | MAXBLOCK (Dex for 75 % block) | NODEX (base Dex) |
|---|---|---|
| Totals (Str / Dex / Vit) | 156 / 337 / 75 | 156 / 32 / 380 |
| **Life** | **394** (364 without quests) | **1,004** (974 without quests) |
| **Defence** (items + Dex/4) | **1,136–1,423** | **1,060–1,347** |
| Defence vs missiles | +250 (Spirit) | +250 |
| **Block chance** | **75 %** standing or walking, **25 % running** | **3 %** |

- **Life law:** 40 + 1/clvl + 2/Vit above base, + Harlequin 1.5/clvl (CharStats LifePerLevel 4/4 and LifePerVitality 8/4; Basin Life class table: Sorceress +1/level, +2/Vit). MODEL-VERIFIED. Battle Orders/CTA and life charms are unpinned and excluded.
- **Defence items** (base range × ED + flat):
  - Spirit Monarch 133–148 (a runeword base has no ED);
  - Shako 98–141;
  - Magefist 20–24;
  - Arachnid 104–136;
  - **Chains of Honor on Archon Plate 697–890. That base is a reference choice, not pinned.** Dusk Shroud gives 613–793.
  - Defence = item sum + Dex/4 (Basin Defense). MODEL-VERIFIED.
- **Resists after the Hell −100**, cap 75:
  - Chains of Honor 50 + Um 15 = 65;
  - Mara 20–30;
  - **Spirit's runes in a shield: Tal poison 35, Thul cold 35, Ort lightning 35. No fire.**
  - So **Fire −15…−5** (or **+15…+25** with the three Anya scrolls, +30), and **cold, lightning and poison 20…30** (50…60 with the scrolls). DATAMINED.
- **Damage Reduced 18 %:** Harlequin 10 + Ber 8; player cap 50. **Magic absorb 3–8** (Spirit).
- **Block law (KP-421 Q1):** `min(75, (BlockFactor + shield block + item block) × (Dex − 15) / (2·clvl))`, then **÷3 while running**, after the cap.
  - BlockFactor Sorceress = 20 (CharStats), Monarch block = 22 (Armor.txt), so the base is 42.
  - **75 % needs Dex 337 at clvl 90.**
  - Sources: D2MOO `Units.cpp` `UNITS_GetBlockRate` (expansion branch) and `SUnitDmg.cpp` `ApplyBlockOrDodge` (÷3 when in moving mode and not walking); Basin Block (same formula, class table +20 for the Sorceress, 25 % maximum while running). MODEL-VERIFIED.
- **FBR:** none pinned, so 0, giving a block animation of **9 ticks (0.36 s)** (animation packet § 3.4, COMMUNITY-VERIFIED). D2MOO also gates the block *animation* on `frame − lastblock > FBR/8 + 15` (`SUnitDmg.cpp` L2005).

---

## 7. Block and hit law for the intake (KP-421)

1. **Block chance law:** see § 6 (MODEL-VERIFIED, D2MOO plus Basin). The cap of 75 applies before the running ÷3. The class factor comes from CharStats `BlockFactor`: Amazon, Assassin and Barbarian 25; Paladin 30; Druid, Necromancer and Sorceress 20. Item "Increased Chance of Blocking" adds to the base before the Dex term (Basin). Classic (non-expansion) block drops the Dex/clvl term (D2MOO `bExpansion`; Basin table).
2. **A block fully negates the hit.** Block sets `DAMAGERESULTFLAG_BLOCK` and **clears `SUCCESSFULHIT`**: no damage and no on-hit modifiers (`SUnitDmg.cpp` `GetResultFlags`; Basin: "prevents damage and other modifiers"; it does not stop missile pierce). MODEL-VERIFIED.
3. **Block eligibility by attack kind:**
   - **Melee:** always eligible (`GetResultFlags` → `ApplyBlockOrDodge(.., bBlock = 1)`).
   - **Missiles:** eligible **only if the missile carries physical damage** (`MissMode.cpp` L4707: `ApplyBlockOrDodge(.., pDamage->dwPhysDamage != 0)`). Pure elemental or magic missiles and spells **cannot be blocked**.
   - **Non-missile area spells:** do not reach this path, so they are not blockable.
   - Basin agrees: blockable = melee, arrows, bolts, javelins, thrown weapons, "missiles applying physical damage", plus three named death explosions; not blockable = Lightning Bolt, Tornado radial, Armageddon, Corpse Explosion, charging Claw Vipers and Reanimated Horde.
   - MODEL-VERIFIED. **Mapping rule for gamora:** a GD slot is blockable iff it is a melee swing, or a projectile with a non-zero physical component. Area pulses, auras and pure-elemental projectiles are never blockable.
4. **Monster-vs-player hit law:**
   - `CtH = clamp(2·mlvl·⌊100·AR/(AR+Def)⌋ / (mlvl + clvl), 5, 95)`, integer.
   - Monster AR = attack TH (from MonStats/MonLvl) + 5·Dex + tohit, × (1 + tohit %) (the champion +49 % enters here).
   - Defender defence includes the vs-melee or vs-missile bonus (Spirit +250 vs missiles).
   - **A running player is hit without a roll** (melee `GetResultFlags`: `PLRMODE_RUN` gives an automatic hit).
   - **Monster spells skip the roll:** a missile rolls to hit only if `Missiles.txt ToHit` is set. That is **71 of 684 missiles**, the physical projectiles (arrows, javelins, spikes, throwing weapons). Every caster missile (MegademonInferno, FingerMageSpider, the fireballs, Bone Spirit) is auto-hit.
   - Sources: D2MOO `SUNITDMG_IsHitSuccessful`; `MissMode.cpp` L5058–5066; Basin Attack (formula, 5/95 clamp, running exemption; monster Charge auto-hits); J4a F05. MODEL-VERIFIED.

## 8. Potions (KP-423, census row 21)

See `potions_notes.md` and `potions.json`. In brief (MODEL-VERIFIED unless marked):

- **Health potions:** Minor 30 / Light 60 / Regular 100 / Greater 180 / Super **320 HP over 256 frames (10.24 s)**.
- **Mana potions:** 40 / 80 / 160 / 300 / 500, each over 128 frames.
- **Rejuvenation:** 35 % of life and mana, instant. **Full Rejuvenation:** 100 %, instant.
- **Sorceress class factor:** health ×1.0, **mana ×2.0**.
- **Double fill:** a Vitality-based (Energy for mana) chance to double the fill.
- **Second potion:** totals add, the rate never rises.
- **Interaction (INFERRED, by absence in code):** no cast interruption, not cancelled by hits, no cooldown.
- **Belt:** Arachnid Mesh (Spiderweb Sash) = **16 slots (4×4)**, bottom row hotkeyed. ⚑ Belts.txt is absent from the 1.13 mirror, so this rests on Armor.txt belt type 6 plus Arreat and Basin.
- **GD Warlord, as the oracle carries it:** Tonic of Mending gives **800 + 25 % max HP instant + 25 % over time**, with a 12 s cooldown and 1 charge. At max HP 20,005 that is 10,802 HP (54 %) per drink. The over-time duration is MEASURED-ABSENT; the oracle spreads it over 12 s.

The row-for-row table is in `potions_notes.md`.

## 9. Universal player laws (KP-426)

See `universal_player_laws_notes.md` and `universal_player_laws.json`. The section is filled from that fork's output; the summary is appended below at commit time.

## 10. Yard → metre key (jack-ryan routed item)

| Anchor (both games state it in-world?) | m per yd | Grade |
|---|---|---|
| Literal yard | **0.9144** | definitional; neither game states it in-world |
| Body radius: GD human actorRadius 0.38–0.40 m (`pm4_body_radii.csv`) ↔ D2 player footprint `COLLISION_UNIT_SIZE_SMALL` = 1 subtile = 2/3 yd, half-width 1/3 yd (D2MOO `Units.cpp` `GetUnitSizeX`) | **1.17** | INFERRED (treats the D2 footprint as a diameter) |
| Melee reach: GD `meleeTargetDistance` 2.4 m ↔ D2 reach = weapon melee range + 1 subtile (`IsInMeleeRange`), taken as about 3 subtiles = 2 yd | **1.2** | INFERRED (D2 reach depends on the weapon's range adder) |
| Run speed: GD Warlord moving 4.55 m/s (pilot measurement, geared) ↔ D2 base run 9 yd/s (CharStats RunVelocity as Basin reads it) | 0.51 | INFERRED, weakest (geared against base) |

**Sensitivity set:** {0.67, **0.9144**, 1.0, 1.17, 1.2, 1.5}. The radii in metres at each value are in `ratio_table.json → yard_metre_anchors.radii_in_metres`; for example Fire Ball 2⅔ yd becomes 1.79 / 2.44 / 2.67 / 3.12 / 3.20 / 4.00 m. **The arena margin at each value needs a sim run with enemy density, so it is gamora's to print.** The two in-world anchors (body and reach) agree at about 1.2, and the literal yard is 0.9144.

---

## 11. Open items (named, not guessed)
1. **D2 monster skill damage** (55/70 types): compute each skill's Skills.txt monster calculation. This is the biggest open term in P2.
2. **D2 attack rate:** AnimData.d2 from the 1.13 MPQ (not on disk).
3. **Baal wave bosses:** hard-coded spawns, unresolved.
4. **GD folded damage** is not reconciled with `config_of_record.json` (gd_notes gap 4).
5. **Chains of Honor base and the Sorceress's attributes** are unpinned. Both profiles are given.
6. **L2b (SP/ladder against non-ladder columns)** is a named choice: SP/ladder.

## Sources (accessed 2026-10-14)
- **DATAMINED:** fabd/diablo2 @ 45112569 `code/d2_113_data`: MonStats, MonLvl, Levels, DifficultyLevels (J-S7 pins re-verified by the script), MonUMod, SuperUniques, MonStats2, Missiles, Armor, Runes, Gems, UniqueItems, CharStats. Potions: Misc.txt, fetched at the pin.
- **D2MOO @ 5596f5cb6c52** (1.10f), captured in `captures/`: `MonsterTbls.cpp`, `LevelsTbls.cpp`, `Monster.cpp`, `MonsterUnique.cpp`, `Monsters.cpp` (D2Common), `Units.cpp`, `SUnitDmg.cpp`, `MissMode.cpp`, `Missiles.cpp`.
- **Basin wiki** (action=raw, `captures/basin-*`): MonLvl, Champion, Unique (monster), Block, Defense, Attack, Life, Mana, Dexterity, Vitality, Faster Block Rate.
- **Prior packets:** J4a (F05, F06, F07, F12, F13), J4b (H07, H09, § 3 loadout), the animation packet (§ 3.4 FBR, § 3.7 movement), C-12b, D-L5 (`2026-10-08-gd-crit-roll-rule-dl5`), and jack-ryan's J4b adapter Gate-1 (INFO-9, the yard→metre item).
- **GD:** the KC2 oracle loaders and `data/kc2/*`, digests in `gd_enemy_quantities.json → inputs_sha256`.
