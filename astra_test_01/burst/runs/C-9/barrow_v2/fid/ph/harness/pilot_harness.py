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
DATA = BF / "godot/data/bv2f" / os.environ.get("PH_PILOT_DATA", "pilot") / "painted"     # rp2: pilot_rp2 (R-C9-240)
LEVELD = BF / "godot/data/bv2f" / os.environ.get("PH_PILOT_LEVEL", "art")                 # rp2: pilot_rp2/level (PIN.json)
CANVAS_PREFIX = os.environ.get("PH_PILOT_CANVASES", "BV2F-PT")                             # rp2: BV2F-PS2


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
    gids = [k for k, v in tab.items() if v["id"].startswith(("ground_", "carved_"))]   # carved_*: terrain carve layers (R-C9-232)
    return (idx == 0) | np.isin(idx, gids)


def self_moving():
    """pixels that move by themselves in the rebuilt pilot (DEV-5): the animated sea (ground_sea ids) and the bobbing floes
    (blobs_shore_ice ids), dilated 6 px. Excluded from P3 and P8 inputs exactly as R-C9-159's animated sea was (p3_residual
    v159_rows `anim`; p9 sway `selfmove`): a heather mask or render taken from frames in which water moves sees the water."""
    if "SM" not in _C:
        man = jload(DATA / "manifest.json")
        idx, tab = ids_built()
        if not man.get("water") or os.environ.get("PH_EXCLUDE_SELF_MOVING") != "1":    # R-C9-196: NOT adopted (off by default)
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
    lit = np.asarray(Image.open(io.BytesIO(open(DATA / "lit.bin", "rb").read())).convert("L"), np.float32) / 255.0
    lit = np.asarray(Image.fromarray((lit * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255.0
    lin = srgb_to_lin(R)
    mul = np.array(jload(DATA / "manifest.json")["shadow_mul"]["linear"])   # the pilot's measured shadow
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
    paths = S5.canvases(CANVAS_PREFIX)
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
        rr = float(o["p6a_match_radius_m"]) * PPM_V1         # an opening whose match disc reaches into the window counts
        if -rr <= x < W + rr and -rr <= y < H + rr:
            out.append({"id": o["id"], "xy": (x, y), "radius_m": float(o["p6a_match_radius_m"]),
                        "corners": [tuple(o["corners_px"][k]) for k in ("bottom_a", "bottom_b", "top_b", "top_a")] if o.get("corners_px") else None})
    return out


def p6a():   # NB: writes results/p6a_triage_pilot.jsonl -- move per build (pilot-1 record lives there)
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
    od = OUT / "p6a_triage"
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
        cls, names = class_map()
        idx, tab = ids_built()
        xi, yi = int(round(x)), int(round(y))
        cw0 = cls[max(yi - 30, 0):yi + 30, max(xi - 30, 0):xi + 30]
        water = {names.index(n) for n in ("sea", "ice", "lead", "ice_mid", "tide_ice", "shore_ice", "stream") if n in names}
        in_water = float(np.isin(cw0, list(water)).mean()) >= 0.5
        verdict = "declared" if matched else ("PENDING conductor triage (water class: R-C9-194)" if in_water
                                              else "invented (outside dark structures: auto-fail)")
        cw = cls[max(yi - 30, 0):yi + 30, max(xi - 30, 0):xi + 30]
        u_, n_ = np.unique(cw, return_counts=True)
        what = {"guide_class_share_0.6m": {names[a]: round(float(b) / cw.size, 3) for a, b in zip(u_, n_)},
                "id_at_centroid": tab[int(idx[yi, xi])]["id"] if int(idx[yi, xi]) in tab else "none (0)"}
        rows.append({"chunk": chunk, "candidate": cid, "candidate_px": [round(x), round(y)], "area_m2": round(f["area_m2"], 2),
                     "h_m": f["h_m"], "w_m": f["w_m"], "inside_dark_structure": False,
                     "crop_sha": O._sha_png(cr), "overlay_sha": O._sha_png(ova),
                     "nearest_declared": best["id"], "distance_m": round(dist, 2), "match_radius_m": best["radius_m"],
                     "verdict": verdict, "inside_water_class": in_water, "evidence": "", "ph_observation": what, "reader": "auto (pilot_harness.py, § 11 triage rule)",
                     "conductor_read": "PENDING (fallback (a), by eye)" if not matched else "n/a",
                     "image": str((od / (cid + ".png")).relative_to(FID)),
                     "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    with open(OUT / "p6a_triage.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    inv = [r for r in rows if r["verdict"].startswith("invented")]
    pend = [r["candidate"] for r in rows if r["verdict"].startswith("PENDING")]
    hit = sorted({r["nearest_declared"] for r in rows if r["verdict"] == "declared"})
    return save("p6a", {"T": T, "detector": "v0.1 (no prior), quarter scale", "declared_in_window": [d["id"] for d in dec],
                        "declared_found": hit, "candidates": len(rows), "unmatched": [r["candidate"] for r in inv],
                        "chunks_failing_by_rule": sorted({c for r in inv for c in r["chunk"]}), "rows": rows,
                        "pending_conductor_triage": pend,
                        "pass": (not inv) and not pend if not inv else False,
                        "verdict": ("PASS" if not pend else "PENDING conductor triage (%d water-class candidates)" % len(pend)) if not inv
                        else "FAIL by the § 11 rule pending the conductor's by-eye read (%d)" % len(inv)})


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
    lvl = jload(LEVELD / "level.json")
    hf = lvl["sim"]["heightfield"]
    Z = np.fromfile(LEVELD / hf["file"], dtype="<f4").reshape(hf["shape"])
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
    lvl = jload(LEVELD / "level.json")
    sn = jload(DATA / "manifest.json")["snow"]
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
    raw = np.fromfile(DATA / g["file"], dtype="<f4")
    mul = raw[:nx * nz].reshape(nz, nx)
    gi = np.clip(((X - g["origin_xz"][0]) / g["cell_m"]).astype(int), 0, nx - 1)
    gj = np.clip(((Zw - g["origin_xz"][1]) / g["cell_m"]).astype(int), 0, nz - 1)
    has = mul[gj, gi] > 0
    n = max(int(walk.sum()), 1)
    hf = lvl["sim"]["heightfield"]
    Zh = np.fromfile(LEVELD / hf["file"], dtype="<f4").reshape(hf["shape"])
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


# ---------------------------------------------------------------------------------------------------------- P9c sub-pixel
def _phase_subpx(a, b, up=20, normalise=True):
    """shift (dy, dx) with b(x) = a(x - d)... read as in p9's phase_shift(b, a): the integer peak of the normalised
    cross-power, refined by a locally UPSAMPLED inverse DFT (factor `up`, +-1.5 px around the peak; Guizar-Sicairos 2008)"""
    A = np.fft.fft2(a)
    B = np.fft.fft2(b)
    Rr = A * np.conj(B)
    if normalise:
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


def _lk_shift(I0, I1, w, iters=12):
    """translation s with I1(x + s) ~ I0(x) (so s = the motion of I0's content into I1), weighted iterative Lucas-Kanade"""
    s = np.zeros(2)
    gy, gx = np.gradient(I0)
    yy, xx = np.mgrid[0:I0.shape[0], 0:I0.shape[1]].astype(float)
    M = np.array([[np.sum(w * gy * gy), np.sum(w * gy * gx)], [np.sum(w * gx * gy), np.sum(w * gx * gx)]])
    for _ in range(iters):
        W1 = ndimage.map_coordinates(I1, [yy + s[0], xx + s[1]], order=3, mode="nearest")
        e = W1 - I0
        b = -np.array([np.sum(w * gy * e), np.sum(w * gx * e)])
        ds = np.linalg.solve(M + 1e-9 * np.eye(2), b)
        s += ds
        if np.hypot(*ds) < 1e-3:
            break
    return float(s[0]), float(s[1])


def floe_drift_v2(dirp, min_px=1500, pad=40, valid=None):
    """P9c RE-INSTRUMENTED (R-C9-196). Marker (ph_life.gd pilot branch): R = constant (the silhouette), G = aperiodic noise
    (the texture). Per floe:
      alpha_t = clip((R_t - R_hide) / (R_floe - R_hide), 0, 1)        (sub-pixel silhouette under MSAA; R_floe = the
                                                                        floe's own interior median)
      silhouette shift = upsampled NON-normalised cross-correlation of the two alpha maps in the floe's region
      texture shift    = the same on G inside the shared core, mean-removed and Gaussian-tapered (a hard shared window
                         correlates with itself at zero shift -- the calibrated instrument's blindness, § 29)
      drift = |silhouette shift - texture shift|; rest-pose UVs -> ~0, world-anchored UVs -> the silhouette's motion.
    Constructed self-test: `p9c_selftest()`."""
    m0, m1, hf = (load_rgb(dirp / n) for n in ("floe_m0.png", "floe_m1.png", "hide_floe.png"))
    rb0, rbh = m0[..., 0] - m0[..., 2], hf[..., 0] - hf[..., 2]
    k0 = ndimage.binary_opening((rb0 - rbh > 40) & (rb0 > 30), iterations=2)
    lab, n = ndimage.label(k0)
    rows = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None or (lab[sl] == i + 1).sum() < min_px:
            continue
        y0, y1 = max(sl[0].start - 12, 0), sl[0].stop + 12
        x0, x1 = max(sl[1].start - 12, 0), sl[1].stop + 12
        if valid is not None and not (y0 >= valid[1] and y1 <= valid[3] and x0 >= valid[0] and x1 <= valid[2]):
            continue                    # the floe's projection runs off the painted plate (clamped-edge streaks)
        p0 = lab[y0:y1, x0:x1] == i + 1
        # silhouette channel R - B: the marker is (0.95, noise, 0.5) -> R - B high and constant on the floe; the water's
        # white foam ring (R ~ B, animated) and the blue sea (R < B) both read ~0 or below
        R0 = m0[y0:y1, x0:x1, 0] - m0[y0:y1, x0:x1, 2]
        R1 = m1[y0:y1, x0:x1, 0] - m1[y0:y1, x0:x1, 2]
        Rh = hf[y0:y1, x0:x1, 0] - hf[y0:y1, x0:x1, 2]
        inner = ndimage.binary_erosion(p0, iterations=4)
        if inner.sum() < 500:
            continue
        rf = float(np.median(R0[inner]))
        den = np.maximum(rf - Rh, 10.0)
        a0, a1 = np.clip((R0 - Rh) / den, 0, 1), np.clip((R1 - Rh) / den, 0, 1)
        edge = ndimage.binary_dilation(p0 ^ ndimage.binary_erosion(p0), iterations=5)
        sil = _lk_shift(ndimage.gaussian_filter(a0, 1.5), ndimage.gaussian_filter(a1, 1.5), edge.astype(float))
        core = ndimage.binary_erosion(p0 & (a1 > 0.5), iterations=6)
        if core.sum() < 500:
            continue
        G0, G1 = m0[y0:y1, x0:x1, 1], m1[y0:y1, x0:x1, 1]
        t = _lk_shift(ndimage.gaussian_filter(G0, 1.0), ndimage.gaussian_filter(G1, 1.0), ndimage.gaussian_filter(core.astype(float), 2))
        rows.append({"px": int(p0.sum()), "silhouette_shift": [round(sil[0], 3), round(sil[1], 3)],
                     "texture_shift": [round(t[0], 3), round(t[1], 3)], "drift": round(math.hypot(sil[0] - t[0], sil[1] - t[1]), 3),
                     "motion": round(math.hypot(*sil), 3)})
    d = [r["drift"] for r in rows]
    return {"floes_measured": len(rows), "median_drift_px": round(float(np.median(d)), 3) if d else None,
            "max_drift_px": round(float(np.max(d)), 3) if d else None,
            "median_motion_px": round(float(np.median([r["motion"] for r in rows])), 3) if rows else None, "rows": rows}


def p9c_selftest():
    """constructed, as rendered: a 4x-supersampled floe (R = 240, G = aperiodic noise) over a moving sea, moved by a known
    sub-pixel offset; rest-pose (texture moves with it) and world-anchored (texture fixed) -- the same code path"""
    import tempfile
    SS, N = 4, 200
    NZ = ndimage.zoom(ndimage.gaussian_filter(np.random.default_rng(5).random((80, 80)), 1.0), 4 * SS, order=1)
    NZ = (NZ - NZ.min()) / (NZ.max() - NZ.min())

    def render(off, rest, t=0.0, floe_on=True):
        yy, xx = np.mgrid[0:N * SS, 0:N * SS] / SS
        sea = 40 + 10 * np.sin(xx / 7.0 + t) * np.cos(yy / 5.0)
        fl = (((yy - 100 - off[0]) / 40.) ** 2 + ((xx - 100 - off[1]) / 60.) ** 2 <= 1) & floe_on
        ty, tx = (yy - off[0], xx - off[1]) if rest else (yy, xx)
        G = 25 + 215 * ndimage.map_coordinates(NZ, [(ty + 20) * SS, (tx + 20) * SS], order=1, mode="nearest")
        img = np.stack([np.where(fl, 240, sea), np.where(fl, G, sea), np.where(fl, 128, sea)], -1)
        return img.reshape(N, SS, N, SS, 3).mean((1, 3))
    out = []
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        for off in ((0.4, 1.3), (1.7, -0.6), (0.0, 2.25), (-0.8, 0.3), (0.15, -0.2)):
            row = {"offset_px": off, "true_motion": round(math.hypot(*off), 3)}
            for nm, rest in (("rest_pose", True), ("world_anchored_RED", False)):
                Image.fromarray(render((0, 0), rest).astype(np.uint8)).save(d / "floe_m0.png")
                Image.fromarray(render(off, rest, 0.3).astype(np.uint8)).save(d / "floe_m1.png")
                Image.fromarray(render(off, rest, 0.9, floe_on=False).astype(np.uint8)).save(d / "hide_floe.png")
                r = floe_drift_v2(d)
                row[nm] = r["median_drift_px"]
            out.append(row)
    return out


def plate_rect_on_screen(view_uv, size=(1920, 1080)):
    """the screen rect showing plate px [0, W) x [0, H) at ground z = 0, for ph_life's play camera parked on view_uv
    (1:1 plate px per screen px; the aim at the screen centre)"""
    env = jload(GA / "guide_manifest.json")["envelope"]
    cx = (view_uv[0] - env["u"][0]) * PPM_V1
    cy = (env["v"][1] - view_uv[1]) * 80.3076
    x0, y0 = size[0] / 2 - cx, size[1] / 2 - cy
    return (max(0, int(math.ceil(x0))), max(0, int(math.ceil(y0))), min(size[0], int(x0 + W)), min(size[1], int(y0 + H)))


def p9c_measure(dirp, view_uv, margin=12):
    """R-C9-197 pre-registered P9c reading (calibration.md § 31): every marker pair in dirp; floes wholly inside the plate's
    screen rect (margin px); per pair the median floe drift; the statistic = the median over pairs"""
    x0, y0, x1, y1 = plate_rect_on_screen(view_uv)
    valid = (x0 + margin, y0 + margin, x1 - margin, y1 - margin)
    pairs = sorted({p.name[len("floe_m0"):-4] for p in pathlib.Path(dirp).glob("floe_m0*.png")})
    import shutil
    import tempfile
    rows = []
    for sfx in pairs:
        with tempfile.TemporaryDirectory() as td:
            for a, b in (("floe_m0", "floe_m0"), ("floe_m1", "floe_m1"), ("hide_floe", "hide_floe")):
                src = pathlib.Path(dirp) / ((a + sfx if a != "hide_floe" else a) + ".png")
                shutil.copy(src, pathlib.Path(td) / (b + ".png"))
            r = floe_drift_v2(pathlib.Path(td), valid=valid)
        rows.append({"pair": sfx or "_0", "floes": r["floes_measured"], "median_drift_px": r["median_drift_px"],
                     "median_motion_px": r["median_motion_px"], "rows": r["rows"]})
    d = [r["median_drift_px"] for r in rows if r["median_drift_px"] is not None]
    return {"valid_rect": valid, "pairs": len(rows), "pairs_measured": len(d),
            "median_drift_px": round(float(np.median(d)), 3) if d else None, "max_pair_drift_px": round(float(max(d)), 3) if d else None,
            "pass": (float(np.median(d)) <= 0.25) if d else None, "per_pair": rows}


# ---------------------------------------------------------------------------------------------------------- F-4 (§ 38)
def flow_geo(dirp, bar=2.064):
    """P9 flow, F-4 re-instrumented: the water mask and the floe exclusion come from the GEOMETRY shot geo_mask.png
    (sea meshes flat green, floes flat red, same camera, one frame) -- no cross-time difference decides membership.
      W = green px (G > 200, R < 60, B < 60), eroded 3 px, minus red (floes) dilated 6 px
      flow = mean |f1 - f0| over W; RED = the hidden-water pair over the same W
      noise = mean |f1 - f0| over px outside W, the floes, the heather (dilated) and the self-moving px (as sway())"""
    import p9_p10_life_perf as L
    G = load_rgb(dirp / "geo_mask.png")
    green = (G[..., 1] > 200) & (G[..., 0] < 60) & (G[..., 2] < 60)
    red = (G[..., 0] > 200) & (G[..., 1] < 60) & (G[..., 2] < 60)
    W = ndimage.binary_erosion(green, iterations=3) & ~ndimage.binary_dilation(red, iterations=6)
    f0, f1 = load_rgb(dirp / "f0.png"), load_rgb(dirp / "f1.png")
    d = L._d(f1, f0)
    hh = load_rgb(dirp / "hide_heather.png")
    selfmove = ndimage.binary_dilation(L._d(hh, load_rgb(dirp / "hide_heather_b.png")) > 3, iterations=3)
    heather = ndimage.binary_dilation(L._d(f0, hh) > 12, iterations=2)
    still = ~ndimage.binary_dilation(green | red, iterations=6) & ~heather & ~selfmove
    flow = float(d[W].mean()) if W.any() else 0.0
    noise = float(d[still].mean())
    red_flow = float(L._d(load_rgb(dirp / "hide_water_b.png"), load_rgb(dirp / "hide_water.png"))[W].mean()) if W.any() else None
    return {"water_px_geo": int(W.sum()), "flow": round(flow, 3), "noise": round(noise, 3), "RED_hidden_water_flow": None if red_flow is None else round(red_flow, 3),
            "pass": flow >= bar and flow >= 3 * noise, "RED_pass": None if red_flow is None else (red_flow >= bar and red_flow >= 3 * noise)}


def floe_view_choose(floe_ids, margin=12, step_m=0.5, size=(1920, 1080)):
    """P9c floe-field view, F-4 (§ 38): over a 0.5 m grid of view centres (uv) inside the plate, count the bobbing floes
    whose ID-render bbox (ids_built, plate px) + margin lies wholly inside BOTH the plate and the 1920 x 1080 screen;
    the view = argmax count (ties: the smallest distance to the counted floes' mean centre). Deterministic, from the
    build's own ID render, decided BEFORE any marker shot."""
    idx, tab = ids_built()
    boxes = []
    for k, v in tab.items():
        if v["id"] in floe_ids:
            lab_, nlab = ndimage.label(idx == k)            # ice_floes_bob is ONE slab group: each component is a floe
            for j, sl in enumerate(ndimage.find_objects(lab_)):
                if sl is None or (lab_[sl] == j + 1).sum() < 400:
                    continue
                boxes.append(("%s#%d" % (v["id"], j), sl[1].start - margin, sl[0].start - margin, sl[1].stop - 1 + margin, sl[0].stop - 1 + margin))
    env = jload(GA / "guide_manifest.json")["envelope"]
    u0, v1 = env["u"][0], env["v"][1]
    inplate = [b for b in boxes if b[1] >= 0 and b[2] >= 0 and b[3] < W and b[4] < H]
    best = None
    for u in np.arange(u0 + 9.6, u0 + W / PPM_V1 - 9.6, step_m):
        for v in np.arange(v1 - H / 80.3076 + 6.8, v1 - 6.8, step_m):
            cx, cy = (u - u0) * PPM_V1, (v1 - v) * 80.3076
            x0, y0 = cx - size[0] / 2, cy - size[1] / 2
            inside = [b for b in inplate if b[1] >= x0 and b[2] >= y0 and b[3] < x0 + size[0] and b[4] < y0 + size[1]]
            if not inside:
                continue
            mx = np.mean([(b[1] + b[3]) / 2 for b in inside]); my = np.mean([(b[2] + b[4]) / 2 for b in inside])
            key = (len(inside), -math.hypot(cx - mx, cy - my))
            if best is None or key > best[0]:
                best = (key, (round(float(u), 3), round(float(v), 3)), [b[0] for b in inside])
    return {"floes_with_ids": len(boxes), "floes_wholly_in_plate": [b[0] for b in inplate],
            "view_uv": best[1] if best else None, "floes_in_view": best[2] if best else [], "n": len(best[2]) if best else 0,
            "sufficient": bool(best and len(best[2]) >= 3)}


def p9c_measure_v2(dirp, view_uv, margin=12, min_motion=0.25):
    """F-4 (§ 38): every (floe, pair) sample with silhouette motion >= 0.25 px, floes wholly in the plate's screen rect;
    statistic = the median drift over all counted samples (also per floe)"""
    r = p9c_measure(dirp, view_uv, margin)
    samples = [(x["px"], y["drift"]) for pr in r["per_pair"] for y in pr["rows"] for x in [y] if y["motion"] >= min_motion]
    d = [s[1] for s in samples]
    r["samples_counted"] = len(d)
    r["median_drift_samples_px"] = round(float(np.median(d)), 3) if d else None
    r["pass_v2"] = (float(np.median(d)) <= 0.25) if d else None
    return r


# ---------------------------------------------------------------------------------------------------------- P4 (§ 38)
def p4_v38():
    """P4 under the § 38 pre-registration (R-C9-203): ICE against sketch A's mere (palette dE <= 9.40, gated b* <= 2;
    spectrum at 24 px/m <= 0.116); SNOW and ROCK against v1 (frozen § 3 bars); coastal snow additionally reported
    against the pilot's inland snow (non-binding). REED: no v1 class -- reported against v1's nearest, heather (v1's
    painted tuft pixels), advisory (no frozen bar)."""
    import p4_texture as T
    import p4_forensic as F
    masks_v1, static_v1 = T.v1_classes()
    per = T.v1_pool(None, masks_v1, static_v1)
    bars = T.v1_bars(per)
    bind = {c: bars[c] for c in ("snow", "rock")}
    bind["cellularity"] = bars["cellularity"]
    idx, tab = ids_built()
    cls, names = class_map()
    ni = {n: i for i, n in enumerate(names)}
    tf = tufts()
    g = ground_mask() & ~tf
    rock = np.isin(idx, [k for k, v in tab.items() if v["class"] == "rock" and v.get("piece") in ("model", "instance", "group") or
                         (v["class"] == "rock" and str(v.get("piece", "")).startswith("instance"))])
    masks = {"snow": g & (cls == ni["snow"]), "rock": rock}
    static = ~(np.asarray(Image.open(PT / "heather_mask.png").convert("L")) > 20) & ~tf
    P = painting()
    lab = rgb_to_lab(P)
    rows = {}
    for key, (x0, y0, x1, y1) in CHUNKS:
        st = T.stats(P[y0:y1, x0:x1], {c: m[y0:y1, x0:x1] for c, m in masks.items()}, static[y0:y1, x0:x1])
        rows[key] = T.score(st, per, bind)
    # ICE vs sketch A
    SKI, skm, MERE = F.sketch_mere()
    lsk = rgb_to_lab(SKI)
    sk = skm & (lsk[..., 2] <= 2.0)
    sk_med = np.median(lsk[sk], 0)
    # § 48 (a): the ice reference is FROZEN at the PS4 mere colour (Matt R-C9-262, measured on pilot 4 at § 47); 'self'
    # (re-deriving it from the build under test) is RETIRED (jack-ryan pilot-4 Gate-2 C-1). 'sketchA' = the § 38 reading.
    ice_ref_mode = os.environ.get("PH_ICE_REF", "ps4_frozen")
    if ice_ref_mode == "self":
        raise SystemExit("PH_ICE_REF=self is RETIRED (s48 (a)); use ps4_frozen")
    W_ = lambda mk: T.windows(mk, frac=0.7, step=32)
    sk_spec = np.array(T.spectrum_shape(luma(SKI), W_(sk)))
    f = PPM_V1 / 24.0
    Ps = np.asarray(Image.fromarray(np.clip(P, 0, 255).astype(np.uint8)).resize((int(W / f), int(H / f)), Image.BOX)).astype(np.float32)
    ls = rgb_to_lab(Ps)
    ice_full = g & (cls == ni["ice"])
    allice = ndimage.binary_erosion(ice_full, iterations=3) & (lab[..., 2] <= 2.0)
    ref_med = np.array([64.58, -2.75, -21.49]) if ice_ref_mode == "ps4_frozen" else sk_med
    ice_rows = {}
    for key, (x0, y0, x1, y1) in CHUNKS:
        m = np.zeros((H, W), bool)
        m[y0:y1, x0:x1] = ice_full[y0:y1, x0:x1]
        m = ndimage.binary_erosion(m, iterations=3) & (lab[..., 2] <= 2.0)
        if m.sum() < 20000:
            continue
        med = np.median(lab[m], 0)
        dE_sk = float(np.linalg.norm(med - sk_med))
        dE = float(np.linalg.norm(med - ref_med))
        ms = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((Ps.shape[1], Ps.shape[0]), Image.BOX)) > 200
        ms &= ls[..., 2] <= 2.0
        sp = T.spectrum_shape(luma(Ps), W_(ms))
        dS = float(np.sqrt(np.mean((np.array(sp) - sk_spec) ** 2))) if sp is not None else None
        hel = T.hellinger(T.lab_hist(lab[m]), T.lab_hist(lsk[sk]))
        ice_rows[key] = {"px": int(m.sum()), "median_lab": med.round(1).tolist(), "dE_vs_reference": round(dE, 2),
                         "dE_vs_sketchA_reported": round(dE_sk, 2), "dE_bar": 9.40,
                         "spectrum_rms_at_24ppm": None if dS is None else round(dS, 3), "spectrum_bar": 0.116,
                         "windows_at_24ppm": len(W_(ms)), "hellinger_reported": round(hel, 3),
                         "pass": dE <= 9.40 and (dS is None or dS <= 0.116)}
    # coastal / inland snow diagnostic
    coastal = {}
    for key, (x0, y0, x1, y1) in CHUNKS:
        c = cls[y0:y1, x0:x1]
        coastal[key] = bool(sum(float((c == ni[n]).mean()) for n in ("shingle", "shore_ice", "sea")) >= 0.02)
    inland_px = np.zeros((H, W), bool)
    for key, (x0, y0, x1, y1) in CHUNKS:
        if not coastal[key]:
            inland_px[y0:y1, x0:x1] |= masks["snow"][y0:y1, x0:x1]
    diag = {}
    if inland_px.sum() > 20000:
        ref = T.lab_hist(lab[ndimage.binary_erosion(inland_px, iterations=3)])
        for key, (x0, y0, x1, y1) in CHUNKS:
            if coastal[key]:
                m = np.zeros((H, W), bool)
                m[y0:y1, x0:x1] = ndimage.binary_erosion(masks["snow"][y0:y1, x0:x1], iterations=3)
                if m.sum() >= 20000:
                    diag[key] = round(T.hellinger(T.lab_hist(lab[m]), ref), 3)
    # REED, advisory: against v1's painted tufts (heather)
    PW = _pw_mod()
    V8 = np.asarray(Image.open(PW.PAINTING).convert("RGB"))
    vidx, _ = PW.id_index()
    vh, vs = PW.tuft_classes(V8, vidx == 0)
    vt = ndimage.binary_opening(vh | vs, iterations=1)
    vref = T.lab_hist(rgb_to_lab(V8.astype(np.float32))[ndimage.binary_erosion(vt, iterations=1)])
    reed = ndimage.binary_erosion((cls == ni["reed"]), iterations=2)
    reed_rows = {}
    for key, (x0, y0, x1, y1) in CHUNKS:
        m = np.zeros((H, W), bool)
        m[y0:y1, x0:x1] = reed[y0:y1, x0:x1]
        if m.sum() >= 5000:
            reed_rows[key] = {"px": int(m.sum()), "hellinger_vs_v1_heather_tufts": round(T.hellinger(T.lab_hist(lab[m]), vref), 3)}
    binding_fail = [(k, c) for k, r in rows.items() for c, v in r["classes"].items() if v.get("pass") is False]
    binding_fail += [(k, "ice (sketch A)") for k, r in ice_rows.items() if not r["pass"]]
    return save("p4", {"rule": "calibration.md s38: ice palette dE <= 9.40 (gated b*<=2) vs the ice reference; spectrum@24ppm <= 0.116 vs sketch A; snow + rock vs v1 frozen s3 bars",
                       "ice_reference": {"mode": ice_ref_mode, "median_lab": ref_med.round(2).tolist(),
                                         "note": "R-C9-262 Matt-ruled exception, FROZEN at s48 (a): the PS4 mere colour Lab (64.58, -2.75, -21.49); NOT a threshold tune; sketch A dE reported" if ice_ref_mode == "ps4_frozen" else "sketch A (s38)"},
                       "sketchA_ice_median": sk_med.round(1).tolist(), "chunks_snow_rock": rows, "ice": ice_rows,
                       "coastal_chunks": [k for k, v in coastal.items() if v], "coastal_snow_vs_inland_hellinger_diagnostic": diag,
                       "reed_advisory": {"nearest_v1_class": "heather (v1's painted tuft px)", "rows": reed_rows},
                       "binding_fails": binding_fail, "pass": not binding_fail})


def _pw_mod():
    import importlib.util
    spec = importlib.util.spec_from_file_location("pw_v1_readonly", BF / "tools/paint_world_prep.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------------------------------------------------- P5 v2 (§ 44)
def p5v2_pilot():
    """P5 v2 as pre-registered (§ 44): BINDS on a1 (pinned raw canvases, bar 9.569) + b (the build's flags-ON stitched
    painting, <= 0.799). REPORTED: a2, c (flags-on = the build painting; flags-off = PT's Tier-B stitch with all flags 0 on
    the same pinned set), raw overlap MAD + a 1:1 crop of every join over 13.09."""
    import p5v2 as V
    import p5_seams as S5
    cal = jload(PH / "results/p5v2_calibration.json")
    bars = cal["bars_v1"]
    mj = jload(PT / os.environ.get("PH_P5_MANIFEST", "build_manifest_ps3a.json"))
    man = mj["chunks"]
    paths = {k: str(ART / v["file"]) for k, v in man.items()}
    bad = [k for k, p in paths.items() if V.sha(p) != man[k]["sha256"]]
    assert not bad, "pinned canvas sha mismatch: %s" % bad
    a = V.a_set(paths)
    P = painting()
    b = S5.seam_vis(P, 3, 3)
    c_on = V.c_measure(P, list(paths))
    off = V.SCR / ("%s_flagsoff.png" % jload(PT / os.environ.get("PH_P5_MANIFEST", "build_manifest_ps3a.json")).get("prefix", "PS3A"))
    V.stitch(mj.get("prefix", "BV2F-PS3A"), 3, 3, off, dict(V.OFF, BV2F_DEV24="0"))
    c_off = V.c_measure(load_rgb(off), list(paths))
    fa1 = [r["join"] for r in a if r["a1_max"] > bars["a1"]]
    fb = [x["seam"] for x in b if x["score"] > 0.799]
    crops = []
    od = OUT / "p5_crops"
    od.mkdir(parents=True, exist_ok=True)
    for r in a:
        if r["raw_mad"] > 13.09:
            k1, k2 = r["join"].replace("|", "/").split("/")
            c1, r1 = map(int, k1.split("_"))
            if "|" in r["join"]:
                x0, y0 = 1280 * (c1 + 1) - 128, 768 * r1 + 256
                box = (x0, y0, x0 + 512, y0 + 512)
            else:
                x0, y0 = 1280 * c1 + 256, 768 * (r1 + 1) - 128
                box = (x0, y0, x0 + 1024, y0 + 512)
            # the worst a1 segment's place along the join, if it lies elsewhere
            seg = int(np.argmax(r["a1_segments"]))
            if "|" in r["join"]:
                y0 = min(max(768 * r1 + seg * 128 - 192, 0), H - 512)
                box = (x0, y0, x0 + 512, y0 + 512)
            else:
                x0 = min(max(1280 * c1 + seg * 128 - 448, 0), W - 1024)
                box = (x0, y0, x0 + 1024, y0 + 512)
            fn = od / ("join_%s_rawMAD%.2f_1to1.jpg" % (r["join"].replace("|", "-").replace("/", "-"), r["raw_mad"]))
            Image.fromarray(np.clip(P[box[1]:box[3], box[0]:box[2]], 0, 255).astype(np.uint8)).save(fn, quality=92)
            crops.append({"join": r["join"], "raw_mad": r["raw_mad"], "a1_max": r["a1_max"], "crop": str(fn.relative_to(FID)), "box_xyxy": box})
    tone_over_on = [(x["boundary"], x["chunk"], x["tone_max"]) for x in c_on if x["tone_max"] is not None and x["tone_max"] > bars["c_tone"]]
    tone_over_off = [(x["boundary"], x["chunk"], x["tone_max"]) for x in c_off if x["tone_max"] is not None and x["tone_max"] > bars["c_tone"]]
    return save("p5v2", {"rule": "calibration.md s44: PASS iff every a1 segment <= %.3f (pinned raw canvases) and every b seam <= 0.799 (flags-ON build painting); a2, c, raw MAD reported" % bars["a1"],
                         "bars_v1": bars, "manifest_ok": True, "painting_sha": sha256(PT / "painting.png"),
                         "a": a, "a1_max": max(r["a1_max"] for r in a), "a1_over": fa1,
                         "b": b, "b_max": max(x["score"] for x in b), "b_over": fb,
                         "reported_a2_max": max(r["a2_max"] for r in a), "reported_raw_mad": {r["join"]: r["raw_mad"] for r in a},
                         "reported_c_flags_on": {"tone_max": V.c_max(c_on, "tone"), "grain_max": V.c_max(c_on, "grain"), "tone_over_v1_bar": tone_over_on},
                         "reported_c_flags_off": {"tone_max": V.c_max(c_off, "tone"), "grain_max": V.c_max(c_off, "grain"), "tone_over_v1_bar": tone_over_off},
                         "c_rows_on": c_on, "c_rows_off": c_off, "crops_raw_mad_over_13.09": crops,
                         "pass": not fa1 and not fb})


# ---------------------------------------------------------------------------------------------------------- P11 v3 on the pilot
def p11v3():
    """P11 v3 (§ 38/39; binding): 40 scored + 10 repeats + 12 catch (v1 vs R-C9-159), judge-ready dir; key kept apart.
    Content control: REED is build-specific (v1 has no reeds) -> EXCLUDED, like sea/wreck/hall/cliff (R-C9-171 rule)."""
    import p11_abx as X
    import p11_abx3 as X3
    if "reed" not in X.EXCLUDED:
        X.EXCLUDED = tuple(X.EXCLUDED) + ("reed",)
    st = sorted((FID / "pt/pilot_stills").glob("pilot_[0-9][0-9].png"))
    X._centres()
    for v in jload(FID / "pt/pilot_stills/views.json")["views"].values():
        X._CENTRES[v["png"]] = tuple(v["camera"]["centre_ground_uv"])
    name = os.environ.get("PH_P11_SET", "pilot3_v1_vs_pilot")
    r = X3.build3(name, st, seed=253)
    return save("p11v3_build", dict(r, stills=[p.name for p in st], excluded=list(X.EXCLUDED),
                                    key="fid/ph/p11/keys/abx3_%s.json" % name))

ROWS["p4v38"] = p4_v38
ROWS["p5v2"] = p5v2_pilot
ROWS["p11v3"] = p11v3

if __name__ == "__main__":
    want = sys.argv[1:] or [k for k in ROWS if k != "p9p10"]
    for k in want:
        r = ROWS[k]()
        brief = {kk: vv for kk, vv in r.items() if kk in ("pass", "verdict", "worst", "median_iou", "min", "whole_window", "candidates",
                                                            "unmatched", "chunks_failing_by_rule", "binding_fails", "value", "worst_class", "below_bar", "trials", "repeats", "images", "UNDERPOWERED")}
        print(k, json.dumps(brief, default=str)[:600])

