#!/usr/bin/env python3
"""C-9 T10-2 step 1 (spec v2) -- FINALIZE: measure the blockout against the spec, merge, map, stage.

    python3 tools/finalize.py [--stage]

Reads captures/ (what the Godot scene BUILT and what the capture tool MEASURED) and writes:
    ../barrow_full_layout.json   the deliverable: design numbers + built transforms + acceptance + crucible
    captures/acceptance.json     every acceptance line with its number and its instrument
    captures/barrow_full_map.png the labelled top-down map (5 m grid, the 4 x 4 paint-chunk grid)
    captures/guide_preview*.png  the guide, downscaled (plain, and with the chunk grid)
    paint/barrow_full_guide.png + paint/cfg_barrow_full.json   staged for guided_paint.py, NOT fired
--stage also copies the review set into the Desktop review folder.

EVERY PLACEMENT NUMBER IS RE-DERIVED FROM THE BUILT SCENE THROUGH THE ANALYTIC FRAME (cos 47 /
sin 47), independently of the live camera basis the scene built in.
"""
import hashlib
import heapq
import json
import math
import pathlib
import re
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import geom2d as G  # noqa: E402

ROOT = HERE.parent
CAP = ROOT / "captures"
PAINT = ROOT / "paint"
STAGE = pathlib.Path.home() / "Desktop" / "Astra Burst Review - 2026-09-26" / "C-9 barrow full"
B = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst")

PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
PX_UP = PPM * math.sin(PITCH)
CY, SY = math.cos(math.radians(47.0)), math.sin(math.radians(47.0))
TOL_M = 0.05


def xz_to_uv(x, z):
    return (x * CY - z * SY, -x * SY - z * CY)


def r(x, n=4):
    return None if x is None else round(float(x), n)


def _np(o):
    """numpy scalars (a comparison of numpy floats is a numpy bool) as plain JSON values"""
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError(type(o).__name__)


def load():
    L = json.loads((ROOT / "barrow_full_layout.json").read_text())
    built = json.loads((CAP / "built.json").read_text())
    rep = json.loads((CAP / "capture_report.json").read_text())
    grid = json.loads((CAP / "walk_grid.json").read_text())
    return L, built, rep, grid


def built_uv(rec):
    o = rec["world_origin"]
    return xz_to_uv(o[0], o[2])


class Grid:
    """The physics flood grid: 'o' reachable, '.' free but not reachable, '#' blocked."""

    def __init__(self, g):
        self.u0, self.v0, self.st, self.nu, self.nv = g["u0"], g["v0"], g["step"], g["nu"], g["nv"]
        self.rows = g["rows_from_v0_up"]
        self.reach = np.array([[c == "o" for c in row] for row in self.rows], dtype=bool)

    def ij(self, u, v):
        return int(round((u - self.u0) / self.st)), int(round((v - self.v0) / self.st))

    def uv(self, i, j):
        return self.u0 + i * self.st, self.v0 + j * self.st

    def reachable(self, u, v):
        i, j = self.ij(u, v)
        return 0 <= i < self.nu and 0 <= j < self.nv and bool(self.reach[j, i])

    def near_reachable(self, u, v, rad):
        i, j = self.ij(u, v)
        k = int(math.ceil(rad / self.st))
        i0, i1 = max(0, i - k), min(self.nu, i + k + 1)
        j0, j1 = max(0, j - k), min(self.nv, j + k + 1)
        if i0 >= i1 or j0 >= j1:
            return False
        sub = self.reach[j0:j1, i0:i1]
        if not sub.any():
            return False
        jj, ii = np.nonzero(sub)
        du = (ii + i0 - i) * self.st
        dv = (jj + j0 - j) * self.st
        return bool((du * du + dv * dv <= rad * rad).any())

    def geodesic_from(self, u, v):
        """Walkable path lengths from (u, v) to every reachable cell: Dijkstra on a 16-connected
        stencil (the eight neighbours plus the eight knight moves, each move allowed only if every
        cell it crosses is reachable), costs = true step lengths. A straight walk's error on this
        stencil is under 2.7%; a 4- or 8-connected grid would overstate by up to 8-41%."""
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1),
                 (1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
        via = {}
        for di, dj in moves:
            si = (di > 0) - (di < 0)
            sj = (dj > 0) - (dj < 0)
            if abs(di) == 1 and abs(dj) == 2:
                via[(di, dj)] = [(0, sj), (di, sj)]          # the two cells the segment crosses
            elif abs(di) == 2 and abs(dj) == 1:
                via[(di, dj)] = [(si, 0), (si, dj)]
            elif di and dj:
                via[(di, dj)] = [(di, 0), (0, dj)]           # a diagonal may not cut a corner
            else:
                via[(di, dj)] = []
        dist = np.full((self.nv, self.nu), np.inf)
        si, sj = self.ij(u, v)
        dist[sj, si] = 0.0
        pq = [(0.0, si, sj)]
        R = self.reach
        while pq:
            d, i, j = heapq.heappop(pq)
            if d > dist[j, i]:
                continue
            for di, dj in moves:
                ni, nj = i + di, j + dj
                if not (0 <= ni < self.nu and 0 <= nj < self.nv) or not R[nj, ni]:
                    continue
                ok = True
                for ci, cj in via[(di, dj)]:
                    xi, xj = i + ci, j + cj
                    if not (0 <= xi < self.nu and 0 <= xj < self.nv) or not R[xj, xi]:
                        ok = False
                        break
                if not ok:
                    continue
                nd = d + self.st * math.hypot(di, dj)
                if nd < dist[nj, ni]:
                    dist[nj, ni] = nd
                    heapq.heappush(pq, (nd, ni, nj))
        return dist


# --- the marker instrument ---------------------------------------------------------------------
def measure_markers(rep):
    """A marker's length in pixels by COVERAGE, in LINEAR light, on the guide's own camera; the
    2 m marker must read double the 1 m one, both ways, before any number is believed."""
    srgb = np.asarray(Image.open(CAP / "guide_calibration.png").convert("RGB")).astype(np.float64) / 255.0
    img = np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)
    out = {}
    for k, m in rep["guide"]["markers"].items():
        (x0, y0), (x1, y1) = m["projected_px"]
        col = np.array(m["rgb"], dtype=np.float64)
        col = np.where(col <= 0.04045, col / 12.92, ((col + 0.055) / 1.055) ** 2.4)
        horizontal = abs(x1 - x0) > abs(y1 - y0)
        lengths = []
        for dd in (-2, -1, 0, 1, 2):
            if horizontal:
                yc = int(round((y0 + y1) / 2.0 - 0.5))
                lo, hi = int(math.floor(min(x0, x1))) - 10, int(math.ceil(max(x0, x1))) + 10
                line = img[yc + dd, lo:hi]
            else:
                xc = int(round((x0 + x1) / 2.0 - 0.5))
                lo, hi = int(math.floor(min(y0, y1))) - 10, int(math.ceil(max(y0, y1))) + 10
                line = img[lo:hi, xc + dd]
            bg = np.median(np.concatenate([line[:6], line[-6:]]), axis=0)
            d = col - bg
            cov = np.clip(((line - bg) @ d) / float(d @ d), 0.0, 1.0)
            lengths.append(float(cov.sum()))
        out[k] = {"length_m": m["length_m"], "axis": "u (across)" if horizontal else "v (up-screen)",
                  "measured_px": round(float(np.median(lengths)), 3), "rows_or_cols": [round(x, 3) for x in lengths],
                  "projected_px": m["projected_length_px"],
                  "expected_px": round(m["length_m"] * (PPM if horizontal else PX_UP), 3)}
    for k, v in out.items():
        if v["measured_px"] < 0.5 * v["expected_px"]:
            raise SystemExit("INSTRUMENT FAILURE: marker %s reads %.2f px against %.2f expected" % (k, v["measured_px"], v["expected_px"]))
    ru = out["u_2m"]["measured_px"] / out["u_1m"]["measured_px"]
    rv = out["v_2m"]["measured_px"] / out["v_1m"]["measured_px"]
    return {"markers": out,
            "instrument_proof": {"u_2m_over_u_1m": round(ru, 4), "v_2m_over_v_1m": round(rv, 4), "_expect": 2.0,
                                 "PASS": abs(ru - 2.0) < 0.01 and abs(rv - 2.0) < 0.01},
            "one_metre_across_px": out["u_1m"]["measured_px"],
            "_instrument": "coverage-summed pixel length along the bar's centre line in guide_calibration.png (5376x3328, same camera as guide.png), in LINEAR light; median of 5 lines",
            "_precision": "MSAA 4x quantises each end's coverage in quarter steps: about +-0.3 px per bar"}


