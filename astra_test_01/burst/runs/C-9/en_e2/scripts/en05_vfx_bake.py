# EN-E2 VFX: the acolytes' two spells as BAKED FLIPBOOKS (the Barrow's discipline: everything rendered offline into ONE atlas,
# played as quads; nothing built, compiled or simulated at cast time). No paid call: procedural, in the painted register --
# a pale blue-white core, lapis washes with a granulated, ragged edge (the wash pools at its rim), a dark ink-blue contour that
# wavers, and neutral grey smoke. No bloom: the "light" is pale value, as the register card asks.
#
#   python3 scripts/en05_vfx_bake.py <out_dir> --id <name> --bolt-r <m> --burst-r <m> --ring-r <m> [--seed n]
#
# ATLAS: rgb = premultiplied colour C, a = cover A, so a frame lays over any ground g as out = C + g * (1 - A) (fire_bake_pack's
# blend). Scale 100.617553710938 px/m (the play camera), so a frame is drawn at its baked size in metres.
# PHASES (frames.json): bolt (billboard loop, travels along +x = EAST, anchor = the bolt's centre), cast (billboard, anchor =
# the release hand), burst (billboard, anchor = the impact point), ring_tele (GROUND plane, anchor = ring centre: the telegraph
# drawn ON the floor -- a ground quad in metres, so the camera's 52.95 deg foreshortening is the renderer's, not baked),
# ring_burst (GROUND plane), ring_smoke (billboard, anchor = ring centre on the floor).
import argparse, json, os, hashlib
import numpy as np
from PIL import Image
from scipy import ndimage

PPM = 100.617553710938
ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--id', required=True)
ap.add_argument('--bolt-r', type=float, default=0.3); ap.add_argument('--burst-r', type=float, default=1.5)
ap.add_argument('--ring-r', type=float, default=2.2); ap.add_argument('--seed', type=int, default=7)
ap.add_argument('--hue', default='cold', choices=['cold', 'pale', 'frost', 'flame', 'storm', 'spirit', 'blight', 'blood', 'aether', 'mud', 'void', 'stone', 'bone'])
ap.add_argument('--extras', default='', help='round 3: slash (claw arcs), aura (a held ground ring loop at --aura-r)')
ap.add_argument('--aura-r', type=float, default=6.0)
A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
rng = np.random.default_rng(A.seed)
PAL = dict(cold=([0.93, 0.96, 1.00], [0.42, 0.58, 0.86]), pale=([0.93, 0.96, 1.00], [0.55, 0.66, 0.84]),
           frost=([0.94, 0.97, 1.00], [0.50, 0.70, 0.88]), flame=([1.00, 0.93, 0.70], [0.90, 0.45, 0.16]),   # fire: the only saturated warm (register)
           storm=([0.96, 0.95, 1.00], [0.58, 0.52, 0.86]), spirit=([0.90, 0.95, 0.97], [0.55, 0.68, 0.74]),
           blight=([0.92, 0.95, 0.80], [0.52, 0.60, 0.34]), blood=([0.93, 0.84, 0.78], [0.52, 0.20, 0.18]),   # madder, moderate (register)
           aether=([0.97, 0.92, 0.98], [0.66, 0.50, 0.78]), mud=([0.86, 0.84, 0.70], [0.42, 0.40, 0.26]),   # crypt mud + moss
           void=([0.93, 0.88, 0.98], [0.40, 0.28, 0.58]),   # void violet
           stone=([0.95, 0.93, 0.88], [0.62, 0.60, 0.55]), bone=([0.95, 0.93, 0.85], [0.66, 0.62, 0.48]))
CORE, WASH = (np.array(v) for v in PAL[A.hue])
INK = np.array([0.12, 0.16, 0.30]); SMOKE = np.array([0.55, 0.55, 0.56])

