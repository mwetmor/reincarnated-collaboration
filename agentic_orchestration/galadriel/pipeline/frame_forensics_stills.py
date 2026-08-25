#!/usr/bin/env python3
"""
frame_forensics_stills.py -- the PARTIAL recovery of the OWED clean-room leg.

The dispatch (sec 2, sec 5) records the clean-room whirlwind as having no MP4 and
marks the leg OWED to drax's serial godot lane. That is correct for D3 and D4,
which are TEMPORAL operators and cannot be evaluated on a still by construction.

⚑ BUT D1 AND D2 ARE SPATIAL OPERATORS. The multiscale detail-energy spectrum and
  the H/S/V distribution of an effect's own contribution are properties of a
  single frame. The clean-room row ships ten pre-registered marks as stills WITH
  A MATCHED fx-off CONTROL -- which is a CLEANER effect isolation than anything
  available on the reference, where no control exists and the mask has to be
  inferred from temporal novelty.

  So the OWED leg is owed for two of four series, not four of four. Saying "no
  MP4, therefore no reading" would have deferred a measurement that the existing
  artifacts already support, and deferring an available measurement is the same
  class of error as taking an unavailable one.

WHAT IS NOT CLAIMED HERE. The clean-room mask (fx_on - fx_ctl) and the reference
mask (frame - motion-compensated local plate) are DIFFERENT OPERATORS. Absolute
quantities are therefore not compared across them. Only the NORMALISED BAND-SHARE
SPECTRUM is compared, because it is a shape statistic of the field and sums to 1
by construction on either mask. Every absolute figure below is reported
within-leg only.
"""

import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frame_forensics as ff   # noqa: E402

WWCR = "/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25"
OUT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "work", "2026-08-25-frame-forensics", "out"))

MARKS = ["00-pre", "01-windup-early", "02-windup-late", "03-rising-mid",
         "04-full", "05-sustain", "06-sustain-moving", "07-release-early",
         "08-release-late", "09-off"]


def load(p):
    return np.array(Image.open(p).convert("RGB"))


def analyse_pair(fx_path, ctl_path, floor_ladder=(2, 4, 6, 8, 12)):
    fx, ctl = load(fx_path), load(ctl_path)
    if fx.shape != ctl.shape:
        return None
    d = np.abs(fx.astype(np.int16) - ctl.astype(np.int16)).max(axis=2).astype(np.float32)
    res = {"authored_px": {}, "band_frac": {}, "n_eff": {},
           "fine_share_b0b1": {}}
    for f in floor_ladder:
        m = d >= f
        res["authored_px"][str(f)] = int(m.sum())
        bf, _ = ff.laplacian_band_energy(d * m)
        res["band_frac"][str(f)] = [round(x, 6) for x in bf]
        res["fine_share_b0b1"][str(f)] = round(float(sum(bf[:2])), 5)
        res["n_eff"][str(f)] = round(ff.n_eff(m), 4)

    m = d >= 2
    if m.sum() >= 32:
        hh, ss, vv = ff.rgb_to_hsv(fx)
        wgt = d[m]
        tot = max(float(wgt.sum()), 1e-9)
        ang = 2 * np.pi * hh[m]
        C = float((wgt * np.cos(ang)).sum() / tot)
        Sn = float((wgt * np.sin(ang)).sum() / tot)
        res["hue_circmean"] = round(float((np.arctan2(Sn, C) / (2 * np.pi)) % 1.0), 5)
        res["hue_circvar"] = round(1.0 - float(np.hypot(C, Sn)), 5)
        res["sat_mean"] = round(float((wgt * ss[m]).sum() / tot), 5)
        res["val_mean"] = round(float((wgt * vv[m]).sum() / tot), 5)
        res["hue_hist24"] = [round(float(x / tot), 5) for x in
                             np.histogram(hh[m], bins=24, range=(0, 1), weights=wgt)[0]]
    return res


def main():
    out = {"corpus": WWCR, "marks": {}, "elements": {}}
    for mk in MARKS:
        fx = f"{WWCR}/combat_fxon_{mk}.png"
        ct = f"{WWCR}/combat_fxctl_{mk}.png"
        if os.path.exists(fx) and os.path.exists(ct):
            out["marks"][mk] = analyse_pair(fx, ct)

    # element arms -- each has its own fxon; control is the shared combat_fxctl
    for el in ("fire", "earth", "water", "wind"):
        for mk in ("05-sustain",):
            fx = f"{WWCR}/t1_{el}_fxon_{mk}.png"
            ct = f"{WWCR}/combat_fxctl_{mk}.png"
            if os.path.exists(fx) and os.path.exists(ct):
                out["elements"][f"{el}_{mk}"] = analyse_pair(fx, ct)

    with open(os.path.join(OUT, "cleanroom_stills.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    print("mark            authored@2   fine_b0b1@2   N_eff@2   hue    sat")
    for mk, r in out["marks"].items():
        if not r:
            continue
        print(f"{mk:16s} {r['authored_px']['2']:>8d} "
              f"{r['fine_share_b0b1']['2']:>12.4f} "
              f"{r['n_eff']['2']:>9.2f} "
              f"{r.get('hue_circmean', float('nan')):>6.3f} "
              f"{r.get('sat_mean', float('nan')):>6.3f}")
    print()
    for k, r in out["elements"].items():
        if not r:
            continue
        print(f"{k:16s} {r['authored_px']['2']:>8d} "
              f"{r['fine_share_b0b1']['2']:>12.4f} "
              f"{r['n_eff']['2']:>9.2f} "
              f"{r.get('hue_circmean', float('nan')):>6.3f} "
              f"{r.get('sat_mean', float('nan')):>6.3f}")


if __name__ == "__main__":
    main()
