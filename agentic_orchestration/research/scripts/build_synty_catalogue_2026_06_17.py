#!/usr/bin/env python3
"""
build_synty_catalogue_2026_06_17.py — elrond (data steward)

Builds / populates the Synty gear-substrate catalogue: a queryable SQLite index
of the downloaded Synty FBX corpus. METADATA + FILESYSTEM PATH INDEX ONLY —
bytes stay on disk in the zips; the DB never holds mesh bytes.

Dispatch: agentic_orchestration/dispatches/2026-06-17-elrond-synty-catalogue.md
Substrate architecture: canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md §7.1
Galadriel slice verification: research/catalogue/synty-recon-2026-06-16/slice-verification-2026-06-17.md

Design decisions (documented in MIGRATION note + agent report):
- SEPARATE DB (synty_catalogue.db) rather than extending research/curated/catalogue.db.
  Rationale: the existing catalogue is a 2D-sprite STYLE-RUBRIC catalogue (six-axis
  pixel-art register scoring, embodiment tags, abstraction groupings). The Synty corpus
  is a 3D FBX MESH catalogue with an orthogonal shape: per-mesh slot taxonomy, license
  incorporation ledger, structural_class, filesystem path index. Forcing 3D-mesh fields
  onto the sprite-rubric tables (or vice versa) would muddy both. Vendor-catalogue
  precedent already separates concerns by folder; we separate by DB file here because the
  schema overlap is near-zero. Cross-DB reference is by stable string keys (collection_id).

- SLICE-FIRST: a representative slice is populated + path-verified and surfaced as a
  checkpoint BEFORE the full 136-pack populate (Gate-1 jack-ryan 2026-06-17 sequencing fix).

Run modes:
    python3 build_synty_catalogue_2026_06_17.py schema    # (re)create schema only
    python3 build_synty_catalogue_2026_06_17.py slice     # populate + verify the slice, STOP (checkpoint)
    python3 build_synty_catalogue_2026_06_17.py full       # populate all 136 FBX packs
    python3 build_synty_catalogue_2026_06_17.py verify     # path-index integrity check only
    python3 build_synty_catalogue_2026_06_17.py queries    # run smoke queries
"""

import json
import os
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HOME = os.path.expanduser("~")
CORPUS_ROOT = os.path.join(HOME, "Games", "synty-corpus")
FBX_DIR = os.path.join(CORPUS_ROOT, "fbx")
COLLAB_ROOT = os.path.join(HOME, "Games", "reincarnated-collaboration")
RECON_DIR = os.path.join(
    COLLAB_ROOT, "agentic_orchestration", "research", "catalogue", "synty-recon-2026-06-16"
)
MANIFEST = os.path.join(RECON_DIR, "full-fbx-variant-manifest.jsonl")
DB_PATH = os.path.join(
    COLLAB_ROOT, "agentic_orchestration", "research", "curated", "synty_catalogue.db"
)

SCHEMA_VERSION = "1.0"

# The slice: representative whole-character packs spanning distinct themes,
# the modular per-slot pack, and a dedicated weapon pack. Keyed by download_id
# (the FBX-variant download id == the join key to the manifest and the zip name).
SLICE_DOWNLOAD_IDS = {
    "1462397": "POLYGON - Adventure Pack",                 # monolithic, weapon-bearing (adventure theme)
    "1485355": "POLYGON - Fantasy Kingdom Pack",           # monolithic (fantasy-kingdom theme)
    "1624702": "POLYGON - Samurai Pack",                   # monolithic (samurai theme)
    "1624700": "POLYGON - Modular Fantasy Hero Characters",# modular per-slot lane
    "1462543": "POLYGON - Bow and Crossbow",               # dedicated weapon pack
}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Synty naming-convention classifier
# ---------------------------------------------------------------------------
# Synty prefixes (consistent across the corpus, verified on the slice):
#   SK_  = skeletal mesh  -> rigged (characters, rigged weapons)
#   SM_  = static mesh    -> sub-typed by the SECOND token:
#            SM_Wep_  -> weapon        SM_Item_ -> small item/prop
#            SM_Prop_ -> prop          SM_Bld_  -> building/environment
#            SM_Env_  -> environment   SM_Veh_  -> vehicle
#   Chr_ = modular character part (StaticMeshes variant), SK_Chr_ = rigged variant
#
# The modular pack's per-slot parts encode the SLOT in the token after Chr_.

