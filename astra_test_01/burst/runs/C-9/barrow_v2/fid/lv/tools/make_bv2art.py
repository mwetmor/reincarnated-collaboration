#!/usr/bin/env python3
"""BV2F lane LV, PHASE 1' (Matt R-C9-185; charter v1.0 s 15): barrow_v2 ART-FIRST -- the layout of record, built the way v1's was.

    python3 fid/lv/tools/make_bv2art.py

v1 PRACTICE, MIRRORED (barrow_full/tools/make_layout.py -> barrow_full_layout.json): ONE script turns the composition into
ONE layout everything downstream reads; the frame is v1's camera-aligned (u, v) -- true ground metres, +u screen-right,
+v up-screen, from the play camera's own basis (pitch 52.95354112560294, yaw 47); placements carry `uv`, a facing, a uniform
`scale`, the GLB and the class; regions carry the ground; bounds are the walkable land; the window is a canvas grid.

THE COMPOSITION IS SKETCH A, LITERALLY (barrow_v2/sites/BV3r2-A.png). Sketch A is drawn at about the play camera's own angle,
so its pixels ARE a map: a point on the ground at sketch pixel (x, y) sits at
    u = (x - 780) / S          v = (452 - y) / (S * sin(pitch))        S = 24 sketch px per metre across
(780, 452) is sketch A's "you start here"; S makes the sketch ~64 m across -- v1's footprint (R-C9-185: ~55-65 m), and it
puts sketch A's own wreck at 13.2 m, the kit-v3 wreck's true length. A point drawn at height z shows (z * S * cos(pitch)) px
lower in the sketch for sea-level things (z < 0); every sketch reading below is a GROUND point (base / threshold / waterline).
Sketch A is not to scale between pieces; each hero is sized by its own sketch footprint, by ONE uniform scale (principle 3).

Writes:
  fid/lv/art/layout_bv2art.json                 the layout of record (v1-style)
  barrow_full/godot/data/bv2f/art/level.json    + terrain_h.f32, classes_png.bin (what scripts/bv2f/bv2f_level.gd reads)
  fid/lv/art/frame_grid_s??.json                the Tier-B --frame-grid configs (2 x 2 guide sections)
"""
import hashlib
import json
import math
import os
import shutil

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
BV2 = os.path.normpath(os.path.join(LV, "..", ".."))
C9 = os.path.dirname(BV2)
RUNS = os.path.dirname(C9)
BF = os.path.join(C9, "barrow_full", "godot")
OUT = os.path.join(BF, "data", "bv2f", "art")
EXT = os.path.join(BF, "data", "bv2f", "ext")
ART = os.path.join(LV, "art")

PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
SP, CP = math.sin(PITCH), math.cos(PITCH)
PX_V = PPM * SP
S = 24.0                                   # sketch px per metre across
START_PX = (780.0, 452.0)
SEA_Z = -6.0
HF_PPM = 4.0
EXT_UV = {"u": [-42.0, 42.0], "v": [-36.0, 36.0]}
CLS_PPM = 16.0
V1M = "runs/C-9/barrow_full/web_painted/models/barrow/"
AABB = json.load(open(os.path.join(LV, "models", "glb_aabb.json")))


def uv(px, z=0.0):
    """sketch A ground pixel -> (u, v) metres. z < 0: the point is drawn that much lower (sea level)."""
    x, y = px
    return ((x - START_PX[0]) / S, (START_PX[1] - (y + z * S * CP)) / (S * SP))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def ab(glb):
    for k, v in AABB.items():
        if k.endswith(glb.replace("runs/", "", 1)) or (glb.startswith("data/bv2f/") and k.endswith("/" + glb)):
            return v["godot_xyz_m"]
    raise KeyError(glb)


def unit(x, y):
    n = math.hypot(x, y)
    return (x / n, y / n)


# ============ THE COMPOSITION (sketch A pixels) ============
WRECK = {"glb": "data/bv2f/models/wreck.glb", "prow": (75, 345), "stern": (330, 495), "len_m": 13.0, "sink": 1.1}
HALL = {"glb": "data/bv2f/models/hall.glb", "door": (1290, 450), "wall_a": (1170, 395), "wall_b": (1345, 515), "len_m": 18.5}
GABLE = {"glb": "data/bv2f/models/gable.glb", "centre": (1430, 585), "size_m": 8.0}
BARROW = {"glb": "data/bv2f/models/barrow.glb", "door": (818, 150), "width_m": 11.6}
MOUND = {"centre": (830, -10), "semi_m": (15.0, 8.5), "rise_m": 5.5}
RING_STAND = [((690, 455), 2.2, "tall"), ((722, 505), 1.7, "mid"), ((780, 385), 1.9, "tall"), ((862, 420), 2.1, "mid"), ((846, 492), 2.0, "tall")]
RING_LIE = [((742, 425), 25.0), ((805, 512), -15.0), ((830, 535), 60.0)]
SLOPE_STONES = [((600, 40), 2.4, "tall"), ((520, 105), 1.8, "mid"), ((690, 185), 2.0, "mid"), ((925, 180), 2.2, "tall"), ((1130, 40), 2.0, "mid"),
                ((1190, 90), 2.3, "tall"), ((380, 365), 1.4, "short"), ((930, 700), 1.6, "short")]
