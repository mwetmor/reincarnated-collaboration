K2-chk-02 — exact measurement command (run from the burst workdir)

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys
import json
from pathlib import Path
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates import common, matte, g1_height, g2_pivot, g3_light, silhouette64, plate_uniformity, g9_alpha, matte_quality
from oracles import keylight, motif
from oracles.common import image_array

out = Path('out')
out.mkdir(exist_ok=True)
base = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts')
inputs = {
    'S': base / 'K1-gen-04/k1_master_L.png',
    'SW': base / 'K2-gen-SW/k2_SW.png',
    'W': base / 'K2-gen-W/k2_W.png',
    'NW': base / 'K2-gen-NW-r1/k2_NW.png',
    'N': base / 'K2-gen-N/k2_N.png',
    'NE': base / 'K2-gen-NE/k2_NE.png',
    'E': base / 'K2-gen-E/k2_E.png',
    'SE': base / 'K2-gen-SE-r1/k2_SE.png',
}
rows = []
master, master_details = matte.extract(common.rgba(inputs['S']), alpha_floor=40)
master_measure = common.measure(master)
for direction, source_path in inputs.items():
    source = common.rgba(source_path)
    im, details = matte.extract(source, alpha_floor=40)
    rgba_path = out / ('k2_' + direction + '_rgba.png')
    silhouette_path = out / ('k2_' + direction + '_64.png')
    im.save(rgba_path)
    descriptor = silhouette64.descriptor(im)
    common.Image.fromarray(descriptor['mask']).convert('L').save(silhouette_path)
    measurement = common.measure(im)
    rgba_array = image_array(im)
    raw_g1 = g1_height.evaluate(im, master, direction, tolerance=.03)
    rows.append(common.result('g1_height', direction,
        value=measurement['height']/master_measure['height'], threshold=[.97,1.03],
        op='within_inclusive', unit='height_ratio', passed=raw_g1['passed'],
        notes=json.dumps({'frozen_tool_result': raw_g1, 'master': str(inputs['S'])})))
    rows.append(g2_pivot.root_anchor(anchor=None, subject=direction, pivot=(256,400), tolerance=4))
    rows.append(g3_light.evaluate(im, direction))
    rows.append(silhouette64.evaluate(im, master, direction, threshold=None))
    rows.append(plate_uniformity.measure(source, subject_alpha=rgba_array[...,3],
        tol=8, min_fraction=None, subject=direction))
    rows.extend(g9_alpha.evaluate(im, direction, dark_threshold=None))
    rows.extend(matte_quality.measure(im, source, tol=20, halo_width_px=2,
        subject=direction, max_spill_fraction=None, max_edge_halo=None, max_particle_loss=None))
    rows.append(keylight.azimuth(im, rgba_array[...,3], mask=None,
        key_azimuth_deg=135, tolerance=None, min_resultant=0, erosion_px=1,
        display_scale=None, subject=direction))
    raw = motif.count_family(im, family='ring', min_radius_px=8, max_radius_px=30,
        vote_thresh=.50, allowed_masks=None, display_scale=None,
        hollow_min=0, max_outside=None, subject=direction)
    raw['id'] = 'O3b_raw'
    rows.append(raw)
    annulus = motif.count_family(im, family='ring', min_radius_px=8, max_radius_px=30,
        vote_thresh=.50, allowed_masks=None, display_scale=None,
        hollow_min=.5, max_outside=None, subject=direction)
    annulus['id'] = 'O3b_annulus'
    rows.append(annulus)
    rows.append(common.result('bleed_index', direction, notes=
        'UNEVALUABLE: no bleed-index function or definition in the named frozen modules; no reviewed allowed motif masks supplied. O3b raw and annulus counts are advisory, not semantic bleed counts. Green spill and edge halo are separate matte_quality measurements.'))
    box = measurement['bbox']
    rows.append(common.result('alpha_bbox', direction, value=box, unit='px_xyxy_exclusive',
        notes='Frozen common.measure; alpha >=128.'))
    rows.append(common.result('alpha_bbox_canvas_fraction', direction,
        value=(box[2]-box[0])*(box[3]-box[1])/(im.width*im.height), unit='fraction',
        notes='Alpha >=128 bounding-rectangle area divided by full canvas area; not opaque-pixel occupancy.'))
    rows.append(common.result('alpha_support_canvas_fraction', direction,
        value=1-measurement['transparent_fraction'], unit='fraction',
        notes='Alpha >0 support fraction, derived from frozen common.measure transparent_fraction.'))
    rows.append(common.result('canvas_size', direction, value=list(im.size), unit='px',
        notes='Input canvas retained; no registration, translation or scaling performed on delivered RGBA.'))
    rows.append(common.result('matte_extract', direction, value=None,
        notes=json.dumps(details)))
    for row in rows:
        if row['subject'] == direction:
            row['evidence'] = [str(source_path), str(rgba_path), str(silhouette_path)]
    print(json.dumps({'direction':direction, 'canvas':list(im.size),
        'height_ratio':measurement['height']/master_measure['height'],
        'bbox':box, 'g3':rows[-19]['id'] if False else g3_light.evaluate(im,direction)['value'],
        'O3b_raw':raw['value'], 'O3b_annulus':annulus['value']}), flush=True)
(out / 'checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
PY

Notes:
- Measurements use frozen modules; output serialization and requested ratio/fraction formatting only.
- No source edits, registration transforms, image generation, or module changes.
- G1 ratio envelope retains the frozen deviation envelope and its literal boolean in notes.
- G2-root requires independent reviewed anchors; none supplied. No sole midpoint substituted.
- O7 value is circular absolute deviation from 135 degrees; azimuth is in notes.metrics.azimuth_deg. No tolerance supplied.
- O3b_raw uses hollow_min=0; O3b_annulus uses hollow_min=0.5; no allowed masks; no semantic bleed classification.
- No frozen bleed-index function/definition supplied: explicit null envelope, with separate motif and green-spill measurements.
- Plate tolerance is 8 per channel with matted alpha>=128 support; no acceptance fraction supplied.
- G9 dark-fringe judgement remains null because no calibrated numerical threshold supplied.
- Silhouette PNGs use the frozen descriptor's 64x64 binary mask; no generated-art upscaling.

Registration limitation discovered from the measured inputs:
All eight sources and matte exports are 1024x1536, not registered 512x512 frames. Frozen register.registration requires a square source; reviewed source anchors/body heights are absent. No attempt to invent registration annotations or bypass the frozen implementation was made. The 64x64 binary PNGs are exact descriptor masks; the frozen descriptor changes aspect ratio for these rectangular sources. These are limitations, not shipping acceptance.

Exact command adding explicit limitation envelopes:

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys
import json
from pathlib import Path
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates.common import result, DIRS
path = Path('out/checks.json')
rows = json.loads(path.read_text())
for direction in DIRS:
    rows.append(result('registration_512', direction, notes=
        'UNEVALUABLE: source is 1024x1536; frozen register.registration requires square input. No reviewed source anchors/body heights supplied. Native-size matte retained. The prescribed 512x512 canvas, (256,400) root and approximately 240px S height are not delivered. No source crop, padding, inferred anchor, or per-frame scale introduced.'))
    rows.append(result('silhouette64_aspect_caveat', direction, notes=
        'Frozen silhouette64.descriptor resizes the entire 1024x1536 source canvas to 64x64 before thresholding alpha>=128. Delivered binary PNG matches that instrument exactly, but this changes source aspect ratio; distances are native-input proxy measurements, not registered-frame validation.'))
path.write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
PY
