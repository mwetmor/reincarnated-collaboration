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
| ~~**Damage per hit** (pre-mitigation)~~ **SUPERSEDED: r_DMG of record = ×97.1 [85.9–110.4] (§ 12.4, stage 5)** | 93 [84–129] (melee/attack columns only ⚑) | 8.06k folded [6.86k–9.59k] (779 raw) | **×86.6 folded** (p25/p25 ×82.1, p75/p75 ×74.5) / ×8.4 raw | flagged ⚑ |
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

> **⚑ Conductor defaults, KP-428 (2026-10-14):**
> - **Allocation: NODEX is the default.** MAXBLOCK is a sensitivity.
> - **The Anya scrolls are done** (the "quests" columns: 460 stat points, resists +30).
> - **Chains of Honor sits on Archon Plate.**
> - **The Barbarian's belt is 16 slots.**
>
> So the **default sheet** is NODEX_quests:
> - **life 1,004**;
> - **defence 1,060–1,347** (+250 vs missiles);
> - **block 3 %**;
> - **resists after the Hell penalty: fire +15…+25, cold/lightning/poison 50…60**;
> - Damage Reduced 18 %.
>
> MAXBLOCK_quests (life 394, block 75 %, 25 % running) is the sensitivity.

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

See `universal_player_laws_notes.md` and `universal_player_laws.json`; `scripts/universal_player_laws.py` regenerates the JSON byte-identical and asserts the table values against a second source. Rows apply to both D2 kits. MODEL-VERIFIED unless marked.

| Row | Law |
|---|---|
| Stun | Capped at **250 frames (10 s)**; not scaled by difficulty. Players are not incapacitated, but any hit during a stun forces hit recovery. The newest stun replaces the old one |
| Freeze | **Players have no frozen state**: freeze length and Freezes Target become chill. **Cannot Be Frozen** zeroes cold and freeze length; **Half Freeze Duration** halves it once and does not stack |
| Hell divisor | The Hell /4 cold and freeze divisors (DifficultyLevels) apply **only when a monster is the target**. For players, the Hell −100 resist penalty enters the length calculation, so an under-resisted player is chilled up to about twice as long |
| Knockback | Puts the player into hit recovery. **Distance is partial and conflicted:** Basin says up to 3 subtiles; D2MOO sets path distance 5 in unknown units |
| Immobilize | **No root effect for players.** Slows add together, floored at 25 % movement speed and 15 % attack rate |
| Chill | **−50 % movement speed and attack rate.** **Casting, block speed and hit-recovery speed are NOT slowed** (those read only FCR/FBR/FHR). Whirlwind is slowed (INFERRED). Length = cold length × (100 − effective cold resist)/100, effective resist including the Hell penalty, capped at 75 (95 with max-res items). A new chill only extends the remaining time |
| Poison | **A new poison replaces the current one only if its per-frame rate is equal or higher.** Length × (100 − PLR_eff)/100, with PLR_eff including the Hell −100 penalty, clamped −100 to 75. **Poison cannot kill a player** (life floored at 1). Burn follows the same replace rule (INFERRED, code only) |
| Stamina | Drain **40/256 per run frame (3.906/s)**, the same for both classes, × body-armour speed factor, outside town only. At 0, running becomes walking. Regen: full in 10.24 s standing, 20.48 s walking, none while running, attacking or casting (code only: partial). **Base: Sorceress 74 + (clvl − 1) + (Vit − 10); Barbarian 92 + (clvl − 1) + (Vit − 25)**; item Vitality counts |
| Mana regen (Barbarian) | **Identical to the Sorceress's H09 law.** CharStats ManaRegen = 120 for both, about 120 s from empty to full. This closes the J4a F12 open item |
| Life regen | **None naturally for players.** Replenish Life +N heals **N × 25/256 life per second** and keeps working while poisoned |
| Barbarian belt | **`d2-ww-barb.json` names no belt**, so the count is a **conductor default.** Reference (checked against Arreat): no belt 4 slots; normal belts 8 / 12 / 16; every exceptional and elite belt 16 |

