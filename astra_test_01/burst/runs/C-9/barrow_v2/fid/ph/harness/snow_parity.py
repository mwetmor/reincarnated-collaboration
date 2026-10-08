#!/usr/bin/env python3
"""R-C9-256 SNOW PARITY investigation (0 images, no Godot): v1 snow vs pilot-3 snow, same class (open snow on ground, tufts
removed, eroded 3 px), same zoom (both paintings are play-camera plates at 100.6 px/m across, 80.3 px/m up-screen).
Per paint chunk (v1: its 16; pilot: its 9), measured and placed against v1's chunk-to-chunk spread:
  PALETTE   Lab median / std; LIT snow (L >= chunk median L) mean a*, b* (the peach cast); SHADOW px (L <= median - 6 and
            b* <= lit b* - 3) mean a*, b* and their offset from lit (shadow hue).
  BLOBS     shadow mask (on Lab blurred sigma 1.5, opened 1 px) -> connected blobs >= 20 px: count per m2 of snow, area
            distribution (median, p90, m2), share of snow covered; EDGE SHARPNESS = blob contrast (lit L - blob L) over the
            mean |grad L*| on the blob boundary = an edge width in px (small = crisp).
  GRAIN     P4's spectrum_shape RMS vs v1's pooled snow spectrum; P4's cellular-mosaic detector (cell_excess p95).
-> results/pilot3/snow_parity.json; sheet results/pilot3/snow_parity_sheet.jpg (v1 | pilot, 6 patches each, 1:1 and 2x)."""
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p4_texture as T
import pilot_harness as PHn

M2 = PPM_V1 * 80.3076            # px per m2 of ground
OUT = PH / __import__("os").environ.get("PH_PILOT_OUT", "results/pilot3")


def chunk_stats(img, lab, mask, gray):
    m = ndimage.binary_erosion(mask, iterations=3)
    if m.sum() < 20000:
        return None
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    medL = float(np.median(L[m]))
    lit = m & (L >= medL)
    litb, lita = float(b[lit].mean()), float(a[lit].mean())
    labs = np.stack([ndimage.gaussian_filter(lab[..., k], 1.5) for k in range(3)], -1)
    sh = m & (labs[..., 0] <= medL - 6) & (labs[..., 2] <= litb - 3)
    sh = ndimage.binary_opening(sh, iterations=1)
    lbl, n = ndimage.label(sh)
    sizes = np.bincount(lbl.ravel())[1:]
    keep = np.where(sizes >= 20)[0] + 1
    blob = np.isin(lbl, keep)
    areas = sizes[sizes >= 20] / M2
    snow_m2 = m.sum() / M2
    gy, gx = np.gradient(ndimage.gaussian_filter(L, 1.0))
    gm = np.hypot(gx, gy)
    edge = blob & ~ndimage.binary_erosion(blob)
    contrast = float(L[lit].mean() - L[blob].mean()) if blob.any() else None
    ew = (contrast / float(gm[edge].mean())) if (blob.any() and edge.any() and gm[edge].mean() > 0) else None
    shade = m & ~blob
    res = {"snow_px": int(m.sum()), "L_median": round(medL, 2), "L_std": round(float(L[m].std()), 2),
           "a_median": round(float(np.median(a[m])), 2), "b_median": round(float(np.median(b[m])), 2),
           "lit_a": round(lita, 2), "lit_b": round(litb, 2),
           "shadow_share": round(float(sh.sum() / m.sum()), 4),
           "shadow_a": round(float(a[sh].mean()), 2) if sh.any() else None, "shadow_b": round(float(b[sh].mean()), 2) if sh.any() else None,
           "shadow_dL": round(float(L[sh].mean() - L[lit].mean()), 2) if sh.any() else None,
           "shadow_db_vs_lit": round(float(b[sh].mean() - litb), 2) if sh.any() else None,
           "shadow_da_vs_lit": round(float(a[sh].mean() - lita), 2) if sh.any() else None,
           "blobs_per_m2": round(float(len(areas) / snow_m2), 3), "blob_area_median_m2": round(float(np.median(areas)), 4) if len(areas) else None,
           "blob_area_p90_m2": round(float(np.percentile(areas, 90)), 4) if len(areas) else None,
           "blob_cover": round(float(blob.sum() / m.sum()), 4), "blob_contrast_L": None if contrast is None else round(contrast, 2),
           "blob_edge_width_px": None if ew is None else round(ew, 2)}
    st = T.stats(img, {"snow": mask}, mask)
    res["_spec"] = st[0]["snow"]["spec"] if "snow" in st[0] else None
    res["cell_p95"] = None if st[1] is None else round(st[1], 3)
    return res


def run(name, img, mask, chunks):
    lab = rgb_to_lab(img)
    gray = luma(img)
    out = {}
    for key, (x0, y0, x1, y1) in chunks:
        r = chunk_stats(img[y0:y1, x0:x1], lab[y0:y1, x0:x1], mask[y0:y1, x0:x1], gray[y0:y1, x0:x1])
        if r:
            out[key] = r
    return out