# --- acceptance ----------------------------------------------------------------------------------
def footprints(built):
    fp = {}
    for pid, rec in built["records"].items():
        fp[pid] = {"low": G.open_poly(rec.get("footprint_uv_low", [])), "all": G.open_poly(rec.get("footprint_uv_all", []))}
    return fp


def acceptance(L, built, rep, grid, marks):
    P = {e["id"]: e for e in L["placements"]}
    R = built["records"]
    fp = footprints(built)
    A = {}
    # 1. placements vs the table
    rows = []
    for e in L["placements"]:
        pid = e["id"]
        rec = R.get(pid)
        if rec is None:
            rows.append({"id": pid, "status": "NOT BUILT"})
            continue
        if e["kind"] == "primitive":
            bc = rec["base_centroid_world"]
            got = xz_to_uv(bc[0], bc[2])
            what = "base slab centroid"
        elif pid == "mound":
            got = G.centroid_area(fp[pid]["all"])[0]
            what = "centroid of the built mound's footprint hull"
        else:
            got = built_uv(rec)
            what = "root origin (footprint centre; the SOCKET for the fallen stone; the trunk base for a birch)"
        row = {"id": pid, "class": e["class"], "built_uv": [r(got[0]), r(got[1])], "measured_as": what}
        if e.get("spec_uv") is not None:
            d = math.dist(got, e["spec_uv"])
            row.update({"spec_uv": e["spec_uv"], "delta_m": r(d), "PASS": d <= TOL_M})
        elif e.get("uv") is not None:
            row.update({"derived_uv": e["uv"], "delta_from_derived_m": r(math.dist(got, e["uv"])),
                        "derived_from": e.get("derived_from", "")})
        rows.append(row)
    groves = {}
    for e in L["placements"]:
        if e["class"] == "birch" and e.get("grove") and e["id"] in R:
            groves.setdefault(e["grove"], {"spec": e["grove_spec_uv"], "pts": []})["pts"].append(built_uv(R[e["id"]]))
    for g, d in sorted(groves.items()):
        c = (sum(p[0] for p in d["pts"]) / len(d["pts"]), sum(p[1] for p in d["pts"]) / len(d["pts"]))
        dd = math.dist(c, d["spec"])
        rows.append({"id": "grove_" + g, "class": "grove", "members": len(d["pts"]), "built_uv": [r(c[0]), r(c[1])],
                     "spec_uv": d["spec"], "delta_m": r(dd), "PASS": dd <= TOL_M, "measured_as": "centroid of the built trunk bases"})
    la, lb = R.get("fallen_tree_log_A"), R.get("fallen_tree_log_B")
    if la and lb:
        ca, cb = built_uv(la), built_uv(lb)
        Cm = ((ca[0] + cb[0]) / 2, (ca[1] + cb[1]) / 2)
        dd = math.dist(Cm, P["fallen_tree_log_A"]["pair_spec_uv"])
        rows.append({"id": "fallen_tree", "class": "fallen tree (2 logs)", "built_uv": [r(Cm[0]), r(Cm[1])],
                     "spec_uv": P["fallen_tree_log_A"]["pair_spec_uv"], "delta_m": r(dd), "PASS": dd <= TOL_M,
                     "measured_as": "midpoint of the two logs' built centres"})
    rv = R.get("raven")
    if rv:
        o = built_uv(rv)
        on = G.dist_poly_pt(fp["ring_p55"]["all"], o) == 0.0
        rows.append({"id": "raven_on_+55", "class": "raven", "built_uv": [r(o[0]), r(o[1])], "over_the_stone": on,
                     "PASS": on, "perch_y": rv["y_min"], "stone_top_y": R["ring_p55"]["y_max"]})
    A["placements"] = {"tolerance_m": TOL_M, "rows": rows,
                       "all_spec_points_within_tolerance": all(x.get("PASS", True) for x in rows),
                       "worst_delta_m": r(max([x.get("delta_m") or 0.0 for x in rows])),
                       "basis_residuals": rep["scene"]["camera"]["ground_basis"],
                       "_instrument": "built world transforms read back into (u, v) through the ANALYTIC frame"}
    # 2. arena, path, ring entrance
    ac = tuple(L["regions"]["arena"]["centre_uv"])
    near = []
    for pid, f in fp.items():
        if P.get(pid, {}).get("margin"):
            continue
        dl = G.dist_poly_pt(f["low"], ac) if len(f["low"]) >= 3 else None
        da = G.dist_poly_pt(f["all"], ac) if len(f["all"]) >= 3 else None
        near.append((pid, dl, da))
    ls = sorted([x for x in near if x[1] is not None], key=lambda x: x[1])
    al = sorted([x for x in near if x[2] is not None], key=lambda x: x[2])
    A["arena"] = {"centre_uv": list(ac), "required_r": L["regions"]["arena"]["r"],
                  "clear_r_walkable_m": r(ls[0][1]), "nearest_walkable": [[x[0], r(x[1])] for x in ls[:6]],
                  "clear_r_any_height_m": r(al[0][2]), "nearest_any_height": [[x[0], r(x[2])] for x in al[:6]],
                  "PASS": ls[0][1] >= L["regions"]["arena"]["r"],
                  "_instrument": "least distance from (0, 1) to each built footprint (convex hull of the mesh's vertices under 1.9 m; and of all of them)"}
    path = [tuple(p) for p in L["regions"]["path"]["extended_off_frame_uv"]]
    half = L["regions"]["path"]["width_m"] / 2.0
    intr = []
    for pid, f in fp.items():
        if len(f["low"]) < 3:
            continue
        d = G.dist_poly_poly(f["low"], path, q_closed=False)
        if d is not None and d < half + 1.0:
            intr.append((pid, d))
    intr.sort(key=lambda x: x[1])
    A["path"] = {"width_m": L["regions"]["path"]["width_m"], "closest": [[x[0], r(x[1]), r(x[1] - half)] for x in intr[:8]],
                 "_columns": "[piece, distance to the centreline m, clearance beyond the 2 m half-width m]",
                 "min_clearance_m": r(intr[0][1] - half) if intr else None, "PASS": (not intr) or intr[0][1] >= half,
                 "_instrument": "least distance from each built footprint (under 1.9 m) to the path's centreline (to the window's bottom edge)"}
    gap = G.dist_poly_poly(fp["ring_p155"]["low"], fp["ring_m155"]["low"])
    A["ring_entrance"] = {"between": ["ring_p155", "ring_m155"], "clear_gap_m": r(gap), "required_m": 6.0,
                          "PASS": gap is not None and gap >= 6.0,
                          "_instrument": "least distance between the two gate stones' built footprints (under 1.9 m)"}
    # 3. walkability
    wg = rep["walk_grid"]["summary"]
    A["flood_fill"] = {"from_uv": grid["spawn_uv"], "cell_m": wg["cell_m"], "reachable_m2": wg["reachable_m2"],
                       "targets": wg["targets"], "ice_reachable_share": wg["ice_reachable_share"],
                       "reachable_outside_bounds_cells": wg["reachable_outside_bounds"],
                       "PASS": all(wg["targets"].values()) and wg["reachable_outside_bounds"] == 0,
                       "_instrument": rep["walk_grid"]["instrument"]}
    df = rep["door_floor"]["floor_y_by_v_at_u0"]
    walks = rep.get("walks", {})
    A["mound_and_door_floor"] = {"reachable_cells_inside_the_mound_outside_the_cutting": wg["reachable_inside_mound_outside_cutting"],
                                 "mound_walk_refused": walks.get("refused_up_the_mound", {}).get("PASS"),
                                 "passage_walk_refused": walks.get("refused_into_the_passage", {}).get("PASS"),
                                 "floor_y_in_the_cutting_to_the_door": df,
                                 "PASS": wg["reachable_inside_mound_outside_cutting"] == 0 and all(v is not None and abs(v) < 0.005 for v in df.values()),
                                 "_instrument": "flood-fill cells inside the mound ellipse outside the cutting; scripted walks at the mound and into the passage; " + rep["door_floor"]["instrument"]}
    if walks:
        A["walks"] = {k: {kk: v[kk] for kk in ("from_uv", "to_uv", "reached", "expected_to_reach", "PASS", "end_uv", "end_floor_y", "seconds")}
                      for k, v in walks.items() if isinstance(v, dict)}
        A["walks"]["_instrument"] = walks["_instrument"]
    A["scale"] = marks
    A["scale"]["PASS"] = marks["instrument_proof"]["PASS"] and abs(marks["one_metre_across_px"] - PPM) < 0.5
    A["guide_frame"] = {"px": rep["guide"]["px"], "corners_projected_px": rep["guide"]["window_corners_projected_px"],
                        "_expect": rep["guide"]["_corners_expect"]}
    # 4. (v2) no squeezes, on the built colliders
    gr = Grid(grid)
    def object_of(g):
        return "fallen_tree" if g.startswith("fallen_tree_log_") else ("door" if g.startswith("door_") else g)
    obs = [(object_of(c["group"]), G.open_poly(c["poly"])) for c in built["collider_footprints"] if len(c["poly"]) >= 3]
    sq = G.squeezes(obs, lambda u, v, w: gr.near_reachable(u, v, G.stand_radius(w, 0.06)))
    A["no_squeezes"] = {"rule": "every gap between two obstacles in the walkable area is < 0.70 m or >= 1.40 m",
                        "obstacles": len(obs), "squeezes": sq, "PASS": not sq,
                        "_instrument": "the gap PROFILED between every pair of BUILT colliders' ground footprints (each shape cut to y 0.05-1.9 and projected): every 0.1 m round each outline, the width to the other; a width in [0.70, 1.40) counts where his capsule can stand in the gap there -- a reachable 0.1 m cell within (w/2 - 0.35 + 0.06) m of the gap's midpoint",
                        "_resolution": "the grid is 0.1 m: a gap narrower than ~0.72 m, which his capsule can only just pass, may fall between cells"}
    # 5. (v2) camera margin
    fr = L["frame"]
    cam = fr["camera"]["frame_reach_from_his_feet_m"]
    win = fr["guide_window"]
    jj, ii = np.nonzero(gr.reach)
    us = gr.u0 + ii * gr.st
    vs = gr.v0 + jj * gr.st
    over = {"left_px": float(np.max((win["u"][0] + cam["across"] - us) * PPM)),
            "right_px": float(np.max((us + cam["across"] - win["u"][1]) * PPM)),
            "bottom_px": float(np.max((win["v"][0] + cam["down_screen"] - vs) * PX_UP)),
            "top_px": float(np.max((vs + cam["up_screen"] - win["v"][1]) * PX_UP))}
    bad = int(np.sum((us - cam["across"] < win["u"][0]) | (us + cam["across"] > win["u"][1])
                     | (vs - cam["down_screen"] < win["v"][0]) | (vs + cam["up_screen"] > win["v"][1])))
    A["camera_margin"] = {"reachable_cells": int(len(us)), "cells_whose_frame_leaves_the_window": bad,
                          "worst_px_outside_by_side": {k: r(v, 1) for k, v in over.items()},
                          "_read": "negative = that many px of margin to spare on that side",
                          "frame_from_his_feet": cam, "PASS": bad == 0,
                          "_instrument": "every reachable cell of the physics flood grid (0.1 m), the 1920 x 1080 play frame centred on him with the 55 px lift, against the 5376 x 3328 window",
                          "_resolution": "the grid is 0.1 m: a position between cell centres can sit up to 0.05 m (5 px across, 4 px up-screen) beyond its cell"}
    # 6. (v2) the door
    m = P["mound"]
    lint_top = R["door_lintel"]["y_max"]
    a_, b_ = m["semi_axes"]
    cu, pa = m["cutting"], m["passage"]

    def dome(u, v):
        rr = (u / a_) ** 2 + ((v - m["uv"][1]) / b_) ** 2
        if rr >= 1:
            return 0.0
        t = min(max((1 - math.sqrt(rr)) / m.get("toe_rho", 1e-4), 0.0), 1.0)
        return m["rise_m"] * (1 - rr) ** m["exponent"] * t * t * (3 - 2 * t)
    lint_u = max(abs(p[0]) for p in fp["door_lintel"]["all"])
    cov = min(dome(u, v) for u in np.linspace(-lint_u, lint_u, 25) for v in np.linspace(cu["v_facade"], pa["v_end"], 21)) - lint_top
    dv = rep["door_visibility"]
    A["door"] = {"cover": {"lintel_top_y_built": lint_top, "lintel_half_width_built_m": r(lint_u),
                           "mound_min_over_the_passage_roof_m": r(cov + lint_top), "cover_m": r(cov), "required_m": 0.3,
                           "PASS": bool(cov >= 0.3),
                           "_instrument": "the built mound's own height function over u +-(the lintel's built half-width), v from the facade to the passage's end, minus the lintel's built top"},
                 "visible_unoccluded_guide_view": dv["guide_view"],
                 "visible_from_the_arena_centre_play_frame": {"share": dv["play_frame"]["share_in_frame_him_at_the_arena_centre"],
                                                              "PASS": dv["play_frame"]["share_in_frame_him_at_the_arena_centre"] >= 0.99},
                 # TWO READINGS OF "visible from the arena": from a place IN the arena, and from its
                 # centre. Both are reported; neither is allowed to stand in for the other.
                 "visible_from_inside_the_arena_play_frame": {
                     "first_v_whole_in_frame": dv["play_frame"]["first_v_door_whole_in_frame"],
                     "arena_north_edge_v": A["arena"]["centre_uv"][1] + A["arena"]["required_r"],
                     "band_m": r(A["arena"]["centre_uv"][1] + A["arena"]["required_r"] - dv["play_frame"]["first_v_door_whole_in_frame"]),
                     "PASS": bool(0 <= dv["play_frame"]["first_v_door_whole_in_frame"] <= A["arena"]["centre_uv"][1] + A["arena"]["required_r"]),
                     "_read": "him on the centre line facing N, the camera following: the face is whole AND unoccluded (magenta share >= 0.99 of the door-centred frame, everything drawn) from this v to the arena's r-7 north edge"},
                 "first_v_door_half_in_frame": dv["play_frame"]["first_v_half_in_frame"],
                 "first_v_door_whole_in_frame": dv["play_frame"]["first_v_door_whole_in_frame"],
                 "why": dv["play_frame"]["_why_zero_at_the_centre"], "_instrument": dv["instrument"]}
    A["frame_cost_ms"] = rep.get("frame_cost_ms")
    # THE EXPORTED APP, labelled from each log's OWN viewport line -- not from an assumption about
    # the display. v1's figure was fullscreen on a 1920 x 1080 display; the display is now a
    # 3440 x 1440 ultrawide, where fullscreen is 2.4x the pixels of the play frame. So the 1080p
    # line is the app's default 1920 x 1080 window, and fullscreen is reported beside it.
    runs = []
    for name, mode in (("app_frame_cost.log", "windowed 1920 x 1080 (the app's default window)"),
                       ("app_frame_cost_repeat.log", "windowed 1920 x 1080, repeat run"),
                       ("app_frame_cost_fullscreen_3440x1440.log", "--fullscreen on the 3440 x 1440 display")):
        lg = CAP / "logs" / name
        if not lg.exists():
            continue
        mm = re.search(r"frame_cost ms_per_frame=([0-9.]+) fps=([0-9.]+) viewport=(\d+)x(\d+) frames=(\d+)", lg.read_text())
        if mm:
            runs.append({"mode": mode, "log": "captures/logs/" + name, "ms_per_frame": float(mm.group(1)), "fps": float(mm.group(2)),
                         "viewport": [int(mm.group(3)), int(mm.group(4))], "frames": int(mm.group(5))})
    if runs:
        A["frame_cost_ms"] = dict(A["frame_cost_ms"] or {})
        at1080 = [x["ms_per_frame"] for x in runs if x["viewport"] == [1920, 1080]]
        A["frame_cost_ms"]["exported_app"] = {"runs": runs, "at_1080p_ms_per_frame": at1080,
            "_at": "the staged app, vsync off, MSAA 2x (project setting), him walking a loop in the ring, 600 frames, wall clock / frames; display 3440 x 1440"}
    return A, gr


