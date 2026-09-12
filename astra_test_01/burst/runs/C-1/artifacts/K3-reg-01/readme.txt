K3-reg-01 registration
All writes are under out/. No image generation.
Frozen matte: /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/gates/matte.py
Character mode: preserve_particles=False, alpha_floor=40, matte before resize.
Uniform scale 0.5106: round(627 * 0.5106) = 320. Every cell uses LANCZOS 320x320, then an unmasked paste at (96,112) into a transparent 512x512 canvas. No fitting, per-frame scale, upscaling, or corrective translation.
Pivot metadata: (256,400), fixed. Sole measurements are independent.
Idle frame 7 is a byte-identical file copy of idle frame 0. Idle sheet 2 slot 0 is intentionally omitted.
Preview strips: eight original 512x512 frames side by side, composited on #3a3f4a, with a 32-pixel label band below (4096x544). Preview composites do not alter delivered frame files.
Alpha bboxes use alpha > 0 and half-open bounds; sole line is the zero-based bottom-most alpha row. Alpha >= 128 measurements are separately included. Native cell-edge contact is measured after frozen matting, before resizing.
Concerns: walk_S_07 touches the top of its native cell. Idle sole lines: 402,402,401,402,402,399,399,402 (3 px span). Walk sole lines: 427,426,422,417,429,429,404,420 (25 px span). The registration JSON records every frame whose sole line differs from any other delivered frame by more than 4 px, including cross-animation comparisons. No gate verdict is issued.

Exact registration command (run from /Users/admin/astra-burst/runs/C-1/K3-reg-01):
python3 -B - <<'PY'
import sys, json, shutil
from pathlib import Path
from PIL import Image, ImageDraw
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates.matte import extract

base = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts')
transform_path = base / 'K3-seed/registration_transform.json'
transform = json.loads(transform_path.read_text())
assert transform['cell_px'] == 627
assert transform['scale'] == 0.5106
assert transform['scaled_cell_px'] == round(627 * 0.5106) == 320
assert transform['offset_xy'] == [96, 112]
assert transform['frame_canvas'] == 512
sources = {
    'idle1': base / 'K3-gen-idle-01/k3_idle_S_00_03.png',
    'idle2': base / 'K3-gen-idle-02/k3_idle_S_04_06.png',
    'walk1': base / 'K3-gen-walk-01/k3_walk_S_00_03.png',
    'walk2': base / 'K3-gen-walk-02/k3_walk_S_04_07.png'
}
sheets = {}
for key, path in sources.items():
    with Image.open(path) as im:
        assert im.size == (1254, 1254), (str(path), im.size)
        sheets[key] = im.copy()
