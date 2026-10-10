#!/usr/bin/env python3
"""Audit native export payloads and write the portable Windows package metadata."""
import hashlib
import json
import shutil
import struct
import sys
from pathlib import Path
from pck_native_alias import entries, ALIAS, PIN


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(sys.argv[1]).resolve()
    output = root / 'build/BarrowArena-Windows-x64'
    pack = output / 'BarrowArena.pck'
    stamp = json.loads((root / 'kc2/bundle/BUNDLE_STAMP.json').read_text())
    expected = dict(stamp['art_files'])
    expected.update({'kc2/bundle/' + name: digest for name, digest in stamp['files'].items()})
    for directory, filename in [('kc2/kc2_runtime', 'MANIFEST.json'), ('kc2/model_pack', 'manifest.json')]:
        manifest = json.loads((root / directory / filename).read_text())
        expected[directory + '/' + filename] = sha(root / directory / filename)
        expected.update({directory + '/' + member['path']: member['sha256'] for member in manifest['members']})
    # Every raw native level/painting/shader input must be present, byte-for-byte.
    for source in (root / 'data').rglob('*'):
        if source.is_file() and source.suffix in ('.bin', '.json', '.gdshader', '.f32'):
            expected[str(source.relative_to(root))] = sha(source)
    expected[ALIAS] = PIN
    with open(pack, 'rb') as f:
        base, rows = entries(f)
        table = {name: (offset, size) for name, offset, size, _ in rows}
        if len(table) != len(rows):
            raise ValueError('duplicate packed paths')
        for name, digest in expected.items():
            if name not in table:
                raise ValueError('missing native payload: ' + name)
            offset, size = table[name]
            f.seek(base + offset)
            h = hashlib.sha256()
            remaining = size
            while remaining:
                chunk = f.read(min(1 << 20, remaining))
                if not chunk:
                    raise ValueError('truncated payload: ' + name)
                h.update(chunk)
                remaining -= len(chunk)
            if h.hexdigest() != digest:
                raise ValueError('native payload changed: ' + name)
    with open(output / 'BarrowArena.exe', 'rb') as f:
        assert f.read(2) == b'MZ'
        f.seek(0x3c)
        pe = struct.unpack('<I', f.read(4))[0]
        f.seek(pe)
        assert f.read(4) == b'PE\0\0'
        assert struct.unpack('<H', f.read(2))[0] == 0x8664, 'not Windows x64'
    (output / 'Play Barrow Arena.cmd').write_bytes(b'@echo off\r\ncd /d "%~dp0"\r\nstart "" /wait "%~dp0BarrowArena.exe"\r\n')
    (output / 'READ ME.txt').write_text('''BARROW ARENA - Windows x64 playtest (2026-10-10)

1. Extract the entire ZIP to a folder on your Windows PC.
2. Open BarrowArena.exe (or Play Barrow Arena.cmd).
   Keep BarrowArena.pck beside the executable.
   No Godot editor, npm, internet connection, or Vercel account is needed.

CONTROLS
Space: begin the fight
Left mouse: move / click an enemy to charge and attack
Right mouse (hold): Whirlwind
1: Potion   2: Might   3: Battle Cry   4: Haste
Z: zoom   R: restart   Escape: exit

This is the existing native bv2f_arena scene, using Forward+ rendering,
original-resolution character strips, native level/painting data, the live
3D hero rig, snow, water, collision/traversal and enemy VFX. No web reductions
are applied. Use a Windows 10/11 x64 PC with graphics support for Godot's
Forward+ renderer; graphics drivers and hardware affect the final appearance.

The sealed KC2 runtime and model pack are unchanged and hash-verified.
Their compiled contact solver is Mac arm64 only. Windows explicitly uses the
runtime's existing exact GDScript reference solver, which may run more slowly.
The legacy absolute data lookup resolves inside the PCK; no folders are
created at that path on the PC. Telemetry/logs use Godot's user data folder.

Validation performed on Mac: packed payload checks and native scene probes.
Windows executable launch, GPU appearance, and performance require a real PC
playtest. This package is unsigned. See BUILD_MANIFEST.json for verified inputs.
The web/mobile bugs are deferred separately; this is an offline PC playtest.
''', encoding='utf-8')
    manifest = {'platform': 'Windows.x86_64', 'engine': 'Godot 4.6.3 stable',
                'main_scene': 'res://scenes/bv2f_arena.tscn', 'renderer': 'forward_plus',
                'contact_solver': 'gdscript (explicit presentation selection)',
                'runtime_tree_digest': stamp['runtime_tree_digest'],
                'model_pack_digest': stamp['model_pack_digest'],
                'verified_native_payloads': len(expected), 'native_art_files': len(stamp['art_files']),
                'kit_count': len(stamp['kit_sources']), 'windows_launch_verified': False,
                'legacy_table_alias': ALIAS,
                'files': {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)}
                          for p in sorted(output.iterdir()) if p.is_file() and p.name != 'BUILD_MANIFEST.json'}}
    (output / 'BUILD_MANIFEST.json').write_text(json.dumps(manifest, indent=2))
    print('NATIVE_PAYLOAD: PASS; %d byte-verified inputs; PE x64 confirmed' % len(expected))


if __name__ == '__main__':
    main()
