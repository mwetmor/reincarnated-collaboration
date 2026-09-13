K3p-xv-cut-04

Delivered: 12 registered walk frames, registered native-frame-0 rest, numbered strip, registration metadata.
All native frames were decoded directly from the named clip with ffmpeg's frame-number select filter; only native indices 0,71,74,77,79,82,85,88,91,94,97,99,102 were emitted. No intermediate PNGs were retained.

Final shared isotropic scale: 0.22059283088235293 (240.005 / 1088).
Final shared integer translation: (170,153).
Anchor is walk frame 00 / native frame 71: alpha>=128 height 240, sole row 399, bbox centre x 255.5. Native frame 0 is the rest image and receives exactly the same transform (height 245).
Native video: 768x1168, 24 fps. Prescribed stride [71,105); last selected frame is 102 at 4.25 s.
PIL LANCZOS uses a shared source box and floor-sized output so x and y scale remain exactly equal. Only unused plate boundary beyond the floor-sized sampling rectangle is excluded. Integer paste preserves straight alpha.

Phase note (conductor supplied): frame 0 is DOWN, one phase after plate-13 CONTACT; rotation +1. The committed phase_table is preserved verbatim, including its initial DOWN entry, without reordering the prescribed frames.

Registration calibration: nominal scale 240/1088 produced 239 thresholded pixels. An intermediate numerator 240.5 produced height 240 but an odd bbox width. The same diagnosed calibration selected the first numerator in linspace(240,240.5,101) meeting both raster targets; the resulting single transform is applied to all delivered frames.

Silhouette jump: largest adjacent selected-frame XOR/union = 0.4409398935110048, native 82 -> 85 (3.4166667 -> 3.5416667 s), 123890 changed pixels / 280968 union pixels. This is a descriptive measurement, not a gate.
Concern: the largest jump over all 33 consecutive native-frame pairs in [71,105) could not be computed under the explicit extract-ONLY-12 restriction. The reported maximum covers 11 adjacent selected pairs with 2-3-frame gaps, excluding the loop seam.
No gates evaluated. No image generation. Inputs and frozen modules unchanged.

