"""D-4c STEP 7 — find the vtable slot of DamageAttribute*::AddDamageToAccumulator and the caller
that drives the `global` bool (arg5) + any XOR selection. READ-ONLY."""
import sys, struct, re; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base

TARGETS = {0x1425b0: 'DamageAttributeDur', 0x140240: 'DamageAttributeAbs'}
for t, lbl in TARGETS.items():
    va = struct.pack('<I', IB + t)
    for s in pe.sections:
        if s['name'] != '.rdata': continue
        blob = pe.raw[s['raddr']: s['raddr'] + s['rsize']]
        for m in re.finditer(re.escape(va), blob):
            rva = s['vaddr'] + m.start()
            # walk back to the vftable start: the nearest exported ??_7 symbol at or below
            best = None
            for n, r in D.EX.items():
                if n.startswith('??_7') and r <= rva and (best is None or r > best[1]):
                    best = (n, r)
            if best and (rva - best[1]) // 4 < 80:
                print(f'{lbl}: fn@{t:#x} at vtable slot {(rva-best[1])//4}  of  {best[0]}')
