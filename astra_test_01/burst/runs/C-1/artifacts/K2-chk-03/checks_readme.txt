K2-chk-03 deterministic checks

Scope and limitations
- All eight named source PNGs are 1024x1536. Measurements use their native, in-memory mattes (alpha_floor=40). No registered 512x512 RGBA frames are delivered: the eight requested out/k2_<DIR>_rgba.png files are omitted. No reviewed source anchors/body-height annotations or locked common scale were supplied; gates/register.py registration() requires square sources. A CHECK burst cannot invent a registration method or annotations.
- G2-root is null: independent reviewed root anchors were not supplied. The nominal atlas pivot (256,400) is not evidence of the actual root position.
- A numeric bleed index is unavailable: no frozen definition or reviewed allowed regions supplied. O3b raw/annulus counts are advisory, full-canvas counts with no masks; they are not verified bleed. Raw uses hollow_min=0; annulus uses 0.5. Both use native radii 8..30 and vote_thresh=0.50.
- G1 value is the native alpha>=128 bbox-height ratio. Its boolean is retained exactly from g1_height.evaluate(tolerance=.03). The original absolute-deviation envelope is preserved in notes. The ratio envelope expresses the inclusive interval [0.97,1.03].
- G3 is the unchanged frozen result. O7 value is wrapped absolute angular deviation from 135 degrees; notes.metrics.azimuth_deg gives the measured azimuth. O7 has no calibrated tolerance, so its boolean is null.
- plate_uniformity uses original RGB and supplied native matte alpha support, tol=8; min_fraction=None. G9 returns border clipping, green contamination, edge mean and an uncalibrated dark-fringe report.
- silhouette64 is the exact frozen descriptor: it resizes native alpha from 1024x1536 to 64x64, binarizes at 128, and compares centroid/area-aligned IoU. These are analytical masks, not registered artwork; the aspect-ratio change in this instrument is disclosed. Its threshold is None and its boolean is null.
- Alpha bbox uses exclusive XYXY coordinates. Bbox canvas fraction is rectangle area / native canvas area. Alpha support canvas fraction is opaque support area / native canvas area.
- No source files or frozen modules were modified. Bytecode writing was disabled. No custom measurement implementation or code file was created.

One diagnosed retry
The initial invocation stopped on S when its 512x512 input validation discovered 1024x1536. No artifacts were written by that invocation. The retry omits unavailable registered RGBA output and performs the measurements at native resolution without changing any gate thresholds.

Exact initial measurement command

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys
import json
from pathlib import Path
from PIL import Image
import numpy as np
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates import matte, g1_height, g2_pivot, g3_light, silhouette64, plate_uniformity, g9_alpha
from gates.common import measure, result
from oracles import keylight, motif

