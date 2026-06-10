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
| Western IAU constellations (88) | in-progress | — | — | Agent A running |
| Mesopotamian (MUL.APIN) | in-progress | — | — | Agent A running |
| Celtic tree zodiac (13) | in-progress | — | — | Agent A running |
| Norse/Germanic | in-progress | — | — | Agent A running |
| Chinese zodiac (12 animals) | ✅ COMPLETE | 12 | 100% image_url + iconography | YAML validated; 2 low-sensitivity flags |
| Chinese Xiu lunar mansions (28) | in-progress | — | — | Agent running |
| Japanese (Jūnishi) | ✅ COMPLETE | 12 | TBC | corpus-japanese-junishi.yaml written |
| Korean (Ddi) | ✅ COMPLETE | 12 | TBC | corpus-korean-ddi.yaml written |
| Vietnamese (12-animal) | ✅ COMPLETE | 12 | TBC | Cat-for-Rabbit documented |
| Tibetan (12-animal) | ✅ COMPLETE | 12 | TBC | Garuda/Nāga variant documented |
| Persian/Zoroastrian (12) | ✅ COMPLETE | 12 | image_url + iconography | Yazatas; Tishtrya=Sirius; Mithra distinguished from Roman Mithras |
| Vedic Rashi (12) | ✅ COMPLETE | 12 | image_url + stars + iconography | Sidereal vs tropical; Makara creature documented; Kalapurusha body-mapping |
| Vedic Nakshatras (27/28) | in-progress | 9/27 | full on 9 | Ashvini–Ashlesha done; agent still running |
| Egyptian decans (36) | in-progress | — | — | Agent running |
| Arabic Manazil al-Qamar (28) | in-progress | — | — | Agent running |
| Mayan Tzolkin (20 day-signs) | ✅ COMPLETE | 20 | image_url + iconography | Living ceremonial; medium sensitivity applied |
| Aztec Tonalpohualli (20 day-signs) | in-progress | — | — | Agent running |
| Polynesian navigator traditions | ✅ COMPLETE | 12 | image_url + stars + iconography | Hawaiian 7 + Maori 5; high sensitivity applied |
| Aboriginal Australian | ✅ COMPLETE | 5 | image_url + dark-cloud schematic | Kamilaroi + Boorong; Protocol C; restricted content excluded |
| Inuit/Arctic Circumpolar | ✅ COMPLETE | 4 | stars + iconography | Per-culture (Inuit/Sámi); high sensitivity applied |
| Andean (Quechua/Aymara) | in-progress | — | — | MEDIUM sensitivity; Agent running |
| West African (Dogon + broader) | in-progress | — | — | HIGH; Griaule flag; Agent running |
| Native American (multi-tribal) | in-progress | — | — | HIGH/RESTRICTED; per-tribe; Agent running |

**Running total: 146 entries confirmed**
**Projected final (all agents complete): 400–430 entries**

---

## Per-tradition completion notes

### Western zodiac — COMPLETE (2026-06-09)
**12 entries.** All 12 signs with full schema: element/modality/ruling planet, primary stars with RA/Dec (J2000), IAU SVG image URLs, asterism schematics, mythic narratives, Babylonian predecessor cross-references. Visual coverage 100% across all 4 sub-fields. YAML produces clean parse. Per-tradition file: `per-tradition/western-zodiac.md`. Image refs: `visual-assets/western-zodiac-image-refs.md`. Corpus file: `corpus-western-zodiac.yaml` (56 KB).

### Chinese zodiac (十二生肖) — COMPLETE (2026-06-09)
**12 entries.** All 12 animals with full schema: earthly branch, fixed element, yin/yang, 2-hour periods, compatible signs, Jade Emperor race narrative per animal, Wikipedia Commons image URLs (M.A. N.Isis Alexandre "Zodiaque" series, CC-BY-SA 3.0). Cultural sensitivity: 2 low flags (Snake, Pig — minor cultural associations), 10 none. Notable: Snake/低 sensitivity flag noted because some cultures have mixed symbolism; Pig/猪 similar. Corpus file: `corpus-chinese-zodiac.yaml` (59 KB). YAML validated cleanly.

### Japanese Jūnishi — COMPLETE (2026-06-09)
**12 entries.** Derivative from Chinese zodiac; distinct primary_culture = "Japanese." Key variant: 12th animal is Boar (Inoshishi/猪) not Pig — Japanese-specific. Corpus file: `corpus-japanese-junishi.yaml` (45 KB).

### Korean Ddi (띠) — COMPLETE (2026-06-09)
**12 entries.** Derivative from Chinese zodiac; distinct primary_culture = "Korean." Korean readings documented. Corpus file: `corpus-korean-ddi.yaml` (44 KB).

