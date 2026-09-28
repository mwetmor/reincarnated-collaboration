#!/usr/bin/env python3
"""C-9 meshy_t2 step 9b: the report sheets.

    python3 scripts/12_sheets.py

Writes into overlays/:
  T2_extremes.png     the rig's extreme poses per clip, E view, skeleton drawn
                      over the rendered sprite. The extreme frames are the
                      ones 09_deform.py picked by measurement (largest joint
                      deviation, worst stretch, most collapsed faces, closest
                      paw pass), not by eye.
  T2_walk_8dir.png    the walk, all eight directions, every frame.
  T2_<clip>_E.png     every frame of each clip in E, with the game's ground
                      row drawn at 398.
"""
import json, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
OVER = os.path.join(ROOT, "overlays")
os.makedirs(OVER, exist_ok=True)
BG = (238, 236, 232)
PAPER = (250, 249, 247)
SOLE = 398
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
LIMB = {"thigh": (255, 90, 90), "shin": (255, 150, 90), "hcannon": (255, 210, 90),
        "hpaw": (255, 250, 140), "shoulder": (90, 190, 255), "upperarm": (110, 230, 255),
        "forearm": (150, 255, 235), "fcannon": (190, 255, 210), "fpaw": (225, 255, 225),
        "spine": (190, 150, 255), "chest": (215, 180, 255), "hips": (255, 120, 220),
        "neck": (150, 255, 150), "head": (110, 255, 110), "root": (150, 150, 150),
        "tail": (255, 175, 110)}


def colour(name):
    return LIMB.get(name.split(".")[0].rstrip("_0123456789"), (255, 255, 255))


def load(clip, d, i, crop=None):
    p = os.path.join(OUT, clip, "colour", d, "%s_%s_%02d.png" % (clip, d, i))
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    bg = Image.new("RGBA", im.size, BG + (255,))
    bg.alpha_composite(im)
    im = bg.convert("RGB")
    return im.crop(crop) if crop else im


def project(M, osc, res, p):
    x = M[0][0] * p[0] + M[0][1] * p[1] + M[0][2] * p[2] + M[0][3]
    y = M[1][0] * p[0] + M[1][1] * p[1] + M[1][2] * p[2] + M[1][3]
    return (res / 2 + x / osc * res, res / 2 - y / osc * res)


def union_bbox(clips, dirs, pad=8, aspect=None):
    lo = [10 ** 9, 10 ** 9]; hi = [-1, -1]
    for clip, n in clips:
        for d in dirs:
            for i in range(n):
                p = os.path.join(OUT, clip, "guides_mask", d,
                                 "mask_%s_%02d.png" % (d, i))
                if not os.path.exists(p):
                    p = os.path.join(OUT, clip, "colour", d,
                                     "%s_%s_%02d.png" % (clip, d, i))
                if not os.path.exists(p):
                    continue
                al = Image.open(p).convert("RGBA").getchannel("A")
                bb = al.point(lambda v: 255 if v > 128 else 0).getbbox()
                if not bb:
                    continue
                lo[0] = min(lo[0], bb[0]); lo[1] = min(lo[1], bb[1])
                hi[0] = max(hi[0], bb[2]); hi[1] = max(hi[1], bb[3])
    x0, y0, x1, y1 = lo[0] - pad, lo[1] - pad, hi[0] + pad, hi[1] + pad
    if aspect:
        w, h = x1 - x0, y1 - y0
        if w / h < aspect:
            need = aspect * h - w
            x0 -= need / 2; x1 += need / 2
        else:
            need = w / aspect - h
            y0 -= need / 2; y1 += need / 2
    return (int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))


