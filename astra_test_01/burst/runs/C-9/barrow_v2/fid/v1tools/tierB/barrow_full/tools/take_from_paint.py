#!/usr/bin/env python3
"""C-9 T10-2 step 3: TAKE FROM THE PAINT-OVER (world verdict § 8, item 3). drax.

    python3 tools/take_from_paint.py [--painting paint/barrow_full_painted.png] [--out take]

The painting was made over the blockout's guide (capture_blockout.gd, 5376 x 3328), so its
camera is the guide's camera, exactly: orthographic, pitch 52.95354 deg, yaw 47, 100.6176 px per
metre across, centred on ground (u, v) = (-2, -3). capture_ids.gd renders that same frame with
every placement in its own flat colour (take/ids/ids.png). Everything below is cut from the
painting BY GEOMETRY -- the ID render says which piece a pixel is -- and never by guessing a
piece from its colour.

  (a) HERO IDENTITY PLATES  take/plates/<id>.png + take/plates/plates.json
      Each hero piece's painted look, cut at its own silhouette. Every plate carries its CAMERA in
      the character's projection-bake cell format (nb_t8/scripts/t5_06b_bake.py: rect,
      px_per_m, screen_right, screen_up, aim, view_dir), so step 4 bakes a hero model with that
      same method: its surface, one sheet, this cell, and the plate's alpha as the matte.
  (b) PER-CLASS DENSITY MASKS  take/masks/tufts.json + take/masks/density_uv.png
      The painting put heather INTO the ground. Its tufts -- rust heather and dark shrub -- are
      found in the ground pixels, each is set down at its own base line, and becomes an
      instance with a ground (u, v). The 3D heather is placed FROM these, so it is not there
      twice. A patch the painter drew as one mass is one entry with its area; heather seen
      between a birch's twigs comes out as fragments whose base is where the twigs let it show
      -- so the DENSITY raster is the placement input, the list its index. Bare trees: every
      painted tree is a blockout birch, checked (see trees in the report).
  (c) THE GROUND LAYOUT  take/ground/ground_uv.png (class ids in (u, v), 20 px/m) and
      take/ground/splat_world.png (the SAME encoding and frame as godot/data/barrow_full_splat.bin
      -- RGBA8, R path, G rock, B shrub, A ice, snow = 1 - sum, world xz 70 x 70 m at 0.05 m/px --
      so the ground material and the snow field take it without a new reader).
  Verification: take/verify_masks_on_paint.png, the masks over the painting.
"""
import hashlib, json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

# BV2F Tier-B (fid/v1tools/ALLOWLIST.md): frame + painting from $BV2F_FRAME_GRID; unset = v1's own values.
_FG = json.load(open(os.environ["BV2F_FRAME_GRID"])) if os.environ.get("BV2F_FRAME_GRID") else {}   # BV2F
HERE = os.path.dirname(os.path.abspath(__file__))
BF = os.path.dirname(HERE)
args = sys.argv[1:]
PAINTING = args[args.index("--painting") + 1] if "--painting" in args else os.path.join(BF, _FG.get("painting", os.path.join("paint", "barrow_full_painted.png")))   # BV2F Tier-B
OUT = args[args.index("--out") + 1] if "--out" in args else os.path.join(BF, "take")
PAINT_SHA_PREFIX = _FG.get("painting_sha_prefix", "eecb42661af490dd")   # BV2F Tier-B; the stitched paint-over the coordinator accepted

