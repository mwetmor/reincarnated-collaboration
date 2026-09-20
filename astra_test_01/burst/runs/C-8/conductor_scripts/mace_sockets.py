# Conductor MACE-HEAD socket PROPOSAL for C-8 cast cells (W3 ruling: cast = shield slam, socket at the mace head). blade_sockets.py lineage:
# the script PROPOSES per frame the alpha pixel farthest from the hip above the foot band (= the thrust mace head / slammed shield edge); the
# MARKED SHEET is the authority. Conductor OVERRIDES (from the eye read of the one-shot sheets) live in OVERRIDE below. Mirrored cells: x' = 511 - x.
# Output: runs/C-8/sockets_v1.json (exporter schema v1: version, canvas, cells{cast_<D>:{sockets, measurements, release_index, release_socket_rule}})
import json, glob, pathlib, hashlib
from PIL import Image, ImageDraw
import numpy as np
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); C = B/'runs/C-8/cells'; SH = B/'runs/C-8/artifacts/sockets-sheets'; SH.mkdir(parents=True, exist_ok=True)
RULE = "C-8 R-MACE (W3): release socket = mace head at the slam frame — the alpha pixel farthest from the hip point of the rest frame above the foot band (bottom 15 %); conductor-proposed, marked-sheet audited; S faces the camera so the thrust shortens on screen — its release frame and socket come from the mace-head GLINT (conductor override, P4-W4-W5-CUTS); mirrored cells take the source socket with x flipped (511 - x)."
OVERRIDE = {'S': dict(release_index=4, socket=[249, 265], reason='mace-head glint centre (112 px, frame 4 = native 71); the far-point rule caught the side wind-up on the toward-camera thrust')}
out = {'version': 1, 'canvas': [512, 512], 'cells': {}, 'notes': RULE, 'conductor_derived': True, 'script_sha256': hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
def tip(im, rest=None):
    # blade tip = the alpha pixel FARTHEST from the hip point (body column x from the sole row of the REST frame; y = sole - 0.5 H):
    # the scythe's reach exceeds the head's and the feet's in every sweep — raised (above the head) or swept low and forward.
    a = np.array(im.convert('RGBA'))[..., 3] >= 128; ys, xs = np.nonzero(a)
    if not len(ys): return None, 'empty_alpha'
    r = np.array(rest.convert('RGBA'))[..., 3] >= 128 if rest is not None else a; rys, rxs = np.nonzero(r)
    sole = int(rys.max()); crown = int(rys.min()); cx = int(np.median(rxs[rys > sole - 30])); hip = (cx, sole - 0.5 * (sole - crown))
    keep = ys < sole - 0.15 * (sole - crown)   # feet can never be the socket: exclude the bottom 15 % of the figure
    xs, ys = xs[keep], ys[keep]
    if not len(ys): return None, 'no_alpha_above_feet'
    d = (xs - hip[0]) ** 2 + (ys - hip[1]) ** 2; k = int(np.argmax(d)); return [int(xs[k]), int(ys[k])], 'ok_farthest_from_hip_above_feet'
_cells = sorted(C.glob('cast_*'), key=lambda c: (bool(json.load(open(c/'registration.json')).get('mirrored')), c.name))  # unique first, then mirrored
for cd in _cells:
    d = cd.name.split('_')[1]; reg = json.load(open(cd/'registration.json')); frames = sorted(glob.glob(str(cd/'frames'/'cast'/d/'*.png')))
    if reg.get('mirrored'):
        src = out['cells'].get(f"cast_{reg['mirror_of'].split('_')[1]}")
        if src is None: continue
        rec = {'sockets': [[511 - p[0], p[1]] if p else None for p in src['sockets']], 'measurements': [dict(m, tip=([511 - m['tip'][0], m['tip'][1]] if m.get('tip') else None), reason=m['reason'] + ' (mirrored x)') for m in src['measurements']], 'release_index': src['release_index'], 'release_socket_rule': RULE + ' [mirror of ' + reg['mirror_of'] + ']'}
    else:
        keys = reg.get('keys') or {}; idx = reg.get('indices_native') or []
        rel = idx.index(keys['release']) if keys.get('release') in idx else 3
        ms = []
        rest = Image.open(cd/'frames'/'rest'/d/f'rest_{d}.png')
        for f in frames:
            t, reason = tip(Image.open(f), rest); ms.append({'tip': t, 'reason': reason, 'method': 'farthest_alpha_from_hip'})
        rec = {'sockets': [m['tip'] for m in ms], 'measurements': ms, 'release_index': rel, 'release_socket_rule': RULE}
        # GLINT rule (W3 prompt asked for a pale glint ON the mace head at the slam): at the release frame, a bright low-saturation cluster
        # (>= 15 px) is the mace head → it beats the far-point proposal there. S's release frame itself is overridden below (toward-camera thrust).
        ri = OVERRIDE[d]['release_index'] if d in OVERRIDE else rec['release_index']
        gim = np.asarray(Image.open(frames[ri]).convert('RGBA')).astype(int); ga = gim[..., 3] > 128; mx = gim[..., :3].max(2); mn = gim[..., :3].min(2)
        gl = ga & (mx > 215) & ((mx - mn) < 45); gys, gxs = np.nonzero(gl)
        if len(gxs) >= 15:
            g = [int(np.median(gxs)), int(np.median(gys))]; rec['release_index'] = ri; rec['sockets'][ri] = g
            rec['measurements'][ri] = dict(tip=g, reason=f'mace-head glint centre ({len(gxs)} px) at the release frame', method='glint_centre'); rec['glint'] = dict(px=int(len(gxs)), centre=g)
        elif d in OVERRIDE:
            o = OVERRIDE[d]; rec['release_index'] = o['release_index']; rec['sockets'][o['release_index']] = o['socket']; rec['measurements'][o['release_index']] = dict(tip=o['socket'], reason=o['reason'], method='conductor_override_glint'); rec['override'] = o
    out['cells'][f'cast_{d}'] = rec
    # marked audit sheet: each frame at 1:1 with a crosshair at the proposed socket; the release frame boxed
    n = len(frames); sheet = Image.new('RGB', (n * 262, 300), (58, 63, 74)); dr = ImageDraw.Draw(sheet)
    for i, f in enumerate(frames):
        im = Image.open(f).convert('RGBA'); t = im.copy(); t.thumbnail((250, 250)); sheet.paste(t, (i * 262 + 6, 40), t)
        p = rec['sockets'][i]
        if p:
            s = 250 / 512; x, y = i * 262 + 6 + p[0] * s, 40 + p[1] * s; dr.line([(x - 8, y), (x + 8, y)], fill=(255, 60, 60), width=2); dr.line([(x, y - 8), (x, y + 8)], fill=(255, 60, 60), width=2)
        dr.text((i * 262 + 8, 8), f'{i}' + (' RELEASE' if i == rec['release_index'] else ''), fill=(255, 230, 120) if i == rec['release_index'] else 'white')
        if i == rec['release_index']: dr.rectangle([i * 262 + 4, 38, i * 262 + 258, 292], outline=(255, 230, 120), width=2)
    sheet.save(SH/f'sockets_{d}.png')
    print(f'cast_{d}', 'release', rec['release_index'], 'socket@release', rec['sockets'][rec['release_index']], '| all', rec['sockets'])
json.dump(out, open(B/'runs/C-8/sockets_v1.json', 'w'), indent=1)
print('cells', list(out['cells'].keys()))
