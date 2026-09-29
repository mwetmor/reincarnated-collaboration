#!/usr/bin/env python3
"""C-9 meshy_t2 step 11a: run meshy_t1's robust matte on T2 sheets.

    python3 scripts/18_cutback_t2.py <sheet.png> <layout.json> <dest_root>
                                     [--report x.json]

This is an ADAPTER, not a second matte. The T1 session's
meshy_t1/scripts/14_cutback.py already does the hard part -- alpha from the
render's own mask, dilated by the measured ink width, with everything outside
the dilated figures push-pull-filled into a background model so a lost green
plate, a dark gradient or a colour wash are all handled the same way. It is
loaded here by path and called; none of its logic is copied.

Exactly two things in it are the KNIGHT's rather than the pipeline's, and both
are module constants, so both are overridden from the outside:

  OUT               it derives the render root from its own location, which
                    would send it looking for the manticore's masks inside
                    meshy_t1/out/. Repointed at meshy_t2/out/.

  ink width         it computes the ink band as
                    INK_PX_PER_1000H / 1000 * 199 * scale, where 199 px is the
                    KNIGHT's rendered helm-to-sole. The manticore shares the
                    world's px/m and is therefore a different number of pixels
                    tall -- measured off its own render masks, not assumed --
                    so INK_PX_PER_1000H is pre-scaled by (t2_height / 199) and
                    their formula comes out right without being touched.

Everything else lines up because the T2 layout schema was written to be
identical to T1's: same sheet and cell geometry, same per-cell
`crop = [x, y, w, h]` / `scale` / `state` / `dir` / `frame`, same
`game_frame_px`.

TWO CORRECTIONS are applied around their call, both reported upstream rather
than forked.

1. A QUADRUPED HAS A HOLE A BIPED DOES NOT. Their matte finishes with
   `binary_fill_holes`, which on the knight closes the odd gap between a limb
   and the tabard. On a hound standing side-on it welds the gap BETWEEN THE
   LEGS shut, and fills it with whatever the background was -- a solid green
   wedge in the middle of the animal, about 10 px across at game scale, on
   run E frames 0/4/6 and run SE frame 0. It is what drove their own residual
   assert to 3.54/255 on run SE (their assert is <3, so the script did say so;
   the number was right and the cause was not obvious from it). Corrected
   afterwards, on the written frames, using the one thing that knows where the
   holes are: the RENDER MASK. Its own enclosed holes, eroded by the ink band
   so the painted contour on both sides survives, are punched back out.
   Worth passing to the T1 session: any view where the knight's arm clears his
   torso has the same shape of hole.

2. One thing does NOT line up, and it is T2's fault rather than theirs: the run
is 8 frames on a 12-cell plate, so four cells are blank and my layout writes
them with `frame: null`. Their cutback walks every cell in the layout and
formats the frame number straight into a path, so a null frame raises
TypeError before it reads a pixel. Blank cells are filtered out here into a
temporary layout rather than fixed in their code or in layouts that have
already been painted against. Worth passing to the T1 session: any clip whose
frame count is not a multiple of 12 will do the same to them.
"""
import argparse, importlib.util, json, os, sys, tempfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
T1_CUTBACK = os.path.join(os.path.dirname(ROOT), "meshy_t1", "scripts", "14_cutback.py")
KNIGHT_BODY_PX = 199.0            # the constant baked into their ink formula


def measured_body_px():
    """The manticore's rendered height, from its own masks rather than from
    the 1.2021 m model height times px/m -- the render is the thing the ink
    width has to match."""
    best = 0
    for clip in ("idle", "walk"):
        for d in ("E", "SE"):
            p = os.path.join(OUT, clip, "guides_mask", d, "mask_%s_00.png" % d)
            if not os.path.exists(p):
                continue
            a = np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128
            ys = np.where(a.any(axis=1))[0]
            if len(ys):
                best = max(best, int(ys.max() - ys.min() + 1))
    return float(best or 132)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("layout")
    ap.add_argument("dest")
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    if not os.path.exists(T1_CUTBACK):
        raise SystemExit("meshy_t1/scripts/14_cutback.py not present; "
                         "the robust matte is the T1 session's to land")
    spec = importlib.util.spec_from_file_location("t1_cutback", T1_CUTBACK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    body = measured_body_px()
    mod.OUT = OUT
    orig_ink = mod.INK_PX_PER_1000H
    mod.INK_PX_PER_1000H = orig_ink * body / KNIGHT_BODY_PX
    print("adapter: OUT -> %s ; body %.0f px (knight %.0f) ; "
          "INK_PX_PER_1000H %.3f -> %.3f"
          % (os.path.relpath(OUT, ROOT), body, KNIGHT_BODY_PX,
             orig_ink, mod.INK_PX_PER_1000H))

    lay = json.load(open(args.layout))
    live = [c for c in lay["cells"] if c.get("frame") is not None and c.get("source")]
    layout_path = args.layout
    tmp = None
    if len(live) != len(lay["cells"]):
        lay["cells"] = live
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(lay, tmp); tmp.close()
        layout_path = tmp.name
        print("adapter: %d of %d cells are blank (short clip on a 12-cell plate); "
              "filtered" % (len(lay["cells"]) - len(live) + (len(lay["cells"]) - len(live)) * 0
                            if False else 12 - len(live), 12))

    argv = [T1_CUTBACK, args.sheet, layout_path, args.dest]
    if args.report:
        argv += ["--report", args.report]
    old = sys.argv
    sys.argv = argv
    try:
        mod.main()
    finally:
        sys.argv = old
        if tmp is not None:
            os.unlink(tmp.name)

    ink = max(2, int(round(mod.INK_PX_PER_1000H / 1000.0 * KNIGHT_BODY_PX
                           * live[0]["scale"])))
    repunch(live, args.dest, ink)


def repunch(cells, dest, ink_sheet_px):
    """Punch the render mask's own enclosed holes back out of the alpha."""
    fixed = 0; px = 0
    for c in cells:
        p = os.path.join(dest, c["state"], c["dir"],
                         "%s_%s_%02d.png" % (c["state"], c["dir"], c["frame"]))
        if not os.path.exists(p):
            continue
        mp = os.path.join(OUT, c["state"], "guides_mask", c["dir"],
                          "mask_%s_%02d.png" % (c["dir"], c["frame"]))
        if not os.path.exists(mp):
            continue
        m = np.asarray(Image.open(mp).convert("RGBA"))[..., 3] > 128
        holes = ndi.binary_fill_holes(m) & ~m
        if not holes.any():
            continue
        # keep the ink band on BOTH sides of the gap: erode the hole by the
        # same width the matte grew the figure by, in FRAME pixels
        ink_frame = max(1, int(round(ink_sheet_px / max(c["scale"], 1e-6))))
        holes = ndi.binary_erosion(holes, np.ones((2 * ink_frame + 1,) * 2))
        if not holes.any():
            continue
        im = Image.open(p).convert("RGBA")
        arr = np.array(im)
        hit = holes & (arr[..., 3] > 0)
        if not hit.any():
            continue
        arr[..., 3][holes] = 0
        Image.fromarray(arr, "RGBA").save(p)
        fixed += 1; px += int(hit.sum())
    if fixed:
        print("adapter: re-punched render-mask holes in %d of %d cells "
              "(%d px of welded background removed)" % (fixed, len(cells), px))


if __name__ == "__main__":
    main()
