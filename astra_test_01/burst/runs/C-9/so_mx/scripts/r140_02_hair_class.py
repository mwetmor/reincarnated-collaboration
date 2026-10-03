# R-C9-140: classify the body's UV islands as HAIR (island-level: the atlas is painted per island, and a hair island is
# dark (mean value < VMAX) in the head zone, or one of the braid's islands behind the back) -> a vertex mask.
#   python3 r140_02_hair_class.py <head.npz> <islands.npy> <out_mask.npy> [--png sheet]
import sys, numpy as np
from PIL import Image
d = np.load(sys.argv[1]); V, hsv = d['V'], d['hsv']; lab = np.load(sys.argv[2])
VMAX = 0.50
hair = np.zeros(len(V), bool); rows = []
for i in np.unique(lab):
    s = lab == i
    y0, y1 = V[s, 1].min(), V[s, 1].max(); z1 = V[s, 2].max(); x0, x1 = V[s, 0].min(), V[s, 0].max(); v = hsv[s, 2].mean()
    head = y1 > 1.30 and y0 > 1.25 and v < VMAX
    braid = z1 < -0.05 and y0 > 0.95 and y1 < 1.46 and max(abs(x0), abs(x1)) < 0.08 and v < 0.60
    if head or braid:
        hair[s] = True; rows.append((int(i), int(s.sum()), 'head' if head else 'braid'))
np.save(sys.argv[3], hair)
print('hair islands', len(rows), 'verts', int(hair.sum()), rows)
if '--png' in sys.argv:
    sel = V[:, 1] > 0.95
    def view(ax, flip):
        img = np.full((800, 600, 3), 255, np.uint8); P = V[sel]; H = hair[sel]; val = hsv[sel, 2]
        u = ((P[:, ax] * flip + 0.3) / 0.6 * 599).astype(int); vv = ((1.75 - P[:, 1]) / 0.8 * 799).astype(int)
        depth = P[:, 2 if ax == 0 else 0] * (flip if ax == 0 else -flip)
        col = np.where(H[:, None], np.array([220, 30, 30]) * val[:, None] + 30, np.stack([val * 255] * 3, 1)).astype(np.uint8)
        for i in np.argsort(depth):
            if 0 <= u[i] < 600 and 0 <= vv[i] < 800: img[vv[i], u[i]] = col[i]
        return img
    Image.fromarray(np.hstack([view(0, 1), view(2, 1), view(0, -1), view(2, -1)])).save(sys.argv[sys.argv.index('--png') + 1])
# BRAID TIP: the braid's last ~10 cm (and its tie) are painted on the big torso islands, so they are grown vertex-wise from the
# braid along the welded mesh, through vertices standing BEHIND the back (the tube), never onto the back itself
if '--grow-tip' in sys.argv:
    from scipy.sparse import coo_matrix
    IDX = d['IDX']; key = np.round(V / 1e-5).astype(np.int64); _, wid = np.unique(key, axis=0, return_inverse=True); wid = wid.ravel()
    m = wid.max() + 1; T = wid[IDX]
    A = coo_matrix((np.ones(T.size), (np.r_[T[:, 0], T[:, 1], T[:, 2]], np.r_[T[:, 1], T[:, 2], T[:, 0]])), shape=(m, m)).tocsr()
    A = A + A.T
    hw = np.zeros(m, bool); hw[wid[hair]] = True
    Vw = np.zeros((m, 3)); Vw[wid] = V
    zback = float(sys.argv[sys.argv.index('--grow-tip') + 1])
    ok = (Vw[:, 2] < zback) & (np.abs(Vw[:, 0]) < 0.07) & (Vw[:, 1] > 0.90) & (Vw[:, 1] < 1.10)
    front = hw.copy(); n0 = hw.sum()
    for it in range(200):
        nb = (A @ front.astype(float)) > 0
        new = nb & ok & ~hw
        if not new.any(): break
        hw |= new; front = new
    hair2 = hw[wid]
    print('braid tip grown: +%d welded verts (%d -> %d), z < %.3f; tip lowest y %.3f' % (hw.sum() - n0, n0, hw.sum(), zback, V[hair2 & ~hair, 1].min() if (hair2 & ~hair).any() else -1))
    np.save(sys.argv[3], hair2)
