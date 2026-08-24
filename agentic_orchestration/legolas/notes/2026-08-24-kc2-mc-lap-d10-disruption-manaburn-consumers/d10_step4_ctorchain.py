"""D-10 step 4 — walk a class's default-ctor chain and report every `[reg+0xca]` write seen along
the way, in ctor order.  The LAST write wins, so this resolves the disruptable flag for a concrete
skill class instead of assuming inheritance.  READ-ONLY."""
import sys, re; sys.path.insert(0, '.')
import d4b_dis as D
import d8_lib as B

FLAG = 0xca


def ctor_rva(cls):
    n = f'??0{cls}@GAME@@QAE@XZ'
    return D.EX.get(n)


def chain(cls, depth=0, seen=None):
    seen = seen if seen is not None else set()
    rva = ctor_rva(cls)
    if rva is None:
        return [(depth, cls, None, 'NO-DEFAULT-CTOR-EXPORT')]
    if cls in seen:
        return []
    seen.add(cls)
    lines = B.bounded(rva, 400)
    writes = []
    bases = []
    for l in lines:
        m = re.search(r'mov\s+(byte|dword) ptr \[\w+ \+ 0xca\], (\S+)', l)
        if m:
            writes.append((int(l.split()[0], 16), m.group(1), m.group(2)))
        m2 = re.search(r'call\s+0x[0-9a-f]+\s+; -> \?\?0(\w+)@GAME@@QAE@XZ', l)
        if m2:
            bases.append(m2.group(1))
    out = []
    for b in bases:
        out += chain(b, depth + 1, seen)
    out.append((depth, cls, rva, writes))
    return out


for cls in sys.argv[1:]:
    print(f'######## {cls}')
    for depth, c, rva, w in chain(cls):
        pad = '  ' * depth
        if rva is None:
            print(f'  {pad}{c}: {w}')
        else:
            print(f'  {pad}{c} @ {rva:#010x}  +0xca writes: {w if w else "none"}')
    print()
