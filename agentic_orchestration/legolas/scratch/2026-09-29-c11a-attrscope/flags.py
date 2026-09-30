import sys, struct, bisect, re
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
rng={a:(a,b) for a,b in F}
EX={}
for a,n in dump(P): EX.setdefault(a,[]).append(n)
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
pat=re.compile(sys.argv[1])
rows=[]
for a in sorted(EX):
    names=[n for n in EX[a] if pat.search(n)]
    if not names: continue
    if a not in rng: continue
    s,e=rng[a]
    o=p.va2off(s); code=p.d[o:o+(e-s)]
    zeroed=set()
    flags=[]
    for ins in md.disasm(code, s):
        if ins.mnemonic=='xor':
            ops=[x.strip() for x in ins.op_str.split(',')]
            if len(ops)==2 and ops[0]==ops[1]: zeroed.add(ops[0]); zeroed.add(ops[0].replace('e','r',1))
        if ins.mnemonic=='mov' and 'byte ptr [' in ins.op_str and '+ 0x10]' in ins.op_str:
            src=ins.op_str.split(',')[-1].strip()
            v=src
            if src in ('cl','dl','al','r8b','bl','sil','dil'):
                big={'cl':'ecx','dl':'edx','al':'eax','bl':'ebx','r8b':'r8d','sil':'esi','dil':'edi'}[src]
                v = '0 (xor-zeroed)' if big in zeroed else src+' (?)'
            flags.append((ins.address, v))
        if ins.mnemonic=='and' and 'byte ptr [' in ins.op_str and '+ 0x10]' in ins.op_str:
            flags.append((ins.address,'AND '+ins.op_str))
    for n in names:
        rows.append((n, hex(a), flags))
for n,a,f in sorted(rows):
    print(f"{a}  {n}")
    for addr,v in f: print(f"        flag[+0x10] <- {v}   @{addr:#x}")
    if not f: print("        (no +0x10 store found)")
