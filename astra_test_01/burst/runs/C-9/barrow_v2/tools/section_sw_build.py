#!/usr/bin/env python3
"""barrow_v2 TRUE-3D, SECTION SW proof (R-C9-158, lane BS, drax).

The south-west of the Fjord Headland -- the wreck (p01), the coast round to the sea cave and its stair (p03),
and the floor edge behind -- rebuilt as REAL 3D for the v1 paint route (guide render -> guided paint-over ->
projected back through the fixed camera). This module emits the section's data; godot/scripts/section_sw.gd
builds it.

What it replaces INSIDE the section box (only there; the rest of the site is the BX blockout, unchanged):
  * the STEPPED heightfield -> a 4 px/m terrain: the floor exactly 0; a shingle STORM BEACH west of the floor
    (berm, shingle slope, a rock step, the wet lower shore, the waterline) blending at the headland's corner
    into a CLIFF TOP that stops at a lip and drops away UNDER a chain of real cliff models;
  * the coast's faces -> a chain of cliffplain instances (rotated, scaled and mixed: shallow bites, deep
    spurs), crag sea stacks and cliff-foot boulders, a crag rock step down the beach; the layout's cave cliff
    and stair cliff stay exactly where BX placed them;
  * the sea's ice -> broken FLOES (Voronoi cells, ragged edges, gaps growing seaward, open dark water between),
    near-continuous shore-fast ice at the beach, PRESSURE RIDGES where it meets the shingle;
  * detail -> a frozen STREAM (the mere's outflow: flush ice across the floor, a gully with banks down the
    beach to the shore ice), cairns, standing stones, driftwood, shingle pebbles, rust heather, dry grass.

Rules it proves on its own output (printed, and written to section.json["checks"]): every dressing item lies
OFF the walkable floor (distance >= its radius + 0.25 m) and OUT of every exit lane; the terrain is exactly 0
on the floor. layout_v2.json is NOT modified (its validator stays 66/66).

    python3 tools/section_sw_build.py      -> godot/data/section_sw/{section.json, terrain.f32, ground.png}
Sim frame: +x east, +y SOUTH, z up. Godot: X = x, Y = z, Z = y.
"""
import json, math, hashlib, pathlib
import numpy as np
from scipy.spatial import cKDTree, Voronoi
from scipy.ndimage import gaussian_filter, distance_transform_edt, map_coordinates
from matplotlib.path import Path
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "godot/data/section_sw"
L = json.load(open(ROOT / "layout_v2.json"))
rng = np.random.default_rng(158)

PITCH = math.radians(float(L["camera"]["pitch_deg"]))
SA, CA = math.sin(PITCH), math.cos(PITCH)
PPM = float(L["camera"]["ppm_plate"])
# THE PAINT FRAME (the guide and the painting): screen_x = x, screen_y = sin(a) y - cos(a) z (metres), and
# guide px = ((screen_x - SX0) * PPM, (screen_y - SY0) * PPM); 6 x 6 chunks of 1536 x 1024 at a 1280 x 768 stride
COLS, ROWS = 6, 6
GW, GH = 1536 + (COLS - 1) * 1280, 1024 + (ROWS - 1) * 768
SX0, SY0 = -57.5, -4.0
# THE SECTION BOX (sim metres): new terrain inside, blended over BLEND m into the BX heightfield at its edges
BX0, BX1, BY0, BY1 = -70.0, 26.0, -14.0, 62.0
HPPM = 4.0
BLEND = 3.0
SEA_Z = float(L["sea"]["z_m"])
DEEP = -8.2
# THE TWO WATERS (the section's one liberty, recorded): the floor is flat at 0 and the south cliff stands 7.5 m over
# the sea, but sketch A's wreck lies on a LOW shingle shore in the ice. So the west is a shallow LAGOON: fast ice
# grounded over a tidal flat at LAG_Z, held off the sea by a rock SPIT running west from the headland's corner;
# south of the spit, and all along the cliff, the sea (-7.5) with its floes.
LAG_Z = -1.30
LAG_FLOOR = -1.75
SPIT_A = np.array([-41.5, 26.8])             # the spit leaves the headland's corner ...
SPIT_DIR = np.array([-0.94, 0.34])            # ... running west-south-west


def spit_off(x, y):
    """signed distance across the spit's centreline (+ = south, the sea side) and the distance along it"""
    v = np.stack([np.asarray(x) - SPIT_A[0], np.asarray(y) - SPIT_A[1]], -1)
    along = v @ SPIT_DIR
    across = v @ np.array([-SPIT_DIR[1], SPIT_DIR[0]])
    return across * -1.0, along

floor = np.array(L["floor"]["polygon"], float)
FP = Path(floor)
lanes = [(l["id"], Path(np.array(l["polygon"], float))) for l in L["lanes"]]


def bearing(x, y):
    return (np.degrees(np.arctan2(x, -y)) + 360.0) % 360.0


