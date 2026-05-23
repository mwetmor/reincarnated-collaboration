#!/usr/bin/env python3
"""
Track N — Modern Military Crawl
Sources: ODIN (odin.t2com.army.mil DotCMS API) + Army Recognition
Discipline #20: robots-verified GREEN before this script runs.
Discipline #19: fires as nohup background process.
Discipline #1: math note at track-N-math-note.md.

ODIN: US government public domain (17 U.S.C. § 105) — CC0 equivalent.
Army Recognition: proprietary editorial — license_class='editorial_only'.

Author: legolas (2026-05-22)
"""

import sqlite3
import requests
import json
import time
import re
import sys
import os
import logging
from datetime import date
from urllib.parse import urljoin, urlparse

# ─── Paths ────────────────────────────────────────────────────────────────────
DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
SUMMARY_DIR = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/summaries"
LOG_PATH = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/track-N-crawl.log"
SUMMARY_PATH = os.path.join(SUMMARY_DIR, "track-N-summary-2026-05-22.json")
ERROR_LOG_PATH = os.path.join(SUMMARY_DIR, "track-N-errors-2026-05-22.jsonl")

os.makedirs(SUMMARY_DIR, exist_ok=True)

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("track-N")

# ─── User-Agent (Discipline #20) ──────────────────────────────────────────────
UA = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"
HEADERS = {"User-Agent": UA}

# ─── Constants ────────────────────────────────────────────────────────────────
ODIN_BASE = "https://odin.t2com.army.mil"
ODIN_SEARCH_URL = f"{ODIN_BASE}/dotcms/api/content/_search"
ODIN_IMAGE_BASE = f"{ODIN_BASE}/dA"

AR_BASE = "https://www.armyrecognition.com"
AR_WEAPONS_CATEGORIES = [
    "/military-products/army/weapons/assault-rifles",
    "/military-products/army/weapons/machine-guns",
    "/military-products/army/weapons/pistols",
    "/military-products/army/weapons/sniper-rifles",
    "/military-products/army/weapons/sub-machine-guns",
    "/military-products/army/weapons/grenade-launchers",
    "/military-products/army/weapons/field-equipment",
    "/military-products/army/weapons/turret",
]

CRAWL_DATE = date.today().isoformat()

# ─── Session ──────────────────────────────────────────────────────────────────
session = requests.Session()
session.headers.update(HEADERS)


# ─── Database helpers ─────────────────────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=OFF")  # knowledge entries have no FK to clusters yet
    return conn


def insert_knowledge_entry(conn, row: dict) -> int | None:
    """Insert one weapon_knowledge_entries row. Returns new id or None if duplicate."""
    sql = """
        INSERT OR IGNORE INTO weapon_knowledge_entries (
            canonical_name, source_library, source_url, source_id,
            description_text, structured_properties,
            cultural_lineage_tags, historical_period,
            genre_appearances, related_entries,
            license_class, imported_at
        ) VALUES (
            :canonical_name, :source_library, :source_url, :source_id,
            :description_text, :structured_properties,
            :cultural_lineage_tags, :historical_period,
            :genre_appearances, :related_entries,
            :license_class, datetime('now')
        )
    """
    cur = conn.execute(sql, row)
    return cur.lastrowid if cur.rowcount else None


def insert_reference_image(conn, entry_id: int, img: dict):
    sql = """
        INSERT OR IGNORE INTO knowledge_entry_reference_images (
            knowledge_entry_id, image_url, image_source, license_class,
            is_canonical, image_caption, imported_at
        ) VALUES (
            :entry_id, :image_url, :image_source, :license_class,
            :is_canonical, :image_caption, datetime('now')
        )
    """
    conn.execute(sql, {**img, "entry_id": entry_id})


def log_error(source: str, url: str, err: str):
    with open(ERROR_LOG_PATH, "a") as f:
        f.write(json.dumps({"source": source, "url": url, "error": err, "ts": CRAWL_DATE}) + "\n")


# ─── ODIN crawl ───────────────────────────────────────────────────────────────
ODIN_WEAPON_KEYWORDS = {
    "infantry weapons", "assault rifles", "machine guns", "mortars",
    "grenade launchers", "rocket launchers", "handguns", "grenades",
    "submachine guns", "landmines", "incendiary devices", "rifles",
    "shotguns", "flamethrowers", "recoilless guns", "anti-tank",
    "artillery", "heavy machine", "light machine", "general-purpose machine",
    "sniper", "battle rifles", "carbine", "anti-material",
    "special purpose weapons", "small arms", "ordnance",
}


