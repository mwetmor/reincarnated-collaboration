# Dispatch — 2026-05-16 — elrond — Pimen full-catalogue curation pass

**From:** knight-rider
**To:** elrond (data steward — Tier C+ within data architecture)
**Approved by:** Matt at 2026-05-16 Day 4 (after legolas full-crawl completion)
**Status:** COMPLETE
**Estimated effort:** 1-2 sessions (~3-5 hours; mix of structured pre-processor application + visual-inspection passes)
**Acceptance:** Curated catalogue ready for downstream consumption (engine pipeline + drax wiring); the four pre-processor rules applied; 20 unknown-resolution rows inspected; CC-BY 4.0 tagging cross-referenced; bundle membership normalized.

## Context — what just landed

Legolas's Mode B full Pimen crawl is COMPLETE: `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` — 46 distinct packs.

Top-line stats (from legolas's completion record):
- **44 VFX / 1 enemy / 1 character** — VFX-heavy catalogue
- **19 free / 27 paid** — paid majority (cost decisions downstream)
- **21 hd2d-pixel / 4 retro / 1 tiny / 20 unknown** — 20 rows need visual inspection
- **13 packs include Aseprite source** — per-layer-wiring capable subset
- **2 packs CC-BY 4.0** — attribution required if acquired (pixel-battle-effects, cutting-and-healing)

Notable structural surprises from legolas (worth your attention during curation):
1. **Buff/Debuff Pack 09 register outlier** — 24×24 canvas vs 48-64px for packs 01-08. Likely retro register, not the locked HD-2D-shaped.
2. **Battle VFX Projectile in "tiny" band** — 12×12 canvas; delivered as ZIP not RAR.
3. **Earth Spell 03 bundles full Earth Elemental enemy character** alongside spell VFX (category-split needed during curation).
4. **20 rows unknown resolution_band** — free/early packs with no canvas-size documentation on itch.io pages.
5. **Buff/Debuff Pack 01 has NO Aseprite source** (packs 02-09 do).

This is the raw extraction. Your job is the curation pass that turns it into something the engine pipeline and drax can consume cleanly.

## What to do

### Step 1 — Apply the four pre-processor rules

From your Pimen structural review (`agentic_orchestration/qa/findings/2026-05-16-elrond-pimen-sample-structural-review.md`), the four pre-processor rules:

1. **`pixel-art` parent value derives to specific sub-register via rubric R5.** Apply R5 to all 46 rows where `style_register: "pixel-art"`. Sub-registers should resolve to `hand-drawn-pixel` / `retro-pixel-art` / `tiny-pixel-art` / `unknown` per the rubric. Document which rows resolve cleanly and which are uncertain (those need visual inspection — see Step 2).
2. **`pimen_element` vendor-specific field maps to `source_metadata_raw` JSON blob.** Per your schema design, vendor-specific fields don't live in normalized columns. Migrate each row's `pimen_element` into a `source_metadata_raw` JSON object preserving the vendor signal without polluting the canonical schema.
3. **`file_format` raw string needs curator-side parse.** Strings like `"PNG, RAR archive (35 kB)"` or `"PNG spritesheet + individual frames + Aseprite source files"` need structured parsing into: `[primary_format, archive_format, archive_size_kb, has_spritesheet, has_individual_frames, has_aseprite_source]`. Apply uniformly to all 46 rows.
4. **Free-pack sub-register requires post-acquisition visual inspection.** Free packs are over-represented in the `unknown` resolution_band bucket. Flag them explicitly with a `requires_visual_inspection: true` field so the engine pipeline knows which catalogue entries are provisional vs confirmed.

These four rules collectively transform the raw legolas output into the curated-catalogue shape your schema expects.

### Step 2 — Visual-inspection pass on the 20 unknown-resolution rows

The 20 rows where `resolution_band: "unknown"` are blocking — they can't enter the engine's consumption-time filter without classification.

Approach options (pick the cleanest given your tooling):

- **(a)** Where the itch.io page has preview images, inspect them visually (open in browser; you have read-only web access via your scout integration if applicable; otherwise, surface these rows to legolas for an additional metadata pass — but that's a second crawl, expensive).
- **(b)** If image-inspection is genuinely not available to you, file the 20 unknown rows as a sub-list and queue them for a later inspection step (Matt or a fresh legolas Mode B sub-commission can handle).

For each inspected row, resolve `resolution_band` to one of: `hd2d-pixel` / `retro-pixel-art` / `tiny-pixel-art` / `narrative-pixel` (per your schema's rubric R1). Update the row in-place; document the change in a curation log.

### Step 3 — CC-BY 4.0 cross-reference tagging

Two rows require attribution if acquired:
- `pixel-battle-effects`
- `cutting-and-healing`

Add a structured field `attribution_required: true` on these rows + a `license_specifics: "CC-BY-4.0; credit creator name + link to original work"` field. Add a sibling field `attribution_acquired_yet: false` (toggled by drax when actually integrated into the loadout/demo). This gives drax a single field to query when deciding whether to extend the footer attribution list.

The other 44 packs are `commercial-royalty-free` per legolas — no attribution required; mark `attribution_required: false` uniformly.

### Step 4 — Bundle membership normalization

The mega-bundle (`mega-pack-elemental-spell-effects`) is a constituent of individual element packs. Build a normalized `bundle_membership` field linking child packs to parents:

```json
{
  "bundle_id": "mega-pack-elemental-spell-effects",
  "constituents": ["fire-spell", "water-spell-effect-...", ..., "thunder-spell-effect-..."]
}
```

Persist this as a separate `bundle_relationships` JSON file at `agentic_orchestration/research/curated/pimen-bundle-relationships-2026-05-16.json` OR as inline `parent_bundle` fields on constituent rows — your call on schema shape. Cost analysis downstream (Matt + you) needs to know: "if I buy the mega bundle, do I avoid buying any constituents?"

### Step 5 — Category split: Earth Spell 03 (and any other category-mixed packs)

Earth Spell 03 bundles spell VFX + an enemy character (Earth Elemental, 6 animation cycles). The current row has `category: "vfx"` (primary). For curation:

- Add a `includes_sub_assets` field listing the embedded enemy character as a separate logical asset
- Decide whether to split this row into two catalogue entries OR keep as one with sub-asset metadata
- Apply same treatment to any other rows legolas flagged with the `includes-enemy-character` or `includes-character` style_tag

Document the choice and apply uniformly.

### Step 6 — Output

The curated catalogue goes to: `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl`

Accompany with:
- `pimen-curation-log-2026-05-16.md` — what changed, per-row deltas, decisions made on uncertain rows
- `pimen-bundle-relationships-2026-05-16.json` (if you chose external file approach for Step 4)

Update `catalogue.db` (your v1.0 schema) by ingesting the curated catalogue. Verify row counts post-ingest.

## What this dispatch DOES NOT do

- **Acquisition decisions.** No "buy these packs" / "skip those." That's Matt's call once curation lands.
- **Cost/KPI analysis.** Once curation lands AND Matt makes acquisition decisions, you can do a follow-up cost-coverage KPI pass — but that's a separate dispatch.
- **Engine-pipeline integration.** Hooking the curated catalogue into the engine's per-season filter is rocket's seam, not yours. Coordinate via ADR-004 (MIGRATION.md) when ready.
- **Drax wiring.** The RAR-unpack / frame-assembly steps drax flagged are drax's seam, not yours. When drax begins implementing those steps, MIGRATION.md will be the coordination boundary.
- **Schema changes to `catalogue.db`.** If the curation surfaces a schema gap, file as a finding + propose a v1.1 schema increment. Do NOT modify the v1.0 schema in this dispatch.

## Required reading

- `agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl` (the raw crawl — your input)
- `agentic_orchestration/research/catalogue/pimen/sample-2026-05-16.json` (the prior sample for comparison)
- `agentic_orchestration/qa/findings/2026-05-16-elrond-pimen-sample-structural-review.md` (your own structural verdict + the four pre-processor rules)
- `agentic_orchestration/research/curated/catalogue-rubric-schema.md` (your six-axis rubric + R5 derived-sub-register rule)
- `agentic_orchestration/research/curated/catalogue-schema.md` (your v1.0 schema)
- `canonical/story/style-register.md` (gandalf's locked HD-2D-shaped register — for context; remember score-don't-filter)
- `agentic_orchestration/CHANGELOG.md` 2026-05-16 entries on viability gate + score-don't-filter

## Acceptance criteria

- [ ] All four pre-processor rules applied across 46 rows
- [ ] 20 unknown-resolution rows either inspected + classified OR flagged + queued
- [ ] CC-BY 4.0 attribution tracking applied (2 rows tagged)
- [ ] Bundle relationships normalized
- [ ] Category-mixed packs (Earth Spell 03 + any others) handled
- [ ] Curated output at `research/curated/pimen-catalogue-curated-2026-05-16.jsonl`
- [ ] Curation log at `research/curated/pimen-curation-log-2026-05-16.md`
- [ ] `catalogue.db` ingested and verified
- [ ] Knight-rider notified at completion: row counts, decisions on uncertain rows, readiness for downstream consumption

---

## Completion record

**Completed:** 2026-05-16 by elrond

**Output paths:**
- `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl` (47 rows; 46 raw + 1 from earth-spell-effect-03 category split)
- `agentic_orchestration/research/curated/pimen-bundle-relationships-2026-05-16.json` (2 bundles registered)
- `agentic_orchestration/research/curated/pimen-curation-log-2026-05-16.md` (full per-row decisions, queue disposition, schema verification)
- `agentic_orchestration/research/curated/MIGRATION.md` (v1.3 entry appended)
- `agentic_orchestration/research/scripts/curate_pimen_full_2026_05_16.py` (one-shot curation tool, ~470 lines)
- `agentic_orchestration/research/curated/catalogue.db` (ingested: 47 assets, 444 tags, 3 packs, 1 source, 1 session; schema v1.0 unchanged)

**Pre-processor rule applications:**
- **R5 derivation cascade** → 28 hand-drawn-pixel (27 positive-tag, 1 vendor-hint-inferred), 2 retro-16bit, 17 manual-review (15 sub-register-uncertain + 2 default-conservative `cutting-and-healing` + `fantasy-platformer-character`)
- **`pimen_element` → tag** → 23 rows tagged `pimen-element:<value>`; raw preserved in `source_metadata_raw`
- **`file_format` parser** → 25 `png-spritesheet` + 22 `png`; aseprite-negation guard correctly classifies 3 "No Aseprite files" rows as `has_aseprite_source = false`; final has-aseprite count = 13 (matches Legolas headline stat)
- **`requires_visual_inspection`** → 21 rows flagged (20 raw unknown-resolution + 1 inherited via split sister); `manual_review_queued = 1` in DB + queryable `requires-visual-inspection` tag

**Visual-inspection pass disposition:** Option (b) — 21 rows queued for later inspection step. Priority guidance per curation log § 2.4: 4 paid rows = HIGH, 1 split sister = HIGH (paid), 16 free rows = MEDIUM, 2 mega-packs = LOW (constituent-inspection covers). Deferred to knight-rider sequencing or Matt acquisition decision.

**Bundle relationships:**
- **mega-pack-elemental-spell-effects** ($12.75 sale, $15 base) — 9 constituents (Fire-03, Water-03, Earth-03, Wind-03, Thunder-03, Dark, Holy, Ice-02, Smoke-02); 63% discount vs sum-of-constituents ($34.21)
- **mega-pack-elemental-spell-effects-02** ($20.40 sale, $24 base) — 5 constituents (Ice-02, Holy, Dark, Acid, Wood); 18% discount; **3 overlaps with bundle-01** (Ice/Holy/Dark) with version-drift surfaced from extraction_notes (verify at acquisition)
- Persisted to external JSON file + inline `in-bundle:<bundle_id>` tags

**Category split:** earth-spell-effect-03 → 2 rows. VFX half + enemy half (`::enemy-elemental` suffix). Shared `pack_id`. Sister tagged `embodiment_tag = 'pending-amendment'` with hint `'elemental humanoid form'` (Earth Elemental). No other category-mixed packs identified.

**CC-BY 4.0 attribution:** 2 rows tagged (`pixel-battle-effects`, `cutting-and-healing`). `curation_attribution` overlay in `source_metadata_raw` + 3 queryable tags per row (`attribution-required`, `attribution-acquired-yet:false`, `license-specifics:cc-by-4.0`).

**Notes for knight-rider:**

1. **Schema lock holds.** v1.0 schema took the full-crawl load (47 rows, 444 tags, 3 packs, all CHECK constraints + FKs) with 0 errors. First end-to-end live application of the schema — empirical validation passed.

2. **Outline-profile coverage gap.** Drax's scene-coherence constraint (outline-profile:hard-1px vs soft-or-variable) CANNOT yet be applied to any Pimen row because `linework_style` is universally `unknown` until post-acquisition visual inspection. Worth a heads-up to drax. The 28 hand-drawn-pixel rows currently lack this secondary tag.

3. **Post-acquisition visual-inspection workflow** is the next operational step the catalogue needs to formalize. Per structural-review Flag 5: ~2 min per asset, backfills axes 2-4 + finalizes resolution_band + promotes `quality_flag` from `unreviewed`/`borderline` to `pass`. Single-batch session per acquired pack. No active dispatch — paired with Matt's acquisition moment.

4. **Curation-pipeline generalization deferred.** This pass is one-shot for Pimen. The four pre-processor rules will need lifting into a generalized `curate_catalogue.py` when the second vendor crawl lands (CraftPix or CreativeKind likely). ~1-2 days when needed.

5. **Pivot-insurance ledger** not updated this pass — single-vendor data is pivot-meaningless. Format finalization deferred until a second-register vendor (retro-16bit candidate) lands.

6. **Embodiment narrative-layer amendment pressure** — one row (`earth-spell-effect-03::enemy-elemental`) tagged `pending-amendment` with hint `'elemental humanoid form'`. Single-instance pressure is low; will accumulate as future vendors ship elementals. Gandalf-owned doc; no action needed yet.

7. **No engine-telemetry change.** ADR-004 satisfied via elrond-side MIGRATION.md v1.3 entry only. No cross-seam coordination required.

8. **Catalogue is now queryable.** Cross-store ATTACH pattern documented in `catalogue-schema.md` § 5 works against this data — drax/star-lord/gandalf can issue analytical queries today. Worked examples in catalogue-schema.md § 5.3 (drax consumption filter) and § 5.4 (register-pivot impact analysis) are exercisable on Pimen rows.

— elrond, 2026-05-16
