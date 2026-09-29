#!/usr/bin/env python3
"""C-9 meshy_t2 step 18: the videos Matt looks at.

    python3 scripts/24_mp4.py faces  --clips walk,idle --dirs E,SE,S
    python3 scripts/24_mp4.py body   --set x --clip walk

`faces` is the one that decides this: a 3x zoom on the HEAD, looping, with
per-frame paint, variant X and variant Y side by side on the same frame. The
knight was rejected on a helm and a visor, which is a few dozen pixels; at
1x, on a 132 px creature, nobody can see whether a face is being redrawn each
frame. At 3x, looping, with the three methods adjacent, it is the only thing
you can see.

THE CROP IS FIXED PER (clip, dir), not per frame: the union of the head's
bounding boxes across the whole clip, padded. A box that tracked the head each
frame would hold the head still and hide exactly the wobble the video exists
to show -- the crop would absorb the drift.

`body` is the full-body eight-direction walk of whichever variant wins, at 1x,
so the thing that ships is also on record.
"""
import argparse, json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
WORK = os.path.join(ROOT, "work")
CAP = os.path.join(ROOT, "captures")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
CLIPS = {"idle": 12, "walk": 12, "run": 8, "attack": 12}
BG = (236, 234, 230)


def srgb(x):
    x = np.clip(np.asarray(x, float), 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def head_union_box(clip, d, pad=10):
    rp = json.load(open(os.path.join(OUT, clip, "render_%s.json" % clip)))
    col = srgb(np.array(rp["guides"]["bone_colours"]["head"]))
    lo = [10 ** 9, 10 ** 9]; hi = [-1, -1]
    for i in range(CLIPS[clip]):
        p = os.path.join(OUT, clip, "guides_part", d, "part_%s_%02d.png" % (d, i))
        a = np.asarray(Image.open(p).convert("RGBA")).astype(float)
        hit = (a[..., 3] > 128) & (np.abs(a[..., :3] / 255 - col).max(-1) < 0.02)
        if hit.sum() < 20:
            continue
        ys, xs = np.nonzero(hit)
        lo[0] = min(lo[0], xs.min()); lo[1] = min(lo[1], ys.min())
        hi[0] = max(hi[0], xs.max()); hi[1] = max(hi[1], ys.max())
    return (max(0, lo[0] - pad), max(0, lo[1] - pad),
            min(512, hi[0] + pad + 1), min(512, hi[1] + pad + 1))


_CHOSEN = None


def paint_png(clip, d, i):
    """The Astra-painted frame itself, from whichever paint_* tree the
    conductor chose. Returns None where no paint exists -- which is the whole
    point for S/N/NE/NW/W/SW, where only two frames were ever painted. A blank
    column there is the honest picture, not a bug."""
    global _CHOSEN
    if _CHOSEN is None:
        _CHOSEN = json.load(open(os.path.join(WORK, "chosen.json")))
    src = _CHOSEN.get(clip, {})
    if d in ("E", "SE"):
        v = src.get(d)
    else:
        k = src.get("keys")
        v = (k.get(d) if isinstance(k, dict) else k)
        if i not in (0, CLIPS[clip] // 2):
            return None
    if not v:
        return None
    return os.path.join(ROOT, "paint_%s" % v, clip, d,
                        "%s_%s_%02d.png" % (clip, d, i))


def load(root, clip, d, i, box, zoom):
    if root == "PAINT":
        p = paint_png(clip, d, i)
        if p is None:
            return None
    elif root == "RENDER":
        p = os.path.join(OUT, clip, "colour", d, "%s_%s_%02d.png" % (clip, d, i))
    else:
        p = os.path.join(root, clip, d, "%s_%s_%02d.png" % (clip, d, i))
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    bg = Image.new("RGBA", im.size, BG + (255,))
    bg.alpha_composite(im)
    t = bg.convert("RGB").crop(box)
    return t.resize((t.width * zoom, t.height * zoom), Image.LANCZOS)


def write_mp4(frames, out, fps):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = os.path.join(WORK, "_mp4")
    os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    for k, im in enumerate(frames):
        w, h = im.size
        if w % 2 or h % 2:
            im = im.crop((0, 0, w - (w % 2), h - (h % 2)))
        im.save(os.path.join(tmp, "f_%04d.png" % k))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
                    "-i", os.path.join(tmp, "f_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", out],
                   check=True)
    print("wrote", out, "(%d frames @ %g fps)" % (len(frames), fps))


def faces(args):
    sets = [s.split("=", 1) for s in args.sets]
    for clip in args.clips.split(","):
        n = CLIPS[clip]
        dirs = args.dirs.split(",")
        boxes = {d: head_union_box(clip, d) for d in dirs}
        zoom = args.zoom
        cw = max((boxes[d][2] - boxes[d][0]) for d in dirs) * zoom
        ch = max((boxes[d][3] - boxes[d][1]) for d in dirs) * zoom
        W = 70 + cw * len(sets)
        H = 26 + ch * len(dirs)
        frames = []
        for rep in range(args.loops):
            for i in range(n):
                im = Image.new("RGB", (W, H), (250, 249, 247))
                dr = ImageDraw.Draw(im)
                dr.text((8, 7), "C-9 T2 manticore  %s  head at %dx  frame %02d/%d"
                        % (clip.upper(), zoom, i, n), fill=(20, 20, 20))
                for c, (name, root) in enumerate(sets):
                    dr.text((70 + c * cw + 6, 7), name, fill=(25, 25, 25))
                for r, d in enumerate(dirs):
                    y = 24 + r * ch
                    dr.text((8, y + ch // 2), d, fill=(20, 20, 20))
                    for c, (name, root) in enumerate(sets):
                        t = load(root, clip, d, i, boxes[d], zoom)
                        if t is None:
                            dr.text((70 + c * cw + 10, y + ch // 2),
                                    "no paint for this frame", fill=(150, 150, 150))
                            continue
                        im.paste(t, (70 + c * cw, y))
                frames.append(im)
        write_mp4(frames, os.path.join(CAP, "T2_faces_%s.mp4" % clip), args.fps)


def body(args):
    root = args.root
    clip = args.clip
    n = CLIPS[clip]
    crop = (135, 235, 410, 425)
    zoom = 2
    cw = (crop[2] - crop[0]) * zoom
    ch = (crop[3] - crop[1]) * zoom
    cols, rows = 4, 2
    W = cw * cols
    H = 24 + ch * rows
    frames = []
    for rep in range(args.loops):
        for i in range(n):
            im = Image.new("RGB", (W, H), (250, 249, 247))
            dr = ImageDraw.Draw(im)
            dr.text((8, 6), "C-9 T2 manticore  %s  variant %s  all 8 directions  "
                            "frame %02d/%d" % (clip.upper(), args.label, i, n),
                    fill=(20, 20, 20))
            for k, d in enumerate(DIRS):
                t = load(root, clip, d, i, crop, zoom)
                if t is None:
                    continue
                dd = ImageDraw.Draw(t)
                dd.text((6, 6), d, fill=(40, 40, 40))
                im.paste(t, ((k % cols) * cw, 22 + (k // cols) * ch))
            frames.append(im)
    write_mp4(frames, os.path.join(CAP, "T2_body8_%s_%s.mp4" % (clip, args.label)),
              args.fps)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("faces")
    f.add_argument("--clips", default="walk,idle")
    f.add_argument("--dirs", default="E,SE,S")
    f.add_argument("--sets", nargs="+",
                   default=["render=RENDER", "per-frame paint=PAINT",
                            "X=sprites_x", "Y=sprites_y"])
    f.add_argument("--zoom", type=int, default=3)
    f.add_argument("--loops", type=int, default=4)
    f.add_argument("--fps", type=float, default=10)
    f.set_defaults(fn=faces)
    b = sub.add_parser("body")
    b.add_argument("--root", default="sprites_x")
    b.add_argument("--label", default="X")
    b.add_argument("--clip", default="walk")
    b.add_argument("--loops", type=int, default=4)
    b.add_argument("--fps", type=float, default=12)
    b.set_defaults(fn=body)
    args = ap.parse_args()
    os.makedirs(CAP, exist_ok=True)
    args.fn(args)


if __name__ == "__main__":
    main()
