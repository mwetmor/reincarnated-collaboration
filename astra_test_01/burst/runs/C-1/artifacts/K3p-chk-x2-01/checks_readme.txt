K3p-chk-x2-01 — CHECK, attempt 2 of relaxed idle.
Same seed; exaggeration-language method change. Previous attempt: K3p-chk-01.
Measurements use only the named 16 composited PNGs and frozen tools/bands.
checks.json is a list of SPEC section 1 envelopes emitted by gates.common.result.
No aggregate shipping verdict is assigned.

Execution deviation:
The inspected frozen oracle.idle_bands.main --ours branch ignores --out and
unconditionally writes OURS_ROOT/<label>_ours.json in the repository.
The requested CLI was therefore NOT executed. The unchanged frozen curves,
idle_bands._plots and idle_bands._write functions were called directly, with
the same defaults, alpha union box, 8 fps, and explicit out/ destinations.
No frozen file was modified; Python bytecode writes were disabled.

Interpretation and unavailable quantities:
- Both frozen intent rows were evaluated without changing committed bands.
  Relaxed is the shipping comparison; combat is comparison only.
- Exact relaxed breath band: floor 0.01958382, target 0.0326397,
  ceiling 0.04895956 H. Task prose rounds these values.
- Intent evaluate uses row provenance fps (default 12); oracle curves use 8.
  The row was not mutated. Displacement metrics do not depend on fps.
- Intent breath: 0.03388720912960344 H; head bob: 0 H;
  sole displacement: 0 H; contamination: 0.
  Right arm is classified MOTION where the relaxed row expects LOCK.
- Literal G6 and G6b remain separate; G6c is the frozen idle fallback to G6b.
- G11/48px numeric MAD for every adjacent pair and closure is recorded using
  frozen pair_differences after the exact drift48 LANCZOS RGBA reduction.
  Frozen drift48.evaluate was also called. Its comparison verdict is null
  because the task supplied no cast05 comparator. No comparator was invented.
- Silhouette distances and Hu/contour metrics were computed for all frames;
  verdicts are null because no calibrated threshold was supplied.
- Sole line means bottommost occupied alpha>=128 pixel row, inclusive.
  Heights and sole-line spreads use maximum minus minimum over all frames.
  This is not an independently annotated root or planted anatomical trajectory.
- Oracle head_sway_H is null for the static head; idle_intent's frozen static
  crop check resolves it to zero. Both original outputs are preserved.
- Oracle breath period is null (period_confidence 0); the frozen estimator
  requires sufficient repeated cycles. One supplied loop does not establish it.
- Oracle regional energy classification differs from idle_intent's displacement
  classification by design; neither is substituted for the other.
- Oracle plots include frozen generic provisional/descriptive wording and
  candidate-amplitude shading. Committed acceptance comparisons are in checks.json.

