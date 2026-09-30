import sys, struct, bisect, re
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
pat=re.compile(r'\+ (0x[0-9a-f]+)\]')
byfn={}
for ins in md.disasm(code, base):
    if '[' not in ins.op_str: continue
    for m in pat.finditer(ins.op_str):
        d=int(m.group(1),16)
        if d in (0x194,0x198,0x19c,0x1f0,0x208,0x210,0x218,0x220,0x1b4,0x1b8):
            f=fn_of(ins.address)
            byfn.setdefault(f,{}).setdefault(d,[]).append((ins.address, ins.mnemonic+' '+ins.op_str))
for f,dd in sorted(byfn.items()):
    keys=set(dd)
    if {0x194,0x19c} & keys and {0x1f0,0x218,0x210} & keys:
        print(f"### fn {f:#x}  offsets {[hex(k) for k in sorted(keys)]}")
        for d in sorted(dd):
            for a,t in dd[d]: print(f"   {a:#x} {t}")
