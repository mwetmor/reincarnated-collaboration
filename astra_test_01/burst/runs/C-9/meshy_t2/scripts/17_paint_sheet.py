#!/usr/bin/env python3
"""C-9 meshy_t2 step 13: look at the paint that landed, next to the render.

    python3 scripts/17_paint_sheet.py

Writes overlays/T2_paint_<clip>_<dir>.png for every direction 15_assemble.py
accepted: the unlit render on top, Astra's paint-over under it, every frame,
with the game's ground row drawn and each frame's IoU against the render's
own mask printed on the cell. Reading the IoU next to the picture it came
from is the point -- a number on its own does not say whether 0.935 is a
knee that moved or a tail that vanished.

Also writes overlays/T2_paint_status.png: one row per direction of all 32,
so what is painted, what is refused and what has not been fired yet is one
picture rather than three lists.

And, once EbSynth has run, overlays/T2_sprites_<clip>.png: the finished
sprites, all eight directions, every frame, with each row marked PAINTED (the
two Astra directions) or EBS (propagated from two keys). Reading them in one
grid is the only way to see whether the propagated six sit in the same world
as the painted two -- per-direction IoU cannot say whether the COLOUR matches.
"""
import json, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
SPR = os.path.join(ROOT, "sprites_t2")
OVER = os.path.join(ROOT, "overlays")
PAPER = (250, 249, 247)
BG = (238, 236, 232)
SOLE = 398
CROP = (135, 235, 410, 425)
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
CLIPS = [("idle", 12), ("walk", 12), ("run", 8), ("attack", 12)]


def load(p, crop=CROP):
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    bg = Image.new("RGBA", im.size, BG + (255,))
    bg.alpha_composite(im)
    return bg.convert("RGB").crop(crop)


def pair_sheet(man, clip, d, n):
    e = man["states"][clip][d]
    tw = 250
    th = int(tw * (CROP[3] - CROP[1]) / (CROP[2] - CROP[0]))
    im = Image.new("RGB", (tw * n, th * 2 + 30), PAPER)
    dr = ImageDraw.Draw(im)
    dr.text((8, 8), "C-9 T2 manticore  %s %s  variant %s  -  render (top) vs Astra "
                    "paint-over (bottom).  IoU %.3f..%.3f, matte area x%.2f"
            % (clip.upper(), d, e["variant"], e["iou_min"],
               max(r["iou"] for r in e["per_frame"]), e["area_ratio_max"]),
            fill=(25, 25, 25))
    for i in range(n):
        for r, p in enumerate([
                os.path.join(OUT, clip, "colour", d, "%s_%s_%02d.png" % (clip, d, i)),
                os.path.join(SPR, clip, d, "%s_%s_%02d.png" % (clip, d, i))]):
            t = load(p)
            if t is None:
                continue
            t = t.resize((tw, th), Image.LANCZOS)
            d2 = ImageDraw.Draw(t)
            y = (SOLE - CROP[1]) * th / (CROP[3] - CROP[1])
            d2.line([(0, y), (tw, y)], fill=(210, 130, 130))
            lab = str(i) if r == 0 else "%d  IoU %.3f" % (i, e["per_frame"][i]["iou"])
            d2.text((5, 4), lab, fill=(40, 40, 40))
            im.paste(t, (i * tw, 26 + r * th))
    p = os.path.join(OVER, "T2_paint_%s_%s.png" % (clip, d))
    im.save(p)
    print("wrote", p, im.size)


def status_sheet(man):
    cw, ch = 132, 22
    W = 150 + cw * 8
    H = 40 + ch * len(CLIPS)
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)
    dr.text((8, 8), "C-9 T2 manticore  PAINT STATUS  (32 directions = 4 clips x 8)",
            fill=(20, 20, 20))
    for c, d in enumerate(DIRS):
        dr.text((150 + c * cw + 4, 24), d, fill=(60, 60, 60))
    for r, (clip, n) in enumerate(CLIPS):
        y = 38 + r * ch
        dr.text((8, y + 4), clip.upper(), fill=(20, 20, 20))
        for c, d in enumerate(DIRS):
            e = (man["states"].get(clip) or {}).get(d)
            if e is None:
                col, txt = (222, 222, 224), "not fired"
            elif not e["assembled"]:
                col, txt = (232, 176, 176), "refused"
            else:
                col = (176, 224, 184)
                txt = "%s %.3f" % (e["variant"], e["iou_mean"])
            dr.rectangle([150 + c * cw + 2, y, 150 + (c + 1) * cw - 2, y + ch - 3],
                         fill=col)
            dr.text((150 + c * cw + 6, y + 4), txt, fill=(30, 30, 30))
    p = os.path.join(OVER, "T2_paint_status.png")
    im.save(p)
    print("wrote", p, im.size)


def sprites_strip(clip, n):
    """All eight directions of a finished clip, painted rows marked."""
    crop = (135, 235, 410, 425)
    tw = 175
    th = int(tw * (crop[3] - crop[1]) / (crop[2] - crop[0]))
    W = 96 + tw * n
    H = 26 + th * 8
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)
    dr.text((8, 8), "C-9 T2 manticore  %s  sprites_t2, all 8 directions x %d "
                    "frames (S=0, SE=45, E=90 ...).  E and SE are Astra "
                    "paint-overs; the other six are EbSynth from two keys."
            % (clip.upper(), n), fill=(22, 22, 22))
    any_found = False
    for r, d in enumerate(DIRS):
        y = 22 + r * th
        tag = "PAINT" if d in ("E", "SE") else "EBS"
        dr.text((8, y + th // 2 - 10), d, fill=(20, 20, 20))
        dr.text((8, y + th // 2 + 3), tag,
                fill=(30, 110, 40) if tag == "PAINT" else (110, 90, 30))
        for i in range(n):
            t = load(os.path.join(SPR, clip, d, "%s_%s_%02d.png" % (clip, d, i)), crop)
            if t is None:
                continue
            any_found = True
            im.paste(t.resize((tw, th), Image.LANCZOS), (96 + i * tw, y))
        dr.line([(0, y), (W, y)], fill=(216, 216, 216))
    if not any_found:
        return None
    p = os.path.join(OVER, "T2_sprites_%s.png" % clip)
    im.save(p)
    print("wrote", p, im.size)
    return p


def main():
    mp = os.path.join(SPR, "manifest.json")
    if not os.path.exists(mp):
        raise SystemExit("run 15_assemble.py first")
    man = json.load(open(mp))
    os.makedirs(OVER, exist_ok=True)
    for clip, n in CLIPS:
        for d in DIRS:
            e = (man["states"].get(clip) or {}).get(d)
            if e and e.get("assembled") and e.get("kind") == "painted":
                pair_sheet(man, clip, d, n)
    status_sheet(man)
    for clip, n in CLIPS:
        sprites_strip(clip, n)


if __name__ == "__main__":
    main()