def crucible(L, built, rep, gr):
    """The wave-arena numbers per spawn: distance to the station, line of sight at eye height,
    walkable path length on the physics grid -- and a re-check that no nudged circle overlaps a
    BUILT stone footprint or the cutting's walls."""
    C = json.loads(json.dumps(L["crucible"]))
    fp = footprints(built)
    st = tuple(C["station"]["uv"])
    dist = gr.geodesic_from(*st)
    walls = [G.open_poly(c["poly"]) for c in built["collider_footprints"] if c["group"] == "mound"]
    los = rep["crucible_los"]["by_spawn"]
    for s in C["spawns"]:
        c = tuple(s["uv"])
        s["distance_to_station_m"] = r(math.dist(c, st), 3)
        s["line_of_sight_to_station"] = los[s["id"]]
        i, j = gr.ij(*c)
        s["walk_path_to_station_m"] = r(float(dist[j, i]), 2) if np.isfinite(dist[j, i]) else None
        s["walk_path_over_straight"] = r(float(dist[j, i]) / max(math.dist(c, st), 1e-6), 3) if np.isfinite(dist[j, i]) else None
        stones = [(pid, fp[pid]["low"]) for pid in fp if pid.startswith("ring_") and len(fp[pid]["low"]) >= 3]
        ov = [pid for pid, poly in stones if G.dist_poly_pt(poly, c) < s["r_m"] - 1e-3]
        ow = [k for k, poly in enumerate(walls) if G.dist_poly_pt(poly, c) < s["r_m"] - 1e-3]
        s["overlaps_built_stone"] = ov
        s["overlaps_cutting_or_mound_collider"] = len(ow) > 0
        s["least_clearance_to_a_built_stone_m"] = r(min(G.dist_poly_pt(poly, c) for pid, poly in stones) - s["r_m"], 3)
    C["_measured"] = {"eye_height_m": rep["crucible_los"]["eye_height_m"], "los_instrument": rep["crucible_los"]["instrument"],
                      "path_instrument": "Dijkstra from the station over the reachable cells of the 0.1 m physics grid, 16-connected (error < 2.7% on a straight walk)",
                      "still": "captures/still_crucible.png (2400 x 1500 at the play camera's scale)",
                      "all_marks_in_the_still": rep["still_crucible"]["marks_projected_px"].get("_all_inside")}
    return C


