#!/usr/bin/env python3
"""
Track K — Multi-ARPG / Open-World Weapon Data Bundle
Mission: weapon-library-import-hive-mind-mission-2026-05-22.md
Dispatch: dispatches/2026-05-22-legolas-track-K-poe-repoe-eldenring-extras.md

Sources:
  - brather1ng/RePoE          → source_library: path-of-exile-repoe  (MIT)
  - deliton/eldenring-api     → source_library: elden-ring-erdb       (MIT, deliton fallback)
  - blizzhackers/d2data       → source_library: diablo2-d2data        (MIT)
  - DurtyFree/gta-v-data-dumps → source_library: gta-v-data           (no explicit license → 'unknown')

All data fetched via raw.githubusercontent.com (no clones needed for JSON files).
INSERT OR IGNORE against (source_library, source_url) unique key.
Batch size: 500.

Discipline #19: fires and exits; summary written on completion.
Discipline #20: raw.githubusercontent.com GREEN (no robots.txt restriction).
Discipline #1: math note authored prior to script.
"""

import json
import sqlite3
import urllib.request
import urllib.error
import ssl
import subprocess
import os
import sys
import time
import datetime
import traceback

# SSL context (certifi if available)
try:
    import certifi
    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = ssl.create_default_context()

# ── Paths ─────────────────────────────────────────────────────────────────────

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
SUMMARY_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "legolas/research/weapon-library-import-2026-05-22/summaries/track-K-wave1.json"
)
LOG_PATH = "/Users/admin/Games/reincarnated-engine/logs/weapon-library-track-K.log"

STARTED_AT = datetime.datetime.now(datetime.timezone.utc).isoformat()

UA = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"

# ── Logging ───────────────────────────────────────────────────────────────────

_log_fh = None

def _open_log():
    global _log_fh
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    _log_fh = open(LOG_PATH, "a", buffering=1)

def log(msg):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    if _log_fh:
        _log_fh.write(line + "\n")
        _log_fh.flush()

# ── HTTP helpers ──────────────────────────────────────────────────────────────

def fetch_json_curl(url):
    """Fallback: curl-based fetch."""
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "120", "-A", UA, url],
            capture_output=True, timeout=130,
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
                log(f"  429 rate-limit on {url}, backing off {wait:.1f}s")
                time.sleep(wait)
                continue
            return None, f"HTTP {e.code}: {e.reason} on {url}"
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            # Try curl fallback
            log(f"  urllib failed ({e}), trying curl fallback...")
            return fetch_json_curl(url)
    return None, f"All {retries} retries failed on {url}"

# ── DB helpers ────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def insert_batch(conn, rows):
    """INSERT OR IGNORE a batch of rows into weapon_knowledge_entries."""
    sql = """
        INSERT OR IGNORE INTO weapon_knowledge_entries
            (canonical_name, source_library, source_url, source_id,
             description_text, structured_properties,
             cultural_lineage_tags, historical_period, genre_appearances,
             related_entries, license_class)
        VALUES
            (:canonical_name, :source_library, :source_url, :source_id,
             :description_text, :structured_properties,
             :cultural_lineage_tags, :historical_period, :genre_appearances,
             :related_entries, :license_class)
    """
    with conn:
        conn.executemany(sql, rows)

def count_source(conn, source_library):
    cur = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library=?",
        (source_library,),
    )
    return cur.fetchone()[0]

# ── Normalization helpers ─────────────────────────────────────────────────────

def make_row(
    canonical_name, source_library, source_url, source_id=None,
    description_text=None, structured_properties=None,
    cultural_lineage_tags=None, historical_period=None,
    genre_appearances=None, related_entries=None, license_class=None,
):
    return {
        "canonical_name": canonical_name,
        "source_library": source_library,
        "source_url": source_url,
        "source_id": source_id,
        "description_text": description_text,
        "structured_properties": json.dumps(structured_properties) if structured_properties else None,
        "cultural_lineage_tags": json.dumps(cultural_lineage_tags) if cultural_lineage_tags else None,
        "historical_period": historical_period,
        "genre_appearances": json.dumps(genre_appearances) if genre_appearances else None,
        "related_entries": json.dumps(related_entries) if related_entries else None,
        "license_class": license_class,
    }

