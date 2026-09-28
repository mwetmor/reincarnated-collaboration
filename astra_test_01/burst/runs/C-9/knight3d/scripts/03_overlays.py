#!/usr/bin/env python3
"""C-9 knight3d step 3 (GATE M-a deliverable): draw the silhouette overlays.

For each of the eight approved stills:
  * the still itself, with the fitted body's outline drawn on it, so the POSE
    and the CAMERA can be judged by eye and not only by a number;
  * a three-colour mask overlay: still-only (red), proxy-only (green),
    both (yellow-ish), with the excluded pollaxe/ambiguity band in dim blue.

Writes knight3d/overlays/ and knight3d/out/iou_report.json.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import knight_proxy as kp

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d")
WORK = os.path.join(K3, "work")
MASKS = os.path.join(WORK, "masks")
OVER = os.path.join(K3, "overlays")
OUT = os.path.join(K3, "out")
SEEDS = os.path.join(ROOT, "artifacts", "seeds")
os.makedirs(OVER, exist_ok=True); os.makedirs(OUT, exist_ok=True)

DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
SEED_FILE = {"N": "seed_N.png", "NE": "seed_NE.png", "E": "seed_E.png",
             "SE": "seed_SE.png", "S": "seed_S_v2.png", "SW": "seed_SW_v2.png",
             "W": "seed_W.png", "NW": "seed_NW.png"}


def outline(m, w=3):
    return ndi.binary_dilation(m, np.ones((w, w))) & ~ndi.binary_erosion(m, np.ones((w, w)))


def main(which="pose_fitted"):
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta = fit["theta_elevation_deg"]
    ds = fit["downsample"]
    p0 = fit["params"]
    rep = {"note": "C-9 knight3d M-a silhouette IoU, full resolution (1024x1536). "
                   "The pollaxe and the matte-cut ambiguity band are excluded "
                   "from BOTH masks.",
           "theta_elevation_deg": theta, "variant": which, "views": {}}
    strips = []
    for d in DIRS:
        v = fit[which]["views"][d]
        pv = dict(p0)
        pv.update(v.get("delta", {}) if which == "pose_fitted" else {})
        for k, dv in (v.get("delta") or {}).items():
            pv[k] = p0[k] + dv
        parts = kp.build(pv)

        body = np.load(os.path.join(MASKS, "%s_body.npy" % d))
        axe = np.load(os.path.join(MASKS, "%s_axe.npy" % d))
        amb = np.load(os.path.join(MASKS, "%s_amb.npy" % d))
        dead = ndi.binary_dilation(axe | amb, np.ones((9, 9)))
        H, W = body.shape
        m = kp.rasterize(parts, v["alpha"], theta, v["scale"] * ds,
                         v["tx"] * ds, v["ty"] * ds, W, H)
        live = ~dead
        A = m & live; B = body & live
        inter = int((A & B).sum()); union = int((A | B).sum())
        # where the residual LIVES: IoU per horizontal band of the figure, so
        # the gate can see whether the body is wrong at the helm, the torso,
        # the skirt or the feet rather than only that it is 0.88 overall.
        ys = np.where(B.any(axis=1))[0]
        y0, y1 = int(ys.min()), int(ys.max()); Hh = y1 - y0 + 1
        BANDS = [("helm_head", 0.00, 0.18), ("torso_arms", 0.18, 0.45),
                 ("tabard_fauld", 0.45, 0.62), ("legs", 0.62, 0.88),
                 ("feet", 0.88, 1.00)]
        bands = {}
        for nm, f0, f1 in BANDS:
            sl = slice(y0 + int(f0 * Hh), y0 + int(f1 * Hh) + 1)
            a_, b_ = A[sl], B[sl]
            u_ = (a_ | b_).sum()
            bands[nm] = dict(iou=float((a_ & b_).sum()) / u_ if u_ else None,
                             proxy_only_px=int((a_ & ~b_).sum()),
                             still_only_px=int((b_ & ~a_).sum()))
        rep["views"][d] = dict(
            iou=inter / union if union else 0.0,
            band_iou=bands,
            alpha=v["alpha"], nominal_alpha=v["nominal_alpha"],
            alpha_residual=v["alpha_residual"],
            scale_px_per_m=v["scale"] * ds,
            proxy_only_px=int((A & ~B).sum()), still_only_px=int((B & ~A).sum()),
            excluded_px=int(dead.sum()), pose_delta=v.get("delta", {}))

        rgb = np.asarray(Image.open(os.path.join(SEEDS, SEED_FILE[d])).convert("RGB")).copy()
        pale = (rgb.astype(np.float32) * 0.45 + 255 * 0.55).astype(np.uint8)
        ol = outline(m, 5)
        pale[ol] = (200, 20, 20)
        strips.append(Image.fromarray(pale))

        tri = np.zeros((H, W, 3), np.uint8)
        tri[..., 0] = np.where(B, 210, 0)
        tri[..., 1] = np.where(A, 210, 0)
        tri[..., 2] = np.where(dead, 70, 0)
        Image.fromarray(tri).save(os.path.join(OVER, "%s_mask_%s.png" % (d, which)))
        Image.fromarray(pale).save(os.path.join(OVER, "%s_outline_%s.png" % (d, which)))
        print("%-3s IoU %.4f  alpha %.1f (nominal %d, residual %+.1f)" %
              (d, rep["views"][d]["iou"], v["alpha"], v["nominal_alpha"], v["alpha_residual"]))

    rep["mean_iou"] = float(np.mean([rep["views"][d]["iou"] for d in DIRS]))
    print("mean IoU %.4f" % rep["mean_iou"])
    with open(os.path.join(OUT, "iou_report_%s.json" % which), "w") as f:
        json.dump(rep, f, indent=1)

    # contact strips
    tw, th = 300, 450
    sheet = Image.new("RGB", (tw * 8, th * 2), (18, 18, 18))
    for i, d in enumerate(DIRS):
        sheet.paste(strips[i].resize((tw, th)), (i * tw, 0))
        sheet.paste(Image.open(os.path.join(OVER, "%s_mask_%s.png" % (d, which)))
                    .resize((tw, th)), (i * tw, th))
    sheet.save(os.path.join(OVER, "ALL_%s.png" % which))
    print("wrote", os.path.join(OVER, "ALL_%s.png" % which))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pose_fitted")