def smoothstep(e0, e1, x):
    t = np.clip((np.asarray(x, float) - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- the floor edge, densely sampled
def densify(poly, step):
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        k = max(1, int(math.ceil(np.linalg.norm(b - a) / step)))
        for j in range(k):
            out.append(a + (b - a) * (j / k))
    return np.array(out)


EDGE = densify(floor, 0.2)
TREE = cKDTree(EDGE)
tang = np.roll(EDGE, -10, 0) - np.roll(EDGE, 10, 0)
tang /= np.linalg.norm(tang, axis=1)[:, None]
nrm = np.stack([tang[:, 1], -tang[:, 0]], 1)
probe = FP.contains_points(EDGE + nrm * 0.6)
nrm[probe] *= -1.0                       # outward
EDGE_B = bearing(EDGE[:, 0], EDGE[:, 1])

# the beach -> cliff blend runs by the floor-edge point's bearing from the start: the wreck's beach at >= 242 deg,
# the cliff from <= 229 deg (the headland's south-west corner), the stair at ~156
T_BEACH, T_CLIFF = 243.0, 228.0


def t_of(b):
    return smoothstep(T_BEACH, T_CLIFF, b)


# the cliff-top margin (floor edge -> lip), wandering 0.8..3.4 m; tight at the cave and the stair
def lip_of(b):
    w = 2.1 + 0.9 * np.sin(np.radians(b) * 23.0) + 0.5 * np.sin(np.radians(b) * 57.0 + 1.3)
    w = np.where((b > 150) & (b < 198), 0.9, w)
    return np.clip(w, 0.8, 3.4)


def beach_z(d):
    d = np.asarray(d, float)
    z = np.interp(d, [0, 3.5, 8.0, 9.0, 10.5, 40], [0.0, -0.5, -1.12, -1.28, LAG_FLOOR, LAG_FLOOR])
    return z


CLIFF_DEPTH = 0.6          # the terrain stays on the cliff top this far past the lip, then drops away: the models ARE the face


def cliff_z(d, lip):
    # past the lip a steep TALUS (not a vertical curtain): where no model stands, the gap reads as a scree gully
    return np.where(d < lip + CLIFF_DEPTH, 0.0, np.interp(d - lip - CLIFF_DEPTH, [0, 0.5, 2.2, 40], [0.0, -1.0, DEEP, DEEP]))


# ---------------------------------------------------------------- the stream (the mere's outflow to the sea)
STREAM = np.array([[-16.0, -1.6], [-21.5, -0.2], [-28.0, 0.6], [-34.5, 0.2], [-40.0, 0.9], [-44.0, 1.7],
                   [-47.5, 2.7], [-51.0, 3.4], [-54.5, 4.6], [-58.0, 5.4]])
# a meander: a gentle sideways wiggle along the line (a few metres' wavelength), so it threads rather than runs
_seg = np.vstack([np.linspace(STREAM[i], STREAM[i + 1], max(2, int(np.linalg.norm(STREAM[i + 1] - STREAM[i]) / 0.5)), endpoint=False) for i in range(len(STREAM) - 1)] + [STREAM[-1:]])
_tan = np.gradient(_seg, axis=0)
_tan /= np.linalg.norm(_tan, axis=1)[:, None] + 1e-9
_arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(_seg, axis=0), axis=1))]
_amp = 0.9 * np.sin(_arc / 3.1) + 0.45 * np.sin(_arc / 1.37 + 0.8)
STREAM = _seg + np.stack([-_tan[:, 1], _tan[:, 0]], 1) * _amp[:, None]
ST_D = np.vstack([np.concatenate([np.linspace(STREAM[i], STREAM[i + 1], max(2, int(np.linalg.norm(STREAM[i + 1] - STREAM[i]) / 0.15)), endpoint=False) for i in range(len(STREAM) - 1)]), STREAM[-1:]])
ST_TREE = cKDTree(ST_D)

# ---------------------------------------------------------------- the terrain grid
nx = int((BX1 - BX0) * HPPM) + 1
ny = int((BY1 - BY0) * HPPM) + 1
gx = BX0 + np.arange(nx) / HPPM
gy = BY0 + np.arange(ny) / HPPM
GX, GY = np.meshgrid(gx, gy)
P = np.stack([GX.ravel(), GY.ravel()], 1)
inside = FP.contains_points(P).reshape(ny, nx)
dist, idx = TREE.query(P)
dist = dist.reshape(ny, nx)
idx = idx.reshape(ny, nx)
d_out = np.where(inside, 0.0, dist)
B = EDGE_B[idx]
T = t_of(B)
LIP = lip_of(B)


def noise(shape, sigma, seed):
    r = np.random.default_rng(seed).normal(size=shape)
    n = gaussian_filter(r, sigma)
    return n / (n.std() + 1e-9)


N1 = noise((ny, nx), 6.0, 1)
N2 = noise((ny, nx), 2.0, 2)
zb = beach_z(d_out) + (0.12 * N1 + 0.05 * N2) * smoothstep(0.5, 2.5, d_out) * (d_out < 9)
# the spit: a rock ridge (top ~ -0.4) on the centreline; north it falls to the lagoon flat, south to the deep sea
SO, SAL = spit_off(GX, GY)
spit_on = SAL > -2.0
ridge = -0.35 + 0.35 * N1 - 0.10 * np.clip(SAL - 10, 0, 30) / 10
north = np.maximum(zb, np.interp(-SO, [1.8, 4.0, 60], [-0.4, LAG_FLOOR, LAG_FLOOR]))   # the flank rising out of the lagoon
south = np.interp(SO, [2.2, 2.8, 4.6, 60], [-0.4, -1.2, DEEP, DEEP])                                   # the sea side drops away (models cover it)
zsp = np.where(SO < -1.8, north, np.where(SO <= 2.2, ridge, south))
zb = np.where(spit_on & (SO > -4.0), zsp, zb)
zc = cliff_z(d_out, LIP) + (0.12 * N1 + 0.05 * N2) * smoothstep(0.5, 2.0, d_out) * (d_out < LIP + CLIFF_DEPTH)
Z = (1 - T) * zb + T * zc
# the stream's gully (off the floor only)
sd, _ = ST_TREE.query(P)
sd = sd.reshape(ny, nx)
gully = 0.55 * np.clip(1 - (sd / 1.9) ** 2, 0, 1) * smoothstep(0.3, 2.0, d_out) * (Z > -7.0)
Z = Z - gully
# the stair's top landing is flush (z 0); under the cave cliff and the stair cliff the ground is deep
S = L["stair"]
Z[Path(np.array(S["top_landing"]["polygon"])).contains_points(P).reshape(ny, nx)] = 0.0
MODELS = {m["id"]: m for m in L["models"]}
for mid in ("cave_cliff", "stair_cliff"):
    fp = np.array(MODELS[mid]["footprint"], float)
    c = fp.mean(0)
    shrunk = c + (fp - c) * 0.9
    m = Path(shrunk).contains_points(P).reshape(ny, nx) & ~inside
    Z[m] = np.minimum(Z[m], DEEP)
# a SHINGLE BANK under the wreck: the beach rises to carry the hull (it lies on it, heeled toward the floor)
wfp0 = np.array(MODELS["wreck"]["footprint"], float)
wpts = densify(wfp0, 0.3)
dwk = cKDTree(wpts).query(P)[0].reshape(ny, nx)
dwk = np.where(Path(wfp0).contains_points(P).reshape(ny, nx), 0.0, dwk)
Z = np.maximum(Z, -0.75 - 0.42 * dwk - 0.10 * N1)
Z[inside] = 0.0

