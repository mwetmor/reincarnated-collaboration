import sys,re
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import _arz, get
fam=[]
for p,a in _arz:
    for n in a.recs:
        if '/lootaffixes/' not in n: continue
        if re.search(r'ad00[0-9]a_res_|ad0[0-9][0-9][a-z]_res_', n):
            fam.append((p,n))
fam.sort(key=lambda t:t[1])
for p,n in fam:
    _,rt,f=get(n)
    vals={k:v for k,v in f.items() if k.startswith('defensive') and v not in (0,0.0)}
    if not vals: continue
    print(f"{n.split('/')[-1]:34s} desc={f.get('FileDescription')!r:10s} jit={f.get('lootRandomizerJitter')} lvlReq={f.get('levelRequirement')} {vals}")
