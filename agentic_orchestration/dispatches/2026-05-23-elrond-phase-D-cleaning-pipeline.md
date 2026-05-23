# Dispatch — 2026-05-23 — elrond — Phase D cleaning pipeline (schema migration + 7-step cleaning execution + acceptance verification)

**From:** knight-rider
**To:** elrond (data steward; external/cross-cutting data layers; curation pipelines)
**Approved by:** Matt 2026-05-23 (G1-G5 gandalf leans accepted; F1-F6 prior-locked; Phase A empirical baselines validated; Phase B policy framework locked)
**Estimated effort:** 3-5 days (Pattern-B session)
**Acceptance:** All 4 math-anchored cleanliness gates pass empirically post-cleaning; schema migration applied + verified; 7-step priority order executed in sequence; per-step acceptance gates pass; MIGRATION.md authored if cross-seam impact discovered; tag shipped; completion record appended

---

## Context

This dispatch is the **load-bearing execution work** of the cleaning-plan campaign. Cycle 9 phases:
- Phase A (legolas) — **COMPLETE** — substrate empirically baselined; 4 deliverables + math note + 38 variant clusters
- Phase B (gandalf) — **COMPLETE** — 7-item policy framework + 26-cluster policy assignments
- **Phase C (Matt) — COMPLETE** — F1-F6 + G1-G5 locked
- **Phase D (THIS DISPATCH; elrond)** — fires now
- Phase E (rocket/legolas Pattern-6 axis discovery) — waits for clean substrate from your Phase D output

You execute the cleaning pipeline that transforms the 89,839-row substrate into a clean canonical-merged dataset ready for Pattern-6 axis discovery. The substrate is empirically dirtier than gandalf's pre-audit projections (FP rate 2.83% vs 0.7% projected; ammo_or_consumable boundary error 17.5% vs 5-8% projected) but field coverage is already met (88.7%/80.7%/69.2%/99.6%). **Phase D is dedup + classification + normalization work, NOT field enrichment.**

## Required reading before starting

