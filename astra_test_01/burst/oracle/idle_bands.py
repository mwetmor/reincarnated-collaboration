"""CLI for numeric idle bands and optional Pillow-only diagnostic plots.

Reference pixels are never written into the repository. --ref plots require
an explicit outside-repository directory; --ours plots may live in the repo's
runs/C-1/oracle directory. JSON contains numbers and provenance only. Reference
rows merge by label. Measuring --ours does not turn a candidate into a reference.
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .idle_curves import CALIBRATION, EPS, FLOOR, TAU, amplitude, curves
from .motion_map import alpha_box, frame_paths, load_frames

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
OURS_ROOT = ROOT / 'runs/C-1/oracle'


def _band(value):
    return {name: value*factor if value is not None else None
            for name, factor in (('floor', .6), ('target', 1.), ('ceiling', 1.5))}


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False)+'\n')


def _plots(directory, label, frames, data):
    directory.mkdir(parents=True, exist_ok=True)
    palette = [(230, 100, 100), (70, 170, 250), (210, 180, 70),
               (100, 210, 120), (180, 120, 240), (240, 150, 60), (100, 210, 210)]
    check = Image.fromarray(frames[0]).convert('RGB')
    draw = ImageDraw.Draw(check)
    for (name, box), colour in zip(data['regions'].items(), palette):
        x0, y0, x1, y1 = box
        draw.rectangle((x0, y0, x1-1, y1-1), outline=colour, width=1)
        draw.text((x0+2, y0+1), name, fill=colour)
    if data['control_box']:
        cx0, cy0, cx1, cy1 = data['control_box']
        draw.rectangle((cx0, cy0, cx1-1, cy1-1), outline='cyan', width=2)
        draw.text((cx0, max(0, cy0-12)), 'background control', fill='cyan')
    x0, y0, x1, y1 = data['box']
    draw.rectangle((x0, y0, x1-1, y1-1), outline='white', width=1)
    draw.text((5, 5), f'{label} box={data["box"]}', fill='white', stroke_width=1,
              stroke_fill='black')
    check_path = directory / f'{label}_box_check.png'
    check.save(check_path)

    plot = Image.new('RGB', (1100, 930), (22, 26, 35))
    draw = ImageDraw.Draw(plot)
    draw.text((25, 15), f'{label}: geometric displacement curves; H={data["height"]} px', fill='white')
    draw.text((25, 32), f'tau={data["tau"]} eps={data["eps"]} floor={data["floor"]}; '
              f'VOID frames={data["void_frames"]}', fill='white')
    panels = [('regional changed-pixel energy', data['energy_by_region'], False),
              ('chest tracked edge width / H', {'chest_dw_H': data['chest_dw_H']}, True),
              ('head vertical displacement from median / H', {'head_dy_H': data['head_dy_H']}, True)]
    n = data['frames']
    for panel, (title, series, shaded) in enumerate(panels):
        top, bottom = 95+panel*270, 280+panel*270
        left, right = 90, 1040
        values = [float(v) for row in series.values() for v in row if v is not None]
        lo, hi = (min(values), max(values)) if values else (0., 1.)
        band_values = None
        if shaded and values:
            a = amplitude(values)
            mid = float(np.median(values))
            band_values = (mid, a)
            lo, hi = min(lo, mid-.75*a), max(hi, mid+.75*a)
        pad = max((hi-lo)*.1, .001)
        lo, hi = lo-pad, hi+pad
        yy = lambda v: int(bottom-(float(v)-lo)/(hi-lo)*(bottom-top))
        xx = lambda i: int(left+i/max(1, n-1)*(right-left))
        draw.text((left, top-28), title, fill='white')
        if band_values:
            mid, a = band_values
            for factor, colour in ((1.5, (40, 48, 60)), (1., (50, 65, 77)), (.6, (60, 80, 90))):
                draw.rectangle((left, yy(mid+factor*a/2), right, yy(mid-factor*a/2)), fill=colour)
        for tick in np.linspace(lo, hi, 5):
            y = yy(tick)
            draw.line((left, y, right, y), fill=(65, 70, 80))
            draw.text((10, y-5), f'{tick:.4f}', fill='white')
        for j, (name, row) in enumerate(series.items()):
            colour = palette[j]
            previous = None
            for i, value in enumerate(row):
                if value is None:
                    previous = None
                    continue
                point = (xx(i), yy(value))
                if previous is not None:
                    draw.line((*previous, *point), fill=colour, width=2)
                draw.ellipse((point[0]-2, point[1]-2, point[0]+2, point[1]+2), fill=colour)
                previous = point
            draw.text((left+j*130, bottom+26), name, fill=colour)
        draw.text((left, bottom+8), '0 s', fill='white')
        draw.text((right-65, bottom+8), f'{(n-1)/data["fps"]:.3f} s', fill='white')
    draw.text((25, 894), 'Shading: median +/- half of amplitude bands (0.6x / 1.0x / 1.5x). Provisional; no shipping verdict.', fill='white')
    path = directory / f'{label}_curves.png'
    plot.save(path)
    return [str(check_path), str(path)]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--ref', type=Path)
    source.add_argument('--ours', type=Path)
    parser.add_argument('--box')
    parser.add_argument('--control_box', help='optional background-only XYXY box, same size')
    parser.add_argument('--fps', required=True, type=float)
    parser.add_argument('--label', required=True)
    parser.add_argument('--out', type=Path, default=Path('oracle/bands_idle.json'))
    parser.add_argument('--plot_dir', type=Path)
    parser.add_argument('--tau', type=float, default=TAU)
    parser.add_argument('--eps', type=float, default=EPS)
    parser.add_argument('--floor', type=float, default=FLOOR)
    args = parser.parse_args(argv)
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.label):
        parser.error('label must contain only letters, digits, underscores, hyphens')
    if args.ref and not args.box:
        parser.error('--ref requires --box')
    if args.ours and args.box:
        parser.error('--ours derives its box from the complete alpha support union')
    directory = (args.ref or args.ours).resolve()
    plot_dir = args.plot_dir.resolve() if args.plot_dir else None
    if plot_dir and args.ref and plot_dir.is_relative_to(REPOSITORY):
        parser.error('reference plots must be outside the repository')
    if plot_dir and args.ours and plot_dir.is_relative_to(ROOT) and not plot_dir.is_relative_to(OURS_ROOT):
        parser.error('in-repository sprite plots must be under runs/C-1/oracle')
    try:
        box = ([int(v) for v in args.box.split(',')] if args.ref else alpha_box(directory))
        control_box = [int(v) for v in args.control_box.split(',')] if args.control_box else None
        data = curves(directory, box, args.fps, args.tau, args.eps, args.floor,
                      control_box=control_box, ours=bool(args.ours))
    except ValueError as exc:
        parser.error(str(exc))
    provenance = {'source_note': ('class-E reference; source pixels remain outside repository: '
                                 if args.ref else 'own registered sprite: ')+str(directory),
                  'frames': data['frames'], 'fps': args.fps, 'box': box,
                  'tau': data['tau'], 'eps': data['eps'], 'floor': data['floor'],
                  'calibration_note': CALIBRATION, 'control_box': data['control_box'],
                  'noise_calibration': data['noise_calibration'], 'estimator': data['estimator'],
                  'frame_names': [p.name for p in frame_paths(directory)]}
    data['provenance'] = provenance
    s = data['summary']
    if plot_dir:
        data['result']['evidence'] = _plots(plot_dir, args.label, load_frames(directory), data)
    if args.ref:
        out = args.out.resolve()
        existing = json.loads(out.read_text()) if out.exists() else {}
        existing[args.label] = {
            'breath_amplitude_H': _band(s['breath_amplitude_H']),
            'breath_period_s': s['breath_period_s'],
            'head_sway_H': _band(s['head_sway_H']),
            'lock_regions': s['LOCK'], 'motion_regions': s['MOTION'],
            'moving_count': s['moving_count'], 'provenance': provenance,
            'void_frames': data['void_frames'], 'result': data['result'],
            'contamination': data['contamination'], 'summary': s,
            'curves': data, 'committed': False}
        _write(out, existing)
    else:
        out = OURS_ROOT / f'{args.label}_ours.json'
        _write(out, data)
    print(json.dumps({'label': args.label, 'out': str(out), 'summary': s,
                      'box': box, 'void_frames': data['void_frames'],
                      'parameters': {'tau': data['tau'], 'eps': data['eps'], 'floor': data['floor']}},
                     allow_nan=False, sort_keys=True))


if __name__ == '__main__':
    main()
