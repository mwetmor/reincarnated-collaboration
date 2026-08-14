#!/usr/bin/env python3
"""KC2-PM4 Lap S — LIMB (a): Crucible ARENA GEOMETRY out of the shipped `.map` world assets.

FIRST-OF-KIND FOR THIS PROJECT.  Lap R recorded Crucible spawn geometry UNREACHED (`UNREACHED-1`)
because it lives in `.map` world assets outside the `.arz` record DB.  This module opens that
container and decodes the entity-placement array.

FORMAT, MAPPED FROM THE BYTES (nothing assumed from memory, no public spec consulted)
    container : `survivalmode{1,2,3}/resources/Maps.arc` -> `survivalworld_{a..j}.map`
    magic     : b'MAP\\t'  (read, then asserted)
    layout    : [ head section: inline `Patrol Points` group ] ... [ LVL region blocks ] ...
                [ STRING TABLE : contiguous run of u32-length-prefixed printable ASCII `.dbr`
                  paths ] [ u32 placement_count ] [ placement records ]
    placement : 9 x f32 row-major 3x3 ROTATION | 3 x f32 WORLD POSITION (x, y, z)
                | u32 | u32 string-table INDEX                       = 56 bytes
                Records are located by walking forward and accepting only positions where the
                nine leading floats form an ORTHONORMAL-ROW matrix (each row norm in [0.98, 1.02])
                AND the index is in range.  Unrecognised bytes advance by 4 and re-try, so the
                reader UNDER-reports rather than inventing placements; the parsed/declared count
                ratio is emitted per map so any shortfall is visible.

    y is the VERTICAL axis (validated per map: y-span << x-span and y-span << z-span).
    Ground distances are therefore computed in the (x, z) plane.

UNITS.  GD world units are metres, on the same scale Lap F used (`actorRadius = 0.32` on the
player; `eyeofreckoning1 :: skillTargetRadius = 3.0`).  This is the ONLY limb of Lap S that does
NOT pass through the px->m bracket -- it is already metric, so it carries no bracket at all.

READ-ONLY on the vendor tree.  OUTCOME-FIREWALLED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap S.
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

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive                       # noqa: E402

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-s-arena-advance")
MAP_ARCS = ["survivalmode1/resources/Maps.arc",
            "survivalmode2/resources/Maps.arc",
            "survivalmode3/resources/Maps.arc"]
REC = 56
INTEREST = re.compile(r"(spawnpoint|patrolpoint|spawnbeacon|spawnplayer|playerspawn|trappoint|"
                      r"defensepoint)", re.I)
#: the tier that owns waves 151-160 — `eventControl.lua` routes rewardTier 15 -> tier16Waves
TIER_OF_RECORD = "tier16spawnpoint01"


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def string_run(b: bytes, start: int):
    i, out = start, []
    n = len(b)
    while i < n - 4:
        ln = struct.unpack_from("<I", b, i)[0]
        if 4 <= ln <= 200 and i + 4 + ln <= n:
            s = b[i + 4:i + 4 + ln]
            if all(32 <= c < 127 for c in s):
                out.append(s.decode("ascii"))
                i += 4 + ln
                continue
        break
    return out, i


def find_table(b: bytes):
    """The longest contiguous length-prefixed-string run in the file is the string table."""
    best = ([], 0, 0)
    i, n = 0, len(b)
    while i < n - 4:
        ln = struct.unpack_from("<I", b, i)[0]
        if 4 <= ln <= 200 and i + 4 + ln <= n:
            s = b[i + 4:i + 4 + ln]
            if all(32 <= c < 127 for c in s):
                out, end = string_run(b, i)
                if len(out) > len(best[0]):
                    best = (out, i, end)
                i = end
                continue
        i += 1
    return best


def rot_ok(f) -> bool:
    for r in range(3):
        n = math.hypot(f[3 * r], f[3 * r + 1], f[3 * r + 2])
        if not (0.98 < n < 1.02):
            return False
    return True


def parse_map(b: bytes):
    assert b[:3] == b"MAP", f"BLOCKED-FORMAT: magic {b[:4]!r}"
    tbl, _, end = find_table(b)
    if not tbl:
        return None
    count = struct.unpack_from("<I", b, end)[0]
    p, recs = end + 4, []
    while len(recs) < count and p < len(b) - REC:
        f = struct.unpack_from("<9f", b, p)
        if rot_ok(f):
            x, y, z = struct.unpack_from("<3f", b, p + 36)
            idx = struct.unpack_from("<I", b, p + 52)[0]
            if idx < len(tbl) and all(math.isfinite(v) and abs(v) < 1e6 for v in (x, y, z)):
                recs.append((tbl[idx], x, y, z))
                p += REC
                continue
        p += 4
    return dict(table=tbl, declared=count, recs=recs)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 100)
    print("KC2-PM4 LAP S — LIMB (a): CRUCIBLE ARENA GEOMETRY FROM `.map` WORLD ASSETS")
    print("=" * 100)
    rows, summary = [], {}

    for rel in MAP_ARCS:
        pth = VENDOR / rel
        print(f"\n  {rel}\n    sha256 {sha256(pth)}")
        arc = ArcArchive(pth)
        for name in sorted(n for n in arc.names() if n.endswith(".map")):
            b = arc.read_file(name)
            r = parse_map(b)
            if r is None:
                print(f"    {name:24s} DECODE-FAILED")
                continue
            recs = r["recs"]
            xs = [x for _, x, _, _ in recs]
            ys = [y for _, _, y, _ in recs]
            zs = [z for _, _, _, z in recs]
            xsp, ysp, zsp = max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)
            v_axis = ysp < xsp and ysp < zsp
            key = f"{rel.split('/')[0]}:{name}"
            print(f"    {name:22s} placements {len(recs):3d}/{r['declared']:3d}  "
                  f"x-span {xsp:7.2f}  y-span {ysp:6.2f}  z-span {zsp:7.2f}  "
                  f"vertical-axis-is-y {v_axis}")

            named = {}
            for dbr, x, y, z in recs:
                if INTEREST.search(dbr):
                    rows.append(dict(archive=rel, map=name, dbr=dbr,
                                     x=round(x, 4), y=round(y, 4), z=round(z, 4)))
                    named.setdefault(pathlib.Path(dbr).stem, []).append((x, y, z))

            # ── the tier-16 spawn set: primary (tier-specific) + the shared 02..06 ──────────
            sp = []
            if TIER_OF_RECORD in named:
                sp.append((f"{TIER_OF_RECORD} (=spawnPoint01)", named[TIER_OF_RECORD][0]))
            for k in ("spawnpoint02", "spawnpoint03", "spawnpoint04", "spawnpoint05",
                      "spawnpoint06"):
                if k in named:
                    sp.append((k, named[k][0]))
            pp = named.get("patrolpoint_01", [])
            ply = named.get("spawnplayer", [None])[0]

            g = dict(n_placements=len(recs), declared=r["declared"],
                     x_span=round(xsp, 3), y_span=round(ysp, 3), z_span=round(zsp, 3),
                     vertical_axis_is_y=v_axis, n_tier16_spawnpoints=len(sp),
                     n_patrolpoints=len(pp))

            if pp:
                cx = sum(q[0] for q in pp) / len(pp)
                cz = sum(q[2] for q in pp) / len(pp)
                rad = [math.dist((q[0], q[2]), (cx, cz)) for q in pp]
                pair = [math.dist((pp[i][0], pp[i][2]), (pp[j][0], pp[j][2]))
                        for i in range(len(pp)) for j in range(i + 1, len(pp))]
                g |= dict(patrol_centroid_xz=[round(cx, 3), round(cz, 3)],
                          patrol_radius_min_m=round(min(rad), 3),
                          patrol_radius_max_m=round(max(rad), 3),
                          patrol_pairwise_max_m=round(max(pair), 3) if pair else None)
            if sp:
                d_ply = [round(math.dist((q[0], q[2]), (ply[0], ply[2])), 3)
                         for _, q in sp] if ply else None
                if pp:
                    d_cen = [round(math.dist((q[0], q[2]), (cx, cz)), 3) for _, q in sp]
                    g |= dict(spawn_to_patrol_centroid_m=d_cen,
                              spawn_to_patrol_centroid_min_m=min(d_cen),
                              spawn_to_patrol_centroid_max_m=max(d_cen))
                    # nearest patrol point to each spawn point — the shortest march
                    d_near = [round(min(math.dist((q[0], q[2]), (t[0], t[2])) for t in pp), 3)
                              for _, q in sp]
                    g |= dict(spawn_to_nearest_patrol_m=d_near,
                              spawn_to_nearest_patrol_min_m=min(d_near),
                              spawn_to_nearest_patrol_max_m=max(d_near))
                pairs = [math.dist((sp[i][1][0], sp[i][1][2]), (sp[j][1][0], sp[j][1][2]))
                         for i in range(len(sp)) for j in range(i + 1, len(sp))]
                g |= dict(spawn_pairwise_max_m=round(max(pairs), 3) if pairs else None,
                          spawn_to_playerspawn_m=d_ply)
            summary[key] = g
            if sp and pp:
                print(f"       tier16 spawn points {len(sp)}  patrol points {len(pp)}  "
                      f"patrol ring radius {g['patrol_radius_min_m']}-{g['patrol_radius_max_m']} m")
                print(f"       spawn -> patrol CENTROID : {g['spawn_to_patrol_centroid_m']}")
                print(f"       spawn -> NEAREST patrol  : {g['spawn_to_nearest_patrol_m']}")
                print(f"       spawn pairwise max       : {g['spawn_pairwise_max_m']} m")

    with open(OUT / "pm4s_arena_placements.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["archive", "map", "dbr", "x", "y", "z"])
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "pm4s_arena_geometry.json", "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)

    # ── the cross-map headline ───────────────────────────────────────────────────────────────
    cen = [v["spawn_to_patrol_centroid_max_m"] for v in summary.values()
           if v.get("spawn_to_patrol_centroid_max_m")]
    near = [v["spawn_to_nearest_patrol_m"] for v in summary.values()
            if v.get("spawn_to_nearest_patrol_m")]
    flat = [d for lst in near for d in lst]
    if cen:
        print("\n  ── CROSS-MAP (every Crucible arena that carries a tier-16 spawn set) ──")
        print(f"    spawn -> patrol-centroid, MAX over all arenas : {max(cen):.3f} m")
        print(f"    spawn -> NEAREST patrol point : min {min(flat):.3f}  "
              f"median {sorted(flat)[len(flat)//2]:.3f}  max {max(flat):.3f} m  (n={len(flat)})")
    print(f"\n  wrote {OUT/'pm4s_arena_placements.csv'}  ({len(rows)} rows)")
    print(f"  wrote {OUT/'pm4s_arena_geometry.json'}")


if __name__ == "__main__":
    sys.exit(main())
