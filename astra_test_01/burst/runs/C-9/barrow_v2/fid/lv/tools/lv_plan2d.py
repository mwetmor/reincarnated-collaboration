#!/usr/bin/env python3
"""BV2F LV Phase 1'': a quick 2D PLAN of the art level (heightfield shaded, class colours, every slab outline, every placed
model's footprint, the bounds) -- a check drawing, straight down, north up.  -> fid/lv/M1pp/plan2d.png"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); LV = os.path.dirname(HERE)
BF = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", "art"))
L = json.load(open(os.path.join(BF, "level.json"))); sim = L["sim"]
hf = sim["heightfield"]; H, W = hf["shape"]; ex = hf["extent_sim_m"]; ppm = int(os.environ.get("PLAN_PPM", "8"))
Z = np.fromfile(os.path.join(BF, "terrain_h.f32"), "<f4").reshape(H, W)
C = np.asarray(Image.open(os.path.join(BF, "classes.png")))
tint = L["tints_srgb"]; names = L["classes"]
pal = np.zeros((256, 3), np.uint8)
for i, n in enumerate(names):
    t = tint.get(n, "#808080"); t = t if isinstance(t, str) else "#%02x%02x%02x" % tuple(int(255 * c) for c in t[:3])
    pal[i] = [int(t[1:3], 16), int(t[3:5], 16), int(t[5:7], 16)]
pal[0] = [40, 60, 90]
img = pal[C].astype(float)
zz = np.asarray(Image.fromarray(Z).resize((C.shape[1], C.shape[0])))
gy, gx = np.gradient(zz)
shade = np.clip(1.0 - 0.9 * (gx - gy), 0.45, 1.25)
img = np.clip(img * shade[..., None], 0, 255).astype(np.uint8)
im = Image.fromarray(img).resize((int((ex["x1"] - ex["x0"]) * ppm), int((ex["y1"] - ex["y0"]) * ppm)))
d = ImageDraw.Draw(im)
P = lambda x, y: ((x - ex["x0"]) * ppm, (y - ex["y0"]) * ppm)          # sim (x, y) = (u, -v)
col = {"shore_ice": (235, 245, 255), "ice": (200, 225, 245), "rock": (150, 140, 130), "snow": (255, 255, 255)}
for gid, g in sim.get("slabs", {}).items():
    for it in g["items"]:
        d.polygon([P(*q) for q in it["poly"]], fill=col.get(g["class"], (255, 0, 255)), outline=(30, 30, 30))
import math
for m in sim["models"]:
    for ins in (m.get("instances") or [m]):
        if ins.get("type") == "box" or "size_m" in ins and isinstance(ins.get("size_m"), list):
            w, dd = ins["size_m"][0], ins["size_m"][1]; a = math.radians(ins["godot_rot_y_deg"])
            fz = (math.sin(a), math.cos(a)); fx = (math.cos(a), -math.sin(a)); c = ins["pos"]
            pts = [P(c[0] + fx[0] * w / 2 * sx + fz[0] * dd / 2 * sz, c[1] + fx[1] * w / 2 * sx + fz[1] * dd / 2 * sz) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            d.polygon(pts, outline=(200, 0, 0)); d.line([P(*c), P(c[0] + fz[0] * dd / 2, c[1] + fz[1] * dd / 2)], fill=(200, 0, 0), width=2)
b = L["bounds"]["polygon_uv"]; d.line([P(q[0], -q[1]) for q in b + b[:1]], fill=(255, 0, 255), width=2)
for w in L["bounds"].get("inner_walls_uv", []):
    d.line([P(q[0], -q[1]) for q in w], fill=(255, 140, 0), width=3)
env = L["frame"]["envelope"]; d.rectangle([P(env["u"][0], -env["v"][1]), P(env["u"][1], -env["v"][0])], outline=(0, 0, 0), width=2)
os.makedirs(os.path.join(LV, "M1pp"), exist_ok=True)
crop = sys.argv[1:5]
if crop:
    u0, v0, u1, v1 = map(float, crop); im = im.crop((*P(u0, -v1), *P(u1, -v0)))
im.save(os.path.join(LV, "M1pp", "plan2d.png")); print(im.size)