Gaps: the code is 1.10f, and no source shows a 1.13 change. Knockback distance is unresolved. Stamina regen and burn rest on one source. Belts.txt is not in the 1.13 mirror, so the belt table uses a D2R index that matches Arreat on all 7 bases checked. Out of scope but noticed: D2MOO's hit-recovery threshold varies by attack type, which conflicts with the community "1/12 of max life" rule.

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

---

## 12. KP-428 follow-up: r_DMG (stage 3 = D2 skill damage; stage 4 = GD reconcile + bound r_DMG)

### 12.1 D2 monster skill damage (done) — `d2_skill_damage.json`, `scripts/d2_skill_damage.py`, `verification_skill_damage.log`

**Laws** (D2MOO, captured in `captures/`):
- Skill level = MonStats `SkNlvl` + Hell `MonsterSkillBonus` 7 (`Monster.cpp` L246–262).
- Level brackets: levels 2–8, 9–16, 17–22, 23–28 and 29+ (`D2Skills.cpp` L2459).
- Skill damage: phys and elemental = (base + bracket) << HitShift, plus SrcDam/128 × owner weapon damage (`D2Skills.cpp` L2490–2717).
- Missile damage: the missile's own damage when `Missiles.Skill` is blank, otherwise the named skill's (`Missile.cpp` L466–760, L1001+).
- DoomKnightMissile: `srvdo148` = srvmissilea + the monster's random component, which gives `undeadmissile1–4` (`SkillMonst.cpp` L2119).

Grade: **structure MODEL-VERIFIED (code); per-skill values INFERRED (computed; no second numeric source found).**

**Declared choices:**
- **Streams excluded from per-hit; their per-second rate is reported:** Infernos, Firewalls, Blizzard, Mosquito, Regurgitator.
- **Not hit damage:** Blood Mana and Healing Vortex are declared non-damaging.
- **Poison is a DoT:** excluded from per-hit.
- **Doom Knight missile:** equal weight over its three hit variants.
- **Imp charged bolt:** HitShift is blank (0), so its value is 0.1 per hit. Flagged UNVERIFIED.

**Use weighting:** D2 monster AI picks attacks through per-AI code (`aip*` parameters), so a general use frequency cannot be derived from data. Two figures are reported instead:
- **best** = the worst-case attack;
- **mean** = equal weight per damaging attack.

**Result: adding skills barely moves the D2 side.**

| Rule | Melee best | Best attack incl. skills | Mean of damaging attacks |
|---|---|---|---|
| R1 | 93 | **97 [84–135]** | 95 |
| R2 | 93 | 116 | 98 |
| R3 | 108 | 110 | 103 |
| R4 | 99 | 106 | 96 |

27 of 70 R1 types have a damaging skill hit; 10 have a stream skill. Most of the 55 skill-bearing types carry utility skills (raise, curse, teleport, nest).

### 12.2 GD side: reconciled (stage 4). ⚑ Its FIGURES are superseded by § 12.4; the damage-path table stands

Files: `gd_damage_reconcile.json` and `scripts/gd_damage_reconcile.py`. The script was written by the GD fork; **I reviewed it and re-ran it.** The re-run is identical except the `wall_s` timer (4.9 against 5.0), and engine `simulation/kc2` and `data/kc2` are untouched.

**What the sealed referent applies is neither "folded" (a × om) nor raw.** It is the GD Game.dll composition, applied per instant row before player mitigation:

| Step | Term | Oracle location |
|---|---|---|
| 1 | `om` = offense fold `mult_for(kind, type)`: the wave and Ultimate damage pool | `threat.py:2038` |
| 2 | `a_mult, t_mult, own_add` = global-magnitude multipliers: the attribute term, Dex for Physical/Pierce and Int otherwise | `threat.py:2076` |
| 3 | C-11a attribute-scope correction to `a_mult` | `threat.py:2082` |
| 4 | `om += own_add`: the body's own total-damage passives join the **same additive pool** | `threat.py:2083` |
| 5 | `om += mutators.pct_add(r)`: Brutal/Corrupted +50 % on instant Pierce/Chaos | `threat.py:2101` |
| 6 | `_im = CompositionFold.instant(...)`: **`m × max(0, a_mult + (om − 1))`**, plus a wave physical term on Physical/Pierce (restoring the clamp at charLevel ≥ 101) | `threat.py:2230`; `gd_composition.py:130–150` (L143 / L147 / L150) |
| 7 | `mitigate(_im × mult, type)`, then `direct += applied × n_volley × band_scale` | `threat.py:2232`, `2235` |

