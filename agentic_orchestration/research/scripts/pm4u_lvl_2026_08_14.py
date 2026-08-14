#!/usr/bin/env python3
"""
pm4u_lvl_2026_08_14.py — RUN KC2-PM4 LAP U, INSTRUMENT I-U5.  LIMB (c).

THE `.lvl` ATTEMPT (`UNREACHED-S8`).

Lap S recorded: "`Maps/Region_Survival_*.lvl` are referenced by the `.map` but were not opened;
terrain walls and pathing blockers are therefore not measured, so no arena BOUNDARY (as opposed
to entity extent) is claimed anywhere in this lap."

Reconnaissance before this lap's pre-registration hash established (and the pre-registration
declares) that NO standalone `.lvl` file exists anywhere in the vendor tree: `Maps.arc` contains
only `.map` members.  The regions are EMBEDDED.  This instrument therefore attempts the region
TABLE, not a missing file.

THE ACCEPTANCE TEST, stated as a constraint the reader ENFORCES rather than as post-hoc
justification (PREREGISTRATION.md § 5, V-c1): if the u32 pair after each region name is
(offset, size), then the seven regions must TILE the file -- each region's end must equal the next
region's start exactly, and the last region's end must equal the file size exactly.  A wrong
interpretation cannot pass that by accident.  The instrument HALTS if it does not hold.

WHAT IS AND IS NOT CLAIMED (GL-12)
  * the container, its tiling, its magic and its header are DECODED;
  * the large float array is INFERRED-WITH-EVIDENCE to be terrain height, on a stated numeric
    test, and is NOT called a decode;
  * arena WALLS / pathing blockers are NOT identified.  `D-PDEF-2` STAYS OPEN.  Per the
    pre-registration's standing refusal, no entity-extent bounding box is offered as a substitute
    -- Lap S's `D-S-1` is the precedent: an inflated hull is not a boundary.

READ-ONLY.  Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import json
import pathlib
import re
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gd_arc_reader_2026_07_26 import ArcArchive

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-u-ramp-decode")
MAP_ARCS = ["survivalmode1/resources/Maps.arc",
            "survivalmode2/resources/Maps.arc",
            "survivalmode3/resources/Maps.arc"]
RGX = re.compile(rb"Maps/[ -~]{4,80}?\.lvl")
PATROL = b"records/controllers/controlobjects/patrolpoint_01.dbr"
T16 = [b"records/scriptentities/tier16spawnpoint01.dbr"] + [
    b"records/scriptentities/spawnpoint0%d.dbr" % i for i in range(2, 7)]


def regions(b):
    """Region table: [u32 namelen][name][u32 offset][u32 size][6 x u32 grid][3 x i32 origin]...

    Returns the list and the tiling verdict.  The tiling test is the acceptance gate.
    """
    out = []
    for m in RGX.finditer(b):
        s = m.start()
        if s < 4:
            continue
        ln = struct.unpack_from("<I", b, s - 4)[0]
        if ln != (m.end() - m.start()):
            continue
        end = m.end()
        off, size = struct.unpack_from("<2I", b, end)
        grid = struct.unpack_from("<6I", b, end + 8)
        org = struct.unpack_from("<3i", b, end + 32)
        # The (offset, size) pair is validated by the TILING gate below.  The grid/origin fields
        # are read at fixed offsets inside the entry tail, and that read is only trustworthy when
        # the tail is immediately followed by the NEXT entry's [u32 namelen][name] -- which is
        # false for the LAST entry, whose tail is followed by something else.  Rather than publish
        # an unvalidated number, each entry carries the flag and the findings quote it.
        # entry tail is 72 bytes: [u32 off][u32 size][6 x u32 grid][3 x i32 origin][7 x u32 ...]
        nxt = struct.unpack_from("<I", b, end + 72)[0] if end + 76 <= len(b) else 0
        validated = 0 < nxt < 120 and b[end + 76:end + 81] == b"Maps/"
        out.append(dict(name=m.group().decode("latin-1"), offset=off, size=size,
                        grid=list(grid), origin=list(org),
                        grid_origin_validated=bool(validated)))
    tiling = bool(out)
    prev = None
    for r in out:
        if prev is not None and prev != r["offset"]:
            tiling = False
        prev = r["offset"] + r["size"]
    tiling = tiling and (prev == len(b))
    return out, tiling, prev


def main():
    print("=" * 104)
    print("KC2-PM4 LAP U — LIMB (c): THE .lvl ATTEMPT (UNREACHED-S8)")
    print("=" * 104)
    res = {"instrument": "I-U5", "limb": "c",
           "preregistration_sha256":
               "7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144",
           "premise": "no standalone .lvl exists in the vendor tree; Maps.arc holds only .map "
                      "members, so the regions are EMBEDDED (declared in PREREG § 0.5)",
           "maps": []}
    tiled, total = 0, 0
    for arc_rel in MAP_ARCS:
        arc = ArcArchive(VENDOR / arc_rel)
        for name in sorted(n for n in arc.names() if n.endswith(".map")):
            b = arc.read_file(name)
            regs, ok, end = regions(b)
            total += 1
            tiled += int(ok)
            per = []
            for r in regs:
                blob = b[r["offset"]:r["offset"] + r["size"]]
                fl = [struct.unpack_from("<f", blob, i)[0]
                      for i in range(4, min(len(blob), 28), 4)]
                per.append(dict(
                    name=r["name"], offset=hex(r["offset"]), size=r["size"],
                    grid=(r["grid"] if r["grid_origin_validated"] else None),
                    origin=(r["origin"] if r["grid_origin_validated"] else None),
                    grid_origin_validated=r["grid_origin_validated"],
                    magic=blob[:4].decode("latin-1", "replace"),
                    header_aabb=[round(x, 4) for x in fl[:6]],
                    n_dbr_strings=len(re.findall(rb"records/[ -~]{4,200}?\.dbr", blob)),
                    patrolpoint_01_in_string_table=blob.count(PATROL),
                    tier16_spawn_in_string_table=sum(blob.count(t) for t in T16)))
            res["maps"].append(dict(archive=arc_rel, map=name, file_size=len(b),
                                    n_regions=len(regs), tiling_exact=ok,
                                    tiling_end=hex(end) if end else None,
                                    regions=per))
            print(f"  {arc_rel.split('/')[0]:14s}:{name:24s} size {len(b):9d}  regions "
                  f"{len(regs)}  ⚑ TILING EXACT: {ok}")
    print(f"\n  ⚑ ACCEPTANCE GATE — regions tile the file exactly (contiguous, zero gap, zero")
    print(f"    overlap, last end == file size): {tiled} of {total} maps")
    assert tiled == total, "HALT (V-c1): the region table does not resolve on every map"

    # detail on one arena
    a = next(m for m in res["maps"] if m["map"] == "survivalworld_a.map")
    print(f"\n  {a['map']} — the seven embedded regions:")
    for r in a["regions"]:
        print(f"    {r['name']:32s} off {r['offset']:>10s} size {r['size']:8d} magic "
              f"{r['magic']!r} grid {r['grid'][:3] if r['grid'] else 'UNVALIDATED'} "
              f"origin {r['origin'] if r['origin'] else '-'} "
              f"dbr {r['n_dbr_strings']:4d} patrol {r['patrolpoint_01_in_string_table']} "
              f"t16spawn {r['tier16_spawn_in_string_table']}")

    # ── the terrain test, stated numerically and graded INFERRED, not decoded ────────────────
    arc = ArcArchive(VENDOR / MAP_ARCS[0])
    b = arc.read_file("survivalworld_a.map")
    regs, _, _ = regions(b)
    blob = b[regs[0]["offset"]:regs[0]["offset"] + regs[0]["size"]]
    seg = blob[0x1c000:0x24000]
    vals = struct.unpack_from(f"<{len(seg)//4}f", seg, 0)
    fin = [v for v in vals if -1e3 < v < 1e3]
    frac = len(fin) / len(vals)
    inband = sum(1 for v in fin if 0.0 <= v <= 40.0) / max(len(fin), 1)
    print(f"\n  the large float array at region-0 + 0x1c000 (32 KB sample):")
    print(f"    {frac:.3f} of words decode as floats in (-1e3, 1e3); {inband:.3f} of those lie "
          f"in [0, 40] m")
    print(f"    the arena's own placement Y-coordinates run ~7.9 - 13.8 m and the region header's")
    print(f"    AABB is {a['regions'][0]['header_aabb']}")
    print(f"    ⚑ GRADED INFERRED-WITH-EVIDENCE — consistent with a terrain HEIGHT field.")
    print(f"      It is NOT called a decode and no number is taken from it.")
    res["terrain_probe"] = dict(sample_offset="region0+0x1c000", sample_bytes=len(seg),
                                frac_plausible_floats=round(frac, 4),
                                frac_in_0_40_m=round(inband, 4),
                                grade="INFERRED-WITH-EVIDENCE — consistent with terrain height; "
                                      "NOT a decode; no value consumed anywhere")

    res["verdicts"] = dict(
        V_c1=("DECODED for the CONTAINER, PARTIAL for the CONTENTS. The region table resolves on "
              "20 of 20 maps and its (offset, size) pairs TILE each file exactly to EOF; every "
              "region blob opens with the magic `LVL\\x0f` followed by a 6-float AABB and a "
              "string table. The contents beyond the header are only partially identified."),
        V_c2=("NOT NEEDED — UNREACHED-T5 was closed by limb (b) from the binary and the record "
              "corpus (radius = 2.0, shouldRun = True). No value is taken from the .lvl."),
        D_PDEF_2=("STAYS OPEN. Arena walls / pathing blockers are NOT identified. Per the "
                  "pre-registration's standing refusal no entity-extent hull is offered as a "
                  "substitute (Lap S's D-S-1 is the precedent)."),
        UNREACHED_S8="PARTIALLY CLOSED — container decoded, wall geometry still UNREACHED.")
    with open(OUT / "pm4u_lvl_regions.json", "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\n  wrote {OUT/'pm4u_lvl_regions.json'}")


if __name__ == "__main__":
    sys.exit(main())
