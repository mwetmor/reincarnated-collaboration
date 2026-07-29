import json,sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
d=json.load(open('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/parsed.json'))
cs=d['blocks']['character_skills']
sk=cs['skills']
print('n skills',len(sk))
inv=[s for s in sk if s.get('level',0)>0 or s.get('devotionLevel',0)>0]
print('n with level>0:',len(inv))
for s in inv:
    print('  ',{k:v for k,v in s.items() if k in ('name','level','devotionLevel','enabled','autoCastSkill','autoCastController')})
print('itemSkills:',json.dumps(cs.get('itemSkills'),indent=1)[:2000])
