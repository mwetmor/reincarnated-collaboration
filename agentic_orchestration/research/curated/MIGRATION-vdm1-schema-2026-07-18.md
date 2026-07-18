# MIGRATION — VDM-1 schema landing zone + Stage-0 ingestion fix — 2026-07-18 — **APPLIED**

**Owner:** elrond (single-writer of `corpus.db`)
**Protocol:** ADR-004 cross-seam handoff doc. Parallels star-lord engine-side `MIGRATION.md`.
**Charter (requirements source):** `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md` (§3 four output streams · §5 parsimony ladder · §7 seam routing).
**Script (fail-loud, single transaction, rollback-on-mismatch):** `scripts/corpus_vdm1_schema_2026_07_18.py`
**Backup (taken BEFORE migration):** `corpus.db.pre-vdm1-schema-2026-07-18-backup` (md5 `48a1f90c407826e438aa5f53ef45215f`)
**Discipline #8:** schema landing zone built BEFORE any crawl payload arrives (schema at boundaries).

---

## What changed (one line)

Built the VDM-1 run's **six-table landing zone** (`kit_dossier`, `kit_citations`, `verify_ledger`, `kit_mapping`, `mint_ledger`, `mechanic_gap_docket`) + a **conf-provenance separation column** (`canon_probe_facts.fact_provenance`) + the **Stage-0 `core_skills` ingestion fix** (`canon_corpus.core_skills` from the mobile JSONLs). **Purely additive** — the 65-column `canon_corpus` content-md5 is byte-identical PRE/POST (`ae67fe2e255467d5daf0dc43c2ac1eb2`), every pre-existing table's row count is conserved, and **no rows were invented**: JSONL ids with no DB row would be logged as orphans (there were 0), and the 12 DB rows with no JSONL `core_skills` are logged below for legolas's parallel census reconciliation.

---

## DELIVERABLE 1 — six new tables (DDL summary)

All FK to `canon_corpus(kit_id)`. All carry a `created_date`/`authored_date`/`verified_date` DEFAULT `date('now')`. CHECK enums per charter §3; the **no-fabrication law is DB-enforced** on `kit_dossier`.

| Table | Grain / PK | Key columns | Enums (CHECK) | Notable constraint |
|---|---|---|---|---|
| `kit_dossier` | AUTOINCREMENT id; `UNIQUE(kit_id, family, source_url)` | `payload_json`, `source_url`, `anchor_quote` (verbatim), `abstained`, `conf`, `extraction_provenance` DEFAULT `fetched-vdm1` | `family IN (skill_loop, skill_geometry, item_alterations, capstone_alterations, author_credit, variants)` | **`CHECK(abstained=0 OR payload_json IS NULL)`** — abstain ⇒ empty payload (no-fabrication law); `abstained IN (0,1)` |
| `kit_citations` | AUTOINCREMENT id; `UNIQUE(kit_id, url)` | `url`, `archive_url` (Wayback), `site`, `author_handle`, `title`, `accessed_date`, `quarantined` DEFAULT 0 | `cite_class IN (authored, communal, official, dataset)`; `rank_class IN (recovered, attested-era)` | `quarantined IN (0,1)` — junk-tail domains recorded, never citable |
| `verify_ledger` | AUTOINCREMENT id | `claim_text`, `anchor_quote`, `source_url`, `errata_applied` DEFAULT 0, `run_tag` DEFAULT `vdm1` | `claim_family IN (identity, mechanics, era, negative_canon)`; `verdict IN (CONFIRMED, CONTRADICTED, UNSUPPORTED, SOURCE_NOT_FOUND)` | `errata_applied IN (0,1)`. (anchor-quote-mandatory for CONFIRMED/CONTRADICTED enforced in-app, not DDL — a verdict can legitimately have no quote when SOURCE_NOT_FOUND) |
| `kit_mapping` | **`kit_id` PK** (1 row/kit — the terminal mapping) | `mapping_json` (motion_frame / t4_doors / option_c_substrate_flags / skill+element+scaffold coords), `deviation_notes`, `mapping_provenance` DEFAULT `authored-vdm1` | `grade IN (EXACT, CLOSE, APPROX, GAPPED)`; `terminal_state IN (MAPPED, MAPPED_DOCKET)` | PK enforces R-6 "every kit reaches exactly one terminal state" |
| `mint_ledger` | `mint_id` AUTOINCREMENT | `description`, `forced_by_kits` (JSON array), `ladder_step_audit` (which of the 4 §5 ladder steps tried first) | `mint_class IN (quantitative, qualitative)` | one row per mint (§5 R-7) |
| `mechanic_gap_docket` | `docket_id` AUTOINCREMENT | `mechanism_class`, `spec_text_or_path`, `evidence_kits` (JSON array), `destination` (e.g. `GX-02`), `status` DEFAULT `open` | — | GX-02 shapeshift destination pre-known (3 kits) |

