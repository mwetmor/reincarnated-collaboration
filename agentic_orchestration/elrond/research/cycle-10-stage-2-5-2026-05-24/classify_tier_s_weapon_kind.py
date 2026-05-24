#!/usr/bin/env python3
"""
Tier-S Weapon-Kind Classification — Cycle 10 Stage 2.5 Refutation-Routing

Classifies all 1,126 Tier-S rows by category (handheld_weapon / accessory / armor /
ammo_consumable / siege_vehicle / art_object / other) using:

1. Source-specific structured signals (most diagnostic):
   - met-museum: structured_properties.classification
   - royal_armouries: structured_properties.category_value + object_type
   - wikipedia: structured_properties.type
   - odin-army-tradoc: structured_properties.properties."System.Type"
   - wikidata: structured_properties.weapon_type
2. Canonical-name token-match fallback (vocabulary per dispatch § Heuristic first pass)
3. wieldable_humanoid as corroborating signal

Per dispatch (Discipline #11 attribution clarity): each row's classification records
the method that fired (source_struct / name_token / wieldable_fallback / unclassified).

NO LLM-judge needed: 100% of rows classified via heuristic — keeping cost at $0.00 per
ADR-006. (LLM-judge reserved for ambiguous tie-breakers; ran zero-cost here.)
"""

import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
OUT_DIR = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/research/cycle-10-stage-2-5-2026-05-24")

# Category constants
CAT_HANDHELD = "handheld_weapon"
CAT_ACCESSORY = "accessory"
CAT_ARMOR = "armor"
CAT_AMMO = "ammo_consumable"
CAT_SIEGE = "siege_vehicle"
CAT_ART = "art_object"
CAT_OTHER = "other"

# ---------------------------------------------------------------------------
# Source-specific structured-signal classifiers
# ---------------------------------------------------------------------------

def classify_met_museum(structured: dict) -> tuple[str, str] | None:
    """Met Museum classification field is highly diagnostic.

    Returns (category, reason) or None if unclassifiable.
    """
    classif = (structured or {}).get("classification", "") or ""
    classif_lower = classif.lower()

    # Direct armor matches (substring; "armor" appears in many variants)
    if "armor" in classif_lower or "mail" == classif_lower or classif_lower == "helmets parts":
        return CAT_ARMOR, f"met:classification={classif}"
    if classif_lower in {"helmets", "shields"}:
        return CAT_ARMOR, f"met:classification={classif}"

    # Sword Furniture & related = accessory (menuki/tsuba/etc.)
    if classif_lower.startswith("sword furniture"):
        return CAT_ACCESSORY, f"met:classification={classif}"
    if classif_lower.startswith("equestrian equipment"):
        return CAT_ACCESSORY, f"met:classification={classif}"
    if classif_lower.startswith("firearms accessories"):
        return CAT_ACCESSORY, f"met:classification={classif}"
    if classif_lower.startswith("miscellaneous-buckles"):
        return CAT_ACCESSORY, f"met:classification={classif}"
    if classif_lower == "banners":
        return CAT_ACCESSORY, f"met:classification={classif}"
    if classif_lower == "costumes":
        return CAT_ACCESSORY, f"met:classification={classif}"
    if classif_lower == "archery equipment-archer's ring":
        return CAT_ACCESSORY, f"met:classification={classif}"

    # Handheld weapons
    if classif_lower in {"swords", "daggers"} or classif_lower.startswith("swords-"):
        return CAT_HANDHELD, f"met:classification={classif}"
    if classif_lower == "shafted weapons":
        return CAT_HANDHELD, f"met:classification={classif}"
    if classif_lower.startswith("firearms") and "accessories" not in classif_lower:
        return CAT_HANDHELD, f"met:classification={classif}"
    if classif_lower == "archery equipment":
        return CAT_HANDHELD, f"met:classification={classif}"
    if classif_lower == "archery equipment-crossbows":
        return CAT_HANDHELD, f"met:classification={classif}"

    # Art / non-weapon
    if classif_lower.startswith("works on paper") or classif_lower in {"paintings", "portraits", "sculpture"}:
        return CAT_ART, f"met:classification={classif}"
    if classif_lower.startswith("miscellaneous-stained glass") or classif_lower.startswith("miscellaneous-paintings"):
        return CAT_ART, f"met:classification={classif}"
    if classif_lower.startswith("books"):
        return CAT_ART, f"met:classification={classif}"
    if classif_lower == "miscellaneous-coins and medals":
        return CAT_OTHER, f"met:classification={classif}"
    if classif_lower == "tools":
        return CAT_OTHER, f"met:classification={classif}"

    # Fall through for "Miscellaneous" alone — need name-token
    return None


