K3p-chk-walk-01 — measurements and reproduction commands

All output is under out/. No source files, frozen tool files, or input images were modified. Python bytecode writes were disabled. The inline invocation below is command plumbing around frozen functions; no executable source file was created.

Instrument limitations:
1. The supplied CLI command was not executed: oracle.walk_bands.main ignores --out in its --ours branch and unconditionally writes to OURS_ROOT inside the repository. Instead, the exact frozen curves(), bands(), _plots(), and _write() functions were invoked with explicit output paths, with fps=12 and k_vert=1.25. No function or module configuration was changed.
2. gait_intent received a deep copy of committed plate13_lateral_ann with exactly arm_roles={"near":"free_arm","far":"weapon_arm"}, plus the dope-sheet frames in order. The frozen implementation looks up assignment["L"] and assignment["R"], so it does not recognize those supplied near/far keys. W5_L=0.064 and W5_R=0.044 are retained with role limits in their notes, but their role flags are null. No screen-to-anatomical identity was invented.
3. W6 pooled value/flag and R opposed count are null: R foot samples are missing at zero-based frames 1 and 10. L has 3 opposed frames of 12. The full landmark payload and planted-foot table retain missing values and ambiguity flags. Contact inference from ground-only stance observes four events, so inferred phase/lead labels are null; candidate dope phases are preserved separately.
4. Frozen drift48.evaluate requires a cast05 comparator, which was not among the named inputs. Its original unevaluable result is retained. All 12 adjacent/seam MADs were measured using the exact 48px LANCZOS RGBA reduction and frozen common.pair_differences. G11 pair thresholds/flags remain null.
5. silhouette64 distances are numeric; no calibrated silhouette threshold was supplied, so flags remain null. Sole/ground spreads and planted-scroll values are descriptive and have no supplied thresholds. No planted-slip ceiling exists in the committed row.
6. The oracle CLI lineage uses NCC head tracking and stationary-x stance; gait_intent uses mask head and ground-only stance for registered in-place sprites. They produce distinct measurements and are kept distinct. Oracle W1=0.084; gait-intent W1=0.088. The oracle W1 sanity diagnostic is false. Its plot uses inferred oracle phases and provisional self-derived bands, not the committed phase schedule or acceptance bands. Committed comparisons live in the gait-intent envelopes.
7. The frozen plot labels samples 1..12; JSON frame indices are 0..11. Mask-check evidence shows frames 0 and 6 using the oracle lineage.
8. Sole line and ground line are both 411 px for every frame; both spreads are 0 px. Ground is defined by the instrument as a clip-wide maximum, so sole-line spread is the independent per-frame alignment measurement. These are sole measurements, not an inferred atlas root anchor.
9. The original gait-intent payload is preserved without edits. Its W3c unit string is fraction_H even though the value is a crossing count; W3c value is 4.
10. The literal G6 flag remains separate from G6b and G6c. No shipping verdict or threshold substitution is made.

Exact measurement command executed:
mkdir -p out/plots
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import copy
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
from gates import gait_intent, g6_seam, drift48, g1_height, silhouette64
from gates.common import result, rgba, pair_differences
from oracle import walk_bands
from oracle.walk_curves import curves, measure_sequence
from oracle.walk_landmarks import figure_mask, track_landmarks_otsu_stance_lineage

