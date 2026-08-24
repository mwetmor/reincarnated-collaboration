"""D-7 step 30 — MD-B2-2.  Diff each ControllerPlayerState<Control> vtable against the BASE
ControllerPlayerState vtable and against Idle.  A control state suppresses exactly what it
OVERRIDES; everything else is inherited.  Named-symbol output, no inference.  READ-ONLY."""
import sys, struct; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base
N = 83   # vtable stride 0x14c / 4, measured from consecutive ??_7 export RVAs

def slots(base, n=N):
    out = []
    for k in range(n):
        v = struct.unpack_from('<I', pe.raw, pe.rva2off(base + 4 * k))[0]
        out.append(v - IB if v > IB else 0)
    return out

BASE = '??_7ControllerPlayerState@GAME@@6B@'
IDLE = '??_7ControllerPlayerStateIdle@GAME@@6B@'
CTRL = ['Stunned', 'KnockedDown', 'Sleep', 'Trapped', 'Immobilized',
        'UseSkillWhileTrapped', 'Dying']
base = slots(D.EX[BASE]); idle = slots(D.EX[IDLE])

def body(rva, k=5):
    try:
        return ' ; '.join(x.split('  ', 3)[-1].strip() for x in D.disasm(rva, k)[:k])
    except Exception:
        return ''

for c in CTRL:
    nm = f'??_7ControllerPlayerState{c}@GAME@@6B@'
    if nm not in D.EX:
        print(f'!! {nm} absent'); continue
    v = slots(D.EX[nm])
    print(f'=== ControllerPlayerState{c}  @ {D.EX[nm]:#010x}')
    for k in range(N):
        if v[k] != base[k]:
            print(f'  [{k:2d}] +{4*k:#05x}  {v[k]:#010x}  {D.nearest(v[k])}')
            print(f'            base -> {D.nearest(base[k])}')
            print(f'            body: {body(v[k])}')
    print()
print('=== IDLE deltas vs base (control reference) ===')
for k in range(N):
    if idle[k] != base[k]:
        print(f'  [{k:2d}] +{4*k:#05x}  {D.nearest(idle[k])}   (base {D.nearest(base[k])})')
