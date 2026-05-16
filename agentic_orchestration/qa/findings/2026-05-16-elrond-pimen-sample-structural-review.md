# Finding — 2026-05-16 — elrond structural-track Pimen sample review

**Reviewer:** elrond
**Severity:** **PASS WITH FLAGS**
**Target:** Legolas Pimen Mode-B sample (`research/catalogue/pimen/sample-2026-05-16.json` — 20 rows, ~30 KB)
**Track:** structural (viability-gate of three)
**Cross-track context:** drax wiring-track = PASS WITH FLAGS; gandalf design-track = PASS (both filed earlier 2026-05-16)

## Verdict (one line)

The Pimen sample fits the v1.0 catalogue schema cleanly — empirically validated by representative-row insertion — with no blocking schema mismatches; the four operational flags below describe **curation-pipeline pre-processor rules** that need to land before live curation begins, not schema rework.

---

## Per-criterion assessment

### 1. Metadata completeness

| Field | Coverage in sample | Adequate at full-crawl scale? |
|---|---|---|
| Identity (`asset_id`, `source`, `url`, `name`, `crawl_date`) | 20/20 populated | ✓ Yes |
| `category` (vfx / enemy / character) | 20/20 populated; all values map to my schema enum | ✓ Yes |
| `dimensionality` | 20/20 = `2d` | ✓ Yes |
| `license` | 20/20 = `commercial-royalty-free` | ✓ Yes (exact match to enum) |
| `cost` (USD float) | 20/20 populated (range $0–$12.75) | ✓ Yes |
| `decomposition` | 17 `not-applicable` (vfx) + 2 `monolithic` (skeleton, character) + 1 `unknown` (earth-spell-effect-03 with embedded character) | ✓ Yes — three values used; all map to schema enum |
| `style_register` (parent) | 20/20 = `pixel-art` | ⚠ See flag 2 — `pixel-art` is parent; not in my axis-6 enum |
| `style_tags` (variable list) | 20/20 populated; multiple tags per row | ✓ Yes — maps to `asset_style_tags` table |
| `resolution_band` | 11/20 = `hd2d-pixel` (derivable from vendor canvas-size notes); 9/20 = `unknown` | ◐ Partial — half-derivable from metadata, half needs post-acquisition visual inspection |
| `palette_size` | 0/20 derivable | ✗ Universal gap — requires frame inspection |
| `shading_technique` | 0/20 derivable | ✗ Universal gap — requires frame inspection |
| `linework_style` | 0/20 derivable | ✗ Universal gap — requires frame inspection |
| `animation_frame_density` | 19/20 populated (5 values used: low/mid/high/cinematic/unknown) + 1 `unknown` | ✓ Yes — all values map to schema enum |
| `pimen_element` | 14 with element name + 3 null (character/skeleton/buff/hit-spark) + 1 `multi` (mega pack) | ⚠ See flag 3 — vendor-specific field with no direct schema home |
| `animations_count`, `frame_count_notes`, `canvas_size_notes`, `extraction_notes` | 20/20 populated | ✓ All preservable via `source_metadata_raw` JSON blob |

**Net assessment:** the **vendor-side fields** are all populated and operationally tolerable. The **rubric-axis fields** are universally underpopulated for 3 of 6 axes (palette/shading/linework) — this is the major operational signal, not a Pimen-specific failure. **Pimen cannot supply palette/shading/linework metadata without frame access; no vendor will.** The resolution path is post-acquisition curator inspection (see flag 5).

### 2. Schema-fit

**Empirically tested.** I ran three representative-row inserts against the empty `catalogue.db` (then cleared) — all three succeeded after curator-side transformations documented in flags 1 + 3:

| Test row | Outcome | Note |
|---|---|---|
| `fire-spell-effect-3` (paid VFX, rubric-derivable case, `hd2d-pixel` + `hand-drawn-pixel` sub-register tag → `derived_register = 'hand-drawn-pixel'`) | ✓ INSERT OK | Clean case; rubric R5 derivation succeeded |
| `fantasy-skeleton-enemies` (free enemy, monolithic decomposition, `embodiment_tag = 'humanoid'` for skeletons) | ✓ INSERT OK | Embodiment tag landed on the first character-bearing Pimen asset |
| `fire-spell` (free VFX, all rubric axes `unknown`, `sub-register-uncertain` → `derived_register = 'manual-review'` + `manual_review_queued = 1`) | ✓ INSERT OK | Manual-review queue absorbs the ambiguous case as designed |
| Plus 5 `asset_style_tags` rows | ✓ INSERT OK | Multi-tag-per-asset works |

**Counter-tests (negative cases — should fail per schema CHECK constraints):**

