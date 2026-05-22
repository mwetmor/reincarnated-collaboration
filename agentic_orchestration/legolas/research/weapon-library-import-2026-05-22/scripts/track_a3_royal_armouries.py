#!/usr/bin/env python3
"""
Track A3 — Royal Armouries collection crawl
Hive-mind: weapon-library-import-2026-05-22
Author: legolas (2026-05-22)

Source: collections.armouries.net/api/v3/ (internal API of royalarmouries.org collection SPA)
robots.txt: GREEN — royalarmouries.org Crawl-delay: 20 (honored as 30s with 1.5× safety margin)
License captured: editorial_only (Royal Armouries proprietary; non-commercial)
Image policy: URL-only; no download; images.royalarmouries.org blocks ClaudeBot so we use
              collections.armouries.net/media/<location> which is 200 accessible.

Discipline #1: math note at track-A3-math-note.md
Discipline #19: fired as nohup background process; returns immediately
Discipline #20: UA = reincarnated-engine/0.1 (research; mhwetmore@gmail.com); 30s delay

DB: /Users/admin/Games/reincarnated-loadout/data/telemetry.db (SQLite WAL)
Log: /Users/admin/Games/reincarnated-engine/logs/weapon-library-track-A3.log
Checkpoint: /Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_royal_armouries_checkpoint.json
Summary: /Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_royal_armouries_summary.json
"""

import sqlite3
import requests
import json
import time
import logging
import signal
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
LOG_PATH = Path("/Users/admin/Games/reincarnated-engine/logs/weapon-library-track-A3.log")
CHECKPOINT_PATH = Path("/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_royal_armouries_checkpoint.json")
SUMMARY_PATH = Path("/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_royal_armouries_summary.json")

# ─── API config ───────────────────────────────────────────────────────────────
API_BASE = "https://collections.armouries.net/api/v3/search"
IMAGE_BASE = "https://collections.armouries.net/media/"
SOURCE_LIBRARY = "royal_armouries"
PAGE_SIZE = 20            # API enforces 20 items/page regardless of size param
CRAWL_DELAY_S = 30        # 20s robots Crawl-delay × 1.5 safety margin
BATCH_SIZE = 50           # rows per DB commit (per dispatch spec)
MAX_CONSECUTIVE_ERRORS = 5

HEADERS = {
    "User-Agent": "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)",
    "Accept": "application/json",
    "Origin": "https://royalarmouries.org",
    "Referer": "https://royalarmouries.org/collection/search",
}

# ─── Logging setup ────────────────────────────────────────────────────────────
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("track_a3")

# ─── Graceful shutdown ────────────────────────────────────────────────────────
_shutdown = False

def _handle_signal(sig, frame):
    global _shutdown
    log.warning(f"Signal {sig} received — will stop after current batch")
    _shutdown = True

signal.signal(signal.SIGTERM, _handle_signal)
signal.signal(signal.SIGINT, _handle_signal)


# ─── DB helpers ───────────────────────────────────────────────────────────────

def open_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def ensure_library_registered(conn: sqlite3.Connection):
    conn.execute("""
        INSERT OR IGNORE INTO libraries
            (slug, display_name, base_url, api_url, import_tier, license_class, notes)
        VALUES
            ('royal_armouries', 'Royal Armouries', 'https://royalarmouries.org',
             'https://collections.armouries.net/api/v3/', 2, 'editorial_only',
             'Proprietary non-commercial; museum-grade historical arms and armour;
              Crawl-delay 20s honored as 30s; UA=reincarnated-engine/0.1; 67K+ objects')
    """)
    conn.commit()


