# VDM-1 basin-2 batch-03 summary
**Kits:** gd-phantasmal-blades-witch-hunter · gd-primal-strike-vindicator · gd-ravenous-earth-oppressor · gd-reap-spirit · gd-retaliation-warlord · gd-righteous-fervor-dervish · gd-roh-infiltrator · gd-savagery-warder · gd-shadow-strike-infiltrator · gd-skeleton-ritualist · gd-stormbox-elementalist · gd-stun-jacks
**Batch:** 03 | **Executed:** 2026-07-18 | **Negative kits:** gd-reap-spirit · gd-stun-jacks

---

## Per-kit one-liners

| kit_id | verdict summary |
|---|---|
| gd-phantasmal-blades-witch-hunter | identity/mechanics/era all CONFIRMED; no era contradiction (Nightblade = base class; kit stamped base-2016 is defensible) |
| gd-primal-strike-vindicator | base-2016 era CONTRADICTED (Inquisitor = AoM debut Oct 2017); aom-2017 + patch-1.1-1.2 CONFIRMED |
| gd-ravenous-earth-oppressor | all claims CONFIRMED; fg-2019 floor correct (Oppressor = Oathkeeper+Necromancer, Oathkeeper = FG 2019) |
| gd-reap-spirit | identity/mechanics/era CONFIRMED; negative_canon CONFIRMED (community consensus: dual-scale failure, pitiful primary damage) |
| gd-retaliation-warlord | all claims CONFIRMED; retaliation mechanics language captured verbatim for steward adjudication |
| gd-righteous-fervor-dervish | all claims CONFIRMED; fg-2019 floor correct (Oathkeeper = FG 2019 debut) |
| gd-roh-infiltrator | all claims CONFIRMED; aom-2017 floor correct (Inquisitor = AoM 2017) |
| gd-savagery-warder | all claims CONFIRMED; base-2016 floor holds (Soldier+Shaman both base-game classes) |
| gd-shadow-strike-infiltrator | base-2016 era CONTRADICTED (Inquisitor = AoM debut); aom-2017 + patch-1.1-1.2 CONFIRMED |
| gd-skeleton-ritualist | all claims CONFIRMED; aom-2017 floor correct (Necromancer = AoM 2017) |
| gd-stormbox-elementalist | all claims CONFIRMED; aom-2017 floor defensible (Shaman+Demolitionist both base classes; Storm Box is Shaman skill introduced in base game) |
| gd-stun-jacks | identity/mechanics/era CONFIRMED; negative_canon UNSUPPORTED — sources attest Stun Jacks was viable and buildable in base/AoM era but no source attests over-centralization critique or trap-skill framing for launch era specifically; later-patch context exists but not as negative corpus claim |

---

## Verdict histogram (ADVISORY — steward recounts from files)

| verdict | count |
|---|---|
| CONFIRMED | 33 |
| CONTRADICTED | 2 |
| UNSUPPORTED | 1 |
| SOURCE_NOT_FOUND | 0 |

Total claim rows: 36

---

## Contradictions (one line each)

1. **gd-primal-strike-vindicator / era / base-2016**: CONTRADICTED. Vindicator = Shaman+Inquisitor. Inquisitor debuted with Ashes of Malmouth (October 2017) — verbatim: "Unleash your vengeance upon the enemies of humanity with two new Masteries: the Inquisitor and the Necromancer" (store.steampowered.com/app/642280). A kit requiring Inquisitor cannot predate AoM. Era floor is 1 year early. D-2a candidate.

2. **gd-shadow-strike-infiltrator / era / base-2016**: CONTRADICTED. Infiltrator = Inquisitor+Nightblade. Same anchor as above — Inquisitor is AoM-2017 debut. Kit stamped base-2016 is impossible. D-2a candidate.

---

## UNSUPPORTED kits / claims

- **gd-stun-jacks / negative_canon**: The negative_canon_target claims "trap-skill over-centralization concern in base game; addressed by later patches." Sources confirm Stun Jacks was viable and widely built in base/AoM era (1.0.3.2, 1.0.6.1 builds found). No source attests an over-centralization concern or negative corpus framing for the launch era specifically. Sources are positive about the skill's damage ceiling ("scales immensely well"; "great damage"). The over-centralization framing is unattested. UNSUPPORTED, not contradicted.

