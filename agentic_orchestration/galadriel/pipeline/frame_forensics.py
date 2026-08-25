#!/usr/bin/env python3
"""
frame_forensics.py — per-frame decomposition instrument for VFX depth comparison.

Dispatch: agentic_orchestration/dispatches/2026-08-25-galadriel-reference-frame-forensics.md
Author:   galadriel (visual perception + UX-similarity steward)
Date:     2026-08-25

WHAT THIS IS
    Runs identically on an arbitrary clip (a reference capture or one of our
    renders) and emits comparable numeric SERIES -- per-frame rows, not summary
    stats, and not a similarity score. Matt's method-word is "statistically pick
    each clip apart"; a single scalar re-composes it, so no series here reduces
    to one.

WHAT THIS IS NOT
    It does not grade. There is no PASS/FAIL, no bar, and no verdict anywhere in
    this file. Thresholds that the series need are DERIVED per-clip from that
    clip's own noise floor and are emitted alongside a SWEEP, so that no reading
    rests on a single chosen value (#80 cl. 2(a); and my own ruling of
    2026-08-25 sec 5.3, where a bar defined against an unswept parameter turned
    out to be unfailable by construction).

DESIGN NOTES THAT ARE LOAD-BEARING
    1. NO DECODED FRAME IS WRITTEN TO DISK. ffmpeg pipes rawvideo to stdout and
       frames are consumed one at a time. See PREFIRE-DISK-PROJECTION.md sec 1.
    2. Component COUNTS are not used as a primary descriptor. My ruling of
       2026-08-25 (notes/2026-08-25-xrow-significant-components-instrument-ruling.md)
       measured a component count moving +426% across a 16x pixel-count range on
       identical frames while a mass fraction moved +9.4%. The two legs here
       differ by 2.25x in pixel count, so a count operator is disqualified before
       it is run. D1 is a multiscale ENERGY spectrum instead; N_eff is emitted as
       a swept secondary only.
    3. Every series is computed on a TEMPORAL-NOVELTY field (frame minus a
       temporal-median background plate), not on the raw frame, so that static
       scene texture -- the arena's tile grid, the cathedral's masonry -- cancels
       instead of being counted as effect detail.
    4. Every series is computed at every rung of a RESOLUTION LADDER. A series
       whose value moves more across the ladder than it moves between the legs
       cannot carry the comparison, and saying so is a finding that outranks the
       number.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field, asdict

import numpy as np

# ---------------------------------------------------------------------------
# Rec.709 luma. Named here rather than inlined so the convention travels with
# every number the module emits (#64 FRAME FORM).
# ---------------------------------------------------------------------------
REC709 = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)

LADDER = [(320, 180), (640, 360), (960, 540), (1280, 720)]
PRIMARY = (1280, 720)
PLATE_SAMPLES = 48
PYRAMID_LEVELS = 6
NEFF_FLOOR_LADDER = [2, 4, 8, 16, 32, 48]


# ===========================================================================
# 0. DECODE -- streaming, zero frames on disk
# ===========================================================================

def probe(path: str) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate,codec_name,nb_frames",
         "-show_entries", "format=duration,size",
         "-of", "json", path],
        capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    st, fm = j["streams"][0], j["format"]
    num, den = st["r_frame_rate"].split("/")
    return {
        "path": path,
        "codec": st["codec_name"],
        "src_w": int(st["width"]),
        "src_h": int(st["height"]),
        "src_fps": float(num) / float(den),
        "duration_s": float(fm["duration"]),
        "bytes": int(fm["size"]),
    }


def stream_frames(path: str, w: int, h: int, fps: float):
    """Yield HxWx3 uint8 frames. Nothing touches disk.

    scale is applied BEFORE fps so the decimation acts on the analysis raster;
    'bicubic' is named explicitly rather than left to the ffmpeg default,
    because a resampler choice is a silent transformation and this seam does not
    permit those.
    """
    vf = f"scale={w}:{h}:flags=bicubic,fps={fps}"
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", vf,
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE, bufsize=w * h * 3 * 4)
    n = w * h * 3
    try:
        while True:
            buf = p.stdout.read(n)
            if len(buf) < n:
                break
            yield np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3)
    finally:
        p.stdout.close()
        p.wait()


# ===========================================================================
# 1. COLOUR + FIELD HELPERS
# ===========================================================================

def luma(rgb: np.ndarray) -> np.ndarray:
    return (rgb.astype(np.float32) @ REC709)


def rgb_to_hsv(rgb: np.ndarray):
    """Vectorised HSV. H in [0,1) turns, S,V in [0,1]."""
    a = rgb.astype(np.float32) / 255.0
    mx = a.max(axis=-1)
    mn = a.min(axis=-1)
    d = mx - mn
    h = np.zeros_like(mx)
    nz = d > 1e-6
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    im = a.argmax(axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        h = np.where(nz & (im == 0), ((g - b) / np.where(d == 0, 1, d)) % 6.0, h)
        h = np.where(nz & (im == 1), ((b - r) / np.where(d == 0, 1, d)) + 2.0, h)
        h = np.where(nz & (im == 2), ((r - g) / np.where(d == 0, 1, d)) + 4.0, h)
    h = (h / 6.0) % 1.0
    s = np.where(mx > 1e-6, d / np.where(mx == 0, 1, mx), 0.0)
    return h.astype(np.float32), s.astype(np.float32), mx.astype(np.float32)


def box_down(x: np.ndarray) -> np.ndarray:
    h, w = x.shape[:2]
    h2, w2 = h // 2, w // 2
    return x[:h2 * 2, :w2 * 2].reshape(h2, 2, w2, 2).mean(axis=(1, 3))


def box_up(x: np.ndarray, shape) -> np.ndarray:
    y = np.repeat(np.repeat(x, 2, axis=0), 2, axis=1)
    return y[:shape[0], :shape[1]]


def laplacian_band_energy(field: np.ndarray, levels: int = PYRAMID_LEVELS):
    """Fraction of total field variance carried in each octave band.

    Band 0 is the finest (single-pixel-scale) detail; the last entry is the
    residual coarse plate. Returns (fractions, total_energy).

    THIS IS THE D1 OPERATOR. It has no threshold, no connectivity convention,
    and no significance gate -- the three parameters that made the component
    count unfit. Its cost is that it is a distribution, not a number, which is
    the point.
    """
    cur = field.astype(np.float32)
    bands = []
    for _ in range(levels):
        if min(cur.shape) < 4:
            break
        # crop to even dims first: box_down/box_up are only inverse on even
        # extents, and an odd row silently shifted the residual by one pixel.
        cur = cur[:(cur.shape[0] // 2) * 2, :(cur.shape[1] // 2) * 2]
        dn = box_down(cur)
        up = box_up(dn, cur.shape)
        bands.append(float(np.sum((cur - up) ** 2)))
        cur = dn
    bands.append(float(np.sum((cur - cur.mean()) ** 2)))
    tot = sum(bands)
    if tot <= 0:
        return [0.0] * len(bands), 0.0
    return [b / tot for b in bands], tot


def n_eff(mask: np.ndarray) -> float:
    """Mass-weighted effective component count = 1 / sum(f_i^2).

    R-1 from my ruling sec 4.1. Continuous; exactly 1.0 for one component;
    exactly k for k equal components; a fleck of relative mass f perturbs it by
    O(f^2). Emitted as a SECONDARY only, swept across floors, because it still
    depends on a binarising cut and 'how many pieces is this' is a scale
    question that one cut cannot answer.
    """
    from scipy import ndimage
    lab, k = ndimage.label(mask)
    if k == 0:
        return 0.0
    sizes = np.bincount(lab.ravel())[1:].astype(np.float64)
    f = sizes / sizes.sum()
    return float(1.0 / np.sum(f * f))


# ===========================================================================
# 2. TILE-WISE PHASE CORRELATION  (D4)
# ===========================================================================

def phase_corr(a: np.ndarray, b: np.ndarray):
    """Sub-tile displacement of b relative to a, plus the correlation peak
    height. Peak height is returned because a phase correlation on a texture-
    less tile returns a confident-looking displacement that means nothing, and
    the only defence is to gate on the peak."""
    a = a - a.mean()
    b = b - b.mean()
    win = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1])).astype(np.float32)
    FA = np.fft.rfft2(a * win)
    FB = np.fft.rfft2(b * win)
    R = FA * np.conj(FB)
    m = np.abs(R)
    R = np.where(m > 1e-8, R / np.where(m == 0, 1, m), 0)
    c = np.fft.irfft2(R, s=a.shape)
    idx = np.unravel_index(np.argmax(c), c.shape)
    peak = float(c[idx])
    dy = idx[0] - (a.shape[0] if idx[0] > a.shape[0] // 2 else 0)
    dx = idx[1] - (a.shape[1] if idx[1] > a.shape[1] // 2 else 0)
    return float(dx), float(dy), peak


def tile_flow(prev: np.ndarray, cur: np.ndarray, grid: int = 8,
              texture_floor: float = 2.0):
    """Per-tile displacement of cur relative to prev.

    texture_floor is in luma std units; tiles below it are marked NOT EVALUABLE
    rather than being given a displacement. The fraction evaluable is returned
    and is part of the reading: a background of flat untextured ground cannot
    report whether it was displaced, and that is an absence of evidence, not
    evidence of absence.
    """
    h, w = prev.shape
    th, tw = h // grid, w // grid
    disp, ok, centres = [], [], []
    for gy in range(grid):
        for gx in range(grid):
            a = prev[gy * th:(gy + 1) * th, gx * tw:(gx + 1) * tw]
            b = cur[gy * th:(gy + 1) * th, gx * tw:(gx + 1) * tw]
            evaluable = (a.std() >= texture_floor)
            if evaluable:
                dx, dy, pk = phase_corr(a, b)
            else:
                dx = dy = np.nan
                pk = 0.0
            disp.append((dx, dy, pk))
            ok.append(bool(evaluable))
            centres.append(((gx + 0.5) * tw, (gy + 0.5) * th))
    return (np.array(disp, dtype=np.float64), np.array(ok),
            np.array(centres, dtype=np.float64))


def fit_camera_model(disp, ok, centres, w, h):
    """Least-squares AFFINE camera model over the evaluable tiles.

    ⚑ THIS EXISTS BECAUSE OF A CONFOUND THAT WOULD HAVE FORGED THE ANSWER TO THE
      DISPATCH'S sec 1.1 S-4(ii) QUESTION.

    A camera DOLLY or ZOOM displaces the whole background radially about the
    frame centre. That is the identical signature to the one a cavitation /
    gravity-lensing distortion produces about the effect centre. A
    translation-only global model leaves the zoom term in the residual, where it
    reads as a large, highly coherent radial field -- i.e. it would have
    reported "the reference exhibits strong environmental distortion" on a clip
    whose camera merely pushed in.

    So the global model is fitted as v = t + A(p - c), and BOTH the translation
    t and the linear part A (divergence = zoom, curl = roll, shear) are removed
    before any residual is called environmental. The fitted divergence is
    emitted so the camera's own behaviour stays visible rather than being
    silently subtracted (no silent transformation).
    """
    if ok.sum() < 6:
        return None
    p = centres[ok] - np.array([w / 2.0, h / 2.0])
    v = disp[ok, :2]
    # design: [1, 0, px, py, 0, 0 ; 0, 1, 0, 0, px, py]
    n = p.shape[0]
    X = np.zeros((2 * n, 6))
    y = np.zeros(2 * n)
    X[0::2, 0] = 1.0
    X[0::2, 2] = p[:, 0]
    X[0::2, 3] = p[:, 1]
    X[1::2, 1] = 1.0
    X[1::2, 4] = p[:, 0]
    X[1::2, 5] = p[:, 1]
    y[0::2] = v[:, 0]
    y[1::2] = v[:, 1]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    tx, ty, a11, a12, a21, a22 = beta
    model = {"tx": float(tx), "ty": float(ty),
             "divergence": float((a11 + a22) / 2.0),   # zoom / dolly
             "curl": float((a21 - a12) / 2.0),         # camera roll
             "shear": float((a11 - a22) / 2.0)}
    # residual for every tile (nan where not evaluable)
    pa = centres - np.array([w / 2.0, h / 2.0])
    pred_x = tx + a11 * pa[:, 0] + a12 * pa[:, 1]
    pred_y = ty + a21 * pa[:, 0] + a22 * pa[:, 1]
    rx = disp[:, 0] - pred_x
    ry = disp[:, 1] - pred_y
    return model, rx, ry


# ===========================================================================
# 3. THE RUN
# ===========================================================================

@dataclass
class ClipResult:
    meta: dict
    derived: dict
    series: dict = field(default_factory=dict)
    ladder: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)


PLATE_HALFWIN = 4          # local plate spans +/- 4 frames = 9 frames @30fps


def local_plate(ring, shifts, centre_idx):
    """Motion-compensated temporal median over a short ring buffer.

    ⚑ WHY NOT A WHOLE-CLIP STATIC PLATE. The first build of this instrument used
      one, and the smoke test refuted it inside a minute: the D3 reference's
      camera PANS at ~5.4 px/frame at 720p, ~1,900 px of cumulative drift over
      374 frames -- further than the frame is wide. A whole-clip median is not a
      background of that clip; it is a smear, and every pixel reads as novel
      against it (measured novel_frac = 1.000 on the first frames, which is the
      instrument saying "everything is an effect" and meaning "I am broken").

    So the plate is LOCAL and MOTION-COMPENSATED: the +/-4 neighbouring frames
    are shifted by their cumulative integer displacement onto the centre frame's
    coordinates and the per-pixel median is taken. Static scene texture cancels;
    transient effect content survives.

    DECLARED COST OF THIS CHOICE: an effect that is perfectly steady across the
    whole 9-frame window (300 ms) cancels along with the background and becomes
    INVISIBLE to every mask-based series here. A constant, unchanging glow reads
    as zero. That is a real blind spot, it is the price of control-free masking
    on a moving camera, and it is written down rather than discovered later.
    """
    cen = ring[centre_idx]
    stack = []
    for j, f in enumerate(ring):
        dx = int(round(shifts[centre_idx][0] - shifts[j][0]))
        dy = int(round(shifts[centre_idx][1] - shifts[j][1]))
        g = np.roll(np.roll(f, dy, axis=0), dx, axis=1)
        # invalidate the wrapped border rather than letting it pollute the median
        if dy > 0:
            g[:dy] = np.nan
        elif dy < 0:
            g[dy:] = np.nan
        if dx > 0:
            g[:, :dx] = np.nan
        elif dx < 0:
            g[:, dx:] = np.nan
        stack.append(g)
    arr = np.stack(stack)
    with np.errstate(all="ignore"):
        plate = np.nanmedian(arr, axis=0).astype(np.float32)
    plate = np.where(np.isfinite(plate), plate, cen)
    return plate


def _flow_pass(path, w, h, fps, grid=8):
    """Pass 0 -- camera solve. Streams the clip and returns, per frame, the
    fitted affine camera model and the tile residual field.

    Emitted as its own pass because EVERY later series depends on it: the plate
    needs the cumulative translation, and D4 needs the residual. Solving the
    camera once and reusing it is also the only way the D4(ii) answer stays
    honest -- if the camera model were re-fitted differently for the plate and
    for the distortion test, the two could disagree and nothing would notice.
    """
    models, resids, oks, centres_out = [], [], [], None
    prev = None
    for frame in stream_frames(path, w, h, fps):
        L = luma(frame)
        if prev is None:
            models.append(None); resids.append(None); oks.append(None)
        else:
            disp, ok, centres = tile_flow(prev, L, grid=grid)
            centres_out = centres
            fit = fit_camera_model(disp, ok, centres, w, h)
            if fit is None:
                models.append(None); resids.append(None); oks.append(ok)
            else:
                model, rx, ry = fit
                models.append(model); resids.append((rx, ry)); oks.append(ok)
        prev = L
    # cumulative translation, in the frame's own pixels
    shifts = [(0.0, 0.0)]
    cx = cy = 0.0
    for m in models[1:]:
        if m is not None:
            cx += m["tx"]; cy += m["ty"]
        shifts.append((cx, cy))
    return models, resids, oks, centres_out, shifts


def analyse(path: str, label: str, w: int, h: int, fps: float,
            grid: int = 8) -> ClipResult:
    meta = probe(path)
    meta.update({"label": label, "analysis_w": w, "analysis_h": h,
                 "analysis_fps": fps, "tile_grid": grid,
                 "plate": "motion-compensated local median, +/-%d frames"
                          % PLATE_HALFWIN})

    models, resids, oks, centres, shifts = _flow_pass(path, w, h, fps, grid)
    nframes = len(models)
    meta["n_frames_analysed"] = nframes

    # ---------------------------------------------------------------- pass 1
    # DERIVE the thresholds from this clip's own noise floor. Nothing below is
    # asserted; every bar is a function of measured quantities of THIS clip and
    # every bar is also emitted as a sweep so no reading rests on one value.
    ring, ringsh, plate_samples, delta_meds = [], [], [], []
    for i, frame in enumerate(stream_frames(path, w, h, fps)):
        ring.append(luma(frame)); ringsh.append(shifts[i])
        if len(ring) > 2 * PLATE_HALFWIN + 1:
            ring.pop(0); ringsh.pop(0)
        if len(ring) == 2 * PLATE_HALFWIN + 1 and (i % 6 == 0):
            pl = local_plate(ring, ringsh, PLATE_HALFWIN)
            cen = ring[PLATE_HALFWIN]
            d = np.abs(cen - pl)
            # the frame-wide MEDIAN of |delta| is the noise floor: in any frame
            # where the effect is a minority of the picture, the median pixel is
            # background, and its residual against its own local plate is
            # exactly the clip's temporal + compression noise.
            delta_meds.append(float(np.median(d)))
            plate_samples.append(pl[::4, ::4].copy())

    noise_mad = float(np.median(delta_meds)) if delta_meds else 1.0
    plate_pool = np.concatenate([p.ravel() for p in plate_samples]) \
        if plate_samples else np.array([0.0])

    tau_spec_sweep = {f"plate_q{q}": float(np.quantile(plate_pool, q / 100.0))
                      for q in (99.0, 99.5, 99.9, 99.95, 99.99)}
    tau_spec = tau_spec_sweep["plate_q99.95"]
    tau_novelty = 6.0 * max(noise_mad, 0.5)

    derived = {
        "noise_mad_luma": noise_mad,
        "noise_derivation": (
            "median over sampled frames of the FRAME-WIDE MEDIAN of "
            "|frame - motion-compensated local plate|. The median pixel of a "
            "frame is background, so its residual is this clip's own temporal + "
            "compression noise, measured rather than assumed."),
        "tau_novelty": tau_novelty,
        "tau_novelty_k_sweep": {str(k): float(k * max(noise_mad, 0.5))
                                for k in (2, 4, 6, 8, 12)},
        "tau_spec": tau_spec,
        "tau_spec_sweep": tau_spec_sweep,
        "spec_derivation": (
            "99.95th percentile of the pooled LOCAL PLATES, i.e. the luma level "
            "this scene reaches only in its brightest 0.05% of pixels when "
            "nothing transient is happening. 'Specular' therefore means "
            "'brighter than this scene ever is at rest' -- a property of the "
            "corpus. The dispatch's asserted 99th-percentile-luma literal is "
            "NOT used; see notes for why it would have been a moving bar."),
        "plate_pool_quantiles": {f"p{q}": float(np.quantile(plate_pool, q / 100.0))
                                 for q in (50, 90, 99, 99.9)},
    }

    res = ClipResult(meta=meta, derived=derived)

    # ---------------------------------------------------------------- pass 2
    S = {k: [] for k in (
        "t", "novel_frac", "novel_mass", "spec_frac", "spec_mass",
        "band_frac", "band_total", "hue_circmean", "hue_circvar",
        "sat_mean", "val_mean", "hue_hist", "sat_hist", "val_hist",
        "frame_luma_mean", "cam_tx", "cam_ty", "cam_divergence", "cam_curl",
        "flow_tiles_evaluable", "resid_bg_median", "resid_near_median",
        "radial_coh_near", "radial_coh_far", "neff_sweep")}

    # ring holds (rgb, luma) pairs. The luma plane is computed ONCE per frame and
    # reused by the 9 plate builds it participates in. The first build recomputed
    # all 9 lumas on every frame -- ~33 MB of float32 churn per frame, which
    # drove peak RSS to 0.82 GiB against a 0.2 GiB projection. The projection was
    # not wrong about the algorithm; it was wrong about this implementation of
    # it, and the fix belongs here rather than in the projection.
    ring, ringsh, idxs = [], [], []
    for i, frame in enumerate(stream_frames(path, w, h, fps)):
        ring.append((frame.copy(), luma(frame)))
        ringsh.append(shifts[i]); idxs.append(i)
        if len(ring) > 2 * PLATE_HALFWIN + 1:
            ring.pop(0); ringsh.pop(0); idxs.pop(0)
        if len(ring) < 2 * PLATE_HALFWIN + 1:
            continue
        c = PLATE_HALFWIN
        ci = idxs[c]
        cf, L = ring[c]
        pl = local_plate([lu for (_, lu) in ring], ringsh, c)
        adelta = np.abs(L - pl)
        m = adelta >= tau_novelty
        npx = L.size

        S["t"].append(ci / fps)
        S["frame_luma_mean"].append(float(L.mean()))
        S["novel_frac"].append(float(m.mean()))
        S["novel_mass"].append(float(adelta[m].sum() / npx) if m.any() else 0.0)

        spec = L >= tau_spec
        S["spec_frac"].append(float(spec.mean()))
        S["spec_mass"].append(
            float(np.clip(L[spec] - tau_spec, 0, None).sum() / npx)
            if spec.any() else 0.0)

        bf, bt = laplacian_band_energy(adelta * m)
        S["band_frac"].append([round(x, 6) for x in bf])
        S["band_total"].append(bt / npx)

        if ci % 6 == 0:
            S["neff_sweep"].append(
                [ci, {str(f): round(n_eff(adelta >= f * max(noise_mad, 0.5)), 4)
                      for f in (2, 4, 6, 8, 12)}])

        if m.sum() >= 32:
            hh, ss, vv = rgb_to_hsv(cf)
            hm, sm, vm = hh[m], ss[m], vv[m]
            wgt = adelta[m]
            tot = max(float(wgt.sum()), 1e-9)
            ang = 2 * np.pi * hm
            C = float((wgt * np.cos(ang)).sum() / tot)
            Sn = float((wgt * np.sin(ang)).sum() / tot)
            S["hue_circmean"].append(float((np.arctan2(Sn, C) / (2 * np.pi)) % 1.0))
            S["hue_circvar"].append(1.0 - float(np.hypot(C, Sn)))
            S["sat_mean"].append(float((wgt * sm).sum() / tot))
            S["val_mean"].append(float((wgt * vm).sum() / tot))
            S["hue_hist"].append([round(float(x / tot), 6) for x in
                                  np.histogram(hm, bins=24, range=(0, 1), weights=wgt)[0]])
            S["sat_hist"].append([round(float(x / tot), 6) for x in
                                  np.histogram(sm, bins=16, range=(0, 1), weights=wgt)[0]])
            S["val_hist"].append([round(float(x / tot), 6) for x in
                                  np.histogram(vm, bins=16, range=(0, 1), weights=wgt)[0]])
        else:
            for k, n in (("hue_hist", 24), ("sat_hist", 16), ("val_hist", 16)):
                S[k].append([0.0] * n)
            for k in ("hue_circmean", "hue_circvar", "sat_mean", "val_mean"):
                S[k].append(float("nan"))

        # ---- D4, on the AFFINE-residual field ----
        mdl, rr, ok = models[ci], resids[ci], oks[ci]
        if mdl is None or rr is None or centres is None:
            for k in ("cam_tx", "cam_ty", "cam_divergence", "cam_curl",
                      "flow_tiles_evaluable", "resid_bg_median",
                      "resid_near_median", "radial_coh_near", "radial_coh_far"):
                S[k].append(float("nan"))
        else:
            rx, ry = rr
            rmag = np.hypot(rx, ry)
            if m.any():
                ys, xs = np.nonzero(m)
                ex, ey = float(xs.mean()), float(ys.mean())
            else:
                ex, ey = w / 2.0, h / 2.0
            d = np.hypot(centres[:, 0] - ex, centres[:, 1] - ey)
            diag = float(np.hypot(w, h))
            near = ok & (d <= 0.20 * diag)
            far = ok & (d > 0.35 * diag)
            S["cam_tx"].append(mdl["tx"]); S["cam_ty"].append(mdl["ty"])
            S["cam_divergence"].append(mdl["divergence"])
            S["cam_curl"].append(mdl["curl"])
            S["flow_tiles_evaluable"].append(float(ok.mean()))
            S["resid_near_median"].append(
                float(np.nanmedian(rmag[near])) if near.sum() else float("nan"))
            S["resid_bg_median"].append(
                float(np.nanmedian(rmag[far])) if far.sum() else float("nan"))

            def _radial(sel):
                if sel.sum() < 4:
                    return float("nan")
                vx, vy = rx[sel], ry[sel]
                px = centres[sel, 0] - ex
                py = centres[sel, 1] - ey
                rn = np.hypot(px, py)
                vn = np.hypot(vx, vy)
                g = (rn > 1e-6) & (vn > 1e-6) & np.isfinite(vn)
                if g.sum() < 4:
                    return float("nan")
                return float(np.mean((vx[g] * px[g] + vy[g] * py[g]) /
                                     (rn[g] * vn[g])))
            S["radial_coh_near"].append(_radial(near))
            S["radial_coh_far"].append(_radial(far))

    res.series = S
    return res


# ===========================================================================
# 4. TEMPORAL STRUCTURE -- intermittency and cycle detection
# ===========================================================================

def temporal_spectrum(x: np.ndarray, fps: float):
    """Power spectrum with its OWN noise floor, and a dominant-frequency call
    that is only made when the peak clears that floor.

    Returns dominant frequency in Hz, its prominence over the spectrum's median,
    and the floor. No fixed prominence bar is baked in: the caller sees the
    ratio and decides. Nothing here returns a verdict."""
    x = np.asarray(x, dtype=np.float64)
    good = np.isfinite(x)
    if good.sum() < 16:
        return None
    x = x[good]
    x = x - x.mean()
    if np.allclose(x, 0):
        return None
    n = len(x)
    win = np.hanning(n)
    P = np.abs(np.fft.rfft(x * win)) ** 2
    f = np.fft.rfftfreq(n, d=1.0 / fps)
    lo = f > (2.0 * fps / n)          # ignore the lowest 2 bins (trend, not cycle)
    if lo.sum() < 4:
        return None
    floor = float(np.median(P[lo]))
    k = int(np.argmax(P[lo]))
    fk = float(f[lo][k])
    pk = float(P[lo][k])
    return {"dominant_hz": fk,
            "dominant_period_s": (1.0 / fk) if fk > 0 else None,
            "peak_over_median": (pk / floor) if floor > 0 else float("inf"),
            "spectrum_median_floor": floor}


def peak_intervals(x, fps, prominence_mult=3.0):
    """Inter-event intervals on a continuous series.

    The prominence bar is DERIVED: it is prominence_mult x the MAD of the
    series' own first difference, i.e. a multiple of how much the series moves
    frame-to-frame when nothing is happening. Not a percentile of luma, which
    was the asserted literal the dispatch flagged in its own sec 4.
    """
    from scipy.signal import find_peaks
    x = np.asarray(x, dtype=np.float64)
    x = np.where(np.isfinite(x), x, 0.0)
    d = np.diff(x)
    mad = float(np.median(np.abs(d - np.median(d)))) if len(d) else 0.0
    prom = prominence_mult * max(mad, 1e-12)
    pk, _ = find_peaks(x, prominence=prom)
    if len(pk) < 2:
        return {"n_events": int(len(pk)), "prominence_bar": prom,
                "intervals_s": [], "mean_interval_s": None,
                "cv_interval": None, "events_per_s": len(pk) / (len(x) / fps)}
    iv = np.diff(pk) / fps
    return {"n_events": int(len(pk)),
            "prominence_bar": prom,
            "derivation": "prominence = %.1f x MAD(diff(series))" % prominence_mult,
            "intervals_s": [round(float(v), 4) for v in iv],
            "mean_interval_s": float(iv.mean()),
            "cv_interval": float(iv.std() / iv.mean()) if iv.mean() > 0 else None,
            "events_per_s": len(pk) / (len(x) / fps)}


if __name__ == "__main__":
    print(json.dumps(probe(sys.argv[1]), indent=2))
