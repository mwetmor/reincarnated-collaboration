import sys
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm4s_pe_2026_08_14 import PE32
G="/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/Game.dll"
E="/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/Engine.dll"
game=PE32(G); eng=PE32(E)
import struct
def vt_slot(pe, vtsym, slot):
    r=pe.exports()[vtsym]; o=pe.rva_to_off(r+slot)
    p=struct.unpack_from('<I',pe.raw,o)[0]-pe.image_base
    return p, pe.sym_at(p)
def imports(pe):
    out={}
    d_rva,_=pe.dirs[1]; off=pe.rva_to_off(d_rva); b=pe.raw
    while True:
        oft,ts,fc,name,ft=struct.unpack_from('<IIIII',b,off)
        if name==0: break
        dll=b[pe.rva_to_off(name):b.index(b'\0',pe.rva_to_off(name))].decode()
        t=oft or ft; i=0
        while True:
            e=struct.unpack_from('<I',b,pe.rva_to_off(t)+4*i)[0]
            if e==0: break
            if not e&0x80000000:
                no=pe.rva_to_off(e)+2; nm=b[no:b.index(b'\0',no)].decode('latin-1')
            else: nm='ord%d'%(e&0xffff)
            out[pe.image_base+ft+4*i]=(dll,nm); i+=1
        off+=20
    return out
