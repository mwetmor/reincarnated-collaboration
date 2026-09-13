K3p-chk-walk-xv — CHECK measurements
All frame numbers are zero-based. No aggregate verdict is declared.

Frozen tools and named inputs were read only. Python -B and PYTHONDONTWRITEBYTECODE=1 suppressed bytecode writes. No image generation, input transforms, frozen-source edits, or new source files. Inline Python below invokes frozen tools and serializes/aggregates their results.

Invocation deviation:
The requested oracle.walk_bands CLI --ours branch ignores --out and unconditionally writes OURS_ROOT/<label>_ours.json into the repository. It was NOT executed. Its frozen curves, bands, _plots, and _write functions were called directly with fps=12, k_vert=1.25, k_lat=0.5. Results are in the requested out/walk_E_K3p_measure.json. The normal oracle curve plot uses its provisional self-derived bands exactly as the CLI would; the additional committed_W1 plot uses the committed row for W1 shading. Frozen plot captions still say provisional. Numeric committed gates use plate13_lateral_ann unchanged except for the two expressly requested in-memory arm_roles assignments.

Requested CLI (NOT RUN because it violates output isolation):
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B -m oracle.walk_bands --ours /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-xv-cut-03/frames/walk/E --fps 12 --label walk_E_K3p --k_vert 1.25 --out out/walk_E_K3p_measure.json --plot_dir out/plots

Measurements:
- W1 silhouette-top gait instrument: 0.0205761316872428 H; floor 0.03945870747438978 (false), ceiling 0.07 (true).
- W2: all 12 phase rotations have passed=false. The committed JSON starts DOWN and matches the dope sheet at rotation 0, contrary to the CONTACT-first wording. Rotations 0 and 6 tie at 12/12 schedule positions; deterministic best rotation is 0. Observed minima: 0,6 (DOWN); maxima: 3 (UP),4 (CONTACT). Expected minimum phase set is UP/DOWN; expected maximum set is UP. No frames or pixels were rotated. The full sweep and exact phase-index mapping are recorded.
- W3a: 0.7693097064055217 versus ceiling 0.35 (false). W3c: 4, floor 2 (true), ceiling 3 (false). W4: 2 (true).
- W5 L=0.037037037037037035 H, R=0.06172839506172839 H. Each meets the weapon floor 0.03; neither meets the free-arm floor 0.08; each is below free-arm ceiling 0.20. Both assignments have full frozen payloads.
- W6: null for both assignments; L has only 10 valid samples and R has 9. Frozen instrument emits neither fraction nor opposed-frame count without all 12 samples. Missing L frames 2,4; missing R frames 8,9,10. A committed threshold does not make missing measurements boolean.
- Staff-arm anatomical near/far identity is not exposed by the frozen landmarks. No screen track was selected as anatomical staff arm.
- G6 seam MAD=1.2459119160970051 vs minimum internal=0.99969482421875 (false). G6b vs median internal=1.2065455118815105 (false). G6c seam/homologue=1.2462922543093797 vs 1.25 (true). G6c does not replace either other instrument.
- G11: all 12 48px adjacent/seam MADs recorded; seam=0.8071469907407407. Its frozen gate needs cast05, which was not supplied, so its comparison threshold and verdict remain null. No rest-frame substitute was made.
- G1: all 12 frozen passed flags are true versus the supplied E rest; maximum relative height difference=0.028340080971659964.
- Silhouette distances computed for every frame; no calibrated threshold supplied, so verdicts remain null.
- Per-frame sole lines: [399,401,402,402,402,402,401,400,398,398,398,397]; spread=5 px. The tracker ground line is 402 for all frames, spread=0 by construction. These silhouette-bottom proxies can include staff support and are not semantic shoe annotations or atlas root anchors.
- Gait planted x: L only frame 3=267; R frames 1=290,2=277,4=251,5=234.5,6=218,7=206. All other planted entries are null. R mean planted scroll=-14.5 px/frame, RMS slip=2.03100960115899. L has no consecutive planted observations, so scroll/slip are null; no committed slip ceiling exists.
- Inferred contact events at frames 1 and 4 both use R. Frozen phase inference requires alternating track identities and remains null. Merged/hidden feet prevent a firm semantic repeated-lead conclusion.
- The separate oracle uses NCC head tracking and stationary-x stance; its W1=0.03292181069958848 and head-track flags at frames 0..6 must not be confused with the gait instrument. All original outputs are retained.
- Mask check visually inspected. Frozen plots use one-based display captions; JSON tables use zero-based frame indices.