Exact final reproduction command (run from the burst workdir; Python is inline glue, no tool file is created):

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys, subprocess, json, hashlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates.matte import extract
from oracle.walk_landmarks import landmarks
from oracle.motion_map import alpha_box
root=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
clip=root/'runs/C-1/xvideo/in/walk_E_grok.mp4'
seed_path=root/'runs/C-1/artifacts/K3p-seed/registration_transform.json'
band_path=root/'oracle/bands_walk.json'
seed=json.loads(seed_path.read_text())
phases=json.loads(band_path.read_text())['plate13_lateral_ann']['phase_table']
indices=[71,74,77,79,82,85,88,91,94,97,99,102]
selected=[0]+indices
selection='select='+ '+'.join('eq(n\\,%d)'%i for i in selected)
argv=['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(clip),'-map','0:v:0','-vf',selection,'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','pipe:1']
decoded=subprocess.run(argv,capture_output=True,check=True)
arrays=np.frombuffer(decoded.stdout,dtype=np.uint8).reshape(-1,1168,768,3)
assert len(arrays)==13
matted={}; masks={}; matte_info={}; native={}
for index,arr in zip(selected,arrays):
    matted[index],matte_info[index]=extract(Image.fromarray(arr),alpha_floor=40)
    masks[index]=np.array(matted[index])[...,3]>=128
    native[index]=landmarks(masks[index])
# Calibrate a SINGLE shared scale against both integer-raster anchor targets.
# No frame-specific scaling or translation is used.
for numerator in np.linspace(240,240.5,101):
    scale=float(numerator/native[71]['H'])
    scaled_size=(int(768*scale),int(1168*scale))
    source_box=(0.,0.,scaled_size[0]/scale,scaled_size[1]/scale)
    candidate=matted[71].resize(scaled_size,Image.Resampling.LANCZOS,box=source_box)
    cy,cx=np.where(np.array(candidate)[...,3]>=128)
    if cy.max()-cy.min()+1==240 and (cx.max()-cx.min()+1)%2==0:
        break
else:
    raise ValueError('No shared scale meets both raster anchor targets in calibration interval')
# The matching source box gives exactly the same x/y scale.
resized={i:im.resize(scaled_size,Image.Resampling.LANCZOS,box=source_box) for i,im in matted.items()}
y,x=np.where(np.array(resized[71])[...,3]>=128)
translation=[int(round(255.5-(x.min()+x.max())/2)),399-int(y.max())]
canvas_size=seed['frame_canvas']
for p in ['out/frames/rest/E','out/frames/walk/E','out/sheets']:
    Path(p).mkdir(parents=True,exist_ok=True)
records=[]; images={}
for index in selected:
    im=Image.new('RGBA',(canvas_size,canvas_size),(0,0,0,0))
    im.paste(resized[index],tuple(translation))
    images[index]=im
    mask=np.array(im)[...,3]>=128
    yy,xx=np.where(mask)
    d=landmarks(mask)
    f=None if index==0 else indices.index(index)
    path='out/frames/rest/E/rest_E.png' if index==0 else 'out/frames/walk/E/walk_E_%02d.png'%f
    im.save(path)
    records.append({'path':path,'output_frame':f,'native_index':index,'time_s':index/24,'native_bbox_height':native[index]['H'],'native_sole_line':native[index]['sole_line_y'],'bbox_xyxy':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'bbox_height':d['H'],'sole_line':d['sole_line_y'],'bbox_center_x':float((xx.min()+xx.max())/2),'matte':matte_info[index],'target_phase_table_row':None if f is None else phases[f]})
strip=Image.new('RGB',(512*12,544),'#3a3f4a')
draw=ImageDraw.Draw(strip)
for f,index in enumerate(indices):
    strip.paste(images[index],(f*512,0),images[index])
    draw.text((f*512+16,519),'%02d | native %d | %.4f s'%(f,index,index/24),fill='white')
strip.save('out/sheets/walk_E_strip.png')
pairs=[]
for a,b in zip(indices,indices[1:]):
    union=masks[a]|masks[b]
    xor=masks[a]^masks[b]
    pairs.append({'native_indices':[a,b],'delta_native_frames':b-a,'times_s':[a/24,b/24],'silhouette_xor_pixels':int(xor.sum()),'silhouette_union_pixels':int(union.sum()),'silhouette_jump_xor_over_union':float(xor.sum()/union.sum())})
concerns=['Largest consecutive native-frame silhouette jump across all 33 pairs in [71,105) was not computed: extraction was explicitly limited to the 12 named walk frames. The largest adjacent selected-frame jump is reported instead, with 2-3 native-frame gaps.']
registration={'task_id':'K3p-xv-cut-04','source_clip':str(clip),'source_dimensions':[768,1168],'fps':24,'stride_native_range_half_open':[71,105],'stride_start_s':71/24,'stride_end_exclusive_s':105/24,'selected_native_indices':indices,'latest_selected_time_s':102/24,'cut_authority':'R-46; head-up stride; R-51; time limit relaxed to 4.4 s, known splice approximately 4.5 s','seed_geometry':seed,'anchor':'walk_E_00 / native frame 71; native frame 0 is rest and uses identical transform','scale':scale,'scale_basis_native_height':native[71]['H'],'scale_calibration_note':'Nominal 240/1088 yielded 239 thresholded pixels. Select first numerator in linspace(240,240.5,101) yielding height 240 and even bbox width; divide by 1088 and apply that ONE scale to every frame.','translation_xy':translation,'canvas':[512,512],'pivot':[256,400],'target_sole_row':399,'target_bbox_center_x':255.5,'target_anchor_height':240,'resampling':'PIL LANCZOS, one exact isotropic scale using shared source sampling box; integer paste, no per-frame recentering','scaled_size':list(scaled_size),'source_sampling_box_xyxy':list(source_box),'sampling_note':'Floor-sized destination excludes only less than one output pixel of the original right/bottom plate boundary; all subject alpha support remains inside the source box. x and y scale are identical.','phase_note':'Output frame 0 is a DOWN phase, one phase after plate-13 CONTACT: rotation +1 (conductor-supplied). The committed phase table is retained verbatim; frames are not reordered or re-selected.','phase_rotation':1,'committed_phase_table':phases,'frames':records[1:],'rest_frame':records[0],'walk_union_alpha_box':alpha_box('out/frames/walk/E'),'silhouette_jump':{'definition':'symmetric difference area / union area of native alpha>=128 masks, no alignment; descriptive only','coverage':'11 adjacent selected-frame pairs, excluding loop seam','pairs':pairs,'largest_adjacent_selected_pair':max(pairs,key=lambda p:p['silhouette_jump_xor_over_union']),'largest_consecutive_native_pair':None},'gates_evaluated':False,'concerns':concerns,'ffmpeg_argv':argv}
Path('out/registration.json').write_text(json.dumps(registration,indent=2)+'\n')
print(json.dumps({'scale':scale,'translation':translation,'scaled_size':scaled_size,'anchor':records[1],'rest_height':records[0]['bbox_height'],'jump':registration['silhouette_jump']['largest_adjacent_selected_pair'],'concerns':concerns},indent=2))
PY

