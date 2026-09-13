K3p-chk-walk-xv2 — frozen CHECK measurements
All frame indices are zero-based. No input images or frozen code were changed.

Commands were run from /Users/admin/astra-burst/runs/C-1/K3p-chk-walk-xv2.
The Python here-documents are invocation/serialization adapters for frozen functions, not new tool implementations or saved code modules. Bytecode writes were disabled.

Requested CLI (NOT EXECUTED):
python3 -m oracle.walk_bands --ours /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-xv-cut-04/frames/walk/E --fps 12 --label walk_E_K3p --k_vert 1.25 --out out/walk_E_K3p_measure.json --plot_dir out/plots

Source inspection found that the --ours branch ignores --out and calls _write on repository OURS_ROOT. To obey the output boundary, the identical frozen curves/bands/plotting functions were invoked directly and _write was given out/walk_E_K3p_measure.json. No monkeypatch, source edit, or repository write was used. The plot's "provisional bands" caption is emitted by the frozen plotting tool: it describes candidate-derived plot shading, not the committed plate13_lateral_ann gate thresholds.

EXACT MEASUREMENT COMMAND:
mkdir -p out/plots
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B - <<'PY'
import json
from pathlib import Path
from oracle.walk_curves import curves, frame_paths
from oracle.walk_bands import bands, _plots, _write
root=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
frames=root/'runs/C-1/artifacts/K3p-xv-cut-04/frames/walk/E'
data=curves(frames,pattern='*.png',fps=12,lateral=True,ours=True,mask_method='A')
data['provenance']=dict(plate='walk',row='K3p',source=str(frames),source_note='own registered sprites',frame_names=data['frame_names'],frames=data['frames'],fps=12,pattern='*.png',mask_params=data['mask_params'],k_vert=1.25,k_lat=.5)
b= bands(data['summary'],k_vert=1.25,k_lat=.5)
evidence=_plots(Path('out/plots').resolve(),'walk_E_K3p',frame_paths(frames,'*.png'),data,b)
for r in data['results']: r['evidence']=evidence
_write(Path('out/walk_E_K3p_measure.json'),data)
print(json.dumps(dict(summary=data['summary'],plots=evidence,mask_stability=data.get('mask_stability'),landmark_keys=list(data['landmarks'][0])),allow_nan=False))
PY

EXACT GATE AND SERIALIZATION COMMAND:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B - <<'PY'
import copy, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image
from gates import gait_intent, g6_seam, drift48, g1_height, silhouette64
from gates.common import result, rgba, pair_differences, measure
from oracle.motion_map import frame_paths
from oracle.walk_landmarks import figure_mask, track_landmarks_otsu_stance_lineage
from oracle.walk_curves import measure_sequence
root=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
frames=root/'runs/C-1/artifacts/K3p-xv-cut-04/frames/walk/E'
rest=root/'runs/C-1/artifacts/K3p-xv-cut-04/frames/rest/E/rest_E.png'
band_path=root/'oracle/bands_walk.json'
dope_path=root/'runs/C-1/oracle/dope_walk_12.json'
row=json.loads(band_path.read_text())['plate13_lateral_ann']
phases=json.loads(dope_path.read_text())['frames']
assert row['committed'] is True
paths=frame_paths(frames)
assert len(paths)==12
images=[rgba(p) for p in paths]
seq=track_landmarks_otsu_stance_lineage([figure_mask(np.array(im)) for im in images])
intent_data=measure_sequence(seq)
checks=[]
metadata=dict(task_id='K3p-chk-walk-xv2',frames=[str(p) for p in paths],rest=str(rest),band_row='plate13_lateral_ann',committed=True,candidate_phases=[p['phase'] for p in phases],expected_phases=[p['phase'] for p in row['phase_table']],input_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*paths,rest,band_path,dope_path]},indexing='zero-based; original frame order unchanged')
checks.append(result('provenance',str(frames),metadata,notes='Descriptive provenance; no threshold. Frozen band and dope sheet both begin DOWN, despite the task prose describing a CONTACT origin.'))
assignments=[{'L':'weapon_arm','R':'free_arm'},{'L':'free_arm','R':'weapon_arm'}]
for assignment in assignments:
    trial=copy.deepcopy(row)
    assert not trial['bands'].get('W5_role_limits',{}).get('assignment')
    trial['arm_roles']=assignment
    payload=gait_intent.evaluate(frames,trial,phases)
    label='L_weapon_R_free' if assignment['L']=='weapon_arm' else 'L_free_R_weapon'
    checks.append(result('gait_intent_full',label,payload,notes=json.dumps(dict(arm_roles=assignment,rotation_left=0,reason='Full unmodified frozen result payload; container has no threshold.'))))
    for r in payload:
        q=copy.deepcopy(r);q['subject']=label+'/'+r['subject'];checks.append(q)
