import struct,re
from pe import PE
p=PE('/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/x64/Game.dll')
n,va,vsz,ro,rsz=p.sec('.text')
text=p.b[ro:ro+vsz]
def lea_xrefs(targets):
    targets=set(targets); out=[]
    for m in re.finditer(rb'[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]',text):
        i=m.start(); disp=struct.unpack_from('<i',text,i+3)[0]
        t=va+i+7+disp
        if t in targets: out.append((va+i,t))
    return out
