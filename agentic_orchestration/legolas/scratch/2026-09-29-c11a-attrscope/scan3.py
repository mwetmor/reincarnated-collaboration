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
NAMES={0x6c4:'set physDmgDV',0x6c8:'set pierceDmgDV',0x6cc:'set magDmgDV',
       0x720:'ld physEq',0x728:'ld physPctEq',0x730:'ld physBonusEq',0x738:'ld physDurEq',
       0x740:'ld pierceEq',0x748:'ld magEq',0x750:'ld magDurEq',
       0x194:'CM.physDmgDV',0x19c:'CM.magDmgDV',0x1f0:'CM.physEq',0x218:'CM.magEq'}
pat=re.compile(r'\+ (0x[0-9a-f]+)\]')
byfn={}
for ins in md.disasm(code, base):
    if '[' not in ins.op_str: continue
    for m in pat.finditer(ins.op_str):
        d=int(m.group(1),16)
        if d in NAMES:
            byfn.setdefault(fn_of(ins.address),[]).append((ins.address,NAMES[d],ins.mnemonic+' '+ins.op_str))
for f,v in sorted(byfn.items()):
    kinds={x[1] for x in v}
    if any(k.startswith('ld ') for k in kinds):
        print(f"### fn {f:#x}")
        for a,k,t in v: print(f"   {a:#x} [{k}] {t}")
