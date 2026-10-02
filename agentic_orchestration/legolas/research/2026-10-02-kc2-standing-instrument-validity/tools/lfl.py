"""Like-for-like: the v3.10 oracle's bodies through the referent's Lap H-2 standing pipeline.

Pre-registered at collab 1865b7a92 (PREREGISTRATION.md § 1). Layers N1, N2, L0, L1, L1g, L2, L3.
The referent's code (d1b.world / d1b.track / d1b.kinematics / bars.find_bars / extract HUD filter) is imported
UNCHANGED from the Lap H-2 method directory (copied; only file paths differ).

usage: python3 lfl.py <layer> <salt_a-salt_b> <out.json> [key=value ...]
  sensitivity keys: S (gpx/m, 122), OFF (plate offset px, 115), MIRROR (0/1), ORDER (asc/desc)
"""
import sys, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', 'ref')
sys.path.insert(0, REF)
import d1b                      # noqa: E402  (the referent's kinematics, unchanged)
import bars                     # noqa: E402  (the referent's plate detector, unchanged)

K = 0.537
FPS = 60.0
EDGES = [0, 100, 150, 220, 300, 400, 600, 900, 1400]
HUD = [(1330, 0, 1920, 262), (0, 0, 1920, 58), (0, 980, 1920, 1080), (0, 0, 300, 120)]   # extract.py


def in_hud(x, y):
    return any(x0 <= x <= x1 and y0 <= y <= y1 for (x0, y0, x1, y1) in HUD)


def load_rows():
    return np.load(os.path.join(HERE, '..', 'cap', 'legB_rows.npy'))


# ── per wave: 60 fps resampling of the oracle (body pre-step positions + player at the same instant) ─────────
def resample(B):
    """returns frame times, player xy per frame, and per frame a list of (body_id, x, y, hp)."""
    ticks = np.unique(B[:, 2]).astype(int)
    k0, k1 = ticks.min(), ticks.max()
    per = B[0, 3] / B[0, 2]
    # player per tick
    pl = {}
    for r in B:
        pl[int(r[2])] = (r[8], r[9])
    # bodies per tick
    bod = {}
    for r in B:
        bod.setdefault(int(r[4]), {})[int(r[2])] = (r[6], r[7], r[10])
    t0, t1 = k0 * per, k1 * per
    nfr = int(math.floor((t1 - t0) * FPS)) + 1
    ft = np.round(t0 + np.arange(nfr) / FPS, 4)
    kk = sorted(pl)
    kt = np.array(kk) * per
    pxs = np.array([pl[k][0] for k in kk]); pys = np.array([pl[k][1] for k in kk])
    PX = np.interp(ft, kt, pxs); PY = np.interp(ft, kt, pys)
    frames = [[] for _ in range(nfr)]
    for bid, d in bod.items():
        ks = sorted(d)
        for a, b in zip(ks[:-1], ks[1:]):
            if b != a + 1:
                continue
            ta, tb = a * per, b * per
            i0 = int(math.ceil((ta - t0) * FPS - 1e-9)); i1 = int(math.floor((tb - t0) * FPS - 1e-9))
            xa, ya, ha = d[a]; xb, yb, hb = d[b]
            for i in range(max(i0, 0), min(i1, nfr - 1) + 1):
                u = (ft[i] - ta) / (tb - ta)
                frames[i].append((bid, xa + u * (xb - xa), ya + u * (yb - ya), ha + u * (hb - ha)))
    return ft, PX, PY, frames


# ── N1 / N2: no detector, no tracking; the referent velocity rule on true body positions ───────────────────
def layer_N(ft, PX, PY, frames, S, OFF, MIRROR, plate_range):
    sgn = -1.0 if MIRROR else 1.0
    seq = {}
    for i, fr in enumerate(frames):
        for (bid, x, y, h) in fr:
            seq.setdefault(bid, []).append((i, x, y))
    cnt = np.zeros((8, 2), int)
    ker = np.ones(15) / 15
    for bid, s in seq.items():
        s = np.array(s)
        # contiguous runs of frames
        br = np.where(np.diff(s[:, 0]) != 1)[0] + 1
        for seg in np.split(s, br):
            if len(seg) < 17:
                continue
            idx = seg[:, 0].astype(int); t = ft[idx]
            gx = seg[:, 1] * S; gy = sgn * seg[:, 2] * S             # ground px (world)
            sx = np.convolve(gx, ker, 'valid'); sy = np.convolve(gy, ker, 'valid'); st = t[7:len(t) - 7]
            v = np.hypot(np.gradient(sx, st), np.gradient(sy, st))
            ii = idx[7:len(idx) - 7]
            bx = seg[7:len(seg) - 7, 1]; by = seg[7:len(seg) - 7, 2]
            dx = (bx - PX[ii]) * S; dyg = sgn * (by - PY[ii]) * S
            if plate_range:
                r = np.hypot(dx, (dyg * K - OFF) / K)
            else:
                r = np.hypot(dx, dyg)
            b = np.digitize(r, EDGES) - 1
            for q in range(len(v)):
                if 0 <= b[q] < 8:
                    cnt[b[q], 0 if v[q] >= 50.0 else 1] += 1
    return cnt


