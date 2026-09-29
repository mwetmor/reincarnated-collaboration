#!/usr/bin/env python3
"""C-9 meshy_t2 step 15: correspondence-compensated drift.

    python3 scripts/21_drift.py <clip> <dir> --sets render=out/... paint=... x=... y=...
    python3 scripts/21_drift.py --selfcheck

THE QUESTION. Does the CREATURE change between consecutive frames, over and
above the change the animation itself requires? A plain frame-to-frame
difference cannot answer that: the animal moves, so every pixel changes, and
a walk scores worse than an idle for reasons that have nothing to do with
identity. That is the metric that was measuring the wrong thing.

THE COMPENSATION. Every frame ships with a `pos` guide: the REST-POSE bind
position of the surface point under each pixel, baked per vertex before
skinning and therefore INVARIANT to the animation. Two pixels with the same
pos value are the same point on the body, whatever the pose or the frame. So
for each pixel of frame i+1, the matching pixel of frame i is found by nearest
neighbour in POS SPACE, not in screen space, and only the COLOURS are
compared. A pose change contributes nothing; a helm that changes shape, or a
face that is redrawn, contributes everything.

  drift(i, i+1) = mean |colour_{i+1}(p) - colour_i(nearest_pos(p))|   in 0-255

Matches further than POS_TOL apart in pos space are dropped: that is a surface
point visible in one frame and not the other, which is occlusion, not drift.

REPORTED over two regions, because the knight's rejection was about a helm and
a visor rather than about a whole figure: the WHOLE body, and the HEAD/FACE
alone, isolated from the `part` guide by the head bone's flat colour.

LOW-PASS BEFORE COMPARING, and the reason is measured rather than stylistic.
Compared pixel to pixel, the RENDER -- which has no drift at all, being one
unlit texture on one mesh -- scored 9.8 against 10.2 shuffled. Tightening the
pos tolerance from 0.035 to 0.002 (3.8 mm on the body) barely moved it: 8.3.
The floor is not correspondence error, it is TEXTURE DETAIL. The manticore's
ribs and fur strokes are finer than the pos guide can resolve at 8 bits, so
two genuinely-corresponding pixels land on different strokes and disagree by
~10/255 no matter how well they are matched.

Drift in the sense that got the knight rejected is a LOW-frequency property --
a helm that changes shape, a face redrawn at 3-10 px scale -- so both frames
are blurred (sigma 3 px, mask-normalised so the background cannot bleed in)
and the silhouette is eroded 2 px before matching. That drops the render floor
to 1.9 and leaves the per-frame paint at 4.3 body / 5.0 head: a real
separation where there was none.

THE NEGATIVE CONTROL is a shuffled frame order, and it reads on a sequence
that HAS drift, not on the render. On the render, true and shuffled are both
at the floor (1.89 vs 2.18) and should be -- every frame shows the same
creature, so which pairs you compare does not matter. On the per-frame paint
it separates (4.29 vs 5.50 body, 5.03 vs 6.08 head): consecutive cells are
more alike than distant ones, which is drift with temporal structure.
"""
import argparse, json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
POS_TOL = 0.010          # normalised bind-bbox units (~18 mm on this body)
BLUR_SIGMA = 3.0         # px; see the low-pass note above
ERODE_PX = 2             # drop the anti-aliased silhouette rim
CLIPS = {"idle": 12, "walk": 12, "run": 8, "attack": 12}


def srgb(x):
    x = np.clip(np.asarray(x, dtype=np.float64), 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(x, 1 / 2.4) - 0.055)


def guides(clip, d, i):
    pp = os.path.join(OUT, clip, "guides_pos", d, "pos_%s_%02d.png" % (d, i))
    mp = os.path.join(OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i))
    ap = os.path.join(OUT, clip, "guides_part", d, "part_%s_%02d.png" % (d, i))
    pos = np.asarray(Image.open(pp).convert("RGBA")).astype(np.float64)
    m = np.asarray(Image.open(mp).convert("RGBA"))[..., 3] > 128
    part = np.asarray(Image.open(ap).convert("RGBA")).astype(np.float64)
    return pos[..., :3] / 255.0, m, part[..., :3] / 255.0


def head_mask(clip, d, i, part):
    rp = json.load(open(os.path.join(OUT, clip, "render_%s.json" % clip)))
    col = srgb(np.array(rp["guides"]["bone_colours"]["head"]))
    return np.abs(part - col).max(-1) < 0.02


def load_rgb(path, mask=None):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(np.float64)
    rgb, al = a[..., :3], a[..., 3] > 128
    if BLUR_SIGMA:
        w = (al & (mask if mask is not None else al)).astype(np.float64)
        num = np.stack([ndi.gaussian_filter(rgb[..., k] * w, BLUR_SIGMA)
                        for k in range(3)], -1)
        den = np.maximum(ndi.gaussian_filter(w, BLUR_SIGMA), 1e-6)[..., None]
        rgb = num / den
    return rgb, al


