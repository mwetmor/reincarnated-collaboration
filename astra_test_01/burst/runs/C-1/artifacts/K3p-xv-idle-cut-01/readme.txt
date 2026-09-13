K3p-xv-idle-cut-01 — measurement and registration

104 native frames retained: indices 0–103, timestamps 0–4.291667 s. Source is 768x1168 at 24 fps. No frame at or beyond the reported ~4.5 s splice was included.
Frozen matte extract(alpha_floor=40) completed for every retained frame. Minimum 10px-border green fraction: 0.99974173553719. Per-frame plate-survival counts and matte metadata are in registration.json and native_measurements.json.

Breath instrument: oracle.idle_curves.curves(matted_dir, native_union_alpha_box, 24, ours=True), without modifying frozen modules. The frozen alpha_box helper requires 512x512 frames, so native alpha>=128 boxes were unioned directly under the same convention; the helper was used on the registered output.
Consecutive rest minima: native 1 and 99, 0.0416667 and 4.125 s. The only full breath spans 98 frame intervals = 4.083333 s. Rest minima are raw local minima in the bottom 5% of the observed range; the enclosed excursion must cover at least 90% of the observed range. These are segmentation choices, not shipping gates.
Chest-width peak-to-peak excursion: 0.7064818482 %H, H=1132 native pixels. Frozen p95–p05 excursion is separately recorded. Chest/head curves and full frozen output: native_curves.json.
The frozen period estimator returned null because at least two cycles are required. Supplemental periodogram dominant bin is 104 frames (4.333333 s); this clip-length bin does not resolve a repeated-cycle period. No same-size nonoverlapping native control box fits, so contamination is unavailable.

Resampling uses nearest native frames at phases j/16, j=0..15, excluding the second minimum to avoid endpoint duplication. Selected native indices: 1, 7, 13, 19, 26, 32, 38, 44, 50, 56, 62, 68, 75, 81, 87, 93. Native samples approximate equal phase to nearest frame; output timing is exactly 8 fps, 2.0 s. No frame blending or motion synthesis.
Final single uniform scale: 0.21178445229681978. Single integer translation: (178,158). All 16 frames are 512x512 RGBA. Frame zero measures height 240, sole row 399, bbox centre-x 255.5. Every frame retains sole row 399; heights range 237–240. Root anchor is fixed atlas metadata (256,400); actual bottom-alpha contact is separately recorded as a sole proxy, without independent anatomical annotation.
One diagnosed registration retry: nominal 240/1132 scaling produced odd bbox width and a +0.5px centre residual under integer translation. A nearby single uniform factor, selected by raster measurement, gives height 240 and even bbox width; it is used identically for every final frame. See registration_scale_search.json. No per-frame scaling or recentering and no upscaling.
Largest retained silhouette jump: native 85→86, XOR/union=0.005060394356209861 (1256/248202 pixels), at 3.583333 s. Only the permitted segment was inspected for this measurement; no claim is made about the excluded splice.

