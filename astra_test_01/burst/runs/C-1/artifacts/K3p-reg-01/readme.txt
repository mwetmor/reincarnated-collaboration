# Exact generation command; run from the burst workdir. No generated-image calls.
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys, json, math, hashlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/gates')
from matte import extract
base = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts')
transform_path = base / 'K3p-seed/registration_transform.json'
transform = json.loads(transform_path.read_text())
assert transform['cell_px'] == 627 and transform['scale'] == 0.5106
assert transform['scaled_cell_px'] == round(627 * transform['scale']) == 320
assert transform['offset_xy'] == [96,112] and transform['frame_canvas'] == 512
out = Path('out')
(out / 'frames/idle/S').mkdir(parents=True, exist_ok=True)
(out / 'sheets').mkdir(parents=True, exist_ok=True)
paths = [base / f'K3p-gen-idle-{i:02d}' / f'k3p_idle_S_{suffix}.png' for i,suffix in enumerate(['01_03','04_06','07_09','10_12','13_15'],1)]
cells, raw_cells, matte_metadata = {}, {}, {}
concerns = []
edge_checks = []
for i,path in enumerate(paths):
    with Image.open(path) as sheet:
        assert sheet.size == (1254,1254)
        for slot in range(4):
            x,y = slot % 2 * 627, slot // 2 * 627
            raw = sheet.crop((x,y,x+627,y+627))
            cell, meta = extract(raw, preserve_particles=False, alpha_floor=40)
            cells[i,slot], raw_cells[i,slot], matte_metadata[i,slot] = cell, np.array(raw.convert('RGBA')), meta
            a = np.array(cell)[...,3]
            edge_max = int(max(a[0].max(),a[-1].max(),a[:,0].max(),a[:,-1].max()))
            edge_checks.append({'source_sheet':str(path),'slot':slot,'alpha_bbox':list(cell.getchannel('A').getbbox()),'border_alpha_max':edge_max,'touches_cell_edge':edge_max>0})
            if edge_max:
                concerns.append(f'{path.name} slot {slot}: matted figure touches cell edge (alpha {edge_max}).')
seed = np.array(cells[0,0]).astype(np.int16)
seed_persistence = []
for i in range(1,5):
    candidate = np.array(cells[i,0]).astype(np.int16)
    delta = np.abs(candidate-seed)
    opaque = (candidate[...,3] == 255) & (seed[...,3] == 255)
    opaque_delta = delta[...,:3][opaque]
    opaque_max = int(opaque_delta.max()) if opaque_delta.size else 0
    opaque_changed = int(np.count_nonzero(np.any(delta[...,:3]>2,axis=2) & opaque))
    item = {'source_sheet':str(paths[i]),'slot':0,'reference_sheet':str(paths[0]),'reference_slot':0,
            'raw_rgba_max_abs_delta':int(np.abs(raw_cells[i,0].astype(np.int16)-raw_cells[0,0].astype(np.int16)).max()),
            'matted_rgba_max_abs_delta':int(delta.max()),'matted_rgba_mean_abs_delta':float(delta.mean()),
            'matted_alpha_max_abs_delta':int(delta[...,3].max()),'mutually_opaque_rgb_max_abs_delta':opaque_max,
            'mutually_opaque_pixels_rgb_delta_gt_2':opaque_changed}
    seed_persistence.append(item)
    if opaque_changed:
        concerns.append(f'{paths[i].name} slot 0 differs from seed beyond edge matte noise: matted RGBA max |delta| {int(delta.max())}; {opaque_changed} mutually opaque pixels have RGB delta >2 (max {opaque_max}).')
