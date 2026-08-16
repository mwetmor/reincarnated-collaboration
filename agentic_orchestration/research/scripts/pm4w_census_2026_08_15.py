import sys, pathlib, csv, json, collections
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts')
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive
GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
ORDER=["database/database.arz","gdx1/database/GDX1.arz","gdx2/database/GDX2.arz","gdx3/database/GDX3.arz",
       "mods/survivalmode/database/SurvivalMode.arz","survivalmode1/database/SurvivalMode1.arz",
       "survivalmode2/database/SurvivalMode2.arz","survivalmode3/database/SurvivalMode3.arz"]
arzs=[(r,ArzArchive(GD/r)) for r in ORDER]
def find(rec):
    for rel,a in reversed(arzs):
        if rec in a.records: return a.read_record(rec)
    return None
# tag tables
tags={}
for p in GD.rglob("*ext_[eE][nN].arc"):
    try: a=ArcArchive(p)
    except Exception: continue
    for n in a.names():
        if not n.endswith('.txt'): continue
        try: s=a.read_file(n).decode('utf-8','replace')
        except Exception: continue
        for line in s.splitlines():
            if '=' in line and not line.startswith('#'):
                k,v=line.split('=',1); tags[k.strip()]=v.strip()
def dispname(rec):
    d=find(rec)
    if not d: return None
    for k in ('description','displayName','tagName'):
        if k in d:
            t=str(d[k]); return tags.get(t,t)
    return None
def members(pool):
    d=find(pool)
    out=[]
    if not d: return out
    for i in range(1,7):
        for pre in ('name','nameChampion'):
            k=f'{pre}{i}'
            if k in d and d[k]: out.append((k,str(d[k])))
    return out
rows=list(csv.DictReader(open('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv')))
bywave=collections.defaultdict(lambda: collections.defaultdict(set))
for r in rows:
    bywave[int(r['global_wave'])][int(r['spawn_point'])].add(r['pool_record'])
out={}
for w in sorted(bywave):
    p06=bywave[w].get(6,set())
    if not p06: continue
    others=set()
    for sp,pools in bywave[w].items():
        if sp!=6: others|=pools
    def names(pools):
        s=set()
        for p in pools:
            for k,rec in members(p):
                n=dispname(rec)
                s.add(n if n else rec)
        return s
    n6=names(p06); no=names(others)
    S=sorted(n6-no)
    out[w]={'p06_pools':sorted(p06),'n_p06_names':len(n6),'n_other_names':len(no),
            'S_w_size':len(S),'S_w':S}
    print(f"wave {w}: |p06 names|={len(n6)} |other names|={len(no)} |S_w|={len(S)}")
    for s in S[:12]: print('    ', s)
    if len(S)>12: print('     ... +%d more'%(len(S)-12))
json.dump(out, open('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-w-p06-election/pm4w_p06_distinct_names.json','w'), indent=1)
