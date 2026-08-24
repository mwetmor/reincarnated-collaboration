"""D-7 step 7 — find every call site of the CalculateStun virtual slot (vtable offset 0x478),
attributed to the NEAREST EXPORTED SYMBOL, so the four float arguments can be named. READ-ONLY."""
import sys, re; sys.path.insert(0, '.')
import d4b_dis as D
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
pe = D.pe; IB = pe.image_base
md = Cs(CS_ARCH_X86, CS_MODE_32)

OFF = sys.argv[1] if len(sys.argv) > 1 else '0x478'
sec = [s for s in pe.sections if s['name'].startswith('.text')][0]
code = pe.raw[sec['raddr']: sec['raddr'] + sec['rsize']]
pat = re.compile(r'^dword ptr \[e[a-z]{2} \+ ' + OFF + r'\]$')
hits = []
for ins in md.disasm(code, IB + sec['vaddr']):
    if ins.mnemonic == 'call' and pat.match(ins.op_str):
        r = ins.address - IB
        hits.append((r, D.nearest(r)))
print(f'# call [reg+{OFF}] sites: {len(hits)}')
for r, s in hits:
    print(f'  {r:#010x}  in {s}')
