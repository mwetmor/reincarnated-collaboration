#!/usr/bin/env python3
"""C-9 image bake-off, JOB 1 build: does the candidate's sheet build as well as NB-1_b's did?

    python3 06_measure_j1_build.py

The kit instrument (56_kit_measure.py), pointed at two barbarians: each Tripo build is
rendered orthographically at pitch 0 every 5 degrees; the azimuth that best matches its
sheet's FRONT view is its front; the four cardinal renders are then scored against the four
views of THE SHEET IT WAS BUILT FROM -- front, left at +90, back at +180, right at +270, the
convention every build in this run has confirmed -- and the swapped assignment is scored too,
so a mirrored build cannot pass as a good one.

    reference   nb_t8/nb_b_tripo.glb   against NB-1_b    (Astra; the approved barbarian)
    candidate   j1_build/nbp_a_tripo.glb against J1_nbp_a (Nano Banana Pro, best sheet)

Both builds are raw Tripo output, unreduced, from the same placement and arguments.
"""
import json
import pathlib
import subprocess

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
C9 = HERE.parent
PROBE = C9 / "t10_barrow" / "54_kit_probe.py"
QUAD = {"front": (0, 0), "right": (1, 0), "back": (0, 1), "left": (1, 1)}
BUILDS = {
    "astra_b (NB-1_b)": (C9 / "nb_t8/nb_b_tripo.glb", C9 / "nb_t8/nb1_b_rgba.png"),
    "nbp_a": (HERE / "j1_build/nbp_a_tripo.glb", HERE / "mattes/J1_nbp_a_rgba.png"),
}


def views(matte):
    a = np.asarray(Image.open(matte).convert("RGBA"))[..., 3] > 128
    H, W = a.shape
    out = {}
    for v, (c, r) in QUAD.items():
        q = a[r * H // 2:(r + 1) * H // 2, c * W // 2:(c + 1) * W // 2]
        lab, n = ndimage.label(q)
        m = lab == 1 + int(np.argmax(ndimage.sum(q, lab, range(1, n + 1))))
        ys, xs = np.nonzero(m)
        out[v] = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return out


def sil(p):
    a = np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128
    ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b, n=256):
    def fit(m):
        s = n / max(m.shape)
        q = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize(
            (max(1, round(m.shape[1] * s)), max(1, round(m.shape[0] * s))), Image.BILINEAR)) > 127
        o = np.zeros((n, n), bool)
        y, x = (n - q.shape[0]) // 2, (n - q.shape[1]) // 2
        o[y:y + q.shape[0], x:x + q.shape[1]] = q
        return o
    A, B = fit(a), fit(b)
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def main() -> None:
    rep = {}
    for name, (glb, matte) in BUILDS.items():
        tag = "ref" if name.startswith("astra") else "cand"
        out = HERE / "j1_build" / ("probe_%s" % tag)
        if not list(out.glob("*_stats.json")):
            out.mkdir(parents=True, exist_ok=True)
            subprocess.run(["blender", "--background", "--python", str(PROBE), "--", str(glb),
                            str(out), "0", "5", "512"], check=True, capture_output=True)
        st = json.loads(next(out.glob("*_stats.json")).read_text())
        az = {int(p.stem.split("az")[1]): p for p in out.glob("*_az*.png")}
        sv = views(matte)
        curve = sorted(((iou(sil(p), sv["front"]), a) for a, p in az.items()), reverse=True)

        def at(a):
            a %= 360
            return sil(az[min(az, key=lambda k: min(abs(k - a), 360 - abs(k - a)))])

        def four_at(a0):
            return {"front": iou(at(a0), sv["front"]), "back": iou(at(a0 + 180), sv["back"]),
                    "left": iou(at(a0 + 90), sv["left"]), "right": iou(at(a0 + 270), sv["right"])}
        # FRONT AND BACK ARE ONE SILHOUETTE ON A SYMMETRIC FIGURE. A man in an A-pose casts
        # nearly the same outline from the front and from behind, so "the azimuth that best
        # matches the FRONT view" is a coin toss between two answers 180 degrees apart -- and
        # on NB-1_b's build it came up BACK (265), which then scored the profiles swapped and
        # read as a mirrored model. The side views are not symmetric (the face, the braid, the
        # feet), so they decide: both candidates are scored under the fixed convention and the
        # one with the higher four-view total is the front.
        cands = [curve[0][1], (curve[0][1] + 180) % 360]
        A0 = max(cands, key=lambda a: sum(four_at(a).values()))
        f_iou = iou(at(A0), sv["front"])
        four = four_at(A0)
        swapped = (iou(at(A0 + 270), sv["left"]) + iou(at(A0 + 90), sv["right"])) / 2
        asis = (four["left"] + four["right"]) / 2
        rep[name] = {"glb": str(glb), "front_azimuth": A0, "front_candidates": cands,
                     "front_iou": round(f_iou, 3),
                     "front_spread": round(f_iou - curve[-1][0], 3),
                     "sheet_iou": {k: round(v, 3) for k, v in four.items()},
                     "sheet_iou_mean": round(float(np.mean(list(four.values()))), 3),
                     "side_pair_asis": round(asis, 3), "side_pair_swapped": round(swapped, 3),
                     "tris": st["tris"], "islands": st["islands"], "open_boundary_edges": st["boundary_edges"]}
        r = rep[name]
        print("%-18s front az %3d | sheet IoU mean %.3f %s | sides as-is %.3f swapped %.3f | tris %d islands %d"
              % (name, A0, r["sheet_iou_mean"], r["sheet_iou"], asis, swapped, r["tris"], r["islands"]))
    (HERE / "score_j1_build.json").write_text(json.dumps(rep, indent=1) + "\n")


if __name__ == "__main__":
    main()
