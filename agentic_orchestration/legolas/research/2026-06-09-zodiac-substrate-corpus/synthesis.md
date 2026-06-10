# Zodiac Substrate Corpus — Synthesis Report

**Mode:** B (systematic catalogue crawl)
**Commissioner:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-09 directive
**Crawl-start date:** 2026-06-09
**Status:** IN PROGRESS — per-tradition reporting appended as each tradition completes

---

## Progress tracker

| Tradition | Status | Entry count | Visual coverage | Notes |
|---|---|---|---|---|
| Western zodiac (12 signs) | ✅ COMPLETE | 12 | 100% all 4 sub-fields | Agent A; full star coords + image URLs |
| Western IAU constellations (88) | ⚠️ RECOVERY | — | — | Agent A hit 32K token limit; recovery batches A/B/C queued |
| Mesopotamian (MUL.APIN) | ⚠️ RECOVERY | — | — | Agent A hit 32K token limit; recovery batch queued |
| Celtic tree zodiac (13) | ⚠️ RECOVERY | — | — | Agent A hit 32K token limit; recovery batch queued |
| Norse/Germanic | ⚠️ RECOVERY | — | — | Agent A hit 32K token limit; recovery batch queued |
| Chinese zodiac (12 animals) | ✅ COMPLETE | 12 | 100% image_url + iconography | YAML validated; 2 low-sensitivity flags |
| Chinese Xiu lunar mansions (28) | ✅ COMPLETE | 28 | asterism + stars + iconography | 4 quadrant guardians; determinative stars |
| Japanese (Jūnishi) | ✅ COMPLETE | 12 | TBC | corpus-japanese-junishi.yaml written |
| Korean (Ddi) | ✅ COMPLETE | 12 | TBC | corpus-korean-ddi.yaml written |
| Vietnamese (12-animal) | ✅ COMPLETE | 12 | TBC | Cat-for-Rabbit documented |
| Tibetan (12-animal) | ✅ COMPLETE | 12 | TBC | Garuda/Nāga variant documented |
| Persian/Zoroastrian (12) | ✅ COMPLETE | 12 | image_url + iconography | Yazatas; Tishtrya=Sirius; Mithra distinguished from Roman Mithras |
| Vedic Rashi (12) | ✅ COMPLETE | 12 | image_url + stars + iconography | Sidereal vs tropical; Makara creature documented; Kalapurusha body-mapping |
| Vedic Nakshatras (27/28) | ✅ COMPLETE | 28 | full schema all 28 | 27 + Abhijit (optional); RA/Dec all yogatara; Krittika former-first noted |
| Egyptian decans (36) | ✅ COMPLETE | 36 | image_url (Dendera) + iconography | Dendera zodiac canonical ref; coffin diagonal star tables |
| Arabic Manazil al-Qamar (28) | ✅ COMPLETE | 28 | stars + iconography + Arabic script | Al-Sufi anchor; native_script populated; Islamic Golden Age sourcing |
| Mayan Tzolkin (20 day-signs) | ✅ COMPLETE | 20 | image_url + iconography | Yucatec + K'iche' dual orthography; SVG glyphs |
| Aztec Tonalpohualli (20 day-signs) | ✅ COMPLETE | 20 | image_url + iconography | SVG glyphs; Sun Stone canonical ref; Ollin = 5th world age |
| Polynesian navigator traditions | ✅ COMPLETE | 12 | image_url + stars + iconography | Hawaiian 7 + Maori 5; high sensitivity applied |
| Aboriginal Australian | ✅ COMPLETE | 5 | image_url + dark-cloud schematic | Kamilaroi + Boorong; Protocol C; restricted content excluded |
| Inuit/Arctic Circumpolar | ✅ COMPLETE | 4 | stars + iconography | Per-culture (Inuit/Sámi); high sensitivity applied |
| Andean (Quechua/Aymara) | ✅ COMPLETE | 9 | image_url + dark-cloud schematic | Yacana + dark-cloud + stellar figs; Quechua/Inca specified |
| West African (Dogon + broader) | ✅ COMPLETE | 3 | iconography | Griaule flag on all Dogon entries; van Beek (1991) cited |
| Native American (multi-tribal) | ✅ COMPLETE | 5 | iconography + stars | Per-tribe: Pawnee(Skidi)×2/Cherokee/Anishinaabe×2; sacred excluded |

