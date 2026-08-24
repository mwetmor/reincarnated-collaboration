"""D-8 step 2 — resolve the .rdata string operands used by BeginFreeze / BeginPetrify, and
disassemble the two helper bodies the Begin* prologue shares.  READ-ONLY."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base

print('=== string operands ===')
for va in (0x104f5594, 0x104f55cc, 0x104f55e0, 0x104f5618, 0x104c0228):
    rva = va - IB
    try:
        print(f'  {va:#010x} (rva {rva:#08x}) = {pe.cstr(rva)!r}')
    except Exception as e:
        print(f'  {va:#010x} rva {rva:#08x} : {e}  raw={pe.at(rva,32)!r}')

print()
print('=== indirect-call slot [0x104e504c] ===')
rva = 0x104e504c - IB
print('  rva', hex(rva), 'raw dword =', hex(struct.unpack_from("<I", pe.raw, pe.rva2off(rva))[0]))
# is it in the IAT?  print the import descriptor range
idir = pe.dirs[1]; iat = pe.dirs[12]
print('  import dir  rva=%#x size=%#x' % idir)
print('  IAT dir     rva=%#x size=%#x' % iat)
print('  in IAT range:', iat[0] <= rva < iat[0]+iat[1])
v = struct.unpack_from("<I", pe.raw, pe.rva2off(rva))[0]
if v & 0x80000000 == 0 and pe.rva2off(v) is not None:
    print('  hint/name ->', pe.raw[pe.rva2off(v)+2: pe.raw.index(b"\0", pe.rva2off(v)+2)].decode('latin-1'))

print()
for nm, r in (('helper@0x0000d460', 0x0000d460),):
    print(f'=== {nm} ===')
    for l in D.disasm(r, 40, stop_at_ret=False): print(l)