rotations=[]
expected=[p['phase'] for p in row['phase_table']]
trial=copy.deepcopy(row);trial['arm_roles']=assignments[0]
for k in range(12):
    rotated=phases[k:]+phases[:k]
    payload=gait_intent.evaluate(frames,trial,rotated)
    w2=next(r for r in payload if r['id']=='W2')
    notes=json.loads(w2['notes'])
    schedule_matches=sum(a==b for a,b in zip(notes['candidate_phases'],expected))
    extrema_matches=sum({p['phase'] for p in notes['observed_extrema'][kind]}=={p['phase'] for p in notes['expected_extrema'][kind]} for kind in ('min','max'))
    rotations.append(dict(rotation_left=k,source_phase_indices=[(i+k)%12 for i in range(12)],schedule_matches=schedule_matches,extrema_sets_matching=extrema_matches,result=w2))
best_score=max((r['schedule_matches'],r['extrema_sets_matching']) for r in rotations)
best=[r['rotation_left'] for r in rotations if (r['schedule_matches'],r['extrema_sets_matching'])==best_score]
checks.append(result('W2_rotation_search','walk/E',dict(rotation_zero=rotations[0],best_rotation_left=best[0],tied_best_rotations=best,best=rotations[best[0]],all_rotations=rotations),notes='Diagnostic search only: left-rotate candidate phase labels over fixed measured frames; maximize full-schedule matching positions, then matching extrema phase sets, then smallest rotation. No image rotation, mirroring, frame reordering, or threshold change. Every W2 envelope retains the frozen boolean.'))
checks.append(result('gait_landmarks_full','walk/E',intent_data,notes='Unmodified frozen stance-lineage extraction and measure_sequence payload used by gait_intent; contains all landmarks, curves and diagnostic summaries. Descriptive container.'))
checks.append(result('staff_arm_screen_track','walk/E',notes='UNEVALUABLE: frozen landmarks expose silhouette extents at 0.45H, not identified wrists or staff ownership; no anatomical near/far mapping is exposed. Both role assignments reported.'))
for assignment in assignments:
    label='L_weapon_R_free' if assignment['L']=='weapon_arm' else 'L_free_R_weapon'
    for side in ('L','R'):
        fraction=intent_data['summary']['W6_per_arm'][side]
        checks.append(result('W6_opposed_frames_'+side,label,None if fraction is None else fraction*12,9,op='>=',unit='frames',notes=json.dumps(dict(arm_role=assignment[side],total_frames=12,valid_frames=intent_data['summary']['valid_frames_per_arm'][side],fraction=fraction,reason='Missing tracked foot samples prevent complete 12-frame opposition; no imputation.' if fraction is None else 'Frozen projected-track opposed fraction multiplied by 12; not anatomical same-side identification.'))))
checks.extend(g6_seam.evaluate(images,'walk/E'))
checks.append(g6_seam.g6c(images,'walk/E',animation='walk'))
checks.append(drift48.evaluate(images,subject='walk/E'))
small=[rgba(im).resize((48,48),Image.Resampling.LANCZOS) for im in images]
pairs=pair_differences(small)
for i,pair in enumerate(pairs):
    checks.append(result('G11_pair',f'walk/E/{i:02d}->{(i+1)%12:02d}',pair['canvas'],op='<',unit='rgb_mad',notes=json.dumps(dict(pair=[i,(i+1)%12],foreground_union_mad=pair['foreground_union'],seam=i==11,reason='No cast05 input: literal G11 comparator and boolean unavailable. Numeric pair uses frozen common.pair_differences after the exact drift48 LANCZOS reduction and dark composite.'))))
for i,path in enumerate(paths):
    checks.append(g1_height.evaluate(path,rest,f'walk/E/{i:02d}'))
    checks.append(silhouette64.evaluate(path,rest,f'walk/E/{i:02d}'))
sole_rows=[]
planted_rows=[]
scroll=intent_data['summary']['sole_scroll']['planted_scroll_lineage']
for i,d in enumerate(seq):
    m=measure(images[i])
    sole_rows.append(dict(frame=i,sole_line_y=d['sole_line_y'],ground_line_y=d['ground_line_y'],alpha_bbox_sole_y=m['bbox'][3]-1,foot_L_y=d['foot_L_y'],foot_R_y=d['foot_R_y']))
    planted_rows.append(dict(frame=i,phase=phases[i]['phase'],foot_L_x=d['foot_L_x'],foot_R_x=d['foot_R_x'],planted=d['planted'],planted_x_px={s:scroll[s]['planted_x_px'][i] for s in ('L','R')},planted_delta_to_next_px={s:scroll[s]['delta_px_per_frame'][i] for s in ('L','R')},identity_ambiguous=d['identity_ambiguous'],foot_identity=d['foot_identity']))
