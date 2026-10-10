#!/usr/bin/env python3
"""BV2F LV, R-C9-384 (BV2F-N1): the site_ph4 LEVEL = the pinned site_ph3 level (LV 9263d053d) + a NORTH BAND.

    python3 fid/lv/tools/ph4_level.py            # writes barrow_full/godot/data/bv2f/site_ph4/level/ + fid/lv/ph4/

Frame: UNCHANGED world. The plate grows north by BAND_PX = 768 rows (exactly one grid stride), so the ph4 plate is
6656 x 4864 and its top edge is v1' = v1 + 768 / (ppm * sin pitch). A ground point keeps its (u, v); its plate pixel moves
down by exactly 768 rows. u0, ppm, pitch, yaw unchanged.

Terrain/classes: only cells whose EVERY drawable point projects ABOVE the ph3 plate's top edge (ph3 plate y < -GUARD_PX)
may change, so nothing the ph3 painting shows can move (proof: fid/lv/ph4/ph4_level_report.json `guard`, and the
ph3-window rows of the band render vs the pinned d26d14c55 guide).
"""
import hashlib
import json
import math
import os
import shutil
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
FID = os.path.dirname(LV)
C9 = os.path.normpath(os.path.join(FID, "..", ".."))
D3 = os.path.join(C9, "barrow_full/godot/data/bv2f/site_ph3/level")
D4 = os.path.join(C9, "barrow_full/godot/data/bv2f/site_ph4/level")
OUT = os.path.join(LV, "ph4")

PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
SV, CZ = PPM * math.sin(PITCH), PPM * math.cos(PITCH)      # px per ground metre up-screen / per metre of height
U0, V1 = -33.57573954303182, 22.36993715728635            # ph3 plate top-left (bv2f_pilot.gd PILOT_U0 / PILOT_V1)
W, H3 = 6656, 4096
BAND_PX = 768
V1N = V1 + BAND_PX / SV                                    # ph4 plate top edge
H4 = H3 + BAND_PX
PAD = 64
SEC_H = BAND_PX + 256                                      # band + 256 ph3 rows (the overlap the proof compares)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def section(sid, x0, y0, sw, sh):
    u0 = U0 + (x0 - PAD) / PPM
    u1 = U0 + (x0 + sw + PAD) / PPM
    vt = V1N - (y0 - PAD) / SV
    vb = V1N - (y0 + sh + PAD) / SV
    return {"id": sid, "px_origin": [x0, y0], "px": [sw, sh], "centre_uv": [(u0 + u1) / 2, (vt + vb) / 2],
            "u": [u0, u1], "v": [vb, vt], "_": "R-C9-384 north band section (ph4 plate px, pad %d)" % PAD}


def frame_grid(sid, sw, sh):
    return {"_what": "BV2F LV Tier-B --frame-grid, ph4 NORTH BAND section %s (R-C9-384)" % sid,
            "name": "barrow_v2 site_ph4 %s" % sid, "variant": "site_ph4/level", "scene": "res://scenes/bv2f_barrow_v2.tscn",
            "guide_px": [sw + 2 * PAD, sh + 2 * PAD], "pad_px": PAD, "px_per_m_across": PPM,
            "pitch_deg": 52.95354112560294, "yaw_deg": 47.0,
            "walk_grid": {"u": [-1.0, 1.0], "v": [-1.0, 1.0], "step": 0.1},
            "topdown": {"px": [2400, 2240], "px_per_m": 30.0}, "section": sid}


GUARD_PX = 32          # an edited cell must project at least this far ABOVE the ph3 plate's top edge, before and after
HF_PPM, CL_PPM = 8, 16
X0, Y0 = -42.0, -36.0  # heightfield / class raster extent origin (sim x = u, sim y = -v)
MOUND_C, MOUND_AB = (2.0, 27.98), (17.0, 10.4)               # make_bv2art MOUND (sketch px (828,-84) -> uv)
RIVER_N = [(-28.6, 27.0), (-28.85, 28.6), (-28.5, 30.4), (-28.95, 32.3), (-28.7, 34.2), (-28.9, 36.2)]
RIVER_HW, RIVER_DEP = 0.5, 0.3                               # make_bv2art CHANNELS river: hw 0.5, dep 0.3
STONE = {"mid": ("data/bv2f/ext/runs__C-9__barrow_full__web_painted__models__barrow__stone_mid.glb.bin", (0.42493, 0.59453), 0.99904),
         "tall": ("data/bv2f/ext/runs__C-9__barrow_full__web_painted__models__barrow__stone_tall.glb.bin", (0.38321, 0.53953), 0.998532)}