# ── Source: RePoE (brather1ng/RePoE) ─────────────────────────────────────────

REPOE_BASE = "https://raw.githubusercontent.com/brather1ng/RePoE/master/RePoE/data"
REPOE_LICENSE = "MIT"
REPOE_SOURCE_LIB = "path-of-exile-repoe"
REPOE_BASE_URL = "https://github.com/brather1ng/RePoE/blob/master/RePoE/data/base_items.json"

# PoE weapon item classes (+ related combat items)
REPOE_WEAPON_CLASSES = {
    "One Hand Sword", "Two Hand Sword", "Thrusting One Hand Sword",
    "One Hand Axe", "Two Hand Axe",
    "One Hand Mace", "Two Hand Mace",
    "Bow", "Crossbow",
    "Claw", "Dagger", "Rune Dagger",
    "Staff", "Warstaff",
    "Wand", "Sceptre",
    "HeistEquipmentWeapon",
    "FishingRod",
    "Shield", "Quiver",
    "AbyssJewel", "Jewel",
}

# Broad weapon classes to keep (excludes pure accessories, gems, etc.)
REPOE_INCLUDE_CLASSES = {
    "One Hand Sword", "Two Hand Sword", "Thrusting One Hand Sword",
    "One Hand Axe", "Two Hand Axe",
    "One Hand Mace", "Two Hand Mace",
    "Bow", "Crossbow",
    "Claw", "Dagger", "Rune Dagger",
    "Staff", "Warstaff",
    "Wand", "Sceptre",
    "HeistEquipmentWeapon",
    "Shield", "Quiver",
}

def _repoe_class_to_subclass(item_class):
    mapping = {
        "One Hand Sword": "sword", "Two Hand Sword": "greatsword",
        "Thrusting One Hand Sword": "rapier",
        "One Hand Axe": "axe", "Two Hand Axe": "greataxe",
        "One Hand Mace": "mace", "Two Hand Mace": "greatmace",
        "Bow": "bow", "Crossbow": "crossbow",
        "Claw": "claw", "Dagger": "dagger", "Rune Dagger": "rune_dagger",
        "Staff": "staff", "Warstaff": "warstaff",
        "Wand": "wand", "Sceptre": "sceptre",
        "HeistEquipmentWeapon": "heist_weapon",
        "Shield": "shield", "Quiver": "quiver",
    }
    return mapping.get(item_class, "other")

def import_repoe(conn):
    log("[RePoE] starting import from base_items.json")
    url = f"{REPOE_BASE}/base_items.json"
    data, err = fetch_json(url)
    if err:
        log(f"[RePoE] FETCH ERROR: {err}")
        return {"source": REPOE_SOURCE_LIB, "rows_inserted": 0, "error": err}

    rows = []
    skipped = 0
    for item_path, item in data.items():
        item_class = item.get("item_class", "")
        if item_class not in REPOE_INCLUDE_CLASSES:
            skipped += 1
            continue

        name = item.get("name", "")
        if not name:
            skipped += 1
            continue

        release_state = item.get("release_state", "released")
        if release_state not in ("released", "unique_only"):
            skipped += 1
            continue

        subclass = _repoe_class_to_subclass(item_class)
        tags = item.get("tags", [])
        reqs = item.get("requirements") or {}
        props = item.get("properties") or {}
        implicits = item.get("implicits", [])

        structured_props = {
            "item_class": item_class,
            "item_subclass": subclass,
            "drop_level": item.get("drop_level"),
            "inventory_width": item.get("inventory_width"),
            "inventory_height": item.get("inventory_height"),
            "requirements": reqs,
            "properties": props,
            "implicits": implicits,
            "release_state": release_state,
            "item_path": item_path,
        }

        # item_path is unique identifier
        item_id = item_path.replace("/", "_")
        source_url = f"https://github.com/brather1ng/RePoE/blob/master/RePoE/data/base_items.json#{item_id}"

        row = make_row(
            canonical_name=name,
            source_library=REPOE_SOURCE_LIB,
            source_url=source_url,
            source_id=item_path,
            description_text=None,
            structured_properties=structured_props,
            cultural_lineage_tags=["fictional"],
            historical_period=None,
            genre_appearances=["fantasy", "arpg"],
            related_entries=None,
            license_class=REPOE_LICENSE,
        )
        rows.append(row)

        if len(rows) >= 500:
            insert_batch(conn, rows)
            rows = []

    if rows:
        insert_batch(conn, rows)

    final_count = count_source(conn, REPOE_SOURCE_LIB)
    log(f"[RePoE] done. inserted/existing={final_count}, skipped={skipped}")
    return {
        "source": REPOE_SOURCE_LIB,
        "rows_inserted": final_count,
        "license": REPOE_LICENSE,
        "error": None,
    }