# Modular slot token -> canonical slot name (the clean set gandalf designs against).
MODULAR_SLOT_MAP = {
    "head": "head",
    "headcoverings": "head_covering",
    "helmetattachment": "helmet_accent",
    "hair": "hair",
    "facialhair": "facial_hair",
    "eyebrow": "eyebrow",
    "ear": "ear",
    "torso": "chest",
    "hips": "hips",
    "legleft": "leg_l",
    "legright": "leg_r",
    "armupperleft": "arm_upper_l",
    "armupperright": "arm_upper_r",
    "armlowerleft": "arm_lower_l",
    "armlowerright": "arm_lower_r",
    "handleft": "hand_l",
    "handright": "hand_r",
    "shoulderattachleft": "shoulder_accent_l",
    "shoulderattachright": "shoulder_accent_r",
    "elbowattachleft": "elbow_accent_l",
    "elbowattachright": "elbow_accent_r",
    "kneeattachleft": "knee_accent_l",
    "kneeattachright": "knee_accent_r",
    "hipsattachment": "hips_accent",
    "backattachment": "back_accent",
}

# Accent slots (mount to the All_NN_ named sockets per galadriel §2). Used to tag
# is_accent so gandalf/rocket can address the silhouette-breaker layer (§3.6).
ACCENT_SLOTS = {
    "head_covering", "helmet_accent", "shoulder_accent_l", "shoulder_accent_r",
    "elbow_accent_l", "elbow_accent_r", "knee_accent_l", "knee_accent_r",
    "hips_accent", "back_accent",
}

CHR_TOKEN_RE = re.compile(r"(?:SK_)?Chr_([A-Za-z]+)_", re.IGNORECASE)
SM_SUBTOKEN_RE = re.compile(r"SM_([A-Za-z]+)_", re.IGNORECASE)
GENDER_RE = re.compile(r"_(Female|Male)_", re.IGNORECASE)

# SM_ second-token -> asset_type for static meshes
SM_TYPE_MAP = {
    "wep": "weapon",
    "weapon": "weapon",
    "item": "prop",
    "prop": "prop",
    "bld": "environment",
    "env": "environment",
    "veh": "environment",
    "fol": "environment",   # foliage
    "tree": "environment",
}


def classify_asset(member_path):
    """
    Classify one FBX member path into (asset_type, slot, gender, is_accent, is_modular_part).
    asset_type in {character, weapon, armor_part, prop, environment, other}.
    slot is nullable; for monolithic characters slot='whole_character'.
    """
    fname = os.path.basename(member_path)
    base = os.path.splitext(fname)[0]
    gender_m = GENDER_RE.search(base)
    gender = gender_m.group(1).lower() if gender_m else None

    lower = base.lower()

    # Cape sub-meshes (page-1 named-character lane ships SK_Chr_<Name>_Cape_NN) — a back accent.
    if "_cape" in lower and lower.startswith(("sk_chr", "chr_")):
        return "armor_part", "back_accent", gender, True, False

    # Modular per-slot part?  (SK_)Chr_<Slot>_...  — a part ONLY when <Slot> is a KNOWN
    # modular slot token. Bare Chr_<Name> (e.g. SK_Chr_King) is a baked named character,
    # NOT a modular part, and falls through to the whole-character branch below.
    chr_m = CHR_TOKEN_RE.match(base)
    if chr_m:
        token = chr_m.group(1).lower()
        slot = MODULAR_SLOT_MAP.get(token)
        if slot is not None:
            is_accent = slot in ACCENT_SLOTS
            return "armor_part", slot, gender, is_accent, True
        # Known accent-prop token families that are NOT per-slot body parts.
        if token in ("attachments", "attach"):
            return "armor_part", None, gender, True, False
        # else fall through: Chr_<Name> baked character handled below.

    # Skeletal whole character: SK_Character_* / SK_Chr_<Name>  (page-1 baked named chars)
    if lower.startswith(("sk_character", "sk_chr", "chr_")):
        return "character", "whole_character", gender, False, False
    if lower.startswith("sk_"):
        # other skeletal (rigged weapons like Rigged_Bow handled below)
        if any(w in lower for w in ("wep", "weapon", "sword", "bow", "crossbow", "axe", "blade")):
            return "weapon", None, gender, False, False
        return "character", "whole_character", gender, False, False

    # Rigged_* test/weapon meshes (weapon packs)
    if lower.startswith("rigged_"):
        return "weapon", None, gender, False, False

    # Static meshes: SM_<sub>_...
    sm_m = SM_SUBTOKEN_RE.match(base)
    if sm_m:
        sub = sm_m.group(1).lower()
        atype = SM_TYPE_MAP.get(sub, "prop")
        slot = None
        if atype == "weapon":
            slot = "weapon"
        return atype, slot, gender, False, False

    return "other", None, gender, False, False


