#!/usr/bin/env python3
"""Restore native world bake detail within a 2048px web memory bound.

Only changes the disposable web mirror. Native originals are hash checked and
read-only. Images remain bounded at 2048px; lossless WebP preserves
RGB/alpha values, including every original texel for bakes at or below the bound. The 4096px overview painting stays unchanged.
"""
import hashlib
import io
import json
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    mirror = Path(sys.argv[1]).resolve()
    if mirror != ROOT / 'web_arena':
        raise ValueError('This operation only writes the web export mirror')
    source = ROOT / 'godot/data/bv2f/site_ph4/painted'
    target = mirror / 'data/bv2f/site_ph4/painted_web'
    native = json.loads((source / 'manifest.json').read_text())
    manifest = json.loads((target / 'manifest.json').read_text())
    if set(native['bakes']) != set(manifest['bakes']):
        raise ValueError('World bake catalogues differ')
    for row in native['bakes'].values():
        if sha((source / row['file']).read_bytes()) != row['sha256']:
            raise ValueError('Changed native world texture: ' + row['file'])
    report = {'recipe': 'native dimensions up to 2048px; lossless WebP', 'bakes': {}, 'bytes': 0}
    rgba_with_mips = 0
    for key, row in native['bakes'].items():
        with Image.open(source / row['file']) as original:
            image = original.convert('RGBA')
            ratio = min(1.0, 2048 / max(image.size))
            size = (round(image.width * ratio), round(image.height * ratio))
            if image.size != size:
                image = image.resize(size, Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, 'WEBP', lossless=True, method=4, exact=True)
        data = buffer.getvalue()
        # Verify that the codec kept every resized texel, including alpha.
        with Image.open(io.BytesIO(data)) as decoded:
            if decoded.convert('RGBA').tobytes() != image.tobytes():
                raise ValueError('World texture changed during lossless encoding')
        destination = target / manifest['bakes'][key]['file']
        destination.write_bytes(data)
        manifest['bakes'][key]['sha256'] = sha(data)
        report['bakes'][key] = {'source_sha256': row['sha256'], 'sha256': sha(data), 'px': list(size), 'bytes': len(data)}
        report['bytes'] += len(data)
        rgba_with_mips += round(size[0] * size[1] * 4 * 4 / 3)
    report['estimated_bake_rgba_with_mips_bytes'] = rgba_with_mips
    manifest['_arena_texture_detail'] = report['recipe']
    (target / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    logs = mirror / 'build/logs'
    logs.mkdir(parents=True, exist_ok=True)
    (logs / 'world_texture_detail.json').write_text(json.dumps(report, indent=2) + '\n')
    print('WORLD_TEXTURE_DETAIL: PASS; %d bakes; %.1f MB packed; %.1f MB estimated RGBA+mips' %
          (len(report['bakes']), report['bytes'] / 1e6, rgba_with_mips / 1e6))


if __name__ == '__main__':
    main()
