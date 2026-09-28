#!/usr/bin/env python3
"""C-9 meshy_t2: draw the skeleton over the rig shots, and build contact sheets.

    python3 scripts/06b_draw.py <shotdir> <outpng> [pose1,pose2,...] [--view side]

The ortho projection is reconstructed from the camera's inverse world matrix,
which 06_rigshot.py dumped -- so a bone lands on the pixel it actually renders
to, rather than on a hand-derived approximation of the camera.
"""
import json, math, os, sys
from PIL import Image, ImageDraw

BG = (24, 24, 30)
LIMB = {"thigh": (255, 90, 90), "shin": (255, 150, 90), "hcannon": (255, 210, 90),
        "hpaw": (255, 250, 140),
        "shoulder": (90, 190, 255), "upperarm": (110, 230, 255), "forearm": (150, 255, 235),
        "fcannon": (190, 255, 210), "fpaw": (225, 255, 225),
        "spine": (200, 160, 255), "chest": (215, 180, 255), "hips": (255, 120, 220),
        "neck": (160, 255, 160), "head": (120, 255, 120), "root": (140, 140, 140),
        "tail": (255, 180, 120)}


def colour(name):
    base = name.split(".")[0].rstrip("_0123456789")
    return LIMB.get(base, (255, 255, 255))


def project(shot, view, p):
    M = shot["views"][view]["cam_matrix_world_inv"]
    x = M[0][0] * p[0] + M[0][1] * p[1] + M[0][2] * p[2] + M[0][3]
    y = M[1][0] * p[0] + M[1][1] * p[1] + M[1][2] * p[2] + M[1][3]
    R = shot["resolution"]; s = shot["ortho_scale"]
    return (R / 2 + x / s * R, R / 2 - y / s * R)


def load(shotdir, pose, view, tag):
    p = os.path.join(shotdir, "%s_%s_%s.png" % (pose, view, tag))
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    bg = Image.new("RGBA", im.size, BG + (255,))
    bg.alpha_composite(im)
    return bg.convert("RGB")


def draw_bones(im, shot, pose, view, only=None, width=3):
    dr = ImageDraw.Draw(im)
    for name, b in shot["bones"][pose].items():
        if only and not any(name.startswith(o) for o in only):
            continue
        h = project(shot, view, b["head"]); t = project(shot, view, b["tail"])
        c = colour(name)
        dr.line([h, t], fill=c, width=width)
        dr.ellipse([h[0] - 4, h[1] - 4, h[0] + 4, h[1] + 4], outline=(10, 10, 10), fill=c)
    return im


def main():
    shotdir, outpng = sys.argv[1], sys.argv[2]
    shot = json.load(open(os.path.join(shotdir, "shot.json")))
    poses = sys.argv[3].split(",") if len(sys.argv) > 3 and not sys.argv[3].startswith("-") \
        else shot["poses"]
    views = ["side", "front", "q"]
    tile = 430
    W = tile * len(views) + 120
    H = tile * len(poses) + 30
    out = Image.new("RGB", (W, H), (248, 247, 245))
    dr = ImageDraw.Draw(out)
    dr.text((8, 8), os.path.basename(outpng), fill=(20, 20, 20))
    for r, pose in enumerate(poses):
        y = 26 + r * tile
        dr.text((8, y + tile // 2), pose, fill=(20, 20, 20))
        for c, view in enumerate(views):
            im = load(shotdir, pose, view, "mesh")
            if im is None:
                continue
            im = im.copy()
            draw_bones(im, shot, pose, view, width=4)
            out.paste(im.resize((tile, tile), Image.LANCZOS), (120 + c * tile, y))
    out.save(outpng)
    print("wrote", outpng, out.size)


if __name__ == "__main__":
    main()
