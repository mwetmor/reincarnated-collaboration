#!/usr/bin/env python3
"""
Track I — Cataclysm: Dark Days Ahead weapon import
Legolas / hive-mind weapon-library-import 2026-05-22

CDDA item format note (as of 2026 main branch):
- All items use "type": "ITEM"
- Weapon classification is via "subtypes" array: ["GUN"], ["AMMO"], ["TOOL"], etc.
- Melee weapons live in items/melee/ and items/ranged/ dirs; may lack subtypes but
  have "weapon_category" field or are weapon by directory classification
- There is NO "type": "GUN" / "type": "AMMO" in current codebase

Inclusion criteria:
  (a) subtypes contains "GUN" — firearms
  (b) subtypes contains "AMMO" — ammunition (weapon-adjacent context)
  (c) item is in items/melee/ directory — all melee weapons
  (d) item is in items/ranged/ directory — ranged non-gun weapons
  (e) item has non-empty "weapon_category" field — explicit weapon tagging
  (f) item is in items/gun/ directory with GUN subtype (covered by a)

License: CC-BY-SA-3.0 (per CDDA LICENSE file)
Genre tags: ["modern", "post-apocalyptic", "improvised"]
Target DB: /Users/admin/Games/reincarnated-loadout/data/telemetry.db
Acceptance: >=800 rows inserted with source_library='cataclysm-dda'
"""

import json
import logging
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CLONE_DIR = "/tmp/track-I/cataclysm"
REPO_URL = "https://github.com/CleverRaven/Cataclysm-DDA"
DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = "/tmp/track-I/track_i_cataclysm.log"
SUMMARY_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "legolas/research/weapon-library-import-2026-05-22/summaries/"
    "track-I-cataclysm-summary.json"
)
SOURCE_LIBRARY = "cataclysm-dda"
LICENSE_CLASS = "CC-BY-SA-3.0"
GENRE_APPEARANCES = json.dumps(["modern", "post-apocalyptic", "improvised"])
BATCH_SIZE = 500

# Subtypes that qualify unconditionally
WEAPON_SUBTYPES = {"GUN", "AMMO"}

# Directory names under items/ whose contents are all weapons by classification
WEAPON_DIRS = {"melee", "ranged", "gun"}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

