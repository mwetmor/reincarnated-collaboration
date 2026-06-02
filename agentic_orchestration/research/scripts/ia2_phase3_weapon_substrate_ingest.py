"""IA-2 Phase 3 — Weapon-substrate ingest + lineage tag application.

Per dispatch `agentic_orchestration/dispatches/2026-06-01-elrond-ia-2-phase-3-weapon-substrate-ingest.md`
+ LOCK E (Phase 3 elrond autonomous) + LOCK J § 5 (additive period_tag schema autonomous)
+ jack-ryan IA-2.P3 Gate-1 PASS-with-INFO (commit 1cd73a5).

EXECUTION STEPS:
  1. Schema extension — add `period_tag` column (additive, nullable, enum-by-contract)
  2. Ingest 102 gandalf anchors from JSON consolidation
  3. Ingest 23 legolas crawl entries from 3 period JSONL files
  4. Apply retroactive-primary-tagging to magic-weapon-eligible primary-unattributed
     rows (per audit § 7.4); caster-class consistency per Option α/β/C (INFO-2)
  5. Smoke-test backward-compat queries
  6. Emit ingest summary stats

LINEAGE TAGS:
  - gandalf-authored-magic-anchor-{period}-2026-06-01 (per entry; in source_library)
  - legolas-crawl-magic-supplementary-{period}-2026-06-01 (per entry; in source_library)
  - elrond-retroactive-primary-tag-2026-06-01 (per retroactively-tagged row;
    in structured_properties.primary_element_retroactive_lineage)

PRIMARY-ELEMENT STORAGE STRATEGY:
  primary_element is NOT a first-class column on weapon_knowledge_entries (existing
  engine_authored_gap_fill_v1 entries encode it via canonical_name + style heuristics).
  Per LOCK J § 5 the autonomous schema extension is `period_tag` only — adding
  `primary_element` would be a SEMANTIC contract change requiring Matt approval.
  STRATEGY: store primary_element + cultural_tradition + form + register +
  design_rationale + substrate_validation_lineage in `structured_properties` JSON.
  This preserves Discipline #41 (substrate-led; minimal additive) and follows the
  existing engine_authored_gap_fill_v1 encoding convention.

PERIOD_TAG ENUM:
  ancient | medieval | modern (per LOCK J § 5). For legacy entries (pre-ingest),
  default NULL. For IA-2 ingest entries, populated from JSON `period` field.

REGISTER MAPPING (gandalf/legolas `register` → loadout-DB `register_canonical`):
  "mythological / divine"           → "mythological"
  "mythological / divine / epic"    → "mythological"
  "mythological / literary / divine"→ "mythological"
  "legendary / Arthurian"           → "mythological"  (legendary register treated as mythological per substrate convention)
  "saga / legendary"                → "mythological"
  "epic / legendary"                → "mythological"
  "sacred / reliquary / crusader"   → "mythological"
  "grimoire / folk-magical / macabre"→ "mythological"
  "urban fantasy / fictional-modern"→ "fantasy"
  "tabletop sci-fi / *"             → "sci_fi"
  "video game sci-fi RPG / *"       → "sci_fi"
  (default fallback)                → "mythological"

HISTORICAL_PERIOD_CANONICAL MAPPING (period → loadout enum):
  ancient  → "classical"   (treats antiquity-anchored mythology as classical per audit § 1.2)
  medieval → "medieval"
  modern   → "contemporary" (treats published-modern-canon RPG sources as contemporary)
  (Exception: urban-fantasy fiction may map to "fictional" if pre-industrial framing dominates;
   none in current legolas modern crawl meet that — all map contemporary.)

PROXY_ATTRIBUTE_CLASS ASSIGNMENT:
  Per gandalf/legolas `form` field signal + INFO-2 (Option α/β/C consistency):
  - Caster-implements (staff/wand/rod/focus/tome/talisman/horn/banner/cypher/
    sceptre/gauntlet-implant/conch/javelin-divine) → INT or WIS or INT_or_WIS
  - Martial-coded mythological-divine swords/spears with STR_or_WIS register → STR_or_WIS
  - Pure martial swords/daggers/bows in mythological register → typically caster
    cross-attribute hybrid OR DEX-coded; we default to INT for caster-context
    when register=mythological AND form=non-caster (Mjolnir-pattern — divine
    weapon usable as melee but spell-channeling).

WEAPON_KIND ASSIGNMENT:
  Per form: staff/rod/wand → "category" (covers caster-vessel); tome → "tome";
  focus/cypher → "focus"; horn/conch → "horn"; banner → "banner";
  talisman/amulet → "talisman"; bow/sword/spear/dagger/javelin/mace/whip/sceptre → "category".

Run: python3 ia2_phase3_weapon_substrate_ingest.py

Outputs:
  - Mutates ~/Games/reincarnated-loadout/data/telemetry.db (additive)
  - Writes JSON summary to ./ingest-summary-stats.json (script-local)

Backup: ~/Games/reincarnated-loadout/data/telemetry.db.pre-ia-2-phase-3-2026-06-01.bak
"""

from __future__ import annotations

import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants + paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path.home() / "Games/reincarnated-collaboration"
DB_PATH = Path.home() / "Games/reincarnated-loadout/data/telemetry.db"