**Running total: 294 entries confirmed (20 traditions complete)**
**Remaining: IAU 88 + Mesopotamian MUL.APIN (~18) + Celtic (13) + Norse/Germanic (~10) = ~129 more**
**Projected final: ~423 — clears 400 without any high-sensitivity material ✓**

---

## Per-tradition completion notes

### Western zodiac — COMPLETE (2026-06-09)
**12 entries.** All 12 signs with full schema: element/modality/ruling planet, primary stars with RA/Dec (J2000), IAU SVG image URLs, asterism schematics, mythic narratives, Babylonian predecessor cross-references. Visual coverage 100% across all 4 sub-fields. YAML produces clean parse. Per-tradition file: `per-tradition/western-zodiac.md`. Image refs: `visual-assets/western-zodiac-image-refs.md`. Corpus file: `corpus-western-zodiac.yaml` (56 KB).

### Chinese zodiac (十二生肖) — COMPLETE (2026-06-09)
**12 entries.** All 12 animals with full schema: earthly branch, fixed element, yin/yang, 2-hour periods, compatible signs, Jade Emperor race narrative per animal, Wikipedia Commons image URLs (M.A. N.Isis Alexandre "Zodiaque" series, CC-BY-SA 3.0). Cultural sensitivity: 2 low flags (Snake, Pig — minor cultural associations), 10 none. Notable: Snake/低 sensitivity flag noted because some cultures have mixed symbolism; Pig/猪 similar. Corpus file: `corpus-chinese-zodiac.yaml` (59 KB). YAML validated cleanly.

### Japanese Jūnishi — COMPLETE (2026-06-09)
**12 entries.** Distinct primary_culture = "Japanese." Key variant: position 12 is Wild Boar (Inoshishi) not Pig. Rich Japanese cultural layer documented: ema votive plaque tradition (Horse/Uma is the etymological origin of the ema system), Moon Rabbit, Nikkō's three wise monkeys, Benzaiten's white snake, Inu no Hi pregnancy ritual. Anti-collapse verified — no "East Asian zodiac" identity fields. Corpus file: `corpus-japanese-junishi.yaml` (45 KB).

### Korean Ddi (띠) — COMPLETE (2026-06-09)
**12 entries.** Distinct primary_culture = "Korean." Animal list identical to Chinese (Sheep at position 8). Korean cultural layer documented: gunghap matchmaking by zodiac, Tiger as national symbol (Hodori 1988 Olympics), Jindo dog as Korean National Treasure, **pig dream (돼지꿈)** as most auspicious Korean folklore omen, Dragon King Yongwang mythology. Corpus file: `corpus-korean-ddi.yaml` (44 KB).

### Vietnamese zodiac — COMPLETE (2026-06-09)
**12 entries.** Distinct primary_culture = "Vietnamese." **Two substitutions from Chinese:** Water Buffalo (Trâu) at position 2; **Cat (Mèo/Mão) at position 4** — documented with phonetic motivation (卯/Mão ≈ Mèo), distinct Vietnamese origin legend, cultural resonance (cats ward evil, protect rice stores, documented 2011 baby boom). Lạc Long Quân dragon myth makes Dragon sign carry Vietnamese national-identity weight. Corpus file: `corpus-vietnamese-zodiac.yaml` (49 KB).