def zip_member_fbx(zip_path):
    """Return list of FBX member paths inside a zip via `unzip -l` (no extraction)."""
    out = subprocess.run(
        ["unzip", "-l", zip_path], capture_output=True, text=True, check=True
    ).stdout
    members = []
    for line in out.splitlines():
        # unzip -l columns: length  date  time  name
        m = re.match(r"\s*\d+\s+[\d-]+\s+[\d:]+\s+(.+)$", line)
        if m:
            name = m.group(1)
            if name.lower().endswith(".fbx"):
                members.append(name)
    return members


def zip_texture_masks(zip_path):
    """Return (mask_paths, palette_variant_atlases) — the recolor levers."""
    out = subprocess.run(
        ["unzip", "-l", zip_path], capture_output=True, text=True, check=True
    ).stdout
    masks, atlases = [], []
    for line in out.splitlines():
        m = re.match(r"\s*\d+\s+[\d-]+\s+[\d:]+\s+(.+)$", line)
        if not m:
            continue
        name = m.group(1)
        low = name.lower()
        if low.endswith(".png") and "_mask" in low and ".swatch" not in low:
            masks.append(name)
        elif low.endswith(".png") and re.search(r"_texture_\d+_[abc]\.png$", low) and ".swatch" not in low:
            atlases.append(name)
    return masks, atlases


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS schema_meta (
    version          TEXT PRIMARY KEY,
    applied_at       TEXT NOT NULL,
    description      TEXT NOT NULL,
    migration_script TEXT
) STRICT;

