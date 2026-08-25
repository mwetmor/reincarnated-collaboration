"""MD-B4app-9 step 7 — DERIVE (not assert) the permission that ControllerBaseCharacter::CheckAction
returns on the monster limb, by executing the decoded 0xea347 branch as a small interpreter over
(lifeState, newActionType, currentActionType).  Each transition below is annotated with the RVA of
the instruction that produces it; if the listing ever changes, the RVAs stop matching and this
table must be rebuilt rather than trusted.  READ-ONLY."""
import sys, json; sys.path.insert(0,'.')

LIFE = {0:'Unknown', 1:'Initializing', 2:'Alive', 3:'Dying', 4:'Dead', 5:'Respawning'}
PERM = {0:'0 REPLACE', 1:'1 PENDING', 2:'2 REJECT', 3:'3 DEFER', 4:'4 INTERRUPT-THEN-REPLACE'}
DIE, RESPAWN = 0x0f, 0x14

def monster_limb(life, new_t, cur_t):
    """cur_t = None when the handler holds no current action."""
    # 0xea35d  test esi,esi / je 0xea39d      -- controlled entity not a Character
    if life is None:
        return 2, 'ea39d: controlled entity is not a Character'
    # 0xea365  call [Character +0x21c] = GetLifeState ; 0xea36b cmp eax,4
    if life == 4:                                    # Dead
        if new_t != RESPAWN:
            return 2, 'ea373: Dead and new-action is not RespawnAction(20)'
        # 0xea375 cmp edi,0xf -> 0x14 != 0xf -> jne 0xea2b6
        return 0, 'ea378: Dead + RespawnAction(20)'
    if life == 3:                                    # 0xea3ab cmp eax,3   Dying
        if new_t != DIE:
            return 2, 'ea3b5: Dying and new-action is not DieAction(15)'
        return _die_tail(cur_t, 'Dying')
    # 0xea3ae jne 0xea375 : lifeState in {Unknown, Initializing, Alive, Respawning}
    if new_t != DIE:
        return 0, f'ea378: {LIFE[life]} + non-Die action -> unconditional REPLACE'
    return _die_tail(cur_t, LIFE[life])

def _die_tail(cur_t, life_label):
    # 0xea37e/0xea389: no current action -> 0xea2b6 REPLACE
    if cur_t is None:
        return 0, 'ea389: DieAction with no current action'
    # 0xea394 cmp eax,0xf / jne 0xea2b6
    if cur_t == DIE:
        return 2, 'ea397->ea39d: DieAction over a DieAction'
    return 0, f'ea397: {life_label} + DieAction over non-Die current action'

print('=== permission returned by CBC::CheckAction (0xea260) on the MONSTER limb ===')
print('    (as-Player downcast NULL => 0xea28c always taken => matrix at 0xea310 unreachable)')
print()
hdr = f'{"lifeState":>14s} | {"new action":>28s} | {"cur action":>12s} | permission'
print(hdr); print('-'*len(hdr))
CASES = [(l, n, c) for l in (2, 1, 3, 4)
                   for n, c in ((4, 19), (4, None), (18, 4), (18, 19), (15, 4), (15, 15), (20, 19))]
NAMES = {4:'4 MoveToAction', 18:'18 PlayAnimationAction', 15:'15 DieAction',
         19:'19 SpawnAction', 20:'20 RespawnAction', None:'<none>'}
rows = []
for l, n, c in CASES:
    p, why = monster_limb(l, n, c)
    rows.append(dict(lifeState=LIFE[l], new=NAMES[n], cur=NAMES[c], permission=PERM[p], why=why))
    print(f'{LIFE[l]:>14s} | {NAMES[n]:>28s} | {NAMES[c]:>12s} | {PERM[p]}    [{why}]')
json.dump(rows, open('evidence/14-monster-permission-table.json','w'), indent=1)

print()
print('=== THE TWO CELLS THIS LAP WAS COMMISSIONED ON ===')
for l in (0,1,2,5):
    p,_ = monster_limb(l, 4, 19)
    q,_ = monster_limb(l, 18, 4)
    print(f'  lifeState={LIFE[l]:>12s}:  pursue MoveTo(4) over SpawnAction(19) -> {PERM[p]}'
          f'   |  alert PlayAnimation(18) over MoveTo(4) -> {PERM[q]}')
print()
print('  INVARIANT over all four non-terminal lifeStates.  Dying(3)/Dead(4) are excluded by the')
print('  measurement itself: the closures fired and the bodies pursued, which a Dying/Dead body')
print('  cannot do (both would REJECT the MoveTo outright).')