### Vietnamese zodiac — COMPLETE (2026-06-09)
**12 entries.** Derivative from Chinese zodiac; distinct primary_culture = "Vietnamese." Key variant: **Cat (Mèo) replaces Rabbit** at position 4 — documented with Vietnamese legend. Corpus file: `corpus-vietnamese-zodiac.yaml` (49 KB).

### Tibetan zodiac — COMPLETE (2026-06-09)
**12 entries.** Derivative from Chinese zodiac; distinct primary_culture = "Tibetan." Dragon entry documents Nāga/Garuda variant framing in Tibetan-Buddhist context. Corpus file: `corpus-tibetan-zodiac.yaml` (49 KB).

### Persian/Zoroastrian — COMPLETE (2026-06-09)
**12 entries.** All 12 month-signs with named Yazata (divine beings): Farvardin/Fravashis, Ordibehesht/Asha Vahishta, Khordad/Haurvatat, Tir/Tishtrya (Sirius — astronomically specific), Mordad/Ameretat, Shahrivar/Kshathra Vairya, Mehr/Mithra (Roman Mithraism tauroctony distinguished as Roman derivative, not Avestan), Aban/Apas, Azar/Atar (sacred fire), Dey/Ahura Mazda, Bahman/Vohu Manah, Esfand/Spenta Armaiti. Faravahar symbol documented. Cultural sensitivity: none. Corpus file: `corpus-persian-zoroastrian.yaml` (65 KB).

### Vedic Rashi — COMPLETE (2026-06-09)
**12 entries.** All 12 Rashi with Sanskrit names, Jyotish ruling planets, element (Agni/Prithvi/Vayu/Jala), quality (Chara/Sthira/Dwiswabhava), Kalapurusha body-part mapping (Mesha=head through Meena=feet). Key distinctions documented: (1) sidereal vs tropical zodiac (~23° ayanamsa offset); (2) Makara documented as mythical Makara sea-creature (NOT simply goat-fish); (3) planetary exaltations and debilities captured. Corpus file: `corpus-vedic-rashi.yaml` (71 KB).

### Vedic Nakshatras — IN PROGRESS (9/27 complete)
**9 entries confirmed** (Ashvini through Ashlesha). All first 9 with full schema: deity, gana (Deva/Manushya/Rakshasa), nadi, hosting Rashi, primary star RA/Dec, symbol, mythic narrative. Agent still running for entries 10–27 (Magha through Revati + optional Abhijit).

### Mayan Tzolkin — COMPLETE (2026-06-09)
**20 entries.** All 20 day-signs with Yucatec and K'iche' name variants, presiding deities, glyph image URLs (Dresden Codex / Wikipedia Commons), cultural iconography, mythic narratives. Aztec parallel noted in each entry. Cultural sensitivity: medium applied throughout. Corpus file: `corpus-mayan-tzolkin.yaml` (88 KB).

### Polynesian navigator traditions — COMPLETE (2026-06-09)
**12 entries** (7 Hawaiian + 5 Maori). Hawaiian: Hokule'a (Arcturus/zenith star), Makali'i (Pleiades/harvest), Hoku Pa'a (Polaris), Newe/Maui's Fishhook (Scorpius), A'a (Sirius), Na Hiku (Big Dipper), Ke Ali'i o Kona i Ka Lewa (Canopus). Maori: Matariki (Pleiades cluster with 7 named stars), Tautoru (Orion's Belt), Māhutonga (Southern Cross), Rehua, Māui's Fishhook. Cultural sensitivity: high applied; sourced from Bishop Museum + Te Papa + PVS + academic only. Star coordinates included where applicable. Corpus file: `corpus-polynesian.yaml` (88 KB).

### Aboriginal Australian — COMPLETE (2026-06-09)
**5 entries.** Kamilaroi Emu in the Sky (dark-cloud, Coalsack-to-Milky-Way-rift), Boorong tradition figures (Wotjobaluk people): Tchingal (Emu dark cloud), Warepil (Wedge-tailed Eagle/Altair), Marpeankurrk (Sugar Ant/Arcturus), and one additional Boorong figure. Protocol C applied; AIATSIS protocol followed; sacred-restricted content excluded. Cultural sensitivity: high. Corpus file: `corpus-aboriginal-australian.yaml` (43 KB).

### Inuit/Arctic Circumpolar — COMPLETE (2026-06-09)
**4 entries.** Per-culture: Inuit Tukturjuit (Caribou/Ursa Major), Inuit Aagjuuk (Altair+Tarazed — summer solstice marker), Inuit Sakiattiat (Pleiades), Sámi Sarva (Elk/Ursa Major). Anti-collapse discipline applied (Inuit ≠ Sámi ≠ Yupik). Cultural sensitivity: high. Corpus file: `corpus-inuit-arctic.yaml` (33 KB).

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
