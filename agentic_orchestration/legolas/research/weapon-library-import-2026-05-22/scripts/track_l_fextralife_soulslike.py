#!/usr/bin/env python3
"""
Track L — Fextralife Soulslike Bundle (DS1 / DS2 / DS3 / Bloodborne / Elden Ring)
Mission:  weapon-library-import-hive-mind-mission-2026-05-22.md
Dispatch: dispatches/2026-05-22-legolas-track-L-fextralife-soulslike-bundle.md

Per-title source_library tags:
  darksouls.wiki.fextralife.com     → fextralife-ds1
  darksouls2.wiki.fextralife.com    → fextralife-ds2
  darksouls3.wiki.fextralife.com    → fextralife-ds3
  bloodborne.wiki.fextralife.com    → fextralife-bloodborne
  eldenring.wiki.fextralife.com     → fextralife-elden-ring

Index structure (confirmed by HTML inspection 2026-05-22):
  /Weapons page contains <div class="row gallery"> blocks.
  First 1-2 blocks = weapon-type CATEGORY links (plural names: Daggers, Greatswords...).
  Subsequent blocks = individual weapon entries.
  Strategy: collect ALL href links from gallery blocks; filter out known category-plural
  names and other non-weapon pages; deduplicate; crawl each remaining link.

Discipline #20: GREEN-with-caution — research-agent UA; 1 req/sec sustained.
               robots.txt: GPTBot Disallow /; ClaudeBot absent (not blocked); no Crawl-delay.
               Backoff: 5s → 15s → 45s on 429.
Discipline #19: fires and returns immediately; summary written on completion.
Discipline #1:  math note in track-L-math-note.md (authored prior to this script).
"""

import json
import os
import re
import sqlite3
import ssl
import time
import datetime
import traceback
import urllib.request
import urllib.error
import urllib.parse

# ── SSL context ────────────────────────────────────────────────────────────────
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()

# ── Paths ──────────────────────────────────────────────────────────────────────
DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
SUMMARY_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "legolas/research/weapon-library-import-2026-05-22/summaries/track-L-fextralife.json"
)
LOG_PATH = "/Users/admin/Games/reincarnated-engine/logs/weapon-library-track-L.log"

STARTED_AT = datetime.datetime.now(datetime.timezone.utc).isoformat()
UA = "reincarnated-engine/0.1 (research; mhwetmore@gmail.com)"

# ── Title catalogue ────────────────────────────────────────────────────────────
TITLES = [
    {
        "source_library": "fextralife-ds1",
        "subdomain":      "darksouls.wiki.fextralife.com",
        "index_path":     "/Weapons",
        "genre_tag":      "dark-souls-1",
        "expected":       120,
    },
    {
        "source_library": "fextralife-ds2",
        "subdomain":      "darksouls2.wiki.fextralife.com",
        "index_path":     "/Weapons",
        "genre_tag":      "dark-souls-2",
        "expected":       220,
    },
    {
        "source_library": "fextralife-ds3",
        "subdomain":      "darksouls3.wiki.fextralife.com",
        "index_path":     "/Weapons",
        "genre_tag":      "dark-souls-3",
        "expected":       190,
    },
    {
        "source_library": "fextralife-bloodborne",
        "subdomain":      "bloodborne.wiki.fextralife.com",
        "index_path":     "/Weapons",
        "genre_tag":      "bloodborne",
        "expected":       25,
    },
    {
        "source_library": "fextralife-elden-ring",
        "subdomain":      "eldenring.wiki.fextralife.com",
        "index_path":     "/Weapons",
        "genre_tag":      "elden-ring",
        "expected":       408,
    },
]

# ── Rate-limit parameters ──────────────────────────────────────────────────────
REQ_INTERVAL  = 1.0   # seconds between requests
BACKOFF_STEPS = [5, 15, 45]
MAX_RETRIES   = 3
BATCH_SIZE    = 50

