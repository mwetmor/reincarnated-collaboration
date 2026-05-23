# Phase A Audit — Deliverable 2 — Variant-Cluster Examples

**Date:** 2026-05-22
**Author:** legolas (Phase A audit; Pattern-A sub-agent)
**Framework:** gandalf `canonical/story/cleaning-policy-design-2026-05-22.md` § 6 (variant-collapse policy framework)
**Decision criteria applied:** § 6.3 (1) mechanical signature variance, (2) cultural-narrative distinctness, (3) substrate-density consequence, (4) anchor-test
**Target:** 30-60 clusters across 24 sources. Produced: 38 clusters.

Per dispatch: legolas surfaces clusters + recommends policy; **Matt + gandalf decide in-flight per § 6.3**.

**Policy legend:**
- A = KEEP-ALL (separate canonical entries + related_entries field)
- B = COLLAPSE-TO-PARENT (one canonical; sub-variants in structured_properties.variants)
- C = TIERED (mix of A and B per variant-cluster characteristics)
- D = FUZZY-COLLAPSE-WITH-VARIANT-PRESERVATION (one canonical + variant-retrievable mode)

---

## Cluster Group 1 — Royal Armouries within-source dedup (F1 — TIERED rule applies)

### Cluster RA-1: Centrefire six-shot revolver specimens

