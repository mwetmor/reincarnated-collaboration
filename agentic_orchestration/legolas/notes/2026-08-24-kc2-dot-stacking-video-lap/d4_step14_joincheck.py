"""STEP 14 — VALIDATE THE POOL JOIN. If riders are orphaned (their body is in no wave pool set),
the per-wave ceilings are UNDERSTATED and the Step-13 exceedance is an artifact of a bad join."""
import csv, collections
POOL='/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv'
LAPI='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense/pm4i_dot_riders.csv'
wave_recs=collections.defaultdict(set); allrecs=set()
for r in csv.DictReader(open(POOL)):
    try: w=int(r['global_wave'])
    except: continue
    if not (149<=w<=161): continue
    for col in ('roster_records','champ_records','pool_record','proxy_record'):
        for x in (r.get(col) or '').split('|'):
            x=x.strip()
            if x: wave_recs[w].add(x); allrecs.add(x)
riders=[r for r in csv.DictReader(open(LAPI)) if r['is_dot']=='True']
recs=set(r['record'] for r in riders)
orph=set()
for r in riders:
    if r['record'] not in allrecs and (r['summoner'] or '') not in allrecs:
        orph.add((r['record'], r['body_kind'], r['summoner']))
print(f'DoT rider rows {len(riders)}; distinct bodies {len(recs)}')
print(f'pool record universe (waves 149-161): {len(allrecs)}')
print(f'ORPHANED bodies (in NO wave pool, directly or via summoner): {len(orph)}')
for o in sorted(orph)[:20]: print('   ', o)
# per-wave matched rider counts
print('\nper-wave matched DoT-rider rows:')
for w in sorted(wave_recs):
    if not 151<=w<=160: continue
    n=sum(1 for r in riders if r['record'] in wave_recs[w] or (r['summoner'] or '') in wave_recs[w])
    print(f'   wave {w}: pool recs {len(wave_recs[w]):3d}  matched rider rows {n:3d}')