### Tibetan zodiac — COMPLETE (2026-06-09)
**12 entries.** Distinct primary_culture = "Tibetan." Four structural differences from Chinese source documented: (1) traditional sequence begins with Hare not Rat; (2) Dragon ('Brug) is Nāga-serpent hybrid; (3) five elements use Iron not Metal; (4) rich Buddhist-tantric layer throughout — Bhavachakra pig (ignorance/moha at Wheel of Life center), Yamantaka bull-headed deity, Garuda cosmic bird, Lungta Wind Horse, Bodhisattva-monkey origin myth. Corpus file: `corpus-tibetan-zodiac.yaml` (49 KB).

### Persian/Zoroastrian — COMPLETE (2026-06-09)
**12 entries.** All 12 month-signs with named Yazata (divine beings): Farvardin/Fravashis, Ordibehesht/Asha Vahishta, Khordad/Haurvatat, Tir/Tishtrya (Sirius — astronomically specific), Mordad/Ameretat, Shahrivar/Kshathra Vairya, Mehr/Mithra (Roman Mithraism tauroctony distinguished as Roman derivative, not Avestan), Aban/Apas, Azar/Atar (sacred fire), Dey/Ahura Mazda, Bahman/Vohu Manah, Esfand/Spenta Armaiti. Faravahar symbol documented. Cultural sensitivity: none. Corpus file: `corpus-persian-zoroastrian.yaml` (65 KB).

### Vedic Rashi — COMPLETE (2026-06-09)
**12 entries.** All 12 Rashi with Sanskrit names, Jyotish ruling planets, element (Agni/Prithvi/Vayu/Jala), quality (Chara/Sthira/Dwiswabhava), Kalapurusha body-part mapping (Mesha=head through Meena=feet). Key distinctions documented: (1) sidereal vs tropical zodiac (~23° ayanamsa offset); (2) Makara documented as mythical Makara sea-creature (NOT simply goat-fish); (3) planetary exaltations and debilities captured. Corpus file: `corpus-vedic-rashi.yaml` (71 KB).

### Chinese Xiu lunar mansions — COMPLETE (2026-06-09)
**28 entries, 118 KB.** All 28 Xiu across 4 quadrants: Azure Dragon/East (Jiǎo through Jī), Black Tortoise/North (Dǒu through Bì), White Tiger/West (Kuí through Shēn), Vermilion Bird/South (Jǐng through Zhěn). Full RA/Dec for high-salience determinative stars. Element cycle confirmed as 7-element (Wood/Gold/Soil/Yang/Yin/Fire/Water per quadrant — NOT standard wuxing 5). Notable substrate details: **Mǎo #18 (Pleiades) = "Subaru" — the car brand name derives from this mansion**; **Shēn #21 (Orion) and Xīn #5 (Antares) embody an eternal-separation proverb** — these mansions never appear simultaneously in the sky, traditionally invoked for separated lovers; **Niú #9 = Qixi Festival** (Chinese Valentine's Day — the Cowherd and Weaver Girl myth); Guǐ #23 (Praesepe) visible as ghost mist to naked eye. Corpus file: `corpus-chinese-xiu.yaml` (118 KB).

### Vedic Nakshatras (27+1 lunar mansions) — COMPLETE (2026-06-09)
**28 entries, 172 KB.** All 27 standard Nakshatras plus Abhijit (28th — marked `status_in_modern_tradition: historical_reference`). Full schema for all 28: Sanskrit names with variants, gana (Deva/Manushya/Rakshasa — 10/8/9 distribution), nadi, hosting Rashi, primary star RA/Dec (J2000 for all yogatara; 19 bright-star anchor-points from Aldebaran through Markab at full precision), asterism schematic, deity, ruling planet (9-graha 3× repeating cycle), mythic narrative 2–3 paragraphs. Notable: **Krittika (#3)** was the ancient first Nakshatra (Pleiades; ~2500 BCE Galactic New Year anchor); **Mula (#19)** points toward Galactic Center; **Revati (#27)** defines sidereal zero point via ζ Piscium; **Abhijit** includes Mahabharata time-dilation narrative + Vega-as-future-pole-star. Corpus file: `corpus-vedic-nakshatras.yaml`.

### Egyptian decans (36) — COMPLETE (2026-06-09)
**36 entries, 90 KB.** All 36 decans from the coffin diagonal star table tradition, using Budge transliterations + Greco-Egyptian forms (Gundel 1936). Each entry: Egyptian name, Greco-Egyptian name, Testament of Solomon demon name (where attested), Western zodiac 10° sector placement, ancient sequence position, Coptic deity association. **Dendera Zodiac (Louvre) used as canonical composite visual reference** — all 36 decans depicted in the zodiac wheel. **Decan 10 = Sepṭet (Sirius)** — highest confidence; Sirius as the most important Egyptian astronomical star (Nile flood predictor, Isis star, Sopdet goddess). **Shesmu (#26)** = wine/oil press god; one of the most individually documented decans. Orion/Osiris body-map analysis in per-tradition summary. Cross-tradition parallels documented: Hermetic, Greek paranatellonta, Indian, Arabic, Japanese. Corpus file: `corpus-egyptian-decans.yaml`.

### Mayan Tzolkin — COMPLETE (2026-06-09)
**20 entries, 85 KB.** All 20 day-signs with Yucatec (Imix, Ik', Ak'bal…) and K'iche' modern orthography (Imox, Iq', Aq'ab'al…) dual naming captured. Two disambiguation traps flagged: K'iche' "Kan" (position 5, serpent) vs "K'at" (position 4, corn/net); and shared name "Q'anil" for positions 7 and 8 in some sources. Mayan glyphs use `MAYA-g-log-cal-D[NN]-[Name].png` Wikipedia Commons series. Aztec parallel in each entry. Cultural sensitivity: medium throughout; ajq'ij day-keeper practices excluded. Corpus file: `corpus-mayan-tzolkin.yaml`.

### Aztec Tonalpohualli — COMPLETE (2026-06-09)
**20 entries, 89 KB.** All 20 day-signs with Nahuatl names, presiding deities (all major Aztec deities represented), SVG glyphs (`[SignName]_glyph.svg` series — scalable vector). **Aztec Sun Stone identified as canonical composite visual reference** (all 20 day-signs in day-ring). Notable: **Ollin (position 17)** is uniquely double-powerful — both a day-sign AND the name of the current Fifth World Age; its glyph occupies the center of the Aztec Sun Stone. Tezcatlipoca paradoxically presides over Acatl (Reed) — the birth-sign of his great rival Quetzalcoatl. One confidence flag: Quiahuitl (position 19) disputed presiding deity (Tonatiuh vs Chantico across sources). Corpus file: `corpus-aztec-tonalpohualli.yaml`.

### Polynesian navigator traditions — COMPLETE (2026-06-09)
**12 entries, 88 KB** (7 Hawaiian + 5 Maori — distinct primary_culture tags throughout). Hawaiian: Hokule'a (Arcturus, zenith star of Hawaii), Makali'i (Pleiades, harvest season marker), Hoku Pa'a (Polaris), Newe/Maui's Fishhook (Scorpius), A'a (Sirius), Na Hiku (Big Dipper), Ke Ali'i o Kona i Ka Lewa (Canopus). Maori: **Matariki (Pleiades) with all 9 named stars documented** per Te Papa public record (Matariki, Pōhutukawa, Tupuānuku, Tupuārangi, Waitī, Waitā, Waipuna-ā-Rangi, Ururangi, Hiwa-i-te-rangi), Tautoru (Orion's Belt), Māhutonga (Southern Cross), Rehua (confidence: medium — disputed Western identity), Tama-rereti. **Note:** Pleiades appears as both Hawaiian Makali'i and Maori Matariki in same YAML file — distinct entries, distinct trigger seasons (November Northern vs June Southern). PVS-restricted navigation-path sequences and iwi-specific oral traditions excluded per Protocol B. Corpus file: `corpus-polynesian.yaml`.

### Aboriginal Australian — COMPLETE (2026-06-09)
**5 entries, 43 KB.** Per-people anti-collapse: **Kamilaroi** — Emu in the Sky (dark-cloud constellation, Coalsack-to-Milky-Way-rift, most iconic Southern sky dark-cloud figure); **Wotjobaluk (Boorong people)** × 3 — Neilloan (Mallee Fowl / Vega, nest-mound tells when to dig eggs), Warepil (Wedge-tailed Eagle / Altair), Kulkunbulla (Two Brothers / Pleiades); **Wardaman** — Lightning Brothers (Yagjagbula + Jambambal, rock-art sky figures; community-authorised per Cairns & Harney 2004; image withheld pending rock-art rights). Protocol C applied throughout; AIATSIS protocol followed; Yolngu ceremonial figures excluded (AIATSIS restriction category). Cultural sensitivity: high. Corpus file: `corpus-aboriginal-australian.yaml`.

### Inuit/Arctic Circumpolar — COMPLETE (2026-06-09)
**4 entries.** Per-culture: Inuit Tukturjuit (Caribou/Ursa Major), Inuit Aagjuuk (Altair+Tarazed — summer solstice marker), Inuit Sakiattiat (Pleiades), Sámi Sarva (Elk/Ursa Major). Anti-collapse discipline applied (Inuit ≠ Sámi ≠ Yupik). Cultural sensitivity: high. Corpus file: `corpus-inuit-arctic.yaml` (33 KB).

### Andean sky figures (Quechua/Aymara) — COMPLETE (2026-06-09)
**9 entries, 61 KB.** Dark-cloud constellations (defined by dark rifts in Milky Way, not star patterns) and stellar figures from Quechua/Aymara/Inca tradition. Documented: **Yacana** (dark-cloud Llama — most iconic Andean sky figure; spans Milky Way from Scorpius to Southern Cross rift), **Atoq** (dark-cloud Fox, Yacana's companion), **Yutu** (dark-cloud Tinamou bird), **Hanp'atu** (dark-cloud Toad near Southern Cross), **Machacuay** (dark-cloud Serpent), **Collca** (Pleiades — **El Niño agricultural proxy indicator validated in *Nature* 2000** — clarity of Pleiades in June predicts frost timing), **Chakana** (Southern Cross — cosmological axis mundi, 3-tier world model; Chakana cross motif appears throughout Andean material culture), **Orqo-Ciella** (Bull/Taurus stellar figure), and **Katachillay** (α+β Centauri — dual roles: eyes of Yacana AND independent llamaherder stars). Academic anchor: Urton (1981) *At the Crossroads of the Earth and the Sky*; Bauer & Dearborn (1995) *Astronomy and Empire in the Ancient Andes*. Dark-cloud schematics use Milky Way rift diagram in `image_url`; distinct visual_representation type from stellar-coordinate traditions. Cultural sensitivity: medium. Corpus file: `corpus-andean.yaml`.

### West African (Dogon + broader) — COMPLETE (2026-06-09)
**3 entries, 31 KB.** Dogon people of Mali: Po Tolo (Sirius A — the tiny but densest star, grain of Fonio), Emme Ya Tolo (Sirius companion — disputed existence), Amma's egg (cosmic origin symbol, primordial star-grain). **Griaule controversy flag applied to all 3 entries** — Marcel Griaule's 1930s claims about Dogon foreknowledge of Sirius B are contested by van Beek (1991 *Current Anthropology* reinvestigation). Corpus entries record documented tradition as transmitted through Griaule's fieldwork without asserting astronomical precision claims. Cultural sensitivity: medium. Corpus file: `corpus-west-african.yaml`.

### Native American (multi-tribal) — COMPLETE (2026-06-09)
**5 entries, 44 KB.** Per-tribe anti-collapse strictly applied: **Pawnee (Skidi Band)** — (1) Council of Chiefs (Corona Borealis): star-council of divine beings; documented Chamberlain (1982) *When Stars Came Down to Earth* + Field Museum Star Chart #16979; (2) Star-That-Does-Not-Walk-Around (Polaris) — cosmic peg of the north; **Cherokee** — Ani Tsutsa (Pleiades / The Boys: seven boys who became stars); **Anishinaabe** — (1) Fisher Stars (Ursa Major / the Fisher spirit who brought summer to the world); (2) Manidoominensag (Pleiades / Spirit Seed People). "Native American zodiac" construct explicitly excluded. Navajo ceremonial figures and Lakota sacred sky-animals deferred: NMAI institutional guidance and Goodman (1992) source-verification pending; Phase 2 candidates if public-record status confirmed. Cultural sensitivity: high. Corpus file: `corpus-native-american.yaml`.

### Vedic Nakshatras (27+1 lunar mansions) — COMPLETE (2026-06-09)
**28 entries, 172 KB.** All 27 standard Nakshatras plus Abhijit (28th — marked `status_in_modern_tradition: historical_reference`). Full schema for all 28: Sanskrit names with variants, gana (divine/human/demon), nadi, hosting Rashi (2–3 Nakshatras per Rashi), primary star RA/Dec (J2000 for all yogatara), asterism schematic, deity, ruling planet (9-graha 3× repeating cycle), mythic narrative 2–3 paragraphs. Key bright stars captured at full precision: Aldebaran, Betelgeuse, Pollux, Regulus, Spica, Arcturus, Antares, Altair, Vega, Markab. Notable: **Krittika (#3)** was the ancient first Nakshatra (Pleiades — Galactic New Year anchor at ~2500 BCE); **Mula (#19)** points toward Galactic Center; **Revati (#27)** defines sidereal zero point via ζ Piscium; **Abhijit** includes Mahabharata time-dilation narrative and Vega-as-future-pole-star fact. Gana distribution: 10 Deva / 8 Manushya / 9 Rakshasa. Corpus file: `corpus-vedic-nakshatras.yaml`. Per-tradition summary: `per-tradition/vedic-nakshatras.md`.

### Arabic Manazil al-Qamar (28 lunar mansions) — COMPLETE (2026-06-09)
**28 entries.** All 28 Manzils with Arabic native script populated for each (`native_script` field: e.g., الشرطان). Academic anchor: Al-Sufi *Book of Fixed Stars* (964 CE). Calendar dates, Western constellation correspondence, star identifications sourced from Wikipedia canonical table cross-referenced with Al-Sufi. Western constellation correspondences documented (Manzil 1 = Aries, etc.). Key figures: Ash-Sharatan (#1, β+γ Arietis), Al-Thurayya (#3, Pleiades), Al-Dabarān (#4, Aldebaran), Al-Haqa (#5, λ Orionis), Al-Hana (#6, γ+ξ Geminorum), through Al-Risha (#28, β Andromedae). Cross-tradition overlaps documented: Arabic Manazil and Chinese Xiu share multiple asterisms (Pleiades, Scorpius, Orion region) — same stars, distinct cultural frames. Cultural sensitivity: none. Corpus file: `corpus-arabic-manazil.yaml`.

---

## Visual-representation completeness audit

*(populated at commission completion)*

---

## Substrate-tagging rep-audit

*(populated at commission completion)*

---

## Cross-tradition deduplication observations

*(populated at commission completion)*

---

## Architectural decision data point

**Target count for Matt's decision:** N ≥ ~400 → kit-binds-1:1 / N < ~400 → cluster-anchor

**Running count:** 0 (in progress)

---

## Recommended Phase 2 supplementary crawl scope

*(populated at commission completion)*
