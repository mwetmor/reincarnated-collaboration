"""Rebuild lossless evidence packing and measure the ASTRA turnaround checkpoint.

No generated art, background removal, relighting, mirroring, or pose fabrication.
Opaque inputs remain opaque; unavailable silhouette measurements remain null.
Run: python3 astra_test_01/check.py [--attempt 1|2]
Exit 1 means the asset checkpoint failed; exit 0 requires all checkpoint gates.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
DIRS = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']


def measure(path, feet):
    original = Image.open(path)
    rgba = original.convert('RGBA')
    assert min(rgba.size) >= 512, 'Upscaling forbidden'
    assert rgba.width == rgba.height, 'Unexpected aspect ratio'
    frame = rgba.resize((512, 512), Image.Resampling.LANCZOS)
    arr = np.array(frame)
    a = arr[:, :, 3]
    transparent = int((a == 0).sum())
    valid_alpha = 'A' in original.getbands() and transparent > 0
    result = {
        'source': str(path.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'source_mode': original.mode, 'source_size': list(original.size),
        'frame_size': [512, 512], 'transparent_pixels': transparent,
        'transparent_percent': round(100 * transparent / a.size, 4),
        'alpha_usable': valid_alpha,
        'bbox': None, 'height': None, 'light_centroid': None,
        'light_pass': None,
    }
    if valid_alpha:
        mask = a >= 128
        ys, xs = np.where(mask)
        bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        luminance = arr[:, :, :3].astype(float) @ np.array([0.2126, 0.7152, 0.0722])
        count = max(1, math.ceil(len(xs) * 0.05))
        # Stable sort fixes tie handling; select exactly ceil(5%) of silhouette.
        selected = np.argsort(luminance[mask], kind='stable')[-count:]
        centroid = [float(xs[selected].mean()), float(ys[selected].mean())]
        center = [(bbox[0] + bbox[2] - 1) / 2, (bbox[1] + bbox[3] - 1) / 2]
        result.update(bbox=bbox, height=bbox[3] - bbox[1],
                      light_centroid=centroid, silhouette_center=center,
                      light_pass=bool(centroid[0] < center[0] and centroid[1] < center[1]),
                      brightest_sample_count=count)
    if feet:
        points = np.array(feet, dtype=float) * 512 / np.array(original.size)
        pivot = points.mean(axis=0)
        delta = pivot - [256, 400]
        result.update(sole_points=points.tolist(), foot_midpoint=pivot.tolist(),
                      pivot_delta=delta.tolist(), pivot_max_axis_error=float(abs(delta).max()),
                      pivot_pass=bool((abs(delta) <= 4).all()))
    else:
        result.update(sole_points=None, foot_midpoint=None, pivot_pass=None)
    return frame, result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    annotations = json.loads((ROOT / 'annotations.json').read_text())
    evidence = ROOT / 'evidence' / f'turnaround_{args.attempt}'
    evidence.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGBA', (512 * 8, 512))
    overlay = Image.new('RGBA', (512 * 8, 552), '#171c27')
    rows = {}
    for col, direction in enumerate(DIRS):
        path = ROOT / 'source' / 'turnaround_1' / f'{direction}.png'
        candidate = ROOT / 'source' / 'turnaround_2' / f'{direction}.png'
        replaced = args.attempt == 2 and candidate.exists()
        if replaced:
            path = candidate
        key = f'{args.attempt if replaced else 1}/{direction}'
        frame, row = measure(path, annotations.get(key))
        rows[direction] = row
        folder = evidence / 'frames' / direction
        folder.mkdir(parents=True, exist_ok=True)
        frame.save(folder / f'idle_{direction}_00.png')
        sheet.paste(frame, (col * 512, 0))
        overlay.alpha_composite(frame, (col * 512, 40))
        draw = ImageDraw.Draw(overlay)
        ox = col * 512
        draw.text((ox + 12, 12), direction + (' / alpha OK' if row['alpha_usable'] else ' / OPAQUE: FAIL'), fill='white')
        draw.line((ox + 246, 440, ox + 266, 440), fill='#ff5577', width=2)
        draw.line((ox + 256, 430, ox + 256, 450), fill='#ff5577', width=2)
        for px, py in row['sole_points'] or []:
            draw.ellipse((ox + px - 3, py + 37, ox + px + 3, py + 43), fill='#40e5cb')
        if row['foot_midpoint']:
            x, y = row['foot_midpoint']
            draw.line((ox + x, y + 40, ox + 256, 440), fill='#40e5cb', width=2)
        if row['bbox']:
            x0, y0, x1, y1 = row['bbox']
            draw.rectangle((ox + x0, 40 + y0, ox + x1, 40 + y1), outline='#ffcc66', width=1)
            x, y = row['light_centroid']
            draw.ellipse((ox+x-4, y+36, ox+x+4, y+44), fill='#ffcc66')
    s_height = rows['S']['height']
    for row in rows.values():
        row['height_deviation_percent'] = None if row['height'] is None else 100 * (row['height'] / s_height - 1)
    judgments = json.loads((ROOT / 'visual_judgments.json').read_text())[str(args.attempt)]
    results = {
        'attempt': args.attempt,
        'measurement_scope': 'Only idle frame 00, eight directions. Animation gates untested.',
        'feet_method': 'Manual visible-sole endpoints, midpoint; annotations in source pixels, approximate +/- 6 source px. No automatic staff-tip proxy.',
        'directions': rows,
        'gate_1': 'PASS' if all(r['height'] is not None and abs(r['height_deviation_percent']) <= 3 for r in rows.values()) else 'FAIL / missing valid silhouette or outside tolerance',
        'gate_2': 'PASS' if all(r['pivot_pass'] is True for r in rows.values()) else 'FAIL / absent or out-of-tolerance contact',
        'gate_3': 'PASS' if all(r['light_pass'] is True for r in rows.values()) else 'FAIL / missing valid silhouette or wrong centroid',
        'gate_4': judgments['gate_4'],
        'gate_7': judgments['gate_7'],
    }
    passed = (all(results[g] == 'PASS' for g in ['gate_1', 'gate_2', 'gate_3'])
              and all(judgments[g]['pass'] for g in ['gate_4', 'gate_7']))
    results['status'] = 'PASS' if passed else 'FAIL'
    sheet.save(evidence / 'turnaround.png')
    sheet.resize((512, 64), Image.Resampling.LANCZOS).save(evidence / 'turnaround_64px.png')
    sheet.resize((1024, 128), Image.Resampling.LANCZOS).save(evidence / 'contact.png')
    overlay.save(evidence / 'measurement_overlay.png')
    (evidence / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
