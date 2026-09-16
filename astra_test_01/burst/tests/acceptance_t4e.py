"""Read the T4e real peak and serialized pieces; write measurements, no verdict."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

from oracle.peak_pieces import isolate, quantise


def main():
    root = Path(__file__).resolve().parents[1]
    run = root/'runs/C-5/t3/T4e'
    source = root/'runs/C-5/artifacts/E0p-peak-01/fire_peak_01_512.png'
    output = run/'pieces'
    manifest = json.loads((output/'pieces.json').read_text())
    original = isolate(source)
    with Image.open(source) as im:
        source_alpha = np.array(im.convert('RGBA'))[..., 3]
    bands, alpha, histogram = quantise(original)
    support = alpha > 0
    union = np.zeros(alpha.shape, dtype=bool)
    counts = np.zeros(alpha.shape, dtype=np.uint32)
    summed_alpha = np.zeros(alpha.shape, dtype=np.uint32)
    piece_rows = []
    for p in manifest['pieces']:
        with Image.open(output/p['mask']) as im:
            a = np.array(im.convert('RGBA'))
            canvas_matches = list(im.size) == manifest['canvas']
        mask = a[..., 3] > 0
        union |= mask
        counts += mask
        summed_alpha += a[..., 3]
        px, py = np.floor(np.array(p['pivot'])+.5).astype(int)
        inside = bool(0 <= py < mask.shape[0] and 0 <= px < mask.shape[1] and mask[py, px])
        hist = np.bincount(bands[mask], minlength=4)
        minority = int(mask.sum()-hist[p['band_index']])
        yy, xx = np.where(mask)
        bbox = [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)]
        piece_rows.append(dict(id=p['id'], area_px=int(mask.sum()), metadata_area_matches=int(mask.sum()) == p['area_px'],
            alpha_area_px=float(a[..., 3].sum()/255), max_alpha=int(a[..., 3].max()),
            bbox_matches=bbox == p['bbox'], canvas_matches=canvas_matches,
            pivot=p['pivot'], pivot_inside=inside, pivot_adjusted=p['pivot_adjusted'],
            band_index=p['band_index'], band_histogram=hist.tolist(), minority_area_fraction=minority/int(mask.sum()),
            alpha_bytes_match=bool(np.array_equal(a[..., 3][mask], alpha[mask])),
            rgb_indices_match=bool(np.all(a[mask, :3] == bands[mask, None]*85)),
            connected_components=p['connected_components'], merged_slivers=p['merged_slivers']))
    with Image.open(output/'peak_index.png') as im:
        index = np.array(im)
    difference = int(np.count_nonzero(union ^ support))
    values = dict(piece_count=len(piece_rows), source_area_px=int(support.sum()), union_area_px=int(union.sum()),
        symmetric_difference_px=difference, symmetric_difference_fraction=difference/int(support.sum()),
        missing_pixels=int(np.count_nonzero(support & ~union)), extra_pixels=int(np.count_nonzero(union & ~support)),
        overlapping_pixels=int(np.count_nonzero(counts > 1)),
        alpha_sum_original=int(alpha.astype(np.uint64).sum()), alpha_sum_pieces=int(summed_alpha.sum()),
        alpha_reconstruction_exact=bool(np.array_equal(summed_alpha, alpha)),
        pivots_inside=sum(p['pivot_inside'] for p in piece_rows), pivots_outside=sum(not p['pivot_inside'] for p in piece_rows),
        max_piece_minority_fraction=max(p['minority_area_fraction'] for p in piece_rows),
        index_alpha_unchanged=bool(np.array_equal(index[..., 3], alpha)),
        index_rgb_matches=bool(np.all(index[support, :3] == bands[support, None]*85)),
        isolated_alpha_equals_png_alpha=bool(np.array_equal(alpha, source_alpha)),
        band_histogram=histogram, plate_path_used=manifest['plate_path_used'], isolation=manifest['isolation'],
        plane_quality=manifest['plane_quality'], pieces=piece_rows)
    concerns = []
    quality = manifest['plane_quality']
    if quality['more_than_four_source_levels']:
        concerns.append('Working peak has more than four source RGB levels; intermediate tones retained only through the specified nearest-band quantisation. No smoothing or stronger quantisation applied.')
    disconnected = [p['id'] for p in piece_rows if p['connected_components'] > 1]
    if disconnected:
        concerns.append('Same-band sliver unions produce disconnected masks for piece IDs '+str(disconnected)+'; distances and component counts are explicit in pieces.json.')
    faint = [dict(id=p['id'], area_px=p['area_px'], alpha_area_px=p['alpha_area_px'], max_alpha=p['max_alpha'])
             for p in piece_rows if p['max_alpha'] < 128]
    if faint:
        concerns.append('Very faint source components are retained under literal alpha>0 support: '+json.dumps(faint)+'. They count as pieces but may be invisible in the runtime; no coverage was discarded.')
    rows = []
    for name, value, threshold, unit in [
        ('piece_count', len(piece_rows), {'min': 6, 'max': 40}, 'pieces'),
        ('union_difference', difference/int(support.sum()), .005, 'fraction'),
        ('pivots_outside', values['pivots_outside'], 0, 'pieces'),
        ('max_minority_band', values['max_piece_minority_fraction'], .05, 'fraction')]:
        rows.append(dict(id='peak_pieces_'+name, subject=str(source.relative_to(root)), passed=None,
            value=value, threshold=threshold, op='report', unit=unit,
            evidence=[str((output/'pieces.json').relative_to(root))], notes='Conductor-owned acceptance; measurement only.'))
    report = dict(task_id='T4e', source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        measurements=values, results=rows, concerns=concerns,
        synthetic_tests=dict(tests_run=9, successful=True, red_names=[],
            command='PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p test_peak_pieces.py -v',
            invocation_retry='Initial tests.test_peak_pieces import failed because tests is not an importable package; discovery succeeded without code changes.'),
        read_scope_deviation='Initial SPEC extraction displayed additional section 7 rows beyond the requested intro, T4e and T4h rows.')
    if (run/'suite_report.json').is_file():
        suite = json.loads((run/'suite_report.json').read_text())
        report['full_suite'] = {k: suite[k] for k in (
            'tests_run', 'successful', 'successful_tests', 'elapsed_s', 'red_names',
            'standing_red_names', 'additional_red_names', 'errors', 'skipped', 'exit_code')}
        report['suite_write_scope_deviation'] = suite['write_scope_deviation']
    (run/'acceptance.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k: v for k, v in values.items() if k not in ('pieces', 'plane_quality')}, indent=2))
    print(json.dumps({k: v for k, v in quality.items() if k != 'luminance_histogram'}, indent=2))


if __name__ == '__main__':
    main()