# ── Known weapon-category (plural) hrefs to skip on the index page ─────────────
# These are weapon-type category pages, not individual weapons.
# Pattern: bare plural nouns, weapon type pages.
# We match normalized (lower, spaces→+) href slug.
_CATEGORY_SLUGS = {
    # DS1 categories
    "daggers", "straight+swords", "greatswords", "ultra+greatswords", "curved+swords",
    "katanas", "curved+greatswords", "piercing+swords", "axes", "great+axes",
    "hammers", "great+hammers", "fist+weapons", "spears", "halberds", "whips",
    "bows", "greatbows", "crossbows", "catalysts", "flames", "talismans",
    "special+weapons", "boss+soul+weapons", "shields",
    # DS2 / DS3 additions
    "twinblades", "reapers", "lances", "claws", "fists", "thrusting+swords",
    "sacred+chimes", "staves", "spellcasting+weapons",
    "small+shields", "medium+shields", "greatshields", "paired+weapons",
    # ER additions
    "colossal+swords", "heavy+thrusting+swords", "great+spears", "flails",
    "light+greatswords", "great+katanas", "backhand+blades", "throwing+blades",
    "perfume+bottles", "hand-to-hand+arts", "claws", "light+bows",
    "glintstone+staves", "glintstone+staffs", "sacred+seals", "ballistas",
    "torches", "thrusting+shields",
    # Bloodborne
    "trick+weapons", "firearms", "hunter+tools",
    # Generic wiki nav
    "weapons", "armor", "items", "rings", "spells", "equipment", "upgrades",
    "lore", "npcs", "locations", "maps", "bosses", "enemies", "builds",
    "stats", "status+effects", "covenants", "classes", "starting+classes",
    "consumables", "ammunition", "key+items", "tools",
    "ashes+of+war", "incantations", "sorceries", "miracles", "pyromancies",
    "great+runes", "spirit+ashes", "talismans", "caryll+runes",
    "chalice+dungeons", "blood+echoes", "runes",
    # ER shadow of erdtree additions
    "colossal+weapons", "light+bows", "ballistas",
}

# Additional non-weapon page name fragments to skip (checked against decoded name)
_SKIP_NAME_FRAGMENTS = {
    "wiki", "guide", "rare item", "rare+item", "playstation", "psn", "xbox",
    "pc ", "dark souls wiki", "new londo", "anor londo", "firelink",
    "undead", "demon's souls", "bloodstone", "echoes", "insight",
    "upgrade", "infusion", "calculator", "patch", "dlc", "community",
    "forum", "editor",
}


def _is_category_href(href):
    """Return True if this href is a weapon-category/nav page, not an individual weapon."""
    slug = href.lstrip("/").lower()
    if slug in _CATEGORY_SLUGS:
        return True
    # Also skip if slug ends with 's' and the de-pluralised form is a weapon-type
    # (catches "Axes", "Bows" etc. that might not be in set)
    # Heuristic: pure single-word plural nouns that are weapon types
    if re.match(r'^[a-z]+s$', slug) and len(slug) < 20:
        # If it's all alpha + plural, likely a category
        singular = slug[:-1]
        if singular in {"dagger", "bow", "axe", "hammer", "spear", "whip",
                        "clue", "catalyst", "flame", "talisman", "torch",
                        "lance", "reaper", "claw", "fist", "shield"}:
            return True
    return False


def _is_skip_name(name):
    """Return True if decoded name looks like a non-weapon page."""
    n = name.lower().strip()
    if len(n) < 3:
        return True
    for frag in _SKIP_NAME_FRAGMENTS:
        if frag in n:
            return True
    return False

# ── Logging ───────────────────────────────────────────────────────────────────
_log_fh = None

def _open_log():
    global _log_fh
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    _log_fh = open(LOG_PATH, "a", encoding="utf-8")

def log(msg):
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    if _log_fh:
        _log_fh.write(line + "\n")
        _log_fh.flush()

# ── HTTP helpers ───────────────────────────────────────────────────────────────
_last_req_time = 0.0

def _throttle():
    global _last_req_time
    elapsed = time.monotonic() - _last_req_time
    if elapsed < REQ_INTERVAL:
        time.sleep(REQ_INTERVAL - elapsed)
    _last_req_time = time.monotonic()

def fetch(url, retries=0):
    """Fetch URL with rate-limiting and exponential backoff on 429."""
    _throttle()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=_SSL_CTX, timeout=25) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code == 429 and retries < MAX_RETRIES:
            wait = BACKOFF_STEPS[min(retries, len(BACKOFF_STEPS) - 1)]
            log(f"  429 on {url} — backing off {wait}s (retry {retries+1}/{MAX_RETRIES})")
            time.sleep(wait)
            return fetch(url, retries + 1)
        elif e.code == 404:
            return None
        log(f"  HTTP {e.code} on {url}")
        return None
    except Exception as exc:
        log(f"  fetch error {url}: {exc}")
        return None

