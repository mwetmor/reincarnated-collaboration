K1-chk-03 deterministic CHECK command record
Working directory: /Users/admin/astra-burst/runs/C-1/K1-chk-03
No image generation. Frozen modules were imported without modification.
PYTHONDONTWRITEBYTECODE=1 prevents bytecode writes beside frozen tools.
Only out/ receives output files.

Interpretation and limitations:
- Both named inputs are RGB 1024x1536, not declared 1254x1254. Matte diagnostics remain native size; these are not registered 512x512 sprite frames.
- The explicit TASK.outputs list controls naming: G and H matte and silhouette outputs. The stray "_rgba.png" and "_B_64" in the prose are treated as typos.
- Character matte uses preserve_particles=False and alpha_floor=40. Plate uniformity uses frozen inferred largest-component support, tol=8, no minimum fraction.
- G9 booleans are frozen tool outputs. No overall verdict is declared. Numeric dark-fringe tolerance is undeclared; visual absence of a halo cannot be established by the numeric screen.
- O7 value is the frozen measured circular mean azimuth, screen x right/y up. Original circular error and literal absolute difference from 135 degrees are both retained in notes.metrics. No tolerance is declared.
- O3b raw uses hollow_min=0; annulus-filtered uses hollow_min=0.5. Both use source green plate, ring radii 8..30, vote_thresh=0.50, no allowed masks, no acceptance threshold. Remaining defaults are frozen.
- O5 PNGs are exactly the descriptor's binary masks, black=outside and white=inside. The frozen oracle uses fixed 64x64, including for these portrait sources; this diagnostic reduction changes aspect ratio. Native matte is not resized. Area fraction and bbox height are recorded at both native and descriptor scales.
- O8 uses source_px equal to each image's actual width/height, at source and display_scale=0.5. The RGB anchor has no alpha mask and includes its background. Anchor dimensions 265x675 differ from candidate dimensions; distances are descriptive and uncalibrated.
- O2 whole-figure values use background RGB [20,25,34], the ground in gates.common.pixels. This is an explicitly chosen diagnostic background, not a supplied game ground. The frozen O2 has no edge/region-mask parameter, so requested key-facing-edge inside/outside means cannot be computed under the no-new-code rule. Separate null O2.key_facing_edge envelopes record this. Bible min_delta=0.08 is not applied because its conversion to the frozen oracle's 0..255 luma units is undeclared.
- All measurements without declared thresholds remain descriptive; motif counts remain advisory.

Exact measurement command:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
from pathlib import Path
import numpy as np
from PIL import Image
from gates import common, matte, plate_uniformity, g9_alpha, matte_quality
from oracles import keylight, motif, silhouette64, grain, figure_ground
from oracles.common import report

