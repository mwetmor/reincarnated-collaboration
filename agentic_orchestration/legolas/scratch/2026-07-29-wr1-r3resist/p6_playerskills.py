import sys,re
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
RES=re.compile(r'^(defensive|conversion|character(Life|Defensive|Offensive)|racial)',re.I)
SKIP=re.compile(r'(Chance|XOR|Global|FxPak|Style|Modifier$)',re.I)
targets={
 'records/skills/playerclass10/_classtraining_class10.dbr':5,
 'records/skills/playerclass10/amatokpact1.dbr':1,
 'records/skills/playerclass10/amatokpact1_buff.dbr':1,
 'records/skills/playerclass10/onslaught1.dbr':13,
 'records/skills/playerclass10/werewolf1.dbr':16,
 'records/skills/playerclass10/werewolf1b.dbr':1,
 'records/skills/playerclass10/passive02.dbr':1,
 'records/skills/itemskills/item_defenseknockdownnova_01.dbr':1,
}
for r,rank in targets.items():
    p,rt,f=get(r)
    if f is None: print('MISSING',r); continue
    print('='*90); print(f'{r}  ({p} / {rt})  rank={rank}  buffSkill={f.get("buffSkillName")}')
    for k in sorted(f):
        v=f[k]
        if not k.lower().startswith(('defensive','conversion')): continue
        if isinstance(v,list):
            if not any(v): continue
            print(f'   {k} = [rank{rank}] {v[min(rank-1,len(v)-1)]}   full={v[:20]}')
        else:
            if v in (0,0.0,'',None): continue
            print(f'   {k} = {v}')
