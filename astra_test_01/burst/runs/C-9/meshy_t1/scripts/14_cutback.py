#!/usr/bin/env python3
"""C-9 meshy_t1: cut a painted Astra sheet back to game frames, with a matte
that does not depend on the plate surviving.

    python3 scripts/14_cutback.py <sheet.png> <layout.json> <dest_root> [--report x.json]

Astra loses the #00ff00 plate on roughly half the walk sheets -- the T1K-walk
pair came back as a dark gradient with light columns -- while the PAINTING is
good. Re-firing for a background is waste, so the matte is built the other way
round:

  GEOMETRY FIRST. The alpha starts as the render's own mask for that exact
  frame, which is exact by construction, dilated by the measured ink width so
  the painted contour is inside it. Nothing about the background can move this
  boundary.

  BACKGROUND MODEL SECOND. Everything outside the dilated masks is known
  background, whatever colour it is; a push-pull fill interpolates it under the
  figures, so a gradient, a colour wash or a flat plate are all handled the
  same way. Only the OUTER part of the ink band is then trimmed against that
  model.

Why not key the colour and be done: on this sheet the ink line is dark sepia
and the lost background is dark brown. They are the same colour. A colour key
cannot separate them; the geometry can, and the ink band is bounded by a
measured width rather than guessed.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
T1 = os.path.dirname(HERE)
OUT = os.path.join(T1, "out")
INK_PX_PER_1000H = 5.59          # measured on the approved stills (R-C9-60)


def render_mask(state, d, i):
    p = os.path.join(OUT, state, "guides_part", d, "part_%s_%02d.png" % (d, i))
    return np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 8


def pushpull(img, known, iters=28):
    """Interpolate the background under the figures from what is known."""
    small = 8
    h, w = known.shape
    a = img.astype(np.float64).copy()
    k = known.astype(np.float64)
    a[~known] = 0.0
    A = a[::small, ::small].copy()
    K = k[::small, ::small].copy()
    for _ in range(iters):
        An = ndi.uniform_filter(A, size=5, axes=(0, 1))
        Kn = ndi.uniform_filter(K, size=5)
        fill = Kn > 1e-6
        A = np.where(K[..., None] > 0.5, A, np.where(fill[..., None],
                                                     An / np.maximum(Kn, 1e-6)[..., None], A))
        K = np.maximum(K, (Kn > 1e-6).astype(np.float64))
    B = np.stack([ndi.zoom(A[..., c], (h / A.shape[0], w / A.shape[1]), order=1)
                  for c in range(3)], -1)
    return B[:h, :w]


def main():
    sheet_p, layout_p, dest = sys.argv[1], sys.argv[2], sys.argv[3]
    repp = sys.argv[sys.argv.index("--report") + 1] if "--report" in sys.argv else None
    sheet = np.asarray(Image.open(sheet_p).convert("RGB")).astype(np.float64)
    lay = json.load(open(layout_p))
    H, W = sheet.shape[:2]
    if [W, H] != lay.get("sheet_px", [W, H]):
        sheet = np.asarray(Image.open(sheet_p).convert("RGB")
                           .resize(tuple(lay["sheet_px"]), Image.LANCZOS)).astype(np.float64)
        H, W = sheet.shape[:2]

    # ---- per-cell render masks, mapped into sheet space -------------------
    cells = []
    for c in lay["cells"]:
        m = render_mask(c["state"], c["dir"], c["frame"])
        x, y, cw, ch = c["crop"]
        sub = Image.fromarray((m[y:y + ch, x:x + cw] * 255).astype(np.uint8))
        sub = np.asarray(sub.resize((c["w"], c["h"]), Image.NEAREST)) > 127
        cells.append((c, sub))

    ink = max(2, int(round(INK_PX_PER_1000H / 1000.0 * 199 * lay["cells"][0]["scale"])))
    sheet_mask = np.zeros((H, W), bool)
    for c, sub in cells:
        sheet_mask[c["y"]:c["y"] + c["h"], c["x"]:c["x"] + c["w"]] |= sub
    grown = ndi.binary_dilation(sheet_mask, np.ones((2 * ink + 1,) * 2))
    known = ~ndi.binary_dilation(grown, np.ones((9, 9)))
    B = pushpull(sheet, known)
    # The background model is only TRUSTWORTHY near real background pixels.
    # Under a figure it is an interpolation, and a dark knight over a dark
    # gradient matches it by coincidence -- classifying there measured "is the
    # armour the same colour as the guess behind it" and reported 22/255 of
    # residual background on a matte that was actually clean.
    reliable = ndi.binary_dilation(known, np.ones((2 * (3 * ink) + 1,) * 2))

    # ---- per cell: geometry mask + ink band, outer band trimmed by B ------
    rep = dict(sheet=os.path.basename(sheet_p), ink_px=ink,
               background_is_plate=bool(np.abs(B[known] - np.array([0, 255, 0])).mean() < 40)
               if known.any() else None,
               cells=[])
    for c, sub in cells:
        x0, y0, cw, ch = c["x"], c["y"], c["w"], c["h"]
        px = sheet[y0:y0 + ch, x0:x0 + cw]
        bg = B[y0:y0 + ch, x0:x0 + cw]
        rel = reliable[y0:y0 + ch, x0:x0 + cw]
        core = sub
        outer = ndi.binary_dilation(core, np.ones((2 * ink + 1,) * 2))
        band = outer & ~core
        dist = np.abs(px - bg).mean(-1)
        # add ink-band pixels that differ from the background, and drop core
        # pixels that match it -- but only where the model can be trusted, so
        # the figure's interior is never second-guessed
        keep_band = band & (dist > 14.0)
        drop_core = core & rel & (dist < 10.0)
        alpha = (core & ~drop_core) | keep_band
        alpha = ndi.binary_fill_holes(alpha)
        lab, n = ndi.label(alpha)
        if n > 1:
            sz = np.array(ndi.sum(alpha, lab, range(1, n + 1)))
            alpha = lab == (1 + int(np.argmax(sz)))
        # ---- asserts ------------------------------------------------------
        bg_like = (dist < 10.0) & alpha & rel
        resid = 255.0 * float(bg_like.sum()) / max(int(alpha.sum()), 1)
        lum = px @ np.array([0.299, 0.587, 0.114])
        rim = alpha & ~ndi.binary_erosion(alpha, np.ones((2 * ink + 1,) * 2))
        inkpx = int(((lum < 110) & rim).sum())
        rim_all = int(rim.sum())
        # write the frame back into a 512 game frame at the recorded crop
        fr = np.zeros((lay["game_frame_px"], lay["game_frame_px"], 4), np.uint8)
        rgba = np.dstack([px.astype(np.uint8), (alpha * 255).astype(np.uint8)])
        im = Image.fromarray(rgba).resize((c["crop"][2], c["crop"][3]), Image.LANCZOS)
        arr = np.asarray(im)
        fr[c["crop"][1]:c["crop"][1] + c["crop"][3],
           c["crop"][0]:c["crop"][0] + c["crop"][2]] = arr
        dd = os.path.join(dest, c["state"], c["dir"])
        os.makedirs(dd, exist_ok=True)
        Image.fromarray(fr).save(os.path.join(
            dd, "%s_%s_%02d.png" % (c["state"], c["dir"], c["frame"])))
        rep["cells"].append(dict(state=c["state"], dir=c["dir"], frame=c["frame"],
                                 residual_bg_per255=round(resid, 3),
                                 ink_rim_px=inkpx, rim_px=rim_all,
                                 ink_rim_frac=round(inkpx / max(rim_all, 1), 3),
                                 alpha_px=int(alpha.sum())))
    r = [c["residual_bg_per255"] for c in rep["cells"]]
    k = [c["ink_rim_frac"] for c in rep["cells"]]
    rep["residual_bg_mean_per255"] = round(float(np.mean(r)), 3)
    rep["residual_bg_max_per255"] = round(float(np.max(r)), 3)
    rep["ink_rim_frac_mean"] = round(float(np.mean(k)), 3)
    rep["assert_residual_under_3"] = bool(np.mean(r) < 3.0)
    print("  %s: residual background %.2f/255 mean, %.2f max  (assert <3: %s); "
          "ink kept on %.0f %% of the rim; background %s"
          % (os.path.basename(sheet_p), rep["residual_bg_mean_per255"],
             rep["residual_bg_max_per255"], rep["assert_residual_under_3"],
             100 * rep["ink_rim_frac_mean"],
             "plate" if rep["background_is_plate"] else "NOT plate"))
    if repp:
        json.dump(rep, open(repp, "w"), indent=1)


if __name__ == "__main__":
    main()
