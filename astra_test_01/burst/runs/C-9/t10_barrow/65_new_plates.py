#!/usr/bin/env python3
"""C-9 T10-1e: identity plates for four new painting-matched models, cut from the concept.

    python3 65_new_plates.py

Same product as 24_identity_plates.py -- the concept's own pixels at native resolution,
matted onto flat #00ff00, registered in CS9-guides/manifest.json -- but NOT the same masks,
and the reason is measured rather than preferred:

  * SAM2's "heather" class is mostly the dark blue-green JUNIPER bushes (#2, #3, #7, #8,
    #10 by eye), and #6 and #11 are ROCKS labelled heather. A heather plate cut from that
    class would show the painter a juniper. The integration drax's "shrub coverage 0.11"
    was measured against the painting, so the thing missing is the orange-brown heather
    itself, and it has no mask.
  * SAM2 and evf-sam cover the two bedded outcrops only in sub-metre fragments -- their
    union reaches a fraction of either mass.
  * evf-sam's `birch2_dead` rank 1 IS the snag, and is kept, but it stops at the thick
    wood and loses the thinner limbs.

So three masks are cut here, locally, at no fal cost -- which matters, because every cent
of the $3.20 is a fraction of a Tripo build:

  OUTCROPS   HAND-TRACED OUTLINES, stated as such. A pixel classifier plus a closing could
             not separate a snow ledge on a rock from the snow ground behind it (same
             colour; only the pen line divides them) and, closed hard enough to bridge the
             ledges, it swallowed the neighbouring juniper whole. The outline is traced on
             a 20 px grid; inside it, vegetation and ice are removed by hue, and the snow
             on the ledges stays -- it is part of what the object is.
  HEATHER    The warmest DENSE clump of the stated size: hue 12-50 deg, saturation > 0.38,
             width 0.55-0.95 m, ranked by fill. The same classifier also found the
             barbarian's fur, which is why the pick is also checked by eye.
  SNAG       evf-sam's mask, grown GEODESICALLY into desaturated grey wood (never into
             snow, never more than 16 px) so the thin limbs come back and the snow does not.

HOW BIG THEY ARE: the plates carry the painting's own ruler (K = 140.86 px/m) for what the
frame shows, but both outcrops are CUT BY THE FRAME EDGE, so their full extent is not in
the painting. Their target sizes are the brief's (gandalf: 4-6 m across, 1.5-2.5 m high),
and the plate says what is visible rather than pretending it is the whole.
"""
import hashlib
import json
import pathlib

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts"
GUIDES = ART / "CS9-guides"
CONCEPT = ART / "T10C-barrow" / "T10C-barrow_a.png"
PLATES = HERE / "plates"
K = 140.86
COS_P = 0.602462172508240
GREEN = (0, 255, 0)

# (x, y) in concept pixels, traced on a 20 px grid
POLY = {
    "outcrop_a": [(0, 790), (40, 768), (100, 752), (125, 745), (130, 705), (160, 692),
                  (200, 700), (215, 740), (205, 790), (205, 830), (215, 880), (235, 910),
                  (240, 960), (225, 1000), (200, 1023), (0, 1023)],
    "outcrop_b": [(1318, 470), (1345, 468), (1382, 430), (1395, 385), (1420, 368),
                  (1445, 372), (1455, 400), (1450, 440), (1480, 445), (1535, 438),
                  (1535, 660), (1480, 650), (1450, 640), (1420, 625), (1380, 600),
                  (1350, 575), (1330, 545), (1315, 510)],
}
HEATHER_BBOX = (1355, 565, 1458, 651)       # warm clump rank 0: 0.74 m, fill 0.52
SNAG_BOX = (1150, 770, 1420, 1000)


def classes(im):
    hsv = np.asarray(im.convert("HSV")).astype(np.float32)
    h, s, v = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    snow = ((v > 0.74) & (s < 0.22)) | ((h > 185) & (h < 250) & (s < 0.33) & (v > 0.55))
    ice = (h > 185) & (h < 235) & (s >= 0.33)
    warm = (h >= 12) & (h <= 50) & (s > 0.38) & (v > 0.22) & (v < 0.92)
    green = (h > 55) & (h < 200) & (s > 0.10) & (v < 0.62)
    wood = (s < 0.22) & (v > 0.30) & (v < 0.78) & ~snow
    return snow, ice, warm, green, wood


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def largest(m):
    lab, n = ndimage.label(m)
    if n == 0:
        return m
    return lab == 1 + int(np.argmax(ndimage.sum(m, lab, range(1, n + 1))))


def poly_mask(pts, shape):
    img = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(img).polygon(pts, fill=255)
    return np.asarray(img) > 127


