"""D-8 step 21 — decode the byte flag at Skill_AttackRadiusSpin + 0x4f4 that gates the whole
passive-defence contribution (and therefore EoR's defensiveCrowdControl).  Disassemble every
method of the class and record every read/write of [reg+0x4f4].  READ-ONLY."""
import sys, re; sys.path.insert(0,'.')
import d4b_dis as D
METH={'IsRunning':0x003ebc10,'StartAction':0x003eba30,'EndAction':0x003ebb70,
      'StopSpinning':0x003eb930,'StopSkill':0x003e8df0,'Update':0x003eb410,
      'Load':0x003eaed0,'ActivateNow':0x003eb250,'GetAllowMove':0x003ebc30,
      'CanInterrupt':0x003e96e0,'GetWarmUpWasActive':0x003e96f0,
      'CollectPassiveCharAttributes':0x003ebc70,
      'CollectPassiveRetaliationAttributes':0x003ebd00,
      'ApplyCastVisualEffects':0x003eb010,'StartMove':0x003ebc50,
      'ctor':0x003eab40}
PAT=re.compile(r'\[\w+ \+ 0x4f4\]')
for nm,rva in METH.items():
    ls=D.disasm(rva,400,stop_at_ret=False)
    hits=[l for l in ls if PAT.search(l)]
    print(f'=== {nm} @ {rva:#010x}  ({len(hits)} touches of +0x4f4)')
    for h in hits: print('   ',h.strip())
print()
print('=== IsRunning / GetAllowMove / CanInterrupt full bodies ===')
for nm in ('IsRunning','GetAllowMove','CanInterrupt','GetWarmUpWasActive','StartMove'):
    print(f'--- {nm}')
    for l in D.disasm(METH[nm],14,stop_at_ret=True): print(l)
