#!/usr/bin/env python3
# Run C-9 Phase 2, lane DV (drax): barrow_v2 per-source SPAWN-DELIVERY VFX atlases + manifests (R-C9-145 spawn plan).
#   python3 tools/make_spawn_vfx.py [source ...]      (sources: p01 p02 p03 p04 p05 p06; default all)
# Reads barrow_v2/layout_v2.json (anchors, deliverer features) -- read-only. Writes <source dir>/*.png + vfx_<source>.json.
# BINDING (KC2): every segment hangs on a runtime ORACLE EVENT (named in each manifest's "events"); nothing free-runs.
import json, math, os, sys, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svfx_core import *

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = os.path.abspath(os.path.join(HERE, '..', '..'))                      # runs/C-9
LAYOUT_P = os.path.join(RUN, 'barrow_v2', 'layout_v2.json')
LAYOUT = json.load(open(LAYOUT_P))
LAYOUT_SHA = hashlib.sha256(open(LAYOUT_P, 'rb').read()).hexdigest()[:16]
PTS = {p['id']: p for p in LAYOUT['anchors']['points']}
FEAT = {f['id']: f for f in LAYOUT['features']}
DISC_R = float(LAYOUT['anchors']['scatter']['disc_radius_m'])          # 8.0 m (polar: theta = 2 pi u1, rho = 8 u2)

PPM_DOOR = PPM_RENDER / 3.0      # 50.446 px/m   door / deliverer segments (soft smoke, ~2/3 of play-zoom 1:1)
PPM_POOL = PPM_RENDER / 5.0      # 30.267 px/m   ground pools (soft mist / smoke / ash; drawn x2.5 at ZOOM-GD)
PPM_FINE = PPM_RENDER / 2.0      # 75.668 px/m   arrivals, bursts, crack fields (= 1:1 at ZOOM-GD play zoom)

def v2(a): return np.array(a, float)
def unit(v): v = v2(v); return v / np.linalg.norm(v)
def anchor(pid): return v2([PTS[pid]['x'], PTS[pid]['y']])
def fp_centre(fid):
    f = FEAT[fid]; fp = np.array(f.get('footprint') or f.get('polygon'), float); return fp.mean(0)
def fp_nearest(fid, to):
    f = FEAT[fid]; fp = np.array(f.get('footprint') or f.get('polygon'), float); return fp[np.argmin(np.linalg.norm(fp - to, axis=1))]
def fp_nearest_edge(fid, to):
    f = FEAT[fid]; fp = np.array(f.get('footprint') or f.get('polygon'), float); best, bd = None, 1e9
    for a, b in zip(fp, np.roll(fp, -1, 0)):
        ab = b - a; u_ = np.clip(np.dot(to - a, ab) / max(np.dot(ab, ab), 1e-9), 0, 1); q = a + u_ * ab; dd = np.linalg.norm(q - to)
        if dd < bd: best, bd = q, dd
    return best
def bearing_vec(b):  # compass bearing (clockwise from north) -> sim (x east, y south)
    b = math.radians(b); return v2([math.sin(b), -math.cos(b)])

# ------------------------------------------------------------------ samplers
def U(lo, hi): return lambda g, n: g.uniform(lo, hi, n)
def births_uniform(T): return lambda g, n: g.uniform(0, T, n)
def births_bursts(times, jit): return lambda g, n: np.array(times)[g.integers(0, len(times), n)] + g.normal(0, jit, n)
def in_disc(r, z=(0, 0)):
    def f(g, n):
        th = g.uniform(0, 2 * math.pi, n); rr = r * np.sqrt(g.random(n))
        return np.stack([rr * np.cos(th), rr * np.sin(th), g.uniform(z[0], z[1], n)], 1)
    return f
def ring(r0, r1, z=(0, 0)):
    def f(g, n):
        th = g.uniform(0, 2 * math.pi, n); rr = g.uniform(r0, r1, n)
        return np.stack([rr * np.cos(th), rr * np.sin(th), g.uniform(z[0], z[1], n)], 1)
    return f
def strip(centre, along, half, back, z, depth=(0, 0)):
    """Points across an opening: centre + along*U(-half,half) + back*U(depth) at height U(z)."""
    c, a, bk = np.r_[np.asarray(centre, float), 0.0], np.r_[np.asarray(along, float), 0.0], np.r_[np.asarray(back, float), 0.0]
    def f(g, n):
        return c + a * g.uniform(-half, half, n)[:, None] + bk * g.uniform(depth[0], depth[1], n)[:, None] + np.stack([np.zeros(n), np.zeros(n), g.uniform(z[0], z[1], n)], 1)
    return f
def vel_dir(d, sp, lat=None, latsd=0.0, vz=(0, 0)):
    d3 = np.r_[d, 0.0]; l3 = np.r_[(-d[1], d[0]) if lat is None else lat, 0.0]
    def f(g, n, p0):
        return d3 * g.uniform(sp[0], sp[1], n)[:, None] + l3 * g.normal(0, latsd, n)[:, None] + np.stack([np.zeros(n), np.zeros(n), g.uniform(vz[0], vz[1], n)], 1)
    return f
def vel_radial(sp, vz, extra=(0, 0)):
    def f(g, n, p0):
        r = np.hypot(p0[:, 0], p0[:, 1]) + 1e-6; s = g.uniform(sp[0], sp[1], n)
        return np.stack([p0[:, 0] / r * s + extra[0], p0[:, 1] / r * s + extra[1], g.uniform(vz[0], vz[1], n)], 1)
    return f

# ------------------------------------------------------------------ palette (cool winter; warm only where fire is the source)
SNOW, SNOW_D = (0.96, 0.97, 1.00), (0.66, 0.69, 0.81)
MIST, MIST2, MIST_D = (0.85, 0.88, 0.95), (0.76, 0.81, 0.91), (0.58, 0.64, 0.78)
WATER, WATER_D = (0.78, 0.88, 0.96), (0.38, 0.53, 0.67)
FOAM, FOAM_D = (0.95, 0.97, 1.00), (0.62, 0.71, 0.82)
ICE, ICE_D = (0.86, 0.93, 0.98), (0.34, 0.50, 0.64)
SMOKE_DK, SMOKE_LT, SMOKE_D = (0.40, 0.39, 0.44), (0.67, 0.66, 0.71), (0.25, 0.24, 0.29)
ASH, ASH2, ASH_D = (0.47, 0.46, 0.50), (0.64, 0.63, 0.67), (0.29, 0.28, 0.32)
EMBER, EMBER_D = (1.00, 0.66, 0.28), (0.82, 0.30, 0.10)
SPARK, SPARK_D = (1.00, 0.80, 0.42), (0.86, 0.38, 0.12)

CAMERA = {"projection": "orthographic", "pitch_deg": ALPHA_DEG, "yaw_deg": 0.0,
          "law": "screen_x = ppm*x ; screen_y = ppm*sin(a)*y - ppm*cos(a)*z (sim frame: x east, y SOUTH, z up)",
          "source": "reincarnated-godot/kc2_runtime/play/kc2play_projection.gd", "ppm_render_join1": PPM_RENDER,
          "runtime_scale_rule": "draw each cell UNROTATED with its pivot_px on the projected pivot point, scaled by s = proj.ppm / px_per_m (the JOIN rule; at ZOOM-GD proj.ppm = 75.668)"}

