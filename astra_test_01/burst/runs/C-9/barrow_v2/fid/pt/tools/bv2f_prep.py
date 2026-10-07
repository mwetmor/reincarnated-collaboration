#!/usr/bin/env python3
"""BV2F lane PT, Phase 2' (R-C9-191): THE PILOT'S PAINTED DATA -- v1's paint_world_prep.py main() on the pilot.

v1's tool (fid/v1tools/tierB/barrow_full/tools/paint_world_prep.py) is wired to v1's schema (ground = ID 0, step 3's
ground_uv raster, 25 bakes asserted, v1's splat). Its algorithms are run here VERBATIM, each block cited to its v1 line,
with these stated adaptations:
  * frame = the pilot plate; ground = the LAND ground ids of the ungrouped pilot ID render (snow, shrub, path, mound);
  * snow_open (the shadow measurement's pool) = the snow ground id, FLAT (|terrain| < 0.03 m: v1's floor was flat);
  * the 3D heather: v1's counts (heather_instances.py, Tier A, run on the pilot root) and v1's greedy cover, on the
    painted tufts of FLAT land only -- v1's sprays stand at y = 0 (barrow_full.gd _build_painted_heather), so a tuft
    painted on the mound's flank stays painted, as v1's would have had it no floor under it;
  * the snow grid: v1's SNOW_BY_CLASS on the bv2art class map (level.json classes_png) -- snow->snow, path->path,
    rock/shingle->rock, shrub->heather, ice/shore ice/stream/sea->ice (none) -- zero where the terrain is not flat;
  * no inpainted ground (v1 ships as_painted; the inpainted variant was a measured reject).
    python3 fid/pt/tools/bv2f_prep.py
Writes barrow_full/godot/data/bv2f/pilot/painted/{manifest.json, painting.bin, lit.bin, bakes/*.bin, heather.json,
snow_grid.bin} and fid/pt/pilot/painted_prep.json.
"""
import hashlib, json, math, os, shutil
import numpy as np
from PIL import Image
from scipy import ndimage

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C9 = os.path.dirname(os.path.dirname(FID))
PILOT = os.path.join(FID, "pt", "pilot")
ROOT = os.path.join(PILOT, "root")
PAINTING = os.path.join(PILOT, "painting.png")
LIT = os.path.join(ROOT, "work", "light", "lit_guide.png")
GD = os.path.join(C9, "barrow_full", "godot")
OUT = os.path.join(GD, "data", "bv2f", "pilot", "painted")
LEVEL = os.path.join(GD, "data", "bv2f", "art", "level.json")
LAND = {"ground_snow", "ground_shrub", "ground_path", "ground_mound"}

U0, V1 = -33.57573954303182, 22.36993715728635
PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
W, H = 4096, 2560
PXV, PXH = PPM * math.sin(PITCH), PPM * math.cos(PITCH)
C47, S47 = math.cos(math.radians(47.0)), math.sin(math.radians(47.0))
# v1 paint_world_prep.py:48-56, unchanged
SNOW_BY_CLASS = {"snow": (1.00, 0.00, 0.00), "path": (0.36, 0.12, 0.85), "rock": (0.45, 0.46, 0.00),
                 "heather": (0.22, 0.70, 0.00), "ice": (0.00, 0.00, 0.00)}
