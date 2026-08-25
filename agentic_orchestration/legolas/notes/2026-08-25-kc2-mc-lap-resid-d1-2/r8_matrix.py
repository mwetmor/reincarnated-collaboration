"""RESID-D1-2 step 8 — reconstruct GameEngine::InitializeActionMatrix's 26x26
CharacterActionPermission table byte-exactly from the shipped .text, then read the cells the lap
needs.  READ-ONLY.  Every store form that appears in the listing is handled; any store form NOT
handled HALTS the script rather than being skipped (a skipped store would silently leave a default
in a cell the game overrides)."""
import sys, struct, json, re; sys.path.insert(0, '.')
import d4b_dis as D, d8_lib as L

BASE = 0x2802c
N = 26
pe = D.pe

# the xmm broadcast source
xmm_src = 0x105f59b0 - pe.image_base
xmm_bytes = pe.at(xmm_src, 16)
xmm_words = list(struct.unpack('<4I', xmm_bytes))
print(f'xmm const @ {0x105f59b0:#x} = {xmm_words}')

rva = D.EX['?InitializeActionMatrix@GameEngine@GAME@@IAEXXZ']
lines = L.bounded(rva, 4000)

cells = {}
eax = None
xmm0 = None          # tracked; HALTs if a store reads it before it is defined
covered = set()
unhandled = []

re_mov_imm = re.compile(r'mov\s+dword ptr \[esi \+ (0x[0-9a-f]+)\], (0x[0-9a-f]+|\d+)$')
re_mov_eax = re.compile(r'mov\s+dword ptr \[esi \+ (0x[0-9a-f]+)\], eax$')
re_movups  = re.compile(r'movups\s+xmmword ptr \[esi \+ (0x[0-9a-f]+)\], xmm0$')
re_movq    = re.compile(r'movq\s+qword ptr \[esi \+ (0x[0-9a-f]+)\], xmm0$')
re_seteax  = re.compile(r'mov\s+eax, (0x[0-9a-f]+|\d+)$')
re_stos    = re.compile(r'rep stosd')
re_movaps  = re.compile(r'movaps\s+xmm0, xmmword ptr \[(0x[0-9a-f]+)\]$')
re_xorps   = re.compile(r'xorps\s+xmm0, xmm0$')

for ln in lines:
    txt = ln.split(None, 1)[1].strip()
    txt = txt.split('   ;')[0]          # strip the harness annotation FIRST
    txt = re.sub(r'\s+', ' ', txt).strip()
    m = re_seteax.match(txt)
    if m:
        eax = int(m.group(1), 0); continue
    if re_stos.search(txt):
        # rep stosd  ecx=0x2a4 dwords from edi = esi+0x2802c, value eax
        assert eax == 2, eax
        for i in range(0x2a4):
            cells[BASE + 4 * i] = eax
        covered.add('stosd')
        continue
    m = re_mov_imm.match(txt)
    if m:
        cells[int(m.group(1), 0)] = int(m.group(2), 0); continue
    m = re_mov_eax.match(txt)
    if m:
        assert eax is not None
        cells[int(m.group(1), 0)] = eax; continue
    m = re_movups.match(txt)
    if m:
        off = int(m.group(1), 0)
        assert xmm0 is not None, f'movups before xmm0 defined: {txt}'
        for k in range(4): cells[off + 4 * k] = xmm0[k]
        continue
    m = re_movq.match(txt)
    if m:
        off = int(m.group(1), 0)
        assert xmm0 is not None, f'movq before xmm0 defined: {txt}'
        for k in range(2): cells[off + 4 * k] = xmm0[k]
        continue
    m = re_movaps.match(txt)
    if m:
        src = int(m.group(1), 0) - pe.image_base
        b = pe.at(src, 16)
        assert b and len(b) == 16, f'movaps source unreadable: {txt}'
        xmm0 = list(struct.unpack('<4I', b)); continue
    if re_xorps.match(txt):
        xmm0 = [0, 0, 0, 0]; continue
    if txt.split()[0] in ('push', 'pop', 'ret', 'int3', 'mov', 'lea', 'nop'):
        # 'mov' here is only the ecx/esi/edi setup lines; assert that is all it is
        if txt.startswith('mov dword ptr') or txt.startswith('mov qword'):
            unhandled.append(txt)
        continue
    unhandled.append(txt)

assert not unhandled, f'UNHANDLED STORE FORMS (HALT): {unhandled[:10]}'
assert 'stosd' in covered, 'the rep stosd default fill was not seen'

# every cell of the 26x26 must be present
grid = [[None] * N for _ in range(N)]
missing = []
for nt in range(N):
    for ct in range(N):
        off = BASE + (nt * N + ct) * 4
        if off not in cells: missing.append((nt, ct))
        else: grid[nt][ct] = cells[off]
assert not missing, f'cells never written: {missing[:20]}'

# stores that fell OUTSIDE the 26x26 window would mean the stride guess is wrong
outside = sorted(o for o in cells if not (BASE <= o < BASE + N * N * 4))
print(f'stores outside the {N}x{N} window: {len(outside)}'
      + (f'  first={[hex(o) for o in outside[:8]]}' if outside else ''))

json.dump({'base': BASE, 'n': N, 'grid': grid, 'outside': [hex(o) for o in outside]},
          open('evidence/71-action-permission-matrix.json', 'w'), indent=1)

hdr = '      ' + ' '.join(f'{c:2d}' for c in range(N))
out = ['CharacterActionPermission matrix — GameEngine+0x2802c, [newType][curType], 26x26',
       f'default fill = 2 (rep stosd 0x2a4 dwords)', '', hdr]
for nt in range(N):
    out.append(f'new={nt:2d} ' + ' '.join(f'{v:2d}' for v in grid[nt]))
open('evidence/72-action-permission-matrix.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))

print()
print(f'>>> LAP CELL  permission[new=PlayAnimationAction(0x12=18)][cur=MoveAction(4)] = {grid[18][4]}')
print(f'>>> row 18 (PlayAnimationAction as the NEW action): {grid[18]}')
print(f'>>> col  4 (MoveAction as the CURRENT action):      {[grid[i][4] for i in range(N)]}')
