# EN-E3 VFX: BAKED FLIPBOOKS in the painted register, generated procedurally (no paid calls), sized from the roster's ability rows.
#   python3 scripts/n20_vfx.py <creature> <outdir>
# Discipline: every effect is a single RGBA atlas (straight alpha, sRGB) + a JSON row: frames, grid, fps, the cell's size IN METRES,
# the pivot (where the socket / ground point sits in the cell), the plane it is drawn on (ground = top-down decal, billboard =
# camera-facing), the roster ability it serves, and the release/contact clip time it is triggered on. Nothing is baked into the
# creature's cells (sprite-cell contract § 2.2: no VFX in the body).
# THE HAND: shapes are laid as transparent washes that POOL at their edges (edge-darkened alpha), GRANULATE (paper noise), and are
# outlined by a wavering dark sepia ink line taken from the wash's own edge -- the register card's line + wash, not glow. No
# additive light, no bloom.
import json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

RNG = np.random.default_rng(132)
INK = np.array([52, 36, 26], float)

def paper(h, w, scale=3.0):
    n = ndimage.gaussian_filter(RNG.standard_normal((h, w)), scale) ; n2 = ndimage.gaussian_filter(RNG.standard_normal((h, w)), 0.8)
    n = (n - n.mean()) / (n.std() + 1e-9); n2 = (n2 - n2.mean()) / (n2.std() + 1e-9)
    return 0.7 * n + 0.3 * n2

def wash(mask, col, dark, h, w, pool=0.55, gran=0.10, ink_w=1.4, ink_a=0.9):
    """mask: float 0..1 coverage. Returns RGBA float (0..255, alpha 0..1)."""
    m = ndimage.gaussian_filter(mask, 1.2)
    edge = np.clip(m - ndimage.gaussian_filter(m, 4.0), 0, 1) * 2.2            # pooling: wash collects at its edge
    g = paper(h, w)
    a = np.clip(m * (0.55 + 0.35 * np.clip(edge, 0, 1)) + gran * g * m, 0, 1)
    t = np.clip(edge * pool + 0.15 * g, 0, 1)[..., None]
    rgb = np.array(col, float) * (1 - t) + np.array(dark, float) * t
    # ink line on the wash boundary, wavering in weight
    hard = m > 0.35
    ring = hard ^ ndimage.binary_erosion(hard, iterations=max(1, int(ink_w)))
    wob = ndimage.gaussian_filter(RNG.random((h, w)), 2.0) > 0.42
    ring = ring & wob
    ri = ndimage.gaussian_filter(ring.astype(float), 0.6)
    rgb = rgb * (1 - ri[..., None] * ink_a) + INK * ri[..., None] * ink_a
    a = np.clip(np.maximum(a, ri * ink_a), 0, 1)
    return rgb, a

def disc(h, w, cx, cy, r, sq=1.0):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - cx) / max(r, 1e-3)) ** 2 + ((yy - cy) / max(r * sq, 1e-3)) ** 2)
    return np.clip(1.6 - d * 1.6, 0, 1) ** 0.7 * (d < 1.0)

