"""D-7 step 32 — MD-B2-2 as a MATRIX.  For every `Request*` slot named by Idle, record whether each
ControllerPlayerState<Control> keeps Idle's implementation (PERMITTED) or replaces it with a
constant-false / empty stub (SUPPRESSED).  The stub shape is printed so the verdict is checkable.
Emits evidence/md_b2_2_player_suppression.csv.  READ-ONLY."""
import sys, struct, re, csv; sys.path.insert(0, '.')
import d4b_dis as D
pe = D.pe; IB = pe.image_base
N = 83

def slots(base, n=N):
    return [(lambda v: v - IB if v > IB else 0)(
        struct.unpack_from('<I', pe.raw, pe.rva2off(base + 4 * k))[0]) for k in range(n)]

def lines(rva, k=8):
    try:
        return [x.split('  ', 3)[-1].strip() for x in D.disasm(rva, k)[:k]]
    except Exception:
        return []

def classify(rva):
    """A slot body is a REFUSAL iff it is `xor al,al; ret n` (returns false) or a bare `ret n`."""
    ls = lines(rva, 4)
    num = lambda s: bool(re.fullmatch(r'(0x[0-9a-f]+|\d+)', s))
    if not ls: return 'EMPTY-BODY'
    if len(ls) == 1 and (num(ls[0]) or ls[0] == ''): return 'STUB-ret'          # bare `ret n`
    if len(ls) >= 2 and ls[0] == 'al, al' and num(ls[1]): return 'STUB-false'   # xor al,al; ret n
    return 'IMPL'

IDLE_RVA = D.EX['??_7ControllerPlayerStateIdle@GAME@@6B@']
IDLE = slots(IDLE_RVA)
names = {}
for k in range(N):
    s = D.nearest(IDLE[k]) or ''
    m = re.match(r'\?(\w+)@ControllerPlayerState', s)
    if m: names[k] = m.group(1)

REQ = {k: v for k, v in names.items() if v.startswith('Request')}
STATES = ['Stunned', 'KnockedDown', 'Sleep', 'Trapped', 'Immobilized', 'UseSkillWhileTrapped']
tabs = {c: slots(D.EX[f'??_7ControllerPlayerState{c}@GAME@@6B@']) for c in STATES}

rows = []
hdr = f'{"slot":>4} {"request":32s} ' + ' '.join(f'{c[:12]:>13s}' for c in STATES)
print(hdr); print('-' * len(hdr))
for k in sorted(REQ):
    cells = []
    for c in STATES:
        cells.append('PERMITTED' if tabs[c][k] == IDLE[k] else classify(tabs[c][k]))
    print(f'{k:>4} {REQ[k]:32s} ' + ' '.join(f'{x[:13]:>13s}' for x in cells))
    rows.append({'vtable_slot': k, 'vtable_offset': hex(4 * k), 'request': REQ[k],
                 **{c: cells[i] for i, c in enumerate(STATES)}})

with open('evidence/md_b2_2_player_suppression.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['vtable_slot', 'vtable_offset', 'request'] + STATES)
    w.writeheader(); w.writerows(rows)
print('\n-> evidence/md_b2_2_player_suppression.csv')

print('\n=== slot occupants replaced, with RVA (for audit) ===')
for c in STATES:
    print(f'--- {c}')
    for k in sorted(REQ):
        if tabs[c][k] != IDLE[k]:
            print(f'   [{k}] {REQ[k]:30s} -> {tabs[c][k]:#010x} {classify(tabs[c][k])}  body={lines(tabs[c][k],3)}')