os.makedirs("/tmp/track-I", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("track-I")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_name(item: dict) -> str | None:
    """Extract canonical name from item. Handles str and {str:, str_pl:, str_sp:} shapes."""
    raw = item.get("name")
    if raw is None:
        return None
    if isinstance(raw, str):
        return raw.strip() or None
    if isinstance(raw, dict):
        # prefer str, then str_sp (singular/plural), then str_pl
        name = raw.get("str") or raw.get("str_sp") or raw.get("str_pl") or ""
        return name.strip() or None
    return None


def path_in_weapon_dir(fpath: Path, items_root: Path) -> bool:
    """True if fpath is inside a directory classified as a weapon directory."""
    try:
        rel = fpath.relative_to(items_root)
        parts = rel.parts
        # First part of path relative to items_root is the subdir
        if parts and parts[0] in WEAPON_DIRS:
            return True
    except ValueError:
        pass
    return False


def is_weapon_item(item: dict, fpath: Path, items_root: Path) -> bool:
    """Determine if this item qualifies as a weapon entry."""
    # Check subtypes array
    subs = item.get("subtypes", [])
    if isinstance(subs, str):
        subs = [subs]
    if isinstance(subs, list):
        for s in subs:
            if s in WEAPON_SUBTYPES:
                return True

    # Check directory classification
    if path_in_weapon_dir(fpath, items_root):
        return True

    # Check weapon_category field (explicit weapon tagging)
    wcat = item.get("weapon_category")
    if wcat:  # non-empty list or non-empty string
        if isinstance(wcat, list) and len(wcat) > 0:
            return True
        if isinstance(wcat, str) and wcat.strip():
            return True

    return False


def build_source_url(item_id: str, rel_path: str) -> str:
    """Build a stable per-item URL.

    Multiple items live in each JSON file, so we append the item id as a
    URL fragment to make each URL unique (satisfies the UNIQUE source_url
    constraint in weapon_knowledge_entries).
    """
    return f"https://github.com/CleverRaven/Cataclysm-DDA/blob/main/{rel_path}#{item_id}"


def build_structured_properties(item: dict) -> str:
    """Extract mechanically relevant fields into a JSON blob."""
    fields = [
        "subtypes", "weapon_category",
        "damage", "range", "dispersion", "recoil", "loudness",
        "weight", "volume", "length", "longest_side",
        "material", "skill", "ammo", "ammo_type", "flags",
        "bashing", "cutting", "pierce", "to_hit", "clip_size",
        "reload", "modes", "durability", "price", "price_postapoc",
        "techniques", "qualities",
    ]
    props = {k: item[k] for k in fields if k in item}
    return json.dumps(props, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Clone
# ---------------------------------------------------------------------------

def clone_repo() -> None:
    if os.path.isdir(CLONE_DIR) and os.listdir(CLONE_DIR):
        log.info("Clone dir already exists at %s — skipping clone.", CLONE_DIR)
        return
    os.makedirs("/tmp/track-I", exist_ok=True)
    log.info("Cloning %s (shallow)...", REPO_URL)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, CLONE_DIR],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log.error("Clone failed:\n%s", result.stderr)
        sys.exit(1)
    log.info("Clone complete.")


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------

def parse_items(items_root: Path, clone_root: Path) -> list[dict]:
    """Walk items_root; parse all JSON arrays; filter to weapon items."""
    results = []
    seen_ids = set()  # deduplicate by source_id within this run
    files_scanned = 0
    parse_errors = 0
    skipped_no_name = 0
    skipped_no_id = 0
    duplicates = 0

    for dirpath, _dirs, filenames in os.walk(items_root):
        for fname in sorted(filenames):
            if not fname.endswith(".json"):
                continue
            fpath = Path(dirpath) / fname
            files_scanned += 1
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as exc:
                log.warning("Parse error %s: %s", fpath, exc)
                parse_errors += 1
                continue

            # CDDA JSON files are either a list of items or a single item dict
            if isinstance(data, dict):
                data = [data]
            if not isinstance(data, list):
                continue

            rel_path = str(fpath.relative_to(clone_root)).replace("\\", "/")
            for item in data:
                if not isinstance(item, dict):
                    continue
                if not is_weapon_item(item, fpath, items_root):
                    continue
                item_id = item.get("id")
                if not item_id:
                    # Some items use "abstract" as id (template base items)
                    item_id = item.get("abstract")
                if not item_id:
                    skipped_no_id += 1
                    continue
                # Deduplicate within parse run
                if item_id in seen_ids:
                    duplicates += 1
                    continue
                seen_ids.add(item_id)
                name = extract_name(item)
                if not name:
                    # Use id as fallback name if no name field (abstract base items)
                    name = str(item_id).replace("_", " ").strip()
                if not name:
                    skipped_no_name += 1
                    continue
                # description may be a dict {str:..., //~:...} or a plain string
                raw_desc = item.get("description", "")
                if isinstance(raw_desc, dict):
                    raw_desc = raw_desc.get("str", "")
                results.append({
                    "canonical_name": name,
                    "source_library": SOURCE_LIBRARY,
                    "source_url": build_source_url(item_id, rel_path),
                    "source_id": item_id,
                    "description_text": raw_desc or "",
                    "structured_properties": build_structured_properties(item),
                    "genre_appearances": GENRE_APPEARANCES,
                    "license_class": LICENSE_CLASS,
                })

    log.info(
        "Scanned %d files; parse errors: %d; weapon items: %d; "
        "dupes: %d; skipped (no id): %d; skipped (no name): %d",
        files_scanned, parse_errors, len(results),
        duplicates, skipped_no_id, skipped_no_name,
    )
    return results


# ---------------------------------------------------------------------------
# Insert
# ---------------------------------------------------------------------------

def insert_rows(rows: list[dict], db_path: str) -> int:
    """INSERT OR IGNORE rows into weapon_knowledge_entries. Returns total count in DB."""
    con = sqlite3.connect(db_path, timeout=30)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")

    sql = """
        INSERT OR IGNORE INTO weapon_knowledge_entries
            (canonical_name, source_library, source_url, source_id,
             description_text, structured_properties,
             genre_appearances, license_class)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    batch_num = 0
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i : i + BATCH_SIZE]
        params = [
            (
                row["canonical_name"],
                row["source_library"],
                row["source_url"],
                row["source_id"],
                row["description_text"],
                row["structured_properties"],
                row["genre_appearances"],
                row["license_class"],
            )
            for row in batch
        ]
        cur = con.executemany(sql, params)
        con.commit()
        batch_num += 1
        log.info("Batch %d: %d rows attempted, %d inserted.",
                 batch_num, len(batch), cur.rowcount)

    total_in_db = con.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library=?",
        (SOURCE_LIBRARY,)
    ).fetchone()[0]
    con.close()
    log.info("Total cataclysm-dda rows now in DB: %d", total_in_db)
    return total_in_db


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def write_summary(
    rows_parsed: int,
    rows_in_db: int,
    start_ts: str,
    end_ts: str,
    duration_s: float,
) -> None:
    summary = {
        "track": "I",
        "source": "cataclysm-dda",
        "source_url": REPO_URL,
        "license": LICENSE_CLASS,
        "genre_tags": ["modern", "post-apocalyptic", "improvised"],
        "run_start": start_ts,
        "run_end": end_ts,
        "duration_seconds": round(duration_s, 1),
        "rows_parsed": rows_parsed,
        "rows_in_db": rows_in_db,
        "acceptance_floor": 800,
        "acceptance_met": rows_in_db >= 800,
        "db_path": DB_PATH,
        "log_path": LOG_PATH,
        "script_path": (
            "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
            "legolas/research/weapon-library-import-2026-05-22/scripts/track_i_cataclysm.py"
        ),
        "math_note_path": (
            "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
            "legolas/research/weapon-library-import-2026-05-22/track-I-math-note.md"
        ),
    }
    os.makedirs(os.path.dirname(SUMMARY_PATH), exist_ok=True)
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    log.info("Summary written to %s", SUMMARY_PATH)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    t0 = time.time()
    start_ts = datetime.now(timezone.utc).isoformat()
    log.info("=== Track I: Cataclysm DDA import starting ===")

    # 1. Clone (skip if already present from prior attempt)
    clone_repo()

    # 2. Parse
    clone_root = Path(CLONE_DIR)
    items_root = clone_root / "data" / "json" / "items"
    if not items_root.is_dir():
        log.error("items dir not found at %s", items_root)
        sys.exit(1)

    rows = parse_items(items_root, clone_root)
    log.info("Total weapon items parsed: %d", len(rows))

    if not rows:
        log.error("No weapon items found — aborting before DB insert.")
        sys.exit(1)

    # 3. Insert
    rows_in_db = insert_rows(rows, DB_PATH)

    # 4. Cleanup
    log.info("Cleaning up clone at %s ...", CLONE_DIR)
    try:
        shutil.rmtree("/tmp/track-I")
        log.info("Cleanup complete.")
    except Exception as exc:
        log.warning("Cleanup failed (non-fatal): %s", exc)

    # 5. Summary
    t1 = time.time()
    end_ts = datetime.now(timezone.utc).isoformat()
    write_summary(len(rows), rows_in_db, start_ts, end_ts, t1 - t0)

    # 6. Final verdict
    if rows_in_db >= 800:
        log.info("PASS — %d rows in DB (>= 800 floor).", rows_in_db)
    else:
        log.error("FAIL — only %d rows in DB (< 800 floor).", rows_in_db)
        sys.exit(2)

    log.info("=== Track I complete ===")


if __name__ == "__main__":
    main()
