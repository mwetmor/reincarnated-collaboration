#!/usr/bin/env python3
"""C-9 T9-1a: find the rows and columns of each sheet FROM THE SHEET, then matte each band.

This replaces an even grid split, which was wrong twice over on T9P-C and wrong invisibly:

  * The band boundary is not the middle. The sheet was asked for two rows; the painter put
    the coil of rope high and the raven low, so an even split at y=512 cut through the
    RAVEN'S NECK. The four "raven" views were headless bodies and the four "rope" views
    were the TOP OF A RAVEN'S HEAD -- and those crops were then SCORED, and produced a
    perfectly reasonable-looking mirror_iou of 0.859 for an object that was not in them.
  * BiRefNet on the whole sheet kept the raven and dropped the coil entirely: on a brown
    gradient it took the one big dark subject and called the rope background. Mattng each
    BAND separately gives it one kind of object at a time and it finds them both.

So: bands and columns come from a background-deviation profile of the sheet itself (a
subject has high-frequency detail, a plate or a smooth gradient does not), each band is
matted on its own, and every cell is checked for its subject TOUCHING a cell edge -- which
is what a bad split looks like from the inside, and what nothing checked for before.
"""
import json
import pathlib
import subprocess

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts"
VIEWS = ["front", "right", "back", "left"]

# sheet -> list of (object, columns) per band, top band first
SHEETS = {
    "T10P-A": [("stone_tall", 4), ("stone_mid", 4)],
    "T10P-B": [("lintel", 4), ("post", 4)],
    "T10P-C": [("rock_large", 4), ("rock_small", 4)],
    "T10P-D": [("birch", 2), ("birch", 2)],     # 1024x1536 portrait 2x2
    "T10P-E": [("stone_short", 4), ("juniper", 4)],
}


def runs(profile: np.ndarray, frac: float, min_len: int) -> list:
    on = profile > profile.max() * frac
    out, s = [], None
    for i, v in enumerate(on):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= min_len:
                out.append((s, i))
            s = None
    if s is not None and len(on) - s >= min_len:
        out.append((s, len(on)))
    return out


def widen(rs: list, lo: int, hi: int) -> list:
    """Grow each run to the MIDPOINT of the gap to its neighbours (and to the edges).

    The run detector trims where detail falls under a tenth of the peak, which on a burnt
    tree is somewhere inside its thinnest twigs. Growing to the gap midpoint costs nothing
    -- there is nothing in a gap, by definition -- and stops the crop deciding where an
    object ends. Without it every snag cell reported its subject touching the frame, and
    that warning was about the crop and not about the picture."""
    out = []
    for i, (a, b) in enumerate(rs):
        na = lo if i == 0 else (rs[i - 1][1] + a) // 2
        nb = hi if i == len(rs) - 1 else (b + rs[i + 1][0]) // 2
        out.append((na, nb))
    return out


def detail(rgb: np.ndarray) -> np.ndarray:
    g = rgb.astype(np.float32).mean(-1)
    return np.abs(g - ndimage.gaussian_filter(g, 24))


def matte(src_img: Image.Image, dst: pathlib.Path) -> Image.Image:
    if not dst.exists():
        import fal_client
        tmp = dst.with_suffix(".src.png")
        src_img.save(tmp)
        url = fal_client.upload_file(str(tmp))
        r = fal_client.subscribe("fal-ai/birefnet/v2", arguments={
            "image_url": url, "model": "General Use (Heavy)",
            "operating_resolution": "2048x2048", "output_format": "png",
            "refine_foreground": True})
        subprocess.run(["curl", "-s", "-L", "-o", str(dst), r["image"]["url"]], check=True)
        tmp.unlink(missing_ok=True)
    return Image.open(dst).convert("RGBA")


def main() -> None:
    (HERE / "work").mkdir(exist_ok=True)
    (HERE / "cells").mkdir(exist_ok=True)
    out = {}
    for sid, bands in SHEETS.items():
        for v in ("a", "b"):
            src = ART / sid / ("%s_%s.png" % (sid, v))
            if not src.exists():
                continue
            im = Image.open(src).convert("RGB")
            d = detail(np.asarray(im))
            rb = widen(runs(d.sum(1), 0.10, im.size[1] // 12), 0, im.size[1])
            print("%s_%s  %s  bands found: %s (expected %d)" % (sid, v, im.size, rb, len(bands)))
            if len(rb) != len(bands):
                # THE ROWS TOUCH. Tall subjects can fill their band and meet the next one,
                # so the detail profile never drops far enough to separate them. Fall back
                # to the QUIETEST row near the even split rather than to the even split
                # itself -- on T10P-A_b the midpoint carries 0.304 of peak detail (a stone
                # crosses it) while row 504 carries 0.114. That is the same cut that took a
                # raven's head off in T9, caught before the cut this time instead of after.
                if len(rb) == 1 and len(bands) == 2:
                    prof = d.sum(1)
                    prof = prof / max(prof.max(), 1e-9)
                    w0, w1 = int(im.size[1] * 0.43), int(im.size[1] * 0.58)
                    cut = w0 + int(np.argmin(prof[w0:w1]))
                    print("   rows touch; splitting at the quietest row %d (detail %.3f of "
                          "peak; the midpoint carries %.3f)"
                          % (cut, prof[cut], prof[im.size[1] // 2]))
                    rb = [(0, cut), (cut, im.size[1])]
                else:
                    print("   HALT: band count disagrees with the layout asked for")
                    continue
            for bi, (y0, y1) in enumerate(rb):
                obj, ncol = bands[bi]
                pad = 0
                by0, by1 = y0, y1
                band = im.crop((0, by0, im.size[0], by1))
                mb = matte(band, HERE / "work" / ("%s_%s_band%d_%d-%d.png" % (sid, v, bi, by0, by1)))
                a = np.asarray(mb)[..., 3] > 128
                cr = widen(runs(a.sum(0).astype(np.float32), 0.06,
                                im.size[0] // (ncol * 4)), 0, im.size[0])
                print("   band %d (%s, y %d-%d) alpha %.3f  columns: %s"
                      % (bi, obj, by0, by1, a.mean(), cr))
                if len(cr) != ncol:
                    print("   HALT: %d columns found, %d expected" % (len(cr), ncol))
                    continue
                names = VIEWS[:2] if sid == "T10P-D" and bi == 0 else (
                    VIEWS[2:] if sid == "T10P-D" else VIEWS)
                for ci, (x0, x1) in enumerate(cr):
                    cell = mb.crop((max(0, x0 - pad), 0, min(mb.size[0], x1 + pad), mb.size[1]))
                    ca = np.asarray(cell)[..., 3] > 128
                    ys, xs = np.nonzero(ca)
                    touch = (ys.min() == 0 or ys.max() == cell.size[1] - 1
                             or xs.min() == 0 or xs.max() == cell.size[0] - 1)
                    cell.save(HERE / "cells" / ("%s_%s_%s.png" % (obj, v, names[ci])))
                    out.setdefault(obj, {}).setdefault(v, {})[names[ci]] = {
                        "bbox": [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)],
                        "cell": list(cell.size), "touches_edge": bool(touch)}
                    if touch:
                        print("      WARN %s %s %s touches a cell edge" % (obj, v, names[ci]))
    (HERE / "cells.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
