#!/usr/bin/env python3
"""Build a digit-glyph atlas for the Crucible wave badge, then OCR whole numbers.

Templates are harvested from sitting-2 frames whose wave value was read visually
and cross-verified (badge sequence 151..160 supplies all ten digits 0-9).

Whole-number matching (not per-glyph classification) is used at read time: the
glow bleed bridges adjacent glyphs at low pulse phase, so column segmentation is
unreliable, but a synthesised full-string template compared by gamma-compressed
NCC is robust to that bleed.

  build  <framedir> <spec.json> <atlas.npz>
  read   <framedir> <atlas.npz> <out.json> [lo] [hi]
"""
import sys, os, glob, json
import numpy as np
from PIL import Image

X0, X1, Y0, Y1 = 36, 77, 8, 39
ROI_W, ROI_H = X1 - X0, Y1 - Y0
MIN_E = 300.0


def red(path):
    im = np.array(Image.open(path).convert("RGB")).astype(np.int16)
    s = im[Y0:Y1, X0:X1]
    return np.clip(s[:, :, 0] - np.maximum(s[:, :, 1], s[:, :, 2]), 0, 255).astype(np.float32)


def comp(v):
    w = v.copy(); w[w < 12] = 0
    return np.power(w, 0.5)


def norm(w):
    n = np.linalg.norm(w)
    return (w / n) if n > 0 else w


def split_columns(v, k):
    """Split a k-digit number into k glyph column ranges using the k-1 deepest
    interior valleys of the column profile."""
    p = comp(v).sum(axis=0)
    on = np.nonzero(p > p.max() * 0.06)[0]
    a, b = int(on.min()), int(on.max())
    if k == 1:
        return [(a, b)]
    interior = list(range(a + 3, b - 2))
    # candidate valleys: local minima, keep k-1 with lowest value and >=5 apart
    cands = sorted(interior, key=lambda x: p[x])
    picked = []
    for c in cands:
        if all(abs(c - q) >= 5 for q in picked):
            picked.append(c)
        if len(picked) == k - 1:
            break
    picked.sort()
    cuts = [a - 1] + picked + [b + 1]
    return [(cuts[i] + 1, cuts[i + 1] - 1) for i in range(k)]


def harvest(framedir, spec):
    """spec: {"<t>": "<value string>"} ; returns dict digit -> list of patches."""
    bank = {}
    for t, val in spec.items():
        f = os.path.join(framedir, f"{int(t):05d}.png")
        v = red(f)
        segs = split_columns(v, len(val))
        for ch, (c0, c1) in zip(val, segs):
            patch = v[:, c0:c1 + 1]
            rows = np.nonzero(comp(patch).sum(axis=1) > 6)[0]
            if len(rows) < 8:
                continue
            g = patch[rows.min():rows.max() + 1]
            bank.setdefault(ch, []).append((g, int(rows.min())))
    return bank


def consolidate(bank):
    """Median-combine patches per digit onto a common canvas."""
    atlas = {}
    for ch, lst in bank.items():
        H = max(g.shape[0] for g, _ in lst)
        W = max(g.shape[1] for g, _ in lst)
        top = int(np.median([o for _, o in lst]))
        stack = []
        for g, _ in lst:
            c = np.zeros((H, W), dtype=np.float32)
            c[:g.shape[0], :g.shape[1]] = g
            stack.append(c)
        atlas[ch] = {"bmp": np.median(np.stack(stack), axis=0), "top": top}
    return atlas


def render(atlas, s, kern=1):
    """Render string s onto the ROI canvas, horizontally centred."""
    parts = [atlas[c] for c in s]
    W = sum(p["bmp"].shape[1] for p in parts) + kern * (len(s) - 1)
    canvas = np.zeros((ROI_H, ROI_W), dtype=np.float32)
    ox = (ROI_W - W) // 2
    for p in parts:
        b, top = p["bmp"], p["top"]
        h, w = b.shape
        canvas[top:top + h, ox:ox + w] = np.maximum(canvas[top:top + h, ox:ox + w], b)
        ox += w + kern
    return canvas


def build(framedir, specfile, out):
    spec = json.load(open(specfile))
    atlas = consolidate(harvest(framedir, spec))
    np.savez(out, **{f"bmp_{k}": v["bmp"] for k, v in atlas.items()},
             **{f"top_{k}": np.array([v["top"]]) for k, v in atlas.items()})
    print("digits:", "".join(sorted(atlas)),
          "widths:", {k: atlas[k]["bmp"].shape[1] for k in sorted(atlas)},
          "tops:", {k: atlas[k]["top"] for k in sorted(atlas)})
    # self-test on the spec frames
    ok = 0
    for t, val in spec.items():
        v = red(os.path.join(framedir, f"{int(t):05d}.png"))
        best, bd = None, 9e9
        for cand in range(0, 200):
            d = 1 - float((norm(comp(v)) * norm(render(atlas, str(cand)))).sum())
            if d < bd: bd, best = d, cand
        ok += (str(best) == val)
        print(f"  t={t} truth={val} ocr={best} d={bd:.4f}")
    print(f"self-test {ok}/{len(spec)}")


def load_atlas(path):
    z = np.load(path)
    ks = sorted(k[4:] for k in z.files if k.startswith("bmp_"))
    return {k: {"bmp": z[f"bmp_{k}"], "top": int(z[f"top_{k}"][0])} for k in ks}


def read_dir(framedir, atlaspath, out, lo=0, hi=200):
    atlas = load_atlas(atlaspath)
    cands = {c: norm(render(atlas, str(c))) for c in range(lo, hi + 1)}
    rows = []
    for f in sorted(glob.glob(os.path.join(framedir, "*.png"))):
        t = int(os.path.basename(f).split(".")[0])
        v = red(f)
        if v.sum() < MIN_E:
            rows.append({"t": t, "wave": None, "d": None, "margin": None}); continue
        q = norm(comp(v))
        ds = sorted(((1 - float((q * tpl).sum()), c) for c, tpl in cands.items()))
        rows.append({"t": t, "wave": ds[0][1], "d": round(ds[0][0], 4),
                     "margin": round(ds[1][0] - ds[0][0], 4)})
    json.dump(rows, open(out, "w"))
    good = [r for r in rows if r["wave"] is not None]
    print(f"frames={len(rows)} badge={len(good)} "
          f"median_d={np.median([r['d'] for r in good]):.4f}")


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        read_dir(sys.argv[2], sys.argv[3], sys.argv[4],
                 int(sys.argv[5]) if len(sys.argv) > 5 else 0,
                 int(sys.argv[6]) if len(sys.argv) > 6 else 200)