**Adaptations from gandalf's requirement shapes (intent preserved):**
- `kit_dossier`: added surrogate AUTOINCREMENT `id` PK (the requested `UNIQUE(kit_id, family, source_url)` becomes a unique index; a surrogate PK is needed because `source_url` can be NULL when a family is authored from an already-fetched shared page, and SQLite treats multiple NULLs as distinct in UNIQUE). Renamed the row-timestamp to `created_date`. Added the `abstained⇒NULL-payload` CHECK to make the no-fabrication law structural, not conventional.
- `verify_ledger` / `kit_citations`: added surrogate `id` PK + a per-row date column. `kit_citations` `UNIQUE(kit_id, url)` prevents duplicate citation rows per kit.
- All CHECK enums preserved verbatim from the dispatch. All named fields retained with their stated intent.

**Verified live** (rolled-back test transactions, no rows left behind): abstain-with-payload → **rejected**; abstain-with-NULL-payload → accepted; bad `family` → rejected; bad `verdict` → rejected; FK to nonexistent kit → rejected; reserved provenance values `verified-v1.1`/`fetched-vdm1` → accepted.

**Landing-zone state:** all six tables created **empty** (0 rows) — payloads land as legolas returns crawl artifacts and gandalf authors mappings.

---

## DELIVERABLE 2 — conf-provenance separation (`canon_probe_facts.fact_provenance`)

New nullable-then-fully-populated column with `CHECK IN ('kb-legacy','named-source-unfetched','verified-v1.1','fetched-vdm1')`.

**Why `named-source-unfetched` was added to the dispatch's stated 3-value vocabulary:** the dispatch itself specifies the ELSE branch — *"backfill existing rows 'kb-legacy' WHERE their sources_used family indicates kb-only, else 'named-source-unfetched'."* The corpus is a projection of model belief (charter §2: sources_used = 84% kb-memory-only, **zero fetched URLs** — confirmed: 0 of 478 sources_used arrays contain `http`). So at migration time NOTHING is `verified-v1.1` or `fetched-vdm1`; those two values are **reserved** and populated only as VDM-1 crawl verdicts/dossiers land. The legacy population splits into exactly two buckets: memory-only vs named-but-unfetched.

**Backfill rule (exact, reproducible):**
1. For each `kit_id`, read its `sources_used` family (`facts_json` = JSON array of source-class strings).
2. Strip **provenance-artifact bookkeeping tokens** (substring match, case-insensitive: `rdr-kit-atlas`, `rdr-kit`, `csv provenance`, `rdr-roster`) — these are internal atlas-lineage markers, not sources.
3. Of the remaining *substantive* tokens: if **every** token begins with `kb` or `od` (memory projections — `kb`=community knowledge base recalled from memory, `od`=online-docs recalled from memory) → the kit is **`kb-legacy`**. If **any** substantive token names a specific external source (a guide/wiki/dataset abbreviation: `iv`, `db`, `sky`, `gt`, `ph`, `dx`, `sf-hot`, `lb`, `gg`, `maxroll`, etc.) → **`named-source-unfetched`**. If only bookkeeping tokens remain (empty substantive set) → **`kb-legacy`** (no named external source present).
4. **All 10 family rows for a kit inherit the kit's single classification** (including the `sources_used` row itself) — every fact for a kit shares the same evidentiary basis, so the provenance tag is a kit-level property stamped onto each family row.

**Counts (POST):**
- `kb-legacy`: **2640 rows** (264 kits × 10 families)
- `named-source-unfetched`: **2140 rows** (214 kits × 10 families)
- `verified-v1.1`: 0 (reserved) · `fetched-vdm1`: 0 (reserved)
- NULLs: **0** (all 4780 rows classified)

**Relationship to the pre-existing `prov` column:** `prov` (populated only sparsely on probe rows) is untouched and remains the raw per-family provenance string as it appeared in the source object. `fact_provenance` is the new **normalized, run-legible** epistemics tag the charter's §2/§3 conf-provenance wall requires. The 107 kits with zero probe facts are absent from `canon_probe_facts` — nothing to backfill there; they get harvest-grade probe authoring in-run (charter §6), landing as `fetched-vdm1`.

---

## DELIVERABLE 3 — Stage-0 ingestion fix (`canon_corpus.core_skills`)

Two new nullable columns: `core_skills` (JSON array text) + `core_skills_prov` (provenance tag).

**Source:** the 17 per-game / final-docs mobile JSONLs under `claude-mobile-session-docs/ARPG-canonical-kit-research/**/canon-corpus-*.jsonl`. The `core_skills` array (1–3 skill names per kit, e.g. `["Cyclone","Fortify"]`) is present on every record in those files but **never landed in the DB**. The two `rdr-roster-kits.jsonl` files carry no `core_skills` and are correctly skipped by the glob.

**Ingestion (inspected actual values first — no quoting/format quirks found):**
- 17 JSONL files parsed; **573 distinct ids carry `core_skills`** (verified 0 cross-file duplicate ids, so no silent overwrite of differing values).
- Values normalized to a list of non-empty trimmed strings; a scalar string would be wrapped to a 1-element list (none occurred); serialized with `ensure_ascii=False` (preserves any non-ASCII skill names).
- **Applied: 573 rows** stamped `core_skills_prov = 'jsonl-stage0-backfill-2026-07-18'`.
- **JSONL orphans (id in JSONL, no `canon_corpus` row): 0.** Every JSONL id resolves to a DB row. (Nothing invented; had any existed, they would be listed here per the no-invent law.)
- Parse errors: 0.

