#!/usr/bin/env python3
"""
Track A1.2 — Wikipedia dump stream-parser for weapon articles
-------------------------------------------------------------
Downloads enwiki-latest-pages-articles.xml.bz2 (stream) and extracts
weapon-related articles matched against Wikidata sitelinks from A1.1.

Enriches weapon_knowledge_entries rows (description_text, structured_properties
from infobox, cultural_lineage_tags from categories) and adds reference images.

Discipline #19: background process; checkpoints per-article; resumes from DB state.
Discipline #20: UA = reincarnated-engine/0.1 (research; mhwetmore@gmail.com)
                Wikipedia policy: use dumps, not api.php page-by-page. Compliant.
"""

import sqlite3
import requests
import bz2
import json
import time
import logging
import sys
import os
import re
from datetime import datetime
from xml.etree import ElementTree as ET

try:
    import mwparserfromhell
    HAVE_MWP = True
except ImportError:
    HAVE_MWP = False

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = "/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_wikipedia.log"
SUMMARY_PATH = "/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_wikipedia_wikidata_commons_summary.json"
SITELINKS_PATH = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/wikidata_sitelinks.json"
DUMP_LOCAL_PATH = "/tmp/enwiki-latest-pages-articles.xml.bz2"
DUMP_URL = "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"

UA = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"
BATCH_SIZE = 100

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# Wikipedia XML namespace
NS_MAP = {"mw": "http://www.mediawiki.org/xml/DTD/MediaWiki"}
MW_NS = "{http://www.mediawiki.org/xml/DTD/MediaWiki}"

# Weapon-related infobox template names
WEAPON_INFOBOX_NAMES = {
    "infobox weapon", "infobox firearm", "infobox sword", "infobox knife",
    "infobox missile", "infobox bomb", "infobox gun", "infobox artillery",
    "infobox military unit weapon", "infobox medieval weapon",
    "infobox bladed weapon", "infobox bow",
}

# Weapon-related category patterns
WEAPON_CATEGORY_PATTERNS = [
    r"weapon", r"sword", r"dagger", r"knife", r"firearms?", r"gun", r"rifle",
    r"pistol", r"bow", r"spear", r"axe", r"mace", r"polearm", r"bladed",
    r"artillery", r"cannon", r"missile", r"explosive", r"armament",
    r"combat", r"martial", r"medieval combat",
]
WEAPON_CAT_RE = re.compile("|".join(WEAPON_CATEGORY_PATTERNS), re.IGNORECASE)

# File reference pattern (first image in article)
FILE_RE = re.compile(r"\[\[(?:File|Image):([^\|\]]+)", re.IGNORECASE)
# Category extraction
CATEGORY_RE = re.compile(r"\[\[Category:([^\|\]]+)", re.IGNORECASE)


def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-32000")
    return conn


def download_dump():
    """Download the dump if not already present. Resume-capable via Content-Range."""
    if os.path.exists(DUMP_LOCAL_PATH):
        size = os.path.getsize(DUMP_LOCAL_PATH)
        log.info(f"Dump already partially downloaded: {size/1e9:.2f} GB at {DUMP_LOCAL_PATH}")
        # Check if complete by trying a HEAD request
        try:
            head = requests.head(DUMP_URL, headers={"User-Agent": UA}, timeout=30)
            remote_size = int(head.headers.get("Content-Length", 0))
            if remote_size > 0 and size >= remote_size:
                log.info("Dump download complete (local size matches remote).")
                return True
        except Exception as e:
            log.warning(f"HEAD check failed: {e}; proceeding with existing file")
            if size > 1e9:  # > 1GB, assume usable partial
                return True

    log.info(f"Downloading Wikipedia dump from {DUMP_URL}")
    log.info("This will take several hours on typical broadband. Running in background.")

    try:
        # Resume support via Range header
        existing_size = os.path.getsize(DUMP_LOCAL_PATH) if os.path.exists(DUMP_LOCAL_PATH) else 0
        headers = {"User-Agent": UA}
        if existing_size > 0:
            headers["Range"] = f"bytes={existing_size}-"

        with requests.get(DUMP_URL, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get("Content-Length", 0)) + existing_size
            mode = "ab" if existing_size > 0 else "wb"
            downloaded = existing_size
            last_log = time.time()

            with open(DUMP_LOCAL_PATH, mode) as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                    f.write(chunk)
                    downloaded += len(chunk)
                    if time.time() - last_log > 60:  # log every minute
                        pct = (downloaded / total * 100) if total else 0
                        log.info(f"  Download progress: {downloaded/1e9:.2f}/{total/1e9:.2f} GB ({pct:.1f}%)")
                        last_log = time.time()

        log.info(f"Download complete: {os.path.getsize(DUMP_LOCAL_PATH)/1e9:.2f} GB")
        return True
    except Exception as e:
        log.error(f"Download failed: {e}")
        return False