def classify_royal_armouries(structured: dict, name: str = "") -> tuple[str, str] | None:
    """Royal Armouries category_value + object_type.

    category_value is the most concise; object_type is JSON array fallback.
    For "& related objects" categories, we apply name-token overrides since RA
    bundles accessories with weapons under the same category_value.
    """
    sp = structured or {}
    cv = (sp.get("category_value") or "").lower()
    ot_raw = sp.get("object_type") or []
    if isinstance(ot_raw, str):
        try:
            ot_raw = json.loads(ot_raw)
        except (json.JSONDecodeError, TypeError):
            ot_raw = [ot_raw]
    ot = [o.lower() for o in ot_raw if isinstance(o, str)]
    nl = name.lower()

    # Name-token overrides — RA bundles accessories under "related objects"
    if cv == "firearms & related objects":
        # Powder flask / horn / shot pouch / cartridge box / sling / bandolier => accessory
        for tok in ["powder flask", "powder horn", "shot pouch", "shot belt",
                    "cartridge box", "bandolier", "sling", "ramrod",
                    "wad-puller", "wad puller", "ball-drawer", "ball drawer",
                    "ball mould", "bullet mould", "priming flask", "primer"]:
            if tok in nl:
                return CAT_ACCESSORY, f"ra:cv={cv}+name:{tok}"
        # Cartridge / shot (ammo) => ammo
        for tok in ["cartridge ", "shot ", "shell ", "musket ball"]:
            if tok in nl:
                return CAT_AMMO, f"ra:cv={cv}+name:{tok}"
        return CAT_HANDHELD, f"ra:cv={cv}"
    if cv == "archery & related objects":
        for tok in ["arrow", "bolt-", "bolts", "quiver"]:
            if tok in nl:
                if tok == "arrow":
                    return CAT_AMMO, f"ra:cv={cv}+name:arrow"
                if tok == "quiver":
                    return CAT_ACCESSORY, f"ra:cv={cv}+name:quiver"
        return CAT_HANDHELD, f"ra:cv={cv}"

    # Handheld weapons
    if cv == "swords":
        # Override "scabbard" alone (rare) or "sheath" only
        if nl in {"scabbard", "sheath"} or nl.startswith("sword scabbard") or nl.startswith("sheath ") or nl == "sheath":
            return CAT_ACCESSORY, f"ra:cv={cv}+name:{nl[:40]}"
        return CAT_HANDHELD, f"ra:cv={cv}"
    if cv == "staff weapons":
        return CAT_HANDHELD, f"ra:cv={cv}"
    if cv == "daggers & knives":
        return CAT_HANDHELD, f"ra:cv={cv}"
    if cv == "bayonets":
        if "sheath" in nl or "scabbard" in nl or "frog" in nl:
            return CAT_ACCESSORY, f"ra:cv={cv}+name"
        return CAT_HANDHELD, f"ra:cv={cv}"
    if cv == "clubs, maces, axes, and truncheons":
        return CAT_HANDHELD, f"ra:cv={cv}"
    if cv == "combination weapons":
        return CAT_HANDHELD, f"ra:cv={cv}"

    # Armor
    if cv == "complete armours":
        return CAT_ARMOR, f"ra:cv={cv}"
    if cv == "helmets":
        return CAT_ARMOR, f"ra:cv={cv}"
    if cv == "armour pieces":
        return CAT_ARMOR, f"ra:cv={cv}"
    if cv == "shields":
        return CAT_ARMOR, f"ra:cv={cv}"
    if cv == "animal armour & equestrian equipment":
        return CAT_ACCESSORY, f"ra:cv={cv}"  # horse barding + spurs etc.

    # Siege / artillery
    if cv == "artillery & related objects":
        return CAT_SIEGE, f"ra:cv={cv}"

    # Art / misc non-weapon
    if cv == "art":
        return CAT_ART, f"ra:cv={cv}"
    if cv == "tower of london memorabilia":
        return CAT_OTHER, f"ra:cv={cv}"
    if cv == "relics & miscellaneous":
        return CAT_OTHER, f"ra:cv={cv}"  # may need name-token override
    if cv == "fakes & reproductions":
        return CAT_OTHER, f"ra:cv={cv}"
    if cv == "loans in":
        return CAT_OTHER, f"ra:cv={cv}"
    if cv == "militaria":
        return CAT_ACCESSORY, f"ra:cv={cv}"
    if cv == "miscellaneous":
        return None  # fall through to name-token

    return None


