# Finding DRAX-001 — Frame-dir convention not captured in curated records

**Filed by:** drax
**Date:** 2026-05-16
**Severity:** LOW — not blocking pipeline
**Target seam:** elrond (curated records)
**Dispatch context:** `2026-05-16-drax-pimen-ingest-pipeline.md`

---

## Observation

10 of 47 curated records have `has_individual_frames=True` in `parsed_file_format`.
Of these 10, none have an explicit `frame_dir_convention` field capturing HOW the
individual frames are organized inside the archive.

The curated records tell Stage 2 that frames exist, but not what the directory
structure looks like. Stage 2 uses a heuristic: scan for subdirectories containing
>=2 PNGs with numeric stems. This works for the expected Pimen layout
(`AnimationName/0001.png`) but will produce an ambiguous error if Pimen ever ships
a flat-directory frame layout (`animation_name_0001.png` all in root).

## Affected packs (10 rows)

From the curated JSONL, source_asset_ids with `has_individual_frames=True`:
- `ice-spell-effect-01` (confirmed individual-frame, no sheet)
- `ice-spell-effect-02` (individual frames + sheet)
- `holy-spell-effect`
- `dark-spell-effect`
- `acid-spell-effect`
- `wood-spell-effect`
- `mega-pack-elemental-spell-effects`
- `mega-pack-elemental-spell-effects-02`
- `smoke-vfx-1`
- `explosion-effect`

## Request

When elrond adds a curation pre-processor pass for Pimen (or if a future curation
pass touches these rows), consider adding:

```json
"frame_dir_layout": "subdirectory-per-animation"
```

or equivalent, to `parsed_file_format`. Values: `subdirectory-per-animation` /
`flat-root` / `unknown`.

This would let Stage 2 raise a precise error when the layout doesn't match expectation,
rather than a generic "no animation dirs found" message.

## Current workaround

Stage 2's heuristic scan (80% numeric stems in a subdir) covers the expected Pimen
layout and will work correctly when archives are acquired. This finding is informational
— it would improve error quality, not fix a bug.

## Disposition

No action required immediately. Queue for elrond's next curation pass, or at first
post-acquisition visual inspection step for these packs.
