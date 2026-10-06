#!/usr/bin/env python3
"""barrow_v2 SW section AS A LEVEL OF THE V1 BARROW (R-C9-159, lane BS, drax): the level's data, for
barrow_full/godot/scripts/barrow_v2_sw.gd.

    python3 tools/v2sw_prep.py   -> barrow_full/godot/data/barrow_v2_sw/{level.json, terrain.f32, ground.png,
                                    heather.json, snow_grid.bin}

THE CAMERA IS V1'S: orthographic, pitch 52.95354, YAW 47 (R-C9-159). The sim frame is unchanged
(+x east, +y south; Godot X = x, Z = y, Y = up) -- only the camera turns. The ground basis is v1's:
    u = x cos47 - y sin47       v = -x sin47 - y cos47     (screen right; ground "up-screen")
    screen_up = v sin(pitch) + h cos(pitch)
THE PAINT FRAME is the screen rectangle covering every still window and the film camera's path, painted at
HALF plate density (R-C9-159: far fewer, larger tiles; the ground is wash, the plants are 3D, the pen is post).
"""
import json, math, pathlib, shutil, hashlib
import numpy as np
from matplotlib.path import Path
from scipy.ndimage import distance_transform_edt, gaussian_filter

ROOT = pathlib.Path(__file__).resolve().parents[1]
C9 = ROOT.parent
BF = C9 / "barrow_full/godot"
OUT = BF / "data/barrow_v2_sw"
OUT.mkdir(parents=True, exist_ok=True)
L = json.load(open(ROOT / "layout_v2.json"))
SEC = json.load(open(ROOT / "godot/data/section_sw/section.json"))
PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
SA, CA = math.sin(PITCH), math.cos(PITCH)
YAW = math.radians(47.0)
UH = np.array([math.cos(YAW), -math.sin(YAW)])      # (x, z)
VH = np.array([-math.sin(YAW), -math.cos(YAW)])
PAINT_PPM = PPM / 2.0
LIFT = 55.0 / PPM                                     # barrow_full CAM_LIFT_PX


def uv(p):
    p = np.asarray(p, float)
    return np.array([p @ UH, p @ VH])


# ---------------------------------------------------------------- the stills and the film, at v1's camera
FRAME_W, FRAME_H = 1920 / PPM, 1080 / PPM            # 19.08 x 13.45 m of screen (v1's plate view)
STILLS = {"S1_wreck": [-44.0, 12.5], "S2_coast": [-27.0, 31.0], "S3_cave_stair": [3.5, 41.0]}
ROUTE = SEC["film_route"]
need = []                                            # screen rects (u0, u1, s0, s1)
for t in STILLS.values():
    c = uv(t)
    need.append((c[0] - FRAME_W / 2, c[0] + FRAME_W / 2, c[1] * SA - FRAME_H / 2, c[1] * SA + FRAME_H / 2))
for i in range(len(ROUTE) - 1):
    a, b = np.array(ROUTE[i]), np.array(ROUTE[i + 1])
    for f in np.linspace(0, 1, 10):
        c = uv(a + (b - a) * f)
        s = c[1] * SA + LIFT * SA
        need.append((c[0] - FRAME_W / 2, c[0] + FRAME_W / 2, s - FRAME_H / 2, s + FRAME_H / 2))
need = np.array(need)
M = 1.5
fu0, fu1 = need[:, 0].min() - M, need[:, 1].max() + M
fs0, fs1 = need[:, 2].min() - M, need[:, 3].max() + M
# whole tiles: 1536 x 1024 at a 1280 x 768 stride, at PAINT_PPM
TW, TH, SX, SY = 1536, 1024, 1280, 768
cols = max(1, math.ceil(((fu1 - fu0) * PAINT_PPM - TW) / SX) + 1)
rows = max(1, math.ceil(((fs1 - fs0) * PAINT_PPM - TH) / SY) + 1)
GW, GH = TW + (cols - 1) * SX, TH + (rows - 1) * SY
cu, cs = (fu0 + fu1) / 2, (fs0 + fs1) / 2
u0 = cu - GW / PAINT_PPM / 2
s_top = cs + GH / PAINT_PPM / 2
frame = {"u0": u0, "v1": s_top / SA, "ppm": PAINT_PPM, "size_px": [GW, GH], "cols": cols, "rows": rows,
         "_law": "PaintedWorld.guide_uv with g_frame = (u0, v1, ppm), g_px_per = (ppm sin, ppm cos), g_size = size_px",
         "stills": STILLS}

