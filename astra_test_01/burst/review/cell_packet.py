"""Portable, offline review packet for exactly one registered cut cell."""
import argparse
import html
import json
import math
from pathlib import Path
import re
import shutil
import time
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from .encode import encode_loop, seam_pairs_png, strip_png, _positive

FPS = {'idle': 8, 'rest': 8, 'walk': 12, 'run': 12, 'jump': 12, 'cast': 20}


def flatten_checks(checks):
    """Flatten metric leaves; propagate proposal status through containers/bands.

    Existing passed values are copied, never recomputed. Either proposed=true
    or committed=false at any ancestor or in a leaf's band forces null.
    """
    rows = []
    def visit(node, path='', report_only=False):
        if isinstance(node, list):
            for i, child in enumerate(node):
                visit(child, f'{path}/{i}'.strip('/'), report_only)
        elif isinstance(node, dict):
            band = node.get('band', {})
            if not isinstance(band, dict):
                band = {}
            proposed = (report_only or node.get('proposed') is True or node.get('committed') is False
                        or band.get('proposed') is True or band.get('committed') is False)
            if 'value' in node:
                bounds = {key: band.get(key, node.get(key)) for key in ('floor', 'target', 'ceiling')}
                threshold = node.get('threshold')
                if isinstance(threshold, dict):
                    for key in bounds:
                        if bounds[key] is None:
                            bounds[key] = threshold.get(key)
                    proposed |= threshold.get('proposed') is True or threshold.get('committed') is False
                elif threshold is not None:
                    key = {'<=': 'ceiling', '>=': 'floor', '==': 'target'}.get(node.get('op'))
                    if key and bounds[key] is None:
                        bounds[key] = threshold
                rows.append({'name': str(node.get('name', node.get('id', path or 'value'))),
                             'subject': node.get('subject', ''), 'value': node['value'],
                             'band': bounds, 'passed': None if proposed else node.get('passed'),
                             'proposed': bool(proposed), 'unit': node.get('unit', ''),
                             'notes': node.get('notes', '')})
            else:
                for key, child in node.items():
                    if isinstance(child, (list, dict)) and key not in ('band', 'proposed_from'):
                        visit(child, f'{path}/{key}'.strip('/'), proposed)
    visit(checks)
    return rows


def _cell(cell):
    cell = Path(cell)
    root = cell/'frames' if (cell/'frames').is_dir() else cell
    groups = {}
    for f in sorted(root.rglob('*.png')):
        if 'rest' not in f.relative_to(root).parts[:-1]:
            groups.setdefault(f.parent, []).append(f)
    if len(groups) != 1:
        raise ValueError('Cell must contain exactly one animation/direction frame sequence (excluding rest)')
    folder, frames = next(iter(groups.items()))
    pieces = frames[0].stem.split('_')
    kind = pieces[0]
    if kind not in FPS or len(pieces) < 2:
        raise ValueError('Frame names must identify animation and direction')
    direction = pieces[1]
    if direction not in ('S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE'):
        raise ValueError('Unknown frame direction')
    name = f'{kind}_{direction}'
    if any(not re.fullmatch(re.escape(name)+r'_(\d+)\.png', f.name) for f in frames):
        raise ValueError('Inconsistent frame names')
    frames.sort(key=lambda f: int(f.stem.rsplit('_', 1)[1]))
    indices = [int(f.stem.rsplit('_', 1)[1]) for f in frames]
    if indices != list(range(len(frames))):
        raise ValueError('Frame indices must be contiguous and start at zero')
    metadata = json.loads((cell/'registration.json').read_text()) if (cell/'registration.json').is_file() else {}
    # Legacy fps is NATIVE fps. Only explicit output-fps keys override charter.
    fps = _positive(metadata.get('fps_out', metadata.get('fps_output', FPS[kind])), 'fps_out')
    return frames, kind, direction, name, fps


class _References(HTMLParser):
    def __init__(self):
        super().__init__(); self.paths = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src', 'href', 'poster') and value is not None:
                self.paths.append(value)
            if key in ('srcset', 'style'):
                raise ValueError('Inline asset URLs/srcset are not allowed in packet markup')


def validate_packet_html(path):
    """Reject external, absolute, escaping, missing, and symlink-outside assets."""
    path = Path(path)
    parser = _References(); parser.feed(path.read_text())
    root = path.parent.resolve()
    for ref in parser.paths:
        decoded = unquote(ref)
        url = urlsplit(decoded)
        target = (root/url.path).resolve()
        if (url.scheme or url.netloc or decoded.startswith(('/', '\\')) or '\\' in decoded
                or not target.is_relative_to(root) or not target.is_file()):
            raise ValueError('Nonlocal or missing packet reference: '+ref)
    return parser.paths


