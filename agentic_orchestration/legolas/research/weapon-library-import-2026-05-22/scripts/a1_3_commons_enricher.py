#!/usr/bin/env python3
"""
Track A1.3 — Wikimedia Commons image metadata enrichment
---------------------------------------------------------
For each knowledge_entry_reference_images row that points to a Commons URL,
fetches license + dimensions via the Commons API (point lookups, 1 req/sec).

Populates: license_class, width_px, height_px (updates existing rows).

Discipline #19: background process; checkpoints via DB; fully resumable.
Discipline #20: UA = reincarnated-engine/0.1 (research; mhwetmore@gmail.com)
                Rate: max 1 req/sec per Wikimedia API etiquette.
"""

import sqlite3
import requests
import json
import time
import logging
import sys
import os
import re
from datetime import datetime
from urllib.parse import unquote, urlparse

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = "/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_commons.log"
SUMMARY_PATH = "/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_wikipedia_wikidata_commons_summary.json"

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UA = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"

REQUEST_DELAY = 1.0    # seconds between API requests (1 req/sec)
BATCH_COMMIT = 50      # rows per DB commit

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# License normalization mapping from Commons short-name to our license_class values
LICENSE_MAP = {
    "cc0": "CC0",
    "cc-by-sa-4.0": "CC_BY_SA",
    "cc-by-sa-3.0": "CC_BY_SA",
    "cc-by-sa-2.5": "CC_BY_SA",
    "cc-by-sa-2.0": "CC_BY_SA",
    "cc-by-4.0": "CC_BY",
    "cc-by-3.0": "CC_BY",
    "cc-by-2.5": "CC_BY",
    "cc-by-2.0": "CC_BY",
    "pd": "CC0",  # Public Domain treated as CC0-equivalent
    "pd-old": "CC0",
    "pd-old-100": "CC0",
    "pd-us": "CC0",
    "pd-usgov": "CC0",
    "pd-art": "CC0",
    "gfdl": "CC_BY_SA",  # GFDL is share-alike
    "fal": "CC_BY",  # Free Art License
}


def normalize_license(raw: str) -> str:
    """Map a Commons license short-name to our license_class slug."""
    if not raw:
        return "unknown"
    lower = raw.lower().strip()
    # Direct match
    if lower in LICENSE_MAP:
        return LICENSE_MAP[lower]
    # Prefix match
    for k, v in LICENSE_MAP.items():
        if lower.startswith(k):
            return v
    # CC-BY-SA family
    if "cc-by-sa" in lower:
        return "CC_BY_SA"
    if "cc-by" in lower and "nc" in lower:
        return "CC_BY_NC"
    if "cc-by" in lower:
        return "CC_BY"
    if "cc0" in lower or "public domain" in lower or "pd" in lower:
        return "CC0"
    return "unknown"


def extract_filename_from_url(url: str) -> str | None:
    """
    Extract the Commons file name from a URL.
    Handles:
    - https://commons.wikimedia.org/wiki/File:Katana.jpg
    - https://commons.wikimedia.org/wiki/Special:FilePath/Katana.jpg
    - http://commons.wikimedia.org/wiki/Special:FilePath/Katana%20weapon.jpg
    - https://upload.wikimedia.org/wikipedia/commons/a/ab/Katana.jpg
    - https://commons.wikimedia.org/w/index.php?title=File:Katana.jpg
    """
    if not url:
        return None

    # Special:FilePath/... (Wikidata P18 image URLs use this pattern)
    m = re.search(r"/Special:FilePath/(.+?)(?:\?|$)", url, re.IGNORECASE)
    if m:
        return unquote(m.group(1).replace("_", " "))

    # commons.wikimedia.org/wiki/File:...
    m = re.search(r"/wiki/File:(.+?)(?:\?|$)", url, re.IGNORECASE)
    if m:
        return unquote(m.group(1).replace("_", " "))

    # upload.wikimedia.org path: last path component
    parsed = urlparse(url)
    if "upload.wikimedia.org" in parsed.netloc:
        filename = parsed.path.rsplit("/", 1)[-1]
        return unquote(filename.replace("_", " "))

    # Fallback: anything after File:
    m = re.search(r"File:(.+?)(?:\?|$)", url, re.IGNORECASE)
    if m:
        return unquote(m.group(1).replace("_", " "))

    return None