- **The attribute term is ADDITIVE with the pool, not multiplicative.** That is why the stage-1 "folded" (a × om) was the wrong form.
- **But the record also carries terms stage 1 omitted:** weapon-swing rows, Brutal/Corrupted flat rows (85 Pierce and 85 Chaos), the wave physical term and C-11b.
- **Net result: on the same cells, record ÷ stage-1 folded = ×2.02 [1.65–2.10]** (30 cells).
- Configuration: the v3.11 driver's V311-FULL composition, arm M0, which `config_of_record.json` marks "THE CONTROL — the model of record". Crit adds ×1.0005 at the board PTH (sealed d100 law). Non-health, DoT, leech and %-current-life rows are excluded and counted (335 of 1,250 dynamic hits carry %-current-life).

**Ablation ladder** (trash, basic swing, body-weighted median):

| Step | Value |
|---|---|
| A0, prior form | 22.4k |
| + C-11b | 24.3k |
| + C-11a | 24.3k |
| **+ composition (GD form)** | **13.7k** |
| + Brutal/Corrupted (= the V311-FULL record) | **16.0k** |

**GD trash per hit, BOARD body-weighted:**

| Instrument | Median [IQR] | Population |
|---|---|---|
| **Static record, max slot** | **9,610 [6,219–15,981]** | 43 cells, 112 bodies. **PRIMARY**: like-for-like with D2's best attack |
| Static record, basic swing | 15,981 [14,562–16,449] | only the 16 cells (55 bodies) that have a basic weapon swing |
| Dynamic, per landed hit, weighted by the oracle's own slot choice | 5,609 [2,941–10,795] | 1 salt, arm M0, 425 trash hits. Slot mix: basic 189, special2 69, special1 58, tree attack 45, initial 42 |

Why dynamic sits below static: it weights by **use** (frequent cheap basic swings and specials), while static takes each cell's **maximum** slot. It is also one salt over the line-up's bodies, not the board's. **Neither instrument is wrong; they answer different weightings.** Dynamic pairs with D2's mean attack; static max slot pairs with D2's best attack.

### 12.3 r_DMG, bound at stage 4 (`c81376a83`). ⚑ SUPERSEDED by § 12.4: primary ×98.9 → ×97.1; basic-swing ×164.4 → ×79.0; use-weighted ×58.9 → ×47.0

**r_DMG = GD static record max slot (trash) ÷ D2 best attack including skills (normal).** This pairs like r_HP.

| Rule | **r_DMG primary [IQR ratio p25/p25 – p75/p75]** | Sens: mean attack (static ÷ D2 mean) | Sens: use-weighted (dynamic ÷ D2 mean) | Sens: basic swing ÷ D2 best |
|---|---|---|---|---|
| **R1** | **×98.9 [74.5–118.2]** | ×100.9 | ×58.9 [40.1–95.6] | ×164.4 |
| R2 | ×83.1 [62.4–133.1] | ×98.3 | ×57.4 | ×138.2 |
| R3 | ×87.6 [76.8–100.9] | ×93.0 | ×54.3 | ×145.6 |
| R4 | ×91.1 [77.7–121.1] | ×100.1 | ×58.4 | ×151.5 |

Grades: GD per-cell values are DATAMINED inputs through the oracle's own MODEL-VERIFIED composition. D2 values are INFERRED (computed through code laws). **The ratio is INFERRED.**

**With r_HP ×40.5, the anchored asymmetry is about 2.4:1 at R1** (GD enemies hit about 99× harder against about 40× more durable). Under the use-weighted sensitivity it is about 1.5:1.

**Baal's hard-coded waves:** not attempted (optional).

### 12.4 Stage 5: engine-native figures of record (supersede the stage-4 numbers in §§ 12.2–12.3)

