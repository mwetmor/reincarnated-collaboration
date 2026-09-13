K3p-xv-cut-03 — registered explicit stride

Delivered 12 walk frames and native clip frame 0 as the rest frame.
Stride [53,87); selected native indices:
53, 56, 59, 61, 64, 67, 70, 73, 76, 79, 81, 84.
All samples are within 0–4.3 s. No stride selection or gait evaluation was performed.
Frame 0 is DOWN, one phase after plate-13 CONTACT — rotation +1, per conductor R-46.
The committed phase_table is preserved verbatim; sample order was not changed.

The previous artifact contained no reusable matted PNGs. The selected clip frames
were decoded directly into memory using ffmpeg select by native frame number.
Actual source size is 768x1168, 24 fps. Frozen gates.matte.extract(alpha_floor=40)
was applied in memory. No intermediate native images are delivered.

Reference walk frame 00 = native frame 53: native alpha>=128 bbox height 1081 px.
Initial nominal scale 240/1081 produced rasterized height 239 px.
One diagnosed calibration used scale 241/1081 = 0.22294172062904719 for all frames.
LANCZOS resized each full native canvas to the same rounded dimensions 171x260.
One integer translation (166,153) was used for every walk frame and the rest frame.
Delivered frame 00 bbox [193,160,319,400), height 240 px, sole row 399,
bbox centre x=255.5. Every delivered frame is transparent RGBA, 512x512.
Atlas pivot is (256,400). No per-frame re-centring, per-frame scaling, or upscaling.
The strip contains the unscaled 512x512 frames on #3a3f4a with frame numbers.
Native and registered per-frame bbox heights and sole rows are in registration.json.
The alpha_box is a descriptive union from the frozen instrument, not a gate result.

Only out/ was written; frozen-module bytecode writes were disabled.
No image generation, web, agent delegation, or gate judgments.
Pre-existing out/.wrapper-* files are live runner telemetry, not produced artifacts;
they are excluded from the receipt manifest because their contents change during
the wrapper's recording of this response.

Exact executed processing commands follow. The first command records the initial
raster calibration; the second overwrites the same deliverables using the final
shared transform. Both call frozen modules through explicitly permitted inline
glue; no new tool files were created. ffmpeg argv is also in registration.json.
This readme was written with apply_patch.

INITIAL COMMAND
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys, json, subprocess, re, hashlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.dont_write_bytecode = True
root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
sys.path.insert(0, str(root))
from gates.matte import extract
from oracle.motion_map import alpha_box
out = Path('out')
clip = root/'runs/C-1/xvideo/in/walk_E_grok.mp4'
seed_path = root/'runs/C-1/artifacts/K3p-seed/registration_transform.json'
band_path = root/'oracle/bands_walk.json'
seed = json.loads(seed_path.read_text())
phases = json.loads(band_path.read_text())['plate13_lateral_ann']['phase_table']
indices = [53,56,59,61,64,67,70,73,76,79,81,84]
all_indices = [0] + indices
select = '+'.join(f'eq(n,{n})' for n in all_indices)
args = ['/opt/homebrew/bin/ffmpeg','-hide_banner','-nostdin','-i',str(clip),'-t','4.3','-map','0:v:0','-vf',f"select='{select}',showinfo",'-fps_mode','passthrough','-frames:v','13','-f','rawvideo','-pix_fmt','rgb24','pipe:1']
p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
log = p.stderr.decode()
(out/'ffmpeg_extract.log').write_text(log)
info = re.findall(r'n:\s*(\d+)\s+pts:\s*(\d+)\s+pts_time:([0-9.]+).*?s:(\d+)x(\d+)',log)
assert len(info) == 13, info
w,h = map(int,info[0][3:])
assert len(p.stdout) == 13*w*h*3
raw = np.frombuffer(p.stdout,dtype=np.uint8).reshape(13,h,w,3)
matted = []
matte_info = []
for a in raw:
    image, report = extract(Image.fromarray(a),alpha_floor=40)
    matted.append(image)
    matte_info.append(report)
def geom(im):
    y,x = np.where(np.asarray(im)[...,3] >= 128)
    box = [int(x.min()),int(y.min()),int(x.max())+1,int(y.max())+1]
    return {'bbox_xyxy':box,'bbox_height':box[3]-box[1],'sole_line':box[3]-1,'bbox_center_x':(box[0]+box[2]-1)/2}
base = geom(matted[1])
scale = 240/base['bbox_height']
size = (round(w*scale),round(h*scale))
scaled = [im.resize(size,Image.Resampling.LANCZOS) for im in matted]
sg = geom(scaled[1])
dx = round(255.5-sg['bbox_center_x'])
dy = 399-sg['sole_line']
concerns = []
if sg['bbox_height'] != 240:
    concerns.append(f"Frame 0 rasterized height is {sg['bbox_height']} px after scale 240/native_height; target 240 px.")
if sg['bbox_center_x']+dx != 255.5:
    concerns.append(f"Integer translation places frame 0 bbox center at {sg['bbox_center_x']+dx}; exact 255.5 is unavailable at this raster width.")
