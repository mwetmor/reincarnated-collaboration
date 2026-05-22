#!/usr/bin/env python3
"""
Track A1.1 — Wikidata SPARQL weapon Q-item extraction
------------------------------------------------------
Extracts all Q728 (weapon) instances and subclasses from Wikidata via SPARQL.
Writes to weapon_knowledge_entries + knowledge_entry_reference_images.

Discipline #19: fires as background process; checkpoints via DB; resumes cleanly.
Discipline #20: User-Agent = reincarnated-engine/0.1 (research; mhwetmore@gmail.com)
"""

import sqlite3
import requests
import json
import time
import logging
import sys
import os
from datetime import datetime

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = "/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_wikidata.log"
SUMMARY_PATH = "/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_wikipedia_wikidata_commons_summary.json"
SITELINKS_PATH = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/wikidata_sitelinks.json"

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
UA = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"

BATCH_SIZE = 200       # rows per DB transaction
CHUNK_LIMIT = 5000     # rows per SPARQL query
REQUEST_DELAY = 3.0    # seconds between SPARQL requests (conservative)
TIMEOUT = 90           # seconds per SPARQL request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


SPARQL_QUERY_TEMPLATE = """
SELECT ?weapon ?weaponLabel ?description ?image ?country ?countryLabel
       ?inception ?inceptionYear ?material ?materialLabel ?typeLabel
WHERE {{
  ?weapon wdt:P31/wdt:P279* wd:Q728 .
  OPTIONAL {{ ?weapon schema:description ?description . FILTER(LANG(?description) = "en") }}
  OPTIONAL {{ ?weapon wdt:P18 ?image . }}
  OPTIONAL {{ ?weapon wdt:P495 ?country . }}
  OPTIONAL {{ ?weapon wdt:P571 ?inception . }}
  OPTIONAL {{ ?weapon wdt:P186 ?material . }}
  OPTIONAL {{ ?weapon wdt:P31 ?type . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
LIMIT {limit}
OFFSET {offset}
"""

# Fallback: band chunking by Q-ID numeric range when OFFSET fails
SPARQL_BAND_QUERY_TEMPLATE = """
SELECT ?weapon ?weaponLabel ?description ?image ?country ?countryLabel
       ?inception ?material ?materialLabel
WHERE {{
  ?weapon wdt:P31/wdt:P279* wd:Q728 .
  BIND(xsd:integer(SUBSTR(STR(?weapon), 33)) AS ?qnum)
  FILTER(?qnum >= {qmin} && ?qnum < {qmax})
  OPTIONAL {{ ?weapon schema:description ?description . FILTER(LANG(?description) = "en") }}
  OPTIONAL {{ ?weapon wdt:P18 ?image . }}
  OPTIONAL {{ ?weapon wdt:P495 ?country . }}
  OPTIONAL {{ ?weapon wdt:P571 ?inception . }}
  OPTIONAL {{ ?weapon wdt:P186 ?material . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
"""

# Also fetch sitelinks in a separate query for A1.2 to use
SITELINK_QUERY_TEMPLATE = """
SELECT ?weapon ?article
WHERE {{
  ?weapon wdt:P31/wdt:P279* wd:Q728 .
  ?article schema:about ?weapon .
  ?article schema:inLanguage "en" .
  ?article schema:isPartOf <https://en.wikipedia.org/> .
}}
LIMIT {limit}
OFFSET {offset}
"""


