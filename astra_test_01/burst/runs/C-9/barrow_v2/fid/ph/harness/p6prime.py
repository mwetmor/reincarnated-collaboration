#!/usr/bin/env python3
"""P6' -- the re-instrumented Phase-1 geometry row, exactly as PRE-REGISTERED in calibration.md § 15 (commit 45fb5eaac,
before any v7c re-read). Four components: PRESENCE, PLACEMENT, SCALE OF RECORD, EXTENT. IoU-vs-prism is reported,
non-binding, beside v1's like-for-like 0.635.

  p6prime.py calibrate      v1 (positive) + one RED per component  -> results/p6prime_calibration.json
  p6prime.py v7c            the current v7c                         -> results/p6prime_v7c.json
"""
import argparse
import copy
import importlib.util
import math
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p6_phase1 as Q

TERRAIN_HIDDEN_MAX = 0.50          # § 15 (1c), written rule
ANISO_MAX = 1.10                   # § 15 (3), principle 3
MIN_PX = 400                       # § 15 (2): v1 pieces with >= 400 ID px enter the bar
BY_DESIGN_WORDS = ("sunk", "buried", "laid flat", "half-sunk")
NON_MODEL_PREFIX = ("ground_", "blobs_", "curtain_", "stair_", "door_lintel", "door_post")