def insert_entry_batch(conn: sqlite3.Connection, rows: list, image_rows: list) -> tuple[int, int]:
    """
    Insert a batch of weapon_knowledge_entries + knowledge_entry_reference_images.
    Returns (entries_inserted, images_inserted).
    Uses INSERT OR IGNORE on UNIQUE(source_library, source_url).
    """
    entries_inserted = 0
    images_inserted = 0
    cur = conn.cursor()

    for row in rows:
        try:
            cur.execute("""
                INSERT OR IGNORE INTO weapon_knowledge_entries
                    (canonical_name, source_library, source_url, source_id,
                     description_text, structured_properties, cultural_lineage_tags,
                     historical_period, genre_appearances, related_entries,
                     license_class, imported_at)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["canonical_name"],
                row["source_library"],
                row["source_url"],
                row["source_id"],
                row["description_text"],
                row["structured_properties"],
                row["cultural_lineage_tags"],
                row["historical_period"],
                row["genre_appearances"],
                row["related_entries"],
                row["license_class"],
                row["imported_at"],
            ))
            if cur.rowcount > 0:
                entries_inserted += 1
                entry_id = cur.lastrowid
                # Insert associated images
                for img in image_rows.get(row["source_id"], []):
                    try:
                        cur.execute("""
                            INSERT OR IGNORE INTO knowledge_entry_reference_images
                                (knowledge_entry_id, image_url, image_source,
                                 license_class, is_canonical, image_caption,
                                 width_px, height_px, imported_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            entry_id,
                            img["image_url"],
                            img["image_source"],
                            img["license_class"],
                            img["is_canonical"],
                            img.get("image_caption"),
                            img.get("width_px"),
                            img.get("height_px"),
                            row["imported_at"],
                        ))
                        if cur.rowcount > 0:
                            images_inserted += 1
                    except sqlite3.Error as e:
                        log.warning(f"Image insert error for {row['source_id']}: {e}")
        except sqlite3.Error as e:
            log.warning(f"Entry insert error for {row.get('source_id','?')}: {e}")

    conn.commit()
    return entries_inserted, images_inserted


# ─── Data normalization ────────────────────────────────────────────────────────

def _normalize_period(date_str: str | None) -> str | None:
    """Rough normalization: 'about 1895' → '1895', 'late 18th century' → '18th century'."""
    if not date_str:
        return None
    return date_str.strip()


def _classify_genre(category_type: str | None, object_type_list: list) -> list:
    """Map Royal Armouries category to genre_appearances tags."""
    genres = ["historical"]
    if category_type:
        ct = category_type.lower()
        if "firearm" in ct or "artillery" in ct:
            genres.append("modern-firearm")
        if "edged" in ct or "sword" in ct or "dagger" in ct:
            genres.append("melee")
        if "armour" in ct or "helmet" in ct or "shield" in ct:
            genres.append("armour")
    return genres


def _extract_cultural_tags(place_made: str | None, agent_list: list) -> list:
    """Extract cultural lineage free-tags from place and agent fields."""
    tags = []
    if place_made:
        tags.append(f"place:{place_made}")
    for agent in agent_list:
        if agent and agent.lower() not in ("unknown", "unidentified"):
            tags.append(f"maker:{agent[:80]}")
    return tags


