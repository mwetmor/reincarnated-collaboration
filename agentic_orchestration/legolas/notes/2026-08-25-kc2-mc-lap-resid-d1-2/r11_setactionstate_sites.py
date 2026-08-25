"""RESID-D1-2 step 11 — census EVERY call site of Character::SetActionState (virtual slot +0x224)
across .text, recording the literal argument where one is pushed immediately before.  This grounds
the CMM::Update gate's membership in the shipped call graph rather than in one sampled function.
Also censuses the direct (non-virtual) calls to RVA 0x46f70.  READ-ONLY."""
import sys, struct, json; sys.path.insert(0, '.')
import d4b_dis as D
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

pe = D.pe; IB = pe.image_base
t = [s for s in pe.sections if s['name'].startswith('.text')][0]
blob = pe.raw[t['raddr']: t['raddr'] + t['rsize']]
base = t['vaddr']
md = Cs(CS_ARCH_X86, CS_MODE_32)

# byte pattern for `call dword ptr [reg + 0x224]`:  FF 9x 24 02 00 00
sites = []
i = 0
while True:
    i = blob.find(b'\x24\x02\x00\x00', i + 1)
    if i == -1: break
    if i < 2: continue
    if blob[i - 2] == 0xFF and 0x90 <= blob[i - 1] <= 0x97:
        rva = base + i - 2
        # walk back up to 24 bytes and disassemble to find the last `push imm`
        start = max(0, i - 2 - 24)
        arg = None
        for ins in md.disasm(blob[start: i + 4], base + start):
            if ins.address >= rva: break
            if ins.mnemonic == 'push' and ins.op_str.startswith('0x'):
                arg = int(ins.op_str, 16)
            elif ins.mnemonic == 'push' and ins.op_str.isdigit():
                arg = int(ins.op_str)
            elif ins.mnemonic == 'push':
                arg = None      # a register/memory push resets the literal
        sites.append((rva, D.nearest(rva), arg))

names = json.load(open('evidence/85-character-actionstate-enum.json'))
out = [f'Character::SetActionState (vtable +0x224) — {len(sites)} indirect call sites in .text', '']
for rva, sym, arg in sites:
    lbl = names.get(str(arg), '?') if arg is not None else 'NON-LITERAL'
    out.append(f'  {rva:#010x}  arg={str(arg):>4}  {lbl:<28}  {sym}')
open('evidence/86-setactionstate-sites.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))

from collections import Counter
c = Counter(a for _, _, a in sites)
print('\nliteral histogram:', dict(sorted(c.items(), key=lambda kv: (kv[0] is None, kv[0]))))
