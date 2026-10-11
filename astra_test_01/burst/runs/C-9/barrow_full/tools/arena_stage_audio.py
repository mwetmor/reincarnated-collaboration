#!/usr/bin/env python3
"""Stage pinned audio, deriving compatible WAVs where specified; sources stay read-only.

Run under the shared heavy lock when a manifest includes conversion recipes.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', type=Path, default=Path(__file__).resolve().parent.parent / 'godot')
    ap.add_argument('--source', type=Path, default=Path('/Users/admin/Games/reincarnated-demo/public/audio'))
    ap.add_argument('--update-derived-hashes', action='store_true', help='Only the selection application may pin newly converted WAVs')
    args = ap.parse_args()
    target = args.project / 'data/audio'
    manifest = json.loads((target / 'arena_audio.json').read_text())
    def source(clip):
        root = Path(manifest['source_roots'][clip['source_root']]) if clip.get('source_root') else args.source
        return root / clip['source']
    # Validate all sources before writing any output. A stale manifest refuses.
    for clip in manifest['clips'].values():
        src = source(clip)
        if not src.is_file() or sha(src) != clip.get('source_sha256', clip['sha256']):
            raise ValueError('Missing/changed audio source: ' + str(src))
    for clip in manifest['clips'].values():
        src, dst = source(clip), target / clip['file']
        if not dst.is_file() or sha(dst) != clip['sha256']:
            if clip.get('conversion'):
                recipe = clip['conversion']
                if recipe['codec'] != 'pcm_s16le':
                    raise ValueError('Unsupported conversion recipe')
                pending = dst.with_suffix('.pending')
                subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-y', '-i', str(src), '-map', '0:a:0', '-map_metadata', '-1',
                                '-ar', str(recipe['sample_rate']), '-ac', str(recipe['channels']), '-c:a', recipe['codec'], '-f', 'wav', str(pending)], check=True)
                converted_sha = sha(pending)
                if args.update_derived_hashes:
                    clip['sha256'], clip['bytes'] = converted_sha, pending.stat().st_size
                elif converted_sha != clip['sha256']:
                    raise ValueError('Conversion output differs from pinned payload: ' + str(src))
                pending.replace(dst)
            else:
                shutil.copy2(src, dst)
        assert sha(dst) == clip['sha256']
    if args.update_derived_hashes:
        (target / 'arena_audio.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('AUDIO_STAGE: PASS; %d pinned clips; %.1f MB' %
          (len(manifest['clips']), sum(c['bytes'] for c in manifest['clips'].values()) / 1e6))


if __name__ == '__main__':
    main()
