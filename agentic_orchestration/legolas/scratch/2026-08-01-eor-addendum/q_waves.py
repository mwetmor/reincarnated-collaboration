import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"mods/survivalmode/database/SurvivalMode.arz")
rec=a.read_record("records/game/survivalinfo.dbr")
for k,v in sorted(rec.items()):
    s=str(v)
    print(f"{k} = {s[:400]}")
print()
tiers=[r for r in a.records if "tier" in r.lower() and "waves" in r.lower()]
print("tier-wave proxy dirs sample:", len(tiers))
import re
dirs=sorted({r.split('/')[1] if r.startswith('records/proxies/') else r for r in a.records if r.startswith('records/proxies/tier')})
print(sorted({re.match(r'records/proxies/(tier\d+waves)/',r).group(1) for r in a.records if re.match(r'records/proxies/tier\d+waves/',r)}))
