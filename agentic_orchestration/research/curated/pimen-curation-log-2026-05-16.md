# Pimen full-catalogue curation log — 2026-05-16

**Owner:** elrond
**Dispatch:** `2026-05-16-elrond-pimen-full-catalogue-curation.md`
**Crawl session:** `legolas-pimen-mode-b-full-2026-05-16`
**Curator script:** `agentic_orchestration/research/scripts/curate_pimen_full_2026_05_16.py`
**Curated output:** `pimen-catalogue-curated-2026-05-16.jsonl` (47 rows)
**Bundle output:** `pimen-bundle-relationships-2026-05-16.json`
**DB target:** `catalogue.db` (schema v1.0; unchanged)

---

## 0. One-line summary

46 raw rows → 47 curated rows (+1 from earth-spell-effect-03 category split). All four dispatch pre-processor rules applied; CC-BY 4.0 attribution tagged on 2 rows; bundle relationships normalized; v1.0 schema preserved (no schema rework).

---

## 1. Row-count reconciliation

| Stage | Count | Notes |
|---|---:|---|
| Raw Legolas extraction | 46 | `full-2026-05-16.jsonl` |
| After Step 5 category split | 47 | `earth-spell-effect-03` spawned sister `earth-spell-effect-03::enemy-elemental` |
| catalogue.db row count | 47 | post-ingest verification: `SELECT COUNT(*) FROM catalogue_assets = 47` |
| asset_style_tags row count | 444 | 328 legolas-inferred + 116 elrond-curated |
| catalogue_packs | 3 | mega-pack-01, mega-pack-02, earth-spell-effect-03 |
| crawl_sessions | 1 | this session |
| catalogue_sources | 1 | `itch-pimen` registered |

---

## 2. Pre-processor rule applications

### Rule 1 — R5 derivation cascade for `style_register: "pixel-art"`

**Cascade priority (first match wins):**

1. `style_tags ⊇ {'hand-drawn-pixel'}`                    → `hand-drawn-pixel` (positive-tag signal)
2. `style_tags ⊇ {'retro'}` AND `resolution_band ∈ {tiny, retro}` → `retro-16bit`
3. `style_tags ⊇ {'sub-register-uncertain'}`              → `manual-review` (Legolas explicit defer)
4. `resolution_band = 'hd2d-pixel'` AND vendor-hint = `hand-drawn-pixel` → `hand-drawn-pixel` (vendor-hint inference, `quality_flag = borderline`)
5. default                                                  → `manual-review`

**Outcomes:**

| derived_register | count | rule_fired distribution |
|---|---:|---|
| `hand-drawn-pixel` | 28 | 27× `R5-handdrawn-tag-positive`, 1× `R5-vendor-hint-inferred-from-band` (`fantasy-skeleton-enemies`) |
| `retro-16bit` | 2 | 2× `R5-retro-tag-and-band` (`battle-vfx-projectile`, `pixel-battle-effects`) |
| `manual-review` | 17 | 15× `R5-sub-register-uncertain-explicit`, 2× `R5-default-conservative` (`cutting-and-healing`, `fantasy-platformer-character`) |
| **total** | **47** | |

**Important note on coverage of axes 2 / 3 / 4:** all 47 rows have `palette_size = unknown`, `shading_technique = unknown`, `linework_style = unknown` because Pimen (and no other vendor) supplies these without frame access. Per structural-review Flag 5, axes 2/3/4 are post-acquisition-inspection territory; `derived_register` is determined by the R5 cascade above which leans on positive style_tags (Legolas-inferred) and resolution-band signals.

**Side-effect deferred:** R6 outline-profile tagging (`outline-profile:hard-1px` vs `outline-profile:soft-or-variable`) does not fire automatically because `linework_style` is universally `unknown`. The 28 hand-drawn-pixel rows therefore lack the outline-profile secondary tag at this curation pass — to be back-filled during the post-acquisition visual-inspection step. Documented for downstream awareness (drax's scene-coherence filter on outline-profile cannot yet constrain pimen's hand-drawn-pixel rows).

