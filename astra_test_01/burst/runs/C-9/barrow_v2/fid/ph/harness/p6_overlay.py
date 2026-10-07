#!/usr/bin/env python3
"""P6a G2-B1 (charter § 13): the DECLARED-OPENING OVERLAY, the § 9 truth set re-rendered with it, and the per-chunk
TRIAGE TOOL (fallback (a), R-C9-169/170: the conductor triages by eye, logged).

Declared openings = the layout's own list, projected to plate pixels -- never the guide's class map (W-7):
  * BVR calibration: layout v5 (git b267b9b00, ph/inputs/) features with an `opening`, by the BVP plate law
    (frame_bvp.json): X = P x + X0, Y = P sin(a) y - P cos(a) z + Y0 (x east, y SOUTH, z up).
  * Phase 1+: LV's declared-opening list for layout_v7 (load_declared(json) -- schema: [{"id", "centre_xy": [x, y],
    "z_bottom_m", "w", "h", "faces_compass_deg"}] in the sim frame, + the frame JSON).
Each opening is a vertical quad in its wall plane: centre (x, y), width w along the wall tangent (perpendicular to
its facing; compass degrees, 0 = north = -y), from z_bottom to z_bottom + h. Projected, outlined CYAN, labelled.
DISTANCE from a candidate to a declared opening = screen metres (plate px / 100.6) to the projected quad's centroid.
MATCH radius (charter § 13): the opening's half-width + 1.0 m.

  p6_overlay.py truthset          the § 9 truth set, judge-ready: ph/p6_overlay_judge/ (items + JUDGE.md), key in
                                  ph/keys/p6_overlay_judge.json
  p6_overlay.py triage <window> <painting.png> <frame.json> <declared.json> <candidates.json> [--dark-mask m.png]
                                  per candidate inside a declared dark structure: crop | crop + overlay, rendered to
                                  ph/triage/<window>/, and a PENDING row in results/p6a_triage_<window>.jsonl
  p6_overlay.py record <window> <candidate_id> <verdict> <evidence...> --reader NAME
                                  the reader's verdict (invented / material / declared) on that row
"""
import argparse
import datetime
import hashlib
import io
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p6_geometry as G

CROP = 512
GAP = 24
CYAN = (0, 230, 255)


def bvp_law():
    f = jload(B2 / "paint/frame_bvp.json")
    P, (X0, Y0), a = f["px_per_m"], f["origin_px"], math.radians(f["pitch_deg"])
    return lambda x, y, z: (P * x + X0, P * math.sin(a) * y - P * math.cos(a) * z + Y0)


def declared_v5():
    L = jload(PH / "inputs/layout_v2_at_b267b9b00_v5.json")
    out = []
    for ft in L["features"]:
        op = ft.get("opening")
        if not op or "clear_w_m" not in op:
            continue
        c = ft.get("mouth_centre") or list(np.mean(np.array(ft["footprint"], float), axis=0))
        out.append({"id": ft["id"], "centre_xy": [float(c[0]), float(c[1])], "z_bottom_m": float(ft.get("z_bottom_m", 0.0)),
                    "w": float(op["clear_w_m"]), "h": float(op["clear_h_m"]), "faces_compass_deg": float(ft.get("faces_deg", 180.0))})
    return out


def quad(o, law):
    t = math.radians(o["faces_compass_deg"])
    tx, ty = math.cos(t), math.sin(t)                     # wall tangent (perpendicular to the facing (sin t, -cos t))
    x, y = o["centre_xy"]
    hw = o["w"] / 2
    z0, z1 = o["z_bottom_m"], o["z_bottom_m"] + o["h"]
    return [law(x - tx * hw, y - ty * hw, z0), law(x + tx * hw, y + ty * hw, z0),
            law(x + tx * hw, y + ty * hw, z1), law(x - tx * hw, y - ty * hw, z1)]


def dist_m(pt, q):
    """screen metres from the point to the projected opening's CENTRE (the quad's centroid). The match radius
    (half-width + 1.0 m) is a radius about the centre; an edge distance would accept anything touching a large
    opening's corner (calibration: the invented doorway sits 1.3 m from the porch quad's corner, 4.4 m from its centre)."""
    c = np.mean(np.array(q, float), axis=0)
    return float(np.hypot(pt[0] - c[0], pt[1] - c[1])) / PPM_V1


