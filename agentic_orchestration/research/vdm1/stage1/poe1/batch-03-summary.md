# VDM-1 Stage-1 PoE1 Batch-03 Summary
**Kits:** poe1-deaths-oath → poe1-flameblast (lines 25-36, 12 kits)
**Date:** 2026-07-18

## Per-kit one-liners

| kit_id | identity | mechanics | era | notes |
|---|---|---|---|---|
| poe1-deaths-oath | CONFIRMED | CONFIRMED | CONTRADICTED | Item existed 1.0.2 (Nov 2013); era floor 2.x is understated |
| poe1-detonate-dead | CONFIRMED | CONFIRMED | UNSUPPORTED | 1.x era plausible (0.9.1 crash fix references skill) but not directly attested from guide sources |
| poe1-discharge | CONFIRMED | CONFIRMED | UNSUPPORTED | 1.x/2.x era plausible; only 3.12/3.22 guides found live |
| poe1-divine-ire | CONFIRMED | CONFIRMED | CONFIRMED | Skill debuted 3.6.0; era stamps 3.0-3.6 / 3.7-3.13 both confirmed |
| poe1-ea-ballista | CONFIRMED | CONFIRMED | CONFIRMED | Modern skill (3.9.0 fuse rework); 3.14-3.19 + 3.20+ guides abundant |
| poe1-earthquake | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 2.2.0; 2.x/3.0-3.6 confirmed via poedb + guides |
| poe1-earthshatter | CONFIRMED | CONFIRMED | CONFIRMED | Debuted 3.11.0; era floor 3.7-3.13 consistent; 3.20+ also attested |
| poe1-edc | CONFIRMED | CONFIRMED | CONFIRMED | Essence Drain added 2.1.0; 3.x era guides across all stamped eras |
| poe1-elemental-hit | CONFIRMED | CONFIRMED | CONFIRMED | Random-element rework at 3.3.0 (within 3.0-3.6 stamp); official GGG announcement |
| poe1-facebreaker | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 0.9.11g; 1.x/2.x/3.x era all confirmed via poedb + forum guides |
| poe1-fire-trap | CONFIRMED | CONFIRMED | UNSUPPORTED | Oldest skill but 1.x/2.x era guides not found live; poedb shows pre-2.0 patch history |
| poe1-flameblast | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 1.0.4; 1.x/2.x/3.x era confirmed via poedb patch history |

## Verdict histogram

| Family | CONFIRMED | CONTRADICTED | UNSUPPORTED | SOURCE_NOT_FOUND |
|---|---|---|---|---|
| identity | 12 | 0 | 0 | 0 |
| mechanics | 12 | 0 | 0 | 0 |
| era | 8 | 1 | 3 | 0 |
| negative_canon | 0 (not applicable — all kits negative=false) | — | — | — |
| **TOTAL** | **32** | **1** | **3** | **0** |

## Contradictions

**poe1-deaths-oath / era:** Corpus stamps era floor as 2.x, but a pathofexile.com forum thread dated November 26, 2013 (v1.0.2) is titled "Death's Oath + 1.0.2 DoT mechanics?" confirming the item existed in 1.x. Era floor should be 1.x, not 2.x. The 2017 "Is the new Death's Oath armour bugged?" thread also confirms that a Death Aura rework occurred within 2.x, not that the item was introduced in 2.x.

## SOURCE_NOT_FOUND kits

None. All 12 kits found.

## UNSUPPORTED era claims (3 kits)

- **poe1-detonate-dead / era 1.x:** Skill referenced in 0.9.1 crash fix but no live build guide attesting 1.x era play found.
- **poe1-discharge / era 1.x, 2.x:** Discharge added 0.9.3 (poedb); CoC Discharge is 3.12+ era in live guides; earlier eras not directly attested via fetched sources.
- **poe1-fire-trap / era 1.x, 2.x:** Skill pre-dates 2.0 per poedb patch notes (version 2.0.0 crit change implies prior existence) but live build guides only span 3.15+ variants. Era stamps plausible but unattested from fetched sources.

## Dossier coverage

| kit_id | families covered (non-abstained) | abstained families |
|---|---|---|
| poe1-deaths-oath | skill_loop, skill_geometry, item_alterations, variants | capstone_alterations, author_credit |
| poe1-detonate-dead | skill_loop, skill_geometry, item_alterations, author_credit (TbXie), variants | capstone_alterations |
| poe1-discharge | skill_loop, skill_geometry, item_alterations, variants | capstone_alterations, author_credit |
| poe1-divine-ire | skill_loop, skill_geometry, author_credit (Bergerbrush), variants | item_alterations, capstone_alterations |
| poe1-ea-ballista | skill_loop, skill_geometry, author_credit (Palsteron), variants | item_alterations, capstone_alterations |
| poe1-earthquake | skill_loop, skill_geometry, variants | item_alterations, capstone_alterations, author_credit |
| poe1-earthshatter | skill_loop, skill_geometry, item_alterations (low-conf alias note), variants | capstone_alterations, author_credit |
| poe1-edc | skill_loop, skill_geometry, author_credit (TbXie), variants | item_alterations, capstone_alterations |
| poe1-elemental-hit | skill_loop, skill_geometry, item_alterations, variants | capstone_alterations, author_credit |
| poe1-facebreaker | skill_loop, skill_geometry, item_alterations, author_credit (KorgothBG), variants | capstone_alterations |
| poe1-fire-trap | skill_loop, skill_geometry, variants | item_alterations, capstone_alterations, author_credit |
| poe1-flameblast | skill_loop, skill_geometry, variants | item_alterations, capstone_alterations, author_credit |

**Overall dossier coverage:** 47 non-abstained rows / 72 total (6 families x 12 kits) = **65%**. capstone_alterations abstained for all 12 kits (source-silent across all fetches). Author credits found for 4 kits: TbXie (detonate-dead, edc), Bergerbrush (divine-ire), Palsteron (ea-ballista), KorgothBG (facebreaker).

## Author credits found

| kit_id | handle | site |
|---|---|---|
| poe1-detonate-dead | TbXie | poe-vault.com |
| poe1-divine-ire | Bergerbrush | pathofexile.com/forum |
| poe1-ea-ballista | Palsteron | maxroll.gg |
| poe1-edc | TbXie | poe-vault.com |
| poe1-facebreaker | KorgothBG#4084 | pathofexile.com/forum |

## Red flags

1. **poe1-deaths-oath era floor understated (CONTRADICTED):** The corpus era stamp starts at 2.x but the item clearly existed in 1.x based on a November 2013 forum thread (v1.0.2). Elrond should review the era field for this kit and consider amending to include 1.x.

2. **poe1-earthshatter alias "Foulborn Ghostwrithe zerker(3.28)":** No item named "Foulborn Ghostwrithe" was found in any source. This may be a phantom alias or an incorrectly remembered item name. The Earthshatter Berserker kit itself is well-confirmed; the alias string is the anomaly. Low-confidence dossier note recorded.

3. **capstone_alterations universally abstained:** No fetched source described capstone gem alterations (e.g., Vaal versions, 20/20 gem quality milestones) in a structured way for any kit. This family appears to require a more targeted poedb gem-level crawl. Not a crawl failure — source-silent.

4. **poewiki.net 403 / fandom paywalled confirmed:** Both fired as expected per template. poedb.tw served most skill data adequately (5/6 fetches succeeded; Deaths Oath 404'd).

0 kits SOURCE_NOT_FOUND. Batch complete.
