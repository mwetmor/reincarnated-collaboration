"""WS2 Phase 1 modern-caster substrate-coverage audit.

Mode A read-only query against weapon_knowledge_entries (~90,220 rows).
Generates per-primary breakdowns for the 19 modern-caster overlay entries.

Run: python3 ws2_phase1_modern_caster_audit.py
"""

from __future__ import annotations

import re
import sqlite3
from collections import defaultdict
from pathlib import Path

DB_PATH = Path.home() / "Games/reincarnated-loadout/data/telemetry.db"

# Per-primary overlay entries + keyword groupings per gandalf deferred § 2.4
# Each entry has the per-overlay-token name + the broader keyword scan.
OVERLAY_QUERIES = {
    "lightning": {
        "tesla": ["tesla"],
        "voltage": ["voltage", "volt-"],
        # NB: bare 'ion' is too noisy ('percussion', 'pavilion', 'champion',
        # 'rebellion', etc.). Restrict to known sci-fi compounds where 'ion' is
        # the radical (ion as ionized-particle).
        "ion": ["ion cannon", "ion rifle", "ion pistol", "ion gun",
                "ion blast", "ion lance", "ion blade", "ion bomb",
                "ion grenade", "ionization", "ionizer", "ion sword"],
        "flash": ["flashbang", "flash grenade", "flashbomb",
                  "flash cannon", "flash pistol", "flash bomb",
                  "flash rifle"],
        # umbrella sci-fi-electrical
        "_railgun_coilgun": ["coilgun", "coil gun", "railgun", "rail gun"],
        "_emp_generator": ["electromagnetic pulse", " emp ", "emp grenade",
                           "emp bomb", "emp pistol"],
        "_plasma_electric": ["plasma"],
    },
    "fire": {
        "fusion": ["fusion"],
        "thermal": ["thermal", "thermite"],
        "combustion": ["combustion"],
        "_flamethrower_modern": ["flamethrower", "incendiary"],
    },
    "holy": {
        "photon": ["photon", "photonic"],
        "laser": ["laser"],
        "prismatic": ["prism", "prismatic"],
        "_radiant_emitter": ["radiant emitter", "light amplifier",
                              "light amplification", "photonic projector"],
    },
    "shadow": {
        "blackhole": ["black hole", "blackhole"],
        "singularity": ["singularity"],
        "darkmatter": ["dark matter", "darkmatter"],
        "_antimatter_void_modern": ["antimatter", "voidmaw"],
    },
    "wind": {
        # sonic-as-weapon (not 'supersonic missile' = firearm by another name)
        "sonic": ["sonic emitter", "sonic cannon", "sonic gun", "sonic blast",
                  "sonic bomb", "sonic rifle", "sonic taser", "sonic amplifier",
                  "sonic spear", "sonic disruptor"],
        "shockwave": ["shockwave", "shock wave"],
        "_acoustic_pressure": ["acoustic", "pressure cannon"],
    },
    "water": {
        # narrow to weapon-vessel naming; exclude civil/research hardware
        "hydro": ["hydro cannon", "hydro pistol", "hydro rifle", "hydro blast",
                  "hydro gun", "hydropump"],
        "hydraulic": ["hydraulic press weapon", "hydraulic hammer"],
        "_cryo_cavitation": ["cryo bomb", "cryo grenade", "cryo gun",
                             "cryo cannon", "cryo rifle", "cryo pistol",
                             "cavitation", "cryogenic gauntlet"],
    },
    "earth": {
        "seismic": ["seismic"],
        "tectonic": ["tectonic"],
        "_mass_driver": ["mass driver", "kinetic impactor"],
    },
}


def like_pattern(keyword: str) -> str:
    """Return SQL LIKE pattern matching keyword as a substring (case-insensitive via LOWER)."""
    return f"%{keyword.lower()}%"


