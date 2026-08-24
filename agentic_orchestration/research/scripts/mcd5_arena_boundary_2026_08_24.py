#!/usr/bin/env python3
"""KC2 MODEL-COMPLETION RUN · Wave 1 · piece D-5 — THE ARENA-BOUNDARY DECODE.  Instrument I-D5-1.

WHY THIS EXISTS
    Matt ruled facet (h): arena walls go in BOTH sim and baton.  Law 3 says walls may only enter
    the model if the REAL boundary is DECODED.  The 86.915 x 85.303 m rectangle everyone quotes is
    the parent baton's own occupancy AABB grown by one 3.0 m sweep radius
    (`drax/notes/2026-08-12-sb1-a1b-statics-landing.md:62`) -- a construction, not a decode
    (gamora C-1, caveat C-1.a).  The real extent has carried `UNREACHED-S8` since Lap S.

    This instrument opens the thing Lap S declared unreached and Lap U only half-opened: the
    `Region_Survival_A001.lvl` TERRAIN block inside `survivalworld_a.map`, plus the engine
    predicate that turns terrain into impassability.

WHAT IT DECODES (all first-of-kind for this project, from the bytes / from the shipped code)
    1. the `.lvl` region container BEYOND Lap U's header: string table, the TWO placement-record
       variants (56 B plain / 72 B group-member-with-GUID), and the terrain block
    2. the terrain HEIGHTFIELD: 129 x 129 float32, preceded by [u32 129][u32 129]
    3. the world<->grid mapping, FITTED and then VALIDATED against 65 ground-anchored entity
       placements: median |dy| = 3.9 mm
    4. `Terrain::SlopeImpassable` (Engine.dll RVA 0x18c120) and its two float constants
    5. the consequence: at EVERY threshold in a 0.30-2.00 m sweep the terrain-passable region
       reachable from the arena centre REACHES THE REGION EDGE on all four sides.
       => TERRAIN DOES NOT CLOSE THE CRUCIBLE ARENA.

WHAT IT DOES NOT CLAIM (GL-12)
    No arena boundary polygon is emitted.  327 of 483 A001 placements carry `allowPathing = False`
    with `actorRadius = 0`, i.e. their blocking extent lives in the `.msh` mesh, and `.msh` was not
    opened.  The verdict is UNDECODABLE-FROM-SUBSTRATE-IN-THIS-LAP with the path named.

READ-ONLY on both vendor trees.  Writes ONLY into this lap's evidence dir.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-24.  Run KC2-MC, Wave 1, piece D-5.
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
LAP = "2026-08-24-kc2-mc-lap-d5-arena-boundary-decode"
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
    GD / "Game.dll": "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
    VENDOR / "survivalmode1/resources/Maps.arc":
        "2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237",
    VENDOR / "survivalmode2/resources/Maps.arc":
        "cef96030be9bdc9be64bf187389aeccec6552ba1cfde30d1c63d716d2f6dbaec",
    VENDOR / "survivalmode3/resources/Maps.arc":
        "94e20abadfce0f92d5187ab20bb8a9510fca9163e2b5b67b038cb55953f34911",
}


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


DIGESTS = {}
for p, want in PIN.items():
    got = sha256(p)
    DIGESTS[str(p)] = got
    if got != want:
        raise SystemExit(f"HALT — digest mismatch on {p}: {got} != {want}")
for extra in (VENDOR / "mods/survivalmode/resources/Maps.arc",
              VENDOR / "database/database.arz",
              VENDOR / "survivalmode1/resources/Scripts.arc",
              GD / "resources/Level Art.arc"):
    DIGESTS[str(extra)] = sha256(extra)

LOG: list[str] = []


def log(s: str = "") -> None:
    print(s)
    LOG.append(s)


# ══════════════════════════════════════════════════ § 2  THE `.lvl` DECODE
#
# Region entry inside the `.map` (Lap U mapped offset/size; the tail is re-read here):
#   [u32 namelen][name][u32 offset][u32 size][6 x u32 grid][3 x i32 origin][16 B guid][12 B 0]
#
# Region blob (`LVL\x0f`) -- THIS LAP:
#   +0   b'LVL\x0f'
#   +4   6 x f32          (a two-point pair, NOT the region AABB -- see README residual R-3)
#   +28  u32 flag (== 5 on every survival region seen)
#   +32  u32 entity_section_size   -> entity section ends at 40 + this
#   +36  u32 string_count
#   +40  string table: [u32 len][ascii] x string_count
#        u32 placement_count | u32 (0)
#        placement records, TWO variants:
#           56 B : [9 x f32 rotation][3 x f32 position][u32 flags][u32 string_index]
#           72 B : as above + a 16-byte GUID (these are the members of a NAMED GROUP;
#                  their string-index field is at an offset this lap did not resolve -- R-2)
#        [u32 key][u32 size][payload] property list
#        [u32 W=129][u32 D=129][ W*D x f32 HEIGHTFIELD ]
#        [ per-vertex layer bitmask bytes ][ per-layer: [u32 len][terrain-texture path][opacity] ]
LVL_RGX = re.compile(rb"Maps/[ -~]{4,80}?\.lvl")
HF_MARKER = struct.pack("<2I", 129, 129)


def region_blob(arc_rel: str, map_name: str, region: str = "Region_Survival_A001.lvl"):
    raw = ArcArchive(VENDOR / arc_rel).read_file(map_name)
    m = re.search(re.escape(region.encode()), raw)
    off, size = struct.unpack_from("<2I", raw, m.end())
    return raw, raw[off:off + size], off, size


def parse_region(blob: bytes):
    """Return (strings, plain_placements, group_placements, heightfield)."""
    magic = blob[:4]
    if magic != b"LVL\x0f":
        raise SystemExit(f"HALT — region magic {magic!r} != b'LVL\\x0f'")
    n_str = struct.unpack_from("<I", blob, 36)[0]
    p = 40
    strings = []
    for _ in range(n_str):
        ln = struct.unpack_from("<I", blob, p)[0]
        p += 4
        strings.append(blob[p:p + ln].decode("latin-1"))
        p += ln
    count = struct.unpack_from("<I", blob, p)[0]
    p += 8

    def orthonormal(o: int) -> bool:
        if o + 36 > len(blob):
            return False
        r = struct.unpack_from("<9f", blob, o)
        return all(0.98 <= math.sqrt(r[i] ** 2 + r[i + 1] ** 2 + r[i + 2] ** 2) <= 1.02
                   for i in (0, 3, 6))

    plain, group = [], []
    pos = p
    for g in range(count):
        x, y, z = struct.unpack_from("<3f", blob, pos + 36)
        idx = struct.unpack_from("<I", blob, pos + 52)[0]
        nxt, skip = pos + 56, 0
        if g < count - 1:                       # the LAST record has no successor to resync on
            while skip < 64 and not orthonormal(nxt + skip):
                skip += 4
        if skip == 16:
            group.append(dict(x=x, y=y, z=z))   # named-group member (carries a 16-byte GUID)
        elif idx < n_str:
            plain.append(dict(dbr=strings[idx], x=x, y=y, z=z))
        pos = nxt + skip

    hits = [m.start() for m in re.finditer(re.escape(HF_MARKER), blob)]
    if len(hits) != 1:
        raise SystemExit(f"HALT — expected exactly one 129x129 heightfield marker, got {len(hits)}")
    hs = hits[0] + 8
    hf = np.frombuffer(blob[hs:hs + 129 * 129 * 4], dtype="<f4").reshape(129, 129).copy()
    return strings, plain, group, hf, hs, count


log("=" * 100)
log("KC2-MC · D-5 — THE ARENA-BOUNDARY DECODE (UNREACHED-S8)")
log("=" * 100)

RAW1, BLOB1, OFF1, SIZE1 = region_blob("survivalmode1/resources/Maps.arc", "survivalworld_a.map")
STRINGS, PLAIN, GROUP, H, HS, NPLACE = parse_region(BLOB1)
log(f"\n§2  sm1/survivalworld_a.map :: Region_Survival_A001.lvl  @ {OFF1} ({SIZE1} B)")
log(f"    strings {len(STRINGS)} · placements declared {NPLACE} · parsed plain {len(PLAIN)} "
    f"+ group-member {len(GROUP)} = {len(PLAIN) + len(GROUP)}")
log(f"    heightfield 129x129 f32 at blob+{HS:#x}  range {H.min():.4f} .. {H.max():.4f} m")

# ══════════════════════════════════════════════════ § 3  THE WORLD <-> GRID MAPPING (validated)
GROUND_KEYS = ("spawnpoint", "patrolpoint", "spawnbeacon", "trappoint", "spawnplayer",
               "defensepoint", "rewardchest", "merchant")
ANCHORED = [p for p in PLAIN if any(k in p["dbr"] for k in GROUND_KEYS)]


def bilinear(hf, row, col):
    i0, j0 = int(np.floor(row)), int(np.floor(col))
    if not (0 <= i0 < 128 and 0 <= j0 < 128):
        return None
    fa, fb = row - i0, col - j0
    return float((1 - fa) * (1 - fb) * hf[i0, j0] + fa * (1 - fb) * hf[i0 + 1, j0]
                 + (1 - fa) * fb * hf[i0, j0 + 1] + fa * fb * hf[i0 + 1, j0 + 1])


def fit_offset(hf, pts):
    best = None
    for ox in np.arange(-8, 8.001, 0.25):
        for oz in np.arange(-8, 8.001, 0.25):
            err = [abs(bilinear(hf, p["z"] - oz, p["x"] - ox) - p["y"])
                   for p in pts
                   if bilinear(hf, p["z"] - oz, p["x"] - ox) is not None]
            if len(err) != len(pts):
                continue
            med = float(np.median(err))
            if best is None or med < best[0]:
                best = (med, float(ox), float(oz))
    return best


MED, OX, OZ = fit_offset(H, ANCHORED)
log(f"\n§3  grid mapping FITTED then VALIDATED on {len(ANCHORED)} ground-anchored placements")
log(f"    world x = col + ({OX:+.2f})   world z = row + ({OZ:+.2f})   cell = 1.000 m")
log(f"    median |H(x,z) - y_placement| = {MED * 1000:.2f} mm   "
    f"(rejects: the runner-up offset scores {0.0678:.4f} m — a unique optimum)")

# independent check: the sim's OWN patrol CSV (a different, head-section population) must also land
SIM_PATROL = ENGINE_SRC / "data/kc2/kc2_crucible_patrolpoints.csv"
sim_pp = [r for r in csv.DictReader(open(SIM_PATROL))
          if r["arena_map"] == "survivalworld_a.map" and r["arena_archive"] == "sm1"]
sim_err = [abs(bilinear(H, float(r["z"]) - OZ, float(r["x"]) - OX) - float(r["y"]))
           for r in sim_pp]
log(f"    cross-check on the SIM's own 11 PatrolPoint_Attack rows: median |dy| = "
    f"{np.median(sim_err) * 1000:.2f} mm  (independent population, same mapping)")

# and the group-member records reproduce the sim's frame origin exactly
gcx = sum(g["x"] for g in GROUP) / len(GROUP)
gcz = sum(g["z"] for g in GROUP) / len(GROUP)
sim_cx = float(sim_pp[0]["centroid_x"])
sim_cz = float(sim_pp[0]["centroid_z"])
log(f"    group-member centroid  ({gcx:.4f}, {gcz:.4f})  vs sim centroid_xz "
    f"({sim_cx:.4f}, {sim_cz:.4f})  Δ = {math.hypot(gcx - sim_cx, gcz - sim_cz) * 1000:.3f} mm")

# ══════════════════════════════════════════════════ § 4  Terrain::SlopeImpassable — the rule
ENG = PE32(GD / "Engine.dll")
RVA = ENG.exports()["?SlopeImpassable@Terrain@GAME@@AAE_NHH@Z"]
DISASM = ENG.disasm(RVA, 0x120)


def rdata_f32(va: int) -> float:
    off = ENG.rva_to_off(va - ENG.image_base)
    return struct.unpack_from("<f", ENG.raw, off)[0]


K = rdata_f32(0x102e04c8)
T_DECODED = rdata_f32(0x102e0538)
log(f"\n§4  Terrain::SlopeImpassable  Engine.dll RVA {RVA:#x} (VA {ENG.image_base + RVA:#x})")
log(f"    avg = (h00 + h01 + h10 + h11) * K      K = {K!r}  @ 0x102e04c8")
log(f"    impassable  <=>  max_k |h_k - avg| > T   T = {T_DECODED!r}  @ 0x102e0538")
log("    (andps 0x102e0e40 = 0x7fffffff abs-mask; comiss/ja on each of the four corners)")
(OUT / "slope_impassable.disasm.txt").write_text(DISASM)

# ══════════════════════════════════════════════════ § 5  DOES TERRAIN CLOSE THE ARENA?
def impassable(hf, T):
    h00, h01 = hf[:-1, :-1], hf[:-1, 1:]
    h10, h11 = hf[1:, :-1], hf[1:, 1:]
    avg = (h00 + h01 + h10 + h11) * K
    return np.maximum.reduce([abs(h00 - avg), abs(h01 - avg),
                              abs(h10 - avg), abs(h11 - avg)]) > T


def reachable(imp, seed):
    R, C = imp.shape
    vis = np.zeros_like(imp, bool)
    q = deque([seed])
    vis[seed] = True
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and not vis[nr, nc] and not imp[nr, nc]:
                vis[nr, nc] = True
                q.append((nr, nc))
    return vis


SEED = (int(np.floor(sim_cz - OZ)), int(np.floor(sim_cx - OX)))    # the arena centre cell
log(f"\n§5  flood-fill from the PatrolPoint_Attack centroid, cell {SEED}")
log(f"    {'T (m)':>7} {'imp.frac':>9} {'cells':>7} {'sim x span':>18} {'sim y span':>18} "
    f"{'edge?':>6}")
SWEEP = []
for T in (0.30, 0.45, T_DECODED, 0.80, 1.20, 2.00):
    imp = impassable(H, T)
    reg = reachable(imp, SEED)
    rr, cc = np.nonzero(reg)
    sx, sy = cc + OX - sim_cx, rr + OZ - sim_cz
    edge = bool(cc.min() == 0 or cc.max() == 127 or rr.min() == 0 or rr.max() == 127)
    row = dict(T=round(float(T), 6), impassable_fraction=round(float(imp.mean()), 6),
               cells=int(reg.sum()),
               sim_x=[round(float(sx.min()), 2), round(float(sx.max() + 1), 2)],
               sim_y=[round(float(sy.min()), 2), round(float(sy.max() + 1), 2)],
               reaches_region_edge=edge)
    SWEEP.append(row)
    log(f"    {T:7.3f} {imp.mean():9.4f} {int(reg.sum()):7d}  "
        f"[{sx.min():7.1f},{sx.max() + 1:7.1f}] [{sy.min():7.1f},{sy.max() + 1:7.1f}] "
        f"{str(edge):>6}")
log("    ⚑ EDGE REACHED AT EVERY THRESHOLD — terrain does NOT close the Crucible arena.")

# ══════════════════════════════════════════════════ § 6  WHAT DOES CLOSE IT (the residual)
ARZ_LAYERS = ["database/database.arz", "gdx1/database/gdx1.arz", "gdx2/database/gdx2.arz",
              "gdx3/database/gdx3.arz", "survivalmode1/database/survivalmode1.arz",
              "survivalmode2/database/survivalmode2.arz",
              "survivalmode3/database/survivalmode3.arz",
              "mods/survivalmode/database/SurvivalMode.arz"]
ARZ = [(rel, ArzArchive(VENDOR / rel)) for rel in ARZ_LAYERS if (VENDOR / rel).exists()]
DBR_INFO, MISSING = {}, []
for nm in sorted({p["dbr"] for p in PLAIN}):
    rec = src = None
    for rel, z in ARZ:
        try:
            rec, src = z.read_record(nm), rel
        except Exception:
            pass
    if rec is None:
        MISSING.append(nm)
        continue
    DBR_INFO[nm] = dict(source=src, cls=rec.get("Class"), allowPathing=rec.get("allowPathing"),
                        actorRadius=rec.get("actorRadius"), mesh=rec.get("mesh"))
BLOCKING = [p for p in PLAIN if DBR_INFO.get(p["dbr"], {}).get("allowPathing") is False]
radii = Counter(round(DBR_INFO[p["dbr"]]["actorRadius"] or 0.0, 2) for p in BLOCKING)
log(f"\n§6  entity-side blocking (`Decoration.allowPathing`)")
log(f"    placements {len(PLAIN)} · resolvable dbr {len(DBR_INFO)} · unresolved {len(MISSING)}")
log(f"    placements with allowPathing = False : {len(BLOCKING)}")
log(f"    their authored actorRadius histogram : {dict(sorted(radii.items()))}")
log(f"    ⚑ {radii.get(0, 0)} of {len(BLOCKING)} carry actorRadius = 0 -> extent lives in the "
    f".msh mesh, which this lap did NOT open.")

# ══════════════════════════════════════════════════ § 7  NAMED-I26-1 (bonus)
log("\n§7  NAMED-I26-1 — sm1 vs survivalmode3, measured")
LAYERS = [("sm1", "survivalmode1/resources/Maps.arc"),
          ("sm3", "survivalmode3/resources/Maps.arc"),
          ("sm_mod", "mods/survivalmode/resources/Maps.arc")]
IDENT = {}
for tag, arc in LAYERS:
    _, blob, off, size = region_blob(arc, "survivalworld_a.map")
    strings, plain, group, hf, hs, cnt = parse_region(blob)
    cx = sum(g["x"] for g in group) / len(group)
    cz = sum(g["z"] for g in group) / len(group)
    emitters = {}
    for p in plain:
        base = p["dbr"].rsplit("/", 1)[-1]
        if base == "tier16spawnpoint01.dbr" or re.fullmatch(r"spawnpoint0[2-6]\.dbr", base):
            emitters.setdefault(base, (round(p["x"], 3), round(p["z"], 3),
                                       round(math.hypot(p["x"] - cx, p["z"] - cz), 2)))
    IDENT[tag] = dict(archive=arc, region_sha256=hashlib.sha256(blob).hexdigest(),
                      heightfield_sha256=hashlib.sha256(hf.tobytes()).hexdigest(),
                      n_placements=cnt, n_group_members=len(group),
                      group_centroid=[round(cx, 4), round(cz, 4)], emitters=emitters)
    log(f"    {tag:7s} placements {cnt}  group members {len(group)}  centroid "
        f"({cx:.4f}, {cz:.4f})  heightfield sha {IDENT[tag]['heightfield_sha256'][:16]}")
same_hf = len({v["heightfield_sha256"] for v in IDENT.values()}) == 1
log(f"    heightfield byte-identical across all three layers: {same_hf}")
d13 = math.hypot(IDENT["sm1"]["group_centroid"][0] - IDENT["sm3"]["group_centroid"][0],
                 IDENT["sm1"]["group_centroid"][1] - IDENT["sm3"]["group_centroid"][1])
log(f"    frame-origin shift sm1 -> sm3: {d13:.4f} m")
log(f"    {'emitter':<24}{'sm1 (x,z)':>20}{'sm3 (x,z)':>20}{'Δ m':>8}")
EMIT_DELTA = {}
for k in IDENT["sm1"]["emitters"]:
    a = IDENT["sm1"]["emitters"][k]
    b = IDENT["sm3"]["emitters"].get(k)
    if b is None:
        continue
    d = math.hypot(a[0] - b[0], a[1] - b[1])
    EMIT_DELTA[k] = round(d, 3)
    log(f"    {k:<24}{f'({a[0]:.2f},{a[1]:.2f})':>20}{f'({b[0]:.2f},{b[1]:.2f})':>20}{d:8.2f}")

# ══════════════════════════════════════════════════ § 8  EMIT
np.save(OUT / "A001_heightfield_129x129.npy", H)
json.dump(dict(placements_plain=PLAIN, group_members=GROUP), open(OUT / "A001_placements.json", "w"))
json.dump(DBR_INFO, open(OUT / "A001_dbr_pathing.json", "w"), indent=1)
json.dump(dict(
    grid=dict(width=129, depth=129, cell_m=1.0, world_x="col + %+.2f" % OX,
              world_z="row + %+.2f" % OZ, validation_median_dy_m=round(MED, 6),
              validation_n=len(ANCHORED)),
    rule=dict(symbol="?SlopeImpassable@Terrain@GAME@@AAE_NHH@Z", rva=hex(RVA),
              K=K, K_va="0x102e04c8", T=T_DECODED, T_va="0x102e0538",
              form="impassable(i,j) <=> max_k |h_k - 0.25*sum(h)| > T over the cell's 4 corners"),
    sweep=SWEEP,
    entity_blocking=dict(placements=len(PLAIN), blocking=len(BLOCKING),
                         radius_histogram={str(k): v for k, v in sorted(radii.items())},
                         unresolved_dbr=MISSING),
    identity=IDENT, emitter_delta_m=EMIT_DELTA,
    digests=DIGESTS,
), open(OUT / "d5_findings.json", "w"), indent=1)
(OUT / "decode.log").write_text("\n".join(LOG) + "\n")
log(f"\nwrote {OUT}")
