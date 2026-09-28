#!/usr/bin/env python3
"""C-9 knight3d: the GATE M-b comparison sheets.

Three rows, one scale, the game's own 512x512 frame:
    GROK        the video cells the game plays today (the reference)
    CUT-OUT     the puppet rig, reproduced from cliffside_B (the comparison)
    3D BODY     this spike

Plus a slow-motion strip: every frame of the 3D body's walk and run, in order,
so the motion can be read frame by frame rather than guessed at from a loop.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
CB = os.path.join(ROOT, "cliffside_B")
K3 = os.path.join(ROOT, "knight3d")
OUT = os.path.join(K3, "out")
SHEETS = os.path.join(K3, "overlays")
os.makedirs(SHEETS, exist_ok=True)
BG = (238, 236, 232)
CROP = (120, 130, 400, 420)          # the part of the 512 frame the knight uses


def load(path):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, BG + (255,))
    bg.alpha_composite(im)
    return bg.convert("RGB").crop(CROP)


def row(paths, tw, th):
    out = []
    for p in paths:
        out.append(load(p).resize((tw, th), Image.LANCZOS) if os.path.exists(p)
                   else Image.new("RGB", (tw, th), (210, 120, 120)))
    return out


def sheet(state, n, picks, tw=250):
    th = int(tw * (CROP[3] - CROP[1]) / (CROP[2] - CROP[0]))
    grok = [os.path.join(CB, "sprites_knight", state, "E", "%s_E_%02d.png" % (state, i))
            for i in picks]
    rig = [os.path.join(OUT, "rig", state, "rig_%s_E_%02d.png" % (state, i)) for i in picks]
    body = [os.path.join(OUT, "sprites", state, "E", "%s_E_%02d.png" % (state, i))
            for i in picks]
    rows = [("GROK video (reference)", grok),
            ("CUT-OUT rig (comparison)", rig),
            ("3D BODY (this spike)", body)]
    lab = 190
    W = lab + tw * len(picks)
    H = th * 3 + 34
    im = Image.new("RGB", (W, H), (250, 249, 247))
    dr = ImageDraw.Draw(im)
    dr.text((10, 10), "C-9 knight3d  GATE M-b   %s, E, game scale (512 frame, "
            "sole y=398)   frames %s of %d" % (state.upper(),
                                               ",".join(str(i) for i in picks), n),
            fill=(30, 30, 30))
    for r, (name, paths) in enumerate(rows):
        y = 30 + r * th
        dr.text((10, y + th // 2 - 4), name, fill=(40, 40, 40))
        for c, tile in enumerate(row(paths, tw, th)):
            im.paste(tile, (lab + c * tw, y))
        dr.line([(0, y), (W, y)], fill=(200, 200, 200))
    p = os.path.join(SHEETS, "M-b_%s_E.png" % state)
    im.save(p)
    print("wrote", p)
    return p


def slowmo(state, n, tw=160):
    th = int(tw * (CROP[3] - CROP[1]) / (CROP[2] - CROP[0]))
    im = Image.new("RGB", (tw * n, th + 24), (250, 249, 247))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "C-9 knight3d  %s, E, all %d frames in order "
            "(slow motion)" % (state.upper(), n), fill=(30, 30, 30))
    for i in range(n):
        p = os.path.join(OUT, "sprites", state, "E", "%s_E_%02d.png" % (state, i))
        im.paste(load(p).resize((tw, th), Image.LANCZOS), (i * tw, 22))
        dr.text((i * tw + 4, 24), str(i), fill=(120, 120, 120))
    out = os.path.join(SHEETS, "M-b_%s_E_slowmo.png" % state)
    im.save(out)
    print("wrote", out)
    return out


def main():
    sheet("walk", 12, [0, 2, 4, 6, 8, 10])
    sheet("run", 8, [0, 1, 3, 5, 7])
    slowmo("walk", 12)
    slowmo("run", 8)
    # a three-row slow strip too, so the motion can be compared frame by frame
    for state, n in (("walk", 12), ("run", 8)):
        tw = 120
        th = int(tw * (CROP[3] - CROP[1]) / (CROP[2] - CROP[0]))
        im = Image.new("RGB", (tw * n + 150, th * 3 + 30), (250, 249, 247))
        dr = ImageDraw.Draw(im)
        dr.text((8, 8), "C-9 knight3d  %s, E, every frame, three ways"
                % state.upper(), fill=(30, 30, 30))
        srcs = [("GROK", os.path.join(CB, "sprites_knight", state, "E", "%s_E_%%02d.png" % state)),
                ("CUT-OUT", os.path.join(OUT, "rig", state, "rig_%s_E_%%02d.png" % state)),
                ("3D BODY", os.path.join(OUT, "sprites", state, "E", "%s_E_%%02d.png" % state))]
        for r, (nm, pat) in enumerate(srcs):
            y = 26 + r * th
            dr.text((8, y + th // 2), nm, fill=(40, 40, 40))
            for i in range(n):
                p = pat % i
                if os.path.exists(p):
                    im.paste(load(p).resize((tw, th), Image.LANCZOS), (150 + i * tw, y))
        out = os.path.join(SHEETS, "M-b_%s_E_strip3.png" % state)
        im.save(out)
        print("wrote", out)


if __name__ == "__main__":
    main()
