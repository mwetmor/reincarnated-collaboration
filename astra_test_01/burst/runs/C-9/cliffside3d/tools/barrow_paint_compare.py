#!/usr/bin/env python3
"""C-9 T10-1b -- THE RENDER AGAINST THE PAINTING, measured.

    python3 barrow_paint_compare.py --cap CAPTURE_DIR --seg SEG_DIR

Inputs: the concept painting, its class map (barrow_paint_dress.py), and two frames from the
capture taken at the painting's OWN framing -- the beauty render and the class-ID render
(every prop in its class colour, unshaded, on black, MSAA off).

Outputs:
  paint_vs_render_side_by_side.png   the painting and the render, side by side
  paint_vs_render_overlay50.png      the render at 50% over the painting
  paint_coverage.json                per class: COVERAGE = the share of the painting's pixels
                                     of that class that a 3D object of THE SAME class covers
                                     in the render, which is the acceptance for "placed as
                                     painted"; plus PRECISION (the share of the render's class
                                     pixels that land on painted pixels of that class) so a
                                     class cannot pass by flooding the frame.

The instrument is checked on a known case first: the painting's class map compared against
ITSELF must give coverage 1.0 and precision 1.0 in every class, and against an all-black
render 0.0 -- or the numbers below are about the comparison code, not the scene.
"""
import argparse
import json
import pathlib

import numpy as np
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent.parent / "artifacts" / "T10C-barrow" / "T10C-barrow_a.png"
NAMES = {1: "stone", 2: "rock", 3: "shrub", 4: "tree"}
# the ID pass's colours (barrow_world.ID_COLOURS): stone red, rock green, shrub blue, tree yellow
ID_RGB = {1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255), 4: (255, 255, 0)}
# T10-1c: heather has its own ID colour so its rendered colour can be sampled apart from the
# junipers'; for COVERAGE it is shrub, like juniper
HEATHER_ID = 5
HEATHER_RGB = (255, 0, 255)


def srgb_to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def rust_r(L):
    return (L[..., 1] > 5) & (L[..., 2] > 13)


def classify_ids(img):
    """Nearest ID colour, with black as 'nothing' and a distance ceiling so a stray grey pixel
    is not forced into a class."""
    a = img.astype(np.int32)
    out = np.zeros(a.shape[:2], np.uint8)
    best = np.full(a.shape[:2], 1 << 30, np.int64)
    for cid, col in list(ID_RGB.items()) + [(HEATHER_ID, HEATHER_RGB), (0, (0, 0, 0))]:
        d = ((a - np.array(col)) ** 2).sum(-1)
        m = d < best
        best[m] = d[m]
        out[m] = cid
    out[best > 90 ** 2] = 0
    return out


