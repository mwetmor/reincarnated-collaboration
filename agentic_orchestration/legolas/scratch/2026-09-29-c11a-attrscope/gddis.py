#!/usr/bin/env python3
import sys, struct, bisect
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-09-29-c11a-attrscope')
from pe import PE
import capstone
P='/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/x64/Game.dll'
p=PE(P)
name,va,vsz,roff,rsz=[s for s in p.sections if s[0]=='.pdata'][0]
FUNCS=[]
for i in range(roff,roff+vsz,12):
    b,e,u=struct.unpack_from('<III',p.d,i)
    if b==0: break
    FUNCS.append((p.imagebase+b,p.imagebase+e))
FUNCS.sort()
def fn_of(v):
    i=bisect.bisect_right(FUNCS,(v,1<<62))-1
    return FUNCS[i] if i>=0 and FUNCS[i][0]<=v<FUNCS[i][1] else None
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail=False
def cstr_at(v):
    o=p.va2off(v)
    if o is None: return None
    e=p.d.find(b'\0',o)
    s=p.d[o:e]
    if len(s)>200 or not s: return None
    try: t=s.decode('ascii')
    except: return None
    return t if all(32<=c<127 or c in (9,10) for c in s) else None
def dis(start, end=None, annotate=True):
    f=fn_of(start)
    if end is None:
        end = f[1] if f else start+0x400
    o=p.va2off(start)
    code=p.d[o:o+(end-start)]
    out=[]
    for ins in md.disasm(code, start):
        line=f"{ins.address:#x}  {ins.mnemonic} {ins.op_str}"
        if annotate and 'rip' in ins.op_str:
            # resolve rip-rel
            import re
            m=re.search(r'\[rip \+ (0x[0-9a-f]+)\]|\[rip - (0x[0-9a-f]+)\]', ins.op_str)
            if m:
                d=int(m.group(1),16) if m.group(1) else -int(m.group(2),16)
                tv=ins.address+ins.size+d
                s=cstr_at(tv)
                line += f"   ; -> {tv:#x}" + (f'  "{s}"' if s else '')
        out.append(line)
    return out
if __name__=='__main__':
    a=int(sys.argv[1],16)
    e=int(sys.argv[2],16) if len(sys.argv)>2 else None
    print('\n'.join(dis(a,e)))