CRAGS = [((515, 600), 3.0), ((265, 600), 2.6), ((175, 640), 2.2), ((440, 640), 2.4), ((1235, 175), 2.0), ((1500, 360), 2.4), ((60, 190), 2.6)]
# the coast: the shore line (W, land to its east) and the cliff lip (S, land to its north), as one chain
SHORE = [(175, -60), (165, 120), (150, 200), (175, 265), (255, 320), (345, 395), (345, 470), (290, 535), (220, 565)]   # the wreck lies OUT on the shore ice
LIP = [(220, 565), (300, 640), (420, 612), (520, 600), (600, 640), (700, 688), (820, 718), (950, 755), (1050, 795), (1150, 855),
       (1260, 925), (1360, 985), (1460, 1035), (1600, 1100)]
MERE = [(115, 145), (250, 112), (400, 150), (560, 168), (622, 238), (588, 318), (455, 335), (322, 302), (205, 272), (125, 222)]
STREAM = [(655, 70), (618, 115), (585, 150), (560, 172)]
PATHS = [[(818, 175), (800, 300), (785, 440)], [(780, 452), (720, 560), (668, 640)]]
SHINGLE = [(150, 200), (180, 265), (260, 320), (350, 392), (352, 470), (296, 538), (225, 568), (290, 600), (395, 530), (430, 430), (380, 340), (250, 260), (200, 190)]
YARD = [(1105, 385), (1300, 330), (1525, 470), (1500, 650), (1250, 660), (1140, 545)]
SHRUB = [((470, 330), 70), ((380, 250), 60), ((640, 300), 50), ((600, 455), 45), ((900, 300), 55), ((1000, 470), 60), ((1060, 230), 70),
         ((720, 220), 50), ((420, 520), 50), ((1000, 650), 45), ((880, 610), 40), ((260, 40), 80), ((470, 60), 60)]
