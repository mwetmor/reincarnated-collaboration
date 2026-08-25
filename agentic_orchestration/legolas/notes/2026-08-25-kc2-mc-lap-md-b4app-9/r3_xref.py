"""D-7 step 9 — direct-call xref index.  Scan .text for E8 rel32 / E9 rel32 whose target is one of
the named control entry points.  Byte-exact, so it cannot be missed by disassembly desync.
Each hit is attributed to the nearest exported symbol.  READ-ONLY."""
import sys, struct; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base
text = [s for s in pe.sections if s['name'].startswith('.text')][0]
base_off, base_rva, size = text['raddr'], text['vaddr'], text['rsize']
blob = pe.raw[base_off: base_off + size]

def xrefs(target_rva):
    out = []
    for i in range(0, len(blob) - 5):
        op = blob[i]
        if op != 0xE8 and op != 0xE9: continue
        rel = struct.unpack_from('<i', blob, i + 1)[0]
        if base_rva + i + 5 + rel == target_rva:
            out.append((base_rva + i, 'call' if op == 0xE8 else 'jmp'))
    return out

names = sys.argv[1:]
for nm in names:
    rva = D.EX[nm] if not nm.startswith('0x') else int(nm, 16)
    print(f'=== xrefs to {nm} @ {rva:#010x}')
    for r, k in xrefs(rva):
        print(f'   {k} @ {r:#010x}  in {D.nearest(r)}')
    print()
