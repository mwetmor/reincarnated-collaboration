#!/usr/bin/env python3
"""BV2F Phase 2' PILOT harness (R-C9-192; plan fid/ph/pilot_run_plan.json). FROZEN bars (calibration.md §§ 1-23).
Inputs: fid/pt/pilot/pilot_record.json. Window = bv2art plate px [0, 0, 4096, 2560] (cols 0-2 x rows 0-2), 100.6176 px/m.
  pilot_harness.py [rows...]   rows: p1 p2 p3 p4 p5 p6a p6prime p8 p11 (default all) -> results/pilot/<row>.json
P9/P10 are read from renders/pilot/ (run_pilot_godot.sh) by `pilot_harness.py p9p10`."""
import io
import math
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

PT = FID / "pt/pilot"
OUT = PH / os.environ.get("PH_PILOT_OUT", "results/pilot")
W, H = 4096, 2560
CHUNKS = [("%d_%d" % (c, r), (1280 * c, 768 * r, 1280 * c + 1536, 768 * r + 1024)) for r in range(3) for c in range(3)]
GA = FID / "lv/guide_art"


def save(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    dump(obj, str(OUT / (name + ".json")))
    return obj


_C = {}


def painting():
    if "P" not in _C:
        _C["P"] = load_rgb(PT / "painting.png")
    return _C["P"]


def ids_built():
    """v1's ID code (paint_world_prep.id_index): idx per pixel, 0 = nothing; table from ids_built/ids.json"""
    if "I" not in _C:
        a = np.asarray(Image.open(PT / "ids_built.png").convert("RGB")).astype(np.int32)
        is_pl = a[..., 2] > 100
        idx = np.where(is_pl, np.clip(np.round((a[..., 1] - 8) / 16.0), 0, 15).astype(np.int32) * 16
                       + np.clip(np.round((a[..., 0] - 8) / 16.0), 0, 15).astype(np.int32), 0)
        tab = {int(k): v for k, v in jload(PT / "ids_built/ids.json")["placements"].items()}
        _C["I"] = (idx, tab)
    return _C["I"]


def class_map():
    if "K" not in _C:
        man = jload(GA / "guide_manifest.json")
        cls = np.asarray(Image.open(GA / "class_art.png"))[:H, :W]
        _C["K"] = (cls, man["class"]["classes"])
    return _C["K"]


def ground_mask():
    idx, tab = ids_built()
    gids = [k for k, v in tab.items() if v["id"].startswith("ground_")]
    return (idx == 0) | np.isin(idx, gids)


def self_moving():
    """pixels that move by themselves in the rebuilt pilot (DEV-5): the animated sea (ground_sea ids) and the bobbing floes
    (blobs_shore_ice ids), dilated 6 px. Excluded from P3 and P8 inputs exactly as R-C9-159's animated sea was (p3_residual
    v159_rows `anim`; p9 sway `selfmove`): a heather mask or render taken from frames in which water moves sees the water."""
    if "SM" not in _C:
        man = jload(BF / "godot/data/bv2f/pilot/painted/manifest.json")
        idx, tab = ids_built()
        if not man.get("water"):
            _C["SM"] = np.zeros((H, W), bool)
        else:
            ks = [k for k, v in tab.items() if v["id"] == "ground_sea" or v["id"].startswith("blobs_shore_ice__")]
            _C["SM"] = ndimage.binary_dilation(np.isin(idx, ks), iterations=6)
    return _C["SM"]


def tufts():
    if "T" not in _C:
        import importlib.util
        spec = importlib.util.spec_from_file_location("pw_v1_readonly", BF / "tools/paint_world_prep.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        P8 = painting().astype(np.uint8)
        h, s = m.tuft_classes(P8, ground_mask())
        _C["T"] = ndimage.binary_opening(h | s, iterations=1)
    return _C["T"]


# ---------------------------------------------------------------------------------------------------------- P1
def p1():
    fr = jload(PT / "frame_grid.pilot.json")
    ppm = float(fr["px_per_m_across"])
    rows = [{"surface": "ground + projected primitives", "source_ppm": ppm, "ratio": round(PPM_V1 / ppm, 4)}]
    br = jload(PT / "bake_report.json")["pieces"]
    for k, v in br.items():
        seen = v["texels_on_mesh"] * (1 - v["unseen_before_fill_pct"] / 100.0)
        sil = v["surface"]["silhouette_px_in_cell"]
        tex = ppm * math.sqrt(seen / max(sil, 1))
        src = min(ppm, tex)
        vis = sil - v["surface"].get("hidden_by_another_piece_px", 0)
        tv = ppm * math.sqrt(seen / max(vis, 1))
        rows.append({"surface": "bake " + k, "source_ppm": round(src, 2), "texture_seen_ppm": round(tex, 1), "ratio": round(PPM_V1 / src, 4),
                     "silhouette_px": sil, "hidden_by_another_piece_px": v["surface"].get("hidden_by_another_piece_px", 0),
                     "sensitivity_ratio_visible_silhouette_only": round(PPM_V1 / min(ppm, tv), 4)})
    worst = max(rows, key=lambda r: r["ratio"])
    return save("p1", {"rows": rows, "worst": worst, "over_bar": [(r["surface"], r["ratio"], r.get("sensitivity_ratio_visible_silhouette_only"))
                                                                for r in rows if r["ratio"] > 1.05],
                       "pass": all(r["ratio"] <= 1.05 for r in rows), "bar": "<= 1.05",
                       "instrument": "frozen (p1_density.v1_surfaces): tex_ppm = ppm * sqrt(seen texels / silhouette_px_in_cell); the sensitivity column "
                                     "drops the silhouette px hidden by another piece (v1's largest hidden share: 2012/18565, door_lintel)"})


# ---------------------------------------------------------------------------------------------------------- P2
REPO = C9.parents[3]
PILOT_COMMIT = os.environ.get("PH_PILOT_COMMIT", "47bb1a054")     # the pilot as handed over (R-C9-192: 47bb1a054; rebuilt R-C9-194: 0b72461db)


def _at_commit(spec, commit, root):
    """the spec with every tracked path it names (painting, nodes, records, tools, inputs) materialised from `commit`
    under `root`; untracked paths are used as they are on disk (reported)."""
    import subprocess
    seen, untracked = {}, []

    def mat(path):
        path = str(path)
        if path in seen:
            return seen[path]
        rel = os.path.relpath(path, REPO)
        r = subprocess.run(["git", "-C", str(REPO), "show", "%s:%s" % (commit, rel)], capture_output=True)
        if r.returncode:
            untracked.append(rel)
            seen[path] = path
            return path
        q = pathlib.Path(root) / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_bytes(r.stdout)
        seen[path] = str(q)
        return str(q)
    sp = json.loads(json.dumps(spec))
    sp["painting"]["path"] = mat(sp["painting"]["path"])
    for n in sp["textures"]:
        n["path"] = mat(n["path"])
        for ln in n["links"]:
            for k in ("record", "tool", "input"):
                if k in ln:
                    ln[k] = mat(ln[k])
    return sp, sorted(set(untracked))


def p2():
    import tempfile
    import p2_lineage as L2
    spec = jload(PT / "lineage.json")
    wt = L2.resolve(spec)
    with tempfile.TemporaryDirectory() as td:
        sp, untracked = _at_commit(spec, PILOT_COMMIT, td)
        L2._SHA.clear()
        at = L2.resolve(sp)
    slim = lambda r: {k: r[k] for k in ("value", "resolved", "n", "unresolved", "pass")}
    return save("p2", dict(slim(at), binding="at the handed-over commit %s" % PILOT_COMMIT, untracked_paths_used_from_disk=untracked,
                           rows=at["rows"], working_tree=dict(slim(wt), rows=[r for r in wt["rows"] if not r["resolves"]])))


# ---------------------------------------------------------------------------------------------------------- P3
def p3_masks():
    idx, tab = ids_built()
    cls, names = class_map()
    baked = set(jload(PT / "bake_report.json")["pieces"])
    hm = ndimage.binary_dilation(np.asarray(Image.open(PT / "heather_mask.png").convert("L")) > 20, iterations=2)
    M = {}
    for k, v in tab.items():
        if v["id"].startswith("ground_") or v["id"].startswith(("curtain_", "door_")):
            continue
        key = "%s (%s)" % (v["class"], "baked" if v["id"] in baked else "projected")
        M.setdefault(key, np.zeros((H, W), bool))
        M[key] |= idx == k
    g = ground_mask() & ~tufts()
    for i, n in enumerate(names):
        if n == "none":
            continue
        m = g & (cls == i)
        if m.sum() > 2000:
            M["ground: " + n] = m
    sm = self_moving()
    for k in M:
        M[k] &= ~hm & ~sm
    return M


def p3():
    import p3_residual as R3
    R = load_rgb(PT / "render_guide.png")
    P = painting()
    M = p3_masks()
    rows = {k: R3.resid(R, P, m) for k, m in M.items()}
    lit = np.asarray(Image.open(io.BytesIO(open(BF / "godot/data/bv2f/pilot/painted/lit.bin", "rb").read())).convert("L"), np.float32) / 255.0
    lit = np.asarray(Image.fromarray((lit * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255.0
    lin = srgb_to_lin(R)
    mul = np.array(jload(BF / "godot/data/bv2f/pilot/painted/manifest.json")["shadow_mul"]["linear"])   # the pilot's measured shadow
    f = lit[..., None] + (1 - lit[..., None]) * mul
    out = lin * f
    srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * np.clip(out, 0, None) ** (1 / 2.4) - 0.055) * 255
    static = np.zeros((H, W), bool)
    for m in M.values():
        static |= m
    R2 = R.copy()
    R2[static] = np.clip(srgb[static], 0, 255)
    red = {k: R3.resid(R2, P, m) for k, m in M.items()}
    return save("p3", {"pilot": R3.verdict(rows), "constructed_reshade_red": R3.verdict(red), "bar": 15.5,
                       "red": "the render re-shaded by the pilot's own lit.bin x shadow_mul (the shadow applied twice)",
                       "pass": R3.verdict(rows)["pass"]})


# ---------------------------------------------------------------------------------------------------------- P4
def p4():
    """binding: snow, rock, ice vs v1's leave-one-chunk-out maxima (the frozen bars). ADVISORY (R-C9-167 (3), W-5
    re-home): wood -> v1 lintel + posts + logs, shingle -> v1 shore_rock (piece bootstrap), sea / shore ice -> v1 tarn ice."""
    import p4_texture as T
    masks_v1, static_v1 = T.v1_classes()
    per = T.v1_pool(None, masks_v1, static_v1)
    bars = T.v1_bars(per)
    bind = {c: bars[c] for c in ("snow", "rock", "ice")}
    bind["cellularity"] = bars["cellularity"]
    idx, tab = ids_built()
    cls, names = class_map()
    ni = {n: i for i, n in enumerate(names)}
    g = ground_mask() & ~tufts()
    model = lambda c: np.isin(idx, [k for k, v in tab.items() if v["class"] == c and not v["id"].startswith(("ground_", "curtain_", "door_"))])
    masks = {"snow": g & (cls == ni["snow"]), "ice": g & (cls == ni["ice"]), "rock": model("rock")}
    adv_masks = {"wood": model("wood"), "shingle": g & (cls == ni["shingle"]), "sea": g & (cls == ni["sea"]),
                 "shore ice": g & (cls == ni["shore_ice"])}
    static = ~(np.asarray(Image.open(PT / "heather_mask.png").convert("L")) > 20) & ~tufts()
    P = painting()
    rows, sa = {}, {}
    for key, (x0, y0, x1, y1) in CHUNKS:
        st = T.stats(P[y0:y1, x0:x1], {c: m[y0:y1, x0:x1] for c, m in masks.items()}, static[y0:y1, x0:x1])
        rows[key] = T.score(st, per, bind)
        sa[key] = T.stats(P[y0:y1, x0:x1], {c: m[y0:y1, x0:x1] for c, m in adv_masks.items()}, static[y0:y1, x0:x1])
    binding_fail = [(k, c) for k, r in rows.items() for c, v in r["classes"].items() if v.get("pass") is False]
    refs = {c: T.bootstrap_bar(T.v1_piece_pool(cl)) for c, (nm, cl) in T.NEW_MAP.items()}
    ph_, ps_ = T.pooled(per, "ice")
    refs["tarn"] = {"pool_hist": ph_, "pool_spec": ps_, "hist_bar": bars["ice"]["hist"], "spec_bar": bars["ice"]["spec"]}
    adv = {}
    for c, ref in (("wood", refs["wood"]), ("shingle", refs["shingle"]), ("sea", refs["tarn"]), ("shore ice", refs["tarn"])):
        rr = []
        for k, (res, _, _) in sa.items():
            if c not in res:
                continue
            r = res[c]
            dh = T.hellinger(r["hist"], ref["pool_hist"])
            dsp = float(np.sqrt(np.mean((r["spec"] - ref["pool_spec"]) ** 2))) if (r["spec"] is not None and ref["pool_spec"] is not None) else None
            ok = dh <= ref["hist_bar"] and (dsp is None or ref["spec_bar"] is None or dsp <= ref["spec_bar"])
            rr.append({"chunk": k, "px": r["px"], "hist": round(dh, 3), "hist_bar": round(ref["hist_bar"], 3),
                       "spec": None if dsp is None else round(dsp, 3),
                       "spec_bar": None if ref["spec_bar"] is None else round(ref["spec_bar"], 3), "within": bool(ok)})
        adv[c] = {"samples": len(rr), "within_bar": sum(r["within"] for r in rr), "rows": rr}
    judged = sorted({c for r in rows.values() for c in r["classes"]})
    return save("p4", {"bars_from_v1": {c: {kk: (None if vv is None else round(float(vv), 3)) if kk != "n_chunks" else vv
                                            for kk, vv in bind[c].items()} for c in ("snow", "rock", "ice")},
                       "chunks": rows, "classes_judged": judged, "binding_fails": binding_fail, "pass": not binding_fail,
                       "advisory_new_classes": adv})


# ---------------------------------------------------------------------------------------------------------- P5
def p5():
    import p5_seams as S5
    paths = S5.canvases("BV2F-PT")
    st = jload(PT / "stitch_record.json")["canvases"]
    shas = {k: sha256(v) for k, v in paths.items()}
    assert set(paths) == set(st) and all(shas[k] == st[k]["sha256"] for k in st), "canvases differ from PT's stitch record"
    mads = S5.overlap_mads(paths)
    vis = S5.seam_vis(painting(), 3, 3)
    b = jload(PH / "results/p5.json")["bars_from_v1"]
    v = S5.verdict({"overlap_mad": mads, "seam_visibility": vis}, b)
    return save("p5", dict(v, overlap_mad=mads, seam_visibility=vis, bars=b))


# ---------------------------------------------------------------------------------------------------------- P6a
def declared():
    out = []
    for o in jload(GA / "declared_openings.json")["openings"]:
        x, y = o["centre_px"]
        if 0 <= x < W and 0 <= y < H:
            out.append({"id": o["id"], "xy": (x, y), "radius_m": float(o["p6a_match_radius_m"]),
                        "corners": [tuple(o["corners_px"][k]) for k in ("bottom_a", "bottom_b", "top_b", "top_a")] if o.get("corners_px") else None})
    return out


def p6a():
    """the v0.1 detector (T = 32, no prior; § 8 (1)) at quarter scale on the pilot painting; each candidate matched by
    screen distance to a declared opening's CENTRE (LV's centre_px) within LV's p6a_match_radius_m (= half-width + 1 m,
    § 11 G2-B1). Window holds no declared dark structure (char/ash share 0, pilot_run_plan), so by § 11's triage rule a
    candidate that matches no declared opening is 'invented (outside dark structures: auto-fail)' -- recorded for the
    conductor's by-eye read (fallback (a)); `p6_overlay.py record pilot <cid> <verdict> ...` rewrites a row."""
    import datetime
    import p6_geometry as G
    import p6_overlay as O
    SC = G.SC
    P = painting()
    im = np.asarray(Image.fromarray(np.clip(P, 0, 255).astype(np.uint8)).resize((W // 4, H // 4), Image.BOX), np.float32)
    T = jload(PH / "results/p6.json")["invention"]["T_v1_ceiling"]
    found = G.openings(im, PPM_V1 * SC, T)
    dec = declared()
    od = PH / "triage" / "pilot"
    od.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, f in enumerate(found):
        x, y = f["xy"][0] / SC, f["xy"][1] / SC
        best = min(dec, key=lambda d: math.hypot(x - d["xy"][0], y - d["xy"][1]))
        dist = math.hypot(x - best["xy"][0], y - best["xy"][1]) / PPM_V1
        matched = dist <= best["radius_m"]
        chunk = [k for k, (x0, y0, x1, y1) in CHUNKS if x0 <= x < x1 and y0 <= y < y1]
        cr, x0, y0 = O._crop(P, x, y)
        g_ = cr.mean(-1, keepdims=True)
        ov = Image.fromarray(np.clip(cr * 0.55 + g_ * 0.45, 0, 255).astype(np.uint8))
        dr = ImageDraw.Draw(ov)
        for d in dec:
            cx, cy = d["xy"][0] - x0, d["xy"][1] - y0
            rr = d["radius_m"] * PPM_V1
            if d["corners"]:
                dr.polygon([(a - x0, b - y0) for a, b in d["corners"]], outline=O.CYAN, width=5)
            dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=O.CYAN, width=2)
            dr.text((max(2, min(O.CROP - 200, cx - 60)), max(2, min(O.CROP - 14, cy - rr - 14))), "declared: " + d["id"], fill=O.CYAN)
        dr.ellipse([x - x0 - 10, y - y0 - 10, x - x0 + 10, y - y0 + 10], outline=(255, 60, 60), width=3)
        ova = np.asarray(ov)
        comp = np.full((O.CROP, 2 * O.CROP + O.GAP, 3), 255, np.uint8)
        comp[:, :O.CROP] = np.clip(cr, 0, 255).astype(np.uint8)
        comp[:, O.CROP + O.GAP:] = ova
        cid = "%s_c%03d" % (chunk[0] if chunk else "w", i)
        Image.fromarray(comp).save(od / (cid + ".png"))
        verdict = "declared" if matched else "invented (outside dark structures: auto-fail)"
        cls, names = class_map()
        idx, tab = ids_built()
        xi, yi = int(round(x)), int(round(y))
        cw = cls[max(yi - 30, 0):yi + 30, max(xi - 30, 0):xi + 30]
        u_, n_ = np.unique(cw, return_counts=True)
        what = {"guide_class_share_0.6m": {names[a]: round(float(b) / cw.size, 3) for a, b in zip(u_, n_)},
                "id_at_centroid": tab[int(idx[yi, xi])]["id"] if int(idx[yi, xi]) in tab else "none (0)"}
        rows.append({"chunk": chunk, "candidate": cid, "candidate_px": [round(x), round(y)], "area_m2": round(f["area_m2"], 2),
                     "h_m": f["h_m"], "w_m": f["w_m"], "inside_dark_structure": False,
                     "crop_sha": O._sha_png(cr), "overlay_sha": O._sha_png(ova),
                     "nearest_declared": best["id"], "distance_m": round(dist, 2), "match_radius_m": best["radius_m"],
                     "verdict": verdict, "evidence": "", "ph_observation": what, "reader": "auto (pilot_harness.py, § 11 triage rule)",
                     "conductor_read": "PENDING (fallback (a), by eye)" if not matched else "n/a",
                     "image": "fid/ph/triage/pilot/%s.png" % cid,
                     "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    with open(PH / "results" / "p6a_triage_pilot.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    inv = [r for r in rows if not r["verdict"].startswith("declared")]
    hit = sorted({r["nearest_declared"] for r in rows if r["verdict"] == "declared"})
    return save("p6a", {"T": T, "detector": "v0.1 (no prior), quarter scale", "declared_in_window": [d["id"] for d in dec],
                        "declared_found": hit, "candidates": len(rows), "unmatched": [r["candidate"] for r in inv],
                        "chunks_failing_by_rule": sorted({c for r in inv for c in r["chunk"]}), "rows": rows,
                        "pass": not inv, "verdict": "PASS" if not inv else "FAIL by the § 11 rule pending the conductor's by-eye read (%d)" % len(inv)})


# ---------------------------------------------------------------------------------------------------------- P6'
def p6prime():
    """presence / placement / scale (frozen bars, results/p6prime_calibration.json) on the BUILT pilot's ID render.
    ids_built is ungrouped (one id per placement); it is re-coded here to the art guide's group ids (ids_art id_table:
    the group = the id before '__'), so p6prime_art's machinery and slots apply unchanged. Window = plate [0,0,4096,2560]."""
    import p6_phase1 as Q
    import p6prime as PP
    import p6prime_art as PA
    lvl, syn = PA.point_variant()
    idx, tab = ids_built()
    man = jload(GA / "guide_manifest.json")
    code = {v["id"]: int(k) for k, v in man["id_table"].items()}
    gidx = np.zeros_like(idx)
    unmapped = []
    for k, v in tab.items():
        g = v["id"].split("__")[0]
        if g not in code:
            unmapped.append(v["id"])
            continue
        gidx[idx == k] = code[g]
    comp, L, cache = PP.v7c_components(ids=gidx)
    bars = jload(PH / "results/p6prime_calibration.json")["bars"]
    objs = comp["objects"]
    hidden = {k: r["terrain_hidden_instances"] for k, r in objs.items() if r["terrain_hidden_instances"]}
    place = {k: r["containment"] for k, r in objs.items() if r["containment"] is not None and r["containment"] < bars["containment_min"]}
    scale = PP.v7c_scale(L, cache)
    sfail = [r for r in scale if not r["pass"]]
    rec_bad = [r for r in scale if r.get("record_agrees_1pct") is False]
    in_frame = sorted(k for k, r in objs.items() if r["in_frame"])
    res = {"inputs": {"ids_built_sha256": sha256(PT / "ids_built.png"), "ids_json_sha256": sha256(PT / "ids_built/ids.json"),
                      "unmapped_ids": unmapped, "regrouped_to": "fid/lv/guide_art/guide_manifest.json id_table"},
           "bars": {k: bars[k] for k in ("presence_missing", "presence_extra", "terrain_hidden_share_max", "containment_min", "anisotropy_max")},
           "objects_in_window": in_frame,
           "presence": {"missing": comp["missing"], "extra": comp["extra"], "terrain_hidden": hidden,
                        "hidden_by_design": comp.get("hidden_by_design", {}),
                        "pass": not comp["missing"] and not comp["extra"] and not hidden and not unmapped},
           "placement": {"bar": bars["containment_min"], "below_bar": place,
                         "containment": {k: objs[k]["containment"] for k in in_frame}, "pass": not place},
           "scale": {"bar": PP.ANISO_MAX, "n_instances": len(scale), "n_over": len(sfail), "record_mismatches_vs_ph": len(rec_bad),
                     "over": [(r["slot"], r["instance"], r["anisotropy"]) for r in sfail], "pass": not sfail and not rec_bad},
           "objects": {k: objs[k] for k in in_frame}}
    res["pass"] = all(res[c]["pass"] for c in ("presence", "placement", "scale"))
    return save("p6prime", res)


# ---------------------------------------------------------------------------------------------------------- P8 + DEV-18
def p8():
    import p7_p8_floor_heather as F
    T_ = tufts()
    HM_raw = np.asarray(Image.open(PT / "heather_mask.png").convert("L")) > 127
    HM = HM_raw & ~self_moving()
    rows_as_delivered = F.precision_chunks(HM_raw, T_)
    rows = F.precision_chunks(HM, T_)
    vals = [v for v in rows.values() if v is not None]
    below = [k for k, v in rows.items() if v is not None and v < 0.4476]
    # constructed RED (as calibrated, § 11 W-3): the drawn heather shifted 1 m across
    red = F.precision_chunks(np.roll(HM, int(PPM_V1), axis=1), T_)
    rv = [v for v in red.values() if v is not None]
    # DEV-18: PT plants 3D heather on FLAT tufts only (flat = |terrain| < 0.03 m, bv2f_prep.py). A painted tuft is
    # 'without 3D heather' when no drawn heather lies within P8's 24 px footprint; split flat / not flat by the same rule.
    near = ndimage.binary_dilation(HM, structure=F._disk(24))
    bare = T_ & ~near
    z, slope = ground_z_slope()
    flat = np.abs(z) < 0.03
    nT = max(int(T_.sum()), 1)
    dev = {"rule": "flat = |terrain z| < 0.03 m at the pixel's ground point (bv2f_prep.py's rule); 3D heather = heather_mask.png drawn "
                   "px within 24 px (P8 footprint); tufts = v1's tuft classifier on the pilot painting's ground",
           "painted_tuft_px": int(T_.sum()),
           "share_on_flat": round(float((T_ & flat).sum() / nT), 4),
           "share_not_flat": round(float((T_ & ~flat).sum() / nT), 4),
           "share_without_3d_heather": round(float(bare.sum() / nT), 4),
           "share_not_flat_without_3d_heather": round(float((bare & ~flat).sum() / nT), 4),
           "share_flat_without_3d_heather": round(float((bare & flat).sum() / nT), 4),
           "share_on_slope_gt_5deg_without_3d_heather": round(float((bare & (slope > 5)).sum() / nT), 4),
           "not_flat_tufts_covered_by_3d_heather": round(float((T_ & ~flat & near).sum() / max(int((T_ & ~flat).sum()), 1)), 4),
           "slope_deg_of_not_flat_bare_tufts_p10_p50_p90": [round(float(np.percentile(slope[bare & ~flat], q)), 1) for q in (10, 50, 90)]
           if (bare & ~flat).any() else None}
    return save("p8", {"per_chunk": rows, "per_chunk_as_delivered_incl_water": rows_as_delivered,
                       "drawn_px_removed_as_self_moving": int((HM_raw & self_moving()).sum()), "chunks_judged": len(vals), "below_bar": below, "min": min(vals) if vals else None,
                       "bar": 0.4476, "pass": bool(vals) and not below,
                       "constructed_red_shift_1m": {"per_chunk": red, "min": min(rv) if rv else None,
                                                    "pass": bool(rv) and all(v >= 0.4476 for v in rv)},
                       "DEV18": dev})


def ground_z_slope():
    """terrain z (m) and slope (deg) at each pilot pixel's GROUND point: the art heightfield (rows north -> south,
    make_bv2art.py), the ground point found by iterating the plate law y = (v1 - v) * 80.3076 - z * 60.6137 (4 passes)."""
    lvl = jload(BF / "godot/data/bv2f/art/level.json")
    hf = lvl["sim"]["heightfield"]
    Z = np.fromfile(BF / "godot/data/bv2f/art" / hf["file"], dtype="<f4").reshape(hf["shape"])
    ex = hf["extent_sim_m"]
    k = float(hf["px_per_m"])
    gy, gx = np.gradient(Z, 1.0 / k)
    S = np.degrees(np.arctan(np.hypot(gx, gy)))
    env = jload(GA / "guide_manifest.json")["envelope"]
    u0, v1 = env["u"][0], env["v"][1]
    ys, xs = np.mgrid[0:H:2, 0:W:2].astype(np.float64)
    u = u0 + (xs + 1) / PPM_V1
    z = np.zeros_like(u)
    for _ in range(4):
        v = v1 - (ys + 1 + z * 60.6137) / 80.3076
        i = np.clip(np.round((-v - ex["y0"]) * k).astype(int), 0, Z.shape[0] - 1)
        j = np.clip(np.round((u - ex["x0"]) * k).astype(int), 0, Z.shape[1] - 1)
        z = Z[i, j].astype(np.float64)
    up = lambda a: np.repeat(np.repeat(a, 2, 0), 2, 1)[:H, :W]
    return up(z), up(S[i, j])


# ---------------------------------------------------------------------------------------------------------- P11
def p11():
    import p11_abx as X
    st = sorted((FID / "pt/pilot_stills").glob("pilot_[0-9][0-9].png"))
    X._centres()
    for v in jload(FID / "pt/pilot_stills/views.json")["views"].values():        # the within-trial same-place guard
        X._CENTRES[v["png"]] = tuple(v["camera"]["centre_ground_uv"])
    r = X.build("pilot_v1_vs_pilot", st, seed=192)
    return save("p11_build", dict(r, stills=[p.name for p in st], v1_pool=[str(p) for p in X.P.V1_STILLS if p.exists()],
                                  key="fid/ph/p11/keys/abx_pilot_v1_vs_pilot.json"))


# ---------------------------------------------------------------------------------------------------------- P9 / P10
def p9p10():
    import p9_p10_life_perf as L9
    R = PH / os.environ.get("PH_PILOT_RENDERS", "renders/pilot")
    v1 = jload(PH / "results/p9_p10.json") if (PH / "results/p9_p10.json").exists() else None
    bar = 2.064
    out = {"sway_bar": bar}
    if (R / "life/f1.png").exists():
        s = L9.sway(R / "life")
        out["p9_sway"] = dict(s, pass_=bool(s["sway"] >= 3 * s["noise"] and s["sway"] >= bar))
    if (R / "life_nowind/f1.png").exists():
        s0 = L9.sway(R / "life_nowind")
        out["p9_red_nowind"] = dict(s0, pass_=bool(s0["sway"] >= 3 * s0["noise"] and s0["sway"] >= bar))
    out["p9_trail"] = trail_pilot()
    for k in ("perf", "perf_burn"):
        r = L9.perf(R / k)
        if r:
            out["p10_" + k] = r
    return save("p9p10", out)


def trail_pilot():
    """the snow field's area (pilot manifest snow.area_xz, world xz) against the pilot's walkable ground: the level's
    bounds polygon (uv) inside the pilot window, world xz = v1's rotation (bv2f_prep.py xz_of_uv). Also reported: the
    share of that ground where the field carries snow at all (depth multiplier > 0; flat ground only by DEV-18)."""
    from matplotlib.path import Path
    lvl = jload(BF / "godot/data/bv2f/art/level.json")
    sn = jload(BF / "godot/data/bv2f/pilot/painted/manifest.json")["snow"]
    env = jload(GA / "guide_manifest.json")["envelope"]
    u0, v1 = env["u"][0], env["v"][1]
    u1, v0 = u0 + W / PPM_V1, v1 - H / 80.3076
    uu, vv = np.meshgrid(np.arange(u0, u1, 0.1), np.arange(v0, v1, 0.1))
    pts = np.c_[uu.ravel(), vv.ravel()]
    walk = Path(np.array(lvl["bounds"]["polygon_uv"])).contains_points(pts)
    C, S_ = math.cos(math.radians(47)), math.sin(math.radians(47))
    X = pts[:, 0] * C - pts[:, 1] * S_
    Zw = -pts[:, 0] * S_ - pts[:, 1] * C
    ax, az, aw, ah = sn["area_xz"]
    inr = (X >= ax) & (X <= ax + aw) & (Zw >= az) & (Zw <= az + ah)
    g = sn["grid"]
    nx, nz = g["nx"], g["nz"]
    raw = np.fromfile(BF / "godot/data/bv2f/pilot/painted" / g["file"], dtype="<f4")
    mul = raw[:nx * nz].reshape(nz, nx)
    gi = np.clip(((X - g["origin_xz"][0]) / g["cell_m"]).astype(int), 0, nx - 1)
    gj = np.clip(((Zw - g["origin_xz"][1]) / g["cell_m"]).astype(int), 0, nz - 1)
    has = mul[gj, gi] > 0
    n = max(int(walk.sum()), 1)
    hf = lvl["sim"]["heightfield"]
    Zh = np.fromfile(BF / "godot/data/bv2f/art" / hf["file"], dtype="<f4").reshape(hf["shape"])
    ex, k = hf["extent_sim_m"], float(hf["px_per_m"])
    zi = np.clip(np.round((-pts[:, 1] - ex["y0"]) * k).astype(int), 0, Zh.shape[0] - 1)
    zj = np.clip(np.round((pts[:, 0] - ex["x0"]) * k).astype(int), 0, Zh.shape[1] - 1)
    flat = np.abs(Zh[zi, zj]) < 0.03
    split = {nm: {"walkable_m2": round(float((walk & m).sum()) * 0.01, 1),
                  "inside_field": round(float((walk & m & inr).sum() / max(int((walk & m).sum()), 1)), 4),
                  "snow_carrying": round(float((walk & m & inr & has).sum() / max(int((walk & m).sum()), 1)), 4)}
             for nm, m in (("flat", flat), ("not_flat (slopes, mound, swells)", ~flat))}
    return {"coverage": round(float((walk & inr).sum() / n), 4), "bar": 0.99, "pass": float((walk & inr).sum() / n) >= 0.99,
            "by_terrain": split,
            "walkable_m2_in_window": round(n * 0.01, 1), "area_xz": sn["area_xz"],
            "informational_snow_carrying_share_of_walkable": round(float((walk & inr & has).sum() / n), 4)}


ROWS = {"p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "p6a": p6a, "p6prime": p6prime, "p8": p8, "p11": p11, "p9p10": p9p10}

if __name__ == "__main__":
    want = sys.argv[1:] or [k for k in ROWS if k != "p9p10"]
    for k in want:
        r = ROWS[k]()
        brief = {kk: vv for kk, vv in r.items() if kk in ("pass", "verdict", "worst", "median_iou", "min", "whole_window", "candidates",
                                                            "unmatched", "chunks_failing_by_rule", "binding_fails", "value", "worst_class", "below_bar", "trials", "repeats", "images", "UNDERPOWERED")}
        print(k, json.dumps(brief, default=str)[:600])


# ---------------------------------------------------------------------------------------------------------- P9c sub-pixel
def _phase_subpx(a, b, up=20):
    """shift (dy, dx) with b(x) = a(x - d)... read as in p9's phase_shift(b, a): the integer peak of the normalised
    cross-power, refined by a locally UPSAMPLED inverse DFT (factor `up`, +-1.5 px around the peak; Guizar-Sicairos 2008)"""
    A = np.fft.fft2(a)
    B = np.fft.fft2(b)
    Rr = A * np.conj(B)
    Rr /= np.abs(Rr) + 1e-9
    r = np.fft.ifft2(Rr).real
    Hh, Ww = r.shape
    y, x = np.unravel_index(np.argmax(r), r.shape)
    y = y - Hh if y > Hh // 2 else y
    x = x - Ww if x > Ww // 2 else x
    fy, fx = np.fft.fftfreq(Hh), np.fft.fftfreq(Ww)
    oy = y + np.arange(-1.5, 1.5 + 1e-9, 1.0 / up)
    ox = x + np.arange(-1.5, 1.5 + 1e-9, 1.0 / up)
    Ey = np.exp(2j * np.pi * np.outer(oy, fy))
    Ex = np.exp(2j * np.pi * np.outer(fx, ox))
    loc = (Ey @ Rr @ Ex).real
    iy, ix = np.unravel_index(np.argmax(loc), loc.shape)
    return float(oy[iy]), float(ox[ix])


def _sil_shift(p0, p1):
    """the silhouette's own motion, sub-pixel: phase correlation of the two (1 px-blurred) binary masks, upsampled"""
    a = ndimage.gaussian_filter(p0.astype(float), 1.0)
    b = ndimage.gaussian_filter(p1.astype(float), 1.0)
    return _phase_subpx(b - b.mean(), a - a.mean())


def _taper(im, core):
    """mean-removed inside the core, multiplied by a smooth (Gaussian-blurred) core window: a hard 0/1 window shared by
    both frames correlates with ITSELF at zero shift and hides the texture's motion (found in R-C9-194's self-test)"""
    w = ndimage.gaussian_filter(core.astype(float), 4)
    return (im - im[core].mean()) * w


def floe_drift_subpx(dirp):
    """P9c, re-instrumented to sub-pixel (R-C9-194 positive control): p9_p10_life_perf.floe_drift with the texture shift
    read by a parabolic-peak phase correlation instead of the integer peak -- the integer peak alone carries up to
    ~0.7 px of quantisation against a 0.25 px bar. Same masks, same pieces, same silhouette centroids."""
    import p9_p10_life_perf as L
    m0, m1 = load_rgb(dirp / "floe_m0.png"), load_rgb(dirp / "floe_m1.png")
    hf = load_rgb(dirp / "hide_floe.png")
    k0 = ndimage.binary_opening(L._d(m0, hf) > 20, iterations=1)
    k1 = ndimage.binary_opening(L._d(m1, hf) > 20, iterations=1)
    lab, n = ndimage.label(k0)
    rows = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None:
            continue
        piece0 = lab[sl] == i + 1
        if piece0.sum() < 1500:
            continue
        y0, y1 = max(sl[0].start - 8, 0), sl[0].stop + 8
        x0, x1 = max(sl[1].start - 8, 0), sl[1].stop + 8
        p0, p1 = k0[y0:y1, x0:x1], k1[y0:y1, x0:x1]
        c0, c1 = ndimage.center_of_mass(p0), ndimage.center_of_mass(p1)
        sil = (c1[0] - c0[0], c1[1] - c0[1])
        core = ndimage.binary_erosion(p0 & p1, iterations=4)
        if core.sum() < 500:
            continue
        a = _taper(luma(m0[y0:y1, x0:x1]), core)
        b = _taper(luma(m1[y0:y1, x0:x1]), core)
        ty, tx = _phase_subpx(b, a)
        rows.append({"px": int(piece0.sum()), "silhouette_shift": [round(sil[0], 3), round(sil[1], 3)],
                     "texture_shift": [round(ty, 3), round(tx, 3)], "drift": round(math.hypot(sil[0] - ty, sil[1] - tx), 3)})
    d = [r["drift"] for r in rows]
    return {"floes_measured": len(rows), "median_drift_px": round(float(np.median(d)), 3) if d else None,
            "max_drift_px": round(float(np.max(d)), 3) if d else None, "rows": rows}


def subpx_selftest():
    """constructed: a textured disc moved by a known sub-pixel offset (Fourier shift) in BOTH silhouette and texture
    (rest-pose: drift 0) and in silhouette only (world-anchored: drift = the offset)"""
    rng = np.random.default_rng(194)
    out = []
    for off in ((0.4, 1.3), (1.7, -0.6), (0.0, 2.25)):
        tex = ndimage.gaussian_filter(rng.random((160, 160)), 1.2)
        yy, xx = np.mgrid[0:160, 0:160]
        disc = (((yy - 80) / 45.0) ** 2 + ((xx - 80) / 60.0) ** 2 <= 1).astype(float)
        sh = lambda im, o: np.fft.ifft2(ndimage.fourier_shift(np.fft.fft2(im), o)).real
        d1 = sh(disc, off) > 0.5
        t_rest = sh(tex, off)
        core = ndimage.binary_erosion((disc > 0.5) & d1, iterations=4)
        c0, c1 = ndimage.center_of_mass(disc > 0.5), ndimage.center_of_mass(d1)
        sil = (c1[0] - c0[0], c1[1] - c0[1])
        ty, tx = _phase_subpx(_taper(t_rest, core), _taper(tex, core))
        ty2, tx2 = _phase_subpx(_taper(tex, core), _taper(tex, core))
        out.append({"offset": off, "rest_pose_drift": round(math.hypot(sil[0] - ty, sil[1] - tx), 3),
                    "world_anchored_drift": round(math.hypot(sil[0] - ty2, sil[1] - tx2), 3), "true_offset_norm": round(math.hypot(*off), 3)})
    return out
