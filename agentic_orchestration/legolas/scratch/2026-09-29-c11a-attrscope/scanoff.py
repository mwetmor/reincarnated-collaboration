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
    return F[i][0] if i>=0 and F[i][0]<=v<F[i][1] else None
TXT=[s for s in p.sections if s[0]=='.text'][0]
base=p.imagebase+TXT[1]; code=p.d[TXT[3]:TXT[3]+TXT[4]]
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
targets={0x1f0:'physEq',0x1f8:'physPct',0x200:'physBonus',0x208:'physDurEq',0x210:'pierceEq',0x218:'magEq',0x220:'magDurEq',
         0x194:'physDmgVal',0x198:'pierceDmgVal',0x19c:'magDmgVal'}
pat=re.compile(r'\+ (0x[0-9a-f]+)\]')
hits={}
for ins in md.disasm(code, base):
    if '[' not in ins.op_str: continue
    for m in pat.finditer(ins.op_str):
        d=int(m.group(1),16)
        if d in targets:
            hits.setdefault(targets[d],[]).append((ins.address, fn_of(ins.address), ins.mnemonic+' '+ins.op_str))
for k in ['physEq','pierceEq','magEq','physDurEq','magDurEq','physPct','physBonus']:
    v=hits.get(k,[])
    fns=sorted(set(x[1] or 0 for x in v))
    print(f"{k}: {len(v)} refs, fns={[hex(f) if f else None for f in fns]}")
    for a,f,t in v: print(f"    {a:#x} in {hex(f) if f else '?'}  {t}")
