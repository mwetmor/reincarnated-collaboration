#!/usr/bin/env python3
"""C-9 T4 close-out: shared measurement library for the video-route bake-off.

WHY A NEW FILE AND NOT `meshy_t2/scripts/21_drift.py` DIRECTLY.  21_drift.py's
compensation is a POS GUIDE -- the rest-pose bind position of the surface point
under each pixel, baked per vertex before skinning.  It exists only because
those frames came out of our own Blender render of a rigged mesh.  Kling and
Ludo return VIDEO: there is no mesh, no bind pose, and no pos pass, so the
nearest-neighbour-in-pos-space match cannot be computed at all.  That is the
one reason the original instrument cannot be run unchanged, and it is a
missing INPUT, not a disagreement about method.

EVERYTHING ELSE IS KEPT, and the one substitution is made in the same spirit:

  * low-pass first (gaussian sigma 3 px, MASK-NORMALISED so the background
    cannot bleed across the silhouette), because the drift that got the knight
    rejected -- "his helmet/head morph once each second" -- is a low-frequency
    property and a pixel-to-pixel compare measures texture detail instead;
  * 2 px erosion of the silhouette, dropping the anti-aliased rim;
  * compare COLOURS ONLY, after compensating for where the thing moved to;
  * a floor sequence that cannot drift, and a shuffled-order negative control.

THE SUBSTITUTION.  pos-space matching is replaced by 2D RIGID REGISTRATION of
the region being measured: the crop is placed on the part's own position each
frame (crown row and head-column centroid for the helm; silhouette centroid
and figure height for the body), resampled to a COMMON SIZE, and then the best
integer translation within +-8 px is searched for before the residual is
taken.  A helm is a rigid object seen in near-profile, so translation is what
pos-matching buys you there; what it does NOT absorb is a change of shape,
which is the thing being measured.

Rotation is deliberately NOT absorbed.  Matt's complaint was that the helmet
morphs WHEN HE TURNS HIS HEAD; a registration free to rotate would quietly
explain away the very frames the test exists to catch.

SCALE NORMALISATION IS NEW AND IS NOT OPTIONAL.  21_drift.py compared 512 px
renders to 512 px renders, so a sigma of 3 px always meant the same thing.
Here Kling returns 1440 px, Ludo returns 310-454 px, and the reference still is
1024 px: blurring all of them by 3 px would low-pass Ludo four times as hard as
Kling and hand Ludo a lower score for free.  So every crop is resampled to a
fixed size (HELM_H px of helm, BODY_H px of figure) BEFORE the blur.

THE FLOOR is `fal_t4/drive/` -- the Meshy carry-walk render that drove both
services.  It is one unlit texture on one rigged mesh, so its identity CANNOT
drift, and it is the same knight at the same kind of gait.  Whatever it scores
is the instrument's floor, exactly as the render's ~1.9 was in T1/T2.
"""
import json
import math
import os

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BLUR_SIGMA = 3.0          # px, on the NORMALISED crop; same value as 21_drift.py
ERODE_PX = 2              # px, on the normalised crop; same value as 21_drift.py
HELM_H = 96               # px: every helm crop is resampled to this helm height
BODY_H = 256              # px: every body crop is resampled to this figure height
SHIFT = 14                # px: half-width of the integer translation search.
#   8 was tried first and the Astra row pinned the cap on dx, which makes every
#   residual there an UPPER bound rather than a measurement -- the crop is
#   already centred on the part, so a pinned search means the centring itself
#   jitters by more than the window and the number reported is the residual at
#   a wrong alignment. 14 px is 15% of the normalised helm height.

RUNS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../runs/C-9


# --------------------------------------------------------------------------
# masks
# --------------------------------------------------------------------------
def load_rgba(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(np.float64)


def mask_of(path, kind):
    """kind: 'green' (flat chroma plate, no alpha) or 'alpha'."""
    a = load_rgba(path)
    rgb = a[..., :3]
    if kind == "alpha":
        m = a[..., 3] > 128
    else:
        g = rgb[..., 1]
        bg = (g > 110) & (g - np.maximum(rgb[..., 0], rgb[..., 2]) > 45)
        m = ~bg
    m = ndi.binary_opening(m, np.ones((3, 3), bool))
    lab, n = ndi.label(m)
    if n > 1:                       # drop keying speckle, keep everything real
        sz = ndi.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s >= 0.01 * sz.max()])
    return rgb, m


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def body_component(mask, r):
    """The figure with the pollaxe HAFT deleted.

    build_knight_frames.py uses a 1 x N HORIZONTAL opening, which is correct
    for the reference still because the haft there is vertical.  It is wrong
    here and was caught by probing rather than by reading: Kling re-stages the
    pollaxe at a lean, and a diagonal bar has horizontal runs far wider than
    its own thickness, so the horizontal opening kept most of Kling's haft
    inside the body (6.9k weapon px against the still's 27.3k) -- the check ran
    and returned a confident wrong answer.  A DISK of radius r severs anything
    thinner than 2r at ANY orientation, which is what "the haft" means.

    The largest surviving component is then the body.  Largest rather than
    topmost, deliberately: the opening disconnects the AXE HEAD as its own
    component, and a topmost rule returns the top of the blade as the crown.
    """
    o = ndi.binary_opening(mask, disk(max(2, int(r))))
    lab, n = ndi.label(o)
    if n == 0:
        return mask
    sz = ndi.sum(o, lab, range(1, n + 1))
    return lab == (1 + int(np.argmax(sz)))


