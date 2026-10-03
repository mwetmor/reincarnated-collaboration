# Run C-9 Phase 2, lane DV (drax): barrow_v2 per-source SPAWN-DELIVERY VFX -- the shared core.
#
# Every effect is a procedural particle system simulated in SIM-FRAME METRES (x east, y SOUTH, z up; the layout_v2.json
# frame) relative to a pivot on the ground, and projected with the JOIN-1 / KC2-PLAY projection law
# (reincarnated-godot kc2_runtime/play/kc2play_projection.gd):
#       screen_x = ppm * x ;  screen_y = ppm * sin(a) * y - ppm * cos(a) * z ;  a = 52.9535411256029 deg, zero yaw, ortho.
# So a cell is ALREADY in the camera's view (ground decals are foreshortened by sin a, heights by cos a); the runtime draws
# it unrotated at the pivot's projected point, scaled by  s = proj.ppm / px_per_m  (the JOIN rule, sprite-cell contract 2.3).
#
# THE HAND: the R-C9-143-approved Meteor smoke (crater_v4_fx.gd, R-C9-128): light puffs on a soft radial sprite
# (1 - d)^2.1, discrete and brief, thrown with DRAG, swelling 0.70 -> 1.35 as they thin, alpha = peak * (1 - u)^0.55 after a
# quick rise. Here the puffs carry a faint lumpy edge and a shade-darker pooled rim (the painted register's wash) so light
# mist still reads on snow. No additive light, no bloom; sparks and embers are small bright dots drawn normally.
# Straight alpha, sRGB. Nothing here calls a paid service, Godot or Blender.
import math, json, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ALPHA_DEG = 52.9535411256029
A = math.radians(ALPHA_DEG)
SA, CA = math.sin(A), math.cos(A)
PPM_RENDER = 151.33680669505316          # JOIN-1 ppm_render (2 x ppm_GD)
PPM_GD = PPM_RENDER / 2.0                # 75.668 px/m: the play zoom (ZOOM-GD) -- 1:1 on screen there

def rng(seed):
    return np.random.default_rng(seed)

# ------------------------------------------------------------------ sprites
_SPR = {}
def _noise_ring(r, seed, amp=0.16):
    g = rng(seed); k = np.arange(1, 6); ph = g.random(5) * 2 * math.pi; am = amp * g.random(5) / k
    return lambda th: 1.0 + sum(am[i] * np.cos(k[i] * th + ph[i]) for i in range(5))

def puff_sprite(rpx, var, rim_amt=0.35, hard=False):
    """(alpha, rim) arrays of size (2R+1)^2. Soft radial (1-d)^2.1 with a lumpy edge; rim = the pooled darker edge weight."""
    rpx = max(1, int(round(rpx))); key = ('p', rpx, var, rim_amt, hard)
    if key in _SPR: return _SPR[key]
    n = 2 * rpx + 1; yy, xx = np.mgrid[0:n, 0:n] - rpx
    th = np.arctan2(yy, xx); ring = _noise_ring(rpx, 1000 + var)(th)
    d = np.hypot(xx, yy) / (rpx * ring)
    if hard:
        a = np.clip(1.5 - 1.5 * d, 0, 1) ** 0.6
    else:
        a = np.clip(1.0 - d, 0, 1) ** 2.1 * 1.6
        a = np.clip(a, 0, 1)
    rim = np.clip((d - 0.45) / 0.45, 0, 1) * (d < 1) * rim_amt
    _SPR[key] = (a.astype(np.float32), rim.astype(np.float32)); return _SPR[key]

def flat_sprite(rpx, var, rim_amt=0.5, hard=True):
    """A ground-lying blob: the puff/clod sprite squashed by sin(a) vertically (it lies on the ground plane)."""
    rpx = max(1, int(round(rpx))); key = ('f', rpx, var, rim_amt, hard)
    if key in _SPR: return _SPR[key]
    a, rim = puff_sprite(rpx, var, rim_amt, hard)
    h = max(1, int(round(a.shape[0] * SA)))
    a2 = np.asarray(Image.fromarray(a).resize((a.shape[1], h), Image.BILINEAR)); r2 = np.asarray(Image.fromarray(rim).resize((a.shape[1], h), Image.BILINEAR))
    _SPR[key] = (a2.astype(np.float32), r2.astype(np.float32)); return _SPR[key]

