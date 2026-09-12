K1-chk-01 deterministic check record

Only frozen measurement functions were used; Python below is invocation, returned-data
serialization, and saving oracle-produced images. No tool modules or inputs were edited.
PYTHONDONTWRITEBYTECODE=1 prevents bytecode writes beside the frozen modules.
All deliverables are in out/. Hidden .wrapper-* files are wrapper-owned live audit
logs, not deliverables; they are not included in the receipt artifact hash list.

Scope and limitations:
- All three actual inputs are 1024x1536, contradicting the declared 1254x1254.
  The RGBA outputs retain actual native dimensions. They are diagnostic mattes,
  not registered 512x512 sprite frames. No scaling/translation registration was requested.
- Character matte: preserve_particles=False, alpha_floor=40.
- Plate support: supplied extracted alpha >=128; tol=8, min_fraction undeclared.
- G9 uses frozen numeric checks as returned. No overall candidate verdict is assigned.
  Dark fringe remains a measurement with no calibrated numeric threshold.
- Matte particle-loss is a model-coupled partial-alpha-mass proxy; it includes
  plate residuals and AA edges, not identified particles.
- O7 value is the oracle's luminance-weighted circular mean azimuth. Both the
  absolute difference from 135 and shortest circular difference appear in notes.metrics.
  Tolerance is undeclared and passed is null.
- O3b runs on original green-plate inputs, at native scale, with no allowed masks.
  Raw count is the length of the frozen detector's retained peaks after geometric
  checks and NMS, before annulus filtering. Filtered count is its returned count
  at hollow_min=0.5. Both advisory, passed null; no placement judgment.
- O5 PNGs are exactly descriptor.mask: LANCZOS alpha reduction to 64x64, then >=128,
  exported as black/white L-mode PNGs. The frozen oracle forces square dimensions
  and therefore alters aspect ratio for the actual portrait inputs; no custom
  aspect-preserving silhouette implementation was substituted. O5 bbox height
  refers to the 64px mask; native alpha bbox height is separately reported.
- O8 compares at source scale and display_scale=0.5, using each input's actual
  source width/height. The anchor is 265x675, all stored alpha=255; its full crop
  is included because no foreground mask is supplied. Different source sizes
  and opaque anchor support limit interpretation. Profiles and anchor results
  are retained. No calibrated distance threshold was supplied.
- O2.key_facing_edge cannot be computed by the supplied frozen function:
  it accepts no edge-region mask, and no scene background RGB is supplied.
  The null envelope explicitly records this. O2.global_green_plate_proxy calls
  the frozen whole-image function with the only given background, [0,255,0].
  It is not a key-edge or scene-ground measurement and is not scored.
  The bible min_delta=0.08 has no declared conversion to O2's 0..255 luma units;
  it is recorded but not used as a threshold.
- All reports use the SPEC section 1 envelope. Extra instrument details are JSON
  within notes; any absent requested quantity has an explicit reason.

Exact measurement and output command (run from
/Users/admin/astra-burst/runs/C-1/K1-chk-01):

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
from pathlib import Path
from PIL import Image
from gates.common import rgba, measure, result
from gates import plate_uniformity, matte, g9_alpha, matte_quality
from oracles import keylight, motif, silhouette64, grain, figure_ground
from oracles.common import image_array, report

root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
inputs = root / 'runs/C-1/artifacts/K1-gen-01'
anchor_path = root / 'fixtures/x0t/F04_starter_native.png'
bible = json.loads((root / 'bible/f04-keepers.json').read_text())
key = bible['LIGHT']['key_azimuth_deg']
anchor = rgba(anchor_path)
anchor_alpha = image_array(anchor)[..., 3]
anchor_reports = {}
for scale in (None, 0.5):
    anchor_reports[scale] = grain.band_energy(anchor, anchor_alpha, anchor.size, display_scale=scale, subject='F04_starter_native')
