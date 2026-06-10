# Western Zodiac — Legolas Mode B Corpus Summary

**Crawl date:** 2026-06-09
**Entry count:** 12
**Visual coverage:** 100% entries with image_url populated; 100% with star_coordinates; 100% with asterism_schematic; 100% with cultural_iconography
**Cultural sensitivity:** none (all public domain / scholarly)
**Sources consulted:** Wikipedia (constellation + astrology pages per sign), IAU constellation data, Britannica, Ridpath "Star Tales" 2018

## Tradition overview

The Western zodiac is a 12-sign belt of constellations along the ecliptic (the Sun's apparent annual path through the sky), originating in Babylonian astronomy (~700 BCE) and codified by the Hellenistic Greek astronomer Ptolemy in the Almagest (~150 CE). Each sign carries astrological properties (element, modality, ruling planet) inherited from Babylonian and Greek cosmological frameworks. The zodiac underwent derivative transmission through Roman, Islamic Golden Age, and modern Western astrological traditions. All 12 signs are also recognized IAU constellations (see corpus-iau-constellations.yaml for IAU scientific context).

## Signs documented

| sign_id | Name | Symbol | Element | Modality | Ruling Planet | Visual Rep Type | Confidence |
|---|---|---|---|---|---|---|---|
| western-zodiac-001 | Aries | ♈ | Fire | Cardinal | Mars | image_url + stars + asterism + iconography | high |
| western-zodiac-002 | Taurus | ♉ | Earth | Fixed | Venus | image_url + stars + asterism + iconography | high |
| western-zodiac-003 | Gemini | ♊ | Air | Mutable | Mercury | image_url + stars + asterism + iconography | high |
| western-zodiac-004 | Cancer | ♋ | Water | Cardinal | Moon | image_url + stars + asterism + iconography | high |
| western-zodiac-005 | Leo | ♌ | Fire | Fixed | Sun | image_url + stars + asterism + iconography | high |
| western-zodiac-006 | Virgo | ♍ | Earth | Mutable | Mercury | image_url + stars + asterism + iconography | high |
| western-zodiac-007 | Libra | ♎ | Air | Cardinal | Venus | image_url + stars + asterism + iconography | high |
| western-zodiac-008 | Scorpio | ♏ | Water | Fixed | Mars/Pluto | image_url + stars + asterism + iconography | high |
| western-zodiac-009 | Sagittarius | ♐ | Fire | Mutable | Jupiter | image_url + stars + asterism + iconography | high |
| western-zodiac-010 | Capricorn | ♑ | Earth | Cardinal | Saturn | image_url + stars + asterism + iconography | high |
| western-zodiac-011 | Aquarius | ♒ | Air | Fixed | Saturn/Uranus | image_url + stars + asterism + iconography | high |
| western-zodiac-012 | Pisces | ♓ | Water | Mutable | Jupiter/Neptune | image_url + stars + asterism + iconography | high |

## Element/Modality matrix

| | Cardinal | Fixed | Mutable |
|---|---|---|---|
| Fire | Aries | Leo | Sagittarius |
| Earth | Capricorn | Taurus | Virgo |
| Air | Libra | Aquarius | Gemini |
| Water | Cancer | Scorpio | Pisces |

## Asterism highlights
- **Leo** — The Sickle (reversed question mark) is one of the most distinctive asterisms in the northern sky
- **Sagittarius** — The Teapot is a highly recognizable modern asterism within the zodiac; arrow points to galactic center
- **Taurus** — Contains two major star clusters: Hyades (bull's face V-shape) and Pleiades (Seven Sisters on shoulder)
- **Cancer** — Contains Praesepe / Beehive Cluster (M44); dimmest zodiac constellation
- **Virgo** — Largest zodiac constellation (1294 sq degrees); second largest overall; contains Virgo Galaxy Cluster

## Key Babylonian predecessors documented
All 12 signs have documented Babylonian predecessor figures from MUL.APIN tradition (cross-referenced in corpus-mesopotamian.yaml):
- Aries ← MULIKU (Hired Man) or MUL.LU.HUN.GA
- Taurus ← MUL.GUD.AN.NA (Bull of Heaven)
- Gemini ← MUL.MASH.TAB.BA.GAL.GAL (Great Twins)
- Cancer ← MUL.AL.LUL (Crayfish)
- Leo ← MUL.UR.GU.LA (Lion/Great Dog)
- Virgo ← MUL.ABSIN (Furrow)
- Libra ← MUL.ZI.BA.AN.NA (Scales)
- Scorpio ← MUL.GIR.TAB (Scorpion)
- Sagittarius ← MUL.PA.BIL.SAG (Pabilsag archer)
- Capricorn ← MUL.SUḪUR.MAS (Goat-Fish)
- Aquarius ← MUL.GU.LA (Great One)
- Pisces ← MUL.ZIB.ME (Tails)

## Primitive association hints summary
Suggested game design attribute mappings:
- **STR**: Aries (Ram initiator), Leo (Lion sovereign), Scorpio (intense sting)
- **CON**: Taurus (Bull endurance), Capricorn (Climber discipline)
- **INT**: Gemini (Twins communication), Virgo (Analytical harvest), Aquarius (Visionary air)
- **WIS**: Cancer (Lunar depth), Libra (Justice balance), Pisces (Dissolution transcendence)
- **DEX**: Sagittarius (Archer speed)

## Gaps + Phase 2 notes
- Full RA/Dec for some secondary stars not captured (Sheratan/Mesarthim exact RA; Elnath exact RA/Dec) — data available on individual Wikipedia star pages, can be filled in Phase 2 star data pass
- Alternative astrological house systems (Placidus, whole-sign, etc.) not documented — out of scope for substrate corpus
- Indian/Vedic zodiac (Jyotish, 27 Nakshatras) not included in this crawl — separate tradition, Phase 2 candidate
- Chinese lunar mansions (28 Xiu) not included — Phase 2 candidate
- Ophiuchus (the 13th ecliptic constellation, not a zodiac sign) documented in IAU corpus as iau-constellations-058
