# Phase D Math Note — Cleaning Pipeline Execution Plan

**Date:** 2026-05-23
**Author:** elrond (data steward; Phase D Pattern-B executor)
**Status:** v1 — load-bearing pre-fire deliverable per Discipline #1 + jack-ryan Gate-1 Amendment #5
**Authority:** Matt 2026-05-23 — **whole-pipeline upfront authorization** (covers schema migration, per-step row mutations, quarantine archive creation, VACUUM, tag, commit); G2-pattern disposition delegated to elrond under Matt's principle
**DB target:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (89,839 active rows / 24 source libraries / 136 MB)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-elrond-phase-D-cleaning-pipeline.md`
**Upstream:**
- gandalf `canonical/story/cleaning-policy-design-2026-05-22.md` v1 (Phase B framework; Matt-locked)
- gandalf `canonical/story/variant-cluster-policy-assignments-2026-05-23.md` (26-cluster / 38-decision policy)
- legolas `phase-A-audit/{per-source-quality, variant-clusters, named-unique-verification, cleanliness-baseline}.md` (empirical baselines)
- legolas `phase-A-math-note.md` (sampling strategy)
- legolas `schema.sql` v1.1.0 (current schema)
- ADR-004 (cross-seam MIGRATION.md); ADR-006 (external-write authorization); jack-ryan Gate-1 review (5 amendments applied)

---

## §0 — Preamble: authorization model + G2-pattern disposition

### §0.1 Matt's authorization (2026-05-23)

> "Authorize the whole pipeline upfront. On #3, if the name contains a categorical name as part of a concatenated name, it is likely not a unique category unto itself and should not be treated as such. You can take ownership of this call."

**Operational reading:**

1. **Pipeline-wide authorization** covers: schema migration (9 ALTER + 3 CREATE VIEW), per-step row mutations across all 7 steps, F3 quarantine archive creation + rename (NOT DELETE per Discipline #11 audit-preservation), VACUUM at end-of-pipeline, intermediate per-step commits, final tag + completion record. Per-statement authorization gates are NOT re-asserted within the pipeline; elrond proceeds end-to-end against the math note plan.

2. **No-DELETE constraint** still holds (dispatch DO NOT list + Discipline #11). Quarantine = rename `source_library` + dump-to-archive + leave rows in DB. The wikipedia-unfiltered pattern at 130K-scale proved this. The single permitted DELETE pathway under whole-pipeline authorization is the wikipedia-unfiltered–style pattern — and even that requires the archive to exist first.

3. **G2-pattern (concatenated-name) disposition delegated to elrond** per Matt's principle. No surface-to-Matt required for G2-pattern cases; documented in `phase-D-flagged-clusters.md` as MATT-PRINCIPLE-DISPOSITIONED. F1/F2/F3/F4/F5/F6 + G1/G3/G4/G5 remain Matt-locked.

### §0.2 G2-pattern principle (Matt-stated; elrond-operationalized)

> "If the name contains a categorical name as part of a concatenated name, it is likely not a unique category unto itself and should not be treated as such."

**Mapped to detection cases:**

| Name pattern | Example | Disposition |
|---|---|---|
| Bare category-name across multiple sources | `Dagger` × 4 soulslike sources | `weapon_kind=category` per source; `related_entries` cross-link; **no auto-merge** (preserve per-source lore) |
| Embedded-category prefix-modifier | `Great Katana`, `Worn Mace`, `Hardened Steel Katana` | `weapon_kind=category` (per-source variant); not `unique` |
| Embedded-category suffix-modifier | `Moonlit Katana`, `Magehunter Katana` | `weapon_kind=named_template` (game-specific narrative naming on category base); not `unique` |
| Embedded-legend-name with brand/model prefix | `M982 Excalibur`, `Kimber Aegis`, `Tyrfing missile`, `Matra Durandal` | `weapon_kind=category` (modern military item named after legend); legendary referent stays separately `unique` |
| Embedded-legend-name with parenthetical-qualifier | `Mjolnir (comics)`, `Excalibur (rifle)` | `weapon_kind=named_template` (variant/derivative)or `category` (real modern weapon); NOT `unique` |
| Bare legend name | `Excalibur`, `Aegis`, `Tyrfing` | `weapon_kind=unique` per allowlist |

**Phase D operationalization:** Step 6 (unique detection) applies allowlist-regex ONLY when the canonical_name is the BARE legendary name (no embedded category-modifier, no brand prefix). Step 5 (brand-prefix disambiguation) catches concatenated cases. Step 7 (F4 merge) flags but does not auto-merge bare-category-name cross-source cases (SOULS-1 Dagger pattern); each per-source row stays canonical with cross-link via `related_entries`.

### §0.3 Empirical baseline verified against live DB

All Phase A audit baselines re-verified at 2026-05-23 01:30:

| Field | DB count | Phase A audit | Match? |
|---|---|---|---|
| total rows | 89,839 | 89,839 | ✓ |
| distinct `LOWER(canonical_name)` | 47,586 | 47,586 | ✓ |
| description_text populated | 79,678 (88.7%) | 88.7% | ✓ |
| structured_properties populated | 89,508 (99.6%) | 99.6% | ✓ |
| cultural_lineage_tags populated | 72,498 (80.7%) | 80.7% | ✓ |
| historical_period populated | 62,126 (69.2%) | 69.2% | ✓ |
| per-source row counts | 24 sources (royal_armouries 38,127 → 5e-bits-5e-database 37) | matches | ✓ |

Raw duplicate baseline for gate (b) recall: **42,253 rows** = 89,839 − 47,586. This is the denominator for the ≥92% dedup-recall verification per jack-ryan Gate-1 Amendment #2.

---

## §1 — Schema migration plan

### §1.1 Idempotent ALTER TABLE strategy

SQLite has no `ALTER TABLE ADD COLUMN IF NOT EXISTS`. Idempotency is implemented via the migration runner: each ALTER is guarded by a PRAGMA `table_info` lookup that confirms the column does not already exist. If it exists, the ALTER is skipped. Same pattern for views via PRAGMA `list_columns` on the view-name index in `sqlite_master`.

**Runner pseudocode:**

```python
def add_column_if_absent(conn, table, col_name, col_def):
    cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if col_name in cols:
        log(f"SKIP {table}.{col_name} — already exists")
        return
    conn.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_def}")
    log(f"ADDED {table}.{col_name}")

def create_view_if_absent(conn, view_name, view_sql):
    exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='view' AND name=?", (view_name,)
    ).fetchone()
    if exists:
        log(f"SKIP view {view_name} — already exists")
        return
    conn.execute(view_sql)
    log(f"CREATED view {view_name}")
```

### §1.2 Nine new columns (all on `weapon_knowledge_entries`)

Per dispatch § Scope schema-migration, exact column definitions:

```sql
-- (1) wieldable_humanoid — 6-bucket per gandalf § 2.4 (with mount_required + shoulder_supported)
ALTER TABLE weapon_knowledge_entries ADD COLUMN wieldable_humanoid TEXT
  DEFAULT 'unknown' CHECK (wieldable_humanoid IN
  ('one_hand','two_hand','shoulder_supported','either','no','mount_required','unknown'));