def y3_of(v, z):
    """the ph3 plate row of a point (u, v, z) (negative = above the ph3 top edge)"""
    return (V1 - v) * SV - z * CZ


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def seg_dist(P, pts):
    """distance from points P (..., 2) to a polyline"""
    d = np.full(P.shape[:-1], np.inf)
    for a, b in zip(pts[:-1], pts[1:]):
        a, b = np.array(a), np.array(b)
        ab = b - a
        t = np.clip(((P - a) @ ab) / (ab @ ab), 0, 1)
        d = np.minimum(d, np.linalg.norm(P - (a + t[..., None] * ab), axis=-1))
    return d


def edit_ground(D, lvl, rep):
    """the NORTH BAND terrain + classes. Returns the edited arrays; every edited cell is guarded (GUARD_PX)."""
    from scipy import ndimage
    hf = lvl["sim"]["heightfield"]
    R, Cn = hf["shape"]
    H0 = np.fromfile(os.path.join(D3, hf["file"]), np.float32).reshape(R, Cn).astype(np.float64)
    W0 = np.fromfile(os.path.join(D3, hf["walk_file"]), np.float32).reshape(R, Cn).astype(np.float64)
    CL0 = np.asarray(Image.open(os.path.join(D3, "classes.png")))
    classes = lvl["classes"]
    ci = classes.index
    # cell centres (u, v)
    hv = Y0 * -1 - np.arange(R) / HF_PPM            # row r -> sim y = -36 + r/8 -> v = 36 - r/8
    hu = X0 + np.arange(Cn) / HF_PPM
    UU, VV = np.meshgrid(hu, hv)
    H = H0.copy()
    # (1) SMOOTH the band zone (the generator's 25 cm steps read as banding in the north): gaussian 0.45 m, faded in
    #     from v1 + 1.0 to v1 + 2.0 so nothing near the ph3 edge moves
    w_s = smoothstep(V1 + 1.0, V1 + 2.0, VV)
    H = H * (1 - w_s) + ndimage.gaussian_filter(H0, 0.45 * HF_PPM) * w_s
    # (2) the BEACH continues north over the sea floor (none / -6.5 at u < -31, v > 32.5): rows north of v 30.5 take the
    #     beach profile of row v 30.5, shifted in u by a slow wobble so no edge runs straight; faded in over 1 m
    r_src = int(round((36 - 30.5) * HF_PPM))
    wob = lambda v: 0.55 * np.sin(v * 0.9) + 0.3 * np.sin(v * 2.1 + 1.0)
    src_h = np.interp(UU + wob(VV), hu, H[r_src])
    w_b = smoothstep(30.5, 31.5, VV) * (1 - smoothstep(-30.4, -29.6, UU))
    H = H * (1 - w_b) + src_h * w_b
    # (3) the RIVER runs on north past the band top: the channel (dep 0.3 under its banks, hw 0.5 widening slightly
    #     with a noisy edge), from the old head at (-28.6, 27.0)
    P = np.stack([UU, VV], -1)
    dr = seg_dist(P, RIVER_N)
    hw = RIVER_HW * (1 + 0.18 * np.sin(VV * 3.1) + 0.12 * np.sin(VV * 7.3 + 2))
    bank = ndimage.gaussian_filter(H, 0.6 * HF_PPM)
    carve = (1 - smoothstep(hw, hw + 0.45, dr)) * (VV > 26.6)
    H = H * (1 - carve) + (bank - RIVER_DEP) * carve
    # (4) the barrow front's BACK is under the mound by design (R-C9-234 (6)) but its rear 4.5 m pokes 0.4-1.14 m through
    #     the dome's crest (v 22.5-27.1). The mound rises over its chamber: a smooth hump sized from the model's own
    #     vertices (PT's export, world -> uv) so every rear vertex is >= 0.30 m under the new ground
    import math
    Vx = np.fromfile(os.path.join(FID, "pt/site/root/work/meshes/barrow_front_V.f32"), np.float32).reshape(-1, 3).astype(np.float64)
    a = math.radians(47.0)
    mu = Vx @ np.array([math.cos(a), 0, -math.sin(a)])
    mv = Vx @ np.array([-math.sin(a), 0, -math.cos(a)])
    mh = Vx[:, 1]
    back = mv > 21.8
    need = np.zeros_like(H)
    rr = np.clip(np.round((36 - mv[back]) * HF_PPM).astype(int), 0, R - 1)
    cc = np.clip(np.round((mu[back] - X0) * HF_PPM).astype(int), 0, Cn - 1)
    np.maximum.at(need, (rr, cc), mh[back] + 0.30)
    lift = np.where(need > 0, np.maximum(need - H, 0), 0.0)            # only cells that hold a protruding rear vertex
    fade = smoothstep(21.0, 21.8, VV)                                   # the facade (v ~17.6) and portal never move
    base = ndimage.gaussian_filter(ndimage.grey_dilation(lift, size=(5, 5)), 1.2 * HF_PPM) * fade
    sel = lift > 0
    k = float((lift[sel] / np.maximum(base[sel], 1e-9)).max()) if sel.any() else 0.0
    hump = k * base
    H = H + hump
    rep["hump"] = {"max_m": round(float(hump.max()), 3), "scale_k": round(k, 3),
                   "rear_vertices": int(back.sum())}
    # every edit is weighted by A: 1 where the cell (and 3 cells round it) projects >= GUARD_PX + 40 above the ph3 top
    # both before and after, falling smoothly to 0 well before the guard
    ok = (y3_of(VV, H0) < -GUARD_PX - 40) & (y3_of(VV, H) < -GUARD_PX - 40)
    ok = ndimage.binary_erosion(ok, np.ones((7, 7), bool))
    A = np.clip(ndimage.gaussian_filter(ok.astype(np.float64), 1.5), 0, 1) * ok
    H = H0 + (H - H0) * A
    rem = need - H
    rep["hump"]["rear_vertex_cells_still_above_ground_m"] = round(float(rem[need > 0].max()), 3)
    # GUARD: every changed cell projects above the ph3 top edge, before and after (+ its 8 neighbours, which share
    # triangles with it)
    ch = np.abs(H - H0) > 1e-6
    chn = ndimage.binary_dilation(ch, np.ones((3, 3), bool))
    y_old, y_new = y3_of(VV, H0), y3_of(VV, H)
    bad = chn & ((y_old > -GUARD_PX) | (y_new > -GUARD_PX))
    rep["terrain"] = {"cells_changed": int(ch.sum()), "guard_px": GUARD_PX, "cells_violating_guard": int(bad.sum()),
                      "max_abs_change_m": round(float(np.abs(H - H0).max()), 3),
                      "max_y3_of_changed_and_neighbours": round(float(np.maximum(y_old, y_new)[chn].max()), 1)}
    assert not bad.any(), "a terrain edit reaches the ph3 plate"
    Wk = W0.copy()
    same = np.abs(W0 - H0) < 1e-4                                       # the walk file follows the terrain where it did
    Wk[same & ch] = H[same & ch]
    # CLASSES (16 px/m): the beach's classes follow (2); the river channel = lead (the river's own class south of 27);
    # the sea floor's `none`/`sea` north of the beach become shore_ice
    cv = 36 - np.arange(CL0.shape[0]) / CL_PPM
    cu = X0 + np.arange(CL0.shape[1]) / CL_PPM
    CU, CV = np.meshgrid(cu, cv)
    CL = CL0.copy()
    rc_src = int(round((36 - 30.5) * CL_PPM))
    src_c = CL0[rc_src][np.clip(np.round((CU + wob(CV) - X0) * CL_PPM).astype(int), 0, CL0.shape[1] - 1)]
    rng = np.random.RandomState(3841)
    nb = ndimage.gaussian_filter(rng.rand(*CL.shape), 6)
    wb_c = (smoothstep(30.5, 31.5, CV) * (1 - smoothstep(-30.4, -29.6, CU)))
    take = wb_c > (0.35 + 1.2 * (nb - nb.mean()))                      # a noisy (not straight) blend line
    CL[take] = src_c[take]
    CL[(CV > 31.0) & (CU < -30.0) & np.isin(CL, [ci("none"), ci("sea")])] = ci("shore_ice")
    drc = seg_dist(np.stack([CU, CV], -1), RIVER_N)
    hwc = RIVER_HW * (1 + 0.18 * np.sin(CV * 3.1) + 0.12 * np.sin(CV * 7.3 + 2))
    CL[(drc < hwc + 0.08) & (CV > 26.6)] = ci("lead")
    # a few reed clumps on the river's banks (the river south of 27 has bank reeds)
    for (bu, bv, r_) in [(-29.7, 29.3, 0.7), (-27.7, 31.4, 0.6), (-29.9, 33.6, 0.65)]:
        m = ((CU - bu) ** 2 + ((CV - bv) / 0.7) ** 2 < r_ ** 2) & (drc > hwc + 0.1) & (CL == ci("snow"))
        CL[m] = ci("reed")
    chc = CL != CL0
    # class cells: the ground under them (terrain at that point) must project above the guard
    Hc = ndimage.map_coordinates(H, [(36 - CV) * HF_PPM, (CU - X0) * HF_PPM], order=1)
    H0c = ndimage.map_coordinates(H0, [(36 - CV) * HF_PPM, (CU - X0) * HF_PPM], order=1)
    badc = chc & ((y3_of(CV, Hc) > -GUARD_PX) | (y3_of(CV, H0c) > -GUARD_PX))
    rep["classes"] = {"cells_changed": int(chc.sum()), "cells_violating_guard": int(badc.sum()),
                      "changed_by_class": {classes[int(k_)]: int(n) for k_, n in zip(*np.unique(CL[chc], return_counts=True))}}
    assert not badc.any(), "a class edit reaches the ph3 plate"
    return H.astype(np.float32), Wk.astype(np.float32), CL, H


