# VDM-1 Basin-3 Batch-03 Summary — kits 25–36 (all d2)
Date: 2026-07-18

## Per-kit one-liners

- **d2-golemancer** (neg): Identity CONFIRMED (narkive newsgroup), mechanics CONFIRMED (item-dep golem), lod era CONFIRMED, negative_canon CONFIRMED (community attests golems fall off past NM vs skeletons)
- **d2-grim-ward-barb** (neg): Identity UNSUPPORTED (no standalone build name found in fetched text; skill Grim Ward exists but "Grim Ward Barb" as build identity not attested), mechanics CONFIRMED (fear totem, corpse-placed), lod era UNSUPPORTED, negative_canon UNSUPPORTED (no standalone build to judge)
- **d2-hammerdin**: Identity CONFIRMED (Icy Veins, PureDiablo), mechanics CONFIRMED (BH/Conc/Holy Shield, magic damage), lod-1.10+ CONFIRMED (PureDiablo v1.10 guide), d2r CONFIRMED, rotw-s13+ UNSUPPORTED (churned post-cutoff token)
- **d2-horker**: Identity CONFIRMED (Yesgamers), mechanics CONFIRMED (WW kill + Find Item corpse loop), lod CONFIRMED, d2r CONFIRMED
- **d2-hydra-sorc**: Identity CONFIRMED (Maxroll S14), mechanics CONFIRMED (Hydra turret 3-headed pet at target), d2r-2.4+ CONFIRMED (patch explicitly named), rotw-s14 UNSUPPORTED (post-cutoff churned token)
- **d2-impale-zon**: Identity CONFIRMED (v1.09 Celine guide), mechanics CONFIRMED (single-target, durability drain, slow), classic UNSUPPORTED (skill is LoD era introduction — classic-era guide not confirmed), lod CONFIRMED, negative_canon CONFIRMED (single-target + durability trap attested)
- **d2-inferno-sorc**: Identity CONFIRMED (community usage as "challenge build"), mechanics CONFIRMED (channeled fire stream, 3.3-yard base range, caster rooted), classic UNSUPPORTED, lod CONFIRMED, negative_canon CONFIRMED (short range + fire immune wall + rooting = attested in fetched text)
- **d2-javazon**: Identity CONFIRMED (Icy Veins), mechanics CONFIRMED (LF/CS/Pierce), lod-1.09+ CONFIRMED (PureDiablo v1.10 guide), d2r CONFIRMED, rotw-s13+ UNSUPPORTED (post-cutoff)
- **d2-kicksin**: Identity CONFIRMED (Icy Veins title + Fandom), mechanics CONFIRMED (Dragon Talon/Fade/Crushing Blow), lod CONFIRMED (Fandom: "one of the most popular...in LoD"), d2r CONFIRMED
- **d2-leap-attack-barb** (neg): Identity CONFIRMED (community usage attested), mechanics CONFIRMED (pre-2.4: movement only; post-2.4: 4.6-yard landing AoE), classic UNSUPPORTED (no classic-specific attestation distinct from lod), lod CONFIRMED (pre-2.4 lod behavior described), negative_canon CONFIRMED (era-bounded: "only viable in Normal Difficulty" pre-2.4 = attested non-viable)
- **d2-lightning-sorc**: Identity CONFIRMED (Icy Veins), mechanics CONFIRMED (Lightning/Chain Lightning/Teleport), lod-infinity+ CONFIRMED (Infinity dependency attested), d2r CONFIRMED, rotw UNSUPPORTED (post-cutoff churned token)
- **d2-maul-bear**: Identity CONFIRMED (Maxroll — "Maul Druid"), mechanics CONFIRMED (Werebear/Maul stack/Shockwave), lod CONFIRMED (Druid is LoD-only class), d2r CONFIRMED

## Verdict histogram (ADVISORY — file truth governs)

| Verdict | Count |
|---|---|
| CONFIRMED | 34 |
| UNSUPPORTED | 14 |
| CONTRADICTED | 0 |
| SOURCE_NOT_FOUND | 0 |

**0 CONTRADICTED verdicts across the batch.** This is a pre-cutoff-stable d2 lod/d2r slice — low contradiction rate is expected per the template law. Stating this LOUDLY as required: all 34 CONFIRMEDs derive from clearly lod-era or D2R guide content; the 0-contradiction result reflects source quality and era stability, not shallow crawl.

## Contradictions

None. 0 contradictions across batch-03.

## SNF kits

