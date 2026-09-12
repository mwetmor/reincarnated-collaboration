"""Median-difference energy and geometric profile tracking; art is never transformed.

Calibration: tau=12 is a provisional max-RGB difference in 0..255 units,
not a candidate-fitted threshold. Alpha support is >=128. Native-alpha and
green plates use the frozen matte with detached components retained. Their
transparent RGB is zeroed, and the clip-wide median RGB of those matted images
is the common composite colour (normally black for sparse sprite canvases).
Opaque reference clips retain their original RGB background.

Camera shifts use half-size luminance phase correlation, subpixel parabolic
peak interpolation, converted back to source pixels. Frame zero uses the first
forward pair; subsequent frames use their preceding pair. Thus a continuously
panning clip marks every frame, including frame zero. No pan correction occurs.
"""
import re
from pathlib import Path

import numpy as np
from PIL import Image

from gates.matte import remove_chroma_key


def frame_paths(directory):
    paths = [p for p in Path(directory).glob('*.png')
             if re.search(r'\d+$', p.stem)]
    paths.sort(key=lambda p: (int(re.search(r'(\d+)$', p.stem).group()), p.name))
    if not paths:
        raise ValueError('no numbered PNG frames')
    return paths


def _matted(path):
    with Image.open(path) as image:
        a = np.array(image.convert('RGBA'))
        border = np.concatenate((a[:10, :, :3].reshape(-1, 3),
                                 a[-10:, :, :3].reshape(-1, 3),
                                 a[:, :10, :3].reshape(-1, 3),
                                 a[:, -10:, :3].reshape(-1, 3)))
        keyed = np.mean((border[:, 1] > 210) & (border[:, 0] < 45) &
                        (border[:, 2] < 45)) >= .95
        alpha = 'A' in image.getbands() and np.any(a[..., 3] < 255)
        if alpha or keyed:
            a = np.array(remove_chroma_key(image, preserve_particles=True))
            a[a[..., 3] == 0, :3] = 0
            return a, True
        return a, False


def load_frames(directory):
    """Read naturally numbered PNGs and return RGB uint8 arrays of one size."""
    loaded = [_matted(p) for p in frame_paths(directory)]
    if len({a.shape for a, _ in loaded}) != 1:
        raise ValueError('frame dimensions differ')
    if len({m for _, m in loaded}) != 1:
        raise ValueError('mixed opaque and alpha/keyed clip')
    if not loaded[0][1]:
        return [a[..., :3].copy() for a, _ in loaded]
    # Median over all matted pixels, not foreground-only median or green plate.
    rgb = np.stack([a[..., :3] for a, _ in loaded])
    colour = np.median(rgb.reshape(-1, 3), axis=0)
    return [np.rint(a[..., :3] * (a[..., 3:4] / 255.) +
                    colour * (1 - a[..., 3:4] / 255.)).astype(np.uint8)
            for a, _ in loaded]


def alpha_box(directory):
    """Union of alpha>=128 support over the complete sprite clip."""
    boxes = []
    for path in frame_paths(directory):
        a, matted = _matted(path)
        if not matted:
            raise ValueError('--ours requires native alpha or a green plate')
        if a.shape != (512, 512, 4):
            raise ValueError('--ours requires registered 512x512 frames')
        y, x = np.where(a[..., 3] >= 128)
        if not x.size:
            raise ValueError('empty alpha support')
        boxes.append((int(x.min()), int(y.min()), int(x.max()+1), int(y.max()+1)))
    b = np.array(boxes)
    return [int(b[:, 0].min()), int(b[:, 1].min()),
            int(b[:, 2].max()), int(b[:, 3].max())]


def _validate(frames):
    if not len(frames):
        raise ValueError('empty clip')
    shape = frames[0].shape
    if len(shape) != 3 or shape[2] != 3 or min(shape[:2]) < 4:
        raise ValueError('frames must be HxWx3 RGB')
    if any(f.dtype != np.uint8 or f.shape != shape for f in frames):
        raise ValueError('frames must be same-sized uint8 RGB')


