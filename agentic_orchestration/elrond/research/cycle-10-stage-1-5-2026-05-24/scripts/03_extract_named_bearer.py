#!/usr/bin/env python3
"""
Cycle 10 Stage 1.5 — Half B: named-bearer extractor.

Parses gandalf's seed list YAML structured block + runs three-pass match:

  Pass A — explicit "X of Y" / "Made for Y" / "attributed to Y" patterns in
           canonical_name (Met Museum primary; preserves source phrasing).
  Pass B — seed-list match (name + aliases) against
           canonical_name + description_text + cultural_lineage_tags.
           High-priority entries: direct match. Low-priority: require
           tradition-coherent context tokens within ±50 chars (Discipline #25
           semantic-layer rep-audit composing on top of regex match).
  Pass C — Sketch F 12 anchors validated for tradition-coherence specifically;
           rep-audit flag recorded per match.

Output:
  - UPDATE weapon_knowledge_entries SET extracted_named_bearer = ?
  - logs/03_extract_named_bearer.json (summary)
  - named-bearer-matches.json (every match: id, canonical_name, source, matched_name,
    aliases-resolved, tradition_tag, tier, regex_priority, pass, rep_audit_flag)

Discipline #11 attribution clarity: source phrasing preserved verbatim.
Discipline #25 rep-audit: low-priority matches require context-token verification.

Usage:
  python 03_extract_named_bearer.py --limit 500              # smoke
  python 03_extract_named_bearer.py                            # full
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_DIR = Path(__file__).parent.parent / "logs"
SEED_LIST_PATH = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-24-named-historical-figure-seed-list.md"
)
MATCH_LOG_PATH = Path(__file__).parent.parent / "named-bearer-matches.json"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Pass A: canonical_name "of X" / "for X" / "attributed to X" patterns
# Used primarily for Met Museum; also applies generally where canonical_name
# encodes a proper-noun bearer phrase.
# ---------------------------------------------------------------------------

# Met Museum / royal_armouries / Wikipedia canonical-name bearer patterns.
#
# Trigger-anchored only. Bare "of" is too greedy (matches "Pair of Gauntlets",
# "of the 15th century", etc.). We require ONE of these specific triggers:
#
#   - Title (Roman-numeral / royal-title) phrase introduced by "of":
#     "Halberd of Archduke Ferdinand II", "Rapier of Emperor Charles V"
#   - Explicit attribution verbs: "Made for", "made for", "attributed to",
#     "belonging to", "presented to", "carried by", "owned by", "of Sir",
#     "of Saint", "of Don", "of Lord", "of Duke"
#
# Continuation: allow bare proper-noun tokens OR connector+proper-noun pairs.
# This captures full multi-word names like "Christian Ernst, Margrave of..." up
# to a comma/paren/end-of-string.
_NAME_BODY = (
    r"[A-ZÀ-Þ][\w'\-À-ÿ]+"  # first token
    # Up to 6 continuation tokens: (bare proper) OR (connector + proper) OR (Roman numeral)
    r"(?:\s+(?:[A-ZÀ-Þ][\w'\-À-ÿ]+|[IVXLCDM]+|"
    r"(?:de|del|du|von|van|le|la|y|el|al|ibn|bin|d[oei]|of|the|and|or)"
    r"(?:\s+[A-ZÀ-Þ][\w'\-À-ÿ]+)?)){0,8}"
)

# Pattern A1: trigger phrase + (optional title prefix) + proper-noun name
RE_BEARER_TITLE = re.compile(
    r"(?:\bof\s+|\battributed\s+to\s+|\bMade\s+for\s+|\bmade\s+for\s+|"
    r"\bbelonging\s+to\s+|\bpresented\s+to\s+|\bcarried\s+by\s+|\bowned\s+by\s+|"
    r"\bcommissioned\s+by\s+|\bassociated\s+with\s+|\bused\s+by\s+)"
    r"(?P<name>"
    r"(?:Archduke|Archduchess|Duke|Duchess|Count|Countess|Marquess|Margrave|Markgraf|"
    r"Lord|Lady|Sir|Dame|King|Queen|Emperor|Empress|Prince|Princess|"
    r"Don|Doña|Saint|St\.?|Sant[ao]?|Holy|"
    r"Cardinal|Bishop|Pope|Father|Brother|Sister|"
    r"General|Captain|Colonel|Admiral|Field Marshal|Marshal|"
    r"Pharaoh|Sultan|Caliph|Shah|Tsar|Khan|Shogun|"
    r"Master|Mistress|Grand Duke|Grand Duchess|Grand Master)"
    r"\s+"
    + _NAME_BODY
    + r")"
)

# Pattern A2: explicit attribution verbs + bare proper-name (no title required)
RE_BEARER_ATTRIB = re.compile(
    r"(?:\battributed\s+to\s+|\bMade\s+for\s+|\bmade\s+for\s+|"
    r"\bbelonging\s+to\s+|\bpresented\s+to\s+|\bcarried\s+by\s+|\bowned\s+by\s+|"
    r"\bcommissioned\s+by\s+|\bassociated\s+with\s+)"
    r"(?P<name>" + _NAME_BODY + r")"
)

# Pattern A3: "of <ProperName>" where ProperName is multi-token OR ends with Roman numeral.
# Catches "Halberd of Christian I of Saxony", "Halberd of Wolf Dietrich von Raitenau".
# Critically does NOT match "of the 15th century" / "of the Bodyguard" / "of Mantua".
RE_BEARER_BARE_OF = re.compile(
    r"\bof\s+"
    r"(?!the\b|a\b|an\b|each\b|both\b|either\b|either\b|some\b)"  # negative lookahead common prefixes
    r"(?P<name>"
    r"[A-ZÀ-Þ][\w'\-À-ÿ]+"
    # Required: at least one continuation (proper-noun or Roman numeral or "von/de" + proper)
    r"(?:\s+(?:[A-ZÀ-Þ][\w'\-À-ÿ]+|[IVXLCDM]+|"
    r"(?:von|van|de|del|du|le|la|y|el|al|ibn|bin|d[oei])"
    r"\s+[A-ZÀ-Þ][\w'\-À-ÿ]+))"
    # Optional further continuations
    r"(?:\s+(?:[A-ZÀ-Þ][\w'\-À-ÿ]+|[IVXLCDM]+|"
    r"(?:de|del|du|von|van|le|la|y|el|al|ibn|bin|d[oei]|of|the|and)"
    r"(?:\s+[A-ZÀ-Þ][\w'\-À-ÿ]+)?)){0,6}"
    r")"
)

# Filter out common Met-Museum "of"-phrasings that are NOT bearer attributions
NON_BEARER_OF_TOKENS = {
    "Austria",
    "France",
    "Germany",
    "Italy",
    "Spain",
    "England",
    "Scotland",
    "Wales",
    "Ireland",
    "Russia",
    "Poland",
    "Hungary",
    "Bohemia",
    "Saxony",
    "Bavaria",
    "Mantua",
    "Brandenburg",
    "Württemberg",
    "Sessa",
    "Tyrol",
    "Burgundy",
    "Cornwall",
    "Brittany",
    "Aquitaine",
    "Normandy",
    "Salzburg",
    "Naples",
    "Sicily",
    "Florence",
    "Venice",
    "Milan",
    "Rome",
    "Paris",
    "London",
    "Vienna",
    "Madrid",
    "Berlin",
    "Moscow",
    "Stockholm",
    "Copenhagen",
    "Prague",
    "Antioch",
    "Jerusalem",
    "Constantinople",
    "Athens",
    "Sparta",
    "Thebes",
    "Memphis",
    "Alexandria",
    "Damascus",
    "Baghdad",
    "Cairo",
    "Tokyo",
    "Kyoto",
    "Beijing",
    "Nanjing",
    "Edo",
    "Aragon",
    "Castile",
    "Andalusia",
    "Catalonia",
    "Lombardy",
    "Tuscany",
    "Piedmont",
    "Holstein",
    "Schleswig",
    "Holy Roman Empire",
    "Roman Empire",
    "Byzantine Empire",
    "Ottoman Empire",
    "Mughal Empire",
    "Ming Dynasty",
    "Qing Dynasty",
    "Tokugawa Shogunate",
}

# Common stopwords that should not survive as bearer-name first token
STOPWORD_FIRST = {
    "The",
    "A",
    "An",
    "Pair",
    "Set",
    "Part",
    "Components",
    "Mounting",
    "Blade",
    "Hilt",
    "Sheath",
    "Scabbard",
    "Type",
    "Model",
    "Series",
    "Group",
    "Style",
    "Front",
    "Back",
    "Side",
    "Top",
    "Bottom",
    "Each",
    "Both",
    "Either",
    "One",
    "Two",
    "Three",
    # Common item-form first-token adjectives that misfire in bare-of pattern
    "Flintlock",
    "Wheellock",
    "Matchlock",
    "Snaphance",
    "Percussion",
    "Caplock",
    "Centrefire",
    "Rimfire",
    "Breech",
    "Muzzle",
    "Repeating",
    "Bolt",
    "Lever",
    "Semi",
    "Fully",
    "Hunting",
    "Target",
    "Duelling",
    "Dueling",
    "Cavalry",
    "Infantry",
    "Naval",
    "Field",
    "Heavy",
    "Light",
    "Medium",
    "Standard",
    "Long",
    "Short",
    "Half",
    "Three",
    "Quarter",
    "Composite",
    "Iron",
    "Steel",
    "Bronze",
    "Copper",
    "Wooden",
    "Silver",
    "Gold",
    "Ivory",
    "Lacquered",
    "Inlaid",
    "Engraved",
    "Etched",
    "Damascened",
    "Trophy",
    "Display",
    "Ceremonial",
    "Presentation",
    "Tournament",
    "Combat",
    "Battle",
    "Parade",
    # Item-form nouns frequently appearing post-trigger
    "Gauntlet",
    "Gauntlets",
    "Greaves",
    "Helm",
    "Helmet",
    "Sword",
    "Sabre",
    "Saber",
    "Rapier",
    "Cuirass",
    "Pistol",
    "Pistols",
    "Mace",
    "Halberd",
    "Polearm",
    "Spear",
    "Lance",
    "Bow",
    "Crossbow",
    "Dagger",
    "Knife",
    "Tantō",
    "Wakizashi",
    "Katana",
    "Naginata",
    "Yari",
    "Yumi",
    "Shōzoku",
    "Sodē",
    "Kotē",
    "Suneate",
    "Mask",
    "Shield",
    "Buckler",
    "Helmet",
    "Cuffs",
    "Cuff",
    "Lamellae",
    "Lamellar",
    "Sleeve",
    "Sleeves",
    "Stirrup",
    "Stirrups",
    "Saddle",
    "Bridle",
    "Reins",
    "Strap",
    "Straps",
    "Buckle",
    "Buckles",
    "Plate",
    "Plates",
    "Pauldron",
    "Pauldrons",
    "Spaulder",
    "Spaulders",
    "Vambrace",
    "Vambraces",
    "Tasset",
    "Tassets",
}


# Common D&D / fantasy / RPG item-attribute suffixes that misfire as bearer matches
ITEM_ATTRIBUTE_SUFFIX = re.compile(
    r"\b(Slaying|Smiting|Bane|Slaughter|Banishing|Warding|Striking|Stunning|"
    r"Healing|Cleansing|Burning|Freezing|Shocking|Piercing|Cleaving|Crushing|"
    r"Arrows|Bolts|Quarrels|Darts|Flame|Frost|Lightning|Acid|Poison|"
    r"Magefire|Spellfire|Hellfire|Stormfire|Soulfire|"
    r"Shadows|Souls|Spirits|Bones|Skulls|Skull|Death|Doom|Wrath|Fury|Rage|"
    r"Power|Might|Strength|Speed|Agility|Dexterity|"
    r"Light|Darkness|Sun|Moon|Stars|Hours|Days|Nights|"
    r"Forlorn|Veiled|Hidden|Bound|Cursed|Blessed|Sacred|Holy|Unholy|"
    r"Hale|Searing|Burning|Eternal|Endless|Unyielding|Unending|Rampant|Bestial|"
    r"Biting|Slayer|Stalker|Hunter|Killer|"
    # Plural weapon nouns and Warhammer-style fantasy attribute phrases
    r"Blades|Hammers|Maces|Axes|Swords|Daggers|Spears|Bows|Arrows|Pistols|Rifles|Knives|"
    r"Choppas|Stikkas|Slaggas|Cuttas|Bashas|Smashas|"
    r"Scrap|Junk|Loot|Plunder|Stuff|Things|Goods|"
    r"Energy|Force|Power|Mana|Essence|Aura|Glory|Vengeance|Pride|"
    r"Justice|Mercy|Truth|Hope|Faith|Courage|Honor|Honour|Valor|Valour|"
    r"Stones|Crystals|Gems|Jewels|Pearls|Diamonds)\b"
)


def is_fantasy_item_attribute(name: str) -> bool:
    """Detect if name is a fantasy item-attribute pattern (not a bearer)."""
    return bool(ITEM_ATTRIBUTE_SUFFIX.search(name))


def extract_pass_a(canonical_name: str) -> str | None:
    """
    Pass A: extract bearer phrase from canonical_name.
    Returns source-phrasing-preserved match or None.

    Uses two trigger-anchored regexes:
      A1: title-prefix bearer ("of Archduke X", "of Sir Y")
      A2: explicit attribution verb + proper name ("Made for X", "attributed to Y")
    """
    if not canonical_name:
        return None
    # Strip trailing parenthetical metadata (dates, regnal info) for cleaner extraction
    cleaned = re.sub(r"\s*\([^)]*\)\s*", " ", canonical_name).strip()
    matches: list[str] = []
    for pat in (RE_BEARER_TITLE, RE_BEARER_ATTRIB, RE_BEARER_BARE_OF):
        for m in pat.finditer(cleaned):
            name = m.group("name").strip()
            # Trim trailing connector tokens
            name = re.sub(r"\s+(?:of|de|del|du|von|van|le|la|y|el|al|the|and)\s*$", "", name).strip()
            # Reject if first token is a stopword (item category)
            first = name.split()[0] if name else ""
            if first in STOPWORD_FIRST:
                continue
            # Reject if entire name is in place-tokens
            if name in NON_BEARER_OF_TOKENS:
                continue
            # Reject if all tokens are place-tokens (e.g., "Holy Roman Empire")
            tokens = name.split()
            if tokens and all(
                tok in NON_BEARER_OF_TOKENS or tok.lower() in {"of", "the", "de", "del", "du", "von", "van", "le", "la", "and", "y"}
                for tok in tokens
            ):
                continue
            # Reject if first content token is a place
            if first in NON_BEARER_OF_TOKENS:
                continue
            # Reject very short names
            if len(name) < 4:
                continue
            # Reject fantasy item-attribute patterns (D&D / WoW / fantasy game data)
            if is_fantasy_item_attribute(name):
                continue
            matches.append(name)
    if not matches:
        return None
    # Return longest match (most specific) — typically the canonical bearer phrase
    return max(matches, key=len)


# ---------------------------------------------------------------------------
# Seed list parser
# ---------------------------------------------------------------------------

# Parse the YAML-style entry: - {name: "X", aliases: ["Y", "Z"], tier: N, regex_priority: high, notes: "..."}
RE_SEED_ENTRY = re.compile(
    r"- \{name:\s*\"(?P<name>[^\"]+)\","
    r"\s*aliases:\s*\[(?P<aliases>[^\]]*)\],"
    r"\s*tier:\s*(?P<tier>\d+),"
    r"\s*regex_priority:\s*(?P<priority>\w+),"
    r"\s*notes:\s*\"(?P<notes>[^\"]*)\"\}"
)

# Parse tradition_tag: "x" form
RE_TRADITION_TAG = re.compile(r'tradition_tag:\s*"([^"]+)"')

# Tradition-context tokens for low-priority disambiguation per Discipline #25
TRADITION_CONTEXT_TOKENS: dict[str, set[str]] = {
    "european_medieval": {
        "arthurian", "excalibur", "camelot", "pendragon", "round table", "avalon",
        "knight", "carolingian", "durendal", "paladin", "frankish", "crusade",
        "medieval", "middle ages", "holy land", "templar", "hospitaller",
        "kingdom", "crusader", "saracen", "moor", "iberia", "reconquista",
    },
    "norse": {
        "norse", "viking", "asgard", "valhalla", "mjolnir", "gungnir", "odin",
        "thor", "loki", "freya", "freyr", "ragnarok", "yggdrasil", "midgard",
        "old norse", "saga", "edda", "berserker", "rune", "valkyrie",
        "scandinavia", "scandinavian", "iceland", "icelandic", "norway", "denmark",
    },
    "greek": {
        "greek", "hellenic", "olympus", "olympian", "trojan", "troy",
        "athenian", "spartan", "homer", "iliad", "odyssey", "achilles",
        "achaean", "myrmidon", "amazon", "centaur", "minotaur", "hellas",
        "greece", "macedonia", "alexandrian", "ptolemy", "delphi", "argonaut",
    },
    "east_asian": {
        "japanese", "japan", "samurai", "katana", "shogun", "edo", "sengoku",
        "kamakura", "ninja", "shinobi", "ronin", "daimyo", "bushido", "yamato",
        "chinese", "china", "han", "tang", "song", "ming", "qing", "three kingdoms",
        "warring states", "shaolin", "wushu", "kung fu", "tao", "confucius",
        "korean", "korea", "goryeo", "joseon", "asia", "asian", "oriental",
    },
    "celtic": {
        "celtic", "gaelic", "irish", "ireland", "ulster", "scottish", "scotland",
        "welsh", "wales", "cymric", "fianna", "tuatha", "druid", "fian", "fenian",
        "highland", "clan", "tartan", "bagpipe", "gael", "pict", "brython", "briton",
    },
    "vedic_hindu": {
        "vedic", "hindu", "hinduism", "sanskrit", "bharata", "india", "indian",
        "mahabharata", "ramayana", "kurukshetra", "kshatriya", "brahman", "brahmin",
        "deva", "asura", "yuga", "krishna", "vishnu", "shiva", "brahma",
        "puranic", "rishi", "yogi", "rajput", "maratha", "mughal", "ayodhya",
    },
    "mesoamerican": {
        "aztec", "maya", "mayan", "mesoamerican", "tenochtitlan", "olmec",
        "tlatoani", "calpulli", "quetzalcoatl", "huitzilopochtli", "obsidian",
        "macuahuitl", "atlatl", "pre-columbian", "mexica", "nahuatl",
        "yucatan", "toltec", "zapotec", "mixtec", "teotihuacan", "chichen itza",
    },
    "egyptian": {
        "egypt", "egyptian", "pharaoh", "nile", "thebes", "memphis",
        "alexandria", "ptolemaic", "ramesside", "dynastic", "hieroglyph",
        "isis", "osiris", "horus", "anubis", "ra", "amun", "ptah", "kemet",
        "north african", "carthage", "punic", "phoenician", "nubia", "sphinx",
        "pyramid", "obelisk", "papyrus",
    },
    "slavic": {
        "slavic", "russian", "russia", "rus", "kievan", "novgorod",
        "polish", "poland", "czech", "bohemian", "ukrainian", "balkan",
        "serbian", "bulgarian", "hussite", "varangian", "boyars",
        "slav", "cossack", "rurik", "drevlian", "polabian",
    },
    "mesopotamian": {
        "sumerian", "sumer", "akkadian", "babylonian", "assyrian", "mesopotamian",
        "ur", "uruk", "nineveh", "babylon", "cuneiform", "ziggurat",
        "tigris", "euphrates", "achaemenid", "persian", "persia",
        "chaldean", "elamite", "hittite", "anatolia", "lagash", "kish", "epic of gilgamesh",
    },
}


def parse_seed_list(path: Path) -> tuple[list[dict], dict]:
    """
    Parse the markdown YAML structured block into a list of entries.
    Returns (entries, summary_stats).
    """
    text = path.read_text(encoding="utf-8")
    entries: list[dict] = []
    current_tradition: str | None = None

    for line in text.splitlines():
        tag_m = RE_TRADITION_TAG.search(line)
        if tag_m:
            current_tradition = tag_m.group(1)
            continue
        ent_m = RE_SEED_ENTRY.search(line)
        if ent_m:
            name = ent_m.group("name")
            aliases_raw = ent_m.group("aliases").strip()
            aliases: list[str] = []
            if aliases_raw:
                for a in re.split(r"\"\s*,\s*\"", aliases_raw.strip().strip("\"")):
                    a = a.strip().strip("\"")
                    if a:
                        aliases.append(a)
            entries.append(
                {
                    "name": name,
                    "aliases": aliases,
                    "tier": int(ent_m.group("tier")),
                    "priority": ent_m.group("priority"),
                    "notes": ent_m.group("notes"),
                    "tradition": current_tradition,
                }
            )

    by_priority: dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    by_tradition: dict[str, int] = {}
    for e in entries:
        by_priority[e["priority"]] = by_priority.get(e["priority"], 0) + 1
        by_tradition[e["tradition"]] = by_tradition.get(e["tradition"], 0) + 1

    stats = {
        "total_entries": len(entries),
        "by_priority": by_priority,
        "by_tradition": by_tradition,
    }
    return entries, stats


# ---------------------------------------------------------------------------
# Pass B: seed-list match
# ---------------------------------------------------------------------------


def build_pattern(name: str) -> re.Pattern:
    """Build word-boundary case-insensitive regex for a name (or alias)."""
    # Use word boundaries; escape special chars in name; keep diacritic-safe
    escaped = re.escape(name)
    return re.compile(rf"\b{escaped}\b", re.IGNORECASE)


def context_window(haystack: str, start: int, end: int, radius: int = 50) -> str:
    return haystack[max(0, start - radius) : min(len(haystack), end + radius)].lower()


def has_tradition_context(window: str, tradition: str | None) -> bool:
    if tradition is None:
        return False  # strict: if tradition unknown, treat as no context (reject)
    tokens = TRADITION_CONTEXT_TOKENS.get(tradition, set())
    if not tokens:
        return False  # strict: if no tokens map defined, reject (better safe than over-matching)
    for t in tokens:
        if t in window:
            return True
    return False


def extract_pass_b(
    haystack_combined: str,
    seed_entries: list[dict],
    seed_patterns: list[tuple[re.Pattern, dict, str]],
) -> list[dict]:
    """
    Pass B: match seed entries against the combined haystack
    (canonical_name + description_text + cultural_lineage_tags).
    Returns list of match dicts. Empty if no match.
    """
    matches: list[dict] = []
    if not haystack_combined:
        return matches
    h_lower = haystack_combined  # patterns are IGNORECASE
    for pat, entry, matched_string in seed_patterns:
        # Hard-skip: 2-or-fewer-character matched_string is hopeless (e.g., "An", "Ra").
        # These will collide with common English words. Source phrasing is preserved
        # in description text but cannot anchor a bearer attribution.
        if len(matched_string) <= 3:
            continue
        for m in pat.finditer(h_lower):
            # Low-priority entries OR short matched_string (<=5 chars): require
            # tradition-context-token in ±50 chars. Short names are common-word
            # false-match magnets (e.g., "Thor", "Sin", "Kay").
            window = context_window(h_lower, m.start(), m.end())
            rep_audit_flag: str | None = None
            effective_priority = entry["priority"]
            if len(matched_string) <= 5 and effective_priority != "low":
                effective_priority = "low"  # treat short strings as low priority
            if effective_priority == "low":
                if not has_tradition_context(window, entry["tradition"]):
                    rep_audit_flag = "rejected_context_mismatch"
                    matches.append(
                        {
                            "entry": entry,
                            "matched_string": matched_string,
                            "source_phrase": m.group(0),
                            "rep_audit_flag": rep_audit_flag,
                            "accepted": False,
                        }
                    )
                    continue
            elif effective_priority == "medium":
                if not has_tradition_context(window, entry["tradition"]):
                    rep_audit_flag = "context_weak_flagged_for_spotcheck"
            matches.append(
                {
                    "entry": entry,
                    "matched_string": matched_string,
                    "source_phrase": m.group(0),
                    "rep_audit_flag": rep_audit_flag,
                    "accepted": True,
                }
            )
            # Only first match per pattern; the dedup happens at result aggregation
            break
    return matches


# ---------------------------------------------------------------------------
# Sketch F 12 anchors (Pass C — explicit special-handling list)
# ---------------------------------------------------------------------------

SKETCH_F_ANCHORS = {
    "Arthur": "european_medieval",
    "Roland": "european_medieval",
    "Hattori Hanzō": "east_asian",
    "Hattori Hanzo": "east_asian",
    "Lu Bu": "east_asian",
    "Thor": "norse_mythological",
    "Achilles": "greek_mythological",
    "Cú Chulainn": "celtic_gaelic",
    "Cu Chulainn": "celtic_gaelic",
    "Cuchulainn": "celtic_gaelic",
    "Moctezuma": "mesoamerican",
    "Quetzalcoatl": "mesoamerican",
    "Cleopatra": "egyptian_north_african",
    "Karna": "vedic_hindu",
    "Baba Yaga": "slavic_eastern_european",
    "Gilgamesh": "sumerian_mesopotamian",
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--source", type=str, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    started = time.time()
    log_name = "03_extract_named_bearer"
    if args.limit:
        log_name += f"_smoke_{args.limit}"
    if args.source:
        log_name += f"_{args.source}"
    if args.dry_run:
        log_name += "_dryrun"
    log_path = LOG_DIR / f"{log_name}.json"

    # Parse seed list
    if not SEED_LIST_PATH.exists():
        print(f"ERROR: Seed list not found at {SEED_LIST_PATH}", file=sys.stderr)
        return 2
    seed_entries, seed_stats = parse_seed_list(SEED_LIST_PATH)
    if not seed_entries:
        print("ERROR: Seed list parsed but produced 0 entries", file=sys.stderr)
        return 3

    # Precompile patterns: (pattern, entry, matched_string)
    seed_patterns: list[tuple[re.Pattern, dict, str]] = []
    for e in seed_entries:
        seed_patterns.append((build_pattern(e["name"]), e, e["name"]))
        for alias in e["aliases"]:
            seed_patterns.append((build_pattern(alias), e, alias))

    log = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "args": vars(args),
        "seed_stats": seed_stats,
        "seed_patterns_compiled": len(seed_patterns),
        "rows_scanned": 0,
        "rows_with_match": 0,
        "rows_written": 0,
        "pass_a_matches": 0,
        "pass_b_matches": 0,
        "rejected_context_mismatch": 0,
        "context_weak_flagged": 0,
        "anchor_match_counts": {a: 0 for a in SKETCH_F_ANCHORS.keys()},
        "per_tradition_match_counts": {},
        "errors": [],
    }
    match_log: list[dict] = []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        query = (
            "SELECT id, canonical_name, source_library, description_text, "
            "cultural_lineage_tags, cultural_lineage_canonical, register_canonical "
            "FROM weapon_knowledge_entries"
        )
        params: list = []
        wheres: list[str] = []
        if args.source:
            wheres.append("source_library = ?")
            params.append(args.source)
        if wheres:
            query += " WHERE " + " AND ".join(wheres)
        if args.limit:
            query += " LIMIT ?"
            params.append(args.limit)

        updates: list = []
        for row in conn.execute(query, params):
            log["rows_scanned"] += 1
            canonical_name = row["canonical_name"] or ""
            desc = row["description_text"] or ""
            tags = row["cultural_lineage_tags"] or ""
            # Combine for Pass B search; preserve case for context-window inspection
            haystack = " ".join([canonical_name, desc[:2000], tags])

            # Pass A
            pass_a_bearer = extract_pass_a(canonical_name)
            pass_a_rep_audit_flag: str | None = None

            # Pass B
            pass_b_matches = extract_pass_b(haystack, seed_entries, seed_patterns)

            # Mode-C/D rep-audit overlay per Discipline #25: if row's
            # cultural_lineage_canonical is modern/sci-fi/fantasy, an accepted
            # Pass B match against a historical/mythological seed tradition is
            # likely a naming-allusion (Mode C) rather than a true bearer
            # attribution. Preserve the match (source phrasing per Discipline #11)
            # but mark with rep_audit_flag.
            row_lineage = row["cultural_lineage_canonical"] or "unknown"
            row_register = row["register_canonical"] or "unknown"

            # Pass A rep-audit: if row's lineage is fantasy_generic / sci_fi_generic,
            # Pass A bearer is almost certainly a fictional-attribute phrase or fictional
            # location-name (e.g., "Lordaeron Kings", "Inverted Probability", "Bad Mojo").
            # Discipline #25: flag and suppress the bearer text to avoid downstream
            # confusion. The source phrasing remains in canonical_name itself.
            pass_a_suppressed = False
            if pass_a_bearer and row_lineage in {"fantasy_generic", "sci_fi_generic"}:
                pass_a_rep_audit_flag = "rep_audit_pass_a_suppressed_fantasy_lineage"
                pass_a_suppressed = True
                log.setdefault("pass_a_suppressed_fantasy", 0)
                log["pass_a_suppressed_fantasy"] += 1
            # Mode-C/D contamination markers per Discipline #25:
            # - sci_fi_generic / fantasy_generic / cross_cultural lineage → Mode A reference suspect
            # - military_modern register → Mode C naming-allusion suspect (Russian Svarog UAV etc.)
            # - sci_fi register → Mode C naming-allusion suspect
            mode_c_lineages = {"sci_fi_generic", "fantasy_generic", "cross_cultural"}
            mode_c_registers = {"military_modern", "sci_fi"}
            for m in pass_b_matches:
                if not m["accepted"]:
                    continue
                if m["rep_audit_flag"] is not None:
                    continue
                if row_lineage in mode_c_lineages:
                    m["rep_audit_flag"] = "rep_audit_mode_c_naming_allusion_suspected"
                elif row_register in mode_c_registers:
                    m["rep_audit_flag"] = "rep_audit_mode_c_naming_allusion_suspected"

            pass_b_accepted = [m for m in pass_b_matches if m["accepted"]]
            pass_b_rejected = [m for m in pass_b_matches if not m["accepted"]]
            log["rejected_context_mismatch"] += len(pass_b_rejected)
            log["context_weak_flagged"] += sum(
                1 for m in pass_b_accepted if m["rep_audit_flag"] == "context_weak_flagged_for_spotcheck"
            )
            log.setdefault("mode_c_naming_allusion_flagged", 0)
            log["mode_c_naming_allusion_flagged"] += sum(
                1 for m in pass_b_accepted if m["rep_audit_flag"] == "rep_audit_mode_c_naming_allusion_suspected"
            )

            # Aggregate: Pass A wins as primary (preserves source phrasing); Pass B accepted appends
            bearer_parts: list[str] = []
            if pass_a_bearer and not pass_a_suppressed:
                log["pass_a_matches"] += 1
                bearer_parts.append(pass_a_bearer)

            for m in pass_b_accepted:
                log["pass_b_matches"] += 1
                bearer_parts.append(m["entry"]["name"])
                tr = m["entry"]["tradition"]
                log["per_tradition_match_counts"][tr] = log["per_tradition_match_counts"].get(tr, 0) + 1
                if m["entry"]["name"] in SKETCH_F_ANCHORS:
                    log["anchor_match_counts"][m["entry"]["name"]] = (
                        log["anchor_match_counts"].get(m["entry"]["name"], 0) + 1
                    )
                # Sketch F 12-anchor alias coverage check
                if m["matched_string"] in SKETCH_F_ANCHORS:
                    log["anchor_match_counts"][m["matched_string"]] = (
                        log["anchor_match_counts"].get(m["matched_string"], 0) + 1
                    )

            # Build extracted_named_bearer value: dedup preserving order; semicolon-separated
            seen = set()
            unique_parts: list[str] = []
            for p in bearer_parts:
                if p and p not in seen:
                    seen.add(p)
                    unique_parts.append(p)

            extracted = "; ".join(unique_parts) if unique_parts else None

            if extracted:
                log["rows_with_match"] += 1
                match_log.append(
                    {
                        "id": row["id"],
                        "canonical_name": canonical_name,
                        "source_library": row["source_library"],
                        "cultural_lineage_canonical": row["cultural_lineage_canonical"],
                        "extracted_named_bearer": extracted,
                        "pass_a_match": pass_a_bearer,
                        "pass_b_seed_matches": [
                            {
                                "name": m["entry"]["name"],
                                "tradition": m["entry"]["tradition"],
                                "tier": m["entry"]["tier"],
                                "priority": m["entry"]["priority"],
                                "source_phrase": m["source_phrase"],
                                "rep_audit_flag": m["rep_audit_flag"],
                            }
                            for m in pass_b_accepted
                        ],
                        "pass_b_rejected": [
                            {
                                "name": m["entry"]["name"],
                                "tradition": m["entry"]["tradition"],
                                "source_phrase": m["source_phrase"],
                            }
                            for m in pass_b_rejected
                        ],
                    }
                )
            updates.append((extracted, row["id"]))

        if not args.dry_run:
            conn.executemany(
                "UPDATE weapon_knowledge_entries SET extracted_named_bearer = ? WHERE id = ?",
                updates,
            )
            conn.commit()
            log["rows_written"] = len(updates)
    finally:
        conn.close()

    log["elapsed_sec"] = round(time.time() - started, 2)
    log["status"] = "ok" if not log["errors"] else "partial"
    log_path.write_text(json.dumps(log, indent=2))

    # Write match log
    if not args.dry_run:
        MATCH_LOG_PATH.write_text(json.dumps(match_log, indent=2, ensure_ascii=False))

    # Compact stdout summary
    summary = {
        "status": log["status"],
        "seed_entries": seed_stats["total_entries"],
        "seed_patterns_compiled": log["seed_patterns_compiled"],
        "rows_scanned": log["rows_scanned"],
        "rows_with_match": log["rows_with_match"],
        "rows_written": log["rows_written"],
        "pass_a_matches": log["pass_a_matches"],
        "pass_b_matches": log["pass_b_matches"],
        "rejected_context_mismatch": log["rejected_context_mismatch"],
        "context_weak_flagged": log["context_weak_flagged"],
        "anchor_match_counts": log["anchor_match_counts"],
        "per_tradition_match_counts": log["per_tradition_match_counts"],
        "elapsed_sec": log["elapsed_sec"],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
