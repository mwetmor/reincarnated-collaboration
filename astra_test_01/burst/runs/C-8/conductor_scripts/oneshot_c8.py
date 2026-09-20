# Conductor EXPLICIT one-shot cut for C-8 (pixel EoR Warlord) cast/jump cells — C-6 oneshot_cell.py lineage (R-C3-17 method on the FROZEN module).
# CAST tracker changed for the shield-slam: the Warlord has no tall blade, so the tracked point is the alpha pixel FARTHEST from the figure
# centroid ABOVE the foot band (bottom 18 % of the figure) = the thrust mace head / slammed shield edge; release = max extension. Jump keys unchanged (sole row + height).
# usage: oneshot_c8.py <cell e.g. S_cast> [<mp4 relpath>]  → runs/C-8/p4/<cell>/cut/{frames,sheets,registration.json,keys.json}
import sys, os, json, pathlib, tempfile, shutil, hashlib
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from oracle import video_cut as vc
import numpy as np
from PIL import Image, ImageDraw
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
cell = sys.argv[1]; D, kind = cell.split('_')[0], cell.split('_')[1]
clip = B/(sys.argv[2] if len(sys.argv) > 2 else f'runs/C-8/xvideo/in/{cell}.mp4')
out = B/f'runs/C-8/p4/{cell}/cut'
if out.exists(): shutil.rmtree(out)
(out/'frames'/kind/D).mkdir(parents=True); (out/'frames'/'rest'/D).mkdir(parents=True); (out/'sheets').mkdir()
wd = pathlib.Path(tempfile.mkdtemp(prefix=f'{cell}_', dir='/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/c798c4cb-f5ae-4f80-8419-ca68760f2e6f/scratchpad'))
m = vc.split(str(clip), str(wd), t_max_s=99); paths = m['paths']; fps = m.get('fps', 24.0)
fr = []; invalid = []
for i, pth in enumerate(paths):
    try:
        r = vc.matte_frames([pth], edge_mode='clamp'); fr.append((r[0] if isinstance(r, tuple) else r)[0])
    except ValueError as ex:  # figure touches the frame border → frozen matte refuses; frame invalid (C-3 cast_S precedent)
        fr.append(None); invalid.append(i)
def feats(im):
    if im is None: return dict(tip=None, sole=None, h=None)
    a = np.array(im)[..., 3] >= 128; ys, xs = np.nonzero(a)
    if not len(ys): return dict(tip=None, sole=None, h=None)
    top = int(ys.min()); bot = int(ys.max()); cy, cx = ys.mean(), xs.mean()
    keep = ys < bot - 0.18 * (bot - top)  # exclude the foot band
    dd = (ys[keep] - cy) ** 2 + (xs[keep] - cx) ** 2; k = int(np.argmax(dd))
    return dict(tip=(int(xs[keep][k]), int(ys[keep][k])), sole=bot, h=int(bot - top), centroid=(float(cx), float(cy)))
F = [feats(im) for im in fr]; n = len(F)
P = np.array([f['tip'] if f['tip'] else [np.nan, np.nan] for f in F], float); sole = np.array([f['sole'] if f['sole'] is not None else np.nan for f in F], float); H = np.array([f['h'] if f['h'] is not None else np.nan for f in F], float)
def first(cond, start, sustain):
    run = 0
    for i in range(start, n):
        run = run + 1 if cond(i) else 0
        if run >= sustain: return i - sustain + 1
    return None
