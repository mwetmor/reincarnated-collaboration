#!/usr/bin/env python3
"""EoR Crucible wave-badge reader.

Reads the red wave-number glyphs from the Grim Dawn Crucible HUD badge.
ROI (full-frame 1920x1080): x 1550..1690, y 125..175  -> crop 140x50 at (1550,125)
Digits sit at crop coords roughly x 30..90, y 15..40.

Strategy: whole-number bitmap clustering (fixed bitmap font, small value alphabet),
then human/multimodal labelling of one exemplar per cluster. Avoids per-digit
segmentation error on touching glyph serifs.
"""
import sys, os, glob, json
import numpy as np
from PIL import Image

# Interior of the gold badge ring only -- rejects combat-FX / blood / minimap
# red bleeding in from outside the circle.
DIG_X0, DIG_X1 = 36, 77
DIG_Y0, DIG_Y1 = 8, 39


def mask_of(path):
    im = np.array(Image.open(path).convert("RGB")).astype(np.int16)
    sub = im[DIG_Y0:DIG_Y1, DIG_X0:DIG_X1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    return (R > 105) & (R - G > 42) & (R - B > 42)


def bitmap_key(m):
    """Return (canvas bitmap, bbox) normalised to top-left of the glyph bbox."""
    ys, xs = np.nonzero(m)
    if len(xs) < 25:            # nothing / noise
        return None, None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if h < 9 or h > 20 or w < 4 or w > 40:
        return None, None
    canvas = np.zeros((20, 40), dtype=bool)
    canvas[:h, :w] = m[y0:y1 + 1, x0:x1 + 1]
    return canvas, (int(x0), int(x1), int(y0), int(y1))


def main(indir, outjson, exemplar_dir):
    os.makedirs(exemplar_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(indir, "*.png")))
    clusters = []          # list of dict(canvas, members)
    rows = []
    for f in files:
        t = int(os.path.basename(f).split(".")[0])
        m = mask_of(f)
        canvas, bbox = bitmap_key(m)
        if canvas is None:
            rows.append({"t": t, "cluster": -1, "px": int(m.sum())})
            continue
        best, bestd = -1, 10 ** 9
        for ci, c in enumerate(clusters):
            d = int(np.logical_xor(canvas, c["canvas"]).sum())
            if d < bestd:
                bestd, best = d, ci
        if best >= 0 and bestd <= 8:
            clusters[best]["members"].append(t)
            clusters[best]["n"] += 1
        else:
            clusters.append({"canvas": canvas, "members": [t], "n": 1,
                             "exemplar": t, "bbox": bbox})
            best = len(clusters) - 1
        rows.append({"t": t, "cluster": best, "px": int(canvas.sum())})

    meta = []
    for ci, c in enumerate(clusters):
        # write exemplar bitmap 10x for reading
        img = Image.fromarray((~c["canvas"]).astype(np.uint8) * 255).convert("L")
        img = img.resize((40 * 10, 20 * 10), Image.NEAREST)
        img.save(os.path.join(exemplar_dir, f"c{ci:03d}_n{c['n']}_t{c['exemplar']}.png"))
        meta.append({"cluster": ci, "n": c["n"], "exemplar_t": c["exemplar"],
                     "bbox": c["bbox"],
                     "first_t": min(c["members"]), "last_t": max(c["members"]),
                     "members": c["members"]})
    json.dump({"rows": rows, "clusters": meta}, open(outjson, "w"))
    print(f"frames={len(files)} clusters={len(clusters)} nohud={sum(1 for r in rows if r['cluster']<0)}")
    for m in sorted(meta, key=lambda x: x["first_t"]):
        print(f"  c{m['cluster']:03d} n={m['n']:5d} t[{m['first_t']}..{m['last_t']}] ex={m['exemplar_t']} bbox={m['bbox']}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
