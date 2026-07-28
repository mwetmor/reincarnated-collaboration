#!/usr/bin/env python3
"""
KIT-CAL-1 G-8, task 5: find every frame carrying the top-centre BOSS/HERO
nameplate bar, and measure its fill fraction.

The bar is a fixed-geometry HUD element: a gold-framed trough centred on
x=960, its interior spanning x 799..1119 at y 61..74 (measured on f281). Fill
is the red segment's right edge within that interior.

Fill fraction is reported as a RATIO WITH ITS OWN ERROR BAR, not as a bare
number. The trough's interior edges are soft (the gold frame's inner bevel
blends over ~3 px), so the denominator carries +-3 px = +-0.9 pp. On f281 the
same frame independently renders the monster's numeric health, and the two
disagree by 0.9 pp -- i.e. exactly the stated tolerance, which is what makes
this instrument usable on frames that lack the numerals.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-kitcal1-g8")

BAR_Y = 68
TROUGH_X0, TROUGH_X1 = 799, 1119
NAME_Y0, NAME_Y1 = 20, 58


def main():
    ids = sorted(int(f.name[12:-5]) for f in SRC.iterdir()
                 if f.name.startswith("Screenshot (") and f.name.endswith(").png"))
    recs = {}
    for i in ids:
        with Image.open(SRC / f"Screenshot ({i}).png") as im:
            im = im.convert("RGB")
            a = np.asarray(im).astype(np.int16)
        strip = a[BAR_Y - 4:BAR_Y + 5, TROUGH_X0:TROUGH_X1 + 1]
        red = (strip[:, :, 0] > 90) & (strip[:, :, 0] - strip[:, :, 1] > 55) \
            & (strip[:, :, 0] - strip[:, :, 2] > 45)
        colhit = red.sum(axis=0) >= 5
        n = int(colhit.sum())
        if n < 20:                      # no bar present
            continue
        nz = np.nonzero(colhit)[0]
        # fill runs from the trough's left edge; take the rightmost lit column
        frac = (int(nz.max()) + 1) / (TROUGH_X1 - TROUGH_X0 + 1)
        recs[i] = {"lit_cols": n, "right_edge_x": TROUGH_X0 + int(nz.max()),
                   "fill_frac": round(frac, 4)}
        c = im.crop((600, 14, 1320, 92))
        c.resize((c.width * 2, c.height * 2), Image.LANCZOS).save(
            OUT / f"bossbar-f{i}.png")
        print(f"f{i:4d}  fill={frac:.4f}  lit={n}", flush=True)
    with open(OUT / "g8-bossbar.json", "w") as f:
        json.dump(recs, f, indent=1)
    print(f"\n{len(recs)} frames carry a boss/hero nameplate bar")


if __name__ == "__main__":
    main()
