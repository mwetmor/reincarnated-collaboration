K3p-chk-01 — exact measurement command follows.

Frozen tools and named inputs are read-only. Only out/ files are written. Python bytecode is disabled.
No source code files were created or modified; the inline Python only invokes frozen measurements and serializes their results.

CLI limitation:
The requested command
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B -m oracle.idle_bands --ours /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-cmp-01/composited --fps 8 --label idle_S_K3p --out out/idle_S_K3p_measure.json --plot_dir out/plots
was NOT executed. Source inspection shows that --ours ignores --out and writes to the repository's runs/C-1/oracle/idle_S_K3p_ours.json. The command below calls the frozen curves/_plots/_write functions directly, without modifying module code or globals, to keep all outputs under out/.

G11: the frozen drift48 evaluator requires cast05. None was supplied. Its result retains a null verdict. Every adjacent pair including 15->0 is measured with the documented 48px LANCZOS reduction and frozen pair_differences. Their verdicts remain null; no substitute comparator is invented.
Silhouette64: all distances, aligned IoUs, contour distances and Hu moments are reported. No calibrated threshold was supplied, so verdicts are null.
G6c: the frozen idle fallback is G6b, reported separately.
Soles: automatic frozen frame_contacts, with both contact coordinates and mean-Y sole line. This is separate from the idle_intent mandatory pairwise sole-mask distance; automatic contacts are not reviewed anatomical IDs.
Bands: stored precision retained; relaxed is committed=true and provisional=true. Combat is comparison only.
FPS: oracle curves use 8 fps. Frozen idle_intent uses row provenance fps or its default 12; no band rows were modified.
Plot shading is the frozen CLI's candidate-derived amplitude shading, not an overlay of committed thresholds; committed limits are in checks.json.
Period estimation requires at least two cycles; any null period is retained as reported by the frozen estimator.

Executed measurement command:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B - <<'PY'
import json
import hashlib
from pathlib import Path
from PIL import Image
from gates import idle_intent, g6_seam, drift48, g1_height, silhouette64
from gates.common import result, measure, rgba, pair_differences
from gates.register import frame_contacts
from oracle.idle_curves import curves, CALIBRATION
from oracle.motion_map import alpha_box, load_frames, frame_paths
from oracle.idle_bands import _plots, _write

root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
directory = root / 'runs/C-1/artifacts/K3p-cmp-01/composited'
band_path = root / 'oracle/bands_idle.json'
out = Path('out')
label = 'idle_S_K3p'
paths = frame_paths(directory)
assert [p.name for p in paths] == [f'idle_S_{i:02d}.png' for i in range(16)]
input_hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths + [band_path]}
bands = json.loads(band_path.read_text())
assert bands['relaxed']['committed'] is True
frames = [rgba(p) for p in paths]
assert all(f.size == (512,512) for f in frames)
results = [
    idle_intent.evaluate(directory, bands['relaxed'], label+'/relaxed'),
    idle_intent.evaluate(directory, bands['combat'], label+'/combat')
]
results[1]['notes'] += '; comparison only; relaxed is the shipping band'
box = alpha_box(directory)
data = curves(directory, box, 8, ours=True)
data['provenance'] = {
    'source_note': 'own registered sprite: '+str(directory),
    'frames': data['frames'], 'fps': 8, 'box': box,
    'tau': data['tau'], 'eps': data['eps'], 'floor': data['floor'],
    'calibration_note': CALIBRATION, 'control_box': data['control_box'],
    'noise_calibration': data['noise_calibration'], 'estimator': data['estimator'],
    'frame_names': [p.name for p in paths],
    'invocation_note': 'Frozen curves, _plots and _write called directly: CLI --ours ignores --out and writes to its repository OURS_ROOT. No frozen module or global was modified.'
}
data['result']['evidence'] = _plots(out/'plots', label, load_frames(directory), data)
_write(out/'idle_S_K3p_measure.json', data)
results.append(data['result'])
results += g6_seam.evaluate(frames, label)
results.append(g6_seam.g6c(frames, label, animation='idle'))
results.append(drift48.evaluate(frames, subject=label))
small = [rgba(f).resize((48,48), Image.Resampling.LANCZOS) for f in frames]
for i, pair in enumerate(pair_differences(small)):
    results.append(result(
        'drift48_pair', f'{label}/{i:02d}->{(i+1)%16:02d}',
        value=pair, unit='rgb_mad',
        notes='48px LANCZOS RGBA reduction and frozen common.pair_differences; canvas and foreground_union MAD. Null verdict: no cast05 supplied for the frozen G11 strict cross-cast comparator.'))
