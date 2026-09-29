#!/usr/bin/env python3
"""C-9 T10-2 step 1 -- FINALIZE: measure the blockout against the spec, merge, map, stage.

    python3 tools/finalize.py [--stage]

Reads captures/ (what the Godot scene BUILT and what the capture tool MEASURED) and writes:
    ../barrow_full_layout.json   the deliverable: design numbers + built transforms + acceptance
    captures/acceptance.json     every acceptance line with its number and its instrument
    captures/barrow_full_map.png the labelled top-down map (5 m grid, 3x3 paint-chunk grid)
    captures/guide_preview*.png  the guide, downscaled (plain, and with the chunk grid)
    paint/barrow_full_guide.png + paint/cfg_barrow_full.json   staged for guided_paint.py, NOT fired
--stage also copies the review set into the Desktop review folder.

EVERY NUMBER HERE IS RE-DERIVED FROM THE BUILT SCENE THROUGH THE ANALYTIC FRAME. The scene built
in the camera's LIVE ground basis; this file reads the built world transforms back through
cos 47 / sin 47 by itself, so a basis the two disagree on shows up as a placement error rather
than cancelling out.
"""
import hashlib
import json
import math
import pathlib
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
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


# --- 2D geometry -----------------------------------------------------------------------------
def seg_pt(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return math.hypot(p[0] - (ax + t * dx), p[1] - (ay + t * dy))


def in_poly(p, poly):
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xi:
                inside = not inside
    return inside


def seg_x(a, b, c, d):
    def o(p, q, s):
        return (q[0] - p[0]) * (s[1] - p[1]) - (q[1] - p[1]) * (s[0] - p[0])
    return (o(a, b, c) * o(a, b, d) < 0) and (o(c, d, a) * o(c, d, b) < 0)


def poly_edges(poly, closed=True):
    n = len(poly)
    return [(poly[i], poly[(i + 1) % n]) for i in range(n if closed else n - 1)]


def dist_poly_pt(poly, p):
    if len(poly) >= 3 and in_poly(p, poly):
        return 0.0
    return min(seg_pt(p, a, b) for a, b in poly_edges(poly))


def dist_poly_poly(P, Q, q_closed=True):
    """0 if they touch or overlap; else the least distance between them."""
    if not P or not Q:
        return None
    if q_closed and len(Q) >= 3 and any(in_poly(p, Q) for p in P):
        return 0.0
    if len(P) >= 3 and any(in_poly(q, P) for q in Q):
        return 0.0
    EP = poly_edges(P)
    EQ = poly_edges(Q, q_closed)
    for a, b in EP:
        for c, d in EQ:
            if seg_x(a, b, c, d):
                return 0.0
    d1 = min(seg_pt(p, c, d) for p in P for c, d in EQ)
    d2 = min(seg_pt(q, a, b) for q in Q for a, b in EP)
    return min(d1, d2)


def centroid_area(poly):
    A = cx = cy = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        c = x1 * y2 - x2 * y1
        A += c
        cx += (x1 + x2) * c
        cy += (y1 + y2) * c
    A *= 0.5
    if abs(A) < 1e-12:
        return (sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n), 0.0
    return (cx / (6 * A), cy / (6 * A)), abs(A)


def poly_in_ellipse_area(poly, c, a, b, step=0.02):
    """Area of `poly` inside the ellipse, by raster at `step` m (the instrument for 'a stone
    standing in the ice')."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    U, V = np.meshgrid(np.arange(min(xs), max(xs), step), np.arange(min(ys), max(ys), step))
    inside = np.zeros(U.shape, dtype=bool)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cond = (y1 > V) != (y2 > V)
        xi = x1 + (V - y1) * (x2 - x1) / ((y2 - y1) if y2 != y1 else 1e-12)
        inside ^= cond & (U < xi)
    ell = ((U - c[0]) / a) ** 2 + ((V - c[1]) / b) ** 2 <= 1.0
    return float((inside & ell).sum()) * step * step


# --- load --------------------------------------------------------------------------------------
def load():
    L = json.loads((ROOT / "barrow_full_layout.json").read_text())
    built = json.loads((CAP / "built.json").read_text())
    rep = json.loads((CAP / "capture_report.json").read_text())
    grid = json.loads((CAP / "walk_grid.json").read_text())
    return L, built, rep, grid


def built_uv(rec):
    o = rec["world_origin"]
    return xz_to_uv(o[0], o[2])


# --- the marker instrument ---------------------------------------------------------------------
def measure_markers(rep):
    """A MARKER'S LENGTH IN PIXELS, BY COVERAGE, on the delivered guide's own camera. Along the
    bar's centre line each pixel's coverage is its position between the local ground colour and
    the marker's pure colour (MSAA leaves fractional pixels at the ends); the coverage summed is
    the length. Proven on its own before it is believed: the 2 m marker must read double the
    1 m one, in both directions."""
    srgb = np.asarray(Image.open(CAP / "guide_calibration.png").convert("RGB")).astype(np.float64) / 255.0
    # COVERAGE IS LINEAR. MSAA resolves the 3D buffer in linear light and the PNG stores sRGB, so
    # a half-covered end pixel is NOT half-way in sRGB bytes: measured in bytes every bar came out
    # 0.1-0.4 px short at the ends (1 m read 100.31). paint_stack.gd's header says the same about
    # its own instrument: an 8-bit target stores sRGB and reading it as linear is the error.
    img = np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)
    H, W = img.shape[:2]
    out = {}
    for k, m in rep["guide"]["markers"].items():
        (x0, y0), (x1, y1) = m["projected_px"]
        col = np.array(m["rgb"], dtype=np.float64)
        col = np.where(col <= 0.04045, col / 12.92, ((col + 0.055) / 1.055) ** 2.4)
        horizontal = abs(x1 - x0) > abs(y1 - y0)
        lengths = []
        if horizontal:
            yc = int(round((y0 + y1) / 2.0 - 0.5))
            lo, hi = int(math.floor(min(x0, x1))) - 10, int(math.ceil(max(x0, x1))) + 10
            for dy in (-2, -1, 0, 1, 2):
                row = img[yc + dy, lo:hi]
                bg = np.median(np.concatenate([row[:6], row[-6:]]), axis=0)
                d = col - bg
                cov = np.clip(((row - bg) @ d) / float(d @ d), 0.0, 1.0)
                lengths.append(float(cov.sum()))
        else:
            xc = int(round((x0 + x1) / 2.0 - 0.5))
            lo, hi = int(math.floor(min(y0, y1))) - 10, int(math.ceil(max(y0, y1))) + 10
            for dx in (-2, -1, 0, 1, 2):
                colm = img[lo:hi, xc + dx]
                bg = np.median(np.concatenate([colm[:6], colm[-6:]]), axis=0)
                d = col - bg
                cov = np.clip(((colm - bg) @ d) / float(d @ d), 0.0, 1.0)
                lengths.append(float(cov.sum()))
        out[k] = {"length_m": m["length_m"], "axis": "u (across)" if horizontal else "v (up-screen)",
                  "measured_px": round(float(np.median(lengths)), 3),
                  "rows_or_cols": [round(x, 3) for x in lengths],
                  "projected_px": m["projected_length_px"],
                  "expected_px": round(m["length_m"] * (PPM if horizontal else PX_UP), 3)}
    for k, v in out.items():
        if v["measured_px"] < 0.5 * v["expected_px"]:
            raise SystemExit("INSTRUMENT FAILURE: marker %s reads %.2f px against %.2f expected -- the "
                             "calibration frame does not contain the markers; no scale number is reported"
                             % (k, v["measured_px"], v["expected_px"]))
    ratio_u = out["u_2m"]["measured_px"] / out["u_1m"]["measured_px"]
    ratio_v = out["v_2m"]["measured_px"] / out["v_1m"]["measured_px"]
    return {"markers": out,
            "instrument_proof": {"u_2m_over_u_1m": round(ratio_u, 4), "v_2m_over_v_1m": round(ratio_v, 4),
                                 "_expect": 2.0, "PASS": abs(ratio_u - 2.0) < 0.01 and abs(ratio_v - 2.0) < 0.01},
            "one_metre_across_px": out["u_1m"]["measured_px"],
            "_instrument": "coverage-summed pixel length along the bar's centre line in guide_calibration.png (4096x2560, same camera as guide.png), in LINEAR light; median of 5 lines; background = median of 6 px beyond each end",
            "_precision": "MSAA 4x quantises each end's coverage in quarter steps, so a single bar reads to about +-0.3 px; the camera's own projection of the same bars is reported beside each (projected_px)"}


# --- acceptance -------------------------------------------------------------------------------
def footprints(L, built):
    """Per piece, the footprint a man can walk into (vertices under 1.9 m) and the whole one."""
    fp = {}
    for pid, rec in built["records"].items():
        low = [tuple(p) for p in rec.get("footprint_uv_low", [])]
        allp = [tuple(p) for p in rec.get("footprint_uv_all", [])]
        # hulls come back closed (first point repeated); open them
        if len(low) > 1 and low[0] == low[-1]:
            low = low[:-1]
        if len(allp) > 1 and allp[0] == allp[-1]:
            allp = allp[:-1]
        fp[pid] = {"low": low, "all": allp}
    return fp


def acceptance(L, built, rep, grid, marks):
    P = {e["id"]: e for e in L["placements"]}
    R = built["records"]
    fp = footprints(L, built)
    A = {}

    # 1. placements vs the table ------------------------------------------------------------
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
            (got, _) = centroid_area(fp[pid]["all"])
            what = "centroid of the built mound's footprint hull"
        else:
            got = built_uv(rec)
            what = "root origin (footprint centre; the SOCKET for the fallen stone; the trunk base for a birch)"
        spec = e.get("spec_uv")
        ref = e.get("uv")
        row = {"id": pid, "class": e["class"], "built_uv": [r(got[0]), r(got[1])], "measured_as": what}
        if spec is not None:
            d = math.dist(got, spec)
            row.update({"spec_uv": spec, "delta_m": r(d), "PASS": d <= TOL_M})
        elif ref is not None:
            row.update({"derived_uv": ref, "delta_from_derived_m": r(math.dist(got, ref)),
                        "derived_from": e.get("derived_from", "")})
        rows.append(row)
    # the groves: the members' centroid against the table's point
    groves = {}
    for e in L["placements"]:
        if e["class"] == "birch" and e["id"] in R:
            groves.setdefault(e["grove"], {"spec": e["grove_spec_uv"], "pts": []})["pts"].append(built_uv(R[e["id"]]))
    for g, d in sorted(groves.items()):
        c = (sum(p[0] for p in d["pts"]) / len(d["pts"]), sum(p[1] for p in d["pts"]) / len(d["pts"]))
        dd = math.dist(c, d["spec"])
        rows.append({"id": "grove_" + g, "class": "grove", "members": len(d["pts"]), "built_uv": [r(c[0]), r(c[1])],
                     "spec_uv": d["spec"], "delta_m": r(dd), "PASS": dd <= TOL_M,
                     "measured_as": "centroid of the built trunk bases"})
    # the fallen tree: the joint between the two logs' facing ends
    la, lb = R.get("fallen_tree_log_A"), R.get("fallen_tree_log_B")
    if la and lb:
        # EACH LOG'S ENDS OFF ITS OWN BUILT FOOTPRINT. Not off the node's local x: the kit bakes
        # the log's length along the play camera's u (yaw 47 inside the GLB), so the node's x is
        # 47 degrees off the log -- the first version of this measured along it and reported a
        # 0.050 m joint error that was the instrument's. The long axis is the hull's principal
        # direction; the ends are the hull's extreme points along it.
        ends = []
        axes = []
        for rec, far in ((la, 1.0), (lb, -1.0)):
            H = np.array([p for p in rec["footprint_uv_all"]], dtype=np.float64)
            c = H.mean(axis=0)
            w, vec = np.linalg.eigh(np.cov((H - c).T))
            ax = vec[:, int(np.argmax(w))]
            other = np.array(built_uv(lb if rec is la else la))
            if np.dot(other - c, ax) < 0:
                ax = -ax                      # point the axis at the other log
            proj = (H - c) @ ax
            e = H[int(np.argmax(proj))]      # this log's end that faces the other log
            ends.append((float(e[0]), float(e[1])))
            axes.append([round(float(ax[0]), 4), round(float(ax[1]), 4)])
        J = ((ends[0][0] + ends[1][0]) / 2, (ends[0][1] + ends[1][1]) / 2)
        ca, cb = built_uv(la), built_uv(lb)
        Cm = ((ca[0] + cb[0]) / 2, (ca[1] + cb[1]) / 2)
        dd = math.dist(Cm, P["fallen_tree_log_A"]["pair_spec_uv"])
        rows.append({"id": "fallen_tree", "class": "fallen tree (2 logs)", "built_uv": [r(Cm[0]), r(Cm[1])],
                     "spec_uv": P["fallen_tree_log_A"]["pair_spec_uv"], "delta_m": r(dd), "PASS": dd <= TOL_M,
                     "joint_built_uv": [r(J[0]), r(J[1])], "joint_design_uv": P["fallen_tree_log_A"]["joint_uv"],
                     "logs_gap_m": r(math.dist(*ends)), "log_axes_uv": axes,
                     "log_axes_deg_from_u": [r(math.degrees(math.atan2(a[1], a[0])) % 180.0, 2) for a in axes],
                     "measured_as": "midpoint of the two logs' BUILT centres (the pair's centroid); the joint is the midpoint of their facing ends, each the extreme point of the log's built footprint along its principal axis"})
    # the raven: ON the +65 stone
    rv = R.get("raven")
    if rv:
        o = built_uv(rv)
        on = dist_poly_pt(fp["ring_p65"]["all"], o) == 0.0
        rows.append({"id": "raven", "class": "raven", "built_uv": [r(o[0]), r(o[1])],
                     "on": "ring_p65", "over_the_stone": on, "PASS": on,
                     "perch_y": rv["y_min"], "stone_top_y": R["ring_p65"]["y_max"],
                     "measured_as": "raven root inside the +65 stone's footprint, feet at the stone's top"})
    A["placements"] = {"tolerance_m": TOL_M, "rows": rows,
                       "all_spec_points_within_tolerance": all(x.get("PASS", True) for x in rows),
                       "worst_delta_m": r(max([x.get("delta_m") or 0.0 for x in rows])),
                       "basis_residuals": rep["scene"]["camera"]["ground_basis"],
                       "_instrument": "built world transforms (built.json) read back into (u, v) through the ANALYTIC frame, independently of the live camera basis the scene built in"}

    # 2. arena, path, ring entrance ---------------------------------------------------------
    arena = L["regions"]["arena"]
    ac = tuple(arena["centre_uv"])
    near = []
    for pid, f in fp.items():
        if pid in ("mound",):
            continue
        dl = dist_poly_pt(f["low"], ac) if len(f["low"]) >= 3 else None
        da = dist_poly_pt(f["all"], ac) if len(f["all"]) >= 3 else None
        near.append((pid, dl, da))
    m = P["mound"]
    mfoot = [(m["uv"][0] + m["semi_axes"][0] * math.cos(t), m["uv"][1] + m["semi_axes"][1] * math.sin(t))
             for t in np.linspace(0, 2 * math.pi, 721)[:-1]]
    near.append(("mound (its foot, the spec ellipse)", dist_poly_pt(mfoot, ac), dist_poly_pt(mfoot, ac)))
    near.append(("mound (built footprint)", dist_poly_pt(fp["mound"]["low"], ac), dist_poly_pt(fp["mound"]["all"], ac)))
    low_sorted = sorted([x for x in near if x[1] is not None], key=lambda x: x[1])
    all_sorted = sorted([x for x in near if x[2] is not None], key=lambda x: x[2])
    A["arena"] = {"centre_uv": list(ac), "required_r": arena["r"],
                  "clear_r_walkable_m": r(low_sorted[0][1]), "nearest_walkable": [[x[0], r(x[1])] for x in low_sorted[:6]],
                  "clear_r_any_height_m": r(all_sorted[0][2]), "nearest_any_height": [[x[0], r(x[2])] for x in all_sorted[:6]],
                  "PASS": low_sorted[0][1] >= arena["r"],
                  "_instrument": "least distance from (0, 1) to each built footprint polygon (convex hull of the mesh's vertices under 1.9 m; and of all its vertices)"}
    path = [tuple(p) for p in L["regions"]["path"]["extended_off_frame_uv"]]
    half = L["regions"]["path"]["width_m"] / 2.0
    intr = []
    for pid, f in fp.items():
        if len(f["low"]) < 3:
            continue
        d = dist_poly_poly(f["low"], path, q_closed=False)
        # the butt cap: a footprint "near" the first point but beyond the start does not count
        if d is not None and d < half + 1.0:
            intr.append((pid, d))
    intr.sort(key=lambda x: x[1])
    A["path"] = {"width_m": L["regions"]["path"]["width_m"], "polyline_uv": [list(p) for p in path],
                 "closest": [[x[0], r(x[1]), r(x[1] - half)] for x in intr[:8]],
                 "_columns": "[piece, distance to the centreline m, clearance beyond the 2 m half-width m]",
                 "min_clearance_m": r(intr[0][1] - half) if intr else None,
                 "PASS": (not intr) or intr[0][1] >= half,
                 "_instrument": "least distance from each built footprint (under 1.9 m) to the path's centreline, against the 2 m half-width"}
    g1, g2 = fp["ring_p155"]["low"], fp["ring_m155"]["low"]
    gap = dist_poly_poly(g1, g2)
    A["ring_entrance"] = {"between": ["ring_p155", "ring_m155"], "clear_gap_m": r(gap), "required_m": 6.0,
                          "PASS": gap is not None and gap >= 6.0,
                          "_instrument": "least distance between the two gate stones' built footprints (under 1.9 m)"}

    # 3. walkability ------------------------------------------------------------------------
    wg = rep["walk_grid"]["summary"]
    A["flood_fill"] = {"from_uv": grid["spawn_uv"], "reachable_m2": wg["reachable_m2"], "targets": wg["targets"],
                       "ice_reachable_share": wg["ice_reachable_share"],
                       "reachable_outside_bounds_cells": wg["reachable_outside_bounds"],
                       "PASS": all(wg["targets"][k] for k in ("arena_centre_(0,1)", "ice_centre_(-13,-5)", "before_the_door_(0,7.25)", "in_the_doorway_(0,7.5)"))
                               and wg["reachable_outside_bounds"] == 0,
                       "_instrument": rep["walk_grid"]["instrument"]}
    df = rep["door_floor"]["floor_y_by_v_at_u0"]
    A["mound_and_door"] = {"reachable_cells_inside_the_mound_outside_the_passage": wg["reachable_inside_mound_outside_passage"],
                           "mound_walk_refused": rep.get("walks", {}).get("refused_up_the_mound", {}).get("PASS"),
                           "passage_floor_y_at_the_door_(0,7.5)": df.get("v=7.5"),
                           "floor_y_down_the_passage": df,
                           "PASS": wg["reachable_inside_mound_outside_passage"] == 0 and df.get("v=7.5") is not None and abs(df["v=7.5"]) < 0.005,
                           "_instrument": "flood-fill cells inside the mound ellipse; a scripted walk at the mound; " + rep["door_floor"]["instrument"]}
    if "walks" in rep:
        A["walks"] = {k: {kk: v[kk] for kk in ("from_uv", "to_uv", "reached", "expected_to_reach", "PASS", "end_uv", "end_floor_y", "seconds")}
                      for k, v in rep["walks"].items() if isinstance(v, dict)}
        A["walks"]["_instrument"] = rep["walks"]["_instrument"]
    A["scale"] = marks
    A["scale"]["PASS"] = marks["instrument_proof"]["PASS"] and abs(marks["one_metre_across_px"] - PPM) < 0.5
    A["guide_frame"] = {"px": rep["guide"]["px"], "corners_projected_px": rep["guide"]["window_corners_projected_px"],
                        "_expect": rep["guide"]["_corners_expect"]}
    A["frame_cost_ms"] = rep.get("frame_cost_ms")
    # the EXPORTED app's own number, if it has been run: `<app>/Contents/MacOS/<exe> --fullscreen
    # -- --frame-cost` prints one line; tools/build_app.sh stages the app it was run from
    lg = CAP / "logs" / "app_frame_cost.log"
    if lg.exists():
        import re
        m = re.search(r"frame_cost ms_per_frame=([0-9.]+) fps=([0-9.]+) viewport=(\d+)x(\d+) frames=(\d+)", lg.read_text())
        if m:
            A["frame_cost_ms"] = dict(A["frame_cost_ms"] or {})
            A["frame_cost_ms"]["exported_app_fullscreen"] = {
                "ms_per_frame": float(m.group(1)), "fps": float(m.group(2)),
                "viewport": [int(m.group(3)), int(m.group(4))], "frames": int(m.group(5)),
                "_at": "the staged C-9 Barrow blockout.app, --fullscreen on the 1920x1080 display, vsync off, MSAA 2x (project setting), him walking a loop in the ring",
                "_run": "heavy_lock.py C-9 -- <app>/Contents/MacOS/'C-9 Barrow blockout' --fullscreen -- --frame-cost"}
    return A


def findings(L, built, rep):
    """The things a reviewer should see before any paint, each measured."""
    P = {e["id"]: e for e in L["placements"]}
    R = built["records"]
    fp = footprints(L, built)
    F = {}
    m = P["mound"]
    mfoot = [(m["uv"][0] + m["semi_axes"][0] * math.cos(t), m["uv"][1] + m["semi_axes"][1] * math.sin(t))
             for t in np.linspace(0, 2 * math.pi, 721)[:-1]]
    F["door_vs_arena"] = {"door_uv": P["door_lintel"]["uv"], "door_to_arena_centre_m": r(math.dist(P["door_lintel"]["uv"], L["regions"]["arena"]["centre_uv"])),
                          "posts_to_arena_centre_m": [r(dist_poly_pt(fp["door_post_L"]["low"], tuple(L["regions"]["arena"]["centre_uv"]))),
                                                      r(dist_poly_pt(fp["door_post_R"]["low"], tuple(L["regions"]["arena"]["centre_uv"])))],
                          "mound_foot_to_arena_centre_m": r(dist_poly_pt(mfoot, tuple(L["regions"]["arena"]["centre_uv"])))}
    F["door_height_vs_mound"] = {"lintel_top_y": R["door_lintel"]["y_max"], "posts_top_y": R["door_post_L"]["y_max"],
                                 "mound_peak_y": rep["scene"]["mound"]["peak_y"], "mound_rise_spec_m": m["rise_m"]}
    F["mound_vs_top_edge"] = {"mound_back_foot_v": rep["scene"]["mound"]["back_foot_v"],
                              "guide_top_v": L["frame"]["guide_window"]["v"][1],
                              "short_by_m": r(L["frame"]["guide_window"]["v"][1] - rep["scene"]["mound"]["back_foot_v"])}
    F["plus_minus_40_stones_to_mound_foot"] = {
        "centre_to_foot_m": r(min(math.dist(tuple(P["ring_p40"]["uv"]), q) for q in mfoot)),
        "footprint_to_foot_m": r(dist_poly_poly(fp["ring_p40"]["low"], mfoot)),
        "spec_says": "1.2 m clear of the mound's foot"}
    tc = L["regions"]["ice"]["centre_uv"]
    ta, tb = L["regions"]["ice"]["axes_m"][0] / 2, L["regions"]["ice"]["axes_m"][1] / 2
    on_ice = {}
    for pid, f in fp.items():
        if pid.startswith("shore_rock") or len(f["low"]) < 3:
            continue
        a = poly_in_ellipse_area(f["low"], tc, ta, tb)
        if a > 0.0005:
            on_ice[pid] = r(a, 3)
    F["footprints_standing_on_the_ice_m2"] = on_ice
    F["squeeze_fallen_stone_to_cover_outcrop_m"] = r(dist_poly_poly(fp["ring_m95"]["low"], fp["cover_outcrop"]["low"]))
    # any two pieces whose walkable footprints touch (the "stone overlaps a tree" check)
    ids = [k for k in fp if len(fp[k]["low"]) >= 3 and k != "mound"]
    touch = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if a.startswith("shore_rock") and b.startswith("shore_rock"):
                continue
            if {a, b} <= {"door_lintel", "door_post_L", "door_post_R"}:
                continue
            if (a.startswith("fallen_tree") and b.startswith("fallen_tree")):
                continue
            d = dist_poly_poly(fp[a]["low"], fp[b]["low"])
            if d is not None and d < 0.05:
                touch.append([a, b, r(d)])
    F["pieces_touching_or_overlapping"] = touch
    # gaps too narrow for him (0.70 m) between neighbouring solid pieces inside the bounds
    return F


# --- the map ------------------------------------------------------------------------------------
def font(sz, bold=False):
    for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf"] if bold else []) + \
             ["/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_map(L, built, rep, grid, A):
    top = Image.open(CAP / "topdown.png").convert("RGB")
    T = rep["topdown"]
    ppm = T["px_per_m"]
    W0, H0 = top.size
    ML, MR, MT, MB = 110, 560, 140, 110
    canvas = Image.new("RGB", (W0 + ML + MR, H0 + MT + MB), (246, 244, 239))
    # lighten the render so the overlays read
    base = Image.blend(top, Image.new("RGB", top.size, (255, 255, 255)), 0.28)
    canvas.paste(base, (ML, MT))
    d = ImageDraw.Draw(canvas, "RGBA")

    def px(u, v):
        return (ML + W0 / 2 + u * ppm, MT + H0 / 2 - v * ppm)

    f12, f14, f16, f20, f26, f34 = font(15), font(17), font(19), font(23, True), font(30, True), font(40, True)
    # reachable area's outline (the flood fill)
    rows = grid["rows_from_v0_up"]
    nu, nv, st = grid["nu"], grid["nv"], grid["step"]
    reach = np.array([[c == "o" for c in row] for row in rows], dtype=bool)
    edge = reach & ~(np.roll(reach, 1, 0) & np.roll(reach, -1, 0) & np.roll(reach, 1, 1) & np.roll(reach, -1, 1))
    for j, i in zip(*np.nonzero(edge)):
        u = grid["u0"] + i * st
        v = grid["v0"] + j * st
        x, y = px(u, v)
        d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=(40, 150, 60, 200))
    # 5 m grid
    for g in range(-20, 21, 5):
        x, _ = px(g, 0)
        d.line([x, MT, x, MT + H0], fill=(90, 90, 90, 110 if g else 170), width=1 if g else 2)
        d.text((x, MT - 30), "u %+d" % g if g else "u 0", font=f14, fill=(40, 40, 40), anchor="mm")
        d.text((x, MT + H0 + 22), "%+d" % g if g else "0", font=f14, fill=(40, 40, 40), anchor="mm")
    for g in range(-15, 16, 5):
        _, y = px(0, g)
        d.line([ML, y, ML + W0, y], fill=(90, 90, 90, 110 if g else 170), width=1 if g else 2)
        d.text((ML - 14, y), "v %+d" % g if g else "v 0", font=f14, fill=(40, 40, 40), anchor="rm")
    # the guide window and the 3x3 paint chunks (their GROUND footprints)
    gw = L["frame"]["guide_window"]
    d.rectangle([*px(gw["u"][0], gw["v"][1]), *px(gw["u"][1], gw["v"][0])], outline=(20, 20, 20, 255), width=4)
    chunks = L["frame"]["chunks"]["list"]
    for ch in chunks:
        gu, gv = ch["ground_uv"]["u"], ch["ground_uv"]["v"]
        a = px(gu[0], gv[1])
        b = px(gu[1], gv[0])
        d.rectangle([*a, *b], outline=(225, 120, 20, 230), width=3)
    # overlap bands (256 px of guide = 2.54 m across, 3.19 m up-screen)
    su, sv = 256 / PPM, 256 / PX_UP
    for c in (1, 2):
        u0 = (c * 1280 - 2048) / PPM
        a = px(u0, gw["v"][1])
        b = px(u0 + su, gw["v"][0])
        d.rectangle([*a, *b], fill=(225, 120, 20, 38))
    for rr in (1, 2):
        v1 = (1280 - rr * 768) / PX_UP
        a = px(gw["u"][0], v1)
        b = px(gw["u"][1], v1 - sv)
        d.rectangle([*a, *b], fill=(225, 120, 20, 38))
    for ch in chunks:
        gu, gv = ch["ground_uv"]["u"], ch["ground_uv"]["v"]
        x, y = px((gu[0] + gu[1]) / 2, gv[1])
        d.text((x, y + 16), "chunk %s" % ch["key"], font=f16, fill=(190, 90, 10), anchor="mm")
    # regions
    R = L["regions"]

    def ell(c, a, b, n=180):
        return [px(c[0] + a * math.cos(t), c[1] + b * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n)]
    d.line(ell(R["ring"]["centre_uv"], 9, 9), fill=(120, 120, 130, 200), width=2)
    arena = ell(R["arena"]["centre_uv"], R["arena"]["r"], R["arena"]["r"])
    for i in range(0, len(arena) - 1, 2):
        d.line([arena[i], arena[i + 1]], fill=(30, 70, 220, 255), width=4)
    d.line(ell(R["ice"]["centre_uv"], R["ice"]["axes_m"][0] / 2, R["ice"]["axes_m"][1] / 2), fill=(20, 130, 170, 255), width=3)
    m = [e for e in L["placements"] if e["id"] == "mound"][0]
    d.line(ell(m["uv"], m["semi_axes"][0], m["semi_axes"][1]), fill=(120, 70, 30, 255), width=3)
    pp = R["path"]["extended_off_frame_uv"]
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
    d.line([px(*p) for p in pp], fill=(120, 80, 40, 160), width=1)
    # bounds
    bp = L["bounds"]["polygon_uv"]
    for i in range(len(bp)):
        a, b = bp[i], bp[(i + 1) % len(bp)]
        if i == L["bounds"]["entry_edge_index"]:
            d.line([px(*a), px(*b)], fill=(240, 200, 0, 255), width=6)
        else:
            d.line([px(*a), px(*b)], fill=(210, 25, 25, 255), width=5)
    # pieces: footprints and labels
    fp = footprints(L, built)
    P = {e["id"]: e for e in L["placements"]}
    for pid, f in fp.items():
        e = P.get(pid, {})
        poly = f["low"] if len(f["low"]) >= 3 else f["all"]
        if len(poly) < 3 or pid == "mound":
            continue
        col = (70, 70, 70, 255) if e.get("kind") in ("model", "kit") else (110, 95, 80, 255)
        d.polygon([px(*p) for p in poly], outline=col)
    lab = {}
    for e in L["placements"]:
        pid = e["id"]
        if pid.startswith("ring_"):
            lab[pid] = ("%+d%s" % (e["theta_deg"], {"stone_tall": " T", "stone_mid": " M", "stone_short": " S"}[e["class"]]) +
                        (" fallen" if e.get("tip") else ""))
        elif pid.startswith("outcrop_"):
            lab[pid] = "O%s  %.1f m" % (pid.split("_")[1], e["height_m"])
        elif pid.startswith("cairn_"):
            lab[pid] = "cairn C%s" % pid.split("_")[1]
        elif pid.startswith("grave_marker"):
            lab[pid] = "grave marker"
    for pid, t in lab.items():
        rec = built["records"].get(pid)
        if not rec:
            continue
        if P[pid]["kind"] == "primitive":
            bc = rec["base_centroid_world"]
            u, v = xz_to_uv(bc[0], bc[2])
        else:
            u, v = built_uv(rec)
        x, y = px(u, v)
        dy = -26 if not pid.startswith("outcrop") else 0
        d.text((x, y + dy), t, font=f14, fill=(15, 15, 15), anchor="mm", stroke_width=3, stroke_fill=(255, 255, 255))
    notes = [("cover_outcrop", "cover outcrop 3x2x1.4", 0, 0), ("door_lintel", "DOOR (lintel on 2 posts)", 0, -34),
             ("raven", "raven", 26, -8), ("fallen_tree_log_A", "fallen tree (2 kit logs)", 30, 28)]
    for pid, t, ox, oy in notes:
        rec = built["records"].get(pid)
        if rec:
            if P[pid]["kind"] == "primitive":
                bc = rec["base_centroid_world"]
                u, v = xz_to_uv(bc[0], bc[2])
            else:
                u, v = built_uv(rec)
            x, y = px(u, v)
            d.text((x + ox, y + oy), t, font=f14, fill=(15, 15, 15), anchor="mm", stroke_width=3, stroke_fill=(255, 255, 255))
    for g, (c, n) in {"G1": ((7, -11), 5), "G2": ((-10, 9.5), 4), "G3": ((13, -6), 4), "G4": ((10, 12), 3)}.items():
        x, y = px(*c)
        d.text((x, y - 44), "%s birch grove x%d" % (g, n), font=f14, fill=(20, 80, 30), anchor="mm", stroke_width=3, stroke_fill=(255, 255, 255))
    x, y = px(-19.9, -6.5)
    d.text((x, y), "shore\nrock", font=f14, fill=(80, 60, 40), anchor="mm", stroke_width=3, stroke_fill=(255, 255, 255))
    x, y = px(0, 11.4)
    d.text((x, y), "BARROW MOUND\n12 x 7 m, rise 2.6 m\n(non-walkable)", font=f16, fill=(90, 50, 15), anchor="mm", align="center", stroke_width=3, stroke_fill=(255, 255, 255))
    x, y = px(0, 1)
    d.text((x, y + 34), "him, 1.85 m", font=f14, fill=(120, 20, 20), anchor="mm", stroke_width=3, stroke_fill=(255, 255, 255))
    # the four beats
    for t, (u, v) in (("1  THE APPROACH", (4.2, -14.2)), ("2  THE TARN", (-13, -1.9)), ("3  THE RING", (0, -2.6)),
                      ("4  THE DOOR", (0, 5.9))):
        x, y = px(u, v)
        d.text((x, y), t, font=f26, fill=(20, 20, 60), anchor="mm", stroke_width=4, stroke_fill=(255, 255, 255))
    x, y = px(-3, -16)
    d.text((x, y + 28), "ENTRY (-5...-1, -16)", font=f16, fill=(120, 90, 0), anchor="mm", stroke_width=3, stroke_fill=(255, 255, 255))
    # title
    d.text((ML, 30), "C-9 T10-2 step 1  —  THE FROST KING'S BARROW, FULL AREA: blockout map", font=f34, fill=(15, 15, 15))
    d.text((ML, 82), "Top-down, true metres, (u, v) in the play camera's ground frame: +u screen-right, +v up-screen (away from the camera). "
                     "Origin = arena centre. 5 m grid. Base = the built greybox rendered straight down (48 px/m).", font=f14, fill=(40, 40, 40))
    # legend
    lx = ML + W0 + 34
    ly = MT
    d.text((lx, ly), "LEGEND", font=f20, fill=(15, 15, 15))
    ly += 42
    T2 = L["tints_srgb"]
    for nm, key in (("snow ground", "snow"), ("trodden path", "path"), ("tarn ice (walkable)", "ice"),
                    ("juniper / heather scrub", "shrub"), ("real models, flat grey", "hero_grey"),
                    ("primitives (outcrops, shore rock)", "primitive_grey")):
        c = tuple(int(x * 255) for x in T2[key])
        d.rectangle([lx, ly, lx + 36, ly + 24], fill=c, outline=(60, 60, 60))
        d.text((lx + 48, ly + 12), nm, font=f14, fill=(20, 20, 20), anchor="lm")
        ly += 34
    ly += 10
    for nm, col, w in (("play bounds (invisible walls)", (210, 25, 25), 5), ("entry / exit edge", (240, 200, 0), 6),
                       ("arena r 7 about (0, 1)", (30, 70, 220), 4), ("stone ring r 9 about (0, 2)", (120, 120, 130), 2),
                       ("path band, 4 m", (120, 80, 40), 3), ("tarn ice edge", (20, 130, 170), 3),
                       ("mound foot", (120, 70, 30), 3), ("reachable from the entry (flood fill)", (40, 150, 60), 4),
                       ("guide window 4096 x 2560 px", (20, 20, 20), 4), ("paint chunk (1536 x 1024 px canvas)", (225, 120, 20), 3)):
        d.line([lx, ly + 12, lx + 36, ly + 12], fill=col, width=w)
        d.text((lx + 48, ly + 12), nm, font=f14, fill=(20, 20, 20), anchor="lm")
        ly += 32
    d.rectangle([lx, ly + 4, lx + 36, ly + 24], fill=(225, 120, 20, 60))
    d.text((lx + 48, ly + 14), "chunk overlap band (256 px)", font=f14, fill=(20, 20, 20), anchor="lm")
    ly += 50
    d.text((lx, ly), "Stones: T tall 2.71 m, M mid 2.71 m,\nS short 1.24 m. Carved faces to -v,\nturned 20 deg toward the ring's axis.", font=f14, fill=(30, 30, 30))
    ly += 90
    # acceptance, in one block
    d.text((lx, ly), "MEASURED", font=f20, fill=(15, 15, 15))
    ly += 36
    acc = [
        ("placements <= 0.05 m", A["placements"]["all_spec_points_within_tolerance"], "worst %.3f m" % A["placements"]["worst_delta_m"]),
        ("flood fill: arena, ice, door", A["flood_fill"]["PASS"], "%d cells outside bounds" % A["flood_fill"]["reachable_outside_bounds_cells"]),
        ("mound non-walkable, door y = 0", A["mound_and_door"]["PASS"], "door floor y %s" % A["mound_and_door"]["passage_floor_y_at_the_door_(0,7.5)"]),
        ("arena clear to r 7", A["arena"]["PASS"], "clear to %.2f m" % A["arena"]["clear_r_walkable_m"]),
        ("path clear at 4 m", A["path"]["PASS"], "min %.2f m spare" % (A["path"]["min_clearance_m"] or 99)),
        ("ring entrance >= 6 m", A["ring_entrance"]["PASS"], "%.2f m" % A["ring_entrance"]["clear_gap_m"]),
        ("1 m marker = 100.6 px", A["scale"]["PASS"], "%.2f px (2 m: x%.3f)" % (A["scale"]["one_metre_across_px"], A["scale"]["instrument_proof"]["u_2m_over_u_1m"])),
    ]
    for nm, ok, val in acc:
        d.text((lx, ly), ("PASS  " if ok else "FAIL  ") + nm, font=f14, fill=(20, 110, 40) if ok else (190, 20, 20))
        d.text((lx + 24, ly + 20), val, font=f12, fill=(60, 60, 60))
        ly += 46
    # the measured findings, on the plan where they happen and listed under the numbers
    Fm = findings(L, built, rep)
    red = (200, 20, 20)
    calls = [
        ((1.6, 7.0), "! door posts %.2f m from the arena centre (r 7 asked)" % min(Fm["door_vs_arena"]["posts_to_arena_centre_m"]), "lm"),
        ((0.0, 14.9), "! mound ends %.2f m short of the top edge" % Fm["mound_vs_top_edge"]["short_by_m"], "mm"),
        ((-7.9, -3.9), "! %.2f m2 of this stone on the ice" % Fm["footprints_standing_on_the_ice_m2"].get("ring_m125", 0.0), "rm"),
        ((-5.4, 8.1), "! %.2f m from the mound foot" % Fm["plus_minus_40_stones_to_mound_foot"]["footprint_to_foot_m"], "rm"),
        ((-11.0, 0.15), "gap to the cover outcrop %.2f m (he is 0.70)" % Fm["squeeze_fallen_stone_to_cover_outcrop_m"], "mm"),
    ]
    for (u, v), txt, anc in calls:
        x, y = px(u, v)
        d.text((x, y), txt, font=f14, fill=red, anchor=anc, stroke_width=3, stroke_fill=(255, 255, 255))
    ly += 10
    d.text((lx, ly), "FINDINGS (measured)", font=f20, fill=red)
    ly += 34
    for line in (
        "Door inside the arena disc: posts %.2f m from (0, 1)," % min(Fm["door_vs_arena"]["posts_to_arena_centre_m"]),
        "  mound foot %.2f m. r 7 cannot hold with the door" % Fm["door_vs_arena"]["mound_foot_to_arena_centre_m"],
        "  at (0, 7.5) -- door + mound 1.0 m up gives 7.3.",
        "Door taller than the mound: lintel top %.2f m," % Fm["door_height_vs_mound"]["lintel_top_y"],
        "  mound peak %.2f m; the passage is an open cut." % Fm["door_height_vs_mound"]["mound_peak_y"],
        "Mound ends %.2f m short of the guide's top edge." % Fm["mound_vs_top_edge"]["short_by_m"],
        "+-40 stones %.2f m from the mound foot (spec: 1.2)." % Fm["plus_minus_40_stones_to_mound_foot"]["footprint_to_foot_m"],
        "-125 stone: %.2f m2 of its footprint on the ice." % Fm["footprints_standing_on_the_ice_m2"].get("ring_m125", 0.0),
        "ADDED: scrub band on every bounds edge; shore-rock",
        "  chain on the tarn's W/SW rim; exit wall at the entry.",
    ):
        d.text((lx, ly), line, font=f12, fill=(40, 40, 40))
        ly += 21
    # scale bar
    x0, y0 = px(12.5, -16.9)
    d.line([x0, y0, x0 + 5 * ppm, y0], fill=(0, 0, 0), width=5)
    d.text((x0 + 2.5 * ppm, y0 - 16), "5 m", font=f14, fill=(0, 0, 0), anchor="mm")
    out = CAP / "barrow_full_map.png"
    canvas.save(out, optimize=True)
    return out


# --- paint staging ------------------------------------------------------------------------------
def stage_paint(L):
    PAINT.mkdir(exist_ok=True)
    guide = PAINT / "barrow_full_guide.png"
    shutil.copyfile(CAP / "guide.png", guide)
    im = Image.open(guide)
    assert im.size == (4096, 2560), im.size
    cfg = {
        "prefix": "T10BF",
        "name": "THE FROST KING'S BARROW, full area: paint-over of the gameplay blockout (T10-2 step 2)",
        "guide": str(guide),
        "cols": 3,
        "rows": 3,
        "experiment": "T10-2-barrow-full-paintover",
        "_status": "STAGED BY drax, NOT FIRED. Painting waits for Matt's look at the map and the greybox (spec § 5). The conductor copies this into conductor_scripts/ and the CS9-guides manifest when painting is approved.",
        "_guide_sha256": hashlib.sha256(guide.read_bytes()).hexdigest(),
        "_guide_frame": "4096 x 2560 px = u -20.35..20.35 m, v -15.94..15.94 m at the play camera (orthographic, pitch 52.95354112560294, yaw 47): 100.6176 px per metre across, 80.3076 px per ground metre up-screen",
        "_note_for_the_conductor": "guided_paint.py's retry clause names 'flat pure #00ff00' sky; this guide has NO sky (the whole frame is ground). The barbarian stands in the arena for SCALE only; the rules below ask for him to be painted OUT.",
        "geo": ("IMAGE 1 is not a flat-colour layout: it is a GREYBOX RENDER of a real 3D game level, seen from the game's fixed high "
                "three-quarter ORTHOGRAPHIC camera (53 degrees down), at true scale -- the small painted barbarian in the ring is 1.85 m tall. "
                "Every grey form is a real object that will be modelled at exactly this position and size. LIGHT WARM GREY ground = deep, "
                "smooth snow; the DARKER BROWN-GREY BAND = a trodden path through the snow (footprints, slush, a little bare earth); "
                "PALE BLUE-GREY = the frozen tarn, flat lapis-blue ice with pale cracks and a dusting of snow at its edges; MUTED GREEN-BROWN "
                "PATCHES = low dark juniper scrub and rust-brown winter heather poking through the snow; FLAT GREY upright slabs = carved "
                "standing stones (spiral and knotwork carvings on the faces turned toward the viewer), one of them FALLEN and lying outward; "
                "the two grey posts with a massive beam on top = the barrow's carved stone doorway, with a DARK passage stepping down into "
                "the mound behind it; the low snow-covered DOME = the barrow mound itself, grassy where the snow has blown thin; the DARKER "
                "GREY STEPPED MASSES = weathered layered rock outcrops (and a low rocky shore on the tarn's far side); thin grey trees = dead "
                "wind-bent birches; small grey stacks = stone cairns; the two grey crosses of spears with a round shield = grave markers; "
                "the long grey cylinders = a fallen birch trunk; a tiny grey bird on a stone = a raven."),
        "rules": ("Paint OVER the render: every object keeps EXACTLY its silhouette, position and size (the 3D models are placed from "
                  "this same layout, so anything moved will not match); shadows stay where the render puts them (one low winter sun from "
                  "the upper LEFT, 55 degrees up, short soft blue-violet shadows touching their objects). Paint the barbarian OUT -- "
                  "he is there only for scale; leave open snow where he stands. Keep the ring's centre, the path and the tarn OPEN: no "
                  "new rocks, trees or drifts on them. Small scatter is welcome only inside the scrub patches and at the foot of rocks "
                  "and stones (pebbles, snow drifts banked against objects, frozen grass tufts). One thin warm dark-brown ink line on "
                  "every contour, the SAME weight everywhere. Palette and hand of IMAGE 2 (the approved Frost King's Barrow concept): "
                  "cold blue-white snow, warm grey granite, rust heather, dark juniper, lapis ice; watercolour washes with pen detail. "
                  "No sky, no horizon, no text, UI, border or characters."),
        "refs": [
            [str(B / "runs/C-9/artifacts/T10C-barrow/T10C-barrow_a.png"),
             "the APPROVED Frost King's Barrow concept (Matt's pick): palette, light, snow, stone carving and painted hand ONLY -- NOT its layout"],
        ],
        "chunks": L["frame"]["chunks"]["list"],
    }
    (PAINT / "cfg_barrow_full.json").write_text(json.dumps(cfg, indent=1, ensure_ascii=False))
    return cfg


def previews():
    g = Image.open(CAP / "guide.png").convert("RGB")
    p = g.resize((1024, 640), Image.LANCZOS)
    p.save(CAP / "guide_preview.png", optimize=True)
    q = g.resize((2048, 1280), Image.LANCZOS)
    d = ImageDraw.Draw(q, "RGBA")
    s = 0.5
    for c in range(3):
        for rr in range(3):
            x0, y0 = c * 1280 * s, rr * 768 * s
            d.rectangle([x0, y0, x0 + 1536 * s - 1, y0 + 1024 * s - 1], outline=(235, 120, 20, 255), width=3)
            d.text((x0 + 14, y0 + 10), "chunk %d_%d" % (c, rr), font=font(26, True), fill=(235, 120, 20), stroke_width=3, stroke_fill=(255, 255, 255))
    q.save(CAP / "guide_preview_chunks.png", optimize=True)


def main():
    L, built, rep, grid = load()
    marks = measure_markers(rep)
    A = acceptance(L, built, rep, grid, marks)
    F = findings(L, built, rep)
    # merge the built numbers into the layout (the deliverable)
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
    L["acceptance"] = A
    L["findings_measured"] = F
    L["built_from"] = {"scene": "runs/C-9/barrow_full/godot/scenes/barrow_full.tscn",
                       "capture": "godot/tools/capture_blockout.gd -> captures/",
                       "_": "'built' in each placement is measured off the scene, not copied from the design",
                       "sandbox_copies_frozen_at": {
                           "commit": "634316024",
                           "files": ["scripts/knight.gd", "scripts/gear.gd", "scripts/paint_stack.gd", "scripts/world.gd",
                                     "data/character.json", "data/gear_manifest.json"],
                           "from": "runs/C-9/cliffside3d/godot/ at that commit, byte-identical, unmodified",
                           "since_then_upstream": ["f2140e680 the chop/attack glitch fix (knight.gd)",
                                                   "b90943fbe T10-1b snow and density pass (paint_stack.gd)"],
                           "_": "the brief: 'Don't modify your copies'; the attacks may look wrong here, and that is expected"}}
    (ROOT / "barrow_full_layout.json").write_text(json.dumps(L, indent=1))
    (CAP / "acceptance.json").write_text(json.dumps({"acceptance": A, "findings": F}, indent=1))
    mp = draw_map(L, built, rep, grid, A)
    previews()
    cfg = stage_paint(L)
    summary = {
        "placements_all_within_0.05": A["placements"]["all_spec_points_within_tolerance"],
        "placements_worst_m": A["placements"]["worst_delta_m"],
        "flood_fill": {"PASS": A["flood_fill"]["PASS"], "targets": A["flood_fill"]["targets"],
                       "outside_bounds": A["flood_fill"]["reachable_outside_bounds_cells"]},
        "mound_door": {"PASS": A["mound_and_door"]["PASS"], "door_y": A["mound_and_door"]["passage_floor_y_at_the_door_(0,7.5)"],
                       "mound_cells": A["mound_and_door"]["reachable_cells_inside_the_mound_outside_the_passage"]},
        "arena_clear_r": A["arena"]["clear_r_walkable_m"], "arena_nearest": A["arena"]["nearest_walkable"][:3],
        "path_min_spare_m": A["path"]["min_clearance_m"], "path_closest": A["path"]["closest"][:3],
        "ring_entrance_m": A["ring_entrance"]["clear_gap_m"],
        "marker_1m_px": A["scale"]["one_metre_across_px"], "marker_proof": A["scale"]["instrument_proof"],
        "frame_cost": A["frame_cost_ms"],
        "walks": {k: v.get("PASS") for k, v in A.get("walks", {}).items() if isinstance(v, dict)},
        "findings": F,
        "map": str(mp), "cfg": str(PAINT / "cfg_barrow_full.json"),
    }
    print(json.dumps(summary, indent=1))
    if "--stage" in sys.argv:
        STAGE.mkdir(parents=True, exist_ok=True)
        for src, dst in ((CAP / "barrow_full_map.png", "1 - top-down map (5 m grid, 3x3 paint chunks).png"),
                         (CAP / "guide.png", "2 - the guide, 4096x2560 (play camera, true scale).png"),
                         (CAP / "guide_preview.png", "2a - the guide, preview 1024x640.png"),
                         (CAP / "guide_preview_chunks.png", "2b - the guide, preview with the 3x3 chunk grid.png"),
                         (CAP / "still_ring.png", "3 - play screen, the ring arena.png"),
                         (CAP / "still_tarn.png", "4 - play screen, the tarn.png"),
                         (CAP / "acceptance.json", "measurements - acceptance.json")):
            shutil.copyfile(src, STAGE / dst)
        print("== staged ->", STAGE)


if __name__ == "__main__":
    main()
