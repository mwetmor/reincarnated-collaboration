#!/usr/bin/env python3
"""C-9 T10-2 step 4 (B): the mini overlay check, measured. drax.

    python3 tools/mini_overlay.py

Reads godot/tools/mini_overlay.gd's crops (work/overlay/) and sets each against the painting at
the same pixels, inside the piece as the ID render sees it (eroded 2 px: the ink line, the MSAA
edge and the matte's own erosion are not what is being measured). Reports the mean per-channel
|difference| (0-255) and the signed mean (render - painting), for the bake worn UNLIT (the
projection alone) and worn as the ramp's ALBEDO under the blockout's sun (painted light lit twice).
Writes take/build/mini_overlay.json and take/build/mini_overlay.png (painting | unlit | lit).
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
BF = os.path.dirname(HERE)
MARGIN = 12


def main():
    plates = json.load(open(os.path.join(BF, "take", "plates", "plates.json")))["plates"]
    ids_meta = json.load(open(os.path.join(BF, "take", "ids", "ids.json")))["placements"]
    idmap = np.asarray(Image.open(os.path.join(BF, "take", "ids", "ids.png")).convert("RGB")).astype(np.int32)
    paint = Image.open(os.path.join(BF, "paint", "barrow_full_painted.png")).convert("RGB")
    ov = os.path.join(BF, "work", "overlay")
    ids = sorted({f.split("_", 1)[1][:-4] for f in os.listdir(ov) if f.startswith("unlit_")})
    rep = {"_what": "C-9 T10-2 step 4 (B): baked heroes rendered at the guide camera against the painting",
           "_measure": "inside the piece's ID-render silhouette, eroded 2 px; 0-255 sRGB per channel",
           "pieces": {}}
    rows = []
    for id_ in ids:
        pl = plates[id_]
        x, y, w, h = pl["rect_px"]
        x0, y0 = max(x - MARGIN, 0), max(y - MARGIN, 0)
        un = np.asarray(Image.open(os.path.join(ov, "unlit_%s.png" % id_)).convert("RGB")).astype(np.float32)
        li = np.asarray(Image.open(os.path.join(ov, "lit_%s.png" % id_)).convert("RGB")).astype(np.float32)
        H, W = un.shape[:2]
        pc = np.asarray(paint.crop((x0, y0, x0 + W, y0 + H))).astype(np.float32)
        col = ids_meta[str(pl["id_index"])]["rgb"]
        sub = idmap[y0:y0 + H, x0:x0 + W]
        m = (np.abs(sub - np.array(col)).sum(-1) < 12)
        m = ndimage.binary_erosion(m, iterations=2)
        d_un, d_li = un[m] - pc[m], li[m] - pc[m]
        rep["pieces"][id_] = {
            "px_measured": int(m.sum()),
            "unlit": {"mean_abs_per_channel": np.abs(d_un).mean(0).round(1).tolist(),
                      "mean_abs": round(float(np.abs(d_un).mean()), 1),
                      "signed_mean": d_un.mean(0).round(1).tolist()},
            "lit": {"mean_abs_per_channel": np.abs(d_li).mean(0).round(1).tolist(),
                    "mean_abs": round(float(np.abs(d_li).mean()), 1),
                    "signed_mean": d_li.mean(0).round(1).tolist()}}
        print("%-18s px %6d   unlit |d| %5.1f  (signed %s)   lit |d| %5.1f  (signed %s)"
              % (id_, m.sum(), rep["pieces"][id_]["unlit"]["mean_abs"], rep["pieces"][id_]["unlit"]["signed_mean"],
                 rep["pieces"][id_]["lit"]["mean_abs"], rep["pieces"][id_]["lit"]["signed_mean"]))
        s = 2 if max(W, H) < 300 else 1
        row = np.concatenate([pc, un, li], 1).clip(0, 255).astype(np.uint8)
        rows.append(Image.fromarray(row).resize((row.shape[1] * s, row.shape[0] * s), Image.NEAREST))
    allu = [v["unlit"]["mean_abs"] for v in rep["pieces"].values()]
    alll = [v["lit"]["mean_abs"] for v in rep["pieces"].values()]
    rep["summary"] = {"unlit_mean_abs": round(float(np.mean(allu)), 1), "lit_mean_abs": round(float(np.mean(alll)), 1)}
    Wm = max(r.width for r in rows)
    out = Image.new("RGB", (Wm, sum(r.height for r in rows) + 8 * (len(rows) - 1)), (30, 30, 36))
    yy = 0
    for r in rows:
        out.paste(r, (0, yy))
        yy += r.height + 8
    os.makedirs(os.path.join(BF, "take", "build"), exist_ok=True)
    out.save(os.path.join(BF, "take", "build", "mini_overlay.png"))
    json.dump(rep, open(os.path.join(BF, "take", "build", "mini_overlay.json"), "w"), indent=1)
    print("mean |d|: unlit %.1f, lit %.1f  ->  take/build/mini_overlay.png" % (
        rep["summary"]["unlit_mean_abs"], rep["summary"]["lit_mean_abs"]))


if __name__ == "__main__":
    main()
