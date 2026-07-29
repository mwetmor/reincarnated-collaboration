import sys,re
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import _arz, get
seen=set()
for p,a in _arz:
    for n in a.recs:
        if n.startswith('records/game/') and n not in seen:
            seen.add(n); print(p,n)
