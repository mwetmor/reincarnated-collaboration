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
| Tibetan (12-animal) | in-progress | — | — | Agent still running |
| Persian/Zoroastrian (12) | ✅ COMPLETE | 12 | TBC | corpus-persian-zoroastrian.yaml written |
| Vedic Rashi (12) | in-progress | — | — | Agent still running |
| Vedic Nakshatras (27/28) | in-progress | — | — | Agent running |
| Egyptian decans (36) | in-progress | — | — | Agent running |
| Arabic Manazil al-Qamar (28) | in-progress | — | — | Agent running |
| Mayan Tzolkin (20 day-signs) | in-progress | — | — | Agent running |
| Aztec Tonalpohualli (20 day-signs) | in-progress | — | — | Agent running |
| Polynesian navigator traditions | in-progress | — | — | HIGH sensitivity; Agent running |
| Aboriginal Australian | in-progress | — | — | HIGH/RESTRICTED; Agent running |
| Inuit/Arctic Circumpolar | in-progress | — | — | HIGH sensitivity; Agent running |
| Andean (Quechua/Aymara) | in-progress | — | — | MEDIUM sensitivity; Agent running |
| West African (Dogon + broader) | in-progress | — | — | HIGH; Griaule flag; Agent running |
| Native American (multi-tribal) | in-progress | — | — | HIGH/RESTRICTED; per-tribe; Agent running |

**Running total: 60 entries confirmed** (12 Western + 12 Chinese + 12 Japanese + 12 Korean + 12 Vietnamese)
**Additional confirmed in-progress: 12 Persian + more from running agents**

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

### Persian/Zoroastrian — COMPLETE (2026-06-09)
**12 entries.** All 12 month-signs with named Yazata (divine beings): Farvardin/Fravashis, Ordibehesht/Asha Vahishta, Khordad/Haurvatat, Tir/Tishtrya (Sirius), Mordad/Ameretat, Shahrivar/Kshathra Vairya, Mehr/Mithra, Aban/Apas, Azar/Atar (sacred fire), Dey/Ahura Mazda, Bahman/Vohu Manah, Esfand/Spenta Armaiti. Faravahar symbol documented. Cultural sensitivity: none. Corpus file: `corpus-persian-zoroastrian.yaml` (65 KB).

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