def extremes_sheet(dump, deform, clips):
    tw = 330
    crop = (135, 235, 410, 425)
    th = int(tw * (crop[3] - crop[1]) / (crop[2] - crop[0]))
    ncol = max(len(deform["clips"][c]["extreme_frames"]) for c, _ in clips)
    W = 150 + tw * ncol
    H = 34 + th * len(clips)
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)
    dr.text((10, 10), "C-9 T2 manticore  RIG EXTREMES, E view, game scale "
                      "(512 frame, 110.185 px/m, sole row 398).  Frames chosen by "
                      "09_deform.py: max joint deviation, worst stretch, most "
                      "collapsed faces, closest paw pass.", fill=(25, 25, 25))
    for r, (clip, n) in enumerate(clips):
        y = 30 + r * th
        fr = deform["clips"][clip]["extreme_frames"]
        dr.text((10, y + th // 2 - 16), clip.upper(), fill=(25, 25, 25))
        s = deform["clips"][clip]["summary"]
        dr.text((10, y + th // 2 + 2), "stretch %.0f mm" % s["elong_max_mm"], fill=(90, 90, 90))
        dr.text((10, y + th // 2 + 16), "dig %.0f mm" % (1000 * s["deepest_below_ground_m"]),
                fill=(90, 90, 90))
        for c, i in enumerate(fr):
            base = load(clip, "E", i)
            if base is None:
                continue
            d2 = ImageDraw.Draw(base)
            d2.line([(0, SOLE), (512, SOLE)], fill=(205, 120, 120))
            row = dump["clips"][clip]["frames"][i]
            M = row["cams"]["E"]
            for bn, b in row["bones"].items():
                h = project(M, dump["ortho_scale"], dump["frame"], b["head"])
                t = project(M, dump["ortho_scale"], dump["frame"], b["tail"])
                d2.line([h, t], fill=colour(bn), width=2)
                d2.ellipse([h[0] - 2, h[1] - 2, h[0] + 2, h[1] + 2], fill=(20, 20, 20))
            tile = base.crop(crop).resize((tw, th), Image.LANCZOS)
            d3 = ImageDraw.Draw(tile)
            d3.text((6, 6), "%s f%02d" % (clip, i), fill=(30, 30, 30))
            im.paste(tile, (150 + c * tw, y))
        dr.line([(0, y), (W, y)], fill=(210, 210, 210))
    p = os.path.join(OVER, "T2_extremes.png")
    im.save(p); print("wrote", p, im.size)


def dir_strip(clip, n, name):
    crop = (135, 240, 410, 425)
    tw = 190
    th = int(tw * (crop[3] - crop[1]) / (crop[2] - crop[0]))
    W = 70 + tw * n
    H = 26 + th * 8
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)
    dr.text((8, 8), "C-9 T2 manticore  %s, all 8 directions x %d frames "
                    "(S=0, SE=45, E=90 ... the game's convention)"
            % (clip.upper(), n), fill=(25, 25, 25))
    for r, d in enumerate(DIRS):
        y = 22 + r * th
        dr.text((8, y + th // 2 - 5), d, fill=(25, 25, 25))
        for i in range(n):
            t = load(clip, d, i, crop)
            if t is None:
                continue
            t = t.resize((tw, th), Image.LANCZOS)
            im.paste(t, (70 + i * tw, y))
        dr.line([(0, y), (W, y)], fill=(215, 215, 215))
    p = os.path.join(OVER, name)
    im.save(p); print("wrote", p, im.size)


def clip_strip(clip, n):
    crop = (135, 240, 410, 425)
    tw = 250
    th = int(tw * (crop[3] - crop[1]) / (crop[2] - crop[0]))
    im = Image.new("RGB", (tw * n, th + 24), PAPER)
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "C-9 T2 manticore  %s, E, every frame" % clip.upper(), fill=(25, 25, 25))
    for i in range(n):
        t = load(clip, "E", i, crop)
        if t is None:
            continue
        t = t.resize((tw, th), Image.LANCZOS)
        d2 = ImageDraw.Draw(t)
        d2.line([(0, (SOLE - crop[1]) * th / (crop[3] - crop[1])),
                 (tw, (SOLE - crop[1]) * th / (crop[3] - crop[1]))], fill=(210, 130, 130))
        d2.text((5, 5), str(i), fill=(40, 40, 40))
        im.paste(t, (i * tw, 20))
    p = os.path.join(OVER, "T2_%s_E.png" % clip)
    im.save(p); print("wrote", p, im.size)


def main():
    dump = json.load(open(os.path.join(ROOT, "work", "bonedump.json")))
    deform = json.load(open(os.path.join(ROOT, "work", "deform.json")))
    clips = [("idle", 12), ("walk", 12), ("run", 8), ("attack", 12)]
    extremes_sheet(dump, deform, clips)
    dir_strip("walk", 12, "T2_walk_8dir.png")
    for c, n in clips:
        clip_strip(c, n)


if __name__ == "__main__":
    main()
