"""D-4c STEP 5 — D-4b Q4: how do `offensiveSlow<X>Global` and `offensiveSlow<X>XOR...` participate?
Read the authoring schema for every offensiveSlow* Variable and classify. READ-ONLY."""
import sys, re; sys.path.insert(0, '.')
from d4b_lib import ArcArchive, VENDOR_FULL

a = ArcArchive(VENDOR_FULL / 'database' / 'templates.arc')
blob = a.read_file('templatebase/parameters_offensive.tpl').decode('latin-1')

blocks = re.findall(r'Variable\s*\{(.*?)\}', blob, re.S)
recs = []
for b in blocks:
    d = dict(re.findall(r'(\w+)\s*=\s*"(.*?)"', b))
    if d.get('name', '').startswith('offensiveSlow'):
        recs.append(d)

def kind(n):
    if n.endswith('Global'): return 'Global'
    if 'XOR' in n: return 'XOR'
    if n.endswith(('Min', 'Max')) and 'Duration' not in n: return 'magnitude'
    if 'Duration' in n: return 'duration'
    if n.endswith('Chance'): return 'chance'
    if n.endswith('Modifier'): return 'modifier'
    return 'other'

from collections import Counter, defaultdict
c = Counter(kind(r['name']) for r in recs)
print(f'offensiveSlow* Variables: {len(recs)}   by kind: {dict(c)}')
byk = defaultdict(list)
for r in recs: byk[kind(r['name'])].append(r)
for k in ('Global', 'XOR'):
    print(f'\n--- {k} ({len(byk[k])}) ---')
    for r in byk[k][:8]:
        print(f"  {r['name']:<46} class={r.get('class'):<8} type={r.get('type'):<7} "
              f"default={r.get('defaultValue','')!r}  desc={r.get('description','')!r}")
    names = sorted(x['name'] for x in byk[k])
    print(f'  all names: {names}')
