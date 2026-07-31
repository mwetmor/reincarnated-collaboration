import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
a=ArcArchive(pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc"))
d=a.read_file("controllerai.tpl").decode("utf-8","replace")
lines=d.split("\n"); grp=None
print("COMPLETE controllerai.tpl FIELD SURFACE (group -> field : type = default)")
for i,l in enumerate(lines):
    m=re.search(r'name = "([^"]+)"',l)
    if not m: continue
    if i+1<len(lines) and 'type = "list"' in lines[i+1]:
        grp=m.group(1); print(f"\n[{grp}]"); continue
    blk="\n".join(lines[i:i+7])
    t=re.search(r'type = "([^"]*)"',blk); dv=re.search(r'defaultValue = "([^"]*)"',blk)
    ds=re.search(r'description = "([^"]*)"',blk)
    print(f"   {m.group(1):34s} {t.group(1) if t else '?':8s} default={dv.group(1) if dv else '':<28} {ds.group(1) if ds else ''}")
