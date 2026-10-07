#!/usr/bin/env python3
"""R-C9-194 P4 FORENSIC (0 images; no bar changes): is the pilot's paler / less-blue ice and the cooler snow in chunks
0_2 / 1_2 coming from the GUIDE or the PAINT?
  (a) guide pixels: v1's guide at the tarn vs the bv2art guide (as pinned for the pilot) at the mere -- Lab, class tint,
      the guide's own light (snow as the reference), area and shape;
  (b) painted: v1's tarn vs the pilot's mere -- Lab and P4's Hellinger distance; paint transfer (painted - guide);
  (c) snow: the same per chunk, 0_2 / 1_2 vs the neighbouring chunks and v1;
  (d) sketch A's own mere (barrow_v2/sites/BV3r2-A.png, MERE polygon of make_bv2art.py) -- Lab vs the pilot ice and v1 tarn.
-> results/pilot/p4_forensic.json + figures results/pilot/p4_forensic_{ice,snow}.jpg (3 panels each).
Masks: P4's own (pilot: guide class map on ground less tufts; v1: p4_texture.v1_classes). Erosion 3 px as P4."""
import importlib.util
import math
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p4_texture as T
import pilot_harness as PHn

OUT = PH / "results/pilot"
SK = B2 / "sites/BV3r2-A.png"


def lab_stats(lab, m):
    v = lab[m]
    return {"px": int(m.sum()), "median": np.median(v, 0).round(1).tolist(), "p10": np.percentile(v, 10, 0).round(1).tolist(),
            "p90": np.percentile(v, 90, 0).round(1).tolist(), "chroma_median": round(float(np.median(np.hypot(v[:, 1], v[:, 2]))), 1)}


def shape(m, ppm_x=PPM_V1, ppm_y=80.3076):
    """ground area (m²) of a plate-px mask; bbox in m; compactness 4πA/P² (perimeter from the boundary px, in m)"""
    a = m.sum() / (ppm_x * ppm_y)
    ys, xs = np.where(m)
    edge = m & ~ndimage.binary_erosion(m)
    per = edge.sum() / math.sqrt(ppm_x * ppm_y)
    return {"area_m2": round(float(a), 1), "bbox_m": [round((xs.max() - xs.min()) / ppm_x, 1), round((ys.max() - ys.min()) / ppm_y, 1)],
            "compactness": round(float(4 * math.pi * a / max(per, 1e-6) ** 2), 3)}


def hel(lab, m, ref_hist):
    return round(T.hellinger(T.lab_hist(lab[m]), ref_hist), 3)


