"""D-11 step 3 — byte-exact-ish scan of .text for ANY instruction whose operand string
mentions a given struct displacement (read OR write), attributed to nearest export.
Linear sweep from every exported entry keeps the decode in phase (D-10 convention). READ-ONLY."""
import sys; sys.path.insert(0,'.')
import d4b_dis as D
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
pe=D.pe
md=Cs(CS_ARCH_X86, CS_MODE_32)
want=[int(a,0) for a in sys.argv[1:]]
hits={w:{} for w in want}
for ep in D.SORTED_RVA:
    code=pe.at(ep,0x900)
    if not code: continue
    for ins in md.disasm(code, D.IB+ep):
        ops=ins.op_str
        for w in want:
            if f'+ {w:#x}]' in ops:
                r=ins.address-D.IB
                hits[w][r]=(f'{ins.mnemonic} {ops}', D.nearest(r))
for w in want:
    print(f'=== [reg+{w:#x}]  ({len(hits[w])} distinct sites)')
    for r in sorted(hits[w]):
        s,nm=hits[w][r]
        print(f'   {r:#010x}  {s:52s}  in {nm}')
    print()
