"""D-7 step 1 — recover the CombatAttributeType enum by disassembling every
GetType@DefenseAttribute*.  READ-ONLY.  Each GetType is `mov eax, <k>; ret`."""
import sys, re, json, collections; sys.path.insert(0, '.')
from d4b_dis import disasm, EX

rows = []
for n in sorted(EX):
    if not n.startswith('?GetType@'): continue
    cls = n.split('@')[1]
    try:
        ls = disasm(n, 6)
    except Exception:
        continue
    if not ls: continue
    m = re.search(r'mov\s+eax, (0x[0-9a-f]+|\d+)\s*$', ls[0])
    if not m: continue
    if len(ls) < 2 or 'ret' not in ls[1]: continue
    rows.append((int(m.group(1), 0), cls, EX[n]))

by_val = collections.defaultdict(list)
for v, c, r in rows: by_val[v].append(c)
print(f'# {len(rows)} constant GetType() bodies, {len(by_val)} distinct enum values')
for v in sorted(by_val):
    print(f'{v:#04x} {v:>4}  ' + ' | '.join(sorted(by_val[v])))
json.dump({str(v): sorted(by_val[v]) for v in by_val},
          open('evidence/combat_attribute_type_enum.json', 'w'), indent=1)
