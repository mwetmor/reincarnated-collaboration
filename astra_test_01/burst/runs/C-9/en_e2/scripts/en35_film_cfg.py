# EN-E2 round 4: film + stills configs for a melee body from its own measure (en09). The VFX kind per one-shot is named here.
#   python3 scripts/en35_film_cfg.py <g> <vfx spec: clip=kind[:speed:range|:dist],...> <stills clips a,b,c,d>
import json, sys
g, VS, SC = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
M = json.load(open('export/final_%s/en_%s_measure.json' % (g, g))); rel = M['release']; Lc = M['clip_len_s']; sp = M['speeds']
vfx = {}
for x in VS.split(','):
    c, k = x.split('='); parts = k.split(':'); vfx[c] = parts
plan = []
if 'emerge' in Lc: plan.append(dict(clip='emerge', seconds=Lc['emerge'], speed=0.0, heading_deg=25))
plan += [dict(clip='idle', seconds=2.4, speed=0.0, heading_deg=25), dict(clip='walk', seconds=3.0, speed=sp['walk']['m_per_s'], heading_deg=100),
         dict(clip='run', seconds=2.0, speed=sp['run']['m_per_s'], heading_deg=100), dict(clip='idle', seconds=0.6, speed=0.0, heading_deg=100)]
for c in [k for k in Lc if k in rel]:
    s = dict(clip=c, seconds=Lc[c], speed=0.0, heading_deg=100, release_s=rel[c]['release_s'], hand=rel[c]['hand'])
    if c in vfx:
        p = vfx[c]; s['vfx'] = p[0]
        if p[0] == 'bolt': s['speed_vfx'] = float(p[1]); s['range'] = float(p[2])
        if p[0] == 'area': s['dist'] = float(p[1])
    plan.append(s)
plan += [dict(clip='hit', seconds=Lc['hit'], speed=0.0, heading_deg=25), dict(clip='death', seconds=Lc['death'] + 1.0, speed=0.0, heading_deg=25)]
json.dump({"shots": [], "headings": [], "scales": [], "watchdog_s": 2000, "film_plan": plan}, open('work/film_%s.json' % g, 'w'), indent=1)
shots = [[c, rel[c]['release_s'] if c in rel else (Lc[c] if c == 'death' else 0.3 if c in ('walk', 'run') else 0.5)] for c in SC]
json.dump({"shots": shots, "headings": [0, 45, 90, 135, 180, 225, 270, 315], "scales": [1], "watchdog_s": 1500, "settle_frames": 4}, open('work/stills_%s.json' % g, 'w'), indent=1)
print('cfg', g, [p['clip'] for p in plan])
