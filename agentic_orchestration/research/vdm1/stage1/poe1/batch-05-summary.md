# VDM-1 Stage-1 PoE1 Batch-05 Summary
**Kits:** poe1-icicle-mines → poe1-pconc (spec-lines 49–60, 12 kits)
**Date:** 2026-07-18
**Legolas instance:** batch-05

---

## Per-kit one-liners

| kit_id | identity | mechanics | era | notes |
|---|---|---|---|---|
| poe1-icicle-mines | CONFIRMED | CONFIRMED | CONTRADICTED | Introduced 3.8.0; era floor 3.7 is pre-skill. Forum guide attests 3.9/3.10. |
| poe1-incinerate | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 0.10.2; 1.x/2.x era attested by version history. |
| poe1-kinetic-fusillade | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 3.27.0; 3.20+ era correct. |
| poe1-lacerate-glad | CONFIRMED | CONFIRMED | UNSUPPORTED | Blood and Sand confirmed 3.7; 3.0-3.6 pre-Blood-and-Sand era not directly attested in fetched sources. |
| poe1-lightning-arrow | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 0.9.7; 1.x attested by version history. |
| poe1-lightning-conduit | CONFIRMED | CONFIRMED | CONTRADICTED | Introduced 3.19.0; era floor 3.14 contaminated — skill did not exist for five patches. |
| poe1-lightning-strike | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 0.9.6; 1.x/3.20+ attested. |
| poe1-low-life-shavs | CONFIRMED | CONFIRMED | CONFIRMED | 2013 forum thread attests 1.x era. Pain Attunement + Shavs confirmed. |
| poe1-minion-pact-bv | UNSUPPORTED | CONFIRMED | CONFIRMED | No community folk-name source found; BV mechanics + Minion Pact mechanic confirmed from poedb. |
| poe1-mjolner | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 1.1.2; 2.x/3.0-3.6 eras attested via version history and forum. |
| poe1-molten-strike | CONFIRMED | CONFIRMED | CONFIRMED | Introduced 1.1.3; 3.0-3.6 era attested via 3.7 redesign note. |
| poe1-pconc | CONFIRMED | CONFIRMED | CONTRADICTED | Introduced 3.16.0 (Scourge); era floor 3.14 contaminated — skill did not exist for two patches. |

---

## Verdict histogram

| family | CONFIRMED | CONTRADICTED | UNSUPPORTED | SOURCE_NOT_FOUND |
|---|---|---|---|---|
| identity | 11 | 0 | 1 | 0 |
| mechanics | 12 | 0 | 0 | 0 |
| era | 8 | 3 | 1 | 0 |
| negative_canon | — | — | — | — (all kits negative=0; family suppressed per law) |
| **TOTAL** | **31** | **3** | **2** | **0** |

---

## Contradictions (3 total)

1. **poe1-icicle-mines / era** — Era floor `3.7` predates skill introduction (3.8.0). The Icicle Mine gem did not exist in 3.7. Correct floor is 3.8. Build is meta throughout 3.8-3.13 per forum evidence. Source: poedb.tw/us/Icicle_Mine ("introduced in patch 3.8.0, originally as 'Freeze Mine'").

2. **poe1-lightning-conduit / era** — Era floor `3.14` predates skill introduction by five patches. Lightning Conduit introduced 3.19.0 (Lake of Kalandra). The `3.14-3.19` bucket is correct as a range only if interpreted as "3.19 within that bucket." Stamped era implies presence from 3.14, which is false. Source: poe-vault.com/guides/lake-of-kalandra-league-new-skill-gems ("three new skill gems themed around lightning damage and shock" in 3.19).

3. **poe1-pconc / era** — Era floor `3.14` predates skill introduction by two patches. Poisonous Concoction introduced 3.16.0 (Scourge League). Correct floor is 3.16. Source: poedb.tw/us/Poisonous_Concoction ("introduced in patch 3.16.0. Added a new Dexterity Skill Gem").

---

## UNSUPPORTED

- **poe1-lacerate-glad / era** — 3.0-3.6 era unattested in fetched sources (only 3.25-3.28 guides surfaced). Blood and Sand confirmed as 3.7 addition, so the 3.0-3.6 era claim refers to pre-Blood-and-Sand Lacerate bleed builds. Sources are silent; not disproven, just unattested. Note abstained in-batch — Wayback search for 3.3/3.4 forum thread would resolve.
- **poe1-minion-pact-bv / identity** — No source found specifically using the folk-name "Minion Pact Blade Vortex" as established community usage; mechanics were confirmed from the component skills' poedb pages. This is a very recent kit (3.28 era) with thin guide coverage at time of crawl.

---

## SOURCE_NOT_FOUND kits
None. All 12 kits found across at least 2 sources.

---

## Dossier coverage

| family | rows (non-abstained) | abstained |
|---|---|---|
| skill_loop | 12 | 0 |
| skill_geometry | 12 | 0 |
| item_alterations | 3 | 9 |
| capstone_alterations | 4 | 8 |
| author_credit | 3 | 9 |
| variants | 6 | 6 |
| **TOTAL** | **40** | **32** |

Dossier non-abstained coverage: 40/72 = 56%. `item_alterations` and `capstone_alterations` are sparse because most kits are skill-centric (no load-bearing unique required). `author_credit` found for 3 of 12 kits: Memoria (icicle-mines), Funsy (mjolner socket order test). `variants` confirmed for 5 kits (Icicle Mine of Sabotage, KF of Detonation, LC of the Heavens, Lacerate of Haemorrhage, PConc of Bouncing).

---

## Author credits found
- **Memoria** — pathofexile.com/forum, "[3.10] Memoria's Icicle Mine Saboteur [SSF, League Starter]" (poe1-icicle-mines)
- **Funsy** — pathofexile.com/forum, empirical Mjölner socket-order mechanics test thread (2014) (poe1-mjolner)
- No named author found for: incinerate, kinetic-fusillade, lacerate-glad, lightning-arrow, lightning-conduit, lightning-strike, low-life-shavs, minion-pact-bv, molten-strike, pconc

---

## Era contamination addendum

Batch-05 finds 3 era contaminations, all in the `3.7-3.13` or `3.14-3.19` buckets — consistent with the batch-level warning. Running tally across known batches: crackling-lance (3.12), generals-cry (3.11), hexblast-mines (3.12), icicle-mines (3.8), lightning-conduit (3.19), pconc (3.16) — six contaminations, all from within wide era buckets. The wide-bucket era stamps treat the entire bucket as an availability window, but several gems were introduced partway through those buckets. Elrond's rekey pass should update `stabilization_patch` for these three kits.

---

## Red flags
- `poe1-lightning-conduit`: era contamination is the most severe in this batch — five full patches off (3.14 vs 3.19). This affects any corpus query filtering by era that includes "3.14" as a valid lightning-conduit era.
- `poe1-minion-pact-bv`: identity UNSUPPORTED + post-cutoff thin coverage. Specs noted as GAP-P1-01; treat as unverified folk name until a community guide surfaces with that exact phrasing.
- `poe1-kinetic-fusillade`: DB has `gx=null` and `era_year=2013` (wrong — 3.27 = 2024). The `era_year` field appears to be a bulk-fill artifact, not a real introduction year for this kit.
