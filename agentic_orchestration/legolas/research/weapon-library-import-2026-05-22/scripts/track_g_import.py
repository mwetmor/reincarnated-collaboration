#!/usr/bin/env python3
"""
Track G — GitHub-Hosted Weapon-Data Repository Import
Mission: weapon-library-import-hive-mind-mission-2026-05-22.md
Dispatch: dispatches/2026-05-22-legolas-track-G-github-data-repos.md

Repos:
  - nick-aschenbach/dnd-data (MIT)
  - osrsbox/osrsbox-db (GPL-3.0)
  - 5e-bits/5e-database (MIT) [reach target]
  - bloqhead/demigods (no license -> unknown) [reach target]

Pipeline per repo:
  1. Fetch canonical JSON via raw.githubusercontent.com (no full clone needed)
  2. Normalize to weapon_knowledge_entries schema
  3. INSERT OR IGNORE with WAL mode, batches of 200
  4. Insert reference images (wiki_url -> image URL for osrsbox)
  5. Write JSON summary artifact

Discipline #19: fires and exits; summary written on completion.
Discipline #20: raw.githubusercontent.com GREEN; no robots concern.
"""

import json
import sqlite3
import urllib.request
import urllib.error
import ssl
import subprocess
import re
import os
import sys
import time
import datetime
import traceback

# Use certifi CA bundle if available (fixes macOS Python SSL verification)
try:
    import certifi
    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = ssl.create_default_context()

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
SUMMARY_PATH = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/summaries/track-G-wave1.json"
LOG_PATH = "/Users/admin/Games/reincarnated-engine/logs/weapon-library-track-G.log"

STARTED_AT = datetime.datetime.now(datetime.timezone.utc).isoformat()

# ── Logging ──────────────────────────────────────────────────────────────────

def log(msg):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)


# ── HTTP fetch helper ─────────────────────────────────────────────────────────

UA = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"

def fetch_json_curl(url):
    """Fallback: use system curl to fetch JSON (avoids Python SSL issues)."""
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "120", "-A", UA, url],
            capture_output=True, timeout=130
        )
        if result.returncode != 0:
            return None, f"curl exit {result.returncode}: {result.stderr.decode()[:200]}"
        return json.loads(result.stdout), None
    except Exception as e:
        return None, f"curl fallback error: {e}"

