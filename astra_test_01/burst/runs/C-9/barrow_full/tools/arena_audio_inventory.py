#!/usr/bin/env python3
"""Read-only inventory of the demo audio, including ignored vendor assets."""
import argparse
import collections
import csv
import hashlib
import json
import subprocess
import wave
from pathlib import Path

EXTENSIONS = {'.wav', '.ogg', '.mp3', '.m4a', '.flac', '.aac', '.aiff', '.opus'}


def metadata(path):
    if path.suffix.lower() == '.wav':
        try:
            with wave.open(str(path)) as f:
                return {'seconds': round(f.getnframes() / f.getframerate(), 3),
                        'channels': f.getnchannels(), 'sample_rate': f.getframerate()}
        except (wave.Error, EOFError):
            pass
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=duration:format_tags:stream=codec_name,channels,sample_rate',
                        '-of', 'json', str(path)], capture_output=True, text=True)
    if r.returncode:
        return {'error': r.stderr.strip()}
    info = json.loads(r.stdout)
    s = info.get('streams', [{}])[0]
    return {'seconds': round(float(info.get('format', {}).get('duration', 0)), 3),
            'channels': s.get('channels'), 'sample_rate': s.get('sample_rate'),
            'tags': info.get('format', {}).get('tags', {})}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, default=Path('/Users/admin/Games/reincarnated-demo/public/audio'))
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    rows, skipped = [], []
    for p in sorted(args.source.rglob('*')):
        if not p.is_file() or p.suffix.lower() not in EXTENSIONS:
            continue
        name = str(p.relative_to(args.source))
        if '__MACOSX' in p.parts or p.name.startswith('._'):
            skipped.append(name)
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        group = name.split('/')[1] if name.startswith('sfx/') else 'Season music'
        rows.append({'path': name, 'group': group, 'format': p.suffix[1:].lower(),
                     'bytes': p.stat().st_size, 'sha256': h, **metadata(p)})
    by_hash = collections.defaultdict(list)
    for row in rows:
        by_hash[row['sha256']].append(row['path'])
    manifest = json.loads((args.source / 'sfx-manifest.json').read_text())
    coverage = {}
    for layer, slots in manifest.items():
        if not isinstance(slots, dict):
            continue
        refs = [p for key, value in slots.items() if not key.startswith('_')
                for p in (value if isinstance(value, list) else [value]) if isinstance(p, str)]
        coverage[layer] = {'slots': sum(not k.startswith('_') for k in slots),
                           'references': len(refs),
                           'missing': sorted({p for p in refs if not (args.source.parent / p).is_file()})}
    result = {'source': str(args.source), 'generated_date': '2026-10-10',
              'audio_files': len(rows), 'unique_byte_contents': len(by_hash),
              'total_bytes': sum(r['bytes'] for r in rows),
              'format_counts': dict(collections.Counter(r['format'] for r in rows)),
              'group_counts': dict(collections.Counter(r['group'] for r in rows)),
              'excluded_appledouble': skipped, 'demo_manifest_coverage': coverage,
              'exact_duplicates': [v for v in by_hash.values() if len(v) > 1],
              'music': [r for r in rows if r['group'] == 'Season music'], 'files': rows}
    identities = collections.defaultdict(set)
    for row in rows:
        identities[row['group']].add(Path(row['path']).stem)
    result['basename_identities_per_group'] = {k: len(v) for k, v in identities.items()}
    result['basename_identity_count'] = sum(len(v) for v in identities.values())
    result['identity_note'] = 'Same basename within a pack groups alternate formats; not a decoded-audio fingerprint.'
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'AUDIO_INVENTORY.json').write_text(json.dumps(result, indent=2) + '\n')
    with (args.output / 'AUDIO_INVENTORY.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'group', 'format', 'seconds', 'channels',
                                              'sample_rate', 'bytes', 'sha256'],
                                extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({k: v for k, v in result.items() if k not in
                      ['files', 'exact_duplicates', 'excluded_appledouble']}, indent=2))


if __name__ == '__main__':
    main()
