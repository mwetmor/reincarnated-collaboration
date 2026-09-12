K1-chk-04 deterministic checks

Processing and verification commands are reproduced exactly below. Python bytecode writes are disabled. Only frozen gate/oracle implementations are used for measurements; inline orchestration loads inputs, calls tools, saves returned masks and mattes, and packages result envelopes.

Actual inputs: J, K, L are 1024x1536 RGB, not the declared 1254x1254. Mattes preserve native dimensions. These outputs are CHECK artifacts, not registered 512x512 animation frames.
The authoritative output list supplies J/K/L names; the prose's _B_64 / _C_64 names are treated as a naming typo.
Matte character mode: preserve_particles=False, alpha_floor=40.
Plate support: supplied matte alpha >=128; tolerance 8; no minimum fraction declared.
G9 numeric booleans are unchanged frozen-tool results. Dark-fringe visual absence is not computable by this numeric tool; its threshold remains null.
O7 uses matted RGB and alpha, source scale, erosion_px=1. Value is azimuth in screen x-right/y-up degrees; circular_absolute_error_deg reports angular distance from 135. No tolerance declared.
O3b uses original RGB at source scale, sheet-wide, allowed_masks=None, radii 8-30, vote_thresh=0.50. Raw hollow_min=0.0; annulus-filtered hollow_min=0.5. All other frozen defaults retained. Both advisory with null thresholds/verdicts.
O5 saves descriptor['mask'] directly as a binary PNG. Frozen oracle uses a 64x64 canvas even for the non-square actual inputs. Summary gives 64px alpha area fraction and bbox height, with native bbox separately.
O8 compares matted source against F04_starter_native.png at matching analytical scales (source and 0.5), each with its own actual source dimensions. Anchor is 265x675 RGB without alpha, so its entire canvas is the support. Anchor is not chroma-keyed. Distances are descriptive and sensitive to differing support/canvas; no threshold declared.
O2 requested key-facing-edge measurement is unavailable: frozen separation has no edge/region mask input. A null envelope records this limitation. Whole-figure means/delta are supplied separately on explicitly assumed RGB [20,25,34], the frozen gates.common.pixels preview ground. No scene ground was supplied. Bible min_delta=0.08 is not applied because conversion to the tool's 0..255 luma units is undeclared.
No new measurement implementation, input edits, image generation, or registration.

EXACT PROCESSING COMMAND
mkdir -p out
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
from pathlib import Path
import numpy as np
from PIL import Image
from gates import plate_uniformity, matte, g9_alpha, matte_quality, common
from oracles import keylight, motif, silhouette64, grain, figure_ground
from oracles.common import report

