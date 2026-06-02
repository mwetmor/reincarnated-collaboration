# Research — Caster Weapon Substrate Enrichment: Source Survey — 2026-06-02

**Mode:** A (analytical)
**Commissioner:** gandalf per Matt 2026-06-02 ratification
**Strategic context:** QDX-4 finding (~98% physical substrate); QDX-5 interim weighted distribution (B4: ~43% physical / ~57% caster); long-term substrate enrichment is the structurally correct path per jack-ryan QDX-6 acceptance signal.
**Composes with:** IA-2 existing 125 entries (102 gandalf anchors + 23 legolas crawl; ingested 2026-06-01); WS2.P2 modern-caster coverage (~49 modern anchors within the 102); existing substrate 90,345 rows post-IA-2.P3
**Sources consulted:** see § 9 source list

---

## Summary (4 sentences)

The caster weapon substrate enrichment landscape is large, multi-layered, and strongly bifurcated by extraction feasibility: the most commercially-clear and structurally-accessible sources are the OGL/ORC/CC-licensed RPG databases (Pathfinder Archives of Nethys, d20PFSRD, D&D SRD 5.2), which together offer 300–600 named caster implements with mechanical context but limited cultural depth. The richest sources for cultural × period × thematic diversity are the Wikipedia mythological object lists and their associated article networks, which cover 25+ cultural traditions and approximately 800–1,200+ caster-relevant entries (staves, wands, orbs, ritual implements, talismans) but require moderate extraction effort from prose and semi-structured tables. The highest-density single sources for named caster implements with provenance and lore text are the Forgotten Realms Wiki (Fandom; ~107 wands, ~150+ staves, ~80+ rods; CC-BY-SA) and the Pathfinder Archives of Nethys (OGL; 127 named staves in PF1 alone, 90+ wands, extensive rods). The most underserved period × culture gaps relative to the existing 125-entry IA-2 substrate are: (1) Renaissance/Enlightenment alchemical implements, (2) Islamic golden age magical implements (Solomonic tradition), (3) Japanese Onmyodo and Shinto ritual instruments beyond the Imperial Regalia, (4) African/Yoruba orisha implement vocabulary, (5) cultivation-genre xianxia/wuxia magical artifacts at named-weapon granularity, and (6) sci-fi magitech implements beyond the four already-crawled modern entries.

---

## Findings

### 1. Wikipedia Mythological Object Networks

**Sources:** `en.wikipedia.org/wiki/List_of_mythological_objects`, `en.wikipedia.org/wiki/List_of_magical_weapons`, `en.wikipedia.org/wiki/Category:Artifacts_in_Norse_mythology`, `en.wikipedia.org/wiki/List_of_sacred_objects_in_Japanese_mythology`, `en.wikipedia.org/wiki/Astra_(weapon)`, `en.wikipedia.org/wiki/Icelandic_magical_staves`

**Item count:**
- List of mythological objects: ~1,200–1,500 total entries across 36 category sections (conservative estimate). Caster-relevant subset (staffs/rods: 6; ritual/ceremonial/amulet categories: 60–90 across jewelry, musical instruments, containers, miscellaneous): estimated 200–350 directly caster-relevant entries.
- List of magical weapons: 100+ entries, primarily weapons, but staves/staffs appear (Ruyi Jingu Bang, Kaladanda, etc.); caster-relevant subset ~25–40.
- Astra (weapon) article: 47 named Hindu divine weapons in structured table format (deity + effect columns).
- List of sacred objects in Japanese mythology: ~30 entries (thin — primarily an index).
- Norse Mythology Artifacts category: 18 articles + 13 in "mythological Norse weapons" subcategory.
- Icelandic magical staves: 23 named galdrastafir with manuscript source citations.

**Accessibility:** Public web; no authentication. Full article text available.

**Structured data:** Mixed. The Astra article has a proper table. The main mythological objects article is prose/bullet-point. The magical weapons article is bulleted prose. Wikipedia article networks can be traversed by following internal links — each named item often has its own article with provenance, cultural source, and description.

**Thematic coverage:**
- Period: Ancient mythological (Greek, Roman, Norse, Celtic, Hindu, Mesopotamian, Japanese, Chinese, Egyptian, Islamic) strongest. Medieval (Arthurian, Carolingian, Norse saga) moderate. Renaissance/Enlightenment/Modern: minimal.
- Type: Staffs/scepters, divine implements, sacred objects, talismans, amulets, rings. Tomes/grimoires: absent. Orbs/crystals: minimal.
- Culture: 25+ traditions represented. Mesoamerican, African, Pacific Islander: sparse.

**Name + context:** Yes — Wikipedia articles typically provide cultural/period provenance + brief description. Individual articles for notable items provide primary source citations (Iliad, Mahabharata, Völsunga saga, etc.). The IA-2 legolas crawl already demonstrated this pattern: 23 entries drawn from Wikipedia-accessible mythological sources all had strong source citation quality.

**License:** CC-BY-SA 3.0 (Wikipedia standard). Commercial use permitted with attribution and share-alike.

**Extraction feasibility:** Medium. Main list articles are prose (require NLP or manual parsing). The article-network crawl pattern (list article → individual named-item articles) is highly viable for Mode B — each linked article yields a structured per-item page. The Astra article is immediately table-extractable. The Icelandic staves article is table-structured. The mythological weapons/objects lists require iterating linked articles.

**Gap flag:** The Wikipedia mythological objects article has minimal coverage of tomes/grimoires/scrolls as magical implements (no dedicated section). Those belong in the grimoire-tradition sources below. Orbs and crystals as standalone implements are also absent — they appear only as embedded elements of staves/scepters.

---

### 2. Pathfinder RPG — Archives of Nethys + d20PFSRD

**Sources:** `aonprd.com` (PF1), `2e.aonprd.com` (PF2), `d20pfsrd.com`

**Item count:**
- PF1 Archives of Nethys: 127 named magical staves (confirmed from direct page retrieval); rods category (est. 40–60 named); wands (est. 60–100 named). Total caster-implement entries: ~230–290.
- PF2 Archives of Nethys: Staves category exists (page returned navigation only; count uncertain; likely similar or smaller than PF1). Wands category exists.
- d20PFSRD: Contains a Google Spreadsheet-backed database of OGL-only content; staves section (~90–100 named per page content); also includes 3rd-party publisher entries. Total cross-PF estimate: 300–450 unique named caster implements (some overlap between PF1 and PF2).

**Accessibility:** Public web; no authentication; direct page access.

**Structured data:** Archives of Nethys pages are HTML tables with name, school, CL (caster level), aura, price — readily parseable. The d20PFSRD Google Spreadsheet is directly exportable as CSV. High extraction feasibility.

**Thematic coverage:**
- Period: Generic fantasy (not period-coded). Cultural tradition: Western high-fantasy only. No ancient/medieval/modern period tags.
- Type: Staves, wands, rods — comprehensive. Each item has a mechanical description. Many have flavor-thematic names (Staff of the Dark Tapestry, Staff of Hungry Shadows, Zenj Totem Staff, Crook of Cildhureen) that carry implicit cultural/elemental context.
- Element affinity: Most staves have explicit elemental school (fire, frost, electricity, necromancy, etc.) — valuable for substrate element-primary tagging.

