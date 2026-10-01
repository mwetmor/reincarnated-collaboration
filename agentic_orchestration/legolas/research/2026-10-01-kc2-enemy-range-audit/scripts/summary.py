import json, collections, math
R=json.load(open('compare.json'))
HALF_W = 960/75.668; HALF_H = 540/(75.668*math.sin(math.radians(52.9535411256029)))
ai=[r for r in R if r['delivery_class'].startswith('AI')]
def lo_ref(r):
    c=[x for x in (r.get('gd_use_range_centre_m_LO'),) if x is not None]
    if r.get('gd_band_max_m') is not None and r['slot'].startswith('special') and r.get('actorRadius') is not None:
        c.append(r['gd_band_max_m']+r['actorRadius']+0.3199999928474426)
    return min(c) if c else None
S={}
S['n_rows_loaded']=len(R)
S['by_delivery']=collections.Counter(r['delivery_class'] for r in R)
S['ai_rows']=len(ai)
S['ai_exceed_HI']=sum(1 for r in ai if r.get('FLAG_pack_exceeds_gd'))
S['ai_exceed_LO']=sum(1 for r in ai if lo_ref(r) is not None and r['pack_reach_m']>lo_ref(r)+1e-6)
S['ai_exceed_by_source']=collections.Counter(r['pack_reach_source'] for r in ai if r.get('FLAG_pack_exceeds_gd'))
S['ai_by_source']=collections.Counter(r['pack_reach_source'] for r in ai)
S['ai_exceed_in_pop']=sum(1 for r in ai if r.get('FLAG_pack_exceeds_gd') and (r['in_w151_160_pool'] or r['kind']=='pet'))
S['ai_exceed_by_more_than_1m']=sum(1 for r in ai if r.get('FLAG_pack_exceeds_gd') and r['diff_m']>1)
S['ai_exceed_by_more_than_5m']=sum(1 for r in ai if r.get('FLAG_pack_exceeds_gd') and r['diff_m']>5)
S['ai_exceed_by_more_than_10m']=sum(1 for r in ai if r.get('FLAG_pack_exceeds_gd') and r['diff_m']>10)
S['ai_pack_beyond_half_w']=sum(1 for r in ai if r['pack_reach_m']>HALF_W)
S['ai_pack_beyond_half_h']=sum(1 for r in ai if r['pack_reach_m']>HALF_H)
S['ai_gd_beyond_half_w']=sum(1 for r in ai if (r['gd_reference_reach_m'] or 0)>HALF_W)
S['ai_gd_beyond_half_h']=sum(1 for r in ai if (r['gd_reference_reach_m'] or 0)>HALF_H)
S['ai_pack_beyond_half_w_but_gd_within']=sum(1 for r in ai if r['pack_reach_m']>HALF_W and (r['gd_reference_reach_m'] or 0)<=HALF_W)
S['ai_under']=sum(1 for r in ai if r.get('diff_m') is not None and r['diff_m']< -1e-6)
au=[r for r in R if r['delivery_class'].startswith('AURA')]
S['aura_exceed']=sum(1 for r in au if r.get('FLAG_pack_exceeds_gd'))
dy=[r for r in R if r['delivery_class'].startswith('DYING')]
S['dying_exceed']=sum(1 for r in dy if r.get('FLAG_pack_exceeds_gd'))
# per-record rollup: max reach (the oracle's max_reach_m drives the engage clock)
recs=collections.defaultdict(list)
for r in R:
    if r['slot']=='dying': continue
    recs[r['record']].append(r)
roll=[]
for rec,rs in recs.items():
    pm=max(x['pack_reach_m'] for x in rs)
    gm=max([x['gd_reference_reach_m'] for x in rs if x.get('gd_reference_reach_m') is not None and x['delivery_class'].startswith('AI')] or [0])
    roll.append(dict(record=rec, pack_max_reach_m=pm, gd_max_ai_reach_m=round(gm,3), diff_m=round(pm-gm,3), in_pop=rs[0]['in_w151_160_pool'], kind=rs[0]['kind']))
S['records']=len(roll)
S['records_pack_max_exceeds_gd_max']=sum(1 for x in roll if x['diff_m']>1e-6)
S['records_pack_max_beyond_half_w']=sum(1 for x in roll if x['pack_max_reach_m']>HALF_W)
S['records_gd_max_beyond_half_w']=sum(1 for x in roll if x['gd_max_ai_reach_m']>HALF_W)
json.dump(roll,open('rollup.json','w'),indent=0)
for k,v in S.items(): print(k, dict(v) if isinstance(v,collections.Counter) else v)
json.dump({k:(dict(v) if isinstance(v,collections.Counter) else v) for k,v in S.items()},open('summary.json','w'),indent=1)