def odin_is_weapon_relevant(item: dict) -> bool:
    domain_text = item.get("domainSort", "").lower()
    name_lower = item.get("name", "").lower()
    return any(kw in domain_text or kw in name_lower for kw in ODIN_WEAPON_KEYWORDS)


def odin_map_tech_level(date_str: str | None) -> str:
    if not date_str:
        return "advanced"
    try:
        year = int(date_str[:4])
        if year >= 1950:
            return "advanced"
        elif year >= 1800:
            return "industrial"
        elif year >= 1500:
            return "early_modern"
        elif year >= 500:
            return "medieval"
        else:
            return "ancient"
    except Exception:
        return "advanced"


def odin_extract_images(item: dict) -> list[dict]:
    """Parse images JSON array from WegCard."""
    images_raw = item.get("images", "[]")
    if isinstance(images_raw, str):
        try:
            images = json.loads(images_raw)
        except Exception:
            return []
    elif isinstance(images_raw, list):
        images = images_raw
    else:
        return []

    result = []
    for i, img in enumerate(images):
        url_path = img.get("url", "")
        if not url_path:
            continue
        # Resolve to full URL
        if url_path.startswith("/dA/"):
            full_url = f"{ODIN_BASE}{url_path}"
        elif url_path.startswith("http"):
            full_url = url_path
        else:
            full_url = f"{ODIN_BASE}/{url_path.lstrip('/')}"
        result.append({
            "image_url": full_url,
            "image_source": "odin-wegcard-images",
            "license_class": "CC0",
            "is_canonical": 1 if i == 0 else 0,
            "image_caption": img.get("name", ""),
        })
    return result


def odin_normalize_item(item: dict) -> dict:
    """Normalize a WegCard to weapon_knowledge_entries schema."""
    name = item.get("name") or item.get("title", "Unknown")

    # Build structured properties from sections
    sections_raw = item.get("sections", "[]")
    if isinstance(sections_raw, str):
        try:
            sections = json.loads(sections_raw)
        except Exception:
            sections = []
    elif isinstance(sections_raw, list):
        sections = sections_raw
    else:
        sections = []

    # Flatten sections to a dict of {property_name: value}
    props = {}
    for section in sections:
        sec_name = section.get("name", "")
        for prop in section.get("properties", []):
            prop_name = f"{sec_name}.{prop.get('name', '')}" if sec_name else prop.get("name", "")
            props[prop_name] = prop.get("value", "")

    # Origin (countries)
    origin_raw = item.get("origin", [])
    origins = [list(o.values())[0] for o in origin_raw if o]

    # Proliferation (user countries)
    prolif_raw = item.get("proliferation", [])
    prolif = [list(p.values())[0] for p in prolif_raw if p]

    # Domain hierarchy
    domain_raw = item.get("domain", [])
    domains = [list(d.values())[0] for d in domain_raw if d]

    # Date of introduction
    doi = item.get("dateOfIntroduction", "")
    tech_level = odin_map_tech_level(doi)

    # Cultural lineage from origin
    lineage_map = {
        "United States": "european", "United Kingdom": "european",
        "Germany": "european", "France": "european", "Russia": "european",
        "Soviet Union": "european", "China": "east_asian",
        "Japan": "east_asian", "Israel": "middle_eastern",
        "South Korea": "east_asian",
    }
    cultural_lineage = "unknown"
    for country in origins:
        if country in lineage_map:
            cultural_lineage = lineage_map[country]
            break

    # Source URL
    item_id = item.get("identifier", item.get("inode", ""))
    source_url = f"{ODIN_BASE}/WEG/{item_id}"

    structured = {
        "properties": props,
        "domain_hierarchy": domains,
        "origin_countries": origins,
        "proliferation_countries": prolif,
        "date_of_introduction": doi,
        "dotcms_identifier": item_id,
        "odin_domain_sort": item.get("domainSort", ""),
    }

    return {
        "canonical_name": name,
        "source_library": "odin-army-tradoc",
        "source_url": source_url,
        "source_id": item_id,
        "description_text": (item.get("notes") or "")[:4000],
        "structured_properties": json.dumps(structured),
        "cultural_lineage_tags": json.dumps(origins),
        "historical_period": doi[:10] if doi else None,
        "genre_appearances": json.dumps(["modern-military"]),
        "related_entries": json.dumps([]),
        "license_class": "CC0",
    }


