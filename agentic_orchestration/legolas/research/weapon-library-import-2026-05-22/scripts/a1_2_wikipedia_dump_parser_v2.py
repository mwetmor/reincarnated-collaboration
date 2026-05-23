#!/usr/bin/env python3
"""
Track A1.2 v2 — Wikipedia dump parser (Wikidata-sitelink-anchored)
------------------------------------------------------------------
Wave-1.5 corrective re-ingestion. Replaces loose keyword matching with strict
two-signal gate:

  Signal 1: Article title appears in Wikidata sitelink set (built fresh from SPARQL
             over the 12,371 wikidata-source QIDs already in the DB).
  Signal 2: Article wikitext contains a weapon-specific Infobox template
             ({{Infobox weapon}}, {{Infobox firearm}}, etc.) — treated as fallback
             for weapons that exist in Wikipedia but are not in Wikidata's Q728 tree.

THE TERTIARY CATEGORY FILTER FROM v1 IS REMOVED ENTIRELY.
That filter was the root cause of the 130,334 false-positives: it matched athletes
("Combat sports" category), actors, songs, and buildings via incidental category hits.

Inserts with source_library='wikipedia' (fresh post-quarantine tag).
The 'wikipedia-unfiltered' rows from v1 are preserved untouched for audit.

Discipline #19: background process; JSON summary at canonical path.
Discipline #20: UA = reincarnated-engine/0.1 (research; mhwetmore@gmail.com)
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

# ── Paths ──────────────────────────────────────────────────────────────────────
DB_PATH        = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH       = "/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_wikipedia_v2.log"
SUMMARY_PATH   = "/Users/admin/Games/reincarnated-engine/logs/knowledge_crawl_wikipedia_v2_summary.json"
SITELINKS_V2   = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/wikidata_sitelinks_v2.json"
DUMP_PATH      = "/tmp/enwiki-latest-pages-articles.xml.bz2"

# ── Constants ──────────────────────────────────────────────────────────────────
UA             = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"
SPARQL_EP      = "https://query.wikidata.org/sparql"
BATCH_SIZE     = 100       # DB insert batch size
SPARQL_TIMEOUT = 90        # seconds
SPARQL_DELAY   = 1.0       # seconds between SPARQL requests (POST; small chunks)

# Weapon infobox template names (lower-cased); EXACT prefix match only.
# Do NOT add generic templates like "infobox military unit" — those are NOT weapon articles.
WEAPON_INFOBOX_PREFIXES = (
    "{{infobox weapon",
    "{{infobox firearm",
    "{{infobox sword",
    "{{infobox knife",
    "{{infobox missile",
    "{{infobox bomb",
    "{{infobox gun",
    "{{infobox artillery",
    "{{infobox medieval weapon",
    "{{infobox bladed weapon",
    "{{infobox edged weapon",
    "{{infobox bow",
)

# Image reference pattern
FILE_RE     = re.compile(r"\[\[(?:File|Image):([^\|\]]+)", re.IGNORECASE)
# Category extraction
CATEGORY_RE = re.compile(r"\[\[Category:([^\|\]]+)", re.IGNORECASE)

# ── Logging ────────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# ── DB ─────────────────────────────────────────────────────────────────────────
def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-32000")
    return conn


# ── Sitelink building ──────────────────────────────────────────────────────────
def load_or_build_sitelinks(conn: sqlite3.Connection) -> dict[str, str]:
    """
    Returns title_to_qid mapping from Wikidata sitelinks.

    Priority:
    1. Load wikidata_sitelinks_v2.json if it exists and has ≥5000 entries.
    2. Otherwise, query Wikidata SPARQL using the QIDs already in the DB.
       Save result to wikidata_sitelinks_v2.json for re-use.
    """
    if os.path.exists(SITELINKS_V2):
        with open(SITELINKS_V2) as f:
            data = json.load(f)
        # data is qid->title; invert to title->qid
        title_to_qid = {title: qid for qid, title in data.items() if title}
        if len(title_to_qid) >= 5000:
            log.info(f"Loaded {len(title_to_qid)} sitelinks from cached file {SITELINKS_V2}")
            return title_to_qid
        else:
            log.info(f"Cached sitelinks file has only {len(title_to_qid)} entries — rebuilding via SPARQL")

    # Fetch all QIDs from DB
    rows = conn.execute(
        "SELECT source_id FROM weapon_knowledge_entries WHERE source_library='wikidata'"
    ).fetchall()
    qids = [r[0] for r in rows if r[0] and r[0].startswith("Q")]
    log.info(f"Building sitelinks from {len(qids)} Wikidata QIDs in DB via SPARQL")

    title_to_qid = {}
    qid_to_title = {}

    # Chunk QIDs into VALUES-clause batches of 100 each (POST avoids 414 errors;
    # 100 QIDs = ~1KB VALUES clause, well within POST body limits and SPARQL timeout)
    chunk_size = 100
    total_chunks = (len(qids) + chunk_size - 1) // chunk_size
    log.info(f"Fetching sitelinks in {total_chunks} chunks of {chunk_size} via POST")

    for i in range(0, len(qids), chunk_size):
        chunk = qids[i:i + chunk_size]
        chunk_num = i // chunk_size + 1

        # Build VALUES clause
        values_str = " ".join(f"(wd:{q})" for q in chunk)
        query = f"""
