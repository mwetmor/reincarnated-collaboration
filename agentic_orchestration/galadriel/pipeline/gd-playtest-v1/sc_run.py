#!/usr/bin/env python3
"""SHADOW-CAL: per-burst pipeline.

  frames -> world-registered median plate -> shadow/sprite separation
         -> figure/shadow pairing -> ground-plane azimuth + length ratio

Everything is measured on the GROUND PLANE through the GAL-CAM pinhole, not in
screen pixels: a screen-space "shadow angle" is meaningless under a 53 deg
pitch, where the same ground direction reads at a different screen angle at
every row and at every column.

SCREEN-LOCKED CONTENT is found, not assumed.  When the camera translates, any
pixel whose value barely changes in SCREEN coordinates is not ground -- it is
HUD, minimap, quest text, an open inventory panel, or a debug label.  That is
measured per burst and excluded.  When the camera does not translate the
detector is void, and the fixed furniture boxes carry the exclusion instead;
which of the two applied is recorded per window.
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

import sc_plate as P
import sc_shadow as S

W, H = 1920, 1080


def furniture_mask():
    m = np.zeros((H, W), bool)
    for x0, y0, x1, y1 in P.FURNITURE_BOXES[:5]:   # not the player box
        m[y0:y1, x0:x1] = True
    return m


FURN = furniture_mask()


def _long_runs(b, axis, minlen):
    st = (np.array([[0, 1, 0], [0, 0, 0], [0, 1, 0]]) if axis == 0
          else np.array([[0, 0, 0], [1, 0, 1], [0, 0, 0]]))
    st = st + np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    lab, n = ndimage.label(b, structure=st)
    if not n:
        return np.zeros_like(b)
    sizes = ndimage.sum(b, lab, range(1, n + 1))
    return np.isin(lab, [i + 1 for i in range(n) if sizes[i] >= minlen])


def ui_mask(frame_rgb, thresh=18.0, minlen=90, pad=14, min_comp=1500):
    """Panels, tooltips and vendor windows, from long straight axis-aligned edges.

    A game render of terrain almost never produces a 90 px run of strong
    same-direction gradient; a UI border always does.  Measured separation on
    this fixture: clean frames 0.0001-0.0010 of pixels, open panels
    0.0140-0.0220 -- 14x to 140x.  Needed because the screen-locked detector
    (which finds furniture from camera motion) is VOID in a static window, and
    a tooltip popping open otherwise reads as a figure with a shadow.
    """
    a = np.asarray(frame_rgb, np.float32)
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    gx = np.abs(np.gradient(L, axis=1))
    gy = np.abs(np.gradient(L, axis=0))
    e = _long_runs(gx > thresh, 0, minlen) | _long_runs(gy > thresh, 1, minlen)
    frac = float(e.mean())
    d = ndimage.binary_dilation(e, np.ones((2 * pad + 1, 2 * pad + 1)))
    lab, n = ndimage.label(d)
    m = np.zeros_like(d)
    for i in range(1, n + 1):
        c = lab == i
        if c.sum() < min_comp:
            continue
        ys, xs = np.nonzero(c)
        m[max(0, ys.min() - pad):ys.max() + pad,
          max(0, xs.min() - pad):xs.max() + pad] = True
    return m, frac


def debug_text_mask(frame_rgb, pad=6):
    """The green entity-state debug overlay this fixture is recorded with.

    It is screen-locked text drawn over each actor's head; in a world-registered
    stack it MOVES, so it reads as a sprite, and it sits directly above the
    player -- inflating any height taken from the top of the figure mask.  It is
    cut by colour, which is unambiguous: pure green over a black outline exists
    nowhere in this game's terrain.
    """
    a = np.asarray(frame_rgb, np.float32)
    g = (a[..., 1] > 140) & (a[..., 1] - a[..., 0] > 55) & (a[..., 1] - a[..., 2] > 55)
    return ndimage.binary_dilation(g, np.ones((2 * pad + 1, 2 * pad + 1))), float(g.mean())


def screen_locked(paths, shifts, thresh=1.2, min_travel=6.0, min_area=20000):
    """Pixels that hardly change in SCREEN coordinates while the ground moves."""
    good = [i for i in range(len(paths)) if np.isfinite(shifts[i]).all()]
    fin = shifts[good]
    travel = max(np.ptp(fin[:, 0]), np.ptp(fin[:, 1])) if len(fin) else 0.0
    if travel < min_travel or len(good) < 12:
        return None, float(travel)
    sub = good[:: max(1, len(good) // 40)]
    L = np.stack([P.luma(P.read(paths[i]).astype(np.float32)) for i in sub])
    mad = 1.4826 * np.median(np.abs(L - np.median(L, 0)), 0)
    m = mad < thresh
    m = ndimage.binary_closing(m, np.ones((9, 9)))
    lab, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, [i + 1 for i in range(n) if sizes[i] >= min_area])
    else:
        m = np.zeros_like(m)
    return ndimage.binary_dilation(m, np.ones((7, 7))), float(travel)


def figures_and_shadows(frame, plate, valid, cam, sigma=None,
                        min_fig=350, min_sh=200, link_px=26, ui=None):
    r = S.separate(frame, plate, sigma)
    if ui is not None:
        valid = valid & ~ui
    sh, _, _ = S.clean(r["shadow"] & valid, min_px=min_sh)
    sp, _, _ = S.clean(r["sprite"] & valid, min_px=min_fig)

    labf, nf = ndimage.label(sp)
    labs, ns = ndimage.label(sh)
    fobj = ndimage.find_objects(labf)
    sobj = ndimage.find_objects(labs)
    out = []
    for fi in range(1, nf + 1):
        fsl = fobj[fi - 1]
        fmb = labf[fsl] == fi
        if fmb.sum() < min_fig:
            continue
        fm = np.zeros_like(labf, bool)
        fm[fsl] = fmb
        ys, xs = np.nonzero(fm)
        y_bot = int(ys.max())
        # ESTIMATORS FIXED BY CONTROL SC-C2 (sc_synth2.py):
        #   base = "bottom_q"  x median of the lowest rows, y at the 92nd pct
        #   top  = "col_q"     2nd pct of rows within +-8 px of the base column
        #   tip  = "q99"       mean of the farthest 1% of shadow pixels
        # naive extremes (bottom-most row / global top / farthest pixel) carry
        # +30% height bias and -12% ratio bias; this triple carries -4.2%.
        bx = float(np.median(xs[ys >= y_bot - 4]))
        by = float(np.percentile(ys, 92))
        _c = np.abs(xs - bx) <= 8
        ty = float(np.percentile(ys[_c], 2)) if _c.any() else float(ys.min())
        hpx = int(ys.max() - ys.min()) + 1
        wpx = int(xs.max() - xs.min()) + 1
        if hpx < 20 or wpx > 420 or hpx > 420:
            continue
        base = cam.unproject_ground([[bx, by]])
        h_m = cam.solve_height((base[0], base[2]), ty)
        if not (0.4 < h_m < 6.0):
            continue
        # bounding-box work only: a full-frame dilation per figure made this
        # loop quadratic in figure count and the pass unusably slow
        y0b = max(0, int(ys.min()) - link_px)
        y1b = min(frame.shape[0], int(ys.max()) + link_px + 1)
        x0b = max(0, int(xs.min()) - link_px)
        x1b = min(frame.shape[1], int(xs.max()) + link_px + 1)
        sub = fm[y0b:y1b, x0b:x1b]
        near = ndimage.binary_dilation(sub, np.ones((link_px, link_px)))
        ids = np.unique(labs[y0b:y1b, x0b:x1b][near])
        ids = ids[ids > 0]
        lobes = []
        for si in ids:
            sl = sobj[si - 1]
            smb = labs[sl] == si
            n = int(smb.sum())
            if n < min_sh:
                continue
            syb, sxb = np.nonzero(smb)
            sy = syb + sl[0].start
            sx = sxb + sl[1].start
            g = cam.unproject_ground(np.stack([sx, sy], 1).astype(float))
            d = g[:, [0, 2]] - np.array([base[0], base[2]])
            rad = np.hypot(d[:, 0], d[:, 1])
            tip = d[rad >= np.quantile(rad, 0.99)].mean(0)
            cen = d.mean(0)
            dc = d - cen
            cov = dc.T @ dc / max(len(dc), 1)
            ev, evec = np.linalg.eigh(cov)
            ax = evec[:, -1]
            if ax @ tip < 0:
                ax = -ax
            k = int(np.argmax(rad))
            lobes.append({
                "px": n,
                "tip_m": [float(tip[0]), float(tip[1])],
                "cen_m": [float(cen[0]), float(cen[1])],
                "len_m": float(np.hypot(*tip)),
                "cen_len_m": float(np.hypot(*cen)),
                "az_tip": float(math.degrees(math.atan2(tip[1], tip[0]))),
                "az_cen": float(math.degrees(math.atan2(cen[1], cen[0]))),
                "az_pca": float(math.degrees(math.atan2(ax[1], ax[0]))),
                "elong": float(np.sqrt(max(ev[-1], 1e-9) / max(ev[0], 1e-9))),
                "tip_px": [float(sx[k]), float(sy[k])],
                "rho": float(np.median(r["rho"][sl][smb])),
                "Lf": float(np.median(r["Lf"][sl][smb])),
                "Lb": float(np.median(r["Lb"][sl][smb])),
            })
        if not lobes:
            continue
        lobes.sort(key=lambda z: -z["px"])
        pad = 46
        ry0 = max(0, int(ys.min()) - pad); ry1 = min(frame.shape[0], int(ys.max()) + pad)
        rx0 = max(0, int(xs.min()) - pad); rx1 = min(frame.shape[1], int(xs.max()) + pad)
        sl = (slice(ry0, ry1), slice(rx0, rx1))
        fsub = fm[sl]
        ring = (ndimage.binary_dilation(fsub, np.ones((61, 61)))
                & ~ndimage.binary_dilation(fsub, np.ones((17, 17))))
        ring = ring & valid[sl] & ~sh[sl] & ~sp[sl]
        Lring = (float(np.median(r["Lb"][sl][ring])) if ring.sum() > 500
                 else float("nan"))
        out.append({
            "base_px": [bx, by],
            "top_px": [float(np.median(xs[ys <= ys.min() + 4])), ty],
            "base_m": [float(base[0]), float(base[2])],
            "h_m": float(h_m), "fig_px": int(fm.sum()),
            "fig_hpx": hpx, "fig_wpx": wpx,
            "L_ring": Lring, "ring_px": int(ring.sum()),
            "lobes": lobes,
        })
    return out, sh, sp, r


def draw(frame, dets, sh, sp, out, box=None):
    vis = np.asarray(frame, np.float32).copy()
    vis[sh] = vis[sh] * 0.35 + np.array([255, 40, 40]) * 0.65
    vis[sp] = vis[sp] * 0.35 + np.array([40, 150, 255]) * 0.65
    im = Image.fromarray(np.clip(vis, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for f in dets:
        bx, by = f["base_px"]
        d.ellipse([bx - 5, by - 5, bx + 5, by + 5], outline=(0, 255, 0), width=2)
        d.line([bx, by, f["top_px"][0], f["top_px"][1]], fill=(0, 255, 0), width=2)
        for L in f["lobes"][:2]:
            tx, ty = L["tip_px"]
            d.line([bx, by, tx, ty], fill=(255, 255, 0), width=2)
            d.text((bx + 8, by + 8),
                   f"az {L['az_tip']:.0f}  L/h {L['len_m']/max(f['h_m'],1e-3):.2f}"
                   f"  rho {L['rho']:.2f}", fill=(255, 255, 0))
    if box:
        im = im.crop(box)
    im.save(out, quality=92)
    return out