def _seg(p, a, b):
    p, a, b = np.array(p, float), np.array(a, float), np.array(b, float)
    t = np.clip(np.dot(p - a, b - a) / max(np.dot(b - a, b - a), 1e-9), 0, 1)
    return float(np.linalg.norm(p - (a + t * (b - a))))


def nearest(pt, decl, law):
    best = None
    for o in decl:
        d = dist_m(pt, quad(o, law))
        if best is None or d < best[1]:
            best = (o, d)
    o, d = best
    return {"id": o["id"], "distance_m": round(d, 2), "match_radius_m": round(o["w"] / 2 + 1.0, 2),
            "matched": d <= o["w"] / 2 + 1.0}


def overlay(crop, x0, y0, decl, law, desat=0.45):
    """the crop, desaturated so the cyan reads, with every declared opening's projected quad outlined and labelled"""
    g = crop.mean(-1, keepdims=True)
    base = np.clip(crop * (1 - desat) + g * desat, 0, 255).astype(np.uint8)
    im = Image.fromarray(base)
    d = ImageDraw.Draw(im)
    for o in decl:
        q = [(px - x0, py - y0) for px, py in quad(o, law)]
        if max(p[0] for p in q) < 0 or min(p[0] for p in q) > CROP or max(p[1] for p in q) < 0 or min(p[1] for p in q) > CROP:
            continue
        d.polygon(q, outline=CYAN, width=5)
        cx = sum(p[0] for p in q) / 4
        cy = min(p[1] for p in q) - 16
        d.text((max(2, min(CROP - 120, cx - 50)), max(2, cy)), "declared opening", fill=CYAN)
    return np.asarray(im)


