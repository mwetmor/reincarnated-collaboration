"""MD-B4app-9 step 2 — identify the RTTI_ClassInfo statics that the two CheckAction downcast
helpers compare against, so the 0xea347 fallback branch is named rather than guessed.  READ-ONLY."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base
def probe(rva, label):
    print(f'=== {label}: RTTI_ClassInfo static @ RVA {rva:#010x}')
    s=D.sym(rva) or D.nearest(rva)
    print(f'    nearest export: {s}')
    b=pe.at(rva, 0x20)
    words=struct.unpack_from('<8I', b, 0)
    for i,w in enumerate(words):
        note=''
        if IB <= w < IB+0x1000000:
            t=w-IB
            try:
                cs=pe.cstr(t)
                if cs.isprintable() and 1<len(cs)<80: note=f'  -> cstr "{cs}"'
            except Exception: pass
            if not note:
                n=D.nearest(t)
                if n: note=f'  -> {n}'
        print(f'    +{i*4:#04x}  {w:#010x}{note}')
    print()
for r,l in ((0x7ff5a0,'helper-A (0x0000b260) target'),(0x7ff618,'helper-B (0x0000b150) target')):
    probe(r,l)
