#!/usr/bin/env python3
"""
gd_arz_adapter_2026_07_24.py — GD .arz -> normalized exact-fields schema (GD-SLICE, width one).

RUN CHARTER
    gandalf RUN-CONDUCTOR, `agentic_orchestration/gandalf/notes/2026-07-24-gd-slice-run-charter.md`.
    Prove the TRUE-SOURCES pipe end-to-end at width one:
    GD .arz primary source -> GD adapter -> ONE normalized exact-fields schema (TSR-2) carrying
    player-facing canonical values + raw provenance columns (TSR-1) -> corpus rows for
    Flames of Ignaffar, byte-verified against .arz ground truth (TSR-4 tier-1 anchor + tier-2 asserts).

    VERIFIED CLAIM CEILING: "the GD adapter path is proven at width one." NOT coverage.

FORMAT TRUTH (productionized from legolas probe `2026-07-23-gd-arz-extraction-probe.md` §0)
    TQIT variant (magic=2). 24-byte header:
      magic(u16) version(u16) rt_offset(i32) rt_size(i32) rt_count(i32) st_offset(i32) st_size(i32)
    Record-data block runs [24 .. rt_offset). Record-table entries are VARIABLE-length (embedded LP_string):
      name_id(i32) recordType(LP_string: i32 len + bytes) data_offset(i32) comp_size(i32) decomp_size(i32) timestamp(i64)
    Compression: LZ4 BLOCK (not frame/zlib): lz4.block.decompress(blob, uncompressed_size=decomp_size).
    DBR field within decompressed record: type(u16) count(u16) key_id(u32) values[count x 4 bytes].
      type IDs: 0=int32, 1=float32, 2=uint32 string-table index, 3=bool(uint32). Flat shared string table.
    String table: [st_offset .. st_offset+st_size), each entry = i32 len + bytes (index 0-based order).

SCOPE (charter §1, frozen)
    File:   ~/Games/vendor/grim-dawn/gdx1/database/GDX1.arz
    Record: records/skills/playerclass07/purifyingflame1.dbr  (Flames of Ignaffar)
    .arc localization parsing is NOT in scope (G4: skillBitmapName workaround + pending-flag).

GATES
    G2 adapter  : FoI rows land; tier-2 in-pipe asserts green on EVERY row
                  (non-null; monotonic rank arrays where field-class implies monotonicity; range bounds).
    G3 anchor   : landed values BYTE-MATCH probe §2 oracle. ANY mismatch = HALT-diagnose (name the layer),
                  never tolerance-fudge.
    G4 provenance: raw columns populated (field name, raw value, record path, source file+version);
                  display name via skillBitmapName workaround, .arc tag-bridge flagged pending.

USAGE
    python3 gd_arz_adapter_2026_07_24.py --verify-only   # parse + adapter + G3 byte-match, NO DB writes
    python3 gd_arz_adapter_2026_07_24.py --dry-run        # + schema/row plan, NO DB writes
    python3 gd_arz_adapter_2026_07_24.py                  # apply: backup, DDL, land rows, verify
"""
import io
import struct
import sqlite3
import sys
import hashlib
import shutil
import datetime
import pathlib

import lz4.block

# ------------------------------------------------------------------ paths + constants
HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parent / "curated" / "corpus.db"
ARZ = pathlib.Path("~/Games/vendor/grim-dawn/gdx1/database/GDX1.arz").expanduser()
RECORD_PATH = "records/skills/playerclass07/purifyingflame1.dbr"
SOURCE_FILE = "GDX1.arz"
KIT_ID = "gd-flames-of-ignaffar-purifier"   # existing canon_corpus kit (join target)
GAME = "gd"
DISPLAY_NAME = "Flames of Ignaffar"          # via skillBitmapName workaround (G4)
NAME_PROVENANCE_FLAG = (
    "display name derived from skillBitmapName='skillicon_flamesofignaffar1up.tex' "
    "(probe §3 workaround); authoritative .arc tag-bridge tagGDX1Class07SkillName04A PENDING "
    "(.arc parsing not in scope)"
)
SCHEMA_VERSION = "gd-slice-exact-fields-2026-07-24"
RUN_DATE = "2026-07-24"