# ------------------------------------------------------------------ segment renderers
def seg_flipbook(emitters, frame, fps, intro_s, loop_s, t0=0.0, extra=None):
    """intro frames t in [t0, t0+intro); loop frames t in [t0+intro, t0+intro+loop). Seamless when intro >= every life."""
    n_i = int(round(intro_s * fps)); n_l = int(round(loop_s * fps)); out = []
    for j in range(n_i + n_l):
        out.append(render(emitters, frame, t0 + j / fps, extra).rgba8())
    return out, n_i, n_l

def write_atlas(src_dir, name, frames, frame=None):
    if frame is not None:                 # crop to the union of drawn pixels; the pivot moves with the crop
        frames, pv, wh = autocrop(frames, frame.pivot_px)
        frame.crop = dict(pivot_px=pv, cell_px=wh)
    A, grid = atlas(frames); p = os.path.join(src_dir, name + '.png'); sz = save_png(A, p)
    return dict(atlas=name + '.png', grid=grid, atlas_px=[A.shape[1], A.shape[0]], png_bytes=sz, vram_bytes=int(A.shape[0] * A.shape[1] * 4)), A

def seg_record(sid, info, frame, fps, n_frames, playback, loop, layer, pivot_world, events, **kw):
    cp = getattr(frame, 'crop', None)
    r = dict(id=sid, **info, frames=n_frames, cell_px=cp['cell_px'] if cp else [frame.W, frame.H], px_per_m=round(frame.ppm, 6), fps=fps,
             duration_s=round(n_frames / fps, 4), playback=playback, loop=loop, draw_layer=layer,
             pivot_px=cp['pivot_px'] if cp else frame.pivot_px, pivot_world_m=[v if isinstance(v, str) else round(float(v), 4) for v in pivot_world], footprint_m=frame.box,
             cell_m=[round(c / frame.ppm, 4) for c in (cp['cell_px'] if cp else [frame.W, frame.H])], events=events, alpha="straight", colorspace="sRGB", blend="normal (mix; no additive)")
    r.update(kw); return r

LAYER_GROUND = "ground: above the painted floor, BELOW every y-sorted actor"
def LAYER_YSORT(pt, note=''): return {"mode": "ysort", "ysort_ground_m": [round(float(pt[0]), 4), round(float(pt[1]), 4)], "note": note or "y-sorted with the actors on this ground point (the projection law's draw order)"}

def door_events(pid):
    return {"start": f"EV_POINT_RELEASE({pid}): play 'intro' once from its frame 0",
            "hold": f"then repeat 'loop' until EV_POINT_RELEASE_DONE({pid}) + 0.8 s (STRETCHABLE: whole loops; the release window comes from the runtime's two-segment release warp)",
            "min_hold": "intro + one full loop, even if the release is instantaneous",
            "end": "fade modulate.a 1 -> 0 over 1.0 s while the loop keeps playing; then free"}
def ground_events(pid):
    return {"start": f"EV_POINT_RELEASE({pid}): start the loop at frame 0 and fade modulate.a 0 -> 1 over 0.6 s",
            "hold": f"loop until EV_POINT_RELEASE_DONE({pid}) + 0.8 s (stretchable)",
            "end": "fade modulate.a 1 -> 0 over 1.5 s; then free"}
def arrival_events(pid):
    return {"start": f"EV_BODY_SPAWN({pid}, body, x, y): one-shot at the body's rolled landing point (theta = 2 pi u1, rho = 8 u2 about the anchor), frame 0 on the spawn tick -- frame 0 is dense on purpose: it covers the body's pop-in",
            "end": "free on the last frame",
            "scale": "x max(1, record_radius_m / 0.8) for bodies wider than 1.6 m (true_size packs)"}

# ------------------------------------------------------------------ the six sources
def build(pid, out_root):
    src_dir = os.path.join(out_root, SRC_DIRS[pid]); os.makedirs(src_dir, exist_ok=True)
    fn = globals()['src_' + pid]; segs, extra = fn(src_dir)
    man = {"source": pid, "deliverer": PTS[pid]['delivered_by'], "anchor_world_m": [PTS[pid]['x'], PTS[pid]['y']],
           "scatter": "polar disc r 8 m about the anchor (oracle: theta = 2 pi u1, rho = 8 u2); every 'ground' segment covers it",
           "layout": "barrow_v2/layout_v2.json sha256_16 " + LAYOUT_SHA, "camera": CAMERA, "segments": segs,
           "generator": "join1_vfx/barrow_v2_spawn/tools/make_spawn_vfx.py (procedural; no paid calls, no Godot/Blender)"}
    man.update(extra)
    man["vram_bytes_total"] = int(sum(s.get('vram_bytes', 0) + s.get('reveal_vram_bytes', 0) for s in segs))
    with open(os.path.join(src_dir, f'vfx_{pid}.json'), 'w') as f:
        json.dump(man, f, indent=2, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, 'item') else str(o)); f.write('\n')
    return man

ARR_T0 = 0.6     # one-shot frame j samples t = (j + 0.6) / fps: frame 0 is already dense (it covers the body's pop-in)
SRC_DIRS = {'p01': 'p01_wreck', 'p02': 'p02_barrow_door', 'p03': 'p03_sea_cave', 'p04': 'p04_hall_door', 'p05': 'p05_mere_ambush', 'p06': 'p06_fallen_gable'}

def door_and_ground_and_arrival(src_dir, pid, door, ground, arrival, door_note):
    """door = (emitters, frame, fps, intro, loop, pivot_xy, extra); ground = (emitters, frame, fps, loop, warm, extra) or a dict
    for a reveal segment; arrival = (emitters, frame, fps, dur)."""
    segs = []
    ems, fr, fps, it, lp, pv, ex = door
    frames, ni, nl = seg_flipbook(ems, fr, fps, it, lp, extra=ex); info, _ = write_atlas(src_dir, f'{pid}_door', frames, fr)
    segs.append(seg_record(f'{pid}_door', info, fr, fps, ni + nl, {"intro": [0, ni - 1], "loop": [ni, ni + nl - 1]}, "intro once, then loop",
                           LAYER_YSORT(pv, door_note), [pv[0], pv[1], 0.0], door_events(pid)))
    if isinstance(ground, dict):
        segs.append(ground)
    else:
        ems, fr, fps, lp, warm, ex = ground
        frames, _, nl = seg_flipbook(ems, fr, fps, 0.0, lp, t0=warm, extra=ex); info, _ = write_atlas(src_dir, f'{pid}_ground', frames, fr)
        segs.append(seg_record(f'{pid}_ground', info, fr, fps, nl, {"loop": [0, nl - 1]}, "loop (seamless)", LAYER_GROUND,
                               [*anchor(pid), 0.0], ground_events(pid)))
    ems, fr, fps, dur = arrival
    frames = [render(ems, fr, (j + ARR_T0) / fps).rgba8() for j in range(int(round(dur * fps)))]; info, _ = write_atlas(src_dir, f'{pid}_arrival', frames, fr)
    segs.append(seg_record(f'{pid}_arrival', info, fr, fps, len(frames), {"oneshot": [0, len(frames) - 1]}, "one-shot",
                           {"mode": "ysort", "ysort_ground_m": "the body's own landing point + 0.05 m south (drawn just in front of its own body)"},
                           ["body.x", "body.y", 0.0], arrival_events(pid)))
    return segs