def main() -> None:
    im = Image.open(CONCEPT).convert("RGB")
    rgb = np.asarray(im)
    snow, ice, warm, green, wood = classes(im)
    H, W = rgb.shape[:2]
    masks, notes = {}, {}

    for name, pts in POLY.items():
        m = poly_mask(pts, (H, W)) & ~ndimage.binary_dilation(green | warm, disk(1)) & ~ice
        m = largest(ndimage.binary_opening(m, disk(1)))
        masks[name] = ndimage.binary_fill_holes(m)
        notes[name] = "hand-traced outline (%d vertices, 20 px grid); vegetation and ice " \
                      "removed by hue inside it; CUT BY THE FRAME EDGE" % len(pts)

    x0, y0, x1, y1 = HEATHER_BBOX
    box = np.zeros((H, W), bool)
    box[max(0, y0 - 8):y1 + 9, max(0, x0 - 8):x1 + 9] = True
    hm = ndimage.binary_closing(ndimage.binary_opening(warm & box, disk(1)), disk(4))
    masks["heather_clump"] = largest(ndimage.binary_fill_holes(hm))
    notes["heather_clump"] = "warm-hue clump (h 12-50, s > 0.38), densest of the 0.55-0.95 m " \
                             "candidates; checked by eye (the classifier also finds fur)"

    dead = np.asarray(Image.open(HERE / "work" / "evf_a_birch2_dead.png").convert("L")) > 127
    lab, n = ndimage.label(dead)
    sz = ndimage.sum(dead, lab, range(1, n + 1))
    snag = lab == 1 + int(np.argsort(-sz)[1])
    sx0, sy0, sx1, sy1 = SNAG_BOX
    allow = np.zeros((H, W), bool)
    allow[sy0:sy1, sx0:sx1] = True
    allow &= wood
    grown = snag.copy()
    for _ in range(16):                          # geodesic: one pixel per step, wood only
        grown = (ndimage.binary_dilation(grown, disk(1)) & allow) | snag
    masks["dead_tree"] = ndimage.binary_fill_holes(largest(grown))
    notes["dead_tree"] = "evf-sam birch2_dead rank 1 (the snag), grown geodesically <= 16 px " \
                         "into desaturated grey wood to recover the thin limbs (+%d px)" \
                         % int(masks["dead_tree"].sum() - snag.sum())

    PLATES.mkdir(exist_ok=True)
    man = json.loads((GUIDES / "manifest.json").read_text())
    rec = {}
    for name, m in masks.items():
        ys, xs = np.nonzero(m)
        bx0, by0, bx1, by1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
        p = 10
        cx0, cy0, cx1, cy1 = max(0, bx0 - p), max(0, by0 - p), min(W, bx1 + p + 1), min(H, by1 + p + 1)
        crop = rgb[cy0:cy1, cx0:cx1].copy()
        crop[~m[cy0:cy1, cx0:cx1]] = GREEN
        local = PLATES / ("T10_%s.png" % name)
        Image.fromarray(crop).save(local)
        guide = GUIDES / ("t10_%s_plate.png" % name)
        Image.fromarray(crop).save(guide)
        sha = hashlib.sha256(guide.read_bytes()).hexdigest()
        man[guide.name] = sha
        edge = [e for e, t in (("left", bx0 == 0), ("top", by0 == 0),
                               ("right", bx1 == W - 1), ("bottom", by1 == H - 1)) if t]
        rec[name] = {"plate": str(local.relative_to(HERE)), "guide": str(guide.relative_to(ART.parent.parent.parent)),
                     "sha256": sha, "screen_bbox": [bx0, by0, bx1, by1],
                     "visible_width_m": round((bx1 - bx0 + 1) / K, 2),
                     "visible_height_if_upright_m": round((by1 - by0 + 1) / (K * COS_P), 2),
                     "cut_by_frame": edge, "mask_px": int(m.sum()), "method": notes[name]}
        print("%-14s bbox %-24s visible %.2f m wide, %.2f m if upright  %s  %s"
              % (name, rec[name]["screen_bbox"], rec[name]["visible_width_m"],
                 rec[name]["visible_height_if_upright_m"],
                 ("CUT BY FRAME " + ",".join(edge)) if edge else "", sha[:12]))
    (GUIDES / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    (HERE / "new_plates.json").write_text(json.dumps(
        {"_what": "C-9 T10-1e identity plates for outcrop_a, outcrop_b, heather_clump and "
                  "dead_tree, cut from T10C-barrow_a with local masks (no fal cost).",
         "px_per_metre": K, "assets": rec}, indent=1) + "\n")
    print("registered %d plates in %s" % (len(rec), GUIDES / "manifest.json"))


if __name__ == "__main__":
    main()
