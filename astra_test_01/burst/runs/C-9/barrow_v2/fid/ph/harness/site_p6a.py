#!/usr/bin/env python3
"""§ 52 (d): FULL-SITE P6a (R-C9-331 / Gate-2 H-2), as pre-registered at 7d47a498d.
The v0.1 detector (T = the frozen § 8 ceiling, quarter scale, no prior) on (1) the r328 PAINTING, whole site (it covers
the DEV-24 layers 4-23: post-stitch service paint that ships) and (2) each of the 16 KEPT Phase 3' RAW canvases.
Each candidate: matched to LV's declared openings (centre_px + p6a_match_radius_m; barrow_door, hall_great_door,
gable_breach, sea_cave_mouth, wreck_hull); else classified from the PINNED class map's 0.6 m window:
  water (>= 50 % sea / lead / ice / ice_mid / tide_ice / shore_ice / stream) -> PENDING conductor triage (R-C9-194/282)
  dark structure (>= 50 % char / ash / wood / passage_dark: hall, gable, palisade, burned yard) -> PENDING (§ 11)
  otherwise -> 'invented (outside dark structures: auto-fail)' pending the conductor's by-eye read
Every unmatched candidate gets a triage row + crop | overlay PNG (sha recorded). Never auto-passed.
  PH_SITE=1 site_p6a.py -> results/site/p6a.json, p6a_triage.jsonl, p6a_triage/<cid>.png"""
import datetime
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

os.environ["PH_SITE"] = "1"
os.environ.setdefault("PH_PILOT_OUT", "results/site")
sys.path.insert(0, os.path.dirname(__file__))
import pilot_harness as H  # noqa
from common import *  # noqa
import p6_geometry as G
import p6_overlay as O
import site_domain as SD

WATER = ("sea", "ice", "lead", "ice_mid", "tide_ice", "shore_ice", "stream")
DARK = ("char", "ash", "wood", "passage_dark")
PIN_CLASS = FID / "pt/ph3/class_art_pinned_d26d14c55.png"
PIN_CLASS_SHA = "baffff669c2d762155d60d8d51f32b9ee14a10e3e30cef1a74cb9401cfc9f947"


