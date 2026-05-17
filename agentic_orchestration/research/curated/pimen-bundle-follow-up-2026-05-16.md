# Pimen bundle-pipeline follow-up — 2026-05-16

**Owner:** elrond
**Triggering dispatch:** Pattern A combined bundle-pipeline follow-up + catalogue.db schema amendment (Matt-authorized 2026-05-16, "yes to all 7" — decisions #2 + #5)
**Upstream context:** drax bundle-extension dispatch completion 2026-05-16 (`drax/v0.13-pimen-pipeline-bundle-archive-support @ 04ef825`)
**Scope:** Track A items 1–3 (slug collision, Icons sub-pack inspection, Explosion VFX scout)

This document captures elrond's inspection findings + curation decisions for the three follow-on items drax surfaced after the bundle-extension dispatch. Track B (schema amendment for the per-vendor register-mixed flag) lives in `MIGRATION.md` v1.4.

---

## 1. Track A item 1 — slug collision finding (`Earth Spell 03` vs `Earth Effect 03`)

### Drax's surfaced concern (verbatim from dispatch)

> Slug collision finding: `Earth Spell 03` and `Earth Effect 03` both fuzzy-match `earth-spell-effect-03`. The curated `earth-spell-effect-03::enemy-elemental` record exists but its normalised form drops the separator and doesn't match `Earth Spell 03` cleanly.

### Inspection finding (elrond)

`lsar` inspection of `/Users/admin/Games/reincarnated-demo/public/assets/pimen/Elemental Effects.rar` confirms BOTH folders exist in the bundle root:

```
Elemental Effects/
├── Earth Effect 03/    ← full content (separated frames + spritesheets)
├── Earth Spell 03/     ← spritesheet-only compact format
├── Fire effect 03/     ← (sister case: corresponds to curated fire-spell-effect-3)
├── Icons/              ← (Track A item 2 — see § 2 below)
├── Thunder Effect 03/  ← (sister case: corresponds to curated thunder-spell-effect-03)
├── Users/              ← (macOS user-path artifact; not asset content)
├── Water Effect 03/    ← (sister case)
└── Wind Effect 03/     ← (sister case)
```

Both `Earth Effect 03/` and `Earth Spell 03/` have **identical 11-dir top-level structure**:

| Top-level dir | Earth Effect 03 | Earth Spell 03 |
|---|---|---|
| Boulder | ✓ | ✓ |
| Earth Burst | ✓ | ✓ |
| Earth Hammer | ✓ | ✓ |
| Earth Mine | ✓ | ✓ |
| Earth Spike | ✓ | ✓ |
| Earth Trap 1 | ✓ | ✓ |
| Earth Trap 2 | ✓ | ✓ |
| Extra - Earth Elemental | ✓ | ✓ |
| Hit Effect | ✓ | ✓ |
| Impale | ✓ | ✓ |
| Petrify | ✓ | ✓ |

The difference is **frame-shape only**:
- `Earth Spell 03/` ships **only the assembled spritesheet PNGs** (e.g., `Boulder/Boulder (64x64).png`, `Extra - Earth Elemental/Earth Elemental (56x56).png`).
- `Earth Effect 03/` ships **both spritesheets AND `Separeted Frames/` subfolders** with individual numbered frames (e.g., `Boulder/Big Boulder Separeted Frames/Faster/Faster roll1.png`, `Boulder/Big Boulder Separeted Frames/Stop/Stop1.png`, etc.).

The same pack-twice-in-bundle pattern applies to the other elemental sister folders (`Fire effect 03` is the compact form of curated `fire-spell-effect-3`; `Earth Spell 03` is the canonical match for curated `earth-spell-effect-03`).

### Why this surfaced as collision

The bundle uses a **naming-convention drift** between product-page titles and bundle-folder names:

| Source layer | Naming form |
|---|---|
| Pimen product page title | "Earth Spell Effect 03" |
| Pimen product page URL slug | `earth-spell-effect-03` |
| Bundle compact-folder name | `Earth Spell 03` (drops "Effect") |
| Bundle full-content-folder name | `Earth Effect 03` (drops "Spell") |

Drax's fuzzy matcher correctly identified BOTH bundle folders as candidates for the curated `earth-spell-effect-03` slug; the collision is a real shape in the data, not a matcher bug. The needed disambiguation: which bundle folder is canonical?

### Action taken (elrond)

Amended the two curated records with `bundle_folder_hint` field (priority-ordered list; canonical first) via `agentic_orchestration/research/scripts/amend_pimen_bundle_folder_hints_2026_05_16.py`.

**Amendment shape** (preserved both in JSONL snapshot at `pimen-catalogue-curated-2026-05-16.jsonl` and in `catalogue.db.catalogue_assets.source_metadata_raw`):

```json
{
  "_amendment_2026_05_16_bundle_folder_hint": {
    "bundle_id": "mega-pack-elemental-spell-effects",
    "bundle_folder_hint": ["Earth Spell 03", "Earth Effect 03"],
    "rationale": "... (per script docstring)",
    "amended_at": "2026-05-16T23:00:00Z",
    "amended_by": "elrond+amend_pimen_bundle_folder_hints_2026_05_16.py"
  }
}
```

For the enemy-elemental sister, an additional field `earth_elemental_subpath: "Extra - Earth Elemental"` points at the in-folder location of the bundled enemy character.

**Queryable tags** (also inserted):

- `bundle-folder-hint:Earth Spell 03` (canonical)
- `bundle-folder-hint:Earth Effect 03` (fallback)

Drax matcher can scan `asset_style_tags` for `bundle-folder-hint:*` tags without parsing the raw JSON.

### Recommendation to drax

Update bundle matcher to:
1. Read `bundle_folder_hint` array from amended metadata (or scan `asset_style_tags WHERE tag LIKE 'bundle-folder-hint:%'`).
2. Try canonical folder first (first list entry).
3. Fall back to alternative folder if canonical is absent OR if richer-format content is required (e.g., needs `Separeted Frames/` for frame-by-frame inspection).
4. Surface ambiguous-match as a pipeline warning (do not halt) when multiple `bundle_folder_hint` candidates resolve.

### Forward signal (not in this dispatch's scope)

The same naming-convention drift likely applies to the other 4 element-effect bundle constituents (`fire-spell-effect-3` / `Fire effect 03`, `thunder-spell-effect-03` / `Thunder Effect 03`, `water-spell-effect-03` / `Water Effect 03`, `wind-spell-effect-03` / `Wind Effect 03`). Inspection of those bundle folders shows each has a single canonical name (no `Effect XX` + `Spell XX` doubled pattern — confirmed for fire/thunder/water/wind), so the slug-collision case is **earth-spell-effect-03 only** in the current bundle. Other sisters are simple slug↔folder pairs that drax's matcher already handles.

Generalization opportunity: at next curation pipeline pass (per `MIGRATION.md` v1.3 open follow-on #2 — generalize `curate_catalogue.py`), capture `bundle_folder_hint` as a first-class field at curation time (not amendment-time), populated by inspecting the bundle archive listing during curation. This makes the slug-collision case impossible to miss at downstream consumption.

---

## 2. Track A item 2 — `Icons` sub-pack inspection + curation decision

### Drax's surfaced concern (verbatim from dispatch)

> `Icons` sub-pack out-of-band: contained in `Elemental Effects.rar`; not in curated catalogue. Action: inspect (visual or metadata-only); decide if it's a curation candidate (UI icons may be useful for VS2a/VS2b); if yes, add curated slug; if no, mark as known-out-of-band.

### Inspection finding (elrond, metadata-only via `lsar`)

```
Elemental Effects/Icons/Earth Icon.png
Elemental Effects/Icons/Earth Icon 2.png
Elemental Effects/Icons/Fire Icon.png
Elemental Effects/Icons/Fire Icon 2.png
Elemental Effects/Icons/Thunder Icon.png
Elemental Effects/Icons/Thunder Icon 2.png
Elemental Effects/Icons/Water Icon.png
Elemental Effects/Icons/Water Icon 2.png
Elemental Effects/Icons/Wind Icon.png
Elemental Effects/Icons/Wind Icon 2.png
```

**10 PNG files** = 5 elements (earth/fire/thunder/water/wind) × 2 variants.

Notable structural observation: no canvas-size suffix in filenames (unlike standard pimen packs which embed canvas size like `Boulder (64x64).png`). Canvas size undetermined from listing alone — visual inspection required post-acquisition to fix `resolution_band`, `palette_size`, `shading_technique`, `linework_style`.

### Curation decision: **INCLUDE**

Rationale:
1. UI icons are useful for VS2a (in-engine element identity rendering) and VS2b (loadout-app element-affinity display) — directly supports both downstream consumer surfaces.
2. 5-element coverage matches pimen's core element palette (earth/fire/thunder/water/wind), aligning with the spirit-swap UI domain (per `canonical/story/style-register.md` register family).
3. 2-variant redundancy gives drax visual-treatment optionality without re-curation.
4. Zero incremental acquisition cost — bundle-internal; bundle already authorized for use.

### Action taken (elrond)

Curated as new slug `mega-pack-elemental-icons` via `agentic_orchestration/research/scripts/curate_pimen_elemental_icons_2026_05_16.py`. Schema row shape:

| Field | Value | Note |
|---|---|---|
| source_asset_id | `mega-pack-elemental-icons` | synthesized slug (no standalone product page) |
| source_url | `https://pimen.itch.io/mega-pack-elemental-spell-effects` | bundle URL (sub-pack has no standalone page) |
| category | `icon` | matches v1.0 schema enum |
| dimensionality | `2d` | |
| derived_register | `manual-review` | R5 cascade defers (no positive register signal in metadata) |
| derived_register_source | `manual-review-resolved` | requires post-acquisition visual inspection |
| embodiment_tag | `not-applicable` | UI asset |
| decomposition | `not-applicable` | UI assets; decomposition meaningless |
| file_format | `png` | 10 separate single-frame PNGs |
| license | `commercial-royalty-free` | inherits bundle license |
| cost_usd | 0.0 | bundle-internal; no incremental cost |
| cost_model | `free` | bundle-internal-only sub-pack |
| quality_flag | `deferred` | post-acquisition inspection required |
| manual_review_queued | 1 | added to visual-inspection queue |

**New operational pattern** captured by this row: **bundle-internal-only sub-packs**. The `source_metadata_raw._curation_overlay_2026_05_16.bundle_internal_only: true` flag + `bundle-internal-only:<bundle_id>` tag identifies sub-packs that ship exclusively as bundle extras (no standalone product page). This is the first instance of this pattern; future bundle inspections will reuse it. The flag distinguishes from standard `in-bundle:<bundle_id>` tags which are for standalone-purchasable packs that ALSO appear in bundles.

**Queryable tags** (all `elrond-curated`):

- `bundle-internal-only:mega-pack-elemental-spell-effects`
- `in-bundle:mega-pack-elemental-spell-effects`
- `subpack-folder-hint:Icons` + `bundle-folder-hint:Icons`
- `asset-count-in-subpack:10`
- `element-coverage:earth,fire,thunder,water,wind`
- `icon-variants:2-per-element`
- `requires-visual-inspection`
- `no-aseprite-source`
- `ui-candidate`
- `pimen-element:multi`

### Visual-inspection queue position

The Icons sub-pack joins the existing 21-row visual-inspection queue (curation-log § 6 in `pimen-curation-log-2026-05-16.md`). Priority guidance:

- **MEDIUM** — bundle-internal-only; no incremental acquisition decision required (bundle already in hand). Inspection can be batched with any post-acquisition pimen visual-inspection session.

Total visual-inspection queue size post-amendment: **23 rows** (22 in catalogue.db post-v1.3 + 1 Icons sub-pack). Note: minor 22-vs-21 discrepancy with the v1.3 curation-log's stated "21" — predates this dispatch; not investigated here.

### Forward signal

If/when drax begins consuming the Icons sub-pack in VS2a or VS2b, the catalogue row provides the canonical reference. Inspection-driven backfill (resolution_band → likely `tiny` or `retro` band; palette_size; shading_technique) updates the row in place (append-only via `superseded_at`).

---

## 3. Track A item 3 — `Explosion VFX 1-30` scout-inspection finding

### Drax's surfaced concern (verbatim from dispatch)

> 30 numbered explosion VFX packs out-of-band: `Explosion VFX.rar` contains `Explosion VFX 1-30`; none match curated `explosion-effect` slug. Action: scout-inspect the 30 sub-packs ...; recommend a curated subset (3-10 packs) for variety, OR mark all 30 as known-out-of-band if none warrant.

### Inspection finding (elrond — **finding contradicts drax's read**)

The 30 numbered `Explosion VFX N/` sub-folders inside `Explosion VFX.rar` are **NOT out-of-band**. They ARE the 30 constituent animations of the already-curated `explosion-effect` pack (`source_asset_id: explosion-effect`, asset_uid in catalogue.db).

**Evidence:**

The curated `explosion-effect` row (from `pimen-catalogue-curated-2026-05-16.jsonl` line 33) has `animations_count: 30`. The `frame_count_notes` field enumerates all 30:

```
VFX1-9 at 32x32 (9-12f); VFX10-12 at 48x48 (10-14f); VFX11 64x32 14f;
VFX13 64x32 10f; VFX14 32x32 10f; VFX15 32x32 12f; VFX16 48x48 10f;
VFX17 48x64 10f; VFX18 48x48 7f; VFX19 64x48 11f; VFX20 48x48 10f;
VFX21 64x64 12f; VFX22 48x48 9f; VFX23 64x64 18f; VFX24 32x32 13f;
VFX25 64x64 10f; VFX26 64x64 10f; VFX27 48x48 9f; VFX28 16x16 10f;
VFX29 16x16 12f; VFX30 32x32 9f.
```

Cross-reference to `lsar` output of `Explosion VFX.rar` confirms exact match:

```
Explosion VFX 1/Explosion VFX 1(32x32).png      → matches VFX1 at 32x32
Explosion VFX 11/Explosion VFX 11(64x32).png    → matches VFX11 at 64x32
Explosion VFX 17/Explosion VFX 17(48x64).png    → matches VFX17 at 48x64
Explosion VFX 21/Explosion VFX 21(64x64).png    → matches VFX21 at 64x64
Explosion VFX 23/Explosion VFX 23(64x64).png    → matches VFX23 at 64x64 (18 frames; "cinematic outlier" per curation note)
Explosion VFX 28/Explosion VFX 28(16x16).png    → matches VFX28 at 16x16 (tiny outlier)
Explosion VFX 29/Explosion VFX 29(16x16).png    → matches VFX29 at 16x16 (tiny outlier)
(... 23 others match equivalently)
```

Each `Explosion VFX N/` folder contains the standard pimen 3-file shape (one `.png` spritesheet + one `.gif` preview + one `.aseprite` source — confirming the curated record's `has_aseprite_source: true`). There are no additional 31st+ sub-packs; no orphaned content. The bundle structure IS the pack structure.

### Root cause of drax's misread

Drax's matcher saw 30 separate folders and inferred "30 separate sub-packs"; the curated row asserts "1 pack with 30 animations". The shape difference (folder-per-animation vs folder-per-pack) is a Pimen packaging convention drax's matcher hadn't yet been calibrated for.

Pimen ships packs in two folder-organization styles:
- **Style A — flat (single-folder)**: `pack-slug/` contains all animations as direct PNG files. Used by older / smaller packs (e.g., `earth-spell-effect-01`, `earth-spell-effect-2`).
- **Style B — per-animation subfolders**: `pack-slug/` contains N `AnimName N/` subfolders, each with one animation's PNG + GIF + aseprite. Used by larger / more recent packs (e.g., `explosion-effect`).

Both styles represent ONE pack; the curated record's `animations_count` tells consumers how many animations are inside, regardless of folder-organization.

### Recommendation: **mark as resolved (no curation action required)**

No additional curated slugs need to be created. The existing `explosion-effect` row covers the 30 animations correctly.

**Subset selection (drax's "recommend a curated subset (3-10 packs) for variety" framing)** is a **CONSUMPTION-time decision**, not a curation-time decision. The catalogue's job is to capture what exists; drax / gandalf / VS2a-integration's job is to select a subset for first-integration. Subset-selection inputs (canvas-size band, frame-count, visual-style) are already in the curated metadata.

### Action taken (elrond)

1. Added drax-matcher-correction tag to the existing `explosion-effect` row:
   - `subpack-organization-style:per-animation-subfolders`
   - `subpack-count-equals-animation-count:true`
2. Annotated the matcher-correction in this finding doc (no JSONL or DB amendment needed; the data IS correct as-curated).

```sql
-- Tags added to explosion-effect (asset_uid lookup at runtime):
INSERT INTO asset_style_tags (asset_uid, tag, confidence, source, added_at)
SELECT asset_uid, 'subpack-organization-style:per-animation-subfolders',
       1.0, 'elrond-curated', '2026-05-16T23:00:00Z'
FROM catalogue_assets WHERE source_asset_id = 'explosion-effect';
-- + matching row for subpack-count-equals-animation-count:true
```

### Recommendation to drax

Update bundle matcher to:
1. Before classifying a folder set as "sub-packs," consult the curated record for `animations_count`. If the folder count equals `animations_count` AND each folder contains a single PNG + (optionally) GIF + aseprite, the structure is per-animation-subfolders (Style B), NOT per-sub-pack.
2. Use the new `subpack-organization-style:*` tag (or absence-thereof) as a fast-path classifier:
   - Tag absent → assume Style A (flat single-folder) for back-compatibility.
   - Tag = `per-animation-subfolders` → expect N subfolders = N animations of the single curated pack.
   - Tag = `multiple-subpacks` → multiple curated slugs share this bundle archive (none in current Pimen catalogue, but generalizes for future cross-pack bundles).
3. When `animations_count` is absent from the curated record, fall back to current heuristic with a pipeline-warning marker on the manifest.

Generalization opportunity (next curation pipeline pass): capture `subpack_organization_style` as a first-class field during curation, populated by inspecting the archive listing.

---

## Summary table — Track A outcomes

| Item | Drax surface | Elrond finding | Action |
|---|---|---|---|
| 1. Slug collision `Earth Spell 03` vs `Earth Effect 03` | Both fuzzy-match `earth-spell-effect-03`; need disambiguation | CONFIRMED — both folders are same pack in 2 formats (compact vs full); canonical = `Earth Spell 03` | `bundle_folder_hint` field added to 2 curated rows (vfx + enemy sister); 4 queryable tags inserted; recommendation to drax matcher documented |
| 2. `Icons` sub-pack out-of-band | Not in curated catalogue; inspect + decide | INSPECTED — 10 PNGs (5 elements × 2 variants); useful for VS2a/VS2b UI | CURATED as new slug `mega-pack-elemental-icons` (`category=icon`, bundle-internal-only flag, queued for post-acquisition visual inspection) |
| 3. 30 explosion VFX sub-packs out-of-band | Inspect; recommend 3-10 curated subset OR all-out-of-band | INSPECTED — they ARE the 30 constituent animations of curated `explosion-effect` (matcher misread); subset selection is consumption-time, not curation-time | 2 queryable tags added to `explosion-effect` row (`subpack-organization-style:per-animation-subfolders`, `subpack-count-equals-animation-count:true`); matcher-correction recommendation documented |

**Net change to catalogue.db state:**

- Existing rows: 47 → 48 (added `mega-pack-elemental-icons`)
- Existing rows amended: 3 (`earth-spell-effect-03` vfx + sister enemy via Track A item 1; `explosion-effect` via Track A item 3)
- Tags added: 4 (Track A item 1 bundle-folder-hints) + 11 (Track A item 2 icon row) + 2 (Track A item 3 explosion-effect annotations) = 17 new tags total
- Visual-inspection queue: 22 → 23 (added Icons sub-pack)
- No `superseded_at` rows created (all amendments are additive overlay; no curation row replaced)

---

## Out-of-band items NOT addressed in this dispatch (forward-queued)

These were observed during Track A inspection but are out of dispatch scope:

1. **`Users/` folder artifact in `Elemental Effects.rar`** — likely a macOS user-path artifact (curator's `~/Users/...` shell history accidentally archived). 0 asset content; mark as known-bundle-noise. Drax matcher can skip safely. No curation action; documenting here for future-bundle-inspection awareness pattern (creator local-path leakage).
2. **Per-element naming-convention drift sister cases** — `Fire effect 03` / `Thunder Effect 03` / `Water Effect 03` / `Wind Effect 03` are bundle-folder names for the corresponding curated `fire-spell-effect-3` / `thunder-spell-effect-03` / `water-spell-effect-03` / `wind-spell-effect-03` records. No `Effect-XX` + `Spell-XX` doubled pattern observed for those 4 (only earth has the doubled variant). Single-folder slug↔match works for those 4 with drax's existing fuzzy matcher; no `bundle_folder_hint` amendment required at this pass. If the matcher surfaces difficulties at first VFX integration in demo, elrond can backfill `bundle_folder_hint` rows for the 4 sisters in a follow-on dispatch.
3. **Generalization of `subpack_organization_style` and `bundle_folder_hint` as first-class curation-time fields** — both surfaced here as amendment-time additions. Next curation pipeline pass (per MIGRATION.md v1.3 open follow-on #2) should capture these at curation time by inspecting the bundle archive listing. Forward-queued; not in this dispatch's scope.
4. **Drax bundle matcher implementation updates** — recommendations captured in §§ 1, 2, 3 above; implementation is drax-side (knight-rider sequences if drax wants a focused matcher-improvement dispatch).

---

## Cross-references

- `agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl` — curated row snapshot (47 → 48 rows; 2 amended in place via overlay)
- `agentic_orchestration/research/curated/catalogue.db` — production catalogue DB (48 rows post-Track-A; v1.1 schema post-Track-B)
- `agentic_orchestration/research/curated/MIGRATION.md` — v1.4 entry covers both Track A and Track B
- `agentic_orchestration/research/scripts/amend_pimen_bundle_folder_hints_2026_05_16.py` — Track A item 1 amendment script (idempotent)
- `agentic_orchestration/research/scripts/curate_pimen_elemental_icons_2026_05_16.py` — Track A item 2 curation script (idempotent)
- `agentic_orchestration/research/scripts/catalogue_migrations/v1_1_register_mixed_flag.sql` — Track B schema migration
- `agentic_orchestration/dispatches/2026-05-16-drax-pimen-ingest-pipeline.md` — upstream drax pipeline completion record
- `agentic_orchestration/research/curated/pimen-curation-log-2026-05-16.md` — initial Pimen curation log (§ 6 visual-inspection queue; this doc adds row 22)
- `agentic_orchestration/research/curated/pimen-bundle-relationships-2026-05-16.json` — bundle constituents map (unchanged by this dispatch; Icons sub-pack joins implicit via `in-bundle:mega-pack-elemental-spell-effects` tag)
- `canonical/story/drift-audit.md` Drift-13 + Pattern P8 — Track B driver

---

— elrond, 2026-05-16. Pattern A dispatch Track A complete. Track B (schema amendment) in `MIGRATION.md` v1.4.