# G3 oracle — probe note `2026-07-23-gd-arz-extraction-probe.md` §2. Byte-exact. NO tolerance.
ORACLE_RANK_COUNT = 26          # skillMaxLevel 16 + 10 ultimate (skillUltimateLevel 26)
# rank-array anchors: field -> {rank_index_1based: value}
ORACLE_RANK = {
    "offensiveFireMin":     {1: 8.0,  16: 129.0, 26: 262.0},
    "offensiveFireMax":     {1: 18.0, 16: 157.0, 26: 306.0},
    "offensiveSlowFireMin": {1: 8.0,  16: 211.0, 26: 382.0},   # burn DoT
    "skillManaCost":        {1: 7.0,  16: 39.0,  26: 69.0},
    "weaponDamagePct":      {1: 9.0,  16: 42.0,  26: 58.0},
}
# static (scalar) anchors
ORACLE_STATIC = {
    "maxRange": 9.1,
    "endWidth": 4.5,
    "startWidth": 2.2,
    "timeBetweenAttacks": 300,               # ms (stored int in DBR)
    "skillCooldownTime": 0.3,                 # s
    "offensiveSlowFireDurationMin": 3.0,      # s (burn duration, constant)
}

# Field-class table: drives schema core/extension split AND tier-2 assert selection.
#   'kind'      : rank_array | static
#   'monotonic' : rank arrays that MUST be non-decreasing across ranks (field-class implies growth)
#   'unit'      : provenance unit string
#   'canon_key' : player-facing canonical key (game-agnostic core vocabulary)
#   'core'      : True -> lands in exact_field core (game-agnostic); False -> per-game extension
FIELD_CLASS = {
    # --- rank arrays (per-rank scaling tables) ---
    "offensiveFireMin":     dict(kind="rank_array", monotonic=True,  unit="gd_dmg",   canon_key="damage_fire_min",       core=True),
    "offensiveFireMax":     dict(kind="rank_array", monotonic=True,  unit="gd_dmg",   canon_key="damage_fire_max",       core=True),
    "offensiveSlowFireMin": dict(kind="rank_array", monotonic=True,  unit="gd_dmg",   canon_key="damage_fire_burn_dot",  core=False),  # GD burn-DoT ext
    "skillManaCost":        dict(kind="rank_array", monotonic=True,  unit="gd_energy",canon_key="cost_resource",         core=True),
    "weaponDamagePct":      dict(kind="rank_array", monotonic=True,  unit="gd_pct",   canon_key="weapon_damage_pct",     core=True),
    # --- statics (scalars) ---
    "maxRange":                     dict(kind="static", monotonic=False, unit="gd_wu",     canon_key="range_max",           core=True),
    "endWidth":                     dict(kind="static", monotonic=False, unit="gd_wu",     canon_key="cone_end_width",      core=False),  # GD cone geom ext
    "startWidth":                   dict(kind="static", monotonic=False, unit="gd_wu",     canon_key="cone_start_width",    core=False),  # GD cone geom ext
    "timeBetweenAttacks":           dict(kind="static", monotonic=False, unit="gd_ms",     canon_key="cast_cadence_ms",     core=True),
    "skillCooldownTime":            dict(kind="static", monotonic=False, unit="gd_sec",    canon_key="cooldown_sec",        core=True),
    "offensiveSlowFireDurationMin": dict(kind="static", monotonic=False, unit="gd_sec",    canon_key="burn_duration_sec",   core=False),  # GD burn ext
}
# meta scalars carried for provenance/verification (not player-facing damage numbers)
META_FIELDS = ("skillMaxLevel", "skillUltimateLevel", "skillBitmapName", "skillDisplayName", "templateName")

TYPE_INT32, TYPE_FLOAT32, TYPE_STRIDX, TYPE_BOOL = 0, 1, 2, 3


