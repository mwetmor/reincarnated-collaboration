#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): THE COMPOSITED PREVIEW -- the take drawn the way kc2_play draws it.

    python3 tools/bvp_preview.py stills          take/preview/V*.png  (+ Y_* y-sort proofs)
    python3 tools/bvp_preview.py film            take/preview/barrow_v2_pan.mp4 (frames piped to ffmpeg; no frame dump)

The 2D runtime's own draw model, reproduced: the ground tiles at the bottom, then every cutout strip and
every actor sorted by the screen y of its ground point (z = 0), ascending; ZOOM-GD (75.668 px/m, the
1920 x 1080 window = 25.37 x 17.88 m) unless stated. The actor is a JOIN-1 hero cell (the dual-wield
barbarian, join1_pack/d2-ww-barb-mx), rendered at 151.34 px/m with its ground origin at (384, 448),
scaled to the same px/m as the plate: it is at TRUE scale.
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BV2 = os.path.dirname(HERE)
TAKE = os.environ.get("BVP_TAKE", os.path.join(BV2, "take"))
FR = json.load(open(os.path.join(BV2, "paint", "frame_bvp.json")))
L = json.load(open(os.path.join(BV2, "layout_v2.json")))
P = FR["px_per_m"]; X0, Y0 = FR["origin_px"]; W, H = FR["size_px"]
A = math.radians(FR["pitch_deg"]); S, C = math.sin(A), math.cos(A)
PPM_GD = float(L["camera"]["ppm_zoom_gd"])
HERO = os.path.join(os.path.dirname(BV2), "join1_pack", "d2-ww-barb-mx")
HM = json.load(open(os.path.join(HERO, "matrix_index.json")))
H_PPM = float(HM["camera"]["ppm_render"]); H_ANCH = HM["camera"]["anchor_px"]
Image.MAX_IMAGE_PIXELS = None


def px(x, y, z=0.0):
    return X0 + P * x, Y0 + P * S * y - P * C * z


class Plate:
    def __init__(self):
        man = json.load(open(os.path.join(TAKE, "ground", "tiles.json")))
        self.ground = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for t in man["tiles"]:
            self.ground.paste(Image.open(os.path.join(TAKE, "ground", t["file"])), tuple(t["plate_px"][:2]))
        cm = json.load(open(os.path.join(TAKE, "cutouts", "cutouts.json")))
        self.cuts = []
        for c in cm["cutouts"]:
            im = Image.open(os.path.join(TAKE, c["file"])).convert("RGBA")
            self.cuts.append((c["sort_point_plate_px"][1], c["plate_px_topleft"], im, c))

    def cell(self, state, d, i):
        p = os.path.join(HERO, "cells", state, d, f"{state}_{d}_{i:02d}.png")
        im = Image.open(p).convert("RGBA")
        k = P / H_PPM
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        return im, (H_ANCH[0] * k, H_ANCH[1] * k)

    def view(self, cx_m, cy_m, actors, ppm=PPM_GD, size=(1920, 1080), boxes=False):
        """actors: [(x, y, state, dir, frame)]. Returns the frame at `ppm` centred on ground (cx, cy)."""
        k = ppm / P
        ww, hh = size[0] / k, size[1] / k
        CX, CY = px(cx_m, cy_m)
        x0, y0 = int(math.floor(CX - ww / 2)), int(math.floor(CY - hh / 2))
        bw, bh = int(math.ceil(ww)) + 2, int(math.ceil(hh)) + 2
        canvas = Image.new("RGBA", (bw, bh), (24, 30, 38, 255))
        canvas.alpha_composite(self.ground.crop((x0, y0, x0 + bw, y0 + bh)))
        draws = []
        for sy, tl, im, c in self.cuts:
            if tl[0] > x0 + bw or tl[0] + im.width < x0 or tl[1] > y0 + bh or tl[1] + im.height < y0:
                continue
            draws.append((sy, 0, im, (tl[0] - x0, tl[1] - y0)))
        for (ax, ay, st, d, fi) in actors:
            im, anch = self.cell(st, d, fi)
            AX, AY = px(ax, ay)
            draws.append((AY, 1, im, (int(round(AX - anch[0] - x0)), int(round(AY - anch[1] - y0)))))
        draws.sort(key=lambda t: (t[0], t[1]))
        for _, _, im, (ox, oy) in draws:
            canvas.alpha_composite(im, (int(ox), int(oy)))
        out = canvas.crop((0, 0, int(round(ww)), int(round(hh)))).resize(size, Image.LANCZOS).convert("RGB")
        if boxes:
            dr = ImageDraw.Draw(out)
            for _, kind, im, (ox, oy) in draws:
                if kind == 0:
                    dr.rectangle([ox * k, oy * k, (ox + im.width) * k, (oy + im.height) * k], outline=(255, 0, 255))
        return out


