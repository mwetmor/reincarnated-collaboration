#!/usr/bin/env python3
"""C-9 knight3d step 5: check that the BUILT body is the FITTED body.

The fitter works on an analytic union-of-convex-solids silhouette because it
has to run tens of thousands of times. The thing that will actually be
textured and animated is the Blender mesh. Those are two different objects and
a fit against the first proves nothing about the second, so this compares the
Blender orthographic renders (04_build_blender.py --render) against:
  (a) the analytic proxy silhouette at the same camera  -> do they agree?
  (b) the matted still                                   -> the IoU that counts.
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
WORK = os.path.join(K3, "work"); MASKS = os.path.join(WORK, "masks")
OUT = os.path.join(K3, "out"); OVER = os.path.join(K3, "overlays")
SIL = os.path.join(OUT, "silhouettes")
SEEDS = os.path.join(ROOT, "artifacts", "seeds")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
SEED_FILE = {"N": "seed_N.png", "NE": "seed_NE.png", "E": "seed_E.png",
             "SE": "seed_SE.png", "S": "seed_S_v2.png", "SW": "seed_SW_v2.png",
             "W": "seed_W.png", "NW": "seed_NW.png"}


def outline(m, w=5):
    return ndi.binary_dilation(m, np.ones((w, w))) & ~ndi.binary_erosion(m, np.ones((w, w)))


def main(which="pose_fitted"):
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta, ds, p0 = fit["theta_elevation_deg"], fit["downsample"], fit["params"]
    rep = {"note": "Blender-built body vs the analytic fitted proxy vs the still.",
           "theta_elevation_deg": theta, "variant": which, "views": {}}
    tiles_out, tiles_mask = [], []
    for d in DIRS:
        v = fit[which]["views"][d]
        pv = dict(p0)
        for k, dv in (v.get("delta") or {}).items():
            pv[k] = p0[k] + dv
        body = np.load(os.path.join(MASKS, "%s_body.npy" % d))
        axe = np.load(os.path.join(MASKS, "%s_axe.npy" % d))
        amb = np.load(os.path.join(MASKS, "%s_amb.npy" % d))
        dead = ndi.binary_dilation(axe | amb, np.ones((9, 9)))
        H, W = body.shape
        ana = kp.rasterize(kp.build(pv), v["alpha"], theta, v["scale"] * ds,
                           v["tx"] * ds, v["ty"] * ds, W, H)
        bl = np.asarray(Image.open(os.path.join(SIL, "%s.png" % d)).convert("RGBA"))[..., 3] > 8
        live = ~dead

        def I(a, b):
            A, B = a & live, b & live
            u = (A | B).sum()
            return float((A & B).sum()) / u if u else 0.0

        rep["views"][d] = dict(iou_blender_vs_still=I(bl, body),
                               iou_analytic_vs_still=I(ana, body),
                               iou_blender_vs_analytic=I(bl, ana),
                               alpha=v["alpha"], nominal_alpha=v["nominal_alpha"],
                               alpha_residual=v["alpha_residual"],
                               scale_px_per_m=v["scale"] * ds,
                               blender_only_px=int((bl & ~body & live).sum()),
                               still_only_px=int((body & ~bl & live).sum()),
                               pose_delta=v.get("delta", {}))
        print("%-3s blender-vs-still %.4f   analytic-vs-still %.4f   blender-vs-analytic %.4f"
              % (d, rep["views"][d]["iou_blender_vs_still"],
                 rep["views"][d]["iou_analytic_vs_still"],
                 rep["views"][d]["iou_blender_vs_analytic"]))

        rgb = np.asarray(Image.open(os.path.join(SEEDS, SEED_FILE[d])).convert("RGB")).copy()
        pale = (rgb.astype(np.float32) * 0.42 + 255 * 0.58).astype(np.uint8)
        pale[outline(bl, 5)] = (190, 20, 20)
        Image.fromarray(pale).save(os.path.join(OVER, "%s_blender_outline.png" % d))
        tiles_out.append(Image.fromarray(pale))
        tri = np.zeros((H, W, 3), np.uint8)
        tri[..., 0] = np.where(body & live, 215, 0)
        tri[..., 1] = np.where(bl & live, 215, 0)
        tri[..., 2] = np.where(dead, 75, 0)
        Image.fromarray(tri).save(os.path.join(OVER, "%s_blender_mask.png" % d))
        tiles_mask.append(Image.fromarray(tri))

    for k in ("iou_blender_vs_still", "iou_analytic_vs_still", "iou_blender_vs_analytic"):
        rep["mean_" + k] = float(np.mean([rep["views"][d][k] for d in DIRS]))
        print("mean %s %.4f" % (k, rep["mean_" + k]))
    with open(os.path.join(OUT, "iou_report_blender.json"), "w") as f:
        json.dump(rep, f, indent=1)

    tw, th = 300, 450
    sheet = Image.new("RGB", (tw * 8, th * 2), (16, 16, 16))
    for i in range(8):
        sheet.paste(tiles_out[i].resize((tw, th)), (i * tw, 0))
        sheet.paste(tiles_mask[i].resize((tw, th)), (i * tw, th))
    sheet.save(os.path.join(OVER, "M-a_GATE_blender.png"))
    print("wrote", os.path.join(OVER, "M-a_GATE_blender.png"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pose_fitted")