measurements = []
for i, (p, f) in enumerate(zip(paths, frames)):
    results.append(g1_height.evaluate(f, frames[0], p.name))
    results.append(silhouette64.evaluate(f, frames[0], p.name))
    m = measure(f)
    contacts = frame_contacts(f)
    measurements.append({
        'frame': p.name, 'alpha_bbox': m['bbox'], 'alpha_bbox_height_px': m['height'],
        'alpha_bottom_y_px': m['bbox'][3]-1,
        'sole_contacts_xy_px': contacts,
        'sole_line_y_px': sum(point[1] for point in contacts)/2
    })
results.append(result('frame_geometry', label, value=measurements, unit='px',
    notes='Alpha bbox uses alpha>=128, exclusive x1/y1. Sole line is the mean Y of two frozen frame_contacts automatic front-view contacts; contacts are screen-left/right, not reviewed anatomical IDs. Descriptive measurements, no threshold.'))
heights = [m['alpha_bbox_height_px'] for m in measurements]
soles = [m['sole_line_y_px'] for m in measurements]
bottoms = [m['alpha_bottom_y_px'] for m in measurements]
results.append(result('sole_spread', label, value={
    'sole_line_min_y_px': min(soles), 'sole_line_max_y_px': max(soles),
    'sole_line_max_spread_px': max(soles)-min(soles),
    'screen_left_sole_y_spread_px': max(m['sole_contacts_xy_px'][0][1] for m in measurements)-min(m['sole_contacts_xy_px'][0][1] for m in measurements),
    'screen_right_sole_y_spread_px': max(m['sole_contacts_xy_px'][1][1] for m in measurements)-min(m['sole_contacts_xy_px'][1][1] for m in measurements),
    'height_min_px': min(heights), 'height_max_px': max(heights),
    'height_max_spread_px': max(heights)-min(heights),
    'alpha_bottom_max_spread_px': max(bottoms)-min(bottoms)
}, unit='px', notes='Descriptive spread; no new acceptance threshold. Mandatory sole-mask displacement and 0.0025 H gate remain in the idle_intent payload.'))
results.append(result('input_provenance', label, value={
    'sha256': input_hashes,
    'bands_used': {k: {key: bands[k].get(key) for key in
        ['committed','provisional','breath_amplitude_H','head_sway_H','lock_regions','motion_regions','lock_eps_H']}
        for k in ['relaxed','combat']}
}, notes='Named inputs only; committed rows passed unchanged to the frozen evaluator. Idle intent internally uses row provenance fps or default 12; oracle curves explicitly use 8 fps. Amplitude and displacement gates do not depend on fps.'))
assert input_hashes == {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths + [band_path]}
_write(out/'checks.json', results)
print(json.dumps({
    'intent': [{'subject':r['subject'], 'breath':r['value']['breath'], 'head_bob':r['value']['head_bob'],
        'classification':r['value']['classification'], 'sole_displacement_H':r['value']['sole_displacement_H'],
        'checks':r['value']['checks']} for r in results[:2]],
    'seams':[{'id':r['id'],'value':r['value'],'threshold':r['threshold'],'passed':r['passed']} for r in results if r['id'] in ['g6_seam','g6b','g6c']],
    'oracle_summary':data['summary'],
    'spread':next(r['value'] for r in results if r['id']=='sole_spread'),
    'result_envelopes':len(results)
}, indent=2, allow_nan=False))
PY
