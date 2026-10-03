#!/usr/bin/env python3
# Run C-9 Phase 2, lane DV (drax): PREVIEW of the barrow_v2 spawn-delivery VFX over the greybox camera views.
#   python3 tools/preview_spawn_vfx.py            -> preview/<source>_stills.jpg, preview/spawn_vfx_preview.mp4, preview/spawn_vfx_overview.jpg
# It plays each manifest EXACTLY as the manifest tells KC2 to (events -> segments, fades, loops, y-sort), so the preview is also a
# check of the manifests. The runtime timeline is MOCKED (labelled on every frame): release at t = 0, six ring bodies spawning over
# 0.75 s at polar-disc positions (theta = 2 pi u1, rho = 8 u2), or for p05 the 4.0 s hold then five bodies with mixed am3 D_long.
# Bodies are grey placeholder capsules. The greybox stills are the BX lane's Godot renders (ZOOM-GD, 75.668 px/m, 1920x1080).
import json, math, os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svfx_core import SA, CA, PPM_GD, reveal, rng

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = os.path.abspath(os.path.join(HERE, '..', '..'))
GB = os.path.join(RUN, 'barrow_v2', 'greybox')
OUT = os.path.join(HERE, 'preview'); os.makedirs(OUT, exist_ok=True)
# view targets = the layout's own views (the BX lane re-rendered the stills from layout v2 at 21:56; checked against the anchor markers, <= 4 px)
_LV = {v['id']: tuple(v['target']) for v in json.load(open(os.path.join(RUN, 'barrow_v2', 'layout_v2.json')))['views']}
VIEWS = {pid: (vid + '.png', _LV[vid]) for pid, vid in {'p02': 'V2_p02_barrow_door', 'p01': 'V3_p01_wreck', 'p04': 'V4_p04_hall_door',
         'p06': 'V5_p06_fallen_gable', 'p05': 'V6_p05_mere', 'p03': 'V7_p03_stair_top'}.items()}
DIRS = {'p01': 'p01_wreck', 'p02': 'p02_barrow_door', 'p03': 'p03_sea_cave', 'p04': 'p04_hall_door', 'p05': 'p05_mere_ambush', 'p06': 'p06_fallen_gable'}
W, H = 1920, 1080
try:
    FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 26); FONT_S = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 20)
except Exception:
    FONT = FONT_S = ImageFont.load_default()

class Seg:
    def __init__(self, d, rec):
        self.r = rec; self.s = PPM_GD / rec['px_per_m']; A = Image.open(os.path.join(d, rec['atlas'])).convert('RGBA')
        cw, ch = rec['cell_px']; cols = rec['grid'][0]
        self.cells = []
        for i in range(rec['frames']):
            rr, cc = divmod(i, cols); c = A.crop((cc * cw, rr * ch, (cc + 1) * cw, (rr + 1) * ch))
            self.cells.append(np.asarray(c.resize((max(1, round(cw * self.s)), max(1, round(ch * self.s))), Image.BILINEAR)))
        self.reveal = None; self.R = None
        if 'reveal_map' in rec:
            C = np.asarray(A); R = np.asarray(Image.open(os.path.join(d, rec['reveal_map'])))
            self.C, self.R = C, R
        self.fps = rec.get('fps') or 1; pb = rec['playback']
        self.intro = pb.get('intro'); self.loop = pb.get('loop'); self.oneshot = pb.get('oneshot')
    def frame_at(self, age):
        """Frame index for an age since the segment's start event, per its playback block."""
        j = int(math.floor(age * self.fps + 1e-9))
        if self.oneshot: return j if j <= self.oneshot[1] else None
        if self.intro:
            if j <= self.intro[1]: return j
            j -= self.intro[1] + 1
        L = self.loop[1] - self.loop[0] + 1; return self.loop[0] + j % L
    def cell_reveal(self, progress, fade):
        img = reveal(self.C, self.R, progress, fade)
        cw, ch = self.r['cell_px']
        return np.asarray(Image.fromarray(img).resize((round(cw * self.s), round(ch * self.s)), Image.BILINEAR))

def to_screen(x, y, z, tgt):
    return 960 + PPM_GD * (x - tgt[0]), 540 + PPM_GD * SA * (y - tgt[1]) - PPM_GD * CA * z

def paste(canvas, cell, sx, sy, piv, s, alpha=1.0):
    im = Image.fromarray(cell)
    if alpha < 0.999:
        a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] * max(0.0, alpha)).astype(np.uint8); im = Image.fromarray(a)
    x0 = int(round(sx - piv[0] * s)); y0 = int(round(sy - piv[1] * s))
    canvas.alpha_composite(im, (x0, y0)) if (x0 >= 0 and y0 >= 0) else _paste_clip(canvas, im, x0, y0)