# blend into the BX heightfield over the box's outer BLEND metres
hf = L["sculpt"]["heightfield"]
H0 = np.fromfile(ROOT / hf["file"], dtype="<f4").reshape(hf["shape"])
ex = hf["extent_sim_m"]
hrow = (GY - ex["y0"]) * hf["px_per_m"]
hcol = (GX - ex["x0"]) * hf["px_per_m"]
Zbx = map_coordinates(H0, [hrow.ravel(), hcol.ravel()], order=1, mode="nearest").reshape(ny, nx)
edge_w = np.minimum.reduce([GX - BX0, BX1 - GX, GY - BY0, BY1 - GY])
wb = smoothstep(0.0, BLEND, edge_w)
Z = wb * Z + (1 - wb) * Zbx
Z[inside] = 0.0
Z = Z.astype("<f4")
assert float(np.abs(Z[inside]).max()) == 0.0


def z_at(x, y):
    c = (np.asarray(x) - BX0) * HPPM
    r = (np.asarray(y) - BY0) * HPPM
    return map_coordinates(Z, [np.atleast_1d(r), np.atleast_1d(c)], order=1, mode="nearest")


def edge_info(x, y):
    d, i = TREE.query([x, y])
    ins = FP.contains_point((x, y))
    return (0.0 if ins else d), i


# ---------------------------------------------------------------- water: distance from the shore (grid)
SOg, SALg = spit_off(GX, GY)
LAGOON = (SOg < 0) & (GX < -30.0)                 # north of the spit, west of the headland: the lagoon's water level
WL = np.where(LAGOON, LAG_Z, SEA_Z).astype("<f4")
water = Z < WL - 0.05
dw = distance_transform_edt(water) / HPPM          # metres from the nearest dry cell


def dw_at(x, y):
    return map_coordinates(dw, [np.atleast_1d((np.asarray(y) - BY0) * HPPM), np.atleast_1d((np.asarray(x) - BX0) * HPPM)], order=1, mode="nearest")


def wl_at(x, y):
    return map_coordinates(WL, [np.atleast_1d((np.asarray(y) - BY0) * HPPM), np.atleast_1d((np.asarray(x) - BX0) * HPPM)], order=0, mode="nearest")


def wet_at(x, y):
    return z_at(x, y) < wl_at(x, y) - 0.05


# the paint frame's ground footprint (with a margin) -- dressing and floes only where the camera can see them
def in_frame(x, y, z=0.0, m=2.0):
    sx = x
    sy = SA * y - CA * z
    return (SX0 - m <= sx <= SX0 + GW / PPM + m) and (SY0 - m <= sy <= SY0 + GH / PPM + m)


# ---------------------------------------------------------------- the dressing rule: off the floor, out of the lanes
def clear(x, y, r):
    if FP.contains_point((x, y)):
        return False
    d, _ = TREE.query([x, y])
    if d < r + 0.25:
        return False
    for _, lp in lanes:
        if lp.contains_point((x, y), radius=-(r + 0.25)) or lp.contains_point((x, y)):
            return False
    return True


# ---------------------------------------------------------------- the coast's real models
inst = {"cliff": [], "crag": [], "cairn": [], "stone_tall": [], "stone_mid": [], "log": []}
GLB = {"cliff": "godot/models/build/cliffplain.glb", "crag": "godot/models/build/crag.glb",
       "cairn": "runs/C-9/barrow_full/web_painted/models/barrow/kit/cairn.glb",
       "log": "runs/C-9/barrow_full/web_painted/models/barrow/kit/log.glb",
       "stone_tall": "runs/C-9/barrow_full/godot/models/barrow/stone_tall.glb",
       "stone_mid": "runs/C-9/barrow_full/godot/models/barrow/stone_mid.glb"}


def yaw_of(n):
    # godot rotation.y that turns the model's local +Z (its front) onto the sim direction n = (x, y_south)
    return math.degrees(math.atan2(n[0], n[1]))


def add(kind, x, y, z, yaw, size, r, **kw):
    inst[kind].append(dict(pos=[round(float(x), 3), round(float(y), 3)], z=round(float(z), 3), yaw=round(float(yaw), 2),
                           size=[round(float(s), 3) for s in size], r=round(float(r), 3), **kw))


# (a) the cliff chain: walk the floor edge from the headland's corner east to the cave cliff's west end, at a
# stride shorter than each face so neighbours overlap (no gap shows the drop behind them)
ia = int(TREE.query([-37.5, 27.0])[1]); ib = int(TREE.query([-10.8, 36.0])[1])
run = list(range(ia, ib + 1)) if ia < ib else list(range(ia, len(EDGE))) + list(range(0, ib + 1))
if len(run) > len(EDGE) / 2:
    run = list(range(ib, ia + 1))[::-1] if ib < ia else (list(range(ib, len(EDGE))) + list(range(0, ia + 1)))[::-1]
pts = EDGE[run]
seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
pattern = [  # (width, depth, top above floor, push outward, yaw jitter) -- spurs (deep, pushed) and bites (shallow, set back)
    (8.6, 6.4, 0.55, 0.6, 9), (6.8, 4.8, 0.25, -0.4, -12), (9.2, 7.2, 1.10, 1.4, 6), (7.4, 5.0, 0.35, -0.2, -7),
    (8.0, 6.0, 0.80, 0.9, 14), (6.4, 4.6, 0.20, -0.5, -10), (8.8, 6.8, 0.95, 1.1, 4), (7.2, 5.4, 0.45, 0.1, -15)]
s_ = 0.0
k = 0
while s_ <= seg[-1] + 0.5:
    w, dep, top, push, jit = pattern[k % len(pattern)]
    j = min(int(np.searchsorted(seg, s_)), len(pts) - 1)
    ei = run[j]
    p, n = EDGE[ei], nrm[ei]
    lip = float(lip_of(EDGE_B[ei]))
    c = p + n * (lip - 0.5 + dep * 0.5 + push * 0.7)   # its back tucked under the lip: the model is the cliff's edge and face
    zb = DEEP - 0.2
    add("cliff", c[0], c[1], zb, yaw_of(n) + jit, [w, top - zb, dep], 0.5 * w, note="cliff face (cliffplain), %s" % ("spur" if push > 0.5 else "bite" if push < 0 else "face"))
    s_ += w * 0.5
    k += 1
# one more face east of the stair (closes the frame's south-east corner against the BX cliff)
for b0 in (149.0,):
    ei = int(np.argmin(np.abs(EDGE_B - b0) + 1000 * (EDGE[:, 1] < 25)))
    p, n = EDGE[ei], nrm[ei]
    c = p + n * (1.0 + 3.2)
    add("cliff", c[0], c[1], DEEP - 0.2, yaw_of(n) - 6, [8.4, 0.5 - DEEP + 0.2, 6.4], 4.2, note="cliff face east of the stair")

