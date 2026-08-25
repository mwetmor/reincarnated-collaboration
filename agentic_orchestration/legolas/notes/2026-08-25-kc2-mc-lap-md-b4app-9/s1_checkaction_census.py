"""MD-B4app-9 step 1 — census every symbol named CheckAction / HandleAction / MoveTo across the
image, and every vtable in .rdata that installs any of them.  READ-ONLY.
Purpose: answer 'is CheckAction overridden anywhere on the controller hierarchy?' by ENUMERATION
rather than by assuming ControllerBaseCharacter's slot is the one that runs."""
import sys, re, struct; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base

print('=== A. every export whose name contains CheckAction ===')
for n,r in sorted(((n,r) for n,r in D.EX.items() if 'CheckAction' in n), key=lambda t:t[1]):
    print(f'  {r:#010x}  {n}')

print()
print('=== B. every export whose name contains HandleAction ===')
for n,r in sorted(((n,r) for n,r in D.EX.items() if 'HandleAction' in n), key=lambda t:t[1]):
    print(f'  {r:#010x}  {n}')

print()
print('=== C. every ??_7Controller* vtable, slot +0x68 ===')
vts=sorted(n for n in D.EX if n.startswith('??_7Controller'))
for c in vts:
    v=D.EX[c]
    b=pe.at(v+0x68,4)
    if not b or len(b)<4:
        print(f'  {c:70s} @ {v:#010x}  +0x68 UNREADABLE'); continue
    t=struct.unpack_from('<I',b,0)[0]-IB
    print(f'  {c:70s} @ {v:#010x}  +0x68 -> {t:#010x}  {D.nearest(t)}')
