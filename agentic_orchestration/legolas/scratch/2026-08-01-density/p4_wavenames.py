#!/usr/bin/env python3
"""P4 - decode Crucible wave naming across all 4 survival archives. READ-ONLY."""
import sys, pathlib, collections, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
SM={"sm_mod":ROOT/"mods/survivalmode/database/SurvivalMode.arz",
    "sm1":ROOT/"survivalmode1/database/SurvivalMode1.arz",
    "sm2":ROOT/"survivalmode2/database/SurvivalMode2.arz",
    "sm3":ROOT/"survivalmode3/database/SurvivalMode3.arz"}
allnames=collections.defaultdict(set)
for k,p in SM.items():
    a=ArzArchive(p)
    for r in a.records:
        if r.count("/")>2 and r.split("/")[2].endswith("waves"):
            allnames[k].add(r)
for k in SM:
    print(f"{k}: {len(allnames[k])} wave records")
print("\n### tier15waves basenames (sm_mod) - all")
n=sorted(x.split("/")[-1] for x in allnames["sm_mod"] if "tier15waves" in x)
print(len(n)); print(n)
print("\n### tier01waves basenames (sm_mod) - all")
n=sorted(x.split("/")[-1] for x in allnames["sm_mod"] if "tier01waves" in x)
print(len(n)); print(n)
print("\n### tier20waves basenames (sm3) - all")
n=sorted(x.split("/")[-1] for x in allnames["sm3"] if "tier20waves" in x)
print(len(n)); print(n)
print("\n### basename regex conformance across ALL")
pat=re.compile(r"^proxy_w(\d+)_p(\d+)([a-z]*)\.dbr$")
bad=collections.Counter()
tot=0
for k in SM:
    for x in allnames[k]:
        tot+=1
        b=x.split("/")[-1]
        if not pat.match(b): bad[b]+=1
print(f"total={tot} nonconforming={sum(bad.values())}")
for b,c in bad.most_common(40): print("   ",b,c)