inputs = {
    'S': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K1-gen-04/k1_master_L.png',
    'SW': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-SW-c1/k2_SW.png',
    'W': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-W-c1/k2_W.png',
    'NW': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-NW-c1/k2_NW.png',
    'N': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-N/k2_N.png',
    'NE': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-NE-c1/k2_NE.png',
    'E': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-E-c1/k2_E.png',
    'SE': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-SE-c1/k2_SE.png',
}
rows = []
master, master_matte = matte.extract(Image.open(inputs['S']), alpha_floor=40)
master_measure = measure(master)
for direction, path in inputs.items():
    source = Image.open(path)
    image, extraction = matte.extract(source, alpha_floor=40)
    if image.size != (512, 512):
        raise ValueError('Input is not the registered 512x512 canvas: ' + direction)
    rgba_path = 'out/k2_' + direction + '_rgba.png'
    silhouette_path = 'out/k2_' + direction + '_64.png'
    image.save(rgba_path)
    descriptor = silhouette64.descriptor(image)
    Image.fromarray(descriptor['mask'].astype('uint8') * 255, mode='L').save(silhouette_path)
    m = measure(image)
    alpha = np.asarray(image.getchannel('A'))
    subject = 'K2/' + direction
    rows.append(result('matte', subject, notes=json.dumps({'input': path, 'canvas': list(image.size), 'extraction': extraction}), evidence=[rgba_path]))
    g1 = g1_height.evaluate(image, master, subject=subject, tolerance=.03)
    g1['notes'] = json.dumps({'literal_tool_result': dict(g1), 'height_px': m['height'], 'master_height_px': master_measure['height'], 'ratio_interval_inclusive': [.97, 1.03]})
    g1['value'] = m['height'] / master_measure['height']
    g1['threshold'] = [.97, 1.03]
    g1['op'] = 'within_inclusive'
    g1['unit'] = 'ratio'
    rows.append(g1)
    rows.append(g2_pivot.root_anchor(anchor=None, subject=subject, pivot=(256, 400), tolerance=4))
    rows.append(g3_light.evaluate(image, subject=subject))
    shape = silhouette64.evaluate(image, master, subject=subject, threshold=None)
    shape['evidence'] = [silhouette_path, 'out/k2_S_64.png']
    rows.append(shape)
    rows.append(plate_uniformity.measure(source, subject_alpha=alpha, tol=8, min_fraction=None, subject=subject))
    rows.extend(g9_alpha.evaluate(image, subject=subject, dark_threshold=None))
    rows.append(keylight.azimuth(image, alpha, mask=None, key_azimuth_deg=135, tolerance=None, min_resultant=0, erosion_px=1, display_scale=None, subject=subject))
    raw = motif.count_family(image, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=.50, allowed_masks=None, display_scale=None, hollow_min=0, max_outside=None, subject=subject)
    raw['id'] = 'O3b_raw'
    rows.append(raw)
    annulus = motif.count_family(image, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=.50, allowed_masks=None, display_scale=None, hollow_min=.5, max_outside=None, subject=subject)
    annulus['id'] = 'O3b_annulus'
    rows.append(annulus)
    rows.append(result('alpha_bbox_px', subject, value=m['bbox'], unit='px_xyxy_exclusive', notes='Alpha >=128; measurement only', evidence=[rgba_path]))
    rows.append(result('alpha_bbox_canvas_fraction', subject, value=((m['bbox'][2]-m['bbox'][0]) * m['height']) / (image.width * image.height), unit='fraction', notes='Bounding rectangle area / canvas area; alpha >=128; measurement only'))
    rows.append(result('alpha_support_canvas_fraction', subject, value=float(np.mean(alpha >= 128)), unit='fraction', notes='Opaque alpha support area / canvas area; measurement only'))
    rows.append(result('bleed_index', subject, notes='UNEVALUABLE: no frozen bleed-index formula or reviewed allowed motif regions supplied. O3b_raw and O3b_annulus report unmasked full-canvas counts, not verified ornament bleed. G9 separately reports partial-alpha green contamination.'))
    print(json.dumps({'direction': direction, 'canvas': image.size, 'bbox': m['bbox'], 'height_ratio': g1['value'], 'g3_value_px': rows[-15]['value'] if False else g3_light.evaluate(image, subject=subject)['value'], 'silhouette_distance': shape['value'], 'raw_ring_count': raw['value'], 'annulus_ring_count': annulus['value']}, allow_nan=False), flush=True)