rows = []
for name in ('A', 'B', 'C'):
    subject = 'k1_master_' + name
    source_path = inputs / (subject + '.png')
    source = rgba(source_path)
    matted, matte_details = matte.extract(source, preserve_particles=False, alpha_floor=40)
    matte_path = Path('out') / (subject + '_rgba.png')
    matted.save(matte_path)
    alpha = image_array(matted)[..., 3]
    rows.append(report('input_dimensions', subject, None, metrics={'actual_px': list(source.size), 'declared_px': [1254, 1254], 'matte_output_px': list(matted.size), 'matte_extraction': matte_details}, reason='Inputs are 1024x1536, not declared 1254x1254. Native dimensions preserved; no registration performed.'))
    rows.append(plate_uniformity.measure(source, subject_alpha=alpha, tol=8, min_fraction=None, subject=subject))
    rows.extend(g9_alpha.evaluate(matted, subject=subject, dark_threshold=None))
    rows.extend(matte_quality.measure(matted, source, tol=20, halo_width_px=2, subject=subject))
    light = keylight.azimuth(matted, alpha, key_azimuth_deg=key, tolerance=None, subject=subject)
    light_notes = json.loads(light['notes'])
    light_metrics = light_notes['metrics']
    light_metrics['circular_absolute_error_deg'] = light['value']
    angle = light_metrics.get('azimuth_deg')
    light_metrics['absolute_error_deg'] = None if angle is None else abs(angle - key)
    light_metrics['key_azimuth_deg'] = key
    rows.append(report('O7', subject, angle, unit='degrees', metrics=light_metrics, reason=light_notes['reason'] or 'Tolerance undeclared; value is luminance-weighted circular mean azimuth, x-right/y-up.'))
    rings = motif.count_family(source, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=0.50, allowed_masks=None, hollow_min=0.5, max_outside=None, subject=subject)
    ring_metrics = json.loads(rings['notes'])['metrics']
    rows.append(report('O3b.raw', subject, len(ring_metrics['peaks']), unit='instances', metrics={'allowed_masks': None, 'scope': 'raw source sheet-wide, after geometric checks and NMS, before annulus filtering', 'min_radius_px': 8, 'max_radius_px': 30, 'vote_thresh': 0.50, 'raw_count': len(ring_metrics['peaks'])}, reason='Advisory; no allowed placement masks or threshold.'))
    rows.append(report('O3b.annulus_filtered', subject, rings['value'], unit='instances', metrics=ring_metrics, reason='Advisory; allowed_masks=None, sheet-wide count, hollow_min=0.5.'))
    desc = silhouette64.descriptor(matted)
    silhouette_path = Path('out') / (subject + '_64.png')
    silhouette = Image.fromarray(desc['mask']).convert('L')
    silhouette.save(silhouette_path)
    bbox = silhouette.getbbox()
    rows.append(report('O5', subject, desc['area'] / 4096, unit='alpha_area_fraction', metrics={'alpha_area_fraction': desc['area'] / 4096, 'area_px': desc['area'], 'bbox_64_xyxy': list(bbox), 'bbox_height_px': bbox[3] - bbox[1], 'source_bbox_height_px': measure(matted)['height'], 'canvas_px': [64, 64], 'source_canvas_px': list(source.size), 'centroid': desc['centroid'], 'hu': desc['hu'], 'silhouette_path': str(silhouette_path), 'reduction': 'Exact frozen descriptor mask: alpha resized to 64x64 with LANCZOS then >=128; non-square source aspect ratio is changed by the oracle.'}, reason='Descriptor summary only; no approved comparison master or threshold.'))
    for scale in (None, 0.5):
        anchor_report = anchor_reports[scale]
        profile = json.loads(anchor_report['notes'])['metrics'].get('profile')
        spectral = grain.band_energy(matted, alpha, source.size, anchor_profile=profile, threshold=None, display_scale=scale, subject=subject)
        spectral_metrics = json.loads(spectral['notes'])['metrics']
        spectral_metrics.update({'display_scale': 1.0 if scale is None else scale, 'anchor_path': str(anchor_path), 'anchor_canvas_px': list(anchor.size), 'anchor_alpha': 'Stored opaque alpha, all 255; no foreground annotation supplied.', 'anchor_result': anchor_report})
        rows.append(report('O8.source' if scale is None else 'O8.display_0.5', subject, spectral['value'], unit='profile_l2', metrics=spectral_metrics, reason='Threshold undeclared; candidate and anchor have different source dimensions; descriptive distance only.'))
    global_fg = figure_ground.separation(matted, [0, 255, 0], sign=1, min_delta=None, subject=subject)
    rows.append(report('O2.global_green_plate_proxy', subject, global_fg['value'], op='>=', unit='luma', metrics={'measurement': json.loads(global_fg['notes'])['metrics'], 'background_rgb': [0, 255, 0], 'scope': 'Entire alpha support versus remaining canvas, not key-facing edge.'}, reason='Only the input green plate is supplied; no scene ground RGB or key-facing edge mask. Whole-figure proxy only.'))
    rows.append(report('O2.key_facing_edge', subject, None, op='>=', unit='luma', metrics={'key_azimuth_deg': key, 'bible_min_delta': bible['PALETTE']['relation_rules'][0]['min_delta']}, reason='Cannot compute requested key-facing-edge separation: frozen O2 accepts no edge mask, and no scene background or reviewed edge region is supplied. No custom measurement code introduced.'))
Path('out/checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
print('Wrote', len(rows), 'result envelopes and six PNGs.')
for row in rows:
    print(row['subject'], row['id'], row['value'])
PY

Exact output verification and receipt-hash commands:

python3 -m json.tool out/checks.json > /dev/null
sips -g pixelWidth -g pixelHeight -g hasAlpha out/k1_master_A_rgba.png out/k1_master_B_rgba.png out/k1_master_C_rgba.png out/k1_master_A_64.png out/k1_master_B_64.png out/k1_master_C_64.png
shasum -a 256 out/checks.json out/checks_readme.txt out/k1_master_A_rgba.png out/k1_master_B_rgba.png out/k1_master_C_rgba.png out/k1_master_A_64.png out/k1_master_B_64.png out/k1_master_C_64.png