def _pw():
    spec = importlib.util.spec_from_file_location("pw_v1_readonly", BF / "tools/paint_world_prep.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def raster(shape, polys=(), tris=None, lines=()):
    H, W = shape
    im = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(im)
    for p in polys:
        if len(p) >= 3:
            dr.polygon([tuple(q) for q in p], fill=255)
    if tris is not None:
        P2, I = tris
        for t in I:
            q = P2[t]
            dr.polygon([tuple(q[0]), tuple(q[1]), tuple(q[2])], fill=255)
    for a, b, w in lines:
        dr.line([a, b], fill=255, width=w)
    return np.asarray(im) > 0


# ====================================================================== v1
def v1_pieces():
    PW = _pw()
    idx, table = PW.id_index()
    L = jload(BF / "barrow_full_layout.json")
    by_id = {v["id"]: k for k, v in table.items()}
    C47, S47 = math.cos(math.radians(47)), math.sin(math.radians(47))
    pieces = []
    cache = {}
    for p in L["placements"]:
        b = p.get("built") or {}
        if "footprint_uv_low" not in b:
            continue
        rec = {"id": p["id"], "class": p["class"], "idx": by_id.get(p["id"])}
        y0, y1 = float(b.get("y_min", 0.0)), float(b.get("y_max", 0.0))
        rec["prism"] = Q.hull([PW.px_of_uv(u, v, h) for u, v in b["footprint_uv_low"] for h in (y0, y1)]) if b["footprint_uv_low"] else None
        glb = p.get("glb")
        if glb and glb.startswith("res://") and "fit_scale" in b:
            path = BF / "godot" / glb[len("res://"):]
            if path.exists():
                if str(path) not in cache:
                    cache[str(path)] = Q.glb_tris(path)
                V, I = cache[str(path)]
                vr = V * np.array(b["fit_scale"]) + np.array(b["fit_offset"])
                Bm = np.array(b["world_basis_columns"]).T          # columns -> matrix
                w = vr @ Bm.T + np.array(b["world_origin"])
                u = w[:, 0] * C47 - w[:, 2] * S47
                v = -w[:, 0] * S47 - w[:, 2] * C47
                px, py = PW.px_of_uv(u, v, w[:, 1])
                rec["own_tris"] = (np.stack([px, py], 1), I)
                if rec["prism"] is None:
                    # § 16 A1: a piece wholly above 1.9 m (lintel, raven) has an EMPTY footprint_uv_low; its slot prism
                    # is the convex hull of its own placed vertices over its y range
                    uv = list(zip(u, v))
                    rec["prism"] = Q.hull([PW.px_of_uv(a_, b_, h) for a_, b_ in Q.hull(uv) for h in (y0, y1)])
                    rec["prism_from"] = "A1: own placed vertices (empty footprint_uv_low)"
        if rec["prism"] is None:
            continue
        if "own_tris" not in rec:
            rec["own_poly"] = rec["prism"]                     # procedural primitives: the slab prism IS the piece
        rec["fit_scale"] = b.get("fit_scale")
        rec["pitch_correct"] = bool(p.get("pitch_correct"))
        rec["pitch_stretch"] = b.get("pitch_stretch")
        pieces.append(rec)
    return idx, table, pieces


def own_mask(shape, r):
    if "own_tris" in r:
        return raster(shape, tris=r["own_tris"])
    return raster(shape, polys=[r["own_poly"]])


def v1_components(shift_px=0):
    idx, table, pieces = v1_pieces()
    shape = idx.shape
    layout_ids = {p["id"] for p in jload(BF / "barrow_full_layout.json")["placements"]}
    known = {k for k, v in table.items() if v["id"] in layout_ids}
    out = {"objects": {}}
    present = set(np.unique(idx).tolist()) - {0}
    out["missing"] = sorted(r["id"] for r in pieces if r["idx"] not in present)
    out["extra"] = sorted(v["id"] for k, v in table.items() if k in present and k not in known and v.get("class") not in (None, "ground"))
    ground = idx == 0
    for r in pieces:
        k = r["idx"]
        idm = idx == k
        prism = raster(shape, polys=[[(x + shift_px, y) for x, y in r["prism"]]])
        own = own_mask(shape, r)
        n = int(idm.sum())
        o = int(own.sum())
        row = {"class": r["class"], "id_px": n, "prism_from": r.get("prism_from", "footprint_uv_low x y range"),
               "containment": round(float((idm & prism).sum() / n), 4) if n else None,
               "terrain_hidden_share": round(float((own & ground).sum() / max(o, 1)), 4) if o else None,
               "id_in_own_silhouette": round(float((idm & own).sum() / n), 4) if n else None}
        s = r["fit_scale"]
        if s:
            s = list(s)
            if r["pitch_correct"] and r["pitch_stretch"]:
                s[1] /= float(r["pitch_stretch"])
            row["anisotropy"] = round(max(s) / min(s), 4)
        else:
            row["anisotropy"] = "N/A (procedural primitive, not normalised)"
        out["objects"][r["id"]] = row
    return out


def v1_extent():
    acc = jload(BF / "barrow_full_layout.json")["acceptance"]
    rows = {}
    def walk(k, v):
        if isinstance(v, dict):
            if "PASS" in v:
                rows.setdefault(k, []).append(bool(v["PASS"]))
            for kk, vv in v.items():
                walk(k, vv)
        elif isinstance(v, list):
            for x in v:
                walk(k, x)
    for key in ("placements", "no_squeezes", "door", "mound_and_door_floor", "flood_fill", "walks"):
        if key in acc:
            walk(key, acc[key])
    flat = {k: all(v) for k, v in rows.items()}
    return {"source": "barrow_full_layout.json acceptance (finalize.py, computed from the built models' own footprints)",
            "checks": flat, "n_pass_flags": sum(len(v) for v in rows.values()), "pass": all(flat.values()) and bool(flat)}


# ====================================================================== v7c
def placed_beam(m, ins, cache):
    """sim (x, y, z) of a BEAM instance's mesh as bv2f_level.gd _place_beam places it (level frame X = x, Y = z, Z = y)"""
    g = ins.get("glb") or m.get("glb")
    p = Q._glb_path(g) if g else None
    if p is None or not p.exists():
        return None
    if str(p) not in cache:
        cache[str(p)] = Q.glb_tris(p)
    V, I = cache[str(p)]
    mn, mx = V.min(0), V.max(0)
    sz = mx - mn
    a = np.array([ins["a"][0], ins["a"][2], ins["a"][1]], float)
    b = np.array([ins["b"][0], ins["b"][2], ins["b"][1]], float)
    d = b - a
    ln = float(np.linalg.norm(d))
    if str(ins.get("fit", "")) == "height":
        s_ = ln / max(sz[1], 1e-3)
        vm = V - np.array([mn[0] + sz[0] / 2, mn[1], mn[2] + sz[2] / 2])
        W = vm * s_ + a
    else:
        k = 0
        if sz[1] > sz[k]:
            k = 1
        if sz[2] > sz[k]:
            k = 2
        zz = d / max(ln, 1e-3)
        xx = np.cross([0.0, 1.0, 0.0], zz)
        xx = np.array([1.0, 0.0, 0.0]) if np.linalg.norm(xx) < 0.05 else xx / np.linalg.norm(xx)
        yy = np.cross(zz, xx)
        yy /= np.linalg.norm(yy)
        th = float(ins["thickness_m"])
        others = [i for i in range(3) if i != k]
        cols = [None, None, None]
        cols[k] = zz * (ln / max(sz[k], 1e-3))
        cols[others[0]] = xx * (th / max(sz[others[0]], 1e-3))
        cols[others[1]] = yy * (th / max(sz[others[1]], 1e-3))
        B = np.stack(cols, 1)                       # columns
        vm = V - (mn + sz / 2)
        W = vm @ B.T + (a + b) / 2
    return np.stack([W[:, 0], W[:, 2], W[:, 1]], 1), I


def placed_procedural_beam(ins, n=10):
    """R-C9-181 _place_primitive_beam: a cylinder of diameter thickness_m along a->b (a post: cone tip within the length);
    vertices of the cylinder's two end rings (sim x, y, z) -- its convex hull is its silhouette"""
    a = np.array(ins["a"], float)
    b = np.array(ins["b"], float)
    d = b - a
    ln = float(np.linalg.norm(d))
    zz = d / max(ln, 1e-6)
    up = np.array([0.0, 0.0, 1.0])
    xx = np.cross(up, zz)
    xx = np.array([1.0, 0.0, 0.0]) if np.linalg.norm(xx) < 0.05 else xx / np.linalg.norm(xx)
    yy = np.cross(zz, xx)
    r = float(ins["thickness_m"]) / 2
    pts = []
    for e in (a, b):
        for k in range(n):
            t = 2 * math.pi * k / n
            pts.append(e + r * (math.cos(t) * xx + math.sin(t) * yy))
    return np.array(pts), None


def placed_vertices(m, ins, cache):
    """sim (x, y, z) of an instance's mesh as bv2f_level.gd _place_box places it (or the brazier stand-in)"""
    if ins.get("type") == "beam" and ins.get("procedural"):
        return placed_procedural_beam(ins)
    if ins.get("type") == "beam":
        return placed_beam(m, ins, cache)
    g = ins.get("glb") or m.get("glb")
    p = Q._glb_path(g) if g else None
    w, d, h = ins["size_m"]
    t = math.radians(float(ins["godot_rot_y_deg"]))
    if p is None or not p.exists():
        if m["id"] != "braziers":
            return None
        # stand-in: stand r 0.2 x 1.5 m + bowl r 0.55 x 0.8 m (AABB 1.1 x 2.3 x 1.1), scaled to the slot
        loc = np.array([[sx * r, y, sz * r] for r, y0, y1 in ((0.2, 0.0, 1.5), (0.55, 1.5, 2.3))
                        for y in (y0, y1) for sx in (-1, 1) for sz in (-1, 1)], float)
        loc = loc * np.array([w / 1.1, h / 2.3, d / 1.1])
        I = None
    else:
        if str(p) not in cache:
            cache[str(p)] = Q.glb_tris(p)
        V, I = cache[str(p)]
        if ins.get("lie_z90"):                      # R-C9-181: node rotation (0, 0, PI/2) inside a wrap, before the fit
            V = np.stack([-V[:, 1], V[:, 0], V[:, 2]], 1)
        mn, mx = V.min(0), V.max(0)
        sz = mx - mn
        sc = np.array([w / max(sz[0], 1e-6), h / max(sz[1], 1e-6), d / max(sz[2], 1e-6)])
        loc = (V - np.array([mn[0] + sz[0] / 2, mn[1], mn[2] + sz[2] / 2])) * sc
    X = loc[:, 0] * math.cos(t) + loc[:, 2] * math.sin(t)
    Z = -loc[:, 0] * math.sin(t) + loc[:, 2] * math.cos(t)
    return np.stack([ins["pos"][0] + X, ins["pos"][1] + Z, float(ins["z"]) + loc[:, 1]], 1), I


def _instances(m):
    insts = m.get("instances") or []
    if insts:
        return insts
    if not m.get("glb"):
        return []
    s = m["size_m"]
    return [{"type": "box", "pos": m["pos"], "z": m["z"], "godot_rot_y_deg": m["godot_rot_y_deg"],
             "size_m": [s["w_local_x"], s["d_local_z"], m.get("aabb_h_m", s["h"])], "glb": m.get("glb")}]


def v7c_components(layout_path=None, ids=None):
    layout_path = layout_path or (Q.LV / "layout_v7c.json")
    L = jload(layout_path)
    man = jload(Q.GV / "guide_manifest.json")
    idm = Q.ids_v7c() if ids is None else ids
    shape = idm.shape
    law = Q.law7()
    env = man["envelope"]
    lvl = jload(BF / "godot/data/bv2f/v7c/level.json")
    skip = set(lvl["sim"].get("skip_models", []))
    name_of = {int(k): v["id"] for k, v in man["id_table"].items()}
    kinds = {v["id"]: v["piece"] for v in man["id_table"].values()}
    ground = np.isin(idm, [int(k) for k, v in man["id_table"].items() if v["piece"] == "ground"])
    present_ids = set(np.unique(idm).tolist()) - {0}
    lm = Q.layout_masks(shape)
    cache = {}
    out = {"objects": {}, "by_design_exclusions": {}, "instances": {}}
    for m in L["models"]:
        mid = m["id"]
        insts = _instances(m)
        if mid in skip:
            out["by_design_exclusions"][mid] = "level skip_models (no plants in the guide)"
            continue
        if not insts:
            out["by_design_exclusions"][mid] = "no mesh of its own: %s" % m.get("status", "")[:90]
            continue
        ks = [k for k, n in name_of.items() if Q.OWN_CURTAIN.get(n, n) == mid]
        idmask = np.isin(idm, ks) if ks else np.zeros(shape, bool)
        own_all = np.zeros(shape, bool)
        inst_rows = []
        for i, ins in enumerate(insts):
            if False:
                pass
            else:
                pv = placed_vertices(m, ins, cache)
                if pv is None:
                    inst_rows.append({"i": i, "type": ins["type"], "unplaceable": True})
                    continue
                Vw, I = pv
                xs = (Vw[:, 0] - env["u"][0]) * PPM_V1
                ys = (env["v"][1] + Vw[:, 1]) * Q.PXV - Vw[:, 2] * Q.PXH
                P2 = np.stack([xs, ys], 1)
                own = raster(shape, tris=(P2, I)) if I is not None else raster(shape, polys=[Q.hull(list(map(tuple, P2)))])
                inst_rows.append({"i": i, "type": ins["type"], "z_top": round(float(Vw[:, 2].max()), 3), "verts": Vw if mid == "longhall" else None,
                                  "footprint_hull": [list(map(float, q)) for q in Q.hull(list(map(tuple, Vw[:, :2])))]})
            n_own = int(own.sum())
            r = inst_rows[-1]
            r["own_px_in_frame"] = n_own
            if n_own:
                r["terrain_hidden_share"] = round(float((own & ground).sum() / n_own), 4)
                r["visible_share"] = round(float((own & idmask).sum() / n_own), 4)
            own_all |= own
        n = int(idmask.sum())
        declared = {i for i, ins in enumerate(insts) if ins.get("burial_by_design")} | ({*range(len(insts))} if m.get("burial_by_design") else set())
        design = sorted(declared)
        hid_all = [r for r in inst_rows if r.get("own_px_in_frame") and r.get("terrain_hidden_share", 0) > TERRAIN_HIDDEN_MAX]
        hid = [r for r in hid_all if r["i"] not in declared]
        out.setdefault("hidden_by_design", {})
        for r in hid_all:
            if r["i"] in declared:
                out["hidden_by_design"].setdefault(mid, []).append({"instance": r["i"], "terrain_hidden_share": r["terrain_hidden_share"],
                                                                   "declaration": (insts[r["i"]].get("burial_by_design") or m.get("burial_by_design"))[:160]})
        in_frame = int(own_all.sum()) > 0
        row = {"kind": m.get("kind"), "instances": len(insts), "id_px": n, "in_frame": in_frame,
               "missing": in_frame and n == 0,
               "terrain_hidden_instances": [(r["i"], r["terrain_hidden_share"]) for r in hid],
               "burial_by_design_instances": design,
               "containment": round(float((idmask & lm[mid]["mask"]).sum() / n), 4) if (n and mid in lm) else None,
               "iou_vs_prism_reported": None}
        if n and mid in lm:
            lay = lm[mid]["mask"]
            row["iou_vs_prism_reported"] = round(float((idmask & lay).sum() / max((idmask | lay).sum(), 1)), 3)
        out["objects"][mid] = row
        out["instances"][mid] = inst_rows
    model_ids = {m["id"] for m in L["models"]}
    out["extra"] = sorted(n for k, n in name_of.items() if k in present_ids and kinds[n] in ("model", "group")
                          and Q.OWN_CURTAIN.get(n, n) not in model_ids and not n.startswith(NON_MODEL_PREFIX))
    out["non_model_ids_excluded"] = sorted(n for n in name_of.values() if n.startswith(NON_MODEL_PREFIX))
    out["missing"] = sorted(k for k, r in out["objects"].items() if r["missing"])
    return out, L, cache


def v7c_scale(L, cache):
    """LV's per-instance record (fid/lv/placed_fit_v7c.json) + PH's cross-check size / GLB AABB"""
    rec = jload(Q.LV / "placed_fit_v7c.json")
    rows = []
    by_slot = {}
    for r in rec["instances"]:
        by_slot.setdefault(r["slot"], []).append(r)
    M = {m["id"]: m for m in L["models"]}
    for slot, rr in by_slot.items():
        m = M.get(slot)
        insts = _instances(m) if m else []
        boxes = [i for i in insts if i["type"] == "box"]
        for j, r in enumerate(rr):
            row = {"slot": slot, "instance": r["instance"], "kind": r["kind"], "recorded_fit_scale": r["fit_scale_xyz"],
                   "anisotropy": r["anisotropy_max_over_min"], "pass": r["anisotropy_max_over_min"] <= ANISO_MAX}
            if str(r["kind"]).startswith("procedural"):
                row["anisotropy"] = 1.0
                row["note"] = "N/A: procedural primitive at true dimensions, no model normalised (as § 15 (3) for v1's slabs)"
            if r["kind"] == "box" and m is not None and j < len(boxes):
                ins = boxes[j]
                g = ins.get("glb") or m.get("glb")
                p = Q._glb_path(g) if g else None
                if p is not None and p.exists():
                    if str(p) not in cache:
                        cache[str(p)] = Q.glb_tris(p)
                    V, _ = cache[str(p)]
                    if ins.get("lie_z90"):
                        V = np.stack([-V[:, 1], V[:, 0], V[:, 2]], 1)
                    sz = V.max(0) - V.min(0)
                    w, d, h = ins["size_m"]
                    mine = [w / sz[0], h / sz[1], d / sz[2]]
                    row["ph_size_over_aabb"] = [round(x, 4) for x in mine]
                    row["record_agrees_1pct"] = all(abs(a - b) <= 0.01 * max(abs(b), 1e-6) for a, b in zip(r["fit_scale_xyz"], mine))
            rows.append(row)
    return rows


def r11_per_region(L2, inst_geo, replaced):
    """R-C9-181 (3): R11 read PER REGION of the one hall + porch mesh: porch h = max placed z inside hall_porch's
    r11_region_footprint; hall body h = max placed z outside it. Written into the layout copy's slot heights."""
    from matplotlib.path import Path
    M = {m["id"]: m for m in L2["models"]}
    hp = M.get("hall_porch")
    g = inst_geo.get("longhall")
    if not hp or not hp.get("r11_region_footprint") or not g or "verts" not in g[0]:
        return None
    Vw = g[0]["verts"]
    inside = Path(np.array(hp["r11_region_footprint"])).contains_points(Vw[:, :2])
    z0 = float(M["longhall"]["z"])
    h_porch = float(Vw[inside, 2].max()) - z0
    h_body = float(Vw[~inside, 2].max()) - z0
    M["longhall"]["size_m"]["h"] = round(h_body, 3)
    hp["size_m"]["h"] = round(h_porch, 3)
    replaced["R11_per_region"] = {"porch_h": round(h_porch, 3), "hall_body_h": round(h_body, 3),
                                  "n_verts_porch_region": int(inside.sum()), "n_verts_body": int((~inside).sum())}
    return replaced["R11_per_region"]


def extent_run(L, inst_geo, label, per_region=True):
    """§ 15 (4): the validator on a PH copy of the layout with every single-placement model's slot replaced by its own
    placed geometry (footprint = convex hull of placed vertices, h = max z - slot z); features of the same id (and
    wreck_hull -> wreck) take the same footprint. Box instances: own extents == the box by construction (_place_box
    scales the AABB to the box) -- verified, left as is."""
    L2 = copy.deepcopy(L)
    replaced = {}
    feat_of = {"wreck": "wreck_hull"}
    F = {f["id"]: f for f in L2["features"]}
    for m in L2["models"]:
        if m.get("instances") or m["id"] not in inst_geo:
            continue
        g = inst_geo[m["id"]]
        if not g or "footprint_hull" not in g[0]:
            continue
        fp = g[0]["footprint_hull"]
        h = g[0]["z_top"] - float(m["z"])
        m["footprint"] = fp
        m["size_m"]["h"] = round(h, 3)
        replaced[m["id"]] = {"footprint_pts": len(fp), "h": round(h, 3)}
        fid = feat_of.get(m["id"], m["id"])
        if fid in F:
            F[fid]["footprint"] = fp
            F[fid]["z_top_m"] = round(float(F[fid].get("z_bottom_m", 0.0)) + h, 3)
            replaced[m["id"]]["feature"] = fid
    if per_region:
        r11_per_region(L2, inst_geo, replaced)
    return run_validator(L2, label), replaced


def run_validator(L2, label):
    d = PH / "results" / "p6prime_extent"
    d.mkdir(parents=True, exist_ok=True)
    lp = d / ("layout_%s.json" % label)
    dump(L2, str(lp))
    jp = d / ("validator_%s.json" % label)
    r = subprocess.run([sys.executable, str(Q.LV / "tools/validate_layout_v7.py"), str(lp), "--json", str(jp)],
                       capture_output=True, text=True, cwd=str(Q.LV))
    res = jload(jp) if jp.exists() else {}
    fails = []
    for c in res.get("checks", res.get("results", [])):
        if isinstance(c, dict) and not c.get("pass", c.get("PASS", True)):
            fails.append({k: c.get(k) for k in ("rule", "check") if k in c})
    return {"exit": r.returncode, "fails": fails, "n_checks": len(res.get("checks", res.get("results", []))),
            "stdout_tail": r.stdout.strip().splitlines()[-3:]}


# ====================================================================== calibration
def calibrate():
    out = {"_what": "P6' calibration (calibration.md § 15 pre-registration, commit 45fb5eaac)"}
    v1 = v1_components()
    big = {k: r for k, r in v1["objects"].items() if r["id_px"] >= MIN_PX and r["containment"] is not None}
    bar_cont = min(r["containment"] for r in big.values())
    worst = min(big, key=lambda k: big[k]["containment"])
    th = [r["terrain_hidden_share"] for r in v1["objects"].values() if r["terrain_hidden_share"] is not None]
    an = [r["anisotropy"] for r in v1["objects"].values() if isinstance(r["anisotropy"], float)]
    v1x = v1_extent()
    out["bars"] = {"presence_missing": 0, "presence_extra": 0, "terrain_hidden_share_max": TERRAIN_HIDDEN_MAX,
                   "containment_min": bar_cont, "containment_min_from": worst, "anisotropy_max": ANISO_MAX,
                   "extent": "every R1-R13 check passes"}
    out["v1"] = {"missing": v1["missing"], "extra": v1["extra"],
                 "terrain_hidden_share_max_observed": max(th) if th else None,
                 "containment_min": bar_cont, "anisotropy_max_observed": max(an) if an else None,
                 "id_in_own_silhouette_median": round(float(np.median([r["id_in_own_silhouette"] for r in big.values()])), 4),
                 "extent": v1x}
    out["v1"]["pass"] = {"presence": not v1["missing"] and not v1["extra"] and (max(th) if th else 0) <= TERRAIN_HIDDEN_MAX,
                         "placement": True, "scale": (max(an) if an else 0) <= ANISO_MAX, "extent": v1x["pass"]}
    out["v1_objects"] = v1["objects"]
    # RED 1 presence: v7c at 2a913e7af, its recorded result
    old = json.loads(subprocess.run(["git", "-C", str(C9.parents[3]), "show",
                                     "2a913e7af:astra_test_01/burst/runs/C-9/barrow_v2/fid/ph/results/p6_phase1_v7c.json"],
                                    capture_output=True, text=True).stdout)
    hidden_old = {k: r for k, r in old["objects"].items() if str(r.get("status", "")).startswith("HIDDEN")}
    out["red_presence_v7c_2a913e7af"] = {"missing": old["missing_from_render"],
                                         "hidden_by_terrain_recorded": {k: r["terrain_covers_share"] for k, r in hidden_old.items()},
                                         "pass": not old["missing_from_render"] and not hidden_old}
    # RED 2 placement: v1 with every slot prism shifted 1.5 m (151 px) across
    sh = v1_components(shift_px=int(round(1.5 * PPM_V1)))
    fails = {k: r["containment"] for k, r in sh["objects"].items() if r["id_px"] >= MIN_PX and r["containment"] is not None and r["containment"] < bar_cont}
    out["red_placement_shift_1p5m"] = {"objects_below_bar": len(fails), "of": len(big),
                                       "examples": dict(sorted(fails.items(), key=lambda kv: kv[1])[:5]), "pass": not fails}
    # RED 3 scale: v6's 3 m porch -- layout v6 hall_porch slot against the hall_porch GLB
    v6 = jload(B2 / "layout_v2.json")
    hp = next(m for m in v6["models"] if m["id"] == "hall_porch")
    V, _ = Q.glb_tris(B2 / hp["glb"])
    sz = V.max(0) - V.min(0)
    s = hp["size_m"]
    sc = [s["w_local_x"] / sz[0], s["h"] / sz[1], s["d_local_z"] / sz[2]]
    a = max(sc) / min(sc)
    out["red_scale_v6_porch"] = {"slot_m": [s["w_local_x"], s["h"], s["d_local_z"]], "glb_aabb_m": [round(float(x), 3) for x in sz],
                                 "fit_scale": [round(float(x), 4) for x in sc], "anisotropy": round(float(a), 3), "pass": bool(a <= ANISO_MAX)}
    # RED 4 extent: the v7c layout with the fallen gable shrunk to 40% about its far point (away from the floor)
    L = jload(Q.LV / "layout_v7c.json")
    L2 = copy.deepcopy(L)
    f = next(x for x in L2["features"] if x["id"] == "fallen_gable")
    fl = np.array(L2["floor"]["polygon"])
    pts = np.array(f["footprint"], float)
    far = pts[np.argmax([np.min(np.hypot(*(fl - p).T)) for p in pts])]
    f["footprint"] = (far + 0.4 * (pts - far)).round(4).tolist()
    for m in L2["models"]:
        if m["id"] == "fallen_gable":
            m["footprint"] = f["footprint"]
    base = run_validator(L, "v7c_as_layout")
    red = run_validator(L2, "red_gable_shrunk")
    out["red_extent_gable_shrunk"] = {"layout_baseline": base, "shrunk": red,
                                      "r10_failed": any("R10" in json.dumps(x) for x in red["fails"]), "pass": red["exit"] == 0}
    out["v1_like_for_like_iou_vs_prism_reported"] = 0.635
    dump(out, str(PH / "results/p6prime_calibration.json"))
    return out


def run_v7c(bars):
    comp, L, cache = v7c_components()
    scale = v7c_scale(L, cache)
    ext, replaced = extent_run(L, comp["instances"], "v7c_r181_own_geometry")
    for rows_ in comp["instances"].values():
        for r_ in rows_:
            r_.pop("verts", None)
    objs = comp["objects"]
    hidden = {k: r["terrain_hidden_instances"] for k, r in objs.items() if r["terrain_hidden_instances"]}
    place_fail = {k: r["containment"] for k, r in objs.items() if r["containment"] is not None and r["containment"] < bars["containment_min"]}
    scale_fail = [r for r in scale if not r["pass"]]
    rec_bad = [r for r in scale if r.get("record_agrees_1pct") is False]
    res = {"_what": "P6' on v7c (pre-registered calibration.md § 15; bars from p6prime_calibration.json)",
           "inputs": {"ids_sha256": sha256(Q.GV / "ids_v7c.png"), "layout_sha256": sha256(Q.LV / "layout_v7c.json"),
                      "placed_fit_sha256": sha256(Q.LV / "placed_fit_v7c.json")},
           "presence": {"missing": comp["missing"], "extra": comp["extra"], "terrain_hidden_not_by_design": hidden,
                        "hidden_by_design_accepted": comp.get("hidden_by_design", {}),
                        "by_design_rule": "accepted only where the layout declares the burial; provenance (I-R2, R-C9-182): circle_stones recorded 'laid flat, sunk flush: top 0.12 m' at d4c59061f, required by R13 (R-C9-155); declared on all 8",
                        "by_design_exclusions": comp["by_design_exclusions"], "non_model_ids_excluded": comp["non_model_ids_excluded"],
                        "pass": not comp["missing"] and not comp["extra"] and not hidden},
           "placement": {"bar": bars["containment_min"], "below_bar": place_fail,
                         "containment": {k: r["containment"] for k, r in objs.items()}, "pass": not place_fail},
           "scale": {"bar": ANISO_MAX, "n_instances": len(scale), "n_over": len(scale_fail),
                     "over_by_slot": {}, "record_mismatches_vs_ph": len(rec_bad), "pass": not scale_fail and not rec_bad},
           "extent": {"validator": ext, "replaced": replaced, "pass": ext["exit"] == 0},
           "iou_vs_prism_reported_non_binding": {k: r["iou_vs_prism_reported"] for k, r in objs.items()},
           "iou_vs_prism_median_reported": round(float(np.median([r["iou_vs_prism_reported"] for r in objs.values() if r["iou_vs_prism_reported"] is not None])), 3),
           "v1_like_for_like_reported": 0.635, "objects": objs, "scale_rows": scale}
    for r in scale_fail:
        res["scale"]["over_by_slot"].setdefault(r["slot"], []).append(round(r["anisotropy"], 3))
    res["P6prime_pass"] = all(res[c]["pass"] for c in ("presence", "placement", "scale", "extent"))
    dump(res, str(PH / "results/p6prime_v7c.json"))
    return res


def recheck_reds_r181():
    """R-C9-181: the calibration REDs re-read with the SAME pipeline changes applied to v7c (per-region R11; lying /
    procedural geometry) -- each must still fail. Bars unchanged (results/p6prime_calibration.json)."""
    out = {}
    # v6's 3 m porch: scale of record (the per-region R11 reading is a HEIGHT reading; it cannot change a fit scale)
    v6 = jload(B2 / "layout_v2.json")
    M6 = {m["id"]: m for m in v6["models"]}
    hp = M6["hall_porch"]
    V, _ = Q.glb_tris(B2 / hp["glb"])
    sz = V.max(0) - V.min(0)
    s_ = hp["size_m"]
    sc = [s_["w_local_x"] / sz[0], s_["h"] / sz[1], s_["d_local_z"] / sz[2]]
    a = max(sc) / min(sc)
    # the per-region R11 reading on v6: there the porch is its OWN model, so its region height is its own placed height
    out["red_scale_v6_porch_r181"] = {"anisotropy": round(float(a), 3), "pass": bool(a <= ANISO_MAX),
                                      "r11_per_region_on_v6": {"porch_h": s_["h"], "hall_body_h": M6["longhall"]["size_m"]["h"],
                                                               "note": "v6's porch is a separate model: per-region = per-model; R11 reads 11.3 vs 6.5 (passes) -- the RED is the scale component, unchanged"}}
    # the shrunk gable, run through the same own-geometry + per-region extent pipeline as v7c
    L = jload(Q.LV / "layout_v7c.json")
    comp, _, _ = v7c_components()
    L2 = copy.deepcopy(L)
    f = next(x for x in L2["features"] if x["id"] == "fallen_gable")
    fl = np.array(L2["floor"]["polygon"])
    pts = np.array(f["footprint"], float)
    far = pts[np.argmax([np.min(np.hypot(*(fl - q).T)) for q in pts])]
    def shrink(P):
        P = np.array(P, float)
        return (far + 0.4 * (P - far)).round(4).tolist()
    f["footprint"] = shrink(f["footprint"])
    geo = copy.deepcopy(comp["instances"])
    if geo.get("fallen_gable") and "footprint_hull" in geo["fallen_gable"][0]:
        geo["fallen_gable"][0]["footprint_hull"] = shrink(geo["fallen_gable"][0]["footprint_hull"])
    ext, rep = extent_run(L2, geo, "red_gable_shrunk_r181")
    out["red_extent_gable_shrunk_r181"] = {"validator": ext, "r11_per_region": rep.get("R11_per_region"),
                                           "r10_failed": any("R10" in json.dumps(x) for x in ext["fails"]), "pass": ext["exit"] == 0}
    dump(out, str(PH / "results/p6prime_reds_r181.json"))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["calibrate", "v7c", "reds_r181"])
    a = ap.parse_args()
    if a.what == "calibrate":
        r = calibrate()
        print(json.dumps({k: v for k, v in r.items() if k != "v1_objects"}, indent=1, default=str)[:6000])
    elif a.what == "reds_r181":
        print(json.dumps(recheck_reds_r181(), indent=1, default=str)[:3000])
    else:
        bars = jload(PH / "results/p6prime_calibration.json")["bars"]
        r = run_v7c(bars)
        print(json.dumps({k: r[k] for k in ("presence", "placement", "extent", "iou_vs_prism_median_reported", "P6prime_pass")}, indent=1, default=str)[:5000])
        print("scale:", {k: r["scale"][k] for k in ("n_instances", "n_over", "over_by_slot", "record_mismatches_vs_ph", "pass")})