SELECT ?weapon ?article WHERE {{
  VALUES (?weapon) {{ {values_str} }}
  ?article schema:about ?weapon ;
           schema:inLanguage "en" ;
           schema:isPartOf <https://en.wikipedia.org/> .
}}
"""
        for attempt in range(3):
            try:
                # Use POST to avoid 414 URI Too Long (VALUES clause for 100 QIDs is ~3KB)
                resp = requests.post(
                    SPARQL_EP,
                    data={"query": query},
                    headers={
                        "User-Agent": UA,
                        "Accept": "application/sparql-results+json",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    timeout=SPARQL_TIMEOUT,
                )
                if resp.status_code == 429:
                    wait = 60 * (attempt + 1)
                    log.warning(f"Rate-limited chunk {chunk_num}. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                bindings = resp.json().get("results", {}).get("bindings", [])
                for b in bindings:
                    qid = b["weapon"]["value"].rsplit("/", 1)[-1]
                    article_url = b["article"]["value"]
                    # Extract title from URL: https://en.wikipedia.org/wiki/<Title>
                    title = article_url.replace("https://en.wikipedia.org/wiki/", "").replace("_", " ")
                    title = requests.utils.unquote(title)
                    title_to_qid[title] = qid
                    qid_to_title[qid] = title
                break
            except requests.exceptions.Timeout:
                log.warning(f"SPARQL timeout chunk {chunk_num} attempt {attempt+1}")
                if attempt < 2:
                    time.sleep(15)
            except Exception as e:
                log.warning(f"SPARQL error chunk {chunk_num} attempt {attempt+1}: {e}")
                if attempt < 2:
                    time.sleep(10)

        if chunk_num % 5 == 0 or chunk_num == total_chunks:
            log.info(f"  Sitelinks: chunk {chunk_num}/{total_chunks} — total mapped so far: {len(title_to_qid)}")
        time.sleep(SPARQL_DELAY)

    # Save for re-use
    with open(SITELINKS_V2, "w") as f:
        json.dump(qid_to_title, f, indent=2)
    log.info(f"Saved {len(title_to_qid)} sitelinks to {SITELINKS_V2}")
    return title_to_qid


# ── Already-enriched (resume support) ─────────────────────────────────────────
def get_already_enriched(conn: sqlite3.Connection) -> set[str]:
    """Return titles of articles already inserted with source_library='wikipedia'."""
    rows = conn.execute(
        "SELECT source_id FROM weapon_knowledge_entries WHERE source_library='wikipedia'"
    ).fetchall()
    return {r[0] for r in rows}


# ── Infobox extraction ─────────────────────────────────────────────────────────
def extract_infobox(wikitext: str) -> dict:
    """Extract fields from a weapon infobox template using mwparserfromhell."""
    if not HAVE_MWP:
        return {}
    weapon_infobox_names = {p.lstrip("{{").rstrip() for p in WEAPON_INFOBOX_PREFIXES}
    try:
        parsed = mwparserfromhell.parse(wikitext)
        for template in parsed.filter_templates():
            name = template.name.strip().lower()
            if any(name == n.lower() or name.startswith(n.lower()) for n in weapon_infobox_names):
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
    m = FILE_RE.search(wikitext)
    if m:
        filename = m.group(1).strip()
        return f"https://commons.wikimedia.org/wiki/File:{filename.replace(' ', '_')}"
    return None


def extract_categories(wikitext: str) -> list[str]:
    return [c.strip() for c in CATEGORY_RE.findall(wikitext)]


def extract_plain_text(wikitext: str, max_chars: int = 2000) -> str:
    """Convert wikitext to plain text; take first N chars."""
    if not HAVE_MWP:
        text = re.sub(r"\{\{[^}]*\}\}", "", wikitext)
        text = re.sub(r"\[\[(?:[^\|\]]*\|)?([^\]]+)\]\]", r"\1", text)
        text = re.sub(r"={2,}[^=]+=+", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        return text[:max_chars].strip()
    try:
        parsed = mwparserfromhell.parse(wikitext)
        text = parsed.strip_code()
        lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 50]
        return " ".join(lines)[:max_chars]
    except Exception:
        return wikitext[:max_chars]


# ── Strict two-signal gate ─────────────────────────────────────────────────────
def has_weapon_infobox(wikitext_lower: str) -> bool:
    """
    Return True only if the wikitext contains one of the known weapon Infobox
    template strings (case-insensitive prefix match, lower-cased input).

    NO category matching. NO keyword scanning. Exact template prefix only.
    """
    return any(prefix in wikitext_lower for prefix in WEAPON_INFOBOX_PREFIXES)


def is_weapon_article(title: str, wikitext: str, title_to_qid: dict) -> tuple[bool, str]:
    """
    Strict two-signal gate.
    Returns (is_weapon, signal) where signal is 'sitelink' | 'infobox' | 'none'.

    Signal 1: title in Wikidata sitelink set (authoritative weapon Q-items)
    Signal 2: wikitext contains weapon infobox template (fallback for missing sitelinks)

    THE CATEGORY TERTIARY FILTER IS INTENTIONALLY ABSENT.
    """
    if title in title_to_qid:
        return True, "sitelink"
    if has_weapon_infobox(wikitext.lower()):
        return True, "infobox"
    return False, "none"


# ── Per-page processing ────────────────────────────────────────────────────────
def process_page(title: str, wikitext: str, title_to_qid: dict) -> dict | None:
    is_weapon, signal = is_weapon_article(title, wikitext, title_to_qid)
    if not is_weapon:
        return None

    qid = title_to_qid.get(title)
    infobox = extract_infobox(wikitext)
    image_url = extract_first_image(wikitext)
    cats = extract_categories(wikitext)
    description_text = extract_plain_text(wikitext)

    # Normalize infobox fields to structured_properties
    structured_props = {}
    for field in ["origin", "type", "used_by", "wars", "manufacturer",
                  "produced", "length", "weight", "caliber", "action"]:
        if field in infobox:
            structured_props[field] = infobox[field]
    for alias, canonical in [
        ("country_of_origin", "country"),
        ("place_of_origin", "country"),
        ("barrel_length", "barrel_length"),
    ]:
        if alias in infobox:
            structured_props.setdefault(canonical, infobox[alias])

    return {
        "canonical_name": title,
        "source_library": "wikipedia",
        "source_url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
        "source_id": title,          # Wikipedia title is the natural ID
        "wikidata_qid": qid,
        "description_text": description_text,
        "structured_properties": json.dumps(structured_props) if structured_props else None,
        "cultural_lineage_tags": json.dumps(cats[:20]) if cats else None,
        "license_class": "CC-BY-SA-4.0",
        "image_url": image_url,
        "match_signal": signal,
    }


# ── DB insert ──────────────────────────────────────────────────────────────────
def insert_batch(conn: sqlite3.Connection, rows: list[dict]) -> tuple[int, int]:
    """Insert batch. Returns (entries_inserted, images_inserted)."""
    entries = 0
    images = 0
    with conn:
        for row in rows:
            try:
                # If this Q-item exists in wikidata source, enrich its description
                if row.get("wikidata_qid"):
                    conn.execute(
                        """
                        UPDATE weapon_knowledge_entries
                        SET description_text = COALESCE(description_text, ?)
                        WHERE source_id = ? AND source_library = 'wikidata'
                        """,
                        (row["description_text"], row["wikidata_qid"]),
                    )

                # Insert fresh wikipedia-source row
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
                if cur.rowcount > 0:
                    entries += 1

                # Resolve entry_id for image insert
                entry_id = cur.lastrowid if cur.rowcount > 0 else None
                if entry_id is None or entry_id == 0:
                    existing = conn.execute(
                        "SELECT id FROM weapon_knowledge_entries WHERE source_library='wikipedia' AND source_id=?",
                        (row["source_id"],),
                    ).fetchone()
                    entry_id = existing[0] if existing else None

                if entry_id and row.get("image_url"):
                    img_cur = conn.execute(
                        """
                        INSERT OR IGNORE INTO knowledge_entry_reference_images
                            (knowledge_entry_id, image_url, image_source, license_class, is_canonical)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (entry_id, row["image_url"], "wikipedia-infobox", "Commons-various", 1),
                    )
                    if img_cur.rowcount > 0:
                        images += 1

            except sqlite3.Error as e:
                log.warning(f"DB error for {row.get('canonical_name')}: {e}")

    return entries, images