def _paste_clip(canvas, im, x0, y0):
    cx, cy = max(0, -x0), max(0, -y0)
    if cx >= im.width or cy >= im.height: return
    canvas.alpha_composite(im.crop((cx, cy, im.width, im.height)), (x0 + cx, y0 + cy))

def body_token(canvas, sx, sy, alpha=1.0):
    d = ImageDraw.Draw(canvas, 'RGBA'); w = 0.36 * PPM_GD; h = 1.8 * PPM_GD * CA
    d.ellipse([sx - w * 1.2, sy - w * 0.45, sx + w * 1.2, sy + w * 0.45], fill=(40, 36, 52, int(80 * alpha)))
    d.rounded_rectangle([sx - w, sy - h, sx + w, sy], radius=int(w), fill=(70, 64, 82, int(255 * alpha)), outline=(30, 26, 38, int(255 * alpha)), width=2)

def fade_val(t, t_on, fin, t_off, fout):
    a = min(1.0, max(0.0, (t - t_on) / fin)) if fin > 0 else 1.0
    if t_off is not None and t > t_off: a *= max(0.0, 1 - (t - t_off) / fout)
    return a

def timeline(pid):
    g = rng(900 + int(pid[1:])); P = json.load(open(os.path.join(HERE, DIRS[pid], f'vfx_{pid}.json')))
    ax, ay = P['anchor_world_m']
    if pid == 'p05':
        n = 5; ts = [4.0] * n; Ds = [4.9, 1.533, 0.867, 2.833, 1.667]
    else:
        n = 6; ts = list(np.round(np.linspace(0.0, 0.75, n), 3)); Ds = [0.0] * n
    th = g.uniform(0, 2 * math.pi, n); rho = 8.0 * g.random(n)
    bodies = [dict(x=ax + r * math.cos(t_), y=ay + r * math.sin(t_), t=ts[i], D=Ds[i]) for i, (t_, r) in enumerate(zip(th, rho))]
    return P, bodies

def compose(pid, P, segs, bodies, bg, t, tgt):
    cv = bg.copy(); recs = {s.r['id']: s for s in segs}
    under, ys = [], []
    if pid != 'p05':
        t_done = max(b['t'] for b in bodies)
        door = recs[f'{pid}_door']; intro_s = (door.intro[1] + 1) / door.fps; loop_s = (door.loop[1] - door.loop[0] + 1) / door.fps
        t_hold_end = max(t_done + 0.8, intro_s + loop_s)
        # door: intro + whole loops until hold end, then a 1.0 s fade
        if t >= 0:
            a = fade_val(t, 0, 0, t_hold_end, 1.0)
            if a > 0:
                pv = door.r['draw_layer']['ysort_ground_m']; sx, sy = to_screen(pv[0], pv[1], door.r['pivot_world_m'][2], tgt)
                ys.append((pv[1], lambda c, sx=sx, sy=sy, a=a, f=door.frame_at(t): paste(c, door.cells[f], sx, sy, door.r['pivot_px'], door.s, a)))
        g_id = [k for k in recs if k.startswith(f'{pid}_ground')][0]; gs = recs[g_id]
        if t >= 0:
            a = fade_val(t, 0, 0.6, t_done + 0.8, 1.5)
            pw = gs.r['pivot_world_m']; sx, sy = to_screen(pw[0], pw[1], 0, tgt)
            if gs.R is not None:
                prog = min(1.0, t / gs.r['build_s']); a2 = fade_val(t, 0, 0, t_done + 0.8, 1.5)
                if a2 > 0: under.append(lambda c, sx=sx, sy=sy, p=prog, a2=a2: paste(c, gs.cell_reveal(p, a2), sx, sy, gs.r['pivot_px'], gs.s))
            elif a > 0:
                under.append(lambda c, sx=sx, sy=sy, a=a, f=gs.frame_at(t): paste(c, gs.cells[f], sx, sy, gs.r['pivot_px'], gs.s, a))
        arr = recs[f'{pid}_arrival']
        for b in bodies:
            if t >= b['t']:
                sx, sy = to_screen(b['x'], b['y'], 0, tgt); ys.append((b['y'], lambda c, sx=sx, sy=sy: body_token(c, sx, sy)))
                f = arr.frame_at(t - b['t'])
                if f is not None: ys.append((b['y'] + 0.05, lambda c, sx=sx, sy=sy, f=f: paste(c, arr.cells[f], sx, sy, arr.r['pivot_px'], arr.s)))
    else:
        cr = recs['p05_hold_cracks']; pw = cr.r['pivot_world_m']; sx, sy = to_screen(pw[0], pw[1], 0, tgt)
        t_last = max(b['t'] + b['D'] for b in bodies)
        if t >= 0:
            prog = min(1.0, t / 4.0); a2 = fade_val(t, 0, 0, t_last, 2.0)
            if a2 > 0: under.append(lambda c, sx=sx, sy=sy, p=prog, a2=a2: paste(c, cr.cell_reveal(p, a2), sx, sy, cr.r['pivot_px'], cr.s))
        hole, burst = recs['p05_hole'], recs['p05_burst']
        for b in bodies:
            if t >= b['t']:
                sx, sy = to_screen(b['x'], b['y'], 0, tgt); age = t - b['t']
                a = fade_val(t, b['t'], 0, b['t'] + b['D'], 1.0)
                if a > 0: under.append(lambda c, sx=sx, sy=sy, a=a, f=hole.frame_at(age): paste(c, hole.cells[f], sx, sy, hole.r['pivot_px'], hole.s, a))
                ys.append((b['y'], lambda c, sx=sx, sy=sy: body_token(c, sx, sy)))
                f = burst.frame_at(age)
                if f is not None: ys.append((b['y'] + 0.05, lambda c, sx=sx, sy=sy, f=f: paste(c, burst.cells[f], sx, sy, burst.r['pivot_px'], burst.s)))
    for fn in under: fn(cv)
    for _, fn in sorted(ys, key=lambda q: q[0]): fn(cv)
    d = ImageDraw.Draw(cv, 'RGBA'); d.rectangle([0, 0, W, 44], fill=(20, 20, 28, 170))
    label = f"{pid}  {P['deliverer']}    t = {t:+.2f} s"
    label += "   (hold: cracks build 0 -> 4.0 s; bodies burst at 4.0 s)" if pid == 'p05' else "   (release at 0; six ring bodies spawn 0 -> 0.75 s)"
    d.text((16, 8), label, fill=(255, 255, 255, 255), font=FONT)
    d.text((16, H - 34), "PREVIEW: mocked runtime timeline; grey capsules = placeholder bodies; greybox camera ZOOM-GD 75.668 px/m, pitch 52.9535 deg, zero yaw", fill=(255, 255, 255, 230), font=FONT_S)
    return cv