# ============================================================ TQIT / .arz parser (productionized)
class ArzArchive:
    """Minimal TQIT .arz reader. Indexes the record table + string table; decodes one record on demand."""

    def __init__(self, path: pathlib.Path):
        self.path = path
        self.raw = path.read_bytes()
        self._parse_header()
        self._parse_string_table()
        self._parse_record_table()

    def _parse_header(self):
        b = self.raw
        (self.magic, self.version, self.rt_offset, self.rt_size,
         self.rt_count, self.st_offset, self.st_size) = struct.unpack_from("<HHiiiii", b, 0)
        if self.magic != 2:
            raise ValueError(f"BLOCKED-FORMAT: magic={self.magic}, expected 2 (TQIT). bytes[0:8]={b[0:8].hex()}")

    def _parse_string_table(self):
        # [st_offset .. st_offset+st_size): u32 COUNT prefix, then COUNT x (i32 len + bytes).
        # (The count prefix was the sole parse bug in first bring-up: without skipping it, the
        #  0x0000df74=57204 count is misread as the first string's length. Empirically the prefix
        #  equals rt_count-of-strings 57204, and consuming it aligns the record table to its end exactly.)
        self.strings = []
        b = self.raw
        pos = self.st_offset
        (self.st_count,) = struct.unpack_from("<I", b, pos)
        pos += 4
        for _ in range(self.st_count):
            (slen,) = struct.unpack_from("<i", b, pos)
            pos += 4
            s = b[pos:pos + slen].decode("latin-1")
            pos += slen
            self.strings.append(s)

    def _parse_record_table(self):
        # variable-length entries (embedded LP_string recordType).
        self.records = {}   # record_path -> dict(rtype, data_offset, comp_size, decomp_size)
        pos = self.rt_offset
        end = self.rt_offset + self.rt_size
        b = self.raw
        for _ in range(self.rt_count):
            if pos >= end:
                break
            (name_id,) = struct.unpack_from("<i", b, pos); pos += 4
            (rt_len,) = struct.unpack_from("<i", b, pos); pos += 4
            rtype = b[pos:pos + rt_len].decode("latin-1"); pos += rt_len
            (data_offset,) = struct.unpack_from("<i", b, pos); pos += 4
            (comp_size,) = struct.unpack_from("<i", b, pos); pos += 4
            (decomp_size,) = struct.unpack_from("<i", b, pos); pos += 4
            (timestamp,) = struct.unpack_from("<q", b, pos); pos += 8
            rec_path = self.strings[name_id]
            self.records[rec_path] = dict(
                rtype=rtype, data_offset=data_offset, comp_size=comp_size, decomp_size=decomp_size)

    def record_type(self, rec_path: str) -> str:
        return self.records[rec_path]["rtype"]

    def read_record(self, rec_path: str) -> dict:
        """Decompress + decode one record -> {field_name: value | [values...]}."""
        if rec_path not in self.records:
            raise KeyError(f"record not in archive: {rec_path}")
        meta = self.records[rec_path]
        # record data block begins at byte 24 (after header); entry data_offset is relative to it.
        base = 24 + meta["data_offset"]
        blob = self.raw[base: base + meta["comp_size"]]
        dec = lz4.block.decompress(blob, uncompressed_size=meta["decomp_size"])
        return self._decode_fields(dec)

    def _decode_fields(self, dec: bytes) -> dict:
        out = {}
        stream = io.BytesIO(dec)
        while True:
            head = stream.read(8)
            if len(head) < 8:
                break
            ftype, count, key_id = struct.unpack("<HHI", head)
            payload = stream.read(count * 4)
            if len(payload) < count * 4:
                break
            field_name = self.strings[key_id]
            vals = []
            for i in range(count):
                chunk = payload[i * 4:(i + 1) * 4]
                if ftype == TYPE_FLOAT32:
                    vals.append(struct.unpack("<f", chunk)[0])
                elif ftype == TYPE_INT32:
                    vals.append(struct.unpack("<i", chunk)[0])
                elif ftype == TYPE_BOOL:
                    vals.append(bool(struct.unpack("<I", chunk)[0]))
                elif ftype == TYPE_STRIDX:
                    vals.append(self.strings[struct.unpack("<I", chunk)[0]])
                else:
                    vals.append(struct.unpack("<i", chunk)[0])
            out[field_name] = vals[0] if count == 1 else vals
        return out


# ============================================================ ADAPTER: raw record -> normalized rows
def _as_list(v):
    return v if isinstance(v, list) else [v]


def _fnum(x):
    """Normalize a float that is integral (e.g. 8.0) to keep byte-faithful compare stable."""
    return x


