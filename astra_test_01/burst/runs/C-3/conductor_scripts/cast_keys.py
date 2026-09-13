# Conductor full-resolution cast key poses (R-C3-17): frozen split + matte (clamp), each native frame scaled so the rest figure is 240 px tall, staff tip by the R-C3-16 rule.
import sys, json, pathlib, tempfile
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); sys.path.insert(0, '/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad')
from oracle import video_cut as vc
from staff_tip import tip
import numpy as np
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-3'); SC = pathlib.Path('/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad/castkeys')
out = {}
for cell in sys.argv[1:]:
    D = cell.split('_')[0]; clip = B/'xvideo/in'/f'{cell}_v2.mp4'
    if not clip.exists(): clip = B/'xvideo/in'/f'{cell}.mp4'
    import os; wd = SC/f'{cell}_{os.getpid()}'; m = vc.split(str(clip), str(wd), t_max_s=99); fr = vc.matte_frames(m['paths'], edge_mode='clamp')
    a0 = np.array(fr[0])[..., 3] >= 128; ys = np.where(a0.any(1))[0]; s = 240.0 / (ys[-1] - ys[0])
    T = []
    for k in range(len(fr)):
        im = Image.fromarray(np.array(fr[k])) if not isinstance(fr[k], Image.Image) else fr[k]
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        try: t = tip(im)['tip']
        except Exception: t = None
        T.append(t)
    P = np.array([t if t else [np.nan, np.nan] for t in T], float)
    base = np.nanmedian(P[:12], 0); noise = float(np.nanstd(np.linalg.norm(P[:12] - base, axis=1))); d = np.linalg.norm(P - base, axis=1)
    tol = max(3 * noise, 0.03 * 240)
    def first(cond, start, sustain):
        run = 0
        for i in range(start, len(d)):
            run = run + 1 if cond(i) else 0
            if run >= sustain: return i - sustain + 1
        return None
    onset = first(lambda i: np.isfinite(d[i]) and d[i] > tol, 12, 2)
    res = dict(clip=clip.name, scale=round(s, 4), baseline=[round(float(x), 1) for x in base], noise=round(noise, 2), tol=round(tol, 2), onset=onset)
    if onset is not None:
        settle = first(lambda i: np.isfinite(d[i]) and d[i] <= tol, onset + 4, 6)
        closest = False
        if settle is None:
            # closest-return fallback (R-C3-17): the frame after the peak displacement where the tip is nearest rest
            pk = onset + int(np.nanargmax(np.where(np.isfinite(d[onset:]), d[onset:], -1)))
            tail = [(d[i], i) for i in range(pk + 6, len(d)) if np.isfinite(d[i])]
            if tail: settle = min(tail)[1]; closest = True
        end = settle if settle is not None else len(d) - 1
        seg = P[onset:end, 1]; gather = onset + int(np.nanargmin(seg)) if np.isfinite(seg).any() else None
        sp = np.r_[0, np.linalg.norm(np.diff(P, axis=0), axis=1)]
        rel_win = [i for i in range((gather or onset) + 1, min(end, (gather or onset) + 36)) if np.isfinite(sp[i])]
        release = max(rel_win, key=lambda i: sp[i]) if rel_win else None
        res.update(settle_closest_return=closest, settle=settle, gather=gather, release=release, max_displacement=round(float(np.nanmax(d[onset:end])), 1))
        if None not in (gather, release, settle) and onset < gather < release < settle:
            L = settle - release
            idx = [onset, round((onset + gather) / 2), gather, release, release + max(1, round(0.25 * L)), release + max(2, round(0.5 * L)), release + max(3, round(0.8 * L)), settle]
            for j in range(1, len(idx)):
                if idx[j] <= idx[j-1]: idx[j] = idx[j-1] + 1
            res['indices'] = idx; res['status'] = 'explicit_full_res'
    res.setdefault('status', 'unresolved')
    res['tip_y_series'] = [None if not t else round(t[1]) for t in T]
    out[cell] = res
    print(cell, {k: res.get(k) for k in ('clip', 'onset', 'gather', 'release', 'settle', 'indices', 'status', 'tol', 'max_displacement')}, flush=True)
prev = json.load(open(SC/'cast_keys.json')) if (SC/'cast_keys.json').exists() else {}
prev.update(out); json.dump(prev, open(SC/'cast_keys.json', 'w'), indent=1)
