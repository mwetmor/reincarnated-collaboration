# Catalogue DB — Schema

**Status:** **Locked v1.0 (design)** as of 2026-05-16, post-dialogue with gandalf. **Pending Matt approval** per ADR-002 cross-seam-architecture lock before the schema is applied to the live `catalogue.db` for production use.
**Author:** elrond.
**Companion:** `catalogue-rubric-schema.md` (the six-axis style rubric implemented as columns here); `curator-tagging-guide.md` (per-axis tagging instructions); `curation-pipeline.md` (operational flow from Legolas raw → curated row); `MIGRATION.md` (schema migration log).
**Location:** `agentic_orchestration/research/curated/catalogue.db` (SQLite; gitignored).
**Implements:** the L3 layer of the data architecture per `data-architecture-audit-2026-05-16.md` § 5.

---

## 0. What this doc is

The complete schema of the catalogue database: tables, columns, types, constraints, indexes, normalization, source-anchoring, audit-trail conventions, schema-versioning. The schema accepts Legolas Mode B raw extraction and produces curator-tagged structured rows queryable by drax/star-lord/gandalf at consumption time.

---

## 1. Design principles (recap from audit § 6)

1. **Source-anchored.** Every row traces to its origin via `source`, `source_url`, `source_date`, and the preserved raw extraction in `asset_metadata_raw`.
2. **Reversible.** Curation transformations are reproducible from the raw extraction. No destructive transforms.
3. **Tagged, not encoded.** Style register, embodiment, category — each is a named column or association table, not packed into compound IDs.
4. **Versioned.** Schema versions via `schema_meta`; rubric versions via `rubric_version` column; data-source versions via `crawl_sessions`.
5. **License + cost legible.** No NULLs allowed on `license`; `unknown` is the explicit value for non-determinable cases.
6. **Audit-trail.** Every curated row carries `curated_at` / `curated_by` / `curation_run_id` / `superseded_at`. Curation is append-only with `superseded_at` rather than UPDATE-in-place.

---

## 2. Database file conventions

- **Path:** `agentic_orchestration/research/curated/catalogue.db`
- **Gitignore:** the `.db`, `.db-wal`, `.db-shm` files are gitignored at `agentic_orchestration/research/curated/.gitignore`. The schema docs (this file + companions) are committed.
- **SQLite version:** ≥ 3.38 (for JSON1 extension + STRICT tables).
- **Tables created with `STRICT` keyword** where supported (rejects type-mismatched inserts at SQL layer rather than silently coercing).
- **Foreign keys enforced:** `PRAGMA foreign_keys = ON;` at every connection.
- **Journal mode:** WAL (for non-blocking reads during curation writes).

---

## 3. Tables

### 3.1 — `schema_meta`

Tracks schema migrations applied. Pattern parallels `reincarnated-engine/src/reincarnated/telemetry/migrations.py` `schema_meta` table.

```sql
CREATE TABLE schema_meta (
  version TEXT PRIMARY KEY,            -- '1.0', '1.1', '2.0'
  applied_at TIMESTAMP NOT NULL,
  description TEXT NOT NULL,
  migration_script TEXT                 -- path to migration script under research/scripts/, NULL for initial
) STRICT;
```

**v1.0 initial row:**
```
('1.0', '2026-05-16T??:??:??Z', 'Initial catalogue schema; six-axis style rubric v1.0; embodiment tag aligned to embodiment-narrative-layer.md v1.0', NULL)
```

### 3.2 — `catalogue_sources`

One row per vendor / catalogue source. Captures vendor-level metadata that doesn't vary per-asset. Per-asset rows in `catalogue_assets` reference this via `source` (string foreign key by name for readability — chose name over surrogate ID for query legibility).