# ---- p02: the barrow door (N; bosses). Cold mist rolls out across the ground; bodies rise up through snow inside it.
def src_p02(src_dir):
    pid = 'p02'; f = bearing_vec(FEAT['barrow_door']['faces_deg']); lat = v2([-f[1], f[0]])
    door_pt = fp_centre('barrow_door') + 0.5 * f; anc = anchor(pid)
    fps, T = 8, 1.5
    mist = Emitter(90, 21, 'puff', MIST, MIST_D, 0.55, U(1.1, 1.5), births_uniform(T), strip([0, 0], lat, 1.1, f, (0.2, 2.2), (-0.4, 0.0)),
                   vel_dir(f, (2.6, 4.6), lat, 0.9, (-0.6, 0.0)), drag=0.75, drift=(0.9 * f[0], 0.9 * f[1], -0.6), size=(0.4, 0.7),
                   swell=(0.8, 2.6), T=T, rim=0.4, col2=MIST2, zfloor=0.2)
    breath = Emitter(24, 22, 'puff', (0.70, 0.75, 0.86), MIST_D, 0.45, U(0.6, 0.9), births_uniform(T), strip([0, 0], lat, 0.9, f, (0.4, 2.2), (-0.5, -0.2)),
                     vel_dir(f, (0.8, 1.4), lat, 0.3, (0.0, 0.2)), drag=1.2, size=(0.3, 0.5), swell=(0.8, 1.6), T=T, rim=0.4)
    door_fr = Frame((-5.5, 5.5), (-1.5, 8.5), (0.0, 3.6), PPM_RENDER / 4.0)   # pure mist: 37.8 px/m is enough
    # the pool: lying mist sheets drifting away from the door + a few low billboards
    pool_fl = Emitter(26, 23, 'flatpuff', MIST, MIST_D, 0.34, U(3.0, 5.0), births_uniform(2.0), in_disc(8.0, (0.05, 0.1)),
                      lambda g, n, p: np.zeros((n, 3)), drift=(0.28 * f[0], 0.28 * f[1], 0), size=(1.4, 2.3), swell=(0.85, 1.25), T=2.0,
                      rim=0.45, rise=0.3, fade_pow=1.0, col2=MIST2)
    pool_bb = Emitter(18, 24, 'puff', MIST, MIST_D, 0.26, U(2.0, 3.0), births_uniform(2.0), in_disc(8.0, (0.2, 0.6)),
                      lambda g, n, p: np.zeros((n, 3)), drift=(0.3 * f[0], 0.3 * f[1], 0.05), size=(0.6, 1.0), swell=(0.8, 1.4), T=2.0,
                      rim=0.4, rise=0.3, fade_pow=1.0)
    pool_fr = Frame((-10.0, 10.0), (-10.0, 10.0), (0.0, 1.6), PPM_POOL)
    clods = Emitter(26, 25, 'clod', SNOW, SNOW_D, 1.0, 0.66, U(0.0, 0.06), ring(0.2, 0.6, (0.05, 0.3)), vel_radial((0.6, 1.6), (2.0, 3.6)),
                    grav=(0, 0, -9.8), ground_kill=True, size=(0.05, 0.11), swell=(1, 1), rim=0.5, fade_pow=0.3, rise=0.01)
    burst = Emitter(14, 26, 'puff', SNOW, SNOW_D, 0.85, U(0.45, 0.66), U(0.0, 0.05), in_disc(0.5, (0.0, 0.9)), vel_radial((0.4, 1.0), (1.0, 2.2)),
                    drag=3.0, size=(0.35, 0.6), swell=(0.9, 1.6), rim=0.35, rise=0.01)
    curl = Emitter(8, 27, 'puff', MIST, MIST_D, 0.5, 0.66, U(0.0, 0.15), ring(0.3, 0.8, (0.05, 0.3)), vel_radial((0.5, 1.0), (0.1, 0.4)),
                   drag=1.5, size=(0.4, 0.6), swell=(0.9, 1.8), rim=0.4, rise=0.05)
    arr_fr = Frame((-1.7, 1.7), (-1.7, 1.7), (0.0, 2.6), PPM_FINE)
    segs = door_and_ground_and_arrival(src_dir, pid,
        ([mist, breath], door_fr, fps, T, T, door_pt, None),
        ([pool_bb], pool_fr, 6, 2.0, 6.0, lambda t: [(-1e12, flow_layer(pool_fr, t, 2.0, 0.55 * f, 202, 8.6, thr=-0.35, gain=0.9, peak=0.5,
                                                                         col=MIST, dark=MIST_D, rim=0.5))]),
        ([curl, burst, clods], arr_fr, 24, 0.6667),
        "the barrow door is NORTH of the patch, so the door mist y-sorts BEHIND bodies on the patch")
    return segs, {"deliverer_world_m": [round(float(door_pt[0]), 4), round(float(door_pt[1]), 4)],
                  "deliverer_feature": "barrow_door (centre + 0.5 m along its facing, 196.71 deg)"}

# ---- p01: the wreck (W). Cracks race across the shore ice; bodies come up from under it, water sheeting off.
def crack_layers(scale=1.0):
    return [(lambda gen: (5.0 - 0.9 * gen) * scale, (226, 240, 250, 140), 0.05),
            (lambda gen: (3.0 - 0.5 * gen) * scale, (72, 104, 130, 225), 0.02),
            (lambda gen: (1.6 - 0.2 * gen) * scale, (26, 40, 56, 255), 0.0)]

def reveal_segment(src_dir, pid, name, segs_c, build_s, wash, fr, events, layer=LAYER_GROUND, extra_kw=None):
    C, R = raster_cracks(segs_c, fr, build_s, crack_layers(), wash)
    p1 = os.path.join(src_dir, f'{name}.png'); p2 = os.path.join(src_dir, f'{name}_reveal.png')
    s1 = save_png(C, p1); s2 = save_png(R, p2)
    rec = dict(id=name, atlas=f'{name}.png', reveal_map=f'{name}_reveal.png', frames=1, grid=[1, 1], atlas_px=[fr.W, fr.H],
               cell_px=[fr.W, fr.H], png_bytes=s1 + s2, vram_bytes=fr.W * fr.H * 4, reveal_vram_bytes=fr.W * fr.H,
               px_per_m=round(fr.ppm, 6), build_s=build_s, shader="../shaders/spawn_crack_reveal.gdshader",
               playback={"reveal": "uniform progress = clamp((t_now - t_event) / build_s, 0, 1); hold at 1"},
               loop=False, draw_layer=layer, pivot_px=fr.pivot_px, pivot_world_m=[*map(lambda v: round(float(v), 4), anchor(pid)), 0.0],
               footprint_m=fr.box, cell_m=fr.cell_m, events=events, alpha="straight", colorspace="sRGB", blend="normal (mix)",
               reveal_encoding="reveal_map.r = arrival / build_s (0..1, 8-bit; 1.0 = never); a pixel shows once progress passes it; the front carries a short pale glint")
    if extra_kw: rec.update(extra_kw)
    return rec, C, R

