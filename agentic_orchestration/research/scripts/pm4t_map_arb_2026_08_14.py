#!/usr/bin/env python3
"""
pm4t_map_arb_2026_08_14.py — RUN KC2-PM4 LAP T, INSTRUMENT I-T3.

LIMB (c): ARBITRATE `D-I19-3`.

Gamora (I-19) reports that two decodes of the SAME `.map` file agree on spawn points to 5.1e-4
and on patrol-point COUNT (11), but disagree on patrol-point POSITIONS by 0.45-13.28 m
(median 3.44), with centroids 2.65 m apart. One of the two parties is Lap S's
`pm4s_map_2026_08_14.py` -- MY OWN INSTRUMENT. This module audits it.

THE TWO STRUCTURES (both decoded here, from the same byte buffer, whose sha256 is recorded)

  READING A -- HEAD-SECTION GROUP (the sim's L-46 reader, per gamora's hypothesis)
      The `.map` head carries, immediately after the 8-byte magic + 32 bytes of header ints:
          u32 len | "PatrolPoint_Attack"      <- the GROUP NAME
          u32 len | "Patrol Points"           <- the FIELD NAME
          u32     | count
          count x { 16-byte GUID | u32 len + dbr path | 16-byte GUID | 3 x f32 position }
      This is the AUTHORED ATTACK-POINT GROUP, named in the file.

  READING B -- PLACEMENT ARRAY (Lap S's reader)
      Further down the file, the general entity-placement array: 56-byte records of
          9 x f32 row-major rotation | 3 x f32 position | u32 | u32 string-table index
      filtered to rows whose string-table entry is `patrolpoint_01.dbr`.

GATE G4: both readings run on the IDENTICAL in-memory buffer; its sha256 is emitted.

THE TEST THAT MATTERS. Gamora compared the two lists BY INDEX. If the two structures hold the
SAME points in a DIFFERENT ORDER, an index-wise comparison produces exactly the reported
signature (large per-index residuals, small centroid residual) while the sets are in fact
identical. So this module compares BOTH ways: by index AND by optimal nearest-neighbour
matching, and reports both.

READ-ONLY.
"""
import hashlib
import json
import math
import pathlib
import re
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gd_arc_reader_2026_07_26 import ArcArchive

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-t-arrival-decode")
MAP_ARCS = ["survivalmode1/resources/Maps.arc",
            "survivalmode2/resources/Maps.arc",
            "survivalmode3/resources/Maps.arc"]
REC = 56
PATROL_DBR = "records/controllers/controlobjects/patrolpoint_01.dbr"


def read_head_group(b):
    """READING A. Returns (group_name, field_name, [ (dbr, (x,y,z)) ])."""
    if b[:4] != b"MAP\t":
        raise ValueError("not a MAP container")
    pos = 40  # 8-byte magic+version then 8 x u32 header ints (verified against the bytes)
    gname_len = struct.unpack_from("<I", b, pos)[0]
    pos += 4
    gname = b[pos:pos + gname_len].decode("latin-1")
    pos += gname_len
    fname_len = struct.unpack_from("<I", b, pos)[0]
    pos += 4
    fname = b[pos:pos + fname_len].decode("latin-1")
    pos += fname_len
    count = struct.unpack_from("<I", b, pos)[0]
    pos += 4
    out = []
    for _ in range(count):
        pos += 16                                    # GUID
        ln = struct.unpack_from("<I", b, pos)[0]
        pos += 4
        dbr = b[pos:pos + ln].decode("latin-1")
        pos += ln
        pos += 16                                    # second GUID
        x, y, z = struct.unpack_from("<fff", b, pos)
        pos += 12
        out.append((dbr, (x, y, z)))
    return gname, fname, out, count


def read_placements(b):
    """READING B. Lap S's algorithm, re-implemented here verbatim in behaviour."""
    # string table: contiguous run of u32-len-prefixed printable-ASCII .dbr paths
    strings, best = [], None
    for mo in re.finditer(rb"records/[ -~]{4,200}?\.dbr", b):
        s0 = mo.start() - 4
        if s0 < 0:
            continue
        ln = struct.unpack_from("<I", b, s0)[0]
        if ln != (mo.end() - mo.start()):
            continue
        if best is None:
            best = [s0]
        strings.append((s0, mo.end(), mo.group().decode("latin-1")))
    # locate the LAST contiguous run (the placement string table sits just before the array)
    runs, cur = [], []
    for i, (s0, e0, nm) in enumerate(strings):
        if cur and s0 != cur[-1][1]:
            runs.append(cur)
            cur = []
        cur.append((s0, e0, nm))
    if cur:
        runs.append(cur)
    run = max(runs, key=len)
    table = [nm for _, _, nm in run]
    arr_off = run[-1][1]
    declared = struct.unpack_from("<I", b, arr_off)[0]
    p = arr_off + 4
    out, n = [], 0
    while p + REC <= len(b) and n < declared:
        m9 = struct.unpack_from("<9f", b, p)
        ok = True
        for r in range(3):
            nrm = math.sqrt(sum(m9[r * 3 + c] ** 2 for c in range(3)))
            if not (0.98 <= nrm <= 1.02):
                ok = False
                break
        if ok:
            x, y, z = struct.unpack_from("<3f", b, p + 36)
            idx = struct.unpack_from("<I", b, p + 52)[0]
            if idx < len(table):
                out.append((table[idx], (x, y, z)))
                p += REC
                n += 1
                continue
        p += 4
    return out, declared, len(table)


