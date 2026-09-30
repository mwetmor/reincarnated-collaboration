import sys, struct, bisect
sys.path.insert(0,'.')
from pe import PE
from exports import dump
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
def fn_of(v):
    i=bisect.bisect_right(F,(v,1<<62))-1
    return F[i][0] if i>=0 and F[i][0]<=v<F[i][1] else 0
EX={}
for a,n in dump(P): EX.setdefault(a,[]).append(n)
TXT=[s for s in p.sections if s[0]=='.text'][0]
base=p.imagebase+TXT[1]; off=TXT[3]; ln=TXT[4]
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
EQ={0x720:'physicalDamageEquation',0x728:'physicalDamagePercentage',0x730:'physicalDamageBonus',
    0x738:'physicalDurationDamageEquation',0x740:'pierceDamageEquation',0x748:'magicalDamageEquation',
    0x750:'magicalDurationDamageEquation'}
res={}
d=p.d
for disp,label in EQ.items():
    pat=struct.pack('<I',disp)
    i=off
    while True:
        i=d.find(pat,i,off+ln)
        if i<0: break
        # try decode starting 3..8 bytes before
        for back in (3,4,2,5,6,7):
            s=i-back
            try: ins=next(md.disasm(d[s:s+16], base+(s-off), 1))
            except StopIteration: continue
            if ins.size==back+4 and f'0x{disp:x}]' in ins.op_str and ins.mnemonic in ('mov','lea','call','cmp','movss'):
                a=base+(s-off); f=fn_of(a)
                res.setdefault(label,[]).append((a,f,ins.mnemonic+' '+ins.op_str))
                break
        i+=1
for label in EQ.values():
    v=res.get(label,[])
    print(f"=== {label}: {len(v)} site(s)")
    seen=set()
    for a,f,t in v:
        n=EX.get(f,['?'])[0]
        print(f"   {a:#x} in {f:#x}  {n[:110]}   | {t}")