def label(im, text):
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
    except Exception:
        f = ImageFont.load_default()
    d.rectangle([0, 0, im.width, 40], fill=(0, 0, 0))
    d.text((12, 6), text, fill=(255, 255, 255), font=f)
    return im


def stills():
    pl = Plate()
    out = os.path.join(TAKE, "preview"); os.makedirs(out, exist_ok=True)
    views = [{"id": "V0_start_plate_scale", "target": [0, 0], "ppm": P}] + L["views"]
    for v in views:
        t = v["target"]
        # the hero stands on the view's target, or on the nearest floor point to it
        ax, ay = nearest_floor(t[0], t[1])
        im = pl.view(t[0], t[1], [(ax, ay, "idle", "S", 0)], ppm=float(v.get("ppm", PPM_GD)))
        label(im, f"{v['id']}  (painted plate + y-sorted cutouts; hero at true scale at ({ax:.1f}, {ay:.1f}))").save(os.path.join(out, v["id"] + ".png"))
        print(v["id"])
    for name, (x, y, d), (cx, cy), what in YSORT:
        im = pl.view(cx, cy, [(x, y, "idle", d, 0)])
        label(im, f"{name}: {what}").save(os.path.join(out, name + ".png"))
        print(name)


def nearest_floor(x, y, inset=1.2):
    F = np.array(L["floor"]["polygon"], float)
    from matplotlib.path import Path
    path = Path(F)
    if path.contains_point((x, y)) and min_dist(F, x, y) > inset:
        return x, y
    c = F.mean(0)
    for t in np.linspace(0, 1, 400):
        qx, qy = x + (c[0] - x) * t, y + (c[1] - y) * t
        if path.contains_point((qx, qy)) and min_dist(F, qx, qy) > inset:
            return qx, qy
    return float(c[0]), float(c[1])


def min_dist(F, x, y):
    a = F; b = np.roll(F, -1, 0); d = b - a
    t = np.clip(((x - a[:, 0]) * d[:, 0] + (y - a[:, 1]) * d[:, 1]) / (d ** 2).sum(1), 0, 1)
    return float(np.min(np.hypot(x - a[:, 0] - t * d[:, 0], y - a[:, 1] - t * d[:, 1])))


# y-sort proofs: (name, (x, y, facing), (camera x, y), caption). Positions are on the floor.
YSORT = [
    ("Y1_behind_hall", (37.6, 13.6, "NW"), (36.0, 12.5), "BEHIND the hall: he is north of its west wall, the hall's roof draws over him"),
    ("Y2_front_barrow_door", (11.6, -38.6, "N"), (11.0, -40.0), "IN FRONT of the barrow door: he is south of it, he draws over it"),
    ("Y3_behind_palisade", (33.2, -14.6, "E"), (34.0, -12.0), "BEHIND the palisade run (north of its strip), its stakes draw over him"),
]


def film():
    pl = Plate()
    route = [tuple(p) for p in L["walk_film"]["route"]]
    st = HM["states"]["run"] if "run" in HM["states"] else HM["states"]["walk"]
    state = "run" if "run" in HM["states"] else "walk"
    nfr = int(st["frames"]); cyc = float(st["clip"]["duration_s"]); stride = float(st.get("stride_m_per_cycle") or 4.0)
    speed = stride / cyc
    fps = 24; size = (1280, 720)
    out = os.path.join(TAKE, "preview", "barrow_v2_pan.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}",
                           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
                           "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    dirs = HM["directions"]["facing_ground_bearing_deg"]
    t = 0.0; n = 0
    for (ax, ay), (bx, by) in zip(route[:-1], route[1:]):
        L_ = math.hypot(bx - ax, by - ay); steps = max(1, int(L_ / speed * fps))
        ang = math.degrees(math.atan2(by - ay, bx - ax)) % 360
        d = min(dirs, key=lambda k: min(abs(dirs[k] - ang), 360 - abs(dirs[k] - ang)))
        for i in range(steps):
            x = ax + (bx - ax) * i / steps; y = ay + (by - ay) * i / steps
            fi = int((t / cyc) * nfr) % nfr
            im = pl.view(x, y, [(x, y, state, d, fi)], size=size)
            ff.stdin.write(im.tobytes()); t += 1 / fps; n += 1
    ff.stdin.close(); ff.wait()
    print(out, n, "frames", round(n / fps, 1), "s")


if __name__ == "__main__":
    {"stills": stills, "film": film}[sys.argv[1]]()
