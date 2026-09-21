#!/usr/bin/env python3
"""Cut one select-screen portrait per character from that character's OWN frames.

Source is the idle_S first frame of each build -- the character facing the camera,
the same bytes the scene plays. Nothing is drawn or synthesised here: the portrait
is a trim + downscale of a real exported frame, so the select screen shows what
you will actually be controlling.

Trims fully-transparent margins, fits inside a fixed box, and keeps the three
figures at a CONSISTENT relative scale (they are all 151 px figure height at
export, so a common scale factor keeps them comparable rather than each filling
its own card differently).

usage: mk_portraits.py <out_dir>
"""
import pathlib
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
BOX = (320, 320)

SOURCES = {
    'warlord': HERE / 'stage-warlord' / 'sprites' / 'idle' / 'S' / 'idle_S_00.png',
    'keeper': HERE / 'stage-keeper' / 'sprites' / 'idle' / 'S' / 'idle_S_00.png',
    'necro': HERE / 'stage-necro' / 'sprites' / 'idle' / 'S' / 'idle_S_00.png',
}


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit('usage: mk_portraits.py <out_dir>')
    out = pathlib.Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=True)

    trimmed = {}
    for char, src in SOURCES.items():
        if not src.is_file():
            sys.exit(f'missing source frame for {char}: {src}')
        im = Image.open(src).convert('RGBA')
        box = im.getbbox()
        if box is None:
            sys.exit(f'{char}: frame is fully transparent')
        trimmed[char] = im.crop(box)
        print(f'{char}: {im.size} -> trimmed {trimmed[char].size}')

    # One scale factor across all three so the figures stay comparable.
    tallest = max(c.height for c in trimmed.values())
    widest = max(c.width for c in trimmed.values())
    scale = min(BOX[0] / widest, BOX[1] / tallest)

    for char, crop in trimmed.items():
        size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
        small = crop.resize(size, Image.LANCZOS)
        canvas = Image.new('RGBA', BOX, (0, 0, 0, 0))
        # Bottom-centred: they are standing figures, so align their feet.
        canvas.paste(small, ((BOX[0] - size[0]) // 2, BOX[1] - size[1]), small)
        dest = out / f'{char}.png'
        canvas.save(dest, optimize=True)
        print(f'{char}: -> {dest} {size} {dest.stat().st_size / 1024:.0f} KB')


if __name__ == '__main__':
    main()