-- One row per Synty collection that ships an FBX SourceFiles pack.
CREATE TABLE IF NOT EXISTS packs (
    pack_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_id        TEXT NOT NULL,          -- Synty collection_id (cross-DB stable key)
    collection_name      TEXT NOT NULL,
    download_id          TEXT NOT NULL,          -- FBX-variant download id (== zip name suffix)
    -- A collection MAY ship more than one FBX download (e.g. Water Guns: two pack versions).
    -- Pack identity is (collection_id, download_id), NOT collection_id alone.
    zip_name             TEXT NOT NULL,          -- corpus zip filename
    corpus_rel_path      TEXT NOT NULL,          -- path relative to corpus root (fbx/<zip>)
    size_mb              REAL,

    -- Variant availability (from the full enumeration manifest).
    has_fbx              INTEGER NOT NULL DEFAULT 1 CHECK (has_fbx IN (0,1)),
    has_unity            INTEGER NOT NULL DEFAULT 0 CHECK (has_unity IN (0,1)),
    has_unreal           INTEGER NOT NULL DEFAULT 0 CHECK (has_unreal IN (0,1)),
    has_godot            INTEGER NOT NULL DEFAULT 0 CHECK (has_godot IN (0,1)),

    structural_class     TEXT NOT NULL DEFAULT 'monolithic'
        CHECK (structural_class IN ('monolithic', 'modular')),

    -- Recolor lever class (galadriel slice-verification 2026-06-17 §3.3 bifurcation):
    --   per_region_mask : ships _Texture_Mask (modular pack) -> 5-zone per-region recolor
    --   whole_atlas_swap: ships whole-atlas palette swaps only (page-1 named packs)
    --   unknown         : not yet inspected
    recolor_scheme       TEXT NOT NULL DEFAULT 'unknown'
        CHECK (recolor_scheme IN ('per_region_mask', 'whole_atlas_swap', 'unknown')),

    -- License incorporation ledger (Matt stipulation: assets not INCORPORATED before
    -- the Synty-Pass subscription lapses cannot be used afterward).
    incorporation_status TEXT NOT NULL DEFAULT 'NOT_INCORPORATED'
        CHECK (incorporation_status IN ('NOT_INCORPORATED', 'INCORPORATED')),
    incorporated_season  TEXT,                   -- season/build stamp when INCORPORATED
    incorporated_at      TEXT,                   -- ISO-8601 timestamp when INCORPORATED

    source               TEXT NOT NULL DEFAULT 'synty-store',
    source_date          TEXT NOT NULL,          -- corpus download date
    added_at             TEXT NOT NULL,
    notes                TEXT,
    UNIQUE (collection_id, download_id)
) STRICT;

-- One row per usable mesh FBX inside a pack. Bytes are NOT stored; path indexes the zip member.
CREATE TABLE IF NOT EXISTS assets (
    asset_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    pack_id              INTEGER NOT NULL REFERENCES packs(pack_id),

    -- Filesystem path index: the zip on disk + the member path inside it.
    -- The bytes live at  <corpus_root>/<zip_rel_path> :: <member_path>  (never in the DB).
    zip_rel_path         TEXT NOT NULL,          -- e.g. fbx/POLYGON_-_Adventure_Pack__1462397.zip
    member_path          TEXT NOT NULL,          -- path inside the zip
    file_name            TEXT NOT NULL,

    asset_type           TEXT NOT NULL CHECK (asset_type IN (
        'character', 'weapon', 'armor_part', 'prop', 'environment', 'other'
    )),

    -- Slot taxonomy handling BOTH lanes:
    --   monolithic character -> 'whole_character'
    --   modular per-slot part -> canonical slot (chest/hips/leg_l/.../shoulder_accent_r/...)
    --   weapon                -> 'weapon'   prop/env -> NULL
    slot                 TEXT,                   -- canonical slot, nullable
    is_accent            INTEGER NOT NULL DEFAULT 0 CHECK (is_accent IN (0,1)),
    is_modular_part      INTEGER NOT NULL DEFAULT 0 CHECK (is_modular_part IN (0,1)),
    gender               TEXT CHECK (gender IN ('male', 'female') OR gender IS NULL),

    -- Distinctiveness hook (galadriel scores later per gandalf §7.4). NULLABLE — DO NOT populate.
    distinctiveness_score REAL,

    added_at             TEXT NOT NULL,
    notes                TEXT
) STRICT;

CREATE INDEX IF NOT EXISTS idx_assets_pack    ON assets(pack_id);
CREATE INDEX IF NOT EXISTS idx_assets_type    ON assets(asset_type);
CREATE INDEX IF NOT EXISTS idx_assets_slot    ON assets(slot);

-- Recolor mask / palette-atlas textures per pack (the _Texture_Mask recolor lever).
-- Channel-region mapping populated from galadriel's slice verification where reported.
CREATE TABLE IF NOT EXISTS textures (
    texture_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    pack_id              INTEGER NOT NULL REFERENCES packs(pack_id),
    zip_rel_path         TEXT NOT NULL,
    member_path          TEXT NOT NULL,
    texture_role         TEXT NOT NULL CHECK (texture_role IN (
        'region_mask', 'palette_atlas', 'base_atlas', 'other'
    )),
    -- Channel->region mapping (galadriel slice-verification 2026-06-17 §3.1), JSON; nullable
    -- until verified per-pack. Modular pack: 5 discrete RGB-corner zones.
    channel_region_map   TEXT,
    added_at             TEXT NOT NULL,
    notes                TEXT
) STRICT;

