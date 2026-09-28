#!/usr/bin/env python3
"""C-9 knight3d: the comparison MP4 and the zoomed leg strip (R-C9-58 item 4).

Same layout gandalf used for the M-b video: three panels -- Grok, cut-out rig,
3D body -- each cropped (96,120,416,440) and doubled, played at the Keeper
cadence, then a 1/3-speed section. Plus a LEG STRIP at 3x zoom, because the
defect Matt reported is in the legs and feet and a full-figure panel is too
small to judge it.
"""
import json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out")
CB = os.path.join(os.path.dirname(K3), "cliffside_B")
CAP = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/" \
      "drax/captures/2026-09-28-knight3d-Mb"
CROP = (96, 120, 416, 440)
BG = (238, 236, 232)
ROWS = [("GROK", os.path.join(CB, "sprites_knight", "%s", "E", "%s_E_%02d.png")),
        ("CUT-OUT", os.path.join(OUT, "rig", "%s", "rig_%s_E_%02d.png")),
        ("3D BODY", os.path.join(OUT, "sprites", "%s", "E", "%s_E_%02d.png"))]


def load(path, zoom=2, crop=CROP):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, BG + (255,))
    bg.alpha_composite(im)
    c = bg.convert("RGB").crop(crop)
    return c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)


def panels(gait, i, zoom=2, crop=CROP, label=True):
    tiles = []
    for name, pat in ROWS:
        n = len(os.listdir(os.path.join(CB, "sprites_knight", gait, "E"))) // 2
        src = pat % (gait, gait, i % n) if "rig" not in pat else pat % (gait, gait, i)
        if not os.path.exists(src):
            src = pat % (gait, gait, i)
        tiles.append((name, load(src, zoom, crop)))
    w = tiles[0][1].width; h = tiles[0][1].height
    im = Image.new("RGB", (w * 3, h + 24), (250, 249, 247))
    dr = ImageDraw.Draw(im)
    for k, (name, t) in enumerate(tiles):
        im.paste(t, (k * w, 24))
        if label:
            dr.text((k * w + 8, 7), name, fill=(30, 30, 30))
    return im


def write_seq(gait, nframes, reps, outdir, tag, zoom=2, crop=CROP):
    os.makedirs(outdir, exist_ok=True)
    k = 0
    for _ in range(reps):
        for i in range(nframes):
            panels(gait, i, zoom, crop).save(os.path.join(outdir, "%s_%05d.png" % (tag, k)))
            k += 1
    return k


def main():
    os.makedirs(CAP, exist_ok=True)
    tmp = os.path.join(OUT, "_mp4")
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    made = []
    plan = [("walk", 12, 20.700), ("run", 8, 14.501)]
    seq, k = [], 0
    for gait, n, fps in plan:
        for rep in range(4):                      # real speed
            for i in range(n):
                panels(gait, i).save(os.path.join(tmp, "f_%05d.png" % k)); k += 1
        for rep in range(2):                      # 1/3 speed: hold each frame
            for i in range(n):
                im = panels(gait, i)
                for _ in range(3):
                    im.save(os.path.join(tmp, "f_%05d.png" % k)); k += 1
    out = os.path.join(CAP, "knight3d_Mb2_grok_rig_3d.mp4")
    cmd = ["ffmpeg", "-y", "-framerate", "20.7", "-i", os.path.join(tmp, "f_%05d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf",
           "pad=ceil(iw/2)*2:ceil(ih/2)*2", out]
    r = subprocess.run(cmd, capture_output=True)
    print(("wrote " + out) if r.returncode == 0 else
          ("ffmpeg failed: " + r.stderr.decode()[-400:]))
    if r.returncode == 0:
        made.append(out)

    # --- the leg strip -------------------------------------------------
    LEG = (150, 300, 330, 420)
    for gait, n, _ in plan:
        w = (LEG[2] - LEG[0]) * 3
        h = (LEG[3] - LEG[1]) * 3
        im = Image.new("RGB", (w * n + 150, h * 3 + 30), (250, 249, 247))
        dr = ImageDraw.Draw(im)
        dr.text((8, 8), "C-9 knight3d  %s, E -- LEGS at 3x, every frame" % gait.upper(),
                fill=(20, 20, 20))
        for r_, (name, pat) in enumerate(ROWS):
            y = 26 + r_ * h
            dr.text((8, y + h // 2), name, fill=(40, 40, 40))
            for i in range(n):
                src = pat % (gait, gait, i)
                if os.path.exists(src):
                    im.paste(load(src, 3, LEG), (150 + i * w, y))
        pth = os.path.join(K3, "overlays", "M-b2_%s_E_legs.png" % gait)
        im.save(pth); made.append(pth); print("wrote", pth)
    shutil.rmtree(tmp)
    with open(os.path.join(OUT, "mp4_paths.json"), "w") as f:
        json.dump(dict(files=made, crop=list(CROP), leg_crop=list(LEG)), f, indent=1)


main()