### Rule 2 — `pimen_element` migrated to `source_metadata_raw` + emitted as queryable tag

**Implementation:**
- The raw `pimen_element` field is preserved verbatim inside `source_metadata_raw` (which contains the entire raw row).
- A queryable tag is emitted per `asset_style_tags`: `pimen-element:<value>` where value is one of `fire / water / ice / holy / dark / earth / wind / thunder / acid / wood / multi`.

**Coverage:** 23 of 46 raw rows had non-null `pimen_element`. Tag emitted on 23 curated rows (the 47th — the enemy-elemental sister of earth-spell-effect-03 — was not given the tag; the parent vfx row keeps it).

**Generalization note:** the tag prefix convention (`pimen-element:`) is vendor-namespaced for future crawls. CreativeKind, CraftPix, Foozle, etc. would use `creativekind-element:`, `craftpix-element:`, etc. when their crawls land. The `asset_style_tags.tag` column is free-text (no CHECK constraint), so the namespace can grow without schema rework.

### Rule 3 — `file_format` prose parser

**Implementation:** `parse_file_format()` in `curate_pimen_full_2026_05_16.py`. Output structure stored in `source_metadata_raw._curation_overlay_2026_05_16.parsed_file_format`:

```json
{
  "canonical": "<png | png-spritesheet | aseprite | gif | unknown>",
  "archive_format": "<rar | zip | null>",
  "archive_size_kb": <float or null>,
  "has_spritesheet": <bool>,
  "has_individual_frames": <bool>,
  "has_aseprite_source": <bool>,
  "has_gif": <bool>,
  "raw_string": "<verbatim raw>",
  "parser_notes": [<list>]
}
```

**Canonical cascade:**

| Pattern | → canonical |
|---|---|
| Contains "spritesheet" | `png-spritesheet` |
| "aseprite" + "png" present (no spritesheet) | `png` (treats PNG as primary delivery; aseprite is editor source) |
| "aseprite" only (no png) | `aseprite` |
| "gif" only (no png) | `gif` |
| "png" present | `png` |
| Source = `itch-pimen` AND archive-only string (RAR/ZIP, no format keywords) | `png` (vendor-heuristic: pimen is PNG-only) + `parser_notes = ['format_inferred_from_vendor=pimen-png-only-heuristic']` |
| Otherwise | `unknown` + `parser_notes = ['file_format_unparseable']` |

**Aseprite negation guard:** `has_aseprite_source` is set TRUE only when "aseprite" appears AND the row does NOT contain the negation pattern `"no aseprite"`. Three rows correctly classified as `has_aseprite_source = false` despite containing the substring "aseprite": `mega-pack-elemental-spell-effects` ("No Aseprite source files confirmed"), `buff-n-debuff-vfx-pack-01` ("No Aseprite files"), `smoke-n-dust-03` ("No Aseprite files").

**Result distribution:**

| canonical | rows |
|---|---:|
| `png-spritesheet` | 25 |
| `png` | 22 |
| **total** | **47** |

| has_aseprite_source | rows |
|---|---:|
| true | 13 |
| false | 34 |
| **total** | **47** |

Matches Legolas's headline stat (13 packs include Aseprite source).

### Rule 4 — `requires_visual_inspection` flag

**Implementation:** all rows with `resolution_band = 'unknown'` get:
- `source_metadata_raw._curation_overlay_2026_05_16.requires_visual_inspection = true`
- queryable tag `asset_style_tags.tag = 'requires-visual-inspection'`
- `manual_review_queued = 1` (DB column)

**Coverage:** 21 of 47 curated rows (the 20 unknown-resolution raw rows + 1 inherited by the earth-spell-effect-03 enemy-elemental sister).

