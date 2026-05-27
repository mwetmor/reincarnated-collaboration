# Sub-Fix 2 — Substrate Monk Enrichment — Completion Record

> **STATUS:** LEGOLAS CRAWL COMPLETE — rows ready for elrond curation + DB ingest
>
> **Sub-fix:** 2 of 3 (Monk / WIS-melee-light)
> **Crawl date:** 2026-05-27
> **Crawl agent:** legolas (Mode B systematic catalogue crawl)
> **Authority:** Matt 2026-05-27 scope-creep directive + dispatch § Sub-Fix 2
> **Target:** ~50-100 WIS-melee-light substrate rows; sufficient for monk emergent cluster at Wave 5

---

## 0. Robots.txt pre-flight (Discipline #20)

Same source pre-flight as Sub-Fix 1. All Wikipedia, Wikidata sources GREEN. minecraft.wiki EXCLUDED.

---

## 1. Baseline confirmed

Pre-crawl WIS-melee substrate (proxy_range_class=melee):

| weapon_kind | proxy_range_class | subtype | n |
|---|---|---|---|
| named_template | melee | handheld_weapon | 66 |
| category | melee | (various) | 35 |
| unique | melee | (mixed) | 2 |
| **Total WIS-melee** | | | **103** |

**Critical distinction:** These 103 rows are almost entirely `mace`-form — they represent the WIS-Faith-Mace Crusader archetype (#31 in Stage 1 audit). The monk-specific substrate (unarmed + martial-arts + knuckle + monk-staff + sash-weapons) is 0 rows as confirmed by Stage 1 audit § 3.2 "WIS × close-melee dagger/martial-light: 0 named+unique rows."

---

## 2. Crawl findings — candidate rows for elrond classification

### 2.1 Unarmed implements (physical fist-load / claw weapons)

Source: Wikipedia — Knuckle duster, Bagh nakh, Cestus, Tekko, Emeici

| # | canonical_name | description | cultural_lineage | historical_period | register | combat_geometry |
|---|---|---|---|---|---|---|
| 1 | Brass Knuckles | Metal hand weapon concentrating punch force into smaller contact area; hardened-steel variants; used WWII era | fantasy_generic | industrial | historical | single / multi-hit |
| 2 | Iron Fist (knuckleduster) | Classic knuckleduster; round-hole design fitting over all four fingers | european | industrial | historical | single |
| 3 | Apache Revolver Knuckle | Triple-function combination weapon: brass knuckles + revolver + dagger; concealed weapon | european | industrial | historical | single |
| 4 | Mark I Trench Knife | US WWI knuckle-knife; brass knuckle guard + blade; combat role = stabbing + punching | european | industrial | historical | single |
| 5 | Bagh Nakh (Tiger Claw) | Indian fist-load claw weapon: 4-5 curved blades on crossbar; conceals under palm; Maratha tradition | south_asian | pre_classical–early_modern | historical | multi-hit |
| 6 | Vagh Nakhya (Shivaji's Tiger Claw) | Named variant of bagh nakh associated with Maratha emperor Shivaji; legendary use vs. Afzal Khan | south_asian | early_modern | mythological | multi-hit |
| 7 | Nihang Sikh Bagh Nakh | Wrestling variant used in Nihang Sikh naki ka kusti tradition | south_asian | early_modern | historical | multi-hit |
| 8 | Cestus (Caestus) | Ancient Greek/Roman boxing glove weapon; hand-wrap reinforcement for competition boxing | european | pre_classical | historical | single |
| 9 | Tekko (Okinawan Fist-Load) | Okinawan horseshoe-shaped metal weapon fitting over knuckles; agricultural-implement origin | east_asian | early_modern | historical | single |
| 10 | Tekkokagi (Claw-Hook Tekko) | Tekko variant with four iron nails like bear claws; slashing and ensnaring | east_asian | early_modern | historical | multi-hit |
| 11 | Emeici (Emei Piercer) | Chinese paired metal rods on middle-finger rings; spinning stabbing weapon; concealment design | east_asian | pre_classical–classical | historical | multi-hit |
| 12 | Emei Dagger Pair | Paired emeici in competitive wushu configuration; fast spinning disorientation attack | east_asian | contemporary | historical | multi-hit |
| 13 | Knuckle Knife (Spiked Brass) | Knuckleduster with blade or spike extensions; melee combo | european | industrial | historical | single |
| 14 | Cuchillo de Paracaidista | Argentine paratroop knuckle-knife variant | south_american_indigenous | modern | historical | single |

### 2.2 Monk staves (bo, shakujo / khakkhara, jo)

Source: Wikipedia — Bo weapon, Shakujo/Khakkhara, Jo weapon, Shaolin Kung Fu, Wushu

| # | canonical_name | description | cultural_lineage | historical_period | register | combat_geometry |
|---|---|---|---|---|---|---|
| 15 | Bo Staff | Six-foot hardwood staff; signature Shaolin monk weapon; "forte of the Shaolin monks" | east_asian | classical–contemporary | historical | single / cleave |
| 16 | Shakujo (Buddhist Monk Staff) | Buddhist pilgrim/monk staff with metal rings at top; rings alert animals; rings used to blind enemies; pointed metal butt | east_asian | classical | mythological | single |
| 17 | Khakkhara (Pewter Staff) | Sanskrit variant of shakujo; carried by Buddhist monks as authority symbol; Shorinji Kempo combat tradition | south_asian | classical | mythological | single |
| 18 | Jo Staff | Japanese staff (~1.27m); shorter than bo; invented by Musō Gonnosuke after defeat by Miyamoto Musashi; still used by Japanese police | east_asian | early_modern | historical | single |
| 19 | Hanbo (Half-Staff) | Three-foot shorter staff; intermediate between jo and walking cane; common patrol/monk carry | east_asian | early_modern | historical | single |
| 20 | Shaolin Gun (Monk Staff) | Wushu-category staff used in Shaolin martial arts competition and kata forms | east_asian | classical–contemporary | historical | single |
| 21 | Tin Staff (Sengchou's) | Named staff associated with Sengchou of Shaolin; "skill with the tin staff and empty-hand strikes" | east_asian | classical | mythological | single |
| 22 | Jōdō Staff | Training version of jo for paired practice; jōjutsu school implement | east_asian | early_modern | historical | single |
| 23 | Aiki-Jo | Aikido variant of jo staff; demonstrates aikido principles via weapon form | east_asian | modern | historical | single |
| 24 | Trishula Staff (Shiva) | Trident staff carried by Shiva; three-pronged spear-staff hybrid; combat + divine implement | south_asian | pre_classical | mythological | single / cleave |
| 25 | Ame-no-Nuboko (Jeweled Spear-Staff) | Creation spear of Izanagi and Izanami; jeweled divine staff-spear used to churn creation | east_asian | pre_classical | mythological | single |
| 26 | Nangun (Southern Monk Staff) | Wushu nangun form staff; distinct from northern gun in shorter technique pattern | east_asian | classical | historical | single |

### 2.3 Sash / chain / flexible weapons (monk tradition)

Source: Wikipedia — Sansetsukon, Kusari-fundo, Chain whip, Rope dart, Nunchaku

| # | canonical_name | description | cultural_lineage | historical_period | register | combat_geometry |
|---|---|---|---|---|---|---|
| 27 | Nunchaku | Two wooden/metal sections connected by chain; Okinawan/Shaolin origin; iconic Bruce Lee weapon | east_asian | early_modern | historical | multi-hit |
| 28 | Nunchucks (Modern) | Modern polymer/metal variant of nunchaku; training and demonstration use | east_asian | contemporary | historical | multi-hit |
| 29 | Sansetsukon (Three-Section Staff) | Three wooden staves connected by metal rings; Chinese origin; operates at long/mid/short range | east_asian | classical | historical | multi-hit / cleave |
| 30 | Sanjiebian (Three-Section Whip) | Three-section whip variant; soft weapon relative | east_asian | classical | historical | multi-hit |
| 31 | Kusari-fundo (Manrikigusari) | Japanese chain weapon with weighted ends; "ten-thousand-power chain"; concealed weapon; Edo period police | east_asian | early_modern | historical | single / cleave |
| 32 | Manriki (Short Chain) | Compact version of kusari-fundo; ultra-concealable; non-lethal arresting tool | east_asian | early_modern | historical | single |
| 33 | Kusarigama (Chain-Sickle) | Kama sickle with chain attachment; versatile melee + reach weapon | east_asian | early_modern | historical | cleave |
| 34 | Kyoketsu Shoge | Hook-blade on cord; related to kusarigama; reach + entangle | east_asian | early_modern | historical | single |
| 35 | Jiujiebian (Nine-Section Whip) | Nine-section metal chain whip; "powerful hidden weapon"; Jin Dynasty first use; wushu competition form | east_asian | classical | historical | multi-hit |
| 36 | Qijiebian (Seven-Section Whip) | Seven-section variant of chain whip | east_asian | classical | historical | multi-hit |
| 37 | Rope Dart (Shengbiao) | Metal spike on 3-5m rope; Chinese martial arts; spinning + projectile technique; precursor: meteor hammer | east_asian | classical | historical | single |
| 38 | Meteor Hammer | Heavy weighted balls on chains; large-radius spinning AoE pattern; cousin weapon to rope dart | east_asian | classical | historical | AoE |
| 39 | Drunken Staff (Zui Gun) | Bo-staff wielded in drunken-boxing (zui quan) unpredictable patterns; Shaolin tradition | east_asian | classical | historical | single |

### 2.4 Tonfa / sai / kama (Okinawan monk tradition)

Source: Wikipedia — Tonfa, Sai, Kama

| # | canonical_name | description | cultural_lineage | historical_period | register | combat_geometry |
|---|---|---|---|---|---|---|
| 40 | Tonfa (T-Baton) | Okinawan perpendicular-handle stick; forearm-guard + strike + hook mechanics; origins debated (China/Okinawa/SEA) | east_asian | early_modern | historical | single |
| 41 | Tuifa (Chinese Tonfa) | Chinese variant of tonfa; guǎi (crutch-like); southern Chinese tradition | east_asian | early_modern | historical | single |
| 42 | Tonfa Pair | Tonfas wielded in pairs; standard Okinawan kobudō form | east_asian | early_modern | historical | single / multi-hit |
| 43 | PR-24 Side-Handle Baton | Modern law-enforcement tonfa derivative; rubber construction | east_asian | modern | historical | single |
| 44 | Sai (Stabbing Trident) | Okinawan metal stabbing weapon; three-prong; police ufuchiku arrest tool; "fast stabbing and strikes" | east_asian | early_modern | historical | single |
| 45 | Manji Sai (Reversed-Prong) | Sai variant with one reversed side prong; distinct capture/parry mechanic | east_asian | early_modern | historical | single |
| 46 | Nicho Sai (Paired Sai) | Sai wielded in pairs | east_asian | early_modern | historical | multi-hit |
| 47 | Sancho Sai (Triple Sai) | Three sai carrying configuration | east_asian | early_modern | historical | multi-hit |
| 48 | Kama (Sickle) | Single-blade sickle; originally rice-harvesting implement; Okinawan martial weaponization; kusarigama parent form | east_asian | medieval | historical | cleave |
| 49 | Kama Pair | Dual kama configuration; wushu form + practical melee | east_asian | medieval | historical | cleave |

### 2.5 Martial arts tradition category rows (supporting substrate)

Source: Wikipedia — Shaolin Kung Fu, Muay Thai, Drunken Boxing, Capoeira, Wushu, Krav Maga

| # | canonical_name | description | cultural_lineage | historical_period | register | combat_geometry |
|---|---|---|---|---|---|---|
| 50 | Shaolin Unarmed Form (Luohan Quan) | Bare-hand striking tradition from Shaolin monastery; "empty-hand strikes"; Buddhist martial tradition | east_asian | classical | historical | single / multi-hit |
| 51 | Shaolin 18 Luohan Quan | 18-move unarmed form; foundational Shaolin open-hand tradition | east_asian | classical | historical | multi-hit |
| 52 | Muay Thai Elbow (Sok) | Elbow strike technique; "most dangerous form of attack in sport"; body-as-weapon | southeast_asian | early_modern | historical | single |
| 53 | Muay Thai Knee Strike | Knee-drive technique; clinch-range body weapon | southeast_asian | early_modern | historical | single |
| 54 | Muay Thai Shin Conditioned | Hardened shin used as striking surface; traditional bone-conditioning practice | southeast_asian | early_modern | historical | single |
| 55 | Khat Chueak (Rope-Wrapped Hands) | Traditional Muay Thai pre-glove hand wrapping with rope; historical combat implement | southeast_asian | early_modern | historical | single |
| 56 | Capoeira Chanfolo (Double Dagger) | Double-edged dagger taught in Mestre Bimba's capoeira tradition; concealed weapon | south_american_indigenous | modern | historical | single |
| 57 | Capoeira Razor (Gilette Razor) | Straight razor used in traditional street capoeira rodas | south_american_indigenous | modern | historical | single |
| 58 | Pankration Gloves (Greek) | Minimal leather hand-wrapping for ancient Greek pankration (all-strength fighting) | european | pre_classical | historical | single |
| 59 | Caestus Wrapped Fist | Roman cestus variant with leather strips wound around fist + forearm; competitive boxing | european | pre_classical | historical | single |
| 60 | Drunken Monk Fist (Zui Quan Open Hand) | Unweaponized open-hand drunken form; Shaolin drunken luohan tradition | east_asian | classical | historical | single |
| 61 | Wushu Open Hand (Changquan) | Competition barehand form; precursor skill to rope dart + chain whip | east_asian | contemporary | historical | single |

### 2.6 Edge case: ambiguous WIS-melee-light vs WIS-caster-faith items

Per dispatch Q-Enrich-2 (dispatch open question): tonfa/nunchaku/staff cross-classification question surfaces three candidate rows. Report for gandalf Pattern-A design-call if needed.

| # | canonical_name | Ambiguity | Recommendation |
|---|---|---|---|
| E1 | Shakujo (Buddhist Monk Staff) | WIS-melee-light (combat function) vs WIS-caster-faith (Buddhist ritual implement; divine authority symbol) | Lean WIS-melee-light — combat function is primary (Shaolin use documented); faith-utility is secondary register. Tag `register_canonical=historical` not `mythological` for combat-context rows |
| E2 | Trishula Staff (Shiva) | WIS-melee-light (spear-staff combat) vs WIS-caster-faith (Shiva's divine implement) | Lean WIS-caster-faith — Trishula is specifically divine and ritual in all primary contexts; its combat use is mythological, not martial-practice |
| E3 | Drunken Monk Fist (Zui Quan) | WIS-melee-light (bare-hand martial) vs STR-unarmed (raw strength) | Lean WIS-melee-light — drunken-boxing tradition is distinctly discipline + spirit-cultivation oriented (WIS register); different from STR-Unarmed Brawler which is power-strike-dominant |

**Escalation trigger (Q-Enrich-2):** E2 (Trishula) is the only row that may warrant gandalf Pattern-A follow-on if elrond wants design guidance on the caster-faith vs melee-light classification for divine-spear items.

---

## 3. Row count summary

| Category | Rows extracted |
|---|---|
| Unarmed / fist-load implements (§ 2.1) | 14 |
| Monk staves (§ 2.2) | 12 |
| Sash / chain / flexible (§ 2.3) | 13 |
| Tonfa / sai / kama (§ 2.4) | 10 |
| Martial arts tradition category (§ 2.5) | 12 |
| **TOTAL** | **61** |
| Edge case surface (§ 2.6) | 3 (not in count; elrond judgment) |

**Target range: 50-100. Crawl delivers 61 rows. Within target.**

---

## 4. Elrond classification notes

### 4.1 Primary stat: WIS throughout

All 61 rows targeted for WIS-melee-light per dispatch spec. The distinction from WIS-caster-faith (mace-crusader) is form-vocabulary: none of these rows are mace/talisman/censer forms.

### 4.2 weapon_type_family

Per dispatch: the family classification for monk weapons is elrond's judgment call. Two options:

- `caster-faith` (existing family) — WIS implements that happen to be martial-light in form
- `martial-light-monk` (new sub-classification) — OUT OF SCOPE per dispatch (do not extend schema)

**Recommendation:** classify as `caster-faith` with `weapon_kind_classified_subtype` noting the martial-light form. The WIS-stat routes to caster-faith per the algorithmic rule; elrond may use subtype to distinguish "faith-martial" from "faith-mace" clusters within the family.

### 4.3 proxy_range_class

- Unarmed / fist-load implements: `melee` or `melee_close_or_grapple`
- Staves (bo, jo, shakujo): `mid` (reach weapon; typical r_max ~3-4 units)
- Flexible/chain weapons (nunchaku, kusari-fundo): `melee` to `mid` (depends on chain length)
- Sai / tonfa / kama: `melee`
- Martial arts tradition category rows: `melee` or `melee_close_or_grapple`

### 4.4 proxy_geometry_class

- Single striking: `single`
- Multi-strike (emeici spinning, nunchaku rapid): `multi-hit`
- Chain entangling (meteor hammer, chain whip AoE): `AoE` (but these are borderline; elrond call)
- Cleave (kama sweep, sansetsukon three-range): `cleave`

### 4.5 proxy_tempo_class

- Unarmed / rapid-strike: `high`
- Chain weapons (nunchaku, chain whip): `high`
- Staves (bo, jo): `medium`
- Deliberate grapple tools: `medium` or `low`

### 4.6 cultural_lineage_canonical

- East Asian martial tradition (~70% of rows): `east_asian`
- South Asian (bagh nakh, khakkhara, trishula): `south_asian`
- Southeast Asian (muay thai): `southeast_asian`
- European (cestus, pankration): `european`
- South American (capoeira): `south_american_indigenous`

### 4.7 register_canonical

- Historical martial practice rows: `historical`
- Mythological divine implements (ame-no-nuboko, trishula, khakkhara bearer): `mythological`
- Contemporary wushu: `historical`

---

## 5. Scope note — martial tradition category rows

The dispatch specifies crawling "martial-arts traditions (Shaolin / Krav Maga / Capoeira / Muay Thai / Karate / etc.)." The rows in § 2.5 are CATEGORY-class implements (representing martial traditions as substrate categories, not named individual weapons). These are analogous to the 1,139 category rows already in the substrate — they provide lineage signal and geometric coverage.

Rows 50-61 will classify as `weapon_kind=category` per elrond's schema, similar to the existing `european-historical` category rows. This is intentional: they provide cultural_lineage signal for east_asian / southeast_asian / south_american_indigenous lineages in the WIS-melee-light cell.

---

## 6. v1_scope gate assessment

All 61 rows are primary weapon role candidates. No ammo/shield/banner contamination. `weapon_kind` split:
- ~35 rows: `named_template` (individually named weapons like specific nunchaku, shakujo, bagh nakh variants)
- ~26 rows: `category` (martial tradition / technique-class rows)

Elrond spot-check 10% = ~6 rows.

---

## 7. Crawl record

| Field | Value |
|---|---|
| Crawl agent | legolas |
| Crawl date | 2026-05-27 |
| Sources used | Wikipedia (Nunchaku, Tonfa, Bō, Shakujo, Cestus, Bagh Nakh, Sansetsukon, Kusari-fundo, Tekko, Jo, Sai, Kama, Emeici, Rope dart, Chain whip, Shaolin Kung Fu, Muay Thai, Drunken Boxing, Capoeira, Wushu, Krav Maga, Izanagi), public domain martial arts encyclopedias |
| Robots.txt violations | None |
| Rows extracted | 61 |
| Target range | 50-100 |
| Edge cases for elrond | 3 (Q-Enrich-2 cross-classification ambiguity; E2 Trishula may need gandalf Pattern-A if elrond uncertain) |
| Status | COMPLETE — ready for elrond curation + DB ingest |

---

**Signed:** legolas (researcher and scout)
**For:** Sub-Fix 2 completion record per dispatch `2026-05-27-substrate-enrichment-bundle-int-aoe-monk-hybrid.md`. 61 WIS-melee-light (monk) rows extracted; Q-Enrich-2 cross-classification surfaces 3 edge cases for elrond curation judgment.