def crawl_odin(conn) -> dict:
    log.info("=== ODIN crawl starting ===")
    stats = {"total_fetched": 0, "inserted": 0, "duplicate": 0, "errors": 0, "images_inserted": 0}

    page_size = 200
    offset = 0
    total_expected = None

    while True:
        payload = {
            "query": "+contentType:WegCard +live:true",
            "limit": page_size,
            "offset": offset,
        }
        try:
            resp = session.post(
                ODIN_SEARCH_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            if resp.status_code == 429:
                log.warning("ODIN 429 rate-limit; sleeping 10s")
                time.sleep(10)
                continue
            if resp.status_code != 200:
                log.error(f"ODIN HTTP {resp.status_code} at offset {offset}")
                log_error("odin-army-tradoc", ODIN_SEARCH_URL, f"HTTP {resp.status_code}")
                stats["errors"] += 1
                break

            data = resp.json()
            entity = data["entity"]
            if total_expected is None:
                total_expected = entity["resultsSize"]
                log.info(f"ODIN total WegCard items: {total_expected}")

            items = entity["jsonObjectView"]["contentlets"]
            if not items:
                log.info("ODIN: no more items, crawl complete")
                break

            stats["total_fetched"] += len(items)

            batch_rows = []
            for item in items:
                row = odin_normalize_item(item)
                batch_rows.append((row, item))

            # Batch insert
            with conn:
                for row, item in batch_rows:
                    entry_id = insert_knowledge_entry(conn, row)
                    if entry_id:
                        stats["inserted"] += 1
                        # Insert reference images
                        for img in odin_extract_images(item):
                            try:
                                insert_reference_image(conn, entry_id, img)
                                stats["images_inserted"] += 1
                            except Exception as e:
                                pass
                    else:
                        stats["duplicate"] += 1

            log.info(
                f"ODIN offset={offset}: fetched={len(items)}, "
                f"inserted={stats['inserted']}, dup={stats['duplicate']}"
            )
            offset += page_size
            if offset >= total_expected:
                log.info(f"ODIN: reached end of corpus ({total_expected} items)")
                break

            time.sleep(1.0)  # 1 req/sec — conservative for gov API

        except Exception as e:
            log.error(f"ODIN exception at offset {offset}: {e}")
            log_error("odin-army-tradoc", ODIN_SEARCH_URL, str(e))
            stats["errors"] += 1
            time.sleep(5)
            if stats["errors"] > 5:
                log.error("ODIN: too many errors, aborting ODIN crawl")
                break

    log.info(f"ODIN crawl complete: {stats}")
    return stats


# ─── Army Recognition crawl ───────────────────────────────────────────────────
AR_REQUEST_DELAY = 5.0  # 5 seconds (AMBER caution rate)


def ar_extract_article_links(html: str, category_url: str) -> list[str]:
    """Extract per-weapon article links from a category listing page."""
    # Pattern: href="/military-products/army/weapons/<category>/<slug>"
    pattern = r'href="(/military-products/army/weapons/[^"?#]{10,})"'
    links = re.findall(pattern, html)
    # Filter out category index pages (no slug after category)
    article_links = []
    seen = set()
    for link in links:
        # Category pages have 3 path segments after /military-products/army/weapons/
        # Article pages have 4+ segments
        parts = [p for p in link.split("/") if p]
        if len(parts) >= 5:  # military-products/army/weapons/<cat>/<slug>
            full = urljoin(AR_BASE, link)
            if full not in seen:
                seen.add(full)
                article_links.append(full)
    return article_links


def ar_extract_specs(html: str) -> dict:
    """Extract specification table from an Army Recognition article."""
    specs = {}
    # Army Recognition uses a <table> for specs
    table_matches = re.findall(
        r'<tr[^>]*>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>.*?</tr>',
        html, re.DOTALL | re.IGNORECASE
    )
    for label, value in table_matches:
        label_clean = re.sub(r'<[^>]+>', '', label).strip()
        value_clean = re.sub(r'<[^>]+>', '', value).strip()
        value_clean = re.sub(r'\s+', ' ', value_clean)
        if label_clean and value_clean and len(label_clean) < 80:
            specs[label_clean] = value_clean[:300]
    return specs


def ar_extract_description(html: str) -> str:
    """Extract description text from an Army Recognition article."""
    # Find article body text
    body_match = re.search(
        r'<div[^>]+class="[^"]*content-article[^"]*"[^>]*>(.*?)</div>',
        html, re.DOTALL | re.IGNORECASE
    )
    if body_match:
        body = body_match.group(1)
    else:
        # Fallback: find the first substantive <p> block
        body = html

    # Strip scripts and styles
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:3000]


