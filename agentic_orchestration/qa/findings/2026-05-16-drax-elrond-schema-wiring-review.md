# Finding — 2026-05-16 — drax-elrond catalogue schema wiring review

**Reviewer:** drax
**Severity:** PASS WITH FLAGS
**Target:** Elrond catalogue schema (catalogue-rubric-schema.md + catalogue-schema.md)
**Dispatch:** agentic_orchestration/dispatches/2026-05-16-elrond-catalogue-db-schema.md

---

## Verdict (one line)

Schema is wireable against both stacks in current state; no blocking adaptation required before catalogue rollout, but three flags require Elrond's documented response before the wiring is considered clean.

---

## Per-criterion assessment

### 1. Pixi.js consumption viability

**Assessment: PASS WITH FLAGS**

The schema provides the fields the demo pipeline needs to do its job at consumption time. The wiring path is not blocked. Specific findings per field cluster:

**Directly usable today:**

- `source_url` — the asset URL the demo will eventually load sprites from. The demo's `archetypeRenderer.ts` already loads from paths passed to `BaseTexture.from(path)`; `source_url` slots directly into that pattern.
- `file_format` — the demo can gate on `'png'` or `'png-spritesheet'` vs `'gif'` or `'mp4'` without any schema change. The existing loader pattern uses `PIXI.Assets.load()` which is format-agnostic for Pixi-supported formats.
- `derived_register` — the consumption-time filter column. Demo queries `WHERE derived_register = 'hand-drawn-pixel'` to get the locked-register asset set. This is straightforward SQL read; no demo-side transformation.
- `decomposition` — directly usable as a wiring gate. The demo only ingests `'decomposed'` or `'partial'` assets for character/enemy (sprite sheets with named regions). `'monolithic'` assets can be excluded at the SQL layer without demo-side adaptation.
- `embodiment_tag` — maps directly to the `sprite_archetype_tag` routing in `archetypeRenderer.ts`. The existing `SPECS` record already keys on archetype strings; embodiment_tag values (`humanoid`, `slime`, `beast`, `brute`, etc.) would populate the same lookup table.
- `resolution_band` — usable as a Pixi.js sizing hint. The demo's `tierScale()` function currently drives size from tier; `resolution_band` lets the demo choose the right sprite sheet variant without computing size from tier independently.
- `asset_uid` — stable surrogate ID, directly usable as the registry key in the sprite-archetype registry.

**FLAG 1 — `file_format` enum is underspecified for sprite-sheet consumption.**

The schema defines `file_format` as a free-text `TEXT NOT NULL` column (no enum, no CHECK constraint). The catalogue-schema.md lists `'png', 'png-spritesheet', 'aseprite', 'svg', 'gif', 'mp4'` as examples, but these are not constrained values. For the demo pipeline, the difference between `'png'` (single frame), `'png-spritesheet'` (requires atlas or manual frame rectangle), and `'aseprite'` (requires export step) is a branching wiring decision. If curators record `'spritesheet'` vs `'png-spritesheet'` vs `'sprite_sheet'`, the demo cannot write a reliable gate.

**Specific ask:** Add a CHECK constraint to `file_format` with an explicit closed value set. Minimum values needed: `'png'`, `'png-spritesheet'`, `'aseprite'`, `'svg'`, `'gif'`, `'mp4'`, `'unknown'`. This is an additive v1.x change; no re-tagging of rows already carrying the correct values.

**No animation-atlas pointer field in the schema.**

This is not a blocking flag for the schema itself — it is a known future wiring concern. The schema captures `file_format` and `source_url` but does not capture the atlas JSON URL (the companion descriptor for sprite sheets specifying frame rectangles). This is appropriate for v1.0: the catalogue's job is to identify and classify assets, not to serve as the full asset-serving layer. The demo's sprite-loading will require a separate atlas-companion convention when real HD-2D sprite sheets enter the pipeline. Tracking this here so the future drax dispatch for S1 sprite-archetype registry work can plan for it.

**Sprite-sheet shape conventions:**

The schema does not define sprite-sheet frame layout conventions (LPC format vs custom atlas vs Aseprite export). This is also appropriate for v1.0 — the schema's `source_metadata_raw` preserves Legolas's full extraction, so vendor-specific format details survive. The demo's eventual loader will need to negotiate per-vendor frame conventions. Not a schema bug; a future wiring task.

---

### 2. Sprite-archetype registry compatibility

**Assessment: PASS**

The schema cleanly supports the sprite-archetype registry pattern locked in `enemy-visual-legibility.md` § S1.