def build_rows(rec: dict):
    """
    GD adapter: raw purifyingflame1 record -> normalized exact_field rows + a header dict.
    Returns (header, rows, rank_count).
      header : per-skill metadata (display name, provenance, rank count, record type…)
      rows   : one row per (field, rank) for arrays; one row per field for statics.
               Each row carries player-facing canonical value + raw provenance.
    """
    rank_count = int(rec["skillUltimateLevel"])   # 26 = 16 base + 10 ultimate
    base_level = int(rec["skillMaxLevel"])         # 16

    header = dict(
        kit_id=KIT_ID, game=GAME, display_name=DISPLAY_NAME,
        record_path=RECORD_PATH, source_file=SOURCE_FILE,
        record_type=None,  # filled by caller (archive knows it)
        skill_max_level=base_level, skill_ultimate_level=rank_count,
        skill_bitmap_name=rec.get("skillBitmapName"),
        skill_display_tag=rec.get("skillDisplayName"),
        template_name=rec.get("templateName"),
        name_provenance=NAME_PROVENANCE_FLAG,
    )

    rows = []
    for field, meta in FIELD_CLASS.items():
        if field not in rec:
            raise KeyError(f"expected field '{field}' absent from record — HALT (parser/scope layer)")
        raw = rec[field]
        if meta["kind"] == "rank_array":
            arr = _as_list(raw)
            # rank arrays are length rank_count in .arz ground truth
            for idx, val in enumerate(arr, start=1):
                rows.append(dict(
                    canon_key=meta["canon_key"], raw_field=field, field_kind="rank_array",
                    rank=idx, rank_count=len(arr), monotonic=meta["monotonic"],
                    canon_value=float(val), raw_value=float(val), unit=meta["unit"], core=meta["core"],
                ))
        else:  # static
            val = _as_list(raw)[0]
            rows.append(dict(
                canon_key=meta["canon_key"], raw_field=field, field_kind="static",
                rank=None, rank_count=None, monotonic=False,
                canon_value=float(val), raw_value=float(val), unit=meta["unit"], core=meta["core"],
            ))
    return header, rows, rank_count


# ============================================================ TIER-2 in-pipe asserts (oracle-free, G2)
def tier2_asserts(rows):
    """Mechanical, oracle-free. non-null; monotonic rank arrays where field-class implies; range bounds."""
    problems = []
    # group rank arrays
    arrays = {}
    for r in rows:
        # non-null on every row
        if r["canon_value"] is None or r["raw_value"] is None:
            problems.append(f"NULL value: {r['raw_field']} rank={r['rank']}")
        # range bound: damage/cost/pct/geometry are all non-negative; cadence positive
        if r["canon_value"] is not None and r["canon_value"] < 0:
            problems.append(f"NEGATIVE value: {r['raw_field']} rank={r['rank']} = {r['canon_value']}")
        if r["field_kind"] == "rank_array":
            arrays.setdefault(r["raw_field"], []).append((r["rank"], r["canon_value"], r["monotonic"]))
    # monotonic non-decreasing where flagged
    for field, seq in arrays.items():
        seq.sort(key=lambda t: t[0])
        if seq and seq[0][2]:  # monotonic flag
            prev = None
            for rank, val, _ in seq:
                if prev is not None and val < prev:
                    problems.append(f"NON-MONOTONIC {field}: rank {rank} value {val} < previous {prev}")
                prev = val
        # each monotonic damage array should be strictly positive at rank 1
        if seq and seq[0][1] is not None and seq[0][1] <= 0:
            problems.append(f"NON-POSITIVE rank-1 {field}: {seq[0][1]}")
    return problems


# ============================================================ G3 anchor byte-match (tier-1)
def _f32(x):
    """Round a Python float to its nearest float32, returned as a float64.
    .arz stores these fields as float32 (type ID 1). The probe §2 oracle lists the human-readable
    single-precision literal (9.1, 2.2, 0.3). Comparing a float32-origin value to a float64 decimal
    literal spuriously fails (9.1 is not binary-exact). Byte-true comparison is at float32 precision:
    we canonicalize BOTH sides through float32 and assert exact bit equality. This is NOT a tolerance —
    it is asserting the identical single-precision bit pattern. (4.5/3.0/integral ranks are unaffected;
    they are already binary-exact.)"""
    return struct.unpack("<f", struct.pack("<f", x))[0]


