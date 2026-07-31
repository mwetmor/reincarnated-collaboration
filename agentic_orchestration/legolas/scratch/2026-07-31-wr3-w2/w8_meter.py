import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
for arcp in ["/Users/admin/Games/vendor/grim-dawn/resources/Text_EN.arc"]:
    p=pathlib.Path(arcp)
    if not p.exists(): print("missing",arcp); continue
    a=ArcArchive(p)
    names=list(a.entries.keys()) if hasattr(a,"entries") else list(a.names)
    print(arcp, len(names),"entries")
    for n in names:
        try: d=a.read_file(n).decode("utf-8","replace")
        except Exception:
            try: d=a.read_file(n).decode("utf-16","replace")
            except Exception: continue
        for line in d.split("\n"):
            if re.search(r'[Mm]eter', line):
                print(f"   [{n}] {line.strip()[:150]}")
