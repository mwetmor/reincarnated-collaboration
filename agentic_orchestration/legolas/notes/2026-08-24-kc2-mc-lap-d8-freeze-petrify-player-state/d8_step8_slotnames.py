"""D-8 step 8 — name every one of the 83 ControllerPlayerState vtable slots, preferring the BASE
class occupant's symbol and falling back to Idle's.  READ-ONLY."""
import sys, struct, re; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base; N=83
def slots(b,n=N):
    return [(lambda v: v-IB if v>IB else 0)(struct.unpack_from('<I',pe.raw,pe.rva2off(b+4*k))[0]) for k in range(n)]
BASE=slots(D.EX['??_7ControllerPlayerState@GAME@@6B@'])
IDLE=slots(D.EX['??_7ControllerPlayerStateIdle@GAME@@6B@'])
def nm(rva):
    s=D.nearest(rva) or ''
    m=re.match(r'\?(~?\w+)@(\w+)@',s)
    return (m.group(1),m.group(2)) if m else (s,'')
NAMES={}
for k in range(N):
    a,ca=nm(BASE[k]); b,cb=nm(IDLE[k])
    pick = a if ca.startswith('ControllerPlayerState') or ca.startswith('ControllerAIState') else (b if cb.startswith('ControllerPlayerState') else a or b)
    NAMES[k]=pick
if __name__=='__main__':
    for k in range(N):
        print(f'  [{k:2d}] +{4*k:#05x}  {NAMES[k]:34s} base={D.nearest(BASE[k])}')