def load_sitelinks() -> dict[str, str]:
    """Load QID->title mapping from A1.1 sitelinks file. Returns title->QID mapping."""
    if not os.path.exists(SITELINKS_PATH):
        log.warning(f"Sitelinks file not found at {SITELINKS_PATH}. A1.2 will use category matching only.")
        return {}

    with open(SITELINKS_PATH) as f:
        qid_to_title = json.load(f)

    # Invert: title -> QID (for lookup by article title during parse)
    title_to_qid = {title: qid for qid, title in qid_to_title.items()}
    log.info(f"Loaded {len(title_to_qid)} sitelink mappings (title -> QID)")
    return title_to_qid


def get_already_enriched(conn: sqlite3.Connection) -> set[str]:
    """Return set of Wikipedia article titles already enriched (have description_text from wikipedia)."""
    rows = conn.execute(
        "SELECT source_id FROM weapon_knowledge_entries WHERE source_library='wikipedia'"
    ).fetchall()
    return {row[0] for row in rows}


def extract_infobox(wikitext: str) -> dict:
    """Extract fields from a weapon infobox template."""
    if not HAVE_MWP:
        return {}

    try:
        parsed = mwparserfromhell.parse(wikitext)
        for template in parsed.filter_templates():
            name = template.name.strip().lower()
            if name in WEAPON_INFOBOX_NAMES:
                props = {}
                for param in template.params:
                    key = str(param.name).strip()
                    val = str(param.value).strip()
                    # Strip nested wikilinks/templates for clean text
                    val = re.sub(r"\[\[([^\|\]]+\|)?([^\]]+)\]\]", r"\2", val)
                    val = re.sub(r"\{\{[^}]+\}\}", "", val)
                    val = val.strip()
                    if val:
                        props[key] = val
                return props
        return {}
    except Exception:
        return {}


def extract_first_image(wikitext: str) -> str | None:
    """Extract the first File/Image reference from wikitext."""
    m = FILE_RE.search(wikitext)
    if m:
        filename = m.group(1).strip()
        # Return as Commons API URL format
        return f"https://commons.wikimedia.org/wiki/File:{filename.replace(' ', '_')}"
    return None


def extract_categories(wikitext: str) -> list[str]:
    """Extract all categories from wikitext."""
    cats = CATEGORY_RE.findall(wikitext)
    return [c.strip() for c in cats]


def extract_plain_text(wikitext: str, max_chars: int = 2000) -> str:
    """Convert wikitext to plain text (first N chars of article body)."""
    if not HAVE_MWP:
        # Fallback: crude regex strip
        text = re.sub(r"\{\{[^}]*\}\}", "", wikitext)
        text = re.sub(r"\[\[(?:[^\|\]]*\|)?([^\]]+)\]\]", r"\1", text)
        text = re.sub(r"={2,}[^=]+=+", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        return text[:max_chars].strip()

    try:
        parsed = mwparserfromhell.parse(wikitext)
        text = parsed.strip_code()
        # Remove infobox content (already captured separately)
        # Take first substantial paragraph
        lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 50]
        return " ".join(lines)[:max_chars]
    except Exception:
        return wikitext[:max_chars]


def is_weapon_article(title: str, wikitext: str, cats: list[str], title_to_qid: dict) -> bool:
    """Determine if this article should be imported as a weapon knowledge entry."""
    # Primary: matched via Wikidata sitelink
    if title in title_to_qid:
        return True
    # Secondary: has weapon infobox
    wikitext_lower = wikitext.lower()
    if "{{infobox weapon" in wikitext_lower or "{{infobox firearm" in wikitext_lower:
        return True
    # Tertiary: weapon-related categories
    if any(WEAPON_CAT_RE.search(cat) for cat in cats):
        return True
    return False