def g3_byte_match(rec, rows, rank_count):
    """Compare landed values to the probe §2 oracle at float32 (source-native) precision.
    Returns (match_table, mismatches)."""
    table = []      # (label, expected, got, PASS/FAIL)
    mism = []

    def check(label, expected, got, layer_hint):
        # canonicalize both sides to float32 when comparing floats (source-native precision)
        if isinstance(expected, float) and isinstance(got, (int, float)):
            ok = (_f32(got) == _f32(expected))
        else:
            ok = (got == expected)
        table.append((label, expected, got, "PASS" if ok else "FAIL"))
        if not ok:
            mism.append(f"{label}: expected {expected}, got {got}  [layer: {layer_hint}]")

    # rank count
    check("rank_count", ORACLE_RANK_COUNT, rank_count, "parser(skillUltimateLevel) / schema")

    # rank-array anchors
    idx = {}  # (field, rank) -> canon_value
    for r in rows:
        if r["field_kind"] == "rank_array":
            idx[(r["raw_field"], r["rank"])] = r["canon_value"]
    for field, anchors in ORACLE_RANK.items():
        for rank, exp in anchors.items():
            got = idx.get((field, rank))
            check(f"{field}[r{rank}]", exp, got, "adapter(rank map) / parser(float decode)")

    # static anchors — check against the landed rows (adapter output), not the raw dict,
    # so a schema/adapter transform bug would surface here too.
    static_idx = {r["raw_field"]: r["canon_value"] for r in rows if r["field_kind"] == "static"}
    for field, exp in ORACLE_STATIC.items():
        got = static_idx.get(field)
        # float32-canonical compare (timeBetweenAttacks oracle=int 300, landed float 300.0 -> _f32 both)
        ok = (got is not None) and (_f32(got) == _f32(float(exp)))
        table.append((field, exp, got, "PASS" if ok else "FAIL"))
        if not ok:
            mism.append(f"{field}: expected {exp}, got {got}  [layer: adapter(static map)/parser]")
    return table, mism


# ============================================================ SCHEMA DDL (G1) — additive
DDL_HEADER = """
CREATE TABLE IF NOT EXISTS exact_skill (
    kit_id             TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    game               TEXT NOT NULL,
    display_name       TEXT,                       -- player-facing canonical (G4 via skillBitmapName)
    -- game-agnostic core provenance --
    record_type        TEXT,                       -- LP_string record class (e.g. Skill_AttackSpellCone)
    rank_count         INTEGER NOT NULL,           -- authoritative rank cardinality (GD FoI = 26)
    -- raw provenance (TSR-1) --
    source_file        TEXT NOT NULL,              -- e.g. GDX1.arz
    source_version     TEXT,                       -- GD build/patch if determinable (NULL otherwise + flagged)
    record_path        TEXT NOT NULL,              -- records/skills/playerclass07/purifyingflame1.dbr
    -- per-game extension (raw record meta) --
    ext_json           TEXT,                       -- {skill_max_level, skill_ultimate_level, template_name, skill_bitmap_name, skill_display_tag}
    name_provenance    TEXT,                       -- flag: .arc tag-bridge PENDING
    adapter            TEXT NOT NULL,              -- adapter id that produced this row (reproducibility)
    schema_version     TEXT NOT NULL,
    created_date       TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (kit_id)
);
"""

DDL_FIELD = """
CREATE TABLE IF NOT EXISTS exact_skill_field (
    kit_id             TEXT NOT NULL REFERENCES exact_skill(kit_id),
    canon_key          TEXT NOT NULL,              -- player-facing canonical key (game-agnostic vocab)
    rank               INTEGER,                    -- 1-based rank; NULL for static scalars
    -- player-facing canonical value (TSR-1 (a)) --
    canon_value        REAL NOT NULL,
    canon_unit         TEXT,                       -- normalized unit tag
    -- raw provenance (TSR-1) --
    raw_field          TEXT NOT NULL,              -- exact .arz field name (e.g. offensiveFireMin)
    raw_value          REAL NOT NULL,              -- byte-faithful value from the record
    field_kind         TEXT NOT NULL CHECK (field_kind IN ('rank_array','static')),
    is_core            INTEGER NOT NULL DEFAULT 1, -- 1=game-agnostic core; 0=per-game extension field
    monotonic_class    INTEGER NOT NULL DEFAULT 0, -- 1=field-class implies non-decreasing across ranks
    source_file        TEXT NOT NULL,
    record_path        TEXT NOT NULL,
    schema_version     TEXT NOT NULL,
    created_date       TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (kit_id, canon_key, rank)
);
CREATE INDEX IF NOT EXISTS idx_esf_kit     ON exact_skill_field(kit_id);
CREATE INDEX IF NOT EXISTS idx_esf_canon   ON exact_skill_field(canon_key);
CREATE INDEX IF NOT EXISTS idx_esf_rawfield ON exact_skill_field(raw_field);
"""


