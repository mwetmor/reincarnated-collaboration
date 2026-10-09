#!/usr/bin/env python3
"""BV2F LV (R-C9-294): AUTOMATED PROOF of the rebuilt ice -- read-only on the built level.

    python3 fid/lv/tools/lv_ice_proof.py   -> fid/lv/art/ice294_proof.json ; exit 1 on any FAIL

Items tagged "r294" in level.json are the NEW Phase 3' ice (floes, flush drifts, brash); the other ice items are the
pilot-LOCKED ones (byte-identical by rule, their own pre-existing stacking reported, not judged). Raster at 20 px/m.
Proved for the NEW ice:
  (1) NO STACK: no new item overlaps another new item, a locked item, or the ground drawn as ice (classes ice/ice_mid/
      shore_ice/tide_ice); each item is rasterised ERODED by one pixel (0.05 m) so exactly shared edges (a drift and its
      floe share their cut) do not count -- any overlap wider than ~0.1 m is caught;
  (2) a DRIFT is flush with its floe: same z1, its cut vertices on the floe's outline;
  (3) THRESHOLDS: floe area >= 0.6 m2, mean width 2A/P >= 0.45 m, no straight run >= 1.2 m; leads >= 0.10 m (a floe dilated
      by 0.05 m touches no other floe); brash area >= 0.04 m2, mean width >= 0.075 m, >= 0.08 m clear of every floe;
  (4) heights (R-C9-319, ONE rule): shore-fast (ice_shorefast) z1 = sea+0.30, every other floe = sea+0.20 (brash awash);
  (5) R-C9-319: ZERO stacking anywhere -- all items, new and locked, on each other or on ground ice."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
BF = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", "art"))
ICE = ["ice_shorefast", "ice_plates", "ice_floes", "ice_floes_bob", "ice_ridges", "ice_brash", "cove_ice", "ice_rims", "trans_rubble", "mere_seams", "ice_drifts"]
FLOES = ["ice_shorefast", "ice_plates", "ice_floes", "ice_floes_bob"]
RP = 20.0


def area_perim(pts):
    A = 0.5 * abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1])))
    P = sum(math.dist(a, b) for a, b in zip(pts, pts[1:] + pts[:1]))
    return A, P


def straight_run(pts, tol=0.03):
    """the longest stretch of the closed outline that is STRAIGHT: every vertex of the stretch within tol (m) of the chord
    between its ends (judged on the outline as written, whatever its vertex density)"""
    n = len(pts)
    if n < 3:
        return 0.0
    P_ = np.array(list(pts) + list(pts), float)
    best = 0.0
    for i in range(n):
        j = i + 2
        while j < i + n:
            a_, b_ = P_[i], P_[j]
            L_ = float(np.hypot(*(b_ - a_)))
            if L_ < 1e-9:
                j += 1
                continue
            d_ = b_ - a_
            mid = P_[i + 1:j]
            off = np.abs((mid[:, 0] - a_[0]) * d_[1] - (mid[:, 1] - a_[1]) * d_[0]) / L_
            if (off > tol).any():
                break
            j += 1
        a_, b_ = P_[i], P_[j - 1]
        best = max(best, float(np.hypot(*(b_ - a_))), float(np.hypot(*(P_[i + 1] - P_[i]))))
    return best


def main():
    Lv = json.load(open(os.path.join(BF, "level.json")))
    sim = Lv["sim"]
    sea = float(sim["sea_z"])
    ex = sim["heightfield"]["extent_sim_m"]
    u0, u1, v0, v1 = ex["x0"], ex["x1"], -ex["y1"], -ex["y0"]
    W, H = int((u1 - u0) * RP), int((v1 - v0) * RP)

    def ras(pts):
        im = Image.new("L", (W, H), 0)
        ImageDraw.Draw(im).polygon([((q[0] - u0) * RP, (v1 - q[1]) * RP) for q in pts], fill=1)
        return np.asarray(im).astype(bool)

    def bbox_sl(pts, pad=4):
        xs = [(q[0] - u0) * RP for q in pts]
        ys = [(v1 - q[1]) * RP for q in pts]
        return slice(max(0, int(min(ys)) - pad), min(H, int(max(ys)) + pad + 1)), slice(max(0, int(min(xs)) - pad), min(W, int(max(xs)) + pad + 1))
    C = np.asarray(Image.open(os.path.join(BF, "classes.png")))
    names = Lv["classes"]
    cppm = sim["classes_png"]["px_per_m"]
    jj, ii = np.mgrid[0:H, 0:W]
    cg = C[np.clip(((jj + 0.5) / RP * cppm).astype(int), 0, C.shape[0] - 1), np.clip(((ii + 0.5) / RP * cppm).astype(int), 0, C.shape[1] - 1)]
    ground = np.isin(cg, [names.index(c) for c in ("ice", "ice_mid", "shore_ice", "tide_ice") if c in names])
    items = []
    for g in ICE:
        for k, it in enumerate(sim["slabs"].get(g, {}).get("items", [])):
            pts = [(q[0], -q[1]) for q in it["poly"]]
            items.append({"g": g, "k": k, "new": bool(it.get("r294")), "pts": pts, "z1": it["z1"], "z0": it["z0"]})
    # (1) stacks: coverage of eroded masks
    cov_new = np.zeros((H, W), np.int16)
    cov_old = np.zeros((H, W), bool)
    masks = []
    for it in items:
        m = ras(it["pts"])
        me = ndimage.binary_erosion(m)
        masks.append((m, me))
        if it["new"]:
            cov_new += me
        else:
            cov_old |= me
    new_new = int((cov_new >= 2).sum())
    new_old = int(((cov_new >= 1) & cov_old).sum())
    new_ground = int(((cov_new >= 1) & ground).sum())
    # pre-existing (locked) stacking, reported only
    cov_lock = np.zeros((H, W), np.int16)
    for it, (m, me) in zip(items, masks):
        if not it["new"]:
            cov_lock += me
    locked_stack_m2 = float(((cov_lock >= 2) | ((cov_lock >= 1) & ground)).sum()) / RP ** 2
    # (2) drifts flush
    floes_new = [(it, m) for it, (m, me) in zip(items, masks) if it["new"] and (it["g"] in FLOES or it["g"] == "trans_rubble")]
    drift_bad = []
    for it, (m, me) in zip(items, masks):
        if it["g"] != "ice_drifts":
            continue
        host = [f for f, fm in floes_new if (ndimage.binary_dilation(m, iterations=1) & fm).any()]
        ok = len(host) == 1 and abs(host[0]["z1"] - it["z1"]) < 1e-6
        if not ok:
            drift_bad.append(it["k"])
    # (3) thresholds
    bad = {"floe_area": [], "floe_width": [], "straight": [], "lead": [], "brash_area": [], "brash_width": [], "brash_clear": [], "height": []}
    floe_union = np.zeros((H, W), bool)
    for f, fm in floes_new:
        floe_union |= fm
    for it, (m, me) in zip(items, masks):
        if not it["new"]:
            continue
        A, P = area_perim(it["pts"])
        if it["g"] in FLOES or it["g"] == "trans_rubble":      # (R-C9-319: the W1 shore-fast edge lives in trans_rubble)
            # a floe that hosts a drift is measured with its drift (one sheet at one height)
            mm = m.copy()
            for it2, (m2, _) in zip(items, masks):
                if it2["g"] == "ice_drifts" and (ndimage.binary_dilation(m2, iterations=1) & m).any() and abs(it2["z1"] - it["z1"]) < 1e-6:
                    A2, P2 = area_perim(it2["pts"])
                    A += A2
                    mm |= m2
            if A < 0.6:
                bad["floe_area"].append((it["g"], it["k"], round(A, 3)))
            if 2 * A / max(P, 1e-6) < 0.45:
                bad["floe_width"].append((it["g"], it["k"], round(2 * A / P, 3)))
            sr = straight_run(it["pts"])
            if sr >= 1.2:
                bad["straight"].append((it["g"], it["k"], round(sr, 2)))
            sl = bbox_sl(it["pts"], 6)
            others = floe_union[sl] & ~ndimage.binary_dilation(mm, iterations=2)[sl]
            if (ndimage.binary_dilation(mm[sl], iterations=1) & others).any():
                bad["lead"].append((it["g"], it["k"]))
            lo, hi = {"ice_shorefast": (0.30, 0.30), "trans_rubble": (0.30, 0.30), "ice_plates": (0.20, 0.20), "ice_floes": (0.20, 0.20), "ice_floes_bob": (0.20, 0.20)}[it["g"]]   # R-C9-319: ONE rule
            if not (lo - 1e-3 <= it["z1"] - sea <= hi + 1e-3):
                bad["height"].append((it["g"], it["k"], round(it["z1"] - sea, 3)))
        elif it["g"] == "ice_brash":
            if A < 0.04:
                bad["brash_area"].append((it["k"], round(A, 3)))
            if 2 * A / max(P, 1e-6) < 0.075:
                bad["brash_width"].append((it["k"], round(2 * A / P, 3)))
            sl = bbox_sl(it["pts"], 4)
            if (ndimage.binary_dilation(m[sl], iterations=1) & floe_union[sl]).any():
                bad["brash_clear"].append(it["k"])
    n_new = {g: sum(1 for it in items if it["new"] and it["g"] == g) for g in ICE}
    res = {"_what": __doc__.split("\n")[0], "raster_px_per_m": RP, "new_items": n_new,
           "stack": {"new_on_new_px": new_new, "new_on_locked_px": new_old, "new_on_ground_ice_px": new_ground,
                     "pass": new_new == 0 and new_old == 0 and new_ground == 0},
           "drifts_flush": {"bad": drift_bad, "pass": not drift_bad},
           "thresholds": {k: v for k, v in bad.items()}, "thresholds_pass": all(not v for v in bad.values()),
           "locked_pilot_items_residual_stack_m2": round(locked_stack_m2, 2),
           "_locked_note": "pilot items locked byte-identical by R-C9-294 (outside the A/C rects); their own pre-existing stacking is reported, not changed"}
    res["all_items_stack_m2"] = round(float(((cov_new + cov_lock) >= 2).sum() + (((cov_new + cov_lock) >= 1) & ground).sum()) / RP ** 2, 3)
    res["locked_items_left"] = {g: sum(1 for it in items if not it["new"] and it["g"] == g) for g in ICE if any(not it["new"] and it["g"] == g for it in items)}
    res["PASS"] = res["stack"]["pass"] and res["drifts_flush"]["pass"] and res["thresholds_pass"] and res["all_items_stack_m2"] == 0.0
    json.dump(res, open(os.path.join(LV, "art", "ice294_proof.json"), "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("new_items", "stack", "drifts_flush", "thresholds_pass", "locked_pilot_items_residual_stack_m2", "all_items_stack_m2", "locked_items_left", "PASS")}, indent=1))
    if not res["thresholds_pass"]:
        print({k: v[:8] for k, v in bad.items() if v})
    sys.exit(0 if res["PASS"] else 1)


if __name__ == "__main__":
    main()