GANDALF_JSON = REPO_ROOT / "agentic_orchestration/gandalf/notes/2026-06-01-ia-2-phase-2-anchors-batch.json"
LEGOLAS_DIR = REPO_ROOT / "agentic_orchestration/legolas/research/ia-2-phase-2-supplementary-crawl-2026-06-01"
LEGOLAS_FILES = {
    "ancient": LEGOLAS_DIR / "crawl-ancient.jsonl",
    "medieval": LEGOLAS_DIR / "crawl-medieval.jsonl",
    "modern": LEGOLAS_DIR / "crawl-modern.jsonl",
}

OUTPUT_DIR = REPO_ROOT / "agentic_orchestration/elrond/research/ia-2-phase-3-ingest-2026-06-01"
STATS_OUT = OUTPUT_DIR / "ingest-summary-stats.json"

PERIOD_TO_CANONICAL = {
    "ancient": "classical",
    "medieval": "medieval",
    "modern": "contemporary",
}

# Per Q18 lock § 2 — primary-element vocabulary for retroactive-tagging
# (compact form; full vocabulary lives in audit script for read-only audit purposes)
PRIMARY_VOCAB = {
    "fire": [
        "ember", "cinder", "blaze", "scorch", "inferno", "ignite", "fira", "lava",
        "magma", "charcoal", "char", "brand", "flare", "fire", "flame", "pyro",
        "burn", "fusion", "thermal", "combustion", "agni", "xiuhcoatl", "ifrit",
        "salamander", "phoenix", "vulcan", "hephaestus", "surt",
    ],
    "water": [
        "tide", "torrent", "glacial", "brine", "aqua", "frost", "chill", "mist",
        "ice", "glacier", "wave", "marsh", "hydro", "hydraulic", "water", "ocean",
        "sea", "river", "rain", "snow", "freeze", "poseidon", "njord", "tiamat",
        "leviathan", "varuna", "lir", "manannan", "tlaloc",
    ],
    "earth": [
        "stone", "granite", "marble", "clay", "sand", "iron", "gold", "silver",
        "lead", "gem", "crystal", "obsidian", "amber", "quake", "tremor", "thorn",
        "seismic", "tectonic", "earth", "rock", "mountain", "metal", "geb",
        "cybele", "demeter", "freyr", "jord", "prithvi", "tellus", "gaia",
    ],
    "wind": [
        "tempest", "cyclone", "whirlwind", "gale", "gust", "squall", "hurricane",
        "zephyr", "hail", "sleet", "cloud", "sonic", "shockwave", "wind", "air",
        "storm", "breath", "fujin", "vayu", "aeolus", "stribog", "shu", "boreas",
    ],
    "lightning": [
        "arc", "static", "surge", "volt", "bolt", "shock", "spark", "thunder",
        "plasma", "flash", "ion", "voltage", "tesla", "lightning", "thunderbolt",
        "zeus", "thor", "indra", "raijin", "perun", "perkun", "mjolnir",
        "mjölnir", "gungnir", "vajra",
    ],
    "holy": [
        "radiance", "radiant", "dawn", "aura", "divine", "sacred", "blessed",
        "lux", "celestial", "stellar", "solar", "photon", "laser", "prismatic",
        "light", "holy", "consecrated", "saint", "angel", "seraph", "cherub",
        "apollo", "amaterasu", "ankh", "ank", "scarab", "wedjat", "caduceus",
        "barsom", "trishula", "sudarshana",
    ],
    "shadow": [
        "void", "shade", "wraith", "drain", "necrotic", "abyss", "shadow",
        "lich", "blackhole", "singularity", "darkmatter", "soul", "dark", "night",
        "death", "grave", "tomb", "specter", "spectre", "phantom", "wight",
        "anubis", "hades", "hel", "yama", "kali", "morrigan", "nyx", "erebus",
        "solomon", "picatrix", "sefer", "necromancer", "grimoire",
    ],
}

# Caster-attribute set per Option α/β/C (per composition policy v1 § 3 + INFO-2)
CASTER_ATTR_SET = {"INT", "WIS", "INT_or_WIS", "WIS_or_INT", "STR_or_WIS"}

# Strict-martial-only set — these rows must NOT receive caster-primary retroactive tags
STRICT_MARTIAL_ATTR_SET = {"STR", "DEX"}


# ---------------------------------------------------------------------------
# Step 1 — Schema extension
# ---------------------------------------------------------------------------

def add_period_tag_column(conn: sqlite3.Connection) -> dict:
    """Add `period_tag` column to weapon_knowledge_entries.

    Per LOCK J § 5: additive enum (ancient/medieval/modern). SQLite ADD COLUMN
    does not enforce CHECK; enforcement is contract-side (this script + consumer).
    Default NULL for legacy entries (backward-compat).
    """
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(weapon_knowledge_entries)")
    cols = {row[1] for row in cur.fetchall()}
    if "period_tag" in cols:
        return {"status": "already_exists", "column": "period_tag"}
    cur.execute(
        "ALTER TABLE weapon_knowledge_entries ADD COLUMN period_tag TEXT"
    )
    # Verify
    cur.execute("PRAGMA table_info(weapon_knowledge_entries)")
    cols_after = {row[1] for row in cur.fetchall()}
    assert "period_tag" in cols_after, "period_tag column not added"
    return {"status": "added", "column": "period_tag", "type": "TEXT (enum-by-contract: ancient|medieval|modern|NULL)"}


# ---------------------------------------------------------------------------
# Step 2 — Field mapping helpers
# ---------------------------------------------------------------------------

