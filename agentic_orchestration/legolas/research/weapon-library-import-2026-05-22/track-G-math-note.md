# Track G Math Note — GitHub-Hosted Weapon-Data Repositories
# Discipline #1 compliance — authored before script

**Date:** 2026-05-22
**Author:** legolas
**Track:** G (GitHub data repos)

---

## Repo inventory — confirmed by API probe

| Repo | License | Weapon rows | Notes |
|---|---|---|---|
| nick-aschenbach/dnd-data | MIT | ~7,310 | All "weapon class" items: Melee Weapon, Ranged Weapon, martial, simple, Weapon, Wand, Rod, Staff, Ammo. Inclusive; description text is rich per item. No image URLs in data — no image rows. |
| osrsbox/osrsbox-db | GPL-3.0 | 957 | `equipable_weapon=true` items from `docs/items-complete.json`. Wiki URLs present → image URL constructable via OSRS wiki. Icon field = base64 PNG (NOT downloaded — URL only policy applies). |
| 5e-bits/5e-database | MIT | 37 | SRD-only Equipment.json weapons. Very small but clean canonical D&D 5e SRD items. Included as reach target (fast, same clone session). |
| bloqhead/demigods | None (no LICENSE file) | 320 | Elden Ring weapons by type. No license file → record as `unknown`. Still imported (inclusion has no license filter). |

**Total estimated yield:** ~8,624 rows  
**Conservative estimate (after dedup / partial failures):** ~7,500 rows

---

## Runtime estimate

| Phase | Time estimate |
|---|---|
| Clone all 4 repos (shallow depth=1) | ~30-90s total (osrsbox is ~615MB on disk but depth=1 limits to recent tree; we fetch via raw.githubusercontent.com HTTP instead of clone for large repos) |
| Parse + normalize nick-aschenbach (15,749 items, filter to ~7,310) | ~5s |
| Parse + normalize osrsbox (24,735 items, filter to ~957 weapons) | ~3s |
| Parse + normalize 5e-database (237 items, filter to ~37) | <1s |
| Parse + normalize demigods (320 items) | <1s |
| DB insert at 200-row batch WAL mode | ~10-30s total |
| Summary JSON write | <1s |
| **Total wall time** | **~2-4 minutes** |

Note: osrsbox-db is 630MB on disk. Shallow clone is feasible but slow. Preferred strategy: fetch `docs/items-complete.json` directly via `raw.githubusercontent.com` (one HTTP request, ~25MB JSON). No full clone needed for any repo — all canonical data files are single large JSON files accessible via raw.

---

## Rate-limit budget

- GitHub API: 4 repo-tree calls + 4 LICENSE calls = 8 requests unauthenticated. Well within 60/hr.
- raw.githubusercontent.com: 4 large file fetches. No rate limit documented; one at a time with no artificial delay (these are CDN-served file downloads, not scraping).
- Disk: ~100MB temp for JSON files. Negligible.

---

## Failure-mode coverage

| Failure mode | Handling |
|---|---|
| README mis-describes schema | Script inspects actual JSON keys; falls back to `structured_properties` dump of all fields |
| LICENSE file absent (demigods) | Record `license_class='unknown'`; continue import |
| Item has no name field | Skip row; log to extraction_error tally |
| osrsbox icon field = base64 PNG | Do NOT decode or store bytes; skip image rows (URL-only policy); wiki_url → image URL is the image link |
| OSRS wiki image URL format ambiguity | Construct as `https://oldschool.runescape.wiki/images/<name_underscored>.png`; flag confidence=0.7 in image_source |
| Network fetch fails on one file | Catch exception; mark repo as `partial` in summary; continue with others |
| DB constraint violation on UNIQUE (source_library, source_url) | `INSERT OR IGNORE` swallows silently; count ignored rows |
| Demigods no-license edge case | Import with license_class=unknown; commercial flag = 0 per schema seed data |

---

## Reach-target additions confirmed viable

- **5e-bits/5e-database** (MIT, 894 stars): fast, 37 clean SRD weapons — fire in same wave
- **bloqhead/demigods** (no license, 4 stars): 320 Elden Ring weapons — fire with `unknown` license
- **NOT firing this wave:** osrsbox GPL-3.0 note — GPL-3.0 maps to `GPL3` license tier (game_approved=0 per schema seed). Import proceeds regardless (no license filter on inclusion). License tier correctly recorded.

---

## Schema fit — no gaps observed

All required columns in `weapon_knowledge_entries` can be populated from source data:
- `canonical_name` — item name field present in all 4 repos
- `source_library` — slug assigned per repo
- `source_url` — constructed from repo raw URL or wiki_url
- `source_id` — repo's native ID field (OSRS numeric ID; dnd-data uses name as key; 5e uses index slug; demigods uses numeric id)
- `description_text` — present in dnd-data (rich), osrsbox (examine field), 5e (desc), demigods (none → NULL)
- `structured_properties` — JSON dump of all source fields per item
- `cultural_lineage_tags` — inferred from weapon type / game context
- `genre_appearances` — inferred from source game context
- `license_class` — from LICENSE file or 'unknown'

One note: `UNIQUE (source_library, source_url)` is the dedup key per schema. We use `source_url` as the raw item URL. For dnd-data (no canonical per-item URL), we construct a synthetic URL pattern `https://github.com/nick-aschenbach/dnd-data/blob/main/data/items.json#<name_slug>`. This is stable and unique per item.

---

**Signed:** legolas (Track G math note; 2026-05-22)
