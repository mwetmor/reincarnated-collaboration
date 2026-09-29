#!/usr/bin/env python3
"""C-9 T9-1a: lay each chosen object's four views on one canvas each, ready for Tripo.

Same shape as nb_t8/01_matte_views.py, with one change that the props need and the figure
did not: the common scale is set by the largest of WIDTH and HEIGHT across the four views,
not by height alone. The coil of rope is 76 px tall and 300 wide -- normalising it by height
would blow it up by 4x and hand Tripo a rope as thick as a tree.

Views are named front / right / back / left as they sit on the sheet. Tripo's multiview
endpoint wants them in the order front, LEFT, back, RIGHT, which is not the sheet order;
that reorder happens once, in 12_build_models.py, and nowhere else.
"""
import json
import pathlib

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
CANVAS = 1024
FILL = 0.86
BASE = 0.94
VIEWS = ["front", "right", "back", "left"]


def main() -> None:
    picks = json.loads((HERE / "choose_props.json").read_text())["picks"]
    out = {}
    (HERE / "placed").mkdir(exist_ok=True)
    for obj, p in picks.items():
        v = p["variant"]
        figs = {}
        for nm in VIEWS:
            im = Image.open(HERE / "cells" / ("%s_%s_%s.png" % (obj, v, nm))).convert("RGBA")
            a = np.asarray(im)[..., 3] > 128
            ys, xs = np.nonzero(a)
            figs[nm] = im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
        big = max(max(f.size) for f in figs.values())
        s = FILL * CANVAS / big
        meta = {"variant": v, "scale": round(s, 4), "views": {}}
        for nm, f in figs.items():
            r = f.resize((max(1, round(f.width * s)), max(1, round(f.height * s))), Image.LANCZOS)
            can = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
            px = (CANVAS - r.width) // 2
            py = int(CANVAS * BASE) - r.height
            can.paste(r, (px, py), r)
            can.save(HERE / "placed" / ("%s_%s.jpg" % (obj, nm)), quality=95)
            meta["views"][nm] = {"src_px": list(f.size), "placed_px": list(r.size)}
        out[obj] = meta
        print("%-6s variant %s  scale %.4f  placed %s"
              % (obj, v, s, {k: m["placed_px"] for k, m in meta["views"].items()}))
    (HERE / "placed_views.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