def main():
    order = ['p02', 'p01', 'p03', 'p04', 'p06', 'p05']; fps = 15
    film_dir = os.environ.get('SVFX_FRAMES') or os.path.join(os.environ.get('TMPDIR', '/tmp'), 'svfx_frames'); os.makedirs(film_dir, exist_ok=True); k = 0
    overview = []
    for pid in order:
        P, bodies = timeline(pid); d = os.path.join(HERE, DIRS[pid]); segs = [Seg(d, s) for s in P['segments']]
        f, tgt = VIEWS[pid]; bg = Image.open(os.path.join(GB, f)).convert('RGBA')
        T_end = 11.2 if pid == 'p05' else 5.0
        keys = [0.05, 0.3, 0.8, 1.6, 3.0, 4.6] if pid != 'p05' else [0.5, 2.0, 3.5, 3.95, 4.3, 6.5]
        stills = []
        for t in np.arange(-0.4, T_end, 1.0 / fps):
            im = compose(pid, P, segs, bodies, bg, float(t), tgt)
            im.convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(film_dir, f'f{k:05d}.jpg'), quality=88); k += 1
        for t in keys:
            stills.append(compose(pid, P, segs, bodies, bg, t, tgt).convert('RGB'))
        sw, sh = 960, 540; sheet = Image.new('RGB', (sw * 3, sh * 2), (0, 0, 0))
        for i, s in enumerate(stills): sheet.paste(s.resize((sw, sh), Image.LANCZOS), ((i % 3) * sw, (i // 3) * sh))
        p = os.path.join(OUT, f'{DIRS[pid]}_stills.jpg'); sheet.save(p, quality=86); print('wrote', p, flush=True)
        overview.append(stills[3 if pid != 'p05' else 4].resize((640, 360), Image.LANCZOS))
    ov = Image.new('RGB', (640 * 3, 360 * 2)); [ov.paste(o, ((i % 3) * 640, (i // 3) * 360)) for i, o in enumerate(overview)]
    ov.save(os.path.join(OUT, 'spawn_vfx_overview.jpg'), quality=86)
    mp4 = os.path.join(OUT, 'spawn_vfx_preview.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(film_dir, 'f%05d.jpg'), '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-crf', '24', '-preset', 'medium', mp4], check=True)
    print('wrote', mp4, os.path.getsize(mp4))
    print('film frames (scratch, outside the repo):', film_dir)

if __name__ == '__main__':
    main()
