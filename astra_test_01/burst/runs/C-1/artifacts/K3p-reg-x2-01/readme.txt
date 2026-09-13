K3p-reg-x2-01 — attempt 2 of relaxed idle (previous: K3p-reg-01).
16 frames, 512x512 RGBA. Shared matte then 627-to-320 LANCZOS reduction,
paste at (96,112), followed only by per-frame integer translation.
Declared atlas pivot: (256,400). Independently measured sole row: 399 for all frames.
No per-frame scale, upscaling, mirroring, or art generation.
BBox uses alpha >=128, matching frozen common.py measurement convention.
Horizontal half-pixel differences round to nearest integer, ties away from zero.
Numbered strip is 8192x544, including a 32px label band, background #3a3f4a.

Concerns:
Frames 02,03: offset (0,7); 05,06: (0,13); 07: (8,0);
08: (0,14); 09: (8,14). These exceed 6 px.
Repeated seed slots in sheets 2–5 differ from sheet 1:
raw RGBA max deltas 180,166,193,160;
matted RGBA max deltas 237,255,255,226;
common opaque RGB max deltas 131,149,145,126 (all in 0..255 units).
These differences are not certified as matte noise; no tolerance was supplied.
No matted cell has nonzero alpha on its boundary.
See registration.json for complete per-cell and per-frame measurements.

Exact generation command (executed from the burst workdir):
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys, json, hashlib, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates.matte import extract

root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts')
transform_path = root / 'K3p-seed/registration_transform.json'
transform = json.loads(transform_path.read_text())
assert transform['cell_px'] == 627 and transform['scale'] == 0.5106
assert transform['scaled_cell_px'] == 320 and transform['offset_xy'] == [96,112]
assert transform['frame_canvas'] == 512
assert round(627 * transform['scale']) == 320
sources = [root / ('K3p-gen-idle-x2-%02d' % i) / ('k3p_idle_x2_S_%02d_%02d.png' % (3*i-2,3*i)) for i in range(1,6)]
out = Path('out')
(out / 'frames/idle/S').mkdir(parents=True, exist_ok=True)
(out / 'sheets').mkdir(parents=True, exist_ok=True)
cells, raw_seeds, matte_seeds, cell_records, concerns = [], [], [], [], []
for si, source in enumerate(sources):
    with Image.open(source) as opened:
        assert opened.size == (1254,1254), (source, opened.size)
        sheet = opened.convert('RGBA')
    for slot in range(4):
        x, y = (slot % 2)*627, (slot // 2)*627
        cell = sheet.crop((x,y,x+627,y+627))
        matte, info = extract(cell, preserve_particles=False, alpha_floor=40)
        a = np.asarray(matte)
        edge = np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])
        edge_max = int(edge.max())
        if edge_max:
            concerns.append('Sheet %d slot %d has nonzero matted alpha at a cell edge (maximum %d).' % (si+1,slot,edge_max))
        cell_records.append(dict(source_sheet=str(source), slot=slot, crop_xyxy=[x,y,x+627,y+627], matte=info, cell_edge_alpha_max=edge_max, figure_touches_cell_edge_alpha128=bool(edge_max>=128)))
        if slot == 0:
            raw_seeds.append(np.asarray(cell).astype(np.int16))
            matte_seeds.append(a.astype(np.int16))
        if si == 0 or slot != 0:
            reduced = matte.resize((320,320), Image.Resampling.LANCZOS)
            frame = Image.new('RGBA',(512,512),(0,0,0,0))
            frame.paste(reduced,(96,112))
            cells.append((str(source),slot,frame))

seed_records = []
for i in range(1,5):
    raw_delta = np.abs(raw_seeds[i]-raw_seeds[0])
    delta = np.abs(matte_seeds[i]-matte_seeds[0])
    opaque = (matte_seeds[i][...,3] == 255) & (matte_seeds[0][...,3] == 255)
    interior_max = int(delta[...,:3][opaque].max()) if opaque.any() else None
    record = dict(source_sheet=str(sources[i]), slot=0, reference_sheet=str(sources[0]), raw_rgba_max_abs_delta=int(raw_delta.max()), matted_rgba_max_abs_delta=int(delta.max()), matted_rgba_mean_abs_delta=float(delta.mean()), changed_matted_pixels=int(np.any(delta != 0,axis=2).sum()), common_opaque_rgb_max_abs_delta=interior_max)
    seed_records.append(record)
    if int(delta.max()) != 0:
        concerns.append('Sheet %d slot 0 differs from seed: matted RGBA max absolute delta %d/255; common opaque RGB max delta %s/255. No numerical matte-noise tolerance is supplied; difference is not certified as matte noise.' % (i+1,int(delta.max()),interior_max))

