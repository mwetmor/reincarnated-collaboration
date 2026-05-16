# Catalogue Curation Pipeline

**Status:** **Operational design locked v1.0** as of 2026-05-16. Curation script (`research/scripts/curate_catalogue.py`) is **not yet implemented** — implementation deferred until the first Legolas Mode B sample lands; no point building the pipeline before there's data to flow through it.
**Author:** elrond.
**Companion:** `catalogue-schema.md` (DB schema); `catalogue-rubric-schema.md` (six-axis rubric); `curator-tagging-guide.md` (per-axis tagging); `MIGRATION.md` (v1.0 schema migration); `pivot-insurance-ledger.md` (output target of pipeline monitoring step).

---

## 0. What this doc is

The operational contract for moving asset data from Legolas Mode B raw output → catalogue.db curated rows. Defines:

1. Input contract (what Legolas produces; what elrond consumes)
2. Curation steps (deduplication, normalization, validation, axis tagging, license clarity, decomposition signal, quality flag)
3. Rejection criteria and rejection-record discipline
4. Provenance preservation and audit-trail
5. Schema migration policy
6. Pipeline monitoring outputs (including the gandalf-dialogue pivot-insurance ledger)
7. Failure modes and recovery

---

## 1. The pipeline at a glance

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌──────────────────────┐
│  Legolas Mode B output  │ ──▶ │   Curation script       │ ──▶ │   catalogue.db       │
│  JSON Lines per session │     │  (curate_catalogue.py)  │     │   curated rows       │
│  research/catalogue/    │     │  research/scripts/      │     │  research/curated/   │
└─────────────────────────┘     └─────────────────────────┘     └──────────────────────┘
                                          │
                                          ▼
                                ┌─────────────────────────┐
                                │  Pipeline outputs       │
                                │  - manual-review queue  │
                                │  - pivot-insurance      │
                                │    ledger updates       │
                                │  - rejection records    │
                                └─────────────────────────┘