def add_stones(lvl, H, rep):
    """the kerb continues round the dome's east side (one stone, the next on make_bv2art's 3.2 m arc step), and a few
    weathered stones in the snowfield north -- appended to slope_stones (existing instance order untouched)"""
    from scipy import ndimage
    import math
    a_k, b_k = MOUND_AB[0] * 1.03, MOUND_AB[1] * 1.03

    def hz_min(c, r):
        us = np.linspace(c[0] - r, c[0] + r, 9)
        vs = np.linspace(c[1] - r, c[1] + r, 9)
        U_, V_ = np.meshgrid(us, vs)
        z = ndimage.map_coordinates(H, [(36 - V_) * HF_PPM, (U_ - X0) * HF_PPM], order=1)
        return float(z[(U_ - c[0]) ** 2 + (V_ - c[1]) ** 2 <= r * r].min())
    # last existing east kerb stone sits at theta -7.3 deg; make_bv2art steps 3.2 m of arc
    th = math.radians(-7.3)
    step = 3.2 / math.hypot(a_k * math.sin(th), b_k * math.cos(th))
    th += step
    kc = (MOUND_C[0] + a_k * math.cos(th), MOUND_C[1] + b_k * math.sin(th))
    new = [("kerb", kc, "tall", 1.9, math.degrees(math.atan2(-(math.sin(th) / b_k), math.cos(th) / a_k)) + 90),
           ("field", (24.4, 30.4), "mid", 1.1, 37.0), ("field", (29.6, 27.9), "mid", 0.9, -61.0),
           ("field", (-20.6, 30.2), "mid", 1.0, 12.0)]
    grp = [m for m in lvl["sim"]["models"] if m["id"] == "slope_stones"][0]
    n0 = len(grp["instances"])
    out = []
    for kind, c, sk, ht, rot in new:
        glb, (fw, fd), fs = STONE[sk]
        z = hz_min(c, 0.4) - 0.1
        y3_top = y3_of(c[1], z + ht)
        y3_base = y3_of(c[1], z)
        assert y3_base < -GUARD_PX, "a new stone reaches the ph3 plate"
        grp["instances"].append({"type": "box", "pos": [round(c[0], 4), round(-c[1], 4)], "z": round(z, 3),
                                 "godot_rot_y_deg": round(rot, 3), "size_m": [round(fw * ht, 4), round(fd * ht, 4), ht],
                                 "glb": glb, "uniform_scale": round(fs * ht, 5),
                                 "note": "R-C9-384 ph4 north band: " + ("the kerb continues round the dome's east side" if kind == "kerb" else "a weathered stone in the north snowfield")})
        out.append({"kind": kind, "uv": [round(c[0], 3), round(c[1], 3)], "z": round(z, 3), "h": ht,
                    "ph3_y_base": round(y3_base, 1), "ph3_y_top": round(y3_top, 1), "ph4_y_base": round(y3_base + BAND_PX, 1)})
    rep["stones"] = {"appended_to": "slope_stones", "existing_instances": n0, "new": out}