| Counter-test | Outcome | Confirms |
|---|---|---|
| INSERT with raw Pimen `file_format = 'PNG, RAR archive (11 kB)'` | ✗ REJECTED (CHECK failed) | drax wiring-track Flag 1 resolution holds — curator-side parse required |
| INSERT with `derived_register = 'pixel-art'` (Pimen parent value) | ✗ REJECTED (CHECK failed) | rubric R5 enum disciplines the closed value set; pixel-art must derive to one of the six |

Both counter-tests fail with explicit CHECK errors — the schema's defenses behave as designed. No schema gymnastics needed for the positive case; the negative case forces curator-pipeline parse logic.

### 3. License clarity

**Clean.** All 20 rows are `commercial-royalty-free`, which exactly matches one of the 12 values in the `license` enum (added in v1.0 per gandalf-dialogue Topic 5). No mapping ambiguity, no edge cases. Pimen's actual itch.io license text aligns with the canonical reading of `commercial-royalty-free` (purchase or NWYP unlocks unlimited commercial use without per-project terms).

Sample is well below the 20%-`unknown`-license threshold gandalf set in MIGRATION.md v1.0 entry (0% `unknown` here).

### 4. Decomposition signal coherence

**Mostly coherent; one schema-question case surfaces.** Three values seen across 20 rows:

| Value | Rows | Sample basis |
|---|---|---|
| `not-applicable` | 17 (all pure VFX) | Schema enum supports it; semantic match (VFX cannot be "decomposed into parts" in a sprite-rigging sense) |
| `monolithic` | 2 (Skeleton Enemies, Fantasy Platformer Character) | Schema enum supports it; expected for pimen's character/enemy work |
| `unknown` | 1 (`earth-spell-effect-03`) | The pack is primarily VFX (`category: vfx`) but bundles a complete Earth Elemental enemy sprite. The `decomposition: unknown` reflects that the character's structure isn't documented. |

**Edge case for curation policy:** the `earth-spell-effect-03` pack is *category-conflated* — primarily VFX but contains an enemy sprite. Drax flagged this in his wiring review; gandalf also surfaced it. From the structural side, **the schema can handle this two ways**:

- **Option A:** single row with `category = 'vfx'` (primary) + `embodiment_tag = 'humanoid'` for the bundled-character signal — but then the row is queryable as VFX, not as enemy
- **Option B:** **TWO rows** with same `source_asset_id` distinguishable by an additional curator suffix (`earth-spell-effect-03::vfx-pack` + `earth-spell-effect-03::enemy-elemental`) — preserves queryability across both axes

I recommend option B as a curation-pipeline rule: when a vendor pack contains assets across multiple `category` values (vfx + enemy + ui in the Mega Pack case), split into multiple `catalogue_assets` rows linked via the same `pack_id`. The `catalogue_packs` table already supports this — packs and assets are 1:N.

### 5. Style-register inferability + resolution path

**This is the load-bearing operational question for Pimen and any vendor that doesn't host browsable frames.** Three layers:

| Axis | Coverage in Pimen sample | Resolution path |
|---|---|---|
| `resolution_band` | 11/20 derivable (vendor canvas-size notes) | Curator parses `canvas_size_notes` field at curation time — pipeline rule |
| `animation_frame_density` | 19/20 derivable (vendor metadata + Legolas inference) | No path change needed |
| `palette_size` | 0/20 derivable from vendor metadata | Post-acquisition visual inspection only |
| `shading_technique` | 0/20 derivable | Post-acquisition visual inspection only |
| `linework_style` | 0/20 derivable | Post-acquisition visual inspection only |
| `derived_register` (axis 6) | Inferable from style_tags `hand-drawn-pixel` (14/20) or `sub-register-uncertain` (6/20) | Curator rule: `hand-drawn-pixel` tag → `hand-drawn-pixel`; `sub-register-uncertain` → `manual-review` + queue |

**Recommended operational workflow** (Pimen-derived, generalizes to other VFX-only vendors):

1. **At curation time** (no purchase): set rubric axes 1, 5 from vendor metadata where present (Pimen has 55% / 95% respectively); set palette/shading/linework to `unknown`; derive axis 6 from sub-register tags (else `manual-review`).
2. **At post-purchase visual-inspection time** (curator opens downloaded assets in image viewer / Aseprite): backfill palette/shading/linework from observation; finalize `derived_register`; clear `manual_review_queued` flag.
3. **At consumption time** (Drax filter query): consumers requesting strict-coherence scenes (per the outline-profile constraint in `catalogue-rubric-schema.md` § 3.1) filter on `quality_flag = 'pass'` to skip rows still in the deferred/manual-review queue.

This is **NOT** a schema rework — the schema already supports all three states (`unknown` enum values exist; `manual_review_queued` boolean exists; `quality_flag` enum with `deferred` value exists). It is a **curation-pipeline operational discipline**.

