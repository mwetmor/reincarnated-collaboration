#!/usr/bin/env python3
"""P6 -- GEOMETRY AGREEMENT between the painting and the geometry of record.

(a) INVENTION CHECK (negative control, Gate-1 W-1: R-C9-155's BVP re-test-2 blocks, artifacts/BVR-*: "two large open
    doors again (the painter invents structures per chunk)"). A DARK OPENING is a connected region where the
    painting's Lab L*, smoothed by a Gaussian of 0.1 m (sigma = 0.1 x px/m: a door interior is textured -- planks,
    smoke, embers -- and an opening is perceived at the region's tone, not its pixels), is below T, after an opening
    by a 0.2 m square (removes ink lines, beams, single stems), with area >= 0.5 m^2 at the plate's px/m.
    T = v1's OWN CEILING: the largest integer L* at which v1's painting shows no opening other than its declared
    one(s) (barrow_full_layout.json: the door_lintel slot at uv (0, 10.6)) -- swept 16..40, computed, not chosen.
    Every detected opening must lie within (max(w,h)/2 + 1.5 m) of a DECLARED opening (layout_v2.json models[].opening,
    projected by the plate's frame law); the rest are INVENTIONS. PASS: inventions = 0.
    Phase-1 use (W-7): the declared openings come from layout_v2's polygons/slots, never from the guide's class map.
(b) SILHOUETTE IoU -- per static model, its ID/render silhouette vs the painting's NON-GROUND class at the same pixels
    (non-ground = Lab L* < 80 or chroma > 18 after a 0.05 m smoothing: painted rock, wood, stone, ink -- snow and pale
    ice are ground). PASS: median IoU over pieces >= v1's median (plan § 4 P6). v1 pieces from take/ids/ids.png; R-C9-159
    pieces from the PH render masks (renders/v159: render vs hide_<group>), the painting being 159's ground painting.
CONSTRUCTED FAILURES: (a) a 2.2 x 2.6 m dark doorway (L* 12, v1's own door colour) stamped onto v1's painting on
    open snow 6 m left of the ring; (b) v1's ID silhouettes shifted 1.5 m (151 px) right against the painting.
"""
import argparse
import glob
import math
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

V1_PPM = PPM_V1


def lstar(img):
    return rgb_to_lab(img)[..., 0]


def openings(img, ppm, T):
    L = ndimage.gaussian_filter(lstar(img), 0.1 * ppm)
    k = max(1, int(round(0.2 * ppm)))
    m = ndimage.binary_opening(L < T, structure=np.ones((k, k)))
    lab, n = ndimage.label(m)
    if n == 0:
        return []
    sz = ndimage.sum(m, lab, range(1, n + 1))
    com = ndimage.center_of_mass(m, lab, range(1, n + 1))
    return [{"xy": (float(c[1]), float(c[0])), "area_m2": float(s) / ppm ** 2}
            for s, c in zip(sz, com) if s >= 0.5 * ppm ** 2]


def match(found, declared, ppm):
    inv = []
    for f in found:
        ok = False
        for d in declared:
            r = (max(d["w"], d["h"]) / 2 + 1.5) * ppm
            if math.hypot(f["xy"][0] - d["xy"][0], f["xy"][1] - d["xy"][1]) <= r:
                ok = True
        if not ok:
            inv.append(f)
    return inv


# ---- v1 ---------------------------------------------------------------------------------------------------------
def v1_frame():
    gw = jload(BF / "barrow_full_layout.json")["frame"]["guide_window"]
    return gw["u"][0], gw["v"][1]


def v1_px(u, v, h=0.0):
    u0, v1 = v1_frame()
    return (u - u0) * V1_PPM, (v1 - v) * 80.3076 - h * 60.6183


def v1_declared():
    # the barrow door: lintel slot at uv (0, 10.6); the door is ~1.8 m wide x 2.2 m high (posts 0.9 m off centre)
    x, y = v1_px(0.0, 10.6, 1.1)
    return [{"id": "barrow door (door_lintel slot)", "xy": (x, y), "w": 1.8, "h": 2.2}]


def v1_painting(scale=1.0):
    return load_rgb(BF / "paint/barrow_full_painted.png", scale)


def v1_ceiling(img, ppm, declared):
    T_ok = None
    sweep = {}
    for T in range(16, 41):
        inv = match(openings(img, ppm, T), declared, ppm)
        sweep[T] = len(inv)
        if not inv:
            T_ok = T
        else:
            break
    return T_ok, sweep


# ---- BVR (R-C9-155 re-test-2) -------------------------------------------------------------------------------------
def bvp_frame():
    return jload(B2 / "paint/frame_bvp.json")


