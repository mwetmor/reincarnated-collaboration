"""RESID-D1-2 step 10 — decode the Character_ActionState enum by name, from the shipped jump table
of Character::GetActionStateAsText (static overload, RVA 0x46fd0).  Each case pushes one .rdata
string literal; the table index IS the enum value.  READ-ONLY."""
import sys, struct, json; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base

TBL = 0x100471a8 - IB
N = 0x16                       # `cmp eax,0x15 / ja default` at 0x46fdf -> 0..0x15 inclusive
names = {}
for i in range(N):
    tgt = struct.unpack_from('<I', pe.at(TBL + 4 * i, 4), 0)[0] - IB
    # each case body is: mov ecx,[ebp+8] ; push <str> ; call <string-assign>
    code = pe.at(tgt, 16)
    # find the `push imm32` (0x68) in the first bytes
    j = code.index(0x68)
    s_rva = struct.unpack_from('<I', code, j + 1)[0] - IB
    names[i] = (pe.cstr(s_rva), f'{tgt:#010x}', f'{s_rva + IB:#010x}')

MOVEMENT_GATE = {5, 6, 0x13, 0x14, 0x15}   # CharacterMovementManager::Update, RVA 0x781a0
out = ['Character_ActionState — decoded from Character::GetActionStateAsText jump table @ '
       f'{TBL + IB:#010x} ({N} entries)', '',
       'val hex  name                          in CMM::Update gate?']
for i in range(N):
    nm, tgt, s = names[i]
    out.append(f'{i:3d} 0x{i:02x}  {nm:<28}  {"YES" if i in MOVEMENT_GATE else "-"}   (case {tgt}, str {s})')
out += ['', 'CharacterMovementManager::Update (RVA 0x781a0) runs its body IFF '
        'Character::GetActionState() is one of: ' + ', '.join(f'{v}={names[v][0]}' for v in sorted(MOVEMENT_GATE))]
open('evidence/85-character-actionstate-enum.txt', 'w').write('\n'.join(out) + '\n')
json.dump({str(k): v[0] for k, v in names.items()},
          open('evidence/85-character-actionstate-enum.json', 'w'), indent=1)
print('\n'.join(out))