For full-crawl scale (Pimen has ~50+ packs total, per Legolas's broader vendor knowledge), the per-asset post-acquisition inspection cost is the binding scaling constraint, not the schema. Estimating ~2 min per asset for the three-axis visual check × 100 assets = ~3 hours of curator-attention to bring axes to full coverage. Acceptable for a high-value primary vendor.

---

## Schema or pipeline refinements recommended

### Flag 1 (pipeline) — `file_format` curator-side parse rule

Pimen ships `file_format` as prose ("PNG, RAR archive (11 kB)", "PNG spritesheet + individual frames", "PNG, individual frames, RAR archive (49 kB)"). The schema CHECK constraint enforces a closed enum; raw values are rejected (verified). Curation pipeline needs a parser:

| Pimen prose pattern | Map to schema enum |
|---|---|
| Contains `spritesheet` | `png-spritesheet` |
| Contains `aseprite` | `aseprite` |
| Contains `PNG` + `individual frames` (no spritesheet) | `png` (single-frame-archive convention) |
| Plain `PNG` | `png` |
| Otherwise | `unknown` (flag for manual review) |

Affects: 20/20 sample rows. Trivial parser (15-line Python). Lands in `curate_catalogue.py` when implemented.

### Flag 2 (pipeline) — `style_register: "pixel-art"` is parent; rubric R6 derivation rule

Pimen ships `style_register: "pixel-art"` (one value, 20/20 rows). The catalogue's `derived_register` enum has no `pixel-art` value — `pixel-art` is the parent category. Curator-side mapping:

```
IF style_tags contains "sub-register-uncertain"
    → derived_register = 'manual-review'
       derived_register_source = 'manual-review-resolved' (will be when queue is drained)
       manual_review_queued = 1
       quality_flag = 'deferred'
ELSE IF style_tags contains "hand-drawn-pixel"
    → derived_register = 'hand-drawn-pixel'
       derived_register_source = 'rule'
       quality_flag = 'unreviewed' (until manual pass)
ELSE IF style_tags contains "16-bit-tagged" AND resolution_band IN ('tiny', 'retro')
    → derived_register = 'retro-16bit'
       derived_register_source = 'rule'
ELSE
    → derived_register = 'manual-review' (default conservative)
       manual_review_queued = 1
```

Affects: 20/20 sample rows. 14 land cleanly on `hand-drawn-pixel`; 6 land in `manual-review` queue. Rule is a 10-line Python function.

### Flag 3 (pipeline) — `pimen_element` → asset_style_tag convention

Vendor-specific element tag (`pimen_element: 'fire'|'water'|'ice'|...|'multi'|null`). No direct schema column — and rightly so; element-by-vendor is an emergent vendor-vocab, not a canonical axis. Recommended convention:

- Preserve raw in `source_metadata_raw` JSON blob (lossless)
- Emit a queryable tag: `asset_style_tags.tag = 'pimen-element:<value>'` (e.g., `pimen-element:fire`, `pimen-element:ice`, `pimen-element:multi`)
- Allows queries like `SELECT … WHERE tag LIKE 'pimen-element:%'` for vendor-element coverage analysis

Generalizes naturally to other vendors (`creativekind-element:`, `foozle-element:` etc.) when those crawls land. The `asset_style_tags.tag` column is free-text by design (no CHECK constraint) to admit this growing namespace.

### Flag 4 (pipeline) — multi-category packs split into multiple `catalogue_assets` rows

Two sample rows are multi-category:

- `earth-spell-effect-03` — primarily `vfx` but bundles Earth Elemental enemy (also flagged by drax + gandalf)
- `mega-pack-elemental-spell-effects` — primarily `vfx` but bundles UI elemental icons

Recommended curator rule: when a pack contains assets crossing the `category` enum boundary, emit **multiple `catalogue_assets` rows** with the same `pack_id` and distinct `source_asset_id` suffix (`earth-spell-effect-03::vfx-pack`, `earth-spell-effect-03::enemy-elemental`). Preserves per-category queryability; preserves pack-level grouping via `catalogue_packs`.

Affects: 2/20 sample rows. Pipeline rule (small switch in `curate_catalogue.py`).

### Flag 5 (operational, not schema) — post-acquisition visual-inspection workflow

For axes 2/3/4 (palette/shading/linework), no vendor metadata can supply values. The curator must inspect downloaded frames. Establish operational workflow:

1. Post-purchase: curator downloads pack, opens representative frames in image viewer / Aseprite
2. Updates `palette_size`, `shading_technique`, `linework_style` from `unknown` → observed value
3. Re-derives `derived_register` if previously `manual-review`
4. Clears `manual_review_queued`; updates `quality_flag` to `pass`/`borderline`/`fail`
5. Tracks per-batch via `crawl_sessions.curated_at` timestamp

**Cost estimate at scale:** ~2 min per asset × full-crawl size (Pimen ~50-100 packs eventually). One curator-batch session per vendor-crawl. Acceptable; lands in `curation-pipeline.md` § operational-workflow section when next updated.

### Optional refinement (suggested by gandalf for me to consider) — `aseprite_available` boolean

Gandalf flagged that Mega Pack + Hit Spark + a few others ship Aseprite source files in addition to PNG, which materially changes Drax's wiring options (per-layer manipulation possible). Considered as a per-asset metadata field.

**My call: defer to `asset_style_tags`** rather than adding a schema column. Convention: `asset_style_tags.tag = 'has-aseprite-source'` (or `'no-aseprite-source'` explicitly when known absent). Queryable; doesn't add to STRICT-table column count; consistent with the score-don't-filter principle. Document in `curator-tagging-guide.md` at next update.

---

## What this unblocks (PASS WITH FLAGS)

Combined with drax (PASS WITH FLAGS) and gandalf (PASS), the three-track viability gate is **GREEN for Pimen full-crawl release** — knight-rider's call.

The four pipeline flags above are **pipeline-implementation work**, not schema rework. They land naturally in the `curate_catalogue.py` implementation (currently deferred per AGENT_STATE "next session pick-up" until Pimen sample arrives — which it now has). Ordering:

1. Knight-rider releases Pimen full crawl to Legolas (~50-100 assets expected; per current Mode-B spec)
2. Legolas crawls, files raw output to `research/catalogue/pimen/full-crawl-2026-05-NN.json`
3. **Then** elrond builds `curate_catalogue.py` with the pre-processor rules from flags 1, 2, 3, 4 baked in
4. Curation pipeline runs the full-crawl through; populates `catalogue.db` with v1.0 schema
5. Post-curation: curator-side visual-inspection pass per flag 5 to backfill palette/shading/linework

Alternative ordering (pipeline-before-crawl): elrond builds `curate_catalogue.py` against the 20-row sample first, validates pipeline behavior, then Legolas-crawl + curation are mechanical. Knight-rider sequences.

---

## What this blocks (NEEDS REWORK)

**Nothing schema-side blocks.** Pipeline-implementation work (flags 1–4) is a 1-2 day deferred item in elrond's queue; it does not block sample acceptance or full-crawl release.

If knight-rider wants the four pipeline rules formalized in a doc before crawl release, that's a quick deliverable on my side — update `curation-pipeline.md` and `curator-tagging-guide.md` with the explicit rules. ~30 min.

---

## Cross-track concordance notes

Drax (wiring): PASS WITH FLAGS. His Cross-track notes mirror my flag 4 (category-conflation of `earth-spell-effect-03`). My structural read agrees and proposes the split-row resolution.

Gandalf (design): PASS. His Cross-track flags overlap with my flag 5 (sub-register classification gap, post-acquisition resolution path) and propose the optional `aseprite_available` enrichment which I address inline above.

No cross-track conflicts; all three tracks converge on operational pipeline rules, not schema or content rework. Knight-rider should be able to greenlight Pimen full crawl directly on the three verdicts.

---

## Schema-fit empirical evidence

Test inserts (then cleared to restore empty-DB state):

```
$ sqlite3 catalogue.db < /tmp/test_pimen_insert.sql
INSERTED|3
TAGS|5
1|Fire Spell Effect 03|vfx|hand-drawn-pixel|not-applicable|commercial-royalty-free
2|Fantasy Skeleton Enemies|enemy|hand-drawn-pixel|monolithic|commercial-royalty-free
3|Fire Spell Effect 01|vfx|manual-review|not-applicable|commercial-royalty-free
```

Counter-tests (negative cases, confirming CHECK enforcement):

```
$ -- Raw Pimen file_format string
$ INSERT ... file_format = 'PNG, RAR archive (11 kB)' ...
Error: stepping, CHECK constraint failed: file_format IN ('png', 'png-spritesheet', ...)

$ -- Pimen parent style_register passed through unchanged
$ INSERT ... derived_register = 'pixel-art' ...
Error: stepping, CHECK constraint failed: derived_register IN ('retro-16bit', 'hand-drawn-pixel', ...)
```

Post-test cleanup verified — `catalogue.db` returns to empty state matching the v1.0 schema-locked design:

```
$ sqlite3 catalogue.db "SELECT 'assets', COUNT(*) FROM catalogue_assets UNION ALL SELECT 'tags', COUNT(*) FROM asset_style_tags;"
assets|0
tags|0
```

---

**Reviewer:** elrond
**Date:** 2026-05-16
**Verdict file location:** `agentic_orchestration/qa/findings/2026-05-16-elrond-pimen-sample-structural-review.md`