# ── Source: Elden Ring (deliton/eldenring-api fallback) ──────────────────────

DELITON_BASE = "https://raw.githubusercontent.com/deliton/eldenring-api/main/api/public/data"
DELITON_LICENSE = "MIT"
ERDB_SOURCE_LIB = "elden-ring-erdb"

def import_eldenring(conn):
    log("[EldenRing/deliton] starting import from public/data/weapons.json")
    url = f"{DELITON_BASE}/weapons.json"
    data, err = fetch_json(url)
    if err:
        log(f"[EldenRing/deliton] FETCH ERROR: {err}")
        return {"source": ERDB_SOURCE_LIB, "rows_inserted": 0, "error": err}

    if not isinstance(data, list):
        log(f"[EldenRing/deliton] unexpected data type: {type(data).__name__}")
        return {"source": ERDB_SOURCE_LIB, "rows_inserted": 0, "error": "unexpected format"}

    rows = []
    skipped = 0
    for item in data:
        name = item.get("name", "").strip()
        if not name:
            skipped += 1
            continue

        item_id = item.get("id", "")
        image_url = item.get("image", "")
        description = item.get("description", "")
        category = item.get("category", "")

        # Collect attack/defence/scalesWith stats
        attack = item.get("attack", [])
        defence = item.get("defence", [])
        scales = item.get("scalesWith", [])
        weight = item.get("weight")

        structured_props = {
            "id": item_id,
            "category": category,
            "attack": attack,
            "defence": defence,
            "scalesWith": scales,
            "weight": weight,
            "image_url": image_url,
        }

        source_url = f"https://github.com/deliton/eldenring-api/blob/main/api/public/data/weapons.json#{item_id}"

        row = make_row(
            canonical_name=name,
            source_library=ERDB_SOURCE_LIB,
            source_url=source_url,
            source_id=item_id,
            description_text=description if description else None,
            structured_properties=structured_props,
            cultural_lineage_tags=["fictional"],
            historical_period=None,
            genre_appearances=["fantasy", "soulslike", "elden-ring"],
            related_entries=None,
            license_class=DELITON_LICENSE,
        )
        rows.append(row)

        if len(rows) >= 500:
            insert_batch(conn, rows)
            rows = []

    if rows:
        insert_batch(conn, rows)

    final_count = count_source(conn, ERDB_SOURCE_LIB)
    log(f"[EldenRing/deliton] done. inserted/existing={final_count}, skipped={skipped}")
    return {
        "source": ERDB_SOURCE_LIB,
        "rows_inserted": final_count,
        "license": DELITON_LICENSE,
        "error": None,
    }

# ── Source: Diablo II (blizzhackers/d2data) ───────────────────────────────────

D2DATA_BASE = "https://raw.githubusercontent.com/blizzhackers/d2data/master/json"
D2DATA_LICENSE = "MIT"
D2DATA_SOURCE_LIB = "diablo2-d2data"