-- (2) weapon_kind — 5-bucket per gandalf § 1.3 (with ammo_or_consumable)
ALTER TABLE weapon_knowledge_entries ADD COLUMN weapon_kind TEXT
  DEFAULT 'unknown' CHECK (weapon_kind IN
  ('category','unique','named_template','ammo_or_consumable','unknown'));

-- (3) dedup_status — 3-state per F1/F4
ALTER TABLE weapon_knowledge_entries ADD COLUMN dedup_status TEXT
  DEFAULT 'unprocessed' CHECK (dedup_status IN
  ('canonical','merged_into','unprocessed'));

-- (4) variant_relationship — TEXT free-form per gandalf § 6.6
ALTER TABLE weapon_knowledge_entries ADD COLUMN variant_relationship TEXT
  DEFAULT 'independent';
  -- enum values: 'independent' | 'sub_variant_of:<parent_id>' |
  --              'model_line_sibling_of:<related_ids>'

-- (5) cultural_lineage_canonical — 15 values (13 + cross_cultural + unknown)
--     Per gandalf § 5.1; aligned with the existing weapons.cultural_lineage enum
ALTER TABLE weapon_knowledge_entries ADD COLUMN cultural_lineage_canonical TEXT
  DEFAULT 'unknown' CHECK (cultural_lineage_canonical IN
  ('european','east_asian','south_asian','southeast_asian','middle_eastern',
   'african','north_american_indigenous','mesoamerican','south_american_indigenous',
   'arctic_circumpolar','oceanic','fantasy_generic','sci_fi_generic',
   'cross_cultural','unknown'));

-- (6) historical_period_canonical — 8 mutually-exclusive year-banded buckets
ALTER TABLE weapon_knowledge_entries ADD COLUMN historical_period_canonical TEXT
  DEFAULT 'unknown' CHECK (historical_period_canonical IN
  ('pre_classical','classical','medieval','early_modern','industrial',
   'modern','contemporary','fictional','unknown'));

-- (7) register_canonical — 5 values (historical / military_modern / fantasy / sci_fi / mythological)
ALTER TABLE weapon_knowledge_entries ADD COLUMN register_canonical TEXT
  DEFAULT 'unknown' CHECK (register_canonical IN
  ('historical','military_modern','fantasy','sci_fi','mythological','unknown'));

-- (8) cultural_lineage_confidence — [0.0, 1.0] per gandalf § 5.3
ALTER TABLE weapon_knowledge_entries ADD COLUMN cultural_lineage_confidence REAL
  DEFAULT 0.0 CHECK (cultural_lineage_confidence >= 0.0
                     AND cultural_lineage_confidence <= 1.0);

-- (9) template_quality_score — per gandalf § 4.8 (named_template sampling priority signal)
ALTER TABLE weapon_knowledge_entries ADD COLUMN template_quality_score REAL
  DEFAULT 0.0 CHECK (template_quality_score >= 0.0
                     AND template_quality_score <= 1.0);
```

**All 9 columns are nullable / have defaults.** Existing readers see new columns as `'unknown'` / `0.0` and continue to function. No FK constraints added (avoiding tight coupling to `knowledge_entry_canonical_merge` since variant_relationship + dedup_status capture the merge state directly).

### §1.3 Three new views

```sql
-- (a) v_category_sample — engine-side default consumption view
CREATE VIEW v_category_sample AS
SELECT * FROM weapon_knowledge_entries
WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either')
  AND weapon_kind IN ('category','named_template')
  AND dedup_status IN ('canonical','unprocessed')
  AND source_library NOT IN (
    'wikipedia-unfiltered',
    'pf2ools-pf2ools-data-quarantined',
    'souls-api-thomaslincoln-quarantined'
  );

-- (b) v_category_sample_humanoid_strict — excludes 'either'
CREATE VIEW v_category_sample_humanoid_strict AS
SELECT * FROM v_category_sample
WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported');

-- (c) v_category_sample_humanoid_permissive — adds 'mount_required'
CREATE VIEW v_category_sample_humanoid_permissive AS
SELECT * FROM v_category_sample
WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either','mount_required');
```

The two humanoid-strict / humanoid-permissive views match gandalf § 2.7 (alternate sample-pool views requested for cohesion-judge per-kit access).

### §1.4 Schema-migration smoke test

After all 9 ALTER + 3 CREATE VIEW execute, run:

```sql
-- (1) PRAGMA table_info(weapon_knowledge_entries) — confirm 26 columns total (17 original + 9 new)
-- (2) SELECT name FROM sqlite_master WHERE type='view' AND name LIKE 'v_category%';
--     Expect 3 rows.
-- (3) SELECT COUNT(*) FROM weapon_knowledge_entries WHERE weapon_kind IS NULL;
--     Expect 0 (default 'unknown' applied to all rows).
-- (4) SELECT COUNT(*) FROM v_category_sample;
--     Expect 0 (no rows yet classified; dedup_status='unprocessed' is INCLUDED;
--                wait — re-check the view definition).
--     [CORRECTION] dedup_status='unprocessed' IS in the view; weapon_kind='unknown' is NOT
--     in the view (view requires category|named_template). At post-migration pre-Step-1
--     state, all rows have weapon_kind='unknown' → v_category_sample returns 0 rows.
--     After Step 1+ classification, count grows as rows are tagged category/named_template.
```

---

## §2 — Per-step row-impact estimates

Anchored to Phase A empirical baselines. Each estimate notes (a) rows touched, (b) rows mutated, (c) rows merged-into-canonical (where applicable), (d) expected post-step active substrate count.

### §2.1 Step 1 — ammo_or_consumable tagging

**Rows touched:** all 89,839 (full-scan classification pass).

**Rows mutated (weapon_kind → 'ammo_or_consumable'):** ~15,750 per legolas empirical (Gate (d.3) baseline).

Per-source breakdown:

| Source | Detection rule | Expected mutations |
|---|---|---|
| royal_armouries | category_value IN ('Ammunition & projectiles', 'Armour pieces', 'Complete armours', 'Helmets', 'Animal armour & equestrian equipment') OR canonical_name regex match | ~10,951 (4,185+3,676+1,665+1,425+500 partial; plus regex catches in Relics/Archery) |
| met-museum | classification LIKE 'Sword Furniture%' OR 'Armor Parts%' OR 'Helmets' OR 'Mail' OR 'Firearms Accessories%' OR 'Swords-Accessories' OR 'Archery Equipment-Arrowheads' | ~2,713 (1,632 sword-furniture + 700 armor + 208 firearms-acc + 97 swords-acc + 288 arrowheads partial) |
| cataclysm-dda | source_url path matches `ammo.json` OR `tool.json` | ~905 (668 ammo + 237 tool) |
| Royal Armouries `Relics & miscellaneous` regex sweep | canonical_name regex `/scabbard|hilt|handle|stand/i` AND category_value='Relics & miscellaneous' | ~400 |
| Other-source regex sweep (canonical_name) | The 13-token regex `/cartridge|round|shell|bullet|ammo|scabbard|tsuba|kozuka|grip|guard|hilt|sheath|handle|stand/i` applied to remaining sources | ~150 (cross-source partial catches) |

**TOTAL Step 1 mutations:** ~15,119 (slightly below legolas's ~15,750 estimate; legolas's number included partial-Relics overlap). Acceptable variance.

**Post-Step-1 active substrate (rows excluded from v_category_sample once weapon_kind='ammo_or_consumable'):**
89,839 − 15,119 = **74,720 active rows in category-sampling-eligible state**.

**Acceptance verification query** (Gate d.3 — ammo boundary ≤ 1.0%):

```sql
-- Count remaining 'category' rows that still match ammo-regex
SELECT COUNT(*) AS leaked_ammo_in_category
FROM weapon_knowledge_entries
WHERE weapon_kind = 'category'
  AND (
    LOWER(canonical_name) REGEXP '\\b(cartridge|round|shell|bullet|ammo|scabbard|tsuba|kozuka|grip|guard|hilt|sheath|handle|stand)\\b'
    OR (source_library='royal_armouries'
        AND json_extract(structured_properties,'$.category_value') IN
          ('Ammunition & projectiles','Armour pieces','Complete armours','Helmets','Animal armour & equestrian equipment'))
    OR (source_library='met-museum'
        AND json_extract(structured_properties,'$.classification') LIKE 'Sword Furniture%')
  );
