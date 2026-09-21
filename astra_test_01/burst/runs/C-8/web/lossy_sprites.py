#!/usr/bin/env python3
"""Second lossy pass: drop the texture threshold from 2048 px to 512 px.

The web overlay (~/Games/reincarnated-godot/web/_overlay/apply_overlay.py) marks
any PNG with a side >= 2048 px as lossy WebP q0.9. That covers the parallax plates
and the two ground tiles. It does NOT cover the character sprites, which are
512x512 -- and those are 544 frames / 39.1 MB in the warlord project, lossless.

That term is (a) the largest single contributor to the pck and (b) the ONLY part
that differs between the three characters, so it is precisely what the three-pck
split is meant to isolate. Leaving it lossless would mean each character's pck
carried ~30 MB of avoidable weight.

Threshold 512 rather than "everything": the VFX kits are mostly sub-512 frames
whose crisp alpha edges are load-bearing for the painted-pixel look, and they are
only ~0.6 MB in total below 512. Nothing is gained by touching them.

Idempotent -- re-running rewrites the same two keys to the same values.
Requires the .import sidecars, so run it AFTER a first headless --import.

usage: lossy_sprites.py <project_dir> [quality]
"""
import pathlib
import re
import struct
import sys

THRESHOLD_PX = 512
DEFAULT_QUALITY = '0.9'
SKIP_PREFIXES = ('.godot/', 'build/')


def png_size(path: pathlib.Path) -> tuple[int, int]:
    with path.open('rb') as handle:
        head = handle.read(24)
    return struct.unpack('>II', head[16:24])


def main() -> None:
    if not 2 <= len(sys.argv) <= 3:
        sys.exit('usage: lossy_sprites.py <project_dir> [quality]')
    root = pathlib.Path(sys.argv[1]).resolve()
    quality = sys.argv[2] if len(sys.argv) == 3 else DEFAULT_QUALITY
    if not (root / 'project.godot').is_file():
        sys.exit(f'not a Godot project: {root}')

    marked = 0
    missing = 0
    bytes_marked = 0
    for png in sorted(root.rglob('*.png')):
        rel = png.relative_to(root).as_posix()
        if rel.startswith(SKIP_PREFIXES):
            continue
        if max(png_size(png)) < THRESHOLD_PX:
            continue
        imp = png.with_name(png.name + '.import')
        if not imp.exists():
            missing += 1
            continue
        text = imp.read_text()
        new = re.sub(r'^compress/mode=.*$', 'compress/mode=1', text, flags=re.M)
        new = re.sub(r'^compress/lossy_quality=.*$', f'compress/lossy_quality={quality}',
                     new, flags=re.M)
        if new != text:
            imp.write_text(new)
        marked += 1
        bytes_marked += png.stat().st_size

    print(f'  sprite lossy (>={THRESHOLD_PX}px, q{quality}): {marked} textures, '
          f'{bytes_marked / 1e6:.1f} MB of source PNG')
    if missing:
        print(f'  WARNING: {missing} textures >= {THRESHOLD_PX}px still lack .import sidecars',
              file=sys.stderr)
        sys.exit(4)


if __name__ == '__main__':
    main()
