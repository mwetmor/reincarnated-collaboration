#!/usr/bin/env python3
"""s54 (R-C9-335): the P9c discriminator, as pre-registered at f7af6f5bc. -> results/site/p9c_null.json"""
import math
import os
import sys
os.environ["PH_SITE"] = "1"
os.environ.setdefault("PH_PILOT_OUT", "results/site")
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pilot_harness as H  # noqa
from common import *  # noqa

UV = (-23.976, -21.834)
R = PH / "renders/site"


def rows(mode):
    r = H.p9c_measure_v2(R / ("p9c_null_" + mode), UV)
    out = []
    for k, pr in enumerate(r["per_pair"]):
        for y in pr["rows"]:
            out.append(dict(y, pair=k))
    return r, out


def centroid(dirp, sfx):
    """silhouette centroids per floe (same labelling as floe_drift_v2) for matching across modes"""
    from scipy import ndimage
    m0, hf = load_rgb(dirp / ("floe_m0%s.png" % sfx)), load_rgb(dirp / "hide_floe.png")
    k0 = ndimage.binary_opening(((m0[..., 0] - m0[..., 2]) - (hf[..., 0] - hf[..., 2]) > 40) & (m0[..., 0] - m0[..., 2] > 30), iterations=2)
    lab, n = ndimage.label(k0)
    return [ndimage.center_of_mass(lab == i + 1) for i in range(n) if (lab == i + 1).sum() >= 1500]


res, per = {}, {}
for m in ("bobt", "rigid", "static"):
    r, rr = rows(m)
    res[m] = {"median_drift_samples_px": r["median_drift_samples_px"], "samples": r["samples_counted"],
              "median_abs_r_all_px": round(float(np.median([y["drift"] for y in rr])), 3) if rr else None}
    per[m] = rr
# match bobt vs rigid rows: same pair, same px count within 3 % (same labelling on same geometry) -> r difference
dr = []
for a in per["bobt"]:
    cands = [b for b in per["rigid"] if b["pair"] == a["pair"] and abs(b["px"] - a["px"]) <= 0.03 * a["px"]
             and math.hypot(b["silhouette_shift"][0] - a["silhouette_shift"][0], b["silhouette_shift"][1] - a["silhouette_shift"][1]) <= 0.5]
    if not cands:
        continue
    b = min(cands, key=lambda b: abs(b["px"] - a["px"]))
    ra = (a["silhouette_shift"][0] - a["texture_shift"][0], a["silhouette_shift"][1] - a["texture_shift"][1])
    rb = (b["silhouette_shift"][0] - b["texture_shift"][0], b["silhouette_shift"][1] - b["texture_shift"][1])
    dr.append({"pair": a["pair"], "px": a["px"], "motion_bobt": a["motion"], "motion_rigid": b["motion"], "drift_bobt": a["drift"],
               "drift_rigid": b["drift"], "dr": round(math.hypot(ra[0] - rb[0], ra[1] - rb[1]), 3),
               "sil_bobt": a["silhouette_shift"], "tex_bobt": a["texture_shift"], "sil_rigid": b["silhouette_shift"], "tex_rigid": b["texture_shift"]})
# image identity bobt vs rigid over floe px
idiff = []
for k in range(5):
    sfx = "" if k == 0 else "_%d" % k
    for f in ("floe_m0", "floe_m1"):
        A, B = load_rgb(R / "p9c_null_bobt" / (f + sfx + ".png")), load_rgb(R / "p9c_null_rigid" / (f + sfx + ".png"))
        hf = load_rgb(R / "p9c_null_bobt" / "hide_floe.png")
        fm = ((A[..., 0] - A[..., 2]) - (hf[..., 0] - hf[..., 2]) > 40)
        idiff.append({"shot": f + sfx, "mean_abs_floe_px": round(float(np.abs(A - B)[fm].mean()), 3), "max": float(np.abs(A - B)[fm].max()),
                      "frac_px_differing": round(float((np.abs(A - B)[fm].max(-1) > 0).mean()), 4)})
mdr = float(np.median([d["dr"] for d in dr])) if dr else None
rg, bt = res["rigid"]["median_drift_samples_px"], res["bobt"]["median_drift_samples_px"]
if rg is not None and (rg > 0.25 or (mdr is not None and mdr <= 0.05 and bt and rg >= 0.5 * bt)):
    verdict = "INSTRUMENT"
elif rg is not None and rg <= 0.10 and bt is not None and bt > 0.25 and mdr is not None and mdr > 0.10:
    verdict = "MATERIAL"
else:
    verdict = "MIXED / UNRESOLVED"
out = {"_what": "s54 P9c discriminator (R-C9-335), pre-registered at f7af6f5bc", "view_uv": UV, "modes": res,
       "matched_floe_pairs": len(dr), "median_dr_bobt_vs_rigid_px": None if mdr is None else round(mdr, 3),
       "image_identity_bobt_vs_rigid": idiff, "per_floe": dr, "verdict": verdict,
       "per_floe_rows": per}
dump(out, str(H.OUT / "p9c_null.json"))
print(res, "matched", len(dr), "median dr", mdr, "->", verdict)
print([ (d["shot"], d["mean_abs_floe_px"], d["frac_px_differing"]) for d in idiff])
for d in sorted(dr, key=lambda d: d["px"]):
    print(d["pair"], d["px"], "bobt", d["drift_bobt"], d["sil_bobt"], d["tex_bobt"], "| rigid", d["drift_rigid"], d["sil_rigid"], d["tex_rigid"], "dr", d["dr"])
