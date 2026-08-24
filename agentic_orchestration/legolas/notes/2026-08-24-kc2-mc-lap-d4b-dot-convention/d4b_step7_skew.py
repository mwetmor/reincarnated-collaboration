"""STEP 7 — VERSION-SKEW CHECK. The convention is decoded from Game.dll in the `vendor/grim-dawn`
pull (v1.2.3.4, 2026-07-23); Lap I's magnitudes come from the edition-III .arz (2026-08-08).
templates.arc differs between the pulls, so the DoT schema must be shown unchanged before the
decode is allowed to transfer. A negative here would bracket the verdict; it is checked, not assumed."""
import sys, re; sys.path.insert(0,'.')
from d4b_lib import *
import pathlib
A = pathlib.Path('/Users/admin/Games/vendor/grim-dawn')
B = VENDOR_E3
def slowvars(root):
    a = ArcArchive(root/'database'/'templates.arc')
    txt = a.read_file('templatebase/parameters_offensive.tpl').decode('utf-8-sig', errors='replace')
    out = []
    for b in re.findall(r'Variable\s*\{(.*?)\}', txt, re.S):
        d = dict(re.findall(r'(\w+)\s*=\s*"(.*?)"', b, re.S))
        if d.get('name','').startswith('offensiveSlow'):
            out.append((d['name'], d.get('class'), d.get('type'), d.get('description'), d.get('defaultValue')))
    return out
va, vb = slowvars(A), slowvars(B)
print(f'grim-dawn (v1.2.3.4 pull) offensiveSlow vars : {len(va)}')
print(f'edition-III pull          offensiveSlow vars : {len(vb)}')
print('IDENTICAL (name/class/type/description/default):', va == vb)
if va != vb:
    sa, sb = {x[0] for x in va}, {x[0] for x in vb}
    print('  only in grim-dawn :', sorted(sa-sb))
    print('  only in editionIII:', sorted(sb-sa))
    for x, y in zip(sorted(va), sorted(vb)):
        if x != y: print('  DIFF', x, '->', y)