def build_packet(cell, checks, out, oracle=None, oracle_fps=None):
    started = time.monotonic()
    frames, kind, direction, name, fps = _cell(cell)
    if oracle is not None:
        if oracle_fps is None:
            raise ValueError('--oracle-fps is required with --oracle')
        oracle_fps = _positive(oracle_fps, 'oracle_fps')
        oracle_frames = sorted(Path(oracle).glob('*.png'))
        if not oracle_frames:
            raise ValueError('Oracle directory contains no PNG frames')
    if isinstance(checks, (str, Path)):
        checks = json.loads(Path(checks).read_text())
    numbers = flatten_checks(checks)
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    (out/'img').mkdir(exist_ok=True)
    # Full sequence, then an additional half second on the final pose.
    # Non-integral frame rates quantize the hold to nearest frame (half-up).
    hold = math.floor(fps*0.5+0.5) if kind in ('jump', 'cast') else 0
    playback = frames + [frames[-1]]*hold
    for scale, suffix in ((2, '2x'), (1, '1to1')):
        encode_loop(playback, fps, out/f'{name}_{suffix}.mp4', scale=scale)
    if oracle is not None:
        encode_loop(oracle_frames, oracle_fps, out/'oracle.mp4', scale=1)
    seam_pairs_png(frames, out/'seam_pairs.png')
    strip_png(frames, out/'strip.png')
    for filename in ('seam_pairs.png', 'strip.png'):
        shutil.copyfile(out/filename, out/'img'/filename)
    (out/'numbers.json').write_text(json.dumps(numbers, indent=2, allow_nan=False)+'\n')
    esc = lambda value: html.escape(str(value), quote=True)
    videos = ''.join(f'<section><h2>{label}</h2><video controls loop muted playsinline preload="metadata" src="{filename}"></video></section>'
                     for label, filename in [('2× Lanczos', f'{name}_2x.mp4'), ('1:1 game scale', f'{name}_1to1.mp4')]
                     + ([('Oracle', 'oracle.mp4')] if oracle is not None else []))
    rows = ''.join('<tr>'+''.join(f'<td>{esc(value)}</td>' for value in
                    (row['name'], row['value'], row['band']['floor'], row['band']['target'],
                     row['band']['ceiling'], 'null (report only)' if row['proposed'] else json.dumps(row['passed'])))+'</tr>'
                   for row in numbers)
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{name} review</title>
<style>body{{background:#20242c;color:#eceff4;font:16px/1.5 system-ui;margin:24px}}video{{display:block;max-width:100%;height:auto}}section{{margin-bottom:24px}}.strip{{overflow:auto}}table{{border-collapse:collapse}}td,th{{padding:8px;border:1px solid #697383;text-align:left}}a{{color:#b8d6ff}}</style>
</head><body><h1>{name}</h1><p>{len(frames)} frames at {fps:g} fps; five encoded repeats.
{('Each repeat holds the final pose for '+str(hold/fps)+' s.') if hold else 'Loop playback.'}</p>{videos}
<h2>Seam: last | first | absolute difference ×4</h2><div class="strip"><img src="img/seam_pairs.png" alt="Seam comparison"></div>
<h2>Numbered frames (zero based)</h2><div class="strip"><img src="img/strip.png" alt="Numbered frame strip"></div>
<h2>Measurements</h2><table><thead><tr><th>Name</th><th>Value</th><th>Floor</th><th>Target</th><th>Ceiling</th><th>Recorded passed</th></tr></thead><tbody>{rows}</tbody></table>
<p><a href="numbers.json">Numbers JSON</a> · <a href="summary.txt">Summary</a></p></body></html>'''
    (out/'review.html').write_text(document)
    wall = time.monotonic()-started
    summary = [f'Cell: {name}', f'Frames: {len(frames)}', f'Playback fps: {fps:g}',
               'Encodes: H.264 yuv420p; Lanczos 2x and 1:1; five repeats',
               f'Final-pose extra hold per repeat: {hold/fps:g} s',
               'Seam image: last | first | absolute RGB difference x4 on #3a3f4a',
               f'Measurements: {len(numbers)}; report-only rows: {sum(r["proposed"] for r in numbers)}',
               f'Oracle: {"included" if oracle is not None else "not supplied"}',
               f'Build wall seconds: {wall:.6f} (criterion <= 120)',
               'Proposed/uncommitted measurements retain null; no gates recomputed.']
    (out/'summary.txt').write_text('\n'.join(summary)+'\n')
    references = validate_packet_html(out/'review.html')
    return {'cell': name, 'fps': fps, 'frames': len(frames), 'hold_frames': hold,
            'wall_s': time.monotonic()-started, 'references': references}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('cell', 'checks', 'out'):
        parser.add_argument('--'+name, required=True)
    parser.add_argument('--oracle')
    parser.add_argument('--oracle-fps', type=float)
    args = parser.parse_args()
    print(json.dumps(build_packet(args.cell, args.checks, args.out, args.oracle, args.oracle_fps), indent=2))


if __name__ == '__main__':
    main()