def src_p01(src_dir):
    pid = 'p01'; anc = anchor(pid); d_in = unit(-anc)          # toward the start, i.e. away from the wreck (east)
    rail = fp_nearest_edge('wreck_hull', anc); lat = v2([-d_in[1], d_in[0]])
    fps, T = 12, 1.0
    sheet = Emitter(110, 11, 'drop', WATER, WATER_D, 0.9, U(0.55, 0.8), births_uniform(T), strip([0, 0], lat, 1.7, d_in, (1.3, 1.75), (-0.1, 0.1)),
                    vel_dir(d_in, (0.4, 1.2), lat, 0.15, (-0.2, 0.3)), grav=(0, 0, -9.8), ground_kill=True, size=(0.022, 0.045), swell=(1, 1),
                    T=T, rim=0.4, streak=0.07, fade_pow=0.2, rise=0.02)
    foot = Emitter(26, 12, 'puff', FOAM, FOAM_D, 0.5, U(0.35, 0.55), births_uniform(T), strip([0, 0], lat, 1.7, d_in, (0.02, 0.1), (0.3, 1.0)),
                   vel_dir(d_in, (0.1, 0.4), lat, 0.2, (0.4, 0.9)), drag=2.5, size=(0.12, 0.24), swell=(0.8, 1.6), T=T, rim=0.35, rise=0.05)
    door_fr = Frame((-1.4, 2.6), (-2.4, 2.4), (0.0, 2.1), PPM_DOOR)
    # the ice-crack field: cracks race in from the wreck side across the disc in 0.9 s
    g = rng(101); seeds = []
    for i in range(5):
        off = g.uniform(-5.5, 5.5); p = -d_in * 8.2 + lat * off
        if np.linalg.norm(p) > 8.3: p = p / np.linalg.norm(p) * 8.2
        h = math.atan2(d_in[1], d_in[0]) + g.normal(0, 0.35); seeds.append((p[0], p[1], h, g.uniform(0, 0.12)))
    segs_c = crack_network(g, seeds, 16.5, 19.0, branch_p=0.12, step=0.2, jitter=0.28, max_gen=3, clip_r=8.4)
    fr = Frame((-8.7, 8.7), (-8.7, 8.7), (0.0, 0.0), PPM_FINE)
    ground, C, R = reveal_segment(src_dir, pid, 'p01_ground_cracks', segs_c, 0.9, ((88, 118, 140, 90), 5, 0.25), fr,
        {"start": f"EV_POINT_RELEASE({pid}): progress 0 -> 1 over build_s 0.9 s (the cracks race in from the wreck side)",
         "hold": f"progress held at 1 until EV_POINT_RELEASE_DONE({pid}) + 0.8 s",
         "end": "fade 1 -> 0 over 1.5 s (shader uniform 'fade'); then free"})
    shards = Emitter(10, 13, 'shard', ICE, ICE_D, 1.0, U(0.6, 0.72), U(0.0, 0.04), ring(0.35, 0.6, (0.02, 0.1)), vel_radial((0.4, 1.0), (1.2, 2.4)),
                     grav=(0, 0, -9.8), ground_kill=True, size=(0.08, 0.15), swell=(1, 1), rim=0.9, fade_pow=0.3, rise=0.01)
    runoff = Emitter(46, 14, 'drop', WATER, WATER_D, 0.9, U(0.35, 0.55), U(0.0, 0.3), ring(0.15, 0.45, (0.4, 1.8)), vel_radial((0.2, 0.5), (-0.6, 0.0)),
                     grav=(0, 0, -9.8), ground_kill=True, size=(0.018, 0.035), swell=(1, 1), rim=0.4, streak=0.05, fade_pow=0.2, rise=0.02)
    splash = Emitter(12, 15, 'puff', FOAM, FOAM_D, 0.8, U(0.4, 0.6), U(0.0, 0.05), in_disc(0.55, (0.0, 0.5)), vel_radial((0.3, 0.9), (0.8, 1.8)),
                     drag=3.0, size=(0.3, 0.5), swell=(0.9, 1.6), rim=0.35, rise=0.01)
    arr_fr = Frame((-1.7, 1.7), (-1.7, 1.7), (0.0, 2.4), PPM_FINE)
    segs = door_and_ground_and_arrival(src_dir, pid, ([sheet, foot], door_fr, fps, 0.8, T, rail, None), ground,
                                       ([splash, shards, runoff], arr_fr, 24, 0.75),
                                       "water sheeting off the wreck's floor-side rail; the rail is WEST of the patch")
    return segs, {"deliverer_world_m": [round(float(rail[0]), 4), round(float(rail[1]), 4)],
                  "deliverer_feature": "wreck_hull (the point of its footprint nearest the anchor = the floor-side rail)"}