# ---------------------------------------------------------------- the knight, the floor's fence
floor = np.array(L["floor"]["polygon"], float)
spawn = np.array(ROUTE[0])
lvl = {
    "_what": "barrow_v2 SW section as a level of the v1 Barrow (R-C9-159); read by scripts/barrow_v2_sw.gd",
    "tints_srgb": {},
    "knight": {"spawn_uv": [float(v) for v in uv(spawn)], "spawn_facing": "S", "gear_stack": 4},
    "frame": {"guide_window": {"u": [fu0, fu1], "v": [fs0 / SA, fs1 / SA]}, "paint": frame},
    "camera_clamp_default": False,
    "placements": [],
    "floor_polygon_xz": floor.tolist(),
    "stair_landing_xz": L["stair"]["top_landing"]["polygon"],
    "lanes": {l["id"]: l["polygon"] for l in L["lanes"]},
    "film_route_xz": ROUTE,
    "box": SEC["box"],
    "lagoon": {"z": -1.30, "spit_a": [-41.5, 26.8], "spit_dir": [-0.94, 0.34]},
    "sea_z": float(L["sea"]["z_m"]),
}

# ---------------------------------------------------------------- heather (3D sprays, never painted)
# the section's heather + dry-grass points (off the floor and the lanes, proved by section_sw_build.py), as
# v1's rows: [x, z, height_m, class (0 heather, 1 grass: paler and taller), mul r, g, b]
hrows = []
rng = np.random.default_rng(159)
# v1's density and colour: v1 set 977 sprays over its whole 50 x 40 m window at height 0.30 (shrubs 0.35) with the
# painting's multiplier (median ~1, p10 ~0.63); the section's points crowd a narrow coast strip, so one in three is
# kept (clumped, not a carpet), at v1's height, with v1's p10..p50 multiplier range
# none inside the new wreck (barrow_v2_sw.gd WRECK2: 17 x 6.42 m at (-48.1, 13.3), godot yaw 102), 0.6 m clear
_a = math.radians(102.0)
_ux, _uz = np.array([math.cos(_a), -math.sin(_a)]), np.array([math.sin(_a), math.cos(_a)])
def in_wreck(x, y):
    v = np.array([x, y]) - np.array([-48.1, 13.3])
    return abs(v @ _ux) < 8.5 + 0.6 and abs(v @ _uz) < 3.21 + 0.6
for i, h in enumerate(SEC["heather"]):
    if i % 3 or in_wreck(h[0], h[1]):
        continue
    t = float(h[4])
    hrows.append([h[0], h[1], 0.26, 0, round(0.50 + 0.22 * t, 3), round(0.46 + 0.20 * t, 3), round(0.44 + 0.18 * t, 3)])
for i, g in enumerate(SEC["grass"]):
    if i % 2 or in_wreck(g[0], g[1]):
        continue
    hrows.append([g[0], g[1], 0.32, 1, 0.80, 0.78, 0.62])
json.dump({"_what": "barrow_v2 SW heather sprays (BarrowHeather), placed off the floor and the lanes",
           "columns": ["x", "z", "height_m", "class", "mul_r", "mul_g", "mul_b"], "rows": hrows},
          open(OUT / "heather.json", "w"))