def fetch_matches(cur: sqlite3.Cursor, keywords: list[str]) -> list[tuple]:
    """Fetch all rows matching ANY of the keywords in canonical_name.

    Uses SQL LIKE for the broad pull then Python word-boundary regex to
    filter out false-positives ('Percussion cannon' matching 'ion cannon'
    because 'percuss-ion' ends in 'ion').
    """
    if not keywords:
        return []
    clauses = " OR ".join(["LOWER(canonical_name) LIKE ?"] * len(keywords))
    sql = f"""
        SELECT canonical_name, source_library, register_canonical,
               historical_period_canonical, proxy_attribute_class, quality_tier,
               weapon_kind, weapon_kind_classified_subtype
        FROM weapon_knowledge_entries
        WHERE {clauses}
    """
    params = [like_pattern(kw) for kw in keywords]
    cur.execute(sql, params)
    broad_results = cur.fetchall()

    # Build word-boundary regex (case-insensitive) for the keywords.
    # Each keyword is anchored at word boundaries on each end.
    patterns = []
    for kw in keywords:
        # Escape regex specials, then anchor with word boundaries.
        escaped = re.escape(kw)
        patterns.append(rf"\b{escaped}\b")
    combined_re = re.compile("|".join(patterns), re.IGNORECASE)

    filtered = []
    for row in broad_results:
        if combined_re.search(row[0]):
            filtered.append(row)
    return filtered


def classify_lineage(source_library: str) -> str:
    """Classify a row's lineage per Matt 2026-06-01 framing.

    Caster substrate was manually-authored; firearms/military hardware are crawl-extracted;
    historical/named-weapon catalogues like Met/Royal Armouries are crawl-extracted.
    Fantasy ARPG/TTRPG sources are typically crawl-extracted ARPG-canon catalogues.
    """
    manual_caster = {
        "engine_authored_gap_fill_v1",
        "legolas_crawl_substrate_enrichment_v1_2026_05_27",  # named anchor + thin-cell
    }
    modern_military_crawl = {
        "cataclysm-dda",          # post-apoc modern weapons
        "gta-v-data",             # contemporary firearms
        "odin-army-tradoc",       # modern military hardware
        "army-recognition",       # contemporary military
    }
    historical_crawl = {
        "royal_armouries",
        "met-museum",
        "wikipedia",
        "wikidata",
    }
    fantasy_crawl = {
        "nick-aschenbach-dnd-data",
        "wow-classic-items",
        "bsdata-warhammer-aos",
        "osrsbox-db",
        "pf2ools-pf2ools-data-quarantined",
        "diablo2-d2data",
        "path-of-exile-repoe",
        "fextralife-elden-ring",
        "bloqhead-demigods",
        "elden-ring-erdb",
        "fextralife-ds2",
        "fextralife-ds3",
        "fextralife-ds1",
        "5e-bits-5e-database-2024",
        "5e-bits-5e-database",
        "souls-api-thomaslincoln",
        "souls-api-thomaslincoln-quarantined",
    }
    if source_library in manual_caster:
        return "manually-authored"
    if source_library in modern_military_crawl:
        return "crawl-modern-military"
    if source_library in historical_crawl:
        return "crawl-historical"
    if source_library in fantasy_crawl:
        return "crawl-fantasy-arpg"
    return "crawl-other"


def is_caster_attribute(attr: str | None) -> bool:
    return attr in {"INT", "WIS", "INT_or_WIS", "WIS_or_INT", "STR_or_WIS"}


def is_caster_kind(kind: str | None, subtype: str | None) -> bool:
    """Heuristic: weapon_kind suggests caster vessel (tome/focus/talisman/horn/banner)
    OR subtype declares accessory_handheld (powder flasks/banners/focuses)."""
    caster_kinds = {"tome", "focus", "talisman", "horn", "banner"}
    if kind in caster_kinds:
        return True
    if subtype == "accessory_handheld":
        return True
    return False


def categorize_eligibility(row: tuple) -> str:
    """Return primary eligibility tag for a row.

    'strong'   = caster-attribute AND modern-period (industrial/modern/contemporary)
    'medium'   = caster-attribute OR modern-period (one but not both)
    'fantasy-fictional-modern-coded' = fictional period + sci-fi/modern naming (fantasy ARPG)
    'firearm'  = crawl-modern-military OR DEX-attribute modern hardware
    'other'    = none of the above
    """
    (
        canonical_name,
        source_library,
        register,
        period,
        attr,
        tier,
        kind,
        subtype,
    ) = row
    is_caster = is_caster_attribute(attr) or is_caster_kind(kind, subtype)
    modern_period = period in {"industrial", "modern", "contemporary"}
    fantasy_fictional = register == "fantasy" and period == "fictional"
    military_modern = register == "military_modern"

    lineage = classify_lineage(source_library)
    if is_caster and modern_period:
        return "strong"
    if is_caster and (fantasy_fictional or military_modern):
        # fantasy-fictional INT/WIS sci-fi-named OR military INT/WIS (rare)
        return "strong"
    if fantasy_fictional:
        # fantasy-fictional sci-fi-named: theme-eligible even if DEX
        return "fantasy-fictional-modern-coded"
    if modern_period or military_modern:
        return "firearm-or-modern-hardware"
    return "other"


