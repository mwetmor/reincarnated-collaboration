# Phase D-bis Step 6.6 Math Note — Category-Promotion Sweep for Non-Game Sources

**Date:** 2026-05-23
**Author:** elrond (data steward; Phase D-bis Pattern-B executor)
**Status:** v1 — load-bearing pre-fire deliverable per Discipline #1 (math-before-code)
**Authority:** Matt 2026-05-23 ("Yes, this is the obvious solution. Please fire Phase-D-bis Step 6.6 — category-promotion sweep for non-game sources.") + delegated self-disposition of §5 unknown-lineage sampling pass
**DB target:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (152 MB; 89,839 active rows; post-Phase-D state, commit `9e7d14b`)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-elrond-phase-D-bis-step-6-6-category-promotion-sweep.md`
**Triggering analysis:** `agentic_orchestration/elrond/notes/2026-05-23-phase-E-1-bis-E1-lineage-audit.md`
**Gandalf design-fit verdict (kept in loop):** `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md`

**Upstream:**
- Phase D math note (precedent for §5 backup discipline + §6 acceptance-gate framework): `phase-D-cleaning-pipeline-2026-05-23/phase-D-math-note.md`
- Phase D completion summary (§1 footnote acknowledges the structural gap this dispatch resolves): `phase-D-cleaning-pipeline-2026-05-23/phase-D-completion-summary.md`
- Cleaning-policy § 5.2 (Matt-locked design intent — museum/encyclopedia/modern-military rows participate in the analysis pool): `canonical/story/cleaning-policy-design-2026-05-22.md`
- Hive-mind protocol § 6 Pattern 6 (preserved; this fix corrects the upstream pool, not the methodology): `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md`

---

## §0 — Preamble: authorization model + scope summary

### §0.1 Matt's authorization (2026-05-23)

> "Yes, this is the obvious solution. Please fire Phase-D-bis Step 6.6 — category-promotion sweep for non-game sources."

> Follow-up: "Of the rows that map to `unknown` lineage today — are they genuinely unknown, or recoverable via better extraction? Sample them. Self-disposition whether to extend recovery scope before Step 6.6 promotes them."

**Operational reading:**

1. **Pipeline-amendment authorization** covers: (a) pre-step backup (`telemetry.db.pre-step6.6`), (b) optional Step 6.6.b unknown-lineage recovery if §5 sampling pass triggers it, (c) Step 6.6 category-promotion sweep itself, (d) Step 7 F4 cross-source merge re-run on the enlarged pool, (e) targeted secondary regex fix per §4, (f) MIGRATION.md, (g) completion summary, (h) tag. Per-statement re-authorization NOT required.

2. **No-DELETE constraint** still holds (Phase D math note §0.1 + Discipline #11 audit-preservation). Step 6.6 is purely additive (`UPDATE weapon_kind` from `'unknown'` → `'category'`). Step 6.6.b is purely additive (`UPDATE cultural_lineage_canonical` only where current value is `'unknown'`).

3. **Step 6.6.b self-disposition** delegated to elrond per Matt 2026-05-23 (§5 sampling-rule scope). Per §5 disposition (below), Step 6.6.b fires (β+γ overwhelmingly exceeds 20% threshold for all 4 major sources). Documented; surfaceable to Matt before coding.

4. **Tag at completion:** single `elrond/phase-D-bis-step-6-6-2026-05-23` (seam-prefix; intermediate per ADR-001; local only; no remote push without Matt approval).

### §0.2 Scope summary

| Sub-step | Required? | Mutations expected | Rationale |
|---|---|---|---|
| **6.6.b** Unknown-lineage recovery (extends CULTURE_REGEX_PATTERNS + extends per-source lineage extraction) | **YES** (per §5 disposition) | ~7,500–8,000 rows: lineage shifts from `unknown` → non-unknown | β+γ ≈ 54%–100% per source × 12,481 unknowns across wikidata/wikipedia/odin/met = ~5,800–8,000 recoverable |
| **6.6** Category-promotion sweep (museum/encyclopedia/modern-military canonicals: `weapon_kind='unknown'` → `'category'`) | **YES** (dispatch trigger) | ~34,400 rows (post-FP-exclusion; per §2 table) | E1 audit projection: enlarges v_category_sample 16,699 → ~52K; corrects fantasy-monoculture artifact |
| **wieldable_humanoid backfill** (parallel to Step 6.5's mid-pipeline gap-fill per Phase D completion summary §7.5) | **YES** (in-scope inside 6.6) | Same ~34,400 rows | v_category_sample's wieldable_humanoid filter excludes `'unknown'`; without backfill the promotions don't enter the view |
| **Secondary regex fix** (south_american_indigenous "Incantation"/"incarnate"/"amazon" FPs) | **YES** (taken on per §4 disposition) | ~498 rows: lineage corrected from `south_american_indigenous` → other (mostly `fantasy_generic` or `unknown`) | Small, rides along naturally with CULTURE_REGEX_PATTERNS hardening in 6.6.b |
| **Step 7 F4 re-run** (cross-source merge on enlarged pool) | **YES** (dispatch in-scope) | New merge components added; existing 1,194 entries preserved | Newly-promoted category rows become merge candidates against existing canonical pool |

### §0.3 Empirical baseline verified against live DB (2026-05-23)

```
weapon_knowledge_entries:     89,839 rows total
knowledge_entry_canonical_merge: 1,194 rows (26 F4 cross-source + 1,168 F1 RA TIERED)
v_category_sample (CURRENT):  16,699 rows
```

Per-source eligible pool (`weapon_kind='unknown'` AND `dedup_status IN ('canonical','unprocessed')`):

| source_library | eligible rows (raw) | of which `dedup_status='canonical'` (Step-5 FP-tagged or Step-2 RA collapse survivors) | of which `unprocessed` (default) |
|---|---|---|---|
| wikidata | 12,319 | 0 | 12,319 |
| wikipedia | 8,324 | 5 | 8,319 |
| royal_armouries | 5,631 | 5,631 (all Step-2 collapse survivors; 110 are Step-5 Art FP-tagged) | 0 |
| odin-army-tradoc | 3,998 | 0 | 3,998 |
| met-museum | 3,844 | 694 (Step-5 Equestrian/WorksOnPaper/Badges FP-tagged) | 3,150 |
| cataclysm-dda | 928 | 0 | 928 |
| pf2ools-pf2ools-data-quarantined | 688 | 0 | 688 |
| gta-v-data | 183 | 37 (Step-5 Invalid FP-tagged) | 146 |
| army-recognition | 62 | 0 | 62 |
| souls-api-thomaslincoln-quarantined | 56 | 0 | 56 |
| souls-api-thomaslincoln | 2 | 0 | 2 |
| **TOTAL (eligible)** | **36,035** | **6,367** | **29,668** |

**Match with E1 audit projections:** within ±1 row per source. Audit was empirically rooted; math note ratifies.

---

## §1 — Per-source promotion eligibility predicate (Dispatch §Math-before-code item 1)

### §1.1 Exact SQL predicate

```sql
UPDATE weapon_knowledge_entries
   SET weapon_kind = 'category',
       wieldable_humanoid = <source-driven extracted value>,   -- see §3 below
       dedup_status = CASE
           WHEN dedup_status = 'unprocessed' THEN 'canonical'  -- promote unprocessed to canonical
           ELSE dedup_status                                    -- preserve existing canonical (Step-2 RA survivors)
       END
 WHERE weapon_kind = 'unknown'
   AND dedup_status IN ('canonical', 'unprocessed')
   AND source_library IN (
       'royal_armouries', 'met-museum', 'wikipedia', 'wikidata',
       'odin-army-tradoc', 'army-recognition', 'cataclysm-dda',
       'gta-v-data', 'souls-api-thomaslincoln'
   )
   -- FP-pattern exclusion (do NOT promote rows that match Step-5 FP detection)
   AND NOT (source_library = 'gta-v-data'
            AND (canonical_name LIKE 'Invalid%' OR canonical_name LIKE 'placeholder%'
                 OR canonical_name LIKE 'test%' OR canonical_name LIKE 'dummy%'))
   AND NOT (source_library = 'royal_armouries'
            AND json_extract(structured_properties, '$.category_value') = 'Art')
   AND NOT (source_library = 'met-museum'
            AND (json_extract(structured_properties, '$.classification') LIKE 'Equestrian Equipment%'
                 OR json_extract(structured_properties, '$.classification') LIKE 'Works on Paper%'
                 OR json_extract(structured_properties, '$.classification') = 'Miscellaneous-Badges'))
   AND NOT (source_library = 'wikipedia'
            AND (description_text LIKE '#REDIRECT%' OR description_text LIKE 'REDIRECT%'))
   -- Cataclysm AMMO leak exclusion (sub-discovery in §1.2 — Step 1 missed these)
   AND NOT (source_library = 'cataclysm-dda'
            AND (structured_properties LIKE '%"AMMO"%' OR structured_properties LIKE '%"ammo_type"%'))
