import sys, glob
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
from arc_text import load_tags
TAGS=load_tags(sorted(glob.glob('/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/**/Text_EN.arc', recursive=True)))
def nz(v):
    if isinstance(v,list): return any(nz(x) for x in v)
    if isinstance(v,(int,float)): return v!=0
    return bool(v) and v!=''
def show(rec, only=None):
    p,rt,f=get(rec)
    if f is None: print(rec,'NOT FOUND'); return
    print(f'== {rec}  [{p}] type={rt}')
    dn=f.get('skillDisplayName') or f.get('itemNameTag') or f.get('lootRandomizerName')
    if dn: print('   displayName:', TAGS.get(dn, dn))
    for k in sorted(f):
        if k in ('skillConnectionOff','skillConnectionOn'): continue
        v=f[k]
        if only:
            if any(o.lower() in k.lower() for o in only): print(f'   {k} = {str(v)[:260]}')
        elif nz(v) and not isinstance(v,str): print(f'   {k} = {str(v)[:260]}')
        elif nz(v) and isinstance(v,str) and not v.startswith(('records/','ui/','creatures/','database/')):
            print(f'   {k} = {TAGS.get(v, v)[:200]}')
if __name__=='__main__':
    only = sys.argv[2].split(',') if len(sys.argv)>2 else None
    show(sys.argv[1], only)
