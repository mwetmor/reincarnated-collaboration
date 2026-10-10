#!/usr/bin/env python3
"""Copy only pinned demo audio into the arena. Source assets stay read-only."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', type=Path, default=Path(__file__).resolve().parent.parent / 'godot')
    ap.add_argument('--source', type=Path, default=Path('/Users/admin/Games/reincarnated-demo/public/audio'))
    args = ap.parse_args()
    target = args.project / 'data/audio'
    manifest = json.loads((target / 'arena_audio.json').read_text())
    # Validate all sources before writing any output. A stale manifest refuses.
    for clip in manifest['clips'].values():
        src = args.source / clip['source']
        if not src.is_file() or sha(src) != clip['sha256']:
            raise ValueError('Missing/changed audio source: ' + str(src))
    for clip in manifest['clips'].values():
        src, dst = args.source / clip['source'], target / clip['file']
        if not dst.is_file() or sha(dst) != clip['sha256']:
            shutil.copy2(src, dst)
        assert sha(dst) == clip['sha256']
    print('AUDIO_STAGE: PASS; %d original-byte clips; %.1f MB' %
          (len(manifest['clips']), sum(c['bytes'] for c in manifest['clips'].values()) / 1e6))


if __name__ == '__main__':
    main()
