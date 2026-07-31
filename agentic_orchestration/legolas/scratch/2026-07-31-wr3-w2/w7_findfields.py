import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
a=ArcArchive(pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc"))
names=list(a.entries.keys()) if hasattr(a,"entries") else list(a.names)
TARGET=re.compile(r'name = "(distressCall|distressCallTime|distressCallRange|maxDistressCalls|distressCallGroup|lowHealthResetLevel)"')
for n in names:
    try: d=a.read_file(n).decode("utf-8","replace")
    except Exception: continue
    if TARGET.search(d):
        print("#"*90); print("#",n); print("#"*90)
        lines=d.split("\n")
        # find enclosing group name
        grp=None
        for i,l in enumerate(lines):
            m=re.search(r'name = "([A-Za-z ]+)"',l)
            if m and i+1<len(lines) and 'type = "list"' in lines[i+1]: grp=m.group(1)
            if TARGET.search(l):
                print(f"   [group={grp}]")
                print("\n".join("   "+x for x in lines[i:i+8]))
