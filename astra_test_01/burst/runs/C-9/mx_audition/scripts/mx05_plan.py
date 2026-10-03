# MX audition (R-C9-149): from a body's spec (specs/<tag>.json) and its measures (work/meas_<tag>.json, mx03), write
#   work/stills_<tag>.json   every row's clip at its read time, 8 headings, scale 1
#   work/film_<tag>_<side>.json  one film plan per side (side 0 = the clip of record, 1.. = the candidates), with IDENTICAL step
#                            durations so the side-by-side film stays in step state for state.
# Still times: loops 0.5 s (walk/run 0.3 s); one-shots at their fastest-hand peak (mx03 'strike'); death at its end; emerge rows
# at 0 s, 45 % and 75 % of the clip (the rise). Film: idle 2.4 s, walk 3.0 s, run 2.0 s (driven at each side's own speed),
# one-shots max(lengths) + 0.5 s hold; idle at heading 25, the rest at 100 (en35's headings).
#   python3 scripts/mx05_plan.py <tag>
import json, sys
tag = sys.argv[1]; S = json.load(open('specs/%s.json' % tag)); M = json.load(open('work/meas_%s.json' % tag))['clips']
rows = []
for st in S['pairs']:
    state, clips = st[0], [c for c in st[1:] if c]
    for c in clips:
        if c not in M: continue
        r = M[c]; L = r['length_s']
        if state.startswith('emerge'): ts = [0.0, round(0.45 * L, 2), round(0.75 * L, 2)]
        elif r['loop']: ts = [0.3 if state in ('walk', 'run', 'crawl') else 0.5]
        elif state.startswith('death'): ts = [round(L, 2)]
        else: ts = [round(r['strike']['at_s'], 2)]
        for t in ts: rows.append([c, t])
json.dump({"shots": rows, "headings": [0, 45, 90, 135, 180, 225, 270, 315], "scales": [1], "watchdog_s": 1400, "settle_frames": 3},
          open('work/stills_%s.json' % tag, 'w'), indent=1)
nside = max(len([c for c in st[1:]]) for st in S['pairs'])
for side in range(nside):
    plan = []
    for st in S['pairs']:
        state, clips = st[0], list(st[1:])
        have = [c for c in clips if c and c in M]
        if not have: continue
        c = clips[side] if side < len(clips) and clips[side] in M else None
        loop = M[have[0]]['loop']
        if state in ('idle',) or (loop and state not in ('walk', 'run', 'crawl')): secs, hd = 2.4, 25
        elif state in ('walk', 'crawl'): secs, hd = 3.0, 100
        elif state == 'run': secs, hd = 2.0, 100
        else: secs, hd = round(max(M[x]['length_s'] for x in have) + 0.5, 4), (25 if state.startswith(('death', 'emerge', 'hit')) else 100)
        if c is None: plan.append(dict(clip=S.get('fallback_idle', 'idle'), seconds=secs, speed=0.0, heading_deg=hd, loop=True)); continue
        sp = M[c].get('drive_m_s', 0.0) if state in ('walk', 'run', 'crawl') else 0.0
        plan.append(dict(clip=c, seconds=secs, speed=sp, heading_deg=hd, loop=bool(M[c]['loop'])))
    json.dump({"shots": [], "headings": [], "scales": [], "watchdog_s": 1400, "film_plan": plan}, open('work/film_%s_%d.json' % (tag, side), 'w'), indent=1)
print('plan', tag, len(rows), 'still rows x 8 headings;', nside, 'film sides;', sum(1 for _ in S['pairs']), 'states')