-- Threshold: leaked_ammo_in_category / total_category_kind <= 0.01
-- Where total_category_kind = SELECT COUNT(*) FROM weapon_knowledge_entries WHERE weapon_kind='category'.
```

SQLite doesn't ship with `REGEXP` by default. Implementation uses Python's `re.search` via the `Connection.create_function` API; the verification query becomes a Python-side fold rather than a single SQL.

### §2.2 Step 2 — F1 Royal Armouries TIERED collapse

**Rows touched:** Royal Armouries rows where weapon_kind != 'ammo_or_consumable' (after Step 1). Approximately 38,127 − 10,951 = **27,176 rows in scope**.

**Mutations:**
- `dedup_status='canonical'` for ~3,500 (per legolas M/N≈9.2% estimate; ±30% range)
- `dedup_status='merged_into'` for ~23,676 (the rows that collapse INTO canonicals)
- `variant_relationship='sub_variant_of:<parent_canonical_id>'` for merged_into rows
- New rows in `knowledge_entry_canonical_merge` (one per canonical): ~3,500 with `merged_entry_ids` JSON array

**Per-cluster per gandalf variant-cluster-policy:**

| Cluster | Variants | Rows | Canonicals after collapse | Policy |
|---|---|---|---|---|
| RA-1 | Centrefire six-shot revolver | 379 | 1 | B (collapse all 379) |
| RA-2 | Generic "Sword" | 3,155 | 150-300 (per culture × century × broad_type buckets w/ ≥3-specimen G4 threshold) | C (TIERED) |
| RA-3 | Flintlock military musket | 486 | 1 + Brown Bess/Charleville/Potsdam sub-variants | D (fuzzy-collapse + variant-preserve) |
| RA-4 | Pike/Spontoon/Halberd/Partizan | 1,687 (588+562+284+253) | 4 type-canonicals + per-type sub-collapse | A-at-top + B-within |
| RA-5 | Already in Step 1 (ammo) | — | — | — |
| Remaining RA category-rows | ~21,000 (firearms 12,140 minus ammo-tagged subset; swords 6,782 minus RA-2; staff weapons 3,269 minus RA-4 contribution; etc.) | G4 ≥3-specimen sweep | C/B mix |

**Post-Step-2 verification (per dispatch acceptance):**

```sql
SELECT COUNT(*) AS ra_canonicals
FROM weapon_knowledge_entries
WHERE source_library='royal_armouries' AND dedup_status='canonical';
-- Expect 2,500-5,000 per dispatch tolerance band.
```

**Post-Step-2 active substrate count:** 74,720 − 23,676 = **51,044 canonical-or-unprocessed rows in scope** (the 23,676 merged_into rows remain in DB but are excluded from v_category_sample via dedup_status filter).

### §2.3 Step 3 — F3 quarantine (pf2ools + souls-api)

**Rows touched:** 688 (pf2ools) + 56 (souls-api items.js) = 744.

**Mutations:**
- pf2ools: 688 rows → `source_library = 'pf2ools-pf2ools-data-quarantined'`
- souls-api items.js: 56 rows → `source_library = 'souls-api-thomaslincoln-quarantined'`

**Open Question Q4 resolution (souls-api 2 weapons.js preservation):** preserve them. The 2 confirmed-weapon rows in `weapons.js` stay as `source_library='souls-api-thomaslincoln'` (unchanged); `weapon_kind='category'`; `dedup_status='unprocessed'` (Step 7 will F4-evaluate against other soulslike daggers/etc.). Rationale: 3.4% TP preservation costs zero — it's per-row source_library rename, not per-source. Quarantine selectively by source_url path.

**Archive creation:**
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/quarantine-archives/pf2ools-quarantine-2026-05-23.jsonl.gz` (entries + linked reference images)
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/quarantine-archives/souls-api-thomaslincoln-quarantine-2026-05-23.jsonl.gz` (56 items.js rows only; 2 weapons.js NOT archived)
- README.md amendment in `quarantine-archives/` documenting both quarantines (mirroring wikipedia-unfiltered pattern; references legolas's per-source-quality.md confirmation 100% and 96.6% non-weapon)

**No DELETE.** Discipline #11 audit-preservation: archived rows remain in DB with renamed source_library; v_category_sample filter excludes them.

**Post-Step-3 active substrate:** 89,839 − 688 − 56 = **89,095 rows** in non-quarantined source_libraries (2 souls-api weapons.js preserved + others unchanged). Phase A audit baseline (89,093-89,095) confirmed.

### §2.4 Step 4 — named_template routing

**Rows touched:** all rows in TRPG/MMO/ARPG/soulslike source-libraries: ~22,000 rows.

| Source | Rows | Expected named_template tagging |
|---|---|---|
| nick-aschenbach-dnd-data | 6,297 | ~4,408 (70% per legolas Deliverable 1) |
| wow-classic-items | 4,440 | ~1,332 (30%) |
| bsdata-warhammer-aos | 2,183 | ~1,856 (85%) |
| osrsbox-db | 940 | ~564 (60%) |
| diablo2-d2data | 521 | ~156 (30%) |
| path-of-exile-repoe | 494 | ~49 (10%) |
| fextralife (4 sources) | 966 | ~676 (70%) |
| bloqhead-demigods | 320 | ~320 (100%) |
| elden-ring-erdb | 307 | ~307 (100%) |
| pf2ools-quarantined | 688 | 0 (quarantined — skip per v_category_sample filter logic) |
| 5e-bits-2014 + 2024 | 147 | 0 (all SRD generics → category) |
| souls-api (2 surviving) | 2 | 0 (those 2 are weapons.js → category) |

**Total named_template mutations:** ~9,668 (legolas estimate ~9,500-11,000; consistent).

**G1 (WIKI-3 game-tier Gladius) operationalization:** when routing TRPG/MMO/ARPG, retain per-game Gladius rows as separate `named_template` canonicals (D2, PoE, WoW each get their own canonical entry with `weapon_kind='named_template'`). Cross-source F4 merge in Step 7 will handle whether they collapse further; per Matt G1-lock, they stay per-game.

**G5 (WIKI-2 OSRS Excalibur) operationalization:** OSRS `Excalibur` row → `weapon_kind='named_template'` + `related_entries`-link to mythological-unique Excalibur canonical. Does NOT inherit the unique allowlist match.

**G3 (AOS-2 compound entry) operationalization:** the compound row "Skull Bludgeon and Varanspire Gladius" is detected by name-pattern (contains " and " connecting two weapon-type words). For this row:
- Insert two NEW rows: `Skull Bludgeon` and `Varanspire Gladius`, each as their own `named_template` with full source_url provenance pointing back to the original compound entry's source
- Original row stays in DB; `weapon_kind='named_template'`; `variant_relationship='model_line_sibling_of:<child1_id>,<child2_id>'`
- Both children have `variant_relationship='sub_variant_of:<original_compound_id>'`
- The split is recorded as a special-case migration; full audit trail in completion record

**Acceptance verification:**

```sql
-- Count category-tagged TRPG/MMO/ARPG rows that match named_template detection criteria
SELECT COUNT(*) AS leaked_named_template_in_category
FROM weapon_knowledge_entries
WHERE weapon_kind = 'category'
  AND source_library IN (
    'nick-aschenbach-dnd-data','5e-bits-5e-database','5e-bits-5e-database-2024',
    'bsdata-warhammer-aos','fextralife-elden-ring','fextralife-ds1','fextralife-ds2','fextralife-ds3',
    'bloqhead-demigods','elden-ring-erdb','diablo2-d2data','path-of-exile-repoe',
    'osrsbox-db','wow-classic-items'
  )
  AND (
    json_extract(structured_properties,'$.rarity') IN
      ('Uncommon','Rare','Very Rare','Legendary')
    OR LENGTH(canonical_name) - LENGTH(REPLACE(LOWER(canonical_name),' ','')) >= 1  -- multi-word
  );