def classify_wikipedia(structured: dict) -> tuple[str, str] | None:
    """Wikipedia infobox 'type' field. Often noisy with HTML-comment leftovers."""
    sp = structured or {}
    t = (sp.get("type") or "").lower()
    # Strip HTML comments and template noise
    t = re.sub(r"<!--.*?-->", "", t, flags=re.DOTALL).strip()
    t = re.sub(r"<[^>]+>", " ", t)  # strip HTML tags
    t = t.replace("\n", " ").replace("  ", " ").strip()

    if not t:
        return None

    # Siege/vehicle/missile (very common in wikipedia Tier-S)
    siege_tokens = [
        "missile", "rocket", "torpedo", "bomb", "nuclear weapon", "warhead",
        "tank", "armored car", "armoured car", "armored recovery", "armoured recovery",
        "field gun", "naval gun", "railway gun", "howitzer", "anti-aircraft gun",
        "anti-tank gun", "self-propelled", "ballistic", "cruise missile",
        "unmanned", "uav", "ugv", "drone", "battle tank", "armored vehicle", "armoured vehicle",
        "personnel carrier", "transport aircraft", "helicopter", "aircraft",
        "anti-ballistic", "anti-aircraft", "artillery", "mortar",
        "rocket propelled grenade", "rocket launcher", "machine gun system",
        "robot", "vehicle", "sub-orbital", "thermobaric",
        # Common military abbreviations
        "slbm", "icbm", "mrbm", "irbm", "srbm", "abm", "sam ",
        "atgm", "manpads", "mlrs",
        "truck", "tractor", "cruiser", "frigate", "destroyer", "submarine",
        "cargo ship", "patrol vessel", "icebreaker",
    ]
    for tok in siege_tokens:
        if tok in t:
            return CAT_SIEGE, f"wp:type={t[:60]} (tok={tok})"

    # Handheld firearms
    handheld_tokens = [
        "rifle", "pistol", "revolver", "carbine", "shotgun", "musket",
        "submachine gun", "machine pistol", "machine gun", "light machine gun",
        "battle rifle", "assault rifle", "sniper rifle", "anti-materiel rifle",
        "blunderbuss", "flintlock", "matchlock", "wheellock",
    ]
    for tok in handheld_tokens:
        if tok in t:
            # But "machine gun system" / "rocket launcher" was caught above
            return CAT_HANDHELD, f"wp:type={t[:60]} (tok={tok})"

    # Handheld blades/polearms
    blade_tokens = [
        "sword", "saber", "sabre", "rapier", "katana", "scimitar", "cutlass",
        "knife", "dagger", "stiletto", "dirk",
        "axe", "mace", "club", "hammer", "flail", "morningstar",
        "spear", "lance", "halberd", "polearm", "glaive", "naginata",
        "bow", "crossbow", "longbow", "shortbow", "arquebus",
    ]
    for tok in blade_tokens:
        if tok in t:
            return CAT_HANDHELD, f"wp:type={t[:60]} (tok={tok})"

    # Ammo
    if any(tok in t for tok in ["cartridge", "round", "ammunition", "shell ", "bullet", "shot"]):
        return CAT_AMMO, f"wp:type={t[:60]}"

    # Armor
    if any(tok in t for tok in ["helmet", "armor", "armour", "shield", "mail", "cuirass"]):
        return CAT_ARMOR, f"wp:type={t[:60]}"

    return None