# ── plate projection ───────────────────────────────────────────────────────────────────────────────────
def project(PX, PY, i, x, y, S, OFF, MIRROR):
    sgn = -1.0 if MIRROR else 1.0
    X = 960.0 + S * (x - PX[i])
    Yg = 544.0 + sgn * S * K * (y - PY[i])
    return X, Yg - OFF


class Noise:
    """the referent's transient anchor residuals (screen px), drawn as contiguous streams per band (L1g/L3)."""

    def __init__(self, seed):
        P = np.load(os.path.join(REF, 'resid_pools.npz'))
        self.pool = [P[f'b{i}'] for i in range(8)]
        self.rng = np.random.default_rng(seed)
        self.ptr = {}

    def draw(self, bid, band):
        if band < 0 or band >= 8:
            band = 7
        st = self.ptr.get(bid)
        if st is None or st[0] != band:
            st = [band, int(self.rng.integers(0, len(self.pool[band])))]
        p = self.pool[band]
        e = p[st[1] % len(p)]
        st[1] += 1
        self.ptr[bid] = st
        return float(e[0]), float(e[1])


def plate_band(X, Ytop_bar, S):
    """the referent's r for a plate at screen (X, y): plate anchor to the player's ground point, in gpx."""
    return int(np.digitize(math.hypot(X - 960.0, (Ytop_bar - 544.0) / K), EDGES) - 1)


# ── detector layers: produce the referent's plate rows (t, 0, x_anchor, y, w, txt) ───────────────────────────
def detect_ideal(ft, PX, PY, frames, S, OFF, MIRROR, minw, noise):
    rows = []
    for i, fr in enumerate(frames):
        for (bid, x, y, h) in fr:
            X, Yb = project(PX, PY, i, x, y, S, OFF, MIRROR)
            if noise is not None:
                ex, ey = noise.draw(bid, plate_band(X, Yb, S))
                X += ex; Yb += ey
            w = int(round(72 * max(0.0, min(1.0, h))))
            xl = int(round(X - 36)); yy = float(int(round(Yb - 1.5)) + 1.5)
            if minw and w < 14:
                continue
            if not (0 <= xl and xl + max(w, 1) - 1 < 1920 and 60 <= yy < 975):
                continue
            if in_hud(xl + (max(w, 1) - 1) / 2.0, yy):
                continue
            rows.append((ft[i], 0, xl + 36, yy, w, 300))
    return rows


RED = np.array([200, 30, 30], np.uint8); DARK = np.array([20, 20, 20], np.uint8)
WHITE = np.array([240, 240, 240], np.uint8); GREEN = np.array([120, 240, 35], np.uint8)
GLYPH = np.array([(c % 7) < 3 for c in range(96)])


def _paint(img, xl, ytop, w, fill):
    H, Wd = img.shape[:2]
    y0, y1 = max(ytop - 1, 0), min(ytop + 4, H)
    x0, x1 = max(xl - 1, 0), min(xl + 73, Wd)
    if y0 < y1 and x0 < x1:
        img[y0:y1, x0:x1] = DARK
    if w > 0:
        y0, y1 = max(ytop, 0), min(ytop + 3, H)
        x0, x1 = max(xl, 0), min(xl + w, Wd)
        if y0 < y1 and x0 < x1:
            img[y0:y1, x0:x1] = fill
    xc = xl + 36
    ty0, ty1 = max(ytop - 31, 0), min(ytop - 20, H)
    if ty0 < ty1:
        cols = np.arange(xc - 48, xc + 48)
        ok = (cols >= 0) & (cols < Wd) & GLYPH
        img[ty0:ty1, cols[ok]] = WHITE


