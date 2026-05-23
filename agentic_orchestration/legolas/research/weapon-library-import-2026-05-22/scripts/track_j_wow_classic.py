#!/usr/bin/env python3
"""
Track J — WoW Classic Items
Hive-mind weapon-library import: nexus-devs/wow-classic-items (MIT)

Discipline #19: fires and returns; writes summary JSON artifact on completion.

Math note:
  ~17K-22K total items; WoW class code 2 = Weapon; expected ~3K-5K weapon rows.
  Single shallow clone; no rate-limit concern. Wall time < 2 min.

Output:
  - Inserts into weapon_knowledge_entries (INSERT OR IGNORE on source_library, source_url)
  - JSON summary at: agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/summaries/track-J-wow-classic-items.json
"""

import json
import os
import sqlite3
import subprocess
import sys
import logging
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
CLONE_DIR       = Path("/tmp/track-J/wow-classic-items")
DB_PATH         = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
SCHEMA_SQL      = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql")
SUMMARIES_DIR   = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/summaries")
SUMMARY_PATH    = SUMMARIES_DIR / "track-J-wow-classic-items.json"
LOG_PATH        = Path("/tmp/track-J/track_j.log")

# Canonical items file in this repo (confirmed from probe)
ITEMS_FILE_RELATIVE = Path("data/json/data.json")

REPO_URL        = "https://github.com/nexus-devs/wow-classic-items"
SOURCE_LIBRARY  = "wow-classic-items"
LICENSE_CLASS   = "MIT"
GENRE_TAGS      = ["mmo", "wow-classic", "fantasy-warcraft"]
BATCH_SIZE      = 500

# This repo stores class as a string "Weapon" (not numeric code 2).
# Confirmed from data probe: 4,440 items with class="Weapon" in the 38K item list.
WEAPON_CLASS_STRING = "Weapon"

# WoW weapon subclass map (class=2) — used to derive weapon_subclass text
WOW_WEAPON_SUBCLASSES = {
    0:  "One-Handed Axe",
    1:  "Two-Handed Axe",
    2:  "Bow",
    3:  "Gun",
    4:  "One-Handed Mace",
    5:  "Two-Handed Mace",
    6:  "Polearm",
    7:  "One-Handed Sword",
    8:  "Two-Handed Sword",
    9:  "Obsolete",
    10: "Staff",
    11: "One-Handed Exotic",
    12: "Two-Handed Exotic",
    13: "Fist Weapon",
    14: "Miscellaneous",
    15: "Dagger",
    16: "Thrown",
    17: "Spear",
    18: "Crossbow",
    19: "Wand",
    20: "Fishing Pole",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("track-J")

# ---------------------------------------------------------------------------
# Step 1: Shallow clone
# ---------------------------------------------------------------------------
def clone_repo():
    CLONE_DIR.parent.mkdir(parents=True, exist_ok=True)
    if CLONE_DIR.exists():
        log.info("Clone already present at %s — skipping clone.", CLONE_DIR)
        return
    log.info("Shallow-cloning %s → %s", REPO_URL, CLONE_DIR)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, str(CLONE_DIR)],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        log.error("Clone failed: %s", result.stderr)
        sys.exit(1)
    log.info("Clone complete.")

# ---------------------------------------------------------------------------
# Step 2: Locate canonical items JSON
# ---------------------------------------------------------------------------
def locate_items_file() -> Path:
    # Canonical path confirmed from repo probe: data/json/data.json
    # 38,294 items; class field is string "Weapon" (4,440 weapons)
    canonical = CLONE_DIR / ITEMS_FILE_RELATIVE
    if canonical.exists():
        log.info("Found canonical items file: %s", canonical)
        return canonical

    # Legacy fallback candidates
    candidates = [
        CLONE_DIR / "data" / "items.json",
        CLONE_DIR / "data" / "items" / "items.json",
        CLONE_DIR / "items.json",
    ]
    for c in candidates:
        if c.exists():
            log.info("Found fallback items file: %s", c)
            return c

    # Last resort: any JSON with "item" in name under data/
    data_dir = CLONE_DIR / "data"
    if data_dir.exists():
        jsons = sorted(data_dir.rglob("*.json"))
        log.info("Candidate JSON files in data/: %s", [str(j) for j in jsons[:10]])
        for j in jsons:
            if "item" in j.name.lower() or "data" in j.name.lower():
                log.info("Using last-resort items file: %s", j)
                return j

    log.error("Cannot locate items JSON. Files found: %s", list(CLONE_DIR.rglob("*.json"))[:20])
    sys.exit(1)

# ---------------------------------------------------------------------------
# Step 3: Ensure schema applied
# ---------------------------------------------------------------------------
def ensure_schema(conn: sqlite3.Connection):
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='weapon_knowledge_entries'"
    )
    if cur.fetchone():
        log.info("Schema already present — skipping DDL.")
        return
    log.info("Applying schema from %s", SCHEMA_SQL)
    schema_text = SCHEMA_SQL.read_text()
    # SQLite's executescript doesn't support PRAGMA foreign_keys mid-script well;
    # split and execute statement by statement to avoid errors on already-existing refs.
    conn.executescript(schema_text)
    conn.commit()
    log.info("Schema applied.")