def classify_odin_army_tradoc(structured: dict) -> tuple[str, str] | None:
    """Odin Army TRADOC properties.System.Type. Almost universally siege/vehicle/system."""
    sp = structured or {}
    props = sp.get("properties") or {}
    t = (props.get("System.Type") or props.get("System.Type ") or "").strip().lower()
    if not t:
        # Fall through
        return None

    # Handheld classes
    handheld_phrases = [
        "assault rifle", "battle rifle", "sniper rifle", "sniper weapon system",
        "shotgun", "submachine gun", "machine pistol", "pistol", "revolver",
        "light machine gun", "machine gun", "general purpose machine gun",
        "carbine", "designated marksman rifle",
        "anti-materiel rifle", "anti-material rifle",
    ]
    for p in handheld_phrases:
        if p in t:
            # Filter "machine gun system" tank-mounted from handheld; usually appears as just "Machine Gun" / "Light Machine Gun"
            return CAT_HANDHELD, f"odin:type={t[:60]}"

    # Everything else odin is siege/vehicle (UAV/UGV/howitzer/missile/etc.)
    siege_phrases = [
        "unmanned aerial vehicle", "uav", "unmanned ground vehicle", "ugv",
        "unmanned underwater vehicle", "uuv", "unmanned surface vessel",
        "howitzer", "mortar", "missile", "rocket", "artillery",
        "anti-aircraft gun", "anti-tank gun", "anti-aircraft", "anti-tank",
        "self-propelled", "tank", "ifv", "apc", "personnel carrier",
        "armored", "armoured", "ballistic", "cruise missile",
        "transport aircraft", "helicopter", "fixed-wing", "rotary",
        "tactical vehicle", "truck", "military vehicle",
        "manpads", "remotely operated", "rov",
        "rocket propelled grenade launcher", "rocket launcher",
        "rocket artillery", "gun-howitzer", "towed gun", "field gun",
        "torpedo", "bomb", "warhead", "naval gun",
    ]
    for p in siege_phrases:
        if p in t:
            return CAT_SIEGE, f"odin:type={t[:60]}"

    return None


def classify_wikidata(structured: dict) -> tuple[str, str] | None:
    """Wikidata weapon_type is sparse but trustworthy."""
    sp = structured or {}
    wt = (sp.get("weapon_type") or "").lower()
    if not wt:
        return None
    if wt == "shield":
        return CAT_ARMOR, "wd:weapon_type=shield"
    if wt in {"sword", "dagger", "knife", "axe", "spear", "polearm", "bow", "crossbow",
              "mace", "club", "hammer", "halberd", "pistol", "rifle", "musket", "katana"}:
        return CAT_HANDHELD, f"wd:weapon_type={wt}"
    return None


# ---------------------------------------------------------------------------
# Canonical-name token-match fallback (per dispatch § Heuristic first pass)
# ---------------------------------------------------------------------------

# Token sets — substring match, lowercased
ACCESSORY_TOKENS = {
    "scabbard", "sheath", "fitting", "ornament", "menuki", "tsuba", "kashira",
    "fuchi", "kojiri", "kozuka", "saya", "powder flask", "powder horn",
    "cartridge box", "bandolier", "banner", "standard", "pennant",
    "spurs", "spur", "buckle", "hanger", "suspension hanger", "frog",
    "ramrod", "wad-puller", "ball drawer", "ball-drawer", "ball mould",
    "bullet mould", "flask", "shot pouch", "shot belt", "sling", "harness fittings",
    "horse trappings", "horse-trapping", "stirrup", "saddle",
    "archer's ring", "thumb-ring", "thumb ring",
    "menuki", "ornamental", "ornaments",
    "wooden head", "wooden block", "head, wooden",
    "decorative",
}

ARMOR_TOKENS = {
    "helmet", "helm", "morion", "sallet", "burgonet", "cuirass", "breastplate",
    "backplate", "gorget", "pauldron", "vambrace", "gauntlet", "greave", "cuisse",
    "tasset", "codpiece", "crinet", "chamfron", "shaffron", "barding",
    "harquebusier's armour", "harquebusier's armor", "harquebusier's breastplate",
    "harquebusier's backplate",
    "pikeman's armour", "pikeman's armor", "pikeman's left tasset",
    "armour", "armor", "mail", "chainmail", "plate armor", "plate armour",
    "shield", "visor", "tournament shield",
    "archer's sleeve", "archer's sleeves", "archers' sleeves",
    "shoe",  # armor shoe / sabaton
    "sabaton", "solleret", "spaulder", "rerebrace", "couter",
    "left vambrace", "right vambrace", "left gauntlet", "right gauntlet",
    "left tasset", "right tasset", "left greave", "right greave",
    "kneecop", "polder",
}

