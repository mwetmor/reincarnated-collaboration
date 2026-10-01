# E1 timing table: every clip's duration RE-READ FROM THE SHIPPED GLB ((keys-1) intervals, on its own key times), its action
# instant measured on the clip, against the packet's (legolas 2026-10-01 packet.json, the README table B). Rate-free authoring:
# the runtime applies the packet's laws, so the column that matters is the playback rate the runtime must use.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); ROOT = os.path.dirname(HERE)
C = __import__('s17_loop_closure')
BODY = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'export', 'wl_body.glb')
PK = {  # state: (packet clip, native s, action s or None, law note)
 'idle': ('combat idle', 2.000, None, 'unscaled'), 'walk': ('walk', 1.000, None, 'unscaled (when GD plays the walk is not in data)'),
 'run': ('run', 0.800, None, 'law 5: x1.35 -> 0.593 s'),
 'attack': ('attack A (45% of the chain)', 0.667, 0.233, 'law A 0.376 s (hit 0.132) / law B 0.340 s (hit 0.119)'),
 'hit': ('get hit', 0.667, None, 'unscaled'), 'death': ('death', 3.000, None, 'unscaled'),
 'warcry': ('War Cry', 0.600, 0.367, 'law 4: x1.84 cast speed -> 0.326 s, shout 0.199 s')}
m = C.model(BODY); nid = m['nid']; W = json.load(open(os.path.join(ROOT, 'work', 'weapon.json')))
rows = []
for st, (pn, pt, pa, law) in PK.items():
    ch = m['anims'][st]; tt = sorted({float(t) for v in ch.values() for t in v[0]}); T = tt[-1] - tt[0]
    act = None; how = ''
    if st == 'attack':
        act = W['strike']['t'] - tt[0]; how = 'mace head lowest after its highest (e12 strike assert)'
    if st == 'warcry':
        hy = [C.globals_at(m, st, t)[nid['RightHand']][1, 3] for t in tt]; act = tt[int(np.argmax(hy))] - tt[0]; how = 'right fist (the raised mace) highest'
    r = dict(state=st, packet_clip=pn, packet_s=pt, clip_s=round(T, 4), keys=len(tt), runtime_rate_to_packet=round(T / pt, 3),
             packet_action_s=pa, clip_action_s=None if act is None else round(act, 4),
             action_frac_clip=None if act is None else round(act / T, 3), action_frac_packet=None if pa is None else round(pa / pt, 3),
             action_measure=how, packet_law=law)
    rows.append(r)
json.dump(rows, open(os.path.join(ROOT, 'work', 'timing_table.json'), 'w'), indent=1)
print('%-7s %-28s %7s %7s %6s %7s %7s %6s %6s' % ('state', 'packet clip', 'pkt s', 'clip s', 'rate', 'pkt act', 'clip act', 'pkt %', 'clip %'))
for r in rows:
    f = lambda v: '-' if v is None else str(v)
    print('%-7s %-28s %7s %7s %6s %7s %7s %6s %6s' % (r['state'], r['packet_clip'][:28], r['packet_s'], r['clip_s'], r['runtime_rate_to_packet'], f(r['packet_action_s']), f(r['clip_action_s']), f(r['action_frac_packet']), f(r['action_frac_clip'])))
