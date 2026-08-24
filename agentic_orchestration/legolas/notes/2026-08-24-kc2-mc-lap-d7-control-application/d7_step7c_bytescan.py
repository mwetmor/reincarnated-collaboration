"""D-7 step 7c — byte-level scan for the CalculateStun vtable slot.  A linear capstone sweep
desyncs on interleaved data, so match the ENCODINGS directly:
    call dword ptr [reg+disp32]   = FF /2  -> FF 90..97 (mod=10) + disp32
    mov  reg,  dword ptr [reg+d32]= 8B /r  (mod=10)      + disp32
Every hit is then re-disassembled from a short backward window and attributed to the nearest
exported symbol.  READ-ONLY."""
import sys, struct, re; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
md = Cs(CS_ARCH_X86, CS_MODE_32)

DISP = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x478
d = struct.pack('<i', DISP)
sec = [s for s in pe.sections if s['name'].startswith('.text')][0]
blob = pe.raw[sec['raddr']: sec['raddr'] + sec['rsize']]

pats = []
for modrm in range(0x90, 0x98):          # call [reg+disp32]
    if modrm == 0x94: continue           # SIB form, skip
    pats.append((b'\xff' + bytes([modrm]) + d, 'call'))
for modrm in range(0x80, 0x100):         # mov r32,[reg+disp32], mod=10
    if (modrm >> 6) != 2: continue
    if (modrm & 7) == 4: continue        # SIB
    pats.append((b'\x8b' + bytes([modrm]) + d, 'mov'))

seen = {}
for p, kind in pats:
    for m in re.finditer(re.escape(p), blob):
        rva = sec['vaddr'] + m.start()
        seen[rva] = kind
print(f'# encoding hits for disp {DISP:#x}: {len(seen)}')
for rva in sorted(seen):
    ins = next(md.disasm(blob[rva - sec['vaddr']: rva - sec['vaddr'] + 8], IB + rva), None)
    print(f'  {rva:#010x}  {seen[rva]:4s} {ins.mnemonic if ins else "?":6s} '
          f'{ins.op_str if ins else "":34s} in {D.nearest(rva)}')
