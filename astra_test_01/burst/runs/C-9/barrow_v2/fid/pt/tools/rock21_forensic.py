#!/usr/bin/env python3
"""BV2F PT (R-C9-272 (d); jack-ryan pilot-4 Gate-2 s4): P4 ROCK 2_1 forensic, 0 images, no Godot. Chunk 2_1 is the stone
circle. Is its rock-spectrum FAIL (0.323 vs bar 0.19) the clean-cut DRESSED stone tops Matt asked for (R-C9-244(b): no
snow-cap lumps; LV's blockout) or the PAINT? PH's own P4 instrument (p4_texture: windows, spectrum_shape, pooled v1
spectrum), imported read-only, on the pilot-4 painting, with chunk 2_1's rock mask SPLIT:
  by object: ring_stones (+ ring_fallen) | every other rock in 2_1
  within the ring stones: TOPS (each stone's upper 30 % on screen = its top face and cap) | FACES (the rest)
  and a TOPS-REMOVED rock mask (2_1 rock less the stone tops)
-> fid/pt/r272/rock21_forensic.json"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
sys.path.insert(0, FID + "/ph/harness")
import p4_texture as T
import pilot_harness as PHn
from common import rgb_to_lab, luma

x0, y0, x1, y1 = dict(PHn.CHUNKS)["2_1"]
masks_v1, static_v1 = T.v1_classes()
per = T.v1_pool(None, masks_v1, static_v1)
bars = T.v1_bars(per)
_, ps = T.pooled(per, "rock")
idx, tab = PHn.ids_built()
rockids = [k for k, v in tab.items() if v["class"] == "rock" and (v.get("piece") in ("model", "instance", "group") or str(v.get("piece", "")).startswith("instance"))]
ring = [k for k in rockids if str(tab[k]["id"]).startswith(("ring_stones", "ring_fallen"))]
P = PHn.painting()[y0:y1, x0:x1]
I = idx[y0:y1, x0:x1]
gray = luma(P)
rock = np.isin(I, rockids)
rs = np.isin(I, ring)
tops = np.zeros_like(rs)
lab, n = ndimage.label(rs)
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    if sl is None:
        continue
    h = sl[0].stop - sl[0].start
    sub = lab[sl] == i
    cut = int(round(0.30 * h))
    t = np.zeros_like(sub); t[:cut] = sub[:cut]
    tops[sl] |= t


def spec(m):
    m2 = ndimage.binary_erosion(m, iterations=3)
    w = T.windows(m2)
    s = T.spectrum_shape(gray, w)
    return {"px": int(m2.sum()), "windows": len(w),
            "spec_dist": None if s is None else round(float(np.sqrt(np.mean((s - ps) ** 2))), 3)}


# windows at P4's 0.9 coverage are scarce on small stones: also report at 0.7 (non-binding, for attribution only)
def spec07(m):
    m2 = ndimage.binary_erosion(m, iterations=3)
    w = T.windows(m2, frac=0.7)
    s = T.spectrum_shape(gray, w)
    return {"windows": len(w), "spec_dist": None if s is None else round(float(np.sqrt(np.mean((s - ps) ** 2))), 3)}


res = {"_what": __doc__.split("\n")[0], "bar_rock_spec": round(bars["rock"]["spec"], 3), "ring_ids": [tab[k]["id"] for k in ring],
       "groups": {}}
for nm, m in {"all_rock_2_1 (P4's mask)": rock, "ring_stones": rs, "other_rock": rock & ~rs, "ring_tops": tops,
              "ring_faces": rs & ~tops, "rock_minus_ring_tops": rock & ~tops}.items():
    res["groups"][nm] = {"p4_0.9": spec(m), "cov_0.7": spec07(m)}
json.dump(res, open(FID + "/pt/r272/rock21_forensic.json", "w"), indent=1)
print(json.dumps(res, indent=1))
