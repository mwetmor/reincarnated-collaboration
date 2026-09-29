#!/usr/bin/env python3
"""C-9 T4 close-out: is the 2D fallback the same instrument as the pos-matched one?

    python3 validate_fallback.py          # writes fallback_check.json

THE QUESTION.  measure.py replaces 21_drift.py's pos-space correspondence with
a 2D rigid registration, because Kling and Ludo return video and there is no
pos pass to match against.  That substitution has to be CHECKED rather than
argued: if the two disagree, every number in drift.json is measuring something
other than what T1 and T2 measured, and the table cannot be read against them.

THE ONE SEQUENCE WHERE BOTH CAN RUN is the knight's own Astra walk E:
knight3d/out/sprites_fit_astra_a/ is per-frame paint registered to
knight3d/out/guides_fit/, which carries pos, mask and part passes.  So both
instruments are pointed at the same twelve frames and the same helm.

  pos-matched   21_drift.py's method, ported: for each pixel of frame i, the
                matching pixel of frame j is the nearest neighbour in POS
                space (the rest-pose bind position, invariant to the pose);
                colours only are compared; matches further than POS_TOL apart
                are dropped as occlusion.  Helm region from the PART guide --
                exactly the helm and visor meshes, no detection involved.
  2D fallback   measure.py's method: crop placed on the part, resampled,
                best integer translation, same blur and erosion.

Three sequences are run through both, so the comparison is of a RANKING and
not of a single number: the per-frame Astra paint, the raw 3D render of the
same cycle (which cannot drift -- one texture on one mesh), and the paint in
shuffled order (the negative control).  What has to survive is the ORDER and
the ratios; the absolute values are not expected to match, because the two
instruments admit different pixels.
"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t4lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
K3 = os.path.join(L.RUNS, "knight3d", "out")
GD = os.path.join(K3, "guides_fit", "walk", "E")
N = 12
POS_TOL = 0.010           # 21_drift.py's value, unchanged
HEAD_PARTS = ("helm", "visor")


def guides(i):
    pos = np.asarray(Image.open(os.path.join(GD, "pos_%02d.png" % i))
                     .convert("RGB")).astype(np.float64) / 255.0
    m = np.asarray(Image.open(os.path.join(GD, "mask_%02d.png" % i))
                   .convert("L")) > 127
    part = np.asarray(Image.open(os.path.join(GD, "part_%02d.png" % i))
                      .convert("RGB"))
    return pos, m, part


def head_mask(part):
    idx = json.load(open(os.path.join(K3, "guides_index.json")))["part_colours"]
    hit = np.zeros(part.shape[:2], bool)
    for p in HEAD_PARTS:
        c = np.array(idx[p], dtype=np.uint8)
        hit |= (np.abs(part.astype(int) - c.astype(int)).max(-1) < 6)
    return hit


def load_rgb(path, mask):
    a = np.asarray(Image.open(path).convert("RGBA")).astype(np.float64)
    rgb, al = a[..., :3], a[..., 3] > 128
    w = (al & mask).astype(np.float64)
    num = np.stack([ndi.gaussian_filter(rgb[..., k] * w, L.BLUR_SIGMA)
                    for k in range(3)], -1)
    den = np.maximum(ndi.gaussian_filter(w, L.BLUR_SIGMA), 1e-6)[..., None]
    return num / den, al


def pos_pair(seq, i, j):
    pos_i, m_i, part_i = guides(i)
    pos_j, m_j, _ = guides(j)
    rgb_i, a_i = load_rgb(seq[i], m_i)
    rgb_j, a_j = load_rgb(seq[j], m_j)
    k = np.ones((2 * L.ERODE_PX + 1,) * 2)
    use_i = ndi.binary_erosion(m_i & a_i, k)
    use_j = ndi.binary_erosion(m_j & a_j, k)
    if use_i.sum() < 50 or use_j.sum() < 50:
        return None
    tree = cKDTree(pos_j[use_j])
    dist, idx = tree.query(pos_i[use_i], k=1)
    ok = dist < POS_TOL
    if ok.sum() < 50:
        return None
    res = np.abs(rgb_i[use_i][ok] - rgb_j[use_j][idx[ok]]).mean(-1)
    hm = head_mask(part_i)[use_i][ok]
    return dict(body=float(res.mean()),
                head=float(res[hm].mean()) if hm.sum() > 20 else None,
                matched_frac=float(ok.mean()))


def pos_series(seq, order):
    b, h, mf = [], [], []
    for k in range(1, len(order)):
        r = pos_pair(seq, order[k], order[k - 1])
        if not r:
            continue
        b.append(r["body"]); mf.append(r["matched_frac"])
        if r["head"] is not None:
            h.append(r["head"])
    return L.stats(b), L.stats(h), round(float(np.mean(mf)), 3)


def twod_series(seq, order):
    recs = []
    for p in seq:
        g = L.frame_geometry(p, "alpha")
        hp, hm, _ = L.helm_patch(g)
        bp, bm, _ = L.body_patch(g)
        recs.append((hp, hm, bp, bm))
        del g
    b, h = [], []
    for k in range(1, len(order)):
        a, c = recs[order[k]], recs[order[k - 1]]
        h.append(L.residual(a[0], a[1], c[0], c[1])[0])
        b.append(L.residual(a[2], a[3], c[2], c[3])[0])
    return L.stats(b), L.stats(h)


def main():
    paint = [os.path.join(K3, "sprites_fit_astra_a", "walk", "E",
                          "walk_E_%02d.png" % i) for i in range(N)]
    render = [os.path.join(K3, "sprites_fit", "walk", "E",
                           "walk_E_%02d.png" % i) for i in range(N)]
    rng = np.random.default_rng(7)
    sh = list(rng.permutation(N))
    while sh == list(range(N)):
        sh = list(rng.permutation(N))
    seqs = [("paint", paint, list(range(N))),
            ("render(floor)", render, list(range(N))),
            ("paint shuffled(control)", paint, sh)]
    rep = dict(what=__doc__.strip().splitlines()[0],
               pos_tol=POS_TOL, blur_sigma=L.BLUR_SIGMA, erode_px=L.ERODE_PX,
               head_parts=list(HEAD_PARTS), frames=N, rows={})
    print("%-26s %-28s %-28s" % ("", "pos-matched (21_drift.py)", "2D fallback (measure.py)"))
    print("%-26s %13s %13s %13s %13s" % ("sequence", "body", "head", "body", "head"))
    for name, seq, order in seqs:
        pb, ph, mf = pos_series(seq, order)
        tb, th = twod_series(seq, order)
        rep["rows"][name] = dict(pos_matched=dict(body=pb, head=ph, matched_frac=mf),
                                 two_d=dict(body=tb, head=th))
        print("%-26s %13.2f %13.2f %13.2f %13.2f"
              % (name, pb["median"], ph["median"], tb["median"], th["median"]))

    def med(row, inst, reg):
        return rep["rows"][row][inst][reg]["median"]
    verdict = {}
    for inst in ("pos_matched", "two_d"):
        for reg in ("body", "head"):
            verdict["%s_%s_paint_over_floor" % (inst, reg)] = round(
                med("paint", inst, reg) / med("render(floor)", inst, reg), 2)
            verdict["%s_%s_shuffled_over_paint" % (inst, reg)] = round(
                med("paint shuffled(control)", inst, reg) / med("paint", inst, reg), 2)
    rep["ratios"] = verdict
    rep["reading"] = (
        "The two instruments are compared on RATIOS, not on absolute values: "
        "they admit different pixels (pos-matching drops the unmatched "
        "fraction; the 2D crop admits whatever is in the box) so the levels "
        "differ by construction. What must agree is (a) paint scores above "
        "floor on both, and (b) shuffled scores above paint on both -- drift "
        "that is real and drift that has temporal structure.")
    with open(os.path.join(HERE, "fallback_check.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print()
    for k, v in verdict.items():
        print("  %-42s %s" % (k, v))
    print("wrote fallback_check.json")


if __name__ == "__main__":
    main()