# ---- p03: the sea cave (S). Spray bursts up over the cliff lip.
def src_p03(src_dir):
    pid = 'p03'; anc = anchor(pid); u = unit(anc); lip = anc + u * 9.2; lat = v2([-u[1], u[0]])
    fps, T = 12, 1.5
    onshore = -u
    def kill(p): return p[2] < 0.0 and (p[0] * u[0] + p[1] * u[1]) < 0.0      # under the land (north of the lip)
    drops = Emitter(120, 31, 'drop', FOAM, WATER_D, 0.95, U(0.9, 1.4), births_bursts([0.05, 0.8], 0.1), strip([0, 0], lat, 2.0, u, (-4.0, -1.0), (0.3, 1.2)),
                    vel_dir(onshore, (0.6, 1.6), lat, 0.6, (6.0, 8.5)), drag=0.3, grav=(0, 0, -9.8), size=(0.03, 0.06), swell=(1, 1), T=T,
                    rim=0.45, streak=0.05, fade_pow=0.4, rise=0.02, kill_fn=kill)
    foam = Emitter(34, 32, 'puff', FOAM, FOAM_D, 0.6, U(0.9, 1.3), births_bursts([0.05, 0.8], 0.1), strip([0, 0], lat, 1.8, u, (-3.0, -0.5), (0.3, 1.0)),
                   vel_dir(onshore, (0.4, 1.0), lat, 0.4, (3.5, 5.5)), drag=1.2, size=(0.3, 0.6), swell=(0.8, 2.0), T=T, rim=0.4)
    door_fr = Frame((-3.4, 3.4), (-4.0, 2.4), (-4.6, 4.2), PPM_DOOR)
    fret_fl = Emitter(22, 33, 'flatpuff', (0.90, 0.93, 0.97), MIST_D, 0.22, U(3.0, 5.0), births_uniform(2.0), in_disc(8.0, (0.05, 0.1)),
                      lambda g, n, p: np.zeros((n, 3)), drift=(0.5 * onshore[0], 0.5 * onshore[1], 0), size=(1.6, 2.6), swell=(0.85, 1.25), T=2.0,
                      rim=0.45, rise=0.3, fade_pow=1.0)
    fret_bb = Emitter(12, 34, 'puff', (0.92, 0.95, 0.99), MIST_D, 0.16, U(2.0, 3.0), births_uniform(2.0), in_disc(8.0, (0.2, 0.7)),
                      lambda g, n, p: np.zeros((n, 3)), drift=(0.5 * onshore[0], 0.5 * onshore[1], 0.05), size=(0.6, 1.0), swell=(0.8, 1.4), T=2.0,
                      rim=0.4, rise=0.3, fade_pow=1.0)
    pool_fr = Frame((-10.0, 10.0), (-10.0, 10.0), (0.0, 1.6), PPM_POOL)
    sdrops = Emitter(34, 35, 'drop', FOAM, WATER_D, 0.95, U(0.5, 0.66), U(0.0, 0.05), in_disc(0.5, (0.0, 0.3)), vel_radial((0.3, 1.0), (2.5, 4.5)),
                     grav=(0, 0, -9.8), ground_kill=True, size=(0.025, 0.05), swell=(1, 1), rim=0.45, streak=0.05, fade_pow=0.3, rise=0.01)
    sfoam = Emitter(12, 36, 'puff', FOAM, FOAM_D, 0.8, U(0.45, 0.66), U(0.0, 0.05), in_disc(0.5, (0.0, 0.9)), vel_radial((0.3, 0.8), (0.8, 2.0)),
                    drag=3.0, size=(0.32, 0.55), swell=(0.9, 1.6), rim=0.35, rise=0.01)
    arr_fr = Frame((-1.7, 1.7), (-1.7, 1.7), (0.0, 2.8), PPM_FINE)
    segs = door_and_ground_and_arrival(src_dir, pid, ([foam, drops], door_fr, fps, 1.5, T, lip, None),
                                       ([fret_bb], pool_fr, 6, 2.0, 6.0, lambda t: [(-1e12, flow_layer(pool_fr, t, 2.0, 0.7 * onshore, 303, 8.6, thr=0.0, gain=0.8, peak=0.32,
                                                                                    col=(0.91, 0.94, 0.98), dark=MIST_D, rim=0.45))]), ([sfoam, sdrops], arr_fr, 24, 0.6667),
                                       "the lip is SOUTH of the patch (toward the camera): the spray y-sorts IN FRONT of bodies; it rises from the cliff face below the lip (z < 0) and dies where it falls onto the land")
    return segs, {"deliverer_world_m": [round(float(lip[0]), 4), round(float(lip[1]), 4)],
                  "deliverer_feature": "the cliff lip on the origin -> p03 ray, 9.2 m out from the anchor (the stair's top landing edge)"}

# ---- p04: the hall's great door (E). Smoke and embers roll out across the yard.
def src_p04(src_dir):
    pid = 'p04'; f = bearing_vec(FEAT['hall_great_door']['faces_deg']); lat = v2([-f[1], f[0]])
    door_pt = fp_centre('hall_great_door') + 0.6 * f
    fps, T = 8, 1.5
    smoke = Emitter(90, 41, 'puff', SMOKE_DK, SMOKE_D, 0.7, U(1.2, 1.5), births_uniform(T), strip([0, 0], lat, 1.3, f, (0.4, 3.4), (-0.3, 0.1)),
                    vel_dir(f, (3.0, 5.0), lat, 0.6, (0.0, 0.4)), drag=0.6, drift=(1.1 * f[0], 1.1 * f[1], 0.35), size=(0.4, 0.7),
                    swell=(0.8, 2.8), T=T, rim=0.35, col2=SMOKE_LT)
    embers = Emitter(44, 42, 'spark', EMBER, EMBER_D, 1.0, U(0.9, 1.5), births_uniform(T), strip([0, 0], lat, 1.3, f, (0.4, 3.0), (-0.2, 0.1)),
                     vel_dir(f, (2.0, 4.0), lat, 0.8, (0.5, 1.8)), drag=0.6, drift=(0.8 * f[0], 0.8 * f[1], 0.6), size=(0.03, 0.045),
                     swell=(1, 0.7), T=T, rim=0.2, flicker=0.5, fade_pow=1.2, rise=0.05)
    door_fr = Frame((-11.0, 1.0), (-4.5, 4.5), (0.0, 6.5), PPM_DOOR)
    bank_fl = Emitter(18, 43, 'flatpuff', (0.55, 0.54, 0.59), SMOKE_D, 0.28, U(3.0, 4.5), births_uniform(2.0), in_disc(8.0, (0.05, 0.1)),
                      lambda g, n, p: np.zeros((n, 3)), drift=(0.6 * f[0], 0.6 * f[1], 0), size=(1.4, 2.4), swell=(0.85, 1.3), T=2.0,
                      rim=0.45, rise=0.3, fade_pow=1.0)
    bank_bb = Emitter(12, 44, 'puff', (0.62, 0.61, 0.66), SMOKE_D, 0.22, U(2.0, 3.0), births_uniform(2.0), in_disc(8.0, (0.3, 0.9)),
                      lambda g, n, p: np.zeros((n, 3)), drift=(0.6 * f[0], 0.6 * f[1], 0.08), size=(0.6, 1.0), swell=(0.8, 1.5), T=2.0,
                      rim=0.4, rise=0.3, fade_pow=1.0)
    bank_em = Emitter(12, 45, 'spark', EMBER, EMBER_D, 0.9, U(1.0, 2.0), births_uniform(2.0), in_disc(7.5, (0.1, 0.6)),
                      lambda g, n, p: np.zeros((n, 3)), drift=(0.5 * f[0], 0.5 * f[1], 0.3), size=(0.03, 0.045), swell=(1, 0.7), T=2.0,
                      rim=0.2, flicker=0.6, fade_pow=1.2, rise=0.1)
    pool_fr = Frame((-10.0, 10.0), (-10.0, 10.0), (0.0, 1.6), PPM_POOL)
    apuff = Emitter(14, 46, 'puff', SMOKE_DK, SMOKE_D, 0.8, U(0.45, 0.66), U(0.0, 0.05), in_disc(0.5, (0.0, 1.0)), vel_radial((0.4, 1.0), (0.8, 2.0)),
                    drag=3.0, size=(0.35, 0.6), swell=(0.9, 1.7), rim=0.35, rise=0.01, col2=SMOKE_LT)
    aemb = Emitter(16, 47, 'spark', EMBER, EMBER_D, 1.0, U(0.45, 0.66), U(0.0, 0.08), in_disc(0.4, (0.1, 0.8)), vel_radial((0.5, 1.4), (1.5, 3.0)),
                   drag=0.8, grav=(0, 0, -2.0), size=(0.02, 0.035), swell=(1, 0.7), rim=0.2, flicker=0.4, fade_pow=1.0, rise=0.02)
    arr_fr = Frame((-1.7, 1.7), (-1.7, 1.7), (0.0, 2.8), PPM_FINE)
    segs = door_and_ground_and_arrival(src_dir, pid, ([smoke, embers], door_fr, fps, T, T, door_pt, None),
                                       ([bank_bb, bank_em], pool_fr, 6, 2.0, 6.0, lambda t: [(-1e12, flow_layer(pool_fr, t, 2.0, 0.8 * f, 404, 8.6, thr=-0.2, gain=0.8, peak=0.42,
                                                                                    col=(0.56, 0.55, 0.60), dark=SMOKE_D, rim=0.5))]), ([apuff, aemb], arr_fr, 24, 0.6667),
                                       "the great door is EAST of the patch; the smoke rolls WEST out of it toward the bodies")
    return segs, {"deliverer_world_m": [round(float(door_pt[0]), 4), round(float(door_pt[1]), 4)],
                  "deliverer_feature": "hall_great_door (centre + 0.6 m along its facing, 270 deg)"}

