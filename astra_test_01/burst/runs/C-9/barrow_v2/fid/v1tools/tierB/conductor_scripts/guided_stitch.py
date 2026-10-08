# C-9 stitch for guided_paint.py chunks. usage: guided_stitch.py <cfg.json> <out.png> [preview.jpg]
# Every chunk is a 1536x1024 canvas at a 1280x768 stride, so neighbours overlap by 256 px. Astra EDIT
# re-synthesises the neighbour strips it was handed (mean abs diff 3-13 of 255 on T10BF), so a hard paste
# leaves a join. Each chunk gets linear ramps across its overlaps (up on the left/top, down on the
# right/bottom, only where a neighbour exists); the ramps form a partition of unity, so the weights
# sum to exactly 1 everywhere, corners where four chunks meet included.
import json, sys, pathlib, hashlib
import numpy as np
from PIL import Image
A9 = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts')
cfg = json.load(open(sys.argv[1])); P, COLS, ROWS = cfg['prefix'], cfg['cols'], cfg['rows']
W, H, SX, SY = 1536, 1024, 1280, 768; OV = W - SX
assert OV == H - SY
def src(k):
    for d in (f'{P}-{k}-r1', f'{P}-{k}'):
        p = A9/d/f'{P}-{k}.png'
        if p.exists(): return p
    sys.exit(f'chunk {k} is not painted')
acc = np.zeros(((ROWS-1)*SY + H, (COLS-1)*SX + W, 3)); wsum = np.zeros(acc.shape[:2])
up = np.linspace(0, 1, OV, endpoint=False) + 0.5/OV
# BV2F-BEGIN DEV-23 (R-C9-241): LOW-FREQUENCY TONE MATCH at the pasted-context boundary. A chunk's left 256 columns / top
# 256 rows are its painted neighbours' pixels (guided_paint stage) and the image model keeps them; but the paint it makes
# NEW can come out at another tone (a light context strip against darker new ice): a straight step at x = 256 / y = 256
# that v1's overlap ramps cannot hide (the ramp ends exactly there). Per chunk, BEFORE the ramps: along the boundary, the
# mean colour of the ICE/SNOW pixels (bright, low chroma) in the CONTEXT band (the strip's last DEV23_BAND px) minus that
# in the NEW band (the first DEV23_BAND px past it), weighted by how many ice/snow pixels both bands hold, smoothed along
# the boundary (normalised Gaussian, sigma DEV23_SIGMA px; no correction where the boundary crosses no ice/snow), is added
# to the NEW paint's ice/snow pixels (a soft mask: rocks, wood, scrub and dark water keep their colour) and faded to 0
# over DEV23_FADE px into the chunk (smoothstep). The context strip is untouched; only a smooth field is added, so no
# high-frequency detail changes. BV2F_DEV23=0 gives v1's stitch byte for byte.
import os
from scipy import ndimage
DEV23 = os.environ.get('BV2F_DEV23', '1') != '0'
DEV23_SIGMA, DEV23_FADE, DEV23_BAND, DEV23_EDGE = 56.0, 300, 48, 4   # BV2F: EDGE = the first new columns/rows, matched one by one (the model's own transition is 1-2 px wide)
DEV23_REP = {}
def _fade(n):
    t = np.clip(np.arange(n) / float(DEV23_FADE), 0.0, 1.0)
    return 1.0 - t * t * (3.0 - 2.0 * t)
def _icesnow(a):
    # bright and low-chroma (sRGB 0-255): snow and pale ice; soft-edged
    mx, mn = a.max(-1), a.min(-1)
    m = ((a.mean(-1) > 150) & ((mx - mn) < 70)).astype(np.float64)
    return m