checks.append(result('sole_lines','walk/E',sole_rows,unit='px',notes='Per-frame frozen gait stance-lineage sole and clip-wide ground; alpha bbox bottom included. No per-frame sole threshold supplied.'))
checks.append(result('ground_line_spread','walk/E',max(d['sole_line_y'] for d in seq)-min(d['sole_line_y'] for d in seq),unit='px',notes=json.dumps(dict(definition='max per-frame sole_line_y minus min per-frame sole_line_y',ground_estimator='clip-wide maximum sole line',clip_ground_line_y=seq[0]['ground_line_y'],estimated_ground_line_spread=max(d['ground_line_y'] for d in seq)-min(d['ground_line_y'] for d in seq),reason='Descriptive spread; no registered threshold supplied.'))))
checks.append(result('planted_foot_table','walk/E',planted_rows,unit='px',notes='Ground-proximity stance from the gait instrument, suitable for in-place scrolling feet. Missing L samples remain null; both tracked feet retained when planted. Not anatomical near/far.'))
checks.append(result('planted_scroll_full','walk/E',scroll,unit='px_per_frame',notes='Frozen planted_scroll_lineage, including seam only when both endpoint contacts exist. No registered slip ceiling.'))
concerns=[
'Exact oracle CLI not run: --ours ignores --out and writes to frozen repository OURS_ROOT. The same frozen curves, bands, _plots and _write functions were invoked directly with output paths under out/.',
'G11 per-pair MAD computed, but literal comparator and passed flags are unavailable because cast05 was not supplied.',
'Far/staff arm screen track is not exposed by the silhouette instrument; both hypothetical W5/W6 assignments are retained.',
'W6 pooled and L-arm opposed counts are null because L foot landmarks are missing in frames 2, 3, 4, 8, 9. Committed status cannot turn unavailable measurements into booleans.',
'Silhouette verdicts and planted-slip verdicts are null because no calibrated silhouette threshold or registered slip ceiling was supplied.',
'Oracle head NCC flags frames 0 and 1; oracle curves use NCC head tracking and stationary-x stance while gait_intent uses mask-top and ground-only stance. Both distinct frozen payloads are retained.',
'Committed band and dope sheet begin DOWN and have identical schedules; this differs from the CONTACT-origin premise in the task. W2 rotation zero and all cyclic phase rotations are explicit.'
]
checks.append(result('measurement_concerns','walk/E',concerns,notes='Limitations, not gate verdicts.'))
Path('out/checks.json').write_text(json.dumps(checks,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(envelopes=len(checks),intent_summary={k:v for k,v in intent_data['summary'].items() if k in ('W1','W2','W3a','W3c','W4','W5','W6','W6_per_arm','valid_frames_per_arm')},best_rotations=best,rotation_scores=[{k:r[k] for k in ('rotation_left','schedule_matches','extrema_sets_matching')} for r in rotations],seams=[r for r in checks if r['id'] in ('g6_seam','g6b','g6c')],sole_rows=sole_rows,planted_rows=planted_rows),allow_nan=False))
PY

Reading the results:
checks.json is a list of SPEC section 1 envelopes. gait_intent_full holds each complete original gate payload, with each component also available as a separate envelope. gait_landmarks_full contains the exact stance-lineage landmarks and curves used by gait_intent. walk_E_K3p_measure.json is the independent frozen oracle pipeline payload.

The two head estimators differ: gait mask-top W1 = 0.02079002079002079 H; oracle NCC W1 = 0.04158004158004158 H. Oracle NCC flags frames 0 and 1. They are not interchangeable.

W2 uses the dope-sheet phases in file/frame order, and the committed row as the expected schedule. Both begin DOWN and are identical, contrary to the task's CONTACT-origin prose. The diagnostic search rotates phase labels only, leaving measured frames fixed. Best schedule-match rotations are 0 and 6 (12/12 labels); neither matches the required extrema sets. All 12 rotations and unchanged frozen W2 booleans are retained. This is a diagnostic, never replacement of the rotation-zero gate.

W5 L=0.014553014553014554 H; R=0.04365904365904366 H. Both possible free/weapon mappings were evaluated. Staff ownership and anatomical near/far cannot be established by the emitted silhouette extents. W6 R has 5 opposed frames out of 12; L and pooled W6 are null due to missing L foot samples at 2,3,4,8,9. A committed row does not supply missing observations.

G6 seam MAD = 0.8322703043619791; minimum internal = 1.0076243082682292; median internal = 1.2447649637858074. G6c seam/homologue ratio = 0.8098339561010615. Frozen booleans are retained.

G11 contains all 11 internal pairs and the closure pair after exact 48px LANCZOS RGBA reduction and the frozen dark-background comparator. Its threshold and booleans remain null because the cast05 reference required by drift48 was not supplied. No rest/cast substitution was made.

G1 is measured against the named E rest frame at the frozen 3% height tolerance. Silhouette distances are numeric but their verdicts are null without a calibrated threshold.

Sole-line y values: 399,396,396,396,396,395,397,399,399,399,399,399. Spread = 4px. Clip-wide estimated ground is 399px in every frame by definition; its own spread is 0px. Gait stance requires proximity within 2px of that clip-wide ground. Consequently frames 1 through 5 have no detected planted foot; missing contacts are not filled in.

Planted-foot table preserves all x coordinates and nulls. Ground-only planted scroll includes R transitions 6->7=0, 7->8=-17, 8->9=-17px and L transitions 10->11=-19, 11->0=-6px. Slip metrics are descriptive because no committed slip ceiling exists. Oracle stationary-x stance is retained separately in the oracle payload.

The generated PNG files are frozen-tool diagnostic plots, not generated artwork. No image generation calls were made.
