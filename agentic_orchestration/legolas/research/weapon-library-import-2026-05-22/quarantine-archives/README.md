# wikipedia-unfiltered quarantine archive

**Date archived:** 2026-05-22
**Authority:** Matt direction 2026-05-22 ("dump-then-delete; scope looks complete, fire both")
**Pattern:** Discipline #11 audit-preservation (compressed JSONL dump before DB DELETE)

## What this is

Compressed audit dump of the 130,334 false-positive rows produced by the A1.2 Wikipedia v1 ingest (loose full-dump keyword matcher; ~9-12% true-positive rate on spot-check). Quarantined as `source_library='wikipedia-unfiltered'` at Cycle 5 (2026-05-22 morning); kept in DB through Cycle 8 wind-down for audit access; deleted from DB on this archive action.

The clean replacement substrate is the v2 ingest at `source_library='wikipedia'` (8,579 rows, Wikidata-anchored, ~100% true-positive).

## Files

| File | Rows | Notes |
|---|---|---|
| `wikipedia-unfiltered-entries-2026-05-22.jsonl.gz` | 130,334 | Full `weapon_knowledge_entries` row export (BLOB columns elided) |
| `wikipedia-unfiltered-images-2026-05-22.jsonl.gz` | 38,589 | Linked `knowledge_entry_reference_images` rows |

## Restoration

If for any reason this quarantine needs restoring to the DB:

```bash
# Round-trip via Python; the JSONL records carry the original schema 1:1 except BLOB elision.
```

## Why preserved

This is the **Discipline #11 empirical anchor** — the bad-data state that taught the team the lesson on loose-regex inclusion gates (athletes, films, songs, train stations, kings matched). Future regex-design work should reference these rows as the negative example library.

## Why deleted from DB

130K rows of confirmed false-positives bloated the DB unnecessarily and complicated downstream queries (every analytical query needed the `WHERE source_library != 'wikipedia-unfiltered'` filter). The compressed archive preserves the audit signal at <100MB; the DB deletion frees space and simplifies the substrate.
