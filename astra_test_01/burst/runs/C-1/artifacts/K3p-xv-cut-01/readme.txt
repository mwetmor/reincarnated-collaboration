K3p-xv-cut-01 — measurement report

Stopped at task step 3: the frozen tracker found zero observed CONTACT onsets
and no same-side contact pair in the permitted segment. L is already planted
at native frames 0-3; its onset precedes the observation boundary or is unknown.
Even treating native frame 0 as a boundary contact supplies only one observation.
No stride period, stride selection, phase resampling, registration transform,
registered walk/rest PNGs, alpha_box or numbered strip could be computed.

Extracted 104 frames, native indices 0-103, at 24 fps, t=0..4.291667 seconds.
Actual input dimensions: 768x1168 (the brief says 720p).
All 104 frames were matted in memory with frozen matte.extract(alpha_floor=40).
Plate border survival minimum: 0.9966425619834711. No below-threshold frames.
The tolerance and 10-pixel border sampling exactly match the frozen matte.
Native PNGs retain the original green plate. Matted masks were measured in memory;
full tracker output, native geometry and per-frame matte diagnostics are recorded.

Contact instrument: oracle.walk_landmarks.track_landmarks, with events from
oracle.walk_curves.phase_table. The stationary-sole requirement is abs(dx)<=2
native pixels per frame and ground proximity <=3 pixels. Clip-wide ground is
row 1123. L/R mean screen-space tracked sides, not anatomical labels. Foot
identity is ambiguous in 26 of 104 frames. Thresholds were not changed.

Largest consecutive silhouette jump in the allowed segment: native 93 -> 94,
t=3.916667 s, 1-IoU=0.24321879853169562, XOR area=55127 pixels.
This is a descriptive measurement, not evidence of a splice. The ~4.5 s
splice is outside the authorized window and its magnitude was not measured.

The committed phase table starts on DOWN; its first CONTACT is oracle frame 4
(printed phase 5). Its original table is preserved in registration.json. A
contact-first rotation would start there, but no phase mapping was performed.
Seed geometry and named input/frozen-module hashes are recorded for provenance.

No image-generation calls, retries, per-frame rescaling or recentering.
No gate verdicts. Outputs were written only under out/. Python bytecode writes
were disabled for imports of frozen modules.

Exact processing commands follow (run from the burst workdir).
The read-only source inspection commands are not needed to reproduce outputs.
The readme itself was written as documentation using apply_patch.

COMMAND 1
mkdir -p out/native
/opt/homebrew/bin/ffmpeg -hide_banner -nostdin -i /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/xvideo/in/walk_E_grok.mp4 -map 0:v:0 -vf "select='lte(t,4.3)',showinfo" -fps_mode passthrough -start_number 0 out/native/native_%03d.png > out/ffmpeg_extract.log 2>&1

COMMAND 2
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys,json,re,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates.matte import extract
from oracle.walk_landmarks import track_landmarks
from oracle.walk_curves import phase_table
root=Path('out')
paths=sorted((root/'native').glob('*.png'))
log=(root/'ffmpeg_extract.log').read_text()
times=[float(t) for t in re.findall(r'n:\s*\d+\s+pts:\s*\d+\s+pts_time:([\d.]+)',log)]
assert len(paths)==len(times) and max(times)<=4.3,(len(paths),len(times))
masks=[]; plates=[]; errors=[]
for i,p in enumerate(paths):
 with Image.open(p) as im:
  rgb=np.array(im.convert('RGB'))
  border=np.concatenate([rgb[:10].reshape(-1,3),rgb[-10:].reshape(-1,3),rgb[:,:10].reshape(-1,3),rgb[:,-10:].reshape(-1,3)])
  survival=float(np.mean((border[:,1]>210)&(border[:,0]<45)&(border[:,2]<45)))
  info={'native_index':i,'time_s':times[i],'border_survival':survival,'below_frozen_minimum':survival<.95}
  try:
   mat,diag=extract(im,alpha_floor=40)
   masks.append(np.asarray(mat)[...,3]>=128)
   info['matte']=diag
  except ValueError as e:
   errors.append({'native_index':i,'error':str(e)}); masks.append(None)
  plates.append(info)
seq=track_landmarks(masks) if not errors else []
phases=phase_table(seq) if seq else []
contacts=[]
for p in phases:
 if p['contact']:
  i=p['frame']
  for s in p['contact_sides']:
   if i==0:
    continue
   d=seq[i]; duration=0
   for j in range(i,len(seq)):
    if seq[j]['planted_'+s] is not True: break
    duration+=1
   contacts.append({'native_index':i,'time_s':times[i],'side':s,'identity_ambiguous':d['identity_ambiguous'],'planted_run_frames':duration,'velocity_x':d['foot_'+s+'_velocity_x'],'sole_y':d['foot_'+s+'_y'],'ground_gap_px':abs(d['foot_'+s+'_y']-d['ground_line_y'])})
periods=[]
for s in ('L','R'):
 cs=[c for c in contacts if c['side']==s]
 for a,b in zip(cs,cs[1:]):
  periods.append({'side':s,'start':a['native_index'],'end':b['native_index'],'period_frames':b['native_index']-a['native_index'],'period_s':times[b['native_index']]-times[a['native_index']]})
jumps=[]
if not errors:
 for i in range(1,len(masks)):
  a,b=masks[i-1:i+1]; xor=int(np.count_nonzero(a^b)); union=int(np.count_nonzero(a|b))
  jumps.append({'from_native_index':i-1,'to_native_index':i,'time_s':times[i],'xor_pixels':xor,'silhouette_jump_1_minus_IoU':xor/union})
