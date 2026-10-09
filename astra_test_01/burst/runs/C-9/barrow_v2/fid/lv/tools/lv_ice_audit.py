#!/usr/bin/env python3
"""BV2F LV (R-C9-289/290): ICE TOPOLOGY AUDIT of the art blockout (level.json + terrain + classes as built) -- read-only.

    python3 fid/lv/tools/lv_ice_audit.py [--tag 67fc4b80b]   -> fid/lv/art/ice_audit.json + fid/lv/M1pp/ice_audit_map.jpg

ICE SURFACES = every ice slab item (ice_shorefast, ice_plates, ice_floes, ice_floes_bob, ice_ridges, ice_brash, cove_ice,
trans_rubble; the snow-class ice_rims and mere_seams lying on ice) + the GROUND drawn as an ice class (ice, ice_mid,
shore_ice, tide_ice: the mere, the margin field, the wreck's cradle, the bays). Rasterised at 10 px/m over the level.
  * STACK: a cell covered by >= 2 ice surfaces (slab on slab, or slab on drawn ground ice);
  * SLIVER: a slab item with mean width 2A/P < 0.30 m or area < 0.10 m2 that sits on another ice surface;
  * STRAIGHT / RECTANGULAR remnant: a slab item with an edge >= 1.6 m that is straight to 3 cm over its length, or
    rectangularity (area / min-area-rectangle) >= 0.88 with >= 1 m2; ground-ice regions with a straight edge >= 1.6 m
    (the class raster's edge cells on one line).
Each finding is projected to the guide plate (its top height) and binned per 5x5 chunk (col_row, PT's naming), pilot
(cols 0-2 x rows 0-2) vs Phase 3'. Also (R-C9-290) the CAVE-TOP inventory: carved snow faces that are vertical (|n_y| <
0.35) and the carved rock column tops, with their plate rectangles.
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
BF = os.path.normpath(os.path.join(LV, "..", "..", "..", "barrow_full", "godot", "data", "bv2f", "art"))
P = 100.617553710938
PITCH = math.radians(52.95354112560294)
CP, SP = math.cos(PITCH), math.sin(PITCH)
PV = P * SP
ICE_SLABS = ["ice_shorefast", "ice_plates", "ice_floes", "ice_floes_bob", "ice_ridges", "ice_brash", "cove_ice", "trans_rubble",
             "ice_rims", "mere_seams"]
ICE_CLASSES = ["ice", "ice_mid", "shore_ice", "tide_ice"]
R_PPM = 10.0


def main():
    tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else "current"
    L = json.load(open(os.path.join(BF, "level.json")))
    sim = L["sim"]
    lay = json.load(open(os.path.join(LV, "art", "layout_bv2art.json")))
    wu0, wv1 = lay["window"]["u"][0], lay["window"]["v"][1]
    hf = sim["heightfield"]
    Hh, Wh = hf["shape"]
    ex = hf["extent_sim_m"]
    Zf = np.fromfile(os.path.join(BF, hf["file"]), "<f4").reshape(Hh, Wh)
    C = np.asarray(Image.open(os.path.join(BF, "classes.png")))
    names = L["classes"]
    cppm = sim["classes_png"]["px_per_m"]
    u0, u1, v0, v1 = ex["x0"], ex["x1"], -ex["y1"], -ex["y0"]
    W, H = int((u1 - u0) * R_PPM), int((v1 - v0) * R_PPM)
    us = u0 + (np.arange(W) + 0.5) / R_PPM
    vs = v1 - (np.arange(H) + 0.5) / R_PPM
    U, V = np.meshgrid(us, vs)
    zg = Zf[np.clip(((-V - ex["y0"]) * hf["px_per_m"]).astype(int), 0, Hh - 1), np.clip(((U - u0) * hf["px_per_m"]).astype(int), 0, Wh - 1)]
    cg = C[np.clip(((v1 - V) * cppm).astype(int), 0, C.shape[0] - 1), np.clip(((U - u0) * cppm).astype(int), 0, C.shape[1] - 1)]
    ground_ice = np.isin(cg, [names.index(c) for c in ICE_CLASSES if c in names])
    cover = ground_ice.astype(np.int16)
    top = np.where(ground_ice, zg, -99.0)
    owner = np.full(U.shape, -1, np.int32)
    items = []

    def poly_px(poly):                                   # sim (x, y) = (u, -v)
        return [((q[0] - u0) * R_PPM, (v1 + q[1]) * R_PPM) for q in poly]
    for g in ICE_SLABS:
        for k, it in enumerate(sim["slabs"].get(g, {}).get("items", [])):
            img = Image.new("L", (W, H), 0)
            ImageDraw.Draw(img).polygon(poly_px(it["poly"]), fill=1)
            m = np.asarray(img).astype(bool)
            if not m.any():
                continue
            idx = len(items)
            pu = [q[0] for q in it["poly"]]
            pv = [-q[1] for q in it["poly"]]
            A = 0.5 * abs(sum(a * d - b * c for a, b, c, d in zip(pu, pv, pu[1:] + pu[:1], pv[1:] + pv[:1])))
            Pm = sum(math.hypot(c - a, d - b) for a, b, c, d in zip(pu, pv, pu[1:] + pu[:1], pv[1:] + pv[:1]))
            items.append({"group": g, "k": k, "z1": it["z1"], "area_m2": A, "perim_m": Pm, "poly_uv": list(zip(pu, pv)), "mask": m})
            stacked_here = (cover[m] > 0)
            items[-1]["on_other_share"] = float(stacked_here.mean())
            cover[m] += 1
            top[m] = np.maximum(top[m], it["z1"])
            owner[m] = idx
    stack = cover >= 2
    # per-cell plate projection -> chunk (col_row of the 5x5 grid, its home tile)
    px = (U - wu0) * P
    py = (wv1 - V) * PV - top * P * CP

    def chunk(x, y):
        c = int(np.clip(x // 1280, 0, 4))
        r = int(np.clip(y // 768, 0, 4))
        return "%d_%d" % (c, r)
    in_env = (px >= 0) & (px < 6656) & (py >= 0) & (py < 4096)
    per_tile = {}
    js, is_ = np.nonzero(stack & in_env)
    for j, i in zip(js, is_):
        ch = chunk(px[j, i], py[j, i])
        per_tile.setdefault(ch, {"stack_m2": 0.0, "slivers": 0, "straight": 0, "rect": 0})
        per_tile[ch]["stack_m2"] += 1.0 / R_PPM ** 2
    # per item: sliver / straight / rectangle
    findings = []
    for it in items:
        pts = it["poly_uv"]
        width = 2 * it["area_m2"] / max(it["perim_m"], 1e-6)
        sliver = (width < 0.30 or it["area_m2"] < 0.10) and it["on_other_share"] > 0.5
        longest = 0.0
        for a, b in zip(pts, pts[1:] + pts[:1]):
            longest = max(longest, math.hypot(b[0] - a[0], b[1] - a[1]))
        # straight runs: consecutive near-collinear vertices summed
        straight = 0.0
        run, prev_d = 0.0, None
        for a, b in zip(pts, pts[1:] + pts[:1]):
            d = (b[0] - a[0], b[1] - a[1])
            Ld = math.hypot(*d)
            if Ld < 1e-6:
                continue
            d = (d[0] / Ld, d[1] / Ld)
            if prev_d is not None and abs(d[0] * prev_d[1] - d[1] * prev_d[0]) < 0.03 / max(Ld, 0.03) and d[0] * prev_d[0] + d[1] * prev_d[1] > 0:
                run += Ld
            else:
                run = Ld
            straight = max(straight, run)
            prev_d = d
        # rectangularity via rotating the outline (min-area bounding rectangle over 90 headings)
        best = 1e9
        arr = np.array(pts)
        for th in np.linspace(0, math.pi / 2, 91):
            R_ = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
            q = arr @ R_
            best = min(best, float((q[:, 0].max() - q[:, 0].min()) * (q[:, 1].max() - q[:, 1].min())))
        rect = it["area_m2"] / max(best, 1e-6)
        cu, cv = float(arr[:, 0].mean()), float(arr[:, 1].mean())
        cx, cy = (cu - wu0) * P, (wv1 - cv) * PV - it["z1"] * P * CP
        flags = []
        if sliver:
            flags.append("sliver_on_ice")
        if straight >= 1.6:
            flags.append("straight_edge_%.1fm" % straight)
        if rect >= 0.88 and it["area_m2"] >= 1.0:
            flags.append("rectangular_%.2f" % rect)
        if flags and 0 <= cx < 6656 and 0 <= cy < 4096:
            ch = chunk(cx, cy)
            per_tile.setdefault(ch, {"stack_m2": 0.0, "slivers": 0, "straight": 0, "rect": 0})
            per_tile[ch]["slivers"] += int(sliver)
            per_tile[ch]["straight"] += int(straight >= 1.6)
            per_tile[ch]["rect"] += int(rect >= 0.88 and it["area_m2"] >= 1.0)
            findings.append({"group": it["group"], "item": it["k"], "chunk": ch, "plate_px": [round(cx), round(cy)], "uv": [round(cu, 2), round(cv, 2)],
                             "area_m2": round(it["area_m2"], 2), "mean_width_m": round(width, 2), "on_other_ice_share": round(it["on_other_share"], 2),
                             "longest_straight_m": round(straight, 2), "rectangularity": round(rect, 2), "flags": flags})
    # ground-ice straight edges (class raster): edge cells of the ground-ice mask, Hough-light: long runs along rows/cols/diagonals
    gi = ground_ice
    edge = gi & ~ndimage.binary_erosion(gi)
    lab, n = ndimage.label(edge, structure=np.ones((3, 3)))
    ground_straight = []
    for s in ndimage.find_objects(lab):
        sub = lab[s] > 0
        ys, xs = np.nonzero(sub)
        if len(xs) < 16:
            continue
        pts = np.c_[xs, ys].astype(float)
        c = pts.mean(0)
        _, sv, vt = np.linalg.svd(pts - c, full_matrices=False)
        d = vt[0]
        resid = np.abs((pts - c) @ np.array([-d[1], d[0]]))
        straight = resid < 0.6
        Lr = (np.ptp((pts[straight] - c) @ d) if straight.sum() > 8 else 0) / R_PPM
        if Lr >= 1.6 and straight.mean() > 0.6:
            jj, ii = int(c[1] + s[0].start), int(c[0] + s[1].start)
            ch = chunk(px[jj, ii], py[jj, ii])
            ground_straight.append({"chunk": ch, "plate_px": [round(float(px[jj, ii])), round(float(py[jj, ii]))], "uv": [round(float(U[jj, ii]), 2), round(float(V[jj, ii]), 2)], "length_m": round(float(Lr), 2)})
    # per-group stack pairs
    pairs = {}
    for it in items:
        if it["on_other_share"] > 0:
            pairs[it["group"]] = pairs.get(it["group"], 0) + 1
    # R-C9-290: the cave top (carved snow faces + the column tops)
    cave = {}
    for cname in ("snow", "rock"):
        f = sim["carved"]["files"].get(cname)
        if not f:
            continue
        arr = np.fromfile(os.path.join(BF, f["file"]), "<f4").reshape(-1, 6)
        pos, nrm = arr[:, :3], arr[:, 3:]
        tri_n = nrm.reshape(-1, 3, 3).mean(1)
        tri_p = pos.reshape(-1, 3, 3).mean(1)
        vert = np.abs(tri_n[:, 1]) < 0.35
        sel = vert if cname == "snow" else (tri_n[:, 1] > 0.85)
        tu, th, tv = tri_p[sel, 0], tri_p[sel, 1], -tri_p[sel, 2]
        x = (tu - wu0) * P
        y = (wv1 - tv) * PV - th * P * CP
        if len(x):
            cave[cname] = {"what": "vertical snow faces" if cname == "snow" else "flat rock tops", "triangles": int(sel.sum()),
                           "plate_bbox": [round(float(x.min())), round(float(y.min())), round(float(x.max())), round(float(y.max()))],
                           "chunks": sorted({chunk(a, b) for a, b in zip(x, y)})}
    pilot = lambda ch: int(ch.split("_")[0]) <= 2 and int(ch.split("_")[1]) <= 2
    out = {"_what": __doc__.split("\n")[0], "tag": tag, "raster_px_per_m": R_PPM,
           "totals": {"ice_slab_items": len(items), "stacked_area_m2": round(float(stack.sum()) / R_PPM ** 2, 1),
                      "stacked_area_in_paint_window_m2": round(float((stack & in_env).sum()) / R_PPM ** 2, 1),
                      "items_sitting_on_other_ice_by_group": pairs, "findings": len(findings), "ground_straight_edges": len(ground_straight)},
           "per_chunk": {k: dict(v, stack_m2=round(v["stack_m2"], 1), pilot=pilot(k)) for k, v in sorted(per_tile.items())},
           "findings": findings, "ground_straight_edges": ground_straight, "cave_top_r290": cave}
    json.dump(out, open(os.path.join(LV, "art", "ice_audit.json"), "w"), indent=1)
    # the map: the guide, stacked cells red, flagged items yellow/magenta, ground straight edges cyan, chunk grid
    g = Image.open(os.path.join(LV, "guide_art", "guide_art.png")).convert("RGB")
    ov = Image.new("RGBA", g.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    sj, si = np.nonzero(stack & in_env)
    for j, i in zip(sj[::2], si[::2]):
        d.rectangle([px[j, i] - 4, py[j, i] - 3, px[j, i] + 4, py[j, i] + 3], fill=(255, 0, 0, 110))
    for f_ in findings:
        col = (255, 220, 0, 255) if "sliver_on_ice" in f_["flags"] else (255, 0, 255, 255)
        x, y = f_["plate_px"]
        d.ellipse([x - 22, y - 22, x + 22, y + 22], outline=col, width=6)
    for gs in ground_straight:
        x, y = gs["plate_px"]
        d.rectangle([x - 26, y - 26, x + 26, y + 26], outline=(0, 255, 255, 255), width=6)
    for cname, cv in cave.items():
        d.rectangle(cv["plate_bbox"], outline=(0, 160, 255, 255), width=8)
    for c in range(5):
        for r in range(5):
            x0, y0 = c * 1280, r * 768
            d.rectangle([x0, y0, x0 + 1536, y0 + 1024], outline=(255, 255, 255, 140) if not (c <= 2 and r <= 2) else (0, 255, 0, 200), width=3)
            d.text((x0 + 14, y0 + 10), "%d_%d" % (c, r), fill=(255, 255, 255, 255))
    m = Image.alpha_composite(g.convert("RGBA"), ov).convert("RGB").resize((3328, 2048))
    m.save(os.path.join(LV, "M1pp", "ice_audit_map.jpg"), quality=86)
    print(json.dumps(out["totals"], indent=1))
    print(json.dumps(out["per_chunk"], indent=1))
    print(json.dumps(cave, indent=1))


if __name__ == "__main__":
    main()