```sql
CREATE TABLE catalogue_sources (
  source TEXT PRIMARY KEY,              -- 'pimen', 'pipoya', 'creativekind', 'craftpix', 'opengameart', 'unity-asset-store', etc.
  display_name TEXT NOT NULL,           -- 'pimen', 'Pipoya', 'CreativeKind', 'CraftPix.net', 'OpenGameArt.org'
  url TEXT NOT NULL,                    -- vendor landing page
  vendor_type TEXT NOT NULL CHECK (vendor_type IN (
    'individual-creator', 'studio-creator', 'aggregator-marketplace', 'commons-repository', 'unknown'
  )),
  primary_register_hint TEXT            -- 'hand-drawn-pixel' / 'retro-16bit' / 'mixed' / 'vector' / etc.; advisory only — per-asset axis values are authoritative
    CHECK (primary_register_hint IN ('retro-16bit', 'hand-drawn-pixel', 'clean-vector', 'painterly-raster', 'anime-cel', 'mixed', 'unknown')),
  default_license TEXT                  -- 'CC0', 'commercial-royalty-free', 'mixed' (vendor ships multiple license varieties), etc.; advisory only — per-asset license is authoritative.
                                        -- 'itch-standard' was dropped per gandalf dialogue Topic 5 + drax wiring-track Flag 3 — itch-vendor licenses vary per asset; force curators to read the actual license.
    CHECK (default_license IN ('CC0', 'CC-BY', 'CC-BY-NC', 'CC-BY-SA', 'CC-BY-ND',
                               'commercial-royalty-free', 'commercial-per-project', 'commercial-royalty-bearing',
                               'commercial-license', 'unity-asset-store', 'proprietary', 'mixed', 'unknown')),
  notes TEXT,                            -- curator-authored notes on the vendor (e.g., "ships free AND paid packs; per-pack license varies")
  added_at TIMESTAMP NOT NULL
) STRICT;
```

**Why `primary_register_hint` and `default_license` are hints, not authoritative:** vendors ship cross-register and cross-license content. The per-asset value is authoritative; vendor-level hints support search and curator orientation. This is the per-asset granularity locked in `catalogue-rubric-schema.md` § 8.2.

### 3.3 — `crawl_sessions`

One row per Legolas crawl invocation. Provenance — every `catalogue_assets` row joins back to a crawl_session.

```sql
CREATE TABLE crawl_sessions (
  session_id TEXT PRIMARY KEY,           -- e.g., 'legolas-pimen-mode-b-2026-05-16'
  source TEXT NOT NULL REFERENCES catalogue_sources(source),
  legolas_version TEXT,                  -- if applicable; helps when Legolas's extraction logic changes
  mode TEXT NOT NULL CHECK (mode IN ('mode-b-sample', 'mode-b-full-crawl', 'mode-a-supplement')),
  started_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP,                -- NULL while in progress
  asset_count INTEGER,                   -- populated at completion
  raw_output_path TEXT NOT NULL,         -- path to raw Legolas output file (research/catalogue/<source>/...)
  curated_at TIMESTAMP,                  -- when elrond curated this session into the DB; NULL while uncurated
  notes TEXT
) STRICT;
```

### 3.4 — `catalogue_assets` — the primary table

One row per asset. Combines Legolas Mode B field spec + the six-axis style rubric + audit-trail.

