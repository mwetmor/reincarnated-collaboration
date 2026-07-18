# VDM-1 Basin-2 Batch-01 Summary
**Batch:** 01 | **Kits:** 1-12 (all Grim Dawn) | **Date:** 2026-07-18

## Per-kit one-liners

| kit_id | verdict summary |
|---|---|
| gd-aar-spellbinder | Identity+Mechanics CONFIRMED; Era CONTRADICTED — `base-2016` stamp invalid (Necromancer/Spellbinder is AoM-only) |
| gd-aegis-paladin | All families CONFIRMED — Paladin=Oathkeeper+Inquisitor, shield ricochet confirmed, fg-2019 era floor correct |
| gd-belgothian-blademaster | Identity+Mechanics+Era all CONFIRMED; resource probe field `spirit/focus` in DB is wrong (GD uses Energy) — noted in contradictions |
| gd-berserker-wereforms | Era=`foa-pending` CONFIRMED (FoA ships July 23 2026; not yet shipped at crawl date); identity+mechanics UNSUPPORTED (pre-release content only) |
| gd-blade-arc-warder | Identity+Mechanics+Era CONFIRMED; Warder=Soldier+Shaman, Blade Arc is Soldier base-game skill, bleed arc confirmed |
| gd-blade-trap | Identity+Mechanics CONFIRMED; negative_canon CONFIRMED (extensively criticized in 2017 community text); Era CONTRADICTED — DB era spans fg-2019/patch-1.1-1.2 but negative_canon_target explicitly says base-era only |
| gd-blight-fiend-ritualist | Identity+Mechanics+Era CONFIRMED; Necromancer is AoM debut (aom-2017 floor confirmed); Blight Fiend explosive-on-death confirmed |
| gd-bloody-pox-conjurer | Identity+Mechanics+Era CONFIRMED; Occultist is base-game mastery, Bloody Pox spreading plague confirmed |
| gd-bwc-demolitionist | Identity+Mechanics+Era CONFIRMED; August 2016 forum thread directly attests base-2016 presence |
| gd-cadence-witchblade | Identity+Mechanics+Era CONFIRMED; July 2016 post (patch 1.0.0.4) directly attests base-2016 presence |
| gd-callidors-tempest-templar | Identity+Mechanics CONFIRMED; Era CONTRADICTED — `base-2016` stamp invalid (Oathkeeper/Templar is FG-only) |
| gd-canister-saboteur | Identity+Mechanics+Era CONFIRMED; base-game 1.0.0.9 thread directly attests Canister Bomb+Saboteur in base era |

## Verdict histogram (ADVISORY — steward recounts files)

| verdict | count |
|---|---|
| CONFIRMED | 26 |
| CONTRADICTED | 4 |
| UNSUPPORTED | 2 |
| SOURCE_NOT_FOUND | 0 |

## Contradictions (one line each)

1. **gd-aar-spellbinder / era**: `base-2016` stamp CONTRADICTED — Spellbinder requires Necromancer mastery which debuted with AoM expansion (Oct 2017); era floor should be `aom-2017` not `base-2016`. Source: forums.crateentertainment.com/t/1-1-9-3-beginners-albrechts-aether-ray-spellbinder/112241

2. **gd-blade-trap / era**: DB era field extends to `fg-2019` and `patch-1.1-1.2` but the negative_canon_target explicitly states "base-era kit only, mechanism later reworked" — the extended era range contradicts the negative-kit framing. The spec also lists only `base-2016;aom-2017`. Era field in DB is wider than the negative canonical claim supports.

3. **gd-callidors-tempest-templar / era**: `base-2016` stamp CONTRADICTED — Templar requires Oathkeeper mastery which debuted with Forgotten Gods expansion (2019); a Templar (Arcanist+Oathkeeper) kit cannot exist in base-2016 era. Era floor should be `fg-2019`. Source: forums.crateentertainment.com/t/forgotten-gods-what-we-know-about-the-new-mastery/46822