d={'task_id':'K3p-xv-cut-01','native_frames':len(paths),'native_dimensions':list(Image.open(paths[0]).size),'fps':24,'times_s':times,'plate_tolerance':{'border_width_px':10,'predicate':'G > 210 and R < 45 and B < 45; same concatenated borders as frozen matte.extract','minimum_survival':.95},'plate_survival_per_frame':plates,'matte_errors':errors,'landmarks_native':seq,'frozen_contact_phase_table':phases,'contact_table':contacts,'same_side_contact_periods':periods,'boundary_contacts':[p for p in phases if p['boundary_contact']],'splice_check':{'scope':'Only retained t <= 4.3 s; the known ~4.5 s splice is excluded and not measured','metric':'1 - IoU of consecutive unregistered alpha >=128 silhouettes','largest':max(jumps,key=lambda x:x['silhouette_jump_1_minus_IoU']) if jumps else None,'all_pairs':jumps},'selected_stride':None,'registered_frames':[]}
(root/'registration.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({'native_frames':len(paths),'last_time_s':times[-1],'plate_min':min(p['border_survival'] for p in plates),'matte_errors':errors,'contact_table':contacts,'periods':periods,'ambiguous_frames':sum(x['identity_ambiguous'] for x in seq),'largest_jump':d['splice_check']['largest']},indent=2))
PY

COMMAND 3
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json,hashlib
from pathlib import Path
root=Path('out'); p=root/'registration.json'; d=json.loads(p.read_text())
base=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
inputs={'clip':base/'runs/C-1/xvideo/in/walk_E_grok.mp4','seed_geometry':base/'runs/C-1/artifacts/K3p-seed/registration_transform.json','walk_band':base/'oracle/bands_walk.json'}
d['inputs']={k:{'path':str(v),'sha256':hashlib.sha256(v.read_bytes()).hexdigest()} for k,v in inputs.items()}
d['seed_geometry']=json.loads(inputs['seed_geometry'].read_text())
d['target_phase_table_original']=json.loads(inputs['walk_band'].read_text())['plate13_lateral_ann']['phase_table']
d['target_phase_rotation_if_stride_existed']=4
d['target_phase_rotation_note']='Original first CONTACT is oracle frame 4 (printed phase 5); no resampling performed.'
d['frozen_modules']={str(base/k):hashlib.sha256((base/k).read_bytes()).hexdigest() for k in ['gates/matte.py','gates/common.py','oracle/walk_landmarks.py','oracle/walk_curves.py','oracle/motion_map.py']}
seq=d['landmarks_native']
d['contact_diagnostics']={'tracker':'oracle.walk_landmarks.track_landmarks','event_instrument':'oracle.walk_curves.phase_table; CONTACT requires explicit False to True stance transition','linear_boundary_policy':'Frame 0 cyclic contacts excluded from interior events and separately reported; no clip-end wrap accepted as a measured onset','ground_line_y':seq[0]['ground_line_y'],'identity_ambiguous_native_indices':[i for i,x in enumerate(seq) if x['identity_ambiguous']],'planted_native_indices':{s:[i for i,x in enumerate(seq) if x['planted_'+s] is True] for s in ('L','R')},'ground_only_lineage_indices':{s:[i for i,x in enumerate(seq) if x['planted_ground_only_lineage'][s] is True] for s in ('L','R')},'thresholds_native_px':{'stationary_sole_abs_dx_max':2,'ground_proximity_max':3}}
d['stop_reason']='No CONTACT onsets detected in 104 native frames covering 0 through 4.291667 s. Fewer than two same-side contacts exist; stopped after reporting as instructed.'
d['scale']=None; d['translation_xy']=None; d['native_indices_used']=[]; d['rest_frame']=None
d['uncomputed']=['Stride period: no same-side contact pair.','Cleanest stride and 12 native phase samples: no eligible contact pair.','Uniform scale, translation, registered walk/rest frames and strip: withheld under explicit step 3 stop condition.','Registered per-frame bbox heights, sole lines, offsets and alpha_box: no registered frames.','Actual ~4.5 s splice magnitude: outside authorized t <= 4.3 s window; largest jump within retained segment is reported.']
d['concerns']=['Frozen tracker found zero CONTACT onsets; no stride or registered image outputs produced.','Track identity is ambiguous in 26 of 104 frames; L/R are screen-space tracks, not anatomical identities.','Actual clip dimensions are 768x1168, differing from the stated 720p.']
d['native_frame_geometry']=[{'native_index':i,'time_s':d['times_s'][i],'bbox_height':x['H'],'sole_line':x['sole_line_y'],'offsets':None} for i,x in enumerate(seq)]
p.write_text(json.dumps(d,indent=2)+'\n')
assert d['native_frames']==104 and not d['contact_table'] and not d['same_side_contact_periods']
assert all(x['border_survival']>=.95 for x in d['plate_survival_per_frame'])
print(json.dumps({'stop_reason':d['stop_reason'],'contact_diagnostics':d['contact_diagnostics'],'uncomputed':d['uncomputed']},indent=2))
PY

COMMAND 4
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json
from pathlib import Path
p=Path('out/registration.json'); d=json.loads(p.read_text())
d['initial_boundary_stance']={'native_index':0,'time_s':0.0,'planted_tracks':['L'],'observed_onset':False,'note':'L is already planted in native frames 0-3. This is a left-censored initial stance, not an observed False-to-True CONTACT onset. Even counting it as a boundary contact gives only one same-side observation.'}
p.write_text(json.dumps(d,indent=2)+'\n')
PY


