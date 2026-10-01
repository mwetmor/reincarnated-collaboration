import sys, pathlib, functools
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929")
STACK = [("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz"),("sm_mod",ROOT/"mods/survivalmode/database/SurvivalMode.arz"),("sm1",ROOT/"survivalmode1/database/SurvivalMode1.arz"),("sm2",ROOT/"survivalmode2/database/SurvivalMode2.arz"),("sm3",ROOT/"survivalmode3/database/SurvivalMode3.arz")]
@functools.lru_cache(maxsize=1)
def archives(): return [(k,ArzArchive(p)) for k,p in STACK]
@functools.lru_cache(maxsize=1)
def index():
    idx={}
    for k,a in archives():
        for r in a.records: idx.setdefault(r.lower(),[]).append((k,r))
    return idx
def read(path, which=None):
    o=index().get(path.lower().replace("\\","/"),[])
    if not o: return None,None
    k,r = o[-1] if which is None else [x for x in o if x[0]==which][0]
    a=dict(archives())[k]
    return a.read_record(r),k
