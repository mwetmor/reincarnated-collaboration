"""Footage census: per frame, every red (hostile) nameplate bar + its OCR'd (cur/max) text,
green (allied) bars, and the top-centre hovered-plate state.

Reuses UNCHANGED: Lap H-2 bars.find_bars (red bar + white-text gate) and galadriel's
eor_hpocr glyph classifier with the board-closure atlas (eye-verified glyphs).
Read-only on the video. Writes JSON rows only.
usage: census.py <video> <t0> <t1> <fps> <out.json>
"""
import sys, json, subprocess
import numpy as np
from scipy import ndimage
import bars as B
import eor_hpocr as O

W, H = 1920, 1080
HUD = [(1330, 0, 1920, 262), (0, 0, 1920, 58), (0, 980, 1920, 1080), (0, 0, 300, 120)]


def in_hud(x, y):
    return any(x0 <= x <= x1 and y0 <= y <= y1 for (x0, y0, x1, y1) in HUD)


def text_box(wh, yb, xc):
    """tight bbox of the white text run immediately above a bar (dy -34..-16)."""
    y0, y1 = max(0, yb - 36), max(1, yb - 15)
    x0, x1 = max(0, int(xc) - 120), min(W, int(xc) + 121)
    m = wh[y0:y1, x0:x1] > 0
    if m.sum() < 30:
        return None
    # dilate horizontally to bind glyphs, pick the component nearest the bar centre
    d = ndimage.binary_dilation(m, structure=np.ones((3, 9)))
    lab, n = ndimage.label(d)
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        w = xs.max() - xs.min() + 1
        h = ys.max() - ys.min() + 1
        if w < 40 or h > 18:
            continue
        cx = (xs.min() + xs.max()) / 2 + x0
        score = abs(cx - xc) - 0.2 * w
        if best is None or score < best[0]:
            best = (score, xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)
    if best is None:
        return None
    _, a, b, c, d2 = best
    return (int(a), int(b), int(c), int(d2))



HUD2 = [(0,0,300,86),(1150,0,1660,210),(1640,20,1920,275),(1600,260,1920,380),(0,985,1920,1080)]
def hud2(x0,y0,x1,y1):
    for a,b,c,d in HUD2:
        ox=max(0,min(x1,c)-max(x0,a)); oy=max(0,min(y1,d)-max(y0,b))
        if ox*oy>0.6*max(1,(x1-x0)*(y1-y0)): return True
    return False

def blobs(a):
    """galadriel eor_hptext.blobs, re-implemented with scipy labelling (same parameters)."""
    m = a.min(axis=2) > 135
    d = ndimage.binary_dilation(m, structure=np.ones((1, 13)))
    d = ndimage.binary_dilation(d, structure=np.ones((3, 1)))
    lab, n = ndimage.label(d)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        ys, xs = sl
        w = xs.stop - xs.start; h = ys.stop - ys.start
        if not (55 <= w <= 300 and 5 <= h <= 16):
            continue
        x0, y0, x1, y1 = xs.start, ys.start, xs.stop - 1, ys.stop - 1
        if hud2(x0, y0, x1, y1):
            continue
        dens = m[y0:y1+1, x0:x1+1].mean()
        if not (0.04 <= dens <= 0.55):
            continue
        out.append((x0, y0, x1, y1))
    return out

def bar_under(a, box):
    x0,y0,x1,y1 = box
    reg = a[y1+6:y1+34, max(0,x0-15):min(W,x1+15)]
    r = B.red_mask(reg); g = B.green_mask2(reg)
    rr = r.sum(axis=1).max() if r.size else 0
    gg = g.sum(axis=1).max() if g.size else 0
    ry = int(np.argmax(r.sum(axis=1)))+y1+6 if rr else None
    return int(rr), int(gg), ry


def topplate(a):
    """hovered-monster plate at top-centre: count of saturated/warm name glyph pixels in the
    name band (x 650-1300, y 14-38) and the family band."""
    reg = a[12:40, 640:1280].astype(int)
    R, G, Bc = reg[..., 0], reg[..., 1], reg[..., 2]
    mx = reg.max(axis=2); mn = reg.min(axis=2)
    colored = ((mx > 140) & (mx - mn > 40)).sum()
    white = (mn > 170).sum()
    return int(colored), int(white)


def run(video, t0, t1, fps, out):
    atlas = O.load('atlas.npz')
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', video,
           '-vf', f'fps={fps}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3)
    N = W * H * 3
    rows = []
    i = 0
    while True:
        raw = p.stdout.read(N)
        if len(raw) < N:
            break
        a = np.frombuffer(raw, dtype=np.uint8).reshape(H, W, 3)
        t = round(t0 + i / fps, 4)
        wh = O.white(a)
        fr = {'t': t, 'top': topplate(a), 'txt': []}
        for box in blobs(a):
            x0, y0, x1, y1 = box
            st, sc, mg = O.read_string(atlas, wh[y0:y1 + 1, x0:x1 + 1])
            pr = O.parse(st)
            rr, gg, ry = bar_under(a, box)
            fr['txt'].append({'box': [int(x0), int(y0), int(x1), int(y1)], 'raw': st,
                              'cur': pr[0] if pr else None, 'max': pr[1] if pr else None,
                              'sc': round(sc, 3), 'red': rr, 'green': gg, 'bary': ry})
        rows.append(fr)
        i += 1
    p.stdout.close(); p.wait()
    json.dump({'video': video, 't0': t0, 't1': t1, 'fps': fps, 'frames': rows}, open(out, 'w'))
    npl = sum(len(r['txt']) for r in rows)
    npar = sum(1 for r in rows for q in r['txt'] if q.get('max'))
    print(f'{out}: frames={i} red={npl} parsed={npar}')


if __name__ == '__main__':
    run(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5])