4. **gd-belgothian-blademaster / probe_facts resource field**: The `canon_probe_facts` row records `resource_verbatim: "spirit/focus"` — Grim Dawn uses "Energy" as the resource system universally; "spirit/focus" is not a GD mechanic. This is a probe-facts inaccuracy (not a canon_corpus era/mechanics field), noted for steward review. Source: Energy regen discussions across multiple forum threads confirm "energy" is the GD resource.

## SOURCE_NOT_FOUND kits

None.

## UNSUPPORTED kits (source silent — honest)

- **gd-berserker-wereforms** (identity, mechanics, all dossier families except era): FoA not yet shipped as of 2026-07-18 (releases July 23). Pre-release marketing copy on grimdawn.com mentions "shapeshift into ferocious beastlike forms" and "bitter unforgiving winds of Asterkarn" (cold theme implied) but no specific skill names or verified mechanics. Full dossier abstained — no fetchable post-release community text exists yet.

## Dossier coverage

- 6 dossier families per kit × 12 kits = 72 rows total
- gd-berserker-wereforms: 6 abstentions (pre-release content only)
- Other 11 kits: `item_alterations` abstained on 8 kits (source silent on specific item interactions); `capstone_alterations` abstained on 9 kits (not extracted in available sources)
- Non-abstained families: skill_loop (11), skill_geometry (11), author_credit (11), variants (11), item_alterations (3/11), capstone_alterations (2/11)
- Estimated dossier coverage: ~57% of non-berserker rows have payload (abstentions are honest, not failures)

## Author credits extracted

| kit_id | handle | site |
|---|---|---|
| gd-aar-spellbinder | Nery | forums.crateentertainment.com |
| gd-aegis-paladin | Ulvar1 | forums.crateentertainment.com |
| gd-belgothian-blademaster | lMarcusl | forums.crateentertainment.com |
| gd-berserker-wereforms | — | — |
| gd-blade-arc-warder | Allan_Ashcroft, The_Coyote | forums.crateentertainment.com |
| gd-blade-trap | — (community discussion threads) | forums.crateentertainment.com |
| gd-blight-fiend-ritualist | Duskdeep86 | forums.crateentertainment.com |
| gd-bloody-pox-conjurer | MergosWetNurse | forums.crateentertainment.com |
| gd-bwc-demolitionist | Norzan, TomoDaK, sfbistimg, Dioarchet | forums.crateentertainment.com |
| gd-cadence-witchblade | jajaja | forums.crateentertainment.com |
| gd-callidors-tempest-templar | WyreZ | forums.crateentertainment.com |
| gd-canister-saboteur | chillstepbbc, Torzini | forums.crateentertainment.com |

## Red flags

1. **D-2a mastery intro failures (2 kits)**: gd-aar-spellbinder and gd-callidors-tempest-templar both carry `base-2016` era stamps requiring mastery-only-available-in-expansions. Spellbinder needs AoM (Necromancer); Templar needs FG (Oathkeeper). Both are straightforward era-floor raises: aom-2017 and fg-2019 respectively. Elrond ERRATA queue.

2. **gd-blade-trap era ambiguity**: The negative-kit era contract ("base-era only, mechanism later reworked") conflicts with the DB's 4-era span. Steward to determine whether the DB era field should be trimmed to base-2016/aom-2017 to match the negative framing, or whether the negative_canon_target text needs revision.

3. **gd-berserker-wereforms — BACKFILL-1 pending**: FoA ships July 23 (5 days from crawl). All dossier and identity/mechanics families abstained. Steward should trigger a re-crawl pass on this kit after release date + community guide lag (~2 weeks post-ship).

4. **gd-blade-trap wayback**: Wayback availability API returned snapshot at 2023-03-28 (closest to requested 2017-01-01). The forum threads for blade-trap discussion are directly accessible live (fetched successfully). No JS-shell issues encountered on forum threads. Negative canon confirmed from live fetched text; wayback was not needed to establish the verdict.

5. **probe_facts resource field for Belgothian**: `spirit/focus` is not a GD system. This is a probe-facts data quality issue, not a canon_corpus fields issue. Flagged for Elrond review.
