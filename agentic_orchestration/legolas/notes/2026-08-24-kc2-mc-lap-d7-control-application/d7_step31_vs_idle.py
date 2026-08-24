"""D-7 step 31 — MD-B2-2, the readable form.  Diff each ControllerPlayerState<Control> vtable
against ControllerPlayerStateIdle (the un-controlled player).  The slot NAME comes from Idle's
occupant; the control state's occupant is what it is replaced with.  A `Default*Action` /
`ret <n>` occupant is a REFUSAL of that request; an Idle-named occupant is PERMITTED. READ-ONLY."""
import sys, struct, re; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base
N = 83

def slots(base, n=N):
    return [(lambda v: v - IB if v > IB else 0)(
        struct.unpack_from('<I', pe.raw, pe.rva2off(base + 4 * k))[0]) for k in range(n)]

def short(rva):
    s = D.nearest(rva) or f'{rva:#x}'
    m = re.match(r'\?(\w+)@(\w+)@', s)
    return f'{m.group(1)}@{m.group(2)}' if m else s

def body(rva, k=6):
    try:
        return ' ; '.join(x.split('  ', 3)[-1].strip() for x in D.disasm(rva, k)[:k])
    except Exception:
        return ''

IDLE = slots(D.EX['??_7ControllerPlayerStateIdle@GAME@@6B@'])
for c in ['Stunned', 'KnockedDown', 'Sleep', 'Trapped', 'Immobilized', 'UseSkillWhileTrapped']:
    nm = f'??_7ControllerPlayerState{c}@GAME@@6B@'
    v = slots(D.EX[nm])
    diffs = [k for k in range(N) if v[k] != IDLE[k]]
    print(f'=== {c}: {len(diffs)} of {N} slots differ from Idle')
    for k in diffs:
        print(f'  [{k:2d}] +{4*k:#05x}  IDLE={short(IDLE[k]):48s} -> {short(v[k])}')
        print(f'            body: {body(v[k])}')
    print()
