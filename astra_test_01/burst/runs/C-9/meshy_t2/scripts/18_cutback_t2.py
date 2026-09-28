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
"""
import argparse, importlib.util, json, os, sys
import numpy as np
from PIL import Image

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

    argv = [T1_CUTBACK, args.sheet, args.layout, args.dest]
    if args.report:
        argv += ["--report", args.report]
    old = sys.argv
    sys.argv = argv
    try:
        mod.main()
    finally:
        sys.argv = old


if __name__ == "__main__":
    main()
