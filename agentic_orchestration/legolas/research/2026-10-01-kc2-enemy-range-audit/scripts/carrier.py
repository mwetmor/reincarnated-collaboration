import csv, json, collections
D='/Users/admin/Games/reincarnated-engine/data/kc2/'
def rd(f): return list(csv.DictReader(open(D+f, newline='')))
meta={}
for f in ['pm2_tg2_attack_slots.csv','q91_pool338_attack_slots.csv']:
    for r in rd(f): meta.setdefault((r['record'],r['slot']), r)
dmg=collections.defaultdict(list); byskill=collections.defaultdict(list)
for f in ['pm2_tg2_attack_damage.csv','q91_pool338_attack_damage.csv']:
    for r in rd(f):
        dmg[(r['record'],r['slot'])].append(r); byskill[(r['record'],r['skill'])].append(r)
def f(x):
    try: v=float(x); return v if v else None
    except: return None
R=json.load(open('compare.json'))
c=collections.Counter()
for r in R:
    key=(r['record'],r['slot']); m=meta.get(key,{}); rows=dmg.get(key,[])
    if r['slot'] in ('tree_attack','toggled_aura'):
        m={}; rows=byskill.get((r['record'],r['skill']),[])
    pr=r['pack_reach_m']; hit=None
    chain=[('slot-meta','projectile_distance',m,None)]+[('damage-row','projectile_distance',x,x) for x in rows]+[('slot-meta','skill_radius',m,None)]+[('damage-row',k,x,x) for x in rows for k in ('skill_target_radius','projectile_explosion_radius')]
    for src,fld,row,x in chain:
        v=f(row.get(fld)) if row else None
        if v is not None:
            hit=(src,fld,v,x); break
    if hit and abs(hit[2]-pr)<1e-6:
        src,fld,v,x=hit
        nest = (x.get('nest_via_field') or '') if x else ''
        sk = (x.get('skill') if x else m.get('skill')) or ''
        r['pack_reach_source']=f"{src}.{fld}" + (f" via {nest}" if nest else "")
        r['pack_reach_source_skill']=sk
        r['pack_reach_source_projectile']=(x.get('projectile') if x else m.get('projectile')) or ''
        c[r['pack_reach_source']]+=1
    elif not hit and abs(pr-2.4)<1e-6:
        r['pack_reach_source']='MELEE_REACH_M fallback (no carrier)'; c[r['pack_reach_source']]+=1
    else:
        r['pack_reach_source']='UNATTRIBUTED (first carrier %s != pack %s)'%(hit[2] if hit else None, pr); c['UNATTRIBUTED']+=1
json.dump(R,open('compare.json','w'),indent=0)
for k,v in c.most_common(): print(v,k)
