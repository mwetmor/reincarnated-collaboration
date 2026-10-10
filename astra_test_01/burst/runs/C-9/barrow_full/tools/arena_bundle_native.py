#!/usr/bin/env python3
"""Vendor the existing arena for native desktop, retaining original art bytes.

Only raw strip filenames gain .bin to bypass Godot's image importer. Cell sizes,
anchors, stage scale, and all pixel bytes remain the source's. No WebP conversion,
texture limits, web paintings, shader switches, or renderer overrides.
"""
import json
import os
import shutil
import sys
from pathlib import Path
import arena_bundle as shared


def copy_exact(src, dst, manifest, key):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    digest = shared.sha(src)
    if shared.sha(dst) != digest:
        shared.die('native asset copy differs: ' + str(src))
    manifest[key] = digest


def main():
    root = Path(sys.argv[1]).resolve()
    if not (root / 'project.godot').is_file():
        shared.die('missing project')
    kc2 = root / 'kc2'
    (kc2 / '.gdignore').unlink(missing_ok=True)
    bundle = kc2 / 'bundle'
    bundle.mkdir(parents=True, exist_ok=True)
    stamp = {'_what': 'Native desktop bundle; full-resolution original bytes',
             'runtime_tree_digest': shared.RT_PIN, 'model_pack_digest': shared.PACK_PIN,
             'files': {}, 'kit_packs': [], 'art_files': {}, 'kit_sources': {}}
    stamp['runtime_members'] = shared.vendor_tree(shared.RT_SRC, str(kc2 / 'kc2_runtime'),
                                                   'MANIFEST.json', 'tree_digest', shared.RT_PIN)
    stamp['model_pack_members'] = shared.vendor_tree(shared.PACK_SRC, str(kc2 / 'model_pack'),
                                                     'manifest.json', 'pack_digest', shared.PACK_PIN)
    inputs = dict(shared.FILES)
    inputs.update({'pm4p_leech_resistance.csv.bin': shared.LEECH_SRC,
                   'crucible-arena-geometry-v1.json': shared.GEOM_SRC})
    for name, source in inputs.items():
        copy_exact(Path(source), bundle / name, stamp['files'], name)
    assert stamp['files']['pm4p_leech_resistance.csv.bin'] == shared.LEECH_PIN
    assert stamp['files']['crucible-arena-geometry-v1.json'] == shared.GEOM_PIN
    art = kc2 / 'art'
    if art.exists():
        shutil.rmtree(art)
    art.mkdir()
    copy_exact(Path(shared.JOIN1) / 'join1_index.json', art / 'join1_index.json',
               stamp['art_files'], 'kc2/art/join1_index.json')
    waves = json.loads((root / 'data/arena/wave_kits.json').read_text())
    # Ship the entire native catalogue, including larva/worm variants and
    # eor_overlay, rather than relying solely on the wave inventory.
    kits = sorted({waves['hero'], 'gd-eor-warlord-eor4x'} |
                  {k for wave in waves['waves'].values() for k in wave} |
                  {p.parent.name for base in (shared.JOIN1, shared.ART_X)
                   for p in Path(base).glob('*/index.json')})
    for kit in kits:
        source = Path(shared.ART_X) / kit
        if not source.is_dir():
            source = Path(shared.JOIN1) / kit
        index = json.loads((source / 'index.json').read_text())
        original = json.loads(json.dumps(index))
        stamp['kit_sources'][kit] = str(source)
        for cell in index['cells'].values():
            name = cell['file']
            target = 'kc2/art/' + name + '.bin'
            if target not in stamp['art_files']:
                copy_exact(source.parent / name, root / target, stamp['art_files'], target)
            cell['file'] = name + '.bin'
        # Assert no metadata drift except the raw file suffix.
        restored = json.loads(json.dumps(index))
        for cell in restored['cells'].values():
            cell['file'] = cell['file'][:-4]
        assert restored == original
        destination = art / kit / 'index.json'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(index, indent=1))
        stamp['art_files']['kc2/art/' + kit + '/index.json'] = shared.sha(destination)
    for member in shared.stage_enemy_vfx(str(root)):
        stamp['art_files'][member] = shared.sha(root / member)
    (bundle / 'BUNDLE_STAMP.json').write_text(json.dumps(stamp, indent=1))
    print('Native bundle: %d kits; %d original art/VFX files; runtime/model pins intact' %
          (len(kits), len(stamp['art_files'])))


if __name__ == '__main__':
    main()
