"""IA-2 Phase 1 magic-weapons-across-periods substrate audit.

Mode A read-only query against weapon_knowledge_entries (~90,220 rows).
Generates per-period × per-primary breakdowns for the 21-cell coverage grid.

Periods:
- ANCIENT  = pre_classical + classical (bronze-age myth + antiquity legendary)
- MEDIEVAL = medieval (enchanted, runed, named legendary, witch/alchemist focus)
- MODERN   = industrial + modern + contemporary (per WS2.P1; reused-by-reference)

7 rotating primaries: fire / water / earth / wind / lightning / holy / shadow
Physical excluded by design (Architecture A taxonomy-sibling registry).

Magic-weapon operational criteria (elrond seam):

  ANCIENT (pre_classical / classical):
    register = mythological OR
    (cultural_lineage_tags / canonical_name evidences mythological/divine attribution) AND
    a caster vessel weapon_kind OR INT/WIS proxy_attribute_class OR named_mythological_match

  MEDIEVAL (medieval):
    weapon_kind IN ('tome','focus','talisman','horn','banner') OR
    register = mythological OR
    canonical_name evidences enchantment/runed/grimoire/witch/named-legendary OR
    proxy_attribute_class = INT or WIS

  MODERN (industrial / modern / contemporary):
    Per WS2.P1 § 1.2:
    INT/WIS-coded modern-period caster-vessel sci-fi-coded implements

Per-primary association: keyword-anchored matching on canonical_name +
named_mythological_match using:
  - Q18 lock vocabulary (per primary)
  - mythological-canonical hero/deity associations (per primary)
  - WS2.P1 modern-caster overlay tokens (MODERN period only; per WS2.P1 audit)

Run: python3 ia2_phase1_magic_weapons_across_periods_audit.py
"""

from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

DB_PATH = Path.home() / "Games/reincarnated-loadout/data/telemetry.db"

# Period definitions (audit-internal)
ANCIENT_PERIODS = ("pre_classical", "classical")
MEDIEVAL_PERIODS = ("medieval",)
MODERN_PERIODS = ("industrial", "modern", "contemporary")

# Per-primary keyword grouping for ANCIENT + MEDIEVAL magic-weapon identification.
# Includes: Q18 lock vocabulary (broader, including substrate-validated) +
# mythological hero/deity vocabulary + magical-implement vocabulary.
#
# Word-boundary regex applied to canonical_name (case-insensitive).
#
# Note: ANCIENT/MEDIEVAL keywords differ structurally from MODERN keywords (which
# target sci-fi vocabulary). These keywords target mythological/legendary canon.
PRIMARY_KEYWORDS_ANCIENT_MEDIEVAL = {
    "fire": {
        "core_vocab": [
            "ember", "cinder", "blaze", "scorch", "inferno", "ignite", "fira",
            "lava", "magma", "charcoal", "char", "brand", "flare", "fire", "flame",
            "pyro", "burn", "agni", "xiuhcoatl", "agneya", "ifrit", "salamander",
            "phoenix", "vulcan", "hephaestus", "surt", "hestia",
        ],
        "implement_signals": [
            "fire staff", "flame staff", "fire wand", "fire focus", "fire tome",
            "flame focus", "fire amulet", "fire ring", "burning brand",
            "infernal", "incandescent",
        ],
    },
    "water": {
        "core_vocab": [
            "tide", "torrent", "glacial", "brine", "aqua", "frost", "chill",
            "mist", "ice", "glacier", "wave", "marsh", "water", "ocean", "sea",
            "river", "rain", "snow", "freeze", "poseidon", "njord", "tiamat",
            "leviathan", "ahti", "varuna", "lir", "manannan",
        ],
        "implement_signals": [
            "water staff", "ice wand", "frost focus", "tide focus", "water tome",
            "rain staff", "ice talisman", "water amulet", "tlaloc",
        ],
    },
    "earth": {
        "core_vocab": [
            "stone", "granite", "marble", "clay", "sand", "iron", "gold", "silver",
            "lead", "gem", "crystal", "obsidian", "amber", "quake", "tremor",
            "thorn", "earth", "rock", "mountain", "metal", "geb", "cybele",
            "demeter", "freyr", "jord", "prithvi", "tellus", "gaia",
        ],
        "implement_signals": [
            "earth staff", "stone wand", "crystal focus", "stone focus",
            "earth tome", "earth amulet", "stone talisman", "geomancer",
        ],
    },
    "wind": {
        "core_vocab": [
            "tempest", "cyclone", "whirlwind", "gale", "gust", "squall",
            "hurricane", "zephyr", "hail", "sleet", "cloud", "wind", "air",
            "storm", "breath", "fujin", "vayu", "vayavyastra", "njord",
            "aeolus", "stribog", "shu", "boreas",
        ],
        "implement_signals": [
            "wind staff", "air wand", "storm focus", "wind tome", "tempest staff",
            "gale staff", "stormcaller", "wind amulet",
        ],
    },
    "lightning": {
        "core_vocab": [
            "arc", "static", "surge", "volt", "bolt", "shock", "spark", "thunder",
            "lightning", "thunderbolt", "zeus", "thor", "indra", "raijin",
            "perun", "perkun", "mjolnir", "mjölnir", "gungnir", "vajra", "tonal",
        ],
        "implement_signals": [
            "thunder staff", "lightning wand", "storm focus", "thunder tome",
            "thunderbolt rod", "lightning rod", "thunder mace",
        ],
    },
    "holy": {
        "core_vocab": [
            "radiance", "radiant", "dawn", "aura", "divine", "sacred", "blessed",
            "lux", "celestial", "stellar", "solar", "light", "holy",
            "consecrated", "saint", "angel", "seraph", "cherub", "aasimar",
            "apollo", "amaterasu", "ra", "ahura mazda", "ra-horakhty",
            "raphael", "michael", "uriel", "gabriel",
        ],
        "implement_signals": [
            "holy staff", "divine focus", "sacred tome", "blessed amulet",
            "consecrated", "reliquary", "censer", "thurible", "cross",
            "crucifix", "ankh", "ank", "scarab", "wedjat", "trishula",
            "vajra", "sudarshana", "caduceus", "barsom",
        ],
    },
    "shadow": {
        "core_vocab": [
            "void", "shade", "wraith", "drain", "necrotic", "abyss", "shadow",
            "lich", "blackhole", "singularity", "darkmatter", "soul", "dark",
            "night", "death", "grave", "tomb", "specter", "spectre", "phantom",
            "wight", "wraith", "anubis", "hades", "hel", "yama", "kali",
            "morrigan", "nyx", "erebus",
        ],
        "implement_signals": [
            "shadow staff", "dark wand", "necromancer", "necromantic", "death tome",
            "shadow focus", "soul gem", "soul focus", "skull", "bone",
        ],
    },
}

