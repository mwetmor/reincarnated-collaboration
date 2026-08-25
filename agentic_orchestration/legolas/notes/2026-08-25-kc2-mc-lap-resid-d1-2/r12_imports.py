"""RESID-D1-2 step 12 — resolve IAT slots to imported symbol names, so the indirect
`call dword ptr [0x104exxxx]` sites in the movement chain are named rather than described.
READ-ONLY."""
import sys, struct, json; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base

imp_rva, imp_sz = pe.dirs[1]
iat = {}
o = pe.rva2off(imp_rva)
while True:
    oft, tds, fc, name_rva, first = struct.unpack_from('<IIIII', pe.raw, o)
    if not (oft or first): break
    dll = pe.cstr(name_rva)
    lookup = oft or first
    lo = pe.rva2off(lookup)
    k = 0
    while True:
        ent = struct.unpack_from('<I', pe.raw, lo + 4 * k)[0]
        if ent == 0: break
        slot = IB + first + 4 * k
        if ent & 0x80000000:
            nm = f'{dll}#ordinal{ent & 0xFFFF}'
        else:
            ho = pe.rva2off(ent & 0x7FFFFFFF)
            e = pe.raw.index(b'\0', ho + 2)
            nm = pe.raw[ho + 2:e].decode('latin-1')
        iat[slot] = (dll, nm)
        k += 1
    o += 20

json.dump({hex(k): v for k, v in sorted(iat.items())}, open('evidence/87-iat.json', 'w'), indent=1)
print(f'IAT slots resolved: {len(iat)}')

QUERY = [0x104e5600, 0x104e57a0, 0x104e504c, 0x104e5288, 0x104e5028, 0x104e5610,
         0x104e5654, 0x104e55ec, 0x104e5760, 0x104e5388, 0x104e5514, 0x104e55f4,
         0x104e54fc, 0x104e550c, 0x104e5680, 0x104e5090, 0x104e5768]
lines = []
for q in QUERY:
    v = iat.get(q)
    lines.append(f'{q:#010x}  ' + (f'{v[0]} :: {v[1]}' if v else 'NOT AN IMPORT SLOT'))
open('evidence/88-iat-queries.txt', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