def main():
    os.makedirs(D4, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    pin3 = json.load(open(os.path.join(D3, "PIN.json")))
    lvl = json.load(open(os.path.join(D3, "level.json")))
    assert sha(os.path.join(D3, "level.json")) == pin3["files"]["level.json"]["sha256"], "ph3 level.json is not the pinned one"
    # every other ph3 file: byte copy (terrain edits, if any, are applied below and recorded)
    for f in sorted(os.listdir(D3)):
        if f in ("level.json", "PIN.json"):
            continue
        shutil.copyfile(os.path.join(D3, f), os.path.join(D4, f))
    rep = {"ruling": "R-C9-384"}
    if os.environ.get("PH4_FRAME_ONLY") != "1":
        Hn, Wn, CLn, Hd = edit_ground(D4, lvl, rep)
        hf = lvl["sim"]["heightfield"]
        Hn.tofile(os.path.join(D4, hf["file"]))
        Wn.tofile(os.path.join(D4, hf["walk_file"]))
        Image.fromarray(CLn).save(os.path.join(D4, "classes.png"))
        shutil.copyfile(os.path.join(D4, "classes.png"), os.path.join(D4, lvl["sim"]["classes_png"]["file"]))
        hf["sha256"] = sha(os.path.join(D4, hf["file"]))
        lvl["sim"]["classes_png"]["sha256"] = sha(os.path.join(D4, lvl["sim"]["classes_png"]["file"]))
        add_stones(lvl, Hd, rep)
    fr = lvl["frame"]
    env = fr["envelope"]
    assert abs(env["v"][1] - V1) < 1e-9 and abs(env["u"][0] - U0) < 1e-9 and env["px"] == [W, H3]
    fr["envelope_ph3"] = json.loads(json.dumps(env))
    env["v"] = [env["v"][0], V1N]
    env["px"] = [W, H4]
    env["centre_uv"] = [env["centre_uv"][0], (env["v"][0] + env["v"][1]) / 2]
    env["_r_c9_384"] = "ph4: the ph3 envelope + a %d px north band (v1' = v1 + %d / (ppm sin pitch)); world unchanged" % (BAND_PX, BAND_PX)
    half = W // 2
    fr["sections"] = [s for s in fr["sections"] if not str(s["id"]).startswith("n")] + [
        section("n0", 0, 0, half, SEC_H), section("n1", half, 0, half, SEC_H)]
    for s in fr["sections"]:
        if s["id"] in ("n0", "n1"):
            json.dump(frame_grid(s["id"], s["px"][0], s["px"][1]), open(os.path.join(OUT, "frame_grid_%s.json" % s["id"]), "w"), indent=1)
    lvl["_ph4"] = {"ruling": "R-C9-384", "base": "site_ph3/level (LV 9263d053d, PIN.json)", "band_px": BAND_PX,
                   "v1_ph3": V1, "v1_ph4": V1N, "plate_px": [W, H4]}
    json.dump(lvl, open(os.path.join(D4, "level.json"), "w"), indent=1)
    pin = {"_what": "R-C9-384: site_ph4 level = site_ph3 level (pinned LV 9263d053d) + north band frame (fid/lv/tools/ph4_level.py)",
           "base_pin": "site_ph3/level/PIN.json", "files": {f: {"sha256": sha(os.path.join(D4, f))} for f in sorted(os.listdir(D4)) if f != "PIN.json"}}
    json.dump(pin, open(os.path.join(D4, "PIN.json"), "w"), indent=1)
    rep["frame"] = {"v1_ph3": V1, "v1_ph4": V1N, "band_px": BAND_PX, "plate_ph4": [W, H4], "u0": U0, "ppm": PPM}
    rep["level_json_sha256"] = pin["files"]["level.json"]["sha256"]
    json.dump(rep, open(os.path.join(OUT, "ph4_level_report.json"), "w"), indent=1)
    print("site_ph4 level: v1' %.6f, plate %d x %d" % (V1N, W, H4))
    print(json.dumps({k: v for k, v in rep.items() if k != "frame"}, indent=1))


if __name__ == "__main__":
    main()
