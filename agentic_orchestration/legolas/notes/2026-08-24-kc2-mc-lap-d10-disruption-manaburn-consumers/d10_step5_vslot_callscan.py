"""D-10 step 5 — byte-exact scan of .text for INDIRECT CALLS through a given vtable displacement
(`FF /2 disp8|disp32`), attributed to the nearest exported symbol.  D-7's step-7c technique, reused
because a virtual call site cannot be found by an E8 xref.  READ-ONLY."""
import sys, struct; sys.path.insert(0, '.')
import d4b_dis as D

pe = D.pe
text = [s for s in pe.sections if s['name'].startswith('.text')][0]
base_off, base_rva, size = text['raddr'], text['vaddr'], text['rsize']
blob = pe.raw[base_off: base_off + size]

# FF /2 = call r/m32.  modrm.reg == 2.  mod 01 => disp8, mod 10 => disp32.
for a in sys.argv[1:]:
    disp = int(a, 0)
    print(f'=== indirect calls through [reg+{disp:#x}]')
    n = 0
    for i in range(len(blob) - 7):
        if blob[i] != 0xFF:
            continue
        modrm = blob[i + 1]
        if ((modrm >> 3) & 7) != 2:
            continue
        mod = modrm >> 6
        rm = modrm & 7
        j = i + 2
        if rm == 4:            # SIB present
            j += 1
        if mod == 1:
            d = struct.unpack_from('<b', blob, j)[0]
        elif mod == 2:
            d = struct.unpack_from('<i', blob, j)[0]
        else:
            continue
        if d != disp:
            continue
        r = base_rva + i
        n += 1
        print(f'   {r:#010x}  in {D.nearest(r)}')
    print(f'   ({n} sites)\n')
