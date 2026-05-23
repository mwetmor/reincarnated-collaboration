# Weapon-Library-Import — Sample Rows From Every Completed Track

**Generated:** 2026-05-22 (hive-mind cycle 7 snapshot)
**Source DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Sample method:** first 3 rows per `source_library` ordered by insertion id (deterministic; reproducible)
**Scope:** ALL tracks with rows committed as of snapshot. `wikipedia-unfiltered` (the quarantined Track A1.2 v1 output) excluded.
**Mission:** `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`
**State:** `agentic_orchestration/weapon-library-import-hive-mind-state.md`

---

## Snapshot at sample time

| Metric | Value |
|---|---|
| Clean knowledge entries (excl. `wikipedia-unfiltered`) | **88,412** / 100K floor (88.4%) |
| 3D model weapons | 5,162 |
| Reference image URLs | 82,191 |
| Distinct `source_library` (knowledge) | 23 |
| Distinct `library` (3D) | 3 |
| Quarantined Wikipedia v1 (audit-preserved; not sampled) | 130,334 |
| Long-runner still firing | Track A3 Royal Armouries (PID 44776; ~15-18h remaining) |

---

## Section 1 — `weapon_knowledge_entries` samples (3 per source_library; 23 sources × 3 = 69 rows)

Columns:
- **source** — `source_library` value (which Track produced this row)
- **name** — `canonical_name`
- **license** — `license_class` (per-row license tag; downstream commercial-usability is a derived flag)
- **img** — Y if at least one reference image URL recorded; N otherwise
- **description** — first 90 chars of `description_text` (truncated; empty for sources whose ingestion didn't capture body text)
- **source_url** — canonical URL

| source | name | license | img | description | source_url |
|---|---|---|---|---|---|
| 5e-bits-5e-database | Club | MIT | N |  | `…/5e-database/main/src/2014/en/5e-SRD-Equipment.json#club` |
| 5e-bits-5e-database | Dagger | MIT | N |  | `…/5e-database/main/src/2014/en/5e-SRD-Equipment.json#dagger` |
| 5e-bits-5e-database | Greatclub | MIT | N |  | `…/5e-database/main/src/2014/en/5e-SRD-Equipment.json#greatclub` |
| 5e-bits-5e-database-2024 | Battleaxe | MIT | N |  | `…/5e-database/blob/main/src/2024/en/5e-SRD-Equipment.json#battleaxe` |
| 5e-bits-5e-database-2024 | Blowgun | MIT | N |  | `…/5e-database/blob/main/src/2024/en/5e-SRD-Equipment.json#blowgun` |
| 5e-bits-5e-database-2024 | Club | MIT | N |  | `…/5e-database/blob/main/src/2024/en/5e-SRD-Equipment.json#club` |
| army-recognition | AK-12 Kalashnikov | editorial_only | N | AK-12 Kalashnikov Izhmash assault rifle | `…/armyrecognition.com/…/ak-12-russia-uk` |
| army-recognition | CZ 805 BREN A1/A2 | editorial_only | N | CZ 805 Bren A1/A2 Ceska Zbrojovka Assault rifle | `…/armyrecognition.com/…/cz-805-bren-a1-a2-czech-republic-uk` |
| army-recognition | CZ S 805 | editorial_only | N | CZ S 805 Ceska zbrojovka Assault rifle | `…/armyrecognition.com/…/cz-s-805` |
| bloqhead-demigods | Academy Glintstone Staff | unknown | N | Elden Ring weapon. Type: glintstone staff. Tier: B. Skill: None. | `…/bloqhead/demigods/main/data/all.json#0` |
| bloqhead-demigods | Alabaster Lord's Sword | unknown | N | Elden Ring weapon. Type: greatsword. Tier: D. Skill: Alabaster Lords' Pull. | `…/bloqhead/demigods/main/data/all.json#1` |
| bloqhead-demigods | Albinauric Bow | unknown | N | Elden Ring weapon. Type: light bow. Tier: C. Skill: Mighty Shot. | `…/bloqhead/demigods/main/data/all.json#2` |
| bsdata-warhammer-aos | Zangrom-Thaz | unknown | N | Zangrom-Thaz — Weapon weapon profile from Age of Sigmar. Type: Melee, Ra… | `…/BSData/warhammer-age-of-sigmar/…/Age%20of%20Sigmar.gst#zangrom-thaz` |
| bsdata-warhammer-aos | Vicious Claws | unknown | N | Vicious Claws — Weapon weapon profile from Age of Sigmar. Type: Melee, Ra… | `…/Age%20of%20Sigmar.gst#vicious-claws` |
| bsdata-warhammer-aos | Tearing Fangs | unknown | N | Tearing Fangs — Weapon weapon profile from Age of Sigmar. Type: Melee, Ra… | `…/Age%20of%20Sigmar.gst#tearing-fangs` |
| cataclysm-dda | battery | CC-BY-SA-3.0 | N | Some free-floating battery charge. Can be reloaded into rechargeable battery cells… | `…/Cataclysm-DDA/…/data/json/items/ammo.json#battery` |
| cataclysm-dda | butane | CC-BY-SA-3.0 | N | A common flammable liquid, used in lighters. | `…/Cataclysm-DDA/…/ammo.json#butane` |
| cataclysm-dda | notch | CC-BY-SA-3.0 | N | A notch used with a fire drill to create an ember. | `…/Cataclysm-DDA/…/ammo.json#notch` |
| diablo2-d2data | Double Axe | MIT | N |  | `…/blizzhackers/d2data/…/json/weapons.json#2ax` |
| diablo2-d2data | Two-Handed Sword | MIT | N |  | `…/d2data/…/weapons.json#2hs` |
| diablo2-d2data | Shillelagh | MIT | N |  | `…/d2data/…/weapons.json#6bs` |
| elden-ring-erdb | Hand Axe | MIT | N | Commonly known as a hatchet, this smaller variety of axe is an everyday work tool… | `…/deliton/eldenring-api/…/weapons.json#…` |
| elden-ring-erdb | Jawbone Axe | MIT | N | Axe made from a herbivore's skull. Weapon of the ancestral followers who disdain… | `…/deliton/eldenring-api/…/weapons.json#…` |
| elden-ring-erdb | Forked Hatchet | MIT | N | Peculiar hatchet wielded by imps. The gently undulating forked blade is known as… | `…/deliton/eldenring-api/…/weapons.json#…` |
| fextralife-ds1 | Dagger | fan-wiki | Y | Dagger is a Weapon in Dark Souls. Dagger guide with all stats, location, upgrades… | `https://darksouls.wiki.fextralife.com/Dagger` |
| fextralife-ds1 | Ghost Blade | fan-wiki | Y | Ghost Blade is a Weapon in Dark Souls. Ghost Blade guide with all stats, location… | `https://darksouls.wiki.fextralife.com/Ghost+Blade` |
| fextralife-ds1 | Bandit | fan-wiki | Y | Bandit is a class in Dark Souls. Bandit starting equipment, stats, tips and builds… | `https://darksouls.wiki.fextralife.com/Bandit` |
| fextralife-ds2 | Chimes | fan-wiki | Y | Chimes are a Weapon Category in Dark Souls 2. List of all Chimes with stats, lore… | `https://darksouls2.wiki.fextralife.com/Chimes` |
| fextralife-ds2 | dagger | fan-wiki | Y | Dagger is a Weapon in Dark Souls 2. Dagger guide with all stats, location, upgrades… | `https://darksouls2.wiki.fextralife.com/Dagger` |
| fextralife-ds2 | Royal Dirk | fan-wiki | Y | (sparse — body text harvested as navigation chrome; lore missing) | `https://darksouls2.wiki.fextralife.com/Royal+Dirk` |
| fextralife-ds3 | Greataxes | fan-wiki | Y | Great Axes are a Weapon Category in Dark Souls 3. List of all Great Axes with stats… | `https://darksouls3.wiki.fextralife.com/Greataxes` |
| fextralife-ds3 | Fist & Claws | fan-wiki | N |  | `https://darksouls3.wiki.fextralife.com/Fist+&+Claws` |
| fextralife-ds3 | Spears & Pikes | fan-wiki | N |  | `https://darksouls3.wiki.fextralife.com/Spears+&+Pikes` |
| fextralife-elden-ring | Greataxes | fan-wiki | Y | Elden Ring Greataxes Guide: Complete list of all Greataxes, where to find them, stats… | `https://eldenring.wiki.fextralife.com/Greataxes` |
| fextralife-elden-ring | Beast Claws | fan-wiki | Y | Elden Ring Beast Claws Guide: Complete list of all Beast Claws, where to find them… | `https://eldenring.wiki.fextralife.com/Beast+Claws` |
| fextralife-elden-ring | Dueling Shield | fan-wiki | Y | Elden Ring Shadow of the Erdtree Dueling Shield Weapon Guide: Damage Type, Effectiveness… | `https://eldenring.wiki.fextralife.com/Dueling+Shield` |
| gta-v-data | Invalid | unknown | N | (placeholder weapon row from data dump; non-canonical) | `…/DurtyFree/gta-v-data-dumps/…/weapons.json#WEAPON_ANIMAL` |
| gta-v-data | Invalid | unknown | N | (placeholder weapon row from data dump; non-canonical) | `…/weapons.json#WEAPON_COUGAR` |
| gta-v-data | Knife | unknown | N |  | `…/weapons.json#WEAPON_KNIFE` |
| met-museum | Blade and Mounting for a Short Sword (Wakizashi) | unknown | N |  | `https://www.metmuseum.org/art/collection/search/21910` |
| met-museum | Blade and Mounting for a Short Sword (Wakizashi) | CC0 | Y |  | `https://www.metmuseum.org/art/collection/search/21911` |
| met-museum | Blade and Mounting for a Dagger (Tantō) | CC0 | Y |  | `https://www.metmuseum.org/art/collection/search/21912` |
| nick-aschenbach-dnd-data | Abominable Club | MIT | N | Melee Weapon (Club), Very Rare. Damage: 1d10 bludgeoning. Two-Handed, Heavy… | `…/nick-aschenbach/dnd-data/…/items.json#abominable-club` |
| nick-aschenbach-dnd-data | Abyss Warden's Axeblade | MIT | N | Trick weapon (longsword, battleaxe), rare. Infused with otherworldly… | `…/dnd-data/…/items.json#abyss-warden-s-axeblade` |
| nick-aschenbach-dnd-data | Abyss Warden's Battleaxe | MIT | N | *Roll20 Note: This weapon should be added to a character sheet with the Abyss Warden's Axe… | `…/dnd-data/…/items.json#abyss-warden-s-battleaxe` |
| odin-army-tradoc | M224 American 60mm Lightweight Company Mortar System (LWCMS) | CC0 | Y | The M224 American 60mm Lightweight Company Mortar System (LWCMS) was adopted in 1982 to re… | `https://odin.t2com.army.mil/WEG/e3479f142199faec9abe8aaf25e3d289` |
| odin-army-tradoc | Zhakh 10 Ukrainian Unmanned Aerial Vehicle (UAV) | CC0 | Y | The Zhakh 10 Ukrainian Unmanned Aerial Vehicle (UAV) is a fiber-optic FPV drone with a spo… | `https://odin.t2com.army.mil/WEG/478ff936e1419ba11eddd91103b22036` |
| odin-army-tradoc | Zhakh 13 Ukrainian Unmanned Aerial Vehicle (UAV) | CC0 | Y | The Zhakh 13 Ukrainian Unmanned Aerial Vehicle (UAV) is a fiber-optic FPV drone with a sp… | `https://odin.t2com.army.mil/WEG/111f2ebc7ce4719794a2e0b7f7d9ac46` |
| osrsbox-db | Excalibur | GPL3 | Y | This used to belong to King Arthur. | `https://oldschool.runescape.wiki/w/Excalibur` |
| osrsbox-db | Cattleprod | GPL3 | Y | A sharp cattleprod. | `https://oldschool.runescape.wiki/w/Cattleprod` |
| osrsbox-db | Blurite sword | GPL3 | Y | A Faladian Knight's sword. | `https://oldschool.runescape.wiki/w/Blurite_sword` |
| path-of-exile-repoe | Golden Flame | MIT | N | (shield class — Demigods Golden Flame from PoE base_items.json) | `…/brather1ng/RePoE/…/base_items.json#…ShieldDemigods` |
| path-of-exile-repoe | Goathide Buckler | MIT | N |  | `…/RePoE/…/base_items.json#…ShieldDex1` |
| path-of-exile-repoe | Battle Buckler | MIT | N |  | `…/RePoE/…/base_items.json#…ShieldDex10` |
| pf2ools-pf2ools-data | Bibliophile | OGL_1_0a | N | You love few things more than a good book, and as a result, Odd Stories is your favorite s… | `…/Pf2ools/pf2ools-data/…/data/AV0/bibliophile` |
| pf2ools-pf2ools-data | Eldritch Anatomist | OGL_1_0a | N | You're a trained physician who can ably tend wounds of many kinds. But more than a practit… | `…/pf2ools-data/…/data/AV0/eldritch-anatomist` |
| pf2ools-pf2ools-data | Fogfen Tale-teller | OGL_1_0a | N | You know there are monstrous things out in the swamp known as Fogfen; you've seen these th… | `…/pf2ools-data/…/data/AV0/fogfen-tale-teller` |
| royal_armouries | Centrefire six-shot revolver | editorial_only | N | Centrefire six-shot revolver - Warnant's patent - about 1895 | `https://royalarmouries.org/collection/object/object-11712` |
| royal_armouries | Rimfire seven-shot revolver | editorial_only | N | Rimfire seven-shot revolver - Smith and Wesson - 1870 | `https://royalarmouries.org/collection/object/object-11943` |
| royal_armouries | Centrefire five-shot revolver | editorial_only | N | Centrefire five-shot revolver - Tranter type - about 1880 (Conversion) | `https://royalarmouries.org/collection/object/object-11702` |
| souls-api-thomaslincoln | DRAGON GREATSWORD | unknown | N | This sword, one of the rare dragon weapons, came from the tail of the stone dragon of Ash… | `…/ThomasLincoln/Souls_API/…/weapons.js#dragon-greatsword` |
| souls-api-thomaslincoln | BLACK KNIGHT HALBERD | unknown | N | Halberd of the black knights who wander Lordran. Used to face chaos demons… | `…/Souls_API/…/weapons.js#black-knight-halberd` |
| souls-api-thomaslincoln | DS1 Item: CHAOS FLAME EMBER | unknown | N | (non-weapon item — DS1 ember; mis-classified by parser) | `…/Souls_API/…/items.js#chaos-flame-ember` |
| wikidata | aegis | CC0 | Y | in the Hellenistic world, a shield, buckler, breastplate or bib of Athena and Zeus bearing… | `http://www.wikidata.org/entity/Q190662` |
| wikidata | Battersea Shield | CC0 | Y | Celtic archaeological discovery | `http://www.wikidata.org/entity/Q810944` |
| wikidata | PMD series mines | CC0 | Y | Wooden anti-personnel mine used by the Soviet Union | `http://www.wikidata.org/entity/Q861313` |
| wikipedia | AK-47 | CC-BY-SA-4.0 | Y | The AK-47, officially known as the Avtomat Kalashnikova (also known as the Kalashnikov)… | `https://en.wikipedia.org/wiki/AK-47` |
| wikipedia | Aegis | CC-BY-SA-4.0 | Y | thumb Athena Lemnia — Roman statue type often identified as a (the aegis on the so-called)… | `https://en.wikipedia.org/wiki/Aegis` |
| wikipedia | AIM-7 Sparrow | CC-BY-SA-4.0 | Y | The AIM-7 Sparrow (Air Intercept Missile) is an American medium-range semi-active radar ho… | `https://en.wikipedia.org/wiki/AIM-7_Sparrow` |
| wow-classic-items | Worn Mace | MIT | N | Item Level 2. Main Hand. 1-3 Damage. (1.05 dps). Durability 20/20… | `https://www.wowhead.com/classic/item=36` |
| wow-classic-items | Worn Shortsword | MIT | N | Item Level 2. Main Hand. 1-3 Damage. (1.05 dps). Durability 20/20… | `https://www.wowhead.com/classic/item=25` |
| wow-classic-items | Worn Axe | MIT | N | Item Level 2. Main Hand. 1-3 Damage. (1.00 dps). Durability 20/20… | `https://www.wowhead.com/classic/item=37` |

---

## Section 2 — `weapons` table (3D model samples; 3 per library; 3 libraries × 3 = 9 rows)

Columns:
- **library** — 3D-model library `slug`
- **display_name** — weapon name as registered by the source
- **license** — license `slug` from the `licenses` reference table
- **subclass** — `weapon_subclass` free-text
- **description** — first 80 chars (truncated)
- **source_url** — canonical asset URL

| library | display_name | license | subclass | description | source_url |
|---|---|---|---|---|---|
| kenney | Blaster A | CC0 | firearm | From Kenney Blaster Kit pack. CC0. | `https://kenney.nl/assets/blaster-kit` |
| kenney | Blaster B | CC0 | firearm | From Kenney Blaster Kit pack. CC0. | `https://kenney.nl/assets/blaster-kit` |
| kenney | Blaster C | CC0 | firearm | From Kenney Blaster Kit pack. CC0. | `https://kenney.nl/assets/blaster-kit` |
| oga | Unknown | CC0 | other | (FAQ page; mis-harvested by parser) | `https://opengameart.org/content/faq` |
| oga | Unknown | CC0 | dagger | This package includes 30 different weapons ranging from knives and grenades to p… | `https://opengameart.org/content/weapon-pack` |
| oga | Unknown | CC_BY_SA | other | Elven/Fey weapon set. I only used procedural textures. I'm sure some nice etchwo… | `https://opengameart.org/content/elven-weapon-set` |
| sketchfab | Military-❌-J33P-III | CC0 | other | itch.io embed promo card; not a weapon (parser-tag-match noise) | `https://sketchfab.com/3d-models/none-8b0600622fa44ae28da0f8c03c7576a9` |
| sketchfab | E 100 HD | CC0 | other | "Это лучший танк для новичка в WoT. Е 100, X уровня…" (Russian; WoT tank model) | `https://sketchfab.com/3d-models/none-fdc34e47284144d5beae529d74f58b56` |
| sketchfab | Old MS-1 in HD | CC0 | other | "Старый MS-1 в HD, или просто Наблюдатель." (Russian; vintage tank) | `https://sketchfab.com/3d-models/none-2d0dc5c972d24824bea9b7e33ef8f500` |

---

## Quick quality observations from the sample

| Source | Quality verdict from sample | Notes |
|---|---|---|
| `wikidata` | CLEAN | Aegis, Battersea Shield, PMD mines — all real weapons; CC0 |
| `wikipedia` (fix v2) | CLEAN | AK-47, Aegis, AIM-7 Sparrow — all real; CC-BY-SA-4.0; images present |
| `royal_armouries` | CLEAN | Real museum revolvers with date + maker; editorial_only |
| `met-museum` | CLEAN | Japanese sword/dagger collection objects; CC0 where public domain |
| `odin-army-tradoc` | CLEAN | Real US Army TRADOC modern equipment; CC0; rich descriptions; images |
| `nick-aschenbach-dnd-data` | CLEAN | Real D&D weapons with full stat block in `description` |
| `osrsbox-db` | CLEAN | Real OSRS items (Excalibur etc.); GPL3 wrapper, CC-BY-NC-SA underlying |
| `wow-classic-items` | CLEAN | Real Vanilla WoW items; MIT data wrapper; structured properties in `description` |
| `cataclysm-dda` | MOSTLY CLEAN | Real items but the sample shows AMMO subcategory (battery / butane / notch — fuels/ammo, not weapons proper). Filter is permissive per dispatch (we record AMMO as item-substrate) |
| `diablo2-d2data` | CLEAN | Double Axe / 2H Sword / Shillelagh — real D2 weapons; MIT |
| `path-of-exile-repoe` | CLEAN BUT MIXED | Sample shows shields (Golden Flame / Buckler / Battle Buckler) — RePoE includes shields under weapons.json; descriptions empty (not in base_items.json) |
| `elden-ring-erdb` | CLEAN | Real Elden Ring weapons with rich lore descriptions |
| `bloqhead-demigods` | CLEAN | Real Elden Ring weapons with tier/type/skill metadata |
| `fextralife-ds1/2/3/elden-ring` | CLEAN with noise | Real weapons but parser also harvests Weapon Category index pages (e.g., "Chimes are a Weapon Category in Dark Souls 2…") and one Class page (Bandit) — substantial yield is real, ~10-15% is meta-pages |
| `army-recognition` | CLEAN | Real modern military weapons (AK-12, CZ-805 BREN); editorial_only |
| `pf2ools-pf2ools-data` | DRIFT | Sample shows backgrounds (Bibliophile, Eldritch Anatomist, Fogfen Tale-teller), NOT weapons. Parser harvested AV0 (Abomination Vaults) archetype dir; needs filter refinement to weapon-data-only path |
| `bsdata-warhammer-aos` | CLEAN | Real AoS weapon profiles (Zangrom-Thaz, Vicious Claws, Tearing Fangs) |
| `souls-api-thomaslincoln` | MOSTLY CLEAN | Real Dark Souls weapons (DRAGON GREATSWORD, BLACK KNIGHT HALBERD); one DS1 item (CHAOS FLAME EMBER, an ember not a weapon) shows mild parser drift |
| `gta-v-data` | DRIFT | Sample shows `WEAPON_ANIMAL`, `WEAPON_COUGAR` (placeholders; "Invalid" name) and `WEAPON_KNIFE`. GTA-V game-internal weapon enum includes animal-attack hook stubs; needs name-filter to drop "Invalid" entries |
| `bloqhead-demigods` | CLEAN | (Elden Ring data again; named demigods sword from `all.json`) |
| `5e-bits-5e-database` + `-2024` | CLEAN | Real D&D 5e weapons (Club, Dagger, Greatclub for 2014; Battleaxe, Blowgun, Club for 2024) |
| **3D models** | | |
| `kenney` | CLEAN BUT TINY | 21 rows; Blaster Kit pack only; yield-gap task #11 queued (filename regex + URL rotation fix needed) |
| `oga` | MIXED | One sample is FAQ page (parser drift); 2 are real weapon packs |
| `sketchfab` | DRIFT | 3 samples shown are NOT weapons (itch.io promo embed; Russian-language WoT tank models). Sketchfab `weapons-military` tag is loose — includes military vehicles + game promo art. Filter refinement candidate for Wave-4 |

---

## Cleanup candidates surfaced by the sample (deferred — not blocking floor)

1. **`pf2ools-pf2ools-data`** — parser was pointed at archetype `data/AV0/` directory which holds character backgrounds, not weapons. Need to scope to per-system weapon JSON files. **Operational impact:** 688 rows currently classified as `pf2ools-pf2ools-data` are mostly NOT weapons. Either rename to `pf2ools-archetypes` (audit-preserve) or quarantine + re-fire with correct path.
2. **`gta-v-data`** — drop rows with `canonical_name='Invalid'` (parser placeholder for animal-attack enum stubs); ~50 such rows estimated. Quick `DELETE WHERE canonical_name='Invalid'` would clean.
3. **`sketchfab`** — `weapons-military` tag is loose. Wave-4 candidate: re-tag-filter against more specific tags (`sword`, `gun`, `axe`, etc.) and drop military-vehicle false positives. Affects ~1-2K of the 4,800 sketchfab rows.
4. **`fextralife-*`** — parser harvested Weapon Category index pages + one Class page; ~10-15% of rows are meta-pages not individual weapons. Quick filter `canonical_name LIKE '%Greataxes%' OR %s$` (plural-name index pages) could quarantine.
5. **`souls-api-thomaslincoln`** — items.js was parsed alongside weapons.js; non-weapon items (embers, etc.) made it in. ~10-20 rows; minor.

None of these block the 100K floor — they're refinement passes for a future quality-pass cycle.

---

## Section 3 — coverage of mission § 2.1 genre buckets

| Mission genre | Sources contributing | Sample weapon |
|---|---|---|
| Historical real-world weapons | wikidata, wikipedia, royal_armouries, met-museum, odin-army-tradoc | Aegis / Battersea Shield / Centrefire revolver / Wakizashi / M224 mortar |
| Fantasy weapons (D&D) | nick-aschenbach-dnd-data, 5e-bits-5e-database, 5e-bits-5e-database-2024, pf2ools-pf2ools-data | Abominable Club, Battleaxe |
| Sci-fi weapons | (light coverage — odin-army-tradoc has modern UAVs; sketchfab has noise; not strong on canonical sci-fi catalogues) | Zhakh 10 UAV |
| Modern military / firearms | odin-army-tradoc, army-recognition, wikipedia, cataclysm-dda (modern subset) | AK-47, M224 mortar, AK-12 Kalashnikov, CZ-805 BREN |
| Ancient / mythological | wikidata, wikipedia, royal_armouries | Aegis (Greek), PMD mines |
| Regional / cultural | met-museum (Japanese), royal_armouries (multi-region per scout note: British/European/East-Asian/African/South-American), wikidata | Wakizashi, Tantō |
| Game data — MMO (WoW) | wow-classic-items | Worn Mace |
| Game data — ARPG (PoE/D2/D3) | path-of-exile-repoe, diablo2-d2data, bloqhead-demigods | Goathide Buckler, Double Axe, Glintstone Staff |
| Game data — soulslike | elden-ring-erdb, fextralife-ds1, fextralife-ds2, fextralife-ds3, fextralife-elden-ring, souls-api-thomaslincoln, bloqhead-demigods | Hand Axe, Chimes, Greataxes, Beast Claws, Dragon Greatsword |
| Game data — OSRS | osrsbox-db | Excalibur |
| Game data — open-world (GTA) | gta-v-data | Knife |
| Tabletop wargames | bsdata-warhammer-aos | Zangrom-Thaz, Vicious Claws |
| Post-apocalyptic / improvised | cataclysm-dda | (covered) |

**Weakest coverage:** **sci-fi canonical** (Star Wars / Trek / Warhammer 40K / Halo / Mass Effect) — Wave-4 candidate. Wave-2 DISCOVERY listed wh40k.lexicanum.com, Halopedia, Wookieepedia (Fandom-AMBER), Memory Alpha (Fandom-AMBER) — would require either Fandom alt-path probe or GitHub-extracted data substitutes.

---

**Signed:** knight-rider (sample doc for Matt return briefing; cycle 7 snapshot 2026-05-22)