def backup_db():
    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    dst = DB.parent / f"corpus.db.pre-gd-slice-{ts}-backup"
    shutil.copy2(DB, dst)
    md5 = hashlib.md5(DB.read_bytes()).hexdigest()
    (dst.parent / f"{dst.name}.md5.txt").write_text(md5 + "\n")
    print(f"BACKUP  {dst.name}  md5={md5}")
    return dst


def apply_rows(con, header, rows, record_type, source_version):
    cur = con.cursor()
    cur.executescript(DDL_HEADER)
    cur.executescript(DDL_FIELD)

    import json
    ext = json.dumps(dict(
        skill_max_level=header["skill_max_level"],
        skill_ultimate_level=header["skill_ultimate_level"],
        template_name=header["template_name"],
        skill_bitmap_name=header["skill_bitmap_name"],
        skill_display_tag=header["skill_display_tag"],
    ))
    # idempotent: clear any prior slice rows for this kit before re-landing
    cur.execute("DELETE FROM exact_skill_field WHERE kit_id=?", (KIT_ID,))
    cur.execute("DELETE FROM exact_skill WHERE kit_id=?", (KIT_ID,))

    cur.execute(
        "INSERT INTO exact_skill(kit_id,game,display_name,record_type,rank_count,source_file,"
        "source_version,record_path,ext_json,name_provenance,adapter,schema_version) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (KIT_ID, GAME, header["display_name"], record_type, header["skill_ultimate_level"],
         SOURCE_FILE, source_version, RECORD_PATH, ext, header["name_provenance"],
         "gd_arz_adapter_2026_07_24", SCHEMA_VERSION),
    )
    for r in rows:
        cur.execute(
            "INSERT INTO exact_skill_field(kit_id,canon_key,rank,canon_value,canon_unit,raw_field,"
            "raw_value,field_kind,is_core,monotonic_class,source_file,record_path,schema_version) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (KIT_ID, r["canon_key"], r["rank"], r["canon_value"], r["unit"], r["raw_field"],
             r["raw_value"], r["field_kind"], 1 if r["core"] else 0, 1 if r["monotonic"] else 0,
             SOURCE_FILE, RECORD_PATH, SCHEMA_VERSION),
        )
    # schema_meta (idempotent)
    exists = cur.execute("SELECT COUNT(*) FROM corpus_schema_meta WHERE version=?", (SCHEMA_VERSION,)).fetchone()[0]
    if not exists:
        cur.execute(
            "INSERT INTO corpus_schema_meta(version, applied_utc, note) VALUES (?,?,?)",
            (SCHEMA_VERSION,
             datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "GD-SLICE exact-fields schema (elrond, gandalf GD-SLICE charter, Matt TSR-3 GD-first). "
             "Additive: exact_skill (header) + exact_skill_field (per-field/per-rank, core/extension split). "
             "First adapter proves schema (TSR-2). FoI landed from GDX1.arz byte-verified vs probe oracle "
             "(G3). No overwrite of banked kit_numeric/dossier rows (G5 = curation-note flag)."),
        )
    con.commit()
    return len(rows)