def detect(img_plate_region, x_org, y_org, label, dec, cls, names, idx, tab, T, od, P_for_crop):
    SC = G.SC
    hh, ww = img_plate_region.shape[:2]
    im = np.asarray(Image.fromarray(np.clip(img_plate_region, 0, 255).astype(np.uint8)).resize((ww // 4, hh // 4), Image.BOX), np.float32)
    found = G.openings(im, PPM_V1 * SC, T)
    rows = []
    wi = {names.index(n) for n in WATER if n in names}
    di = {names.index(n) for n in DARK if n in names}
    for i, f in enumerate(found):
        lx, ly = f["xy"][0] / SC, f["xy"][1] / SC
        x, y = lx + x_org, ly + y_org                                # plate px
        best = min(dec, key=lambda d: math.hypot(x - d["xy"][0], y - d["xy"][1]))
        dist = math.hypot(x - best["xy"][0], y - best["xy"][1]) / PPM_V1
        matched = dist <= best["radius_m"]
        chunk = [k for k, (x0, y0, x1, y1) in H.CHUNKS if x0 <= x < x1 and y0 <= y < y1]
        xi, yi = int(round(x)), int(round(y))
        cw = cls[max(yi - 30, 0):yi + 30, max(xi - 30, 0):xi + 30]
        u_, n_ = np.unique(cw, return_counts=True)
        share = {names[a]: round(float(b) / cw.size, 3) for a, b in zip(u_, n_)}
        in_water = float(np.isin(cw, list(wi)).mean()) >= 0.5
        in_dark = float(np.isin(cw, list(di)).mean()) >= 0.5
        if matched:
            verdict = "declared"
        elif in_water:
            verdict = "PENDING conductor triage (water class: R-C9-194/282)"
        elif in_dark:
            verdict = "PENDING conductor triage (inside dark structure: s11)"
        else:
            verdict = "invented (outside dark structures: auto-fail) -- pending the conductor's by-eye read"
        cid = "%s_%s_c%03d" % (label, chunk[0] if chunk else "w", i)
        rec = {"source": label, "chunk": chunk, "candidate": cid, "candidate_px": [round(x), round(y)], "area_m2": round(f["area_m2"], 2),
               "h_m": f["h_m"], "w_m": f["w_m"], "nearest_declared": best["id"], "distance_m": round(dist, 2),
               "match_radius_m": best["radius_m"], "verdict": verdict, "inside_water_class": in_water, "inside_dark_structure": in_dark,
               "pinned_class_share_0.6m": share, "id_at_centroid": tab[int(idx[yi, xi])]["id"] if int(idx[yi, xi]) in tab else "none (0)",
               "reader": "auto (site_p6a.py, s52 (d))", "conductor_read": "n/a" if matched else "PENDING (by eye)",
               "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        if not matched:
            cr, cx0, cy0 = O._crop(P_for_crop, lx, ly)
            g_ = cr.mean(-1, keepdims=True)
            ov = Image.fromarray(np.clip(cr * 0.55 + g_ * 0.45, 0, 255).astype(np.uint8))
            dr = ImageDraw.Draw(ov)
            for d in dec:
                ddx, ddy = d["xy"][0] - x_org - cx0, d["xy"][1] - y_org - cy0
                rr = d["radius_m"] * PPM_V1
                if d["corners"]:
                    dr.polygon([(a - x_org - cx0, b - y_org - cy0) for a, b in d["corners"]], outline=O.CYAN, width=5)
                dr.ellipse([ddx - rr, ddy - rr, ddx + rr, ddy + rr], outline=O.CYAN, width=2)
            dr.ellipse([lx - cx0 - 10, ly - cy0 - 10, lx - cx0 + 10, ly - cy0 + 10], outline=(255, 60, 60), width=3)
            ova = np.asarray(ov)
            comp = np.full((O.CROP, 2 * O.CROP + O.GAP, 3), 255, np.uint8)
            comp[:, :O.CROP] = np.clip(cr, 0, 255).astype(np.uint8)
            comp[:, O.CROP + O.GAP:] = ova
            fn = od / (cid + ".png")
            Image.fromarray(comp).save(fn)
            rec.update(crop_sha=O._sha_png(cr), overlay_sha=O._sha_png(ova), image=str(fn.relative_to(FID)), image_sha256=sha256(fn))
        rows.append(rec)
    return rows


def main():
    assert sha256(PIN_CLASS) == PIN_CLASS_SHA, "pinned class map sha -> STOP"
    cls = np.asarray(Image.open(PIN_CLASS))
    names = jload(FID / "lv/guide_art/guide_manifest.json")["class"]["classes"]
    idx, tab = H.ids_built()
    T = jload(PH / "results/p6.json")["invention"]["T_v1_ceiling"]
    dec = H.declared()
    od = H.OUT / "p6a_triage"
    od.mkdir(parents=True, exist_ok=True)
    P = H.painting()
    rows = detect(P, 0, 0, "painting", dec, cls, names, idx, tab, T, od, P)
    for k, v in SD.CANV.items():
        if v["pilot"]:
            continue
        c, r = map(int, k.split("_"))
        img = load_rgb(SD.ART / v["canvas"])
        assert sha256(SD.ART / v["canvas"]) == v["sha256"]
        rows += detect(img, 1280 * c, 768 * r, "canvas-" + pathlib.Path(v["canvas"]).parent.name.replace("BV2F-PH3-", ""), dec, cls, names, idx, tab, T, od, img)
    with open(H.OUT / "p6a_triage.jsonl", "w") as fh:
        for rr in rows:
            fh.write(json.dumps(rr) + "\n")
    inv = [rr for rr in rows if rr["verdict"].startswith("invented")]
    pend = [rr for rr in rows if rr["verdict"].startswith("PENDING")]
    rec42 = {"plate_px": [6446, 1789], "pinned_class": names[int(cls[1789, 6446])],
             "class_share_0.6m": {names[a]: round(float(b) / 3600, 3) for a, b in zip(*np.unique(cls[1759:1819, 6416:6476], return_counts=True))},
             "id": tab[int(idx[1789, 6446])]["id"] if int(idx[1789, 6446]) in tab else "none (0)"}
    out = {"_what": "s52 (d) full-site P6a (R-C9-331)", "T": T, "declared": [d["id"] for d in dec],
           "declared_found": sorted({rr["nearest_declared"] for rr in rows if rr["verdict"] == "declared"}),
           "candidates": len(rows), "by_source": {s: sum(rr["source"] == s for rr in rows) for s in sorted({rr["source"] for rr in rows})},
           "unmatched_n": len(inv) + len(pend), "invented_outside_dark_n": len(inv), "pending_water_n": sum("water" in rr["verdict"] for rr in pend),
           "pending_dark_n": sum("dark" in rr["verdict"] for rr in pend), "record_4_2_candidate_6446_1789": rec42,
           "rows": rows, "verdict": "PENDING conductor by-eye triage of %d unmatched candidates (%d outside water/dark classes)" % (len(inv) + len(pend), len(inv))
           if (inv or pend) else "PASS"}
    dump(out, str(H.OUT / "p6a.json"))
    print({k: out[k] for k in ("candidates", "by_source", "declared_found", "unmatched_n", "invented_outside_dark_n", "pending_water_n", "pending_dark_n", "record_4_2_candidate_6446_1789")})
    for rr in inv:
        print("OUTSIDE:", rr["candidate"], rr["candidate_px"], rr["pinned_class_share_0.6m"], rr["id_at_centroid"])


if __name__ == "__main__":
    main()
