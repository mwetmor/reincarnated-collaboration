"""STEP — cross-reference scanner over Game.dll .text.
Finds (a) direct `call rel32` sites to a target RVA, (b) `push imm32` of an absolute VA
(covers both function-pointer uses and string-literal references)."""
import sys, struct, re; sys.path.insert(0,'.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base
TEXT = next(s for s in pe.sections if s['name'] == '.text')
code = pe.raw[TEXT['raddr']: TEXT['raddr'] + TEXT['rsize']]
BASE = TEXT['vaddr']

def call_xrefs(target_rva):
    out = []
    for m in re.finditer(b'\xe8', code):
        off = m.start()
        if off + 5 > len(code): continue
        rel = struct.unpack_from('<i', code, off + 1)[0]
        src = BASE + off
        if src + 5 + rel == target_rva: out.append(src)
    return out

def push_xrefs(target_rva):
    va = IB + target_rva
    pat = b'\x68' + struct.pack('<I', va)
    return [BASE + m.start() for m in re.finditer(re.escape(pat), code)]

def data_xrefs(target_rva):
    """any 4-byte little-endian occurrence of the absolute VA inside .text (mov/lea/cmp forms)."""
    va = struct.pack('<I', IB + target_rva)
    return [BASE + m.start() for m in re.finditer(re.escape(va), code)]

if __name__ == '__main__':
    t = int(sys.argv[1], 16)
    print(f'target RVA {t:#010x} = {D.nearest(t)}')
    c = call_xrefs(t); print(f'  call xrefs : {len(c)}')
    for x in c[:40]: print(f'    {x:#010x}  in {D.nearest(x)}')
    p = push_xrefs(t); print(f'  push imm32 : {len(p)}')
    for x in p[:40]: print(f'    {x:#010x}  in {D.nearest(x)}')