def findings(L, built, rep, A):
    P = {e["id"]: e for e in L["placements"]}
    R = built["records"]
    fp = footprints(built)
    F = {}
    m = P["mound"]
    a_, b_ = m["semi_axes"]
    cot = math.cos(PITCH) / math.sin(PITCH)
    def dome(u, v):
        rr = (u / a_) ** 2 + ((v - m["uv"][1]) / b_) ** 2
        if rr >= 1:
            return 0.0
        t = min(max((1 - math.sqrt(rr)) / m.get("toe_rho", 1e-4), 0.0), 1.0)
        return m["rise_m"] * (1 - rr) ** m["exponent"] * t * t * (3 - 2 * t)
    sil = max(v + cot * dome(u, v) for u in np.linspace(-a_, a_, 61) for v in np.linspace(m["uv"][1] - b_, m["uv"][1] + b_, 181))
    F["mound_silhouette_vs_the_window_top"] = {"mound_top_v_eq": r(sil), "window_top_v": L["frame"]["guide_window"]["v"][1],
                                               "past_the_edge_m": r(sil - L["frame"]["guide_window"]["v"][1]),
                                               "past_the_edge_px": r((sil - L["frame"]["guide_window"]["v"][1]) * PX_UP, 1),
                                               "back_foot_v": m["uv"][1] + b_}
    tc = L["regions"]["ice"]["centre_uv"]
    ta, tb = L["regions"]["ice"]["axes_m"][0] / 2, L["regions"]["ice"]["axes_m"][1] / 2
    on_ice = {}
    for pid, f in fp.items():
        if pid.startswith("shore_rock") or len(f["low"]) < 3:
            continue
        c, _ = G.centroid_area(f["low"])
        if any(((p[0] - tc[0]) / ta) ** 2 + ((p[1] - tc[1]) / tb) ** 2 < 1.0 for p in f["low"]) or \
                ((c[0] - tc[0]) / ta) ** 2 + ((c[1] - tc[1]) / tb) ** 2 < 1.0:
            on_ice[pid] = True
    F["pieces_touching_the_ice"] = sorted(on_ice)
    F["fallen_stone_to_cover_outcrop_m"] = r(G.dist_poly_poly(fp["ring_m95"]["low"], fp["cover_outcrop"]["low"]))
    F["plus_minus_35_stones_to_mound_rim_collider_m"] = r(min(G.dist_poly_poly(fp[k]["low"], G.open_poly(c["poly"]))
                                                         for k in ("ring_p35", "ring_m35")
                                                         for c in built["collider_footprints"] if c["group"] == "mound"))
    F["door_threshold_stops_him_at_v"] = A["walks"]["ice_to_the_door"]["end_uv"][1] if "walks" in A else None
    return F


