import json,sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
KEYS=['defensiveProtection','defensiveProtectionModifier','defensiveProtectionChance',
 'defensiveAbsorption','defensiveAbsorptionModifier','defensiveBlock','blockAbsorption','blockRecoveryTime',
 'defensiveDodge','defensiveProjectile','defensiveBlockChance','defensiveBlockModifier',
 'characterDefensiveAbility','characterDefensiveAbilityModifier','characterOffensiveAbility',
 'characterAttackSpeedModifier','characterBaseAttackSpeed','characterAttackSpeed',
 'defensiveCold','defensiveFreeze','defensivePhysical','defensiveSlowColdModifier',
 'characterLife','characterLifeModifier','lootRandomizerJitter','itemLevel','levelRequirement',
 'itemSkillName','augmentSkillName1']
d=json.load(open('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/gear_resolved.json'))
for it in d:
    if it['group']!='equipment': continue
    print(f"--- slot {it['slot']}")
    for part in ('baseName','prefixName','suffixName','componentName','augmentName'):
        r=it[part]['record']
        if not r: continue
        p,rt,f=get(r)
        if f is None: print(f"   {part}: {r}  NOT FOUND"); continue
        hits={k:f[k] for k in KEYS if k in f and f[k] not in (0,0.0,'')}
        print(f"   {part}: {r} [{rt}]  {hits}")