```sql
CREATE TABLE catalogue_assets (
  -- Identity + source provenance
  asset_uid INTEGER PRIMARY KEY AUTOINCREMENT,  -- elrond-assigned surrogate; stable across re-crawls
  source TEXT NOT NULL REFERENCES catalogue_sources(source),
  source_asset_id TEXT NOT NULL,                 -- source-specific id (the Legolas `asset_id`)
  crawl_session_id TEXT NOT NULL REFERENCES crawl_sessions(session_id),
  source_url TEXT NOT NULL,                      -- the asset's source URL
  source_date DATE NOT NULL,                     -- when source was crawled / claim was true
  source_metadata_raw TEXT NOT NULL,             -- preserved Legolas raw extraction (JSON string)

  -- Display fields
  name TEXT NOT NULL,
  description TEXT,                              -- vendor's description, if available

  -- Content classification (separate dimension from style register)
  category TEXT NOT NULL CHECK (category IN (
    'character', 'enemy', 'vfx', 'environment', 'ui', 'audio', 'tile', 'icon', 'portrait', 'other'
  )),
  dimensionality TEXT NOT NULL CHECK (dimensionality IN ('2d', '3d')) DEFAULT '2d',

  -- Six-axis style rubric (see catalogue-rubric-schema.md)
  rubric_version TEXT NOT NULL DEFAULT '1.0',
  resolution_band TEXT NOT NULL CHECK (resolution_band IN (
    'tiny', 'retro', 'hd2d-pixel', 'narrative-pixel', 'cinematic-pixel', 'raster', 'vector', 'unknown'
  )),
  palette_size TEXT NOT NULL CHECK (palette_size IN (
    '16-color', 'restricted', 'expansive', 'truecolor', 'unknown'
  )),
  shading_technique TEXT NOT NULL CHECK (shading_technique IN (
    'flat-fill', 'single-step', 'dithered', 'gradient-ramp', 'painterly', 'vector-flat', 'unknown'
  )),
  linework_style TEXT NOT NULL CHECK (linework_style IN (
    'hard-1px-outline', 'soft-outline', 'variable-width', 'no-outline', 'vector-clean', 'unknown'
  )),
  animation_frame_density TEXT NOT NULL CHECK (animation_frame_density IN (
    'static', 'low', 'mid', 'high', 'cinematic', 'unknown'
  )),
  derived_register TEXT NOT NULL CHECK (derived_register IN (
    'retro-16bit', 'hand-drawn-pixel', 'clean-vector', 'painterly-raster', 'anime-cel', 'manual-review'
  )),
  derived_register_source TEXT NOT NULL DEFAULT 'rule'
    CHECK (derived_register_source IN ('rule', 'override', 'manual-review-resolved', 'gandalf-call')),
  derived_register_override_rationale TEXT,      -- required when derived_register_source = 'override'

  -- Embodiment tag (character/enemy assets only; see embodiment-narrative-layer.md)
  -- v1.0 enum is the eight starter embodiments + structural placeholders per gandalf dialogue.
  -- New embodiments are NOT pre-loaded — they enter via the narrative-layer amendment protocol.
  embodiment_tag TEXT
    CHECK (embodiment_tag IN (
      'humanoid', 'slime', 'beast', 'dragonling', 'swarm', 'construct', 'spirit', 'plant',
      'pending-amendment',   -- asset depicts a form not yet canonicalized; see pending_amendment_hint
      'not-applicable',      -- non-creature asset (vfx, tile, ui, environment)
      'unknown'              -- creature asset but form is unclear from source
    )),
  pending_amendment_hint TEXT,   -- curator's read when embodiment_tag = 'pending-amendment'
                                 -- e.g., 'looks like undead', 'mecha-form', 'aquatic-merfolk-coded'
                                 -- accumulating hints drive evidence for narrative-layer amendment

  -- Wiring viability (Legolas Mode B decomposition signal — critical for drax's pixi.js consumption)
  decomposition TEXT NOT NULL CHECK (decomposition IN (
    'monolithic', 'decomposed', 'partial', 'not-applicable', 'unknown'
  )),
  -- 'not-applicable' covers VFX / environment / tile categories where decomposition is meaningless.

  -- file_format: closed enum per drax wiring-track Flag 1 (2026-05-16).
  -- The demo's sprite-loading gates differently on 'png' (single frame) vs 'png-spritesheet' (atlas required) vs 'aseprite' (export needed).
  -- A closed value set prevents curators from diverging on format strings ('spritesheet' vs 'png-spritesheet' vs 'sprite_sheet').
  file_format TEXT NOT NULL CHECK (file_format IN (
    'png',                -- single PNG frame
    'png-spritesheet',    -- PNG with multi-frame layout; atlas / frame-rectangles required for parsing
    'aseprite',           -- Aseprite native format; export pass required
    'svg',                -- vector
    'gif',                -- animated GIF
    'jpg',                -- single JPG (rare for game art; allowed for portraits)
    'mp4',                -- video; rare in current scope
    'webm',               -- video; rare in current scope
    'json-atlas',         -- texture-atlas JSON descriptor (paired with png-spritesheet)
    'tmx',                -- Tiled tilemap format
    'wav', 'mp3', 'ogg',  -- audio formats (catalogue may include later)
    'ttf', 'otf',         -- font formats (catalogue may include later)
    'other',              -- legitimate but uncommon format; record specifics in source_metadata_raw
    'unknown'             -- format not determinable from source
  )),

  -- License + cost (see § 4 below for value-set details)
  -- Per gandalf dialogue 2026-05-16: commercial-license split into four narrower values;
  -- itch-standard dropped (meaningless category — itch creators ship every variety).
  license TEXT NOT NULL CHECK (license IN (
    'CC0', 'CC-BY', 'CC-BY-NC', 'CC-BY-SA', 'CC-BY-ND',
    'commercial-royalty-free',     -- CraftPix-style; pay once, ship in any project; indie-pack default
    'commercial-per-project',      -- license is per-game-title
    'commercial-royalty-bearing',  -- per-copy or revenue-share; rare in this market
    'commercial-license',          -- commercial terms apply, specifics-not-yet-parsed; narrower than 'unknown'; force borderline review
    'unity-asset-store',           -- Unity Asset Store standard EULA
    'proprietary',                 -- vendor-specific proprietary; manual review required
    'unknown'                      -- not determinable; treat as no-ship until resolved
  )),
  license_url TEXT,                              -- optional link to license terms
  cost_usd REAL NOT NULL DEFAULT 0.0,            -- 0 for free; numeric amount for paid; flagged in cost_model if non-standard
  cost_model TEXT NOT NULL DEFAULT 'free' CHECK (cost_model IN (
    'free', 'one-time', 'per-seat', 'per-project', 'royalty', 'subscription', 'non-standard', 'unknown'
  )),

  -- Quality / curator review flags
  quality_flag TEXT NOT NULL DEFAULT 'unreviewed'
    CHECK (quality_flag IN ('unreviewed', 'pass', 'borderline', 'fail', 'deferred')),
  quality_rationale TEXT,                        -- free text; populated when quality_flag != 'unreviewed'
  manual_review_queued INTEGER NOT NULL DEFAULT 0 CHECK (manual_review_queued IN (0, 1)),

  -- Audit-trail (Discipline #14 spirit + audit § 6.6)
  curated_at TIMESTAMP NOT NULL,
  curated_by TEXT NOT NULL,                      -- 'elrond' or 'elrond+<script-name>' or 'gandalf' for design-call overrides
  superseded_at TIMESTAMP,                       -- NULL if this is the current curation; set when a newer curation supersedes
  superseded_by_uid INTEGER REFERENCES catalogue_assets(asset_uid),

  -- Uniqueness on the source-anchor pair, within a crawl session, scoped to non-superseded rows.
  -- SQLite syntax: composite UNIQUE on the natural key allows multiple superseded rows + one current.
  UNIQUE (source, source_asset_id, crawl_session_id)
) STRICT;

CREATE INDEX idx_catalogue_assets_source ON catalogue_assets(source);
CREATE INDEX idx_catalogue_assets_category ON catalogue_assets(category);
CREATE INDEX idx_catalogue_assets_derived_register ON catalogue_assets(derived_register);
CREATE INDEX idx_catalogue_assets_embodiment_tag ON catalogue_assets(embodiment_tag) WHERE embodiment_tag IS NOT NULL;
CREATE INDEX idx_catalogue_assets_pending_amendment ON catalogue_assets(pending_amendment_hint) WHERE embodiment_tag = 'pending-amendment';
CREATE INDEX idx_catalogue_assets_decomposition ON catalogue_assets(decomposition);
CREATE INDEX idx_catalogue_assets_license ON catalogue_assets(license);
CREATE INDEX idx_catalogue_assets_current ON catalogue_assets(superseded_at) WHERE superseded_at IS NULL;
```

