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
    python3 build_synty_catalogue_2026_06_17.py full       # populate all 136 FBX packs (WAVE 1; scans zips)
    python3 build_synty_catalogue_2026_06_17.py nonfbx     # populate the 21 extracted unitypackages (WAVE 2; scans loose FBX tree)
    python3 build_synty_catalogue_2026_06_17.py verify     # path-index integrity check only
    python3 build_synty_catalogue_2026_06_17.py queries    # run smoke queries

WAVE 2 (nonfbx mode) — added 2026-06-17 second populate pass.
    The 21 no-FBX packs were downloaded as Unity .unitypackage files (variant=Unity, has_fbx=0
    natively) and knight-rider extracted their meshes into a LOOSE FBX TREE (not zips) at
    ~/Games/synty-corpus/nonfbx_extracted/<PACK_FOLDER>/Assets/Synty/.../Models/*.fbx .
    The folder name carries the manifest download_id as its __<id> suffix; we map folder ->
    (collection_id, download_id) via the manifest. These packs index EXTRACTED meshes, not native
    FBX SourceFiles — provenance 'extracted-from-unitypackage' is stamped on every pack + asset.
    Idempotent: upsert-keyed on (collection_id, download_id) exactly as WAVE 1, so re-runs are
    clean and the WAVE-1 136 packs stay untouched.

    Naming-convention note (WAVE 2 differs from WAVE 1 SourceFiles packs):
    Unity-export FBX lack the SK_ skeletal prefix. Whole-character meshes are baked single FBX
    named  Characters.fbx / Generic_Characters.fbx / Characters_<Variant>.fbx  (monolithic
    appearance-units). Character attachments are  SM_(Gen_)Chr_Attach_*  (hats/hair/beards/masks/
    glasses) — the silhouette-breaker accent layer, classified armor_part + is_accent. The WAVE-2
    classifier (classify_asset_loose) handles these; the WAVE-1 classify_asset is left untouched.
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


# ---------------------------------------------------------------------------
# WAVE 2 — loose-FBX-tree (extracted unitypackage) corpus
# ---------------------------------------------------------------------------
NONFBX_DIR = os.path.join(CORPUS_ROOT, "nonfbx_extracted")

# The 21 extracted packs. The folder __<suffix> is the manifest download_id (the join key).
# We derive (collection_id, download_id) from the manifest at populate time — this map only
# carries the survey-accurate structural_class hint per the dispatch relevance notes:
#   - 'character_monolithic' : ships baked whole-character FBX (Characters.fbx / Generic_Characters.fbx)
#                              + SM_Chr_Attach_* accents. structural_class='monolithic'.
#   - 'environment'          : prop/env FBX, no character meshes (SIMPLE packs + MINI Fantasy*).
#   - 'ui_textureonly'       : INTERFACE HUD packs — texture-only / near-zero FBX.
# *MINI Fantasy is listed character-relevant in the dispatch, but the extracted tree ships ZERO
#  character meshes (all SM_Bld_/SM_Tile_/SM_Env_/SM_Prop_ + FX) — see populate report. We record
#  what EXISTS: it populates as environment. structural_class falls out of detect_structural_class
#  on the actual members regardless of this hint (hint informs the report only).
WAVE2_STRUCTURAL_HINT = {
    "1485274": "character_monolithic",  # POLYGON - Battle Royale Pack
    "1411544": "character_monolithic",  # POLYGON - Gang Warfare Pack
    "1624756": "character_monolithic",  # POLYGON - Kids Pack
    "1624761": "character_monolithic",  # POLYGON - Knights Pack
    "1162033": "character_monolithic",  # POLYGON - Vikings Pack
    "1158342": "character_monolithic",  # POLYGON - Western Pack
    "1226798": "character_monolithic",  # POLYGON MINI - Fantasy Pack (dispatch hint; tree ships 0 chars — see report)
    "1624768": "environment",           # POLYGON - Nature Pack (env/prop, no chars)
    "1174040": "environment",           # SIMPLE - Farm
    "1195038": "environment",           # SIMPLE - Port
    "1624802": "environment",           # SIMPLE - Props/Items/Icons
    "1624805": "environment",           # SIMPLE - Shop Interiors
    "1624807": "environment",           # SIMPLE - Space
    "1163104": "environment",           # SIMPLE - Temples
    "1195045": "environment",           # SIMPLE - Trains
    "1272892": "ui_textureonly",        # INTERFACE - Apocalypse HUD
    "2007482": "ui_textureonly",        # INTERFACE - Dark Fantasy HUD (6 flask props)
    "1616987": "ui_textureonly",        # INTERFACE - Fantasy Warrior HUD
    "1774637": "ui_textureonly",        # INTERFACE - Military Combat HUD
    "2241212": "ui_textureonly",        # INTERFACE - Sci-Fi Menus
    "1373855": "ui_textureonly",        # INTERFACE - Sci-Fi Soldier HUD
}

# Per-pack FBX counts from ~/Games/synty-corpus/extract.log — the integrity-check target.
WAVE2_EXPECTED_FBX = {
    "1272892": 0,    "2007482": 6,    "1616987": 0,    "1774637": 0,
    "2241212": 0,    "1373855": 0,    "1485274": 831,  "1411544": 945,
    "1624756": 1095, "1624761": 789,  "1624768": 691,  "1162033": 807,
    "1158342": 844,  "1226798": 892,  "1174040": 103,  "1195038": 84,
    "1624802": 716,  "1624805": 443,  "1624807": 114,  "1163104": 188,
    "1195045": 107,
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


# WAVE-2 Unity-export naming. Whole-character meshes (no SK_ prefix in Unity exports):
WAVE2_CHAR_MESH_RE = re.compile(
    r"^(Generic_Characters|Characters)(_[A-Za-z]+)?$", re.IGNORECASE
)
# Character attachment: SM_Chr_Attach_* or SM_Gen_Chr_Attach_* (accents — hats/hair/beard/mask/...).
WAVE2_CHR_ATTACH_RE = re.compile(r"^SM_(?:Gen_)?Chr_Attach_", re.IGNORECASE)
# SM_<sub> for Unity exports, tolerating the optional Gen_ infix and Synty's in-the-wild typos.
WAVE2_SM_SUBTOKEN_RE = re.compile(r"^SM_(?:Gen_)?([A-Za-z]+)_", re.IGNORECASE)

# OLDER SIMPLE-line bare-prefix convention (no SM_): environment vs prop families.
WAVE2_SIMPLE_ENV_RE = re.compile(
    r"^(Building|Env|Vehicle|road|Ground|Tree|Rock|Water|Bridge|Track|Rail|Platform|Tile)",
    re.IGNORECASE,
)
WAVE2_SIMPLE_PROP_RE = re.compile(
    r"^(Prop|Item|Items|Litter|Sign|signFolding|PowerBox|Billboard|VendingMachine|"
    r"Window|Door|Fence|Crate|Barrel|Box|Light|Lamp|Bench|Table|Chair|Shelf|Counter)",
    re.IGNORECASE,
)

# SM second-token -> asset_type for WAVE-2 Unity-export static meshes. Superset of SM_TYPE_MAP
# adding the loose-tree-specific tokens (tile/ui/character-attach handled before this map).
WAVE2_SM_TYPE_MAP = {
    "wep": "weapon", "weapon": "weapon",
    "item": "prop", "prop": "prop",
    "bld": "environment", "env": "environment", "veh": "environment",
    "fol": "environment", "tree": "environment", "tile": "environment",
    "generic": "environment", "gerneric": "environment",  # Synty typo seen in Gang Warfare
    "ui": "other", "fx": "other", "lightraycube": "other", "lightrayround": "other",
    "flame": "other", "beam": "other",
}


def classify_asset_loose(member_rel_path):
    """
    WAVE-2 classifier for loose-FBX-tree (extracted unitypackage) members.
    Returns (asset_type, slot, gender, is_accent, is_modular_part).

    Differs from classify_asset (WAVE 1, zip SourceFiles) because Unity-export FBX lack the
    SK_ skeletal prefix and bake characters into Characters.fbx / Generic_Characters.fbx, with
    accents as SM_(Gen_)Chr_Attach_*. None of the WAVE-2 packs ship modular per-slot body parts
    (none ship the _Texture_Mask), so is_modular_part is always 0 here.
    """
    fname = os.path.basename(member_rel_path)
    base = os.path.splitext(fname)[0]
    gender_m = GENDER_RE.search("_" + base + "_")  # tolerate Female/Male at token boundaries
    gender = gender_m.group(1).lower() if gender_m else None
    lower = base.lower()

    # Whole-character baked mesh (monolithic appearance-unit).
    if WAVE2_CHAR_MESH_RE.match(base):
        return "character", "whole_character", None, False, False

    # Character attachment (accent silhouette-breaker): hats, hair, beards, masks, glasses, etc.
    if WAVE2_CHR_ATTACH_RE.match(base):
        return "armor_part", None, gender, True, False

    # Static meshes (SM_ / SM_Gen_).
    sm_m = WAVE2_SM_SUBTOKEN_RE.match(base)
    if sm_m:
        sub = sm_m.group(1).lower()
        atype = WAVE2_SM_TYPE_MAP.get(sub, "prop")
        slot = "weapon" if atype == "weapon" else None
        return atype, slot, gender, False, False

    # OLDER Synty SIMPLE-line convention (no SM_ prefix; bare type token).
    # SIMPLE - Farm/Port/Space/Trains/Temples/Shop/Props use Building_/Vehicle_/Prop_/Env_/road/
    # SI_ (Simple Icons)/Items_/Sign*/etc. None ship characters. Map to environment/prop/other.
    if WAVE2_SIMPLE_ENV_RE.match(base):
        return "environment", None, None, False, False
    if WAVE2_SIMPLE_PROP_RE.match(base):
        return "prop", None, None, False, False

    # Props-pack 2D-icon family (SI_Letter/Symbol/Number/<X>Icon) — true 'other' (UI sprites-as-mesh).
    if re.match(r"^SI_(Letter|Symbol|Number|[A-Za-z]*Icon)", base, re.IGNORECASE):
        return "other", None, None, False, False
    # Shop-Interiors product prefix (SI_*) + Simple-Temples product prefix (ST_*): interior/temple
    # objects -> prop. (The SI_ collision with the Props-pack icon family is resolved by the icon
    # check above, which fires first.)
    if re.match(r"^(SI|ST)_", base, re.IGNORECASE):
        return "prop", None, None, False, False

    # FX / collision / animation / unrecognised loose meshes.
    if lower.startswith(("fx_", "sphere", "animations")):
        return "other", None, None, False, False

    return "other", None, gender, False, False


