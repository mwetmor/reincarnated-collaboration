#!/usr/bin/env python3
"""s59 (R-C9-339 delta): the changed-px mask D = r339 != r332, its geometry and class histogram (pinned d26d14c55 class
map), pilot px, the P9c trigger (D vs bobbing-floe ids), and the P11 FOOTPRINT check (every A/B/X crop of the judged set
abx3_site_v1_vs_site that comes from a site still, mapped to plate px by its still's camera centre) -> results/site_r339/delta.json"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

os.environ["PH_SITE"] = "1"
sys.path.insert(0, os.path.dirname(__file__))
import pilot_harness as H  # noqa
from common import *  # noqa

OUT = PH / "results/site_r339"
A = FID / "pt/ph3/final/painting_ph3_r332_full.png"
B = FID / "pt/ph3/final/painting_ph3_r339_full.png"
U0, V1 = -33.57573954303182, 22.36993715728635
PXV = 80.3076


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    a, b = np.asarray(Image.open(A)), np.asarray(Image.open(B))
    D = np.any(a != b, -1)
    ys, xs = np.nonzero(D)
    cls = np.asarray(Image.open(FID / "pt/ph3/class_art_pinned_d26d14c55.png"))
    assert sha256(FID / "pt/ph3/class_art_pinned_d26d14c55.png") == "baffff669c2d762155d60d8d51f32b9ee14a10e3e30cef1a74cb9401cfc9f947"
    names = jload(FID / "lv/guide_art/guide_manifest.json")["class"]["classes"]
    u, c = np.unique(cls[D], return_counts=True)
    hist = {names[k]: int(n) for k, n in zip(u, c)}
    idx, tab = H.ids_built()
    floe_ids = [k for k, v in tab.items() if v["id"] == "ice_floes_bob" or v["id"].startswith("blobs_shore_ice__")]
    floe_hit = int((D & np.isin(idx, floe_ids)).sum())
    iu, ic = np.unique(idx[D], return_counts=True)
    ids_hist = {tab.get(int(k), {}).get("id", "none(0)"): int(n) for k, n in zip(iu, ic)}
    chunks = sorted({"%d_%d" % (cc, rr) for cc in range(5) for rr in range(5)
                     if D[768 * rr:768 * rr + 1024, 1280 * cc:1280 * cc + 1536].any()})
    pilot_px = int(D[:2304, :3840].sum())
    # P11 footprint
    key = jload(PH / "p11/keys/abx3_site_v1_vs_site.json")
    views = {v["name"] + ".png": v["camera_centre_ground_uv"] for v in jload(FID / "pt/site/stills_views.json")["views"]}
    crops, hits = 0, []
    Dd = D
    for tn, t in key["trials"].items():
        for side in ("A", "B", "X"):
            cdef = t[side]
            nm = pathlib.Path(cdef["src"]).name
            if nm not in views:
                continue
            crops += 1
            with Image.open(cdef["src"]) as im:
                W, Hh = im.size
            cu, cv = views[nm]
            xc, yc = (cu - U0) * PPM_V1, (V1 - cv) * PXV
            x, y, w, h = cdef["rect"][0], cdef["rect"][1], cdef["rect"][2], cdef["rect"][3]
            X0, Y0 = int(round(xc - W / 2 + x)), int(round(yc - Hh / 2 + y))
            sub = Dd[max(Y0, 0):max(Y0 + h, 0), max(X0, 0):max(X0 + w, 0)]
            n = int(sub.sum()) if sub.size else 0
            if n:
                hits.append({"trial": tn, "side": side, "still": nm, "plate_rect_xywh": [X0, Y0, w, h], "changed_px": n})
    out = {"_what": "s59 delta mask r339 vs r332", "r332_sha256": sha256(A), "r339_sha256": sha256(B),
           "changed_px": int(D.sum()), "bbox_xyxy": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if D.any() else None,
           "class_histogram_pinned_d26d14c55": hist, "tide_ice_only": set(hist) == {"tide_ice"}, "ids_histogram": ids_hist,
           "chunks_touched": chunks, "pilot_px_x<3840_y<2304": pilot_px,
           "p9c_trigger_floe_px_in_delta": floe_hit, "p9c_rerun": floe_hit > 0,
           "p11_footprint": {"site_crops_checked": crops, "crops_intersecting": hits, "pass": not hits and set(hist) == {"tide_ice"}}}
    dump(out, str(OUT / "delta.json"))
    Image.fromarray((D * 255).astype(np.uint8)).save(OUT / "delta_mask.png")
    print({k: v for k, v in out.items() if k != "ids_histogram"}, list(ids_hist.items())[:6])


if __name__ == "__main__":
    main()