1. **`canonical/story/cleaning-policy-design-2026-05-22.md`** — gandalf's full 828-line Phase B policy framework; read in full
2. **`canonical/story/variant-cluster-policy-assignments-2026-05-23.md`** — gandalf's 26-cluster (38 variant decisions) policy assignments; informs Phase D execution per-cluster
3. **`agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-math-note.md`** — sampling strategy + per-source classification baselines
4. **`agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/per-source-quality.md`** — per-source FP rates + classification distributions
5. **`agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/variant-clusters.md`** — 38 variant clusters with mechanical-signature analysis
6. **`agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/named-unique-verification.md`** — 16 confirmed + 10 proposed allowlist additions
7. **`agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/cleanliness-baseline.md`** — empirical baselines vs gandalf projections for the 4 cleanliness gates
8. `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0 — current schema
9. `agentic_orchestration/dispatches/2026-05-22-legolas-phase-A-substrate-audit.md` — Phase A dispatch (your upstream)
10. `agentic_orchestration/dispatches/2026-05-22-gandalf-cleaning-policy-design-review.md` — Phase B dispatch (gandalf's upstream)
11. `agentic_orchestration/weapon-library-import-hive-mind-state.md` — Cycle 9.3 live state

## Math-before-code

Yes. Per Discipline #1, required deliverables BEFORE pipeline code fires:

### Math note — Phase D execution plan

Author at `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-math-note.md`. Required content:

1. **Schema migration plan.** Exact ALTER TABLE statements for all 9 new columns + 1 view. Idempotency strategy (CREATE COLUMN IF NOT EXISTS pattern OR via temp-table + INSERT-SELECT).
2. **Per-step row-impact estimates.** For each of the 7 cleaning steps below, estimate (a) rows touched, (b) rows mutated (classification update), (c) rows merged-into-canonical, (d) expected post-step counts. Validate against legolas's empirical baselines.
3. **Acceptance gate verification queries.** Pre-author the SQL/Python checks that verify each math-anchored cleanliness bar passes post-cleaning. Each check returns a number; the bar passes if number ≤ threshold.
4. **Idempotency guarantees per step.** Each step must be re-runnable without corrupting state. Audit-preservation pattern (mirror Discipline #11): rename source_library / mark dedup_status / populate merged_entry_ids — never DELETE unless explicitly authorized.
5. **Rollback plan per step.** Each step should be reversible (or its modifications well-isolated for a re-run). Backup strategy before destructive operations.

The math note is jack-ryan Gate-1 reviewable at your discretion. Knight-rider recommends it.

## Cross-seam contract change? (Principle 6 gate)

**YES — schema migration touches `weapon_knowledge_entries` table structure.** Per ADR-004:
- The DB lives at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (loadout repo's data dir; gitignored)
- The substrate tables (`weapon_knowledge_entries`, `weapons`, etc.) are cross-cutting data — owned by elrond per AGENTS.md but consumed by drax (loadout) and rocket (engine).
- **Required: MIGRATION.md** at `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/MIGRATION.md` documenting:
  - Schema delta (9 new columns + 1 view; all on `weapon_knowledge_entries`)
  - Forward-compat: new columns are nullable / have defaults; existing readers continue working
  - Backward-compat: no columns dropped, no enums tightened, no row counts shrunk (except via documented quarantines)
  - Per-consumer impact: drax (loadout) — does loadout currently query `weapon_knowledge_entries`? If yes, document. If no, declare so.
  - Per-consumer impact: rocket (engine) — does engine currently query `weapon_knowledge_entries`? Same question.

**Round-trip smoke:** Required. Production-path fixture: a sample of 5-10 rows from each of the 24 active source libraries; pass through your cleaning pipeline; verify all 9 new columns populated; verify `v_category_sample` returns expected row counts; verify per-source consumer paths (if any exist).

If your investigation shows no current cross-seam consumers, state `MIGRATION.md: not applicable — no current consumers; schema delta is additive` and proceed. But you must verify the no-consumer claim, not assume it.

## Locked decisions (F1-F6 + G1-G5; all Matt-approved)

| ID | Decision | Operational |
|---|---|---|
| F1 | Royal Armouries TIERED collapse | Per gandalf RA-1/RA-3/RA-4/RA-5 cluster policies; ≥3 specimens with matching (culture × century × broad_type) triggers collapse (G4) |
| F2 | Cultural-lineage weighted inverse-frequency | For Phase E axis discovery; NOT stratified sampling; Phase D produces the normalized canonical taxonomy that Phase E weights from |
| F3 | pf2ools quarantine | 688 rows = 100% non-weapons (Pathfinder 2e character backgrounds); mirror wikipedia-unfiltered pattern (rename source_library + dump-then-delete with archive) |
| F3-extension | souls-api quarantine | 56 of 58 rows = 96.6% non-weapons (Dark Souls game items: keys, embers, consumables); same pattern as pf2ools |
| F4 | Fuzzy cross-source name-match for canonical merge | ≥0.85 cosine + cross-source corroboration required; Matra Durandal vs Durandal sword case-validated |
| F5 | Pattern-6 methodology | PCA-as-starting-method; Phase D produces substrate suitable for PCA; non-linear methods (autoencoder/UMAP) are Phase E pilot question |
| F6 | Sample-pool size N | N=20-50 default for category sampling; Phase D's `v_category_sample` view enforces |
| G1 | WIKI-3 Gladius game-tier | Keep per-game (slight gandalf lean); per-game named_template canonical |
| G2 | SOULS-1 Dagger across soulslikes | Manual review per-cluster (F4 cosine borderline 0.80-0.85; auto-merge risks flattening per-game lore) — flag clusters for Matt review during pipeline execution |
| G3 | AOS-2 Skull Bludgeon + Varanspire Gladius compound | Split into two children + retain compound (gandalf lean) |
| G4 | RA-2 grouping threshold | ≥3 specimens with matching (culture × century × broad_type) triggers collapse |
| G5 | WIKI-2 OSRS Excalibur | Keep separate as named_template (gandalf lean); game-canon distinct from mythological-unique Excalibur |

## Scope — Schema migration (9 new columns + 1 view)

```sql
ALTER TABLE weapon_knowledge_entries ADD COLUMN wieldable_humanoid TEXT
  DEFAULT 'unknown' CHECK (wieldable_humanoid IN
  ('one_hand','two_hand','shoulder_supported','either','no','mount_required','unknown'));