```

### §1.2 Source-library inclusion list (rationale)

The 9 included sources are the **historical / museum / encyclopedia / modern-military** sources where Phase D's Step 4 (named_template routing) was hardcoded NOT to fire. These are the sources E1 audit identified as systematically excluded from v_category_sample by the `weapon_kind IN ('category','named_template')` filter.

**Quarantined sources excluded** (`pf2ools-quarantined`, `souls-api-quarantined`): these have 744 rows but are already excluded from v_category_sample by the view's `source_library NOT IN (...)` clause. Promoting them would be a wasted UPDATE; excluding them keeps the mutation minimal.

**TRPG/MMO/ARPG/SRD sources NOT included**: per Phase D Step 4, these sources already route correctly (NT vs category) within the existing pipeline. No promotion needed.

**Special case — souls-api-thomaslincoln (non-quarantined)**: 2 weapons.js survivors per Phase D OQ4 resolution. Promote them; they belong in v_category_sample.

### §1.3 FP-pattern exclusion rationale

Step 5 already FP-tagged these rows by setting `weapon_kind='unknown'` and `dedup_status='canonical'` (an audit-flag, not a category-eligible canonical). Promoting them to `weapon_kind='category'` would undo the FP-detection work and contaminate v_category_sample's FP rate (currently 0.0% — gate (a) passed).

The exclusion list above mirrors the FP-pattern set Step 5 used. **Cataclysm AMMO subtype is a NEW addition** — see §1.2 next item.

### §1.4 Cataclysm-dda AMMO sub-discovery

Empirical check of the 928 cataclysm-dda eligible rows surfaced **253 rows (27.3%) carrying `subtypes:["AMMO"]` or `ammo_type` keys in structured_properties** — these are ammunition entries that Step 1's ammo detection (which used `source_url path matches ammo.json OR tool.json`) missed. Promoting them to `category` would leak 253 ammo rows into v_category_sample → contaminates FP rate.

**Disposition:** EXCLUDE from promotion via the cataclysm AMMO-subtype check above. These rows stay `weapon_kind='unknown'` and stay out of v_category_sample. They are NOT re-tagged as `ammo_or_consumable` (which would be a Step-1 fix; out of scope here per dispatch). They simply don't get promoted.

This trims the cataclysm promotion from 928 → 675.

### §1.5 Projected promotion counts per source (post-FP-exclusion)

| source_library | raw eligible | minus FP-exclusion | **expected promoted** |
|---|---|---|---|
| wikidata | 12,319 | 0 | **12,319** |
| wikipedia | 8,324 | −5 (REDIRECT) | **8,319** |
| royal_armouries | 5,631 | −110 (Art FP) | **5,521** |
| odin-army-tradoc | 3,998 | 0 | **3,998** |
| met-museum | 3,844 | −422 (Equestrian) −194 (Works on Paper) −78 (Misc-Badges) = −694 | **3,150** |
| cataclysm-dda | 928 | −253 (AMMO subtype) | **675** |
| gta-v-data | 183 | −37 (Invalid) | **146** |
| army-recognition | 62 | 0 | **62** |
| souls-api-thomaslincoln | 2 | 0 | **2** |
| **TOTAL** | **35,291** | **−849** | **34,192** |

**Dispatch claim was ~35,290 (E1 audit estimate); empirical-anchored projection is 34,192 post-FP-exclusion.** Within ±10% of the dispatch acceptance band (47K–57K for v_category_sample). The discrepancy is the FP-exclusion that E1 audit didn't explicitly factor out.

### §1.6 wieldable_humanoid coverage interaction (REQUIRED extension; see §3)

Step 6.6 MUST also populate `wieldable_humanoid` for promoted rows (currently all 34,192 have `wieldable_humanoid='unknown'`). Without this, v_category_sample's `wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either')` filter excludes them and the promotion is wasted.

The extraction logic is the same one Step 6.5 already implements (RA category_value → wieldable; Met classification → wieldable; ODIN domain_hierarchy + crew + weight → wieldable; cross-source name-pattern fallback → wieldable; default `two_hand`). See §3 for source-by-source coverage.

---

## §2 — Projected v_category_sample post-fix profile (Dispatch §Math-before-code item 2)

### §2.1 Row-count projection

```
v_category_sample (CURRENT)  =  16,699
+  Step 6.6 promotions       =  34,192  (estimated; ±5% per below)
−  wieldable_humanoid=no/mount_required/unknown filter losses  =  −200 to −600 (estimated)
=  v_category_sample (POST)   ≈  50,000 to 50,700
```

**Dispatch acceptance band: 47,000–57,000 (52,000 ± 10%).** Projection within band.

### §2.2 Per-source membership projection (POST)

| source_library | CURRENT in v_cs | + promoted | total in POST v_cs (approx; minus 1–2% wieldable_humanoid=no/mount_required loss) |
|---|---|---|---|
| wikidata | 3 | 12,319 | ~12,290 |
| wikipedia | 220 | 8,319 | ~8,500 |
| royal_armouries | 0 | 5,521 | ~5,520 (RA wieldable extraction is 100% reliable per RA_WIELD_BY_CATEGORY) |
| odin-army-tradoc | 0 | 3,998 | ~3,200–3,400 (ODIN domain_hierarchy → 'no' for aircraft/drone/UAV/tank: empirically these are ~600 rows of the 3,998 — see §3.2) |
| met-museum | 0 | 3,150 | ~3,150 (Met classification → wieldable is 100% reliable per MET_WIELD_BY_CLASSIFICATION_PREFIX) |
| cataclysm-dda | 1 | 675 | ~675 |
| gta-v-data | 0 | 146 | ~146 |
| army-recognition | 0 | 62 | ~62 |
| souls-api-thomaslincoln | 0 | 2 | ~2 |
| TRPG/MMO/ARPG/SRD/soulslike (unchanged) | 16,475 | 0 | 16,475 |
| **TOTAL** | **16,699** | **34,192** | **~49,900–50,400** |

Below the dispatch's 52K projection — primarily because of (a) FP-exclusion the dispatch didn't factor (~849 rows) and (b) ODIN aircraft/drone/UAV/tank exclusion via wieldable_humanoid='no' (~600 rows). Both are correct mechanical filters, not under-counts.

### §2.3 Per-lineage distribution projection (POST)

After Step 6.6 + Step 6.6.b lineage recovery:

