#!/usr/bin/env python3
"""
curate_pimen_full_2026_05_16.py — Pimen full-catalogue curation pass.

Owner: elrond
Dispatch: 2026-05-16-elrond-pimen-full-catalogue-curation.md
Inputs:
  - agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl  (46 raw rows)
Outputs:
  - agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl
  - agentic_orchestration/research/curated/pimen-bundle-relationships-2026-05-16.json
  - agentic_orchestration/research/curated/pimen-curation-log-2026-05-16.md
  - Side effect: ingest into catalogue.db (v1.0 schema)

This is a one-shot curation tool, not a generalized pipeline. It implements:
  1. R5 derivation cascade for `style_register: "pixel-art"` → derived_register sub-register
  2. `pimen_element` migrated into `source_metadata_raw` JSON + emitted as `pimen-element:<value>` tag
  3. `file_format` prose parser → closed-enum file_format + structured parsed_file_format JSON
  4. `requires_visual_inspection` flag for the 20 unknown-resolution rows
  5. CC-BY 4.0 attribution tagging on 2 known CC-BY rows
  6. Bundle membership normalization for mega-pack-elemental-spell-effects (1 and 02)
  7. Category split for earth-spell-effect-03 (vfx pack + bundled enemy character)

This script does NOT modify the v1.0 catalogue.db schema. If curation surfaces a schema gap,
that surfaces as a finding + proposed v1.1 increment; the schema lock is preserved.
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path("/Users/admin/Games/reincarnated-collaboration")
RAW_INPUT = REPO_ROOT / "agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl"
CURATED_DIR = REPO_ROOT / "agentic_orchestration/research/curated"
CURATED_OUT = CURATED_DIR / "pimen-catalogue-curated-2026-05-16.jsonl"
BUNDLE_OUT = CURATED_DIR / "pimen-bundle-relationships-2026-05-16.json"
CURATION_LOG = CURATED_DIR / "pimen-curation-log-2026-05-16.md"
CATALOGUE_DB = CURATED_DIR / "catalogue.db"

CRAWL_SESSION_ID = "legolas-pimen-mode-b-full-2026-05-16"
RAW_OUTPUT_PATH_REL = "agentic_orchestration/research/catalogue/pimen/full-2026-05-16.jsonl"
CURATED_BY = "elrond+curate_pimen_full_2026_05_16.py"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
CURATION_DATE = "2026-05-16"

# ---------------------------------------------------------------------------
# Bundle constituent map — manually derived from extraction_notes 2026-05-16
# ---------------------------------------------------------------------------
# Mega 01 lists 9 element packs: Thunder, Fire, Water, Earth, Wind, Dark, Holy, Ice, Smoke
# Mega 02 lists 5 element packs: Ice, Holy, Dark, Acid, Wood (with potential version drift
#   relative to mega 01's Ice/Holy/Dark per extraction_notes — surfaced for downstream review)
BUNDLE_CONSTITUENTS = {
    "mega-pack-elemental-spell-effects": [
        "fire-spell-effect-3",
        "water-spell-effect-03",
        "earth-spell-effect-03",
        "wind-spell-effect-03",
        "thunder-spell-effect-03",
        "dark-spell-effect",
        "holy-spell-effect",
        "ice-spell-effect-02",
        "smoke-effect-02",
    ],
    "mega-pack-elemental-spell-effects-02": [
        "ice-spell-effect-02",       # overlaps with mega-01; version-drift surfaced
        "holy-spell-effect",          # overlaps with mega-01; version-drift surfaced
        "dark-spell-effect",          # overlaps with mega-01; version-drift surfaced
        "acid-spell-effect",
        "wood-spell-effect",
    ],
}

# CC-BY-4.0 rows — Legolas extraction flagged 2; verified
CC_BY_ROWS = {
    "pixel-battle-effects",
    "cutting-and-healing",
}

# ---------------------------------------------------------------------------
# Pre-processor #3: file_format prose parser
# ---------------------------------------------------------------------------
# Output: (canonical_enum_value, archive_format, archive_size_kb,
#          has_spritesheet, has_individual_frames, has_aseprite_source, parser_notes)
FF_RE_SIZE = re.compile(r"([\d.]+)\s*(kB|MB)", re.IGNORECASE)


def parse_file_format(raw: str, source: str = "pimen") -> dict[str, Any]:
    """Parse Pimen's prose file_format field into structured data.

    Per Pimen structural review Flag 1. The cascade prefers png-spritesheet over aseprite
    when both are present (the spritesheet is the load-time consumable for Pixi.js; aseprite
    is editor-source bonus, captured separately).

    Vendor-heuristic: for source=pimen, "RAR archive (X kB)" with no PNG mention is
    interpreted as png (pimen ships PNG-only content), but marked with
    parser_notes='format_inferred_from_vendor' for audit-trail visibility.
    """
    s = raw.strip()
    sl = s.lower()
    has_spritesheet = "spritesheet" in sl
    has_individual_frames = "individual frames" in sl
    # Negation guard: rows that say "No Aseprite source files confirmed" / "No Aseprite files"
    # should NOT be flagged has_aseprite_source despite containing the substring 'aseprite'.
    aseprite_substr = "aseprite" in sl or ".ase" in sl
    aseprite_negated = bool(re.search(r"no\s+aseprite", sl))
    has_aseprite = aseprite_substr and not aseprite_negated
    has_gif = "gif" in sl
    has_png = "png" in sl
    is_rar = "rar" in sl
    is_zip = "zip" in sl

    archive_format = "rar" if is_rar else ("zip" if is_zip else None)
    size_match = FF_RE_SIZE.search(s)
    archive_size_kb: float | None = None
    if size_match:
        n = float(size_match.group(1))
        unit = size_match.group(2).lower()
        archive_size_kb = n if unit == "kb" else n * 1024.0

    parser_notes: list[str] = []

    # Cascade per structural review Flag 1, extended:
    if has_spritesheet:
        canonical = "png-spritesheet"
    elif has_aseprite and has_png:
        canonical = "png"  # png + aseprite (but no explicit spritesheet)
    elif has_aseprite and not has_png:
        canonical = "aseprite"
    elif has_gif and not has_png:
        canonical = "gif"
    elif has_png:
        canonical = "png"
    elif source == "itch-pimen" and (is_rar or is_zip):
        # Vendor heuristic: pimen ships PNG-only; archive-only string still implies PNG.
        canonical = "png"
        parser_notes.append("format_inferred_from_vendor=pimen-png-only-heuristic")
    else:
        canonical = "unknown"
        parser_notes.append("file_format_unparseable")

    return {
        "canonical": canonical,
        "archive_format": archive_format,
        "archive_size_kb": archive_size_kb,
        "has_spritesheet": has_spritesheet,
        "has_individual_frames": has_individual_frames,
        "has_aseprite_source": has_aseprite,
        "has_gif": has_gif,
        "raw_string": raw,
        "parser_notes": parser_notes,
    }


# ---------------------------------------------------------------------------
# Pre-processor #1: R5 derivation cascade for style_register=pixel-art
# ---------------------------------------------------------------------------
def derive_register(row: dict[str, Any], vendor_register_hint: str = "hand-drawn-pixel") -> tuple[str, str, str]:
    """Apply the structural-review Flag-2 cascade.

    Returns (derived_register, derived_register_source, rationale).

    derived_register_source values match the schema enum:
      - 'rule'                       → deterministic match (positive tag or vendor-hint inference)
      - 'manual-review-resolved'     → reserved for post-curator review (not used in this pass)

    Cascade priority (first match wins):
      1. style_tags contains 'hand-drawn-pixel'             → hand-drawn-pixel  (positive signal)
      2. style_tags contains 'retro' AND resolution_band ∈ ('tiny','retro') → retro-16bit
      3. style_tags contains 'sub-register-uncertain'       → manual-review     (Legolas-explicit defer)
      4. resolution_band == 'hd2d-pixel' AND vendor_hint    → hand-drawn-pixel  (vendor-hint inference,
                                                                                quality_flag=borderline)
      5. default                                            → manual-review
    """
    tags = set(row.get("style_tags") or [])
    rb = row.get("resolution_band") or "unknown"

    if "hand-drawn-pixel" in tags:
        return ("hand-drawn-pixel", "rule", "R5-handdrawn-tag-positive")
    if "retro" in tags and rb in ("tiny", "retro"):
        return ("retro-16bit", "rule", "R5-retro-tag-and-band")
    if "sub-register-uncertain" in tags:
        return ("manual-review", "rule", "R5-sub-register-uncertain-explicit")
    if rb == "hd2d-pixel" and vendor_register_hint == "hand-drawn-pixel":
        return (
            "hand-drawn-pixel",
            "rule",
            "R5-vendor-hint-inferred-from-band",
        )
    return ("manual-review", "rule", "R5-default-conservative")


# ---------------------------------------------------------------------------
# Embodiment derivation (basic — covers pimen's character/enemy assets)
# ---------------------------------------------------------------------------
def derive_embodiment(row: dict[str, Any]) -> tuple[str, str | None]:
    """Return (embodiment_tag, pending_amendment_hint)."""
    cat = row.get("category")
    if cat not in ("character", "enemy"):
        return ("not-applicable", None)
    tags = set(row.get("style_tags") or [])
    # v1.0 starter set: humanoid / slime / beast / dragonling / swarm / construct / spirit / plant
    if "skeleton" in tags or "undead" in tags:
        # Skeleton/undead is a v1.0 starter? No — humanoid covers skeletons (skeletons are bipedal humanoid frames).
        # The structural-review test placed skeleton → humanoid; honour that here.
        return ("humanoid", None)
    if "battlemage" in tags or "character-sprite" in tags:
        return ("humanoid", None)
    if "construct" in tags:
        return ("construct", None)
    if "elemental" in tags:
        # Earth Elemental etc. — read as a 'construct' or 'spirit'? Embodiment vocabulary
        # treats elementals as constructs in the v1.0 starter set (humanoid form, elemental
        # material). Conservative: pending-amendment with hint, let gandalf decide if it's
        # construct-canonical.
        return ("pending-amendment", "elemental humanoid form (Earth Elemental in earth-spell-effect-03)")
    # Default unknown for character/enemy without identifying tags
    return ("unknown", None)


# ---------------------------------------------------------------------------
# Quality flag derivation
# ---------------------------------------------------------------------------
def initial_quality_flag(
    derived_register: str,
    rationale: str,
    license_value: str,
    requires_visual_inspection: bool,
) -> tuple[str, str]:
    """Return (quality_flag, quality_rationale)."""
    notes: list[str] = []
    flag = "unreviewed"

    # License-clarity default per catalogue-schema.md § 4
    if license_value in ("commercial-license", "commercial-royalty-bearing", "proprietary", "unknown"):
        flag = "borderline"
        notes.append(f"license={license_value} requires explicit terms parse")

    if derived_register == "manual-review":
        flag = "deferred"
        notes.append(f"derived_register=manual-review via {rationale}")

    if rationale == "R5-vendor-hint-inferred-from-band":
        # Hand-drawn-pixel inferred from vendor + resolution band only (no positive style_tag);
        # promote-on-inspection workflow.
        if flag == "unreviewed":
            flag = "borderline"
        notes.append("derived from vendor-register hint; promote-on-inspection")

    if requires_visual_inspection and flag == "unreviewed":
        # Don't demote borderline / deferred; only escalate from unreviewed → unreviewed
        # (visual-inspection-required is captured via tags + raw payload, not by demoting
        # the flag from unreviewed unless rule above already set borderline/deferred).
        pass

    return (flag, "; ".join(notes) if notes else None)


# ---------------------------------------------------------------------------
# Asset-style-tags assembly (preserves Legolas tags + adds curator-emitted tags)
# ---------------------------------------------------------------------------
def assemble_tags(
    raw_tags: list[str],
    pimen_element: str | None,
    requires_visual_inspection: bool,
    cc_by: bool,
    parsed_ff: dict[str, Any],
    derived_register: str,
    in_bundle: list[str],
) -> list[dict[str, Any]]:
    """Return list of dicts ready for asset_style_tags insertion."""
    tags: list[dict[str, Any]] = []
    seen: set[str] = set()

    def emit(tag: str, source: str, confidence: float = 1.0) -> None:
        if tag in seen:
            return
        seen.add(tag)
        tags.append({"tag": tag, "source": source, "confidence": confidence})

    # Preserve Legolas-extracted tags
    for t in raw_tags or []:
        emit(t, "legolas-inferred", 1.0)

    # Pimen-element queryable tag (Flag 3 from structural review)
    if pimen_element and pimen_element != "null":
        emit(f"pimen-element:{pimen_element}", "elrond-curated", 1.0)

    # Visual-inspection queue flag
    if requires_visual_inspection:
        emit("requires-visual-inspection", "elrond-curated", 1.0)

    # CC-BY attribution tags (dispatch Step 3)
    if cc_by:
        emit("attribution-required", "elrond-curated", 1.0)
        emit("attribution-acquired-yet:false", "elrond-curated", 1.0)
        emit("license-specifics:cc-by-4.0", "elrond-curated", 1.0)

    # Aseprite-source convenience tag (deferred from structural review optional)
    if parsed_ff.get("has_aseprite_source"):
        emit("has-aseprite-source", "elrond-curated", 1.0)
    else:
        emit("no-aseprite-source", "elrond-curated", 1.0)

    # Bundle membership (curator-emitted)
    for parent_id in in_bundle:
        emit(f"in-bundle:{parent_id}", "elrond-curated", 1.0)

    # Outline-profile side effect — DEFERRED (cannot fire R6 without linework_style filled).
    # Captured in curation log as an outstanding manual-review item; no automated tag here.

    return tags


# ---------------------------------------------------------------------------
# Single-asset curation transform
# ---------------------------------------------------------------------------
def curate_asset(raw: dict[str, Any], constituent_to_bundles: dict[str, list[str]]) -> dict[str, Any]:
    asset_id = raw["asset_id"]
    rb = raw.get("resolution_band") or "unknown"

    # Step 1: derive register
    derived_register, drs, drs_rationale = derive_register(raw)

    # Step 2: parse file_format
    parsed_ff = parse_file_format(raw["file_format"], source=raw.get("source", "itch-pimen"))

    # Step 3: visual-inspection flag (unknown resolution_band triggers it)
    requires_visual_inspection = rb == "unknown"

    # Step 4: derive embodiment
    embodiment_tag, pending_hint = derive_embodiment(raw)

    # Step 5: license → cost_model
    license_value = raw.get("license", "unknown")
    cost_usd = float(raw.get("cost", 0) or 0)
    cost_model = "free" if cost_usd == 0 else "one-time"
    cc_by = asset_id in CC_BY_ROWS

    # Step 6: quality flag
    quality_flag, quality_rationale = initial_quality_flag(
        derived_register, drs_rationale, license_value, requires_visual_inspection
    )

    # Step 7: assemble curated source_metadata_raw — preserve raw + add curation overlays
    curation_overlay = {
        "rule_fired": drs_rationale,
        "parsed_file_format": parsed_ff,
        "requires_visual_inspection": requires_visual_inspection,
        "in_bundles": constituent_to_bundles.get(asset_id, []),
    }
    if cc_by:
        curation_overlay["curation_attribution"] = {
            "attribution_required": True,
            "license_specifics": "CC-BY-4.0; credit creator (Pimen) + link to original work",
            "attribution_acquired_yet": False,
        }

    source_metadata_raw = {
        **raw,
        "_curation_overlay_2026_05_16": curation_overlay,
    }

    # Step 8: assemble queryable style tags
    style_tags = assemble_tags(
        raw_tags=raw.get("style_tags") or [],
        pimen_element=raw.get("pimen_element"),
        requires_visual_inspection=requires_visual_inspection,
        cc_by=cc_by,
        parsed_ff=parsed_ff,
        derived_register=derived_register,
        in_bundle=constituent_to_bundles.get(asset_id, []),
    )

    # Step 9: assemble curated row (schema-shaped)
    return {
        "source": raw.get("source", "itch-pimen"),
        "source_asset_id": asset_id,
        "name": raw["name"],
        "description": None,
        "source_url": raw["url"],
        "source_date": raw["crawl_date"],
        "source_metadata_raw": source_metadata_raw,
        "category": raw["category"],
        "dimensionality": raw.get("dimensionality") or "2d",
        "rubric_version": "1.0",
        "resolution_band": rb,
        "palette_size": raw.get("palette_size") or "unknown",
        "shading_technique": raw.get("shading_technique") or "unknown",
        "linework_style": raw.get("linework_style") or "unknown",
        "animation_frame_density": raw.get("animation_frame_density") or "unknown",
        "derived_register": derived_register,
        "derived_register_source": drs,
        "derived_register_override_rationale": None,
        "embodiment_tag": embodiment_tag,
        "pending_amendment_hint": pending_hint,
        "decomposition": raw.get("decomposition") or "unknown",
        "file_format": parsed_ff["canonical"],
        "license": license_value,
        "license_url": None,
        "cost_usd": cost_usd,
        "cost_model": cost_model,
        "quality_flag": quality_flag,
        "quality_rationale": quality_rationale,
        "manual_review_queued": 1 if derived_register == "manual-review" or requires_visual_inspection else 0,
        "style_tags": style_tags,
        # Curator-pipeline-only field (not in catalogue_assets DDL — placed in source_metadata_raw)
        "_curated_at": NOW,
        "_curated_by": CURATED_BY,
        "_crawl_session_id": CRAWL_SESSION_ID,
    }


# ---------------------------------------------------------------------------
# Category split — earth-spell-effect-03 splits into vfx + enemy character
# ---------------------------------------------------------------------------
def split_category_mixed(curated: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Apply Flag-4: split category-conflated packs into multiple catalogue_assets rows.

    For Pimen full-crawl 2026-05-16, the only confirmed category-conflated pack is
    earth-spell-effect-03 (vfx + bundled Earth Elemental enemy character).

    Result: emit a second row with suffixed source_asset_id ('::enemy-elemental') flagged
    as enemy/construct, sharing the same pack_id when packs are introduced.
    """
    result: list[dict[str, Any]] = []
    for row in curated:
        result.append(row)
        if row["source_asset_id"] == "earth-spell-effect-03":
            # Spawn enemy-elemental sister row
            sister = {**row}
            sister["source_asset_id"] = "earth-spell-effect-03::enemy-elemental"
            sister["name"] = "Earth Spell Effect 03 — Earth Elemental (bundled enemy)"
            sister["category"] = "enemy"
            sister["decomposition"] = "monolithic"  # pimen pattern for char/enemy
            sister["embodiment_tag"] = "pending-amendment"
            sister["pending_amendment_hint"] = (
                "elemental humanoid form (Earth Elemental in earth-spell-effect-03)"
            )
            # Refresh metadata overlay to reflect the split
            new_overlay = dict(sister["source_metadata_raw"]["_curation_overlay_2026_05_16"])
            new_overlay["category_split_from"] = "earth-spell-effect-03"
            new_overlay["category_split_role"] = "enemy-character-half"
            sister["source_metadata_raw"] = {
                **sister["source_metadata_raw"],
                "_curation_overlay_2026_05_16": new_overlay,
            }
            # Tags: replace bundle membership noise with split-marker tags; preserve attribution etc.
            sister_tags = [t for t in sister["style_tags"]
                           if not t["tag"].startswith("in-bundle:")  # bundle membership stays on vfx half
                           and not t["tag"].startswith("pimen-element:")]
            sister_tags.append({"tag": "category-split-from:earth-spell-effect-03",
                                "source": "elrond-curated", "confidence": 1.0})
            sister_tags.append({"tag": "category-split-role:enemy-character-half",
                                "source": "elrond-curated", "confidence": 1.0})
            sister_tags.append({"tag": "bundled-with:earth-spell-effect-03",
                                "source": "elrond-curated", "confidence": 1.0})
            sister["style_tags"] = sister_tags
            result.append(sister)

            # And modify the original row's category-split annotation
            row_overlay = dict(row["source_metadata_raw"]["_curation_overlay_2026_05_16"])
            row_overlay["category_split_into"] = "earth-spell-effect-03::enemy-elemental"
            row_overlay["category_split_role"] = "vfx-pack-half"
            row["source_metadata_raw"] = {
                **row["source_metadata_raw"],
                "_curation_overlay_2026_05_16": row_overlay,
            }
            row["style_tags"].append({
                "tag": "category-split-role:vfx-pack-half",
                "source": "elrond-curated", "confidence": 1.0,
            })
            row["style_tags"].append({
                "tag": "bundled-with:earth-spell-effect-03::enemy-elemental",
                "source": "elrond-curated", "confidence": 1.0,
            })
    return result


