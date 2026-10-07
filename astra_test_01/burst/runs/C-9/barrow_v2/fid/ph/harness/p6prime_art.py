#!/usr/bin/env python3
"""P6' on LV's ART blockout (charter § 15/15.1, R-C9-185/186): presence / placement / scale against the geometry of
record fid/lv/art/layout_bv2art.json, with the FROZEN bars of results/p6prime_calibration.json (extent retired).
  p6prime_art.py        -> results/p6prime_art.json  (+ the I-4 constructed 1.5 m-shift RED on bv2art)

The level's slot data (barrow_full/godot/data/bv2f/art/level.json sim.models, written by bv2f_level_prep from the layout)
is what bv2f_level.gd places; it is CROSS-CHECKED here against layout_bv2art.json placement by placement (u, v, z, size,
uniform scale) before any measurement, so the slots measured are the layout's."""
import math
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p6_phase1 as Q
import p6prime as PP

ART = Q.LV / "art"
GA = Q.LV / "guide_art"
LEVEL_ART = BF / "godot/data/bv2f/art/level.json"


def point_variant():
    lvl = jload(LEVEL_ART)
    syn = {"models": lvl["sim"]["models"], "features": [], "_what": "PH synthetic: level.json sim.models of the art variant"}
    p = PH / "results" / "art" / "layout_art_slots.json"
    dump(syn, str(p))
    Q.GV = GA
    Q.LAYOUT = p
    Q.IDS = GA / "ids_art.png"
    Q.LEVEL = LEVEL_ART
    PP.PLACED_FIT = Q.LV / "placed_fit_bv2art.json"
    return lvl, syn


def crosscheck(lvl):
    """every layout_bv2art placement against the level's slot data: pos = (u, -v), z, size (w, d, h), uniform scale"""
    L = jload(ART / "layout_bv2art.json")
    slots = []
    for m in lvl["sim"]["models"]:
        insts = m.get("instances") or []
        if insts:
            for ins in insts:
                if ins["type"] == "box":
                    slots.append((m["id"], ins["pos"], float(ins["z"]), ins["size_m"], ins.get("uniform_scale")))
        elif m.get("glb"):
            s = m["size_m"]
            slots.append((m["id"], m["pos"], float(m["z"]), [s["w_local_x"], s["d_local_z"], s["h"]], None))
    rows, bad = [], []
    for p in L["placements"]:
        u, v = p["uv"]
        best = min(slots, key=lambda sl: math.hypot(sl[1][0] - u, sl[1][1] + v))
        d = math.hypot(best[1][0] - u, best[1][1] + v)
        sz = p["size_m"]
        ok_pos = d <= 0.02
        ok_z = abs(best[2] - float(p["z"])) <= 0.02
        ok_sz = all(abs(a - b) <= 0.01 for a, b in zip(sorted([sz["w"], sz["d"], sz["h"]]), sorted(best[3])))
        r = {"id": p["id"], "slot_group": best[0], "pos_delta_m": round(d, 4), "z_ok": ok_z, "size_ok": ok_sz}
        rows.append(r)
        if not (ok_pos and ok_z and ok_sz):
            bad.append(r)
    return {"n_layout_placements": len(L["placements"]), "n_level_box_slots": len(slots), "mismatches": bad, "pass": not bad}, rows