# --- the map ------------------------------------------------------------------------------------
def font(sz, bold=False):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf"] if bold else []) + \
             ["/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_map(L, built, rep, grid, A, C, F):
    top = Image.open(CAP / "topdown.png").convert("RGB")
    T = rep["topdown"]
    ppm = T["px_per_m"]
    tu0, tv1 = T["u"][0], T["v"][1]
    W0, H0 = top.size
    ML, MR, MT, MB = 110, 600, 140, 110
    canvas = Image.new("RGB", (W0 + ML + MR, H0 + MT + MB), (246, 244, 239))
    canvas.paste(Image.blend(top, Image.new("RGB", top.size, (255, 255, 255)), 0.28), (ML, MT))
    d = ImageDraw.Draw(canvas, "RGBA")

    def px(u, v):
        return (ML + (u - tu0) * ppm, MT + (tv1 - v) * ppm)
    f13, f15, f17, f22, f28, f38 = font(15), font(17), font(19), font(24, True), font(30, True), font(40, True)
    halo = {"stroke_width": 3, "stroke_fill": (255, 255, 255)}
    # the flood fill's outline
    gr = Grid(grid)
    reach = gr.reach
    edge = reach & ~(np.roll(reach, 1, 0) & np.roll(reach, -1, 0) & np.roll(reach, 1, 1) & np.roll(reach, -1, 1))
    for j, i in zip(*np.nonzero(edge)):
        x, y = px(*gr.uv(i, j))
        d.rectangle([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(40, 150, 60, 200))
    # 5 m grid
    for g in range(-30, 30, 5):
        if not (T["u"][0] <= g <= T["u"][1]):
            continue
        x, _ = px(g, 0)
        d.line([x, MT, x, MT + H0], fill=(90, 90, 90, 110 if g else 170), width=1 if g else 2)
        d.text((x, MT - 26), "u %+d" % g if g else "u 0", font=f15, fill=(40, 40, 40), anchor="mm")
    for g in range(-25, 25, 5):
        if not (T["v"][0] <= g <= T["v"][1]):
            continue
        _, y = px(0, g)
        d.line([ML, y, ML + W0, y], fill=(90, 90, 90, 110 if g else 170), width=1 if g else 2)
        d.text((ML - 12, y), "v %+d" % g if g else "v 0", font=f15, fill=(40, 40, 40), anchor="rm")
    # the window and the 4 x 4 chunks
    gw = L["frame"]["guide_window"]
    d.rectangle([*px(gw["u"][0], gw["v"][1]), *px(gw["u"][1], gw["v"][0])], outline=(20, 20, 20, 255), width=4)
    for ch in L["frame"]["chunks"]["list"]:
        gu, gv = ch["ground_uv"]["u"], ch["ground_uv"]["v"]
        d.rectangle([*px(gu[0], gv[1]), *px(gu[1], gv[0])], outline=(225, 120, 20, 230), width=3)
    su, sv = 256 / PPM, 256 / PX_UP
    for c in range(1, L["frame"]["chunks"]["cols"]):
        u0 = gw["u"][0] + c * 1280 / PPM
        d.rectangle([*px(u0, gw["v"][1]), *px(u0 + su, gw["v"][0])], fill=(225, 120, 20, 34))
    for rr in range(1, L["frame"]["chunks"]["rows"]):
        v1 = gw["v"][1] - rr * 768 / PX_UP
        d.rectangle([*px(gw["u"][0], v1), *px(gw["u"][1], v1 - sv)], fill=(225, 120, 20, 34))
    for ch in L["frame"]["chunks"]["list"]:
        gu, gv = ch["ground_uv"]["u"], ch["ground_uv"]["v"]
        x, y = px((gu[0] + gu[1]) / 2, gv[1])
        d.text((x, y + 15), "chunk %s" % ch["key"], font=f17, fill=(190, 90, 10), anchor="mm")
    # the reach box (where his centre may stand for the camera margin)
    rb = L["frame"]["reach_box"]
    a, b = px(rb["u"][0], rb["v"][1]), px(rb["u"][1], rb["v"][0])
    for x in np.arange(a[0], b[0], 18):
        d.line([x, a[1], min(x + 9, b[0]), a[1]], fill=(20, 140, 20, 230), width=2)
        d.line([x, b[1], min(x + 9, b[0]), b[1]], fill=(20, 140, 20, 230), width=2)
    for y in np.arange(a[1], b[1], 18):
        d.line([a[0], y, a[0], min(y + 9, b[1])], fill=(20, 140, 20, 230), width=2)
        d.line([b[0], y, b[0], min(y + 9, b[1])], fill=(20, 140, 20, 230), width=2)
    # regions
    Rg = L["regions"]

    def ell(c, aa, bb, n=180):
        return [px(c[0] + aa * math.cos(t), c[1] + bb * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n)]
    d.line(ell(Rg["ring"]["centre_uv"], 9, 9), fill=(120, 120, 130, 200), width=2)
    arena = ell(Rg["arena"]["centre_uv"], Rg["arena"]["r"], Rg["arena"]["r"])
    for i in range(0, len(arena) - 1, 2):
        d.line([arena[i], arena[i + 1]], fill=(30, 70, 220, 255), width=4)
    d.line(ell(Rg["ice"]["centre_uv"], Rg["ice"]["axes_m"][0] / 2, Rg["ice"]["axes_m"][1] / 2), fill=(20, 130, 170, 255), width=3)
    mnd = [e for e in L["placements"] if e["id"] == "mound"][0]
    d.line(ell(mnd["uv"], *mnd["semi_axes"]), fill=(120, 70, 30, 255), width=3)
    pp = Rg["path"]["extended_off_frame_uv"]
    for side in (-1, 1):
        pts = []
        for i, p in enumerate(pp):
            dp = np.array([0.0, 0.0])
            if i > 0:
                q = np.array(p) - np.array(pp[i - 1])
                dp += q / np.linalg.norm(q)
            if i < len(pp) - 1:
                q = np.array(pp[i + 1]) - np.array(p)
                dp += q / np.linalg.norm(q)
            dp /= np.linalg.norm(dp)
            nrm = np.array([-dp[1], dp[0]]) * 2.0 * side
            pts.append(px(p[0] + nrm[0], p[1] + nrm[1]))
        d.line(pts, fill=(120, 80, 40, 255), width=3)
    bp = L["bounds"]["polygon_uv"]
    for i in range(len(bp)):
        a2, b2 = bp[i], bp[(i + 1) % len(bp)]
        col = (240, 200, 0, 255) if i == L["bounds"]["entry_edge_index"] else (210, 25, 25, 255)
        d.line([px(*a2), px(*b2)], fill=col, width=5 if i != L["bounds"]["entry_edge_index"] else 6)
    # the crucible
    rune = tuple(int(x * 255) for x in L["tints_srgb"]["rune"])
    for s in C["spawns"]:
        u, v = s["uv"]
        rr = s["r_m"]
        d.ellipse([*px(u - rr, v + rr), *px(u + rr, v - rr)], outline=rune + (255,), width=5)
        if s["nudge_m"] != 0.0:
            d.line([px(*s["spec_uv"]), px(u, v)], fill=(20, 60, 160, 255), width=2)
        d.text(px(u, v), s["id"], font=f22, fill=(20, 60, 160), anchor="mm", **halo)
    bg = C["boss_gate"]["uv"]
    d.line([px(-C["boss_gate"]["width_m"] / 2, bg[1]), px(C["boss_gate"]["width_m"] / 2, bg[1])], fill=(230, 110, 30, 255), width=8)
    d.text(px(0, bg[1] - 1.3), "BOSS GATE", font=f17, fill=(200, 80, 10), anchor="mm", **halo)
    stp = C["station"]["uv"]
    d.ellipse([*px(stp[0] - 0.75, stp[1] + 0.75), *px(stp[0] + 0.75, stp[1] - 0.75)], outline=(40, 40, 40, 255), width=3)
    d.text(px(stp[0], stp[1] - 1.2), "STATION", font=f15, fill=(30, 30, 30), anchor="mm", **halo)
    # piece labels
    P = {e["id"]: e for e in L["placements"]}
    Rr = built["records"]
    for pid, e in P.items():
        rec = Rr.get(pid)
        if not rec:
            continue
        if e["kind"] == "primitive":
            bc = rec["base_centroid_world"]
            u, v = xz_to_uv(bc[0], bc[2])
        else:
            u, v = built_uv(rec)
        t = None
        if pid.startswith("ring_"):
            t = "%+d%s%s" % (e["theta_deg"], {"stone_tall": "T", "stone_mid": "M", "stone_short": "S"}[e["class"]], " fallen" if e.get("tip") else "")
            v -= 1.0 if e["theta_deg"] in (35, -35, 55, -55) else 0.0
        elif pid.startswith("outcrop_"):
            t = "O%s %.1fm" % (pid.split("_")[1], e["height_m"])
        elif pid.startswith("margin_outcrop_"):
            t = "M%s" % pid.split("_")[2]
        elif pid.startswith("cairn_"):
            t = "C%s" % pid.split("_")[1]
        elif pid.startswith("grave_marker"):
            t = "grave"
        elif pid == "cover_outcrop":
            t = "cover 3x2x1.4"
        elif pid == "door_lintel":
            t = "DOOR"
            v -= 0.9
        elif pid == "raven":
            t = "raven"
            u += 1.0
        elif pid == "fallen_tree_log_A":
            t = "fallen tree"
            v -= 0.8
        if t:
            d.text(px(u, v), t, font=f13, fill=(15, 15, 15), anchor="mm", **halo)
    for g, c in (("G1", (7, -11)), ("G2", (-10, 9.5)), ("G3", (13, -6)), ("G4", (10, 12))):
        x, y = px(*c)
        d.text((x, y - 50), g, font=f17, fill=(20, 80, 30), anchor="mm", **halo)
    x, y = px(0, 14.2)
    d.text((x, y), "BARROW MOUND 12 x 9 m, rise %.1f m, kerbed" % mnd["rise_m"], font=f17, fill=(90, 50, 15), anchor="mm", **halo)
    for t, (u, v) in (("1 THE APPROACH", (4.4, -14.2)), ("2 THE TARN", (-13.5, -1.2)), ("3 THE RING", (2.8, 3.4)), ("4 THE DOOR", (0, 7.35))):
        x, y = px(u, v)
        d.text((x, y), t, font=f28, fill=(20, 20, 60), anchor="mm", stroke_width=4, stroke_fill=(255, 255, 255))
    x, y = px(-3, -16.2)
    d.text((x - 150, y + 20), "ENTRY / exit line v -16.2", font=f15, fill=(120, 90, 0), anchor="mm", **halo)
    d.text((ML, 28), "C-9 T10-2 step 1 (spec v2)  —  THE FROST KING'S BARROW, FULL AREA: blockout map", font=f38, fill=(15, 15, 15))
    d.text((ML, 80), "Top-down, true metres, (u, v) in the play camera's ground frame: +u screen-right, +v up-screen. Arena at (0, 1). "
                     "5 m grid; the 4 x 4 paint chunks; base = the built greybox straight down (40 px/m).", font=f15, fill=(40, 40, 40))
    # legend and numbers
    lx, ly = ML + W0 + 30, MT
    d.text((lx, ly), "LEGEND", font=f22, fill=(15, 15, 15))
    ly += 40
    T2 = L["tints_srgb"]
    for nm, key in (("snow", "snow"), ("trodden path", "path"), ("tarn ice (walkable)", "ice"), ("juniper / heather scrub", "shrub"),
                    ("real models, flat grey", "hero_grey"), ("primitives", "primitive_grey"), ("the mound", "mound")):
        d.rectangle([lx, ly, lx + 34, ly + 22], fill=tuple(int(x * 255) for x in T2[key]), outline=(60, 60, 60))
        d.text((lx + 46, ly + 11), nm, font=f15, fill=(20, 20, 20), anchor="lm")
        ly += 30
    ly += 6
    for nm, col, w in (("play bounds (invisible walls)", (210, 25, 25), 5), ("entry / exit line", (240, 200, 0), 6),
                       ("arena r 7 about (0, 1)", (30, 70, 220), 4), ("stone ring r 9 about (0, 2)", (120, 120, 130), 2),
                       ("path band 4 m", (120, 80, 40), 3), ("tarn ice edge", (20, 130, 170), 3), ("mound foot", (120, 70, 30), 3),
                       ("reachable from the entry (flood fill)", (40, 150, 60), 4), ("camera-margin reach box", (20, 140, 20), 2),
                       ("window 5376 x 3328 px", (20, 20, 20), 4), ("paint chunk 1536 x 1024 px", (225, 120, 20), 3),
                       ("crucible spawn, r 1.5", rune, 5), ("boss gate", (230, 110, 30), 8)):
        d.line([lx, ly + 11, lx + 34, ly + 11], fill=col, width=w)
        d.text((lx + 46, ly + 11), nm, font=f15, fill=(20, 20, 20), anchor="lm")
        ly += 28
    ly += 14
    d.text((lx, ly), "MEASURED", font=f22, fill=(15, 15, 15))
    ly += 34
    acc = [("placements <= 0.05 m", A["placements"]["all_spec_points_within_tolerance"], "worst %.3f m" % A["placements"]["worst_delta_m"]),
           ("flood fill: arena, ice, door", A["flood_fill"]["PASS"], "%d cells outside the bounds" % A["flood_fill"]["reachable_outside_bounds_cells"]),
           ("mound non-walkable; floor y = 0 to the door", A["mound_and_door_floor"]["PASS"], "passage refused: %s" % A["mound_and_door_floor"]["passage_walk_refused"]),
           ("arena clear to r 7", A["arena"]["PASS"], "clear to %.2f m" % A["arena"]["clear_r_walkable_m"]),
           ("path clear at 4 m", A["path"]["PASS"], "min %.2f m spare" % (A["path"]["min_clearance_m"] or 99)),
           ("ring entrance >= 6 m", A["ring_entrance"]["PASS"], "%.2f m" % A["ring_entrance"]["clear_gap_m"]),
           ("1 m marker = 100.6 px", A["scale"]["PASS"], "%.2f px (2 m: x%.3f / x%.3f)" % (A["scale"]["one_metre_across_px"], A["scale"]["instrument_proof"]["u_2m_over_u_1m"], A["scale"]["instrument_proof"]["v_2m_over_v_1m"])),
           ("no squeezes (<0.70 or >=1.40)", A["no_squeezes"]["PASS"], "%d gaps in [0.70, 1.40)" % len(A["no_squeezes"]["squeezes"])),
           ("camera margin: 0 px outside", A["camera_margin"]["PASS"], "worst side %+.0f px" % max(A["camera_margin"]["worst_px_outside_by_side"].values())),
           ("door covered >= 0.3 m", A["door"]["cover"]["PASS"], "cover %.2f m" % A["door"]["cover"]["cover_m"]),
           ("door face whole from inside the arena", A["door"]["visible_from_inside_the_arena_play_frame"]["PASS"],
            "from v %.2f to the arena's edge v %.1f" % (A["door"]["first_v_door_whole_in_frame"], A["door"]["visible_from_inside_the_arena_play_frame"]["arena_north_edge_v"])),
           ("door face in frame from the arena CENTRE", A["door"]["visible_from_the_arena_centre_play_frame"]["PASS"],
            "%.0f%%: the frame's top is v 8.41, the door v 10.3" % (100 * A["door"]["visible_from_the_arena_centre_play_frame"]["share"]))]
    for nm, ok, val in acc:
        d.text((lx, ly), ("PASS  " if ok else "FAIL  ") + nm, font=f15, fill=(20, 110, 40) if ok else (190, 20, 20))
        d.text((lx + 24, ly + 20), val, font=f13, fill=(60, 60, 60))
        ly += 44
    x0, y0 = px(14.0, -24.8)
    d.line([x0, y0, x0 + 5 * ppm, y0], fill=(0, 0, 0), width=5)
    d.text((x0 + 2.5 * ppm, y0 - 14), "5 m", font=f15, fill=(0, 0, 0), anchor="mm")
    out = CAP / "barrow_full_map.png"
    canvas.save(out, optimize=True)
    return out


# --- paint staging ------------------------------------------------------------------------------
def stage_paint(L):
    PAINT.mkdir(exist_ok=True)
    guide = PAINT / "barrow_full_guide.png"
    shutil.copyfile(CAP / "guide.png", guide)
    im = Image.open(guide)
    gp = tuple(L["frame"]["guide_window"]["px"])
    assert im.size == gp, (im.size, gp)
    cfg = {
        "prefix": "T10BF",
        "name": "THE FROST KING'S BARROW, full area: paint-over of the gameplay blockout (T10-2 step 2, spec v2)",
        "guide": str(guide), "cols": L["frame"]["chunks"]["cols"], "rows": L["frame"]["chunks"]["rows"],
        "experiment": "T10-2-barrow-full-paintover",
        "_status": "STAGED BY drax, NOT FIRED. Painting waits for Matt's look at the map and the greybox. The conductor copies this into conductor_scripts/ and the CS9-guides manifest when painting is approved.",
        "_guide_sha256": hashlib.sha256(guide.read_bytes()).hexdigest(),
        "_guide_frame": "%d x %d px = u %.2f..%.2f m, v %.2f..%.2f m at the play camera (orthographic, pitch 52.95354112560294, yaw 47): 100.6176 px per metre across, 80.3076 px per ground metre up-screen" % (
            gp[0], gp[1], *L["frame"]["guide_window"]["u"], *L["frame"]["guide_window"]["v"]),
        "_note_for_the_conductor": "guided_paint.py's retry clause names a #00ff00 sky; this guide has none (the conductor: 'mine to fix when I write the paint briefs'). The crucible marks are NOT in the guide. The barbarian stands in the arena for scale only; the rules ask for him to be painted out (ratified).",
        "geo": ("IMAGE 1 is not a flat-colour layout: it is a GREYBOX RENDER of a real 3D game level, seen from the game's fixed high "
                "three-quarter ORTHOGRAPHIC camera (53 degrees down), at true scale -- the small painted barbarian in the ring is 1.85 m tall. "
                "Every grey form is a real object that will be modelled at exactly this position and size. LIGHT WARM GREY ground = deep, "
                "smooth snow; the DARKER BROWN-GREY BAND = a trodden path through the snow; PALE BLUE-GREY = the frozen tarn, flat lapis-blue "
                "ice with pale cracks; MUTED GREEN-BROWN PATCHES = low dark juniper scrub and rust-brown winter heather poking through the "
                "snow; FLAT GREY upright slabs = fourteen carved standing stones in a ring (spiral and knotwork carvings on the faces turned "
                "toward the viewer), one FALLEN and lying outward; the LARGE PALE DOME at the top = the barrow mound, earth and dead grass "
                "under thin snow, KERBED (steep sides, rounded top), running off the top of the picture; cut into its front, a stone-lined "
                "CUTTING leads to the door -- two grey posts and a massive carved lintel set into a stone facade, the mound rising over them, "
                "a DARK passage stepping down behind; the DARKER GREY STEPPED MASSES = weathered layered rock outcrops (and a low rocky shore "
                "on the tarn's far side); thin grey trees = dead wind-bent birches, in groves and in tree lines at the edges; small grey stacks "
                "= stone cairns; the two grey crosses of spears with a round shield = grave markers; the long grey cylinders = a fallen birch "
                "trunk; a tiny grey bird on a stone = a raven."),
        "rules": ("Paint OVER the render: every object keeps EXACTLY its silhouette, position and size (the 3D models are placed from this "
                  "same layout, so anything moved will not match); shadows stay where the render puts them (one winter sun from the upper "
                  "LEFT, 55 degrees up, short soft blue-violet shadows touching their objects). Paint the barbarian OUT -- he is there only "
                  "for scale; leave open snow where he stands. Keep the ring's centre, the path, the cutting and the tarn OPEN: no new rocks, "
                  "trees or drifts on them. Small scatter is welcome only inside the scrub patches and at the foot of rocks and stones. One "
                  "thin warm dark-brown ink line on every contour, the SAME weight everywhere. Palette and hand of IMAGE 2 (the approved "
                  "Frost King's Barrow concept): cold blue-white snow, warm grey granite, rust heather, dark juniper, lapis ice; watercolour "
                  "washes with pen detail. No sky, no horizon, no text, UI, border or characters."),
        "refs": [[str(B / "runs/C-9/artifacts/T10C-barrow/T10C-barrow_a.png"),
                  "the APPROVED Frost King's Barrow concept (Matt's pick): palette, light, snow, stone carving and painted hand ONLY -- NOT its layout"]],
        "chunks": L["frame"]["chunks"]["list"],
    }
    (PAINT / "cfg_barrow_full.json").write_text(json.dumps(cfg, indent=1, ensure_ascii=False, default=_np))
    return cfg


def previews(L):
    g = Image.open(CAP / "guide.png").convert("RGB")
    W, H = g.size
    g.resize((W // 4, H // 4), Image.LANCZOS).save(CAP / "guide_preview.png", optimize=True)
    q = g.resize((W // 2, H // 2), Image.LANCZOS)
    d = ImageDraw.Draw(q, "RGBA")
    s = 0.5
    ch = L["frame"]["chunks"]
    for c in range(ch["cols"]):
        for rr in range(ch["rows"]):
            x0, y0 = c * 1280 * s, rr * 768 * s
            d.rectangle([x0, y0, x0 + 1536 * s - 1, y0 + 1024 * s - 1], outline=(235, 120, 20, 255), width=3)
            d.text((x0 + 14, y0 + 10), "chunk %d_%d" % (c, rr), font=font(26, True), fill=(235, 120, 20), stroke_width=3, stroke_fill=(255, 255, 255))
    q.save(CAP / "guide_preview_chunks.png", optimize=True)


def main():
    L, built, rep, grid = load()
    marks = measure_markers(rep)
    A, gr = acceptance(L, built, rep, grid, marks)
    C = crucible(L, built, rep, gr)
    F = findings(L, built, rep, A)
    for e in L["placements"]:
        rec = built["records"].get(e["id"])
        if rec is None:
            continue
        keep = {k: rec[k] for k in rec if k not in ("footprint_uv_all",)}
        if e["kind"] == "primitive":
            bc = rec["base_centroid_world"]
            keep["built_uv"] = [r(v) for v in xz_to_uv(bc[0], bc[2])]
        else:
            keep["built_uv"] = [r(v) for v in built_uv(rec)]
        e["built"] = keep
    L["crucible"] = C
    L["acceptance"] = A
    L["findings_measured"] = F
    L["built_from"] = {"scene": "runs/C-9/barrow_full/godot/scenes/barrow_full.tscn",
                       "capture": "godot/tools/capture_blockout.gd -> captures/",
                       "_": "'built' in each placement is measured off the scene, not copied from the design",
                       "script_copies": {"from": "runs/C-9/cliffside3d/godot at git HEAD (knight.gd with the attack fix f2140e680, paint_stack.gd and snow_field.gd with the T10-1b snow pass b90943fbe, character.json), byte-identical, unmodified; nb-body.glb md5 f1017ee14dfe055bc77d54bb393fccbb from disk"}}
    (ROOT / "barrow_full_layout.json").write_text(json.dumps(L, indent=1, default=_np))
    (CAP / "acceptance.json").write_text(json.dumps({"acceptance": A, "crucible": C, "findings": F}, indent=1, default=_np))
    mp = draw_map(L, built, rep, grid, A, C, F)
    previews(L)
    stage_paint(L)
    summary = {k: A[k]["PASS"] for k in ("placements", "flood_fill", "mound_and_door_floor", "arena", "path", "ring_entrance",
                                         "scale", "no_squeezes", "camera_margin") if "PASS" in A[k]}
    summary["placements"] = A["placements"]["all_spec_points_within_tolerance"]
    summary["door_cover"] = A["door"]["cover"]["PASS"]
    summary["door_whole_from_inside_the_arena"] = A["door"]["visible_from_inside_the_arena_play_frame"]["PASS"]
    summary["door_visible_from_arena_centre"] = A["door"]["visible_from_the_arena_centre_play_frame"]["PASS"]
    print(json.dumps({"pass": summary, "worst_placement_m": A["placements"]["worst_delta_m"],
                      "arena_clear": A["arena"]["clear_r_walkable_m"], "path_spare": A["path"]["min_clearance_m"],
                      "entrance": A["ring_entrance"]["clear_gap_m"], "marker_1m": A["scale"]["one_metre_across_px"],
                      "marker_proof": A["scale"]["instrument_proof"], "squeezes": A["no_squeezes"]["squeezes"],
                      "camera_margin": A["camera_margin"]["worst_px_outside_by_side"], "door": A["door"]["cover"]["cover_m"],
                      "door_first_whole_v": A["door"]["first_v_door_whole_in_frame"], "door_guide_unoccluded": A["door"]["visible_unoccluded_guide_view"]["unoccluded_share"],
                      "walks": {k: v.get("PASS") for k, v in A.get("walks", {}).items() if isinstance(v, dict)},
                      "crucible": [(s["id"], s["distance_to_station_m"], s["line_of_sight_to_station"]["clear"], s["walk_path_to_station_m"], s["nudge_m"], s["overlaps_built_stone"]) for s in C["spawns"]],
                      "frame_cost": A["frame_cost_ms"], "findings": F, "map": str(mp)}, indent=1, default=_np))
    if "--stage" in sys.argv:
        STAGE.mkdir(parents=True, exist_ok=True)
        for src, dst in ((CAP / "barrow_full_map.png", "1 - top-down map (5 m grid, 4x4 paint chunks).png"),
                         (CAP / "guide.png", "2 - the guide, 5376x3328 (play camera, true scale).png"),
                         (CAP / "guide_preview.png", "2a - the guide, preview 1344x832.png"),
                         (CAP / "guide_preview_chunks.png", "2b - the guide, preview with the 4x4 chunk grid.png"),
                         (CAP / "still_ring.png", "3 - play screen, the ring arena.png"),
                         (CAP / "still_tarn.png", "4 - play screen, the tarn.png"),
                         (CAP / "still_crucible.png", "5 - the crucible marks, play camera scale.png"),
                         (CAP / "still_door.png", "6 - play screen, where the door first shows whole.png"),
                         (CAP / "acceptance.json", "measurements - acceptance.json")):
            shutil.copyfile(src, STAGE / dst)
        for old in ("1 - top-down map (5 m grid, 3x3 paint chunks).png", "2 - the guide, 4096x2560 (play camera, true scale).png",
                    "2a - the guide, preview 1024x640.png", "2b - the guide, preview with the 3x3 chunk grid.png"):
            (STAGE / old).unlink(missing_ok=True)
        print("== staged ->", STAGE)


if __name__ == "__main__":
    main()
