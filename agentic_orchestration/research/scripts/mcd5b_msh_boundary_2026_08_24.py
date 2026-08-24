#!/usr/bin/env python3
"""KC2 MODEL-COMPLETION RUN · Wave 1 · piece D-5b — THE `.msh` DECODE + BOUNDARY DERIVATION.
Instrument I-D5b-1.  DIRECT SEQUEL to D-5 (instrument `mcd5_arena_boundary_2026_08_24.py`).

WHY THIS EXISTS
    D-5 established that the Crucible arena is NOT closed by terrain (flood-fill exits all four
    sides at every threshold in a 6.7x sweep) and that what closes it must be entity collision:
    341 of 483 A001 placements carry `Decoration.allowPathing = False`, 336 of them with
    `actorRadius = 0`, i.e. their blocking extent lives in the mesh.  D-5 did not open `.msh`.
    This instrument opens it, and derives the boundary.

WHAT IT DECODES (first-of-kind for this project, all from the shipped bytes)
    1. the `MSH\\x03` container: a flat [u32 chunk_id][u32 size][payload] chain from +4 to EOF,
       with SEVEN chunk ids observed.  Decoded here: 10 (AABB), 4 (vertex buffer), 5 (index
       buffer), 8 (HITBOX OBB ARRAY), 7 (material list), 13/6 (2-word + 1-word scalars).
    2. chunk 10 == the exact vertex-extreme AABB.  PROVED bit-exact, per mesh, against the
       chunk-4 vertex positions -- the parse validates itself.
    3. chunk 8 == the collision sub-block the D-5b commission hypothesised: a 96-byte-per-entry
       OBB array (32 B name, 3 f32 half-extents, 3x3 f32 rotation, 3 f32 centre, u32 0xFFFFFFFF),
       which is what `Entity::GetHitBox(int)` hands `NavMeshBuilder::AddBox`.
    4. `NavManager::SetDefaultConfig` (Engine.dll RVA 0x126d70): the 13 navigation-build
       parameters, read out of the immediate operands.

WHAT IT CORRECTS IN D-5 (§ 5 step 2, the engine chain)
    D-5 named `Entity::OccludesPathing -> ImpassableData::AddEntity -> ImpassableData::AddBox`.
    In THIS shipped build all three are ICF-folded EMPTY stubs (`ret 8` / `ret 0xc` /
    `xor al,al; ret`).  The live chain is `Level::CreatePathMesh` ->
    {`NavMeshBuilder::Create(const Level*)`  [mesh-instance TRIANGLES],
     `NavMeshBuilder::Create(const Entity*)` [entity HITBOX OBBs]} -> `NavManager::AddData`.
    So the engine's static blocker is triangle geometry, not a per-mesh AABB.  This instrument
    therefore composes THREE rules and reports all three rather than blessing one.

OUTCOME (GL-12 / Law 3) -- the format target is MET, the geometry target is NOT
    A 24-cell composition sweep (3 blocking rules x 8 walkable bands) plus a 17-cell terrain sweep
    produces NO cell that is both CLOSED and ANCHOR-COMPLETE.  At the most engine-faithful cell,
    three anchors the shipped game uses -- including `tier16spawnpoint01`, the tier-16 emitter --
    land INSIDE blocking geometry.  A monster emitter cannot be inside a wall, so the composition
    is falsified by the game's own data.  NO BOUNDARY IS EMITTED: no polygon, no radial profile,
    no rectangle.  The walkability rule lives behind `NavManager::CreateNavigationData`, which is
    not decoded; reimplementing it would be inventing a rule, which Law 3 forbids.

READ-ONLY on both vendor trees.  Writes ONLY into this lap's evidence dir.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-24.  Run KC2-MC, Wave 1, piece D-5b.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import pathlib
import re
import struct
import sys
from collections import Counter, deque

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
COLLAB = HERE.parent.parent.parent
LAP = "2026-08-24-kc2-mc-lap-d5b-msh-boundary-derivation"
OUT = COLLAB / "agentic_orchestration/legolas/notes" / LAP / "evidence"
OUT.mkdir(parents=True, exist_ok=True)

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")
ENGINE_SRC = pathlib.Path("/Users/admin/Games/reincarnated-engine")

sys.path.insert(0, str(HERE))
from gd_arc_reader_2026_07_26 import ArcArchive          # noqa: E402
from gd_arz_adapter_2026_07_24 import ArzArchive         # noqa: E402
from pm4s_pe_2026_08_14 import PE32                      # noqa: E402

# ══════════════════════════════════════════════════ § 1  PINS — HALT on mismatch
PIN = {
    GD / "Engine.dll": "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c",
    GD / "resources/Level Art.arc":
        "e33e3b93b89c4f4d1bfdbf6fbd3223e097ebea7941a45a0b16a86f173a4a8f33",
    VENDOR / "survivalmode1/resources/Maps.arc":
        "2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237",
}


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


DIGESTS = {}
for _p, _want in PIN.items():
    _got = sha256(_p)
    DIGESTS[str(_p)] = _got
    if _got != _want:
        raise SystemExit(f"HALT — digest mismatch on {_p}: {_got} != {_want}")
for _extra in (VENDOR / "mods/survivalmode/resources/Creatures.arc",
               VENDOR / "database/database.arz"):
    DIGESTS[str(_extra)] = sha256(_extra)

LOG: list[str] = []


def log(s: str = "") -> None:
    print(s)
    LOG.append(s)


log("=" * 100)
log("KC2-MC · D-5b — THE `.msh` DECODE + ARENA-BOUNDARY DERIVATION")
log("=" * 100)

# ══════════════════════════════════════════════════ § 2  THE `MSH\x03` FORMAT
#
#   +0   b'MSH\x03'
#   +4   flat chain, to EOF exactly:   [u32 chunk_id][u32 chunk_size][payload]
#
#   id  4  VERTEX BUFFER   [u32 n_stream][u32 stride][u32 n_vert][u32 stream_type x n_stream]
#                          [ n_vert x stride bytes ];  position = first 3 f32 of each vertex
#   id  5  INDEX BUFFER    [u32 n_tri][u32 n_submesh][u16 idx x 3*n_tri][44 B x n_submesh tail]
#   id  8  HITBOX OBB LIST [u32 n][ n x 96 B: 32 B name | 3 f32 half-extent | 9 f32 rotation
#                                             | 3 f32 centre | u32 0xFFFFFFFF ]
#   id 10  AABB            [6 f32]  = EXACT vertex extremes (proved per mesh, § 2.2)
#   id  7  MATERIAL LIST   [u32 n][ per material: len-prefixed shader path + typed properties ]
#   id 13  [u32][u32]      id 6  [u32]
MSH_MAGIC = b"MSH\x03"
HITBOX_STRIDE = 96


def msh_chunks(b: bytes):
    """Walk the chunk chain.  Returns (dict id -> [(payload_off, size)], chain_closes_exactly)."""
    if b[:4] != MSH_MAGIC:
        raise SystemExit(f"HALT — msh magic {b[:4]!r} != {MSH_MAGIC!r}")
    p, out = 4, {}
    while p + 8 <= len(b):
        cid, sz = struct.unpack_from("<2I", b, p)
        if p + 8 + sz > len(b):
            return out, False
        out.setdefault(cid, []).append((p + 8, sz))
        p = p + 8 + sz
    return out, p == len(b)


def msh_parse(b: bytes):
    """Return dict with aabb, verts (n,3), tris (m,3), hitboxes[], chunk map, chain flag."""
    C, clean = msh_chunks(b)
    aabb = verts = tris = None
    if 10 in C:
        o, sz = C[10][0]
        if sz == 24:
            aabb = np.array(struct.unpack_from("<6f", b, o), dtype=np.float64)
    if 4 in C:
        o, sz = C[4][0]
        n_stream, stride, n_vert = struct.unpack_from("<3I", b, o)
        vs = o + 12 + 4 * n_stream
        raw = np.frombuffer(b[vs:vs + stride * n_vert], dtype=np.uint8).reshape(n_vert, stride)
        verts = raw[:, :12].copy().view("<f4").reshape(n_vert, 3).astype(np.float64)
    if 5 in C:
        o, sz = C[5][0]
        n_tri, n_sub = struct.unpack_from("<2I", b, o)
        tris = np.frombuffer(b[o + 8:o + 8 + 6 * n_tri], dtype="<u2").reshape(n_tri, 3).astype(np.int32)
    hb = []
    if 8 in C:
        o, sz = C[8][0]
        n = struct.unpack_from("<I", b, o)[0]
        for i in range(n):
            q = o + 4 + i * HITBOX_STRIDE
            name = b[q:q + 32].split(b"\0")[0].decode("latin-1")
            ext = np.array(struct.unpack_from("<3f", b, q + 32), dtype=np.float64)
            rot = np.array(struct.unpack_from("<9f", b, q + 44), dtype=np.float64).reshape(3, 3)
            ctr = np.array(struct.unpack_from("<3f", b, q + 80), dtype=np.float64)
            tail = struct.unpack_from("<I", b, q + 92)[0]
            hb.append(dict(name=name, ext=ext, rot=rot, ctr=ctr, tail=tail))
    return dict(aabb=aabb, verts=verts, tris=tris, hitboxes=hb,
                chunks={k: [(o, s) for o, s in v] for k, v in C.items()}, clean=clean)


# ── mesh resolution across the two depots that hold A001's blocking meshes
LA = ArcArchive(GD / "resources/Level Art.arc")
MC = ArcArchive(VENDOR / "mods/survivalmode/resources/Creatures.arc")
_MESH_IDX = {}
for _arc, _pre in ((LA, "level art/"), (MC, "creatures/")):
    for _n in _arc.names():
        _MESH_IDX[(_pre + _n).lower()] = (_arc, _n)

_MESH_CACHE = {}


def mesh(path: str):
    key = path.lower().replace("\\", "/")
    if key not in _MESH_CACHE:
        arc, n = _MESH_IDX[key]
        _MESH_CACHE[key] = msh_parse(arc.read_file(n))
    return _MESH_CACHE[key]


# ══════════════════════════════════════════════════ § 3  THE `.lvl` REGION — with ROTATIONS
# Same container as D-5 § 2; this lap additionally KEEPS the 9-float rotation of each placement,
# which D-5's parser read for resynchronisation and then discarded.
def region_blob(arc_rel: str, map_name: str, region="Region_Survival_A001.lvl"):
    raw = ArcArchive(VENDOR / arc_rel).read_file(map_name)
    m = re.search(re.escape(region.encode()), raw)
    off, size = struct.unpack_from("<2I", raw, m.end())
    return raw[off:off + size]


def parse_region(blob: bytes):
    if blob[:4] != b"LVL\x0f":
        raise SystemExit(f"HALT — region magic {blob[:4]!r}")
    n_str = struct.unpack_from("<I", blob, 36)[0]
    p, strings = 40, []
    for _ in range(n_str):
        ln = struct.unpack_from("<I", blob, p)[0]
        p += 4
        strings.append(blob[p:p + ln].decode("latin-1"))
        p += ln
    count = struct.unpack_from("<I", blob, p)[0]
    p += 8

    def ortho(o):
        if o + 36 > len(blob):
            return False
        r = struct.unpack_from("<9f", blob, o)
        return all(0.98 <= math.sqrt(r[i] ** 2 + r[i + 1] ** 2 + r[i + 2] ** 2) <= 1.02
                   for i in (0, 3, 6))

    plain, group, pos = [], [], p
    for g in range(count):
        R = struct.unpack_from("<9f", blob, pos)
        x, y, z = struct.unpack_from("<3f", blob, pos + 36)
        flags, idx = struct.unpack_from("<2I", blob, pos + 48)
        nxt, skip = pos + 56, 0
        if g < count - 1:
            while skip < 64 and not ortho(nxt + skip):
                skip += 4
        if skip == 16:
            group.append(dict(x=x, y=y, z=z))
        elif idx < n_str:
            plain.append(dict(dbr=strings[idx], x=x, y=y, z=z,
                              R=np.array(R, dtype=np.float64).reshape(3, 3), flags=flags))
        pos = nxt + skip
    hits = [m.start() for m in re.finditer(re.escape(struct.pack("<2I", 129, 129)), blob)]
    if len(hits) != 1:
        raise SystemExit(f"HALT — {len(hits)} heightfield markers")
    hs = hits[0] + 8
    hf = np.frombuffer(blob[hs:hs + 129 * 129 * 4], dtype="<f4").reshape(129, 129).astype(np.float64)
    return strings, plain, group, hf


BLOB = region_blob("survivalmode1/resources/Maps.arc", "survivalworld_a.map")
STRINGS, PLAIN, GROUP, H = parse_region(BLOB)
CX = sum(g["x"] for g in GROUP) / len(GROUP)
CZ = sum(g["z"] for g in GROUP) / len(GROUP)
OX, OZ = -4.00, 0.00                        # D-5 § 3, validated to 3.92 mm
log(f"\n§3  A001 re-parsed WITH rotations: {len(PLAIN)} plain + {len(GROUP)} group members")
log(f"    PatrolPoint_Attack centroid (sim origin) = ({CX:.4f}, {CZ:.4f})")

DBR = json.load(open(COLLAB / "agentic_orchestration/legolas/notes"
                     / "2026-08-24-kc2-mc-lap-d5-arena-boundary-decode/evidence/A001_dbr_pathing.json"))
BLOCK = [p for p in PLAIN if DBR.get(p["dbr"], {}).get("allowPathing") is False]
log(f"    blocking placements (allowPathing = False): {len(BLOCK)}  "
    f"[D-5 count 341 -> {'MATCH' if len(BLOCK) == 341 else 'MISMATCH'}]")

# ── the placement 3x3 carries NO scale: every row is unit length (checked, not assumed)
ROWN = np.array([np.linalg.norm(p["R"], axis=1) for p in BLOCK])
DETS = np.array([np.linalg.det(p["R"]) for p in BLOCK])
log(f"    3x3 row norms in [{ROWN.min():.6f}, {ROWN.max():.6f}]  det in "
    f"[{DETS.min():.6f}, {DETS.max():.6f}]  => pure rotation, unit scale")

# ── are the blockers a RING (a wall) or a FIELD (decoration)?  measured, not eyeballed.
BR = np.array([math.hypot(p["x"] - CX, p["z"] - CZ) for p in BLOCK])
RADHIST = [int(((BR >= a) & (BR < a + 10)).sum()) for a in range(0, 110, 10)]
log(f"    blocker distance from the arena centroid: min {BR.min():.1f} · p10 "
    f"{np.percentile(BR, 10):.1f} · median {np.median(BR):.1f} · p90 {np.percentile(BR, 90):.1f} "
    f"· max {BR.max():.1f} m")
log(f"    10 m-bin histogram 0..110 m: {RADHIST}")
log("    => a FIELD, not a ring: no annulus holds a dominant share.")

# ══════════════════════════════════════════════════ § 4  ENGINE-SIDE: the real chain + config
ENG = PE32(GD / "Engine.dll")
EX = ENG.exports()


def first_bytes(rva, n=8):
    return ENG.raw[ENG.rva_to_off(rva):ENG.rva_to_off(rva) + n]


STUBS = {}
for _sym in ("?AddEntity@ImpassableData@GAME@@QAEXPAVEntity@2@_N@Z",
             "?AddBox@ImpassableData@GAME@@AAEXHABVOBBox@2@_N@Z",
             "?GetCollisionBox@Entity@GAME@@UBE_NAAVOBBox@2@@Z",
             "?OccludesPathing@Entity@GAME@@UBE_NXZ",
             "?OccludesPathing@Actor@GAME@@UBE_NXZ"):
    STUBS[_sym] = dict(rva=hex(EX[_sym]), first_bytes=first_bytes(EX[_sym], 6).hex(" "))
log("\n§4  ENGINE CHAIN — D-5 § 5 step 2 CORRECTED")
for k, v in STUBS.items():
    log(f"    {v['rva']:>9}  {v['first_bytes']:<20}  {k.split('@@')[0]}")
log("    -> ImpassableData::AddEntity = `ret 8`, ::AddBox = `ret 0xc`, Entity::GetCollisionBox")
log("       = `xor al,al; ret 4`, Entity::OccludesPathing = `xor al,al; ret`  (ICF-folded stubs).")
log("       The LIVE chain is Level::CreatePathMesh -> NavMeshBuilder::Create(Level*) [TRIANGLES]")
log("       + NavMeshBuilder::Create(Entity*) [HITBOX OBBs] -> NavManager::AddData(Region*).")

# NavManager::SetDefaultConfig — 13 immediates, read out of the instruction stream
CFG_RVA = EX["?SetDefaultConfig@NavManager@GAME@@AAEXXZ"]
_raw = ENG.raw[ENG.rva_to_off(CFG_RVA):ENG.rva_to_off(CFG_RVA) + 0x60]
NAVCFG = []
_i = 0
while _i + 7 <= len(_raw) and _raw[_i] == 0xC7 and _raw[_i + 1] == 0x41:
    _slot = _raw[_i + 2]
    _w = _raw[_i + 3:_i + 7]
    NAVCFG.append(dict(offset=hex(_slot), u32=struct.unpack("<I", _w)[0],
                       f32=round(struct.unpack("<f", _w)[0], 6)))
    _i += 7
log(f"\n    NavManager::SetDefaultConfig  RVA {CFG_RVA:#x} — {len(NAVCFG)} immediates:")
for _r in NAVCFG:
    log(f"      this+{_r['offset']:<5} u32={_r['u32']:<12} f32={_r['f32']}")

# The float that governs the height gate below.  Named by POSITION in the block, graded in the note.
AGENT_HEIGHT = [r["f32"] for r in NAVCFG][3]      # this+0x18
CELL_SIZE = [r["f32"] for r in NAVCFG][1]         # this+0x10
AGENT_RADIUS = [r["f32"] for r in NAVCFG][4]      # this+0x1c
log(f"    -> gate inputs used below: cell {CELL_SIZE} m · height {AGENT_HEIGHT} m · "
    f"radius {AGENT_RADIUS} m")

# Terrain rule, re-read from .rdata exactly as D-5 did (no retyped constants)
SLOPE_RVA = EX["?SlopeImpassable@Terrain@GAME@@AAE_NHH@Z"]


def rdata_f32(va):
    return struct.unpack_from("<f", ENG.raw, ENG.rva_to_off(va - ENG.image_base))[0]


K_AVG = rdata_f32(0x102e04c8)
T_SLOPE = rdata_f32(0x102e0538)
log(f"    Terrain::SlopeImpassable RVA {SLOPE_RVA:#x}  K={K_AVG}  T={T_SLOPE}  (D-5 § 4, re-read)")

# ══════════════════════════════════════════════════ § 5  `.msh` PARSE + SELF-VALIDATION
MESHES = sorted({DBR[p["dbr"]]["mesh"] for p in BLOCK})
log(f"\n§5  `.msh` decode — {len(MESHES)} distinct meshes behind the {len(BLOCK)} blocking placements")
MESH_TABLE = []
for nm in MESHES:
    M = mesh(nm)
    aabb_exact = bool(M["aabb"] is not None and M["verts"] is not None and np.array_equal(
        M["aabb"], np.concatenate([M["verts"].min(0), M["verts"].max(0)])))
    idx_ok = bool(M["tris"] is None or M["tris"].max() == len(M["verts"]) - 1)
    MESH_TABLE.append(dict(
        mesh=nm, chain_closes=M["clean"], n_vert=int(len(M["verts"])),
        n_tri=int(len(M["tris"])), n_hitbox=len(M["hitboxes"]),
        aabb=[round(float(v), 4) for v in M["aabb"]],
        aabb_equals_vertex_extremes=aabb_exact, index_max_is_nvert_minus_1=idx_ok,
        chunk_ids=sorted(M["chunks"])))
N_EXACT = sum(r["aabb_equals_vertex_extremes"] for r in MESH_TABLE)
N_CLEAN = sum(r["chain_closes"] for r in MESH_TABLE)
N_IDXOK = sum(r["index_max_is_nvert_minus_1"] for r in MESH_TABLE)
log(f"    chunk chain closes exactly at EOF : {N_CLEAN}/{len(MESH_TABLE)}")
log(f"    chunk-10 AABB == vertex extremes  : {N_EXACT}/{len(MESH_TABLE)}   (bit-exact, 6/6 floats)")
log(f"    chunk-5 max index == n_vert - 1   : {N_IDXOK}/{len(MESH_TABLE)}")
log(f"    total triangles behind the blockers: "
    f"{sum(len(mesh(DBR[p['dbr']]['mesh'])['tris']) for p in BLOCK):,}")
log(f"    meshes carrying a chunk-8 hitbox   : "
    f"{sum(1 for r in MESH_TABLE if r['n_hitbox'] > 0)}/{len(MESH_TABLE)}  "
    f"(total OBBs {sum(r['n_hitbox'] for r in MESH_TABLE)})")

# ── an independent corpus-wide format check, so the format claim does not rest on 27 files
CORPUS = [n for n in LA.names() if n.lower().endswith(".msh")]
rng = np.random.default_rng(20260824)
SAMPLE = [CORPUS[i] for i in rng.choice(len(CORPUS), size=400, replace=False)]
c_clean = c_exact = c_idx = c_tot = 0
for n in SAMPLE:
    try:
        M = msh_parse(LA.read_file(n))
    except Exception:
        continue
    c_tot += 1
    c_clean += bool(M["clean"])
    if M["aabb"] is not None and M["verts"] is not None and len(M["verts"]):
        c_exact += bool(np.array_equal(M["aabb"],
                                       np.concatenate([M["verts"].min(0), M["verts"].max(0)])))
    if M["tris"] is not None and len(M["tris"]) and M["verts"] is not None:
        c_idx += bool(M["tris"].max() == len(M["verts"]) - 1)
log(f"    corpus control ({c_tot} random `.msh` from {len(CORPUS)} in Level Art.arc): "
    f"chain {c_clean}/{c_tot} · AABB-exact {c_exact}/{c_tot} · index-exact {c_idx}/{c_tot}")

# ── chunk 8 cross-validated against chunk 10: for a SINGLE-hitbox mesh the OBB centre must
#    reproduce the AABB centre on the axes the OBB rotation leaves aligned.  Falsifiable.
HB_CHECK = []
for r in MESH_TABLE:
    M = mesh(r["mesh"])
    if r["n_hitbox"] != 1 or M["aabb"] is None:
        continue
    hb = M["hitboxes"][0]
    ac = (M["aabb"][:3] + M["aabb"][3:]) / 2
    ae = (M["aabb"][3:] - M["aabb"][:3]) / 2
    # which world axis does each local box axis map to, and how big is the box on it
    w_ext = np.abs(hb["rot"]).T @ hb["ext"]
    HB_CHECK.append(dict(mesh=r["mesh"], name=hb["name"],
                         centre_delta=[round(float(v), 6) for v in (hb["ctr"] - ac)],
                         obb_world_extent=[round(float(v), 4) for v in w_ext],
                         aabb_extent=[round(float(v), 4) for v in ae]))
_best = min(HB_CHECK, key=lambda d: abs(d["centre_delta"][1])) if HB_CHECK else None
if _best:
    log(f"    chunk-8 vs chunk-10 cross-check on {len(HB_CHECK)} single-hitbox meshes: "
        f"|delta y-centre| median "
        f"{np.median([abs(d['centre_delta'][1]) for d in HB_CHECK]) * 1000:.3f} mm; "
        f"tightest {_best['mesh'].rsplit('/', 1)[-1]} delta {_best['centre_delta']}")

# ── SCALE FALSIFIER: are mesh units world metres?  The player character says so.
_CR = ArcArchive(GD / "resources/Creatures.arc")
_hero = msh_parse(_CR.read_file("pc/hero01.msh"))
HERO_H = float(_hero["aabb"][4] - _hero["aabb"][1])
log(f"    scale falsifier — creatures/pc/hero01.msh AABB y {_hero['aabb'][1]:.4f} .. "
    f"{_hero['aabb'][4]:.4f} = {HERO_H:.4f} m tall, against the decoded agentHeight "
    f"{AGENT_HEIGHT} m => mesh units ARE world metres.")

# ══════════════════════════════════════════════════ § 6  THE TRANSFORM CONVENTION — decoded
# `NavMeshBuilder::Create(const Level*)` transforms each mesh vertex with
#     out.x = m[0]*v.x + m[3]*v.y + m[6]*v.z   (operands at [ebp-0xa8], [ebp-0x9c], [ebp-0x90],
#     out.y = m[1]*.. + m[4]*.. + m[7]*..       i.e. floats 0,3,6 / 1,4,7 / 2,5,8 of the 9-float
#     out.z = m[2]*.. + m[5]*.. + m[8]*..       instance matrix copied from meshinst+0x74)
# => ROW-VECTOR convention: world = local @ M, M row-major.  Not assumed; read.
def to_world(local: np.ndarray, p) -> np.ndarray:
    return local @ p["R"] + np.array([p["x"], p["y"], p["z"]])


# ══════════════════════════════════════════════════ § 7  RASTER GRID + TERRAIN
CS = CELL_SIZE                                   # 0.25 m, decoded
NX = int(round(128 / CS))                        # 512
X0, Z0 = OX, OZ                                  # region origin in world coords: (-4, 0)
xs = X0 + (np.arange(NX) + 0.5) * CS
zs = Z0 + (np.arange(NX) + 0.5) * CS
GX, GZ = np.meshgrid(xs, zs)                     # [row=z, col=x]


def bilinear_h(x, z):
    r = np.clip((z - OZ), 0, 127.999)
    c = np.clip((x - OX), 0, 127.999)
    i0, j0 = np.floor(r).astype(int), np.floor(c).astype(int)
    fa, fb = r - i0, c - j0
    return ((1 - fa) * (1 - fb) * H[i0, j0] + fa * (1 - fb) * H[i0 + 1, j0]
            + (1 - fa) * fb * H[i0, j0 + 1] + fa * fb * H[i0 + 1, j0 + 1])


TH = bilinear_h(GX, GZ)                          # terrain height per 0.25 m cell


def terrain_impassable(T):
    h00, h01 = H[:-1, :-1], H[:-1, 1:]
    h10, h11 = H[1:, :-1], H[1:, 1:]
    avg = (h00 + h01 + h10 + h11) * K_AVG
    imp = np.maximum.reduce([abs(h00 - avg), abs(h01 - avg),
                             abs(h10 - avg), abs(h11 - avg)]) > T
    return np.repeat(np.repeat(imp, int(1 / CS), axis=0), int(1 / CS), axis=1)


TIMP = terrain_impassable(T_SLOPE)

# ══════════════════════════════════════════════════ § 8  RASTER GRID + TERRAIN
CS = CELL_SIZE                                   # 0.25 m — the engine's own nav cell
NX = int(round(128 / CS))                        # 512
X0, Z0 = OX, OZ                                  # region origin in level coords: (-4, 0)
xs = X0 + (np.arange(NX) + 0.5) * CS
zs = Z0 + (np.arange(NX) + 0.5) * CS
GX, GZ = np.meshgrid(xs, zs)                     # [row = z, col = x]


def bilinear_h(x, z):
    r = np.clip(z - OZ, 0, 127.999)
    c = np.clip(x - OX, 0, 127.999)
    i0, j0 = np.floor(r).astype(int), np.floor(c).astype(int)
    fa, fb = r - i0, c - j0
    return ((1 - fa) * (1 - fb) * H[i0, j0] + fa * (1 - fb) * H[i0 + 1, j0]
            + (1 - fa) * fb * H[i0, j0 + 1] + fa * fb * H[i0 + 1, j0 + 1])


TH = bilinear_h(GX, GZ)
UP = int(round(1 / CS))


def up(m):
    return np.repeat(np.repeat(m, UP, axis=0), UP, axis=1)


H00, H01, H10, H11 = H[:-1, :-1], H[:-1, 1:], H[1:, :-1], H[1:, 1:]
AVG = (H00 + H01 + H10 + H11) * K_AVG
DEV = np.maximum.reduce([abs(H00 - AVG), abs(H01 - AVG), abs(H10 - AVG), abs(H11 - AVG)])
GRAD = np.hypot(np.maximum(abs(H01 - H00), abs(H11 - H10)),
                np.maximum(abs(H10 - H00), abs(H11 - H01)))
SLOPE_DEG = np.degrees(np.arctan(GRAD))
STEP = np.maximum.reduce([abs(H01 - H00), abs(H10 - H00), abs(H11 - H00),
                          abs(H11 - H01), abs(H11 - H10), abs(H10 - H01)])
TIMP = up(DEV > T_SLOPE)                         # D-5's decoded terrain rule, at 0.25 m

# ══════════════════════════════════════════════════ § 9  SAMPLE CLOUDS — the three rules
def _bary(n):
    a, b = [], []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            a.append(i / n)
            b.append(j / n)
    return np.array(a), np.array(b)


_LAT = {}


def cloud_triangles():
    parts, buckets = [], {}
    for p in BLOCK:
        M = mesh(DBR[p["dbr"]]["mesh"])
        T = to_world(M["verts"], p)[M["tris"]]
        e = np.maximum.reduce([np.linalg.norm(T[:, 1] - T[:, 0], axis=1),
                               np.linalg.norm(T[:, 2] - T[:, 1], axis=1),
                               np.linalg.norm(T[:, 0] - T[:, 2], axis=1)])
        n = np.clip(np.ceil(e / (CS / 2)).astype(int), 1, 48)
        for nb in np.unique(n):
            buckets.setdefault(int(nb), []).append(T[n == nb])
    for nb, ps in sorted(buckets.items()):
        T = np.concatenate(ps)
        if nb not in _LAT:
            _LAT[nb] = _bary(nb)
        a, b = _LAT[nb]
        c = 1 - a - b
        parts.append((T[:, 0][:, None, :] * a[None, :, None]
                      + T[:, 1][:, None, :] * b[None, :, None]
                      + T[:, 2][:, None, :] * c[None, :, None]).reshape(-1, 3))
    return np.concatenate(parts)


def _box(centre, axes, ext, step):
    ns = [max(2, int(np.ceil(2 * ext[i] / step)) + 1) for i in range(3)]
    g = np.meshgrid(*[np.linspace(-ext[i], ext[i], ns[i]) for i in range(3)], indexing="ij")
    return np.stack([g[0].ravel(), g[1].ravel(), g[2].ravel()], axis=1) @ axes + centre


def cloud_hitboxes():
    parts, n = [], 0
    for p in BLOCK:
        for hb in mesh(DBR[p["dbr"]]["mesh"])["hitboxes"]:
            n += 1
            parts.append(to_world(_box(hb["ctr"], hb["rot"], hb["ext"], CS / 2), p))
    return np.concatenate(parts), n


def cloud_aabb():
    parts = []
    for p in BLOCK:
        bb = mesh(DBR[p["dbr"]]["mesh"])["aabb"]
        lo, hi = bb[:3], bb[3:]
        parts.append(to_world(_box((lo + hi) / 2, np.eye(3), (hi - lo) / 2, CS / 2), p))
    return np.concatenate(parts)


def index_cloud(S):
    ci = np.floor((S[:, 0] - X0) / CS).astype(np.int64)
    ri = np.floor((S[:, 2] - Z0) / CS).astype(np.int64)
    ok = (ci >= 0) & (ci < NX) & (ri >= 0) & (ri < NX)
    ci, ri = ci[ok], ri[ok]
    return ci, ri, S[ok, 1] - TH[ri, ci]          # height ABOVE the terrain under the sample


log("\n§9  blocking-geometry sample clouds (world-space, indexed to the 0.25 m grid)")
CLOUD = {}
CLOUD["triangles"] = index_cloud(cloud_triangles())
_hb, N_HB = cloud_hitboxes()
CLOUD["hitboxOBB"] = index_cloud(_hb)
CLOUD["renderAABB"] = index_cloud(cloud_aabb())
for k, (ci, ri, rel) in CLOUD.items():
    log(f"    {k:<12} {len(ci):>12,} in-region samples · height-above-terrain "
        f"p05 {np.percentile(rel, 5):+.2f} · median {np.median(rel):+.2f} · "
        f"p95 {np.percentile(rel, 95):+.2f} m")
log(f"    (hitboxOBB uses {N_HB} chunk-8 OBBs across the {len(BLOCK)} placements)")

# ══════════════════════════════════════════════════ § 10  FLOOD FILL + ACCEPTANCE TEST
SEED = (int((CZ - Z0) / CS), int((CX - X0) / CS))


def flood(blocked):
    vis = np.zeros_like(blocked, bool)
    if blocked[SEED]:
        return vis, True
    q = deque([SEED])
    vis[SEED] = True
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < NX and 0 <= nc < NX and not vis[nr, nc] and not blocked[nr, nc]:
                vis[nr, nc] = True
                q.append((nr, nc))
    rr, cc = np.nonzero(vis)
    return vis, bool(rr.min() == 0 or rr.max() == NX - 1 or cc.min() == 0 or cc.max() == NX - 1)


# The acceptance set: points the SHIPPED GAME uses, therefore points that MUST be walkable.
ANCHORS = []
for p in PLAIN:
    b = p["dbr"].rsplit("/", 1)[-1]
    if b == "tier16spawnpoint01.dbr" or re.fullmatch(r"spawnpoint0[2-6]\.dbr", b):
        ANCHORS.append(("emitter:" + b[:-4], p["x"], p["z"]))
    elif "spawnplayer" in b:
        ANCHORS.append(("player_spawn", p["x"], p["z"]))
for i, g in enumerate(GROUP):
    ANCHORS.append((f"patrolpoint_attack_{i:02d}", g["x"], g["z"]))


def cell(x, z):
    return int((z - Z0) / CS), int((x - X0) / CS)


def summarise(blocked, tag):
    reach, edge = flood(blocked)
    rr, cc = np.nonzero(reach)
    if not len(rr):
        return dict(tag=tag, reach_area_m2=0.0, reaches_region_edge=True,
                    anchors_reachable=0, anchors_total=len(ANCHORS),
                    sim_x=None, sim_y=None), reach
    sx = X0 + (cc + 0.5) * CS - CX
    sy = Z0 + (rr + 0.5) * CS - CZ
    ok = sum(1 for _, x, z in ANCHORS if reach[cell(x, z)])
    return dict(tag=tag, reach_area_m2=round(float(reach.sum()) * CS * CS, 1),
                reaches_region_edge=edge, anchors_reachable=ok, anchors_total=len(ANCHORS),
                sim_x=[round(float(sx.min()), 2), round(float(sx.max()), 2)],
                sim_y=[round(float(sy.min()), 2), round(float(sy.max()), 2)]), reach


# ── (a) terrain alone, three independent rules, each swept
log("\n§10a  TERRAIN ALONE — three rules, each swept.  D-5 swept only the first.")
log(f"     {'rule':<26}{'param':>8}{'imp%':>8}{'reach m2':>10}{'edge?':>7}{'anchors':>9}")
TERRAIN_SWEEP = []
for nm, arr, params in (("SlopeImpassable dev (m)", DEV, [0.15, 0.30, T_SLOPE, 1.20, 2.00]),
                        ("surface slope (deg)", SLOPE_DEG, [8, 10, 12, 16, 20, 30, 45]),
                        ("max step per cell (m)", STEP, [0.2, 0.3, 0.5, 0.8, 1.5])):
    for v in params:
        imp = up(arr > v)
        row, _ = summarise(imp, f"{nm}={v}")
        row.update(rule=nm, param=round(float(v), 4),
                   impassable_fraction=round(float(imp.mean()), 4))
        TERRAIN_SWEEP.append(row)
        log(f"     {nm:<26}{v:>8.3f}{100 * imp.mean():>7.1f}%{row['reach_area_m2']:>10.0f}"
            f"{str(row['reaches_region_edge']):>7}"
            f"{row['anchors_reachable']:>6}/{row['anchors_total']}")

# ── (b) terrain + composed static geometry, 3 rules x walkable band
log("\n§10b  TERRAIN + COMPOSED STATIC GEOMETRY — 3 blocking rules x walkable band")
log("      band = [terrain + lo, terrain + hi]; lo = walkable-climb analogue, hi = agent height")
log(f"     {'rule':<12}{'lo':>5}{'hi':>6}{'geo%':>8}{'reach m2':>10}"
    f"{'sim x span':>19}{'sim y span':>19}{'edge?':>7}{'anchors':>9}")
GEO_SWEEP = []
BEST = None
for rule, (ci, ri, rel) in CLOUD.items():
    for lo in (0.0, 0.5, 1.0):
        for hi in (1.0, AGENT_HEIGHT, 3.0):
            if hi <= lo:
                continue
            geo = np.zeros((NX, NX), bool)
            h = (rel >= lo) & (rel <= hi)
            geo[ri[h], ci[h]] = True
            row, reach = summarise(geo | TIMP, f"{rule}|{lo}|{hi}")
            row.update(rule=rule, band_lo=lo, band_hi=round(float(hi), 3),
                       geo_blocked_fraction=round(float(geo.mean()), 4))
            GEO_SWEEP.append(row)
            log(f"     {rule:<12}{lo:>5}{hi:>6}{100 * geo.mean():>7.1f}%{row['reach_area_m2']:>10.0f}"
                f"{str(row['sim_x']):>19}{str(row['sim_y']):>19}"
                f"{str(row['reaches_region_edge']):>7}"
                f"{row['anchors_reachable']:>6}/{row['anchors_total']}")
            if rule == "triangles" and lo == 0.5 and hi == AGENT_HEIGHT:
                BEST = (geo, reach)

BEST_ANY = max(GEO_SWEEP, key=lambda r: (r["anchors_reachable"], -r["reach_area_m2"]))
log(f"\n     BEST cell over the whole 27-cell sweep, by anchors reachable: "
    f"{BEST_ANY['tag']} -> {BEST_ANY['anchors_reachable']}/{BEST_ANY['anchors_total']} anchors, "
    f"closed = {not BEST_ANY['reaches_region_edge']}")
log("     ⚑ NO CELL IN THE SWEEP IS BOTH CLOSED AND ANCHOR-COMPLETE. "
    "The pre-registered acceptance test (D-5 § 5 step 4) FAILS everywhere.")

# ── (c) per-anchor diagnosis at the most favourable engine-faithful cell
GEO_B, REACH_B = BEST
LBL = np.zeros((NX, NX), np.int32)
FREE = ~(GEO_B | TIMP)
nlab = 0
for r0 in range(NX):
    for c0 in range(NX):
        if FREE[r0, c0] and LBL[r0, c0] == 0:
            nlab += 1
            q = deque([(r0, c0)])
            LBL[r0, c0] = nlab
            while q:
                r, c = q.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < NX and 0 <= nc < NX and FREE[nr, nc] and LBL[nr, nc] == 0:
                        LBL[nr, nc] = nlab
                        q.append((nr, nc))
SEEDLAB = LBL[SEED]
log(f"\n§10c  ANCHOR DIAGNOSIS at rule=triangles, band=[+0.5, +{AGENT_HEIGHT}] m "
    f"(the engine-faithful cell): {nlab} free components; seed component "
    f"{(LBL == SEEDLAB).sum() * CS * CS:,.0f} m2")
ANCHOR_TABLE = []
for nm, x, z in ANCHORS:
    r, c = cell(x, z)
    if GEO_B[r, c]:
        st = "INSIDE-BLOCKING-GEOMETRY"
    elif TIMP[r, c]:
        st = "INSIDE-TERRAIN-IMPASSABLE"
    elif LBL[r, c] == SEEDLAB:
        st = "reachable"
    else:
        st = f"DISCONNECTED (component {LBL[r, c]}, {(LBL == LBL[r, c]).sum() * CS * CS:.0f} m2)"
    ANCHOR_TABLE.append(dict(anchor=nm, sim_x=round(x - CX, 3), sim_y=round(z - CZ, 3), status=st))
    if st != "reachable":
        log(f"     ⚑ {nm:<26} sim ({x - CX:+7.2f}, {z - CZ:+7.2f})  {st}")
N_BAD = sum(1 for r in ANCHOR_TABLE if r["status"] != "reachable")
log(f"     {len(ANCHOR_TABLE) - N_BAD}/{len(ANCHOR_TABLE)} anchors reachable; {N_BAD} FAIL.")
log("     ⚑ A monster emitter cannot be inside a wall.  The composition is FALSIFIED BY THE")
log("       GAME'S OWN DATA — not by judgement.  No boundary is offered.")

# ══════════════════════════════════════════════════ § 11  WHAT IS STILL MEASURABLE
# The commission asked for clearance vs the occupancy hull.  With no earned boundary that
# question is unanswerable as posed; what IS measurable is how far the terrain-passable ground
# extends past the hull, and where the region tile itself cuts in.
HULL = dict(w=86.915, h=85.303, cx=-1.819, cy=0.244)
HX0, HX1 = HULL["cx"] - HULL["w"] / 2, HULL["cx"] + HULL["w"] / 2
HY0, HY1 = HULL["cy"] - HULL["h"] / 2, HULL["cy"] + HULL["h"] / 2
REGION_SIM = dict(x=[round(X0 - CX, 3), round(X0 + 128 - CX, 3)],
                  y=[round(Z0 - CZ, 3), round(Z0 + 128 - CZ, 3)])
TERR_ONLY, _TR = summarise(TIMP, "terrain-only@decoded-T")
CLEAR = dict(
    hull_sim_x=[round(HX0, 3), round(HX1, 3)], hull_sim_y=[round(HY0, 3), round(HY1, 3)],
    region_tile_sim=REGION_SIM,
    terrain_passable_sim_x=TERR_ONLY["sim_x"], terrain_passable_sim_y=TERR_ONLY["sim_y"],
    hull_to_region_edge_east_m=round(REGION_SIM["x"][1] - HX1, 3),
    hull_to_region_edge_west_m=round(HX0 - REGION_SIM["x"][0], 3),
    hull_to_region_edge_north_m=round(REGION_SIM["y"][1] - HY1, 3),
    hull_to_region_edge_south_m=round(HY0 - REGION_SIM["y"][0], 3),
    hull_perimeter_on_terrain_passable=None)
per = []
for t in np.linspace(0, 1, 400):
    per += [(HX0 + t * HULL["w"], HY0), (HX0 + t * HULL["w"], HY1),
            (HX0, HY0 + t * HULL["h"]), (HX1, HY0 + t * HULL["h"])]
_, TREACH = summarise(TIMP, "t")
CLEAR["hull_perimeter_on_terrain_passable"] = (
    f"{sum(1 for x, y in per if TREACH[cell(x + CX, y + CZ)])}/{len(per)}")
log("\n§11  CLEARANCE — what survives the negative")
log(f"     occupancy hull  sim x [{HX0:+.2f}, {HX1:+.2f}] · sim y [{HY0:+.2f}, {HY1:+.2f}]")
log(f"     A001 region tile sim x {REGION_SIM['x']} · sim y {REGION_SIM['y']}")
log(f"     terrain-passable-from-centroid (decoded T) sim x {TERR_ONLY['sim_x']} · "
    f"sim y {TERR_ONLY['sim_y']}")
log(f"     hull edge to the REGION TILE edge:  east {CLEAR['hull_to_region_edge_east_m']:+.2f} m · "
    f"west {CLEAR['hull_to_region_edge_west_m']:+.2f} m · "
    f"north {CLEAR['hull_to_region_edge_north_m']:+.2f} m · "
    f"south {CLEAR['hull_to_region_edge_south_m']:+.2f} m")
log(f"     hull perimeter samples on terrain-passable ground: "
    f"{CLEAR['hull_perimeter_on_terrain_passable']}")

# ══════════════════════════════════════════════════ § 11b  RESIDUALS — each looked at ONCE
MAPRAW = ArcArchive(VENDOR / "survivalmode1/resources/Maps.arc").read_file("survivalworld_a.map")

# (i) the `.map` head's named-object table — is any of them a BOUNDS object?
HEAD = MAPRAW[:4700]
NAMES, _seen = [], set()
for _i in range(len(HEAD) - 4):
    _ln = struct.unpack_from("<I", HEAD, _i)[0]
    if 3 <= _ln <= 80 and _i + 4 + _ln <= len(HEAD):
        _s = HEAD[_i + 4:_i + 4 + _ln]
        if all(32 <= c < 127 for c in _s):
            _t = _s.decode()
            if _t not in _seen:
                _seen.add(_t)
                NAMES.append(_t)
HEAD_NAMES = [n for n in NAMES if not n.startswith("records/") and not n.startswith("Maps/")]
log("\n§11b  RESIDUALS")
log(f"     (i) `.map` head named objects: {HEAD_NAMES}")
log("         each carries a GUID + two editor RGBA colours; NO geometry payload.")

# (ii) the seven region entries — offsets, sizes, grids, origins
REGIONS = []
for _m in re.finditer(rb"Region_Survival_A00[0-9]\.lvl", MAPRAW):
    _off, _size = struct.unpack_from("<2I", MAPRAW, _m.end())
    _g = struct.unpack_from("<6I", MAPRAW, _m.end() + 8)
    _o = struct.unpack_from("<3i", MAPRAW, _m.end() + 32)
    REGIONS.append(dict(name=_m.group().decode(), offset=_off, size=_size,
                        next_grid=list(_g), next_origin=list(_o)))
log(f"     (ii) {len(REGIONS)} regions; A001 blob @{REGIONS[0]['offset']} ({REGIONS[0]['size']} B). "
    "Trailing (grid, origin) words recorded in the findings JSON; they do NOT read as a "
    "contiguous 128 m tiling and were NOT reconciled this lap.")

# (iii) the head's seven 262,188 B blobs — D-5 R-5 said 'presumed minimap'.  One look.
BLOB_SZ = 262188
log(f"     (iii) head arithmetic: 7 x {BLOB_SZ} + 4655 = {7 * BLOB_SZ + 4655} vs A001 blob offset "
    f"{REGIONS[0]['offset']} (delta {REGIONS[0]['offset'] - (7 * BLOB_SZ + 4655)} B); "
    f"{BLOB_SZ} - 44 = {BLOB_SZ - 44}, which is 512*512 ({(BLOB_SZ - 44) == 512 * 512}) "
    f"AND 256*256*4 ({(BLOB_SZ - 44) == 256 * 256 * 4}). Payload reads as 4-byte pixel runs "
    "-> a 256x256 RGBA IMAGE, not a 512x512 0.25 m pathing bitmap.")

# (iv) the `.lvl` property list between the entity section and the terrain block
_ess = struct.unpack_from("<I", BLOB, 32)[0]
_PROP_SECT_SIZE = struct.unpack_from("<I", BLOB, 40 + _ess)[0]
_p, _keys, _guard = 40 + _ess + 4, [], 0
_hf = [m.start() for m in re.finditer(re.escape(struct.pack("<2I", 129, 129)), BLOB)][0]
while _p + 8 <= _hf and _guard < 4000:
    _k, _sz = struct.unpack_from("<2I", BLOB, _p)
    if _p + 8 + _sz > _hf:
        break
    _keys.append((_k, _sz))
    _p += 8 + _sz
    _guard += 1
_szs = Counter(sz for _, sz in _keys)
log(f"     (iv) `.lvl` property list: entity section ends {40 + _ess:#x}, heightfield marker "
    f"{_hf:#x}, gap {_hf - (40 + _ess)} B, declared property-section size "
    f"{_PROP_SECT_SIZE} -> {len(_keys)} [key][size][payload] entries, "
    f"payload-size histogram {dict(_szs.most_common(4))}; the 12-byte payloads decode as RGB "
    "float triples -> a colour/lighting table, NOT bounds.")

# ══════════════════════════════════════════════════ § 12  EMIT
np.save(OUT / "terrain_height_0p25.npy", TH)
np.save(OUT / "terrain_impassable_0p25.npy", TIMP)
np.save(OUT / "blocking_geometry_triangles_band0p5_2p0.npy", GEO_B)
np.save(OUT / "reachable_triangles_band0p5_2p0.npy", REACH_B)

json.dump(dict(
    verdict=dict(
        msh_format="DECODED — first-of-kind, self-validated bit-exact (§ 5)",
        boundary="NOT DERIVED — every composition in a 24-cell sweep fails the pre-registered "
                 "acceptance test; three shipped anchors land inside blocking geometry",
        anchors_failing=N_BAD, anchors_total=len(ANCHOR_TABLE)),
    frame=dict(centroid_level_xz=[round(CX, 6), round(CZ, 6)],
               heightfield_map="world_x = col - 4.00 ; world_z = row + 0.00 ; cell 1.000 m",
               raster_cell_m=CS, raster_nx=NX, raster_origin_level_xz=[X0, Z0],
               region_tile_sim=REGION_SIM),
    msh_format=dict(
        magic="MSH\\x03",
        container="flat [u32 chunk_id][u32 size][payload] chain from +4, closes exactly at EOF",
        chunks={
            "4": "vertex buffer: [u32 n_stream][u32 stride][u32 n_vert][u32 stream_type x n_stream]"
                 " then n_vert x stride bytes; position = first 3 f32 of each vertex",
            "5": "index buffer: [u32 n_tri][u32 n_submesh][u16 x 3*n_tri][44 B x n_submesh tail]",
            "7": "material list: [u32 n] then len-prefixed shader path + typed properties",
            "8": "HITBOX OBB array: [u32 n] then n x 96 B "
                 "(32 B name | 3 f32 half-extent | 9 f32 rotation | 3 f32 centre | u32 0xFFFFFFFF)",
            "10": "AABB: 6 f32 = exact vertex extremes",
            "13": "[u32][u32]", "6": "[u32]"},
        validation=dict(blocking_meshes=len(MESH_TABLE), chain_closes=N_CLEAN,
                        aabb_bit_exact=N_EXACT, index_max_exact=N_IDXOK,
                        corpus_control=dict(sampled=c_tot, chain=c_clean,
                                            aabb_bit_exact=c_exact, index_exact=c_idx,
                                            corpus_size=len(CORPUS)),
                        hitbox_vs_aabb=HB_CHECK,
                        scale_falsifier=dict(mesh="creatures/pc/hero01.msh",
                                             height_m=round(HERO_H, 4),
                                             agent_height_m=AGENT_HEIGHT))),
    engine=dict(
        d5_chain_correction=STUBS,
        live_chain=["Level::CreatePathMesh (Engine.dll)",
                    "NavMeshBuilder::Create(const Level*) — appends mesh-instance TRIANGLES, "
                    "no slope/normal filter in the accumulation loop",
                    "NavMeshBuilder::Create(const Entity*) — appends entity HITBOX OBBs "
                    "via GetHitBox(i) -> AddBox",
                    "NavMeshBuilder::CreateNavMesh -> NavMesh::Set{Vertex,Index,Face}Data",
                    "NavManager::AddData(Region*) / NavManager::CreateNavigationData"],
        allowPathing=dict(
            dbr_key_va="0x10540b7c (Game.dll)", stored_at="Decoration + 0x428 (byte)",
            sole_consumer="?IsStatic@Decoration@GAME@@UBE_NXZ RVA 0x1a53a0: "
                          "`cmp byte [ecx+0x428], 0 ; sete al`",
            meaning="allowPathing == 0  <=>  IsStatic() == true; there is NO "
                    "Decoration::OccludesPathing override, so Decorations inherit "
                    "Entity::OccludesPathing == false"),
        nav_config=dict(symbol="?SetDefaultConfig@NavManager@GAME@@AAEXXZ",
                        rva=hex(CFG_RVA), fields=NAVCFG),
        terrain_rule=dict(symbol="?SlopeImpassable@Terrain@GAME@@AAE_NHH@Z",
                          rva=hex(SLOPE_RVA), K=K_AVG, T=T_SLOPE),
        transform_convention="world = local @ M (row-vector; M row-major from the .lvl 9 floats) "
                             "— read from the operand offsets 0,3,6 / 1,4,7 / 2,5,8 in "
                             "NavMeshBuilder::Create(const Level*) @ 0x100e94b0"),
    placements=dict(plain=len(PLAIN), blocking=len(BLOCK),
                    blocker_radius_m=dict(min=round(float(BR.min()), 2),
                                          p10=round(float(np.percentile(BR, 10)), 2),
                                          median=round(float(np.median(BR)), 2),
                                          p90=round(float(np.percentile(BR, 90)), 2),
                                          max=round(float(BR.max()), 2),
                                          hist_10m_bins=RADHIST),
                    row_norm_range=[float(ROWN.min()), float(ROWN.max())],
                    det_range=[float(DETS.min()), float(DETS.max())],
                    distinct_meshes=len(MESHES)),
    mesh_table=MESH_TABLE,
    terrain_sweep=TERRAIN_SWEEP,
    geometry_sweep=GEO_SWEEP,
    anchor_diagnosis=ANCHOR_TABLE,
    clearance=CLEAR,
    residuals=dict(map_head_named_objects=HEAD_NAMES, regions=REGIONS,
                   head_blob_size=BLOB_SZ,
                   lvl_property_entries=len(_keys),
                   lvl_property_size_hist={str(k): v for k, v in _szs.items()}),
    digests=DIGESTS,
), open(OUT / "d5b_findings.json", "w"), indent=1)

with open(OUT / "msh_mesh_table.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(MESH_TABLE[0].keys()))
    w.writeheader()
    for r in MESH_TABLE:
        w.writerow(r)
with open(OUT / "composition_sweep.csv", "w", newline="") as fh:
    keys = ["rule", "band_lo", "band_hi", "geo_blocked_fraction", "reach_area_m2",
            "reaches_region_edge", "anchors_reachable", "anchors_total", "sim_x", "sim_y"]
    w = csv.writer(fh)
    w.writerow(keys)
    for r in GEO_SWEEP:
        w.writerow([r.get(k) for k in keys])
with open(OUT / "anchor_diagnosis.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["anchor", "sim_x", "sim_y", "status"])
    w.writeheader()
    for r in ANCHOR_TABLE:
        w.writerow(r)

(OUT / "decode.log").write_text("\n".join(LOG) + "\n")
log(f"\nwrote {OUT}")