-- Threshold: leaked / total_trpg_category_rows <= 0.05 (gandalf § 4.5 named_template ≤ 5%)
```

**Post-Step-4 row-state:** 9,668 rows now have `weapon_kind='named_template'`. Active substrate unchanged in count (mutations are tagging, not removal).

### §2.5 Step 5 — FP removal + brand-prefix disambiguation

**Rows touched:** scattered FPs + brand-prefix candidates. Estimated ~1,650 rows total in scope.

| FP source | Detection | Mutations |
|---|---|---|
| gta-v-data Invalid placeholders | canonical_name = 'Invalid' OR LIKE 'Invalid%' OR LIKE '%placeholder%' OR LIKE '%test%' | 37 rows → `weapon_kind='unknown'` + `dedup_status='canonical'` (audit-flag; no category sampling, no merge target); cluster_id will route to FP-quarantine via flagged-clusters doc |
| Royal Armouries Art category | structured_properties.category_value='Art' | 658 rows → `weapon_kind='unknown'` (pure FP; not weapons; not ammo-adjacent; remain in DB per audit-preservation) |
| Met Museum equestrian + works-on-paper + miscellaneous-non-weapons | classification IN ('Equestrian Equipment-Spurs','Equestrian Equipment-Stirrups','Equestrian Equipment-Bits','Equestrian Equipment-Saddles','Works on Paper-Prints','Works on Paper-Drawings','Miscellaneous-Badges') | ~580 → `weapon_kind='unknown'` |
| fextralife enemy/NPC + category-index | URL pattern + name signal | ~50 → `weapon_kind='unknown'` or 'category' depending |
| wikidata loose-Q (P31 chain check) | run Q-item check via stored wikidata_qid; if Q-item is NOT in Q728-subclass tree, flag | ~250 → `weapon_kind='unknown'` |
| wikipedia v2 redirect + disambiguation | description_text contains 'REDIRECT' or is < 50 chars AND URL contains disambig hint | ~100 → `weapon_kind='unknown'` |

**Brand-prefix disambiguation (per Matt G2-pattern principle):**

Apply NEGATIVE-LOOKAHEAD overrides per legolas's detection-rule refinement § 4:

```python
BRAND_PREFIX_PATTERNS = [
    r'^[A-Z]+\d+\s+(?:Excalibur|Aegis|Tyrfing|Durandal|Mjolnir|Gungnir)\b',
    r'^[A-Z][a-z]+\s+(?:Aegis|Excalibur|Durandal|Tyrfing)\b',
    r'\([a-z]+\)$',  # parenthetical qualifier like "(comics)" "(rifle)" "(pistol)"
    r'\s+(?:rifle|pistol|missile|bomb|shell|tank)$',
    r'^[A-Z][a-z]+\s+(?:Katana|Sword|Dagger|Mace|Axe|Bow|Spear|Hammer|Shield)\b',  # G2-pattern prefix-modifier
]
```

For each row where canonical_name matches a brand-prefix pattern AND the embedded name is in the unique allowlist:
- `weapon_kind='category'` (or 'named_template' for game-source rows with rarity-signal)
- NOT `weapon_kind='unique'`

Specific G2-disposition cases (Matt-principle):
- `M982 Excalibur` → category (modern artillery; brand-prefix M982)
- `Excalibur rifle` → category (parenthetical-qualifier `(rifle)` pattern; bare "Excalibur rifle" name)
- `Kimber Aegis` → category (brand-prefix Kimber)
- `Mjolnir (comics)` → named_template (parenthetical-qualifier `(comics)`)
- `Narsil` (wikipedia REDIRECT) → `weapon_kind='unknown'`; flag for removal (redirect row, not substantive article)

**Acceptance verification:**

```sql
-- Re-fire Phase A audit methodology: stratified N=50 per source × 24 sources
-- (excluding pf2ools-quarantined + souls-api-thomaslincoln-quarantined)
-- Compute new FP rate post-Step-5
-- Threshold: <= 1.5% target; <= 3.0% hard.
-- Implementation: Python-side classification re-run + judgment;
-- comparison against pre-Phase-D legolas baseline of 2.83% total / 2.08% post-F3
```

**Post-Step-5 estimated FP rate:** ~0.4% (from legolas's "Phase D actions required" calculation in cleanliness-baseline § Gate(a)).

### §2.6 Step 6 — unique detection + named-unique allowlist application

**Rows touched:** all rows where `weapon_kind='unknown'` OR (`weapon_kind='category'` AND row is from museum/wikidata/wikipedia source-libraries) — approximately ~30,000 rows in detection scope.

**Allowlist scan (26 entries: 16 gandalf-original + 10 legolas-additions):**

For each allowlist entry, search canonical_name with case-insensitive match, BUT only fire `weapon_kind='unique'` when:
1. Bare match (no brand-prefix per Step 5 patterns) AND
2. Signal A (single-or-few capitalized words, no generic-type-noun) per gandalf § 3.5 AND
3. (Signal B [royal/imperial ownership] OR Signal C [Wikidata Q-item is specific object, not class])

**Expected unique mutations:** ~150-300 rows (per Phase A Gate (d.1) baseline ≈ 0.2-0.3% of substrate).

Per-source breakdown:
- wikidata: ~26 confirmed (from legolas Named-Unique-Verification + 10 additions, minus brand-prefix collisions)
- wikipedia: ~26 confirmed (same set)
- royal_armouries: ~50-200 estimated (per gandalf § 3.4); detected via Signal B regex on description + name
- met-museum: ~10-50 estimated (Halberd of Archduke Ferdinand-style attribution); detected via Signal B
- osrsbox-db: 0 (per G5: OSRS Excalibur → named_template, not unique)
- Other sources: 0-2 (negligible)

**G2-pattern explicit exclusions applied:** the following allowlist matches are routed AWAY from `unique`:
- `M982 Excalibur` → category (Step 5 pre-emptive)
- `Excalibur rifle` → category
- `Kimber Aegis` / `Kimber Aegis II` → category
- `Mjolnir (comics)` → named_template
- `Guthix mjolnir` / `Saradomin mjolnir` / `Zamorak mjolnir` (OSRS) → named_template per G5
- `Ulfberht swords` (wikipedia article on the CLASS) → category (museum/encyclopedia article on a class)
- `Kusanagi no Tsurugi` (wikipedia variant) → unique (allowlist hit + Signal A; F4 in Step 7 will merge with wikidata `Kusanagi`)
- `Narsil` (wikipedia redirect) → unknown + flag (per Step 5)

**Acceptance verification:**

```sql
-- Audit-sample of category-tagged rows for known-named-unique slip-throughs
SELECT canonical_name, source_library, json_extract(structured_properties,'$.classification') AS clf
FROM weapon_knowledge_entries
WHERE weapon_kind = 'category'
  AND canonical_name IN (
    'Joyeuse','Curtana','Excalibur','Mjolnir','Gungnir','Gáe Bulg','Aegis','Tizona','Colada',
    'Szczerbiec','Honjō Masamune','Mikazuki Munechika','Kusanagi','Reichsschwert','Sword of Goujian',
    'Battersea Shield','Witham Shield',
    'Tyrfing','Fragarach','Caladbolg','Gram','Ruyi Jingu Bang','Sudarshana Chakra','Gandiva','Skofnung','Shield of Achilles'
  );