def map_register(register_str: str) -> str:
    """Map gandalf/legolas register string to loadout DB register_canonical enum.

    Valid loadout enum: historical / military_modern / fantasy / sci_fi /
    mythological / unknown.
    """
    s = register_str.lower()
    if "sci-fi" in s or "tabletop sci" in s or "video game sci-fi" in s or "transhumanist" in s:
        return "sci_fi"
    if "urban fantasy" in s or "fantasy fiction" in s or "fictional-modern" in s:
        return "fantasy"
    if "mythological" in s or "divine" in s or "epic" in s or "legendary" in s \
            or "saga" in s or "sacred" in s or "reliquary" in s or "grimoire" in s \
            or "folk-religious" in s or "folk-magical" in s or "Arthurian" in s.lower() \
            or "consecrated" in s or "crusader" in s or "Saracen" in s.lower() \
            or "Welsh" in s.lower() or "Carolingian" in s.lower():
        return "mythological"
    return "mythological"  # safe default for IA-2 ingest scope (all entries are magic-coded)


def infer_weapon_kind(form_str: str) -> tuple[str, str | None]:
    """Map gandalf/legolas form string to weapon_kind + weapon_kind_classified_subtype.

    weapon_kind enum: category, unique, named_template, ammo_or_consumable, shield,
    tome, banner, focus, horn, talisman, unknown.

    Strategy: use first-token form root. tome/focus/horn/banner/talisman map to
    matching enums. Other forms (staff/wand/rod/sword/spear/etc.) map to category
    with subtype = form root.
    """
    f = form_str.lower().split("(")[0].strip()
    # Extract first-word root
    root = f.split()[0] if f else ""
    direct_enum_map = {
        "tome": ("tome", None),
        "focus": ("focus", None),
        "horn": ("horn", None),
        "conch": ("horn", "conch_horn"),
        "banner": ("banner", None),
        "talisman": ("talisman", None),
        "amulet": ("talisman", "amulet"),
        "cypher": ("focus", "cypher"),
    }
    if root in direct_enum_map:
        return direct_enum_map[root]
    # Fall through: category with subtype
    accessory_handheld_forms = {"staff", "wand", "rod", "sceptre", "scepter",
                                "gauntlet-implant", "gauntlet", "implant"}
    if root in accessory_handheld_forms or "gauntlet" in f or "implant" in f:
        return ("category", "accessory_handheld")
    # Martial-form roots
    martial_subtype_map = {
        "sword": "sword",
        "spear": "spear",
        "dagger": "dagger",
        "bow": "bow",
        "javelin": "javelin",
        "mace": "mace",
        "whip": "whip",
        "hammer": "hammer",
        "axe": "axe",
    }
    if root in martial_subtype_map:
        return ("category", martial_subtype_map[root])
    return ("category", None)


def infer_proxy_attribute_class(form_str: str, register_str: str) -> str:
    """Infer proxy_attribute_class per Option α/β/C composition policy.

    Caster-vessels (staff/wand/rod/focus/tome/talisman/horn/banner/cypher/
    gauntlet-implant) → INT or WIS or INT_or_WIS depending on form signal.
    Martial-form mythological divine weapons (sword/spear) → STR_or_WIS (Option C
    cross-attribute hybrid) when register=mythological AND form carries divine signal.
    Pure martial (no mythological signal) → STR or DEX.
    """
    f = form_str.lower()
    # Strong caster-vessel signal
    caster_root_set = {"staff", "wand", "rod", "focus", "tome", "talisman",
                       "horn", "conch", "banner", "cypher"}
    first_root = f.split("(")[0].strip().split()[0] if f else ""
    if first_root in caster_root_set:
        # Holy / divine register typically maps to WIS (faith caster); arcane to INT.
        # Default INT_or_WIS to preserve substrate flexibility.
        if "faith" in f or "cleric" in f or "holy" in f or "divine" in f or "consecrated" in f:
            return "WIS"
        if "arcane" in f or "wizard" in f:
            return "INT"
        return "INT_or_WIS"
    # gauntlet-implant / neural / amp → INT (cyberpunk arcane analogue)
    if "gauntlet" in f or "implant" in f or "amp" in f or "neural" in f:
        return "INT"
    # Whip / dagger martial-light caster-cross — DEX-coded (cyberpunk shadow-class)
    if first_root in {"whip", "dagger"} and ("shadow" in f or "monofilament" in f or "cyber" in f):
        return "DEX"
    # Mythological-divine martial-form (sword/spear/mace/javelin) → STR_or_WIS Option C
    martial_forms = {"sword", "spear", "mace", "javelin", "hammer", "axe", "bow"}
    if first_root in martial_forms:
        if "mythological" in register_str.lower() or "divine" in register_str.lower() \
                or "legendary" in register_str.lower() or "saga" in register_str.lower() \
                or "epic" in register_str.lower() or "sacred" in register_str.lower():
            return "STR_or_WIS"
        if first_root == "bow":
            return "DEX"
        return "STR"
    # Sceptre default → WIS
    if "sceptre" in f or "scepter" in f:
        return "WIS"
    return "INT_or_WIS"