def geometry(im):
    alpha = np.asarray(im)[...,3]
    yy, xx = np.where(alpha >= 128)
    assert len(xx)
    box = [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
    return box, int(yy.max()), (box[0]+box[2]-1)/2

assert len(cells) == 16
base_box, base_sole, base_x = geometry(cells[0][2])
frames, records = [], []
for fi, (source,slot,frame) in enumerate(cells):
    box, sole, cx = geometry(frame)
    difference = base_x-cx
    dx = (int(math.copysign(math.floor(abs(difference)+0.5),difference)) if abs(difference)>2 else 0)
    dy = base_sole-sole
    aligned = Image.new('RGBA',(512,512),(0,0,0,0))
    aligned.paste(frame,(dx,dy))
    after_box, after_sole, after_x = geometry(aligned)
    assert after_sole == base_sole
    assert after_box == [box[0]+dx,box[1]+dy,box[2]+dx,box[3]+dy]
    assert int(np.asarray(frame)[...,3].sum()) == int(np.asarray(aligned)[...,3].sum())
    path = out / 'frames/idle/S' / ('idle_S_%02d.png' % fi)
    aligned.save(path)
    if max(abs(dx),abs(dy))>6 or math.hypot(dx,dy)>6:
        concerns.append('Frame %02d requires integer translation (%d,%d) px; magnitude %.3f px exceeds 6 px.' % (fi,dx,dy,math.hypot(dx,dy)))
    records.append(dict(frame=fi,path=str(path),source_sheet=source,slot=slot,alpha_bbox_threshold=128,alpha_bbox_before=box,alpha_bbox=after_box,alpha_nonzero_bbox=list(aligned.getchannel('A').getbbox()),bbox_height_px=after_box[3]-after_box[1],sole_line_before=sole,sole_line_after=after_sole,alpha_bbox_center_x_before=cx,alpha_bbox_center_x_after=after_x,offsets_applied_xy=[dx,dy],total_paste_offset_xy=[96+dx,112+dy],translation_magnitude_px=math.hypot(dx,dy),atlas_pivot=[256,400]))
    frames.append(aligned)

strip = Image.new('RGB',(16*512,544),'#3a3f4a')
draw = ImageDraw.Draw(strip)
for fi, frame in enumerate(frames):
    strip.paste(frame,(fi*512,0),frame)
    draw.text((fi*512+12,520),'%02d' % fi,fill='white')
strip.save(out / 'sheets/idle_S_strip.png')
registration = dict(task_id='K3p-reg-x2-01',attempt=2,previous_attempt='K3p-reg-01',transform_source=str(transform_path),transform=transform,actual_raster_scale=320/627,transform_method='Matte native 627px cell with frozen extract(character, alpha_floor=40); shared LANCZOS reduction to 320px; unmasked paste at (96,112); integer translation only, with no resampling.',alpha_bbox_convention='alpha >= 128; xyxy with exclusive upper bounds; pixel-centre x=(x_min+x_max_exclusive-1)/2',horizontal_rounding='Only translate when absolute centre difference >2px; nearest integer, half ties away from zero.',sole_reference=dict(frame=0,line_y=base_sole),atlas_pivot=[256,400],pivot_note='Declared atlas pivot; sole alignment is independently measured and does not assert reviewed anatomical anchor validation.',seed_persistence=dict(metric='maximum absolute channel delta on native 627px slot-0 cells; raw RGBA and frozen-matted RGBA recorded separately',max_abs_delta=max(r['matted_rgba_max_abs_delta'] for r in seed_records),raw_max_abs_delta=max(r['raw_rgba_max_abs_delta'] for r in seed_records),matte_noise_tolerance='Not numerically specified in brief; report all nonzero differences conservatively.',comparisons=seed_records),cells=cell_records,frames=records,concerns=concerns)
(out / 'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
print(json.dumps(dict(frame_count=len(frames),sole_y=base_sole,offsets=[r['offsets_applied_xy'] for r in records],heights=[r['bbox_height_px'] for r in records],seed_persistence=registration['seed_persistence'],concerns=concerns),indent=2))
PY

Exact verification and hashing command:
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
out = Path('out')
reg = json.loads((out/'registration.json').read_text())
assert len(reg['frames']) == 16
for record in reg['frames']:
    with Image.open(record['path']) as im:
        assert im.size == (512,512) and im.mode == 'RGBA'
        a = np.asarray(im)
        yy,xx = np.where(a[...,3]>=128)
        assert int(yy.max()) == 399 == record['sole_line_after']
        assert [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)] == record['alpha_bbox']
with Image.open(out/'sheets/idle_S_strip.png') as im:
    assert im.size == (8192,544)
files = [dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(out.rglob('*')) if p.is_file()]
assert len(files) == 19
print(json.dumps(dict(files=files),indent=2))
PY

Verification retry: frame geometry and strip dimensions verified; total file-count assertion encountered two active wrapper-owned logs (out/.wrapper-events.jsonl and out/.wrapper-stderr.txt). Corrected census excludes those mutable wrapper logs from the 19 delivered artifact hashes; no artwork or registration changes.
Exact corrected verification command:
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
out = Path('out')
reg = json.loads((out/'registration.json').read_text())
assert len(reg['frames']) == 16
for record in reg['frames']:
    with Image.open(record['path']) as im:
        assert im.size == (512,512) and im.mode == 'RGBA'
        a = np.asarray(im)
        yy,xx = np.where(a[...,3]>=128)
        assert int(yy.max()) == 399 == record['sole_line_after']
        assert [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)] == record['alpha_bbox']
with Image.open(out/'sheets/idle_S_strip.png') as im:
    assert im.size == (8192,544)
files = [dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(out.rglob('*')) if p.is_file() and not p.name.startswith('.wrapper-')]
assert len(files) == 19
print(json.dumps(dict(files=files),indent=2))
PY
