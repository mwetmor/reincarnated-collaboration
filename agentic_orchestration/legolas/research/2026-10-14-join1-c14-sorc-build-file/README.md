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
| Skill progression | Plus 24 more points: Fire Bolt +3, Inferno +19, Enchant +2. **Final at 99: Fire Bolt 20, Inferno 20, Enchant 3** (110 points = 98 + 12 quest). This matches the guide's "max in order Meteor, Fire Mastery, Fire Ball, Fire Bolt, Inferno, Enchant" |

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
| **slvl** Fire Ball / Meteor / Fire Mastery / Fire Bolt / Inferno | **45 / 45 / 45 / 45 / 45** | same | 34 each | same | 31–33 (Fire Bolt unpinned) |
| slvl Warmth / Enchant / Frozen Armor | 26 / 28 / 15 | same | 15 / 17 / 11 | same | — |
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
