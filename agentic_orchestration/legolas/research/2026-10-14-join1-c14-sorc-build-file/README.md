# Research: C-14 Sorceress build file (KP-435), 2026-10-14

**Mode:** A · **Agent:** legolas · **Commissioner:** gandalf (JOIN-1). **Matt ruling KP-435:** her endgame sheet comes from the guide her kit record cites, pinned verbatim.
**Guide:** Maxroll, *Fire Ball Meteor Sorceress Endgame Build Guide for Diablo II: Resurrected Season 14*, by Teo1904. <https://maxroll.gg/d2/guides/meteor-sorceress>. The page reads **"Season 14 · Last Updated: May 22, 2026"**.
**Law:** LoD 1.13 (`fabd/diablo2 @ 45112569`, `research/datamine-acquisition/d2/raw/`). Read-only throughout. No forks were used.

## Files

| File | What |
|---|---|
| `captures/maxroll-meteor-sorceress.html` | The guide page as served (server-rendered Remix HTML), 672,650 B. sha256 `cda05ef8…ca64de` |
| `captures/maxroll-meteor-sorceress.txt` | Its visible text, tags stripped. sha256 `d249e962…95678` |
| `captures/maxroll-d2planner-gca1a0l6.json` | **The build data itself.** The page embeds its builds as `data-d2planner-profile="gca1a0l6"`; the JSON is fetched from `https://planners.maxroll.gg/profiles/d2/gca1a0l6`. Author Teo1904, profile date 2026-02-04 09:18:34. sha256 `d6256571…64de` |
| `captures/maxroll-d2planner-gca1a0l6.data.json` | The `data` field, decoded and indented (no edits). sha256 `0bfe5aa7…22a1` |
| `build_file_standard_verbatim.json` | **The pinned build file:** the guide's "Standard" profile and its 20 items, copied verbatim (`scripts/extract_standard_verbatim.py`) |
| `sorc_build_sheet.json` · `scripts/sorc_build_sheet.py` · `verification_sheet.log` | The 1.13 sheet, four variants |

**How it was captured** (2026-10-14T23:38Z): plain `curl` with a browser user-agent. Both the HTML and the planner API returned **200**; no JavaScript execution was needed.
- The prose (skills, attributes, breakpoints, gear-option table, playstyle) is server-rendered in the HTML.
- The per-variant gear lives in the d2planner profile the page references. The guide's tabs Starter, Standard, Magic Find, Set Build and Ubers map to planner sets 1, 2, 3, 6 and 4. The planner also holds "Skill Tree", "Hardcore" and "Damage" profiles, which the guide's tabs do not show.

Grades:
- **VERBATIM:** copied from the capture.
- **DATAMINED:** read from 1.13 tables.
- **MODEL-VERIFIED / INFERRED:** as in the C-13 packet.

---

## 0. ⚑ Ruling needed: which variant

The guide offers five build variants. **This packet resolves "Standard", and that is my proposal, not a pick.** Standard is the guide's general endgame setup, and the kit record names this guide as "Endgame". **The other variants are captured verbatim in the planner JSON.**

| Variant | What it is | 1.13 problems |
|---|---|---|
| **Standard** | General endgame. **Every item exists in 1.13** | None |
| Magic Find | Tal Rasha pieces plus Chance Guards | — |
| Ubers | Griffon's Eye, Stormshield, Death's Fathom-class gear | — |
| Set Build | Tal Rasha | — |
| Starter | Level 75 | — |

## 1. The build file: the guide's "Standard" variant, verbatim

**Prose** (VERBATIM from the page, Standard tab):
- *"Important Breakpoints: 63% or 105% FCR and at least 60% FHR."*
- *"Allocate enough Stat Points into Strength to equip your gear. Put the remaining Stat Points into Vitality."*
- *"Use Flame Rift instead of Burning Grand Charm of Vita to enable farming of any monster."*
- *"Might Aura Mercenary … Infinity Giant Thresher … Andariel's Visage, and Fortitude."*

**Late-game** (VERBATIM): *"At the beginning of each run, buff yourself by swapping to Call to Arms and cast Battle Command 2 times, Battle Orders, swap back to your main setup and cast Frozen Armor. Make sure these buffs stay active all the time."*

**From the planner, set 2** (VERBATIM values):

