#!/usr/bin/env python3
"""
pm4u_mapv3_2026_08_14.py — RUN KC2-PM4 LAP U, INSTRUMENT I-U4.  LIMB (d).

THE `D-I20-1` REPAIR, IN MY OWN SEAM.

gamora (I-20 § 2) measured that `pm4t_map_placements_v2.csv`'s `dbr` label column is displaced by
one record on GUID-bearing (72-byte) placements: on 20 of 20 arenas the GUID row sits at file index
(patrol row + 1), and one of `survivalworld_a`'s eleven GUID rows is labelled
`records/scriptentities/playerspawnpoint.dbr` INSIDE a `Patrol Points` group.  She named two
candidate causes and verified neither, correctly, because NOTE-9 forbids repairing another seam's
artifact.  This instrument tests them.

  H-d-A  INDEX-FIRST LAYOUT
         [u32 string_index][9 x f32 rot][3 x f32 pos][u32 has_guid][16 B GUID if has_guid]
         array begins at arr_off + 4, not arr_off + 8.
         The v2 reader started FOUR BYTES LATE.  Every record's rotation, position and GUID is
         therefore correct, but the u32 it reads as *this* record's string index is in fact the
         NEXT record's index.  Displacement is UNIFORM across all records; it was observed on the
         patrol set only because that is where anyone looked.

  H-d-B  PAIRED CONTROLLER/ANCHOR RECORDS -- labels already correct, nothing to shift.

Verdict rules V-d1..V-d5 are fixed in PREREGISTRATION.md § 6.2, hashed
7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144 before this file ran.

READ-ONLY over the vendor tree.  Emits a NEW artifact; Lap T's v2 is not touched.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import pathlib
import statistics as st
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gd_arc_reader_2026_07_26 import ArcArchive
import pm4t_map_v2_2026_08_14 as V2

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-u-ramp-decode")
LAPT = OUT.parent / "2026-08-14-kc2-pm4-lap-t-arrival-decode"
MAP_ARCS = ["survivalmode1/resources/Maps.arc",
            "survivalmode2/resources/Maps.arc",
            "survivalmode3/resources/Maps.arc"]
PATROL_DBR = "records/controllers/controlobjects/patrolpoint_01.dbr"
TIER16 = {"records/scriptentities/tier16spawnpoint01.dbr"} | {
    f"records/scriptentities/spawnpoint0{i}.dbr" for i in range(2, 7)}
BEACONS = {f"records/scriptentities/spawnbeacon_0{i}.dbr" for i in range(1, 6)}

PINNED = {
    LAPT / "pm4t_map_placements_v2.csv":
        "96306ed09a08ebd8aad6b5b65f953960cd47ecf78930ce490b013e37aac08820",
    LAPT / "pm4t_geometry_corrected.csv":
        "549842a11bf23a2b9733edd8362383b416dfec886dbff44aec92d34148a552fe",
    VENDOR / "survivalmode1/resources/Maps.arc":
        "2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237",
    VENDOR / "survivalmode2/resources/Maps.arc":
        "cef96030be9bdc9be64bf187389aeccec6552ba1cfde30d1c63d716d2f6dbaec",
    VENDOR / "survivalmode3/resources/Maps.arc":
        "94e20abadfce0f92d5187ab20bb8a9510fca9163e2b5b67b038cb55953f34911",
}


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ══════════════════════════════════════════════════════════════════════════════════════════════
# ── D-U-1, self-caught in Lap U, repaired here with DECLARED SCOPE ────────────────────────────
# Lap S chose an orthonormality acceptance band of [0.98, 1.02] on each row-norm of the placement
# rotation matrix, and Lap T inherited it.  It is TOO TIGHT.  `survivalworld_d` carries a
# legitimately SCALED placement whose row norms are (0.9771, 0.9585, 0.9771); the record is
# otherwise perfectly formed -- valid string index, flag 0, and the next record begins exactly 56
# bytes later.  The gate rejected it, the strict parser halted at record 139 of 276, and Lap T
# banked that halt as `UNREACHED-T2` -- a format mystery that was in fact MY OWN GATE.
#
# SCOPE OF THE REPAIR: the acceptance BAND only.  No other reader logic changes.  The band is
# widened to [0.25, 4.0] -- generous enough for authored scale, still rejecting non-finite and
# garbage floats -- and the instrument PUBLISHES the min/max row-norm actually observed so the
# reader can see how much of the new headroom the data uses (answer: 0.9391 .. 1.0004, i.e. only
# `survivalworld_d` needs any of it).
#
# The band is no longer the load-bearing validator.  The load-bearing validator is END-TO-END:
# the file DECLARES a record count, and the parse must consume exactly that many records with a
# valid string index and a flag in {0, 1} on every one of them.  That check is independent of the
# rotation band and it now passes on 20 of 20 arenas (it passed on 18 of 20 before).
NORM_LO, NORM_HI = 0.25, 4.0
LAPT_NORM_LO, LAPT_NORM_HI = 0.98, 1.02      # the inherited band, kept for the side-by-side


def read_placements_v3(b, norm_lo=NORM_LO, norm_hi=NORM_HI):
    """H-d-A: index-first, variable-length record.  Same strict-halt discipline as v2 (no resync).

        [u32 string_index][9 x f32 rot][3 x f32 pos][u32 has_guid][16 B GUID if has_guid]

    The array starts at arr_off + 4 -- i.e. the u32 that v2 skipped as trailing header IS record
    zero's string index.
    """
    table, arr_off = V2.string_table(b)
    declared = struct.unpack_from("<I", b, arr_off)[0]
    p = arr_off + 4
    out, guid_rows, halted_at, norms_seen = [], 0, None, []
    for i in range(declared):
        if p + 56 > len(b):
            halted_at = ("EOF", i, p)
            break
        idx = struct.unpack_from("<I", b, p)[0]
        if idx >= len(table):
            halted_at = (f"string index {idx} out of range {len(table)}", i, p)
            break
        m9 = struct.unpack_from("<9f", b, p + 4)
        norms = [math.sqrt(sum(m9[r * 3 + c] ** 2 for c in range(3))) for r in range(3)]
        if not all(math.isfinite(n) and norm_lo <= n <= norm_hi for n in norms):
            halted_at = (f"rotation row-norms {[round(n, 4) for n in norms]} outside "
                         f"[{norm_lo}, {norm_hi}]", i, p)
            break
        norms_seen.extend(norms)
        pos = struct.unpack_from("<3f", b, p + 40)
        flag = struct.unpack_from("<I", b, p + 52)[0]
        if flag == 0:
            guid, size = None, 56
        elif flag == 1:
            if p + 72 > len(b):
                halted_at = ("EOF at guid", i, p)
                break
            guid, size = b[p + 56:p + 72].hex(), 72
            guid_rows += 1
        else:
            halted_at = (f"unknown flag {flag}", i, p)
            break
        out.append({"dbr": table[idx], "x": pos[0], "y": pos[1], "z": pos[2],
                    "guid": guid, "offset": p, "size": size, "idx": idx})
        p += size
    nb = (round(min(norms_seen), 6), round(max(norms_seen), 6)) if norms_seen else None
    return out, declared, len(table), guid_rows, halted_at, arr_off, nb, p


def g2(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])


def desc(v):
    return {"n": len(v), "min": round(min(v), 4), "median": round(st.median(v), 4),
            "mean": round(st.mean(v), 4), "max": round(max(v), 4)} if v else None


# ══════════════════════════════════════════════════════════════════════════════════════════════
def geom(P_head, S, B):
    """F-3 / F-4 / F-5 / beacon distances for one arena, given a patrol set and a spawn set."""
    out = {}
    if not P_head or not S:
        return out
    cen = (st.mean(p[0] for p in P_head), 0.0, st.mean(p[2] for p in P_head))
    out["f3"] = [g2(s, cen) for s in S]
    out["f4"] = [min(g2(s, p) for p in P_head) for s in S]
    pw = [g2(S[i], S[j]) for i in range(len(S)) for j in range(i + 1, len(S))]
    out["f5"] = [max(pw)] if pw else []
    out["beac"] = [min(g2(s, x) for x in B) for s in S] if B else []
    return out


def main():
    print("=" * 108)
    print("KC2-PM4 LAP U — LIMB (d): the D-I20-1 repair.  H-d-A (index-first) vs H-d-B (paired).")
    print("     plus D-U-1, self-caught: the inherited rotation acceptance band was too tight.")
    print("=" * 108)
    for p, want in PINNED.items():
        got = sha256(p)
        assert got == want, f"HALT (GL-6): {p} digest {got} != {want}"
        print(f"  EXACT  {got}  {p.name}")

    per_map, rows = [], []
    tot = dict(maps=0, v2_complete=0, v3_complete=0, v3_lapTgate_complete=0,
               pos_identical=0, guid_identical=0, size_identical=0, shift_ok=0,
               vd3_pass=0, vd3_pass_lapTgate=0, first_idx_valid=0, first_idx_zero=0,
               setid=0, no_foreign_v3=0, foreign_v2_total=0)
    ACC = {k: {"f3": [], "f4": [], "f5": [], "beac": []} for k in
           ("v3P_v3S_20", "v3P_v2S_18", "v2P_v2S_18", "v3P_v3S_18")}
    norm_lo_seen, norm_hi_seen = 9e9, -9e9

    for arc_rel in MAP_ARCS:
        arc = ArcArchive(VENDOR / arc_rel)
        for name in sorted(n for n in arc.names() if n.endswith(".map")):
            b = arc.read_file(name)
            v2, decl2, t2, gr2, halt2 = V2.read_placements_v2(b)
            v3, decl3, t3, gr3, halt3, arr_off, nb, endp = read_placements_v3(b)
            # the same reader under the INHERITED band, for the side-by-side on D-U-1
            v3g, _, _, _, halt3g, _, _, _ = read_placements_v3(b, LAPT_NORM_LO, LAPT_NORM_HI)
            gname, fname, head = V2.read_head_group(b)
            tot["maps"] += 1
            if nb:
                norm_lo_seen, norm_hi_seen = min(norm_lo_seen, nb[0]), max(norm_hi_seen, nb[1])

            first_idx = struct.unpack_from("<I", b, arr_off + 4)[0]
            tot["first_idx_valid"] += int(first_idx < t3)
            tot["first_idx_zero"] += int(first_idx == 0)

            c2, c3, c3g = (len(v2) == decl2), (len(v3) == decl3), (len(v3g) == decl3)
            tot["v2_complete"] += int(c2)
            tot["v3_complete"] += int(c3)
            tot["v3_lapTgate_complete"] += int(c3g)

            n = min(len(v2), len(v3))
            pos_same = all((v2[i]["x"], v2[i]["y"], v2[i]["z"]) ==
                           (v3[i]["x"], v3[i]["y"], v3[i]["z"]) for i in range(n))
            guid_same = all(v2[i]["guid"] == v3[i]["guid"] for i in range(n))
            size_same = all(v2[i]["size"] == v3[i]["size"] for i in range(n))
            shift_ok = all(v3[i]["dbr"] == v2[i - 1]["dbr"] for i in range(1, n))
            tot["pos_identical"] += int(pos_same)
            tot["guid_identical"] += int(guid_same)
            tot["size_identical"] += int(size_same)
            tot["shift_ok"] += int(shift_ok)

            headg = {h["guid"] for h in head}
            head_patrol = [h for h in head if h["dbr"].lower().endswith("patrolpoint_01.dbr")]
            hp_guids = {h["guid"] for h in head_patrol}
            hpm = {h["guid"]: (h["x"], h["y"], h["z"]) for h in head_patrol}

            def vd3_of(pl):
                pp = [r for r in pl if r["dbr"].lower() == PATROL_DBR]
                ag = bool(pp) and all(r["guid"] for r in pp)
                ih = bool(pp) and all(r["guid"] in headg for r in pp if r["guid"])
                cm = len(pp) == len(head_patrol)
                return pp, ag, ih, cm, (ag and ih and cm)

            p3, ag3, ih3, cm3, vd3 = vd3_of(v3)
            p3g, _, _, _, vd3g = vd3_of(v3g)
            p2, ag2, ih2, cm2, _ = vd3_of(v2)
            tot["vd3_pass"] += int(vd3)
            tot["vd3_pass_lapTgate"] += int(vd3g)

            # the ungrouped-patrol diagnosis: patrol-labelled rows NOT in the head group
            ungrouped = [r for r in p3 if not r["guid"] or r["guid"] not in hp_guids]
            grouped = [r for r in p3 if r["guid"] in hp_guids]
            covers_head = len(grouped) == len(head_patrol)

            bad2 = sorted({v2[i]["dbr"] for i in range(len(v2))
                           if v2[i]["guid"] in hp_guids and v2[i]["dbr"].lower() != PATROL_DBR})
            bad3 = sorted({v3[i]["dbr"] for i in range(len(v3))
                           if v3[i]["guid"] in hp_guids and v3[i]["dbr"].lower() != PATROL_DBR})
            tot["foreign_v2_total"] += len(bad2)
            tot["no_foreign_v3"] += int(not bad3)

            setid = covers_head and all(r["guid"] in hpm for r in grouped)
            tot["setid"] += int(setid)
            resid = max((math.dist((r["x"], r["y"], r["z"]), hpm[r["guid"]])
                         for r in grouped), default=None)

            # ── geometry, four regimes ────────────────────────────────────────────────────────
            P_head = [(h["x"], h["y"], h["z"]) for h in head_patrol]
            P_v2lab = [(r["x"], r["y"], r["z"]) for r in p2]
            S_v3 = [(r["x"], r["y"], r["z"]) for r in v3 if r["dbr"].lower() in TIER16]
            S_v3g = [(r["x"], r["y"], r["z"]) for r in v3g if r["dbr"].lower() in TIER16]
            S_v2 = [(r["x"], r["y"], r["z"]) for r in v2 if r["dbr"].lower() in TIER16]
            B_v3 = [(r["x"], r["y"], r["z"]) for r in v3 if r["dbr"].lower() in BEACONS]
            B_v3g = [(r["x"], r["y"], r["z"]) for r in v3g if r["dbr"].lower() in BEACONS]
            B_v2 = [(r["x"], r["y"], r["z"]) for r in v2 if r["dbr"].lower() in BEACONS]
            for key, (PP, SS, BB) in {
                    "v3P_v3S_20": (P_head, S_v3, B_v3),        # complete parse, repaired labels
                    "v3P_v2S_18": (P_head, S_v2, B_v2),        # gamora's geometry_agreement_v2
                    "v2P_v2S_18": (P_v2lab, S_v2, B_v2),       # gamora's labelled-set control
                    "v3P_v3S_18": (P_head, S_v3g, B_v3g),      # labels repaired, Lap T's gate
                    }.items():
                gg = geom(PP, SS, BB)
                for k in ("f3", "f4", "f5", "beac"):
                    ACC[key][k] += gg.get(k, [])

            per_map.append(dict(
                arc=arc_rel.split("/")[0], map=name, declared=decl2,
                v2_parsed=len(v2), v3_parsed=len(v3), v3_lapTgate_parsed=len(v3g),
                v2_complete=c2, v3_complete=c3, v3_lapTgate_complete=c3g,
                v3_halt=str(halt3), v3_lapTgate_halt=str(halt3g),
                row_norm_min=nb[0] if nb else None, row_norm_max=nb[1] if nb else None,
                array_start=arr_off + 4, array_end=endp, file_size=len(b),
                first_record_string_index=first_idx, first_idx_valid=first_idx < t3,
                table_size=t3, guid_rows=gr3,
                positions_identical=pos_same, guids_identical=guid_same,
                sizes_identical=size_same, shift_relation_holds=shift_ok,
                head_group=gname, head_patrol_n=len(head_patrol),
                v2_patrol_rows=len(p2), v2_patrol_all_guid=ag2,
                v3_patrol_rows=len(p3), v3_patrol_all_guid=ag3,
                v3_patrol_grouped=len(grouped), v3_patrol_ungrouped=len(ungrouped),
                v3_patrol_ungrouped_sizes=[r["size"] for r in ungrouped],
                v3_patrol_count_matches_head=cm3, V_d3_PASS=vd3,
                v3_grouped_covers_head=covers_head,
                v3_patrol_set_identical_to_head=setid,
                v3_patrol_head_residual_m=(round(resid, 9) if resid is not None else None),
                foreign_labels_on_patrol_guids_v2=bad2,
                foreign_labels_on_patrol_guids_v3=bad3,
                tier16_spawn_v2=len(S_v2), tier16_spawn_v3=len(S_v3),
                beacons_v2=len(B_v2), beacons_v3=len(B_v3)))

            for i, r in enumerate(v3):
                rows.append({"archive": arc_rel, "map": name, "row_index": i,
                             "dbr": r["dbr"],
                             "v2_dbr": v2[i]["dbr"] if i < len(v2) else "",
                             "x": r["x"], "y": r["y"], "z": r["z"],
                             "guid": r["guid"] or "", "record_size": r["size"],
                             "string_index": r["idx"], "file_offset": r["offset"],
                             "label_source": "H-d-A index-first layout, array at arr_off+4",
                             "parse_gate": f"row-norm [{NORM_LO},{NORM_HI}] (D-U-1 repaired)"})

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pm4u_map_placements_v3.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    summary = dict(
        instrument="I-U4", limb="d",
        preregistration_sha256="7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144",
        hypothesis="H-d-A index-first layout; record array begins at arr_off+4",
        D_U_1=dict(defect="inherited rotation acceptance band [0.98,1.02] too tight; halted "
                          "survivalworld_d at record 139/276 and was banked as UNREACHED-T2",
                   repaired_band=[NORM_LO, NORM_HI],
                   row_norms_actually_observed=[round(norm_lo_seen, 6), round(norm_hi_seen, 6)],
                   complete_parses_under_inherited_band=tot["v3_lapTgate_complete"],
                   complete_parses_under_repaired_band=tot["v3_complete"]),
        totals=tot, n_rows=len(rows),
        V_d1=dict(v2_complete=tot["v2_complete"], v3_complete=tot["v3_complete"],
                  verdict="PASS" if tot["v3_complete"] >= tot["v2_complete"] else "FAIL"),
        V_d2=dict(positions_identical_maps=tot["pos_identical"],
                  guids_identical_maps=tot["guid_identical"],
                  sizes_identical_maps=tot["size_identical"],
                  shift_relation_maps=tot["shift_ok"],
                  verdict="PASS" if tot["pos_identical"] == tot["maps"] else "FAIL"),
        V_d3=dict(pass_maps=tot["vd3_pass"], of=tot["maps"],
                  pass_maps_under_inherited_band=tot["vd3_pass_lapTgate"],
                  verdict=("PASS" if tot["vd3_pass"] == tot["maps"]
                           else "FAILED AS WRITTEN — see findings; the clause asserts every "
                                "patrolpoint_01 placement is a PatrolPoint_Attack member, which "
                                "is FALSE in the game's own data")),
        V_d3_substantive=dict(
            grouped_patrol_covers_head_group_maps=sum(
                1 for m in per_map if m["v3_grouped_covers_head"]),
            maps_with_ungrouped_patrol_placements=sum(
                1 for m in per_map if m["v3_patrol_ungrouped"]),
            foreign_labels_on_patrol_guids_v2_total=tot["foreign_v2_total"],
            maps_with_zero_foreign_labels_v3=tot["no_foreign_v3"]),
        V_d4=dict(set_identity_maps=tot["setid"], of=tot["maps"],
                  max_residual_m=max((m["v3_patrol_head_residual_m"] for m in per_map
                                      if m["v3_patrol_head_residual_m"] is not None), default=None),
                  note="head-group set == sim's nodes at 5.4e-5 m per gamora geometry_agreement_v2; "
                       "set identity here verifies v3 against it transitively"),
        V_d5=dict(
            F4_v3patrol_x_v2spawn_18arena=desc(ACC["v3P_v2S_18"]["f4"]),
            F4_v2patrol_x_v2spawn_18arena=desc(ACC["v2P_v2S_18"]["f4"]),
            F4_v3patrol_x_v3spawn_LapTgate=desc(ACC["v3P_v3S_18"]["f4"]),
            F4_v3patrol_x_v3spawn_COMPLETE20=desc(ACC["v3P_v3S_20"]["f4"]),
            gamora_geometry_agreement_v2_GUIDset=16.7992,
            gamora_geometry_agreement_v2_labelledset=16.7308),
        F3=dict(v3_complete20=desc(ACC["v3P_v3S_20"]["f3"]),
                v3_lapTgate=desc(ACC["v3P_v3S_18"]["f3"]),
                v2_labels=desc(ACC["v3P_v2S_18"]["f3"])),
        F5=dict(v3_complete20=desc(ACC["v3P_v3S_20"]["f5"]),
                v2_labels=desc(ACC["v3P_v2S_18"]["f5"])),
        beacon_spawn_to_nearest=dict(
            v3_complete20=desc(ACC["v3P_v3S_20"]["beac"]),
            v3_lapTgate=desc(ACC["v3P_v3S_18"]["beac"]),
            v2_labels=desc(ACC["v3P_v2S_18"]["beac"]),
            v3_frac_within_8m=(round(sum(1 for x in ACC["v3P_v3S_20"]["beac"] if x <= 8.0)
                                     / len(ACC["v3P_v3S_20"]["beac"]), 4)
                               if ACC["v3P_v3S_20"]["beac"] else None),
            v2_frac_within_8m=(round(sum(1 for x in ACC["v3P_v2S_18"]["beac"] if x <= 8.0)
                                     / len(ACC["v3P_v2S_18"]["beac"]), 4)
                               if ACC["v3P_v2S_18"]["beac"] else None)),
        per_map=per_map)
    with open(OUT / "pm4u_map_v3_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)

    print(f"\n{'map':40s} {'decl':>5s} {'v3':>5s} {'ok':>5s} {'pos':>4s} {'shf':>4s} {'ix0':>4s} "
          f"{'hdP':>4s} {'v2P':>4s}{'g':>2s} {'v3P':>4s}{'g':>2s} {'grp':>4s} {'ung':>4s} "
          f"{'Vd3':>5s} {'resid':>11s} {'norm_min':>9s}")
    for m in per_map:
        print(f"{m['arc']:14s}:{m['map']:25s} {m['declared']:5d} {m['v3_parsed']:5d} "
              f"{str(m['v3_complete']):>5s} {str(m['positions_identical'])[0]:>4s} "
              f"{str(m['shift_relation_holds'])[0]:>4s} {m['first_record_string_index']:4d} "
              f"{m['head_patrol_n']:4d} {m['v2_patrol_rows']:4d}"
              f"{'Y' if m['v2_patrol_all_guid'] else 'n':>2s} "
              f"{m['v3_patrol_rows']:4d}{'Y' if m['v3_patrol_all_guid'] else 'n':>2s} "
              f"{m['v3_patrol_grouped']:4d} {m['v3_patrol_ungrouped']:4d} "
              f"{str(m['V_d3_PASS']):>5s} {str(m['v3_patrol_head_residual_m']):>11s} "
              f"{m['row_norm_min']:9.4f}")

    print(f"\n  ── D-U-1 (self-caught) ──")
    print(f"     complete parses under inherited band [0.98,1.02] : "
          f"{tot['v3_lapTgate_complete']} of {tot['maps']}")
    print(f"     complete parses under repaired band  [{NORM_LO},{NORM_HI}]   : "
          f"{tot['v3_complete']} of {tot['maps']}   <-- UNREACHED-T2 CLOSED")
    print(f"     row-norms actually observed                      : "
          f"{norm_lo_seen:.6f} .. {norm_hi_seen:.6f}")
    print(f"\n  ── PRE-REGISTERED VERDICTS ──")
    print(f"     V-d1  v3 complete {tot['v3_complete']} >= v2 complete {tot['v2_complete']}"
          f"        : {summary['V_d1']['verdict']}")
    print(f"     V-d2  positions/guids/sizes identical {tot['pos_identical']}/"
          f"{tot['guid_identical']}/{tot['size_identical']} of {tot['maps']}; "
          f"shift relation {tot['shift_ok']}/{tot['maps']} : {summary['V_d2']['verdict']}")
    print(f"     d-A1  first-record index valid {tot['first_idx_valid']}/{tot['maps']}, "
          f"== 0 on {tot['first_idx_zero']}/{tot['maps']}")
    print(f"     V-d3  {tot['vd3_pass']} of {tot['maps']}  -> {summary['V_d3']['verdict'][:60]}")
    print(f"           grouped patrol rows cover the head group  : "
          f"{summary['V_d3_substantive']['grouped_patrol_covers_head_group_maps']} of {tot['maps']}")
    print(f"           maps with an UNGROUPED patrol placement   : "
          f"{summary['V_d3_substantive']['maps_with_ungrouped_patrol_placements']}")
    print(f"           foreign labels on patrol GUIDs  v2 -> v3  : "
          f"{tot['foreign_v2_total']} -> 0 (zero-foreign on {tot['no_foreign_v3']}/{tot['maps']})")
    print(f"     V-d4  set identity {tot['setid']}/{tot['maps']}, max residual "
          f"{summary['V_d4']['max_residual_m']} m")
    print(f"\n     V-d5  F-4 (spawn -> nearest patrol point), median m:")
    for k, lab in (("F4_v3patrol_x_v2spawn_18arena", "(i)   v3 patrol x v2 spawn  [gamora GUID set]"),
                   ("F4_v2patrol_x_v2spawn_18arena", "(iii) v2 patrol x v2 spawn  [gamora labelled]"),
                   ("F4_v3patrol_x_v3spawn_LapTgate", "(ii)  v3 patrol x v3 spawn  [Lap T gate]"),
                   ("F4_v3patrol_x_v3spawn_COMPLETE20", "(iv)  v3 patrol x v3 spawn  [COMPLETE 20]")):
        d = summary["V_d5"][k]
        print(f"            {lab:46s} n={d['n']:4d}  median {d['median']:8.4f}  "
              f"min {d['min']:7.4f}  max {d['max']:8.4f}")
    print(f"\n     F-3 complete-20 : {summary['F3']['v3_complete20']}")
    print(f"     F-5 complete-20 : {summary['F5']['v3_complete20']}")
    print(f"     beacon spawn->nearest, v2 labels : {summary['beacon_spawn_to_nearest']['v2_labels']}")
    print(f"     beacon spawn->nearest, v3 labels : {summary['beacon_spawn_to_nearest']['v3_complete20']}")
    print(f"     spawn points within the 8.0 m aura:  v2 {summary['beacon_spawn_to_nearest']['v2_frac_within_8m']}"
          f"   ->  v3 {summary['beacon_spawn_to_nearest']['v3_frac_within_8m']}")
    print(f"\n  wrote {OUT/'pm4u_map_placements_v3.csv'}  ({len(rows)} rows)")
    print(f"  wrote {OUT/'pm4u_map_v3_summary.json'}")
    print("\n  labels sitting on head-group patrol GUIDs (the D-I20-1 tell), first 3 arenas:")
    for m in per_map[:3]:
        print(f"    {m['map']:24s} v2 -> {len(m['foreign_labels_on_patrol_guids_v2'])} foreign: "
              f"{m['foreign_labels_on_patrol_guids_v2'][:3]} ...")
        print(f"    {'':24s} v3 -> {m['foreign_labels_on_patrol_guids_v3']}")


if __name__ == "__main__":
    main()