def bvp_declared(layout=None):
    """declared openings, projected by the BVP plate law. layout_v2 v6 (models[].opening, the Phase-1 source) or,
    for the R-C9-155 calibration, the layout THE BVR BLOCKS WERE PAINTED FROM: v5, git b267b9b00 (committed
    2026-10-03 08:44 -0400; BVR-* delivered 08:52), copied read-only to ph/inputs/ (features[].opening, centre =
    footprint centroid, z = z_bottom + clear_h / 2)."""
    f = bvp_frame()
    P, (X0, Y0), a = f["px_per_m"], f["origin_px"], math.radians(f["pitch_deg"])
    L = jload(layout or (B2 / "layout_v2.json"))
    out = []
    for ft in L.get("features", []):
        op = ft.get("opening")
        if not op or "footprint" not in ft or "clear_w_m" not in op:
            continue
        x, y = np.mean(np.array(ft["footprint"], float), axis=0)
        z = float(ft.get("z_bottom_m", 0.0)) + op["clear_h_m"] / 2
        out.append({"id": ft["id"], "xy": (P * x + X0, P * math.sin(a) * y - P * math.cos(a) * z + Y0),
                    "w": op["clear_w_m"], "h": op["clear_h_m"]})
    for m in L.get("models", []):
        op = m.get("opening")
        if not op:
            continue
        ops = op.get("openings", [op])
        for o in ops:
            if "centre" not in o:
                continue
            x, y = o["centre"]
            z = float(o.get("z_bottom_m", m.get("z", 0.0))) + o["h"] / 2
            out.append({"id": "%s/%s" % (m["id"], o.get("id", o.get("kind", "opening"))),
                        "xy": (P * x + X0, P * math.sin(a) * y - P * math.cos(a) * z + Y0), "w": o["w"], "h": o["h"]})
    return out


def bvr_block(keys, prefix="BVR"):
    f = bvp_frame()
    ch = {c["key"]: c for c in f["chunks"]}
    rs = [ch[k]["px"] for k in keys]
    x0, y0 = min(r[0] for r in rs), min(r[1] for r in rs)
    x1, y1 = max(r[2] for r in rs), max(r[3] for r in rs)
    o = Image.new("RGB", (x1 - x0, y1 - y0))
    for k in keys:
        o.paste(Image.open(ART / ("%s-%s/%s-%s.png" % (prefix, k, prefix, k))).convert("RGB"), (ch[k]["px"][0] - x0, ch[k]["px"][1] - y0))
    return np.asarray(o, np.float32), (x0, y0)


BLOCKS = {"BVR hall (T2a, 7_5..8_7)": ["7_5", "8_5", "7_6", "8_6", "7_7", "8_7"],
          "BVR barrow door (T2b, 4_0..6_1)": ["4_0", "5_0", "6_0", "4_1", "5_1", "6_1"]}

SC = 0.25          # measured at quarter scale (ppm / 4) everywhere: the thresholds are in metres, not pixels


def invention_rows(T):
    ppm = V1_PPM * SC
    rows = {}
    v1 = v1_painting(SC)
    dec = [dict(d, xy=(d["xy"][0] * SC, d["xy"][1] * SC)) for d in v1_declared()]
    f = openings(v1, ppm, T)
    rows["v1"] = {"found": len(f), "inventions": len(match(f, dec, ppm)), "declared": [d["id"] for d in dec]}
    # constructed: a dark doorway on open snow, v1's own door tone
    c = v1.copy()
    x, y = v1_px(-6.0, 1.0, 1.3)
    w, h = 2.2 * ppm, 2.6 * 60.6183 * SC
    c[int(y * SC - h / 2):int(y * SC + h / 2), int(x * SC - w / 2):int(x * SC + w / 2)] = np.array([30, 27, 25], np.float32)
    f = openings(c, ppm, T)
    rows["constructed"] = {"found": len(f), "inventions": len(match(f, dec, ppm)),
                           "stamp": "2.2 x 2.6 m doorway RGB (30,27,25) at uv (-6, 1)"}
    decl = bvp_declared(PH / "inputs/layout_v2_at_b267b9b00_v5.json")
    for name, keys in BLOCKS.items():
        img, (x0, y0) = bvr_block(keys)
        im = np.asarray(Image.fromarray(img.astype(np.uint8)).resize((int(img.shape[1] * SC), int(img.shape[0] * SC)), Image.BOX), np.float32)
        d2 = [dict(d, xy=((d["xy"][0] - x0) * SC, (d["xy"][1] - y0) * SC)) for d in decl]
        d2 = [d for d in d2 if -200 <= d["xy"][0] <= im.shape[1] + 200 and -200 <= d["xy"][1] <= im.shape[0] + 200]
        f = openings(im, ppm, T)
        inv = match(f, d2, ppm)
        rows[name] = {"found": len(f), "inventions": len(inv), "declared_in_block": [d["id"] for d in d2],
                      "inventions_xy_plate_px": [(round(i["xy"][0] / SC + x0), round(i["xy"][1] / SC + y0), round(i["area_m2"], 1)) for i in inv]}
    return rows


