import sys, struct, bisect
sys.path.insert(0,'.')
from pe import PE
import capstone
p=PE('/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/x64/Game.dll')
nm,va,vsz,roff,rsz=[s for s in p.sections if s[0]=='.pdata'][0]
F=[]
for i in range(roff,roff+vsz,12):
    b,e,u=struct.unpack_from('<III',p.d,i)
    if b==0: break
    F.append((p.imagebase+b,p.imagebase+e))
F.sort()
def fn_of(v):
    i=bisect.bisect_right(F,(v,1<<62))-1
    return F[i][0] if i>=0 and F[i][0]<=v<F[i][1] else 0
TXT=[s for s in p.sections if s[0]=='.text'][0]
base=p.imagebase+TXT[1]; code=p.d[TXT[3]:TXT[3]+TXT[4]]
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
T={int(x,16) for x in sys.argv[1:]}
res={}
for ins in md.disasm(code, base):
    if ins.mnemonic in ('call','jmp') and ins.op_str.startswith('0x'):
        t=int(ins.op_str,16)
        if t in T:
            res.setdefault(t,[]).append((ins.address, fn_of(ins.address), ins.mnemonic))
# also data refs (vtables)
for t in sorted(T):
    b=struct.pack('<Q', t)
    dr=[]
    i=0
    while True:
        i=p.d.find(b,i)
        if i<0: break
        v=p.off2va(i)
        if v: dr.append((v, p.sec_of_va(v)))
        i+=1
    print(f"== target {t:#x}: {len(res.get(t,[]))} direct calls, {len(dr)} data refs")
    for a,f,m in res.get(t,[]): print(f"   {m} from {a:#x} in fn {f:#x}")
    for v,s in dr[:12]: print(f"   dataref @ {v:#x} [{s}]")
