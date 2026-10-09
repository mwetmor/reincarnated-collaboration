#!/usr/bin/env python3
"""BV2F PT (R-C9-281): Phase 3' MANUAL per-wave QA (calibration s48 (e)), read-only on the canvases, PH's instruments
imported (common / p5v2 / p4_texture / p6_geometry):
  P6a       the v0.1 opening detector (T = s8 v1 ceiling, quarter scale) on each new canvas at its plate position; every
            candidate matched to LV's declared openings (s11 radius); unmatched = INVENTED
  a1 raw    per join touching a new chunk, the full v1 band (s44: p5v2.a_pair, band None), bar 9.569; raw MAD reported
  P4        per new chunk: snow (class snow on ground ids, less v1's tuft classifier) and rock (rock-class models) vs v1's
            pool with the frozen s3 bars; support rule s50 (b): snow < 100 windows / rock < 3 windows = 'insufficient
            support' (not judged, never PASS)
  sheets    contact sheet of the wave's canvases; a stitched PREVIEW: the painted chunks in the smallest grid holding them,
            the unpainted cells filled with the pinned guide (stand-ins, BV2F-PH3PV-*, STAND_IN.json), DEV-23/25/26/27
            on, DEV-26 PIN on, DEV-24 (read pins) on
    python3 fid/pt/tools/ph3_wave_qa.py <wave tag> <chunk> [<chunk> ...]   -> fid/pt/ph3/qa_<tag>/"""
import hashlib, json, math, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
Image.MAX_IMAGE_PIXELS = None
FIDS = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
sys.path.insert(0, FIDS + "/ph/harness")
from common import *  # noqa
import p5v2 as V
import p4_texture as T
import p6_geometry as G
FIDS = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
A9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts"
C9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
tag, keys = sys.argv[1], sys.argv[2:]
OUT = FIDS + "/pt/ph3/qa_" + tag
os.makedirs(OUT, exist_ok=True)
CFG = FIDS + "/pt/pilot/cfg_bv2a_ph3.json"
cfg = json.load(open(CFG))
PX = cfg["prefix"]


def src(k):
    for d in ["%s-%s%s" % (PX, k, s_) for s_ in cfg.get("src_suffixes", [])] + ["%s-%s-r1" % (PX, k), "%s-%s" % (PX, k)]:   # the stitch's own src() order
        p = "%s/%s/%s-%s.png" % (A9, d, PX, k)
        if os.path.exists(p):
            return p


