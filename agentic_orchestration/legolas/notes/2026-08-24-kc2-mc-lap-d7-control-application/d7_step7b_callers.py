"""D-7 step 7b — the vtable slot is loaded then called (`mov eax,[eax+0x478]; call eax`),
not called in place.  Scan for the LOAD of offset 0x478 out of a vtable pointer. READ-ONLY."""
import sys, re; sys.path.insert(0, '.')
import d4b_dis as D
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
pe = D.pe; IB = pe.image_base
md = Cs(CS_ARCH_X86, CS_MODE_32)

OFF = sys.argv[1] if len(sys.argv) > 1 else '0x478'
sec = [s for s in pe.sections if s['name'].startswith('.text')][0]
code = pe.raw[sec['raddr']: sec['raddr'] + sec['rsize']]
pat = re.compile(r'^e[a-z]{2}, dword ptr \[e[a-z]{2} \+ ' + OFF + r'\]$')
hits = []
for ins in md.disasm(code, IB + sec['vaddr']):
    if ins.mnemonic == 'mov' and pat.match(ins.op_str):
        r = ins.address - IB
        hits.append((r, ins.op_str, D.nearest(r)))
print(f'# mov reg,[reg+{OFF}] sites: {len(hits)}')
for r, o, s in hits:
    print(f'  {r:#010x}  {o:34s} in {s}')