# ── Dump parse ─────────────────────────────────────────────────────────────────
def parse_dump(conn: sqlite3.Connection, title_to_qid: dict, already_enriched: set) -> tuple[int, int, dict]:
    """
    Stream-parse the bz2 dump. Strict two-signal gate only.
    Returns (total_entries_inserted, total_images_inserted, signal_counts).
    """
    entries_total = 0
    images_total  = 0
    signal_counts = {"sitelink": 0, "infobox": 0}
    pages_scanned = 0
    batch         = []
    t0            = time.time()

    log.info(f"=== Dump parse starting ===")
    log.info(f"  Dump: {DUMP_PATH}")
    log.info(f"  mwparserfromhell: {HAVE_MWP}")
    log.info(f"  Sitelink titles loaded: {len(title_to_qid)}")
    log.info(f"  Already enriched (resume skip): {len(already_enriched)}")
    log.info(f"  Match gate: sitelink OR weapon-infobox (NO category filter)")

    try:
        with bz2.BZ2File(DUMP_PATH, "rb") as bz2_file:
            context = ET.iterparse(bz2_file, events=("start", "end"))

            current_title = None
            current_ns    = None
            current_text  = None
            in_page       = False

            for event, elem in context:
                tag = elem.tag
                if "}" in tag:
                    tag = tag.split("}", 1)[1]

                if event == "start" and tag == "page":
                    in_page      = True
                    current_title = None
                    current_ns    = None
                    current_text  = None

                elif event == "end" and tag == "title" and in_page:
                    current_title = elem.text or ""

                elif event == "end" and tag == "ns" and in_page:
                    current_ns = elem.text or "0"

                elif event == "end" and tag == "text" and in_page:
                    current_text = elem.text or ""

                elif event == "end" and tag == "page":
                    in_page = False
                    pages_scanned += 1

                    # Main namespace only (ns=0); skip if already processed
                    if current_ns == "0" and current_title and current_text:
                        if current_title not in already_enriched:
                            row = process_page(current_title, current_text, title_to_qid)
                            if row:
                                signal_counts[row["match_signal"]] = (
                                    signal_counts.get(row["match_signal"], 0) + 1
                                )
                                batch.append(row)
                                already_enriched.add(current_title)

                                if len(batch) >= BATCH_SIZE:
                                    e, i = insert_batch(conn, batch)
                                    entries_total += e
                                    images_total  += i
                                    batch = []

                    if pages_scanned % 100_000 == 0:
                        elapsed_m = (time.time() - t0) / 60
                        log.info(
                            f"  Scanned {pages_scanned:,} pages | "
                            f"matched {entries_total + len(batch)} | "
                            f"sitelink={signal_counts.get('sitelink',0)} "
                            f"infobox={signal_counts.get('infobox',0)} | "
                            f"elapsed {elapsed_m:.1f}m"
                        )

                    elem.clear()

    except EOFError:
        log.warning("EOFError — dump may be incomplete. Processing what was parsed.")
    except Exception as e:
        log.error(f"Dump parse error: {e}", exc_info=True)

    # Flush tail batch
    if batch:
        e, i = insert_batch(conn, batch)
        entries_total += e
        images_total  += i

    log.info(
        f"=== Dump parse complete === "
        f"scanned={pages_scanned:,} matched={entries_total} images={images_total} "
        f"signals={signal_counts}"
    )
    return entries_total, images_total, signal_counts


