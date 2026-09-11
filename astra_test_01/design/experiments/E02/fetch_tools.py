"""Fetch pinned public test dependencies with system TLS verification and hashes."""
from pathlib import Path
import hashlib
import json
import subprocess
import tarfile

P=Path(__file__).resolve().parent
vendor=P/'pixi/vendor'
vendor.mkdir(exist_ok=True)
for dep in json.loads((P/'DEPENDENCIES.json').read_text()):
    path=vendor/dep['name']
    if path.exists():
        assert hashlib.sha256(path.read_bytes()).hexdigest()==dep['sha256'], f'Changed cache: {path}'
        continue
    temporary=path.with_suffix(path.suffix+'.download')
    subprocess.run(['curl','--fail','--location','--max-time','30',dep['url'],'--output',str(temporary)],check=True)
    assert hashlib.sha256(temporary.read_bytes()).hexdigest()==dep['sha256'], f'Upstream hash mismatch: {path}'
    temporary.rename(path)
destination=vendor/'playwright-package'
if not destination.exists():
    with tarfile.open(vendor/'playwright-core-1.63.0.tgz') as archive:
        archive.extractall(destination,filter='data')
package=json.loads((destination/'package/package.json').read_text())
assert package['version']=='1.63.0'
print('Pinned Pixi and isolated-browser tooling ready; no browser binary downloaded.')
