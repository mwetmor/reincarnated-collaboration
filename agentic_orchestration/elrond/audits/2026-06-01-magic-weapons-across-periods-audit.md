# IA-2 Phase 1 — Magic-Weapons-Across-Periods Substrate Coverage Audit

**STATUS:** CURRENT (Mode A read-only audit; produced 2026-06-01)
**Author:** elrond (data steward seam)
**Authority:** Matt 2026-06-01 strategic reset directive (transmitted via gandalf Pattern B reframe; "agree with the above") + jack-ryan IA-2 Phase 1 Gate-1 PASS-with-INFO 2026-06-01
**Companion docs:**
- `agentic_orchestration/dispatches/2026-06-01-elrond-ia-2-phase-1-magic-weapons-across-periods-audit.md` (dispatch)
- `agentic_orchestration/qa/findings/2026-06-01-ia-2-phase-1-gate-1.md` (Gate-1 PASS-with-INFO; 3 INFO items)
- `agentic_orchestration/elrond/audits/2026-06-01-modern-caster-substrate-coverage-audit.md` (WS2.P1 MODERN-period input; REUSED by reference)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (7 rotating primaries + 19 modern-scientific overlay locks)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC axes; substrate measurement coordinate)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (composition policy)
- `agentic_orchestration/research/scripts/ia2_phase1_magic_weapons_across_periods_audit.py` (audit query script — reproducible)

---

## 0. TL;DR

**Magic-weapon coverage is asymmetric across periods.** ANCIENT is substantively backed (the strongest period, ~115 magic-weapon rows across 7 primaries — anchored by Vedic / Greek / Norse / Mesopotamian mythological canon and WoW-classic fantasy at classical period). MEDIEVAL is moderately thin (37 magic-weapon rows; Solomonic grimoires + Mongol banners + Aztec Moctezuma families + Carolingian named weapons compose the bulk). MODERN is uniformly thin across all 7 primaries (per WS2.P1; ~45-67 weapons authoring gap).

The 21-cell coverage grid shows **strongest backing at ANCIENT.holy / ANCIENT.earth / ANCIENT.lightning** (where mythological-canonical inventory directly maps to primaries), **moderate backing at ANCIENT.shadow / ANCIENT.wind / MEDIEVAL.earth / MEDIEVAL.holy**, and **uniform absent/weak coverage at fire and water across all periods**. MODERN is uniformly absent per WS2.P1's prior finding.

### 21-cell coverage grid

| Primary | ANCIENT (n rows) | MEDIEVAL (n rows) | MODERN (n rows) |
|---|---|---|---|
| **fire** | WEAK (3) | WEAK (2) | ABSENT (~0 strong, per WS2.P1) |
| **water** | WEAK (5) | WEAK (2) | ABSENT (~0 strong, per WS2.P1) |
| **earth** | STRONG (38) | MEDIUM (13) | ABSENT (~0 strong, per WS2.P1) |
| **wind** | MEDIUM (10) | WEAK (2) | ABSENT (~0 strong, per WS2.P1) |
| **lightning** | MEDIUM (16) | WEAK (6) | WEAK (1 strong; Staff of Ionization per WS2.P1) |
| **holy** | STRONG (30) | MEDIUM (11) | WEAK (per WS2.P1; ~26 fantasy-fictional, mostly pre-industrial) |
| **shadow** | MEDIUM (13) | ABSENT (1) | WEAK (per WS2.P1; ~8 fantasy-fictional sci-fi) |

Total magic-weapon-eligible rows discovered: **~117 ANCIENT + ~37 MEDIEVAL + ~2 MODERN strong (per WS2.P1) = ~156 across all 21 cells**.

### Per-period gap quantification (Phase 2 anchor-authoring scope)

| Period | Per-cell anchor-authoring scope (gandalf) | Catalogue crawl supplementary scope (legolas) | Per-period total |
|---|---|---|---|
| ANCIENT | 2-4 anchors × 7 primaries = 14-28 | 10-20 supplementary (water/fire underserved) | ~25-50 |
| MEDIEVAL | 3-5 anchors × 7 primaries = 21-35 | 10-20 supplementary (witch/alchemist, runed) | ~30-55 |
| MODERN | Per WS2.P1: 5-10 × 7 = 35-67 (WS2.P1 § 5.2 estimate) | ~10 supplementary (sci-fi-themed substrate templates exist in `nick-aschenbach-dnd-data`) | ~45-77 |
| **TOTAL** | **~70-130 anchors** | **~30-60 supplementary** | **~100-180** |

This is broader than the dispatch's ~45-80 range. The dispatch range was anchored on WS2.P1's MODERN-only ~45-67 estimate. Audit recommends scope-mid-range **~80-100 weapons** for the full 21-cell grid as the practical Phase 2 commitment (gandalf 60-70 manual anchors + legolas 20-30 supplementary crawl); upper-bound 180 reserved for v1.1+ extension if Phase 2 reveals MODERN demands the full WS2.P1 estimate.

**Notable finding:** the substrate has **substantial primary-unattributed magic-weapon coverage** at ANCIENT (509 magic-weapon-eligible rows where only 117 carry primary-element vocabulary signal) and MEDIEVAL (60 eligible, 37 carry signal). This suggests Phase 3 elrond ingest may want to RETROACTIVELY tag the unattributed-magic-weapon rows with primary-element associations where appropriate (e.g., Solomonic grimoires → shadow/holy; Mongol banners → wind/earth; Picatrix → shadow). This is a separate methodology recommendation — surfaced in § 6.

---

## 1. Methodology

### 1.1 Audit scope

Mode A read-only SQL query against `~/Games/reincarnated-loadout/data/telemetry.db` `weapon_knowledge_entries` table (90,220 rows current; dispatch cited 89,839 — per WS2.P1 stale-figure note already acknowledged).

The 21-cell grid spans 3 periods × 7 rotating primaries. Per INFO-1 from jack-ryan Gate-1: **physical is excluded by design** because Architecture-A taxonomy-sibling registry classifies it as not a rotating-primary flavor pool. Confirmed.

### 1.2 Period definitions (audit-internal)

Substrate `historical_period_canonical` field maps to the 3 IA-2 periods:

| IA-2 Period | substrate periods | rows |
|---|---|---:|
| **ANCIENT** | `pre_classical` (77) + `classical` (5,361) | 5,438 |
| **MEDIEVAL** | `medieval` (2,081) | 2,081 |
| **MODERN** | `industrial` (7,207) + `modern` (6,215) + `contemporary` (7,783) | 21,205 |

Plus, MODERN admits `fictional` period rows (14,113) when register=`fantasy` AND name evidences sci-fi-coded vocabulary (per WS2.P1 § 1.2 fantasy-fictional-modern-coded eligibility tier). This audit reuses WS2.P1's MODERN data directly per dispatch instruction; no re-execution.

Substrate `early_modern` (14,549 rows) is NOT mapped to any IA-2 period because it spans the Renaissance / gunpowder transition era which is conceptually ambiguous against ANCIENT/MEDIEVAL/MODERN. Audit holds early_modern out of scope.

### 1.3 Per-period "magic-weapon" operational criteria (elrond seam authority, per INFO-3)

**ANCIENT period magic-weapon eligibility:**

