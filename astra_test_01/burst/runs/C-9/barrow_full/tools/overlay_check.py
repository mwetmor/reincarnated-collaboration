#!/usr/bin/env python3
"""C-9 T10-2 step 5 -- THE OVERLAY CHECK, PER CHUNK: the assembled Barrow at the guide camera,
set against the painting, pixel for pixel. drax.

    python3 tools/overlay_check.py [--capture captures/painted] [--variant inpainted]

Reads captures/painted/guide_<variant>.png and heather_mask.png (godot/tools/capture_painted.gd
--guide: the painted scene without him, 5376 x 3328, the wind held still) and the painting.

THE CLASSES, off the painting's own pixels (step 3's instruments, unchanged):
  the pieces by the ID render (the assembled scene's geometry IS the blockout's, so the ID render
  is exact for it): stones (baked: the ring, the posts, the lintel), kit + raven (baked: cairns,
  logs, grave markers, raven), rock (projected: 18 outcrops + 10 shore rocks), mound (projected),
  birches (projected); and the ground by step 3's ground layout: open snow, path, heather ground,
  ice -- less the painted tufts, which are their own class (step 3's tuft classifier).
PER CHUNK (the 16 paint chunks, their own 1536 x 1024 rects -- the overlaps counted in both), PER
CLASS: pixels; coverage (the share of the painting's class pixels the render draws AS that class:
the ID render's class, overridden by the 3D heather where heather_mask shows it); and the mean
per-channel |difference|, sRGB 0-255, inside the class eroded 2 px (misregistration at a class's
edge is the neighbour's colour, not this class's error). The heather is also measured the other
way (precision: the drawn heather that lands on painted tufts) and by colour (render against
painting, linear, on the pixels both call heather) -- the number its grade is calibrated from.

THE BAR (the conductor): static pieces within a few points of the unlit bake's 15.5.
Writes take/build/overlay_check.json and take/build/overlay_check.png. EVERY CHUNK IS REPORTED.
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paint_world_prep as PW  # noqa: E402

BF = PW.BF
GROUPS = {"stones (baked)": {"stone_tall", "stone_mid", "stone_short", "lintel", "post"},
          "kit + raven (baked)": {"cairn", "log", "shield", "raven"},
          "rock (projected)": {"outcrop", "shore_rock"},
          "mound (projected)": {"mound"},
          "birches (projected)": {"birch"}}
GROUND = {0: "ground: open snow", 1: "ground: path", 3: "ground: heather ground", 4: "ground: ice"}
STATIC = list(GROUPS)
BAR = 15.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", default=os.path.join(BF, "captures", "painted"))
    ap.add_argument("--variants", default="inpainted,as_painted")
    ap.add_argument("--out", default=os.path.join(BF, "take", "build"))
    a = ap.parse_args()
    sha = hashlib.sha256(open(PW.PAINTING, "rb").read()).hexdigest()
    assert sha.startswith(PW.PAINT_SHA_PREFIX)
    P8 = np.asarray(Image.open(PW.PAINTING).convert("RGB"))
    H, W = P8.shape[:2]
    idx, table = PW.id_index()
    ground = idx == 0
    heather, shrub = PW.tuft_classes(P8, ground)
    tufts = ndimage.binary_opening(heather | shrub, iterations=1)
    cls_of = np.full(idx.max() + 1, "", object)
    for k, v in table.items():
        cls_of[k] = v["class"]
    # the class map of the PAINTING: pieces by ID, ground by step 3's layout, tufts on top
    GU = np.asarray(Image.open(os.path.join(PW.TAKE, "ground", "ground_uv.png")))
    ys, xs = np.mgrid[0:H, 0:W]
    uu, vv = PW.uv_of_px(xs + 0.5, ys + 0.5)
    gi = np.clip(((uu - PW.U0) * 20).astype(int), 0, GU.shape[1] - 1)
    gj = np.clip(((PW.V1 - vv) * 20).astype(int), 0, GU.shape[0] - 1)
    gcls = GU[gj, gi]
    names = STATIC + [GROUND[k] for k in (0, 1, 3, 4)] + ["heather + shrub tufts"]
    paint_cls = np.full((H, W), -1, np.int16)
    for i, g in enumerate(STATIC):
        ids = [k for k, v in table.items() if v["class"] in GROUPS[g]]
        paint_cls[np.isin(idx, ids)] = i
    for j, k in enumerate((0, 1, 3, 4)):
        paint_cls[ground & (gcls == k)] = len(STATIC) + j
    tuft_c = len(names) - 1
    paint_cls[tufts] = tuft_c
    masks_eroded = {}
    for c in range(len(names)):
        m = paint_cls == c
        masks_eroded[c] = ndimage.binary_erosion(m, iterations=2) if c != tuft_c else m
    chunks = PW.L["frame"]["chunks"]["list"]
    Plin = PW.s2l(P8.astype(np.float64) / 255.0)
    HM = np.asarray(Image.open(os.path.join(a.capture, "heather_mask.png")).convert("L")) > 127
    # THE SPRAYS' OWN COLOUR (heather_colour over black, divided by the mask's coverage) against the
    # painted tufts under the same pixels, both weighted by coverage: the grade's calibration
    cal = None
    hc = os.path.join(a.capture, "heather_colour.png")
    if os.path.exists(hc):
        cov = PW.s2l(np.asarray(Image.open(os.path.join(a.capture, "heather_mask.png")).convert("L")).astype(np.float64) / 255.0)
        HC = PW.s2l(np.asarray(Image.open(hc).convert("RGB")).astype(np.float64) / 255.0)
        on = tufts & (cov > 0.02)
        wsum = cov[on].sum()
        stem = HC[on].sum(0) / max(wsum, 1e-9)
        painted = (Plin[on] * cov[on][:, None]).sum(0) / max(wsum, 1e-9)
        cal = {"sprays_own_colour_linear": [round(float(x), 4) for x in stem],
               "painted_tufts_beneath_linear": [round(float(x), 4) for x in painted],
               "painted_over_sprays": [round(float(x), 4) for x in painted / np.maximum(stem, 1e-6)],
               "coverage_weight_px": round(float(wsum), 1),
               "_instrument": "heather_colour.png (the sprays as drawn, everything else black) over heather_mask.png's coverage, linear, on painted tuft pixels only"}
    out = {"_what": "C-9 T10-2 step 5: the overlay check, per chunk -- the assembled Barrow at the guide camera against the painting",
           "heather_grade_calibration": cal,
           "painting_sha256": sha, "bar": {"static_pieces_mean_abs_diff": "within a few points of %.1f (the unlit bake)" % BAR},
           "classes": names, "variants": {}}
    for variant in a.variants.split(","):
        R8 = np.asarray(Image.open(os.path.join(a.capture, "guide_%s.png" % variant)).convert("RGB"))
        assert R8.shape == P8.shape, (R8.shape, P8.shape)
        D = np.abs(R8.astype(np.int16) - P8.astype(np.int16)).astype(np.float32)
        rend_cls = paint_cls.copy()
        rend_cls[HM] = tuft_c                  # what the render DRAWS: its heather where the heather is
        rend_cls[(~HM) & (paint_cls == tuft_c)] = -2    # a painted tuft pixel the render does not draw as heather
        v = {"per_chunk": {}, "whole_window": {}}
        for ch in chunks + [{"key": "whole_window", "px": [0, 0, W, H]}]:
            x0, y0, x1, y1 = ch["px"]
            sl = (slice(y0, y1), slice(x0, x1))
            rec = {}
            for c, nm in enumerate(names):
                pm = paint_cls[sl] == c
                n = int(pm.sum())
                if n == 0:
                    continue
                cov = float((rend_cls[sl][pm] == c).mean())
                me = masks_eroded[c][sl]
                d = D[sl][me].mean(axis=0) if me.sum() else np.array([np.nan] * 3)
                row = {"px": n, "coverage": round(cov, 4),
                       "mean_abs_diff_rgb": [round(float(x), 2) for x in d],
                       "mean_abs_diff": round(float(np.nanmean(d)), 2) if me.sum() else None}
                if c == tuft_c:
                    rh = HM[sl]
                    row["drawn_heather_px"] = int(rh.sum())
                    row["precision_drawn_on_painted"] = round(float((pm & rh).sum()) / max(float(rh.sum()), 1.0), 4)
                    both = pm & rh
                    if both.sum() > 200:
                        Rl = PW.s2l(R8[sl][both].astype(np.float64) / 255.0).mean(0)
                        Pl = Plin[sl][both].mean(0)
                        row["colour_on_both_linear"] = {"render": [round(float(x), 4) for x in Rl],
                                                        "painting": [round(float(x), 4) for x in Pl],
                                                        "painting_over_render": [round(float(x), 3) for x in Pl / np.maximum(Rl, 1e-4)]}
                rec[nm] = row
            stm = np.zeros_like(paint_cls[sl], bool)
            for c in range(len(STATIC)):
                stm |= masks_eroded[c][sl]
            gm = np.zeros_like(stm)
            for c in range(len(STATIC), len(STATIC) + 4):
                gm |= masks_eroded[c][sl]
            rec["ALL STATIC PIECES"] = {"px": int(stm.sum()), "mean_abs_diff": round(float(D[sl][stm].mean()), 2) if stm.sum() else None,
                                        "mean_abs_diff_rgb": [round(float(x), 2) for x in D[sl][stm].mean(0)] if stm.sum() else None}
            rec["ALL GROUND (tufts apart)"] = {"px": int(gm.sum()), "mean_abs_diff": round(float(D[sl][gm].mean()), 2) if gm.sum() else None}
            rec["WHOLE CHUNK"] = {"px": int(D[sl].shape[0] * D[sl].shape[1]), "mean_abs_diff": round(float(D[sl].mean()), 2)}
            if ch["key"] == "whole_window":
                v["whole_window"] = rec
            else:
                v["per_chunk"][ch["key"]] = rec
        # the bar, per chunk
        worst = max(((k, r["ALL STATIC PIECES"]["mean_abs_diff"]) for k, r in v["per_chunk"].items()
                     if r["ALL STATIC PIECES"]["mean_abs_diff"] is not None), key=lambda t: t[1])
        v["static_pieces_worst_chunk"] = {"chunk": worst[0], "mean_abs_diff": worst[1]}
        v["static_pieces_by_chunk"] = {k: r["ALL STATIC PIECES"]["mean_abs_diff"] for k, r in v["per_chunk"].items()}
        out["variants"][variant] = v
        # the picture: painting | render | |difference| x3, one row, downscaled 4x, the chunk grid on
        if variant == a.variants.split(",")[0]:
            sc = 4
            p_ = Image.fromarray(P8).resize((W // sc, H // sc), Image.LANCZOS)
            r_ = Image.fromarray(R8).resize((W // sc, H // sc), Image.LANCZOS)
            d_ = Image.fromarray(np.clip(D.mean(-1) * 3.0, 0, 255).astype(np.uint8)).resize((W // sc, H // sc), Image.BILINEAR).convert("RGB")
            pic = Image.new("RGB", (3 * W // sc + 20, H // sc), (255, 255, 255))
            for i, im in enumerate((p_, r_, d_)):
                dr = ImageDraw.Draw(im)
                for ch in chunks:
                    x0, y0, x1, y1 = [q // sc for q in ch["px"]]
                    dr.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(220, 40, 40))
                    dr.text((x0 + 4, y0 + 2), ch["key"], fill=(220, 40, 40))
                pic.paste(im, (i * (W // sc + 10), 0))
            pic.save(os.path.join(a.out, "overlay_check.png"))
    json.dump(out, open(os.path.join(a.out, "overlay_check.json"), "w"), indent=1)
    if cal:
        print("== heather grade:", cal["sprays_own_colour_linear"], "painted", cal["painted_tufts_beneath_linear"], "x", cal["painted_over_sprays"])
    for variant, v in out["variants"].items():
        ww = v["whole_window"]
        print("== %s: static pieces %.2f (worst chunk %s %.2f); ground %.2f; tufts coverage %.3f precision %.3f diff %.2f"
              % (variant, ww["ALL STATIC PIECES"]["mean_abs_diff"], v["static_pieces_worst_chunk"]["chunk"],
                 v["static_pieces_worst_chunk"]["mean_abs_diff"], ww["ALL GROUND (tufts apart)"]["mean_abs_diff"],
                 ww["heather + shrub tufts"]["coverage"], ww["heather + shrub tufts"]["precision_drawn_on_painted"],
                 ww["heather + shrub tufts"]["mean_abs_diff"]))
        for nm in names:
            if nm in ww:
                print("   %-26s px %8d  coverage %.3f  diff %s  %s" % (nm, ww[nm]["px"], ww[nm]["coverage"], ww[nm]["mean_abs_diff"], ww[nm]["mean_abs_diff_rgb"]))
        print("   by chunk (static pieces):", v["static_pieces_by_chunk"])
        if "colour_on_both_linear" in ww["heather + shrub tufts"]:
            print("   heather colour:", ww["heather + shrub tufts"]["colour_on_both_linear"])


if __name__ == "__main__":
    main()