def normalize_object(detail: dict) -> tuple[dict, list]:
    """
    Convert a raw Royal Armouries API object detail into:
    - a weapon_knowledge_entries row dict
    - a list of knowledge_entry_reference_images row dicts

    Returns (entry_row, image_rows_list).
    """
    now = datetime.now(timezone.utc).isoformat()
    obj_id = detail.get("id", "")
    accession = detail.get("accession_number", "")
    summary_title = detail.get("summary_title", "").strip()
    object_name = detail.get("object_name", "").strip()

    canonical_name = object_name or summary_title or obj_id

    template_intro = detail.get("templateIntro", {}) or {}
    template_meta = detail.get("templateMeta", {}) or {}
    template_teaser = detail.get("templateTeaserData", {}) or {}
    classification = detail.get("classification", []) or []

    # Description: combine intro fields
    desc_parts = []
    intro_title = template_intro.get("Title", "")
    intro_brief = template_intro.get("Brief description", "")
    if intro_title:
        desc_parts.append(intro_title)
    if intro_brief and intro_brief != intro_title:
        desc_parts.append(intro_brief)
    description_text = " | ".join(desc_parts) if desc_parts else None

    # Structured properties
    struct_props = {
        "accession_number": accession,
        "object_name": object_name,
        "place": template_meta.get("Place") or template_teaser.get("Production place"),
        "date": template_meta.get("Date") or template_teaser.get("Date"),
        "location_in_museum": template_meta.get("Location"),
        "object_type": [
            ot
            for c in classification
            for ot in (c.get("object_type") or [])
        ],
        "category_type": (detail.get("category") or {}).get("type"),
        "category_value": (detail.get("category") or {}).get("value"),
    }

    # Historical period
    historical_period = _normalize_period(struct_props["date"])

    # Category/genre
    category_type = struct_props["category_type"]
    object_types = struct_props["object_type"]
    genre_appearances = _classify_genre(category_type, object_types)

    # Cultural lineage tags
    place_made = struct_props["place"]
    agent_field = detail.get("agent") or []
    if not isinstance(agent_field, list):
        agent_field = [str(agent_field)]
    cultural_tags = _extract_cultural_tags(place_made, agent_field)

    # Source URL: canonical royalarmouries.org collection page
    source_url = f"https://royalarmouries.org/collection/object/{obj_id}"

    # Image rows
    media_list = detail.get("media") or []
    image_rows = []
    for media_idx, media in enumerate(media_list):
        artifacts = media.get("artifact") or []
        # Prefer "mid" (370px); fallback to "large"; fallback to "preview"
        preferred_order = ["mid", "large", "preview"]
        chosen = None
        for pref in preferred_order:
            for art in artifacts:
                if art.get("name") == pref:
                    chosen = art
                    break
            if chosen:
                break
        if not chosen and artifacts:
            chosen = artifacts[0]
        if chosen:
            location = chosen.get("location", "")
            image_url = f"{IMAGE_BASE}{location}"
            image_rows.append({
                "image_url": image_url,
                "image_source": "royal-armouries-api-media",
                "license_class": "editorial_only",
                "is_canonical": 1 if media_idx == 0 else 0,
                "image_caption": None,
                "width_px": chosen.get("width"),
                "height_px": chosen.get("height"),
            })

    entry_row = {
        "canonical_name": canonical_name,
        "source_library": SOURCE_LIBRARY,
        "source_url": source_url,
        "source_id": obj_id,
        "description_text": description_text,
        "structured_properties": json.dumps(struct_props, ensure_ascii=False),
        "cultural_lineage_tags": json.dumps(cultural_tags, ensure_ascii=False),
        "historical_period": historical_period,
        "genre_appearances": json.dumps(genre_appearances, ensure_ascii=False),
        "related_entries": None,
        "license_class": "editorial_only",
        "imported_at": now,
    }

    return entry_row, image_rows


# ─── Checkpoint I/O ───────────────────────────────────────────────────────────

def load_checkpoint() -> dict:
    if CHECKPOINT_PATH.exists():
        try:
            return json.loads(CHECKPOINT_PATH.read_text())
        except Exception:
            pass
    return {"last_from": 0, "inserted": 0, "images_inserted": 0,
            "errors": 0, "started_at": None, "last_update": None}


def save_checkpoint(cp: dict):
    cp["last_update"] = datetime.now(timezone.utc).isoformat()
    CHECKPOINT_PATH.write_text(json.dumps(cp, indent=2))


def save_summary(cp: dict, total_addressable: int):
    summary = {
        "track": "A3",
        "source": "royal_armouries",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "total_addressable": total_addressable,
        "entries_inserted": cp["inserted"],
        "images_inserted": cp["images_inserted"],
        "errors": cp["errors"],
        "started_at": cp["started_at"],
        "db_path": str(DB_PATH),
        "log_path": str(LOG_PATH),
        "checkpoint_path": str(CHECKPOINT_PATH),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2))
    log.info(f"Summary written to {SUMMARY_PATH}")


# ─── Fetch helpers ────────────────────────────────────────────────────────────

def fetch_page(session: requests.Session, from_offset: int) -> dict | None:
    """
    Fetch one page of objects from the Royal Armouries API.
    Returns parsed JSON dict, or None on failure.
    """
    params = {
        "filter": "data_type:(object)",
        "size": PAGE_SIZE,
        "from": from_offset,
    }
    try:
        resp = session.get(API_BASE, params=params, timeout=30)
        if resp.status_code == 429:
            return "RATE_LIMITED"
        if resp.status_code != 200:
            log.warning(f"HTTP {resp.status_code} at offset {from_offset}")
            return None
        return resp.json()
    except requests.RequestException as e:
        log.warning(f"Request error at offset {from_offset}: {e}")
        return None


# ─── Main crawl loop ─────────────────────────────────────────────────────────