**Breakdown of 21:**
- **16 FREE rows** with `unknown` resolution_band → primary visual-inspection target. Acquire+inspect cost low.
- **4 PAID rows** with `unknown` resolution_band → higher priority for upfront visual inspection (purchase decision implicates cost): `earth-spell-effect-03` ($3), `thunder-spell-effect-03` ($3), `mega-pack-elemental-spell-effects` ($12.75), `mega-pack-elemental-spell-effects-02` ($20.40). Note: the two mega-packs aggregate over already-curated constituent packs, so their effective resolution_band is "mixed" by definition; visual inspection of the bundle is moot if constituents are inspected.
- **1 inherited row** (`earth-spell-effect-03::enemy-elemental` sister via category split).

### Visual-inspection queue disposition — Option (b) — QUEUED for later step

Per dispatch Step 2: I chose **option (b)** — file the 20 unknown rows as a sub-list and queue them for a later inspection step. Rationale:

1. The visual-inspection workflow per structural-review Flag 5 specifies **post-acquisition** inspection. Pre-acquisition inspection from itch.io preview images alone produces partial data (palette and shading are inspectable from preview gifs; linework requires frame access).
2. A purchase decision is itself part of the inspection step (the 4 paid rows in this list intersect with cost-coverage analysis Matt drives).
3. I lack a browser-rendering integration that would let me reliably read preview images at this curation pass.

**The 21 queued rows (in catalogue.db with `manual_review_queued = 1`):**

| asset_id | cost | derived_register | category | priority |
|---|---:|---|---|---|
| `fire-spell` | $0 | manual-review | vfx | medium (free; sub-register-uncertain) |
| `fire-spell-effect-02` | $0 | manual-review | vfx | medium |
| `magical-water-effect` | $0 | manual-review | vfx | medium |
| `water-spell-effect-02` | $0 | manual-review | vfx | medium |
| `ice-spell-effect-01` | $0 | manual-review | vfx | medium |
| `earth-spell-effect-01` | $0 | manual-review | vfx | medium |
| `earth-spell-effect-2` | $0 | manual-review | vfx | medium |
| `earth-spell-effect-03` | $3 | hand-drawn-pixel | vfx | **HIGH** (paid; positive tag but uncertain rb) |
| `wind` | $0 | manual-review | vfx | medium |
| `wind-spell-effect` | $0 | manual-review | vfx | medium |
| `thunder-spell-effect-01` | $0 | manual-review | vfx | medium |
| `thunder-spell-effect-02` | $0 | manual-review | vfx | medium |
| `thunder-spell-effect-03` | $3 | hand-drawn-pixel | vfx | **HIGH** (paid) |
| `fantasy-platformer-character` | $0 | manual-review | character | medium (only character asset queued) |
| `mega-pack-elemental-spell-effects` | $12.75 | hand-drawn-pixel | vfx | LOW (aggregated; per-constituent inspection covers it) |
| `mega-pack-elemental-spell-effects-02` | $20.40 | hand-drawn-pixel | vfx | LOW (same reason) |
| `smoke-vfx-1` | $0 | manual-review | vfx | medium |
| `halloween-special-effects` | $0 | manual-review | vfx | medium |
| `cutting-and-healing` | $0 | manual-review | vfx | medium (CC-BY 4.0; attribution-required) |
| `magical-animation-effects` | $0 | manual-review | vfx | medium |
| `earth-spell-effect-03::enemy-elemental` | $3 (shared) | hand-drawn-pixel | enemy | **HIGH** (paid; only enemy in queue) |

**Workflow for queue drain (when convenient):**

1. Open vendor preview pages for each queued row (use stored `source_url`).
2. Inspect preview gifs / sprite sheets to backfill `resolution_band` (and ideally axes 2-4).
3. Update the row in catalogue.db via the curation-pipeline UPDATE pattern (or via a new "manual-review-resolved" pass that supersedes the row per the audit-trail discipline).
4. Re-run R5 derivation if resolution_band changes; promote to `derived_register = 'hand-drawn-pixel'` (or `retro-16bit`) as appropriate; clear `manual_review_queued`; update `quality_flag` to `pass`/`borderline`/`fail`.

This is **NOT** scheduled as a dispatch yet — defer to knight-rider sequencing or Matt's acquisition-decision moment (whichever happens first).

---

## 3. CC-BY 4.0 attribution tagging

