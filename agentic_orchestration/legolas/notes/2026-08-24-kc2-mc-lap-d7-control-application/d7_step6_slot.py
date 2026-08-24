"""D-7 step 6 — locate the vtable slot that holds CalculateStun, so the CALLER can be found
by its indirect-call offset rather than guessed.  READ-ONLY."""
import sys, struct, re; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base

VT = {n: D.EX[n] for n in D.EX if n.startswith('??_7') and
      n in ('??_7Character@GAME@@6B@', '??_7Player@GAME@@6B@', '??_7Monster@GAME@@6B@')}
print('vtable roots:', {k: hex(v) for k, v in VT.items()})

TARGETS = {0x00054110: 'CalculateStun@Character',
           0x0031ee20: 'CalculateStun@Player',
           0x002d5170: 'CalculateStun@Monster'}

for t, nm in TARGETS.items():
    va = struct.pack('<I', IB + t)
    for s in pe.sections:
        if s['name'] != '.rdata': continue
        blob = pe.raw[s['raddr']: s['raddr'] + s['rsize']]
        for m in re.finditer(re.escape(va), blob):
            rva = s['vaddr'] + m.start()
            owner = None
            for k, v in VT.items():
                if v <= rva < v + 0x900:
                    owner = (k, (rva - v) // 4, rva - v)
            print(f'{nm:26s} slot @ {rva:#010x}  owner={owner}')