def loose_tree_fbx(pack_dir):
    """Return list of FBX member paths (relative to pack_dir) by walking the loose tree."""
    members = []
    for root, _dirs, files in os.walk(pack_dir):
        for fn in files:
            if fn.lower().endswith(".fbx"):
                full = os.path.join(root, fn)
                members.append(os.path.relpath(full, pack_dir))
    return sorted(members)


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


def wave2_folder_for_download(download_id):
    """The nonfbx_extracted folder whose name ends in __<download_id>."""
    if not os.path.isdir(NONFBX_DIR):
        return None
    for fn in os.listdir(NONFBX_DIR):
        if fn.endswith(f"__{download_id}") and os.path.isdir(os.path.join(NONFBX_DIR, fn)):
            return fn
    return None


def populate_pack_loose(conn, download_id, fbx_rows, avail, source_date):
    """
    WAVE-2 populate: index one extracted-unitypackage pack from its loose FBX tree.
    Upsert-keyed on (collection_id, download_id) — idempotent, additive to WAVE 1.
    Provenance: extracted-from-unitypackage (has_fbx reflects NATIVE availability from the
    manifest, which is 0 for these; the meshes indexed here are extracted, not native FBX).
    """
    # These packs are NOT FBX variants in the manifest, so fbx_rows lookup fails — we read the
    # collection identity directly from the manifest's Unity-variant row for this download_id.
    cid = cname = None
    with open(MANIFEST) as f:
        for line in f:
            r = json.loads(line)
            if r["download_id"] == download_id:
                cid = r["collection_id"]
                cname = r["collection_name"]
                break
    if cid is None:
        print(f"  ! download_id {download_id} not in manifest; skipping")
        return None

    folder = wave2_folder_for_download(download_id)
    if folder is None:
        print(f"  ! no extracted folder for download_id {download_id} ({cname}); skipping")
        return None
    pack_dir = os.path.join(NONFBX_DIR, folder)
    # corpus-relative path root for this pack (under nonfbx_extracted/<folder>/).
    pack_rel_root = os.path.join("nonfbx_extracted", folder)

    # Variant availability: native flags from the manifest (these are Unity-only: unity=1, fbx=0).
    a = avail.get(cid, {"fbx": 0, "unity": 1, "unreal": 0, "godot": 0})

    members = loose_tree_fbx(pack_dir)            # paths relative to pack_dir
    structural_class = detect_structural_class(members)  # WAVE-2 packs resolve monolithic (no modular slot parts)
    recolor = "whole_atlas_swap"                  # none ship _Texture_Mask (dispatch + verified)

    prov_note = (
        f"WAVE-2 extracted-from-unitypackage (variant=Unity, native has_fbx=0); meshes extracted "
        f"by knight-rider 2026-06-17 to nonfbx_extracted/{folder}. structural hint="
        f"{WAVE2_STRUCTURAL_HINT.get(download_id, 'unknown')}."
    )

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
            "recolor_scheme=?, source=?, source_date=?, notes=? WHERE pack_id=?",
            (cname, download_id, folder, pack_rel_root, None,
             a["fbx"], a["unity"], a["unreal"], a["godot"], structural_class,
             recolor, "synty-store-unitypackage", source_date, prov_note, pack_id),
        )
    else:
        cur = conn.execute(
            "INSERT INTO packs(collection_id, collection_name, download_id, zip_name, "
            "corpus_rel_path, size_mb, has_fbx, has_unity, has_unreal, has_godot, "
            "structural_class, recolor_scheme, source, source_date, added_at, notes) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (cid, cname, download_id, folder, pack_rel_root, None,
             a["fbx"], a["unity"], a["unreal"], a["godot"], structural_class,
             recolor, "synty-store-unitypackage", source_date, now_iso(), prov_note),
        )
        pack_id = cur.lastrowid

    # Assets — zip_rel_path holds the pack-root corpus-relative dir; member_path is tree-relative.
    n_assets = 0
    type_counts = {}
    for member in members:
        atype, slot, gender, is_accent, is_modular = classify_asset_loose(member)
        type_counts[atype] = type_counts.get(atype, 0) + 1
        conn.execute(
            "INSERT INTO assets(pack_id, zip_rel_path, member_path, file_name, asset_type, "
            "slot, is_accent, is_modular_part, gender, added_at, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (pack_id, pack_rel_root, member, os.path.basename(member), atype, slot,
             1 if is_accent else 0, 1 if is_modular else 0, gender, now_iso(),
             "extracted-from-unitypackage"),
        )
        n_assets += 1

    conn.commit()
    exp = WAVE2_EXPECTED_FBX.get(download_id)
    ok = "OK" if exp is None or exp == n_assets else f"MISMATCH(exp={exp})"
    chars = type_counts.get("character", 0)
    accents = sum(1 for m in members if classify_asset_loose(m)[3])
    print(f"  + {cname}: {structural_class}, {n_assets} fbx [{ok}], "
          f"chars={chars}, accents={accents}, types={type_counts}")
    return pack_id


