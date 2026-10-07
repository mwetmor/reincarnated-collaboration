#!/usr/bin/env python3
"""BV2F lane PT, Phase 2' (R-C9-191): THE TAKE of the pilot -- cut by GEOMETRY from the ID render, never by colour.

v1's take (fid/v1tools/tierB/barrow_full/tools/take_from_paint.py) is wired to v1's layout schema (HERO_CLASSES by v1 class
name, v1's ground = ID 0, v1's path/ice regions for (c)). This front end runs v1's OWN algorithms on the pilot -- copied
verbatim, each block cited to its v1 line -- with exactly these stated adaptations:
  * frame  = the pilot plate (u0 -33.5757, v1 22.3699, 4096 x 2560 at v1's 100.6176 px/m, pitch 52.95354, yaw 47);
  * heroes = every REAL MODEL the pilot shows (the ids pt_export_meshes.gd exported: LV's placed GLBs), not v1's class list;
  * ground = the bv2art ground classes the ID render registers as pieces; v1's tuft pool (ground = ID 0) becomes the
             LAND ground ids (snow, shrub, path, mound) -- v1 had no sea, shingle or shore ice for a tuft to fall on;
  * (c) v1's ground-layout section is not run: the pilot's ground classes ARE the guide's class map (fid/lv/guide_art).
Outputs (root = fid/pt/pilot/root, the BF-like root v1's hero_surface.py / t5_06b_bake.py run against via v1run.py):
  take/plates/<id>.png + plates.json (v1 (a): alpha 255 piece / 160 the 3 px ring / 0; the t5_06b cell per plate)
  take/masks/density_uv.png + tufts.json (v1 (b): rust heather + dark shrub, 10 px/m density at the 0.15 m half-height)
  take/take_report.json
    python3 fid/pt/tools/bv2f_take.py [--config CFG.json]
CONFIG (DEV-17, R-C9-192): every input and the frame come from a config; the default is the pilot's
(fid/pt/pilot/fe_take.json). fid/pt/dev17/fe_take_v1.json runs the SAME code on v1's own barrow_full data (the proof).
"""
import hashlib, json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_a = sys.argv[1:]
CFG = json.load(open(_a[_a.index("--config") + 1] if "--config" in _a else os.path.join(FID, "pt", "pilot", "fe_take.json")))
_P = lambda k: os.path.join(FID, CFG[k]) if not os.path.isabs(CFG[k]) else CFG[k]
PAINTING = _P("painting")
IDS_DIR = _P("ids_dir")
OUT = _P("out")
MESHES = _P("meshes_dir") if CFG.get("meshes_dir") else None
HEROES = CFG["heroes"]                     # {"ids_file": ...} or {"classes": [...]} (v1: HERO_CLASSES)
LAND = CFG["land"]                         # {"ids": [...]} or {"id0": true} (v1: ground = ID 0)
GROW_EXTRA = CFG.get("grow_extra_classes", [])   # v1: the birches (take_from_paint.py:137)

# ---- the camera: v1's own constants and formulas (take_from_paint.py:46-64), on the pilot frame
U0, V1 = float(CFG["frame"]["u0"]), float(CFG["frame"]["v1"])
PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
YAW = math.radians(47.0)
W_PX, H_PX = int(CFG["frame"]["px"][0]), int(CFG["frame"]["px"][1])
PXU = PPM
PXV = PPM * math.sin(PITCH)
PXH = PPM * math.cos(PITCH)
U1, V0 = U0 + W_PX / PXU, V1 - H_PX / PXV
# v1 writes its layout's rounded literals (barrow_full_layout.json guide_window); a config may carry them (DEV-17 proof)
U1 = float(CFG["frame"].get("u1", U1))
V0 = float(CFG["frame"].get("v0", V0))
U_HAT = np.array([math.cos(YAW), 0.0, -math.sin(YAW)])
V_HAT = np.array([-math.sin(YAW), 0.0, -math.cos(YAW)])
Y_HAT = np.array([0.0, 1.0, 0.0])
SCREEN_RIGHT = U_HAT
SCREEN_UP = math.sin(PITCH) * V_HAT + math.cos(PITCH) * Y_HAT
TO_CAMERA = -math.cos(PITCH) * V_HAT + math.sin(PITCH) * Y_HAT
TUFT_HALF_H_M = 0.15