def camera_shift(frames):
    """Return signed [dx,dy] per frame in original pixels; norm>1 is VOID."""
    _validate(frames)
    h, w = frames[0].shape[:2]
    size = (max(2, w//2), max(2, h//2))
    small = []
    for frame in frames:
        a = np.array(Image.fromarray(frame).resize(size, Image.Resampling.BOX),
                     dtype=float) @ np.array([.2126, .7152, .0722])
        small.append(a - a.mean())
    shifts = []
    for a, b in zip(small, small[1:]):
        if np.max(np.abs(a-b)) < 1e-9 or min(np.std(a), np.std(b)) < 1e-9:
            shifts.append([0., 0.])
            continue
        cross = np.fft.fft2(b) * np.conj(np.fft.fft2(a))
        denom = np.abs(cross)
        cross = np.divide(cross, denom, out=np.zeros_like(cross), where=denom>1e-9)
        corr = np.fft.ifft2(cross).real
        peak = np.unravel_index(np.argmax(corr), corr.shape)
        displacement = []
        for axis, p in enumerate(peak):
            n = corr.shape[axis]
            left, right = list(peak), list(peak)
            left[axis], right[axis] = (p-1)%n, (p+1)%n
            v0, v1, v2 = corr[tuple(left)], corr[peak], corr[tuple(right)]
            d = v0 - 2*v1 + v2
            offset = float(np.clip(.5*(v0-v2)/d, -.5, .5)) if abs(d)>1e-12 else 0.
            signed = p if p <= n//2 else p-n
            displacement.append((signed + offset) * (h/n if axis == 0 else w/n))
        shifts.append([displacement[1], displacement[0]])
    return [shifts[0].copy()] + shifts if shifts else [[0., 0.]]


def region_boxes(box, shape):
    if (len(box) != 4 or any(isinstance(x, (bool, np.bool_)) or
                            not isinstance(x, (int, np.integer)) for x in box)):
        raise ValueError('box must contain four integer XYXY coordinates')
    x0, y0, x1, y1 = map(int, box)
    if not (0 <= x0 < x1 <= shape[1] and 0 <= y0 < y1 <= shape[0]):
        raise ValueError('box must be nonempty and inside canvas')
    height, width = y1-y0, x1-x0
    rows = [y0 + int(round(f*height)) for f in (0, .18, .45, .60, .85, 1)]
    names = ('head', 'shoulders_chest', 'hips', 'legs', 'feet')
    regions = {name: [x0, rows[i], x1, rows[i+1]] for i, name in enumerate(names)}
    arm_width = int(round(.22*width))
    regions['arms_left'] = [x0, rows[1], x0+arm_width, rows[3]]
    regions['arms_right'] = [x1-arm_width, rows[1], x1, rows[3]]
    if any(b[0] >= b[2] or b[1] >= b[3] for b in regions.values()):
        raise ValueError('box too small for region bands')
    return regions


def _band_profiles(frames, box, band, axis):
    """RGB profiles of band content and its temporal-median image."""
    _validate(frames)
    regions = region_boxes(box, frames[0].shape)
    bounds = regions[band] if isinstance(band, str) else region_boxes(box, frames[0].shape)[
        next(name for name, bounds in regions.items() if bounds == list(band))]
    x0, y0, x1, y1 = bounds
    crop = np.stack([f[y0:y1, x0:x1] for f in frames])
    reference = np.median(crop, axis=0).mean(axis=axis)
    profiles = crop.mean(axis=axis+1)
    return profiles, reference, bounds


def _profile_shift(profile, reference, limit):
    """Least-squares RGB-gradient translation, subpixel parabolic minimum.

    A fixed interior reference window is compared at every trial shift, so
    changing overlap cannot reward large shifts. Positive means down/right.
    No displacement multiplier or synthetic amplitude correction is applied.
    """
    a, b = np.diff(profile, axis=0), np.diff(reference, axis=0)
    limit = min(int(limit), (len(b)-3)//2)
    if limit < 1 or np.max(np.abs(b)) < 1e-9:
        return 0., False
    core = b[limit:-limit]
    errors = [float(np.mean((a[limit+d:len(a)-limit+d]-core)**2))
              for d in range(-limit, limit+1)]
    k = int(np.argmin(errors))
    offset = 0.
    if 0 < k < len(errors)-1:
        left, center, right = errors[k-1:k+2]
        denom = left-2*center+right
        if denom > 1e-12:
            offset = float(np.clip(.5*(left-right)/denom, -.5, .5))
    return float(k-limit+offset), k in (0, len(errors)-1)


def band_shift_y(frames, box, band='head'):
    """Band-content vertical translation relative to the median image, px / H.

    RGB row-profile gradients reject uniform light offsets. A static band
    retains null displacement for compatibility (no observed moving feature).
    Search radius is 20% of the band height; saturation is explicitly reported.
    """
    profiles, reference, bounds = _band_profiles(frames, box, band, 1)
    h = box[3]-box[1]
    if np.max(np.ptp(profiles, axis=0)) < 1e-9:
        shifts, clipped = [None]*len(frames), [False]*len(frames)
    else:
        values = [_profile_shift(p, reference, max(1, int(.2*len(reference))))
                  for p in profiles]
        shifts, clipped = map(list, zip(*values))
    return {'dy_px': shifts, 'dy_H': [v/h if v is not None else None for v in shifts],
            'search_limit_frames': [i for i, v in enumerate(clipped) if v],
            'band_box': bounds}


def band_edges_x(frames, box, band='shoulders_chest'):
    """Track left/right apparent contour profiles against the median image.

    Each half-band's strongest mean RGB spatial edge anchors a local template.
    Translation of that template measures displacement, not changed support.
    On textured opaque backgrounds these are apparent contour estimates, not
    semantic segmentation; edge anchors and search saturation remain auditable.
    """
    profiles, reference, bounds = _band_profiles(frames, box, band, 0)
    gradient = np.linalg.norm(np.diff(reference, axis=0), axis=1)
    half = len(gradient)//2
    radius = max(3, int(round(.12*len(reference))))
    edges, anchors, saturation = [], [], []
    for start, stop in ((0, half), (half, len(gradient))):
        if stop <= start or gradient[start:stop].max() < 1e-9:
            edges.append([None]*len(frames)); anchors.append(None); saturation.append([])
            continue
        anchor = start+int(np.argmax(gradient[start:stop]))
        lo, hi = max(0, anchor-radius), min(len(reference), anchor+radius+2)
        shifts = [_profile_shift(p[lo:hi], reference[lo:hi], max(1, radius//2))
                  for p in profiles]
        edges.append([float(bounds[0]+anchor+1+d) for d, _ in shifts])
        anchors.append(float(bounds[0]+anchor+1))
        saturation.append([i for i, (_, clipped) in enumerate(shifts) if clipped])
    left, right = edges
    width = [r-l if l is not None and r is not None else None for l, r in zip(left, right)]
    h = box[3]-box[1]
    return {'left_px': left, 'right_px': right, 'width_px': width,
            'left_H': [v/h if v is not None else None for v in left],
            'right_H': [v/h if v is not None else None for v in right],
            'width_H': [v/h if v is not None else None for v in width],
            'median_edge_anchors_px': anchors,
            'search_limit_frames': {'left': saturation[0], 'right': saturation[1]},
            'band_box': bounds}


def _control_box(box, shape, control_box):
    if control_box is not None:
        region_boxes(control_box, shape)
        if (control_box[2]-control_box[0], control_box[3]-control_box[1]) != (box[2]-box[0], box[3]-box[1]):
            raise ValueError('control_box must match figure box size')
        if (max(box[0], control_box[0]) < min(box[2], control_box[2]) and
                max(box[1], control_box[1]) < min(box[3], control_box[3])):
            raise ValueError('control_box must not overlap figure box')
        return list(control_box)
    step = int(round(1.2*(box[2]-box[0])))
    for dx in (step, -step):
        candidate = [box[0]+dx, box[1], box[2]+dx, box[3]]
        if 0 <= candidate[0] and candidate[2] <= shape[1]:
            return candidate
    return None


def motion_energy(frames, box, tau=12, control_box=None):
    """Median-difference energy plus geometric displacement and control energy.

    Contamination pools all frame/region energies equally, including arm bands.
    Zero/zero is 0; positive/zero is JSON null with an explicit infinite-ratio
    flag. An unavailable control is null and reported, never silently clean.
    Original changed-pixel proxies are retained with an _extent suffix.
    """
    _validate(frames)
    if not np.isfinite(tau) or not 0 <= tau <= 255:
        raise ValueError('tau must be finite in 0..255')
    regions = region_boxes(box, frames[0].shape)
    h = box[3]-box[1]
    control_box = _control_box(box, frames[0].shape, control_box)
    controls = region_boxes(control_box, frames[0].shape) if control_box else {}
    control_energy = {name: [] for name in controls}
    # Bound median workspace for full-resolution references and long clips.
    median = np.empty(frames[0].shape, dtype=np.float32)
    for row in range(0, median.shape[0], 32):
        stack = np.stack([f[row:row+32] for f in frames])
        median[row:row+32] = np.median(stack, axis=0, overwrite_input=True)
    energy = {name: [] for name in regions}
    head, chest, tip = [], [], []
    for frame in frames:
        changed = np.max(np.abs(frame.astype(float)-median), axis=2) > tau
        for name, (x0, y0, x1, y1) in controls.items():
            control_energy[name].append(float(changed[y0:y1, x0:x1].mean()))
        for name, (x0, y0, x1, y1) in regions.items():
            local = changed[y0:y1, x0:x1]
            energy[name].append(float(local.mean()))
            yy, xx = np.where(local)
            if name == 'head':
                head.append(float(yy.mean()+y0) if yy.size else None)
            elif name == 'shoulders_chest':
                chest.append(float(xx.max()-xx.min()+1)/h if xx.size else 0.)
        top = max(0, box[1]-int(np.floor(.5*h)))
        yy = np.where(changed[top:box[1]])[0]
        tip.append(float(yy.min()+top)/h if yy.size else None)
    head_shift = band_shift_y(frames, box, 'head')
    chest_edges = band_edges_x(frames, box, 'shoulders_chest')
    figure_median = float(np.median(list(energy.values())))
    control_median = float(np.median(list(control_energy.values()))) if controls else None
    infinite = control_median is not None and control_median > 0 and figure_median == 0
    contamination = (control_median/figure_median if figure_median else
                     (0. if control_median == 0 else None)) if controls else None
    return {'box': list(map(int, box)), 'height': int(h), 'regions': regions,
            'tau': float(tau), 'energy_by_region': energy,
            'head_dy_px': head_shift['dy_px'], 'head_dy_H': head_shift['dy_H'],
            'chest_dw_H': chest_edges['width_H'],
            'head_dy_px_extent': head,
            'head_dy_H_extent': [v/h if v is not None else None for v in head],
            'chest_dw_H_extent': chest, 'weapon_tip_H': tip,
            'head_shift': head_shift, 'chest_edges': chest_edges,
            'control_box': control_box, 'control_regions': controls,
            'control_energy': control_energy, 'contamination': contamination,
            'contamination_infinite': infinite, 'figure_energy_median': figure_median,
            'control_energy_median': control_median,
            'estimator': 'median RGB profile-gradient translation; local left/right edge templates',
            'estimator_caveat': 'Apparent edges on textured backgrounds; no semantic segmentation. '
                                'Search-limit frames can underestimate displacement.'}