AMMO_TOKENS = {
    "arrow", "bolt", "bullet", "cartridge", "ball", "shot",
    "powder", "fuze", "fuse", "primer", "musket ball",
    "shell ", "grenade", "smoke grenade",
    "pinfire", "rimfire cartridge", "centerfire cartridge",
}

SIEGE_TOKENS = {
    "cannon", "mortar", "howitzer", "ballista", "trebuchet", "catapult",
    "tank", "missile", "rocket", "torpedo", "drone", "uav", "ugv",
    "anti-aircraft", "anti-tank", "armored car", "armoured car",
    "vehicle", "self-propelled", "field gun", "naval gun", "machine gun",
    "rocket launcher", "missile launcher", "grenade launcher",
    "ballistic", "cruise missile", "warhead", "shahed",
    "personnel carrier", "transport aircraft", "helicopter", "aircraft",
    "anti-ballistic", "anti-materiel",
}

HANDHELD_TOKENS = {
    "sword", "saber", "sabre", "rapier", "katana", "scimitar", "cutlass",
    "broadsword", "longsword", "shortsword", "claymore", "wakizashi", "tanto",
    "knife", "dagger", "stiletto", "dirk", "kris", "kukri",
    "axe", "hatchet", "tomahawk", "halberd", "battle-axe",
    "mace", "club", "hammer", "flail", "morningstar",
    "spear", "lance", "pike", "polearm", "glaive", "naginata", "yari",
    "bow", "crossbow", "longbow", "shortbow",
    "rifle", "pistol", "revolver", "carbine", "shotgun", "musket",
    "blunderbuss", "flintlock", "matchlock", "wheellock", "harquebus", "arquebus",
    "machine pistol", "submachine",
    "spontoon", "guisarme", "voulge", "bardiche", "bill", "war-hammer",
    "talwar", "tulwar",
}

ART_TOKENS = {
    "stained glass", "panel of", "tapestry", "painting", "print", "drawing",
    "manuscript", "engraving", "etching", "lithograph",
    "ship model", "model of",
    "portrait", "sculpture", "statue",
    "medal", "coin",
    "book", "manuscript",
}


def token_match(name: str, tokens: set) -> str | None:
    """Return first matching token, or None."""
    nl = name.lower()
    # Sort longer tokens first for specificity
    for tok in sorted(tokens, key=len, reverse=True):
        if tok in nl:
            return tok
    return None


def classify_by_name(name: str) -> tuple[str, str] | None:
    """Order matters: more specific token-sets first.

    Sword Furniture accessory tokens (menuki/tsuba) must beat 'sword' handheld token.
    """
    # Order: ammo > accessory > armor > siege > art > handheld
    # (Specific subparts/decorations before general weapon-named items.)
    accessory_tok = token_match(name, ACCESSORY_TOKENS)
    if accessory_tok:
        return CAT_ACCESSORY, f"name:tok={accessory_tok}"
    armor_tok = token_match(name, ARMOR_TOKENS)
    if armor_tok:
        return CAT_ARMOR, f"name:tok={armor_tok}"
    ammo_tok = token_match(name, AMMO_TOKENS)
    if ammo_tok:
        return CAT_AMMO, f"name:tok={ammo_tok}"
    siege_tok = token_match(name, SIEGE_TOKENS)
    if siege_tok:
        return CAT_SIEGE, f"name:tok={siege_tok}"
    art_tok = token_match(name, ART_TOKENS)
    if art_tok:
        return CAT_ART, f"name:tok={art_tok}"
    handheld_tok = token_match(name, HANDHELD_TOKENS)
    if handheld_tok:
        return CAT_HANDHELD, f"name:tok={handheld_tok}"
    return None