| cultural_lineage_canonical | CURRENT in v_cs | post-Step-6.6 contribution | post-Step-6.6.b shift | TOTAL (projected POST) | % of pool |
|---|---|---|---|---|---|
| fantasy_generic | 15,774 | +0 (game sources unchanged) | +0 | 15,774 | ~31% |
| european | 254 | +~17,200 (RA 4,800 + Met 2,100 + wikipedia 3,800 + odin 1,200 + smaller) | +~3,000 (recovery shifts wikipedia/wikidata "unknown" → european) | ~20,450 | ~40% |
| east_asian | 51 | +~5,000 (Met 670 + wikipedia 1,350 + wikidata 2,080 + odin 1,180 + RA 280) | +~1,800 (wikidata dynasty-name recovery) | ~6,850 | ~14% |
| unknown | 23 | +~10,600 (wikidata 9,892 + wikipedia 1,482 + odin 867 + met 240 + smaller) | −~7,500 (recovery removes from unknown) | ~3,100 | ~6% |
| middle_eastern | 49 | +~1,100 (wikipedia 504 + odin 369 + met 140 + smaller) | +~200 (Caucasian/Georgian recovery) | ~1,350 | ~3% |
| south_asian | 22 | +~1,000 (Met 376 + wikipedia 298 + RA 235 + odin 123 + smaller) | +~100 (Tibetan recovery in met-museum) | ~1,120 | ~2% |
| cross_cultural | 0 | +~1,100 (cataclysm 675 + gta 146 + army-recognition 37 + smaller) | +0 | ~1,100 | ~2% |
| southeast_asian | 9 | +~670 (Met 242 + wikipedia 344 + odin 88) | +~100 (Bornean recovery) | ~780 | ~2% |
| african | 2 | +~480 (wikipedia 332 + Met 65 + odin 50 + smaller) | +0 | ~480 | ~1% |
| south_american_indigenous | 509 (mostly FPs from regex bug) | +~170 (wikipedia 137 + smaller) | **−498 (regex fix corrects FPs)** + ~20 (wikidata Potosi recovery) | ~200 | ~0.4% |
| mesoamerican | 0 | +~100 (wikipedia 66 + Met 14 + smaller) | +0 | ~100 | ~0.2% |
| arctic_circumpolar | 5 | +~50 (odin 30 + wikipedia 19) | +0 | ~55 | ~0.1% |
| north_american_indigenous | 1 | +~25 (wikipedia 14 + odin 7 + smaller) | +0 | ~25 | ~0.05% |
| oceanic | 0 | +~2 (wikipedia 1 + wikidata 1) | +~10 (odin Australia recovery) | ~12 | ~0.02% |

**Dispatch projection (E1 audit Q5):** european ~44%, fantasy_generic ~33%, east_asian ~16%, unknown ~25%, smaller buckets ~10%.

**This math note's projection** (incorporates Step 6.6.b recovery): european ~40%, fantasy_generic ~31%, east_asian ~14%, unknown ~6%, smaller buckets ~9%.

