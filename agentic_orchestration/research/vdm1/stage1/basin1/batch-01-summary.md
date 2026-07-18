# VDM-1 basin-1 batch-01 summary — kits 1-12 (poe2-acolyte-darkness through poe2-gemling-stacker)

**Batch:** 01 | **Game:** poe2 (all 12 kits) | **Date:** 2026-07-18
**Legolas instance:** batch-01

---

## Per-kit one-liners

| kit_id | identity | mechanics | era | negative_canon | flag |
|--------|----------|-----------|-----|----------------|------|
| poe2-acolyte-darkness | UNSUPPORTED | UNSUPPORTED | CONTRADICTED | n/a | ERA-CONTRADICTION; Into the Breach v0.3+ per poe2db; era floor 0.1 is invalid |
| poe2-archmage-totems | CONFIRMED | UNSUPPORTED | CONFIRMED | n/a | Mechanics UNSUPPORTED — Oracle+Archmage+Totem+Spark specific combo not attested in single source; component skills confirmed individually |
| poe2-blood-mage | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Clean |
| poe2-bonestorm | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Clean |
| poe2-chronomancer-01 | CONFIRMED | CONFIRMED | CONFIRMED | UNSUPPORTED | Negative canon claim (removed/reworked at launch) not supported — Time Freeze/Snap both real and active in current game; Chronomancer reworks noted at 0.5 but "launch removal" not confirmed |
| poe2-cof-comet | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Build nerfed in 0.1.0d (trigger energy nerf) — era 0.4 confirmed via CoC Comet Chronomancer guide |
| poe2-concoction | CONFIRMED | CONFIRMED | CONTRADICTED | UNSUPPORTED | ERA-CONTRADICTION: Poisonous Concoction guide active in 0.1.0e (Dec 2024); era floor stamp of 0.2-dawn is wrong — skill existed in 0.1; negative_canon claim is corpus triage metadata, not a testable game-state claim |
| poe2-demon-form | CONFIRMED | UNSUPPORTED | CONFIRMED | n/a | Mechanics UNSUPPORTED — Demon Form is element-agnostic; "fire spells in-form" is NOT confirmed as the exclusive or defining mechanic. Fetched builds include lightning (Spark) and cold variants. Fire nodes exist in ascendancy but form itself does not lock element. |
| poe2-erasure-edc-lich | UNSUPPORTED | UNSUPPORTED | CONFIRMED | n/a | "Erasure" skill/node — 404 on poe2db, absent from all maxroll/forum sources fetched. Essence Drain + Contagion confirmed real. Erasure claimed as core mechanic is SOURCE_NOT_FOUND. |
| poe2-galvanic-shards | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Clean; Armour Piercing Rounds confirmed real |
| poe2-gas-arrow-ignite | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Clean; note: archetype archived after 0.3 Ignite changes — era 0.3-edict stamp still valid (present but weakened) |
| poe2-gemling-stacker | CONFIRMED | CONFIRMED | CONFIRMED | n/a | Clean; HoWA confirmed real and central to build |

---

## Verdict histogram (advisory — file truth governs)

| verdict | count |
|---------|-------|
| CONFIRMED | 25 |
| UNSUPPORTED | 9 |
| CONTRADICTED | 2 |
| SOURCE_NOT_FOUND | 0 |

Total claim rows: 36 (identity×12 + mechanics×12 + era×12; negative_canon: 2 kits negative=true, 2 rows emitted)

---

## Contradictions (2 total)

1. **poe2-acolyte-darkness / era** — corpus stamps era floor 0.1. Into the Breach skill version history on poe2db starts at v0.3.0. Under uniform law (D-2a), era floor predating skill introduction = CONTRADICTED. Anchor: "version history starting from v0.3.0, with updates continuing through v0.5.0."

2. **poe2-concoction / era** — corpus stamps era floor 0.2-dawn. Maxroll Poisonous Concoction guide explicitly mentions "Adjusted build for patch 0.1.0e Hotfix 6" — the skill and build were active in 0.1. The 0.2-dawn floor is wrong direction (too late, not too early) — skill existed earlier than stamped, making the floor claim internally inconsistent per evidence of presence in 0.1.

