"""D-4 HP-orb reader.

Gate design (documented defect D-D4-1): Lap K's absolute per-glyph NCC floor (0.78) rejects the
LAST glyph of the hp_max field, whose anti-aliasing against the globe rim depresses NCC to ~0.73
while its top-2 margin stays enormous (0.73 vs 0.46). An absolute floor is therefore the wrong
gate here; a MARGIN gate is the discriminative one. Gates:
  G1  best NCC          >= 0.70
  G2  top-2 margin      >= 0.15      <- the discriminative gate
  G3  no box touching a ROI edge      (in d4_ocr.boxes)
  G4  at most one leading + one trailing junk box may be stripped, and the LONGEST valid
      parse wins (never discard a glyph that parses)
Validated against Lap K's certified trace on eor-test-2: see d4_validate.py output in method.md.
"""
import numpy as np, pickle, os
from d4_ocr import mask_of, boxes, norm, ncc
_T=pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'d4_templates.pkl'),'rb'))
G1, G2 = 0.70, 0.15
def _classify(m,bs):
    out=[]
    for a,b in bs:
        v=norm(m[:,a:b])
        if v is None: return None
        sc=sorted(((ncc(v,t),ch) for ch,t in _T.items()), reverse=True)
        out.append((sc[0][1], sc[0][0], sc[0][0]-sc[1][0]))
    return out
def read(img):
    m=mask_of(img); bs=boxes(m)
    if not (7<=len(bs)<=13): return None
    ch=_classify(m,bs)
    if ch is None: return None
    cands=[]
    for lead in (0,1):
        for trail in (0,1):
            c=ch[lead:len(ch)-trail] if trail else ch[lead:]
            if len(c)<3: continue
            if min(x[1] for x in c) < G1: continue
            if min(x[2] for x in c) < G2: continue
            s=''.join(x[0] for x in c)
            if s.count('/')!=1: continue
            a,b=s.split('/')
            if not(a and b and a.isdigit() and b.isdigit()): continue
            if len(a)>5 or len(b)>5: continue
            cands.append((-(len(c)), -min(x[1] for x in c), int(a), int(b)))
    if not cands: return None
    cands.sort()
    return cands[0][2], cands[0][3]
