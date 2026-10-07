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


RUNS = C9.parent


def glb_tris(path):
    """positions (n, 3) and triangle indices (m, 3) of a single-node, single-mesh GLB (the normalised builds)"""
    import struct
    b = open(path, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + n])
    blob = b[20 + n + 8:]
    V, I = [], []
    base = 0
    for mesh in j["meshes"]:
        for pr in mesh["primitives"]:
            def acc(i):
                a = j["accessors"][i]
                bv = j["bufferViews"][a["bufferView"]]
                dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}[a["componentType"]]
                k = {"SCALAR": 1, "VEC3": 3}[a["type"]]
                off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
                stride = bv.get("byteStride")
                if stride and stride != np.dtype(dt).itemsize * k:
                    raw = np.frombuffer(blob, np.uint8, a["count"] * stride, off).reshape(a["count"], stride)
                    return raw[:, :np.dtype(dt).itemsize * k].copy().view(dt).reshape(a["count"], k)
                arr = np.frombuffer(blob, dt, a["count"] * k, off)
                return arr.reshape(a["count"], k) if k > 1 else arr
            v = acc(pr["attributes"]["POSITION"]).astype(np.float64)
            i = acc(pr["indices"]).astype(np.int64).reshape(-1, 3) if "indices" in pr else np.arange(len(v)).reshape(-1, 3)
            V.append(v)
            I.append(i + base)
            base += len(v)
    return np.concatenate(V), np.concatenate(I)


def _glb_path(g):
    if g.startswith("data/bv2f/"):
        return BF / "godot" / g
    if g.startswith("runs/"):
        return RUNS / g[5:]
    return B2 / g


def model_alone_masks(shape, lmasks):
    """each object's OWN silhouette, rendered alone (no occlusion): its GLB triangles placed exactly as
    bv2f_level.gd _place_box does (AABB bottom-centre to the slot origin, per-axis scale to the slot, yaw about up),
    projected and rasterised; beams = the drawn segment (the log fitted to it); the braziers' primitive stand-in
    (R-C9-178: a 0.4 m stand to 1.5 m, a 1.1 m bowl 1.5-2.3 m) as two boxes."""
    L = jload(LV / "layout_v7c.json")
    law = law7()
    H, W = shape
    out = {}
    cache = {}
    for m in L["models"]:
        if m["id"] not in lmasks:
            continue
        im = Image.new("L", (W, H), 0)
        dr = ImageDraw.Draw(im)
        insts = m.get("instances") or [{"type": "box", "pos": m["pos"], "z": m["z"], "godot_rot_y_deg": m["godot_rot_y_deg"],
                                        "size_m": [m["size_m"]["w_local_x"], m["size_m"]["d_local_z"], m.get("aabb_h_m", m["size_m"]["h"])],
                                        "glb": m.get("glb")}]
        for ins in insts:
            if ins["type"] != "box":
                a = law(*ins["a"])
                b = law(*ins["b"])
                dr.line([a, b], fill=255, width=max(1, int(round(float(ins["thickness_m"]) * PPM_V1))))
                continue
            g = ins.get("glb") or m.get("glb")
            p = _glb_path(g) if g else None
            if p is None or not p.exists():
                if m["id"] == "braziers":
                    t, (x, y), z = float(ins["godot_rot_y_deg"]), ins["pos"], float(ins["z"])
                    dr.polygon(box_hull(law, (x, y), z, t, 0.4, 0.4, 1.5), fill=255)
                    dr.polygon(box_hull(law, (x, y), z + 1.5, t, 1.1, 1.1, 0.8), fill=255)
                continue
            if str(p) not in cache:
                cache[str(p)] = glb_tris(p)
            V, I = cache[str(p)]
            mn, mx = V.min(0), V.max(0)
            sz = mx - mn
            w, d, h = ins["size_m"]
            sc = np.array([w / max(sz[0], 1e-6), h / max(sz[1], 1e-6), d / max(sz[2], 1e-6)])
            loc = (V - np.array([mn[0] + sz[0] / 2, mn[1], mn[2] + sz[2] / 2])) * sc
            t = math.radians(float(ins["godot_rot_y_deg"]))
            X = loc[:, 0] * math.cos(t) + loc[:, 2] * math.sin(t)
            Z = -loc[:, 0] * math.sin(t) + loc[:, 2] * math.cos(t)
            xs = ins["pos"][0] + X
            ys = ins["pos"][1] + Z
            zs = float(ins["z"]) + loc[:, 1]
            env = jload(GV / "guide_manifest.json")["envelope"]
            px = (xs - env["u"][0]) * PPM_V1
            py = (env["v"][1] + ys) * PXV - zs * PXH
            P2 = np.stack([px, py], 1)
            for tri in I:
                q = P2[tri]
                dr.polygon([tuple(q[0]), tuple(q[1]), tuple(q[2])], fill=255)
        out[m["id"]] = np.asarray(im) > 0
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