def classify_by_wieldable(wieldable: str, source: str = "") -> tuple[str, str] | None:
    """Last-resort: wieldable_humanoid as corroborating signal.

    NOTE: only trust wieldable for sources where named-legendary-weapons dominate
    (wikidata + game-data-dump). For wikipedia and odin-army-tradoc, `two_hand`
    is frequently spurious-defaulted on missiles/vehicles/etc.
    """
    trusted_sources = {
        "wikidata", "nick-aschenbach-dnd-data", "osrsbox-db", "bsdata-warhammer-aos",
        "fextralife-ds1", "fextralife-ds2", "fextralife-ds3",
        "fextralife-elden-ring", "elden-ring-erdb",
        "pf2ools-pf2ools-data-quarantined", "5e-bits-5e-database",
        "5e-bits-5e-database-2024", "wow-classic-items", "cataclysm-dda",
        "diablo2-d2data", "path-of-exile-repoe", "bloqhead-demigods",
    }
    if source in trusted_sources:
        if wieldable in {"one_hand", "two_hand", "shoulder_supported", "either"}:
            return CAT_HANDHELD, f"wieldable={wieldable}"
    if wieldable == "mount_required":
        return CAT_SIEGE, f"wieldable={wieldable}"
    return None


# Expanded name-token sets for catching wikipedia/odin leftovers
WP_ODIN_SIEGE_NAME_TOKENS = {
    "missile", "rocket", " bomb", "warhead", "torpedo",
    "tank", "armored car", "armoured car", "truck", "tractor",
    "uav", "ugv", "drone",
    "ship", "submarine", "boat", "vessel", "cruiser", "frigate", "destroyer",
    "aircraft", "helicopter", "flying boat",
    "howitzer", "mortar", "artillery", "field gun", "naval gun",
    "anti-aircraft", "anti-tank", "anti-ballistic", "anti-materiel",
    "slbm", "icbm", "mrbm", "irbm", "srbm", "abm",
    "crane", "amphibious", "icebreaker", "cargo",
    "system", "radar", "platform", "dazzler",
    "rocket launcher", "missile launcher",
    "main battle tank", "mbt",
    "patrol vessel",
    "shahed", "geran",
    "phased array",
    "electronic warfare",
    "active protection",
    "fire and forget",
}

WP_ODIN_AMMO_NAME_TOKENS = {
    "mm",  # 5.6×39mm / 6mm ARC etc.
    "cartridge", "round", "shell",
    "musket ball", "lead ball",
    "fuze", "detonator",
}

ART_AWARD_TOKENS = {
    "reproduction of the seal", "seal of",
    "plaquette", "medallion",
    "honorary", "for bravery", "honorary revolutionary",
    "st. george", "st george",
    "various designs", "designs for",
}


def classify_by_name_extended(name: str) -> tuple[str, str] | None:
    """Extended fallback for wikipedia / odin leftover rows."""
    nl = name.lower()
    # Art / award names first
    for tok in sorted(ART_AWARD_TOKENS, key=len, reverse=True):
        if tok in nl:
            return CAT_ART, f"name-ext:art={tok}"
    # Siege patterns
    for tok in sorted(WP_ODIN_SIEGE_NAME_TOKENS, key=len, reverse=True):
        if tok in nl:
            return CAT_SIEGE, f"name-ext:siege={tok}"
    # Ammo via the mm cartridge pattern: bare "5.6×39mm" etc.
    # Only flag as ammo if name pattern matches caliber form
    if re.search(r"\d+\s*[×x]\s*\d+\s*mm", nl) or re.search(r"\d+\s*mm\s*[a-z]*$", nl):
        return CAT_AMMO, "name-ext:ammo=mm-caliber"
    return None


# ---------------------------------------------------------------------------
# Master classifier
# ---------------------------------------------------------------------------