CREATE INDEX IF NOT EXISTS idx_textures_pack ON textures(pack_id);
"""


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn):
    conn.executescript(SCHEMA_SQL)
    conn.execute(
        "INSERT OR IGNORE INTO schema_meta(version, applied_at, description, migration_script) VALUES (?,?,?,?)",
        (
            SCHEMA_VERSION,
            now_iso(),
            "Initial Synty gear-substrate catalogue: packs + assets + textures. "
            "Metadata + filesystem path index only; bytes stay on disk.",
            os.path.basename(__file__),
        ),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Manifest -> variant availability map (collection_id -> {fbx,unity,unreal,godot})
# ---------------------------------------------------------------------------
def load_variant_availability():
    avail = {}            # collection_id -> dict of variant flags
    fbx_rows = {}         # download_id -> manifest row (FBX variant)
    coll_name = {}        # collection_id -> name
    with open(MANIFEST) as f:
        for line in f:
            row = json.loads(line)
            cid = row["collection_id"]
            coll_name[cid] = row["collection_name"]
            v = row["variant"].lower()
            a = avail.setdefault(cid, {"fbx": 0, "unity": 0, "unreal": 0, "godot": 0})
            if v == "fbx":
                a["fbx"] = 1
                fbx_rows[row["download_id"]] = row
            elif v == "unity":
                a["unity"] = 1
            elif v == "unreal":
                a["unreal"] = 1
            elif v == "godot":
                a["godot"] = 1
    return avail, fbx_rows, coll_name


def zip_name_for_download(download_id):
    """The corpus zip whose name ends in __<download_id>.zip."""
    for fn in os.listdir(FBX_DIR):
        if fn.endswith(f"__{download_id}.zip"):
            return fn
    return None


def detect_structural_class(members):
    """
    A pack is 'modular' only if it ships genuine per-slot body parts in bulk —
    Chr_<KnownSlot> across many slots. Counting the bare Chr_ prefix mis-flags
    packs that merely ship Chr_Attachments accent props (e.g. Fantasy Kingdom).
    """
    slot_parts = 0
    for m in members:
        cm = CHR_TOKEN_RE.match(os.path.basename(m))
        if cm and cm.group(1).lower() in MODULAR_SLOT_MAP:
            slot_parts += 1
    return "modular" if slot_parts >= 20 else "monolithic"


def populate_pack(conn, download_id, fbx_rows, avail, source_date):
    row = fbx_rows.get(download_id)
    if row is None:
        print(f"  ! download_id {download_id} not an FBX variant in manifest; skipping")
        return None
    cid = row["collection_id"]
    cname = row["collection_name"]
    zip_name = zip_name_for_download(download_id)
    if zip_name is None:
        print(f"  ! no zip on disk for download_id {download_id} ({cname}); skipping")
        return None
    zip_path = os.path.join(FBX_DIR, zip_name)
    zip_rel = os.path.join("fbx", zip_name)
    corpus_rel = zip_rel
    a = avail.get(cid, {"fbx": 1, "unity": 0, "unreal": 0, "godot": 0})

    members = zip_member_fbx(zip_path)
    structural_class = detect_structural_class(members)
    masks, atlases = zip_texture_masks(zip_path)
    recolor = "per_region_mask" if masks else ("whole_atlas_swap" if atlases or structural_class == "monolithic" else "unknown")

    # Upsert pack — identity is (collection_id, download_id); a collection may ship >1 FBX pack.
    cur = conn.execute(
        "SELECT pack_id FROM packs WHERE collection_id = ? AND download_id = ?", (cid, download_id)
    )
    existing = cur.fetchone()
    if existing:
        pack_id = existing[0]
        conn.execute("DELETE FROM assets WHERE pack_id = ?", (pack_id,))
        conn.execute("DELETE FROM textures WHERE pack_id = ?", (pack_id,))
        conn.execute(
            "UPDATE packs SET collection_name=?, download_id=?, zip_name=?, corpus_rel_path=?, "
            "size_mb=?, has_fbx=?, has_unity=?, has_unreal=?, has_godot=?, structural_class=?, "
            "recolor_scheme=?, source_date=? WHERE pack_id=?",
            (cname, download_id, zip_name, corpus_rel, row.get("size_mb"),
             a["fbx"], a["unity"], a["unreal"], a["godot"], structural_class,
             recolor, source_date, pack_id),
        )
    else:
        cur = conn.execute(
            "INSERT INTO packs(collection_id, collection_name, download_id, zip_name, "
            "corpus_rel_path, size_mb, has_fbx, has_unity, has_unreal, has_godot, "
            "structural_class, recolor_scheme, source_date, added_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (cid, cname, download_id, zip_name, corpus_rel, row.get("size_mb"),
             a["fbx"], a["unity"], a["unreal"], a["godot"], structural_class,
             recolor, source_date, now_iso()),
        )
        pack_id = cur.lastrowid

    # Assets
    n_assets = 0
    for member in members:
        atype, slot, gender, is_accent, is_modular = classify_asset(member)
        conn.execute(
            "INSERT INTO assets(pack_id, zip_rel_path, member_path, file_name, asset_type, "
            "slot, is_accent, is_modular_part, gender, added_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (pack_id, zip_rel, member, os.path.basename(member), atype, slot,
             1 if is_accent else 0, 1 if is_modular else 0, gender, now_iso()),
        )
        n_assets += 1

    # Textures (masks + palette atlases)
    for m in masks:
        conn.execute(
            "INSERT INTO textures(pack_id, zip_rel_path, member_path, texture_role, channel_region_map, added_at, notes) "
            "VALUES (?,?,?,?,?,?,?)",
            (pack_id, zip_rel, m, "region_mask",
             json.dumps({
                 "scheme": "synty_5zone_rgb_corner",
                 "zones": {"WHITE": "R+G+B", "CYAN": "G+B", "BLUE": "B", "YELLOW": "R+G", "MAGENTA": "R+B"},
                 "source": "galadriel slice-verification 2026-06-17 §3.1",
                 "semantic_labels": "expected primary/secondary/metal/leather/accent — unrendered (galadriel §5 caveat)"
             }),
             now_iso(), "per-region recolor mask"),
        )
    for atl in atlases:
        conn.execute(
            "INSERT INTO textures(pack_id, zip_rel_path, member_path, texture_role, added_at) VALUES (?,?,?,?,?)",
            (pack_id, zip_rel, atl, "palette_atlas", now_iso()),
        )

    conn.commit()
    print(f"  + {cname}: {structural_class}, {n_assets} fbx assets, "
          f"{len(masks)} masks, {len(atlases)} palette-atlases, recolor={recolor}")
    return pack_id


def cmd_schema():
    conn = connect()
    create_schema(conn)
    print(f"schema {SCHEMA_VERSION} applied at {DB_PATH}")
    conn.close()


def cmd_slice():
    conn = connect()
    create_schema(conn)
    avail, fbx_rows, _ = load_variant_availability()
    source_date = "2026-06-17"
    print("=== SLICE-FIRST checkpoint populate ===")
    for did in SLICE_DOWNLOAD_IDS:
        populate_pack(conn, did, fbx_rows, avail, source_date)
    conn.close()
    print("\n--- slice path-index integrity ---")
    verify_paths(only_slice=True)


def cmd_full():
    conn = connect()
    create_schema(conn)
    avail, fbx_rows, _ = load_variant_availability()
    source_date = "2026-06-17"
    print(f"=== FULL populate: {len(fbx_rows)} FBX packs ===")
    for did in sorted(fbx_rows.keys()):
        populate_pack(conn, did, fbx_rows, avail, source_date)
    conn.close()
    print("\n--- full path-index integrity ---")
    verify_paths()


def verify_paths(only_slice=False):
    conn = connect()
    q = "SELECT DISTINCT p.zip_name, p.collection_name FROM packs p"
    if only_slice:
        ids = ",".join("?" for _ in SLICE_DOWNLOAD_IDS)
        q += f" WHERE p.download_id IN ({ids})"
        rows = conn.execute(q, tuple(SLICE_DOWNLOAD_IDS)).fetchall()
    else:
        rows = conn.execute(q).fetchall()
    misses = []
    for zip_name, cname in rows:
        if not os.path.isfile(os.path.join(FBX_DIR, zip_name)):
            misses.append((zip_name, cname))
    total_assets = conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
    total_packs = conn.execute("SELECT COUNT(*) FROM packs").fetchone()[0]
    print(f"packs={total_packs}, assets={total_assets}, zip-misses={len(misses)}")
    for z, c in misses:
        print(f"  MISS: {z} ({c})")
    conn.close()
    return len(misses)


def cmd_verify():
    verify_paths()


def cmd_queries():
    conn = connect()
    print("=== SMOKE QUERIES ===\n")

    print("Q1: whole-character appearance-units (monolithic), by pack")
    for r in conn.execute(
        "SELECT p.collection_name, COUNT(*) n FROM assets a JOIN packs p ON a.pack_id=p.pack_id "
        "WHERE a.slot='whole_character' GROUP BY p.collection_name ORDER BY n DESC LIMIT 12"):
        print(f"   {r[1]:>4}  {r[0]}")

    print("\nQ2: modular torso (chest) parts")
    for r in conn.execute(
        "SELECT p.collection_name, a.file_name, a.gender FROM assets a JOIN packs p ON a.pack_id=p.pack_id "
        "WHERE a.slot='chest' AND a.is_modular_part=1 LIMIT 8"):
        print(f"   {r[0]} :: {r[1]} ({r[2]})")
    n = conn.execute("SELECT COUNT(*) FROM assets WHERE slot='chest' AND is_modular_part=1").fetchone()[0]
    print(f"   ...{n} modular chest parts total")

    print("\nQ3: all weapons (count by pack, top 12)")
    for r in conn.execute(
        "SELECT p.collection_name, COUNT(*) n FROM assets a JOIN packs p ON a.pack_id=p.pack_id "
        "WHERE a.asset_type='weapon' GROUP BY p.collection_name ORDER BY n DESC LIMIT 12"):
        print(f"   {r[1]:>4}  {r[0]}")

    print("\nQ4: packs still NOT_INCORPORATED (count)")
    n = conn.execute("SELECT COUNT(*) FROM packs WHERE incorporation_status='NOT_INCORPORATED'").fetchone()[0]
    print(f"   {n} packs NOT_INCORPORATED")

    print("\nQ5: per-region-mask packs (the rich restyle lane)")
    for r in conn.execute(
        "SELECT collection_name, recolor_scheme, structural_class FROM packs WHERE recolor_scheme='per_region_mask'"):
        print(f"   {r[0]} ({r[1]}, {r[2]})")

    print("\nQ6: accent parts (silhouette-breakers) by slot")
    for r in conn.execute(
        "SELECT slot, COUNT(*) n FROM assets WHERE is_accent=1 GROUP BY slot ORDER BY n DESC"):
        print(f"   {r[1]:>4}  {r[0]}")

    print("\nQ7: asset_type distribution (whole corpus)")
    for r in conn.execute("SELECT asset_type, COUNT(*) n FROM assets GROUP BY asset_type ORDER BY n DESC"):
        print(f"   {r[1]:>6}  {r[0]}")

    conn.close()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "slice"
    {
        "schema": cmd_schema,
        "slice": cmd_slice,
        "full": cmd_full,
        "verify": cmd_verify,
        "queries": cmd_queries,
    }.get(cmd, lambda: print(f"unknown cmd: {cmd}"))()


if __name__ == "__main__":
    main()
