#!/usr/bin/env python3
"""BV2F lane PT, Phase 2' (R-C9-191; DEV-17 R-C9-192): THE PAINTED DATA -- v1's paint_world_prep.py main() as a
front end. v1's tool (fid/v1tools/tierB/barrow_full/tools/paint_world_prep.py) is wired to v1's schema; its algorithms
run here VERBATIM (each block cited to its v1 line), every input chosen by a CONFIG:
    python3 fid/pt/tools/bv2f_prep.py [--config CFG.json]      (default: the pilot, fid/pt/pilot/fe_prep.json)
The pilot config states the pilot's adaptations (DEV-17/DEV-18):
  * ground = the LAND ground ids of the ungrouped pilot ID render (v1: ID 0);
  * flat = |terrain| < 0.03 m from the bv2art heightfield (v1: all flat); snow_open = the snow id, flat (v1: ground_uv);
  * 3D heather on FLAT tufts only (DEV-18); the snow grid from the bv2art class map, flat only (v1: the painted splat);
  * no inpainted ground (v1 ships as_painted; its inpainted variant was a measured reject).
fid/pt/dev17/fe_prep_v1.json runs the SAME code on v1's own data with v1's choices (ID 0, all flat, v1's ground_uv, v1's
splat snow, inpaint on): the DEV-17 proof compares its outputs with v1's recorded ones.
"""
import hashlib, json, math, os, shutil, sys
import numpy as np
from PIL import Image
from scipy import ndimage

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_a = sys.argv[1:]
CFG = json.load(open(_a[_a.index("--config") + 1] if "--config" in _a else os.path.join(FID, "pt", "pilot", "fe_prep.json")))
P_ = lambda v: v if os.path.isabs(v) else os.path.join(FID, v)
PAINTING = P_(CFG["painting"])
LIT = P_(CFG["lit"])
OUT = P_(CFG["out"])
REPORT = P_(CFG["report"])

U0, V1 = float(CFG["frame"]["u0"]), float(CFG["frame"]["v1"])
W, H = int(CFG["frame"]["px"][0]), int(CFG["frame"]["px"][1])
PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
PXV, PXH = PPM * math.sin(PITCH), PPM * math.cos(PITCH)
C47, S47 = math.cos(math.radians(47.0)), math.sin(math.radians(47.0))
# v1 paint_world_prep.py:48-56, unchanged
SNOW_BY_CLASS = {"snow": (1.00, 0.00, 0.00), "path": (0.36, 0.12, 0.85), "rock": (0.45, 0.46, 0.00),
                 "heather": (0.22, 0.70, 0.00), "ice": (0.00, 0.00, 0.00)}
HEATHER_ALBEDO_MUL = (round(1.622 * 0.7715, 4), round(1.254 * 0.8059, 4), round(0.534 * 1.0631, 4))
HEATHER_ALBEDO_MUL_WHY = ("the installed Barrow's stem grade (1.622, 1.254, 0.534) x the overlay check's first "
                          "calibration (0.7715, 0.8059, 1.0631): the sprays' own colour onto the painted tufts beneath them")   # paint_world_prep.py:56-57, verbatim
