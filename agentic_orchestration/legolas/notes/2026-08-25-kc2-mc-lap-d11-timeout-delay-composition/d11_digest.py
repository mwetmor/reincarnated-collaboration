"""D-11 — digest manifest for the pinned substrate + this lap's own artefacts. READ-ONLY."""
import hashlib, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
SRC = ['/Users/admin/Games/vendor/grim-dawn/Game.dll']
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda: f.read(1<<20), b''): h.update(b)
    return h.hexdigest()
out={'substrate':{}, 'lap_artifacts':{}}
for s in SRC:
    if pathlib.Path(s).exists(): out['substrate'][s]=sha(s)
for p in sorted(HERE.rglob('*')):
    if p.is_file() and p.name not in ('d11_digests.json',) and '__pycache__' not in str(p):
        out['lap_artifacts'][str(p.relative_to(HERE))]=sha(p)
(HERE/'d11_digests.json').write_text(json.dumps(out, indent=2))
print(json.dumps(out['substrate'], indent=2)); print(len(out['lap_artifacts']),'artifacts')