**Census-drift residue (the OTHER direction — 12 DB rows with NO JSONL `core_skills`):** these are NOT orphans (they have valid DB rows); they simply have no `core_skills` source. Logged here for legolas's parallel census reconciliation, NOT filled:

| kit_id | game | folk_name | negative | source_date | likely cause |
|---|---|---|---|---|---|
| `d3-wizard-black-hole` | d3 | Wizard — Black Hole | 0 | 2026-07-15 | Edition-III pull-tranche row, added to DB after mobile JSONL freeze |
| `d4-spiritborn-vortex` | d4 | Spiritborn — Vortex | 0 | 2026-07-15 | Edition-III pull-tranche row, post-JSONL |
| `di-cyclone-strike-monk-base` | di | DI Monk — Cyclone Strike (base) | 0 | 2026-07-15 | Edition-III pull-tranche row, post-JSONL |
| `d2-sacrifice` | d2 | Sacrifice (Paladin) | 1 | 2026-07-12 | ingest-era; negative twin filled from mint dossier (per A.5 log), not from JSONL |
| `d2-teleport-sorc` | d2 | Teleport Sorceress | 0 | 2026-07-12 | id-slug drift vs JSONL id (census reconcile) |
| `d3-call-of-the-ancients` | d3 | Call of the Ancients Barbarian | 0 | 2026-07-12 | id-slug drift |
| `d3-dashing-strike-monk` | d3 | Dashing Strike Monk | 0 | 2026-07-12 | id-slug drift |
| `le-ring-of-shields` | le | Ring of Shields / Sentinel Guard | 0 | 2026-07-12 | id-slug drift |
| `le-shift-bladedancer` | le | Shift Bladedancer | 0 | 2026-07-12 | id-slug drift |
| `poe1-blood-magic-kit` | poe1 | Blood Magic Life-as-Resource | 0 | 2026-07-12 | id-slug drift (poe1 94-DB / 91-JSONL gap) |
| `poe1-totem-hierophant` | poe1 | Totem Hierophant | 0 | 2026-07-12 | id-slug drift |
| `poe1-vaal-blade-vortex` | poe1 | Vaal Blade Vortex | 0 | 2026-07-12 | id-slug drift |

The `poe1` case corroborates the dispatch's census-drift note (memo said 91 PoE1, DB has 94): 91 JSONL records matched, 3 poe1 DB rows have no JSONL `core_skills` source. VDM-1's crawl will author `core_skills`-equivalent loop data for these 12 into `kit_dossier.skill_loop` (fetched-evidence), which supersedes the missing Stage-0 value.

---

## Integrity asserts (pre/post — all PASSED, else the transaction would have ROLLED BACK)

| Assert | PRE | POST | Result |
|---|---|---|---|
| `canon_corpus` content-md5 (65 original cols, ORDER BY kit_id) | `ae67fe2e255467d5daf0dc43c2ac1eb2` | `ae67fe2e255467d5daf0dc43c2ac1eb2` | **conserved** (proves additivity — no existing value mutated) |
| `canon_corpus` rows | 585 | 585 | conserved |
| `canon_probe_facts` rows | 4780 | 4780 | conserved |
| `canon_engine_key` rows | 585 | 585 | conserved |
| `roster_atlas` / `roster_lineage_enrichment` | 45 / 45 | 45 / 45 | conserved |
| all 9 `atlas_*` tables | (12,12,2,2,8,469,628,86,86) | identical | conserved |
| `corpus_schema_meta` rows | 16 | 17 | **+1** (intended: the VDM-1 meta row) |
| six new tables exist | — | all present | pass |
| `fact_provenance` NULLs | — | 0 / 4780 | pass |
| `PRAGMA integrity_check` | — | `ok` | pass |

**Reversibility:** `corpus.db.pre-vdm1-schema-2026-07-18-backup` is a full file-copy of the pre-migration DB. The migration is additive, so reversal = drop the six tables + drop the two `canon_corpus` columns + drop `canon_probe_facts.fact_provenance` + delete the schema-meta row; or restore the backup wholesale.

**Rebuild chain:** base ingest → s1 → fold12 → cell-key → A.5 → mcd → edition3 A/B → gamecode-normalize → dual-hard-delete → la-mcd-9.19 → s2/econ passes → dr-reclassify → **this (vdm1-schema-2026-07-18)**.

---

## corpus_schema_meta row written

`version = 'vdm1-schema-2026-07-18'`, `applied_at = '2026-07-18T00:00:00Z'`, note summarizing the +6 tables, fact_provenance backfill (2640/2140), core_skills ingest (573 applied / 0 orphans / 12 residue logged), additivity guarantee, and the backup path.

---

**Signed:** elrond (single-writer, corpus.db) — schema at the boundary, built before the payload; every field's intent preserved; nothing invented.
