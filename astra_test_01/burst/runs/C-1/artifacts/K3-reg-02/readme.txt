K3-reg-02 registration packet

All eight frames are 512x512 RGBA. Alpha >= 128 sole rows before:
399, 399, 399, 399, 399, 396, 396, 399.
After: 399 for every frame.
Offsets (dx,dy), frames 00-07:
(0,0), (0,0), (0,0), (0,0), (0,0), (0,3), (0,3), (0,0).
No horizontal alpha-bbox centre differed from frame 0 by more than 2 px.
Frame 07 is byte-identical to frame 00. Maximum translation is 3 px.
Concerns: none.

Frozen gates/register.py and gates/common.py were read. sole_contacts,
measured_anchor and register_reviewed require two reviewed sole regions.
The task-authorized fallback measured the bottom-most alpha >= 128 row directly.
No per-foot contacts were inferred. The atlas root anchor remains (256,400).

Only integer translations were applied, using the task-authorized PIL library.
No resampling, resizing, matting, generation, or frozen-tool modification.
The original uniform reduction is inherited from K3-reg-01.
Unchanged frames were copied byte-for-byte; translated frames used unmasked
PIL paste so RGBA values were preserved. Assertions checked sizes, modes,
sole rows, translated bboxes, subject bytes, alpha histograms, and loop closure.

Preview: out/sheets/idle_S_strip.png, 4096x544 RGB, eight unscaled 512x512
frames on #3a3f4a with frame numbers 00-07 below.

Exact measurement command (run from /Users/admin/astra-burst/runs/C-1/K3-reg-02):
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
from PIL import Image
import hashlib
root=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-01/frames/idle/S')
for i in range(8):
    p=root/f'idle_S_{i:02d}.png'
    im=Image.open(p)
    a=im.getchannel('A')
    b=a.getbbox()
    s=a.point([0]*128+[255]*128).getbbox()
    print(i, im.mode, im.size, 'alpha>0 bbox', b, 'centre_x',(b[0]+b[2]-1)/2, 'alpha>=128 bbox', s, 'sole',s[3]-1, 'sha256',hashlib.sha256(p.read_bytes()).hexdigest())
PY

Exact packing and verification command (same working directory):
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json
import hashlib
import shutil

source = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-01')
out = Path('out')
frames_dir = out/'frames/idle/S'
frames_dir.mkdir(parents=True, exist_ok=True)
(out/'sheets').mkdir(parents=True, exist_ok=True)
prior = json.loads((source/'registration.json').read_text())
lut = [0]*128 + [255]*128
reference = Image.open(source/'frames/idle/S/idle_S_00.png')
reference_bbox = reference.getchannel('A').getbbox()
reference_cx = (reference_bbox[0]+reference_bbox[2]-1)/2
assert reference.getchannel('A').point(lut).getbbox()[3]-1 == 399
assert (source/'frames/idle/S/idle_S_00.png').read_bytes() == (source/'frames/idle/S/idle_S_07.png').read_bytes()
records = []
concerns = []
strip = Image.new('RGBA', (8*512, 544), '#3a3f4a')
draw = ImageDraw.Draw(strip)
for i in range(8):
    name = f'idle_S_{i:02d}'
    src = source/'frames/idle/S'/f'{name}.png'
    dest = frames_dir/f'{name}.png'
    im = Image.open(src)
    assert im.mode == 'RGBA' and im.size == (512,512)
    alpha = im.getchannel('A')
    before_bbox = alpha.getbbox()
    before_support = alpha.point(lut).getbbox()
    sole_before = before_support[3]-1
    cx = (before_bbox[0]+before_bbox[2]-1)/2
    delta = reference_cx-cx
    dx = round(delta) if abs(delta)>2 else 0
    dy = 399-sole_before
    assert isinstance(dx, int) and isinstance(dy, int)
    assert 0 <= before_bbox[0]+dx < before_bbox[2]+dx <= 512
    assert 0 <= before_bbox[1]+dy < before_bbox[3]+dy <= 512
    if dx == 0 and dy == 0:
        shutil.copyfile(src, dest)
    else:
        translated = Image.new('RGBA', (512,512), (0,0,0,0))
        translated.paste(im, (dx,dy))
        translated.save(dest)
    delivered = Image.open(dest)
    after_bbox = delivered.getchannel('A').getbbox()
    after_support = delivered.getchannel('A').point(lut).getbbox()
    assert after_support[3]-1 == 399
    expected_bbox = tuple(v + (dx if j%2 == 0 else dy) for j,v in enumerate(before_bbox))
    assert after_bbox == expected_bbox
    assert im.crop(before_bbox).tobytes() == delivered.crop(after_bbox).tobytes()
    assert alpha.histogram() == delivered.getchannel('A').histogram()
    if max(abs(dx),abs(dy)) > 6:
        concerns.append(f'{name}: translation ({dx}, {dy}) exceeds 6 px on an axis.')
    record = {
        'name': name, 'frame_index': i, 'path': str(dest), 'source': str(src),
        'source_sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
        'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
        'sole_line_before': sole_before, 'sole_line_after': after_support[3]-1,
        'offset_xy': [dx,dy],
        'alpha_bbox_before': before_bbox, 'alpha_bbox_after': after_bbox,
        'alpha_bbox_height_before_px': before_bbox[3]-before_bbox[1],
        'alpha_bbox_height_after_px': after_bbox[3]-after_bbox[1],
        'bbox_centre_x_before': cx,
        'bbox_centre_x_after': (after_bbox[0]+after_bbox[2]-1)/2,
        'alpha_ge_128_bbox_before': before_support,
        'alpha_ge_128_bbox_after': after_support,
        'alpha_ge_128_height_before_px': before_support[3]-before_support[1],
        'alpha_ge_128_height_after_px': after_support[3]-after_support[1],
        'root_anchor_xy': [256,400],
        'pixel_content_preserved_under_integer_translation': True
    }
    records.append(record)
    strip.alpha_composite(delivered, (i*512,0))
    draw.text((i*512+248,520), f'{i:02d}', fill='#ffffff')