def process_page(title: str, wikitext: str, title_to_qid: dict) -> dict | None:
    """Extract structured data from a single Wikipedia page. Returns row dict or None."""
    cats = extract_categories(wikitext)

    if not is_weapon_article(title, wikitext, cats, title_to_qid):
        return None

    qid = title_to_qid.get(title)
    infobox = extract_infobox(wikitext)
    image_url = extract_first_image(wikitext)
    description_text = extract_plain_text(wikitext)
    weapon_cats = [c for c in cats if WEAPON_CAT_RE.search(c)]

    # Map infobox fields to structured_properties
    structured_props = {}
    for field in ["origin", "type", "used_by", "wars", "manufacturer", "produced", "length", "weight"]:
        if field in infobox:
            structured_props[field] = infobox[field]
    # Try common aliases
    for alias, canonical in [
        ("country_of_origin", "country"), ("place_of_origin", "country"),
        ("action", "action"), ("caliber", "caliber"), ("barrel_length", "barrel_length"),
    ]:
        if alias in infobox:
            structured_props[canonical] = infobox[alias]

    source_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

    return {
        "canonical_name": title,
        "source_library": "wikipedia",
        "source_url": source_url,
        "source_id": title,  # Wikipedia uses title as ID; QID cross-ref via Wikidata
        "wikidata_qid": qid,
        "description_text": description_text,
        "structured_properties": json.dumps(structured_props) if structured_props else None,
        "cultural_lineage_tags": json.dumps(weapon_cats[:20]) if weapon_cats else None,
        "license_class": "CC-BY-SA-4.0",
        "image_url": image_url,
    }


