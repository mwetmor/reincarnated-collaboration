#!/usr/bin/env python3
"""
pm4t_map_v2_2026_08_14.py — RUN KC2-PM4 LAP T, INSTRUMENT I-T3b.

THE CORRECTED `.map` PLACEMENT READER, and the repair of defect `D-T-3`.

WHAT LAP S GOT WRONG (self-report, FIT law)
    `pm4s_map_2026_08_14.py` assumed a FIXED 56-byte placement record:
        [ 9 x f32 rotation | 3 x f32 position | u32 | u32 string-index ]
    The record is in fact VARIABLE-LENGTH:
        [ 9 x f32 rotation | 3 x f32 position | u32 has_guid
          | if has_guid: 16-byte GUID | u32 string-index ]
      -> has_guid == 0 : 56 bytes   (the case Lap S modelled)
      -> has_guid == 1 : 72 bytes   (the case Lap S did NOT model)
    The GUID-bearing records are exactly those an authored GROUP can reference by id -- which
    includes EVERY member of the head-section `PatrolPoint_Attack` group.

    Lap S's reader hit a 72-byte record, read the GUID's first 4 bytes as the string index, found
    it out of range, rejected the record, and advanced 4 bytes to resync. On
    `survivalmode3:survivalworld_c` that happened **509,756 times over 2,039,024 bytes** while
    collecting exactly `declared` (536) gate-passing windows spread over ~2 MB.

    CONSEQUENCE 1 -- the reader systematically DROPPED every grouped placement.
    CONSEQUENCE 2 -- Lap S's published quality gate, "parsed/declared ratio, 11 of 20 maps at
    100 %, worst 97.67 %", MEASURED NOTHING. The loop terminates when it has collected
    `declared` many accepted windows from anywhere downstream, so the ratio is ~100 % by
    construction whenever enough gate-passing windows exist. It was reported as evidence of a
    clean parse. It was not evidence of anything.

READ-ONLY.
"""
import csv
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
PATROL_DBR = "records/controllers/controlobjects/patrolpoint_01.dbr"


def string_table(b):
    strings, runs, cur = [], [], []
    for mo in re.finditer(rb"records/[ -~]{4,200}?\.dbr", b):
        s0 = mo.start() - 4
        if s0 < 0:
            continue
        if struct.unpack_from("<I", b, s0)[0] != (mo.end() - mo.start()):
            continue
        strings.append((s0, mo.end(), mo.group().decode("latin-1")))
    for s0, e0, nm in strings:
        if cur and s0 != cur[-1][1]:
            runs.append(cur)
            cur = []
        cur.append((s0, e0, nm))
    if cur:
        runs.append(cur)
    run = max(runs, key=len)
    return [nm for _, _, nm in run], run[-1][1]


def read_placements_v2(b):
    """Strict sequential parse. NO resync heuristic: any malformed record HALTS the parse
    and the shortfall is reported honestly instead of being back-filled."""
    table, arr_off = string_table(b)
    declared = struct.unpack_from("<I", b, arr_off)[0]
    # `arr_off + 4` carries one further u32 (observed 0) before the first record; the record
    # array therefore begins at `arr_off + 8`. Verified by orthonormality of the first
    # rotation matrix, which fails at +4 and passes at +8.
    p = arr_off + 8
    out, guid_rows, halted_at = [], 0, None
    for i in range(declared):
        if p + 52 > len(b):
            halted_at = ("EOF", i, p)
            break
        m9 = struct.unpack_from("<9f", b, p)
        norms = [math.sqrt(sum(m9[r * 3 + c] ** 2 for c in range(3))) for r in range(3)]
        if not all(0.98 <= n <= 1.02 for n in norms):
            halted_at = ("rotation not orthonormal", i, p)
            break
        pos = struct.unpack_from("<3f", b, p + 36)
        flag = struct.unpack_from("<I", b, p + 48)[0]
        if flag == 0:
            idx_off, size = p + 52, 56
            guid = None
        elif flag == 1:
            guid = b[p + 52:p + 68].hex()
            idx_off, size = p + 68, 72
            guid_rows += 1
        else:
            halted_at = (f"unknown flag {flag}", i, p)
            break
        if idx_off + 4 > len(b):
            halted_at = ("EOF at index", i, p)
            break
        idx = struct.unpack_from("<I", b, idx_off)[0]
        if idx >= len(table):
            halted_at = (f"string index {idx} out of range {len(table)}", i, p)
            break
        out.append({"dbr": table[idx], "x": pos[0], "y": pos[1], "z": pos[2],
                    "guid": guid, "offset": p, "size": size})
        p += size
    return out, declared, len(table), guid_rows, halted_at


