#!/usr/bin/env python3
"""BV2F PT sea pass (R-C9-321): crops of one patch -- BEFORE (its staged base) | AFTER (pasted) | the new GUIDE.
  play zoom = the whole 1536x1024 canvas at 1/2 (the game's view of the plate is ~1/2 at 1080p);
  1:1       = 640x480 windows at the region's support centre and at the 3 support-edge points farthest apart.
    python3 fid/pt/tools/sea_crops.py <name> <att> [outdir]   -> fid/pt/ph3/sea/crops/<name>-<att>_{play,1to1_k}.jpg"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
Image.MAX_IMAGE_PIXELS = None
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
name, att = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else FID + "/pt/ph3/%s/crops" % ("sea" if os.environ.get("SEA_ROUND", "r321") == "r321" else "sea_" + os.environ["SEA_ROUND"])
os.makedirs(out, exist_ok=True)
S = json.load(open(FID + "/pt/dev24/spec_%s.json" % name))
x0, y0 = S["rect_xy"]
crop = lambda p: np.asarray(Image.open(p).convert("RGB"))[y0:y0 + 1024, x0:x0 + 1536]
_stp = FID + "/pt/ph3/%s/state.json" % ("sea" if os.environ.get("SEA_ROUND", "r321") == "r321" else "sea_" + os.environ["SEA_ROUND"])
_acc = [a for a in json.load(open(_stp))["accepted"] if a["pin"]["name"] == "%s-%s" % (name, att)] if os.path.exists(_stp) else []
bef = crop(_acc[0]["base"] if _acc else S["painting"])   # the accepted patch's own staged base (after a rebuild)
_ps = FID + "/pt/dev24/%s/painting_sea_%s.png" % (name, att)   # the accepted (pinned soft-corr) paste when present
aft = crop(_ps if os.path.exists(_ps) else FID + "/pt/dev24/%s/painting_patched_%s.png" % (name, att)); gd = crop(S["guide_png"])
R = np.asarray(Image.open(S["region"]["png"])) > 127
sup = (aft != bef).any(-1)
lab = lambda a, t: (Image.fromarray(a), t)


def strip(arrs, w):
    ims = [Image.fromarray(a).resize((w, int(w * a.shape[0] / a.shape[1])), Image.LANCZOS) if a.shape[1] != w else Image.fromarray(a) for a in arrs]
    H = ims[0].height
    o = Image.new("RGB", (w * len(ims) + 8 * (len(ims) - 1), H), (255, 255, 255))
    for i, im in enumerate(ims):
        o.paste(im, (i * (w + 8), 0))
    return o


strip([bef, aft, gd], 768).save(os.path.join(out, "%s-%s_play.jpg" % (name, att)), quality=88)
pts = []
if sup.any():
    ys, xs = np.nonzero(sup)
    pts.append((int(np.median(ys)), int(np.median(xs))))
    e = sup & ~ndimage.binary_erosion(sup)
    ey, ex = np.nonzero(e)
    if len(ey):
        idx = np.random.default_rng(0).choice(len(ey), min(4000, len(ey)), replace=False)
        cand = list(zip(ey[idx], ex[idx]))
        for _ in range(3):   # farthest-point picks along the support edge
            d = [min((cy - py) ** 2 + (cx - px) ** 2 for py, px in pts) for cy, cx in cand]
            pts.append(tuple(int(v) for v in cand[int(np.argmax(d))]))
rec = []
for k, (cy, cx) in enumerate(pts):
    a, b = max(0, min(1024 - 480, cy - 240)), max(0, min(1536 - 640, cx - 320))
    strip([bef[a:a + 480, b:b + 640], aft[a:a + 480, b:b + 640], gd[a:a + 480, b:b + 640]], 640).save(os.path.join(out, "%s-%s_1to1_%d.jpg" % (name, att, k)), quality=92)
    rec.append({"k": k, "plate_xy": [x0 + b, y0 + a], "size": [640, 480]})
json.dump({"name": name, "att": att, "rect_xy": [x0, y0], "changed_px": int(sup.sum()), "region_px": int(R.sum()), "crops_1to1": rec},
          open(os.path.join(out, "%s-%s_crops.json" % (name, att)), "w"), indent=1)
print(name, att, "changed", int(sup.sum()), "crops", len(rec) + 1)
