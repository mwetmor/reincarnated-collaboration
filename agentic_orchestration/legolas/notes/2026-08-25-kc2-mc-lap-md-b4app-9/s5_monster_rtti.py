"""MD-B4app-9 step 5 — walk the RTTI_ClassInfo base chain for Monster and Player so the claim
'Get<Player>(monsterEntityId) == NULL' rests on the shipped class graph, not on intuition.
Also dumps ?GetLocalPlayer@AreaTrigger@ (the 0x2e-byte helper-A wrapper whose MANGLED RETURN TYPE
is PAVPlayer) as the independent corroboration of helper-A's identity.  READ-ONLY."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
import d8_lib as B
pe=D.pe; IB=pe.image_base
def chain(name):
    rva=D.EX[name]; print(f'=== base chain from {name} @ {rva:#010x}')
    seen=set(); cur=rva
    while cur and cur not in seen:
        seen.add(cur)
        s=D.sym(cur) or D.nearest(cur)
        print(f'    {cur:#010x}  {s}')
        b=pe.at(cur+8,4)
        if not b or len(b)<4: break
        nxt=struct.unpack_from('<I',b,0)[0]
        cur = nxt-IB if nxt else 0
    print()
for n in ('?classInfo@Monster@GAME@@1VRTTI_ClassInfo@2@B','?classInfo@Player@GAME@@1VRTTI_ClassInfo@2@B'):
    if n in D.EX: chain(n)
    else: print(f'!! {n} not exported'); print()

print('=== ?GetLocalPlayer@AreaTrigger@GAME@@IBEPAVPlayer@2@XZ  (helper-A identity witness) ===')
for l in B.bounded(D.EX['?GetLocalPlayer@AreaTrigger@GAME@@IBEPAVPlayer@2@XZ'], 30): print('  ',l)
print()
print('=== ?RequestMove@ControllerMonsterStateStartup@GAME@@UAEXIABVWorldVec3@2@@Z  (monster-side null idiom) ===')
for l in B.bounded(D.EX['?RequestMove@ControllerMonsterStateStartup@GAME@@UAEXIABVWorldVec3@2@@Z'], 40): print('  ',l)