# the SPIT's sea face: cliff faces along its south side, low crags along its back
sn = np.array([-SPIT_DIR[1], SPIT_DIR[0]]) * -1.0
sn = sn if sn[1] > 0 else -sn
for along, w, dep, top, jit in ((2.5, 7.4, 4.8, 0.45, -8), (8.6, 6.6, 4.4, 0.05, 10), (14.4, 7.8, 5.0, 0.30, -5), (20.6, 6.8, 4.4, -0.15, 12)):
    c = SPIT_A + SPIT_DIR * along + sn * (1.0 + dep * 0.5)
    add("crag", c[0], c[1], DEEP + 1.0, yaw_of(sn) + jit * 9, [w * 0.95, top - DEEP + 0.4, dep * 1.05], 0.5 * w, note="spit sea face (crag)")
for along in np.arange(1.0, 24.0, 2.6):
    c = SPIT_A + SPIT_DIR * along + sn * rng.uniform(-1.6, 0.6)
    w = rng.uniform(1.4, 2.8)
    add("crag", c[0], c[1], float(z_at(*c)[0]) - 0.5, rng.uniform(0, 360), [w, w * rng.uniform(0.45, 0.7), w * 0.8], w * 0.5, note="spit back rock")
# GAP FILL: walk the cliff's lip (bearing 148..236) every metre; wherever no model covers it, set another face there
def covers(q):
    for it in inst["cliff"] + [i for i in inst["crag"] if "spit" not in i["note"]]:
        a = math.radians(it["yaw"])
        ux, uz = np.array([math.cos(a), -math.sin(a)]), np.array([math.sin(a), math.cos(a)])
        v = q - np.array(it["pos"])
        if abs(v @ ux) <= it["size"][0] * 0.36 and abs(v @ uz) <= it["size"][2] / 2 + 0.6:
            return True
    for mid in ("cave_cliff", "stair_cliff"):
        if Path(np.array(MODELS[mid]["footprint"], float)).contains_point(q, radius=-0.8) or Path(np.array(MODELS[mid]["footprint"], float)).contains_point(q):
            return True
    return False


lipline = [i for i in range(0, len(EDGE), 3) if 148.0 <= EDGE_B[i] <= 236.0 and EDGE[i][1] > 20]
near_cave = lambda q: min(np.min(np.linalg.norm(densify(np.array(MODELS[m]["footprint"], float), 0.5) - q, axis=1)) for m in ("cave_cliff", "stair_cliff")) < 1.2
nfill = 0
for i in lipline:
    q = EDGE[i] + nrm[i] * (float(lip_of(EDGE_B[i])) + 0.9)
    if covers(q):
        continue
    lipn = float(lip_of(EDGE_B[i]))
    if near_cave(q):
        # beside the cave and the stair: a rounded crag plugs the notch, set back so it never crosses their faces
        w = float(rng.uniform(3.0, 4.2))
        c = EDGE[i] + nrm[i] * (lipn + w * 0.3)
        add("crag", c[0], c[1], DEEP + 0.5, rng.uniform(0, 360), [w, 0.6 - DEEP, w * 0.9], 0.5 * w, note="crag plug (gap fill)")
    else:
        w = float(rng.uniform(4.0, 6.0))
        dep = float(rng.uniform(4.2, 5.4))
        c = EDGE[i] + nrm[i] * (lipn - 0.5 + dep * 0.5)
        kind = "cliff" if rng.random() < 0.6 else "crag"
        add(kind, c[0], c[1], DEEP - 0.2, yaw_of(nrm[i]) + rng.uniform(-14, 14) + (180 if rng.random() < 0.4 else 0),
            [w, rng.uniform(0.2, 0.9) - DEEP + 0.2, dep], 0.5 * w, note="cliff face (gap fill)")
    nfill += 1
# the notch between the cave cliff and the stair cliff
add("crag", 4.3, 39.4, DEEP + 0.4, 37.0, [3.6, 0.7 - DEEP, 3.2], 1.8, note="crag plug (cave/stair notch)")
print("gap-fill faces:", nfill)

# (b) sea stacks and cliff-foot boulders in front of the spurs; the crag rock step down the beach
for i, cl in enumerate(list(inst["cliff"])[:-1]):
    if "spur" not in cl["note"]:
        continue
    yaw = math.radians(cl["yaw"])
    n = np.array([math.sin(yaw), math.cos(yaw)])
    t2 = np.array([n[1], -n[0]])
    c = np.array(cl["pos"]) + n * (cl["size"][2] * 0.5 + 1.6) + t2 * rng.uniform(-2.0, 2.0)
    h = rng.uniform(2.2, 3.6)
    add("crag", c[0], c[1], SEA_Z - 1.0, rng.uniform(0, 360), [rng.uniform(2.6, 4.0), h + 1.0, rng.uniform(2.2, 3.4)], 1.8, note="sea stack at a spur's foot")
for b0 in np.arange(244.0, 290.0, 3.4):            # the beach's rock step (d ~ 9.5-10.5): broken, with gaps
    if rng.random() < 0.22:
        continue
    ei = int(np.argmin(np.abs(EDGE_B - b0) + 1000 * (EDGE[:, 0] > -30)))
    p, n = EDGE[ei], nrm[ei]
    c = p + n * rng.uniform(5.5, 13.0) + np.array([n[1], -n[0]]) * rng.uniform(-0.8, 0.8)
    if rng.random() < 0.45 or not clear(c[0], c[1], 1.2) or spit_off(*c)[0] > -2.0:
        continue
    zz = float(z_at(*c)[0])
    w = rng.uniform(1.2, 2.6)
    add("crag", c[0], c[1], zz - 0.7 * w * 0.6, rng.uniform(0, 360), [w, w * 0.6, w * rng.uniform(0.6, 0.9)], w * 0.5, note="beach / lagoon boulder")
for b0 in (236.0, 232.5, 239.0):                   # the headland corner: boulders where the beach becomes cliff
    ei = int(np.argmin(np.abs(EDGE_B - b0)))
    p, n = EDGE[ei], nrm[ei]
    c = p + n * rng.uniform(7.5, 9.5)
    zz = float(z_at(*c)[0])
    w = rng.uniform(3.0, 4.6)
    add("crag", c[0], c[1], zz - 1.6, rng.uniform(0, 360), [w, rng.uniform(2.6, 3.6), w * 0.8], w * 0.5, note="corner boulder")