def read_head_group(b):
    pos = 40
    gl = struct.unpack_from("<I", b, pos)[0]
    pos += 4
    gname = b[pos:pos + gl].decode("latin-1")
    pos += gl
    fl = struct.unpack_from("<I", b, pos)[0]
    pos += 4
    fname = b[pos:pos + fl].decode("latin-1")
    pos += fl
    count = struct.unpack_from("<I", b, pos)[0]
    pos += 4
    out = []
    for _ in range(count):
        guid = b[pos:pos + 16].hex()
        pos += 16
        ln = struct.unpack_from("<I", b, pos)[0]
        pos += 4
        dbr = b[pos:pos + ln].decode("latin-1")
        pos += ln
        pos += 16
        x, y, z = struct.unpack_from("<fff", b, pos)
        pos += 12
        out.append({"guid": guid, "dbr": dbr, "x": x, "y": y, "z": z})
    return gname, fname, out


def main():
    rows, per_map = [], []
    for arc_rel in MAP_ARCS:
        arc = ArcArchive(VENDOR / arc_rel)
        for name in sorted(n for n in arc.names() if n.endswith(".map")):
            b = arc.read_file(name)
            pl, declared, tsize, guid_rows, halt = read_placements_v2(b)
            gname, fname, head = read_head_group(b)
            # cross-check: are the head group's GUIDs present in the placement rows?
            pg = {r["guid"]: r for r in pl if r["guid"]}
            matched, resid = 0, []
            for h in head:
                r = pg.get(h["guid"])
                if r:
                    matched += 1
                    resid.append(math.dist((h["x"], h["y"], h["z"]),
                                           (r["x"], r["y"], r["z"])))
            per_map.append({
                "arc": arc_rel, "map": name, "sha256": hashlib.sha256(b).hexdigest(),
                "declared": declared, "parsed": len(pl),
                "complete": len(pl) == declared, "halt": halt,
                "guid_rows": guid_rows, "table": tsize,
                "head_group": gname, "head_count": len(head),
                "head_guids_matched_in_placements": matched,
                "guid_position_residual_max_m": (round(max(resid), 6) if resid else None),
                "patrol_rows_in_placements": sum(1 for r in pl
                                                 if r["dbr"].lower() == PATROL_DBR),
            })
            for r in pl:
                rows.append({"archive": arc_rel, "map": name, "dbr": r["dbr"],
                             "x": r["x"], "y": r["y"], "z": r["z"],
                             "guid": r["guid"] or "", "record_size": r["size"]})

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pm4t_map_placements_v2.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "pm4t_map_v2_summary.json", "w") as fh:
        json.dump(per_map, fh, indent=2)

    print(f"{'map':44s} {'decl':>5s} {'parsed':>6s} {'ok':>5s} {'guidrows':>8s} "
          f"{'patrol':>6s} {'headN':>5s} {'matched':>7s} {'resid':>8s}")
    for m in per_map:
        print(f"{m['arc'].split('/')[0]}:{m['map']:30s} {m['declared']:5d} {m['parsed']:6d} "
              f"{str(m['complete']):>5s} {m['guid_rows']:8d} {m['patrol_rows_in_placements']:6d} "
              f"{m['head_count']:5d} {m['head_guids_matched_in_placements']:7d} "
              f"{str(m['guid_position_residual_max_m']):>8s}")
    ok = sum(1 for m in per_map if m["complete"])
    print(f"\nmaps: {len(per_map)} | COMPLETE strict parses: {ok} | "
          f"total placements: {len(rows)}")
    for m in per_map:
        if not m["complete"]:
            print(f"   HALT {m['map']}: {m['halt']}")


if __name__ == "__main__":
    main()