-- Expect 0 rows (or only G2-pattern justified cases like M982/Kimber/comics).
```

Threshold: category-vs-unique boundary ≤ 2.0% (gandalf § 4.5). Post-Phase-A baseline already at 0.2-0.3%; Phase D maintains.

### §2.7 Step 6.5 — Canonical taxonomy normalization (CRITICAL Amendment #1)

**Rows touched:** all 89,839 rows (full-scan normalization pass).

**Mutations:**
- `cultural_lineage_canonical` populated for ≥ 70% of `v_category_sample` rows (per gandalf § 4.4 floor applied to canonical column)
- `historical_period_canonical` populated for ≥ 60% of v_category_sample rows
- `register_canonical` populated for ≥ 95% of v_category_sample rows
- `cultural_lineage_confidence` populated [0.0, 1.0] per gandalf § 5.3 confidence ladder

**Per-source mapping pipeline (per gandalf § 5.2):**

Implementation strategy — single Python pass with per-source mapping function dispatched on `source_library` value:

```python
def normalize_row(row):
    src = row['source_library']
    rl = ROW_LANGUAGE_DISPATCH.get(src, default_lineage_mapper)
    canonical_lineage, lineage_conf = rl(row)

    period_canonical = period_mapper(row)  # uses structured_properties.objectBeginDate
                                            # / inception P571 / Royal Armouries date / etc.

    register_canonical = REGISTER_BY_SOURCE.get(src, 'unknown')
    # Override: if row was tagged unique AND name in mythological-allowlist subset → 'mythological'
    if row['weapon_kind'] == 'unique' and is_mythological(row['canonical_name']):
        register_canonical = 'mythological'

    return canonical_lineage, lineage_conf, period_canonical, register_canonical
```

**Acceptance verification queries:**

```sql
-- Gate (c) on v_category_sample:
SELECT
  100.0 * SUM(CASE WHEN cultural_lineage_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*)
    AS pct_cultural_populated,
  100.0 * SUM(CASE WHEN historical_period_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*)
    AS pct_period_populated,
  100.0 * SUM(CASE WHEN register_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*)
    AS pct_register_populated
FROM v_category_sample;
-- Thresholds: cultural >= 70%; period >= 60%; register >= 95%.
```

**Post-Step-6.5 state:** canonical taxonomy populated for axis-discovery and Step 7 blocking. Field coverage gate (c) verified non-degraded.

### §2.8 Step 7 — F4 cross-source canonical merge

**Rows touched:** all canonical-or-unprocessed rows post-Steps-1..6.5: estimated ~51,000 - 23,676 + 9,668 named_template (which CAN merge cross-source per F4) ≈ **~37,000 unique-canonicals + ~9,668 named_template = ~47,000 rows in F4 scope**.

**Algorithm:**

1. **Blocking step:** group rows by `(weapon_subclass_inferred, cultural_lineage_canonical)`.
   - `weapon_subclass_inferred` derived from canonical_name patterns + structured_properties: "katana", "dagger", "sword", "longbow", "pistol", "revolver", "AK_family", etc. ~50-80 canonical subclass labels.
   - Within each block, compute pairwise candidates only.
   - Expected block sizes: max ~3,000 (Sword/European/medieval); typical 50-500.
   - Total pairwise candidates: ≈ Σ blocks (n choose 2) ≈ 5-10 million pairs (down from 89K² ≈ 8 billion).

2. **Per-pair scoring:**
   - `name_sim` = Levenshtein-normalized canonical_name similarity (case-insensitive; strip parenthetical-qualifier)
   - `desc_cos` = cosine similarity on description-embedding (sentence-transformer, 384-dim)
   - `cross_source` = pair has rows from ≥ 2 distinct source_library values
   - `wikidata_corroborated` = both rows have non-null source_id (wikidata_qid path) OR one matches the other's structured_properties.wikidata_qid

3. **Merge condition:** `(name_sim >= 0.90) OR (name_sim >= 0.75 AND desc_cos >= 0.85)` AND `(cross_source OR wikidata_corroborated)`.

4. **Three-lane router for CS-1 (Katana) + CS-2 (Dagger) + generalized to high-cross-source canonicals:**
   - **Historical lane:** museum (royal_armouries, met-museum) + wikidata + wikipedia + historical-period_canonical NOT IN ('fictional') → merge to single historical canonical.
   - **Game-category lane:** game-source rows with game-specific lore → KEEP-ALL per Policy A (G1 + G5 + Matt G2-principle confirms; per-game-source canonical retained; cross-link via related_entries).
   - **Named_template lane:** D&D / TRPG rows → per-source-canonical retained; cross-source merge only if name + description both align ≥ 0.95.

5. **Caliber-bucket logic for WIKI-4 AK family (and generalized to FN FAL, G3, M-16/AR-15 families if surfaced):**
   - Bucket by `structured_properties.caliber` field (or extract from description regex if not structured).
   - Collapse same-caliber-same-mechanical-pattern within bucket via Policy B.
   - KEEP-ALL across calibers (AK-47/AKM bucket; AK-74/AK-74M bucket; AK-12; AK-15; AK-103; AK-203).
   - Net: 9 ODIN AK rows → 6 canonicals.

6. **G2 (SOULS-1 Dagger) auto-disposition (Matt-principle):**
   - Per Matt's G2-pattern principle, bare-category-name across sources (SOULS-1 daggers in DS1/DS2/DS3/ER fextralife) → preserve per-source as `weapon_kind='category'`; cross-link via `related_entries`; do NOT auto-merge.
   - **No surface-to-Matt** required; documented in `phase-D-flagged-clusters.md` as MATT-PRINCIPLE-DISPOSITIONED.
   - Similar generalization to any other 0.80-0.85 borderline cases that match the same pattern (bare category-name; multiple game-sources; per-game lore distinct).

**Open Question Q5 (embedding model) resolution:**

Use `sentence-transformers/all-MiniLM-L6-v2` (384-dim; ~80 MB model; runs in 1-2 hours on 47K descriptions on CPU; well-established as the default sentence-transformer baseline; reproducible via pinned model version `1.0.4` or current stable). Rationale:
- 384-dim is sufficient for the cross-source weapon-description similarity task (descriptions are short ~50-500 chars; semantic-equivalence not domain-specific reasoning).
- Pretrained on 1B sentence pairs; generalizes to weapon-description English.
- Reproducible: model checksum recorded in math note; embeddings serialized to `text_embedding` BLOB column post-fire.
- Alternative considered: `all-mpnet-base-v2` (768-dim, 3x slower, marginally better quality) — rejected as overkill for this task and 3x compute cost.

**Acceptance verification:**

```sql
-- Gate (b) dual verification per jack-ryan Gate-1 Amendment #2:

-- (i) Residual duplication
WITH canon AS (
  SELECT canonical_name, COUNT(*) AS n
  FROM weapon_knowledge_entries
  WHERE dedup_status = 'canonical'
  GROUP BY canonical_name
)
SELECT
  (SELECT COUNT(*) FROM weapon_knowledge_entries WHERE dedup_status='canonical') AS canonical_count,
  (SELECT COUNT(DISTINCT canonical_name) FROM weapon_knowledge_entries WHERE dedup_status='canonical') AS distinct_canon_names,
  CAST((SELECT COUNT(*) FROM weapon_knowledge_entries WHERE dedup_status='canonical') AS REAL) /
    (SELECT COUNT(DISTINCT canonical_name) FROM weapon_knowledge_entries WHERE dedup_status='canonical') - 1.0
    AS residual_dup_ratio;
-- Threshold: residual_dup_ratio <= 0.04

-- (ii) Dedup recall
SELECT
  CAST((SELECT COUNT(*) FROM weapon_knowledge_entries WHERE dedup_status='merged_into') AS REAL) / 42253.0 AS recall;
-- Threshold: recall >= 0.92
-- Denominator 42,253 = 89,839 total - 47,586 distinct (legolas Phase A baseline)
```

**Post-Step-7 estimated state:** ~7,000-10,000 canonicals across 89,839 source rows; ~42,000-44,000 rows with `dedup_status='merged_into'`; residual duplication ≤ 4% target.

---

## §3 — Acceptance gate verification queries (consolidated)

All 4 overall gates re-stated with their pre-authored verification SQL. Each gate's pass/fail is computed at end-of-pipeline (or per-step where applicable).

### §3.1 Gate (a) — FP rate in active substrate ≤ 3.0% hard / ≤ 1.5% target

Implementation: re-fire legolas Phase A audit methodology on a stratified N=50 per source × (24 − 2 quarantined) = 22 sources = 1,100 sample.

```python
# Pseudocode (Python; runs after Step 7):
sample = []
for src in all_active_source_libraries:
    src_rows = query(f"SELECT * FROM weapon_knowledge_entries WHERE source_library='{src}' AND dedup_status='canonical' LIMIT 50")
    sample.extend(src_rows)

fp_count = sum(1 for r in sample if classify_fp(r))  # rule-based FP detection
fp_rate = fp_count / len(sample)
assert fp_rate <= 0.03, f"FP rate {fp_rate:.2%} exceeds hard ceiling 3.0%"
print(f"FP rate target check: {fp_rate:.2%} (target ≤ 1.5%)")
```

### §3.2 Gate (b) — Within-canonical-merge duplication ≤ 4.0% residual / ≥ 92% recall

Per Amendment #2 dual verification — see § 2.8 above.

### §3.3 Gate (c) — Field-coverage floors NO DEGRADATION

```sql
-- Run after Step 6.5 + Step 7 against v_category_sample:
SELECT
  100.0 * SUM(CASE WHEN structured_properties IS NOT NULL AND structured_properties != '{}' THEN 1 ELSE 0 END) / COUNT(*) AS pct_structured,
  100.0 * SUM(CASE WHEN description_text IS NOT NULL AND description_text != '' THEN 1 ELSE 0 END) / COUNT(*) AS pct_description,
  100.0 * SUM(CASE WHEN cultural_lineage_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*) AS pct_cultural,
  100.0 * SUM(CASE WHEN historical_period_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*) AS pct_period
FROM v_category_sample;
-- Thresholds: structured >= 95%; description >= 85%; cultural >= 70%; period >= 60%.
```

### §3.4 Gate (d) — `weapon_kind` mis-classification ≤ per-dim thresholds

Three sub-gates re-fired post-Step-6:

```sql
-- (d.1) category-vs-unique boundary ≤ 2.0%
-- Stratified sample of category rows; count known-named-unique slip-throughs.

-- (d.2) category-vs-named_template boundary ≤ 5.0%
SELECT COUNT(*) AS leaked_named_template_in_category
FROM weapon_knowledge_entries
WHERE weapon_kind='category'
  AND source_library IN ([TRPG/MMO/ARPG sources])
  AND <named_template_detection_pattern>;
-- Compare to total category-kind rows in TRPG/MMO/ARPG sources.

-- (d.3) category-vs-ammo_or_consumable boundary ≤ 1.0%
SELECT COUNT(*) AS leaked_ammo_in_category
FROM weapon_knowledge_entries
WHERE weapon_kind='category'
  AND <ammo_regex_or_classification_pattern>;
