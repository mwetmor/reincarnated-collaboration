#!/usr/bin/env python3
"""P6 Phase 1 (conductor task, R-C9-177 v7c): GEOMETRY AGREEMENT of LV's ID render against the LAYOUT POLYGONS
(layout_v7c.json), never against the guide's own class map (Gate-1 W-7), plus an independent read of LV's check (a)
door visibility from the same ID render.

(1) Per placed layout object, the LAYOUT SILHOUETTE = the union of its projected placement prisms:
      * box instance / single model: the rectangle (size_m w x d, rotated by godot_rot_y_deg as bv2f_level.gd
        _place_box does: local x -> (cos t, -sin t), local z -> (sin t, cos t) in sim (x, y)), from z to z + h
        (_place_box stands the model's AABB bottom on z), convex hull of the 8 projected corners;
      * beam instance: the segment a-b drawn thickness_m wide.
    Projection (LV's declared_openings.json law): x = (u - u0) 100.6176, y = (v1 - v) 80.3076 - z 60.6137,
    u = sim x, v = -sim y, (u0, v1) = the guide envelope.
    The ID SILHOUETTE = ids_v7c.png pixels with the object's id (R<<16|G<<8|B, guide_manifest id_table); a model's own
    declared-opening curtain counts as the model (barrow_door -> barrow_front, hall_great_door -> longhall).
    OCCLUSION: the layout silhouette is clipped by every OTHER placed object's ID pixels (what stands in front of it
    hides it in the render, not in the layout).  IoU = |ID n layout_vis| / |ID u layout_vis|.
(2) The SAME MEASURE ON v1 (like for like): v1's ID render (take/ids/ids.png) against v1's own placements
    (barrow_full_layout.json built.footprint_uv_low, y_min..y_max, px_of_uv), same occlusion rule. Its median is the
    like-for-like bar; the ruled bar 0.513 (P6b: v1 ID silhouette vs the PAINTED non-ground class) is reported beside it.
(3) MISSING (a placed layout object with no ID pixels) and EXTRA (an ID with no layout object) are listed.
(4) Check (a), independently: the declared openings' visible screen area from the ID render.
      * v-probe openings (barrow door, hall great door, sea cave mouth): the curtain id's pixels / 100.6176^2
        (LV's unit: projected screen m^2), against LV's check_a.json;
      * the breach, the open hull and the mere (horizontal probes): LV's probe polygons are reproduced from
        bv2f_level_prep.py; visible = probe px whose id is NOT an occluding placed model (ground / the opening's own
        model allowed), against the full probe.
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

LV = FID / "lv"
GV = LV / "guide_v7c"
PXV = 80.3076
PXH = 60.6137


def law7():
    env = jload(GV / "guide_manifest.json")["envelope"]
    u0, v1 = env["u"][0], env["v"][1]
    return lambda x, y, z: ((x - u0) * PPM_V1, (v1 + y) * PXV - z * PXH)      # v = -y


def hull(pts):
    pts = sorted(set((round(a, 2), round(b, 2)) for a, b in pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def box_hull(law, pos, z, rot_deg, w, d, h):
    t = math.radians(rot_deg)
    ex = (math.cos(t), -math.sin(t))
    ez = (math.sin(t), math.cos(t))
    cs = []
    for a in (-w / 2, w / 2):
        for b in (-d / 2, d / 2):
            x = pos[0] + ex[0] * a + ez[0] * b
            y = pos[1] + ex[1] * a + ez[1] * b
            for zz in (z, z + h):
                cs.append(law(x, y, zz))
    return hull(cs)


def layout_masks(shape):
    L = jload(LV / "layout_v7c.json")
    law = law7()
    H, W = shape
    out = {}
    skip = {"birch_grove_1", "birch_grove_2", "birch_grove_3"}          # the guide carries no plants (bv2f_level_prep)
    for m in L["models"]:
        if m["id"] in skip:
            continue
        im = Image.new("L", (W, H), 0)
        dr = ImageDraw.Draw(im)
        insts = m.get("instances") or []
        n = 0
        if not insts:
            if not m.get("glb"):
                continue                                                  # no GLB slot: bv2f_level places nothing
            s = m["size_m"]
            dr.polygon(box_hull(law, m["pos"], float(m["z"]), float(m["godot_rot_y_deg"]), s["w_local_x"], s["d_local_z"],
                                float(m.get("aabb_h_m", s["h"]))), fill=255)
            n = 1
        for ins in insts:
            if ins["type"] == "box":
                s = ins["size_m"]
                dr.polygon(box_hull(law, ins["pos"], float(ins["z"]), float(ins["godot_rot_y_deg"]), s[0], s[1], s[2]), fill=255)
            else:
                a = law(*ins["a"])
                b = law(*ins["b"])
                dr.line([a, b], fill=255, width=max(1, int(round(float(ins["thickness_m"]) * PPM_V1))))
            n += 1
        out[m["id"]] = {"mask": np.asarray(im) > 0, "pieces": n}
    return out


def ids_v7c():
    a = np.asarray(Image.open(GV / "ids_v7c.png").convert("RGB")).astype(np.int32)
    return (a[..., 0] << 16) | (a[..., 1] << 8) | a[..., 2]


OWN_CURTAIN = {"curtain_barrow_door": "barrow_front", "curtain_hall_great_door": "longhall"}


def iou_rows(idm, table, lmasks):
    name_of = {int(k): v["id"] for k, v in table.items()}
    model_ids = {k: v for k, v in name_of.items() if table[str(k)]["piece"] in ("model", "group")}
    obj_px = {}
    for k, nm in name_of.items():
        tgt = OWN_CURTAIN.get(nm, nm)
        if tgt in lmasks:
            obj_px.setdefault(tgt, []).append(k)
    placed_any = np.isin(idm, [k for k, nm in name_of.items() if OWN_CURTAIN.get(nm, nm) in lmasks])
    rows = {}
    for nm, L in lmasks.items():
        ks = obj_px.get(nm, [])
        idmask = np.isin(idm, ks) if ks else np.zeros(idm.shape, bool)
        others = placed_any & ~idmask
        lay = L["mask"] & ~others
        inter = int((idmask & lay).sum())
        uni = int((idmask | lay).sum())
        cont = round(int((idmask & L["mask"]).sum()) / max(int(idmask.sum()), 1), 3) if idmask.any() else None
        off = None
        if idmask.any() and lay.any():
            c1 = ndimage.center_of_mass(idmask)
            c2 = ndimage.center_of_mass(lay)
            off = round(float(np.hypot(c1[0] - c2[0], c1[1] - c2[1])) / PPM_V1, 2)
        rows[nm] = {"id_px": int(idmask.sum()), "layout_px": int(L["mask"].sum()), "layout_visible_px": int(lay.sum()),
                    "iou": round(inter / uni, 3) if uni else None, "containment": cont, "centroid_offset_m": off,
                    "pieces": L["pieces"], "ids": ks}
    return rows, name_of


def v1_like_for_like():
    import importlib.util
    spec = importlib.util.spec_from_file_location("pw_v1_readonly", BF / "tools/paint_world_prep.py")
    PW = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(PW)
    idx, table = PW.id_index()
    H, W = idx.shape
    L = jload(BF / "barrow_full_layout.json")
    by_id = {v["id"]: k for k, v in table.items()}
    placed = [p for p in L["placements"] if p.get("built", {}).get("footprint_uv_low") and p["id"] in by_id]
    allk = [by_id[p["id"]] for p in placed]
    placed_any = np.isin(idx, allk)
    rows = {}
    for p in placed:
        b = p["built"]
        y0, y1 = float(b.get("y_min", 0.0)), float(b.get("y_max", 0.0))
        pts = [PW.px_of_uv(u, v, h) for u, v in b["footprint_uv_low"] for h in (y0, y1)]
        im = Image.new("L", (W, H), 0)
        ImageDraw.Draw(im).polygon(hull(pts), fill=255)
        lm = np.asarray(im) > 0
        k = by_id[p["id"]]
        idm = idx == k
        lay = lm & ~(placed_any & ~idm)
        uni = int((idm | lay).sum())
        rows[p["id"]] = {"class": p["class"], "iou": round(int((idm & lay).sum()) / uni, 3) if uni else None, "id_px": int(idm.sum()),
                         "containment": round(int((idm & lm).sum()) / max(int(idm.sum()), 1), 3) if idm.any() else None}
    vals = [r["iou"] for r in rows.values() if r["iou"] is not None and r["id_px"] >= 400]
    return {"median": round(float(np.median(vals)), 3), "n": len(vals), "rows": rows}


def check_a(idm, name_of):
    """visible screen m^2 of each deliverer opening, from the ID render"""
    A = jload(GV / "check_a.json")
    lvrows = {r["opening"]: r for r in A["rows"]}
    k_of = {v: k for k, v in name_of.items()}
    out = {}
    for op, cur in (("barrow_door", "curtain_barrow_door"), ("hall_great_door", "curtain_hall_great_door"),
                    ("sea_cave_mouth", "curtain_sea_cave_mouth")):
        px = int((idm == k_of[cur]).sum())
        out[op] = {"probe": "v (curtain id px)", "visible_px": px, "visible_m2": round(px / PPM_V1 ** 2, 2),
                   "lv_visible_px": lvrows[op]["visible_px"], "lv_visible_m2": lvrows[op]["visible_m2"],
                   "agree": abs(px - lvrows[op]["visible_px"]) <= max(0.02 * lvrows[op]["visible_px"], 200)}
    # horizontal probes: reproduce LV's probe polygons (bv2f_level_prep.py:213-233), z at the probe height
    L = jload(LV / "layout_v7c.json")
    M = {m["id"]: m for m in L["models"]}
    law = law7()
    H, W = idm.shape
    placed_models = [k for k, v in name_of.items() if v in M or v in OWN_CURTAIN or v.startswith("rock_outcrop")]

    def rect(c, rot, Ln, Wd, z):
        t = math.radians(rot)
        ax, ay = math.cos(t), math.sin(t)
        bx, by = -math.sin(t), math.cos(t)
        return [law(c[0] + ax * a + bx * b, c[1] + ay * a + by * b, z) for a, b in
                ((-Ln / 2, -Wd / 2), (Ln / 2, -Wd / 2), (Ln / 2, Wd / 2), (-Ln / 2, Wd / 2))]
    wm = M["wreck"]
    wf = next(f for f in L["features"] if f["id"] == "wreck_hull")
    gm = M["fallen_gable"]
    gt = math.radians(gm["faces_compass_deg"])
    gs = gm["size_m"]["w_local_x"]
    gc = (gm["pos"][0] + math.sin(gt) * gs * 0.2, gm["pos"][1] - math.cos(gt) * gs * 0.2)
    probes = {"wreck_rail": (rect(wm["pos"], wf["axis_rot_deg"], 0.7 * wm["size_m"]["w_local_x"], 0.45 * wm["size_m"]["d_local_z"], 0.4), "wreck"),
              "fallen_gable_breach": (rect(gc, gm["faces_compass_deg"], 4.0, 0.5 * gs, 0.5 * gm["size_m"]["h"]), "fallen_gable"),
              "mere_ice": ([law(x, y, 0.03) for x, y in L["mere"]["polygon"]], None)}
    for op, (poly, own) in probes.items():
        im = Image.new("L", (W, H), 0)
        ImageDraw.Draw(im).polygon([tuple(p) for p in poly], fill=255)
        pm = np.asarray(im) > 0
        occl = np.isin(idm, [k for k in placed_models if name_of[k] != own])
        vis = pm & ~occl
        out[op] = {"probe": "h (reproduced probe polygon; visible = not an occluding model)", "probe_px": int(pm.sum()),
                   "visible_px": int(vis.sum()), "visible_m2": round(int(vis.sum()) / PPM_V1 ** 2, 2),
                   "pct_of_probe": round(100.0 * vis.sum() / max(pm.sum(), 1), 1),
                   "lv_visible_px": lvrows[op]["visible_px"], "lv_reference_px": lvrows[op]["reference_px"],
                   "lv_visible_m2": lvrows[op]["visible_m2"], "lv_pct": lvrows[op]["pct_of_unoccluded"]}
    out["_faces_camera_note"] = {"wreck_rail": {"declared_openings.json": next(o for o in jload(GV / "declared_openings.json")["openings"] if o["id"] == "wreck_rail")["faces_camera"],
                                                "check_a.json": lvrows["wreck_rail"]["faces_camera"]}}
    return out


if __name__ == "__main__":
    man = jload(GV / "guide_manifest.json")
    idm = ids_v7c()
    lm = layout_masks(idm.shape)
    rows, name_of = iou_rows(idm, man["id_table"], lm)
    v1 = v1_like_for_like()
    vals = [r["iou"] for r in rows.values() if r["iou"] is not None and r["id_px"] > 0]
    missing = sorted(k for k, r in rows.items() if r["id_px"] == 0 and r["layout_px"] > 0)
    outside = sorted(k for k, r in rows.items() if r["layout_px"] == 0)
    layout_ids = {m["id"] for m in jload(LV / "layout_v7c.json")["models"]}
    extra = sorted(v["id"] for v in man["id_table"].values()
                   if v["piece"] in ("model", "group") and OWN_CURTAIN.get(v["id"], v["id"]) not in layout_ids)
    not_placed = sorted(m["id"] for m in jload(LV / "layout_v7c.json")["models"] if m["id"] not in lm)
    res = {"_what": "P6 Phase 1: LV's v7c ID render vs the layout_v7c polygons (PH, conductor task)",
           "inputs": {"ids": man["ids"], "layout": {"file": "fid/lv/layout_v7c.json", "sha256": sha256(LV / "layout_v7c.json")}},
           "bar_ruled_v1_p6b": 0.513, "bar_like_for_like_v1": v1["median"], "v1_like_for_like_n": v1["n"],
           "median_iou_v7c": round(float(np.median(vals)), 3) if vals else None, "n": len(vals),
           "objects": rows, "missing_from_render": missing, "outside_envelope": outside, "extra_in_render": extra,
           "layout_models_not_placed_by_design": not_placed, "check_a_independent": check_a(idm, name_of),
           "v1_like_for_like_rows": v1["rows"]}
    # v1 baselines by kind (like for like with v7c's kinds: v7c's guide carries no trees)
    v1r = v1["rows"]
    def med(sel):
        v = [r["iou"] for r in v1r.values() if r["iou"] is not None and r["id_px"] >= 400 and sel(r["class"])]
        return {"median": round(float(np.median(v)), 3) if v else None, "n": len(v)}
    res["v1_baselines"] = {"all": {"median": v1["median"], "n": v1["n"]},
                           "real_models_excl_trees": med(lambda c: c not in ("outcrop", "shore_rock", "mound", "birch")),
                           "primitives (prism = mesh)": med(lambda c: c in ("outcrop", "shore_rock", "mound")),
                           "trees": med(lambda c: c == "birch")}
    # v7c objects classed by what the render shows (diagnostic: the share of the layout prism the terrain covers)
    ground = np.isin(idm, [int(k) for k, v in man["id_table"].items() if v["piece"] == "ground"])
    for k, r in rows.items():
        m = lm[k]["mask"]
        r["layout_px_in_frame"] = int(m.sum())
        r["terrain_covers_share"] = round(float(ground[m].mean()), 3) if m.any() else None
        if r["layout_px_in_frame"] == 0:
            r["status"] = "outside the paint envelope"
        elif r["id_px"] == 0:
            r["status"] = "MISSING from the render"
        elif r["id_px"] < 0.1 * r["layout_visible_px"] and (r["terrain_covers_share"] or 0) >= 0.8:
            r["status"] = "HIDDEN/BURIED: terrain covers the layout prism"
        else:
            r["status"] = "rendered"
    ok = [r["iou"] for r in rows.values() if r["status"] == "rendered"]
    res["containment_v7c_rendered"] = {k: r["containment"] for k, r in rows.items() if r["status"] == "rendered"}
    res["containment_v7c_median"] = round(float(np.median(list(res["containment_v7c_rendered"].values()))), 3) if ok else None
    cv1 = [r["containment"] for r in v1r.values() if r["containment"] is not None and r["id_px"] >= 400 and r["class"] != "birch"]
    res["containment_v1_median_excl_trees"] = round(float(np.median(cv1)), 3) if cv1 else None
    res["median_iou_v7c_rendered"] = round(float(np.median(ok)), 3) if ok else None
    res["n_rendered"] = len(ok)
    res["below_like_for_like_bar"] = sorted(k for k, r in rows.items() if r["iou"] is not None and r["id_px"] > 0 and r["iou"] < v1["median"])
    res["glb_missing_in_level"] = jload(BF / "godot/data/bv2f/v7c/level.json")["sim"].get("glb_missing")
    dump(res, str(PH / "results/p6_phase1_v7c.json"))
    print("containment v7c median %s, v1 median (excl trees) %s" % (res["containment_v7c_median"], res["containment_v1_median_excl_trees"]))
    print("rendered median %s (n %d); v1 baselines %s" % (res["median_iou_v7c_rendered"], res["n_rendered"], res["v1_baselines"]))
    for k, r in rows.items():
        if r["status"] != "rendered":
            print("  ", k, r["status"], "terrain share", r["terrain_covers_share"])
    print("v7c median IoU %s over %d objects; v1 like-for-like median %s (n %d); ruled bar 0.513" % (res["median_iou_v7c"], res["n"], v1["median"], v1["n"]))
    for k, r in sorted(rows.items(), key=lambda kv: (kv[1]["iou"] is None, kv[1]["iou"] or 0)):
        print("  %-18s IoU %-6s id_px %8d layout_vis %8d pieces %d" % (k, r["iou"], r["id_px"], r["layout_visible_px"], r["pieces"]))
    print("missing:", missing, "extra:", extra, "not placed by design:", not_placed)
    for k, v in res["check_a_independent"].items():
        print("check(a)", k, v)