out = Path('out')
out.mkdir(exist_ok=True)
root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
bible = json.loads((root / 'bible/f04-keepers.json').read_text())
key = bible['LIGHT']['key_azimuth_deg']
anchor_path = root / 'fixtures/x0t/F04_starter_native.png'
anchor = common.rgba(anchor_path)
anchor_alpha = np.array(anchor.getchannel('A'))
anchor_source = grain.band_energy(anchor, anchor_alpha, anchor.size, subject='F04_starter_native/source')
anchor_display = grain.band_energy(anchor, anchor_alpha, anchor.size, display_scale=0.5, subject='F04_starter_native/display_0.5')
source_profile = json.loads(anchor_source['notes'])['metrics']['profile']
display_profile = json.loads(anchor_display['notes'])['metrics']['profile']
rows = []
for candidate in ('G', 'H'):
    subject = 'k1_master_' + candidate
    source_path = root / ('runs/C-1/artifacts/K1-gen-03/' + subject + '.png')
    source = Image.open(source_path)
    rgba, matte_info = matte.extract(source, preserve_particles=False, alpha_floor=40)
    rgba_path = out / (subject + '_rgba.png')
    rgba.save(rgba_path)
    alpha = np.array(rgba.getchannel('A'))
    rows.append(report('input_dimensions', subject, list(source.size), metrics={'mode': source.mode, 'declared_size': [1254,1254], 'matte_output_size': list(rgba.size)}, reason='Actual input is 1024x1536, not declared 1254x1254. Native diagnostic matte retained; no registration or art resizing performed.'))
    rows.append(report('matte.extract', subject, None, metrics=matte_info, reason='Extraction metadata; character mode, alpha_floor=40.'))
    rows.append(plate_uniformity.measure(source, tol=8, min_fraction=None, subject=subject))
    rows.extend(g9_alpha.evaluate(rgba, subject=subject, dark_threshold=None))
    rows.extend(matte_quality.measure(rgba, source, tol=20, halo_width_px=2, subject=subject))

    light = keylight.azimuth(rgba, alpha, key_azimuth_deg=key, tolerance=None, subject=subject)
    light_notes = json.loads(light['notes'])
    light_notes['metrics']['circular_error_deg'] = light['value']
    angle = light_notes['metrics'].get('azimuth_deg')
    light_notes['metrics']['absolute_difference_from_135_deg'] = None if angle is None else abs(angle-key)
    light_notes['metrics']['key_azimuth_deg'] = key
    light_notes['reason'] = 'Tolerance undeclared; value is luminance-weighted circular mean azimuth in degrees, screen x right/y up.'
    light.update(value=angle, passed=None, notes=json.dumps(light_notes, allow_nan=False, sort_keys=True))
    rows.append(light)

    raw = motif.count_family(source, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=0.50, allowed_masks=None, hollow_min=0, max_outside=None, subject=subject)
    raw_notes = json.loads(raw['notes'])
    raw_notes['reason'] = 'ADVISORY raw sheet-wide count, annulus filter disabled with hollow_min=0; no allowed masks.'
    raw.update(id='O3b.raw', passed=None, notes=json.dumps(raw_notes, allow_nan=False, sort_keys=True))
    rows.append(raw)
    annulus = motif.count_family(source, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=0.50, allowed_masks=None, hollow_min=0.5, max_outside=None, subject=subject)
    annulus_notes = json.loads(annulus['notes'])
    annulus_notes['reason'] = 'ADVISORY annulus-filtered sheet-wide count, hollow_min=0.5; no allowed masks.'
    annulus.update(id='O3b.annulus_filtered', passed=None, notes=json.dumps(annulus_notes, allow_nan=False, sort_keys=True))
    rows.append(annulus)

    desc = silhouette64.descriptor(rgba)
    silhouette = Image.fromarray(desc['mask']).convert('L')
    silhouette_path = out / (subject + '_64.png')
    silhouette.save(silhouette_path)
    silhouette_rgba = Image.new('RGBA', silhouette.size, (255,255,255,255))
    silhouette_rgba.putalpha(silhouette)
    silhouette_measure = common.measure(silhouette_rgba)
    native_measure = common.measure(rgba)
    rows.append(report('O5', subject, float(np.mean(desc['mask'])), unit='alpha_area_fraction', metrics={'area_px': desc['area'], 'bbox_height_px': silhouette_measure['height'], 'bbox': silhouette_measure['bbox'], 'centroid': desc['centroid'], 'hu': desc['hu'], 'canvas_size': list(silhouette.size), 'native_alpha_area_fraction': float(np.mean(alpha>=128)), 'native_bbox_height_px': native_measure['height'], 'native_bbox': native_measure['bbox'], 'silhouette_png': str(silhouette_path)}, reason='Descriptor summary only. Frozen oracle resizes alpha to fixed 64x64 with Lanczos, then thresholds at 128; native portrait aspect is not preserved by this diagnostic.'))
    for scale, profile, anchor_result, label in ((None, source_profile, anchor_source, 'source'), (0.5, display_profile, anchor_display, 'display_0.5')):
        spectral = grain.band_energy(rgba, alpha, source.size, anchor_profile=profile, threshold=None, display_scale=scale, subject=subject)
        spectral_notes = json.loads(spectral['notes'])
        spectral_notes['metrics'].update(display_scale=scale, anchor_path=str(anchor_path), anchor_source_size=list(anchor.size), anchor_profile=json.loads(anchor_result['notes'])['metrics']['profile'], anchor_alpha_support='Full canvas: RGB anchor has no alpha or supplied foreground mask.')
        spectral_notes['reason'] = 'Descriptive L2 distance only; no threshold. Anchor background is included; candidate and anchor source dimensions differ and this comparison is not calibrated.'
        spectral.update(id='O8.'+label, passed=None, notes=json.dumps(spectral_notes, allow_nan=False, sort_keys=True))
        rows.append(spectral)

    separation = figure_ground.separation(rgba, [20,25,34], sign=1, min_delta=None, subject=subject)
    separation_notes = json.loads(separation['notes'])
    separation_notes['metrics'].update(background_rgb=[20,25,34], sampling='Whole alpha>=128 figure versus alpha<128 outside.')
    separation_notes['reason'] = 'Whole-figure diagnostic only on common.pixels standard cool background, chosen explicitly; actual game ground unspecified. Frozen O2 has no key-facing-edge mask parameter. No threshold applied; bible min_delta=0.08 has no declared conversion to this oracle 0..255 luma unit.'
    separation.update(passed=None, notes=json.dumps(separation_notes, allow_nan=False, sort_keys=True))
    rows.append(separation)
    rows.append(report('O2.key_facing_edge', subject, None, unit='luma', reason='Cannot compute requested edge-local inside/outside means using frozen separation(): no edge or region mask parameter; no key-facing-edge annotation or actual ground supplied. Whole-figure O2 reported separately. No new metric code permitted.'))
    print(json.dumps({'subject': subject, 'input_size': list(source.size), 'O7_azimuth_deg': angle, 'O3b_raw': raw['value'], 'O3b_annulus_filtered': annulus['value'], 'O5_area_fraction': float(np.mean(desc['mask'])), 'O5_bbox_height_px': silhouette_measure['height'], 'O2_whole_figure_delta': separation['value']}))
(out / 'checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
print('Wrote', len(rows), 'result envelopes.')
PY

Exact artifact verification commands:
file out/k1_master_G_rgba.png out/k1_master_H_rgba.png out/k1_master_G_64.png out/k1_master_H_64.png
shasum -a 256 out/checks.json out/checks_readme.txt out/k1_master_G_rgba.png out/k1_master_H_rgba.png out/k1_master_G_64.png out/k1_master_H_64.png
