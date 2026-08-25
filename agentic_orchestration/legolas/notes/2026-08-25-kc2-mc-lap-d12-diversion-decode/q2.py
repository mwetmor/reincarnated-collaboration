import importlib.util, collections
spec=importlib.util.spec_from_file_location('arzlib','/tmp/d12/pm4t_arz_2026_08_14.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
C=m.Corpus()
tally=collections.Counter(); mult=collections.Counter(); byclass=collections.Counter()
examples=collections.defaultdict(list)
n=0
for p in C.paths():
    try:
        t=C.record_type(p)
    except Exception: continue
    if t!='PetPlayerScaling': continue
    try: rec=C.read(p)
    except Exception: continue
    n+=1
    ca=rec.get('causesAnger','<ABSENT>'); am=rec.get('angerMultiplier','<ABSENT>')
    tally[ca]+=1; mult[am]+=1
    examples[(ca,am)].append(p)
print('PetPlayerScaling records:',n)
print('causesAnger:',dict(tally))
print('angerMultiplier:',dict(mult))
for k,v in examples.items():
    print(k, len(v), v[:6])
