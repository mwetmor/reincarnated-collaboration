K1-chk-02 frozen CHECK commands and measurement notes

All image outputs preserve the native source geometry except the exact frozen
O5 analytical 64x64 binary descriptor render. Explicit output names D/E/F take
precedence over the task prose's stray _B_64/_C_64 labels.
Source inputs are actually 1024x1536 RGB, not the stated 1254x1254.
No artwork registration is performed.
O7 value is the circular mean azimuth; notes retain circular error and |value-135|.
O3b raw disables only the annulus filter with hollow_min=0; filtered uses 0.5.
O8 uses the RGB anchor's entire opaque rectangular support, with separate anchor
profiles at native scale and display_scale=0.5; no subject mask was supplied.
O2 whole-figure numbers use the declared green plate as diagnostic ground.
Key-facing-edge O2 is unavailable with the frozen signature and is recorded null.
No undeclared thresholds are inferred. Frozen G9 booleans are retained.
PYTHONDONTWRITEBYTECODE prevents writes to the read-only frozen tool directories.
The inline Python only orchestrates frozen measurements and serializes their
results; no new measurement implementation or persistent code file is created.

Exact measurement command:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
from pathlib import Path
from PIL import Image
import numpy as np
from gates import plate_uniformity, matte, g9_alpha, matte_quality
from gates.common import measure, rgba
from oracles import keylight, motif, silhouette64, grain, figure_ground
from oracles.common import report

root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
out = Path('out')
anchor_path = root / 'fixtures/x0t/F04_starter_native.png'
anchor = rgba(anchor_path)
anchor_alpha = np.asarray(anchor.getchannel('A'))
anchor_profiles = {}
for scale in (None, 0.5):
    anchor_result = grain.band_energy(anchor, anchor_alpha, source_px=list(anchor.size), display_scale=scale, subject='F04_starter_native')
    anchor_profiles[scale] = json.loads(anchor_result['notes'])['metrics']['profile']

