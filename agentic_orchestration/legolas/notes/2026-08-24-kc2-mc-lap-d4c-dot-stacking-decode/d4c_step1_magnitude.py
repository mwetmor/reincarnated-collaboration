"""D-4c STEP 1 — locate `damageMagnitude` (GameEngine::LoadFromDatabase @0x2579f2 reads it into
gGameEngine+0x292d4, the vector<float> exposed as GameEngine::GetDurationDamageV()).
READ-ONLY on every vendor path."""
import sys, pathlib; sys.path.insert(0, '.')
from d4b_lib import ArzArchive, VENDOR_FULL, VENDOR_E3

for tag, root in (('FULL v1.2.3.4', VENDOR_FULL), ('ED-III 20260808', VENDOR_E3)):
    for arz in sorted(root.rglob('*.arz')):
        try:
            a = ArzArchive(arz)
        except Exception as e:
            print(f'  !! {arz}: {e}'); continue
        hits = []
        for rp in a.records:
            if 'gameengine' in rp.lower() or rp.lower().endswith('game/game.dbr'):
                hits.append(rp)
        for rp in hits:
            try: rec = a.read_record(rp)
            except Exception as e: print(f'   !! {rp}: {e}'); continue
            if 'damageMagnitude' in rec:
                print(f'[{tag}] {arz.relative_to(root)}  ::  {rp}   (type={a.record_type(rp)})')
                print(f'    damageMagnitude = {rec["damageMagnitude"]!r}')
                for k in sorted(rec):
                    if 'agnitude' in k or 'uration' in k.lower():
                        print(f'      {k} = {rec[k]!r}')