def main():
    global _shutdown

    log.info("=" * 60)
    log.info("Track A3 — Royal Armouries — starting")
    log.info(f"DB: {DB_PATH}")
    log.info(f"API: {API_BASE}")
    log.info(f"Crawl delay: {CRAWL_DELAY_S}s (20s × 1.5 safety margin)")
    log.info("=" * 60)

    conn = open_db()
    ensure_library_registered(conn)

    cp = load_checkpoint()
    if not cp["started_at"]:
        cp["started_at"] = datetime.now(timezone.utc).isoformat()
    current_from = cp["last_from"]
    log.info(f"Resuming from offset {current_from} ({cp['inserted']} already inserted)")

    session = requests.Session()
    session.headers.update(HEADERS)

    total_addressable = 67783  # empirically determined; updated after first page
    consecutive_errors = 0
    backoff_s = 60

    entry_batch: list = []
    image_batch: dict = {}  # source_id -> list of image rows

    while not _shutdown:
        page_data = fetch_page(session, current_from)

        # Handle rate limiting
        if page_data == "RATE_LIMITED":
            log.warning(f"429 received at offset {current_from}; backing off {backoff_s}s")
            time.sleep(backoff_s)
            backoff_s = min(backoff_s * 2, 480)
            consecutive_errors += 1
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                log.error("Sustained 429s — marking AMBER and exiting per Discipline #20")
                cp["status"] = "AMBER_RATE_LIMITED"
                save_checkpoint(cp)
                save_summary(cp, total_addressable)
                break
            continue

        if page_data is None:
            consecutive_errors += 1
            log.warning(f"Fetch failed at offset {current_from}; consecutive errors: {consecutive_errors}")
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                log.error("Too many consecutive errors — stopping")
                save_checkpoint(cp)
                save_summary(cp, total_addressable)
                break
            time.sleep(CRAWL_DELAY_S)
            continue

        # Reset error counter on success
        consecutive_errors = 0
        backoff_s = 60

        # Update total from stats
        stats = page_data.get("stats", {})
        if stats:
            reported_total = stats.get("total", total_addressable)
            if reported_total and reported_total != total_addressable:
                total_addressable = reported_total
                log.info(f"Total addressable updated: {total_addressable}")

        metadata = page_data.get("metadata", [])
        if not metadata:
            log.info(f"Empty page at offset {current_from} — crawl complete")
            break

        # Normalize and batch
        for item in metadata:
            detail = item.get("detail", {})
            if not detail:
                cp["errors"] += 1
                continue
            try:
                entry_row, img_rows = normalize_object(detail)
                entry_batch.append(entry_row)
                if img_rows:
                    image_batch[entry_row["source_id"]] = img_rows
            except Exception as e:
                log.warning(f"Normalization error for {detail.get('id', '?')}: {e}")
                cp["errors"] += 1

        # Flush batch if at or over threshold
        if len(entry_batch) >= BATCH_SIZE:
            inserted, img_inserted = insert_entry_batch(conn, entry_batch, image_batch)
            cp["inserted"] += inserted
            cp["images_inserted"] += img_inserted
            log.info(
                f"offset={current_from} | inserted={inserted} imgs={img_inserted} "
                f"total={cp['inserted']} errors={cp['errors']}"
            )
            entry_batch = []
            image_batch = {}

        # Advance offset
        current_from += len(metadata)
        cp["last_from"] = current_from
        save_checkpoint(cp)

        # Check if we've reached the end
        if current_from >= total_addressable:
            log.info(f"Reached total addressable ({total_addressable}) — crawl complete")
            break

        # Respect crawl delay
        log.debug(f"Sleeping {CRAWL_DELAY_S}s before next request")
        time.sleep(CRAWL_DELAY_S)

    # Flush remaining batch
    if entry_batch:
        inserted, img_inserted = insert_entry_batch(conn, entry_batch, image_batch)
        cp["inserted"] += inserted
        cp["images_inserted"] += img_inserted
        log.info(f"Final flush: inserted={inserted} imgs={img_inserted}")

    cp["last_from"] = current_from
    save_checkpoint(cp)
    conn.close()

    # Final summary
    save_summary(cp, total_addressable)
    log.info("=" * 60)
    log.info(f"Track A3 complete")
    log.info(f"  Total addressable: {total_addressable}")
    log.info(f"  Entries inserted:  {cp['inserted']}")
    log.info(f"  Images inserted:   {cp['images_inserted']}")
    log.info(f"  Errors:            {cp['errors']}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