def sparql_query(query: str, retries: int = 3) -> list[dict] | None:
    """Fire a SPARQL query; return list of bindings or None on failure."""
    for attempt in range(retries):
        try:
            resp = requests.get(
                SPARQL_ENDPOINT,
                params={"query": query, "format": "json"},
                headers={
                    "User-Agent": UA,
                    "Accept": "application/sparql-results+json",
                },
                timeout=TIMEOUT,
            )
            if resp.status_code == 429:
                wait = 30 * (attempt + 1)
                log.warning(f"Rate-limited (429). Waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code == 500 or resp.status_code == 503:
                wait = 15 * (attempt + 1)
                log.warning(f"Server error {resp.status_code}. Waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            return data.get("results", {}).get("bindings", [])
        except requests.exceptions.Timeout:
            log.warning(f"SPARQL timeout on attempt {attempt+1}")
            if attempt < retries - 1:
                time.sleep(10)
        except Exception as e:
            log.warning(f"SPARQL error attempt {attempt+1}: {e}")
            if attempt < retries - 1:
                time.sleep(10)
    return None


def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-32000")  # 32MB cache
    return conn


def get_resume_offset(conn: sqlite3.Connection) -> int:
    """Find highest offset already processed by checking row count."""
    row = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='wikidata'"
    ).fetchone()
    count = row[0] if row else 0
    # Round down to nearest chunk boundary to avoid gaps
    return (count // CHUNK_LIMIT) * CHUNK_LIMIT


def parse_qid(uri: str) -> str:
    """Extract Q-number from Wikidata URI like http://www.wikidata.org/entity/Q12345"""
    return uri.rsplit("/", 1)[-1] if uri else ""


def normalize_binding(b: dict, key: str) -> str | None:
    v = b.get(key, {}).get("value")
    return v if v else None


def build_structured_props(b: dict) -> dict:
    props = {}
    country = normalize_binding(b, "countryLabel")
    if country:
        props["country"] = country
    inception = normalize_binding(b, "inception")
    if inception:
        props["inception"] = inception[:10]  # ISO date prefix
    material = normalize_binding(b, "materialLabel")
    if material:
        props["material"] = material
    type_label = normalize_binding(b, "typeLabel")
    if type_label:
        props["weapon_type"] = type_label
    return props


def insert_batch(conn: sqlite3.Connection, rows: list[dict], images: list[dict]):
    """Insert a batch of knowledge entries + images in one transaction."""
    with conn:
        for row in rows:
            try:
                cur = conn.execute(
                    """
                    INSERT OR IGNORE INTO weapon_knowledge_entries
                        (canonical_name, source_library, source_url, source_id,
                         description_text, structured_properties, license_class)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row["canonical_name"],
                        row["source_library"],
                        row["source_url"],
                        row["source_id"],
                        row["description_text"],
                        row["structured_properties"],
                        row["license_class"],
                    ),
                )
                entry_id = cur.lastrowid
                # If INSERT OR IGNORE skipped (duplicate), fetch existing id
                if entry_id == 0 or cur.rowcount == 0:
                    existing = conn.execute(
                        "SELECT id FROM weapon_knowledge_entries WHERE source_library=? AND source_url=?",
                        ("wikidata", row["source_url"]),
                    ).fetchone()
                    entry_id = existing[0] if existing else None

                if entry_id and row.get("image_url"):
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO knowledge_entry_reference_images
                            (knowledge_entry_id, image_url, image_source, license_class, is_canonical)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (entry_id, row["image_url"], "wikidata-p18", "Commons-various", 1),
                    )
            except sqlite3.Error as e:
                log.warning(f"DB insert error for {row.get('source_id')}: {e}")


def run_offset_pagination(conn: sqlite3.Connection) -> tuple[int, int, bool]:
    """
    Main extraction loop using OFFSET pagination.
    Returns (entries_inserted, images_inserted, completed_normally).
    """
    entries_inserted = 0
    images_inserted = 0
    offset = get_resume_offset(conn)
    log.info(f"Resuming A1.1 from offset={offset}")

    consecutive_empty = 0

    while True:
        query = SPARQL_QUERY_TEMPLATE.format(limit=CHUNK_LIMIT, offset=offset)
        log.info(f"SPARQL offset={offset} limit={CHUNK_LIMIT}")
        t0 = time.time()
        bindings = sparql_query(query)
        elapsed = time.time() - t0
        log.info(f"  -> {len(bindings) if bindings is not None else 'FAILED'} rows in {elapsed:.1f}s")

        if bindings is None:
            log.error(f"SPARQL failed at offset={offset}. Switching to band strategy.")
            return entries_inserted, images_inserted, False  # signal fallback needed

        if len(bindings) == 0:
            consecutive_empty += 1
            if consecutive_empty >= 2:
                log.info("Two consecutive empty results. Pagination complete.")
                break
        else:
            consecutive_empty = 0

        batch_rows = []
        seen_qids = set()  # dedup within batch

        for b in bindings:
            weapon_uri = normalize_binding(b, "weapon")
            if not weapon_uri:
                continue
            qid = parse_qid(weapon_uri)
            if qid in seen_qids:
                continue
            seen_qids.add(qid)

            label = normalize_binding(b, "weaponLabel") or qid
            description = normalize_binding(b, "description") or ""
            image_url = normalize_binding(b, "image")
            source_url = weapon_uri

            structured_props = build_structured_props(b)

            batch_rows.append({
                "canonical_name": label,
                "source_library": "wikidata",
                "source_url": source_url,
                "source_id": qid,
                "description_text": description,
                "structured_properties": json.dumps(structured_props) if structured_props else None,
                "license_class": "CC0",
                "image_url": image_url,
            })

        if batch_rows:
            insert_batch(conn, batch_rows, [])
            entries_inserted += len(batch_rows)
            images_inserted += sum(1 for r in batch_rows if r.get("image_url"))
            log.info(f"  Inserted {len(batch_rows)} entries (total so far: {entries_inserted})")

        offset += CHUNK_LIMIT
        time.sleep(REQUEST_DELAY)

    return entries_inserted, images_inserted, True


def run_band_strategy(conn: sqlite3.Connection) -> tuple[int, int]:
    """
    Fallback: Q-ID band chunking. Covers Q1 to Q130M in 500K-wide bands.
    Skips bands whose Q-IDs are already in DB.
    """
    log.info("Starting band-chunking fallback strategy.")
    entries_inserted = 0
    images_inserted = 0

    # Get already-inserted source_ids to skip
    existing = set(
        row[0]
        for row in conn.execute(
            "SELECT source_id FROM weapon_knowledge_entries WHERE source_library='wikidata'"
        )
    )
    log.info(f"Skipping {len(existing)} already-imported Q-IDs")

    BAND_SIZE = 500_000
    Q_MAX = 135_000_000  # current Wikidata ceiling

    for qmin in range(1, Q_MAX, BAND_SIZE):
        qmax = qmin + BAND_SIZE
        query = SPARQL_BAND_QUERY_TEMPLATE.format(qmin=qmin, qmax=qmax)
        log.info(f"Band Q{qmin}–Q{qmax}")
        t0 = time.time()
        bindings = sparql_query(query)
        elapsed = time.time() - t0

        if bindings is None:
            log.warning(f"Band Q{qmin}–Q{qmax} failed; skipping.")
            time.sleep(REQUEST_DELAY * 2)
            continue

        if not bindings:
            time.sleep(REQUEST_DELAY / 2)
            continue

        log.info(f"  -> {len(bindings)} rows in {elapsed:.1f}s")

        batch_rows = []
        for b in bindings:
            weapon_uri = normalize_binding(b, "weapon")
            if not weapon_uri:
                continue
            qid = parse_qid(weapon_uri)
            if qid in existing:
                continue
            existing.add(qid)

            label = normalize_binding(b, "weaponLabel") or qid
            description = normalize_binding(b, "description") or ""
            image_url = normalize_binding(b, "image")
            structured_props = build_structured_props(b)

            batch_rows.append({
                "canonical_name": label,
                "source_library": "wikidata",
                "source_url": weapon_uri,
                "source_id": qid,
                "description_text": description,
                "structured_properties": json.dumps(structured_props) if structured_props else None,
                "license_class": "CC0",
                "image_url": image_url,
            })

        if batch_rows:
            insert_batch(conn, batch_rows, [])
            entries_inserted += len(batch_rows)
            images_inserted += sum(1 for r in batch_rows if r.get("image_url"))

        time.sleep(REQUEST_DELAY)

    return entries_inserted, images_inserted


def fetch_sitelinks(conn: sqlite3.Connection):
    """
    Fetch EN-Wikipedia sitelinks for all wikidata weapon Q-items.
    Saves to SITELINKS_PATH as {qid: wikipedia_title} mapping for A1.2 to use.
    """
    log.info("Fetching EN-Wikipedia sitelinks...")
    sitelinks = {}

    # Load existing if partial run
    if os.path.exists(SITELINKS_PATH):
        with open(SITELINKS_PATH) as f:
            sitelinks = json.load(f)
        log.info(f"  Loaded {len(sitelinks)} existing sitelinks from cache")

    offset = (len(sitelinks) // CHUNK_LIMIT) * CHUNK_LIMIT
    log.info(f"  Resuming sitelinks from offset={offset}")

    consecutive_empty = 0
    while True:
        query = SITELINK_QUERY_TEMPLATE.format(limit=CHUNK_LIMIT, offset=offset)
        bindings = sparql_query(query)

        if bindings is None:
            log.warning(f"Sitelink query failed at offset={offset}; stopping sitelink fetch.")
            break

        if not bindings:
            consecutive_empty += 1
            if consecutive_empty >= 2:
                break
        else:
            consecutive_empty = 0
            for b in bindings:
                weapon_uri = normalize_binding(b, "weapon")
                article_url = normalize_binding(b, "article")
                if weapon_uri and article_url:
                    qid = parse_qid(weapon_uri)
                    # Extract title from URL: https://en.wikipedia.org/wiki/Title
                    title = article_url.split("/wiki/", 1)[-1].replace("_", " ")
                    sitelinks[qid] = title

        offset += CHUNK_LIMIT
        time.sleep(REQUEST_DELAY)

        # Checkpoint every 5K
        if offset % (CHUNK_LIMIT * 5) == 0:
            with open(SITELINKS_PATH, "w") as f:
                json.dump(sitelinks, f)
            log.info(f"  Sitelinks checkpoint: {len(sitelinks)} entries at offset={offset}")

    with open(SITELINKS_PATH, "w") as f:
        json.dump(sitelinks, f)
    log.info(f"Sitelinks complete: {len(sitelinks)} Q-item → Wikipedia title mappings saved.")
    return sitelinks


def write_summary(entries: int, images: int, start_time: float, errors: list):
    """Append/update the shared summary JSON with A1.1 results."""
    summary = {}
    if os.path.exists(SUMMARY_PATH):
        try:
            with open(SUMMARY_PATH) as f:
                summary = json.load(f)
        except Exception:
            pass

    summary["a1_1_wikidata"] = {
        "entries_imported": entries,
        "images_imported": images,
        "runtime_seconds": round(time.time() - start_time, 1),
        "errors": errors[-20:],  # last 20 errors
        "completed_at": datetime.utcnow().isoformat() + "Z",
        "status": "complete",
    }

    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)
    log.info(f"Summary written to {SUMMARY_PATH}")


def main():
    start_time = time.time()
    log.info("=== A1.1 Wikidata SPARQL extraction starting ===")
    log.info(f"DB: {DB_PATH}")
    log.info(f"Endpoint: {SPARQL_ENDPOINT}")
    log.info(f"Chunk limit: {CHUNK_LIMIT} | Request delay: {REQUEST_DELAY}s")

    errors = []
    conn = get_db()

    # Phase 1: Main extraction via OFFSET pagination
    entries, images, completed = run_offset_pagination(conn)
    log.info(f"OFFSET pagination: {entries} entries, {images} images")

    if not completed:
        log.info("Falling back to band-chunking strategy...")
        band_entries, band_images = run_band_strategy(conn)
        entries += band_entries
        images += band_images
        log.info(f"Band strategy: +{band_entries} entries, +{band_images} images")

    # Phase 2: Fetch sitelinks for A1.2 (runs after main extraction)
    log.info("Fetching Wikipedia sitelinks for A1.2 handoff...")
    try:
        fetch_sitelinks(conn)
    except Exception as e:
        log.error(f"Sitelink fetch failed: {e}")
        errors.append(f"sitelink_fetch: {e}")

    # Final count from DB (authoritative)
    db_count = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='wikidata'"
    ).fetchone()[0]
    img_count = conn.execute(
        "SELECT COUNT(*) FROM knowledge_entry_reference_images WHERE image_source='wikidata-p18'"
    ).fetchone()[0]

    log.info(f"=== A1.1 COMPLETE ===")
    log.info(f"  DB weapon_knowledge_entries (wikidata): {db_count}")
    log.info(f"  DB knowledge_entry_reference_images (wikidata-p18): {img_count}")
    log.info(f"  Wall time: {(time.time()-start_time)/60:.1f} minutes")

    write_summary(db_count, img_count, start_time, errors)
    conn.close()


if __name__ == "__main__":
    main()