root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
frames_dir = root/'runs/C-1/artifacts/K3p-reg-walk-01/frames/walk/E'
rest = root/'runs/C-1/artifacts/K3p-reg-walk-01/frames/rest/E/rest_E.png'
band_path = root/'oracle/bands_walk.json'
dope_path = root/'runs/C-1/oracle/dope_walk_12.json'
paths = [frames_dir/f'walk_E_{i:02d}.png' for i in range(12)]
inputs = [*paths, rest, band_path, dope_path]
before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
row = copy.deepcopy(json.loads(band_path.read_text())['plate13_lateral_ann'])
row['arm_roles'] = {'near': 'free_arm', 'far': 'weapon_arm'}
dope = json.loads(dope_path.read_text())
phases = sorted(dope['frames'], key=lambda f:f['frame'])
assert [p['frame'] for p in phases] == list(range(12))
assert row['committed'] is True
intent = gait_intent.evaluate(frames_dir, row, phases)
output = list(intent)
output.extend(g6_seam.evaluate(paths, 'walk/E'))
output.append(g6_seam.g6c(paths, 'walk/E', animation='walk'))
output.append(drift48.evaluate(paths, subject='walk/E'))
small = [rgba(p).resize((48,48), Image.Resampling.LANCZOS) for p in paths]
pairs = pair_differences(small)
for i, pair in enumerate(pairs):
    output.append(result('G11_pair', f'walk/E/{i:02d}->{(i+1)%12:02d}', pair['canvas'],
        unit='rgb_mad', notes=json.dumps({'foreground_union':pair['foreground_union'],
        'seam':i==11, 'reason':'No cast05 reference supplied; comparison threshold and passed remain null.',
        'definition':'Frozen drift48 reduction (48px LANCZOS RGBA), then frozen common.pair_differences.'})))
for p in paths:
    output.append(g1_height.evaluate(p, rest, str(p)))
    output.append(silhouette64.evaluate(p, rest, str(p)))
masks = [figure_mask(np.array(rgba(p))) for p in paths]
seq = track_landmarks_otsu_stance_lineage(masks)
lineage = measure_sequence(seq, subject='walk/E')
output.append(result('gait_intent_landmark_payload', 'walk/E', lineage,
    unit='payload', notes='Full underlying ground-proximity lineage used by gait_intent; descriptive payload, no threshold.'))
for i, lm in enumerate(seq):
    output.append(result('sole_line', str(paths[i]), lm.get('sole_line_y'), unit='px',
        notes='Frozen gait-intent landmark sole line in source coordinates; no registered threshold.'))
    output.append(result('ground_line', str(paths[i]), lm.get('ground_line_y'), unit='px',
        notes='Frozen lineage uses clip-wide maximum sole y; no registered threshold.'))
sole = [lm['sole_line_y'] for lm in seq]
ground = [lm['ground_line_y'] for lm in seq]
output.append(result('sole_line_spread', 'walk/E', max(sole)-min(sole), unit='px',
    notes=json.dumps({'per_frame':sole,'definition':'max minus min sole_line_y; no registered threshold.'})))
output.append(result('ground_line_spread', 'walk/E', max(ground)-min(ground), unit='px',
    notes=json.dumps({'per_frame':ground,'definition':'max minus min ground_line_y; clip-wide by construction, also see sole_line_spread; no registered threshold.'})))
table = [{'frame':i,'file':paths[i].name,'candidate_phase':phases[i]['phase'],
    'sole_line_y':lm.get('sole_line_y'),'ground_line_y':lm.get('ground_line_y'),
    'foot_L_x':lm.get('foot_L_x'),'foot_R_x':lm.get('foot_R_x'),
    'foot_L_y':lm.get('foot_L_y'),'foot_R_y':lm.get('foot_R_y'),
    'planted':lm.get('planted'),
    'planted_x_px':{s:lm.get('foot_'+s+'_x') if lm.get('planted_'+s) is True else None for s in ('L','R')},
    'identity_ambiguous':lm.get('identity_ambiguous'),
    'foot_identity':lm.get('foot_identity')} for i,lm in enumerate(seq)]
output.append(result('planted_foot_table', 'walk/E', table, unit='source_px',
    notes='Ground-proximity lineage appropriate to in-place sprites. L/R are screen tracks, not near/far anatomical labels; missing tracks remain null. No threshold.'))
output.append(result('planted_sole_trajectory', 'walk/E',
    lineage['summary']['sole_scroll']['planted_scroll_lineage'], unit='px_per_frame',
    notes='Frozen instrument includes seam delta when both endpoint samples of the same track are planted; no registered slip ceiling.'))
