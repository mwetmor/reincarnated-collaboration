# VDM-1 basin-5 batch-c07 summary — tli + tl1 (11 kits)

Crawl date: 2026-07-18. Legolas Mode B.

---

## Per-kit one-liners

| kit_id | identity | mechanics | era | notes |
|---|---|---|---|---|
| tl1-alchemist-summoner | CONFIRMED | CONFIRMED | CONFIRMED | Lightning via Ember Lightning attested |
| tl1-ricochet-vanquisher | CONFIRMED | CONFIRMED (partial: bounce geometry CONFIRMED; chain-hop vs bounce disambiguation UNSUPPORTED) | CONFIRMED | Physical/neutral — no element attested |
| tli-rehan-berserker | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Physical primary; fire-convert variant attested |
| tli-gemma-frost-caster | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Cold attested; dual-element (Ice-Fire Fusion) variant noted |
| tli-iris2-thunder-magus | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Lightning attested via Thunder Magus |
| tli-youga-spirit-magus | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Lightning attested via Thunder Magus variant |
| tli-carino2-lethal-flash | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Physical — no elemental type inherent to trait; element-silent |
| tli-erika3-vendetta | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Cold attested (late-game Frostbite endgame) |
| tli-moto-bots | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Physical-to-Erosion convert; no engine family — element-silent |
| tli-rosa-unsullied | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Corpus elem_raw=holy NOT attested by fetched text; sources describe cold/lightning/fire via Mercury Baptism tracking — see RED FLAG |
| tli-sage-elixir | CONFIRMED | CONFIRMED | UNSUPPORTED (era-U wall) | Tri-elemental: Cold + Fire + Lightning all attested |

---

## Verdict histogram (ADVISORY — steward recounts from file)

- CONFIRMED: ~18
- UNSUPPORTED: ~11 (all era claims for tli = era-U wall; tl1-ricochet chain-hop disambiguation)
- CONTRADICTED: 0
- SOURCE_NOT_FOUND: 0

---

## Contradictions

NONE. Zero contradictions across all 11 kits.

---

## SOURCE_NOT_FOUND kits

NONE. All 11 kits found via fallback sources (tlidb.com, vortexgaming, mmopixel, iggm, earlyguides, maxroll, alteredgamer, slashnblast). fandom.com 402 confirmed for both torchlight-infinite.fandom AND torchlight.fandom — fallbacks used throughout.

---

## Dossier coverage

11 kits × 6 families = 66 rows total.
- author_credit: 11 × abstained (no bylined authors recoverable from fetched pages)
- item_alterations: tl1-alchemist-summoner + tl1-ricochet-vanquisher abstained (old game, no gem/rune system; source silent)
- All other families: populated

Non-abstained rows: 66 − 11 (author_credit) − 2 (item_alterations tl1) = 53 populated
Abstained rows: 13
Coverage %: 53/66 = ~80%

---

## Element attestation summary (per-kit)

| kit_id | elem_raw in corpus | attested element | anchor |
|---|---|---|---|
| tl1-alchemist-summoner | lightning | LIGHTNING attested | "Ember Lightning casts a lightning bolt at foes, doing electric damage" |
| tl1-ricochet-vanquisher | physical | NONE attested — physical/neutral; element-silent | n/a |
| tli-rehan-berserker | physical | FIRE attested (variant only): "converting as much of its Damage from Physical to Fire" | Whirlwind fire-convert; base kit physical → element-silent base |
| tli-gemma-frost-caster | cold | COLD attested: "When using Cold Skills, Gemma will gain Cold Energy, which will increase Cold Damage" | Frostbitten Heart trait |
| tli-iris2-thunder-magus | lightning | LIGHTNING attested: "Thunder Magnus' ultimate skill damage scaling benefits from lightning damage increases. The build scales with … lightning damage." | vortexgaming.io SS11 guide |
| tli-youga-spirit-magus | lightning | LIGHTNING attested: "Summon Thunder Magus (Spell, Summon, Lightning)" | tlidb.com Spirit_Magus page |
| tli-carino2-lethal-flash | physical | NONE attested — trait text has no inherent damage type; projectile element depends on skill choice; element-silent | per law: name-only (Ice Shot/Electrifying Shot skill names) does not count |
| tli-erika3-vendetta | cold | COLD attested: "switch to the Frost Spike skill to enhance cold damage and utilize the 'Frostbite' status ailment" | iggm.com SS11 guide |
| tli-moto-bots | physical | NONE attested as engine family — Decayed Mind ring converts to Erosion (engine has no Erosion family); element-silent | per law: not a recognized engine family |
| tli-rosa-unsullied | holy | NONE attested as holy — see RED FLAG below | |
| tli-sage-elixir | unknown | COLD + FIRE + LIGHTNING all attested: "Chromatic Shot: Shoots 3 bolts that deal Cold, Fire or Lightning Damage"; "utilizing all of Chromatic Shot's tags (Cold, Lightning, Fire)" | tri-elemental; corpus elem_raw=unknown confirmed as blank/undefined |

---

## Red flags

1. **tli-rosa-unsullied elem_raw=holy NOT attested.** Corpus records elem_raw=holy for Rosa Unsullied Blade. Fetched text from tlidb.com/Unsullied_Blade and iggm.com build guides describes the kit as "Elemental Damage" tracker (Mercury Baptism records highest of Fire/Lightning/Cold). Cold is the dominant practical element in all guide recommendations. The word "holy" does not appear in any fetched source as a damage type descriptor for Rosa. This is an internal inconsistency: elem_raw field claims holy; fetched evidence supports cold-dominant elemental. NOT a verdict CONTRADICTED (verdict measures fetched text vs claim_text, not probe vs probe). Flagged for steward/Elrond review. Downstream mapper should treat Rosa as cold-primary (or element-flexible) rather than holy.

2. **tli-moto-bots Erosion damage.** Moto's primary endgame damage type is Erosion (via Decayed Mind ring conversion). Engine has no Erosion family. Mapper will need to park this. Physical is the base type before conversion; flagged as physical/neutral for engine purposes.

3. **tli-sage-elixir elem_raw=unknown confirmed.** Corpus correctly flags element as blank/undefined. Chromatic Shot is tri-elemental (Cold/Fire/Lightning simultaneously). Downstream mapping will need to decide how to handle tri-elemental kits — this is an edge case with no single family assignment.

4. **fandom.com total 402 blackout.** Both torchlight-infinite.fandom.com AND torchlight.fandom.com returned 402. All TLI and TL1 sourcing relied entirely on tlidb.com, vortexgaming.io, mmopixel.com, iggm.com, alteredgamer.com, earlyguides.com, maxroll.gg. Coverage is adequate but steward should note fandom is permanently unavailable.

5. **All tli era claims UNSUPPORTED (era-U wall).** Consistent with basin-5 hot-fact warning. Live-service gacha seasons means guides attest current patch only; no era floor can be confirmed. Honest UNSUPPORTED across all 9 tli kits.

---

## Author credits

All 11 kits: abstained. No bylined authors recoverable from fetched pages (community guides, wikis, build-site aggregators without named authors).

---

## Negative canon

NONE emitted. All 11 kits are negative=0.
