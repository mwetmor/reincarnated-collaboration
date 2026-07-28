#!/usr/bin/env python3
"""
G-6 pass 6c: locate the skill tooltip by FFT template-matching the literal
string "Current Level" (harvested from frame 352).

Passes 6a (gold border) and 6b (white text block) both failed: the panel frame
shares the tooltip's gold, and the tooltip body text is warm-grey, not white.
The one thing guaranteed present in every skill tooltip and present NOWHERE
else on screen is the heading "Current Level". Matching that anchor gives the
tooltip's left edge and its heading row exactly; the box is then taken as a
fixed offset from the anchor (tooltip layout is constant, only its position
moves).

Normalised cross-correlation via FFT (scipy.signal.fftconvolve) on the
binarised text mask -- brightness-invariant and fast enough for a full-panel
search per frame.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.signal import fftconvolve

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6")
TIP = OUT / "tooltips"

SEARCH = (455, 240, 1530, 890)
ANCHOR_FRAME = 352
ANCHOR_BOX = (664, 502, 800, 522)      # "Current Level" heading, native, f352
# tooltip box relative to the anchor's top-left (measured on f352)
REL = (-26, -172, 316, 232)            # dx0, dy0, dx1, dy1


def ink(rgb):
    """Heading-ink mask.

    The "Current Level :" heading is warm gold -- sampled on f352 as
    ~(145,128,90) with the mode bin at (128,112,80). A plain brightness mask
    (first attempt) matched every bright thing on screen and the anchor search
    collapsed. Keying on the gold instead isolates the heading, because the
    tooltip's body text is grey and the tree carries no gold text at all.
    """
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    m = (r > 105) & (r < 210) & (g > 90) & (b < 125) & (r - b > 30) & (abs(r - g) < 45)
    return m.astype(np.float32)


def load(fid):
    with Image.open(SRC / f"Screenshot ({fid}).png") as im:
        return np.asarray(im.convert("RGB"))


def ncc_map(img, tpl):
    t = tpl - tpl.mean()
    tn = np.linalg.norm(t)
    num = fftconvolve(img, t[::-1, ::-1], mode="valid")
    ones = np.ones_like(t)
    s1 = fftconvolve(img, ones[::-1, ::-1], mode="valid")
    s2 = fftconvolve(img * img, ones[::-1, ::-1], mode="valid")
    n = t.size
    var = np.maximum(s2 - s1 * s1 / n, 1e-6)
    return num / (np.sqrt(var) * tn + 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("--scale", type=int, default=3)
    ap.add_argument("--thresh", type=float, default=0.55)
    a = ap.parse_args()
    TIP.mkdir(parents=True, exist_ok=True)
    ax0, ay0, ax1, ay1 = ANCHOR_BOX
    tpl = ink(load(ANCHOR_FRAME)[ay0:ay1, ax0:ax1])
    sx0, sy0, sx1, sy1 = SEARCH
    res = {}
    for f in (int(v) for v in a.frames.split(",")):
        img = ink(load(f)[sy0:sy1, sx0:sx1])
        m = ncc_map(img, tpl)
        j, i = np.unravel_index(np.argmax(m), m.shape)
        score = float(m[j, i])
        ax, ay = sx0 + i, sy0 + j
        box = (ax + REL[0], ay + REL[1], ax + REL[2], ay + REL[3])
        box = (max(0, box[0]), max(0, box[1]), min(1920, box[2]), min(1080, box[3]))
        ok = score >= a.thresh
        res[str(f)] = {"anchor": [ax, ay], "score": round(score, 3),
                       "box": list(box), "quality": "LOCATED" if ok else "LOW_CONF"}
        print(f"f{f}: score={score:.3f} anchor=({ax},{ay}) box={box} "
              f"{'LOCATED' if ok else 'LOW_CONF'}")
        c = Image.fromarray(load(f)[box[1]:box[3], box[0]:box[2]])
        c.save(TIP / f"T3_f{f}_native.png")
        c.resize((c.width * a.scale, c.height * a.scale), Image.LANCZOS).save(
            TIP / f"T3_f{f}_x{a.scale}.png")
    json.dump(res, open(OUT / "g6-tooltip-boxes3.json", "w"), indent=1, default=int)


if __name__ == "__main__":
    main()
