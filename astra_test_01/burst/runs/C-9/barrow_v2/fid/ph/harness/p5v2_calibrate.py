#!/usr/bin/env python3
"""P5 v2 calibration C1-C5 (jack-ryan pre-ruling 309c4c41b; R-C9-251). -> results/p5v2_calibration.json
No pilot-3 build value is read here except the C4 specificity join PS3a 1_1/1_2, which the pre-ruling itself names."""
import json
import math
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p5_seams as S5
import p5v2 as V

OUT = PH / "results/p5v2_calibration.json"
R = {"_what": __doc__.split("\n")[0], "params": {"a_sigma": 6, "a_trim": V.TRIM, "a_seg": V.SEG_A, "a2_hp_sigma": 3, "a2_eps": 0.5,
                                                 "c_seg": V.SEG_C, "c_lab_sigma": 4, "c_hp_sigma": 3, "c_eps": 0.05,
                                                 "c_offsets": V.OFFS, "c_run": 2, "c_unpainted_window": 110}}


def save():
    dump(R, str(OUT))


def b_of(img):
    cols, rows = img.shape[1] // V.SX, img.shape[0] // V.SY
    return S5.seam_vis(img, cols, rows)


# ------------------------------------------------------------------ v1 (bars) and C1
v1p = V.v1_paths()
a_v1 = V.a_set(v1p)
V1IMG = BF / "paint/barrow_full_painted.png"
v1img = load_rgb(V1IMG)
c_v1 = V.c_measure(v1img, list(v1p))
b_v1 = b_of(v1img)
bars = {"a1": max(r["a1_max"] for r in a_v1), "a2": max(r["a2_max"] for r in a_v1),
        "b": 0.799, "c_tone": V.c_max(c_v1, "tone"), "c_grain": V.c_max(c_v1, "grain")}
R["bars_v1"] = bars
R["v1"] = {"a": a_v1, "c": c_v1, "b": b_v1, "raw_mad_max": max(r["raw_mad"] for r in a_v1),
           "verdict": V.verdict_row(a_v1, b_v1, c_v1, bars)}
save()
print("bars", bars, "v1 PASS", R["v1"]["verdict"]["pass"])

V.SCR.mkdir(parents=True, exist_ok=True)
off = V.SCR / "T10BF_flagsoff.png"
V.stitch("T10BF", 4, 4, off, V.OFF)
same_bytes = V.sha(off) == V.sha(V1IMG)
same_px = bool(np.array_equal(load_rgb(off), v1img))
on = V.SCR / "T10BF_dev23_25.png"
V.stitch("T10BF", 4, 4, on, V.ON2325)
onimg = load_rgb(on)
c_on, b_on = V.c_measure(onimg, list(v1p)), b_of(onimg)
allon = V.SCR / "T10BF_allflags.png"
V.stitch("T10BF", 4, 4, allon, V.ALLON)
alimg = load_rgb(allon)
c_al, b_al = V.c_measure(alimg, list(v1p)), b_of(alimg)
R["C1"] = {"flags_off_byte_identical": same_bytes, "flags_off_pixel_identical": same_px,
           "flags_off_sha": V.sha(off), "v1_sha": V.sha(V1IMG),
           "dev23_25_on": {"b_max": max(s["score"] for s in b_on), "c_tone_max": V.c_max(c_on, "tone"), "c_grain_max": V.c_max(c_on, "grain"),
                           "verdict_b_c": V.verdict_row([], b_on, c_on, bars)},
           "all_build_flags_on_(23,25,26,27)_reported": {"b_max": max(s["score"] for s in b_al), "c_tone_max": V.c_max(c_al, "tone"),
                                                       "c_grain_max": V.c_max(c_al, "grain"), "verdict_b_c": V.verdict_row([], b_al, c_al, bars)}}
save()
print("C1", R["C1"]["flags_off_byte_identical"], R["C1"]["flags_off_pixel_identical"], R["C1"]["dev23_25_on"]["verdict_b_c"]["pass"])

# ------------------------------------------------------------------ C2: R-C9-158 (BVSW)
bvp = S5.canvases("BVSW")
a_158 = V.a_set(bvp)
sw = load_rgb(B2 / "paint/section_sw/section_sw_painted.png")
c_158 = V.c_measure(sw, list(bvp))
b_158 = b_of(sw)
v158 = V.verdict_row(a_158, b_158, c_158, bars)
R["C2_R-C9-158"] = {"verdict": v158, "a1_max": max(r["a1_max"] for r in a_158), "a2_max": max(r["a2_max"] for r in a_158),
                    "b_max": max(s["score"] for s in b_158), "c_tone_max": V.c_max(c_158, "tone"), "c_grain_max": V.c_max(c_158, "grain"),
                    "n_over": {k: len(v) for k, v in v158.items() if k != "pass"}, "raw_mad_max": max(r["raw_mad"] for r in a_158)}
