#!/usr/bin/env python3
"""barrow_v2 (lane BX): PROJECTION-LAW PREVIEWS of the six camera windows, drawn in Python.

NOT the Godot render. The Godot greybox (godot/) could not be run: the host was under the 20 GiB
disk gate (heavy part HALTED). These previews apply the arena's own projection law to the same
layout so the windows can be looked at now:

    screen_x = ppm * (x - tx) + W/2
    screen_y = ppm * sin(a) * (y - ty) - ppm * cos(a) * z + H/2        (zero yaw, a = 52.9535411256029 deg)

ppm = ppm_GD (75.668 px/m) at 1920 x 1080, i.e. the 25.4 x 17.9 m ZOOM-GD window. Ground from the
zone texture (godot/data/ground_colour.png); primitives as painter-sorted flat-shaded faces.

    python3 tools/preview_views.py      -> greybox/preview_V*.png
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bv2_geom as G  # noqa: E402

ROOT = os.path.dirname(HERE)
L = json.load(open(os.path.join(ROOT, "layout_v2.json")))
EXT = {"x0": -62.0, "x1": 66.0, "y0": -74.0, "y1": 62.0}
A = math.radians(L["camera"]["pitch_deg"])
SA, CA = math.sin(A), math.cos(A)
W, H = 1920, 1080
FWD = (0.0, -CA, -SA)                      # camera forward in (x, y_sim, z)
SUN = np.array([0.45, 0.55, 0.70])         # toward the light (x, y_sim(south), z)
SUN = SUN / np.linalg.norm(SUN)
KIND_RGB = {"mound": (0.66, 0.64, 0.55), "door": (0.25, 0.18, 0.12), "standing_stone": (0.47, 0.47, 0.46),
            "wreck": (0.45, 0.31, 0.19), "mast": (0.33, 0.22, 0.14), "rock": (0.50, 0.50, 0.49),
            "hall": (0.33, 0.26, 0.20), "gable": (0.38, 0.27, 0.19), "palisade": (0.40, 0.31, 0.22),
            "cliff": (0.58, 0.55, 0.50), "cave": (0.05, 0.05, 0.06), "fallen_stone": (0.62, 0.61, 0.57),
            "grave_marker": (0.45, 0.41, 0.38), "driftwood": (0.56, 0.45, 0.32), "beam": (0.18, 0.15, 0.13),
            "step": (0.76, 0.71, 0.60), "landing": (0.74, 0.69, 0.58)}


def faces_prism(poly, z0, z1, rgb):
    out = [([(p[0], p[1], z1) for p in poly], (0, 0, 1), rgb)]
    ccw = G.signed_area(poly) > 0
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]
        Ln = math.hypot(ex, ey) or 1.0
        nx, ny = (ey / Ln, -ex / Ln) if ccw else (-ey / Ln, ex / Ln)
        out.append(([(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)], (nx, ny, 0.0), rgb))
    return out


def faces_dome(s, rgb):
    cx, cy = s["centre"]
    a, b = s["semi_axes_m"]
    rot = s["rot_deg"]
    rise = s["rise_m"]
    out = []
    K = 10
    for k in range(K):
        t0, t1 = k / K, (k + 1) / K
        z0, z1 = rise * math.sin(t0 * math.pi / 2), rise * math.sin(t1 * math.pi / 2)
        r1 = math.cos(t1 * math.pi / 2)
        ring = G.ellipse_poly(cx, cy, a * max(r1, 0.02), b * max(r1, 0.02), rot, 64)
        shade = 0.82 + 0.18 * t1
        out.append(([(p[0], p[1], z1) for p in ring], (0, 0, 1), tuple(c * shade for c in rgb)))
        r0 = math.cos(t0 * math.pi / 2)
        ring0 = G.ellipse_poly(cx, cy, a * r0, b * r0, rot, 64)
        out.append(([(p[0], p[1], z0) for p in ring0], (0, 0, 1), tuple(c * (0.78 + 0.18 * t0) for c in rgb)))
    return out


def scene_faces():
    F = []
    lip = L["land"]["cliff_lip"]
    foot = L["land"]["z_cliff_foot_m"]
    for i in range(len(lip) - 1):
        a, b = lip[i], lip[i + 1]
        ex, ey = b[0] - a[0], b[1] - a[1]
        Ln = math.hypot(ex, ey) or 1.0
        F.append(([(a[0], a[1], foot), (b[0], b[1], foot), (b[0], b[1], 0.0), (a[0], a[1], 0.0)],
                  (-ey / Ln, ex / Ln, 0.0), KIND_RGB["cliff"]))
    for f in L["features"]:
        if f["kind"] == "mound":
            F += faces_dome(f["shape"], KIND_RGB["mound"])
        else:
            F += faces_prism(f["footprint"], f["z_bottom_m"], f["z_top_m"], KIND_RGB.get(f["kind"], (0.5, 0.5, 0.5)))
    S = L["stair"]
    F += faces_prism(S["top_landing"]["polygon"], foot - 0.3, 0.0, KIND_RGB["landing"])
    F += faces_prism(S["bottom_landing"]["polygon"], foot - 0.3, S["bottom_landing"]["z_m"], KIND_RGB["landing"])
    fl = S["flight"]["polygon"]
    n, rise, tread = S["flight"]["n_steps"], S["flight"]["step_rise_m"], S["flight"]["step_tread_m"]
    for k in range(n):
        t0, t1 = k / n, (k + 1) / n

        def at(p, q, t):
            return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
        q = [at(fl[0], fl[3], t0), at(fl[1], fl[2], t0), at(fl[1], fl[2], t1), at(fl[0], fl[3], t1)]
        rgb = KIND_RGB["step"] if k % 2 == 0 else tuple(c * 0.93 for c in KIND_RGB["step"])
        F += faces_prism(q, foot - 0.3, -(k + 1) * rise, rgb)
    return F


def render(view, ground_img, faces, font, font_s, W=1920, H=1080, walker=None, caption=True):
    tx, ty = view["target"]
    ppm = view["ppm"] * W / 1920.0
    # ground: inverse-map every pixel onto z = 0 (land/ice/floor) from the zone texture; sea where the
    # texture says sea, drawn at its own height by the cliff faces covering the gap
    gx = tx + (np.arange(W) + 0.5 - W / 2) / ppm
    gy = ty + (np.arange(H) + 0.5 - H / 2) / (ppm * SA)
    X, Y = np.meshgrid(gx, gy)
    gw, gh = ground_img.shape[1], ground_img.shape[0]
    u = np.clip(((X - EXT["x0"]) / (EXT["x1"] - EXT["x0"]) * gw).astype(int), 0, gw - 1)
    v = np.clip(((Y - EXT["y0"]) / (EXT["y1"] - EXT["y0"]) * gh).astype(int), 0, gh - 1)
    img = Image.fromarray(ground_img[v, u])
    dr = ImageDraw.Draw(img, "RGBA")

    def scr(p):
        return (ppm * (p[0] - tx) + W / 2, ppm * SA * (p[1] - ty) - ppm * CA * p[2] + H / 2)
    vis = []
    for pts, nrm, rgb in faces:
        if nrm[0] * FWD[0] + nrm[1] * FWD[1] + nrm[2] * FWD[2] >= 0 and nrm[2] == 0:
            continue
        sp = [scr(p) for p in pts]
        xs = [p[0] for p in sp]
        ys = [p[1] for p in sp]
        if max(xs) < 0 or min(xs) > W or max(ys) < 0 or min(ys) > H:
            continue
        depth = sum(-p[1] * CA - p[2] * SA for p in pts) / len(pts)
        lam = 0.55 + 0.45 * max(0.0, nrm[0] * SUN[0] + nrm[1] * SUN[1] + nrm[2] * SUN[2])
        col = tuple(int(255 * min(1.0, c * lam)) for c in rgb)
        vis.append((depth, sp, col))
    vis.sort(key=lambda t: -t[0])
    for _, sp, col in vis:
        dr.polygon(sp, fill=col + (255,), outline=(0, 0, 0, 40))
    # the walker for scale: a 1.9 m capsule just south of the target
    wx, wy = walker if walker is not None else (tx, ty + 1.5)
    b = scr((wx, wy, 0.0))
    t = scr((wx, wy, 1.9))
    r = 0.32 * ppm
    dr.ellipse([b[0] - r, b[1] - r * SA, b[0] + r, b[1] + r * SA], fill=(0, 0, 0, 60))
    dr.rounded_rectangle([b[0] - r, t[1], b[0] + r, b[1]], radius=int(r), fill=(150, 148, 144, 255), outline=(60, 60, 60, 255))
    for a in L["anchors"]["points"]:
        p = scr((a["x"], a["y"], 0.0))
        if -50 < p[0] < W + 50 and -50 < p[1] < H + 50:
            dr.ellipse([p[0] - 6, p[1] - 5, p[0] + 6, p[1] + 5], fill=(140, 75, 10, 230))
            dr.text((p[0] + 10, p[1] - 12), f"{a['id']}  {a['delivered_by'].split(' (')[0]}", font=font, fill=(60, 30, 0, 255),
                    stroke_width=3, stroke_fill=(255, 255, 255, 220))
    o = scr((0, 0, 0))
    dr.line([o[0] - 12, o[1], o[0] + 12, o[1]], fill=(0, 0, 0, 255), width=3)
    dr.line([o[0], o[1] - 10, o[0], o[1] + 10], fill=(0, 0, 0, 255), width=3)
    if not caption:
        return img
    cap = (f"{view['id']}  -- {view['what']}   |   PROJECTION-LAW PREVIEW (python), not the Godot render   |   "
           f"zero yaw, pitch {L['camera']['pitch_deg']:.4f} deg, ppm {ppm:.3f} (ZOOM-GD), window {view['window_m'][0]:.1f} x {view['window_m'][1]:.1f} m, target ({tx:.1f}, {ty:.1f})")
    dr.rectangle([0, H - 34, W, H], fill=(255, 255, 255, 210))
    dr.text((12, H - 28), cap, font=font_s, fill=(20, 20, 20, 255))
    # 5 m scale bar
    dr.rectangle([W - 40 - 5 * ppm, 24, W - 40, 32], fill=(0, 0, 0, 220))
    dr.text((W - 40 - 5 * ppm, 36), "5 m", font=font_s, fill=(0, 0, 0, 255))
    return img


def film(ground, faces):
    """The walk film, PROJECTION-LAW PREVIEW: frames piped straight into ffmpeg (no frame files)."""
    import subprocess
    wf = L["walk_film"]
    route = wf["route"]
    speed = wf["speed_mps"]
    fps = 24
    Wf, Hf = 960, 540
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 14)
        font_s = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 11)
    except OSError:
        font = font_s = ImageFont.load_default()
    pts = []
    step = speed / fps
    for a, b in zip(route[:-1], route[1:]):
        Ln = math.dist(a, b)
        k = max(1, int(Ln / step))
        for i in range(k):
            t = i / k
            pts.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    pts.append(tuple(route[-1]))
    out = os.path.join(ROOT, "greybox", "barrow_v2_walk_preview.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wf}x{Hf}", "-r", str(fps),
           "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "28", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    view = {"id": "walk", "what": "", "ppm": L["camera"]["ppm_zoom_gd"], "window_m": L["camera"]["window_zoom_gd_1920x1080_m"]}
    for i, p in enumerate(pts):
        view["target"] = [p[0], p[1]]
        img = render(view, ground, faces, font, font_s, W=Wf, H=Hf, walker=p, caption=False)
        d = ImageDraw.Draw(img)
        d.rectangle([0, Hf - 20, Wf, Hf], fill=(255, 255, 255))
        d.text((8, Hf - 16), f"barrow_v2 greybox walk -- PROJECTION-LAW PREVIEW (python), not the Godot render -- ZOOM-GD 25 x 18 m, zero yaw, pitch 52.95 -- ({p[0]:.1f}, {p[1]:.1f}) m",
               font=font_s, fill=(20, 20, 20))
        pr.stdin.write(img.convert("RGB").tobytes())
    pr.stdin.close()
    rc = pr.wait()
    print("film", os.path.relpath(out, ROOT), "frames", len(pts), "seconds", round(len(pts) / fps, 1), "rc", rc)


def main():
    if "--film" in sys.argv:
        ground = np.asarray(Image.open(os.path.join(ROOT, "godot", "data", "ground_colour.png")).convert("RGB"))
        film(ground, scene_faces())
        return
    ground = np.asarray(Image.open(os.path.join(ROOT, "godot", "data", "ground_colour.png")).convert("RGB"))
    faces = scene_faces()
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
        font_s = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 19)
    except OSError:
        font = font_s = ImageFont.load_default()
    for v in L["views"]:
        img = render(v, ground, faces, font, font_s)
        p = os.path.join(ROOT, "greybox", f"preview_{v['id']}.png")
        img.save(p, optimize=True)
        print("wrote", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
