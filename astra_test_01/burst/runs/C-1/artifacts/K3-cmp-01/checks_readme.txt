K3-cmp-01 — mask composite mechanism test

No loop approval is implied; loops remain unvalidated until the oracle (R-17).
Frozen modules were imported read-only; no source or executable script files were created.
Python bytecode writes were disabled. All artifact writes are under out/.

Inputs: /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-02/frames/idle/S/idle_S_00.png through idle_S_07.png.
Frame 0 is the locked base, copied byte-for-byte. Source frame 7 equals frame 0 in RGBA pixels; composited frame 7 also equals frame 0.

Region: alpha > 0 bbox [209,157,303,403], exclusive XYXY.
Requested geometric belt proxy: 157 + round(0.55 * 246) = 292.
Applied box: [209,157,303,292], exclusive XYXY, fixed across all frames.
composite defaults were used without overrides: thresh=8, dilate_px=2.
Each variant is composited directly onto frame 0; no cumulative compositing, registration, scaling or matting.

checks.json is a flat list of SPEC section 1 envelopes. G12 metrics and composite diagnostics are in each envelope's JSON-encoded notes.
G12 base_preserved_fraction is 1.0 for every frame. Frames 04 and 06 have null passed, because the frozen coverage guard marks them UNEVALUABLE: mask_figure_fraction 0.6102052885021543 and 0.6140069274309369 exceed 0.60. No threshold or region adjustment was made to rescue these results.
Mask area fraction is mask pixels / full canvas; mask figure fraction is mask intersection with base alpha >=128 / base alpha >=128 support.
Frame 00 is an additional identity control. G12 envelopes for 01–07 are the requested measurements.

G11 pair measurements use exactly drift48's documented 48x48 RGBA LANCZOS reduction followed by frozen common.pair_differences. All seven internal pairs and the 7->0 seam are recorded for each loop, with foreground-union MAD in notes. No cast05 reference was supplied: the frozen drift48.evaluate envelopes retain the UNEVALUABLE reason, and pairwise measurements have null threshold/passed. No surrogate cast reference or threshold was introduced.
Original 3->4 canvas MAD: 0.40436921296296297; composited: 0.2977430555555556.
Original 6->7 canvas MAD: 0.5027488425925926; composited: 0.3823784722222222.
The task's contextual 0.503 value matches this input's 6->7 pair, not its 3->4 pair. The contextual 0.462 comparator cannot be reproduced from the named inputs because cast05 was not supplied.
G11 closure MAD is 0.0 for both loops.

G6 and G6b run on full 512x512 frames via frozen g6_seam.evaluate, using its dark comparison background (20,25,34).
Both seam values: 0.0.
Original G6 literal minimum-internal threshold: 0.22975285847981772; G6b median-internal threshold: 1.0075963338216145.
Composited G6 literal threshold: 0.1545842488606771; G6b threshold: 0.7226753234863281.
Literal G6 and G6b remain separate instruments; no shipping-bar ruling is made.

Strip: 4096x1024 RGB; upper row ORIGINAL, lower row COMPOSITED, columns 00 through 07 left to right. Frames placed at native 512x512 without resampling on #3a3f4a. The strip background is for review only, not the gate comparison background.

Exact artifact-generation command, from /Users/admin/astra-burst/runs/C-1/K3-cmp-01:

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B - <<'PY'
from pathlib import Path
import json
import shutil
import hashlib
import numpy as np
from PIL import Image
from gates import mask_composite, drift48, g6_seam
from gates.common import rgba, pair_differences, result

source = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3-reg-02/frames/idle/S')
out = Path('out')
(out / 'composited').mkdir(parents=True, exist_ok=True)
(out / 'strips').mkdir(parents=True, exist_ok=True)
paths = [source / f'idle_S_{k:02d}.png' for k in range(8)]
original = [rgba(p) for p in paths]
assert all(im.size == (512, 512) for im in original)
assert np.array_equal(np.array(original[7]), np.array(original[0])), 'Source frame 7 must equal locked base'
base = original[0]
bbox = base.getchannel('A').getbbox()
x0, y0, x1, y1 = bbox
region_box = (x0, y0, x1, y0 + round(0.55 * (y1 - y0)))
records = []
composited = [base]
shutil.copyfile(paths[0], out / 'composited/idle_S_00.png')
for k in range(8):
    if k == 0:
        frame, mask, metrics = mask_composite.composite(base, base, region_box)
    else:
        frame, mask, metrics = mask_composite.composite(base, original[k], region_box)
        composited.append(frame)
        frame.save(out / f'composited/idle_S_{k:02d}.png')
    envelope = mask_composite.evaluate(base, frame, mask, subject=f'composited/idle/S/{k:02d}')
    details = json.loads(envelope['notes'])
    details.update(composite_metrics=metrics, base_alpha_bbox=list(bbox), alpha_bbox_definition='alpha > 0; XYXY exclusive', belt_rule='y0 + round(0.55 * (y1-y0)); prescribed geometric belt proxy', loop_approval='Unvalidated until oracle; mechanism test only')
    envelope['notes'] = json.dumps(details, sort_keys=True)
    envelope['evidence'] = [f'out/composited/idle_S_{k:02d}.png']
    records.append(envelope)
