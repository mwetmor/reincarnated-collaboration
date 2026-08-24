"""D-4c STEP 6 — locate the `Global` / `XOR` field strings in Game.dll and the code that reads them,
so D-4b Q4 is answered from the binary rather than from the (silent) schema. READ-ONLY."""
import sys, re, struct; sys.path.insert(0, '.')
import d4b_dis as D
import d4b_xref as X
pe = D.pe; IB = pe.image_base

def find_str(needle):
    out = []
    nb = needle.encode()
    for s in pe.sections:
        if s['name'] not in ('.rdata', '.data'): continue
        blob = pe.raw[s['raddr']: s['raddr'] + s['rsize']]
        for m in re.finditer(re.escape(nb + b'\0'), blob):
            rva = s['vaddr'] + m.start()
            # must be a string START (preceded by NUL)
            if m.start() and blob[m.start()-1] != 0: continue
            out.append(rva)
    return out

for needle in ('offensiveSlowPoisonXOR', 'offensiveSlowPoisonGlobal', 'XOR', 'Global',
               'offensiveSlowPoisonMin'):
    hits = find_str(needle)
    print(f'--- {needle!r}: {len(hits)} string(s)')
    for rva in hits[:6]:
        xr = X.push_xrefs(rva) + X.data_xrefs(rva)
        xr = sorted(set(xr))
        print(f'    rva={rva:#010x}  xrefs={len(xr)}  ' +
              ', '.join(f'{a:#010x} in {D.nearest(a)}' for a in xr[:4]))