def shard_sprite(spx, var, rot_bucket, flat=False):
    """An angular ice / ash plate: a 4-5 sided polygon, pale body, dark edge (rim=1 on the outline)."""
    spx = max(2, int(round(spx))); key = ('s', spx, var, rot_bucket, flat)
    if key in _SPR: return _SPR[key]
    g = rng(2000 + var); nv = 4 + var % 2; S = 4 * spx + 4
    angs = np.sort(g.random(nv) * 2 * math.pi) + rot_bucket * (2 * math.pi / 16)
    rads = spx * (0.6 + 0.6 * g.random(nv))
    pts = [(S / 2 + math.cos(t) * r, S / 2 + math.sin(t) * r * (SA if flat else 1.0)) for t, r in zip(angs, rads)]
    im = Image.new('L', (S, S), 0); ImageDraw.Draw(im).polygon(pts, fill=255)
    ed = Image.new('L', (S, S), 0); ImageDraw.Draw(ed).line(pts + [pts[0]], fill=255, width=max(1, spx // 4))
    a = np.asarray(im, np.float32) / 255.0; e = np.asarray(ed, np.float32) / 255.0
    a = np.maximum(a * 0.9, e); _SPR[key] = (a, e * 0.9); return _SPR[key]

# ------------------------------------------------------------------ canvas
class Canvas:
    """Premultiplied RGBA float canvas; 'over' compositing."""
    def __init__(self, W, H):
        self.W, self.H = W, H; self.rgb = np.zeros((H, W, 3), np.float32); self.a = np.zeros((H, W), np.float32)
    def splat(self, spr, cx, cy, col, dark, alpha):
        a, rim = spr; h, w = a.shape; x0 = int(round(cx - w / 2)); y0 = int(round(cy - h / 2))
        xa, ya = max(0, x0), max(0, y0); xb, yb = min(self.W, x0 + w), min(self.H, y0 + h)
        if xa >= xb or ya >= yb or alpha <= 0.002: return
        sa = a[ya - y0:yb - y0, xa - x0:xb - x0] * alpha; sr = rim[ya - y0:yb - y0, xa - x0:xb - x0][..., None]
        c = np.asarray(col, np.float32) * (1 - sr) + np.asarray(dark, np.float32) * sr
        R = self.rgb[ya:yb, xa:xb]; Al = self.a[ya:yb, xa:xb]
        R *= (1 - sa)[..., None]; R += c * sa[..., None]
        Al *= (1 - sa); Al += sa
    def rgba8(self):
        a = np.clip(self.a, 0, 1); rgb = self.rgb / np.maximum(a, 1e-5)[..., None]
        out = np.zeros((self.H, self.W, 4), np.uint8)
        out[..., :3] = np.clip(rgb * 255 + 0.5, 0, 255).astype(np.uint8); out[..., 3] = np.clip(a * 255 + 0.5, 0, 255).astype(np.uint8)
        out[..., :3][out[..., 3] == 0] = 0
        return out

# ------------------------------------------------------------------ framing
class Frame:
    """A cell framing a local metre box (x, y, z ranges about the pivot) at px_per_m."""
    def __init__(self, xr, yr, zr, ppm, pad=4):
        self.ppm = ppm
        sx0, sx1 = xr[0] * ppm, xr[1] * ppm
        sy0 = ppm * (SA * yr[0] - CA * zr[1]); sy1 = ppm * (SA * yr[1] - CA * zr[0])
        self.ox = -sx0 + pad; self.oy = -sy0 + pad
        self.W = int(math.ceil(sx1 - sx0 + 2 * pad)); self.H = int(math.ceil(sy1 - sy0 + 2 * pad))
        self.W += self.W % 2; self.H += self.H % 2
        self.box = dict(x=list(xr), y=list(yr), z=list(zr))
    def proj(self, x, y, z):
        return self.ox + self.ppm * x, self.oy + self.ppm * (SA * y - CA * z)
    @property
    def pivot_px(self):
        return [round(self.ox, 2), round(self.oy, 2)]
    @property
    def cell_m(self):
        return [round(self.W / self.ppm, 4), round(self.H / self.ppm, 4)]

# ------------------------------------------------------------------ particle systems
class Emitter:
    """N base particles. births: periodic with period T (copies k = 0..K) or one-shot (T=None).
    Motion: p = p0 + v0 (1 - e^{-k a}) / k + w a + 0.5 g a^2.  Size: r * (s0 + (s1 - s0) u).  Alpha: peak * rise * (1-u)^0.55."""
    def __init__(self, n, seed, kind, col, dark, peak, life, birth, pos, vel, drag=0.0, drift=(0, 0, 0), grav=(0, 0, 0),
                 size=(0.3, 0.3), swell=(0.70, 1.35), T=None, ground_kill=False, flicker=0.0, rim=0.35, fade_pow=0.55, rise=0.08,
                 col2=None, var_n=6, streak=0.0, alpha_fn=None, zfloor=None, kill_fn=None):
        g = rng(seed); self.n = n; self.kind = kind; self.T = T
        self.col = np.array(col, np.float32); self.dark = np.array(dark, np.float32)
        self.col2 = None if col2 is None else np.array(col2, np.float32)
        self.mix = g.random(n); self.peak = peak; self.life = life(g, n) if callable(life) else np.full(n, life)
        self.b = birth(g, n) if callable(birth) else np.full(n, birth)
        self.p0 = pos(g, n); self.v0 = vel(g, n, self.p0); self.k = drag; self.w = np.array(drift, float); self.gv = np.array(grav, float)
        self.r = g.uniform(size[0], size[1], n); self.swell = swell; self.ground_kill = ground_kill; self.flicker = flicker
        self.var = g.integers(0, var_n, n); self.rot = g.integers(0, 16, n); self.spin = g.choice([-1, 1], n) * g.uniform(3, 9, n)
        self.ph = g.random(n) * 2 * math.pi; self.rim = rim; self.fade_pow = fade_pow; self.rise = rise; self.streak = streak
        self.alpha_fn = alpha_fn; self.zfloor = zfloor; self.kill_fn = kill_fn
    def pos(self, a, i):
        k = self.k; d = (1 - math.exp(-k * a)) / k if k > 0 else a
        return self.p0[i] + self.v0[i] * d + self.w * a + 0.5 * self.gv * a * a
    def items(self, t, frame, ppm):
        """Live particles at time t as draw items (sort_key, fn)."""
        out = []
        ks = [0] if self.T is None else range(0, int(t / self.T) + 2)
        for kk in ks:
            for i in range(self.n):
                bb = self.b[i] + (0 if self.T is None else kk * self.T)
                a = t - bb
                if a < 0 or a >= self.life[i]: continue
                u = a / self.life[i]
                p = self.pos(a, i)
                if self.zfloor is not None and p[2] < self.zfloor: p = p.copy(); p[2] = self.zfloor
                if self.ground_kill and p[2] < 0.0: continue
                if self.kill_fn is not None and self.kill_fn(p): continue
                if self.alpha_fn is not None:
                    al = self.peak * self.alpha_fn(u, a, i)
                else:
                    al = self.peak * min(1.0, u / self.rise if self.rise > 0 else 1.0) * (1 - u) ** self.fade_pow
                if self.flicker > 0: al *= 1 - self.flicker * (0.5 + 0.5 * math.sin(37.0 * a + self.ph[i]))
                rr = self.r[i] * (self.swell[0] + (self.swell[1] - self.swell[0]) * u)
                col = self.col if self.col2 is None else self.col * (1 - self.mix[i]) + self.col2 * self.mix[i]
                out.append((p[1] * SA * 1000 + p[2], self._drawer(frame, ppm, p, rr, al, col, i, a)))
        return out
    def _drawer(self, frame, ppm, p, rr, al, col, i, a):
        kind = self.kind; dark = self.dark; rim = self.rim
        def draw(cv):
            cx, cy = frame.proj(*p)
            if kind == 'puff':
                cv.splat(puff_sprite(rr * ppm, int(self.var[i]), rim), cx, cy, col, dark, al)
            elif kind == 'flatpuff':
                cv.splat(flat_sprite(rr * ppm, int(self.var[i]), rim, hard=False), cx, cy, col, dark, al)
            elif kind == 'clod':
                cv.splat(puff_sprite(rr * ppm, int(self.var[i]), rim, hard=True), cx, cy, col, dark, al)
            elif kind == 'flatclod':
                cv.splat(flat_sprite(rr * ppm, int(self.var[i]), rim, hard=True), cx, cy, col, dark, al)
            elif kind in ('shard', 'flatshard'):
                rb = int((self.rot[i] + self.spin[i] * a * 16 / (2 * math.pi)) % 16)
                cv.splat(shard_sprite(rr * ppm, int(self.var[i]), rb, flat=(kind == 'flatshard')), cx, cy, col, dark, al)
            elif kind in ('drop', 'spark'):
                rp = max(0.8, rr * ppm)
                if self.streak > 0:          # a short streak back along the screen velocity
                    p2 = self.pos(max(0.0, a - self.streak), i); cx2, cy2 = frame.proj(*p2)
                    for s in (0.75, 0.5, 0.25):
                        cv.splat(puff_sprite(rp * (0.5 + 0.5 * s), 0, 0.0, hard=True), cx + (cx2 - cx) * (1 - s), cy + (cy2 - cy) * (1 - s), col, dark, al * s * 0.8)
                if kind == 'spark':
                    cv.splat(puff_sprite(rp * 2.6, 0, 0.0), cx, cy, col, dark, al * 0.35)
                cv.splat(puff_sprite(rp, 0, rim, hard=True), cx, cy, col, dark, al)
        return draw

def render(emitters, frame, t, extra=None):
    cv = Canvas(frame.W, frame.H); cv._fr = frame; items = []
    for e in emitters: items += e.items(t, frame, frame.ppm)
    if extra: items += extra(t)
    for _, fn in sorted(items, key=lambda q: q[0]): fn(cv)
    return cv

# ------------------------------------------------------------------ atlas + crack networks
def atlas(frames, max_w=8192):
    h, w = frames[0].shape[:2]; n = len(frames)
    cols = max(1, min(n, int(round(math.sqrt(n * h / w)))))
    while cols * w > max_w: cols -= 1
    rows = (n + cols - 1) // cols
    A = np.zeros((rows * h, cols * w, 4), np.uint8)
    for i, f in enumerate(frames):
        r, c = divmod(i, cols); A[r * h:(r + 1) * h, c * w:(c + 1) * w] = f
    return A, [cols, rows]

def crack_network(g, seeds, length, speed, branch_p=0.18, step=0.18, jitter=0.35, max_gen=4, clip_r=None, t_ease=None):
    """Random-walk crack polylines in ground metres. seeds: [(x, y, heading_rad, t0)]. Returns segments
    [(x0, y0, x1, y1, t_arrive_at_end, generation)]."""
    segs = []; stack = [(sx, sy, h, t0, 0, length) for sx, sy, h, t0 in seeds]
    while stack:
        x, y, h, t, gen, L = stack.pop(); dist = 0.0
        while dist < L:
            h += g.normal(0, jitter); nx, ny = x + math.cos(h) * step, y + math.sin(h) * step
            if clip_r is not None and math.hypot(nx, ny) > clip_r: break
            t += step / speed; segs.append((x, y, nx, ny, t, gen)); x, y = nx, ny; dist += step
            if gen < max_gen and g.random() < branch_p * step / 0.18 * 0.35:
                stack.append((x, y, h + g.choice([-1, 1]) * g.uniform(0.5, 1.2), t, gen + 1, (L - dist) * g.uniform(0.35, 0.7)))
    return segs

def raster_cracks(segs, frame, t_build, layers, wash=None):
    """Rasterise crack segments into (RGBA8 colour, L8 arrival map). arrival is t / t_build in [0, 1]; 255 = never.
    layers: [(width_px_by_gen fn, colour rgba, delay_s)] drawn widest-first. wash: optional (colour rgba, blur_px, delay_s)."""
    W, H = frame.W, frame.H
    col = Image.new('RGBA', (W, H), (0, 0, 0, 0)); arr = Image.new('F', (W, H), 2.0)
    dc, da = ImageDraw.Draw(col), ImageDraw.Draw(arr)
    items = []
    for x0, y0, x1, y1, t, gen in segs:
        p0 = frame.proj(x0, y0, 0.0); p1 = frame.proj(x1, y1, 0.0)
        for li, (wfn, c, dl) in enumerate(layers):
            items.append((t + dl, li, p0, p1, wfn(gen), c))
    items.sort(key=lambda q: (-q[0], q[1]))
    for tt, li, p0, p1, wpx, c in items:
        if wpx <= 0: continue
        w = max(1, int(round(wpx)))
        dc.line([p0, p1], fill=c, width=w); da.line([p0, p1], fill=float(tt / t_build), width=w)
        if w >= 3:
            r = w / 2.0
            for p in (p0, p1):
                dc.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=c); da.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=float(tt / t_build))
    C = np.asarray(col, np.float32).copy(); R = np.asarray(arr, np.float32).copy()
    if wash is not None:
        wc, blur, dl = wash
        m = ndimage.gaussian_filter((C[..., 3] > 0).astype(np.float32), blur); m = np.clip(m * 2.2, 0, 1)
        wa = ndimage.grey_erosion(np.where(R < 1.5, R, 2.0), size=(int(blur * 2) | 1, int(blur * 2) | 1)) + dl / t_build
        wa = ndimage.gaussian_filter(np.minimum(wa, 2.0), blur * 0.5)
        under = (C[..., 3] == 0) & (m > 0.02)
        C[under] = [wc[0], wc[1], wc[2], 0]; C[..., 3][under] = (m[under] * wc[3])
        R[under] = np.minimum(wa[under], 1.0)
    R = np.where(C[..., 3] > 0, np.clip(R, 0, 1), 1.0)
    return np.clip(C + 0.5, 0, 255).astype(np.uint8), np.clip(R * 254 + 0.5, 0, 255).astype(np.uint8)