def noise(h, w, scale, oct=4):
    n = np.zeros((h, w)); amp = 1.0; tot = 0
    for o in range(oct):
        s = max(1, int(scale / 2 ** o)); g = rng.standard_normal((h // s + 2, w // s + 2))
        g = ndimage.zoom(g, s, order=3)[:h, :w]; n += amp * g; tot += amp; amp *= 0.5
    return n / tot

def wash_layer(field, thresh, col, pool=0.35, gran=0.25, h=None):
    """A watercolour wash where field > thresh: flat-ish interior, darker POOLED rim, granulation."""
    m = field > thresh
    if not m.any(): return np.zeros(field.shape + (3,)), np.zeros(field.shape)
    d = ndimage.distance_transform_edt(m); rim = np.exp(-d / 3.0) * m
    g = noise(*field.shape, 3, 2) * gran
    a = np.clip(m * (0.55 + g) + rim * pool, 0, 1)
    c = col[None, None, :] * (1 - 0.35 * rim[..., None]) * np.ones(field.shape + (3,))
    return c, a

def ink_line(field, thresh, wob=1.2, w=1.6):
    m = field > thresh; e = m ^ ndimage.binary_erosion(m, iterations=1)
    d = ndimage.distance_transform_edt(~e)
    wv = w * (0.6 + 0.8 * np.clip(noise(*field.shape, 12, 2) + 0.5, 0, 1))
    return np.clip(1 - d / wv, 0, 1) * 0.85

def over(dst_c, dst_a, c, a):            # straight colour "over", returns straight
    out_a = a + dst_a * (1 - a)
    out_c = (c * a[..., None] + dst_c * dst_a[..., None] * (1 - a[..., None])) / np.maximum(out_a[..., None], 1e-6)
    return out_c, out_a

def blob_field(h, w, cx, cy, rx, ry, rough=0.18, nscale=10):
    yy, xx = np.mgrid[0:h, 0:w]; r = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    return 1 - r + rough * noise(h, w, nscale, 3)

frames = []   # (phase, i, rgba float, anchor(x,y), plane)

# ---- BOLT: 8-frame loop, travelling EAST, teardrop with a tail ---------------------------------------------------------
br = A.bolt_r * PPM; W_, H_ = int(br * 4.4), int(br * 2.8)
for i in range(8):
    cx, cy = W_ - br * 1.4, H_ / 2
    yy, xx = np.mgrid[0:H_, 0:W_]
    tail = np.clip((cx - xx) / (W_ - br * 2), 0, 1)
    ry = br * (1 - 0.75 * tail) * (1 + 0.08 * np.sin(i / 8 * 2 * np.pi))
    f = 1 - np.sqrt(((xx - cx) / np.where(xx > cx, br, br * 2.6)) ** 2 + ((yy - cy) / np.maximum(ry, 1)) ** 2) + 0.22 * noise(H_, W_, 6, 3)
    c, a = wash_layer(f, 0.0, WASH)
    c2, a2 = wash_layer(f, 0.45, CORE, pool=0.1, gran=0.1); c, a = over(c, a, c2, a2 * 0.95)
    ink = ink_line(f, 0.0); c, a = over(c, a, np.broadcast_to(INK, c.shape), ink)
    frames.append(('bolt', i, np.dstack([c, a]), (cx, cy), 'billboard'))

# ---- CAST: 6-frame puff at the hand (a gathering spiral of wash closing to the core) --------------------------------------
cr = 0.32 * PPM; S = int(cr * 3)
for i in range(6):
    k = i / 5; yy, xx = np.mgrid[0:S, 0:S]; th = np.arctan2(yy - S / 2, xx - S / 2); r = np.hypot(xx - S / 2, yy - S / 2) / cr
    f = (1 - abs(r - (1.2 - 0.9 * k))) * 0.9 + 0.35 * np.sin(3 * th + 6 * k) * (1 - k) + 0.2 * noise(S, S, 5, 2) - 0.25
    c, a = wash_layer(f, 0.1, WASH, pool=0.4)
    fc = 1 - r / (0.3 + 0.5 * k) + 0.15 * noise(S, S, 4, 2); c2, a2 = wash_layer(fc, 0.0, CORE, 0.1, 0.1)
    c, a = over(c, a, c2, a2); a *= (0.5 + 0.5 * k)
    frames.append(('cast', i, np.dstack([c, a]), (S / 2, S / 2), 'billboard'))

# ---- BURST: 10 frames, the explosion radius, a cold shock ring + grey smoke that lingers ---------------------------------
R = A.burst_r * PPM; S = int(R * 2.3)
for i in range(10):
    k = i / 9; yy, xx = np.mgrid[0:S, 0:S]; r = np.hypot(xx - S / 2, yy - S / 2) / R
    ringw = 0.10 + 0.12 * k; rr = 0.25 + 0.75 * np.sqrt(k)
    f = 1 - abs(r - rr) / ringw + 0.35 * noise(S, S, 9, 3)
    c, a = wash_layer(f, 0.0, WASH, pool=0.5); a *= (1 - k) ** 0.8
    fc = 1 - r / max(0.05, 0.45 * (1 - k)) + 0.2 * noise(S, S, 6, 2); c2, a2 = wash_layer(fc, 0.0, CORE, 0.1, 0.1)
    c, a = over(c, a, c2, a2 * (1 - k))
    fs = blob_field(S, S, S / 2, S / 2 - R * 0.15 * k, R * (0.35 + 0.45 * k), R * (0.3 + 0.4 * k), 0.45, 14)
    cs, as_ = wash_layer(fs, 0.25, SMOKE, pool=0.25, gran=0.35); as_ *= 0.40 * np.sin(np.pi * min(0.97, 0.05 + k * 1.3))
    c, a = over(cs, as_, c, a)
    ink = ink_line(f, 0.0) * (1 - k); c, a = over(c, a, np.broadcast_to(INK, c.shape), ink)
    frames.append(('burst', i, np.dstack([c, a]), (S / 2, S / 2), 'billboard'))

# ---- RING (ground plane, metres): telegraph 12 frames (the circle drawn, hour-marks ticking in), burst 10 -------------------
RR = A.ring_r * PPM; S = int(RR * 2.25)
yy, xx = np.mgrid[0:S, 0:S]; r = np.hypot(xx - S / 2, yy - S / 2) / RR; th = np.arctan2(yy - S / 2, xx - S / 2)
base_n = noise(S, S, 10, 3)
for i in range(12):
    k = (i + 1) / 12; sweep = ((th + np.pi) / (2 * np.pi)) <= k
    f = (1 - abs(r - 1) / 0.035 + 0.25 * base_n) * sweep
    ticks = (np.abs(((th + np.pi) / (2 * np.pi) * 12) % 1 - 0.5) > 0.47) & (r > 0.86) & (r < 0.98) & sweep
    f = np.maximum(f, ticks * 1.0)
    c, a = wash_layer(f, 0.0, WASH, pool=0.5, gran=0.3); a *= 0.85
    fi = (1 - r) * 0.6 + 0.3 * base_n - 0.35; ci, ai = wash_layer(fi, 0.0, WASH, 0.2, 0.4); c, a = over(ci, ai * 0.18 * k, c, a)
    frames.append(('ring_tele', i, np.dstack([c, a]), (S / 2, S / 2), 'ground'))
for i in range(10):
    k = i / 9
    f = 1 - abs(r - (1 - 0.15 * k)) / (0.06 + 0.25 * k) + 0.4 * base_n
    c, a = wash_layer(f, 0.0, WASH, pool=0.5); a *= (1 - k) ** 0.7
    fc = 1 - r / (0.95 * (1 - 0.6 * k)) + 0.4 * noise(S, S, 8, 3) - 0.2; c2, a2 = wash_layer(fc, 0.0, CORE, 0.2, 0.3)
    c, a = over(c, a, c2, a2 * 0.40 * (1 - k) ** 1.5)
    frames.append(('ring_burst', i, np.dstack([c, a]), (S / 2, S / 2), 'ground'))
SH, SW = int(RR * 2.2), int(RR * 2.4)
for i in range(10):
    k = i / 9; fs = np.zeros((SH, SW)) - 1
    for j in range(7):
        ang = j / 7 * 2 * np.pi; px = SW / 2 + np.cos(ang) * RR * 0.85; py = SH * 0.62 + np.sin(ang) * RR * 0.3 - RR * 0.5 * k
        fs = np.maximum(fs, blob_field(SH, SW, px, py, RR * (0.16 + 0.12 * k), RR * (0.14 + 0.1 * k), 0.4, 12))
    cs, as_ = wash_layer(fs, 0.2, SMOKE, 0.3, 0.35); as_ *= 0.32 * np.sin(np.pi * (0.06 + 0.9 * k))
    frames.append(('ring_smoke', i, np.dstack([cs, as_]), (SW / 2, SH * 0.62), 'billboard'))


# ---- round 3 EXTRAS ---------------------------------------------------------------------------------------------------------
if 'slash' in A.extras:
    # CLAW: three parallel curved strokes swept across ~120 deg in front of the caster, 8 frames, billboard (anchor = the arc's centre)
    Rr = 0.9 * PPM; S = int(Rr * 2.4)
    yy, xx = np.mgrid[0:S, 0:S]; r = np.hypot(xx - S / 2, yy - S / 2) / Rr; th = (np.degrees(np.arctan2(yy - S / 2, xx - S / 2)) + 360) % 360
    for i in range(8):
        k = i / 7; head = 200 + 140 * min(1, k * 1.6); tail = 200 + 140 * max(0, k * 1.6 - 0.6)
        f = np.full((S, S), -1.0)
        for j, off in enumerate((-0.10, 0.0, 0.10)):
            band = 1 - np.abs(r - (0.85 + off)) / (0.035 * (1 - abs(off) * 3))
            inarc = (th >= tail) & (th <= head)
            f = np.maximum(f, np.where(inarc, band, -1) + 0.15 * noise(S, S, 5, 2))
        c, a = wash_layer(f, 0.0, WASH, pool=0.5); c2, a2 = wash_layer(f, 0.45, CORE, 0.1, 0.1); c, a = over(c, a, c2, a2)
        a *= (1 - max(0, k - 0.6) / 0.4)
        ink = ink_line(f, 0.0) * (1 - k); c, a = over(c, a, np.broadcast_to(INK, c.shape), ink)
        frames.append(('slash', i, np.dstack([c, a]), (S / 2, S / 2), 'billboard'))
if 'aura' in A.extras:
    # AURA: a held ground ring at --aura-r, a slow 12-frame breathing loop (closes: frame 12 == frame 0), ground plane
    RA = A.aura_r * PPM; S = int(RA * 2.15)
    yy, xx = np.mgrid[0:S, 0:S]; r = np.hypot(xx - S / 2, yy - S / 2) / RA; th = np.arctan2(yy - S / 2, xx - S / 2)
    bn = noise(S, S, 14, 3)
    for i in range(12):
        ph = 2 * np.pi * i / 12
        f = 1 - np.abs(r - 1) / (0.025 + 0.008 * np.sin(ph)) + 0.25 * bn + 0.15 * np.sin(6 * th + ph)
        c, a = wash_layer(f, 0.0, WASH, pool=0.4, gran=0.3); a *= 0.55 + 0.15 * np.sin(ph)
        fi = (1 - r) * 0.5 + 0.35 * bn - 0.3; ci, ai = wash_layer(fi, 0.0, WASH, 0.2, 0.4); c, a = over(ci, ai * 0.10, c, a)
        frames.append(('aura', i, np.dstack([c, a]), (S / 2, S / 2), 'ground'))

PHASE_SCALE = {ph: 0.5 for ph in ('ring_tele', 'ring_burst', 'ring_smoke', 'aura') if max(A.ring_r, A.aura_r if 'aura' in A.extras else 0) > 2.3}
# ---- pack: premultiply, trim, shelf-pack into one atlas --------------------------------------------------------------------
tiles = []
for ph, i, rgba, (ax, ay), plane in frames:
    a = np.clip(rgba[..., 3], 0, 1); C = np.clip(rgba[..., :3], 0, 1) * a[..., None]
    img = (np.dstack([C, a]) * 255 + 0.5).astype(np.uint8); nz = img[..., 3] > 0
    if not nz.any(): nz[int(ay), int(ax)] = True
    ys, xs = np.nonzero(nz); x0, y0, x1, y1 = max(xs.min() - 1, 0), max(ys.min() - 1, 0), xs.max() + 2, ys.max() + 2
    k_ = PHASE_SCALE.get(ph, 1.0); tile = img[y0:y1, x0:x1]; off = (x0 - ax, y0 - ay)
    if k_ != 1.0:                                  # round 3: big ground rings are soft washes -- stored at half scale (texture-size limit)
        tile = np.asarray(Image.fromarray(tile, 'RGBA').resize((max(1, round(tile.shape[1] * k_)), max(1, round(tile.shape[0] * k_))), Image.LANCZOS))
        off = (off[0] * k_, off[1] * k_)
    tiles.append(dict(phase=ph, i=i, img=tile, off=off, plane=plane))
AW = 4096; x = y = sh = 0
for t in sorted(tiles, key=lambda t: -t['img'].shape[0]):
    h, w = t['img'].shape[:2]
    if x + w > AW: x, y, sh = 0, y + sh + 1, 0
    t['rect'] = (x, y, w, h); x += w + 1; sh = max(sh, h)
AH = y + sh + 1; assert AH <= 16384, 'atlas %d px tall: over the 16384 texture limit' % AH; atlas = np.zeros((AH, AW, 4), np.uint8)
for t in tiles:
    x, y, w, h = t['rect']; atlas[y:y + h, x:x + w] = t['img']
p = os.path.join(A.out, '%s_atlas.png' % A.id); Image.fromarray(atlas, 'RGBA').save(p)
FPS = dict(bolt=20, cast=20, burst=20, ring_tele=15, ring_burst=20, ring_smoke=12)
if 'slash' in A.extras: FPS['slash'] = 24
if 'aura' in A.extras: FPS['aura'] = 8
table = dict(id=A.id, atlas=os.path.basename(p), atlas_size=[AW, AH], sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest(),
             px_per_m=PPM, blend='premultiplied: out = rgb + ground * (1 - a)',
             params=dict(bolt_body_r_m=A.bolt_r, burst_r_m=A.burst_r, ring_r_m=A.ring_r, seed=A.seed, palette=A.hue, **({'aura_r_m': A.aura_r} if 'aura' in A.extras else {}), **({'slash_r_m': 0.9} if 'slash' in A.extras else {})),
             phases={}, procedural='en05_vfx_bake.py (no paid call)')
for ph in FPS:
    fr = sorted([t for t in tiles if t['phase'] == ph], key=lambda t: t['i'])
    table['phases'][ph] = dict(fps=FPS[ph], px_per_m=round(PPM * PHASE_SCALE.get(ph, 1.0), 6), plane=fr[0]['plane'], loop=ph in ('bolt', 'aura'), n=len(fr),
                               frames=[dict(rect=list(map(int, t['rect'])), offset_px=[round(float(v), 2) for v in t['off']]) for t in fr])
json.dump(table, open(os.path.join(A.out, '%s_frames.json' % A.id), 'w'), indent=1)
# preview: every phase's frames over the Barrow-ish stone grey and over the lapis floor tone
pv = []
for ph in FPS:
    for t in sorted([t for t in tiles if t['phase'] == ph], key=lambda t: t['i']):
        im = t['img'].astype(float) / 255
        if im.shape[0] > 900: im = np.asarray(Image.fromarray(t['img'], 'RGBA').resize((im.shape[1] // 3, im.shape[0] // 3))).astype(float) / 255
        g = np.ones(im.shape[:2] + (3,)) * np.array([0.62, 0.60, 0.57])
        pv.append(np.clip(im[..., :3] + g * (1 - im[..., 3:4]), 0, 1))
mh = max(v.shape[0] for v in pv); tw = sum(v.shape[1] + 4 for v in pv)
cols = 8; rows = [pv[i:i + cols] for i in range(0, len(pv), cols)]
rw = max(sum(v.shape[1] + 4 for v in rr) for rr in rows); rh = [max(v.shape[0] for v in rr) + 4 for rr in rows]
can = np.ones((sum(rh), rw, 3)) * 0.62; yy = 0
for rr, h in zip(rows, rh):
    xx = 0
    for v in rr: can[yy:yy + v.shape[0], xx:xx + v.shape[1]] = v; xx += v.shape[1] + 4
    yy += h
Image.fromarray((can * 255).astype(np.uint8)).save(os.path.join(A.out, '%s_preview.png' % A.id))
print('VFX %s: %d frames, atlas %dx%d, %s' % (A.id, len(tiles), AW, AH, {k: v['n'] for k, v in table['phases'].items()}))