Artifacts: registration.json; checks.json; native_curves.json; native_measurements.json; registration_scale_search.json; extraction.log; native/*.png; frames/idle/S/*.png; sheets/idle_S_strip.png. Intermediate matte PNGs were deleted after measurement/registration, with their hashes retained in registration.json. No image generation, external writes, or gate verdicts.

Exact processing commands follow in execution order. Run from a clean burst workdir with empty output image directories. Inspection-only commands are not repeated. Python bytecode writes were disabled for every frozen-module processing invocation. These inline commands are provenance, not new tool files.

COMMAND 1
mkdir -p out/native out/matted out/frames/idle/S out/sheets
/opt/homebrew/bin/ffmpeg -hide_banner -nostdin -i /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/xvideo/in/idle_C_grok.mp4 -map 0:v:0 -vf "select='lte(t,4.3)',showinfo" -fps_mode passthrough -start_number 0 out/native/native_%03d.png 2> out/extraction.log

COMMAND 2
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys,json,re
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.signal import find_peaks
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates.matte import extract
from oracle.idle_curves import curves
root=Path('out')
records=[]; boxes=[]; jumps=[]; previous=None
log=(root/'extraction.log').read_text()
times={int(n):float(t) for n,t in re.findall(r' n:\s*(\d+).*?pts_time:([\d.]+)',log)}
for p in sorted((root/'native').glob('*.png')):
    i=int(p.stem.split('_')[-1]); im=Image.open(p); rgb=np.array(im.convert('RGB'))
    keyed=(rgb[:,:,1]>210)&(rgb[:,:,0]<45)&(rgb[:,:,2]<45)
    border=np.concatenate([keyed[:10].ravel(),keyed[-10:].ravel(),keyed[:,:10].ravel(),keyed[:,-10:].ravel()])
    rec={'native_index':i,'time_s':times[i],'plate_border_green_fraction':float(border.mean()),'plate_pixels':int(keyed.sum())}
    try:
        m,meta=extract(im,alpha_floor=40); m.save(root/'matted'/f'matted_{i:03d}.png')
        a=np.array(m); mask=a[:,:,3]>=128; y,x=np.where(mask)
        b=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]; boxes.append(b)
        rec.update({'matte_error':None,'matte':meta,'bbox':b,'bbox_height':b[3]-b[1],'sole_line':b[3]-1,'keyed_pixels_surviving_alpha_positive':int(np.count_nonzero(keyed & (a[:,:,3]>0))),'keyed_pixels_surviving_alpha_128':int(np.count_nonzero(keyed & mask))})
        if previous is not None:
            union=previous|mask; xor=previous^mask
            jumps.append({'from_native_index':i-1,'to_native_index':i,'time_s':times[i],'silhouette_xor_pixels':int(xor.sum()),'silhouette_union_pixels':int(union.sum()),'silhouette_jump_iou_distance':float(xor.sum()/union.sum())})
        previous=mask
    except ValueError as e:
        rec['matte_error']=str(e)
    records.append(rec)
(root/'native_measurements.json').write_text(json.dumps({'frames':records,'silhouette_jumps':jumps},indent=2)+'\n')
errors=[r for r in records if r['matte_error']]
print('frames',len(records),'matte_errors',errors,flush=True)
if errors: raise RuntimeError('Matte failures: cannot measure a continuous clip')
b=np.array(boxes); box=[int(b[:,0].min()),int(b[:,1].min()),int(b[:,2].max()),int(b[:,3].max())]
data=curves(root/'matted',box,24,ours=True)
(root/'native_curves.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
x=np.array(data['chest_dw_H']); mins,props=find_peaks(-x,prominence=.05*np.ptp(x))
print(json.dumps({'box':box,'summary':data['summary'],'ptp_percent_H':float(np.ptp(x)*100),'minima':mins.tolist(),'minima_prominences':props['prominences'].tolist(),'chest_width_H':x.tolist(),'head_search_limits':data['head_shift']['search_limit_frames'],'chest_search_limits':data['chest_edges']['search_limit_frames'],'largest_silhouette_jump':max(jumps,key=lambda j:j['silhouette_jump_iou_distance'])},indent=2),flush=True)
PY

COMMAND 3
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys,json,hashlib,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.signal import find_peaks,periodogram
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from oracle.motion_map import alpha_box
from gates.common import measure
root=Path('out'); data=json.loads((root/'native_curves.json').read_text()); native=json.loads((root/'native_measurements.json').read_text())
x=np.array(data['chest_dw_H']); raw,props=find_peaks(-x,prominence=0)
rest=[int(i) for i in raw if x[i]<=x.min()+.05*np.ptp(x)]
candidates=[(a,b) for a,b in zip(rest,rest[1:]) if np.max(x[a:b+1])-max(x[a],x[b])>=.9*np.ptp(x)]
if not candidates: raise RuntimeError('No minimum-to-minimum full breath found')
a,b=min(candidates,key=lambda ab: abs(float(x[ab[0]]-x[ab[1]])))
indices=np.floor(a+np.arange(16)*(b-a)/16+.5).astype(int).tolist()
first=Image.open(root/'matted'/f'matted_{a:03d}.png').convert('RGBA')
source_measure=measure(first); scale=240/source_measure['height']
if scale>1: raise RuntimeError('Requested scale would upscale')
scaled_size=tuple(math.ceil(v*scale) for v in first.size)
def scaled(im):
    return im.transform(scaled_size,Image.Transform.AFFINE,(1/scale,0,0,0,1/scale,0),resample=Image.Resampling.BICUBIC)
sm=measure(scaled(first)); sx=(sm['bbox'][0]+sm['bbox'][2]-1)/2; sy=sm['bbox'][3]-1
dx=round(255.5-sx); dy=399-sy
frames=[]
strip=Image.new('RGB',(512*16,544),'#3a3f4a'); draw=ImageDraw.Draw(strip)
for j,i in enumerate(indices):
    im=Image.open(root/'matted'/f'matted_{i:03d}.png').convert('RGBA'); small=scaled(im)
    frame=Image.new('RGBA',(512,512)); frame.alpha_composite(small,(dx,dy))
    path=root/'frames'/'idle'/'S'/f'idle_S_{j:02d}.png'; frame.save(path)
    m=measure(frame); nr=native['frames'][i]
    frames.append({'frame':j,'path':str(path),'native_index':i,'time_s':nr['time_s'],'output_time_s':j/8,'phase':j/16,'ideal_native_index':a+j*(b-a)/16,'native_bbox':nr['bbox'],'native_bbox_height':nr['bbox_height'],'native_sole_line':nr['sole_line'],'bbox':m['bbox'],'bbox_height':m['height'],'sole_line':m['bbox'][3]-1,'center_x':m['silhouette_center'][0],'root_anchor':[256,400],'sole_contact_bbox_bottom_x_range':[m['bbox'][0],m['bbox'][2]-1],'border_alpha_max':m['border_alpha_max'],'plate_survival':{k:v for k,v in nr.items() if k.startswith('plate_') or k.startswith('keyed_')},'matte_error':nr['matte_error']})
    strip.paste(frame,(j*512,0),frame)
    draw.text((j*512+12,518),f'{j:02d}  native {i:03d}  t={nr["time_s"]:.6f}s',fill='white')
strip.save(root/'sheets'/'idle_S_strip.png')
freq,power=periodogram(x,fs=24,detrend='constant',window='boxcar'); k=int(np.argmax(power[1:])+1)
seed_path=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-seed/registration_transform.json')
band_path=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/oracle/bands_idle.json'); band=json.loads(band_path.read_text())['relaxed']
concerns=['Frozen autocorrelation dominant period is unavailable: the retained clip contains only one full breath; the frozen instrument requires at least two cycles.','A same-size nonoverlapping control box does not fit the native canvas; frozen contamination measurement is unavailable.','The spectral dominant period is one clip-length bin (104 frames), not a resolved repeated-cycle estimate.','Input geometry is 768x1168 at 24 fps, rather than the brief description of 720p.']
if frames[0]['center_x']!=255.5: concerns.append(f'Integer translation leaves frame-0 center-x at {frames[0]["center_x"]}, a {frames[0]["center_x"]-255.5:+.1f} px residual from 255.5 due to raster parity.')
if frames[0]['bbox_height']!=240: concerns.append(f'Frame-0 raster height is {frames[0]["bbox_height"]} px after exact uniform factor 240/source_height.')
reg={'task_id':'K3p-xv-idle-cut-01','source':{'clip':'/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/xvideo/in/idle_C_grok.mp4','dimensions':[768,1168],'fps':24,'retained_frames':104,'retained_time_range_s':[native['frames'][0]['time_s'],native['frames'][-1]['time_s']],'selection_filter':'lte(t,4.3)','native_index_base':0},'seed_geometry':json.loads(seed_path.read_text()),'relaxed_band':{k:band[k] for k in ['breath_period_s','breath_amplitude_H','head_sway_H','committed','provisional']},'native_alpha_box':data['box'],'native_alpha_box_method':'Union of alpha>=128 boxes, identical convention to frozen alpha_box; native dimensions exceed its 512x512 input restriction.','registered_alpha_box':alpha_box(root/'frames'/'idle'/'S'),'breath':{'frozen_dominant_period_frames':data['summary']['breath_period_frames'],'frozen_dominant_period_s':data['summary']['breath_period_s'],'frozen_period_confidence':data['summary']['period_confidence'],'spectral_dominant_period_frames':float(24/freq[k]),'spectral_dominant_period_s':float(1/freq[k]),'spectral_method':'scipy.signal.periodogram, constant detrend, boxcar; largest non-DC bin; one-cycle finite-window diagnostic only','chest_width_peak_to_peak_percent_H':float(np.ptp(x)*100),'chest_width_p95_minus_p05_percent_H':data['summary']['breath_amplitude_H']*100,'head_peak_to_peak_percent_H':float(np.ptp(data['head_dy_H'])*100),'head_p95_minus_p05_percent_H':data['summary']['head_sway_H']*100,'normalization_H_native_px':data['height'],'all_raw_local_minima':raw.tolist(),'all_raw_minima_prominence_H':props['prominences'].tolist(),'rest_minima_native_indices':rest,'rest_minima_definition':'Raw local minima within the bottom 5% of the full chest-width range; ignores small fluctuations on expanded plateaus.','full_breath_candidates':[list(v) for v in candidates],'full_breath_definition':'Consecutive rest minima enclosing at least 90% of the measured chest-width range.','chosen_consecutive_minima_native_indices':[a,b],'chosen_minima_time_s':[native['frames'][a]['time_s'],native['frames'][b]['time_s']],'chosen_minima_chest_width_H':[float(x[a]),float(x[b])],'minimum_to_minimum_period_native_frames':b-a,'minimum_to_minimum_period_s':(b-a)/24,'selection_reason':'Only qualifying full breath; minimum-to-minimum with nearest rest-width endpoint match.','selected_peak_native_index':int(a+np.argmax(x[a:b+1])),'endpoint_excluded':True,'resampling':'Nearest native frame at equal target phases j/16, round-half-up; no blending, synthesis or endpoint duplication.','output_fps':8,'output_duration_s':2.0,'time_compression_source_duration_over_output':(b-a)/24/2,'curve_files':['out/native_curves.json','out/native_measurements.json']},'transform':{'scale':scale,'source_frame_zero_native_index':a,'source_frame_zero_bbox_height':source_measure['height'],'scaled_canvas_size':list(scaled_size),'resampling':'PIL affine bicubic, inverse diagonal 1/scale on both axes; scale about origin','integer_translation_xy':[dx,dy],'canvas':[512,512],'pivot':[256,400],'target_sole_row':399,'target_center_x':255.5,'frame_zero_measured_height':frames[0]['bbox_height'],'frame_zero_measured_sole_line':frames[0]['sole_line'],'frame_zero_measured_center_x':frames[0]['center_x'],'one_scale_and_translation_for_all_frames':True,'upscaling':False,'sole_line_definition':'Bottommost row of alpha>=128 figure support (includes held equipment); no independent anatomical annotation.','root_anchor_note':'Atlas pivot is fixed metadata, not independently inferred anatomy.'},'plate_survival':{'definition':'Border plate survival = fraction satisfying G>210,R<45,B<45 in 10px border; also counts those keyed pixels retaining alpha>0 and alpha>=128 after frozen matte.','alpha_floor':40,'minimum_border_green_fraction':min(r['plate_border_green_fraction'] for r in native['frames']),'matte_failures':[r for r in native['frames'] if r['matte_error']],'per_native_frame':native['frames']},'splice_check':{'metric':'XOR silhouette area divided by union silhouette area, alpha>=128, consecutive native frames','largest_silhouette_jump':max(native['silhouette_jumps'],key=lambda j:j['silhouette_jump_iou_distance']),'largest_absolute_xor_jump':max(native['silhouette_jumps'],key=lambda j:j['silhouette_xor_pixels']),'scope':'Only retained 0–4.3s segment; the reported ~4.5s splice is excluded and is not measured.','all_pairs':native['silhouette_jumps']},'frames':frames,'concerns':concerns}
(root/'registration.json').write_text(json.dumps(reg,indent=2,allow_nan=False)+'\n')
print(json.dumps({'minima':[a,b],'rest':rest,'period_frames':b-a,'amplitude_percent_H':np.ptp(x)*100,'transform':reg['transform'],'indices':indices,'concerns':concerns},indent=2),flush=True)
PY

COMMAND 4
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json,math
from pathlib import Path
import numpy as np
from PIL import Image
r=json.loads(Path('out/registration.json').read_text()); s=r['transform']['scale']; im=Image.open('out/matted/matted_001.png').convert('RGBA')
found=[]
for factor in sorted(np.linspace((240-1)/1132,(240+1)/1132,401),key=lambda v:abs(v-s)):
    small=im.transform(tuple(math.ceil(v*factor) for v in im.size),Image.Transform.AFFINE,(1/factor,0,0,0,1/factor,0),resample=Image.Resampling.BICUBIC)
    y,x=np.where(np.array(small)[:,:,3]>=128); h=int(y.max()-y.min()+1); w=int(x.max()-x.min()+1)
    if h==240 and w%2==0:
        found.append({'scale':float(factor),'bbox':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]}); break
Path('out/registration_scale_search.json').write_text(json.dumps({'initial_scale':s,'reason':'Frame-zero width was odd; seek a single uniform scale giving measured height 240 and even width for exact half-integer centre with integer translation.','grid':{'min':239/1132,'max':241/1132,'count':401},'chosen':found[0] if found else None},indent=2)+'\n')
print(found)
PY

COMMAND 5
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys,json,hashlib,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.signal import find_peaks,periodogram
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from oracle.motion_map import alpha_box
from gates.common import measure
root=Path('out'); data=json.loads((root/'native_curves.json').read_text()); native=json.loads((root/'native_measurements.json').read_text())
x=np.array(data['chest_dw_H']); raw,props=find_peaks(-x,prominence=0)
rest=[int(i) for i in raw if x[i]<=x.min()+.05*np.ptp(x)]
candidates=[(a,b) for a,b in zip(rest,rest[1:]) if np.max(x[a:b+1])-max(x[a],x[b])>=.9*np.ptp(x)]
if not candidates: raise RuntimeError('No minimum-to-minimum full breath found')
a,b=min(candidates,key=lambda ab: abs(float(x[ab[0]]-x[ab[1]])))
indices=np.floor(a+np.arange(16)*(b-a)/16+.5).astype(int).tolist()
first=Image.open(root/'matted'/f'matted_{a:03d}.png').convert('RGBA')
source_measure=measure(first); scale=json.loads((root/'registration_scale_search.json').read_text())['chosen']['scale']
if scale>1: raise RuntimeError('Requested scale would upscale')
scaled_size=tuple(math.ceil(v*scale) for v in first.size)
def scaled(im):
    return im.transform(scaled_size,Image.Transform.AFFINE,(1/scale,0,0,0,1/scale,0),resample=Image.Resampling.BICUBIC)
sm=measure(scaled(first)); sx=(sm['bbox'][0]+sm['bbox'][2]-1)/2; sy=sm['bbox'][3]-1
dx=round(255.5-sx); dy=399-sy
frames=[]
strip=Image.new('RGB',(512*16,544),'#3a3f4a'); draw=ImageDraw.Draw(strip)
for j,i in enumerate(indices):
    im=Image.open(root/'matted'/f'matted_{i:03d}.png').convert('RGBA'); small=scaled(im)
    frame=Image.new('RGBA',(512,512)); frame.alpha_composite(small,(dx,dy))
    path=root/'frames'/'idle'/'S'/f'idle_S_{j:02d}.png'; frame.save(path)
    m=measure(frame); nr=native['frames'][i]
    frames.append({'frame':j,'path':str(path),'native_index':i,'time_s':nr['time_s'],'output_time_s':j/8,'phase':j/16,'ideal_native_index':a+j*(b-a)/16,'native_bbox':nr['bbox'],'native_bbox_height':nr['bbox_height'],'native_sole_line':nr['sole_line'],'bbox':m['bbox'],'bbox_height':m['height'],'sole_line':m['bbox'][3]-1,'center_x':m['silhouette_center'][0],'root_anchor':[256,400],'sole_contact_bbox_bottom_x_range':[m['bbox'][0],m['bbox'][2]-1],'border_alpha_max':m['border_alpha_max'],'plate_survival':{k:v for k,v in nr.items() if k.startswith('plate_') or k.startswith('keyed_')},'matte_error':nr['matte_error']})
    strip.paste(frame,(j*512,0),frame)
    draw.text((j*512+12,518),f'{j:02d}  native {i:03d}  t={nr["time_s"]:.6f}s',fill='white')
strip.save(root/'sheets'/'idle_S_strip.png')
freq,power=periodogram(x,fs=24,detrend='constant',window='boxcar'); k=int(np.argmax(power[1:])+1)
seed_path=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-seed/registration_transform.json')
band_path=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/oracle/bands_idle.json'); band=json.loads(band_path.read_text())['relaxed']
concerns=['Frozen autocorrelation dominant period is unavailable: the retained clip contains only one full breath; the frozen instrument requires at least two cycles.','A same-size nonoverlapping control box does not fit the native canvas; frozen contamination measurement is unavailable.','The spectral dominant period is one clip-length bin (104 frames), not a resolved repeated-cycle estimate.','Input geometry is 768x1168 at 24 fps, rather than the brief description of 720p.']
if frames[0]['center_x']!=255.5: concerns.append(f'Integer translation leaves frame-0 center-x at {frames[0]["center_x"]}, a {frames[0]["center_x"]-255.5:+.1f} px residual from 255.5 due to raster parity.')
if frames[0]['bbox_height']!=240: concerns.append(f'Frame-0 raster height is {frames[0]["bbox_height"]} px after exact uniform factor 240/source_height.')
reg={'task_id':'K3p-xv-idle-cut-01','source':{'clip':'/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/xvideo/in/idle_C_grok.mp4','dimensions':[768,1168],'fps':24,'retained_frames':104,'retained_time_range_s':[native['frames'][0]['time_s'],native['frames'][-1]['time_s']],'selection_filter':'lte(t,4.3)','native_index_base':0},'seed_geometry':json.loads(seed_path.read_text()),'relaxed_band':{k:band[k] for k in ['breath_period_s','breath_amplitude_H','head_sway_H','committed','provisional']},'native_alpha_box':data['box'],'native_alpha_box_method':'Union of alpha>=128 boxes, identical convention to frozen alpha_box; native dimensions exceed its 512x512 input restriction.','registered_alpha_box':alpha_box(root/'frames'/'idle'/'S'),'breath':{'frozen_dominant_period_frames':data['summary']['breath_period_frames'],'frozen_dominant_period_s':data['summary']['breath_period_s'],'frozen_period_confidence':data['summary']['period_confidence'],'spectral_dominant_period_frames':float(24/freq[k]),'spectral_dominant_period_s':float(1/freq[k]),'spectral_method':'scipy.signal.periodogram, constant detrend, boxcar; largest non-DC bin; one-cycle finite-window diagnostic only','chest_width_peak_to_peak_percent_H':float(np.ptp(x)*100),'chest_width_p95_minus_p05_percent_H':data['summary']['breath_amplitude_H']*100,'head_peak_to_peak_percent_H':float(np.ptp(data['head_dy_H'])*100),'head_p95_minus_p05_percent_H':data['summary']['head_sway_H']*100,'normalization_H_native_px':data['height'],'all_raw_local_minima':raw.tolist(),'all_raw_minima_prominence_H':props['prominences'].tolist(),'rest_minima_native_indices':rest,'rest_minima_definition':'Raw local minima within the bottom 5% of the full chest-width range; ignores small fluctuations on expanded plateaus.','full_breath_candidates':[list(v) for v in candidates],'full_breath_definition':'Consecutive rest minima enclosing at least 90% of the measured chest-width range.','chosen_consecutive_minima_native_indices':[a,b],'chosen_minima_time_s':[native['frames'][a]['time_s'],native['frames'][b]['time_s']],'chosen_minima_chest_width_H':[float(x[a]),float(x[b])],'minimum_to_minimum_period_native_frames':b-a,'minimum_to_minimum_period_s':(b-a)/24,'selection_reason':'Only qualifying full breath; minimum-to-minimum with nearest rest-width endpoint match.','selected_peak_native_index':int(a+np.argmax(x[a:b+1])),'endpoint_excluded':True,'resampling':'Nearest native frame at equal target phases j/16, round-half-up; no blending, synthesis or endpoint duplication.','output_fps':8,'output_duration_s':2.0,'time_compression_source_duration_over_output':(b-a)/24/2,'curve_files':['out/native_curves.json','out/native_measurements.json']},'transform':{'scale':scale,'source_frame_zero_native_index':a,'source_frame_zero_bbox_height':source_measure['height'],'scaled_canvas_size':list(scaled_size),'resampling':'PIL affine bicubic, inverse diagonal 1/scale on both axes; scale about origin','integer_translation_xy':[dx,dy],'canvas':[512,512],'pivot':[256,400],'target_sole_row':399,'target_center_x':255.5,'frame_zero_measured_height':frames[0]['bbox_height'],'frame_zero_measured_sole_line':frames[0]['sole_line'],'frame_zero_measured_center_x':frames[0]['center_x'],'one_scale_and_translation_for_all_frames':True,'upscaling':False,'sole_line_definition':'Bottommost row of alpha>=128 figure support (includes held equipment); no independent anatomical annotation.','root_anchor_note':'Atlas pivot is fixed metadata, not independently inferred anatomy.'},'plate_survival':{'definition':'Border plate survival = fraction satisfying G>210,R<45,B<45 in 10px border; also counts those keyed pixels retaining alpha>0 and alpha>=128 after frozen matte.','alpha_floor':40,'minimum_border_green_fraction':min(r['plate_border_green_fraction'] for r in native['frames']),'matte_failures':[r for r in native['frames'] if r['matte_error']],'per_native_frame':native['frames']},'splice_check':{'metric':'XOR silhouette area divided by union silhouette area, alpha>=128, consecutive native frames','largest_silhouette_jump':max(native['silhouette_jumps'],key=lambda j:j['silhouette_jump_iou_distance']),'largest_absolute_xor_jump':max(native['silhouette_jumps'],key=lambda j:j['silhouette_xor_pixels']),'scope':'Only retained 0–4.3s segment; the reported ~4.5s splice is excluded and is not measured.','all_pairs':native['silhouette_jumps']},'frames':frames,'concerns':concerns}
(root/'registration.json').write_text(json.dumps(reg,indent=2,allow_nan=False)+'\n')
print(json.dumps({'minima':[a,b],'rest':rest,'period_frames':b-a,'amplitude_percent_H':np.ptp(x)*100,'transform':reg['transform'],'indices':indices,'concerns':concerns},indent=2),flush=True)
PY

COMMAND 6
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates.common import difference
root=Path('out'); p=root/'registration.json'; r=json.loads(p.read_text())
for f in r['frames']:
    im=Image.open(f['path']); assert im.size==(512,512) and im.mode=='RGBA'
    mask=np.array(im)[:,:,3]>=128; y,x=np.where(mask); bottom=int(y.max()); bx=np.where(mask[bottom])[0]
    f.pop('sole_contact_bbox_bottom_x_range',None)
    f['planted_sole_contact_proxy']={'method':'Bottommost alpha>=128 support row, not independent anatomical sole annotation','row':bottom,'x_range':[int(bx.min()),int(bx.max())],'median_x':float(np.median(bx))}
    assert f['time_s']<=4.3 and f['border_alpha_max']==0
assert len(r['frames'])==16 and len(list((root/'native').glob('*.png')))==104
assert r['frames'][0]['bbox_height']==240 and r['frames'][0]['sole_line']==399 and r['frames'][0]['center_x']==255.5
r['transform']['scale_selection']='Closest sampled single uniform factor to 240/1132 yielding raster height 240 and even alpha-bbox width; see registration_scale_search.json. Initial factor left a half-pixel centre residual.'
r['transform']['nominal_ratio_240_over_source_height']=240/1132
r['resampling_endpoint_diagnostics']={'minimum_to_minimum_native_rgb_MAD':difference(root/'matted'/'matted_001.png',root/'matted'/'matted_099.png'),'output_last_to_first_rgb_MAD':difference(r['frames'][-1]['path'],r['frames'][0]['path']),'note':'Descriptive only; no seam gate evaluated.'}
r['input_sha256']={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in [Path(r['source']['clip']),Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-seed/registration_transform.json'),Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/oracle/bands_idle.json')]}
for f in r['plate_survival']['per_native_frame']:
    q=root/'matted'/f'matted_{f["native_index"]:03d}.png'; f['intermediate_matte_sha256']=hashlib.sha256(q.read_bytes()).hexdigest()
r['intermediate_mattes']='Every native frame was matted and measured; intermediate PNGs removed after registration. Native PNGs, per-frame matte metadata and intermediate hashes retained.'
p.write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
checks={'task_id':r['task_id'],'native_count':104,'registered_count':16,'all_registered_rgba_512':True,'frame_zero':{'height':240,'sole_line':399,'center_x':255.5},'single_uniform_scale':r['transform']['scale'],'single_integer_translation':r['transform']['integer_translation_xy'],'maximum_retained_time_s':r['source']['retained_time_range_s'][1],'minimum_plate_border_green_fraction':r['plate_survival']['minimum_border_green_fraction'],'matte_error_count':len(r['plate_survival']['matte_failures']),'native_indices':[f['native_index'] for f in r['frames']],'registered_height_range':[min(f['bbox_height'] for f in r['frames']),max(f['bbox_height'] for f in r['frames'])],'registered_sole_row_range':[min(f['sole_line'] for f in r['frames']),max(f['sole_line'] for f in r['frames'])],'concerns':r['concerns'],'note':'Measurements and artifact consistency only; no conductor gates evaluated.'}
(root/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
for q in (root/'matted').glob('*.png'): q.unlink()
(root/'matted').rmdir()
print(json.dumps(checks,indent=2))
PY
