"""STEP 1 — find the sustained-drain signature: runs of consecutive frames whose HP falls
steadily at small magnitude (no discrete direct hit). Such runs are DoT out-draining regen."""
import collections
from d4_lib import load_trace, deltas, contiguous_blocks, FPS

frames = load_trace()
blocks = contiguous_blocks(frames)
print(f'contiguous blocks: {len(blocks)}  frames: {len(frames)}')
d = deltas(frames)
print(f'adjacent pairs: {len(d)}')

# Classify frames
cls = collections.Counter()
for _,_,_,x in d:
    if x > 3: cls['leech/heal (>+3)'] += 1
    elif x in (2,3): cls['pure-regen band (+2,+3)'] += 1
    elif x in (0,1): cls['suppressed regen (0,+1)'] += 1
    elif -30 <= x < 0: cls['small negative (-1..-30)'] += 1
    else: cls['large negative (<-30)'] += 1
tot = len(d)
for k,v in cls.most_common(): print(f'  {k:28s} {v:6d}  {100*v/tot:5.1f}%')

# Hunt: maximal runs of consecutive frames with delta in [-LIM, 1] and mean strictly negative
LIM = 40
runs=[]; cur=[]
prev_f=None
for f,t,hp,x in d:
    ok = (prev_f is None or f == prev_f+1) and (-LIM <= x <= 1)
    if ok: cur.append((f,t,hp,x))
    else:
        if len(cur) >= 12: runs.append(cur)
        cur = [(f,t,hp,x)] if (-LIM <= x <= 1) else []
    prev_f=f
if len(cur) >= 12: runs.append(cur)

sig = []
for r in runs:
    dur=(r[-1][0]-r[0][0]+1)/FPS
    drop=r[0][2]-r[-1][2]-r[0][3]
    net=(r[-1][2]-r[0][2])/dur
    if net < -5: sig.append((r[0][1], dur, r[0][2], r[-1][2], net, r))
sig.sort(key=lambda z:-z[1])
print(f'\nSUSTAINED SMALL-DRAIN RUNS (>=0.2s, all deltas in [-{LIM},+1], net slope < -5 HP/s): {len(sig)}')
print(f"{'t_start':>10} {'dur_s':>7} {'hp0':>6} {'hp1':>6} {'net HP/s':>10} {'drain(+regen)':>14}")
REGEN = 129.38
for t0,dur,h0,h1,net,r in sig[:30]:
    print(f'{t0:10.4f} {dur:7.4f} {h0:6d} {h1:6d} {net:10.2f} {REGEN-net:14.2f}')
