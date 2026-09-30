#!/usr/bin/env python3
"""C-9 T10-1b -- DRESS THE BARROW AS PAINTED.

    python3 barrow_paint_dress.py --out DIR

The coordinator's refinement: the density target is the concept painting itself
(T10C-barrow_a.png), not a density knob. The T10 segmentation pulled 70 objects out of it;
the painting has far more -- about ten standing stones round the mound where we place three,
dozens of dark juniper clumps where we place none, heather far denser than 19 tussocks, and
big layered rock outcrops at every edge where we have 27 copies of one small rock.

TWO PRODUCTS, ONE SEGMENTATION:

  1. godot/data/barrow_dress_a.json -- instances in the SAME schema as barrow_scene_a.json's
     `instances.height_a_authored` rows (asset, scene_xz, height_m, yaw_deg), so the scene
     places them through the same _place_prop the 70 go through.
  2. paint_classes.png -- the painting segmented ONCE into stone / rock / shrub / tree, the
     reference the coverage instrument (barrow_paint_compare.py) measures a render against.

THE RULER IS THE PAINTING'S OWN, and it is the T10 pipeline's (23_objects.py), not a new one:
an orthographic camera at pitch 52.9536 / azimuth 47 with K = 140.86 px/m fixed by the 1.85 m
barbarian. A standing object of height h spans h * cos(pitch) * K screen rows; a ground pixel
maps to world x/z through the camera basis, and world -> scene is the AUTHORED frame's offset
(2.619, -0.472) -- verified against the 70 emitted instances at median error 0.000 m.

THE FLOOR IS FLAT (R-C9-74), so every base pixel is unprojected at h = 0. That is the one
place this departs from the painting on purpose: the painting's ground rolls, ours does not.

SEGMENTATION, and why it is not the prompted masks: evf-sam's `rock` mask returned the
standing stones, its `birch_union` returned stones too, `juniper` found one clump of dozens.
The pipeline's own docstring says the same -- a prompted segmenter is reliable for big
distinctive things and unreliable for small repeated ones. So:
  - ICE, the FIGURE and the BARROW DOOR come from the prompted masks, which are good for them.
  - everything else is split by colour in CIELAB, then by SHAPE: grey components that are
    tall and upright are stones, the rest are rock; warm saturated growth is heather, dark
    low-chroma growth is juniper; thin pale branching structure is tree.
The class map is saved with an overlay so it can be checked by eye -- a coverage number
against a segmentation nobody looked at is a number about the segmentation.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
RUN = HERE.parent.parent                       # runs/C-9
ART = RUN / "artifacts" / "T10C-barrow" / "T10C-barrow_a.png"
WORK = RUN / "t10_barrow" / "work"
OUT_T10 = RUN / "t10_barrow" / "out"
GODOT = HERE.parent / "godot"

RIGHT = np.array([0.681998491287231, 0.0, -0.731353580951691])
UP = np.array([-0.583728015422821, 0.60246217250824, -0.54433536529541])
FWD = np.array([-0.440612882375717, -0.798147439956665, -0.410878270864487])
SIN_P, COS_P = 0.798147439956665, 0.602462172508240
# world (the painting camera's own frame) -> scene, for the AUTHORED ground's frame:
# scene = world - grid_origin + scene_offset = world - (-7.049, -7.088) + (-4.43, -7.56)
W2S = np.array([2.619, -0.472])

# THE STANDING STONES, ANNOTATED BY HAND, in painting pixels [x0, y0, x1, y1], base at y1.
#
# By hand because nothing automatic could find them. The prompted `standing_stones` mask
# catches four of twelve; a colour split sends their warm lichen to heather and their dark
# carving to juniper (a* 4.6 / b* 12 median, the same as heather's low end); a texture split
# fails too (local-std median 10.2 against juniper's 13.1, overlapping across most of both
# ranges -- and the rock faces score HIGHER than juniper). Twelve boxes read off a 100 px
# grid is the reliable instrument here, and it is written down so it can be checked.
#   cut: the stone runs off the top edge of the painting, so its painted height is a LOWER
#        bound; it is placed at `min_h` rather than at the visible fraction of itself.
STONE_BOXES = [
    {"box": [365, 85, 425, 205], "note": "plain stone, far left of the ring"},
    {"box": [490, 0, 555, 100], "cut": True, "min_h": 1.8, "note": "behind the ring, left, cut by the top edge"},
    {"box": [500, 15, 612, 255], "note": "the big carved spiral stone left of the door"},
    {"box": [622, 150, 712, 335], "note": "the carved stone flanking the door on the left"},
    {"box": [650, 0, 700, 45], "cut": True, "min_h": 1.6, "note": "behind the mound, cut by the top edge"},
    {"box": [1000, 0, 1040, 40], "cut": True, "min_h": 1.5, "note": "behind the mound, cut by the top edge"},
    {"box": [1100, 0, 1150, 75], "cut": True, "min_h": 1.7, "note": "behind the mound right, cut by the top edge"},
    {"box": [1170, 10, 1210, 95], "note": "small stone behind the ring, right"},
    {"box": [1020, 340, 1120, 495], "note": "the snow-capped stone in front of the door, right"},
    # already in the scene list, annotated so the COVERAGE reference includes them:
    {"box": [1105, 120, 1240, 400], "placed": True, "note": "the big rough stone right of the door (stone_mid)"},
    {"box": [1230, 40, 1335, 275], "placed": True, "note": "the serpent stone the raven sits on (stone_tall)"},
    {"box": [1365, 115, 1405, 180], "placed": True, "note": "small stone far right (placed as a rock by T10)"},
]
# THE FALLEN DEAD TREE at the bottom right, root end to crown end, in painting pixels. The
# kit log stands in for it: 2.6 m of trunk laid along the painted line.
FALLEN_TREE = {"root": [1480, 700], "tip": [1250, 1000], "box": [1200, 680, 1536, 1010]}
# NOT GROWTH, though dark: the barrow's own passage between the door posts, and the figure
# (the prompted figure mask misses the rim of his shield). Both read as juniper by colour.
EXCLUDE_BOXES = [[800, 195, 945, 345], [690, 470, 840, 640]]

CLASS_ID = {"other": 0, "stone": 1, "rock": 2, "shrub": 3, "tree": 4}
CLASS_RGB = {0: (0, 0, 0), 1: (230, 60, 60), 2: (240, 200, 40), 3: (60, 200, 90), 4: (80, 150, 255)}


def srgb_to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]], np.float32)
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883], np.float32)
    e, k = 216 / 24389, 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], -1)


def pix_to_scene(px, py, K, W, H, h=0.0):
    """A screen pixel's ground contact at height h -> scene x/z. 23_objects.ground_xz, at a
    fixed h because the floor is flat."""
    u = (px - W / 2.0) / K
    v = -(py - H / 2.0) / K
    D = (COS_P * v - h) / SIN_P
    x = RIGHT[0] * u + UP[0] * v + FWD[0] * D
    z = RIGHT[2] * u + UP[2] * v + FWD[2] * D
    return float(x + W2S[0]), float(z + W2S[1])


def scene_to_pix(sx, sy, sz, K, W, H):
    """The inverse, for any scene point (the camera is orthographic, so it is a dot product)."""
    w = np.array([sx - W2S[0], sy, sz - W2S[1]])
    return W / 2.0 + float(w @ RIGHT) * K, H / 2.0 - float(w @ UP) * K


def mask(name, shape):
    p = WORK / ("evf_a_%s.png" % name)
    if not p.exists():
        return np.zeros(shape, bool)
    return np.asarray(Image.open(p).convert("L")) > 127


def bottom_contour(m):
    """For each column of a component, the lowest pixel row that is set (the base, at the
    ground) and the run of set pixels above it (the height there). Columns with nothing
    return -1."""
    H, W = m.shape
    rows = np.where(m.any(axis=0), H - 1 - np.argmax(m[::-1, :], axis=0), -1)
    tops = np.where(m.any(axis=0), np.argmax(m, axis=0), -1)
    return rows, tops


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    rgb = np.asarray(Image.open(ART).convert("RGB")).astype(np.float32) / 255.0
    H, W = rgb.shape[:2]
    K = float(json.loads((OUT_T10 / "height_a_marigold.json").read_text())["figure"]["px_per_metre"])
    lab = srgb_to_lab(rgb)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    C = np.hypot(A, B)

    ice = ndimage.binary_dilation(mask("ice", L.shape), iterations=2)
    figure = ndimage.binary_dilation(mask("figure", L.shape), iterations=8)
    door = mask("barrow_door", L.shape)
    stone_seed = mask("standing_stones", L.shape) & ~door

    # SNOW: bright and low-chroma, or the blue of snow in shadow
    snow = ((L > 74) & (C < 17)) | ((L > 52) & (B < -3) & (C < 22) & ~ice)
    obj = ~(snow | ice | figure)
    obj = ndimage.binary_opening(obj, iterations=1)

    # SHAPE BEFORE COLOUR. The first version split by colour first and sent the standing
    # stones to SHRUB: their lichen is warm (a* 4.6, b* 12 median, the same as heather's
    # low end) and their carving is dark (L p10 25, juniper territory). Colour cannot tell a
    # carved stone from a juniper in this painting. MASS can: a stone or an outcrop is a
    # SOLID region that survives an opening with a ~13 px disc; a shrub is fragmented growth
    # and a dead tree is thin branching, and neither survives it. The survivors are grown
    # back to their full outline by geodesic reconstruction inside the object mask, so the
    # opening decides WHICH things are solid without shaving their edges.
    core = ndimage.binary_opening(obj, iterations=6)
    solid = ndimage.binary_propagation(core, mask=obj) & ndimage.binary_dilation(core, iterations=10)
    growth = obj & ~solid

    # growth: tall sparse components are trees, the rest shrub
    lab_t, nt = ndimage.label(ndimage.binary_closing(growth, iterations=2))
    tree = np.zeros_like(growth)
    for i, sl in enumerate(ndimage.find_objects(lab_t), start=1):
        if sl is None:
            continue
        comp = (lab_t[sl] == i) & growth[sl]
        hgt, wid = comp.shape
        fill = comp.sum() / float(hgt * wid)
        if hgt >= 1.25 * K * COS_P and fill < 0.26 and hgt > 0.9 * wid:
            tree[sl] |= comp
    tree |= (mask("trees", L.shape) | mask("birch2_dead", L.shape)) & growth
    shrub_all = growth & ~tree
    heather = shrub_all & (A > 5.0) & (B > 13.0)
    juniper = shrub_all & ~heather

    # STONE: the annotated boxes, minus the snow inside them, plus the door
    stone = door.copy()
    for sb in STONE_BOXES:
        x0, y0, x1, y1 = sb["box"]
        stone[y0:y1 + 1, x0:x1 + 1] |= obj[y0:y1 + 1, x0:x1 + 1]
    # ROCK: solid mass that is not a stone and is LIGHT -- a rock face in this painting is a
    # lit grey (L ~55-70) with dark crevices; a juniper clump is dark all through. So the rock
    # class is the solid mass above L 42 and not rust-coloured, and the crevices inside an
    # outcrop are filled back by a closing so the outcrop is one region, not lace.
    rust = (A > 5.0) & (B > 13.0)
    rock = solid & ~stone & (L > 42.0) & ~rust
    rock = ndimage.binary_closing(rock, iterations=3) & obj & ~stone
    lab_rk, nrk = ndimage.label(rock)
    if nrk:
        sizes = ndimage.sum(rock, lab_rk, range(1, nrk + 1))
        rock = np.isin(lab_rk, 1 + np.nonzero(sizes >= 400)[0])
    tree &= ~stone & ~rock
    fx0, fy0, fx1, fy1 = FALLEN_TREE["box"]
    # GROWTH IS EVERYTHING ELSE THAT IS NOT SNOW. The first cut took it from `growth` (what the
    # opening removed) -- and the dense juniper clumps SURVIVED the opening, so they were solid;
    # and they were too dark to be rock (L < 42); so they fell through every class and the
    # painting's dozens of junipers came back as six. The solid/growth split decides rock
    # against thin structure, not against dense shrub.
    shrub_all = obj & ~tree & ~stone & ~rock
    for ex in EXCLUDE_BOXES:
        shrub_all[ex[1]:ex[3] + 1, ex[0]:ex[2] + 1] = False
    heather = shrub_all & rust
    juniper = shrub_all & ~heather & (L < 50.0)
    shrub_all = heather | juniper
    lab_sh, nsh = ndimage.label(shrub_all)
    if nsh:
        sizes = ndimage.sum(shrub_all, lab_sh, range(1, nsh + 1))
        keep = np.isin(lab_sh, 1 + np.nonzero(sizes >= 60)[0])
        heather &= keep
        juniper &= keep
        shrub_all &= keep
    shrub = shrub_all & ~stone & ~rock

    # ------------------------------------------------------------------ placements
    inst = []
    existing = json.loads((GODOT / "data" / "barrow_scene_a.json").read_text())["instances"]["height_a_authored"]
    megal = [r for r in existing if r.get("asset") in ("stone_tall", "stone_mid", "stone_short", "post", "lintel")]
    mound = np.array([0.0, -4.0])
    cam_dir = np.array([math.sin(math.radians(47.0)), math.cos(math.radians(47.0))])
    stone_yaw = {"stone_tall": 60.0, "stone_mid": 60.0, "stone_short": 345.0}
    rng = np.random.default_rng(20260929)

    def near_existing(sx, sz, r):
        for e in megal:
            ex, ez = e["scene_xz"]
            if math.hypot(ex - sx, ez - sz) < r:
                return True
        return False

    # STONES: one per annotated box that is not already in the scene list
    stones_new = 0
    for sb in STONE_BOXES:
        if sb.get("placed"):
            continue
        x0, y0, x1, y1 = sb["box"]
        sub = obj[y0:y1 + 1, x0:x1 + 1]
        ys, xs = np.nonzero(sub)
        if ys.size == 0:
            continue
        yb = ys.max()
        base = ys >= yb - 3
        bx, by = float(xs[base].mean()) + x0, float(yb) + y0
        sx, sz = pix_to_scene(bx, by, K, W, H)
        h = (y1 - y0 + 1) / (K * COS_P)
        if sb.get("cut"):
            h = max(h, float(sb.get("min_h", 1.6)))
        model = "stone_tall" if h >= 2.2 else ("stone_mid" if h >= 1.5 else "stone_short")
        # THE CARVED FACE POINTS OUTWARD, as painted. Each model's manifest yaw is the turn at
        # which its sheet's front faces the CAMERA; turning it further by the angle between the
        # camera direction and this stone's outward direction points that face away from the
        # mound. Round the near side of the ring the two are nearly the same direction, which is
        # why the painting shows the carvings.
        o = np.array([sx, sz]) - mound
        phi_o = math.atan2(o[0], o[1])
        phi_c = math.atan2(cam_dir[0], cam_dir[1])
        yaw = (stone_yaw[model] + math.degrees(phi_o - phi_c)) % 360.0
        inst.append({"asset": model, "scene_xz": [round(sx, 3), round(sz, 3)], "height_m": round(h, 2),
                     "yaw_deg": round(yaw, 1), "width_mul": round(float(rng.uniform(0.9, 1.1)), 3),
                     "source": "painting_annotation", "class": "stone", "priority": True,
                     "note": sb.get("note", "")})
        stones_new += 1

    # ROCK OUTCROPS: rock_large packed along each component's base, a back row where it is deep
    lab_r, nr = ndimage.label(rock)
    rocks_new = 0
    for i, sl in enumerate(ndimage.find_objects(lab_r), start=1):
        if sl is None:
            continue
        comp = lab_r[sl] == i
        if comp.sum() < 300:
            continue
        rows, tops = bottom_contour(comp)
        cols = np.nonzero(rows >= 0)[0]
        step = max(int(0.72 * K), 8)                  # 0.72 m across the screen, 1:1 metres
        for c0 in range(cols.min(), cols.max() + 1, step):
            band = cols[(cols >= c0) & (cols < c0 + step)]
            if band.size < step * 0.35:
                continue
            by = float(np.max(rows[band])) + sl[0].start
            bx = float(band.mean()) + sl[1].start
            run = float(np.max(rows[band] - tops[band] + 1))
            h = float(np.clip(run / (K * COS_P) * rng.uniform(0.85, 1.05), 0.35, 1.7))
            sx, sz = pix_to_scene(bx, by, K, W, H)
            asset = "rock_large" if h >= 0.55 else "rock_small"
            inst.append({"asset": asset, "scene_xz": [round(sx, 3), round(sz, 3)],
                         "height_m": round(h * float(rng.uniform(0.85, 1.15)), 2),
                         "yaw_deg": round(float(rng.uniform(0, 360)), 1),
                         "source": "painting_seg", "class": "rock"})
            rocks_new += 1
            # LAYERED: a deep outcrop gets a second, lower rock set back behind the first --
            # 0.5 m further from the camera on the ground, which is 0.5 * sin(pitch) * K rows up
            if run > 1.15 * K * COS_P:
                bx2, by2 = bx + float(rng.uniform(-0.2, 0.2)) * K, by - 0.5 * SIN_P * K
                sx2, sz2 = pix_to_scene(bx2, by2, K, W, H)
                inst.append({"asset": "rock_large", "scene_xz": [round(sx2, 3), round(sz2, 3)],
                             "height_m": round(h * float(rng.uniform(0.7, 0.9)), 2),
                             "yaw_deg": round(float(rng.uniform(0, 360)), 1),
                             "source": "painting_seg", "class": "rock"})
                rocks_new += 1

    # SHRUBS: juniper where the growth is dark, heather where it is warm -- FILLED, not edged.
    #
    # The first version put one plant per 0.6-0.75 m along each growth region's BOTTOM edge,
    # which is how an outcrop is placed and not how a slope of heather grows: shrub coverage
    # came back 0.14 against the painting, the lowest of the four classes, on the class that
    # covers more of the painting than any other. So each region is sampled on a grid spaced in
    # GROUND metres (x: spacing * K px across the screen; y: spacing * sin(pitch) * K rows,
    # because a ground metre up-screen is foreshortened), and a plant stands wherever a grid
    # point lands in the region, based at that point. Heather is procedural and costs ~1 us a
    # tussock, so it is dense; juniper is a 20k-triangle model at ~28 us each, so it is not.
    shrubs = {"juniper": 0, "heather": 0}
    # CLUMP FLOORS IN PIXELS OF PAINTING, from what a plant is: 700 px is a clump about 0.35 m
    # across the screen (0.35 * 140.86 = 49 px wide by ~14 rows), the smallest dark mass that is
    # a juniper rather than a rock crevice or a cast shadow; 150 px of warm growth is a tuft.
    # At 90 / 40 px the fill found 190 "junipers", most of them 7 cm specks of dark paint.
    # T10-1c: DENSER, now that instancing takes the per-copy cost off -- heather 0.36 -> 0.26 m,
    # juniper 0.62 -> 0.46 m between plants in a clump
    for asset, m, spacing, hlo, hhi, min_px in (("juniper", juniper & shrub, 0.46, 0.55, 1.4, 700),
                                                 ("heather", heather & shrub, 0.26, 0.35, 0.95, 150)):
        dx = max(int(spacing * K), 4)
        dy = max(int(spacing * SIN_P * K), 4)
        lab_s, ns = ndimage.label(ndimage.binary_closing(m, iterations=2))
        sizes = ndimage.sum(np.ones_like(lab_s), lab_s, range(1, ns + 1)) if ns else []
        keep = np.isin(lab_s, 1 + np.nonzero(np.asarray(sizes) >= min_px)[0]) if ns else np.zeros_like(m)
        # the local height of the growth above each pixel: the run of region pixels upward
        run = np.zeros(m.shape, np.int32)
        for yy in range(1, m.shape[0]):
            run[yy] = np.where(keep[yy], run[yy - 1] + 1, 0)
        hit = set()
        off = 0
        for gy in range(dy // 2, m.shape[0], dy):
            off = (off + dx // 2) % dx               # a staggered grid, so rows do not stack in columns
            for gx in range(off, m.shape[1], dx):
                if not keep[gy, gx]:
                    continue
                # base the plant at the region's lowest pixel within half a cell below the point
                yb = gy
                while yb + 1 < m.shape[0] and yb + 1 <= gy + dy // 2 and keep[yb + 1, gx]:
                    yb += 1
                h = float(np.clip(run[yb, gx] / (K * COS_P) * rng.uniform(0.8, 1.1), hlo, hhi))
                sx, sz = pix_to_scene(float(gx) + float(rng.uniform(-0.3, 0.3)) * dx, float(yb), K, W, H)
                inst.append({"asset": asset, "scene_xz": [round(sx, 3), round(sz, 3)],
                             "height_m": round(h, 2), "yaw_deg": round(float(rng.uniform(0, 360)), 1),
                             "source": "painting_seg", "class": "shrub"})
                shrubs[asset] += 1
                hit.add(int(lab_s[gy, gx]))
        # EVERY CLUMP GETS AT LEAST ONE. A grid cell is 87 x 70 px for juniper; a painted clump
        # is often 60 x 40, so the grid alone missed more than half of them -- the first run of
        # this fill placed 11 junipers where the edge method had placed 54. A clump no grid
        # point landed in gets one plant at the centre of its base.
        for i, sl in enumerate(ndimage.find_objects(lab_s), start=1):
            if sl is None or i in hit:
                continue
            comp = (lab_s[sl] == i) & keep[sl]
            if comp.sum() < min_px:
                continue
            ys, xs = np.nonzero(comp)
            yb = ys.max()
            bx = float(xs[ys >= yb - 2].mean()) + sl[1].start
            h = float(np.clip((ys.max() - ys.min() + 1) / (K * COS_P), hlo, hhi))
            sx, sz = pix_to_scene(bx, float(yb + sl[0].start), K, W, H)
            inst.append({"asset": asset, "scene_xz": [round(sx, 3), round(sz, 3)],
                         "height_m": round(h, 2), "yaw_deg": round(float(rng.uniform(0, 360)), 1),
                         "source": "painting_seg", "class": "shrub"})
            shrubs[asset] += 1

    # TREES: a birch per upright tree component; the wide low one at the bottom right is the
    # painting's FALLEN dead tree, and the kit log stands in for it
    lab_tr, ntr = ndimage.label(ndimage.binary_dilation(tree, iterations=3))
    trees_new = 0
    logs = 0
    for i, sl in enumerate(ndimage.find_objects(lab_tr), start=1):
        if sl is None:
            continue
        comp = (lab_tr[sl] == i) & tree[sl]
        if comp.sum() < 150:
            continue
        ys, xs = np.nonzero(comp)
        ys = ys + sl[0].start
        xs = xs + sl[1].start
        hgt = ys.max() - ys.min() + 1
        wid = xs.max() - xs.min() + 1
        y1 = ys.max()
        base = ys >= y1 - max(2, int(hgt * 0.05))
        bx, by = float(xs[base].mean()), float(ys[base].mean())
        sx, sz = pix_to_scene(bx, by, K, W, H)
        if fx0 <= xs.mean() <= fx1 and fy0 <= ys.mean() <= fy1 and wid > 0.8 * hgt:
            continue                     # the fallen tree is placed from its annotation
        h = float(np.clip(hgt / (K * COS_P), 1.2, 3.6))
        inst.append({"asset": "birch", "scene_xz": [round(sx, 3), round(sz, 3)], "height_m": round(h, 2),
                     "yaw_deg": round(float(rng.uniform(0, 360)), 1), "source": "painting_seg",
                     "class": "tree"})
        trees_new += 1

    # THE FALLEN TREE: the log laid along the painted trunk, centred on it
    r = FALLEN_TREE["root"]
    tp = FALLEN_TREE["tip"]
    ax, az = pix_to_scene(r[0], r[1], K, W, H)
    bx2, bz2 = pix_to_scene(tp[0], tp[1], K, W, H)
    # the kit log's long axis is its model +X (size_m [2.6, 0.43, 0.42]); a Y rotation by
    # theta turns +X to (cos theta, -sin theta) in x/z, so theta = atan2(-dz, dx)
    th = math.degrees(math.atan2(-(bz2 - az), bx2 - ax))
    inst.append({"asset": "log", "scene_xz": [round((ax + bx2) * 0.5, 3), round((az + bz2) * 0.5, 3)],
                 "height_m": 0.4254, "yaw_deg": round(th % 360.0, 1), "source": "painting_annotation",
                 "class": "tree", "note": "the painting's fallen dead tree; painted length %.2f m" % math.hypot(bx2 - ax, bz2 - az)})
    logs += 1
    ftb = (obj & ~stone & ~rock & (L > 55) & (C < 14))
    tree[fy0:fy1 + 1, fx0:fx1 + 1] |= ftb[fy0:fy1 + 1, fx0:fx1 + 1]

    cls = np.zeros(L.shape, np.uint8)
    cls[rock] = CLASS_ID["rock"]
    cls[shrub] = CLASS_ID["shrub"]
    cls[tree] = CLASS_ID["tree"]
    cls[stone] = CLASS_ID["stone"]
    Image.fromarray(cls).save(out / "paint_classes.png")
    vis = (rgb * 0.40 * 255).astype(np.uint8)
    for cid, col in CLASS_RGB.items():
        if cid == 0:
            continue
        mm = cls == cid
        vis[mm] = (0.35 * rgb[mm] * 255 + 0.65 * np.array(col)).astype(np.uint8)
    Image.fromarray(vis).save(out / "paint_classes_overlay.png")

    # the painting's framing and the figure, for the comparison render
    fig = mask("figure", L.shape)
    fy, fx = np.nonzero(fig)
    fb = fy >= fy.max() - 3
    fsx, fsz = pix_to_scene(float(fx[fb].mean()), float(fy[fb].mean()), K, W, H)
    csx, csz = pix_to_scene(W / 2.0, H / 2.0, K, W, H)
    corners = [pix_to_scene(x, y, K, W, H) for x, y in ((0, 0), (W, 0), (W, H), (0, H))]
    frame = {"image_px": [W, H], "K_px_per_m": K, "ortho_size_m": round(H / K, 4),
             "footprint_xz": [[round(a, 3), round(b, 3)] for a, b in corners],
             "aim_scene_xyz": [round(csx, 3), 0.0, round(csz, 3)],
             "figure_scene_xz": [round(fsx, 3), round(fsz, 3)],
             "_aim": "the painting's centre pixel unprojected at h = 0: the flat floor"}
    doc = {"_what": "C-9 T10-1b: dressing read off the concept painting by segmentation; see tools/barrow_paint_dress.py",
           "frame": frame,
           "counts": {"stones": stones_new, "rocks": rocks_new, "juniper": shrubs["juniper"],
                      "heather": shrubs["heather"], "birches": trees_new, "logs": logs},
           "class_px": {k: int((cls == v).sum()) for k, v in CLASS_ID.items()},
           "instances": inst}
    (GODOT / "data" / "barrow_dress_a.json").write_text(json.dumps(doc, indent=1))
    (out / "paint_frame.json").write_text(json.dumps(frame, indent=1))
    print(json.dumps({"counts": doc["counts"], "class_px": doc["class_px"], "frame": frame}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
