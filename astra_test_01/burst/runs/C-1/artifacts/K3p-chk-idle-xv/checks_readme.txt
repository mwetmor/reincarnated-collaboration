K3p-chk-idle-xv — step 8, X-video relaxed idle process test (R-42)
All 16 named input frames were measured directly. No input pixels or frozen source files were changed.
checks.json is a list of 72 SPEC section 1 result envelopes, including both complete idle_intent payloads, three seam instruments, G11 availability plus all 16 pair measurements, 16 G1 comparisons, 16 silhouette distances, 16 alpha-bbox records, height spread and sole spread.

Frozen-tool output-path workaround:
oracle.idle_bands --ours ignores --out and writes to module constant OURS_ROOT. The unchanged main function was invoked with OURS_ROOT configured in memory to this workdir's out directory. Its generated idle_S_xv_ours.json was renamed within out to idle_S_xv_measure.json. No repository write was attempted. No frozen implementation was edited.
Bytecode writing was disabled.

Instrument limitations:
- G11 numeric measurements include every adjacent pair and closure, using exactly drift48's 48px LANCZOS RGBA reduction and frozen common.pair_differences. The frozen drift48 evaluator was also called; its comparison verdict is null because the required cast05 input was not supplied. No comparator was invented.
- Silhouette distances and contour/Hu diagnostics were computed; verdicts are null because no calibrated silhouette threshold was supplied.
- The oracle could not estimate breath period (frames and seconds are null, confidence 0). Its estimator requires sufficient cycle evidence.
- idle_intent uses the unmodified band rows and its frozen fps selection (12 fps for these rows); oracle CLI measurement uses the requested 8 fps. Reported displacement amplitudes and region classifications do not depend on that fps choice.
- G6c for idle is the frozen fallback to G6b, not the walk half-cycle instrument.
- Sole line is the bottommost alpha>=128 supported row (bbox exclusive bottom minus one); it is not a reviewed per-boot trajectory or root anchor. The full pairwise sole-band mask distance is in idle_intent.
- Oracle plot shading comes from the candidate's measured amplitude as implemented by the frozen plotter. Committed band comparisons are in the intent envelopes.
- Receipt inventories authored output artifacts. Hidden .wrapper-* files are live conductor-owned logs, not static deliverables.

Numeric observations (no conductor verdict):
H = 240 px (clip-wide union). Relaxed breath = 0.004141131124248132 H versus floor 0.01958382, target 0.0326397, ceiling 0.04895956 H.
Head bob = 0.019425583799634223 H versus floor 0, target 0.006, ceiling 0.012 H.
Sole mask displacement = 0.004166666666666667 H versus 0.0025 H.
Height spread = 3 px; sole-line spread = 0 px.
Seam MAD = 0.5969734191894531; minimum internal = 0.13275527954101562; median internal = 0.41462453206380206.
Geometric regions: LOCK legs/feet; MOTION head/shoulders_chest/hips/arms_left/arms_right.
Contamination = 0. Full figure drift and per-region search-limit diagnostics are preserved in checks.json.

Exact measurement command, run from /Users/admin/astra-burst/runs/C-1/K3p-chk-idle-xv:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 -B - <<'PY'
import json
from pathlib import Path
from PIL import Image
from gates import idle_intent, g6_seam, drift48, g1_height, silhouette64
from gates.common import result, rgba, measure, pair_differences
from oracle import idle_bands
from oracle.motion_map import frame_paths

frames_dir = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts/K3p-xv-idle-cut-01/frames/idle/S')
bands_path = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/oracle/bands_idle.json')
bands = json.loads(bands_path.read_text())
paths = frame_paths(frames_dir)
assert [p.name for p in paths] == [f'idle_S_{i:02d}.png' for i in range(16)]
frames = [rgba(p) for p in paths]
assert all(f.size == (512,512) for f in frames)
out = Path('out')
out.mkdir(exist_ok=True)
rows = [idle_intent.evaluate(frames_dir, bands[name], 'idle/S/xv/'+name) for name in ('relaxed','combat')]
rows += g6_seam.evaluate(frames, 'idle/S/xv')
rows.append(g6_seam.g6c(frames, 'idle/S/xv', animation='idle'))
rows.append(drift48.evaluate(frames, subject='idle/S/xv'))
small = [f.resize((48,48), Image.Resampling.LANCZOS) for f in frames]
pairs = pair_differences(small)
rows += [result('drift48_pair', f'idle/S/xv/{i:02d}->{(i+1)%16:02d}', pair['canvas'], unit='rgb_mad', notes=json.dumps({'foreground_union_mad':pair['foreground_union'],'method':'frozen drift48 reduction (48px LANCZOS RGBA), gates.common.pair_differences dark composite','unevaluable_comparator':'cast05 was not supplied; numeric measurement only'})) for i,pair in enumerate(pairs)]
rows += [g1_height.evaluate(f, frames[0], f'idle/S/xv/{i:02d}->00') for i,f in enumerate(frames)]
rows += [silhouette64.evaluate(f, frames[0], f'idle/S/xv/{i:02d}->00') for i,f in enumerate(frames)]
measures = [measure(f) for f in frames]
heights = [m['height'] for m in measures]
soles = [m['bbox'][3]-1 for m in measures]
rows += [result('alpha_bbox', f'idle/S/xv/{i:02d}', {'bbox_xyxy_exclusive':m['bbox'],'height_px':m['height'],'sole_line_y':m['bbox'][3]-1}, unit='px', notes='Descriptive; alpha >=128; sole line is bottommost supported row, not an annotated per-boot contact or root anchor.') for i,m in enumerate(measures)]
rows.append(result('height_spread', 'idle/S/xv', max(heights)-min(heights), unit='px', notes=json.dumps({'minimum':min(heights),'maximum':max(heights),'per_frame':heights,'verdict':'descriptive; no separate spread threshold supplied'})))
rows.append(result('sole_spread', 'idle/S/xv', max(soles)-min(soles), unit='px', notes=json.dumps({'minimum':min(soles),'maximum':max(soles),'per_frame':soles,'verdict':'descriptive; feet-lock mask displacement is separately evaluated by idle_intent'})))
(out/'checks.json').write_text(json.dumps(rows, indent=2, allow_nan=False)+'\n')
idle_bands.OURS_ROOT = out.resolve()
idle_bands.main(['--ours',str(frames_dir),'--fps','8','--label','idle_S_xv','--out','out/idle_S_xv_measure.json','--plot_dir','out/plots'])
(out/'idle_S_xv_ours.json').rename(out/'idle_S_xv_measure.json')
print(json.dumps({'envelopes':len(rows),'intent':[{k:r['value'][k] for k in ['breath','head_bob','sole_displacement_H','classification','contamination']} for r in rows[:2]],'seams':[{k:r[k] for k in ['id','value','threshold','passed']} for r in rows[2:5]],'height_spread_px':max(heights)-min(heights),'sole_spread_px':max(soles)-min(soles)}, allow_nan=False))
PY