def reveal(C, R, progress, fade=1.0, soft=0.015, glint=0.6, glint_w=0.06, glint_col=(235, 246, 255)):
    """Python twin of shaders/spawn_crack_reveal.gdshader (preview + self-check)."""
    a = R.astype(np.float32) / 254.0
    on = np.clip((progress - a) / soft, 0, 1) * (R < 255)
    gl = (1 - np.clip((progress - a) / glint_w, 0, 1)) * on * glint
    rgb = C[..., :3].astype(np.float32) * (1 - gl[..., None]) + np.array(glint_col, np.float32) * gl[..., None]
    out = np.zeros_like(C); out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(C[..., 3].astype(np.float32) * on * fade, 0, 255).astype(np.uint8)
    return out

def save_png(arr, path):
    Image.fromarray(arr).save(path, optimize=True)
    return os.path.getsize(path)

# ------------------------------------------------------------------ crop + flow fields
def autocrop(frames, pivot_px, thr=2, pad=2):
    """Crop every frame to the union of non-empty alpha across the set; returns (frames, pivot_px, [W, H])."""
    al = np.zeros(frames[0].shape[:2], bool)
    for f in frames: al |= f[..., 3] > thr
    ys, xs = np.nonzero(al)
    if len(xs) == 0: return frames, pivot_px, [frames[0].shape[1], frames[0].shape[0]]
    x0, x1 = max(0, xs.min() - pad), min(al.shape[1], xs.max() + 1 + pad); y0, y1 = max(0, ys.min() - pad), min(al.shape[0], ys.max() + 1 + pad)
    if (x1 - x0) % 2: x1 = min(al.shape[1], x1 + 1) if x1 < al.shape[1] else x1; 
    if (y1 - y0) % 2: y1 = min(al.shape[0], y1 + 1) if y1 < al.shape[0] else y1
    out = [np.ascontiguousarray(f[y0:y1, x0:x1]) for f in frames]
    return out, [round(pivot_px[0] - x0, 2), round(pivot_px[1] - y0, 2)], [x1 - x0, y1 - y0]

