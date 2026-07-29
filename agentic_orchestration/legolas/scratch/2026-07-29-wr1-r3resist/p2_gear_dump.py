import json, sys, re
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
G='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/gear_resolved.json'
d=json.load(open(G))
SKIP=re.compile(r'(Chance|XOR|Global|DamageFxPak|Style|bitmap|Texture|Mesh|Sound|fx|FX|Tag$|Text$|Description)',re.I)
KEEP=re.compile(r'^(defensive|character|conversion|.*Conversion|itemSkill|augmentSkill|petBonus|racial|skillName|modifiedSkillName|itemLevel|levelRequirement|lootRandomizerJitter|itemClassification|itemNameTag|lootRandomizerName|artifactName|Class)',re.I)
for it in d:
    print('='*100)
    print(f"GROUP {it['group']}  SLOT {it['slot']}  seed={it.get('seed')}")
    for part in ('baseName','prefixName','suffixName','componentName','augmentName','relicName','relicBonus','materiaCombines'):
        node=it.get(part)
        if not node: continue
        r=node['record'] if isinstance(node,dict) else node
        if not r: continue
        p,rt,f=get(r)
        if f is None:
            print(f"  [{part}] {r}  ** NOT FOUND **"); continue
        print(f"  [{part}] {r}   ({p} / {rt})")
        for k in sorted(f):
            v=f[k]
            if SKIP.search(k): continue
            if not KEEP.match(k): continue
            if v in (0,0.0,'',None): continue
            if isinstance(v,list) and not any(v): continue
            print(f"        {k} = {v}")