keys = dict(cell=cell, kind=kind, clip=clip.name, clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(), n_native=n, fps=fps, tracker='farthest-from-centroid alpha pixel above the foot band = mace head / shield edge (cast) / sole row + height (jump)')
if kind == 'cast':
    base = np.nanmedian(P[:12], 0); noise = float(np.nanstd(np.linalg.norm(P[:12] - base, axis=1))); d = np.linalg.norm(P - base, axis=1); tol = max(3 * noise, 0.03 * np.nanmedian(H[:12]))
    onset = first(lambda i: np.isfinite(d[i]) and d[i] > tol, int(os.environ.get('CAST_START', 12)), 2)  # CAST_START: conductor skips early far-point noise (N_cast precedent)
    if os.environ.get('CAST_START'): keys['flags_pre'] = keys.get('flags_pre', []) + [f"onset search started at native {os.environ['CAST_START']} (CAST_START) — early far-point noise skipped"]
    keys.update(baseline=[round(float(x), 1) for x in base], noise=round(noise, 2), tol=round(float(tol), 2), onset=onset)
    if onset is not None:
        settle = first(lambda i: np.isfinite(d[i]) and d[i] <= tol, onset + 4, 6); closest = False
        if settle is None:
            pk = onset + int(np.nanargmax(np.where(np.isfinite(d[onset:]), d[onset:], -1))); tail = [(d[i], i) for i in range(pk + 6, n) if np.isfinite(d[i])]
            if tail: settle = min(tail)[1]; closest = True
        end = settle if settle is not None else n - 1
        if os.environ.get('CAST_END'):  # conductor window cap: Grok repeated the slam; keep the FIRST action (SW_cast precedent)
            end = min(end, int(os.environ['CAST_END'])); settle = end; keys['flags_pre'] = keys.get('flags_pre', []) + [f'window capped at native {end} (CAST_END) — second slam excluded']
        C = np.array([f['centroid'] if f.get('centroid') else [np.nan, np.nan] for f in F], float); ext = np.linalg.norm(P - C, axis=1)
        rel_win = [i for i in range(onset + 1, end) if np.isfinite(ext[i])]
        release = max(rel_win, key=lambda i: ext[i]) if rel_win else None   # full extension = the slam
        gseg = [i for i in range(onset, release) if np.isfinite(ext[i])] if release else []
        gather = min(gseg, key=lambda i: ext[i]) if gseg else None          # drawn back before the slam
        keys['extension_series'] = [None if not np.isfinite(e) else round(float(e), 1) for e in ext]
        keys.update(settle=settle, settle_closest_return=closest, gather=gather, release=release, max_displacement=round(float(np.nanmax(d[onset:end])), 1))
        if None not in (gather, release, settle) and onset <= gather < release < settle:  # gather may coincide with onset (N_cast: the draw-back is the first motion seen from behind); the monotonic bump below separates them
            L = settle - release
            idx = [onset, round((onset + gather) / 2), gather, release, release + max(1, round(0.25 * L)), release + max(2, round(0.5 * L)), release + max(3, round(0.8 * L)), settle]
            for j in range(1, 8):
                if idx[j] <= idx[j-1]: idx[j] = idx[j-1] + 1
            keys['indices'] = idx; keys['status'] = 'explicit_far_point'
    keys['tip_y_series'] = [None if not np.isfinite(y) else int(y) for y in P[:, 1]]
else:  # jump
    b_sole = float(np.nanmedian(sole[:12])); b_h = float(np.nanmedian(H[:12])); tol = max(3 * float(np.nanstd(H[:12])), 0.03 * b_h)
    dh = b_h - H  # positive when crouched (shorter)
    onset = first(lambda i: np.isfinite(dh[i]) and abs(dh[i]) > tol, int(os.environ.get('JUMP_START', 12)), 2)  # JUMP_START: skip early height noise (E_jump precedent: four standing frames before the crouch)
    if os.environ.get('JUMP_START'): keys['flags_pre'] = keys.get('flags_pre', []) + [f"onset search started at native {os.environ['JUMP_START']} (JUMP_START) — early height noise skipped"]
    keys.update(baseline_sole=round(b_sole, 1), baseline_h=round(b_h, 1), tol=round(tol, 2), onset=onset)
    if onset is not None:
        airborne = [i for i in range(onset, n) if np.isfinite(sole[i]) and b_sole - sole[i] > tol]
        take_off = airborne[0] if airborne else None; touchdown = (airborne[-1] + 1) if airborne else None
        apex = int(np.nanargmin(np.where(np.arange(n) >= (take_off or onset), sole, np.inf))) if take_off else None
        crouch = onset + int(np.nanargmax(dh[onset:take_off])) if take_off and take_off > onset else None
        settle = first(lambda i: np.isfinite(dh[i]) and abs(dh[i]) <= tol and abs(sole[i] - b_sole) <= tol, (touchdown or onset) + 2, 6) if touchdown else None
        landing = (touchdown + int(np.nanargmax(dh[touchdown:(settle or n)]))) if touchdown and (settle or n) > touchdown else None
        if settle is None and landing is not None:
            valid_tail = [i for i in range(landing + 6, n) if fr[i] is not None]
            if valid_tail: settle = valid_tail[-1]; keys.setdefault('flags_pre', []).append(f'no six-sample settle after landing → last valid frame {settle} taken as settle (charter best-candidate fallback, FLAGGED)')
        keys.update(crouch=crouch, take_off=take_off, apex=apex, touchdown=touchdown, landing_crouch=landing, settle=settle)
        if None not in (crouch, take_off, apex, touchdown, landing, settle) and onset < crouch < take_off < apex < touchdown <= landing < settle:
            idx = [onset, crouch, take_off, round((take_off + apex) / 2), apex, round((apex + touchdown) / 2), landing, settle]
            for j in range(1, 8):
                if idx[j] <= idx[j-1]: idx[j] = idx[j-1] + 1
            keys['indices'] = idx; keys['status'] = 'explicit_sole_height'
    keys['sole_series'] = [None if not np.isfinite(s) else int(s) for s in sole]; keys['h_series'] = [None if not np.isfinite(h) else int(h) for h in H]
