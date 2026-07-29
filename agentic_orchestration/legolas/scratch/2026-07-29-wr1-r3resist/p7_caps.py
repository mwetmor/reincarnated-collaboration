import sys,re
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
for r in ['records/game/gameengine.dbr','records/game/combatformulas.dbr']:
    p,rt,f=get(r)
    print('='*90); print(r,p,rt)
    for k in sorted(f):
        v=f[k]
        if re.search(r'cap|resist|defense|absorb|protect|equation|reduction',k,re.I):
            print(f'   {k} = {v}')
