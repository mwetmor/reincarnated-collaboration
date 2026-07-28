import glob, sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from arz_index import Arz
ROOT='/Users/admin/Games/vendor/grim-dawn-edition-II-20260724'
ORDER=['database/database.arz','gdx1/database/GDX1.arz','gdx2/database/GDX2.arz','gdx3/database/GDX3.arz']
_arz=[(p,Arz(f'{ROOT}/{p}')) for p in ORDER]
def get(rec):
    for p,a in _arz:
        if rec in a.recs:
            rt,f=a.fields(rec); return p,rt,f
    return None,None,None
def find(pat):
    out=[]
    for p,a in _arz:
        for n in a.recs:
            if pat.lower() in n.lower(): out.append((p,n))
    return out
def grep_field(field, pat=None):
    out=[]
    for p,a in _arz:
        for n in a.recs:
            if pat and pat.lower() not in n.lower(): continue
            try: rt,f=a.fields(n)
            except: continue
            if field in f: out.append((p,n,f[field]))
    return out