def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-16000")
    return conn


def get_unenriched_images(conn: sqlite3.Connection) -> list[tuple]:
    """Return image rows that need enrichment (no license or no dimensions)."""
    rows = conn.execute(
        """
        SELECT id, image_url
        FROM knowledge_entry_reference_images
        WHERE (image_url LIKE '%commons.wikimedia.org%'
               OR image_url LIKE '%upload.wikimedia.org%')
          AND (license_class IS NULL OR license_class = 'Commons-various'
               OR width_px IS NULL)
        ORDER BY id
        """
    ).fetchall()
    return rows


def fetch_image_metadata(filename: str, retries: int = 3) -> dict | None:
    """Call Commons API for image license + dimensions."""
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "format": "json",
    }
    headers = {
        "User-Agent": UA,
        "Accept": "application/json",
    }

    for attempt in range(retries):
        try:
            resp = requests.get(COMMONS_API, params=params, headers=headers, timeout=20)
            if resp.status_code == 429:
                wait = 10 * (attempt + 1)
                log.warning(f"Rate-limited (429) for {filename}. Waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()

            pages = data.get("query", {}).get("pages", {})
            for page_id, page in pages.items():
                if page_id == "-1":
                    return None  # File not found
                imageinfo = page.get("imageinfo", [])
                if not imageinfo:
                    return None
                info = imageinfo[0]
                extmeta = info.get("extmetadata", {})

                # License extraction
                license_short = extmeta.get("LicenseShortName", {}).get("value", "")
                license_url = extmeta.get("LicenseUrl", {}).get("value", "")

                # Try artist/attribution
                artist = extmeta.get("Artist", {}).get("value", "")
                # Strip HTML tags from artist
                artist = re.sub(r"<[^>]+>", "", artist).strip()

                return {
                    "license_raw": license_short,
                    "license_class": normalize_license(license_short),
                    "license_url": license_url,
                    "width_px": info.get("width"),
                    "height_px": info.get("height"),
                    "artist": artist[:500] if artist else None,
                    "canonical_url": info.get("url"),  # Direct file URL
                }
            return None

        except requests.exceptions.Timeout:
            log.warning(f"Timeout for {filename} attempt {attempt+1}")
            if attempt < retries - 1:
                time.sleep(5)
        except Exception as e:
            log.warning(f"API error for {filename}: {e}")
            if attempt < retries - 1:
                time.sleep(5)

    return None


def enrich_images(conn: sqlite3.Connection) -> tuple[int, int, int]:
    """Main enrichment loop. Returns (enriched, skipped_not_found, errors)."""
    rows = get_unenriched_images(conn)
    log.info(f"Found {len(rows)} Commons images to enrich")

    enriched = 0
    not_found = 0
    errors = 0
    pending = []

    for i, (row_id, image_url) in enumerate(rows):
        filename = extract_filename_from_url(image_url)
        if not filename:
            log.warning(f"Cannot extract filename from: {image_url}")
            errors += 1
            continue

        metadata = fetch_image_metadata(filename)

        if metadata is None:
            not_found += 1
            # Mark as extraction_error = 'not_found' to avoid re-querying
            pending.append((row_id, None, None, None, "not_found_on_commons"))
        else:
            pending.append((
                row_id,
                metadata["license_class"],
                metadata.get("width_px"),
                metadata.get("height_px"),
                None,  # no error
            ))
            enriched += 1

        # Batch commit
        if len(pending) >= BATCH_COMMIT:
            _commit_enrichments(conn, pending)
            pending = []
            log.info(f"  Progress: {i+1}/{len(rows)} | enriched={enriched} not_found={not_found}")

        time.sleep(REQUEST_DELAY)

    # Flush remainder
    if pending:
        _commit_enrichments(conn, pending)

    log.info(f"Enrichment complete: enriched={enriched} not_found={not_found} errors={errors}")
    return enriched, not_found, errors


def _commit_enrichments(conn: sqlite3.Connection, pending: list):
    with conn:
        for row_id, license_class, width_px, height_px, error in pending:
            try:
                if error:
                    conn.execute(
                        "UPDATE knowledge_entry_reference_images SET license_class=? WHERE id=?",
                        (error, row_id),
                    )
                else:
                    conn.execute(
                        """
                        UPDATE knowledge_entry_reference_images
                        SET license_class=?, width_px=?, height_px=?
                        WHERE id=?
                        """,
                        (license_class, width_px, height_px, row_id),
                    )
            except sqlite3.Error as e:
                log.warning(f"DB update error for row {row_id}: {e}")


def write_summary(enriched: int, not_found: int, errors: int, start_time: float):
    summary = {}
    if os.path.exists(SUMMARY_PATH):
        try:
            with open(SUMMARY_PATH) as f:
                summary = json.load(f)
        except Exception:
            pass

    summary["a1_3_commons"] = {
        "images_enriched": enriched,
        "images_not_found": not_found,
        "errors": errors,
        "runtime_seconds": round(time.time() - start_time, 1),
        "completed_at": datetime.utcnow().isoformat() + "Z",
        "status": "complete",
    }

    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)
    log.info(f"Summary updated: {SUMMARY_PATH}")


