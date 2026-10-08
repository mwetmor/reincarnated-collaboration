#!/usr/bin/env python3
"""BV2F PT R-C9-261: PILOT REPAINT 4 review, BEFORE any take/bake/build. Read-only on the canvases and paintings.
    python3 fid/pt/tools/ps4_review.py contact            -> fid/pt/ps4_dry/contact_sheet.jpg (the 9 canvases, 1/3 scale)
    python3 fid/pt/tools/ps4_review.py seams              -> P5(c)-style all-class TONE excess (p5c_boundary.py's measure) +
                                                             an all-class TEXTURE excess (same geometry, detail amplitude),
                                                             PS4 dry stitch vs rp3 (ps3a_dry/painting.png); 1:1 join crops
    python3 fid/pt/tools/ps4_review.py snow_ice           -> PH s46 snow measure (snow_parity.chunk_stats, imported read-only)
                                                             on PS4 and, as a same-mask control, on rp3; the mere ice vs
                                                             sketch A's frozen median (calibration s38: (72.9, -1.0, -9.4), bar dE 9.40)
Masks: the PS4 pins (fid/pt/pilot/{ids,class}_art_pinned_ps4.png): snow = class snow on ground ids, less v1's tuft classifier;
ice = class ice on ground ids, less tufts, eroded 3 px, gated b* <= 2 (s38)."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
Image.MAX_IMAGE_PIXELS = None
C9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
FID = C9 + "/barrow_v2/fid"
A9 = C9 + "/artifacts"
OUT = FID + "/pt/ps4_dry"
PIN = FID + "/pt/pilot"
PFX = "BV2F-PS4"
W, H = 4096, 2560
CHUNKS = [("%d_%d" % (c, r), (1280 * c, 768 * r, 1280 * c + 1536, 768 * r + 1024)) for r in range(3) for c in range(3)]
os.makedirs(OUT, exist_ok=True)


def src(k):
    for d in ("%s-%s-r1" % (PFX, k), "%s-%s" % (PFX, k)):
        p = "%s/%s/%s-%s.png" % (A9, d, PFX, k)
        if os.path.exists(p):
            return p


def lab(P):
    x = P.astype(np.float64) / 255.0
    c = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def contact():
    s = 3
    cw, ch = 1536 // s, 1024 // s
    sheet = Image.new("RGB", (cw * 3 + 16, ch * 3 + 16), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    rec = {}
    for r in range(3):
        for c in range(3):
            k = "%d_%d" % (c, r)
            p = src(k)
            rec[k] = os.path.relpath(p, A9) if p else None
            if p:
                sheet.paste(Image.open(p).convert("RGB").resize((cw, ch), Image.LANCZOS), (c * (cw + 8), r * (ch + 8)))
                d.text((c * (cw + 8) + 6, r * (ch + 8) + 6), k + (" r1" if "-r1" in p else ""), fill=(255, 0, 0))
    sheet.save(OUT + "/contact_sheet.jpg", quality=90)
    json.dump(rec, open(OUT + "/contact_sheet.json", "w"), indent=1)
    print("contact", rec)


def boundaries():
    out = []
    for r in range(3):
        for c in range(3):
            k = "%d_%d" % (c, r)
            if c >= 1:
                out.append(("%s|x%d" % (k, 1280 * c + 256), "x", 1280 * c + 256, 768 * r, min(768 * r + 1024, H)))
            if r >= 1:
                out.append(("%s|y%d" % (k, 768 * r + 256), "y", 768 * r + 256, 1280 * c, min(1280 * c + 1536, W)))
    return out


def seam_measures(P):
    """per 128-px segment: TONE = low-pass (sigma 6) Lab dE across the line (bands 8..16 px) minus the median at parallel
    offsets +-32/64/96 (p5c_boundary.py's measure, re-implemented on the same geometry); TEXTURE = |log2| ratio of the detail
    amplitude (L* minus Gaussian sigma 3, local RMS) across the line, minus the same at the parallel offsets."""
    LB = lab(P)
    LF = np.stack([ndimage.gaussian_filter(LB[..., i], 6) for i in range(3)], -1)
    D = LB[..., 0] - ndimage.gaussian_filter(LB[..., 0], 3)
    R = np.sqrt(ndimage.gaussian_filter(D * D, 4))
    res = {}
    for name, ax, pos, a0, a1 in boundaries():
        segs = []
        for s0 in range(a0, a1 - 127, 128):
            s1 = s0 + 128

            def tone(p):
                if ax == "x":
                    return float(np.linalg.norm(LF[s0:s1, p - 16:p - 8].mean((0, 1)) - LF[s0:s1, p + 8:p + 16].mean((0, 1))))
                return float(np.linalg.norm(LF[p - 16:p - 8, s0:s1].mean((0, 1)) - LF[p + 8:p + 16, s0:s1].mean((0, 1))))

            def tex(p):
                if ax == "x":
                    u, v = R[s0:s1, p - 16:p - 4].mean(), R[s0:s1, p + 4:p + 16].mean()
                else:
                    u, v = R[p - 16:p - 4, s0:s1].mean(), R[p + 4:p + 16, s0:s1].mean()
                return abs(float(np.log2(max(u, 1e-3) / max(v, 1e-3))))
            lim = W if ax == "x" else H
            offs = [o for o in (-96, -64, -32, 32, 64, 96) if 24 <= pos + o < lim - 24]
            segs.append({"at": [s0, s1], "tone_excess": round(tone(pos) - float(np.median([tone(pos + o) for o in offs])), 2),
                         "texture_excess": round(tex(pos) - float(np.median([tex(pos + o) for o in offs])), 3)})
        res[name] = {"max_tone_excess": max(s["tone_excess"] for s in segs), "tone_segments_over_3": sum(s["tone_excess"] > 3 for s in segs),
                     "max_texture_excess": max(s["texture_excess"] for s in segs), "texture_segments_over_0.5": sum(s["texture_excess"] > 0.5 for s in segs),
                     "segments": segs}
    return res


def seams():
    ps4 = np.asarray(Image.open(OUT + "/painting.png").convert("RGB"))
    rp3 = np.asarray(Image.open(FID + "/pt/ps3a_dry/painting.png").convert("RGB"))
    a, b = seam_measures(ps4), seam_measures(rp3)
    rows = {}
    for k in a:
        rows[k] = {"ps4": {kk: v for kk, v in a[k].items() if kk != "segments"}, "rp3": {kk: v for kk, v in b[k].items() if kk != "segments"}}
        print("%-12s tone ps4 %6.2f (%d>3)  rp3 %6.2f (%d>3) | texture ps4 %.3f (%d>0.5)  rp3 %.3f (%d>0.5)" % (
            k, a[k]["max_tone_excess"], a[k]["tone_segments_over_3"], b[k]["max_tone_excess"], b[k]["tone_segments_over_3"],
            a[k]["max_texture_excess"], a[k]["texture_segments_over_0.5"], b[k]["max_texture_excess"], b[k]["texture_segments_over_0.5"]))
    # 1:1 crops at each boundary's worst tone segment, PS4 only (for the eye)
    os.makedirs(OUT + "/joins", exist_ok=True)
    crops = {}
    for name, ax, pos, a0, a1 in boundaries():
        s = max(a[name]["segments"], key=lambda q: q["tone_excess"])
        m = (s["at"][0] + s["at"][1]) // 2
        x, y = (pos, m) if ax == "x" else (m, pos)
        x0 = int(np.clip(x - 192, 0, W - 384)); y0 = int(np.clip(y - 192, 0, H - 384))
        p = "%s/joins/%s_x%d_y%d.png" % (OUT, name.replace("|", "_"), x0, y0)
        Image.fromarray(ps4[y0:y0 + 384, x0:x0 + 384]).save(p)
        crops[name] = os.path.relpath(p, FID)
    json.dump({"_what": "R-C9-261 PS4 dry-stitch seams (all-class P5(c)-style tone + texture excess), vs rp3 (ps3a_dry, accepted R-C9-252)",
               "boundaries": rows, "detail_ps4": a, "join_crops_1to1": crops}, open(OUT + "/seams.json", "w"), indent=1)


def masks():
    sys.path.insert(0, FID + "/ph/harness")
    import importlib.util
    gm = json.load(open(PIN + "/pins.json"))
    import subprocess
    man = json.loads(subprocess.check_output(["git", "-C", FID, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json" % gm["lv_commit"]]))
    ids = np.asarray(Image.open(PIN + "/ids_art_pinned_ps4.png").convert("RGB"))[:H, :W].astype(np.int64)
    gid = (ids[..., 0] << 16) | (ids[..., 1] << 8) | ids[..., 2]
    ground = np.isin(gid, [int(k) for k, v in man["id_table"].items() if v["id"].startswith(("ground_", "carved_"))])
    cls = np.asarray(Image.open(PIN + "/class_art_pinned_ps4.png"))[:H, :W]
    ni = {n: i for i, n in enumerate(man["class"]["classes"])}
    spec = importlib.util.spec_from_file_location("pw_v1_readonly", C9 + "/barrow_full/tools/paint_world_prep.py")
    pw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pw)
    return ground, cls, ni, pw


def snow_ice():
    sys.path.insert(0, FID + "/ph/harness")
    import snow_parity as SP   # PH's s46 instrument, read-only
    ground, cls, ni, pw = masks()
    ph = json.load(open(FID + "/ph/results/pilot3/snow_parity.json"))
    res = {"_what": "R-C9-261 snow spot check (PH s46 chunk_stats, imported) + mere ice vs sketch A (s38); masks = PS4 pins",
           "v1_and_rp3_as_PH_published": {k: {kk: ph["summary"][k][kk] for kk in ("v1_mean", "v1_min", "v1_max", "pilot_median")}
                                          for k in ("lit_a", "lit_b", "shadow_a", "shadow_share", "blobs_per_m2", "blob_area_median_m2", "blob_cover", "blob_edge_width_px", "L_std") if k in ph["summary"]}}
    for name, path in (("ps4", OUT + "/painting.png"), ("rp3_same_mask", FID + "/pt/ps3a_dry/painting.png")):
        P = np.asarray(Image.open(path).convert("RGB"))[:H, :W]
        h, s = pw.tuft_classes(P.astype(np.uint8), ground)
        tufts = ndimage.binary_opening(h | s, iterations=1)
        snow = ground & ~tufts & (cls == ni["snow"])
        L = lab(P)
        per = SP.run(name, P, snow, CHUNKS)
        for r in per.values():
            r.pop("_spec", None)
        # peach-pixel share of LIT snow (a* > 2 and b* > 4), per chunk, as in the R-C9-256 diff
        for k, (x0, y0, x1, y1) in CHUNKS:
            if k in per:
                m = ndimage.binary_erosion(snow[y0:y1, x0:x1], iterations=3)
                Lc = L[y0:y1, x0:x1]
                lit = m & (Lc[..., 0] >= np.median(Lc[..., 0][m]))
                per[k]["peach_px_share_of_lit"] = round(float(((Lc[..., 1] > 2) & (Lc[..., 2] > 4))[lit].mean()), 3)
        med = {kk: round(float(np.median([r[kk] for r in per.values() if r.get(kk) is not None])), 4)
               for kk in ("lit_a", "lit_b", "shadow_a", "shadow_share", "blobs_per_m2", "blob_area_median_m2", "blob_cover", "blob_edge_width_px", "L_std", "peach_px_share_of_lit")}
        ice = ndimage.binary_erosion(ground & ~tufts & (cls == ni["ice"]), iterations=3) & (L[..., 2] <= 2)
        ic = {}
        for k, (x0, y0, x1, y1) in CHUNKS:
            m = ice[y0:y1, x0:x1]
            if m.sum() >= 20000:
                v = np.median(L[y0:y1, x0:x1][m], 0)
                ic[k] = {"px": int(m.sum()), "lab_median": [round(float(x), 1) for x in v],
                         "dE_vs_sketchA": round(float(np.linalg.norm(v - np.array([72.9, -1.0, -9.4]))), 2)}
        res[name] = {"snow_chunk_medians": med, "snow_chunks": per, "ice_vs_sketchA": ic,
                     "ice_worst_dE": max(v["dE_vs_sketchA"] for v in ic.values()) if ic else None}
        print(name, "snow", json.dumps(med))
        print(name, "ice", {k: (v["lab_median"], v["dE_vs_sketchA"]) for k, v in ic.items()})
    res["sketchA_ice_ref"] = {"lab_median": [72.9, -1.0, -9.4], "bar_dE": 9.40, "source": "calibration.md s38 (frozen)"}
    json.dump(res, open(OUT + "/snow_ice.json", "w"), indent=1)


if __name__ == "__main__":
    {"contact": contact, "seams": seams, "snow_ice": snow_ice}[sys.argv[1]]()
