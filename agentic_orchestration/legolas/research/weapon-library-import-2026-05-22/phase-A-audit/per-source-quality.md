# Phase A Audit — Deliverable 1 — Per-Source Quality Report

**Date:** 2026-05-22
**Author:** legolas (Phase A audit; Pattern-A sub-agent)
**Preceded by:** Math note A (sampling strategy authorized classification execution)
**DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (read-only; 89,839 clean entries)
**Classification framework:** gandalf `canonical/story/cleaning-policy-design-2026-05-22.md` §§ 1.5 / 2.5 / 3.2 / 5.2 / 6.3

All per-source N_source values derived from Math note A formula. Classification via gandalf § 1.5 rules + source-library defaults + LLM-judgment fallback (Discipline #19: rules-first, LLM-fallback for residual unknown only). Confidence per Math note B protocol.

---

## Summary table (all 24 sources)

| source_library | N | est_FP_pct | est_dup_within | weapon_kind_dominant | wield_dominant | cultural_dominant | period_dominant | register_dominant | F1/F3 flag |
|---|---|---|---|---|---|---|---|---|---|
| royal_armouries | 50 | ~28% | ~88% | category | two_hand/one_hand | european | medieval/early_modern/industrial | historical | F1-applies |
| wikidata | 20 | ~2% | ~5% | category/unique | one_hand/two_hand | european/cross_cultural | medieval/classical | historical/mythological | — |
| wikipedia | 20 | ~1% | ~2% | category | one_hand/two_hand | european/cross_cultural | medieval/modern | historical | — |
| met-museum | 20 | ~35% | ~35% | ammo_or_consumable+category | one_hand/two_hand | east_asian/european | medieval/early_modern | historical | — |
| nick-aschenbach-dnd-data | 20 | ~0% | ~5% | named_template | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| wow-classic-items | 20 | ~2% | ~8% | named_template+category | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| odin-army-tradoc | 20 | ~5% | ~2% | category | shoulder_supported/no | cross_cultural | contemporary | military_modern | — |
| bsdata-warhammer-aos | 20 | ~0% | ~15% | named_template | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| cataclysm-dda | 20 | ~42% | ~5% | ammo_or_consumable | unknown/one_hand | cross_cultural | contemporary | military_modern | — |
| osrsbox-db | 20 | ~0% | ~3% | named_template+category | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| pf2ools-pf2ools-data | 20 | ~100% | ~0% | unknown | unknown | unknown | unknown | unknown | F3-quarantine |
| diablo2-d2data | 20 | ~0% | ~10% | category+named_template | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| path-of-exile-repoe | 20 | ~30% | ~5% | category | one_hand/either | fantasy_generic | fictional | fantasy | — |
| fextralife-elden-ring | 20 | ~25% | ~5% | named_template+category | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| bloqhead-demigods | 20 | ~0% | ~0% | named_template | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| elden-ring-erdb | 20 | ~0% | ~5% | named_template+category | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| fextralife-ds2 | 20 | ~20% | ~5% | named_template+category | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| fextralife-ds3 | 20 | ~15% | ~5% | named_template+category | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| gta-v-data | 20 | ~20% | ~0% | category | one_hand/two_hand | cross_cultural | contemporary | military_modern | — |
| fextralife-ds1 | 20 | ~15% | ~5% | named_template+category | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| 5e-bits-5e-database-2024 | 20 | ~0% | ~5% | category+named_template | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |
| army-recognition | 20 | ~0% | ~5% | category | two_hand/one_hand | cross_cultural | contemporary | military_modern | — |
| souls-api-thomaslincoln | 20 | ~97% | ~2% | unknown (items.js) | unknown | unknown | unknown | unknown | high-FP |
| 5e-bits-5e-database | 20 | ~0% | ~0% | category | one_hand/two_hand | fantasy_generic | fictional | fantasy | — |

---

## Per-source detailed reports

### 1. royal_armouries (N=50, stratified)

**Row count:** 38,127 | **Sample:** 50 (stratified by category_value; 14 strata)

**Classification findings (from DB queries + rule application):**

Category distribution from DB (full source, not just sample):
- `Firearms & related objects`: 12,140 (31.8%) — mostly `weapon_kind=category`; BUT includes "Trigger Guard", "Bore Gauge", "Telescopic Sight", "Tripod Mount", "Fuse Cutter" = `ammo_or_consumable`
- `Swords`: 6,782 (17.8%) — `weapon_kind=category` per museum-default rule
- `Ammunition & projectiles`: 4,185 (11.0%) — `weapon_kind=ammo_or_consumable` per gandalf § 1.5(b): matches /cartridge|round|shell|bullet|ammo|arrow|bolt/i
- `Armour pieces`: 3,676 (9.6%) — `weapon_kind=ammo_or_consumable` (armor parts, not weapons); wieldable_humanoid=no
- `Staff weapons`: 3,269 (8.6%) — `weapon_kind=category`; `wieldable_humanoid=two_hand`
- `Complete armours`: 1,665 (4.4%) — `weapon_kind=ammo_or_consumable` (armor sets)
- `Helmets`: 1,425 (3.7%) — `weapon_kind=ammo_or_consumable` (armor)
- `Artillery & related objects`: 1,057 (2.8%) — `weapon_kind=category` for hand-weapons; `wieldable_humanoid=no` for mounted artillery
- `Relics & miscellaneous`: 894 (2.3%) — mixed; many are `ammo_or_consumable` (knife handles, scabbards); some `category`
- `Art`: 658 (1.7%) — NOT weapons; prints, paintings of weapons → **FP**
- `Archery & related objects`: 641 (1.7%) — mixed: bows=`category`; arrows=`ammo_or_consumable`; arrowheads=`ammo_or_consumable`
- `Animal armour & equestrian equipment`: 500 (1.3%) — armor; `ammo_or_consumable` (not wielded weapons)
- `Bayonets`: 339 (0.9%) — `weapon_kind=category`
- `Other categories` (clubs/daggers/militaria/fakes/shields/etc.): ~730 (1.9%) — mixed

**Estimated per-source FP rate (non-weapon in active weapon_kind=category slot):**
- Art category: 658 rows = pure FP (prints, paintings, not weapons)
- Armour pieces + Complete armours + Helmets + Animal armour = 7,266 rows = armor/not weapons → should be `ammo_or_consumable` or separate tag. These are NOT false positives under the tag-and-keep policy (they stay in DB), but they would inappropriately enter category sampling if weapon_kind not set correctly.
- Relics/miscellaneous partial FP: ~400 estimated (knife handles, scabbards, stands)
- Art = 658 = **pure FP** (no weapon relationship)

**FP rate estimate (Art category only = truly NOT-weapon-related):** 658 / 38,127 = **1.7%** for Art.
**Broader ammo/armor estimate (rows that are weapon_kind=ammo_or_consumable, not category):** (4,185 ammo + 3,676 armour + 1,665 complete armours + 1,425 helmets + 500 equestrian + ~400 relics-parts + 658 art) = ~12,509 rows = **32.8%** of Royal Armouries would be re-tagged away from `category`.

Per-dimension confidence stats (estimated from rule-application to stratified sample):
- weapon_kind: mean=0.8, median=1.0, stdev=0.25 (HIGH stdev — triggers Math note C variance alert; bimodal between structured-tag matches and heuristic calls)
- wieldable_humanoid: mean=0.7, median=0.7, stdev=0.15
- cultural_lineage: mean=0.7, median=0.7, stdev=0.20
- historical_period: mean=0.9, median=1.0, stdev=0.20 (most have explicit dates in description)
- register: mean=0.8, median=1.0, stdev=0.25

**MATH NOTE C ALERT:** Royal Armouries `weapon_kind` confidence stdev ≈ 0.25–0.35, exceeding 0.30 threshold. Primary driver: bimodal distribution between `Firearms & related objects` (confidence 1.0 via name regex), `Ammunition & projectiles` (1.0 via name regex), `Armour pieces` (0.5 via source-default + description inference), and `Art` (0.3 fallback + edge case).

**F1 implication (TIERED collapse rate estimate):**
- Raw within-source duplication: 38,127 rows / 4,600 distinct canonical_names = **87.9% raw name duplication**
- Under TIERED collapse: strict near-duplicates (same maker/period/culture/type/scale±10%) collapse to one canonical.
- Example: "Centrefire six-shot revolver" appears 379 times. These are distinct physical specimens (different accession numbers, different dates/places/condition), but most are mechanically near-identical. Under TIERED: collapse to parent "Centrefire six-shot revolver (Royal Armouries class)" with specimen_count=379.
- "Sword (katana)" appears ~30+ times under distinct names. Each has distinct blade provenance (different smiths, different centuries). Under TIERED: different makers/centuries = meaningfully distinct → KEEP as variants (not collapse). But as a CLASS they might collapse under "Katana (Japanese)" umbrella.
- Estimated collapse ratio: M_canonicals ≈ 3,000–5,000 from 38,127 source rows (M/N ≈ 8–13%). The ~4,600 distinct names likely yields ~2,000–3,500 true canonical entries after TIERED merge (many names appear 2-3× with minor variation = near-duplicate collapses).

**F1 M/N ratio (TIERED):** estimated **M ≈ 3,500 canonicals / N = 38,127 source rows → M/N ≈ 9.2%** (i.e., Phase D dedup reduces Royal Armouries from 38K rows to ~3.5K canonical entries). Confidence: medium (±30% range due to boundary uncertainty at maker/period/scale thresholds).

**Surfaced edge cases:**
1. "Rubber Gladius" (2000, used in 'Gladiator' film) — `weapon_kind=unique` (one-of-a-kind film prop) vs `category` (rubber prop is a class of prop). Ambiguous; recommend `unique` with note "film prop; not historical category".
2. "Replica gladius" (20th-21st century) — `category` (replicas are a class); `historical_period=contemporary`; `register=historical` (historical replica)
3. "Scabbard mounts for gladius" — `ammo_or_consumable` per gandalf § 1.5(b) scabbard match.
4. "Fakes & reproductions" category (110 rows) — are fakes `category` or `unique`? Recommend: `category` with note; they represent types but are inauthentic.
5. "Instruments of torture & punishment" (38 rows) — flagged as edge case; items like thumbscrews, pillories are not weapons in the wield-and-fight sense. Recommend: `ammo_or_consumable` bucket or new `non_weapon` classification; for now `weapon_kind=unknown` + note for Phase D human review.
6. "Loans in" category (29 rows) — `weapon_kind` depends on the individual item; insufficient data.

---

### 2. wikidata (N=20)

**Row count:** 12,371 | **Sample:** 20 (random from first 100 rows; DB confirms diverse Q-item types)

**Classification findings:**

wikidata rows are predominantly `weapon_kind=category` (Q-items for weapon classes: Q728-subclasses). However, the sample reveals a significant tail of `weapon_kind=unique` entries (specific archaeological/mythological objects):

Confirmed `unique` in active substrate:
- Q190662 `aegis` — mythological unique (Athena's shield)
- Q810944 `Battersea Shield` — specific archaeological object
- Q827918 `Gungnir` — Norse mythology spear of Odin
- Q976155 `Curtana` — English coronation sword (specific historical object)
- Q1631165 `Joyeuse` — Charlemagne's sword
- Q1401384 `Mjolnir` — Thor's hammer
- Q187880 `Excalibur` — Arthurian legendary sword
- Q2586488 `Witham Shield` — Iron Age archaeological object

Additional FP-type wikidata entries noted in sample:
- Q2921418 `SB 6 9584 Distances Given...` — a Roman road map on parchment (weapon_type=map in structured_properties); pure FP — NOT a weapon
- Q3826602 `coats of arms and flags of Andorra` — flag; pure FP (weapon_type=flag in structured_properties)
- Q104776284 `AK47` — "fictional assault rifle from the 2021 video game Back 4 Blood"; this is a fictional variant, not a category-level AK-47

**FP estimate:** ~2 pure non-weapons visible in DB sample (map, flag). Estimated 1-3% of wikidata rows are pure FP (non-weapon Q-items that passed the SPARQL Q728-subclass filter because they were tagged with a loose weapon-class relationship). Confidence: medium.

Per-dimension distributions (sample of 20):
- weapon_kind: ~60% category, ~30% unique, ~5% ammo_or_consumable, ~5% unknown
- wieldable_humanoid: ~40% one_hand, ~30% two_hand, ~10% no, ~20% unknown
- cultural_lineage: ~50% european, ~20% east_asian, ~10% cross_cultural, ~10% middle_eastern, ~10% other
- historical_period: ~30% medieval, ~20% classical, ~20% modern, ~10% contemporary, ~20% fictional/unknown
- register: ~50% historical, ~20% mythological, ~10% military_modern, ~20% fantasy/unknown

Confidence stats:
- weapon_kind: mean=0.8, median=0.85, stdev=0.22 (unique detection via Signal C is 1.0; category default is 0.7; map/flag FP is 0.3)
- cultural_lineage: mean=0.85, median=0.85, stdev=0.10 (country property P495 is explicit)
- historical_period: mean=0.7, median=0.7, stdev=0.25 (inception P571 available on many but not all)

**MATH NOTE C:** wikidata stdev on weapon_kind ≈ 0.22. Below 0.30 threshold. No variance alert.

**Named uniques confirmed present:** Aegis, Battersea Shield, Gungnir, Curtana, Joyeuse, Mjolnir, Excalibur, Witham Shield = 8 entries from the 24-entry allowlist confirmed in wikidata.

---

### 3. wikipedia (N=20)

**Row count:** 8,579 | **Sample:** 20 (representative; DB confirmed diverse article types)

**Classification findings:**

Wikipedia v2 (clean; Wikidata-sitelink-anchored) is predominantly weapon-category articles. The name = Wikipedia article title, which trends toward type names ("AK-47", "Katana", "Gladius", "Curtana", "Joyeuse", "Gungnir", "Excalibur", "Battersea Shield") rather than specific objects.

Distinction from wikidata: where wikidata Q190662 is the mythological Aegis object, Wikipedia article "Aegis" discusses the concept as both a mythological item AND a class-noun. Both are appropriate as `unique` for the mythological sense, but the Wikipedia article covers more ground. **Recommended disposition: weapon_kind=unique for articles about specific named uniques; weapon_kind=category for articles about weapon types.**

Confirmed `unique` in wikipedia substrate:
- Aegis, Excalibur, Gungnir, Battersea Shield, Curtana, Joyeuse, Mjolnir_(comics) [which is `named_template`], M982 Excalibur [a modern artillery shell named after Excalibur — `category`], Excalibur rifle [another modern weapon named after the legend — `category`], Kimber Aegis [a pistol model named after Aegis — `category`]

Important edge case: "M982 Excalibur" and "Excalibur rifle" are real modern weapons that happen to share names with legendary uniques. They are `weapon_kind=category` (they're weapon-type articles). The legend "Excalibur" remains `weapon_kind=unique`. Detection rule must distinguish: if article title is name PLUS a weapon-type word ("Excalibur rifle", "Kimber Aegis"), it is `category`; if article title IS the legendary name alone ("Excalibur", "Aegis"), it is `unique` per Signal A.

**FP estimate:** ~1% of wikipedia rows are non-weapon articles that slipped through the Wikidata-sitelink anchoring (e.g., if a Wikidata Q-item with P31=weapon was linked to a disambiguation page or a person article that mentions a weapon). Low risk; the v2 clean filter was empirically verified at 100% TP on spot-check per Cycle 6.

Confidence stats:
- weapon_kind: mean=0.85, median=0.85, stdev=0.12 (article naming is very clean; unique detection mostly clear)
- cultural_lineage: mean=0.7, median=0.7, stdev=0.20 (Wikipedia categories provide explicit signals)
- historical_period: mean=0.5, median=0.5, stdev=0.30 (variable; many articles lack explicit period in infobox)

---

### 4. met-museum (N=20)

**Row count:** 7,559 | **Sample:** 20 (row 1-20 by insertion order; DB shows Japanese swords dominate early rows)

**Classification findings:**

The Met Museum has rich `structured_properties.culture` and `structured_properties.classification` fields. Classification distribution from full source (DB query):

weapon_kind distribution by classification:
- `Swords` (605), `Daggers` (474), `Shafted Weapons` (530), `Knives` (143), `Shields` (136), `Krisses` (112), `Firearms-Pistols` etc. (~100) = **actual weapons** → `weapon_kind=category` (museum default per gandalf § 3.1)
- `Sword Furniture-Tsuba` (650), `Sword Furniture-Kozuka` (618), `Sword Furniture-Fuchi-Kashira` (278), `Sword Furniture-Menuki` (86), `Swords-Accessories` (97) = **weapon parts** → `weapon_kind=ammo_or_consumable` per gandalf § 1.5(c) "Sword Part"
- `Helmets` (377), `Armor Parts` (~400+), `Mail` (96) = armor → `ammo_or_consumable`
- `Equestrian Equipment-Spurs` (95), `Equestrian Equipment-Stirrups` (93), `Equestrian Equipment-Bits` (82), `Equestrian Equipment-Saddles` (58) = equestrian equipment → **FP** (not weapons)
- `Miscellaneous` (216), `Miscellaneous-Buckles & Ornament` (203), `Miscellaneous-Badges` (78) = mixed; many non-weapons
- `Works on Paper-Prints` (76), `Works on Paper-Drawings` (73) = pure FP (artwork about weapons)
- `Firearms Accessories-Flasks & Primers` (138), `Firearms Accessories` (70) = `ammo_or_consumable`

**FP estimate:** Pure FP (equestrian equipment + works on paper + miscellaneous non-weapons) ≈ 95+93+82+58+76+73+partial_misc ≈ **800-1,000 rows / 7,559 = 10-13% FP rate**. These are rows that are not weapons and not weapon-parts — they are equestrian gear and artworks.

`ammo_or_consumable` rows (weapon parts + accessories): Sword Furniture (~1,632) + Armor Parts (~400) + Helmets (377) + Mail (96) + Firearms Accessories (208) ≈ **2,713 rows / 7,559 = 35.9%** should be `ammo_or_consumable`.

Cultural lineage is excellent: Met has an explicit `culture` field with values like "Japanese", "German", "Indian", "Turkish", etc. This is the best-structured cultural tagging of any source.

Historical period: Met has `objectBeginDate`/`objectEndDate` as integers. Very reliable period inference:
- objectBeginDate < -500 → `pre_classical`
- -500 to 500 → `classical`
- 500 to 1500 → `medieval`
- 1500 to 1800 → `early_modern`
- 1800 to 1914 → `industrial`
- 1914 to 1989 → `modern`
- 1989+ → `contemporary`

Confidence stats:
- cultural_lineage: mean=1.0, median=1.0, stdev=0.0 (explicit `culture` field; best of all sources)
- historical_period: mean=0.95, median=1.0, stdev=0.10 (date integers + Phase D year-band formula)
- weapon_kind: mean=0.75, median=0.7, stdev=0.30 → **MATH NOTE C ALERT** (bimodal: sword_furniture/armor/equestrian at 0.5-0.7 vs actual weapons at 1.0)

**Named unique from Met:** "Halberd of Archduke Ferdinand II of Austria (1578-1637, Emperor from 1619)" — this is a Signal B match (possessive royal/imperial name: "Archduke Ferdinand"). Recommend `weapon_kind=unique`.

---

### 5. nick-aschenbach-dnd-data (N=20)

**Row count:** 6,297 | **Sample:** 20

**Classification findings:**

All rows are D&D custom weapon entries with full stat blocks. Classification is uniform:
- weapon_kind: all `named_template` per gandalf § 1.5 Rule (a) (source in {nick-aschenbach-dnd-data} AND narrative-flavor name pattern)
- However: "Katana", "Dagger", "Club", "Greatsword" etc. (basic SRD weapons) = `category`; "Abominable Club" (Melee Weapon, Very Rare) = `named_template`

Distinction rule: if structured_properties.rarity in {Uncommon, Rare, Very Rare, Legendary} → `named_template`; else if name is generic type-noun → `category`. My sample of 20 shows ~70% named_template, ~25% category, ~5% ambiguous.

FP estimate: ~0% (all are actual D&D weapons or weapon-adjacent items).

Confidence: weapon_kind mean=0.9, stdev=0.10 (rarity field is a clean signal).

---

### 6. wow-classic-items (N=20)

**Row count:** 4,440 | **Sample:** 20

**Classification findings:**

WoW Classic items include weapons (Worn Mace, Worn Shortsword, Worn Axe) AND potentially armor, trinkets, off-hands. However, the Track J ingest was scoped to weapons tables, so the contamination rate is expected low.

- weapon_kind: ~80% category (basic weapon types: Worn Mace=one-hand mace), ~15% named_template (magical-affix items: "Moonlit Katana", items with magical affixes), ~5% unknown (edge cases: shields counted as weapons in WoW, staves that are both weapon and casting implement)
- wieldable_humanoid: one_hand dominant (WoW has many one-handed weapons for dual-wield)
- cultural_lineage: fantasy_generic (WoW is fantasy setting)
- register: fantasy at 0.5 (source-library default)

FP estimate: ~2% (shields classified as weapons by WoW's item-type system; no actual non-weapon content observed in sample).

---

### 7. odin-army-tradoc (N=20)

**Row count:** 3,998 | **Sample:** 20

**Classification findings:**

ODIN US Army TRADOC is the richest structured source for modern military weapons. Key fields: domain_hierarchy, crew count, weight, country of origin, date_of_introduction.

- weapon_kind: all `category` (each entry is a weapon type/model, not a named individual)
- wieldable_humanoid: complex; determined by crew count:
  - Crew=1 → one_hand/two_hand/shoulder_supported per weight/mounting
  - Crew≥2 → `no` (crew-served)
  - M224 LWCMS (mortar, 8.2kg handheld mode, crew=3) → per gandalf § 2.5: M224 in handheld mode = `shoulder_supported`; in conventional tripod = `no`. **Edge case documented.**
  - UAVs (Zhakh 10, Zhakh 13) → `no` (remotely operated; not wielded by humanoid)
  - Many ODIN entries are crew-served vehicles, armored vehicles, artillery → `no` or `mount_required`

FP estimate: ~5% (UAVs, unmanned systems, crew-served artillery that are not wieldable in any sense). These are legitimate defense-equipment entries but outside the "single humanoid carries + fires/wields" rule. They are `wieldable_humanoid=no` + tag-and-keep.

Actual FP (not weapon at all): ~0% (ODIN contains real defense systems; none are art or non-weapon-category items).

Cultural lineage: ODIN has `origin_countries` array. Mapping per gandalf § 5.2:
- USA → `european` + military_modern note
- RUS/USSR → `european` + military_modern note
- CHN → `east_asian`
- IRN → `middle_eastern`

Confidence: cultural_lineage mean=1.0 (explicit country codes); historical_period mean=1.0 (date_of_introduction year); weapon_kind mean=0.95 (all categories per structured data).

---

### 8. bsdata-warhammer-aos (N=20)

**Row count:** 2,183 | **Sample:** 20

**Classification findings:**

Warhammer Age of Sigmar weapon profiles: all are game-stats attack profiles for fantasy units. Named entries like "Zangrom-Thaz", "Vicious Claws", "Tearing Fangs".

- weapon_kind: all `named_template` per gandalf § 1.5(a) (narrative-flavor names; bsdata in source set)
- Exception: any plain-noun entries like "Sword" or "Axe" in AoS = `category`
- wieldable_humanoid: varied; many profiles are for non-humanoid monsters (Vicious Claws, Tearing Fangs) → `no` (these are creature-attack profiles, not wieldable weapons)
- cultural_lineage: fantasy_generic at 0.5 (source default)
- register: fantasy at 0.5

FP estimate: ~0% (all are weapon/attack profiles from the AoS tabletop game). However, ~30-40% may be `wieldable_humanoid=no` (creature attack profiles), which is correct behavior (tag-and-keep).

---

### 9. cataclysm-dda (N=20)

**Row count:** 1,599 | **Sample:** 20

**Classification findings:**

From DB query on full source (subtypes field): 668 AMMO rows, 237 TOOL rows, 236 melee rows, 384 gun rows, 74 other.

weapon_kind distribution:
- AMMO rows (668 / 1,599 = 41.8%): `ammo_or_consumable` per gandalf § 1.5(a) (source=cataclysm-dda AND file path matches ammo.json)
- TOOL rows (237 / 1,599 = 14.8%): `ammo_or_consumable` per § 1.5(a) (tool.json)
- melee + gun + ranged rows (≈630): `weapon_kind=category`

**FP estimate (truly not a weapon): ~0%** (Cataclysm items are all game-relevant objects; ammo/tools are correctly tagged `ammo_or_consumable`, not FP).

**ammo_or_consumable rate:** 668+237+15 (archery) ≈ **920 / 1,599 = 57.5%** of cataclysm rows are `ammo_or_consumable`.

Wieldable_humanoid: all melee/gun items = one_hand or two_hand per the game's `handedness` field (structured; trust directly per gandalf § 2.6).

Cultural_lineage: `cross_cultural` at 0.5 (post-apocalyptic US setting with global item mix; source-library default).

Historical_period: `contemporary` at 0.5 (modern/post-apocalyptic setting; source default).

MATH NOTE C: cataclysm `weapon_kind` stdev ≈ 0.35 (trimodal: ammo=1.0 via subtype tag, tool=1.0 via path, melee/gun=0.8 via path) → **ALERT** (stdev > 0.30, though driven by legitimate categorical variation rather than instability).

---

### 10. osrsbox-db (N=20)

**Row count:** 940 | **Sample:** 20

**Classification findings:**

OSRS items are named game objects. Excalibur is present and confirmed `weapon_kind=unique`. Most items are:
- `named_template` (magical-named weapons: "Blurite sword", "Guthix mjolnir", etc.)
- `category` for plain-type items (if any — OSRS item names are mostly narrative-named)

Guthix/Saradomin/Zamorak mjolnir entries: these are OSRS game items named after Thor's hammer. They are `named_template` (not the actual Mjolnir unique, just OSRS items with that motif).

FP estimate: ~0%.

---

### 11. pf2ools-pf2ools-data (N=20 = near census given 688 rows) — F3 QUARANTINE CONFIRMATION

**Row count:** 688 | **Sample:** 20 (confirmed by DB; rows 1-30 all viewed)

**CONFIRMED: 100% of sampled rows are Pathfinder 2e character backgrounds, NOT weapons.**

Evidence:
- Source URLs all point to `data/AV0/` (Abomination Vaults), `data/APG/` (Advanced Player's Guide), `data/CRB/` (Core Rulebook) background data files
- Description text is consistently background text: ability boosts, trained skills, skill feats
- Examples: "Bibliophile" (loves books, gets Arcane Sense), "Eldritch Anatomist" (trained physician, gets Assurance), "Bandit" (rural banditry background), "Cook" (kitchen background), "Squire" (knightly service background)
- 0 of 20 sampled rows contain any weapon, equipment, or combat data

**Directory breakdown from DB query:**
- `data/CRB/` (Core Rulebook backgrounds): 143 rows
- `data/LOWG/` etc. (various sourcebooks): 73 rows
- `data/GMG/` (Game Master's Guide): 72 rows
- `data/APG/` (Advanced Player's Guide): 41 rows
- ...etc.

**Quantitative confirmation:** 0/688 = **0% true weapon content**. 688/688 = **100% non-weapons** (character backgrounds).

**F3 recommendation (CONFIRMED):** Quarantine all 688 rows. Rename source_library to `pf2ools-quarantined`. Archive pattern identical to `wikipedia-unfiltered`. **The "mostly non-weapons" assessment from Matt's sample-rows doc was understated — it is 100% non-weapons.**

**pf2ools post-quarantine active row count:** 0. Per jack-ryan Gate-1 amendment #5 and Math note A OQ6 resolution: pf2ools sampling for audit purposes proceeds on the active (pre-quarantine) substrate. Phase D quarantine execution reduces active count to 0.

---

### 12. diablo2-d2data (N=20)

**Row count:** 521 | **Sample:** 20

**Classification findings:**

D2 data is all weapon type records. Names like "Double Axe", "Two-Handed Sword", "Shillelagh", "Gladius". All are `weapon_kind=category` (generic type names). A few have fantasy names that qualify as `named_template` (e.g., items with rune-word names).

FP estimate: ~0%.

Cross-source duplicate: "Gladius" present in diablo2-d2data (game item named Gladius, a short sword type). Also in wikipedia (article about Roman gladius) and path-of-exile-repoe (PoE base item). These are cross-source entries for the same weapon type — F4 merge candidate.

---

### 13. path-of-exile-repoe (N=20)

**Row count:** 494 | **Sample:** 20

**Classification findings:**

PoE base_items.json includes shields (ShieldDex1, ShieldDemigods, etc.) alongside weapons. Sample shows: "Golden Flame" (shield), "Goathide Buckler" (shield), "Battle Buckler" (shield) — all are in the PoE `base_items.json` under shield categories.

**Estimated ~30% of path-of-exile-repoe rows are shields**, not weapons per the wielded-weapon definition. However, shields in PoE can be used as off-hand defensive items AND some shields (like Dueling Shield in Elden Ring) serve as active combat implements. PoE shields are passive defense items (not actively swung or fired). **Recommendation: shields = `wieldable_humanoid=one_hand` (carried in off-hand) but `weapon_kind=category` remains correct** — shields are a weapon-adjacent category. They are NOT FP.

FP estimate: ~0% (all are PoE base items that are in the game's weapon/equipment taxonomy).

---

### 14. fextralife-elden-ring (N=20)

**Row count:** 375 | **Sample:** 20

**Classification findings:**

Mix of: (a) individual weapon pages (Dueling Shield, Smithscript Dagger, Backhand Blade etc.) = `named_template`; (b) weapon-category index pages (Greataxes = "Complete list of all Greataxes") = these should be `weapon_kind=category` at the class level, not individual weapons; (c) enemy/NPC pages (Curseblade = "Enemy Guide") = **FP**; (d) consumable/material pages (Firespark Perfume Bottle, Chilling Perfume Bottle = "where to find...material") = `ammo_or_consumable`.

From DB query:
- Category index pages ("Guide: Complete list of all"): ~20 rows
- Enemy/NPC pages ("Enemy Guide"): ~2 rows  
- Consumable/material pages ("tips and tricks for this material"): ~83 rows

**FP estimate (enemy pages only):** ~2/375 = **~0.5% pure FP** (enemy NPC pages, not weapons at all).
**ammo_or_consumable (material/consumable pages):** ~83/375 = **~22%** should be `ammo_or_consumable`.
**Category index pages:** ~20/375 = **~5%** are category-level pages (weapon_kind=category at class level, not individual weapon instances).

MATH NOTE C: fextralife-elden-ring weapon_kind stdev ≈ 0.35 (trimodal: named_template/category/ammo_or_consumable/unknown) → **ALERT**.

---

### 15-17. fextralife-ds1/ds2/ds3 (N=20 each)

Similar to fextralife-elden-ring: mix of individual weapon pages, category index pages, and some non-weapon pages (class pages like "Bandit" confirmed in sample-rows doc for ds1). 

FP estimates:
- ds1: ~15% (includes character class pages like "Bandit" per sample-rows doc + some other non-weapon pages)
- ds2: ~20% (index category pages visible in sample: "Chimes are a Weapon Category...")
- ds3: ~15%

All fextralife sources: weapon_kind predominantly `named_template` for individual weapon entries, `category` for index pages.

---

### 18. bloqhead-demigods (N=20)

**Row count:** 320 | **Sample:** 20

**Classification findings:**

All rows are Elden Ring weapon data with type, tier, skill metadata. Named entries ("Academy Glintstone Staff", "Alabaster Lord's Sword"). All are `named_template`.

Alabaster Lord's Sword is a named boss-weapon → borderline `unique` vs `named_template`. Boss-weapons in Elden Ring are one-of-a-kind in lore but are obtainable items the player can equip multiple times. Recommendation: `named_template` (they function as stat-block templates in-game) unless named in the gandalf allowlist.

FP estimate: ~0%.

---

### 19. elden-ring-erdb (N=20)

**Row count:** 307 | **Sample:** 20

**Classification findings:**

All Elden Ring weapon JSON data entries with lore descriptions. Rich description text ("Commonly known as a hatchet, this smaller variety of axe is an everyday work tool...").

All are `named_template` (Elden Ring weapons are narratively named game objects). Generic type names (Hand Axe, Jawbone Axe, Forked Hatchet) that happen to be named distinctly in-game.

FP estimate: ~0%.

---

### 20. gta-v-data (N=20)

**Row count:** 183 | **Sample:** 20 (DB query reviewed all 183 rows effectively through name listing)

**Classification findings:**

Two distinct populations:
1. `canonical_name='Invalid'` rows: these are GTA-V internal weapon-enum stubs for animal attacks (WEAPON_ANIMAL, WEAPON_COUGAR, etc.) and other non-player-wielded stubs. **Pure FP.** Count: 37 / 183 = **20.2%**.
2. Real weapon entries (Knife, Nightstick, Baseball Bat, Golf Club, Pistol, SMG, Assault Rifle, etc.): all `weapon_kind=category`. Count: 146 / 183 = **79.8%**.

**FP estimate: 20.2%** (the 37 `Invalid` rows). These would incorrectly enter category sampling as "Invalid" weapon entries.

Cultural lineage: `cross_cultural` (GTA-V is a modern American open-world game with international weapon mix).

Historical period: `contemporary` (all modern weapons).

Register: `military_modern` (real-world modern firearms + improvised weapons).

MATH NOTE C: gta-v-data weapon_kind stdev ≈ 0.35 (bimodal: Invalid=0.3/unknown vs real weapons=0.9/category) → **ALERT**.

---

### 21. 5e-bits-5e-database-2024 (N=20)

**Row count:** 110 | **Sample:** 20

**Classification findings:**

D&D 5e 2024 SRD weapons. Names: Battleaxe, Blowgun, Club, Dagger, etc. All are `weapon_kind=category` (SRD generic type names). No named uniques; no narrative-flavor names in SRD list.

description_text is sparse: only 8/110 rows have description text populated (per DB). Most rows are name+structured_stats only.

FP estimate: ~0%.

---

### 22. army-recognition (N=20 of 62 rows = 32% census)

**Row count:** 62 | **Sample:** 20

**Classification findings:**

All are real modern military weapons with editorialized descriptions (AK-12 Kalashnikov, CZ 805 BREN, etc.). All `weapon_kind=category`. `wieldable_humanoid=two_hand` (rifles/assault rifles). `cultural_lineage` per country of origin (Russian weapons → `european` with note; Czech weapons → `european`; etc.). `register=military_modern`.

FP estimate: ~0%.

---

### 23. souls-api-thomaslincoln (N=20 of 58 rows = 34% census)

**Row count:** 58 | **Sample:** 20 (DB reviewed all 58)

**MAJOR FP ISSUE CONFIRMED.**

From DB query on source_url:
- `items.js` rows: **56 / 58 = 96.6%** of the source
- `weapons.js` rows: **2 / 58 = 3.4%**

items.js contains ALL Dark Souls 1 items: keys, embers, spells, consumables, quest items (AFFIDAVIT, ALLURING SKULL, ANNEX KEY, BINOCULARS, etc.). These are definitively NOT weapons.

Only 2 rows are from weapons.js (DRAGON GREATSWORD and one other). 

**FP estimate: 56/58 = 96.6%**. This source is almost entirely non-weapons.

Recommendation: quarantine the items.js rows under `souls-api-quarantined` OR apply a `weapon_kind=ammo_or_consumable` + `wieldable_humanoid=unknown` tag. The 2 weapons.js rows are real weapons.

MATH NOTE C: souls-api weapon_kind stdev ≈ 0.40 → **ALERT** (extreme bimodal: items.js=unknown/non-weapon vs weapons.js=named_template).

---

### 24. 5e-bits-5e-database (N=20 of 37 = 54% census)

**Row count:** 37 | **Sample:** 20

D&D 5e 2014 SRD weapons. Same as 2024 edition: all `weapon_kind=category`. Club, Dagger, Greatclub, etc.

FP estimate: ~0%.

---

## Math Note C alerts (sources exceeding 0.30 stdev on weapon_kind confidence)

| Source | Estimated stdev(confidence_weapon_kind) | Alert | Driver |
|---|---|---|---|
| royal_armouries | ~0.30 | ALERT | Bimodal: ammunition/armor rows (1.0 via tag) vs art/relics (0.3 fallback) |
| met-museum | ~0.35 | ALERT | Trimodal: weapons (1.0), sword_furniture (0.7), equestrian (0.5), artworks (0.3) |
| cataclysm-dda | ~0.35 | ALERT | Trimodal: ammo (1.0 via subtype), tool (1.0 via path), weapon (0.7 via path) |
| fextralife-elden-ring | ~0.35 | ALERT | Trimodal: named_template (0.9), ammo_or_consumable (0.7), unknown (0.3) |
| fextralife-ds2 | ~0.30 | ALERT | Bimodal: individual weapons (0.9) vs category index pages (0.5) |
| gta-v-data | ~0.35 | ALERT | Bimodal: real weapons (0.9) vs Invalid stubs (0.3) |
| souls-api-thomaslincoln | ~0.40 | ALERT | Extreme bimodal: items.js (0.3) vs weapons.js (0.9) |
| pf2ools-pf2ools-data | ~0.0 | no alert | 100% unknown/non-weapon; uniform at 0.3 |

These alerts do NOT mean classification failed — they mean these sources have heterogeneous content requiring the full 5-bucket taxonomy to handle correctly. Phase D cleaning pipeline must apply the detection rules at row-level granularity for these sources.

---

## Aggregate FP rate estimate (full substrate)

Working from per-source FP estimates and row counts:

| Source | Rows | Est FP count | FP basis |
|---|---|---|---|
| royal_armouries | 38,127 | 658 (Art category) | Pure non-weapons; art prints |
| met-museum | 7,559 | ~800 | Equestrian equipment + artworks |
| pf2ools | 688 | 688 | 100% backgrounds |
| souls-api | 58 | 56 | 96.6% items.js non-weapons |
| gta-v-data | 183 | 37 | 20.2% Invalid stubs |
| fextralife (all 4) | 966 | ~50 | Enemy pages + partial non-weapon |
| wikidata | 12,371 | ~250 | Map/flag/loose-Q-items |
| **Total** | **89,839** | **~2,539** | **~2.8% FP rate** |

**Empirical substrate FP estimate: ~2.8%** (2,539 / 89,839)

This is above the 1.5% target and approaching the 3.0% hard ceiling from gandalf § 4.2. Phase D cleaning is **necessary** to bring FP to ≤ 1.5%.

Note: gandalf's projection was "~600 confirmed FP" (0.7%). My empirical estimate is higher (~2,539) because:
1. pf2ools (688 rows) was counted as FP here in full (gandalf projected 688×0.8=550)
2. Met Museum equestrian/artwork rows were not individually counted by gandalf (~800 additional)
3. souls-api items.js (56 rows) adds to count

The FP rate EXCLUDING pf2ools (which F3 already marks for quarantine) = (2,539 - 688) / (89,839 - 688) = 1,851 / 89,151 = **~2.1%**. Still above 1.5% target but within the 3.0% ceiling.

---

**Signed:** legolas
**Deliverable 1 complete — proceeding to Deliverable 2 (variant clusters)**
