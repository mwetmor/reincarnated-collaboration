#!/usr/bin/env python3
"""Audit actual web-pack bytes against current local gameplay/audio/scene inputs."""
import hashlib
import json
import sys
from pathlib import Path
from pck_native_alias import entries

ROOT = Path(__file__).resolve().parent.parent
web = Path(sys.argv[1]).resolve()
output = web / 'build/web'
table = {}
for pack in sorted(output.glob('*.pck')):
    if pack.stat().st_size >= 50_000_000:
        raise ValueError('Web file exceeds 50 MB: ' + pack.name)
    with pack.open('rb') as f:
        base, rows = entries(f)
        for name, offset, size, _ in rows:
            table[name] = (pack, base + offset, size)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packed_digest(name):
    if name not in table:
        raise ValueError('Missing web payload: ' + name)
    pack, offset, size = table[name]
    with pack.open('rb') as f:
        f.seek(offset)
        return hashlib.sha256(f.read(size)).hexdigest()


expected = {}
for path in (web / 'data').rglob('*'):
    if path.is_file() and path.suffix in ('.bin', '.json', '.f32', '.gdshader'):
        expected[str(path.relative_to(web))] = digest(path)
for path in (web / 'kc2/bundle').rglob('*'):
    if path.is_file():
        expected[str(path.relative_to(web))] = digest(path)
for path in (ROOT / 'godot/scripts').rglob('*.gd'):
    expected[str(path.relative_to(ROOT / 'godot'))] = digest(path)
fields = list((web / 'data').rglob('*.f32'))
for path in fields:
    name = str(path.relative_to(web))
    expected[name] = digest(ROOT / 'godot' / name)
manifest_path = ROOT / 'godot/data/audio/arena_audio.json'
manifest = json.loads(manifest_path.read_text())
expected['data/audio/arena_audio.json'] = digest(manifest_path)
for clip in manifest['clips'].values():
    expected['data/audio/' + clip['file']] = clip['sha256']
for relative, filename in [('kc2/kc2_runtime', 'MANIFEST.json'), ('kc2/model_pack', 'manifest.json')]:
    members = json.loads((web / relative / filename).read_text())['members']
    expected.update({relative + '/' + m['path']: m['sha256'] for m in members})
stamp = json.loads((web / 'kc2/bundle/BUNDLE_STAMP.json').read_text())
kits = {k for group in stamp['kit_pack_members'].values() for k in group}
native_kits = set(json.loads((ROOT / 'pc_arena/kc2/bundle/BUNDLE_STAMP.json').read_text())['kit_sources'])
if kits != native_kits:
    raise ValueError('Web catalogue differs from native: ' + str(kits ^ native_kits))
art_files = set()
for kit in kits:
    name = 'kc2/art/' + kit + '/index.json'
    index = json.loads((web / name).read_text())
    native_index = json.loads((ROOT / 'pc_arena' / name).read_text())
    for cell in native_index['cells'].values():
        cell['file'] = str(Path(cell['file'].removesuffix('.bin')).with_suffix('.webp.bin'))
        for key in ('fw', 'fh'):
            if key in cell:
                cell[key] *= 0.5
        if 'anchor_px' in cell:
            cell['anchor_px'] = [v * 0.5 for v in cell['anchor_px']]
    native_index['stage_scale'] = native_index.get('stage_scale', 0.5) * 0.5
    comparable = {k: v for k, v in index.items() if k != '_bundle'}
    if native_index != comparable:
        raise ValueError('Web animation catalogue differs from native: ' + kit)
    expected[name] = digest(web / name)
    for cell in index['cells'].values():
        name = 'kc2/art/' + cell['file']
        art_files.add(name)
        expected[name] = digest(web / name)
for name, sha in expected.items():
    if packed_digest(name) != sha:
        raise ValueError('Web payload differs: ' + name)
result = {'verified_payloads': len(expected), 'terrain_fields': len(fields), 'character_kits': len(kits),
    'art_strips': len(art_files), 'audio_clips': len(manifest['clips']), 'audio_manifest_sha256': digest(manifest_path),
    'runtime_digest': stamp['runtime_tree_digest'], 'model_digest': stamp['model_pack_digest'],
    'files': {p.name: {'bytes': p.stat().st_size, 'sha256': digest(p)} for p in sorted(output.iterdir()) if p.is_file()},
    'web_texture_conversion': 'Half-resolution WebP character art and phone painting; gameplay and audio bytes unchanged'}
(web / 'build/logs/web_payload_audit.json').write_text(json.dumps(result, indent=2) + '\n')
print('WEB_PAYLOAD: PASS; ' + json.dumps({k: result[k] for k in ['verified_payloads', 'terrain_fields', 'character_kits', 'audio_clips']}))
