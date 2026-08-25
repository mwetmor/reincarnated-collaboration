import importlib.util, collections, re
spec=importlib.util.spec_from_file_location('arzlib','/tmp/d12/pm4t_arz_2026_08_14.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
C=m.Corpus()
stems=collections.Counter()
for p in C.paths():
    try:
        if C.record_type(p)!='PetPlayerScaling': continue
        rec=C.read(p)
    except Exception: continue
    if rec.get('causesAnger') is True:
        stems[re.sub(r'\d+(?=\.dbr$)','NN',p.rsplit('/',1)[1])]+=1
print('causesAnger=True stems:', dict(stems))
print()
# look for famous pets
for kw in ['briarthorn','hellhound','blightfiend','raven','guardianofempyrion','celestialguardian','skeleton','wolves','familiar','wendigo','manticore','golem','stormtotem','bloodofdreeg']:
    hits=[p for p in C.paths() if kw in p and '/pets/' in p]
    if not hits: continue
    p=sorted(hits)[len(hits)//2]
    rec=C.read(p)
    print('%-22s %-70s type=%-18s causesAnger=%s angerMult=%s invincible=%s'%(kw,p,C.record_type(p),rec.get('causesAnger'),rec.get('angerMultiplier'),rec.get('invincible')))