def run():
    bars = jload(PH / "results/p6prime_calibration.json")["bars"]
    lvl, syn = point_variant()
    cc, ccrows = crosscheck(lvl)
    comp, L, cache = PP.v7c_components()
    scale = PP.v7c_scale(L, cache)
    objs = comp["objects"]
    hidden = {k: r["terrain_hidden_instances"] for k, r in objs.items() if r["terrain_hidden_instances"]}
    lvlm = {m["id"]: m for m in lvl["sim"]["models"]}
    sea_z = float(lvl["sim"].get("sea_z", -6.0))
    attrib = {}
    for k, lst in hidden.items():
        for i, sh_ in lst:
            ins = PP._instances(lvlm[k])[i]
            row = [r for r in comp["instances"][k] if r["i"] == i][0]
            top = row.get("z_top")
            why = []
            if row.get("own_px_in_frame", 0) < 400:
                why.append("frame edge: only %d px of its own silhouette inside the paint envelope" % row.get("own_px_in_frame", 0))
            if top is not None and top < sea_z:
                why.append("wholly below the sea surface (top z %.2f < sea_z %.1f; ground_sea is a ground id)" % (top, sea_z))
            attrib["%s#%d" % (k, i)] = {"terrain_hidden_share": sh_, "visible_share": row.get("visible_share"), "attribution": why or ["terrain"]}
    place_fail = {k: r["containment"] for k, r in objs.items() if r["containment"] is not None and r["containment"] < bars["containment_min"]}
    scale_fail = [r for r in scale if not r["pass"]]
    rec_bad = [r for r in scale if r.get("record_agrees_1pct") is False]
    # I-4: the constructed 1.5 m-shift RED on bv2art -- every slot prism shifted 1.5 m across (151 px), same bar
    idm = Q.ids_v7c()
    lm = Q.layout_masks(idm.shape)
    man = jload(GA / "guide_manifest.json")
    name_of = {int(k): v["id"] for k, v in man["id_table"].items()}
    shift = int(round(1.5 * PPM_V1))
    red = {}
    for mid, L_ in lm.items():
        ks = [k for k, n in name_of.items() if Q.OWN_CURTAIN.get(n, n) == mid]
        idmask = np.isin(idm, ks)
        n = int(idmask.sum())
        if not n:
            continue
        sh = np.roll(L_["mask"], shift, axis=1)
        red[mid] = round(float((idmask & sh).sum() / n), 4)
    red_fail = {k: v for k, v in red.items() if v < bars["containment_min"]}
    res = {"_what": "P6' on the bv2art blockout (frozen bars; extent retired, charter § 15)",
           "inputs": {"layout_bv2art_sha256": sha256(ART / "layout_bv2art.json"), "ids_art_sha256": sha256(GA / "ids_art.png"),
                      "ids_manifest_sha256": man["ids"]["sha256"], "level_art_sha256": sha256(LEVEL_ART),
                      "placed_fit_sha256": sha256(Q.LV / "placed_fit_bv2art.json"), "frame": "fid/lv/art/frame_grid.bv2art.json"},
           "bars": {k: bars[k] for k in ("presence_missing", "presence_extra", "terrain_hidden_share_max", "containment_min", "anisotropy_max")},
           "slot_crosscheck_vs_layout": cc,
           "I4_red_shift_1p5m": {"objects": len(red), "below_bar": len(red_fail), "values": red, "pass": not red_fail},
           "presence": {"missing": comp["missing"], "extra": comp["extra"], "terrain_hidden": hidden, "terrain_hidden_attribution": attrib,
                        "by_design_exclusions": comp["by_design_exclusions"], "non_model_ids_excluded": comp["non_model_ids_excluded"],
                        "pass": not comp["missing"] and not comp["extra"] and not hidden},
           "placement": {"bar": bars["containment_min"], "below_bar": place_fail,
                         "containment": {k: r["containment"] for k, r in objs.items()}, "pass": not place_fail},
           "scale": {"bar": PP.ANISO_MAX, "n_instances": len(scale), "n_over": len(scale_fail), "record_mismatches_vs_ph": len(rec_bad),
                     "over": [(r["slot"], r["instance"], r["anisotropy"]) for r in scale_fail],
                     "pass": not scale_fail and not rec_bad},
           "iou_vs_prism_reported": {k: r["iou_vs_prism_reported"] for k, r in objs.items()},
           "objects": objs, "instances_terrain": {k: [{kk: vv for kk, vv in r.items() if kk not in ("footprint_hull", "verts")} for r in v]
                                                  for k, v in comp["instances"].items()},
           "scale_rows": scale, "crosscheck_rows": ccrows}
    vals = [v for v in res["iou_vs_prism_reported"].values() if v is not None]
    res["iou_vs_prism_median_reported"] = round(float(np.median(vals)), 3) if vals else None
    res["P6prime_pass"] = all(res[c]["pass"] for c in ("presence", "placement", "scale"))
    dump(res, str(PH / "results/p6prime_art.json"))
    return res


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: r[k] for k in ("slot_crosscheck_vs_layout", "I4_red_shift_1p5m", "presence", "placement", "scale",
                                        "iou_vs_prism_median_reported", "P6prime_pass")}, indent=1, default=str)[:6000])
