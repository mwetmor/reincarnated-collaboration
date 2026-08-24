"""STEP 3 — locate the .dbr record carrying magicalDurationDamageEquation / physicalDurationDamageEquation.
Game.dll's CombatManager loads these by name (debug string: '-=- Combat Manager Equation load failure :
magicalDurationDamageEquation'), so the equation TEXT is data in the .arz, not code."""
import sys; sys.path.insert(0,'.')
from d4b_lib import *
KEYS = {'magicalDurationDamageEquation','physicalDurationDamageEquation'}
for arzname, arz in [('database.arz', VENDOR_E3/'database'/'database.arz')]:
    a = ArzArchive(arz)
    print(f'{arzname}: {a.rt_count} records, {len(a.strings)} strings')
    # the field name must be in the string table if any record uses it
    present = KEYS & set(a.strings)
    print('  keys present in string table:', present)
    # candidate records: paths mentioning combat/game
    cands = [p for p in a.records if 'combat' in p.lower() or p.startswith('records/game/')]
    print(f'  candidate record paths: {len(cands)}')
    hits=[]
    for p in cands:
        try: rec = a.read_record(p)
        except Exception: continue
        if KEYS & set(rec): hits.append((p, rec))
    print('  HITS:', [h[0] for h in hits])
    for p, rec in hits:
        print(f'\n--- {p}  (type={a.record_type(p)}) ---')
        for k in sorted(rec):
            if 'uration' in k or 'quation' in k: print(f'    {k} = {rec[k]!r}')