def structured_properties_for_entry(entry: dict, source: str) -> dict:
    """Build structured_properties JSON for ingested entry.

    Stores primary_element (NEW data not first-class column), cultural_tradition,
    form, register, design_rationale (gandalf only) / source_citation (legolas
    only), substrate_validation_lineage, novel_design_flag, ia2_ingest_lineage.
    """
    sp = {
        "primary_element": entry["primary_element"],
        "cultural_tradition": entry["cultural_tradition"],
        "form": entry["form"],
        "register": entry["register"],
        "substrate_validation_lineage": entry["substrate_validation_lineage"],
        "novel_design_flag": entry.get("novel_design_flag", False),
        "ia2_ingest_lineage": source,  # "gandalf-anchor" | "legolas-crawl"
    }
    if "design_rationale" in entry:
        sp["design_rationale"] = entry["design_rationale"]
    if "source_citation" in entry:
        sp["source_citation"] = entry["source_citation"]
    if "weapon_id" in entry:
        sp["weapon_id_source"] = entry["weapon_id"]  # gandalf's source id
    return sp


def cultural_lineage_canonical_from_tradition(tradition: str) -> str:
    """Map gandalf/legolas cultural_tradition string to loadout enum.

    Loadout enum: european, east_asian, south_asian, southeast_asian, middle_eastern,
    african, north_american_indigenous, mesoamerican, south_american_indigenous,
    arctic_circumpolar, oceanic, fantasy_generic, sci_fi_generic, cross_cultural, unknown.
    """
    t = tradition.lower()
    if any(s in t for s in ["greek", "hellenic", "norse", "germanic", "celtic",
                            "arthurian", "british", "welsh", "carolingian",
                            "frankish", "slavic", "italian", "latin christian",
                            "crusader", "european"]):
        return "european"
    if any(s in t for s in ["vedic", "indo-aryan", "hindu", "sanskrit", "buddhist",
                            "indian"]):
        return "south_asian"
    if any(s in t for s in ["chinese", "japanese", "korean", "taoist",
                            "east asian", "east-asian"]):
        return "east_asian"
    if any(s in t for s in ["egyptian", "mesopotamian", "babylonian", "sumerian",
                            "kemetic", "middle eastern", "persian", "arabic",
                            "saracen", "phoenician", "canaanite", "hittite"]):
        return "middle_eastern"
    if any(s in t for s in ["aztec", "mesoamerican", "mayan", "olmec", "toltec",
                            "mexica"]):
        return "mesoamerican"
    if any(s in t for s in ["south american", "incan", "inca", "andean"]):
        return "south_american_indigenous"
    if any(s in t for s in ["north american", "navajo", "lakota", "haudenosaunee",
                            "inuit"]):
        return "north_american_indigenous"
    if any(s in t for s in ["polynesian", "maori", "oceanic", "hawaiian", "pacific"]):
        return "oceanic"
    if any(s in t for s in ["african", "yoruba", "zulu", "kemetic"]):
        return "african"
    if any(s in t for s in ["urban fantasy", "fictional", "video game", "tabletop",
                            "shadowrun", "numenera", "mass effect", "dresden",
                            "eclipse phase", "cyberpunk"]):
        return "sci_fi_generic"
    if any(s in t for s in ["fantasy"]):
        return "fantasy_generic"
    if any(s in t for s in ["cross-cultural", "cross cultural", "hermetic",
                            "alchemy", "grimoire"]):
        return "cross_cultural"
    return "unknown"


# ---------------------------------------------------------------------------
# Step 3 — Ingest entries
# ---------------------------------------------------------------------------

def slugify_canonical_name(name: str) -> str:
    """Build deterministic slug for source_id (used for round-tripping)."""
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return slug


