"""B1 target-selection decode — read DBR records straight out of the `.arz` overlay.

Reuses the TQIT reader banked at `research/scripts/gd_arz_adapter_2026_07_24.py` (ArzArchive)
verbatim — the lane was established 2026-07-23 and is not re-derived here.  READ-ONLY: no
write path exists in this script or in the adapter.

Edition of record for the KC2 referent window (fight 2026-08-05) is **Edition III**
(`grim-dawn-edition-III-20260808`, intake note 2026-08-08).  Edition I (`vendor/grim-dawn/`,
2026-07-23) is read alongside so that any field drift across the referent window is VISIBLE
rather than assumed absent.

Usage:
  python3 b1_arz.py dump   <edition> <record-path> [...]     # full field dump
  python3 b1_arz.py fields <edition> <substr> [...]          # field-name vocabulary census
"""
import sys, pathlib, hashlib, importlib.util

SPEC = pathlib.Path.home() / 'Games/reincarnated-collaboration/agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py'
spec = importlib.util.spec_from_file_location('gd_arz_adapter', SPEC)
mod = importlib.util.module_from_spec(spec)
sys.modules['gd_arz_adapter'] = mod
spec.loader.exec_module(mod)

EDITIONS = {
    'III': '~/Games/vendor/grim-dawn-edition-III-20260808',
    'I':   '~/Games/vendor/grim-dawn',
}
# archive-key -> path suffix under the edition root
ARCHIVES = [
    ('base', 'database/database.arz'),
    ('gdx1', 'gdx1/database/GDX1.arz'),
    ('gdx2', 'gdx2/database/GDX2.arz'),
    ('gdx3', 'gdx3/database/GDX3.arz'),
    ('sm1',  'survivalmode1/database/SurvivalMode1.arz'),
    ('sm2',  'survivalmode2/database/SurvivalMode2.arz'),
    ('sm3',  'survivalmode3/database/SurvivalMode3.arz'),
]


def load(edition):
    root = pathlib.Path(EDITIONS[edition]).expanduser()
    out = []
    for key, suf in ARCHIVES:
        p = root / suf
        if not p.exists():
            continue
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        out.append((key, p, sha, mod.ArzArchive(p)))
    return out


def fmt(v, rec_v=None):
    if isinstance(v, list):
        body = ', '.join(f'{x:g}' if isinstance(x, float) else str(x) for x in v)
        return f'[{body}]  (n={len(v)})'
    return f'{v:g}' if isinstance(v, float) else str(v)


def cmd_dump(edition, paths):
    stack = load(edition)
    print(f'### EDITION {edition}')
    for key, p, sha, a in stack:
        print(f'  archive {key:5s} {p}')
        print(f'          sha256 {sha}   records={len(a.records)}')
    for rp in paths:
        print(f'\n--- {rp}')
        hits = [(key, a) for key, p, sha, a in stack if rp in a.records]
        if not hits:
            print('    NOT IN ANY ARCHIVE OF THIS EDITION')
            continue
        for key, a in hits:
            rec = a.read_record(rp)
            print(f'  [{key}] rtype={a.record_type(rp)}  fields={len(rec)}')
            for k in sorted(rec):
                print(f'    {k:46s} {fmt(rec[k])}')


def cmd_fields(edition, subs):
    """Census: which field NAMES anywhere in the overlay contain any of `subs`."""
    stack = load(edition)
    subs = [s.lower() for s in subs]
    seen = {}
    for key, p, sha, a in stack:
        for rp in a.records:
            try:
                rec = a.read_record(rp)
            except Exception:
                continue
            for k in rec:
                kl = k.lower()
                if any(s in kl for s in subs):
                    seen.setdefault(k, [0, set()])
                    seen[k][0] += 1
                    if len(seen[k][1]) < 3:
                        seen[k][1].add(f'{key}:{rp}')
    for k in sorted(seen, key=lambda x: -seen[x][0]):
        n, ex = seen[k]
        print(f'{n:8d}  {k:46s} {sorted(ex)[0]}')


if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'dump':
        cmd_dump(sys.argv[2], sys.argv[3:])
    elif which == 'fields':
        cmd_fields(sys.argv[2], sys.argv[3:])
    else:
        raise SystemExit(__doc__)
