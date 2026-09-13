K3p-cmp-01 — frozen-tool composition and measurements

Base: seed slot 0, crop (0,0,627,627), character matte with alpha_floor=40
and preserve_particles=False; requested scale 0.5106, raster size 320x320
(round(627*0.5106)), LANCZOS. Initial paste (96,112). Integer correction
(dx,dy)=(0,0). Alpha>=128 bbox=(210,160,302,400), height 240 px,
centre-x 255.5, sole row 399. Frame 00 is a byte-identical copy of this base.
Pillow's integer dimensions imply effective raster ratio 320/627;
the specified scale is used to determine those dimensions.

Region (exclusive XYXY): (210,160,302,292).
Belt bound: bbox top + round(0.55*bbox height) = 292.
Frozen defaults: thresh=8; dilate_px=2. Strict difference > 8,
square Chebyshev dilation, clipped to the region after dilation.
Each variant uses the same seed-derived base.

G12: all 16 preservation fractions are 1.0. Frame 00 uses an empty mask.
Frames 01–15 mask-figure fractions range 0.5019643673–0.5497487437;
frame 00 is 0.0. Registered limits remain >=0.99 preservation and <=0.60 coverage.

Original / composited seam MAD: 0.4681358337402344 / 0.37044016520182294.
Original / composited literal G6 threshold: 0.11506398518880208 / 0.08031590779622395.
Original / composited G6b threshold: 0.44507471720377606 / 0.3434638977050781.
G6c uses the frozen idle fallback to G6b. All literal instruments are retained.
Only frozen tools assign comparison booleans in the envelopes.

G11 concern: no cast05 reference was supplied. The frozen drift48.evaluate
requires it to compute the G11 threshold, so its two envelopes retain null
comparison values and the explicit UNEVALUABLE reason. Every adjacent pair,
including 15->00, is separately measured at 48x48 with LANCZOS and the frozen
common.pair_differences comparator. All 16 original-to-seed-base drifts are
also reported through the frozen common.difference comparator at 48x48.
These descriptive envelopes have null thresholds and comparison booleans.
No substitute threshold or cast reference is used.

checks.json is a flat list of 73 SPEC section 1 result envelopes.
Per-pair notes include both canvas MAD and foreground-union MAD.
G6 measurements use full-resolution frames; G11 measurements use 48x48.
All comparisons use the frozen comparator's RGB(20,25,34) background.

Strip: 8192x1024 RGB, background #3a3f4a, unchanged 512px cells.
Top row: ORIGINAL K3p-reg-01 frames 00–15, including re-rendered original 00.
Bottom row: COMPOSITED 00–15, with seed-derived base at 00.
Columns increase left to right. No frame resizing, mirroring, or per-frame
registration is performed during compositing. Inputs and tools stay read-only.
No image calls and no executable code files were created.

Exact processing command (run in /Users/admin/astra-burst/runs/C-1/K3p-cmp-01):
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys, json, shutil, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from gates import matte, mask_composite, drift48, g6_seam, common
root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
source = root / 'runs/C-1/artifacts/K3p-reg-01/frames/idle/S'
seed_path = root / 'runs/C-1/artifacts/K3p-seed/canvas_idle_S_seed.png'
out = Path('out')
for directory in ('base', 'composited', 'strips'):
    (out / directory).mkdir(parents=True, exist_ok=True)
original_paths = [source / f'idle_S_{k:02d}.png' for k in range(16)]
original = [common.rgba(p) for p in original_paths]
assert all(im.size == (512, 512) for im in original)
with Image.open(seed_path) as seed:
    assert seed.size == (1254, 1254)
    crop = seed.crop((0, 0, 627, 627))
extracted, matte_info = matte.extract(crop, preserve_particles=False, alpha_floor=40)
scale = 0.5106
size = round(627 * scale)
assert size == 320
small = extracted.resize((size, size), Image.Resampling.LANCZOS)
initial = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
initial.paste(small, (96, 112))
before = common.measure(initial)
box = before['bbox']
center_x = (box[0] + box[2] - 1) / 2
dx = round(255.5 - center_x) if abs(center_x - 255.5) > 2 else 0
dy = 399 - (box[3] - 1)
base = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
base.paste(initial, (dx, dy))
after = common.measure(base)
assert after['bbox'][3] - 1 == 399
assert after['height'] == before['height']
base_path = out / 'base/idle_S_base.png'
base.save(base_path)
frame0_path = out / 'composited/idle_S_00.png'
shutil.copyfile(base_path, frame0_path)
x0, y0, x1, y1 = after['bbox']
belt_y = y0 + round(0.55 * (y1 - y0))
region = [x0, y0, x1, belt_y]
records = [common.result('seed_base_registration', 'base/idle/S', after['height'], unit='px',
    notes=json.dumps({'reason': 'Descriptive registration measurement; no scalar gate assigned',
    'source': str(seed_path), 'source_sha256': hashlib.sha256(seed_path.read_bytes()).hexdigest(),
    'crop_xyxy': [0, 0, 627, 627], 'matte': matte_info,
    'requested_uniform_scale': scale, 'raster_resize_px': [size, size],
    'raster_effective_scale': size / 627, 'resampling': 'LANCZOS',
    'initial_paste_xy': [96, 112], 'integer_translation_xy': [dx, dy],
    'final_paste_xy': [96 + dx, 112 + dy], 'bbox_alpha_threshold': 128,
    'before': before, 'after': after, 'sole_row': after['bbox'][3] - 1,
    'region_box_xyxy_exclusive': region, 'belt_definition': 'bbox top + round(0.55 * bbox height)',
    'thresh': 8, 'dilate_px': 2, 'min_preserved_fraction': 0.99,
    'max_mask_figure_fraction': 0.60}, sort_keys=True), evidence=[str(base_path)])]
