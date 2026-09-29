#!/usr/bin/env python3
"""C-9 T9-1a: score the corrected cells and choose a variant per OBJECT.

Same measures as the first pass, run on the cells 10b_bands_and_cells.py cut rather than on
an even grid split. The first pass scored two of the five objects on crops that did not
contain them and returned plausible numbers for both, so the scores here supersede it
entirely rather than being compared with it.

  mirror_iou   RIGHT against LEFT MIRRORED. Four views of one object have one constraint a
               drawing cannot fake: the profiles are each other's mirror. It is the fault a
               multiview build cannot recover from, so it leads.
  self_iou     FRONT and BACK against their own mirrors -- a drifted three-quarter shows here.
  height_cv    Coefficient of variation of the four subject heights: "one scale", as a number.
  width_cv     Same for width, which is what a flat object like a coil is sized by.
"""
import json
import pathlib

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
VIEWS = ["front", "right", "back", "left"]
OBJECTS = ["snag", "post", "stump", "rope", "raven"]


def sil(p: pathlib.Path):
    a = np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128
    ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b) -> float:
    h, w = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])

    def pad(m):
        o = np.zeros((h, w), bool)
        o[(h - m.shape[0]) // 2:(h - m.shape[0]) // 2 + m.shape[0],
          (w - m.shape[1]) // 2:(w - m.shape[1]) // 2 + m.shape[1]] = m
        return o

    A, B = pad(a), pad(b)
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def main() -> None:
    rep, picks = {}, {}
    for obj in OBJECTS:
        print("\n%-6s %-12s %-11s %-10s %-9s %s" % (obj, "mirror_iou", "self_front",
                                                    "self_back", "height_cv", "width_cv"))
        for v in ("a", "b"):
            ps = [HERE / "cells" / ("%s_%s_%s.png" % (obj, v, n)) for n in VIEWS]
            if not all(p.exists() for p in ps):
                continue
            s = [sil(p) for p in ps]
            hs = [x.shape[0] for x in s]
            ws = [x.shape[1] for x in s]
            r = {"mirror_iou": round(iou(s[1], s[3][:, ::-1]), 3),
                 "self_iou_front": round(iou(s[0], s[0][:, ::-1]), 3),
                 "self_iou_back": round(iou(s[2], s[2][:, ::-1]), 3),
                 "heights_px": hs, "widths_px": ws,
                 "height_cv": round(float(np.std(hs) / np.mean(hs)), 4),
                 "width_cv": round(float(np.std(ws) / np.mean(ws)), 4)}
            rep.setdefault(obj, {})[v] = r
            print("   %s   %-12.3f %-11.3f %-10.3f %-9.4f %.4f   h %s  w %s"
                  % (v, r["mirror_iou"], r["self_iou_front"], r["self_iou_back"],
                     r["height_cv"], r["width_cv"], hs, ws))
        rows = rep.get(obj, {})
        if not rows:
            continue
        vs = sorted(rows, key=lambda v: -rows[v]["mirror_iou"])
        if len(vs) == 2 and abs(rows[vs[0]]["mirror_iou"] - rows[vs[1]]["mirror_iou"]) < 0.02:
            key = "width_cv" if obj == "rope" else "height_cv"
            vs = sorted(rows, key=lambda v: rows[v][key])
            why = "mirror within 0.02; lower %s (%.4f)" % (key, rows[vs[0]][key])
        else:
            why = "higher mirror_iou (%.3f vs %.3f)" % (rows[vs[0]]["mirror_iou"],
                                                        rows[vs[-1]]["mirror_iou"])
        picks[obj] = {"variant": vs[0], "why": why}
        print("   -> %s: %s" % (vs[0], why))
    (HERE / "choose_props.json").write_text(
        json.dumps({"scores": rep, "picks": picks}, indent=1) + "\n")


if __name__ == "__main__":
    main()
