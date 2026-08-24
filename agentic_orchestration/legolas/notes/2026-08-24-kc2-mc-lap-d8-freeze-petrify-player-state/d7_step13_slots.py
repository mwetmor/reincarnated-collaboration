"""D-7 step 13 — resolve named vtable slots.  Usage: d7_step13_slots.py <vftable-symbol> <off>...
Every slot is printed with the symbol it actually holds, so a call site's `[eax+0x3c8]` becomes a
NAMED function rather than an offset.  READ-ONLY."""
import sys, struct; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base

vt = sys.argv[1]
base = D.EX[vt] if not vt.startswith('0x') else int(vt, 16)
print(f'=== {vt} @ {base:#010x}')
for a in sys.argv[2:]:
    off = int(a, 0)
    v = struct.unpack_from('<I', pe.raw, pe.rva2off(base + off))[0]
    tgt = v - IB
    body = ''
    try:
        body = ' | '.join(x.split('  ', 3)[-1].strip() for x in D.disasm(tgt, 4)[:4])
    except Exception:
        pass
    print(f'  +{off:#05x} (slot {off//4:3d}) -> {tgt:#010x}  {D.nearest(tgt)}')
    if body: print(f'        body: {body}')
