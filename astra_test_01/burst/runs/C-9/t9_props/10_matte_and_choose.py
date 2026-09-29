#!/usr/bin/env python3
"""C-9 T9-1a: matte the prop sheets, cut the four views out of each, and choose a variant
by MEASURING view consistency rather than by looking at them.

The sheets came back with their #00ff00 plates lost (white on A and B, a brown gradient on
C), so the cut-out is a segmentation matte -- fal BiRefNet v2, the same model and the same
arguments the barbarian's own views were cut with in nb_t8/01_matte_views.py.

WHAT IS MEASURED, and why each one is the thing that breaks a multiview build:

  mirror_iou   The RIGHT view against the LEFT view MIRRORED. Four views of one object
               have one hard constraint a picture cannot fake: the two profiles are each
               other's mirror. This is the measure that catches a bird drawn facing the
               same way twice -- the exact fault T9P-C was retried for -- and it catches it
               without my having to decide which of two small dark birds is pointing which
               way at a glance.
  self_iou_0/2 Front and back against their own mirrors. A front view of a post, a stump, a
               coil or a bird is close to bilaterally symmetric; a three-quarter view that
               has drifted is not.
  height_cv    Coefficient of variation of the four cut-out heights. "One scale" was the
               instruction; this is it as a number.
  foot_spread  Spread of the four subjects' baselines within their cells, in cell heights.

IoU is computed on silhouettes after centring each on its own bounding box, so it measures
SHAPE agreement and not where in the cell the painter happened to put things.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts"

# sheet -> (cols, rows, {object: row}); columns are always front, right, back, left
SHEETS = {
    "T9P-A": {"grid": (2, 2), "objects": {"snag": "quad"}},
    "T9P-B": {"grid": (4, 2), "objects": {"post": 0, "stump": 1}},
    "T9P-C": {"grid": (4, 2), "objects": {"rope": 0, "raven": 1}},
}
VIEWS = ["front", "right", "back", "left"]


def matte(src: pathlib.Path, dst: pathlib.Path) -> Image.Image:
    if dst.exists():
        return Image.open(dst).convert("RGBA")
    import fal_client
    url = fal_client.upload_file(str(src))
    r = fal_client.subscribe("fal-ai/birefnet/v2", arguments={
        "image_url": url, "model": "General Use (Heavy)",
        "operating_resolution": "2048x2048", "output_format": "png",
        "refine_foreground": True})
    subprocess.run(["curl", "-s", "-L", "-o", str(dst), r["image"]["url"]], check=True)
    return Image.open(dst).convert("RGBA")


def cells(im: Image.Image, spec: dict, obj: str) -> list:
    W, H = im.size
    if spec["objects"][obj] == "quad":          # 2x2: TL front, TR right, BL back, BR left
        boxes = [(0, 0), (1, 0), (0, 1), (1, 1)]
        return [im.crop((c * W // 2, r * H // 2, (c + 1) * W // 2, (r + 1) * H // 2))
                for c, r in boxes]
    cols, rows = spec["grid"]
    r = spec["objects"][obj]
    return [im.crop((c * W // cols, r * H // rows, (c + 1) * W // cols, (r + 1) * H // rows))
            for c in range(cols)]


def sil(c: Image.Image) -> tuple:
    a = np.asarray(c)[..., 3] > 128
    if not a.any():
        return None, None
    ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1], (int(xs.min()), int(ys.min()),
                                                             int(xs.max() + 1), int(ys.max() + 1))


def iou(a: np.ndarray, b: np.ndarray) -> float:
    if a is None or b is None:
        return 0.0
    h = max(a.shape[0], b.shape[0])
    w = max(a.shape[1], b.shape[1])

    def pad(m):
        o = np.zeros((h, w), bool)
        y = (h - m.shape[0]) // 2
        x = (w - m.shape[1]) // 2
        o[y:y + m.shape[0], x:x + m.shape[1]] = m
        return o

    A, B = pad(a), pad(b)
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def main() -> int:
    rep = {}
    (HERE / "work").mkdir(exist_ok=True)
    (HERE / "views").mkdir(exist_ok=True)
    for sid, spec in SHEETS.items():
        for v in ("a", "b"):
            src = ART / sid / ("%s_%s.png" % (sid, v))
            if not src.exists():
                continue
            im = matte(src, HERE / "work" / ("%s_%s_rgba.png" % (sid, v)))
            print("matte %s_%s %s  alpha>0 %.3f"
                  % (sid, v, im.size, (np.asarray(im)[..., 3] > 0).mean()))
            for obj in spec["objects"]:
                cs = cells(im, spec, obj)
                sils, boxes = zip(*[sil(c) for c in cs])
                hs = [0 if b is None else b[3] - b[1] for b in boxes]
                ch = cs[0].size[1]
                feet = [0 if b is None else b[3] / ch for b in boxes]
                rec = {
                    "variant": v, "sheet": str(src),
                    "sha256": hashlib.sha256(src.read_bytes()).hexdigest()[:16],
                    "heights_px": hs,
                    "height_cv": round(float(np.std(hs) / max(np.mean(hs), 1)), 4),
                    "foot_spread": round(float(max(feet) - min(feet)), 4),
                    "mirror_iou": round(iou(sils[1], None if sils[3] is None else sils[3][:, ::-1]), 3),
                    "self_iou_front": round(iou(sils[0], None if sils[0] is None else sils[0][:, ::-1]), 3),
                    "self_iou_back": round(iou(sils[2], None if sils[2] is None else sils[2][:, ::-1]), 3),
                    "boxes": [list(b) if b else None for b in boxes],
                }
                rep.setdefault(obj, {})[v] = rec
                for i, c in enumerate(cs):
                    c.save(HERE / "views" / ("%s_%s_%s.png" % (obj, v, VIEWS[i])))

    picks = {}
    print()
    for obj, rows in rep.items():
        print("%-6s %-27s %-10s %-10s %-9s %s" % ("", "mirror_iou(R vs mirrored L)",
                                                  "self_front", "self_back", "height_cv", "foot_spread"))
        for v, r in rows.items():
            print("   %s   %-27.3f %-10.3f %-10.3f %-9.4f %.4f   heights %s"
                  % (v, r["mirror_iou"], r["self_iou_front"], r["self_iou_back"],
                     r["height_cv"], r["foot_spread"], r["heights_px"]))
        # THE RULE, fixed before the numbers: the two profiles being each other's mirror is
        # the constraint a multiview build cannot recover from, so mirror_iou leads. Only if
        # the two variants are within 0.02 of each other there does one-scale break the tie.
        vs = sorted(rows, key=lambda v: -rows[v]["mirror_iou"])
        if len(vs) == 2 and abs(rows[vs[0]]["mirror_iou"] - rows[vs[1]]["mirror_iou"]) < 0.02:
            vs = sorted(rows, key=lambda v: rows[v]["height_cv"])
            why = "mirror within 0.02; lower height_cv (%.4f)" % rows[vs[0]]["height_cv"]
        else:
            why = "higher mirror_iou (%.3f vs %.3f)" % (
                rows[vs[0]]["mirror_iou"], rows[vs[-1]]["mirror_iou"])
        picks[obj] = {"variant": vs[0], "why": why}
        print("   -> %s: %s\n" % (vs[0], why))

    (HERE / "choose_props.json").write_text(
        json.dumps({"scores": rep, "picks": picks}, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
