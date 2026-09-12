K3-chk-01 registered idle/S and walk/S checks

Outputs
- checks.json: 267 SPEC section 1 result envelopes.
- evidence/: empty. The named frozen gates have no PNG-emission interface; requested seam-diff images and drift strips could not be produced within this CHECK burst's no-code constraint.

Interpretation and limitations
G1 uses idle_S_00.png as the master for both loops and alpha >=128 height.
Silhouette64 compares each frame to frame 0 of its own loop; distances are measured, verdicts null because no threshold was supplied.
Literal G5 is null because no cast05 input was supplied. All full-resolution adjacent/seam MAD measurements are included. g5_frame04_proxy is separately labeled supplemental and does not replace literal G5.
G11/drift48 uses the requested frame-0-versus-frame-4 comparator. Each of seven internal pairs and the frame-7-to-frame-0 seam has a separate envelope. RGB MAD uses the frozen [20,25,34] composite.
G6 literal compares seam MAD <= minimum internal pair MAD. G6b compares seam MAD <= median internal pair MAD. Frozen booleans are preserved independently; no shipping ruling is made.
G9 dark-fringe verdicts are null: the frozen gate requires visual inspection or an explicitly calibrated numeric threshold, which was not supplied. Edge mean, green contamination, and registered-canvas clipping are measured.
Plate uniformity is N/A on matted RGBA. Each alpha >0 bbox height and bottom-most alpha row is measured directly from the named PNG. Alpha >=128 values are separately reported. The maximum within-loop spreads are included. A bottom-most alpha row is not an anatomical planted-foot contact.
G2 independent root and planted trajectory remain null without reviewed inputs. The fixed registration pivot is recorded as provenance only.
Registration metadata records walk_S_07 source-cell top-edge contact. Registered-canvas G9 clipping cannot establish absence of prior source-cell clipping; no source sheets were read.
No image generation, input edits, persisted source-code files, or writes outside out/. Python invocations only call frozen measurements and assemble/verify report data.
Wrapper-owned hidden event/stderr files are live runtime logs, not authored check deliverables; their hashes cannot be frozen during this turn.

Working directory
/Users/admin/astra-burst/runs/C-1/K3-chk-01

Exact measurement invocation
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
import hashlib
from pathlib import Path
from gates.common import rgba, measure, difference, pair_differences, result
from gates import g1_height, g2_pivot, g3_light, g5_drift, g6_seam, g9_alpha, drift48, silhouette64

root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-01')
registration = json.loads((root / 'registration.json').read_text())
master = root / 'frames/idle/S/idle_S_00.png'
out = Path('out')
(out / 'evidence').mkdir(parents=True, exist_ok=True)
rows = [
    result('check_scope', 'K3-chk-01', notes='Registered idle/S and walk/S only. G1 master is idle_S_00.png for both loops. Silhouette reference is frame 0 of each loop. G5 literal has no cast05. G11 uses frame 0 versus frame 4 as explicitly requested; this is not a cast comparison. No dark-fringe or silhouette threshold supplied. All gate booleans are frozen-tool outputs; no overall verdict.'),
    result('registration_provenance', 'K3-chk-01', notes=json.dumps({'path': str(root / 'registration.json'), 'sha256': hashlib.sha256((root / 'registration.json').read_bytes()).hexdigest(), 'transform': registration['transform'], 'measurement_conventions': registration['measurement_conventions']})),
    result('evidence_pngs', 'K3-chk-01', notes='UNEVALUABLE: named frozen measurement gates return result envelopes only; they have no PNG emission interface. No seam diff PNGs or drift strips produced because creating gate code is prohibited.')
]
for anim in ('idle', 'walk'):
    subject = anim + '/S'
    frames = [root / 'frames' / anim / 'S' / (anim + '_S_%02d.png' % i) for i in range(8)]
    rows.append(result('frame_count', subject, len([f for f in frames if f.exists()]), 8, op='==', unit='frames'))
    heights = []
    soles = []
    core_heights = []
    core_soles = []
    for i, f in enumerate(frames):
        key = f.relative_to(root / 'frames').as_posix()
        im = rgba(f)
        m = measure(im)
        box = list(im.getchannel('A').getbbox())
        height = box[3] - box[1]
        sole = box[3] - 1
        heights.append(height)
        soles.append(sole)
        core_heights.append(m['height'])
        core_soles.append(m['bbox'][3] - 1)
        rows.append(result('frame_metadata', key, notes=json.dumps({'path': str(f), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(), 'canvas': list(im.size), 'mode': im.mode, 'frame_index': i})))
        rows.append(g1_height.evaluate(im, master, key))
        rows.append(g3_light.evaluate(im, key))
        rows.extend(g9_alpha.evaluate(im, key))
        rows.append(silhouette64.evaluate(im, frames[0], key))
        rows.append(result('alpha_bbox_height', key, height, unit='px', notes=json.dumps({'alpha_threshold': '>0', 'bbox_half_open': box, 'reason': 'Measurement only; includes resampling fringes'})))
        rows.append(result('sole_line', key, sole, unit='px', notes='Zero-based bottom-most alpha >0 row, includes resampling fringes; not an anatomical planted-sole annotation.'))
        rows.append(result('alpha_ge128_height', key, m['height'], unit='px', notes=json.dumps({'bbox_half_open': m['bbox'], 'reason': 'Frozen G1 support convention; measurement only'})))
        rows.append(result('alpha_ge128_sole_line', key, m['bbox'][3] - 1, unit='px', notes='Zero-based bottom-most alpha >=128 row; measurement only.'))
        rows.append(g2_pivot.root_anchor(None, key))
    rows.append(g2_pivot.planted_trajectory(subject=subject))
    rows.append(result('sole_line_spread', subject, max(soles) - min(soles), unit='px', notes=json.dumps({'alpha_threshold': '>0', 'sole_lines': soles, 'min': min(soles), 'max': max(soles), 'reason': 'Measurement only; no independent root or planted-sole claim'})))
    rows.append(result('alpha_bbox_height_spread', subject, max(heights) - min(heights), unit='px', notes=json.dumps({'alpha_threshold': '>0', 'heights': heights})))
    rows.append(result('alpha_ge128_sole_line_spread', subject, max(core_soles) - min(core_soles), unit='px', notes=json.dumps({'sole_lines': core_soles})))
    rows.append(result('alpha_ge128_height_spread', subject, max(core_heights) - min(core_heights), unit='px', notes=json.dumps({'heights': core_heights})))
    rows.append(result('plate_uniformity', subject, notes='N/A: supplied frames are matted RGBA; original flat-green plates were not supplied. Alpha bbox heights and sole-line spreads are reported separately.'))
    rows.append(g5_drift.evaluate(frames, None, subject))
    for i, pair in enumerate(pair_differences(frames)):
        rows.append(result('g5_pair_mad', subject + '/%d->%d' % (i, (i+1)%8), pair['canvas'], unit='rgb_mad', notes=json.dumps({'pair': [i, (i+1)%8], 'seam': i == 7, 'foreground_union_mad': pair['foreground_union'], 'composite_rgb': [20,25,34], 'reason': 'No cast05 comparator; literal G5 comparison unavailable'})))
    proxy = g5_drift.evaluate(frames, frames[4], subject)
    proxy['id'] = 'g5_frame04_proxy'
    proxy['notes'] = 'Supplemental frame-0-versus-frame-4 proxy, NOT literal G5; ' + proxy['notes'].replace('cross_cast_05', 'comparator_frame_04')
    rows.append(proxy)
    rows.extend(g6_seam.evaluate(frames, subject))
    small = drift48.evaluate(frames, frames[4], subject)
    small['notes'] = 'G11: requested frame-0-versus-frame-4 comparator in absence of cast frame; ' + small['notes'].replace('cross_cast_05', 'comparator_frame_04')
    rows.append(small)
    pair_data = json.loads(small['notes'][small['notes'].index('{'):])
    for i, pair in enumerate(pair_data['adjacent_and_seam']):
        rows.append(result('drift48_pair', subject + '/%d->%d' % (i, (i+1)%8), pair['canvas'], small['threshold'], op='<', unit='rgb_mad', notes=json.dumps({'pair': [i, (i+1)%8], 'seam': i == 7, 'foreground_union_mad': pair['foreground_union'], 'comparator': 'frame 0 versus frame 4; no cast frame', 'comparator_mad': pair_data['comparator_frame_04'], 'method': 'Frozen drift48: 48x48 LANCZOS RGBA then RGB composite on [20,25,34]'})))