ALTER TABLE weapon_knowledge_entries ADD COLUMN weapon_kind TEXT
  DEFAULT 'unknown' CHECK (weapon_kind IN
  ('category','unique','named_template','ammo_or_consumable','unknown'));

ALTER TABLE weapon_knowledge_entries ADD COLUMN dedup_status TEXT
  DEFAULT 'unprocessed' CHECK (dedup_status IN
  ('canonical','merged_into','unprocessed'));

ALTER TABLE weapon_knowledge_entries ADD COLUMN variant_relationship TEXT
  DEFAULT 'independent';
  -- enum values: 'independent', 'sub_variant_of:<parent_id>',
  --              'model_line_sibling_of:<related_ids>'
  -- per gandalf cleaning-policy-design § 6.6

ALTER TABLE weapon_knowledge_entries ADD COLUMN cultural_lineage_canonical TEXT
  DEFAULT 'unknown' CHECK (cultural_lineage_canonical IN
  ('european','east_asian','south_asian','southeast_asian','middle_eastern',
   'african','north_american_indigenous','mesoamerican','south_american_indigenous',
   'arctic_circumpolar','oceanic','fantasy_generic','sci_fi_generic',
   'cross_cultural','unknown'));

ALTER TABLE weapon_knowledge_entries ADD COLUMN historical_period_canonical TEXT
  DEFAULT 'unknown' CHECK (historical_period_canonical IN
  ('pre_classical','classical','medieval','early_modern','industrial',
   'modern','contemporary','fictional','unknown'));

ALTER TABLE weapon_knowledge_entries ADD COLUMN register_canonical TEXT
  DEFAULT 'unknown' CHECK (register_canonical IN
  ('historical','military_modern','fantasy','sci_fi','mythological','unknown'));

ALTER TABLE weapon_knowledge_entries ADD COLUMN cultural_lineage_confidence REAL
  DEFAULT 0.0 CHECK (cultural_lineage_confidence >= 0.0 AND cultural_lineage_confidence <= 1.0);

ALTER TABLE weapon_knowledge_entries ADD COLUMN template_quality_score REAL
  DEFAULT 0.0 CHECK (template_quality_score >= 0.0 AND template_quality_score <= 1.0);
  -- per gandalf § 4.8 — for named_template sampling-priority signal

CREATE VIEW v_category_sample AS
SELECT * FROM weapon_knowledge_entries
WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either')
  AND weapon_kind IN ('category','named_template')
  AND dedup_status IN ('canonical','unprocessed')
  AND source_library NOT IN ('wikipedia-unfiltered','pf2ools-pf2ools-data-quarantined','souls-api-thomaslincoln-quarantined');

CREATE VIEW v_category_sample_humanoid_strict AS
SELECT * FROM v_category_sample
WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported');