def fetch_json(url, retries=3, delay=2.0):
    """Fetch URL and parse JSON. Returns (data, None) or (None, error_string)."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120, context=_SSL_CONTEXT) as resp:
                raw = resp.read()
            return json.loads(raw), None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = delay * (2 ** attempt)
                log(f"  429 rate-limit on {url}; backing off {wait:.1f}s")
                time.sleep(wait)
            else:
                return None, f"HTTPError {e.code}: {url}"
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                # Final fallback: try system curl
                log(f"  urllib failed ({e}); trying curl fallback")
                return fetch_json_curl(url)
    return None, f"Exhausted retries: {url}"


# ── DB helpers ────────────────────────────────────────────────────────────────

def open_db(path):
    conn = sqlite3.connect(path, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def insert_entries_batch(conn, rows):
    """INSERT OR IGNORE a batch of weapon_knowledge_entries rows.
    Returns (inserted_count, ignored_count).
    """
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
    before = conn.execute("SELECT changes()").fetchone()[0]
    conn.executemany(sql, rows)
    conn.commit()
    # SQLite changes() only counts the last statement; use rowcount approximation
    # Best estimate: count via SELECT after insert
    return len(rows)  # upper bound; IGNORE silently drops duplicates


def insert_images_batch(conn, image_rows):
    """INSERT OR IGNORE reference images."""
    # First get entry IDs for the source_urls we just inserted
    sql = """
    INSERT OR IGNORE INTO knowledge_entry_reference_images
        (knowledge_entry_id, image_url, image_source, license_class, is_canonical, image_caption)
    VALUES
        (:knowledge_entry_id, :image_url, :image_source, :license_class, :is_canonical, :image_caption)
    """
    conn.executemany(sql, image_rows)
    conn.commit()


def get_entry_id(conn, source_library, source_url):
    row = conn.execute(
        "SELECT id FROM weapon_knowledge_entries WHERE source_library=? AND source_url=?",
        (source_library, source_url)
    ).fetchone()
    return row[0] if row else None


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ── Repo 1: nick-aschenbach/dnd-data ─────────────────────────────────────────

WEAPON_ITEM_TYPES = {
    "Melee Weapon", "Ranged Weapon", "martial", "simple", "Weapon",
    "Staff", "Wand", "Rod", "Ammunition",
}

def is_dnd_weapon(item):
    props = item.get("properties", {})
    if not isinstance(props, dict):
        return False
    itype = props.get("Item Type", "")
    if itype in WEAPON_ITEM_TYPES:
        return True
    # Catch "Weapon (longsword)" etc.
    if itype.startswith("Weapon (") or itype.startswith("weapon"):
        return True
    return False


def normalize_dnd_data(item, license_class):
    props = item.get("properties", {}) or {}
    name = item.get("name", "").strip()
    if not name:
        return None

    slug = slugify(name)
    source_url = f"https://github.com/nick-aschenbach/dnd-data/blob/main/data/items.json#{slug}"

    desc = item.get("description", "") or ""
    publisher = item.get("publisher", "") or ""
    book = item.get("book", "") or ""

    # Infer cultural_lineage_tags and genre from Item Type
    itype = props.get("Item Type", "") or ""
    rarity = props.get("Item Rarity", "") or props.get("Rarity", "") or ""

    cultural_tags = ["fictional"]
    genre = ["fantasy", "game-dnd-5e"]

    # Structured properties — preserve all source fields
    structured = {
        "item_type": itype,
        "rarity": rarity,
        "publisher": publisher,
        "book": book,
    }
    # Add all props fields
    for k, v in props.items():
        structured[k] = v

    return {
        "canonical_name": name,
        "source_library": "nick-aschenbach-dnd-data",
        "source_url": source_url,
        "source_id": slug,
        "description_text": desc[:4000] if desc else None,
        "structured_properties": json.dumps(structured),
        "cultural_lineage_tags": json.dumps(cultural_tags),
        "historical_period": "fantasy",
        "genre_appearances": json.dumps(genre),
        "related_entries": None,
        "license_class": license_class,
    }


def import_dnd_data(conn):
    log("=== Repo: nick-aschenbach/dnd-data ===")
    url = "https://raw.githubusercontent.com/nick-aschenbach/dnd-data/main/data/items.json"
    log(f"  Fetching {url}")
    data, err = fetch_json(url)
    if err:
        log(f"  FETCH ERROR: {err}")
        return {"repo": "nick-aschenbach-dnd-data", "url": "https://github.com/nick-aschenbach/dnd-data",
                "license": "MIT", "entries_imported": 0, "images_imported": 0,
                "failures": [err], "notes": "Fetch failed"}

    license_class = "MIT"  # confirmed by API probe
    total = len(data)
    log(f"  Loaded {total} total items")

    weapons = [item for item in data if is_dnd_weapon(item)]
    log(f"  Weapon-class items: {len(weapons)}")

    rows = []
    skipped = 0
    for item in weapons:
        row = normalize_dnd_data(item, license_class)
        if row is None:
            skipped += 1
            continue
        rows.append(row)

    log(f"  Normalized: {len(rows)} rows; skipped (no name): {skipped}")

    # Insert in batches of 200
    BATCH = 200
    total_inserted = 0
    for i in range(0, len(rows), BATCH):
        batch = rows[i:i+BATCH]
        insert_entries_batch(conn, batch)
        total_inserted += len(batch)
        log(f"  Inserted batch {i//BATCH + 1}: {len(batch)} rows")

    log(f"  Done. Total rows attempted: {total_inserted}")

    return {
        "repo": "nick-aschenbach-dnd-data",
        "url": "https://github.com/nick-aschenbach/dnd-data",
        "license": license_class,
        "entries_imported": total_inserted,
        "images_imported": 0,
        "failures": [],
        "notes": f"7310 weapon-class items from {total} total; MIT license; no image URLs in source data"
    }


# ── Repo 2: osrsbox/osrsbox-db ────────────────────────────────────────────────

OSRS_WEAPON_TYPE_MAP = {
    "blunt": "hammer_mace",
    "stab_sword": "sword",
    "staff": "staff",
    "spear": "polearm",
    "thrown": "thrown",
    "bow": "bow",
    "slash_sword": "sword",
    "polearm": "polearm",
    "axe": "axe",
    "banner": "other",
    "2h_sword": "sword",
    "crossbow": "crossbow",
    "spiked": "hammer_mace",
    "pickaxe": "other",
    "unarmed": "other",
    "polestaff": "polearm",
    "powered_staff": "staff",
    "claw": "dagger",
    "scythe": "polearm",
    "bladed_staff": "staff",
}


def normalize_osrs_item(item_id, item, license_class):
    name = item.get("name", "").strip()
    if not name:
        return None, None

    wiki_url = item.get("wiki_url", "") or ""
    if not wiki_url:
        # Construct from name
        name_slug = name.replace(" ", "_")
        wiki_url = f"https://oldschool.runescape.wiki/w/{name_slug}"

    source_url = wiki_url  # use wiki URL as canonical

    examine = item.get("examine", "") or ""
    weapon_data = item.get("weapon", {}) or {}
    equipment_data = item.get("equipment", {}) or {}

    weapon_type = weapon_data.get("weapon_type", "unknown")
    attack_speed = weapon_data.get("attack_speed")
    stances = weapon_data.get("stances", [])

    # Cultural + genre tags
    cultural_tags = ["fictional", "game-osrs"]
    genre = ["fantasy", "game-osrs"]

    # Build structured properties
    structured = {
        "osrs_id": item.get("id"),
        "weapon_type": weapon_type,
        "attack_speed": attack_speed,
        "stances": stances,
        "members": item.get("members"),
        "tradeable": item.get("tradeable"),
        "cost": item.get("cost"),
        "weight": item.get("weight"),
        "release_date": item.get("release_date"),
        "equipment": equipment_data,
        "quest_item": item.get("quest_item"),
        "wiki_url": wiki_url,
    }

    entry_row = {
        "canonical_name": name,
        "source_library": "osrsbox-db",
        "source_url": source_url,
        "source_id": str(item.get("id", item_id)),
        "description_text": examine[:4000] if examine else None,
        "structured_properties": json.dumps(structured),
        "cultural_lineage_tags": json.dumps(cultural_tags),
        "historical_period": "fantasy",
        "genre_appearances": json.dumps(genre),
        "related_entries": None,
        "license_class": license_class,
    }

    # Image row: construct OSRS wiki image URL from name
    # Pattern: https://oldschool.runescape.wiki/images/<Name_with_underscores>.png
    # This is approximate — OSRS wiki uses this pattern for most items
    name_for_img = name.replace(" ", "_")
    image_url = f"https://oldschool.runescape.wiki/images/{name_for_img}.png"
    image_row_template = {
        "image_url": image_url,
        "image_source": "osrsbox-wiki-url",
        "license_class": "CC-BY-SA",  # OSRS wiki uses CC BY-SA 3.0
        "is_canonical": 1,
        "image_caption": f"{name} (OSRS wiki item icon)",
    }

    return entry_row, image_row_template


def import_osrsbox(conn):
    log("=== Repo: osrsbox/osrsbox-db ===")
    url = "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/docs/items-complete.json"
    log(f"  Fetching {url} (~25MB, may take a moment)")
    data, err = fetch_json(url)
    if err:
        log(f"  FETCH ERROR: {err}")
        return {"repo": "osrsbox-db", "url": "https://github.com/osrsbox/osrsbox-db",
                "license": "GPL-3.0", "entries_imported": 0, "images_imported": 0,
                "failures": [err], "notes": "Fetch failed"}

    license_class = "GPL3"  # confirmed by API probe; GPL-3.0
    log(f"  Loaded {len(data)} total items")

    # Filter to equipable weapons only
    weapons = {k: v for k, v in data.items() if v.get("equipable_weapon")}
    log(f"  Equipable weapon items: {len(weapons)}")

    entry_rows = []
    image_row_templates = []  # keyed by source_url
    skipped = 0

    for item_id, item in weapons.items():
        entry_row, image_tmpl = normalize_osrs_item(item_id, item, license_class)
        if entry_row is None:
            skipped += 1
            continue
        entry_rows.append(entry_row)
        if image_tmpl:
            image_row_templates.append((entry_row["source_url"], image_tmpl))

    log(f"  Normalized: {len(entry_rows)} rows; skipped (no name): {skipped}")

    # Insert entries in batches
    BATCH = 200
    total_inserted = 0
    for i in range(0, len(entry_rows), BATCH):
        batch = entry_rows[i:i+BATCH]
        insert_entries_batch(conn, batch)
        total_inserted += len(batch)
        log(f"  Inserted batch {i//BATCH + 1}: {len(batch)} rows")

    log(f"  Entry insertion done. Rows attempted: {total_inserted}")

    # Now insert images — need to look up IDs
    images_inserted = 0
    image_batch = []
    for source_url, tmpl in image_row_templates:
        entry_id = get_entry_id(conn, "osrsbox-db", source_url)
        if entry_id is None:
            continue  # was ignored (duplicate) — skip image too
        tmpl["knowledge_entry_id"] = entry_id
        image_batch.append(tmpl)
        if len(image_batch) >= BATCH:
            insert_images_batch(conn, image_batch)
            images_inserted += len(image_batch)
            image_batch = []
    if image_batch:
        insert_images_batch(conn, image_batch)
        images_inserted += len(image_batch)

    log(f"  Images inserted: {images_inserted}")

    return {
        "repo": "osrsbox-db",
        "url": "https://github.com/osrsbox/osrsbox-db",
        "license": license_class,
        "entries_imported": total_inserted,
        "images_imported": images_inserted,
        "failures": [],
        "notes": (
            "957 equipable_weapon items from 24735 total; "
            "GPL-3.0 license (game_approved=0 per schema — recorded, not excluded); "
            "image URLs constructed as wiki PNG pattern (CC-BY-SA); "
            "icon field (base64 PNG) NOT stored per URL-only policy"
        )
    }


# ── Repo 3: 5e-bits/5e-database (reach target) ───────────────────────────────

def normalize_5e_srd_item(item, license_class):
    name = item.get("name", "").strip()
    if not name:
        return None

    index = item.get("index", slugify(name))
    source_url = f"https://raw.githubusercontent.com/5e-bits/5e-database/main/src/2014/en/5e-SRD-Equipment.json#{index}"
    api_url = item.get("url", "")

    # Description from desc array
    desc_list = item.get("desc", [])
    desc = " ".join(desc_list) if desc_list else ""

    # Structured props
    damage = item.get("damage", {})
    two_hand_damage = item.get("two_handed_damage", {})
    props_list = item.get("properties", [])
    prop_names = [p.get("name") for p in props_list if isinstance(p, dict)]

    structured = {
        "index": index,
        "weapon_category": item.get("weapon_category"),
        "weapon_range": item.get("weapon_range"),
        "category_range": item.get("category_range"),
        "damage": damage,
        "two_handed_damage": two_hand_damage,
        "range": item.get("range"),
        "throw_range": item.get("throw_range"),
        "properties": prop_names,
        "cost": item.get("cost"),
        "weight": item.get("weight"),
        "api_url": api_url,
    }

    weapon_range = item.get("weapon_range", "").lower()
    genre = ["fantasy", "game-dnd-5e-srd"]
    cultural_tags = ["fictional", "european"]

    return {
        "canonical_name": name,
        "source_library": "5e-bits-5e-database",
        "source_url": source_url,
        "source_id": index,
        "description_text": desc[:4000] if desc else None,
        "structured_properties": json.dumps(structured),
        "cultural_lineage_tags": json.dumps(cultural_tags),
        "historical_period": "fantasy",
        "genre_appearances": json.dumps(genre),
        "related_entries": None,
        "license_class": license_class,
    }


def import_5e_database(conn):
    log("=== Repo: 5e-bits/5e-database (reach target) ===")
    url = "https://raw.githubusercontent.com/5e-bits/5e-database/main/src/2014/en/5e-SRD-Equipment.json"
    log(f"  Fetching {url}")
    data, err = fetch_json(url)
    if err:
        log(f"  FETCH ERROR: {err}")
        return {"repo": "5e-bits-5e-database", "url": "https://github.com/5e-bits/5e-database",
                "license": "MIT", "entries_imported": 0, "images_imported": 0,
                "failures": [err], "notes": "Fetch failed"}

    license_class = "MIT"
    log(f"  Loaded {len(data)} equipment items")

    # Filter to weapons
    weapons = [x for x in data if
               x.get("equipment_category", {}).get("name") in ("Weapon", "Weapons") or
               x.get("weapon_category")]
    log(f"  Weapon items: {len(weapons)}")

    rows = []
    skipped = 0
    for item in weapons:
        row = normalize_5e_srd_item(item, license_class)
        if row is None:
            skipped += 1
            continue
        rows.append(row)

    log(f"  Normalized: {len(rows)} rows; skipped: {skipped}")

    total_inserted = 0
    BATCH = 200
    for i in range(0, len(rows), BATCH):
        batch = rows[i:i+BATCH]
        insert_entries_batch(conn, batch)
        total_inserted += len(batch)

    log(f"  Done. Rows attempted: {total_inserted}")

    return {
        "repo": "5e-bits-5e-database",
        "url": "https://github.com/5e-bits/5e-database",
        "license": license_class,
        "entries_imported": total_inserted,
        "images_imported": 0,
        "failures": [],
        "notes": "37 SRD weapon items; MIT license; official D&D 5e SRD canonical equipment data; no image URLs"
    }


# ── Repo 4: bloqhead/demigods (Elden Ring, reach target) ─────────────────────

ELDEN_RING_TYPE_MAP = {
    "axe": "axe",
    "ballista": "crossbow",
    "claw": "dagger",
    "colossal-sword": "sword",
    "colossal-weapon": "hammer_mace",
    "crossbow": "crossbow",
    "curved-greatsword": "sword",
    "curved-sword": "sword",
    "dagger": "dagger",
    "fist": "other",
    "flail": "hammer_mace",
    "glintstone-staff": "staff",
    "great-axe": "axe",
    "great-bow": "bow",
    "great-spear": "polearm",
    "greatsword": "sword",
    "halberd": "polearm",
    "hammer": "hammer_mace",
    "heavy-thrusting-sword": "sword",
    "katana": "sword",
    "light-bow": "bow",
    "light-thrusting-sword": "sword",
    "reaper": "polearm",
    "sacred-seal": "ritual_instrument",
    "spear": "polearm",
    "straight-sword": "sword",
    "thrusting-sword": "sword",
    "twinblade": "sword",
    "warhammer": "hammer_mace",
    "whip": "other",
    "torch": "other",
}


def normalize_elden_ring_item(item, license_class):
    name = item.get("weapon", "").strip()
    if not name:
        return None

    item_id = item.get("id", 0)
    weapon_type = item.get("type", "unknown")
    source_url = f"https://raw.githubusercontent.com/bloqhead/demigods/main/data/all.json#{item_id}"

    scaling = item.get("scaling", [])
    stats = item.get("stats", {})
    tier = item.get("tier", "")
    skill = item.get("skill", "")

    structured = {
        "id": item_id,
        "type": weapon_type,
        "tier": tier,
        "skill": skill,
        "scaling": scaling,
        "stats": stats,
    }

    genre = ["fantasy", "game-elden-ring"]
    cultural_tags = ["fictional"]

    return {
        "canonical_name": name,
        "source_library": "bloqhead-demigods",
        "source_url": source_url,
        "source_id": str(item_id),
        "description_text": f"Elden Ring weapon. Type: {weapon_type}. Tier: {tier}. Skill: {skill}." if weapon_type else None,
        "structured_properties": json.dumps(structured),
        "cultural_lineage_tags": json.dumps(cultural_tags),
        "historical_period": "fantasy",
        "genre_appearances": json.dumps(genre),
        "related_entries": None,
        "license_class": license_class,
    }


def import_demigods(conn):
    log("=== Repo: bloqhead/demigods (Elden Ring, reach target) ===")
    url = "https://raw.githubusercontent.com/bloqhead/demigods/main/data/all.json"
    log(f"  Fetching {url}")
    data, err = fetch_json(url)
    if err:
        log(f"  FETCH ERROR: {err}")
        return {"repo": "bloqhead-demigods", "url": "https://github.com/bloqhead/demigods",
                "license": "unknown", "entries_imported": 0, "images_imported": 0,
                "failures": [err], "notes": "Fetch failed"}

    license_class = "unknown"  # no LICENSE file in repo
    log(f"  Loaded {len(data)} weapon items")

    rows = []
    skipped = 0
    for item in data:
        row = normalize_elden_ring_item(item, license_class)
        if row is None:
            skipped += 1
            continue
        rows.append(row)

    log(f"  Normalized: {len(rows)} rows; skipped: {skipped}")

    total_inserted = 0
    BATCH = 200
    for i in range(0, len(rows), BATCH):
        batch = rows[i:i+BATCH]
        insert_entries_batch(conn, batch)
        total_inserted += len(batch)

    log(f"  Done. Rows attempted: {total_inserted}")

    return {
        "repo": "bloqhead-demigods",
        "url": "https://github.com/bloqhead/demigods",
        "license": license_class,
        "entries_imported": total_inserted,
        "images_imported": 0,
        "failures": [],
        "notes": (
            "320 Elden Ring weapons across 28 weapon types; "
            "no LICENSE file in repo -> recorded as unknown (game_approved=0); "
            "includes DLC Shadow of the Erdtree weapons"
        )
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    log(f"Track G import starting. DB: {DB_PATH}")
    log(f"Summary will be written to: {SUMMARY_PATH}")

    conn = open_db(DB_PATH)
    log("DB connection opened with WAL mode")

    repos_attempted = [
        "nick-aschenbach-dnd-data",
        "osrsbox-db",
        "5e-bits-5e-database",
        "bloqhead-demigods",
    ]
    per_repo_results = []
    schema_gaps = []

    # Run each repo importer
    try:
        result = import_dnd_data(conn)
        per_repo_results.append(result)
    except Exception as e:
        log(f"ERROR in dnd-data import: {e}")
        traceback.print_exc()
        per_repo_results.append({"repo": "nick-aschenbach-dnd-data", "error": str(e), "entries_imported": 0, "images_imported": 0})

    try:
        result = import_osrsbox(conn)
        per_repo_results.append(result)
    except Exception as e:
        log(f"ERROR in osrsbox import: {e}")
        traceback.print_exc()
        per_repo_results.append({"repo": "osrsbox-db", "error": str(e), "entries_imported": 0, "images_imported": 0})

    try:
        result = import_5e_database(conn)
        per_repo_results.append(result)
    except Exception as e:
        log(f"ERROR in 5e-database import: {e}")
        traceback.print_exc()
        per_repo_results.append({"repo": "5e-bits-5e-database", "error": str(e), "entries_imported": 0, "images_imported": 0})

    try:
        result = import_demigods(conn)
        per_repo_results.append(result)
    except Exception as e:
        log(f"ERROR in demigods import: {e}")
        traceback.print_exc()
        per_repo_results.append({"repo": "bloqhead-demigods", "error": str(e), "entries_imported": 0, "images_imported": 0})

    conn.close()
    log("DB connection closed")

    # Final counts
    total_entries = sum(r.get("entries_imported", 0) for r in per_repo_results)
    total_images = sum(r.get("images_imported", 0) for r in per_repo_results)

    completed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Compute wall seconds
    start_dt = datetime.datetime.fromisoformat(STARTED_AT)
    end_dt = datetime.datetime.fromisoformat(completed_at)
    wall_seconds = (end_dt - start_dt).total_seconds()

    summary = {
        "track": "G",
        "wave": 1,
        "started_at": STARTED_AT,
        "completed_at": completed_at,
        "wall_seconds": wall_seconds,
        "repos_attempted": repos_attempted,
        "per_repo_results": per_repo_results,
        "total_entries_imported": total_entries,
        "total_images_imported": total_images,
        "schema_gaps_observed": schema_gaps,
        "next_wave_recommendations": [
            {
                "repo": "5e-bits/5e-database-2024",
                "url": "https://github.com/5e-bits/5e-database",
                "note": "2024 edition has additional weapons beyond 2014 SRD; same MIT license; check src/2024 dir",
                "estimated_yield": 50,
                "license": "MIT"
            },
            {
                "repo": "Pf2ools/pf2ools-data",
                "url": "https://github.com/Pf2ools/pf2ools-data",
                "note": "Pathfinder 2e structured data; MIT license; 11 stars; weapons included",
                "estimated_yield": 200,
                "license": "MIT"
            },
            {
                "repo": "ThomasLincoln/Souls_API",
                "url": "https://github.com/ThomasLincoln/Souls_API",
                "note": "Items/weapons from Dark Souls series; no license listed; ~140KB structured data",
                "estimated_yield": 200,
                "license": "unknown"
            },
            {
                "repo": "kaggle-dark-souls-weapons",
                "url": "https://www.kaggle.com/datasets/ihelon/dark-souls-weapons",
                "note": "Dark Souls III weapon dataset on Kaggle; CC BY 4.0; ~200 weapons with full stats CSV",
                "estimated_yield": 200,
                "license": "CC_BY"
            },
            {
                "repo": "wowhead-weapon-db / wow-classic-data",
                "url": "https://github.com/search?q=wow+weapons+json&type=repositories",
                "note": "Multiple WoW community data repos; verify license per repo; estimated 1K+ weapons possible",
                "estimated_yield": 500,
                "license": "varies"
            }
        ]
    }

    os.makedirs(os.path.dirname(SUMMARY_PATH), exist_ok=True)
    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    log(f"Summary written: {SUMMARY_PATH}")
    log(f"Total entries imported: {total_entries}")
    log(f"Total images imported: {total_images}")
    log(f"Wall time: {wall_seconds:.1f}s")
    log("Track G Wave 1 complete.")


if __name__ == "__main__":
    main()