# ---------------------------------------------------------------------------
# Step 4: Parse + filter weapons
# ---------------------------------------------------------------------------
def parse_weapons(items_file: Path) -> list[dict]:
    log.info("Loading %s …", items_file)
    raw = json.loads(items_file.read_text())

    # The repo stores items as a list or as a dict keyed by category; probe shape.
    if isinstance(raw, dict):
        # Could be {"items": [...]} or {"Weapon": [...]} etc.
        if "items" in raw:
            items = raw["items"]
        else:
            # Flatten all values if they're lists
            items = []
            for v in raw.values():
                if isinstance(v, list):
                    items.extend(v)
    elif isinstance(raw, list):
        items = raw
    else:
        log.error("Unexpected JSON shape: %s", type(raw))
        sys.exit(1)

    log.info("Total items loaded: %d", len(items))

    # Sample first item to detect field names
    if items:
        log.info("Sample item keys: %s", list(items[0].keys())[:20])

    weapons = []
    skipped_no_class = 0
    skipped_not_weapon = 0

    for item in items:
        # In nexus-devs/wow-classic-items, class is stored as a string: "Weapon", "Armor", etc.
        item_class = (
            item.get("class")
            or item.get("itemClass")
            or item.get("type")
            or item.get("itemType")
        )

        if item_class is None:
            skipped_no_class += 1
            continue

        if str(item_class) != WEAPON_CLASS_STRING:
            skipped_not_weapon += 1
            continue

        weapons.append(item)

    log.info(
        "Weapon filter: %d weapons | %d skipped (no class) | %d skipped (not weapon)",
        len(weapons), skipped_no_class, skipped_not_weapon
    )
    return weapons

# ---------------------------------------------------------------------------
# Step 5: Normalize → weapon_knowledge_entries row
# ---------------------------------------------------------------------------
def normalize_item(item: dict) -> dict | None:
    item_id = item.get("id") or item.get("itemId") or item.get("_id") or item.get("itemID")
    name    = item.get("name") or item.get("itemName") or item.get("displayName")

    if not name:
        return None

    # Source URL: wowhead classic item page (informational; we don't crawl wowhead)
    if item_id:
        source_url = f"https://www.wowhead.com/classic/item={item_id}"
        source_id  = str(item_id)
    else:
        # Use name-slug as fallback
        slug = name.lower().replace(" ", "-").replace("'", "")
        source_url = f"https://www.wowhead.com/classic/search?q={slug}"
        source_id  = slug

    # Description / tooltip
    # In this repo, tooltip is a list of {"label": ..., "format": ...} dicts.
    # Extract label text from tooltip entries that look like flavor text or description.
    raw_tooltip = item.get("tooltip")
    if isinstance(raw_tooltip, list):
        # Flavor text entries often have format "Flavor" or no format; join non-header labels
        tooltip_lines = [
            entry.get("label", "")
            for entry in raw_tooltip
            if isinstance(entry, dict) and entry.get("label")
            and entry.get("format") not in ("alignRight",)
            and entry.get("label") != name  # skip the name label
        ]
        description = " | ".join(filter(None, tooltip_lines))
    else:
        description = (
            item.get("description")
            or str(raw_tooltip or "")
            or item.get("flavorText")
            or item.get("flavor_text")
            or ""
        )

    # Weapon subclass text: in this repo it's already a string e.g. "Mace", "Dagger", "Bow"
    subclass_text = (
        item.get("subclass")
        or item.get("subClass")
        or item.get("itemSubClass")
        or "Unknown"
    )
    # Fallback: if numeric, map via WOW_WEAPON_SUBCLASSES
    if isinstance(subclass_text, int):
        subclass_text = WOW_WEAPON_SUBCLASSES.get(subclass_text, "Unknown")

    # Structured properties: preserve key fields from this repo's schema
    # Confirmed field names from probe: itemId, name, icon, class, subclass,
    # sellPrice, quality, itemLevel, requiredLevel, slot, tooltip, itemLink
    props = {}
    for field in [
        "itemId", "icon", "class", "subclass", "slot",
        "quality", "itemLevel", "requiredLevel", "sellPrice",
        "buyPrice", "stackSize", "maxStack", "unique",
        # Additional fields that may be present in some items
        "damage", "dps", "speed", "attackSpeed",
        "minDamage", "maxDamage",
        "source", "sources",
        "bonuses", "stats", "spells",
        "weight",
    ]:
        if field in item and item[field] is not None:
            props[field] = item[field]

    props["subclass_text"] = subclass_text

    # Build cultural_lineage_tags: genre + any source tags
    culture_tags = list(GENRE_TAGS)

    return {
        "canonical_name":         name,
        "source_library":         SOURCE_LIBRARY,
        "source_url":             source_url,
        "source_id":              source_id,
        "description_text":       description,
        "structured_properties":  json.dumps(props),
        "cultural_lineage_tags":  json.dumps(culture_tags),
        "historical_period":      "fantasy",
        "genre_appearances":      json.dumps(["mmo", "fantasy", "game-specific"]),
        "related_entries":        None,
        "license_class":          LICENSE_CLASS,
    }

