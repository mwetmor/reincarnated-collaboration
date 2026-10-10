#!/usr/bin/env python3
"""BV2F PT R-C9-389 add-on (for R-C9-390's web build): the PHONE variant of site_ph4's painted data, by v1's own recipe
(barrow_full/tools/paint_world_prep.py web(): the painting within 4096 px and the bakes at 512, lossy WebP q90; the light
map at a quarter; everything else copied as is), every file's sha256 in painted_web/manifest.json. The manifest keeps
the desktop manifest's other keys (frame, snow, water, reeds, heather...), so the scene loads it the same way; `frame.px`
stays the PLATE's (6656 x 4864): the painting is sampled by normalised plate UV, so a scaled painting projects the same.
    python3 fid/pt/tools/site4_web.py [--q 90]
Report: fid/pt/site4/painted_web_prep.json (bytes, the WebP cost measured as in v1)."""
import hashlib
import json
import os
import shutil
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.normpath(os.path.join(FID, "../../barrow_full/godot/data/bv2f/site_ph4"))
OUT, WEB = os.path.join(D, "painted"), os.path.join(D, "painted_web")
WEB_MAX_PX, WEB_BAKE_PX, WEB_LIT_SCALE = 4096, 512, 4               # v1's constants (paint_world_prep.py)
Q = int(sys.argv[sys.argv.index("--q") + 1]) if "--q" in sys.argv else 90


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    os.makedirs(os.path.join(WEB, "bakes"), exist_ok=True)
    man = json.load(open(os.path.join(OUT, "manifest.json")))
    for k in ("painting", "lit"):
        assert sha(os.path.join(OUT, man[k]["file"])) == man[k]["sha256"], "desktop %s is not the manifest's" % k
    rep = {"_what": "R-C9-389: site_ph4's phone data (fid/pt/tools/site4_web.py = v1 paint_world_prep web()), and what the downsizing cost",
           "from": "data/bv2f/site_ph4/painted/manifest.json", "desktop_painting_sha256": man["painting"]["sha256"]}
    P = Image.open(os.path.join(OUT, man["painting"]["file"])).convert("RGB")
    k = WEB_MAX_PX / float(max(P.size))
    wsz = (int(round(P.size[0] * k)), int(round(P.size[1] * k)))
    Pw = P.resize(wsz, Image.LANCZOS)
    pp = os.path.join(WEB, "painting.bin")
    Pw.save(pp, format="WEBP", quality=Q, method=6)
    dec = np.asarray(Image.open(pp).convert("RGB")).astype(np.float64)
    rep["painting"] = {"px": list(wsz), "scale": round(k, 4), "bytes": os.path.getsize(pp), "webp_q": Q,
                       "webp_vs_lossless_same_size_mean_abs": round(float(np.abs(dec - np.asarray(Pw).astype(np.float64)).mean()), 3)}
    wm = {k_: v for k_, v in man.items() if k_ not in ("painting", "ground_as_painted", "lit", "bakes")}
    wm["_what"] = man["_what"] + " -- THE PHONE PAGE'S (fid/pt/tools/site4_web.py, v1's --web recipe)"
    wm["painting"] = {"file": "painting.bin", "sha256": sha(pp), "px": list(wsz),
                      "_": "the accepted paint-over within %d px, lossy WebP q%d (frame.px stays the plate's: sampled by normalised UV)" % (WEB_MAX_PX, Q)}
    wm["ground_as_painted"] = dict(wm["painting"])
    W, H = man["frame"]["px"]
    L_ = Image.open(os.path.join(OUT, man["lit"]["file"]))
    lw = (W // WEB_LIT_SCALE, H // WEB_LIT_SCALE)
    lp = os.path.join(WEB, "lit.bin")
    L_.resize(lw, Image.BILINEAR).save(lp, format="PNG")
    wm["lit"] = {"file": "lit.bin", "sha256": sha(lp), "px": list(lw), "_": man["lit"]["_"] + " -- a quarter, for the phone"}
    wm["bakes"] = {}
    bsum = 0
    for pid, b in man["bakes"].items():
        dst = os.path.join(WEB, "bakes", "%s.bin" % pid)
        Image.open(os.path.join(OUT, b["file"])).convert("RGB").resize((WEB_BAKE_PX, WEB_BAKE_PX), Image.LANCZOS).save(dst, format="WEBP", quality=Q, method=6)
        wm["bakes"][pid] = {"file": "bakes/%s.bin" % pid, "sha256": sha(dst)}
        bsum += os.path.getsize(dst)
    rep["bakes"] = {"count": len(wm["bakes"]), "px": WEB_BAKE_PX, "bytes": bsum}
    copied = []
    for f in sorted(os.listdir(OUT)):
        if f in ("painting.bin", "lit.bin", "manifest.json", "bakes"):
            continue
        shutil.copyfile(os.path.join(OUT, f), os.path.join(WEB, f))
        copied.append({"file": f, "sha256": sha(os.path.join(WEB, f)), "bytes": os.path.getsize(os.path.join(WEB, f))})
    rep["copied_as_is"] = copied
    json.dump(wm, open(os.path.join(WEB, "manifest.json"), "w"), indent=1)
    rep["manifest_sha256"] = sha(os.path.join(WEB, "manifest.json"))
    rep["total_bytes"] = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(WEB) for f in fs)
    json.dump(rep, open(os.path.join(FID, "pt/site4/painted_web_prep.json"), "w"), indent=1)
    print(json.dumps({k_: rep[k_] for k_ in ("painting", "bakes", "manifest_sha256", "total_bytes")}, indent=1))


if __name__ == "__main__":
    main()
