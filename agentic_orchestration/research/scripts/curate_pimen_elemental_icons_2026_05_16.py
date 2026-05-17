#!/usr/bin/env python3
"""Curate the Elemental Icons sub-pack (Track A item 2).

Per drax bundle-extension dispatch completion 2026-05-16, the `Icons` sub-folder
in `Elemental Effects.rar` was surfaced as out-of-band (not in curated catalogue).
Inspection finding (via `lsar`):

    Elemental Effects/Icons/Earth Icon.png        (5 elements ×
    Elemental Effects/Icons/Earth Icon 2.png       2 variants =
    Elemental Effects/Icons/Fire Icon.png          10 PNG files)
    Elemental Effects/Icons/Fire Icon 2.png
    Elemental Effects/Icons/Thunder Icon.png
    Elemental Effects/Icons/Thunder Icon 2.png
    Elemental Effects/Icons/Water Icon.png
    Elemental Effects/Icons/Water Icon 2.png
    Elemental Effects/Icons/Wind Icon.png
    Elemental Effects/Icons/Wind Icon 2.png

Curation decision: CURATE as a new slug `mega-pack-elemental-icons` because:

  1. UI icons are useful for VS2a (in-engine element identity) and VS2b
     (loadout-app element-affinity display).
  2. 5-element coverage matches pimen's core element palette (earth, fire,
     thunder, water, wind) — natural fit for spirit-swap UI rendering.
  3. 10 small assets (2 variants each) gives Drax + the demo enough redundancy
     to pick visual treatment without re-curating.

Provenance:
  - Sourced ONLY from bundle Elemental Effects.rar (no standalone Pimen product
    page for these icons; they ship exclusively as a bundle extra).
  - `bundle_internal_only=true` flag in source_metadata_raw distinguishes from
    standalone-product packs. This is a new operational pattern — first instance
    captured here; will generalize via the next curation pipeline pass.
  - source_url = bundle URL (mega-pack-elemental-spell-effects on pimen.itch.io)
  - source_asset_id = 'mega-pack-elemental-icons' (synthesized slug for the
    sub-pack, not a vendor-issued ID)

Schema row shape:
  - category = 'icon' (per the v1.0 schema enum)
  - dimensionality = '2d'
  - resolution_band = 'unknown' (canvas size not specified in archive listing;
    visible filenames show no size suffix, unlike standard pimen packs that
    embed canvas size in filename like 'Boulder (64x64).png')
  - palette_size / shading_technique / linework_style / animation_frame_density
    = 'unknown' until post-acquisition visual inspection (manual_review_queued=1)
  - decomposition = 'not-applicable' (UI icons; decomposition meaningless)
  - file_format = 'png' (single-frame PNG; 10 separate files; not a spritesheet)
  - license = 'commercial-royalty-free' (inherited from bundle license)
  - cost_usd = 0.0 (bundle-internal; pricing is bundle-level not per-sub-pack)
  - cost_model = 'free' (per the bundle-internal-only nature; not separately purchasable)
  - embodiment_tag = 'not-applicable' (UI element)
  - derived_register = 'manual-review' (R5 cascade defers — no positive register
    signal in metadata; bundle context says hand-drawn-pixel but icon-style may
    not match the parent pack's register signature; force post-acquisition review)

Tags applied:
  - bundle-internal-only:mega-pack-elemental-spell-effects
  - in-bundle:mega-pack-elemental-spell-effects
  - subpack-folder-hint:Icons
  - asset-count-in-subpack:10
  - element-coverage:earth,fire,thunder,water,wind
  - icon-variants:2-per-element
  - requires-visual-inspection
  - no-aseprite-source
  - bundle-folder-hint:Icons

Audit-trail:
  - curated_by = 'elrond+curate_pimen_elemental_icons_2026_05_16.py'
  - curated_at = 2026-05-16T23:00:00Z
  - rubric_version = 1.0

Idempotent: re-run is a no-op (uses INSERT OR IGNORE on the natural-key
constraint UNIQUE (source, source_asset_id, crawl_session_id)).

Usage:
  python3 agentic_orchestration/research/scripts/curate_pimen_elemental_icons_2026_05_16.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path("/Users/admin/Games/reincarnated-collaboration")
CURATED_DIR = REPO_ROOT / "agentic_orchestration" / "research" / "curated"
DB_PATH = CURATED_DIR / "catalogue.db"
JSONL_PATH = CURATED_DIR / "pimen-catalogue-curated-2026-05-16.jsonl"

NOW_ISO = "2026-05-16T23:00:00Z"
CRAWL_SESSION_ID = "legolas-pimen-mode-b-full-2026-05-16"

ICON_ASSET = {
    "source": "itch-pimen",
    "source_asset_id": "mega-pack-elemental-icons",
    "crawl_session_id": CRAWL_SESSION_ID,
    "source_url": "https://pimen.itch.io/mega-pack-elemental-spell-effects",
    "source_date": "2026-05-16",
    "name": "Elemental Icons (mega-pack bundle sub-pack)",
    "description": (
        "5-element pixel icon set (earth/fire/thunder/water/wind, 2 variants each). "
        "Shipped EXCLUSIVELY as bundle-internal sub-pack inside Elemental Effects.rar "
        "(mega-pack-elemental-spell-effects); no standalone Pimen product page."
    ),
    "category": "icon",
    "dimensionality": "2d",
    "rubric_version": "1.0",
    "resolution_band": "unknown",
    "palette_size": "unknown",
    "shading_technique": "unknown",
    "linework_style": "unknown",
    "animation_frame_density": "static",
    "derived_register": "manual-review",
    "derived_register_source": "manual-review-resolved",
    "derived_register_override_rationale": (
        "R5 cascade defers: no positive register signal in archive metadata. "
        "Bundle context implies hand-drawn-pixel (matches parent pack register) "
        "but icon-style typography may diverge from parent. Post-acquisition "
        "visual inspection required to commit derived_register; meanwhile "
        "manual-review marker keeps icons out of default consumption filter "
        "(which requires derived_register IN locked-register set)."
    ),
    "embodiment_tag": "not-applicable",
    "pending_amendment_hint": None,
    "decomposition": "not-applicable",
    "file_format": "png",
    "license": "commercial-royalty-free",
    "license_url": None,
    "cost_usd": 0.0,
    "cost_model": "free",
    "quality_flag": "deferred",
    "quality_rationale": (
        "Bundle-internal sub-pack; visual inspection required post-acquisition. "
        "License is clear (inherits bundle royalty-free); register / palette / "
        "shading deferred to inspection. UI consumption candidate for VS2a / VS2b."
    ),
    "manual_review_queued": 1,
}

ICON_TAGS = [
    "bundle-internal-only:mega-pack-elemental-spell-effects",
    "in-bundle:mega-pack-elemental-spell-effects",
    "subpack-folder-hint:Icons",
    "bundle-folder-hint:Icons",
    "asset-count-in-subpack:10",
    "element-coverage:earth,fire,thunder,water,wind",
    "icon-variants:2-per-element",
    "requires-visual-inspection",
    "no-aseprite-source",
    "ui-candidate",
    "pimen-element:multi",
]

ICON_SOURCE_METADATA_RAW = {
    "_curation_overlay_2026_05_16": {
        "in_bundles": ["mega-pack-elemental-spell-effects"],
        "bundle_internal_only": True,
        "subpack_folder": "Icons",
        "subpack_file_inventory": [
            "Earth Icon.png",
            "Earth Icon 2.png",
            "Fire Icon.png",
            "Fire Icon 2.png",
            "Thunder Icon.png",
            "Thunder Icon 2.png",
            "Water Icon.png",
            "Water Icon 2.png",
            "Wind Icon.png",
            "Wind Icon 2.png",
        ],
        "parsed_file_format": {
            "canonical": "png",
            "raw_string": "10 PNG files (5 elements x 2 variants)",
            "has_aseprite_source": False,
            "has_gif": False,
            "has_individual_frames": True,
            "has_spritesheet": False,
            "archive_format": "bundle-internal",
            "archive_size_kb": None,
            "parser_notes": [
                "shipped as 10 separate PNG files within bundle Icons/ folder",
                "no standalone product page; sub-pack of Elemental Effects.rar",
                "canvas size not in filename (unlike standard pimen packs)",
            ],
        },
        "requires_visual_inspection": True,
        "rule_fired": "R5-defer-manual-review",
        "discovered_by": "drax-bundle-pipeline-2026-05-16-out-of-band-flag",
        "curation_decision": "include",
        "curation_rationale": (
            "UI icon coverage useful for VS2a (in-engine element identity) and "
            "VS2b (loadout-app element-affinity display). 5-element coverage "
            "matches pimen's core element palette. Free bundle-internal; no "
            "incremental acquisition cost."
        ),
    },
}


def insert_icon_row() -> dict:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"catalogue.db missing: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        # Check if already inserted (idempotence).
        existing = conn.execute(
            "SELECT asset_uid FROM catalogue_assets "
            "WHERE source = ? AND source_asset_id = ? AND crawl_session_id = ?",
            (
                ICON_ASSET["source"],
                ICON_ASSET["source_asset_id"],
                ICON_ASSET["crawl_session_id"],
            ),
        ).fetchone()

        if existing is not None:
            asset_uid = existing[0]
            print(f"[skip] row already exists at asset_uid={asset_uid}")
            return {"inserted": 0, "asset_uid": asset_uid, "tags_inserted": 0}

        # Insert primary row.
        columns = [
            "source", "source_asset_id", "crawl_session_id", "source_url",
            "source_date", "source_metadata_raw", "name", "description",
            "category", "dimensionality", "rubric_version", "resolution_band",
            "palette_size", "shading_technique", "linework_style",
            "animation_frame_density", "derived_register",
            "derived_register_source", "derived_register_override_rationale",
            "embodiment_tag", "pending_amendment_hint", "decomposition",
            "file_format", "license", "license_url", "cost_usd", "cost_model",
            "quality_flag", "quality_rationale", "manual_review_queued",
            "curated_at", "curated_by",
        ]
        placeholders = ", ".join(["?"] * len(columns))
        values = [
            ICON_ASSET["source"],
            ICON_ASSET["source_asset_id"],
            ICON_ASSET["crawl_session_id"],
            ICON_ASSET["source_url"],
            ICON_ASSET["source_date"],
            json.dumps(ICON_SOURCE_METADATA_RAW, sort_keys=True, ensure_ascii=False),
            ICON_ASSET["name"],
            ICON_ASSET["description"],
            ICON_ASSET["category"],
            ICON_ASSET["dimensionality"],
            ICON_ASSET["rubric_version"],
            ICON_ASSET["resolution_band"],
            ICON_ASSET["palette_size"],
            ICON_ASSET["shading_technique"],
            ICON_ASSET["linework_style"],
            ICON_ASSET["animation_frame_density"],
            ICON_ASSET["derived_register"],
            ICON_ASSET["derived_register_source"],
            ICON_ASSET["derived_register_override_rationale"],
            ICON_ASSET["embodiment_tag"],
            ICON_ASSET["pending_amendment_hint"],
            ICON_ASSET["decomposition"],
            ICON_ASSET["file_format"],
            ICON_ASSET["license"],
            ICON_ASSET["license_url"],
            ICON_ASSET["cost_usd"],
            ICON_ASSET["cost_model"],
            ICON_ASSET["quality_flag"],
            ICON_ASSET["quality_rationale"],
            ICON_ASSET["manual_review_queued"],
            NOW_ISO,
            "elrond+curate_pimen_elemental_icons_2026_05_16.py",
        ]
        cur = conn.execute(
            f"INSERT INTO catalogue_assets ({', '.join(columns)}) "
            f"VALUES ({placeholders})",
            values,
        )
        asset_uid = cur.lastrowid

        # Tags.
        tags_inserted = 0
        for tag_value in ICON_TAGS:
            tag_cur = conn.execute(
                "INSERT OR IGNORE INTO asset_style_tags "
                "(asset_uid, tag, confidence, source, added_at) "
                "VALUES (?, ?, 1.0, 'elrond-curated', ?)",
                (asset_uid, tag_value, NOW_ISO),
            )
            if tag_cur.rowcount > 0:
                tags_inserted += 1

        conn.commit()
        return {"inserted": 1, "asset_uid": asset_uid, "tags_inserted": tags_inserted}
    finally:
        conn.close()


def append_jsonl_row(asset_uid: int) -> None:
    """Append curated row to the JSONL snapshot.

    Idempotent: scans existing JSONL first to skip if source_asset_id already
    present.
    """
    if not JSONL_PATH.exists():
        raise FileNotFoundError(f"JSONL snapshot missing: {JSONL_PATH}")

    # Check idempotence.
    with JSONL_PATH.open("r", encoding="utf-8") as fp:
        for line in fp:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("source_asset_id") == ICON_ASSET["source_asset_id"]:
                print(f"[jsonl] row for {ICON_ASSET['source_asset_id']} already present; skipping")
                return

    # Build the JSONL row matching the v1.3 snapshot shape.
    jsonl_row = dict(ICON_ASSET)
    jsonl_row["source_metadata_raw"] = ICON_SOURCE_METADATA_RAW
    jsonl_row["_crawl_session_id"] = CRAWL_SESSION_ID
    jsonl_row["_curated_at"] = NOW_ISO
    jsonl_row["_curated_by"] = "elrond+curate_pimen_elemental_icons_2026_05_16.py"
    jsonl_row["style_tags"] = [
        {
            "confidence": 1.0,
            "source": "elrond-curated",
            "tag": tag_value,
        }
        for tag_value in ICON_TAGS
    ]
    # Strip crawl_session_id duplicate (already in _crawl_session_id).
    jsonl_row.pop("crawl_session_id", None)

    with JSONL_PATH.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(jsonl_row, sort_keys=True, ensure_ascii=False))
        fp.write("\n")
    print(f"[jsonl] appended row for {ICON_ASSET['source_asset_id']}")


def main() -> int:
    print(f"[curate] starting Elemental Icons sub-pack curation ({NOW_ISO})")
    print(f"[curate] JSONL: {JSONL_PATH}")
    print(f"[curate] DB:    {DB_PATH}")
    print()

    db_stats = insert_icon_row()
    print(f"[db] {db_stats}")

    append_jsonl_row(db_stats["asset_uid"])

    print()
    print("[verify] re-run is a no-op (uniqueness on (source, source_asset_id, crawl_session_id))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
