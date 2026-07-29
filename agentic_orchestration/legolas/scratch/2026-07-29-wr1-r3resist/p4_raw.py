import sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import get
for r in ['records/items/gearshoulders/a03_shoulder01.dbr','records/items/gearlegs/a02_legs01.dbr',
          'records/items/gearfeet/a02_feet02.dbr','records/items/geartorso/a02_torso002.dbr',
          'records/items/gearaccessories/waist/a02_waist001.dbr','records/items/gearhead/a03_head002.dbr',
          'records/items/gearhands/a02_hands01.dbr',
          'records/items/lootaffixes/suffix/b_ar002_ar.dbr','records/items/lootaffixes/prefix/b_ar104_ar_a.dbr',
          'records/items/lootaffixes/prefix/b_ar030_ar.dbr','records/items/lootaffixes/suffix/a029e_off_dmg%cold_01_ar.dbr']:
    p,rt,f=get(r)
    print('='*90); print(r,'|',p,'|',rt)
    for k in sorted(f):
        v=f[k]
        if v in (0,0.0,'',None): continue
        if isinstance(v,list) and not any(v): continue
        print('   ',k,'=',v)