PINS = json.load(open(FIDS + "/pt/ph3/pins_ph3.json"))   # R-C9-284: the CURRENT Phase 3' pins (guide / ids / class copies, LV commit)
B2 = os.path.dirname(FIDS)
man = json.loads(subprocess.check_output(["git", "-C", FIDS, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json" % PINS["lv_commit"]]))
tab = {int(k): v for k, v in man["id_table"].items()}
ids = np.asarray(Image.open(os.path.join(B2, PINS["ids"]["pinned_copy"])).convert("RGB")).astype(np.int64)
gid = (ids[..., 0] << 16) | (ids[..., 1] << 8) | ids[..., 2]
cls = np.asarray(Image.open(os.path.join(B2, PINS["class"]["pinned_copy"])))
ni = {n: i for i, n in enumerate(man["class"]["classes"])}
ground = np.isin(gid, [k for k, v in tab.items() if v["id"].startswith(("ground_", "carved_"))])
rockid = np.isin(gid, [k for k, v in tab.items() if v["class"] == "rock" and (v.get("piece") in ("model", "instance", "group") or str(v.get("piece", "")).startswith("instance"))])
import importlib.util
spec = importlib.util.spec_from_file_location("pw_v1_readonly", C9 + "/barrow_full/tools/paint_world_prep.py")
pw = importlib.util.module_from_spec(spec); spec.loader.exec_module(pw)
masks_v1, static_v1 = T.v1_classes()
per = T.v1_pool(None, masks_v1, static_v1)
bars = T.v1_bars(per)
Tp6 = jload(PH / "results/p6.json")["invention"]["T_v1_ceiling"]
dec = [{"id": o["id"], "xy": tuple(o["centre_px"]), "radius_m": float(o["p6a_match_radius_m"])}
       for o in json.loads(subprocess.check_output(["git", "-C", FIDS, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/declared_openings.json" % PINS["lv_commit"]]))["openings"]]
res = {"_what": __doc__.split("\n")[0], "wave": tag, "chunks": {}, "joins": {}}
# s51 (R-C9-299/300): pilot-side joins are read with the pilot side SUBSTITUTED by DEV-29's context_patch -- the real
# pinned inputs, sha-checked, and the substitution checked on them first (changed px subset of mask, == patched there)
PILOT = {"%d_%d" % (c_, r_) for c_ in range(3) for r_ in range(3)}
CP = cfg.get("context_patch")
SUBST = None
if CP:
    for f_, s_ in ((CP["painting"], CP["painting_sha256"]), (CP["mask"], CP["mask_sha256"])):
        assert hashlib.sha256(open(f_, "rb").read()).hexdigest() == s_, "s51 STOP: %s is not the pinned file" % f_
    _PP = np.asarray(Image.open(CP["painting"]).convert("RGB")).astype(np.float32)
    _MM = np.asarray(Image.open(CP["mask"])) > 127
    chk = {}
    for kk in ("0_2", "1_2", "2_2"):
        A_ = V.load(src(kk)); A2_ = V.context_patch(A_, kk, _PP, _MM)
        c_, r_ = map(int, kk.split("_")); mc = np.zeros((1024, 1536), bool)
        hh, ww = min(1024, _MM.shape[0] - 768 * r_), min(1536, _MM.shape[1] - 1280 * c_)
        mc[:hh, :ww] = _MM[768 * r_:768 * r_ + hh, 1280 * c_:1280 * c_ + ww]
        ch_ = np.any(A2_ != A_, -1)
        chk[kk] = {"mask_px": int(mc.sum()), "changed_px": int(ch_.sum()), "changed_outside_mask": int((ch_ & ~mc).sum()),
                   "inside_equals_patched": bool(np.array_equal(A2_[mc], np.pad(_PP[768 * r_:768 * r_ + 1024, 1280 * c_:1280 * c_ + 1536], ((0, 1024 - hh), (0, 1536 - ww), (0, 0)))[mc]))}
    res["s51_substitution_check"] = chk
    assert all(v["changed_outside_mask"] == 0 and v["inside_equals_patched"] for v in chk.values()), "s51 STOP: substitution check failed"
    SUBST = lambda kk, im: V.context_patch(im, kk, _PP, _MM) if kk in PILOT else im
for k in keys:
    c, r = map(int, k.split("_"))
    x0, y0 = 1280 * c, 768 * r
    p = src(k)
    im = V.load(p)
    row = {"canvas": os.path.relpath(p, A9), "sha256": V.sha(p)}
    q = np.asarray(Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).resize((384, 256), Image.BOX), np.float32)
    cands = []
    for f in G.openings(q, PPM_V1 * G.SC, Tp6):
        x, y = f["xy"][0] / G.SC + x0, f["xy"][1] / G.SC + y0
        best = min(dec, key=lambda d: math.hypot(x - d["xy"][0], y - d["xy"][1]))
        dist = math.hypot(x - best["xy"][0], y - best["xy"][1]) / PPM_V1
        cands.append({"plate_xy": [round(x), round(y)], "nearest_declared": best["id"], "dist_m": round(dist, 2), "matched": dist <= best["radius_m"]})
    row["P6a"] = {"candidates": cands, "invented": sum(not c_["matched"] for c_ in cands)}
    sl = (slice(y0, y0 + 1024), slice(x0, x0 + 1536))
    P8 = np.clip(im, 0, 255).astype(np.uint8)
    h, s = pw.tuft_classes(P8, ground[sl])
    tufts = ndimage.binary_opening(h | s, iterations=1)
    m = {"snow": ground[sl] & ~tufts & (cls[sl] == ni["snow"]), "rock": rockid[sl]}
    st = T.stats(im, m, ~tufts)
    sc = T.score(st, per, {"snow": bars["snow"], "rock": bars["rock"], "cellularity": bars["cellularity"]})
    p4 = {}
    for cn, wmin in (("snow", 100), ("rock", 3)):
        nwin = len(T.windows(ndimage.binary_erosion(m[cn], iterations=3)))
        e = sc["classes"].get(cn)
        if nwin < wmin:
            p4[cn] = {"windows": nwin, "verdict": "insufficient support (not judged)", "w_min": wmin, "reading": e}
        else:
            p4[cn] = {"windows": nwin, "verdict": "PASS" if e and e.get("pass") else "FAIL", "w_min": wmin, "reading": e}
    row["P4"] = p4
    # R-C9-288 GUARD: the s46 snow palette on chunks with enough snow support (>= 100 windows) vs v1's range; lit a*/b* or the
    # peach share outside v1's range = STOP
    if p4["snow"]["windows"] >= 100:
        import snow_parity as SP
        sp = SP.chunk_stats(P8.astype(np.float64), rgb_to_lab(P8.astype(np.float64)), m["snow"], luma(P8.astype(np.float64)))
        L = rgb_to_lab(P8.astype(np.float64)); mm = ndimage.binary_erosion(m["snow"], iterations=3)
        lit = mm & (L[..., 0] >= np.median(L[..., 0][mm]))
        peach = float(((L[..., 1] > 2) & (L[..., 2] > 4))[lit].mean())
        V1R = json.load(open(FIDS + "/ph/results/pilot3/snow_parity.json"))["summary"]
        rng = {k: (V1R[k]["v1_min"], V1R[k]["v1_max"]) for k in ("lit_a", "lit_b", "shadow_a")}
        rng["peach_share_of_lit"] = (0.381, 0.973)   # v1's own per-chunk range (fid/pt/ps4_dry/snow_ice.json, R-C9-261)
        vals = {"lit_a": sp["lit_a"], "lit_b": sp["lit_b"], "shadow_a": sp["shadow_a"], "peach_share_of_lit": round(peach, 3)}
        inside = {k: (v is not None and rng[k][0] <= v <= rng[k][1]) for k, v in vals.items()}
        row["snow_palette"] = {"values": vals, "v1_range": rng, "inside": inside,
                               "STOP": not (inside["lit_a"] and inside["lit_b"] and inside["peach_share_of_lit"])}
    else:
        row["snow_palette"] = {"not_measured": "snow support %d < 100 windows" % p4["snow"]["windows"]}
    res["chunks"][k] = row
    # joins touching this chunk (left / top neighbours; right / bottom if painted)
    for (dc, dr, horiz) in ((-1, 0, True), (0, -1, False), (1, 0, True), (0, 1, False)):
        n = "%d_%d" % (c + dc, r + dr)
        if not (0 <= c + dc < 5 and 0 <= r + dr < 5) or src(n) is None:
            continue
        a, b = (n, k) if (dc < 0 or dr < 0) else (k, n)
        jn = a + ("|" if horiz else "/") + b
        if jn in res["joins"]:
            continue
        rr = V.a_pair(V.load(src(a)), V.load(src(b)), horiz, None)
        row_ = {"a1_max": round(max(rr["a1"]), 3), "a1_segments": [round(x, 3) for x in rr["a1"]], "raw_mad": rr["raw_mad"], "bar": 9.569}
        if SUBST is not None and (a in PILOT) != (b in PILOT):   # s51: a pilot-side join -- the substituted a1 binds
            rs = V.a_pair(SUBST(a, V.load(src(a))), SUBST(b, V.load(src(b))), horiz, None)
            row_ = {"a1_max": round(max(rs["a1"]), 3), "a1_segments": [round(x, 3) for x in rs["a1"]], "raw_mad": rs["raw_mad"], "bar": 9.569,
                    "binding": "s51 substituted (pilot side = raw + context_patch)", "plain_raw_a1_REPORT_ONLY": round(max(rr["a1"]), 3)}
        row_["verdict"] = "PASS" if row_["a1_max"] <= 9.569 else "FAIL"
        res["joins"][jn] = row_
    # s51 diagonal corner joins (the upper-left neighbour's corner pasted as context): bar full 4.809 (pilot-side, binding)
    if r > 0 and c > 0 and src("%d_%d" % (c - 1, r - 1)):
        ul = "%d_%d" % (c - 1, r - 1)
        if SUBST is not None and ul in PILOT:
            rd = V.a_pair_diag(SUBST(ul, V.load(src(ul))), V.load(src(k)))
            rr_ = V.a_pair_diag(V.load(src(ul)), V.load(src(k)))
            res["joins"][ul + "\\" + k] = {"a1_max": round(max(rd["a1"]), 3), "a1_segments": [round(x, 3) for x in rd["a1"]], "raw_mad": rd["raw_mad"],
                                         "bar": 4.809, "binding": "s51 diagonal corner, substituted", "plain_raw_a1_REPORT_ONLY": round(max(rr_["a1"]), 3),
                                         "verdict": "PASS" if max(rd["a1"]) <= 4.809 else "FAIL"}
            if ul + "\\" + k != "2_2\\3_3":   # s51 names only 2_2\3_3 as a binding diagonal: any other is REPORT-ONLY
                res["joins"][ul + "\\" + k]["binding"] = "REPORT-ONLY (not in s51's list)"; res["joins"][ul + "\\" + k]["verdict"] = "report"
# contact sheet
sh = Image.new("RGB", (len(keys) * 776, 540), (255, 255, 255))
d = ImageDraw.Draw(sh)
for i, k in enumerate(keys):
    sh.paste(Image.open(src(k)).convert("RGB").resize((768, 512), Image.LANCZOS), (i * 776, 28))
    d.text((i * 776 + 6, 6), "%s  %s" % (k, os.path.relpath(src(k), A9)), fill=(0, 0, 0))
sh.save(OUT + "/contact_sheet.jpg", quality=90)
# stitched preview: smallest grid holding every painted chunk; unpainted cells = guide stand-ins
painted = [k for k in ("%d_%d" % (c, r) for r in range(5) for c in range(5)) if src(k)]
NC = max(int(k.split("_")[0]) for k in painted) + 1; NR = max(int(k.split("_")[1]) for k in painted) + 1
PV = "BV2F-PH3PV"
Gd = Image.open(os.path.join(B2, PINS["guide"]["pinned_copy"])).convert("RGB")
for r in range(NR):
    for c in range(NC):
        k = "%d_%d" % (c, r)
        dd = "%s/%s-%s" % (A9, PV, k); os.makedirs(dd, exist_ok=True)
        p = "%s/%s-%s.png" % (dd, PV, k)
        if src(k):
            shutil.copyfile(src(k), p); what = "copy of " + os.path.relpath(src(k), A9)
        else:
            Gd.crop((1280 * c, 768 * r, 1280 * c + 1536, 768 * r + 1024)).save(p); what = "GUIDE stand-in (unpainted)"
        json.dump({"_what": "R-C9-281 stitched PREVIEW cell -- NOT a painting of record", "cell": what}, open(dd + "/STAND_IN.json", "w"), indent=1)
pc = dict(cfg); pc["prefix"], pc["cols"], pc["rows"] = PV, NC, NR
pcp = OUT + "/preview_cfg.json"; json.dump(pc, open(pcp, "w"), indent=1)
scr = "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/df21e264-6571-4d04-96ee-b8e2bd6d97fa/scratchpad/ph3pv_%s.png" % tag
rp = subprocess.run(["python3", FIDS + "/v1tools/tierB/conductor_scripts/guided_stitch.py", pcp, scr, OUT + "/stitched_preview.jpg"],
                    env=dict(os.environ, BV2F_DEV24="1"), capture_output=True, text=True)
res["preview"] = {"grid": [NC, NR], "rc": rp.returncode, "log": rp.stdout.strip().splitlines()[-6:] + rp.stderr.strip().splitlines()[-3:],
                  "file": "stitched_preview.jpg (half size); cells not painted are the GUIDE"}
json.dump(res, open(OUT + "/qa.json", "w"), indent=1)
print(json.dumps({"chunks": {k: {"P6a_invented": v["P6a"]["invented"], "P4": {c_: (x["windows"], x["verdict"]) for c_, x in v["P4"].items()}, "snow_palette": v["snow_palette"]} for k, v in res["chunks"].items()},
                  "joins": {k: (v["a1_max"], v["verdict"], v["raw_mad"]) for k, v in res["joins"].items()}, "preview_rc": rp.returncode}, indent=1))
