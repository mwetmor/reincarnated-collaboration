#!/usr/bin/env python3
"""C-9 meshy_t1: does the Meshy model have its SIDES the right way round, and
does game-E walk to screen-right? (gandalf's two warnings, R-C9-61)

Both are answered against art that is known good rather than by reasoning
about axes: the eight approved painted stills, and the Grok E walk cells.

  SIDES   the bind-pose render at E is compared with the painted E still AND
          with the painted W still, after matching figure height and bbox.
          Silhouette IoU is nearly symmetric on an A-pose so it cannot decide
          this; the COLOUR does, because the knight's heraldry differs side to
          side. Reported per horizontal band so a single global average cannot
          hide a local swap.
  FACING  the rendered E walk is compared with the Grok E cells and with those
          cells MIRRORED. Grok's E knight demonstrably walks to screen-right,
          so if the unmirrored comparison wins, so does ours.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
T1 = os.path.dirname(HERE)
C9 = os.path.dirname(T1)
SEEDS = os.path.join(C9, "artifacts", "seeds")
MASKS = os.path.join(C9, "knight3d", "work", "masks")
SEED = {"E": "seed_E.png", "W": "seed_W.png"}


def still(d):
    rgb = np.asarray(Image.open(os.path.join(SEEDS, SEED[d])).convert("RGB"))
    body = np.load(os.path.join(MASKS, "%s_body.npy" % d))
    return rgb, body


def render(p):
    im = Image.open(p).convert("RGBA")
    a = np.asarray(im)
    return a[..., :3], a[..., 3] > 8


def norm(rgb, m, H=220):
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    sc = H / float(y1 - y0 + 1)
    W = max(int(round((x1 - x0 + 1) * sc)), 4)
    r = np.asarray(Image.fromarray(rgb[y0:y1 + 1, x0:x1 + 1]).resize((W, H), Image.LANCZOS),
                   dtype=np.float64)
    mm = np.asarray(Image.fromarray((m[y0:y1 + 1, x0:x1 + 1] * 255).astype(np.uint8))
                    .resize((W, H), Image.NEAREST)) > 127
    return r, mm


def compare(A, Am, B, Bm, bands=6):
    w = min(A.shape[1], B.shape[1])
    A, Am = A[:, :w], Am[:, :w]
    B, Bm = B[:, :w], Bm[:, :w]
    both = Am & Bm
    out = []
    H = A.shape[0]
    for i in range(bands):
        sl = slice(H * i // bands, H * (i + 1) // bands)
        m = both[sl]
        out.append(float(np.abs(A[sl][m] - B[sl][m]).mean()) if m.any() else None)
    g = float(np.abs(A[both] - B[both]).mean()) if both.any() else None
    iou = float((Am & Bm).sum()) / max((Am | Bm).sum(), 1)
    return g, out, iou


def main():
    bind = sys.argv[1] if len(sys.argv) > 1 else os.path.join(T1, "work", "bind179")
    rep = {"note": "sides and facing, checked against approved art", "sides": {}}
    print("SIDES -- bind render vs the painted stills (mean |RGB| error, lower is the match)")
    for rd in ("E", "W"):
        R, Rm = render(os.path.join(bind, "bind_%s.png" % rd))
        Rn, Rmn = norm(R, Rm)
        row = {}
        for sd in ("E", "W"):
            S, Sm = still(sd)
            Sn, Smn = norm(S, Sm)
            g, bands, iou = compare(Rn, Rmn, Sn, Smn)
            row[sd] = dict(mean_err=round(g, 2), bands=[round(b, 1) if b else None for b in bands],
                           silhouette_iou=round(iou, 4))
            print("  render %s vs still %s : err %6.2f   IoU %.3f   bands %s"
                  % (rd, sd, g, iou, [round(b) if b else None for b in bands]))
        row["verdict"] = "matches same side" if row[rd]["mean_err"] <= row["W" if rd == "E" else "E"]["mean_err"] else "SWAPPED"
        print("    -> %s" % row["verdict"])
        rep["sides"][rd] = row
    rep["sides_verdict"] = ("sides correct" if all(
        rep["sides"][d]["verdict"] == "matches same side" for d in ("E", "W"))
        else "SIDES SWAPPED")
    print("  VERDICT:", rep["sides_verdict"])

    # ---- facing -------------------------------------------------------
    walk = os.path.join(T1, "out", "walk_real", "colour", "E")
    if os.path.isdir(walk):
        grok = os.path.join(C9, "cliffside_B", "sprites_knight", "walk", "E")
        gs = sorted(f for f in os.listdir(grok) if f.endswith(".png"))
        ious, iousm = [], []
        n = len([f for f in os.listdir(walk) if f.endswith(".png")])
        for i in range(n):
            R, Rm = render(os.path.join(walk, "walk_E_%02d.png" % i))
            gi = int(round(i * len(gs) / n)) % len(gs)
            G, Gm = render(os.path.join(grok, gs[gi]))
            Rn, Rmn = norm(R, Rm); Gn, Gmn = norm(G, Gm)
            _, _, a = compare(Rn, Rmn, Gn, Gmn)
            _, _, b = compare(Rn, Rmn, Gn[:, ::-1], Gmn[:, ::-1])
            ious.append(a); iousm.append(b)
        rep["facing"] = dict(iou_vs_grok=round(float(np.mean(ious)), 4),
                             iou_vs_grok_mirrored=round(float(np.mean(iousm)), 4))
        rep["facing"]["verdict"] = ("E walks to screen-right (matches Grok)"
                                    if np.mean(ious) >= np.mean(iousm)
                                    else "E IS MIRRORED -- facing correction wrong")
        print("\nFACING -- rendered E walk vs Grok E cells")
        print("  IoU unmirrored %.4f   mirrored %.4f   -> %s"
              % (np.mean(ious), np.mean(iousm), rep["facing"]["verdict"]))
    json.dump(rep, open(os.path.join(T1, "work", "sides_facing.json"), "w"), indent=1)
    print("wrote work/sides_facing.json")


main()
