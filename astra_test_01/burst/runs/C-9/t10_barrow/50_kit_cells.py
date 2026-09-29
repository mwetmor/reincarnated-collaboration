#!/usr/bin/env python3
"""C-9 T10-1b: cut the three scatter-kit sheets into cells and matte each band.

Same method as 31_cells.py -- bands and columns found FROM the sheet's own detail profile,
each band matted on its own so BiRefNet sees one kind of object at a time -- with two
changes the kit sheets need:

  * THE COLUMNS ARE NOT EVEN. T10K-B's log is drawn side-on in FRONT/BACK and END-ON in
    RIGHT/LEFT, so two of its four columns are a fifth the width of the other two. An even
    quarter-split would cut both long views in half. The run detector already handles this;
    what had to change is `min_len`, which at W/(ncol*4) = 96 px is close enough to the
    end-on disc's own width to be worth stating rather than discovering.
  * NO GREEN PLATE. Most of these sheets lost the plate to a dark vignette. That is not a
    defect to repair before matting -- BiRefNet is what removes the background either way,
    and a vignette is a smooth gradient, which is exactly what the detail profile ignores.

The edge-touch check from T9 is kept. It is the cheap test that says a crop went wrong
from the inside, and it is the one nothing checked for the time it mattered.
"""
import json
import pathlib
import subprocess

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts"
WORK = HERE / "kit_work"
VIEWS = ["front", "right", "back", "left"]
REFINE = {"T10K-C"}   # rows 13 px apart; see the margin refine below
MARGIN = 60

