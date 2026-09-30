#!/usr/bin/env python3
import sys, struct
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-09-29-c11a-attrscope')
from pe import PE
P = sys.argv[1]
p = PE(P)
# .pdata RUNTIME_FUNCTION table -> function ranges
name,va,vsz,roff,rsz = [s for s in p.sections if s[0]=='.pdata'][0]
funcs=[]
for i in range(roff, roff+vsz, 12):
    b,e,u = struct.unpack_from('<III', p.d, i)
    if b==0: break
    funcs.append((p.imagebase+b, p.imagebase+e))
funcs.sort()
def fn_of(va):
    import bisect
    i = bisect.bisect_right(funcs, (va, 1<<62)) - 1
    if i>=0 and funcs[i][0] <= va < funcs[i][1]: return funcs[i][0]
    return None
for s in sys.argv[2:]:
    offs = p.find_cstr(s)
    print(f"== {s!r}: {len(offs)} occurrence(s)")
    for o in offs:
        va = p.off2va(o)
        sec = p.sec_of_va(va)
        xr = p.lea_xrefs(va)
        fns = sorted(set(fn_of(x) for x in xr))
        print(f"   off {o:#x} va {va:#x} [{sec}] lea-xrefs={len(xr)} fns={[hex(f) if f else None for f in fns]}")