**Name + context:** Each item has: name, school, mechanical effects, sometimes flavor description. No cultural/period provenance — all are Golarion-setting (Pathfinder's world). The names are often generative (Staff of Stoneweaving, Staff of Spirit-Talking) rather than culturally grounded.

**License:** OGL v1.0a for PF1 content. ORC license for PF2 content (Paizo adopted ORC post-OGL controversy in 2023). Both are permissive for derivative game content. Key constraint: Pathfinder-specific "Product Identity" (proper nouns — place names, named characters, deities like Nethys) cannot be reused. Generic mechanical item names (Staff of Fire, Staff of Charming) are OGC and freely usable. Items with Golarion-specific proper names (Staff of Nethys, Crook of Cildhureen) require name-stripping or renaming for commercial use.

**Extraction feasibility:** High. Archives of Nethys HTML tables are structured. d20PFSRD Google Sheet is directly downloadable. Elrond could ingest these efficiently. Name-curation pass required to strip PI proper nouns.

**Scale note:** This is the single largest structured database of *named* caster implements with *element-school tagging* of any source surveyed. The school tags (fire, frost, electricity, necromancy, enchantment, etc.) map directly onto the reincarnated engine's 7+1 primary element taxonomy.

---

### 3. D&D SRD 5e / 5.2 (2024 Creative Commons)

**Sources:** `5esrd.com/gamemastering/magic-items/rods-staves-wands/`, `dndbeyond.com/magic-items`

**Item count:**
- SRD 5e: 31 items (6 rods, 12 staves, 13 wands) — confirmed by direct retrieval. This is the minimal open-content slice.
- D&D Beyond full database (non-SRD books included): Significantly larger (hundreds of magic items across all sourcebooks), but most are under WotC copyright, not freely usable.
- D&D 2024 SRD 5.2: Released under Creative Commons CC-BY 4.0 (simpler than OGL). Contains the 2024 revised core items. Added ~15 new magic items per search results. Still a relatively small open set (~40–50 caster-relevant implements in the open CC portion).

**Accessibility:** 5esrd.com is public. D&D Beyond requires account for full browsing but items are individually browsable.

**Structured data:** The 5esrd.com pages are HTML tables. D&D Beyond is structured JSON internally but no public API. The SRD 5.2 PDF/text is machine-readable.

**Thematic coverage:** Western fantasy generic. No cultural/period coding. Item names are mostly mechanical-descriptive (Wand of Fireballs, Staff of Power). Less culturally generative than Pathfinder or mythological sources.

**License:** SRD 5e content: OGL. SRD 5.2 (2024): CC-BY 4.0 — cleanest commercial license of any RPG source; attribution only, no share-alike requirement, no PI name restrictions. WotC trademarked content (proper nouns like Mordenkainen) excluded, but generic item names are CC-BY free.

**Extraction feasibility:** High for SRD portion (31 items; direct HTML). Low for non-SRD WotC content (copyright-locked). Best consumption pattern: use CC-BY SRD 5.2 items as seed + augment with Pathfinder OGL/ORC items.

**Assessment:** Smallest named-item pool of any RPG source surveyed, but cleanest license. Primarily useful as license-clear seed entries rather than volume source.

---

### 4. Forgotten Realms Wiki (Fandom)

**Sources:** `forgottenrealms.fandom.com/wiki/Category:Staves`, `forgottenrealms.fandom.com/wiki/Category:Wands`, `forgottenrealms.fandom.com/wiki/Category:Rods`

**Item count:**
- Wands category: 107 confirmed per search result metadata.
- Staves category: Confirmed to exist; count uncertain from available data — estimate ~150 based on the FR wiki being broader than SRD (covers all D&D editions including 1e, 2e, 3e, 3.5e, 4e, 5e FR-specific content). May be 100–200.
- Rods category: Estimate ~80–120 (similar pattern to wands).
- Total estimate: ~280–430 named caster implements across three categories.

**Accessibility:** Public web; Fandom direct access attempted with 403 errors — Fandom anti-bot headers block direct WebFetch. However, category pages are browsable in a normal browser. Google search indexing confirms category counts. Extraction via curl with appropriate headers or via Fandom's MediaWiki API endpoint.

**Structured data:** MediaWiki categories list items alphabetically; individual item pages contain infoboxes with edition, source book, effects. The Fandom MediaWiki API (`/api.php?action=query&list=categorymembers&cmtitle=Category:Staves`) can enumerate all pages in a category programmatically without hitting the anti-bot layer.

**Thematic coverage:** D&D multiverse setting (Forgotten Realms, Greyhawk, Spelljammer, etc.). Items have edition-source tagging. Cultural tradition is Western fantasy generic, but includes Forgotten Realms-specific named items (many Realmslore-specific). Some items trace to real-world mythological analogs.

**Name + context:** Each item has: name, edition, source book reference, mechanical description, and often a flavor paragraph. Source book attribution enables secondary licensing analysis per item.

**License:** CC-BY-SA 3.0 (Fandom standard for text content). Commercial use permitted with attribution. Underlying WotC D&D content IP is separate from wiki text; wiki text describing items (not the items themselves as WotC IP) is CC-BY-SA. Practical guidance: item names that are generic (Staff of Fire) are OGC; Forgotten Realms proper-noun items (Staff of the Magi — borderline; Staff of Cildhureen — FR-specific PI) require naming caution.

**Extraction feasibility:** Medium-High. Fandom blocks direct HTTP crawl but MediaWiki API is accessible. Mode B crawl targeting specific categories (Staves, Wands, Rods, plus Orbs, Focuses, Tomes, Talismans if those categories exist) is viable via API. Individual item pages yield infobox data extractable via MediaWiki parse.

---

### 5. Fire Emblem Wiki — Tomes

**Sources:** `fireemblemwiki.org/wiki/Tome`

**Item count:**
- Tomes appear in 7 Fire Emblem games. Across the full series (all 17 games), total distinct named tomes is estimated 300–500+, with significant repetition of base types (Fire, Thunder, Wind, Elfire, Thoron, Bolting, etc.) across games. Unique named tomes (not base-class repeats): est. 150–250.
- Fire Emblem Heroes (mobile gacha) expands the pool substantially with hundreds of named tome weapons.

**Accessibility:** fireemblemwiki.org is public; Fandom variant (fireemblem.fandom.com) has the same 403 anti-bot issue but MediaWiki API available. The non-Fandom version (fireemblemwiki.org) should be accessible.

**Structured data:** Tables per game listing all tomes with might/weight/hit/crit stats. Individual tome pages provide series-appearance history.

**Thematic coverage:** JRPG-elemental. Tomes are categorized as Fire, Thunder, Wind, Dark (Flux, Nosferatu), Light (Shine, Divine), Anima (combined elemental), and individual named books. Cultural tradition: Japanese fantasy with Norse/Greek naming conventions (Rexflame, Mjolnir, Bolganone, Grimleal dark tomes). Strong "Japanese caster" substrate coverage.

**Name + context:** Names and mechanical stats; minimal lore prose per item. Cultural/period provenance: not documented at item level.

**License:** The Fire Emblem Wiki (fireemblemwiki.org) uses CC-BY-SA. The underlying game content is Nintendo IP — names of items are factual data points. Using item names (Bolganone, Excalibur, Ereshkigal) as substrate inspiration is distinct from reproducing protected expression.

**Extraction feasibility:** Medium. Tables are HTML-parseable. The large number of game-specific variants (Fire appears in 17 games) requires deduplication. Best Mode B pattern: extract unique named tomes only, not base-class repeats.

**Substrate value:** Strong for JRPG-coded tomes and elemental magic books. Complements the Western fantasy RPG sources by adding Eastern/JRPG register to the tome substrate tier.

---

### 6. Final Fantasy XIV — Thaumaturge's Arms Database

**Sources:** `ffxiv.consolegameswiki.com/wiki/Two-handed_Thaumaturge%27s_Arm`

**Item count:** 200+ named caster weapons (confirmed from direct page retrieval; organized by level bracket 1–100+). These are staves/rods for Black Mage / Thaumaturge. Additional caster weapon types (White Mage staves, Summoner books, Sage nouliths, Scholar books, Red Mage swords) exist in separate category pages. Total FFXIV caster weapon estimate: 600–900+ named items across all caster jobs and item level tiers.

**Accessibility:** Public wiki; no 403 issue encountered.

**Structured data:** HTML tables per level bracket with name, ilvl, damage, stats — well-structured.

**Thematic coverage:** Final Fantasy high fantasy setting. Naming draws from real-world mythology (Laevateinn — Norse; Thyrus — Roman; Stardust Rod — generic), alchemy, and Japanese aesthetics. Cultural registers: Western, Norse, Roman, Japanese-adjacent. Many items have flavor/lore names without documentation of origin.

**Name + context:** Names and mechanical stats. No cultural/period provenance on item pages. Lore flavor text exists on named/rare weapons but not all items.

**License:** Square Enix copyright. The FFXIV wiki is CC-BY-SA for its text, but underlying game IP (item names as creative works) is Square Enix property. Using FFXIV weapon names as substrate directly is IP-risky. However, the mythologically-derived names (Laevateinn, Thyrus, etc.) are themselves from public domain mythological sources — those can be sourced from mythology directly. The FFXIV wiki is most useful as a discovery vehicle for tracing item names back to mythological primary sources.

**Extraction feasibility:** Medium. Tables are cleanly structured. However, direct name extraction for commercial substrate use requires IP caution — items derived from mythology should be sourced from the mythological primary rather than the game derivative.

**Assessment:** High discovery value; moderate direct-extraction value due to IP constraints. Best consumed as a pointer to mythological primary sources rather than a substrate source itself.

---

### 7. Path of Exile — Unique Staves / Wands / Sceptres

**Sources:** `poewiki.net`, `pathofexile.fandom.com`

**Item count:**
- Unique staves: ~20–30 (PoE1 + PoE2 combined estimate from search results showing PoE2 staves list on mobalytics)
- Unique wands: 25 confirmed (PoE1)
- Unique sceptres: 26 confirmed (PoE1)
- Unique foci (PoE2): additional category; count uncertain
- Total caster unique implements: ~75–100+ across PoE1 and PoE2

**Accessibility:** poewiki.net returned 403 on direct fetch. pathofexile.fandom.com also returned 403. Both accessible via MediaWiki API or via search-engine-indexed data.

**Structured data:** PoE wiki uses MediaWiki with well-structured item templates including name, item class, flavor text (lore quotes), mod text. Flavor text per item is often evocative prose with cultural/metaphysical references.

**Thematic coverage:** Dark fantasy / Lovecraftian cosmic horror. Cultural tradition: Original world (Wraeclast) with real-world mythological references (Marohi Erqi — Maori; Hiltless — Japanese; Kongming's Stratagem — Chinese). Register: dark fantasy, cosmological, elemental.

**Name + context:** Each unique item has: name, item class, flavor text (1–2 sentences of lore), mod text. Flavor text is the highest-quality lore prose of any game-database source surveyed. Example: items with cosmic horror flavor text, historical/cultural name analogs.

**License:** Grinding Gear Games copyright. PoE wiki text is CC-BY-SA. Same IP constraint as FFXIV: item names are GGG property. The flavor text per item is GGG IP. Best use: discovery vehicle for thematic vocabulary and naming patterns; not direct extraction.

**Assessment:** High thematic value for flavor text vocabulary. The dark-fantasy / cosmic register fills a gap not covered by RPG database sources. Not viable for direct commercial substrate ingestion (name + flavor text are GGG IP). Useful as inspiration-layer for gandalf-authored anchors in future passes.

---

### 8. Grimoire Tradition Sources (Key of Solomon, Sacred Texts Archive, Galdrabók)

**Sources:** `sacred-texts.com/grim/`, `en.wikipedia.org/wiki/Key_of_Solomon`, `en.wikipedia.org/wiki/Icelandic_magical_staves`

**Item count:**
- Key of Solomon: ~12–15 named magical implements per the two books (knife, sword, sickle, poniard, dagger, lance, wand, staff, pentacle, aspergillum, censer, circle). Not a large named-item catalog — more a typology with construction instructions.
- Internet Sacred Text Archive grimoires: 112+ texts including Key of Solomon, Book of Ceremonial Magic, Sacred Magic of Abramelin, The Magus (Francis Barrett). Named implements per text: small (5–20 per text). Aggregate across texts: ~100–200 named or typologically-distinct implements.
- Galdrabók and Icelandic staves: 23 named galdrastafir (confirmed from Wikipedia table; source manuscripts cited).

**Accessibility:** sacred-texts.com is public. Full text of most grimoires in the public domain (pre-1927 in US; pre-1977 CE for publication; original manuscripts 15th–19th century). Archive.org holds digital scans.

**Structured data:** Prose only. No structured tables or databases. Extraction requires manual curation or NLP parsing of chapters. The Icelandic staves Wikipedia article is the exception — table-formatted.

**Thematic coverage:**
- Period: Renaissance/Enlightenment alchemical (Key of Solomon, Abramelin, The Magus = 15th–19th c); Medieval European folk magic (Galdrabók = 17th c Iceland); Late classical Greco-Egyptian (Greek Magical Papyri = 2nd c BCE – 5th c CE).
- Type: Ritual implements (wands, staffs, swords, knives, pentacles, censers, circles, seals); not named-item catalog format but typology-of-implements format.
- Cultural tradition: European ceremonial magic, Western hermetic tradition, Solomonic tradition (Jewish-Islamic-Christian syncretism), Norse/Icelandic folk magic.

**Name + context:** Context-rich: each implement has ritual purpose, material construction specification, astrological timing, inscribed symbols. Historical sources cited (manuscript shelf marks). Primary source quality is highest of any source surveyed — the Key of Solomon text IS the source.

**License:** All pre-1928 works are public domain in the US. Sacred-texts.com makes them freely available. The Wikipedia article on Icelandic staves is CC-BY-SA.

**Extraction feasibility:** Low for bulk-catalog extraction (prose-only, no structured format). Medium for targeted extraction — manual curation of implement types + names from chapter headings yields a compact but high-quality set. Estimated yield from manual pass through major grimoires: 50–80 distinct named/typologically-distinct implements.

**Assessment:** Highest cultural authenticity and primary-source quality for the Renaissance/alchemical and Western ceremonial magic registers. Small-to-medium item count but each entry is substantive. Most valuable as gandalf-authored anchor substrate rather than Mode B crawl target.

---

### 9. Hindu / Vedic Astra Database (Wikipedia)

**Sources:** `en.wikipedia.org/wiki/Astra_(weapon)`, `sanskritimagazine.com/weapons-of-the-gods/`

**Item count:** 47 named astras in the Wikipedia table (confirmed by direct retrieval). Each has deity attribution and effect description.

**Accessibility:** Public web; Wikipedia directly accessible.

**Structured data:** Wikipedia article has a proper three-column table: Astra name | Deity | Effect. Directly parseable.

**Thematic coverage:** Ancient Vedic/Hindu. Period: ancient mythological. Cultural tradition: Vedic/Sanskrit epic (Ramayana, Mahabharata, Ahirbudhnya Samhita). Type: primarily divine weapons/projectiles — not staves/wands per se, but divine implements invoked by mantra (functionally equivalent to spell-cast implements). The Brahmastra, Pashupatastra, Vajra, Trishula all qualify as caster-implement analogs.

**Name + context:** Strong. Each entry: Sanskrit name + deity + source text citation. The existing IA-2 substrate already includes Vasavi Shakti (lightning/ancient) — this source has 46 more.

**License:** CC-BY-SA (Wikipedia).

**Extraction feasibility:** High — table is directly parseable. 47 rows × 3 columns. The most immediately table-extractable mythological source surveyed.

---

### 10. Xianxia / Wuxia Cultivation Genre Sources

**Sources:** `immortalmountain.wordpress.com/glossary/`, `cultivatingdragons.com`, `wuxiaworld.com`, `webnovel.com` community discussions

**Item count:**
- The Immortal Mountain glossary: ~35 magical items/weapons entries in the implements section; ~8–10 caster-relevant.
- No single structured database of named xianxia weapons exists. Cultivation novels have thousands of named magical weapons/artifacts, but they are distributed across individual novel wikis (Fandom wikis per novel: ISSTH wiki, Coiling Dragon wiki, etc.) with no aggregate catalog.
- Named legendary items from mythology (Ruyi Jingu Bang, Erlang Shen's spear, Eight Trigrams Furnace, etc.) ARE accessible via the Chinese mythological tradition sources (Journey to the West, Romance of Three Kingdoms) — already partly represented in IA-2 crawl.

**Accessibility:** Glossary pages are public. Individual novel Fandom wikis have the same 403-block as other Fandom sites (MediaWiki API available).

**Structured data:** Glossary format (prose definitions). Individual novel wikis: item pages with infobox data. Not a unified catalog.

**Thematic coverage:** Chinese mythology + cultivation fantasy. Period: ancient (classic novels) + modern (contemporary web fiction). Type: flying swords, magic treasures (fabo), spirit tools, talismans, jade slips, seals, formation flags, cauldrons, musical instrument weapons (flute, guqin). The category of "music as magical weapon" is a culturally-specific implements type absent from Western sources.

**Name + context:** Classic mythology items (Ruyi Jingu Bang, Lotus Lantern) have strong primary source citations. Modern webnovel items have no real-world provenance — they are invented.

**License:** Classic mythology items from Journey to the West, Investiture of the Gods (Fengshen Yanyi) are public domain. Community glossary prose is openly shared. Fandom wiki text is CC-BY-SA. Modern webnovel item names from Qidian/WuxiaWorld are proprietary.

**Extraction feasibility:** Low for aggregate database. High for targeted mythology-sourced items (Journey to the West, Fengshen Yanyi, Chinese mythology) — these should be sourced via Chinese mythology primary text sources rather than webnovel wikis.

**Assessment:** The xianxia substrate gap is best addressed by: (a) mining Chinese mythology primaries (Journey to the West, Fengshen Yanyi, Classic of Mountains and Seas [Shanhaijing]) for named magical implements — these are in the public domain; (b) using the cultivation genre's implement *typology* (flying swords, jade slips, spirit seals, musical instruments) as a generative framework for gandalf-authored anchors. A structured xianxia named-weapon database does not currently exist as a single extractable source.

---

### 11. Japanese Sacred Objects / Onmyodo Implements

**Sources:** `en.wikipedia.org/wiki/List_of_sacred_objects_in_Japanese_mythology`, `en.wikipedia.org/wiki/Onmyodo`, `en.wikipedia.org/wiki/Abe_no_Seimei`

**Item count:**
- List of sacred objects in Japanese mythology: ~30 entries (confirmed; primarily index without descriptions).
- Japanese mythology broader: Shinto ritual implements (gohei, ōnusa, shide, shimenawa), Imperial Regalia (Kusanagi-no-Tsurugi, Yasakani-no-Magatama, Yata-no-Kagami), Onmyodo implements (ofuda talismans, shikigami seals, divination tools, paper effigies).
- Abe no Seimei's Seiman (pentagram) and bangshu (divination rods) are named implements.

**Accessibility:** Wikipedia is fully accessible.

**Structured data:** The sacred objects list is an index (names + brief descriptions). Individual articles for major implements (Kusanagi, the Three Sacred Treasures, Gohei) provide more detail. Onmyodo and Abe no Seimei articles describe implement types but not named-item catalog format.

**Thematic coverage:** Ancient Japanese Shinto (pre-Buddhist, kami-worship implements), Heian-period Onmyodo (divination, protective talismans, exorcism tools), Buddhist ceremonial implements. Period: ancient → medieval. Type: ritual/ceremonial implements, sacred mirrors, sacred jewels, sacred swords, talismans, paper effigies.

**Name + context:** Named objects (Kusanagi, Yata-no-Kagami) have strong textual provenance (Kojiki, Nihon Shoki). Onmyodo implements are typological (ofuda, nusa) rather than individually named in the same way. The IA-2 substrate has essentially no Japanese-period coverage — this is a clean gap.

**Extraction feasibility:** Medium. Wikipedia articles for individual items are extractable one-by-one. The Japanese sacred objects list is too thin for bulk Mode B crawl — best served by gandalf-authored anchors drawing from Kojiki / Nihon Shoki / Heike Monogatari primary texts.

---

### 12. Yoruba / African Orisha Ritual Implements

**Sources:** `en.wikipedia.org/wiki/Orisha`, `originalbotanica.com/blog/orishas-and-their-tools`

**Item count:** Not a named-item catalog. The implement vocabulary is primarily typological: Ogun's iron cauldron + machete; Shango's oshe (double-headed axe); Oya's flywhisk and iron sword; Yemoja's fan and river staff; Oshun's mirror, fan, and copper bracelet; Obatala's white staff; Eshu/Elegba's crooked staff and pouch.

**Accessibility:** Public web; orisha-focused sites are accessible.

**Structured data:** Prose articles. The "Orishas and Their Tools" page on originalbotanica.com lists implements per orisha — semi-structured (orisha → implements list).

**Thematic coverage:** Yoruba religious tradition (Candomble, Santeria, Lucumi, Orisha Worship). Period: ancient → modern continuous practice. Type: staffs, ritual blades, fans, mirrors, necklaces, pouches, cauldrons — all caster-implement analogs within the orisha practice framework.

**License:** Wikipedia articles are CC-BY-SA. The orisha ritual implements are living religious tradition — no IP restrictions on the implement names themselves.

**Extraction feasibility:** Low for bulk catalog (no structured database). Medium for targeted extraction from per-orisha articles. The vocabulary is distinctive and under-represented in all other sources surveyed — this is a clean diversity gap.

**Assessment:** Best addressed via gandalf-authored anchors drawing from publicly documented Yoruba tradition. A single targeted reference article per major orisha (21 principal orishas × 2–5 implements each = ~40–90 potential entries) would cover the gap. Not a Mode B crawl target; a gandalf authoring target.

---

### 13. Wicca / Modern Occult Implements (Historical Roots)

**Sources:** `en.wikipedia.org/wiki/Magical_tools_in_Wicca`, `sacred-texts.com/grim/`

**Item count:** 8–13 canonical Wiccan ritual tools (athame, wand, chalice, pentacle, censer, staff, boline, besom, cauldron, crystal ball, mirror, Book of Shadows, bell). These trace to Golden Dawn / Solomonic / Celtic primary sources.

**Accessibility:** Wikipedia fully accessible.

**Structured data:** Wikipedia article is well-organized prose with per-implement sections. Each implement has historical derivation (athame ← Key of Solomon; wand ← British folk magic; chalice ← Celtic cauldron tradition).

**Thematic coverage:** Modern occultism (19th–20th century synthesis). Implements are the intersection point of:
- Celtic four treasures (sword/spear/cauldron/stone)
- Solomonic tradition (ritual knife, wand, circle)
- Tarot suits (swords/wands/cups/pentacles)
- Golden Dawn ceremonial magic

**Name + context:** The implements are named but the vocabulary is small (~13 items). Their value is as a *structural framework* for categorizing caster implements across traditions (all four suits of a tarot deck are caster-implement types: wands, cups/chalices, swords/athames, pentacles/discs).

**License:** CC-BY-SA (Wikipedia). The Wicca practice itself has no IP restrictions.

**Extraction feasibility:** High — small vocabulary, well-documented. Not a Mode B crawl target (too small). Value is as a typological framework for categorizing other sources' items.

---

### 14. Sci-Fi Magitech Sources (Shadowrun, Numenera, Eclipse Phase, Mass Effect)

**Sources:** `shadowrun.fandom.com`, `montecookgames.com`, search results for Eclipse Phase, Cyberpunk 2020

**Item count:**
- Shadowrun: Foci types are categorical (7 categories: Enchanting, Metamagic, Power, Qi, Spell, Spirit, Weapon). Named foci are created by players/GMs per rules, not a named-item catalog. Few canonical named foci exist (named items are setting artifacts).
- Numenera: 400 cyphers + 225 artifacts confirmed in Technology Compendium. Total Numenera item count across all sourcebooks: 1,000+ items (per "over a thousand" claim on montecookgames.com). Most are sci-fi-magitech caster implements — cypher-class (single-use) and artifact-class (permanent).
- Eclipse Phase, Cyberpunk 2020, Shadowrun: No structured named-item catalog accessible for caster-class implements specifically.
- Mass Effect: Biotic amps (cranial implants) as a caster-implement type. A small number of named/legendary amp variants exist but no catalog.

**Accessibility:** Numenera sourcebooks are commercial PDFs (paid). Shadowrun wiki (Fandom) has 403 issue but MediaWiki API available. Eclipse Phase is CC-BY-SA licensed (the game itself!).

**Structured data:** No aggregate database available for Shadowrun/Numenera without accessing paid content. Eclipse Phase is the exception — the full game is CC-BY-SA, and its items list is accessible.

**Thematic coverage:** Sci-fi magitech / cyberpunk magical implements. Period: modern/near-future/far-future. Type: neural-amplifier implants, energy-focusing devices, single-use tech cyphers, psi-focus mesh implants, monowire weapons. This is the "modern-caster sci-fi implements" type from the commission scope.

**License:** Eclipse Phase (full game): CC-BY-SA — freely usable commercially. Numenera: commercial (Monte Cook Games); OGL content unclear. Shadowrun: proprietary (Topps/Catalyst Game Labs). Mass Effect: EA copyright. The four modern-period entries already in the IA-2 substrate (Shadowrun Dikote Monofilament Whip, Numenera Onslaught Cypher, Biotic Amp, Eclipse Phase Psi-Chi Sleight Focus) represent this category.

**Extraction feasibility:** Low (commercial books) to Medium (Eclipse Phase CC-BY-SA). The most viable path for expanding this register is Gandhi-authored anchors drawing on publicly described sci-fi-magitech tropes rather than bulk database crawl.

---

### 15. League of Legends / Runeterra Universe Items

**Sources:** `wiki.leagueoflegends.com/en-us/Universe:Unique_items`

**Item count:** ~60 unique named items across all Runeterra regions (confirmed by direct page retrieval). ~15–20 are caster-relevant (tomes, staves, magical orbs, relics).

**Accessibility:** The LoL Universe wiki (wiki.leagueoflegends.com) is public; CC-BY-SA 3.0 confirmed on page.

**Structured data:** HTML tables organized by region. Per-item: name, description, brief lore text. Easily parseable.

**Thematic coverage:** Original fantasy world (Runeterra) with multiple cultural analogs (Shurima = Egypt-analog; Targon = Greek/cosmic-analog; Ionia = East Asian-analog; Demacia = high-fantasy medieval; Zaun = steampunk). Period: game-world internal, not historical. Type: named legendary artifacts, magical tomes (Book of Thresholds), relic-stone weapons, divine instruments.

**Name + context:** Each item has brief lore prose. Cultural provenance is Runeterra-internal (not real-world grounded). Items like the "Book of Thresholds" (a sentient tome enabling instantaneous travel) are generatively interesting for substrate but carry Riot Games IP.

**License:** CC-BY-SA 3.0 (wiki text). Underlying Riot IP (item names as creative works) is Riot Games copyright. Same constraint as FFXIV — Runeterra item names are proprietary. Discovery vehicle, not direct extraction source.

**Assessment:** Discovery vehicle for modern-fantasy caster implement vocabulary. Small catalog, moderate quality. Low priority for Mode B crawl.

---

## Summary Table — Per-Source Analysis

| Source | Item Count (caster-relevant) | Accessibility | Structured | Cultural Coverage | License | Extraction Feasibility | Priority |
|---|---|---|---|---|---|---|---|
| Pathfinder Archives of Nethys (PF1) | ~230–290 (staves 127 confirmed; rods ~50; wands ~80+) | Public, no auth | HTML tables | Western fantasy generic; element-school tagged | OGL (PF1) | HIGH | **TIER 1** |
| d20PFSRD Magic Items DB | ~300–450 (PF1+PF2+3rd party; some overlap) | Public, Google Sheet | Google Sheet/CSV | Western fantasy generic | OGL | HIGH (CSV export) | **TIER 1** |
| Forgotten Realms Wiki (Fandom) | ~280–430 (wands 107 confirmed; staves ~150; rods ~100) | Fandom 403-block; MediaWiki API available | MediaWiki API | Western D&D fantasy; multi-edition | CC-BY-SA | MEDIUM-HIGH (API) | **TIER 1** |
| Wikipedia — List of Mythological Objects + article network | ~200–350 (caster-relevant subset of 1,200–1,500 total) | Public, fully accessible | Prose + tables (mixed) | 25+ mythological traditions; ancient strongest | CC-BY-SA | MEDIUM (article crawl) | **TIER 1** |
| Wikipedia — Hindu Astra table | 47 entries | Public, fully accessible | TABLE | Vedic/Sanskrit epic; ancient | CC-BY-SA | HIGH (direct table) | **TIER 1** |
| D&D SRD 5.2 (2024 CC-BY) | ~40–50 (SRD-licensed caster implements only) | Public | HTML | Western fantasy generic | CC-BY 4.0 (cleanest) | HIGH | **TIER 2** |
| Fire Emblem Wiki — Tomes | ~150–250 unique named tomes | Public (fireemblemwiki.org non-403) | HTML tables | JRPG-elemental; Norse/Greek name borrowing | CC-BY-SA | MEDIUM | **TIER 2** |
| Final Fantasy XIV Wiki | 200+ named caster weapons (thm/blm staves alone) | Public | HTML tables | FF high-fantasy; mythology-derived names | CC-BY-SA (wiki text); SE IP (names) | MEDIUM (discovery) | **TIER 3** |
| Path of Exile Wiki — unique wands/staves/sceptres | ~75–100 | Fandom/poewiki 403; MediaWiki API | MediaWiki API | Dark fantasy / Lovecraftian | CC-BY-SA (wiki text); GGG IP (names) | MEDIUM (discovery) | **TIER 3** |
| Icelandic magical staves (Wikipedia) | 23 named galdrastafir | Public, fully accessible | TABLE | Norse/Icelandic folk magic; medieval | CC-BY-SA | HIGH (direct table) | **TIER 2** |
| Internet Sacred Text Archive grimoires | ~100–200 (typological implements across all texts) | Public | Prose only | European ceremonial; Solomonic | Public domain | LOW (manual) | **TIER 2** |
| Wikipedia — Mythological weapons (magical weapons list) | ~25–40 caster-relevant | Public | Prose/bullets | Multi-cultural; primarily weapons | CC-BY-SA | MEDIUM | **TIER 2** |
| League of Legends Universe items | ~60 total (~15–20 caster-relevant) | Public | HTML tables | Runeterra-internal; cultural analogs | CC-BY-SA (wiki); Riot IP | LOW (discovery) | **TIER 3** |
| Cultivation/xianxia glossaries | ~35 (Immortal Mountain glossary) | Public | Prose | Chinese cultivation genre | CC-BY-SA / open | LOW (manual) | **TIER 3** |
| Yoruba orisha implements | ~40–90 (typological; not named catalog) | Public | Prose | Yoruba / African traditional | CC-BY-SA / no IP | LOW (manual) | **TIER 2 (gandalf)** |
| Wicca ritual tools (Wikipedia) | ~13 (typological framework) | Public | Prose | Modern occult / ceremonial magic | CC-BY-SA | HIGH (small set) | **TIER 2 (framework)** |
| Japanese sacred objects (Wikipedia) | ~30 entries (thin index) | Public | Prose index | Japanese Shinto / Onmyodo | CC-BY-SA | MEDIUM | **TIER 2** |

---

## Aggregate Scale Estimate

Combining all sources surveyed and applying conservative deduplication across sources (substantial overlap in Arthurian/Norse/Greek items across Wikipedia, D&D FR wiki, and PF1):

| Source tier | Estimated unique caster-relevant entries (post-dedup) |
|---|---|
| OGL RPG databases (PF1 AoN + d20PFSRD + D&D SRD 5.2) | 350–500 |
| Fandom wikis — FR wiki + Fire Emblem | 350–550 |
| Wikipedia mythological networks (all lists + linked articles) | 300–500 |
| Grimoire / historical occult sources | 100–200 |
| Game databases (FFXIV, PoE, LoL — discovery only) | 50–100 (if names stripped of IP) |
| **TOTAL estimated unique new entries available** | **1,150–1,850** |

Against existing substrate baseline of 125 IA-2 entries (all ingested) and existing general weapon substrate (the 90,345-row substrate has some caster weapons but ~98% physical per QDX-4), the enrichment potential is **10–15x the existing caster weapon count** before hitting diminishing returns.

Realistic Mode B crawl scope for next 2–3 enrichment sessions targeting TIER 1 sources only: **300–500 new named caster implement entries** with element-primary tagging, cultural tradition, period, and form metadata.

---

## Recommended Prioritization for Elrond Mode B Crawl

### TIER 1 — Highest leverage; authorize first

**1A. Pathfinder Archives of Nethys — Staves, Rods, Wands (PF1)**
- Count: ~230–290 items
- License: OGL — clear for commercial derivative use (with PI name stripping where applicable)
- Why first: Largest single structured database with element-school tagging; HTML tables; direct extractability; element mapping aligns with reincarnated's 7+1 primary taxonomy; diverse item name vocabulary
- Curation note: Items with Golarion proper-noun PI (Crook of Cildhureen, Staff of Nethys, Zenj Totem Staff) require renaming or exclusion; generic items (Staff of Fire, Staff of Frost, Staff of the Dark Tapestry) are OGC-free
- Mode B pattern: Crawl `aonprd.com/MagicStaves.aspx`, `aonprd.com/MagicRods.aspx`, `aonprd.com/MagicWands.aspx` — all HTML tables; extract name + school + mechanical flavor

**1B. Forgotten Realms Wiki — Category:Staves, Category:Wands, Category:Rods (Fandom)**
- Count: ~280–430 items
- License: CC-BY-SA (wiki text); WotC D&D PI caution for named items (same PI-stripping discipline as PF1)
- Why tier 1: Large named item pool across multiple D&D editions; items have per-item lore pages; culturally generative item names
- Mode B pattern: MediaWiki API category enumeration → per-item page parse for name + source edition + effects; avoid direct HTTP crawl (403 block)

**1C. Wikipedia — Hindu Astras (immediate extraction)**
- Count: 47 entries
- License: CC-BY-SA
- Why tier 1: Table-structured; immediate extractability; 47 entries directly fill ancient/Vedic gap; strong primary source citations already in table
- Mode B pattern: Direct table parse from `en.wikipedia.org/wiki/Astra_(weapon)` — 5-minute extraction

**1D. Wikipedia — Mythological Object article network (multi-session crawl)**
- Count: 200–350 caster-relevant entries
- License: CC-BY-SA
- Why tier 1: Broadest cultural × period coverage of any source; covers Arthurian, Norse, Celtic, Greek, Japanese, Chinese, Egyptian, Mesopotamian, Islamic, Hindu, African, Mesoamerican traditions
- Mode B pattern: Start from `en.wikipedia.org/wiki/List_of_mythological_objects` + `List_of_magical_weapons` → enumerate linked article URLs → fetch per-item pages → extract: name, cultural tradition, period, implement type, description, source citations
- Rate limit: 1 req/2 sec per Wikipedia's robots.txt

### TIER 2 — High quality; authorize after TIER 1 pass validated

**2A. Icelandic Magical Staves (Wikipedia)**
- Count: 23 entries
- License: CC-BY-SA
- Pattern: Direct table parse; immediate; adds Renaissance/folk-magic / Nordic register

**2B. Fire Emblem Wiki — Tomes**
- Count: 150–250 unique named tomes (after deduplication across games)
- License: CC-BY-SA (fireemblemwiki.org)
- Pattern: Per-game tome tables → deduplicate by name → extract element-type + name; adds JRPG register + elemental tome substrate

**2C. D&D SRD 5.2 (2024)**
- Count: ~40–50
- License: CC-BY 4.0 — cleanest license of all
- Pattern: Direct fetch from 5esrd.com; small set; immediate
- Note: Small but license-cleanest; good for license-certain seed entries

**2D. Grimoire tradition — targeted manual extraction (gandalf-authoring pattern)**
- Count: 50–80 distinct implements
- License: Public domain
- Pattern: Manual pass through Key of Solomon, Book of Ceremonial Magic, Abramelin — extract chapter headings for named/typological implements; gandalf authors substrate entries using implement names + historical context
- Covers: Renaissance/alchemical, Solomonic, Western hermetic — the most historically-grounded caster implement substrate

**2E. Japanese sacred objects — targeted Wikipedia crawl**
- Count: 30–60 (across Shinto implements + Onmyodo articles)
- License: CC-BY-SA
- Pattern: Start from sacred objects index + linked articles; supplemented by Kojiki / Nihon Shoki -sourced gandalf anchors
- Covers: Japanese ancient / Heian period gap

**2F. Yoruba orisha implements (gandalf-authoring pattern)**
- Count: ~40–90 entries
- License: No IP restrictions
- Pattern: Gandhi authors anchors per orisha (Shango, Yemoja, Ogun, Oya, Oshun, Obatala, Eshu × 4–6 implements each)
- Covers: African tradition gap — absent from all other sources surveyed

### TIER 3 — Discovery value; not primary crawl targets

- FFXIV caster weapons: Discovery vehicle for mythology-derived names; trace those names back to primary mythological sources and source there instead
- PoE unique wands/staves/sceptres: Thematic vocabulary / flavor text inspiration for gandalf-authored anchors; not direct extraction (GGG IP)
- League of Legends Universe items: Discovery; CC-BY-SA wiki text; small catalog; moderate quality; Riot IP on item names
- Xianxia/wuxia named weapons: No aggregate database; best sourced via Chinese mythology primaries (Journey to the West, Fengshen Yanyi, Shanhaijing)

---

## License Clearance — Recommended Sources

| Source | License | Commercial use? | Constraint |
|---|---|---|---|
| Pathfinder AoN (PF1) | OGL v1.0a | YES (OGC content) | Strip/rename Golarion PI proper nouns |
| Pathfinder 2e | ORC | YES | ORC attribution; strip Paizo-specific PI |
| D&D SRD 5.2 (2024) | CC-BY 4.0 | YES | Attribution sentence only; no share-alike |
| Wikipedia (all articles) | CC-BY-SA 3.0 | YES | Attribution + share-alike on derivative wiki content (not on substrate data per se) |
| Fandom wikis (FR, FE) | CC-BY-SA 3.0 | YES (wiki text) | Same as Wikipedia; individual D&D/Nintendo IP in underlying games requires name-level review |
| Internet Sacred Texts grimoires | Public domain | YES | None |
| Icelandic magical staves (Wikipedia) | CC-BY-SA 3.0 | YES | Attribution |
| Eclipse Phase (the game) | CC-BY-SA | YES | Full game is CC-BY-SA — unusual for a commercial RPG |

**Key constraint across all RPG sources:** The distinction between the *game mechanical item name* (OGC / CC / CC-BY-SA) and the *setting-specific proper noun* (Product Identity / copyright). Items like "Staff of Fire" (OGC), "Staff of Charming" (OGC) are freely usable. Items like "Wand of Orcus" (Orcus = WotC PI), "Staff of Nethys" (Nethys = Paizo PI), and "Wand of Orcus" require renaming to generic equivalents. This is manageable via a naming-review pass as part of elrond ingest.

**No license concerns** for mythological primary sources (Wikipedia mythological articles, Astra table, Icelandic staves, grimoire tradition works).

---

## Composition with Existing WS2.P2 / IA-2 Substrate (~125 Entries)

The existing 125 entries (ingested as of IA-2.P3 close, 2026-06-01) cover:
- ANCIENT: 24 gandalf anchors + 9 legolas crawl entries = 33 total
- MEDIEVAL: 29 gandalf anchors + 9 legolas crawl entries = 38 total
- MODERN: 49 gandalf anchors + 5 legolas crawl entries = 54 total

Per IA-2.P4 validation: coverage is PARTIALLY-CLOSED for MODERN (substrate-honest given the thinness) across all 7 primaries. ANCIENT/MEDIEVAL cells show improvement but fire/water are uniformly thin cross-period.

New Mode B enrichment from this survey composes additively:

**What TIER 1 sources add:**
- OGL RPG databases (PF1 AoN + FR Wiki): Add ~400–600 new generic fantasy caster weapons. Strong element-school coverage (fire, frost, electricity, necromancy, enchantment, conjuration, etc.). Fills the "what does a magic staff named for its magical school look like" gap.
- Hindu Astra table: 47 new ancient/Vedic entries. Fills fire/lightning/wind/earth/water via divine weapons (Agni-astra = fire; Vayu-astra = wind; Varuna-astra = water; Brahmastra = earth/universal; Vajra = lightning). Near-perfect element coverage in a single table.
- Wikipedia mythological network: 200–350 new entries spanning all cultures and ancient/medieval periods. Deepens the cultural × period matrix substantially.

**Where existing 125 entries remain thin after TIER 1:**
- Renaissance/alchemical (TIER 2 grimoire tradition)
- Japanese Onmyodo / Heian period (TIER 2 Japanese sources)
- African/Yoruba tradition (TIER 2 gandalf-authoring)
- Cultivation genre musical implements (flute, guqin — xianxia TIER 3)
- Modern-caster sci-fi beyond the 4 existing entries (TIER 3 Eclipse Phase)

**Scalability ceiling:** The 90,345-row substrate is predominantly physical weapons. Adding 300–500 caster weapon entries brings the caster ratio from ~98% physical / ~2% caster to approximately ~95% physical / ~5% caster. Reaching ~30-40% caster would require adding ~25,000–45,000 entries — far beyond what mythological/grimoire sources provide. The RPG databases (PF1/PF2/FR wiki) are the only sources at that scale, and their entries are generic-fantasy rather than culturally-grounded. The design team should assess whether 300–500 high-quality culturally-grounded caster entries vs. 25,000+ generic-fantasy mechanical entries better serves the substrate. Quality-over-quantity is the historic pattern per the existing WS2.P1 audit discipline.

---

## Knowledge Gaps Not Resolved

1. **Forgotten Realms Wiki exact category counts** for Staves and Rods could not be confirmed (403 blocks on direct fetch; 107 confirmed for Wands via search metadata). Actual counts may vary from estimates above.

2. **Pathfinder 2e staves count** from Archives of Nethys 2e was not confirmed (page returned navigation stub only). PF1 at 127 staves is confirmed.

3. **d20PFSRD Google Spreadsheet total item count** — the spreadsheet is accessible but total entry count not determined. Estimate based on PF1 + 3rd party items: 500–1,000 total entries across all item types; caster subset ~30–40% = 150–400.

4. **Chinese mythology primary sources** (Journey to the West, Fengshen Yanyi, Classic of Mountains and Seas) were not directly surveyed in this pass. These are public-domain texts with named magical implements; a targeted pass would reveal 50–100 additional Chinese mythology caster implements with strong source citation quality.

5. **Mesopotamian/Babylonian named magical implements** beyond the Enuma Elish references (Marduk's mace — already in IA-2) were not located in a structured database. The Metropolitan Museum has Mesopotamian magic scholarship but not a structured implement catalog accessible for extraction.

6. **Norse runic implements** — the Wikipedia runic articles describe the *practice* of runic inscription on staffs and objects, but no structured catalog of historically-documented runic implements (with names) was found. The Icelandic staves (23 galdrastafir) cover the medieval Icelandic folk-magic layer but not the Viking Age archaeological layer.

7. **Numenera item count verification** — the "1,000+ items" claim from montecookgames.com could not be verified against a public catalog (commercial PDFs behind paywall). Eclipse Phase (CC-BY-SA) was not directly surveyed for its caster-implement vocabulary.

---

## Source List

1. Wikipedia — List of magical weapons: https://en.wikipedia.org/wiki/List_of_magical_weapons (accessed 2026-06-02)
2. Wikipedia — List of mythological objects: https://en.wikipedia.org/wiki/List_of_mythological_objects (accessed 2026-06-02)
3. Wikipedia — Astra (weapon): https://en.wikipedia.org/wiki/Astra_(weapon) (accessed 2026-06-02)
4. Wikipedia — List of sacred objects in Japanese mythology: https://en.wikipedia.org/wiki/List_of_sacred_objects_in_Japanese_mythology (accessed 2026-06-02)
5. Wikipedia — Icelandic magical staves: https://en.wikipedia.org/wiki/Icelandic_magical_staves (accessed 2026-06-02)
6. Wikipedia — Category: Artifacts in Norse mythology: https://en.wikipedia.org/wiki/Category:Artifacts_in_Norse_mythology (accessed 2026-06-02)
7. Wikipedia — Orisha: https://en.wikipedia.org/wiki/Orisha (accessed 2026-06-02)
8. Wikipedia — Magical tools in Wicca: https://en.wikipedia.org/wiki/Magical_tools_in_Wicca (accessed 2026-06-02)
9. Wikipedia — Greek Magical Papyri: https://en.wikipedia.org/wiki/Greek_Magical_Papyri (accessed 2026-06-02)
10. Wikipedia — Key of Solomon: https://en.wikipedia.org/wiki/Key_of_Solomon (accessed 2026-06-02)
11. Wikipedia — Open Game License: https://en.wikipedia.org/wiki/Open_Game_License (accessed 2026-06-02)
12. Pathfinder Archives of Nethys (PF1) — Staves: https://aonprd.com/MagicStaves.aspx (accessed 2026-06-02; 127 staves confirmed)
13. Pathfinder Archives of Nethys (PF1) — Rods: https://aonprd.com/MagicRods.aspx (accessed 2026-06-02)
14. Pathfinder Archives of Nethys (PF1) — Licenses: https://www.aonprd.com/Licenses.aspx (accessed 2026-06-02)
15. Pathfinder Archives of Nethys (PF2) — Staves: https://2e.aonprd.com/Equipment.aspx?Category=32 (accessed 2026-06-02)
16. d20PFSRD — Magic Items DB: https://www.d20pfsrd.com/magic-items/magic-items-db/ (accessed 2026-06-02)
17. d20PFSRD — Staves: https://www.d20pfsrd.com/magic-items/staves/ (accessed 2026-06-02; 90+ items estimated)
18. D&D 5e SRD — Rods, Staves & Wands: https://www.5esrd.com/gamemastering/magic-items/rods-staves-wands/ (accessed 2026-06-02; 31 items confirmed: 6 rods + 12 staves + 13 wands)
19. D&D 2024 SRD 5.2 CC-BY announcement: https://screenrant.com/dnd-2024-srd-52-creative-commons-license-explainer/ (accessed 2026-06-02)
20. Forgotten Realms Wiki — Category:Staves: https://forgottenrealms.fandom.com/wiki/Category:Staves (accessed 2026-06-02; count not confirmed from direct fetch — 403)
21. Forgotten Realms Wiki — Category:Wands: https://forgottenrealms.fandom.com/wiki/Category:Wands (accessed 2026-06-02; 107 items per search metadata)
22. Forgotten Realms Wiki — Category:Rods: https://forgottenrealms.fandom.com/wiki/Category:Rods (accessed 2026-06-02)
23. Fandom Licensing — CC-BY-SA: https://www.fandom.com/licensing (accessed 2026-06-02)
24. Fire Emblem Wiki — Tome: https://fireemblemwiki.org/wiki/Tome (accessed 2026-06-02)
25. Fire Emblem Wiki — Dark magic: https://fireemblemwiki.org/wiki/Dark_(magic) (accessed 2026-06-02)
26. FFXIV Consolegameswiki — Two-handed Thaumaturge's Arm: https://ffxiv.consolegameswiki.com/wiki/Two-handed_Thaumaturge%27s_Arm (accessed 2026-06-02; 200+ items confirmed)
27. PoE Wiki — List of unique staves: https://www.poewiki.net/wiki/List_of_unique_staves (accessed 2026-06-02; 403 on direct fetch)
28. PoE Wiki — List of unique wands: https://www.poewiki.net/wiki/List_of_unique_wands (accessed 2026-06-02; 25 items per search metadata)
29. PoE Wiki — List of unique sceptres: https://www.poewiki.net/wiki/List_of_unique_sceptres (accessed 2026-06-02; 26 items per search metadata)
30. League of Legends Universe — Unique items: https://wiki.leagueoflegends.com/en-us/Universe:Unique_items (accessed 2026-06-02; ~60 items; CC-BY-SA 3.0 confirmed)
31. Scryfall API documentation: https://scryfall.com/docs/api/bulk-data (accessed 2026-06-02)
32. Scryfall Terms of Service: https://scryfall.com/docs/terms (accessed 2026-06-02; 403 on direct fetch)
33. Immortal Mountain — Xianxia/Wuxia Glossary: https://immortalmountain.wordpress.com/glossary/wuxia-xianxia-xuanhuan-terms/ (accessed 2026-06-02; ~35 magic implement entries)
34. Cultivating Dragons — Cultivation naming guide: https://cultivatingdragons.com/crafting-artefact-technique-and-martial-skill-names-like-a-cultivation-master-nailing-the-names-part-3/ (accessed 2026-06-02)
35. Internet Sacred Text Archive — Grimoires index: https://sacred-texts.com/grim/index.htm (accessed 2026-06-02; 112+ texts)
36. Internet Sacred Text Archive — Key of Solomon: https://sacred-texts.com/grim/kos/index.htm (accessed 2026-06-02)
37. GURPS Magic Items Catalog — Fandom: https://gurps.fandom.com/wiki/Magic_Items_Catalog (accessed 2026-06-02)
38. Shadowrun Wiki — Fandom: https://shadowrun.fandom.com/wiki/Shadowrun_magic (accessed 2026-06-02)
39. Monte Cook Games — Numenera items announcement: https://www.montecookgames.com/over-a-thousand-numenera-items-for-your-gaming-table/ (accessed 2026-06-02)
40. Orishas and Their Tools: https://originalbotanica.com/blog/orishas-and-their-tools (accessed 2026-06-02)
41. Sanskriti Magazine — Weapons of the Gods: https://www.sanskritimagazine.com/weapons-of-the-gods/ (accessed 2026-06-02)
42. ScreenRant — D&D 2024 SRD 5.2 CC license explainer: https://screenrant.com/dnd-2024-srd-52-creative-commons-license-explainer/ (accessed 2026-06-02)
43. Paizo — ORC License: https://paizo.com/orclicense (accessed 2026-06-02)
44. Galdrastafir.com: https://galdrastafir.com/ (accessed 2026-06-02)

---

**Authored:** legolas, Mode A, 2026-06-02
**Commission:** gandalf per Matt 2026-06-02 ratification
**Output path:** `agentic_orchestration/legolas/research/2026-06-02-caster-weapon-substrate-enrichment-research/synthesis.md`
