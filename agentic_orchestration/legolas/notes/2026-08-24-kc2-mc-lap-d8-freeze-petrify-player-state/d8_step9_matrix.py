"""D-8 step 9 — the suppression matrix, re-derived on its own basis (not cited from D-7).
Columns: the five D-7 control states PLUS the four channel/cast states, so the question
'does a Freeze/Petrify landing END the channel' is read off the vtable rather than argued.
Emits evidence/d8_freeze_petrify_suppression.csv.  READ-ONLY."""
import sys, struct, re, csv; sys.path.insert(0,'.')
import d4b_dis as D
from d8_step8_slotnames import NAMES, slots, BASE, IDLE
pe=D.pe; IB=pe.image_base; N=83

def lines(rva,k=8):
    try: return [x.split('  ',3)[-1].strip() for x in D.disasm(rva,k)[:k]]
    except Exception: return []
def classify(rva):
    ls=lines(rva,4); num=lambda s: bool(re.fullmatch(r'(0x[0-9a-f]+|\d+)',s))
    if not ls: return 'EMPTY-BODY'
    if len(ls)==1 and (num(ls[0]) or ls[0]==''): return 'STUB-ret'
    if len(ls)>=2 and ls[0]=='al, al' and num(ls[1]): return 'STUB-false'
    return 'IMPL'

CTRL   = ['Stunned','KnockedDown','Sleep','Trapped','Immobilized']
CHAN   = ['UseSkill','ChargeToUseSkill','MoveAndUseSkill','MoveToUseSkill','JumpToUseSkill',
          'UseSkillWhileTrapped','Evade','MoveTo']
STATES = CTRL + CHAN
tabs={c:slots(D.EX[f'??_7ControllerPlayerState{c}@GAME@@6B@']) for c in STATES}

REQ=[k for k in range(N) if NAMES[k].startswith('Request')] + [54,55,56,57]
REQ=sorted(set(REQ))

print('### REQUEST-SLOT MATRIX  (PERMITTED = keeps Idle occupant)')
hdr=f'{"slot":>4} {"request":28s} '+' '.join(f'{c[:11]:>12s}' for c in STATES)
print(hdr); print('-'*len(hdr))
rows=[]
for k in REQ:
    cells=[('PERMITTED' if tabs[c][k]==IDLE[k] else classify(tabs[c][k])) for c in STATES]
    print(f'{k:>4} {NAMES[k]:28s} '+' '.join(f'{x[:12]:>12s}' for x in cells))
    rows.append({'vtable_slot':k,'vtable_offset':hex(4*k),'request':NAMES[k],
                 'idle_occupant_rva':hex(IDLE[k]),
                 **{c:cells[i] for i,c in enumerate(STATES)}})
with open('evidence/d8_request_matrix.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['vtable_slot','vtable_offset','request','idle_occupant_rva']+STATES)
    w.writeheader(); w.writerows(rows)

print()
print('### CONTROL-ENTRY SLOTS 40..51  (who each state routes an incoming control to)')
ENTRY={40:'BeginImmobilize',41:'EndImmobilize',42:'BeginTrap',43:'EndTrap',44:'BeginStun',
       45:'EndStun',46:'BeginSleep',47:'EndSleep',48:'BeginKnockdown',49:'EndKnockdown',
       50:'BeginTakeHit',51:'EndTakeHit',68:'OnBegin',70:'OnUpdate'}
hdr=f'{"slot":>4} {"entry":16s} {"IDLE":42s} '+' '.join(f'{c[:11]:>12s}' for c in STATES)
print(hdr); print('-'*len(hdr))
for k in sorted(ENTRY):
    cells=[('=IDLE' if tabs[c][k]==IDLE[k] else (D.nearest(tabs[c][k]) or hex(tabs[c][k]))) for c in STATES]
    short=lambda s: (re.match(r'\?(\w+)@(\w+)@',s).group(1) if re.match(r'\?(\w+)@(\w+)@',s) else s)[:12]
    print(f'{k:>4} {ENTRY[k]:16s} {str(D.nearest(IDLE[k]))[:42]:42s} '+' '.join(f'{short(x):>12s}' for x in cells))

print()
print('### FULL 83-SLOT DIFF: Immobilized vs Stunned  (the STUN_PROXY test)')
imm=tabs['Immobilized']; stn=tabs['Stunned']
d=[k for k in range(N) if imm[k]!=stn[k]]
print(f'{len(d)} of {N} slots differ')
for k in d:
    print(f'  [{k:2d}] +{4*k:#05x} {NAMES[k]:26s} Stunned={D.nearest(stn[k])}')
    print(f'                                    Immobilized={D.nearest(imm[k])}')
    print(f'        Stunned body     : {lines(stn[k],5)}')
    print(f'        Immobilized body : {lines(imm[k],5)}')