None. SOURCE_NOT_FOUND = 0. All 12 kits found usable sources.

## Unsupported claims (notable)

- **d2-grim-ward-barb**: identity, era, and negative_canon ALL UNSUPPORTED — "Grim Ward Barbarian" as a standalone named community build is not attested in any fetched source. The Grim Ward skill exists; the skill is confirmed functional as described; but no guide/forum/wiki presents a distinct "Grim Ward Barb" build archetype. This is a red flag — see below.
- **rotw-s13+/rotw-s14/rotw** era tokens across hammerdin/javazon/hydra-sorc/lightning-sorc: all UNSUPPORTED (post-cutoff churned tokens — fetched sources do not reach these era labels)
- **classic** era tokens for impale-zon, inferno-sorc, leap-attack-barb: UNSUPPORTED (no dedicated classic-era source found that independently attests these builds pre-LoD; LoD-era sources found only)

## Dossier coverage

- 12 kits × 6 families = 72 family slots
- Abstained: d2-golemancer (capstone, author_credit), d2-grim-ward-barb (item_alterations, capstone, author_credit, variants), d2-hammerdin (author_credit), d2-horker (capstone, author_credit), d2-hydra-sorc (item_alterations, author_credit), d2-impale-zon (capstone), d2-inferno-sorc (item_alterations, author_credit), d2-javazon (author_credit), d2-kicksin (author_credit), d2-leap-attack-barb (item_alterations, author_credit), d2-lightning-sorc (author_credit), d2-maul-bear (item_alterations, author_credit)
- Abstained count: ~22 slots
- Non-abstained coverage: ~50/72 = ~69%
- author_credit abstained for 11/12 kits — fetched guides on Icy Veins, Maxroll, Yesgamers, diablo2.io do not display named author bylines on guide pages in the fetched text; only Celine (Impale guide, diablowiki.net) had explicit author attribution

## Author credits found

- **Celine** — "Guide: Amazon Subclasses v1.09" — diablo2.diablowiki.net — d2-impale-zon

## Red flags for steward/erratum queue

1. **d2-grim-ward-barb identity not attested**: No fetched source uses "Grim Ward Barbarian" or "Grim Ward Barb" as a standalone build name. The skill is real; a named kit is not confirmed. Recommend steward/elrond review whether this kit should be reclassified or the identity claim softened in the DB. The negative_canon_target ("functions as support gimmick not viable solo build identity") may be internally accurate but cannot be verdict-CONFIRMED because there is no standalone build to evaluate.

2. **d2-impale-zon classic era not confirmed**: The `classic` era token in the DB record for impale-zon is not independently confirmed in fetched sources. The Celine guide is v1.09 (LoD era). Impale skill existed in classic D2 (pre-LoD), but no fetched source explicitly attests the build in classic. Era token `classic` carries as UNSUPPORTED. Steward may backfill from Arreat Summit if Wayback access is restored.

3. **d2-inferno-sorc classic era not confirmed**: Same pattern as impale-zon. Inferno skill existed in classic, but no fetched source independently attests a classic-era build identity. `classic` token UNSUPPORTED.

4. **d2-leap-attack-barb classic era not confirmed**: No fetched source distinguishes classic vs lod behavior for Leap Attack specifically. Pre-2.4 references are lod-era framing.

5. **Wayback access blocked**: web.archive.org fetch returned "Claude Code is unable to fetch from web.archive.org" error. All 5 wayback-flagged kits (golemancer, grim-ward-barb, impale-zon, inferno-sorc, leap-attack-barb) were intended to have Arreat Summit snapshots as primary lod-era sources. These were not obtained. Classic-era claims rest on search-derived community sources only. Arreat Summit snapshots should be fetched in a follow-up pass if the block is lifted or an alternative fetch method is available.

6. **d2-hydra-sorc capstone era clarification**: Hydra was not a viable primary build skill in original LoD. The DB era floor is `d2r-2.4+` which is correct per fetched text ("new creation thanks to Patch 2.4"). The probe fact `resource_verbatim: cooldown` may be a D2R framing (original Hydra used mana not cooldown-gating; D2R 2.4 removed the casting delay making "cooldown" the functional limiter). Minor probe-fact drift — noted.

7. **d2-grim-ward-barb era lod UNSUPPORTED**: Grim Ward skill is LoD-era (confirmed by fextralife + search), but without a named standalone build, the era-of-the-BUILD claim is unverifiable. The skill is lod; a "build" around it is not attested.
