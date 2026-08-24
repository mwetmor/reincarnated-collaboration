"""STEP 15 — THE CONSERVATIVE POPULATION. Crucible waves overlap: a body spawned on an earlier
wave can still be alive later. The honest refresh-only ceiling at time t therefore uses the UNION
of pools for every wave up to and including the wave containing t (waves 151..W), not wave W alone.
This is the population that CANNOT understate the ceiling."""
import csv, collections
POOL='/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv'
LAPI='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense/pm4i_dot_riders.csv'
RES={'Bleeding':0.85,'Physical':0.16}
wave_recs=collections.defaultdict(set)
for r in csv.DictReader(open(POOL)):
    try: w=int(r['global_wave'])
    except: continue
    if not (149<=w<=161): continue
    for col in ('roster_records','champ_records','pool_record','proxy_record'):
        for x in (r.get(col) or '').split('|'):
            x=x.strip()
            if x: wave_recs[w].add(x)
riders=[r for r in csv.DictReader(open(LAPI)) if r['is_dot']=='True']
WAVES={151:(682.10,698.37),152:(698.38,714.63),153:(714.85,729.60),154:(729.62,743.73),
       155:(743.75,760.07),156:(760.08,780.28),157:(780.57,799.42),158:(799.43,812.53),
       159:(812.55,838.85),160:(838.87,868.32)}
def ceiling(recs, conv):
    best={}
    for r in riders:
        sms=[x.strip() for x in (r['summoner'] or '').split('|') if x.strip()]
        if r['record'] not in recs and not any(x in recs for x in sms): continue
        f=r['dot_family']
        try: v=float(r[conv]) if r[conv] else 0.0
        except ValueError: continue
        best[f]=max(best.get(f,0.0), v*(1-RES.get(f,0.80)))
    return sum(best.values())
plats=list(csv.DictReader(open('d4_plateaus.csv')))
print(f"{'plateau t':>10} {'wave':>5} {'obs HP/s':>9} | {'per-wave T':>10} {'per-wave P':>10} | {'CUMUL T':>9} {'CUMUL P':>9} | verdict")
for p in plats:
    t=float(p['t_start_s']); obs=float(p['implied_dot_hp_per_s'])
    w=next((k for k,(a,b) in WAVES.items() if a<=t<=b), None)
    if w is None: continue
    per=wave_recs[w]
    cum=set().union(*[wave_recs[x] for x in range(149,w+1) if x in wave_recs])
    pT=ceiling(per,'dps_if_field_is_total_lo'); pP=ceiling(per,'dps_if_field_is_per_second_lo')
    cT=ceiling(cum,'dps_if_field_is_total_lo'); cP=ceiling(cum,'dps_if_field_is_per_second_lo')
    v = 'EXCEEDS BOTH (cumulative)' if obs>cP else ('exceeds cumul TOTAL only' if obs>cT else 'within cumulative bracket')
    print(f'{t:10.4f} {w:5d} {obs:9.1f} | {pT:10.1f} {pP:10.1f} | {cT:9.1f} {cP:9.1f} | {v}')