# MODERN keywords reused from WS2.P1 audit (incorporated by reference, not re-executed)
WS2_P1_MODERN_OVERLAY_KEYWORDS = {
    "lightning": ["tesla", "voltage", "ion cannon", "ion rifle", "ion pistol",
                  "ion gun", "ion blast", "ion lance", "ion blade", "ion bomb",
                  "ion grenade", "ionization", "ionizer", "ion sword",
                  "flashbang", "flash grenade", "flashbomb", "flash cannon",
                  "flash pistol", "flash bomb", "flash rifle",
                  "coilgun", "coil gun", "railgun", "rail gun",
                  "electromagnetic pulse", " emp ", "emp grenade", "emp bomb",
                  "emp pistol", "plasma"],
    "fire": ["fusion", "thermal", "thermite", "combustion",
             "flamethrower", "incendiary"],
    "holy": ["photon", "photonic", "laser", "prism", "prismatic",
             "radiant emitter", "light amplifier", "light amplification",
             "photonic projector"],
    "shadow": ["black hole", "blackhole", "singularity", "dark matter",
               "darkmatter", "antimatter", "voidmaw"],
    "wind": ["sonic emitter", "sonic cannon", "sonic gun", "sonic blast",
             "sonic bomb", "sonic rifle", "sonic taser", "sonic amplifier",
             "sonic spear", "sonic disruptor", "shockwave", "shock wave",
             "acoustic", "pressure cannon"],
    "water": ["hydro cannon", "hydro pistol", "hydro rifle", "hydro blast",
              "hydro gun", "hydropump", "hydraulic press weapon",
              "hydraulic hammer", "cryo bomb", "cryo grenade", "cryo gun",
              "cryo cannon", "cryo rifle", "cryo pistol", "cavitation",
              "cryogenic gauntlet"],
    "earth": ["seismic", "tectonic", "mass driver", "kinetic impactor"],
}

# Manually-authored sources (per WS2.P1 audit § 1.3)
MANUAL_SOURCES = {
    "engine_authored_gap_fill_v1",
    "legolas_crawl_substrate_enrichment_v1_2026_05_27",
}


def build_word_boundary_regex(keywords):
    """Build a single case-insensitive regex matching any keyword at word boundaries."""
    patterns = [rf"\b{re.escape(kw)}\b" for kw in keywords]
    return re.compile("|".join(patterns), re.IGNORECASE)


def fetch_period_rows(cur, periods):
    """Fetch ALL rows for the given period set. Returns list of dict-like rows."""
    placeholders = ",".join("?" for _ in periods)
    sql = f"""
        SELECT id, canonical_name, source_library, register_canonical,
               historical_period_canonical, proxy_attribute_class, quality_tier,
               weapon_kind, weapon_kind_classified_subtype,
               named_mythological_match, cultural_lineage_tags,
               structured_properties, cultural_lineage_canonical
        FROM weapon_knowledge_entries
        WHERE historical_period_canonical IN ({placeholders})
    """
    cur.execute(sql, periods)
    rows = cur.fetchall()
    return rows


