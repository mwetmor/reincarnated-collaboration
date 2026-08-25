"""D-11 step 5 — find which vtable displacement of a class holds a given target RVA. READ-ONLY."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base
cls=sys.argv[1]; tgt=int(sys.argv[2],0); span=int(sys.argv[3],0) if len(sys.argv)>3 else 0x400
for c in sorted(n for n in D.EX if n.startswith(f'??_7{cls}@GAME@@6B')):
    v=D.EX[c]
    for d in range(0, span, 4):
        b=pe.at(v+d,4)
        if not b or len(b)<4: break
        if struct.unpack_from('<I',b,0)[0]-IB == tgt:
            print(f'{c} @ {v:#010x}  slot +{d:#05x} ({d//4}) -> {tgt:#010x} {D.nearest(tgt)}')
