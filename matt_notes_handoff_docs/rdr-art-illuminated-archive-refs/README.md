# ART-1 "Illuminated Archive": pinned references

**Date:** 2026-09-26 · **For:** the painted-book A/B test (companion to `../rdr-art-illuminated-archive-brief.md`)
**Register:** medieval painted book (tempera and gold on vellum), merged with FFT-style watercolor. No oil paintings and no engravings are used as references: the generator copies the medium it is shown.

`ledger.jsonl` holds one row per image: source, object ID, image URL, licence, retrieval time, local file, pixel size and sha256. Each licence was checked at harvest: Getty pages show the Open Content Program marker, Met objects return `isPublicDomain: true` from the collection API, and Commons files carry `Public domain`.

## Picks (Matt, 2026-09-26)

| Role | Pick | Folder |
|---|---|---|
| **B character** | Getty Ms. 114, fol. 129v, the **right-hand knight** (blue tabard with gold crosses, closed armet). **Skirt removed:** the tabard ends at the hip, with plate legs as on the right-hand knight of fol. 123. **Weapon: poleaxe.** | `character/` |
| **A character** | The Keeper (existing, H1 register). The EoR Warlord is dropped. | n/a |
| **Cathedral style** | Belles Heures, Office of the Dead choir (Met 54.1.1a,b; images DP274537 and DP224804). Matt: the best register. | `cathedral-look/` |
| **Cathedral architecture** | Spinola Hours fol. 185 (Getty, Flemish, about 1510–20). **Architecture only:** the vaulted ceiling, the height and the details (tomb, tall windows, tower outside). Not a style source. | `cathedral-look-alt/` |
| **Cathedral building** | Antwerp, Cathedral of Our Lady: transept plus ambulatory with radiating chapels, laid over the Crucible arena footprint | `cathedral-plan/` |
| **Cliffside scenery** | *Très Riches Heures* calendar (Limbourg, the same hand as the choir) plus Belles Heures landscapes | `cliffside-horizon/` |
| Cliffside landmark: cathedral | TRH June, the Sainte-Chapelle | |
| Cliffside landmark: bridge | TRH July, the wooden trestle bridge at Poitiers | |
| Cliffside landmark: Keeper's domain | TRH September, Saumur (tower castle); Belles Heures DP274540 as a same-book alternative | |
| Grassland / valley / forest | TRH June (meadow), March (valley and roads), August (hills and river), May (forest); Belles Heures DP253017 (forest), DP274542 (meadow) | |

| **FFT style target (LOOK-ONLY)** | Yoshida FFT character page, supplied by Matt. **Copyrighted: never attach it to Astra or any generator.** Used only for human comparison and for the numbers in `metrics-2026-09-26.md`. | `look-only-never-attach/` |

Every ledger row carries `attach_to_generator`. Only rows marked `true` may be passed to a burst.

## Arena → cathedral mapping (Crucible geometry: `agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json`)

| Arena feature | Cathedral element |
|---|---|
| North corridor and red door (spawn) | Entry into the crossing through the choir screen |
| Central oval | The crossing under the lantern: lit from above, so it is the brightest and calmest floor |
| NW and NE lobes | The transept arms |
| Two long thin E and W walls | Choir stalls (as in the Belles Heures choir) |
| SW, S and SE lobes; the two small S islands | Ambulatory chapels; the altar and a tomb |
| Six green DoT zones | Rotted, miasma-soaked chapel floor. **They stay enterable: do not paint them as pits.** |

## Open points

- The Belles Heures choir leaf carries the corner number 221. The brief's "fol. 94v" was not located; the Met does not caption folios.
- There is no Greek temple in the painted-book vocabulary; a tower castle is the register-native landmark.
- *Très Riches Heures* images are Commons reproductions (Musée Condé, Chantilly). They are public domain as faithful copies of a public-domain work, but they are not an open-access release from the museum itself.