File structure:
checks.json is a list of SPEC section 1 envelopes, including complete original gait payloads, both arm assignments, every cyclic phase result, G6 variants, G11 pairs, G1, silhouette distances, sole/ground lines, and planted-foot records. Descriptive payload envelopes have null verdicts with reasons. instrument_payloads.json preserves the committed row, dope sheet, input hashes, original gait results, and landmarks. No filled-in missing observations.

Exact executed measurement and aggregation commands (run from the burst workdir):

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B - <<'PY'
import json, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
from oracle.walk_curves import curves, measure_sequence
from oracle.walk_bands import bands, _plots, _write
from oracle.walk_landmarks import figure_mask, track_landmarks_otsu_stance_lineage
from oracle.motion_map import frame_paths
from gates import gait_intent
root=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
frames=root/'runs/C-1/artifacts/K3p-xv-cut-03/frames/walk/E'
rest=root/'runs/C-1/artifacts/K3p-xv-cut-03/frames/rest/E/rest_E.png'
out=Path('out'); out.mkdir(exist_ok=True)
paths=frame_paths(frames)
row=json.loads((root/'oracle/bands_walk.json').read_text())['plate13_lateral_ann']
phases=json.loads((root/'runs/C-1/oracle/dope_walk_12.json').read_text())['frames']
inputs=[*paths,rest,root/'oracle/bands_walk.json',root/'runs/C-1/oracle/dope_walk_12.json']
provenance=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in inputs]
data=curves(frames,pattern='*.png',fps=12,lateral=True,ours=True)
b=bands(data['summary'],k_vert=1.25,k_lat=.5)
evidence=_plots(out/'plots','walk_E_K3p',paths,data,b)
for r in data['results']: r['evidence']=evidence
data['provenance']=dict(source=str(frames),source_note='own registered sprites',frame_names=data['frame_names'],frames=12,fps=12,pattern='*.png',mask_params=data['mask_params'],k_vert=1.25,k_lat=.5,label='walk_E_K3p',invocation='frozen curves/bands/_plots/_write APIs; CLI --ours ignores --out and was not executed')
_write(out/'walk_E_K3p_measure.json',data)
seq=track_landmarks_otsu_stance_lineage([figure_mask(np.array(Image.open(p).convert('RGBA'))) for p in paths])
intent=measure_sequence(seq)
assignments=[{'L':'weapon_arm','R':'free_arm'},{'L':'free_arm','R':'weapon_arm'}]
gaits=[]
for roles in assignments:
    assigned=dict(row,arm_roles=roles)
    gaits.append(dict(arm_roles=roles,rotation=0,results=gait_intent.evaluate(frames,assigned,phases)))
rotations=[]
expected=[p['phase'] for p in row['phase_table']]
for k in range(12):
    rotated=phases[k:]+phases[:k]
    payload=gaits[0]['results'] if k==0 else gait_intent.evaluate(frames,dict(row,arm_roles=assignments[0]),rotated)
    w2=next(r for r in payload if r['id']=='W2')
    note=json.loads(w2['notes'])
    rotations.append(dict(left_rotation=k,candidate_source_indices=list(range(k,12))+list(range(k)),schedule_matching_positions=sum(p['phase']==e for p,e in zip(rotated,expected)),extrema_phase_sets_matching=sum({p['phase'] for p in note['observed_extrema'][side]}=={p['phase'] for p in note['expected_extrema'][side]} for side in ('min','max')),result=w2))
best=max(rotations,key=lambda r:(r['result']['passed'] is True,r['schedule_matching_positions'],r['extrema_phase_sets_matching'],-r['left_rotation']))
_write(out/'instrument_payloads.json',dict(input_sha256=provenance,committed_row=row,dope_phases=phases,gait_intent=gaits,gait_landmarks=seq,gait_measurement=intent,w2_rotations=rotations,best_rotation=best,best_rotation_selection='lexicographic: literal W2 true, schedule matching positions, matching extrema phase sets, smallest left rotation; frame pixels/order unchanged'))
print(json.dumps(dict(gait_summary=intent['summary'],gait_results=gaits,w2_rotation_summary=[{k:r[k] for k in ('left_rotation','schedule_matching_positions','extrema_phase_sets_matching')} for r in rotations],best_rotation=best,oracle_summary=data['summary'],landmark_first=seq[0]),allow_nan=False))
PY

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B - <<'PY'
import json, hashlib
from pathlib import Path
from PIL import Image
from gates.common import result, rgba, pair_differences
from gates import g6_seam, drift48, g1_height, silhouette64
from oracle.motion_map import frame_paths
from oracle.walk_bands import _write
out=Path('out'); payload=json.loads((out/'instrument_payloads.json').read_text())
root=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
frames=root/'runs/C-1/artifacts/K3p-xv-cut-03/frames/walk/E'; rest=root/'runs/C-1/artifacts/K3p-xv-cut-03/frames/rest/E/rest_E.png'
paths=frame_paths(frames); seq=payload['gait_landmarks']; summary=payload['gait_measurement']['summary']
checks=[]
for bundle in payload['gait_intent']:
    label='walk/E/rotation_0/'+('L_weapon_R_free' if bundle['arm_roles']['L']=='weapon_arm' else 'L_free_R_weapon')
    checks.append(result('gait_intent_full_payload',label,value=bundle,unit='payload',notes='Full unmodified frozen evaluate output; no aggregate verdict.'))
    for r in bundle['results']:
        checks.append(dict(r,subject=label,notes=json.dumps(dict(json.loads(r['notes']),arm_roles=bundle['arm_roles']),sort_keys=True)))
