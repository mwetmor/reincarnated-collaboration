"""D-4c STEP 4 — locate the vtable(s) holding the insert/merge (0x20d6b0) and per-tick-sum
(0x20da10) slots, so their `this` layouts can be attributed to a NAMED class rather than assumed
to be the same object. READ-ONLY."""
import sys, struct, re; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base

def find_vptr(target_rva):
    """Every 4-byte LE occurrence of VA(target) anywhere in the image, with section + nearby syms."""
    va = struct.pack('<I', IB + target_rva); out = []
    for s in pe.sections:
        blob = pe.raw[s['raddr']: s['raddr'] + s['rsize']]
        for m in re.finditer(re.escape(va), blob):
            out.append((s['name'], s['vaddr'] + m.start()))
    return out

for t in (0x20d6b0, 0x20da10):
    print(f'=== references to {t:#010x} ===')
    for sec, rva in find_vptr(t):
        print(f'  {sec:8s} rva={rva:#010x}  sym={D.sym(rva)}  nearest={D.nearest(rva) if sec=="_ text" else ""}')
        if sec == '.rdata':
            # dump the surrounding slot window
            for k in range(-3, 9):
                a = rva + 4*k
                v = struct.unpack_from('<I', pe.raw, pe.rva2off(a))[0]
                nm = D.nearest(v - IB) if v > IB else ''
                mark = ' <<<' if k == 0 else ''
                print(f'      slot[{k:+d}] @{a:#010x} = {v:#010x}  {nm}{mark}')
    print()

# what symbol owns each vtable address?
print('=== exported ??_7 vftable symbols near DurationDamage ===')
for n, r in sorted(D.EX.items(), key=lambda kv: kv[1]):
    if n.startswith('??_7') and ('DurationDamage' in n or 'DurationDam' in n):
        print(f'  {r:#010x}  {n}')
