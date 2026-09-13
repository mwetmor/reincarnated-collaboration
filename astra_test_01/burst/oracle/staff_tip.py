"""Full-resolution alpha-only staff line instrument; deterministic RANSAC.

Coordinates are pixel centres on the input canvas. Alpha >=128 is foreground.
Slope is dy/dx (None for a vertical line or an unevaluable input); reason
separates those cases. No resizing, colour heuristics or per-cell calibration.
"""
import numpy as np


def _runs(row):
    edges = np.flatnonzero(np.diff(np.r_[False, row, False].astype(np.int8)))
    return list(zip(edges[::2], edges[1::2]))


def tip(rgba):
    """Return {tip, reason, line_inliers, slope}; null tip means unevaluable."""
    result = dict(tip=None, reason='', line_inliers=0, slope=None)
    a = np.asarray(rgba)
    if a.ndim != 3 or a.shape[2] != 4 or a.dtype != np.uint8:
        raise ValueError('rgba must be an H x W x 4 uint8 array or RGBA image')
    mask = a[:, :, 3] >= 128
    yy, xx = np.nonzero(mask)
    if not len(xx):
        return dict(result, reason='empty_alpha')
    height = int(yy.max()-yy.min()+1)
    head = None
    row_runs = []
    for y, row in enumerate(mask):
        runs = _runs(row)
        row_runs.append(runs)
        broad = [(lo, hi) for lo, hi in runs if hi-lo >= 14]
        if head is None and broad:
            lo, hi = max(broad, key=lambda r: r[1]-r[0])
            head = ((lo+hi-1)/2, y)
    if head is None:
        return dict(result, reason='no_head_run_ge_14')
    hx, hy = head
    points = []
    def add(x, y):
        if hy <= y <= hy+0.14*height and abs(x-hx) <= 0.10*height:
            return
        points.append((x, y))
    for y, runs in enumerate(row_runs):
        for lo, hi in runs:
            if hi-lo <= 9:
                for x in range(lo, hi):
                    add(x, y)
    for x, column in enumerate(mask.T):
        for lo, hi in _runs(column):
            if hi-lo <= 9:
                for y in range(lo, hi):
                    add(x, y)
    points = np.unique(np.asarray(points, dtype=float).reshape(-1, 2), axis=0)
    if len(points) < 40:
        return dict(result, reason='fewer_than_40_thin_points')
    rng = np.random.default_rng(0)
    best, best_key = None, (-1, -1.0)
    for i, j in rng.integers(0, len(points), size=(2400, 2)):
        d = points[j]-points[i]
        norm = np.linalg.norm(d)
        if norm < 20:
            continue
        d /= norm
        delta = points-points[i]
        inliers = np.abs(delta[:, 0]*d[1]-delta[:, 1]*d[0]) <= 2.5
        n = int(inliers.sum())
        span = float(np.ptp(delta[inliers]@d))
        if (n, span) > best_key:
            best, best_key = inliers, (n, span)
    if best is None or best_key[0] < 40:
        return dict(result, reason='no_line_with_40_inliers', line_inliers=max(0, best_key[0]))
    for _ in range(3):
        centre = points[best].mean(axis=0)
        _, _, vh = np.linalg.svd(points[best]-centre, full_matrices=False)
        d = vh[0]
        delta = points-centre
        best = np.abs(delta[:, 0]*d[1]-delta[:, 1]*d[0]) <= 2.5
    count = int(best.sum())
    if count < 40:
        return dict(result, reason='refined_line_below_40_inliers', line_inliers=count)
    selected = points[best]
    t = (selected-centre)@d
    if abs(d[1]) < 0.20:
        ends = [centre+t.min()*d, centre+t.max()*d]
        end = max(ends, key=lambda p: abs(p[0]-hx))
        direction = d if np.dot(end-centre, d) > 0 else -d
    else:
        direction = d if d[1] < 0 else -d
        end = centre+(t.min() if d[1] > 0 else t.max())*d
    # Follow contiguous foreground in half-pixel steps, perpendicular tolerance
    # of one pixel permits raster stair steps without jumping gaps along staff.
    normal = np.array([-direction[1], direction[0]])
    last = end.copy()
    for step in np.arange(0, 2*max(mask.shape), 0.5):
        p = end+direction*step
        hits = []
        for offset in (0, -0.5, 0.5, -1, 1):
            q = np.rint(p+normal*offset).astype(int)
            x, y = q
            if 0 <= y < mask.shape[0] and 0 <= x < mask.shape[1] and mask[y, x]:
                hits.append(q)
        if not hits:
            break
        last = hits[0]
    return dict(tip=[int(round(v)) for v in last], reason='ok', line_inliers=count,
                slope=None if abs(d[0]) < 1e-9 else float(d[1]/d[0]))