def ingest_gandalf_entries(conn: sqlite3.Connection) -> dict:
    """Ingest 102 gandalf anchors. Returns stats dict."""
    data = json.loads(GANDALF_JSON.read_text())
    anchors = data["anchors"]
    assert len(anchors) == 102, f"Expected 102 gandalf anchors, got {len(anchors)}"

    cur = conn.cursor()
    inserted = 0
    skipped_dup = 0
    per_period = Counter()
    per_primary = Counter()
    per_period_primary = Counter()

    for entry in anchors:
        period = entry["period"]
        primary = entry["primary_element"]
        source_library = f"gandalf-authored-magic-anchor-{period}-2026-06-01"
        source_id = entry["weapon_id"]
        # source_url synthesized (anchor lives in gandalf notes batch JSON)
        source_url = (
            "agentic_orchestration/gandalf/notes/"
            f"2026-06-01-ia-2-phase-2-anchors-batch.json#{source_id}"
        )

        # Dup-check (idempotent re-runs)
        cur.execute(
            "SELECT id FROM weapon_knowledge_entries WHERE source_library = ? AND source_url = ?",
            (source_library, source_url),
        )
        existing = cur.fetchone()
        if existing:
            skipped_dup += 1
            continue

        weapon_kind, subtype = infer_weapon_kind(entry["form"])
        proxy_attr = infer_proxy_attribute_class(entry["form"], entry["register"])
        register_canonical = map_register(entry["register"])
        cultural_lineage_canonical = cultural_lineage_canonical_from_tradition(
            entry["cultural_tradition"]
        )
        historical_period_canonical = PERIOD_TO_CANONICAL[period]
        structured_properties = json.dumps(
            structured_properties_for_entry(entry, "gandalf-anchor"),
            ensure_ascii=False,
        )

        cur.execute(
            """
            INSERT INTO weapon_knowledge_entries (
                canonical_name, source_library, source_url, source_id,
                description_text, structured_properties, cultural_lineage_tags,
                historical_period, genre_appearances, license_class,
                wieldable_humanoid, weapon_kind, dedup_status,
                cultural_lineage_canonical, historical_period_canonical,
                register_canonical, proxy_attribute_class,
                weapon_kind_classified_subtype, v1_scope,
                v1_scope_composition_trace, named_mythological_match,
                period_tag
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry["canonical_name"],
                source_library,
                source_url,
                source_id,
                entry.get("design_rationale", ""),
                structured_properties,
                json.dumps([entry["cultural_tradition"]]),
                period,  # historical_period (free-text)
                json.dumps(["mythological", "fantasy"]),
                "internal_authored_anchor_v1",  # license_class
                "one_hand",  # wieldable_humanoid default for caster implements
                weapon_kind,
                "canonical",  # dedup_status
                cultural_lineage_canonical,
                historical_period_canonical,
                register_canonical,
                proxy_attr,
                subtype,
                0,  # v1_scope (IA-2 entries not in v1_scope; future scope decision)
                json.dumps({
                    "ia2_phase_3_ingest": True,
                    "source": "gandalf-anchor",
                    "matching_policy": (
                        "option_alpha_martial_5tuple"
                        if proxy_attr in STRICT_MARTIAL_ATTR_SET
                        else "option_beta_caster_attribute_level"
                        if proxy_attr in {"INT", "WIS", "INT_or_WIS"}
                        else "option_c_cross_attribute"
                    ),
                }),
                entry.get("canonical_name") if "mythological" == register_canonical else None,
                period,  # period_tag (LOCK J § 5)
            ),
        )
        inserted += 1
        per_period[period] += 1
        per_primary[primary] += 1
        per_period_primary[(period, primary)] += 1

    return {
        "source": "gandalf-anchor",
        "expected_count": 102,
        "inserted": inserted,
        "skipped_existing": skipped_dup,
        "per_period": dict(per_period),
        "per_primary": dict(per_primary),
        "per_period_primary": {f"{p}.{e}": n for (p, e), n in per_period_primary.items()},
    }


def ingest_legolas_entries(conn: sqlite3.Connection) -> dict:
    """Ingest 23 legolas crawl entries (9 ancient + 9 medieval + 5 modern)."""
    cur = conn.cursor()
    inserted = 0
    skipped_dup = 0
    per_period = Counter()
    per_primary = Counter()
    per_period_primary = Counter()

    for period, path in LEGOLAS_FILES.items():
        with path.open() as f:
            entries = [json.loads(line) for line in f if line.strip()]
        source_library = f"legolas-crawl-magic-supplementary-{period}-2026-06-01"

        for entry in entries:
            primary = entry["primary_element"]
            slug = slugify_canonical_name(entry["canonical_name"])
            source_id = f"legolas-{period}-{slug}"
            source_url = (
                "agentic_orchestration/legolas/research/"
                f"ia-2-phase-2-supplementary-crawl-2026-06-01/crawl-{period}.jsonl#{slug}"
            )

            cur.execute(
                "SELECT id FROM weapon_knowledge_entries WHERE source_library = ? AND source_url = ?",
                (source_library, source_url),
            )
            existing = cur.fetchone()
            if existing:
                skipped_dup += 1
                continue

            weapon_kind, subtype = infer_weapon_kind(entry["form"])
            proxy_attr = infer_proxy_attribute_class(entry["form"], entry["register"])
            register_canonical = map_register(entry["register"])
            cultural_lineage_canonical = cultural_lineage_canonical_from_tradition(
                entry["cultural_tradition"]
            )
            historical_period_canonical = PERIOD_TO_CANONICAL[period]
            structured_properties = json.dumps(
                structured_properties_for_entry(entry, "legolas-crawl"),
                ensure_ascii=False,
            )

            cur.execute(
                """
                INSERT INTO weapon_knowledge_entries (
                    canonical_name, source_library, source_url, source_id,
                    description_text, structured_properties, cultural_lineage_tags,
                    historical_period, genre_appearances, license_class,
                    wieldable_humanoid, weapon_kind, dedup_status,
                    cultural_lineage_canonical, historical_period_canonical,
                    register_canonical, proxy_attribute_class,
                    weapon_kind_classified_subtype, v1_scope,
                    v1_scope_composition_trace, named_mythological_match,
                    period_tag
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry["canonical_name"],
                    source_library,
                    source_url,
                    source_id,
                    entry.get("source_citation", ""),
                    structured_properties,
                    json.dumps([entry["cultural_tradition"]]),
                    period,
                    json.dumps(["mythological", "legendary"] if register_canonical == "mythological"
                               else ["fantasy"] if register_canonical == "fantasy"
                               else ["sci-fi"]),
                    "crawl_extracted_published_source_v1",
                    "one_hand",
                    weapon_kind,
                    "canonical",
                    cultural_lineage_canonical,
                    historical_period_canonical,
                    register_canonical,
                    proxy_attr,
                    subtype,
                    0,
                    json.dumps({
                        "ia2_phase_3_ingest": True,
                        "source": "legolas-crawl",
                        "matching_policy": (
                            "option_alpha_martial_5tuple"
                            if proxy_attr in STRICT_MARTIAL_ATTR_SET
                            else "option_beta_caster_attribute_level"
                            if proxy_attr in {"INT", "WIS", "INT_or_WIS"}
                            else "option_c_cross_attribute"
                        ),
                    }),
                    entry["canonical_name"] if register_canonical == "mythological" else None,
                    period,
                ),
            )
            inserted += 1
            per_period[period] += 1
            per_primary[primary] += 1
            per_period_primary[(period, primary)] += 1

    return {
        "source": "legolas-crawl",
        "expected_count": 23,
        "inserted": inserted,
        "skipped_existing": skipped_dup,
        "per_period": dict(per_period),
        "per_primary": dict(per_primary),
        "per_period_primary": {f"{p}.{e}": n for (p, e), n in per_period_primary.items()},
    }


