"""D-8 step 31 — byte-exact scan of .text for every instruction encoding that references the
displacement 0x1cb7 (the Character byte ExecuteImmobilize sets) and for indirect calls to
DurationDamageManager vtable slot 6 (RemoveAllDamages).  Two independent techniques, D-7 §6 pattern."""
import sys, struct, re; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe;IB=pe.image_base
text=[s for s in pe.sections if s['name'].startswith('.text')][0]
blob=pe.raw[text['raddr']:text['raddr']+text['rsize']]; base=text['vaddr']
pat=struct.pack('<i',0x1cb7)
i=blob.find(pat); hits=[]
while i!=-1:
    hits.append(base+i); i=blob.find(pat,i+1)
print(f'=== disp32 0x1cb7 occurrences in .text: {len(hits)}')
for h in hits:
    # decode the instruction that most likely starts up to 8 bytes earlier
    for back in range(2,9):
        ls=D.disasm(h-back,1,stop_at_ret=False)
        if ls and '0x1cb7' in ls[0]:
            print(f'   {ls[0].strip():70s} in {D.nearest(h-back)}'); break
    else:
        print(f'   rva {h:#010x}  (no clean decode)  in {D.nearest(h)}')
print()
print('=== ImDead@DurationDamageManager (does the death path cleanse?) ===')
from d8_lib import bounded
for l in bounded(D.EX['?ImDead@DurationDamageManager@GAME@@QAEXXZ']): print(l)
