# Conductor P4 CHECK glue (the C-3 P4c brief STEP 2, run by the conductor because Astra is halted): FROZEN gates, REPORT ONLY.
# usage: p4_check.py <cell e.g. E_walk> <cut_dir e.g. runs/C-6/p4/E_walk/cut> [<band_row e.g. walk_E_video>]  → <cut_dir>/../checks.json + grid.png
import sys, json, glob, pathlib, traceback
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from PIL import Image, ImageDraw
import numpy as np
from oracle import bands_from_exemplar as bfe
from gates import g6_seam, g1_height, head_pitch, coherence, matte_quality, common
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
cell, cut = sys.argv[1], B/sys.argv[2]; d, a = cell.split('_')[0], cell.split('_')[1]; row_label = sys.argv[3] if len(sys.argv) > 3 else None
reg = json.load(open(cut/'registration.json')); frames_dir = cut/'frames'/a/d; frames = sorted(glob.glob(str(frames_dir/'*.png'))); rest = str(cut/'frames'/'rest'/d/f'rest_{d}.png')
fps = reg.get('fps_out') or 12
out = dict(cell=cell, clip=reg.get('clip'), clip_sha256=reg.get('clip_sha256'), tool_sha256=reg.get('tool_sha256'), flags=[], cut={k: reg.get(k) for k in ('period','selection','detection','splice','transform','wall_seconds','indices_native')}, results=[], concerns=[])
def env(id_, **kw): e = common.result(id_, cell, **kw); out['results'].append(e); return e
def guard(fn, id_):
    try: return fn()
    except Exception as ex: env(id_, value=None, passed=None, notes=f'EXC {type(ex).__name__}: {ex}'); return None
if not frames:
    out['flags'].append('no frames cut'); json.dump(out, open(cut.parent/'checks.json','w'), indent=1); print(cell, 'NO FRAMES'); raise SystemExit
if reg.get('period', {}).get('source') == 'sibling': out['flags'].append('period from sibling/prompted stride (charter fallback) — FLAGGED')
# a) bands measure + proposed-row score (passed forced null: PROPOSED rows are report, never verdict)
def a_():
    values, diag = bfe.measure(a, str(frames_dir), fps); env('bands_measure', value=values, passed=None, notes=json.dumps(diag)[:800])
    rows = json.load(open(B/'oracle/bands_proposed.json')); label = row_label
    if label is None:
        cand = [k for k in rows if k.startswith(f'{a}_{d}_')] or [k for k in rows if k.startswith(f'{a}_')]
        label = cand[0] if cand else None
    if label and rows[label].get('quantities'):
        sc = bfe.score(values, rows[label], subject=cell)
        for e in (sc if isinstance(sc, list) else [sc]):
            if isinstance(e, dict): e['passed'] = None; e['notes'] = (e.get('notes') or '') + f' | scored against PROPOSED row {label}' + ('' if label.startswith(f'{a}_{d}_') else ' (nearest proposal, not this facing)'); out['results'].append(e)
    else: env('bands_score', value=None, passed=None, notes=f'no proposed row with quantities for {a}/{d} — measure only')
guard(a_, 'bands_measure')
guard(lambda: [out['results'].append(dict(e, passed=None)) for e in ([g6_seam.evaluate(frames, subject=cell)] if isinstance(g6_seam.evaluate(frames, subject=cell), dict) else g6_seam.evaluate(frames, subject=cell))], 'g6_seam')
guard(lambda: out['results'].append(dict(g6_seam.g6c(frames, subject=cell, animation=a), passed=None)), 'g6c')
def c_():
    vals = [g1_height.evaluate(f, rest, subject=cell)['value'] for f in frames]; env('g1_size_stability', value=max(v for v in vals if v is not None), passed=None, unit='fraction', notes=json.dumps([round(v,4) if v is not None else None for v in vals]))
guard(c_, 'g1_size_stability')
guard(lambda: out['results'].append(dict(head_pitch.evaluate(frames, rest, fps=fps), passed=None)), 'head_pitch')
guard(lambda: out['results'].append(dict(coherence.evaluate(str(frames_dir), None), passed=None)) if isinstance(coherence.evaluate(str(frames_dir), None), dict) else [out['results'].append(dict(e, passed=None)) for e in coherence.evaluate(str(frames_dir), None)], 'coherence')
def f_():
    vals = []
    for f in frames:
        r = matte_quality.rim_luma_excess(common.rgba(Image.open(f))); vals.append(r['value'] if isinstance(r, dict) else float(r))
    env('rim_luma_excess_mean', value=float(np.mean([v for v in vals if v is not None])), passed=None, notes=json.dumps([round(v,4) for v in vals if v is not None]))
guard(f_, 'rim_luma_excess')
def g_():
    def mad(p, q):
        A = np.asarray(Image.open(p).convert('RGBA')).astype(float); Bm = np.asarray(Image.open(q).convert('RGBA')).astype(float)
        w = np.maximum(A[...,3], Bm[...,3])/255.0; return float((np.abs(A[...,:3]-Bm[...,:3]).mean(2)*w).sum()/max(w.sum(),1))
    env('closure_first_last', value=mad(frames[0], frames[-1]), passed=None, unit='rgb_mad'); env('closure_last_rest', value=mad(frames[-1], rest), passed=None, unit='rgb_mad')
guard(g_, 'closure')
# grid sheet
tiles = [Image.open(f).convert('RGBA') for f in frames]; n = len(tiles); cols = 4; rows_ = (n+cols-1)//cols; C = 256
grid = Image.new('RGB', (cols*C, rows_*C), (58,63,74)); dr = ImageDraw.Draw(grid)
for i, t in enumerate(tiles):
    t2 = t.copy(); t2.thumbnail((C-8, C-8)); grid.paste(t2, ((i%cols)*C+4, (i//cols)*C+4), t2); dr.text(((i%cols)*C+6, (i//cols)*C+4), str(i), fill='white')
grid.save(cut.parent/'grid.png'); json.dump(out, open(cut.parent/'checks.json','w'), indent=1)
print(cell, 'frames', n, '| flags', out['flags'], '| envelopes', len(out['results']), '| exceptions', sum(1 for e in out['results'] if str(e.get('notes','')).startswith('EXC')))
for e in out['results']: print('  ', e.get('id'), '=', (round(e['value'],4) if isinstance(e.get('value'), float) else (e.get('value') if not isinstance(e.get('value'), dict) else '{…}')), '|', str(e.get('notes',''))[:90])