| Field | Value |
|---|---|
| **clvl** | **99** (merc 98), difficulty Hell, all quests done in all three difficulties |
| **Stats added** | **Str 74, Dex 0, Energy 0, Vit 431** (505 points = 98×5 + 15 from Lam Esen) |
| **Skills** (hard points; Skills.txt ids) | Fire Bolt 17, Warmth 1, Frozen Armor 1, Inferno 1, Static Field 1, Telekinesis 1, Blaze 1, Fire Ball 20, Fire Wall 1, Enchant 1, Teleport 1, Meteor 20, Fire Mastery 20 (86 points) |
| Skill progression | The planner also carries `skillProgression`, 24 entries: Fire Bolt ×3, Inferno ×19, Enchant ×2. **Final at 99: Fire Bolt 20, Inferno 20, Enchant 3** (110 points = 98 + 12 quest). **Of record per KP-444 (stage 6, § 10):** the 24 progression points are spent. (Stage 5's 17 / 1 / 1 is superseded.) |

**Gear** (planner items with their rolls):

| Slot | Item (VERBATIM) | Sockets | Rolls as pinned |
|---|---|---|---|
| Helm | **Harlequin Crest** (Shako, def 141) | Ist | +2 all skills, 1.5 life and 1.5 mana per clvl, 50 MF, 10 % DR, +2 all attributes |
| Weapon | **The Oculus** (Swirling Crystal, ethereal) | Ist | +3 Sorceress skills, 30 FCR, 20 all res, 20 Vit, 20 Energy, 20 % ED, 5 mana per kill, 50 MF, 25 % Teleport when struck |
| Shield | **Spirit Monarch** (148 def) | Tal-Thul-Ort-Amn | **35 FCR, 112 mana, 8 magic absorb** (max), 55 FHR, +250 def vs missile, 22 Vit, +2 skills |
| Armour | **Chains of Honor on a superior Dusk Shroud** (468 base, +15 % def) | Dol-Um-Ber-Ist | +50 all res, +70 % ED (+15 superior), +2 skills, +20 Str |
| Gloves | **Magefist** (12 def) | — | 20 FCR, 25 mana regen, +1 fire skills, +30 % ED, +10 def |
| Belt | **Arachnid Mesh** (63 def) | — | +120 % ED, 20 FCR, +1 skills, 5 % mana |
| Boots | **War Traveler** (Battle Boots, 48 def) | — | 190 % ED, 10 Str, 10 Vit, 50 MF, 25 FRW |
| Rings ×2 | magic rings | — | 40 MF each (prefix 15 + suffix 25) |
| Amulet | magic amulet | — | +3 fire skills, 35 MF |
| Switch weapon | **Call to Arms on an ethereal Crystal Sword** | Amn-Ral-Mal-Ist-Ohm | +6 Battle Command, +6 Battle Orders, +4 Battle Cry, +1 all skills |
| Switch shield | **Spirit Monarch** (identical) | | |
| Charms | 6× small charm (5 all res, 7 MF); 1× small charm (5 all res, 5 FHR); **Annihilus** (+1 skills, 20 all attributes, 20 all res, 10 % XP); **7× grand charm (+1 fire skills, 45 life)**; **Gheed's Fortune** (40 MF, 160 % gold, 15 % prices); **Hellfire Torch, Sorceress** (20 all attributes, 20 all res) | | |
| Mercenary | type 11, level 98. **Infinity on an ethereal Giant Thresher** (Conviction level 12, 340 % ED); **ethereal Fortitude on Sacred Armor**; **ethereal Andariel's Visage** with a 15 IAS / 30 fire-res jewel. The guide's text names the **Might**-aura merc (Act 2) | | |

Also in the inventory: Horadric Cube and Tome of Town Portal.

**Gear-option table** (the alternatives the guide lists per slot), VERBATIM:

| Slot | Options |
|---|---|
| Weapon | Heart of the Oak · Spirit · Obsession Archon Staff · The Oculus · Eschuta's Temper · Wizardspike · Tal Rasha's Lidless Eye |
| Off-hand | Spirit Monarch · Rhyme · Ancients' Pledge · Stormshield |
| Swap | Call to Arms Crystal Sword · Memory Battle Staff · Gull · Blade of Ali Baba · Wand of Lower Resistance |
| Helmet | **Flickering Flame Diadem** · Lore · Crown of Ages · Harlequin Crest · Tal Rasha's Horadric Crest · Rare Diadem · Gemmed Mask |
| Body armour | Chains of Honor · Stealth · Skin of the Vipermagi · Ormus' Robes · Skullder's Ire · Tal Rasha's Guardianship |
| Gloves | Magefist · Chance Guards · Trang-Oul's Claws · rare or magic |
| Belt | Arachnid Mesh · Goldwrap · Verdungo's · Tal's Fine-Spun Cloth · IK Detail · magic |
| Boots | War Traveler · Sandstorm Trek · Waterwalk · Marrowwalk · Aldur's · rare or magic |
| Amulet | Mara's · Tal's Adjudication · caster craft · magic |
| Rings | SoJ · Bul-Kathos' Wedding Band · Nagelring · Dwarf Star · rare or magic |
| Charms | grand / large / small |
| Unique charms | Gheed's · Hellfire Torch · Annihilus · **Flame Rift** |

## 2. The 1.13 resolution, slot by slot (DATAMINED)

**Every Standard item resolves in the 1.13 tables, with the same property set and ranges the planner pins:**
- Harlequin Crest (`uap`), The Oculus (`oba`), Magefist (`tgl`), Arachnid Mesh (`ulc`), Wartraveler (`xtb`, 1.13 index "Wartraveler"), Annihilus (`cm1`), Hellfire Torch (`cm2`), Gheed's Fortune (`cm3`), Andariel's Visage (`usk`): all in `UniqueItems.txt`.
- **Hellfire Torch:** `randclassskill` gives **+3** class skills (`Properties.txt` val1 = 3). The planner's "1" is the class index.
- Spirit (`Runeword130`, 25–35 FCR, 89–112 mana, 3–8 absorb), Chains of Honor (`Runeword14`: res-all 50, ac% 70, +2, +20 Str), Call to Arms (`Runeword13`: BO 1–6, BC 2–6, BCry 1–4, +1), Infinity (`Runeword60`, Conviction 12), Fortitude (`Runeword41`): all in `Runes.txt`. Rune socket mods come from `Gems.txt`; in body armour, Um adds res-all 15 and Ber adds 8 % DR.
- **Bases:** Dusk Shroud 361–467 (Str 77), Monarch 133–148 (block 22, Str 156), Battle Boots 39–47 (Str 95), Spiderweb Sash 55–62 (belt type 6).
- **Magic affixes** (Fortune MF on rings and amulet, +3 fire skills on the amulet, Shimmering / Good Luck / Balance on small charms, Burning / Vita on grand charms) exist in the 1.13 affix tables. Their exact max rolls were not individually re-checked (INFERRED).

**D2R-only content, and the guide's own alternative:**

| Item | Where it appears | 1.13 resolution | Effect |
|---|---|---|---|
| **Flame Rift** (Sunder charm, D2R 2.5+) | Not equipped. The prose says *"Use Flame Rift instead of Burning Grand Charm of Vita"* | **Use the guide's own alternative, the Burning Grand Charm of Vita. That is what the planner equips anyway** (7 of them) | No change to the sheet. **Fire immunes stay immune in 1.13** (C-12b) |
| **Flickering Flame** | Helm option list only, not in Standard | Not needed: Standard pins Harlequin Crest | none |
| Terror Zones / Sunder farming notes | Prose | No 1.13 analogue | none |

**No substitution needs your ruling for Standard.** Two observations, flagged but not ruled:
- **Ethereal Oculus:** a sorceress orb that is ethereal only changes durability, not its stats. It is admissible in 1.13.
- **The Ist sockets in Oculus and Shako** need Larzuk's socket quest on uniques, which exists in 1.13.

## 3. Her resolved sheet (`sorc_build_sheet.json`), clvl 99, guide stats, max rolls as pinned

**Laws:**
- Life and mana: the J4a F12 pattern with Sorceress CharStats (40 + 1/clvl + 2/Vit; 35 + 2/clvl + 2/Energy).
- BO: J4a F03. The % applies to base life plus flat life, **not** to item Vitality.
- Defence: each item's own ED, plus Dex/4. Oculus's "+20 % ED" sits on a weapon with no armour class; ItemStatCost op 13 is item-local, so it adds nothing (INFERRED).
- Block: `Units.cpp`.
- Resists: Hell −100, +30 Anya (KP-428), cap 75.
- FCR/FHR frames: the Sorceress breakpoint tables (animation packet / J4b).

**BO level from the swap:** CTA BO +6, plus every +all-skills item worn while swapped: CTA 1, switch Spirit 2, Shako 2, CoH 2, Arachnid 1, Annihilus 1. That gives **slvl 15**, and **16 after the guide's Battle Command casts**, so **+80 % life and mana**. Without charms: 14, then 15 with BC, so +77 %. The planner's own figure is 14 / +74 %, which appears to omit the switch Spirit or Annihilus. INFERRED from the CTA and F03 laws.

| | **Charms, no BO** | **Charms + BO 16** | No charms, no BO | No charms + BO 15 | **Current default (KP-428)** |
|---|---|---|---|---|---|
| clvl | 99 | 99 | 99 | 99 | 90 |
| Str / Dex / Energy / Vit (total) | 156 / 67 / 97 / 535 | same | **116** / 27 / 57 / 495 ⚑ | same ⚑ | 156 / 32 / 35+ / 380 |
| **Life** | **1,651** | **2,821** | 1,256 | 2,139 | **1,004** |
| Mana | 639 | 1,032 | 559 | 937 | — |
| **Defence** (vs melee / missile) | **1,472 / 1,722** | 1,472 / 1,722 | 1,462 / 1,712 | same | 1,060–1,347 / +250 |
| **Block** (stationary / running) | **11 % / 3 %** | 11 / 3 | 2 / 0 | 2 / 0 | 3 % |
| **Resists after Hell + Anya** (fire / cold / lightning / poison) | **75 / 75 / 75 / 75** (uncapped 90 / 125 / 125 / 125) | same | **15 / 50 / 50 / 50** | same | +15…+25 / 50…60 |
| FCR | **105 → 8 frames** | same | same | same | 105 |
| FHR | **60 → 8 frames** | same | **55 → 9 frames** | same | 55 |
| FBR | 0 → 9 frames | same | same | same | 0 |
| DR % / magic absorb | 18 / 8 flat | same | same | same | 18 / 3–8 |
| **+skills to her fire skills** | **+25** (all 8, Sorceress 6, fire 11) | same | +14 | same | +11–13 |
| **slvl** Fire Ball / Meteor / Fire Mastery / Fire Bolt / Inferno | **45 / 45 / 45 / 45 / 45** (stage-5 42 / 26 superseded, § 10) | same | 34 each (stage-5 31 / 15 superseded) | same | 31–33 (Fire Bolt unpinned) |
| slvl Warmth / Enchant / Frozen Armor | 26 / 28 / 15 (stage-5 Enchant 26 superseded) | same | 15 / 17 / 11 | same | — |
| MF % | 427 | same | 345 | same | — |

**⚑ Without charms the guide's allocation does not meet the Monarch's Strength requirement** (116 < 156): Annihilus and the Torch supply 40 of it. A no-charm sheet would have to move 40 points from Vitality to Strength, costing 80 life. That is a modelling choice for you, not something I picked; the column above keeps the guide's allocation.

**Grades:**
- Item values: VERBATIM (planner) and DATAMINED (1.13 rows agree).
- Life, mana, defence and block: MODEL-VERIFIED laws, values INFERRED (computed).
- BO level: INFERRED. It differs from the planner's 14 by 2 levels, which is 6 % life.

## 4. Flags for elrond and the conductor

1. **Battle Orders is a precast buff** with a long duration. At slvl 16 with Battle Command at blvl 7 or more, the J4a F03 duration is about 180 s or more, and the guide says *"make sure these buffs stay active all the time."*
   - **It is a sheet operand** (a % of life and mana) **if** a wave never outlasts its duration.
   - Otherwise it needs a re-cast mechanism: a weapon swap plus two casts at FCR 0 on the CTA, since the swap loses the Oculus/Spirit FCR.
2. **Frozen Armor** is also a precast, and no census row covers it.
   - slvl 15: +% defence per Skills.txt `skill_armor_percent` ln12.
   - **It freezes melee attackers**, which is a control mechanism, not a sheet number.
3. **The mercenary is a separate actor.** Act 2, Might aura per the prose, at level 98.
   - **Infinity's Conviction aura lowers enemy resists** (it can break some fire immunes in 1.13), and Might adds his damage.
   - **In or out is a ruling.** If he is out, the Conviction −res is lost from her damage path.
4. **Gear effects no census row covers:**
   - **Oculus: 25 % chance to cast Teleport when struck** (an involuntary reposition);
   - **Hellfire Torch: chance to cast Firestorm on striking**, plus Hydra charges;
   - Arachnid Mesh: Venom charges;
   - War Traveler: thorns 10;
   - Spirit: 8 magic absorb (sheet);
   - 5 mana per kill (Oculus);
   - the **Teleport, Static Field and Telekinesis** skills (the guide uses Static against bosses and TK to stun immunes);
   - **Enchant** (a merc buff).
5. **No Sunder in 1.13.** The guide's farming spots marked "strong without a Sunder Charm" (Mausoleum, Pit, Andariel, Cows, Stony Tombs, Ancient Tunnels, Maggot Lair, Arcane, Summoner, Lower Kurast, Mephisto, Diablo, Eldritch) are the 1.13-consistent set.
6. **Variant choice** (§ 0) needs a ruling. This sheet is "Standard".

## Sources (accessed 2026-10-14)
- **Maxroll guide page** and **d2planner profile `gca1a0l6`** (captured, sha256 above). Author Teo1904. Guide last updated 2026-05-22; profile dated 2026-02-04.
- **1.13 tables** `fabd/diablo2 @ 45112569`: CharStats, Armor, Weapons, UniqueItems, Runes, Gems, Properties, ItemStatCost, Skills.
- **Prior packets:** J4a F03/F12, J4b § 3, the animation packet (FCR/FHR/FBR), C-13 § 6 (default sheet, KP-428).

---

## 6. Stage 2 (KP-436): Standard variant as written, Battle Orders always on, mercenaries out

Files: `c14_stage2.json`, `scripts/c14_stage2.py`, `verification_stage2.log`. The Basin and D2MOO captures are in `captures/stage2/`.

### 6.1 Hit chance against the build-file sheet

> **⚑ KP-437:** Frozen Armor is now always on. **The primary table is § 7.3** (with Frozen Armor at slvl 16, +105 %). The "build-file sheet" column below becomes the no-Frozen-Armor **sensitivity**, and the slvl-15 Frozen Armor column is superseded by § 7.3.

**Defender:** Defence **1,472** vs melee and **1,722** vs missiles, dlvl **99**. Battle Orders does not change defence. **This supersedes the C-13 NO-DEX tables** (§ 13 and § 14.2 there are marked).

**Method:** the same AR rows, roles, weighting and laws as C-13 stages 6–7 (`CtH = clamp(2·alvl·⌊100·AR/(AR+Def)⌋/(alvl+dlvl), 5, 95)`; missiles roll only if `ToHit` is set; casters auto-hit). Grades: INFERRED values through MODEL-VERIFIED laws on DATAMINED AR. The level term falls because dlvl rises from 90 to 99.

Per-type best attack; median [p25–p75] (min–max), equal weight; normal monster level 85:

| Attacker | **Build-file sheet** | With Frozen Armor precast (def 2,944 / 3,194) | (superseded NO-DEX) |
|---|---|---|---|
| Normal, melee (57 types) | **67 [64–72] (56–81)**; slot-weighted 67 | 53 [49–59] (40–72) | 74 [71–78] |
| Normal, ranged-physical (3) | **68 [65–68] (62–68)** | 56 [52–56] | 74 |
| Normal, caster (6, or 10 with C-13's 4) | **100 (auto-hit)** | 100 | 100 |
| Champion (lower bound) | **74 [72–78]** | 62 [59–68] | ≥ 81 |
| Unique (+3 levels) | **69 [66–73.25] (58–82)** | 54 [51–60.25] | 76 [74–80.25] |
| Unique with Extra Strong | **77 [75–80] (68–86)** | 65 [63–70.25] | 84 [82–87] |

**Named** (melee / vs missile defence):

| Monster | Build-file sheet | With Frozen Armor |
|---|---|---|
| Grand Vizier of Chaos | 77 / 75 | 65 / 64 |
| Lord De Seis | 80 / 79 | 71 / 69 |
| Infector of Souls | 74 / 71 | 61 / 59 |
| Diablo | 81 / 79 | 71 / 69 |
| Baal | 86 / 85 | 76 / 75 |

**Frozen Armor is not in KP-436's ruling,** so it is given only as a sensitivity. The guide precasts it ("cast Frozen Armor"), and at slvl 15 it doubles defence (§ 6.3).

### 6.2 Battle Orders: slvl and duration, settled

**Items worn on the swap, and their +skills that reach BO** (an oskill takes +all-skills bonuses; Basin Oskill):

| Item | +skills to BO |
|---|---|
| Call to Arms | +1 all, +6 BO oskill, +6 BC oskill |
| Spirit Monarch (switch shield) | +2 all |
| Harlequin Crest | +2 all |
| Chains of Honor | +2 all |
| Arachnid Mesh | +1 all |
| Annihilus | +1 all |
| **Not counted** | Magefist (+1 fire), amulet (+3 fire), the 7 grand charms (+1 fire), Hellfire Torch (+3 Sorceress), and the Oculus, which is swapped out of the main hand |

**BO slvl = 6 + 9 = 15 without Battle Command, 16 after it.** Battle Command gives +1 all skills and also applies to itself.

| | BO % | Duration |
|---|---|---|
| Without BC (slvl 15) | +77 % | **170 s** |
| **After BC (slvl 16)** | **+80 %** | **180 s** |

- **Duration formula:** 750 + 250·(slvl−1) frames (Skills.txt row 149, `auralencalc`). The synergy term (Shout.blvl + BC.blvl) × 125 is **0**, because blvl counts hard points and she has none.
- **BC itself:** slvl 15 on the first cast, 16 on the second. The second cast lasts 125 + 250·15 frames = **155 s**.
- **The planner's 14 / +74 %** equals 6 + 8. It omits one +1 source, and **its data does not let me tell which**. My count is 15/16 from the item list above. INFERRED.
- **⚑ For the census:** if Battle Command is also treated as always on, every skill gets +1. That makes Fire Ball, Meteor and Fire Mastery slvl 46 and Frozen Armor 16. KP-436 rules only BO.

### 6.3 Frozen Armor law at the build file's slvl 15

slvl = 1 hard + 8 all skills + 6 Sorceress skills (Oculus 3, Torch 3), +1 if BC is active.

| Quantity | Formula | Value at slvl 15 | Grade |
|---|---|---|---|
| **Defence bonus** | `skill_armor_percent` = ln12 = 30 + 5·(slvl−1) % | **+100 %** of total defence | DATAMINED (Skills.txt row 40) |
| **Duration** | ln34 = 3000 + 300·(slvl−1) frames (synergies 0) | **7,200 frames = 288 s** | DATAMINED |
| **Freeze on melee attacker** | Event `damagedinmelee`, **only if the hit dealt physical damage > 0** (D2MOO `SkillSor.cpp` `EventFunc02_FrozenArmor`). Freeze length = calc1 = ln56 = 30 + 3·(slvl−1) frames | **72 frames = 2.88 s base** | MODEL-VERIFIED |

**Who gets frozen:** freeze length **freezes normal and minion monsters, and only CHILLS champions, uniques, superuniques and bosses** (Basin Freeze length; C-13 KP-426). Cold-immune targets are unaffected.

**Length against monsters in Hell:** × (100 − cold resist)/100, then ÷4 (Hell MonsterFreezeDivisor). So a normal monster is frozen **0.72 s** at cold resist 0, **0.48 s** at 33 and **0.36 s** at 50.

**Ranged and spell attacks never trigger it** (melee event only).

### 6.4 The two proc items

| Item | Proc (1.13 data) | Trigger (Basin) | What it does here |
|---|---|---|---|
| **The Oculus** | `gethit-skill` par 54: **25 % chance, level 1 Teleport, when struck** | Hit by melee, or by a missile carrying weapon or monster damage. **Not** by missiles that apply only their own or skill damage, so most monster spells do not trigger it | Teleport is cast on the user (Basin's "cast on user" column). **She is moved involuntarily.** The destination rule for an untargeted Teleport cast is **UNVERIFIED**: D2MOO `SrvDo027` teleports to the skill's target XY, and I did not trace how a when-struck cast sets that target. **A mechanism with no census row** |
| **Hellfire Torch** | `hit-skill` par 197: **5 % chance, level 10, on striking.** Skill 197 is **DiabWall, i.e. Diablo's Firestorm**, not the Druid's Firestorm (Id 225) | **Only a weapon attack** that is not missed, blocked or dodged | **Fire Ball and Meteor are spells, so the Torch's Firestorm effectively never fires for this kit** (INFERRED from the trigger law). Its Hydra charges are unused unless spent manually |

### 6.5 Changes to the census

- **BO always on** (KP-436): use the "Charms + BO 16" sheet. Life **2,821**, mana 1,032, all else as in § 3.
- **Mercenaries out** (KP-436): Infinity's Conviction and the Might aura are gone. Fire immunes stay immune.
- **Still unruled:** Frozen Armor (precast; +100 % defence and freezes melee attackers); Battle Command (+1 all skills); the Oculus teleport.

---

## 7. Stage 3 (KP-437): Static Field added; Battle Command and Frozen Armor always on

Files: `c14_stage3.json`, `scripts/c14_stage3.py` (derived from the stage-2 script; Frozen Armor slvl 16 is primary), `verification_stage3.log`. Captures: `captures/stage2/basin-Static_Field-raw.txt`, `d2moo-SkillsTbls.h`, `d2moo-SkillSor.cpp`, `d2moo-SkillItem.cpp`.

### 7.1 Static Field, 1.13 law, at her slvl 16

Her slvl is 1 hard + 8 all skills + 6 Sorceress skills + 1 Battle Command. No lightning-tree bonuses are worn.

| Item | Law and value | Grade / source |
|---|---|---|
| **Radius** | `aurarangecalc` ln12 = 5 + (slvl−1)·1 subtiles. **slvl 16 → 20 subtiles = 13⅓ yd** | DATAMINED (Skills.txt row 42, Param1 5, Param2 1); Basin "(4+slvl)·2/3" agrees. MODEL-VERIFIED |
| **Damage** | **25 % of the target's CURRENT life per cast** (calc1 = par4 = 25; minimum damage calc2 = par3 = 0). It is not scaled by slvl or by +% lightning damage | D2MOO `SkillSor.cpp` `SrvDo020_StaticField` / `AuraCallback_StaticField`; Basin. MODEL-VERIFIED |
| **Hell floor** | In expansion games, **no effect if the target's current life is ≤ 50 % of max life** (DifficultyLevels `StaticFieldMin` Hell 50; Nightmare 33, Normal 0). The test runs **before** the damage, so one cast can take a target from just above 50 % to below it (e.g. 55 % → 41.25 %) | D2MOO (check before damage) + Basin ("unless target already has < 50 % life in Hell"). MODEL-VERIFIED |
| **Boss / unique rule** | **None in code.** It applies to every unit in the aura filter, bosses included, subject to the same 50 % floor | D2MOO callback (no rank branch); Basin lists none. MODEL-VERIFIED |
| **Resist** | **Lightning family.** Damage is reduced by **positive** lightning resist (LR 50 % halves it; LR ≥ 100 means immune). **Negative LR does not increase it**: the code pre-divides by (100 − LR) so the later resist step cancels out. **This kit has no −% enemy lightning resist** | D2MOO callback; Basin (resist reduces, negative LR does not increase it; only item −ELR can). MODEL-VERIFIED |
| **Can it miss?** | **No.** Radial aura callback, no to-hit roll, no block (no physical damage) | D2MOO. MODEL-VERIFIED |
| **Mana** | **9 per cast at every level** (mana 9, manashift 8, lvlmana 0, minmana 1) | DATAMINED; Basin "Mana = 9" |
| **Casting delay** | **None** (`delay` blank). It casts at her normal FCR, 8 frames at FCR 105. The separate Lightning/Chain Lightning table does not apply | DATAMINED; animation packet § 3.1 |
| **Timing** | Instant on the cast frame; it hits every eligible enemy in radius once per cast | D2MOO (`SrvDo020` runs the aura callback once) |

### 7.2 The Oculus Teleport destination: SOURCED, not UNVERIFIED

1. Teleport's Skills.txt row has **`ItemTarget = 2`** (and `ItemEffect` 1). DATAMINED.
2. In D2MOO, `SkillsTbls.h` names `SKILLSITEMTARGET_RANDOM = 2` as *"Random walkable location in a radius of size 20"*.
3. `SKILLITEM_HandleItemEffectSkill` → **`SKILLITEM_FindTargetPosition`** makes up to **10 tries** at `(x ± rand%40 − 20, y ± rand%40 − 20)` around **her own position**, i.e. a uniform square from −20 to +19 subtiles on each axis (**about ±13⅓ yd**). It takes the **first non-colliding (walkable) point**. **If all 10 tries collide, nothing is cast.**
4. Teleport (`SrvDo027`) then moves her there, unless the area forbids Teleport (Levels.txt `Teleport` flag; towns).

So **a struck proc teleports her to a random walkable spot within about 13 yd of where she stood**, not toward or away from the attacker. Grade: **MODEL-VERIFIED** (DATAMINED `ItemTarget` plus the D2MOO code path). Trigger and chance are unchanged from § 6.4: 25 %, level 1, when struck by melee or by a weapon/monster-damage missile.

### 7.3 FINAL primary hit tables, WITH Frozen Armor (slvl 16, +105 %)

**Defence by attack kind:** **3,017 vs melee** (1,472 × 2.05) and **3,267 vs missiles** (+250 Spirit), clvl 99. Casters auto-hit. Same AR rows, roles and laws as C-13 stages 6–7.

Per-type best attack; median [p25–p75] (min–max), equal weight:

| Attacker | **PRIMARY (Frozen Armor 16)** | Without Frozen Armor (sensitivity; = stage 2) |
|---|---|---|
| Normal, melee (57 types) | **52 [49–59] (40–72)**; slot-weighted 52 | 67 [64–72] |
| Normal, ranged-physical (3) | **56 [52–56] (48–56)** | 68 |
| Normal, caster | **100** | 100 |
| Champion (lower bound) | **61 [58–67]** | 74 |
| Unique (+3 levels) | **54 [51–60.25] (41–74)** | 69 |
| Unique with Extra Strong | **64 [63–70] (53–80)** | 77 |

**Named bosses** (melee / vs missile):

| Monster | Primary | Without Frozen Armor |
|---|---|---|
| Grand Vizier of Chaos | **64 / 64** | 77 / 75 |
| Lord De Seis | **70 / 69** | 80 / 79 |
| Infector of Souls | **61 / 59** | 74 / 71 |
| Diablo | **70 / 69** | 81 / 79 |
| Baal | **76 / 75** | 86 / 85 |

Grades: INFERRED (computed) through MODEL-VERIFIED laws on DATAMINED attack ratings. **The stage-2 build-file table without Frozen Armor is now the sensitivity.**

**Frozen Armor at slvl 16:**
- +105 % defence; duration 3,000 + 300·15 = 7,500 frames = **300 s**.
- Freeze on attackers 30 + 3·15 = **75 frames (3.0 s) base**. In Hell a normal monster is frozen 0.75 / 0.50 / 0.375 s at cold resist 0 / 33 / 50. **Champions, uniques and bosses are only chilled.**
- It triggers only on melee hits that deal physical damage (§ 6.3 law).

### 7.4 Her final sheet (KP-435/436/437)

Standard variant, clvl 99, charms, BO / BC / Frozen Armor always on, mercenaries out:

| Quantity | Value |
|---|---|
| Life / mana | **2,821 / 1,032** (BO 16, +80 %) |
| **Defence** vs melee / vs missile | **3,017 / 3,267** (Frozen Armor +105 %) |
| Block | 11 % (3 % running) |
| Resists after Hell + Anya | 75 / 75 / 75 / 75 (uncapped 90 / 125 / 125 / 125) |
| FCR / FHR / FBR | 105 (8 frames) / 60 (8) / 0 (9) |
| DR / magic absorb | 18 % / 8 flat |
| **+skills** | all 9 (8 + BC 1), Sorceress 6, fire tree 11 → **+26 to her fire skills** |
| **slvl** | **Fire Ball 46, Meteor 46, Fire Mastery 46, Fire Bolt 46, Inferno 46**, Warmth 27, **Enchant 29**, **Static Field 16**, Frozen Armor 16, Teleport 16. **Of record per KP-444 (§ 10);** stage-5 43 / 27 / 27 superseded |
| Castables | Fire Ball, Meteor, **Static Field** (KP-437) |
| Buffs, always on | Battle Orders 16 (180 s), Battle Command 16 (155 s), Frozen Armor 16 (300 s) |
| MF | 427 % |

Life, mana, block and resists are unchanged by BC: BC adds skill levels only, and Battle Orders was already counted at 16.

### 7.5 Belt (owed item): Arachnid Mesh

Arachnid Mesh is the unique on **Spiderweb Sash `ulc`**. 1.13 `Armor.txt` gives `belt = 6` (DATAMINED), which is **16 slots = 4 rows × 4 columns**. Only the bottom row is hotkeyed.
- Corroboration: Arreat elite belts list #Boxes 16; Basin lists Rows 4; a D2R mirror gives numboxes 16. **Belts.txt is not in the 1.13 mirror.**
- **Grade: MODEL-VERIFIED.**
- This was delivered in C-13 (`../2026-10-14-join1-c13-enemy-anchor/potions.json → d2.belt`, `potions_notes.md` item 10) and is restated here so the build file carries it.

---

## 8. Stage 4 (gamora ADDENDUM-9): six 1.13 facts

Files: `c14_stage4.json`, `scripts/c14_stage4.py`, `verification_stage4.log`. Captures: `captures/stage4/`, which holds D2MOO `SUnitDmg.cpp/.h` and `MissMode.cpp`, plus Basin Absorb, Magic Absorb, Attacker Takes Damage, Mana After Each Kill, Cold Damage and Chill effectiveness. Code lines refer to D2MOO `5596f5cb` (1.10f).

### 8.1 Monster chill magnitude: NOT a flat −50 %

**Law.** Chill sets `velocitypercent`, `attackrate` **and** `other_animrate` all to the target's **chill effectiveness**.
- **For a monster** that is its **MonStats `coldeffect` column for the current difficulty** (`coldeffect(H)` in Hell).
- **Players, mercenaries and pets: −50.**
- Source: `SUnitDmg.cpp` `GetColdEffect` L85–99 and `ApplyColdState` L1552–1611; Basin Chill effectiveness ("determines the attack rate and movement speed modifiers"). **MODEL-VERIFIED.**

**So chill slows movement AND attack rate (and other animation rates) equally.**

**Hell values are smaller than Normal** (DATAMINED): Oblivion Knight −50 / −33 / −25 across Normal / Nightmare / Hell; Diablo −25 / −15 / **−10**; Baal **−15**; Mephisto **−10**.

**R1 population, Hell** (70 types; DATAMINED):

| Chill effectiveness | Types |
|---|---|
| −40 | 5 |
| −33 | 35 |
| −25 | 24 |
| 0 | 6 |

- Median **−33** [−33 to −25].
- **coldeffect ≥ 0 means no chill and no freeze** (`ApplyColdState` returns on 0; `ApplyFreezeState` returns if coldeffect ≥ 0).
- Bosses: Diablo −10, Baal −15. Seal bosses use their class value: Grand Vizier −25, Lord De Seis −25, Infector −33.
- Floors (Basin Cold Damage): no unit goes below 25 % movement speed or 15 % attack rate.
- Chill length on monsters: ÷ MonsterColdDivisor (Hell 4), minimum 1 frame (`ApplyColdState` L1569–1578).

**⚑ CONFLICT: who is chilled instead of frozen.**
- **D2MOO `ApplyFreezeState` (L1665–1675)** converts freeze into chill only for **bosses, monsters with type-flag 8 (unique, which superuniques also carry) and hirelings**. **Champions (flag 4) are not in that test, so the code FREEZES champions.**
- **Basin** (Champion page: *"Freeze length chills instead; only minions can be frozen"*; Freeze length; Chill effectiveness) says **champions are chilled**.
- I do not pick. The code is 1.10f, and Basin may reflect 1.11–1.13 behaviour. **My stage-2 and stage-3 sentences "champions … are only chilled" rest on Basin alone and inherit this conflict.**

### 8.2 Does flat magic absorb heal? YES, by the amount absorbed

**Code** (`SUnitDmg.cpp` L1040–1056 and L1292–1297):
1. Magic damage after magic resist and flat Magic Damage Reduced has % absorb (capped at 40) taken off.
2. Then **flat absorb** takes off `min(absorb×256, remaining)`.
3. **Both absorbed amounts are added to `dwAbsLife`, which is healed** (current HP + absorbed, capped at max) before the remaining damage is subtracted.

Basin Magic Absorb: *"decreases any magic damage then heals life equivalent to that damage decrease"*; actual healing = min(max − current, absorbed). **MODEL-VERIFIED.**

**For her: Spirit's Magic Absorb +8 heals up to 8 life per magic hit, and only on magic-damage hits.** It does nothing against fire, cold, lightning or physical.

### 8.3 Are thorns reduced by the attacker's physical resist? YES. Flat DR applies too

`EventFunc06_AttackerTakesDamage` (stage-2 capture `SkillItem.cpp` L1009–1027) builds a **physical** hit (`dwPhysDamage = value << 8`, result flags 0x4021) and runs it through `SUNITDMG_ExecuteEvents(…, bMissile = 1)`. That path calls `CalculateTotalDamage`, which applies the physical row: the target's damage-resist % and flat physical damage reduction. Basin: *"The only way to increase damage is to reduce attacker Damage Resist (Amplify Damage, Decrepify)"*, i.e. damage resist governs it. **MODEL-VERIFIED.**

- **Triggers only on a successful melee hit on her.** Thorns can't be blocked.
- **War Traveler's thorns 10 = 10 physical per melee hit taken, × (100 − attacker DR %)/100, minus the attacker's flat DR.**
- **Thorns kills do NOT trigger on-kill effects:** the 0x20 result flag suppresses the KILL event; Basin lists Attacker Takes Damage as excluded.

### 8.4 Kill credit for owned missiles: "mana after each kill" DOES fire

Missile damage is executed with **the missile's owner as the attacker**: `MissMode.cpp` L4755–4760 `SUNITDMG_ExecuteEvents(pGame, pOwner, …)`. `ExecuteEvents` fires `UNITEVENT_KILL` on that attacker when the target dies and the 0x20 flag is absent (`SUnitDmg.cpp` L1396–1400). `EventFunc17_ManaAfterKill` adds the mana for a player owner.

Basin Mana After Each Kill excludes only mercenary/pet/trap/convert kills, passive radial auras (Holy Fire, Freeze, Shock, Sanctuary radial; Blade Shield) and returned damage. **It does not exclude missiles or ground effects.**

**So a Fire Ball explosion or a Meteor impact or burning-ground kill credits her: +5 mana (the Oculus).** Grade: **MODEL-VERIFIED** for missiles in general. **INFERRED for the Meteor ground fire specifically**: same owner path, but I did not trace `meteorfire`'s result flags line by line.

**Static Field cannot kill** (it leaves at least 1 HP).

### 8.5 Does a BLOCKED strike trigger the Oculus "when struck"? NO

- `EventFunc21_SkillOnGetHit` (`SkillItem.cpp` L1683–1708) requires **`DAMAGERESULTFLAG_GETHIT` (0x4)** on the hit.
- Item events fire only when **`SUCCESSFULHIT`** is set (`ExecuteEvents` L1131–1146).
- **A block sets BLOCK and clears SUCCESSFULHIT** (`GetResultFlags`; `MissMode.cpp` L4707–4729). For melee, GETHIT is set only on a surviving successful hit.
- Basin When Struck: *"whenever the user … is hit by a melee attack … or a missile attack"*; a blocked attack is not a hit.

**MODEL-VERIFIED.** Corollaries from the same gate:
- **No proc while she is uninterruptible** (GETHIT is withheld).
- **No proc from spells or pure-skill missiles** (§ 6.4).

### 8.6 Integer rounding of freeze length: resist first, then the Hell divisor, both floored

**Order** (code):
1. **`floor(L × (100 − coldres) / 100)`** in `CalculateTotalDamage`, stat-table row "Flen" (`SUnitDmg.cpp` L770; `CalculatePercentage`). Resist is capped at 100; **negative resist lengthens it**.
2. Cannot Be Frozen sets it to 0, or Half Freeze Duration halves it with integer `/2` (L867–878). Monsters normally have neither.
3. `ApplyFreezeState`: if `coldeffect(H) ≥ 0`, no freeze; else **`floor(… / MonsterFreezeDivisor)`** (Hell 4).
4. For bosses, uniques and hirelings, the same value goes to `ApplyColdState`: **`floor(… / MonsterColdDivisor)`** (Hell 4), **minimum 1 frame**.

Basin Cold Damage agrees that resist reduces length and that the difficulty penalty is 1/4 in Hell. **MODEL-VERIFIED.**

**Her Frozen Armor at slvl 16 = 75 frames.** Hell, by target cold resist:

| Cold res | after resist | **frozen (normal/minion)** | **chilled (unique/boss)** |
|---|---|---|---|
| −50 | 112 | 28 | 28 |
| −25 | 93 | 23 | 23 |
| 0 | 75 | **18 (0.72 s)** | 18 |
| 20 | 60 | 15 | 15 |
| 33 | 50 | **12 (0.48 s)** | 12 |
| 50 | 37 | **9 (0.36 s)** | 9 |
| 60 | 30 | 7 | 7 |
| 75 | 18 | 4 | 4 |
| ≥ 99 | 0 | 0 | 0 |

⚑ **This supersedes the unfloored 0.75 / 0.50 / 0.375 s in § 7.3 and § 6.3.**

For R1's cold resists, look up each type's `ResCo(H)` in this table (`c14_stage4.json → chill_effectiveness_R1.rows`).

---

## 9. Stage 5: verbatim hard points (correction found by gamora). ⚑ ITS VALUES ARE SUPERSEDED BY § 10 (KP-444)

**The defect.** `scripts/sorc_build_sheet.py` hard-coded Fire Bolt 20, Inferno 20 and Enchant 3. That assumed the planner's 24-entry `skillProgression` had been spent on top of `profile.skills`. **The verbatim `profile.skills` is Fire Bolt 17, Inferno 1, Enchant 1** (86 points).

**The fix.** The script now **reads every hard point from the verbatim planner JSON** (Skills.txt Id → points) and computes the synergies from them. It also has a final row with Battle Command on.

**Every other sheet field reproduces bit-exactly** against the stage-1 JSON: life, mana, defence, block, resists, FCR/FHR, +skills, MF and Strength check (checked field by field).

### Corrected values

| | Superseded (stage 1 / § 7.4) | **Corrected (verbatim hard points)** |
|---|---|---|
| Hard points Fire Bolt / Inferno / Enchant | 20 / 20 / 3 | **17 / 1 / 1** |
| **Final sheet slvl** (BO + BC + FA on) Fire Bolt / Inferno / Enchant | 46 / 46 / 29 | **43 / 27 / 27** |
| Charms, no BC: Fire Bolt / Inferno / Enchant | 45 / 45 / 28 | 42 / 26 / 26 |
| No charms: Fire Bolt / Inferno / Enchant | 34 / 34 / 17 | 31 / 15 / 15 |
| **Fire Ball synergy** 14 % × (Fire Bolt + Meteor hard points) | +560 % | **+518 %** (14 × 37) |
| **Meteor impact synergy** 5 % × (Fire Bolt + Fire Ball) | +200 % | **+185 %** (5 × 37) |
| **Meteor burning-ground synergy** 3 % × Inferno | +60 % | **+3 %** (3 × 1) |

The synergy laws are J4b H01–H03: synergies read hard points only. **Unchanged:** Fire Ball, Meteor and Fire Mastery slvl 46 (45 without BC), Warmth 27, Static Field 16, Frozen Armor 16.

### Did stages 2–4 use the wrong hard points? No.
- Those stages use only Battle Orders/Battle Command (oskills, 0 hard points), **Frozen Armor (hard 1)** and **Static Field (hard 1)**. Both are correct in the verbatim data, so FA slvl 15/16 (§§ 6.3, 7.3, 8.6) and Static Field slvl 16 (§ 7.1) stand.
- **No stage of C-14 computed Fire Ball or Meteor DAMAGE**, so no damage figure needs re-issuing. Any damage figure built downstream from § 7.4's synergies must use +518 / +185 / +3 %.
- The C-13 packet is unaffected: it used no hard-point values from this build.

### ⚑ Ruling item (raised, not decided)
**`profile.skills` totals 86 hard points at clvl 99, but a clvl-99 character with all quests has 110** (98 levels + 12 from quests: 2 + 1 + 1 per difficulty).
- The planner's `skillProgression` holds **exactly the 24 missing points**: Fire Bolt +3, Inferno +19, Enchant +2.
- Spending them reproduces the guide's prose order: *"Max out … 1. Meteor 2. Fire Mastery 3. Fire Ball 4. Fire Bolt 5. Inferno 6. Enchant."*
- **This stage follows the instruction (verbatim `profile.skills`).** If the conductor or Matt rule that the progression points are spent, the stage-1 values return: Fire Bolt 46, Inferno 46, Enchant 29; synergies +560 / +200 / +60 %. **I do not pick.**

---

## 10. Stage 6 (KP-444): the 24 `skillProgression` points ARE SPENT

**The ruling.** The clvl-99 build with all quests has 110 points (98 levels + 12 quest), and the guide's prose gives the max-out order. So the planner's 24 `skillProgression` entries are spent on top of `profile.skills`.

**The script** (`scripts/sorc_build_sheet.py`) now derives the hard points as the **verbatim `profile.skills` plus one point per verbatim `skillProgression` entry**. Both are read from the captured JSON; nothing is hard-coded. It **asserts the total equals 110**.

### Of record

| Quantity | Value |
|---|---|
| Hard points Fire Bolt / Inferno / Enchant | **20 / 20 / 3** |
| **Final sheet slvl** (BO + BC + Frozen Armor on): Fire Ball / Meteor / Fire Mastery / Fire Bolt / Inferno / Enchant | **46 / 46 / 46 / 46 / 46 / 29** |
| Charms, no BC | 45 / 45 / 45 / 45 / 45 / 28 |
| No charms | 34 / 34 / 34 / 34 / 34 / 17 |
| **Synergies** (J4b H01–H03, hard points only) | **Fire Ball +560 %** (14 × (20 + 20)) · **Meteor impact +200 %** (5 × (20 + 20)) · **burning ground +60 %** (3 × 20) |
| Unchanged | Warmth 27, Static Field 16, Frozen Armor 16, Teleport 16; every non-skill sheet field |

**Superseded:** stage 5's **17 / 1 / 1** hard points (sheet 43 / 27 / 27; synergies +518 / +185 / +3 %). **Reason:** stage 5 read `profile.skills` alone, which is 86 points and leaves 24 unspent. KP-444 rules those 24 are spent.

Stages 2–4 are unaffected either way: Frozen Armor and Static Field have 1 hard point in both readings, and no damage was computed.

---

## 11. Stage 7: facts for drax's J4b kit open questions

Source questions: `reincarnated-godot/kc2_play/join/J4B-KIT-OPEN-QUESTIONS.md` (godot `bc3c656`; read-only). Gamora rules them in ADDENDUM-12.

Files: `c14_stage7.json`, `scripts/c14_stage7.py`, `verification_stage7.log`. Captures: `captures/stage7/` (D2MOO `D2Seed.cpp/.h`, `Path.cpp`, `PathMisc.cpp`, `PathUtil.cpp`, `Step.cpp`; Basin Fire Ball, Meteor, Missile, Stamina, Faster Run/Walk). They are also reused from C-13: `captures/d2moo-MissMode.cpp`, `-Missiles.cpp`, `-SUnitDmg.cpp`, `-Units.cpp`, `captures/potions/`, `universal_player_laws.json`.

Code is D2MOO `5596f5cb` (1.10f). "Code" grades are **MODEL-VERIFIED** when a community source agrees, and **code-only** otherwise.

### The RNG primitive (for Q1–Q4)

D2's per-unit seed is a two-word LCG (`D2Seed.h`):
- `SEED_RollRandomNumber`: `lSeed = nHighSeed + 0x6AC690C5 · nLowSeed` (64-bit). The new low word is the next `nLowSeed`, the high word the next `nHighSeed`. It returns the 64-bit value; `ITEMS_RollRandomNumber` is used with `% 100` or `& mask`.
- `SEED_RollLimitedRandomNumber(n)` returns **`roll & (n−1)` if n is a power of two, otherwise `(uint32)roll % n`**. **The result is in [0, n−1].**

Grade: code-only. This seed form is long-standing community knowledge, but no second source was captured this stage.

### Q1 · Spell damage roll (context)

- **Each damage type** is rolled as **`min + RollLimited(missile.pSeed, max − min)`** in 1/256 points (`MissMode.cpp` `MISSMODE_RollDamageValue` L281–314).
  - So the range is **[min, max − 1/256]**: the maximum is exclusive by 1/256.
  - Mastery (Fire Mastery %) is applied to min and max **before** the roll.
  - The draw is on the **missile's own seed**, not the caster's.
- **Fire Ball:** `SrvHit01` rolls **once per explosion** (`MISSMODE_GetDamageValue`), then applies **that same damage to every unit in the 4-subtile radius** (`sub_6FD10200`; L2087–2121).
- **Meteor impact:** `SrvHit14` rolls **once per impact** (`FillDamageParams`) and applies it to all units in radius (L2746–2795).
- **How the missile's seed is initialised from the caster was not traced.**

Grade: code-only. Basin agrees that radius targets share the explosion, but does not address the roll.

### Q2 · Meteor pyre per-frame value: ROLLED EACH COLLISION, not fixed

- Each pyre missile (`meteorfire`, `pSrvDoFunc` 5, `pSrvDmgFunc` 3) collides with an overlapping unit and calls `MISSMODE_FillDamageParams`. That **rolls fire = min + RollLimited(missile.pSeed, max − min)** from the missile's min/max bit rate (H03) on **every collision**.
- `SrvDmg03` then draws **`(RollRandomNumber(missile.pSeed) & 127) < 19`** for a soft hit (L4387–4396).
- A collision occurs every frame for DamageRate-41 missiles (Basin Missile: *"those with 41 typically apply damage every frame (25 times per second)"*).

**So: one fire roll plus one soft-hit draw per pyre missile, per overlapped unit, per frame, on that pyre missile's seed.** Grade: **MODEL-VERIFIED** (code + Basin frame rate).

### Q3 · Potion double-fill draw form (context)

`SkillItem.cpp` `pSpell03` L196 (health) and L212 (mana):

```
if (Vit > 0 && (RollRandomNumber(unit.pSeed) % 100) < RollLimited(unit.pSeed, Vit) / 2)  value *= 2
```

- Two draws on **the drinker's own seed**.
- **⚑ The order of the two draws is not fixed by the reconstruction:** C++ leaves operand evaluation order unspecified, and only the original binary's instruction order settles it. **UNVERIFIED.**
- The probability law itself is MODEL-VERIFIED (C-13 potions: matches Arreat on both branches).

### Q4 · Block and Oculus draw forms (context)

- **Block** (`SUnitDmg.cpp` `ApplyBlockOrDodge` L2722–2735): `chance = UNITS_GetBlockRate(..)`, then **÷3 if running**. Then **`RollRandomNumber(defender.pSeed) % 100 < chance` → block.** That is an **integer d100 on the defender's (her) seed**.
- **Oculus when struck** (`SkillItem.cpp` `EventFunc21` L1683–1708): requires **`DAMAGERESULTFLAG_GETHIT`**, then **`RollRandomNumber(owner.pSeed) % 100 < 25`**, an **integer d100 on her seed**.
- Both are MODEL-VERIFIED (code, plus Basin's percent semantics).
- **How the port serves these as streams is a JOIN design matter, not a D2 fact.**

### Q5 · Fire Ball geometry

| Item | Value | Grade |
|---|---|---|
| **Velocity units** | Missile path velocity = `(Vel << 8) · 75/100` (`Missiles.cpp` L123–146) = **3,840** for Vel 20. Per frame the position advances by `direction(|v| = 0x1000) × velocity >> 8` in FP16 coordinates (65,536 per subtile; `PathMisc.cpp`, `Step.cpp` `lutTanToDirection`) → **61,440 / 65,536 = 0.9375 subtile per frame = 23.44 subtiles/s = 15.6 yd/s** at 2/3 yd per subtile | MODEL-VERIFIED: the code reproduces the d2mods convention `Vel·Range/32` yd exactly |
| **Range** | 50 frames (2.0 s) → **46.9 subtiles = 31.25 yd** | DATAMINED + code |
| **Collision size** | `Size` 1 (small-unit footprint); `CollideType` 3; **`CollideKill` 1: it stops at the first unit (or wall) and does not pass through** | DATAMINED |
| **Explosion** | 4-subtile (2⅔ yd) radius **centred on the missile's position at impact**, one shared roll | MODEL-VERIFIED (H06) |
| **End of range / wall** | `HandleMissileCollision` calls the hit handler with `a4 = 1` when the frame count runs out or it hits a wall. With `a4 = 1` the handler falls through to the server hit function, so **the fireball explodes at range end and on walls**. `AlwaysExplode` is blank; the `a4` path makes it unnecessary | **Code-only, single reading of a complex control flow: moderate confidence** |

Aim and target choice are NOT D2 data questions (Q6 is out of this scope).

### Q7 · The 18 pyre offsets and footprint (DATAMINED from code)

`MISSMODE_CreateMeteor_MoltenBoulderSubmissiles`, J4b `primary_rows.json → missile_notes`. Subtiles from the impact point; all 18 spawn.

```
dx:  2 -2  0  0 -3  0  3 -1  1 -1  2 -4 -3 -1  0  1  3  4
dy: -2 -2  2  5  3  3  3  2  1 -1 -1 -2 -2 -3 -4 -3 -3 -2
```

- **Each pyre missile is `Size` 2** (Missiles.txt `meteorfire`), static, colliding every frame.
- How many overlap a target depends on its size and position (Basin: a size-2 target at centre typically overlaps 3, up to 6). Copied into `c14_stage7.json`.
- Overlap against GD radii is a JOIN modelling choice.

### Q8 · Monster hit recovery in 1.13

`SUnitDmg.cpp` L2090–2228; `sub_6FCC1870` returns TRUE meaning **no** get-hit.

**When it can happen:** only if the hit carries **`GETHIT`**.
- Fire Ball's missile has `GetHit` = 1.
- Pyre missiles do not; they carry only the 19/128 **soft hit**, which sets AI state 19 and refreshes the unit but is **not** a GetHit mode change.

**No get-hit if any of these holds:**
- the monster is **frozen**;
- the hit is **pure poison**;
- total damage **< 1 point**;
- the monster's **MonStats2 `mGH` (GetHit mode) flag is 0**.

**Threshold by hit class.** Divisor 8 for 1H swing/thrust and bow/crossbow; 32 for 2H swing vs small and club; 64 for 2H swing vs large; **16 for everything else, including spells**.

| Damage dealt | GetHit chance |
|---|---|
| < maxHP/16 | **0** |
| < maxHP/8 | **50 %** (`rand & 1`) |
| < maxHP/4 | **75 %** (no get-hit iff `rand & 3 == 0`) |
| otherwise | **100 %** |

**Length:** the monster's GH animation frames. **UNKNOWN from the txt tables** (they live in AnimData.d2).

**Who is immune:**
- **Diablo and Baal have `mGH` = 0, so they are immune to hit recovery** (DATAMINED). Mephisto and the Chaos seal classes have it.
- R1: **69 of 70 types have it.**
- Uniques share their base type's flag; there is no unique or champion branch in this function.

Grade: code-only for the thresholds; `mGH` is DATAMINED.

⚑ drax's note of "softhit 19/128" is the **pyre's soft-hit chance**, not the GetHit threshold.

### Q10 · Stamina and movement for the build-file sheet

| Item | Value | Grade |
|---|---|---|
| **Max stamina at clvl 99** (Vitality 535 incl. items) | **697** = 74 + 98 + (535 − 10) | MODEL-VERIFIED (C-13 universal laws: CharStats + Basin) |
| With BO +80 % | ~~**1,254** if BO's `skill_staminapercent` applies to the total~~ **1,179**. **⚑ Corrected in stage 8 (§ 12)** | ~~INFERRED~~ MODEL-VERIFIED (§ 12) |
| **Armour speed** | **Dusk Shroud 0, Monarch 0** (Armor.txt `speed`) → **no drain multiplier**. Drain 2 × RunDrain 20 × 1 = ~~**40/256 per running frame = 3.906/s**~~ **24/256 = 2.344/s after War Traveler's 40 % slower stamina drain. ⚑ Corrected in stage 8 (§ 12)** | DATAMINED + MODEL-VERIFIED |
| **Walk / Run velocity** | CharStats **WalkVelocity 6, RunVelocity 9** (Basin reads these as yd/s) | DATAMINED |
| **FRW 25** (War Traveler) | FRW_eff = ⌊150·25/(150+25)⌋ = **21** → **walk 6·1.21 = 7.26**, **run 9 + 6·0.21 = 10.26** (same units) | MODEL-VERIFIED (animation packet § 3.7: Basin + D2MOO) |

### Q11 · Chill on a monster's attack animation

`Units.cpp` `UNITS_UpdateAttackAnimRateAndVelocity` L1340–1417:

```
rate      = clamp(IAS_eff + STAT_ATTACKRATE, 15, 175)
animSpeed = rate · baseAnimSpeed / 100          (integer floor)
```

- `STAT_ATTACKRATE` starts at 100 for monsters (`Monster.cpp`), and chill adds its `coldeffect` (stage 4 § 8.1).
- The frame counter advances by `animSpeed` (1/256 frame) each tick, and the attack ends when `current + speed ≥ frameCount·256`. So **ticks = ceil(256·frames / floor(rate·baseSpeed/100))**.
- Example, base 256 and a 16-frame attack: **16 ticks normally; −25 → 22; −33 → 24; −40 → 27; −50 → 32** (`c14_stage7.json` has 8/12/16/20-frame examples).
- Non-attack modes use `velocitypercent` and `other_animrate` the same way.
- Grade: code-only. Basin's chill page gives the magnitude but not the rounding.

### Q14 · Belt drink order, and the Super Mana ×2

- **D2 has no "drink health" key.** The bottom row's four hotkeys each drink **that column's** bottom potion, and the column then drops down (`ItemMode.cpp`; PureDiablo; C-13 `potions_notes.md` item 10).
- **Choosing between a Full Rejuvenation and a Super Healing column is player behaviour, not a D2 rule**, so it is a JOIN policy ruling. D2 would drink whichever column the player presses.
- **Super Mana: the listed Sorceress value (500) ALREADY includes the ×2 class factor.** C-13 `potions.json` lists `total_mana_by_class` (Sorceress 500, Barbarian 250) and `sorceress_total_mana`. **Do not apply the class factor again.** MODEL-VERIFIED (code `ITEMS_GetBonusManaBasedOnClass` + Arreat tables).
- Rejuvenation has no class factor.

### Q17 · DoT duration units on players

- D2 lengths are **integer frames at 25 fps** (`dwPoisLen`, `dwBurnLen`, …, in `D2DamageStrc`).
- The player's poison length is floored: **`floor(len × (100 − PLR_eff) / 100)`**, with PLR_eff including the Hell −100 penalty and clamped to [−100, 75] (C-13 universal laws).
- Poison damage is per frame in 1/256 points. Burn has no resist row.
- **D2 itself never converts seconds.** Mapping GD seconds to D2 frames (e.g. `ceil(25·s)`) is a JOIN adapter choice.
- Grade: MODEL-VERIFIED (code + Basin Poison Length Reduced).

### Not in this stage's scope (from drax's list)

Q6 (targeting), Q9 (regen placement), Q12 (HITREC comparator), Q13 (Resilient cap), Q15 (Cruel window) and Q16 (wave boundaries) are design or pack questions, not D2 facts. Q12's D2 side is answered by Q8: the code uses strict `<` against maxHP/divisor.

---

## 12. Stage 8: stamina drain with "slower stamina drain", and BO on max stamina

Captures: `captures/stage8/d2moo-PlrModes.cpp`, `d2moo-D2StatList.cpp`. Script `scripts/c14_stage7.py` is updated, and `c14_stage7.json` and `verification_stage7.log` are regenerated.

### Run drain with War Traveler's 40 % slower stamina drain: 24/256 per frame (gamora is right)

`PlrModes.cpp` L255–293, run mode, outside town:

```
L  = 2 × CharStats RunDrain                 (Sorceress 20 → 40, in 1/256 points per frame)
L *= torso-armour speed / 10 + 1           (integer; Dusk Shroud speed 0 → ×1)
L += L × item_staminadrainpct / −100       (C integer division, truncates toward zero)
L  = max(L, 1)
```

- **The percentage applies AFTER the armour-speed multiplier,** as a subtraction of L × pct / 100 truncated toward zero. For non-multiples it rounds the reduction down in magnitude, i.e. keeps the drain slightly higher.
- `item_staminadrainpct` is the summed item stat. Here **War Traveler's 40 % is the only source**, so **40 + (−16) = 24/256 per running frame = 2.34 points per second**.
- At 0 stamina, running becomes walking (unchanged).
- Grade: **MODEL-VERIFIED.** Code is primary. Basin Stamina Drain (C-13 capture) describes "slower stamina drain" as a percentage reduction of the drain; the order relative to the armour factor and the truncation are code-only.
- **Supersedes stage 7's 40/256 (3.906/s),** which omitted War Traveler's stat.

### Battle Orders on max stamina: 1,179, not 1,254

- BO's `skill_staminapercent` is **op 1 on `maxstamina`** (ItemStatCost; DATAMINED).
- In `D2StatList.cpp` (case 1, L209–225), for a player owner, op 1 adds **`ComputeStatPercentage(nPreviousOpStatValue, …)`**. `nPreviousOpStatValue` is the stat's accumulated value **before** the op terms are added. That is the same arithmetic as op 11, which J4a F03 already showed does not reach item-Vitality life.
- **Basin Battle Orders:** *"Only applies to base stamina, including that from levelling up, points invested in Vitality and + Maximum Stamina items."*

**So BO multiplies base stamina only:** 74 + (99 − 1) + (allocated Vitality 441 − 10) = **603**, × 1.80 = **1,085**, plus the item Vitality's +94 (1 per point) = **1,179**.
- Grade: **MODEL-VERIFIED** (code + Basin).
- **Supersedes stage 7's INFERRED 1,254.**
- No-BO max stamina is unchanged at **697**.

### Seconds of running from full

| Max stamina | Drain 24/256 per frame | Seconds of running |
|---|---|---|
| 1,179 (with BO) | 2.344/s | ≈ **503 s** |
| 697 (without BO) | 2.344/s | ≈ 297 s |