assert np.array_equal(np.array(composited[7]), np.array(base))
assert (out / 'composited/idle_S_00.png').read_bytes() == paths[0].read_bytes()
for label, frames in [('original', original), ('composited', composited)]:
    missing_comparator = drift48.evaluate(frames, subject=f'{label}/idle/S')
    missing_comparator['evidence'] = ['out/strips/original_vs_composited.png']
    records.append(missing_comparator)
    small = [rgba(im).resize((48, 48), Image.Resampling.LANCZOS) for im in frames]
    pairs = pair_differences(small)
    for k, pair in enumerate(pairs):
        envelope = result('drift48_pair', f'{label}/idle/S/{k:02d}->{(k+1)%8:02d}', value=pair['canvas'], unit='rgb_mad', notes=json.dumps({'definition':'Frozen drift48 reduction: 48x48 RGBA LANCZOS, then common.pair_differences on dark RGB (20,25,34)', 'foreground_union_mad':pair['foreground_union'], 'boundary_3_to_4':k==3, 'seam_7_to_0':k==7, 'reason':'Measurement only; cast05 reference not supplied, so G11 comparison threshold and passed are null'}, sort_keys=True), evidence=['out/strips/original_vs_composited.png'])
        records.append(envelope)
    for envelope in g6_seam.evaluate(frames, subject=f'{label}/idle/S'):
        envelope['evidence'] = ['out/strips/original_vs_composited.png']
        records.append(envelope)
strip = Image.new('RGBA', (4096, 1024), (58, 63, 74, 255))
for row, frames in enumerate([original, composited]):
    for column, frame in enumerate(frames):
        strip.alpha_composite(frame, (column * 512, row * 512))
strip.convert('RGB').save(out / 'strips/original_vs_composited.png')
(out / 'checks.json').write_text(json.dumps(records, indent=2, allow_nan=False) + '\n')
print(json.dumps({'base_alpha_bbox':bbox, 'region_box':region_box, 'G12':[{'subject':r['subject'],'value':r['value'],'passed':r['passed'],'mask_area_fraction':json.loads(r['notes'])['mask_area_fraction'],'mask_figure_fraction':json.loads(r['notes'])['mask_figure_fraction'],'changed_inside_fraction':json.loads(r['notes'])['changed_inside_fraction']} for r in records if r['id']=='g12_base_preservation'], 'G11_pairs':[{'subject':r['subject'],'value':r['value']} for r in records if r['id']=='drift48_pair'], 'G6':[{'id':r['id'],'subject':r['subject'],'value':r['value'],'threshold':r['threshold'],'passed':r['passed']} for r in records if r['id'] in ('g6_seam','g6b')]}, indent=2))
PY

Exact artifact verification and SHA-256 command:

PYTHONDONTWRITEBYTECODE=1 python3 -B - <<'PY'
from pathlib import Path
import hashlib
import json
from PIL import Image

out = Path('out')
records = json.loads((out / 'checks.json').read_text())
keys = {'id', 'subject', 'passed', 'value', 'threshold', 'op', 'unit', 'evidence', 'notes'}
assert len(records) == 30
assert all(set(r) == keys for r in records)
assert all((out.parent / p).is_file() for r in records for p in r['evidence'])
for k in range(8):
    with Image.open(out / f'composited/idle_S_{k:02d}.png') as im:
        assert im.size == (512,512) and im.mode == 'RGBA'
with Image.open(out / 'strips/original_vs_composited.png') as im:
    assert im.size == (4096,1024) and im.mode == 'RGB'
    assert im.getpixel((0,0)) == (58,63,74)
files = [{'path':p.as_posix(), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.rglob('*')) if p.is_file() and not p.name.startswith('.wrapper-')]
assert len(files) == 11
print(json.dumps(files, indent=2))
PY

Verification note: the first file-count assertion included two hidden wrapper-owned runtime logs, so it observed 13 files instead of 11. The final verification above excludes .wrapper-* logs. These live event/stderr logs are not stable deliverables and are omitted from receipt hashes; all 11 requested artifacts are included. No measured artifact was changed for this verification correction.
