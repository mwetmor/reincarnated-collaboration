import sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
def R(p):
    _,_,f=get(p); return f
def arr(v,rank):
    if isinstance(v,list): return v[min(max(int(rank)-1,0),len(v)-1)]
    return v
cl=13
# --- Primordian bio
b=R('records/creatures/enemies/bios/bio_boss_standard_01.dbr')
ev=lambda e: eval(e.replace('^','**'),{'__builtins__':{}},{'charLevel':float(cl)})
print('bio @cl13:',{k:round(ev(b[k]),2) for k in ('characterLife','characterStrength','characterDexterity','characterOffensiveAbility','characterDefensiveAbility')})
pak=R('records/game/balancingadjustment_mp+difficulty_enemies01.dbr')
P=lambda k: (pak[k][0] if isinstance(pak.get(k),list) else pak.get(k,0)) or 0
dex=ev(b['characterDexterity'])*(1+P('characterDexterityModifier')/100)
stre=ev(b['characterStrength'])*(1+P('characterStrengthModifier')/100)
OA=(ev(b['characterOffensiveAbility'])+P('characterOffensiveAbility')+cl*12+dex*0.5)*(1+P('characterOffensiveAbilityModifier')/100)+53
DA=(ev(b['characterDefensiveAbility'])+P('characterDefensiveAbility')+cl*12+stre*0.5)*(1+P('characterDefensiveAbilityModifier')/100)+53
print(f'Primordian @cl13  OA={OA:.1f} DA={DA:.1f} dex={dex:.1f} str={stre:.1f}')
ab5=R('records/skills/nonplayerskills/passive/armorbase05.dbr')
print('armorbase05 r13: TDM=',arr(ab5['offensiveTotalDamageModifier'],13),' armor=',arr(ab5['defensiveProtection'],13),' lifeMod=',arr(ab5['characterLifeModifier'],13))
dta=R('records/skills/nonplayerskills/passive/damage_totaladjuster.dbr')
print('damage_totaladjuster rank int(13/25+2)=',int(13/25+2),'TDM=',arr(dta['offensiveTotalDamageModifier'],int(13/25+2)))
print('pak: TDM=',P('offensiveTotalDamageModifier'),' aspdMod=',P('characterAttackSpeedModifier'),' absorbMod=',P('defensiveAbsorptionModifier'),' DA=',P('characterDefensiveAbility'),P('characterDefensiveAbilityModifier'))
# frigidring rank 4
fr=R('records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr')
rk=int(cl/4+1)
print(f'\nfrigidring rank={rk} (skillLevel7=charLevel/4+1 @cl{cl})')
for k in ('offensivePhysicalMin','offensiveColdMin','offensiveFreezeMin','offensiveFreezeMax','offensiveSlowColdMin','skillManaCost'):
    print('   ',k,'=',arr(fr[k],rk))
print('    offensiveSlowColdDurationMin =',fr['offensiveSlowColdDurationMin'])
wv=R('records/skills/nonplayerskills/bossskills/primordian_wave.dbr')
print('wave rank',rk,{k:arr(wv[k],rk) for k in ('offensivePhysicalMin','offensiveColdMin','offensiveSlowColdMin','offensiveSlowDamageMultMin') if k in wv})
bz=R('records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr')
print('blizzard rank',rk,{k:arr(bz[k],rk) for k in ('offensivePhysicalMin','offensiveColdMin','offensiveSlowTotalSpeedMin') if k in bz})
ia=R('records/skills/nonplayerskills/bossskills/primordian_icearmor.dbr')
print('icearmor rank',rk,{k:arr(ia[k],rk) for k in ('damageAbsorptionPercent','characterAttackSpeedModifier','offensiveColdModifier','retaliationSlowColdMin') if k in ia})
# opposition attack speeds
print('\n--- opposition characterAttackSpeed (raw / after pak -10%)')
for p in ['records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr','records/creatures/enemies/slitha_melee_b01.dbr','records/creatures/enemies/slitha_shaman_c01.dbr','records/creatures/enemies/zombie_a01.dbr','records/creatures/enemies/trollhalfswamp_a02.dbr','records/creatures/enemies/boss&quest/warden01.dbr','records/creatures/enemies/hero/boar_h01.dbr']:
    f=R(p)
    if not f: print('  MISSING',p); continue
    a=f.get('characterAttackSpeed',1.0); s=f.get('characterSpellCastSpeed')
    print(f"  {p.split('/')[-1]:34s} aspd={a:.2f} -> {a*(1+P('characterAttackSpeedModifier')/100):.3f}  cast={s}  tag={f.get('characterBaseAttackSpeedTag')}")