BV2ART_TO_SNOW = {"snow": "snow", "path": "path", "rock": "rock", "shingle": "rock", "shrub": "heather",
                  "ice": "ice", "shore_ice": "ice", "stream": "ice", "sea": "ice"}


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def l2s(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def uv_of_px(x, y, h=0.0):        # paint_world_prep.py:75
    return U0 + x / PPM, V1 - (y + h * PXH) / PXV


def xz_of_uv(u, v):               # paint_world_prep.py:83
    return u * C47 - v * S47, -u * S47 - v * C47


def _up2(a, shape):               # paint_world_prep.py:87, verbatim
    h, w = shape
    ys = (np.arange(h) + 0.5) / 2.0 - 0.5
    xs = (np.arange(w) + 0.5) / 2.0 - 0.5
    y0 = np.clip(np.floor(ys).astype(int), 0, a.shape[0] - 1)
    x0 = np.clip(np.floor(xs).astype(int), 0, a.shape[1] - 1)
    y1 = np.clip(y0 + 1, 0, a.shape[0] - 1)
    x1 = np.clip(x0 + 1, 0, a.shape[1] - 1)
    ty = np.clip(ys - np.floor(ys), 0, 1)[:, None, None]
    tx = np.clip(xs - np.floor(xs), 0, 1)[None, :, None]
    top = a[y0][:, x0] * (1 - tx) + a[y0][:, x1] * tx
    bot = a[y1][:, x0] * (1 - tx) + a[y1][:, x1] * tx
    return top * (1 - ty) + bot * ty


def push_pull(img, known):        # paint_world_prep.py:104, verbatim
    levels = []
    c = img * known[..., None]
    w = known.astype(np.float64)
    while min(w.shape) > 4:
        levels.append((c, w))
        h2, w2 = (w.shape[0] + 1) // 2 * 2, (w.shape[1] + 1) // 2 * 2
        cp = np.zeros((h2, w2, 3)); wp = np.zeros((h2, w2))
        cp[:c.shape[0], :c.shape[1]] = c; wp[:w.shape[0], :w.shape[1]] = w
        c = cp.reshape(h2 // 2, 2, w2 // 2, 2, 3).sum((1, 3))
        w = wp.reshape(h2 // 2, 2, w2 // 2, 2).sum((1, 3))
    fill = c / np.maximum(w, 1e-9)[..., None]
    for c, w in reversed(levels):
        up = _up2(fill, w.shape)
        mine = c / np.maximum(w, 1e-9)[..., None]
        a = np.clip(w, 0.0, 1.0)[..., None]
        fill = mine * a + up * (1.0 - a)
    return np.where(known[..., None], img, fill)


def tuft_classes(P8, ground):     # paint_world_prep.py:127, verbatim
    f = P8.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    lum = f.mean(-1)
    sat = (f.max(-1) - f.min(-1)) / np.maximum(f.max(-1), 1.0)
    heather = (r > g) & (g > b) & (r - b > 42) & (sat > 0.24) & (lum < 212) & ground
    shrub = (lum < 128) & (b < r + 6) & (g >= r - 12) & ~heather & ground
    return heather, shrub


def main():
    os.makedirs(os.path.join(OUT, "bakes"), exist_ok=True)
    sha = sha_file(PAINTING)
    P8 = np.asarray(Image.open(PAINTING).convert("RGB"))
    assert P8.shape[:2] == (H, W)
    Plin = s2l(P8.astype(np.float64) / 255.0)
    rep = {"_what": CFG.get("report_what", "BV2F PT: painted data, measured (fid/pt/tools/bv2f_prep.py = v1 paint_world_prep main)"),
           "painting_sha256": sha}
    man = {"_what": CFG.get("manifest_what", "what the painted level wears, every file's sha256 -- the scene checks each as it loads it"),
           "painting": {}, "bakes": {}}
    if CFG.get("manifest_frame"):
        man["frame"] = {"u0": U0, "v1": V1, "px": [W, H], "px_per_m": PPM}
    # the ID render, v1's decode (paint_world_prep.py:138-146)
    IDS = json.load(open(P_(CFG["ids_dir"]) + "/ids.json"))
    ID8 = np.asarray(Image.open(P_(CFG["ids_dir"]) + "/ids.png").convert("RGB")).astype(np.int32)
    is_pl = ID8[..., 2] > 100
    idx = np.where(is_pl, np.clip(np.round((ID8[..., 1] - 8) / 16.0), 0, 15).astype(np.int32) * 16
                   + np.clip(np.round((ID8[..., 0] - 8) / 16.0), 0, 15).astype(np.int32), 0)
    idx_of = {v["id"]: int(k) for k, v in IDS["placements"].items()}
    ground = (idx == 0) if CFG["land"].get("id0") else np.isin(idx, [idx_of[i] for i in CFG["land"]["ids"] if i in idx_of])
    ys, xs = np.mgrid[0:H, 0:W]
    uu, vv = uv_of_px(xs + 0.5, ys + 0.5)
    # FLAT (DEV-18): the terrain under each pixel at h = 0; v1's floor is flat everywhere
    L = Hf = hf = None
    if CFG["flat"].get("level"):
        L = json.load(open(P_(CFG["flat"]["level"])))
        hf = L["sim"]["heightfield"]
        Hf = np.fromfile(os.path.join(os.path.dirname(P_(CFG["flat"]["level"])), hf["file"]), "<f4").reshape(hf["shape"])
        ex = hf["extent_sim_m"]
        hi = np.clip(((uu - ex["x0"]) * hf["px_per_m"]).astype(int), 0, Hf.shape[1] - 1)
        hj = np.clip(((-vv - ex["y0"]) * hf["px_per_m"]).astype(int), 0, Hf.shape[0] - 1)
        flat = np.abs(Hf[hj, hi]) < 0.03
    else:
        flat = np.ones((H, W), bool)
    # tufts: step 3's classifier re-run and checked against the take's own counts (paint_world_prep.py:164-171)
    heather, shrub = tuft_classes(P8, ground)
    T3 = json.load(open(P_(CFG["take_report"])))["tufts"]
    rep["tufts_self_test"] = {"heather_px": [int(heather.sum()), T3["heather_px"]], "shrub_px": [int(shrub.sum()), T3["shrub_px"]],
                              "PASS": int(heather.sum()) == T3["heather_px"] and int(shrub.sum()) == T3["shrub_px"],
                              "_": "[this run, step 3's take_report] -- the same classifier on the same painting"}
    assert rep["tufts_self_test"]["PASS"], rep["tufts_self_test"]
    tuft_px = ndimage.binary_opening(heather | shrub, iterations=1)
    # the painting's light (paint_world_prep.py:173-182)
    LG = s2l(np.asarray(Image.open(LIT).convert("RGB")).astype(np.float64) / 255.0)
    assert LG.shape[:2] == (H, W)
    castG, ndlB = LG[..., 1], LG[..., 2]
    litR = castG * np.clip(ndlB / math.sin(math.radians(55.0)), 0.0, 1.0)
    # open snow (paint_world_prep.py:183-194): v1 = ground with step 3's ground_uv class 0; the pilot = the snow id, flat
    so = CFG["snow_open"]
    if so.get("v1_ground_uv"):
        GU = np.asarray(Image.open(P_(so["v1_ground_uv"])))
        if GU.ndim == 3:
            GU = GU[..., 0]
        gpx = json.load(open(P_(CFG["take_report"])))["ground"]["px_per_m"]
        gi = np.clip(((uu - U0) * gpx).astype(int), 0, GU.shape[1] - 1)
        gj = np.clip(((V1 - vv) * gpx).astype(int), 0, GU.shape[0] - 1)
        snow_open = ground & (GU[gj, gi] == 0)
    else:
        snow_open = (idx == idx_of.get(so["ground_id"], -1)) & flat
    # THE PAINTER'S SHADOW, measured (paint_world_prep.py:196-239, verbatim)
    clear = snow_open & ~ndimage.binary_dilation(tuft_px | ~ground, iterations=12)
    sh_set = clear & (castG < 0.08) & (litR < 0.08)
    lt_set = clear & (castG > 0.98) & (litR > 0.98)
    med_sh = np.median(Plin[sh_set], axis=0)
    med_lt = np.median(Plin[lt_set], axis=0)
    mul = med_sh / med_lt
    per_chunk = {}
    for ch in CFG["chunks"]:
        x0, y0, x1, y1 = ch["px"]
        a = sh_set[y0:y1, x0:x1]
        bm = lt_set[y0:y1, x0:x1]
        if a.sum() > 2000 and bm.sum() > 2000:
            per_chunk[ch["key"]] = [round(float(v), 3) for v in
                                    np.median(Plin[y0:y1, x0:x1][a], axis=0) / np.median(Plin[y0:y1, x0:x1][bm], axis=0)]
    ax = med_sh - med_lt
    s = ((Plin - med_lt) @ ax) / float(ax @ ax)
    s = ndimage.median_filter(s.astype(np.float32), size=21)
    painted_sh = (s > 0.5) & snow_open
    render_sh = (castG < 0.5) & snow_open
    inter = float((painted_sh & render_sh).sum())
    union = float((painted_sh | render_sh).sum())
    near = float((painted_sh & ndimage.binary_dilation(render_sh, iterations=10)).sum())
    rep["shadow"] = {
        "painted_shadow_over_painted_light_linear": [round(float(v), 4) for v in mul],
        "as_srgb_on_lit_snow": {"lit": [int(round(float(v) * 255)) for v in l2s(med_lt)],
                                "shadow": [int(round(float(v) * 255)) for v in l2s(med_sh)]},
        "pixels": {"shadow": int(sh_set.sum()), "lit": int(lt_set.sum())},
        "per_chunk_linear": per_chunk,
        "painted_vs_rendered_shadow_on_open_snow": {
            "recall_rendered_shadow_painted_as_shadow": round(inter / max(float(render_sh.sum()), 1.0), 4),
            "precision": round(inter / max(float(painted_sh.sum()), 1.0), 4), "iou": round(inter / max(union, 1.0), 4),
            "painted_shadow_within_10px_of_a_rendered_one": round(near / max(float(painted_sh.sum()), 1.0), 4),
            "painted_px": int(painted_sh.sum()), "rendered_px": int(render_sh.sum()),
            "_read": "recall: the share of the render's cast shadow the painter painted as shadow -- where the SUN's real shadow will darken him; the rest of the painted blue is the snow's own washes (hollows, dabs), which no object casts",
            "_instrument": "painted: a pixel's position on the lit->shadow colour axis > 0.5 after a 21 px median; rendered: the blockout's own cast shadow (lit_guide G < 0.5); open snow only"},
        "_use": "his shadow on the painted world = this multiplier (PaintedWorld.shadow_mul), where the painting shows sun (lit.bin)"}
    man["shadow_mul"] = {"linear": [round(float(v), 4) for v in mul], "_": "measured: the painting's shadowed open snow over its sunlit open snow (median, linear)"}
    # the painting, as is (paint_world_prep.py:241-244)
    shutil.copyfile(PAINTING, os.path.join(OUT, "painting.bin"))
    man["painting"] = {"file": "painting.bin", "sha256": sha, "px": [W, H], "_": CFG.get("painting_note", "the accepted paint-over's own PNG bytes")}
    man["ground_as_painted"] = dict(man["painting"])
    # the ground, the tufts taken out (paint_world_prep.py:246-257) -- v1 config only
    if CFG.get("inpaint"):
        hole = ndimage.binary_dilation(tuft_px, iterations=2) & ground
        filled = np.where(hole[..., None], push_pull(Plin, ground & ~hole), Plin)
        G8 = (l2s(filled) * 255.0 + 0.5).astype(np.uint8)
        gp = os.path.join(OUT, "ground_inpainted.bin")
        Image.fromarray(G8, "RGB").save(gp, format="PNG", compress_level=6)
        man["ground_inpainted"] = {"file": "ground_inpainted.bin", "sha256": sha_file(gp), "px": [W, H],
                                   "_": "the painting with the tufts the 3D heather replaces filled from the ground round them"}
        rep["inpaint"] = {"px": int(hole.sum()), "share_of_ground": round(float(hole[ground].mean()), 4),
                          "method": "push-pull pyramid fill (bilinear pull; donors: ground pixels only; known pixels untouched), linear light; the tuft mask dilated 2 px for its ink"}
    # the light map, half resolution (paint_world_prep.py:259-264)
    lr = litR.reshape(H // 2, 2, W // 2, 2).mean((1, 3))
    lp = os.path.join(OUT, "lit.bin")
    Image.fromarray((np.clip(lr, 0, 1) * 255.0 + 0.5).astype(np.uint8), "L").save(lp, format="PNG")
    man["lit"] = {"file": "lit.bin", "sha256": sha_file(lp), "px": [W // 2, H // 2],
                  "_": "the painting's direct sun as a share of flat sunlit ground's: lit_guide G x min(B / sin 55, 1), 8-bit, half resolution"}
    # the bakes (paint_world_prep.py:266-276)
    BR = json.load(open(P_(CFG["bake_report"])))
    for pid, b in sorted(BR["pieces"].items()):
        if b.get("bake") == "FAILED":
            continue
        dst = os.path.join(OUT, "bakes", "%s.bin" % pid)
        shutil.copyfile(os.path.join(P_(CFG["bakes_dir"]), "%s.png" % pid), dst)
        man["bakes"][pid] = {"file": "bakes/%s.bin" % pid, "sha256": sha_file(dst)}
    if CFG.get("manifest_frame"):
        man["real_models_in_window"] = sorted(BR["pieces"].keys())
    rep["bakes"] = len(man["bakes"])
    if CFG.get("bakes_expected") is not None:
        assert len(man["bakes"]) == CFG["bakes_expected"], len(man["bakes"])
    # the heather: v1's counts, v1's greedy cover (paint_world_prep.py:278-348); the pilot: on FLAT tufts (DEV-18)
    HI = json.load(open(P_(CFG["heather_instances"])))
    cs = 4
    Hc, Wc = H // cs, W // cs
    def cells(m):
        return m[:Hc * cs, :Wc * cs].reshape(Hc, cs, Wc, cs).mean((1, 3))
    rows, cols, counts = [], [], []
    placed_px = {}
    remaining = {"heather": cells(heather & tuft_px & flat), "shrub": cells(shrub & tuft_px & flat)}
    for ci, cls in ((1, "shrub"), (0, "heather")):
        c = HI["classes"][cls]
        hgt = float(c["height_m"])
        n_want = int(c["count"])
        rx = 0.78 * hgt * PPM
        ry = 0.5 * (hgt * PXH + 1.55 * hgt * PXV)
        R = remaining[cls].copy()
        kx, ky = max(int(round(2 * rx / cs)), 1), max(int(round(2 * ry / cs)), 1)
        ex_, ey = rx / cs, ry / cs
        got = 0
        while got < n_want:
            score = ndimage.uniform_filter(R, size=(ky, kx), mode="constant")
            j, i = np.unravel_index(int(np.argmax(score)), score.shape)
            if score[j, i] <= 1e-6:
                break
            y0, y1 = max(int(j - ey), 0), min(int(j + ey) + 1, Hc)
            x0, x1 = max(int(i - ex_), 0), min(int(i + ex_) + 1, Wc)
            yy, xx = np.mgrid[y0:y1, x0:x1]
            ell = ((xx - i) / ex_) ** 2 + ((yy - j) / ey) ** 2 <= 0.8 ** 2
            R[y0:y1, x0:x1][ell] = 0.0
            cx, cy = (i + 0.5) * cs, (j + 0.5) * cs
            u, v = uv_of_px(cx, cy, hgt * 0.5)
            x, z = xz_of_uv(u, v)
            X0, X1 = int(max(cx - rx, 0)), int(min(cx + rx + 1, W))
            Y0, Y1 = int(max(cy - ry, 0)), int(min(cy + ry + 1, H))
            YY, XX = np.mgrid[Y0:Y1, X0:X1]
            fel = ((XX + 0.5 - cx) / rx) ** 2 + ((YY + 0.5 - cy) / ry) ** 2 <= 1.0
            tm = fel & tuft_px[Y0:Y1, X0:X1]
            if tm.sum() < 12:
                tm = fel & ground[Y0:Y1, X0:X1]
            cols.append(Plin[Y0:Y1, X0:X1][tm].mean(axis=0))
            counts.append(int(tm.sum()))
            rows.append([round(float(x), 4), round(float(z), 4), hgt, ci])
            got += 1
        placed_px[cls] = {"placed": got, "wanted": n_want, "footprint_px": [round(2 * rx, 1), round(2 * ry, 1)],
                          "tuft_cells_covered_share": round(1.0 - float(R.sum()) / max(float(remaining[cls].sum()), 1e-9), 4)}
    cols = np.array(cols)
    mean = cols.mean(axis=0)
    rel = cols / mean
    for rw, m in zip(rows, rel):
        rw += [round(float(m[0]), 4), round(float(m[1]), 4), round(float(m[2]), 4)]
    json.dump({"_what": CFG.get("heather_what", "the 3D heather: v1's counts RE-PLACED on the painted tufts (greedy cover), each coloured by the painting's tufts beneath it"),
               "columns": ["x", "z", "height_m", "class (0 heather, 1 shrub)", "mul_r", "mul_g", "mul_b"],
               "_mul": "linear: the painting's tuft pixels under the spray's screen footprint, over the mean of all sprays",
               "painted_mean_linear": [round(float(v), 5) for v in mean], "placement": placed_px, "rows": rows},
              open(os.path.join(OUT, "heather.json"), "w"))
    man["heather"] = {"file": "heather.json", "count": len(rows), "albedo_mul": list(HEATHER_ALBEDO_MUL),
                      "_albedo_mul": HEATHER_ALBEDO_MUL_WHY}
    rep["heather"] = {"instances": len(rows), "placement": placed_px,
                      "painted_mean_linear": [round(float(v), 5) for v in mean],
                      "painted_mean_srgb": [int(round(float(v) * 255)) for v in l2s(mean)],
                      "rel_mul_p10_p50_p90": [[round(float(np.percentile(rel[:, k], q)), 3) for q in (10, 50, 90)] for k in range(3)],
                      "tuft_px_per_spray_median": int(np.median(counts))}
    if CFG["flat"].get("level"):
        rep["heather"]["tufts_on_flat_land_share"] = round(float((tuft_px & flat).sum()) / max(float(tuft_px.sum()), 1.0), 4)
    # the snow's depth grid (paint_world_prep.py:350-391)
    sn = CFG["snow"]
    if sn.get("v1_splat"):
        V = sn["v1_splat"]
        rb = V["reach_box"]
        cu = [xz_of_uv(u, v) for u in rb["u"] for v in rb["v"]]
    else:
        win = [(U0, V1 - H / PXV), (U0 + W / PPM, V1 - H / PXV), (U0, V1), (U0 + W / PPM, V1)]
        cu = [xz_of_uv(u, v) for u, v in win]
    pad = 1.5
    xmn, xmx = min(p[0] for p in cu) - pad, max(p[0] for p in cu) + pad
    zmn, zmx = min(p[1] for p in cu) - pad, max(p[1] for p in cu) + pad
    side = max(xmx - xmn, zmx - zmn)
    cx, cz = (xmn + xmx) / 2, (zmn + zmx) / 2
    area = [round(cx - side / 2, 3), round(cz - side / 2, 3), round(side, 3), round(side, 3)]
    cell = 0.1
    nx = int(math.ceil(side / cell)) + 1
    gx0, gz0 = area[0], area[1]
    zz, xx = np.mgrid[0:nx, 0:nx]
    X = gx0 + xx * cell
    Z = gz0 + zz * cell
    rng = np.random.default_rng(91127)
    def smooth_noise(scale_m):
        n0 = rng.random((nx, nx))
        s_ = ndimage.gaussian_filter(n0, sigma=scale_m / cell, mode="wrap")
        return (s_ - s_.mean()) / (s_.std() * 6.0) + 0.5
    if sn.get("v1_splat"):
        SP = np.asarray(Image.open(P_(V["splat"])).convert("RGBA")).astype(np.float64) / 255.0
        so_, smpp = V["origin_xz"], V["m_per_px"]
        si = np.clip(((X - so_[0]) / smpp).astype(int), 0, SP.shape[1] - 1)
        sj = np.clip(((Z - so_[1]) / smpp).astype(int), 0, SP.shape[0] - 1)
        w = SP[sj, si]
        wsnow = np.clip(1.0 - w.sum(-1), 0.0, 1.0)
        weights = (("snow", wsnow), ("path", w[..., 0]), ("rock", w[..., 1]), ("heather", w[..., 2]), ("ice", w[..., 3]))
    else:
        cp = L["sim"]["classes_png"]
        CL = np.asarray(Image.open(os.path.join(os.path.dirname(P_(CFG["flat"]["level"])), cp["file"])))
        if CL.ndim == 3:
            CL = CL[..., 0]
        Uw = X * C47 - Z * S47
        Vw = -X * S47 - Z * C47
        sx, sy = Uw, -Vw
        ci_ = np.clip(((sx - cp["extent_sim_m"]["x0"]) * cp["px_per_m"]).astype(int), 0, CL.shape[1] - 1)
        cj_ = np.clip(((sy - cp["extent_sim_m"]["y0"]) * cp["px_per_m"]).astype(int), 0, CL.shape[0] - 1)
        cls_grid = CL[cj_, ci_]
        ex = hf["extent_sim_m"]
        hi_ = np.clip(((sx - ex["x0"]) * hf["px_per_m"]).astype(int), 0, Hf.shape[1] - 1)
        hj_ = np.clip(((sy - ex["y0"]) * hf["px_per_m"]).astype(int), 0, Hf.shape[0] - 1)
        flat_g = np.abs(Hf[hj_, hi_]) < 0.03
        weights = []
        for k_, nm in enumerate(L["classes"]):
            if BV2ART_TO_SNOW.get(nm):
                weights.append((BV2ART_TO_SNOW[nm], ((cls_grid == k_) & flat_g).astype(np.float64)))
    nv = np.clip(smooth_noise(1.4) * 0.7 + smooth_noise(0.45) * 0.3, 0.0, 1.0)
    mulg = np.zeros((nx, nx))
    trod = np.zeros((nx, nx))
    for name, wk in weights:
        m_, patch, tr = SNOW_BY_CLASS[name]
        keep = np.clip((nv - (patch - 0.08)) / 0.16, 0.0, 1.0) if patch > 0 else 1.0
        keep = keep * keep * (3 - 2 * keep) if patch > 0 else 1.0
        mulg += wk * m_ * keep
        trod += wk * tr
    gridp = os.path.join(OUT, "snow_grid.bin")
    np.concatenate([mulg.astype("<f4").ravel(), trod.astype("<f4").ravel()]).tofile(gridp)
    man["snow"] = {"area_xz": area, "field_px": 768, "trail_px": 1024,
                   "grid": {"file": "snow_grid.bin", "sha256": sha_file(gridp), "origin_xz": [gx0, gz0], "cell_m": cell,
                            "nx": nx, "nz": nx, "_layout": "float32 little-endian: nx*nz depth multipliers (row = z), then nx*nz trodden amounts"},
                   "_": CFG.get("snow_note", "the installed Barrow's SNOW_BY_CLASS on the painted splat; the field covers the reach box + 1.5 m (world xz, square)")}
    rep["snow"] = {"area_xz": area, "grid_cells": nx * nx, "mean_mul": round(float(mulg.mean()), 4),
                   "bare_share_mul_under_0.125": round(float((mulg < 0.125).mean()), 4)}
    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    json.dump(rep, open(REPORT, "w"), indent=1)
    print(json.dumps({k: rep[k] for k in ("tufts_self_test", "heather", "snow")}, indent=1)[:1500])


main()
