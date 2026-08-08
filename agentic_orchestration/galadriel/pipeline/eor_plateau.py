#!/usr/bin/env python3
"""EoR Crucible wave-badge plateau segmentation.

Input : directory of 1-fps badge crops (140x50 crop of full frame at (1550,125)).
Output: JSON with per-frame signature + plateau segmentation (runs of frames whose
        badge glyph image is the same within tolerance).

Signal used is a *redness* map v = clip(R - max(G,B), 0, 255) restricted to the
interior of the gold badge ring. Binary thresholding flickers with the glyph glow
pulse; the continuous redness map with normalised cross-correlation does not.
"""
import sys, os, glob, json
import numpy as np
from PIL import Image

X0, X1, Y0, Y1 = 36, 77, 8, 39      # badge-ring interior, crop coords
CANVAS_W, CANVAS_H = 44, 24
MIN_ENERGY = 200.0                   # below this -> no badge on screen


def redness(path):
    im = np.array(Image.open(path).convert("RGB")).astype(np.int16)
    s = im[Y0:Y1, X0:X1]
    v = s[:, :, 0] - np.maximum(s[:, :, 1], s[:, :, 2])
    v = np.clip(v, 0, 255).astype(np.float32)
    v[v < 25] = 0.0                  # kill faint background tint
    return v


def signature(v):
    """Centre-aligned normalised patch, or None if no glyphs."""
    e = float(v.sum())
    if e < MIN_ENERGY:
        return None, e, None
    ys, xs = np.nonzero(v > 40)
    if len(xs) < 15:
        return None, e, None
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if h < 9 or h > 20 or w < 4 or w > 40:
        return None, e, None
    patch = v[y0:y1 + 1, x0:x1 + 1]
    canvas = np.zeros((CANVAS_H, CANVAS_W), dtype=np.float32)
    # centre horizontally, top-align vertically (glyph baseline is stable)
    ox = (CANVAS_W - w) // 2
    canvas[:h, ox:ox + w] = patch
    n = np.linalg.norm(canvas)
    if n == 0:
        return None, e, None
    return canvas / n, e, (x0, x1, y0, y1)


def dist(a, b):
    return 1.0 - float((a * b).sum())


def main(indir, outjson, thresh=0.14):
    files = sorted(glob.glob(os.path.join(indir, "*.png")))
    sigs, energies, bboxes, ts = [], [], [], []
    for f in files:
        t = int(os.path.basename(f).split(".")[0])
        s, e, bb = signature(redness(f))
        ts.append(t); sigs.append(s); energies.append(e); bboxes.append(bb)

    # plateau segmentation: greedy, compare to plateau's running medoid
    plateaus = []
    cur = None
    for i, s in enumerate(sigs):
        if s is None:
            if cur is not None:
                plateaus.append(cur); cur = None
            plateaus.append({"kind": "nobadge", "t0": ts[i], "t1": ts[i], "members": [ts[i]]})
            continue
        if cur is None or cur["kind"] != "badge":
            cur = {"kind": "badge", "t0": ts[i], "t1": ts[i], "members": [ts[i]],
                   "ref": s, "idx": [i]}
            continue
        d = dist(cur["ref"], s)
        if d <= thresh:
            cur["t1"] = ts[i]; cur["members"].append(ts[i]); cur["idx"].append(i)
        else:
            plateaus.append(cur)
            cur = {"kind": "badge", "t0": ts[i], "t1": ts[i], "members": [ts[i]],
                   "ref": s, "idx": [i]}
    if cur is not None:
        plateaus.append(cur)

    # merge adjacent nobadge runs
    merged = []
    for p in plateaus:
        if merged and merged[-1]["kind"] == "nobadge" == p["kind"]:
            merged[-1]["t1"] = p["t1"]; merged[-1]["members"] += p["members"]
        else:
            merged.append(p)

    out = []
    for p in merged:
        rec = {"kind": p["kind"], "t0": p["t0"], "t1": p["t1"], "n": len(p["members"])}
        if p["kind"] == "badge":
            # medoid frame = the one closest to the plateau mean signature
            mean = np.mean([sigs[i] for i in p["idx"]], axis=0)
            mean = mean / (np.linalg.norm(mean) or 1)
            best = min(p["idx"], key=lambda i: dist(mean, sigs[i]))
            rec["medoid_t"] = ts[best]
            rec["bbox"] = bboxes[best]
        out.append(rec)
    json.dump({"plateaus": out,
               "energy": {str(t): round(e, 1) for t, e in zip(ts, energies)}},
              open(outjson, "w"), indent=1)
    for p in out:
        tag = f"[{p['t0']:5d}..{p['t1']:5d}] n={p['n']:4d} {p['kind']}"
        if p["kind"] == "badge":
            tag += f" medoid_t={p['medoid_t']} bbox={p['bbox']}"
        print(tag)
    print(f"total plateaus={len(out)} badge={sum(1 for p in out if p['kind']=='badge')}")


if __name__ == "__main__":
    th = float(sys.argv[3]) if len(sys.argv) > 3 else 0.14
    main(sys.argv[1], sys.argv[2], th)