def is_caster_vessel(weapon_kind, subtype):
    caster_kinds = {"tome", "focus", "talisman", "horn", "banner"}
    if weapon_kind in caster_kinds:
        return True
    if subtype == "accessory_handheld":
        return True
    return False


def is_caster_attribute(attr):
    return attr in {"INT", "WIS", "INT_or_WIS", "WIS_or_INT", "STR_or_WIS"}


def matches_primary_keyword_ancient_medieval(row, primary):
    """Check if a row's canonical_name OR named_mythological_match matches the
    primary's ancient/medieval vocabulary."""
    name = row[1] or ""
    myth_match = row[9] or ""
    structured = row[11] or ""
    keywords = (
        PRIMARY_KEYWORDS_ANCIENT_MEDIEVAL[primary]["core_vocab"]
        + PRIMARY_KEYWORDS_ANCIENT_MEDIEVAL[primary]["implement_signals"]
    )
    rx = build_word_boundary_regex(keywords)
    if rx.search(name) or rx.search(myth_match) or rx.search(structured):
        return True
    return False


def matches_primary_keyword_modern(row, primary):
    """Check if a row's canonical_name matches WS2.P1 modern keywords."""
    name = (row[1] or "").lower()
    keywords = WS2_P1_MODERN_OVERLAY_KEYWORDS.get(primary, [])
    for kw in keywords:
        if kw in name:
            # word-boundary check
            rx = re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)
            if rx.search(row[1] or ""):
                return True
    return False


def is_magic_weapon_ancient(row):
    """ANCIENT period magic-weapon operational criterion."""
    (_, name, src, register, period, attr, tier, kind, subtype,
     myth_match, lineage_tags, structured, cult_lin) = row
    # register=mythological is highest-confidence signal
    if register == "mythological":
        return True
    # named_mythological_match means substrate's classifier flagged it as
    # tied to a mythological figure
    if myth_match:
        return True
    # caster-vessel weapon_kind in ancient period
    if is_caster_vessel(kind, subtype):
        return True
    # INT/WIS attribute means the substrate classified it as caster
    if is_caster_attribute(attr):
        return True
    return False


def is_magic_weapon_medieval(row):
    """MEDIEVAL period magic-weapon operational criterion."""
    (_, name, src, register, period, attr, tier, kind, subtype,
     myth_match, lineage_tags, structured, cult_lin) = row
    if register == "mythological":
        return True
    if myth_match:
        return True
    if is_caster_vessel(kind, subtype):
        return True
    if is_caster_attribute(attr):
        return True
    # Named medieval legendary: matches enchanted/runed/named/grimoire vocab
    enchanted_keywords = [
        "enchanted", "runed", "rune", "grimoire", "witch", "alchemist",
        "alchemic", "alchemy", "warlock", "wizard", "sorcerer", "sorceress",
        "mage", "magus", "magi", "magical", "magic", "ritual", "blessed",
        "consecrated", "cursed",
    ]
    name_lower = (name or "").lower()
    for kw in enchanted_keywords:
        if kw in name_lower:
            rx = re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)
            if rx.search(name):
                return True
    return False


def is_magic_weapon_modern(row):
    """MODERN period magic-weapon criterion (per WS2.P1 § 1.2)."""
    (_, name, src, register, period, attr, tier, kind, subtype,
     myth_match, lineage_tags, structured, cult_lin) = row
    # Per WS2.P1 § 1.2 strong-eligible criterion
    is_caster = is_caster_attribute(attr) or is_caster_vessel(kind, subtype)
    modern_period = period in MODERN_PERIODS
    fantasy_fictional = register == "fantasy" and period == "fictional"
    military_modern = register == "military_modern"
    if is_caster and modern_period:
        return True
    if is_caster and (fantasy_fictional or military_modern):
        return True
    if fantasy_fictional:
        return True
    return False


def classify_lineage(src):
    if src in MANUAL_SOURCES:
        return "manually-authored"
    return "crawl-extracted"


def gap_verdict(strong_count):
    """STRONG / MEDIUM / WEAK / ABSENT verdict per cell."""
    if strong_count >= 20:
        return "STRONG"
    if strong_count >= 8:
        return "MEDIUM"
    if strong_count >= 2:
        return "WEAK"
    return "ABSENT"