def atlas(frames, cols):
    h, w = frames[0][1].shape; rows = (len(frames) + cols - 1) // cols
    A = np.zeros((rows * h, cols * w, 4), np.uint8)
    for i, (rgb, al) in enumerate(frames):
        r, c = divmod(i, cols)
        A[r * h:(r + 1) * h, c * w:(c + 1) * w, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
        A[r * h:(r + 1) * h, c * w:(c + 1) * w, 3] = np.clip(al * 255, 0, 255).astype(np.uint8)
        A[r * h:(r + 1) * h, c * w:(c + 1) * w, 3][[0, -1], :] = 0; A[r * h:(r + 1) * h, c * w:(c + 1) * w, 3][:, [0, -1]] = 0
    return A

# ---------------- effect generators ----------------
def spray(n, W, H, length_m, width_m, col, dark, droplets=70, chunk=1.0, fade_from=0.55):
    """A cone/wave spray, top-down, apex at the cell's left middle, travelling +x. length/width in metres; cell W x H px."""
    ppm = (W - 16) / (length_m * 1.12); out = []
    births = RNG.random(droplets) * 0.6; ang = (RNG.random(droplets) - 0.5); spd = 0.75 + 0.5 * RNG.random(droplets)
    size = (0.05 + 0.08 * RNG.random(droplets)) * chunk
    for i in range(n):
        t = i / (n - 1); mask = np.zeros((H, W))
        for b, an, sp, sz in zip(births, ang, spd, size):
            age = (t - b) / 0.5
            if age <= 0 or age > 1.25: continue
            dist = min(age * sp, 1.0) * length_m
            half = 0.12 + (width_m / 2 - 0.12) * min(dist / length_m * 1.4, 1)
            cx = 8 + dist * ppm; cy = H / 2 + an * 2 * half * ppm
            r = (sz + 0.035 * dist) * ppm
            mask = np.maximum(mask, disc(H, W, cx, cy, r, 0.8) * (1.0 if age < 1 else (1.25 - age) * 4))
            # streak behind the droplet
            for k in range(1, 4):
                mask = np.maximum(mask, 0.6 * disc(H, W, cx - k * r * 0.7, cy - an * k * 0.05 * ppm, r * (1 - 0.2 * k), 0.7) * (age < 1))
        fade = 1.0 if t < fade_from else max(0.0, 1 - (t - fade_from) / (1 - fade_from))
        rgb, al = wash(np.clip(mask, 0, 1), col, dark, H, W)
        out.append((rgb, al * fade))
    return out, ppm

def impact(n, S, radius_m, col, dark, spikes=7):
    """A strike mark: a splash crescent + radiating ink snap lines, billboard, grows then fades."""
    ppm = (S / 2 - 8) / radius_m; out = []
    ang0 = RNG.random(spikes) * 2 * math.pi
    for i in range(n):
        t = i / (n - 1); grow = min(1.0, t / 0.35); r = radius_m * (0.35 + 0.65 * grow) * ppm
        mask = disc(S, S, S / 2, S / 2, r * 0.55, 0.8) * (1 - t) ** 0.6
        for a in ang0:
            for k in range(6):
                d = r * (0.4 + 0.12 * k); rr = r * (0.16 - 0.022 * k)
                mask = np.maximum(mask, disc(S, S, S / 2 + math.cos(a) * d, S / 2 + math.sin(a) * d * 0.8, rr, 1.0) * max(0, 1 - t * 1.2))
        hole = disc(S, S, S / 2, S / 2, r * 0.35 * grow, 0.8) * (t > 0.3)
        rgb, al = wash(np.clip(mask - 0.8 * hole, 0, 1), col, dark, S, S)
        out.append((rgb, al * (1 if t < 0.6 else (1 - t) / 0.4)))
    return out, ppm

def ring(n, S, radius_m, col, dark, thick=0.18):
    """A ground ring/shockwave (top-down decal), expanding to radius_m."""
    ppm = (S / 2 - 8) / radius_m; out = []
    for i in range(n):
        t = i / (n - 1); r = radius_m * (0.15 + 0.85 * (1 - (1 - t) ** 2)) * ppm
        yy, xx = np.mgrid[0:S, 0:S]; d = np.hypot(xx - S / 2, (yy - S / 2))
        jag = 1 + 0.08 * np.sin(np.arctan2(yy - S / 2, xx - S / 2) * 9 + i)
        m = np.clip(1 - np.abs(d - r * jag) / (thick * ppm * (1 - 0.6 * t)), 0, 1)
        rgb, al = wash(m, col, dark, S, S)
        out.append((rgb, al * (1 - t) ** 0.8))
    return out, ppm

def orb(n, S, radius_m, col, dark):
    """A projectile body (billboard), a lumpy wash ball that wobbles; loops."""
    ppm = (S / 2 - 6) / radius_m; out = []
    for i in range(n):
        ph = 2 * math.pi * i / n; m = np.zeros((S, S))
        for k in range(5):
            a = ph + k * 1.26; m = np.maximum(m, disc(S, S, S / 2 + math.cos(a) * 0.25 * radius_m * ppm, S / 2 + math.sin(a) * 0.25 * radius_m * ppm, 0.6 * radius_m * ppm, 1))
        rgb, al = wash(m, col, dark, S, S); out.append((rgb, al))
    return out, ppm

def puff(n, S, radius_m, col, dark, blobs=9, rise=0.4):
    """Dust/earth puff (billboard), for a sprout or emergence: blobs swell and rise, then fade."""
    ppm = (S / 2 - 6) / radius_m; out = []
    ang = RNG.random(blobs) * 2 * math.pi; rad = 0.3 + 0.5 * RNG.random(blobs)
    for i in range(n):
        t = i / (n - 1); m = np.zeros((S, S))
        for a, rr in zip(ang, rad):
            cx = S / 2 + math.cos(a) * rr * radius_m * ppm * (0.4 + 0.6 * t)
            cy = S * 0.72 - (rise * t + 0.1 * math.sin(a) * rr) * radius_m * ppm
            m = np.maximum(m, disc(S, S, cx, cy, (0.18 + 0.25 * t) * radius_m * ppm, 0.75))
        rgb, al = wash(m, col, dark, S, S); out.append((rgb, al * (1 - t) ** 1.2))
    return out, ppm

PRESETS = {
 'gazer': [
  dict(id='gazer_glare_cone', fn='spray', n=16, fps=24, cols=4, W=704, H=256, length_m=6.0, width_m=2.0, col=(198, 214, 196), dark=(110, 128, 112),
       plane='ground', pivot='left-middle (the eyes, projected to the ground)', ability='basilisk_petrifyingglare (aoe wave 6 m long, 1.4-2 m wide, slow)',
       trigger='cast_glare release f16; loop frames 4-11 while the stare holds (the clip holds f16-f34)'),
  dict(id='gazer_eye_flare', fn='impact', n=8, fps=24, cols=4, S=128, radius_m=0.16, col=(214, 246, 228), dark=(120, 170, 150),
       plane='billboard', pivot='centre = each eye socket (eye_L / eye_R)', ability='basilisk_petrifyingglare: the eyes FLARE', trigger='cast_glare f12 to f34, then fade'),
  dict(id='gazer_acid_breath', fn='spray', n=16, fps=24, cols=4, W=576, H=320, length_m=4.0, width_m=2.0, col=(176, 172, 84), dark=(104, 110, 44),
       plane='ground', pivot='left-middle (the mouth, projected to the ground)', ability='basilisk_acidbarf (aoe wave 4 m x 2 m, poison)', trigger='cast_breath release f16'),
  dict(id='gazer_spit_orb', fn='orb', n=8, fps=20, cols=4, S=96, radius_m=0.12, col=(160, 176, 70), dark=(90, 106, 34),
       plane='billboard', pivot='centre = the spit in flight (body r 0.1 m)', ability='basilisk_acidspit (projectile 18 m/s)', trigger='cast_spit release f21 at the maw'),
  dict(id='gazer_spit_splash', fn='ring', n=12, fps=24, cols=4, S=256, radius_m=1.5, col=(170, 186, 86), dark=(96, 112, 40),
       plane='ground', pivot='centre = the impact point (area 1.5 m)', ability='basilisk_acidspit impact', trigger='on spit impact'),
  dict(id='gazer_tail_ring', fn='ring', n=12, fps=30, cols=4, S=384, radius_m=3.8, col=(196, 186, 164), dark=(112, 102, 90),
       plane='ground', pivot='centre = the root', ability='basilisk_tailswipe (aoe r 3.8 m)', trigger='attack_tail release f16'),
 ],
 'bloom': [
  dict(id='bloom_bite_impact', fn='impact', n=8, fps=30, cols=4, S=256, radius_m=0.6, col=(150, 46, 40), dark=(86, 24, 26),
       plane='billboard', pivot='centre = the jaw tip at contact', ability='livingplant_bite (melee 0-2.86 m, bleeding 5 s)', trigger='attack_bite contact f13'),
  dict(id='bloom_seed_orb', fn='orb', n=8, fps=20, cols=4, S=160, radius_m=0.35, col=(150, 170, 70), dark=(86, 104, 34),
       plane='billboard', pivot='centre = the seed in flight (a mortar lob from the mouth; the roster body radius is 1 m, the drawn seed 0.35 m)',
       ability='livingplant_venomousseed (projectile drop/mortar, 30 m/s, 3.6-23 m)', trigger='cast_spit release f19 at the maw socket'),
  dict(id='bloom_seed_splash', fn='ring', n=12, fps=24, cols=4, S=384, radius_m=2.5, col=(170, 186, 86), dark=(96, 112, 40),
       plane='ground', pivot='centre = the landing point (area 1.5 / 2.5 m; the 5 s poison field is a runtime tint, not baked)', ability='livingplant_venomousseed landing', trigger='on seed landing'),
  dict(id='bloom_sprout_dust', fn='puff', n=12, fps=24, cols=4, S=256, radius_m=1.2, col=(178, 166, 148), dark=(104, 94, 82),
       plane='billboard', pivot='bottom-centre = the plant root (the p05 breach)', ability='p05 emergence (sprout 1.5 s)', trigger='spawn start f0'),
 ],
 'raptor': [
  dict(id='raptor_rake_impact', fn='impact', n=8, fps=30, cols=4, S=256, radius_m=0.6, col=(150, 46, 40), dark=(86, 24, 26),
       plane='billboard', pivot='centre = the left forelimb claw tip at contact', ability='sandlizard / eldritchlizard double swipe (melee 0-2.95 m)', trigger='attack_swipe contact f14'),
  dict(id='raptor_kick_impact', fn='impact', n=8, fps=30, cols=4, S=256, radius_m=0.5, col=(206, 112, 52), dark=(120, 52, 30),
       plane='billboard', pivot='centre = the right sickle claw at contact', ability='sandlizard leg claw / volcanic fire claw (melee 0-3.02 m, bleeding / fire)', trigger='attack_kick contact f22'),
  dict(id='raptor_leap_ring', fn='ring', n=12, fps=30, cols=4, S=384, radius_m=2.8, col=(204, 160, 118), dark=(118, 70, 46),
       plane='ground', pivot='centre = the landing point (root)', ability='sandlizard_leap (aoe r 2.8 m at landing, bleeding)', trigger='attack_leap release f19'),
  dict(id='raptor_leap_dust', fn='puff', n=12, fps=24, cols=4, S=256, radius_m=1.2, col=(186, 170, 150), dark=(110, 98, 86),
       plane='billboard', pivot='bottom-centre = the landing point', ability='sandlizard_leap landing dust', trigger='attack_leap release f19'),
 ],
 'crab': [
  dict(id='crab_frost_breath', fn='spray', n=16, fps=20, cols=4, W=640, H=256, length_m=3.5, width_m=1.0, col=(214, 226, 232), dark=(112, 142, 164),
       plane='ground', pivot='left-middle (the mouth plates, projected to the ground)', ability='ghostcrab_waterbreath (aoe wave 3.5 m long x 1 m wide, cold 6 s)',
       trigger='cast_breath release f14; plays 0.8 s, may loop frames 4-11 while the breath holds (the clip holds its pose f14-f36)'),
  dict(id='crab_slam_ring', fn='ring', n=12, fps=30, cols=4, S=320, radius_m=1.1, col=(196, 186, 164), dark=(112, 102, 90),
       plane='ground', pivot='centre = between the two claw tips at contact', ability='swampcrab_clawslam (melee 0-3.09 m)', trigger='attack_slam contact f12'),
  dict(id='crab_strike_impact', fn='impact', n=8, fps=30, cols=4, S=256, radius_m=0.55, col=(150, 46, 40), dark=(86, 24, 26),
       plane='billboard', pivot='centre = the left claw tip at contact', ability='swampcrab_waterspoutstrike / shellspin (melee 0-3.09 m)', trigger='attack_strike contact f12'),
  dict(id='crab_spout_orb', fn='orb', n=8, fps=20, cols=4, S=160, radius_m=0.5, col=(150, 182, 196), dark=(78, 108, 128),
       plane='billboard', pivot='centre = the projectile body (r 0.5 m), loops in flight', ability='swampcrab_waterspout (lobbed area projectile)', trigger='cast_lob release f19 at the claw tips'),
  dict(id='crab_spout_splash', fn='ring', n=12, fps=24, cols=4, S=384, radius_m=3.0, col=(160, 190, 200), dark=(84, 116, 134),
       plane='ground', pivot='centre = the landing point (area r 3 m; the 5 s field is a runtime tint, not baked)', ability='swampcrab_waterspout landing', trigger='on projectile landing'),
 ],
 'maw': [
  dict(id='maw_bile_spray', fn='spray', n=16, fps=30, cols=4, W=576, H=256, length_m=3.0, width_m=1.0, col=(176, 172, 84), dark=(104, 110, 44),
       plane='ground', pivot='left-middle (the mouth, projected to the ground)', ability='chthoniandevourer_vomit (aoe wave 3 m long x 1 m wide, poison 3 s)',
       trigger='cast_spit release_s 1.2333 (f37); plays 0.53 s'),
  dict(id='maw_bite_impact', fn='impact', n=8, fps=30, cols=4, S=256, radius_m=0.55, col=(150, 46, 40), dark=(86, 24, 26),
       plane='billboard', pivot='centre = the jaw tip at contact', ability='chthoniandevourer_chomp / megachomp (melee 0-2.66 m)',
       trigger='attack_bite contact_s 0.3667 (f11); attack_bite_b contact_s 0.4 (f12)'),
 ],
}

def main():
    who, outdir = sys.argv[1], sys.argv[2]; os.makedirs(outdir, exist_ok=True); rows = []
    for P in PRESETS[who]:
        fn = P['fn']
        if fn == 'spray': fr, ppm = spray(P['n'], P['W'], P['H'], P['length_m'], P['width_m'], P['col'], P['dark'], **P.get('kw', {}))
        elif fn == 'impact': fr, ppm = impact(P['n'], P['S'], P['radius_m'], P['col'], P['dark'])
        elif fn == 'ring': fr, ppm = ring(P['n'], P['S'], P['radius_m'], P['col'], P['dark'])
        elif fn == 'orb': fr, ppm = orb(P['n'], P['S'], P['radius_m'], P['col'], P['dark'])
        elif fn == 'puff': fr, ppm = puff(P['n'], P['S'], P['radius_m'], P['col'], P['dark'])
        A = atlas(fr, P['cols']); path = os.path.join(outdir, P['id'] + '.png'); Image.fromarray(A, 'RGBA').save(path)
        h, w = fr[0][1].shape
        rows.append(dict(id=P['id'], atlas=os.path.basename(path), frames=P['n'], grid=[P['cols'], (P['n'] + P['cols'] - 1) // P['cols']], cell_px=[w, h],
                         fps=P['fps'], duration_s=round(P['n'] / P['fps'], 4), cell_m=[round(w / ppm, 4), round(h / ppm, 4)], px_per_m=round(ppm, 3),
                         plane=P['plane'], pivot=P['pivot'], ability=P['ability'], trigger=P['trigger'], alpha='straight', colorspace='sRGB', loop=fn == 'orb',
                         blend='normal (painted register: no additive glow)'))
        print('  %-22s %2d frames  cell %dx%d px = %.2f x %.2f m' % (P['id'], P['n'], w, h, w / ppm, h / ppm))
    json.dump(dict(creature=who, effects=rows), open(os.path.join(outdir, 'vfx_%s.json' % who), 'w'), indent=1)
    # preview strip
    prev = []
    for r in rows:
        im = Image.open(os.path.join(outdir, r['atlas'])); bg = Image.new('RGBA', im.size, (226, 218, 200, 255)); bg.alpha_composite(im); prev.append(bg.convert('RGB'))
    Wt = max(p.size[0] for p in prev); Ht = sum(p.size[1] for p in prev)
    sheet = Image.new('RGB', (Wt, Ht), (240, 236, 228)); y = 0
    for p in prev: sheet.paste(p, (0, y)); y += p.size[1]
    sheet.save(os.path.join(outdir, 'vfx_%s_preview.jpg' % who), quality=88)

if __name__ == '__main__':
    main()
