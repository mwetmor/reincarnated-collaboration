"""D-11 step 6 — census of ONE vtable displacement across EVERY `??_7X@GAME@@6B@` vtable whose
class name matches a prefix filter.  Answers 'is this slot ever overridden?'  READ-ONLY."""
import sys, struct, collections; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base
disp=int(sys.argv[1],0); pref=sys.argv[2] if len(sys.argv)>2 else ''
c=collections.Counter(); who=collections.defaultdict(list)
for n,v in D.EX.items():
    if not n.startswith('??_7'): continue
    cls=n[4:].split('@GAME@@6B')[0]
    if pref and not cls.startswith(pref): continue
    b=pe.at(v+disp,4)
    if not b or len(b)<4: continue
    t=struct.unpack_from('<I',b,0)[0]-IB
    c[t]+=1; who[t].append(cls)
for t,k in c.most_common():
    print(f'{t:#010x}  n={k:4d}  {D.nearest(t)}')
    print(f'      e.g. {", ".join(sorted(set(who[t]))[:8])}')