Path('out/checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
PY

Exact retry command (produced checks.json and all eight analytical masks)

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys
import json
from pathlib import Path
from PIL import Image
import numpy as np
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates import matte, g1_height, g2_pivot, g3_light, silhouette64, plate_uniformity, g9_alpha
from gates.common import measure, result
from oracles import keylight, motif

inputs = {
    'S': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K1-gen-04/k1_master_L.png',
    'SW': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-SW-c1/k2_SW.png',
    'W': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-W-c1/k2_W.png',
    'NW': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-NW-c1/k2_NW.png',
    'N': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-N/k2_N.png',
    'NE': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-NE-c1/k2_NE.png',
    'E': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-E-c1/k2_E.png',
    'SE': '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K2-gen-SE-c1/k2_SE.png',
}
rows = []
master, master_matte = matte.extract(Image.open(inputs['S']), alpha_floor=40)
master_measure = measure(master)
for direction, path in inputs.items():
    source = Image.open(path)
    image, extraction = matte.extract(source, alpha_floor=40)
    rgba_path = 'out/k2_' + direction + '_rgba.png'
    silhouette_path = 'out/k2_' + direction + '_64.png'
    descriptor = silhouette64.descriptor(image)
    Image.fromarray(descriptor['mask'].astype('uint8') * 255, mode='L').save(silhouette_path)
    m = measure(image)
    alpha = np.asarray(image.getchannel('A'))
    subject = 'K2/' + direction
    rows.append(result('registered_rgba_output', subject, notes='Not produced: source is 1024x1536; no reviewed registration annotations or locked common scale supplied, and frozen registration requires square input. Native matte measured in memory only.'))
    rows.append(result('matte', subject, notes=json.dumps({'input': path, 'canvas': list(image.size), 'extraction': extraction}), evidence=[path]))
    g1 = g1_height.evaluate(image, master, subject=subject, tolerance=.03)
    g1['notes'] = json.dumps({'literal_tool_result': dict(g1), 'height_px': m['height'], 'master_height_px': master_measure['height'], 'ratio_interval_inclusive': [.97, 1.03], 'measurement_space': 'native matte; no registration performed'})
    g1['value'] = m['height'] / master_measure['height']
    g1['threshold'] = [.97, 1.03]
    g1['op'] = 'within_inclusive'
    g1['unit'] = 'ratio'
    rows.append(g1)
    rows.append(g2_pivot.root_anchor(anchor=None, subject=subject, pivot=(256, 400), tolerance=4))
    rows.append(g3_light.evaluate(image, subject=subject))
    shape = silhouette64.evaluate(image, master, subject=subject, threshold=None)
    shape['notes'] += '; Native 1024x1536 alpha is resized to 64x64 by the frozen descriptor; analytical instrument only, not registered artwork.'
    shape['evidence'] = [silhouette_path, 'out/k2_S_64.png']
    rows.append(shape)
    rows.append(plate_uniformity.measure(source, subject_alpha=alpha, tol=8, min_fraction=None, subject=subject))
    rows.extend(g9_alpha.evaluate(image, subject=subject, dark_threshold=None))
    rows.append(keylight.azimuth(image, alpha, mask=None, key_azimuth_deg=135, tolerance=None, min_resultant=0, erosion_px=1, display_scale=None, subject=subject))
    raw = motif.count_family(image, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=.50, allowed_masks=None, display_scale=None, hollow_min=0, max_outside=None, subject=subject)
    raw['id'] = 'O3b_raw'
    rows.append(raw)
    annulus = motif.count_family(image, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=.50, allowed_masks=None, display_scale=None, hollow_min=.5, max_outside=None, subject=subject)
    annulus['id'] = 'O3b_annulus'
    rows.append(annulus)
    rows.append(result('alpha_bbox_px', subject, value=m['bbox'], unit='px_xyxy_exclusive', notes='Alpha >=128; measurement only', evidence=[path]))
    rows.append(result('alpha_bbox_canvas_fraction', subject, value=((m['bbox'][2]-m['bbox'][0]) * m['height']) / (image.width * image.height), unit='fraction', notes='Bounding rectangle area / canvas area; alpha >=128; measurement only'))
    rows.append(result('alpha_support_canvas_fraction', subject, value=float(np.mean(alpha >= 128)), unit='fraction', notes='Opaque alpha support area / canvas area; measurement only'))
    rows.append(result('bleed_index', subject, notes='UNEVALUABLE: no frozen bleed-index formula or reviewed allowed motif regions supplied. O3b_raw and O3b_annulus report unmasked full-canvas counts, not verified ornament bleed. G9 separately reports partial-alpha green contamination.'))
    print(json.dumps({'direction': direction, 'canvas': image.size, 'bbox': m['bbox'], 'height_ratio': g1['value'], 'g3_value_px': g3_light.evaluate(image, subject=subject)['value'], 'silhouette_distance': shape['value'], 'raw_ring_count': raw['value'], 'annulus_ring_count': annulus['value']}, allow_nan=False), flush=True)
Path('out/checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
PY

Exact final hash command

shasum -a 256 out/checks.json out/checks_readme.txt out/k2_*_64.png

Only task artifacts are enumerated in the receipt. The pre-existing, actively written out/.wrapper-* files belong to the conductor wrapper and are not task deliverables.
