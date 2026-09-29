#!/usr/bin/env python3
"""C-9 T4 close-out: the two pictures.

    python3 make_visuals.py

  helm_strip.png   eight evenly spaced frames of every route's helm, stacked,
                   with the reference still's helm in the left column as the
                   thing they were all asked to hold.
  helm_quad.mp4    the four candidates' helms side by side at 2x, each played
                   at ITS OWN fps so the cadence difference is visible rather
                   than normalised away.

THE CROP IS FIXED PER ROUTE -- the union of that route's helm boxes over the
whole clip, padded -- and this is 24_mp4.py's rule, kept for its reason: a box
that tracked the helm every frame would hold the helm still and hide exactly
the wobble the picture exists to show.  The crop would absorb the drift.

The cells ARE scale-normalised to a common helm height, because otherwise
Kling's 169 px helm and Ludo's 91 px helm would be compared at different
magnifications and the bigger one would look more detailed for free.
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t4lib as L
import measure as M

HERE = os.path.dirname(os.path.abspath(__file__))
R = L.RUNS
CELL = 320                 # px per helm cell in both outputs
PAD_FRAC = 0.18            # of the union box, added all round
OUT_FPS = 30
SECONDS = 5.0
BG = (22, 22, 24)
FG = (238, 238, 240)

STRIP = ["kling", "hydra", "forge", "anim", "drive", "astra"]
QUAD = ["kling", "hydra", "forge", "anim"]
NICE = {"kling": "Kling v3 Pro", "hydra": "Ludo tm hydra", "forge": "Ludo tm forge",
        "anim": "Ludo text 'walking'", "drive": "drive (floor)",
        "astra": "Astra per-frame (benchmark)"}


def union_box(cfg, idxs):
    lo = [10 ** 9, 10 ** 9]
    hi = [-10 ** 9, -10 ** 9]
    hh = []
    for i in idxs:
        g = L.frame_geometry(cfg["frames"][i], cfg["kind"])
        y0, y1, x0, x1 = L.helm_box(g["rgb"], g["mask"], g["body"], g["crown"],
                                    g["neck"], g["sole"])
        lo[0] = min(lo[0], x0); lo[1] = min(lo[1], y0)
        hi[0] = max(hi[0], x1); hi[1] = max(hi[1], y1)
        hh.append(g["neck"] - g["crown"])
        del g
    w, h = hi[0] - lo[0], hi[1] - lo[1]
    pad = int(PAD_FRAC * max(w, h))
    return (lo[1] - pad, hi[1] + pad, lo[0] - pad, hi[0] + pad), float(np.median(hh))


def cell_of(path, kind, box, helm_h, target_helm=None):
    """Crop the FIXED box and scale so the helm is target_helm px tall."""
    a = np.asarray(Image.open(path).convert("RGBA")).astype(np.float64)
    rgb = a[..., :3]
    if kind == "alpha":
        m = a[..., 3] > 128
    else:
        g = rgb[..., 1]
        m = ~((g > 110) & (g - np.maximum(rgb[..., 0], rgb[..., 2]) > 45))
    comp = rgb * m[..., None] + np.array(BG) * (~m)[..., None]
    crop = L.crop_pad(comp, *box, fill=float(BG[0]))
    im = Image.fromarray(np.clip(crop, 0, 255).astype(np.uint8))
    if target_helm:
        s = target_helm / max(helm_h, 1e-6)
        im = im.resize((max(8, int(im.width * s)), max(8, int(im.height * s))),
                       Image.LANCZOS)
    c = Image.new("RGB", (CELL, CELL), BG)
    if im.width > CELL or im.height > CELL:
        im.thumbnail((CELL, CELL), Image.LANCZOS)
    c.paste(im, ((CELL - im.width) // 2, (CELL - im.height) // 2))
    return c


def label(img, text, sub=None):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 22], fill=(0, 0, 0))
    d.text((6, 6), text, fill=FG)
    if sub:
        d.text((img.width - 6 - 6 * len(sub), 6), sub, fill=(170, 170, 175))
    return img


def main():
    defs = M.route_defs()
    # the reference still: its own helm, at the same magnification
    gref = L.frame_geometry(M.REF, "green")
    rbox = L.helm_box(gref["rgb"], gref["mask"], gref["body"], gref["crown"],
                      gref["neck"], gref["sole"])
    rh = gref["neck"] - gref["crown"]
    pad = int(PAD_FRAC * (rbox[1] - rbox[0]))
    rbox = (rbox[0] - pad, rbox[1] + pad, rbox[2] - pad, rbox[3] + pad)
    del gref
    TARGET = int(0.42 * CELL)          # helm height inside the cell

    # ---- strip -----------------------------------------------------------
    rows = []
    meta = {}
    for name in STRIP:
        cfg = defs[name]
        n = len(cfg["frames"])
        idxs = [int(round(k * (n - 1) / 7.0)) for k in range(8)]
        box, hh = union_box(cfg, idxs)
        meta[name] = dict(box=[int(v) for v in box], helm_h=round(hh, 1),
                          frames=idxs)
        cells = [cell_of(cfg["frames"][i], cfg["kind"], box, hh, TARGET)
                 for i in idxs]
        rows.append((name, cells, idxs))
        sys.stderr.write("strip %s box=%s helm=%.0f\n" % (name, box, hh))

    refcell = label(cell_of(M.REF, "green", rbox, rh, TARGET), "REFERENCE",
                    "still")
    W = CELL * 9
    Hh = CELL * len(rows) + 26
    strip = Image.new("RGB", (W, Hh), BG)
    d = ImageDraw.Draw(strip)
    d.text((8, 8), "C-9 test 4 -- the helm, 8 evenly spaced frames per route, "
                   "fixed crop per route, scale-normalised", fill=FG)
    for r, (name, cells, idxs) in enumerate(rows):
        y = 26 + r * CELL
        strip.paste(refcell, (0, y))
        for c, (cell, i) in enumerate(zip(cells, idxs)):
            strip.paste(label(cell, NICE[name] if c == 0 else "", "f%d" % i),
                        ((c + 1) * CELL, y))
    strip.save(os.path.join(HERE, "helm_strip.png"))
    print("wrote helm_strip.png", strip.size)

    # ---- quad mp4 --------------------------------------------------------
    cache, boxes = {}, {}
    for name in QUAD:
        cfg = defs[name]
        n = len(cfg["frames"])
        probe = [int(round(k * (n - 1) / 15.0)) for k in range(16)]
        box, hh = union_box(cfg, probe)
        boxes[name] = dict(box=[int(v) for v in box], helm_h=round(hh, 1))
        cache[name] = [np.asarray(cell_of(p, cfg["kind"], box, hh, int(0.52 * CELL)))
                       for p in cfg["frames"]]
        sys.stderr.write("quad %s cached %d cells\n" % (name, len(cache[name])))

    nout = int(OUT_FPS * SECONDS)
    tmp = os.path.join(HERE, "_quadtmp")
    os.makedirs(tmp, exist_ok=True)
    for t in range(nout):
        canvas = Image.new("RGB", (CELL * len(QUAD), CELL + 26), BG)
        dd = ImageDraw.Draw(canvas)
        dd.text((8, 8), "C-9 test 4 -- helms at 2x, each played at its own fps "
                        "(%.1f s)" % SECONDS, fill=FG)
        for c, name in enumerate(QUAD):
            cfg = defs[name]
            src = int(t * cfg["fps"] / OUT_FPS) % len(cache[name])
            cell = Image.fromarray(cache[name][src])
            label(cell, NICE[name], "f%d" % src)
            canvas.paste(cell, (c * CELL, 26))
        canvas.save(os.path.join(tmp, "q_%04d.png" % t))
    mp4 = os.path.join(HERE, "helm_quad.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(OUT_FPS),
                    "-i", os.path.join(tmp, "q_%04d.png"), "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "20", mp4], check=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    print("wrote helm_quad.mp4", os.path.getsize(mp4) // 1024, "KB")

    with open(os.path.join(HERE, "visuals.json"), "w") as f:
        json.dump(dict(cell_px=CELL, pad_frac=PAD_FRAC, out_fps=OUT_FPS,
                       seconds=SECONDS, strip=meta, quad=boxes,
                       crop_rule="fixed per route (union of helm boxes over the "
                                 "clip, padded); a per-frame crop would hold the "
                                 "helm still and hide the wobble"), f, indent=1)


if __name__ == "__main__":
    main()
