# VDM-1 basin-2 batch-04 summary — kits 37-48 (GD 37-41 + LE 42-48)

**Batch:** b04 | **Crawl date:** 2026-07-18 | **Legolas instance:** batch-04

---

## Per-kit one-liners

| kit_id | result |
|--------|--------|
| gd-trozan-druid | Identity+mechanics CONFIRMED; patch-1.1-1.2 era CONFIRMED; aom-2017 + base-2016 UNSUPPORTED from fetched text; author mad_lee credited |
| gd-vires-might-shieldbreaker | All claims CONFIRMED; Oathkeeper=FG-2019 confirmed from forum pre-release thread; Volcanic Stride fire/burn verbatim extracted |
| gd-vitality-conjurer | Identity+mechanics CONFIRMED; patch-1.1-1.2 CONFIRMED; **aom-2017 floor CONTRADICTED** — fetched text: "Conjurer class available since base game" (Occ+Shaman are both base classes); fg-2019 era UNSUPPORTED |
| gd-wendigo-totem-ritualist | Identity+mechanics CONFIRMED; aom-2017 floor CONFIRMED (Necromancer=AoM journalism source); patch-1.1-1.2 CONFIRMED; Dark One's Gift 4-totem mechanics extracted |
| gd-word-of-pain-tactician | Identity+mechanics CONFIRMED; aom-2017 floor CONFIRMED (Inquisitor=AoM journalism source); patch-1.1-1.2 CONFIRMED; WoP brand geometry 1.5-screen verbatim extracted |
| le-bladestorm-bd | Identity+mechanics+1.4-omens era CONFIRMED via maxroll S4 guide; Bladestorm = placed spinning AoE generating Shurikens (not pure orbit); author LizardIRL |
| le-bomb-lance-falconer | All families SOURCE_NOT_FOUND / UNSUPPORTED — no guide found on maxroll or forum; post-cutoff 1.4-only kit |
| le-chthonic-fissure-warlock | Identity+mechanics CONFIRMED; 1.0-launch + 1.1 + 1.4 eras CONFIRMED; damage tags fire+necrotic (verbatim), NOT void (internal inconsistency with probe_facts "Void/Fire" label); author Terek (maxroll leveling guide) |
| le-detonating-arrow-mm | Identity+mechanics CONFIRMED via Blast Rain guide; 1.0 + 1.4 eras CONFIRMED; 1.2-woven UNSUPPORTED; no standalone DA Marksman guide on maxroll — DA appears as supporting mechanic in Blast Rain + Reign of Winter builds; author Volca |
| le-dive-bomb-falconer | Identity+mechanics CONFIRMED via dedicated maxroll guide; all 3 eras CONFIRMED (1.0 debut + planner attests 1.1 + S4); author LizardIRL |
| le-erasing-strike-vk | Identity+mechanics CONFIRMED; Void Well Mana mechanic verbatim extracted; 1.0 + 1.4 CONFIRMED; beta-0.8-0.9 UNSUPPORTED; author Volca; no "spirit/focus" language — Mana confirmed |
| le-explosive-trap-falconer | Identity+mechanics CONFIRMED via Explosive Ballista guide; 1.0-launch CONFIRMED; 1.1-harbingers UNSUPPORTED |

---

## Verdict histogram (advisory — steward recounts file)

| verdict | count |
|---------|-------|
| CONFIRMED | 36 |
| CONTRADICTED | 1 |
| UNSUPPORTED | 9 |
| SOURCE_NOT_FOUND | 3 |

---

## Contradictions (1)

1. **gd-vitality-conjurer / era / aom-2017 floor**: Fetched guide states "Conjurer (Shaman + Occultist) class is available since base game." Both Occultist and Shaman are base-game masteries. Era floor aom-2017 predates no class/skill introduction constraint — the issue is the floor is TOO LATE (should be base-2016 at minimum). D-2a floor-too-late class. Anchor: "Conjurer (Shaman + Occultist) class is available since base game." Source: forums.crateentertainment.com/t/1-1-6-2-beginners-vitality-caster-conjurer-guide.

---