def geometry(im):
    a = np.array(im)[...,3]
    box = list(im.getchannel('A').getbbox())
    yy,xx = np.where(a>=128)
    opaque_box = [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
    return {'alpha_bbox':box,'bbox_height_px':box[3]-box[1],'bbox_center_x':(box[0]+box[2]-1)/2,
            'alpha_128_bbox':opaque_box,'alpha_128_bbox_height_px':opaque_box[3]-opaque_box[1],'sole_line':int(yy.max())}
frames, records = [], []
for number,(i,slot) in enumerate([(0,0)]+[(i,slot) for i in range(5) for slot in (1,2,3)]):
    reduced = cells[i,slot].resize((320,320),Image.Resampling.LANCZOS)
    registered = Image.new('RGBA',(512,512),(0,0,0,0))
    registered.paste(reduced,(96,112))
    before = geometry(registered)
    if number == 0:
        target_sole, target_x = before['sole_line'], before['bbox_center_x']
    dy = target_sole-before['sole_line']
    difference_x = target_x-before['bbox_center_x']
    dx = int(math.copysign(math.floor(abs(difference_x)+0.5), difference_x)) if abs(difference_x)>2 else 0
    b = before['alpha_bbox']
    assert b[0]+dx>=0 and b[1]+dy>=0 and b[2]+dx<=512 and b[3]+dy<=512
    aligned = Image.new('RGBA',(512,512),(0,0,0,0))
    aligned.paste(registered,(dx,dy))
    after = geometry(aligned)
    assert after['sole_line'] == target_sole
    assert after['bbox_height_px'] == before['bbox_height_px']
    destination = out / f'frames/idle/S/idle_S_{number:02d}.png'
    aligned.save(destination)
    if max(abs(dx),abs(dy))>6:
        concerns.append(f'Frame {number:02d} requires integer translation ({dx},{dy}) px, exceeding 6 px on an axis.')
    records.append({'frame':number,'output':str(destination),'source_sheet':str(paths[i]),'slot':slot,
                    'source_alpha_bbox':list(cells[i,slot].getchannel('A').getbbox()),'matte':matte_metadata[i,slot],
                    'before_alignment':before,'alpha_bbox':after['alpha_bbox'],'bbox_height_px':after['bbox_height_px'],
                    'alpha_128_bbox':after['alpha_128_bbox'],'alpha_128_bbox_height_px':after['alpha_128_bbox_height_px'],
                    'sole_line_before':before['sole_line'],'sole_line_after':after['sole_line'],
                    'offsets_applied':{'base_paste_xy':[96,112],'integer_alignment_xy':[dx,dy],'total_paste_xy':[96+dx,112+dy]},
                    'bbox_center_x_after':after['bbox_center_x']})
    frames.append(aligned)
strip = Image.new('RGB',(512*16,512),'#3a3f4a')
for number,frame in enumerate(frames):
    tile = Image.new('RGBA',(512,512),'#3a3f4a')
    tile.alpha_composite(frame)
    strip.paste(tile.convert('RGB'),(number*512,0))
    ImageDraw.Draw(strip).text((number*512+12,12),f'{number:02d}',fill='#ffffff')
strip.save(out / 'sheets/idle_S_strip.png')
report = {'task_id':'K3p-reg-01','transform_source':str(transform_path),'transform':transform,
          'raster_scale_effective':320/627,'operations':'Matte each native cell; LANCZOS 627 to 320; paste at (96,112); integer translation only.',
          'alpha_bbox_convention':'alpha > 0; exclusive right/bottom; pixel-centre x = (left+right-1)/2',
          'sole_convention':'bottom-most row with alpha >=128',
          'horizontal_rounding':'If absolute centre difference >2, round difference to nearest integer, half away from zero.',
          'target_sole_line':target_sole,'target_bbox_center_x':target_x,
          'atlas_pivot':[256,400],'pivot_note':'Declared canvas pivot; sole alignment uses measured frame-0 sole, not a new anchor fit.',
          'seed_persistence_max_abs_delta':max(x['matted_rgba_max_abs_delta'] for x in seed_persistence),
          'seed_persistence':seed_persistence,
          'seed_noise_note':'No matte-noise tolerance was supplied. Differences >2 in RGB at mutually opaque pixels are conservatively flagged as beyond edge matte noise; all raw metrics retained.',
          'cell_edge_checks':edge_checks,'frames':records,'concerns':concerns}
(out / 'registration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'target_sole_line':target_sole,'offsets':[x['offsets_applied']['integer_alignment_xy'] for x in records], 'seed_persistence_max_abs_delta':report['seed_persistence_max_abs_delta'],'concerns':concerns},indent=2))
PY
