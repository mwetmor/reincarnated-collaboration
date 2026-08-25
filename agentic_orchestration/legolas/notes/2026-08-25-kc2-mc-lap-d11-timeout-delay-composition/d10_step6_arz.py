"""D-10 step 6 — read the two armed-row carrier records straight out of the `.arz`, so every
DBR field the two decoded consumers read is MEASURED at its source rather than inherited from
`pm2_tg2_attack_damage.csv`'s projection.  Reuses the TQIT reader banked at
`research/scripts/gd_arz_adapter_2026_07_24.py` (ArzArchive) verbatim.  READ-ONLY.

Usage: python3 d10_step6_arz.py <archive-key> <record-path> [<record-path> ...]
"""
import sys, pathlib, hashlib
sys.path.insert(0, str(pathlib.Path.home() / 'Games/reincarnated-collaboration/agentic_orchestration/research/scripts'))
import importlib.util

SPEC = pathlib.Path.home() / 'Games/reincarnated-collaboration/agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py'
spec = importlib.util.spec_from_file_location('gd_arz_adapter', SPEC)
mod = importlib.util.module_from_spec(spec)
sys.modules['gd_arz_adapter'] = mod
spec.loader.exec_module(mod)

ARCHIVES = {
    'base': '~/Games/vendor/grim-dawn/database/database.arz',
    'gdx1': '~/Games/vendor/grim-dawn/gdx1/database/GDX1.arz',
    'gdx2': '~/Games/vendor/grim-dawn/gdx2/database/GDX2.arz',
    'sm1': '~/Games/vendor/grim-dawn/survivalmode1/database/SurvivalMode1.arz',
    'sm2': '~/Games/vendor/grim-dawn/survivalmode2/database/SurvivalMode2.arz',
}

key = sys.argv[1]
p = pathlib.Path(ARCHIVES[key]).expanduser()
print(f'=== archive {key}: {p}')
print(f'    sha256 {hashlib.sha256(p.read_bytes()).hexdigest()}')
a = mod.ArzArchive(p)
print(f'    records {len(a.records)}  strings {len(a.strings)}')
for rp in sys.argv[2:]:
    print(f'\n--- {rp}')
    if rp not in a.records:
        print('    NOT IN ARCHIVE')
        continue
    print(f'    rtype={a.record_type(rp)}')
    rec = a.read_record(rp)
    for k in sorted(rec):
        v = rec[k]
        if isinstance(v, list):
            v = '[' + ', '.join(f'{x:g}' if isinstance(x, float) else str(x) for x in v) + f']  (n={len(rec[k])})'
        print(f'    {k:44s} {v}')