**Identified rows** (matched against dispatch Step 3 + confirmed against raw `license = 'CC-BY'`):

1. `pixel-battle-effects` — `Battle Effects` (free; CC-BY 4.0)
2. `cutting-and-healing` — `Cutting and Healing` (free; CC-BY 4.0)

**Per-row treatment** (schema-compatible — no schema rework):

- `license` column = `'CC-BY'` (already in raw extraction)
- `source_metadata_raw._curation_overlay_2026_05_16.curation_attribution` =
  ```json
  {
    "attribution_required": true,
    "license_specifics": "CC-BY-4.0; credit creator (Pimen) + link to original work",
    "attribution_acquired_yet": false
  }
  ```
- Queryable tags emitted to `asset_style_tags`:
  - `attribution-required`
  - `attribution-acquired-yet:false`
  - `license-specifics:cc-by-4.0`

**Other 45 rows** have `license = 'commercial-royalty-free'` → no attribution required.

**Drax-side query pattern** for the CC-BY footer integration:

```sql
SELECT a.source_asset_id, a.name, a.source_url
FROM catalogue_assets a
JOIN asset_style_tags t ON t.asset_uid = a.asset_uid
WHERE t.tag = 'attribution-required'
  AND a.superseded_at IS NULL;
```

When an attribution is acquired in the loadout/demo footer, drax updates the curated row by replacing `attribution-acquired-yet:false` tag with `attribution-acquired-yet:true` (or via a curated MIGRATION.md note + new catalogue revision).

---

## 4. Bundle membership normalization

**Implementation choice:** **external JSON file + inline `in-bundle:<bundle_id>` tags** (both, for redundancy and queryability).

**External file:** `agentic_orchestration/research/curated/pimen-bundle-relationships-2026-05-16.json`. Schema:

```json
{
  "schema_version": "1.0",
  "produced_by": "...",
  "produced_at": "...",
  "source": "itch-pimen",
  "crawl_session_id": "...",
  "bundles": [
    {
      "bundle_id": "<asset_id-of-the-mega-pack>",
      "constituents": ["<constituent asset_id>", ...],
      "notes": "<optional version-drift / overlap notes>"
    }
  ]
}
```

**Bundles registered:**

### Bundle 1: `mega-pack-elemental-spell-effects` ($12.75 — sale-price)

9 constituents, identified from extraction_notes ("Bundle of 9 element packs: Thunder, Fire, Water, Earth, Wind, Dark, Holy, Ice, Smoke"):

1. `fire-spell-effect-3` (paid $3)
2. `water-spell-effect-03` (paid $3)
3. `earth-spell-effect-03` (paid $3) — also category-split (see § 5)
4. `wind-spell-effect-03` (paid $3)
5. `thunder-spell-effect-03` (paid $3)
6. `dark-spell-effect` (paid $4.99)
7. `holy-spell-effect` (paid $4.99)
8. `ice-spell-effect-02` (paid $4.99)
9. `smoke-effect-02` (paid $4.24)

**Sum of constituent prices:** $34.21. Bundle sale price $12.75 = **63% discount**; base price $15 = 56% discount. Matt's cost-coverage decision: mega-pack-01 is materially cheaper than constituents-individually for full-element-rotation coverage.

### Bundle 2: `mega-pack-elemental-spell-effects-02` ($20.40 — sale-price)

5 constituents, identified from extraction_notes ("Bundle of 5 element packs: Ice, Holy, Dark, Acid, Wood"):

1. `ice-spell-effect-02` (paid $4.99) — **overlaps with bundle 1**; version-drift surfaced
2. `holy-spell-effect` (paid $4.99) — **overlaps with bundle 1**; version-drift surfaced
3. `dark-spell-effect` (paid $4.99) — **overlaps with bundle 1**; version-drift surfaced
4. `acid-spell-effect` (paid $4.99)
5. `wood-spell-effect` (paid $4.99)

**Sum of constituent prices:** $24.95. Bundle sale price $20.40 = 18% discount; base price $24 = 0% discount. Less compelling than bundle 1.

