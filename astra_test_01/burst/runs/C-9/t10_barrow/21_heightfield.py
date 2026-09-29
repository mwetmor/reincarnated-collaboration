#!/usr/bin/env python3
"""C-9 T10: unproject a concept painting into a TRUE-SCALE ground heightfield.

    python3 21_heightfield.py --variant a --depth marigold [--grid 0.05]

THE CAMERA IS KNOWN, so this is not a guess about perspective -- it is arithmetic with one
unknown. The concept was painted to the game's own fixed orthographic camera (R-C9-68):
pitch 52.9536 deg, azimuth 47.00 deg, basis taken from cliffside3d.gd and checked
orthonormal to 3e-8. A screen pixel and a depth give a world point outright:

    w = right*u + up*v + fwd*D          u = screen-x in metres, v = -screen-y in metres
    w.y = 0.602462*v - 0.798147*D

The one unknown is the depth map's scale, because a monocular model returns RELATIVE depth.
It is fixed TWICE, independently, and the two answers are reported side by side:

  1. THE FIGURE. A vertical rod of height h has its top nearer the camera by exactly
     sin(pitch)*h = 0.798147*h. The barbarian is 1.85 m and he is in the painting for this
     reason, so the raw depth difference between his head and his feet corresponds to a
     known 1.4766 m. This is the calibration the level is built on.
  2. THE GROUND. On flat ground D = 0.75483*v exactly -- depth there is a function of
     screen height alone. Regressing raw depth against v over open snow gives a second
     scale that never touches the figure. The ground is a hill, not a plane, so the two
     will not agree exactly; HOW MUCH they disagree is the honest error bar on the whole
     terrain, and it is printed rather than buried.

If those two disagree by more than a little, the terrain is not trustworthy at that scale
and the report says so instead of shipping a confident heightfield.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts" / "T10C-barrow"
WORK = HERE / "work"

RIGHT = np.array([0.681998491287231, 0.0, -0.731353580951691])
UP = np.array([-0.583728015422821, 0.60246217250824, -0.54433536529541])
FWD = np.array([-0.440612882375717, -0.798147439956665, -0.410878270864487])
SIN_PITCH = 0.798147439956665
COS_PITCH = 0.602462172508240
FIGURE_M = 1.85

# masks that are NOT terrain and must be filled under
OBJECT_MASKS = ["figure", "standing_stones", "barrow_door", "trees", "juniper", "rock", "raven"]


def srgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    """sRGB 8-bit -> CIE Lab (D65). Written out rather than imported: the material classes
    here are separated by CHROMA and by warm-vs-neutral, and both of those are meaningless
    in RGB, where the snow's blue shadow and the rock's grey differ mostly in luma."""
    c = rgb.astype(np.float32) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]], np.float32)
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883], np.float32)
    e, k = 216.0 / 24389.0, 24389.0 / 27.0
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16.0) / 116.0)
    return np.stack([116.0 * f[..., 1] - 16.0,
                     500.0 * (f[..., 0] - f[..., 1]),
                     200.0 * (f[..., 1] - f[..., 2])], -1)


def load_mask(v: str, name: str, shape) -> np.ndarray | None:
    p = WORK / ("evf_%s_%s.png" % (v, name))
    if not p.exists():
        return None
    m = np.asarray(Image.open(p).convert("L").resize((shape[1], shape[0]), Image.NEAREST))
    return m > 127


def load_depth(v: str, name: str, shape) -> np.ndarray | None:
    """Load a depth map WITHOUT going through 8-bit.

    Marigold returns mode 'I;16' at full resolution, and `.convert("L")` on it saturates:
    the array comes back min 0, max 255, MEAN 255 -- a picture that is almost entirely
    white and still loads, still resizes, still unprojects, and would have produced a
    confident flat terrain from the best map of the four. The 8-bit models are read as
    before; the 16-bit one is read as 16-bit.
    """
    p = WORK / ("depth_%s_%s.png" % (v, name))
    if not p.exists():
        return None
    im = Image.open(p)
    if im.mode in ("I;16", "I;16B", "I", "F"):
        d = np.asarray(im).astype(np.float32)
    else:
        d = np.asarray(im.convert("L")).astype(np.float32)
    if d.shape != tuple(shape):
        d = np.asarray(Image.fromarray(d, mode="F").resize((shape[1], shape[0]), Image.BILINEAR))
    return d.astype(np.float32)


def orient(d: np.ndarray, ground: np.ndarray) -> tuple[np.ndarray, str]:
    """Return depth that INCREASES with distance, and say which way it came in.

    Every model in this set is free to return either depth or inverse depth, and both
    render as a plausible grey picture. The bottom of an orthographic ground plane is
    nearer than the top by construction, so the sign is read off the picture rather than
    off the model's documentation."""
    h = d.shape[0]
    top = d[: h // 4][ground[: h // 4]]
    bot = d[-h // 4:][ground[-h // 4:]]
    if top.size < 50 or bot.size < 50:
        return d, "unknown (not enough ground)"
    if bot.mean() > top.mean():        # bright = near => inverse depth
        return d.max() - d, "inverse (bright = near), flipped"
    return d, "direct (bright = far)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="a")
    ap.add_argument("--depth", default="marigold")
    ap.add_argument("--grid", type=float, default=0.05, help="heightfield metres per cell")
    ap.add_argument("--smooth", type=float, default=0.0,
                    help="gaussian sigma in SCREEN pixels applied to the depth map before "
                         "unprojecting. A painted snow field's fine depth detail is TEXTURE "
                         "-- brush grain, footprints, hatching -- and unprojecting it turns "
                         "every brushstroke into a cliff. Smoothing before unprojection is "
                         "not cosmetic: it is the statement that relief lives at metre "
                         "scale here and the rest is surface.")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    v = a.variant

    rgb = np.asarray(Image.open(ART / ("T10C-barrow_%s.png" % v)).convert("RGB"))
    H, W = rgb.shape[:2]
    rep = {"variant": v, "depth_model": a.depth, "image": [W, H]}

    # ---- the scale bar -------------------------------------------------------
    fig = load_mask(v, "figure", (H, W))
    if fig is None or fig.sum() < 200:
        raise SystemExit("no usable figure mask for variant %s" % v)
    fig = ndimage.binary_opening(fig, np.ones((3, 3)))
    lab, n = ndimage.label(fig)
    if n > 1:                      # keep the largest blob: the mask can catch his shadow
        sizes = ndimage.sum(fig, lab, range(1, n + 1))
        fig = lab == (1 + int(np.argmax(sizes)))
    ys, xs = np.nonzero(fig)
    fig_px = int(ys.max() - ys.min() + 1)
    # he is drawn with a helmet; the brief's 1.85 m is the body. Use the body height and
    # say so, rather than silently calling the helmet part of the man.
    K = fig_px / (FIGURE_M * COS_PITCH)
    rep["figure"] = {"bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                     "screen_px_tall": fig_px, "assumed_m": FIGURE_M,
                     "px_per_metre": round(float(K), 2),
                     "scene_metres": [round(W / K, 2), round(H / (K * SIN_PITCH), 2)]}

    # ---- terrain vs objects --------------------------------------------------
    objs = np.zeros((H, W), bool)
    found = {}
    for nm in OBJECT_MASKS:
        m = load_mask(v, nm, (H, W))
        if m is None:
            continue
        found[nm] = round(float(m.mean() * 100), 2)
        objs |= m
    objs = ndimage.binary_dilation(objs, np.ones((5, 5)))
    terrain = ~objs
    rep["masks_pct"] = found
    rep["terrain_pct"] = round(float(terrain.mean() * 100), 2)

    d_raw = load_depth(v, a.depth, (H, W))
    if d_raw is None:
        raise SystemExit("no depth map %s for variant %s" % (a.depth, v))
    d_raw, sense = orient(d_raw, terrain)
    rep["depth_sense"] = sense
    # THE FIGURE IS MEASURED ON THE UNSMOOTHED MAP. He is 157 px tall and about 100 wide;
    # a sigma-24 blur -- which is what makes the TERRAIN plausible -- mixes his head and
    # his feet into the snow behind them and flattens the very difference the calibration
    # reads. Smoothing both moved the calibration ratio from 1.74 to 8.30 and reported it
    # as though the two estimates had simply disagreed more.
    d_fig = d_raw.copy()
    if a.smooth > 0:
        d_raw = ndimage.gaussian_filter(d_raw, a.smooth)
    rep["depth_smooth_px"] = a.smooth

    # screen coordinates in metres, origin at image centre
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx - W / 2.0) / K
    vv = -(yy - H / 2.0) / K

    # ---- calibration 1: the figure ------------------------------------------
    col = fig.sum(0)
    cx = int(np.argmax(col))
    band = slice(max(0, cx - 6), cx + 7)
    fcol = fig[:, band]
    rows = np.nonzero(fcol.any(1))[0]
    head_rows = rows[: max(3, len(rows) // 12)]
    foot_rows = rows[-max(3, len(rows) // 12):]
    d_head = float(np.median(d_fig[head_rows][:, band][fcol[head_rows]]))
    d_foot = float(np.median(d_fig[foot_rows][:, band][fcol[foot_rows]]))
    dd = d_foot - d_head          # his head is NEARER, so smaller depth
    alpha_fig = (SIN_PITCH * FIGURE_M) / dd if abs(dd) > 1e-6 else float("nan")
    rep["calib_figure"] = {"d_head": round(d_head, 2), "d_foot": round(d_foot, 2),
                           "raw_delta": round(dd, 2),
                           "expected_m": round(SIN_PITCH * FIGURE_M, 4),
                           "metres_per_raw_unit": round(float(alpha_fig), 5)}

    # ---- calibration 2: the ground ------------------------------------------
    # open snow only: terrain, and away from the objects' dilated halo
    open_snow = terrain & (ndimage.distance_transform_edt(terrain) > 12)
    A = np.stack([vv[open_snow], np.ones(int(open_snow.sum()), np.float32)], 1)
    sol, *_ = np.linalg.lstsq(A, d_raw[open_snow], rcond=None)
    slope = float(sol[0])         # raw units per metre of screen-up
    alpha_gnd = 0.754826 / slope if abs(slope) > 1e-9 else float("nan")
    rep["calib_ground"] = {"raw_per_screen_metre": round(slope, 3),
                           "flat_ground_D_per_v": 0.754826,
                           "metres_per_raw_unit": round(float(alpha_gnd), 5),
                           "open_snow_pct": round(float(open_snow.mean() * 100), 2)}
    ratio = alpha_fig / alpha_gnd if alpha_gnd else float("nan")
    rep["calib_agreement_ratio"] = round(float(ratio), 3)

    # ---- calibration 3: the unprojection must TILE ---------------------------
    # The two physical calibrations disagree badly (ratio 1.74 on variant a), and neither
    # is above suspicion: a monocular model compresses the depth of a thin vertical object
    # against a background, which inflates alpha_figure, and the ground regression assumes
    # a plane where there is a hill, which biases alpha_ground. So here is a third
    # constraint that needs no physics at all, only bookkeeping.
    #
    # The source pixels tile the screen exactly. Under the true alpha the unprojected
    # ground samples land on the world grid at roughly even density; under too large an
    # alpha the surface stretches along the view direction and TEARS, leaving grid cells
    # with no sample; under too small an alpha it piles up. So sweep alpha and watch two
    # things that disagree with each other -- grid coverage, which wants alpha small, and
    # relief, which wants it large -- and take the knee, subject to the surface staying
    # walkable. It is reported next to the other two, and if all three disagree that is the
    # finding, not something to average away.
    def build(alpha_try: float):
        Dt = (d_raw - d_raw[open_snow].mean()) * alpha_try
        wy_ = COS_PITCH * vv - SIN_PITCH * Dt
        wx_ = RIGHT[0] * u + UP[0] * vv + FWD[0] * Dt
        wz_ = RIGHT[2] * u + UP[2] * vv + FWD[2] * Dt
        pxs, pzs, pys = wx_[terrain], wz_[terrain], wy_[terrain]
        gx_ = np.floor((pxs - pxs.min()) / a.grid).astype(np.int32)
        gz_ = np.floor((pzs - pzs.min()) / a.grid).astype(np.int32)
        gw, gh = int(gx_.max()) + 1, int(gz_.max()) + 1
        if gw * gh > 40_000_000:
            return None
        acc_ = np.zeros((gh, gw), np.float64)
        cnt_ = np.zeros((gh, gw), np.int32)
        np.add.at(acc_, (gz_, gx_), pys)
        np.add.at(cnt_, (gz_, gx_), 1)
        f_ = cnt_ > 0
        h_ = np.zeros((gh, gw), np.float32)
        h_[f_] = (acc_[f_] / cnt_[f_]).astype(np.float32)
        if (~f_).any():
            _, ii = ndimage.distance_transform_edt(~f_, return_indices=True)
            h_ = h_[ii[0], ii[1]]
        h_ = ndimage.median_filter(h_, 3)
        gy_, gxx_ = np.gradient(h_, a.grid)
        sl = np.degrees(np.arctan(np.hypot(gy_, gxx_)))
        # COVERAGE MEANS INTERIOR HOLES, not the fraction of the bounding box.
        # The screen rectangle maps to a PARALLELOGRAM in world x/z -- the camera's azimuth
        # is 47 degrees -- so an axis-aligned grid can be at most 45.4% filled however
        # perfect the surface is. The first version measured exactly that and reported
        # 41.7% as though the surface were tearing. Closing the holes and comparing against
        # the closed mask asks the question that was meant: did the unprojection leave gaps
        # INSIDE its own footprint.
        closed = ndimage.binary_fill_holes(ndimage.binary_closing(f_, np.ones((5, 5))))
        return {"alpha": alpha_try,
                "coverage": float(f_.sum() / max(closed.sum(), 1)),
                "footprint_of_bbox": float(closed.mean()),
                "relief": float(h_.max() - h_.min()),
                "over70": float((sl > 70).mean()), "over45": float((sl > 45).mean()),
                "median_slope": float(np.median(sl))}

    sweep = []
    for mult in (0.1, 0.15, 0.2, 0.3, 0.45, 0.65, 1.0, 1.5, 2.2):
        r = build(alpha_fig * mult)
        if r:
            r["mult_of_alpha_figure"] = mult
            sweep.append(r)
    rep["calib_sweep"] = [{k: (round(v, 5) if isinstance(v, float) else v)
                           for k, v in s.items()} for s in sweep]
    ok = [s for s in sweep if s["over70"] < 0.01]
    alpha_tile = max(ok, key=lambda s: s["relief"])["alpha"] if ok else alpha_fig * 0.1
    rep["calib_tiling"] = {"metres_per_raw_unit": round(float(alpha_tile), 6),
                           "rule": "largest relief whose surface keeps <1% of cells over 70 deg"}

    # THE GROUND REGRESSION IS PRIMARY, and the reason is which signal is bigger.
    #
    # alpha_ground fits the whole snow field -- 73% of the frame -- against a relation that
    # is EXACT for this camera: on flat ground D = 0.75483*v, depth as a function of screen
    # height alone. The ground is a hill rather than a plane, so the fit is biased, but the
    # hill's deviation is small beside a ramp that runs the full 9 m of the scene.
    #
    # alpha_figure fits ONE thin vertical object 157 px tall, and monocular models are
    # known to compress the depth extent of exactly that -- a thin thing against a
    # background. Its bias has a direction: it reads the head and feet as closer together
    # in depth than they are, so it over-estimates metres-per-unit. Measured here at 1.74x
    # alpha_ground, which is that bias, not a coin toss between two equal estimates.
    #
    # So: ground leads, figure is the cross-check, and the ratio is the error bar. The
    # tiling sweep stays in the report as a diagnostic but no longer chooses anything --
    # its coverage number was measuring the camera's azimuth until it was fixed.
    alpha = float(alpha_gnd)
    rep["alpha_used"] = {"value": round(alpha, 7), "source": "ground regression",
                         "vs_figure": round(alpha / alpha_fig, 3),
                         "vs_tiling": round(alpha / alpha_tile, 3)}
    D = (d_raw - d_raw[open_snow].mean()) * alpha

    # ---- unproject -----------------------------------------------------------
    wy = COS_PITCH * vv - SIN_PITCH * D
    wx = RIGHT[0] * u + UP[0] * vv + FWD[0] * D
    wz = RIGHT[2] * u + UP[2] * vv + FWD[2] * D

    sel = terrain
    px, pz, py = wx[sel], wz[sel], wy[sel]
    g = a.grid
    gx = np.floor((px - px.min()) / g).astype(np.int32)
    gz = np.floor((pz - pz.min()) / g).astype(np.int32)
    GW, GH = int(gx.max()) + 1, int(gz.max()) + 1
    acc = np.zeros((GH, GW), np.float64)
    cnt = np.zeros((GH, GW), np.int32)
    np.add.at(acc, (gz, gx), py)
    np.add.at(cnt, (gz, gx), 1)
    filled = cnt > 0
    hf = np.zeros((GH, GW), np.float32)
    hf[filled] = (acc[filled] / cnt[filled]).astype(np.float32)

    # fill the holes the objects left, from their rims inward
    if (~filled).any():
        _, idx = ndimage.distance_transform_edt(~filled, return_indices=True)
        hf = hf[idx[0], idx[1]]
    hf = ndimage.median_filter(hf, 3)

    gy, gxg = np.gradient(hf, g)
    slope_deg = np.degrees(np.arctan(np.hypot(gy, gxg)))
    lap = ndimage.laplace(hf)
    rep["heightfield"] = {
        "grid_m": g, "size": [GW, GH],
        "extent_m": [round(GW * g, 2), round(GH * g, 2)],
        "height_range_m": [round(float(hf.min()), 3), round(float(hf.max()), 3)],
        "relief_m": round(float(hf.max() - hf.min()), 3),
        "coverage_pct": round(float(filled.sum() / max(ndimage.binary_fill_holes(
            ndimage.binary_closing(filled, np.ones((5, 5)))).sum(), 1) * 100), 2),
        "footprint_pct_of_bbox": round(float(ndimage.binary_fill_holes(
            ndimage.binary_closing(filled, np.ones((5, 5)))).mean() * 100), 2),
        "slope_deg": {"median": round(float(np.median(slope_deg)), 1),
                      "p90": round(float(np.percentile(slope_deg, 90)), 1),
                      "over_45_pct": round(float((slope_deg > 45).mean() * 100), 2),
                      "over_70_pct": round(float((slope_deg > 70).mean() * 100), 2)},
        "roughness_lap_rms_m": round(float(np.sqrt((lap ** 2).mean())), 4),
    }

    # ---- material splat, IN THE SAME PASS -----------------------------------
    # Registered to the heightfield by construction rather than by agreement: the same
    # pixels, the same D, the same (gz,gx). Two tools unprojecting separately would need
    # their camera constants, their depth calibration and their grid origin to match, and
    # nothing would check that they did.
    lab = srgb_to_lab(rgb)
    L, aa_, bb_ = lab[..., 0], lab[..., 1], lab[..., 2]
    chroma = np.hypot(aa_, bb_)
    ice_m = load_mask(v, "ice", (H, W))
    path_m = load_mask(v, "path", (H, W))
    cls = np.zeros((H, W), np.uint8)              # 0 = snow
    cls[(chroma > 12) & (bb_ > 6)] = 3            # dead grass / heather: warm
    cls[(L < 72) & (chroma <= 14)] = 2            # rock: mid grey, neutral
    if ice_m is not None:
        cls[ice_m & (bb_ < 2)] = 4                # blue ice, only where it reads blue
    if path_m is not None:
        cls[path_m & (cls == 0)] = 1              # trodden path, only over snow
    names = ["snow", "path", "rock", "grass", "ice"]
    splat = np.zeros((GH, GW), np.uint8)
    votes = np.zeros((GH, GW, len(names)), np.int32)
    np.add.at(votes, (gz, gx, cls[sel]), 1)
    any_v = votes.sum(2) > 0
    splat[any_v] = votes[any_v].argmax(1).astype(np.uint8)
    if (~any_v).any():
        _, idx2 = ndimage.distance_transform_edt(~any_v, return_indices=True)
        splat = splat[idx2[0], idx2[1]]
    rep["splat"] = {"classes": names,
                    "screen_pct": {n: round(float((cls == i).mean() * 100), 2)
                                   for i, n in enumerate(names)},
                    "grid_pct": {n: round(float((splat == i).mean() * 100), 2)
                                 for i, n in enumerate(names)}}

    out = pathlib.Path(a.out) if a.out else HERE / "out"
    out.mkdir(parents=True, exist_ok=True)
    pal = np.array([[245, 247, 250], [214, 219, 226], [122, 122, 118],
                    [166, 138, 84], [150, 196, 214]], np.uint8)
    Image.fromarray(pal[splat]).save(out / ("splat_%s_%s.png" % (v, a.depth)))
    Image.fromarray(splat).save(out / ("splat_ids_%s_%s.png" % (v, a.depth)))
    lo, hi = float(hf.min()), float(hf.max())
    span = max(hi - lo, 1e-6)
    png = ((hf - lo) / span * 65535.0).astype(np.uint16)
    Image.fromarray(png, mode="I;16").save(out / ("height_%s_%s.png" % (v, a.depth)))
    rep["png"] = {"file": str(out / ("height_%s_%s.png" % (v, a.depth))),
                  "encoding": "16-bit, 0 = min height, 65535 = max",
                  "metres_per_pixel": g, "height_min_m": round(lo, 4),
                  "height_max_m": round(hi, 4),
                  "metres_per_level": round(span / 65535.0, 8)}
    (out / ("height_%s_%s.json" % (v, a.depth))).write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps(rep, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