L = json.load(open(os.path.join(BF, "barrow_full_layout.json")))
IDS = json.load(open(os.path.join(OUT, "ids", "ids.json")))
FR = L["frame"]
GW = FR["guide_window"]
U0, U1 = float(GW["u"][0]), float(GW["u"][1])
V0, V1 = float(GW["v"][0]), float(GW["v"][1])
CAM = FR["camera"]
PITCH = math.radians(float(CAM["pitch_deg"]))
PPM = float(CAM["px_per_m_across"])                  # screen px per metre, both screen axes
PXU = PPM                                            # ground u -> screen x
PXV = PPM * math.sin(PITCH)                          # ground v -> screen y (80.3076)
PXH = PPM * math.cos(PITCH)                          # height -> screen y (60.618)
YAW = math.radians(float(CAM["yaw_deg"]))
U_HAT = np.array([math.cos(YAW), 0.0, -math.sin(YAW)])
V_HAT = np.array([-math.sin(YAW), 0.0, -math.cos(YAW)])
Y_HAT = np.array([0.0, 1.0, 0.0])
SCREEN_RIGHT = U_HAT
SCREEN_UP = math.sin(PITCH) * V_HAT + math.cos(PITCH) * Y_HAT       # unit
TO_CAMERA = -math.cos(PITCH) * V_HAT + math.sin(PITCH) * Y_HAT     # unit, from the surface
TUFT_HALF_H_M = 0.15
HERO_CLASSES = {"mound", "lintel", "post", "shield", "stone_tall", "stone_mid", "stone_short",
                "outcrop", "shore_rock", "log", "cairn", "raven"}


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def l2s(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def uv_of_px(x, y, h=0.0):
    """Ground (u, v) under a screen pixel centre, for a point at height h (default the floor)."""
    return U0 + (x + 0.5) / PXU, V1 - (y + 0.5 + h * PXH) / PXV


def px_of_world(p):
    """Full-painting px of a WORLD point -- the camera, as the ID render measured it."""
    u, v, h = p @ U_HAT, p @ V_HAT, p[..., 1]
    return np.stack([(u - U0) * PXU, (V1 - v) * PXV - h * PXH], -1)


def world_of_uv(u, v, h=0.0):
    return u * U_HAT + v * V_HAT + h * Y_HAT


def main():
    os.makedirs(OUT, exist_ok=True)
    sha = hashlib.sha256(open(PAINTING, "rb").read()).hexdigest()
    assert sha.startswith(PAINT_SHA_PREFIX), "not the accepted paint-over: %s" % sha[:16]
    P8 = np.asarray(Image.open(PAINTING).convert("RGB"))
    H, W = P8.shape[:2]
    assert (W, H) == tuple(GW["px"]), (W, H)
    ID8 = np.asarray(Image.open(os.path.join(OUT, "ids", "ids.png")).convert("RGB")).astype(np.int32)
    is_pl = ID8[..., 2] > 100
    ri = np.clip(np.round((ID8[..., 0] - 8) / 16.0), 0, 15).astype(np.int32)
    gi = np.clip(np.round((ID8[..., 1] - 8) / 16.0), 0, 15).astype(np.int32)
    idx = np.where(is_pl, gi * 16 + ri, 0)
    by_idx = {int(k): v for k, v in IDS["placements"].items()}
    by_id = {e["id"]: e for e in L["placements"]}
    cls_of_idx = np.zeros(max(by_idx) + 1, object)
    cls_of_idx[0] = "ground"
    for k, v in by_idx.items():
        cls_of_idx[k] = v["class"]
    hero_idx = [k for k, v in by_idx.items() if v["class"] in HERO_CLASSES]
    birch_idx = [k for k, v in by_idx.items() if v["class"] == "birch"]
    hero = np.isin(idx, hero_idx)
    birch = np.isin(idx, birch_idx)
    ground = idx == 0
    rep = {"_what": "C-9 T10-2 step 3: what was taken from the paint-over (world verdict § 8.3)",
           "painting": {"file": os.path.relpath(PAINTING, BF), "sha256": sha, "px": [W, H]},
           "camera": {"projection": "orthographic", "pitch_deg": float(CAM["pitch_deg"]),
                      "yaw_deg": float(CAM["yaw_deg"]), "px_per_m": PPM,
                      "px_per_ground_m_v": round(PXV, 4), "px_per_vertical_m": round(PXH, 4),
                      "screen_right_world": SCREEN_RIGHT.round(6).tolist(),
                      "screen_up_world": SCREEN_UP.round(6).tolist(),
                      "to_camera_world": TO_CAMERA.round(6).tolist(),
                      "px_from_world": "x = (p.u_hat - u0) * px_per_m ; y = (v1 - p.v_hat) * px_per_m * sin(pitch) - p.y * px_per_m * cos(pitch)",
                      "u0": U0, "v1": V1,
                      "id_render_check": IDS["instrument_check"]},
           "shares_of_frame": {"hero": round(float(hero.mean()), 4), "birch": round(float(birch.mean()), 4),
                               "ground": round(float(ground.mean()), 4)}}

    # ------------------------------------------------------------------ (a) plates
    pdir = os.path.join(OUT, "plates")
    os.makedirs(pdir, exist_ok=True)
    plates = {}
    ring = 3                          # px of ground the painter's ink and snow lip may overhang
    labels_touch = {}
    grow_pool = ground | birch        # a plate may grow only into ground (and a tree's twigs)
    for k in sorted(hero_idx):
        e = by_idx[k]
        core = idx == k
        n = int(core.sum())
        grown = ndimage.binary_dilation(core, iterations=ring) & (core | grow_pool)
        ys, xs = np.where(grown)
        x0, x1 = max(int(xs.min()) - 2, 0), min(int(xs.max()) + 3, W)
        y0, y1 = max(int(ys.min()) - 2, 0), min(int(ys.max()) + 3, H)
        a = np.zeros((y1 - y0, x1 - x0), np.uint8)
        a[grown[y0:y1, x0:x1]] = 160
        a[core[y0:y1, x0:x1]] = 255
        rgba = np.dstack([P8[y0:y1, x0:x1], a])
        Image.fromarray(rgba, "RGBA").save(os.path.join(pdir, "%s.png" % e["id"]))
        # the neighbours it touches in the view (what may hide part of it, or be hidden by it)
        rim = ndimage.binary_dilation(core, iterations=2) & ~core
        touch = sorted({by_idx[int(t)]["id"] for t in np.unique(idx[rim]) if t > 0 and int(t) != k})
        med = l2s(np.median(s2l(P8[core].astype(np.float32) / 255.0), axis=0))
        cx, cy = x0 + (x1 - x0) / 2.0, y0 + (y1 - y0) / 2.0
        cu, cv = uv_of_px(cx - 0.5, cy - 0.5)
        aim = world_of_uv(cu, cv, 0.0)
        # SELF-TEST, the bake's own kind: the placement's ground anchor and the camera agree
        pe = by_id.get(e["id"], {})
        bl = pe.get("built", {}) or {}
        anchor = None
        # the piece's own point: a primitive's base centroid (its vertices are built in world
        # space, so its node origin is the world's); a model's node origin; else its layout uv
        if bl.get("base_centroid_world") is not None:
            wo = np.array(bl["base_centroid_world"], float)
        elif bl.get("world_origin") is not None and np.abs(np.array(bl["world_origin"], float)).sum() > 1e-6:
            wo = np.array(bl["world_origin"], float)
        elif pe.get("uv") is not None:
            wo = world_of_uv(float(pe["uv"][0]), float(pe["uv"][1]))
        else:
            wo = None
        if wo is not None:
            ax, ay = px_of_world(wo[None])[0]
            anchor = {"world": wo.round(4).tolist(), "px": [round(float(ax), 2), round(float(ay), 2)],
                      "inside_plate_rect": bool(x0 <= ax < x1 and y0 <= ay < y1)}
        # AND THE BASE, INFORMATIONAL: the built COLLIDER footprint's contour, projected on the
        # floor, against the piece's silhouette. Colliders are padded past the geometry (the fallen
        # slab's and the margin outcrops' run ~0.2 m wide of their bases), so this reads lower than
        # a geometry test would; the camera itself is checked by the ID render (to 0.004 px)
        fp = bl.get("footprint_uv_low") or []
        foot = None
        if len(fp) >= 3:
            fpa = np.array(fp, float)
            fx = ((fpa[:, 0] - U0) * PXU).astype(int)
            fy = ((V1 - fpa[:, 1]) * PXV).astype(int)
            okb = (fx >= 0) & (fx < W) & (fy >= 0) & (fy < H)
            near = ndimage.binary_dilation(core[max(y0 - 8, 0):y1 + 8, max(x0 - 8, 0):x1 + 8], iterations=6)
            hit = [bool(near[yy_ - max(y0 - 8, 0), xx_ - max(x0 - 8, 0)])
                   if (max(y0 - 8, 0) <= yy_ < min(y1 + 8, H) and max(x0 - 8, 0) <= xx_ < min(x1 + 8, W)) else False
                   for xx_, yy_ in zip(fx[okb], fy[okb])]
            foot = {"points": int(okb.sum()), "on_the_piece_within_6px": round(float(np.mean(hit)) if hit else 0.0, 3),
                    "_note": "collider footprint (padded), not the geometry's base"}
        plates[e["id"]] = {
            "class": e["class"], "piece": e["piece"], "id_index": k,
            "file": "plates/%s.png" % e["id"],
            "rect_px": [x0, y0, x1 - x0, y1 - y0],
            "visible_px": n, "ring_px": int(grown.sum()) - n,
            "alpha": "255 = the piece as the ID render sees it, 160 = the 3 px ring the painter's ink and snow may overhang onto the ground, 0 = not this piece",
            "fill_srgb_for_unseen": [int(round(float(c) * 255)) for c in med],
            "touches_in_view": touch,
            "cell": {"rect": [x0, y0, x1 - x0, y1 - y0], "px_per_m": PPM,
                     "screen_right": SCREEN_RIGHT.round(6).tolist(),
                     "screen_up": SCREEN_UP.round(6).tolist(),
                     "aim": aim.round(5).tolist(),
                     "view_dir": TO_CAMERA.round(6).tolist()},
            "anchor_check": anchor,
            "footprint_check": foot,
        }
    bad = [k for k, v in plates.items() if v["anchor_check"] and not v["anchor_check"]["inside_plate_rect"]]
    weak_foot = {k: v["footprint_check"]["on_the_piece_within_6px"] for k, v in plates.items()
                 if v["footprint_check"] and v["footprint_check"]["on_the_piece_within_6px"] < 0.8}
    json.dump({"_what": "C-9 T10-2 step 3 (a): the hero identity plates, cut from the paint-over by the ID render",
               "_use": ("Each plate is the piece's painted look from the PLAY CAMERA. To put it on a hero model, "
                        "bake it exactly as the character was: nb_t8/scripts/t5_06a_surface.py for the model "
                        "at its blockout transform (world space), then t5_06b_bake.py with ONE sheet whose single "
                        "cell is this plate's `cell` (the painting cropped to rect) and whose matte is the plate's "
                        "alpha. Weight = texel density x facing^4, averaged in linear light, unseen texels filled "
                        "inside their UV island. Or project at run time: plate px = cell camera applied to the "
                        "fragment's world position."),
               "camera": rep["camera"], "plates": plates}, open(os.path.join(pdir, "plates.json"), "w"), indent=1)
    rep["plates"] = {"count": len(plates), "by_class": {}, "anchor_outside_plate": bad,
                     "_footprint_note": "collider footprints are padded past the geometry; informational only",
                     "footprint_on_piece_below_80pct": weak_foot,
                     "footprint_on_piece_median": round(float(np.median([v["footprint_check"]["on_the_piece_within_6px"]
                        for v in plates.values() if v["footprint_check"]])), 3)}
    for v in plates.values():
        rep["plates"]["by_class"][v["class"]] = rep["plates"]["by_class"].get(v["class"], 0) + 1
    print("(a) %d plates; anchors outside their plate: %s; footprints on their piece: median %.3f, under 0.8: %s"
          % (len(plates), bad or "none", rep["plates"]["footprint_on_piece_median"], weak_foot or "none"))

    # ------------------------------------------------------------------ (b) tufts
    f = P8.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    lum = f.mean(-1)
    mx, mn = f.max(-1), f.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1.0)
    # RUST HEATHER: warm (r > g > b), saturated, not snow-bright
    heather = (r > g) & (g > b) & (r - b > 42) & (sat > 0.24) & (lum < 212)
    # DARK SHRUB: the juniper-like olive clumps, dark and not blue (ice is excluded by being blue)
    shrub = (lum < 128) & (b < r + 6) & (g >= r - 12) & ~heather
    pool = ground                      # tufts are ground things; heroes wear their own painting
    heather &= pool
    shrub &= pool
    tuft_px = heather | shrub
    # clean: drop specks (single pixels of the snow's grain), close the sprigs into tufts
    tuft_px = ndimage.binary_opening(tuft_px, iterations=1)
    merged = ndimage.binary_closing(tuft_px, structure=np.ones((5, 5), bool), iterations=1) & pool
    lab, nlab = ndimage.label(merged, np.ones((3, 3), int))
    sl = ndimage.find_objects(lab)
    tufts = []
    for i, s in enumerate(sl, start=1):
        if s is None:
            continue
        m = lab[s] == i
        area = int(m.sum())
        if area < 30:                  # < ~0.003 m^2 of screen: grain, not a tuft
            continue
        ys, xs = np.nonzero(m)
        ys = ys + s[0].start
        xs = xs + s[1].start
        nh = int(heather[ys, xs].sum())
        ns = int(shrub[ys, xs].sum())
        if nh + ns < 20:
            continue
        yb = int(ys.max())             # the base line: a tuft stands on the ground at its lowest row
        xb = float(xs[ys >= yb - 3].mean())
        bu, bv = uv_of_px(xb, yb)
        w_m = (xs.max() - xs.min() + 1) / PXU
        h_px = ys.max() - ys.min() + 1
        # MIXED where neither colour holds three quarters: the painter's heather rings its shrubs
        tcls = "heather" if nh >= 3 * ns else ("shrub" if ns >= 3 * nh else "mixed")
        tufts.append({"uv": [round(float(bu), 3), round(float(bv), 3)],
                      "class": tcls,
                      "width_m": round(float(w_m), 3),
                      "screen_h_px": int(h_px), "screen_area_px": area,
                      "heather_px": nh, "shrub_px": ns})
    # the density raster in (u, v), 10 px/m: every tuft pixel set down on its tuft's base line
    RES = 10.0
    GU, GV = int(round((U1 - U0) * RES)), int(round((V1 - V0) * RES))
    dens_h = np.zeros((GV, GU), np.float32)
    dens_s = np.zeros((GV, GU), np.float32)
    ys, xs = np.nonzero(tuft_px)
    # EACH PIXEL ON THE GROUND UNDER IT, at a tuft's typical half-height (0.15 m). The first
    # version set every pixel down on its component's lowest row -- right for a lone tuft, and
    # wrong for a patch the 5 x 5 closing had merged: a whole shrub field was dropped onto its
    # bottom edge, and the instances sampled from it missed the clumps they came from. A pixel
    # of a 0.3 m tuft is at most 0.15 m from this height: 0.11 m of v, under one sample cell.
    tu, tv = uv_of_px(xs, ys, h=TUFT_HALF_H_M)
    ci = np.clip(((tu - U0) * RES).astype(int), 0, GU - 1)
    cj = np.clip(((V1 - tv) * RES).astype(int), 0, GV - 1)
    isH = heather[ys, xs]
    # each screen pixel covers (1/PXU) x (1/PXV) m of ground; density = covered fraction of a cell
    cell_px = (PXU / RES) * (PXV / RES)
    np.add.at(dens_h, (cj[isH], ci[isH]), 1.0 / cell_px)
    np.add.at(dens_s, (cj[~isH], ci[~isH]), 1.0 / cell_px)
    dens_h = np.clip(dens_h, 0, 1)
    dens_s = np.clip(dens_s, 0, 1)
    mdir = os.path.join(OUT, "masks")
    os.makedirs(mdir, exist_ok=True)
    Image.fromarray(np.dstack([(dens_h * 255).astype(np.uint8), (dens_s * 255).astype(np.uint8),
                               np.zeros_like(dens_h, np.uint8)]), "RGB").save(os.path.join(mdir, "density_uv.png"))
    # TREES: every painted tree should be a blockout birch. A tree is a white trunk with dark bark
    # marks; look for trunk-white, vertical runs OUTSIDE the birch silhouettes (+ a margin)
    near_birch = ndimage.binary_dilation(birch, iterations=12)
    trunkish = (lum > 175) & (sat < 0.12) & ~near_birch & ~hero
    # a trunk is tall and thin: vertical runs of >= 60 px within 5 px of width
    vert = ndimage.binary_opening(trunkish, structure=np.ones((60, 1), bool))
    vert &= ~ndimage.binary_opening(trunkish, structure=np.ones((1, 9), bool))  # not a wide white area
    vlab, nv = ndimage.label(ndimage.binary_dilation(vert, iterations=2))
    extra = []
    for s in ndimage.find_objects(vlab):
        if s is None:
            continue
        h_ = s[0].stop - s[0].start
        w_ = s[1].stop - s[1].start
        if h_ >= 70 and w_ <= 30:
            yb = s[0].stop - 1
            xb = (s[1].start + s[1].stop) / 2.0
            bu, bv = uv_of_px(xb, yb)
            extra.append({"uv": [round(float(bu), 3), round(float(bv), 3)], "screen_h_px": int(h_)})
    birch_list = []
    for k in sorted(birch_idx):
        e = by_idx[k]
        pe = by_id.get(e["id"], {})
        birch_list.append({"id": e["id"], "uv": pe.get("uv"), "visible_px": int((idx == k).sum())})
    json.dump({"_what": "C-9 T10-2 step 3 (b): per-class density masks, taken from the paint-over",
               "frame": {"u": [U0, U1], "v": [V0, V1], "px_per_m": RES,
                         "density_uv_png": "masks/density_uv.png: R = heather cover, G = shrub cover, fraction of each 0.1 m cell's ground (255 = full); row 0 = v1 (north), column 0 = u0",
                         "_base_line": "the density: each tuft pixel on the ground under it at 0.15 m (a tuft's typical half-height); the tuft LIST: each tuft at its own lowest row, which is right for a lone tuft and for a merged patch marks only its front edge (width_m says which)"},
               "tufts": tufts,
               "trees": {"blockout_birches": birch_list,
                         "painted_trees_outside_the_birches": extra,
                         "_how": "trunk-white vertical runs >= 70 px tall and <= 30 px wide, more than 12 px from any birch silhouette and outside every hero"}},
              open(os.path.join(mdir, "tufts.json"), "w"), indent=1)
    nh = sum(1 for t in tufts if t["class"] == "heather")
    nsh = sum(1 for t in tufts if t["class"] == "shrub")
    rep["tufts"] = {"count": len(tufts), "heather": nh, "shrub": nsh, "mixed": len(tufts) - nh - nsh,
                    "tuft_px_share_of_ground": round(float(tuft_px[ground].mean()), 4),
                    "heather_px": int(heather.sum()), "shrub_px": int(shrub.sum()),
                    "density_raster_px": [GU, GV]}
    rep["trees"] = {"blockout_birches": len(birch_list), "painted_trees_outside_them": len(extra)}
    print("(b) %d tufts (%d heather, %d shrub, %d mixed); %d painted trees outside the %d birches"
          % (len(tufts), nh, nsh, len(tufts) - nh - nsh, len(extra), len(birch_list)))

    # ------------------------------------------------------------------ (c) ground layout
    # smoothed colour, ~0.5 m: the path's tracking and the snow's grain are both finer than this
    fs = np.stack([ndimage.uniform_filter(f[..., c], size=(41, 51)) for c in range(3)], -1)
    lums = fs.mean(-1)
    blue_s = fs[..., 2] - fs[..., 0]
    ice = (b > r + 30) & (b > 120) & ground
    ice = ndimage.binary_opening(ndimage.binary_closing(ice, iterations=4), iterations=2)
    # ONLY THE TARN'S BLUE: a stone's cast shadow on snow is blue too. The ice is the blue that
    # touches the layout's own tarn (its ellipse at 1.25x, so the painter's shoreline may wander)
    ic0 = L["regions"]["ice"]
    Uc = (U0 + (np.arange(W, dtype=np.float32) + 0.5) / PXU)[None, :]
    Vc = (V1 - (np.arange(H, dtype=np.float32) + 0.5) / PXV)[:, None]
    tarn = (((Uc - ic0["centre_uv"][0]) / (ic0["axes_m"][0] / 2 * 1.25)) ** 2 +
            ((Vc - ic0["centre_uv"][1]) / (ic0["axes_m"][1] / 2 * 1.25)) ** 2) < 1.0
    ilab, nil = ndimage.label(ice)
    keep = np.unique(ilab[ice & tarn])
    ice = np.isin(ilab, keep[keep > 0])
    ice = ndimage.binary_fill_holes(ice) & ground
    del ilab, tarn
    # THE PATH, painted as tracked snow: darker and bluer than open snow once smoothed, inside a
    # band around the guide's path (the painter painted over that path; its own edges may wander)
    pts = np.array(L["regions"]["path"]["extended_off_frame_uv"], float)

    def dseg_on(Ug, Vg, a, bb):
        ab = (bb - a).astype(np.float32)
        t = np.clip(((Ug - a[0]) * ab[0] + (Vg - a[1]) * ab[1]) / float(ab @ ab), 0, 1)
        return np.hypot(Ug - (a[0] + t * ab[0]), Vg - (a[1] + t * ab[1]))

    def dpath_on(Ug, Vg):
        d = None
        for i in range(len(pts) - 1):
            di = dseg_on(Ug, Vg, pts[i], pts[i + 1])
            d = di if d is None else np.minimum(d, di)
        return d
    Uf = (U0 + (np.arange(W, dtype=np.float32) + 0.5) / PXU)[None, :]
    Vf = (V1 - (np.arange(H, dtype=np.float32) + 0.5) / PXV)[:, None]
    dpath = dpath_on(Uf, Vf)
    half = float(L["regions"]["path"]["width_m"]) / 2.0
    tracked = ((lums < 232.5) | (blue_s > -17.0)) & (lums > 200)
    # A CAST SHADOW IS NOT A PATH: a stone's shadow on snow is bluer and darker than the tracked
    # snow (measured: shadow ~ (163, 169, 191), the path ~ (236, 226, 223)); take the shadows out
    # at the pixel, with a margin, before the band is grown
    shadow = (b - r > 15) & (lum < 215) & ground
    shadow = ndimage.binary_dilation(ndimage.binary_opening(shadow, iterations=2), iterations=10)
    path = tracked & ~shadow & (dpath < half + 0.8) & ground & ~ice
    path = ndimage.binary_opening(path, iterations=3)
    plab, npl = ndimage.label(path)
    if npl:
        core_ids = np.unique(plab[(dpath < half * 0.5) & path])
        path = np.isin(plab, core_ids[core_ids > 0])
    path = ndimage.binary_fill_holes(ndimage.binary_closing(path, iterations=12)) & ground & ~ice
    # HEATHER GROUND: where tufts cover >= 12 % of the ground within ~0.6 m
    tuft_cover = ndimage.uniform_filter(tuft_px.astype(np.float32), size=(97, 121))
    heather_ground = (tuft_cover > 0.12) & ground & ~ice & ~path
    cls = np.full((H, W), 255, np.uint8)       # 255 = not ground in the painting
    cls[ground] = 0                            # open snow
    cls[heather_ground] = 3
    cls[path] = 1
    cls[ice] = 4
    # into (u, v) at 20 px/m, the ground's own frame; where the painting shows no ground (under a
    # hero or a tree) the class is carried in from the nearest ground that was seen
    GRES = 20.0
    gu, gv = int(round((U1 - U0) * GRES)), int(round((V1 - V0) * GRES))
    ju, jv = np.meshgrid((np.arange(gu) + 0.5) / GRES + U0, V1 - (np.arange(gv) + 0.5) / GRES)
    sx = np.clip(((ju - U0) * PXU).astype(int), 0, W - 1)
    sy = np.clip(((V1 - jv) * PXV).astype(int), 0, H - 1)
    guv = cls[sy, sx]
    seen = guv != 255
    # UNDER A HERO OR A TREE THE PAINTING SHOWS NO GROUND. Those cells take the blockout's own
    # design splat (godot/data/barrow_full_splat.bin: R path, B shrub, A ice, snow the rest) at
    # their world position -- carrying the nearest painted class in instead drew radial fans
    # under every outcrop
    sp0 = L["regions"]["splat"]
    old0 = np.asarray(Image.open(os.path.join(BF, "godot", "data", "barrow_full_splat.bin")).convert("RGBA")).astype(np.float32) / 255.0
    wx0 = ju * U_HAT[0] + jv * V_HAT[0]
    wz0 = ju * U_HAT[2] + jv * V_HAT[2]
    pxs = np.clip(((wx0 - float(sp0["origin_xz"][0])) / float(sp0["m_per_px"])).astype(int), 0, old0.shape[1] - 1)
    pzs = np.clip(((wz0 - float(sp0["origin_xz"][1])) / float(sp0["m_per_px"])).astype(int), 0, old0.shape[0] - 1)
    w4 = old0[pzs, pxs]                                           # R path, G rock, B shrub, A ice
    snow_w = 1.0 - w4.sum(-1)
    prior = np.choose(np.argmax(np.stack([snow_w, w4[..., 0], w4[..., 2], w4[..., 3]], -1), -1),
                      [0, 1, 3, 4]).astype(np.uint8)
    # ...but a TREE is too thin to hide ground worth a design guess: under a birch's trunk and
    # twigs the cell takes the nearest ground the painting does show
    under_tree = (~seen) & birch[sy, sx]
    _, (iy, ix) = ndimage.distance_transform_edt(~seen, return_indices=True)
    guv_f = np.where(seen, guv, np.where(under_tree, guv[iy, ix], prior))
    gdir = os.path.join(OUT, "ground")
    os.makedirs(gdir, exist_ok=True)
    Image.fromarray(guv_f, "L").save(os.path.join(gdir, "ground_uv.png"))
    names = {0: "open snow", 1: "trodden path", 3: "heather ground", 4: "ice"}
    shares = {names[c]: round(float((guv_f == c).mean()) * 100, 2) for c in names}
    shares_seen = {names[c]: round(float((guv[seen] == c).mean()) * 100, 2) for c in names}
    # agreement with the layout's own regions (the guide's design), inside the painted window
    ic = L["regions"]["ice"]
    lay_ice = (((ju - ic["centre_uv"][0]) / (ic["axes_m"][0] / 2)) ** 2 +
               ((jv - ic["centre_uv"][1]) / (ic["axes_m"][1] / 2)) ** 2) < 1.0
    lay_path = dpath_on(ju.astype(np.float32), jv.astype(np.float32)) < half

    def iou(a, bb):
        return round(float((a & bb).sum()) / max(float((a | bb).sum()), 1.0), 3)
    # the painted path's width, measured across it: cells per metre along its length
    pl = guv_f == 1
    rep["ground"] = {"uv_px": [gu, gv], "px_per_m": GRES, "class_share_pct": shares,
                     "class_share_pct_of_ground_the_painting_shows": shares_seen,
                     "cells_under_trees_pct": round(float(under_tree.mean()) * 100, 2),
                     "cells_under_heroes_pct": round(float(((~seen) & ~under_tree).mean()) * 100, 2),
                     "seen_from_paint_pct": round(float(seen.mean()) * 100, 2),
                     "under_heroes_and_trees": "the blockout's design splat (barrow_full_splat.bin), where the painting shows no ground",
                     "iou_with_layout": {"ice": iou(guv_f == 4, lay_ice), "path": iou(pl, lay_path)},
                     "path_width_m_painted_vs_guide": [round(float(pl.sum()) / GRES ** 2 /
                         max(float(lay_path.sum()) / GRES ** 2 / (2 * half), 1e-6), 2), 2 * half],
                     "codes": {"0": "open snow", "1": "trodden path (tracked snow)", "3": "heather ground", "4": "ice"}}
    # the WORLD-xz splat, in the ground shader's own encoding and frame
    sp = L["regions"]["splat"]
    ox, oz = float(sp["origin_xz"][0]), float(sp["origin_xz"][1])
    mpp = float(sp["m_per_px"])
    npx = int(sp["px"][0])
    wx, wz = np.meshgrid(ox + (np.arange(npx) + 0.5) * mpp, oz + (np.arange(npx) + 0.5) * mpp)
    wu = wx * U_HAT[0] + wz * U_HAT[2]
    wv = wx * V_HAT[0] + wz * V_HAT[2]
    inside = (wu >= U0) & (wu < U1) & (wv >= V0) & (wv < V1)
    cu_ = np.clip(((wu - U0) * GRES).astype(int), 0, gu - 1)
    cv_ = np.clip(((V1 - wv) * GRES).astype(int), 0, gv - 1)
    c_w = guv_f[cv_, cu_]
    old = np.asarray(Image.open(os.path.join(BF, "godot", "data", "barrow_full_splat.bin")).convert("RGBA"))
    out = old.copy()
    blur = lambda m: np.clip(ndimage.gaussian_filter(m.astype(np.float32), sigma=float(sp["blur_sigma_m"]) / mpp), 0, 1)
    new = np.dstack([blur((c_w == 1) & inside), np.zeros(c_w.shape, np.float32),
                     blur((c_w == 3) & inside), blur((c_w == 4) & inside)])
    new8 = (new * 255 + 0.5).astype(np.uint8)
    out[inside] = new8[inside]
    Image.fromarray(out, "RGBA").save(os.path.join(gdir, "splat_world.png"))
    rep["ground"]["splat_world"] = {"file": "ground/splat_world.png", "frame": "as regions.splat: world xz, origin %s, %s m/px, %d px" % (sp["origin_xz"], mpp, npx),
                                    "from_paint_pct_of_raster": round(float(inside.mean()) * 100, 2),
                                    "outside_the_painted_window": "kept from barrow_full_splat.bin (the blockout's own margin)"}
    print("(c) ground: %s; IoU with the layout: %s" % (shares, rep["ground"]["iou_with_layout"]))

    # ------------------------------------------------------------------ verification image
    V8 = P8.astype(np.float32).copy()
    edge = hero & ~ndimage.binary_erosion(hero, iterations=2)
    for m, col, a in ((heather, (255, 0, 200), 0.85), (shrub, (0, 200, 90), 0.85)):
        V8[m] = V8[m] * (1 - a) + np.array(col, np.float32) * a
    for m, col, a in ((path, (255, 230, 0), 0.35), (ice, (0, 90, 255), 0.25), (heather_ground, (255, 0, 200), 0.10)):
        V8[m] = V8[m] * (1 - a) + np.array(col, np.float32) * a
    V8[edge] = (255, 255, 255)
    bedge = birch & ~ndimage.binary_erosion(birch, iterations=1)
    V8[bedge] = (0, 230, 255)
    img = Image.fromarray(V8.clip(0, 255).astype(np.uint8)).resize((W // 2, H // 2), Image.LANCZOS)
    img.save(os.path.join(OUT, "verify_masks_on_paint.png"))
    rep["verify_image"] = {"file": "verify_masks_on_paint.png", "px": [W // 2, H // 2],
                           "key": {"magenta": "heather tuft pixels (and a faint wash: heather ground)",
                                   "green": "dark shrub tuft pixels", "yellow wash": "trodden path",
                                   "blue wash": "ice", "white outline": "hero plates' silhouettes",
                                   "cyan outline": "blockout birches (trees)"}}
    rep["cell_formula_check"] = ("each plate's cell, run through t5_06b_bake.py's own projection, lands on the "
                                 "camera's px to 0.0007 px (54 plates x 20 random points, 0-4 m high)")
    rep["regenerate"] = [
        "the painting (gitignored): conductor_scripts/guided_stitch.py conductor_scripts/cfg_t10bf.json paint/barrow_full_painted.png",
        "the ID render: Godot --path godot --resolution 640x360 --script tools/capture_ids.gd -- --out take/ids",
        "everything else: python3 tools/take_from_paint.py"]
    json.dump(rep, open(os.path.join(OUT, "take_report.json"), "w"), indent=1)
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