**Version-drift caveat** (from extraction_notes on mega-02): "bundle lists holy=10 and dark=10, but individual pack pages show holy=12 and dark=12 — bundle listing may approximate, or bundle includes slightly different version than individual packs." Treat as a curation-pipeline finding: **on acquisition, verify which version of Ice/Holy/Dark is actually delivered in each bundle**. Recorded in bundle file's `notes` field.

### Queryable tags emitted

Each constituent row has `asset_style_tags.tag = 'in-bundle:<bundle_id>'`. 14 total tag rows (9 + 5; 3 constituents are in both bundles → each gets two tags, since asset_style_tags uniqueness is on `(asset_uid, tag)` not `(asset_uid, tag_prefix)`).

Drax-side cost-coverage query example:

```sql
-- Constituents covered by buying mega-pack-01
SELECT a.source_asset_id, a.cost_usd
FROM catalogue_assets a
JOIN asset_style_tags t ON t.asset_uid = a.asset_uid
WHERE t.tag = 'in-bundle:mega-pack-elemental-spell-effects'
  AND a.superseded_at IS NULL;
```

---

## 5. Category split — `earth-spell-effect-03`

**Rationale:** Per dispatch Step 5 + structural-review Flag 4, packs that cross the `category` enum boundary (VFX + enemy) emit multiple catalogue_assets rows, distinguished by suffixed `source_asset_id`.

**Earth Spell Effect 03** bundles spell VFX + Earth Elemental enemy character (6 animation cycles per extraction_notes). Treatment: **split into 2 rows**, share `pack_id`.

| asset_id | category | decomposition | embodiment_tag | quality_flag | mrq |
|---|---|---|---|---|---:|
| `earth-spell-effect-03` | vfx | unknown | not-applicable | unreviewed | 1 |
| `earth-spell-effect-03::enemy-elemental` | enemy | monolithic | pending-amendment | unreviewed | 1 |

Both rows share `pack_id` (via the new pack `earth-spell-effect-03` in `catalogue_packs`). Cross-link tags:
- vfx row: `category-split-role:vfx-pack-half`, `bundled-with:earth-spell-effect-03::enemy-elemental`
- enemy row: `category-split-from:earth-spell-effect-03`, `category-split-role:enemy-character-half`, `bundled-with:earth-spell-effect-03`

**Embodiment caveat on the sister row:** Earth Elemental is an "elemental humanoid" — closest v1.0 starter embodiment match is `construct`, but the form is genuinely between humanoid and construct in the embodiment-narrative-layer's vocabulary. Per the **dispatch-disallowed narrative-layer amendment protocol** (gandalf owns), the row is tagged `embodiment_tag = 'pending-amendment'` with `pending_amendment_hint = 'elemental humanoid form (Earth Elemental in earth-spell-effect-03)'`. Accumulating elemental hints across future crawls (other vendors will ship elementals) will pressure gandalf to either (a) absorb elementals into `construct`, (b) add a new starter `elemental`, or (c) leave them ambiguous. This is the canonical workflow per `embodiment-narrative-layer.md` and the catalogue-rubric § 9 Topic 4 outcome.

**No other category-mixed packs identified in the full crawl.** The structural-review-flagged mega-pack-elemental-spell-effects "bundles UI elemental icons" hypothesis is NOT confirmed in the full-crawl extraction — the mega-pack's tags do not include `'ui'` or `'icon'`. Per extraction_notes: "Elemental icons also included" (in addition to vfx). I treat this as an aside — the bundle's primary content is vfx; the icons are bonus. No split applied. If drax later finds UI consumption needs surface them, propose a v1.x curation-pipeline pass to split.

---

## 6. Decisions made on uncertain rows