root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
out = Path('out')
anchor_path = root / 'fixtures/x0t/F04_starter_native.png'
anchor = common.rgba(anchor_path)
anchor_alpha = np.asarray(anchor.getchannel('A'))
anchor_source = grain.band_energy(anchor, anchor_alpha, source_px=anchor.size, display_scale=None, subject='F04_starter_native/source')
anchor_display = grain.band_energy(anchor, anchor_alpha, source_px=anchor.size, display_scale=0.5, subject='F04_starter_native/display_0.5')
anchor_source_profile = json.loads(anchor_source['notes'])['metrics']['profile']
anchor_display_profile = json.loads(anchor_display['notes'])['metrics']['profile']
rows = []
for letter in ('J', 'K', 'L'):
    subject = 'k1_master_' + letter
    source_path = root / 'runs/C-1/artifacts/K1-gen-04' / (subject + '.png')
    source = common.rgba(source_path)
    extracted, extraction = matte.extract(source, preserve_particles=False, alpha_floor=40)
    rgba_path = out / (subject + '_rgba.png')
    extracted.save(rgba_path)
    alpha = np.asarray(extracted.getchannel('A'))
    rows.append(report('input_metadata', subject, None, metrics={'source_path': str(source_path), 'actual_size_px': list(source.size), 'declared_size_px': [1254,1254], 'output_size_px': list(extracted.size), 'extraction': extraction}, reason='Actual source dimensions differ from task declaration; native dimensions preserved, no registration requested.'))
    rows.append(plate_uniformity.measure(source, subject_alpha=alpha, tol=8, min_fraction=None, subject=subject))
    rows.extend(g9_alpha.evaluate(extracted, subject=subject, dark_threshold=None))
    rows.extend(matte_quality.measure(extracted, source, tol=20, halo_width_px=2, subject=subject))
    az = keylight.azimuth(extracted, alpha, key_azimuth_deg=135, tolerance=None, min_resultant=0, erosion_px=1, display_scale=None, subject=subject)
    az_metrics = json.loads(az['notes'])['metrics']
    az_metrics.update({'circular_absolute_error_deg': az['value'], 'key_azimuth_deg': 135, 'erosion_px': 1, 'display_scale': None})
    rows.append(report('O7', subject, az_metrics.get('azimuth_deg'), unit='degrees', metrics=az_metrics, reason='Value is circular mean azimuth; circular absolute error from 135 degrees is in metrics. Tolerance undeclared.'))
    raw = motif.count_family(source, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=0.50, allowed_masks=None, hollow_min=0.0, max_outside=None, subject=subject)
    raw['id'] = 'O3b.raw'
    rows.append(raw)
    filtered = motif.count_family(source, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=0.50, allowed_masks=None, hollow_min=0.5, max_outside=None, subject=subject)
    filtered['id'] = 'O3b.annulus_filtered'
    rows.append(filtered)
    descriptor = silhouette64.descriptor(extracted)
    silhouette = Image.fromarray(descriptor['mask'])
    silhouette_path = out / (subject + '_64.png')
    silhouette.save(silhouette_path)
    bbox64 = silhouette.getbbox()
    native_metrics = common.measure(extracted)
    rows.append(report('O5', subject, None, metrics={'alpha_area_fraction': descriptor['area']/descriptor['mask'].size, 'alpha_area_px': descriptor['area'], 'bbox_height_px': bbox64[3]-bbox64[1], 'bbox_xyxy': list(bbox64), 'canvas_px': [64,64], 'centroid': descriptor['centroid'], 'hu': descriptor['hu'], 'native_bbox_height_px': native_metrics['height'], 'native_bbox_xyxy': native_metrics['bbox']}, reason='Descriptor only; exact frozen oracle mask saved. Oracle resizes the non-square source to 64x64.'))
    for scale, profile, anchor_result, suffix in ((None, anchor_source_profile, anchor_source, 'source'), (0.5, anchor_display_profile, anchor_display, 'display_0.5')):
        row = grain.band_energy(extracted, alpha, source_px=source.size, anchor_profile=profile, display_scale=scale, threshold=None, subject=subject)
        row['id'] = 'O8.' + suffix
        notes = json.loads(row['notes'])
        notes['metrics'].update({'display_scale': scale, 'anchor_path': str(anchor_path), 'anchor_size_px': list(anchor.size), 'anchor_profile': profile, 'anchor_alpha_support': 'All pixels: RGB anchor has no alpha and is not a green plate.'})
        notes['reason'] = 'Descriptive distance only; anchor and candidates have different source dimensions and alpha support.'
        row['notes'] = json.dumps(notes, sort_keys=True, allow_nan=False)
        rows.append(row)
    fg = figure_ground.separation(extracted, background_rgb=(20,25,34), sign=1, min_delta=None, subject=subject)
    fg['id'] = 'O2.whole_figure_proxy'
    fg_notes = json.loads(fg['notes'])
    fg_notes['metrics']['background_rgb'] = [20,25,34]
    fg_notes['reason'] = 'Whole-figure proxy only. Ground RGB is the gates.common.pixels preview ground, not a supplied scene ground. Frozen separation has no key-facing-edge mask parameter. Bible min_delta 0.08 has no declared conversion to tool luma units; no threshold applied.'
    fg['notes'] = json.dumps(fg_notes, sort_keys=True, allow_nan=False)
    rows.append(fg)
    rows.append(report('O2.key_facing_edge', subject, None, unit='luma', reason='Cannot compute requested key-facing-edge inside/outside means using frozen figure_ground.separation: no edge-mask parameter; no reviewed edge mask or scene ground supplied. Whole-figure proxy reported separately.'))
    print(subject, 'matte saved', 'rings raw/filtered', raw['value'], filtered['value'], 'azimuth', az_metrics.get('azimuth_deg'), flush=True)

(out / 'checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
print('Wrote', len(rows), 'result envelopes.')
PY

EXACT VERIFICATION / HASH COMMAND
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json
import hashlib
from pathlib import Path
from PIL import Image
out = Path('out')
rows = json.loads((out / 'checks.json').read_text())
print('Envelope count:', len(rows))
print('Envelope keys:', sorted(rows[0]))
for row in rows:
    print(row['subject'], row['id'], 'value=', row['value'], 'threshold=', row['threshold'])
for path in sorted(out.iterdir()):
    if path.suffix == '.png':
        with Image.open(path) as im:
            print('IMAGE', path.name, im.size, im.mode)
    print('SHA256', path.as_posix(), hashlib.sha256(path.read_bytes()).hexdigest())
PY