def _parea(q):
    n = len(q)
    return abs(sum(q[i][0] * q[(i + 1) % n][1] - q[(i + 1) % n][0] * q[i][1] for i in range(n))) / 2


def check_a(idm, name_of):
    """check (a) re-read with LV's OWN probe definition (level.json sim.openings[].probe, bv2f_level.gd _build_probes):
      (1) REFERENCE (unoccluded) projected px of each probe, computed analytically here from its definition
          (v: the w x h face at the centre, facing faces_deg, z0 up; h_rect: the L x W rectangle at z, L across the
          facing; poly: the mere polygon at z) -- against LV's reference_px from its probe_only render;
      (2) VISIBLE px recounted by PH from LV's own probe_with renders (guide_v7c/probe_with_<section>/ids.png, pad
          cropped, the probe ids from ids.json) -- against LV's visible_px;
      (3) the HALL-DOOR question: the ID render's dark curtain (id curtain_*) is a 0.3 m-deep box set curtain_inset_m
          behind the probe plane; its analytic box silhouette vs PH's first count (8.22 m2)."""
    A = jload(GV / "check_a.json")
    lvrows = {r["opening"]: r for r in A["rows"]}
    lvl = jload(BF / "godot/data/bv2f/v7c/level.json")
    ops = {o["id"]: o for o in lvl["sim"]["openings"]}
    law = law7()
    k_of = {v: k for k, v in name_of.items()}
    out = {}
    # (2) recount LV's probe_with / probe_only renders
    cnt = {"with": {}, "only": {}}
    for mode in cnt:
        for sec in lvl["frame"]["sections"]:
            d = GV / ("probe_%s_%s" % (mode, sec["id"]))
            pad = int(jload(LV / "v7c" / ("frame_grid_%s.json" % sec["id"])).get("pad_px", 0))
            sw, sh = sec["px"]
            a = np.asarray(Image.open(d / "ids.png").convert("RGB")).astype(np.int32)[pad:pad + sh, pad:pad + sw]
            code = (a[..., 0] << 16) | (a[..., 1] << 8) | a[..., 2]
            for rec in jload(d / "ids.json")["placements"].values():
                if rec["id"].startswith("probe_"):
                    r_, g_, b_ = rec["rgb"]
                    cnt[mode][rec["id"][6:]] = cnt[mode].get(rec["id"][6:], 0) + int((code == (r_ << 16 | g_ << 8 | b_)).sum())
    for oid, o in ops.items():
        pr = o["probe"]
        if pr["type"] == "v":
            t = math.radians(pr["faces_deg"])
            tx, ty = math.cos(t), math.sin(t)
            (cx, cy), w, h, z0 = pr["centre"], pr["w"], pr["h"], pr["z0"]
            q = [law(cx - tx * w / 2, cy - ty * w / 2, z0), law(cx + tx * w / 2, cy + ty * w / 2, z0),
                 law(cx + tx * w / 2, cy + ty * w / 2, z0 + h), law(cx - tx * w / 2, cy - ty * w / 2, z0 + h)]
            ref = _parea(q)
        elif pr["type"] == "h_rect":
            t = math.radians(pr["rot_deg"])
            ax, ay = math.cos(t), math.sin(t)
            bx, by = -math.sin(t), math.cos(t)
            (cx, cy), Ln, Wd, z = pr["centre"], pr["L"], pr["W"], pr["z"]
            q = [law(cx + ax * a_ + bx * b_, cy + ay * a_ + by * b_, z) for a_, b_ in
                 ((-Ln / 2, -Wd / 2), (Ln / 2, -Wd / 2), (Ln / 2, Wd / 2), (-Ln / 2, Wd / 2))]
            ref = _parea(q)
        else:
            ref = _parea([law(x, y, pr["z"]) for x, y in pr["polygon"]])
        lr = lvrows[oid]
        row = {"probe": pr["type"], "ref_px_analytic": int(round(ref)), "lv_reference_px": lr["reference_px"],
               "ref_agree_pct": round(100.0 * (ref - lr["reference_px"]) / lr["reference_px"], 2),
               "visible_px_recount": cnt["with"].get(oid), "lv_visible_px": lr["visible_px"],
               "only_px_recount": cnt["only"].get(oid),
               "visible_m2": round((cnt["with"].get(oid) or 0) / PPM_V1 ** 2, 2), "lv_visible_m2": lr["visible_m2"],
               "pct_of_unoccluded": round(100.0 * (cnt["with"].get(oid) or 0) / max(cnt["only"].get(oid) or 1, 1), 1),
               "lv_pct": lr["pct_of_unoccluded"], "visible": (cnt["with"].get(oid) or 0) > 0}
        cur = {"barrow_door": "curtain_barrow_door", "hall_great_door": "curtain_hall_great_door", "sea_cave_mouth": "curtain_sea_cave_mouth"}.get(oid)
        if cur and cur in k_of and pr["type"] == "v":
            ins = float(o.get("curtain_inset_m", 0.0))
            fx, fy = math.sin(t), -math.cos(t)
            ccx, ccy = cx - fx * ins, cy - fy * ins
            qq = []
            for dd in (0.15, -0.15):
                ox, oy = ccx + fx * dd, ccy + fy * dd
                qq += [law(ox - tx * w / 2, oy - ty * w / 2, z0), law(ox + tx * w / 2, oy + ty * w / 2, z0),
                       law(ox + tx * w / 2, oy + ty * w / 2, z0 + h), law(ox - tx * w / 2, oy - ty * w / 2, z0 + h)]
            row["curtain_id_px"] = int((idm == k_of[cur]).sum())
            row["curtain_box_0p3m_silhouette_px_analytic"] = int(round(_parea(hull(qq))))
        out[oid] = row
    out["_faces_camera"] = {o["id"]: {k: v for k, v in o.items() if "faces_camera" in k or k == "check_a_probe"}
                            for o in jload(GV / "declared_openings.json")["openings"]}
    out["_lv_faces_camera_in_check_a"] = {k: v.get("faces_camera") for k, v in lvrows.items()}
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
    # R-C9-178: ATTRIBUTION of each object's IoU residual (1 - IoU) -- no bar change proposed
    alone = model_alone_masks(idm.shape, lm)
    att = {}
    for k, r in rows.items():
        if k not in alone or r["status"] != "rendered":
            continue
        L_ = lm[k]["mask"]
        A_ = alone[k]
        iou_alone = float((A_ & L_).sum() / max((A_ | L_).sum(), 1))
        ks = r["ids"]
        idmask = np.isin(idm, ks)
        in_alone = float((idmask & A_).sum() / max(idmask.sum(), 1))
        hidden = float(1 - (idmask.sum() / max(A_.sum(), 1)))
        att[k] = {"iou_observed": r["iou"], "iou_model_alone_vs_prism": round(iou_alone, 3),
                  "organic_underfill": round(1 - iou_alone, 3),
                  "occlusion": round(max(iou_alone - (r["iou"] or 0), 0.0), 3),
                  "placement_outside_prism": round(1 - (r["containment"] or 0), 3),
                  "id_px_inside_model_alone_silhouette": round(in_alone, 3),
                  "model_alone_px_hidden_share": round(hidden, 3)}
    res["attribution_R_C9_178"] = {"_how": ("organic under-fill = 1 - IoU(the object's own GLB silhouette rendered alone, its layout "
                                            "prism); occlusion = IoU(alone) - IoU(observed); placement = the share of its ID pixels "
                                            "outside its own prism. id_px_inside_model_alone_silhouette ~ 1 confirms the render places "
                                            "the GLB exactly where the layout says"), "rows": att}
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
    for k, a in sorted(att.items(), key=lambda kv: kv[1]["iou_observed"] or 0):
        print("ATT %-16s obs %.3f alone %.3f underfill %.3f occl %.3f place %.3f in_alone %.3f" % (k, a["iou_observed"], a["iou_model_alone_vs_prism"],
              a["organic_underfill"], a["occlusion"], a["placement_outside_prism"], a["id_px_inside_model_alone_silhouette"]))