CREATE VIEW v_category_sample_humanoid_permissive AS
SELECT * FROM v_category_sample
WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either','mount_required');
```

(The two additional permissive/strict views are per gandalf § 2.7.)

## Scope — 7-step cleaning pipeline (execute in this order)

### Step 1 — `ammo_or_consumable` tagging (HIGHEST EMPIRICAL PRIORITY)

**Why first:** Legolas empirical = 17.5% boundary error vs gandalf's 5-8% projection. This drains ~10K+ rows from active substrate BEFORE merge work runs, preventing wasted dedup compute on rows that should be excluded anyway.

**Per-source action:**
- **Royal Armouries (`royal_armouries`):** Apply gandalf § 1.5 detection rule (a) — match canonical_name regex `/cartridge|round|shell|bullet|ammo|scabbard|tsuba|kozuka|grip|guard|hilt|sheath|handle|stand/i` + classification field check. Expected ~10,951 rows tagged. Specific clusters: RA-5 (cartridges, 2,171 rows; B-COLLAPSE policy from gandalf).
- **Met Museum (`met-museum`):** Apply gandalf § 1.5 detection rule (c) — structured_properties.classification contains "Helmet Part"/"Sword Part"/"Armor Part"/"Hilt". Expected ~1,778 rows tagged. Specific clusters: MET-3 (tsuba/kozuka/fuchi/menuki, 1,632 rows; B-COLLAPSE policy).
- **Cataclysm-DDA (`cataclysm-dda`):** Apply gandalf § 1.5 detection rule (a) — source file path matches `ammo.json` OR `tool.json`. Pre-existing structured signal; expected ~50-200 rows tagged.
- **Other sources:** Apply gandalf § 1.5 detection rule (b) — canonical_name regex match. Sweep all 24 source libraries.

**Acceptance:** `ammo_or_consumable` boundary error ≤ 1.0% post-tagging (per gandalf § 4.5). Verify via: count `weapon_kind='category'` rows where canonical_name matches ammo regex; result should be ≤ 1% of category-tagged rows.

### Step 2 — F1 Royal Armouries TIERED collapse

**Why second:** Royal Armouries is 42% of substrate by volume; the largest single dedup opportunity. Step 1 already excluded RA-5 cartridges; this step collapses the remaining ~28K active RA rows.

**Per-cluster execution (from gandalf's variant-cluster-policy doc):**
- **RA-1 (Centrefire revolver, 379 specimens):** Policy B COLLAPSE — single canonical "Centrefire six-shot revolver (Royal Armouries class)" with specimen_count=379 and merged_entry_ids preserving all source rows.
- **RA-2 (generic "Sword", 3,155 rows):** Policy C TIERED — group by (culture × century × broad_type); collapse groups with ≥3 matching specimens per G4 threshold; preserve singleton/dyad-specimens as variants.
- **RA-3 (Flintlock musket, 486 rows):** Policy D FUZZY-COLLAPSE — single canonical with Brown Bess/Charleville sub-retrievable.
- **RA-4 (Pike/Spontoon/Halberd/Partizan, ~1,687 rows):** Hybrid A-at-top + B-within — 4 distinct geometries (KEEP-ALL at top); specimens within each type collapse per G4 threshold.
- **Other RA rows (~24K):** Apply G4 threshold sweep across all RA name-clusters; collapse groups meeting (≥3 specimens AND matching culture × century × broad_type).

**Acceptance:** RA collapse ratio M/N ≈ 9.2% (per legolas estimate; 38,127 raw rows → ~3,500 canonicals); confidence ±30% acceptable. Verify via post-step count of `royal_armouries` rows with `dedup_status='canonical'`; should be 2,500-5,000.

### Step 3 — F3 quarantine (pf2ools + souls-api)

**Why third:** Two whole-source quarantines remove ~750 rows from active substrate before downstream classification work. Mirrors the wikipedia-unfiltered pattern proven at 130K scale.

**Action:**
- **pf2ools (`pf2ools-pf2ools-data`, 688 rows):** Rename `source_library` to `pf2ools-pf2ools-data-quarantined`. Dump-then-archive at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/quarantine-archives/pf2ools-quarantine-2026-05-23.jsonl.gz`. Mirror the wikipedia-unfiltered archive pattern (entries + linked images; README explaining quarantine rationale; reference legolas's Phase A audit confirming 100% non-weapon).
- **souls-api (`souls-api-thomaslincoln`, 58 rows):** Same pattern. Archive at `…/quarantine-archives/souls-api-thomaslincoln-quarantine-2026-05-23.jsonl.gz`. Reference legolas's audit confirming 96.6% FP. Optional: preserve the 2 confirmed-weapon rows (the 3.4% true-positive) with `dedup_status='canonical'` and `weapon_kind='category'` — only quarantine the 56 non-weapon rows. Your judgment.

**Acceptance:** post-quarantine active substrate count = current_active - (688 + 56 or 58) = 89,839 - 746 or 89,839 - 744 = ~89,093-89,095 active rows.

### Step 4 — `named_template` routing for TRPG/MMO/ARPG sources

**Per gandalf § 1.5 detection rule for named_template:** source-library in {nick-aschenbach-dnd-data, 5e-bits*, pf2ools* (now quarantined), bsdata-warhammer-aos, fextralife*, bloqhead-demigods, elden-ring-erdb, souls-api-thomaslincoln (mostly quarantined), diablo2-d2data, path-of-exile-repoe, osrsbox-db (excl. canonical-named-historical), wow-classic-items} AND name not in named-unique allowlist AND name contains narrative-flavor adjectives OR compound-noun-with-flavor-prefix pattern OR D&D rarity in {Uncommon, Rare, Very Rare, Legendary}.

**Per-cluster operational hints from gandalf:**
- **G1 (WIKI-3 Gladius game-tier):** Keep per-game named_template canonical (Matt-locked). Each of D2/PoE/WoW Gladius stays separate.
- **G5 (WIKI-2 OSRS Excalibur):** Keep separate as named_template (Matt-locked). Do NOT merge into mythological-unique Excalibur canonical.
- **G3 (AOS-2 Skull Bludgeon + Varanspire Gladius compound):** Split into two children (each their own named_template canonical) + retain compound as a third entry with `variant_relationship='model_line_sibling_of:<child_ids>'`.

**Acceptance:** `named_template` boundary error ≤ 5.0% (per gandalf § 4.5). Verify post-routing: TRPG/MMO/ARPG rows with `weapon_kind='category'` that match named_template detection criteria should be ≤ 5% of TRPG/MMO/ARPG total.

### Step 5 — FP removal (scattered + brand-prefix disambiguation)

**Scattered FPs:**
- **gta-v-data:** ~25% FP rate in legolas audit (Invalid-name placeholders). Apply name-regex `/^(Invalid|placeholder|test|dummy)/i` → quarantine or `weapon_kind='unknown'` then audit-review.
- **fextralife-*:** ~10-15% FP (category-index pages mistakenly ingested). Detect via short canonical_name + no description_text + URL pattern signaling category-index rather than weapon-detail page. Quarantine flagged subset.
- **wikidata:** ~2% FP loose Q-items (flags, maps, non-weapon objects mis-tagged as Q728 subclass). Use Q-item P31 chain verification; if Q-item is NOT in canonical weapon-class subclass tree, flag for `weapon_kind='unknown'` with FP-suspected note.
- **wikipedia v2:** ~1.2% FP (redirect pages + disambiguation articles). Detect via single-line description + URL-pattern `/redirect|disambiguation/` → quarantine.

**Brand-prefix disambiguation (legolas-flagged refinement):**
- **M982 Excalibur (artillery shell)** vs **Excalibur (Arthurian sword)** — same canonical_name "Excalibur"; description divergence is the signal. Apply F4 ≥0.85 cosine + corroboration test → these correctly do NOT merge.
- **Kimber Aegis (modern pistol)** vs **Aegis (mythological shield)** — same canonical_name; description divergence; F4 disambiguation correctly applied.
- **Tyrfing (anti-radar missile)** vs **Tyrfing (legendary Norse sword)** — same canonical_name; F4 correctly disambiguates.
- General rule: when applying named-unique allowlist, FIRST check description-cosine against allowlist-canonical descriptions; if cosine < 0.50, the name is a brand-prefix coincidence and should NOT be tagged unique.

**Acceptance:** Overall FP rate ≤ 1.5% target / ≤ 3.0% hard (per gandalf § 4.2). Verify via post-step audit-sample (re-fire legolas's Phase A audit methodology against a fresh N=50 per source sample; compute new FP rate; should be ≤ 1.5% target).

### Step 6 — `unique` detection + named-unique allowlist application

**Per gandalf § 3.3 + legolas's 10 proposed additions:**

**Confirmed allowlist (16 of original 24 + 10 additions = ~26 entries to scan for):**
- Confirmed in substrate: Joyeuse, Curtana, Excalibur, Mjolnir, Gungnir, Gáe Bulg, Aegis, Tizona, Colada, Szczerbiec, Honjō Masamune, Mikazuki Munechika, Kusanagi, Reichsschwert, Sword of Goujian, Battersea Shield
- Legolas's 10 additions: Tyrfing, Fragarach, Caladbolg, Gram, Ruyi Jingu Bang, Sudarshana Chakra, Gandiva, Skofnung, Shield of Achilles, Witham Shield
- Borderline / not-found / requires-disposition: Ulfberht swords (article = class; specimens = unique), Narsil (wikipedia redirect — remove), Stormbringer, Andúril, Witch-King's Morgul Blade, The One Ring, Kris Mpu Gandring, Seven-Branched Sword (Chiljido)

**Detection pipeline:**
1. Apply gandalf § 3.5 regex patterns to all rows with `weapon_kind='unknown'` OR `weapon_kind='category'` (museum + wikidata sources prioritized per § 3.4)
2. For matches: apply brand-prefix disambiguation (Step 5 rule)
3. For confirmed matches: set `weapon_kind='unique'`
4. For ambiguous matches (Signal A alone without B or C): flag for manual review; report cluster in your completion record

**Acceptance:** `category-vs-unique` boundary error ≤ 2.0% (per gandalf § 4.5). Verify via post-step audit-sample of `weapon_kind='category'` rows for known-named-unique slip-throughs.

### Step 7 — F4 cross-source canonical merge

**Last step because:** Cross-source merge requires the canonical taxonomy + cleaned classifications + populated allowlist from Steps 1-6 to operate correctly. Running it earlier risks merging dirty-state rows that should have been quarantined or re-classified first.

**Algorithm:**
1. **Block by `weapon_subclass` + `cultural_lineage_canonical`** to reduce comparison space from 89K² to per-bucket-N²
2. **Within each block, compute:**
   - Levenshtein-normalized canonical_name similarity
   - Cosine similarity on description-text embeddings (sentence-transformer, 384-dim)
3. **Merge condition:** name similarity ≥ 0.90 OR (name similarity ≥ 0.75 AND description cosine ≥ 0.85) — AND cross-source corroboration (must appear in ≥2 source libraries OR have explicit Wikidata QID cross-reference)
4. **Apply gandalf's three-lane router for CS-1 (Katana) + CS-2 (Dagger):**
   - **Historical lane:** museum + wikidata + wikipedia entries with historical_period_canonical ≠ 'fictional' → cross-source fuzzy-merge to single canonical historical entity
   - **Game-category lane:** game-source entries with game-specific lore → KEEP-ALL per Policy A (G1 + G5 leans confirm)
   - **Named_template lane:** D&D / TRPG entries → per-source-canonical retained; no cross-source merge unless name + description both align ≥0.95
5. **Apply gandalf's caliber-bucket logic for WIKI-4 AK family** (and generalize the pattern to FN FAL, G3, M-16/AR-15 families if surfaced):
   - Group by caliber metadata; collapse same-caliber-same-mechanical-pattern; KEEP-ALL across calibers
6. **For G2 (SOULS-1 Dagger across soulslikes):** Flag the borderline 0.80-0.85 cosine cases for manual review BEFORE auto-merging. Author a `phase-D-flagged-clusters.md` document; surface to knight-rider for Matt+gandalf in-flight call.

**Acceptance:** Within-canonical-merge duplication ≤ 4.0% residual / dedup recall ≥ 92% (per gandalf § 4.3). Verify via:
- Count distinct canonical_names post-merge (rows where dedup_status='canonical')
- Compute residual duplication: (rows-with-canonical-status / distinct-canonical-names) - 1; should be ≤ 0.04
- Cross-reference legolas's 47% raw duplication baseline; post-merge should be ≤ (47% × 0.08) = ≤ 3.76% residual

## Acceptance gates (overall Phase D acceptance — all must pass)

Per gandalf § 4 math-anchored cleanliness bars; verified empirically via Step-by-step verification queries pre-authored in your math note:

| Gate | Threshold | Verification |
|---|---|---|
| (a) FP rate in active substrate | ≤ 3.0% hard / ≤ 1.5% target | Re-fire legolas's Phase A audit methodology (N=50 per source sample); compute new FP rate; report against thresholds |
| (b) Within-canonical-merge duplication | ≤ 4.0% residual / ≥ 92% dedup recall | Post-Step-7 count of canonical rows vs distinct canonical_names |
| (c) Field-coverage floors | Already met; verify NO DEGRADATION post-cleaning | structured ≥95% / description ≥85% / cultural ≥70% / period ≥60% — all on `v_category_sample` view |
| (d) `weapon_kind` mis-classification | per-dim per gandalf § 4.5 (category↔unique ≤2%; category↔named_template ≤5%; category↔ammo ≤1%) | Re-sample audit on `v_category_sample` for each per-dim boundary |

If any gate fails post-pipeline-execution, the failed step is re-runnable per Discipline #19 (idempotency). Do NOT proceed to Phase E (Pattern-6 axis discovery) until all 4 gates pass.

## Deliverables (in order of execution)

1. **Math note** at `elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-math-note.md` — BEFORE pipeline code fires
2. **MIGRATION.md** at `elrond/research/phase-D-cleaning-pipeline-2026-05-23/MIGRATION.md` — declares cross-seam impact (or not-applicable + verification)
3. **Schema migration applied + verified** — all 9 ALTER TABLE statements + 3 views; idempotent; rollback-able
4. **Step 1 — ammo_or_consumable tagging** + acceptance gate verified
5. **Step 2 — F1 Royal Armouries TIERED collapse** + acceptance gate verified
6. **Step 3 — F3 pf2ools + souls-api quarantine + archives** + acceptance gate verified
7. **Step 4 — named_template routing** + acceptance gate verified
8. **Step 5 — FP removal + brand-prefix disambiguation** + acceptance gate verified
9. **Step 6 — unique detection + allowlist application** + acceptance gate verified
10. **Step 7 — F4 cross-source canonical merge + three-lane router + caliber-bucket** + acceptance gate verified
11. **`phase-D-flagged-clusters.md`** — surface G2 (SOULS-1 Dagger borderline) + any other Matt-needs-review items
12. **Phase D completion summary** at `elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-completion-summary.md` — empirical baselines post-cleaning vs Phase A baselines + gandalf projections; per-gate pass/fail; row-count deltas per step

## Acceptance criteria (commit + tag)

- [ ] Math note authored BEFORE pipeline code fires
- [ ] MIGRATION.md authored (or declared not-applicable with verification)
- [ ] Schema migration applied + smoke-tested (10-row sample passes through pipeline cleanly)
- [ ] All 7 cleaning steps executed in order; each with independent commit + per-step gate verification
- [ ] All 4 overall acceptance gates pass empirically
- [ ] `phase-D-flagged-clusters.md` authored (or stated empty if no flag-needed clusters)
- [ ] Phase D completion summary authored
- [ ] Round-trip smoke: 10-row fixture per source library passes through pipeline; all 9 new columns populated; `v_category_sample` returns expected counts
- [ ] Tag: `elrond/phase-D-cleaning-pipeline-2026-05-23`
- [ ] Append completion record to this dispatch file per `dispatches/README.md` convention

## Out of scope (explicit non-goals)

- **DO NOT** modify gandalf's `canonical/story/cleaning-policy-design-2026-05-22.md` or `variant-cluster-policy-assignments-2026-05-23.md` — operationalize, don't amend
- **DO NOT** execute Pattern-6 axis discovery (Phase E; later; rocket + legolas + gandalf)
- **DO NOT** drop columns or tables — schema delta is additive only
- **DO NOT** delete rows except via documented quarantine pattern (mirror wikipedia-unfiltered) — audit-preservation always
- **DO NOT** re-fire Phase A audit beyond what's needed for acceptance-gate verification
- **DO NOT** make Matt-decisions on G1-G5 — they are LOCKED; apply them
- **DO NOT** decide on the G2 borderline soulslike-Dagger cases yourself — surface for Matt+gandalf in-flight via `phase-D-flagged-clusters.md`
- **DO NOT** modify the loadout web app code (drax's seam); if any drax-side reader of `weapon_knowledge_entries` exists, raise to knight-rider for MIGRATION.md cross-seam coordination

## Open questions for you to resolve + document in math note

1. **Idempotency strategy.** For each of the 7 steps, define exactly how a re-run behaves. For Step 7 (F4 merge), if rows are already in canonical-merged state, what does re-run do? Document.
2. **VACUUM strategy.** After quarantine + delete + classification updates, when do you VACUUM? Mid-pipeline or end-only? Document the disk-reclamation plan.
3. **Backup strategy.** Before each destructive step (quarantine delete; canonical-merge), what's the rollback path? Document.
4. **Step-3 souls-api preservation choice.** Do you preserve the 2 confirmed-weapon rows out of 58 (the 3.4% true-positive)? Or quarantine all 58 and accept the small TP loss? Document your judgment + rationale.
5. **Cosine threshold for description embeddings.** Step 7 uses ≥0.85 cosine; this is gandalf-locked. But the EMBEDDING model choice (sentence-transformer variant) is yours. Document choice; ensure reproducibility.
6. **Anchor-test execution.** Gandalf § 6.3 criterion 4 says "would the generated player-facing kit be more interesting / coherent" — this is human-judgment. You can't fire this without a sample-generation pipeline. Either (a) skip anchor-test in Phase D and defer to Phase E pilot validation, or (b) flag clusters for Matt+gandalf manual anchor-test review. Pick + document.
7. **Phase D-bis trigger.** Gandalf § 7.5 mentions a "Phase D-bis targeted cleaning pass" if Phase E reveals surprises. Phase D should produce a "Phase D-bis hook" that elrond can re-engage if Phase E finds unexpected axes. Document the hook (likely a re-runnable subset of Step 6-7).

## Cross-references

### Upstream Phase B + C artifacts (load-bearing)
- `canonical/story/cleaning-policy-design-2026-05-22.md` — gandalf Phase B framework
- `canonical/story/variant-cluster-policy-assignments-2026-05-23.md` — gandalf 26-cluster policy assignments

### Upstream Phase A artifacts (empirical baselines)
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-math-note.md`
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/per-source-quality.md`
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/variant-clusters.md`
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/named-unique-verification.md`
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/cleanliness-baseline.md`

### Schema + dispatch chain
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0
- `agentic_orchestration/dispatches/2026-05-22-gandalf-cleaning-policy-design-review.md`
- `agentic_orchestration/dispatches/2026-05-22-legolas-phase-A-substrate-audit.md`

### Disciplines
- #1 math-before-code — math note authored first
- #11 audit-preservation pattern — quarantines rename rather than delete; archive everything
- #19 right tool / smoke-test discipline — idempotent steps; smoke-test at the boundary
- #20 robots.txt / Claude-agent respect — already honored upstream

### Prior tags in cycle
- `knight-rider/cleaning-plan-design-locked-2026-05-22`
- `gandalf/cleaning-policy-design-review-2026-05-22`
- `knight-rider/cycle-9-2-phase-A-dispatch-ready-2026-05-22`
- `legolas/phase-A-substrate-audit-2026-05-22`
- `knight-rider/cycle-9-3-phase-A-audit-complete-2026-05-23`
- `gandalf/variant-cluster-policy-2026-05-23`

---

## Tag at completion

```
elrond/phase-D-cleaning-pipeline-2026-05-23
```

(Seam-prefix per ADR-001; intermediate execution artifact; not Matt-milestone tag. Milestone tag candidate is `v0.2-weapon-library-substrate-cleaned` — requires Matt approval after all 4 acceptance gates pass.)

## What happens after you return

Knight-rider:
1. Reads your Phase D completion summary
2. Surfaces any flagged clusters (phase-D-flagged-clusters.md) to Matt + gandalf for in-flight decision
3. Verifies all 4 acceptance gates passed via independent spot-check (legolas Mode A re-sample if needed)
4. Coordinates with Matt on milestone-tag promotion (`v0.2-weapon-library-substrate-cleaned`)
5. Authors Phase E dispatch chain (gandalf § 7.2 hybrid: legolas Mode A dirty-probe + rocket Pattern-6 canonical run)

Phase E (Pattern-6 canonical axis discovery + clustering + designer labeling) operates on your clean substrate.

---

**Signed:** knight-rider (dispatch authored 2026-05-23 ~00:50 EDT; Phase D execution fires next)