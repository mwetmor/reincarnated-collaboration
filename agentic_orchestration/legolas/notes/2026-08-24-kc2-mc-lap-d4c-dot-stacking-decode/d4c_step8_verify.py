"""D-4c STEP 8 — machine-checked verification of every load-bearing claim in the README.
Each check prints PASS/FAIL against bytes read from Game.dll / database.arz. READ-ONLY."""
import sys, struct, re; sys.path.insert(0, '.')
import d4b_dis as D
from d4b_lib import ArzArchive, VENDOR_FULL, VENDOR_E3
pe = D.pe; IB = pe.image_base
ok = lambda c: 'PASS' if c else '**FAIL**'

def bytes_at(rva, n): return pe.at(rva, n)
def f32(rva): return struct.unpack('<f', pe.at(rva, 4))[0]

print('=== V1  bit-exact constants on the DoT path ===')
# bit-exact means BYTES: compare against the IEEE-754 float32 encoding of the intended literal,
# not against a Python double (0.1f != 0.1 as a double -- that is the point of the check).
for rva, want, label in ((0x5f58a4, 10.0, 'nTicks = duration x 10.0f'),
                         (0x5f57ac, 0.1,  'perTick = damage x 0.1f'),
                         (0x5f5780, 0.01, 'stack multiplier = table[i] x 0.01f')):
    got = pe.at(rva, 4); exp = struct.pack('<f', want)
    print(f'  [{rva:#08x}] = {got.hex()}  want float32({want}) = {exp.hex()}  '
          f'{ok(got == exp)}   {label}')

print('\n=== V2  the merge/sum instruction sites (opcode bytes, not mnemonics) ===')
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
_md = Cs(CS_ARCH_X86, CS_MODE_32)
def decode1(rva):
    for ins in _md.disasm(pe.at(rva, 16), IB + rva):
        return f'{ins.mnemonic} {ins.op_str}'
SITES = [
    (0x20d822, 'movss xmm0, dword ptr [eax]',      'read inst+0x00 (same-source path)'),
    (0x20d828, 'maxss xmm0, xmm1',                 'SAME-SOURCE = MAX on inst+0x00'),
    (0x20d82c, 'movss dword ptr [eax], xmm0',      'write back inst+0x00'),
    (0x20da60, 'addss xmm1, dword ptr [esi + 4]',  'TICK SUM is over inst+0x04'),
    (0x20d8d7, 'mulss xmm0, dword ptr [eax]',      'effective = ... x inst+0x00'),
    (0x20d8db, 'movss dword ptr [eax + 4], xmm0',  'inst+0x04 = inst+0x00 x multiplier'),
    (0x20d870, 'call 0x1020e420',                  'append path: vector::push_back(new instance)'),
    (0x20d899, 'call 0x1020ea70',                  'std::sort over the bucket'),
]
for rva, want, label in SITES:
    got = decode1(rva)
    print(f'  {rva:#010x}  {got:<32} want {want:<32} {ok(got==want)}  {label}')

print('\n=== V3  sort comparator key + direction ===')
# insertion sort inner: comiss xmm0,[eax-0x18] / jb  -> shift while prev < val  => DESCENDING on +0x00
for rva, hexwant, label in ((0x20ef9c, '0f2f0f',   'comiss xmm1,[edi]      compares offset +0x00'),
                            (0x20effa, '0f2fc1',   'comiss xmm0,xmm1'),
                            (0x20effd, '72e1',     'jb  -> shift while prev < val  => DESCENDING')):
    got = pe.at(rva, len(hexwant)//2).hex()
    print(f'  {rva:#010x}  {got:<8} want {hexwant:<8} {ok(got==hexwant)}  {label}')

print('\n=== V4  the stack-ordinal multiplier TABLE (gGameEngine+0x292d4) ===')
# name string pushed by GameEngine::LoadFromDatabase @0x2579f9
pushed = struct.unpack_from('<I', pe.raw, pe.rva2off(0x2579f9) + 1)[0]
nm = pe.cstr(pushed - IB)
print(f'  loader @0x002579f9 pushes {pushed:#010x} -> {nm!r}   {ok(nm=="damageMagnitude")}')
lea = pe.at(0x2579f2, 6).hex()
print(f'  loader @0x002579f2 lea eax,[edi+0x292d4] bytes={lea}  {ok(lea=="8d87d4920200")}')
TYPES = {0: 'int', 1: 'real', 2: 'string', 3: 'bool'}
import lz4.block
for tag, root in (('FULL v1.2.3.4', VENDOR_FULL), ('ED-III', VENDOR_E3)):
    a = ArzArchive(root / 'database' / 'database.arz')
    m = a.records['records/game/gameengine.dbr']
    dec = lz4.block.decompress(a.raw[24+m['data_offset']: 24+m['data_offset']+m['comp_size']],
                               uncompressed_size=m['decomp_size'])
    pos = 0
    while pos + 8 <= len(dec):
        typ, cnt, nid = struct.unpack_from('<HHi', dec, pos); pos += 8
        vals = struct.unpack_from(f'<{cnt}I', dec, pos); pos += 4*cnt
        if a.strings[nid] == 'damageMagnitude':
            fv = [struct.unpack('<f', struct.pack('<I', x))[0] for x in vals]
            print(f'  [{tag}] type={TYPES[typ]} COUNT={cnt} values={fv}   '
                  f'{ok(cnt==1 and fv==[100.0])}  -> multiplier for EVERY ordinal = '
                  f'{fv[min(0,cnt-1)]*0.01}')
            break

print('\n=== V5  CAP SCAN — is any instance COUNT limited anywhere on the apply/tick path? ===')
# Enumerate every cmp/test against an immediate inside the six functions that touch the
# instance vector, and classify. A cap would appear as a compare of a computed COUNT.
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
md = Cs(CS_ARCH_X86, CS_MODE_32)
FUNCS = {'insert/merge 0x20d6b0': (0x20d6b0, 0x20d930),
         'sort           0x20ea70': (0x20ea70, 0x20eb70),
         'insertion sort 0x20ef70': (0x20ef70, 0x20f015),
         'tick sum       0x20da10': (0x20da10, 0x20dbc0),
         'EndAttack      0x20d940': (0x20d940, 0x20da07),
         'bucket retire  0x20dc80': (0x20dc80, 0x20dd50)}
ALLOC_GUARD = {0x3fffffff, 0xaaaaaaa, 0x1000, 0x23, 0x1f, 0x2aaaaaab}
for lbl, (a, b) in FUNCS.items():
    imms = []
    for ins in md.disasm(pe.at(a, b-a), IB+a):
        if ins.mnemonic in ('cmp', 'test') and re.search(r',\s*(-?\d+|0x[0-9a-f]+)$', ins.op_str):
            v = int(ins.op_str.rsplit(',', 1)[1].strip(), 0)
            if v not in (0, 1, 2, 4, 8) and v not in ALLOC_GUARD:
                imms.append((ins.address-IB, ins.mnemonic, ins.op_str))
    print(f'  {lbl}: non-trivial immediate compares = {len(imms)}')
    for r, m_, o in imms: print(f'      {r:#010x}  {m_} {o}')
print('  (0x20 in std::sort = MSVC introsort insertion-sort threshold, not a game cap;'
      ' 0x3fffffff/0xaaaaaaa/0x1000/0x23/0x1f = allocator max_size + small-block guards)')
