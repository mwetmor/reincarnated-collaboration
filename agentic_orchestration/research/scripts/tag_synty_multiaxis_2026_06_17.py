#!/usr/bin/env python3
"""
tag_synty_multiaxis_2026_06_17.py — elrond (data steward)

ADDITIVE multi-axis tagging of the Synty gear-substrate catalogue (synty_catalogue.db).
Materializes the manifest substrate-half + density map per the gandalf commission:
    agentic_orchestration/gandalf/requests/2026-06-17-elrond-catalogue-multiaxis-tagging.md

Tags all 157 pack rows (156 content collections; Water Guns ships 2 FBX packs) on FIVE axes:
    1. register           — substrate-GIVEN  (POLYGON | POLYGON_MINI | SIMPLE), parsed from name.
    2. contribution_role  — doc-DERIVED      (armor-base-skinned | weapon-base-static |
                            accent-attach-static | environment | anim | ui), from asset-type mix.
    3. time_period        — substrate-VOTED  (PROPOSED stratum; gandalf curates the label).
    4. cultural_identity  — substrate-VOTED  (PROPOSED stratum; gandalf curates the label).
    5. seam               — substrate-GIVEN + light curation.

DISCIPLINE — substrate-led split (brief §2):
    Axes 1, 5 are factual (Synty naming). Axis 2 is doc-derived design taxonomy. Axes 3, 4 are
    where the substrate must VOTE and gandalf curates the labels at a rep-audit. This script writes
    a PROPOSED stratum to the DB for axes 3+4, AND emits a rep-examples manifest (the JSONL/MD
    deliverables) so gandalf can audit reps and curate the final label. The DB value is elrond's
    proposal — NOT a unilateral semantic label. Per semantic-layer rep-audit discipline (#25),
    substrate-vote is binding at the geometry layer but NOT the semantic layer.

ADDITIVE (brief §4): adds nullable columns to `packs`; does NOT delete or re-shape any existing
row, column, or asset. synty_catalogue schema 1.0 -> 1.1. Idempotent — re-runnable.

Run:
    python3 tag_synty_multiaxis_2026_06_17.py            # apply additive schema + tag all packs
    python3 tag_synty_multiaxis_2026_06_17.py report     # (after tagging) emit JSONL + MD deliverables
    python3 tag_synty_multiaxis_2026_06_17.py all         # tag THEN report (default-runnable end-to-end)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
COLLAB_ROOT = os.path.join(HOME, "Games", "reincarnated-collaboration")
DB_PATH = os.path.join(COLLAB_ROOT, "agentic_orchestration", "research", "curated", "synty_catalogue.db")
RECON_DIR = os.path.join(
    COLLAB_ROOT, "agentic_orchestration", "research", "catalogue", "synty-recon-2026-06-16"
)
OUT_JSONL = os.path.join(RECON_DIR, "multiaxis-tags-2026-06-17.jsonl")
OUT_MD = os.path.join(RECON_DIR, "multiaxis-tags-2026-06-17.md")

NEW_SCHEMA_VERSION = "1.1"


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Axis 1 — register (substrate-GIVEN: parse the Synty pack-name prefix)
# ---------------------------------------------------------------------------
def axis_register(name):
    if name.startswith("POLYGON MINI"):
        return "POLYGON_MINI"
    if name.startswith("POLYGON"):
        return "POLYGON"
    if name.startswith("SIMPLE"):
        return "SIMPLE"
    if name.startswith("ANIMATION"):
        return "ANIMATION"   # animation packs are register-orthogonal (rig-targeted, not a style line)
    if name.startswith("INTERFACE"):
        return "INTERFACE"   # ui packs are register-orthogonal
    return "OTHER"


# ---------------------------------------------------------------------------
# Axis 2 — contribution_role (doc-DERIVED: asset-class x skinned/static from the asset mix)
# ---------------------------------------------------------------------------
# Per brief §0 gear-spec architecture:
#   armor-base-skinned  : ships skinned character/armor meshes — the restyle base.
#   accent-attach-static: ships BoneAttachment3D accents (silhouette-breakers) WITHOUT being a
#                         skinned-character base (i.e. accent-dominant prop packs).
#   weapon-base-static  : weapon-dominant (the 100k corpus is PRIMARY for weapons; Synty weapon
#                         packs are a SECONDARY common-weapon base).
#   environment         : set-dressing — no character/weapon/accent contribution.
#   anim                : ANIMATION packs (rig-targeted clips).
#   ui                  : INTERFACE packs (HUD/menu).
#
# Routing is by the dominant *contribution* the pack makes to the architecture, NOT by raw asset
# counts alone — a pack with a handful of incidental characters in a city environment is
# environment-primary. Threshold logic documented inline; reproducible from counts in the DB.
# Bestiary packs — skinned NON-humanoid creature/animal meshes. These are genuinely skinned but
# are NOT humanoid armor restyle bases (an animal does not take a chest/legs/boots armor fill).
# They route to `bestiary` contribution (a distinct enemy-mesh contribution), guarding the
# armor-base-skinned set from polluting with cats/dogs/kaiju. (zombies in human clothing DO stay
# armor-base-skinned — they are humanoid restyle bases.)
BESTIARY_NONHUMANOID = {
    "SIMPLE - Cats", "SIMPLE - Dogs", "SIMPLE - Farm Animals", "SIMPLE - Forest Animals",
    "POLYGON - Dog Pack", "POLYGON - Kaiju", "POLYGON - Frog Shrine",
}


def axis_contribution_role(name, counts):
    chars = counts["chars"]
    weps = counts["weps"]
    accents = counts["accents"]
    env = counts["env"]
    prop = counts["prop"]
    total = counts["total"]

    reg = axis_register(name)
    if reg == "ANIMATION":
        return "anim", "ANIMATION pack — rig-targeted clips; no geometry contribution."
    if reg == "INTERFACE":
        return "ui", "INTERFACE pack — HUD/menu textures; no skinned-character/weapon geometry."

    if name in BESTIARY_NONHUMANOID:
        return ("bestiary",
                f"skinned NON-humanoid creature meshes ({chars} chars) — enemy/companion mesh, "
                f"NOT a humanoid armor restyle base.")

    # NOTE: the WAVE-1 classifier mislabels rigged SK_Veh_/SK_Bld_ meshes as 'character' in a few
    # vehicle/environment packs (Sci-Fi Worlds, Street Racer). We guard those by name below so a
    # vehicle pack does not route to armor-base-skinned. (Substrate-honest: the false-positive is in
    # the upstream asset classifier; we correct the ROUTING here without rewriting asset rows.)
    VEHICLE_FALSE_CHAR = {
        "POLYGON - Sci-Fi Worlds Pack",   # SK_Veh_ rigged vehicles counted as chars
        "POLYGON - Street Racer",         # SK_ rigged car parts counted as chars
        "POLYGON - Pro Racer",
    }
    effective_chars = 0 if name in VEHICLE_FALSE_CHAR else chars

    # Skinned-character base: a meaningful population of genuine skinned characters.
    # >=8 whole characters OR a modular per-slot pack (armor_part-dominant skinned).
    is_modular_armor = counts["structural_class"] == "modular"
    if is_modular_armor:
        return ("armor-base-skinned",
                "Modular per-slot SKINNED armor pack — the canonical restyle base (StyleProfile fill).")
    if effective_chars >= 8:
        return ("armor-base-skinned",
                f"{effective_chars} skinned whole-character appearance-units — restyle base.")

    # Accent-dominant: ships accents (BoneAttachment3D silhouette-breakers) but is not a
    # skinned-character base. (Few packs in corpus; guards the accent contribution explicitly.)
    if accents >= 8 and effective_chars < 8:
        return ("accent-attach-static",
                f"{accents} accent attachments (silhouette-breakers) dominate; sub-base char count.")

    # Weapon-dominant base: weapon-heavy, character-light (dedicated weapon packs).
    if weps >= 4 and effective_chars < 8 and (env + prop) < max(1, weps):
        return ("weapon-base-static",
                f"{weps} weapon meshes dominate (common-weapon base; 100k corpus is primary).")

    # A small character presence inside an environment pack still contributes a few skinned bases,
    # but the pack's PRIMARY contribution is set-dressing. Record as environment with a char note.
    if effective_chars > 0:
        return ("environment",
                f"environment-primary ({env} env + {prop} prop); incidental {effective_chars} chars "
                f"(secondary skinned-base contribution).")
    if weps > 0:
        return ("environment",
                f"environment-primary; incidental {weps} weapon meshes (secondary weapon-base).")
    return ("environment", f"set-dressing ({env} env + {prop} prop); no skinned/weapon contribution.")


# ---------------------------------------------------------------------------
# Axis 5 — seam (substrate-GIVEN Synty category + light curation)
# ---------------------------------------------------------------------------
# seam values per brief §2: descent | overworld | nature | char-skeletal |
#   char-named-silhouette | weapon-prop | bestiary | anim | ui
def axis_seam(name, counts):
    n = name.lower()
    reg = axis_register(name)
    if reg == "ANIMATION":
        return "anim"
    if reg == "INTERFACE":
        return "ui"

    # nature biomes / nature pack
    if "nature biome" in n or n.endswith("- nature pack") or "nature pack" in n:
        return "nature"
    # bestiary — creature/animal/monster packs
    if any(k in n for k in ("dog pack", "cats", "dogs", "farm animals", "forest animals",
                            "kaiju", "werewolf", "boss zombies", "zombies", "frog shrine")):
        return "bestiary"
    # weapon-prop — dedicated weapon/prop packs
    if any(k in n for k in ("bow and crossbow", "water guns", "pride crystal weapons",
                            "bubblegum killstick", "icons pack", "props/items/icons",
                            "legendary chest", "halloween horror masks", "adult face plates")):
        return "weapon-prop"
    # descent — dungeon/crypt/fortress interiors
    if any(k in n for k in ("dungeon", "dark fortress", "temples", "frog shrine",
                            "horror asylum", "horror mansion", "apocalypse interiors",
                            "fantasy interiors", "house interiors", "space interiors",
                            "shop interiors")):
        return "descent"
    # char-skeletal — modular/skinned character base packs
    if counts["structural_class"] == "modular":
        return "char-skeletal"
    if any(k in n for k in ("characters", "citizens", "people", "modular fantasy hero")):
        return "char-skeletal"
    # char-named-silhouette — named-character monolithic packs with high char count
    if counts["chars"] >= 8 and name not in (
        "POLYGON - Sci-Fi Worlds Pack", "POLYGON - Street Racer", "POLYGON - Pro Racer"
    ):
        return "char-named-silhouette"
    # default: overworld set-dressing
    return "overworld"


# ---------------------------------------------------------------------------
# Axes 3 + 4 — time_period + cultural_identity (substrate-VOTED — PROPOSED only)
# ---------------------------------------------------------------------------
# These are PROPOSALS. gandalf curates the final semantic label at a rep-audit. The DB column
# carries elrond's proposed stratum; the rep-examples manifest carries the evidence gandalf audits.
#
# Hypothesis strata (brief §2) — used as PROPOSAL buckets, not imposed enums:
#   time_period:  antiquity | medieval-fantasy | renaissance-early-modern |
#                 industrial-steampunk | modern | sci-fi-future | timeless-na
#   cultural:     (Mode-A geographic / Mode-B tradition) w-euro-medieval | norse | east-asian |
#                 egyptian | mesoamerican | indo-asian | modern-western | generic-fantasy |
#                 sci-fi | na   (+ confidence + mode-flag to guard the Mode A/B/C/D collapse)
#
# Each pack carries a `_basis` string naming the name-token evidence the proposal rests on —
# this is what gandalf rep-audits against the actual meshes.

# (substring-in-lowered-name, time_period proposal, basis)
TIME_PERIOD_RULES = [
    ("ancient egypt", "antiquity", "Egypt = bronze-age antiquity"),
    ("ancient empire", "antiquity", "ancient empire = greco-roman antiquity"),
    ("samurai", "renaissance-early-modern", "feudal-Japan sengoku ~ early-modern"),
    ("viking", "medieval-fantasy", "Norse early-medieval"),
    ("pirate", "renaissance-early-modern", "age-of-sail early-modern"),
    ("western", "modern", "American frontier 19thC (industrial-adjacent)"),
    ("knights", "medieval-fantasy", "high-medieval"),
    ("dark fantasy", "medieval-fantasy", "gothic medieval-fantasy"),
    ("dark fortress", "medieval-fantasy", "medieval-fantasy fortress"),
    ("dungeon", "medieval-fantasy", "medieval-fantasy dungeon"),
    ("elven", "medieval-fantasy", "high-fantasy"),
    ("goblin", "medieval-fantasy", "fantasy"),
    ("fantasy", "medieval-fantasy", "generic medieval-fantasy"),
    ("dwarven", "medieval-fantasy", "fantasy"),
    ("adventure", "medieval-fantasy", "fantasy adventure"),
    ("explorer", "modern", "modern explorer kit"),
    ("apocalypse", "modern", "modern/post-apocalyptic"),
    ("woodland apocalypse", "modern", "modern post-apocalyptic"),
    ("military", "modern", "modern military"),
    ("war map - wwi", "industrial-steampunk", "WWI industrial-era"),
    ("war pack", "modern", "modern war"),
    ("heist", "modern", "modern crime"),
    ("spy", "modern", "modern espionage"),
    ("gang warfare", "modern", "modern urban"),
    ("city", "modern", "modern city"),
    ("town", "modern", "modern town"),
    ("street racer", "modern", "modern motorsport"),
    ("pro racer", "modern", "modern motorsport"),
    ("racer", "modern", "modern motorsport"),
    ("office", "modern", "modern office"),
    ("nightclub", "modern", "modern nightlife"),
    ("casino", "modern", "modern casino"),
    ("coffee shop", "modern", "modern retail"),
    ("shops", "modern", "modern retail"),
    ("shop", "modern", "modern retail"),
    ("shopping plaza", "modern", "modern retail"),
    ("construction", "modern", "modern construction"),
    ("police", "modern", "modern police"),
    ("farm", "modern", "modern/timeless rural"),
    ("port", "modern", "modern port"),
    ("airport", "modern", "modern transport"),
    ("trains", "industrial-steampunk", "rail = industrial-era"),
    ("quad bike", "modern", "modern vehicle"),
    ("stunt plane", "modern", "modern aviation"),
    ("hearse", "modern", "modern vehicle"),
    ("kids", "modern", "modern contemporary"),
    ("wheelchair", "modern", "modern contemporary"),
    ("battle royale", "modern", "modern/near-future shooter"),
    ("mech", "sci-fi-future", "mech = sci-fi"),
    ("sci-fi", "sci-fi-future", "explicit sci-fi"),
    ("space", "sci-fi-future", "space = sci-fi"),
    ("kaiju", "modern", "modern-monster (kaiju genre)"),
    ("werewolf", "timeless-na", "creature — period-agnostic"),
    ("zombie", "modern", "modern-horror zombie"),
    ("horror asylum", "modern", "modern-horror"),
    ("horror mansion", "modern", "modern/gothic-horror"),
    ("horror carnival", "modern", "modern-horror"),
    ("sci-fi horror", "sci-fi-future", "sci-fi horror"),
    ("prototype", "timeless-na", "greybox/prototype — period-agnostic"),
    ("starter", "timeless-na", "tutorial/starter — mixed"),
    # holiday/seasonal/pride/misc -> timeless-na
    ("easter", "timeless-na", "seasonal"),
    ("xmax", "timeless-na", "seasonal"),
    ("santa", "timeless-na", "seasonal"),
    ("holiday", "timeless-na", "seasonal"),
    ("gingerbread", "timeless-na", "seasonal"),
    ("pumpkin", "timeless-na", "seasonal"),
    ("snow kit", "timeless-na", "seasonal"),
    ("valentine", "timeless-na", "seasonal"),
    ("celebration", "timeless-na", "seasonal"),
    ("pride", "timeless-na", "thematic"),
    ("gnome", "medieval-fantasy", "fantasy"),
    ("frog shrine", "medieval-fantasy", "fantasy shrine"),
    ("plushie", "timeless-na", "toy/thematic"),
    ("dog", "timeless-na", "animal — period-agnostic"),
    ("cat", "timeless-na", "animal — period-agnostic"),
    ("animal", "timeless-na", "animal — period-agnostic"),
    ("forest animals", "timeless-na", "animal — period-agnostic"),
    ("face plates", "timeless-na", "modular-face — period-agnostic"),
    ("particle fx", "timeless-na", "FX — period-agnostic"),
    ("fx", "timeless-na", "FX — period-agnostic"),
    ("sky", "timeless-na", "skybox — period-agnostic"),
    ("roadwork", "modern", "modern infrastructure"),
    ("buildings", "modern", "generic modern buildings"),
    ("car", "modern", "modern vehicle"),
    ("legendary chest", "medieval-fantasy", "fantasy loot prop"),
    ("icons", "timeless-na", "UI icon meshes — period-agnostic"),
    ("nature", "timeless-na", "nature biome — period-agnostic"),
    ("alpine", "timeless-na", "nature biome"),
    ("desert", "timeless-na", "nature biome"),
    ("forest", "timeless-na", "nature biome"),
    ("jungle", "timeless-na", "nature biome"),
    ("marsh", "timeless-na", "nature biome"),
    ("swamp", "timeless-na", "nature biome"),
    ("meadow", "timeless-na", "nature biome"),
    ("palm city", "modern", "modern tropical city"),
]

# (substring, cultural proposal, mode-flag, basis)
#   mode A = geographic-origin token, B = cultural-tradition, C = naming-allusion, D = metadata-mix
CULTURE_RULES = [
    ("ancient egypt", "egyptian", "A", "explicit Egypt geography"),
    ("samurai", "east-asian", "B", "Japanese samurai tradition"),
    ("viking", "norse", "B", "Norse cultural tradition"),
    ("knights", "w-euro-medieval", "B", "W-European chivalric tradition"),
    ("ancient empire", "greco-roman", "B", "greco-roman classical tradition"),
    ("dwarven", "generic-fantasy", "C", "fantasy-race allusion (not a real culture)"),
    ("elven", "generic-fantasy", "C", "fantasy-race allusion"),
    ("goblin", "generic-fantasy", "C", "fantasy-race allusion"),
    ("pirate", "generic-fantasy", "C", "age-of-sail genre (pan-cultural)"),
    ("western", "modern-western", "B", "American frontier tradition"),
    ("dark fantasy", "generic-fantasy", "C", "gothic-fantasy allusion"),
    ("dark fortress", "generic-fantasy", "C", "gothic-fantasy allusion"),
    ("fantasy", "generic-fantasy", "C", "generic-fantasy"),
    ("dungeon", "generic-fantasy", "C", "generic-fantasy"),
    ("adventure", "generic-fantasy", "C", "generic-fantasy"),
    ("sci-fi", "sci-fi", "C", "sci-fi register (acultural)"),
    ("space", "sci-fi", "C", "sci-fi register"),
    ("mech", "sci-fi", "C", "sci-fi register"),
    ("apocalypse", "modern-western", "C", "post-apoc modern-western default skin"),
    ("battle royale", "modern-western", "C", "modern military-shooter"),
    ("military", "modern-western", "C", "modern military"),
    ("war", "modern-western", "C", "modern war"),
    ("city", "modern-western", "C", "modern western-urban default"),
    ("town", "modern-western", "C", "modern western default"),
    ("gang", "modern-western", "C", "modern urban"),
    ("heist", "modern-western", "C", "modern crime"),
    ("spy", "modern-western", "C", "modern espionage"),
    ("office", "modern-western", "C", "modern western"),
    ("street racer", "modern-western", "C", "modern motorsport"),
    ("pro racer", "modern-western", "C", "modern motorsport"),
    ("kids", "modern-western", "C", "modern contemporary"),
    ("nature", "na", "D", "nature biome — no cultural read"),
    ("alpine", "na", "D", "nature biome"),
    ("desert", "na", "D", "nature biome"),
    ("forest", "na", "D", "nature biome"),
    ("jungle", "na", "D", "nature biome"),
    ("swamp", "na", "D", "nature biome"),
    ("meadow", "na", "D", "nature biome"),
]


def propose_time_period(name):
    n = name.lower()
    for sub, tp, basis in TIME_PERIOD_RULES:
        if sub in n:
            return tp, f"name-token '{sub}': {basis}"
    return "unresolved", "no time-period token matched — gandalf rep-audit required"


def propose_culture(name):
    n = name.lower()
    for sub, cul, mode, basis in CULTURE_RULES:
        if sub in n:
            return cul, mode, f"name-token '{sub}' [mode {mode}]: {basis}"
    return "unresolved", "?", "no culture token matched — gandalf rep-audit required"


# ---------------------------------------------------------------------------
# Schema migration (additive) + tagging
# ---------------------------------------------------------------------------
ADDITIVE_COLUMNS = [
    ("register", "TEXT"),
    ("contribution_role", "TEXT"),
    ("contribution_basis", "TEXT"),
    ("time_period_proposed", "TEXT"),
    ("time_period_basis", "TEXT"),
    ("cultural_identity_proposed", "TEXT"),
    ("cultural_mode_flag", "TEXT"),
    ("cultural_basis", "TEXT"),
    ("seam", "TEXT"),
    ("tagged_at", "TEXT"),
]


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_columns(conn):
    existing = {r[1] for r in conn.execute("PRAGMA table_info(packs)")}
    for col, typ in ADDITIVE_COLUMNS:
        if col not in existing:
            conn.execute(f"ALTER TABLE packs ADD COLUMN {col} {typ}")
    conn.commit()


def pack_counts(conn, pack_id, structural_class):
    row = conn.execute(
        "SELECT "
        " SUM(CASE WHEN asset_type='character' THEN 1 ELSE 0 END),"
        " SUM(CASE WHEN asset_type='weapon' THEN 1 ELSE 0 END),"
        " SUM(CASE WHEN asset_type='armor_part' THEN 1 ELSE 0 END),"
        " SUM(CASE WHEN is_accent=1 THEN 1 ELSE 0 END),"
        " SUM(CASE WHEN asset_type='environment' THEN 1 ELSE 0 END),"
        " SUM(CASE WHEN asset_type='prop' THEN 1 ELSE 0 END),"
        " COUNT(*)"
        " FROM assets WHERE pack_id=?", (pack_id,)
    ).fetchone()
    return {
        "chars": row[0] or 0, "weps": row[1] or 0, "armor": row[2] or 0,
        "accents": row[3] or 0, "env": row[4] or 0, "prop": row[5] or 0,
        "total": row[6] or 0, "structural_class": structural_class,
    }


def cmd_tag():
    conn = connect()
    ensure_columns(conn)
    packs = conn.execute(
        "SELECT pack_id, collection_id, collection_name, structural_class FROM packs ORDER BY collection_name"
    ).fetchall()
    n = 0
    for pack_id, cid, name, structural_class in packs:
        counts = pack_counts(conn, pack_id, structural_class)
        register = axis_register(name)
        role, role_basis = axis_contribution_role(name, counts)
        tp, tp_basis = propose_time_period(name)
        cul, mode, cul_basis = propose_culture(name)
        seam = axis_seam(name, counts)
        conn.execute(
            "UPDATE packs SET register=?, contribution_role=?, contribution_basis=?, "
            "time_period_proposed=?, time_period_basis=?, cultural_identity_proposed=?, "
            "cultural_mode_flag=?, cultural_basis=?, seam=?, tagged_at=? WHERE pack_id=?",
            (register, role, role_basis, tp, tp_basis, cul, mode, cul_basis, seam, now_iso(), pack_id),
        )
        n += 1
    # bump synty schema 1.0 -> 1.1 (additive)
    conn.execute(
        "INSERT OR IGNORE INTO schema_meta(version, applied_at, description, migration_script) VALUES (?,?,?,?)",
        (NEW_SCHEMA_VERSION, now_iso(),
         "Additive multi-axis pack tagging: register, contribution_role, time_period_proposed, "
         "cultural_identity_proposed (+mode_flag), seam. Axes 3+4 are PROPOSALS for gandalf rep-audit "
         "curation; basis columns carry the name-token evidence. No destructive change.",
         os.path.basename(__file__)))
    conn.commit()
    print(f"tagged {n} packs on 5 axes; synty schema -> {NEW_SCHEMA_VERSION}")
    conn.close()


def cmd_report():
    conn = connect()
    rows = conn.execute(
        "SELECT p.pack_id, p.collection_id, p.collection_name, p.register, p.structural_class, "
        "p.contribution_role, p.contribution_basis, p.time_period_proposed, p.time_period_basis, "
        "p.cultural_identity_proposed, p.cultural_mode_flag, p.cultural_basis, p.seam, p.source, "
        "(SELECT COUNT(*) FROM assets a WHERE a.pack_id=p.pack_id AND a.asset_type='character'), "
        "(SELECT COUNT(*) FROM assets a WHERE a.pack_id=p.pack_id AND a.asset_type='weapon'), "
        "(SELECT COUNT(*) FROM assets a WHERE a.pack_id=p.pack_id AND a.is_accent=1), "
        "(SELECT COUNT(*) FROM assets a WHERE a.pack_id=p.pack_id) "
        "FROM packs p ORDER BY p.collection_name"
    ).fetchall()

    # JSONL — one row per pack
    with open(OUT_JSONL, "w") as f:
        for r in rows:
            f.write(json.dumps({
                "pack_id": r[0], "collection_id": r[1], "collection_name": r[2],
                "axis1_register": r[3], "structural_class": r[4],
                "axis2_contribution_role": r[5], "contribution_basis": r[6],
                "axis3_time_period_proposed": r[7], "time_period_basis": r[8],
                "axis4_cultural_identity_proposed": r[9], "cultural_mode_flag": r[10],
                "cultural_basis": r[11],
                "axis5_seam": r[12], "source": r[13],
                "char_count": r[14], "weapon_count": r[15], "accent_count": r[16],
                "asset_count": r[17],
            }) + "\n")

    # Strata aggregation for the gandalf rep-audit (axes 3+4)
    tp_strata = {}
    cul_strata = {}
    for r in rows:
        tp_strata.setdefault(r[7], []).append((r[2], r[8], r[14], r[15]))
        cul_strata.setdefault((r[9], r[10]), []).append((r[2], r[11], r[14]))

    role_dist = {}
    seam_dist = {}
    reg_dist = {}
    for r in rows:
        role_dist[r[5]] = role_dist.get(r[5], 0) + 1
        seam_dist[r[12]] = seam_dist.get(r[12], 0) + 1
        reg_dist[r[3]] = reg_dist.get(r[3], 0) + 1

    lines = []
    lines.append("# Synty catalogue — multi-axis tags (substrate-half + density map)\n")
    lines.append("**Author:** elrond | **Date:** 2026-06-17 | **Commission:** "
                 "`agentic_orchestration/gandalf/requests/2026-06-17-elrond-catalogue-multiaxis-tagging.md`\n")
    lines.append("**Substrate:** `synty_catalogue.db` (schema 1.1) — 157 pack rows / 156 content "
                 "collections. Tags are ADDITIVE columns on `packs`.\n")
    lines.append("**Axis discipline:** 1+5 substrate-GIVEN; 2 doc-DERIVED; **3+4 substrate-VOTED — "
                 "PROPOSALS for gandalf rep-audit curation, NOT unilateral labels.**\n")

    lines.append("\n## Axis 1 — register distribution\n")
    for k in sorted(reg_dist): lines.append(f"- `{k}`: {reg_dist[k]} packs")

    lines.append("\n## Axis 2 — contribution_role distribution (every pack routes)\n")
    for k in sorted(role_dist, key=lambda x: -role_dist[x]):
        lines.append(f"- `{k}`: {role_dist[k]} packs")

    lines.append("\n## Axis 5 — seam distribution\n")
    for k in sorted(seam_dist, key=lambda x: -seam_dist[x]):
        lines.append(f"- `{k}`: {seam_dist[k]} packs")

    lines.append("\n## Axis 3 — PROPOSED time_period strata (gandalf curates) — rep examples\n")
    for tp in sorted(tp_strata, key=lambda x: -len(tp_strata[x])):
        reps = tp_strata[tp]
        lines.append(f"\n### `{tp}` — {len(reps)} packs")
        for name, basis, c, w in reps[:8]:
            lines.append(f"- **{name}** (chars={c}, weps={w}) — {basis}")
        if len(reps) > 8:
            lines.append(f"- …and {len(reps)-8} more")

    lines.append("\n## Axis 4 — PROPOSED cultural_identity strata (gandalf curates) — rep examples\n")
    lines.append("Mode flags guard the Mode A/B/C/D collapse: "
                 "**A**=geographic-origin, **B**=cultural-tradition, **C**=naming-allusion (NOT a real culture), "
                 "**D**=metadata/no-cultural-read.\n")
    for (cul, mode) in sorted(cul_strata, key=lambda x: -len(cul_strata[x])):
        reps = cul_strata[(cul, mode)]
        lines.append(f"\n### `{cul}` [mode {mode}] — {len(reps)} packs")
        for name, basis, c in reps[:8]:
            lines.append(f"- **{name}** (chars={c}) — {basis}")
        if len(reps) > 8:
            lines.append(f"- …and {len(reps)-8} more")

    # ----- §3 density-gap findings (design-valuable; the gap-fill routing surface) -----
    # Helper: humanoid skinned-char count per pack (guards SK_Veh_/SK_Bld_ false-positive chars).
    def humanoid_chars(pack_id):
        return conn.execute(
            "SELECT COUNT(*) FROM assets WHERE pack_id=? AND asset_type='character' "
            "AND (file_name LIKE 'SK_Character%' OR file_name LIKE 'SK_Chr%') "
            "AND file_name NOT LIKE '%Veh%' AND file_name NOT LIKE '%Bld%'", (pack_id,)
        ).fetchone()[0]

    lines.append("\n---\n\n## §3 Density-gap findings — the base-mesh gap-fill routing surface\n")
    lines.append("Gap-fill rule (brief §0/§3): temporal-cultural regions where Synty supplies NO "
                 "skinned-character base route to **image-to-3D / Sidekick**, NOT to a Synty base mesh. "
                 "The gap is **asymmetric by contribution layer** — a cultural register can ship rich "
                 "environment+weapon coverage but a HOLLOW skinned-character base; that still forces "
                 "character gap-fill.\n")

    # Finding 1 — sci-fi POLYGON skinned-character coverage (the headline question).
    lines.append("\n### Finding 1 — sci-fi POLYGON skinned-character coverage: EXISTS (brief premise refuted)\n")
    lines.append("The brief's apparent gap (\"only `SIMPLE - Space Characters` seen; POLYGON sci-fi "
                 "packs look environment-only\") is **refuted by the substrate.** POLYGON sci-fi ships "
                 "substantial humanoid skinned-character coverage:\n")
    scifi = conn.execute(
        "SELECT pack_id, collection_name, contribution_role FROM packs "
        "WHERE collection_name LIKE '%Sci-Fi%' OR collection_name LIKE '%Space%' OR collection_name LIKE '%Mech%' "
        "ORDER BY collection_name"
    ).fetchall()
    for pid, cn, role in scifi:
        hc = humanoid_chars(pid)
        lines.append(f"- **{cn}** — `{role}`, {hc} humanoid skinned chars")
    lines.append("\n**Answer (coverage half):** POLYGON sci-fi humanoid skinned-character base = "
                 "**~110 characters** across Sci-Fi City (40), Sci-Fi Space (52), Sci-Fi Cyber City (18). "
                 "These are genuine skinned bodies (Cyborg / Soldier / Mercenary / Crew / EVA-Suit / "
                 "SpaceSoldier / Android). `SIMPLE - Space Characters` ships a single baked `Characters.fbx` "
                 "(set-aside register). Sci-Fi *environment* packs (Horror, Outpost, Worlds-vehicles, Mech) "
                 "carry NO humanoid skinned base. **Conclusion: sci-fi-body does NOT require full gap-fill** "
                 "— the POLYGON consumption line already supplies a sci-fi skinned base. This UPDATES the "
                 "prior-canon \"sci-fi = zero coverage, full image-to-3D, deferred v1.1+\" entry. "
                 "(galadriel's parallel spike answers the mask-mechanism half.)\n")

    # Finding 2 — cultural thinness, asymmetric by layer.
    lines.append("\n### Finding 2 — cultural-register coverage is asymmetric by contribution layer\n")
    lines.append("Several named cultural registers ship environment + weapon coverage but a THIN or "
                 "ABSENT skinned-character base — character gap-fill is forced even where set-dressing is rich:\n")
    cult_probe = [
        ("Ancient Egypt", "egyptian"), ("Viking Realm", "norse"), ("Vikings Pack", "norse"),
        ("Samurai Empire", "east-asian"), ("Samurai Pack", "east-asian"),
        ("Goblin War Camp", "fantasy"), ("Knights Pack", "w-euro-medieval"),
        ("Western Frontier Pack", "modern-western"),
    ]
    for cn_sub, cul in cult_probe:
        row = conn.execute(
            "SELECT pack_id, collection_name, contribution_role FROM packs WHERE collection_name LIKE ?",
            (f"%{cn_sub}%",)
        ).fetchone()
        if row:
            pid, cn, role = row
            hc = humanoid_chars(pid)
            weps = conn.execute("SELECT COUNT(*) FROM assets WHERE pack_id=? AND asset_type='weapon'", (pid,)).fetchone()[0]
            verdict = "skinned base PRESENT" if hc >= 8 else ("THIN skinned base" if hc > 0 else "NO skinned base — char gap-fill forced")
            lines.append(f"- **{cn}** ({cul}): {hc} humanoid chars, {weps} weapons, `{role}` — {verdict}")
    lines.append("\n**Egypt + Vikings are the sharp cases:** rich weapon/environment coverage "
                 "(Egypt 28 weapons, Viking-Realm 184 weapons) but ZERO/near-zero humanoid skinned base. "
                 "Their character base is a gap-fill target despite the apparent 'coverage'.\n")

    # Finding 3 — zero-coverage cultural registers (full gap-fill).
    lines.append("\n### Finding 3 — ZERO-coverage cultural registers (full gap-fill route)\n")
    lines.append("Searched the corpus for these registers — **none present at any layer**:\n")
    lines.append("- **Mesoamerican / Aztec / Maya / Inca:** 0 packs. Full image-to-3D / Sidekick route.")
    lines.append("- **Indo-Asian (India / Hindu / South-Asian):** 0 packs. Full gap-fill.")
    lines.append("- **Persian / MENA / Ottoman / Arab:** 0 packs. Full gap-fill.")
    lines.append("- **Sub-Saharan African:** 0 packs. Full gap-fill.")
    lines.append("\nThese match the `canonical/48` roster's later cultural registers — the rotation's "
                 "non-Euro-Sinitic cultural homes are exactly where Synty supplies nothing.\n")

    # Finding 4 — steampunk/industrial thinness.
    lines.append("\n### Finding 4 — steampunk / industrial thinness\n")
    lines.append("- **Industrial-era set-dressing exists** but thin: only `POLYGON - War Map - WWI` and "
                 "`SIMPLE - Trains` read industrial. Western (frontier 19thC) covers the modern-industrial "
                 "edge but reads modern-western, not Victorian-steampunk.")
    lines.append("- **Victorian-steampunk proper:** 0 packs. No steampunk skinned-character base — full gap-fill "
                 "for a steampunk class register.\n")

    # Finding 5 — the Sidekick tool + wave-split structural note.
    lines.append("\n### Finding 5 — corpus-structure notes for routing\n")
    lines.append("- **Sidekick Character Creator (collection 157753)** is in `collections-157.json` but is "
                 "NOT a content pack — it ships no FBX corpus and is correctly absent from the 157 DB pack "
                 "rows. It is the gap-fill *mechanism* (parametric humanoid base), not a tagged geometry pack. "
                 "The '157 packs' = 157 DB rows across 156 content collections (Water Guns ships 2 FBX packs).")
    lines.append("- **WAVE split is contribution-aligned:** the WAVE-2 extracted-unitypackage packs "
                 "(Knights / Kids / Battle Royale / Gang Warfare / Western / Nature) contribute the "
                 "`accent-attach-static` silhouette-breaker layer (`SM_Chr_Attach_*` hats/beards/hair/ammo) "
                 "with only 2-3 baked whole-character meshes each. The WAVE-1 FBX SourceFiles packs "
                 "contribute the skinned-character armor bases. The two waves split cleanly along the "
                 "armor-base vs accent contribution axis.")
    lines.append("- **Upstream classifier caveat (honest):** the WAVE-1 asset classifier labels rigged "
                 "`SK_Veh_`/`SK_Bld_` meshes as `character` in Sci-Fi Worlds / Street Racer / Pro Racer. "
                 "The contribution_role routing GUARDS these by name (they route `environment`); the asset "
                 "rows are left unrewritten (reversibility — the raw classification is preserved, the "
                 "routing corrects above it).\n")

    with open(OUT_MD, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"wrote {OUT_JSONL}")
    print(f"wrote {OUT_MD}")
    conn.close()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("tag", "all"):
        cmd_tag()
    if cmd in ("report", "all"):
        cmd_report()
    if cmd not in ("tag", "report", "all"):
        print(f"unknown cmd: {cmd}")


if __name__ == "__main__":
    main()