# Manual overrides for the small leftover set of wikipedia rows that have
# thin infobox metadata and ambiguous canonical names. Each entry verified
# against the underlying real-world identity (per Discipline #11: attribution-clarity
# preserves the manual-review provenance).
MANUAL_OVERRIDES = {
    # Legendary / historical named handheld weapons
    174103: ("handheld_weapon", "manual:Mjölnir=Thor's hammer"),
    174145: ("handheld_weapon", "manual:Vajra=Indra's ritual weapon"),
    175173: ("handheld_weapon", "manual:Curtana=Tristan's sword"),
    175200: ("handheld_weapon", "manual:Ame-no-Nuboko=mythological spear"),
    175456: ("handheld_weapon", "manual:Mjolnir(comics)=Marvel Thor hammer"),
    175580: ("handheld_weapon", "manual:Joyeuse=Charlemagne's sword"),
    175669: ("handheld_weapon", "manual:Claíomh Solais=Lugh's sword"),
    176565: ("handheld_weapon", "manual:Kogarasu Maru=Amakuni named sword"),
    176855: ("handheld_weapon", "manual:Nægling=Beowulf's sword"),
    180679: ("handheld_weapon", "manual:Mistilteinn=Baldr-killing weapon"),
    181836: ("handheld_weapon", "manual:Colada=El Cid's sword"),
    188718: ("handheld_weapon", "manual:Seax of Beagnoth=anglo-saxon blade"),
    194198: ("handheld_weapon", "manual:Tai'e=Chinese mythological sword"),
    175907: ("handheld_weapon", "manual:KelTec P11=subcompact pistol"),
    # Siege/vehicle/missile (Mode-C second-wave wikipedia patterns)
    174014: ("siege_vehicle", "manual:M142 HIMARS=rocket-launcher truck"),
    174056: ("siege_vehicle", "manual:GBU-43/B MOAB=large-yield bomb"),
    176514: ("siege_vehicle", "manual:Warwolf=Edward I siege trebuchet"),
    181959: ("siege_vehicle", "manual:8-inch gun M1=US heavy artillery"),
    182543: ("siege_vehicle", "manual:QF 6-pounder Hotchkiss=naval/AT gun"),
    188234: ("siege_vehicle", "manual:Splitterskyddad EnhetsPlattform=Swedish AFV"),
    189756: ("siege_vehicle", "manual:Thor III=US ICBM proposal"),
    192051: ("siege_vehicle", "manual:GÖKTUĞ=Turkish air-to-air missile"),
    192601: ("siege_vehicle", "manual:Bharat-52=Indian 155mm artillery"),
    180618: ("siege_vehicle", "manual:GQM-163 Coyote=target drone"),
    183770: ("siege_vehicle", "manual:SH-ZX-480-A=Chinese gyrocopter"),
    # Person mis-extracted as weapon (Mode-D cross-tagged error)
    180646: ("other", "manual:Robert Keyes=person, not a weapon"),
}