frames=[]
for i,(native,im) in enumerate(zip(all_indices,scaled)):
    canvas=Image.new('RGBA',(512,512),(0,0,0,0))
    canvas.paste(im,(dx,dy))
    target = out/'frames/rest/E/rest_E.png' if i==0 else out/f'frames/walk/E/walk_E_{i-1:02d}.png'
    target.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(target)
    before = geom(im)
    after = geom(canvas)
    if after['bbox_height'] != before['bbox_height'] or after['bbox_xyxy'] != [before['bbox_xyxy'][0]+dx,before['bbox_xyxy'][1]+dy,before['bbox_xyxy'][2]+dx,before['bbox_xyxy'][3]+dy]:
        concerns.append(f'Alpha>=128 support was clipped for native frame {native}.')
    frames.append({'path':str(target),'frame':None if i==0 else i-1,'native_index':native,'time_s':native/24,'pts':int(info[i][1]),'ffmpeg_pts_time_s':float(info[i][2]),'native':geom(matted[i]),'registered':after,'scale':scale,'translation_xy':[dx,dy],'matte':matte_info[i]})
strip=Image.new('RGB',(512*12,512),'#3a3f4a')
draw=ImageDraw.Draw(strip)
font=ImageFont.load_default(size=24)
for i,im in enumerate(scaled[1:]):
    with Image.open(out/f'frames/walk/E/walk_E_{i:02d}.png') as frame:
        strip.paste(frame,(i*512,0),frame)
    draw.text((i*512+20,20),f'{i:02d} | native {indices[i]}',fill='#ffffff',font=font)