opposition = lineage['summary'].get('W6_per_arm')
output.append(result('W6_opposed_frame_counts', 'walk/E',
    {s: {'fraction':opposition.get(s),'opposed_frames':None if opposition.get(s) is None else opposition[s]*12,
         'total_frames':12} for s in ('L','R')}, unit='frames',
    notes='Counts are frozen opposed fractions multiplied by 12; missing-data results remain null. Screen-track proxy, not anatomical same-side identity.'))

# Call frozen functions directly: CLI --ours ignores --out and writes into the repository.
data = curves(frames_dir, pattern='*.png', fps=12, lateral=True, ours=True, mask_method='A')
band = walk_bands.bands(data['summary'], k_vert=1.25, k_lat=.5)
data['provenance'] = dict(plate='walk', row='K3p', source=str(frames_dir.resolve()),
    source_note='own registered sprites', frame_names=data['frame_names'], frames=data['frames'],
    fps=12, pattern='*.png', mask_params=data['mask_params'], k_vert=1.25, k_lat=.5)
evidence = walk_bands._plots(Path('out/plots').resolve(), 'walk_E_K3p', paths, data, band)
for r in data['results']:
    r['evidence'] = evidence
walk_bands._write(Path('out/walk_E_K3p_measure.json'), data)
output.append(result('oracle_walk_payload', 'walk/E', data['summary'], unit='payload',
    notes='CLI-equivalent frozen functions; output explicitly redirected using _write. Oracle stationary-x stance/NCC head differs from gait_intent ground-only stance/mask head. Derived plot bands are provisional self-measurement bands, not committed acceptance bands.',
    evidence=evidence))
output.append(result('input_provenance', 'walk/E', before, unit='sha256',
    notes=json.dumps({'committed_row':'plate13_lateral_ann','arm_roles':row['arm_roles'],
    'candidate_phases':[p['phase'] for p in phases],
    'expected_phases':[p['phase'] for p in row['phase_table']],
    'notes':'Committed row copied in memory; inputs unchanged.'})))
assert before == {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
Path('out/checks.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
print(json.dumps({'results':len(output),'gait_intent':intent,
    'loop':[r for r in output if r['id'] in ('g6_seam','g6b','g6c')],
    'sole_line_spread':max(sole)-min(sole),'ground_line_spread':max(ground)-min(ground),
    'planted_foot_table':table,'oracle_summary':data['summary']},allow_nan=False))
PY

Exact output-validation and hashing command:
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import hashlib
import json
from pathlib import Path
from PIL import Image
out = Path('out')
checks = json.loads((out/'checks.json').read_text())
fields = {'id','subject','passed','value','threshold','op','unit','evidence','notes'}
assert len(checks) == 84
assert all(set(r)==fields and (r['passed'] is None or isinstance(r['passed'],bool)) for r in checks)
assert sum(r['id']=='G11_pair' for r in checks)==12
assert sum(r['id']=='g1_height' for r in checks)==12
assert sum(r['id']=='silhouette64' for r in checks)==12
assert sum(r['id']=='sole_line' for r in checks)==12
assert sum(r['id']=='ground_line' for r in checks)==12
assert {r['id'] for r in checks} >= {'g6_seam','g6b','g6c','W1_floor','W1_ceiling','W2','W3a','W3c_floor','W3c_ceiling','W4','W5_L','W5_R','W6'}
measure = json.loads((out/'walk_E_K3p_measure.json').read_text())
assert measure['frames']==12 and measure['fps']==12 and len(measure['landmarks'])==12
for p in out.glob('plots/*.png'):
    with Image.open(p) as im:
        im.verify()
provenance = next(r['value'] for r in checks if r['id']=='input_provenance')
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha for p,sha in provenance.items())
print(json.dumps({'envelopes':len(checks),'G1':[{'subject':r['subject'],'value':r['value'],'passed':r['passed']} for r in checks if r['id']=='g1_height'],
 'files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.rglob('*')) if p.is_file()]},indent=2))
PY

