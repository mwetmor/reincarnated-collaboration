# Track I Math Note — Cataclysm: Dark Days Ahead

**Date:** 2026-05-22
**Agent:** legolas
**Discipline:** #1 (math-before-code)

---

## Source

- Repo: `https://github.com/CleverRaven/Cataclysm-DDA`
- License: CC-BY-SA-3.0 (confirmed via LICENSE file in repo root)
- Clone strategy: `git clone --depth 1` (shallow; no history)

## Expected yield

| Estimate basis | Count |
|---|---|
| Total items in data/json/items/ (all types) | ~4,500–5,500 |
| GUN type items (all included, weapons by definition) | ~300–600 |
| AMMO type items (included; often weapon-adjacent) | ~300–700 |
| TOOL type items with WEAPON flag | ~100–300 |
| GENERIC type items with WEAPON flag | ~200–500 |
| **Total weapon-class entries expected** | **800–2,100** |
| Scout estimate | 1K–3K |
| Acceptance floor | 800 |

## Runtime estimate

| Phase | Estimate |
|---|---|
| Shallow clone (~100-200MB repo) | 30–90s (network-bound) |
| JSON walk + parse (local) | 5–15s |
| DB insert (batch 500) | <5s |
| Cleanup | <1s |
| **Total wall time** | **<3 minutes** |

## Rate-limit budget

Zero — all processing is local after clone. No network calls during parse/insert phase.

## Name field shape variation

CDA items use two name shapes:
- Simple string: `"name": "kitchen knife"`
- Object: `"name": {"str": "knife", "str_pl": "knives"}`

Script handles both via isinstance check.

## Item inclusion logic

- `type == "GUN"`: include unconditionally (all gun-type items are weapons)
- `type == "AMMO"`: include unconditionally (ammo provides weapon-context data)
- `type == "TOOL"`: include only if `"WEAPON"` in flags array
- `type == "GENERIC"`: include only if `"WEAPON"` in flags array
- Other types: skip

## Failure modes

| Mode | Coverage |
|---|---|
| Malformed JSON file | try/except per file; log + continue |
| Missing `id` or `name` field | skip row; log warning |
| Duplicate (id, path) | INSERT OR IGNORE on (source_library, source_url) |
| Clone fails (network) | script exits with non-zero; log captures error |
| Repo structure change | os.walk covers all subdirs under data/json/items/ |

## Batch strategy

- INSERT OR IGNORE batches of 500 rows per transaction
- SQLite WAL mode (pre-existing on DB)
- No lock contention expected (single writer for this track)

## Output artifacts

- Script: `scripts/track_i_cataclysm.py`
- Log: `/tmp/track-I/track_i_cataclysm.log`
- Summary JSON: `summaries/track-I-cataclysm-summary.json`
- Temp clone dir: `/tmp/track-I/cataclysm` (cleaned post-import)