def ar_extract_image(html: str, article_url: str) -> dict | None:
    """Extract the primary image from an Army Recognition article."""
    img_match = re.search(
        r'data-src="(https://www\.armyrecognition\.com/images/[^"]+\.(?:jpg|jpeg|png|webp))"',
        html, re.IGNORECASE
    )
    if not img_match:
        img_match = re.search(
            r'<img[^>]+src="(https://www\.armyrecognition\.com/images/[^"]+\.(?:jpg|jpeg|png))"',
            html, re.IGNORECASE
        )
    if img_match:
        return {
            "image_url": img_match.group(1),
            "image_source": "army-recognition-article",
            "license_class": "editorial_only",
            "is_canonical": 1,
            "image_caption": "",
        }
    return None


def ar_extract_name(html: str, url: str) -> str:
    """Extract weapon name from article page."""
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
    if h1_match:
        name = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
        name = re.sub(r'\s+', ' ', name)
        if name:
            return name[:200]
    # Fallback: slug from URL
    slug = url.rstrip('/').split('/')[-1]
    return slug.replace('-', ' ').title()


def ar_extract_country(specs: dict, description: str) -> str:
    """Infer country from specs or description for cultural_lineage."""
    country_map = {
        "united states": "european", "american": "european",
        "usa": "european", "u.s.": "european",
        "russia": "european", "russian": "european",
        "soviet": "european", "ussr": "european",
        "germany": "european", "german": "european",
        "france": "european", "french": "european",
        "uk": "european", "british": "european", "britain": "european",
        "belgium": "european", "belgian": "european",
        "china": "east_asian", "chinese": "east_asian",
        "israel": "middle_eastern", "israeli": "middle_eastern",
        "austria": "european", "austrian": "european",
        "czech": "european", "poland": "european",
        "south korea": "east_asian", "korean": "east_asian",
        "japan": "east_asian", "japanese": "east_asian",
    }
    combined = (json.dumps(specs) + " " + description).lower()
    for keyword, lineage in country_map.items():
        if keyword in combined:
            return lineage
    return "unknown"


def ar_normalize_article(url: str, html: str) -> dict:
    """Normalize an Army Recognition article to weapon_knowledge_entries row."""
    name = ar_extract_name(html, url)
    specs = ar_extract_specs(html)
    description = ar_extract_description(html)
    cultural = ar_extract_country(specs, description)

    slug = url.rstrip('/').split('/')[-1]
    # Infer category from URL path
    parts = url.split('/')
    category = parts[-2] if len(parts) >= 2 else "unknown"

    structured = {
        "specifications": specs,
        "category": category,
        "source_slug": slug,
    }

    return {
        "canonical_name": name,
        "source_library": "army-recognition",
        "source_url": url,
        "source_id": slug,
        "description_text": description[:4000],
        "structured_properties": json.dumps(structured),
        "cultural_lineage_tags": json.dumps([cultural]),
        "historical_period": None,
        "genre_appearances": json.dumps(["modern-military"]),
        "related_entries": json.dumps([]),
        "license_class": "editorial_only",
    }