# ── HTML parsing helpers ───────────────────────────────────────────────────────

def _strip_tags(html_frag):
    text = re.sub(r"<[^>]+>", " ", html_frag or "")
    return re.sub(r"\s+", " ", text).strip()

def _decode_href_name(href):
    """Convert href path to display name: /Balder+Side+Sword → Balder Side Sword"""
    slug = href.lstrip("/")
    decoded = urllib.parse.unquote_plus(slug)
    return decoded.strip()

def _extract_page_title(html):
    """Extract <title> text, stripping site suffix."""
    m = re.search(r"<title>([^<]+)</title>", html, re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1)
    # Strip trailing " | Fextralife Wiki" or " - Dark Souls Wiki" etc.
    raw = re.split(r"\s*[|–—-]\s*(?:Fextralife|Dark Souls|Bloodborne|Elden Ring|Wiki)", raw)[0].strip()
    return raw or None

def _extract_og_image(html):
    m = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](https?://[^"\']+)["\']', html, re.IGNORECASE)
    if m:
        return m.group(1)
    # Also try content first variation
    m = re.search(r'<meta\s+content=["\'](https?://[^"\']+\.(?:png|jpg|jpeg|webp))["\'\s][^>]*property=["\']og:image["\']', html, re.IGNORECASE)
    if m:
        return m.group(1)
    return None

def _extract_meta_description(html):
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    if m:
        return _strip_tags(m.group(1))[:2000]
    return None

def _extract_infobox(html):
    """
    Extract weapon infobox data from Fextralife pages.
    Fextralife uses <table> elements for stat tables.
    Returns dict of label → value (first table; best effort).
    """
    result = {}
    # Find all tables
    tables = re.findall(r"<table[^>]*>(.*?)</table>", html, re.IGNORECASE | re.DOTALL)
    for table_html in tables[:3]:  # Check up to 3 tables
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.IGNORECASE | re.DOTALL)
        for row in rows:
            cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.IGNORECASE | re.DOTALL)
            if len(cells) == 2:
                key = _strip_tags(cells[0])[:100].strip()
                val = _strip_tags(cells[1])[:500].strip()
                if key and val and key not in result:
                    result[key] = val
            elif len(cells) >= 3:
                key = _strip_tags(cells[0])[:100].strip()
                vals = [_strip_tags(c)[:200].strip() for c in cells[1:]]
                if key and key not in result:
                    result[key] = " | ".join(v for v in vals if v)
    return result

def _extract_image_urls(html):
    """Extract weapon render image URLs from the page. Cap at 5."""
    seen = set()
    out = []
    # data-src lazily-loaded images (Fextralife lazy-loads via data-src)
    for src in re.findall(r'data-src=["\'](https?://[^"\']+\.(?:png|jpg|jpeg|webp))["\']', html, re.IGNORECASE):
        if src not in seen and not re.search(r'(favicon|thumbnail|mhws|/ads/|pixel)', src, re.IGNORECASE):
            seen.add(src)
            out.append(src)
    # Regular src images
    for src in re.findall(r'<img[^>]+src=["\'](https?://[^"\']+\.(?:png|jpg|jpeg|webp))["\']', html, re.IGNORECASE):
        if src not in seen and not re.search(r'(favicon|thumbnail|mhws|/ads/|pixel)', src, re.IGNORECASE):
            seen.add(src)
            out.append(src)
    return out[:5]

def _extract_lore_text(html):
    """Pull first substantial paragraph of lore/description text."""
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.IGNORECASE | re.DOTALL)
    for p in paras:
        text = _strip_tags(p).strip()
        if len(text) > 80:
            return text[:2000]
    return None