```

---

## §4 — Idempotency guarantees per step (Open Question Q1 resolution)

**Master principle:** every step is set-classification-if-condition (no row-deletion; no destructive collapse). Re-running a step on an already-processed row is a no-op (the conditional sets the same value or skips because the mutation already happened).

| Step | Idempotency strategy |
|---|---|
| Schema migration (§ 1) | PRAGMA-guarded ALTER + sqlite_master-guarded CREATE VIEW. Re-run is no-op. |
| Step 1 (ammo tagging) | `UPDATE ... SET weapon_kind='ammo_or_consumable' WHERE weapon_kind != 'ammo_or_consumable' AND <detection_rule>`. Re-run: WHERE clause filters out already-tagged rows. Net effect: idempotent. |
| Step 2 (F1 RA collapse) | Each row gets `dedup_status='canonical'` OR `dedup_status='merged_into'` exactly once. Re-run: `UPDATE ... WHERE dedup_status='unprocessed' AND source_library='royal_armouries'`. Already-processed rows skipped. **Special handling for `knowledge_entry_canonical_merge` table inserts:** check by `canonical_name + source_library` uniqueness before INSERT. Re-run: INSERT OR IGNORE pattern. |
| Step 3 (F3 quarantine) | Source-library rename: `UPDATE ... SET source_library='pf2ools-pf2ools-data-quarantined' WHERE source_library='pf2ools-pf2ools-data'`. Re-run: rows already renamed are filtered out by WHERE clause. Archive file: check existence before write; if exists, skip + log; if absent, create. Re-run on existing archive: no-op. |
| Step 4 (named_template routing) | `UPDATE ... SET weapon_kind='named_template' WHERE weapon_kind IN ('unknown','category') AND source_library IN [list] AND <named_template_detection>`. AOS-2 split: check if child rows already exist by (canonical_name, source_url) UNIQUE constraint; INSERT OR IGNORE. Re-run: idempotent. |
| Step 5 (FP removal + brand-prefix) | `UPDATE ... SET weapon_kind='unknown' WHERE weapon_kind != 'unknown' AND <FP_or_brand_prefix_detection>`. Re-run: rows already moved to 'unknown' filtered out. |
| Step 6 (unique detection + allowlist) | `UPDATE ... SET weapon_kind='unique' WHERE weapon_kind != 'unique' AND canonical_name IN [allowlist] AND NOT <brand_prefix_pattern>`. Re-run: idempotent. |
| Step 6.5 (canonical taxonomy normalization) | Per-row `UPDATE` to populate `cultural_lineage_canonical`, `historical_period_canonical`, `register_canonical`, `cultural_lineage_confidence`. The mapping is deterministic per source_library + structured_properties content. Re-run: produces same value → idempotent overwrite. **Note:** confidence ladder treats re-run as overwriting with same confidence; no degradation. |
| Step 7 (F4 merge) | Most complex idempotency. Strategy: (a) if row is `dedup_status='canonical'` and a candidate merge to another canonical is found in re-run, the re-run is a no-op IF the candidate match was already evaluated (track via `knowledge_entry_canonical_merge.merge_strategy` audit field). (b) If `dedup_status='merged_into'`, re-run skips (already merged). (c) Row-order sensitivity: blocking + pairwise comparison is order-INDEPENDENT (all pairs scored deterministically against threshold; merges committed in batch); however the choice of which row in a merge-set becomes the canonical-survivor IS order-dependent (default: lowest `id` survives). Re-run on already-processed clusters: skip via `knowledge_entry_canonical_merge` existence check on `merged_entry_ids` containing the row. **Embedding cache:** `text_embedding` BLOB is computed once and cached; re-run reuses cached embeddings (no re-compute). |

**Random-seed reproducibility:** any step using randomness (e.g., if Step 7 needs tiebreaking on equal-similarity pairs) uses `random.seed(20260523)` fixed seed. Documented in completion summary.

---

## §5 — Rollback plan per step (Open Question Q3 resolution)

**Master strategy:** SQLite file-level snapshot before each destructive step. Backups stored at `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/backups/`.

| Step | Backup before fire | Rollback path |
|---|---|---|
| Schema migration | `cp telemetry.db backups/telemetry.db.pre-schema-migration-2026-05-23` | Restore file copy. Per ADR-006, restoration requires Matt authorization; whole-pipeline authorization covers in-pipeline rollback decisions. |
| Step 1 (ammo tagging) | `cp telemetry.db backups/telemetry.db.pre-step1` | Restore OR (preferred) reverse-UPDATE: `UPDATE ... SET weapon_kind='unknown' WHERE weapon_kind='ammo_or_consumable' AND imported_at >= '2026-05-23'` (won't work because `imported_at` predates Phase D; safer is restore from snapshot). |
| Step 2 (F1 RA collapse) | `cp telemetry.db backups/telemetry.db.pre-step2` | Restore (rollback of the `knowledge_entry_canonical_merge` inserts + `dedup_status` mutations is non-trivial; snapshot is the reliable path). |
| Step 3 (F3 quarantine) | `cp telemetry.db backups/telemetry.db.pre-step3` PLUS retain quarantine-archive files unchanged | Reverse-UPDATE on source_library rename: `UPDATE ... SET source_library='pf2ools-pf2ools-data' WHERE source_library='pf2ools-pf2ools-data-quarantined'`. Archive files remain available; safe. |
| Step 4 (named_template) | `cp telemetry.db backups/telemetry.db.pre-step4` | Restore (AOS-2 child-row inserts are non-trivial to reverse cleanly). |
| Step 5 (FP removal) | `cp telemetry.db backups/telemetry.db.pre-step5` | Restore. |
| Step 6 (unique detection) | `cp telemetry.db backups/telemetry.db.pre-step6` | Restore. |
| Step 6.5 (canonical taxonomy) | `cp telemetry.db backups/telemetry.db.pre-step6.5` | Restore. |
| Step 7 (F4 merge) | `cp telemetry.db backups/telemetry.db.pre-step7` (CRITICAL — most destructive step) | Restore. Embedding cache (`text_embedding` BLOB) survives restore if backup taken AFTER embedding-pass populated. |

**Per-step backup size:** ~136 MB → ~250 MB (post-classification growth from cluster_id + canonical-merge rows). 9 backups × 250 MB ≈ 2.3 GB total. Stored locally; not committed to git (DB file size precedent: already gitignored).

**Backup retention:** keep all backups until milestone-tag `v0.2-weapon-library-substrate-cleaned` is Matt-approved. After milestone tag, prune pre-step-1 through pre-step-6.5 backups; retain pre-step-7 backup as the "before F4" canonical snapshot for the next 30 days.

---

## §6 — Open Question resolutions (full enumeration; Q1-Q7 per dispatch + Amendment #5)

### §6.1 Q1 — Idempotency strategy per step

See § 4 above. Each of 7 steps is naturally idempotent via WHERE-clause filtering on already-processed state. Step 7 (F4 merge) idempotency relies on `knowledge_entry_canonical_merge` lookup + `dedup_status` state check.

### §6.2 Q2 — VACUUM strategy

**Decision:** Single VACUUM at end-of-pipeline only (after Step 7 + acceptance-gate verification + flagged-clusters surface + completion summary). Rationale:
- Mid-pipeline VACUUM is high-disk-cost (rewrites the full DB; doubles disk-IO during run).
- The 136 → ~250 MB intermediate growth is well within disk capacity (no fragmentation concerns at this scale).
- Single end-of-pipeline VACUUM reclaims any disk fragmentation from the canonical-merge INSERTs + UPDATEs in one efficient pass.
- VACUUM cost: estimated 5-10 minutes on 250 MB DB. Acceptable.

**No VACUUM after Step 3 quarantine renames** (just source_library rename; no row count change; no disk fragmentation from these mutations).

### §6.3 Q3 — Backup strategy

See § 5 above. Pre-step file-level copies; 9 backups; ~2.3 GB total disk; retention to milestone-tag.

### §6.4 Q4 — Step 3 souls-api 2-row preservation

**Decision:** Preserve. The 2 confirmed-weapon rows in souls-api `weapons.js` (DRAGON GREATSWORD + 1 other) stay `source_library='souls-api-thomaslincoln'` (unchanged); become `weapon_kind='category'` in Step 1 if they pass detection; Step 7 F4-evaluates them against other soulslike-weapon canonicals.

Rationale: per-row source_url path filter is mechanical (1-line WHERE clause); preserves 3.4% true-positive at zero cost. Loss-avoidance > simplicity.

**Implementation:**

```sql
UPDATE weapon_knowledge_entries
SET source_library = 'souls-api-thomaslincoln-quarantined'
WHERE source_library = 'souls-api-thomaslincoln'
  AND source_url LIKE '%items.js%';