def _step_along(ctx, new):
    # ctx, new: (L, BAND, 3) bands either side of the boundary (L along it) -> (L, 3) step, smoothed along the boundary
    mc, mn_ = _icesnow(ctx), _icesnow(new)
    nc, nn = mc.sum(1), mn_.sum(1)
    mean_c = (ctx * mc[..., None]).sum(1) / np.maximum(nc, 1)[:, None]
    mean_n = (new * mn_[..., None]).sum(1) / np.maximum(nn, 1)[:, None]
    fc, fn = nc / float(ctx.shape[1]), nn / float(new.shape[1])
    w = np.where((fc >= 0.25) & (fn >= 0.25), np.minimum(fc, fn), 0.0)
    d = (mean_c - mean_n) * w[:, None]
    gw = ndimage.gaussian_filter1d(w, DEV23_SIGMA, mode='constant')
    st = np.stack([ndimage.gaussian_filter1d(d[:, i], DEV23_SIGMA, mode='constant') for i in range(3)], -1) / np.maximum(gw, 1e-6)[:, None]
    return st * np.clip(gw / 0.2, 0.0, 1.0)[:, None]
def _bv2f_tone(im, c, r):
    if not DEV23:
        return im
    rep = {}
    soft = lambda a: ndimage.gaussian_filter(_icesnow(a), 3.0)
    if c > 0:   # left context: columns 0..255; new paint from column 256
        ctx = im[:, OV - DEV23_BAND:OV]
        st = _step_along(ctx, im[:, OV + DEV23_EDGE:OV + DEV23_EDGE + DEV23_BAND])
        edge = [_step_along(ctx, im[:, OV + e:OV + e + 1]) for e in range(DEV23_EDGE)]
        sm = soft(im[:, OV:])
        im = im.copy(); im[:, OV + DEV23_EDGE:] += st[:, None, :] * (_fade(W - OV)[None, DEV23_EDGE:] * sm[:, DEV23_EDGE:])[..., None]
        for e in range(DEV23_EDGE):
            im[:, OV + e] += edge[e] * sm[:, e:e + 1]
        rep['left_step_mean_abs'] = round(float(np.abs(st).mean()), 2)
    if r > 0:   # top context: rows 0..255; new paint from row 256
        T = lambda a: np.transpose(a, (1, 0, 2))
        ctx = T(im[OV - DEV23_BAND:OV])
        st = _step_along(ctx, T(im[OV + DEV23_EDGE:OV + DEV23_EDGE + DEV23_BAND]))
        edge = [_step_along(ctx, T(im[OV + e:OV + e + 1])) for e in range(DEV23_EDGE)]
        sm = soft(im[OV:, :])
        im = im.copy(); im[OV + DEV23_EDGE:, :] += st[None, :, :] * (_fade(H - OV)[DEV23_EDGE:, None] * sm[DEV23_EDGE:, :])[..., None]
        for e in range(DEV23_EDGE):
            im[OV + e, :] += edge[e] * sm[e][:, None]
        rep['top_step_mean_abs'] = round(float(np.abs(st).mean()), 2)
    DEV23_REP[f'{c}_{r}'] = rep
    return im
# BV2F-END
# BV2F-BEGIN DEV-25 (R-C9-248): GRAIN-AMPLITUDE MATCH at the pasted-context boundary, after DEV-23's tone match. The
# image service redraws the pasted strip (R-C9-247: softer than the neighbour by 0.67-1.07 on ice) and paints the new area
# at its own grain (up to 2.5x the strip's on the mound): a straight grain line at x/y = 256. Per chunk: the detail
# (image - Gaussian sigma DEV25_SIGMA) is measured on snow/ice pixels (bright, low chroma) in the strip's last DEV25_BAND
# px and the new paint's first DEV25_BAND px; the ratio strip/new, smoothed along the boundary (normalised Gaussian
# sigma 56; 1 where the boundary crosses no snow/ice), clipped 0.5..1.0 (soften only), scales the NEW paint's detail, fading to 1 over
# DEV25_FADE px into the chunk (smoothstep). No pixel moves and no detail is added or removed: only its amplitude.
# BV2F_DEV25=0 turns it off; with BV2F_DEV23=0 as well the stitch is v1's byte for byte.
DEV25 = os.environ.get('BV2F_DEV25', '1') != '0'
DEV25_SIGMA, DEV25_BAND, DEV25_FADE = 3.0, 48, 300
DEV25_REP = {}
def _det(a):
    return a - np.stack([ndimage.gaussian_filter(a[..., i], DEV25_SIGMA) for i in range(3)], -1)