def insert_batch(conn: sqlite3.Connection, rows: list[dict]):
    with conn:
        for row in rows:
            try:
                # If Wikidata already has this entry (via QID), UPDATE rather than duplicate
                if row.get("wikidata_qid"):
                    conn.execute(
                        """
                        UPDATE weapon_knowledge_entries
                        SET description_text = COALESCE(description_text, ?),
                            cultural_lineage_tags = COALESCE(cultural_lineage_tags, ?)
                        WHERE source_id = ? AND source_library = 'wikidata'
                        """,
                        (row["description_text"], row["cultural_lineage_tags"], row["wikidata_qid"]),
                    )

                # Insert Wikipedia-source row (separate record; canonical merge is post-processing)
                cur = conn.execute(
                    """
                    INSERT OR IGNORE INTO weapon_knowledge_entries
                        (canonical_name, source_library, source_url, source_id,
                         description_text, structured_properties, cultural_lineage_tags,
                         license_class)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row["canonical_name"],
                        row["source_library"],
                        row["source_url"],
                        row["source_id"],
                        row["description_text"],
                        row["structured_properties"],
                        row["cultural_lineage_tags"],
                        row["license_class"],
                    ),
                )
                entry_id = cur.lastrowid
                if entry_id == 0 or cur.rowcount == 0:
                    existing = conn.execute(
                        "SELECT id FROM weapon_knowledge_entries WHERE source_library=? AND source_url=?",
                        ("wikipedia", row["source_url"]),
                    ).fetchone()
                    entry_id = existing[0] if existing else None

                if entry_id and row.get("image_url"):
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO knowledge_entry_reference_images
                            (knowledge_entry_id, image_url, image_source, license_class, is_canonical)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (entry_id, row["image_url"], "wikipedia-infobox", "Commons-various", 1),
                    )
            except sqlite3.Error as e:
                log.warning(f"DB insert error for {row.get('canonical_name')}: {e}")


def parse_dump(conn: sqlite3.Connection, title_to_qid: dict, already_enriched: set) -> tuple[int, int]:
    """Stream-parse the bz2 XML dump. Returns (entries_inserted, images_inserted)."""
    entries_inserted = 0
    images_inserted = 0
    total_pages_scanned = 0
    batch = []
    last_checkpoint = time.time()

    log.info(f"Parsing dump: {DUMP_LOCAL_PATH}")
    log.info(f"  mwparserfromhell available: {HAVE_MWP}")
    log.info(f"  Target articles (sitelinks): {len(title_to_qid)}")
    log.info(f"  Already enriched: {len(already_enriched)}")

    try:
        with bz2.BZ2File(DUMP_LOCAL_PATH, "rb") as bz2_file:
            # Use iterparse to stream without loading full XML into memory
            context = ET.iterparse(bz2_file, events=("start", "end"))

            current_title = None
            current_ns = None
            current_text = None
            in_page = False

            for event, elem in context:
                tag = elem.tag
                # Strip namespace prefix
                if "}" in tag:
                    tag = tag.split("}", 1)[1]

                if event == "start" and tag == "page":
                    in_page = True
                    current_title = None
                    current_ns = None
                    current_text = None

                elif event == "end" and tag == "title" and in_page:
                    current_title = elem.text or ""

                elif event == "end" and tag == "ns" and in_page:
                    current_ns = elem.text or "0"

                elif event == "end" and tag == "text" and in_page:
                    current_text = elem.text or ""

                elif event == "end" and tag == "page":
                    in_page = False
                    total_pages_scanned += 1

                    # Only process main namespace (ns=0)
                    if current_ns == "0" and current_title and current_text:
                        title = current_title
                        if title not in already_enriched:
                            row = process_page(title, current_text, title_to_qid)
                            if row:
                                batch.append(row)
                                already_enriched.add(title)

                                if len(batch) >= BATCH_SIZE:
                                    insert_batch(conn, batch)
                                    entries_inserted += len(batch)
                                    images_inserted += sum(1 for r in batch if r.get("image_url"))
                                    batch = []

                    # Progress log every 100K pages
                    if total_pages_scanned % 100_000 == 0:
                        log.info(
                            f"  Scanned {total_pages_scanned:,} pages | "
                            f"weapon matches: {entries_inserted} | "
                            f"elapsed: {(time.time()-last_checkpoint)/60:.1f}m"
                        )
                        last_checkpoint = time.time()

                    # Clear element to free memory (iterparse discipline)
                    elem.clear()

    except EOFError:
        log.warning("EOFError during dump parse — dump may be incomplete/corrupt. Processing what we have.")
    except Exception as e:
        log.error(f"Dump parse error: {e}")

    # Flush remaining batch
    if batch:
        insert_batch(conn, batch)
        entries_inserted += len(batch)
        images_inserted += sum(1 for r in batch if r.get("image_url"))

    log.info(f"Dump parse complete: scanned {total_pages_scanned:,} pages; matched {entries_inserted} weapon articles")
    return entries_inserted, images_inserted


def write_summary(entries: int, images: int, start_time: float):
    summary = {}
    if os.path.exists(SUMMARY_PATH):
        try:
            with open(SUMMARY_PATH) as f:
                summary = json.load(f)
        except Exception:
            pass

    summary["a1_2_wikipedia"] = {
        "entries_imported": entries,
        "images_imported": images,
        "runtime_seconds": round(time.time() - start_time, 1),
        "completed_at": datetime.utcnow().isoformat() + "Z",
        "status": "complete",
        "dump_path": DUMP_LOCAL_PATH,
    }

    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)
    log.info(f"Summary updated: {SUMMARY_PATH}")


def main():
    start_time = time.time()
    log.info("=== A1.2 Wikipedia dump parser starting ===")
    log.info(f"DB: {DB_PATH}")
    log.info(f"Dump: {DUMP_URL}")
    log.info(f"Local dump path: {DUMP_LOCAL_PATH}")

    # Step 1: Download dump
    ok = download_dump()
    if not ok:
        log.error("Dump download failed. Exiting.")
        sys.exit(1)

    # Step 2: Load sitelinks from A1.1
    conn = get_db()
    title_to_qid = load_sitelinks()
    already_enriched = get_already_enriched(conn)

    # Step 3: Parse dump
    entries, images = parse_dump(conn, title_to_qid, already_enriched)

    # Step 4: Final counts
    db_count = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='wikipedia'"
    ).fetchone()[0]
    img_count = conn.execute(
        "SELECT COUNT(*) FROM knowledge_entry_reference_images WHERE image_source='wikipedia-infobox'"
    ).fetchone()[0]

    log.info(f"=== A1.2 COMPLETE ===")
    log.info(f"  DB weapon_knowledge_entries (wikipedia): {db_count}")
    log.info(f"  DB knowledge_entry_reference_images (wikipedia-infobox): {img_count}")
    log.info(f"  Wall time: {(time.time()-start_time)/3600:.2f} hours")

    write_summary(db_count, img_count, start_time)
    conn.close()


if __name__ == "__main__":
    main()
