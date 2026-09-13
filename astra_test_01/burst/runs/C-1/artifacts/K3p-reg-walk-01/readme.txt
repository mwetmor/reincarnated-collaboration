K3p-reg-walk-01
Delivered 12 walk frames, sheet-1 slot-0 REST frame, numbered strip, and registration measurements.
No image generation. No per-frame scale, upscaling, mirroring, or affine resampling.
Each 627x627 cell is extracted with frozen gates.matte.extract(character mode, alpha_floor=40), reduced once with LANCZOS to 320x320, and pasted at (96,112). Pixel rounding of nominal scale 0.5106 yields effective scale 320/627 for every cell.
Sole alignment uses the task's literal bottom-most alpha >= 128 row, including any connected staff reaching lower than a boot; this global measurement is not an independently reviewed anatomical sole annotation.
REST ground row is 411; atlas root pivot metadata remains (256,400). No root-anchor gate is evaluated.
Horizontal centres use alpha >=128 bbox extreme-pixel midpoint. Half-pixel differences are rounded to the nearest integer, halves away from zero. Frame 0 is the horizontal reference.
All original per-cell and per-frame measurements, integer offsets, seed persistence, and concerns are in registration.json.
Source cells touching edges: sheet 2 slot 0; sheet 3 slots 0 and 1; sheet 4 slots 0 and 1.
Walk frames 01 through 11 need >6 px translation on at least one axis. Maximum |dx|=35, maximum |dy|=20.
All four source REST cells differ from the original E seed beyond matte-edge noise; max absolute raw RGB and matted RGBA delta is 255. Opaque-core deltas and counts are provided separately, without establishing a new gate.
Wrapper-owned hidden .wrapper-* logs are live audit infrastructure, not packet deliverables; they are left untouched and excluded from the deliverable hashes.
The strip uses 12 unscaled 512x512 frames over #3a3f4a, with a separate 32px number band.

Exact production command (run from /Users/admin/astra-burst/runs/C-1/K3p-reg-walk-01):
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates.matte import extract
base=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts')
out=Path('out')
transform_path=base/'K3p-seed/registration_transform.json'
t=json.loads(transform_path.read_text())
assert t['cell_px']==627 and t['scale']==0.5106 and t['scaled_cell_px']==320
assert t['offset_xy']==[96,112] and t['frame_canvas']==512
assert round(627*t['scale'])==320 and t['scale']<=1
sources=[base/f'K3p-gen-walk-{i+1:02d}'/name for i,name in enumerate(['k3p_walk_E_00_02.png','k3p_walk_E_03_05.png','k3p_walk_E_06_08.png','k3p_walk_E_09_11.png'])]
seed_path=base/'K3p-seed/canvas_walk_E_seed.png'
seed_sheet=Image.open(seed_path).convert('RGB')
assert seed_sheet.size==(1254,1254)
seed=seed_sheet.crop((0,0,627,627))
seed_matte,_=extract(seed,preserve_particles=False,alpha_floor=40)
seed_rgb=np.array(seed).astype(np.int16)
seed_rgba=np.array(seed_matte).astype(np.int16)
concerns=[]
records=[]
persistence=[]
frames=[]
def metrics(im):
    a=np.array(im)[...,3]
    y,x=np.where(a>=128)
    assert len(y)
    box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
    return {'alpha_bbox':box,'bbox_height_px':box[3]-box[1],
            'bbox_center_x':(box[0]+box[2]-1)/2,'sole_line':int(y.max()),
            'alpha_nonzero_bbox':list(im.getchannel('A').getbbox())}