HEATHER_ALBEDO_MUL = (round(1.622 * 0.7715, 4), round(1.254 * 0.8059, 4), round(0.534 * 1.0631, 4))
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
    rep = {"_what": "BV2F PT pilot: the painted pilot's data, measured (fid/pt/tools/bv2f_prep.py = v1 paint_world_prep main on the pilot)",
           "painting_sha256": sha}
    man = {"_what": "what the painted pilot wears (godot/data/bv2f/pilot/painted/), every file's sha256 -- the scene checks each as it loads it",
           "painting": {}, "bakes": {}, "frame": {"u0": U0, "v1": V1, "px": [W, H], "px_per_m": PPM}}
    # the ID render (the ungrouped pilot render), v1's decode
    IDS = json.load(open(os.path.join(PILOT, "ids_built", "ids.json")))
    ID8 = np.asarray(Image.open(os.path.join(PILOT, "ids_built", "ids.png")).convert("RGB")).astype(np.int32)
    is_pl = ID8[..., 2] > 100
    idx = np.where(is_pl, np.clip(np.round((ID8[..., 1] - 8) / 16.0), 0, 15).astype(np.int32) * 16
                   + np.clip(np.round((ID8[..., 0] - 8) / 16.0), 0, 15).astype(np.int32), 0)
    idx_of = {v["id"]: int(k) for k, v in IDS["placements"].items()}
    ground = np.isin(idx, [idx_of[i] for i in LAND if i in idx_of])
    # the terrain under each pixel (at h = 0) -- flat where |h| < 0.03 m
    L = json.load(open(LEVEL))
    hf = L["sim"]["heightfield"]
    Hf = np.fromfile(os.path.join(os.path.dirname(LEVEL), hf["file"]), "<f4").reshape(hf["shape"])
    ex = hf["extent_sim_m"]
    ys, xs = np.mgrid[0:H, 0:W]
    uu, vv = uv_of_px(xs + 0.5, ys + 0.5)
    hi = np.clip(((uu - ex["x0"]) * hf["px_per_m"]).astype(int), 0, Hf.shape[1] - 1)
    hj = np.clip(((-vv - ex["y0"]) * hf["px_per_m"]).astype(int), 0, Hf.shape[0] - 1)
    flat = np.abs(Hf[hj, hi]) < 0.03
    # tufts: step 3's classifier re-run and checked against the take's own counts (paint_world_prep.py:164-171)
    heather, shrub = tuft_classes(P8, ground)
    T3 = json.load(open(os.path.join(ROOT, "take", "take_report.json")))["tufts"]
    rep["tufts_self_test"] = {"heather_px": [int(heather.sum()), T3["heather_px"]], "shrub_px": [int(shrub.sum()), T3["shrub_px"]],
                              "PASS": int(heather.sum()) == T3["heather_px"] and int(shrub.sum()) == T3["shrub_px"]}
    assert rep["tufts_self_test"]["PASS"], rep["tufts_self_test"]
    tuft_px = ndimage.binary_opening(heather | shrub, iterations=1)
    # the painting's light (paint_world_prep.py:173-182)
    LG = s2l(np.asarray(Image.open(LIT).convert("RGB")).astype(np.float64) / 255.0)
    assert LG.shape[:2] == (H, W)
    castG, ndlB = LG[..., 1], LG[..., 2]
    litR = castG * np.clip(ndlB / math.sin(math.radians(55.0)), 0.0, 1.0)
    # THE PAINTER'S SHADOW, measured (paint_world_prep.py:196-213), snow_open = flat snow ground
    snow_open = (idx == idx_of.get("ground_snow", -1)) & flat
    clear = snow_open & ~ndimage.binary_dilation(tuft_px | ~ground, iterations=12)
    sh_set = clear & (castG < 0.08) & (litR < 0.08)
    lt_set = clear & (castG > 0.98) & (litR > 0.98)
    med_sh = np.median(Plin[sh_set], axis=0)
    med_lt = np.median(Plin[lt_set], axis=0)
    mul = med_sh / med_lt
    per_chunk = {}
    for r in range(3):
        for c in range(3):
            x0, y0 = c * 1280, r * 768
            a = sh_set[y0:y0 + 1024, x0:x0 + 1536]
            bm = lt_set[y0:y0 + 1024, x0:x0 + 1536]
            if a.sum() > 2000 and bm.sum() > 2000:
                per_chunk["%d_%d" % (c, r)] = [round(float(v), 3) for v in np.median(Plin[y0:y0 + 1024, x0:x0 + 1536][a], axis=0)
                                               / np.median(Plin[y0:y0 + 1024, x0:x0 + 1536][bm], axis=0)]
    rep["shadow"] = {"painted_shadow_over_painted_light_linear": [round(float(v), 4) for v in mul],
                     "pixels": {"shadow": int(sh_set.sum()), "lit": int(lt_set.sum())}, "per_chunk_linear": per_chunk,
                     "v1_value_linear": [0.419, 0.548, 0.892]}
    man["shadow_mul"] = {"linear": [round(float(v), 4) for v in mul], "_": "measured: the pilot painting's shadowed flat open snow over its sunlit flat open snow (median, linear)"}
    # the painting, as is (paint_world_prep.py:241-244)
    shutil.copyfile(PAINTING, os.path.join(OUT, "painting.bin"))
    man["painting"] = {"file": "painting.bin", "sha256": sha, "px": [W, H], "_": "the stitched pilot paint-over's own PNG bytes"}
    man["ground_as_painted"] = dict(man["painting"])
    # the light map, half resolution (paint_world_prep.py:259-264)
    lr = litR.reshape(H // 2, 2, W // 2, 2).mean((1, 3))
    lp = os.path.join(OUT, "lit.bin")
    Image.fromarray((np.clip(lr, 0, 1) * 255.0 + 0.5).astype(np.uint8), "L").save(lp, format="PNG")
    man["lit"] = {"file": "lit.bin", "sha256": sha_file(lp), "px": [W // 2, H // 2],
                  "_": "the painting's direct sun as a share of flat sunlit ground's: lit_guide G x min(B / sin 55, 1), 8-bit, half resolution"}
    # the bakes (paint_world_prep.py:266-276), the pilot's own count
    BR = json.load(open(os.path.join(PILOT, "bake_report.json")))
    for pid, b in sorted(BR["pieces"].items()):
        if b.get("bake") == "FAILED":
            continue
        dst = os.path.join(OUT, "bakes", "%s.bin" % pid)
        shutil.copyfile(os.path.join(ROOT, "work", "bakes", "%s.png" % pid), dst)
        man["bakes"][pid] = {"file": "bakes/%s.bin" % pid, "sha256": sha_file(dst)}
    man["real_models_in_window"] = sorted(BR["pieces"].keys())
    rep["bakes"] = len(man["bakes"])
    # the heather: v1's counts, v1's greedy cover, on FLAT land tufts (paint_world_prep.py:278-348)
    HI = json.load(open(os.path.join(ROOT, "take", "build", "heather_instances.json")))
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
    json.dump({"_what": "the pilot's 3D heather: v1's counts (heather_instances.py) RE-PLACED on the painted flat-land tufts (v1's greedy cover), each coloured by the painting beneath it",
               "columns": ["x", "z", "height_m", "class (0 heather, 1 shrub)", "mul_r", "mul_g", "mul_b"],
               "painted_mean_linear": [round(float(v), 5) for v in mean], "placement": placed_px, "rows": rows},
              open(os.path.join(OUT, "heather.json"), "w"))
    man["heather"] = {"file": "heather.json", "count": len(rows), "albedo_mul": list(HEATHER_ALBEDO_MUL),
                      "_albedo_mul": "v1's calibrated grade (paint_world_prep.py:55), unchanged"}
    rep["heather"] = {"instances": len(rows), "placement": placed_px, "painted_mean_linear": [round(float(v), 5) for v in mean],
                      "tuft_px_per_spray_median": int(np.median(counts)),
                      "tufts_on_flat_land_share": round(float((tuft_px & flat).sum()) / max(float(tuft_px.sum()), 1.0), 4)}
    # the snow's depth grid (paint_world_prep.py:350-391): v1's SNOW_BY_CLASS on the bv2art class map, flat only
    cp = L["sim"]["classes_png"]
    CL = np.asarray(Image.open(os.path.join(os.path.dirname(LEVEL), cp["file"])))
    if CL.ndim == 3:
        CL = CL[..., 0]
    names = L["classes"]
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
    Uw = X * C47 - Z * S47                      # world xz -> (u, v) (the inverse of xz_of_uv)
    Vw = -X * S47 - Z * C47
    sx, sy = Uw, -Vw                            # bv2art sim = (u, -v)
    ci_ = np.clip(((sx - cp["extent_sim_m"]["x0"]) * cp["px_per_m"]).astype(int), 0, CL.shape[1] - 1)
    cj_ = np.clip(((sy - cp["extent_sim_m"]["y0"]) * cp["px_per_m"]).astype(int), 0, CL.shape[0] - 1)
    cls_grid = CL[cj_, ci_]
    hi_ = np.clip(((sx - ex["x0"]) * hf["px_per_m"]).astype(int), 0, Hf.shape[1] - 1)
    hj_ = np.clip(((sy - ex["y0"]) * hf["px_per_m"]).astype(int), 0, Hf.shape[0] - 1)
    flat_g = np.abs(Hf[hj_, hi_]) < 0.03
    rng = np.random.default_rng(91127)
    def smooth_noise(scale_m):
        n0 = rng.random((nx, nx))
        s_ = ndimage.gaussian_filter(n0, sigma=scale_m / cell, mode="wrap")
        return (s_ - s_.mean()) / (s_.std() * 6.0) + 0.5
    nv = np.clip(smooth_noise(1.4) * 0.7 + smooth_noise(0.45) * 0.3, 0.0, 1.0)
    mulg = np.zeros((nx, nx))
    trod = np.zeros((nx, nx))
    for k_, nm in enumerate(names):
        sc = BV2ART_TO_SNOW.get(nm)
        if sc is None:
            continue
        wk = ((cls_grid == k_) & flat_g).astype(np.float64)
        m_, patch, tr = SNOW_BY_CLASS[sc]
        keep = np.clip((nv - (patch - 0.08)) / 0.16, 0.0, 1.0) if patch > 0 else 1.0
        keep = keep * keep * (3 - 2 * keep) if patch > 0 else 1.0
        mulg += wk * m_ * keep
        trod += wk * tr
    gridp = os.path.join(OUT, "snow_grid.bin")
    np.concatenate([mulg.astype("<f4").ravel(), trod.astype("<f4").ravel()]).tofile(gridp)
    man["snow"] = {"area_xz": area, "field_px": 768, "trail_px": 1024,
                   "grid": {"file": "snow_grid.bin", "sha256": sha_file(gridp), "origin_xz": [gx0, gz0], "cell_m": cell,
                            "nx": nx, "nz": nx, "_layout": "float32 little-endian: nx*nz depth multipliers (row = z), then nx*nz trodden amounts"},
                   "_": "v1's SNOW_BY_CLASS on the bv2art class map, flat ground only; the field covers the pilot window + 1.5 m (world xz, square)"}
    rep["snow"] = {"area_xz": area, "grid_cells": nx * nx, "mean_mul": round(float(mulg.mean()), 4),
                   "flat_share": round(float(flat_g.mean()), 4)}
    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    json.dump(rep, open(os.path.join(PILOT, "painted_prep.json"), "w"), indent=1)
    print(json.dumps({k: rep[k] for k in ("tufts_self_test", "shadow", "heather", "snow")}, indent=1)[:3000])


main()
