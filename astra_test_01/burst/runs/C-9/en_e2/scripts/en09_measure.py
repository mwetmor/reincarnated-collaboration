# EN-E2 measures on the SHIPPED body (pure glTF, s17_loop_closure's evaluator, the clip's own keys and clock; +Y up, forward +Z):
#   release  cast_bolt: the leading hand's peak FORWARD speed; release_s = the key that ENDS the fastest interval (s18's THROW rule)
#            cast_area: the fastest interval of either hand in 3D (the push/slam that sets the ring down); release_s likewise
#   loops    idle/walk/run seam: worst joint position gap between the first and last key (m, at shipped scale)
#   speeds   walk/run m/s = the source's root travel (graft json, metres at the rig's scale) x the export scale / clip length
#   cell     the figure's extents over every clip (m from the origin): for the sprite-cell window
#   python3 scripts/en09_measure.py <body.glb> <graft.json> <height.json> --json <out>
import json, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure')
a = sys.argv[1:]; BODY, GJ, HJ = a[0], a[1], a[2]; OUT = a[a.index('--json') + 1]
m = C.model(BODY); k = json.load(open(HJ))['factor'] if HJ != '-' else 1.0
names = {i: m['nodes'][i].get('name') for i in m['joints']}
idx = {v: i for i, v in names.items()}
def keys(clip):
    return sorted({float(t) for v in m['anims'][clip].values() for t in v[0]})
def world(clip, t):
    G = C.globals_at(m, clip, t); S = C.globals_at(m, clip, t)  # noqa
    return {names[i]: G[i][:3, 3] for i in G if i in names}
# the body's root scale (e19) lives on the scene root, which globals_at includes; report in metres as drawn
rep = dict(body=BODY, export_scale=k, release={}, loops={}, speeds={}, extent={}, clip_len_s={})
for clip in m['anims']:
    ts = keys(clip); rep['clip_len_s'][clip] = round(ts[-1] - ts[0], 4)
    W = [world(clip, t) for t in ts]
    allp = np.array([p for w in W for p in w.values()])
    rep['extent'][clip] = dict(x=[round(float(allp[:, 0].min()), 3), round(float(allp[:, 0].max()), 3)],
                               y_top=round(float(allp[:, 1].max()), 3), z=[round(float(allp[:, 2].min()), 3), round(float(allp[:, 2].max()), 3)])
    if clip in ('idle', 'walk', 'run', 'glide'):
        rep['loops'][clip] = round(max(float(np.linalg.norm(W[0][n] - W[-1][n])) for n in W[0] if n != 'Hips'), 4)
    RULE = dict(cast_bolt='fwd', claw='fwd', cast_area='3d', aura='3d', attack='fwd', hurl='fwd', roar='3d', swipe='fwd', throw='fwd', buff='3d', slam='3d', lob='fwd', summon='3d', pound='3d')
    if clip in RULE:
        best = None
        for hand in ('LeftHand', 'RightHand'):
            for i in range(1, len(ts)):
                d = W[i][hand] - W[i - 1][hand]; dt = ts[i] - ts[i - 1]
                v = (d[2] / dt) if RULE[clip] == 'fwd' else (np.linalg.norm(d) / dt)
                if best is None or v > best[0]:
                    best = (v, hand, ts[i] - ts[0], i, [round(float(x), 3) for x in W[i][hand]])
        rep['release'][clip] = dict(hand=best[1], release_s=round(best[2], 4), key=best[3], speed_mps=round(float(best[0]), 3),
                                    hand_pos_m=best[4], rule='peak forward (+Z) hand speed' if RULE[clip] == 'fwd' else 'peak 3D hand speed')
g = json.load(open(GJ))
for nm, c in g['clips'].items():
    if nm in ('walk', 'run') and nm in rep['clip_len_s']:
        tr = c.get('source_travel_m'); L = rep['clip_len_s'][nm]
        rep['speeds'][nm] = dict(travel_m=round(float(np.hypot(*tr)) * k, 4), loop_s=L, m_per_s=round(float(np.hypot(*tr)) * k / L, 3),
                                 basis='source root travel over the clip (graft json) x export scale / shipped clip length')
json.dump(rep, open(OUT, 'w'), indent=1)
print(json.dumps(dict(release=rep['release'], loops=rep['loops'], speeds=rep['speeds'], len=rep['clip_len_s'])))
