# Cycle 10 Stage 2 — Thin-Tradition List (Sidecar B Substrate-Enrichment Scope)

**Date:** 2026-05-24
**Owner:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-cross-tab-thin-cell-surfacing.md`
**Companion:** `cross-tab.html` · `thin-cell-list.md` · `critical-fill-targets.md`
**Authority:** Sketch D § 4.3 substrate-enrichment fold into Sidecar B

---

## 0. TL;DR

Per Sketch D § 4.3, Sidecar B substrate-enrichment scope extends to THIN cultural-tradition tiers. This artifact enumerates per-tradition substrate share vs Sketch D target, surfaces top-priority Sidecar B targeted-crawl candidates, and flags methodology notes for Sidecar B execution.

**Top 3 thin traditions by absolute gap:**

| Rank | Tradition | Current substrate % | Sketch D target % | Gap % |
|---|---|---:|---:|---:|
| 1 | Egyptian | 0.01 | 4 | **-3.99** |
| 2 | Vedic / Hindu | 0.02 | 4 | **-3.98** |
| 3 | Mesoamerican | 0.11 | 4 | **-3.89** |

These three traditions need ~3,500-3,600 substrate-row additions to hit Sketch D targets (against ~89,841 substrate baseline). Sidecar B targeted crawl should prioritize these first.

---

## 1. Top-tier traditions (canonical lineage label)

Substrate share calculated against full substrate (N=89,841 rows). Sketch D target percentages refer to the **v1_scope** subset (~1,100-1,400 items), not the full substrate; therefore "gap" is approximate (assumes v1_scope mirrors substrate ratios per Sketch D substrate-led philosophy).

| Tradition | Substrate rows | Mode-A eligible | Substrate % | Sketch D target % | Gap % | Sidecar B priority |
|---|---:|---:|---:|---:|---:|---|
| European medieval (broad) | 28,595 | 13,239 | 31.83 | 35 | -3.17 | LOW (rich; Norse/Celtic subset under-tagged) |
| East Asian | 16,102 | 3,088 | 17.92 | 21 | -3.08 | LOW (rich; named-bearer subset thin per Sketch F) |
| Pan-Fantasy / fantasy_generic | 17,165 | 0 | 19.11 | 16 | +3.11 | NEGATIVE (trim during v1_scope sampling) |
| Middle Eastern (canonical) | 1,650 | 448 | 1.84 | 6 | -4.16 | HIGH (Egyptian + Sumerian sub-traditions) |
| South Asian (canonical) | 1,538 | 737 | 1.71 | 5 | -3.29 | HIGH (Vedic + Hindu sub-traditions) |
| Mesoamerican | 97 | 24 | 0.11 | 4 | -3.89 | HIGH (Aztec + Maya) |
| African (canonical) | 563 | 125 | 0.63 | — | — | (untargeted but available) |
| Southeast Asian | 872 | 354 | 0.97 | — | — | (untargeted but available) |
| Marginal lineages (sum of arctic/oceanic/n_am_indig/s_am_indig) | 345 | — | 0.38 | — | — | v1.1+ deferred per Sketch D § 4.2 |

---

## 2. Sub-tradition tag probes (Sketch D § 4.1 sub-allocations)

Sketch D § 4.1 sub-divides the canonical-lineage layer into more specific cultural-traditions. These sub-traditions appear in `cultural_lineage_tags` JSON (not in `cultural_lineage_canonical`). Tag-substring probes give lower-bound counts.

| Sub-tradition | Tag patterns | Substrate rows | Substrate % | Sketch D target % | Gap % | Sidecar B priority |
|---|---|---:|---:|---:|---:|---|
| Egyptian | `egyptian` | 9 | 0.01 | 4 | **-3.99** | **TOP-PRIORITY** |
| Sumerian / Mesopotamian | `sumerian`, `mesopotamian` | 0 | 0.00 | 3 | **-3.00** | **TOP-PRIORITY** |
| Vedic / Hindu | `vedic`, `hindu` | 17 | 0.02 | 4 | **-3.98** | **TOP-PRIORITY** |
| Mesoamerican (canonical lineage = `mesoamerican`) | — | 97 | 0.11 | 4 | **-3.89** | **TOP-PRIORITY** |
| Slavic | `slavic`, `russian`, `polish` | 149 | 0.17 | 3 | -2.83 | HIGH (much hides in `european` canonical) |
| Norse | `norse`, `viking` | 25 | 0.03 | 10 | -9.97 | HIGH (much hides in `european` canonical) |
| Greek | `greek`, `hellenic` | 16 | 0.02 | 8 | -7.98 | HIGH (much hides in `european` canonical) |
| Celtic | `celtic`, `gaelic`, `irish` | 14 | 0.02 | 6 | -5.98 | HIGH (much hides in `european` canonical) |

**Critical methodology note:** the Norse / Greek / Celtic gaps appear catastrophic at tag-substring level because **most Norse/Greek/Celtic substrate is encoded under the broader `european` canonical lineage**, not as a tag substring. The true Norse/Greek/Celtic substrate is part of the 28,595-row European pool. Sidecar B's job here is **cluster-level reclamation** (i.e., assigning the European-canonical Norse/Greek/Celtic subset to a refined tag) rather than substrate-crawl-extension.

---

## 3. Sidecar B targeted crawl candidates (prioritized)

Per the gap analysis above, three sub-traditions need substrate-expansion crawls (Sketch D § 4.3 explicitly named):

### 3.1 Egyptian (gap -3.99%, ~3,600 rows desired)
- **Current:** 9 tagged rows (most are sub-saharan / hellenic edge cases or museum artifacts)
- **Sources to crawl:** Egyptian Museum (Cairo), Met Museum Egyptian section (already partial), British Museum Egyptian section, Petrie Museum, Bulaq Museum, academic egyptology databases
- **Expected weapon families:** khopesh, mace, axe (battle-axe), spear, sling, bow (Egyptian composite), war-chariot equipage
- **Named-bearer anchors:** Cleopatra (Sketch F Tier-2), Pharaonic ceremonial weapons (Tier-1 mythological — Set, Horus weapons)
- **Discipline #25 rep-audit:** distinguish historical Egyptian (Mode A) from modern Egyptian military (Mode B); Saqr / Egyptian-army items will be Mode-B contamination

### 3.2 Sumerian / Mesopotamian (gap -3.00%, ~2,700 rows desired)
- **Current:** 0 tagged rows under `sumerian`/`mesopotamian`. Per Stage 1.5 per-source-coverage § 3, mesopotamian Pass B match count = 15 (over-catching "Ishtar"/"Marduk" cross-cultural references); spot-check needed.
- **Sources to crawl:** Iraq Museum (Baghdad), Met Museum ANE section, British Museum ANE section, Oriental Institute (Chicago), Louvre ANE collection
- **Expected weapon families:** sickle-sword (sappara), bronze mace, composite bow, javelin, axe (epsilon/duck-bill), siege engines
- **Named-bearer anchors:** Gilgamesh (Sketch F Tier-1 mythological)
- **Discipline #25 rep-audit:** Sumerian period is pre_classical / classical; distinguish from contemporary Iraqi military (Mode B)

### 3.3 Vedic / Hindu (gap -3.98%, ~3,500 rows desired)
- **Current:** 17 tagged rows; 120 Pass B matches (over-catching real-Indian-military "Agni"/"Karna" namesakes per Stage 1.5 § 3 — Mode C contamination)
- **Sources to crawl:** National Museum (New Delhi), Salar Jung Museum (Hyderabad), Calico Museum (Ahmedabad), Met Museum South Asian section
- **Expected weapon families:** talwar, khanda, urumi, katar, chakram, vajra (ceremonial), bow (Karna's Vijaya, Arjuna's Gandiva)
- **Named-bearer anchors:** Karna (Sketch F Tier-1 mythological), Arjuna, Rama, weapons of the Mahabharata
- **Discipline #25 rep-audit:** Vedic-Hindu has high Mode-C contamination (Indian military missile names — Agni, Prithvi, Akash); strictly enforce `register='historical' AND period ∈ pre-classical/classical/medieval` for Sidecar B

### 3.4 Mesoamerican (gap -3.89%, ~3,500 rows desired)
- **Current:** 97 canonical-lineage rows; per Stage 1.5 § 3, only 3 Pass B matches (Quetzalcoatl × 2 + Camazotz × 1). Per `marginal-lineage-tagging-pattern-2026-05-23.md`, the existing canonical-mesoamerican rows are heavily contaminated with modern Mexican arms-industry (Mendoza / Cabañas / Zaragoza / Mexican Mauser); ~12-15 actual cultural-Pre-Columbian items scattered across 5 clusters.
- **Sources to crawl:** Museo Nacional de Antropología (Mexico City), Museo del Templo Mayor, Museo Maya de Cancún, Museo Larco (Lima — for cross-reference), Met Museum Pre-Columbian section
- **Expected weapon families:** macuahuitl, tlacochtli, atlatl (Aztec javelin-thrower), tepoztopilli, hammers of obsidian, slings, bow (Maya), ceremonial obsidian blades
- **Named-bearer anchors:** Moctezuma (Sketch F Tier-2 historical + Tier-1 nested mythological summoning Quetzalcoatl)
- **Discipline #25 rep-audit:** strictly enforce `register='historical' AND period ∈ pre_classical/classical/medieval`; filter out `mendoza`/`cabañas`/`zaragoza`/`mexican-mauser` tokens which are 19th-20th C arms-industry.

---

## 4. Additional Sidecar B opportunities (rich-but-tag-buried)

These sub-traditions have substantial substrate populations buried under the broad `european` canonical lineage and would benefit from **cluster-level reclamation** rather than crawl-extension:

### 4.1 Norse (gap -9.97% at tag level; suspect actual gap << this)
- The `european` lineage holds many Norse/Viking weapons (greatsword, war-hammer, axe, seax). Sidecar B could:
  - Spot-check `european` rows for Norse-period markers (early medieval, runic, Scandinavia origin)
  - Refine `cultural_lineage_tags` to add 'norse'/'viking' tag where applicable

### 4.2 Greek (gap -7.98% at tag level; suspect actual gap << this)
- Same pattern; classical-period Mediterranean weapons in `european` substrate
- Sidecar B reclamation via period × geographic filter on `european`

### 4.3 Celtic (gap -5.98% at tag level; suspect actual gap << this)
- Same pattern; Iron Age + early medieval Insular/Continental Celtic weapons

### 4.4 Slavic (gap -2.83% at tag level)
- The 149 tag-matched Slavic rows are mostly Russian / Polish (modern + historical). Sidecar B should disambiguate via period filter; the Stage 1.5 record's Baba Yaga 6 Slavic + 6 modern-Ukrainian-UAV-naming-allusion split is the model contamination pattern.

---

## 5. Sketch F 4-zero anchor enrichment

These Stage 0 named-bearer anchors have zero substrate presence and should be addressed via Sidecar B's substrate-expansion-by-Mode-A-targeting discipline (per `marginal-lineage-tagging-pattern-2026-05-23.md`):

| Anchor | Tier | Substrate hits | Target sub-tradition | Sidecar B route |
|---|---|---:|---|---|
| Hattori Hanzō | Tier 2 (East Asian historical) | 1 (fantasy-coinage WoW item only) | East Asian (Sengoku-era) | Crawl Japanese castle museums, ninja-history primary sources |
| Lu Bu | Tier 2 (East Asian historical) | 0 | East Asian (Three Kingdoms) | Crawl Chinese historical sources, Three Kingdoms iconography |
| Moctezuma | Tier 2 (Mesoamerican historical) | 0 | Mesoamerican | Crawl Aztec museums (covered above § 3.4) |
| Gilgamesh | Tier 1 (Sumerian mythological) | 0 | Sumerian / Mesopotamian | Crawl ANE museums (covered above § 3.2) |

---

## 6. Methodology notes for Sidecar B execution

### 6.1 Pre-crawl rep-audit discipline
Per Discipline #25 + `marginal-lineage-tagging-pattern-2026-05-23.md`, every Sidecar B crawl target should:
1. Pre-audit 30-50 sample candidate rows for Mode A/B/C/D distribution
2. Confirm sources skew Mode A (cultural-tradition pre-industrial)
3. Reject sources that surface Mode B (geographic-region modern military) at >30%
4. Filter aggressively on `register_canonical` + `historical_period_canonical` at write-time

### 6.2 Discipline #11 attribution preservation
Source phrasing must be preserved verbatim. Curation interpretation happens downstream.

### 6.3 Cycle 10 v1.1+ deferment for marginal lineages
Per Sketch D § 4.2 and the 5 marginal-lineage recognition records (n.am / s.am / arctic / oceanic / mesoamerican):
- Native American Indigenous, Aboriginal Australian, Pacific Islander / Polynesian, Sub-Saharan African, Inuit/Arctic, Tibetan/Mongolian — DEFERRED to v1.1+
- v1.0 substrate-enrichment focuses on the 4 top-priority sub-traditions above (Egyptian + Sumerian + Vedic-Hindu + Mesoamerican)

### 6.4 Sidecar B does NOT fire at Stage 2 boundary
Per dispatch § 6 out-of-scope: Stage 2 only **surfaces** the thin-tradition list. Sidecar B execution is a separate dispatch fire.

---

## 7. Cross-references

- HTML cross-tab: `cross-tab.html` § 3
- Sketch D substrate-enrichment fold: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 4.3
- Sketch F 4-zero anchors: `canonical/story/v1-bc-target-intent-2026-05-24.md` § 6.1
- Marginal-lineage tagging pattern: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Stage 1.5 per-source coverage: `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/per-source-coverage.md`
- Engineering disciplines #11, #25: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## 8. Sign-off

**Author:** elrond (data steward)
**Authority:** Cycle 10 Wave 3 dispatch — Stage 2 thin-tradition surfacing for Sidecar B
**Status:** EXECUTION COMPLETE — feeds Stage 3 design call + future Sidecar B scope
**Tag intent:** `elrond/v0.0-cycle-10-stage-2-cross-tab` (combined)
