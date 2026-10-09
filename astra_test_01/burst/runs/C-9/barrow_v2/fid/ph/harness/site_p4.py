#!/usr/bin/env python3
"""§ 52 (c): FULL-SITE P4 as pre-registered at 7d47a498d (R-C9-331 / Gate-2 H-3). Run with PH_SITE=1.
  binding rows = the 16 Phase 3' chunks of the r328 painting: snow / rock vs v1's frozen § 3 bars with the § 50 (b)
  minimum support (snow 100, rock 3 windows -> 'insufficient support', never PASS); ICE domain = LV class 'ice' (mere ice)
  vs the FROZEN PS4 Lab (dE <= 9.40, gated b* <= 2, chunk >= 20 000 px) + spectrum vs sketch A at 24 px/m (<= 0.116).
  pilot 9 chunks: reported only (stay as judged at § 47). REPORT-ONLY ice classes: ice_mid, shore_ice, tide_ice, stream, lead.
  PT's per-wave QA P4 readings reported beside. -> results/site/p4.json"""
import glob
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

os.environ["PH_SITE"] = "1"
os.environ.setdefault("PH_PILOT_OUT", "results/site")
sys.path.insert(0, os.path.dirname(__file__))
import pilot_harness as H  # noqa
from common import *  # noqa
import p4_texture as T

WMIN = {"snow": 100, "rock": 3}
REF = np.array([64.58, -2.75, -21.49])
PILOT = {"%d_%d" % (c, r) for c in range(3) for r in range(3)}


def support(mask_chunk):
    return len(T.windows(ndimage.binary_erosion(mask_chunk, iterations=3)))


def main():
    base = H.p4_v38()                     # writes results/site/p4.json (raw harness rows); re-written below with the rules
    idx, tab = H.ids_built()
    cls, names = H.class_map()
    ni = {n: i for i, n in enumerate(names)}
    tf = H.tufts()
    g = H.ground_mask() & ~tf
    rock = np.isin(idx, [k for k, v in tab.items() if v["class"] == "rock" and v.get("piece") in ("model", "instance", "group") or
                         (v["class"] == "rock" and str(v.get("piece", "")).startswith("instance"))])
    masks = {"snow": g & (cls == ni["snow"]), "rock": rock}
    P = H.painting()
    lab = rgb_to_lab(P)
    rows = {}
    for key, (x0, y0, x1, y1) in H.CHUNKS:
        r = base["chunks_snow_rock"][key]
        out = {"pilot": key in PILOT, "binding": key not in PILOT}
        for c in ("snow", "rock"):
            n = support(masks[c][y0:y1, x0:x1])
            v = r["classes"].get(c)
            if v is None:
                out[c] = {"support_windows": n, "verdict": "absent (< 20 000 px after erosion)"}
                continue
            if n < WMIN[c]:
                verdict = "%s: insufficient support (%d < %d)" % (c, n, WMIN[c])
            else:
                verdict = "PASS" if v["pass"] else "FAIL"
            out[c] = dict(v, support_windows=n, w_min=WMIN[c], verdict=verdict)
        ir = base["ice"].get(key)
        out["ice"] = dict(ir, verdict="PASS" if ir["pass"] else "FAIL") if ir else {"verdict": "absent (< 20 000 px gated)"}
        rows[key] = out
    # report-only ice-family classes vs the same frozen Lab
    rep = {}
    for nm in ("ice_mid", "shore_ice", "tide_ice", "stream", "lead"):
        if nm not in ni:
            continue
        full = g & (cls == ni[nm])
        rr = {}
        for key, (x0, y0, x1, y1) in H.CHUNKS:
            m = np.zeros(full.shape, bool)
            m[y0:y1, x0:x1] = full[y0:y1, x0:x1]
            m = ndimage.binary_erosion(m, iterations=3)
            mg = m & (lab[..., 2] <= 2.0)
            if mg.sum() < 5000:
                continue
            med = np.median(lab[mg], 0)
            rr[key] = {"px_gated": int(mg.sum()), "px_ungated": int(m.sum()), "median_lab": med.round(1).tolist(),
                       "dE_vs_frozen_ps4": round(float(np.linalg.norm(med - REF)), 2)}
        rep[nm] = rr
    # PT's per-wave QA P4 readings, beside
    pt = {}
    for f in sorted(glob.glob(str(FID / "pt/ph3/qa_w*/qa.json"))):
        q = jload(f)
        s = json_find(q, "p4")
        if s is not None:
            pt[os.path.basename(os.path.dirname(f))] = s
    bf = []
    for k, r in rows.items():
        if not r["binding"]:
            continue
        for c in ("snow", "rock", "ice"):
            if r[c].get("verdict") == "FAIL":
                bf.append((k, c))
    out = {"_what": "s52 (c) full-site P4 (R-C9-331) on the r328 painting, as pre-registered at 7d47a498d",
           "painting_sha256": sha256(H.PT / "painting.png"), "bars": base["bars_from_v1"] if "bars_from_v1" in base else None,
           "ice_reference": base["ice_reference"], "sketchA_ice_median": base["sketchA_ice_median"],
           "w_min": WMIN, "chunks": rows, "binding_fails_phase3": bf,
           "insufficient_support_phase3": [(k, c) for k, r in rows.items() if r["binding"] for c in ("snow", "rock")
                                           if "insufficient" in str(r[c].get("verdict"))],
           "pilot_reread_report_only": {k: {c: rows[k][c].get("verdict") for c in ("snow", "rock", "ice")} for k in sorted(PILOT)},
           "ice_family_report_only": rep, "coastal_snow_vs_inland_hellinger_diagnostic": base["coastal_snow_vs_inland_hellinger_diagnostic"],
           "reed_advisory": base["reed_advisory"], "pt_qa_p4_beside": pt,
           "pass_phase3": not bf}
    dump(out, str(H.OUT / "p4.json"))
    for k, r in rows.items():
        print(k, "B" if r["binding"] else "p", {c: (r[c].get("verdict"), r[c].get("support_windows"), r[c].get("spec_dist"), r[c].get("hist_dist"))
                                              for c in ("snow", "rock")}, "ice", r["ice"].get("verdict"), r["ice"].get("dE_vs_reference"), r["ice"].get("spectrum_rms_at_24ppm"))
    print("binding fails:", bf)


def json_find(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.lower().startswith(key):
                return v
        for v in o.values():
            r = json_find(v, key)
            if r is not None:
                return r
    return None


if __name__ == "__main__":
    main()
