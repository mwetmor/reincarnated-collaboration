#!/usr/bin/env python3
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
a=ArcArchive(pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc"))
for t in ["controllerai.tpl","controllermonster.tpl","controllerbasecharacter.tpl","controllercharacter.tpl"]:
    try: data=a.read(t)
    except Exception as e:
        try: data=a.read_file(t)
        except Exception as e2: print(t,"ERR",e,e2); continue
    print("#"*100); print("#",t,len(data),"bytes"); print("#"*100)
    print(data.decode("utf-8","replace"))