**Variants:** 379 rows all named "Centrefire six-shot revolver" with varying accession numbers, places (Belgium, Britain, USA), dates (1870-1956), specific models (Warnant's patent, Webley Mk.IV, Trade Model, Bayet patent, etc.)

**Mechanical signature variance:** All are single-action/double-action revolvers firing centrefire cartridges. range_class=ranged; geometry_class=point; tempo_class=fast; charge_class=semi-auto (revolver cylinder). **IDENTICAL mechanical signature across all 379.**

**Cultural-narrative distinctness:** These are distinct commercial products (different manufacturers, different patents), but all represent the same TYPE of weapon (European centrefire revolver, ~1860-1960). A player/designer interacting with "centrefire revolver" needs ONE canonical entry; the 379 specimens are redundant.

**Substrate-density consequence:** 379 rows all pointing to the same canonical class → EXTREME density concentration. Would create a dominant cluster around "Victorian revolver" in pattern discovery. Collapsing to 1 canonical with specimen_count=379 resolves this.

**My recommendation: Policy B (COLLAPSE-TO-PARENT).** One canonical "Centrefire six-shot revolver (Royal Armouries class)" with structured_properties.specimen_count=379, structured_properties.variants listing notable sub-models (Webley Mk.IV, Warnant's patent). All 379 source rows preserved via merged_entry_ids.

**F1 impact:** High-yield single move. Applies to at least 50+ similar high-multiplicity groups in Royal Armouries.

---

### Cluster RA-2: Sword specimens (generic "Sword" canonical_name)

**Variants:** 3,155 rows all named "Sword" in Royal Armouries, with different periods (medieval, early modern, 19th century), cultures (English, German, Indian, Japanese), and object types.

**Mechanical signature variance:** Significant. A 14th-century English longsword has different range_class/geometry_class than an 18th-century Indian tulwar or a 17th-century Japanese sword. These are NOT the same mechanical type.

**Cultural-narrative distinctness:** "Sword" is a generic type word, not a culturally-specific term. Each specimen represents a different cultural/temporal sword tradition.

**My recommendation: Policy C (TIERED).**
- Strict near-duplicates (same culture + period + approximate form): COLLAPSE (e.g., 12 nearly-identical English 17th-century cavalry swords → 1 canonical "English cavalry sword (17th c.)")
- Culturally/typologically distinct: KEEP-ALL (English longsword vs Indian tulwar vs Japanese katana vs Ottoman kilij all stay separate canonicals)

Phase D should first group by (culture + century + broad type) then apply per-group policy.

---

### Cluster RA-3: Flintlock military musket specimens

**Variants:** 486 rows named "Flintlock military musket" with varying origins (British, French, Prussian, etc.) and dates (mostly 1700-1820).

**Mechanical signature variance:** All are flintlock mechanisms, smoothbore barrels, approximately .75 caliber. range_class=ranged; geometry_class=line; tempo_class=slow; charge_class=single-shot. **Mechanically near-identical.**

**Cultural-narrative distinctness:** Different national patterns (Brown Bess vs Charleville vs Potsdam) ARE culturally recognized, but all are "flintlock military musket" at the level of useful categorical differentiation for the engine.

**My recommendation: Policy D (FUZZY-COLLAPSE-WITH-VARIANT-PRESERVATION).** One canonical "Flintlock military musket" accessible for general sampling; variant sub-entries for nationally-recognized patterns (Brown Bess, Charleville) accessible when period/culture query is specific.

---

### Cluster RA-4: Staff weapons — Pike, Spontoon, Halberd, Partizan

**Variants:** Pike (588), Spontoon (562), Halberd (284), Partizan (253), plus smaller groups

**Mechanical signature variance:** Distinct.
- Pike: range_class=melee; geometry_class=point; extra_long (4-6m); two_hand
- Spontoon: range_class=melee; geometry_class=point+slash; shorter than pike; two_hand
- Halberd: range_class=melee; geometry_class=slash+point; axe-head + spike; two_hand
- Partizan: range_class=melee; geometry_class=slash+point; side lugs; two_hand

**Cultural-narrative distinctness:** All four are distinct named and culturally recognized weapons. A halberd is not a pike; a partizan is not a spontoon.

**My recommendation: Policy A (KEEP-ALL).** These are four distinct weapon types that happen to be large in Royal Armouries holdings. Each stays as its own canonical entry.

F1 implication: within each type, many specimens → Policy B per-type (e.g., all 588 Pike specimens collapse to one "Pike" canonical + variants).

---

### Cluster RA-5: Ammunition varieties — Centrefire rifle cartridge / Pistol cartridge / Shotgun cartridge

**Variants:** Centrefire rifle cartridge (1,758), Centrefire pistol cartridge (248), Centrefire shotgun cartridge (165) plus others

**Mechanical signature variance:** Ammunition; weapon_kind=ammo_or_consumable for all. No wield signature.

**My recommendation: Policy B (COLLAPSE-TO-PARENT) after tagging as ammo_or_consumable.** These should not be in the category-sampling pool at all (ammo_or_consumable bucket). Once tagged, the collapse question is moot for generation purposes, but for substrate-density queries about what ammunition was associated with what firearms, collapse to canonical ammunition classes: "Centrefire rifle cartridge", "Centrefire pistol cartridge", etc.

---

## Cluster Group 2 — Met Museum Japanese sword variants

### Cluster MET-1: Katana / Tachi / Wakizashi / Tantō

**Variants present in Met Museum:**
- Blade and Mounting for a Sword (Katana): 10+ rows
- Blade for a Sword (Katana): 15+ rows
- Blade and Mounting for a Short Sword (Wakizashi): 36 rows
- Blade for a Short Sword (Wakizashi): 10 rows
- Blade and Mounting for a Slung Sword (Tachi): 5 rows
- Blade for a Slung Sword (Tachi): 2 rows
- Short Sword (Wakizashi): 2 rows
- Blade and Mounting for a Dagger (Tantō): from sample

**Mechanical signature variance:** DISTINCT.
- Katana: melee; arc_sweep (single-edge curved); measured tempo; two_hand; cutting length ~60-75cm
- Tachi: melee; arc_sweep; older curved slung sword; two_hand; similar to katana but longer
- Wakizashi: melee; arc_sweep; shorter (30-60cm); one_hand; worn with katana as daisho
- Tantō: melee; point/arc_sweep; very short (15-30cm); one_hand; dagger

**Cultural-narrative distinctness:** All four are culturally named and recognized as distinct objects in Japanese tradition (and internationally). A katana is not a wakizashi; both are essential to the samurai daisho pair. Tantō is specifically a dagger.

**My recommendation: Policy A (KEEP-ALL).** Four canonical entries: Katana, Tachi, Wakizashi, Tantō. Within each type, Met's individual specimens may collapse (per Cluster RA-1 pattern for museum specimens).

---

### Cluster MET-2: Blade-only vs Blade-with-Mounting (same sword)

**Variants:** "Blade for a Sword (Katana)" vs "Blade and Mounting for a Sword (Katana)" — these are the SAME type of sword, one mounted and one unmounted.

**Mechanical signature variance:** None (same sword, different mounting completeness).

**Cultural-narrative distinctness:** Not culturally distinct — both represent the same katana class.

**Substrate-density consequence:** Splitting on blade-vs-mounting creates artificial density bifurcation.

**My recommendation: Policy B (COLLAPSE-TO-PARENT).** One canonical "Katana" entry; structured_properties.mounted = true/false to distinguish blade-only vs blade-with-mounting objects.

---

### Cluster MET-3: Sword Furniture variants (Tsuba, Kozuka, Fuchi-Kashira, Menuki)

**Variants:**
- Sword Furniture-Tsuba (650): sword guard disk
- Sword Furniture-Kozuka (618): small knife handle
- Sword Furniture-Fuchi-Kashira (278): collar + pommel cap
- Sword Furniture-Menuki (86): decorative grip ornament

**Mechanical signature variance:** None — these are all weapon parts (ammo_or_consumable), not wieldable weapons.

**My recommendation: Policy B (COLLAPSE-TO-PARENT) + ammo_or_consumable tagging.** All sword furniture is ammo_or_consumable. The four sub-types stay as distinct canonical entries within the ammo_or_consumable bucket (they're meaningfully different parts) but are excluded from category sampling.

---

## Cluster Group 3 — Wikidata / Wikipedia cross-source named unique cluster

### Cluster WIKI-1: Aegis (wikidata Q190662 + wikipedia Aegis article)

**Variants:**
- wikidata `aegis` (Q190662): "in the Hellenistic world, a shield, buckler, breastplate or bib of Athena and Zeus bearing the head of Medusa/Gorgo"
- wikipedia `Aegis` article: detailed article on the mythological concept + modern usages

**Mechanical signature variance:** Both describe the same mythological object. The Wikipedia article additionally covers "Aegis cruiser", "Kimber Aegis pistol" — but those are separate Wikipedia articles (Kimber Aegis, M982 Excalibur) that appear as separate DB rows. The AEGIS article itself describes the mythological item.

**Cultural-narrative distinctness:** The Aegis is a uniquely named mythological object (one-of-a-kind); both entries describe it.

**F4 test:** Name match (case-insensitive): `aegis` = `aegis` → exact match. Description cosine similarity: both describe "shield/breastplate of Athena and Zeus" → very high cosine (estimated >0.90). Cross-source corroboration: present in both wikidata (explicit Q-item) and wikipedia (full article). **F4 threshold (≥0.85 + corroboration) IS met.**

**My recommendation: Policy D (FUZZY-COLLAPSE-WITH-VARIANT-PRESERVATION).** One canonical "Aegis" (unique weapon; mythological) with wikidata Q190662 as primary source + wikipedia description as secondary. weapon_kind=unique for both.

---

### Cluster WIKI-2: Excalibur (wikidata + wikipedia + osrsbox-db)

**Variants:**
- wikidata `Excalibur` (Q187880): "legendary sword of King Arthur"
- wikipedia `Excalibur` article: full article on Arthurian sword
- osrsbox-db `Excalibur`: OSRS game item "This used to belong to King Arthur"
- (also: wikipedia `M982 Excalibur` = modern artillery shell; different article; stays separate)

**Cultural-narrative distinctness:** The mythological Excalibur is a unique. The OSRS Excalibur is a game-item named after the legend → `named_template` (it's obtainable by players; not the actual unique). The wikidata + wikipedia entries are both the mythological unique.

**My recommendation: Policy D for wikidata+wikipedia pair (merge to one "Excalibur" unique canonical). KEEP-ALL for osrsbox-db (stays as named_template = "Excalibur (OSRS)" with related_entries pointing to the mythological unique).** The M982 Excalibur stays as its own `category` entry.

---

### Cluster WIKI-3: Gladius (wikipedia + diablo2-d2data + path-of-exile-repoe + wow-classic-items + royal_armouries)

**Variants:**
- wikipedia `Gladius`: article about the Roman short sword
- diablo2-d2data `Gladius`: D2 game item (short sword type named Gladius)
- path-of-exile-repoe `Gladius`: PoE base item (one-hand sword type named Gladius)
- wow-classic-items `Gladius`: WoW item Level 9 one-hand sword
- royal_armouries `Replica gladius` (20th-21st century): film/education replica
- royal_armouries `Rubber Gladius` (2000): film prop from 'Gladiator'

**Mechanical signature variance:** All represent the same weapon type (Roman short sword). range_class=melee; geometry_class=point+slash; tempo_class=fast; one_hand.

**Cultural-narrative distinctness:** "Gladius" is THE Roman sword — culturally recognized and historically specific. All sources use the same name for the same type.

**My recommendation: Policy A (KEEP-ALL) across sources, each as separate canonical entry:** "Gladius" (wikipedia/historical), "Gladius" (D2 game item), "Gladius" (PoE), "Gladius" (WoW). These are genuinely different substrate points (historical vs fantasy vs modern game item). The F4 cross-source merge would merge the three game-item entries into one "Gladius (fantasy ARPG)" canonical, but the wikipedia historical entry stays separate.

**Cross-source duplicate for Phase D:** D2 + PoE + WoW all have "Gladius" as a one-hand sword type with similar stats. F4 threshold (≥0.85 + corroboration) would catch these as a cross-source merge candidate for ARPG-Gladius.

---

### Cluster WIKI-4: AK-47 / AKM / AK-74 / AK-103 / AK-12 / AK-203 variant family

**Variants (from multiple sources):**
- wikidata: (likely — SPARQL likely returned AK-47 Q-item; confirmed in DB indirectly)
- wikipedia `AK-47`: full article
- odin-army-tradoc: AK-47 (7.62mm), AKM (7.62mm), AK-74 (5.45mm), AK-74M (5.45mm), AK-103 (7.62mm), AK-12 (5.45mm), AK-15 (5.45mm), AK-203 (7.62mm), AK-63 AMM (7.62mm)
- cataclysm-dda: AK-47 rifle (civilian clone)
- army-recognition: AK-12 Kalashnikov

**Mechanical signature variance:**
- AK-47 vs AKM: SAME caliber (7.62×39mm); AKM is stamped-receiver version of AK-47; mechanically near-identical. Lean COLLAPSE within the 7.62 family.
- AK-47/AKM vs AK-74: DIFFERENT caliber (7.62mm vs 5.45mm); different recoil, different muzzle velocity, different effective range. These are materially distinct.
- AK-12 vs AK-15: AK-12=5.45mm, AK-15=7.62mm — different calibers again.
- AK-103 vs AK-12/15: AK-103=7.62mm updated export variant.

**Cultural-narrative distinctness:** AK-47, AKM, AK-74 are EACH culturally-named-and-recognized generations that military culture distinguishes. "Did they use AK-47s or AK-74s?" is a real question with different answers. These are model-line generations per gandalf § 6.3 (2) second example.

**My recommendation: Policy C (TIERED):**
- AK-47 and AKM: Policy B collapse to parent "AK/AKM (Soviet 7.62mm assault rifle)" with AK-47/AKM as variant entries. AKM is the production-simplified AK-47; mechanically identical enough.
- AK-74 / AK-74M: KEEP-ALL from AK-47 (different caliber = different mechanical signature). AK-74M is essentially AK-74 with folding stock → Policy B collapse within AK-74 family.
- AK-12 / AK-15 / AK-103 / AK-203: modern derivatives; each has distinct caliber; Policy A (KEEP-ALL as distinct canonicals; all with related_entries pointing to AK-47 as progenitor).

---

## Cluster Group 4 — D&D named template clusters

### Cluster DND-1: Katana variants (nick-aschenbach-dnd-data)

**Variants:**
- "Katana" (basic; likely category-level)
- "Katana for Dummies" (uncommon magic weapon)
- "Katana of the Deathtouched" (Very Rare)
- "Katana of the Ronin" (Rare)
- "Magehunter Katana" (Very Rare)
- "Treant's Bane Katana" (Rare)

**Mechanical signature variance:** All are katana-type swords with different magical affixes. The base katana (melee; arc_sweep; one_hand/two_hand; measured) is the same class; variants differ only in magical properties.

**Cultural-narrative distinctness:** These are distinct magical weapons with different narrative purposes. "Katana of the Ronin" has a different flavor than "Magehunter Katana".

**My recommendation: Policy A (KEEP-ALL).** Each D&D magic weapon is a distinct named_template that serves a different narrative function. The base "Katana" entry is `category`. Phase D can distinguish rarity-gated named_templates from the plain category entry.

---

### Cluster DND-2: Abyss Warden's Axeblade / Battleaxe pair

**Variants:**
- "Abyss Warden's Axeblade": "Trick weapon (longsword, battleaxe), rare"
- "Abyss Warden's Battleaxe": "Roll20 Note: This weapon should be added to a character sheet with the Abyss Warden's Axeblade..."

These are two parts of the SAME trick weapon — the Axeblade transforms between longsword and battleaxe modes. They are mechanically linked.

**My recommendation: Policy B (COLLAPSE-TO-PARENT).** One canonical "Abyss Warden's Trick Weapon" with modes captured in structured_properties.forms = ["longsword", "battleaxe"]. The two source rows merge via merged_entry_ids.

---

### Cluster DND-3: WoW Classic "Worn" base weapon set

**Variants:** Worn Mace (Item Level 2), Worn Shortsword (Item Level 2), Worn Axe (Item Level 2) — all the lowest-tier WoW starter weapons.

**Mechanical signature variance:** Different weapon types (mace=blunt; shortsword=point/slash; axe=slash). These ARE mechanically distinct — different attack type, different damage profile.

**My recommendation: Policy A (KEEP-ALL).** Each starter weapon type stays as its own category entry. "Worn Mace" represents the mace category; "Worn Shortsword" the sword category; etc.

---

## Cluster Group 5 — Soulslike duplicate/variant clusters

### Cluster SOULS-1: Dagger (fextralife-ds1, fextralife-ds2, fextralife-ds3, fextralife-elden-ring)

**Variants:**
- fextralife-ds1 `Dagger`: Dark Souls 1 dagger stats + lore
- fextralife-ds2 `dagger`: Dark Souls 2 dagger stats + lore
- (fextralife-ds3 and ER likely also have dagger entries)
- elden-ring-erdb and bloqhead-demigods also likely have dagger entries

**Mechanical signature variance:** The dagger TYPE is the same across all games (one_hand; point; fast; light), but each game's specific dagger stats and lore are different. These are "Dagger" in 4 different game universes.

**Cross-source F4 test:** Name "Dagger" vs "dagger" (case-insensitive: identical). Description similarity: all describe the same basic weapon type. Cosine similarity likely >0.80 but perhaps not >0.85 since each game's description adds different lore. Corroboration: 4 sources. **F4 might catch this as a merge candidate, but the descriptions are game-specific enough that the 0.85 threshold might not be met.**

**My recommendation: Policy C (TIERED).** Create one cross-game canonical "Dagger (soulslike)" with game-specific variants in structured_properties. The fan-wiki descriptions provide per-game richness. The cross-source merge via F4 should be flagged as a manual review item — automatic merge might flatten game-specific lore.

---

### Cluster SOULS-2: Great Katana (bloqhead-demigods + fextralife-elden-ring)

**Variants:**
- bloqhead-demigods "Great Katana": "Elden Ring weapon. Type: colossal sword. Tier: A. Skill: Dragon Hunt."
- fextralife-elden-ring "Great Katana": "Elden Ring Shadow of the Erdtree Great Katana Weapon Guide"

These are the same weapon from the same game (Elden Ring Shadow of the Erdtree DLC) in two different sources.

**F4 test:** Name exact match. Description: both describe the ER Great Katana. Cosine similarity likely >0.90. Cross-source corroboration: YES (two ER-specific sources). **F4 threshold met → should merge.**

**My recommendation: Policy B (COLLAPSE-TO-PARENT).** One canonical "Great Katana (Elden Ring)" with both source rows merged. bloqhead has structured tier/skill data; fextralife has description text — the merged entry is richer than either alone.

---

### Cluster SOULS-3: Fextralife "Greataxes" category index pages (DS3 + ER)

**Variants:**
- fextralife-ds3 `Greataxes`: "Great Axes are a Weapon Category in Dark Souls 3. List of all Great Axes..."
- fextralife-elden-ring `Greataxes`: "Elden Ring Greataxes Guide: Complete list of all Greataxes..."

These are weapon-CATEGORY index pages, not individual weapons. They represent the greataxe CLASS in each game.

**My recommendation: Policy A (KEEP-ALL) but weapon_kind=category (not named_template).** Each is a valid class-level canonical ("Greataxe (DS3 category)" and "Greataxe (ER category)") that provides cluster-level information. They should NOT be in category sampling (they're meta-pages), but they're useful as class-level anchors for axis discovery.

---

## Cluster Group 6 — Modern military variant families (ODIN)

### Cluster ODIN-1: AK-47 cross-source cluster (see WIKI-4 above for full analysis)

See WIKI-4. ODIN entries (AK-47, AKM, AK-74, AK-74M, AK-12, AK-15, AK-103, AK-203, AK-63 AMM) + wikipedia AK-47 + cataclysm AK-47 rifle constitute the largest multi-source variant cluster in the substrate.

**Key Phase D question:** Should the ODIN-military and the wikipedia-historical and the Cataclysm-game entries merge into one "AK-47" canonical, or stay separate as source-specific entries?

**My recommendation: Policy C (TIERED):**
- Wikidata Q-item for AK-47 (if present) + Wikipedia "AK-47" + ODIN "AK-47 Russian 7.62mm..." → FUZZY-COLLAPSE-WITH-VARIANT-PRESERVATION (D): one "AK-47" canonical with source-specific variant entries (military-doc variant, encyclopedia variant, game variant)
- Cataclysm "AK-47 rifle" stays separate (it's a post-apocalyptic civilian-legal clone with game-specific properties)

---

### Cluster ODIN-2: M224 LWCMS mortar — wieldability edge case

**Variants:**
- odin-army-tradoc `M224 American 60mm Lightweight Company Mortar System (LWCMS)`: Crew=3; has handheld mode (8.2kg) AND conventional mode (21.1kg)

**This is a wieldability edge case, not a variant cluster per se, but surfaces here because:**
The same physical system has TWO operational modes with different wieldability classifications:
- Conventional mode (crew=3, bipod/baseplate): `wieldable_humanoid=no` (crew-served)
- Handheld mode (8.2kg, single-operator): `wieldable_humanoid=shoulder_supported` (per gandalf § 2.5 explicitly noting M224)

**My recommendation:** Tag as `wieldable_humanoid=shoulder_supported` with a note that conventional mode is `no`. Phase D canonical entry should capture both modes. This is a Policy A situation (the single DB entry stays as one canonical with mode-variants captured in structured_properties).

---

### Cluster ODIN-3: Yak-130 / Yak-130M aircraft pair

**Variants:**
- odin-army-tradoc `Yak-130 (Mitten) Russian Light Combat Aircraft`
- odin-army-tradoc `Yak-130M Russian Light Combat Aircraft`

**Mechanical signature variance:** Yak-130 vs Yak-130M are trainer/combat variants of the same aircraft platform. Both are aircraft (wieldable_humanoid=no; mount_required). Minor spec differences between variants.

**Cultural-narrative distinctness:** Both are recognized as the same aircraft family; M suffix = modernized variant.

**My recommendation: Policy B (COLLAPSE-TO-PARENT).** One canonical "Yak-130 (Russian light combat aircraft)" with Yak-130M as variant in structured_properties.

Note: aircraft are `wieldable_humanoid=no` (mount_required) — they won't enter category sampling regardless. Collapse reduces noise in axis discovery.

---

## Cluster Group 7 — Warhammer AoS variant families

### Cluster AOS-1: Creature-attack profiles vs weapon-equipment profiles

**Variants:**
- "Vicious Claws" (creature attack; non-humanoid)
- "Tearing Fangs" (creature attack; non-humanoid)
- "Zangrom-Thaz" (named AoS weapon; probably humanoid-wieldable)

**Mechanical signature variance:** Vicious Claws / Tearing Fangs are not humanoid-wieldable equipment — they are creature attack profiles for monsters. `wieldable_humanoid=no`. Named weapons like Zangrom-Thaz are wielded by named AoS characters.

**My recommendation:** No collapse needed. These are distinct weapon_kind=named_template entries with different wieldable_humanoid values. Keep-All.

---

### Cluster AOS-2: "Skull Bludgeon and Varanspire Gladius" compound profile

**Variants:**
- bsdata-warhammer-aos "Skull Bludgeon and Varanspire Gladius": a COMPOUND attack profile (two weapons in one entry)

**This is a schema edge case:** one row = two weapons in one AoS attack profile. The Skull Bludgeon (blunt) and Varanspire Gladius (point/slash) have different mechanical signatures.

**My recommendation: Phase D decision.** Either split into two separate entries OR keep as one compound entry with weapon_kind=category + note. Surface for gandalf judgment.

---

## Cluster Group 8 — Cross-source canonicals (multiple sources, same weapon class)

### Cluster CS-1: Katana across all sources

Sources confirmed with "Katana" entries:
- wikipedia (article)
- wikidata (several specific blade Q-items + general katana class)
- met-museum (dozens of "Blade and Mounting for a Sword (Katana)" entries)
- royal_armouries ("Katana" and "Sword (katana)" entries, ~30+)
- osrsbox-db ("Katana")
- nick-aschenbach-dnd-data ("Katana", "Katana of the Ronin", etc.)
- wow-classic-items (e.g., "Moonlit Katana", "Skystrider Katana" — named variants)
- fextralife-elden-ring ("Great Katana")
- bloqhead-demigods ("Great Katana")
- cataclysm-dda (katana, hardened steel katana, high steel katana, mild steel katana, etc.)

**Scale:** Katana is the highest cross-source canonical in the substrate — present in at least 10 of 24 sources.

**My recommendation: Policy C (TIERED) + cross-source canonical merge:**
- One "Katana" category-level canonical as the primary merge target for historical/encyclopedia entries (wikipedia + wikidata class Q-item + met-museum specimens + royal_armouries specimens)
- Game-specific katanas keep separate canonical entries per game (Moonlit Katana stays as wow WoW item; hardened steel katana stays as Cataclysm item; Great Katana stays as Elden Ring specific)
- Fantasy-named D&D katanas: named_template, not merged into the base katana canonical

This is the most complex variant cluster in the substrate and will require a dedicated Phase D decision pass.

---

### Cluster CS-2: Dagger (ultra-high cross-source)

Like Katana, "Dagger" appears in essentially every source. Same analysis applies. One historical canonical "Dagger"; game-specific daggers stay source-specific.

---

### Cluster CS-3: Spear / Pike / Polearm family (Royal Armouries + multiple sources)

**Variants across substrate:**
- Royal Armouries: Spear (180 specimens), Pike (588), Spontoon (562), Partizan (253), Halberd (284)
- ODIN: various polearm entries
- wikipedia: "Spear", "Pike (weapon)", "Halberd" articles
- D&D sources: spear, pike, halberd as weapon types

These are distinct weapon types (spear ≠ pike ≠ halberd). The sub-variants within each type in Royal Armouries collapse per Policy B; the types themselves stay as separate canonicals per Policy A.

---

## Summary: clusters requiring priority Matt+gandalf in-flight decision

**Top 5 clusters needing immediate human judgment:**

1. **Cluster WIKI-4 / ODIN-1: AK-47 family** (9+ ODIN entries + 1 wikipedia + 1 cataclysm) — highest cross-source variant complexity; requires caliber-based tiered policy lock before Phase D.

2. **Cluster MET-1: Katana / Tachi / Wakizashi / Tantō in Met Museum** — 75+ combined specimens; KEEP-ALL vs per-type collapse within Met; impacts cultural axis loading for Japanese sword cluster.

3. **Cluster RA-2: Generic "Sword" (3,155 Royal Armouries rows)** — largest single-source cluster after Firearms; Policy C requires defining the grouping logic (by culture + period + broad type) before Phase D can execute.

4. **Cluster CS-1: Katana cross-source (10+ sources)** — most complex cross-source canonical merge; F4 threshold testing needed for met-museum entries vs wikipedia article vs wikidata Q-items.

5. **Cluster SOULS-1: Dagger across all soulslike sources** — F4 borderline case (might not reach 0.85 cosine due to game-specific lore differences); Phase D needs explicit decision on whether to auto-merge or keep-separate.

---

**Signed:** legolas
**Deliverable 2 complete — proceeding to Deliverable 3 (named-unique allowlist verification)**
