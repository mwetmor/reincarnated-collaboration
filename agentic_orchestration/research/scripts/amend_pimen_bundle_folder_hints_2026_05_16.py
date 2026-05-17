#!/usr/bin/env python3
"""Amend curated pimen records with bundle_folder_hint (Track A item 1).

Per drax bundle-extension dispatch completion 2026-05-16, the bundle matcher
needs disambiguation help for the slug-collision case in
`Elemental Effects.rar`: both `Earth Spell 03` and `Earth Effect 03` folders
exist as the SAME pack delivered in two formats:

  - `Earth Spell 03/` — spritesheet-only compact format
  - `Earth Effect 03/` — full content (separated frames + spritesheets)

Both have identical top-level structure (11 dirs each, both contain
`Extra - Earth Elemental/`), confirmed by `lsar` inspection of
`/Users/admin/Games/reincarnated-demo/public/assets/pimen/Elemental Effects.rar`.

The curated `earth-spell-effect-03` (vfx primary) and its
`earth-spell-effect-03::enemy-elemental` sister both need the bundle_folder_hint
amendment so drax's matcher can route correctly.

Pattern (extends to other bundle constituents at next curation pass):
  Each bundle-constituent slug carries a list of bundle-folder candidate names
  (matcher tries each in priority order; first-existing wins).

Schema design:
  Lives in `source_metadata_raw` JSON as a new overlay key
  `_amendment_2026_05_16_bundle_folder_hint` to keep amendment lineage explicit.
  This is ADDITIVE to the existing `_curation_overlay_2026_05_16` key (the
  original v1.3 curation overlay). No existing data is mutated; both Legolas's
  raw extraction AND the v1.3 curation overlay remain byte-preserved.

  The amendment also writes a queryable tag into `asset_style_tags`:
  `bundle-folder-hint:Earth Spell 03` (and friends), so drax can scan
  catalogue.db for hints without parsing source_metadata_raw JSON.

Reversibility: the script is idempotent. Running twice has the same effect as
running once. The JSONL snapshot is rewritten in-place with the amendment
overlay appended; the original v1.3 curation overlay is preserved untouched.

Usage:
  python3 agentic_orchestration/research/scripts/amend_pimen_bundle_folder_hints_2026_05_16.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path("/Users/admin/Games/reincarnated-collaboration")
CURATED_DIR = REPO_ROOT / "agentic_orchestration" / "research" / "curated"
DB_PATH = CURATED_DIR / "catalogue.db"
JSONL_PATH = CURATED_DIR / "pimen-catalogue-curated-2026-05-16.jsonl"

AMENDMENT_KEY = "_amendment_2026_05_16_bundle_folder_hint"
NOW_ISO = "2026-05-16T23:00:00Z"  # dispatch authorization date

# Per-slug bundle_folder_hint map.
# Priority order: canonical first, fallback second.
# 'Earth Spell 03' is canonical because the curated record's pack_id resolves
# to the spritesheet-form-only constituent (the format match drax's
# stage-2 frame-assembly expects); 'Earth Effect 03' is the alternative
# full-content format also present in the bundle.
BUNDLE_FOLDER_HINTS = {
    "earth-spell-effect-03": {
        "bundle_id": "mega-pack-elemental-spell-effects",
        "bundle_folder_hint": ["Earth Spell 03", "Earth Effect 03"],
        "rationale": (
            "Elemental Effects.rar contains both 'Earth Spell 03' (spritesheet-only "
            "compact format) and 'Earth Effect 03' (full content: separated frames + "
            "spritesheets). Both folders have identical 11-dir top-level structure, both "
            "contain 'Extra - Earth Elemental/' enemy. Canonical = 'Earth Spell 03' "
            "(matches source product page 'Earth Spell Effect 03' naming convention). "
            "Drax matcher should try canonical first; fall back to 'Earth Effect 03' if "
            "richer format is preferred (more frame data available)."
        ),
    },
    "earth-spell-effect-03::enemy-elemental": {
        "bundle_id": "mega-pack-elemental-spell-effects",
        "bundle_folder_hint": ["Earth Spell 03", "Earth Effect 03"],
        "earth_elemental_subpath": "Extra - Earth Elemental",
        "rationale": (
            "Enemy-elemental sister of earth-spell-effect-03 vfx pack; shares the same "
            "bundle folder. Inside the canonical 'Earth Spell 03/' folder, the Earth "
            "Elemental enemy character lives at 'Extra - Earth Elemental/Earth "
            "Elemental (56x56).png'. Same content under 'Earth Effect 03/' fallback."
        ),
    },
}


def amend_jsonl() -> dict:
    """Append amendment overlay key to matching JSONL rows. Idempotent."""
    if not JSONL_PATH.exists():
        raise FileNotFoundError(f"JSONL snapshot missing: {JSONL_PATH}")

    rows = []
    amended_count = 0
    with JSONL_PATH.open("r", encoding="utf-8") as fp:
        for line in fp:
            if not line.strip():
                continue
            row = json.loads(line)
            asset_id = row.get("source_asset_id")
            if asset_id in BUNDLE_FOLDER_HINTS:
                hint = dict(BUNDLE_FOLDER_HINTS[asset_id])
                hint["amended_at"] = NOW_ISO
                hint["amended_by"] = (
                    "elrond+amend_pimen_bundle_folder_hints_2026_05_16.py"
                )
                # Append amendment overlay; preserve existing _curation_overlay_2026_05_16
                row.setdefault("source_metadata_raw", {})[AMENDMENT_KEY] = hint
                amended_count += 1
            rows.append(row)

    # Atomic write: write to .tmp, then rename
    tmp_path = JSONL_PATH.with_suffix(".jsonl.tmp")
    with tmp_path.open("w", encoding="utf-8") as fp:
        for row in rows:
            fp.write(json.dumps(row, sort_keys=True, ensure_ascii=False))
            fp.write("\n")
    tmp_path.replace(JSONL_PATH)
    return {"total_rows": len(rows), "amended": amended_count}


def amend_catalogue_db() -> dict:
    """Update catalogue.db source_metadata_raw + add asset_style_tags entries.

    Updates the JSON text in catalogue_assets.source_metadata_raw to include the
    amendment overlay. Adds a queryable `bundle-folder-hint:<folder-name>` tag
    per folder candidate (so drax can scan tags without parsing JSON).
    Idempotent.
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(f"catalogue.db missing: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    db_updates = 0
    tags_inserted = 0
    tags_already_present = 0

    try:
        for asset_id, hint_spec in BUNDLE_FOLDER_HINTS.items():
            row = conn.execute(
                "SELECT asset_uid, source_metadata_raw FROM catalogue_assets "
                "WHERE source_asset_id = ? AND source = 'itch-pimen' "
                "AND superseded_at IS NULL",
                (asset_id,),
            ).fetchone()
            if row is None:
                print(
                    f"  WARN: no row for source_asset_id={asset_id} in catalogue.db",
                    file=sys.stderr,
                )
                continue

            asset_uid, raw_json = row
            metadata = json.loads(raw_json) if raw_json else {}

            amendment = dict(hint_spec)
            amendment["amended_at"] = NOW_ISO
            amendment["amended_by"] = (
                "elrond+amend_pimen_bundle_folder_hints_2026_05_16.py"
            )
            metadata[AMENDMENT_KEY] = amendment

            conn.execute(
                "UPDATE catalogue_assets SET source_metadata_raw = ? "
                "WHERE asset_uid = ?",
                (json.dumps(metadata, sort_keys=True, ensure_ascii=False), asset_uid),
            )
            db_updates += 1

            for folder_name in hint_spec["bundle_folder_hint"]:
                tag_value = f"bundle-folder-hint:{folder_name}"
                # ON CONFLICT IGNORE (PRIMARY KEY = (asset_uid, tag))
                cur = conn.execute(
                    "INSERT OR IGNORE INTO asset_style_tags "
                    "(asset_uid, tag, confidence, source, added_at) "
                    "VALUES (?, ?, 1.0, 'elrond-curated', ?)",
                    (asset_uid, tag_value, NOW_ISO),
                )
                if cur.rowcount > 0:
                    tags_inserted += 1
                else:
                    tags_already_present += 1

        conn.commit()
    finally:
        conn.close()

    return {
        "db_updates": db_updates,
        "tags_inserted": tags_inserted,
        "tags_already_present": tags_already_present,
    }


def main() -> int:
    print(f"[amend] starting bundle_folder_hint amendment ({NOW_ISO})")
    print(f"[amend] JSONL: {JSONL_PATH}")
    print(f"[amend] DB:    {DB_PATH}")
    print()

    jsonl_stats = amend_jsonl()
    print(f"[jsonl] {jsonl_stats}")

    db_stats = amend_catalogue_db()
    print(f"[db]    {db_stats}")

    print()
    print("[verify] re-run is a no-op (tags already-present count rises)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