def drift_pair(clip, d, i, j, seq):
    """Mean colour residual from frame j to frame i, matched in pos space."""
    pos_i, m_i, part_i = guides(clip, d, i)
    pos_j, m_j, _ = guides(clip, d, j)
    rgb_i, a_i = load_rgb(seq[i], m_i)
    rgb_j, a_j = load_rgb(seq[j], m_j)
    use_i = ndi.binary_erosion(m_i & a_i, np.ones((2 * ERODE_PX + 1,) * 2))
    use_j = ndi.binary_erosion(m_j & a_j, np.ones((2 * ERODE_PX + 1,) * 2))
    if use_i.sum() < 50 or use_j.sum() < 50:
        return None
    src = pos_j[use_j]
    tree = cKDTree(src)
    tgt = pos_i[use_i]
    dist, idx = tree.query(tgt, k=1)
    ok = dist < POS_TOL
    if ok.sum() < 50:
        return None
    ci = rgb_i[use_i][ok]
    cj = rgb_j[use_j][idx[ok]]
    res = np.abs(ci - cj).mean(-1)
    hm = head_mask(clip, d, i, part_i)[use_i][ok]
    return dict(n=int(ok.sum()), matched_frac=round(float(ok.mean()), 4),
                body=float(res.mean()),
                head=(float(res[hm].mean()) if hm.sum() > 20 else None),
                head_px=int(hm.sum()))


def series(clip, d, seq, order=None):
    n = len(seq)
    order = order if order is not None else list(range(n))
    body, head, mf = [], [], []
    for k in range(n):
        i = order[k]
        j = order[(k - 1) % n]
        r = drift_pair(clip, d, i, j, seq)
        if r is None:
            continue
        body.append(r["body"]); mf.append(r["matched_frac"])
        if r["head"] is not None:
            head.append(r["head"])
    if not body:
        return None
    return dict(pairs=len(body),
                body_mean=round(float(np.mean(body)), 2),
                body_max=round(float(np.max(body)), 2),
                head_mean=round(float(np.mean(head)), 2) if head else None,
                head_max=round(float(np.max(head)), 2) if head else None,
                matched_frac=round(float(np.mean(mf)), 3))


def seq_paths(root, clip, d, n, pat=None):
    pat = pat or "%s_%s_%%02d.png" % (clip, d)
    return [os.path.join(root, clip, d, pat % i) for i in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", default="walk")
    ap.add_argument("--dirs", default="E,SE,S")
    ap.add_argument("--sets", nargs="*", default=[],
                    help="name=root (root/<clip>/<dir>/<clip>_<dir>_NN.png)")
    ap.add_argument("--selfcheck", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    sets = {}
    if args.selfcheck or not args.sets:
        sets["render"] = None            # special-cased below
    for s in args.sets:
        k, v = s.split("=", 1)
        sets[k] = v

    rep = dict(clip=args.clip, pos_tol=POS_TOL, blur_sigma=BLUR_SIGMA,
               erode_px=ERODE_PX,
               render_floor="the render scores ~1.9 body / ~2.0 head; that is "
                            "the instrument's floor, not a drift measurement",
               note="mean |dRGB| in 0-255 between consecutive frames after "
                    "matching pixels by the pos guide; shuffled order is the "
                    "negative control",
               sets={}, control={})
    n = CLIPS[args.clip]
    rng = np.random.default_rng(7)
    for name, root in sets.items():
        per_dir = {}
        for d in args.dirs.split(","):
            if name == "render":
                seq = [os.path.join(OUT, args.clip, "colour", d,
                                    "%s_%s_%02d.png" % (args.clip, d, i))
                       for i in range(n)]
            else:
                seq = seq_paths(root, args.clip, d, n)
            if not all(os.path.exists(p) for p in seq):
                continue
            per_dir[d] = series(args.clip, d, seq)
            sh = list(rng.permutation(n))
            while sh == list(range(n)):
                sh = list(rng.permutation(n))
            per_dir[d + "_shuffled"] = series(args.clip, d, seq, order=sh)
        if per_dir:
            rep["sets"][name] = per_dir
    print("clip %s   (mean |dRGB| 0-255, lower = steadier)" % args.clip)
    print("%-10s %-4s %9s %9s %9s %9s %8s" % ("set", "dir", "body", "head",
                                              "body(shuf)", "head(shuf)", "matched"))
    for name, per_dir in rep["sets"].items():
        for d in args.dirs.split(","):
            a = per_dir.get(d)
            if not a:
                continue
            b = per_dir.get(d + "_shuffled") or {}
            print("%-10s %-4s %9.2f %9s %9s %9s %8.3f"
                  % (name, d, a["body_mean"],
                     ("%.2f" % a["head_mean"]) if a["head_mean"] else "-",
                     ("%.2f" % b["body_mean"]) if b else "-",
                     ("%.2f" % b["head_mean"]) if b.get("head_mean") else "-",
                     a["matched_frac"]))
    if args.out:
        json.dump(rep, open(args.out, "w"), indent=1)
        print("wrote", args.out)


if __name__ == "__main__":
    main()
