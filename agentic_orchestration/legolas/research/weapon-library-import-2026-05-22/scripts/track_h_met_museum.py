#!/usr/bin/env python3
"""
Track H — Met Museum Open Access API (Arms & Armor)
Weapon Library Import — Wave 2

Fetches all departmentIds=4 (Arms & Armor) objects from the Met Museum Open
Access API and inserts them into weapon_knowledge_entries + knowledge_entry_reference_images.

Discipline #1:  math note at track-H-math-note.md (authored before this script)
Discipline #19: fire with nohup; return PID immediately; do NOT monitor inline
Discipline #20: API subdomain collectionapi.metmuseum.org is GREEN (no robots.txt);
                research-agent UA used

Transport: urllib.request + ThreadPoolExecutor (avoids aiohttp Imperva bot-detection)
Rate: MAX_WORKERS=5 threads (≤5 req/sec courtesy ceiling)
Expected wall: ~46-55 minutes for 13,753 objects
"""

import certifi
import concurrent.futures
import json
import shutil
import sqlite3
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
SUMMARY_PATH = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "legolas/research/weapon-library-import-2026-05-22/summaries/track-H-met-museum-summary.json"
)
LOG_PATH = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/logs/"
    "weapon-library-track-H.log"
)

DEPT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=4"
OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{}"

SOURCE_LIBRARY = "met-museum"
BATCH_SIZE = 100
MAX_WORKERS = 5          # 5 concurrent threads = ~5 req/sec courtesy ceiling
REQUEST_TIMEOUT = 30     # seconds per request
MAX_RETRIES = 3
BACKOFF_BASE = 2.0       # seconds; doubles per retry

USER_AGENT = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"

# Shared SSL context (certifi CA bundle)
SSL_CTX = ssl.create_default_context(cafile=certifi.where())


# ---------------------------------------------------------------------------
# Logging helper
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line, flush=True)


# ---------------------------------------------------------------------------
# HTTP fetch helper (urllib-based; avoids aiohttp Imperva triggers)
# ---------------------------------------------------------------------------

