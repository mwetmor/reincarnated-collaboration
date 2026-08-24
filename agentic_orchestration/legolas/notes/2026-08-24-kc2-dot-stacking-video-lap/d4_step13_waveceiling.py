"""STEP 13 — PER-WAVE refresh-only ceiling, built from the POOL (what CAN spawn on wave W),
never from the frozen baton ROLL (Lap M's population law: the referent rolled its own board).
Ceiling(W) = sum over DoT families of max single-rider dps among bodies the wave-W pools can
place (plus their summons), x (1 - player resist)."""
import csv, collections, statistics
POOL='/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv'
LAPI='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense/pm4i_dot_riders.csv'
RES={'Bleeding':0.85,'Physical':0.16}
wave_recs=collections.defaultdict(set)
for r in csv.DictReader(open(POOL)):
    try: w=int(r['global_wave'])
    except: continue
    if not (149<=w<=161): continue
    for col in ('roster_records','champ_records','pool_record','proxy_record'):
        v=r.get(col) or ''
        for x in v.split('|'):
            x=x.strip()
            if x: wave_recs[w].add(x)
print('pool records per wave:', {w:len(v) for w,v in sorted(wave_recs.items())})
riders=[r for r in csv.DictReader(open(LAPI)) if r['is_dot']=='True']
WAVES={151:(682.10,698.37),152:(698.38,714.63),153:(714.85,729.60),154:(729.62,743.73),
       155:(743.75,760.07),156:(760.08,780.28),157:(780.57,799.42),158:(799.43,812.53),
       159:(812.55,838.85),160:(838.87,868.32)}
def ceiling(w, conv):
    recs=wave_recs.get(w,set()); best={}
    for r in riders:
        rec=r['record']
        sms=[x.strip() for x in (r['summoner'] or '').split('|') if x.strip()]
        if rec not in recs and not any(x in recs for x in sms): continue
        f=r['dot_family']
        try: v=float(r[conv]) if r[conv] else 0.0
        except ValueError: continue
        eff=v*(1-RES.get(f,0.80))
        best[f]=max(best.get(f,0.0), eff)
    return sum(best.values()), best
plats=list(csv.DictReader(open('d4_plateaus.csv')))
print(f"\n{'plateau t':>10} {'wave':>5} {'observed HP/s':>14} {'ceil TOTAL':>11} {'ceil PERSEC':>12} {'verdict':>28}")
for p in plats:
    t=float(p['t_start_s']); obs=float(p['implied_dot_hp_per_s'])
    w=next((k for k,(a,b) in WAVES.items() if a<=t<=b), None)
    if w is None: continue
    cT,_=ceiling(w,'dps_if_field_is_total_lo'); cP,_=ceiling(w,'dps_if_field_is_per_second_lo')
    if obs>cP:   v='EXCEEDS BOTH -> stacking'
    elif obs>cT: v='exceeds TOTAL limb only'
    else:        v='within both -> no discrimination'
    print(f'{t:10.4f} {w:5d} {obs:14.1f} {cT:11.1f} {cP:12.1f} {v:>28}')
