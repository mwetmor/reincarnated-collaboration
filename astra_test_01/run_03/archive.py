"""Create and verify a self-contained local review archive, including source art."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent


def package_archive():
    files = []
    for folder in [ROOT, BASE / 'run_02']:
        files.extend(p for p in folder.rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts
                     and p.suffix not in ['.zip', '.pyc']
                     and p.name not in ['archive_verification.json', 'archive_manifest.json', '.DS_Store'])
    files = sorted(files)
    skill = BASE.parent / '.agents/skills/painted-character-vfx'
    files.extend(p for p in skill.rglob('*') if p.is_file())
    brief = BASE.parent / 'codex-3d-modeling/ASTRA TEST 01 painted character vfx.md'
    files.append(brief)
    def archive_name(p):
        if p == brief:return 'ASTRA TEST 01 painted character vfx.md'
        if p.is_relative_to(skill):return 'workflow/' + str(p.relative_to(skill))
        return str(p.relative_to(BASE))
    manifest = {archive_name(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    target = BASE / 'astra_test_01_run_03_review.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for p in files:
            archive.write(p, archive_name(p))
        archive.writestr('archive_manifest.json', json.dumps(manifest, indent=2) + '\n')
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for name, expected in manifest.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected, name
        assert sum(name.startswith('run_03/character/frames/') and name.endswith('.png') for name in manifest) == 224
        assert sum(name.startswith('run_03/vfx/frames/') and name.endswith('.png') for name in manifest) == 24
        assert 'run_03/preview/index.html' in manifest
    result = dict(archive=target.name, bytes=target.stat().st_size,
                  sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                  files=len(manifest), member_hashes='PASS', zip_integrity='PASS',
                  character_frames=224, vfx_frames=24,
                  character_acceptance='FAIL', vfx_acceptance='PARTIAL')
    (ROOT / 'evidence/archive_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    package_archive()