def crop_at(img, m, size=512):
    ys, xs = np.where(ndimage.binary_erosion(m, iterations=size // 4))
    if not len(ys):
        ys, xs = np.where(m)
    i = len(ys) // 2
    y, x = int(ys[i]), int(xs[i])
    H, W = img.shape[:2]
    y0, x0 = min(max(y - size // 2, 0), H - size), min(max(x - size // 2, 0), W - size)
    return (y0, x0)


def panel(guide, paint, yx, title, stats_g, stats_p, size=512):
    y0, x0 = yx
    g = np.clip(guide[y0:y0 + size, x0:x0 + size], 0, 255).astype(np.uint8)
    p = np.clip(paint[y0:y0 + size, x0:x0 + size], 0, 255).astype(np.uint8)
    pan = Image.new("RGB", (size, 2 * size + 60), (255, 255, 255))
    pan.paste(Image.fromarray(g), (0, 30))
    pan.paste(Image.fromarray(p), (0, size + 60))
    d = ImageDraw.Draw(pan)
    d.text((4, 4), title, fill=(0, 0, 0))
    d.text((4, 16), "guide  Lab %s" % stats_g, fill=(0, 0, 0))
    d.text((4, size + 34), "painted  Lab %s" % stats_p, fill=(0, 0, 0))
    return pan


def sketch_mere():
    spec = importlib.util.spec_from_file_location("mk", FID / "lv/tools/make_bv2art.py")
    src = open(FID / "lv/tools/make_bv2art.py").read()
    i = src.index("MERE = [")
    MERE = eval(src[i + 7:src.index("\n", i)])
    img = load_rgb(SK)
    im = Image.new("L", (img.shape[1], img.shape[0]), 0)
    ImageDraw.Draw(im).polygon(MERE, fill=1)
    m = ndimage.binary_erosion(np.asarray(im).astype(bool), iterations=6)
    return img, m, MERE


def main():
    # ---------------- v1
    masks_v1, static_v1 = T.v1_classes()
    per = T.v1_pool(None, masks_v1, static_v1)
    V1P = load_rgb(BF / "paint/barrow_full_painted.png")
    V1G = load_rgb(BF / "paint/barrow_full_guide.png")
    lv1p, lv1g = rgb_to_lab(V1P), rgb_to_lab(V1G)
    v1 = {c: ndimage.binary_erosion(masks_v1[c], iterations=3) for c in ("ice", "snow")}
    # ---------------- pilot
    P = PHn.painting()
    G = load_rgb(FID / "pt/pilot/guide_art_pinned.png")[:PHn.H, :PHn.W]
    lp, lg = rgb_to_lab(P), rgb_to_lab(G)
    cls, names = PHn.class_map()
    ni = {n: i for i, n in enumerate(names)}
    gr = PHn.ground_mask() & ~PHn.tufts()
    pm = {c: ndimage.binary_erosion(gr & (cls == ni[c]), iterations=3) for c in ("ice", "snow")}
    ref = {c: T.pooled(per, c)[0] for c in ("ice", "snow")}
    tints = jload(BF / "barrow_full_layout.json")["tints_srgb"]
    tints2 = jload(FID / "lv/guide_art/guide_manifest.json")["tints_srgb"]
    R = {"_what": __doc__.split("\n")[0], "tints_srgb": {"v1_layout": {k: tints[k] for k in ("ice", "snow")},
                                                         "bv2art_guide": {k: tints2[k] for k in ("ice", "snow")}},
         "brief_text": "IDENTICAL ice wording in both briefs ('PALE BLUE-GREY = the frozen tarn/mere, flat lapis-blue ice with pale cracks'), same IMAGE 2 ref (T10C-barrow_a)"}
    # (a)+(b) ice
    ice = {"v1_tarn": {"guide": lab_stats(lv1g, v1["ice"]), "painted": lab_stats(lv1p, v1["ice"]), "shape": shape(masks_v1["ice"]),
                       "painted_hellinger_to_v1_pool": hel(lv1p, v1["ice"], ref["ice"])},
           "pilot_mere": {"guide": lab_stats(lg, pm["ice"]), "painted": lab_stats(lp, pm["ice"]), "shape": shape(gr & (cls == ni["ice"])),
                          "painted_hellinger_to_v1_pool": hel(lp, pm["ice"], ref["ice"])}}
    for k, (lgx, lpx, m) in {"v1_tarn": (lv1g, lv1p, v1["ice"]), "pilot_mere": (lg, lp, pm["ice"])}.items():
        ice[k]["transfer_painted_minus_guide_median"] = (np.median(lpx[m], 0) - np.median(lgx[m], 0)).round(1).tolist()
    # the guide's own light: open snow (lit, the reference) and ice relative to it
    for k, (lgx, ms, mi) in {"v1_tarn": (lv1g, v1["snow"], v1["ice"]), "pilot_mere": (lg, pm["snow"], pm["ice"])}.items():
        ice[k]["guide_snow_L_median"] = round(float(np.median(lgx[ms][:, 0])), 1)
        ice[k]["guide_ice_minus_snow_L"] = round(float(np.median(lgx[mi][:, 0]) - np.median(lgx[ms][:, 0])), 1)
    # (d) sketch A
    SKI, skm, MERE = sketch_mere()
    lsk = rgb_to_lab(SKI)
    sk = lab_stats(lsk, skm)
    hs = T.lab_hist(lsk[skm])
    ice["sketch_A_mere"] = {"lab": sk, "hellinger_to_pilot_painted_ice": round(T.hellinger(hs, T.lab_hist(lp[pm["ice"]])), 3),
                            "hellinger_to_v1_painted_tarn": round(T.hellinger(hs, ref["ice"]), 3),
                            "dE76_median_to_pilot_ice": round(float(np.linalg.norm(np.array(sk["median"]) - np.array(ice["pilot_mere"]["painted"]["median"]))), 1),
                            "dE76_median_to_v1_tarn": round(float(np.linalg.norm(np.array(sk["median"]) - np.array(ice["v1_tarn"]["painted"]["median"]))), 1),
                            "polygon_px": MERE, "note": "sketch A is a JPEG-like concept sketch at its own exposure; not a bar (M2' input)"}
    R["ice"] = ice
    # (c) snow per chunk
    snow = {"v1_whole": {"guide": lab_stats(lv1g, v1["snow"]), "painted": lab_stats(lv1p, v1["snow"])}, "pilot_chunks": {}}
    lit = PHn.np.asarray(Image.open(__import__("io").BytesIO(open(BF / "godot/data/bv2f/pilot/painted/lit.bin", "rb").read())).convert("L")
                         .resize((PHn.W, PHn.H), Image.BILINEAR)) / 255.0
    for key, (x0, y0, x1, y1) in PHn.CHUNKS:
        m = np.zeros_like(pm["snow"])
        m[y0:y1, x0:x1] = pm["snow"][y0:y1, x0:x1]
        if m.sum() < 20000:
            continue
        snow["pilot_chunks"][key] = {"guide": lab_stats(lg, m), "painted": lab_stats(lp, m),
                                     "transfer_painted_minus_guide_median": (np.median(lp[m], 0) - np.median(lg[m], 0)).round(1).tolist(),
                                     "painted_hellinger_to_v1_pool": hel(lp, m, ref["snow"]),
                                     "guide_lit_share_gt_0.8": round(float((lit[m] > 0.8).mean()), 3)}
    R["snow"] = snow
    # verdict helpers (numbers only; the reading is in calibration.md § 27)
    dump(R, str(OUT / "p4_forensic.json"))
    # ---------------- figures: 3 panels per class (guide over painted at the same px)
    f = lambda s: "(%.0f, %.1f, %.1f)" % tuple(s["median"])
    a = panel(V1G, V1P, crop_at(V1P, v1["ice"]), "v1 tarn (guide / painted)", f(ice["v1_tarn"]["guide"]), f(ice["v1_tarn"]["painted"]))
    b = panel(G, P, crop_at(P, pm["ice"]), "pilot mere (guide / painted)", f(ice["pilot_mere"]["guide"]), f(ice["pilot_mere"]["painted"]))
    ys, xs = np.where(skm)
    y0, x0 = max(int(ys.mean()) - 128, 0), max(int(xs.mean()) - 256, 0)
    skc = Image.fromarray(np.clip(SKI[y0:y0 + 256, x0:x0 + 512], 0, 255).astype(np.uint8)).resize((512, 256))
    c = Image.new("RGB", (512, 2 * 512 + 60), (255, 255, 255))
    c.paste(skc, (0, 30))
    ImageDraw.Draw(c).text((4, 4), "sketch A mere (look of record; 2x)", fill=(0, 0, 0))
    ImageDraw.Draw(c).text((4, 16), "Lab %s" % f(sk), fill=(0, 0, 0))
    fig = Image.new("RGB", (3 * 512 + 48, 2 * 512 + 60), (255, 255, 255))
    for i, pnl in enumerate((a, b, c)):
        fig.paste(pnl, (i * (512 + 24), 0))
    fig.save(OUT / "p4_forensic_ice.jpg", quality=88)
    sc = snow["pilot_chunks"]
    def chunk_mask(k):
        x0, y0, x1, y1 = dict(PHn.CHUNKS)[k]
        m = np.zeros_like(pm["snow"])
        m[y0:y1, x0:x1] = pm["snow"][y0:y1, x0:x1]
        return m
    a = panel(V1G, V1P, crop_at(V1P, v1["snow"]), "v1 snow (guide / painted)", f(snow["v1_whole"]["guide"]), f(snow["v1_whole"]["painted"]))
    b = panel(G, P, crop_at(P, chunk_mask("2_1")), "pilot snow, chunk 2_1 (passes)", f(sc["2_1"]["guide"]), f(sc["2_1"]["painted"]))
    c = panel(G, P, crop_at(P, chunk_mask("1_2")), "pilot snow, chunk 1_2 (fails)", f(sc["1_2"]["guide"]), f(sc["1_2"]["painted"]))
    fig = Image.new("RGB", (3 * 512 + 48, 2 * 512 + 60), (255, 255, 255))
    for i, pnl in enumerate((a, b, c)):
        fig.paste(pnl, (i * (512 + 24), 0))
    fig.save(OUT / "p4_forensic_snow.jpg", quality=88)
    return R


if __name__ == "__main__":
    R = main()
    print(json.dumps({k: R[k] for k in ("ice", "snow")}, indent=1, default=str)[:7000])
