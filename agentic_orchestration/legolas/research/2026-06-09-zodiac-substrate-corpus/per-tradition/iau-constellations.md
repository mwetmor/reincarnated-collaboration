# IAU 88 Constellations — Legolas Mode B Corpus Summary

**Crawl date:** 2026-06-09
**Entry count:** 88 (batch A: 29, batch B: 29, batch C: 30)
**Visual coverage:** 100% image_url + star_coordinates; 82% asterism_schematic; 88% cultural_iconography
**Cultural sensitivity:** mostly none; Indus (medium — colonial-era depiction)
**Sources consulted:**
- https://en.wikipedia.org/wiki/[Constellation]_(constellation) — per entry
- IAU official constellation listing: https://www.iau.org/public/themes/constellations/
- https://en.wikipedia.org/wiki/IAU_designated_constellations_by_area
- Individual Wikipedia star pages (alpha star RA/Dec per entry)

---

## Tradition overview

The 88 IAU (International Astronomical Union) constellations are the modern scientific sky-partitioning system, standardized in 1930 by Eugène Delporte following the IAU boundary recommendation. The boundaries are defined in J1875.0 coordinates (Delporte's working epoch) and partition the entire celestial sphere with no gaps or overlaps. 48 constellations originate with Ptolemy's Almagest (~150 CE); the remaining 40 were added by European astronomers from the 1500s–1800s (primarily Lacaille, Hevelius, Keyser/de Houtman, Plancius) to cover the southern sky visible from their trading posts and expeditions.

The IAU constellations serve as the astronomical reference frame — not an astrological or cultural system, but the scientific coordinate partitioning. Corpus entries capture: IAU name, abbreviation, and genitive; alpha star (brightest star) with RA/Dec J2000 coordinates; area in square degrees; classification as Ptolemaic (ancient Greek origin) or Modern/IAU (post-Renaissance); brief mythic/cultural narrative; and game-design hooks from notable stellar phenomena.

---

## Classification breakdown

| Type | Count | Description |
|---|---|---|
| Classical Greco-Roman (Ptolemy 48) | 48 | Originally catalogued in Almagest ~150 CE; includes all 12 zodiacal constellations |
| Modern/IAU (post-Renaissance) | 40 | Added 1500s–1800s; mostly southern sky; named for instruments and animals |

## Notable astronomical features captured

| Feature | Constellation | Design hook |
|---|---|---|
| Nearest star system (α Centauri 4.24 ly) | Centaurus | "Gateway to the nearest world" mechanic |
| Nearest major galaxy (M31 Andromeda) | Andromeda | "Window to another galaxy" |
| Brightest star overall (Sirius α = -1.46) | Canis Major | Binary + white dwarf companion |
| Future north pole star (Vega ~13,727 CE) | Lyra | Precession / Age-of-Vega |
| Ancient pole star (Thuban ~2787 BCE) | Draco | Great Pyramid alignment |
| T CrB recurrent nova (upcoming) | Corona Borealis | Real-world timed event mechanic |
| SN 1006 brightest recorded supernova (mag -7.5) | Lupus | Supernovae flash mechanic |
| Cygnus X-1 first black hole candidate | Cygnus | Black hole portal mechanic |
| Ophiuchus "13th zodiac sign" | Ophiuchus | Hidden/unlockable class hook |
| M13 + 1974 Arecibo Message to stars | Hercules | "Message sent; awaiting reply" |
| PSR B1919+21 first pulsar ("LGM-1") | Vulpecula | Cosmic signal / alien contact hook |
| Only split IAU constellation | Serpens | Dual-form / split-consciousness design |
| Smallest IAU constellation (68 sq deg) | Crux | Southern Cross; flags of 5 nations |
| Largest IAU constellation (1303 sq deg) | Hydra | The great serpent; "the spreading water" |
| Mira variable star 11-month cycle | Cetus | Pulsing / revival mechanic |
| M87 galaxy / first black hole image | Virgo | "The eye of god" visual anchor |

## Zodiacal constellations in IAU corpus

The 12 Western zodiacal constellations appear in both `corpus-western-zodiac.yaml` (astrological schema) and in batch C of `corpus-iau-constellations-C.yaml` (scientific schema). Distinct entries with distinct sign_ids; different schema emphasis (astrological vs. astronomical). No deduplication needed — they serve different corpus purposes.

## Cultural sensitivity

| Entry | Flag | Notes |
|---|---|---|
| Indus | medium | Colonial-era European constellation depicting an indigenous figure in generically "exotic" costume (Keyser/de Houtman 1597); no specific people identified |
| Grus | low | Living tradition — crane symbolism in East Asian cultures |
| All others | none | Classical Greco-Roman mythology or instrument/animal naming; public domain |

## Gaps / Phase 2

1. **Asterism depth**: Many modern-IAU constellations (Antlia, Circinus, Norma, etc.) have no mythic narrative — iconography coverage is lower for instrument constellations. Phase 2 could add stellar physics highlights per entry to compensate.
2. **Double star / multiple star systems**: Several entries note double-star systems (Mizar, Castor, α Centauri) but detailed components not captured.
3. **Messier / NGC objects per constellation**: Game-design value in cataloguing notable nebulae/clusters per constellation — e.g., M42 Orion Nebula, M45 Pleiades, M1 Crab Nebula — could be a sub-table.
4. **Cultural name variants**: Many alpha stars have Arabic names (Aldebaran, Betelgeuse, Rigel, Vega, Altair) derived from medieval Islamic astronomy — these cross-reference with Arabic Manazil corpus.