# ---------------------------------------------------------------------------
# Step 6: Insert in batches
# ---------------------------------------------------------------------------
def insert_weapons(conn: sqlite3.Connection, rows: list[dict]) -> tuple[int, int]:
    sql = """
        INSERT OR IGNORE INTO weapon_knowledge_entries
            (canonical_name, source_library, source_url, source_id,
             description_text, structured_properties, cultural_lineage_tags,
             historical_period, genre_appearances, related_entries, license_class)
        VALUES
            (:canonical_name, :source_library, :source_url, :source_id,
             :description_text, :structured_properties, :cultural_lineage_tags,
             :historical_period, :genre_appearances, :related_entries, :license_class)
    """
    inserted = 0
    skipped  = 0

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i : i + BATCH_SIZE]
        cur = conn.executemany(sql, batch)
        conn.commit()
        inserted += cur.rowcount
        skipped  += len(batch) - cur.rowcount
        log.info(
            "Batch %d-%d: %d inserted, %d skipped (duplicates)",
            i, min(i + BATCH_SIZE, len(rows)), cur.rowcount, len(batch) - cur.rowcount
        )

    return inserted, skipped

# ---------------------------------------------------------------------------
# Step 7: Write JSON summary artifact
# ---------------------------------------------------------------------------
def write_summary(
    total_raw: int,
    weapon_count: int,
    normalized_count: int,
    inserted: int,
    skipped_dup: int,
    elapsed_s: float,
    items_file: str,
):
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "track":              "J",
        "source_library":     SOURCE_LIBRARY,
        "repo_url":           REPO_URL,
        "license":            LICENSE_CLASS,
        "items_file":         items_file,
        "crawl_date":         datetime.now(timezone.utc).isoformat(),
        "total_items_raw":    total_raw,
        "weapon_class_filter": [WEAPON_CLASS_STRING],
        "weapons_found":      weapon_count,
        "normalized_rows":    normalized_count,
        "inserted":           inserted,
        "skipped_duplicates": skipped_dup,
        "acceptance_floor":   3000,
        "acceptance_met":     inserted >= 3000,
        "elapsed_seconds":    round(elapsed_s, 1),
        "genre_tags":         GENRE_TAGS,
        "log_path":           str(LOG_PATH),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2))
    log.info("Summary written: %s", SUMMARY_PATH)
    return summary

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    t0 = datetime.now(timezone.utc)

    clone_repo()
    items_file = locate_items_file()

    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    ensure_schema(conn)

    weapons_raw = parse_weapons(items_file)
    total_raw   = None  # will be set below after reload for accuracy

    # Re-count total items for summary
    raw_data = json.loads(items_file.read_text())
    if isinstance(raw_data, list):
        total_raw = len(raw_data)
    elif isinstance(raw_data, dict):
        if "items" in raw_data:
            total_raw = len(raw_data["items"])
        else:
            total_raw = sum(len(v) for v in raw_data.values() if isinstance(v, list))
    else:
        total_raw = 0

    # Normalize
    rows = []
    for w in weapons_raw:
        row = normalize_item(w)
        if row:
            rows.append(row)
    log.info("Normalized %d rows from %d weapon items.", len(rows), len(weapons_raw))

    # Insert
    inserted, skipped_dup = insert_weapons(conn, rows)
    conn.close()

    t1     = datetime.now(timezone.utc)
    elapsed = (t1 - t0).total_seconds()

    summary = write_summary(
        total_raw=total_raw,
        weapon_count=len(weapons_raw),
        normalized_count=len(rows),
        inserted=inserted,
        skipped_dup=skipped_dup,
        elapsed_s=elapsed,
        items_file=str(items_file),
    )

    log.info("=" * 60)
    log.info("Track J complete.")
    log.info("  Total items in repo:  %d", summary["total_items_raw"])
    log.info("  Weapons found:        %d", summary["weapons_found"])
    log.info("  Rows inserted:        %d", summary["inserted"])
    log.info("  Acceptance floor 3K:  %s", "PASS" if summary["acceptance_met"] else "FAIL")
    log.info("  Elapsed:              %.1fs", elapsed)

    # Cleanup clone
    log.info("Cleaning up /tmp/track-J/ …")
    import shutil
    shutil.rmtree("/tmp/track-J", ignore_errors=True)
    log.info("Cleanup done.")

    if not summary["acceptance_met"]:
        log.warning(
            "ACCEPTANCE FLOOR NOT MET: inserted=%d < 3000. "
            "Possible causes: weapon class code differs from 2, or repo structure changed. "
            "Inspect log for field-key diagnostic output.",
            inserted
        )
        sys.exit(2)

if __name__ == "__main__":
    main()