**What happened.** The GD fork kept running after `c81376a83`. It then rewrote `gd_damage_reconcile.json` and `scripts/gd_damage_reconcile.py` (the 6-line diff adds `engine_head` and a `HEADLINE` field) and added `gd_damage_reconcile_notes.md`. Both edits are **reviewed and committed here**. I re-ran the final script: the output is identical except the wall-clock field and the per-hit `engine_id` (an object memory address); the 957 dynamic hits match field for field otherwise. Engine `simulation/kc2` and `data/kc2` are untouched.

**Which figures are of record, and why.**
- **ENGINE-NATIVE E5** (`engine_native_static_summaries`) is of record. Every board and line-up slot is composed with the salt-0 M0 run's **own** per-wave `ThreatEngine` folds, the same objects that resolved the hits. It is **cross-checked against the dynamic capture: 684 of 688 non-granted hits are exact**; the 4 misses are chance-gated rows.
- **The stage-4 `static_summaries` is SUPERSEDED (audit only).** It was a reconstruction from a re-loaded roster, without the run's winner-surface, fire-range and self-cast loaders, so it did not reproduce the engine's profiles. Its trash basic median of 15,981 is about 2× the engine's 7,683.
- **The dynamic figure is also re-captured.** It is now taken at `CompositionFold.instant`, not at `mitigate`, which is shared by leech and Vitality rows. That gives 309 trash hits, against stage 4's 425.

**GD trash per hit, BOARD body-weighted, 47 cells / 123 bodies (E5 = record):**

| Instrument | Median [IQR] (min–max) |
|---|---|
| **Max slot (PRIMARY)** | **9,435 [7,175–14,927]** (4,632–24,580). Stage 4 had 9,610 |
| Basic slot | 7,683 [6,178–14,927]. Stage 4 had 15,981 (superseded) |
| Mean damaging slot | 7,481 [6,003–9,947] |
| Use-weighted, dynamic (1 salt) | 4,472 [2,851–5,609], 309 hits; chthonianservitor_b01 alone lands 100 |

The derivation ladder (E0 → E5) and the line-up-weighted figures are in `gd_damage_reconcile_notes.md` §§ 3–4. Notably, **E5 ÷ the stage-1 "folded" form is ×0.656 on max slot**: the composition step alone multiplies by ×0.555, and Brutal/Corrupted adds ×1.171.

**r_DMG of record** (`r_dmg.json`, `verification_r_dmg.log`); the D2 side is unchanged from stage 3:

| Rule | **r_DMG primary = E5 max slot ÷ D2 best [IQR ratio]** | E5 max slot ÷ D2 mean | E5 mean ÷ D2 mean | Use-weighted ÷ D2 mean | E5 basic ÷ D2 best |
|---|---|---|---|---|---|
| **R1** | **×97.1 [85.9–110.4]** | ×99.1 | ×78.6 | ×47.0 [38.9–49.7] | ×79.0 |
| R2 | ×81.6 [72.1–124.3] | ×96.5 | ×76.6 | ×45.8 | ×66.4 |
| R3 | ×86.0 [88.6–94.3]* | ×91.3 | ×72.4 | ×43.3 | ×70.0 |
| R4 | ×89.4 [89.7–113.1]* | ×98.3 | ×77.9 | ×46.6 | ×72.8 |

\* The IQR is a ratio of quartiles (p25/p25, p75/p75), so it need not bracket the median ratio.

**Do any conclusions change?**
- **The primary r_DMG barely moves** (×98.9 → ×97.1). **The 2.4:1 asymmetry against r_HP ×40.5 stands** (97.1 / 40.5 = 2.40).
- **The use-weighted variant moves down** (×58.9 → ×47.0), so the asymmetry under use weighting is **about 1.16:1**, not 1.5:1. Weighted by how often the oracle actually swings each slot, GD's damage scale is close to its HP scale.
- **The basic-swing variant flips** from ×164.4 to ×79.0. It now sits below the primary, as a basic swing should.

---

## 13. Stage 6 (KP-431): D2 monster attack rating and hit chance against the NODEX Sorceress, R1

Files: `d2_hit_chance_r1.json` (per-type rows, each with every attack), `scripts/d2_hit_chance_r1.py`, `verification_hit_chance.log`. This serves gamora's L-24 quantile matching, which is rank-preserving per role pair.

