#!/usr/bin/env python3
"""OUR side of the R-29 comparison: re-measure the cathedral floor and the
lap-2 arc, with BOTH region constructions, so the reference/ours comparison
is not decided by an asymmetry in how each region was drawn.

Two reasons this exists:

  1. REGRESSION.  R-27 § R6 reported our effect ratio 2.352, floor ratio
     2.257, effect midS 0.2906, floor midS 0.6225 on `plk06650_cathedral_
     fxon/fxctl`.  R-28 did not touch those artifacts, so those numbers should
     reproduce EXACTLY.  If they do not, the R-29 instrument has drifted and
     nothing downstream is trustworthy.

  2. THE ASYMMETRY THAT RUNS AGAINST THE HEADLINE.  Our effect region is
     CONTROL-DIFFERENCED (|dL| > tau), so it contains the arc's dark pixels as
     well as its bright ones.  The reference's region is CHROMA-SELECTED, and
     a chroma floor truncates an effect's dark tail -- which DEPRESSES P95/P20
     by construction.  So the (b) comparison is biased in favour of ours.
     Bounding it matters, because the (b) finding is that ours is HIGHER than
     the reference; an asymmetry that inflates ours is the one that could
     manufacture that finding.  Two bounds are computed:
       * ours over the SUPPORT (closing+fill) of its own mask -- the same
         footprint construction applied to the reference;
       * the reference side's own dilation ladder, computed in the main
         module, which is the mirror-image bound.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vfx_lap2_battery import luma, sat_val  # noqa: E402
from vfx_ref_anchor import MIN_COMPONENT_PX, agg, ownership, region_stats  # noqa: E402
from vfx_ref_anchor_true import CLOSE_RADIUS, SPATIAL_FLOOR_DILATE, sha256  # noqa: E402
from vfx_true_recon import probe  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--on", required=True)
    ap.add_argument("--ctl", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sustain", nargs=2, type=int, default=[62, 143])
    ap.add_argument("--tau", type=float, default=0.07647053897380829)
    a = ap.parse_args()

    w, h, fps, codec, pix = probe(a.on)
    pa = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.on, "-f", "rawvideo",
                           "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    pb = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.ctl, "-f", "rawvideo",
                           "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    acc = {k: [] for k in ("eff_ratio", "eff_midS", "eff_own", "eff_area",
                           "sup_ratio", "sup_midS", "sup_area",
                           "floor_ratio", "floor_midS", "floor_own",
                           "lift_ratio", "lift_midS", "lift_own",
                           "share_of_self")}
    lo, hi = a.sustain
    i = 0
    while True:
        ba, bb = pa.stdout.read(n), pb.stdout.read(n)
        if not ba or not bb or len(ba) < n or len(bb) < n or i > hi:
            break
        if i < lo:
            i += 1
            continue
        fa = np.frombuffer(ba, np.uint8).reshape(h, w, 3)
        fb = np.frombuffer(bb, np.uint8).reshape(h, w, 3)
        La, Lb = luma(fa), luma(fb)
        sA, _ = sat_val(fa)
        E = ndimage.binary_opening(np.abs(La - Lb) > a.tau, np.ones((3, 3)))
        lab, k = ndimage.label(E, np.ones((3, 3)))
        if k:
            sz = np.array(ndimage.sum(E, lab, range(1, k + 1)))
            keep = np.nonzero(sz >= MIN_COMPONENT_PX)[0] + 1
            E = np.isin(lab, keep) if keep.size else np.zeros_like(E)
        SUP = ndimage.binary_fill_holes(
            ndimage.binary_closing(E, np.ones((CLOSE_RADIUS, CLOSE_RADIUS))))
        es = region_stats(E, La, sA)
        ss = region_stats(SUP, La, sA)
        eo, top = ownership(E, La)
        NE = ~ndimage.binary_dilation(SUP, np.ones((SPATIAL_FLOOR_DILATE,) * 2))
        fs = region_stats(NE, La, sA)
        fo, _ = ownership(NE, La)
        acc["eff_ratio"].append(es["ratio"])
        acc["eff_midS"].append(es["midS"])
        acc["eff_area"].append(es["area"])
        acc["eff_own"].append(eo["own"])
        acc["sup_ratio"].append(ss["ratio"])
        acc["sup_midS"].append(ss["midS"])
        acc["sup_area"].append(ss["area"])
        acc["floor_ratio"].append(fs["ratio"])
        acc["floor_midS"].append(fs["midS"])
        acc["floor_own"].append(fo["own"])
        acc["share_of_self"].append(float((top & E).sum()) / max(int(E.sum()), 1))
        if fs["ratio"] > 1e-6:
            acc["lift_ratio"].append(es["ratio"] / fs["ratio"])
        if fs["midS"] > 1e-6:
            acc["lift_midS"].append(es["midS"] / fs["midS"])
        if fo["own"] > 1e-9:
            acc["lift_own"].append(eo["own"] / fo["own"])
        i += 1
    for p in (pa, pb):
        p.stdout.close()
        p.kill()
        p.wait()

    S = {k: agg(v) for k, v in acc.items() if v}
    R27 = {"eff_ratio": 2.352, "floor_ratio": 2.257, "eff_midS": 0.2906,
           "floor_midS": 0.6225, "eff_own": 0.4017, "floor_own": 0.4367}
    reg = {k: {"r27": v, "now": round(S[k]["median"], 4),
               "delta": round(S[k]["median"] - v, 5)} for k, v in R27.items() if k in S}
    out = {"on": a.on, "ctl": a.ctl,
           "sha256_on": sha256(a.on), "sha256_ctl": sha256(a.ctl),
           "video": {"w": w, "h": h, "fps": fps, "codec": codec, "pix_fmt": pix},
           "sustain": a.sustain, "tau": a.tau,
           "summary": S, "regression_vs_R27_sec_R6": reg}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1))
    print("OURS  n=%d" % S["eff_ratio"]["n"])
    for k, v in reg.items():
        print("  %-12s R-27 %8.4f   now %8.4f   delta %+.5f %s"
              % (k, v["r27"], v["now"], v["delta"], "OK" if abs(v["delta"]) < 0.002 else "⚑ DRIFT"))
    print("  SUPPORT region  ratio %.4f  midS %.4f  area %.0f (effect area %.0f)"
          % (S["sup_ratio"]["median"], S["sup_midS"]["median"],
             S["sup_area"]["median"], S["eff_area"]["median"]))
    print("  LIFT  ratio %.4fx  midS %.4fx  own %.4fx"
          % (S["lift_ratio"]["median"], S["lift_midS"]["median"], S["lift_own"]["median"]))
    print("  share-of-self %.4f" % S["share_of_self"]["median"])
    print("wrote", a.out)


if __name__ == "__main__":
    main()
