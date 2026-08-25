"""MD-B4app-9 step 6 — CONTROL-FLOW PROOF, not eyeballing.
Build the intra-procedural CFG of ControllerBaseCharacter::CheckAction (0xea260) from the decoded
branch edges, then ask: with the single edge 0xea28c --taken--> 0xea347 REMOVED (i.e. assuming the
as-Player downcast returned NULL, so the je IS taken and the fallthrough is impossible), is the
matrix-read instruction at 0xea310 still reachable from the entry?

If it is NOT reachable, the 26x26 permission matrix is unreachable for any controller whose
controlled entity is not a Player.  HALTs if the listing shape is not what the model expects.
READ-ONLY."""
import sys, re; sys.path.insert(0,'.')
import d4b_dis as D
import d8_lib as B

LO, HI = 0x000ea260, 0x000ea3c3
MATRIX = 0x000ea310          # mov eax,[eax+ecx*4+0x2802c]
PLAYER_JE = 0x000ea28c       # je 0x100ea347   (taken when as-Player == NULL)

lines = [l for l in B.bounded(LO, 400) if LO <= int(l.split()[0],16) < HI]
assert lines, 'HALT: no listing'
recs = []
for l in lines:
    p = l.split(None, 2)
    rva = int(p[0], 16); mn = p[1]
    ops = (p[2].split(';')[0].strip() if len(p) > 2 else '')   # strip the harness' '; -> sym' annotation
    recs.append((rva, mn, ops))
addrs = [r[0] for r in recs]
nxt = {addrs[i]: (addrs[i+1] if i+1 < len(addrs) else None) for i in range(len(addrs))}

UNCOND = {'jmp'}
RET    = {'ret', 'retn'}
edges = {}
for rva, mn, ops in recs:
    e = []
    m = re.match(r'^0x([0-9a-f]+)\s*$', ops)
    tgt = int(m.group(1), 16) - D.pe.image_base if m else None
    if mn in RET:
        pass
    elif mn in UNCOND:
        if tgt is None: raise SystemExit(f'HALT: indirect jmp at {rva:#x} — CFG not modelled')
        e.append(('jmp', tgt))
    elif mn.startswith('j'):
        if tgt is None: raise SystemExit(f'HALT: indirect cond-branch at {rva:#x}')
        e.append(('taken', tgt)); e.append(('fall', nxt[rva]))
    elif mn == 'int3':
        pass
    else:
        e.append(('fall', nxt[rva]))
    edges[rva] = [(k, t) for k, t in e if t is not None]

assert any(k == 'taken' and t == 0x000ea347 for k, t in edges[PLAYER_JE]), \
    'HALT: 0xea28c is not the je -> 0xea347 the model assumes'

def reach(cut_fallthrough_of=None):
    seen, stack = set(), [LO]
    while stack:
        a = stack.pop()
        if a in seen or a not in edges: continue
        seen.add(a)
        for kind, t in edges[a]:
            if a == cut_fallthrough_of and kind == 'fall':
                continue          # as-Player == NULL  =>  the je is ALWAYS taken
            stack.append(t)
    return seen

full = reach()
cut  = reach(cut_fallthrough_of=PLAYER_JE)
print(f'instructions in body                     : {len(recs)}')
print(f'reachable, no assumption                 : {len(full)}   matrix@{MATRIX:#x} reachable = {MATRIX in full}')
print(f'reachable, as-Player==NULL (monster)     : {len(cut)}   matrix@{MATRIX:#x} reachable = {MATRIX in cut}')
print()
print('--- instructions reachable ONLY when the controlled entity IS-A Player ---')
for rva, mn, ops in recs:
    if rva in full and rva not in cut:
        print(f'  {rva:#010x}  {mn:8s} {ops}')
print()
print('--- the monster-reachable body (as-Player == NULL) ---')
for rva, mn, ops in recs:
    if rva in cut:
        print(f'  {rva:#010x}  {mn:8s} {ops}')