(out / 'checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False) + '\n')
print(json.dumps({'result_envelopes': len(rows), 'loop_measurements': [r for r in rows if r['id'] in ('g5_drift', 'g5_frame04_proxy', 'g6_seam', 'g6b', 'drift48', 'sole_line_spread', 'alpha_bbox_height_spread')]}, indent=2))
PY

Exact verification invocation
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json
import hashlib
from pathlib import Path
rows = json.loads(Path('out/checks.json').read_text())
required = {'id','subject','passed','value','threshold','op','unit','evidence','notes'}
assert all(set(r) == required for r in rows)
assert all(r['passed'] is None or type(r['passed']) is bool for r in rows)
for anim in ('idle', 'walk'):
    prefix = anim + '/S'
    for gate, count in [('g1_height',8),('g3_light',8),('g9_alpha',8),('g9_green',8),('g9_edge_mean',8),('g9_dark_fringe',8),('silhouette64',8),('sole_line',8),('alpha_bbox_height',8),('g5_drift',1),('g6_seam',1),('g6b',1),('drift48',1),('drift48_pair',8),('g5_pair_mad',8)]:
        assert len([r for r in rows if r['id'] == gate and r['subject'].startswith(prefix)]) == count, (anim, gate)
metadata = [json.loads(r['notes']) for r in rows if r['id'] == 'frame_metadata']
assert len(metadata) == 16
for item in metadata:
    assert item['canvas'] == [512,512] and item['mode'] == 'RGBA'
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256']
registration_path = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-01/registration.json')
registration = json.loads(registration_path.read_text())
for item in registration['frames']:
    key = item['animation'] + '/S/' + item['name'] + '.png'
    for gate, field in [('sole_line','sole_line'), ('alpha_bbox_height','alpha_bbox_height_px'), ('alpha_ge128_height','alpha_ge_128_height_px'), ('alpha_ge128_sole_line','alpha_ge_128_sole_line')]:
        assert next(r['value'] for r in rows if r['id'] == gate and r['subject'] == key) == item[field]
print(json.dumps({'envelopes':len(rows), 'frames':len(metadata), 'input_hashes_unchanged':True, 'alpha_measurements_match_registration':True, 'numeric_summary':{anim:{gate:[r['value'] for r in rows if r['id']==gate and r['subject'].startswith(anim+'/S')] for gate in ('g1_height','g3_light','g9_green')} for anim in ('idle','walk')}}, indent=2))
PY

Exact deliverable checksum command
shasum -a 256 out/checks.json out/checks_readme.txt
