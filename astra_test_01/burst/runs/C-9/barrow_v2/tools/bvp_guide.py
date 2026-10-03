#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): THE PAINT GUIDE.

    python3 tools/bvp_guide.py ground            -> paint/guide_ground.png  (the greybox's ground texture, re-coloured)
    python3 tools/bvp_guide.py compose CAPDIR    -> paint/barrow_v2_guide.png (+ _preview.jpg)

`ground`: the ground class map (greybox/ground_class_map.png, BX's extent, 4 px/m) becomes a soft
colour field at 8 px/m in sketch A's palette: class edges domain-warped by low-frequency noise (no
straight or circular border survives), blended over BLEND_M, lightly mottled. No anchor rings, no
floor outline: the walkable edge is the land itself (R-C9-144), never a drawn line. The Godot
capture (godot/tools/bvp_capture.gd --mode guide --ground paint/guide_ground.png) wears it.

`compose`: the capture's 2048 tiles are assembled onto the plate grid (paint/frame_bvp.json), then
the guide is SOFTENED (a small blur) so the painter reads masses and placements, not hard greybox
edges (R-C9-149a: guidance light enough for the painter's hand to make shapes organic).
"""
import json, math, os, sys, hashlib
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
BV2 = os.path.dirname(HERE)
PAINT = os.path.join(BV2, "paint")
GCM = json.load(open(os.path.join(BV2, "greybox", "ground_class_map.json")))
L = json.load(open(os.path.join(BV2, "layout_v2.json")))
CARRY_M = 6.0
BLEND_M = 3.0
OUT_PPM = 8.0
SOFT_SIGMA_PX = 1.6

# sketch A's palette (sites/BV3r2-A.png): blue-white snow, rust heather, warm grey rock, sooty ash, lapis ice
PAL = {
    "outside_sea":       (52, 72, 92),
    "outside_shore_ice": (196, 212, 226),
    "outside_land":      (232, 233, 236),
    "grave_ground":      (196, 170, 150),
    "shore_shingle":     (168, 158, 146),
    "cliff_top_rock":    (184, 178, 168),
    "hall_yard_ash":     (128, 116, 106),
    "snow_field":        (238, 239, 242),
    "mere_ice":          (150, 186, 212),
    "stream_ice":        (160, 194, 218),
    "circle":            (222, 218, 210),
    "path":              (212, 205, 194),
}


def noise(shape, scale_px, seed):
    r = np.random.default_rng(seed)
    small = r.standard_normal((shape[0] // scale_px + 3, shape[1] // scale_px + 3))
    z = ndimage.zoom(small, scale_px, order=3)[:shape[0], :shape[1]]
    return z / (z.std() + 1e-9)


def ground():
    """BX's own sculpted ground colour (godot/data/ground_colour.png, render_ground_and_plan.py), cleaned for
    painting: the 8 m disc tints, their rings and dots and the floor outline are taken OUT (alpha-blend
    inverted, line pixels in-painted from their neighbours); then the floor's biomes are carried a few
    metres past the walkable edge onto the land so the edge is not drawn as a colour step either."""
    src = np.asarray(Image.open(os.path.join(BV2, "godot", "data", "ground_colour.png")).convert("RGB"), np.float32)
    Hh, Ww = src.shape[:2]
    e = GCM["extent_sim_m"]; ppm = Ww / (e["x1"] - e["x0"])
    assert abs(ppm - OUT_PPM) < 1e-6, ppm
    yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
    Xm = xx / ppm + e["x0"]; Ym = yy / ppm + e["y0"]
    img = src.copy()
    line = np.zeros((Hh, Ww), bool)
    r8 = L["anchors"]["scatter"]["disc_radius_m_brief"]
    for a in reversed(L["anchors"]["points"]):          # undo in reverse drawing order
        d = np.hypot(Xm - a["x"], Ym - a["y"]) * ppm     # px
        inside = d <= r8 * ppm
        al = 34 / 255.0
        img[inside] = (img[inside] - np.array([235, 180, 60]) * al) / (1 - al)
        line |= np.abs(d - r8 * ppm) <= 3.5
        line |= d <= 6.5
    fl = Image.new("L", (Ww, Hh), 0)
    pts = [((p[0] - e["x0"]) * ppm, (p[1] - e["y0"]) * ppm) for p in L["floor"]["polygon"]]
    ImageDraw.Draw(fl).line(pts + [pts[0]], fill=255, width=7)
    line |= np.asarray(fl) > 0
    # in-paint the line pixels: repeated normalised blur of the known pixels
    known = (~line).astype(np.float32)
    acc = img * known[..., None]; w = known.copy()
    for sig in (2, 4, 8):
        a2 = np.stack([ndimage.gaussian_filter(acc[..., c], sig) for c in range(3)], -1)
        w2 = ndimage.gaussian_filter(w, sig)
        fill = a2 / np.maximum(w2, 1e-6)[..., None]
        m = line & (w2 > 1e-3)
        img[m] = fill[m]
        line &= ~m
    img = np.clip(img, 0, 255)
    # biomes carried past the edge onto the plain land (not onto the beach, ice, water or the mound)
    cm = np.asarray(Image.open(os.path.join(BV2, GCM["png"])))
    up = int(round(OUT_PPM / GCM["px_per_m"]))
    cm = np.kron(cm, np.ones((up, up), np.uint8))[:Hh, :Ww]
    inv = {v: int(k) for k, v in GCM["classes"].items()}
    biome = np.isin(cm, [inv[n] for n in ("grave_ground", "shore_shingle", "cliff_top_rock", "hall_yard_ash", "snow_field")])
    d, (iy, ix) = ndimage.distance_transform_edt(~biome, return_indices=True)
    carry = np.clip(1.0 - d / (CARRY_M * OUT_PPM), 0, 1) ** 1.5
    carry *= (cm == inv["outside_land"])
    wx = noise((Hh, Ww), int(4 * OUT_PPM), 11) * 0.25
    carry = np.clip(carry + wx * (carry > 0), 0, 1)
    # the carried colour is the floor's own colour field, extended smoothly (normalised blur of the floor pixels)
    bw = biome.astype(np.float32); sg = 2.5 * OUT_PPM
    ext = np.stack([ndimage.gaussian_filter(img[..., c] * bw, sg) for c in range(3)], -1) / np.maximum(ndimage.gaussian_filter(bw, sg), 1e-4)[..., None]
    mott = (noise((Hh, Ww), int(1.0 * OUT_PPM), 12) * 4)[..., None]
    img = img * (1 - carry[..., None]) + np.clip(ext + mott, 0, 255) * carry[..., None]
    out = os.path.join(PAINT, "guide_ground.png")
    Image.fromarray(img.round().astype(np.uint8)).save(out)
    print(out, (Ww, Hh), "ppm", OUT_PPM)


def compose(capdir):
    fr = json.load(open(os.path.join(PAINT, "frame_bvp.json")))
    W, H = fr["size_px"]
    info = json.load(open(os.path.join(capdir, "guide_tiles.json")))
    T = info["tile"]
    plate = Image.new("RGB", (W, H))
    for t in info["tiles"]:
        im = Image.open(os.path.join(capdir, t["file"])).convert("RGB")
        assert im.size == (T, T), im.size
        plate.paste(im, tuple(t["px"]))
    if SOFT_SIGMA_PX > 0:
        plate = plate.filter(ImageFilter.GaussianBlur(SOFT_SIGMA_PX))
    # the 0.5 m heightfield leaves (a) a row of white teeth where the snow banks rise off the flat floor and
    # (b) vertical sawtooth stripes down the south cliff face (BX's known limit). A painter would draw (a) as a
    # fence. Both bands get a stronger blur so they read as a soft bank and a rough face.
    P = fr["px_per_m"]; X0, Y0 = fr["origin_px"]; a = math.radians(fr["pitch_deg"]); S_, C_ = math.sin(a), math.cos(a)
    band = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(band)
    fl = [(X0 + P * q[0], Y0 + P * S_ * q[1]) for q in L["floor"]["polygon"]]
    dr.line(fl + [fl[0]], fill=255, width=int(1.4 * P))
    lip = L["land"]["cliff_lip"]
    for q0, q1 in zip(lip[:-1], lip[1:]):
        quad = [(X0 + P * q0[0], Y0 + P * S_ * q0[1]), (X0 + P * q1[0], Y0 + P * S_ * q1[1]),
                (X0 + P * q1[0], Y0 + P * S_ * q1[1] + P * C_ * 4.8), (X0 + P * q0[0], Y0 + P * S_ * q0[1] + P * C_ * 4.8)]
        dr.polygon(quad, fill=255)
    # keep the stair, its landings and the cave mouth crisp: they are openings the paint must keep exactly
    keep = []
    st = L["stair"]
    for poly, zs in ((st["flight"]["polygon"], (0.0, -4.5)), (st["bottom_landing"]["polygon"], (-4.0, -4.6)),
                     (st["top_landing"]["polygon"], (0.0, -4.5)),
                     (next(f for f in L["features"] if f["kind"] == "cave")["footprint"], (-1.2, -4.5))):
        pts = [(X0 + P * q[0], Y0 + P * S_ * q[1] - P * C_ * z) for q in poly for z in zs]
        xs = [t[0] for t in pts]; ys = [t[1] for t in pts]
        dr.rectangle([min(xs) - 0.8 * P, min(ys) - 0.8 * P, max(xs) + 0.8 * P, max(ys) + 0.8 * P], fill=0)
    band = band.filter(ImageFilter.GaussianBlur(12))
    strong = plate.filter(ImageFilter.GaussianBlur(6))
    plate = Image.composite(strong, plate, band)
    out = os.path.join(PAINT, "barrow_v2_guide.png")
    plate.save(out, optimize=True)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    pv = plate.copy(); pv.thumbnail((2400, 2400)); pv.save(os.path.join(PAINT, "barrow_v2_guide_preview.jpg"), quality=85)
    print(out, plate.size, "sha256", sha)


if __name__ == "__main__":
    {"ground": lambda: ground(), "compose": lambda: compose(sys.argv[2])}[sys.argv[1]]()
