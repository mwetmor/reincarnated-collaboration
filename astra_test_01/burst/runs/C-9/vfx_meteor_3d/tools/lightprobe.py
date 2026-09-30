#!/usr/bin/env python3
"""C-9 lane B: her colour under the Meteor's fire, desktop (Forward+) against web (Compatibility, --as-web).
Her silhouette = pixels where the fire-off frame differs from the her-hidden frame; over it, the per-channel
LINEAR ratio of fire-on to fire-off (the ruling's instrument for the other meeting rules: a lit/unlit ratio).
   lightprobe.py <fplus dir> <compat dir> [out.json]"""
import json, sys, numpy as np
from PIL import Image
def lin(a):
    a = a / 255.0
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
def load(d, k):
    return np.asarray(Image.open(f"{d}/{k}.png").convert("RGB")).astype(np.float64)
res = {}
masks = {}
for name, d in (("forward_plus", sys.argv[1]), ("compat_web", sys.argv[2])):
    A, B, D, C = (load(d, k) for k in ("A_off", "B_on", "D_on_hot", "C_hidden"))
    masks[name] = np.abs(A - C).sum(-1) > 12
m = masks["forward_plus"] & masks["compat_web"]           # her pixels in BOTH frames
for name, d in (("forward_plus", sys.argv[1]), ("compat_web", sys.argv[2])):
    A, B, D = (lin(load(d, k)) for k in ("A_off", "B_on", "D_on_hot"))
    a, b, dd = A[m].mean(0), B[m].mean(0), D[m].mean(0)
    lit = (B[m].sum(-1) > A[m].sum(-1) * 1.03)
    res[name] = {"her_px": int(m.sum()), "off_mean_lin": a.round(4).tolist(), "on_mean_lin": b.round(4).tolist(),
                 "ratio_on_off": (b / a).round(4).tolist(), "ratio_hot_off": (dd / a).round(4).tolist(),
                 "lit_share": round(float(lit.mean()), 4)}
f, w = res["forward_plus"], res["compat_web"]
res["diff_web_minus_desktop"] = {
    "ratio_on_off": (np.array(w["ratio_on_off"]) - np.array(f["ratio_on_off"])).round(4).tolist(),
    "ratio_hot_off": (np.array(w["ratio_hot_off"]) - np.array(f["ratio_hot_off"])).round(4).tolist(),
    "on_mean_lin": (np.array(w["on_mean_lin"]) - np.array(f["on_mean_lin"])).round(4).tolist(),
    "lit_share": round(w["lit_share"] - f["lit_share"], 4)}
print(json.dumps(res, indent=1))
if len(sys.argv) > 3:
    json.dump(res, open(sys.argv[3], "w"), indent=1)