# ============================================================ MAIN
def main(mode="apply"):
    if not ARZ.exists():
        sys.exit(f"FATAL: .arz not found at {ARZ}")
    print(f"ARZ     {ARZ}")
    arc = ArzArchive(ARZ)
    print(f"HEADER  magic={arc.magic} version={arc.version} records={arc.rt_count} strings={len(arc.strings)}")

    # ---- honorable fallback: record-class the probe didn't cover ----
    if RECORD_PATH not in arc.records:
        sys.exit(f"BLOCKED-FORMAT: record not indexed: {RECORD_PATH}")
    rtype = arc.record_type(RECORD_PATH)
    print(f"RECORD  {RECORD_PATH}  type={rtype}")
    if rtype != "Skill_AttackSpellCone":
        print(f"  NOTE: record type '{rtype}' differs from probe-expected 'Skill_AttackSpellCone' — proceeding, flagged.")

    try:
        rec = arc.read_record(RECORD_PATH)
    except Exception as e:
        sys.exit(f"BLOCKED-FORMAT: decode failed for {RECORD_PATH}: {e!r}")

    header, rows, rank_count = build_rows(rec)
    header["record_type"] = rtype

    # ---- G2 tier-2 asserts ----
    problems = tier2_asserts(rows)
    print(f"\nG2 tier-2 asserts: {len(rows)} rows checked  ->  {'ALL GREEN' if not problems else 'FAIL'}")
    for p in problems:
        print("  FAIL:", p)
    if problems:
        sys.exit("G2 FAILED — HALT (mechanical assert). No DB writes.")

    # ---- G3 byte-match ----
    table, mism = g3_byte_match(rec, rows, rank_count)
    print(f"\nG3 anchor byte-match ({len(table)} anchors):")
    for label, exp, got, verdict in table:
        print(f"  [{verdict}] {label:<32} expected={exp!r:<10} got={got!r}")
    n_pass = sum(1 for t in table if t[3] == "PASS")
    print(f"G3 result: {n_pass}/{len(table)} PASS")
    if mism:
        print("\nG3 MISMATCHES (HALT-diagnose — layer named per line):")
        for m in mism:
            print("  ", m)
        sys.exit("G3 FAILED — HALT-diagnose. Never tolerance-fudge. No DB writes.")

    if mode in ("verify", "dry"):
        print(f"\n{'VERIFY-ONLY' if mode=='verify' else 'DRY-RUN'} — gates green, NO DB writes.")
        if mode == "dry":
            core = sum(1 for r in rows if r["core"])
            ext = len(rows) - core
            print(f"  Would land: 1 exact_skill header + {len(rows)} exact_skill_field rows "
                  f"({core} core, {ext} per-game extension) into corpus.db.")
        return

    # ---- APPLY ----
    backup_db()
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON;")
    # source_version: GDX1.arz has no in-record build tag we parse here; flag as undetermined.
    source_version = None
    n = apply_rows(con, header, rows, rtype, source_version)

    # ---- post-apply verification (re-read from DB, re-run G3 against landed rows) ----
    cur = con.cursor()
    landed = cur.execute(
        "SELECT canon_key, rank, canon_value, raw_field, raw_value, field_kind, is_core, monotonic_class "
        "FROM exact_skill_field WHERE kit_id=?", (KIT_ID,)).fetchall()
    landed_rows = [dict(canon_key=r[0], rank=r[1], canon_value=r[2], raw_field=r[3], raw_value=r[4],
                        field_kind=r[5], core=bool(r[6]), monotonic=bool(r[7]), unit=None) for r in landed]
    lr_count = cur.execute("SELECT rank_count FROM exact_skill WHERE kit_id=?", (KIT_ID,)).fetchone()[0]
    _, mism2 = g3_byte_match(rec, landed_rows, lr_count)
    p2 = tier2_asserts(landed_rows)
    fk = cur.execute("PRAGMA foreign_key_check").fetchall()
    integ = cur.execute("PRAGMA integrity_check").fetchone()[0]

    print("\n---- POST-APPLY VERIFICATION (re-read from DB) ----")
    print(f"  exact_skill_field rows landed : {n}")
    print(f"  rank_count in exact_skill     : {lr_count}")
    print(f"  G3 re-match on landed rows    : {'CLEAN' if not mism2 else mism2}")
    print(f"  tier-2 on landed rows         : {'ALL GREEN' if not p2 else p2}")
    print(f"  foreign_key_check             : {'clean' if not fk else fk}")
    print(f"  integrity_check               : {integ}")
    assert not mism2, "post-apply G3 mismatch — HALT"
    assert not p2, "post-apply tier-2 failure — HALT"
    assert lr_count == ORACLE_RANK_COUNT
    assert not fk and integ == "ok"
    print("POST-APPLY VERIFICATION PASS.")
    con.close()


if __name__ == "__main__":
    if "--verify-only" in sys.argv:
        main("verify")
    elif "--dry-run" in sys.argv:
        main("dry")
    else:
        main("apply")
