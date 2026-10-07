#!/usr/bin/env python3
"""BV2F lane LV, Phase 1.3: prepare the barrow_v2 level of v1's engine from layout v7b.

    python3 fid/lv/tools/bv2f_level_prep.py [layout]      (default fid/lv/layout_v7b.json)

Writes (allowlisted new paths only, barrow_full/godot/data/bv2f/):
  level.json        what scripts/bv2f/bv2f_level.gd reads: v1-shaped keys the frozen capture tools touch
                    (tints_srgb, knight, frame.guide_window, regions, placements[mound], bounds, crucible) +
                    the v7b content in the SIM frame (models, stair, features, blobs, sea, class raster, heightfield)
  classes.png       the ground CLASS raster, 8 px/m over the heightfield's extent, R = class index (lossless PNG)
  terrain_h.f32     copy of layout v7b's heightfield
and fid/lv/v7b/frame_grid_*.json, the Tier-B --frame-grid configs (guide sections, walk grid, map).

FRAME. v1's Level node carries (u, v) with local (u, h, -v); its local axes ARE sim (x, z, y) under the frame fix
(world = R_y(+47).(x, z, y), fid/lv/frame.py): u = x, v = -y. Every v1-shaped key below is in (u, v).

TINTS. v1's own values for the classes v1 had (barrow_full_layout.json tints_srgb, read by barrow_full.gd:146-148);
DEV-2 provisional tints for the new ones (fid/lv/DEV12_proposal.json; R-C9-174: cliffs and crags take v1 `rock`).
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
BV2 = os.path.normpath(os.path.join(LV, "..", ".."))
C9 = os.path.dirname(BV2)
BF = os.path.join(C9, "barrow_full", "godot")
OUT = os.path.join(BF, "data", "bv2f")
sys.path.insert(0, os.path.join(BV2, "tools"))
import bv2_geom as G  # noqa: E402

PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
PX_V = PPM * math.sin(PITCH)                       # 80.3076 px per ground metre of v
CLS_PPM = 16.0
CLASSES = ["none", "snow", "path", "ice", "shrub", "rock", "mound", "shingle", "shore_ice", "stream", "char", "sea", "wood", "passage_dark", "ash"]
V1_TINTS = json.load(open(os.path.join(BF, "data", "barrow_full_layout.json")))["tints_srgb"]
NEW_TINTS = json.load(open(os.path.join(LV, "DEV12_proposal.json")))["class_list"]["new_classes_DEV2_provisional"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def uv(p):
    return [round(float(p[0]), 4), round(-float(p[1]), 4)]


def main():
    global OUT
    lp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(LV, "layout_v7b.json")
    VAR = "v7c" if "v7c" in os.path.basename(lp) else "v7b"          # BV2F-LV R-C9-177: one data dir per variant
    OUT = os.path.join(BF, "data", "bv2f", VAR)
    L = json.load(open(lp))
    os.makedirs(OUT, exist_ok=True)
    tints = dict(V1_TINTS)
    tints.update(NEW_TINTS)
    # ash: the burnt hall's YARD (trampled ash, soot-grey snow) takes layout v6's own zone colour (layout_v2.json zones
    # hall_yard_ash rgb), not the charred-timber `char` -- a ground of char tint read as a black void at the play camera
    tints["ash"] = L["zones"]["classes"]["hall_yard_ash"]["rgb"]
    # ---------------- the class raster (sim frame), priority low -> high ----------------
    hf = L["sculpt"]["heightfield"]
    ex = hf["extent_sim_m"]
    Hh = np.fromfile(os.path.join(BV2, hf["file"]), dtype="<f4").reshape(hf["shape"])
    W = int(round((ex["x1"] - ex["x0"]) * CLS_PPM))
    Hn = int(round((ex["y1"] - ex["y0"]) * CLS_PPM))
    xs = ex["x0"] + (np.arange(W) + 0.5) / CLS_PPM
    ys = ex["y0"] + (np.arange(Hn) + 0.5) / CLS_PPM
    X, Y = np.meshgrid(xs, ys)
    # bilinear heights at the class cells
    fi = (X - ex["x0"]) * hf["px_per_m"]
    fj = (Y - ex["y0"]) * hf["px_per_m"]
    i0 = np.clip(np.floor(fi).astype(int), 0, Hh.shape[1] - 2)
    j0 = np.clip(np.floor(fj).astype(int), 0, Hh.shape[0] - 2)
    ti, tj = fi - i0, fj - j0
    Z = (Hh[j0, i0] * (1 - ti) * (1 - tj) + Hh[j0, i0 + 1] * ti * (1 - tj) + Hh[j0 + 1, i0] * (1 - ti) * tj + Hh[j0 + 1, i0 + 1] * ti * tj)
    gy, gx = np.gradient(Z, 1.0 / CLS_PPM)
    slope = np.degrees(np.arctan(np.hypot(gx, gy)))
    C = np.full((Hn, W), CLASSES.index("snow"), np.uint8)
    sea_z = float(L["sea"]["z_m"])
    # rock = the CLIFF faces (steep AND below the floor's level: the sea cliffs and the stair cut), opened so the barrow
    # slope's sculpt noise does not speckle; above the floor the slopes stay their biome
    from scipy import ndimage as _nd
    _rk = _nd.binary_opening((slope > 40.0) & (Z < -0.3), iterations=2)
    C[_rk] = CLASSES.index("rock")

    def poly_mask(poly):
        img = Image.new("L", (W, Hn), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(img).polygon([((p[0] - ex["x0"]) * CLS_PPM, (p[1] - ex["y0"]) * CLS_PPM) for p in poly], fill=1)
        return np.asarray(img).astype(bool)

    def line_mask(pl, w):
        img = Image.new("L", (W, Hn), 0)
        from PIL import ImageDraw
        d = ImageDraw.Draw(img)
        pts = [((p[0] - ex["x0"]) * CLS_PPM, (p[1] - ex["y0"]) * CLS_PPM) for p in pl]
        d.line(pts, fill=1, width=max(1, int(round(w * CLS_PPM))), joint="curve")
        r = w * CLS_PPM / 2
        for q in pts:
            d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=1)
        return np.asarray(img).astype(bool)

    floor = poly_mask(L["floor"]["polygon"])
    # the seeded biomes on the floor (and a 4 m skirt outside it): nearest seed
    zmap = {"grave_ground": "shrub", "shore_shingle": "shingle", "cliff_top_rock": "rock", "hall_yard_ash": "ash", "snow_field": "snow"}
    seeds = [(zmap[k], s) for k, v in L["zones"]["classes"].items() if "seeds" in v for s in v["seeds"]]
    dbest = np.full((Hn, W), 1e9)
    zc = np.full((Hn, W), CLASSES.index("snow"), np.uint8)
    # the seams wander (layout v6 blends its biomes over blend_m = 3 m; a class map has no blend, so the seam is
    # DOMAIN-WARPED by up to ~blend_m instead of drawn as a straight Voronoi line)
    rng = np.random.default_rng(7)
    def _noise(scale_m, amp):
        g = rng.normal(0, 1, (int(Hn / CLS_PPM / scale_m) + 3, int(W / CLS_PPM / scale_m) + 3))
        from scipy.ndimage import zoom as _zoom
        z = _zoom(g, (Hn / (g.shape[0] - 2), W / (g.shape[1] - 2)), order=3)[:Hn, :W]
        return amp * z / (np.abs(z).max() + 1e-9)
    WX = X + _noise(9.0, 3.0) + _noise(3.0, 1.0)
    WY = Y + _noise(9.0, 3.0) + _noise(3.0, 1.0)
    for cname, s in seeds:
        d = np.hypot(WX - s[0], WY - s[1])
        m = d < dbest
        dbest[m] = d[m]
        zc[m] = CLASSES.index(cname)
    skirt = np.zeros_like(floor)
    from scipy import ndimage
    skirt = ndimage.binary_dilation(floor, iterations=int(4 * CLS_PPM)) & (slope <= 38.0)
    C[skirt] = zc[skirt]
    for f in L["features"]:
        if f["kind"] == "mound":
            m = poly_mask(f["footprint"]) & ~floor & (slope <= 38.0)
            C[m] = CLASSES.index("mound")
    C[poly_mask(L["shore_ice"]["polygon"]) & ~floor & (Z > sea_z + 0.15)] = CLASSES.index("shore_ice")
    for ln in L["lanes"]:
        C[poly_mask(ln["polygon"]) & (slope <= 38.0)] = CLASSES.index("path")
    C[line_mask(L["path"]["polyline"], L["path"]["width_m"]) & floor] = CLASSES.index("path")
    C[line_mask(L["stream"]["polyline"], L["stream"]["width_m"])] = CLASSES.index("stream")
    C[poly_mask(L["mere"]["polygon"])] = CLASSES.index("ice")
    for f in L["features"]:
        if f["kind"] in ("forecourt", "apron"):
            C[poly_mask(f["footprint"])] = CLASSES.index("path")
    C[(Z <= sea_z + 0.15) & ~floor] = CLASSES.index("none")          # under the sea plane: no ground mesh
    Image.fromarray(C, "L").save(os.path.join(OUT, "classes.png"))
    shutil.copyfile(os.path.join(BV2, hf["file"]), os.path.join(OUT, "terrain_h.f32"))
    counts = {CLASSES[k]: int((C == k).sum()) for k in range(len(CLASSES)) if (C == k).any()}

    # ---------------- the paint envelope and the guide sections (u, v) ----------------
    fu = [p[0] for p in L["floor"]["polygon"]]
    fv = [-p[1] for p in L["floor"]["polygon"]]
    env_px = (11776, 8704)                                        # 9 x 11 canvases of 1536 x 1024 on 1280 x 768
    cu, cv = (min(fu) + max(fu)) / 2, (min(fv) + max(fv)) / 2
    u0 = cu - env_px[0] / 2 / PPM
    v1 = cv + env_px[1] / 2 / PX_V
    env = {"u": [u0, u0 + env_px[0] / PPM], "v": [v1 - env_px[1] / PX_V, v1], "px": list(env_px), "centre_uv": [cu, cv],
           "floor_bbox_uv": [min(fu), max(fu), min(fv), max(fv)],
           "_": "the paint envelope: the floor's bbox centre, 9 x 11 canvases (1536 x 1024 on a 1280 x 768 stride) at v1's px/m"}
    sx, sy = 2, 2
    PAD = 64          # each section is rendered 64 px larger all round and cropped: v1's screen-space pen draws a line at a viewport's edge
    sw, sh = env_px[0] // sx, env_px[1] // sy
    sections = []
    for j in range(sy):
        for i in range(sx):
            cx, cy = sw * (i + 0.5), sh * (j + 0.5)
            c = [u0 + cx / PPM, v1 - cy / PX_V]
            sections.append({"id": f"s{j}{i}", "px_origin": [sw * i, sh * j], "px": [sw, sh], "centre_uv": c,
                             "u": [c[0] - (sw / 2 + PAD) / PPM, c[0] + (sw / 2 + PAD) / PPM], "v": [c[1] - (sh / 2 + PAD) / PX_V, c[1] + (sh / 2 + PAD) / PX_V],
                             "_uv": "the RENDERED window: the section + PAD px all round (cropped by lv_guide_stitch.py)"})
    os.makedirs(os.path.join(LV, VAR), exist_ok=True)
    for s in sections:
        json.dump({"_what": "BV2F LV Tier-B --frame-grid for guide section %s of layout %s" % (s["id"], VAR), "name": "barrow_v2 %s %s" % (VAR, s["id"]), "variant": VAR,
                   "scene": "res://scenes/bv2f_barrow_v2.tscn", "guide_px": [s["px"][0] + 2 * PAD, s["px"][1] + 2 * PAD], "pad_px": PAD, "px_per_m_across": PPM,
                   "pitch_deg": 52.95354112560294, "yaw_deg": 47.0, "walk_grid": {"u": [-1.0, 1.0], "v": [-1.0, 1.0], "step": 0.1},
                   "topdown": {"px": [2400, 2240], "px_per_m": 18.0}, "section": s["id"]},
                  open(os.path.join(LV, VAR, f"frame_grid_{s['id']}.json"), "w"), indent=1)

    # ---------------- level.json ----------------
    mere = np.array(L["mere"]["polygon"])
    A = {a["id"]: a for a in L["anchors"]["points"]}
    # ---------------- the DECLARED OPENINGS (deliverer doors) -- dark 'curtains' in the guide + the list PH's P6a overlay reads
    M = {m["id"]: m for m in L["models"]}
    F = {f["id"]: f for f in L["features"]}
    openings = []
    bo = M["barrow_front"]["opening"]
    openings.append({"id": "barrow_door", "point": "p02", "model": "barrow_front", "centre_sim": bo["centre"], "z0": 0.0, "w": bo["w"], "h": bo["h"],
                     "faces_deg": M["barrow_front"]["faces_compass_deg"], "curtain_inset_m": 1.9, "dark": True,
                     "_inset": "the build's door threshold is 0.4 m behind its AABB front (lv/models/measure/barrow_measure.json); the curtain 1.5 m into the passage"})
    ho = M["hall_porch"]["opening"]
    openings.append({"id": "hall_great_door", "point": "p04", "model": "longhall", "centre_sim": ho["centre"], "z0": 0.0, "w": ho["w"], "h": ho["h"],
                     "faces_deg": M["hall_porch"]["faces_compass_deg"], "curtain_inset_m": 1.6, "dark": True,
                     "_inset": "the porch is 1.29 m deep; the curtain at the hall's own wall line"})
    cv = F["sea_cave_mouth"]
    openings.append({"id": "sea_cave_mouth", "point": "p03", "model": "cave_cliff", "centre_sim": [round(sum(q[0] for q in cv["footprint"]) / len(cv["footprint"]), 4),
                     round(sum(q[1] for q in cv["footprint"]) / len(cv["footprint"]), 4)], "z0": cv["z_bottom_m"], "w": cv["opening"]["clear_w_m"],
                     "h": cv["opening"]["clear_h_m"], "faces_deg": cv["faces_deg"], "curtain_inset_m": 1.2 if M["cave_cliff"].get("glb") else -0.1, "dark": True})   # v7c (cave cliff trimmed): the dark sits ON the terrain face
    go = M["fallen_gable"]["opening"]
    openings.append({"id": "fallen_gable_breach", "point": "p06", "model": "fallen_gable", "centre_sim": go["centre"], "z0": 0.0, "w": go["w"], "h": go["h"],
                     "faces_deg": M["fallen_gable"]["faces_compass_deg"], "dark": False})
    wo = M["wreck"]["opening"]
    openings.append({"id": "wreck_rail", "point": "p01", "model": "wreck", "centre_sim": wo["centre"], "z0": 0.0, "w": wo["w"], "h": wo["h"],
                     "faces_deg": round((M["wreck"]["faces_compass_deg"] + 180.0) % 360.0, 2), "dark": False})
    # BV2F-LV R-C9-177 CHECK (a) probes: each deliverer opening's PROBE shape at the play camera (vertical door planes; the
    # open hull, the ruin's breach heap and the mere's ice are open to the sky, so their probes are horizontal)
    for o in openings:
        if o["id"] in ("barrow_door", "hall_great_door", "sea_cave_mouth"):
            o["probe"] = {"type": "v", "centre": o["centre_sim"], "faces_deg": o["faces_deg"], "w": o["w"], "h": o["h"], "z0": o["z0"],
                          "frontal_m2": round(o["w"] * o["h"], 3)}
    _wm = M["wreck"]
    _wf = next(f for f in L["features"] if f["id"] == "wreck_hull")
    _wl, _wb = _wm["size_m"]["w_local_x"], _wm["size_m"]["d_local_z"]
    next(o for o in openings if o["id"] == "wreck_rail")["probe"] = {"type": "h_rect", "centre": _wm["pos"], "rot_deg": _wf["axis_rot_deg"],
        "L": round(0.7 * _wl, 3), "W": round(0.45 * _wb, 3), "z": 0.4, "frontal_m2": round(0.7 * _wl * 0.45 * _wb, 3),
        "_": "the OPEN HULL (bodies come up through the shore ice / over the rail): its interior, 70 % of the length x 45 % of the beam, 0.4 m up"}
    _gm = M["fallen_gable"]
    _gt = math.radians(_gm["faces_compass_deg"])
    _gfv = (math.sin(_gt), -math.cos(_gt))
    _gs = _gm["size_m"]["w_local_x"]
    _gc = (_gm["pos"][0] + _gfv[0] * _gs * 0.2, _gm["pos"][1] + _gfv[1] * _gs * 0.2)
    next(o for o in openings if o["id"] == "fallen_gable_breach")["probe"] = {"type": "h_rect", "centre": [round(_gc[0], 4), round(_gc[1], 4)],
        "rot_deg": round(_gm["faces_compass_deg"], 3),          # the L axis runs ACROSS the facing: (cos t, sin t) for compass t
        "L": 4.0, "W": round(0.5 * _gs, 3), "z": round(0.5 * _gm["size_m"]["h"], 3), "frontal_m2": round(4.0 * 0.5 * _gs, 3),
        "_": "the BREACH heap (up out of ash): 4 m wide x half the ruin deep on its breach side, at half the ruin's height"}
    import bv2_geom as _G
    openings.append({"id": "mere_ice", "point": "p05", "model": "mere", "centre_sim": [round(float(mere[:, 0].mean()), 4), round(float(mere[:, 1].mean()), 4)],
                     "z0": 0.0, "w": None, "h": None, "faces_deg": None, "dark": False,
                     "probe": {"type": "poly", "polygon": L["mere"]["polygon"], "z": 0.03, "frontal_m2": round(_G.area([tuple(q) for q in L["mere"]["polygon"]]), 3),
                               "_": "p05's dead burst up through the mere's ice: the ice surface itself"}})
    level = {
        "_what": "BV2F lane LV: barrow_v2 layout v7b as a level of the v1 Barrow (read by scripts/bv2f/bv2f_level.gd); written by fid/lv/tools/bv2f_level_prep.py",
        "layout": os.path.relpath(lp, C9), "layout_sha256": sha(lp),
        "tints_srgb": tints, "classes": CLASSES, "class_counts_8ppm": counts,
        "knight": {"spawn_uv": [0.0, 0.0], "spawn_facing": "S", "guide_uv": [0.0, 0.0], "guide_facing": "S", "gear_stack": 4},
        "frame": {"guide_window": {"centre_uv": sections[0]["centre_uv"], "u": sections[0]["u"], "v": sections[0]["v"]},
                  "envelope": env, "sections": sections},
        "camera_clamp_default": False,
        "regions": {"ice": {"centre_uv": uv(mere.mean(0)), "axes_m": [float(np.ptp(mere[:, 0])), float(np.ptp(mere[:, 1]))]}},
        "placements": [{"id": "mound", "kind": "structure", "uv": [0.0, 60.0], "semi_axes": [1.0, 1.0], "rise_m": 0.0, "exponent": 1.0,
                        "toe_rho": 0.2, "cutting": {"half_w": 0.0, "v_facade": -999.0},
                        "passage": {"half_w": 0.0, "v0": 0.0, "v_end": 0.0, "risers_v": [], "riser_m": 0.0},
                        "_": "STUB: v1's mound spec is read by the frozen capture tool's walk-grid statistics; barrow_v2 has no v1 mound"}],
        "bounds": {"polygon_uv": [uv(p) for p in L["floor"]["polygon"][::4]],
                   "_": "v1's invisible walls (_build_bounds, unchanged) on the walkable floor's edge (every 4th vertex, 2 m spacing)"},
        "crucible": {"eye_height_m": 1.6, "station": {"uv": [0.0, 0.0]}, "boss_gate": {"uv": uv((A["p02"]["x"], A["p02"]["y"]))},
                     "spawns": [{"id": k, "uv": uv((a["x"], a["y"])), "r_m": 8.0} for k, a in A.items()]},
        "sim": {"heightfield": {"file": "terrain_h.f32", "shape": hf["shape"], "px_per_m": hf["px_per_m"], "extent_sim_m": ex, "sha256": hf["sha256"]},
                "classes_png": {"file": "classes.png", "px_per_m": CLS_PPM, "extent_sim_m": ex, "sha256": sha(os.path.join(OUT, "classes.png"))},
                "sea_z": sea_z, "openings": openings, "floor": L["floor"]["polygon"], "models": L["models"], "stair": L["stair"],
                "features": [f for f in L["features"] if f.get("render", "prism") != "sculpt"],
                "blobs": [b for b in L["sculpt"]["blobs"] if b["k"] in ("rock", "flag", "floe", "ice", "dark")],
                "anchors": L["anchors"]["points"], "lanes": [{"id": ln["id"], "polygon": ln["polygon"]} for ln in L["lanes"]],
                "model_class": {"longhall": "wood", "hall_porch": "wood", "fallen_gable": "char", "wreck": "wood", "barrow_front": "rock",
                                "standing_stones": "rock", "circle_stones": "rock", "grave_markers": "rock", "logs_and_beams": "wood",
                                "palisade": "wood", "braziers": "char", "cave_cliff": "rock", "stair_cliff": "rock", "cliff_faces": "rock",
                                "_outcrop": "rock"},
                "skip_models": ["birch_grove_1", "birch_grove_2", "birch_grove_3"],
                "blob_class": {"rock": "rock", "flag": "path", "floe": "shore_ice", "ice": "shore_ice", "dark": "passage_dark"},
                "_rules": "no plants in the guide (groves, tufts, juniper, trees skipped); flat marks (footprints, ripples, cracks) skipped; v1 tints for v1 classes"},
    }
    # SELF-CONTAINED for an export (the walkable app): every GLB the level uses is copied into data/bv2f/ext/ as RAW bytes
    # named .glb.bin (an export's include_filter ships non-resource files as themselves; a .glb would ship as its import),
    # and the classes PNG likewise; the level reads them with append_from_buffer / load_png_from_buffer.
    ext_dir = os.path.join(BF, "data", "bv2f", "ext")
    os.makedirs(ext_dir, exist_ok=True)
    RUNS = os.path.dirname(C9)

    def _src(gp):
        if gp.startswith("data/bv2f/"):
            return os.path.join(BF, gp)
        if gp.startswith("runs/"):
            return os.path.join(RUNS, gp[5:])
        return os.path.join(BV2, gp)
    copied, missing = {}, []
    for m in level["sim"]["models"]:
        for holder in [m] + list(m.get("instances") or []):
            gp = holder.get("glb")
            if not gp:
                continue
            src = _src(gp)
            if not os.path.exists(src):
                missing.append(gp)
                holder["glb"] = None
                continue
            key = gp.replace("/", "__") + ".bin"
            if key not in copied:
                shutil.copyfile(src, os.path.join(ext_dir, key))
                copied[key] = {"from": gp, "sha256": sha(src)}
            holder["glb"] = "data/bv2f/ext/" + key
    shutil.copyfile(os.path.join(OUT, "classes.png"), os.path.join(OUT, "classes_png.bin"))
    level["sim"]["classes_png"]["file"] = "classes_png.bin"
    level["sim"]["glb_copies"] = copied
    level["sim"]["glb_missing"] = missing
    json.dump(level, open(os.path.join(OUT, "level.json"), "w"), indent=1)
    print("[prep] level.json, classes.png %dx%d %s, envelope u %.2f..%.2f v %.2f..%.2f, %d sections %dx%d" % (
        W, Hn, counts, env["u"][0], env["u"][1], env["v"][0], env["v"][1], len(sections), sw, sh))


if __name__ == "__main__":
    main()
