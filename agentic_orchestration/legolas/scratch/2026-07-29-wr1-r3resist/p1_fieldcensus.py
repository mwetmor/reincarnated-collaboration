import sys, collections
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import _arz
names=collections.Counter()
for p,a in _arz:
    for n in a.recs:
        try: rt,f=a.fields(n)
        except: continue
        for k in f: names[k]+=1
print('total distinct fields', len(names))
import re
pat=re.compile(r'defensive|convert|conversion|resist', re.I)
for k,v in sorted(names.items()):
    if pat.search(k): print(f'{v:8d}  {k}')