# ---- (b) silhouette IoU -------------------------------------------------------------------------------------------
def nonground(img, ppm):
    lab = rgb_to_lab(ndimage.gaussian_filter(img, (0.05 * ppm, 0.05 * ppm, 0)))
    ch = np.hypot(lab[..., 1], lab[..., 2])
    return (lab[..., 0] < 80) | (ch > 18)


def iou_v1(shift_px=0):
    meta = jload(BF / "take/ids/ids.json")["placements"]
    idm = np.asarray(Image.open(BF / "take/ids/ids.png").convert("RGB")).astype(np.int32)
    paint = v1_painting()
    ng = nonground(paint, V1_PPM)
    if shift_px:
        idm = np.roll(idm, shift_px, axis=1)
    out = {}
    for k, m in meta.items():
        if m.get("class") in (None, "birch", "ground"):
            continue
        col = np.array(m["rgb"])
        sil = np.abs(idm - col).sum(-1) < 12
        if sil.sum() < 400:
            continue
        ys, xs = np.where(sil)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        pad = 20
        y0, x0 = max(y0 - pad, 0), max(x0 - pad, 0)
        bb_ng = ng[y0:y1 + pad, x0:x1 + pad]
        bb_s = sil[y0:y1 + pad, x0:x1 + pad]
        out[m.get("id", k)] = round(float((bb_ng & bb_s).sum() / max((bb_ng | bb_s).sum(), 1)), 3)
    return out


def iou_render(rdir, painting_path):
    """pieces = connected components of P3's R-C9-159 model-family silhouettes (p3_residual.v159_rows: |render -
    hide_<group>| less the animated sea); IoU vs the painting's non-ground class inside each piece's padded bbox
    (the v1 rule). Components under v1's 400 px piece floor (at 159's own px/m) are skipped, as in v1."""
    import p3_residual as P3
    rdir = pathlib.Path(rdir)
    paint = load_rgb(painting_path)
    ppm = float(jload(rdir / "ph_capture.json")["frame"]["ppm"])
    ng = nonground(paint, ppm)
    _, M = P3.v159_rows(rdir)
    out = {}
    for fam, m in M.items():
        if fam.startswith("ground"):
            continue
        lab, n = ndimage.label(m)
        for i, sl in enumerate(ndimage.find_objects(lab)):
            piece = lab[sl] == i + 1
            if piece.sum() < 400 * (ppm / V1_PPM) ** 2:
                continue
            y0, y1 = max(sl[0].start - 20, 0), sl[0].stop + 20
            x0, x1 = max(sl[1].start - 20, 0), sl[1].stop + 20
            bb_s = lab[y0:y1, x0:x1] == i + 1
            bb_ng = ng[y0:y1, x0:x1]
            out["%s#%d" % (fam.split(" (")[0], i)] = round(float((bb_ng & bb_s).sum() / max((bb_ng | bb_s).sum(), 1)), 3)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="all", choices=["all", "invention", "iou"])
    a = ap.parse_args()
    res = {}
    if a.part in ("all", "invention"):
        ppm = V1_PPM * SC
        dec = [dict(d, xy=(d["xy"][0] * SC, d["xy"][1] * SC)) for d in v1_declared()]
        T, sweep = v1_ceiling(v1_painting(SC), ppm, dec)
        rows = invention_rows(T)
        res["invention"] = {"T_v1_ceiling": T, "sweep_v1_inventions_by_T": sweep, "rows": rows}
        for k, r in rows.items():
            print("P6a %-34s openings %2d  inventions %2d  -> %s" % (k, r["found"], r["inventions"], "PASS" if r["inventions"] == 0 else "FAIL"))
        print("     T (v1 ceiling) = %s" % T)
    if a.part in ("all", "iou"):
        v1 = iou_v1()
        bar = float(np.median(list(v1.values())))
        rows = {"v1": v1, "constructed": iou_v1(shift_px=151)}
        r159 = PH / "renders/v159"
        if (r159 / "render.png").exists():
            rows["159"] = iou_render(r159, BF / "godot/data/barrow_v2_sw/painted/ground.png")
        res["iou"] = {"bar_v1_median": round(bar, 3), "rows": {k: {"median": round(float(np.median(list(v.values()))), 3),
                                                                     "n": len(v), "pieces": v} for k, v in rows.items()}}
        for k, v in res["iou"]["rows"].items():
            print("P6b %-12s median IoU %.3f over %d pieces (bar %.3f)  -> %s" % (k, v["median"], v["n"], bar,
                                                                               "PASS" if v["median"] >= bar else "FAIL"))
    old = jload(PH / "results/p6.json") if (PH / "results/p6.json").exists() else {}
    old.update(res)
    dump(old, str(PH / "results/p6.json"))