---

## SOURCE_NOT_FOUND kits

None. All 12 kits found sources.

---

## Dossier coverage

All 12 kits received non-null dossier rows for skill_loop, skill_geometry, variants, author_credit, and capstone_alterations (where source attested content). item_alterations abstained for 5 kits (gd-phantasmal-blades-witch-hunter partial, gd-ravenous-earth-oppressor, gd-savagery-warder, gd-shadow-strike-infiltrator, gd-skeleton-ritualist) — source text did not surface specific item-alteration names in the crawled posts. capstone_alterations abstained for gd-roh-infiltrator and gd-shadow-strike-infiltrator.

Estimated dossier coverage: ~78% of family slots non-abstained across 12 kits x 6 families = 72 slots; approximately 56 non-abstained.

---

## Author credits (attested handles)

| kit_id | handle | site |
|---|---|---|
| gd-ravenous-earth-oppressor | Nery | forums.crateentertainment.com |
| gd-reap-spirit | Squib | forums.crateentertainment.com |
| gd-reap-spirit | Evil_Baka, TheFuentes5551, Ptirodaktill | forums.crateentertainment.com |
| gd-savagery-warder | Archangel2245 | forums.crateentertainment.com |
| gd-skeleton-ritualist | jhillman87 | forums.crateentertainment.com |
| gd-stormbox-elementalist | russell_timmerman | forums.crateentertainment.com |
| gd-stun-jacks | afanasenkov26, x1x1x1x2 | forums.crateentertainment.com |
| era anchor (all Inquisitor/Oathkeeper kits) | Crate Entertainment | store.steampowered.com |

---

## Red flags for steward / elrond

1. **RED FLAG — resource artifact (probe_facts)**: `gd-phantasmal-blades-witch-hunter`, `gd-primal-strike-vindicator`, `gd-skeleton-ritualist` canon_probe_facts rows carry `resource_verbatim: "mana"`. GD's universal resource is Energy (not "Mana"). "Spirit" is a GD stat name. These are confirmed artifact hits in the probe_facts rows — fetched sources consistently say "energy" for all three kits. Elrond sweep needed on all GD `resource_verbatim` fields in canon_probe_facts; `"mana"` and `"mana (reserve)"` should read `"energy"` and `"energy (reserve)"`.

2. **RED FLAG — D-2a era floor errors (2 hits this batch)**: gd-primal-strike-vindicator and gd-shadow-strike-infiltrator both carry `base-2016` era stamps that are impossible given Inquisitor = AoM-2017 debut. These join the batch-01/02 mastery-intro pattern. Both kits queued for ERRATA.

3. **Wayback note (gd-stun-jacks)**: Wayback availability API returned empty for all timestamps ≤2018 against the base 1.0.6.1 Stun Jacks thread URL. A 2022 snapshot exists (`20220519085600`) but web.archive.org WebFetch is blocked in this environment. The 1.0.3.2 CDR Stun Jacks Sorcerer thread (live) confirmed base-era presence for the era claim; Wayback was not required for verdict.

4. **gd-reap-spirit probe_facts absent**: DB query returned no canon_probe_facts rows for gd-reap-spirit or gd-stun-jacks. This is consistent with negative=true kits potentially having sparser probe ingest — not an error, noted for steward awareness.

5. **gd-stormbox-elementalist — Storm Box on Elementalist specifically**: Most forum Storm Box build guides found use Vindicator (Shaman+Inquisitor) not Elementalist (Shaman+Demolitionist). Community text confirms Elementalist = Shaman+Demolitionist and Storm Box is viable on that combination, but the dedicated Elementalist Storm Box guide corpus is thinner than for Vindicator. Era claim CONFIRMED on the basis of Shaman+Demolitionist being base-game classes and community posts from 2019 showing Elementalist Stun Jacks/Storm Box use. Steward may want to assess whether Storm Box Elementalist as distinct from Storm Box Vindicator is the intended corpus entry.