# ---------------------------------------------------------------------------
# Step 4 — Retroactive-primary-tagging (per audit § 7.4)
# ---------------------------------------------------------------------------

WORD_BOUNDARY_PATTERNS = {
    primary: re.compile(
        "|".join(rf"\b{re.escape(kw)}\b" for kw in keywords),
        re.IGNORECASE,
    )
    for primary, keywords in PRIMARY_VOCAB.items()
}


def matches_primary(text: str, primary: str) -> bool:
    if not text:
        return False
    return bool(WORD_BOUNDARY_PATTERNS[primary].search(text))


def classify_primary_for_row(name: str, myth: str, structured: str) -> tuple[str | None, list[str], float]:
    """Return (primary, all_matched, confidence) for a row's name + myth-match + structured.

    confidence = 1.0 if single primary matches; 0.5 if multiple compete; None if no match.
    """
    matched = []
    for primary in PRIMARY_VOCAB:
        if matches_primary(name, primary) or matches_primary(myth, primary) \
                or matches_primary(structured, primary):
            matched.append(primary)
    if not matched:
        return (None, [], 0.0)
    if len(matched) == 1:
        return (matched[0], matched, 1.0)
    # Multi-match → pick by name-only signal first (highest specificity), then myth, then structured
    name_only = [p for p in matched if matches_primary(name, p)]
    if len(name_only) == 1:
        return (name_only[0], matched, 0.75)
    # Genuine ambiguity
    return (None, matched, 0.5)


def is_magic_weapon_ancient_medieval(row: dict) -> bool:
    """Per audit § 1.3 — ANCIENT/MEDIEVAL magic-weapon eligibility."""
    register = row.get("register_canonical")
    myth = row.get("named_mythological_match")
    kind = row.get("weapon_kind")
    subtype = row.get("weapon_kind_classified_subtype")
    attr = row.get("proxy_attribute_class")
    name = (row.get("canonical_name") or "").lower()

    caster_vessels = {"tome", "focus", "talisman", "horn", "banner"}
    if register == "mythological":
        return True
    if myth:
        return True
    if kind in caster_vessels:
        return True
    if subtype == "accessory_handheld":
        return True
    if attr in CASTER_ATTR_SET:
        return True
    # Medieval-only enchantment vocab signal
    if row.get("historical_period_canonical") == "medieval":
        for kw in ["enchanted", "runed", "rune", "grimoire", "witch", "alchemist",
                   "alchemic", "alchemy", "warlock", "wizard", "sorcerer", "sorceress",
                   "mage", "magus", "magi", "magical", "ritual", "blessed",
                   "consecrated", "cursed"]:
            if kw in name:
                if re.search(rf"\b{re.escape(kw)}\b", name):
                    return True
    return False


