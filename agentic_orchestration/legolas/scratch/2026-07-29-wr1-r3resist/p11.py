import sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
for r in ['records/game/gamerandomizerweights.dbr','records/game/gameiteminfo.dbr','records/game/bonussharing.dbr']:
    p,rt,f=get(r)
    print('='*80); print(r,p,rt,len(f),'fields')
    for k in sorted(f):
        v=f[k]
        if isinstance(v,str) and ('.dbr' in v or '.tex' in v): continue
        print('   ',k,'=',v)