# cairns + standing stones on the cliff top (where the margin is wide) and the beach berm
def place_on_margin(b0, frac, r, tries=40):
    for _ in range(tries):
        b = b0 + rng.uniform(-1.5, 1.5)
        ei = int(np.argmin(np.abs(EDGE_B - b)))
        p, n = EDGE[ei], nrm[ei]
        lip = float(lip_of(EDGE_B[ei])) if EDGE_B[ei] < T_BEACH else 4.0
        c = p + n * max(r + 0.45, lip * frac + rng.uniform(-0.3, 0.6))
        if clear(c[0], c[1], r):
            return c
    return None


for b0, hgt in ((233.0, 1.35), (219.0, 1.1), (210.0, 1.5), (247.0, 1.2), (272.0, 1.25), (281.0, 1.0)):
    c = place_on_margin(b0, 1.6 if b0 < T_BEACH else 0.6, 0.6)
    if c is not None:
        add("cairn", c[0], c[1], float(z_at(*c)[0]) - 0.05, rng.uniform(0, 360), [hgt * 0.85, hgt, hgt * 0.85], 0.6, note="cairn")
for kind, b0, hgt in (("stone_tall", 214.5, 2.4), ("stone_mid", 224.0, 1.6), ("stone_mid", 203.0, 1.4)):
    c = place_on_margin(b0, 1.7, 0.55)
    if c is not None:
        add(kind, c[0], c[1], float(z_at(*c)[0]) - 0.15, rng.uniform(-30, 30) + 180, [0.9 * hgt / 2.4, hgt, 0.55 * hgt / 2.4], 0.55, note="standing stone", lean=round(float(rng.uniform(-7, 7)), 1))

# driftwood: the layout's nine logs (re-seated on the new ground) + more along the beach
for ins in MODELS["logs_and_beams"]["instances"]:
    a, b = np.array(ins["a"][:2]), np.array(ins["b"][:2])
    c = (a + b) / 2
    if not clear(c[0], c[1], 0.3):
        continue
    za, zb2 = float(z_at(*a)[0]), float(z_at(*b)[0])
    inst["log"].append(dict(a=[float(a[0]), float(a[1]), za + 0.14], b=[float(b[0]), float(b[1]), zb2 + 0.16], th=0.35, note="driftwood (layout " + ins["of"] + ")"))
n_log = 0
while n_log < 9:
    b = rng.uniform(244, 292)
    ei = int(np.argmin(np.abs(EDGE_B - b) + 1000 * (EDGE[:, 0] > -30)))
    p, n = EDGE[ei], nrm[ei]
    c = p + n * rng.uniform(2.5, 14.0)
    if wet_at(*c)[0] or not clear(c[0], c[1], 1.4):
        continue
    ang = rng.uniform(0, math.pi)
    ln = rng.uniform(1.6, 3.4)
    dv = np.array([math.cos(ang), math.sin(ang)]) * ln / 2
    a, b2 = c - dv, c + dv
    if wet_at(*a)[0] or wet_at(*b2)[0]:
        continue
    inst["log"].append(dict(a=[float(a[0]), float(a[1]), float(z_at(*a)[0]) + 0.12], b=[float(b2[0]), float(b2[1]), float(z_at(*b2)[0]) + 0.12],
                            th=float(rng.uniform(0.22, 0.38)), note="driftwood (beach)"))
    n_log += 1