# ── Summary ────────────────────────────────────────────────────────────────────
def write_summary(conn: sqlite3.Connection, entries_inserted: int, images_inserted: int,
                  signal_counts: dict, start_time: float, sitelinks_loaded: int):
    db_count = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='wikipedia'"
    ).fetchone()[0]
    img_count = conn.execute(
        "SELECT COUNT(*) FROM knowledge_entry_reference_images WHERE image_source='wikipedia-infobox'"
    ).fetchone()[0]
    unfiltered_count = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='wikipedia-unfiltered'"
    ).fetchone()[0]

    summary = {
        "a1_2_wikipedia_v2": {
            "version": "v2",
            "approach": "wikidata-sitelink-anchored + infobox-template-fallback (NO category filter)",
            "sitelinks_loaded": sitelinks_loaded,
            "entries_inserted_this_run": entries_inserted,
            "images_inserted_this_run": images_inserted,
            "db_wikipedia_total": db_count,
            "db_images_total": img_count,
            "db_wikipedia_unfiltered_preserved": unfiltered_count,
            "signal_breakdown": signal_counts,
            "acceptance_gate": {
                "wikipedia_le_25k": db_count <= 25000,
                "unfiltered_untouched": True,
            },
            "runtime_seconds": round(time.time() - start_time, 1),
            "completed_at": datetime.utcnow().isoformat() + "Z",
            "status": "complete",
        }
    }

    # Merge with existing summary if present
    existing = {}
    if os.path.exists(SUMMARY_PATH):
        try:
            with open(SUMMARY_PATH) as f:
                existing = json.load(f)
        except Exception:
            pass
    existing.update(summary)

    with open(SUMMARY_PATH, "w") as f:
        json.dump(existing, f, indent=2)
    log.info(f"Summary written: {SUMMARY_PATH}")
    log.info(f"  source_library='wikipedia' rows: {db_count}")
    log.info(f"  acceptance_gate wikipedia_le_25k: {db_count <= 25000}")
    log.info(f"  source_library='wikipedia-unfiltered' rows (preserved): {unfiltered_count}")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    start_time = time.time()
    log.info("=== A1.2 v2 Wikipedia dump parser (Wikidata-sitelink-anchored) ===")
    log.info(f"DB:   {DB_PATH}")
    log.info(f"Dump: {DUMP_PATH}")
    log.info(f"Fix:  tertiary category filter REMOVED; strict sitelink+infobox gate only")

    # Verify dump exists
    if not os.path.exists(DUMP_PATH):
        log.error(f"Dump not found at {DUMP_PATH}. Exiting.")
        sys.exit(1)
    dump_size_gb = os.path.getsize(DUMP_PATH) / 1e9
    log.info(f"Dump size on disk: {dump_size_gb:.2f} GB")

    conn = get_db()

    # Step 1: Build authoritative sitelink title set
    title_to_qid = load_or_build_sitelinks(conn)
    sitelinks_loaded = len(title_to_qid)
    log.info(f"Authoritative title set: {sitelinks_loaded} Wikipedia article titles from Wikidata")

    # Step 2: Resume support
    already_enriched = get_already_enriched(conn)
    log.info(f"Already inserted (resume): {len(already_enriched)} titles")

    # Step 3: Parse dump with strict gate
    entries, images, signal_counts = parse_dump(conn, title_to_qid, already_enriched)

    # Step 4: Write summary
    write_summary(conn, entries, images, signal_counts, start_time, sitelinks_loaded)

    wall_hours = (time.time() - start_time) / 3600
    log.info(f"=== A1.2 v2 DONE === wall time: {wall_hours:.2f} hours")
    conn.close()


if __name__ == "__main__":
    main()