Exact measurement command (run from the workdir):
mkdir -p out
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
from pathlib import Path
from PIL import Image
from gates import idle_intent, g6_seam, drift48, g1_height, silhouette64
from gates.common import rgba, measure, pair_differences, result
from oracle import idle_bands
from oracle.idle_curves import curves
from oracle.motion_map import alpha_box, load_frames, frame_paths
root = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
source = root / 'runs/C-1/artifacts/K3p-cmp-x2-01/composited'
frames = frame_paths(source)
assert [p.name for p in frames] == [f'idle_S_{i:02d}.png' for i in range(16)]
bands = json.loads((root / 'oracle/bands_idle.json').read_text())
label = 'idle_S_K3p'
rows = [idle_intent.evaluate(source, bands[name], label + ':' + name) for name in ('relaxed', 'combat')]
rows.extend(g6_seam.evaluate(frames, label))
rows.append(g6_seam.g6c(frames, label, animation='idle'))
rows.append(drift48.evaluate(frames, subject=label))
small = [rgba(p).resize((48,48), Image.Resampling.LANCZOS) for p in frames]
pairs = pair_differences(small)
rows.extend(result('drift48_pair', f'{frames[i].name}->{frames[(i+1)%16].name}', p, unit='rgb_mad', notes='48px LANCZOS RGBA then frozen dark-background composite; canvas and foreground_union; comparator unavailable: cast05 not supplied') for i,p in enumerate(pairs))
rows.extend(g1_height.evaluate(p, frames[0], p.name) for p in frames)
rows.extend(silhouette64.evaluate(p, frames[0], p.name) for p in frames)
measures = [measure(rgba(p)) for p in frames]
rows.extend(result('alpha_bbox_height', p.name, m['height'], unit='px', notes=json.dumps({'bbox':m['bbox'],'alpha_threshold':128})) for p,m in zip(frames,measures))
rows.extend(result('sole_line', p.name, m['bbox'][3]-1, unit='px', notes='Bottommost occupied alpha>=128 pixel row (inclusive); not reviewed anatomical sole/root annotation') for p,m in zip(frames,measures))
rows.append(result('height_spread', label, max(m['height'] for m in measures)-min(m['height'] for m in measures), unit='px', notes='Maximum minus minimum alpha>=128 bbox height'))
rows.append(result('sole_spread', label, max(m['bbox'][3]-1 for m in measures)-min(m['bbox'][3]-1 for m in measures), unit='px', notes='Maximum minus minimum inclusive sole line; report-only'))
box = alpha_box(source)
data = curves(source, box, 8, ours=True)
data['provenance'] = {'source_note':'own registered sprite: '+str(source), 'frames':data['frames'], 'fps':8, 'box':box, 'tau':data['tau'], 'eps':data['eps'], 'floor':data['floor'], 'calibration_note':idle_bands.CALIBRATION, 'control_box':data['control_box'], 'noise_calibration':data['noise_calibration'], 'estimator':data['estimator'], 'frame_names':[p.name for p in frames], 'invocation_note':'Frozen curves + idle_bands._plots + idle_bands._write API; CLI --ours ignores --out and would write outside out/.'}
data['result']['evidence'] = idle_bands._plots(Path('out/plots'), label, load_frames(source), data)
idle_bands._write(Path('out/idle_S_K3p_measure.json'), data)
rows.append(data['result'])
idle_bands._write(Path('out/checks.json'), rows)
print(json.dumps({'intent':[{'subject':r['subject'],'passed':r['passed'],'breath':r['value']['breath'],'head_bob':r['value']['head_bob'],'classification':r['value']['classification'],'sole_displacement_H':r['value']['sole_displacement_H'],'contamination':r['value']['contamination']} for r in rows[:2]], 'seams':rows[2:5], 'G11':rows[5], 'sole_spread_px':rows[-2]['value'], 'summary':data['summary'], 'null_envelopes':[{'id':r['id'],'subject':r['subject'],'notes':r['notes']} for r in rows if r['value'] is None]}, indent=2))
PY

Exact validation and hash command:
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json, hashlib
from pathlib import Path
from collections import Counter
from PIL import Image
rows = json.loads(Path('out/checks.json').read_text())
required = {'id','subject','passed','value','threshold','op','unit','evidence','notes'}
assert all(set(r) == required for r in rows)
counts = Counter(r['id'] for r in rows)
assert counts['idle_intent'] == 2
assert all(counts[k] == 16 for k in ('drift48_pair','g1_height','silhouette64','alpha_bbox_height','sole_line'))
assert all(counts[k] == 1 for k in ('g6_seam','g6b','g6c','drift48','sole_spread','height_spread'))
data = json.loads(Path('out/idle_S_K3p_measure.json').read_text())
assert data['frames'] == 16 and data['fps'] == 8
for p in Path('out/plots').glob('*.png'):
    with Image.open(p) as im: im.verify()
print(json.dumps({'envelopes':len(rows),'counts':dict(counts),'regions':rows[0]['value']['regions'],'height_and_sole':[{k:r[k] for k in ('id','subject','value')} for r in rows if r['id'] in ('alpha_bbox_height','sole_line','sole_spread','height_spread')],'files':[{'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(Path('out').rglob('*')) if p.is_file()]}, indent=2))
PY