---

## SOURCE_NOT_FOUND kits

None. All 12 kits returned relevant sources. However two kits have significant UNSUPPORTED claims requiring note:

- **poe2-erasure-edc-lich**: "Erasure" as a named skill/node is effectively SNF — 404 on poe2db, absent from all lich/witch sources. Essence Drain + Contagion confirmed; "Erasure" is the distinguishing claim and it is unverified.
- **poe2-acolyte-darkness**: Folk name "Darkness Acolyte" and alias "chaos-convert striker" are unattested. The class is "Acolyte of Chayula" in all sources. No guide uses "Darkness Acolyte" as a label.

---

## Dossier coverage

Families attempted per kit: 6 (skill_loop, skill_geometry, item_alterations, capstone_alterations, author_credit, variants)
Total rows: 72 (12 kits × 6 families)

| family | filled | abstained |
|--------|--------|-----------|
| skill_loop | 10 | 2 (acolyte-darkness, archmage-totems — mechanics UNSUPPORTED) |
| skill_geometry | 9 | 3 (acolyte-darkness, demon-form, galvanic-shards item_alt) |
| item_alterations | 3 | 9 (most kits — item specifics not in fetched sources) |
| capstone_alterations | 11 | 1 (acolyte-darkness) |
| author_credit | 5 | 7 |
| variants | 12 | 0 |

Coverage: 50/72 non-abstained = **69%**

Author credits recovered: wishdropper#0634 (demon-form spark, pathofexile.com), DrugaddictMenemist#6176 (blood-mage bonestorm, pathofexile.com), Void241 (gemling-stacker, maxroll.gg).

---

## Red flags

1. **"Erasure" skill does not exist in fetched sources.** The corpus kit `poe2-erasure-edc-lich` is named for and claims "Erasure" as a core mechanic (listed as core_skill in specs). poe2db returns 404. Lich ascendancy overview lists 8 nodes — none named Erasure. No maxroll or forum guide mentions Erasure. This is either a wrong skill name (possibly the corpus KB invented or mis-transcribed it) or it is a very obscure skill with no guide coverage. **Elrond should flag for re-key.**

2. **Into the Breach intro date.** The skill did not exist in 0.1 per poe2db version history (starts 0.3.0). The corpus era stamp 0.1 is invalid under uniform law. The Acolyte of Chayula ascendancy existed from launch, but the specific Into the Breach skill gem was added at 0.3.

3. **Demon Form element framing.** Corpus stamps element as "Fire" and core_skills as "fire spells in-form." Fetched sources show Demon Form is element-agnostic (used with Spark/lightning, cold, and fire builds equally). The fire framing is misleading — while fire nodes exist in Infernalist ascendancy, they are not the form's defining mechanic.

4. **poe2-concoction era floor direction error.** The era floor is 0.2-dawn but the skill demonstrably existed in 0.1 EA. The error is opposite-direction from the typical uniform law violation (stamp claims too-recent a start, not too-early). Likely a curation/harvest error rather than a uniform-law violation, but it should be corrected.

5. **poe2-archmage-totems Oracle+Archmage+Totem+Spark combo** — Oracle Spell Totem builds exist (Grim Pillars dominant), Oracle Spark builds exist, Archmage Spark exists (Stormweaver). The specific three-way combo (Oracle + Archmage + Spell Totem + Spark) was not confirmed in a single build guide. poe.ninja shows the individual components exist in Runes of Aldur but cannot confirm the exact combination without page content. Flagged as low-confidence (0.45) in dossier.

---

## Abstention reasons (dossier)

- **item_alterations abstained (9 kits):** Item-specific uniques not discussed in ascendancy overview pages fetched; would require dedicated build guides with gear sections — fetched pages were ascendancy overviews or leveling summaries only.
- **skill_geometry abstained (3 kits):** poe2-acolyte-darkness (mechanics too uncertain to characterize geometry), poe2-demon-form (form geometry varies by spell used), poe2-galvanic-shards skill_geometry rows filled but item_alterations abstained.
- **author_credit abstained (7 kits):** Maxroll guides do not expose individual author handles on ascendancy overview pages; forum thread authors recovered where threads fetched.