def audit_primary(cur: sqlite3.Cursor, primary: str, overlays: dict[str, list[str]]) -> dict:
    """Audit one primary across all its overlay tokens."""
    result = {
        "primary": primary,
        "overlay_breakdown": {},  # overlay_token -> {eligibility -> count}
        "all_rows": [],          # deduped union across overlays
        "lineage_counts": defaultdict(int),
        "eligibility_counts": defaultdict(int),
    }
    seen_ids = set()
    for overlay_token, keywords in overlays.items():
        rows = fetch_matches(cur, keywords)
        breakdown = defaultdict(int)
        for row in rows:
            elig = categorize_eligibility(row)
            breakdown[elig] += 1
        result["overlay_breakdown"][overlay_token] = dict(breakdown)
        for row in rows:
            row_key = (row[0], row[1])  # canonical_name + source_library
            if row_key in seen_ids:
                continue
            seen_ids.add(row_key)
            result["all_rows"].append(row)
            result["lineage_counts"][classify_lineage(row[1])] += 1
            result["eligibility_counts"][categorize_eligibility(row)] += 1
    return result


def representative_reps(rows: list[tuple], n: int = 5) -> list[tuple]:
    """Return top N reps prioritized by:
    1. eligibility='strong'
    2. caster-attribute
    3. quality_tier (S > A > B > C)
    """
    tier_order = {"S": 0, "A": 1, "B": 2, "C": 3, None: 4, "": 4}

    def sort_key(row):
        elig = categorize_eligibility(row)
        elig_rank = {"strong": 0, "fantasy-fictional-modern-coded": 1,
                     "firearm-or-modern-hardware": 2, "other": 3}.get(elig, 3)
        is_caster_rank = 0 if is_caster_attribute(row[4]) else 1
        tier_rank = tier_order.get(row[5], 4)
        return (elig_rank, is_caster_rank, tier_rank)

    sorted_rows = sorted(rows, key=sort_key)
    return sorted_rows[:n]


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM weapon_knowledge_entries")
    total = cur.fetchone()[0]
    print(f"# WS2 Phase 1 Modern-Caster Substrate Coverage Audit")
    print(f"# Total weapon_knowledge_entries: {total}")
    print()

    for primary, overlays in OVERLAY_QUERIES.items():
        result = audit_primary(cur, primary, overlays)
        print(f"## Primary: {primary}")
        print(f"  total unique rows matched (any overlay): {len(result['all_rows'])}")
        print(f"  eligibility breakdown: {dict(result['eligibility_counts'])}")
        print(f"  lineage breakdown: {dict(result['lineage_counts'])}")
        print()
        print(f"  per-overlay-token breakdown:")
        for overlay, breakdown in result["overlay_breakdown"].items():
            total_for_overlay = sum(breakdown.values())
            strong = breakdown.get("strong", 0)
            fantasy_fictional = breakdown.get("fantasy-fictional-modern-coded", 0)
            firearm = breakdown.get("firearm-or-modern-hardware", 0)
            other = breakdown.get("other", 0)
            print(
                f"    {overlay}: total={total_for_overlay} "
                f"strong={strong} fantasy-fictional-modern={fantasy_fictional} "
                f"firearm-or-modern-hw={firearm} other={other}"
            )
        print()
        print(f"  top 5 representative reps (sorted by eligibility + caster-attr + tier):")
        for rep in representative_reps(result["all_rows"], n=5):
            name, src, reg, per, attr, tier, kind, subtype = rep
            print(
                f"    - '{name}' | src={src} | reg={reg} | per={per} | "
                f"attr={attr or '-'} | tier={tier or '-'} | "
                f"kind={kind or '-'} | subtype={subtype or '-'}"
            )
        print()
        print("---")
        print()

    conn.close()


if __name__ == "__main__":
    main()