```

---

## 2. Input contract (Legolas Mode B raw output)

Per `~/.claude/agents/legolas.md` § Mode B specification, Legolas produces JSON Lines under `agentic_orchestration/research/catalogue/<source>/<session-id>.jsonl`. Each line is one asset extraction.

**Minimum required fields per asset** (Legolas Mode B spec):

```json
{
  "asset_id": "<source-specific identifier>",
  "source": "<vendor name>",
  "url": "<asset source URL>",
  "name": "<asset display name>",
  "category": "<character | enemy | vfx | environment | ui | audio | tile | icon | portrait | other>",
  "dimensionality": "<2d | 3d>",
  "style_register": "<initial style register read; legolas's best guess>",
  "style_tags": ["<secondary tags>"],
  "decomposition": "<monolithic | decomposed | partial | unknown>",
  "file_format": "<png | png-spritesheet | aseprite | svg | gif | mp4 | ...>",
  "license": "<license value per legolas's read>",
  "cost": <numeric usd or 0>,
  "crawl_date": "<ISO-8601 date>"
}
```

**Additionally accepted fields** (Legolas captures when available; curation script consumes when present):

- `pack_name` — vendor's pack-level grouping (e.g., "Free Pixel Magic Sprite Effects Pack")
- `description` — vendor's asset description
- `preview_url` — URL of a preview image (helps curator visual inspection)
- `vendor_metadata` — full vendor JSON if vendor exposes one; preserved verbatim in `source_metadata_raw`
- `extraction_error` — populated if Legolas failed extraction on this row (the curation script skips these and surfaces them in a separate error log)

**Crawl-session manifest:** Legolas additionally produces a session-summary file at `research/catalogue/<source>/<session-id>.session.json` with crawl metadata (started_at, completed_at, asset_count, mode, legolas_version, source). The curation script writes this to `crawl_sessions` table before inserting any assets.

---

## 3. Curation steps (in order)

For each Legolas raw output file, the curation script applies these steps. **Per dispatch + audit § 6.2: reversible.** Every step preserves the raw Legolas extraction in `source_metadata_raw`; no destructive transform.

### Step 1 — Session registration

Write or update the `crawl_sessions` row for this session. If the session is already curated (`crawl_sessions.curated_at IS NOT NULL`), abort and surface — re-curation requires explicit elrond authorization (avoids duplicate inserts).

### Step 2 — Source registration

If `catalogue_sources` doesn't have a row for this source, insert one with `display_name`, `url`, `vendor_type` filled from elrond's standing vendor-registry knowledge or surfaced for manual entry. Vendor entries are append-only at the source level; new vendors trigger a one-line elrond-authored note in `pipeline-runs.md`.

### Step 3 — Deduplication

For each raw asset, check `(source, source_asset_id)` against existing rows in `catalogue_assets`. Three cases:

- **Net-new asset** (no prior row): proceed to step 4.
- **Re-crawl with identical content** (raw `source_metadata_raw` is byte-identical, or differs only in `crawl_date`): SKIP. Asset is already curated; no work needed. Log to session report.
- **Re-crawl with content drift** (raw extraction differs): create a NEW row, link the prior row via `superseded_at` + `superseded_by_uid` audit-trail. This is append-only re-curation; the prior row is retained for historical integrity.

### Step 4 — Field normalization

Map Legolas fields to catalogue schema columns:

- `asset_id` → `source_asset_id` (preserved verbatim)
- `source` → `source` (validated against `catalogue_sources.source`; rejected if unknown vendor unless source-registration ran in step 2)
- `url` → `source_url`
- `crawl_date` → `source_date`
- `category` → `category` (validated against enum; mapped if Legolas used an alias)
- `dimensionality` → `dimensionality`
- `decomposition` → `decomposition` (validated; `null` from Legolas maps to `unknown`)
- `file_format` → `file_format` (lower-cased; common aliases normalized — e.g., `'PNG'` → `'png'`, `'sprite-sheet'` → `'png-spritesheet'`)
- `license` → `license` (validated against enum; `itch-standard` from older Legolas data is rejected — curator must re-read source; per gandalf dialogue Topic 5)
- `cost` → `cost_usd` (numeric coercion; non-zero non-`null` Legolas cost data populates this; `cost_model` derived from `license` heuristically)
- Entire raw record → `source_metadata_raw` (JSON-stringified; preserved verbatim)

### Step 5 — Axis tagging (the heart of curation)

For each of the five mechanical axes (resolution_band, palette_size, shading_technique, linework_style, animation_frame_density):

1. Check if Legolas captured the value (Legolas may have partial axis-inference from vendor metadata).
2. If unset or `unknown` AND `preview_url` is available, surface to manual-review queue with the preview URL for curator visual inspection. **Curator-fillable** in manual-review pass.
3. If unset AND no preview available, set the value to `unknown` — the asset is queued for source-page-re-inspection on the next curation pass.

Once all five axes have non-`unknown` values:

4. Apply the deterministic rule from `catalogue-rubric-schema.md` § 3 to compute `derived_register`.
5. Record `derived_register_source = 'rule'` and the rule that fired (e.g., `'R6'`) in a debug-comment field embedded in `source_metadata_raw` for diagnostic queryability.

### Step 6 — R6 / R7 side effects

Per `catalogue-rubric-schema.md` § 3.1:

- **R6 trigger** (`hand-drawn-pixel` + `hard-1px-outline`): pipeline inserts `asset_style_tags` row `(asset_uid, 'outline-profile:hard-1px', confidence=1.0, source='elrond-curated')`.
- **Non-R6 hand-drawn-pixel** (linework ∈ `soft-outline / variable-width / no-outline`): pipeline inserts `(asset_uid, 'outline-profile:soft-or-variable', ...)`.
- **R7 trigger** (Foozle boundary cluster): pipeline sets `quality_flag = 'borderline'` and appends to `quality_rationale`: `"R7 boundary-cluster admit; curator confirm after eyeball"`.

### Step 7 — Embodiment tagging

For `category IN ('character', 'enemy')` only:

1. Check `style_tags` for embodiment hints (`'humanoid'`, `'slime'`, `'beast'`, etc.).
2. If a starter-set embodiment is identified, set `embodiment_tag` accordingly.
3. If a non-starter embodiment is identified (`'undead'`, `'mecha'`, etc.), set `embodiment_tag = 'pending-amendment'`, populate `pending_amendment_hint` with the legolas-tagged or curator-inferred form description.
4. If no embodiment hint and no preview to inspect, set `embodiment_tag = 'unknown'`. Queue for manual review.

For `category NOT IN ('character', 'enemy')`: `embodiment_tag = 'not-applicable'`.

### Step 8 — License clarity pass

Per `catalogue-schema.md` § 4 default `quality_flag` by license:

- `commercial-license`, `commercial-royalty-bearing`, `proprietary`, `unknown` → `quality_flag = 'borderline'` (auto-set unless already borderline from R7); concatenate license-clarity to `quality_rationale`.
- Other licenses → `quality_flag` default `'unreviewed'`; gets `'pass'` after curator-pass.

`license_url` required for `commercial-license` and `proprietary` — pipeline rejects asset if `license_url` is missing for those values. Surfaced for manual fix.

### Step 9 — Quality flag review

Final `quality_flag` after all auto-flags:

- `unreviewed` — default; needs curator-pass before consumption-time use
- `pass` — curator-confirmed (only set by explicit curator action, not auto)
- `borderline` — auto-set from R7, license, or quality-rationale; needs explicit curator review to move to `pass` or `fail`
- `fail` — curator-set; asset is in catalogue for record but excluded from consumption-time filters
- `deferred` — curator-set; review revisited later (e.g., source page unreachable)

### Step 10 — Audit-trail population

For every inserted row:
- `curated_at` = pipeline run timestamp
- `curated_by` = `'elrond+curate_catalogue.py'`
- `superseded_at` = NULL (new current row)
- `superseded_by_uid` = NULL

For superseded rows (re-curation):
- The prior row's `superseded_at` and `superseded_by_uid` are filled.
- The new row points to the prior via... well, by being its successor; the link is the FK in the old row.

### Step 11 — Session completion

After all assets in the Legolas raw output are processed:
- Update `crawl_sessions.curated_at` to the pipeline run timestamp.
- Update `crawl_sessions.asset_count` if Legolas didn't already populate it.

### Step 12 — Pivot-insurance-ledger update

Per gandalf dialogue Topic 6: append a summary row to `pivot-insurance-ledger.md` at every curation pass. The summary records:

- Date + session-id curated
- Total catalogue asset count after this pass
- Per-`derived_register` asset counts
- Per-embodiment coverage in `hand-drawn-pixel` (the locked register)
- Per-embodiment coverage in the next-most-populated register (the pivot candidate)
- Any embodiments where pivot-insurance is near-zero (<5 assets in pivot-candidate register)

The script appends; the ledger is human-readable. Knight-rider / elrond can scan the ledger monthly-ish to surface coverage erosion.

### Step 13 — Rejection recording

If a Legolas raw entry can't be curated (e.g., `extraction_error` set; mandatory field missing; license is uninterpretable):
- Insert a row in `catalogue_rejections` with `failure_track = 'structural'`, the rationale, and `re_sampleable = 1` if Legolas's extraction can be adjusted, `0` if the source itself is unusable.
- Do not insert into `catalogue_assets`.

If a Legolas sample triggers a viability-gate failure post-curation (e.g., >20% unknown-license per gandalf dialogue Topic 5 strengthening):
- The pipeline produces a curation-pass summary flagging the sample as gate-failed.
- Knight-rider receives the summary; sample fails the design-track gate.
- A rejection row records the structural failure if it's the dominant failure mode.

---

## 4. Provenance preservation

- **Source raw extraction:** `source_metadata_raw` JSON column preserves every Legolas field. The curated row is reconstructible from raw via re-running the script.
- **Crawl session:** every curated row links via `crawl_session_id` to the session that produced it. Knowing when the source was crawled is one query away.
- **Pack:** when the asset has a pack, `pack_id` links to `catalogue_packs`.
- **Curation script provenance:** every row has `curated_by` recording the script name (and version, future).
- **Rubric version:** every row records `rubric_version` so mixed-rubric-version states are discoverable when v2.0 lands.
- **Override audit-trail:** override and manual-review-resolved values record `derived_register_source` and `derived_register_override_rationale`.

---

## 5. Rejection criteria (curation-time)

Curation rejects an asset row from insertion if:

1. **Mandatory field missing.** `source`, `source_asset_id`, `source_url`, `name`, `category`, `file_format`, `license`, `decomposition` — all NOT NULL. Any missing → rejection.
2. **Unknown vendor.** Source not in `catalogue_sources` and curation script can't auto-add (e.g., metadata required for `vendor_type` is missing) → rejection.
3. **Invalid enum value.** Any Legolas value not in the schema's CHECK constraint set (after normalization in step 4) → rejection.
4. **`license = 'commercial-license'` or `'proprietary'` without `license_url`** → rejection.
5. **`extraction_error` flagged by Legolas** → rejection (no usable data).

Rejections are recorded; the curation pipeline does not silently drop.

---

## 6. Schema migration policy (recap from `MIGRATION.md`)

- **Additive (v1.x):** new column, new optional table, new value in CHECK enum. Migration script under `research/scripts/catalogue_migrations/v1_x_<topic>.sql`. Existing rows unchanged. MIGRATION.md entry.
- **Breaking (v2.0):** column rename / type change / re-tagging. Senior-design approval (Matt) per ADR-002. Migration script + back-fill script + verification. MIGRATION.md entry. Rollback plan documented.

The curation script's behavior depends on schema version; the script checks `schema_meta` on startup and refuses to operate against a schema version it doesn't recognize.

---

## 7. Pipeline monitoring outputs

Three files updated at each curation pass:

### 7.1 — `pivot-insurance-ledger.md`

Per gandalf dialogue Topic 6. See § 3 step 12. Tracks per-register / per-embodiment coverage; surfaces silent pivot-insurance erosion.

### 7.2 — `manual-review-queue.md`

Append a section for each curation pass: assets requiring manual review (axis values unknown, embodiment unclear, license borderline, R7 default-borderline, etc.). Elrond drains this at curation passes. Persistent items (>3 passes unresolved) escalate to gandalf or knight-rider.

### 7.3 — `pipeline-runs.md`

A run log of curation invocations. Date, session_id, raw_assets_processed, inserted_count, superseded_count, rejected_count, manual-review-queue additions. Operational log; not analytical.

These three files live in `agentic_orchestration/research/curated/` alongside the schema docs. All three are committed to git (the DB is gitignored; the human-readable monitoring docs are tracked).

---

## 8. Failure modes and recovery

### 8.1 — Legolas crawl fails mid-session

Curation can't proceed for incomplete sessions. The session manifest's `completed_at` is NULL; the curation script refuses to curate. Recovery: Legolas resumes the crawl or marks it failed; if failed, the partial raw output is archived to `research/catalogue/<source>/archive/` and a new session is started.

### 8.2 — Schema version mismatch

Curation script refuses to operate against a `schema_meta.version` it doesn't recognize. Recovery: re-run the appropriate migration, then re-run the script. If schema is ahead of the script, update the script.

### 8.3 — Mass rejection (>20% of a sample)

The curation pass summary flags a high-rejection-rate sample. Knight-rider receives the summary; this is a gate-failure-equivalent. Possible causes: Legolas extraction logic broke, source page format changed, mass license-unknown. Investigation routes to legolas (re-extract) or elrond (rubric refinement).

### 8.4 — Curator-override pattern surface

The script tracks override counts per curator per rule clause. When threshold (10% corpus or 5-instances-per-clause) is exceeded, the run summary surfaces it as a rule-bug. Per gandalf dialogue Topic 3. Elrond reviews; refines rule or accepts the override pattern as design-correct.

### 8.5 — DB lock during long curation

WAL journal mode handles concurrent reads. If a long curation pass holds the writer lock and analytical scripts contend, recovery is just to wait — WAL is non-blocking on reads. If a curation pass crashes mid-way, WAL replays cleanly on next open.

---

## 9. Cross-references

- `catalogue-schema.md` — DB tables this pipeline writes
- `catalogue-rubric-schema.md` — six-axis rubric the pipeline applies
- `curator-tagging-guide.md` — per-axis manual tagging that supplements automated curation
- `MIGRATION.md` — schema migration history
- `pivot-insurance-ledger.md` — monitoring output (gandalf dialogue Topic 6)
- `~/.claude/agents/legolas.md` § Mode B — upstream extraction contract
- AGENTS.md § "Viability-gate workflow" — the design-track / structural-track / wiring-track gates the pipeline feeds

---

## 10. Implementation note — script not yet written

`research/scripts/curate_catalogue.py` is **not implemented in this dispatch.** Per the dispatch context ("Catalogue work is multi-week+; no operational blocker"), implementation is deferred until the first Legolas Mode B sample lands. The catalogue.db file is empty; this pipeline contract documents the intended flow.

Rationale for deferral: there's no point building a curation pipeline before there's data flowing through it. The data drives the pipeline's edge cases. Writing it now would produce a script tested only against synthetic data; writing it after the first Pimen sample gives it a real working corpus.

Knight-rider should sequence implementation alongside (or just after) Legolas Pimen sample dispatch release. Estimated implementation cost: 1-2 days elrond work.

---

— elrond, 2026-05-16