**Defender:** the KP-428 default sheet NODEX_quests: Defence 1,060 / **1,203** / 1,347, plus **+250 against missiles** (Spirit), clvl 90.

**Attacker:** R1 normal monsters, monster level = alvl 85, players 1.

### Laws

| Id | Law | Grade |
|---|---|---|
| H1 | `CtH = clamp(2·alvl·⌊100·AR/(AR+Def)⌋/(alvl+dlvl), 5, 95)`, integer arithmetic. Sources: D2MOO `SUNITDMG_IsHitSuccessful`; Basin Attack; J4a F05 | MODEL-VERIFIED |
| H2 | AR per slot = MonStats `A1TH/A2TH/S1TH(H)` × MonLvl `L-TH(H)` / 100 | DATAMINED via MODEL-VERIFIED scaling |
| H3 | Defence: melee rolls against Defence; a missile rolls against Defence + the vs-missile bonus | MODEL-VERIFIED |
| H4 | A missile rolls only if `Missiles.txt ToHit` is set; otherwise it **auto-hits (100 %, no clamp)** | MODEL-VERIFIED |

**Not folded into the figures:** H5 (melee hits a *running* Sorceress without a roll) and block (3 % on NODEX, which applies after a successful roll). Both are noted only.

### Role per attack (DATAMINED flags)

