#!/usr/bin/env python3
"""C-9 image bake-off, JOB 1 build: ONE Tripo build from the better candidate's best sheet.

    python3 04_build_j1.py nbp_a

THE PICK, AND WHY IT IS NOT JUST THE TOP NUMBER. By mirror IoU Nano Banana Pro is the better
candidate (0.904 / 0.732 against Nano Banana's 0.712 / 0.629), and its best sheet is variant
a. It is also the ONLY candidate sheet whose two profiles face the right ways: Pro b's RIGHT
view and both Nano Banana sheets' LEFT views face the wrong way, which a multiview build turns
into a mirrored or broken body. Pro a's faults -- text labels, cell borders, the tattoo on the
wrong arm in its FRONT view -- are paint, not geometry: the labels and borders are separate
components, and the largest-component cut below drops them before Tripo sees anything.

SAME PLACEMENT AS NB-1_b's BUILD (nb_t8/01_matte_views.py): each quarter's figure on a white
1024 canvas at ONE common scale set by the tallest view (0.88 of the canvas), soles on one
baseline at 0.94, sent in Tripo's order front, LEFT, back, RIGHT with the same arguments.
Anything else would make the comparison with NB-1_b's build a comparison of placements.
"""
import json
import os
import pathlib
import subprocess
import sys
import time

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
os.environ["FAL_LEDGER"] = str(HERE / "fal_spend_R-C9-79.json")
os.environ["FAL_BUDGET"] = "5.00"
sys.path.insert(0, str(HERE.parent / "t10_barrow"))
import fal_ledger  # noqa: E402

QUAD = {"front": (0, 0), "right": (1, 0), "back": (0, 1), "left": (1, 1)}
EP = "tripo3d/h3.1/multiview-to-3d"


def main() -> int:
    import fal_client
    name = sys.argv[1]
    score = json.loads((HERE / "score_j1.json").read_text())[name]
    im = Image.open(score["matte"]).convert("RGBA")
    W, H = im.size
    figs = {}
    for v, (c, r) in QUAD.items():
        q = im.crop((c * W // 2, r * H // 2, (c + 1) * W // 2, (r + 1) * H // 2))
        a = np.asarray(q)[..., 3] > 128
        lab, n = ndimage.label(a)
        keep = lab == 1 + int(np.argmax(ndimage.sum(a, lab, range(1, n + 1))))
        arr = np.asarray(q).copy()
        arr[..., 3] = np.where(keep, arr[..., 3], 0)          # drop labels, borders, specks
        ys, xs = np.nonzero(keep)
        figs[v] = Image.fromarray(arr).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    hmax = max(f.size[1] for f in figs.values())
    S, base = 0.88 * 1024 / hmax, int(1024 * 0.94)
    pd = HERE / "j1_build" / "placed"
    pd.mkdir(parents=True, exist_ok=True)
    for v, f in figs.items():
        g = f.resize((max(1, round(f.size[0] * S)), max(1, round(f.size[1] * S))), Image.LANCZOS)
        can = Image.new("RGB", (1024, 1024), (255, 255, 255))
        can.paste(g, ((1024 - g.size[0]) // 2, base - g.size[1]), g)
        can.save(pd / ("%s_%s.jpg" % (name, v)), quality=95)
    glb = HERE / "j1_build" / ("%s_tripo.glb" % name)
    if glb.exists():
        print("already built", glb)
        return 0
    before = fal_ledger.check(EP)                    # refuse BEFORE the upload
    urls = [fal_client.upload_file(str(pd / ("%s_%s.jpg" % (name, v))))
            for v in ("front", "left", "back", "right")]
    t0 = time.time()
    r = fal_client.subscribe(EP, arguments={"image_urls": urls, "texture": True, "pbr": False,
                                            "texture_quality": "detailed"})
    sec = time.time() - t0
    run = fal_ledger.record(EP, "J1 build from %s" % name, sec)
    url = (r.get("model_mesh") or {}).get("url") or next(
        (x.get("url") for x in r.values() if isinstance(x, dict) and str(x.get("url", "")).endswith(".glb")), None)
    subprocess.run(["curl", "-s", "-L", "-o", str(glb), url], check=True)
    print("built %s in %.0f s -> %s (%.1f MB)   fal running $%.4f -> $%.4f"
          % (name, sec, glb.name, glb.stat().st_size / 1e6, before, run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