checks.append(result('W2_cyclic_phase_search','walk/E',value=payload['w2_rotations'],unit='phase_rotation_table',notes=payload['best_rotation_selection']+'; left rotation k assigns original phase[(i+k)%12] to unchanged frame i. The committed file already starts DOWN, exactly as the dope sheet; no CONTACT-first schedule was substituted.'))
checks.append(dict(payload['best_rotation']['result'],id='W2_best_cyclic_rotation',subject='walk/E/left_rotation_'+str(payload['best_rotation']['left_rotation'])))
checks.append(result('W2_rotation_ties','walk/E',value=[r['left_rotation'] for r in payload['w2_rotations'] if (r['result']['passed'],r['schedule_matching_positions'],r['extrema_phase_sets_matching'])==(payload['best_rotation']['result']['passed'],payload['best_rotation']['schedule_matching_positions'],payload['best_rotation']['extrema_phase_sets_matching'])],unit='rotation_indices',notes='All rotations retained above; frozen literal W2 remains distinct from schedule-only matching.'))
checks.extend(g6_seam.evaluate(paths,'walk/E')); checks.append(g6_seam.g6c(paths,'walk/E',animation='walk'))
checks.append(drift48.evaluate(paths,subject='walk/E'))
small=[rgba(p).resize((48,48),Image.Resampling.LANCZOS) for p in paths]
pairs=pair_differences(small)
for i,pair in enumerate(pairs):
    checks.append(result('G11_pair',f'walk/E/{i:02d}->{(i+1)%12:02d}',value=pair['canvas'],unit='rgb_mad',notes=json.dumps(dict(pair=pair,from_frame=i,to_frame=(i+1)%12,seam=i==11,method='exact drift48 preprocessing: 48x48 LANCZOS RGBA then common.pair_differences dark composite',reason='No cast05 input supplied; frozen G11 comparison threshold unavailable; per-pair metrics only.'))))
for i,p in enumerate(paths):
    checks.append(g1_height.evaluate(p,rest,f'walk/E/{i:02d} versus rest/E'))
    checks.append(silhouette64.evaluate(p,rest,f'walk/E/{i:02d} versus rest/E'))
sole=[d['sole_line_y'] for d in seq]; ground=[d['ground_line_y'] for d in seq]
checks.append(result('sole_lines','walk/E',value=sole,unit='source_pixel_y',notes='Frozen silhouette bottom (inclusive alpha row), not semantic shoe annotation. Frame order 00..11; from gait-intent ground-proximity lineage.'))
checks.append(result('sole_line_spread','walk/E',value=max(sole)-min(sole),unit='px',notes='max(per-frame sole_line_y)-min(per-frame sole_line_y); no committed spread threshold supplied.'))
checks.append(result('ground_lines','walk/E',value=ground,unit='source_pixel_y',notes='Frozen tracker sets every ground_line_y to clip-wide maximum sole y; a constant line is an estimator definition, not evidence of zero sole motion.'))
checks.append(result('ground_line_spread','walk/E',value=max(ground)-min(ground),unit='px',notes='max(ground_line_y)-min(ground_line_y); constant by frozen tracker construction. See sole_line_spread.'))
planted=[]
for i,d in enumerate(seq):
    planted.append(dict(frame=i,phase=payload['dope_phases'][i]['phase'],sole_line_y=d['sole_line_y'],ground_line_y=d['ground_line_y'],torso_cx=d['torso_cx'],foot_L_x=d['foot_L_x'],foot_L_y=d['foot_L_y'],foot_R_x=d['foot_R_x'],foot_R_y=d['foot_R_y'],planted_L=d['planted_L'],planted_R=d['planted_R'],planted_L_x=summary['sole_scroll']['planted_scroll_lineage']['L']['planted_x_px'][i],planted_R_x=summary['sole_scroll']['planted_scroll_lineage']['R']['planted_x_px'][i],identity_ambiguous=d['identity_ambiguous']))
