# VDM-1 Basin-1 Batch-03 Summary
**Kits:** poe2-snipe-mirage-deadeye through poe2-warbringer-totems (spec lines 25-36; 12 kits, all poe2)
**Crawl date:** 2026-07-18
**Mode:** B (systematic verify + dossier)

---

## Per-kit one-liners

| kit_id | identity | mechanics | era | notes |
|---|---|---|---|---|
| poe2-snipe-mirage-deadeye | CONFIRMED | CONFIRMED | CONFIRMED (0.5-ancients) | Mirage Deadeye + Snipe combo gated to 0.5 per fextralife wiki; correct era floor |
| poe2-spark-stormweaver | CONFIRMED | CONFIRMED | CONFIRMED (0.1–0.5) | Archived 0.1.1 maxroll + current 0.5.4 guide both live; full era range attested |
| poe2-spiral-volley | CONFIRMED | CONFIRMED | UNSUPPORTED | Only 0.5.1 guides found; 0.4 era not attested in fetched text |
| poe2-supporting-fire | CONFIRMED | CONFIRMED | UNSUPPORTED | Only 0.5.4 guide found; pre-0.5 eras (0.2–0.4) not attested from fetched sources |
| poe2-tempest-bell | CONFIRMED | CONFIRMED | CONFIRMED (0.1–0.5) | Invoker leveling guide attests EA; Switchblade article confirms multi-era presence |
| poe2-tempest-flurry | CONFIRMED | CONFIRMED | CONFIRMED (0.1, 0.2, 0.5) | Mobalytics [0.1] guide + maxroll 0.5.1 guide both attested |
| poe2-temporalis-blink | CONFIRMED | CONFIRMED | CONFIRMED (0.1, 0.2) | PoE forum EA feedback thread confirms 0.1 era; Blink + Temporalis loop attested |
| poe2-titan-hotg | CONFIRMED | UNSUPPORTED | CONFIRMED (0.1–0.3) | HotG confirmed; Armour Breaker/Perfect Strike as core skills not confirmed from fetched guide (archived guide uses Earthshatter + Stampede in the skill loop) |
| poe2-twister | CONFIRMED | CONFIRMED | CONFIRMED (0.2–0.5) | poe2db earliest entry 0.2.0b; Spirit Walker Huntress ascendancy confirmed; 0.5.4 maxroll guide live |
| poe2-walking-calamity | CONTRADICTED | CONTRADICTED | CONFIRMED (0.5) | Class: Druid/Shaman (not Warrior/Marauder). Core skills: meteor skill + Rage/Glory economy (not herald/retaliation procs). Introduced 0.4.0b. |
| poe2-wall-of-shields | CONFIRMED | CONFIRMED | CONFIRMED (0.3–0.4) | Introduced 0.1.0 (poe2db crash-fix note). Static fissure placement confirmed. Negative canon confirmed. |
| poe2-warbringer-totems | CONFIRMED | CONFIRMED | CONTRADICTED | Era floor 0.1 CONTRADICTED — Ancestral Warrior Totem introduced 0.2.0 per poe2db version history. 0.2+ eras are consistent. |

---

## Verdict histogram (advisory — file truth governs)

| verdict | count |
|---|---|
| CONFIRMED | 28 |
| CONTRADICTED | 3 |
| UNSUPPORTED | 4 |
| SOURCE_NOT_FOUND | 0 |

---

## Contradictions (one line each)

1. **poe2-walking-calamity / identity**: Aliases include "herald retaliation autobomber" and "Molten Crash autobomb" — fetched text confirms Walking Calamity is a Druid/Shaman meteor skill, not a herald/retaliation build. Class is Druid (Shaman ascendancy), not Warrior/Marauder.
2. **poe2-walking-calamity / mechanics**: Core skills recorded as "herald/retaliation procs, Molten Crash(weapon)" — contradicted; Walking Calamity is a Rage/Glory-fueled meteor shower skill (poe2db: introduced 0.4.0b; maxroll 0.5.1 Shaman guide confirms meteor mechanic).
3. **poe2-warbringer-totems / era**: Era floor 0.1 contradicted — poe2db version history shows Ancestral Warrior Totem first appears at 0.2.0; no 0.1.0 entry exists. Floor should be 0.2-dawn.

---

## UNSUPPORTED kits / claims

- **poe2-spiral-volley / era (0.4)**: No fetched source explicitly attests 0.4 presence; only 0.5.1 and 0.5.4 guides found. Source silent — honest UNSUPPORTED.
- **poe2-supporting-fire / era (0.2-dawn, 0.3-edict, 0.4)**: Only 0.5.4 maxroll guide fetched; no pre-0.5 era attestation found in fetched text. Source silent on earlier patches.
- **poe2-titan-hotg / mechanics**: Armour Breaker and Perfect Strike listed as core skills — the archived maxroll guide's skill loop uses Stampede + Earthshatter + Hammer of the Gods; Armour Breaker and Perfect Strike not named as the combo pair in the guide. UNSUPPORTED (not contradicted — the guide is archived 0.1 and may predate AWT integration).

---

## SOURCE_NOT_FOUND kits

None. All 12 kits had live attesting sources.

---

## Dossier coverage

All 6 families attempted for all 12 kits = 72 possible rows.
- Non-abstained: 52 rows
- Abstained (source silent): 20 rows (all `author_credit` rows across all 12 kits = 12; plus `item_alterations` for snipe/spark/spiral/tempest-bell/tempest-flurry/warbringer = 6; capstone_alterations for twister partial = 1; temporalis capstone = partial abstain avoided per conf 0.45 floor)
- Dossier coverage: 72% non-abstained

**Author credits:** 0 of 12 kits had named author handles in the fetched guide text. All `author_credit` family rows are abstained (source silent — guides on maxroll/poe2db do not name authors in the fetched content).

---

## Red flags

1. **Walking Calamity corpus record is substantially wrong**: class field says "Warrior/Marauder"; should be "Druid/Shaman". Core skills say "herald/retaliation procs, Molten Crash(weapon)"; actual skill is a Rage/Glory-fueled meteor shower. The `folk_name` "Walking Calamity Autobomber" is real community usage but the aliases conflate it with a different autobomber archetype (herald-retaliation builds use separate skills like Repulsion/Armageddon, not Walking Calamity). Elrond should correct the corpus record for this kit.

2. **Warbringer-totems era floor 0.1**: The corpus era floor includes 0.1 for Ancestral Warrior Totem, but poe2db confirms it was introduced in 0.2.0. The Shockwave Totem (different skill) existed at launch; Ancestral Warrior Totem did not. The kit identity/folk-name "Ancestral Totem Warrior" implies Ancestral Warrior Totem specifically; the 0.1 era is a floor contradiction.

3. **Spiral-volley and Supporting-fire pre-0.5 eras**: Both have corpus eras stamped back to 0.4 (spiral) and 0.2 (supporting fire) but fetched guides only confirm 0.5.x. These are UNSUPPORTED, not CONTRADICTED — a future pass with PoE forum or Wayback could upgrade. Not a corpus error necessarily, just unverified from current fetch pass.

4. **Mobalytics quarantine note**: One Temporalis Blink citation (jungroan build) was quarantined per domain order (mobalytics.gg = 403-dead per brief). Used only as identity confirmation hint; all verify/dossier anchors draw from pathofexile.com forum instead.