-- 2 weapons.js rows unaffected.
```

### §6.5 Q5 — Embedding model choice

See § 2.8 above. **`sentence-transformers/all-MiniLM-L6-v2` v1.0.4** (384-dim). Reproducible via pinned model SHA recorded in completion summary.

### §6.6 Q6 — Anchor-test execution

**Decision:** SKIP in Phase D. Defer to Phase E pilot validation.

Rationale: gandalf § 6.3 criterion 4 (anchor-test) requires sample-generation + human-judgment loop ("would the generated player-facing kit be more interesting / coherent"). Phase D does not have a generation pipeline; can't fire the anchor-test without invoking the engine + cohesion-judge. Phase E (Pattern-6 axis discovery + rocket-side generation pilot) is the natural place.

**Documented in `phase-D-flagged-clusters.md`:** the 3 Matt-flagged variant-clusters (RA-2 threshold, AOS-2 split, soulslike Dagger borderline) get my Matt-principle dispositions explicitly; if Phase E reveals anchor-test signal that contradicts a Phase D disposition, the Phase D-bis hook (Q7) re-engages.

### §6.7 Q7 — Phase D-bis trigger

**Hook design:** Phase D produces a re-runnable subset called `phase-D-bis-hook.md` at completion. It documents:
1. Which steps' classifications might be revisited if Phase E surfaces unexpected axes (likely Steps 5-7 — FP removal, unique detection, F4 merge)
2. Per-step re-fire pseudocode (using the existing idempotency model)
3. Backup-state references (which pre-step backup to restore from if a hard revert is needed)

If Phase E (rocket + legolas Pattern-6) discovers an axis that Phase D collapsed away (e.g., the dirty probe surfaces an axis the F4 merge destroyed), Matt or gandalf instructs me to re-engage Steps 5-7 with adjusted detection rules.

The hook itself is NOT executed in Phase D; only documented.

---

## §7 — Execution sequence summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Phase D pipeline execution                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [0] Author MIGRATION.md (cross-seam analysis; grep consumers)     │
│         ↓                                                           │
│  [1] Schema migration (9 ALTER + 3 CREATE VIEW; idempotent)        │
│      Backup: pre-schema-migration                                   │
│      Smoke test: PRAGMA + view existence + null-default check       │
│         ↓                                                           │
│  [2] Step 1 — ammo_or_consumable tagging                            │
│      Backup: pre-step1 ; Mutations: ~15,119 rows                   │
│      Gate (d.3) verify: ≤ 1.0% boundary error                       │
│         ↓                                                           │
│  [3] Step 2 — F1 Royal Armouries TIERED collapse                   │
│      Backup: pre-step2 ; Mutations: ~3,500 canonical / ~23,676 merged │
│      Verify: 2,500-5,000 RA canonicals                              │
│         ↓                                                           │
│  [4] Step 3 — F3 quarantine (pf2ools + souls-api items.js)         │
│      Backup: pre-step3 ; Mutations: 688 + 56 source_library renames │
│      Archive: 2 .jsonl.gz files + README.md amendment               │
│      Verify: active substrate = 89,095                              │
│         ↓                                                           │
│  [5] Step 4 — named_template routing                                │
│      Backup: pre-step4 ; Mutations: ~9,668 rows; AOS-2 split        │
│      Gate (d.2) verify: ≤ 5.0% boundary error                       │
│         ↓                                                           │
│  [6] Step 5 — FP removal + brand-prefix disambiguation              │
│      Backup: pre-step5 ; Mutations: ~1,650 rows                     │
│      Gate (a) verify: FP rate ≤ 1.5% target                         │
│         ↓                                                           │
│  [7] Step 6 — unique detection + allowlist application              │
│      Backup: pre-step6 ; Mutations: ~150-300 rows                   │
│      Gate (d.1) verify: ≤ 2.0% boundary error                       │
│         ↓                                                           │
│  [8] Step 6.5 — Canonical taxonomy normalization (CRITICAL Amend#1) │
│      Backup: pre-step6.5 ; Mutations: ~70-95% of 89K rows           │
│      Gate (c) verify: NO DEGRADATION on coverage floors             │
│         ↓                                                           │
│  [9] Step 7 — F4 cross-source canonical merge                       │
│      Backup: pre-step7 ; Embedding compute: ~1-2 hr / 47K rows      │
│      Three-lane router + caliber-bucket + G2-principle disposition  │
│      Gate (b) verify: ≤ 4.0% residual + ≥ 92% recall                │
│         ↓                                                           │
│  [10] Author phase-D-flagged-clusters.md                            │
│       (RA-2 G4-threshold result; AOS-2 split outcome;               │
│        SOULS-1 G2-principle disposition; any Step-7 borderlines)    │
│         ↓                                                           │
│  [11] Author phase-D-completion-summary.md                          │
│       (per-step row-impact deltas; per-gate pass/fail;              │
│        Matt-principle dispositions; Phase D-bis hook)               │
│         ↓                                                           │
│  [12] VACUUM (single end-of-pipeline pass)                          │
│         ↓                                                           │
│  [13] Commit + tag elrond/phase-D-cleaning-pipeline-2026-05-23      │
│         ↓                                                           │
│  [14] Append completion record to dispatch file                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## §8 — What gets committed to git

| Path | Content |
|---|---|
| `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-math-note.md` | THIS DOC |
| `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/MIGRATION.md` | Cross-seam analysis (Task 3) |
| `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/scripts/*.py` | Pipeline scripts (curation/migration tool scripts per AGENTS.md ; NOT production code) |
| `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-flagged-clusters.md` | Matt-principle dispositions + any post-execution Matt-review items |
| `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-completion-summary.md` | Per-step deltas + per-gate pass/fail + Phase D-bis hook |
| `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-bis-hook.md` | Re-runnable subset documentation per Q7 |
| `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/quarantine-archives/pf2ools-quarantine-2026-05-23.jsonl.gz` | F3 archive |
| `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/quarantine-archives/souls-api-thomaslincoln-quarantine-2026-05-23.jsonl.gz` | F3 archive |
| `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/quarantine-archives/README.md` | Amendment to existing README with both new quarantines |

**NOT committed:**
- DB file (`telemetry.db`) — gitignored per loadout repo convention
- Pre-step backup files (`.db.pre-step1`, etc.) — stay local; pruned to pre-step7 only after milestone-tag

---

## §9 — Cross-references

- Dispatch: `agentic_orchestration/dispatches/2026-05-23-elrond-phase-D-cleaning-pipeline.md`
- Gate-1 review: `agentic_orchestration/dispatches/2026-05-23-jack-ryan-gate-1-phase-D-dispatch.md` (5 amendments applied)
- gandalf Phase B: `canonical/story/cleaning-policy-design-2026-05-22.md` § 1.5 / § 3.3-3.5 / § 4 / § 5 / § 6 / § 7
- gandalf variant-cluster policy: `canonical/story/variant-cluster-policy-assignments-2026-05-23.md`
- legolas Phase A: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/{per-source-quality, variant-clusters, named-unique-verification, cleanliness-baseline}.md`
- Schema: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0
- Disciplines: #1 math-before-code; #11 audit-preservation; #19 right tool / smoke-test; #20 robots.txt
- ADRs: ADR-001 (team topology); ADR-004 (cross-seam MIGRATION.md); ADR-006 (external-write authorization); ADR-007 (survey-mode)

---

**Signed:** elrond (data steward; Phase D Pattern-B executor)
**Authority:** Matt 2026-05-23 (whole-pipeline upfront + G2-pattern delegation)
**Next:** MIGRATION.md (cross-seam consumer verification) → schema migration → 7-step pipeline → acceptance gates → flagged-clusters + completion summary → tag.
