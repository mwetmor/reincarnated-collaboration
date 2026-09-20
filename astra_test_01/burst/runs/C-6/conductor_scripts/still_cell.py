# Conductor: a STILL → a one-frame cell (walk_<D> and idle_<D>) via the frozen matte + register (probe cells; no animation). usage: still_cell.py <still png> <D> <cells_dir> [pad_scale=0.7]
import sys, pathlib, json, tempfile, hashlib
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from oracle import video_cut as vc
from PIL import Image
import numpy as np
still, D, cells = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3]); scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.7
im = Image.open(still).convert('RGB'); a = np.asarray(im).astype(int)
plate = tuple(int(v) for v in np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0))   # the still's own plate colour
# re-key the still's own plate (any green Grok chose) to PURE #00ff00 so the frozen matte recognises it; figure pixels untouched
pl = np.array(plate); dist = np.abs(a - pl).sum(axis=2); mask = dist < 60
b = a.copy(); b[mask] = (0, 255, 0); im = Image.fromarray(b.astype(np.uint8)); plate = (0, 255, 0)
w, h = im.size; small = im.resize((round(w * scale), round(h * scale)), Image.NEAREST); canvas = Image.new('RGB', (768, 1168), plate); canvas.paste(small, ((768 - small.size[0]) // 2, (1168 - small.size[1]) // 2))
tmp = pathlib.Path(tempfile.mkdtemp(prefix=f'still_{D}_', dir='/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/c798c4cb-f5ae-4f80-8419-ca68760f2e6f/scratchpad')); p = tmp/'f_000.png'; canvas.save(p)
fr = vc.matte_frames([str(p)], edge_mode='clamp'); fr = (fr[0] if isinstance(fr, tuple) else fr)[0]
reg, transform = vc.register([fr, fr], anchor_index=0)
for kind in ('walk', 'idle'):
    d = cells/f'{kind}_{D}'; (d/'frames'/kind/D).mkdir(parents=True, exist_ok=True); (d/'frames'/'rest'/D).mkdir(parents=True, exist_ok=True)
    reg[0].save(d/'frames'/'rest'/D/f'rest_{D}.png'); reg[1].save(d/'frames'/kind/D/f'{kind}_{D}_00.png'); reg[1].save(d/'frames'/kind/D/f'{kind}_{D}_01.png')
    json.dump(dict(kind=kind, direction=D, source_still=str(still), still_sha256=hashlib.sha256(still.read_bytes()).hexdigest(), method='PROBE one-frame cell from a still (padded to %.2f on its own plate; frozen matte + register); no animation' % scale, transform=transform, conductor_derived=True, flags=['probe still cell — not animated']), open(d/'registration.json', 'w'), indent=1)
print(D, 'cells written', [f'walk_{D}', f'idle_{D}'], 'plate', plate, 'transform', json.dumps(transform)[:120])