# ---------------------------------------------------------------- ice: floes, shore-fast ice, pressure ridges
cave_front = np.array(L["stair"]["bottom_landing"]["polygon"], float)
CAVE_KEEP = Path(cave_front)
pts = []
X = rng.uniform(-66, 26, 60000)
Y = rng.uniform(-12, 62, 60000)
wet = wet_at(X, Y)
DW = dw_at(X, Y)
keep_pts = []
grid = {}
for x, y, w, dd in zip(X, Y, wet, DW):
    if not w or not in_frame(x, y, float(wl_at(x, y)[0]), 4.0):
        continue
    lag = float(wl_at(x, y)[0]) > -5
    r = (1.45 + 0.04 * dd) if lag else (1.5 + 0.08 * dd)   # the lagoon's fast ice: big plates near the shingle
    gk = (int(x // 1.0), int(y // 1.0))
    ok = True
    for ix in range(gk[0] - 6, gk[0] + 7):
        for iy in range(gk[1] - 6, gk[1] + 7):
            for q in grid.get((ix, iy), ()):
                if (q[0] - x) ** 2 + (q[1] - y) ** 2 < (r * 2) ** 2 * 0.55:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            break
    if ok:
        grid.setdefault(gk, []).append((x, y))
        keep_pts.append((x, y, dd))
sites = np.array([(p[0], p[1]) for p in keep_pts])
dws = np.array([p[2] for p in keep_pts])
far = np.array([[-200, -200], [200, -200], [200, 200], [-200, 200]])
# LAND SITES on the dry ground just above the waterline bound the shore-side cells (no runaway wedges)
dry_near = np.argwhere((~water) & (distance_transform_edt(~water) / HPPM < 3.0))
dry_near = dry_near[rng.choice(len(dry_near), min(len(dry_near), 2500), replace=False)]
land_sites = np.stack([BX0 + dry_near[:, 1] / HPPM, BY0 + dry_near[:, 0] / HPPM], 1)
vor = Voronoi(np.vstack([sites, far, land_sites]))
floes = []
for si in range(len(sites)):
    reg = vor.regions[vor.point_region[si]]
    if -1 in reg or len(reg) < 3:
        continue
    poly = vor.vertices[reg]
    site = sites[si]
    dd = dws[si]
    if (not lag) and (dd > 15 and rng.random() < 0.35 or dd > 24 and rng.random() < 0.6):
        continue                                  # open dark water out to sea
    if lag and dd > 4.0 and rng.random() < 0.10:
        continue                                  # dark LEADS of open water between the lagoon's plates
    if CAVE_KEEP.contains_point(site, radius=-3.0) or np.linalg.norm(site - np.array([-1.8, 44.5])) < 4.5:
        continue                                  # the cave's ledge and its mouth stay open water
    gap = (0.06 if dd < 2.0 else min(0.10 + 0.05 * dd, 0.7)) if lag else (0.05 if dd < 2.5 else min(0.12 + 0.07 * dd, 1.8))
    # ragged edges: subdivide, push each vertex in by the gap plus noise
    pp = []
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        k = max(1, int(np.linalg.norm(b - a) / 0.55))
        for j in range(k):
            pp.append(a + (b - a) * j / k)
    pp = np.array(pp)
    lvl = float(wl_at(*site)[0])
    lag = lvl > -5
    if np.linalg.norm(pp - site, axis=1).max() > 3.0 * ((1.45 + 0.04 * dd) if lag else (1.5 + 0.08 * dd)):
        continue
    v = pp - site
    ln = np.linalg.norm(v, axis=1)[:, None] + 1e-9
    inset = gap * 0.5 + np.abs(rng.normal(0, 0.10 + 0.012 * dd, (len(pp), 1)))
    pp = site + v * np.clip(1 - inset / ln, 0.15, 1)
    # rounder, more various plates: shrink some, then two Chaikin passes knock the Voronoi corners off
    if not (lag and dd < 2.0):
        pp = site + (pp - site) * (rng.uniform(0.88, 0.99) if dd < 8 else rng.uniform(0.7, 0.95))
    for _c in range(2):
        q1 = pp * 0.75 + np.roll(pp, -1, 0) * 0.25
        q2 = pp * 0.25 + np.roll(pp, -1, 0) * 0.75
        pp = np.stack([q1, q2], 1).reshape(-1, 2)
    pp = pp + rng.normal(0, 0.06, pp.shape)
    # pull any vertex that lands on the shore back toward the site
    for _ in range(14):
        dry = ~wet_at(pp[:, 0], pp[:, 1])
        if not dry.any():
            break
        pp[dry] = site + (pp[dry] - site) * 0.8
    if (~wet_at(pp[:, 0], pp[:, 1])).mean() > 0.1:
        continue
    area = 0.5 * abs(np.dot(pp[:, 0], np.roll(pp[:, 1], 1)) - np.dot(pp[:, 1], np.roll(pp[:, 0], 1)))
    if area < 0.35:
        continue
    fast = lag or dd < 2.5
    top = lvl + (0.20 if fast else 0.10) + rng.uniform(0, 0.10)
    floes.append(dict(poly=[[round(float(a), 3), round(float(b), 3)] for a, b in pp], top=round(float(top), 3),
                      bot=round(lvl - 0.35, 3), snow=round(float(rng.uniform(0.0, 1.0)), 2), fast=bool(fast)))

# brash: small broken bits in the gaps between floes out at sea
brash = []
for _ in range(4000):
    x, y = rng.uniform(-62, 24), rng.uniform(26, 56)
    if not wet_at(x, y)[0] or not in_frame(x, y, SEA_Z, 1.0) or float(wl_at(x, y)[0]) > -5:
        continue
    if CAVE_KEEP.contains_point((x, y), radius=-2.0):
        continue
    if len(brash) < 380:
        brash.append([round(x, 3), round(y, 3), round(SEA_Z + 0.05, 3), round(float(rng.uniform(0.15, 0.55)), 3), round(float(rng.uniform(0, 360)), 0)])

# pressure ridges: where the shore-fast ice meets the shingle (the beach's waterline), and a few along fast-ice seams
ridges = []
shore = np.argwhere((dw > 0.2) & (dw < 0.9))
rng.shuffle(shore)
seen = cKDTree(np.zeros((1, 2)) + 1e6)
placed = []
for r_, c_ in shore:
    x, y = BX0 + c_ / HPPM, BY0 + r_ / HPPM
    if not in_frame(x, y, LAG_Z, 1.0) or not LAGOON[r_, c_]:
        continue
    b = bearing(x, y)
    _, ei = TREE.query([x, y])
    if t_of(EDGE_B[ei]) > 0.6:
        continue                                   # the cliff foot has floes against it, not ridges
    if placed and min((x - p[0]) ** 2 + (y - p[1]) ** 2 for p in placed[-80:]) < 0.55 ** 2:
        continue
    placed.append((x, y))
    for _ in range(int(rng.integers(1, 3))):
        ridges.append(dict(pos=[round(x + rng.uniform(-0.3, 0.3), 3), round(y + rng.uniform(-0.3, 0.3), 3)], z=round(LAG_Z + rng.uniform(0.05, 0.35), 3),
                           size=[round(float(rng.uniform(0.5, 1.4)), 3), round(float(rng.uniform(0.18, 0.4)), 3), round(float(rng.uniform(0.4, 1.0)), 3)],
                           rot=[round(float(rng.uniform(-45, 45)), 1), round(float(rng.uniform(0, 360)), 1), round(float(rng.uniform(-35, 35)), 1)]))

# ---------------------------------------------------------------- shingle, heather, dry grass (instanced)
pebbles, heather, grass = [], [], []
HN = noise((ny, nx), 5.0, 7)


def hn_at(x, y):
    return map_coordinates(HN, [np.atleast_1d((y - BY0) * HPPM), np.atleast_1d((x - BX0) * HPPM)], order=1)[0]


for _ in range(26000):
    x, y = rng.uniform(-66, 24), rng.uniform(-12, 50)
    if not in_frame(x, y, -3.0, 1.0):
        continue
    if FP.contains_point((x, y)):
        continue
    z = float(z_at(x, y)[0])
    if z < float(wl_at(x, y)[0]) + 0.03:
        continue
    d, ei = TREE.query([x, y])
    t = float(t_of(EDGE_B[ei]))
    if t < 0.7 and 2.2 < d < 11 and len(pebbles) < 5200:
        if clear(x, y, 0.15):
            r = float(rng.uniform(0.06, 0.24))
            pebbles.append([round(x, 3), round(y, 3), round(z, 3), round(r, 3), round(float(rng.uniform(0, 360)), 0), round(float(rng.uniform(0.0, 1.0)), 2)])
        continue
for _ in range(90000):
    x, y = rng.uniform(-66, 24), rng.uniform(-12, 46)
    if not in_frame(x, y, 0.0, 1.0) or FP.contains_point((x, y)):
        continue
    z = float(z_at(x, y)[0])
    if z < -3.4:
        continue
    d, ei = TREE.query([x, y])
    t = float(t_of(EDGE_B[ei]))
    lip = float(lip_of(EDGE_B[ei]))
    on_top = t > 0.5 and d < lip + CLIFF_DEPTH - 0.6
    on_berm = t <= 0.5 and d < 6.5
    sdist = ST_TREE.query([x, y])[0]
    on_bank = 0.9 < sdist < 2.6
    if not (on_top or on_berm or on_bank):
        continue
    h = hn_at(x, y)
    if h < 0.15 and not on_bank:
        continue
    if not clear(x, y, 0.3):
        continue
    if rng.random() < 0.7:
        if len(heather) < 2600:
            heather.append([round(x, 3), round(y, 3), round(z, 3), round(float(rng.uniform(0.10, 0.24)), 3), round(float(rng.uniform(0, 1)), 2)])
    elif len(grass) < 420:
        grass.append([round(x, 3), round(y, 3), round(z, 3), round(float(rng.uniform(0.35, 0.75)), 3), int(rng.integers(5, 11))])

# ---------------------------------------------------------------- the stream's ice ribbon (sampled on the terrain)
rib = []
for i, p in enumerate(ST_D[::3]):
    ins = FP.contains_point(p)
    z = 0.012 if ins else float(z_at(*p)[0]) + 0.05
    w = 0.95 if ins else 1.25 - 0.25 * (i / (len(ST_D) / 3))
    rib.append([round(float(p[0]), 3), round(float(p[1]), 3), round(z, 3), round(w, 3)])
stream_rocks = []
for p in ST_D[::14]:
    if FP.contains_point(p):
        continue
    for side in (-1, 1):
        if rng.random() < 0.45:
            continue
        i = int(np.argmin(np.linalg.norm(ST_D - p, axis=1)))
        tv = ST_D[min(i + 1, len(ST_D) - 1)] - ST_D[max(i - 1, 0)]
        tv /= np.linalg.norm(tv) + 1e-9
        q = p + np.array([-tv[1], tv[0]]) * side * rng.uniform(1.0, 1.5)
        r = float(rng.uniform(0.25, 0.55))
        if clear(q[0], q[1], r) and not wet_at(*q)[0]:
            add("crag", q[0], q[1], float(z_at(*q)[0]) - r * 0.5, rng.uniform(0, 360), [r * 2.2, r * 1.3, r * 1.8], r, note="stream bank stone")

# ---------------------------------------------------------------- the ground colour (8 px/m over the box)
GPPM = 8.0
cw, ch = int((BX1 - BX0) * GPPM), int((BY1 - BY0) * GPPM)
cx = BX0 + (np.arange(cw) + 0.5) / GPPM
cy = BY0 + (np.arange(ch) + 0.5) / GPPM
CX, CY = np.meshgrid(cx, cy)
Q = np.stack([CX.ravel(), CY.ravel()], 1)
ins_c = FP.contains_points(Q).reshape(ch, cw)
dq, iq = TREE.query(Q)
dq = np.where(ins_c.ravel(), 0, dq).reshape(ch, cw)
tq = t_of(EDGE_B[iq]).reshape(ch, cw)
lq = lip_of(EDGE_B[iq]).reshape(ch, cw)
zq = map_coordinates(Z, [((CY - BY0) * HPPM).ravel(), ((CX - BX0) * HPPM).ravel()], order=1).reshape(ch, cw)
n1 = noise((ch, cw), 10.0, 11)
n2 = noise((ch, cw), 2.0, 12)
n3 = noise((ch, cw), 0.7, 13)
snow = np.array([0.93, 0.94, 0.96])
col = np.ones((ch, cw, 3)) * snow
col += (0.012 * n1 + 0.008 * n2)[..., None] * np.array([-1, -0.6, 0.4])
# the floor: a thin shingle-in-snow tint near the beach seeds, the worn path, the mere's ice
shs = np.array(L["zones"]["classes"]["shore_shingle"]["seeds"], float)
dsh = np.min(np.linalg.norm(Q[:, None, :] - shs[None], axis=2), 1).reshape(ch, cw)
tint = np.clip(np.exp(-dsh / 12.0) * 0.55 * (0.6 + 0.4 * (n2 > 0.3)), 0, 1)[..., None] * ins_c[..., None]
col = col * (1 - tint * 0.35) + tint * 0.35 * np.array([0.74, 0.74, 0.73])
mere = Path(np.array(L["mere"]["polygon"], float)).contains_points(Q).reshape(ch, cw)
col[mere] = np.array([0.70, 0.81, 0.90]) + (0.03 * n2[mere])[:, None]
pth = np.array(L["path"]["polyline"], float)
pdist = cKDTree(np.vstack([np.linspace(pth[i], pth[i + 1], 80) for i in range(len(pth) - 1)])).query(Q)[0].reshape(ch, cw)
pm = np.clip(1 - pdist / 0.8, 0, 1) * 0.5 * ins_c
col = col * (1 - pm[..., None]) + pm[..., None] * np.array([0.80, 0.77, 0.72])
# outside the floor
out = ~ins_c
beachw = (1 - tq) * out
shingle = np.array([0.57, 0.55, 0.52]) + (0.07 * n3)[..., None] * np.array([1, 1, 1]) + (0.03 * n2)[..., None] * np.array([1, 0.6, 0.2])
wetsh = np.array([0.40, 0.39, 0.38]) + (0.05 * n3)[..., None]
rock = np.array([0.52, 0.50, 0.47]) + (0.06 * n2)[..., None]
snowcov = np.clip(smoothstep(4.0, 1.0, dq) + (n1 > 0.9) * 0.6, 0, 1)            # snow over the berm, patchy below
bcol = shingle * (1 - snowcov[..., None]) + snow * snowcov[..., None]
bcol = np.where(((dq > 9.0) & (dq < 11.0))[..., None], rock, bcol)
bcol = np.where((dq >= 11.0)[..., None], wetsh, bcol)
iceline = smoothstep(-7.0, -7.4, zq)
bcol = bcol * (1 - iceline[..., None]) + iceline[..., None] * np.array([0.86, 0.90, 0.94])
top = np.clip(0.55 + 0.25 * n1 + 0.2 * n3, 0, 1)                                 # the cliff top: snow over scree
ccol = snow * top[..., None] + np.array([0.66, 0.64, 0.61]) * (1 - top[..., None])
ccol = np.where((zq < -0.5)[..., None], rock, ccol)
ocol = beachw[..., None] * bcol + ((1 - tq) * 0 + tq)[..., None] * ccol
SOq, SALq = spit_off(CX, CY)
spitm = ((np.abs(SOq) < 2.6) & (SALq > -2.0))[..., None]
ocol = np.where(spitm, snow * top[..., None] + np.array([0.60, 0.58, 0.55]) * (1 - top[..., None]), ocol)
col = np.where(out[..., None], ocol, col)
# the stream's ice and its banks
sq = ST_TREE.query(Q)[0].reshape(ch, cw)
bank = np.clip(1 - np.abs(sq - 1.1) / 0.5, 0, 1) * out
col = col * (1 - bank[..., None] * 0.5) + bank[..., None] * 0.5 * np.array([0.60, 0.57, 0.53])
ice = sq < 0.7
col[ice] = np.array([0.66, 0.79, 0.90]) + (0.04 * n3[ice])[:, None] - (0.06 * (sq[ice] < 0.2))[:, None]
img = Image.fromarray((np.clip(col, 0, 1) ** (1 / 1.0) * 255).round().astype(np.uint8))

# ---------------------------------------------------------------- the film route and the chunks the camera needs
ROUTE0 = [(-39.5, 5.0), (-39.0, 13.5), (-36.5, 21.0), (-31.0, 26.5), (-23.5, 30.5), (-14.0, 33.0), (-4.0, 34.5),
          (6.0, 35.0), (12.5, 34.6), (17.2, 37.6)]
route = []
for q in ROUTE0[:-1]:
    q = np.array(q, float)
    for _ in range(60):
        d, ei = TREE.query(q)
        if FP.contains_point(q) and d >= 1.6:
            break
        q = q - nrm[ei] * 0.25
    route.append([round(float(q[0]), 3), round(float(q[1]), 3)])
route.append(list(ROUTE0[-1]))                     # the last point stands on the stair's flush top landing
GDW, GDH = 1920 / 75.66840334752658 / 2, 1080 / 75.66840334752658 / 2
need = []
STILL_T = [(-38.7439, 10.7813), (-23.0, 27.5), (5.79, 42.6977)]
for t in STILL_T:
    need.append((t[0], SA * t[1]))
for i in range(len(route) - 1):
    a_, b_ = np.array(route[i]), np.array(route[i + 1])
    for f in np.linspace(0, 1, 12):
        q = a_ + (b_ - a_) * f
        need.append((q[0], SA * q[1]))
skip = []
for r in range(ROWS):
    for c in range(COLS):
        x0c, y0c = SX0 + c * 1280 / PPM, SY0 + r * 768 / PPM
        x1c, y1c = x0c + 1536 / PPM, y0c + 1024 / PPM
        hit = any(x0c - 0.5 < nx_ + GDW and x1c + 0.5 > nx_ - GDW and y0c - 0.5 < ny_ + GDH and y1c + 0.5 > ny_ - GDH for nx_, ny_ in need)
        if not hit:
            skip.append(f"{c}_{r}")

# ---------------------------------------------------------------- the checks, then write
checks = {}
bad = []
for kind in ("cairn", "stone_tall", "stone_mid"):
    for it in inst[kind]:
        if not clear(it["pos"][0], it["pos"][1], it["r"] - 0.01):
            bad.append((kind, it["pos"]))
for it in inst["log"]:
    for q in (it["a"], it["b"]):
        if FP.contains_point((q[0], q[1])):
            bad.append(("log", q))
for arr, nm, r in ((pebbles, "pebble", 0.15), (heather, "heather", 0.3), (grass, "grass", 0.3)):
    for p in arr:
        if not clear(p[0], p[1], r - 0.01):
            bad.append((nm, p[:2]))
cl_bad = [c["pos"] for c in inst["cliff"] + inst["crag"] if FP.contains_point(tuple(c["pos"]))]
checks["dressing_off_floor_and_lanes"] = {"pass": not bad, "offenders": bad[:20]}
checks["models_centres_off_floor"] = {"pass": not cl_bad, "offenders": cl_bad}
checks["terrain_zero_on_floor"] = {"pass": float(np.abs(Z[inside]).max()) == 0.0}
OUT.mkdir(parents=True, exist_ok=True)
Z.tofile(OUT / "terrain.f32")
img.save(OUT / "ground.png", optimize=True)
wreck = MODELS["wreck"]
wfp = np.array(wreck["footprint"])
wz = [round(float(z_at(*p)[0]), 2) for p in wfp]
doc = {
    "_what": __doc__.split("\n\n")[0],
    "ruling": "R-C9-158",
    "frame": {"cols": COLS, "rows": ROWS, "size_px": [GW, GH], "sx0_m": SX0, "sy0_m": SY0, "ppm": PPM, "pitch_deg": math.degrees(PITCH),
              "law": "guide px = ((x - sx0) * ppm, (sin(a) y - cos(a) z - sy0) * ppm), sim frame"},
    "box": {"x0": BX0, "x1": BX1, "y0": BY0, "y1": BY1, "blend_m": BLEND},
    "terrain": {"file": "data/section_sw/terrain.f32", "px_per_m": HPPM, "shape": [ny, nx], "sha256": hashlib.sha256(Z.tobytes()).hexdigest()},
    "ground": {"file": "data/section_sw/ground.png", "px_per_m": GPPM},
    "sea_z": SEA_Z,
    "skip_models": ["cliff_faces", "rock_outcrop_10", "rock_outcrop_11", "logs_and_beams"],
    "skip_blob_kinds_in_box": ["rock", "ice", "floe", "ripple"],
    "wreck_ground_z_at_corners": wz,
    "glb": GLB,
    "instances": inst,
    "floes": floes, "ridges": ridges, "brash": brash,
    "pebbles": pebbles, "heather": heather, "grass": grass,
    "stream": {"polyline": STREAM.tolist(), "ribbon": rib},
    "checks": checks,
    "film_route": route, "stills_targets": STILL_T, "paint_skip": skip,
    "counts": {k: len(v) for k, v in inst.items()} | {"floes": len(floes), "ridges": len(ridges), "pebbles": len(pebbles), "heather": len(heather), "grass": len(grass)},
}
json.dump(doc, open(OUT / "section.json", "w"), indent=1)
print(json.dumps({"skip": skip, "route": route, "counts": doc["counts"], "checks": {k: v["pass"] for k, v in checks.items()}, "wreck_ground_z": wz, "grid": [ny, nx], "guide_px": [GW, GH]}))
