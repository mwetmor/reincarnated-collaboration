"""STEP 2 — dump the developer 'description' for every offensiveSlow* Variable in the live template."""
import sys, re; sys.path.insert(0,'.')
from d4b_lib import *
a = ArcArchive(VENDOR_E3/'database'/'templates.arc')
txt = a.read_file('templatebase/parameters_offensive.tpl').decode('utf-8-sig', errors='replace')
open('evidence/parameters_offensive.tpl','w').write(txt)
print('chars:', len(txt))
# Variable blocks: 'Variable\n{ ... }' -- brace matched shallowly (no nesting inside Variable)
blocks = re.findall(r'Variable\s*\{(.*?)\}', txt, re.S)
print('Variable blocks:', len(blocks))
def kv(b):
    d={}
    for m in re.finditer(r'(\w+)\s*=\s*"(.*?)"', b, re.S): d[m.group(1)]=m.group(2)
    return d
sel=[kv(b) for b in blocks]
sel=[d for d in sel if d.get('name','').startswith('offensiveSlow')]
print('offensiveSlow Variables:', len(sel))
for d in sel:
    print(f"  {d.get('name'):<45} type={d.get('type','?'):<10} desc={d.get('description','')!r}")
