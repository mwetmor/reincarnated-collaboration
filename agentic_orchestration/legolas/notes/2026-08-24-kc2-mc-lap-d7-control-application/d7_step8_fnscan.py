"""D-7 step 8 — disassemble EVERY exported function body (not a linear sweep, which desyncs on
interleaved data) and record every indirect call whose vtable displacement matches a target set.
Handles both emitted shapes:
    (a) call dword ptr [reg + disp]
    (b) mov reg, dword ptr [reg + disp] ; ... ; call reg
READ-ONLY."""
import sys, re, collections; sys.path.insert(0, '.')
import d4b_dis as D
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
pe = D.pe; IB = pe.image_base
md = Cs(CS_ARCH_X86, CS_MODE_32)

DISPS = {int(x, 0) for x in (sys.argv[1:] or ['0x478'])}
text = [s for s in pe.sections if s['name'].startswith('.text')][0]
lo, hi = text['vaddr'], text['vaddr'] + text['rsize']

starts = sorted({r for r in D.EX.values() if lo <= r < hi})
print(f'# {len(starts)} distinct exported code entry points; disps={[hex(d) for d in DISPS]}')

hits = []
callre = re.compile(r'^dword ptr \[(e[a-z]{2}) \+ (0x[0-9a-f]+)\]$')
movre = re.compile(r'^(e[a-z]{2}), dword ptr \[(e[a-z]{2}) \+ (0x[0-9a-f]+)\]$')
for i, st in enumerate(starts):
    end = starts[i + 1] if i + 1 < len(starts) else hi
    n = min(end - st, 0x3000)
    blob = pe.raw[text['raddr'] + (st - text['vaddr']): text['raddr'] + (st - text['vaddr']) + n]
    pend = {}
    for ins in md.disasm(blob, IB + st):
        r = ins.address - IB
        if ins.mnemonic == 'call':
            m = callre.match(ins.op_str)
            if m and int(m.group(2), 16) in DISPS:
                hits.append((r, 'direct-indirect', ins.op_str))
            elif ins.op_str in pend:
                hits.append((r, 'loaded', f'{ins.op_str} <- {pend[ins.op_str]}'))
        m2 = movre.match(ins.op_str) if ins.mnemonic == 'mov' else None
        if m2 and int(m2.group(3), 16) in DISPS:
            pend[m2.group(1)] = f'[{m2.group(2)}+{m2.group(3)}]@{r:#x}'
        elif ins.mnemonic in ('mov', 'lea', 'pop', 'xor', 'add') and ins.op_str.split(',')[0] in pend and not m2:
            pend.pop(ins.op_str.split(',')[0], None)

print(f'# hits: {len(hits)}')
for r, kind, det in hits:
    print(f'  {r:#010x}  {kind:16s} {det:44s} in {D.nearest(r)}')