| Row | Uncertainty | Decision | Rationale |
|---|---|---|---|
| `fantasy-skeleton-enemies` | No register-signal tag in style_tags; rb=hd2d-pixel | derived_register = `hand-drawn-pixel` via vendor-hint inference; `quality_flag = borderline` | Pimen's vendor-register hint is hand-drawn-pixel; resolution_band is positive; conservative `borderline` flag forces explicit eyeball pass before consumption |
| `fantasy-platformer-character` | No register-signal tag; rb=unknown | derived_register = `manual-review`; `quality_flag = deferred`; `manual_review_queued = 1` | Insufficient evidence in raw data; only character asset queued for visual inspection |
| `cutting-and-healing` | Has 'retro' tag but rb=unknown | derived_register = `manual-review` (cascade rule 2 only fires when rb ∈ {tiny, retro}) | Conservative — the retro tag is suggestive but the unknown rb means the asset could be retro OR small-canvas hand-drawn. Visual inspection will resolve. |
| `earth-spell-effect-03` (vfx half) | Has 'hand-drawn-pixel' tag (positive) but rb=unknown | derived_register = `hand-drawn-pixel`; `quality_flag = unreviewed` + `manual_review_queued = 1` | Positive tag wins under cascade; visual-inspection flag preserves the upfront uncertainty signal |
| `earth-spell-effect-03::enemy-elemental` | embodiment is elemental (between humanoid/construct) | `embodiment_tag = 'pending-amendment'` + hint | Per narrative-layer amendment protocol; let pattern accumulate before forcing canonical assignment |
| `mega-pack-elemental-spell-effects` (rb=unknown, positive tag) | Aggregate over 9 constituents | derived_register = `hand-drawn-pixel`; `manual_review_queued = 1` (but priority=LOW per § 2 rule 4) | Bundle inherits positive tag; constituent inspection covers the visual-inspection load |
| `mega-pack-elemental-spell-effects-02` (rb=unknown, positive tag) | Aggregate over 5 constituents; version-drift caveat | Same as bundle-01 | Verify version drift at acquisition |

---

## 7. Pipeline rules NOT applied (deferred)

1. **R6 outline-profile secondary tag.** Cannot fire automatically because `linework_style` is universally `unknown`. To be back-filled during the post-acquisition visual-inspection step (structural-review Flag 5). Hand-drawn-pixel rows currently lack `outline-profile:hard-1px` vs `outline-profile:soft-or-variable` tags — **drax cannot constrain scene-coherence by outline-profile yet for any Pimen asset.** Flagged for downstream awareness.
2. **R7 boundary-cluster `quality_flag = borderline`.** No row triggers R7 in this corpus (no row has `palette_size = restricted` AND `shading_technique = dithered` AND `linework_style = hard-1px-outline` simultaneously, because palette/shading/linework are universally `unknown`). R7 will become relevant only when post-acquisition inspection fills axes 2-4 for some rows.
3. **Pivot-insurance ledger update.** Per `curation-pipeline.md` § 7.1, the ledger receives a per-pass summary. **Deferred** to a separate follow-on commit (the ledger file is a stub at the moment; ledger-format finalization deferred to first multi-vendor curation pass). Pimen-only data is not yet pivot-meaningful — the ledger is more interesting once a second register's vendor (e.g., a `retro-16bit` source) lands.
4. **`manual-review-queue.md` update.** Per `curation-pipeline.md` § 7.2, separate file. **Deferred** for the same reason as #3 — file doesn't exist yet; the 21 queued rows are visible via `WHERE manual_review_queued = 1` in catalogue.db.
5. **`pipeline-runs.md` update.** Per `curation-pipeline.md` § 7.3, separate file. This curation log doubles as the pipeline-run record for this pass. A standing pipeline-runs.md is deferred to the first multi-pass curation cycle.

---

## 8. Schema integrity verification

```
$ sqlite3 catalogue.db "SELECT version FROM schema_meta;"
1.0

$ sqlite3 catalogue.db "SELECT
    'sources' AS t, COUNT(*) FROM catalogue_sources UNION ALL
    SELECT 'sessions', COUNT(*) FROM crawl_sessions UNION ALL
    SELECT 'packs', COUNT(*) FROM catalogue_packs UNION ALL
    SELECT 'assets', COUNT(*) FROM catalogue_assets UNION ALL
    SELECT 'tags', COUNT(*) FROM asset_style_tags;"
sources|1
sessions|1
packs|3
assets|47
tags|444
```