The wiring path: `catalogue_assets.embodiment_tag` JOIN `catalogue_assets.category = 'enemy'` JOIN `derived_register = 'hand-drawn-pixel'` JOIN `decomposition IN ('decomposed', 'partial')` returns the candidate asset set for the registry. The demo's registry (`archetypeRenderer.ts` SPECS record) is keyed on `archetype_tag` strings; the catalogue's `embodiment_tag` provides the content-axis join key.

The cross-store query example in `catalogue-schema.md` § 5.2 already sketches this exactly:

```sql
SELECT m.sprite_archetype_tag, c.embodiment_tag, COUNT(*) AS asset_count
FROM engine.monsters m
JOIN catalogue_assets c ON c.embodiment_tag = m.embodiment
WHERE c.derived_register = 'hand-drawn-pixel'
  AND c.category IN ('character', 'enemy')
  AND c.decomposition IN ('decomposed', 'partial')
  AND c.superseded_at IS NULL
GROUP BY m.sprite_archetype_tag, c.embodiment_tag;
```

This is the form-bias unblocker query the demo eventually needs to populate the registry. The schema supports it without adaptation.

One structural alignment to note: `enemy-visual-legibility.md` S1 specifies 6 base monster archetypes (brute / caster / controller / sniper / swarmer / tank). The demo's `archetypeRenderer.ts` SPECS already implements exactly these 6 monster archetype tags. The catalogue's `embodiment_tag` covers the embodiment layer (what form the creature is) while `archetype_tag` (on the engine's monster output) covers the combat-role layer. These are orthogonal dimensions — the schema correctly keeps them separate. A slime embodiment can be a caster archetype; the registry maps the combat archetype to a visual spec, then the embodiment modulates the sprite choice within that spec. Schema design supports this correctly.

The `pending-amendment` holding pattern for unsupported embodiment values is also correct from the wiring perspective. Assets with `embodiment_tag = 'pending-amendment'` are excluded from the default consumption filter and will not enter the registry until their embodiment is canonicalized. This is the right behavior; the demo does not want unknown embodiment types entering the registry silently.

---

### 3. Style-register filter query feasibility

**Assessment: PASS**

The filter query for the locked HD-2D-shaped register is feasible and clean. The six-axis rubric provides the columns needed. The deterministic classification rule (§ 3 of the rubric-schema) means `derived_register` is reliably populated for the vast majority of assets, reducing the filter to a single-column predicate in the common case.

**Filter query for the locked Reincarnated register (enemy/character assets, demo consumption):**

```sql
SELECT
  c.asset_uid,
  c.name,
  c.source_url,
  c.file_format,
  c.embodiment_tag,
  c.resolution_band,
  c.animation_frame_density,
  c.license,
  c.cost_usd,
  c.decomposition
FROM catalogue_assets c
WHERE c.derived_register = 'hand-drawn-pixel'
  AND c.category IN ('character', 'enemy')
  AND c.decomposition IN ('decomposed', 'partial')
  AND c.license IN (
    'CC0', 'CC-BY', 'CC-BY-SA', 'CC-BY-ND',
    'commercial-royalty-free', 'commercial-per-project',
    'unity-asset-store'
  )
  AND c.quality_flag = 'pass'
  AND c.superseded_at IS NULL
  AND c.embodiment_tag != 'pending-amendment'
ORDER BY c.embodiment_tag, c.resolution_band;
```

This returns the demo's actionable registry-population set. All predicates map to indexed columns (`derived_register`, `category`, `decomposition`, `license`, `superseded_at` all have explicit indexes in the schema).

**Handling of `manual-review` cases:**

Assets where the deterministic rule produces `manual-review` are excluded from this query (they do not have `derived_register = 'hand-drawn-pixel'`). They do not block the query. They accumulate in a manual-review queue and are resolved before entering the consumption-ready set. This is the correct behavior: the filter works cleanly for the automated-classification majority; manual-review is a curation workflow, not a query complication.

**Scene-level outline-profile constraint (R6 side effect):**

The `outline-profile:hard-1px` vs `outline-profile:soft-or-variable` secondary tag lives in `asset_style_tags` (the many-to-many table). Scene-level coherence filtering requires a JOIN against `asset_style_tags`:

```sql
SELECT c.asset_uid, c.name, c.source_url, ast.tag AS outline_profile
FROM catalogue_assets c
JOIN asset_style_tags ast ON ast.asset_uid = c.asset_uid
  AND ast.tag IN ('outline-profile:hard-1px', 'outline-profile:soft-or-variable')
WHERE c.derived_register = 'hand-drawn-pixel'
  AND c.category IN ('character', 'enemy')
  AND c.superseded_at IS NULL
  AND ast.tag = 'outline-profile:soft-or-variable'  -- constrain to one scene-coherent profile
```

This is clean and writable. The demo's scene-level filter picks one outline-profile for a given encounter and constraints to it. The schema supports this correctly.

---

### 4. Loadout app consumption

**Assessment: PASS WITH FLAGS**

The loadout app (`reincarnated-loadout/`) currently consumes engine output (season data, gear pool, class data) and does not yet consume catalogue data directly. When catalogue assets reach the loadout (gear card art, character display), the following field-by-field compatibility holds:

**Compatible fields (directly usable):**

- `name` (TEXT NOT NULL) — compatible with all loadout card displays; the `GearPoolEntry.name` field follows the same pattern.
- `source_url` (TEXT NOT NULL) — the URL string pattern is directly usable as an `<img src>` value in React. No type conversion needed.
- `license` (TEXT NOT NULL, enum) — the license taxonomy maps cleanly to the loadout's display needs (attribution footer for CC-BY, etc.).
- `cost_usd` (REAL NOT NULL DEFAULT 0.0) — numeric; directly displayable.
- `embodiment_tag` (TEXT, nullable) — nullable correctly handled; `not-applicable` value for non-character assets is a string, not null, which means the loadout can reliably type-check it without null guards.
- `derived_register` (TEXT NOT NULL) — enum string; directly usable as a CSS class selector or display label.
- `quality_flag` (TEXT NOT NULL) — the `'pass'` value as the loadout's render gate is straightforward.

**FLAG 2 — `asset_style_tags.confidence` field (REAL, 0.0-1.0) has no loadout UI analog yet.**

The confidence score on secondary tags is accurate and important for curator-workflow purposes, but the loadout has no existing pattern for rendering confidence-weighted metadata. When gear card art includes a tag (e.g., a style tag like `dark-fantasy` surfaced on the loadout card), the loadout will need to decide whether to filter on `confidence > 0.8` or display the tag unconditionally. This is not a schema problem — the schema is correct to capture confidence. It is a future loadout-side rendering decision. Flagging so Elrond is aware the loadout will need a confidence threshold convention when tags surface in the UI.

**FLAG 3 — `catalogue_sources.default_license` references `'itch-standard'` in its CHECK constraint while the per-asset `licence` column's `'itch-standard'` value was dropped from the v1.0 enum.**

Reading `catalogue-schema.md` § 3.2 carefully: `catalogue_sources.default_license` CHECK constraint includes `'itch-standard'` as a valid value (line: `'commercial-license', 'itch-standard', 'unity-asset-store', 'proprietary', 'mixed', 'unknown'`). However, `catalogue-rubric-schema.md` § 9 Topic 5 records the gandalf-dialogue decision to drop `'itch-standard'` because it is a meaningless category. The per-asset `licence` column correctly omits it. But the vendor-level `catalogue_sources.default_license` still carries `'itch-standard'` in its CHECK.

This is a schema internal inconsistency, not a wiring blocker — but it means a curator who records `default_license = 'itch-standard'` at the source level is using a value the per-asset standard considers dropped. The inconsistency will surface as a subtle data-hygiene issue downstream. Flagging for Elrond to align `catalogue_sources.default_license` CHECK to the same post-dialogue license enum.

---

### 5. Demo viability in current state vs demo update needed

**Assessment: (A) Demo consumes as-is, with one qualification**

The current `reincarnated-demo/` and `reincarnated-loadout/` codebases can ingest assets tagged against this schema without requiring a demo-side adaptation patch before catalogue rollout. The schema provides a superset of what the demo currently needs, and the consumption path (SQL query → asset_uid + source_url + embodiment_tag + file_format → demo registry population) is writable against existing demo patterns.

**The qualification:** the demo's current sprite-archetype registry (`archetypeRenderer.ts` SPECS record) is programmatic and populated at code-write time, not at runtime from the catalogue. The schema does not break this — it is designed as the eventual data source for that registry, not an immediate runtime replacement. The wiring from schema to demo is a future dispatch (the S1 sprite-archetype registry dispatch referenced in `enemy-visual-legibility.md`), not something the current schema blocks.

**No demo-side patch is needed before catalogue rollout.** Catalogue work can proceed; Legolas can crawl and tag against this schema; Elrond can curate. When drax's S1 registry dispatch lands, the demo will wire against the schema as designed.

---

## Specific gaps or missing artifacts

The following dispatch deliverables specified in `2026-05-16-elrond-catalogue-db-schema.md` are not yet present in `agentic_orchestration/research/curated/`:

1. **`MIGRATION.md`** — listed as a required deliverable; not present. The dispatch requires a v1.0 entry documenting the initial schema. Acceptance criteria: "MIGRATION.md committed with v1.0 entry."

2. **`catalogue.db`** — the empty SQLite file with schema applied. Not present. Acceptance criteria: "empty catalogue.db created with schema applied; visible via `sqlite3 catalogue.db .schema`." (Note: `.db`, `.db-wal`, `.db-shm` are specified as gitignored, but there is also no `.gitignore` file in the `research/curated/` directory. Both the `.gitignore` and the `catalogue.db` itself are missing.)

3. **`curation-pipeline.md`** — operational pipeline doc. Not present. Referenced in `catalogue-schema.md` § 7 as a companion doc but not yet committed.

4. **`catalogue-rubric-validation-2026-05-16.md`** — the validation pass on existing empirical research (Dispatch deliverable 4). Not present. Referenced in `catalogue-rubric-schema.md` § 10 but not yet committed.

5. **`pivot-insurance-ledger.md`** — specified as a new file in `catalogue-rubric-schema.md` § 9 Topic 6 (gandalf-dialogue outcome). Not present.

**What IS present:** `catalogue-rubric-schema.md`, `catalogue-schema.md`, and `curator-tagging-guide.md`. Three of the eight acceptance criteria are met.

**Assessment of gap severity:** The three missing docs (MIGRATION.md, curation-pipeline.md, pivot-insurance-ledger.md) and two missing files (catalogue.db + .gitignore) are dispatch-completion blockers per the acceptance criteria, but they are NOT wiring-track blockers for this review. The wiring review is on the schema design itself. The schema design is sound. Elrond should complete the missing artifacts to close the dispatch per acceptance criteria, but drax's wiring verdict is not contingent on those artifacts being present.

---

## Recommendations to Elrond

**Flag 1 (FILE_FORMAT ENUM — moderate priority):** Add a CHECK constraint to `catalogue_assets.file_format` with a closed value set. Suggested minimum: `'png'`, `'png-spritesheet'`, `'aseprite'`, `'svg'`, `'gif'`, `'mp4'`, `'unknown'`. This is a v1.x additive migration (add constraint to existing column); requires a MIGRATION.md entry. Do this before the first Legolas crawl session inserts rows, so curators cannot accidentally diverge on format strings.

**Flag 2 (CONFIDENCE THRESHOLD — low priority, defer):** When catalogue tags begin surfacing in the loadout app UI, document the confidence threshold convention (e.g., `confidence >= 0.8` for display). Not a schema change; a loadout-side rendering convention. Can be deferred to the drax S1 dispatch.

**Flag 3 (ITCH-STANDARD IN SOURCES TABLE — low priority):** Remove `'itch-standard'` from `catalogue_sources.default_license` CHECK constraint, consistent with the per-asset license enum drop (gandalf dialogue Topic 5). Either drop the value or replace with `'mixed'` as the vendor-level escape valve. This is a v1.x migration if rows already exist; a DDL fix before the DB is created if the empty DB hasn't been applied yet. Since the DB does not yet exist, this is a DDL-edit-before-first-apply fix — no migration script needed, just correct the schema definition.

**Missing artifacts (dispatch completion — various priority):**

- `MIGRATION.md` — required before dispatch is declared complete; low effort; write now.
- `.gitignore` for the `research/curated/` directory — required so `catalogue.db` is not accidentally committed; write alongside the empty DB.
- `catalogue.db` — required per acceptance criteria; `sqlite3 catalogue.db < schema.sql && sqlite3 catalogue.db .schema` to verify.
- `curation-pipeline.md` — required per acceptance criteria; authored to the § 7 overview already in catalogue-schema.md.
- `catalogue-rubric-validation-2026-05-16.md` — required per acceptance criteria (Dispatch deliverable 4).
- `pivot-insurance-ledger.md` — required per gandalf-dialogue outcome record; referenced from catalogue-rubric-schema.md § 9 Topic 6.

---

## What this unblocks (PASS WITH FLAGS)

- **Legolas Pimen sample dispatch** — knight-rider can release. The schema is wireable; Legolas can crawl and tag against it. Assets tagged against the current schema will be consumable by drax without rework.
- **Elrond curation work** — can proceed. The schema design is sound for curation use.
- **Future drax S1 registry dispatch** — has a clear schema target to wire against. No schema changes required before that dispatch begins.

---

## What this blocks (none, given PASS WITH FLAGS)

No catalogue work is blocked. Elrond's documented response to the three flags closes this review. Flag 1 (file_format enum) is the only one with enough impact to warrant Elrond's explicit decision on whether to fix in this dispatch or defer to v1.1.

---

— drax, 2026-05-16
