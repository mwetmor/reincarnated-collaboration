"""RESID-D1-2 step 14 — resolve the *Action classes whose out-of-line ctor did not carry a literal
type, by finding every .text site that installs the class' vtable and reading the nearest following
`[reg+8] = <literal>`.  Needed because MoveAttackAction sets ActionState 20, which IS a member of
the CharacterMovementManager::Update gate: if the alert's PlayAnimationAction were REJECTED over it
the immobility claim would have a hole.  READ-ONLY."""
import sys, struct, re; sys.path.insert(0, '.')
import d4b_dis as D
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

pe = D.pe; IB = pe.image_base
t = [s for s in pe.sections if s['name'].startswith('.text')][0]
blob = pe.raw[t['raddr']: t['raddr'] + t['rsize']]; base = t['vaddr']
md = Cs(CS_ARCH_X86, CS_MODE_32)

WANT = ['MoveAttackAction', 'JumpAttackAction', 'EvadeAction', 'RotateAction',
        'MoveToAction', 'PlayAnimationAction', 'WalkAction', 'SpawnAction', 'EngageNpcAction']
out = []
for cls in WANT:
    key = f'??_7{cls}@GAME@@6B@'
    if key not in D.EX:
        out.append(f'{cls}: NO VTABLE SYMBOL'); continue
    v = D.EX[key] + IB
    needle = struct.pack('<I', v)
    types = {}
    i = blob.find(needle)
    while i != -1:
        # the vtable pointer appears as an immediate in `mov dword ptr [reg], imm32`
        if i >= 2 and blob[i - 2] == 0xC7:
            site = base + i - 2
            for ins in md.disasm(blob[i - 2: i + 4 + 64], site):
                m = re.match(r'dword ptr \[\w+ \+ 8\], (0x[0-9a-f]+|\d+)$', ins.op_str)
                if ins.mnemonic == 'mov' and m:
                    types.setdefault(int(m.group(1), 0), []).append(f'{site:#010x} {D.nearest(site)}')
                    break
        i = blob.find(needle, i + 1)
    out.append(f'{cls}: vtable {v:#010x} -> types ' +
               (', '.join(f'{k} (from {len(vv)} site(s): {vv[0]})' for k, vv in sorted(types.items()))
                if types else 'NONE FOUND'))
open('evidence/96-missing-action-types.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
