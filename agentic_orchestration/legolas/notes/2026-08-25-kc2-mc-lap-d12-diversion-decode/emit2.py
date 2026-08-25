import importlib.util, csv, json, hashlib, pathlib, collections, re
spec=importlib.util.spec_from_file_location('arzlib','/tmp/d12/pm4t_arz_2026_08_14.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
C=m.Corpus()
OUT=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-25-kc2-mc-lap-d12-diversion-decode')

# ---- 1. summon-side threat eligibility census over every player-summonable body ----
rows=[]
for p in sorted(C.paths()):
    try: t=C.record_type(p)
    except Exception: continue
    if t not in ('PetPlayerScaling','Pet'): continue
    try: rec=C.read(p)
    except Exception: continue
    rows.append(dict(
        record=p, arz_owners='|'.join(C.layers(p)), record_class=t,
        causes_anger=rec.get('causesAnger'), anger_multiplier=rec.get('angerMultiplier'),
        invincible=rec.get('invincible'), controller=rec.get('controller'),
        monster_classification=rec.get('monsterClassification'),
        threat_table_eligible=(rec.get('causesAnger') is True),
        divertible=(rec.get('causesAnger') is True and (rec.get('angerMultiplier') or 0) > 0),
        grade='DECODED', source='ARZ field read; gate = ShouldRemoveEnemy@AngerManager 0x0000fff0 (+0x38 CausesAnger vslot 0x428)'))
with (OUT/'d12_summon_threat_eligibility.csv').open('w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
cen=collections.Counter((r['record_class'], r['causes_anger'], r['anger_multiplier']) for r in rows)
print('rows',len(rows)); [print(k,v) for k,v in sorted(cen.items(), key=lambda x:-x[1])]

# ---- 2. per-controller anger parameters for the 77 roster controllers ----
d3=list(csv.DictReader(open('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d3-controller-groups/d3_roster_controller_params.csv')))
nmon={}
for r in d3: nmon[r['controller']]=r.get('n_monsters')
FIELDS=['AngerTolerance','AttackedAnger','AllyAttackedAnger','petAngerTransference','ignorePetsChance','ignorePetsInterval','RandomAngerChance','RandomAngerEvaluationTime','ClearAngerWhenFleeing']
SLOT={'AngerTolerance':'+0x294','AttackedAnger':'+0x298','AllyAttackedAnger':'+0x29c','petAngerTransference':'+0x57c (int x 0.01 -> float)','ignorePetsChance':'+0x56c','ignorePetsInterval':'+0x570','RandomAngerChance':'+0x390','RandomAngerEvaluationTime':'+0x504','ClearAngerWhenFleeing':'+0x31c'}
out=[]
for c in sorted(nmon):
    rec=C.read(c)
    row={'controller':c,'n_monsters':nmon[c],'arz_owners':'|'.join(C.layers(c))}
    for f in FIELDS:
        row[f]=rec.get(f,'')
        row[f+'_slot']=SLOT[f]
    row['transference_fraction_t']= (rec.get('petAngerTransference') or 0)/100.0
    row['pet_leg_anger']= round((1-row['transference_fraction_t'])*(rec.get('AttackedAnger') or 0),4)
    row['owner_leg_anger']= round(row['transference_fraction_t']*(rec.get('AttackedAnger') or 0),4)
    out.append(row)
with (OUT/'d12_roster_anger_parameters.csv').open('w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print('controllers',len(out))
for f in FIELDS:
    print('%-26s %s'%(f, dict(collections.Counter(r[f] for r in out))))

# ---- digests ----
dig={}
for p in ['/Users/admin/Games/vendor/grim-dawn/Game.dll',
 '/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/database/database.arz',
 '/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/gdx1/database/GDX1.arz',
 '/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/gdx2/database/GDX2.arz',
 '/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/gdx3/database/GDX3.arz']:
    dig[p]=hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
prod={}
for f in sorted(OUT.rglob('*')):
    if f.is_file() and f.name!='d12_digests.json':
        prod[str(f.relative_to(OUT))]=hashlib.sha256(f.read_bytes()).hexdigest()
(OUT/'d12_digests.json').write_text(json.dumps({'substrate':dig,'products':prod},indent=2)+'\n')
print('digests written')
