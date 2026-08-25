"""MD-B4app-9 step 3 — decode Character_LifeState BY NAME from GetLifeStateAsText's shipped
string table, the same method the prior lap used for Character_ActionState.  READ-ONLY.
No enum value is named by inference; every name below is a shipped literal."""
import sys, re; sys.path.insert(0,'.')
import d4b_dis as D
import d8_lib as B
lines = B.bounded(0x00046e80, 300)
print('\n'.join('  '+l for l in lines))
print()
print('--- literal string operands referenced in the body ---')
for l in lines:
    for m in re.finditer(r'0x1[0-9a-f]{7}', l):
        t = int(m.group(0),16) - D.pe.image_base
        try:
            s = D.pe.cstr(t)
        except Exception:
            continue
        if s.isprintable() and 0 < len(s) < 40:
            print(f'  {l.split()[0]}  {m.group(0)} -> "{s}"')