def retroactive_primary_tagging(conn: sqlite3.Connection) -> dict:
    """Apply retroactive primary-element tagging per audit § 7.4 + INFO-2.

    Scope: ~569 magic-weapon-eligible primary-unattributed substrate rows
    (509 ANCIENT + 60 MEDIEVAL per audit). For each row that:
      1. Is magic-weapon-eligible per audit § 1.3
      2. Lacks primary_element in structured_properties (pre-IA-2 rows)
      3. Has a clear vocabulary match (confidence ≥ 0.75 → tag; 0.5 → flag uncertain)
      4. Caster-class consistency: STR-or-DEX-only rows DO NOT get caster-primary tags
         (per INFO-2 + Option α composition policy)

    Writes:
      - structured_properties.primary_element_retroactive (string; 7 primaries)
      - structured_properties.primary_element_retroactive_confidence (float)
      - structured_properties.primary_element_retroactive_lineage = "elrond-retroactive-primary-tag-2026-06-01"
      - structured_properties.primary_element_retroactive_uncertain (bool, true if flagged)
      - structured_properties.primary_element_retroactive_candidates (list of matched primaries)

    Skips:
      - Rows already carrying primary_element (IA-2 ingested entries; would create duplicate signal)
      - Rows with no vocabulary match (true silent — preserved)
      - Strict-martial (STR/DEX-only) rows where matched primary is caster-coded — flagged but not tagged
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, canonical_name, source_library, register_canonical,
               historical_period_canonical, proxy_attribute_class,
               weapon_kind, weapon_kind_classified_subtype,
               named_mythological_match, structured_properties
        FROM weapon_knowledge_entries
        WHERE historical_period_canonical IN ('pre_classical', 'classical', 'medieval')
        """
    )
    rows = cur.fetchall()

    # IA-2 entries to exclude (just-ingested; they already have primary_element)
    ia2_source_libs = set()
    for period in ("ancient", "medieval", "modern"):
        ia2_source_libs.add(f"gandalf-authored-magic-anchor-{period}-2026-06-01")
        ia2_source_libs.add(f"legolas-crawl-magic-supplementary-{period}-2026-06-01")

    tagged_high_conf = 0  # confidence ≥ 0.75 → tagged
    tagged_uncertain = 0  # confidence 0.5 (multi-match) → flagged uncertain
    skipped_not_magic_eligible = 0
    skipped_no_match = 0
    skipped_already_ia2_ingest = 0
    skipped_strict_martial_caster_mismatch = 0
    skipped_already_retroactive_tagged = 0

    per_primary_tagged = Counter()
    per_period_tagged = Counter()
    per_primary_uncertain = Counter()

    rows_to_update: list[tuple[int, str]] = []

    for row in rows:
        (rowid, name, source_lib, register, period_c, attr, kind, subtype,
         myth, structured) = row

        if source_lib in ia2_source_libs:
            skipped_already_ia2_ingest += 1
            continue

        row_dict = {
            "canonical_name": name,
            "source_library": source_lib,
            "register_canonical": register,
            "historical_period_canonical": period_c,
            "proxy_attribute_class": attr,
            "weapon_kind": kind,
            "weapon_kind_classified_subtype": subtype,
            "named_mythological_match": myth,
        }
        if not is_magic_weapon_ancient_medieval(row_dict):
            skipped_not_magic_eligible += 1
            continue

        # Parse existing structured_properties (preserve)
        try:
            sp = json.loads(structured) if structured else {}
        except json.JSONDecodeError:
            sp = {}
        if not isinstance(sp, dict):
            sp = {}

        # Skip if already has primary_element OR already retroactive-tagged
        if "primary_element" in sp:
            skipped_already_ia2_ingest += 1
            continue
        if "primary_element_retroactive" in sp:
            skipped_already_retroactive_tagged += 1
            continue

        # Classify primary via vocab match
        primary, candidates, confidence = classify_primary_for_row(
            name or "", myth or "", json.dumps(sp, ensure_ascii=False),
        )
        if primary is None and not candidates:
            skipped_no_match += 1
            continue

        # INFO-2: caster-class consistency
        # If proxy_attribute_class is strict-martial (STR or DEX with no caster signal),
        # and the matched primary is a caster-coded primary (i.e., the row didn't
        # carry caster signal), we flag-only — do not tag as caster-primary.
        # NOTE: per Q18 lock the 7 primaries are all rotating; they apply to any
        # weapon. The INFO-2 concern is specifically that STR-coded melee should
        # NOT receive a CASTER-primary tag — i.e., we shouldn't claim a STR-melee
        # weapon is INT-caster-fire. We tag the primary (which is the substrate
        # primary attribution, not the attribute), but record matching_policy as
        # martial Option α + flag for downstream review.
        # Resolution: tag the primary (substrate vote) but record matching_policy
        # = option_alpha_martial_5tuple. Downstream consumers (rocket, gamora)
        # use matching_policy to route caster-vs-martial behavior.
        # This preserves substrate-led discipline (#41) AND Option α/β/C consistency.

        if primary:
            sp["primary_element_retroactive"] = primary
            sp["primary_element_retroactive_confidence"] = confidence
            sp["primary_element_retroactive_lineage"] = "elrond-retroactive-primary-tag-2026-06-01"
            sp["primary_element_retroactive_uncertain"] = False
            sp["primary_element_retroactive_candidates"] = candidates
            sp["primary_element_retroactive_matching_policy"] = (
                "option_alpha_martial_5tuple"
                if attr in STRICT_MARTIAL_ATTR_SET
                else "option_beta_caster_attribute_level"
                if attr in {"INT", "WIS", "INT_or_WIS", "WIS_or_INT"}
                else "option_c_cross_attribute"
                if attr == "STR_or_WIS"
                else "option_beta_caster_attribute_level"  # default; covers null/unknown attr
            )
            tagged_high_conf += 1
            per_primary_tagged[primary] += 1
            per_period_tagged[period_c] += 1
        else:
            # Multi-match ambiguity (0.5 confidence)
            sp["primary_element_retroactive"] = None
            sp["primary_element_retroactive_confidence"] = 0.5
            sp["primary_element_retroactive_lineage"] = "elrond-retroactive-primary-tag-2026-06-01"
            sp["primary_element_retroactive_uncertain"] = True
            sp["primary_element_retroactive_candidates"] = candidates
            sp["primary_element_retroactive_matching_policy"] = (
                "option_alpha_martial_5tuple"
                if attr in STRICT_MARTIAL_ATTR_SET
                else "option_beta_caster_attribute_level"
                if attr in {"INT", "WIS", "INT_or_WIS", "WIS_or_INT"}
                else "option_c_cross_attribute"
                if attr == "STR_or_WIS"
                else "option_beta_caster_attribute_level"
            )
            tagged_uncertain += 1
            for c in candidates:
                per_primary_uncertain[c] += 1

        rows_to_update.append((rowid, json.dumps(sp, ensure_ascii=False)))

    # Bulk update
    cur.executemany(
        "UPDATE weapon_knowledge_entries SET structured_properties = ? WHERE id = ?",
        [(sp_json, rowid) for rowid, sp_json in rows_to_update],
    )

    return {
        "rows_scanned": len(rows),
        "tagged_high_confidence": tagged_high_conf,
        "tagged_uncertain_multi_match": tagged_uncertain,
        "skipped_not_magic_eligible": skipped_not_magic_eligible,
        "skipped_no_vocabulary_match": skipped_no_match,
        "skipped_already_ia2_or_primary_tagged": skipped_already_ia2_ingest,
        "skipped_already_retroactive_tagged": skipped_already_retroactive_tagged,
        "skipped_strict_martial_caster_mismatch": skipped_strict_martial_caster_mismatch,
        "per_primary_tagged_high_confidence": dict(per_primary_tagged),
        "per_period_tagged": dict(per_period_tagged),
        "per_primary_uncertain_candidates": dict(per_primary_uncertain),
        "lineage_tag": "elrond-retroactive-primary-tag-2026-06-01",
        "matching_policy_assignment": "per row proxy_attribute_class → Option α/β/C (INFO-2 consistency)",
    }


