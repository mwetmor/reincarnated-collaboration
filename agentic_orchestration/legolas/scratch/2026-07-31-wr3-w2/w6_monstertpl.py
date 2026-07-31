import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
a=ArcArchive(pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc"))
d=a.read_file("monster.tpl").decode("utf-8","replace")
import re
# print blocks containing distress / call
lines=d.split("\n")
for i,l in enumerate(lines):
    if re.search(r'name = "(distressCall|distressCallTime|distressCallRange|maxDistressCalls|distressCallGroup|lowHealthResetLevel|championWeight|isBoss|monsterClassification)"',l):
        print("\n".join(lines[i:i+8])); print("-"*60)