PALISADE = [[(1040, 375), (1110, 340), (1165, 312)], [(1330, 238), (1430, 262), (1530, 300)], [(1150, 560), (1200, 625), (1265, 690), (1420, 702)]]
LOGS = [((1370, 262), (1445, 302)), ((1250, 565), (1330, 622)), ((1300, 625), (1385, 660)), ((25, 485), (100, 505)), ((1335, 440), (1395, 475))]
CAVE = {"mouth_px": (560, 795), "w_m": 4.4, "h_m": 3.6}
STAIR = {"foot_px": (610, 780), "top_px": (688, 690), "width_m": 2.2, "rise": 0.18, "tread": 0.27}
FLOES = [(40, 640), (110, 690), (60, 760), (150, 760), (230, 820), (110, 860), (300, 880), (200, 930), (380, 960), (480, 1000), (30, 900),
         (20, 560), (290, 1000), (420, 900), (30, 300), (25, 380), (35, 230)]


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(ART, exist_ok=True)
    os.makedirs(EXT, exist_ok=True)
    shore = [uv(p) for p in SHORE]
    lip = [uv(p) for p in LIP]
    coast = shore + lip[1:]
    # ---------------- terrain + classes over EXT_UV ----------------
    u0, u1 = EXT_UV["u"]
    v0, v1 = EXT_UV["v"]
    W = int((u1 - u0) * HF_PPM) + 1
    H = int((v1 - v0) * HF_PPM) + 1
    us = u0 + np.arange(W) / HF_PPM
    vs = v1 - np.arange(H) / HF_PPM                   # rows north -> south (sim y0 -> y1)
    U, V = np.meshgrid(us, vs)

    def mask(poly, Uq, Vq, ppm, ou, ov):
        img = Image.new("L", (Uq.shape[1], Uq.shape[0]), 0)
        ImageDraw.Draw(img).polygon([((p[0] - ou) * ppm, (ov - p[1]) * ppm) for p in poly], fill=1)
        return np.asarray(img).astype(bool)

    land_poly = coast + [(u1 + 5, lip[-1][1]), (u1 + 5, v1 + 5), (shore[0][0], v1 + 5)]
    land = mask(land_poly, U, V, HF_PPM, u0, v1)

    def dist_to_chain(chain, Uq, Vq):
        d = np.full(Uq.shape, 1e9)
        for (a, b) in zip(chain[:-1], chain[1:]):
            ax, ay, bx, by = a[0], a[1], b[0], b[1]
            dx, dy = bx - ax, by - ay
            t = np.clip(((Uq - ax) * dx + (Vq - ay) * dy) / (dx * dx + dy * dy), 0, 1)
            d = np.minimum(d, np.hypot(Uq - (ax + t * dx), Vq - (ay + t * dy)))
        return d
    d_shore = dist_to_chain(shore, U, V)
    d_lip = dist_to_chain(lip, U, V)
    Z = np.zeros(U.shape, np.float32)
    rng = np.random.default_rng(185)
    # W: the beach falls 0 -> -0.5 over 4 m to the grounded SHORE ICE shelf (-0.5) 9 m wide, then drops to the sea floor
    west = ~land & (d_shore < d_lip)
    beach = np.clip(d_shore / 4.0, 0, 1)
    ice_w = 13.0
    shelf = -0.5 - (np.clip((d_shore - ice_w) / 3.0, 0, 1) ** 1.5) * 8.0
    Z = np.where(west, np.where(d_shore < 4.0, -0.5 * beach, shelf), Z)
    # S: the cliff -- a near-vertical face from the lip to the sea floor (-9) within 1.6 m; a 1.6 m ledge at the stair foot
    south = ~land & ~west
    Z = np.where(south, -0.4 - 8.6 * np.clip(d_lip / 1.6, 0, 1) ** 0.6, Z)
    # N: the barrow mound (the kit front stands in its south toe)
    mc = uv(MOUND["centre"])
    a_, b_ = MOUND["semi_m"]
    rho = np.hypot((U - mc[0]) / a_, (V - mc[1]) / b_)
    dome = MOUND["rise_m"] * np.clip(1 - rho ** 2, 0, None) ** 0.45
    # the door's FORECOURT: the mound is cut back in front of the carved front (its threshold at ground level)
    bdc = uv(BARROW["door"])
    fc = (np.abs(U - bdc[0]) < 7.0) & (V < bdc[1] + 1.0)
    dome = np.where(fc, 0.0, dome)
    Z = np.where(land, np.maximum(Z, dome), Z)
    # gentle snow swells on the land outside the walkable centre (never on the floor around the start)
    swell = 0.35 * np.sin(U / 6.3 + 1.1) * np.sin(V / 5.1 + 0.4) * np.clip((np.hypot(U, V) - 22.0) / 8.0, 0, 1)
    Z = np.where(land & (dome < 0.05), Z + np.maximum(swell, 0), Z)
    # the stair: a sea-level LEDGE in front of the cave and the stair's foot
    cave_c = uv(CAVE["mouth_px"], SEA_Z)
    foot = uv(STAIR["foot_px"], SEA_Z)
    ledge_poly = [(cave_c[0] - 4.0, cave_c[1] + 0.6), (foot[0] + 2.0, foot[1] + 0.6), (foot[0] + 2.0, foot[1] - 2.2), (cave_c[0] - 4.0, cave_c[1] - 2.2)]
    led = mask(ledge_poly, U, V, HF_PPM, u0, v1) & south
    Z = np.where(led, SEA_Z + 0.4, Z)
    Z = Z.astype("<f4")
    Z.tofile(os.path.join(OUT, "terrain_h.f32"))
    # ---- classes at CLS_PPM ----
    names = ["none", "snow", "path", "ice", "shrub", "rock", "mound", "shingle", "shore_ice", "stream", "char", "sea", "wood", "passage_dark", "ash"]
    Wc = int((u1 - u0) * CLS_PPM)
    Hc = int((v1 - v0) * CLS_PPM)
    Uc, Vc = np.meshgrid(u0 + (np.arange(Wc) + 0.5) / CLS_PPM, v1 - (np.arange(Hc) + 0.5) / CLS_PPM)
    fi = np.clip(((Uc - u0) * HF_PPM).astype(int), 0, W - 1)
    fj = np.clip(((v1 - Vc) * HF_PPM).astype(int), 0, H - 1)
    Zc = Z[fj, fi]
    landc = mask(land_poly, Uc, Vc, CLS_PPM, u0, v1)
    dsc = dist_to_chain(shore, Uc, Vc)
    dlc = dist_to_chain(lip, Uc, Vc)
    C = np.full(Uc.shape, names.index("snow"), np.uint8)
    rhoc = np.hypot((Uc - mc[0]) / a_, (Vc - mc[1]) / b_)
    C[landc & (rhoc < 1.0)] = names.index("mound")
    for (p, r) in SHRUB:
        c = uv(p)
        rr = r / S
        n_ = 0.35 * np.sin(Uc * 1.7 + p[0]) * np.sin(Vc * 1.3 + p[1])
        C[landc & (np.hypot(Uc - c[0], Vc - c[1]) < rr * (1 + n_))] = names.index("shrub")
    C[mask([uv(p) for p in SHINGLE], Uc, Vc, CLS_PPM, u0, v1) & landc] = names.index("shingle")
    westc = ~landc & (dsc < dlc)
    C[westc & (dsc < 4.0)] = names.index("shingle")
    C[westc & (dsc >= 4.0) & (Zc > SEA_Z + 0.1)] = names.index("shore_ice")
    C[mask([uv(p) for p in YARD], Uc, Vc, CLS_PPM, u0, v1)] = names.index("ash")

    def line_mask(pl, w):
        img = Image.new("L", (Wc, Hc), 0)
        d = ImageDraw.Draw(img)
        pts = [((q[0] - u0) * CLS_PPM, (v1 - q[1]) * CLS_PPM) for q in pl]
        d.line(pts, fill=1, width=int(w * CLS_PPM), joint="curve")
        for q in pts:
            r = w * CLS_PPM / 2
            d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=1)
        return np.asarray(img).astype(bool)
    for pl in PATHS:
        C[line_mask([uv(p) for p in pl], 1.4) & landc] = names.index("path")
    C[mask([uv(p) for p in MERE], Uc, Vc, CLS_PPM, u0, v1)] = names.index("ice")
    C[line_mask([uv(p) for p in STREAM], 1.8)] = names.index("stream")
    southc = ~landc & ~westc
    C[southc & (Zc > SEA_Z + 0.05)] = names.index("rock")
    C[mask(ledge_poly, Uc, Vc, CLS_PPM, u0, v1)] = names.index("rock")
    C[Zc <= SEA_Z + 0.05] = names.index("none")             # under the sea plane
    Image.fromarray(C, "L").save(os.path.join(OUT, "classes.png"))
    shutil.copyfile(os.path.join(OUT, "classes.png"), os.path.join(OUT, "classes_png.bin"))

    # ---------------- placements ----------------
    models, layout_pl, blobs, openings = [], [], [], []
    glb_copies = {}

    def ext(glb):
        key = glb.replace("/", "__") + ".bin"
        src = os.path.join(BF, glb) if glb.startswith("data/bv2f/") else os.path.join(RUNS, glb[5:])
        if key not in glb_copies:
            shutil.copyfile(src, os.path.join(EXT, key))
            glb_copies[key] = {"from": glb, "sha256": sha(src)}
        return "data/bv2f/ext/" + key

    def yaw_of(face_uv):
        fs = (face_uv[0], -face_uv[1])                   # sim (x, y) = (u, -v)
        return math.degrees(math.atan2(fs[0], fs[1]))

    def model(mid, cls, glb, c_uv, face_uv, s, z=0.0, piece=None, lie=False, note=""):
        bx, by, bz = ab(glb)
        dims = (by, bx, bz) if lie else (bx, by, bz)
        w, h, d = dims[0] * s, dims[1] * s, dims[2] * s
        ins = {"type": "box", "pos": [round(c_uv[0], 4), round(-c_uv[1], 4)], "z": round(z, 3), "godot_rot_y_deg": round(yaw_of(face_uv), 3),
               "size_m": [round(w, 4), round(d, 4), round(h, 4)], "glb": ext(glb), "uniform_scale": round(s, 5)}
        if lie:
            ins["lie_z90"] = True
        layout_pl.append({"id": mid, "piece": piece or mid, "class": cls, "kind": "model", "glb": glb, "uv": [round(c_uv[0], 4), round(c_uv[1], 4)],
                          "z": round(z, 3), "facing_uv": [round(face_uv[0], 4), round(face_uv[1], 4)], "scale": round(s, 5), "lying": lie,
                          "size_m": {"w": round(w, 3), "d": round(d, 3), "h": round(h, 3)}, "note": note})
        return ins

    def hz(c):
        i = int(round((c[0] - u0) * HF_PPM))
        j = int(round((v1 - c[1]) * HF_PPM))
        return float(Z[min(max(j, 0), H - 1), min(max(i, 0), W - 1)])

    def hz_min(c, r):
        return min(hz((c[0] + dx, c[1] + dy)) for dx in (-r, 0, r) for dy in (-r, 0, r))
    # -- the wreck (W): heeled, half-sunk in the shore ice, prow up (upper-left), its open hull to the camera
    pa, pb = uv(WRECK["prow"]), uv(WRECK["stern"])
    ax_ = unit(pb[0] - pa[0], pb[1] - pa[1])
    face = (-ax_[1], ax_[0]) if -ax_[0] < 0 else (ax_[1], -ax_[0])
    if face[1] > 0:
        face = (-face[0], -face[1])
    wc = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
    sw = WRECK["len_m"] / ab(WRECK["glb"])[0]
    wins = model("wreck", "wood", WRECK["glb"], wc, face, sw, z=hz_min(wc, 2.0) - WRECK["sink"], note="sketch A: prow upper-left, stern lower-right, half-sunk")
    models.append({"id": "wreck", "kind": "wreck", "pos": wins["pos"], "z": wins["z"], "godot_rot_y_deg": wins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": wins["size_m"][0], "d_local_z": wins["size_m"][1], "h": wins["size_m"][2]}, "glb": wins["glb"]})
    wl = WRECK["len_m"]
    wb = ab(WRECK["glb"])[2] * sw
    openings.append({"id": "wreck_hull", "point": "W", "model": "wreck", "centre_sim": wins["pos"], "z0": 0.0, "w": None, "h": None, "faces_deg": None, "dark": False,
                     "probe": {"type": "h_rect", "centre": wins["pos"], "rot_deg": round(math.degrees(math.atan2(-ax_[1], ax_[0])), 3), "L": round(0.7 * wl, 3), "W": round(0.45 * wb, 3),
                               "z": 0.3, "frontal_m2": round(0.7 * wl * 0.45 * wb, 3)}})
    # -- the barrow front (N): its door threshold at the sketch's door, facing the camera
    bd = uv(BARROW["door"])
    sb = BARROW["width_m"] / ab(BARROW["glb"])[0]
    face_b = (0.0, -1.0)
    cb = (bd[0], bd[1] + 8.2 * sb * (25.8 / ab(BARROW["glb"])[0]) / (25.8 / ab(BARROW["glb"])[0]))
    bins = model("barrow_front", "rock", BARROW["glb"], cb, face_b, sb, z=0.0, note="the monumental carved door; door %.2f x %.2f m" % (5.81 * sb * 25.8 / ab(BARROW["glb"])[0], 6.67 * sb * 25.8 / ab(BARROW["glb"])[0]))
    models.append({"id": "barrow_front", "kind": "barrow", "pos": bins["pos"], "z": 0.0, "godot_rot_y_deg": bins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": bins["size_m"][0], "d_local_z": bins["size_m"][1], "h": bins["size_m"][2]}, "glb": bins["glb"]})
    k_b = sb * 25.8 / ab(BARROW["glb"])[0]
    openings.append({"id": "barrow_door", "point": "N", "model": "barrow_front", "centre_sim": [round(bd[0], 4), round(-bd[1], 4)], "z0": 0.0,
                     "w": round(5.81 * k_b, 3), "h": round(6.67 * k_b, 3), "faces_deg": 180.0, "curtain_inset_m": 0.8, "dark": True})
    # -- the hall (E): sketch A's long side + great door facing the start; one uniform scale
    wa, wb2 = uv(HALL["wall_a"]), uv(HALL["wall_b"])
    wdir = unit(wb2[0] - wa[0], wb2[1] - wa[1])
    door = uv(HALL["door"])
    nrm = (-wdir[1], wdir[0])
    if nrm[0] * (0 - door[0]) + nrm[1] * (0 - door[1]) < 0:
        nrm = (-nrm[0], -nrm[1])
    sh = HALL["len_m"] / ab(HALL["glb"])[0]
    k_h = sh * 32.4 / ab(HALL["glb"])[0]
    # the build's door: 3.5875 m (at 32.4 m) toward its local -X, its porch mouth 8.233 m in front of its centre
    fs = (nrm[0], -nrm[1])
    th = math.atan2(fs[0], fs[1])
    Xs = (math.cos(th), -math.sin(th))
    Xuv = (Xs[0], -Xs[1])
    hc = (door[0] - nrm[0] * 8.233 * k_h + Xuv[0] * 3.5875 * k_h, door[1] - nrm[1] * 8.233 * k_h + Xuv[1] * 3.5875 * k_h)
    hins = model("longhall", "wood", HALL["glb"], hc, nrm, sh, z=0.0, note="the burnt hall as sketch A draws it: long side and great door facing the start")
    models.append({"id": "longhall", "kind": "building", "pos": hins["pos"], "z": 0.0, "godot_rot_y_deg": hins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": hins["size_m"][0], "d_local_z": hins["size_m"][1], "h": hins["size_m"][2]}, "glb": hins["glb"]})
    openings.append({"id": "hall_great_door", "point": "E", "model": "longhall", "centre_sim": [round(door[0], 4), round(-door[1], 4)], "z0": 0.0,
                     "w": round(4.55 * k_h, 3), "h": round(4.75 * k_h, 3), "faces_deg": round(math.degrees(math.atan2(fs[0], -fs[1])) % 360, 3),
                     "curtain_inset_m": 1.6 * k_h, "dark": True})
    # -- the fallen gable (SE): its OWN ruin, facing the start
    gc = uv(GABLE["centre"])
    gn = unit(-gc[0], -gc[1])
    sg = GABLE["size_m"] / ab(GABLE["glb"])[0]
    gins = model("fallen_gable", "char", GABLE["glb"], gc, gn, sg, z=hz_min(gc, 3.0) - 0.05, note="its own collapsed ruin (R-C9-177/185)")
    models.append({"id": "fallen_gable", "kind": "ruin", "pos": gins["pos"], "z": gins["z"], "godot_rot_y_deg": gins["godot_rot_y_deg"],
                   "size_m": {"w_local_x": gins["size_m"][0], "d_local_z": gins["size_m"][1], "h": gins["size_m"][2]}, "glb": gins["glb"]})
    openings.append({"id": "gable_breach", "point": "SE", "model": "fallen_gable", "centre_sim": gins["pos"], "z0": 0.0, "w": None, "h": None, "faces_deg": None, "dark": False,
                     "probe": {"type": "h_rect", "centre": [round(gc[0] + gn[0] * 1.6, 4), round(-(gc[1] + gn[1] * 1.6), 4)],
                               "rot_deg": round(math.degrees(math.atan2(-gn[0], -gn[1])), 3), "L": 4.0, "W": 4.0, "z": round(0.5 * gins["size_m"][2], 3), "frontal_m2": 16.0}})
    # -- v1's stones: the broken ring at the start, the barrow-slope stones (uniform scale, rotation only)
    stone_insts = []
    slope_insts = []
    for i, (p, ht, kind_) in enumerate(SLOPE_STONES):
        g = V1M + "stone_%s.glb" % kind_
        s_ = ht / ab(g)[1]
        c = uv(p)
        rot = (math.sin(i * 1.9 + 1), -abs(math.cos(i * 1.9 + 1)) - 0.2)
        slope_insts.append(model("slope_stone_%d" % i, "rock", g, c, unit(*rot), s_, z=hz_min(c, 0.6) - 0.1))
    models.append({"id": "slope_stones", "kind": "stones", "pos": [0, 0], "z": 0, "godot_rot_y_deg": 0, "size_m": {"w_local_x": 1, "d_local_z": 1, "h": 1}, "instances": slope_insts, "glb": None})
    for i, (p, ht, kind_) in enumerate(RING_STAND):
        g = V1M + "stone_%s.glb" % kind_
        s_ = ht / ab(g)[1]
        c = uv(p)
        rot = (math.sin(i * 2.3), -abs(math.cos(i * 2.3)) - 0.2)
        stone_insts.append(model("stone_%d" % i, "rock", g, c, unit(*rot), s_, z=hz_min(c, 0.6) - 0.1))
    for i, (p, deg) in enumerate(RING_LIE):
        g = V1M + "stone_tall.glb"
        s_ = 1.4 / ab(g)[1]
        c = uv(p)
        a = math.radians(deg)
        stone_insts.append(model("fallen_stone_%d" % i, "rock", g, c, (math.sin(a), -math.cos(a)), s_, z=-0.15, lie=True))
    models.append({"id": "ring_stones", "kind": "stones", "pos": [0, 0], "z": 0, "godot_rot_y_deg": 0, "size_m": {"w_local_x": 1, "d_local_z": 1, "h": 1}, "instances": stone_insts, "glb": None})
    # -- crags along the beach and cliff top (kit crag, uniform)
    crag_insts = []
    gcr = "data/bv2f/models/crag.glb"
    for i, (p, ht) in enumerate(CRAGS):
        c = uv(p)
        s_ = ht / ab(gcr)[1]
        crag_insts.append(model("crag_%d" % i, "rock", gcr, c, unit(math.sin(i * 1.7), -1.0), s_, z=hz_min(c, 1.5) - 0.4))
    models.append({"id": "crags", "kind": "outcrop", "pos": [0, 0], "z": 0, "godot_rot_y_deg": 0, "size_m": {"w_local_x": 1, "d_local_z": 1, "h": 1}, "instances": crag_insts, "glb": None})
    # -- the S cliff: modular cliff faces along the lip (kit cliffplain, uniform, rotation only), out of the cave and stair
    cliff_insts = []
    gcl = "data/bv2f/models/cliffplain.glb"
    s_cl = 8.2 / ab(gcl)[1]
    acc = 0.0
    seglen = [math.dist(a, b) for a, b in zip(lip[:-1], lip[1:])]
    total = sum(seglen)
    stair_top = uv(STAIR["top_px"])
    t = 3.0
    k = 0
    while t < total - 2.0:
        rem, i = t, 0
        while rem > seglen[i]:
            rem -= seglen[i]
            i += 1
        a, b = lip[i], lip[i + 1]
        d_ = unit(b[0] - a[0], b[1] - a[1])
        p = (a[0] + d_[0] * rem, a[1] + d_[1] * rem)
        out = (d_[1], -d_[0])                                        # seaward (S)
        if out[1] > 0:
            out = (-out[0], -out[1])
        skip = math.dist(p, cave_c) < 4.5 or math.dist(p, stair_top) < 4.0 or math.dist(p, foot) < 3.0
        if not skip:
            cdep = ab(gcl)[2] * s_cl
            cc = (p[0] + out[0] * (cdep / 2 + 0.3), p[1] + out[1] * (cdep / 2 + 0.3))
            cliff_insts.append(model("cliff_%d" % k, "rock", gcl, cc, out, s_cl * (0.9 + 0.2 * ((k * 37) % 10) / 10), z=SEA_Z - 1.6))
            k += 1
        t += ab(gcl)[0] * s_cl * 0.85
    models.append({"id": "cliff_faces", "kind": "cliff", "pos": [0, 0], "z": 0, "godot_rot_y_deg": 0, "size_m": {"w_local_x": 1, "d_local_z": 1, "h": 1}, "instances": cliff_insts, "glb": None})
    # -- the sea cave: its dark mouth on the cliff face under the lip
    lipn = min(lip, key=lambda q: math.dist(q, cave_c))
    openings.append({"id": "sea_cave_mouth", "point": "SW", "model": "cliff", "centre_sim": [round(cave_c[0], 4), round(-(cave_c[1] + 0.3), 4)], "z0": SEA_Z + 0.4,
                     "w": CAVE["w_m"], "h": CAVE["h_m"], "faces_deg": 180.0, "curtain_inset_m": -0.1, "dark": True})
    # -- the straight open-sided stair: from the sea-level ledge up the face to the clifftop (procedural steps, true size)
    drop = 0.0 - (SEA_Z + 0.4)
    n_st = int(round(drop / STAIR["rise"]))
    run = n_st * STAIR["tread"]
    sd = unit(stair_top[0] - foot[0], stair_top[1] - foot[1])
    st_top = stair_top
    st_foot = (st_top[0] - sd[0] * run, st_top[1] - sd[1] * run)
    steps = []
    for i in range(n_st):
        c = (st_foot[0] + sd[0] * STAIR["tread"] * (i + 0.5), st_foot[1] + sd[1] * STAIR["tread"] * (i + 0.5))
        steps.append({"c_sim": [round(c[0], 4), round(-c[1], 4)], "z_top": round(SEA_Z + 0.4 + STAIR["rise"] * (i + 1), 4),
                      "w": STAIR["width_m"], "tread": STAIR["tread"], "yaw_deg": round(yaw_of(sd), 3)})
    # -- the palisade (procedural posts at true size) and the yard logs
    post_insts = []
    k_post = 0
    for run_ in PALISADE:
        pts = [uv(p) for p in run_]
        for a, b in zip(pts[:-1], pts[1:]):
            L = math.dist(a, b)
            n_ = max(1, int(L / 0.45))
            for j in range(n_):
                f = (j + 0.5) / n_
                c = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
                k_post += 1
                if k_post % 9 in (4, 5):
                    continue                                           # burnt-through gaps
                ht = 2.4 + 0.7 * ((len(post_insts) * 13) % 10) / 10
                z0 = hz(c) - 0.3
                lean = (0.12 * math.sin(len(post_insts)), 0.12 * math.cos(len(post_insts) * 1.3))
                post_insts.append({"type": "beam", "a": [round(c[0], 3), round(-c[1], 3), round(z0, 3)],
                                   "b": [round(c[0] + lean[0], 3), round(-(c[1] + lean[1]), 3), round(z0 + ht, 3)], "thickness_m": 0.22, "procedural": "post", "glb": None})
    models.append({"id": "palisade", "kind": "palisade", "pos": [0, 0], "z": 0, "godot_rot_y_deg": 0, "size_m": {"w_local_x": 1, "d_local_z": 1, "h": 1}, "instances": post_insts, "glb": None})
    log_insts = []
    for (pa_, pb_) in LOGS:
        a, b = uv(pa_), uv(pb_)
        log_insts.append({"type": "beam", "a": [round(a[0], 3), round(-a[1], 3), round(hz(a) + 0.17, 3)], "b": [round(b[0], 3), round(-b[1], 3), round(hz(b) + 0.17, 3)],
                          "thickness_m": 0.34, "procedural": "log", "glb": None})
    models.append({"id": "logs", "kind": "debris", "pos": [0, 0], "z": 0, "godot_rot_y_deg": 0, "size_m": {"w_local_x": 1, "d_local_z": 1, "h": 1}, "instances": log_insts, "glb": None})
    # -- floes on the sea (shore ice class), as blobs
    for i, p in enumerate(FLOES):
        c = uv(p, SEA_Z)
        r = 1.2 + 0.9 * ((i * 7) % 5) / 5
        blobs.append({"k": "floe", "c": [round(c[0], 3), round(-c[1], 3)], "cz": SEA_Z - 0.1, "r": [r, r * 0.8, 0.35], "rot": (i * 37) % 180, "rgb": [0.85, 0.9, 0.95], "proto": "slab", "top": SEA_Z + 0.25})
    # -- the mere (an opening of its own: the ice)
    mere_uv = [uv(p) for p in MERE]
    openings.append({"id": "mere_ice", "point": "NW", "model": "mere", "centre_sim": [round(float(np.mean([q[0] for q in mere_uv])), 4), round(-float(np.mean([q[1] for q in mere_uv])), 4)],
                     "z0": 0.0, "w": None, "h": None, "faces_deg": None, "dark": False,
                     "probe": {"type": "poly", "polygon": [[round(q[0], 3), round(-q[1], 3)] for q in mere_uv], "z": 0.03,
                               "frontal_m2": round(0.5 * abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(mere_uv, mere_uv[1:] + mere_uv[:1]))), 3)}})
    for o in openings:
        if o.get("w") and "probe" not in o:
            o["probe"] = {"type": "v", "centre": o["centre_sim"], "faces_deg": o["faces_deg"], "w": o["w"], "h": o["h"], "z0": o["z0"], "frontal_m2": round(o["w"] * o["h"], 3)}

    # ---------------- the window, sections, bounds, knight ----------------
    GUIDE = (1280 * 4 + 1536, 768 * 4 + 1024)                     # 5 x 5 canvases: 6656 x 4096
    sk_c = uv((768, 512))
    win_c = (round(sk_c[0], 3), round(sk_c[1], 3))
    half = (GUIDE[0] / 2 / PPM, GUIDE[1] / 2 / PX_V)
    wu = [win_c[0] - half[0], win_c[0] + half[0]]
    wv = [win_c[1] - half[1], win_c[1] + half[1]]
    PAD = 64
    sx, sy = 2, 2
    sw_, sh_ = GUIDE[0] // sx, GUIDE[1] // sy
    sections = []
    for j in range(sy):
        for i in range(sx):
            cx, cy = sw_ * (i + 0.5), sh_ * (j + 0.5)
            c = [wu[0] + cx / PPM, wv[1] - cy / PX_V]
            sections.append({"id": f"s{j}{i}", "px_origin": [sw_ * i, sh_ * j], "px": [sw_, sh_], "centre_uv": c,
                             "u": [c[0] - (sw_ / 2 + PAD) / PPM, c[0] + (sw_ / 2 + PAD) / PPM], "v": [c[1] - (sh_ / 2 + PAD) / PX_V, c[1] + (sh_ / 2 + PAD) / PX_V]})
    for s in sections:
        json.dump({"_what": "BV2F LV Phase 1' Tier-B --frame-grid, guide section %s of the art blockout" % s["id"], "name": "barrow_v2 art " + s["id"], "variant": "art",
                   "scene": "res://scenes/bv2f_barrow_v2.tscn", "guide_px": [s["px"][0] + 2 * PAD, s["px"][1] + 2 * PAD], "pad_px": PAD, "px_per_m_across": PPM,
                   "pitch_deg": 52.95354112560294, "yaw_deg": 47.0, "walk_grid": {"u": [-1.0, 1.0], "v": [-1.0, 1.0], "step": 0.1},
                   "topdown": {"px": [2400, 2240], "px_per_m": 30.0}, "section": s["id"]}, open(os.path.join(ART, f"frame_grid_{s['id']}.json"), "w"), indent=1)
    # walkable land: the land inside the window, the coast inset 0.6 m; v1's _build_bounds walls it
    bpoly = []
    for (p, q) in zip(coast[:-1], coast[1:]):
        bpoly.append(p)
    bpoly = [p for p in coast if wu[0] - 2 <= p[0] <= wu[1] + 2]
    bpoly += [(wu[1], coast[-1][1]), (wu[1], wv[1]), (shore[0][0], wv[1])]
    tints = json.load(open(os.path.join(BF, "data", "barrow_full_layout.json")))["tints_srgb"]
    tints.update(json.load(open(os.path.join(LV, "DEV12_proposal.json")))["class_list"]["new_classes_DEV2_provisional"])
    hf = {"file": "terrain_h.f32", "shape": [H, W], "px_per_m": HF_PPM, "extent_sim_m": {"x0": u0, "x1": u1, "y0": -v1, "y1": -v0}, "sha256": sha(os.path.join(OUT, "terrain_h.f32"))}
    level = {
        "_what": "BV2F lane LV Phase 1': barrow_v2 ART blockout (sketch A, v1 practice) as a level of the v1 Barrow; read by scripts/bv2f/bv2f_level.gd; written by fid/lv/tools/make_bv2art.py",
        "tints_srgb": tints, "classes": names,
        "knight": {"spawn_uv": [0.0, 0.0], "spawn_facing": "S", "guide_uv": [0.0, 0.0], "guide_facing": "S", "gear_stack": 4},
        "frame": {"guide_window": {"centre_uv": sections[0]["centre_uv"], "u": sections[0]["u"], "v": sections[0]["v"]},
                  "envelope": {"u": wu, "v": wv, "px": list(GUIDE), "centre_uv": list(win_c)}, "sections": sections},
        "camera_clamp_default": False,
        "regions": {"ice": {"centre_uv": [round(float(np.mean([q[0] for q in mere_uv])), 3), round(float(np.mean([q[1] for q in mere_uv])), 3)], "axes_m": [20.0, 9.0]}},
        "placements": [{"id": "mound", "kind": "structure", "uv": [0.0, 60.0], "semi_axes": [1.0, 1.0], "rise_m": 0.0, "exponent": 1.0, "toe_rho": 0.2,
                        "cutting": {"half_w": 0.0, "v_facade": -999.0}, "passage": {"half_w": 0.0, "v0": 0.0, "v_end": 0.0, "risers_v": [], "riser_m": 0.0},
                        "_": "STUB for the frozen capture tool's walk-grid statistics (v1's mound spec); the art mound is terrain"}],
        "bounds": {"polygon_uv": [[round(p[0], 3), round(p[1], 3)] for p in bpoly]},
        "crucible": {"eye_height_m": 1.6, "station": {"uv": [0.0, 0.0]}, "boss_gate": {"uv": [round(bd[0], 3), round(bd[1], 3)]}, "spawns": []},
        "sim": {"heightfield": hf, "classes_png": {"file": "classes_png.bin", "px_per_m": CLS_PPM, "extent_sim_m": hf["extent_sim_m"], "sha256": sha(os.path.join(OUT, "classes_png.bin"))},
                "sea_z": SEA_Z, "models": models, "features": [], "blobs": blobs, "openings": openings, "stair_steps": steps,
                "stair": None, "skip_models": [], "glb_copies": glb_copies, "glb_missing": [],
                "model_class": {"wreck": "wood", "barrow_front": "rock", "longhall": "wood", "fallen_gable": "char", "ring_stones": "rock", "slope_stones": "rock", "crags": "rock",
                                "cliff_faces": "rock", "palisade": "wood", "logs": "wood"},
                "blob_class": {"floe": "shore_ice"}, "colliders": True,
                "_frame": "sim (x, y) = (u, -v): the Level node's local frame IS v1's (u, v) -- no site rotation (R-C9-185)"},
    }
    json.dump(level, open(os.path.join(OUT, "level.json"), "w"), indent=1)
    layout = {
        "_what": "barrow_v2 ART-FIRST layout of record (Matt R-C9-185; charter v1.0 s 15): sketch A literally, in v1's camera-aligned (u, v) frame, v1's layout practice. Built by fid/lv/tools/make_bv2art.py.",
        "frame": {"units": "metres", "u_hat_world": [0.682, 0.0, -0.7314], "v_hat_world": [-0.7314, 0.0, -0.682], "world_from_uv": "x = u*cos47 - v*sin47; z = -u*sin47 - v*cos47 (v1's own)",
                  "sketch_map": "u = (x - 780) / 24, v = (452 - y - z*24*cos(pitch)) / (24*sin(pitch)), sketch A px (x, y)"},
        "window": {"guide_px": list(GUIDE), "centre_uv": list(win_c), "u": wu, "v": wv, "chunks": {"cols": 5, "rows": 5, "canvas_px": [1536, 1024], "stride_px": [1280, 768]}},
        "tints_srgb": tints, "sea_z_m": SEA_Z,
        "regions": {"mere": [[round(q[0], 3), round(q[1], 3)] for q in mere_uv], "stream": [[round(uv(p)[0], 3), round(uv(p)[1], 3)] for p in STREAM],
                    "coast_chain": [[round(q[0], 3), round(q[1], 3)] for q in coast], "mound": {"centre_uv": [round(mc[0], 3), round(mc[1], 3)], "semi_m": list(MOUND["semi_m"]), "rise_m": MOUND["rise_m"]},
                    "shingle": [[round(uv(p)[0], 3), round(uv(p)[1], 3)] for p in SHINGLE], "hall_yard_ash": [[round(uv(p)[0], 3), round(uv(p)[1], 3)] for p in YARD],
                    "paths": [[[round(uv(p)[0], 3), round(uv(p)[1], 3)] for p in pl] for pl in PATHS], "shore_ice": "W of the shore line: beach 4 m, grounded ice shelf at -0.5 to 13 m out, one sea level -6"},
        "placements": layout_pl,
        "procedural": {"palisade_posts": len(post_insts), "logs": len(log_insts), "stair_steps": len(steps), "floes": len(blobs)},
        "openings": openings, "knight": level["knight"], "bounds": level["bounds"],
        "classes": names, "class_counts": {names[k]: int((C == k).sum()) for k in range(len(names)) if (C == k).any()},
    }
    json.dump(layout, open(os.path.join(ART, "layout_bv2art.json"), "w"), indent=1)
    print("[art] window %.1f x %.1f m (%dx%d px); %d heroes+instances; %d posts; %d steps; openings %s" % (
        wu[1] - wu[0], wv[1] - wv[0], GUIDE[0], GUIDE[1], len(layout_pl), len(post_insts), len(steps), [o["id"] for o in openings]))


if __name__ == "__main__":
    main()