def weapon_component(mask, body):
    """What the opening removed: haft + blade + anything else thin."""
    w = mask & ~ndi.binary_dilation(body, np.ones((3, 3), bool))
    lab, n = ndi.label(w)
    if n == 0:
        return w
    sz = ndi.sum(w, lab, range(1, n + 1))
    return np.isin(lab, [i + 1 for i, s in enumerate(sz) if s >= 0.05 * sz.max()])


# --------------------------------------------------------------------------
# figure and helm geometry
# --------------------------------------------------------------------------
def figure_span(body):
    ys = np.nonzero(body.sum(1))[0]
    return int(ys.min()), int(ys.max())


def helm_band(body, crown, sole, frac_cap=0.35, smooth=3):
    """Crown row -> NECK row, found from the body's own row-width profile.

    Descending from the crown the profile rises across the helm, falls to a
    local minimum at the neck/gorget, then rises again into the shoulders.
    The neck is that minimum.  The search is capped at frac_cap of the figure
    so a narrow waist can never be mistaken for a neck.
    """
    H = sole - crown + 1
    cap = crown + max(4, int(frac_cap * H))
    prof = body[crown:cap + 1].sum(1).astype(float)
    if len(prof) < 5:
        return crown, min(sole, crown + max(2, int(0.15 * H)))
    k = np.ones(smooth) / smooth
    sm = np.convolve(prof, k, mode="same")
    top = int(np.argmax(sm[:max(2, len(sm) // 2)]))       # widest row of the helm
    tail = sm[top:]
    neck_rel = top + int(np.argmin(tail))
    if neck_rel - top < 2:                                 # no pinch found
        neck_rel = max(2, int(0.15 * H))
    return crown, crown + neck_rel


def helm_box(rgb, mask, body, crown, neck, sole, pad_frac=0.25):
    """A FIXED-PROPORTION box, positioned on the helm.

    Square, side 1.5 x the crown-to-neck height, centred on the helm's own
    column centroid.  The padding is a fraction of the HELM, not of the figure:
    keyed to the figure it made the box more than twice the head's height, and
    most of what got measured was empty plate below the gorget.

    Fixed proportions matter.  A box refitted to the helm's silhouette every
    frame would shrink onto a helm that changed shape and hide the change --
    the crop would absorb exactly the drift it exists to show (24_mp4.py's
    rule, for the same reason).  The box MOVES with the helm; it does not
    RESIZE.
    """
    hh = max(4, neck - crown)
    pad = max(2, int(pad_frac * hh))
    y0, y1 = crown - pad, neck + pad
    band = body[max(0, crown):neck + 1]
    xs = np.nonzero(band.sum(0))[0]
    cx = float(xs.mean()) if len(xs) else body.shape[1] / 2.0
    half = (y1 - y0) / 2.0
    x0, x1 = int(round(cx - half)), int(round(cx + half))
    return y0, y1, x0, x1


def crop_pad(arr, y0, y1, x0, x1, fill=0.0):
    """Crop with zero padding, so a box running off the canvas is still legal."""
    h, w = arr.shape[:2]
    shp = (y1 - y0, x1 - x0) + arr.shape[2:]
    out = np.full(shp, fill, dtype=arr.dtype)
    sy0, sy1 = max(0, y0), min(h, y1)
    sx0, sx1 = max(0, x0), min(w, x1)
    if sy1 > sy0 and sx1 > sx0:
        out[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = arr[sy0:sy1, sx0:sx1]
    return out


def resample(rgb, m, size):
    """Resample a crop and its mask to (size, size)."""
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    mm = Image.fromarray((m * 255).astype(np.uint8))
    return (np.asarray(im.resize((size, size), Image.BILINEAR)).astype(np.float64),
            np.asarray(mm.resize((size, size), Image.BILINEAR)) > 127)


# --------------------------------------------------------------------------
# the drift measure itself
# --------------------------------------------------------------------------
def lowpass(rgb, m):
    """Mask-normalised gaussian: background cannot bleed across the silhouette."""
    w = m.astype(np.float64)
    num = np.stack([ndi.gaussian_filter(rgb[..., k] * w, BLUR_SIGMA)
                    for k in range(3)], -1)
    den = np.maximum(ndi.gaussian_filter(w, BLUR_SIGMA), 1e-6)[..., None]
    return num / den


def prepped(rgb, m, size):
    r, mm = resample(rgb, m, size)
    return lowpass(r, mm), ndi.binary_erosion(mm, np.ones((2 * ERODE_PX + 1,) * 2))


def _score(a, ma, b, mb, dy, dx, floor=40):
    bs = np.roll(np.roll(b, dy, 0), dx, 1)
    ms = np.roll(np.roll(mb, dy, 0), dx, 1)
    ov = ma & ms
    n = int(ov.sum())
    if n < floor:
        return None
    return float(np.abs(a[ov] - bs[ov]).mean()), n


def residual(a, ma, b, mb, shift=SHIFT):
    """Mean |dRGB| in 0-255 over the shared silhouette, at the best integer
    translation within +-shift.  Returns (value, dy, dx, overlap_fraction).

    Coarse-to-fine: the full +-shift grid is swept on a 2x-decimated copy, then
    refined +-2 px at full resolution.  Exhaustive at full resolution costs
    (2*shift+1)^2 evaluations of a 256x256 array per pair, which on the 150
    Kling frames is the whole runtime; the decimated sweep is 1/4 the pixels
    and the refinement is 25 evaluations.  Checked against the exhaustive
    version on every route: same shift or within 1 px, residual within 0.02.
    """
    a2, ma2 = a[::2, ::2], ma[::2, ::2]
    b2, mb2 = b[::2, ::2], mb[::2, ::2]
    h = max(1, shift // 2)
    best = None
    for dy in range(-h, h + 1):
        for dx in range(-h, h + 1):
            s = _score(a2, ma2, b2, mb2, dy, dx, floor=10)
            if s and (best is None or s[0] < best[0]):
                best = (s[0], dy, dx)
    if best is None:
        return float("nan"), 0, 0, 0.0
    cy, cx = best[1] * 2, best[2] * 2
    fine = None
    for dy in range(cy - 2, cy + 3):
        for dx in range(cx - 2, cx + 3):
            s = _score(a, ma, b, mb, dy, dx)
            if s and (fine is None or s[0] < fine[0]):
                fine = (s[0], dy, dx, s[1] / max(1, int(ma.sum())))
    return fine if fine else (float("nan"), 0, 0, 0.0)


def residual_exhaustive(a, ma, b, mb, shift=SHIFT):
    """The un-optimised version, kept so the fast one can be checked against it."""
    best = None
    for dy in range(-shift, shift + 1):
        for dx in range(-shift, shift + 1):
            s = _score(a, ma, b, mb, dy, dx)
            if s and (best is None or s[0] < best[0]):
                best = (s[0], dy, dx, s[1] / max(1, int(ma.sum())))
    return best if best else (float("nan"), 0, 0, 0.0)


# --------------------------------------------------------------------------
# per-frame geometry record, shared by every measurement below
# --------------------------------------------------------------------------
def frame_geometry(path, kind, open_frac=0.016):
    """open_frac: disk RADIUS as a fraction of the mask's height.  0.016 puts
    the cut at ~3.2% of figure height -- above the haft (measured 1.5-2.5%
    across all five sources) and below the greave and the forearm (6%+)."""
    rgb, m = mask_of(path, kind)
    ys = np.nonzero(m.sum(1))[0]
    if not len(ys):
        return None
    open_w = max(2, int(round(open_frac * (ys.max() - ys.min() + 1))))
    body = body_component(m, open_w)
    crown, sole = figure_span(body)
    c, neck = helm_band(body, crown, sole)
    return dict(rgb=rgb, mask=m, body=body, crown=crown, sole=sole, neck=neck,
                H=sole - crown + 1, open_w=open_w,
                weapon=weapon_component(m, body))


def helm_patch(g):
    y0, y1, x0, x1 = helm_box(g["rgb"], g["mask"], g["body"], g["crown"],
                              g["neck"], g["sole"])
    r = crop_pad(g["rgb"], y0, y1, x0, x1)
    mm = crop_pad(g["body"].astype(np.uint8), y0, y1, x0, x1).astype(bool)
    return prepped(r, mm, HELM_H) + ((y0, y1, x0, x1),)


def body_patch(g):
    """Square box about the whole figure (body only -- the weapon is excluded so
    a route that redrew the pollaxe is not scored twice for it)."""
    H = g["H"]
    xs = np.nonzero(g["body"].sum(0))[0]
    cx = float(xs.mean())
    pad = int(0.08 * H)
    y0, y1 = g["crown"] - pad, g["sole"] + pad
    half = (y1 - y0) / 2.0
    x0, x1 = int(round(cx - half)), int(round(cx + half))
    r = crop_pad(g["rgb"], y0, y1, x0, x1)
    mm = crop_pad(g["body"].astype(np.uint8), y0, y1, x0, x1).astype(bool)
    return prepped(r, mm, BODY_H) + ((y0, y1, x0, x1),)


def stats(vals):
    v = np.asarray([x for x in vals if x == x], dtype=float)
    if not len(v):
        return None
    return dict(n=int(len(v)), median=round(float(np.median(v)), 2),
                p90=round(float(np.percentile(v, 90)), 2),
                max=round(float(v.max()), 2), mean=round(float(v.mean()), 2),
                p10=round(float(np.percentile(v, 10)), 2),
                min=round(float(v.min()), 2))
