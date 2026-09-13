K1p-chk-01 deterministic checks

All measurement algorithms are unchanged frozen module calls. Inline Python is orchestration, result-envelope adaptation and output serialization; no module or program files were created or modified. PYTHONDONTWRITEBYTECODE prevents writes to the frozen tool tree.

Scope and limitations:
- RGBA masters preserve the supplied 1024x1536 native canvas. Registration to 512x512 and pivot placement are not part of this CHECK task.
- Character matting: preserve_particles=False, alpha_floor=40. Plate support uses extracted alpha>=128 and is model-coupled.
- Each _64.png is the exact binary mask returned by the frozen O5 descriptor. The frozen instrument always uses a 64x64 canvas, so nonsquare source aspect is not retained. These are analytical masks, not registered artwork. O5 reports both native and 64px bbox heights.
- O7 value is the circular mean angle in degrees (adapted from the frozen module's azimuth_deg metric); both literal |value-135| and circular error are reported. No tolerance is inferred.
- O3b uses the entire original RGB plate, allowed_masks=None. Raw count is the number of unchanged post-NMS peaks before annulus filtering; filtered count is the frozen return value at hollow_min=0.5. Both counts are advisory and carry null verdicts.
- O8 computes both anchors at source scale and display_scale=0.5. The H1 anchor is character-matted with alpha_floor=40. A preliminary extraction attempt on the v1.0 anchor raised: No native alpha or uniform green plate: border green fraction 0.0000. That opaque 265x675 gray-background image has no supplied subject mask, so its native full-canvas alpha is used. All four requested distances are computed, but continuity distances include background energy and source-size differences; a subject-only continuity distance cannot be computed with supplied support and frozen extraction. This is not a replacement registration anchor or a calibrated acceptance test.
- O2 uses RGB [20,25,34], the background in frozen gates.common.pixels, as an explicit reporting assumption because no ground color is supplied. The whole-figure metric does not isolate the key-facing edge. No threshold is applied: the bible's 0.08 relation does not declare its conversion to the oracle's 0..255 luma units. Separation against an actual scene ground cannot be computed from the supplied inputs.
- G9 clipping and green-spill booleans are emitted unchanged by the frozen gate. G9 dark-fringe absence remains unevaluable numerically without a declared threshold or visual judgment. Other undeclared thresholds remain null. No candidate-level verdict is issued.
- Files below are the eight requested deliverables. Existing hidden .wrapper-* files are live conductor-owned audit streams, not burst-authored deliverables, and are not included in receipt hashes.

Exact production command (run from the workdir):

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
from pathlib import Path
import numpy as np
from PIL import Image
from gates import plate_uniformity, matte, g9_alpha, matte_quality
from gates.common import rgba, measure
from oracles import keylight, motif, silhouette64, grain, figure_ground
from oracles.common import report

root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
out = Path('out')
bible = json.loads((root / 'bible/f04-keepers.json').read_text())
key = bible['LIGHT']['key_azimuth_deg']
anchors = {}
anchor_paths = {
    'H1_ruled_register': root / 'runs/C-1/artifacts/K4-gen-H1/k4_H1_1.png',
    'v1_painted_continuity_only': root / 'fixtures/x0t/F04_starter_native.png',
}
for name, path in anchor_paths.items():
    anchor = rgba(path)
    support_note = 'Native opaque full-canvas support: no alpha or green plate; gray background contributes; continuity only.'
    if name == 'H1_ruled_register':
        anchor, anchor_meta = matte.extract(anchor, preserve_particles=False, alpha_floor=40)
        support_note = 'Frozen character matte, alpha_floor=40: ' + json.dumps(anchor_meta, sort_keys=True)
    for scale in (None, 0.5):
        profile = grain.band_energy(anchor, np.asarray(anchor.getchannel('A')), anchor.size, display_scale=scale, subject=name)
        anchors[(name, scale)] = (json.loads(profile['notes'])['metrics']['profile'], support_note)

rows = []
for candidate in ('A', 'B', 'C'):
    subject = 'k1p_master_' + candidate
    path = root / 'runs/C-1/artifacts/K1p-gen-01' / (subject + '.png')
    source = rgba(path)
    image, extraction = matte.extract(source, preserve_particles=False, alpha_floor=40)
    matte_path = out / (subject + '_rgba.png')
    image.save(matte_path)
    alpha = np.asarray(image.getchannel('A'))
    plate = plate_uniformity.measure(source, subject_alpha=alpha, tol=8, min_fraction=None, subject=subject)
    plate['evidence'] = [str(path), str(matte_path)]
    notes = json.loads(plate['notes'])
    notes['metrics']['matte_extraction'] = extraction
    plate['notes'] = json.dumps(notes, sort_keys=True, allow_nan=False)
    rows.append(plate)
    for row in g9_alpha.evaluate(image, subject=subject, dark_threshold=None):
        row['evidence'] = [str(matte_path)]
        rows.append(row)
    for row in matte_quality.measure(image, source, tol=20, halo_width_px=2, subject=subject):
        row['evidence'] = [str(path), str(matte_path)]
        rows.append(row)

    light = keylight.azimuth(image, alpha, key_azimuth_deg=key, tolerance=None, min_resultant=0, erosion_px=1, subject=subject)
    light_metrics = json.loads(light['notes'])['metrics']
    light_metrics['circular_absolute_error_deg'] = light['value']
    light_metrics['absolute_value_minus_135_deg'] = abs(light_metrics['azimuth_deg'] - key)
    light_metrics['key_azimuth_deg'] = key
    light_metrics['erosion_px'] = 1
    light = report('O7', subject, light_metrics['azimuth_deg'], unit='degrees', metrics=light_metrics, reason='Circular mean azimuth; tolerance undeclared; gradient proxy, not visual lighting judgment.')
    light['evidence'] = [str(matte_path)]
    rows.append(light)

    rings = motif.count_family(source, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=0.50, allowed_masks=None, hollow_min=0.5, max_outside=None, subject=subject)
    ring_metrics = json.loads(rings['notes'])['metrics']
    raw_count = len(ring_metrics['peaks'])
    ring_metrics['raw_count_before_annulus_filter'] = raw_count
    ring_metrics['annulus_filtered_count'] = rings['value']
    ring_metrics['allowed_masks'] = None
    ring_metrics['input_support'] = 'Entire original RGB plate; no subject crop or mask.'
    for mode, value in (('raw', raw_count), ('annulus_filtered', rings['value'])):
        row = report('O3b.' + mode, subject, value, unit='instances', metrics=ring_metrics, reason='ADVISORY; starter motif budget is zero; no acceptance verdict.')
        row['evidence'] = [str(path)]
        rows.append(row)

    desc = silhouette64.descriptor(image.getchannel('A'))
    mask_image = Image.fromarray(desc['mask']).convert('L')
    mask_path = out / (subject + '_64.png')
    mask_image.save(mask_path)
    box64 = mask_image.getbbox()
    native = measure(image)
    row = report('O5', subject, desc['area'] / desc['mask'].size, unit='alpha_area_fraction_64', metrics={
        'alpha_area_fraction_64': desc['area'] / desc['mask'].size,
        'alpha_area_px_64': desc['area'],
        'bbox_height_px_64': box64[3] - box64[1],
        'bbox_xyxy_64': list(box64),
        'canvas_size_64': list(mask_image.size),
        'native_bbox_height_px': native['height'],
        'native_bbox_xyxy': native['bbox'],
        'native_canvas_size': list(image.size),
        'centroid_64': desc['centroid'],
        'hu': desc['hu'],
        'alpha_threshold': 128,
    }, reason='Report only. Frozen descriptor always resizes to 64x64, including nonsquare inputs; PNG is its unchanged binary mask, not a registered sprite.')
    row['evidence'] = [str(matte_path), str(mask_path)]
    rows.append(row)

    for name, anchor_path in anchor_paths.items():
        for scale in (None, 0.5):
            anchor_profile, support_note = anchors[(name, scale)]
            row = grain.band_energy(image, alpha, image.size, anchor_profile=anchor_profile, threshold=None, display_scale=scale, subject=subject)
            row['id'] = 'O8.' + name + ('.source' if scale is None else '.display_0.5')
            notes = json.loads(row['notes'])
            notes['metrics'].update({
                'anchor_path': str(anchor_path),
                'anchor_profile': anchor_profile,
                'anchor_support': support_note,
                'display_scale': 1.0 if scale is None else scale,
                'candidate_support': 'Frozen character matte, alpha_floor=40, alpha>0',
            })
            notes['reason'] = 'Descriptive distance; threshold undeclared; anchors have different source sizes. Continuity anchor includes its opaque background.'
            row['notes'] = json.dumps(notes, sort_keys=True, allow_nan=False)
            row['evidence'] = [str(matte_path), str(anchor_path)]
            rows.append(row)

    row = figure_ground.separation(image, (20, 25, 34), sign=1, min_delta=None, subject=subject)
    notes = json.loads(row['notes'])
    notes['metrics']['background_rgb'] = [20, 25, 34]
    notes['metrics']['background_basis'] = 'Explicit reporting assumption: gates.common.pixels frozen compositing background; task supplies no ground.'
    notes['metrics']['bible_relation_min_delta_unapplied'] = bible['PALETTE']['relation_rules'][0]['min_delta']
    notes['reason'] = 'Report only, whole-figure mean. No supplied ground or key-facing-edge mask; bible 0.08 lacks declared conversion to oracle 0..255 luma.'
    row['notes'] = json.dumps(notes, sort_keys=True, allow_nan=False)
    row['evidence'] = [str(matte_path)]
    rows.append(row)
    print(subject, 'completed', flush=True)

(out / 'checks.json').write_text(json.dumps(rows, indent=2, sort_keys=True, allow_nan=False) + '\n')
print('Wrote', len(rows), 'SPEC section 1 result envelopes.')

PY

Exact verification and hash command:

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json
from pathlib import Path
from PIL import Image
rows = json.loads(Path('out/checks.json').read_text())
print('Envelope count:', len(rows))
print('Envelope fields:', sorted(rows[0]))
for candidate in ('A', 'B', 'C'):
    subject = 'k1p_master_' + candidate
    for suffix in ('_rgba.png', '_64.png'):
        with Image.open(Path('out') / (subject + suffix)) as im:
            im.verify()
        with Image.open(Path('out') / (subject + suffix)) as im:
            print(subject + suffix, im.mode, im.size)
            if suffix == '_64.png':
                print('Binary pixel values:', im.getcolors())
    print(subject, [(r['id'], r['value']) for r in rows if r['subject'] == subject])
PY
shasum -a 256 out/checks.json out/checks_readme.txt out/k1p_master_A_rgba.png out/k1p_master_B_rgba.png out/k1p_master_C_rgba.png out/k1p_master_A_64.png out/k1p_master_B_64.png out/k1p_master_C_64.png