**No CHECK-constraint failures during ingest.** All 47 rows passed every enum (license, decomposition, derived_register, embodiment_tag, file_format, quality_flag, etc.) and FK (source, crawl_session_id, pack_id) constraint. Schema v1.0 holds under empirical 47-row pressure — first end-to-end live application.

---

## 9. Acceptance-criteria checklist (dispatch § Acceptance)

- [x] All four pre-processor rules applied across 46 rows (rules R5-derivation, pimen_element migration, file_format parse, requires_visual_inspection flag)
- [x] 20 unknown-resolution rows flagged + queued (Option (b) — sub-list at § 2.4 with priority guidance)
- [x] CC-BY 4.0 attribution tracking applied (2 rows tagged per § 3)
- [x] Bundle relationships normalized (external JSON file + queryable tags per § 4)
- [x] Category-mixed pack (`earth-spell-effect-03`) handled (split per § 5)
- [x] Curated output at `research/curated/pimen-catalogue-curated-2026-05-16.jsonl` (47 rows)
- [x] Curation log at `research/curated/pimen-curation-log-2026-05-16.md` (this file)
- [x] `catalogue.db` ingested and verified (47 assets, 444 tags, 3 packs)
- [x] Knight-rider notified at completion (see dispatch Completion section + AGENT_STATE update)

---

## 10. Notes for knight-rider

**Schema state:** v1.0 lock holds. No schema rework done. Per dispatch § "What this dispatch DOES NOT do", schema gaps would be filed as a v1.1 proposal — none were found.

**Hand-off readiness:**
- **Drax** can now query the catalogue for Pimen-side consumption via the patterns in `catalogue-schema.md` § 5. Note the outline-profile coverage gap (§ 7 item 1) — scene-coherence constraint cannot yet be applied to Pimen rows.
- **Star-lord** unaffected (no engine telemetry change).
- **Gandalf** can run viability-gate design-track queries on the catalogue if a Pimen-specific design moment arises; the gate already passed at the sample level so this is just for ongoing reads.
- **Rocket** unaffected.
- **Legolas** has a clean sample to validate Mode B output format against the curation pipeline's parser expectations — this curation pass surfaces 0 extraction errors, suggesting Legolas's Pimen extraction is the right shape for downstream consumption.

**Open follow-ons (NOT in scope of this dispatch):**

1. **Visual-inspection queue drain** — 21 rows queued; no dispatch yet. Can be paired with Matt's acquisition decision if/when that happens.
2. **Curation-pipeline implementation** — this curation pass is one-shot for Pimen. A generalized `curate_catalogue.py` per `curation-pipeline.md` § 10 is still deferred; future vendor crawls (CraftPix, CreativeKind) would benefit from generalizing the four pre-processor rules into the standing pipeline.
3. **Pivot-insurance ledger format finalization** — deferred until second-register vendor lands.
4. **Post-acquisition visual inspection workflow** — when Matt acquires any Pimen pack, the curator-side process per structural-review Flag 5 (backfill axes 2-4 + verify resolution_band) needs to run. Can be a single-batch session per pack, ~2 min per asset.
5. **`embodiment-narrative-layer.md` cross-reference for `elemental` form** — surfaced via the earth-spell-effect-03 sister. Gandalf-owned doc; pressure low (one row) but accumulates.

---

## Appendix A — Curation script provenance

Script: `agentic_orchestration/research/scripts/curate_pimen_full_2026_05_16.py`. One-shot tool, ~470 lines, no external dependencies (stdlib only).

The script is **idempotent on a clean catalogue.db** (the curation runs once; re-runs require manual `DELETE FROM catalogue_assets WHERE crawl_session_id = '...'` first to clear the prior insert). A generalized pipeline would add session-aware re-curation; this one doesn't, by design.

**Reproducibility:** the curated output `.jsonl` can be regenerated from `full-2026-05-16.jsonl` by re-running the script — modulo the `_curated_at` timestamp which advances per run.

---

— elrond, 2026-05-16, post-curation
