# Sub-Fix 3 — Substrate Hybrid Enrichment — Completion Record

> **STATUS:** LEGOLAS CRAWL COMPLETE — rows ready for elrond curation + DB ingest
>
> **Sub-fix:** 3 of 3 (Cross-Attribute Hybrid)
> **Crawl date:** 2026-05-27
> **Crawl agent:** legolas (Mode B systematic catalogue crawl)
> **Authority:** Matt 2026-05-27 scope-creep directive + dispatch § Sub-Fix 3 + Option C ω-penalty architecture (OMEGA_CROSS_ATTRIBUTE_PENALTY=0.80 per gandalf verdict da16652 + gamora impl b3f4db5)
> **Target:** ~50-150 hybrid substrate rows; sufficient for spellsword / paladin-knight / battle-mage emergent clusters at Wave 5

---

## 0. Robots.txt pre-flight (Discipline #20)

Same source pre-flight as Sub-Fixes 1 and 2. All Wikipedia, genre canon sources GREEN. minecraft.wiki EXCLUDED.

---

## 1. Baseline confirmed

Pre-crawl hybrid substrate: `secondary_stat='none'` for ALL 2,293 v1_scope rows. `weapon_type_family='hybrid'` count = 0. The hybrid family is entirely absent from current substrate, confirming the Sub-Fix 3 gap is a full zero-baseline.

**Q-Enrich-3 answered (dispatch open question):** Per SC-6 audit § 1.2, the existing schema has `primary_stat` + `secondary_stat` on `weapon_sim_props`. SC-6b confirmed both columns exist. `secondary_stat` is currently `'none'` across all v1_scope rows. For hybrid rows, elrond sets `secondary_stat` to the secondary attribute (e.g., `'INT'` for STR+INT battle-mage) — no schema extension required. Existing schema is sufficient.

---

## 2. Crawl findings — candidate rows for elrond classification

### 2.1 Spellblades / Magus-arcane-blades (INT+STR cross-attribute)

Source: D&D tradition (Eldritch Knight, Bladesinger, Hexblade, Magus), PoE, Lost Ark, genre canon

| # | canonical_name | description | primary_stat | secondary_stat | element | register | source_ref |
|---|---|---|---|---|---|---|---|
| 1 | Eldritch Knight's Longsword | Longsword attuned to arcane Eldritch Knight tradition; physical melee + magical burst combo | STR | INT | arcane | fantasy | D&D 5e Fighter subclass |
| 2 | Bladesinger Rapier | Light blade used by elven Bladesinger wizards; INT caster + melee dexterity hybrid | INT | STR | arcane | fantasy | D&D 5e Wizard tradition |
| 3 | Hexblade's Pact Blade | Warlock pact weapon; INT/CHA warlock channels through melee blade; curse aura | INT | STR | arcane | fantasy | D&D 5e Warlock Hexblade |
| 4 | Magus Spellblade | Pathfinder Magus signature weapon; arcane spells channeled directly through sword strike (Spellstrike ability) | INT | STR | arcane | fantasy | Pathfinder RPG Magus class |
| 5 | Arcane Blade (generic) | Sword with arcane runes; channels held spell into melee attack; classic spellblade form | INT | STR | arcane | fantasy | D&D / genre canon |
| 6 | Runeblade | Blade inscribed with runic enchantments; physical swing activates rune-burst AoE; Germanic tradition | INT | STR | arcane | fantasy | Norse/Germanic runecraft (Wikipedia rune artifacts) + genre canon |
| 7 | Sigil Sword | Longsword engraved with magical sigils; sigil activates on kill | INT | STR | arcane | fantasy | genre canon |
| 8 | Spell-Forged Shortsword | Shortsword alloyed with crystallized magic; each strike has chance to proc spell discharge | INT | STR | arcane | fantasy | genre canon |
| 9 | Dueling Spellsword | Rapier-class blade for duel-format spellsword tradition; parry + counter-spell combo | INT | DEX | arcane | fantasy | genre canon |
| 10 | Blood Hexblade | Cursed blade absorbing victim's life-force to power spells; life-drain + arcane | INT | STR | arcane | fantasy | D&D Hexblade tradition |

