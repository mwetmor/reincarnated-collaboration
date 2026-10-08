#!/usr/bin/env python3
"""P5 a1 re-instrumented for DEV-25c's INNER-128 paste (§ 48 (d); jack-ryan pilot-4 Gate-2 § 6 item 5). v1's 9.569 (full 256)
does not transfer. a1 is computed over ONE 128-px half of the 256-px overlap's width:
   band E = [0, 128)   the newer chunk's canvas-EDGE half (the neighbour-interior side)
   band C = [128, 256) the newer chunk's interior-side half
Which half is DEV-25c's pasted band is read from DEV-25c's Tier-B paste mask when it lands; BOTH bars are derived now,
before any Phase 3' value exists, so the choice cannot follow a reading. Per band: v1 bar (max segment over T10BF raw
canvases), C2 R-C9-158 must FAIL, C3 constructed fails (6 % second hand on 1_1; +6 sRGB on 3_2's rendition of the band of
2_2|3_2), masking control PS3b (raw) must FAIL, specificity PS2 0_1/0_2 and PS3a 1_1/1_2 reported. -> results/p5v2c_calibration.json"""
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p5_seams as S5
import p5v2 as V

BANDS = {"E": (0, 128), "C": (128, 256)}
R = {"_what": __doc__.split("\n")[0], "bands": BANDS}
v1p = V.v1_paths()
bvp = S5.canvases("BVSW")
ps3b = S5.canvases("BV2F-PS3")
ps2 = S5.canvases("BV2F-PS2")
p3a = {k: v["path"] for k, v in V.manifest_pilot3().items()}


def join(rows, j):
    return [r for r in rows if r["join"] == j][0]


for name, band in BANDS.items():
    lo, hi = band
    a_v1 = V.a_set(v1p, band=band)
    bar = max(r["a1_max"] for r in a_v1)
    a_158 = V.a_set(bvp, band=band)
    sh = V.a_set(v1p, band=band, mod=lambda k, im: np.clip(im * np.array([1.06, 0.98, 0.92]), 0, 255) if k == "1_1" else im)

    def plus6(k, im, lo=lo, hi=hi):
        if k != "3_2":
            return im
        im = im.copy()
        im[:, lo:hi] = np.clip(im[:, lo:hi] + 6.0, 0, 255)       # 3_2's rendition of the band of 2_2|3_2 (its left strip)
        return im
    dense = V.a_set(v1p, band=band, mod=plus6)
    a_m = V.a_set(ps3b, band=band)
    r2 = V.a_pair(V.load(ps2["0_1"]), V.load(ps2["0_2"]), False, band)
    r3 = V.a_pair(V.load(p3a["1_1"]), V.load(p3a["1_2"]), False, band)
    R[name] = {
        "v1_bar": bar, "v1_bar_join": max(a_v1, key=lambda r: r["a1_max"])["join"],
        "C2_R-C9-158": {"a1_max": max(r["a1_max"] for r in a_158), "joins_over": [r["join"] for r in a_158 if r["a1_max"] > bar],
                        "FAIL": any(r["a1_max"] > bar for r in a_158)},
        "C3_second_hand_1_1": {"a1_max": max(r["a1_max"] for r in sh), "RED": max(r["a1_max"] for r in sh) > bar},
        "C3_dense_plus6_2_2|3_2": {"a1_join": join(dense, "2_2|3_2")["a1_max"], "unmodified": join(a_v1, "2_2|3_2")["a1_max"],
                                   "RED": join(dense, "2_2|3_2")["a1_max"] > bar},
        "masking_control_PS3b_raw": {"joins_over": [r["join"] for r in a_m if r["a1_max"] > bar], "FAIL": any(r["a1_max"] > bar for r in a_m)},
        "specificity": {"PS2 0_1/0_2": round(max(r2["a1"]), 3), "PS3a 1_1/1_2": round(max(r3["a1"]), 3)}}
    R[name]["usable"] = R[name]["C2_R-C9-158"]["FAIL"] and R[name]["C3_second_hand_1_1"]["RED"] and R[name]["C3_dense_plus6_2_2|3_2"]["RED"] \
        and R[name]["masking_control_PS3b_raw"]["FAIL"]
    dump(R, str(PH / "results/p5v2c_calibration.json"))
    print(name, json.dumps(R[name])[:900])
