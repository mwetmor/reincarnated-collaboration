import json,sys,collections
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
G='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/gear_resolved.json'
N='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/gear_named.json'
d=json.load(open(G)); nm={(x['group'],x['slot']):x['name'] for x in json.load(open(N))}
RES=['defensiveFire','defensiveCold','defensiveLightning','defensivePoison','defensivePierce',
     'defensivePhysical','defensiveBleeding','defensiveLife','defensiveAether','defensiveChaos',
     'defensiveElementalResistance','defensiveAllResistance','defensiveTotalSpeedResistance']
CC=['defensiveStun','defensiveFreeze','defensiveSleep','defensivePetrify','defensiveTrap','defensiveKnockdown',
    'defensiveConfusion','defensiveFear','defensiveDisruption','defensiveManaBurn','defensiveSlowLifeLeach',
    'defensiveReflect','defensiveConvert','defensiveCrowdControl','defensivePercentCurrentLife','defensiveBonusProtection']
MAXR=['defensiveFireMaxResist','defensiveColdMaxResist','defensiveLightningMaxResist','defensivePoisonMaxResist',
      'defensivePierceMaxResist','defensivePhysicalMaxResist','defensiveBleedingMaxResist','defensiveLifeMaxResist',
      'defensiveAetherMaxResist','defensiveChaosMaxResist','defensiveAllMaxResist','defensiveFreezeMaxResist',
      'defensiveSlowLifeLeachMaxResist','defensiveCrowdControlMaxResist','defensivePetrifyMaxResist']
ARM=['defensiveProtection','defensiveProtectionModifier','defensiveAbsorption','defensiveAbsorptionModifier']
CONV=['conversionInType','conversionOutType','conversionPercentage']
tot=collections.defaultdict(float); rows=[]
for it in d:
    key=(it['group'],it['slot']); label=nm.get(key,'?')
    for part in ('baseName','prefixName','suffixName','componentName','augmentName'):
        node=it.get(part);
        if not node: continue
        r=node['record'];
        if not r: continue
        p,rt,f=get(r)
        jit=f.get('lootRandomizerJitter')
        for k in RES+CC+MAXR+ARM:
            v=f.get(k)
            if v in (None,0,0.0): continue
            rows.append((label,key,part,r,p,k,v,jit))
            if k in RES+CC: tot[k]+=v
        if f.get('conversionPercentage'):
            rows.append((label,key,part,r,p,f'CONVERSION {f["conversionInType"]}->{f["conversionOutType"]}',f['conversionPercentage'],jit))
print(f"{'item':46s} {'part':10s} {'field':32s} {'val':>7s} {'jit':>5s}  record")
for label,key,part,r,p,k,v,jit in rows:
    print(f"{label[:45]:46s} {part[:9]:10s} {k:32s} {v:7.2f} {('' if jit is None else f'{jit:.0f}'):>5s}  {r}")
print()
print('=== SUMMED (nominal, .arz exact-original) ===')
for k,v in sorted(tot.items()): print(f'   {k:32s} {v:7.2f}')