save()
print("C2", v158["pass"], R["C2_R-C9-158"]["n_over"])

# ------------------------------------------------------------------ C3: constructed fails
C3 = {}
# a1 (i): the existing 6 % hue/tone second hand on 1_1
a_i = V.a_set(v1p, mod=lambda k, im: np.clip(im * np.array([1.06, 0.98, 0.92]), 0, 255) if k == "1_1" else im)
C3["a1_i_second_hand_1_1"] = {"a1_max": max(r["a1_max"] for r in a_i), "a1_bar": bars["a1"],
                              "red": max(r["a1_max"] for r in a_i) > bars["a1"], "a2_max": max(r["a2_max"] for r in a_i)}


def strip32(k, im, f):
    """modify v1 3_2's rendition of the 2_2|3_2 strip (its own left 256 columns)"""
    if k != "3_2":
        return im
    im = im.copy()
    im[:, :V.OV] = f(im[:, :V.OV])
    return im


def join(rows, j):
    return [r for r in rows if r["join"] == j][0]


def norm_mad(paths, j, mod=None):
    """the REJECTED texture-normalised MAD, for the record (PH's reading of it: raw strip MAD / mean of the two strips'
    HF std (luma - G_sigma3)); not jack-ryan's exact implementation"""
    a, b = j.split("|")
    A, B = V.load(paths[a]), V.load(paths[b])
    if mod:
        A, B = mod(a, A), mod(b, B)
    sa, sb = V._strips(A, B, True)
    la, lb = V._luma(sa), V._luma(sb)
    hs = 0.5 * ((la - ndimage.gaussian_filter(la, 3)).std() + (lb - ndimage.gaussian_filter(lb, 3)).std())
    return round(float(np.abs(sa - sb).mean() / hs), 3)


plus6 = lambda k, im: strip32(k, im, lambda s: np.clip(s + 6.0, 0, 255))
a_ii = V.a_set(v1p, mod=plus6)
C3["a1_ii_dense_plus6_on_2_2|3_2"] = {"a1_join": join(a_ii, "2_2|3_2")["a1_max"], "a1_join_unmodified": join(a_v1, "2_2|3_2")["a1_max"],
                                       "a1_bar": bars["a1"], "red": join(a_ii, "2_2|3_2")["a1_max"] > bars["a1"],
                                       "raw_mad_join": join(a_ii, "2_2|3_2")["raw_mad"],
                                       "rejected_normalised_mad_join": norm_mad(v1p, "2_2|3_2", plus6),
                                       "rejected_normalised_mad_join_unmodified": norm_mad(v1p, "2_2|3_2"),
                                       "rejected_normalised_mad_v1_max": max(norm_mad(v1p, r["join"]) for r in a_v1 if "|" in r["join"])}


def soften(s, k=0.67):
    g = np.stack([ndimage.gaussian_filter(s[..., c], 3) for c in range(3)], -1)
    return np.clip(g + k * (s - g), 0, 255)


a_a2 = V.a_set(v1p, mod=lambda k, im: strip32(k, im, soften))
C3["a2_strip_HF_x0.67_on_2_2|3_2"] = {"a2_join": join(a_a2, "2_2|3_2")["a2_max"], "a2_join_unmodified": join(a_v1, "2_2|3_2")["a2_max"],
                                       "a2_bar": bars["a2"], "red": join(a_a2, "2_2|3_2")["a2_max"] > bars["a2"],
                                       "a1_join": join(a_a2, "2_2|3_2")["a1_max"], "raw_mad_join": join(a_a2, "2_2|3_2")["raw_mad"]}
A2_ALIVE = C3["a2_strip_HF_x0.67_on_2_2|3_2"]["red"]
C3["a2_status"] = "KEPT (its constructed fail reads RED)" if A2_ALIVE else "DISCARDED (its constructed fail reads GREEN; mechanism 1 rests on (c))"

# c (i) / (ii) on v1's stitched painting: chunk 3_2's context boundary x = 1280*3 + 256 = 4096, rows 1920..2176 (256 px)
X0, Y0, LEN = V.SX * 3 + V.OV, V.SY * 2 + 384, 256


