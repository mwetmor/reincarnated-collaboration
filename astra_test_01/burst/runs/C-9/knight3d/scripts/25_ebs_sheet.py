#!/usr/bin/env python3
"""C-9 knight3d: the EbSynth comparison sheet (R-C9-60).

Four columns at the frames gandalf asked for: the 3D raw render, Astra's
per-frame paint-over (the thing propagation is trying to avoid paying for),
EbSynth propagated from one key, and from two keys blended by temporal
distance. Everything flattened on the same ground so the only difference on
screen is the pixels.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out")
BG = (238, 236, 232)
CROP = (185, 160, 355, 400)
ZOOM = 3


def load(p, mask=None):
    """EbSynth has no alpha, so its output arrives on black. Composited as-is
    beside two panels on the light ground, the comparison would be between
    backgrounds rather than between pixels; the guide mask puts every column on
    the same ground."""
    im = Image.open(p).convert("RGBA")
    if mask is not None:
        a = np.asarray(im).copy()
        a[..., 3] = np.where(mask, 255, 0)
        im = Image.fromarray(a)
    bg = Image.new("RGBA", im.size, BG + (255,))
    bg.alpha_composite(im)
    c = bg.convert("RGB").crop(CROP)
    return c.resize((c.width * ZOOM, c.height * ZOOM), Image.LANCZOS)


def main():
    gait = sys.argv[1] if len(sys.argv) > 1 else "walk"
    frames = [3, 6, 9]
    cols = [("3D raw", os.path.join(OUT, "sprites_fit", gait, "E", "%s_E_%%02d.png" % gait)),
            ("Astra per-frame", os.path.join(OUT, "sprites_fit_astra_a", gait, "E",
                                             "%s_E_%%02d.png" % gait)),
            ("EbSynth 1-key (00)", os.path.join(OUT, "ebs_fit", gait, "E", "k1_%02d.png")),
            ("EbSynth 2-key (00,06)", os.path.join(OUT, "ebs_fit", gait, "E", "k2_%02d.png"))]
    w = (CROP[2] - CROP[0]) * ZOOM
    h = (CROP[3] - CROP[1]) * ZOOM
    im = Image.new("RGB", (w * 4 + 70, h * len(frames) + 34), (250, 249, 247))
    dr = ImageDraw.Draw(im)
    dr.text((8, 8), "C-9 knight3d  EbSynth propagation, %s E  (guides: pos w4, part w2, "
            "mask w2)" % gait.upper(), fill=(20, 20, 20))
    for c, (name, _) in enumerate(cols):
        dr.text((70 + c * w + 6, 22), name, fill=(40, 40, 40))
    for r, f in enumerate(frames):
        y = 34 + r * h
        dr.text((8, y + h // 2), "f%02d" % f, fill=(40, 40, 40))
        for c, (_, pat) in enumerate(cols):
            p = pat % f
            mk = None
            if "ebs_fit" in pat:
                mk = np.asarray(Image.open(os.path.join(
                    OUT, "guides_fit", gait, "E", "mask_%02d.png" % f)).convert("L")) > 127
            if os.path.exists(p):
                im.paste(load(p, mk), (70 + c * w, y))
            else:
                dr.rectangle([70 + c * w, y, 70 + (c + 1) * w, y + h], fill=(210, 120, 120))
    out = os.path.join(K3, "overlays", "R-C9-60_ebsynth_%s.png" % gait)
    im.save(out)
    print("wrote", out)


main()