# D2 weapon types (from items.json "type" field)
D2_WEAPON_TYPES = {
    "axe", "sword", "mace", "polearm", "spear", "bow", "crossbow",
    "dagger", "staff", "wand", "sceptre", "amazon", "throwing",
    "javelin", "orb", "hammer", "club",
}

def _d2_type_to_genre(type_str):
    """Determine cultural lineage tags from D2 type."""
    if type_str in ("amazon", "javelin"):
        return ["fictional", "greek_inspired"]
    return ["fictional"]

def import_d2data(conn):
    log("[D2/blizzhackers] starting import")

    # File 1: weapons.json — base weapon types (306 entries)
    log("[D2] fetching weapons.json (base types)")
    weapons_url = f"{D2DATA_BASE}/weapons.json"
    weapons_data, err = fetch_json(weapons_url)
    if err:
        log(f"[D2] weapons.json FETCH ERROR: {err}")
        weapons_data = {}

    # File 2: items.json — all items by type field (692 entries, many weapons)
    log("[D2] fetching items.json (all items)")
    items_url = f"{D2DATA_BASE}/items.json"
    items_data, err2 = fetch_json(items_url)
    if err2:
        log(f"[D2] items.json FETCH ERROR: {err2}")
        items_data = {}

    # File 3: uniqueitems.json — unique named weapons (433 items, filter by code)
    log("[D2] fetching uniqueitems.json (unique named items)")
    unique_url = f"{D2DATA_BASE}/uniqueitems.json"
    unique_data, err3 = fetch_json(unique_url)
    if err3:
        log(f"[D2] uniqueitems.json FETCH ERROR: {err3}")
        unique_data = {}

    # Build set of base weapon codes from weapons.json for unique items filtering
    weapon_codes = set()
    if isinstance(weapons_data, dict):
        for code, v in weapons_data.items():
            weapon_codes.add(code)
            # also add normcode, ubercode, ultracode
            for field in ("normcode", "ubercode", "ultracode"):
                c = v.get(field, "")
                if c and c != "xxx":
                    weapon_codes.add(c)

    rows = []
    seen_names = set()  # dedup within this import

    # --- weapons.json base types ---
    if isinstance(weapons_data, dict):
        for code, item in weapons_data.items():
            name = item.get("name", "").strip()
            if not name or name in seen_names:
                continue
            seen_names.add(name)
            w_type = item.get("type", "")
            structured_props = {
                "code": code,
                "type": w_type,
                "mindam": item.get("mindam"),
                "maxdam": item.get("maxdam"),
                "speed": item.get("speed"),
                "reqstr": item.get("reqstr"),
                "reqdex": item.get("reqdex"),
                "durability": item.get("durability"),
                "level": item.get("level"),
                "range": item.get("rangeadder"),
                "wclass": item.get("wclass"),
                "2handedwclass": item.get("2handedwc"),
                "2handed": item.get("2handed"),
                "normcode": item.get("normcode"),
                "ubercode": item.get("ubercode"),
                "ultracode": item.get("ultracode"),
            }
            source_url = f"https://github.com/blizzhackers/d2data/blob/master/json/weapons.json#{code}"
            row = make_row(
                canonical_name=name,
                source_library=D2DATA_SOURCE_LIB,
                source_url=source_url,
                source_id=code,
                description_text=None,
                structured_properties=structured_props,
                cultural_lineage_tags=_d2_type_to_genre(w_type),
                historical_period=None,
                genre_appearances=["fantasy", "arpg", "diablo"],
                related_entries=None,
                license_class=D2DATA_LICENSE,
            )
            rows.append(row)

    # --- items.json: items with weapon types not already captured ---
    if isinstance(items_data, dict):
        for code, item in items_data.items():
            name = item.get("name", "").strip()
            if not name or name in seen_names:
                continue
            w_type = item.get("type", "").lower()
            if w_type not in D2_WEAPON_TYPES:
                continue
            seen_names.add(name)
            structured_props = {
                "code": code,
                "type": w_type,
                "mindam": item.get("mindam"),
                "maxdam": item.get("maxdam"),
                "speed": item.get("speed"),
                "reqstr": item.get("reqstr"),
                "reqdex": item.get("reqdex"),
                "durability": item.get("durability"),
                "level": item.get("level"),
            }
            source_url = f"https://github.com/blizzhackers/d2data/blob/master/json/items.json#{code}"
            row = make_row(
                canonical_name=name,
                source_library=D2DATA_SOURCE_LIB,
                source_url=source_url,
                source_id=f"items_{code}",
                description_text=None,
                structured_properties=structured_props,
                cultural_lineage_tags=["fictional"],
                historical_period=None,
                genre_appearances=["fantasy", "arpg", "diablo"],
                related_entries=None,
                license_class=D2DATA_LICENSE,
            )
            rows.append(row)

    # --- uniqueitems.json: unique named weapons ---
    if isinstance(unique_data, dict):
        for uid, item in unique_data.items():
            name = item.get("index", "").strip()
            if not name or name in seen_names:
                continue
            code = item.get("code", "")
            base_name = item.get("*ItemName", "")
            # Only include if code matches a weapon base code
            if code not in weapon_codes:
                continue
            seen_names.add(name)
            structured_props = {
                "uid": uid,
                "code": code,
                "base_item": base_name,
                "set": item.get("set"),
                "level": item.get("lvl"),
                "level_req": item.get("lvl req"),
                "rarity": item.get("rarity"),
                "props": {f"prop{i}": item.get(f"prop{i}") for i in range(1, 13) if item.get(f"prop{i}")},
            }
            source_url = f"https://github.com/blizzhackers/d2data/blob/master/json/uniqueitems.json#{uid}"
            row = make_row(
                canonical_name=name,
                source_library=D2DATA_SOURCE_LIB,
                source_url=source_url,
                source_id=f"unique_{uid}",
                description_text=None,
                structured_properties=structured_props,
                cultural_lineage_tags=["fictional"],
                historical_period=None,
                genre_appearances=["fantasy", "arpg", "diablo"],
                related_entries=None,
                license_class=D2DATA_LICENSE,
            )
            rows.append(row)

    # Batch insert
    for i in range(0, len(rows), 500):
        insert_batch(conn, rows[i:i + 500])

    final_count = count_source(conn, D2DATA_SOURCE_LIB)
    log(f"[D2/blizzhackers] done. inserted/existing={final_count}")
    return {
        "source": D2DATA_SOURCE_LIB,
        "rows_inserted": final_count,
        "license": D2DATA_LICENSE,
        "error": None,
    }

