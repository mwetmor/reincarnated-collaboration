#!/usr/bin/env python3
"""
Phase D Step 6.5: Canonical taxonomy normalization (CRITICAL Amendment #1).

Per gandalf §5 + math note §2.7:

Populates cultural_lineage_canonical, historical_period_canonical, register_canonical,
cultural_lineage_confidence on all rows. Step 7 BLOCKS on (weapon_subclass,
cultural_lineage_canonical) — without populated canonical taxonomy, blocking
collapses to single 89K bucket and merge becomes computationally infeasible.

Confidence ladder (gandalf §5.3):
  1.0 — explicit structured-tag match
  0.7 — description-regex match
  0.5 — source-library default
  0.3 — fallback heuristic

Idempotency: only overwrites if new confidence >= existing confidence.
Authority: Matt 2026-05-23 whole-pipeline upfront authorization.
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "08_step6_5_canonical_taxonomy.json"

# ---------------------------------------------------------------------------
# Register mapping per source_library (deterministic)
# ---------------------------------------------------------------------------

REGISTER_BY_SOURCE = {
    "royal_armouries": "historical",
    "met-museum": "historical",
    "wikidata": "historical",
    "wikipedia": "historical",
    "nick-aschenbach-dnd-data": "fantasy",
    "5e-bits-5e-database": "fantasy",
    "5e-bits-5e-database-2024": "fantasy",
    "bsdata-warhammer-aos": "fantasy",
    "fextralife-elden-ring": "fantasy",
    "fextralife-ds1": "fantasy",
    "fextralife-ds2": "fantasy",
    "fextralife-ds3": "fantasy",
    "bloqhead-demigods": "fantasy",
    "elden-ring-erdb": "fantasy",
    "diablo2-d2data": "fantasy",
    "path-of-exile-repoe": "fantasy",
    "osrsbox-db": "fantasy",
    "wow-classic-items": "fantasy",
    "souls-api-thomaslincoln": "fantasy",
    "odin-army-tradoc": "military_modern",
    "army-recognition": "military_modern",
    "cataclysm-dda": "military_modern",
    "gta-v-data": "military_modern",
    # Quarantined slugs (excluded from v_category_sample anyway)
    "pf2ools-pf2ools-data-quarantined": "fantasy",
    "souls-api-thomaslincoln-quarantined": "fantasy",
}

# ---------------------------------------------------------------------------
# Cultural lineage extraction (regex patterns; same order-sensitive as Step 2)
# ---------------------------------------------------------------------------

CULTURE_REGEX_PATTERNS = [
    (re.compile(r"\b(japan|edo|tokyo|kyoto|nara|heian|kamakura|samurai)", re.I), "east_asian"),
    (re.compile(r"\b(china|chinese|qing|ming|tang)", re.I), "east_asian"),
    (re.compile(r"\b(korea|korean|joseon)", re.I), "east_asian"),
    (re.compile(r"\b(india|indian|mughal|sikh|rajput|punjab|sri lanka|tamil)", re.I), "south_asian"),
    (re.compile(r"\b(indonesia|java|sumatra|bali|philippines|vietnam|thailand|burma|malaya|filipino)", re.I), "southeast_asian"),
    (re.compile(r"\b(iran|persia|persian|safavid|qajar|ottoman|turkey|anatolia|arab|syria|iraq|yemen|saudi|mamluk)", re.I), "middle_eastern"),
    (re.compile(r"\b(africa|moroc|algeria|nubia|ethiopia|zulu|maasai|tunisia|tswana|coptic)", re.I), "african"),
    (re.compile(r"\b(mexic|aztec|maya|toltec|tlatoani)", re.I), "mesoamerican"),
    (re.compile(r"\b(inca|peru|andean|amazon|brazil|colombia)", re.I), "south_american_indigenous"),
    (re.compile(r"\b(native\s+american|first\s+nations|sioux|apache|cherokee|iroquois)", re.I), "north_american_indigenous"),
    (re.compile(r"\b(sami|inuit|greenland|arctic)", re.I), "arctic_circumpolar"),
    (re.compile(r"\b(maori|polynesian|hawaiian|fijian|samoan|tongan|melanesian)", re.I), "oceanic"),
    (re.compile(
        r"\b(britain|british|england|english|scottish|welsh|irish|german|french|italian|spanish|"
        r"polish|russian|dutch|belgian|swiss|austrian|danish|swedish|norwegian|portuguese|"
        r"hungarian|czech|birmingham|london|europe|european|usa|canada|america|austria-hungary)",
        re.I,
    ), "european"),
]

# Country-code → lineage mapping (for ODIN structured_properties.origin_countries)
COUNTRY_CODE_TO_LINEAGE = {
    "USA": "european", "RUS": "european", "USSR": "european",
    "FRA": "european", "GER": "european", "UK": "european", "GBR": "european",
    "POL": "european", "ITA": "european", "ESP": "european", "BEL": "european",
    "NLD": "european", "CHE": "european", "AUT": "european", "SWE": "european",
    "NOR": "european", "DNK": "european", "FIN": "european", "PRT": "european",
    "GRC": "european", "TUR": "middle_eastern", "ISR": "middle_eastern",
    "IRN": "middle_eastern", "IRQ": "middle_eastern", "SAU": "middle_eastern",
    "EGY": "african", "ZAF": "african", "NGA": "african",
    "CHN": "east_asian", "JPN": "east_asian", "KOR": "east_asian", "PRK": "east_asian",
    "TWN": "east_asian", "VNM": "southeast_asian", "THA": "southeast_asian",
    "IDN": "southeast_asian", "PHL": "southeast_asian", "MYS": "southeast_asian",
    "IND": "south_asian", "PAK": "south_asian", "BGD": "south_asian", "LKA": "south_asian",
    "MEX": "mesoamerican", "BRA": "south_american_indigenous", "ARG": "south_american_indigenous",
    "AUS": "oceanic", "NZL": "oceanic",
    "CAN": "european",
}


def extract_culture_from_text(*texts: str | None) -> tuple[str, float]:
    """Run regex bank over text; return (lineage, confidence) — confidence=0.7 if hit, else (unknown, 0.0)."""
    combined = " ".join(t for t in texts if t)
    if not combined.strip():
        return ("unknown", 0.0)
    for pat, bucket in CULTURE_REGEX_PATTERNS:
        if pat.search(combined):
            return (bucket, 0.7)
    return ("unknown", 0.0)


def extract_culture_for_row(row: dict) -> tuple[str, float]:
    """Per-source mapping with confidence ladder."""
    src = row["source_library"] or ""
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json)
    except Exception:
        sp = {}
    desc = row["description_text"] or ""
    cultural_tags = row["cultural_lineage_tags"] or ""

    # CONFIDENCE 1.0 — explicit structured-tag match
    if src == "met-museum":
        culture_field = sp.get("culture") or ""
        if culture_field:
            lineage, _ = extract_culture_from_text(culture_field)
            if lineage != "unknown":
                return (lineage, 1.0)

    if src == "odin-army-tradoc":
        origin_countries = sp.get("origin_countries") or []
        if isinstance(origin_countries, list) and origin_countries:
            for code in origin_countries:
                if code in COUNTRY_CODE_TO_LINEAGE:
                    return (COUNTRY_CODE_TO_LINEAGE[code], 1.0)

    if src == "wikidata":
        country = sp.get("country_of_origin") or sp.get("country") or ""
        if country:
            lineage, _ = extract_culture_from_text(country)
            if lineage != "unknown":
                return (lineage, 1.0)

    # CONFIDENCE 0.7 — description regex hit
    lineage, conf = extract_culture_from_text(desc, cultural_tags, sp.get("place") or "")
    if conf > 0.0:
        return (lineage, 0.7)

    # CONFIDENCE 0.5 — source-library default
    if src in {
        "nick-aschenbach-dnd-data", "5e-bits-5e-database", "5e-bits-5e-database-2024",
        "bsdata-warhammer-aos", "fextralife-elden-ring", "fextralife-ds1", "fextralife-ds2", "fextralife-ds3",
        "bloqhead-demigods", "elden-ring-erdb", "diablo2-d2data", "path-of-exile-repoe",
        "osrsbox-db", "wow-classic-items", "souls-api-thomaslincoln",
        "pf2ools-pf2ools-data-quarantined", "souls-api-thomaslincoln-quarantined",
    }:
        return ("fantasy_generic", 0.5)
    if src in {"cataclysm-dda", "gta-v-data"}:
        return ("cross_cultural", 0.5)
    if src == "army-recognition":
        return ("cross_cultural", 0.5)
    if src == "royal_armouries":
        return ("european", 0.5)  # Royal Armouries default is European-centric
    if src == "met-museum":
        return ("unknown", 0.3)  # Met has explicit culture; if absent, fallback

    # CONFIDENCE 0.3 — fallback
    return ("unknown", 0.3)


# ---------------------------------------------------------------------------
# Historical period extraction
# ---------------------------------------------------------------------------

CENTURY_WORD_RE = re.compile(r"(\d{1,2})(st|nd|rd|th)\s+century", re.I)
YEAR_RE = re.compile(r"\b(\d{3,4})\b")


def year_to_period(year: int) -> str:
    if year < -500:
        return "pre_classical"
    if year < 500:
        return "classical"
    if year < 1500:
        return "medieval"
    if year < 1800:
        return "early_modern"
    if year < 1914:
        return "industrial"
    if year < 1989:
        return "modern"
    return "contemporary"


def century_to_period(century: int) -> str:
    """century=1 → 1st century (1-100 CE → classical); century=19 → 1801-1900 (industrial); etc."""
    representative_year = (century - 1) * 100 + 50
    return year_to_period(representative_year)


def extract_period_for_row(row: dict) -> tuple[str, float]:
    src = row["source_library"] or ""
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json)
    except Exception:
        sp = {}
    desc = row["description_text"] or ""
    hist_period_raw = row["historical_period"] or ""

    # CONFIDENCE 1.0 — explicit structured year fields
    if src == "met-museum":
        obj_begin = sp.get("objectBeginDate")
        if isinstance(obj_begin, (int, float)) and obj_begin != 0:
            return (year_to_period(int(obj_begin)), 1.0)

    if src == "odin-army-tradoc":
        introd = sp.get("date_of_introduction")
        if isinstance(introd, (int, float)) and introd != 0:
            return (year_to_period(int(introd)), 1.0)
        # ODIN modern military default
        return ("contemporary", 0.8)

    if src == "army-recognition":
        return ("contemporary", 0.8)

    # CONFIDENCE 0.7 — date string regex on (RA date / wikidata period / wikipedia)
    for candidate in (sp.get("date"), sp.get("inception"), hist_period_raw, desc[:500]):
        if not candidate:
            continue
        s = str(candidate)
        m = CENTURY_WORD_RE.search(s)
        if m:
            return (century_to_period(int(m.group(1))), 0.7)
        m = YEAR_RE.search(s)
        if m:
            year = int(m.group(1))
            if 1 <= year <= 2100:
                return (year_to_period(year), 0.7)

    # CONFIDENCE 0.5 — source-library default
    if src in {
        "nick-aschenbach-dnd-data", "5e-bits-5e-database", "5e-bits-5e-database-2024",
        "bsdata-warhammer-aos", "fextralife-elden-ring", "fextralife-ds1", "fextralife-ds2", "fextralife-ds3",
        "bloqhead-demigods", "elden-ring-erdb", "diablo2-d2data", "path-of-exile-repoe",
        "osrsbox-db", "wow-classic-items", "souls-api-thomaslincoln",
        "pf2ools-pf2ools-data-quarantined", "souls-api-thomaslincoln-quarantined",
    }:
        return ("fictional", 0.5)
    if src in {"cataclysm-dda", "gta-v-data"}:
        return ("contemporary", 0.5)
    if src == "royal_armouries":
        return ("early_modern", 0.4)  # RA holdings skew early-modern but variable

    return ("unknown", 0.3)


# ---------------------------------------------------------------------------
# Wieldable_humanoid extraction (gap-fill within Step 6.5 — v_category_sample
# requires this populated; default to two_hand for general weapon-kind rows).
# Per gandalf §2.6 per-source signal inventory.
# ---------------------------------------------------------------------------

# Royal Armouries category_value → wieldable_humanoid mapping
RA_WIELD_BY_CATEGORY = {
    "Swords": "one_hand",          # default; some two-handers exist but most museum swords one-hand
    "Daggers & knives": "one_hand",
    "Bayonets": "one_hand",
    "Staff weapons": "two_hand",   # pikes/spontoons/halberds/partizans/etc.
    "Archery & related objects": "two_hand",
    "Clubs, maces, axes, and truncheons": "one_hand",
    "Shields": "one_hand",         # carried in off-hand
    "Firearms & related objects": "two_hand",  # rifles/muskets default; "Pistol"-name rows below
    "Artillery & related objects": "no",      # most are mounted/crew-served
    "Combination weapons": "one_hand",
    "Instruments of torture & punishment": "unknown",
}

# Met Museum classification → wieldable_humanoid
MET_WIELD_BY_CLASSIFICATION_PREFIX = {
    "Swords": "one_hand",
    "Daggers": "one_hand",
    "Knives": "one_hand",
    "Shafted Weapons": "two_hand",
    "Shields": "one_hand",
    "Krisses": "one_hand",
    "Firearms-Pistols": "one_hand",
    "Firearms-Rifles": "two_hand",
    "Firearms-Long Guns": "two_hand",
    "Firearms-Muskets": "two_hand",
    "Firearms-Carbines": "two_hand",
    "Firearms": "two_hand",       # generic fallback
}


def extract_wieldable_humanoid(row: dict) -> str:
    """Source-driven wieldable_humanoid extraction. Returns one of:
    one_hand / two_hand / shoulder_supported / either / no / mount_required / unknown.
    """
    src = row["source_library"] or ""
    name = (row["canonical_name"] or "").lower()
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json)
    except Exception:
        sp = {}

    # ----- Cataclysm-DDA: direct `handedness` field (gandalf §2.6) -----
    if src == "cataclysm-dda":
        h = sp.get("handedness")
        if h == 1:
            return "one_hand"
        if h == 2:
            return "two_hand"

    # ----- ODIN: crew count -----
    if src == "odin-army-tradoc":
        crew = sp.get("crew")
        try:
            crew_n = int(crew) if crew else None
        except Exception:
            crew_n = None
        weight = sp.get("weight_kg") or sp.get("system_weight_kg")
        if crew_n is not None:
            if crew_n >= 2:
                # M224 LWCMS edge case: gandalf §2.5 — shoulder_supported in handheld mode
                if "m224" in name or "lwcms" in name:
                    return "shoulder_supported"
                return "no"
            if crew_n == 1:
                # Check weight for shoulder_supported (~5-25kg)
                if weight is not None:
                    try:
                        w = float(weight)
                        if 5.0 <= w <= 25.0:
                            return "shoulder_supported"
                    except Exception:
                        pass
                return "two_hand"
        # ODIN aircraft/UAVs etc — `no` default
        domain = sp.get("domain_hierarchy") or ""
        if isinstance(domain, str) and any(t in domain.lower() for t in ("aircraft", "drone", "uav", "tank", "vehicle")):
            return "no"
        return "two_hand"

    # ----- Royal Armouries -----
    if src == "royal_armouries":
        cv = sp.get("category_value")
        if cv in RA_WIELD_BY_CATEGORY:
            base = RA_WIELD_BY_CATEGORY[cv]
            # Refinement: "Pistol" in name → one_hand even within Firearms category
            if cv == "Firearms & related objects" and "pistol" in name:
                return "one_hand"
            return base
        return "two_hand"  # RA fallback

    # ----- Met Museum -----
    if src == "met-museum":
        clf = sp.get("classification") or ""
        for prefix, w in MET_WIELD_BY_CLASSIFICATION_PREFIX.items():
            if clf.startswith(prefix):
                return w
        # Met fallback
        return "two_hand"

    # ----- Name-pattern fallback (cross-source) -----
    # One-handed indicators
    if any(t in name for t in (
        "dagger", "knife", "tantō", "tanto", "wakizashi", "pistol", "revolver",
        "buckler", "shield", "wand", "orb", "throwing", "sling", "javelin",
        "kris", "katar", "kukri",
    )):
        return "one_hand"
    # Two-handed indicators
    if any(t in name for t in (
        "greatsword", "two-handed", "two handed", "twohanded", "longbow", "crossbow",
        "musket", "rifle", "spear", "pike", "lance", "halberd", "spontoon", "partizan",
        "polearm", "staff", "naginata", "yari", "great katana", "trident", "warhammer",
        "great axe", "greataxe", "battleaxe", "war scythe",
    )):
        return "two_hand"
    # Either-hand indicators (bastard / hand-and-a-half)
    if any(t in name for t in ("bastard", "hand-and-a-half")):
        return "either"
    # Shoulder-supported indicators
    if any(t in name for t in ("rpg-7", "manpads", "stinger", "javelin launcher", "smaw")):
        return "shoulder_supported"
    # No-wield indicators (mounted/siege)
    if any(t in name for t in ("turret", "artillery", "mortar", "cannon", "howitzer", "siege")):
        return "no"

    # Default: two_hand (conservative; matches the largest weapon category bucket)
    return "two_hand"


# ---------------------------------------------------------------------------
# Step execution
# ---------------------------------------------------------------------------


def run_step6_5(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    cur.execute(
        """SELECT id, canonical_name, source_library,
                  description_text, structured_properties, cultural_lineage_tags,
                  historical_period,
                  weapon_kind,
                  cultural_lineage_canonical, cultural_lineage_confidence,
                  historical_period_canonical, register_canonical
           FROM weapon_knowledge_entries
           WHERE dedup_status != 'merged_into'"""
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    # In-memory updates collected, then bulk-applied
    updates: list[tuple] = []  # (lineage, conf, period, register, wieldable, id)
    per_source_culture: dict[str, dict[str, int]] = {}
    per_source_period: dict[str, dict[str, int]] = {}
    per_source_register: dict[str, dict[str, int]] = {}
    per_source_wieldable: dict[str, dict[str, int]] = {}

    for r in rows:
        row = dict(zip(cols, r))
        existing_conf = row["cultural_lineage_confidence"] or 0.0

        new_lineage, new_conf = extract_culture_for_row(row)
        new_period, _period_conf = extract_period_for_row(row)
        new_register = REGISTER_BY_SOURCE.get(row["source_library"], "unknown")
        if row["weapon_kind"] == "unique" and row["register_canonical"]:
            # Preserve Step 6's mythological/historical register classification for uniques
            new_register = row["register_canonical"]

        # Wieldable: skip rows that are weapon_kind in {ammo_or_consumable, unknown}
        # (they're not engine-sampling-eligible regardless)
        wk = row["weapon_kind"]
        if wk in ("ammo_or_consumable", "unknown"):
            new_wieldable = "unknown"
        else:
            new_wieldable = extract_wieldable_humanoid(row)

        # Idempotency on confidence: only overwrite lineage if new conf >= existing
        if new_conf >= existing_conf:
            final_lineage, final_conf = new_lineage, new_conf
        else:
            final_lineage, final_conf = (
                row["cultural_lineage_canonical"] or "unknown",
                existing_conf,
            )

        updates.append((final_lineage, final_conf, new_period, new_register, new_wieldable, row["id"]))

        src = row["source_library"] or "unknown"
        per_source_culture.setdefault(src, {})[final_lineage] = (
            per_source_culture.setdefault(src, {}).get(final_lineage, 0) + 1
        )
        per_source_period.setdefault(src, {})[new_period] = (
            per_source_period.setdefault(src, {}).get(new_period, 0) + 1
        )
        per_source_register.setdefault(src, {})[new_register] = (
            per_source_register.setdefault(src, {}).get(new_register, 0) + 1
        )
        per_source_wieldable.setdefault(src, {})[new_wieldable] = (
            per_source_wieldable.setdefault(src, {}).get(new_wieldable, 0) + 1
        )

    # Bulk UPDATE
    cur.executemany(
        """UPDATE weapon_knowledge_entries
           SET cultural_lineage_canonical = ?,
               cultural_lineage_confidence = ?,
               historical_period_canonical = ?,
               register_canonical = ?,
               wieldable_humanoid = ?
           WHERE id = ?""",
        updates,
    )
    conn.commit()

    return {
        "rows_processed": len(rows),
        "updates_applied": len(updates),
        "per_source_culture_top_5": {
            k: dict(sorted(v.items(), key=lambda x: -x[1])[:5])
            for k, v in per_source_culture.items()
        },
        "per_source_register": per_source_register,
        "per_source_wieldable": per_source_wieldable,
    }


def acceptance_check(conn: sqlite3.Connection) -> dict:
    """Gate (c) check on v_category_sample:
        cultural >= 70% ; period >= 60% ; register >= 95% (all on v_category_sample)
    """
    cur = conn.cursor()
    total_v = cur.execute("SELECT COUNT(*) FROM v_category_sample").fetchone()[0]
    if total_v == 0:
        return {"v_category_sample_count": 0, "skipped": True}

    pct_cultural = cur.execute(
        """SELECT 100.0 * SUM(CASE WHEN cultural_lineage_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*)
           FROM v_category_sample"""
    ).fetchone()[0]
    pct_period = cur.execute(
        """SELECT 100.0 * SUM(CASE WHEN historical_period_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*)
           FROM v_category_sample"""
    ).fetchone()[0]
    pct_register = cur.execute(
        """SELECT 100.0 * SUM(CASE WHEN register_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*)
           FROM v_category_sample"""
    ).fetchone()[0]

    return {
        "v_category_sample_count": total_v,
        "pct_cultural_populated": round(pct_cultural, 2),
        "pct_period_populated": round(pct_period, 2),
        "pct_register_populated": round(pct_register, 2),
        "gate_cultural_pass": pct_cultural >= 70.0,
        "gate_period_pass": pct_period >= 60.0,
        "gate_register_pass": pct_register >= 95.0,
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "08_step6_5_canonical_taxonomy.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        summary["execution"] = run_step6_5(conn)
        summary["acceptance"] = acceptance_check(conn)
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    acc = summary["acceptance"]
    summary["passed"] = (
        acc.get("gate_cultural_pass", False)
        and acc.get("gate_period_pass", False)
        and acc.get("gate_register_pass", False)
    )

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"  ==> Rows processed: {summary['execution']['rows_processed']}")
    print(f"  ==> v_category_sample rows: {acc['v_category_sample_count']}")
    print(f"  ==> cultural_lineage populated: {acc['pct_cultural_populated']}% (gate ≥70)")
    print(f"  ==> historical_period populated: {acc['pct_period_populated']}% (gate ≥60)")
    print(f"  ==> register populated: {acc['pct_register_populated']}% (gate ≥95)")
    print(f"  ==> PASSED: {summary['passed']}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
