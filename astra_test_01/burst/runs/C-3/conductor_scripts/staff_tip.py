# Conductor pixel reading (R-C3-16): staff tip on a registered 512 RGBA frame, full resolution.
# Staff = alpha>=128 row-runs no wider than 9 px whose centre lies > 0.10·H from the head column; tip = the topmost such run
# that belongs to a vertical chain of >= 25 staff rows (rejects hair strands); fallback: the farthest chained staff point from the torso centroid.
import sys, json, glob
import numpy as np
from PIL import Image
def tip(path):
    im = path if isinstance(path, Image.Image) else Image.open(path)
    a = np.array(im.convert('RGBA'))[..., 3] >= 128
    ys = np.where(a.any(1))[0]; sole = int(ys[-1])
    def maxrun(row):
        xs = np.where(row)[0]
        if not len(xs): return 0
        br = np.where(np.diff(xs) > 1)[0]; st = np.r_[xs[0], xs[br + 1]]; en = np.r_[xs[br], xs[-1]]
        return int((en - st + 1).max())
    top = int(next(y for y in ys if maxrun(a[y]) >= 14)); H = sole - top
    hb = a[top:top + int(0.12 * H)]; hx = np.where(hb.any(0))[0]; head_cx = float(hx.mean())
    pts = []
    for y in range(max(0, top - int(0.4 * H)), sole):
        row = a[y]; xs = np.where(row)[0]
        if not len(xs): continue
        br = np.where(np.diff(xs) > 1)[0]; starts = np.r_[xs[0], xs[br + 1]]; ends = np.r_[xs[br], xs[-1]]
        for s0, e0 in zip(starts, ends):
            if e0 - s0 + 1 <= 9 and not (top <= y <= top + 0.14 * H and abs((s0 + e0) / 2 - head_cx) <= 0.10 * H): pts.append((y, (s0 + e0) / 2))
    # column runs (near-horizontal or diagonal staffs); exclude the head/torso column band
    for x in range(a.shape[1]):
        col = a[:, x]; cy = np.where(col)[0]
        if not len(cy): continue
        br = np.where(np.diff(cy) > 1)[0]; st = np.r_[cy[0], cy[br + 1]]; en = np.r_[cy[br], cy[-1]]
        for s0, e0 in zip(st, en):
            yc = (s0 + e0) / 2
            if e0 - s0 + 1 <= 9 and not (top <= yc <= top + 0.14 * H and abs(x - head_cx) <= 0.10 * H): pts.append((yc, float(x)))
    if not pts: return dict(tip=None, reason='no thin runs', H=H, head_top=top)
    P = np.array(pts, float); rng = np.random.default_rng(0); best = None
    for _ in range(800):
        i1, i2 = rng.choice(len(P), 2, replace=False); (y1, x1), (y2, x2) = P[i1], P[i2]
        L = np.hypot(y2 - y1, x2 - x1)
        if L < 30: continue
        inl = np.abs((x2 - x1) * (P[:, 0] - y1) - (y2 - y1) * (P[:, 1] - x1)) / L <= 2.5
        m = (x2 - x1) / (y2 - y1) if abs(y2 - y1) > 1e-6 else 1e6; c = x1 - m * y1
        if best is None or inl.sum() > best[0]: best = (int(inl.sum()), m, c, inl)
    if best is None or best[0] < 40: return dict(tip=None, reason='no staff line', H=H, head_top=top)
    n, m, c, inl = best; Q = P[inl]
    if abs(m) > 1.5:   # near-horizontal: tip = the end farther from the head column
        e = Q[np.argmax(np.abs(Q[:, 1] - head_cx))]
        return dict(tip=[round(float(e[1]), 1), int(e[0])], line_inliers=int(n), slope_dx_per_dy=round(float(m), 3), H=H, head_top=top, head_cx=round(head_cx, 1), mode='horizontal-end')
    Y = Q[:, 0]; ytop = int(Y.min()); ybot = int(Y.max())
    # extend upward along the line through any alpha (ferrule/astrolabe wider than 9 px)
    y = ytop
    while y - 1 >= 0:
        x = int(round(m * (y - 1) + c))
        if 0 <= x < a.shape[1] and a[y - 1, max(0, x - 2):x + 3].any(): y -= 1
        else: break
    return dict(tip=[round(float(m * y + c), 1), int(y)], line_inliers=n, slope_dx_per_dy=round(float(m), 3), shaft_bottom=[round(float(m * ybot + c), 1), ybot], H=H, head_top=top, head_cx=round(head_cx, 1))
if __name__ == '__main__':
    print(json.dumps(default=float, obj={p.split('/')[-1]: tip(p) for p in sys.argv[1:]}, indent=0) if False else json.dumps({p.split("/")[-1]: tip(p) for p in sys.argv[1:]}, default=float))
