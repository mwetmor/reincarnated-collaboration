CHECK BURST K3p-cmp-x2-01 — attempt 2 of relaxed idle.

Inputs: explicitly named K3p-reg-x2-01 frames 00-15 and K3p-seed canvas.
References to K3p-reg-01 inside the task are treated as stale attempt-1 labels.
No generation calls. No input or frozen-tool modifications. Python bytecode writes disabled.
Only inline calls to frozen measurements and task-authorized Pillow/numpy orchestration; no executable source files created.

Base: seed slot (0,0,627,627), character matte alpha_floor=40, scale request 0.5106,
rounded raster 320x320 with LANCZOS, paste (96,112), integer translation (0,0).
The effective integer-raster ratio is 320/627. Alpha>=128 bbox [210,160,302,400],
height 240, sole row 399, center-x 255.5. Direct alpha>=128 bbox computation was used.

Frozen shoulders_chest R: [210,203,302,268].
Staff qualifying columns 215,216,217 have row coverage 1,1,0.9076923076923077.
Staff support [215,218); padded exclusion [212,221).
Final boxes (exclusive upper bounds): [210,203,212,268], [221,203,302,268].
Composite defaults: strict difference >8; square dilation radius 2 clipped to each box.
Frozen compose_loop supports only one box per variant; composite() called sequentially per box.
Every frame starts from the same seed-derived base, never the preceding animation frame.
Frame 00 is a byte-identical file copy of the base.
Primary G12 uses the union of declared boxes; replacement-mask-union G12 is also reported.
Union changed fraction uses any differing RGBA byte and geometric union area 5395 pixels.
All 16 primary preservation fractions are 1.0; geometric mask figure fraction is 0.34600274097761535.
No candidate verdict is declared here; instrument booleans remain in the SPEC envelopes.

Limitations:
1. No cast05 input was supplied, so the literal G11 comparator is UNEVALUABLE.
   All 16 adjacent/seam drift48 pairs for each loop and 16 original-versus-base values are computed.
2. Frozen shoulders_chest overlaps frozen arms_left/arms_right. The explicitly mandated
   R/staff boxes are retained; unchanged overlapping arm strips cannot also be guaranteed.
   Observed changed arm pixels are reported per frame, so the arm-preservation constraint
   is not represented as satisfied.
3. G6c for idle is the frozen G6b fallback, not an independent seam instrument.
4. thresh=8 and dilate_px=2 are documented provisional synthetic defaults, not tuned here.

Composited G6 seam MAD: 0.10262425740559895; literal minimum threshold 0.0629730224609375;
median threshold for G6b/idle G6c 0.27307383219401044.
Original G6 seam MAD: 0.20595169067382812; literal minimum threshold 0.15016301472981772;
median threshold for G6b/idle G6c 0.5673573811848959.
Strip: top original, bottom composited, columns 00-15, 512px cells, #3a3f4a background.
checks.json is a list of SPEC section 1 result envelopes. Gate values and thresholds come
from the frozen tools; threshold-free descriptive measurements have null passed.

