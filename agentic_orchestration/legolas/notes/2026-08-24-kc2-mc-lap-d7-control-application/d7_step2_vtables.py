"""D-7 step 2 — dump the vtables of the control attribute classes so the AddToAccumulator
implementation each family actually uses is a NAMED function, not an assumption. READ-ONLY."""
import sys, struct; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base

TARGETS = [n for n in D.EX if n.startswith('??_7') and (
    'DamageAttributeReflex' in n or 'DefenseAttributeAbs_' in n or
    'DefenseAttributeDefenseCap_' in n or 'DamageAttributeAbs_' in n)]

def slots(vt_rva, n=14):
    out = []
    for k in range(n):
        a = vt_rva + 4 * k
        try:
            v = struct.unpack_from('<I', pe.raw, pe.rva2off(a))[0]
        except Exception:
            break
        if v <= IB: break
        out.append((k, v - IB, D.nearest(v - IB)))
    return out

FAM = ('Stun', 'Freeze', 'Petrify', 'Trap', 'Sleep', 'Knockdown',
       'Confusion', 'Convert', 'Fear', 'Taunt', 'Disruption', 'CrowdControl', 'Fire')
for n in sorted(TARGETS):
    if not any(f'_{f}@' in n for f in FAM): continue
    print(f'=== {n}  @ {D.EX[n]:#010x}')
    for k, r, s in slots(D.EX[n]):
        print(f'   [{k:2d}] {r:#010x}  {s}')
    print()