def cmd_nonfbx():
    conn = connect()
    create_schema(conn)
    avail, fbx_rows, _ = load_variant_availability()
    source_date = "2026-06-17"
    print(f"=== WAVE 2: nonfbx populate ({len(WAVE2_EXPECTED_FBX)} extracted unitypackages) ===")
    for did in WAVE2_EXPECTED_FBX:
        populate_pack_loose(conn, did, fbx_rows, avail, source_date)
    conn.close()
    print("\n--- WAVE 2 loose-tree path-index integrity ---")
    verify_loose_paths()


def verify_loose_paths():
    """Every WAVE-2 asset path must resolve under nonfbx_extracted/; counts match extract.log."""
    conn = connect()
    misses = 0
    checked = 0
    count_fail = []
    rows = conn.execute(
        "SELECT pack_id, download_id, collection_name FROM packs WHERE source='synty-store-unitypackage'"
    ).fetchall()
    for pack_id, did, cname in rows:
        arows = conn.execute(
            "SELECT zip_rel_path, member_path FROM assets WHERE pack_id=?", (pack_id,)
        ).fetchall()
        n = len(arows)
        exp = WAVE2_EXPECTED_FBX.get(did)
        if exp is not None and exp != n:
            count_fail.append((cname, exp, n))
        # spot-check existence of every path (cheap; loose files on disk)
        for root_rel, member in arows:
            full = os.path.join(CORPUS_ROOT, root_rel, member)
            checked += 1
            if not os.path.isfile(full):
                misses += 1
                if misses <= 10:
                    print(f"  MISS: {full}")
    w2_packs = len(rows)
    w2_assets = conn.execute(
        "SELECT COUNT(*) FROM assets a JOIN packs p ON a.pack_id=p.pack_id "
        "WHERE p.source='synty-store-unitypackage'"
    ).fetchone()[0]
    print(f"WAVE2 packs={w2_packs}, assets={w2_assets}, paths-checked={checked}, path-misses={misses}")
    if count_fail:
        for c, e, g in count_fail:
            print(f"  COUNT-MISMATCH: {c} expected={e} got={g}")
    else:
        print("  per-pack FBX counts MATCH extract.log for all WAVE-2 packs")
    conn.close()
    return misses, count_fail


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
    # WAVE-1 packs only (zip-backed). WAVE-2 packs are folder-backed and verified by
    # verify_loose_paths(); their zip_name holds a folder, not a corpus zip.
    q = ("SELECT DISTINCT p.zip_name, p.collection_name FROM packs p "
         "WHERE p.source != 'synty-store-unitypackage'")
    if only_slice:
        ids = ",".join("?" for _ in SLICE_DOWNLOAD_IDS)
        q += f" AND p.download_id IN ({ids})"
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
    print("--- WAVE 1 (zip-backed) ---")
    verify_paths()
    print("--- WAVE 2 (loose-tree) ---")
    verify_loose_paths()


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

    print("\nQ8: packs + assets by WAVE (source provenance) — both waves landed")
    for r in conn.execute(
        "SELECT p.source, COUNT(DISTINCT p.pack_id) packs, COUNT(a.asset_id) assets "
        "FROM packs p LEFT JOIN assets a ON a.pack_id=p.pack_id GROUP BY p.source ORDER BY packs DESC"):
        print(f"   {r[1]:>4} packs  {r[2]:>7} assets  source={r[0]}")

    print("\nQ9: structural_class spanning both waves")
    for r in conn.execute("SELECT structural_class, COUNT(*) n FROM packs GROUP BY structural_class ORDER BY n DESC"):
        print(f"   {r[1]:>4}  {r[0]}")

    print("\nQ10: WAVE-2 (extracted) character meshes by pack")
    for r in conn.execute(
        "SELECT p.collection_name, COUNT(*) n FROM assets a JOIN packs p ON a.pack_id=p.pack_id "
        "WHERE p.source='synty-store-unitypackage' AND a.asset_type='character' "
        "GROUP BY p.collection_name ORDER BY n DESC"):
        print(f"   {r[1]:>3}  {r[0]}")

    print("\nQ11: WAVE-2 character ATTACHMENT accents (silhouette-breakers) by pack")
    for r in conn.execute(
        "SELECT p.collection_name, COUNT(*) n FROM assets a JOIN packs p ON a.pack_id=p.pack_id "
        "WHERE p.source='synty-store-unitypackage' AND a.is_accent=1 "
        "GROUP BY p.collection_name ORDER BY n DESC"):
        print(f"   {r[1]:>4}  {r[0]}")

    conn.close()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "slice"
    {
        "schema": cmd_schema,
        "slice": cmd_slice,
        "full": cmd_full,
        "nonfbx": cmd_nonfbx,
        "verify": cmd_verify,
        "queries": cmd_queries,
    }.get(cmd, lambda: print(f"unknown cmd: {cmd}"))()


if __name__ == "__main__":
    main()
