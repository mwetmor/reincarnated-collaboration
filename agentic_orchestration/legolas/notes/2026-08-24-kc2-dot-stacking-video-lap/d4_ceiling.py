"""Refresh-only CEILING: if at most ONE instance of each DoT family can sit on the target,
the maximum sustainable DoT drain is sum over families of (max single-rider dps) x (1-resist).
Player resistance sheet is Lap A MEASURED (via Lap M 2.1): physical 16, bleed 85, all others 80."""
import csv, collections
LAPI='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense/pm4i_dot_riders.csv'
RES={'Bleeding':0.85,'Poison':0.80,'Fire':0.80,'Cold':0.80,'Lightning':0.80,
     'Aether':0.80,'Chaos':0.80,'Life':0.80,'LifeLeach':0.80,'Physical':0.16}
rows=[r for r in csv.DictReader(open(LAPI)) if r['is_dot']=='True']
print(f'DoT rider rows: {len(rows)}')
fams=collections.Counter(r['dot_family'] for r in rows)
print('families:', dict(fams))
for conv in ('dps_if_field_is_total_lo','dps_if_field_is_per_second_lo'):
    best={}
    for r in rows:
        f=r['dot_family']
        try: v=float(r[conv]) if r[conv] else 0.0
        except ValueError: continue
        res=RES.get(f, 0.80)
        eff=v*(1-res)
        if eff>best.get(f,(0,None))[0]: best[f]=(eff, r['display_name'], v, r['record'].split('/')[-1])
    tot=sum(v[0] for v in best.values())
    print(f'\n--- convention: {conv} ---')
    for f,(eff,dn,raw,rec) in sorted(best.items(), key=lambda kv:-kv[1][0]):
        print(f'  {f:12s} raw dps {raw:9.2f}  x(1-{RES.get(f,0.8)}) -> {eff:8.2f} HP/s   [{rec}]')
    print(f'  REFRESH-ONLY CEILING (one instance per family, whole 150-160 corpus) = {tot:.2f} HP/s')
