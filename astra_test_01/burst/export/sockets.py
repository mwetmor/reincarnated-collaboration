"""Measure staff sockets on registered canvases. CLI defaults to cast cells.

JSON: {version:1, canvas:[512,512], cells:{cast_S:{sockets:[[x,y],...],
release_index:3, measurements:[{tip,reason,line_inliers,slope},...]}}}.
A missing measurement stays null; consumers must not invent an attachment.
"""
import argparse
import json
from pathlib import Path
from PIL import Image
from oracle.staff_tip import tip
from export.godot_import import discover_cells, _nearby


def build_sockets(cells, out=None, all_cells=False):
    root = Path(cells).resolve()
    entries = discover_cells(root)
    result = {'version': 1, 'canvas': [512, 512], 'cells': {}}
    for name, cell in sorted(entries.items()):
        if cell['anim'] != 'cast' and not all_cells:
            continue
        measurements = []
        for path in cell['frames']:
            with Image.open(path) as image:
                measurements.append(tip(image))
        record = {'sockets': [m['tip'] for m in measurements], 'measurements': measurements}
        if cell['anim'] == 'cast':
            meta = _nearby(cell['folder'], root, 'registration.json')
            meta = json.loads(meta.read_text()) if meta else {}
            release = meta.get('release_output_index', 3)
            if isinstance(release, bool) or not isinstance(release, int) or not 0 <= release < len(measurements):
                raise ValueError('release_output_index must index an output frame: '+name)
            record['release_index'] = release
        result['cells'][name] = record
    if not result['cells']:
        raise ValueError('No requested cells')
    target = Path(out) if out is not None else root.parent/'sockets.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    return result


def load_sockets(path, cells):
    """Validate canvas, counts, coordinates and release against exported cells."""
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict) or data.get('version') != 1 or data.get('canvas') != [512, 512] or not isinstance(data.get('cells'), dict):
        raise ValueError('Invalid socket document')
    import math
    for name, cell in cells.items():
        if cell['anim'] != 'cast':
            continue
        record = data['cells'].get(name)
        if not isinstance(record, dict) or not isinstance(record.get('sockets'), list) or len(record['sockets']) != len(cell['frames']):
            raise ValueError('Missing sockets or incorrect frame count: '+name)
        release = record.get('release_index')
        if isinstance(release, bool) or not isinstance(release, int) or not 0 <= release < len(cell['frames']):
            raise ValueError('Invalid release_index: '+name)
        for p in record['sockets']:
            if p is None:
                continue
            if not isinstance(p, list) or len(p) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v < 512 for v in p):
                raise ValueError('Invalid socket coordinate: '+name)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cells', required=True)
    parser.add_argument('--out')
    parser.add_argument('--all-cells', action='store_true')
    args = parser.parse_args()
    result = build_sockets(args.cells, args.out, args.all_cells)
    print(json.dumps({'cells': len(result['cells']), 'missing': sum(p is None for c in result['cells'].values() for p in c['sockets'])}))


if __name__ == '__main__':
    main()