def s2l(x):  # take_from_paint.py:70
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def l2s(x):  # take_from_paint.py:74
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def uv_of_px(x, y, h=0.0):  # take_from_paint.py:79
    return U0 + (x + 0.5) / PXU, V1 - (y + 0.5 + h * PXH) / PXV


def px_of_world(p):  # take_from_paint.py:84
    u, v, h = p @ U_HAT, p @ V_HAT, p[..., 1]
    return np.stack([(u - U0) * PXU, (V1 - v) * PXV - h * PXH], -1)


def world_of_uv(u, v, h=0.0):  # take_from_paint.py:90
    return u * U_HAT + v * V_HAT + h * Y_HAT


def main():
    os.makedirs(OUT, exist_ok=True)
    sha = hashlib.sha256(open(PAINTING, "rb").read()).hexdigest()
    P8 = np.asarray(Image.open(PAINTING).convert("RGB"))
    H, W = P8.shape[:2]
    assert (W, H) == (W_PX, H_PX), (W, H)
    IDS = json.load(open(os.path.join(IDS_DIR, "ids.json")))
    # the ID code, v1's (take_from_paint.py:101-105)
    ID8 = np.asarray(Image.open(os.path.join(IDS_DIR, "ids.png")).convert("RGB")).astype(np.int32)
    is_pl = ID8[..., 2] > 100
    ri = np.clip(np.round((ID8[..., 0] - 8) / 16.0), 0, 15).astype(np.int32)
    gi = np.clip(np.round((ID8[..., 1] - 8) / 16.0), 0, 15).astype(np.int32)
    idx = np.where(is_pl, gi * 16 + ri, 0)
    by_idx = {int(k): v for k, v in IDS["placements"].items()}
    idx_of = {v["id"]: k for k, v in by_idx.items()}
    if "ids_file" in HEROES:
        REAL = [l.strip() for l in open(os.path.join(FID, HEROES["ids_file"])) if l.strip()]
        hero_idx = [idx_of[i] for i in REAL if i in idx_of]
    else:
        REAL = [v["id"] for k, v in sorted(by_idx.items()) if v["class"] in HEROES["classes"]]
        hero_idx = [k for k, v in by_idx.items() if v["class"] in HEROES["classes"]]
    hero = np.isin(idx, hero_idx)
    ground = (idx == 0) if LAND.get("id0") else np.isin(idx, [idx_of[i] for i in LAND["ids"] if i in idx_of])
    extra = np.isin(idx, [k for k, v in by_idx.items() if v["class"] in GROW_EXTRA])
    rep = {"_what": "BV2F PT pilot take (fid/pt/tools/bv2f_take.py): v1's take (a)+(b) on the pilot",
           "painting": {"file": "fid/pt/pilot/painting.png", "sha256": sha, "px": [W, H]},
           "camera": {"projection": "orthographic", "pitch_deg": math.degrees(PITCH), "yaw_deg": 47.0, "px_per_m": PPM,
                      "px_per_ground_m_v": round(PXV, 4), "px_per_vertical_m": round(PXH, 4), "u0": U0, "v1": V1,
                      "screen_right_world": SCREEN_RIGHT.round(6).tolist(), "screen_up_world": SCREEN_UP.round(6).tolist(),
                      "to_camera_world": TO_CAMERA.round(6).tolist(), "id_render_check": IDS["instrument_check"]},
           "ids": {"total_site_ungrouped": len(by_idx), "in_pilot": int(len(np.unique(idx)) - (1 if (idx == 0).any() else 0)),
                   "dev16": "NOT OPENED: %d ids ungrouped site-wide <= 256" % len(by_idx)}}

    # ------------------------------------------------------------------ (a) plates (take_from_paint.py:131-230)
    pdir = os.path.join(OUT, "plates")
    os.makedirs(pdir, exist_ok=True)
    plates = {}
    ring = 3
    grow_pool = ground | extra         # v1: ground | birch (take_from_paint.py:137)
    for k in sorted(hero_idx):
        e = by_idx[k]
        core = idx == k
        n = int(core.sum())
        grown = ndimage.binary_dilation(core, iterations=ring) & (core | grow_pool)
        ys, xs = np.where(grown)
        x0, x1 = max(int(xs.min()) - 2, 0), min(int(xs.max()) + 3, W)
        y0, y1 = max(int(ys.min()) - 2, 0), min(int(ys.max()) + 3, H)
        a = np.zeros((y1 - y0, x1 - x0), np.uint8)
        a[grown[y0:y1, x0:x1]] = 160
        a[core[y0:y1, x0:x1]] = 255
        rgba = np.dstack([P8[y0:y1, x0:x1], a])
        Image.fromarray(rgba, "RGBA").save(os.path.join(pdir, "%s.png" % e["id"]))
        rim = ndimage.binary_dilation(core, iterations=2) & ~core
        touch = sorted({by_idx[int(t)]["id"] for t in np.unique(idx[rim]) if t > 0 and int(t) != k})
        med = l2s(np.median(s2l(P8[core].astype(np.float32) / 255.0), axis=0))
        cx, cy = x0 + (x1 - x0) / 2.0, y0 + (y1 - y0) / 2.0
        cu, cv = uv_of_px(cx - 0.5, cy - 0.5)
        aim = world_of_uv(cu, cv, 0.0)
        sr = json.load(open(os.path.join(MESHES, "%s.json" % e["id"])))["screen_rect_px"] if MESHES else None
        plates[e["id"]] = {
            "class": e["class"], "piece": e["piece"], "id_index": k,
            "file": "plates/%s.png" % e["id"],
            "rect_px": [x0, y0, x1 - x0, y1 - y0],
            "visible_px": n, "ring_px": int(grown.sum()) - n,
            "alpha": "255 = the piece as the ID render sees it, 160 = the 3 px ring the painter's ink and snow may overhang onto the ground, 0 = not this piece",
            "fill_srgb_for_unseen": [int(round(float(c) * 255)) for c in med],
            "touches_in_view": touch,
            "cell": {"rect": [x0, y0, x1 - x0, y1 - y0], "px_per_m": PPM,
                     "screen_right": SCREEN_RIGHT.round(6).tolist(),
                     "screen_up": SCREEN_UP.round(6).tolist(),
                     "aim": aim.round(5).tolist(),
                     "view_dir": TO_CAMERA.round(6).tolist()},
            "mesh_screen_rect_px": [round(float(v), 1) for v in sr] if sr else None,
            "mesh_rect_inside_plate_window": bool(sr[0] >= -0.5 and sr[1] >= -0.5 and sr[0] + sr[2] <= W + 0.5 and sr[1] + sr[3] <= H + 0.5) if sr else None,
        }
    json.dump({"_what": "BV2F PT pilot: the hero identity plates, cut from the pilot painting by the ID render (v1 take (a))",
               "camera": rep["camera"], "plates": plates}, open(os.path.join(pdir, "plates.json"), "w"), indent=1)
    rep["plates"] = {"count": len(plates), "missing_in_ids": [i for i in REAL if i not in idx_of],
                     "mesh_extends_outside_the_pilot_plate": [k for k, v in plates.items() if v["mesh_rect_inside_plate_window"] is False]}
    print("(a) %d plates; meshes reaching past the pilot plate: %s" % (len(plates), rep["plates"]["mesh_extends_outside_the_pilot_plate"]))

    # ------------------------------------------------------------------ (b) tufts (take_from_paint.py:231-344, verbatim)
    f = P8.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    lum = f.mean(-1)
    mx, mn = f.max(-1), f.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1.0)
    heather = (r > g) & (g > b) & (r - b > 42) & (sat > 0.24) & (lum < 212)
    shrub = (lum < 128) & (b < r + 6) & (g >= r - 12) & ~heather
    pool = ground
    heather &= pool
    shrub &= pool
    tuft_px = heather | shrub
    tuft_px = ndimage.binary_opening(tuft_px, iterations=1)
    merged = ndimage.binary_closing(tuft_px, structure=np.ones((5, 5), bool), iterations=1) & pool
    lab, nlab = ndimage.label(merged, np.ones((3, 3), int))
    sl = ndimage.find_objects(lab)
    tufts = []
    for i, s in enumerate(sl, start=1):
        if s is None:
            continue
        m = lab[s] == i
        area = int(m.sum())
        if area < 30:
            continue
        ys, xs = np.nonzero(m)
        ys = ys + s[0].start
        xs = xs + s[1].start
        nh = int(heather[ys, xs].sum())
        ns = int(shrub[ys, xs].sum())
        if nh + ns < 20:
            continue
        yb = int(ys.max())
        xb = float(xs[ys >= yb - 3].mean())
        bu, bv = uv_of_px(xb, yb)
        w_m = (xs.max() - xs.min() + 1) / PXU
        h_px = ys.max() - ys.min() + 1
        tcls = "heather" if nh >= 3 * ns else ("shrub" if ns >= 3 * nh else "mixed")
        tufts.append({"uv": [round(float(bu), 3), round(float(bv), 3)], "class": tcls, "width_m": round(float(w_m), 3),
                      "screen_h_px": int(h_px), "screen_area_px": area, "heather_px": nh, "shrub_px": ns})
    RES = 10.0
    GU, GV = int(round((U1 - U0) * RES)), int(round((V1 - V0) * RES))
    dens_h = np.zeros((GV, GU), np.float32)
    dens_s = np.zeros((GV, GU), np.float32)
    ys, xs = np.nonzero(tuft_px)
    tu, tv = uv_of_px(xs, ys, h=TUFT_HALF_H_M)
    ci = np.clip(((tu - U0) * RES).astype(int), 0, GU - 1)
    cj = np.clip(((V1 - tv) * RES).astype(int), 0, GV - 1)
    isH = heather[ys, xs]
    cell_px = (PXU / RES) * (PXV / RES)
    np.add.at(dens_h, (cj[isH], ci[isH]), 1.0 / cell_px)
    np.add.at(dens_s, (cj[~isH], ci[~isH]), 1.0 / cell_px)
    dens_h = np.clip(dens_h, 0, 1)
    dens_s = np.clip(dens_s, 0, 1)
    mdir = os.path.join(OUT, "masks")
    os.makedirs(mdir, exist_ok=True)
    Image.fromarray(np.dstack([(dens_h * 255).astype(np.uint8), (dens_s * 255).astype(np.uint8),
                               np.zeros_like(dens_h, np.uint8)]), "RGB").save(os.path.join(mdir, "density_uv.png"))
    json.dump({"_what": "BV2F PT pilot (b): per-class density masks, taken from the pilot painting (v1 take (b))",
               "frame": {"u": [U0, U1], "v": [V0, V1], "px_per_m": RES,
                         "density_uv_png": "masks/density_uv.png: R = heather cover, G = shrub cover; row 0 = v1 (north), column 0 = u0",
                         "_pool": "ground = ID 0 (v1)" if LAND.get("id0") else "the LAND ground ids %s (v1: ground = ID 0)" % sorted(LAND["ids"])},
               "tufts": tufts}, open(os.path.join(mdir, "tufts.json"), "w"), indent=1)
    nh = sum(1 for t in tufts if t["class"] == "heather")
    nsh = sum(1 for t in tufts if t["class"] == "shrub")
    rep["tufts"] = {"count": len(tufts), "heather": nh, "shrub": nsh, "mixed": len(tufts) - nh - nsh,
                    "tuft_px_share_of_ground": round(float(tuft_px[ground].mean()), 4),
                    "heather_px": int(heather.sum()), "shrub_px": int(shrub.sum()), "density_raster_px": [GU, GV]}
    print("(b) %d tufts (%d heather, %d shrub, %d mixed)" % (len(tufts), nh, nsh, len(tufts) - nh - nsh))
    json.dump(rep, open(os.path.join(OUT, "take_report.json"), "w"), indent=1)


main()
