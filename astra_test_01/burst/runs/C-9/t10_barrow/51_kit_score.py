#!/usr/bin/env python3
"""C-9 T10-1b: score both variants of each kit object and pick one by mirror IoU.

Same measures as 32_score_sheets.py. The T10 props had identity plates -- crops of the
concept painting -- so a variant could be chosen against what the scene actually contains.
These six were painted from words and there is no plate, so the ONE constraint left is the
one a drawing cannot fake: RIGHT and LEFT are the same object from opposite sides, so each
is the other's mirror. That is what picks the variant here, and it is the fault a multiview
build cannot recover from, so leading with it is not a compromise.

Two notes on reading the numbers:

  * THE LOG'S SIDE VIEWS ARE ITS ENDS. Its RIGHT and LEFT columns are end-on discs, not
    side elevations, so its mirror_iou compares two discs and its height_cv/width_cv are
    meaningless across the four (a 2.6 m log seen end-on is 0.3 m wide, correctly). Its
    consistency is checked on FRONT vs BACK instead, reported as `pair_iou`.
  * `pair_iou` is FRONT against BACK MIRRORED, which is the second constraint four views of
    one object owe each other, and it is the one that catches a painter who drew the back
    of a different object.
"""
import json
import pathlib
import sys

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
VIEWS = ["front", "right", "back", "left"]
SETS = {"kit": ("kit_work", ["rocks", "stump", "log", "cairn", "skull", "shield"]),
        "kit2": ("kit_work2", ["rocks", "stump", "skull", "boulder"]),
        "kit3": ("kit_work3", ["outcrop_a", "outcrop_b", "heather_clump", "dead_tree"])}
SET = sys.argv[1] if len(sys.argv) > 1 else "kit"
WORK, OBJECTS = HERE / SETS[SET][0], SETS[SET][1]
END_ON = {"log"}          # RIGHT/LEFT are end-on views; scale spread across views is real


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
        print("\n%-7s %-11s %-9s %-11s %-10s %-9s %s"
              % (obj, "mirror_iou", "pair_iou", "self_front", "self_back", "height_cv", "width_cv"))
        for v in ("a", "b"):
            ps = [WORK / "cells" / ("%s_%s_%s.png" % (obj, v, n)) for n in VIEWS]
            if not all(p.exists() for p in ps):
                continue
            s = [sil(p) for p in ps]
            hs = [x.shape[0] for x in s]
            ws = [x.shape[1] for x in s]
            r = {"mirror_iou": round(iou(s[1], s[3][:, ::-1]), 3),
                 "pair_iou": round(iou(s[0], s[2][:, ::-1]), 3),
                 "self_iou_front": round(iou(s[0], s[0][:, ::-1]), 3),
                 "self_iou_back": round(iou(s[2], s[2][:, ::-1]), 3),
                 "heights_px": hs, "widths_px": ws,
                 "height_cv": round(float(np.std(hs) / np.mean(hs)), 4),
                 "width_cv": round(float(np.std(ws) / np.mean(ws)), 4),
                 "px": [int((x).sum()) for x in s]}
            rep.setdefault(obj, {})[v] = r
            print("   %s   %-11.3f %-9.3f %-11.3f %-10.3f %-9.4f %.4f   h %s  w %s"
                  % (v, r["mirror_iou"], r["pair_iou"], r["self_iou_front"],
                     r["self_iou_back"], r["height_cv"], r["width_cv"], hs, ws))
        rows = rep.get(obj, {})
        if not rows:
            continue
        vs = sorted(rows, key=lambda v: -rows[v]["mirror_iou"])
        if len(vs) == 2 and abs(rows[vs[0]]["mirror_iou"] - rows[vs[1]]["mirror_iou"]) < 0.02:
            vs = sorted(rows, key=lambda v: -rows[v]["pair_iou"])
            why = "mirror within 0.02; higher pair_iou (%.3f vs %.3f)" % (
                rows[vs[0]]["pair_iou"], rows[vs[-1]]["pair_iou"])
        else:
            why = "higher mirror_iou (%.3f vs %.3f)" % (rows[vs[0]]["mirror_iou"],
                                                        rows[vs[-1]]["mirror_iou"])
        picks[obj] = {"variant": vs[0], "why": why,
                      "mirror_iou": rows[vs[0]]["mirror_iou"],
                      "pair_iou": rows[vs[0]]["pair_iou"]}
        print("   -> %s: %s" % (vs[0], why))
    (WORK / "choose_kit.json").write_text(
        json.dumps({"scores": rep, "picks": picks}, indent=1) + "\n")


if __name__ == "__main__":
    main()
