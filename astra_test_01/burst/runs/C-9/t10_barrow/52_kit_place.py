#!/usr/bin/env python3
"""C-9 T10-1b: lay each chosen kit object's four views on one canvas each, ready for Tripo.

Same as 33_place_views.py, kept deliberately: one common scale across the four views, set
by the largest of WIDTH and HEIGHT rather than by height alone, and every view bottom-aligned
to the same baseline.

The log is why the width half of that rule exists here. Its FRONT is 545 px wide and 191
tall; its RIGHT is an END-ON disc, 155 wide. Scaling each view to a common HEIGHT would
leave the two right, and scaling by height across the set would be harmless -- but scaling
the SET by its widest view is what keeps a 2.6 m log from being drawn at the same canvas
width as a 1.0 m cairn, and the builder reads relative proportion out of exactly that.

Views are named front / right / back / left as they sit on the sheet. Tripo's multiview
endpoint wants front, LEFT, back, RIGHT. That reorder happens once, in 53_kit_build.py.
"""
import json
import pathlib

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE / "kit_work"
CANVAS = 1024
FILL = 0.86
BASE = 0.94
VIEWS = ["front", "right", "back", "left"]


def main() -> None:
    picks = json.loads((WORK / "choose_kit.json").read_text())["picks"]
    out = {}
    (WORK / "placed").mkdir(exist_ok=True)
    for obj, p in picks.items():
        v = p["variant"]
        figs = {}
        for nm in VIEWS:
            im = Image.open(WORK / "cells" / ("%s_%s_%s.png" % (obj, v, nm))).convert("RGBA")
            a = np.asarray(im)[..., 3] > 128
            ys, xs = np.nonzero(a)
            figs[nm] = im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
        big = max(max(f.size) for f in figs.values())
        s = FILL * CANVAS / big
        meta = {"variant": v, "scale": round(s, 4), "views": {}}
        for nm, f in figs.items():
            r = f.resize((max(1, round(f.width * s)), max(1, round(f.height * s))), Image.LANCZOS)
            can = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
            can.paste(r, ((CANVAS - r.width) // 2, int(CANVAS * BASE) - r.height), r)
            can.save(WORK / "placed" / ("%s_%s.jpg" % (obj, nm)), quality=95)
            meta["views"][nm] = {"src_px": list(f.size), "placed_px": list(r.size)}
        out[obj] = meta
        print("%-7s variant %s  scale %.4f  placed %s"
              % (obj, v, s, {k: m["placed_px"] for k, m in meta["views"].items()}))
    (WORK / "placed_views.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