# ---- p06: the fallen gable (SE). Ash heaps heave, with a shower of sparks.
def src_p06(src_dir):
    pid = 'p06'; anc = anchor(pid); d_in = unit(-anc); lat = v2([-d_in[1], d_in[0]])
    foot = fp_nearest_edge('fallen_gable', anc)
    fps, T = 10, 1.2
    sparks = Emitter(90, 61, 'spark', SPARK, SPARK_D, 1.0, U(0.7, 1.15), births_bursts([0.0, 0.45, 0.85], 0.05), strip([0, 0], lat, 1.5, d_in, (0.2, 0.8), (-0.4, 0.4)),
                     vel_dir(d_in, (0.5, 2.2), lat, 1.0, (3.5, 6.5)), drag=0.4, grav=(0, 0, -9.8), size=(0.035, 0.055), swell=(1, 0.8), T=T,
                     rim=0.2, flicker=0.4, streak=0.05, ground_kill=True, fade_pow=0.8, rise=0.02)
    plume = Emitter(40, 62, 'puff', ASH, ASH_D, 0.62, U(0.9, 1.2), births_uniform(T), strip([0, 0], lat, 1.4, d_in, (0.2, 1.0), (-0.4, 0.4)),
                    vel_dir(d_in, (0.3, 0.8), lat, 0.3, (0.5, 1.2)), drag=0.8, drift=(0, 0, 0.3), size=(0.35, 0.6), swell=(0.8, 2.2), T=T,
                    rim=0.35, col2=ASH2)
    door_fr = Frame((-4.5, 4.5), (-4.5, 3.5), (0.0, 6.0), PPM_DOOR)
    # the ash field: heaps that heave (swell and settle, each on its own phase -- one whole cycle per loop), dust lifting at each peak
    g = rng(63); K = 15; hp = in_disc(7.4)(g, K)[:, :2]; hr = g.uniform(0.55, 1.0, K); ph = g.random(K); Tg = 2.0
    def heaves(t):
        out = []
        for i in range(K):
            s = max(0.0, math.sin(2 * math.pi * (t / Tg + ph[i]))) ** 2
            def mk(i=i, s=s):
                def draw(cv):
                    cx, cy = cv._fr.proj(hp[i, 0], hp[i, 1], 0.0)
                    r = hr[i] * (1.0 + 0.22 * s) * cv._fr.ppm
                    cv.splat(flat_sprite(r, i % 6, 0.55, hard=True), cx, cy, ASH2, ASH_D, 0.72)
                    cx2, cy2 = cv._fr.proj(hp[i, 0], hp[i, 1], 0.12 + 0.25 * s)
                    cv.splat(flat_sprite(r * 0.55, (i + 3) % 6, 0.2, hard=False), cx2, cy2, (0.74, 0.73, 0.76), ASH_D, 0.45 + 0.45 * s)
                return draw
            out.append((hp[i, 1] * SA * 1000 - 1e6, mk()))
        return out
    # dust and sparks born at each heap's peak (periodic in Tg)
    peak_b = ((0.25 - ph) % 1.0) * Tg
    def heap_pos(g, n):
        idx = np.arange(n) % K; p = np.c_[hp[idx], np.full(n, 0.2)]; p[:, :2] += g.normal(0, 0.2, (n, 2)); return p
    def heap_birth(g, n): idx = np.arange(n) % K; return peak_b[idx] + g.normal(0, 0.05, n)
    dust = Emitter(K * 2, 64, 'puff', ASH2, ASH_D, 0.42, U(0.8, 1.2), heap_birth, heap_pos, vel_radial((0.1, 0.4), (0.4, 0.9)),
                   drag=1.5, size=(0.3, 0.5), swell=(0.8, 1.8), T=Tg, rim=0.35)
    hsp = Emitter(K * 2, 65, 'spark', SPARK, SPARK_D, 1.0, U(0.4, 0.7), heap_birth, heap_pos, vel_radial((0.2, 0.8), (1.5, 2.6)),
                  grav=(0, 0, -9.8), ground_kill=True, size=(0.035, 0.05), swell=(1, 0.8), T=Tg, rim=0.2, flicker=0.4, fade_pow=0.8, rise=0.02)
    pool_fr = Frame((-9.0, 9.0), (-9.0, 9.0), (0.0, 1.8), PPM_POOL)
    def ex(t): return heaves(t)
    aclod = Emitter(22, 66, 'clod', ASH, ASH_D, 1.0, 0.66, U(0.0, 0.05), ring(0.2, 0.55, (0.05, 0.3)), vel_radial((0.5, 1.4), (1.8, 3.2)),
                    grav=(0, 0, -9.8), ground_kill=True, size=(0.05, 0.1), swell=(1, 1), rim=0.5, fade_pow=0.3, rise=0.01, col2=ASH2)
    adust = Emitter(14, 67, 'puff', ASH2, ASH_D, 0.85, U(0.45, 0.66), U(0.0, 0.05), in_disc(0.5, (0.0, 0.9)), vel_radial((0.4, 1.0), (0.9, 2.0)),
                    drag=3.0, size=(0.35, 0.6), swell=(0.9, 1.6), rim=0.35, rise=0.01, col2=ASH)
    asp = Emitter(24, 68, 'spark', SPARK, SPARK_D, 1.0, U(0.4, 0.66), U(0.0, 0.1), in_disc(0.4, (0.1, 0.5)), vel_radial((0.5, 1.6), (2.0, 4.0)),
                  grav=(0, 0, -9.8), ground_kill=True, size=(0.03, 0.05), swell=(1, 0.8), rim=0.2, flicker=0.4, streak=0.04, fade_pow=0.8, rise=0.02)
    arr_fr = Frame((-1.7, 1.7), (-1.7, 1.7), (0.0, 2.8), PPM_FINE)
    segs = door_and_ground_and_arrival(src_dir, pid, ([plume, sparks], door_fr, fps, T, T, foot, None),
                                       ([dust, hsp], pool_fr, 6, Tg, 4.0, ex), ([adust, aclod, asp], arr_fr, 24, 0.6667),
                                       "the gable's rubble foot is SOUTH-EAST of the patch")
    return segs, {"deliverer_world_m": [round(float(foot[0]), 4), round(float(foot[1]), 4)],
                  "deliverer_feature": "fallen_gable (the point of its footprint nearest the anchor = the rubble foot)"}