# ---------------------------------------------------------------------------
# DB ingest
# ---------------------------------------------------------------------------
def ingest_catalogue_db(curated: list[dict[str, Any]]) -> dict[str, int]:
    """Ingest curated rows into catalogue.db.

    Returns counts dict for verification.

    Order:
      1. catalogue_sources (pimen) — upsert
      2. crawl_sessions — upsert
      3. catalogue_packs (mega-pack-01 + mega-pack-02 + earth-spell-effect-03 pack)
      4. catalogue_assets (all curated rows)
      5. asset_style_tags
    """
    conn = sqlite3.connect(CATALOGUE_DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    # Step 1: source registration
    cur.execute(
        """
        INSERT OR REPLACE INTO catalogue_sources
            (source, display_name, url, vendor_type,
             primary_register_hint, default_license, notes, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "itch-pimen",
            "pimen (itch.io)",
            "https://pimen.itch.io/",
            "individual-creator",
            "hand-drawn-pixel",
            "commercial-royalty-free",
            "HD-2D-shaped pixel art VFX + occasional character/enemy sprite work. Ships free + paid packs; "
            "two packs (pixel-battle-effects, cutting-and-healing) are CC-BY-4.0. Most packs ship as PNG inside "
            "RAR archive. ~30% include Aseprite source. Vendor-canonical register = hand-drawn-pixel.",
            NOW,
        ),
    )

    # Step 2: session registration
    cur.execute(
        """
        INSERT OR REPLACE INTO crawl_sessions
            (session_id, source, legolas_version, mode,
             started_at, completed_at, asset_count, raw_output_path, curated_at, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            CRAWL_SESSION_ID,
            "itch-pimen",
            None,
            "mode-b-full-crawl",
            "2026-05-16T00:00:00Z",  # crawl start (best-known)
            "2026-05-16T00:00:00Z",
            46,
            RAW_OUTPUT_PATH_REL,
            NOW,
            "Pimen full creator-catalogue crawl. Three-track viability gate passed 2026-05-16. "
            "Curated per dispatch 2026-05-16-elrond-pimen-full-catalogue-curation.md.",
        ),
    )

    # Step 3: pack registration — only the explicit bundles + earth-spell-effect-03's pack-of-record
    # (each individual standalone pack-asset is also its own pack for queryability; we model
    # explicit bundles and the category-split-shared pack)
    pack_ids: dict[str, int] = {}
    for pack_source_id, pack_name, pack_cost in (
        ("mega-pack-elemental-spell-effects", "Mega Pack Elemental Spell Effects 01", 12.75),
        ("mega-pack-elemental-spell-effects-02", "Mega Pack Spell Effects 02", 20.40),
        ("earth-spell-effect-03", "Earth Spell Effect 03 (VFX + Earth Elemental enemy)", 3.0),
    ):
        cur.execute(
            """
            INSERT INTO catalogue_packs
                (source, source_pack_id, pack_name, pack_url, pack_license,
                 pack_cost_usd, asset_count, pack_register_consistency, added_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source, source_pack_id) DO UPDATE SET
                pack_name=excluded.pack_name,
                pack_cost_usd=excluded.pack_cost_usd,
                added_at=excluded.added_at
            RETURNING pack_id
            """,
            (
                "itch-pimen",
                pack_source_id,
                pack_name,
                f"https://pimen.itch.io/{pack_source_id}",
                "commercial-royalty-free",
                pack_cost,
                None,  # asset_count populated post-insert
                "unknown",  # populated once all assets curated
                NOW,
            ),
        )
        row = cur.fetchone()
        pack_ids[pack_source_id] = row[0]

    # Step 4: insert assets
    assets_inserted = 0
    tags_inserted = 0
    for row in curated:
        # Determine pack_id, if any
        pid = None
        if row["source_asset_id"] in pack_ids:
            pid = pack_ids[row["source_asset_id"]]
        elif row["source_asset_id"] == "earth-spell-effect-03::enemy-elemental":
            pid = pack_ids.get("earth-spell-effect-03")

        cur.execute(
            """
            INSERT INTO catalogue_assets (
                source, source_asset_id, crawl_session_id, source_url, source_date,
                source_metadata_raw, name, description, pack_id,
                category, dimensionality, rubric_version,
                resolution_band, palette_size, shading_technique, linework_style,
                animation_frame_density, derived_register, derived_register_source,
                derived_register_override_rationale, embodiment_tag, pending_amendment_hint,
                decomposition, file_format,
                license, license_url, cost_usd, cost_model,
                quality_flag, quality_rationale, manual_review_queued,
                curated_at, curated_by, superseded_at, superseded_by_uid
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING asset_uid
            """,
            (
                row["source"],
                row["source_asset_id"],
                CRAWL_SESSION_ID,
                row["source_url"],
                row["source_date"],
                json.dumps(row["source_metadata_raw"], sort_keys=True),
                row["name"],
                row["description"],
                pid,
                row["category"],
                row["dimensionality"],
                row["rubric_version"],
                row["resolution_band"],
                row["palette_size"],
                row["shading_technique"],
                row["linework_style"],
                row["animation_frame_density"],
                row["derived_register"],
                row["derived_register_source"],
                row["derived_register_override_rationale"],
                row["embodiment_tag"],
                row["pending_amendment_hint"],
                row["decomposition"],
                row["file_format"],
                row["license"],
                row["license_url"],
                row["cost_usd"],
                row["cost_model"],
                row["quality_flag"],
                row["quality_rationale"],
                row["manual_review_queued"],
                NOW,
                CURATED_BY,
                None,
                None,
            ),
        )
        asset_uid = cur.fetchone()[0]
        assets_inserted += 1

        for t in row["style_tags"]:
            cur.execute(
                """
                INSERT INTO asset_style_tags (asset_uid, tag, confidence, source, added_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(asset_uid, tag) DO NOTHING
                """,
                (asset_uid, t["tag"], t["confidence"], t["source"], NOW),
            )
            tags_inserted += cur.rowcount

    # Update pack asset_count
    for pack_source_id, pid in pack_ids.items():
        cur.execute(
            "SELECT COUNT(*) FROM catalogue_assets WHERE pack_id=?",
            (pid,),
        )
        cnt = cur.fetchone()[0]
        cur.execute(
            "UPDATE catalogue_packs SET asset_count=? WHERE pack_id=?",
            (cnt, pid),
        )

    conn.commit()
    counts = {
        "assets_inserted": assets_inserted,
        "tags_inserted": tags_inserted,
        "packs_registered": len(pack_ids),
    }
    conn.close()
    return counts


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    # 1. Load raw rows
    raw_rows = [json.loads(line) for line in RAW_INPUT.read_text().splitlines() if line.strip()]
    print(f"[load] {len(raw_rows)} raw rows from {RAW_INPUT.name}")

    # 2. Build constituent-to-bundles reverse map
    constituent_to_bundles: dict[str, list[str]] = {}
    for bundle, constituents in BUNDLE_CONSTITUENTS.items():
        for c in constituents:
            constituent_to_bundles.setdefault(c, []).append(bundle)

    # 3. Curate each row
    curated = [curate_asset(r, constituent_to_bundles) for r in raw_rows]

    # 4. Apply category split (earth-spell-effect-03)
    curated = split_category_mixed(curated)
    print(f"[curate] {len(curated)} rows after category split")

    # 5. Write curated JSONL
    CURATED_OUT.write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in curated) + "\n"
    )
    print(f"[write] {CURATED_OUT}")

    # 6. Write bundle relationships JSON
    bundle_doc = {
        "schema_version": "1.0",
        "produced_by": CURATED_BY,
        "produced_at": NOW,
        "source": "itch-pimen",
        "crawl_session_id": CRAWL_SESSION_ID,
        "bundles": [
            {
                "bundle_id": bundle_id,
                "constituents": constituents,
                "notes": "version-drift surfaced in extraction_notes for overlap between mega-01 and mega-02"
                if bundle_id == "mega-pack-elemental-spell-effects-02"
                else None,
            }
            for bundle_id, constituents in BUNDLE_CONSTITUENTS.items()
        ],
    }
    BUNDLE_OUT.write_text(json.dumps(bundle_doc, indent=2, sort_keys=True) + "\n")
    print(f"[write] {BUNDLE_OUT}")

    # 7. Ingest into catalogue.db
    counts = ingest_catalogue_db(curated)
    print(f"[ingest] {counts}")

    # 8. Print curation summary for stdout / log capture
    register_counter = Counter(r["derived_register"] for r in curated)
    quality_counter = Counter(r["quality_flag"] for r in curated)
    license_counter = Counter(r["license"] for r in curated)
    print(f"[summary] derived_register: {dict(register_counter)}")
    print(f"[summary] quality_flag:     {dict(quality_counter)}")
    print(f"[summary] license:          {dict(license_counter)}")


if __name__ == "__main__":
    main()