def coverage(paint, render):
    rows = {}
    for cid, nm in NAMES.items():
        p = paint == cid
        r = render == cid
        both = (p & r).sum()
        rows[nm] = {"painting_px": int(p.sum()), "render_px": int(r.sum()),
                    "coverage": round(float(both) / max(int(p.sum()), 1), 4),
                    "precision": round(float(both) / max(int(r.sum()), 1), 4)}
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", required=True)
    ap.add_argument("--seg", required=True)
    ap.add_argument("--before", default="",
                    help="an earlier capture dir: adds warmth_before_after.png, painting | before | this")
    # NOT `a`: the warmth loop below reuses `a` for a Lab mean, and a flag read after it would
    # be read off a numpy array (it was, once: AttributeError on --before)
    args = ap.parse_args()
    a = args
    cap = pathlib.Path(a.cap)
    seg = pathlib.Path(a.seg)
    paint_rgb = np.asarray(Image.open(ART).convert("RGB"))
    paint_cls = np.asarray(Image.open(seg / "paint_classes.png"))
    beauty = np.asarray(Image.open(cap / "barrow_painting_frame.png").convert("RGB"))
    ids = np.asarray(Image.open(cap / "barrow_painting_ids.png").convert("RGB"))
    if beauty.shape[:2] != paint_rgb.shape[:2] or ids.shape[:2] != paint_rgb.shape[:2]:
        raise SystemExit("frame size mismatch: painting %s, render %s, ids %s"
                         % (paint_rgb.shape, beauty.shape, ids.shape))
    rep = {"_defn": {"coverage": "painted pixels of class C covered by a render pixel of class C / painted pixels of class C",
                     "precision": "render pixels of class C on painted pixels of class C / render pixels of class C"}}
    # the instrument, on known cases
    self_cmp = coverage(paint_cls, paint_cls)
    zero_cmp = coverage(paint_cls, np.zeros_like(paint_cls))
    rep["instrument_check"] = {
        "painting_vs_itself_coverage": {k: v["coverage"] for k, v in self_cmp.items()},
        "painting_vs_black_coverage": {k: v["coverage"] for k, v in zero_cmp.items()},
        "_expect": "1.0 in every class against itself, 0.0 against black"}
    rcls_raw = classify_ids(ids)
    rcls = np.where(rcls_raw == HEATHER_ID, 3, rcls_raw)
    rep["classes"] = coverage(paint_cls, rcls)
    # T10-1c: THE VISIBLE PIXELS. The T10-1b ID frame hides the ground, the mound, the snow and
    # him, so a prop's buried base counts as that prop -- fine for "is it placed where the
    # painting has it", wrong for "what colour does it read as", where it samples SNOW at
    # pixels the ID calls heather. The occluded frame draws those four black instead; its
    # classes are what the eye can see. Reported beside the continuity numbers, not instead.
    occ_path = cap / "barrow_painting_ids_occl.png"
    rcls_vis_raw = None
    if occ_path.exists():
        rcls_vis_raw = classify_ids(np.asarray(Image.open(occ_path).convert("RGB")))
        rcls_vis = np.where(rcls_vis_raw == HEATHER_ID, 3, rcls_vis_raw)
        rep["classes_visible"] = coverage(paint_cls, rcls_vis)
        rep["visible_share"] = {nm: round(float((rcls_vis == cid).sum()) / max(int((rcls == cid).sum()), 1), 4)
                                for cid, nm in NAMES.items()}

    # ---- WARMTH: the painting's colours against the render's, same framing -------------
    # Each pair is sampled by the SAME rule on both images, and reported as CIE76 dE:
    #   lit snow  the brightest 30% of low-chroma, non-ice, non-object pixels
    #   heather   painting: shrub pixels that are rust (a* > 5, b* > 13); render: heather's ID
    #   juniper   painting: the rest of the shrub pixels, dark (L < 50); render: juniper's ID
    PL = srgb_to_lab(paint_rgb.astype(np.float64) / 255.0)
    RL = srgb_to_lab(beauty.astype(np.float64) / 255.0)
    CP = np.hypot(PL[..., 1], PL[..., 2])
    CR = np.hypot(RL[..., 1], RL[..., 2])
    ice_p = PL[..., 2] < -6
    ice_r = RL[..., 2] < -6
    ps = (paint_cls == 0) & ~ice_p & (CP < 18)
    rs = (rcls_raw == 0) & ~ice_r & (CR < 30)
    warm = {}
    if ps.any() and rs.any():
        ps &= PL[..., 0] >= np.percentile(PL[..., 0][ps], 70)
        rs &= RL[..., 0] >= np.percentile(RL[..., 0][rs], 70)
    rust = (PL[..., 1] > 5) & (PL[..., 2] > 13)
    rid = rcls_vis_raw if rcls_vis_raw is not None else rcls_raw

    def erode(m):
        # one pixel in from every edge: the interior of a mask, away from the 4x-MSAA blend
        # with whatever is behind it (the ID frame is MSAA off, the beauty is not)
        e = m.copy()
        e[1:, :] &= m[:-1, :]
        e[:-1, :] &= m[1:, :]
        e[:, 1:] &= m[:, :-1]
        e[:, :-1] &= m[:, 1:]
        return e
    pairs = {"lit_snow": (ps, rs),
             "heather": ((paint_cls == 3) & rust, rid == HEATHER_ID),
             "juniper": ((paint_cls == 3) & ~rust & (PL[..., 0] < 50), rid == 3),
             "heather_interior": ((paint_cls == 3) & rust, erode(rid == HEATHER_ID)),
             "juniper_interior": ((paint_cls == 3) & ~rust & (PL[..., 0] < 50), erode(rid == 3))}
    for nm, (pm, rm) in pairs.items():
        if pm.sum() < 50 or rm.sum() < 50:
            warm[nm] = {"_": "too few pixels", "painting_px": int(pm.sum()), "render_px": int(rm.sum())}
            continue
        a = PL[pm].mean(0)
        b = RL[rm].mean(0)
        warm[nm] = {"painting_lab": [round(float(v), 2) for v in a],
                    "render_lab": [round(float(v), 2) for v in b],
                    "dE76": round(float(np.linalg.norm(a - b)), 2),
                    "painting_px": int(pm.sum()), "render_px": int(rm.sum())}
    # HOW MUCH OF THE HEATHER READS WARM AT ALL, by the painting's own rust rule: of the
    # heather pixels the eye can see, the share that pass a* > 5 and b* > 13. The painting's
    # figure is 1.0 by construction (its heather IS the rust pixels); the render's is not.
    hv = rid == HEATHER_ID
    if hv.sum() >= 50:
        warm["heather_warm_share"] = {"render": round(float((hv & rust_r(RL)).sum()) / float(hv.sum()), 4),
                                      "_rule": "a* > 5 and b* > 13 (the painting's heather rule), over visible heather pixels"}
    warm["_sampled_on"] = "occluded ID frame (visible pixels)" if rcls_vis_raw is not None else "T10-1b ID frame (all prop pixels)"
    rep["warmth"] = warm
    # where the misses are: coverage by image third (top = behind the mound, bottom = foreground)
    H = paint_cls.shape[0]
    bands = {}
    for nm_b, (y0, y1) in {"top": (0, H // 3), "middle": (H // 3, 2 * H // 3), "bottom": (2 * H // 3, H)}.items():
        bands[nm_b] = {k: v["coverage"] for k, v in coverage(paint_cls[y0:y1], rcls[y0:y1]).items()}
    rep["coverage_by_band"] = bands
    Image.fromarray(np.concatenate([paint_rgb, beauty], axis=1)).save(cap / "paint_vs_render_side_by_side.png")
    over = (paint_rgb.astype(np.float32) * 0.5 + beauty.astype(np.float32) * 0.5).astype(np.uint8)
    Image.fromarray(over).save(cap / "paint_vs_render_overlay50.png")
    # the ID comparison as a picture too: painting class vs render class, per pixel
    vis = np.zeros(paint_rgb.shape, np.uint8)
    for cid, col in ID_RGB.items():
        p = paint_cls == cid
        r = rcls == cid
        vis[p & r] = np.array(col) // 1
        vis[p & ~r] = (np.array(col) * 0.35).astype(np.uint8)
    Image.fromarray(vis).save(cap / "paint_coverage_map.png")
    # THE WARMTH, BEFORE AND AFTER, where the painting has its heather and juniper: the mound's
    # crown, the ring and the door, the shore, the right-hand outcrops. Same crops of the same
    # framing; the painting first, then the earlier capture, then this one.
    if args.before:
        bf = pathlib.Path(args.before) / "barrow_painting_frame.png"
        if bf.exists():
            before = np.asarray(Image.open(bf).convert("RGB"))
            crops = [(700, 0, 1100, 230), (430, 120, 900, 420), (0, 560, 470, 900), (1060, 300, 1536, 700)]
            rows = []
            for (x0, y0, x1, y1) in crops:
                row = np.concatenate([paint_rgb[y0:y1, x0:x1], np.full((y1 - y0, 8, 3), 255, np.uint8),
                                      before[y0:y1, x0:x1], np.full((y1 - y0, 8, 3), 255, np.uint8),
                                      beauty[y0:y1, x0:x1]], axis=1)
                rows.append(row)
            wmax = max(r.shape[1] for r in rows)
            rows = [np.pad(r, ((0, 8), (0, wmax - r.shape[1]), (0, 0)), constant_values=255) for r in rows]
            Image.fromarray(np.concatenate(rows, axis=0)).save(cap / "warmth_before_after.png")
            rep["warmth_before_after"] = {"before": str(bf), "crops_xyxy": crops,
                                          "columns": ["painting", "before", "this capture"]}
    (cap / "paint_coverage.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep["classes"]))
    if "classes_visible" in rep:
        print(json.dumps({"classes_visible": rep["classes_visible"], "visible_share": rep["visible_share"]}))
    print(json.dumps(rep["warmth"]))
    print(json.dumps(rep["instrument_check"]))


if __name__ == "__main__":
    main()