def detect_render(ft, PX, PY, frames, S, OFF, MIRROR, noise, order='asc'):
    rows = []
    for i, fr in enumerate(frames):
        pl = []
        for (bid, x, y, h) in fr:
            X, Yb = project(PX, PY, i, x, y, S, OFF, MIRROR)
            if noise is not None:
                ex, ey = noise.draw(bid, plate_band(X, Yb, S))
                X += ex; Yb += ey
            w = int(round(72 * max(0.0, min(1.0, h))))
            xl = int(round(X - 36)); ytop = int(round(Yb - 1.5))
            if ytop < -10 or ytop > 1090 or xl < -80 or xl > 1990:
                continue
            pl.append((ytop, xl, w))
        if not pl:
            continue
        pl.sort(reverse=(order == 'desc'))
        # the player's own plate (Lap H-2: green bar rows 428-431, left edge ~921-924), drawn last (on top)
        ys = [p[0] for p in pl] + [428]
        ya, yz = max(min(ys) - 40, 0), min(max(ys) + 10, 1080)
        img = np.zeros((yz - ya, 1920, 3), np.uint8)
        for (ytop, xl, w) in pl:
            _paint(img, xl, ytop - ya, w, RED)
        _paint(img, 924, 428 - ya, 72, GREEN)
        y0 = max(60 - ya, 0); y1 = min(975 - ya, yz - ya)
        if y1 <= y0:
            continue
        for b in bars.find_bars(img, minw=14, y0=y0, y1=y1):
            yy = b['y'] + ya
            if in_hud(b['x_c'], yy):
                continue
            rows.append((ft[i], 0, b['x_left'] + 36, yy, b['w'], b['txt']))
    return rows


def census(rows, ft, PX, PY, S, MIRROR):
    """the referent's world/track/kinematics on the synthetic plate rows; returns per-band [moving, still] and
    per-band frame counts of narrow detections."""
    sgn = -1.0 if MIRROR else 1.0
    cnt = np.zeros((8, 2), int)
    if not rows:
        return cnt, 0, 0
    R = np.array(rows, float)
    ctt = ft.copy()
    cx = -(PX - PX[0]) * S
    cy = -sgn * (PY - PY[0]) * S * K
    W, pw = d1b.world(R, ctt, cx, cy)
    trs = d1b.track(W, ft[0] - 1, ft[-1] + 1)
    ntr = 0
    for tr in trs:
        if len(tr['p']) < int(1.0 * FPS):
            continue
        k = d1b.kinematics(tr, pw, W)
        if k is None:
            continue
        ntr += 1
        b = np.digitize(k['r'], EDGES) - 1
        for q in range(len(b)):
            if 0 <= b[q] < 8:
                cnt[b[q], 0 if k['spd'][q] >= 50.0 else 1] += 1
    return cnt, ntr, len(R)


def run(layer, salts, opts):
    S = float(opts.get('S', 122)); OFF = float(opts.get('OFF', 115)); MIRROR = int(opts.get('MIRROR', 0))
    ORDER = opts.get('ORDER', 'asc')
    A = load_rows()
    tot = np.zeros((8, 2), int); ntr = 0; nplates = 0; nframes = 0
    per_wave = {}
    for s in salts:
        noise = Noise(1000 + s) if layer in ('L1g', 'L3') else None
        for w in range(151, 161):
            B = A[(A[:, 0] == s) & (A[:, 1] == w)]
            if len(B) == 0:
                continue
            ft, PX, PY, frames = resample(B)
            nframes += len(ft)
            if layer in ('N1', 'N2'):
                c = layer_N(ft, PX, PY, frames, S, OFF, MIRROR, plate_range=(layer == 'N2'))
            else:
                if layer in ('L0', 'L1', 'L1g'):
                    rows = detect_ideal(ft, PX, PY, frames, S, OFF, MIRROR, minw=(layer != 'L0'), noise=noise)
                else:
                    rows = detect_render(ft, PX, PY, frames, S, OFF, MIRROR, noise=noise, order=ORDER)
                c, nt, npl = census(rows, ft, PX, PY, S, MIRROR)
                ntr += nt; nplates += npl
            tot += c
            per_wave.setdefault(w, np.zeros((8, 2), int))
            per_wave[w] += c
    return tot, dict(n_tracks=ntr, n_plate_rows=nplates, n_frames=nframes,
                     per_wave={w: v.tolist() for w, v in per_wave.items()})


def summary(tot):
    sf = [round(float(tot[i, 1] / tot[i].sum()), 4) if tot[i].sum() else None for i in range(8)]
    ins = tot[:4].sum(0); mid = tot[4:6].sum(0)
    return dict(still_by_band=sf, n_by_band=tot.sum(1).tolist(),
                inside_300gpx=round(float(ins[1] / ins.sum()), 4) if ins.sum() else None,
                band_300_600gpx=round(float(mid[1] / mid.sum()), 4) if mid.sum() else None)


if __name__ == '__main__':
    layer, sl, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    opts = dict(a.split('=') for a in sys.argv[4:])
    a, b = (int(x) for x in sl.split('-'))
    tot, extra = run(layer, range(a, b + 1), opts)
    out = dict(layer=layer, salts=[a, b], opts=opts, counts=tot.tolist(), **summary(tot), **extra)
    json.dump(out, open(outp, 'w'), indent=1)
    print(layer, sl, opts, 'inside', out['inside_300gpx'], '300-600', out['band_300_600gpx'], out['still_by_band'],
          'tracks', extra['n_tracks'], 'plates', extra['n_plate_rows'])