# ── Source: GTA-V (DurtyFree/gta-v-data-dumps) ───────────────────────────────

GTAV_BASE = "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master"
GTAV_LICENSE = "unknown"  # No explicit license in repo; data-dumps for modding; no explicit license file
GTAV_SOURCE_LIB = "gta-v-data"

# Filter out non-weapons
GTAV_SKIP = {"WEAPON_UNARMED"}

def _gtav_name(item):
    """Extract English display name from GTA-V weapon entry."""
    label = item.get("TranslatedLabel", {})
    if isinstance(label, dict):
        return label.get("English", "") or item.get("Name", "")
    return item.get("Name", "")

def import_gtav(conn):
    log("[GTA-V/DurtyFree] starting import from weapons.json")
    url = f"{GTAV_BASE}/weapons.json"
    data, err = fetch_json(url)
    if err:
        log(f"[GTA-V] FETCH ERROR: {err}")
        return {"source": GTAV_SOURCE_LIB, "rows_inserted": 0, "error": err}

    if not isinstance(data, list):
        log(f"[GTA-V] unexpected type: {type(data).__name__}")
        return {"source": GTAV_SOURCE_LIB, "rows_inserted": 0, "error": "unexpected format"}

    rows = []
    skipped = 0
    for item in data:
        raw_name = item.get("Name", "")
        if raw_name in GTAV_SKIP:
            skipped += 1
            continue

        display_name = _gtav_name(item)
        if not display_name:
            display_name = raw_name

        if not display_name:
            skipped += 1
            continue

        # Remove WEAPON_ prefix for cleaner canonical name
        if display_name.startswith("WEAPON_"):
            display_name = display_name[7:].replace("_", " ").title()

        weapon_hash = item.get("Hash")
        int_hash = item.get("IntHash")
        translated = item.get("TranslatedLabel", {})
        # Collect all translations as structured props
        structured_props = {
            "raw_name": raw_name,
            "hash": weapon_hash,
            "int_hash": int_hash,
            "translations": translated if isinstance(translated, dict) else {},
        }

        source_url = f"https://github.com/DurtyFree/gta-v-data-dumps/blob/master/weapons.json#{raw_name}"

        row = make_row(
            canonical_name=display_name,
            source_library=GTAV_SOURCE_LIB,
            source_url=source_url,
            source_id=raw_name,
            description_text=None,
            structured_properties=structured_props,
            cultural_lineage_tags=["fictional", "modern"],
            historical_period="modern",
            genre_appearances=["modern", "open-world", "gta"],
            related_entries=None,
            license_class=GTAV_LICENSE,
        )
        rows.append(row)

        if len(rows) >= 500:
            insert_batch(conn, rows)
            rows = []

    if rows:
        insert_batch(conn, rows)

    final_count = count_source(conn, GTAV_SOURCE_LIB)
    log(f"[GTA-V/DurtyFree] done. inserted/existing={final_count}, skipped={skipped}")
    return {
        "source": GTAV_SOURCE_LIB,
        "rows_inserted": final_count,
        "license": GTAV_LICENSE,
        "error": None,
    }

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    _open_log()
    log("=== Track K — Multi-ARPG / Open-World Weapon Bundle starting ===")
    log(f"DB: {DB_PATH}")
    log(f"Summary: {SUMMARY_PATH}")

    conn = get_db()
    results = []

    # 1. RePoE
    try:
        r = import_repoe(conn)
        results.append(r)
    except Exception as e:
        log(f"[RePoE] EXCEPTION: {e}\n{traceback.format_exc()}")
        results.append({"source": REPOE_SOURCE_LIB, "rows_inserted": 0, "error": str(e)})

    # 2. Elden Ring (deliton fallback)
    try:
        r = import_eldenring(conn)
        results.append(r)
    except Exception as e:
        log(f"[EldenRing] EXCEPTION: {e}\n{traceback.format_exc()}")
        results.append({"source": ERDB_SOURCE_LIB, "rows_inserted": 0, "error": str(e)})

    # 3. Diablo II
    try:
        r = import_d2data(conn)
        results.append(r)
    except Exception as e:
        log(f"[D2] EXCEPTION: {e}\n{traceback.format_exc()}")
        results.append({"source": D2DATA_SOURCE_LIB, "rows_inserted": 0, "error": str(e)})

    # 4. GTA-V
    try:
        r = import_gtav(conn)
        results.append(r)
    except Exception as e:
        log(f"[GTA-V] EXCEPTION: {e}\n{traceback.format_exc()}")
        results.append({"source": GTAV_SOURCE_LIB, "rows_inserted": 0, "error": str(e)})

    conn.close()

    # Aggregate count
    total = sum(r.get("rows_inserted", 0) for r in results)

    finished_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    summary = {
        "track": "K",
        "wave": "wave1",
        "started_at": STARTED_AT,
        "finished_at": finished_at,
        "total_rows_inserted": total,
        "acceptance_criterion": ">=1500",
        "acceptance_met": total >= 1500,
        "per_source": results,
    }

    os.makedirs(os.path.dirname(SUMMARY_PATH), exist_ok=True)
    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    log(f"=== Track K complete. Total rows: {total} / acceptance: {summary['acceptance_met']} ===")
    log(f"Summary written to: {SUMMARY_PATH}")

    if _log_fh:
        _log_fh.close()

    # Print final summary to stdout for caller
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