def crawl_army_recognition(conn) -> dict:
    log.info("=== Army Recognition crawl starting ===")
    stats = {"total_fetched": 0, "inserted": 0, "duplicate": 0, "errors": 0, "images_inserted": 0}

    # Step 1: collect all article URLs from category listing pages
    all_article_urls = set()

    for cat_path in AR_WEAPONS_CATEGORIES:
        cat_url = f"{AR_BASE}{cat_path}"
        page_num = 0
        while True:
            fetch_url = cat_url if page_num == 0 else f"{cat_url}?start={page_num * 25}"
            try:
                resp = session.get(fetch_url, timeout=20)
                if resp.status_code == 429:
                    log.warning(f"AR 429 on {fetch_url}, sleeping 15s")
                    time.sleep(15)
                    continue
                if resp.status_code != 200:
                    log.warning(f"AR category {fetch_url} returned {resp.status_code}")
                    break

                html = resp.text
                new_links = ar_extract_article_links(html, cat_url)
                if not new_links:
                    break

                before = len(all_article_urls)
                for link in new_links:
                    all_article_urls.add(link)
                after = len(all_article_urls)

                log.info(f"AR category {cat_path} page {page_num}: found {len(new_links)} links (+{after-before} new)")

                # If no new links were added, we've seen all pages for this category
                if after == before and page_num > 0:
                    break

                page_num += 1
                # Only go up to 10 pages per category (safety limit)
                if page_num >= 10:
                    break

                time.sleep(AR_REQUEST_DELAY)

            except Exception as e:
                log.error(f"AR category error {fetch_url}: {e}")
                log_error("army-recognition", fetch_url, str(e))
                stats["errors"] += 1
                break

        time.sleep(AR_REQUEST_DELAY)

    log.info(f"AR: collected {len(all_article_urls)} unique article URLs")

    # Step 2: fetch and normalize each article
    for article_url in sorted(all_article_urls):
        try:
            resp = session.get(article_url, timeout=20)
            if resp.status_code == 429:
                log.warning(f"AR 429 on {article_url}, sleeping 30s")
                time.sleep(30)
                resp = session.get(article_url, timeout=20)
            if resp.status_code != 200:
                log.warning(f"AR article {article_url} returned {resp.status_code}")
                stats["errors"] += 1
                log_error("army-recognition", article_url, f"HTTP {resp.status_code}")
                time.sleep(AR_REQUEST_DELAY)
                continue

            html = resp.text
            stats["total_fetched"] += 1

            row = ar_normalize_article(article_url, html)
            img = ar_extract_image(html, article_url)

            with conn:
                entry_id = insert_knowledge_entry(conn, row)
                if entry_id:
                    stats["inserted"] += 1
                    if img:
                        try:
                            insert_reference_image(conn, entry_id, img)
                            stats["images_inserted"] += 1
                        except Exception:
                            pass
                else:
                    stats["duplicate"] += 1

            log.info(f"AR article: {row['canonical_name'][:50]} | inserted={bool(entry_id)}")
            time.sleep(AR_REQUEST_DELAY)

        except Exception as e:
            log.error(f"AR article exception {article_url}: {e}")
            log_error("army-recognition", article_url, str(e))
            stats["errors"] += 1
            time.sleep(AR_REQUEST_DELAY)

    log.info(f"AR crawl complete: {stats}")
    return stats


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    log.info("Track N — Modern Military crawl starting")
    log.info(f"DB: {DB_PATH}")
    log.info(f"UA: {UA}")

    conn = get_conn()

    # Pre-crawl DB count
    pre_count = conn.execute("SELECT COUNT(*) FROM weapon_knowledge_entries").fetchone()[0]
    log.info(f"Pre-crawl weapon_knowledge_entries count: {pre_count}")

    summary = {
        "track": "N",
        "crawl_date": CRAWL_DATE,
        "pre_count": pre_count,
        "sources": {},
        "robots_disposition": {
            "odin-army-tradoc": "GREEN — US gov, no robots.txt, public domain API",
            "army-recognition": "GREEN-with-CAUTION — permissive robots.txt, no Claude block, editorial content",
            "globalmilitary-net": "RED (effective) — Cloudflare WAF managed challenge on all content pages; not crawlable",
            "small-arms-survey-db": "STRUCTURAL SKIP — robots permissive but database is aggregate statistics (no per-weapon rows); yield=0",
        },
    }

    # Source 1: ODIN
    odin_stats = crawl_odin(conn)
    summary["sources"]["odin-army-tradoc"] = odin_stats

    # Source 2: Army Recognition
    ar_stats = crawl_army_recognition(conn)
    summary["sources"]["army-recognition"] = ar_stats

    # Post-crawl DB count
    post_count = conn.execute("SELECT COUNT(*) FROM weapon_knowledge_entries").fetchone()[0]
    summary["post_count"] = post_count
    summary["net_inserted"] = post_count - pre_count

    # Source breakdown
    rows = conn.execute(
        "SELECT source_library, COUNT(*) FROM weapon_knowledge_entries GROUP BY source_library ORDER BY 2 DESC"
    ).fetchall()
    summary["db_breakdown"] = {r[0]: r[1] for r in rows}

    conn.close()

    # Write summary JSON
    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    log.info(f"Track N complete. Net inserted: {summary['net_inserted']}")
    log.info(f"Summary: {SUMMARY_PATH}")
    log.info(f"Post-crawl total: {post_count}")
    log.info("=== DONE ===")


if __name__ == "__main__":
    main()