keys['invalid_native_indices'] = invalid; keys['flags'] = keys.pop('flags_pre', []) + ([f'{len(invalid)} native frames touch the frame border (blade/jump leaves the plate) — matte refused; excluded from the series'] if invalid else [])
if 'indices' in keys and invalid:
    valid = [i for i in range(n) if fr[i] is not None]
    fixed = [min(valid, key=lambda v: abs(v - i)) for i in keys['indices']]
    if fixed != keys['indices']: keys['flags'].append(f"key frames moved to nearest valid: {keys['indices']} → {fixed}"); keys['indices'] = fixed
    for j in range(1, 8):
        if keys['indices'][j] <= keys['indices'][j-1]: keys['indices'][j] = keys['indices'][j-1] + 1
    if fr[0] is None or any(fr[i] is None for i in keys['indices']): keys.pop('indices'); keys['status'] = 'unresolved: rest or key frame invalid'
keys.setdefault('status', 'unresolved')
json.dump(keys, open(out/'keys.json', 'w'), indent=1)
if 'indices' in keys:
    idx = keys['indices']; reg_frames, transform = vc.register([fr[0]] + [fr[i] for i in idx], anchor_index=0)
    reg_frames[0].save(out/'frames'/'rest'/D/f'rest_{D}.png')
    for k, im in enumerate(reg_frames[1:]): im.save(out/'frames'/kind/D/f'{kind}_{D}_{k:02d}.png')
    strip = Image.new('RGB', (9 * 260, 300), (58, 63, 74)); dr = ImageDraw.Draw(strip)
    for k, im in enumerate(reg_frames):
        t = im.copy(); t.thumbnail((250, 250)); strip.paste(t, (k * 260 + 5, 40), t); dr.text((k * 260 + 6, 8), 'rest' if k == 0 else f'{k-1} · native {idx[k-1]}', fill='white')
    if kind == 'cast' and keys.get('release') is not None:
        rel_pos = idx.index(keys['release']); im = reg_frames[rel_pos + 1]; a = np.array(im)[..., 3] >= 128; ys, xs = np.nonzero(a)
        top, bot = ys.min(), ys.max(); cy, cx = ys.mean(), xs.mean(); keep = ys < bot - 0.18 * (bot - top)
        k = int(np.argmax((ys[keep] - cy) ** 2 + (xs[keep] - cx) ** 2)); sx, sy = int(xs[keep][k]), int(ys[keep][k])
        sc = 250 / max(im.size); ox = (rel_pos + 1) * 260 + 5 + int(sx * sc); oy = 40 + int(sy * sc)
        dr.ellipse((ox - 5, oy - 5, ox + 5, oy + 5), outline='red', width=2); dr.text(((rel_pos + 1) * 260 + 6, 24), f'socket? ({sx},{sy})', fill='red')
        json.dump(dict(version=1, canvas=list(im.size), cell=f'cast_{D}', release_index=rel_pos, socket_proposed=[sx, sy], rule='farthest-from-centroid above the foot band at the release frame — script PROPOSES, marked sheet DECIDES', conductor_derived=True), open(out/'socket_proposed.json', 'w'), indent=1)
    strip.save(out/'sheets'/f'{kind}_{D}_strip.png')
    json.dump(dict(kind=kind, direction=D, clip=str(clip), clip_sha256=keys['clip_sha256'], method='explicit one-shot (conductor keys, R-C3-17 lineage; far-point tracker for the shield slam)', indices_native=idx, keys={k: keys.get(k) for k in ('onset','crouch','take_off','apex','touchdown','landing_crouch','gather','release','settle')}, transform=transform, fps=fps, n_native=n, invalid_native_indices=invalid, flags=keys['flags'], conductor_derived=True, script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()), open(out/'registration.json', 'w'), indent=1)
print(cell, keys['status'], {k: keys.get(k) for k in ('onset','gather','release','crouch','take_off','apex','touchdown','landing_crouch','settle','indices')})
shutil.rmtree(wd, ignore_errors=True)
