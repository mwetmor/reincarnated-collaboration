# MX audition (R-C9-149): per-clip measures on an audition GLB (clips of record + grafted Mixamo clips on ONE body), pure glTF
# evaluation (en_e2 s17_loop_closure's evaluator; world metres, +Y up, the body faces +Z).
#   length / keys      the clip's natural length (s) and its key count (30 fps)
#   arm elevation      each upper arm's angle from hanging straight down (deg; 0 at the side, 90 level, >90 above the shoulder),
#                      mean and max over every key -- en56_arm_calm's measure, against world +Y
#   foot slide (loops) en_e2 s6 estimator: an ANKLE is planted in the bottom 25 % of its own height range; the median BACKWARD
#                      speed of a planted ankle, dense 60 Hz; slide = |foot speed - drive speed| / drive speed, where the drive
#                      speed is the speed the runtime moves the record (the manifest's for clips of record; the source's own root
#                      travel / length for a graft, the en09 rule)
#   foot creep (non-locomotion) the largest horizontal travel of a planted ankle (within 3 cm of its own lowest) inside one
#                      contiguous contact, m -- a planted foot that skates in an idle or a strike
#   loop seam          largest joint gap between the first and last key, m (loops only)
#   figure             skinned-mesh extent: top (m), lowest point at t=0, head height at t=0 / at rest (crouch ratio), and the
#                      hips height at t=0 / rest -- for an emerge: does the body START at or below the snow line, or crouched
#   strike             the fastest hand (3D speed) and the time of its peak (s), one-shots only
#   python3 scripts/mx03_measure.py <aud.glb> <graft.json|-> <manifest_clips.json|-> [--loops a,b] [--json out]
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', 'en_e2', 'scripts'))
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = sys.argv[1:]; GLB, GJ, MJ = a[0], a[1], a[2]
outj = a[a.index('--json') + 1] if '--json' in a else None
m = C.model(GLB); js, b = L.load_glb(GLB); nid = m['nid']
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
graft = json.load(open(GJ))['clips'] if GJ != '-' else {}
man = json.load(open(MJ)) if MJ != '-' else {}
LOOPS = set(a[a.index('--loops') + 1].split(',')) if '--loops' in a else set()
def keys(clip): return sorted({float(t) for ch in m['anims'][clip].values() for t in ch[0]})
def P(G, n): return G[nid[n]][:3, 3]
Grest = C.globals_at(m, next(iter(m['anims'])), -1.0) if False else None
G0 = W.globals_(js)[0]; Vr = W.skin_rest(js, b, mn, G0); rest_head = float(P(G0, 'Head')[1]); rest_hips = float(P(G0, 'Hips')[1])
rest_top = float(Vr[:, 1].max())
rep = dict(glb=os.path.basename(GLB), rest=dict(top_m=round(rest_top, 3), head_m=round(rest_head, 3), hips_m=round(rest_hips, 3)), clips={})
for clip in m['anims']:
    if clip.startswith('Armature') or clip.startswith('chk_'): continue
    T = keys(clip); r = dict(length_s=round(T[-1] - T[0], 4), keys=len(T))
    Gs = [C.globals_at(m, clip, t) for t in T]
    # arm elevation
    for side in ('Left', 'Right'):
        el = []
        for G in Gs:
            d = P(G, side + 'ForeArm') - P(G, side + 'Arm'); d /= np.linalg.norm(d); el.append(float(np.degrees(np.arccos(np.clip(-d[1], -1, 1)))))
        r['arm_%s' % side[0]] = dict(mean=round(float(np.mean(el)), 1), max=round(max(el), 1))
    loop = clip in LOOPS or clip in ('idle', 'walk', 'run') or 'loop' in graft.get(clip, {}).get('flags', [])
    r['loop'] = loop
    if loop:
        r['seam_m'] = round(max(float(np.linalg.norm(Gs[0][i][:3, 3] - Gs[-1][i][:3, 3])) for i in m['joints']), 4)
    # drive speed
    v = None
    if clip in graft and 'source_travel_m' in graft[clip]:
        tr = graft[clip]['source_travel_m']; v = float(np.hypot(*tr)) / max(graft[clip]['length_s'], 1e-9)
    elif clip in man.get('locomotion_in_place', {}):
        v = float(man['locomotion_in_place'][clip]['speed_m_s'])
    dense = np.arange(T[0], T[-1] + 1e-9, 1 / 60)
    Fd = {f: np.array([P(C.globals_at(m, clip, t), f) for t in dense]) for f in ('LeftFoot', 'RightFoot')}
    if loop and v is not None and v > 0.2:
        sp = []
        for f, X in Fd.items():
            y = X[:, 1]; thr = y.min() + 0.25 * (y.max() - y.min()); pl = y <= thr
            for i in range(len(dense) - 1):
                if pl[i] and pl[i + 1]: sp.append(-(X[i + 1, 2] - X[i, 2]) * 60)
        fs = float(np.median(sp)) if sp else float('nan')
        r['drive_m_s'] = round(v, 3); r['foot_m_s'] = round(fs, 3); r['slide_pct'] = round(100 * abs(fs - v) / v, 1)
    else:
        cr = 0.0
        for f, X in Fd.items():
            y = X[:, 1]; pl = y <= y.min() + 0.03; s = None
            for i in range(len(dense)):
                if pl[i]:
                    s = i if s is None else s; cr = max(cr, float(np.hypot(*(X[i, [0, 2]] - X[s, [0, 2]]))))
                else: s = None
        r['foot_creep_m'] = round(cr, 3)
        if v is not None: r['drive_m_s'] = round(v, 3)
    # figure (skinned) at t=0 and over ~8 samples
    idx = sorted(set(np.linspace(0, len(T) - 1, 8).astype(int)))
    tops, lows = [], []
    for i in idx:
        V = W.skin_rest(js, b, mn, Gs[i]); tops.append(float(V[:, 1].max())); lows.append(float(V[:, 1].min()))
        if i == 0: r['t0'] = dict(low_m=round(lows[-1], 3), top_m=round(tops[-1], 3), head_ratio=round(float(P(Gs[0], 'Head')[1]) / rest_head, 3),
                                  hips_ratio=round(float(P(Gs[0], 'Hips')[1]) / rest_hips, 3))
    r['top_m'] = round(max(tops), 3); r['low_min_m'] = round(min(lows), 3)
    if not loop:
        best = (0, 0, '')
        for h in ('LeftHand', 'RightHand'):
            X = np.array([P(G, h) for G in Gs]); s = np.linalg.norm(np.diff(X, axis=0), axis=1) * 30
            k = int(np.argmax(s)); best = max(best, (float(s[k]), T[k + 1] - T[0], h))
        r['strike'] = dict(hand=best[2], peak_m_s=round(best[0], 2), at_s=round(best[1], 4))
    rep['clips'][clip] = r
    print('%-14s %5.2fs %3dk | armL %5.1f/%5.1f armR %5.1f/%5.1f | %s | top %.2f low %.2f t0 low %.2f head %.2f hips %.2f%s' % (
        clip, r['length_s'], r['keys'], r['arm_L']['mean'], r['arm_L']['max'], r['arm_R']['mean'], r['arm_R']['max'],
        ('drive %.2f foot %.2f slide %4.1f%% seam %.3f' % (r['drive_m_s'], r['foot_m_s'], r['slide_pct'], r.get('seam_m', 0))) if 'slide_pct' in r
        else ('creep %.3f%s' % (r['foot_creep_m'], (' seam %.3f' % r['seam_m']) if 'seam_m' in r else '')),
        r['top_m'], r['low_min_m'], r['t0']['low_m'], r['t0']['head_ratio'], r['t0']['hips_ratio'],
        (' | strike %s %.1f m/s @%.2fs' % (r['strike']['hand'][:1], r['strike']['peak_m_s'], r['strike']['at_s'])) if 'strike' in r else ''))
if outj: json.dump(rep, open(outj, 'w'), indent=1)
