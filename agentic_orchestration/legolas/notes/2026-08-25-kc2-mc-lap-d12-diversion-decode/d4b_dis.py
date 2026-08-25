"""D-4b disassembly harness. READ-ONLY. Annotates x86-32 with:
   - call/jmp targets resolved to EXPORTED symbol names (Game.dll ships 25,091 named exports)
   - absolute memory operands resolved to .rdata constants, shown as float32/float64/int
This makes 'is there a divide-by-duration' a readable question instead of a guess."""
import sys, struct, bisect; sys.path.insert(0,'.')
from d4b_pe import PE32
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

DLL = '/Users/admin/Games/vendor/grim-dawn/Game.dll'
pe = PE32(DLL)
EX, _ = pe.exports()
BY_RVA = {}
for n, r in EX.items(): BY_RVA.setdefault(r, []).append(n)
SORTED_RVA = sorted(BY_RVA)
md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
IB = pe.image_base

def sym(rva):
    ns = BY_RVA.get(rva)
    if ns: return min(ns, key=len) if len(ns) > 1 else ns[0]
    return None

def nearest(rva):
    i = bisect.bisect_right(SORTED_RVA, rva) - 1
    if i < 0: return None
    base = SORTED_RVA[i]
    return f'{sym(base)}+{rva-base:#x}' if rva != base else sym(base)

def const_at(rva):
    """Render an .rdata/.data constant several ways so a divisor is recognisable."""
    b = pe.at(rva, 8)
    if not b or len(b) < 4: return None
    out = []
    f32 = struct.unpack_from('<f', b, 0)[0]
    i32 = struct.unpack_from('<i', b, 0)[0]
    out.append(f'f32={f32:g}')
    out.append(f'i32={i32}')
    if len(b) == 8:
        out.append(f'f64={struct.unpack_from("<d", b, 0)[0]:g}')
    return ' '.join(out)

def in_const_sec(rva):
    for s in pe.sections:
        if s['name'] in ('.rdata', '.data') and s['vaddr'] <= rva < s['vaddr']+max(s['vsize'], s['rsize']):
            return True
    return False

def disasm(name_or_rva, n=200, stop_at_ret=True):
    rva = EX[name_or_rva] if isinstance(name_or_rva, str) else name_or_rva
    code = pe.at(rva, n*8)
    lines = []
    count = 0
    for ins in md.disasm(code, IB + rva):
        r = ins.address - IB
        ann = ''
        if ins.mnemonic in ('call', 'jmp') and ins.op_str.startswith('0x'):
            t = int(ins.op_str, 16) - IB
            s = nearest(t)
            if s: ann = f'   ; -> {s}'
        else:
            # absolute memory operand  [0x1xxxxxxx]
            import re
            m = re.search(r'\[(0x[0-9a-f]+)\]', ins.op_str)
            if m:
                t = int(m.group(1), 16) - IB
                if in_const_sec(t):
                    c = const_at(t)
                    s = sym(t)
                    ann = f'   ; {"["+s+"] " if s else ""}{c or ""}'
        lines.append(f'  {r:#010x}  {ins.mnemonic:<8} {ins.op_str}{ann}')
        count += 1
        if stop_at_ret and ins.mnemonic.startswith('ret'): break
        if count >= n: break
    return lines

if __name__ == '__main__':
    tgt = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    print(f'=== {tgt}  @ RVA {EX[tgt]:#010x} ===')
    print('\n'.join(disasm(tgt, n)))