def tone_step(img, dE):
    out = img.copy()
    reg = out[Y0:Y0 + LEN, X0:X0 + LEN]
    lab0 = rgb_to_lab(reg)
    lo, hi = 0.0, 40.0
    for _ in range(40):                        # a uniform sRGB lift whose mean dE76 over the region = dE
        mid = 0.5 * (lo + hi)
        d = float(np.linalg.norm(rgb_to_lab(np.clip(reg + mid, 0, 255)) - lab0, axis=-1).mean())
        lo, hi = (mid, hi) if d < dE else (lo, mid)
    out[Y0:Y0 + LEN, X0:X0 + LEN] = np.clip(reg + 0.5 * (lo + hi), 0, 255)
    return out, round(0.5 * (lo + hi), 3)


def grain_x(img, k):
    out = img.copy()
    reg = out[Y0 - 16:Y0 + LEN + 16, X0 - 16:X0 + LEN + 16]
    g = np.stack([ndimage.gaussian_filter(reg[..., c], 3) for c in range(3)], -1)
    mod = np.clip(g + k * (reg - g), 0, 255)
    out[Y0:Y0 + LEN, X0:X0 + LEN] = mod[16:-16, 16:-16]
    return out


def c_on(img, what):
    rows = V.c_measure(img, list(v1p))
    b = [x for x in rows if x["boundary"] == "x=%d" % X0 and x["chunk"] == "3_2"][0]
    return b[what + "_max"], V.c_max(rows, what)


for nm, fn, what, stated, bar in (("c_i_tone_step_dE7.16", lambda m: tone_step(v1img, m)[0], "tone", 7.16, bars["c_tone"]),
                                   ("c_ii_grain_x2.5", lambda m: grain_x(v1img, m), "grain", 2.5, bars["c_grain"])):
    val, allmax = c_on(fn(stated), what)
    row = {"stated_magnitude": stated, "boundary": "x=%d rows %d-%d (chunk 3_2)" % (X0, Y0, Y0 + LEN), "value": val, "bar": bar,
           "red": val is not None and val > bar}
    if not row["red"]:
        floor = None
        for m in np.linspace(stated, 2 * stated, 9)[1:]:
            v, _ = c_on(fn(float(m)), what)
            if v is not None and v > bar:
                floor = round(float(m), 3)
                break
        row["detection_floor_magnitude"] = floor
        row["discard_c_" + what] = floor is None
    C3[nm] = row
    save()
# masking control: PS3b (the -r1 set of BV2F-PS3), stitched DEV-23 + DEV-25 ON
ps3b = S5.canvases("BV2F-PS3")                   # highest rN = the PS3b set, which is the point here
mk = V.SCR / "PS3b_dev23_25.png"
V.stitch("BV2F-PS3", 3, 3, mk, V.ON2325)
mimg = load_rgb(mk)
a_m, c_m, b_m = V.a_set(ps3b), V.c_measure(mimg, list(ps3b)), b_of(mimg)
vm = V.verdict_row(a_m, b_m, c_m, bars, A2_ALIVE)
C3["masking_control_PS3b_dev23_25"] = {"canvases": {k: pathlib.Path(p).parent.name for k, p in ps3b.items()}, "verdict": vm,
                                       "n_over": {k: len(v) for k, v in vm.items() if k != "pass"}, "must_FAIL": True,
                                       "c_alone_fails": bool(vm["c_tone_over"] or vm["c_grain_over"])}
R["C3"] = C3
save()
print("C3", {k: (v.get("red") if isinstance(v, dict) else v) for k, v in C3.items()})

# ------------------------------------------------------------------ C4: specificity
ps2 = S5.canvases("BV2F-PS2")
man = V.manifest_pilot3()
p3 = {k: v["path"] for k, v in man.items()}
r_ps2 = V.a_pair(V.load(ps2["0_1"]), V.load(ps2["0_2"]), False)
r_ps3 = V.a_pair(V.load(p3["1_1"]), V.load(p3["1_2"]), False)
R["C4_specificity"] = {
    "PS2 0_1/0_2": {"raw_mad": r_ps2["raw_mad"], "a1_max": round(max(r_ps2["a1"]), 3), "a2_max": round(max(r_ps2["a2"]), 3),
                    "pass": max(r_ps2["a1"]) <= bars["a1"] and (not A2_ALIVE or max(r_ps2["a2"]) <= bars["a2"])},
    "PS3a 1_1/1_2": {"raw_mad": r_ps3["raw_mad"], "a1_max": round(max(r_ps3["a1"]), 3), "a2_max": round(max(r_ps3["a2"]), 3),
                     "pass": max(r_ps3["a1"]) <= bars["a1"] and (not A2_ALIVE or max(r_ps3["a2"]) <= bars["a2"])}}
# ------------------------------------------------------------------ C5: the canvas pin
R["C5_manifest_pilot3"] = man
save()
print("C4", R["C4_specificity"]); print("C5", {k: v["dir"] for k, v in man.items()})