def audit_period(cur, period_name, periods, primary_matcher, magic_filter):
    """Audit a period across all 7 primaries.

    primary_matcher: callable (row, primary) -> bool
    magic_filter: callable (row) -> bool
    """
    rows = fetch_period_rows(cur, periods)
    print(f"\n## {period_name} ({'/'.join(periods)}) — {len(rows)} total rows in period\n")

    results = {}
    for primary in ["fire", "water", "earth", "wind", "lightning", "holy", "shadow"]:
        magic_rows = []
        for row in rows:
            if not magic_filter(row):
                continue
            if not primary_matcher(row, primary):
                continue
            magic_rows.append(row)

        manual_rows = [r for r in magic_rows if classify_lineage(r[2]) == "manually-authored"]
        crawl_rows = [r for r in magic_rows if classify_lineage(r[2]) == "crawl-extracted"]
        # caster-attribute sub-count
        caster_attr = [r for r in magic_rows if is_caster_attribute(r[5])]
        caster_vessel = [r for r in magic_rows if is_caster_vessel(r[7], r[8])]

        verdict = gap_verdict(len(magic_rows))

        # Top reps: prioritize caster-attribute + tier
        def rep_sort_key(r):
            tier_order = {"S": 0, "A": 1, "B": 2, "C": 3, None: 4, "": 4}
            return (
                0 if is_caster_attribute(r[5]) else 1,
                tier_order.get(r[6], 4),
                0 if r[9] else 1,  # named_mythological_match present
            )

        reps = sorted(magic_rows, key=rep_sort_key)[:5]

        # Lineage breakdown by source library
        src_counts = defaultdict(int)
        for r in magic_rows:
            src_counts[r[2]] += 1

        results[primary] = {
            "count": len(magic_rows),
            "verdict": verdict,
            "manual": len(manual_rows),
            "crawl": len(crawl_rows),
            "caster_attr": len(caster_attr),
            "caster_vessel": len(caster_vessel),
            "top_reps": reps,
            "source_counts": dict(src_counts),
        }

        print(f"### {primary} — {len(magic_rows)} magic-weapon rows | verdict: {verdict}")
        print(f"  Lineage: manually-authored={len(manual_rows)} crawl-extracted={len(crawl_rows)}")
        print(f"  Caster signal: caster-attr={len(caster_attr)} caster-vessel-kind={len(caster_vessel)}")
        print(f"  Top sources: {sorted(src_counts.items(), key=lambda x: -x[1])[:5]}")
        print(f"  Top reps:")
        for rep in reps:
            name = rep[1]
            src = rep[2]
            reg = rep[3]
            per = rep[4]
            attr = rep[5] or "-"
            tier = rep[6] or "-"
            kind = rep[7] or "-"
            myth = rep[9] or "-"
            print(f"    - '{name}' | src={src} | reg={reg} | per={per} | attr={attr} | tier={tier} | kind={kind} | myth={myth}")
        print()

    return results


def main():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM weapon_knowledge_entries")
    total = cur.fetchone()[0]
    print(f"# IA-2 Phase 1 Magic-Weapons-Across-Periods Substrate Coverage Audit")
    print(f"# Total weapon_knowledge_entries: {total}")
    print(f"# 21-cell grid: ANCIENT + MEDIEVAL + MODERN × 7 primaries")
    print()

    print("=" * 80)
    ancient_results = audit_period(
        cur, "ANCIENT", ANCIENT_PERIODS,
        matches_primary_keyword_ancient_medieval,
        is_magic_weapon_ancient,
    )

    print("=" * 80)
    medieval_results = audit_period(
        cur, "MEDIEVAL", MEDIEVAL_PERIODS,
        matches_primary_keyword_ancient_medieval,
        is_magic_weapon_medieval,
    )

    print("=" * 80)
    modern_results = audit_period(
        cur, "MODERN", MODERN_PERIODS,
        matches_primary_keyword_modern,
        is_magic_weapon_modern,
    )

    print("=" * 80)
    print("\n## 21-CELL COVERAGE GRID SUMMARY\n")
    print(f"{'Primary':<12}{'ANCIENT':<15}{'MEDIEVAL':<15}{'MODERN':<15}")
    for primary in ["fire", "water", "earth", "wind", "lightning", "holy", "shadow"]:
        a = ancient_results[primary]
        m = medieval_results[primary]
        mo = modern_results[primary]
        print(f"{primary:<12}{a['count']:<3} {a['verdict']:<11}{m['count']:<3} {m['verdict']:<11}{mo['count']:<3} {mo['verdict']:<11}")
    print()

    # Aggregate stats
    print("\n## AGGREGATE LINEAGE STATS\n")
    for label, results in [("ANCIENT", ancient_results), ("MEDIEVAL", medieval_results), ("MODERN", modern_results)]:
        total_manual = sum(r["manual"] for r in results.values())
        total_crawl = sum(r["crawl"] for r in results.values())
        print(f"{label}: manually-authored={total_manual} crawl-extracted={total_crawl}")

    conn.close()


if __name__ == "__main__":
    main()
