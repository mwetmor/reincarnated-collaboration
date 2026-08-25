"""RESID-D1-2 step 13 — the LAST HOP, in Engine.dll: NavManager.  Game.dll's
CharacterMovementManager::Stop resolves to Engine.dll `NavManager::StopObject(Entity*)`; this walks
the Engine-side owner of per-frame entity translation so the immobility claim is anchored on the
module that actually moves the body.  READ-ONLY."""
import sys, struct, bisect, re; sys.path.insert(0, '.')
from d4b_pe import PE32
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

DLL = '/Users/admin/Games/vendor/grim-dawn/Engine.dll'
pe = PE32(DLL)
EX, _ = pe.exports()
BY_RVA = {}
for n, r in EX.items(): BY_RVA.setdefault(r, []).append(n)
SORTED = sorted(BY_RVA)
md = Cs(CS_ARCH_X86, CS_MODE_32)
IB = pe.image_base

def sym(r):
    ns = BY_RVA.get(r)
    return (min(ns, key=len) if ns and len(ns) > 1 else (ns[0] if ns else None))

def nearest(r):
    i = bisect.bisect_right(SORTED, r) - 1
    if i < 0: return None
    b = SORTED[i]
    return f'{sym(b)}+{r-b:#x}' if r != b else sym(b)

def bounded(rva, maxn=600):
    i = bisect.bisect_right(SORTED, rva)
    end = SORTED[i] if i < len(SORTED) else rva + 0x800
    out = []
    for ins in md.disasm(pe.at(rva, maxn * 8), IB + rva):
        r = ins.address - IB
        if r >= end: break
        ann = ''
        if ins.mnemonic in ('call', 'jmp') and ins.op_str.startswith('0x'):
            t = int(ins.op_str, 16) - IB
            s = nearest(t)
            if s: ann = f'   ; -> {s}'
        out.append(f'  {r:#010x}  {ins.mnemonic:<8} {ins.op_str}{ann}')
        if len(out) >= maxn: break
    return out

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'ls':
        rx = re.compile(sys.argv[2])
        for r, n in sorted((r, n) for n, r in EX.items() if rx.search(n)):
            print(f'{r:#010x} {n}')
    elif mode == 'd':
        nm = sys.argv[2]
        rva = EX[nm] if not nm.startswith('0x') else int(nm, 16)
        print(f'=== {nm} @ {rva:#010x} ({nearest(rva)}) ===')
        print('\n'.join(bounded(rva, int(sys.argv[3]) if len(sys.argv) > 3 else 300)))
    elif mode == 'x':          # byte-exact call/jmp xrefs
        tgt = EX[sys.argv[2]] if not sys.argv[2].startswith('0x') else int(sys.argv[2], 16)
        t = [s for s in pe.sections if s['name'].startswith('.text')][0]
        blob = pe.raw[t['raddr']: t['raddr'] + t['rsize']]; base = t['vaddr']
        for i in range(len(blob) - 5):
            if blob[i] in (0xE8, 0xE9):
                rel = struct.unpack_from('<i', blob, i + 1)[0]
                if base + i + 5 + rel == tgt:
                    print(f'  {"call" if blob[i]==0xE8 else "jmp "} @ {base+i:#010x}  in {nearest(base+i)}')