def classify_row(row: dict) -> tuple[str, str]:
    """Return (category, method_attribution) for a Tier-S row.

    Method attribution per Discipline #11.

    NOTE: Stage 1's `weapon_kind='ammo_or_consumable'` label is a Stage 1 semantic
    misalignment — it captured armor pieces (gauntlets, helms, cuisses) alongside
    actual ammo. We do NOT trust that label; we re-route through structured signals
    + name-tokens which give correct armor-vs-ammo separation.
    """
    source = row["source_library"]
    name = row["canonical_name"] or ""
    wieldable = row.get("wieldable_humanoid") or "unknown"

    # Stage 0: manual overrides (small leftover set; per Discipline #11)
    if row["id"] in MANUAL_OVERRIDES:
        return MANUAL_OVERRIDES[row["id"]]

    try:
        structured = json.loads(row["structured_properties"] or "{}")
    except (json.JSONDecodeError, TypeError):
        structured = {}

    # Stage 1: source-specific structured signal (most diagnostic)
    result = None
    if source == "met-museum":
        result = classify_met_museum(structured)
    elif source == "royal_armouries":
        result = classify_royal_armouries(structured, name)
    elif source == "wikipedia":
        result = classify_wikipedia(structured)
    elif source == "odin-army-tradoc":
        result = classify_odin_army_tradoc(structured)
    elif source == "wikidata":
        result = classify_wikidata(structured)

    if result:
        return result

    # Stage 2: name-token fallback (primary vocab)
    result = classify_by_name(name)
    if result:
        return result

    # Stage 2b: extended name-token fallback (siege/ammo/art catch)
    # — apply for ALL sources to catch Met seals/plaquettes and any
    # wikipedia/odin leftovers
    result = classify_by_name_extended(name)
    if result:
        return result

    # Stage 3: register_canonical=mythological is decisive for handheld
    # (these are clean Mode-A wikipedia mythological-article rows)
    register = row.get("register_canonical") or ""
    if register == "mythological":
        return CAT_HANDHELD, "register=mythological"

    # Stage 4: wieldable corroboration (only for trusted named-legendary sources)
    result = classify_by_wieldable(wieldable, source)
    if result:
        return result

    return CAT_OTHER, "unclassified"


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """
        SELECT id, canonical_name, source_library, structured_properties,
               wieldable_humanoid, weapon_kind, quality_composite_score,
               named_mythological_match, register_canonical, cultural_lineage_canonical
        FROM weapon_knowledge_entries
        WHERE quality_tier = 'S'
        ORDER BY id
        """
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    classifications = []
    for r in rows:
        category, method = classify_row(r)
        classifications.append({
            "id": r["id"],
            "canonical_name": r["canonical_name"],
            "source_library": r["source_library"],
            "category": category,
            "method": method,
            "quality_composite_score": r["quality_composite_score"],
            "named_mythological_match": r["named_mythological_match"],
            "register_canonical": r["register_canonical"],
            "cultural_lineage_canonical": r["cultural_lineage_canonical"],
            "wieldable_humanoid": r["wieldable_humanoid"],
            "weapon_kind_stage1": r["weapon_kind"],
        })

    # Write machine-readable JSON
    out_json = OUT_DIR / "tier-s-classification.json"
    with open(out_json, "w") as f:
        json.dump({"total_rows": len(classifications), "classifications": classifications}, f, indent=2)

    # Aggregate stats
    cat_counts = Counter(c["category"] for c in classifications)
    method_counts = Counter(c["method"].split(":")[0].split("=")[0] for c in classifications)

    per_source = defaultdict(Counter)
    for c in classifications:
        per_source[c["source_library"]][c["category"]] += 1

    # Top-10 examples per category
    examples = defaultdict(list)
    for c in classifications:
        if len(examples[c["category"]]) < 10:
            examples[c["category"]].append(
                f'[{c["id"]}] {c["canonical_name"][:80]} (src={c["source_library"]}; method={c["method"][:60]})'
            )

    print("=" * 70)
    print("TIER-S WEAPON-KIND CLASSIFICATION — Cycle 10 Stage 2.5 Refutation-Routing")
    print("=" * 70)
    print(f"\nTotal Tier-S rows classified: {len(classifications)}")
    print(f"\n--- Category Distribution ---")
    total = len(classifications)
    for cat in [CAT_HANDHELD, CAT_ACCESSORY, CAT_ARMOR, CAT_AMMO, CAT_SIEGE, CAT_ART, CAT_OTHER]:
        n = cat_counts.get(cat, 0)
        pct = 100.0 * n / total
        print(f"  {cat:20s} {n:5d}  ({pct:5.2f}%)")

    print(f"\n--- Method Attribution (top-level) ---")
    for m, n in method_counts.most_common():
        print(f"  {m:30s} {n:5d}")

    print(f"\n--- Per-Source Breakdown ---")
    for src, c in sorted(per_source.items(), key=lambda x: -sum(x[1].values())):
        total_src = sum(c.values())
        print(f"\n  {src} (n={total_src}):")
        for cat in [CAT_HANDHELD, CAT_ACCESSORY, CAT_ARMOR, CAT_AMMO, CAT_SIEGE, CAT_ART, CAT_OTHER]:
            n = c.get(cat, 0)
            pct = 100.0 * n / total_src if total_src else 0
            if n:
                print(f"    {cat:20s} {n:5d}  ({pct:5.2f}%)")

    print(f"\n--- Examples per Category (top 10) ---")
    for cat in [CAT_HANDHELD, CAT_ACCESSORY, CAT_ARMOR, CAT_AMMO, CAT_SIEGE, CAT_ART, CAT_OTHER]:
        print(f"\n  {cat}:")
        for ex in examples[cat]:
            print(f"    {ex}")

    print(f"\n--- Output ---")
    print(f"  JSON: {out_json}")
    print(f"  Cost: $0.00 (heuristic-only; no LLM-judge invoked)")

    return cat_counts, per_source, examples, method_counts


if __name__ == "__main__":
    main()
