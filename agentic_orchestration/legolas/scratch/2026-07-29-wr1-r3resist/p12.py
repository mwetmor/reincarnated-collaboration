import sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
for r in ['records/items/gearaccessories/necklaces/b001_necklace.dbr',
          'records/items/gearweapons/blunt1h/b015b_blunt.dbr',
          'records/items/gearweapons/shields/b013a_shield.dbr',
          'records/items/lootaffixes/prefix/ao006b_poison_02.dbr',
          'records/items/lootaffixes/suffix/a032c_off_dmg%acid_01_we.dbr',
          'records/items/lootaffixes/suffix/b_ar103_ar_a.dbr',
          'records/items/lootaffixes/prefix/b_ar022_ar.dbr',
          'records/items/lootaffixes/suffix/b_ar014_arje.dbr']:
    p,rt,f=get(r)
    print('='*90); print(r,'|',p,'|',rt)
    for k in sorted(f):
        v=f[k]
        if v in (0,0.0,'',None): continue
        if isinstance(v,list) and not any(v): continue
        if isinstance(v,str) and ('.tex' in v or '.msh' in v or 'sounds/' in v): continue
        if k in ('actorHeight','actorRadius','castsShadows','maxTransparency','outlineThickness','physicsFriction','physicsMass','scale','templateName','itemCostName','characterBaseAttackSpeedTag','marketAdjustmentPercent','lootRandomizerCost'): continue
        print('   ',k,'=',v)