A row is ANCIENT magic-weapon-eligible if `historical_period_canonical IN ('pre_classical', 'classical')` AND ANY of:

1. `register_canonical = 'mythological'` (substrate's classifier flagged divine/mythological)
2. `named_mythological_match` is populated (substrate tied the entry to a mythological named figure)
3. `weapon_kind IN ('tome','focus','talisman','horn','banner')` (caster-vessel weapon-class)
4. `proxy_attribute_class IN ('INT','WIS','INT_or_WIS','WIS_or_INT','STR_or_WIS')` (caster-attribute coded)

**Rationale:** ancient magic-weapons in the substrate are anchored by mythological-named-bearer + caster-vessel + caster-attribute signals. The four-OR-rule captures the union of these signals while preserving auditability. Bronze-Age and Antiquity legendary weapons (Mjolnir, Vajra, Gungnir, Sudarshana Chakra, Gandiva, Trishula, Indra's Rod, Zeus's Thunderbolt) consistently carry mythological-register OR named-bearer signals; pre-Christian Indo-European mage-staves carry caster-attribute INT/WIS signals.

**MEDIEVAL period magic-weapon eligibility:**

A row is MEDIEVAL magic-weapon-eligible if `historical_period_canonical = 'medieval'` AND ANY of:

1. `register_canonical = 'mythological'` (divine attribution)
2. `named_mythological_match` is populated
3. `weapon_kind IN ('tome','focus','talisman','horn','banner')` (caster-vessel)
4. `proxy_attribute_class IN ('INT','WIS','INT_or_WIS','WIS_or_INT','STR_or_WIS')` (caster-attribute)
5. `canonical_name` contains enchantment / runed / grimoire / witch / alchemist / mage / sorcerer / blessed / consecrated / cursed vocabulary (medieval-magical naming)

**Rationale:** medieval magic-weapons split into enchanted-named-legendary (Joyeuse, Durendal, Excalibur, Sword of Freyr) + grimoires (Solomonic / Picatrix / Sefer-tradition) + named-banner artifacts (Raven Banner, Oriflamme) + ritual-talismans (Charlemagne, Solomon). The 5-OR-rule captures these clusters; the 5th rule (vocabulary) supplements where periods don't explicitly carry mythological-register but the name evidences enchantment.

**MODERN period magic-weapon eligibility:**

Per WS2.P1 § 1.2 (REUSED, NOT re-executed):

A row is MODERN magic-weapon-strong if:
- `proxy_attribute_class IN ('INT','WIS','INT_or_WIS','WIS_or_INT','STR_or_WIS')` (caster-attribute), AND
- `historical_period_canonical IN ('industrial','modern','contemporary')` (modern-period) OR (`register_canonical = 'fantasy'` AND `historical_period_canonical = 'fictional'` with sci-fi-coded naming) OR (`register_canonical = 'military_modern'`), AND
- `weapon_kind` suggests caster-vessel OR `weapon_kind_classified_subtype = 'accessory_handheld'`.

A row is MODERN fantasy-fictional-modern-coded if `register_canonical = 'fantasy'` AND `historical_period_canonical = 'fictional'` AND sci-fi-coded naming, regardless of attribute. This captures fantasy-ARPG entries (D&D / WoW / PoE) using sci-fi terminology in pre-industrial mechanical framing.

### 1.4 Per-primary keyword matching

For ANCIENT + MEDIEVAL, each primary's vocabulary set draws from:
- Q18 lock allow-list (per primary; 12-18 entries each)
- Mythological hero/deity vocabulary (Agni, Indra, Thor, Poseidon, Zeus, etc.)
- Magical-implement signals (X staff, X wand, X tome, X focus)

Word-boundary regex (case-insensitive) applied to `canonical_name`, `named_mythological_match`, and `structured_properties` text. False-positive false-positives reduced via word-boundary anchoring (rejecting `passion` for `ion`, etc.).

For MODERN, keyword vocabulary REUSED from WS2.P1 audit's `OVERLAY_QUERIES` dict; no re-execution of the audit, just citation.

### 1.5 Audit blind spots

1. **Keyword-only signal.** Magic-weapon identity expressed through non-canonical vocabulary (e.g., "Crystal Star" without explicit primary-element vocabulary) is under-counted. Audit reports a CONSERVATIVE FLOOR per primary.
2. **Description-text and structured-properties scan is shallow.** Audit examines `canonical_name`, `named_mythological_match`, and `structured_properties` JSON-string. Deep-semantic scoring of description_text deferred as out-of-scope for Phase 1 quick-discovery.
3. **Embeddings unused.** `text_embedding` BLOB column not queried; semantic-similarity sweep would surface 10-30 additional candidates per period. Deferred to Phase 4 validation if scope precision matters more.
4. **Primary-unattributed magic-weapon pool not classified.** ~509 ANCIENT and ~60 MEDIEVAL rows are magic-weapon-eligible but carry no primary-element vocabulary in canonical_name. They COULD be primary-tagged retroactively (Solomonic grimoires → shadow/holy; Mongol banners → wind/earth). This is a Phase 3 ingest methodology question, not Phase 1 audit scope. See § 6.4.
5. **Early-modern period held out of scope.** 14,549 rows in `early_modern` (Renaissance through gunpowder transition; Hattori Hanzō ninja-tradition, etc.) span the ANCIENT-MEDIEVAL/MODERN boundary. Audit excluded for clarity. If kit-identity-realization demands early-modern coverage (e.g., Hanzō / Yagyū / Edo-period esoteric weapons), supplementary audit needed.
6. **Period mis-classification risk in fantasy substrate.** WoW-classic-items (3,149 rows) are classified `historical_period_canonical = classical` because the in-game lore positions them as ancient. This inflates the ANCIENT.fantasy count. Audit conservatively reports the substrate-as-classified; downstream consumers should be aware that ANCIENT counts include WoW-pre-industrial-fantasy that may or may not be ancient-coded for Reincarnated kit identity.
7. **Lineage classification heuristic (per WS2.P1 § 1.3 framing).** `source_library` → manually-authored vs crawl-extracted is heuristic. The genuinely manually-authored sources are `engine_authored_gap_fill_v1` (43 rows) + `legolas_crawl_substrate_enrichment_v1_2026_05_27` (206 rows). All others are crawl-extracted.
8. **MODERN reused-by-reference.** Per dispatch § 4 + jack-ryan Gate-1 § 4.2, WS2.P1 audit data is incorporated by reference; MODERN cell counts in this audit derive from WS2.P1 § 0 + § 2 reporting and are NOT re-derived against current 90,220-row substrate. The MODERN audit data is current as of 2026-06-01 WS2.P1 close.

### 1.6 Reproducibility

Audit script: `agentic_orchestration/research/scripts/ia2_phase1_magic_weapons_across_periods_audit.py`. Mode A Python 3 read-only query; deterministic regex; deterministic period boundaries. Re-run produces same output up to substrate enrichment.

---

## 2. Per-period detailed findings — ANCIENT (pre_classical + classical)

Period scope: 5,438 substrate rows; 509 magic-weapon-eligible; ~117 carry primary-element vocabulary.

### 2.1 fire — WEAK (3 rows; 0 manual / 3 crawl)

**Top reps:**
- Staff of the Shadow Flame (wow-classic-items; classical; INT; tier B; named_template)
- Wand of Purifying Fire (wow-classic-items; classical; INT; tier B; named_template)
- Staff of the Shadow Flame (Purple Enchant) (wow-classic-items; classical; INT; tier B; named_template)

**Lineage:** all 3 from wow-classic-items; period-misclassified as classical (in-game lore = pre-industrial fantasy). No mythological-pre_classical fire weapons in the substrate (Agni / Surt / Hephaestus / Vulcan / Xiuhcoatl are not represented as primary-fire weapons).

**Verdict ABSENT-as-mythological + WEAK-as-fantasy-classical:** the substrate lacks mythological-fire-primary weapons from Vedic / Norse / Greek / Egyptian / Aztec canon. Phase 2 anchor candidates: Agni's Astra (Vedic), Brand of Surt (Norse), Phoenix Feather Wand (Greek), Tlaloc's Fire-Cycle Wand (Aztec — currently exists at engine_authored_gap_fill_v1 as `moctezuma_xiuhcoatl_staff` but classified medieval). **Recommend 3-5 anchor weapons.**

### 2.2 water — WEAK (5 rows; 0 manual / 5 crawl)

**Top reps:**
- Nethekurse's Rod of Torment (wow-classic-items; classical; INT; tier B)
- Solid Ice Wand (wow-classic-items; classical; INT; tier B)
- Cascading Water Staff (wow-classic-items; classical; INT; tier B)
- Snow Blossom Staff (wow-classic-items; classical; INT; tier B)
- trident of Poseidon (wikidata; classical; DEX; tier S; named=Poseidon)

**Lineage:** 4 of 5 from WoW (fantasy-classical pre-industrial); 1 from wikidata-mythological-Greek. Poseidon's trident exists but is DEX-coded (not caster).

**Verdict WEAK:** the substrate lacks named-mythological-water-caster weapons from ancient canon (Poseidon's trident is the only named-mythological water weapon, and it's DEX). Phase 2 anchor candidates: Varuna's Pasha (Vedic noose-staff), Tlaloc's Rain Conch (Aztec; currently `moctezuma_tlaloc_rain_staff` at engine-authored medieval), Lir's Tide Wand (Celtic), Ahti's Storm Lure (Finnic). **Recommend 3-5 anchor weapons.**

### 2.3 earth — STRONG (38 rows; 5 manual / 33 crawl)

**Top reps:**
- mace (wikidata; pre_classical; WIS; tier S; named=Shulgi, mesopotamian)
- Fang of the Crystal Spider (wow-classic-items; classical; INT; tier B)
- Resurgence Rod (wow-classic-items; classical; INT; tier B)
- High Warlord's War Staff (wow-classic-items; classical; INT; tier B)
- Sparkling Crystal Wand (wow-classic-items; classical; INT; tier B)

**Lineage:** dominant wow-classic-items (22); supplementary wikipedia (8) + engine-authored (5 — `moctezuma_*` family at medieval) + wikidata (3 — Shulgi mace; crystal-named entries).

**Verdict STRONG:** earth is the best-backed ANCIENT primary, owing to (a) crystal/stone/jade/obsidian vocabulary saturation in fantasy ARPG sources (b) Mesopotamian named-bearer signal (Shulgi). However, the rep set is heavily fantasy-modern-coded WoW, not Bronze-Age-myth-coded; the substrate underserves Vedic Prithvi / Greek Gaia / Egyptian Geb / Aztec Coatlicue. **Recommend 2-3 anchor weapons** for mythological-earth-deity-named-bearer enrichment.

### 2.4 wind — MEDIUM (10 rows; 1 manual / 9 crawl)

**Top reps:**
- Vayavyastra Staff (legolas-crawl-substrate-enrichment; pre_classical; INT; tier S; named_template)
- Wind Spirit Staff (wow-classic-items; classical; INT; tier B)
- Wand of Chilled Renewal (wow-classic-items; classical; INT; tier B)
- Green Mace (wikipedia; classical; WIS; tier B)
- Rod of the Vonindod (nick-aschenbach-dnd-data; classical; INT; tier C)

**Lineage:** wikipedia (6) + wow (2) + nick-aschenbach (1) + legolas-crawl-enrichment (1). The Vedic Vayavyastra is the strongest reference; substrate lacks Greek Aeolus / Norse Njord / Slavic Stribog / Egyptian Shu wind-named-bearer weapons.

**Verdict MEDIUM:** wind has 1 strong mythological anchor (Vayavyastra) + 9 secondary entries; sufficient floor for kit-identity-realization but thin on cultural-anchor diversity. **Recommend 2-3 anchor weapons** for Greek/Norse/Slavic/Egyptian-canon wind-deity diversification.

### 2.5 lightning — MEDIUM (16 rows; 7 manual / 9 crawl)

**Top reps:**
- vajra (wikidata; pre_classical; WIS; tier S; named=Indra)
- Vajra (wikipedia; pre_classical; WIS; tier S; named=Indra)
- Indra's Rod (legolas-crawl-substrate-enrichment; pre_classical; INT; tier S; named_template)
- Mjolnir-Pattern Warhammer Rod (legolas-crawl-substrate-enrichment; pre_classical; INT; tier S; named_template)
- Zeus's Thunderbolt Staff (legolas-crawl-substrate-enrichment; pre_classical; INT; tier S; named_template)

**Lineage:** legolas-crawl-enrichment (7) + wikidata (4) + wikipedia (3) + nick-aschenbach (1) + wow (1). The 7 manually-curated entries plus Indra/Thor/Zeus mythological backing make lightning the second-strongest ANCIENT primary by depth.

**Verdict MEDIUM:** lightning has substantive cultural-canon coverage (Vedic / Norse / Greek explicitly represented) but Slavic Perun / Japanese Raijin / Aztec Tlaloc-lightning gaps. **Recommend 2-3 anchor weapons** for cross-cultural diversification.

### 2.6 holy — STRONG (30 rows; 8 manual / 22 crawl)

**Top reps:**
- vajra (wikidata; pre_classical; WIS; tier S; named=Indra) — flex matched on holy too via implement_signals
- Vajra (wikipedia; pre_classical; WIS; tier S; named=Indra)
- Sudarshana Chakra Rod (legolas-crawl-substrate-enrichment; pre_classical; INT; tier S; named_template)
- Trishula Staff (Shiva) (legolas-crawl-substrate-enrichment; pre_classical; WIS; tier S; named_template)
- Caduceus (Hermes Wand) (legolas-crawl-substrate-enrichment; pre_classical; INT; tier S; named_template)

**Lineage:** wow-classic-items (11) + wikipedia (9) + legolas-crawl-enrichment (8) + wikidata (2). The strongest ANCIENT cell — Vedic divine-implement canon (Sudarshana / Trishula / Vajra / Caduceus) + WoW priest staves + Hermetic / Egyptian / Buddhist staff-tradition.

**Verdict STRONG:** holy is well-backed for ANCIENT period. Modest gap on Egyptian Ra / Aztec Quetzalcoatl-holy / Aztec Huitzilopochtli weapons. **Recommend 1-2 anchor weapons** (gap is the slimmest).

### 2.7 shadow — MEDIUM (13 rows; 0 manual / 13 crawl)

**Top reps:**
- Shadow Wing Focus Staff (wow-classic-items; classical; INT; tier B)
- Staff of the Shadow Flame (wow-classic-items; classical; INT; tier B)
- Dark Augur's Wand (wow-classic-items; classical; INT; tier B)
- Soul-Wand of the Aldor (wow-classic-items; classical; INT; tier B)
- Tirisfal Wand of Ascendancy (wow-classic-items; classical; INT; tier B)

**Lineage:** wow-classic-items (11) + wikipedia (2). 11-of-13 from WoW; mythological canon thin (no Hades / Anubis / Yama / Kali / Erebus-named-bearer weapons in substrate).

**Verdict MEDIUM:** shadow has decent WoW-fantasy-classical depth but lacks mythological-named-bearer anchors from underworld-deity canon. **Recommend 3-4 anchor weapons** for Greek Hades / Egyptian Anubis / Vedic Yama / Norse Hel cross-cultural diversification.

### 2.8 ANCIENT lineage aggregate

ANCIENT primaries (across all 7) sum to ~117 magic-weapon-vocabulary rows. Lineage:
- **manually-authored:** 21 rows (engine_authored_gap_fill_v1 + legolas_crawl_substrate_enrichment — primarily the Gilgamesh / Karna / Vedic-astras / WoW-curation supplements)
- **crawl-extracted:** 94 rows (predominantly wow-classic-items at classical + wikipedia/wikidata at pre_classical/classical)

**Primary-unattributed ANCIENT magic-weapon pool:** 509 substrate rows are magic-weapon-eligible (caster-vessel OR caster-attribute OR mythological-register OR named-mythological-match) but only 117 carry primary-element vocabulary signal. The 392-row gap is the **untapped retroactive-primary-tagging surface** — see § 6.4 methodology recommendation.

---

## 3. Per-period detailed findings — MEDIEVAL (medieval)

Period scope: 2,081 substrate rows; 60 magic-weapon-eligible; ~37 carry primary-element vocabulary.

### 3.1 fire — WEAK (2 rows; 1 manual / 1 crawl)

**Top reps:**
- moctezuma_xiuhcoatl_staff (engine_authored_gap_fill_v1; medieval; WIS; tier S; named=Xiuhcoatl)
- Nine White Banners of Mongolia (wikipedia; medieval; STR_or_WIS; banner)

**Verdict WEAK:** the Aztec fire-serpent staff is the single manually-authored anchor; Mongol banners are coverage-adjacent. Substrate lacks medieval-witch-flame focuses, alchemist fire-rods, Crusader-era enchanted flame swords. **Recommend 3-5 anchor weapons** for medieval witch / alchemist / Crusader-era fire-magic coverage.

### 3.2 water — WEAK (2 rows; 1 manual / 1 crawl)

**Top reps:**
- moctezuma_tlaloc_rain_staff (engine_authored_gap_fill_v1; medieval; WIS; tier S; named=Tlaloc)
- Islamic Talismanic Bowl (wikipedia; medieval; WIS_or_INT; talisman)

**Verdict WEAK:** as above. Tlaloc Aztec rain-staff is the manually-authored anchor; Islamic talismanic-bowl is coverage-adjacent (talismanic, not primary-water-named). Substrate lacks witch storm-staves, alchemist mercury-flasks, Crusader-era enchanted ice swords. **Recommend 3-5 anchor weapons.**

### 3.3 earth — MEDIUM (13 rows; 3 manual / 10 crawl)

**Top reps:**
- moctezuma_macuahuitl (engine_authored_gap_fill_v1; medieval; INT; tier S; named=Moctezuma)
- moctezuma_obsidian_blade_knife (engine_authored_gap_fill_v1; medieval; INT; tier S; named=Moctezuma)
- Islamic Talismanic Bowl (wikipedia; medieval; WIS_or_INT; talisman)
- Joyeuse (wikidata; medieval; STR; tier S; named=Charlemagne)
- Sword of Freyr (wikidata; medieval; STR; tier S; named=Freyr)

**Lineage:** met-museum (6) + engine_authored (3) + wikidata (2) + wikipedia (2). The substrate has reasonable Aztec-obsidian + Carolingian + Norse-Freyr named coverage.

**Verdict MEDIUM:** earth has substantive medieval-named-bearer coverage but lacks witch-stone-circle focuses, alchemist-metallurgy implements, Crusader-era enchanted-warhammer artifacts. **Recommend 2-3 anchor weapons** for medieval-witch + alchemist-metallurgy expansion.

### 3.4 wind — WEAK (2 rows; 0 manual / 2 crawl)

**Top reps:**
- S-500 missile system (wikipedia; medieval — PERIOD-MISCLASSIFIED; DEX; tier S; named=Prometheus)
- R.550 Magic (wikipedia; medieval — PERIOD-MISCLASSIFIED; tier B; category)

**Verdict ABSENT-effective:** both top reps are modern military hardware mis-classified as medieval. True medieval-wind magic-weapon coverage is **functionally absent**. Substrate lacks Aeolian harps as wind-focus, witch-storm-staves, alchemist-bellows-focuses, medieval-named-wind-deity-implements. **Recommend 4-5 anchor weapons.**

### 3.5 lightning — WEAK (6 rows; 0 manual / 6 crawl)

**Top reps:**
- Mjölnir (wikidata; medieval; STR; tier S; named=Thor)
- Gungnir (wikidata; medieval; STR; tier S; named=Odin)
- Mjölnir (wikipedia; medieval; STR; tier S; named=Thor)
- R-14 Chusovaya (wikipedia; medieval — PERIOD-MISCLASSIFIED; tier S; named=Thor)
- CZ 805 BREN (wikipedia; medieval — PERIOD-MISCLASSIFIED; DEX; named=Lada-slavic)

**Verdict WEAK:** the Norse Mjölnir/Gungnir are STR-coded melee, not caster. Two reps are modern-military period-misclassified. True medieval-lightning-caster substrate is thin. **Recommend 3-4 anchor weapons** for medieval witch / alchemist / Crusader-era lightning-focus expansion.

### 3.6 holy — MEDIUM (11 rows; 1 manual / 10 crawl)

**Top reps:**
- De velitatione bellica (wikipedia; medieval; INT_or_WIS; tome)
- Sefer Raziel Ha-Malakh (wikipedia; medieval; INT_or_WIS; tome)
- Ghayat al-Hakim (Picatrix) (wikipedia; medieval; INT_or_WIS; tome)
- Sefer HaRazim (wikipedia; medieval; INT_or_WIS; tome)
- Nine White Banners of Mongolia (wikipedia; medieval; STR_or_WIS; banner)

**Lineage:** wikipedia (6) + met-museum (3) + wikidata (1) + legolas-crawl-enrichment (1). MEDIEVAL.holy is best-covered through Solomonic/Hermetic grimoire-tomes + Mongol-Ottoman banners.

**Verdict MEDIUM:** strong tome coverage; gaps on Crusader-era reliquaries, monk staves, papal scepters, named-saint-relics. **Recommend 2-3 anchor weapons** for relic/scepter/saint-named diversification.

### 3.7 shadow — ABSENT (1 row; 0 manual / 1 crawl)

**Top reps:**
- Talisman of Charlemagne (wikipedia; medieval; WIS_or_INT; talisman)

**Verdict ABSENT:** the single row is talismanic (Charlemagne's medieval relic-talisman) — neither shadow-vocabulary nor underworld-deity-bearer. MEDIEVAL.shadow is the SECOND-weakest cell in the audit. Substrate lacks necromancer grimoires (despite Solomonic / Hermetic / Picatrix being attributable to shadow at retro-tagging gate; see § 6.4), witch-shadow-foci, alchemist-blackmetal-rods, named-medieval-undead-bearer weapons. **Recommend 5-6 anchor weapons** — the largest single-cell MEDIEVAL gap.

### 3.8 MEDIEVAL lineage aggregate

MEDIEVAL primaries (across all 7) sum to ~37 magic-weapon-vocabulary rows. Lineage:
- **manually-authored:** 6 rows (Moctezuma family at engine_authored_gap_fill_v1 + Roland family)
- **crawl-extracted:** 31 rows (predominantly wikipedia at medieval + met-museum)

**Primary-unattributed MEDIEVAL magic-weapon pool:** 60 substrate rows are magic-weapon-eligible but only 37 carry primary-element vocabulary signal. The 23-row gap is smaller than ANCIENT's gap (relative scale matches the smaller medieval substrate base) but is the same retroactive-primary-tagging methodology question. Phase 3 ingest should consider tagging Solomonic grimoires → shadow/holy split; Picatrix → shadow; Mongol banners → wind/earth.

---

## 4. Per-period detailed findings — MODERN (incorporated by reference)

Per dispatch § 4 + jack-ryan Gate-1 § 4.2: **WS2.P1 audit data is REUSED here; no re-execution.** The audit at `agentic_orchestration/elrond/audits/2026-06-01-modern-caster-substrate-coverage-audit.md` is the primary input for MODERN-period coverage.

### 4.1 WS2.P1 MODERN findings (verbatim restate)

Per WS2.P1 § 0 TL;DR + § 2 per-primary findings:

| Primary | Modern-caster strong (caster-attr ∩ modern-period) | Fantasy-fictional-modern-coded | WS2.P1 verdict |
|---|---:|---:|---|
| lightning | 1 (Staff of Ionization) | 3 | ABSENT |
| fire | 0 | 4 | ABSENT |
| holy | 0 | 26 (mostly pre-industrial `radiant`) | WEAK |
| shadow | 0 | 8 | WEAK |
| wind | 0 | 1 | ABSENT |
| water | 0 | 2 | ABSENT |
| earth | 0 | 1 | ABSENT |

**MODERN aggregate:** 1 row caster-attribute ∩ modern-period strong (Staff of Ionization). ~45 fantasy-fictional-modern-coded entries spread across primaries (predominantly holy and shadow).

**MODERN sub-finding from WS2.P1:** the `nick-aschenbach-dnd-data` library provides ~17 sci-fi-coded fantasy weapons (Antimatter Carbine, Plasma Foil, Fusion Blade, Laser Sword, Ion Cannon, EMP Grenade, Cryo Bomb, Singularity, etc.) — these are NOT modern-caster substrate but DO provide naming/identity TEMPLATES for Phase 2 authoring.

### 4.2 MODERN INFO-2 confirmation

Per jack-ryan Gate-1 INFO-2: the 19 designer-curation-modern-scientific-overlay entries (per WS1A.Q18 § 7 lineage table) are the audit's primary MODERN target. These entries (`fusion`, `thermal`, `combustion`, `hydro`, `hydraulic`, `seismic`, `tectonic`, `sonic`, `shockwave`, `plasma`, `flash`, `ion`, `voltage`, `tesla`, `stellar`, `solar`, `photon`, `laser`, `prismatic`) were added at the WS1A.Q18 designer-curation gate **precisely because substrate was absent**. WS2.P1's empirical finding ("modern-caster IS a missing substrate axis") corroborates the gate-side designer commitment.

### 4.3 MODERN coverage grid (per WS2.P1)

Per the WS2.P1 audit § 0 per-primary gap quantification table:

| Primary | WS2.P1 verdict | WS2.P1 Phase-2 anchor scope estimate |
|---|---|---:|
| lightning | ABSENT | 8-12 |
| fire | ABSENT | 7-10 |
| holy | WEAK | 7-10 |
| shadow | WEAK | 7-10 |
| wind | ABSENT | 6-9 |
| water | ABSENT | 5-8 |
| earth | ABSENT | 5-8 |
| **TOTAL** | **uniformly thin** | **~45-67** |

### 4.4 MODERN findings of note (cross-reference)

Per WS2.P1 § 7.2 "modern-caster IS a missing substrate AXIS" empirical claim: the substrate cell-coordinate (`attribute=INT/WIS × register=fantasy × period=fictional × naming=sci-fi-modern`) is genuinely unoccupied. This is the structural finding that anchors MODERN Phase 2 scope at the upper-medium range per WS2.P1 § 5.

---

## 5. Cross-period patterns

### 5.1 Pattern 1 — Coverage asymmetry across periods

**ANCIENT is the strongest period (117 magic-weapon rows / 7 primaries = avg 17/primary).**
**MEDIEVAL is moderately thin (37 / 7 = avg 5/primary).**
**MODERN is uniformly thin (1 strong + 45 fantasy-fictional-modern-coded / 7 = avg 7/primary, but no genuine modern-caster).**

The asymmetry reflects substrate-curation history: the 2026-05-22 Cycle 8 hive-mind weapon-substrate cycle plus subsequent enrichment passes targeted historical / mythological / fantasy-ARPG coverage. Modern-caster was implicitly out-of-scope at that cycle (per WS2.P1 § 7.2). Bronze-Age and Antiquity mythological canon got prioritized through enrichment passes; medieval received less attention.

### 5.2 Pattern 2 — Fire and water are uniformly thin across all 3 periods

Fire and water are the **weakest primaries cross-period**, with the audit finding:
- fire ANCIENT WEAK (3) / MEDIEVAL WEAK (2) / MODERN ABSENT (0 strong)
- water ANCIENT WEAK (5) / MEDIEVAL WEAK (2) / MODERN ABSENT (0 strong)

**Hypothesis:** fire and water are mostly expressed in the substrate as DEX-coded military hardware (flamethrowers, depth charges, naval cannons) or STR-coded melee (Sword of Freyr, Poseidon's Trident). Caster-class fire/water implements at any period are under-represented across the substrate's curation history.

Phase 2 should prioritize fire and water across ALL THREE periods at higher anchor count (3-5 per cell) than the average (2-3 per cell).

### 5.3 Pattern 3 — Earth and holy are best-backed cross-period

Earth and holy are the strongest primaries cross-period:
- earth ANCIENT STRONG (38) / MEDIEVAL MEDIUM (13) / MODERN ABSENT (0)
- holy ANCIENT STRONG (30) / MEDIEVAL MEDIUM (11) / MODERN WEAK (~26 fantasy-fictional)

**Hypothesis:** crystal / stone / obsidian (earth) and radiance / divine / sacred (holy) vocabulary have the broadest substrate coverage in fantasy-ARPG and mythological-canon sources. WoW-classic-items, Vedic mythological canon, and Solomonic grimoires all contribute.

Phase 2 anchor scope for earth and holy can be at the LOWER end (1-2 per ANCIENT cell, 2-3 per MEDIEVAL cell).

### 5.4 Pattern 4 — Shadow has period-asymmetric coverage

Shadow is MEDIUM ANCIENT (13 — wow-fantasy-classical), ABSENT MEDIEVAL (1 — Charlemagne talisman only), WEAK MODERN (8 fantasy-fictional sci-fi). The MEDIEVAL gap is the **single worst cell in the audit** for a cross-period primary that has ANCIENT and MODERN backing.

**Hypothesis:** the substrate lacks medieval-necromancer / witch / sorcerer-class implements as a curated cohort. Solomonic grimoires (currently tagged holy) could be retro-split into shadow grimoires for necromantic / demonic-tradition entries (Munich Manual of Demonic Magic, Sefer HaRazim, Ars Goetia all read as shadow-coded).

Phase 2 should prioritize MEDIEVAL.shadow at higher anchor count (5-6 per cell) — the biggest single-cell gap.

### 5.5 Pattern 5 — Manually-authored substrate exists but is sparse

Across 21 cells:
- ANCIENT manually-authored: 21 rows (most concentrated in lightning 7 + holy 8)
- MEDIEVAL manually-authored: 6 rows (Moctezuma family + Roland family)
- MODERN manually-authored: 0 rows (per WS2.P1)

The manually-authored corpus (per `engine_authored_gap_fill_v1` + `legolas_crawl_substrate_enrichment_v1_2026_05_27`) is the structural template for Phase 2 anchor authoring. Per WS2.P1 § 4.1 + § 5.3: the operational pattern is rocket-authors-skill-kit + gandalf-curates-cultural-tradition + star-lord-cohesion-coalescence + jack-ryan-Gate-2.

---

## 6. Phase 2 gap-fill scope recommendation

### 6.1 Y3 hybrid CONFIRMED across all 3 periods

Per dispatch § 2.4 + IA-2 queue § Phase 2: gandalf manual-authoring + legolas catalogue-crawl supplementary Y3 hybrid. Audit confirms the hybrid is needed across all 3 periods.

### 6.2 Per-cell anchor-authoring scope recommendation

| Primary | ANCIENT anchors | MEDIEVAL anchors | MODERN anchors (per WS2.P1) | Per-primary total |
|---|---:|---:|---:|---:|
| fire | 3-5 | 3-5 | 7-10 | 13-20 |
| water | 3-5 | 3-5 | 5-8 | 11-18 |
| earth | 1-2 | 2-3 | 5-8 | 8-13 |
| wind | 2-3 | 4-5 | 6-9 | 12-17 |
| lightning | 2-3 | 3-4 | 8-12 | 13-19 |
| holy | 1-2 | 2-3 | 7-10 | 10-15 |
| shadow | 3-4 | 5-6 | 7-10 | 15-20 |
| **TOTAL** | **15-24** | **22-31** | **45-67** | **82-122** |

### 6.3 Gandalf manual-authoring vs legolas catalogue-crawl split per cell

**Gandalf manual-authoring (Y3 anchor authoring) — recommended where:**
- Named-mythological-bearer anchors are needed (e.g., Vedic Astras, Aztec deity-named, Carolingian Joyeuse-family)
- Cross-cultural diversification is needed (e.g., Slavic Perun lightning, Egyptian Ra holy)
- The cell has named-canonical inventory that crawl-extraction wouldn't reliably surface

**Legolas catalogue-crawl (Y3 supplementary) — recommended where:**
- Pattern-broad coverage is needed (e.g., medieval grimoire-canon, alchemist focus families)
- Existing libraries (osrsbox / wow-classic-items / nick-aschenbach-dnd-data) have systematic-extension surfaces
- Vocabulary-coverage rather than identity-coverage is the gap

**Per-cell Y3 split recommendation:**

| Cell | Gandalf anchors | Legolas crawl supplementary | Rationale |
|---|---:|---:|---|
| ANCIENT.fire | 3-4 | 1 | Vedic Agni / Aztec Xiuhcoatl / Greek Hephaestus named anchors (manual); Vedic / Egyptian fire-implement crawl supplementary |
| ANCIENT.water | 3-4 | 1 | Varuna / Tlaloc / Lir / Manannan named anchors (manual); Celtic / Vedic water-implement crawl supplementary |
| ANCIENT.earth | 1 | 1 | Prithvi / Gaia / Geb named anchor (manual); WoW + osrsbox earth-crystal expansion (crawl) |
| ANCIENT.wind | 2 | 1 | Stribog / Aeolus / Shu named anchors (manual); cross-cultural wind-implement crawl |
| ANCIENT.lightning | 2 | 1 | Perun / Raijin / Tlaloc-lightning named anchors (manual); cross-cultural lightning crawl |
| ANCIENT.holy | 1 | 1 | Ra / Quetzalcoatl named anchor (manual); Buddhist staff-tradition crawl |
| ANCIENT.shadow | 3 | 1 | Hades / Anubis / Yama / Kali named anchors (manual); underworld-deity-implement crawl |
| MEDIEVAL.fire | 3 | 2 | Witch-flame / alchemist fire-rod anchors (manual); Crusader-era enchanted-flame crawl |
| MEDIEVAL.water | 3 | 2 | Witch-storm / alchemist-mercury / hydromancer anchors (manual); medieval-water-rite crawl |
| MEDIEVAL.earth | 2 | 1 | Witch-stone-circle / alchemist-metallurgy anchors (manual); medieval-stone-relic crawl |
| MEDIEVAL.wind | 4 | 1 | Aeolian harp / witch-storm-staff / alchemist-bellows / named-wind anchors (manual); medieval-wind-rite crawl |
| MEDIEVAL.lightning | 3 | 1 | Crusader-era thunder-focus / Slavic Perun-medieval anchors (manual); medieval-lightning-rite crawl |
| MEDIEVAL.holy | 2 | 1 | Reliquary / saint-relic / monk-stave anchors (manual); Crusader/papal artifact crawl |
| MEDIEVAL.shadow | 5 | 1 | Necromancer-grimoire / witch-shadow / undead-named anchors (manual; LARGEST single-cell anchor scope); Munich Manual-style crawl |
| MODERN (all 7) | per WS2.P1 § 5.2 | per WS2.P1 § 5.2 | WS2.P1 recommendation in full; ~45-67 weapons; `nick-aschenbach-dnd-data` sci-fi templates inform anchor naming |

**Aggregate Y3 split estimate:**
- **Gandalf anchor authoring:** ~37-43 ANCIENT/MEDIEVAL + ~30-45 MODERN per WS2.P1 = ~67-88 anchor weapons
- **Legolas catalogue-crawl supplementary:** ~12 ANCIENT/MEDIEVAL + ~10 MODERN = ~22 supplementary entries
- **Total Phase 2:** ~89-110 weapons (gandalf 67-88 + legolas 22)

This is broader than the dispatch's ~45-80 estimate (which was anchored on MODERN-only). Audit recommends Phase 2 scope-mid-range of **~80-100 weapons** as the practical commitment, with the upper-bound of ~110 reserved for v1.1+ extension if Phase 2 reveals MODERN demands the full WS2.P1 estimate.

### 6.4 Methodology recommendation — retroactive primary-tagging for primary-unattributed magic-weapon pool

A SEPARATE methodology question: 509 ANCIENT and 60 MEDIEVAL magic-weapon-eligible substrate rows lack primary-element vocabulary in canonical_name. Many of these are interpretable to a specific primary:
- Solomonic grimoires (Key of Solomon, Picatrix, Lesser Key) → shadow + holy split
- Mongol banners (Raven Banner, Oriflamme, White Banners) → wind + earth split
- Hermetic instruments (Caduceus, Wedjat eye, Ankh) → holy (already partial coverage)
- Egyptian Ankh / Scarab Amulet → holy
- Norse mythological named weapons (Mjölnir, Gungnir, Gram, Tyrfing) → lightning + earth + shadow

**Recommend:** at IA-2 Phase 3 (elrond ingest + lineage tag application), supplement Phase 2's freshly-authored entries with a **retroactive-primary-tagging pass** for the existing primary-unattributed magic-weapon pool. This would amount to ~50-100 retroactive primary tags applied to existing crawl-extracted entries (e.g., `Sefer HaRazim` tagged as shadow-primary with holy-flex; `Key of Solomon` tagged as shadow-primary with holy-flex).

This is a Phase 3 methodology amendment and NOT in scope for the Phase 1 audit's core deliverable. Surfaced here for gandalf + Matt consideration at Phase 2 plan-shape decision.

### 6.5 Cycle 10 Stage 3.5 operational template (proven; reuse)

Per WS2.P1 § 5.3: Phase 2 should follow the established Cycle 10 Stage 3.5 pattern:
- **rocket** authors engine-side skill kit for each weapon (mechanical profile)
- **gandalf** curates cultural-tradition / lore / naming per period
- **star-lord** runs Phase 5 cohesion-coalescence LLM calls (if needed for naming)
- **jack-ryan** Gate-2 sim-viability per gap-fill per T4-A § 3.3 step 5

Per-entry schema must populate (per `weapon-substrate-composition-policy-v1-2026-05-24.md` § 9.3): canonical_name + description_text + structured_properties + register_canonical + historical_period_canonical + cultural_lineage_canonical + proxy_attribute_class + proxy_range_class + proxy_geometry_class + proxy_tempo_class + quality_tier + lineage tag.

New lineage tag values for IA-2 (per dispatch § 9 / queue § IA-2 Phase 3):
- `gandalf-authored-magic-anchor-ancient-2026-06-XX`
- `gandalf-authored-magic-anchor-medieval-2026-06-XX`
- `gandalf-authored-magic-anchor-modern-2026-06-XX`
- `legolas-crawl-magic-supplementary-ancient-2026-06-XX`
- `legolas-crawl-magic-supplementary-medieval-2026-06-XX`
- `legolas-crawl-magic-supplementary-modern-2026-06-XX`
- (Optional retroactive tag) `elrond-retroactive-primary-tag-ancient-medieval-2026-06-XX`

---

## 7. Audit limitations

1. **Keyword-only scan over canonical_name + named_mythological_match + structured_properties.** Magic-weapon identity expressed through OTHER vocabulary undercounted. Audit reports a CONSERVATIVE FLOOR.
2. **Description text un-scanned.** A weapon with generic name but magic-weapon-establishing description text uncounted. A deeper Mode A pass over description_text would surface 10-30 additional candidates per period.
3. **Embeddings un-queried.** `text_embedding` BLOB column not used. Semantic-similarity sweep against magic-weapon prototypes would surface non-keyword-matched candidates. Deferred to Phase 4 validation pass.
4. **WoW-classic-items period-misclassification.** 3,149 wow-classic-items rows are classified `historical_period_canonical = classical`. They are in-game-lore pre-industrial fantasy. ANCIENT.fantasy counts include this category. Downstream consumers should be aware.
5. **Early-modern (14,549 rows) held out of scope.** If Hattori Hanzō / Yagyū / Edo-period esoteric weapons need first-class IA-2 coverage, a supplementary Phase 1.5 audit pass would be needed.
6. **Period boundaries audit-internal.** ANCIENT = pre_classical + classical is the audit's operational boundary; alternate framings (e.g., ANCIENT = pre_classical only; classical = ANTIQUITY separate cell) would shift counts. Audit chose the inclusive boundary for substrate-realism.
7. **Primary-element keyword vocabulary is audit-internal.** ANCIENT/MEDIEVAL keywords (per § 1.4) draw from Q18 lock + mythological-canon vocabulary; alternate vocabulary frames (e.g., including more obscure or vernacular terms) might surface 10-20 additional entries per primary. Audit's vocabulary is the conservative-floor inclusion.
8. **MODERN reused-by-reference.** MODERN cell data is per WS2.P1 audit; NOT re-derived against current 90,220-row substrate. WS2.P1 substrate base was 90,220 at audit date (2026-06-01); current substrate base is 90,220 (consistent).
9. **Primary-unattributed magic-weapon pool not enumerated per primary.** § 6.4 notes ~509 ANCIENT + 60 MEDIEVAL primary-unattributed rows exist; specific per-primary retroactive-tagging recommendations are NOT in scope. Phase 3 ingest methodology consultation needed if retroactive-tagging is pursued.
10. **Lineage-tag heuristic.** `source_library` → manually-authored vs crawl-extracted per WS2.P1 § 1.3. Phase 3 ingest may want to formalize this.

---

## 8. Notable findings to surface to Knight-rider

### 8.1 Audit broadens but does NOT fundamentally alter Phase 2 scope shape

Per dispatch § 4 escalation criterion ("if your audit surfaces evidence that fundamentally changes IA-2 Phase 2 scope shape... surface to KR via report-back"):

**Audit does NOT surface evidence requiring Matt + gandalf re-engagement on Phase 2 scope shape.** Audit BROADENS the per-period scope (~82-122 weapons recommended vs ~45-80 dispatch estimate) but the Y3 hybrid path + per-cell methodology + operational template are unchanged. Phase 2 can proceed at the audit's recommended ~80-100 mid-range commitment with KR/Matt routing of the broadening for Matt awareness.

### 8.2 Coverage-asymmetry pattern is the audit's load-bearing finding

ANCIENT (117) > MEDIEVAL (37) > MODERN (~46) is the substrate's empirical state. Phase 2 anchor-authoring per period should be sized to the gap, not uniform — MEDIEVAL needs deeper anchor count (22-31) than ANCIENT (15-24) despite MEDIEVAL having a smaller period base.

### 8.3 Fire and water are uniformly thin cross-period (Pattern 2)

Fire and water are the weakest primaries at every period — substrate has DEX-coded military / STR-coded melee saturation but caster-class implements at any period are under-represented. Phase 2 should prioritize fire/water at higher per-cell anchor count.

### 8.4 MEDIEVAL.shadow is the single worst cell

ABSENT (1 row only — Talisman of Charlemagne). 5-6 anchor weapons recommended — the highest single-cell anchor scope. Necromancer-grimoire / witch-shadow / undead-named-bearer authoring needed.

### 8.5 Retroactive-primary-tagging methodology candidate for Phase 3

§ 6.4 surfaces the 509 ANCIENT + 60 MEDIEVAL primary-unattributed magic-weapon-eligible substrate pool. Phase 3 elrond ingest could amend methodology to retroactively-tag these entries with primary-element associations (~50-100 retroactive tags). This is NOT a Phase 1 audit recommendation — surfaced for gandalf + Matt Phase 2 plan consideration.

### 8.6 INFO items confirmation (per jack-ryan Gate-1)

- **INFO-1:** physical excluded by design (Architecture-A taxonomy-sibling). CONFIRMED in § 1.1.
- **INFO-2:** 19 designer-curation-modern-scientific-overlay entries are MODERN primary target. CONFIRMED in § 4.2 + cross-reference to WS2.P1 § 7.2.
- **INFO-3:** per-period operational criteria explicitly defined in § 1.3. CONFIRMED.

---

## 9. Cross-references

### Composes with (existing canon)

- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (7 rotating primaries + 19 modern-scientific overlay; this audit's primary-vocabulary anchor)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 6 (substrate dependency summary; this audit composes with the per-period-coordinate)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 9 (Stage 3.5 gap-fill pattern)
- `agentic_orchestration/elrond/audits/2026-06-01-modern-caster-substrate-coverage-audit.md` (WS2.P1; MODERN data REUSED)
- `agentic_orchestration/qa/findings/2026-06-01-ia-2-phase-1-gate-1.md` (jack-ryan Gate-1 PASS-with-INFO + 3 INFO items absorbed)

### Authorizes downstream

- **IA-2.P2** Gandalf + legolas Y3 hybrid gap-fill — ~80-100 weapons recommended; per-cell scope per § 6.2 + § 6.3
- **IA-2.P3** Elrond ingest + lineage tag application — including potentially retroactive-primary-tagging methodology per § 6.4
- **IA-2.P4** Substrate-coverage validation pass — re-run this audit's query post-ingest; confirm verdict-shift per cell

### Does NOT replace or amend

- 90,220-row weapon substrate (PRESERVED; audit is read-only)
- WS2.P1 modern-caster substrate-coverage audit (PRESERVED; this audit composes by reference for MODERN cells)
- pool.json v1.1 canonical lock (PRESERVED; this audit informs downstream substrate authoring)

### Audit script (reproducibility)

`agentic_orchestration/research/scripts/ia2_phase1_magic_weapons_across_periods_audit.py` — Python 3 read-only query. Re-runs produce deterministic output; reflect substrate updates if any.

---

## 10. Sign-off

**Author:** elrond (data steward seam)
**Authority chain:**
- Matt 2026-06-01 strategic reset directive (transmitted via gandalf Pattern B reframe)
- jack-ryan IA-2 Phase 1 Gate-1 PASS-with-INFO 2026-06-01 (fire authorization)
- Elrond seam authority on Mode A audit query design + substrate-lineage interpretation + per-cell gap-quantification methodology + Y3 hybrid recommendation per cell (per dispatch § 5 + jack-ryan Gate-1 § 4.5)

**Status:** CURRENT — Phase 1 audit COMPLETE. Phase 2 / Phase 3 / Phase 4 HELD pending Matt + gandalf direction per dispatch § 8 out-of-scope block.

**Routing back to KR:** Audit ready for Matt + gandalf Phase 2 plan. Audit broadens recommended scope to ~80-100 weapons (vs dispatch ~45-80) and surfaces a retroactive-primary-tagging methodology candidate for Phase 3 consideration. Y3 hybrid path + operational template are unchanged.

**Disciplines composed:**
- Discipline #41 (substrate-led) — audit grounds Phase 2 scope in empirical substrate evidence per period × primary
- Discipline #42 (framing-audit) — § 6.4 surfaces the primary-unattributed magic-weapon pool transparently rather than counting through it
- Discipline #18 (math-hotspot methodology consultation) — per-period operational criteria documented explicitly for reproducibility per jack-ryan INFO-3
- Discipline #25 (semantic-layer rep-audit / marginal-lineage tagging) — § 4 + § 6.3 lineage findings preserved for downstream Phase 3

---

**End of IA-2 Phase 1 magic-weapons-across-periods substrate-coverage audit.**

---

## Completion record

**Completed:** 2026-06-01
**Audit artifact:** `agentic_orchestration/elrond/audits/2026-06-01-magic-weapons-across-periods-audit.md`
**Audit script:** `agentic_orchestration/research/scripts/ia2_phase1_magic_weapons_across_periods_audit.py`

**21-cell coverage grid:**

| Primary | ANCIENT | MEDIEVAL | MODERN |
|---|---|---|---|
| fire | WEAK (3) | WEAK (2) | ABSENT (per WS2.P1) |
| water | WEAK (5) | WEAK (2) | ABSENT (per WS2.P1) |
| earth | STRONG (38) | MEDIUM (13) | ABSENT (per WS2.P1) |
| wind | MEDIUM (10) | WEAK (2) | ABSENT (per WS2.P1) |
| lightning | MEDIUM (16) | WEAK (6) | WEAK (per WS2.P1) |
| holy | STRONG (30) | MEDIUM (11) | WEAK (per WS2.P1) |
| shadow | MEDIUM (13) | ABSENT (1) | WEAK (per WS2.P1) |

**Per-period gap quantification:**
- ANCIENT: 117 magic-weapon rows; Phase 2 anchor scope ~15-24 weapons
- MEDIEVAL: 37 magic-weapon rows; Phase 2 anchor scope ~22-31 weapons
- MODERN: ~46 fantasy-fictional-modern-coded; Phase 2 anchor scope ~45-67 per WS2.P1

**Phase 2 scope recommendation:** ~80-100 weapons mid-range (gandalf 67-88 anchors + legolas 22 supplementary); Y3 hybrid confirmed; per-cell split per § 6.3.

**Audit limitations / blind spots:**
- Keyword-only scan; description text + embeddings un-queried
- WoW-classic-items period-misclassification at classical (inflates ANCIENT.fantasy)
- Early-modern period held out of scope
- MODERN reused-by-reference; not re-derived
- Primary-unattributed magic-weapon pool (~569 rows ANCIENT+MEDIEVAL) not per-primary-classified

**Notable findings:**
- Coverage asymmetry: ANCIENT >> MEDIEVAL ≈ MODERN — Phase 2 anchor scope should be sized to gap, not uniform
- Fire and water uniformly thin cross-period — substrate has DEX-coded military + STR-coded melee saturation, caster-class fire/water under-represented at every period
- MEDIEVAL.shadow is single worst cell (1 row); requires highest per-cell anchor scope (5-6)
- 509 ANCIENT + 60 MEDIEVAL primary-unattributed magic-weapon-eligible substrate rows exist — Phase 3 retroactive-primary-tagging methodology candidate surfaced for Matt + gandalf consideration

**Routing back to KR:** report ready for Matt + gandalf Phase 2 plan. Audit broadens scope mid-range to ~80-100 weapons; surfaces retroactive-primary-tagging methodology candidate; Y3 hybrid + operational template unchanged.
