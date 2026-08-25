"""D-8 helper: disassemble a function BOUNDED by the next exported RVA (the D-7 harness had no
bounds, which lets a listing leak into the neighbouring body).  READ-ONLY."""
import sys, bisect; sys.path.insert(0,'.')
import d4b_dis as D
def bounded(rva, maxn=600):
    i=bisect.bisect_right(D.SORTED_RVA, rva)
    end=D.SORTED_RVA[i] if i < len(D.SORTED_RVA) else rva+0x400
    out=[]
    for l in D.disasm(rva, maxn, stop_at_ret=False):
        r=int(l.split()[0],16)
        if r>=end: break
        out.append(l)
    return out