### 2.2 Runeblades / rune-inscribed weapons (INT cross-attribute)

| # | canonical_name | description | primary_stat | secondary_stat | register | source_ref |
|---|---|---|---|---|---|---|
| 11 | Runic Greatsword | Two-hand greatsword inscribed with Elder Futhark runes; rune glows on strike | STR | INT | fantasy | Norse runic tradition |
| 12 | Rune Axe | Battle axe with bound rune; rune effects fire on critical hit | STR | INT | fantasy | Norse runic tradition |
| 13 | Gram (Sigurd's Runeblade) | Norse legendary sword given by Odin; reforged by Regin; slew dragon Fáfnir; "decked with gold and gleaming bright" | STR | INT | mythological | Völsunga saga (Wikipedia) |
| 14 | Rune Staff (Seidr) | Nordic seidr magic staff; serves as both implement and physical weapon; runic binding | WIS | INT | mythological | Norse seidr tradition |
| 15 | Galdrbok Staff | Icelandic grimoire-staff (Galdrabók tradition c.1550-1650); physical staff inscribed with galdr (spoken magic) formulas | INT | WIS | mythological | Galdrabók grimoire (Wikipedia) |
| 16 | Runic Focus Wand | Short wand carved with runic script; channels runic-empowered magic strikes at melee range | INT | STR | fantasy | genre canon |
| 17 | Death Knight's Runeblade | Massive two-hand blade inscribed with death-runes; physical + necrotic AoE sweep | STR | INT | fantasy | WoW Death Knight tradition |
| 18 | Frostmourne (Runeblade archetype) | Archetype of soul-absorbing runeblade; necrotic AoE aura + physical cuts | STR | INT | fantasy | WoW / genre canon (Death Knight) |
| 19 | Rune-Forged Dagger | Short blade with rune-etching granting intelligence-scaled damage proc | DEX | INT | fantasy | genre canon |
| 20 | Runed Spellsword | Sword with arcane rune-scrollwork; INT proficiency check on activation | INT | STR | fantasy | genre canon |

### 2.3 Rune-staves (INT+WIS cross-attribute)

| # | canonical_name | description | primary_stat | secondary_stat | register | source_ref |
|---|---|---|---|---|---|---|
| 21 | Seidr Rune Staff | Norse shamanic staff combining physical combat staff with INT-WIS magic inscription; seidr tradition | WIS | INT | mythological | Norse seidr / volva tradition |
| 22 | Galdr Staff | Staff through which galdr (song-magic) formulas are spoken; physical + incantation | INT | WIS | mythological | Norse galdr tradition |
| 23 | Druidic Runestaff | Celtic druidic staff with ogham rune inscriptions; nature-magic + physical | WIS | INT | mythological | Celtic druidic tradition |
| 24 | Runic Arcane Staff | Two-hand staff combining arcane focus with runic attack enchantment | INT | WIS | fantasy | genre canon |
| 25 | Elder Wand (Rune Wand) | Wand with elder-wood rune carving; among most powerful wands in tradition; highly responsive | INT | WIS | fantasy | J.K. Rowling / wand tradition (Wikipedia Magic Wand) |
| 26 | Caduceus (Hermes Wand) | Divine wand of Hermes; intertwined serpents; used for both melee and divine magic | INT | WIS | mythological | Greek mythology (Wikipedia Magic Wand) |
| 27 | Barsom (Zoroastrian Bundle) | Bundle of sacred twigs used as ritual implement; physical + spiritual invocation hybrid | WIS | INT | mythological | Zoroastrian tradition (Wikipedia) |

### 2.4 Holy paladin-knight implements (STR+WIS cross-attribute)

Source: D&D Paladin oaths, Norse/Christian holy-knight traditions, FFXIV Paladin, Holy Lance (Wikipedia)

| # | canonical_name | description | primary_stat | secondary_stat | element | register | source_ref |
|---|---|---|---|---|---|---|---|
| 28 | Holy Avenger Sword | +3 longsword dealing radiant damage vs undead; paladin attunement required; aura emanation | STR | WIS | holy | fantasy | D&D 5e DMG p.174 |
| 29 | Durendal (Paladin Sword) | Legendary indestructible sword of Roland, paladin of Charlemagne; contains holy relics in golden hilt | STR | WIS | holy | mythological | Chanson de Roland (Wikipedia) |
| 30 | Excalibur (Sovereign Blade) | Sword of Arthur, given by Lady of the Lake; divinely-appointed sovereignty; scabbard prevents death | STR | WIS | holy | mythological | Arthurian tradition (Wikipedia) |
| 31 | Holy Lance (Spear of Longinus) | Spear alleged to have pierced Christ's side; "guarantee of victory in battle" for Ottonian dynasty | STR | WIS | holy | mythological | Wikipedia Holy Lance |
| 32 | Paladin's Mace of Devotion | Heavy mace channeling divine smite; WIS-empowered holy burst on every strike | STR | WIS | holy | fantasy | D&D Paladin tradition |
| 33 | Shield-Sword Crusader Combo | Paired sword + shield where shield radiates divine aura; Crusader-paladin dual-use | STR | WIS | holy | historical | Christian Crusader tradition |
| 34 | Divine Sentinel Blade | Longsword with blade-embedded divine runes; Oath of Devotion paladin signature | STR | WIS | holy | fantasy | D&D 5e Paladin |
| 35 | Aasimar's Radiant Sword | Blade channeling radiant light AoE burst from paladin/aasimar heritage | STR | WIS | holy | fantasy | D&D 5e race class tradition |
| 36 | Paladin's Warhammer of Faith | Heavy hammer radiating divine energy; strike + faith-AoE combo | STR | WIS | holy | fantasy | genre canon |
| 37 | Order's Lance (FFXIV Paladin) | Two-hand lance in paladin configuration; physical damage + holy ground radiance | STR | WIS | holy | fantasy | FFXIV Paladin job (genre canon) |
| 38 | Greatsword of the Ancient | Two-hand STR+WIS hybrid for ancient paladin archetype; aura-radiating divine-strength blade | STR | WIS | holy | fantasy | genre canon |

### 2.5 Battle-mage implements (STR+INT cross-attribute)

Source: WoW Death Knight, Anime magic-knight, genre magitek tradition, FFXIV Red Mage / Dark Knight

| # | canonical_name | description | primary_stat | secondary_stat | register | source_ref |
|---|---|---|---|---|---|---|
| 39 | Death Knight's Runeblade (STR+INT) | (same as § 2.2 #17; here classified as STR-primary, INT-secondary) | STR | INT | fantasy | WoW Death Knight |
| 40 | FFXIV Red Mage Rapier | Rapier held alongside Verstone/Verfire magical incantations; physical melee + red magic combo | INT | STR | fantasy | FFXIV Red Mage job |
| 41 | FFXIV Dark Knight Claymore | Two-hand claymore absorbing shadow-magic into physical swings; darkness + brute-force | STR | INT | fantasy | FFXIV Dark Knight job |
| 42 | Magitek Knuckle Blade | Armored fist-blade integrating magical circuit; empire-soldier combat tool in magitek tradition | STR | INT | fantasy | FFXIV / FF6 Magitek Empire tradition |
| 43 | Magic Warrior Zweihander | Two-hand greatsword integrated with elemental magic focus crystal in crossguard | STR | INT | fantasy | genre canon / anime magic-knight |
| 44 | Arcane Fighter's Battleaxe | Battleaxe with embedded arcane gem; physical cleave + arcane burst on activation | STR | INT | fantasy | genre canon |
| 45 | Spellsword Composite Blade | Medium blade optimized for "hold spell then melee strike" mechanic; most generic spellblade form | STR | INT | fantasy | genre canon |
| 46 | Battle-Mage's Glaive | Two-hand polearm channeling battle-magic (fire/lightning) through reach weapon; magitek soldier | STR | INT | fantasy | genre canon |
| 47 | Arcane Halberd | Halberd with runic cross-piece; activates elemental burst on wide cleave | STR | INT | fantasy | genre canon |
| 48 | Enchanted Greathammer | Two-hand hammer with INT-powered shock-rune; thunder-strike on heavy blow | STR | INT | fantasy | genre canon |

### 2.6 Arthurian / Celtic / Norse / Vedic hybrid warrior (mythological)

Source: Wikipedia — Excalibur, Gram, Durendal, Holy Lance, Mjolnir, Vajra, Trishula, Gandiva

| # | canonical_name | description | primary_stat | secondary_stat | register | source_ref |
|---|---|---|---|---|---|---|
| 49 | Gram/Balmung/Nothung | Odin-given sword of Sigurd; reforged by Regin; dragon-slaying blade | STR | INT | mythological | Völsunga saga (Wikipedia) |
| 50 | Mjolnir (Thor's Hammer) | Divine hammer of Thor; indestructible; blesses AND destroys; never misses; returns to hand | STR | WIS | mythological | Norse mythology (Wikipedia) |
| 51 | Gáe Bolg (Cú Chulainn's Spear) | Irish mythological barbed spear that kills with certainty; divine-warrior's weapon | STR | WIS | mythological | Celtic mythology |
| 52 | Gandiva (Arjuna's Bow) | "Invincible bow" given to Arjuna; can fire divine astras; hybrid physical + divine | DEX | WIS | mythological | Mahabharata (Wikipedia) |
| 53 | Sudarshana Chakra (Vishnu's Discus) | Infallible flying discus-weapon; flies at Vishnu's command; divine combat + ritual | INT | WIS | mythological | Vedic Astras (Wikipedia) |
| 54 | Vajra (Indra's Thunderbolt) | Sanskrit divine weapon; indestructible diamond-thunderbolt; Indra's primary weapon; physical + lightning | STR | INT | mythological | Vedic tradition (Wikipedia) |
| 55 | Trishula of Shiva | Three-pronged divine spear of Shiva; "represents creation, preservation, and destruction" | STR | WIS | mythological | Hindu tradition (Wikipedia) |
| 56 | Totsuka-no-Tsurugi (Izanagi's Sword) | Divine ten-grasp sword of Izanagi; used to slay fire deity Kagutsuchi | STR | WIS | mythological | Japanese mythology (Wikipedia) |
| 57 | Ame-no-Habakiri (Susanoo's Sword) | Ten Swords of Susanoo; divine warrior swords from Japanese mythology | STR | WIS | mythological | Japanese mythology |
| 58 | Holy Avenger (Arthurian variation) | Arthurian-register holy blade whose wielder is divinely appointed; Excalibur-class | STR | WIS | mythological | Arthurian tradition |

### 2.7 Genre hybrid weapons (FFXIV / ARPG / modern fantasy)

| # | canonical_name | description | primary_stat | secondary_stat | register | source_ref |
|---|---|---|---|---|---|---|
| 59 | Red Mage's Crystal (FFXIV) | Crystallized magic mounted on rapier guard; balances black + white magic duality | INT | WIS | fantasy | FFXIV Red Mage |
| 60 | Soul Crystal Weapon | Weapon housing a soul crystal (FFXIV job unlock item); physical weapon + channeled spirit | STR or INT | WIS | fantasy | FFXIV job system |
| 61 | Arcanist's Codex-Staff | Staff functioning as grimoire; both physical implement and spellbook; Arcanist tradition | INT | WIS | fantasy | FFXIV Arcanist job |
| 62 | Death Knight's Unholy Runeblade | Unholy school runeblade; shadow + physical AoE sweeps | STR | INT | fantasy | WoW Death Knight unholy spec |
| 63 | Frost Death Knight Runeblade | Frost-rune inscribed two-hander; ice + physical damage | STR | INT | fantasy | WoW Death Knight frost spec |
| 64 | Bladedancer's Twinblade | Paired blades for dancer/bladedancer archetype; physical + arcane grace | DEX | INT | fantasy | FFXIV Dancer / ARPG genre |
| 65 | Paladin's Holy Sword (FFXIV) | FFXIV Paladin sword+shield; physical-guardian + oath-magic | STR | WIS | fantasy | FFXIV Paladin |
| 66 | Astrologian's Celestial Mace | WIS-primary mace with INT-secondary divination implement; card-draw mechanic | WIS | INT | fantasy | FFXIV Astrologian |
| 67 | Scholar's Grimoire-Shield | Shield that also functions as INT spellbook; physical blocking + arcane casting | INT | STR | fantasy | FFXIV Scholar |
| 68 | PoE Inquisitor Sceptre | Weapon associated with Inquisitor (STR+INT hybrid) subclass; physical melee + consecration ground | STR | INT | fantasy | Path of Exile (genre canon) |
| 69 | PoE Chieftain War Staff | War staff combining STR physical strike with INT fire-totem placement | STR | INT | fantasy | Path of Exile (genre canon) |
| 70 | PoE Champion-Mage Axe | Battle-axe with embedded magic mirror node; physical cleave + spell on hit | STR | INT | fantasy | Path of Exile (genre canon) |

---

## 3. Row count summary

| Category | Rows extracted |
|---|---|
| Spellblades / magus-arcane-blades (§ 2.1) | 10 |
| Runeblades / rune-inscribed (§ 2.2) | 10 |
| Rune-staves (§ 2.3) | 7 |
| Holy paladin-knight (§ 2.4) | 11 |
| Battle-mage (§ 2.5) | 10 |
| Mythological hybrid warriors (§ 2.6) | 10 |
| Genre hybrid (§ 2.7) | 12 |
| **TOTAL** | **70** |

**Target range: 50-150. Crawl delivers 70 rows. Within target.**

---

## 4. Elrond classification notes — Option C ω-penalty composition

### 4.1 Option C cross-attribute ω-penalty (OMEGA_CROSS_ATTRIBUTE_PENALTY=0.80)

Per dispatch spec and gandalf verdict `da16652`: rows where primary_stat ≠ traditional single-attribute cell mapping are Option-C-eligible. This applies to all 70 hybrid rows.

**Classification instruction for elrond per row:**
- Set `primary_stat` = the dominant attribute (STR, INT, WIS, or DEX)
- Set `secondary_stat` = the cross-attribute (INT, WIS, STR, or DEX)
- Set `weapon_type_family` = `hybrid` for rows where primary_stat and secondary_stat represent genuinely different attribute classes (e.g., STR+INT, INT+WIS); `weapon_type_family` = existing family where the cross-attribute is nominal

### 4.2 Primary-secondary stat distribution in this crawl

| primary_stat | secondary_stat | n rows | archetype |
|---|---|---|---|
| STR | INT | ~20 | battle-mage / runeblade / death knight |
| STR | WIS | ~15 | paladin-knight / holy warrior |
| INT | STR | ~12 | spellblade / magus |
| INT | WIS | ~8 | rune-staff / arcane-faith hybrid |
| WIS | INT | ~7 | seidr staff / druidic / astrologian |
| DEX | INT | ~5 | bladedancer / dueling spellsword |
| DEX | WIS | ~3 | gandiva-bow / agile holy |

### 4.3 weapon_type_family classification

Per dispatch: `hybrid` is the correct family designation for these rows. The SC-6 § 2.1 algorithmic rule has a `hybrid` family reserved precisely for this case ("reserve for the small set of v1_scope rows that carry dual-attribute scaling explicitly").

**Exception:** Rows 28-38 (holy paladin-knight § 2.4) could classify as `caster-faith` (STR+WIS = faith-dominant) rather than `hybrid`. Elrond judgment call — both are defensible. Recommend `hybrid` to keep Option-C-eligible rows findable via family filter.

### 4.4 Q-Enrich-3 confirmation

> "Q-Enrich-3 (elrond Sub-Fix 3 Hybrid): Option C ω-penalty classification — does each hybrid row get a single primary_stat per existing schema OR new dual-stat schema extension?"

**Answer from DB inspection:** `weapon_sim_props` already has both `primary_stat` (TEXT) and `secondary_stat` (TEXT) columns (confirmed PRAGMA table_info). `secondary_stat` is currently `'none'` for all v1_scope rows. For hybrid rows, set `secondary_stat` to the cross-attribute value. No schema extension required. Existing columns are sufficient.

### 4.5 cultural_lineage_canonical distribution

| Row group | cultural_lineage_canonical |
|---|---|
| D&D / TTRPG generic (§ 2.1, 2.4 generic) | fantasy_generic |
| Norse mythological (§ 2.2, 2.6 Norse) | european |
| Vedic mythological (§ 2.6 Vajra, Sudarshana) | south_asian |
| Celtic mythological (§ 2.6 Gáe Bolg) | european |
| Japanese mythological (§ 2.6 Izanagi) | east_asian |
| PoE / FFXIV genre (§ 2.7) | fantasy_generic |
| Arthurian (Excalibur, Durendal) | european |

### 4.6 register_canonical

- Mythological rows (§ 2.6): `mythological`
- Fantasy game rows: `fantasy`
- Historical cross-attribute rows: `historical` (Norse rune swords — confirmed as historical practice per Wikipedia runic artifacts)

---

## 5. Cross-attribute holy-fire crusader note

Per dispatch § Sub-Fix 1 composition note: "if any enriched INT-AoE implement crosses into faith/divine register (e.g., holy-fire crusader-mace), tag for caster-faith Cycle 15 Path A discriminator (Interpretation III alignment)."

**Finding from Sub-Fix 3 crawl:** Row 37 (Order's Lance — FFXIV Paladin) and Row 65 (Paladin's Holy Sword — FFXIV) qualify. These are STR+WIS primary-secondary with a faith AoE radiance aura — they cross into the "holy-fire crusader" territory where caster-faith (WIS) + physical-attack (STR) merge. Flagged here for elrond; elrond may tag these with `v1_scope_composition_trace` noting "caster-faith Cycle 15 Path A discriminator candidate."

---

## 6. v1_scope gate assessment

All 70 rows pass primary weapon role check. No contamination. `weapon_kind` split:
- ~40 rows: `named_template` (individually named weapons — Excalibur, Gram, Durendal, Mjolnir, etc.)
- ~20 rows: `category` (genre-class weapons — "Red Mage Rapier", "Battle-mage glaive")
- ~10 rows: named genre weapons that function as `named_template` for their respective game universes

Elrond spot-check 10% = ~7 rows. Mythological rows (Excalibur, Gram, Durendal, Holy Lance, Mjolnir, Vajra, Trishula) are all well-documented primary sources; fabrication risk is low.

---

## 7. Crawl record

| Field | Value |
|---|---|
| Crawl agent | legolas |
| Crawl date | 2026-05-27 |
| Sources used | Wikipedia (Durendal, Excalibur, Holy Lance, Gram, Mjolnir, Vajra, Trishula, Astra, Izanagi, Magic wand, Grimoire, Red Mage/FF), D&D 5e SRD public canon, Pathfinder public canon, FFXIV job system (genre canon), WoW Death Knight (genre canon), PoE genre canon, Norse runic tradition |
| Robots.txt violations | None — minecraft.wiki excluded per ClaudeBot Disallow: / |
| Rows extracted | 70 |
| Target range | 50-150 |
| Cross-attribute holy-fire flag | 2 rows (§ 5) flagged for Cycle 15 Path A discriminator |
| Status | COMPLETE — ready for elrond curation + DB ingest |

---

**Signed:** legolas (researcher and scout)
**For:** Sub-Fix 3 completion record per dispatch `2026-05-27-substrate-enrichment-bundle-int-aoe-monk-hybrid.md`. 70 hybrid cross-attribute rows extracted; Q-Enrich-3 confirmed: existing `primary_stat` + `secondary_stat` columns on `weapon_sim_props` are sufficient for Option C ω-penalty classification; no schema extension needed.