assert (frames_dir/'idle_S_07.png').read_bytes() == (frames_dir/'idle_S_00.png').read_bytes()
strip.convert('RGB').save(out/'sheets/idle_S_strip.png')
registration = {
    'task_id': 'K3-reg-02',
    'source_registration': str(source/'registration.json'),
    'source_registration_sha256': hashlib.sha256((source/'registration.json').read_bytes()).hexdigest(),
    'inherited_transform': prior['transform'],
    'additional_scale': 1,
    'resampling': 'none; integer PIL paste without a mask; unchanged frames copied byte-for-byte',
    'frame_canvas_px': [512,512],
    'root_anchor_xy': [256,400],
    'target_sole_line': 399,
    'measurement_conventions': {
        'sole_line': 'zero-based bottom-most row with alpha >= 128',
        'sole_method': 'Derived directly from alpha >= 128 support bbox because frozen sole_contacts, measured_anchor and register_reviewed require two reviewed sole regions; no reviewed regions supplied.',
        'alpha_bbox': 'alpha > 0; half-open [left, top, right, bottom]',
        'bbox_centre_x': '(left + right - 1)/2, centre of included pixel coordinates',
        'horizontal_alignment': 'Only if absolute centre-x difference from frame 0 exceeds 2 px; nearest integer difference, ties-to-even. No frame triggered this condition.',
        'offset_xy': 'integer pixels applied to input; positive x right, positive y down',
        'root_anchor': 'Atlas metadata (256,400), separate from measured sole row; no gate verdict inferred.',
        'preview': '4096x544 RGB, eight unscaled 512x512 frames on #3a3f4a, labels 00-07 in bottom 32-pixel margin'
    },
    'frames': records,
    'summary': {
        'sole_lines_before': [r['sole_line_before'] for r in records],
        'sole_lines_after': [r['sole_line_after'] for r in records],
        'offsets_xy': [r['offset_xy'] for r in records],
        'frame_7_byte_identical_to_frame_0': True,
        'all_frames_512x512_rgba': True,
        'max_absolute_translation_px': max(max(map(abs,r['offset_xy'])) for r in records),
        'visible_pixel_content_and_alpha_histograms_preserved': True
    },
    'concerns': concerns
}
(out/'registration.json').write_text(json.dumps(registration, indent=2)+'\n')
print(json.dumps(registration['summary'], indent=2))
print('concerns:', concerns)
PY