## SOURCE_NOT_FOUND kits

- **le-bomb-lance-falconer**: No guide found on maxroll.gg/last-epoch, forum.lastepoch.com, or Steam guides. Post-cutoff 1.4-only skill. Bomb Lance is mentioned as a powerful S4 build variant in a SEO-content article (playerauctions.com — quarantine-adjacent; not used as verify/dossier source). All 6 dossier families abstained. Honest SNF.

---

## Dossier coverage

- 12 kits × 6 families = 72 family rows
- Abstained: 18 rows (le-bomb-lance-falconer = 6 full; le-bladestorm-bd capstone+variants = 2; le-chthonic-fissure-warlock item_alterations = 1; le-detonating-arrow-mm item_alterations = 1; le-dive-bomb-falconer item_alterations = 1; gd-wendigo-totem-ritualist capstone_alterations = 1; le-erasing-strike-vk none abstained; gd-trozan-druid all covered; etc.)
- Non-abstained rows: 54 / 72 = **75% coverage**

---

## Author credits captured

| handle | kit(s) | site |
|--------|--------|------|
| mad_lee | gd-trozan-druid | forums.crateentertainment.com |
| LizardIRL (Team Lead) | le-bladestorm-bd, le-dive-bomb-falconer | maxroll.gg |
| Volca | le-detonating-arrow-mm, le-erasing-strike-vk | maxroll.gg |
| Terek | le-chthonic-fissure-warlock | maxroll.gg |
| unknown | gd-vires-might-shieldbreaker, gd-vitality-conjurer, gd-wendigo-totem-ritualist, gd-word-of-pain-tactician, le-explosive-trap-falconer | forums.crateentertainment.com / maxroll.gg |

---

## Red flags for steward/elrond queue

1. **RED — gd-vitality-conjurer era floor ERRATA candidate**: KB stamps era floor as `aom-2017`; Conjurer=Occultist+Shaman, both base-game masteries confirmed by fetched source. Floor should be `base-2016`. ERRATA row owed.

2. **RED — le-chthonic-fissure-warlock elem_raw / probe_facts internal inconsistency**: Corpus `elem_raw=fire` is partially correct (fire tag confirmed). However `canon_probe_facts.label_verbatim` = "Void / Fire (FI suffix)" includes void, which is NOT attested by fetched text — forum source states "fire & necrotic tags by default." Void tag in probe_facts is unsupported and likely a generation artifact. Claim-vs-claim rule: not a verdict contradiction (probe_facts vs probe_facts), but flagged for elrond sweep. Elrond should correct probe_facts label to "fire / necrotic."

3. **AMBER — le-bomb-lance-falconer full SNF**: 1.4-omens-only kit with zero guide coverage on primary or secondary domains. Skill may be very new (Season 4 debut as new Falconer skill) or obscure. Recommend re-crawl after Season 4 guide ecosystem matures.

4. **AMBER — le-detonating-arrow-mm no standalone maxroll guide**: DA Marksman identity is attested (skill appears in multiple guides as supporting mechanic) but there is no dedicated DA Marksman build guide on maxroll. KB folk name "Detonating Arrow Marksman" is weakly confirmed as a build archetype — the dominant expression on maxroll is Blast Rain (which procs DA). If Elrond's curation requires a primary-skill guide anchor, this should be flagged.