Exact processing commands, executed from /Users/admin/astra-burst/runs/C-1/K3p-cmp-x2-01:

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B <<'PY'
from pathlib import Path
import json
import numpy as np
from PIL import Image
from gates import matte, common
from oracle.motion_map import region_boxes
out=Path('out')
(out/'base').mkdir(parents=True,exist_ok=True)
(out/'composited').mkdir(exist_ok=True)
(out/'strips').mkdir(exist_ok=True)
seed=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-seed/canvas_idle_S_seed.png')
crop=Image.open(seed).crop((0,0,627,627))
matted,metadata=matte.extract(crop,preserve_particles=False,alpha_floor=40)
small=matted.resize((round(627*0.5106),round(627*0.5106)),Image.Resampling.LANCZOS)
base=Image.new('RGBA',(512,512),(0,0,0,0))
base.paste(small,(96,112))
before=common.measure(base)
dy=399-(before['bbox'][3]-1)
cx=(before['bbox'][0]+before['bbox'][2]-1)/2
dx=int(round(255.5-cx)) if abs(cx-255.5)>2 else 0
shifted=Image.new('RGBA',(512,512),(0,0,0,0))
shifted.paste(base,(dx,dy))
shifted.save(out/'base/idle_S_base.png')
a=np.array(shifted)
y,x=np.where(a[...,3]>=128)
box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
regions=region_boxes(box,a.shape)
r=regions['shoulders_chest']
coverage=(a[r[1]:r[3],:,3]>=128).mean(axis=0)
columns=np.flatnonzero(coverage>=0.90)
groups=np.split(columns,np.where(np.diff(columns)>1)[0]+1)
bands=[[int(g[0]),int(g[-1])+1] for g in groups if len(g)]
record={'seed':str(seed),'crop_xyxy':[0,0,627,627],'matte':metadata,'requested_scale':0.5106,'rounded_size':list(small.size),'effective_raster_scale':320/627,'paste_xy':[96,112],'before_translation':before,'translation_xy':[dx,dy],'after_translation':common.measure(shifted),'alpha_box_method':'Identical alpha >=128 bbox directly from base, as explicitly permitted; no temporary input directory.','alpha_box':box,'regions':regions,'shoulders_chest_R':r,'all_contiguous_column_bands_with_90pct_support_half_open':bands,'staff_candidate_bands_at_most_14px':[b for b in bands if b[1]-b[0]<=14],'column_support_fractions':{str(i):float(coverage[i]) for b in bands if b[1]-b[0]<=14 for i in range(b[0],b[1])}}
(out/'base/registration.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
PY

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B <<'PY'
from pathlib import Path
import json, shutil
import numpy as np
from PIL import Image
from gates import common, mask_composite, drift48, g6_seam
out=Path('out')
source=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-reg-x2-01/frames/idle/S')
original=[common.rgba(source/f'idle_S_{i:02d}.png') for i in range(16)]
base=common.rgba(out/'base/idle_S_base.png')
b=np.array(base)
registration=json.loads((out/'base/registration.json').read_text())
boxes=[[210,203,212,268],[221,203,302,268]]
region_union=np.zeros((512,512),dtype=bool)
for x0,y0,x1,y1 in boxes:
    region_union[y0:y1,x0:x1]=True
results=[common.result('base_registration','idle/S/base',value=registration['after_translation']['height'],unit='px',notes=json.dumps(registration),evidence=['out/base/idle_S_base.png'])]
configuration={'input_directory':str(source),'input_resolution_note':'All original frames 00-15 use the explicitly named K3p-reg-x2-01; task references to K3p-reg-01 are treated as stale attempt-1 labels.','region_R':registration['shoulders_chest_R'],'boxes_xyxy_exclusive':boxes,'staff_support_x_half_open':[215,218],'staff_exclusion_x_half_open':[212,221],'staff_selection':'Leftmost narrow contiguous band with alpha >=128 in >=90% of R rows; visually confirmed screen-left staff.','thresh':8,'dilate_px':2,'min_preserved_fraction':0.99,'max_mask_figure_fraction':0.60,'region_union_pixels':int(region_union.sum()),'G12_primary_mask':'Union of the declared geometric boxes; actual replacement-mask union also reported separately.','arm_overlap_note':'Frozen shoulders_chest spans full alpha-box width and overlaps arms_left and arms_right. Exact requested R/staff split is used; arm-strip pixel preservation cannot simultaneously be imposed without changing those prescribed boxes.','g11_note':'No cast05 input supplied: literal G11 comparison remains UNEVALUABLE. Numeric adjacent/seam and original-vs-base measurements use identical 48px LANCZOS + frozen common dark-background comparator.','g6c_note':'animation=idle uses the frozen G6b fallback.'}
results.append(common.result('composite_configuration','idle/S',notes=json.dumps(configuration)))
composited=[base]
shutil.copyfile(out/'base/idle_S_base.png',out/'composited/idle_S_00.png')
frame_summary=[]
for i in range(16):
    actual_union=np.zeros((512,512),dtype=bool)
    per_box=[]
    current=base
    if i:
        for box in boxes:
            current,mask,metrics=mask_composite.composite(current,original[i],box)
            actual_union|=mask
            per_box.append(metrics)
        current.save(out/f'composited/idle_S_{i:02d}.png')
        composited.append(current)
    subject=f'composited/idle/S/{i:02d}'
    primary=mask_composite.evaluate(base,current,region_union,subject=subject)
    details=json.loads(primary['notes'])
    details['boxes_xyxy_exclusive']=boxes
    details['measurement_mask']='union of declared boxes'
    details['per_box_composite_metrics']=per_box
    primary['notes']=json.dumps(details,sort_keys=True)
    primary['evidence']=[f'out/composited/idle_S_{i:02d}.png','out/base/idle_S_base.png']
    results.append(primary)
    actual=mask_composite.evaluate(base,current,actual_union,subject=subject+'/replacement_mask_union')
    actual['id']='g12_base_preservation_replacement_mask_union'
    results.append(actual)
    changed=np.any(np.array(current)!=b,axis=2)
    results.append(common.result('union_box_changed_fraction',subject,value=float(changed[region_union].mean()),unit='fraction',notes=json.dumps({'changed_pixels':int(np.count_nonzero(changed&region_union)),'union_box_pixels':int(region_union.sum()),'definition':'Any differing RGBA byte versus approved base; denominator is geometric box union.'})))
    arm_counts={}
    for arm in ('arms_left','arms_right'):
        x0,y0,x1,y1=registration['regions'][arm]
        arm_counts[arm]=int(changed[y0:y1,x0:x1].sum())
    results.append(common.result('arm_strip_changed_pixels',subject,notes=json.dumps({'boxes':{k:registration['regions'][k] for k in arm_counts},'changed_pixels':arm_counts,'reason':'Documented overlap of frozen chest and arm region definitions.'})))
    frame_summary.append({'frame':i,'preserved_fraction':primary['value'],'region_mask_figure_fraction':details['mask_figure_fraction'],'union_changed_fraction':float(changed[region_union].mean()),'arm_changed_pixels':arm_counts})
small_base=base.resize((48,48),Image.Resampling.LANCZOS)
loop_summary={}
for name,frames in [('original',original),('composited',composited)]:
    subject=f'{name}/idle/S'
    literal_g11=drift48.evaluate(frames,subject=subject)
    results.append(literal_g11)
    small=[f.resize((48,48),Image.Resampling.LANCZOS) for f in frames]
    pairs=common.pair_differences(small)
    for i,pair in enumerate(pairs):
        results.append(common.result('drift48_pair',f'{subject}/{i:02d}->{(i+1)%16:02d}',value=pair['canvas'],unit='rgb_mad',notes=json.dumps({'foreground_union':pair['foreground_union'],'definition':'48px LANCZOS RGBA, composite on RGB(20,25,34), mean absolute RGB difference; no cast05 threshold supplied.'})))
    results.append(common.result('drift48_max_adjacent_and_seam',subject,value=max(p['canvas'] for p in pairs),unit='rgb_mad',notes='Numeric G11 measurement only; no cast05 comparison input supplied.'))
    seam_results=g6_seam.evaluate(frames,subject=subject)+[g6_seam.g6c(frames,subject=subject,animation='idle')]
    results.extend(seam_results)
    loop_summary[name]={'drift48_adjacent_and_seam':pairs,'G6_G6b_G6c':[{'id':r['id'],'value':r['value'],'threshold':r['threshold']} for r in seam_results]}
    if name=='original':
        for i,f in enumerate(small):
            diff=common.difference(f,small_base)
            results.append(common.result('drift48_original_vs_base',f'original/idle/S/{i:02d}',value=diff['canvas'],unit='rgb_mad',notes=json.dumps({'foreground_union':diff['foreground_union'],'definition':'Original frame versus approved seed-derived base at 48px LANCZOS; RGB(20,25,34) composite.'})))
strip=Image.new('RGBA',(512*16,512*2),(58,63,74,255))
for row,frames in enumerate((original,composited)):
    for i,frame in enumerate(frames):
        strip.alpha_composite(frame,(i*512,row*512))
strip.convert('RGB').save(out/'strips/original_vs_composited.png')
results.append(common.result('review_strip','idle/S',notes='Top row original frames 00-15; bottom row composited frames 00-15. Native 512px cells; background #3a3f4a.',evidence=['out/strips/original_vs_composited.png']))
(out/'checks.json').write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
print(json.dumps({'configuration':configuration,'frames':frame_summary,'loops':loop_summary},indent=2))
PY

