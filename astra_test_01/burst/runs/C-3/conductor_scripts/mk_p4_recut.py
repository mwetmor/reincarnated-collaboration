# Explicit-index re-cut CHECK briefs for one-shot cells (R-C3-17). Data, not lane code.
import json, pathlib, re
S = pathlib.Path('/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad')
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); XV = B/'runs/C-3/xvideo/in'
J = json.load(open(S/'jump_keys.json')); J.update(json.loads(__import__('subprocess').run(['python3', str(S/'oneshot_indices.py'), 'P4c-SE-jump'], capture_output=True, text=True).stdout))
C = json.load(open(S/'castkeys/cast_keys.json'))
cells = {}
for D in ['S', 'E', 'W', 'SW', 'SE']:
    v = J[f'P4c-{D}-jump']; cells[f'{D}_jump'] = (v['indices'], 12, 'explicit key poses from the frozen tool\'s own head/sole series with a floored settle tolerance' + ('; settle = closest return (no sustained return)' if v.get('settle_closest_return') else ''))
for D in ['S', 'E', 'W', 'N', 'SE', 'SW', 'NE']:
    v = C[f'{D}_cast']; cells[f'{D}_cast'] = (v['indices'], 20, 'explicit key poses from a FULL-RESOLUTION staff-tip series (R-C3-16 rule) — the tool\'s cast detection ran on the low-resolution tip proxy that tracks the hair' + ('; settle = closest return' if v.get('settle_closest_return') else '') + (f"; noisy tip baseline (tol {v['tol']} px)" if v['tol'] > 20 else ''))
base = json.load(open(B/'briefs/C-3/P4c-S-jump.task.json'))['text']
out = []
for cell, (idx, fps, why) in cells.items():
    D, a = cell.split('_'); bid = f'P4c-{D}-{a}-x'
    clip = XV/f'{cell}_v2.mp4'; ver = 'v2'
    if not clip.exists(): clip, ver = XV/f'{cell}.mp4', 'v1'
    src = json.load(open(B/f'briefs/C-3/P4c-{D}-{a}.task.json'))['text']
    i = src.index('STEP 1'); j = src.index('STEP 2')
    step1 = (f"STEP 1 — EXPLICIT CUT (conductor, ledger R-C3-17; K3p-xv-cut-04 precedent — there is NOTHING to detect or decide): the 8 native frame indices are {idx} ({why}). Using the frozen module functions only (`from oracle import video_cut as vc`): vc.split(clip, <a temp dir under out/tmp>, t_max_s=99) → take native frame 0 (the rest frame) and the 8 listed native frames → vc.matte_frames(those paths, edge_mode='clamp') → vc.register([rest] + the 8, anchor_index=0) (ONE uniform scale + ONE translation from the rest frame: height 240, sole 399, cx 255.5) → write out/cut/frames/rest/{D}/rest_{D}.png and out/cut/frames/{a}/{D}/{a}_{D}_00..07.png, out/cut/sheets/{a}_{D}_strip.png (frames on #3a3f4a, numbered), out/cut/registration.json = {{\"kind\":\"{a}\",\"direction\":\"{D}\",\"clip\":\"{clip.name}\",\"fps_out\":{fps},\"n\":8,\"indices_native\":{idx},\"selection_authority\":\"R-C3-17 explicit key poses\",\"transform\":<from register>,\"splice\":<vc.splice_check on the 145 native matted frames if cheap, else null with reason>}}. Delete out/tmp before returning. If a listed frame cannot be matted, report it and continue with the rest.\n")
    text = src[:i].replace(f'P4c-{D}-{a}', bid).replace('with the FROZEN cut tool', 'at EXPLICIT native indices with the frozen cut functions') + step1 + src[j:].replace(f'P4c-{D}-{a}', bid)
    text = re.sub(r'"cut":<the registration.json blocks:[^>]*>', '"cut":<out/cut/registration.json>', text)
    task = json.load(open(B/f'briefs/C-3/P4c-{D}-{a}.task.json')); task['text'] = text
    json.dump(task, open(B/f'briefs/C-3/{bid}.task.json', 'w'), indent=1, ensure_ascii=False); out.append(bid)
print(len(out), out)
