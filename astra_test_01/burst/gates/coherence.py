"""Report regional carried motion versus redrawing; never a shipping verdict.

All translation trials use the SAME interior window (no changing-overlap
reward). RGB is composited by motion_map. The ±6 native-pixel block search
is an instrument only and never alters delivered art. No seam pair is added.
"""
import numpy as np
from gates.common import result
from oracle.motion_map import load_frames, alpha_box, region_boxes

SEARCH_RADIUS_PX = 6
NOISE_MAD = 1.0  # one 8-bit RGB level; provisional quantization/noise floor
CARRIED_RESIDUAL_RATIO = 0.5


def evaluate(frames_dir, regions):
    """regions: named XYXY boxes, names from motion_map, or None for all bands."""
    frames = load_frames(frames_dir)
    if len(frames) < 2:
        raise ValueError('coherence requires at least two frames')
    shape = frames[0].shape
    if regions is None or not isinstance(regions, dict):
        bands = region_boxes(alpha_box(frames_dir), shape)
        regions = bands if regions is None else {name: bands[name] for name in regions}
    if not regions:
        raise ValueError('at least one region required')
    rows = {}
    radius = SEARCH_RADIUS_PX
    shifts = sorted(((dx, dy) for dy in range(-radius, radius+1)
                     for dx in range(-radius, radius+1)),
                    key=lambda p: (abs(p[0])+abs(p[1]), p))
    for name, bounds in regions.items():
        if (len(bounds) != 4 or any(isinstance(v, bool) or not isinstance(v, (int, np.integer)) for v in bounds)):
            raise ValueError('regions require integer XYXY bounds')
        x0, y0, x1, y1 = bounds
        if not (0 <= x0 < x1 <= shape[1] and 0 <= y0 < y1 <= shape[0]):
            raise ValueError('region outside canvas')
        # Keep all the named region except at canvas boundaries; samples in B
        # may come from its ±6 halo, avoiding clipping a moving region edge.
        x0, y0 = max(radius, x0), max(radius, y0)
        x1, y1 = min(shape[1]-radius, x1), min(shape[0]-radius, y1)
        if x1 <= x0 or y1 <= y0:
            rows[name] = dict(classification=None, reason='no fixed search interior', pairs=[])
            continue
        pairs = []
        for i, (a, b) in enumerate(zip(frames, frames[1:])):
            core = a[y0:y1, x0:x1].astype(np.float32)
            raw = float(np.mean(abs(core-b[y0:y1, x0:x1])))
            best, offset = raw, (0, 0)
            for dx, dy in shifts:
                residual = float(np.mean(abs(core-b[y0+dy:y1+dy, x0+dx:x1+dx])))
                if residual < best:
                    best, offset = residual, (dx, dy)
            carried = raw < NOISE_MAD or best <= CARRIED_RESIDUAL_RATIO*raw
            pairs.append(dict(pair=[i, i+1], raw_mad=raw, residual_mad=best,
                translation_xy=list(offset), classification='carried' if carried else 'redrawn'))
        worst = max(pairs, key=lambda p: p['residual_mad'])
        rows[name] = dict(max_residual_mad=worst['residual_mad'],
            raw_mad_at_max_residual=worst['raw_mad'], max_raw_mad=max(p['raw_mad'] for p in pairs),
            worst_pair=worst['pair'], bounds=list(bounds), search_core=[x0,y0,x1,y1],
            classification='carried' if all(p['classification']=='carried' for p in pairs) else 'redrawn', pairs=pairs)
    report = result('coherence', frames_dir, value=rows, passed=None,
        unit='rgb_mad', notes='Report replaces LOCK/MOTION interpretation; fixed support; no verdict.')
    report.update(
        threshold=dict(residual_ratio=CARRIED_RESIDUAL_RATIO, noise_mad=NOISE_MAD,
                       search_radius_px=radius), op='report', unit='rgb_mad',
        notes='Report replaces LOCK/MOTION interpretation; worst consecutive residual, fixed support; no verdict.')
    return report