# ---------------------------------------------------------------- the snow field's depth grid (v1's SnowField)
# snow lies on the walkable floor (and the flush stair landing), feathered 1 m in from the edge; none on the
# mere's ice and the stream's ice; the floor's west shingle zone thinner (the painted shingle shows through)
ox, oz, size, cell = -46.0, -6.0, 68.0, 0.1
n = int(size / cell)
gx = ox + (np.arange(n) + 0.5) * cell
gz = oz + (np.arange(n) + 0.5) * cell
GX, GZ = np.meshgrid(gx, gz)
P = np.stack([GX.ravel(), GZ.ravel()], 1)
ins = Path(floor).contains_points(P).reshape(n, n) | Path(np.array(L["stair"]["top_landing"]["polygon"])).contains_points(P).reshape(n, n)
d_in = distance_transform_edt(ins) * cell
mul = np.clip(d_in / 1.0, 0, 1)
mere = Path(np.array(L["mere"]["polygon"], float)).contains_points(P).reshape(n, n)
mul[mere] = 0.0
st = np.array(SEC["stream"]["polyline"], float)
from scipy.spatial import cKDTree
sd = cKDTree(np.vstack([np.linspace(st[i], st[i + 1], 40) for i in range(len(st) - 1)])).query(P)[0].reshape(n, n)
mul[sd < 0.8] = 0.0
shs = np.array(L["zones"]["classes"]["shore_shingle"]["seeds"], float)
dsh = np.min(np.linalg.norm(P[:, None, :] - shs[None], axis=2), 1).reshape(n, n)
mul *= 1.0 - 0.45 * np.exp(-dsh / 12.0)
mul = gaussian_filter(mul, 1.0) * ins
pth = np.array(L["path"]["polyline"], float)
pd = cKDTree(np.vstack([np.linspace(pth[i], pth[i + 1], 80) for i in range(len(pth) - 1)])).query(P)[0].reshape(n, n)
trod = np.clip(1 - pd / 0.9, 0, 1) * 0.6 * ins
buf = np.concatenate([mul.astype("<f4").ravel(), trod.astype("<f4").ravel()])
buf.tofile(OUT / "snow_grid.bin")
snow = {"area_xz": [ox, oz, size, size], "field_px": 1024, "trail_px": 1024,
        "grid": {"file": "snow_grid.bin", "sha256": hashlib.sha256(buf.tobytes()).hexdigest(), "origin_xz": [ox, oz],
                 "cell_m": cell, "nx": n, "nz": n}}
lvl["snow"] = snow

# ---------------------------------------------------------------- the section's own data (built by section_sw_build.py)
for f in ("terrain.f32", "ground.png"):
    shutil.copyfile(ROOT / "godot/data/section_sw" / f, OUT / f)
shutil.copyfile(ROOT / "godot/data/section_sw/section.json", OUT / "section.json")
json.dump(lvl, open(OUT / "level.json", "w"), indent=1)
print(json.dumps({"frame": {k: frame[k] for k in ("u0", "v1", "size_px", "cols", "rows")}, "tiles": cols * rows,
                  "frame_m": [round(GW / PAINT_PPM, 2), round(GH / PAINT_PPM, 2)], "spawn_uv": lvl["knight"]["spawn_uv"],
                  "heather_rows": len(hrows)}))

# ---------------------------------------------------------------- the water's floe distance field (foam rings)
from PIL import Image, ImageDraw
bx = SEC["box"]
WP = 8.0
ww, wh = int((bx["x1"] - bx["x0"]) * WP), int((bx["y1"] - bx["y0"]) * WP)
mask = Image.new("L", (ww, wh), 0)
dr = ImageDraw.Draw(mask)
for f in SEC["floes"]:
    dr.polygon([((p[0] - bx["x0"]) * WP, (p[1] - bx["y0"]) * WP) for p in f["poly"]], fill=255)
for r in SEC["ridges"]:
    x, y = (r["pos"][0] - bx["x0"]) * WP, (r["pos"][1] - bx["y0"]) * WP
    dr.ellipse((x - 3, y - 3, x + 3, y + 3), fill=255)
# the shore is an edge too: foam where the water meets the land (the terrain above the water level)
Zs = np.fromfile(ROOT / "godot/data/section_sw/terrain.f32", "<f4").reshape(SEC["terrain"]["shape"])
from scipy.ndimage import zoom
land = Image.fromarray(((zoom(Zs, WP / SEC["terrain"]["px_per_m"], order=1)[:wh, :ww] > -1.32) * 255).astype(np.uint8))
m = np.maximum(np.asarray(mask), np.asarray(land.resize((ww, wh))))
dist = distance_transform_edt(m < 128) / WP
Image.fromarray((np.clip(dist / 2.0, 0, 1) * 255).astype(np.uint8)).save(OUT / "water_sdf.png")
print("water_sdf", ww, wh)