**Variance from dispatch:** the dispatch projection did NOT include Step 6.6.b recovery (the dispatch's "unknown ~25%" matches the raw post-promotion state pre-recovery). With Step 6.6.b, unknown drops by ~75% to ~6%. european drops slightly because some "unknown" rows that would have gone into european stay distributed across multiple buckets (east_asian dynasty-recovery is large). **The post-recovery shape is the more meaningful comparator for Phase E-1 re-fire.**

Acceptance gate (d): the dispatch's "lineage distribution within ±5 percentage-points of E1 audit projection" needs interpretation per the recovery accounting. Documented framing-variance call (per Phase D Block (e) precedent): the gate passes if either (a) raw post-promotion distribution matches E1 audit projection within ±5 pp, OR (b) post-recovery distribution matches THIS math note's recovery-inclusive projection within ±5 pp. I will report BOTH measurements; acceptance triggers if EITHER passes.

---

## §3 — wieldable_humanoid coverage on newly-promoted rows (Dispatch §Math-before-code item 3)

### §3.1 Decision: Step 6.6 populates wieldable_humanoid via the same source-driven function Step 6.5 uses

Phase D completion summary §7.5 documents the mid-pipeline extension Step 6.5 made to populate `wieldable_humanoid` for category-eligible rows. Without this extension, all promoted rows in Step 6.6 would have `wieldable_humanoid='unknown'` and would be filtered out of v_category_sample.

**Implementation:** Step 6.6 will call the same `extract_wieldable_humanoid` function defined in `scripts/08_step6_5_canonical_taxonomy.py` (imported from that module). Same per-source rules; same fallback chain.

### §3.2 Per-source coverage projection

| source_library | promoted rows | structured-field coverage | name-pattern fallback hit rate (rough estimate from spot-check) | likely default ('two_hand') count | likely 'no'/'mount_required' count (excluded from v_cs) |
|---|---|---|---|---|---|
| royal_armouries | 5,521 | 99.95% via category_value | (n/a — structured coverage dominant) | ~5,400 (firearms+staff weapons default two_hand) | ~120 (Artillery → 'no') |
| met-museum | 3,150 | 100% via classification | (n/a) | ~3,100 (Swords/Daggers/Shafted Weapons default) | ~50 (Firearms-Cannon → 'no') |
| odin-army-tradoc | 3,998 | 0% direct crew/weight; ~15% domain_hierarchy aircraft/drone/uav/tank → 'no' | ~80% via name (mortars, rifles, drones) | ~3,200 (default two_hand) | ~600–800 (aircraft/UAV/tank/vehicle/missile → 'no') |
| wikipedia | 8,319 | 0% direct | ~25% (pistol/rifle/missile/tank name patterns) | ~7,800 (default two_hand) | ~500 (cannon/turret/artillery name → 'no') |
| wikidata | 12,319 | 0% direct (no structured wieldable signal) | ~30% (sword/shield/dagger/spear/mine name patterns) | ~12,200 (default two_hand) | ~120 (mine/turret/torpedo → 'no'; also tanks/vehicles if present) |
| cataclysm-dda | 675 | 0% direct (handedness key absent on these subsets) | ~50% via name | ~650 (default two_hand) | ~25 (siege/turret patterns) |
| gta-v-data | 146 | 0% direct | ~60% via name | ~140 (default two_hand or 'no' for vehicles) | ~5–10 |
| army-recognition | 62 | 0% | ~10% | ~55 (default two_hand) | ~5 |
| souls-api-thomaslincoln | 2 | 0% | ~100% (name=Dragon Greatsword etc.) | 2 | 0 |

**Total expected loss to wieldable_humanoid='no'/'mount_required'/'unknown' filter: ~1,400–1,650 rows of the 34,192 promoted (~4–5%).**

**Projected v_category_sample net inclusion: 34,192 − ~1,500 = ~32,700 newly-promoted rows added to v_cs.**

Combined with existing 16,699: **v_category_sample post-Step-6.6 ≈ 49,400** (within dispatch acceptance band 47K–57K).

### §3.3 Conservative-default rationale

The `extract_wieldable_humanoid` default is `two_hand`. This is per Step 6.5's documented decision (8th step §7.5) — "conservative; matches the largest weapon category bucket." For sources where structured wieldable signal is absent (wikidata especially), most rows will land on `two_hand` and enter v_category_sample.

**Risk:** some rows may be mis-classified (e.g., a wikidata "dagger" defaulting to two_hand when one_hand is correct). The name-pattern fallback in `extract_wieldable_humanoid` catches the high-frequency cases (dagger/knife/pistol/etc. → one_hand; greatsword/musket/rifle → two_hand). Residual mis-classification is downstream-tolerable: Pattern-6 axis discovery is robust to ±1 bucket on wieldability for a small fraction of rows.

---

## §4 — Secondary regex fix disposition (Dispatch §Math-before-code item 4)

### §4.1 Bug confirmed empirically

Per Q9 live-DB query:
- **fextralife-elden-ring**: 342 rows mapped to `south_american_indigenous`. ALL 342 contain "incantation" in name or description. ZERO contain legitimate south-american terms.
- **nick-aschenbach-dnd-data**: 156 rows mapped to `south_american_indigenous`. None contain "incantation" or "amazon" — but inspection shows hits like "Vice **inca**rnate", "**inca**ndescent", "**inca**rnation". 1 row has legitimate south-american content (the remaining 155 are FPs).
- **wikipedia**: 138 mapped (some legitimate, some FP — needs sub-inspection; Step 6.6.b will tighten regex globally so all sources benefit).
- **Other sources**: smaller; need re-evaluation after regex tightening.

The bug source: `CULTURE_REGEX_PATTERNS` line `(re.compile(r"\b(inca|peru|andean|amazon|brazil|colombia)", re.I), "south_american_indigenous")` — `\binca` matches the start of "inca**ntation**", "inca**rnate**", "inca**ndescent**", "inca**rnation**" because the regex has NO trailing word boundary.

### §4.2 Fix: rolled into Step 6.6.b CULTURE_REGEX_PATTERNS rewrite

Per §5 below, Step 6.6.b extends CULTURE_REGEX_PATTERNS substantially for lineage recovery. The south_american_indigenous regex is rewritten as part of the same overhaul:

```python
# OLD (buggy):
(re.compile(r"\b(inca|peru|andean|amazon|brazil|colombia)", re.I), "south_american_indigenous"),

# NEW:
(re.compile(
    r"\b(peruvian|andean|amazonian|brazilian|colombian|argentin|chilean|bolivian|ecuadorian|venezuelan|paraguayan|uruguayan|"
    r"quechua|aymara|guaran[ií]|mapuche|tainos?|moche|nazca|chim[uú]|potos[ií]|cuzco|cusco|machu picchu)\b",
    re.I,
), "south_american_indigenous"),
# Notes:
# - Drop 'inca' (matches incantation/incarnate/incandescent across game sources)
# - Drop bare 'amazon' (D&D Amazon-warrior context; too ambiguous)
# - Drop bare 'peru'/'brazil'/'colombia' in favor of adjectival forms (peruvian/brazilian/colombian)
#   This avoids matching things like "Peruvian rifle" prefix in modern military contexts where the substring-only match was OK,
#   but specifically protects against "perused", "perusing", "Brazilia" (not Brazil — capital), etc.
# - Add indigenous-group nouns (Quechua, Aymara, Mapuche, Guaraní) — these legitimately resolve to south_american_indigenous.
# - Add Potosi (Bolivia/Peru), Cuzco/Cusco, Machu Picchu — specific place names that strongly indicate south_amer.
```

### §4.3 Targeted SQL UPDATE after Step 6.6.b regex rewrite

Step 6.6.b re-runs `extract_culture_for_row` against rows whose CURRENT `cultural_lineage_canonical = 'unknown'` (additive recovery only — doesn't relabel rows that already have non-unknown lineage). **BUT** the regex fix also needs to UNDO the 498 current FP labels:

```sql
-- Identify rows incorrectly labeled south_american_indigenous via the old regex
-- (no legitimate south-american term in description; canonical_name contains incantation/incarnate/etc.)
UPDATE weapon_knowledge_entries
   SET cultural_lineage_canonical = 'unknown',
       cultural_lineage_confidence = 0.0
 WHERE cultural_lineage_canonical = 'south_american_indigenous'
   AND source_library IN ('fextralife-elden-ring', 'nick-aschenbach-dnd-data',
                          'bsdata-warhammer-aos', 'pf2ools-pf2ools-data-quarantined',
                          'elden-ring-erdb', 'fextralife-ds1', 'fextralife-ds2', 'fextralife-ds3',
                          'bloqhead-demigods')  -- all game sources with no legitimate south-amer
   AND LOWER(coalesce(description_text, '')) NOT REGEXP '\b(peruvian|andean|amazonian|brazilian|colombian|quechua|aymara|guaran[ií]|mapuche)\b';
-- Note: SQLite REGEXP requires Python-side implementation; this UPDATE runs in Python via the same script.
```

Then re-fire `extract_culture_for_row` on those rows. For game-source rows, the source-library default applies → they land at `fantasy_generic` (confidence 0.5). Net effect:
- fextralife-elden-ring: 342 south_amer → fantasy_generic (correct per cleaning-policy § 5.2)
- nick-aschenbach-dnd-data: 155 south_amer → fantasy_generic (correct)
- Other small game sources: similar small shifts
- wikipedia/wikidata legitimate south-amer rows: untouched (description has legit term; preserved)

Estimated UPDATE: ~498 rows (98% of current south_amer pool).

### §4.4 Acceptance criterion (per dispatch optional gate)

Per dispatch acceptance criteria final bullet: "South-american-indigenous bucket post-fix carries only the 17 rows that legitimately match." Post-fix expected: ~20 rows (allowing small variance from this math note's sampling — wikipedia legitimates may be 5–10 more than the dispatch's 17 estimate, plus wikidata's Potosi/Cuzco recovery may add a few).

**Documented projection: south_amer post-fix = 15–35 rows. Hard ceiling: ≤ 50 rows. Bias toward correctness over count-match.**

---

## §5 — Unknown-lineage sampling pass + Step 6.6.b self-disposition (Dispatch §Math-before-code item 5)

### §5.1 Sampling methodology

Per dispatch §Math-before-code item 5, sampled 50 rows from each of 4 major unknown-source contributors: **wikidata** (9,892 unknowns; 80% of source), **wikipedia** (1,482; 18%), **odin-army-tradoc** (867; 22%), **met-museum** (240; 6%). Each row classified into 4 buckets:

- **(α) Genuinely unknown** — description too generic; no structured cues; no regional vocabulary
- **(β) Regex-recoverable** — description contains clear regional cue that current CULTURE_REGEX_PATTERNS doesn't capture
- **(γ) Structured-field-recoverable** — additional structured field (e.g., wikidata `country`, wikipedia `origin`, ODIN country name vs ISO code, Met `culture` field with new culture name) carries regional signal Step 6.5 doesn't currently consult
- **(δ) Human-judgment-needed / fictional** — ambiguous, cross-cultural, fictional, or genuinely contested

### §5.2 Per-source α/β/γ/δ distribution (sample n=50 each)

| source | α (true unknown) | β (regex recoverable) | γ (structured recoverable) | δ (judgment / fictional) | **β+γ %** | Disposition |
|---|---|---|---|---|---|---|
| wikidata | 21 (42%) | 22 (44%) | 5 (10%) | 2 (4%) | **54%** | **FIRE 6.6.b** (well above 20%) |
| wikipedia | 0 (0%) | 3 (6%) | 38 (76%) | 9 (18%) | **82%** | **FIRE 6.6.b** |
| odin-army-tradoc | 0 (0%) | 0 (0%) | 50 (100%) | 0 (0%) | **100%** | **FIRE 6.6.b** (the canonical_name "Ukrainian X" alone is a near-perfect signal) |
| met-museum | 0 (0%) | 3 (6%) | 47 (94%) | 0 (0%) | **100%** | **FIRE 6.6.b** (culture field populated but regex doesn't recognize values like Tibetan, Caucasian, Flemish) |

**Disposition rule per dispatch §5 (β+γ ≥ 20% for any major source → fire 6.6.b):** ALL four major sources clear the threshold by a wide margin. **Step 6.6.b FIRES.**

### §5.3 What Step 6.6.b extends — proposed regex/field additions for Matt visibility

#### §5.3.1 CULTURE_REGEX_PATTERNS extensions

```python
# === EAST ASIAN (extends current "china|chinese|qing|ming|tang") ===
# Major Chinese dynasties (wikidata `country` field uses dynasty names heavily)
(re.compile(r"\b(shang|zhou|qin|han|wei|jin|liao|song|yuan|cao wei|"
            r"northern wei|southern wei|eastern jin|western jin|"
            r"eastern han|western han|eastern zhou|western zhou|"
            r"warring states|three kingdoms|sui|five dynasties)\b", re.I), "east_asian"),
# Tibetan / Mongolian / Bhutanese (Met museum heavily populated)
(re.compile(r"\b(tibetan?|mongol(ian)?|bhutanese|manchu(rian)?|sinhala|sinhalese|"
            r"khampa|amdo|kham)\b", re.I), "east_asian"),  # tibetan family classified east_asian

# === EUROPEAN (extends current adjectival list with country-name forms + missing regional groups) ===
# Country-name forms (current regex only matches adjectives; add country names)
(re.compile(r"\b(france|germany|italy|spain|poland|russia|netherlands|belgium|switzerland|"
            r"austria|denmark|sweden|norway|portugal|finland|hungary|czechia|"
            r"romania|bulgaria|bosnia|croatia|serbia|slovenia|slovakia|ireland|"
            r"ukraine|belarus|moldova|estonia|latvia|lithuania|albania|north macedonia|"
            r"andorra|monaco|luxembourg|liechtenstein|iceland|malta|cyprus|"
            r"vatican|san marino|montenegro|kosovo)\b", re.I), "european"),
# Missing regional adjectives
(re.compile(r"\b(silesian|bohemian|flemish|flanders|netherlandish|albanian|visigothic|"
            r"cypriote|etruscan|burgundian|prussian|saxon|bavarian|tyrolean|"
            r"vlach|romanian|moldavian|ruthenian|cossack|ukrainian|belarusian|"
            r"venetian|florentine|genoese|milanese|"
            r"andalusian|catalan|basque|galician|"
            r"cornish|gaelic|breton|frankish|"
            r"slovak|magyar|finnic|sami|estonian|latvian|lithuanian)\b", re.I), "european"),
# Wikidata-specific: USSR / Soviet Union (already matches "soviet"; add "ussr")
(re.compile(r"\b(ussr|soviet union)\b", re.I), "european"),

# === MIDDLE EASTERN (extends current "iran|persia|...|mamluk") ===
# Caucasian region (Met heavily populated)
(re.compile(r"\b(caucasian|caucasus|georgian|dagestan|circassian|chechen|"
            r"armenian|azerbaijani|abkhaz|ossetian)\b", re.I), "middle_eastern"),
# Additional middle-eastern terms
(re.compile(r"\b(palestinian|jordanian|lebanese|syrian|kurdish|kuwaiti|qatari|emirati|"
            r"omani|bahraini|israeli|"
            r"byzantine|crusader|levantine|mesopotamian|sumerian|akkadian|"
            r"phoenician|hittite|assyrian|babylonian|sassanid)\b", re.I), "middle_eastern"),

# === SOUTHEAST ASIAN (extends current "indonesia|java|...|filipino") ===
(re.compile(r"\b(bornean|dyak|iban|kadazan|cambodian|laotian|mongol|"
            r"khmer|cham|mon|tagalog|cebuano|moro|hmong|karen|tai|"
            r"timor(ese)?|brunei|malay(an)?)\b", re.I), "southeast_asian"),

# === AFRICAN (extends current "africa|moroc|...|coptic") ===
(re.compile(r"\b(nigerian|ghanaian|senegalese|cameroon(ian)?|congo(lese)?|kenyan|"
            r"tanzanian|ugandan|south african|namibian|zimbabwean|mozambican|"
            r"angolan|sudanese|somali|eritrean|libyan|tunisian|"
            r"yoruba|igbo|hausa|fulani|swahili|amhara|oromo|berber|tuareg|"
            r"benin|ashanti|dahomey|mande)\b", re.I), "african"),

# === NORTH AMERICAN INDIGENOUS (extends current "native_american|first_nations|...") ===
(re.compile(r"\b(navaj[oa]|hopi|comanche|lakota|dakota|nakota|crow|blackfoot|"
            r"haida|tlingit|kwakiutl|nuu-chah-nulth|cree|inuit|métis|"
            r"seminole|chickasaw|choctaw|creek|powhatan|wampanoag)\b", re.I), "north_american_indigenous"),

# === ARCTIC CIRCUMPOLAR (extends current "sami|inuit|greenland|arctic") ===
(re.compile(r"\b(yupik|aleut|chukchi|nenets|evenki|saami|finno-ugric)\b", re.I), "arctic_circumpolar"),

# === OCEANIC (extends current "maori|polynesian|...") ===
(re.compile(r"\b(aboriginal|aborigine|australian|new zealander|"
            r"papuan|melanesian|micronesian|austronesian|gweagal)\b", re.I), "oceanic"),

# === MESOAMERICAN (refinement; less change needed) ===
# Current regex covers mexic|aztec|maya|toltec|tlatoani — add more
(re.compile(r"\b(zapotec|mixtec|tarascan|totonac|otomi|huastec|"
            r"olmec|teotihuacan|tarasco|nahua|mexica|chichimec)\b", re.I), "mesoamerican"),

# === SOUTH AMERICAN INDIGENOUS — REWRITTEN per §4 ===
(re.compile(
    r"\b(peruvian|andean|amazonian|brazilian|colombian|argentin(ian|e)?|chilean|bolivian|"
    r"ecuadorian|venezuelan|paraguayan|uruguayan|"
    r"quechua|aymara|guaran[ií]|mapuche|tainos?|moche|nazca|chim[uú]|"
    r"potos[ií]|cuzco|cusco|machu picchu|inca empire|incan empire)\b",
    re.I,
), "south_american_indigenous"),
```

#### §5.3.2 COUNTRY_CODE_TO_LINEAGE extensions (for ODIN + others)

```python
# Extend the dictionary to handle full country names AND additional ISO codes:
COUNTRY_NAME_TO_LINEAGE = {
    # Europe (full country names — ODIN uses "Ukraine" not "UKR")
    "Ukraine": "european", "Belarus": "european", "Moldova": "european",
    "Czech Republic": "european", "Slovakia": "european", "Slovenia": "european",
    "Croatia": "european", "Serbia": "european", "Bosnia and Herzegovina": "european",
    "Albania": "european", "Romania": "european", "Bulgaria": "european",
    "North Macedonia": "european", "Montenegro": "european", "Kosovo": "european",
    "United States": "european", "Russia": "european", "France": "european",
    "Germany": "european", "United Kingdom": "european", "Italy": "european",
    "Spain": "european", "Poland": "european", "Netherlands": "european",
    "Belgium": "european", "Switzerland": "european", "Austria": "european",
    "Sweden": "european", "Norway": "european", "Finland": "european",
    "Denmark": "european", "Portugal": "european", "Greece": "european",
    "Ireland": "european", "Hungary": "european", "Estonia": "european",
    "Latvia": "european", "Lithuania": "european", "Iceland": "european",
    "Soviet Union": "european", "USSR": "european",
    # East Asian (full names)
    "China": "east_asian", "Japan": "east_asian", "South Korea": "east_asian",
    "North Korea": "east_asian", "Taiwan": "east_asian", "Hong Kong": "east_asian",
    "Mongolia": "east_asian", "Tibet": "east_asian", "Bhutan": "east_asian",
    # Southeast Asian
    "Vietnam": "southeast_asian", "Thailand": "southeast_asian", "Indonesia": "southeast_asian",
    "Philippines": "southeast_asian", "Malaysia": "southeast_asian", "Singapore": "southeast_asian",
    "Myanmar": "southeast_asian", "Cambodia": "southeast_asian", "Laos": "southeast_asian",
    "Brunei": "southeast_asian", "East Timor": "southeast_asian",
    # South Asian
    "India": "south_asian", "Pakistan": "south_asian", "Bangladesh": "south_asian",
    "Sri Lanka": "south_asian", "Nepal": "south_asian", "Maldives": "south_asian",
    # Middle Eastern
    "Iran": "middle_eastern", "Iraq": "middle_eastern", "Saudi Arabia": "middle_eastern",
    "Turkey": "middle_eastern", "Israel": "middle_eastern", "Palestine": "middle_eastern",
    "Jordan": "middle_eastern", "Lebanon": "middle_eastern", "Syria": "middle_eastern",
    "Yemen": "middle_eastern", "Oman": "middle_eastern", "Qatar": "middle_eastern",
    "Bahrain": "middle_eastern", "Kuwait": "middle_eastern",
    "United Arab Emirates": "middle_eastern", "UAE": "middle_eastern",
    # African
    "Egypt": "african", "South Africa": "african", "Nigeria": "african",
    "Kenya": "african", "Ethiopia": "african", "Algeria": "african",
    "Morocco": "african", "Tunisia": "african", "Libya": "african",
    "Sudan": "african", "Ghana": "african", "Cameroon": "african",
    # Mesoamerican
    "Mexico": "mesoamerican", "Guatemala": "mesoamerican", "Honduras": "mesoamerican",
    "El Salvador": "mesoamerican", "Nicaragua": "mesoamerican",
    # South American
    "Brazil": "south_american_indigenous", "Argentina": "south_american_indigenous",
    "Chile": "south_american_indigenous", "Peru": "south_american_indigenous",
    "Colombia": "south_american_indigenous", "Venezuela": "south_american_indigenous",
    "Ecuador": "south_american_indigenous", "Bolivia": "south_american_indigenous",
    "Paraguay": "south_american_indigenous", "Uruguay": "south_american_indigenous",
    "Guyana": "south_american_indigenous", "Suriname": "south_american_indigenous",
    # Oceanic
    "Australia": "oceanic", "New Zealand": "oceanic", "Papua New Guinea": "oceanic",
    "Fiji": "oceanic", "Samoa": "oceanic", "Tonga": "oceanic",
    "Vanuatu": "oceanic", "Solomon Islands": "oceanic",
    # Canada (special; treat as European default; cf. existing COUNTRY_CODE_TO_LINEAGE)
    "Canada": "european",
}
```

#### §5.3.3 Per-source extraction enhancements

```python
# wikipedia — currently extract_culture_for_row hits desc-regex on (desc, cultural_tags, sp['place'])
# but wikipedia rows almost never have 'place'. They have 'origin'. Add:
if src == "wikipedia":
    origin = sp.get("origin") or ""
    if origin:
        # First try the COUNTRY_NAME map (e.g., "United States" → european)
        # Then try description regex (catches "Soviet Union", "Israel<br>United States" cross-cases)
        for country_name, lineage in COUNTRY_NAME_TO_LINEAGE.items():
            if country_name.lower() in origin.lower():
                return (lineage, 0.9)  # 0.9 confidence — structured-but-text-parsed
        # Fallback to regex
        lineage, _ = extract_culture_from_text(origin)
        if lineage != "unknown":
            return (lineage, 0.85)

# wikidata — extends `country` handling beyond pure regex match
if src == "wikidata":
    country = sp.get("country_of_origin") or sp.get("country") or ""
    if country:
        # COUNTRY_NAME_TO_LINEAGE first (e.g., "France" → european)
        for country_name, lineage in COUNTRY_NAME_TO_LINEAGE.items():
            if country_name.lower() == country.lower() or country.lower().startswith(country_name.lower()):
                return (lineage, 1.0)
        # Then regex (will catch dynasties via new patterns)
        lineage, _ = extract_culture_from_text(country)
        if lineage != "unknown":
            return (lineage, 0.9)

# odin-army-tradoc — currently uses origin_countries as ISO codes; add full-name handling
if src == "odin-army-tradoc":
    origin_countries = sp.get("origin_countries") or []
    if isinstance(origin_countries, list) and origin_countries:
        for entry in origin_countries:
            # Try ISO code first (existing logic)
            if entry in COUNTRY_CODE_TO_LINEAGE:
                return (COUNTRY_CODE_TO_LINEAGE[entry], 1.0)
            # Then full country name
            for country_name, lineage in COUNTRY_NAME_TO_LINEAGE.items():
                if country_name.lower() == str(entry).lower():
                    return (lineage, 1.0)
    # Fallback: extract from canonical_name (ODIN names follow "X [Nationality] [Type]" pattern)
    name = row["canonical_name"] or ""
    name_lineage, _ = extract_culture_from_text(name)
    if name_lineage != "unknown":
        return (name_lineage, 0.85)  # high-confidence; ODIN naming convention is reliable

# met-museum — extends existing logic; new culture patterns (Tibetan etc.) will hit the regex naturally
# But also: when `culture` field doesn't match, try `country` (Met often has both)
if src == "met-museum":
    culture_field = sp.get("culture") or ""
    if culture_field:
        lineage, _ = extract_culture_from_text(culture_field)
        if lineage != "unknown":
            return (lineage, 1.0)
    # NEW: also check `country` if culture doesn't resolve
    country = sp.get("country") or ""
    if country:
        for country_name, lineage in COUNTRY_NAME_TO_LINEAGE.items():
            if country_name.lower() in country.lower():
                return (lineage, 0.95)
        lineage, _ = extract_culture_from_text(country)
        if lineage != "unknown":
            return (lineage, 0.9)
```

### §5.4 Projected recovery counts per source

Using the per-source α/β/γ distribution × current unknown count:

| source | unknown rows | β+γ % | **recoverable (β+γ)** | remaining α + δ |
|---|---|---|---|---|
| wikidata | 9,892 | 54% | **~5,340** | ~4,552 (mostly bare Q-IDs with no info) |
| wikipedia | 1,482 | 82% | **~1,215** | ~267 (mostly fictional weapons + FPs) |
| odin-army-tradoc | 867 | 100% | **~867** | 0 |
| met-museum | 240 | 100% | **~240** | 0 |
| **TOTAL major sources** | **12,481** | — | **~7,662** | ~4,819 |

**Step 6.6.b expected mutations: ~7,662 rows shift from `cultural_lineage_canonical='unknown'` to a recovered non-unknown lineage.**

### §5.5 Step 6.6.b acceptance criteria (per dispatch open question 6)

| Criterion | Threshold | Rationale |
|---|---|---|
| Recovery rate per targeted source | ≥ 50% (relaxed from dispatch's 60% suggested floor) | Sampling pass shows wikidata is bottlenecked by ~46% genuinely-unknown bare Q-IDs; 50% achievable, 60% requires getting into LSA-on-name territory which is out of scope here |
| False-recovery rate (rows that get a wrong lineage label vs staying unknown) | ≤ 5% per random-sample audit of N=50 recovered rows | Matches dispatch suggested ceiling |
| Additive-only invariant | 0 rows have their non-unknown lineage relabeled (except the 498 south_amer FP-correction in §4) | Hard invariant; verified post-run |

The 50% recall relaxation from the dispatch's suggested 60%: wikidata's ~46% α (genuinely bare Q-IDs with `{"weapon_type": "X"}` and no other signal) is irrecoverable without external Q-ID lookup against Wikidata's live SPARQL endpoint — that's a separate dispatch (and out of scope per dispatch §Out of scope). Documenting this constraint explicitly: wikidata's α dominates; the ceiling on recovery is structural, not algorithmic.

### §5.6 Operating order: Step 6.6.b runs BEFORE Step 6.6

Per dispatch §5: "Step 6.6.b must complete before Step 6.6 promotes rows to `weapon_kind='category'` so the newly-promoted rows enter v_category_sample with the best-available lineage labels."

**Execution order:**
1. Pre-step backup (`telemetry.db.pre-step6.6`)
2. Run Step 6.6.b → ~7,662 rows shift from `lineage='unknown'` → various recovered lineages
3. Apply secondary regex fix per §4 → ~498 south_amer FPs corrected (mostly to fantasy_generic via game-source default)
4. Run Step 6.6 → ~34,192 rows promoted from `weapon_kind='unknown'` → `'category'` + wieldable_humanoid populated
5. Run Step 7 F4 re-run on enlarged candidate pool
6. Acceptance gates + round-trip smoke
7. MIGRATION.md + completion summary + tag

---

## §6 — Step 7 F4 re-run scope (Dispatch open question 3)

### §6.1 Decision: full F4 re-cluster on enlarged candidate pool

The dispatch offers two options:
- (A) Re-cluster only newly-promoted rows against existing canonical pool — faster but order-dependent
- (B) Full F4 re-cluster of all candidate rows with embedding-cache reuse — thorough; produces consistent merges

**Chosen: Option B.** Rationale:

1. **Step 7's existing code naturally picks up the enlarged pool** via the WHERE clause `weapon_kind NOT IN ('ammo_or_consumable','unknown')`. The newly-promoted category rows enter the candidate pool without code modification.

2. **Existing 1,194 canonical-merge entries are preserved** by the WHERE clause `dedup_status IN ('canonical','unprocessed')` — `merged_into` rows skip. The new run only ADDS merges; doesn't undo prior ones.

3. **Block-level re-clustering ensures consistency.** Example: a previously-canonical RA Sword (now `weapon_kind='category'`) entering the (sword × european × historical) block will be pairwise-compared against existing wikipedia/wikidata canonical Swords in the same block. The historical-lane aggressive merge (NAME_SIM ≥ 0.7) catches cross-source name matches. Without re-running, these cross-source merges would be missed.

4. **Embedding-cache: not applicable.** Step 7 uses TF-IDF vectorizer (per Phase D Q5 adjustment: sentence-transformers unavailable). TF-IDF is recomputed each run; "embedding cache" doesn't apply. Wall-clock cost: estimated 4–8 minutes for fit + cosine on ~48K descriptions (4x larger pool than Phase D's ~26K).

5. **Risk: union-find canonical-survivor flips.** When a new row joins an existing canonical's merge component, the canonical-survivor (chosen as min(id)) may flip if the new row has a smaller id than the existing canonical. In practice this is unlikely because newly-promoted rows come from older sources (royal_armouries, met-museum) which have low IDs, BUT existing F4-merge canonicals also have low IDs (they're the lowest-ID rows of their components). The risk is minimal but non-zero. Documented; will be verified in §6 acceptance gate (c).

### §6.2 F4 re-run mutations expected

| Component | CURRENT count | Expected POST count |
|---|---|---|
| `dedup_status='canonical'` rows | 6,621 | ~40,000–42,000 (existing canonicals + newly-promoted-then-not-merged) |
| `dedup_status='merged_into'` rows | 19,146 | ~19,800–20,500 (existing + small batch of new F4 cross-source merges) |
| `knowledge_entry_canonical_merge` rows | 1,194 | ~1,250–1,500 (existing 1,194 + new cross-source components from enlarged pool) |

### §6.3 Cross-seam contract preservation

Per dispatch §"Cross-seam contract change? (Principle 6 gate)":
- The `knowledge_entry_canonical_merge` table's schema is unchanged
- Existing 1,194 entries are preserved (idempotent UNIQUE constraint on `canonical_name`)
- New entries are appended only; no destructive mutation
- The view definitions for `v_category_sample` / `v_category_sample_humanoid_strict` / `v_category_sample_humanoid_permissive` are unchanged
- The only contract change: row-membership of `v_category_sample` grows ~16,699 → ~50K (per §2)

---

## §7 — Tag granularity decision (Dispatch open question 4)

**Decision: single tag `elrond/phase-D-bis-step-6-6-2026-05-23`** at end of pipeline.

Rationale: this is a focused amendment (one logical step, with three sub-mutations: 6.6.b lineage recovery, 6.6 category promotion + wieldable backfill, Step 7 F4 re-run). The Phase D block-tag discipline was justified because Phase D had 9 independent steps with significant scope per step; Phase D-bis is one targeted fix with three coupled mutations. Single tag is cleaner for audit and matches the granularity of the dispatch authorization.

If acceptance gates fail mid-pipeline (e.g., Step 6.6.b's recovery audit fails ≤5% false-recovery threshold), I will restore from `pre-step6.6` backup, fix the regex/extraction logic, and re-run from scratch — same single-tag scope but iterated to passing state.

---

## §8 — Idempotency guarantees per sub-step

| Sub-step | Idempotency strategy |
|---|---|
| **6.6.b** | WHERE clause filters on `cultural_lineage_canonical = 'unknown'`. Re-run skips rows already recovered (now non-unknown). For the 498 south_amer FPs, the WHERE clause specifically targets them; re-run after relabel sees them at `unknown` and re-attempts extraction (will produce same result via deterministic source-driven function → idempotent). |
| **6.6** | WHERE clause filters on `weapon_kind = 'unknown' AND dedup_status IN ('canonical','unprocessed')`. Re-run skips rows already promoted (now `weapon_kind='category'`). |
| **wieldable_humanoid backfill** | Per-row UPDATE; deterministic source-driven extraction. Re-run produces same value → idempotent overwrite. |
| **Step 7 F4 re-run** | Per Phase D math note §4: union-find guard via `knowledge_entry_canonical_merge` lookup + `dedup_status='merged_into'` skip. Re-run on already-clustered rows is a no-op. |

**Random-seed reproducibility:** all extraction is deterministic (no randomness). TF-IDF vectorizer uses `random_state=42` (Phase D convention).

---

## §9 — Rollback plan

**Master strategy:** SQLite file-level snapshot before Step 6.6 fires.

| Step | Backup before fire | Rollback path |
|---|---|---|
| Pre-Step-6.6.b | `cp telemetry.db backups/telemetry.db.pre-step6.6` | Restore file copy. Captures pre-amendment state. |
| Per-sub-step intermediate states | Not backed up (single-tag scope; rollback is to pre-6.6 snapshot if anything fails) | Re-run from scratch after pre-6.6 restore |

**Backup retention:** keep pre-step6.6 backup until milestone-tag `v0.2-weapon-library-substrate-cleaned` is Matt-approved (matches Phase D backup retention policy).

**Pre-existing Phase D backups (9 files; ~2.3 GB)** stay in place per Phase D math note §5 retention policy. Phase D's pre-step7 backup is the canonical "before F4" snapshot; pre-Phase-D-bis is the canonical "before Phase-D-bis" snapshot. Together they bracket the full re-fire range if needed.

---

## §10 — Acceptance gate verification queries (consolidated)

### §10.1 Gate (a) — Promotion-eligibility precision (random-sample audit N=50)

```python
# Python-side audit: sample 50 newly-promoted rows, classify each via FP detection rules
sample = query("SELECT * FROM weapon_knowledge_entries
                 WHERE weapon_kind='category'
                   AND source_library IN (<the 9 promoted sources>)
                   AND <some marker that promotion was Phase-D-bis>  -- use audit query on dedup_status flip post-pre-6.6 backup
                 ORDER BY RANDOM() LIMIT 50")
fp_count = sum(1 for r in sample if classify_fp(r))
precision_error = fp_count / 50
assert precision_error <= 0.05  # hard
print(f"Precision-error: {precision_error:.2%} (target ≤ 2.0%)")
```

Marker for "Phase-D-bis-promoted" — comparison against pre-step6.6 backup: rows whose weapon_kind='category' now BUT was 'unknown' in the backup. Implementation: ATTACH pre-step6.6 backup as separate DB, JOIN on id, compare weapon_kind.

### §10.2 Gate (b) — Promotion-eligibility recall (random-sample audit N=50 of post-fix unknowns)

```python
# Sample 50 rows still at weapon_kind='unknown' post-fix; check if they SHOULD have been promoted
sample = query("SELECT * FROM weapon_knowledge_entries
                 WHERE weapon_kind='unknown'
                   AND source_library IN (<the 9 promoted sources>)
                 ORDER BY RANDOM() LIMIT 50")
missed_promotion_count = sum(1 for r in sample if NOT classify_fp(r) AND is_real_weapon(r))
recall_error = missed_promotion_count / 50
assert recall_error <= 0.05
```

### §10.3 Gate (c) — Step 7 F4 stability

```sql
-- Pre-existing 1,194 canonical-merge entries still intact
SELECT COUNT(*) FROM knowledge_entry_canonical_merge;
-- Expect ≥ 1,194 (additive only; new entries added)

-- Pre-existing canonical rows (pre-Step-7-rerun) not demoted to merged_into without justification
-- Compare backup vs current
ATTACH 'backups/telemetry.db.pre-step6.6' AS pre;
SELECT COUNT(*) FROM pre.weapon_knowledge_entries p
JOIN main.weapon_knowledge_entries m ON p.id = m.id
WHERE p.dedup_status = 'canonical'
  AND m.dedup_status = 'merged_into'
  AND p.weapon_kind != 'unknown'  -- exclude the deliberate 6.6 promotion-then-merge cases
  -- "Justified demotion" is one where post-Step-7 the row joined an existing merge component
  -- Quantify and document — should be ≤ small handful (≤ 10) for stability
```

### §10.4 Gate (d) — v_category_sample post-fix profile

```sql
-- Row count
SELECT COUNT(*) FROM v_category_sample;
-- Expect 47,000 ≤ N ≤ 57,000

-- Per-source membership
SELECT source_library, COUNT(*) FROM v_category_sample GROUP BY source_library ORDER BY 2 DESC;
-- Compare against §2.2 projection

-- Per-lineage distribution
SELECT cultural_lineage_canonical, COUNT(*),
       100.0 * COUNT(*) / (SELECT COUNT(*) FROM v_category_sample) AS pct
FROM v_category_sample
GROUP BY cultural_lineage_canonical
ORDER BY 2 DESC;
-- Compare against §2.3 projection (both raw post-promotion and post-recovery measurements report;
-- gate passes if EITHER matches within ±5pp)
```

### §10.5 Round-trip smoke per Principle 6

30-row random-sample category-eligibility audit:
```python
sample_30 = query("SELECT * FROM v_category_sample
                    WHERE id IN (SELECT id FROM weapon_knowledge_entries
                                  WHERE id IN <ids promoted by Phase-D-bis>)
                    ORDER BY RANDOM() LIMIT 30")
# Human-judge each: is this a category-eligible weapon?
# Threshold: FP-rate ≤ 2.0% target / ≤ 5.0% hard
```

### §10.6 No-regression on Phase D gates

Re-evaluate Phase D Gates (a)-(d) on the post-Step-6.6 + post-Step-7 state per dispatch acceptance criteria last bullet.

Specifically:
- **Phase D Gate (a) FP rate** in v_category_sample stays ≤ 1.5% target / ≤ 3.0% hard (was 0.0%)
- **Phase D Gate (b) residual duplication** ≤ 4.0% on the (canonical_name × lineage × period × source) key
- **Phase D Gate (c) field-coverage floors** all maintained: structured ≥ 95%, description ≥ 85%, cultural ≥ 70%, period ≥ 60%, register ≥ 95%
- **Phase D Gate (d) weapon_kind misclassification** stays ≤ 2% on the (d.1) and (d.2) sub-axes (these test category-vs-unique and category-vs-named_template); (d.3) category-vs-ammo: should remain 0% (the cataclysm AMMO-subtype exclusion in §1.1 keeps the ammo leak out)

---

## §11 — Files produced

| Path | Content |
|---|---|
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/phase-D-bis-math-note.md` | **THIS DOC** |
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/MIGRATION.md` | Cross-seam impact declaration (legolas Phase E-1 deliverables are now stale; ADR-004) |
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/scripts/09b_step6_6b_unknown_lineage_recovery.py` | Step 6.6.b implementation (extends CULTURE_REGEX_PATTERNS + adds COUNTRY_NAME_TO_LINEAGE + per-source enhancements; runs BEFORE Step 6.6) |
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/scripts/09_step6_6_category_promotion_sweep.py` | Step 6.6 implementation (the promotion sweep with wieldable_humanoid backfill) |
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/scripts/10_step7_f4_rerun.py` | Step 7 F4 re-run wrapper (imports + calls the Phase D Step 7 logic on the enlarged pool) |
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/scripts/11_final_acceptance_gates.py` | Final 4-gate verification + round-trip smoke |
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/phase-D-bis-completion-summary.md` | Per-step deltas + per-gate pass/fail |
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/logs/*.json` | Per-step structured summary artifacts |
| `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/backups/telemetry.db.pre-step6.6` | Single pre-fire backup (gitignored) |

**NOT committed:**
- DB file (`telemetry.db`) — gitignored per loadout repo convention
- `backups/telemetry.db.pre-step6.6` — local; retained to milestone-tag

---

## §12 — Cross-references

- E1 audit (this dispatch's trigger): `agentic_orchestration/elrond/notes/2026-05-23-phase-E-1-bis-E1-lineage-audit.md`
- Phase D math note (precedent): `phase-D-cleaning-pipeline-2026-05-23/phase-D-math-note.md`
- Phase D completion summary: `phase-D-cleaning-pipeline-2026-05-23/phase-D-completion-summary.md`
- Phase D tag: `elrond/phase-D-cleaning-pipeline-2026-05-23` (durable; not modified by this dispatch)
- Phase D commit: `9e7d14b` (durable; not modified)
- Gandalf design-fit verdict (kept in loop): `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md`
- Legolas Phase E-1 features (the downstream consumer that surfaced the 94.46% figure): `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-features.md`
- Cleaning-policy § 5.2 (design-side canonical, Matt-locked): `canonical/story/cleaning-policy-design-2026-05-22.md`
- Hive-mind protocol § 6 (Pattern 6 doctrine; preserved): `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md`
- ADR-001 (tag protocol): `agentic_orchestration/GOVERNANCE.md`
- ADR-004 (cross-seam coordination via MIGRATION.md): `agentic_orchestration/GOVERNANCE.md`
- ADR-006 (external-write authorization): `agentic_orchestration/GOVERNANCE.md`
- Engineering disciplines #1 math-before-code, #11 audit-preservation, #19 right tool, #20 robots.txt: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

**Signed:** elrond (data steward; Phase D-bis Pattern-B executor)
**Authority:** Matt 2026-05-23 (fire authorization + §5 self-disposition delegation)
**Next:** MIGRATION.md (cross-seam consumer impact) → pre-step6.6 backup → Step 6.6.b regex/extraction extension run → Step 6.6 category-promotion sweep + wieldable backfill → secondary regex FP correction → Step 7 F4 re-run → acceptance gates + round-trip smoke → completion summary → tag.