def d3(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def d2(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])


def match_nearest(A, B):
    """Greedy optimal-ish matching: for each a, its nearest unused b."""
    used, pairs = set(), []
    for i, a in enumerate(A):
        best, bj = None, None
        for j, b in enumerate(B):
            if j in used:
                continue
            dd = d3(a, b)
            if best is None or dd < best:
                best, bj = dd, j
        if bj is not None:
            used.add(bj)
            pairs.append((i, bj, best))
    return pairs


def main():
    results = []
    for arc_rel in MAP_ARCS:
        arc = ArcArchive(VENDOR / arc_rel)
        for name in sorted(arc.names()):
            if not name.endswith(".map"):
                continue
            b = arc.read_file(name)
            buf_sha = hashlib.sha256(b).hexdigest()
            try:
                gname, fname, head, hcount = read_head_group(b)
            except Exception as e:
                results.append({"arc": arc_rel, "map": name, "error": f"headA: {e}"})
                continue
            try:
                pl, declared, tsize = read_placements(b)
            except Exception as e:
                results.append({"arc": arc_rel, "map": name, "error": f"placeB: {e}"})
                continue

            A = [p for dbr, p in head if dbr.lower().endswith("patrolpoint_01.dbr")]
            B = [p for dbr, p in pl if dbr.lower() == PATROL_DBR]

            rec = {"arc": arc_rel, "map": name, "buffer_sha256": buf_sha,
                   "head_group_name": gname, "head_field_name": fname,
                   "head_declared_count": hcount, "head_patrol_n": len(A),
                   "placement_declared": declared, "placement_parsed": len(pl),
                   "placement_patrol_n": len(B)}
            if A and B and len(A) == len(B):
                byidx = [d3(A[i], B[i]) for i in range(len(A))]
                byidx2 = [d2(A[i], B[i]) for i in range(len(A))]
                pairs = match_nearest(A, B)
                nn = sorted(p[2] for p in pairs)
                cA = tuple(sum(p[i] for p in A) / len(A) for i in range(3))
                cB = tuple(sum(p[i] for p in B) / len(B) for i in range(3))
                rec.update({
                    "BY_INDEX_3d": {"min": round(min(byidx), 4),
                                    "median": round(sorted(byidx)[len(byidx) // 2], 4),
                                    "max": round(max(byidx), 4)},
                    "BY_INDEX_ground": {"min": round(min(byidx2), 4),
                                        "median": round(sorted(byidx2)[len(byidx2) // 2], 4),
                                        "max": round(max(byidx2), 4)},
                    "BY_NEAREST_3d": {"min": round(min(nn), 6),
                                      "median": round(nn[len(nn) // 2], 6),
                                      "max": round(max(nn), 6)},
                    "centroid_gap_3d": round(d3(cA, cB), 4),
                    "is_same_point_set_1mm": max(nn) < 0.001,
                    "is_same_point_set_1cm": max(nn) < 0.01,
                    "permutation": [p[1] for p in sorted(pairs)],
                    "is_identity_permutation": [p[1] for p in sorted(pairs)] == list(range(len(A))),
                })
            results.append(rec)

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pm4t_map_arbitration.json", "w") as fh:
        json.dump(results, fh, indent=2)

    print(f"{'map':38s} {'A':>3s} {'B':>3s} {'idx_med':>8s} {'idx_max':>8s} "
          f"{'nn_max':>10s} {'same?':>6s} {'ident_perm':>10s}")
    same_all, ident_all = 0, 0
    for r in results:
        if "BY_INDEX_3d" not in r:
            print(f"{r['arc'].split('/')[0]}:{r['map']:28s} -- {r.get('error','count mismatch')} "
                  f"A={r.get('head_patrol_n')} B={r.get('placement_patrol_n')}")
            continue
        same_all += r["is_same_point_set_1cm"]
        ident_all += r["is_identity_permutation"]
        print(f"{r['arc'].split('/')[0]}:{r['map']:26s} {r['head_patrol_n']:3d} "
              f"{r['placement_patrol_n']:3d} {r['BY_INDEX_3d']['median']:8.3f} "
              f"{r['BY_INDEX_3d']['max']:8.3f} {r['BY_NEAREST_3d']['max']:10.6f} "
              f"{str(r['is_same_point_set_1cm']):>6s} {str(r['is_identity_permutation']):>10s}")
    n = sum(1 for r in results if "BY_INDEX_3d" in r)
    print(f"\nmaps compared: {n} | SAME POINT SET within 1 cm: {same_all} | "
          f"identity permutation: {ident_all}")
    print(f"group name (all): {sorted(set(r.get('head_group_name') for r in results))}")


if __name__ == "__main__":
    main()