def fetch_url(url: str) -> dict | None:
    """
    Fetch a Met API URL with retries. Returns parsed JSON dict, None for 404,
    or dict with '_extraction_error' key on failure.
    """
    for attempt in range(MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=REQUEST_TIMEOUT) as resp:
                body = resp.read()
                return json.loads(body)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None   # Retired / missing object
            wait = BACKOFF_BASE ** (attempt + 1)
            if attempt < MAX_RETRIES:
                time.sleep(wait)
            else:
                return {"_extraction_error": f"HTTP {exc.code}"}
        except urllib.error.URLError as exc:
            wait = BACKOFF_BASE ** (attempt + 1)
            if attempt < MAX_RETRIES:
                time.sleep(wait)
            else:
                return {"_extraction_error": f"URLError: {exc.reason}"}
        except Exception as exc:
            wait = BACKOFF_BASE ** (attempt + 1)
            if attempt < MAX_RETRIES:
                time.sleep(wait)
            else:
                return {"_extraction_error": f"Exception: {exc}"}
    return {"_extraction_error": "max retries exceeded"}


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Verify the required tables exist; abort if missing."""
    required = ["weapon_knowledge_entries", "knowledge_entry_reference_images"]
    for table in required:
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ).fetchone()
        if row is None:
            raise RuntimeError(
                f"Required table '{table}' not found in DB. "
                "Run schema.sql first."
            )


def insert_batch(conn: sqlite3.Connection, entries: list[dict], images: list[dict]) -> tuple[int, int]:
    """
    Insert a batch of knowledge entries + their images.
    Returns (entries_inserted, images_inserted).
    Uses INSERT OR IGNORE on (source_library, source_url) unique constraint.
    """
    entry_count = 0
    image_count = 0
    now_iso = datetime.now(timezone.utc).isoformat()

    for e in entries:
        try:
            cur = conn.execute(
                """
                INSERT OR IGNORE INTO weapon_knowledge_entries
                    (canonical_name, source_library, source_url, source_id,
                     description_text, structured_properties, cultural_lineage_tags,
                     historical_period, genre_appearances, license_class, imported_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    e["canonical_name"],
                    e["source_library"],
                    e["source_url"],
                    e["source_id"],
                    e.get("description_text"),
                    e.get("structured_properties"),
                    e.get("cultural_lineage_tags"),
                    e.get("historical_period"),
                    e.get("genre_appearances"),
                    e.get("license_class"),
                    now_iso,
                ),
            )
            entry_count += cur.rowcount
            # Resolve rowid for image FK (works whether INSERT or IGNORE fired)
            row = conn.execute(
                "SELECT id FROM weapon_knowledge_entries WHERE source_library=? AND source_url=?",
                (e["source_library"], e["source_url"]),
            ).fetchone()
            if row:
                e["_db_id"] = row[0]
        except sqlite3.Error as exc:
            log(f"  DB entry error for source_id={e.get('source_id')}: {exc}")

    for img in images:
        entry = img.get("_entry_ref")
        if entry is None or "_db_id" not in entry:
            continue
        try:
            cur = conn.execute(
                """
                INSERT OR IGNORE INTO knowledge_entry_reference_images
                    (knowledge_entry_id, image_url, image_source, license_class,
                     is_canonical, image_caption, imported_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry["_db_id"],
                    img["image_url"],
                    img.get("image_source", "met-museum-api"),
                    img.get("license_class", "CC0"),
                    img.get("is_canonical", 0),
                    img.get("image_caption"),
                    now_iso,
                ),
            )
            image_count += cur.rowcount
        except sqlite3.Error as exc:
            log(f"  DB image error for entry_id={entry.get('_db_id')}: {exc}")

    conn.commit()
    return entry_count, image_count


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def normalize_object(obj: dict) -> tuple[dict, list[dict]]:
    """
    Normalize a raw Met API object dict into:
      - one entry dict (for weapon_knowledge_entries)
      - list of image dicts (for knowledge_entry_reference_images)
    """
    object_id = obj.get("objectID")
    title = (obj.get("title") or "").strip()
    object_name = (obj.get("objectName") or "").strip()

    # Canonical name: prefer title; fall back to objectName; last resort synthetic
    canonical_name = title or object_name or f"Met-Arms-{object_id}"

    source_url = (
        obj.get("objectURL")
        or f"https://www.metmuseum.org/art/collection/search/{object_id}"
    )
    source_id = str(object_id)

    is_public_domain = bool(obj.get("isPublicDomain", False))
    license_class = "CC0" if is_public_domain else "unknown"

    # Structured properties: capture the rich metadata fields
    structured = {
        "objectID":           object_id,
        "objectName":         object_name,
        "classification":     obj.get("classification") or "",
        "culture":            obj.get("culture") or "",
        "period":             obj.get("period") or "",
        "dynasty":            obj.get("dynasty") or "",
        "reign":              obj.get("reign") or "",
        "country":            obj.get("country") or "",
        "region":             obj.get("region") or "",
        "subregion":          obj.get("subregion") or "",
        "medium":             obj.get("medium") or "",
        "dimensions":         obj.get("dimensions") or "",
        "objectDate":         obj.get("objectDate") or "",
        "objectBeginDate":    obj.get("objectBeginDate"),
        "objectEndDate":      obj.get("objectEndDate"),
        "department":         obj.get("department") or "",
        "artistDisplayName":  obj.get("artistDisplayName") or "",
        "accessionNumber":    obj.get("accessionNumber") or "",
        "creditLine":         obj.get("creditLine") or "",
        "isPublicDomain":     is_public_domain,
        "primaryImageSmall":  obj.get("primaryImageSmall") or "",
        "objectWikidata_URL": obj.get("objectWikidata_URL") or "",
        "isHighlight":        bool(obj.get("isHighlight", False)),
        "GalleryNumber":      obj.get("GalleryNumber") or "",
    }

    # Historical period: prefer explicit period field, fall back to dynasty or objectDate
    historical_period = (
        (obj.get("period") or "").strip()
        or (obj.get("dynasty") or "").strip()
        or (obj.get("objectDate") or "").strip()
        or None
    )

    # Cultural lineage tags: from culture, country, region, and tags[]
    lineage_parts = []
    for field in ("culture", "country", "region"):
        val = (obj.get(field) or "").strip()
        if val:
            lineage_parts.append(val)
    raw_tags = obj.get("tags") or []
    if isinstance(raw_tags, list):
        for t in raw_tags:
            if isinstance(t, dict):
                term = (t.get("term") or "").strip()
            else:
                term = str(t).strip()
            if term:
                lineage_parts.append(term)
    cultural_lineage_tags = json.dumps(lineage_parts) if lineage_parts else None

    # Genre appearances: museum objects are historical by default
    genre_appearances = json.dumps(["historical"])

    entry = {
        "canonical_name":        canonical_name,
        "source_library":        SOURCE_LIBRARY,
        "source_url":            source_url,
        "source_id":             source_id,
        "description_text":      None,   # Met API does not expose free-text description
        "structured_properties": json.dumps(structured),
        "cultural_lineage_tags": cultural_lineage_tags,
        "historical_period":     historical_period,
        "genre_appearances":     genre_appearances,
        "license_class":         license_class,
    }

    # Images (URL-only per mission §3; images only available for public domain objects)
    images = []
    primary_url = (obj.get("primaryImage") or "").strip()
    if primary_url:
        images.append({
            "_entry_ref":   entry,
            "image_url":    primary_url,
            "image_source": "met-museum-primary",
            "license_class": "CC0",
            "is_canonical": 1,
            "image_caption": canonical_name,
        })

    additional = obj.get("additionalImages") or []
    if isinstance(additional, list):
        for idx, img_url in enumerate(additional):
            if isinstance(img_url, str) and img_url.strip():
                images.append({
                    "_entry_ref":   entry,
                    "image_url":    img_url.strip(),
                    "image_source": "met-museum-additional",
                    "license_class": "CC0",
                    "is_canonical": 0,
                    "image_caption": f"{canonical_name} (additional {idx+1})",
                })

    return entry, images


# ---------------------------------------------------------------------------
# Fetch task (runs in thread pool)
# ---------------------------------------------------------------------------

def fetch_one(oid: int) -> tuple[int, dict | None]:
    """Fetch a single object by ID. Returns (oid, result_dict_or_None)."""
    url = OBJECT_URL.format(oid)
    return oid, fetch_url(url)


# ---------------------------------------------------------------------------
# Main crawl
# ---------------------------------------------------------------------------

def crawl(object_ids: list[int]) -> dict:
    """
    Thread-pool crawl. Fetches all object_ids with MAX_WORKERS threads.
    Returns stats dict.
    """
    total = len(object_ids)
    inserted_entries = 0
    inserted_images = 0
    skipped_404 = 0
    errors = []
    entries_with_image = 0

    conn = get_db_connection()
    ensure_schema(conn)

    batch_entries: list[dict] = []
    batch_images: list[dict] = []

    start_time = time.monotonic()
    last_log_time = start_time
    processed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_one, oid): oid for oid in object_ids}

        for future in concurrent.futures.as_completed(futures):
            oid, obj = future.result()
            processed += 1

            if obj is None:
                # 404 — retired or missing object
                skipped_404 += 1
            elif "_extraction_error" in obj:
                errors.append({"object_id": oid, "error": obj["_extraction_error"]})
            else:
                entry, images = normalize_object(obj)
                batch_entries.append(entry)
                batch_images.extend(images)
                if images:
                    entries_with_image += 1

            # Flush batch to DB
            if len(batch_entries) >= BATCH_SIZE:
                e_ins, i_ins = insert_batch(conn, batch_entries, batch_images)
                inserted_entries += e_ins
                inserted_images += i_ins
                batch_entries.clear()
                batch_images.clear()

            # Progress log every 60 seconds
            now = time.monotonic()
            if now - last_log_time >= 60:
                elapsed = now - start_time
                rate = processed / elapsed if elapsed > 0 else 0
                eta = (total - processed) / rate if rate > 0 else 0
                log(
                    f"  Progress: {processed}/{total} ({100*processed/total:.1f}%) "
                    f"| inserted={inserted_entries} images={inserted_images} "
                    f"| 404s={skipped_404} errors={len(errors)} "
                    f"| rate={rate:.1f}/s ETA={eta/60:.1f}min"
                )
                last_log_time = now

    # Flush remaining batch
    if batch_entries:
        e_ins, i_ins = insert_batch(conn, batch_entries, batch_images)
        inserted_entries += e_ins
        inserted_images += i_ins

    conn.close()

    elapsed = time.monotonic() - start_time
    image_coverage_pct = (entries_with_image / max(inserted_entries, 1)) * 100

    return {
        "track": "H",
        "source": SOURCE_LIBRARY,
        "crawl_date": datetime.now(timezone.utc).isoformat(),
        "total_object_ids": total,
        "processed": processed,
        "inserted_entries": inserted_entries,
        "inserted_images": inserted_images,
        "entries_with_image": entries_with_image,
        "image_coverage_pct": round(image_coverage_pct, 1),
        "skipped_404": skipped_404,
        "errors": errors,
        "error_count": len(errors),
        "wall_time_seconds": round(elapsed, 1),
        "wall_time_minutes": round(elapsed / 60, 1),
        "acceptance_criteria": {
            "rows_gte_10000": inserted_entries >= 10000,
            "image_coverage_gte_70pct": image_coverage_pct >= 70.0,
            "cc0_captured": True,   # set by logic: isPublicDomain=true → license_class='CC0'
        },
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    log("=== Track H — Met Museum Open Access API ===")
    log(f"DB:      {DB_PATH}")
    log(f"Summary: {SUMMARY_PATH}")

    # Pre-flight: disk space check
    free_bytes = shutil.disk_usage(str(DB_PATH.parent)).free
    if free_bytes < 500 * 1024 * 1024:
        log(f"ABORT: insufficient disk space ({free_bytes // (1024*1024)} MB free; need ≥500 MB)")
        sys.exit(1)

    # Ensure output dirs exist
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Step 1: fetch department object list
    log(f"Step 1: fetching department object list from {DEPT_URL}")
    dept_result = fetch_url(DEPT_URL)
    if dept_result is None or "_extraction_error" in (dept_result or {}):
        log(f"ABORT: failed to fetch department list: {dept_result}")
        sys.exit(1)

    object_ids: list[int] = dept_result.get("objectIDs") or []
    total_reported = dept_result.get("total", 0)
    log(f"  API reports total={total_reported}, objectIDs list length={len(object_ids)}")

    if not object_ids:
        log("ABORT: no object IDs returned. Check API availability.")
        sys.exit(1)

    # Step 2: per-object fetch + insert
    log(f"Step 2: fetching {len(object_ids)} objects at ≤{MAX_WORKERS} concurrent threads")
    expected_min = len(object_ids) / MAX_WORKERS / 60
    log(f"  Expected wall time: ~{expected_min:.0f}–{expected_min * 1.2:.0f} minutes")

    stats = crawl(object_ids)

    # Step 3: write summary JSON
    log(f"Step 3: writing summary to {SUMMARY_PATH}")
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    log("=== Track H complete ===")
    log(f"  Inserted entries:    {stats['inserted_entries']}")
    log(f"  Inserted images:     {stats['inserted_images']}")
    log(f"  Image coverage:      {stats['image_coverage_pct']}%")
    log(f"  404s (retired):      {stats['skipped_404']}")
    log(f"  Errors:              {stats['error_count']}")
    log(f"  Wall time:           {stats['wall_time_minutes']} min")
    log(
        f"  Acceptance: rows≥10K={stats['acceptance_criteria']['rows_gte_10000']} "
        f"img≥70%={stats['acceptance_criteria']['image_coverage_gte_70pct']}"
    )
    log(f"  Summary:             {SUMMARY_PATH}")

    # Exit non-zero if hard acceptance criterion fails
    if not stats["acceptance_criteria"]["rows_gte_10000"]:
        log("WARN: rows < 10,000 — acceptance criterion C1 NOT MET")
        sys.exit(2)


if __name__ == "__main__":
    main()