def _grain_ratio(cd, nd, cm, nm):
    def s(d, m):
        n = m.sum(1)
        mu = (d * m[..., None]).sum(1) / np.maximum(n, 1)[:, None]
        v = (((d - mu[:, None, :]) ** 2) * m[..., None]).sum(1) / np.maximum(n, 1)[:, None]
        return np.sqrt(v.mean(-1)), n
    sc, nc = s(cd, cm)
    sn, nn = s(nd, nm)
    w = ((nc >= 12) & (nn >= 12)).astype(np.float64)
    k = np.where(w > 0, sc / np.maximum(sn, 1e-6), 1.0)
    gw = ndimage.gaussian_filter1d(w, DEV23_SIGMA, mode='constant')
    ks = ndimage.gaussian_filter1d(k * w, DEV23_SIGMA, mode='constant') / np.maximum(gw, 1e-6)
    return np.clip(np.where(gw > 0.05, ks, 1.0), 0.5, 1.0)   # BV2F: soften only -- amplifying new grain toward a busier strip made two joins worse (R-C9-248 dry run)
def _bv2f_grain(im, c, r):
    if not DEV25:
        return im
    rep = {}
    if c > 0:
        d = _det(im); m = _icesnow(im)
        k = _grain_ratio(d[:, OV - DEV25_BAND:OV], d[:, OV:OV + DEV25_BAND], m[:, OV - DEV25_BAND:OV], m[:, OV:OV + DEV25_BAND])
        g = (k[:, None] - 1.0) * _fade(W - OV)[None, :]
        im = im.copy(); im[:, OV:] += d[:, OV:] * g[..., None]
        rep['left_k_median'] = round(float(np.median(k)), 3)
    if r > 0:
        d = _det(im); m = _icesnow(im); T = lambda a: np.swapaxes(a, 0, 1)
        k = _grain_ratio(T(d[OV - DEV25_BAND:OV]), T(d[OV:OV + DEV25_BAND]), T(m[OV - DEV25_BAND:OV]), T(m[OV:OV + DEV25_BAND]))
        g = (k[None, :] - 1.0) * _fade(H - OV)[:, None]
        im = im.copy(); im[OV:, :] += d[OV:, :] * g[..., None]
        rep['top_k_median'] = round(float(np.median(k)), 3)
    DEV25_REP[f'{c}_{r}'] = rep
    return im
# BV2F-END
for r in range(ROWS):
    for c in range(COLS):
        im = np.asarray(Image.open(src(f'{c}_{r}')).convert('RGB'), dtype=np.float64)
        assert im.shape == (H, W, 3), (c, r, im.shape)
        im = _bv2f_tone(im, c, r)   # BV2F DEV-23
        im = _bv2f_grain(im, c, r)   # BV2F DEV-25
        wx, wy = np.ones(W), np.ones(H)
        if c > 0: wx[:OV] *= up
        if c < COLS-1: wx[W-OV:] *= up[::-1]
        if r > 0: wy[:OV] *= up
        if r < ROWS-1: wy[H-OV:] *= up[::-1]
        w = np.outer(wy, wx)
        acc[r*SY:r*SY+H, c*SX:c*SX+W] += im * w[..., None]; wsum[r*SY:r*SY+H, c*SX:c*SX+W] += w
assert abs(wsum.min() - 1) < 1e-9 and abs(wsum.max() - 1) < 1e-9, (wsum.min(), wsum.max())
out = Image.fromarray((acc / wsum[..., None]).clip(0, 255).round().astype(np.uint8))
out.save(sys.argv[2], optimize=True)
print(pathlib.Path(sys.argv[2]).name, out.size, 'sha256', hashlib.sha256(pathlib.Path(sys.argv[2]).read_bytes()).hexdigest())
print('DEV-23', 'on' if DEV23 else 'off', DEV23_REP)   # BV2F DEV-23
print('DEV-25', 'on' if DEV25 else 'off', DEV25_REP)   # BV2F DEV-25
if len(sys.argv) > 3:
    out.resize((out.width // 2, out.height // 2), Image.LANCZOS).save(sys.argv[3], quality=86)
