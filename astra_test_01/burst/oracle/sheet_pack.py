"""Pack native numbered RGBA movie frames without trimming or resampling."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

from PIL import Image


def numbered_frames(directory, prefix='fx'):
    """Return numerically sorted frames; reject gaps, aliases and empty input."""
    root = Path(directory).resolve()
    pattern = re.compile(re.escape(prefix) + r'(\d+)\.png')
    indexed = []
    for path in root.glob(prefix + '*.png'):
        match = pattern.fullmatch(path.name)
        if match is None:
            raise ValueError('Malformed numbered PNG: ' + path.name)
        if not path.resolve().is_relative_to(root):
            raise ValueError('Escaping frame path')
        indexed.append((int(match[1]), path))
    indexed.sort()
    if not indexed or [n for n, _ in indexed] != list(range(indexed[0][0], indexed[0][0] + len(indexed))):
        raise ValueError('Frames must be nonempty, contiguous and unique')
    return [path for _, path in indexed]


def sheet_pack(frames, out, columns=8, pivot=(256, 256), fps=60):
    """Write a lossless atlas and JSON manifest; all cells keep their full canvas.

    Native cells are at most 512x512. Pivot is an unchanged cell-space offset,
    which may lie outside the canvas. No alpha-mask paste (it loses alpha).
    """
    frames = list(map(Path, frames))
    if not frames or isinstance(columns, bool) or not isinstance(columns, int) or columns < 1:
        raise ValueError('Need frames and positive integer columns')
    if isinstance(fps, bool) or not isinstance(fps, (int, float)) or not math.isfinite(fps) or fps <= 0:
        raise ValueError('fps must be finite and positive')
    if len(pivot) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in pivot):
        raise ValueError('pivot must be a finite pair')
    images = []
    for path in frames:
        with Image.open(path) as im:
            if im.mode != 'RGBA' or max(im.size) > 512:
                raise ValueError('Native frames must be RGBA and at most 512x512')
            if images and im.size != images[0].size:
                raise ValueError('Frame canvas mismatch')
            images.append(im.copy())
    width, height = images[0].size
    columns = min(columns, len(images))
    sheet = Image.new('RGBA', (columns * width, math.ceil(len(images) / columns) * height))
    records = []
    for index, (path, im) in enumerate(zip(frames, images)):
        x, y = index % columns * width, index // columns * height
        sheet.paste(im, (x, y))
        records.append({'index': index, 'source': path.name, 'rect': [x, y, width, height],
                        'pivot': list(pivot), 'atlas_pivot': [x + pivot[0], y + pivot[1]],
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    out = Path(out)
    if out.resolve() in {p.resolve() for p in frames}:
        raise ValueError('Sheet cannot overwrite an input')
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    manifest = {'cell_size': [width, height], 'columns': columns, 'fps': fps,
                'pivot': list(pivot), 'trimmed': False, 'resampled': False, 'frames': records}
    out.with_suffix('.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frames', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--prefix', default='fx')
    parser.add_argument('--columns', type=int, default=8)
    parser.add_argument('--pivot', type=float, nargs=2, default=(256, 256))
    parser.add_argument('--fps', type=float, default=60)
    args = parser.parse_args()
    print(json.dumps(sheet_pack(numbered_frames(args.frames, args.prefix), args.out,
                                args.columns, args.pivot, args.fps), indent=2))


if __name__ == '__main__':
    main()