# ---- p05: the frozen mere -- THE AMBUSH. Warning cracks spider across the ice for the 4.0 s hold, then shards + water burst.
AMBUSH_HOLD_S = 4.0
def src_p05(src_dir):
    pid = 'p05'; g = rng(505); seeds = []
    # three slow hairlines near the middle first, then the rim joins, then everything at once: tension builds
    for i in range(3): p = in_disc(2.5)(g, 1)[0]; seeds.append((p[0], p[1], g.uniform(0, 2 * math.pi), g.uniform(0.0, 0.35)))
    segs_c = crack_network(g, seeds, 5.5, 2.2, branch_p=0.25, step=0.15, jitter=0.35, max_gen=3, clip_r=8.3)
    s2 = []
    for i in range(5):
        th = g.uniform(0, 2 * math.pi); s2.append((7.9 * math.cos(th), 7.9 * math.sin(th), th + math.pi + g.normal(0, 0.4), g.uniform(1.1, 2.0)))
    segs_c += crack_network(g, s2, 8.0, 4.0, branch_p=0.3, step=0.18, jitter=0.3, max_gen=3, clip_r=8.3)
    s3 = [(*in_disc(7.5)(g, 1)[0][:2], g.uniform(0, 2 * math.pi), g.uniform(2.3, 3.1)) for _ in range(8)]
    segs_c += crack_network(g, s3, 4.5, 5.5, branch_p=0.35, step=0.18, jitter=0.35, max_gen=3, clip_r=8.3)
    s4 = [(*in_disc(8.0)(g, 1)[0][:2], g.uniform(0, 2 * math.pi), g.uniform(3.3, 3.85)) for _ in range(30)]
    segs_c += [s for s in crack_network(g, s4, 1.6, 9.0, branch_p=0.3, step=0.14, jitter=0.45, max_gen=2, clip_r=8.3)]
    segs_c = [(a, b, c, d, min(t, AMBUSH_HOLD_S - 0.02), gen) for a, b, c, d, t, gen in segs_c]
    fr = Frame((-8.6, 8.6), (-8.6, 8.6), (0.0, 0.0), PPM_FINE)
    segs = []
    rec, C, R = reveal_segment(src_dir, pid, 'p05_hold_cracks', segs_c, AMBUSH_HOLD_S, ((56, 92, 118, 110), 7, 0.4), fr,
        {"start": "EV_AMBUSH_HOLD_START(p05) = the p05 ProxyAmbush release (am1: bodies absent 0 -> 4.0 s, P05_FIRST_ARRIVAL_S): progress = (t - t0) / 4.0",
         "hold": "progress held at 1 from t0 + 4.0 (the cracks are fully open as the bodies burst)",
         "end": "fade 1 -> 0 over 2.0 s from the LAST p05 body's EV_AM5_TIMEOUT; then free"},
        extra_kw={"build_s_fixed": "EXACTLY 4.0 s (am1 P05_FIRST_ARRIVAL_S) -- not stretchable",
                  "build_curve": "slow hairlines from the middle (0-1 s), the rim joins (1.1-2 s), spreading (2.3-3.1 s), a flurry of short cracks everywhere (3.3-3.9 s)"})
    segs.append(rec)
    # the burst (per body, at its arrival = t0 + 4.0)
    shards = Emitter(14, 51, 'shard', ICE, ICE_D, 1.0, U(0.6, 0.75), U(0.0, 0.04), ring(0.3, 0.7, (0.02, 0.15)), vel_radial((0.8, 1.8), (2.5, 4.5)),
                     grav=(0, 0, -9.8), ground_kill=True, size=(0.1, 0.2), swell=(1, 1), rim=0.9, fade_pow=0.3, rise=0.01)
    water = Emitter(44, 52, 'drop', WATER, WATER_D, 0.95, U(0.5, 0.75), U(0.0, 0.08), in_disc(0.5, (0.0, 0.4)), vel_radial((0.5, 1.4), (2.0, 4.0)),
                    grav=(0, 0, -9.8), ground_kill=True, size=(0.025, 0.05), swell=(1, 1), rim=0.45, streak=0.05, fade_pow=0.3, rise=0.01)
    splash = Emitter(14, 53, 'puff', FOAM, FOAM_D, 0.85, U(0.45, 0.7), U(0.0, 0.05), in_disc(0.6, (0.0, 1.0)), vel_radial((0.4, 1.0), (1.0, 2.2)),
                     drag=3.0, size=(0.35, 0.6), swell=(0.9, 1.7), rim=0.35, rise=0.01)
    mist = Emitter(6, 54, 'puff', MIST, MIST_D, 0.45, 0.75, U(0.05, 0.2), ring(0.4, 0.9, (0.05, 0.3)), vel_radial((0.4, 0.8), (0.1, 0.3)),
                   drag=1.5, size=(0.45, 0.65), swell=(0.9, 1.8), rim=0.4, rise=0.05)
    bfr = Frame((-2.1, 2.1), (-2.1, 2.1), (0.0, 3.4), PPM_FINE)
    frames = [render([mist, splash, shards, water], bfr, (j + ARR_T0) / 24).rgba8() for j in range(18)]
    info, _ = write_atlas(src_dir, 'p05_burst', frames, bfr)
    segs.append(seg_record('p05_burst', info, bfr, 24, 18, {"oneshot": [0, 17]}, "one-shot",
                           {"mode": "ysort", "ysort_ground_m": "the body's own landing point + 0.05 m south (drawn just in front of its own body)"},
                           ["body.x", "body.y", 0.0],
                           {"start": "EV_AMBUSH_ARRIVAL(body, x, y) = the body's p05 spawn at t0 + 4.0 s: frame 0 on that tick (dense: it covers the pop-in; the health bar shows from the same frame per the Sim Session's footage read)",
                            "end": "free on the last frame (0.75 s; fits inside the shortest am3 window, D_long 0.867 s)",
                            "scale": "x max(1, record_radius_m / 0.8) for wide bodies"}))
    # the hole under each body: opens with the burst, slush laps while the body stands (am3 window D), fades after
    g2 = rng(55); NS = 11; sa = np.sort(g2.uniform(0, 2 * math.pi, NS)); sr = g2.uniform(0.8, 1.05, NS); ss = g2.uniform(0.09, 0.16, NS)
    NF = 16; fa = g2.uniform(0, 2 * math.pi, NF); fph = g2.random(NF)
    INTRO, LOOP = 0.3, 1.2
    def hole(t):
        def draw(cv):
            fr_ = cv._fr; o = min(1.0, t / INTRO)
            cx, cy = fr_.proj(0, 0, 0)
            cv.splat(flat_sprite(0.95 * fr_.ppm * (0.4 + 0.6 * o), 2, 0.5, hard=False), cx, cy, (0.42, 0.55, 0.66), ICE_D, 0.55 * o)
            cv.splat(flat_sprite(0.72 * fr_.ppm * o, 1, 0.55, hard=True), cx, cy, (0.17, 0.26, 0.34), (0.08, 0.13, 0.19), 0.92)
            for i in range(NS):
                if t < 0.06 + 0.02 * i % 0.2: continue
                px, py = fr_.proj(math.cos(sa[i]) * sr[i] * (0.7 + 0.3 * o), math.sin(sa[i]) * sr[i] * (0.7 + 0.3 * o), 0.0)
                cv.splat(shard_sprite(ss[i] * fr_.ppm, i % 4, i % 16, flat=True), px, py, ICE, ICE_D, 1.0)
            if t >= INTRO:
                tl = (t - INTRO) / LOOP
                for i in range(NF):
                    rr = 0.62 + 0.07 * math.sin(2 * math.pi * (tl + fph[i]))
                    a = fa[i] + 0.25 * math.sin(2 * math.pi * (tl + fph[i]))
                    px, py = fr_.proj(math.cos(a) * rr, math.sin(a) * rr, 0.0)
                    cv.splat(flat_sprite(0.06 * fr_.ppm, i % 6, 0.4, hard=True), px, py, SNOW, SNOW_D, 0.8 * (0.6 + 0.4 * math.sin(2 * math.pi * (tl + fph[i] * 2)) ** 2))
        return [(0.0, draw)]
    hfr = Frame((-1.35, 1.35), (-1.35, 1.35), (0.0, 0.0), PPM_FINE)
    frames = []
    for j in range(int(round((INTRO + LOOP) * 10))):
        cv = Canvas(hfr.W, hfr.H); cv._fr = hfr
        for _, fnc in hole(j / 10): fnc(cv)
        frames.append(cv.rgba8())
    info, _ = write_atlas(src_dir, 'p05_hole', frames, hfr)
    ni = int(round(INTRO * 10))
    segs.append(seg_record('p05_hole', info, hfr, 10, len(frames), {"intro": [0, ni - 1], "loop": [ni, len(frames) - 1]}, "intro once, then loop",
                           LAYER_GROUND, ["body.x", "body.y", 0.0],
                           {"start": "EV_AMBUSH_ARRIVAL(body, x, y): intro from frame 0 (under the body; the burst plays over it)",
                            "hold": "loop for the record's am3 window D: until EV_AM5_TIMEOUT(body) = arrival + D_long_s(record) (STRETCHABLE: D is per RECORD -- engine pack v3.11 model/waves.json '⚑ v3p8_rows'.am3_emergence_window, key monster.p05_emergence_window_s, value.D_long_s; 31 rows V38-AM3-*; 0.867 .. 4.9 s; ticks ceil(t / period - 1e-9))",
                            "end": "at EV_AM5_TIMEOUT(body) (the body starts moving) fade modulate.a 1 -> 0 over 1.0 s; then free",
                            "parameter": "D = value.D_long_s of the body's record (NOT D_short_s)"}))
    return segs, {"deliverer_world_m": None, "deliverer_feature": "none: the mere itself delivers (the ambush)",
                  "ambush": {"hold_s": AMBUSH_HOLD_S, "hold_source": "kc2_runtime/sim/kc2rt_fight.gd am1 P05_FIRST_ARRIVAL_S (via the conductor relay)",
                             "am3_D_source": "engine pack kc2-model-pack-v3-E-s09-cp150-mech-v3p11 model/waves.json '⚑ v3p8_rows'.am3_emergence_window value.D_long_s",
                             "am3_D_long_range_s": [0.867, 4.9],
                             "only_p05_emerges": "p01-p04 and p06 release ring bodies with NO emergence; their arrivals are a cover-the-pop one-shot"}}

