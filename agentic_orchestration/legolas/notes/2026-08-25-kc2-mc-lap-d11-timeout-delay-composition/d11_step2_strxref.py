"""D-11 step 2 — every 4-byte image-wide reference to a given string VA (push imm32 / mov imm32),
attributed to the nearest exported symbol.  READ-ONLY."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base; raw=pe.raw
def off2rva(i):
    for s in pe.sections:
        if s['raddr'] <= i < s['raddr']+s['rsize']:
            return s['vaddr'] + (i - s['raddr']), s['name']
    return None,'-'
for a in sys.argv[1:]:
    rva=int(a,0); va=IB+rva
    pat=struct.pack('<I', va); hits=[]; i=raw.find(pat)
    while i!=-1:
        r,sec=off2rva(i)
        hits.append((i,r,sec)); i=raw.find(pat,i+1)
    try: nm = pe.cstr(rva)
    except Exception: nm='?'
    print(f'=== {rva:#010x} VA {va:#010x} "{nm}" : {len(hits)} refs')
    for off,r,sec in hits:
        print(f'   file{off:#010x} rva {r if r is None else hex(r)} sec={sec} nearest={D.nearest(r) if r else "-"}')