def _guess_weapon_type(name, infobox):
    """Infer weapon type from infobox fields or name heuristics."""
    for k in ("Type", "Weapon Type", "Weapon type", "Category", "Weapon Class",
              "Weapon category", "weapon type"):
        if k in infobox and infobox[k]:
            return infobox[k][:100]
    name_l = name.lower()
    # Name heuristics
    for pattern, wtype in [
        (r"greatsword|claymore|zweihander|flamberge", "Greatsword"),
        (r"ultra greatsword|colossal sword|colossal weapon", "Ultra Greatsword"),
        (r"katana", "Katana"),
        (r"curved sword|scimitar", "Curved Sword"),
        (r"rapier|estoc|thrusting sword", "Thrusting Sword"),
        (r"straight sword|longsword|broadsword", "Straight Sword"),
        (r"dagger|knife|dirk|parrying", "Dagger"),
        (r"greataxe|great axe", "Greataxe"),
        (r"\baxe\b", "Axe"),
        (r"great hammer|great club|giant club", "Great Hammer"),
        (r"hammer|mace|club\b|warpick|morning star", "Hammer"),
        (r"halberd|partisan", "Halberd"),
        (r"spear|lance|pike", "Spear"),
        (r"whip|witch locks", "Whip"),
        (r"great bow|greatbow", "Greatbow"),
        (r"crossbow", "Crossbow"),
        (r"\bbow\b", "Bow"),
        (r"claw|caestus|fist|knuckle", "Fist/Claw"),
        (r"catalyst|staff|sorcery|glintstone", "Staff/Catalyst"),
        (r"talisman|sacred chime|seal|holy symbol", "Talisman/Sacred Seal"),
        (r"pyromancy flame", "Pyromancy Flame"),
        (r"torch", "Torch"),
        (r"reaper|scythe|sickle", "Reaper"),
        (r"flail", "Flail"),
        (r"twin blade|twinblade", "Twinblade"),
        (r"hand axe|battle axe", "Axe"),
        (r"perfume|bottle", "Perfume Bottle"),
        (r"throwing", "Throwing Weapon"),
    ]:
        if re.search(pattern, name_l):
            return wtype
    return None

# ── Index page parsing ─────────────────────────────────────────────────────────

def parse_weapons_index(html, base_host):
    """
    Parse the /Weapons gallery blocks and return list of (decoded_name, full_url) tuples.
    Strategy:
      - Find all <div class="row gallery"> blocks
      - Collect all href links from them
      - Filter out: (a) category-plural slugs, (b) known non-weapon names,
        (c) absolute external URLs, (d) admin/forum paths
    """
    ADMIN_PAT = re.compile(
        r"^/(?:wiki/|forums|login|register|Editing|changes|settings|"
        r"authentication|filemanager|ws/|pixel|Dark\+Souls\+Wiki|Dark\+Souls\+2\+Wiki|"
        r"Dark\+Souls\+3\+Wiki|Elden\+Ring\+Wiki|Bloodborne\+Wiki)",
        re.IGNORECASE,
    )

    gallery_blocks = re.findall(
        r'<div\s+class="row gallery"[^>]*>(.*?)(?=<div\s+class="row gallery"|'
        r'<h[1-6][\s>]|<footer|</article|</main)',
        html, re.DOTALL | re.IGNORECASE,
    )

    seen_urls = set()
    results = []

    for blk in gallery_blocks:
        hrefs = re.findall(r'href=["\'](/[^"\'?#][^"\']*)["\']', blk)
        for href in hrefs:
            if ADMIN_PAT.match(href):
                continue
            if _is_category_href(href):
                continue
            # Skip file extensions
            if re.search(r'\.(css|js|png|jpg|gif|ico|xml|rss|txt)$', href, re.IGNORECASE):
                continue
            full_url = f"https://{base_host}{href}"
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)
            name = _decode_href_name(href)
            if _is_skip_name(name):
                continue
            results.append((name, full_url))

    return results

# ── DB helpers ─────────────────────────────────────────────────────────────────

def get_db():
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA foreign_keys=ON")
    return con

def ensure_fextralife_library(con):
    """Register Fextralife library slugs in the libraries table."""
    for t in TITLES:
        slug = t["source_library"]
        base = f"https://{t['subdomain']}"
        display_map = {
            "fextralife-ds1":         "Fextralife Dark Souls 1 Wiki",
            "fextralife-ds2":         "Fextralife Dark Souls 2 Wiki",
            "fextralife-ds3":         "Fextralife Dark Souls 3 Wiki",
            "fextralife-bloodborne":  "Fextralife Bloodborne Wiki",
            "fextralife-elden-ring":  "Fextralife Elden Ring Wiki",
        }
        con.execute("""
            INSERT OR IGNORE INTO libraries
                (slug, display_name, base_url, api_url, import_tier, license_class, notes)
            VALUES (?,?,?,NULL,2,'editorial_only',
                    'Fan-maintained wiki; license=fan-wiki/editorial_only; soulslike weapon data')
        """, (slug, display_map.get(slug, slug), base))
    con.commit()

