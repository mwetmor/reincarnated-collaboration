import csv, collections, importlib.util
spec=importlib.util.spec_from_file_location('arzlib','/tmp/d12/pm4t_arz_2026_08_14.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
C=m.Corpus()
rows=list(csv.DictReader(open('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d3-controller-groups/d3_roster_controller_params.csv')))
ctrls=sorted({r['controller'] for r in rows})
print('controllers:',len(ctrls))
tal=collections.defaultdict(collections.Counter)
FIELDS=['AngerTolerance','AttackedAnger','AllyAttackedAnger','petAngerTransference','ignorePetsChance','ignorePetsInterval','RandomAngerChance']
missing=0
for c in ctrls:
    if not C.has(c): missing+=1; continue
    rec=C.read(c)
    for f in FIELDS: tal[f][rec.get(f,'<DEFAULT/ABSENT>')]+=1
print('missing controllers:',missing)
for f in FIELDS: print('%-24s %s'%(f, dict(tal[f])))
# player pet stance controllers
print()
for c in ['records/controllers/pets/controller_celestialguardian_aggressive.dbr',
          'records/controllers/pets/controller_hellhound_normal.dbr']:
    rec=C.read(c)
    print(c, {f:rec.get(f,'<ABSENT>') for f in FIELDS})
