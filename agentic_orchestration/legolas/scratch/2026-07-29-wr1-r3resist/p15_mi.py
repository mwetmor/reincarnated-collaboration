import sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import _arz, get
tgt='records/items/gearaccessories/necklaces/b001_necklace.dbr'
hits=[]
for p,a in _arz:
    for n in a.recs:
        try: rt,f=a.fields(n)
        except: continue
        for k,v in f.items():
            if isinstance(v,str) and v.lower()==tgt: hits.append((p,n,k))
            elif isinstance(v,list) and any(isinstance(x,str) and x.lower()==tgt for x in v): hits.append((p,n,k))
for h in hits[:40]: print(h)
print('n refs',len(hits))
# what does the boss record point to for loot
p,rt,f=get('records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr')
for k,v in sorted(f.items()):
    if 'loot' in k.lower() and v not in (0,0.0,'',None): print('BOSS',k,'=',v)