rows = []
for letter in 'DEF':
    subject = 'k1_master_' + letter
    source_path = root / 'runs/C-1/artifacts/K1-gen-02' / (subject + '.png')
    source = Image.open(source_path)
    extracted, matte_metadata = matte.extract(source, preserve_particles=False, alpha_floor=40)
    rgba_path = out / (subject + '_rgba.png')
    extracted.save(rgba_path)
    alpha = np.asarray(extracted.getchannel('A'))
    rows.append(report('input_geometry', subject, list(source.size), unit='pixels', metrics={'expected_size': [1254, 1254], 'actual_mode': source.mode, 'registration_applied': False}, reason='Source is 1024x1536, not stated 1254x1254; preserved native geometry.'))
    rows.append(report('matte_extract', subject, None, metrics=matte_metadata, reason='Extraction metadata; character mode, alpha_floor=40.'))
    rows.append(plate_uniformity.measure(source, subject_alpha=alpha, tol=8, min_fraction=None, subject=subject))
    rows.extend(g9_alpha.evaluate(extracted, subject=subject, dark_threshold=None))
    rows.extend(matte_quality.measure(extracted, source, tol=20, halo_width_px=2, subject=subject))
    light = keylight.azimuth(extracted, alpha, key_azimuth_deg=135, tolerance=None, min_resultant=0, erosion_px=1, subject=subject)
    light_notes = json.loads(light['notes'])
    light_metrics = light_notes['metrics']
    light_metrics['circular_absolute_error_deg'] = light['value']
    light_metrics['key_azimuth_deg'] = 135
    angle = light_metrics.get('azimuth_deg')
    light_metrics['absolute_value_minus_135_deg'] = None if angle is None else abs(angle - 135)
    rows.append(report('O7', subject, angle, unit='degrees', metrics=light_metrics, reason=light_notes['reason'] or 'Circular mean azimuth; tolerance undeclared. Luminance-gradient proxy, not a direct light-source estimate.'))
    for hollow_min, variant in ((0.0, 'raw'), (0.5, 'annulus_filtered')):
        count = motif.count_family(source, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=0.50, allowed_masks=None, hollow_min=hollow_min, max_outside=None, subject=subject)
        count_notes = json.loads(count['notes'])
        count_notes['metrics']['variant'] = variant
        count_notes['metrics']['input_domain'] = 'raw RGB source, entire sheet, no allowed masks'
        count['notes'] = json.dumps({'metrics': count_notes['metrics'], 'reason': 'Advisory only; no count verdict. raw uses hollow_min=0.0; annulus_filtered uses frozen default 0.5.'}, sort_keys=True, allow_nan=False)
        rows.append(count)
    desc = silhouette64.descriptor(extracted)
    silhouette = Image.fromarray(desc['mask'].astype('uint8') * 255, 'L')
    silhouette_path = out / (subject + '_64.png')
    silhouette.save(silhouette_path)
    silhouette_measure = measure(Image.merge('RGBA', (silhouette, silhouette, silhouette, silhouette)))
    native_measure = measure(extracted)
    rows.append(report('O5', subject, desc['area'] / 4096, unit='alpha_area_fraction', metrics={'canvas_px': [64, 64], 'alpha_area_px': int(desc['area']), 'bbox_height_px': silhouette_measure['height'], 'bbox': silhouette_measure['bbox'], 'centroid': desc['centroid'], 'hu': desc['hu'], 'native_bbox_height_px': native_measure['height'], 'native_bbox': native_measure['bbox'], 'silhouette_path': str(silhouette_path)}, reason='Descriptor report only. Frozen oracle resizes to 64x64; rectangular source is therefore anisotropically reduced for this analytical diagnostic, not registered artwork.'))
    for scale in (None, 0.5):
        texture = grain.band_energy(extracted, alpha, source_px=list(source.size), anchor_profile=anchor_profiles[scale], threshold=None, display_scale=scale, subject=subject)
        texture_notes = json.loads(texture['notes'])
        texture_notes['metrics'].update({'display_scale': 1.0 if scale is None else scale, 'anchor_path': str(anchor_path), 'anchor_source_px': list(anchor.size), 'anchor_profile': anchor_profiles[scale], 'anchor_alpha_support': 'Full rectangular crop: RGB input has no supplied alpha mask.'})
        texture['notes'] = json.dumps({'metrics': texture_notes['metrics'], 'reason': 'Descriptive L2 distance only; threshold undeclared. Anchor is 265x675 RGB with full-crop support, candidate uses extracted alpha; source dimensions and support differ.'}, sort_keys=True, allow_nan=False)
        rows.append(texture)
    separation = figure_ground.separation(extracted, background_rgb=[0,255,0], sign=1, min_delta=None, subject=subject)
    separation_notes = json.loads(separation['notes'])
    separation_notes['metrics'].update({'background_rgb': [0,255,0], 'sampling_scope': 'whole foreground and outside alpha, not key-facing edge'})
    separation['notes'] = json.dumps({'metrics': separation_notes['metrics'], 'reason': 'Green-plate diagnostic only. No scene ground RGB or key-facing-edge mask supplied; frozen O2 has no edge/mask parameter. No threshold applied.'}, sort_keys=True, allow_nan=False)
    rows.append(separation)
    rows.append(report('O2.key_facing_edge', subject, None, unit='luma', reason='Cannot compute requested key-facing-edge separation: frozen O2 samples whole foreground/outside alpha only and accepts no edge mask; scene background RGB is also unspecified.'))
    for row in rows:
        if row['subject'] == subject and not row['evidence']:
            row['evidence'] = [str(source_path), str(rgba_path)]
    print(subject, 'completed', 'O7', angle, 'silhouette_height', silhouette_measure['height'], flush=True)

(out / 'checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
print('Wrote', len(rows), 'result envelopes.', flush=True)
PY

Exact verification and hash command:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
from pathlib import Path
from PIL import Image
import numpy as np
from oracles.silhouette64 import descriptor
rows = json.loads(Path('out/checks.json').read_text())
print('Envelope count:', len(rows))
print('Envelope fields:', sorted(rows[0]))
for letter in 'DEF':
    subject = 'k1_master_' + letter
    rgba_image = Image.open('out/' + subject + '_rgba.png')
    silhouette = Image.open('out/' + subject + '_64.png')
    print(subject, 'RGBA:', rgba_image.size, rgba_image.mode, 'silhouette:', silhouette.size, silhouette.mode,
          'matches frozen descriptor:', np.array_equal(np.asarray(silhouette), descriptor(rgba_image)['mask'].astype('uint8') * 255))
    for row in rows:
        if row['subject'] == subject:
            print(row['id'], 'value=', row['value'], 'threshold=', row['threshold'])
PY
shasum -a 256 out/checks.json out/checks_readme.txt out/k1_master_D_rgba.png out/k1_master_E_rgba.png out/k1_master_F_rgba.png out/k1_master_D_64.png out/k1_master_E_64.png out/k1_master_F_64.png
