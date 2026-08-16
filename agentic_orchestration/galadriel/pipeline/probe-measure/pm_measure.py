#!/usr/bin/env python3
"""PROBE-MEASURE — the numbers.

Measures, for each still and each chroma threshold, the two silhouette-side
VERTICAL edges of the magenta probe box (leftmost and rightmost near-vertical
boundaries of the magenta region), plus the full-silhouette bounding box.

CHROMA. magenta-ness m = min(R,B) - G on 8-bit sRGB. The probe's albedo is pure
(1,0,1) and unshaded, so m saturates at 255 on the box body; scene content sits
at m < 16. Three thresholds are carried end to end:
    tight    m >= 200   only near-pure box
    nominal  m >= 128   the 50%-coverage antialias convention
    generous m >=  40   any appreciable magenta above the frame's noise shelf

CORNER LOCATION. For each wall the boundary x(y) is walked and its local slope
dx/dy is taken over a +/-WIN row window. The vertical box edge is FLAT (it leans
only toward the nadir, hundredths of a px/row); the top-face and ground-face
silhouette edges run at ~1 px/row. Three endpoint values are emitted per corner:

    TIGHT     innermost row that is unambiguously on the flat wall
              (first/last row with |slope| <= FLAT)
    READ      the half-slope crossing -- the row at which |slope| first passes
              half the adjacent slant magnitude. PRIMARY.
    GENEROUS  outermost row still plausibly on the wall
              (last/first row before |slope| reaches 0.9 * slant magnitude)

OCCLUDER NOTCHES. Rows where the wall departs its plateau by > NOTCH px and
returns within NOTCH_MAX rows are reported as notches and excluded from the
slant-magnitude estimate. They are never silently repaired.
"""
import argparse, json
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--label", required=True)
ap.add_argument("--win", type=int, default=4)
ap.add_argument("--flat", type=float, default=0.15)
ap.add_argument("--notch", type=int, default=2)
ap.add_argument("--notch-max", type=int, default=12)
ap.add_argument("--json", default=None)
a = ap.parse_args()

THRS = [("tight", 200), ("nominal", 128), ("generous", 40)]

im = Image.open(a.src).convert("RGB")
A = np.asarray(im, dtype=np.int16)
m = np.minimum(A[..., 0], A[..., 2]) - A[..., 1]
H, W = m.shape

res = {"label": a.label, "src": a.src, "frame_w": int(W), "frame_h": int(H),
       "chroma": "m = min(R,B) - G on 8-bit sRGB",
       "win_rows": a.win, "flat_pxrow": a.flat, "thresholds": {}}

def find_notches(rows, v, sign):
    """sign=-1 for the left wall (plateau is the MIN x), +1 for the right.

    A notch is an INTERIOR excursion off the plateau: it must lie strictly
    between the first and last plateau contact, so the top-face and ground-face
    slant runs at the two ends of the wall can never be mistaken for one.
    """
    out = []
    ext = v.min() if sign < 0 else v.max()
    dev_all = (v - ext) if sign < 0 else (ext - v)
    on = np.nonzero(dev_all <= a.notch)[0]
    if on.size < 2:
        return out
    i0, i1 = int(on[0]), int(on[-1])
    i = i0
    while i <= i1:
        if dev_all[i] > a.notch:
            j = i
            while j <= i1 and dev_all[j] > a.notch:
                j += 1
            if (j - i) <= a.notch_max:
                out.append((int(rows[i]), int(rows[j - 1])))
            i = j
        else:
            i += 1
    return out

for name, thr in THRS:
    mask = m >= thr
    rows, L, R = [], [], []
    for y in range(H):
        xs = np.nonzero(mask[y])[0]
        if xs.size:
            rows.append(y); L.append(int(xs.min())); R.append(int(xs.max()))
    rows = np.array(rows); L = np.array(L); R = np.array(R)
    n = len(rows)

    entry = {"threshold_m": thr,
             "bbox": {"x_min": int(L.min()), "x_max": int(R.max()),
                      "y_min": int(rows[0]), "y_max": int(rows[-1]),
                      "h_px": int(rows[-1] - rows[0]),
                      "h_frac": round(float(rows[-1] - rows[0]) / H, 5),
                      "w_px": int(R.max() - L.min()),
                      "n_rows_inclusive": int(rows[-1] - rows[0] + 1)},
             "walls": {}}

    for lab, v, sign in (("left", L, -1), ("right", R, +1)):
        notches = find_notches(rows, v, sign)
        notch_rows = set()
        for r0, r1 in notches:
            notch_rows.update(range(r0, r1 + 1))
        keep = np.array([r not in notch_rows for r in rows])
        rr, vv = rows[keep], v[keep]
        nn = len(rr)
        k = a.win
        slope = np.full(nn, np.nan)
        for i in range(nn):
            lo, hi = max(0, i - k), min(nn - 1, i + k)
            dy = rr[hi] - rr[lo]
            if dy:
                slope[i] = (vv[hi] - vv[lo]) / dy
        s = slope * (-1 if sign < 0 else 1)   # top slant is NEGATIVE for both after this

        ext = vv.min() if sign < 0 else vv.max()
        at_ext = np.nonzero(vv == ext)[0]
        i_mid = at_ext[len(at_ext) // 2]

        # slant magnitudes: median |slope| over the outer thirds of the run
        top_slant = float(np.nanmedian(np.abs(slope[:max(3, nn // 6)])))
        bot_slant = float(np.nanmedian(np.abs(slope[-max(3, nn // 6):])))

        def endpoint(which):
            if which == "top":
                idx = range(i_mid, -1, -1); slant = top_slant
            else:
                idx = range(i_mid, nn);     slant = bot_slant
            tight = read = generous = None
            for i in idx:
                sl = abs(slope[i])
                if np.isnan(sl):
                    continue
                if sl <= a.flat:
                    tight = int(rr[i])
                if read is None and sl > slant * 0.5:
                    read = int(rr[i])
                if sl >= slant * 0.9:
                    generous = int(rr[i]); break
            if read is None: read = int(rr[idx[0] if which == "top" else -1])
            if tight is None: tight = read
            if generous is None: generous = int(rr[0] if which == "top" else rr[-1])
            return {"tight": tight, "read": read, "generous": generous}

        top, bot = endpoint("top"), endpoint("bottom")
        xt = int(vv[np.searchsorted(rr, top["read"])])
        xb = int(vv[min(np.searchsorted(rr, bot["read"]), nn - 1)])

        def h(y0, y1): return int(y1 - y0)
        entry["walls"][lab] = {
            "plateau_x": int(ext),
            "x_top": xt, "x_bottom": xb,
            "y_top": top, "y_bottom": bot,
            "h_px": {"read": h(top["read"], bot["read"]),
                     "tight": h(top["tight"], bot["tight"]),
                     "generous": h(top["generous"], bot["generous"])},
            "h_frac": {kk: round(vv2 / H, 5) for kk, vv2 in
                       {"read": h(top["read"], bot["read"]),
                        "tight": h(top["tight"], bot["tight"]),
                        "generous": h(top["generous"], bot["generous"])}.items()},
            "lean_px_over_edge": int(abs(vv[np.searchsorted(rr, bot["read"]) - 1] -
                                          vv[np.searchsorted(rr, top["read"])])),
            "slant_pxrow": {"top_face": round(top_slant, 3), "ground_face": round(bot_slant, 3)},
            "occluder_notches_rows": notches,
        }
    res["thresholds"][name] = entry

print(json.dumps(res, indent=1))
if a.json:
    with open(a.json, "w") as f:
        json.dump(res, f, indent=1)