5. **AMBER — gd-trozan-druid base-2016 + aom-2017 era UNSUPPORTED**: Oldest attested guide found is patch 1.1.4.0 era. The base-2016 and aom-2017 stamps are plausible (Druid=base classes, Trozan's Sky Shard is a base-game item set) but no fetched text confirms pre-patch-1.1 era presence. Not a contradiction — the absence of old guides is a corpus gap, not evidence of non-existence. Steward may want to attempt wayback/old-thread lookup if era floors matter for downstream logic.

6. **AMBER — gd-word-of-pain-tactician elem_raw=fire**: Fetched WoP Tactician builds show chaos, lightning, and pierce variants — not fire as primary. The KB `elem_raw=fire` is likely a generation artifact confusing WoP's burn/fire secondary with the build's actual damage profile. Not a verify-family claim (elem_raw is descriptive) but flagged for elrond sweep.

7. **AMBER — le-erasing-strike-vk beta-0.8-0.9 UNSUPPORTED**: Void Knight is a base Sentinel mastery (likely pre-1.0) but no fetched text confirms beta era presence of this specific Erasing Strike build. Plausible but unverified from fetched text.

---

## Resource artifact check

No `spirit` or `focus` resource language found in any of the 12 kits' probe_facts rows or fetched sources. All GD kits show "cooldown", "cooldown+leech", or "mana" (lowercase); all LE kits show "Mana." Clean pass.

---

## STEWARD AUDIT ADDENDUM (gandalf, 2026-07-18)

**Recount (D-2c):** file truth PRE-audit **42C / 1X / 9U / 0SNF** = **52 rows** (identity 12 · mechanics 12 · era 28), not the advisory's 49. Advisory drifted TWICE: CONFIRMED undercounted by 6, AND the 3 bomb-lance rows were WRITTEN as UNSUPPORTED while the summary (correctly) calls them "Honest SNF." Era family = 28 rows: **per-era-token verdicts on 10 kits** — b03's duplicate pattern now pervasive; steward-ACCEPTED run-wide (schema-legal; better resolution for the D-2a floor law).

**Steward ruling — bomb-lance-falconer ×3 RECLASSED UNSUPPORTED → SOURCE_NOT_FOUND (in-place edit):** no usable source found on ANY domain (playerauctions SEO = quarantine-class, never a source). Template vocab: SNF = no source after honest search; U = a fetched source SILENT on the claim. Files now match the crawler's own stated intent. POST-audit file truth: **42C / 1X / 6U / 3SNF = 52.** le-bomb-lance-falconer enters the **Unattested Register** + the re-crawl queue (S4 guide-lag; BACKFILL-class alongside gd-berserker-wereforms).

**Upheld:** vitality-conjurer era X — the run's first **floor-TOO-LATE** D-2a (aom-2017 floor vs "Conjurer (Shaman + Occultist) class is available since base game," verbatim-fetched ✓); restamp → base-2016. **D-2a harvest now 9 kits** (b01 ×2 · b02 ×4 · b03 ×2 · b04 ×1 — 8 floor-too-early + 1 floor-too-late). · Honest-U era tokens (trozan base+aom · vitality fg · detonating-arrow 1.2-woven · erasing-strike beta · explosive-trap 1.1-harbingers) — corpus gaps, not evidence-of-absence; no action; trozan wayback chase NOT fired (era floor rides the erratum/review-book only if downstream logic needs it).

**Identity ruling — detonating-arrow-mm C STANDS (contrast-case to stormbox):** its anchor attests the actual skill proccing on the actual class from fetched text ("proc Detonating Arrow with Explosive Trap... through the Arrow Traps Node," maxroll Blast Rain Marksman guide) — components attested together; weak only on folk-name-as-headline. WATCH annotation queued (identity-intent, alongside stormbox): dominant maxroll expression is Blast Rain; demote candidate iff elrond curation later requires primary-skill-anchored identities.

**Erratum queue additions:** chthonic-fissure probe label "Void / Fire" → fetched "fire & necrotic" (void unattested — generation artifact) · word-of-pain elem_raw=fire vs fetched chaos/lightning/pierce variants (descriptive-field artifact). ⚠ **The "clean pass" framing above is too narrow:** lowercase "mana" on GD kits IS the b03-broadened wrong-resource class (GD = Energy) — the gd-wide elrond sweep covers b04's GD rows too.

**Citations:** 23 / 0 quarantined / 0 banned-domain (crate 10 · maxroll 10 · massivelyop 2 [era-anchor class ✓] · LE forum 1 — official 5 / authored 8 / communal 10). **Dossier:** 72 rows exact · 12 abstained strictly-null ✓ (crawler prose "18 abstained / 75%" — advisory drift; files govern) · 60/72 = **83.3%** · conf floats ✓ · first maxroll-authored credit set of the basin (LizardIRL · Volca · Terek) + mad_lee (crate).