def main():
    out_root = HERE; want = sys.argv[1:] or ['p01', 'p02', 'p03', 'p04', 'p05', 'p06']
    summary = {}
    for pid in want:
        m = build(pid, out_root)
        summary[pid] = {"segments": [s['id'] for s in m['segments']], "vram_MiB": round(m['vram_bytes_total'] / 2 ** 20, 2),
                        "png_KiB": round(sum(s['png_bytes'] for s in m['segments']) / 1024, 1)}
        print(pid, json.dumps(summary[pid]), flush=True)
    write_index(out_root)

EVENTS = {
  "EV_POINT_RELEASE(point)": "the oracle's wave release at a ring point (p01, p02, p03, p04, p06). Starts the point's door intro and ground loop/reveal.",
  "EV_BODY_SPAWN(point, body, x, y)": "a ring body appears at its rolled landing point (theta = 2 pi u1, rho = 8 u2 about the anchor; NO emergence on ring points). Starts that body's arrival one-shot.",
  "EV_POINT_RELEASE_DONE(point)": "the point's release has finished (its last EV_BODY_SPAWN under the runtime's two-segment release warp). If the runtime has no such event, derive it as the LAST EV_BODY_SPAWN of that point's release (the count is known from the wave row). Door + ground hold to this + 0.8 s, then fade.",
  "EV_AMBUSH_HOLD_START(p05)": "the p05 ProxyAmbush release = am1 start (bodies absent 0 -> 4.0 s, P05_FIRST_ARRIVAL_S). Starts the hold-crack reveal: progress = (t - t0) / 4.0.",
  "EV_AMBUSH_ARRIVAL(body, x, y)": "a p05 body's spawn at t0 + 4.0 s (it stands, hittable, for its record's am3 window). Starts p05_burst (over) and p05_hole (under) at the body.",
  "EV_AM5_TIMEOUT(body)": "arrival + D_long_s(record) (am3 window end; specials arm). Ends that body's p05_hole (1.0 s fade). The LAST p05 body's timeout starts the hold-crack field's 2.0 s fade."
}

def write_index(out_root):
    idx = {"what": "barrow_v2 per-source SPAWN-DELIVERY VFX (Run C-9 Phase 2, lane DV, drax; R-C9-145 spawn plan, R-C9-147 priority)",
           "binding": "KC2: every segment keys off a runtime ORACLE EVENT below -- never a free-running timer. Fixed tails ('+ 0.8 s', 'fade over 1.0 s') are measured FROM those events.",
           "events": EVENTS, "camera": CAMERA,
           "draw_layers": {"ground": LAYER_GROUND, "ysort": "y-sorted with the actors by the named ground point (the projection law's draw order)"},
           "stretch": "door + ground segments are intro-once-then-loop (or loop-only) with whole loops repeated while the event window lasts; the p05 hole is parameterised by D = value.D_long_s of the body's record; the p05 crack build is fixed at exactly 4.0 s",
           "modulate": "fades are the runtime's CanvasItem modulate.a (or the reveal shader's 'fade' uniform), never baked frames",
           "import": "colour atlases: Godot 2D import, filter linear, no mipmaps (VRAM-compressed is acceptable for the soft door/ground atlases); *_reveal.png: LOSSLESS, no sRGB conversion, no mipmaps (it is data)",
           "shader": "shaders/spawn_crack_reveal.gdshader", "sources": {}}
    total = 0
    for pid, d in SRC_DIRS.items():
        p = os.path.join(out_root, d, f'vfx_{pid}.json')
        if not os.path.exists(p): continue
        m = json.load(open(p)); total += m['vram_bytes_total']
        idx['sources'][pid] = {"manifest": f"{d}/vfx_{pid}.json", "deliverer": m['deliverer'],
                               "segments": {s['id']: {"layer": s['draw_layer'] if isinstance(s['draw_layer'], str) else s['draw_layer']['mode'],
                                                      "start_event": s['events']['start'].split(':')[0]} for s in m['segments']},
                               "vram_MiB": round(m['vram_bytes_total'] / 2 ** 20, 2)}
    idx['vram_MiB_total_rgba8'] = round(total / 2 ** 20, 2)
    with open(os.path.join(out_root, 'spawn_vfx_index.json'), 'w') as f:
        json.dump(idx, f, indent=2, ensure_ascii=False); f.write('\n')

if __name__ == '__main__':
    main()
