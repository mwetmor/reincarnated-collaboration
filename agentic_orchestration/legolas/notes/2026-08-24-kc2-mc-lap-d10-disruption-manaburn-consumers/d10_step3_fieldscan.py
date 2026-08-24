"""D-10 step 3 — byte-exact scan of .text for instructions that WRITE a given struct offset
(`mov byte/dword ptr [reg+disp8/disp32], ...`), attributed to the nearest exported symbol.
Used to find which loader populates a flag byte, so the flag's DBR field name can be read out of
the neighbouring `GetBool("...")` call rather than guessed.  READ-ONLY."""
import sys, struct; sys.path.insert(0, '.')
import d4b_dis as D
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

pe = D.pe
text = [s for s in pe.sections if s['name'].startswith('.text')][0]
base_off, base_rva, size = text['raddr'], text['vaddr'], text['rsize']
md = Cs(CS_ARCH_X86, CS_MODE_32)

want = [int(a, 0) for a in sys.argv[1:]]
# Linear sweep from every exported entry point keeps the decode in-phase.
hits = {w: [] for w in want}
for ep in D.SORTED_RVA:
    code = pe.at(ep, 0x600)
    if not code:
        continue
    for ins in md.disasm(code, D.IB + ep):
        if ins.mnemonic != 'mov':
            continue
        for w in want:
            for form in (f'+ {w:#x}]', f'+ {w}]'):
                if form in ins.op_str and ins.op_str.split(',')[0].strip().endswith(']'):
                    r = ins.address - D.IB
                    hits[w].append((r, f'{ins.mnemonic} {ins.op_str}', D.nearest(r)))
for w in want:
    seen = set()
    print(f'=== writes to [reg+{w:#x}]  ({len(hits[w])} raw)')
    for r, s, nm in sorted(hits[w]):
        if r in seen:
            continue
        seen.add(r)
        print(f'   {r:#010x}  {s:44s}  in {nm}')