(out/'sheets').mkdir(exist_ok=True)
strip.save(out/'sheets/walk_E_strip.png')
sha=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest()
registration={'task_id':'K3p-xv-cut-03','source':{'path':str(clip),'sha256':sha(clip),'native_size':[w,h],'fps':24,'permitted_time_s':[0,4.3],'extraction_indices':all_indices,'reused_matted_frames':False},'stride_native_interval_half_open':[53,87],'selected_native_indices':indices,'scale':scale,'scale_definition':'240 / native alpha>=128 bbox height of walk frame 00 (native 53)','native_reference_height':base['bbox_height'],'scaled_canvas_size':list(size),'resize':'PIL Image.resize, LANCZOS, dimensions rounded from the one shared scalar','rasterized_axis_ratios':[size[0]/w,size[1]/h],'translation_xy':[dx,dy],'canvas':[512,512],'pivot':[256,400],'target_sole_line':399,'target_bbox_center_x':255.5,'reference_frame':{'walk_frame':0,'native_index':53,'registered':frames[1]['registered']},'phase_note':"Frame 0 is a DOWN phase, one phase after plate-13's CONTACT — rotation +1 (conductor R-46). Native sample order is fixed as supplied; no additional rotation applied.",'rotation':1,'phase_table_source':str(band_path),'phase_table_row':'plate13_lateral_ann','phase_table':phases,'phase_table_note':'Committed table preserved verbatim as target metadata; phases are not re-detected or judged.','seed_geometry':seed,'seed_geometry_sha256':sha(seed_path),'band_sha256':sha(band_path),'rest':frames[0],'frames':frames[1:],'alpha_box':alpha_box(out/'frames/walk/E'),'gate_evaluation_performed':False,'concerns':concerns,'ffmpeg_argv':args}
(out/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
print(json.dumps({'native_size':[w,h],'native_height':base['bbox_height'],'scale':scale,'scaled_size':size,'translation':[dx,dy],'frame0':frames[1]['registered'],'concerns':concerns,'frames_written':len(frames)},indent=2))
PY

FINAL COMMAND
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys, json, subprocess, re, hashlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.dont_write_bytecode = True
root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
sys.path.insert(0, str(root))
from gates.matte import extract
from oracle.motion_map import alpha_box
out = Path('out')
clip = root/'runs/C-1/xvideo/in/walk_E_grok.mp4'
seed_path = root/'runs/C-1/artifacts/K3p-seed/registration_transform.json'
band_path = root/'oracle/bands_walk.json'
seed = json.loads(seed_path.read_text())
phases = json.loads(band_path.read_text())['plate13_lateral_ann']['phase_table']
indices = [53,56,59,61,64,67,70,73,76,79,81,84]
all_indices = [0] + indices
select = '+'.join(f'eq(n,{n})' for n in all_indices)
args = ['/opt/homebrew/bin/ffmpeg','-hide_banner','-nostdin','-i',str(clip),'-t','4.3','-map','0:v:0','-vf',f"select='{select}',showinfo",'-fps_mode','passthrough','-frames:v','13','-f','rawvideo','-pix_fmt','rgb24','pipe:1']
p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
log = p.stderr.decode()
(out/'ffmpeg_extract.log').write_text(log)
info = re.findall(r'n:\s*(\d+)\s+pts:\s*(\d+)\s+pts_time:([0-9.]+).*?s:(\d+)x(\d+)',log)
assert len(info) == 13, info
w,h = map(int,info[0][3:])
assert len(p.stdout) == 13*w*h*3
raw = np.frombuffer(p.stdout,dtype=np.uint8).reshape(13,h,w,3)
matted = []
matte_info = []
for a in raw:
    image, report = extract(Image.fromarray(a),alpha_floor=40)
    matted.append(image)
    matte_info.append(report)
def geom(im):
    y,x = np.where(np.asarray(im)[...,3] >= 128)
    box = [int(x.min()),int(y.min()),int(x.max())+1,int(y.max())+1]
    return {'bbox_xyxy':box,'bbox_height':box[3]-box[1],'sole_line':box[3]-1,'bbox_center_x':(box[0]+box[2]-1)/2}
base = geom(matted[1])
scale = 241/base['bbox_height']
size = (round(w*scale),round(h*scale))
scaled = [im.resize(size,Image.Resampling.LANCZOS) for im in matted]
sg = geom(scaled[1])
dx = round(255.5-sg['bbox_center_x'])
dy = 399-sg['sole_line']
concerns = []
if sg['bbox_height'] != 240:
    concerns.append(f"Frame 0 rasterized height is {sg['bbox_height']} px after scale 240/native_height; target 240 px.")
if sg['bbox_center_x']+dx != 255.5:
    concerns.append(f"Integer translation places frame 0 bbox center at {sg['bbox_center_x']+dx}; exact 255.5 is unavailable at this raster width.")
frames=[]
for i,(native,im) in enumerate(zip(all_indices,scaled)):
    canvas=Image.new('RGBA',(512,512),(0,0,0,0))
    canvas.paste(im,(dx,dy))
    target = out/'frames/rest/E/rest_E.png' if i==0 else out/f'frames/walk/E/walk_E_{i-1:02d}.png'
    target.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(target)
    before = geom(im)
    after = geom(canvas)
    if after['bbox_height'] != before['bbox_height'] or after['bbox_xyxy'] != [before['bbox_xyxy'][0]+dx,before['bbox_xyxy'][1]+dy,before['bbox_xyxy'][2]+dx,before['bbox_xyxy'][3]+dy]:
        concerns.append(f'Alpha>=128 support was clipped for native frame {native}.')
    frames.append({'path':str(target),'frame':None if i==0 else i-1,'native_index':native,'time_s':native/24,'pts':int(info[i][1]),'ffmpeg_pts_time_s':float(info[i][2]),'native':geom(matted[i]),'registered':after,'scale':scale,'translation_xy':[dx,dy],'matte':matte_info[i]})
strip=Image.new('RGB',(512*12,512),'#3a3f4a')
draw=ImageDraw.Draw(strip)
font=ImageFont.load_default(size=24)
for i,im in enumerate(scaled[1:]):
    with Image.open(out/f'frames/walk/E/walk_E_{i:02d}.png') as frame:
        strip.paste(frame,(i*512,0),frame)
    draw.text((i*512+20,20),f'{i:02d} | native {indices[i]}',fill='#ffffff',font=font)
(out/'sheets').mkdir(exist_ok=True)
strip.save(out/'sheets/walk_E_strip.png')
sha=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest()
registration={'task_id':'K3p-xv-cut-03','source':{'path':str(clip),'sha256':sha(clip),'native_size':[w,h],'fps':24,'permitted_time_s':[0,4.3],'extraction_indices':all_indices,'reused_matted_frames':False},'stride_native_interval_half_open':[53,87],'selected_native_indices':indices,'scale':scale,'scale_definition':'241 / native alpha>=128 bbox height of walk frame 00 (native 53); one-pixel raster calibration from nominal 240/H to deliver alpha>=128 height exactly 240','native_reference_height':base['bbox_height'],'scaled_canvas_size':list(size),'resize':'PIL Image.resize, LANCZOS, dimensions rounded from the one shared scalar','rasterized_axis_ratios':[size[0]/w,size[1]/h],'translation_xy':[dx,dy],'canvas':[512,512],'pivot':[256,400],'target_sole_line':399,'target_bbox_center_x':255.5,'reference_frame':{'walk_frame':0,'native_index':53,'registered':frames[1]['registered']},'phase_note':"Frame 0 is a DOWN phase, one phase after plate-13's CONTACT — rotation +1 (conductor R-46). Native sample order is fixed as supplied; no additional rotation applied.",'rotation':1,'phase_table_source':str(band_path),'phase_table_row':'plate13_lateral_ann','phase_table':phases,'phase_table_note':'Committed table preserved verbatim as target metadata; phases are not re-detected or judged.','seed_geometry':seed,'seed_geometry_sha256':sha(seed_path),'band_sha256':sha(band_path),'rest':frames[0],'frames':frames[1:],'alpha_box':alpha_box(out/'frames/walk/E'),'gate_evaluation_performed':False,'concerns':concerns,'calibration_note':'Initial nominal 240/1081 scale rasterized to height 239; a single shared calibrated scale 241/1081 is used for every delivered walk/rest frame. No per-frame scaling.','ffmpeg_argv':args}
(out/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
print(json.dumps({'native_size':[w,h],'native_height':base['bbox_height'],'scale':scale,'scaled_size':size,'translation':[dx,dy],'frame0':frames[1]['registered'],'concerns':concerns,'frames_written':len(frames)},indent=2))
PY

