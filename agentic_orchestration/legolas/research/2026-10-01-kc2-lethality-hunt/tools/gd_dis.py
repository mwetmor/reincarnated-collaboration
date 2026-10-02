import sys, struct, bisect, re, pickle, os
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-09-29-c11a-attrscope')
from pe import PE
import exports as EX
import capstone
P='/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/x64/Game.dll'
p=PE(P)
nm,va,vsz,roff,rsz=[s for s in p.sections if s[0]=='.pdata'][0]
F=[]
for i in range(roff,roff+vsz,12):
    b,e,u=struct.unpack_from('<III',p.d,i)
    if b==0: break
    F.append((p.imagebase+b,p.imagebase+e))
F.sort()
NAMES={}
for v,n in EX.dump(P):
    NAMES.setdefault(v,[]).append(n)
def nm(v):
    n=NAMES.get(v)
    if not n: return None
    s=n[0]
    m=re.match(r'\?(\w+)@(\w+)@',s)
    short = f"{m.group(2)}::{m.group(1)}" if m else s
    return short + (f" (+{len(n)-1})" if len(n)>1 else "")
def fn_of(v):
    i=bisect.bisect_right(F,(v,1<<62))-1
    return F[i] if i>=0 and F[i][0]<=v<F[i][1] else None
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
def cstr(v):
    o=p.va2off(v)
    if o is None: return None
    e=p.d.find(b'\0',o); s=p.d[o:e]
    if not s or len(s)>120: return None
    if all(32<=c<127 for c in s): return s.decode()
    return None
def flt(v):
    o=p.va2off(v)
    if o is None: return None
    return struct.unpack_from('<f',p.d,o)[0]
def dis(start,end=None):
    f=fn_of(start)
    if end is None: end=f[1] if f else start+0x300
    o=p.va2off(start); code=p.d[o:o+(end-start)]
    out=[]
    for ins in md.disasm(code,start):
        line=f"{ins.address:#x}  {ins.mnemonic} {ins.op_str}"
        m=re.search(r'\[rip ([+-]) (0x[0-9a-f]+)\]',ins.op_str)
        if m:
            d=int(m.group(2),16)*(1 if m.group(1)=='+' else -1)
            tv=ins.address+ins.size+d
            s=cstr(tv); n=nm(tv)
            extra=f'"{s}"' if s else (n or '')
            if ('ss ' in ins.mnemonic+' ' or ins.mnemonic in('movss','mulss','addss','subss','divss','comiss','ucomiss','maxss','minss')) and not s:
                extra += f' float={flt(tv)}'
            line+=f"   ; {tv:#x} {extra}"
        if ins.mnemonic in('call','jmp') and ins.op_str.startswith('0x'):
            t=int(ins.op_str,16); n=nm(t)
            if n: line+=f"   ; {n}"
        out.append(line)
    return out
_X=None
def xrefs():
    global _X
    cache='/tmp/legolas_gd_calls.pkl'   # scratch cache, outside the repo
    if _X is None and os.path.exists(cache): _X=pickle.load(open(cache,'rb'))
    if _X is None:
        X={}
        for (a,b) in F:
            o=p.va2off(a)
            if o is None: continue
            for ins in md.disasm(p.d[o:o+(b-a)],a):
                if ins.mnemonic in('call','jmp') and ins.op_str.startswith('0x'):
                    X.setdefault(int(ins.op_str,16),[]).append((ins.address,a))
        _X=X; pickle.dump(X,open(cache,'wb'))
    return _X
if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='dis':
        a=int(sys.argv[2],16); e=int(sys.argv[3],16) if len(sys.argv)>3 else None
        f=fn_of(a); print(f"; fn {f and hex(f[0])}-{f and hex(f[1])} {nm(f[0]) if f else ''}")
        print('\n'.join(dis(a,e)))
    elif cmd=='callers':
        X=xrefs()
        for t in sys.argv[2:]:
            t=int(t,16); print(f"== {t:#x} {nm(t)}")
            for (ad,fa) in X.get(t,[]): print(f"   {ad:#x} in {fa:#x} {nm(fa)}")
