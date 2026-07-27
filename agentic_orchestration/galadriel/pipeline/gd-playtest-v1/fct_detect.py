#!/usr/bin/env python3
"""
FCT (floating combat text) detector for the GD play-test v1 video.

WHAT THE INSTRUMENT ACTUALLY IS (measured 2026-07-26, round 2)
--------------------------------------------------------------
F-1  FCT exists and renders as near-WHITE, LOW-SATURATION digits with a dark
     outline, drawn over the world layer. It is NOT the green
     `character.LogData` overlay (which is saturated green) and it is NOT the
     PlayStats panel (which is fixed to the right column).

F-2  FCT is MULTI-SCALE. A number spawns large (~16 px glyph height at 1080p),
     then RISES and SHRINKS and FADES over its lifetime (~10 px by end of
     life). A fixed-height template reader therefore misses most of a number's
     frames. Detection is by blob geometry; the read is taken at the frame
     where the blob is LARGEST (spawn frame), never averaged across life.

F-3  Because a single damage instance persists for many frames while moving,
     naive per-frame counting multiply-counts it. Instances must be TRACKED
     across frames (upward drift + shrink) and collapsed to one event.

Detection mask, in order of what each clause excludes:
  bright   min(R,G,B) > 140      -- text core is near-white
  achromatic (max-min) < 45      -- excludes the saturated green debug overlay,
                                    orange quest tracker, red/blue globes
  world region only              -- excludes panel column and HUD tray
"""

import numpy as np

# World region: everything outside the right-hand panel column and the bottom
# HUD tray and the top-centre enemy nameplate.
WORLD = dict(x0=0, x1=1320, y0=60, y1=930)

BRIGHT_MIN = 140
CHROMA_MAX = 45


def fct_mask(rgb, region=WORLD):
    sub = rgb[region["y0"]:region["y1"], region["x0"]:region["x1"]].astype(np.int16)
    mx = sub.max(axis=2)
    mn = sub.min(axis=2)
    return (mn > BRIGHT_MIN) & ((mx - mn) < CHROMA_MAX)


def components(mask, min_px=8):
    """4-connected components via iterative flood fill on a boolean array."""
    h, w = mask.shape
    lab = np.zeros((h, w), dtype=np.int32)
    out = []
    cur = 0
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        cur += 1
        stack = [(y0, x0)]
        lab[y0, x0] = cur
        pts = []
        while stack:
            y, x = stack.pop()
            pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = cur
                    stack.append((ny, nx))
        if len(pts) >= min_px:
            p = np.array(pts)
            out.append(dict(n=len(pts), y0=int(p[:, 0].min()), y1=int(p[:, 0].max()),
                            x0=int(p[:, 1].min()), x1=int(p[:, 1].max())))
    return out


def group_glyphs(comps, max_gap=6, max_dy=4):
    """Merge glyph components that sit on a common baseline into NUMBERS."""
    if not comps:
        return []
    cs = sorted(comps, key=lambda c: (round((c["y0"] + c["y1"]) / 6), c["x0"]))
    groups = []
    for c in cs:
        placed = False
        for g in groups:
            if (abs(((c["y0"] + c["y1"]) / 2) - g["cy"]) <= max_dy
                    and 0 <= c["x0"] - g["x1"] <= max_gap):
                g["x1"] = max(g["x1"], c["x1"])
                g["y0"] = min(g["y0"], c["y0"])
                g["y1"] = max(g["y1"], c["y1"])
                g["parts"].append(c)
                g["cy"] = (g["y0"] + g["y1"]) / 2
                placed = True
                break
        if not placed:
            groups.append(dict(x0=c["x0"], x1=c["x1"], y0=c["y0"], y1=c["y1"],
                               cy=(c["y0"] + c["y1"]) / 2, parts=[c]))
    return groups
