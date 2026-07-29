import sys,statistics as st
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import _arz
import collections
by=collections.defaultdict(list)
for p,a in _arz:
    for n in a.recs:
        if not n.startswith('records/items/gear'): continue
        try: rt,f=a.fields(n)
        except: continue
        dp=f.get('defensiveProtection'); il=f.get('itemLevel')
        if not dp or isinstance(dp,list): continue
        slot=n.split('/')[2]
        by[(slot,f.get('armorClassification'))].append((il,dp))
for k in sorted(by, key=lambda t:(t[0],str(t[1]))):
    v=by[k]
    lows=[dp for il,dp in v if il and 7<=il<=15]
    if not lows: continue
    print(f'{str(k):46s} n={len(v):4d}  itemLevel7-15: n={len(lows):3d} min={min(lows):6.1f} med={st.median(lows):6.1f} max={max(lows):6.1f}')