for si,path in enumerate(sources):
    sheet=Image.open(path).convert('RGB')
    assert sheet.size==(1254,1254)
    for slot in range(4):
        x=(slot%2)*627;y=(slot//2)*627
        cell=sheet.crop((x,y,x+627,y+627))
        matte,info=extract(cell,preserve_particles=False,alpha_floor=40)
        a=np.array(matte)[...,3]
        border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
        edge=bool(np.any(border>0))
        if edge: concerns.append(f'{path.name} slot {slot}: extracted figure touches cell edge.')
        reduced=matte.resize((320,320),Image.Resampling.LANCZOS)
        registered=Image.new('RGBA',(512,512),(0,0,0,0))
        registered.paste(reduced,(96,112))
        pre=metrics(registered)
        rec={'source_sheet':str(path),'slot':slot,'cell_crop_xyxy':[x,y,x+627,y+627],
             'cell_alpha_bbox':list(matte.getchannel('A').getbbox()),'cell_edge_touched':edge,
             'cell_border_alpha_max':int(border.max()),'matte':info,'before_alignment':pre}
        if slot==0:
            raw_diff=np.abs(np.array(cell).astype(np.int16)-seed_rgb)
            rgba=np.array(matte).astype(np.int16)
            delta=np.abs(rgba-seed_rgba)
            core=(rgba[...,3]==255)&(seed_rgba[...,3]==255)
            core_delta=delta[...,:3][core]
            p={'source_sheet':str(path),'slot':0,'seed_path':str(seed_path),'seed_slot':0,
               'raw_rgb_max_abs_delta':int(raw_diff.max()),'raw_rgb_mean_abs_delta':float(raw_diff.mean()),
               'matted_rgba_max_abs_delta':int(delta.max()),
               'matted_rgba_mean_abs_delta':float(delta.mean()),
               'shared_opaque_core_rgb_max_abs_delta':int(core_delta.max()) if core_delta.size else None,
               'shared_opaque_core_pixels_with_rgb_delta_over_8':int(np.count_nonzero(np.any(core_delta>8,axis=1))) if core_delta.size else 0}
            persistence.append(p)
            rec['seed_persistence']=p
            rec['offsets_applied_xy']=[0,0]
            rec['sole_line_before']=pre['sole_line'];rec['sole_line_after']=pre['sole_line']
            rec.update(pre)
            if p['shared_opaque_core_pixels_with_rgb_delta_over_8']>0:
                concerns.append(f'{path.name} slot 0 differs from seed beyond edge matte noise: raw RGB max |delta|={p["raw_rgb_max_abs_delta"]}; shared opaque core max={p["shared_opaque_core_rgb_max_abs_delta"]}, {p["shared_opaque_core_pixels_with_rgb_delta_over_8"]} core pixels exceed 8 levels.')
            if si==0:
                rest=registered
                ground=pre['sole_line']
                rec['output']='out/frames/rest/E/rest_E.png'
            records.append(rec)
        else:
            frames.append((registered,rec))
reference_x=metrics(frames[0][0])['bbox_center_x']
walk_records=[]
strip=Image.new('RGB',(512*12,544),'#3a3f4a')
draw=ImageDraw.Draw(strip)
font=ImageFont.load_default(size=20)
for i,(im,rec) in enumerate(frames):
    pre=rec['before_alignment']
    difference=reference_x-pre['bbox_center_x']
    dx=int(math.copysign(math.floor(abs(difference)+0.5),difference)) if abs(difference)>2 else 0
    dy=ground-pre['sole_line']
    aligned=Image.new('RGBA',(512,512),(0,0,0,0))
    aligned.paste(im,(dx,dy))
    post=metrics(aligned)
    assert post['sole_line']==ground
    assert int(np.array(im)[...,3].sum())==int(np.array(aligned)[...,3].sum())
    assert post['bbox_height_px']==pre['bbox_height_px']
    path=out/f'frames/walk/E/walk_E_{i:02d}.png'
    path.parent.mkdir(parents=True,exist_ok=True)
    aligned.save(path)
    rec.update(post)
    rec.update({'frame':i,'output':str(path),'sole_line_before':pre['sole_line'],
                'sole_line_after':post['sole_line'],'offsets_applied_xy':[dx,dy],
                'total_paste_offset_xy':[96+dx,112+dy],
                'horizontal_difference_to_frame_0_before':difference,
                'horizontal_residual_to_frame_0_after':reference_x-post['bbox_center_x']})
    if max(abs(dx),abs(dy))>6:
        concerns.append(f'walk_E_{i:02d} needs translation ({dx}, {dy}) px, exceeding 6 px on at least one axis.')
    walk_records.append(rec)
    strip.paste(aligned,(512*i,32),aligned.getchannel('A'))
    draw.text((512*i+12,6),f'{i:02d}',font=font,fill='white')
rest_path=out/'frames/rest/E/rest_E.png'
rest_path.parent.mkdir(parents=True,exist_ok=True)
rest.save(rest_path)
(out/'sheets').mkdir(parents=True,exist_ok=True)
strip.save(out/'sheets/walk_E_strip.png')
registration={'task_id':'K3p-reg-walk-01','transform_source':str(transform_path),'transform':t,
    'effective_raster_scale':320/627,'resampling':'LANCZOS, exactly once per cell',
    'matte_order':'extract character mode alpha_floor=40 before resize',
    'alpha_bbox_threshold':128,'alpha_bbox_convention':'xyxy, upper bounds exclusive',
    'sole_definition':'bottom-most row with alpha >= 128; global lower contact per brief',
    'rest_ground_line':ground,'atlas_pivot_xy':[256,400],
    'pivot_note':'Declared atlas root anchor; sole line independently measured, not equated to the atlas pivot.',
    'horizontal_reference_frame':0,'horizontal_reference_center_x':reference_x,
    'integer_rounding':'nearest integer, halves away from zero; only when absolute centre difference > 2',
    'rest_cells':records,'walk_frames':walk_records,
    'seed_persistence':{'seed':str(seed_path),'seed_crop_xyxy':[0,0,627,627],
        'max_abs_delta_raw_rgb':max(p['raw_rgb_max_abs_delta'] for p in persistence),
        'max_abs_delta_matted_rgba':max(p['matted_rgba_max_abs_delta'] for p in persistence),
        'per_sheet':persistence,'noise_note':'Opaque-core changes are reported separately from matte edges; 8 levels is a diagnostic count, not an acceptance gate.'},
    'concerns':concerns}
(out/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
print(json.dumps({'rest_ground_line':ground,'offsets':[r['offsets_applied_xy'] for r in walk_records],
                  'bbox_heights':[r['bbox_height_px'] for r in walk_records],
                  'seed_persistence':registration['seed_persistence'],'concerns':concerns},indent=2))

PY

Exact verification and SHA-256 command:
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
out=Path('out')
r=json.loads((out/'registration.json').read_text())
paths=[out/'registration.json',out/'readme.txt',out/'sheets/walk_E_strip.png',out/'frames/rest/E/rest_E.png']+[out/f'frames/walk/E/walk_E_{i:02d}.png' for i in range(12)]
for p in paths:
    assert p.is_file(),str(p)
for row in r['walk_frames']:
    im=Image.open(row['output'])
    assert im.size==(512,512) and im.mode=='RGBA'
    a=np.array(im)[...,3]
    y,x=np.where(a>=128)
    assert int(y.max())==r['rest_ground_line']==row['sole_line_after']
    assert [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]==row['alpha_bbox']
    assert all(isinstance(v,int) for v in row['offsets_applied_xy'])
    assert row['bbox_height_px']==row['before_alignment']['bbox_height_px']
assert Image.open(out/'frames/rest/E/rest_E.png').size==(512,512)
assert Image.open(out/'sheets/walk_E_strip.png').size==(6144,544)
print(json.dumps({'files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
                  'verified_frames':12,'sole_row':r['rest_ground_line'],'concerns':r['concerns']},indent=2))

PY