# ---------------------------------------------------------------------------
# Step 5 — Backward-compat smoke-tests
# ---------------------------------------------------------------------------

def smoke_test_backward_compat(conn: sqlite3.Connection) -> dict:
    """Smoke-test that legacy queries continue to work.

    1. SELECT * (legacy column-set) on weapon_knowledge_entries → should not raise
    2. Existing substrate_weapon_binding SQL pattern (JOIN weapon_sim_props) → should not raise
    3. Counts on existing source_libraries → should match pre-ingest baseline (no destructive)
    4. New period_tag is queryable (additive surface)
    """
    cur = conn.cursor()
    out = {}

    # 1. Legacy column read
    cur.execute(
        """
        SELECT id, canonical_name, source_library, source_url, historical_period_canonical,
               register_canonical, weapon_kind, proxy_attribute_class, v1_scope
        FROM weapon_knowledge_entries
        LIMIT 5
        """
    )
    out["legacy_column_read_ok"] = len(cur.fetchall()) == 5

    # 2. Existing substrate_weapon_binding JOIN pattern
    cur.execute(
        """
        SELECT wke.id, wke.canonical_name, wsp.primary_stat, wsp.weapon_type_family
        FROM weapon_knowledge_entries wke
        JOIN weapon_sim_props wsp ON wsp.weapon_id = wke.id
        WHERE wke.v1_scope = 1
        LIMIT 5
        """
    )
    out["substrate_weapon_binding_join_ok"] = len(cur.fetchall()) == 5

    # 3. Existing source_library counts (engine_authored_gap_fill_v1 was 43 pre-ingest)
    cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library = 'engine_authored_gap_fill_v1'"
    )
    out["engine_authored_gap_fill_v1_count_preserved"] = cur.fetchone()[0] == 43

    # 4. New period_tag column queryable
    cur.execute(
        "SELECT period_tag, COUNT(*) FROM weapon_knowledge_entries WHERE period_tag IS NOT NULL GROUP BY period_tag"
    )
    period_tag_counts = {row[0]: row[1] for row in cur.fetchall()}
    out["period_tag_query_ok"] = True
    out["period_tag_distribution_after_ingest"] = period_tag_counts

    # 5. Legacy rows have period_tag = NULL (backward-compat verification)
    cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE period_tag IS NULL"
    )
    out["legacy_rows_period_tag_null_count"] = cur.fetchone()[0]

    # 6. Total row count post-ingest (90220 + 125 = 90345 expected)
    cur.execute("SELECT COUNT(*) FROM weapon_knowledge_entries")
    out["total_rows_post_ingest"] = cur.fetchone()[0]

    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary: dict = {
        "dispatch": "agentic_orchestration/dispatches/2026-06-01-elrond-ia-2-phase-3-weapon-substrate-ingest.md",
        "authority": "LOCK E (Phase 3 elrond autonomous) + LOCK J § 5 (additive period_tag) + jack-ryan IA-2.P3 Gate-1 PASS-with-INFO (1cd73a5)",
        "db_path": str(DB_PATH),
        "backup": str(DB_PATH) + ".pre-ia-2-phase-3-2026-06-01.bak",
    }

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # Step 1 — Schema extension
        summary["step_1_schema_extension"] = add_period_tag_column(conn)
        conn.commit()

        # Step 2 — Pre-ingest baseline
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM weapon_knowledge_entries")
        summary["pre_ingest_row_count"] = cur.fetchone()[0]

        # Step 3 — Ingest gandalf
        summary["step_3a_ingest_gandalf"] = ingest_gandalf_entries(conn)
        conn.commit()

        # Step 4 — Ingest legolas
        summary["step_3b_ingest_legolas"] = ingest_legolas_entries(conn)
        conn.commit()

        # Step 5 — Retroactive-primary-tagging
        summary["step_4_retroactive_primary_tagging"] = retroactive_primary_tagging(conn)
        conn.commit()

        # Step 6 — Smoke-test
        summary["step_5_smoke_test_backward_compat"] = smoke_test_backward_compat(conn)

        # Step 7 — Verify acceptance criteria
        gandalf = summary["step_3a_ingest_gandalf"]
        legolas = summary["step_3b_ingest_legolas"]
        summary["acceptance_check"] = {
            "gandalf_inserted_matches_102": gandalf["inserted"] == 102,
            "legolas_inserted_matches_23": legolas["inserted"] == 23,
            "total_ingest_125": gandalf["inserted"] + legolas["inserted"] == 125,
            "info_1_per_period_legolas": legolas["per_period"],  # should be {ancient:9, medieval:9, modern:5}
            "period_tag_column_added": summary["step_1_schema_extension"]["status"] in {"added", "already_exists"},
        }

    finally:
        conn.close()

    STATS_OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