checks.append(result('planted_foot_table','walk/E',value=planted,unit='source_pixels',notes='Ground proximity selector used by gait_intent, not oracle stationary-x selector. Null hidden/merged feet preserved. Screen tracks do not establish anatomy.'))
checks.append(result('planted_scroll_full_payload','walk/E',value=summary['sole_scroll']['planted_scroll_lineage'],unit='payload',notes='Frozen sole_scroll_planted_lineage, including seam if both endpoints planted; no registered slip ceiling.'))
checks.append(result('inferred_contact_events','walk/E',value=payload['gait_measurement']['phase_table'],unit='phase_table',notes='Events at frames 1 and 4 both belong to R; tool requires two different lead tracks, so inferred phases are null. This screen-track proxy cannot resolve a semantic repeated lead through missing feet.'))
checks.append(result('W6_opposed_frames','walk/E/both_arm_assignments',value={side:dict(opposed_fraction=summary['W6_per_arm'][side],opposed_frames=None,valid_frames=summary['valid_frames_per_arm'][side],missing_frames=[i for i,d in enumerate(seq) if d.get('foot_'+side+'_x') is None or d.get('wrist_ext_'+side) is None]) for side in ('L','R')},unit='frame_counts',notes='Frozen arm_swing requires all 12 samples before emitting opposition. L has 10, R has 9; fractions and opposed-frame counts remain null under both role assignments.'))
checks.append(result('far_staff_arm_track','walk/E',notes='UNEVALUABLE: frozen silhouette extent landmarks do not expose anatomical near/far or staff identity; both L/R role assignments reported without selecting anatomy.'))
checks.append(result('gait_landmarks_full_payload','walk/E',value=seq,unit='payload',notes='Frozen ground-proximity tracker landmarks; no repaired or invented observations.'))
checks.append(result('gait_measurement_full_payload','walk/E',value=payload['gait_measurement'],unit='payload',notes='Frozen measure_sequence called on the exact gait_intent landmark lineage. Oracle NCC/stationary-x output is separately in walk_E_K3p_measure.json.'))
checks.append(result('input_provenance','walk/E',value=payload['input_sha256'],unit='sha256',notes='Named read-only inputs, including committed row container and dope sheet.'))
concerns=['Exact oracle CLI not executed: --ours ignores --out and writes outside out/. Equivalent frozen measurement/plot functions used directly with requested fps and multipliers.', 'W6 fractions, opposed-frame counts, and booleans cannot be computed: missing L feet in frames 2,4 and R feet in frames 8,9,10; frozen instrument requires all 12 samples. No false booleans substituted for null.', 'Far staff arm screen track cannot be established by the frozen landmarks; both hypothetical role assignments retained.', 'G11 gate verdict and threshold unavailable without a supplied cast05 reference; all 12 adjacent/seam MADs computed with frozen preprocessing/comparator.', 'L planted-sole slip and mean scroll unavailable: no consecutive planted observations; neither arm has a committed slip threshold. Semantic foot contact and repeated-lead identity remain uncertain through merges.', 'Silhouette distances computed; verdicts null because no calibrated silhouette threshold was supplied.', 'Oracle NCC head tracker flags frames 0 through 6; its W1=0.03292181069958848 differs from gait silhouette-top W1=0.0205761316872428. Both frozen lineages retained.', 'Committed phase_table already starts DOWN and equals dope phases, contrary to CONTACT-first wording. Literal W2 is false for every phase rotation; best schedule matches at 0 and 6, smallest rotation 0 retained.']
checks.append(result('instrument_concerns','walk/E',value=concerns,unit='text_list',notes='Measurement limitations and invocation deviation; no aggregate gate verdict.'))
_write(out/'checks.json',checks)
print(json.dumps(dict(result_envelopes=len(checks),seams=[r for r in checks if r['id'] in ('g6_seam','g6b','g6c')],G11_pairs=pairs,sole_lines=sole,sole_spread=max(sole)-min(sole),ground_spread=max(ground)-min(ground),G1=[dict(value=r['value'],passed=r['passed']) for r in checks if r['id']=='g1_height'],silhouette_distances=[r['value'] for r in checks if r['id']=='silhouette64']),allow_nan=False))
PY

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B - <<'PY'
import json
from pathlib import Path
from oracle.walk_bands import _curve_plot
out=Path('out')
payload=json.loads((out/'instrument_payloads.json').read_text())
data=json.loads((out/'walk_E_K3p_measure.json').read_text())
print(_curve_plot(out/'plots','walk_E_K3p_committed_W1',data,payload['committed_row']['bands']))
PY

