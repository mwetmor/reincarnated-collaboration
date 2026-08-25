import sys, importlib.util, csv, json, hashlib, pathlib, collections
sys.path.insert(0,'/tmp/d12')
import d4b_dis as D, d8_lib as L
OUT=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-25-kc2-mc-lap-d12-diversion-decode')
EV=OUT/'evidence'

def dump(name, rva, n=400, stop=None):
    lines=L.bounded(rva,n)
    if stop is not None:
        lines=[l for l in lines if int(l.split()[0],16)<stop]
    (EV/name).write_text('\n'.join(lines)+'\n')
    return len(lines)

targets = {
 'step01_UnderAttack_ControllerMonster.txt': (0xfc350, 400, None),
 'step02_AddAnger_AngerManager.txt': (0xf6a0, 300, None),
 'step03_ShouldRemoveEnemy_AngerManager.txt': (0xfff0, 200, 0x100f0),
 'step04_GetNewTarget_AngerManager.txt': (0xf850, 400, None),
 'step05_HasOnlyPetTargets.txt': (0xfb70, 200, None),
 'step06_ShouldIgnorePets.txt': (0xfb650, 40, None),
 'step07_FindEnemy_ControllerMonster.txt': (0xfb670, 200, None),
 'step08_GetMostHatedEnemy_ControllerMonster.txt': (0xfb9c0, 200, None),
 'step09_GetAnger_GetAngerMultiplier_CausesAnger.txt': (0xf330, 60, None),
 'step10_TauntMe_ControllerMonster.txt': (0xf9c80, 60, None),
 'step11_TransferAnger_family.txt': (0xfe20, 60, None),
}
for k,(r,n,s) in targets.items():
    print(k, dump(k,r,n,s))

# raw disasm windows (unbounded regions inside big functions)
def window(name, start, end):
    out=[]
    for l in D.disasm(start, 400, stop_at_ret=False):
        a=int(l.split()[0],16)
        if a>=end: break
        out.append(l)
    (EV/name).write_text('\n'.join(out)+'\n'); return len(out)

print('step12', window('step12_Load_ControllerMonster_PetBehaviour_parse.txt', 0xf79e0, 0xf7ac0))
print('step13', window('step13_Load_ControllerMonster_Anger_parse.txt', 0xf7770, 0xf77f0))
print('step14', window('step14_Update_ControllerMonster_ignorePets_roll.txt', 0xf6330, 0xf63a5))
print('step15', window('step15_Update_ControllerMonster_RandomAnger.txt', 0xf6660, 0xf6730))
print('step16', window('step16_anger_comparator_default.txt', 0x10110, 0x10180))
print('step17', window('step17_anger_comparator_distance.txt', 0x10180, 0x101b0))