_NOISE = {}
def _noise_grid(seed, n, sig):
    key = (seed, n, sig)
    if key not in _NOISE:
        g = rng(seed); z = np.zeros((n, n), np.float32)
        for s, w in sig:
            q = ndimage.gaussian_filter(g.standard_normal((n, n)).astype(np.float32), s, mode='wrap'); z += w * q / (q.std() + 1e-6)
        _NOISE[key] = (z - z.mean()) / (z.std() + 1e-6)
    return _NOISE[key]

def flow_layer(frame, t, T, vel, seed, R, thr=0.1, gain=1.4, peak=0.4, col=(1, 1, 1), dark=(0.6, 0.6, 0.7), cell=0.2,
               sig=((6.0, 1.0), (2.2, 0.5), (0.9, 0.22)), edge_jag=0.12, z=0.0, rim=0.45, centre=(0.0, 0.0)):
    """A seamless-looping painted ground wash (mist / fret / smoke bank) on the ground plane, masked to a ragged disc of
    radius R about `centre` (local metres). Two noise phases half a period apart, triangle-weighted (w(0) = w(1) = 0), so frame T == frame 0.
    Returns a draw fn(cv)."""
    n = 512; Z = _noise_grid(seed, n, sig)
    yy, xx = np.mgrid[0:frame.H, 0:frame.W].astype(np.float32)
    X = (xx - frame.ox) / frame.ppm; Y = ((yy - frame.oy) / frame.ppm + math.cos(A) * z) / math.sin(A)
    ph = (t / T) % 1.0; acc = np.zeros_like(X); wsum = 0.0; w2 = 0.0
    for k, phase in enumerate((ph, (ph + 0.5) % 1.0)):
        w = 1.0 - abs(2.0 * phase - 1.0); sx = X - vel[0] * T * phase + 37.0 * k; sy = Y - vel[1] * T * phase + 19.0 * k
        acc += w * ndimage.map_coordinates(Z, [(sy / cell) % n, (sx / cell) % n], order=1, mode='grid-wrap'); wsum += w; w2 += w * w
    f = acc / math.sqrt(max(w2, 1e-6))      # variance-normalised blend: no pulse at the crossfade
    th = np.arctan2(Y - centre[1], X - centre[0]); rr = np.hypot(X - centre[0], Y - centre[1])
    Zr = _noise_grid(seed + 7, 256, ((8.0, 1.0),)); jag = np.clip(1 + edge_jag * ndimage.map_coordinates(Zr, [np.full_like(th, 3.0), (th / (2 * math.pi) * 256) % 256], order=1, mode='grid-wrap'), 1 - edge_jag, 1 + edge_jag)
    mask = np.clip((R * jag - rr) / 1.6, 0, 1) ** 1.2
    a = np.clip((f - thr) * gain, 0, 1) * mask * peak
    a = ndimage.gaussian_filter(a, 1.0)
    e2 = np.clip(a / (peak + 1e-6), 0, 1); rimw = (np.clip(1 - e2 * 1.6, 0, 1) * (e2 > 0.02) * rim)[..., None]
    rgb = np.asarray(col, np.float32) * (1 - rimw) + np.asarray(dark, np.float32) * rimw
    def draw(cv):
        cv.rgb *= (1 - a)[..., None]; cv.rgb += rgb * a[..., None]; cv.a *= (1 - a); cv.a += a
    return draw