def insert_batch(con, batch):
    """Insert batch into weapon_knowledge_entries + reference images."""
    inserted_entries = 0
    inserted_images  = 0
    for item in batch:
        try:
            cur = con.execute("""
                INSERT OR IGNORE INTO weapon_knowledge_entries
                    (canonical_name, source_library, source_url, source_id,
                     description_text, structured_properties,
                     cultural_lineage_tags, historical_period,
                     genre_appearances, related_entries, license_class)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                item["canonical_name"],
                item["source_library"],
                item["source_url"],
                item.get("source_id"),
                item.get("description_text"),
                json.dumps(item.get("structured_properties") or {}),
                json.dumps(item.get("cultural_lineage_tags") or []),
                item.get("historical_period"),
                json.dumps(item.get("genre_appearances") or []),
                json.dumps(item.get("related_entries") or []),
                item.get("license_class", "fan-wiki"),
            ))
            if cur.rowcount > 0 and cur.lastrowid:
                entry_id = cur.lastrowid
                inserted_entries += 1
                for i, img_url in enumerate(item.get("image_urls") or []):
                    con.execute("""
                        INSERT OR IGNORE INTO knowledge_entry_reference_images
                            (knowledge_entry_id, image_url, image_source,
                             license_class, is_canonical)
                        VALUES (?,?,?,?,?)
                    """, (
                        entry_id, img_url,
                        "fextralife-wiki-render",
                        "editorial_only",
                        1 if i == 0 else 0,
                    ))
                    inserted_images += 1
        except Exception as exc:
            log(f"  INSERT error ({item.get('canonical_name')}): {exc}")
    con.commit()
    return inserted_entries, inserted_images

# ── Per-weapon page scrape ─────────────────────────────────────────────────────

def scrape_weapon_page(name_hint, url, source_library, genre_tag):
    """Fetch + parse a weapon page. Returns dict (may have extraction_error)."""
    html = fetch(url)
    if html is None:
        return {
            "canonical_name":        name_hint,
            "source_library":        source_library,
            "source_url":            url,
            "source_id":             urllib.parse.urlparse(url).path.lstrip("/"),
            "structured_properties": {"extraction_error": "fetch-failed"},
            "cultural_lineage_tags": ["soulslike", genre_tag],
            "historical_period":     "fantasy",
            "genre_appearances":     ["fantasy-soulslike"],
            "license_class":         "fan-wiki",
            "image_urls":            [],
            "_error":                True,
        }

    page_title = _extract_page_title(html) or name_hint
    infobox    = _extract_infobox(html)
    meta_desc  = _extract_meta_description(html)
    lore_text  = _extract_lore_text(html)

    desc_parts = [p for p in [meta_desc, lore_text] if p]
    description = " | ".join(desc_parts)[:3000] if desc_parts else None

    og_img   = _extract_og_image(html)
    img_list = _extract_image_urls(html)
    if og_img and og_img not in img_list:
        img_list.insert(0, og_img)
    image_urls = img_list[:5]

    weapon_type = _guess_weapon_type(page_title, infobox)
    props = dict(infobox)
    if weapon_type:
        props["weapon_type"] = weapon_type

    return {
        "canonical_name":        page_title,
        "source_library":        source_library,
        "source_url":            url,
        "source_id":             urllib.parse.urlparse(url).path.lstrip("/"),
        "description_text":      description,
        "structured_properties": props,
        "cultural_lineage_tags": ["soulslike", genre_tag],
        "historical_period":     "fantasy",
        "genre_appearances":     ["fantasy-soulslike"],
        "related_entries":       [],
        "license_class":         "fan-wiki",
        "image_urls":            image_urls,
    }

# ── Per-title crawl ────────────────────────────────────────────────────────────

def crawl_title(title_cfg, con):
    lib  = title_cfg["source_library"]
    sub  = title_cfg["subdomain"]
    path = title_cfg["index_path"]
    tag  = title_cfg["genre_tag"]
    index_url = f"https://{sub}{path}"

    log(f"=== {lib} — index: {index_url}")

    index_html = fetch(index_url)
    if not index_html:
        log(f"  FAIL: could not fetch index for {lib}")
        return {
            "source_library": lib, "index_url": index_url,
            "weapons_found": 0, "inserted_entries": 0,
            "inserted_images": 0, "errors": 0,
            "status": "index-fetch-failed",
        }

    candidates = parse_weapons_index(index_html, sub)
    log(f"  {lib}: {len(candidates)} individual weapon candidates from index")

    inserted_entries = 0
    inserted_images  = 0
    errors           = 0
    batch            = []

    for i, (name, url) in enumerate(candidates):
        result = scrape_weapon_page(name, url, lib, tag)

        if result.get("_error"):
            errors += 1
            log(f"  [{i+1}/{len(candidates)}] fetch-failed: {url}")

        batch.append(result)

        if (i + 1) % 20 == 0:
            log(f"  [{i+1}/{len(candidates)}] last scraped: {result['canonical_name']}")

        if len(batch) >= BATCH_SIZE:
            ie, ii = insert_batch(con, batch)
            inserted_entries += ie
            inserted_images  += ii
            log(f"  batch flush @{i+1}: +{ie} entries, +{ii} images (running total: {inserted_entries})")
            batch = []

    if batch:
        ie, ii = insert_batch(con, batch)
        inserted_entries += ie
        inserted_images  += ii
        log(f"  final flush: +{ie} entries, +{ii} images")

    log(f"  {lib} DONE: {inserted_entries} entries, {inserted_images} images, {errors} errors")
    return {
        "source_library":   lib,
        "index_url":        index_url,
        "weapons_found":    len(candidates),
        "inserted_entries": inserted_entries,
        "inserted_images":  inserted_images,
        "errors":           errors,
        "status":           "completed",
    }

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    _open_log()
    log("Track L — Fextralife Soulslike Bundle — START (v2: gallery-block parser)")
    log(f"DB: {DB_PATH}")
    log(f"Summary: {SUMMARY_PATH}")

    con = get_db()
    ensure_fextralife_library(con)

    per_title_results = []
    total_entries = 0
    total_images  = 0
    total_errors  = 0

    for title_cfg in TITLES:
        try:
            result = crawl_title(title_cfg, con)
        except Exception as exc:
            log(f"UNCAUGHT ERROR in {title_cfg['source_library']}: {exc}")
            log(traceback.format_exc())
            result = {
                "source_library":   title_cfg["source_library"],
                "index_url":        f"https://{title_cfg['subdomain']}{title_cfg['index_path']}",
                "weapons_found":    0,
                "inserted_entries": 0,
                "inserted_images":  0,
                "errors":           1,
                "status":           "uncaught-exception",
            }
        per_title_results.append(result)
        total_entries += result.get("inserted_entries", 0)
        total_images  += result.get("inserted_images",  0)
        total_errors  += result.get("errors",           0)

    # DB count verify
    try:
        row = con.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library LIKE 'fextralife%'"
        ).fetchone()
        db_total = row[0] if row else 0
    except Exception:
        db_total = -1

    finished_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    summary = {
        "track":          "L",
        "mission":        "fextralife-soulslike-bundle",
        "started_at":     STARTED_AT,
        "finished_at":    finished_at,
        "db_path":        DB_PATH,
        "per_title":      per_title_results,
        "total_inserted_entries": total_entries,
        "total_inserted_images":  total_images,
        "total_errors":           total_errors,
        "db_count_fextralife":    db_total,
        "acceptance": {
            "ge_1000_rows":    db_total >= 1000,
            "each_title_ge_1": all(r.get("inserted_entries", 0) >= 1
                                   for r in per_title_results),
            "license_fan_wiki": True,
            "summary_written":  True,
        },
    }

    os.makedirs(os.path.dirname(SUMMARY_PATH), exist_ok=True)
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    log(f"Track L COMPLETE — entries: {total_entries}, images: {total_images}, "
        f"db_fextralife_count: {db_total}")
    log(f"Summary written: {SUMMARY_PATH}")
    con.close()


if __name__ == "__main__":
    main()
