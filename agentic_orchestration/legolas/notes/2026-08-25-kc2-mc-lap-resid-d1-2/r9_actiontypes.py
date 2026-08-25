"""RESID-D1-2 step 9 — decode the CharacterActionType enum (the matrix's index space) by reading
each *Action class' constructor for its `[this+8] = <type>` store, paired with the vtable it
installs.  Nothing is named by guess; a class whose ctor does not store a literal type is listed
UNRESOLVED rather than assumed.  READ-ONLY."""
import sys, re, json; sys.path.insert(0, '.')
import d8_lib as L, d4b_dis as D

ctors = sorted((r, n) for n, r in D.EX.items()
               if re.match(r'\?\?0\w*Action\w*@GAME@@QAE@', n) and 'Packet' not in n and 'Handler' not in n)
seen = {}
rows = []
for rva, name in ctors:
    if rva in seen:
        rows.append((name, seen[rva], 'ICF-shared-body'))
        continue
    lines = L.bounded(rva, 200)
    ty = None
    vt = None
    for ln in lines:
        t = ln.split(None, 1)[1].split('   ;')[0]
        t = re.sub(r'\s+', ' ', t).strip()
        m = re.match(r'mov dword ptr \[\w+ \+ 8\], (0x[0-9a-f]+|\d+)$', t)
        # take the LAST such store: the base ctor is inlined first and writes 0, the derived ctor
        # then overwrites with its own type.  Taking the first yields 0 for every class.
        if m: ty = int(m.group(1), 0)
        m2 = re.match(r'mov dword ptr \[\w+\], (0x10[0-9a-f]{6})$', t)
        if m2:
            v = int(m2.group(1), 0) - D.pe.image_base
            s = D.sym(v)
            if s and s.startswith('??_7'): vt = s
    seen[rva] = ty
    rows.append((name, ty, vt))

by_type = {}
for name, ty, vt in rows:
    if ty is None: continue
    by_type.setdefault(ty, []).append(name.split('@')[0][3:])

out = ['CharacterActionType enum — decoded from each *Action ctor\'s `[this+8] = <literal>` store',
       '(index space of the GameEngine+0x2802c permission matrix)', '']
for ty in sorted(by_type):
    out.append(f'  type {ty:2d} (0x{ty:02x}) : ' + ', '.join(sorted(set(by_type[ty]))))
unres = sorted({n.split('@')[0][3:] for n, t, v in rows if t is None})
out += ['', f'UNRESOLVED (ctor stores no literal type; copy-ctors and base ctors): {len(unres)}',
        '  ' + ', '.join(unres)]
open('evidence/73-action-type-enum.txt', 'w').write('\n'.join(out) + '\n')
json.dump({str(k): sorted(set(v)) for k, v in by_type.items()},
          open('evidence/73-action-type-enum.json', 'w'), indent=1)
print('\n'.join(out))
