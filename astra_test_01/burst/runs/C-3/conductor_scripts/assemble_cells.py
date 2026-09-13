# Conductor assembly for P6 (copy only; no art transformation). Writes runs/C-3/cells/, cells_advanced/, vfx/, matrix_index.json.
import json, shutil, pathlib, glob
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); R = B/'runs/C-3'; A = R/'artifacts'
DIRS = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']; ANIMS = ['idle', 'walk', 'run', 'jump', 'cast']
L = json.load(open(R/'ledger.json')); ok = {b['id'] for b in L['bursts'] if b['exit'] == 0}
PREFER = {('E','walk'):'-g2', ('SW','walk'):'-g2', ('NW','walk'):'-g2', ('SE','run'):'-g2', ('SW','jump'):'-g2', ('NE','cast'):'-v2x', ('NW','cast'):'-v2x', ('NW','jump'):'-v2'}
def src(D, a):
    for suf in ((PREFER[(D,a)],) if (D,a) in PREFER else ()) + ('-x', '-r1', ''):
        if f'P4c-{D}-{a}{suf}' in ok and glob.glob(str(A/f'P4c-{D}-{a}{suf}/cut/frames/{a}/{D}/*_00.png')): return suf
    return None
CFLAGS = {
 'walk_E': ['head down in the first second on v1 → re-generated with the gaze line doubled; re-generation head-up (R-C3-24)'],
 'walk_SW': ['head down on v1 → re-generated; re-generation head-up (R-C3-24)'],
 'walk_W': ['HEAD DOWN in the first second and in frame 0; stride ≈ 2.8 s (≈ 2× other directions). The gaze re-generation is head-up but the cut tool found no cycle in it (70-frame bob) — original kept (second failure)'],
 'walk_NE': ['HEAD DOWN in the first second and frame 0 on BOTH attempts (second failure) — original kept'],
 'walk_NW': ['head down on v1 → re-generated; transcriber: cannot tell (back view)'],
 'run_SE': ['head down on v1 → re-generated; re-generation head-up'],
 'jump_SW': ['head down on v1 → re-generated; re-generation head-up'],
 'run_N': ['first second head-down: cannot tell (back view)'],
 'walk_N': ['first second head-down: cannot tell (back view)'],
 'cast_S': ['raised staff reaches the frame top at gather even from the padded seed; 45 of 89 event frames have no tracked staff tip (staff foreshortened toward the camera); key poses conductor-computed (R-C3-17)'],
 'cast_W': ['noisy staff-tip baseline (tolerance 39.9 px); key poses conductor-computed (R-C3-17)'],
 'cast_NE': ['v2 clip (R-C3-24); gather and release on adjacent native frames 90/91; transcriber: last frame does NOT return to rest; key poses conductor-computed'],
 'cast_NW': ['v2 clip (R-C3-24); key poses conductor-computed'],
 'jump_NW': ['v2 clip (R-C3-24); HEAD DOWN in the first second on BOTH attempts (second failure) — v2 kept; both failures are back three-quarter views: likely a transcriber misread of an averted head, Matt\'s eye rules'], 'walk_NE_note': [],
}
for k in ('cast_E', 'cast_N', 'cast_SE', 'cast_SW'): CFLAGS.setdefault(k, ['key poses conductor-computed from a full-resolution staff-tip series (R-C3-17)'])
for k in ('jump_S', 'jump_E', 'jump_W', 'jump_SE'): CFLAGS.setdefault(k, ['key poses conductor-computed from the tool\'s head/sole series with a floored settle tolerance (R-C3-17)'])
out = R/'cells'; out.mkdir(exist_ok=True); missing = {}; index = {}
Q = json.load(open(R/'matrix_questions.json'))['sets']
for D in DIRS:
    for a in ANIMS:
        cell = f'{a}_{D}'; suf = src(D, a)
        if suf is None:
            reason = 'v1 clip only (v2 re-drive stopped by H-C3-1 Grok balance); the figure exits the frame — ' + ('tracking invalid' if a == 'jump' else 'frozen matte refuses (border green 0.94)') if D == 'NW' and a in ('jump', 'cast') else 'no cut produced'
            missing[cell] = reason; index[cell] = dict(status='INCOMPLETE', reason=reason); continue
        cb = A/f'P4c-{D}-{a}{suf}'; dst = out/cell
        if dst.exists(): shutil.rmtree(dst)
        shutil.copytree(cb/'cut/frames', dst/'frames'); shutil.copyfile(cb/'cut/registration.json', dst/'registration.json')
        pk = A/f'P4p-{D}-{a}{suf}/packet'
        if pk.exists():
            for f in pk.iterdir():
                if f.is_file() and f.suffix in ('.mp4', '.json'): shutil.copyfile(f, dst/f.name)
        chk = json.load(open(cb/'checks.json')); tr = A/f'P4t-{D}-{a}{suf}/answers.json'
        ans = {x['id']: x['answer'] for x in json.load(open(tr))['answers']} if tr.exists() else {}
        items = Q[a]['items'] + [{'id': 'first_second_head_down', 'expected': 'no', 'class': 'motion'}]
        mism = [i['id'] for i in items if i['class'] == 'motion' and i['id'] in ans and ans[i['id']] != i['expected']]
        ctrl = all(ans.get(i['id']) == 'no' for i in items if i['class'] == 'declared_absent_control') if ans else None
        index[cell] = dict(status='COMPLETE', check_burst=cb.name, pack_burst=pk.parent.name if pk.exists() else None, transcribe_burst=tr.parent.name if tr.exists() else None,
                           clip=chk.get('clip'), clip_version=chk.get('clip_version'), flags=chk.get('flags', []) + CFLAGS.get(cell, []), transcriber_disagrees_with_intent=mism, transcriber_controls_caught=ctrl,
                           packet=f'../artifacts/{pk.parent.name}/packet/review.html' if pk.exists() else None)
json.dump(missing, open(out/'missing.json', 'w'), indent=1)
adv = R/'cells_advanced'; adv.mkdir(exist_ok=True)
for chk, cell in (('K1p-paintchk-idle-S-r2', 'idle_S'), ('K1p-paintchk-walk-E-r2', 'walk_E')):
    d = adv/cell
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(A/chk/'advanced/frames', d/'frames'); shutil.copyfile(A/chk/'advanced/registration.json', d/'registration.json')
v = R/'vfx_frames'
if v.exists(): shutil.rmtree(v)
shutil.copytree(A/'K4v-chk-01/vfx/frames', v)
json.dump(dict(generated_by='conductor assemble_cells.py (copy only)', cells=index), open(R/'matrix_index.json', 'w'), indent=1)
print('complete', sum(1 for x in index.values() if x['status'] == 'COMPLETE'), 'incomplete', missing)
