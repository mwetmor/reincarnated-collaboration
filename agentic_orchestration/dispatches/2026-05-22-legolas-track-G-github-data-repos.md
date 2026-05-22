# Dispatch — legolas — Track G: GitHub-Hosted Weapon-Data Repositories

**Date:** 2026-05-22
**Author:** knight-rider (hive-mind orchestrator)
**For:** legolas
**Pattern:** B (long task; per-repo clone + parse + insert pipeline)
**Status:** FIRING (Wave 1)
**Mission:** `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`

---

## Required reading

1. Mission doc (above)
2. Schema: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0
3. Robots / etiquette note: GitHub is GREEN for git-clone of public repos — no robots concern. Honor GitHub API rate limits (5000 req/hr authenticated; 60/hr unauthenticated) if using API for repo metadata.

---

## Task

Clone and parse GitHub-hosted weapon/RPG-data repositories. Insert normalized rows into `weapon_knowledge_entries` (with `source_library` set per-repo) and `knowledge_entry_reference_images` for any reference-image URLs encountered.

### Seed list (FIRE these immediately)

| Repo | URL | Genre | Expected yield |
|---|---|---|---|
| nick-aschenbach/dnd-data | https://github.com/nick-aschenbach/dnd-data | D&D 5e | ~200-500 weapons (low confidence; verify) |
| osrsbox/osrsbox-db | https://github.com/osrsbox/osrsbox-db | OSRS | ~2K-3K weapon items (estimated from their item-count claims) |

### Extend the seed list with DISCOVERY scout output

After the DISCOVERY scout returns its CSV (`discovery-wave1.csv`), knight-rider will filter rows where `category` includes `game-data-*` AND `access_method = git-clone` AND `robots_status = GREEN`, and append them to this dispatch as Wave-2 additions. For this Wave-1 fire, work the seed list.

### Optional wave-1 reach targets (investigate, fire if quick)

Use GitHub's search API or web-search to identify any of these as high-yield repos to add to this wave:
- `5e-database` or similar D&D 5e JSON databases
- `pathfinder-data` or Pathfinder structured data
- `wow-classic-database` if structured-public
- `path-of-exile-data` or PoE community data exports
- `eldenring-data` or similar
- Any `<game-name>-data` repo with ≥100 stars

---

## Per-repo pipeline (canonical pattern)

For each repo:

1. **Probe phase (cheap):** `git clone --depth 1 <url> /tmp/track-G/<repo-name>` — shallow clone
2. **Schema-discovery phase:** walk the file tree, identify the canonical weapon-data file(s) (JSON, YAML, CSV, SQL, XML, sometimes Markdown). Read the README for licensing + structure docs
3. **Normalize phase:** map source-specific weapon schema → our `weapon_knowledge_entries` schema:
   - `source_library` = repo's canonical short name (e.g., `osrsbox-db`, `nick-aschenbach-dnd-data`)
   - `source_id` = repo's per-item identifier (e.g., OSRS item ID, D&D weapon slug)
   - `canonical_name` = repo's canonical weapon name
   - `description_text` = freetext description if present
   - `structured_properties` = JSON of the repo's per-item structured fields (damage, weight, material, rarity, etc.)
   - `cultural_lineage_tags` = list of tags (e.g., `medieval`, `fantasy-d&d-5e`, `osrs-game`)
   - `genre_tags` = list of mission-doc § 2.1 genre matches
4. **License extraction phase:** read LICENSE file; map to `licenses` reference-table tier. If no LICENSE file: log as `unknown` and continue (do NOT skip — record what we found)
5. **Image-link extraction phase:** if the repo references image URLs (some include `image_url` field; some include local image files like `images/<id>.png` which then live in GitHub raw), record per `knowledge_entry_reference_images` row with `image_source=<repo-name>` and `image_url=<raw.githubusercontent.com/...>`. URL-only per mission § 3.
6. **Insert phase:** `INSERT OR IGNORE INTO weapon_knowledge_entries(...) VALUES (...)`. Batch 100-500 per transaction with WAL.
7. **Summary phase:** at end of repo, INSERT one row to a per-track import-log file noting (entries-imported, license, schema-fit-notes, any failures)

---

## Discipline #19 compliance

- **Author script first**, fire as `nohup python track_g_import.py > logs/weapon-library-track-G.log 2>&1 &`
- Return immediately to knight-rider with: script path, PID, log path, `JSON_summary_path=agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/summaries/track-G-wave1.json`
- Knight-rider polls on-demand
- Final JSON summary on completion:
  ```json
  {
    "track": "G",
    "wave": 1,
    "started_at": "...",
    "completed_at": "...",
    "wall_seconds": ...,
    "repos_attempted": [...],
    "per_repo_results": [
      {
        "repo": "osrsbox-db",
        "url": "...",
        "license": "BSD-2-Clause",
        "entries_imported": 2841,
        "images_imported": 2841,
        "failures": [],
        "notes": "..."
      },
      ...
    ],
    "total_entries_imported": ...,
    "total_images_imported": ...,
    "schema_gaps_observed": [...],
    "next_wave_recommendations": [...]
  }
  ```

---

## Discipline #20 compliance

- GitHub public repos are GREEN for git-clone; no robots concern for clone path
- If a per-repo CDN serves images via robots-restricted endpoint, honor that — but raw.githubusercontent.com is GREEN
- GitHub API rate limits: 60 req/hr unauthenticated. If using API for repo enumeration, use authenticated requests (`GH_TOKEN` env var if available) or pace at 60/hr. Don't burn the limit.

---

## Discipline #1 (math-before-code)

Brief math note before authoring the script:
- Per-repo expected yield (refine from seed list above with quick README peek)
- Wall-time estimate (clone + parse + insert; should be minutes per small repo, ~10-30 min for osrsbox-db which is larger)
- Failure mode coverage: what if README mis-describes schema? What if LICENSE absent? What if image-paths broken?

Math note: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-G-math-note.md`

(Math note is brief — half a page. No jack-ryan Gate-1 needed under default authority.)

---

## Acceptance criteria

| # | Criterion |
|---|---|
| 1 | Seed-list repos (nick-aschenbach/dnd-data + osrsbox-db) both attempted; whatever they yield, recorded |
| 2 | ≥1,500 `weapon_knowledge_entries` rows imported across Track G (could be higher; floor is sanity-check) |
| 3 | JSON summary at canonical path |
| 4 | License tier captured per repo (NULL = explicitly recorded as `unknown`, not silently dropped) |
| 5 | Logs at `/Users/admin/Games/reincarnated-engine/logs/weapon-library-track-G.log` |
| 6 | Script committed at `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/scripts/track_g_import.py` |
| 7 | Cloned repos cleaned up after import (rm -rf /tmp/track-G/) UNLESS Matt directs otherwise |

---

## Out of scope

- Cloning RED-licensed repos (those would be discovered by DISCOVERY scout; should be excluded from Wave-2 additions)
- Negotiating with repo maintainers
- Building schema-bridging UI; we're insert-only here

---

## Cross-references

- Mission: `agentic_orchestration/weapon-library-import-hive-mind-mission-2026-05-22.md`
- DISCOVERY dispatch: `dispatches/2026-05-22-legolas-DISCOVERY-source-scouting.md`
- Schema: `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0

---

**Signed:** knight-rider (hive-mind orchestrator; Wave-1 fire 2026-05-22)
