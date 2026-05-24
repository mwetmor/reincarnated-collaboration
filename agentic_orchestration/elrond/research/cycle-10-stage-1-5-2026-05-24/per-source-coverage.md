# Per-Source Coverage Histogram — Cycle 10 Stage 1.5 Post-Execution

**Date:** 2026-05-24
**Author:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-elrond-cycle-10-stage-1-5-per-source-structured-field-extractor.md`
**DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Schema added:** 8 columns on `weapon_knowledge_entries` (see per-source-schema-mapping.md §1)

---

## §1 Final coverage table (post-execution)

| Source | n | len% | wt% | mat% | bearer% | hist_use% | prov_avg |
|---|---:|---:|---:|---:|---:|---:|---:|
| royal_armouries | 38,127 | 0.0 | 0.0 | 0.0 | 0.3 | 0.0 | 0.947 |
| wikidata | 12,371 | 0.0 | 0.0 | 6.8 | 1.0 | 0.0 | 0.360 |
| wikipedia | 8,579 | 14.7 | 12.8 | 0.0 | 3.7 | 69.3 | 0.691 |
| met-museum | 7,559 | 43.6 | 70.6 | 98.9 | 4.9 | 100.0 | 0.827 |
| nick-aschenbach-dnd-data | 6,297 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.300 |
| wow-classic-items | 4,440 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.300 |
| odin-army-tradoc | 3,998 | 48.0 | 21.6 | 0.0 | 1.5² | 49.8 | 0.442 |
| bsdata-warhammer-aos | 2,185 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.300 |
| cataclysm-dda | 1,599 | 0.0 | 60.6 | 58.6 | 0.6 | 0.0 | 0.162 |
| osrsbox-db | 940 | 0.0 | 98.9 | 0.0 | 0.4 | 0.0 | 0.300 |
| pf2ools-quarantined | 688 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.300 |
| diablo2-d2data | 521 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.300 |
| path-of-exile-repoe | 494 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.300 |
| fextralife-elden-ring | 375 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.280 |
| bloqhead-demigods | 320 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.300 |
| elden-ring-erdb | 307 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.300 |
| fextralife-ds2 | 239 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.277 |
| fextralife-ds3 | 219 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.272 |
| gta-v-data | 183 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.300 |
| fextralife-ds1 | 133 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.283 |
| 5e-bits-5e-database-2024 | 110 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.300 |
| army-recognition | 62 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.284 |
| souls-api-quarantined | 56 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.300 |
| 5e-bits-5e-database | 37 | 0.0 | 0.0 | 0.0 | 0.0¹ | 0.0 | 0.300 |
| souls-api-thomaslincoln | 2 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.300 |

**TOTAL bearer-populated rows: 1,051 / 89,841 = 1.17%** (well above 500-row floor; 2.1x target)

¹ Fantasy/RPG sources: Pass A bearer matches suppressed at write-time per Discipline #25 (lineage `fantasy_generic` / `sci_fi_generic` flag). Pass B seed-list matches retained with rep-audit Mode-C/D flags where applicable. The suppressed pass-A count is captured in the match log (`pass_a_suppressed_fantasy`) — these rows have canonical_name patterns like "Greataxe of Agonizing Paralysis" / "Dagger of Bad Mojo" where the "of X" phrase is a fictional-attribute name, not a person attribution.

² odin-army-tradoc bearer matches are flagged `rep_audit_mode_c_naming_allusion_suspected` per `register_canonical='military_modern'`. Examples: Russian "Sadko Truck", "S-500 Prometheus" missile, Ukrainian "Baba Yagas (Vampire) UAV" — Mode C naming-allusion contamination per marginal-lineage-tagging-pattern record §1.1. Preserve source phrasing per Discipline #11; downstream curation interprets.

---

## §2 Match-pass breakdown

| Pass | Count | Description |
|---|---:|---|
| Pass A — canonical_name title-bearer | 438 | Met Museum primary (e.g., "Halberd of Archduke Ferdinand II of Austria") — regex extracts proper-noun phrase post-trigger |
| Pass B — seed-list match | 818 | Wikipedia + cross-source via gandalf 680-entry seed list × 1,071 patterns (incl. aliases) |
| Pass A suppressed (fantasy-lineage rep-audit) | 289 | Discipline #25 — fantasy/sci-fi lineage rows where Pass A regex matched but bearer is fictional-attribute, not person |
| Context-mismatch rejected (Pass B) | 630 | Discipline #25 low-priority / short-name entries failing tradition-context-token check |
| Context-weak flagged (Pass B) | 209 | Discipline #25 medium-priority entries with weak context; logged for spot-check |
| Mode-C naming-allusion flagged (Pass B) | ~72 | military_modern register + lineage-mismatch combination |

**Wall-time:** 345 sec for full bearer extraction (~89K rows × 1,071 patterns); foreground execution acceptable per Discipline #2.1 resource-bound projection.

---

## §3 Per-tradition match counts (Pass B; rep-audit-passed only)

| Tradition | Matches | Sketch D target | Status |
|---|---:|---|---|
| european_medieval | 259 | RICH (40.1% substrate) | aligned |
| greek | 168 | MODERATE | aligned |
| vedic_hindu | 120 | THIN | OVER-CATCHING via real-Indian-military Mode C (e.g., Agni missiles) — see §6 |
| norse | 119 | MODERATE | aligned |
| east_asian | 56 | RICH (23.0%) | under-target due to substrate Mode B/C/D in modern-military rows; substrate-honest |
| egyptian | 35 | THIN | aligned |
| celtic | 26 | MODERATE | aligned |
| slavic | 17 | THIN | aligned |
| mesopotamian | 15 | THIN | OVER-CATCHING via "Ishtar" / "Marduk" cross-cultural references; spot-check needed |
| mesoamerican | 3 | THIN | substrate-thin; Quetzalcoatl × 2 + Camazotz × 1 |

---

## §4 Sketch F 12-anchor presence audit

| Anchor | Match count | Substrate-honest finding |
|---|---:|---|
| Arthur | 24 | aligned; mostly Wikipedia Arthurian articles + Met Museum sword variants |
| Roland | 6 | aligned; Wikipedia Carolingian + 1 Met Museum |
| Thor | 40 | aligned; many Mode-C contamination flags (Russian missile codename collision per gandalf seed list disambig § 4.3) |
| Achilles | 10 | aligned; mythological articles + tendon medical references suppressed via context-check |
| Cú Chulainn | 6 + 1 (Cuchulainn alias) | aligned; clean Celtic mythological rows |
| Karna | 12 | aligned but partially Mode-C (real-Indian-military "Karna" namesakes); spot-check candidate |
| Baba Yaga | 12 | mixed: 6 Slavic-mythological + 6 modern-Ukrainian-drone-naming-allusion (correctly Mode-C flagged) |
| Cleopatra | 2 | substrate-thin; substrate-honest |
| Quetzalcoatl | 2 | substrate-thin; substrate-honest |
| Hattori Hanzō / Hanzo | 0 | substrate-honest **GAP** — "Hanzo" appears 2× substrate-wide but no context match |
| Lu Bu | 0 | substrate-honest **GAP** — entirely absent from substrate |
| Moctezuma | 0 | substrate-honest **GAP** — entirely absent from substrate |
| Gilgamesh | 0 | substrate-honest **GAP** — entirely absent from substrate |

**Sketch F gap finding:** 4 of 12 anchors (Hattori Hanzō, Lu Bu, Moctezuma, Gilgamesh) have ZERO substrate presence. This aligns with the marginal-lineage-tagging-pattern record's documentation of substrate-thin traditions (east_asian historical-real-persons + mesoamerican + sumerian). v1.1+ substrate-expansion-by-Mode-A-targeting per sub-carry 9.10-E would be the corrective path.

---

## §5 Floor-check compliance

**Floor target (per dispatch § 3):** ≥500 named-bearer matches.
**Actual:** 1,051 rows with `extracted_named_bearer IS NOT NULL`.
**Status:** PASS (2.1× floor).

---

## §6 Rep-audit Mode-A/B/C/D pattern observations (Discipline #25)

Carries through the marginal-lineage-tagging-pattern record's 4-mode taxonomy:

| Mode | Pattern | Example | Volume in this extraction |
|---|---|---|---|
| Mode A — true bearer attribution | "Halberd of Archduke X" | Met Museum entries | ~430 rows (most Pass A + Pass B Wikipedia mythological) |
| Mode B — geographic-of-origin masquerading as bearer | "Crossbow of Italy" | filtered via NON_BEARER_OF_TOKENS | ~0 (filter holds) |
| Mode C — naming-allusion in modern-military/fantasy items | "S-500 Prometheus", "Baba Yagas UAV", "Tiamat Mace" | flagged via register_canonical='military_modern' + lineage fantasy_generic | ~120 rows flagged or suppressed |
| Mode D — cross-tagged metadata error | rare — seed list disambig § 4 caught most | TBD via gandalf spot-check | TBD |

The empirical Mode-C contamination volume (~120) confirms the marginal-lineage-tagging-pattern record's hypothesis that geographic+military substrate sources pull naming-allusion content into seed-anchored lineages. This is preserved (Discipline #11) + flagged (Discipline #25) for downstream curation.

---

## §7 Cross-references

- Schema mapping: `per-source-schema-mapping.md`
- Named-bearer match log: `named-bearer-matches.json`
- Track M1 dividend memo: `track-m1-mining-dividend.md`
- Gandalf 30-row spot-check artifact: `spot-check-gandalf-request.md`
- Logs: `logs/02_extract_structured_fields.json`, `logs/03_extract_named_bearer.json`