| Role | Rule |
|---|---|
| **melee** | An A1/A2/S1 slot with no `MissA1/MissA2/MissS1` missile, even on a `rangedtype` monster |
| **ranged-physical** | A slot that fires a missile with `ToHit` set (archers' arrows, blowguns) |
| **caster** | A slot whose missile has no `ToHit`, and every damaging monster **skill** hit from stage 3 (`d2_skill_damage.json`). Auto-hit |

A type's role is the role of its **highest-damage** attack.

### Results

Defence mid; median [p25–p75] (min–max):

| Role | Types | Attacks | Attack AR | Hit % per attack | Hit % at def lo / hi | **Hit % per type (best attack), equal** | Champion (def mid) |
|---|---|---|---|---|---|---|---|
| **melee** | 57 | 91 | 4,089 [3,578–5,112] (2,385–11,382) | 74 [71–77] (64–87) | 76 / 72 | **74 [71–78] (64–87)** | ≥ 81 |
| **ranged-physical** | 3 | 3 | 5,112 [4,430–5,112] | 74 [71.5–74] (69–74) | 76 / 73 | **74 [71.5–74] (69–74)** | ≥ 81 |
| **caster** | 6 | 36 | — | **100** | 100 | **100** | 100 |
| all | 66 | 130 | 4,089 [3,578–5,112] | 76 [72–100] | 78 / 74 | 74 [71–78] (64–100) | ≥ 83 |

- **The slot-weighted (spawn-slot) variant** gives melee 74 [72–78] (64–87). That is the same weighting as r_HP's slot variant; the equal-per-type figure matches r_HP's primary.
- **The D2 melee spread to preserve:** IQR 7 points (71–78), range 23 points (64–87). gamora's linear form had compressed it to IQR 3 / range 7.
- **Champion figures are a lower bound:** AR ×1.49 at alvl+2, applied through the level term only; the attack rating is not re-looked-up at the higher level.
- **Missiles roll against a higher defence** (+250 from Spirit), which is why ranged-physical sits about 0–3 points below melee at the same AR.

### Gaps
- **4 R1 types have no per-slot attack in this table:** `fetishshaman8` (stream-only inferno) and `skmage_ltng4`, `skmage_ltng6`, `skmage_pois6` (their A1 fires a Missiles.txt missile with no ToHit, and the damage is not computed). **They are casters, so they auto-hit**; for role counts, casters are 10 types.
- **Grades:** AR is DATAMINED; hit chance is computed (INFERRED) through MODEL-VERIFIED laws; the role split is DATAMINED flags plus H4.

---

## 14. Stage 7 (KP-432, gamora ADDENDUM-6): mean ÷ mean r_DMG, and the D2 unique attack rating

Files: `d2_unique_ar_r1.json`, `scripts/d2_unique_ar_r1.py`, `verification_unique_ar.log`.

### 14.1 Mean ÷ mean r_DMG (now the primary)

The ratio is GD engine-native E5 mean damaging slot (trash, body-weighted: 7,481 [6,003–9,947]) over the D2 mean of damaging attacks including skills (normal, equal per type).

| Rule | **r_DMG, mean ÷ mean** | IQR ratio (p25/p25 – p75/p75) |
|---|---|---|
| **R1** | **×78.58** | 81.9 – 88.1 |
| R2 | **×76.56** | 72.2 – 89.5 |
| R3 | **×72.38** | 87.6 – 82.9 |
| R4 | **×77.93** | 80.9 – 85.2 |

- R1 reproduces the KP-432 figure (×78.58).
- The IQR is a ratio of quartiles, so it need not bracket the median.
- Grade: INFERRED (the ratio of a GD figure composed by the oracle's MODEL-VERIFIED path and an INFERRED D2 figure).

### 14.2 D2 unique / superunique / boss attack rating, R1 areas, Hell, players 1

Defender: NODEX, Defence 1,203 melee and 1,453 against missiles; clvl 90.

**Laws:**
- **U1:** unique and minion level is +3, and that level selects the MonLvl attack-rating row. Sources: Basin Unique (monster), and D2MOO `UMod4_LevelBonus`. MODEL-VERIFIED.
- **U2:** Extra Strong, if rolled, gives a unique **+66 % to-hit** (MonUMod[13] 100 × ChampionDamageBonus 66/100) and a minion +33 % (MonUMod[12] 50 × 0.66). Sources: D2MOO `UMod5_Strong`; asserted in the script. MODEL-VERIFIED.
- **U3:** superunique level = alvl + 3, INFERRED. Fixed mods come from SuperUniques.txt (Mod 5 = Extra Strong).
- **Not modelled:** Hell's three random unique bonuses (Basin). **Both arms are given** (no Extra Strong / Extra Strong).
- **U4:** bosses use MonStats `Level(H)`.
- **Casters auto-hit,** as in stage 6.

**Uniques built on R1 types** (64 types with a rolling attack; 10 caster types auto-hit at 100 %):

| Quantity | Median [IQR] (min–max) |
|---|---|
| Attack AR, unique | 4,226 [3,698–5,283] (2,465–11,763) |
| Attack AR, unique with Extra Strong | 7,015 [6,138–8,769] (4,091–19,526) |
| **Hit % per type (best attack), unique** | **76 [74–80.25] (66–88)**; melee 76 [74–81], ranged-physical 77 |
| **Hit % per type, unique with Extra Strong** | **84 [82–87] (76–92)** |
| (for comparison) normal, same types | 74 [71–78] (64–87) |

Minions use the unique attack rating (+3 levels); with Strong they get +33 % to-hit. Per-attack rows are in `rows`.

**Named superuniques and bosses** (best rolling attack):

| Name (class) | Level | Fixed mods | AR | **Hit % melee / vs missile defence** |
|---|---|---|---|---|
| Grand Vizier of Chaos (`fingermage3`) | 88 | Extra Strong (5), 9 | 7,015 | **84 / 81** |
| Lord De Seis (`doomknight3`) | 88 | Extra Strong (5), 30, 24 | 9,354 | **87 / 85** |
| Infector of Souls (`megademon3`) | 88 | 6, 27 (no Strong) | 5,635 | **81 / 78** |
| Diablo (boss) | 94 | — | 8,062 | **88 / 85** |
| Baal (`baalcrab`, boss) | 99 | — | 9,850 | **93 / 91** |

The boss rows are the melee roll only. **Most boss and superunique damage is skill-based and therefore auto-hit (100 %).**

**Suggested pairing for gamora** (her call):
- GD boss/nemesis ↔ the superunique + boss rows, or the unique-with-Extra-Strong arm: **84–93 %**.
- GD champion-hero ↔ the stage-6 champion figure (≥ 81 %), or plain uniques (**76 [74–80]**).

Grades: AR inputs are DATAMINED; the laws are as marked; hit % is INFERRED (computed).
