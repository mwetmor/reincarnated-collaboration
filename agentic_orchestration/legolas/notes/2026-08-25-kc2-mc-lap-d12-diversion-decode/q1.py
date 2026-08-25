import sys, importlib.util
spec=importlib.util.spec_from_file_location('arzlib','/tmp/d12/pm4t_arz_2026_08_14.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
C=m.Corpus()
recs=['records/skills/playerclass09/pets/celestialguardian_02.dbr',
      'records/skills/playerclass09/pets/celestialguardian_01.dbr',
      'records/skills/itemskillsgdx1/pets/itempet_deathstalker_a01.dbr']
FIELDS=['causesAnger','angerMultiplier','invincible','Class','templateName','monsterClassification','factions','controllerTemplate','controller']
for r in recs:
    if not C.has(r): print('=== MISSING',r); continue
    rec=C.read(r)
    print('===',r,'| layers:',C.layers(r),'| type:',C.record_type(r))
    for f in FIELDS:
        print('   %-24s %r'%(f, rec.get(f,'<ABSENT>')))
    # any anger-ish key
    print('   anger-keys:', {k:v for k,v in rec.items() if 'nger' in k or 'Pet' in k or 'pet' in k})
