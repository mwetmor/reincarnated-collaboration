"""D-11 step 4 — read named vtable slots.  Locate `??_7<Class>@GAME@@6B@` in .rdata (it is an
exported symbol in this build), then print the function at each requested byte displacement,
resolved to its export name plus the first four instructions of its body.  READ-ONLY."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
import d8_lib as B
pe=D.pe; IB=pe.image_base
cls=sys.argv[1]
disps=[int(a,0) for a in sys.argv[2:]]
cands=[n for n in D.EX if n.startswith(f'??_7{cls}@GAME@@6B')]
for c in sorted(cands):
    v=D.EX[c]
    print(f'=== {c} @ {v:#010x}')
    for d in disps:
        tgt=struct.unpack_from('<I', pe.at(v+d,4),0)[0]-IB
        nm=D.nearest(tgt)
        body=[l.split(None,2)[2] if len(l.split(None,2))>2 else l for l in B.bounded(tgt,6)[:6]]
        print(f'  +{d:#05x} (slot {d//4:4d}) -> {tgt:#010x}  {nm}')
        for b in body: print(f'        {b}')
    print()
