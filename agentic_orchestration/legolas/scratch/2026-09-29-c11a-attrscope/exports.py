import sys,struct; sys.path.insert(0,'.')
from pe import PE
def dump(path):
    p=PE(path); d=p.d
    e=struct.unpack_from('<I',d,0x3c)[0]; opt=e+24
    erva,esz=struct.unpack_from('<II',d,opt+112)
    if erva==0: return []
    eo=p.va2off(p.imagebase+erva)
    ch,ts,mj,mi,nr,ob,nF,nN,af,an,ao=struct.unpack_from('<IIHHIIIIIII',d,eo)
    AF=p.va2off(p.imagebase+af); AN=p.va2off(p.imagebase+an); AO=p.va2off(p.imagebase+ao)
    out=[]
    for i in range(nN):
        r=struct.unpack_from('<I',d,AN+4*i)[0]; o=struct.unpack_from('<H',d,AO+2*i)[0]
        no=p.va2off(p.imagebase+r); nm=d[no:d.find(b'\0',no)].decode('latin-1')
        fr=struct.unpack_from('<I',d,AF+4*o)[0]
        out.append((p.imagebase+fr, nm))
    return out
if __name__=='__main__':
    import re
    path=sys.argv[1]; pat=re.compile(sys.argv[2])
    ex=dump(path)
    n=0
    for va,nm in sorted(ex, key=lambda x:x[1]):
        if pat.search(nm): print(f"{va:#x}  {nm}"); n+=1
    print(f"--- {n}/{len(ex)}", file=sys.stderr)
