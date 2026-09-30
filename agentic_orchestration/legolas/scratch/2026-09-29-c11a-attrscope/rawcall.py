import sys, struct, bisect
sys.path.insert(0,'.')
from pe import PE
from exports import dump
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
d=p.d
def refs(target):
    out=[]
    for i in range(off, off+ln-5):
        b=d[i]
        if b!=0xE8 and b!=0xE9: continue
        rel=struct.unpack_from('<i', d, i+1)[0]
        va_=base+(i-off)
        if va_+5+rel==target:
            out.append((va_, 'call' if b==0xE8 else 'jmp'))
    return out
for t in [int(x,16) for x in sys.argv[1:]]:
    r=refs(t)
    print(f"== {t:#x} {EX.get(t,[''])[0]}  -> {len(r)} refs")
    for a,k in r:
        f=fn_of(a)
        print(f"   {k} @ {a:#x} in {f:#x}  {EX.get(f,['?'])[0][:110]}")
