#!/usr/bin/env python3
"""ZIP the audited package only after the packed native scene probe passes."""
import json
import sys
import zipfile
from pathlib import Path
from arena_native_package import sha


def main():
    root = Path(sys.argv[1]).resolve()
    package = root / 'build/BarrowArena-Windows-x64'
    manifest_path = package / 'BUILD_MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    evidence = root / 'build/logs/native/native_probe.json'
    probe = json.loads(evidence.read_text())
    if probe['solver'] != 'gdscript' or probe['ticks_advanced'] <= 0:
        raise ValueError('packed reference-solver probe did not pass')
    stamp = json.loads((root / 'kc2/bundle/BUNDLE_STAMP.json').read_text())
    catalogue = {p.parent.name for p in Path('/Users/admin/Games/reincarnated-godot/kc2_play/art/join1').glob('*/index.json')}
    if not catalogue.issubset(stamp['kit_sources']):
        raise ValueError('full native catalogue not yet bundled; ZIP refused')
    for name, member in manifest['files'].items():
        if sha(package / name) != member['sha256']:
            raise ValueError('package changed after audit: ' + name)
    manifest['mac_packed_scene_probe'] = probe
    manifest['windows_launch_verified'] = False
    manifest_path.write_text(json.dumps(manifest, indent=2))
    target = root / 'build/BarrowArena-Windows-x64.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as archive:
        for path in sorted(package.rglob('*')):
            if path.is_file():
                archive.write(path, package.name + '/' + str(path.relative_to(package)))
    with zipfile.ZipFile(target) as archive:
        corrupt = archive.testzip()
        if corrupt:
            raise ValueError('ZIP CRC failure: ' + corrupt)
    checksum = sha(target)
    target.with_suffix('.zip.sha256').write_text(checksum + '  ' + target.name + '\n')
    print('NATIVE_ZIP: PASS; %d bytes; sha256 %s; %s' % (target.stat().st_size, checksum, target))


if __name__ == '__main__':
    main()