def _crop(img, x, y):
    H, W = img.shape[:2]
    x0 = int(min(max(x - CROP // 2, 0), W - CROP))
    y0 = int(min(max(y - CROP // 2, 0), H - CROP))
    return img[y0:y0 + CROP, x0:x0 + CROP].astype(np.float32), x0, y0


def _sha_png(arr):
    b = io.BytesIO()
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(b, format="PNG")
    return hashlib.sha256(b.getvalue()).hexdigest()


# ------------------------------------------------------------------ the § 9 truth set, judge-ready
JUDGE_MD = """# Painting against its declared openings

Each image `item_NN.png` shows two squares side by side, of the SAME place. LEFT: a crop of a painting. RIGHT: the same
crop, greyed, with every DECLARED opening (a doorway or opening the level is meant to have) outlined in cyan.

For each item answer one question:

**Does the painting show a doorway or opening that is NOT inside a cyan outline?**

Answer `yes` or `no`. Return a JSON object {"item_01": "yes" or "no", ...} and, per item, one short sentence naming
what you see.
"""

TRUTH = {"item_17": "invented", "item_08": "invented", "item_11": "invented", "item_18": "invented", "item_13": "declared"}


def truthset(seed=173):
    key9 = jload(PH / "keys/p6_judge.json")["items"]
    law = bvp_law()
    decl = declared_v5()
    keys = G.BLOCKS["BVR hall (T2a, 7_5..8_7)"]
    paint, (bx0, by0) = G.bvr_block(keys)
    P1 = load_rgb(BF / "paint/barrow_full_painted.png")
    sx, sy = G.v1_px(-6.0, 1.0, 1.3)
    C1 = P1.copy()
    w, h = 2.2 * PPM_V1, 2.6 * 60.6183
    C1[int(sy - h / 2):int(sy + h / 2), int(sx - w / 2):int(sx + w / 2)] = np.array([30, 27, 25], np.float32)
    # v1's declared barrow door as a declared-opening record in v1's own frame (a uv -> plate px law)
    v1law = lambda u, v, z: G.v1_px(u, v, z)
    v1decl = [{"id": "v1 barrow door (door_lintel slot)", "centre_xy": [0.0, 10.6], "z_bottom_m": 0.0, "w": 1.8, "h": 2.2,
               "faces_compass_deg": 0.0}]                      # in (u, v): t = 0 gives the tangent +u (the door faces the camera)
    items = []
    for nm, v in key9.items():
        x, y = v["plate_xy"]
        if v["source"] == "BVR hall T2a":
            c, x0, y0 = _crop(paint, x - bx0, y - by0)
            ov = overlay(c, x0 + bx0, y0 + by0, decl, law)
            ne = nearest((x, y), decl, law)
        else:
            src = C1 if v["source"] == "v1 + stamp" else P1
            c, x0, y0 = _crop(src, x, y)
            ov = overlay(c, x0, y0, v1decl, v1law)
            ne = nearest((x, y), v1decl, v1law)
        items.append({"old_item": nm, "kind": v["kind"], "truth": TRUTH.get(nm, "material"), "plate_xy": [x, y],
                      "nearest_declared": ne, "paint": c, "overlay": ov})
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(items))
    jd = PH / "p6_overlay_judge"
    jd.mkdir(parents=True, exist_ok=True)
    for f in jd.glob("item_*.png"):
        f.unlink()
    key = {"_what": "P6a overlay truth set key (G2-B1) -- NEVER given to the judge; truth = calibration.md § 9",
           "acceptance": "every invented feature flagged (item_17; 08 or 11; the stamp); the declared door not; <= 2 material yes",
           "items": {}}
    for n, i in enumerate(order):
        it = items[i]
        comp = np.full((CROP, 2 * CROP + GAP, 3), 255, np.uint8)
        comp[:, :CROP] = np.clip(it["paint"], 0, 255).astype(np.uint8)
        comp[:, CROP + GAP:] = it["overlay"]
        name = "item_%02d" % (n + 1)
        Image.fromarray(comp).save(jd / (name + ".png"))
        key["items"][name] = {k: v for k, v in it.items() if k not in ("paint", "overlay")}
    (jd / "JUDGE.md").write_text(JUDGE_MD)
    dump(key, str(PH / "keys/p6_overlay_judge.json"))
    return {"dir": str(jd), "items": len(items)}


def score_truthset(answers):
    key = jload(PH / "keys/p6_overlay_judge.json")["items"]
    ans = {k: str(v).strip().lower() for k, v in jload(answers).items()}
    yes = lambda k: ans.get(k, "").startswith("y")
    by_old = {v["old_item"]: k for k, v in key.items()}
    feats = {"doorway by brazier_sw": ["item_17"], "gable-end opening": ["item_08", "item_11"], "stamp": ["item_18"]}
    flagged = {f: any(yes(by_old[o]) for o in olds) for f, olds in feats.items()}
    mat = [k for k, v in key.items() if v["truth"] == "material"]
    r = {"invented_flagged": flagged, "declared_flagged": yes(by_old["item_13"]),
         "material_yes": sorted(key[k]["old_item"] for k in mat if yes(k)), "material": len(mat)}
    r["acceptance"] = all(flagged.values()) and not r["declared_flagged"] and len(r["material_yes"]) <= 2
    return r


# ------------------------------------------------------------------ the per-chunk triage tool (fallback (a))
def triage(window, painting, frame, declared, candidates, dark_mask=None, origin=(0, 0)):
    """painting: a PNG covering plate px [origin, origin + size); candidates and the dark mask in PLATE px / painting px."""
    img = load_rgb(painting)
    ox, oy = origin
    fr = jload(frame)
    P, (X0, Y0), a = fr["px_per_m"], fr["origin_px"], math.radians(fr["pitch_deg"])
    law = lambda x, y, z: (P * x + X0, P * math.sin(a) * y - P * math.cos(a) * z + Y0)
    decl = jload(declared)
    cands = jload(candidates)          # [{"chunk", "xy": [plate px]}] -- p6_geometry.openings() output, plate px
    dm = (np.asarray(Image.open(dark_mask)) > 0) if dark_mask else None
    od = PH / "triage" / window
    od.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, c in enumerate(cands):
        x, y = c["xy"]
        inside = bool(dm[int(y - oy), int(x - ox)]) if dm is not None else True
        ne = nearest((x, y), decl, law)
        cr, x0, y0 = _crop(img, x - ox, y - oy)
        ov = overlay(cr, x0 + ox, y0 + oy, decl, law)
        comp = np.full((CROP, 2 * CROP + GAP, 3), 255, np.uint8)
        comp[:, :CROP] = np.clip(cr, 0, 255).astype(np.uint8)
        comp[:, CROP + GAP:] = ov
        cid = "%s_c%03d" % (c.get("chunk", "w"), i)
        Image.fromarray(comp).save(od / (cid + ".png"))
        verdict = ("declared" if ne["matched"] else ("PENDING" if inside else "invented (outside dark structures: auto-fail)"))
        rows.append({"chunk": c.get("chunk"), "candidate": cid, "candidate_px": [round(x), round(y)],
                     "inside_dark_structure": inside, "crop_sha": _sha_png(cr), "overlay_sha": _sha_png(ov),
                     "nearest_declared": ne["id"], "distance_m": ne["distance_m"], "match_radius_m": ne["match_radius_m"],
                     "verdict": verdict, "evidence": "", "reader": "" if verdict == "PENDING" else "auto (p6_overlay.py)",
                     "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    with open(PH / "results" / ("p6a_triage_%s.jsonl" % window), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return rows


def record(window, cid, verdict, evidence, reader):
    p = PH / "results" / ("p6a_triage_%s.jsonl" % window)
    rows = [json.loads(l) for l in open(p)]
    hit = 0
    for r in rows:
        if r["candidate"] == cid:
            r.update(verdict=verdict, evidence=evidence, reader=reader,
                     ts=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            hit += 1
    if not hit:
        raise SystemExit("no candidate %s in %s" % (cid, p))
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("truthset")
    s = sub.add_parser("score")
    s.add_argument("answers")
    t = sub.add_parser("triage")
    for k in ("window", "painting", "frame", "declared", "candidates"):
        t.add_argument(k)
    t.add_argument("--dark-mask")
    t.add_argument("--origin", nargs=2, type=int, default=[0, 0], help="the painting's plate-px origin")
    sub.add_parser("demo_bvr", help="run the triage tool on the BVR hall block (calibration demo)")
    r = sub.add_parser("record")
    r.add_argument("window")
    r.add_argument("candidate")
    r.add_argument("verdict", choices=["invented", "material", "declared"])
    r.add_argument("evidence", nargs="+")
    r.add_argument("--reader", required=True)
    a = ap.parse_args()
    if a.cmd == "truthset":
        print(truthset())
    elif a.cmd == "score":
        print(json.dumps(score_truthset(a.answers), indent=1))
    elif a.cmd == "triage":
        rows = triage(a.window, a.painting, a.frame, a.declared, a.candidates, a.dark_mask, tuple(a.origin))
        print("%d candidates -> results/p6a_triage_%s.jsonl (%d PENDING)" % (len(rows), a.window, sum(r["verdict"] == "PENDING" for r in rows)))
    elif a.cmd == "demo_bvr":
        keys = G.BLOCKS["BVR hall (T2a, 7_5..8_7)"]
        paint, (bx0, by0) = G.bvr_block(keys)
        d = PH / "triage_inputs"
        d.mkdir(parents=True, exist_ok=True)
        Image.fromarray(paint.astype(np.uint8)).save(d / "bvr_hall.png")
        m = G.zonemap_dark_mask((bx0, by0, bx0 + paint.shape[1], by0 + paint.shape[0]), 1.0)
        Image.fromarray(m.astype(np.uint8) * 255).save(d / "bvr_hall_dark.png")
        dump(declared_v5(), str(d / "declared_v5.json"))
        rows = jload(PH / "results/p6.json")["invention"]["rows"]["BVR hall (T2a, 7_5..8_7)"]["inventions_xy_plate_px"]
        dump([{"chunk": "bvr_hall", "xy": [x, y]} for x, y, _ in rows], str(d / "bvr_hall_candidates.json"))
        rr = triage("bvr_demo", d / "bvr_hall.png", B2 / "paint/frame_bvp.json", d / "declared_v5.json",
                    d / "bvr_hall_candidates.json", d / "bvr_hall_dark.png", (bx0, by0))
        print("%d rows -> results/p6a_triage_bvr_demo.jsonl; %d PENDING, %d auto" % (len(rr), sum(r["verdict"] == "PENDING" for r in rr),
              sum(r["verdict"] != "PENDING" for r in rr)))
    elif a.cmd == "record":
        record(a.window, a.candidate, a.verdict, " ".join(a.evidence), a.reader)