composited = [base]
zero_mask = np.zeros((512, 512), dtype=bool)
r = mask_composite.evaluate(base, base, zero_mask, subject='composited/idle/S/00')
r['evidence'] = [str(base_path), str(frame0_path)]
records.append(r)
for k, (im, mask, metrics) in enumerate(mask_composite.compose_loop(base, original[1:], [region] * 15), 1):
    path = out / 'composited' / f'idle_S_{k:02d}.png'
    im.save(path)
    composited.append(im)
    r = mask_composite.evaluate(base, im, mask, subject=f'composited/idle/S/{k:02d}')
    r['notes'] = json.dumps(dict(json.loads(r['notes']), composite=metrics), sort_keys=True)
    r['evidence'] = [str(base_path), str(original_paths[k]), str(path)]
    records.append(r)
for name, frames in [('original', original), ('composited', composited)]:
    subject = f'{name}/idle/S'
    r = drift48.evaluate(frames, subject=subject)
    r['notes'] += '; cast05 not supplied; no G11 comparison threshold can be computed. All adjacent and seam measurements are reported separately using the frozen comparator.'
    records.append(r)
    reduced = [im.resize((48, 48), Image.Resampling.LANCZOS) for im in frames]
    pairs = common.pair_differences(reduced)
    for k, metrics in enumerate(pairs):
        records.append(common.result('g11_drift48_pair', f'{subject}/{k:02d}->{(k+1)%16:02d}',
            metrics['canvas'], unit='rgb_mad',
            notes=json.dumps({'reason': 'Measurement only; no cast05 supplied for G11 threshold',
                'pair': [k, (k+1)%16], 'seam': k == 15, 'metrics': metrics,
                'reduction': '48x48 LANCZOS RGBA; frozen common comparator on RGB(20,25,34)'}),
            evidence=[str(out / 'strips/original_vs_composited.png')]))
    records.extend(g6_seam.evaluate(frames, subject=subject))
    records.append(g6_seam.g6c(frames, subject=subject, animation='idle'))
base48 = base.resize((48, 48), Image.Resampling.LANCZOS)
for k, im in enumerate(original):
    metrics = common.difference(im.resize((48, 48), Image.Resampling.LANCZOS), base48)
    records.append(common.result('original_vs_seed_base_drift48', f'original/idle/S/{k:02d}',
        metrics['canvas'], unit='rgb_mad',
        notes=json.dumps({'reason': 'Descriptive original-to-approved-base measurement; no gate threshold assigned',
            'metrics': metrics, 'reduction': '48x48 LANCZOS RGBA; frozen common comparator on RGB(20,25,34)'}),
        evidence=[str(original_paths[k]), str(base_path)]))
strip = Image.new('RGBA', (512 * 16, 512 * 2), '#3a3f4a')
for row, frames in enumerate((original, composited)):
    for col, im in enumerate(frames):
        strip.alpha_composite(im, (col * 512, row * 512))
strip.convert('RGB').save(out / 'strips/original_vs_composited.png')
(out / 'checks.json').write_text(json.dumps(records, indent=2, allow_nan=False) + '\n')
print(json.dumps({'base_bbox': after['bbox'], 'height': after['height'], 'translation': [dx, dy],
    'region': region, 'g12': [{'subject': r['subject'], 'preserved': r['value'],
    'mask_figure_fraction': json.loads(r['notes'])['mask_figure_fraction']} for r in records if r['id']=='g12_base_preservation'],
    'seams': [{key: r[key] for key in ('id','subject','value','threshold')} for r in records if r['id'] in ('g6_seam','g6b','g6c')],
    'drift48_pairs': {name: [r['value'] for r in records if r['id']=='g11_drift48_pair' and r['subject'].startswith(name)] for name in ('original','composited')},
    'original_vs_base_drift48': [r['value'] for r in records if r['id']=='original_vs_seed_base_drift48'],
    'record_count': len(records)}, indent=2))
PY

Exact output verification and SHA-256 command:
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json, hashlib
from pathlib import Path
from PIL import Image
out = Path('out')
records = json.loads((out / 'checks.json').read_text())
fields = {'id','subject','passed','value','threshold','op','unit','evidence','notes'}
assert len(records) == 73 and all(set(r) == fields for r in records)
assert (out / 'base/idle_S_base.png').read_bytes() == (out / 'composited/idle_S_00.png').read_bytes()
for path in [out / 'base/idle_S_base.png'] + sorted((out / 'composited').glob('*.png')):
    with Image.open(path) as im:
        assert im.size == (512, 512) and im.mode == 'RGBA'
with Image.open(out / 'strips/original_vs_composited.png') as im:
    assert im.size == (8192, 1024) and im.mode == 'RGB'
assert sum(r['id']=='g12_base_preservation' for r in records) == 16
assert sum(r['id']=='g11_drift48_pair' for r in records) == 32
assert sum(r['id']=='original_vs_seed_base_drift48' for r in records) == 16
assert sum(r['id'] in ('g6_seam','g6b','g6c') for r in records) == 6
paths = sorted(p for p in out.rglob('*') if p.is_file() and not p.name.startswith('.wrapper-'))
assert len(paths) == 20
print(json.dumps([{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths], indent=2))
PY

Verification note: the initial file-count check included two live wrapper-owned logs,
out/.wrapper-events.jsonl and out/.wrapper-stderr.txt. These are not task artifacts
and may change while the burst runs. The verification below excludes .wrapper-*
files. Their hashes are not included in the receipt; all 20 requested artifacts are.