def main():
    start_time = time.time()
    log.info("=== A1.3 Commons image enrichment starting ===")
    log.info(f"DB: {DB_PATH}")
    log.info(f"API: {COMMONS_API}")
    log.info(f"Rate: 1 req/{REQUEST_DELAY}s")

    conn = get_db()

    # Check how many images need enrichment
    total = conn.execute(
        """
        SELECT COUNT(*) FROM knowledge_entry_reference_images
        WHERE (image_url LIKE '%commons.wikimedia.org%'
               OR image_url LIKE '%upload.wikimedia.org%')
          AND (license_class IS NULL
               OR license_class = 'Commons-various'
               OR width_px IS NULL)
        """
    ).fetchone()[0]

    if total == 0:
        log.info("No Commons images need enrichment. Check that A1.1 has run.")
        log.info("A1.3 will exit and can be re-run after A1.1 produces image rows.")
        # Don't exit with error — this is expected if A1.3 fires before A1.1 completes
        write_summary(0, 0, 0, start_time)
        conn.close()
        return

    estimated_hours = total / 3600
    log.info(f"Images to enrich: {total} | Estimated wall time: {estimated_hours:.1f} hours")

    enriched, not_found, errors = enrich_images(conn)

    # Final DB counts
    enriched_db = conn.execute(
        """
        SELECT COUNT(*) FROM knowledge_entry_reference_images
        WHERE license_class IS NOT NULL AND license_class != 'Commons-various'
          AND (image_url LIKE '%commons.wikimedia.org%' OR image_url LIKE '%upload.wikimedia.org%')
        """
    ).fetchone()[0]

    log.info(f"=== A1.3 COMPLETE ===")
    log.info(f"  Images enriched this run: {enriched}")
    log.info(f"  Images not found on Commons: {not_found}")
    log.info(f"  Errors: {errors}")
    log.info(f"  Total enriched in DB: {enriched_db}")
    log.info(f"  Wall time: {(time.time()-start_time)/3600:.2f} hours")

    write_summary(enriched, not_found, errors, start_time)
    conn.close()


if __name__ == "__main__":
    main()
