# Conductor-derived explicit regions/sockets (R-C3-16) from base frames at full resolution.
import sys, json, glob, pathlib
sys.path.insert(0, '/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad')
from staff_tip import tip
import numpy as np
from PIL import Image
R = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs')
def frames(d): return sorted(glob.glob(str(d) + '/*_[0-9][0-9].png'))
def regions(fs, view):
    out = []
    for f in fs:
        t = tip(f); a = np.array(Image.open(f).convert('RGBA'))[..., 3] >= 128; top, H = t['head_top'], t['H']
        tx, ty = t['tip']; half = 0.11 * H
        staff = [int(tx - half), int(ty - 0.06 * H - half), int(tx + half), int(ty - 0.06 * H + half)]
        band = a[int(top + 0.15 * H):int(top + 0.30 * H)]; cols = np.where(band.any(0))[0]
        if view == 'S':
            re = int(cols.max()); pa = [int(re - 0.18 * H), int(top + 0.12 * H), int(re + 10), int(top + 0.32 * H)]
        else:
            be = int(cols.min()); pa = [int(be - 6), int(top + 0.12 * H), int(be + 0.16 * H), int(top + 0.30 * H)]
        out.append(dict(frame=pathlib.Path(f).name, staff_tip=t['tip'], staff_head_box=[max(0, v) for v in staff], pauldron_box=[max(0, v) for v in pa], H=H, head_top=top))
    return out
res = {
 'idle_S': regions(frames(R/'C-1/artifacts/K3p-xv-idle-cut-01/frames/idle/S'), 'S'),
 'walk_E': regions(frames(R/'C-3/artifacts/P4c-E-walk/cut/frames/walk/E'), 'E'),
}
sock = [dict(frame=pathlib.Path(f).name, socket=tip(f)['tip']) for f in frames(R/'C-3/artifacts/P4c-S-cast/cut/frames/cast/S')]
od = R/'C-3/artifacts/P5-regions'; od.mkdir(exist_ok=True)
rule = 'R-C3-16: staff tip = topmost inlier of a RANSAC line through full-resolution thin (≤ 9 px) row/column alpha runs, head band excluded, extended upward through contiguous alpha; staff-head box = square 0.22·H centred 0.06·H above the tip; pauldron box S = [right shoulder edge − 0.18·H, head_top + 0.12·H, edge + 10, head_top + 0.32·H]; E = [back edge − 6, head_top + 0.12·H, back edge + 0.16·H, head_top + 0.30·H]'
for k, v in res.items(): json.dump(dict(rule=rule, frames=v), open(od/f'regions_{k}.json', 'w'), indent=1)
json.dump(dict(rule=rule.split(';')[0], frames=sock), open(od/'sockets_cast_S.json', 'w'), indent=1)
print({k: (v[0]['staff_head_box'], v[0]['pauldron_box']) for k, v in res.items()}, sock[:3])