def main():
    masks_v1, static_v1 = T.v1_classes()
    V = load_rgb(BF / "paint/barrow_full_painted.png")
    v1 = run("v1", V, masks_v1["snow"], T.v1_chunks())
    P = PHn.painting()
    cls, names = PHn.class_map()
    ni = {n: i for i, n in enumerate(names)}
    pm = PHn.ground_mask() & ~PHn.tufts() & (cls == ni["snow"])
    pl = run("pilot3", P, pm, PHn.CHUNKS)
    pool = np.mean([r["_spec"] for r in v1.values() if r["_spec"] is not None], 0)
    for d in (v1, pl):
        for r in d.values():
            r["spec_rms_vs_v1_pool"] = None if r["_spec"] is None else round(float(np.sqrt(np.mean((np.array(r["_spec"]) - pool) ** 2))), 4)
            del r["_spec"]
    keys = [k for k in next(iter(v1.values())) if k != "snow_px"]
    summ = {}
    for k in keys:
        vv = [r[k] for r in v1.values() if r[k] is not None]
        pv = [r[k] for r in pl.values() if r[k] is not None]
        if not vv or not pv:
            continue
        mu, sd = float(np.mean(vv)), float(np.std(vv)) or 1e-9
        summ[k] = {"v1_min": round(min(vv), 4), "v1_max": round(max(vv), 4), "v1_mean": round(mu, 4), "v1_sd": round(sd, 4),
                   "pilot_median": round(float(np.median(pv)), 4), "pilot_min": round(min(pv), 4), "pilot_max": round(max(pv), 4),
                   "pilot_chunks_outside_v1_range": sum(not (min(vv) <= x <= max(vv)) for x in pv), "pilot_n": len(pv),
                   "z_of_pilot_median": round((float(np.median(pv)) - mu) / sd, 2)}
    res = {"_what": __doc__.split("\n")[0], "v1_chunks": v1, "pilot3_chunks": pl, "summary": summ}
    dump(res, str(OUT / "snow_parity.json"))
    sheet(V, masks_v1["snow"], P, pm)
    return res


def patches(img, mask, n=6, size=256, seed=256):
    """n patches of open snow, as clean as the plate allows: the strictest snow-coverage threshold (0.97 -> 0.80) and
    spacing (900 x 600 -> 450 x 300 px) that yields n, so pilot 3's smaller, more broken snow still gives 6"""
    cov = ndimage.uniform_filter(ndimage.binary_erosion(mask, iterations=3).astype(np.float32), size)
    rng = np.random.default_rng(seed)
    for thr, sx, sy in ((0.97, 900, 600), (0.95, 700, 450), (0.90, 600, 400), (0.85, 450, 300), (0.80, 450, 300)):
        m = cov >= thr
        ys, xs = np.where(m[size // 2:-size // 2:32, size // 2:-size // 2:32])
        ys, xs = ys * 32 + size // 2, xs * 32 + size // 2
        picked = []
        for i in rng.permutation(len(ys)):
            y, x = ys[i], xs[i]
            if all(abs(y - py) > sy or abs(x - px) > sx for py, px in picked):
                picked.append((y, x))
            if len(picked) == n:
                break
        if len(picked) == n:
            break
    return [np.clip(img[y - size // 2:y + size // 2, x - size // 2:x + size // 2], 0, 255).astype(np.uint8) for y, x in picked], picked, thr


def sheet(V, vm, P, pm):
    pv, cv, tv = patches(V, vm)
    pp, cp, tp = patches(P, pm)
    print("patch snow-coverage thresholds: v1 %.2f, pilot %.2f" % (tv, tp))
    S, G = 256, 12
    W_ = 6 * S + 7 * G
    H_ = 40 + 2 * (S + G + 24) + 40 + 2 * (2 * 128 + G + 24)
    sh = Image.new("RGB", (W_, H_ + 40), (255, 255, 255))
    d = ImageDraw.Draw(sh)
    d.text((G, 8), "SNOW PARITY (R-C9-256): open snow, tufts removed; both plates 100.6 px/m (play zoom = 1:1). Rows: v1 | pilot 3", fill=(0, 0, 0))
    y = 40
    for lbl, ps, cs in (("v1 (T10BF) 1:1", pv, cv), ("pilot 3 (PS3A) 1:1", pp, cp)):
        d.text((G, y), lbl + "   centres " + ", ".join("(%d,%d)" % (x, yy) for yy, x in cs), fill=(0, 0, 0))
        for i, im in enumerate(ps):
            sh.paste(Image.fromarray(im), (G + i * (S + G), y + 18))
        y += S + G + 24
    d.text((G, y + 10), "2x magnified (central 128 px of each patch above)", fill=(0, 0, 0))
    y += 40
    for lbl, ps in (("v1 2x", pv), ("pilot 3 2x", pp)):
        d.text((G, y), lbl, fill=(0, 0, 0))
        for i, im in enumerate(ps):
            c = Image.fromarray(im[64:192, 64:192]).resize((256, 256), Image.NEAREST)
            sh.paste(c, (G + i * (S + G), y + 18))
        y += 2 * 128 + G + 24
    sh.save(OUT / "snow_parity_sheet.jpg", quality=92)


if __name__ == "__main__":
    r = main()
    for k, v in r["summary"].items():
        print("%-22s v1 %8.3f..%8.3f (mean %7.3f sd %6.3f) | pilot med %8.3f [%8.3f..%8.3f] outside %d/%d z %6.2f" % (
            k, v["v1_min"], v["v1_max"], v["v1_mean"], v["v1_sd"], v["pilot_median"], v["pilot_min"], v["pilot_max"],
            v["pilot_chunks_outside_v1_range"], v["pilot_n"], v["z_of_pilot_median"]))
