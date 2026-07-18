# VDM-1 Stage-1 PoE1 Batch-06 Summary
Lines 61-72 of poe1-search-specs.jsonl — 12 kits

## Per-kit one-liners

| kit_id | folk_name | verdict summary |
|---|---|---|
| poe1-pizza-sticks | Pizza Sticks | identity CONFIRMED (forum thread); mechanics CONFIRMED (totem-channel outsourcing); era 3.0-3.6 CONFIRMED |
| poe1-poets-pen-vd | Poet's Pen Volatile Dead | identity CONFIRMED (odealo 3.1 guide); mechanics CONFIRMED (trigger chain); era 3.0-3.6 CONFIRMED; item alteration Poet's Pen captured |
| poe1-poison-bv | Poison Blade Vortex | identity CONFIRMED; mechanics CONFIRMED (10-blade orbit + Plague Bearer); all 4 era stamps CONFIRMED; Plague Bearer intro 3.8 noted |
| poe1-reaper | Summon Reaper | identity CONFIRMED; mechanics CONFIRMED; era 3.14-3.19 CONFIRMED; negative_canon CONFIRMED (author discontinued guide, power insufficient for new content) |
| poe1-righteous-fire | Righteous Fire | identity CONFIRMED; mechanics CONFIRMED (walk-forward aura + Fire Trap supplement); all 5 era stamps CONFIRMED; author credit Pohx captured |
| poe1-scourge-arrow | Scourge Arrow | identity CONFIRMED; mechanics CONFIRMED (channel-release spore pod fan); both era stamps CONFIRMED |
| poe1-seismic-trap | Seismic Trap | identity CONFIRMED; mechanics CONFIRMED (shockwave pulses + Exsanguinate pair); era 3.7-3.13 CONTRADICTED (see below); era 3.14-3.19 CONFIRMED |
| poe1-siege-ballista | Iron Commander Siege Ballista | identity CONFIRMED; mechanics CONFIRMED (DEX-stack totem army); both era stamps CONFIRMED; item alteration Iron Commander captured |
| poe1-skeleton-mages | Skeleton Mages | identity CONFIRMED; mechanics CONFIRMED (Dead Reckoning jewel conversion to mages); both era stamps CONFIRMED; item alteration Dead Reckoning captured |
| poe1-soulrend | Soulrend | identity CONFIRMED; mechanics CONFIRMED (homing chaos pierce + ES leech); era 3.0-3.6 CONFIRMED (intro patch); era 3.7-3.13 UNSUPPORTED |
| poe1-spark | Spark | identity CONFIRMED (all aliases); mechanics CONFIRMED (wandering bounce projectiles); all 4 era stamps CONFIRMED |
| poe1-spectral-helix | Spectral Helix | identity CONFIRMED; mechanics CONFIRMED (corkscrew spiral geometry); both era stamps CONFIRMED |

## Verdict histogram

| Verdict | Count |
|---|---|
| CONFIRMED | 55 |
| CONTRADICTED | 1 |
| UNSUPPORTED | 1 |
| SOURCE_NOT_FOUND | 0 |

Total verify rows: 57

## Contradictions

**poe1-seismic-trap — era 3.7-3.13 CONTRADICTED**
Seismic Trap introduced patch 3.3.0. The era floor "3.7-3.13" appears to be a contamination vector. All meta attestations found begin at 3.16 (Scourge league). poedb version history shows the skill received minor damage buffs in 3.6.0 and 3.13.0 but no guide evidence, community build write-up, or poe.ninja attestation confirms it was a meta build in the 3.7-3.13 window. The 3.14-3.19 era stamp is confirmed valid (3.16 Scourge was the confirmed meta spike). Recommended correction: remove 3.7-3.13, replace era floor with 3.14-3.19 only.

Note: poedb confirms a 3.13.0 buff (added damage effectiveness raised to 140%) which may have seeded the "3.7-3.13" stamp — the buff was real but no meta adoption evidence found in that window.

## UNSUPPORTED notes

**poe1-soulrend — era 3.7-3.13 UNSUPPORTED**
Soulrend was introduced 3.6.0 and would have been playable in 3.7-3.13, but no build guide, community write-up, or poe.ninja era attestation was found confirming it was a recognized meta or popular build in that bucket. Source silent on this era.

## SNF kits

None. All 12 kits had sufficient source presence.

## Dossier coverage

| family | non-abstained kits | abstained kits |
|---|---|---|
| skill_loop | 12/12 | 0 |
| skill_geometry | 12/12 | 0 |
| item_alterations | 4/12 (pizza-sticks, poets-pen-vd, siege-ballista, skeleton-mages) | 8 (source silent — no notable unique item alteration found) |
| capstone_alterations | 0/12 | 12 (source silent across all kits) |
| author_credit | 6/12 | 6 |
| variants | 12/12 | 0 |

Overall dossier coverage: 46/72 rows non-abstained = 64%. Abstentions are source-silent, not fabricated. capstone_alterations 0/12 — no source described capstone passive notables as build-defining alterations across this batch; this is expected for builds where the class node tree is generic.

## Author credits captured

| kit_id | handle | site |
|---|---|---|
| poe1-poison-bv | TbXie | poe-vault.com |
| poe1-righteous-fire | Pohx | poe-vault.com |
| poe1-scourge-arrow | TbXie | poe-vault.com |
| poe1-seismic-trap | TbXie | poe-vault.com |
| poe1-skeleton-mages | GhazzyTV | poe-vault.com |
| poe1-reaper | cheapbunny | pathofexile.com |

## Red flags / notes for Elrond

1. **poe1-seismic-trap era 3.7-3.13 CONTRADICTED** — DB era stamp needs correction. Skill introduced 3.3.0, meta confirmed 3.16+. The 3.13.0 damage buff may have seeded the stamp but no meta guide evidence exists for that window.

2. **poe1-soulrend era 3.7-3.13 UNSUPPORTED** — Not contradicted (skill existed from 3.6.0 so it was technically present), but no meta attestation found. Elrond may want to flag this as low-confidence or downgrade the era stamp.

3. **poe1-poets-pen-vd class field** — DB lists "Elementalist/Necromancer" but all primary source guides from 3.1 are Berserker, then Inquisitor Templar from 3.2. Elementalist/Necromancer not attested as primary classes for this build in sources consulted.

4. **Scourge Arrow era 3.0-3.6 narrow** — Scourge Arrow was introduced 3.4.0 so only 3.4 and 3.5 are covered within the 3.0-3.6 bucket. Stamp is technically correct but should be understood as 3.4-3.6 not full bucket.

5. **Plague Bearer introduction 3.8** — The poe1-poison-bv DB entry lists era starting at "2.x". The current core_skills includes Plague Bearer. The "2.x" era is valid for base poison BV (Blade Vortex 2.1.0, physical/ele poison variants existed pre-Plague Bearer), but the Plague Bearer-enabled variant is 3.8+ specifically. Elrond may want to split the mechanics note.

6. **Reddit blocked** — reddit.com/r/pathofexile returned 403 across all search attempts. All identity claims verified through pathofexile.com forum, poe-vault.com, maxroll.gg, odealo.com, poedb.tw, and buildofexile.com. Coverage considered adequate.

7. **Wayback.org blocked** — WebFetch could not fetch web.archive.org URLs directly. Wayback availability API was usable. Era verification for Seismic Trap 3.7-3.13 relied on poedb version history and presence/absence of indexed guides.