mapping = {
    'idle': [('idle1', i) for i in range(4)] + [('idle2', i) for i in range(1, 4)] + [('idle1', 0)],
    'walk': [('walk1', i) for i in range(4)] + [('walk2', i) for i in range(4)]
}
out = Path('out')
(out / 'sheets').mkdir(parents=True, exist_ok=True)
records = []
for animation, slots in mapping.items():
    target = out / 'frames' / animation / 'S'
    target.mkdir(parents=True, exist_ok=True)
    strip = Image.new('RGB', (512 * 8, 544), '#3a3f4a')
    draw = ImageDraw.Draw(strip)
    for index, (key, slot) in enumerate(slots):
        name = f'{animation}_S_{index:02d}'
        path = target / (name + '.png')
        left, top = (slot % 2) * 627, (slot // 2) * 627
        crop_box = (left, top, left + 627, top + 627)
        cell = sheets[key].crop(crop_box)
        matted, details = extract(cell, preserve_particles=False, alpha_floor=40)
        source_bbox = matted.getchannel('A').getbbox()
        assert source_bbox is not None
        edges = [edge for edge, hit in [
            ('left', source_bbox[0] == 0), ('top', source_bbox[1] == 0),
            ('right', source_bbox[2] == 627), ('bottom', source_bbox[3] == 627)
        ] if hit]
        scaled = matted.resize((320, 320), Image.Resampling.LANCZOS)
        frame = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
        frame.paste(scaled, (96, 112))
        if animation == 'idle' and index == 7:
            shutil.copyfile(target / 'idle_S_00.png', path)
            with Image.open(path) as im:
                assert frame.tobytes() == im.tobytes()
        else:
            frame.save(path)
        alpha = frame.getchannel('A')
        bbox = alpha.getbbox()
        opaque_bbox = alpha.point(lambda value: 255 if value >= 128 else 0).getbbox()
        record = {
            'name': name, 'path': str(path), 'animation': animation, 'direction': 'S', 'frame_index': index,
            'source_sheet': str(sources[key]), 'source_slot': slot, 'slot_order': 'row-major',
            'source_crop_xyxy': list(crop_box), 'source_matted_alpha_bbox': list(source_bbox),
            'source_cell_edge_contacts': edges, 'alpha_bbox': list(bbox),
            'alpha_bbox_height_px': bbox[3] - bbox[1], 'sole_line': bbox[3] - 1,
            'alpha_ge_128_bbox': list(opaque_bbox),
            'alpha_ge_128_height_px': opaque_bbox[3] - opaque_bbox[1],
            'alpha_ge_128_sole_line': opaque_bbox[3] - 1,
            'root_anchor_xy': [256, 400], 'matte': dict(details, preserve_particles=False, mode='character', before_downscale=True),
            'transform': {'scale': 0.5106, 'scaled_cell_px': 320, 'offset_xy': [96, 112], 'canvas_px': [512, 512], 'resample': 'LANCZOS'}
        }
        if animation == 'idle' and index == 7:
            record['byte_identical_copy_of'] = 'out/frames/idle/S/idle_S_00.png'
        records.append(record)
        strip.paste(frame, (512 * index, 0), frame)
        draw.text((512 * index + 12, 520), name, fill='#ffffff')
    strip.save(out / 'sheets' / f'{animation}_S_strip.png')
concerns = []
for record in records:
    different = [other['name'] for other in records if abs(record['sole_line'] - other['sole_line']) > 4]
    record['sole_line_differs_by_more_than_4_px_from'] = different
    if record['source_cell_edge_contacts']:
        concerns.append(record['name'] + ': matted figure touches cell edge(s): ' + ', '.join(record['source_cell_edge_contacts']))
    if different:
        concerns.append(record['name'] + ': sole line ' + str(record['sole_line']) + ' differs by more than 4 px from ' + ', '.join(different))
summary = {}
for animation in mapping:
    values = [r['sole_line'] for r in records if r['animation'] == animation]
    summary[animation] = {'sole_lines': values, 'sole_line_min': min(values), 'sole_line_max': max(values), 'sole_line_span_px': max(values) - min(values)}
registration = {
    'task_id': 'K3-reg-01', 'transform_source': str(transform_path),
    'transform': transform,
    'measurement_conventions': {
        'alpha_bbox': 'alpha > 0, half-open [left, top, right, bottom], in 512x512 canvas',
        'sole_line': 'zero-based bottom-most alpha > 0 row; bbox bottom minus one; includes Lanczos alpha fringes',
        'alpha_ge_128': 'additional opaque-support measurements, explicitly separate from alpha > 0',
        'edge_contact': 'any nonzero alpha touching a native 627x627 cell edge after frozen matting, before resizing',
        'sole_comparison': 'all delivered frames compared pairwise; flag each frame with any difference greater than 4 px',
        'root_anchor': 'fixed atlas pivot metadata; sole trajectory reported separately, no corrective translations',
        'integer_resize': 'round(627 * 0.5106) = 320, as specified by the frozen transform; identical for every frame'
    },
    'summary': summary, 'frames': records, 'concerns': concerns
}
(out / 'registration.json').write_text(json.dumps(registration, indent=2) + '\n')
assert (out / 'frames/idle/S/idle_S_00.png').read_bytes() == (out / 'frames/idle/S/idle_S_07.png').read_bytes()
print(json.dumps({'summary': summary, 'cell_edge_contacts': {r['name']: r['source_cell_edge_contacts'] for r in records if r['source_cell_edge_contacts']}, 'concerns': concerns}, indent=2))
PY

Exact verification and SHA-256 census command:
python3 -B - <<'PY'
import json, hashlib
from pathlib import Path
from PIL import Image
root = Path('out')
registration = json.loads((root / 'registration.json').read_text())
assert len(registration['frames']) == 16
for record in registration['frames']:
    with Image.open(record['path']) as im:
        assert im.size == (512, 512) and im.mode == 'RGBA'
        bbox = im.getchannel('A').getbbox()
        assert list(bbox) == record['alpha_bbox']
        assert bbox[3] - 1 == record['sole_line']
for animation in ('idle', 'walk'):
    with Image.open(root / 'sheets' / f'{animation}_S_strip.png') as im:
        assert im.size == (4096, 544)
        assert im.getpixel((0, 0)) == (58, 63, 74)
assert (root / 'frames/idle/S/idle_S_00.png').read_bytes() == (root / 'frames/idle/S/idle_S_07.png').read_bytes()
files = [{'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in sorted(root.rglob('*')) if path.is_file()]
assert len(files) == 20
print(json.dumps({'verified_frame_count': 16, 'files': files}, indent=2))
PY

Verification census refinement: the initial command above counted two wrapper-owned .wrapper-* logs and stopped at its file-count assertion after all frame checks completed. Those logs are not delivered artifacts; .wrapper-events.jsonl is live and cannot have a stable receipt hash. They remain untouched and are excluded from the corrected artifact census below.

Exact corrected verification command:
python3 -B - <<'PY'
import json, hashlib
from pathlib import Path
from PIL import Image
root = Path('out')
registration = json.loads((root / 'registration.json').read_text())
assert len(registration['frames']) == 16
for record in registration['frames']:
    with Image.open(record['path']) as im:
        assert im.size == (512, 512) and im.mode == 'RGBA'
        bbox = im.getchannel('A').getbbox()
        assert list(bbox) == record['alpha_bbox']
        assert bbox[3] - 1 == record['sole_line']
for animation in ('idle', 'walk'):
    with Image.open(root / 'sheets' / f'{animation}_S_strip.png') as im:
        assert im.size == (4096, 544)
        assert im.getpixel((0, 0)) == (58, 63, 74)
assert (root / 'frames/idle/S/idle_S_00.png').read_bytes() == (root / 'frames/idle/S/idle_S_07.png').read_bytes()
files = [{'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in sorted(root.rglob('*')) if path.is_file() and not path.name.startswith('.wrapper-')]
assert len(files) == 20
print(json.dumps({'verified_frame_count': 16, 'files': files}, indent=2))
PY
