#!/usr/bin/env python3
"""Mask overlays -- the LOOK step.  Every instrument in this run that returned
a confident wrong answer was caught by a picture or a null, never by reading
the code.  So the masks get looked at before the statistics are believed."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vfx_lap2_battery import luma, sat_val  # noqa: E402
from vfx_ref_anchor_true import (chroma, clutter_mask, eff_support,  # noqa: E402
                                 eff_tight, hud_map)
from vfx_true_recon import hue_sat, probe, valid_map  # noqa: E402


def grab(path, t, w, h):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path,
                          "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out[:w * h * 3], np.uint8).reshape(h, w, 3).copy()


def tint(img, M, rgb, alpha=0.55):
    img[M] = (img[M] * (1 - alpha) + np.array(rgb, np.float32) * alpha).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--t", type=float, nargs="+", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--crop", type=int, nargs=4, default=None)
    a = ap.parse_args()
    w, h, *_ = probe(a.clip)
    V = valid_map(h, w)
    HUD = hud_map(h, w)
    ev = Path(a.evidence)
    ev.mkdir(parents=True, exist_ok=True)
    for t in a.t:
        f = grab(a.clip, t, w, h)
        L = luma(f)
        sA, _ = sat_val(f)
        hh, _ = hue_sat(f)
        C = chroma(f)
        cl, text, bars = clutter_mask(f, L, sA, hh, C)
        region = V & ~HUD & ~cl
        E, lab, sz, bar_px = eff_tight(hh, C, L, region)
        SUP = eff_support(E)
        core = (lab == int(np.argmax(sz) + 1)) if sz.size else np.zeros_like(E)
        aux = (lab > 0) & ~core
        # top-0.5% of the SCENE, for the ownership picture
        sc = V & ~HUD
        thr = np.percentile(L[sc], 99.5)
        top = sc & (L >= thr)

        img = f.copy()
        tint(img, HUD, (40, 40, 200), 0.35)
        tint(img, bars, (255, 0, 255), 0.5)
        tint(img, text, (255, 255, 0), 0.35)
        tint(img, SUP & ~E, (0, 160, 255), 0.35)
        tint(img, aux, (255, 140, 0), 0.75)
        tint(img, core, (0, 255, 0), 0.75)
        tint(img, top & ~E, (255, 0, 0), 0.9)
        name = "overlay-%s-t%05.2f" % (a.tag, t)
        Image.fromarray(img).save(ev / (name + ".png"))
        if a.crop:
            x, y, cw, ch = a.crop
            Image.fromarray(img[y:y + ch, x:x + cw]).resize(
                (cw * 2, ch * 2), Image.NEAREST).save(ev / (name + "-zoom.png"))
        print("%s  effect %6d px (core %6d, aux %6d, %d comps)  bars-dropped %5d  clutter %6d  top-tail %5d (%.3f in effect)"
              % (name, int(E.sum()), int(core.sum()), int(aux.sum()), int(sz.size), int(bar_px),
                 int(cl.sum()), int(top.sum()),
                 float((top & E).sum()) / max(int(top.sum()), 1)))


if __name__ == "__main__":
    main()
