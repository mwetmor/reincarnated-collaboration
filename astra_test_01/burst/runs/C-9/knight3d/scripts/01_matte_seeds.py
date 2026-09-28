#!/usr/bin/env python3
"""C-9 knight3d step 1: matte the eight approved knight stills off the green plate,
split the pollaxe from the body, and write masks + measurements.

Inputs  : runs/C-9/artifacts/seeds/seed_{N,NE,E,SE,S_v2,SW_v2,W,NW}.png  (the
          exact current files named by artifacts/knight_cells_manifest.json)
Outputs : knight3d/work/masks/<D>_full.npy   bool, figure+pollaxe
          knight3d/work/masks/<D>_body.npy   bool, figure only
          knight3d/work/masks/<D>_axe.npy    bool, pollaxe only
          knight3d/work/seed_measurements.json

Method (measure, don't assume):
  - plate key: the register card says figures sit on flat #00ff00. Key by
    (G high) AND (G - max(R,B) high), then close small holes.
  - pollaxe split: the haft is a long near-vertical bar of near-constant width
    and the head is at the top of it. We find it as the connected component of
    the "thin vertical" opening that reaches both far above the crown and far
    below the body's own mass, then re-attach the axe head by dilating from the
    haft top.  The grip region (where the hand overlaps the haft) is resolved
    by *excluding* a dilation band around the split from BOTH masks at scoring
    time -- it is never assigned to one side by guesswork.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
SEEDS = os.path.join(ROOT, "artifacts", "seeds")
WORK = os.path.join(ROOT, "knight3d", "work")
MASKS = os.path.join(WORK, "masks")
os.makedirs(MASKS, exist_ok=True)

# direction -> exact current seed file (S and SW are the v2 files, per manifest)
SEED_FILE = {
    "N": "seed_N.png", "NE": "seed_NE.png", "E": "seed_E.png", "SE": "seed_SE.png",
    "S": "seed_S_v2.png", "SW": "seed_SW_v2.png", "W": "seed_W.png", "NW": "seed_NW.png",
}
DIRS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def key_plate(rgb):
    r = rgb[..., 0].astype(np.int16)
    g = rgb[..., 1].astype(np.int16)
    b = rgb[..., 2].astype(np.int16)
    # green screen: green dominant and bright
    dom = g - np.maximum(r, b)
    plate = (dom > 60) & (g > 110)
    fig = ~plate
    # clean: remove specks, fill interior holes, keep largest component
    fig = ndi.binary_opening(fig, np.ones((3, 3)))
    lab, n = ndi.label(fig)
    if n:
        sizes = ndi.sum(fig, lab, range(1, n + 1))
        keep = (np.arange(1, n + 1))[sizes > 0.01 * sizes.max()]
        fig = np.isin(lab, keep)
    fig = ndi.binary_fill_holes(fig)
    return fig


def split_axe(full):
    """Return (body, axe, ambiguous).

    The haft is the tallest THIN near-vertical structure. Cutting it out
    disconnects the axe head (and butt cap) from the figure, so after the cut
    the largest component is the body and every other component that touches
    the haft is pollaxe. Where the gripping hand overlaps the haft the cut
    takes a notch out of the hand; that band is returned as `ambiguous` and is
    excluded from BOTH masks at scoring time rather than guessed at.
    """
    h, w = full.shape
    wide = ndi.binary_opening(full, np.ones((1, 55)))   # survives only >=55px-wide runs
    thin = full & ~wide

    lab, n = ndi.label(thin, structure=np.ones((3, 3)))
    best, best_h = 0, 0
    for i in range(1, n + 1):
        ys, _ = np.where(lab == i)
        ext = ys.max() - ys.min()
        if ext > best_h:
            best_h, best = ext, i
    haft = (lab == best)

    # The grip splits the haft into several thin components (and in the profile
    # views the tallest is only the length BELOW the hand). Fit the haft's line
    # from the tallest piece, then absorb every other thin piece that sits on
    # that same line, and refit.
    def line_of(mask):
        ys, xs = np.where(mask)
        A = np.vstack([ys, np.ones_like(ys)]).T.astype(float)
        m, c = np.linalg.lstsq(A, xs.astype(float), rcond=None)[0]
        return m, c

    m, c = line_of(haft)
    med_w = float(np.median([np.count_nonzero(haft[y]) for y in
                             np.where(haft.any(axis=1))[0]]))
    for _ in range(2):
        for i in range(1, n + 1):
            if (lab == i).sum() < 30:
                continue
            ys, xs = np.where(lab == i)
            if np.median(np.abs(xs - (m * ys + c))) < 1.5 * med_w:
                haft |= (lab == i)
        m, c = line_of(haft)

    rows = np.where(haft.any(axis=1))[0]
    hy0, hy1 = int(rows.min()), int(rows.max())
    bar = np.zeros_like(full)
    for y in range(hy0, hy1 + 1):
        cc = m * y + c
        a = int(round(cc - med_w / 2.0)); b = int(round(cc + med_w / 2.0)) + 1
        bar[y, max(0, a):min(w, b)] = True
    haft = bar & full

    rest = full & ~ndi.binary_dilation(haft, np.ones((3, 3)))
    lab, n = ndi.label(rest, structure=np.ones((3, 3)))
    sizes = np.array(ndi.sum(rest, lab, range(1, n + 1))) if n else np.array([])
    body_id = 1 + int(np.argmax(sizes)) if n else 0
    body = (lab == body_id)
    axe = haft.copy()
    ambiguous = np.zeros_like(full)
    haft_near = ndi.binary_dilation(haft, np.ones((7, 7)))
    for i in range(1, n + 1):
        if i == body_id:
            continue
        comp = (lab == i)
        if (comp & haft_near).any() and comp.sum() > 40:
            axe |= comp                          # axe head, langets, butt cap
        else:
            ambiguous |= comp                    # crumbs from the cut
    # the grip: rows where the haft cut removed pixels that were interior to a
    # wide run (i.e. the hand) -- flag a band there, do not assign it.
    grip = haft & ndi.binary_dilation(body, np.ones((1, 9))) & \
        ndi.binary_dilation(body, np.ones((9, 1)))
    ambiguous |= ndi.binary_dilation(grip, np.ones((9, 9))) & full
    body = ndi.binary_fill_holes(body)
    return body, axe, ambiguous


def profile(mask):
    rows = np.where(mask.any(axis=1))[0]
    out = {}
    if not len(rows):
        return out
    y0, y1 = int(rows.min()), int(rows.max())
    xs_min, xs_max = [], []
    for y in range(y0, y1 + 1):
        xs = np.where(mask[y])[0]
        xs_min.append(int(xs.min())); xs_max.append(int(xs.max()))
    out["y_top"] = y0
    out["y_bottom"] = y1
    out["height"] = y1 - y0 + 1
    out["x_min"] = int(min(xs_min)); out["x_max"] = int(max(xs_max))
    out["width"] = out["x_max"] - out["x_min"] + 1
    out["area_px"] = int(mask.sum())
    out["cx"] = float(np.where(mask)[1].mean())
    # widths at fractional heights, as a shape fingerprint
    fr = {}
    for f in (0.02, 0.06, 0.10, 0.14, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.98):
        y = int(round(y0 + f * (y1 - y0)))
        xs = np.where(mask[y])[0]
        fr["%.2f" % f] = [int(xs.min()), int(xs.max()), int(xs.max() - xs.min() + 1)] if len(xs) else None
    out["width_at_height_frac"] = fr
    return out


def main():
    meas = {"note": "C-9 knight3d: mattes + measurements of the eight approved stills.",
            "seed_files": SEED_FILE, "views": {}}
    for d in DIRS:
        p = os.path.join(SEEDS, SEED_FILE[d])
        rgb = np.asarray(Image.open(p).convert("RGB"))
        full = key_plate(rgb)
        body, axe, amb = split_axe(full)
        np.save(os.path.join(MASKS, "%s_full.npy" % d), full)
        np.save(os.path.join(MASKS, "%s_body.npy" % d), body)
        np.save(os.path.join(MASKS, "%s_axe.npy" % d), axe)
        np.save(os.path.join(MASKS, "%s_amb.npy" % d), amb)
        meas["views"][d] = {
            "file": SEED_FILE[d],
            "image_size": [int(rgb.shape[1]), int(rgb.shape[0])],
            "full": profile(full),
            "body": profile(body),
            "axe": profile(axe),
            "ambiguous_px": int(amb.sum()),
        }
        print(d, "full h=%d" % meas["views"][d]["full"]["height"],
              "body h=%d w=%d area=%d" % (meas["views"][d]["body"]["height"],
                                          meas["views"][d]["body"]["width"],
                                          meas["views"][d]["body"]["area_px"]))
    with open(os.path.join(WORK, "seed_measurements.json"), "w") as f:
        json.dump(meas, f, indent=1)
    print("wrote", os.path.join(WORK, "seed_measurements.json"))


if __name__ == "__main__":
    main()