# sheet -> [(object, n columns)] per band, top band first
SHEETS = {
    "T10K-A": [("rocks", 4), ("stump", 4)],
    "T10K-B": [("log", 4), ("cairn", 4)],
    "T10K-C": [("skull", 4), ("shield", 4)],
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
    out = []
    for i, (a, b) in enumerate(rs):
        na = lo if i == 0 else (rs[i - 1][1] + a) // 2
        nb = hi if i == len(rs) - 1 else (b + rs[i + 1][0]) // 2
        out.append((na, nb))
    return out


def min_ink_split(prof: np.ndarray, ncol: int) -> tuple:
    """Cut a band into ncol columns at the LEAST-INK column near each nominal boundary.

    The elk-skull row needs this and the other five objects do not: its four views are
    drawn with the antlers of neighbouring views INTERLOCKING, so the alpha profile never
    returns to background between them and the run detector finds two columns where there
    are four. There is no crop that does not sever something; the question is how much, so
    this returns the severed ink with the cuts rather than only the cuts. Reported, not
    hidden -- the tines are the part of this object most likely to be lost, and a cut
    through them is a loss that happens BEFORE the builder ever sees the sheet.
    """
    W = len(prof)
    p = prof / max(prof.max(), 1e-9)
    cuts, cost = [], []
    for k in range(1, ncol):
        c = int(round(W * k / ncol))
        lo, hi = max(1, c - W // 8), min(W - 1, c + W // 8)
        x = lo + int(np.argmin(p[lo:hi]))
        cuts.append(x)
        cost.append(round(float(p[x]), 4))
    bounds = [(a, b) for a, b in zip([0] + cuts, cuts + [W])]
    return bounds, cuts, cost


def drop_slivers(cell: Image.Image, frac: float = 0.05):
    """Remove the OTHER view's severed antler tip from this view's cell.

    A min-ink cut through interlocked antlers leaves a fragment of the neighbour on this
    side of the line -- 759 px of tine floating at the left edge of the skull's LEFT view.
    It is small, it touches the cut, and it belongs to a different view; feeding it to a
    multiview build asks the builder to reconcile a spur that is not on the object.

    The rule is deliberately narrow: drop a component only if it TOUCHES A CUT EDGE (left
    or right) AND is under `frac` of the largest component. The elk's three ribs are the
    reason for the second half -- they are genuinely detached, 3.8k to 7.1k px, and a
    plain 'keep the biggest component' would have thrown all three away.
    """
    a = np.asarray(cell)
    m = a[..., 3] > 128
    lab, n = ndimage.label(m)
    if n < 2:
        return cell, []
    sizes = ndimage.sum(m, lab, range(1, n + 1)).astype(int)
    big = sizes.max()
    out, dropped = a.copy(), []
    for i in range(1, n + 1):
        c = lab == i
        cols = np.nonzero(c.any(0))[0]
        if sizes[i - 1] < frac * big and (cols.min() == 0 or cols.max() == m.shape[1] - 1):
            out[c] = 0
            dropped.append(int(sizes[i - 1]))
    return Image.fromarray(out), dropped


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
    WORK.mkdir(exist_ok=True)
    (WORK / "cells").mkdir(exist_ok=True)
    out = {}
    for sid, bands in SHEETS.items():
        for v in ("a", "b"):
            src = ART / sid / ("%s_%s.png" % (sid, v))
            if not src.exists():
                print("%s_%s MISSING" % (sid, v))
                continue
            im = Image.open(src).convert("RGB")
            d = detail(np.asarray(im))
            rb = widen(runs(d.sum(1), 0.10, im.size[1] // 12), 0, im.size[1])
            print("%s_%s  %s  bands: %s (expected %d)" % (sid, v, im.size, rb, len(bands)))
            if len(rb) != len(bands):
                if len(rb) == 1 and len(bands) == 2:
                    prof = d.sum(1) / max(d.sum(1).max(), 1e-9)
                    w0, w1 = int(im.size[1] * 0.40), int(im.size[1] * 0.60)
                    cut = w0 + int(np.argmin(prof[w0:w1]))
                    print("   rows touch; quietest row %d (detail %.3f; midpoint %.3f)"
                          % (cut, prof[cut], prof[im.size[1] // 2]))
                    rb = [(0, cut), (cut, im.size[1])]
                else:
                    print("   HALT: band count disagrees with the layout asked for")
                    continue
            for bi, (y0, y1) in enumerate(rb):
                obj, ncol = bands[bi]
                H = im.size[1]
                if sid in REFINE:
                    # THE ROWS ON T10K-C ARE 13 PIXELS APART. The detail profile put the
                    # boundary 19 px INSIDE the spearheads, and the edge-touch check caught
                    # it: all four shield views reported ink on their top row. The detail
                    # profile cannot do better -- a spear tip is thin and pale and its
                    # detail falls under the threshold before the paint does. So matte a
                    # band with MARGIN to spare at each end and put the real boundary at
                    # the quietest row of the ALPHA, which is the thing that knows where
                    # the object actually stops.
                    e0, e1 = max(0, y0 - MARGIN), min(H, y1 + MARGIN)
                    mb = matte(im.crop((0, e0, im.size[0], e1)),
                               WORK / ("%s_%s_band%d_%d-%d_m.png" % (sid, v, bi, e0, e1)))
                    ap = (np.asarray(mb)[..., 3] > 128).sum(1).astype(np.float32)
                    t = 0 if e0 == 0 else int(np.argmin(ap[:MARGIN + 24]))
                    b = len(ap) if e1 == H else (
                        len(ap) - MARGIN - 24 + int(np.argmin(ap[len(ap) - MARGIN - 24:])))
                    print("   band %d margin refine: %d-%d -> %d-%d (alpha rows %d / %d)"
                          % (bi, y0, y1, e0 + t, e0 + b, ap[t], ap[min(b, len(ap) - 1)]))
                    y0, y1 = e0 + t, e0 + b
                    mb = mb.crop((0, t, mb.size[0], b))
                else:
                    mb = matte(im.crop((0, y0, im.size[0], y1)),
                               WORK / ("%s_%s_band%d_%d-%d.png" % (sid, v, bi, y0, y1)))
                a = np.asarray(mb)[..., 3] > 128
                colprof = a.sum(0).astype(np.float32)
                cr = widen(runs(colprof, 0.06, im.size[0] // (ncol * 4)), 0, im.size[0])
                print("   band %d (%s, y %d-%d) alpha %.3f  columns: %s"
                      % (bi, obj, y0, y1, a.mean(), cr))
                sever = None
                if len(cr) != ncol:
                    cr, cuts, sever = min_ink_split(colprof, ncol)
                    px = [int(colprof[c]) for c in cuts]
                    print("   views overlap; min-ink split at %s -> %s  severed ink "
                          "%s of peak (%s px)" % (cuts, cr, sever, px))
                for ci, (x0, x1) in enumerate(cr):
                    cell = mb.crop((x0, 0, x1, mb.size[1]))
                    cell, dropped = drop_slivers(cell)
                    if dropped:
                        print("      %s %s %s: dropped %d severed sliver(s) %s px"
                              % (obj, v, VIEWS[ci], len(dropped), dropped))
                    ca = np.asarray(cell)[..., 3] > 128
                    ys, xs = np.nonzero(ca)
                    ed = [e for e, t in (("top", ys.min() == 0),
                                         ("bottom", ys.max() == cell.size[1] - 1),
                                         ("left", xs.min() == 0),
                                         ("right", xs.max() == cell.size[0] - 1)) if t]
                    cell.save(WORK / "cells" / ("%s_%s_%s.png" % (obj, v, VIEWS[ci])))
                    out.setdefault(obj, {}).setdefault(v, {})[VIEWS[ci]] = {
                        "sheet": sid,
                        "bbox": [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)],
                        "cell": list(cell.size), "band_y": [int(y0), int(y1)],
                        "touches_edge": bool(ed), "edges": ed,
                        "severed_ink_frac_of_peak": sever}
                    if ed:
                        n = [int(ca[0].sum()), int(ca[-1].sum()),
                             int(ca[:, 0].sum()), int(ca[:, -1].sum())]
                        print("      WARN %s %s %s touches %s (px on t/b/l/r: %s)"
                              % (obj, v, VIEWS[ci], ",".join(ed), n))
    (WORK / "cells.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