**Rationale for design choices:**

- **`asset_uid` surrogate.** A stable internal ID independent of source taxonomies. Allows re-crawls and cross-source duplicate detection without ID collisions. Source-specific `(source, source_asset_id)` uniqueness preserves the natural-key constraint.
- **`source_metadata_raw` as TEXT JSON.** SQLite STRICT tables don't have a JSON type; TEXT with JSON1-extension queries is the convention. Preserves Legolas's full extraction for reproducibility and rubric-refinement re-tagging.
- **`derived_register_source = 'rule' | 'override' | 'manual-review-resolved' | 'gandalf-call'`.** Distinguishes how axis 6 got its value. `rule` = deterministic from `catalogue-rubric-schema.md` § 3 rule table. `override` = curator override, rationale required, audit-trail preserved. `manual-review-resolved` = was queued for manual review, resolved by curator. `gandalf-call` = senior-design call — **reserved for register-genuinely-ambiguous cases only**, not for routine curator-vs-rule disagreements (per gandalf dialogue Topic 3; see rubric § 3.1).
- **`embodiment_tag` enum — eight starters + structural placeholders only.** Per gandalf dialogue Topic 4, the v1.0 enum is the eight canonical embodiments from `embodiment-narrative-layer.md` + `pending-amendment` (asset depicts a form not yet canonicalized — curator records hint in `pending_amendment_hint`; asset is fully tagged on other dimensions but blocked from embodiment-specific filtering until the narrative-layer amendment lands) + `not-applicable` (non-creature asset) + `unknown` (creature but form unclear). New embodiments enter via the narrative-layer amendment protocol, NOT by pre-loading the catalogue enum.
- **`pending_amendment_hint TEXT` column.** Captures the curator's read for `pending-amendment`-tagged assets. Accumulating hints across N assets pressure the formal narrative-layer amendment.
- **`decomposition = 'not-applicable'` value.** Per dispatch context, decomposition matters for character/enemy (drax wiring track). For VFX / tile / UI, decomposition is meaningless; `not-applicable` is the legitimate value.
- **`cost_usd REAL NOT NULL DEFAULT 0.0`.** Numeric. Free is `0.0`. Paid is the typical pack price. Non-standard cost models flag in `cost_model`; the numeric is then a representative single-seat one-time price equivalent (curator judgment recorded in notes).
- **`quality_flag` separate from `derived_register`.** Quality is "is this asset worth shipping" — a gandalf-design-track concern. Register is "what style is it." Orthogonal. The license taxonomy in § 4 prescribes default `quality_flag` values per license to surface borderline/ambiguous cases for explicit review.
- **R7 default-borderline interaction with `quality_flag`.** Per `catalogue-rubric-schema.md` § 3.1, the curation script sets `quality_flag = 'borderline'` when R7 (Foozle higher-tier boundary cluster) produces the axis-6 value. The license default (e.g., `commercial-license`'s borderline default) does not override this; whichever produces `borderline` first wins. Multiple borderline-triggers compound into a single `borderline` flag with concatenated rationale.
- **Append-only via `superseded_at`.** Curation overrides don't mutate; they insert a new row with `superseded_by_uid` pointing back. The `idx_catalogue_assets_current` partial index keeps "current rows" queries fast.

### 3.5 — `asset_style_tags`

Secondary style descriptors (Legolas `style_tags` array — `retro`, `anime`, `dark-fantasy`, `cartoony`, etc.). Many-to-many.

```sql
CREATE TABLE asset_style_tags (
  asset_uid INTEGER NOT NULL REFERENCES catalogue_assets(asset_uid) ON DELETE CASCADE,
  tag TEXT NOT NULL,                             -- free-form within the curator's tag vocabulary
  confidence REAL NOT NULL DEFAULT 1.0 CHECK (confidence BETWEEN 0.0 AND 1.0),
  source TEXT NOT NULL CHECK (source IN ('vendor-metadata', 'legolas-inferred', 'elrond-curated')),
  added_at TIMESTAMP NOT NULL,
  PRIMARY KEY (asset_uid, tag)
) STRICT;

CREATE INDEX idx_asset_style_tags_tag ON asset_style_tags(tag);
```

**Why not an enum:** secondary tags are a free vocabulary that grows with experience. Locking them to an enum would block legitimate tag additions. Curator discipline keeps the tag vocabulary clean; elrond maintains a `tag_vocabulary.md` file documenting recognized tags and their meanings.

### 3.6 — `catalogue_packs`

When a vendor groups multiple assets into a pack (Pipoya FREE VFX series, CraftPix Magic Effects Pack), the pack is tracked here. Each `catalogue_assets` row may reference a pack.

```sql
CREATE TABLE catalogue_packs (
  pack_id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL REFERENCES catalogue_sources(source),
  source_pack_id TEXT,                           -- vendor's pack identifier, if any
  pack_name TEXT NOT NULL,
  pack_url TEXT,
  pack_license TEXT CHECK (pack_license IN (     -- hint; per-asset license is authoritative.
                                                  -- 'itch-standard' dropped per gandalf dialogue Topic 5 + drax wiring-track Flag 3.
    'CC0', 'CC-BY', 'CC-BY-NC', 'CC-BY-SA', 'CC-BY-ND',
    'commercial-royalty-free', 'commercial-per-project', 'commercial-royalty-bearing',
    'commercial-license', 'unity-asset-store', 'proprietary', 'mixed', 'unknown'
  )),
  pack_cost_usd REAL,                            -- pack-level cost; per-asset cost may differ
  asset_count INTEGER,                           -- populated as assets are curated
  -- pack_register_consistency: per gandalf dialogue 2026-05-16 (Topic 2 addition).
  -- Populated by the curation script after the pack's assets are all tagged.
  -- 'consistent' = all assets in the pack share the same derived_register; pack is internally coherent.
  -- 'mixed' = assets land in multiple registers; quality signal driving curator suspicion on the vendor's other packs.
  -- 'unknown' = pack not yet fully curated or insufficient evidence.
  pack_register_consistency TEXT NOT NULL DEFAULT 'unknown'
    CHECK (pack_register_consistency IN ('consistent', 'mixed', 'unknown')),
  added_at TIMESTAMP NOT NULL,
  UNIQUE (source, source_pack_id)
) STRICT;
```

And the asset-side back-reference:

```sql
ALTER TABLE catalogue_assets ADD COLUMN pack_id INTEGER REFERENCES catalogue_packs(pack_id);
CREATE INDEX idx_catalogue_assets_pack ON catalogue_assets(pack_id);
```

(In v1.0 migration, `pack_id` is created inline in the `catalogue_assets` DDL above; the ALTER pattern is shown for readability of how the relationship is established.)

### 3.7 — `catalogue_rejections`

When Legolas's sample triggers viability-gate failure (per AGENTS.md § "Viability-gate workflow (catalogue work)"), the rejection is recorded so future passes don't repeat the dead end.

```sql
CREATE TABLE catalogue_rejections (
  rejection_id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,                          -- not FK; rejection may name a source we never added
  pack_name TEXT,                                -- if rejection is pack-specific
  rejection_date DATE NOT NULL,
  failure_track TEXT NOT NULL CHECK (failure_track IN ('structural', 'wiring', 'design', 'multi-track')),
  failure_rationale TEXT NOT NULL,               -- elrond / drax / gandalf rationale
  reviewer TEXT NOT NULL,                        -- 'elrond', 'drax', 'gandalf', or comma-list for multi-track
  re_sampleable INTEGER NOT NULL DEFAULT 0 CHECK (re_sampleable IN (0, 1)),  -- can extraction strategy be adjusted and re-sampled?
  notes TEXT
) STRICT;
```

### 3.8 — `abstraction_groupings` (future)

Per audit § 5.3, when elrond performs emergent-grouping analysis on the catalogue (e.g., "what visual-style clusters emerge from the corpus"), groupings are stored here as analytical outputs. Stub-defined at v1.0 for forward-compatibility; not actively populated until first analysis lands.

```sql
CREATE TABLE abstraction_groupings (
  grouping_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,                            -- e.g., 'emergent-visual-clusters-2026-06-01'
  dimension TEXT NOT NULL,                       -- 'visual-style' / 'embodiment-form' / 'license-coverage' / ...
  created_by_analysis TEXT NOT NULL,             -- path to the analysis script under research/scripts/
  created_at TIMESTAMP NOT NULL,
  member_count INTEGER,
  description TEXT
) STRICT;

CREATE TABLE asset_grouping_membership (
  asset_uid INTEGER NOT NULL REFERENCES catalogue_assets(asset_uid) ON DELETE CASCADE,
  grouping_id INTEGER NOT NULL REFERENCES abstraction_groupings(grouping_id) ON DELETE CASCADE,
  confidence REAL NOT NULL DEFAULT 1.0 CHECK (confidence BETWEEN 0.0 AND 1.0),
  PRIMARY KEY (asset_uid, grouping_id)
) STRICT;
```

---

## 4. License taxonomy — explicit value set + meaning

Per `catalogue-rubric-schema.md` § 9 dialogue Topic 5 + audit § 6.5, the `license` column rejects NULL and uses these values. The Topic-5 refinements (commercial-license split into four; itch-standard dropped) reflect gandalf's design-track read that curators must record the *real* license each asset carries, not a shortcut bucket.

| Value | Meaning | Commercial-use OK? | Default `quality_flag` on insert |
|---|---|---|---|
| `CC0` | Creative Commons Zero — public domain dedication | Yes | `pass` |
| `CC-BY` | Creative Commons Attribution | Yes, with attribution | `pass` |
| `CC-BY-NC` | Creative Commons Attribution Non-Commercial | **No** — excluded from default consumption filter | `pass` (license-clear; just non-commercial) |
| `CC-BY-SA` | Creative Commons Attribution ShareAlike | Yes, with attribution + share-alike | `pass` |
| `CC-BY-ND` | Creative Commons Attribution NoDerivs | Yes, with attribution, no modification — usable for unmodified assets only | `pass` |
| `commercial-royalty-free` | Pay once, ship in any number of projects, no per-copy royalty. CraftPix-style, GameDev Market-style. The dominant indie-pack license model. | Yes | `pass` |
| `commercial-per-project` | License is per-game-title. Less common; some Unity Asset Store entries. | Yes, scoped to one project | `pass` |
| `commercial-royalty-bearing` | Per-copy royalty or revenue-share. Rare in this asset market; may surface in music/SFX catalogue later. | Conditional — terms matter | `borderline` (forces manual review) |
| `commercial-license` | Commercial terms apply, specifics-not-yet-parsed. Narrower escape valve than `unknown` — used when the asset's commercial-friendliness is established but the exact license variant isn't yet read. | Conditional — pending parsing | `borderline` (forces manual review) |
| `unity-asset-store` | Unity Asset Store standard EULA | Yes within Unity terms; uncertain outside Unity context | `pass` |
| `proprietary` | Vendor-specific proprietary; manual review required for usage | **Conditional** — manual review | `borderline` |
| `unknown` | Not determinable from source metadata; queued for clarification | **Treat as no-ship until resolved** | `borderline` |

**Notes:**
- `itch-standard` was **removed** from v1.0 (was in earlier drafts). itch.io creators ship every license variety; the value was a shortcut bucket curators would mis-use. Force the read.
- `license_url`: optional link to the license document. **Required when** `license = 'commercial-license'` or `proprietary` — those values demand the reader can verify terms.
- `quality_flag` and `quality_rationale` carry license-clarity concerns: when the rubric assigns `borderline` by license-default, curators resolve via documentation read; `pass` is the post-review confirmation.
- **Viability-gate sample threshold (per gandalf dialogue Topic 5 strengthening):** at sample-time, if **>20% of a sample carries `license = 'unknown'`**, the sample fails the design-track viability gate on data-hygiene grounds. The catalogue's job is to know what we can ship; unknown-heavy samples indicate the curation pass didn't do its job, not that the source is unusable. Re-curation requested; failure rationale recorded in `catalogue_rejections` if not addressable.

### 4.1 — Default consumption filter (the locked-Reincarnated read)

Drax / Star-lord / Gandalf-design-track query the catalogue at consumption time using this filter as the locked-register default:

```sql
WHERE derived_register = 'hand-drawn-pixel'
  AND license IN ('CC0', 'CC-BY', 'CC-BY-SA', 'CC-BY-ND',
                  'commercial-royalty-free', 'commercial-per-project',
                  'unity-asset-store')                        -- commercial-OK; specifics-clear
  AND quality_flag IN ('pass')                                -- not borderline / fail / deferred / unreviewed
  AND superseded_at IS NULL
  AND embodiment_tag != 'pending-amendment'                    -- exclude assets blocked on narrative-layer amendment
```

Variants for the form-bias case study and the register-pivot impact analysis appear in § 5.

---

## 5. Cross-store join patterns (per audit § 8)

The catalogue.db is the **primary connection**; engine telemetry is **ATTACH-read-only** when joining.

### 5.1 — Standard cross-store query template

```python
import sqlite3
conn = sqlite3.connect("agentic_orchestration/research/curated/catalogue.db")
conn.execute("PRAGMA foreign_keys = ON;")
conn.execute(
    "ATTACH DATABASE 'file:///Users/admin/Games/reincarnated-engine/data/telemetry.db?mode=ro' AS engine"
)
# Now: SELECT ... FROM catalogue_assets c JOIN engine.classes cls ON cls.embodiment = c.embodiment_tag ...
```

### 5.2 — Worked example: form-bias work

"For each engine-generated monster archetype × embodiment, count catalogue assets in the locked register with appropriate decomposition signal."

```sql
SELECT
  m.sprite_archetype_tag,
  c.embodiment_tag,
  COUNT(*) AS asset_count
FROM engine.monsters m
JOIN catalogue_assets c
  ON c.embodiment_tag = m.embodiment      -- (when engine emits this field)
WHERE c.derived_register = 'hand-drawn-pixel'
  AND c.category IN ('character', 'enemy')
  AND c.decomposition IN ('decomposed', 'partial')
  AND c.license != 'CC-BY-NC'             -- exclude non-commercial
  AND c.license != 'unknown'              -- exclude unverified
  AND c.superseded_at IS NULL
GROUP BY m.sprite_archetype_tag, c.embodiment_tag
ORDER BY asset_count DESC;
```

This is the form-bias unblocker per doc 37 § 8.

### 5.3 — Worked example: drax consumption filter

"Give me all hand-drawn-pixel character assets, decomposed, commercial-OK, with their license terms and source."

```sql
SELECT
  c.asset_uid, c.name, c.source, c.source_url,
  c.embodiment_tag, c.resolution_band, c.animation_frame_density,
  c.license, c.cost_usd
FROM catalogue_assets c
WHERE c.derived_register = 'hand-drawn-pixel'
  AND c.category = 'character'
  AND c.decomposition = 'decomposed'
  AND c.license IN ('CC0', 'CC-BY', 'CC-BY-SA', 'commercial-royalty-free', 'commercial-per-project', 'unity-asset-store')
  AND c.superseded_at IS NULL
ORDER BY c.embodiment_tag, c.resolution_band;
```

### 5.4 — Worked example: register-pivot impact analysis

"If we pivot from hand-drawn-pixel to retro-16bit, what's our coverage delta?"

```sql
SELECT
  category,
  derived_register,
  COUNT(*) AS asset_count
FROM catalogue_assets
WHERE superseded_at IS NULL
GROUP BY category, derived_register
ORDER BY category, asset_count DESC;
```

Pivot-insurance lives in the data; the query answers the impact without re-crawl.

---

## 6. Schema migration policy

Per audit § 6.4 + `MIGRATION.md` v1.0 entry:

- **Additive migrations (v1.x):** new column, new optional table, new value in an open enum (but **CHECK constraints lock enum value sets** — adding a value requires a migration). Forward-compatible; existing rows remain valid. Migration script in `research/scripts/catalogue_migrations/v1_x_*.sql`. MIGRATION.md entry.
- **Breaking migrations (v2.0+):** column type change, column rename, constraint change in a way that requires existing rows to be updated. Senior-design approval (Matt) per ADR-002. Migration script + back-fill script + verification query. MIGRATION.md entry with rollback plan.
- **No silent transformations.** Every migration logs each row touched; back-fill output is captured in a `migration_runs` table (forward-defined; created in v1.1 if first migration warrants it).

---

## 7. Curation pipeline contract (overview; full spec in `curation-pipeline.md`)

The schema accepts data through a curation pipeline, not from arbitrary writers. Pipeline contract:

1. **Input:** Legolas raw output file (JSON Lines under `research/catalogue/<source>/<session-id>.jsonl`).
2. **Curation script** (`research/scripts/curate_catalogue.py` — to be implemented) reads raw output, applies deduplication / normalization / validation, runs deterministic axis-6 rule (§ 3 of rubric-schema.md), inserts rows.
3. **Manual-review queue** flags rows where axis values can't be determined from raw extraction; elrond resolves by visual inspection.
4. **Quality-flag pass** by curator: pass / borderline / fail / deferred, with rationale.
5. **MIGRATION.md update** when schema changes; `curation_runs` table tracks each curation invocation (defined in v1.1 if needed).

Curation is **append-only** with `superseded_at`. No row is overwritten in place.

---

## 8. Cross-references

- `catalogue-rubric-schema.md` — the six-axis rubric this schema implements
- `curator-tagging-guide.md` — per-axis curator instructions (when authored)
- `curation-pipeline.md` — operational pipeline doc (when authored)
- `MIGRATION.md` — schema migration log (v1.0 entry pending)
- `data-architecture-audit-2026-05-16.md` — § 5.3 (L3 layer; this DB), § 5.1 (four-layer separation), § 6 (schema conventions), § 8 (cross-store query patterns)
- `canonical/story/style-register.md` — the locked register
- `canonical/story/embodiment-narrative-layer.md` — the embodiment-tag value set
- `canonical/story/enemy-visual-legibility.md` — sprite-archetype registry (downstream consumer of catalogue queries)
- `AGENTS.md` § "Viability-gate workflow (catalogue work)" + § "Score-don't-filter principle"
- `~/.claude/agents/legolas.md` Mode B field spec (the upstream extraction contract)

---

— elrond, 2026-05-16, post-gandalf-dialogue. Schema design locked v1.0; pending Matt approval before live application.
